import { notFound } from "next/navigation";

import { requireCoach } from "@/lib/auth";
import { query, queryOne } from "@/lib/db";
import { CATEGORY_LABEL, duration, gameLabel } from "@/lib/format";
import { canGenerateHighlights, consentFor } from "@/lib/permissions";

export const dynamic = "force-dynamic";

export default async function PlayerPage({ params }: { params: Promise<{ playerId: string }> }) {
  await requireCoach();
  const { playerId } = await params;

  const player = await queryOne<{
    id: string;
    first_name: string;
    last_name: string;
    preferred_name: string | null;
    jersey_number: string | null;
    bats: string | null;
    throws: string | null;
    team_id: string;
    team_name: string;
  }>(
    `SELECT p.*, t.name AS team_name
       FROM players p JOIN teams t ON t.id = p.team_id
      WHERE p.id = $1`,
    [playerId],
  );
  if (!player) notFound();

  const gate = await canGenerateHighlights(playerId);
  const consent = await consentFor(playerId);

  const byCategory = await query<{ category: string; n: number; approved: number }>(
    `SELECT category, count(*)::int AS n,
            count(*) FILTER (WHERE review_status IN ('auto_approved','approved'))::int AS approved
       FROM clips WHERE player_id = $1 GROUP BY category`,
    [playerId],
  );

  const reels = await query<{
    id: string;
    title: string;
    scope: string;
    aspect: string;
    duration_seconds: string | null;
    output_key: string | null;
    rendered_at: string | null;
    share_count: number;
  }>(
    `SELECT r.*, count(sl.id)::int AS share_count
       FROM reels r LEFT JOIN share_links sl ON sl.reel_id = r.id AND sl.revoked_at IS NULL
      WHERE r.player_id = $1
   GROUP BY r.id
   ORDER BY r.created_at DESC`,
    [playerId],
  );

  const games = await query<{ id: string; played_on: string; opponent_name: string; n: number }>(
    `SELECT g.id, g.played_on, g.opponent_name, count(c.id)::int AS n
       FROM clips c JOIN plays p ON p.id = c.play_id JOIN games g ON g.id = p.game_id
      WHERE c.player_id = $1 AND c.review_status IN ('auto_approved','approved')
   GROUP BY g.id ORDER BY g.played_on DESC`,
    [playerId],
  );

  const seasons = await query<{ id: string; name: string }>(
    `SELECT s.id, s.name FROM seasons s WHERE s.team_id = $1 ORDER BY s.starts_on DESC`,
    [player.team_id],
  );

  const tournaments = await query<{ id: string; name: string }>(
    `SELECT tr.id, tr.name FROM tournaments tr
       JOIN seasons s ON s.id = tr.season_id WHERE s.team_id = $1 ORDER BY tr.starts_on DESC`,
    [player.team_id],
  );

  const displayName = `${player.preferred_name ?? player.first_name} ${player.last_name}`;

  return (
    <>
      <h2>
        {displayName} {player.jersey_number && <span className="muted">#{player.jersey_number}</span>}
      </h2>
      <p className="subtitle">
        {player.team_name}
        {player.bats && ` · bats ${player.bats}`}
        {player.throws && ` · throws ${player.throws}`}
      </p>

      {!gate.allowed && (
        <div className="notice error">
          <strong>Highlights are blocked for this player.</strong> {gate.message} Missing:{" "}
          {gate.missing.join(", ").replace(/_/g, " ")}. <a href="/team/consent">Record consent</a>
        </div>
      )}

      <div className="grid cols-3">
        {(["offense", "defense", "pitching", "baserunning"] as const).map((category) => {
          const row = byCategory.find((c) => c.category === category);
          return (
            <div key={category} className="card" style={{ marginBottom: 0 }}>
              <div className="stat">{row?.approved ?? 0}</div>
              <div className="stat-label">{CATEGORY_LABEL[category]} clips</div>
              {row && row.n > row.approved && (
                <div className="small muted" style={{ marginTop: 4 }}>
                  {row.n - row.approved} awaiting review
                </div>
              )}
            </div>
          );
        })}
      </div>

      <h3>Build a reel</h3>
      <form action="/api/reels" method="post" className="card">
        <input type="hidden" name="playerId" value={playerId} />
        <div className="row">
          <div className="field" style={{ flex: "1 1 200px" }}>
            <label htmlFor="scope">Scope</label>
            <select id="scope" name="scope" defaultValue="game">
              <option value="game">Single game</option>
              <option value="tournament">Tournament</option>
              <option value="season">Full season</option>
            </select>
          </div>
          <div className="field" style={{ flex: "1 1 240px" }}>
            <label htmlFor="targetId">Which one</label>
            <select id="targetId" name="targetId">
              <optgroup label="Games">
                {games.map((g) => (
                  <option key={g.id} value={`game:${g.id}`}>
                    {gameLabel(g)} ({g.n} clips)
                  </option>
                ))}
              </optgroup>
              <optgroup label="Tournaments">
                {tournaments.map((t) => (
                  <option key={t.id} value={`tournament:${t.id}`}>{t.name}</option>
                ))}
              </optgroup>
              <optgroup label="Seasons">
                {seasons.map((s) => (
                  <option key={s.id} value={`season:${s.id}`}>{s.name}</option>
                ))}
              </optgroup>
            </select>
          </div>
          <div className="field" style={{ flex: "0 0 160px" }}>
            <label htmlFor="aspect">Format</label>
            <select id="aspect" name="aspect" defaultValue="16:9">
              <option value="16:9">16:9 horizontal</option>
              <option value="9:16">9:16 vertical</option>
              <option value="both">Both</option>
            </select>
          </div>
          <div className="field">
            <button type="submit" className="primary" disabled={!gate.allowed}>
              Render reel
            </button>
          </div>
        </div>
        <p className="muted small" style={{ margin: 0 }}>
          Only approved clips are used. Anything still in the review queue is left out.
        </p>
      </form>

      <h3>Reels</h3>
      <div className="card" style={{ padding: 0 }}>
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Scope</th>
              <th>Format</th>
              <th>Length</th>
              <th>Status</th>
              <th>Shared with</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {reels.map((r) => (
              <tr key={r.id}>
                <td>{r.title}</td>
                <td className="small muted">{r.scope}</td>
                <td className="mono small">{r.aspect}</td>
                <td>{r.duration_seconds ? duration(Number(r.duration_seconds)) : "-"}</td>
                <td>
                  {r.output_key ? (
                    <span className="badge high">ready</span>
                  ) : (
                    <span className="badge neutral">rendering</span>
                  )}
                </td>
                <td>{r.share_count || <span className="muted">nobody</span>}</td>
                <td className="small">
                  {r.output_key && (
                    <>
                      <a href={`/api/media/${encodeURI(r.output_key)}`}>Watch</a> ·{" "}
                    </>
                  )}
                  <a href={`/reels/${r.id}/share`}>Share</a>
                </td>
              </tr>
            ))}
            {reels.length === 0 && (
              <tr><td colSpan={7} className="muted">No reels built yet.</td></tr>
            )}
          </tbody>
        </table>
      </div>

      <h3>Consent on file</h3>
      <div className="card">
        <ul className="small" style={{ margin: 0, paddingLeft: 18 }}>
          <ConsentLine label="Appears in team video" held={consent.mediaCapture} />
          <ConsentLine label="Personal highlight reels may be generated" held={consent.highlightGeneration} />
          <ConsentLine label="Reels may be shared with this player's own family" held={consent.familySharing} />
          <ConsentLine label="Reels may be visible to other families on the team" held={consent.teamSharing} />
          <ConsentLine label="Reels may be downloaded and posted elsewhere" held={consent.externalSharing} />
        </ul>
      </div>
    </>
  );
}

function ConsentLine({ label, held }: { label: string; held: boolean }) {
  return (
    <li>
      {label}:{" "}
      <span className={`badge ${held ? "high" : "low"}`}>{held ? "granted" : "not granted"}</span>
    </li>
  );
}
