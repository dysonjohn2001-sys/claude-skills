import { notFound } from "next/navigation";

import { requireCoach } from "@/lib/auth";
import { query, queryOne } from "@/lib/db";
import { gameLabel } from "@/lib/format";

export const dynamic = "force-dynamic";

/**
 * The batting order is the single most useful cross-check the matcher has: it
 * confirms or contradicts the name the scorebook gave for a given at-bat.
 */
export default async function LineupPage({ params }: { params: Promise<{ gameId: string }> }) {
  await requireCoach();
  const { gameId } = await params;

  const game = await queryOne<{ id: string; played_on: string; opponent_name: string }>(
    "SELECT id, played_on, opponent_name FROM games WHERE id = $1",
    [gameId],
  );
  if (!game) notFound();

  const roster = await query<{
    id: string;
    name: string;
    jersey_number: string | null;
    batting_order: number | null;
    starting_position: string | null;
    entered_inning: number | null;
  }>(
    `SELECT p.id, p.first_name || ' ' || p.last_name AS name, p.jersey_number,
            le.batting_order, le.starting_position, le.entered_inning
       FROM games g
       JOIN seasons s ON s.id = g.season_id
       JOIN players p ON p.team_id = s.team_id AND p.is_active
  LEFT JOIN lineup_entries le ON le.player_id = p.id AND le.game_id = g.id
      WHERE g.id = $1
   ORDER BY le.batting_order NULLS LAST, p.last_name`,
    [gameId],
  );

  const POSITIONS = ["", "P", "C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "DH", "EH"];

  return (
    <>
      <h2>Lineup · {gameLabel(game)}</h2>
      <p className="subtitle">
        Set the batting order and where each player entered. Substitutions matter: a player who came
        in at the fourth inning should not be matched to a play in the second.
      </p>
      <p className="small"><a href={`/games/${gameId}`}>Back to game</a></p>

      <form action="/api/lineup" method="post" className="card">
        <input type="hidden" name="gameId" value={gameId} />
        <table>
          <thead>
            <tr>
              <th>Player</th>
              <th style={{ width: 110 }}>Batting slot</th>
              <th style={{ width: 130 }}>Position</th>
              <th style={{ width: 130 }}>Entered inning</th>
            </tr>
          </thead>
          <tbody>
            {roster.map((p) => (
              <tr key={p.id}>
                <td>
                  {p.name} {p.jersey_number && <span className="muted mono">#{p.jersey_number}</span>}
                </td>
                <td>
                  <input type="number" min={1} max={20} name={`order_${p.id}`}
                         defaultValue={p.batting_order ?? ""} />
                </td>
                <td>
                  <select name={`pos_${p.id}`} defaultValue={p.starting_position ?? ""}>
                    {POSITIONS.map((pos) => (
                      <option key={pos} value={pos}>{pos || "-"}</option>
                    ))}
                  </select>
                </td>
                <td>
                  <input type="number" min={1} max={20} name={`entered_${p.id}`}
                         defaultValue={p.entered_inning ?? 1} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <p style={{ marginTop: 16 }}>
          <button type="submit" className="primary">Save lineup</button>
        </p>
      </form>
    </>
  );
}
