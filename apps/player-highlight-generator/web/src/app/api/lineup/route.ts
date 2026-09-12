import { NextResponse } from "next/server";

import { requireCoach } from "@/lib/auth";
import { audit, transaction } from "@/lib/db";

export async function POST(request: Request) {
  const user = await requireCoach();
  const form = await request.formData();
  const gameId = String(form.get("gameId") ?? "");

  let saved = 0;
  await transaction(async (run) => {
    await run("DELETE FROM lineup_entries WHERE game_id = $1", [gameId]);

    for (const [key, value] of form.entries()) {
      if (!key.startsWith("order_")) continue;
      const playerId = key.slice("order_".length);
      const order = Number(value);
      if (!Number.isFinite(order) || order < 1) continue;

      const position = String(form.get(`pos_${playerId}`) ?? "") || null;
      const entered = Number(form.get(`entered_${playerId}`) ?? 1) || 1;

      await run(
        `INSERT INTO lineup_entries (game_id, player_id, batting_order, starting_position, entered_inning)
         VALUES ($1, $2, $3, $4, $5)
         ON CONFLICT (game_id, player_id, entered_inning) DO UPDATE
           SET batting_order = EXCLUDED.batting_order,
               starting_position = EXCLUDED.starting_position`,
        [gameId, playerId, order, position, entered],
      );
      saved += 1;
    }
  });

  await audit(user.id, "lineup.saved", "game", gameId, { entries: saved });
  return NextResponse.redirect(new URL(`/games/${gameId}`, request.url), { status: 303 });
}
