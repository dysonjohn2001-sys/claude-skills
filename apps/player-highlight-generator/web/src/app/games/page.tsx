import { requireCoach } from "@/lib/auth";
import { query } from "@/lib/db";

export const dynamic = "force-dynamic";

export default async function GamesPage() {
  await requireCoach();

  const games = await query<{
    id: string;
    played_on: string;
    opponent_name: string;
    home_away: string;
    tournament_name: string | null;
    season_name: string;
    score_us: number | null;
    score_them: number | null;
    media_count: number;
    play_count: number;
    clip_count: number;
  }>(`
    SELECT g.id, g.played_on, g.opponent_name, g.home_away,
           t.name AS tournament_name, s.name AS season_name,
           g.score_us, g.score_them,
           count(DISTINCT m.id) AS media_count,
           count(DISTINCT p.id) AS play_count,
           count(DISTINCT c.id) AS clip_count
      FROM games g
      JOIN seasons s ON s.id = g.season_id
 LEFT JOIN tournaments t  ON t.id = g.tournament_id
 LEFT JOIN media_assets m ON m.game_id = g.id
 LEFT JOIN plays p        ON p.game_id = g.id
 LEFT JOIN clips c        ON c.play_id = p.id
  GROUP BY g.id, t.name, s.name
  ORDER BY g.played_on DESC
  `);

  return (
    <>
      <h2>Games</h2>
      <p className="subtitle">
        Each game holds its own video, play-by-play import and generated clips.
      </p>
      <p>
        <a className="btn primary" href="/games/new">Add a game</a>
      </p>

      <div className="card" style={{ padding: 0 }}>
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Opponent</th>
              <th>Event</th>
              <th>Score</th>
              <th>Video</th>
              <th>Plays</th>
              <th>Clips</th>
            </tr>
          </thead>
          <tbody>
            {games.map((g) => (
              <tr key={g.id}>
                <td>{new Date(g.played_on).toLocaleDateString()}</td>
                <td>
                  <a href={`/games/${g.id}`}>
                    {g.home_away === "away" ? "at " : "vs "}
                    {g.opponent_name}
                  </a>
                </td>
                <td className="muted small">{g.tournament_name ?? g.season_name}</td>
                <td>
                  {g.score_us !== null && g.score_them !== null
                    ? `${g.score_us}-${g.score_them}`
                    : "-"}
                </td>
                <td>{g.media_count || <span className="muted">-</span>}</td>
                <td>{g.play_count || <span className="muted">-</span>}</td>
                <td>{g.clip_count || <span className="muted">-</span>}</td>
              </tr>
            ))}
            {games.length === 0 && (
              <tr>
                <td colSpan={7} className="muted">No games yet.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}
