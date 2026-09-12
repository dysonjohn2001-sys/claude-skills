"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { CATEGORY_LABEL, confidenceLabel, explainConfidence, timecode } from "@/lib/format";

export interface ReviewClip {
  id: string;
  playerId: string;
  playerName: string;
  jerseyNumber: string | null;
  mediaAssetId: string;
  category: "offense" | "defense" | "pitching" | "baserunning";
  sourceStart: number;
  sourceEnd: number;
  preRoll: number;
  postRoll: number;
  matchConfidence: number;
  matchMethod: string;
  confidenceFactors: Record<string, number>;
  reviewStatus: "auto_approved" | "needs_review" | "approved" | "rejected";
  rankScore: number;
  title: string;
  playDescription: string | null;
  inning: number | null;
  half: string | null;
  playId: string | null;
  thumbnailUrl: string | null;
}

export interface ReviewMedia {
  id: string;
  label: string;
  url: string;
  durationSeconds: number;
}

export interface RosterOption {
  id: string;
  name: string;
  jerseyNumber: string | null;
}

const CATEGORIES = ["offense", "defense", "pitching", "baserunning"] as const;

export default function ReviewWorkspace({
  gameId,
  media,
  clips: initialClips,
  roster,
}: {
  gameId: string;
  media: ReviewMedia[];
  clips: ReviewClip[];
  roster: RosterOption[];
}) {
  const [clips, setClips] = useState(initialClips);
  const [assetId, setAssetId] = useState(media[0]?.id ?? "");
  const [selectedId, setSelectedId] = useState<string | null>(
    initialClips.find((c) => c.reviewStatus === "needs_review")?.id ?? initialClips[0]?.id ?? null,
  );
  const [filter, setFilter] = useState<"needs_review" | "all" | (typeof CATEGORIES)[number]>(
    "needs_review",
  );
  const [playhead, setPlayhead] = useState(0);
  const [busy, setBusy] = useState(false);
  const [flash, setFlash] = useState<string | null>(null);
  const videoRef = useRef<HTMLVideoElement>(null);

  const asset = media.find((m) => m.id === assetId) ?? media[0];
  const visible = useMemo(() => {
    const onAsset = clips.filter((c) => c.mediaAssetId === asset?.id);
    if (filter === "all") return onAsset;
    if (filter === "needs_review") return onAsset.filter((c) => c.reviewStatus === "needs_review");
    return onAsset.filter((c) => c.category === filter);
  }, [clips, asset?.id, filter]);

  const selected = clips.find((c) => c.id === selectedId) ?? null;

  const seek = useCallback((seconds: number) => {
    const video = videoRef.current;
    if (!video) return;
    video.currentTime = Math.max(0, seconds);
    setPlayhead(seconds);
  }, []);

  const selectClip = useCallback(
    (clip: ReviewClip) => {
      setSelectedId(clip.id);
      if (clip.mediaAssetId !== asset?.id) setAssetId(clip.mediaAssetId);
      seek(clip.sourceStart);
    },
    [asset?.id, seek],
  );

  const step = useCallback(
    (delta: number) => {
      if (!visible.length) return;
      const index = visible.findIndex((c) => c.id === selectedId);
      const next = visible[Math.min(visible.length - 1, Math.max(0, index + delta))];
      if (next) selectClip(next);
    },
    [visible, selectedId, selectClip],
  );

  const patchClip = useCallback(
    async (clipId: string, body: Record<string, unknown>, note: string) => {
      setBusy(true);
      try {
        const response = await fetch(`/api/clips/${clipId}`, {
          method: "PATCH",
          headers: { "content-type": "application/json" },
          body: JSON.stringify(body),
        });
        if (!response.ok) throw new Error((await response.json()).error ?? "Update failed");
        const updated: ReviewClip = await response.json();
        setClips((all) => all.map((c) => (c.id === clipId ? { ...c, ...updated } : c)));
        setFlash(note);
      } catch (error) {
        setFlash(error instanceof Error ? error.message : "Update failed");
      } finally {
        setBusy(false);
        setTimeout(() => setFlash(null), 2600);
      }
    },
    [],
  );

  const decide = useCallback(
    async (status: "approved" | "rejected") => {
      if (!selected) return;
      await patchClip(
        selected.id,
        { reviewStatus: status },
        status === "approved" ? "Approved" : "Rejected",
      );
      step(1);
    },
    [selected, patchClip, step],
  );

  const setSyncPoint = useCallback(async () => {
    if (!asset) return;
    const video = videoRef.current;
    if (!video) return;
    const response = await fetch(`/api/games/${gameId}/anchors`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        mediaAssetId: asset.id,
        videoSeconds: video.currentTime,
        playId: selected?.playId ?? null,
      }),
    });
    setFlash(
      response.ok
        ? "Sync point saved. Re-run matching from the game page to apply it."
        : "Could not save the sync point.",
    );
    setTimeout(() => setFlash(null), 4000);
  }, [asset, gameId, selected?.playId]);

  // Keyboard shortcuts. Ignored while a form field has focus so typing a
  // player's name does not approve a clip.
  useEffect(() => {
    function onKey(event: KeyboardEvent) {
      const target = event.target as HTMLElement;
      if (["INPUT", "SELECT", "TEXTAREA"].includes(target.tagName)) return;
      const video = videoRef.current;
      switch (event.key.toLowerCase()) {
        case " ":
          event.preventDefault();
          if (video) (video.paused ? video.play() : video.pause());
          break;
        case "j": if (video) video.currentTime -= 2; break;
        case "l": if (video) video.currentTime += 2; break;
        case "k": if (video) video.pause(); break;
        case "a": event.preventDefault(); void decide("approved"); break;
        case "x": event.preventDefault(); void decide("rejected"); break;
        case "arrowdown": event.preventDefault(); step(1); break;
        case "arrowup": event.preventDefault(); step(-1); break;
        case "r": if (selected) seek(selected.sourceStart); break;
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [decide, step, seek, selected]);

  if (!asset) {
    return <div className="notice warn">No processed video for this game yet.</div>;
  }

  const pending = clips.filter((c) => c.reviewStatus === "needs_review").length;

  return (
    <>
      {flash && <div className="notice">{flash}</div>}

      <div className="row" style={{ justifyContent: "space-between", marginBottom: 12 }}>
        <div className="row">
          {media.length > 1 && (
            <select
              value={assetId}
              onChange={(e) => setAssetId(e.target.value)}
              style={{ width: "auto" }}
            >
              {media.map((m) => (
                <option key={m.id} value={m.id}>{m.label}</option>
              ))}
            </select>
          )}
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value as typeof filter)}
            style={{ width: "auto" }}
          >
            <option value="needs_review">Needs review ({pending})</option>
            <option value="all">All clips ({clips.length})</option>
            {CATEGORIES.map((c) => (
              <option key={c} value={c}>{CATEGORY_LABEL[c]}</option>
            ))}
          </select>
        </div>
        <button onClick={() => void setSyncPoint()} disabled={busy}>
          Set sync point at playhead
        </button>
      </div>

      <div className="grid" style={{ gridTemplateColumns: "minmax(0, 1.6fr) minmax(320px, 1fr)" }}>
        <div>
          <video
            ref={videoRef}
            src={asset.url}
            controls
            preload="metadata"
            onTimeUpdate={(e) => setPlayhead(e.currentTarget.currentTime)}
          />

          <Timeline
            duration={asset.durationSeconds}
            clips={clips.filter((c) => c.mediaAssetId === asset.id)}
            selectedId={selectedId}
            playhead={playhead}
            onSeek={seek}
            onSelect={selectClip}
          />

          {selected && <ClipInspector clip={selected} roster={roster} busy={busy} onPatch={patchClip} onDecide={decide} onReplay={() => seek(selected.sourceStart)} />}
        </div>

        <div>
          <div className="clip-list">
            {visible.map((clip) => (
              <ClipRow
                key={clip.id}
                clip={clip}
                selected={clip.id === selectedId}
                onSelect={() => selectClip(clip)}
              />
            ))}
            {visible.length === 0 && (
              <p className="muted small">Nothing in this filter. Everything here has been reviewed.</p>
            )}
          </div>
          <p className="muted small" style={{ marginTop: 12 }}>
            Shortcuts: <span className="mono">space</span> play · <span className="mono">J</span>/
            <span className="mono">L</span> nudge 2s · <span className="mono">R</span> replay clip ·{" "}
            <span className="mono">A</span> approve · <span className="mono">X</span> reject ·{" "}
            <span className="mono">↑</span>/<span className="mono">↓</span> move through the list.
          </p>
        </div>
      </div>
    </>
  );
}

