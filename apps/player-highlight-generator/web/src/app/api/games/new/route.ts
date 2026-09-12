import { NextResponse } from "next/server";

import { requireCoach } from "@/lib/auth";
import { audit, queryOne } from "@/lib/db";

export async function POST(request: Request) {
  const user = await requireCoach();
  const form = await request.formData();

  const text = (key: string) => String(form.get(key) ?? "").trim();
  const seasonId = text("seasonId");
  const opponent = text("opponentName");
  const playedOn = text("playedOn");

  if (!seasonId || !opponent || !playedOn) {
    return NextResponse.redirect(
      new URL(
        `/games/new?error=${encodeURIComponent("Season, date and opponent are all required.")}`,
        request.url,
      ),
      { status: 303 },
    );
  }

  const firstPitch = text("firstPitchAt");
  const game = await queryOne<{ id: string }>(
    `INSERT INTO games (season_id, tournament_id, played_on, first_pitch_at,
                        opponent_name, home_away, location)
     VALUES ($1, NULLIF($2,'')::uuid, $3, $4, $5, $6::home_away, NULLIF($7,''))
     RETURNING id`,
    [
      seasonId,
      text("tournamentId"),
      playedOn,
      firstPitch ? new Date(firstPitch) : null,
      opponent,
      text("homeAway") || "home",
      text("location"),
    ],
  );

  await audit(user.id, "game.created", "game", game!.id, { opponent, playedOn });
  return NextResponse.redirect(new URL(`/games/${game!.id}`, request.url), { status: 303 });
}
