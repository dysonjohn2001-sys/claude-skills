FROM python:3.12-slim

# ffmpeg does the cutting and rendering; tesseract backs the optional
# jersey-number reader. Neither is bundled in the base image.
RUN apt-get update && apt-get install -y --no-install-recommends \
      ffmpeg \
      tesseract-ocr \
      libgl1 \
      libglib2.0-0 \
      fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY worker/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY worker/ /app/
COPY shared/ /shared/
ENV PYTHONUNBUFFERED=1 \
    PHG_MEDIA_ROOT=/media \
    PHG_WORK_ROOT=/tmp/phg-work

RUN useradd --create-home --shell /bin/bash phg && mkdir -p /media /tmp/phg-work \
    && chown -R phg:phg /media /tmp/phg-work
USER phg

CMD ["python", "-m", "phg.cli", "worker"]