function Timeline({
  duration,
  clips,
  selectedId,
  playhead,
  onSeek,
  onSelect,
}: {
  duration: number;
  clips: ReviewClip[];
  selectedId: string | null;
  playhead: number;
  onSeek: (s: number) => void;
  onSelect: (c: ReviewClip) => void;
}) {
  const pct = (seconds: number) => `${Math.min(100, Math.max(0, (seconds / duration) * 100))}%`;
  const ticks = Array.from({ length: 9 }, (_, i) => (duration / 8) * i);

  return (
    <>
      <div
        className="timeline"
        style={{ marginTop: 12 }}
        onClick={(e) => {
          const rect = e.currentTarget.getBoundingClientRect();
          onSeek(((e.clientX - rect.left) / rect.width) * duration);
        }}
      >
        {ticks.map((t, i) => (
          <div key={i} className="tick" style={{ left: pct(t) }} />
        ))}
        {clips.map((c) => (
          <div
            key={c.id}
            title={`${c.title} — ${confidenceLabel(c.matchConfidence).label}`}
            className={[
              "marker",
              c.category,
              c.id === selectedId ? "selected" : "",
              c.reviewStatus === "needs_review" ? "review" : "",
            ].join(" ")}
            style={{
              left: pct(c.sourceStart),
              width: `max(4px, ${((c.sourceEnd - c.sourceStart) / duration) * 100}%)`,
              opacity: c.reviewStatus === "rejected" ? 0.25 : undefined,
            }}
            onClick={(e) => {
              e.stopPropagation();
              onSelect(c);
            }}
          />
        ))}
        <div className="playhead" style={{ left: pct(playhead) }} />
      </div>
      <div className="timeline-axis">
        {ticks.map((t, i) => (
          <span key={i}>{timecode(t)}</span>
        ))}
      </div>
      <div className="legend">
        <span className="offense">Offense</span>
        <span className="defense">Defense</span>
        <span className="pitching">Pitching</span>
        <span className="baserunning">Baserunning</span>
        <span>Dashed outline = awaiting your review</span>
      </div>
    </>
  );
}

