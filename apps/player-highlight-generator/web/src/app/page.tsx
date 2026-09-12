import { requireCoach } from "@/lib/auth";
import { query, queryOne } from "@/lib/db";
import { gameLabel } from "@/lib/format";

export const dynamic = "force-dynamic";

interface Counts {
  players: number;
  games: number;
  clips: number;
  needs_review: number;
  reels: number;
  unconsented: number;
}

export default async function Dashboard() {
  await requireCoach();

  const counts = await queryOne<Counts>(`
    SELECT
      (SELECT count(*) FROM players WHERE is_active)                               AS players,
      (SELECT count(*) FROM games)                                                 AS games,
      (SELECT count(*) FROM clips)                                                 AS clips,
      (SELECT count(*) FROM clips WHERE review_status = 'needs_review')            AS needs_review,
      (SELECT count(*) FROM reels WHERE output_key IS NOT NULL)                    AS reels,
      (SELECT count(*) FROM players p WHERE p.is_active AND NOT EXISTS (
         SELECT 1 FROM effective_consents ec
          WHERE ec.player_id = p.id AND ec.type = 'highlight_generation' AND ec.is_active
       ))                                                                          AS unconsented
  `);

  const recentGames = await query<{
    id: string;
    played_on: string;
    opponent_name: string;
    clip_count: number;
    review_count: number;
    media_count: number;
    play_count: number;
  }>(`
    SELECT g.id, g.played_on, g.opponent_name,
           count(DISTINCT c.id) FILTER (WHERE c.id IS NOT NULL)                     AS clip_count,
           count(DISTINCT c.id) FILTER (WHERE c.review_status = 'needs_review')     AS review_count,
           count(DISTINCT m.id)                                                     AS media_count,
           count(DISTINCT p.id)                                                     AS play_count
      FROM games g
 LEFT JOIN media_assets m ON m.game_id = g.id
 LEFT JOIN plays p        ON p.game_id = g.id
 LEFT JOIN clips c        ON c.play_id = p.id
  GROUP BY g.id
  ORDER BY g.played_on DESC
     LIMIT 8
  `);

  const runningJobs = await query<{ job_type: string; status: string; n: number }>(`
    SELECT job_type, status, count(*)::int AS n
      FROM jobs
     WHERE status IN ('queued', 'running') OR finished_at > now() - interval '1 hour'
  GROUP BY job_type, status
  ORDER BY job_type
  `);

  return (
    <>
      <h2>Dashboard</h2>
      <p className="subtitle">Everything waiting on you, and what the worker is doing right now.</p>

      <div className="grid cols-3">
        <Stat label="Players" value={counts?.players ?? 0} />
        <Stat label="Games" value={counts?.games ?? 0} />
        <Stat label="Clips matched" value={counts?.clips ?? 0} />
        <Stat label="Awaiting review" value={counts?.needs_review ?? 0} href="/review" />
        <Stat label="Reels rendered" value={counts?.reels ?? 0} />
        <Stat label="Missing consent" value={counts?.unconsented ?? 0} href="/team/consent" />
      </div>

      {(counts?.unconsented ?? 0) > 0 && (
        <div className="notice warn">
          {counts!.unconsented} player{counts!.unconsented === 1 ? "" : "s"} have no active
          highlight-generation consent on file. No clips are produced for them until a guardian
          grants it. <a href="/team/consent">Review consent</a>
        </div>
      )}

      <h3>Recent games</h3>
      <div className="card" style={{ padding: 0 }}>
        <table>
          <thead>
            <tr>
              <th>Game</th>
              <th>Video</th>
              <th>Plays</th>
              <th>Clips</th>
              <th>To review</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {recentGames.map((g) => (
              <tr key={g.id}>
                <td>{gameLabel(g)}</td>
                <td>{g.media_count || <span className="muted">none</span>}</td>
                <td>{g.play_count || <span className="muted">none</span>}</td>
                <td>{g.clip_count}</td>
                <td>
                  {g.review_count > 0 ? (
                    <span className="badge medium">{g.review_count}</span>
                  ) : (
                    <span className="muted">clear</span>
                  )}
                </td>
                <td>
                  <a href={`/games/${g.id}`}>Open</a>
                  {g.clip_count > 0 && <> · <a href={`/games/${g.id}/review`}>Review</a></>}
                </td>
              </tr>
            ))}
            {recentGames.length === 0 && (
              <tr>
                <td colSpan={6} className="muted">
                  No games yet. <a href="/games/new">Add your first game</a>.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <h3>Processing</h3>
      <div className="card">
        {runningJobs.length === 0 ? (
          <p className="muted small" style={{ margin: 0 }}>
            The worker queue is empty.
          </p>
        ) : (
          <ul className="small" style={{ margin: 0, paddingLeft: 18 }}>
            {runningJobs.map((j) => (
              <li key={`${j.job_type}-${j.status}`}>
                {j.n} × <span className="mono">{j.job_type}</span> {j.status}
              </li>
            ))}
          </ul>
        )}
      </div>
    </>
  );
}

function Stat({ label, value, href }: { label: string; value: number; href?: string }) {
  const body = (
    <div className="card" style={{ marginBottom: 0 }}>
      <div className="stat">{value}</div>
      <div className="stat-label">{label}</div>
    </div>
  );
  return href ? <a href={href} style={{ color: "inherit" }}>{body}</a> : body;
}
