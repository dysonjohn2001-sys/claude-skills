import { NextResponse } from "next/server";

import { requireCoach } from "@/lib/auth";
import { audit, enqueueJob, queryOne } from "@/lib/db";
import { canGenerateHighlights } from "@/lib/permissions";

/**
 * Queue a reel render.
 *
 * The consent gate is enforced here as well as in the worker. A check in the
 * UI alone is a suggestion; a check at both ends is a rule.
 */
export async function POST(request: Request) {
  const user = await requireCoach();
  const form = await request.formData();

  const playerId = String(form.get("playerId") ?? "");
  const rawTarget = String(form.get("targetId") ?? "");
  const aspectChoice = String(form.get("aspect") ?? "16:9");

  const back = (message: string, ok = false) =>
    NextResponse.redirect(
      new URL(`/players/${playerId}?${ok ? "notice" : "error"}=${encodeURIComponent(message)}`, request.url),
      { status: 303 },
    );

  const [scope, targetId] = rawTarget.split(":");
  if (!["game", "tournament", "season"].includes(scope) || !targetId) {
    return back("Pick which game, tournament or season the reel covers.");
  }

  const gate = await canGenerateHighlights(playerId);
  if (!gate.allowed) return back(gate.message);

  const player = await queryOne<{ name: string; team_id: string }>(
    `SELECT first_name || ' ' || last_name AS name, team_id FROM players WHERE id = $1`,
    [playerId],
  );
  if (!player) return back("That player does not exist.");

  const label = await scopeLabel(scope, targetId);
  const aspects = aspectChoice === "both" ? ["16:9", "9:16"] : [aspectChoice];

  for (const aspect of aspects) {
    const reel = await queryOne<{ id: string }>(
      `INSERT INTO reels (player_id, scope, game_id, tournament_id, season_id, title, aspect, created_by)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING id`,
      [
        playerId,
        scope,
        scope === "game" ? targetId : null,
        scope === "tournament" ? targetId : null,
        scope === "season" ? targetId : null,
        `${player.name} — ${label}`,
        aspect,
        user.id,
      ],
    );
    await enqueueJob("render_reel", "reel", reel!.id, { aspect });
    await audit(user.id, "reel.queued", "reel", reel!.id, { scope, targetId, aspect });
  }

  return back(
    `Queued ${aspects.length} reel${aspects.length === 1 ? "" : "s"}. Rendering usually takes a few minutes.`,
    true,
  );
}

async function scopeLabel(scope: string, targetId: string): Promise<string> {
  if (scope === "game") {
    const row = await queryOne<{ played_on: string; opponent_name: string }>(
      "SELECT played_on, opponent_name FROM games WHERE id = $1",
      [targetId],
    );
    return row
      ? `${new Date(row.played_on).toLocaleDateString()} vs ${row.opponent_name}`
      : "Game highlights";
  }
  const table = scope === "tournament" ? "tournaments" : "seasons";
  const row = await queryOne<{ name: string }>(`SELECT name FROM ${table} WHERE id = $1`, [targetId]);
  return row?.name ?? "Highlights";
}
