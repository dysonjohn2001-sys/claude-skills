import { notFound } from "next/navigation";

import { requireCoach } from "@/lib/auth";
import { query, queryOne } from "@/lib/db";
import { duration, gameLabel } from "@/lib/format";

export const dynamic = "force-dynamic";

interface GameRow {
  id: string;
  played_on: string;
  first_pitch_at: string | null;
  opponent_name: string;
  home_away: string;
  location: string | null;
  score_us: number | null;
  score_them: number | null;
  season_name: string;
  team_name: string;
  tournament_name: string | null;
}

export default async function GamePage({
  params,
  searchParams,
}: {
  params: Promise<{ gameId: string }>;
  searchParams: Promise<{ notice?: string; error?: string }>;
}) {
  await requireCoach();
  const { gameId } = await params;
  const flash = await searchParams;

  const game = await queryOne<GameRow>(
    `SELECT g.*, s.name AS season_name, t.name AS team_name, tr.name AS tournament_name
       FROM games g
       JOIN seasons s ON s.id = g.season_id
       JOIN teams t   ON t.id = s.team_id
  LEFT JOIN tournaments tr ON tr.id = g.tournament_id
      WHERE g.id = $1`,
    [gameId],
  );
  if (!game) notFound();

  const media = await query<{
    id: string;
    kind: string;
    original_filename: string;
    duration_seconds: number | null;
    width: number | null;
    height: number | null;
    status: string;
    error_message: string | null;
    recording_started_at: string | null;
    anchor_count: number;
  }>(
    `SELECT m.*, count(a.id)::int AS anchor_count
       FROM media_assets m
  LEFT JOIN media_sync_anchors a ON a.media_asset_id = m.id
      WHERE m.game_id = $1
   GROUP BY m.id
   ORDER BY m.created_at`,
    [gameId],
  );

  const playStats = await queryOne<{ total: number; timed: number; ours: number }>(
    `SELECT count(*)::int AS total,
            count(occurred_at)::int AS timed,
            count(*) FILTER (WHERE is_our_offense)::int AS ours
       FROM plays WHERE game_id = $1`,
    [gameId],
  );

  const clipStats = await queryOne<{ total: number; review: number; approved: number }>(
    `SELECT count(*)::int AS total,
            count(*) FILTER (WHERE c.review_status = 'needs_review')::int AS review,
            count(*) FILTER (WHERE c.review_status IN ('auto_approved','approved'))::int AS approved
       FROM clips c JOIN plays p ON p.id = c.play_id
      WHERE p.game_id = $1`,
    [gameId],
  );

  const lineup = await query<{ batting_order: number; name: string; jersey_number: string | null }>(
    `SELECT le.batting_order, p.first_name || ' ' || p.last_name AS name, p.jersey_number
       FROM lineup_entries le JOIN players p ON p.id = le.player_id
      WHERE le.game_id = $1 AND le.batting_order IS NOT NULL
   ORDER BY le.batting_order`,
    [gameId],
  );

  const readyMedia = media.filter((m) => m.status === "ready");
  const noAnchors = readyMedia.length > 0 && readyMedia.every((m) => m.anchor_count === 0);
  const canMatch = readyMedia.length > 0 && (playStats?.total ?? 0) > 0;

  return (
    <>
      <h2>{gameLabel(game)}</h2>
      <p className="subtitle">
        {game.team_name} · {game.tournament_name ?? game.season_name}
        {game.location ? ` · ${game.location}` : ""}
        {game.score_us !== null ? ` · final ${game.score_us}-${game.score_them}` : ""}
      </p>

      {flash.notice && <div className="notice">{flash.notice}</div>}
      {flash.error && <div className="notice error">{flash.error}</div>}

      {noAnchors && (
        <div className="notice warn">
          None of this game&apos;s videos has a sync point yet. Matching will fall back to the file&apos;s
          recording timestamp, which on phone footage is often a minute out. Open the review screen,
          scrub to any play you recognise and press <strong>Set sync point</strong> — one is enough,
          two is better.
        </div>
      )}

      <div className="grid cols-2">
        <section className="card">
          <h3 style={{ marginTop: 0 }}>Video</h3>
          {media.length === 0 && <p className="muted small">Nothing uploaded yet.</p>}
          {media.map((m) => (
            <div key={m.id} style={{ paddingBottom: 10, marginBottom: 10, borderBottom: "1px solid var(--border)" }}>
              <div style={{ fontWeight: 560 }}>{m.original_filename}</div>
              <div className="muted small">
                {m.kind === "full_game" ? "Full game" : "Single clip"}
                {m.duration_seconds ? ` · ${duration(Number(m.duration_seconds))}` : ""}
                {m.width ? ` · ${m.width}×${m.height}` : ""}
                {" · "}
                <StatusBadge status={m.status} />
                {m.anchor_count > 0 && ` · ${m.anchor_count} sync point${m.anchor_count === 1 ? "" : "s"}`}
              </div>
              {m.error_message && <div className="notice error small">{m.error_message}</div>}
            </div>
          ))}

          <form action="/api/uploads" method="post" encType="multipart/form-data">
            <input type="hidden" name="gameId" value={gameId} />
            <div className="field">
              <label htmlFor="file">Add a recording or clip</label>
              <input id="file" name="file" type="file" accept="video/*" required />
            </div>
            <div className="row">
              <div className="field" style={{ flex: 1 }}>
                <label htmlFor="kind">Type</label>
                <select id="kind" name="kind" defaultValue="full_game">
                  <option value="full_game">Full game recording</option>
                  <option value="clip">Individual clip</option>
                </select>
              </div>
              <div className="field" style={{ flex: 1 }}>
                <label htmlFor="recordingStartedAt">Recording started (optional)</label>
                <input id="recordingStartedAt" name="recordingStartedAt" type="datetime-local" />
              </div>
            </div>
            <button type="submit" className="primary">Upload</button>
          </form>
        </section>

        <section className="card">
          <h3 style={{ marginTop: 0 }}>Play-by-play</h3>
          <p className="small muted">
            Export the scorebook from your scorekeeping app as CSV and upload it here. The importer
            matches the column names itself and shows you what it found before anything is saved.
          </p>
          <p>
            <strong>{playStats?.total ?? 0}</strong> plays imported
            {(playStats?.total ?? 0) > 0 && (
              <span className="muted small">
                {" "}· {playStats!.timed} with timestamps · {playStats!.ours} on offense
              </span>
            )}
          </p>
          {(playStats?.total ?? 0) > 0 && playStats!.timed === 0 && (
            <div className="notice warn small">
              No timestamps in this import. Plays will be paced from first pitch, which is far less
              precise. Set a first-pitch time on the game, or add two sync points in the review screen.
            </div>
          )}

          <form action="/api/imports/plays" method="post" encType="multipart/form-data">
            <input type="hidden" name="gameId" value={gameId} />
            <div className="field">
              <label htmlFor="playsFile">Play-by-play CSV</label>
              <input id="playsFile" name="file" type="file" accept=".csv,text/csv" required />
            </div>
            <div className="field">
              <label htmlFor="weBatIn">If the file has no team column, we bat in</label>
              <select id="weBatIn" name="weBatIn" defaultValue={game.home_away === "home" ? "bottom" : "top"}>
                <option value="top">the top of the inning (away)</option>
                <option value="bottom">the bottom of the inning (home)</option>
              </select>
            </div>
            <button type="submit" className="primary">Import plays</button>
          </form>

          <h3>Lineup</h3>
          {lineup.length === 0 ? (
            <p className="muted small">
              No batting order recorded. Matching still works, but the batting slot is one of the
              strongest checks available, so accuracy drops without it.{" "}
              <a href={`/games/${gameId}/lineup`}>Set the lineup</a>
            </p>
          ) : (
            <ol className="small" style={{ margin: 0, paddingLeft: 20 }}>
              {lineup.map((l) => (
                <li key={l.batting_order}>
                  {l.name} {l.jersey_number && <span className="muted">#{l.jersey_number}</span>}
                </li>
              ))}
            </ol>
          )}
        </section>
      </div>

      <section className="card">
        <h3 style={{ marginTop: 0 }}>Matching</h3>
        <div className="row" style={{ alignItems: "center", justifyContent: "space-between" }}>
          <div>
            <p style={{ margin: 0 }}>
              <strong>{clipStats?.total ?? 0}</strong> clips matched ·{" "}
              <strong>{clipStats?.review ?? 0}</strong> awaiting review ·{" "}
              <strong>{clipStats?.approved ?? 0}</strong> ready for reels
            </p>
            <p className="muted small" style={{ margin: "4px 0 0" }}>
              Re-running matching keeps every clip you have already approved or rejected.
            </p>
          </div>
          <div className="row">
            <form action={`/api/games/${gameId}/match`} method="post">
              <button type="submit" className="primary" disabled={!canMatch}>
                {clipStats?.total ? "Re-run matching" : "Match plays to video"}
              </button>
            </form>
            {(clipStats?.total ?? 0) > 0 && (
              <a className="btn" href={`/games/${gameId}/review`}>Open review screen</a>
            )}
          </div>
        </div>
        {!canMatch && (
          <p className="notice small" style={{ marginTop: 12 }}>
            Matching needs at least one processed video and an imported play-by-play file.
          </p>
        )}
      </section>
    </>
  );
}

function StatusBadge({ status }: { status: string }) {
  const tone =
    status === "ready" ? "high" : status === "failed" ? "low" : "neutral";
  return <span className={`badge ${tone}`}>{status}</span>;
}