function ClipRow({
  clip,
  selected,
  onSelect,
}: {
  clip: ReviewClip;
  selected: boolean;
  onSelect: () => void;
}) {
  const conf = confidenceLabel(clip.matchConfidence);
  return (
    <div className={`clip-row${selected ? " selected" : ""}`} onClick={onSelect}>
      <div
        className="thumb"
        style={clip.thumbnailUrl ? { backgroundImage: `url(${clip.thumbnailUrl})` } : undefined}
      />
      <div>
        <div className="title">{clip.playerName}</div>
        <div className="meta">
          {CATEGORY_LABEL[clip.category]}
          {clip.inning ? ` · ${clip.half === "top" ? "Top" : "Bot"} ${clip.inning}` : ""} ·{" "}
          {timecode(clip.sourceStart)}
        </div>
      </div>
      <span className={`badge ${conf.tone}`}>{Math.round(clip.matchConfidence * 100)}%</span>
    </div>
  );
}

function ClipInspector({
  clip,
  roster,
  busy,
  onPatch,
  onDecide,
  onReplay,
}: {
  clip: ReviewClip;
  roster: RosterOption[];
  busy: boolean;
  onPatch: (id: string, body: Record<string, unknown>, note: string) => Promise<void>;
  onDecide: (status: "approved" | "rejected") => Promise<void>;
  onReplay: () => void;
}) {
  const conf = confidenceLabel(clip.matchConfidence);
  const reasons = explainConfidence(clip.confidenceFactors);

  return (
    <div className="card" style={{ marginTop: 16 }}>
      <div className="row" style={{ justifyContent: "space-between" }}>
        <div>
          <h3 style={{ margin: 0 }}>{clip.title || clip.playerName}</h3>
          <p className="muted small" style={{ margin: "4px 0 0" }}>
            {clip.playDescription ?? "No play text"} · rank {clip.rankScore.toFixed(0)} · matched by{" "}
            {clip.matchMethod.replace("_", " + ")}
          </p>
        </div>
        <span className={`badge ${conf.tone}`}>{conf.label}</span>
      </div>

      {reasons.length > 0 && (
        <div className="notice warn small" style={{ marginTop: 12 }}>
          <strong>Why this needs a look</strong>
          <ul style={{ margin: "6px 0 0", paddingLeft: 18 }}>
            {reasons.map((r) => (
              <li key={r}>{r}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="row" style={{ marginTop: 14 }}>
        <div className="field" style={{ flex: "1 1 200px" }}>
          <label htmlFor="player">Player</label>
          <select
            id="player"
            value={clip.playerId}
            disabled={busy}
            onChange={(e) =>
              void onPatch(clip.id, { playerId: e.target.value }, "Reassigned to another player")
            }
          >
            {roster.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name}{p.jerseyNumber ? ` #${p.jerseyNumber}` : ""}
              </option>
            ))}
          </select>
        </div>

        <div className="field" style={{ flex: "1 1 140px" }}>
          <label htmlFor="category">Category</label>
          <select
            id="category"
            value={clip.category}
            disabled={busy}
            onChange={(e) => void onPatch(clip.id, { category: e.target.value }, "Category changed")}
          >
            {CATEGORIES.map((c) => (
              <option key={c} value={c}>{CATEGORY_LABEL[c]}</option>
            ))}
          </select>
        </div>

        <div className="field" style={{ flex: "0 0 110px" }}>
          <label htmlFor="pre">Before (s)</label>
          <input
            id="pre"
            type="number"
            min={0}
            max={30}
            step={0.5}
            defaultValue={clip.preRoll}
            disabled={busy}
            onBlur={(e) =>
              void onPatch(clip.id, { preRoll: Number(e.target.value) }, "Lead-in updated")
            }
          />
        </div>

        <div className="field" style={{ flex: "0 0 110px" }}>
          <label htmlFor="post">After (s)</label>
          <input
            id="post"
            type="number"
            min={0}
            max={60}
            step={0.5}
            defaultValue={clip.postRoll}
            disabled={busy}
            onBlur={(e) =>
              void onPatch(clip.id, { postRoll: Number(e.target.value) }, "Follow-through updated")
            }
          />
        </div>
      </div>

      <div className="row">
        <button className="primary" disabled={busy} onClick={() => void onDecide("approved")}>
          Approve
        </button>
        <button className="danger" disabled={busy} onClick={() => void onDecide("rejected")}>
          Reject
        </button>
        <button disabled={busy} onClick={onReplay}>Replay</button>
        <span className="muted small">
          Window {timecode(clip.sourceStart)} – {timecode(clip.sourceEnd)} (
          {(clip.sourceEnd - clip.sourceStart).toFixed(1)}s)
        </span>
      </div>
    </div>
  );
}
