import { requireCoach } from "@/lib/auth";
import { query } from "@/lib/db";
import { CATEGORY_LABEL, confidenceLabel } from "@/lib/format";

export const dynamic = "force-dynamic";

/**
 * The cross-game queue. The order is deliberate: highest-ranked clip with the
 * lowest confidence first, because that is the clip most likely to end up in a
 * reel while being wrong.
 */
export default async function ReviewQueuePage() {
  await requireCoach();

  const rows = await query<{
    clip_id: string;
    player_name: string;
    match_confidence: string;
    rank_score: string;
    category: string;
    game_id: string;
    played_on: string;
    opponent_name: string;
    play_description: string | null;
    inning: number | null;
    half: string | null;
  }>("SELECT * FROM review_queue LIMIT 200");

  const byGame = new Map<string, typeof rows>();
  for (const row of rows) {
    const bucket = byGame.get(row.game_id) ?? [];
    bucket.push(row);
    byGame.set(row.game_id, bucket);
  }

  return (
    <>
      <h2>Review queue</h2>
      <p className="subtitle">
        {rows.length} uncertain assignment{rows.length === 1 ? "" : "s"} across all games, most
        consequential first.
      </p>

      {rows.length === 0 && (
        <div className="notice">
          Nothing to review. Every matched clip cleared the confidence threshold.
        </div>
      )}

      {[...byGame.entries()].map(([gameId, clips]) => (
        <section key={gameId}>
          <h3>
            {new Date(clips[0].played_on).toLocaleDateString()} vs {clips[0].opponent_name}{" "}
            <a className="small" href={`/games/${gameId}/review`}>open review screen</a>
          </h3>
          <div className="card" style={{ padding: 0 }}>
            <table>
              <thead>
                <tr>
                  <th>Player</th>
                  <th>Category</th>
                  <th>Play</th>
                  <th>Confidence</th>
                  <th>Rank</th>
                </tr>
              </thead>
              <tbody>
                {clips.map((c) => {
                  const conf = confidenceLabel(Number(c.match_confidence));
                  return (
                    <tr key={c.clip_id}>
                      <td>{c.player_name}</td>
                      <td className="small muted">{CATEGORY_LABEL[c.category]}</td>
                      <td className="small">
                        {c.inning ? `${c.half === "top" ? "Top" : "Bot"} ${c.inning} · ` : ""}
                        {c.play_description ?? "-"}
                      </td>
                      <td><span className={`badge ${conf.tone}`}>{conf.label}</span></td>
                      <td className="small muted">{Number(c.rank_score).toFixed(0)}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </section>
      ))}
    </>
  );
}
