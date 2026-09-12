import { requireCoach } from "@/lib/auth";
import { query } from "@/lib/db";

export const dynamic = "force-dynamic";

export default async function PlayersPage() {
  await requireCoach();

  const players = await query<{
    id: string;
    name: string;
    jersey_number: string | null;
    positions: string[];
    clip_count: number;
    approved_count: number;
    reel_count: number;
    consented: boolean;
  }>(`
    SELECT p.id,
           p.first_name || ' ' || p.last_name AS name,
           p.jersey_number,
           COALESCE(array_agg(DISTINCT pp.position) FILTER (WHERE pp.position IS NOT NULL), '{}') AS positions,
           count(DISTINCT c.id)::int AS clip_count,
           count(DISTINCT c.id) FILTER (WHERE c.review_status IN ('auto_approved','approved'))::int AS approved_count,
           count(DISTINCT r.id)::int AS reel_count,
           EXISTS (SELECT 1 FROM effective_consents ec
                    WHERE ec.player_id = p.id AND ec.type = 'highlight_generation' AND ec.is_active) AS consented
      FROM players p
 LEFT JOIN player_positions pp ON pp.player_id = p.id
 LEFT JOIN clips c ON c.player_id = p.id
 LEFT JOIN reels r ON r.player_id = p.id AND r.output_key IS NOT NULL
     WHERE p.is_active
  GROUP BY p.id
  ORDER BY p.last_name, p.first_name
  `);

  return (
    <>
      <h2>Players</h2>
      <p className="subtitle">Every player&apos;s clip inventory and rendered reels.</p>

      <div className="card" style={{ padding: 0 }}>
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Player</th>
              <th>Positions</th>
              <th>Clips</th>
              <th>Approved</th>
              <th>Reels</th>
              <th>Consent</th>
            </tr>
          </thead>
          <tbody>
            {players.map((p) => (
              <tr key={p.id}>
                <td className="mono">{p.jersey_number ?? "-"}</td>
                <td><a href={`/players/${p.id}`}>{p.name}</a></td>
                <td className="small muted">{p.positions.join(", ") || "-"}</td>
                <td>{p.clip_count}</td>
                <td>{p.approved_count}</td>
                <td>{p.reel_count}</td>
                <td>
                  {p.consented ? (
                    <span className="badge high">on file</span>
                  ) : (
                    <span className="badge low">missing</span>
                  )}
                </td>
              </tr>
            ))}
            {players.length === 0 && (
              <tr>
                <td colSpan={7} className="muted">
                  No players yet. <a href="/team/roster">Import a roster</a>.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}
