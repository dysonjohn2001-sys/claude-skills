"""Jersey-number recognition - the SECONDARY matching signal only.

Design constraints, in force everywhere in this file:

  * No facial recognition, no face detection, no biometric template of any
    kind. The only thing extracted from a frame is printed digits on fabric.
  * This module never assigns a player. It returns digit observations. The
    confidence model folds them in with a hard cap (confidence.apply_jersey),
    so a good read can nudge and a bad read cannot overturn the scorebook.
  * It only runs on clips whose schedule-based confidence landed in the
    uncertain band, because it is the most expensive step in the pipeline and
    the least reliable on 1080p youth footage shot from the bleachers.

Pipeline per sampled frame: person bounding boxes from OpenCV's stock HOG
pedestrian detector -> crop the upper-back band of each box -> upscale,
grayscale, CLAHE, Otsu -> Tesseract restricted to digits.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass

import cv2
import numpy as np

from phg.models import JerseyObservation

log = logging.getLogger(__name__)

_DIGITS = re.compile(r"^\d{1,2}$")

try:  # Tesseract is optional; without it the pipeline degrades, it does not fail.
    import pytesseract

    _HAS_TESSERACT = True
except Exception:  # pragma: no cover - import guard
    pytesseract = None  # type: ignore[assignment]
    _HAS_TESSERACT = False

# OpenCV 5 removed HOGDescriptor and its stock pedestrian detector. Jersey
# reading needs OpenCV 4.x; on 5.x it turns itself off rather than failing, and
# matching carries on with the schedule signals it was always meant to lead on.
_HAS_PERSON_DETECTOR = hasattr(cv2, "HOGDescriptor") and hasattr(
    cv2, "HOGDescriptor_getDefaultPeopleDetector"
)


@dataclass(frozen=True)
class OcrSettings:
    samples_per_clip: int = 12
    min_person_height_px: int = 90
    # Fraction of a person box treated as "where a number is printed".
    back_band_top: float = 0.18
    back_band_bottom: float = 0.52
    upscale: int = 4
    min_ocr_confidence: float = 0.55
    max_people_per_frame: int = 6


class JerseyReader:
    def __init__(self, settings: OcrSettings | None = None) -> None:
        self.settings = settings or OcrSettings()
        self._clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        self._hog = None
        if _HAS_PERSON_DETECTOR:
            self._hog = cv2.HOGDescriptor()
            self._hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    @property
    def available(self) -> bool:
        """Whether a jersey read can be attempted at all.

        Constructing this class must never raise. It is an optional secondary
        signal, and a missing dependency has to degrade matching, not break it.
        """
        return _HAS_TESSERACT and self._hog is not None

    @property
    def unavailable_reason(self) -> str:
        if not _HAS_PERSON_DETECTOR:
            return (
                f"OpenCV {cv2.__version__} has no HOGDescriptor; jersey reading needs "
                "opencv-python-headless 4.x"
            )
        if not _HAS_TESSERACT:
            return "tesseract is not installed"
        return ""

    # -- public -----------------------------------------------------------

    def read_window(
        self, video_path: str, start_seconds: float, end_seconds: float
    ) -> list[JerseyObservation]:
        """Sample the window and return every digit string we could read."""
        if not self.available:
            log.warning("skipping jersey recognition: %s", self.unavailable_reason)
            return []

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            log.error("could not open %s for jersey reading", video_path)
            return []

        try:
            return self._scan(cap, start_seconds, end_seconds)
        finally:
            cap.release()

    # -- internals --------------------------------------------------------

    def _scan(self, cap, start: float, end: float) -> list[JerseyObservation]:
        n = max(1, self.settings.samples_per_clip)
        step = (end - start) / n
        observations: list[JerseyObservation] = []

        for i in range(n):
            t = start + step * (i + 0.5)
            cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000.0)
            ok, frame = cap.read()
            if not ok or frame is None:
                continue
            for digits, conf, bbox in self._read_frame(frame):
                observations.append(
                    JerseyObservation(
                        video_seconds=round(t, 3),
                        digits=digits,
                        ocr_confidence=round(conf, 3),
                        bbox=bbox,
                    )
                )
        return observations

    def _read_frame(self, frame: np.ndarray) -> list[tuple[str, float, tuple[int, int, int, int]]]:
        boxes = self._detect_people(frame)
        out: list[tuple[str, float, tuple[int, int, int, int]]] = []
        for (x, y, w, h) in boxes[: self.settings.max_people_per_frame]:
            if h < self.settings.min_person_height_px:
                continue
            crop = self._back_band(frame, x, y, w, h)
            if crop is None:
                continue
            digits, conf = self._ocr(crop)
            if digits and conf >= self.settings.min_ocr_confidence:
                out.append((digits, conf, (int(x), int(y), int(w), int(h))))
        return out

    def _detect_people(self, frame: np.ndarray) -> list[tuple[int, int, int, int]]:
        if self._hog is None:
            return []
        # Downscale first: the stock HOG detector is slow and the extra
        # resolution buys nothing at bleacher distance.
        height = frame.shape[0]
        scale = 640.0 / max(1, frame.shape[1])
        small = cv2.resize(frame, None, fx=scale, fy=scale) if scale < 1.0 else frame
        rects, weights = self._hog.detectMultiScale(
            small, winStride=(8, 8), padding=(8, 8), scale=1.05
        )
        inv = 1.0 / scale if scale < 1.0 else 1.0
        boxes = []
        for (x, y, w, h), weight in zip(rects, weights if len(weights) else [1.0] * len(rects)):
            if float(weight) < 0.3:
                continue
            boxes.append((int(x * inv), int(y * inv), int(w * inv), int(h * inv)))
        # Biggest first: the closest player is the one most likely to be legible.
        boxes.sort(key=lambda b: b[3], reverse=True)
        del height
        return boxes

    def _back_band(self, frame: np.ndarray, x: int, y: int, w: int, h: int) -> np.ndarray | None:
        top = int(y + h * self.settings.back_band_top)
        bottom = int(y + h * self.settings.back_band_bottom)
        left = max(0, x)
        right = min(frame.shape[1], x + w)
        top = max(0, top)
        bottom = min(frame.shape[0], bottom)
        if bottom - top < 12 or right - left < 12:
            return None
        return frame[top:bottom, left:right]

    def _ocr(self, crop: np.ndarray) -> tuple[str | None, float]:
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(
            gray, None, fx=self.settings.upscale, fy=self.settings.upscale,
            interpolation=cv2.INTER_CUBIC,
        )
        gray = self._clahe.apply(gray)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Numbers are printed light-on-dark about as often as dark-on-light.
        best: tuple[str | None, float] = (None, 0.0)
        for image in (binary, cv2.bitwise_not(binary)):
            digits, conf = self._tesseract(image)
            if digits and conf > best[1]:
                best = (digits, conf)
        return best

    def _tesseract(self, image: np.ndarray) -> tuple[str | None, float]:
        assert pytesseract is not None
        config = "--psm 8 -c tessedit_char_whitelist=0123456789"
        try:
            data = pytesseract.image_to_data(
                image, config=config, output_type=pytesseract.Output.DICT
            )
        except Exception as exc:  # pragma: no cover - runtime environment issue
            log.warning("tesseract failed: %s", exc)
            return None, 0.0

        best_text, best_conf = None, 0.0
        for text, conf in zip(data.get("text", []), data.get("conf", [])):
            text = (text or "").strip()
            try:
                conf_val = float(conf)
            except (TypeError, ValueError):
                continue
            if conf_val < 0 or not _DIGITS.match(text):
                continue
            normalized = conf_val / 100.0
            if normalized > best_conf:
                best_text, best_conf = text, normalized
        return best_text, best_conf


def summarize(observations: list[JerseyObservation]) -> list[tuple[str, float]]:
    """Collapse raw observations into (digits, summed_confidence) pairs."""
    totals: dict[str, float] = {}
    for obs in observations:
        key = obs.digits.lstrip("0") or "0"
        totals[key] = totals.get(key, 0.0) + obs.ocr_confidence
    return sorted(totals.items(), key=lambda kv: kv[1], reverse=True)
