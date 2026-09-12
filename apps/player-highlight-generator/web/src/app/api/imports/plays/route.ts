import { NextResponse } from "next/server";

import { requireCoach } from "@/lib/auth";
import { audit, enqueueJob, query, queryOne, transaction } from "@/lib/db";
import { parsePlayByPlayCsv } from "@/lib/csv";

export const runtime = "nodejs";

/**
 * Import a play-by-play CSV the coach exported from their scorekeeping app.
 *
 * Re-importing the same game replaces its plays rather than appending, because
 * a coach re-uploads precisely when the first file was wrong.
 */
export async function POST(request: Request) {
  const user = await requireCoach();
  const form = await request.formData();
  const gameId = String(form.get("gameId") ?? "");
  const weBatIn = String(form.get("weBatIn") ?? "") as "top" | "bottom" | "";
  const file = form.get("file");

  const back = (message: string, ok = false) =>
    NextResponse.redirect(
      new URL(`/games/${gameId}?${ok ? "notice" : "error"}=${encodeURIComponent(message)}`, request.url),
      { status: 303 },
    );

  if (!(file instanceof File)) return back("No file was attached.");

  const game = await queryOne<{ id: string; team_name: string }>(
    `SELECT g.id, t.name AS team_name
       FROM games g JOIN seasons s ON s.id = g.season_id JOIN teams t ON t.id = s.team_id
      WHERE g.id = $1`,
    [gameId],
  );
  if (!game) return back("That game does not exist.");

  const result = parsePlayByPlayCsv(await file.text(), {
    ourTeamName: game.team_name,
    weBatIn: weBatIn || null,
  });

  const batch = await queryOne<{ id: string }>(
    `INSERT INTO import_batches (game_id, kind, filename, source_label, row_count, status,
                                 column_map, error_log, created_by)
     VALUES ($1, 'play_by_play', $2, 'csv_upload', $3, $4, $5, $6, $7) RETURNING id`,
    [
      gameId,
      file.name,
      result.plays.length,
      result.errors.length ? "failed" : "applied",
      JSON.stringify(result.columnMap),
      JSON.stringify([...result.errors, ...result.warnings]),
      user.id,
    ],
  );

  if (result.errors.length) {
    return back(`Import rejected: ${result.errors.map((e) => e.message).join("; ")}`);
  }

  await transaction(async (run) => {
    await run("DELETE FROM plays WHERE game_id = $1", [gameId]);

    for (const p of result.plays) {
      const inserted = await run<{ id: string }>(
        `INSERT INTO plays (
           game_id, import_batch_id, sequence_no, inning, half, occurred_at,
           play_type, result, description, batter_name_raw, pitcher_name_raw,
           is_our_offense, outs_before, balls, strikes, rbi, runs_scored,
           score_us, score_them, leverage_tag, raw_row)
         VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21)
         RETURNING id`,
        [
          gameId, batch!.id, p.sequenceNo, p.inning, p.half, p.occurredAt,
          p.playType, p.result, p.description, p.batter, p.pitcher,
          p.isOurOffense, p.outsBefore, p.balls, p.strikes, p.rbi, p.runsScored,
          p.scoreUs, p.scoreThem, p.leverageTag,
          JSON.stringify({
            batting_order: p.battingOrder,
            runners: p.runners,
            putout_by: p.putoutBy,
            assist_by: p.assistBy,
            error_by: p.errorBy,
            source_row: p.sourceRow,
            inferred_play_type: p.inferredPlayType,
          }),
        ],
      );

      // Raw participant names are stored now; the worker resolves them to
      // player ids during matching, where the roster and lineup are in hand.
      const participants: [string, string | null][] = [
        ["batter", p.isOurOffense ? p.batter : null],
        ["pitcher", p.isOurOffense ? null : p.pitcher],
        ...p.putoutBy.map((n) => ["fielder_putout", n] as [string, string]),
        ...p.assistBy.map((n) => ["fielder_assist", n] as [string, string]),
        ...p.errorBy.map((n) => ["fielder_error", n] as [string, string]),
        ...p.runners.map((n) => ["runner", n] as [string, string]),
      ];
      for (const [role, name] of participants) {
        if (!name) continue;
        await run(
          `INSERT INTO play_participants (play_id, role, raw_name)
           VALUES ($1, $2, $3) ON CONFLICT DO NOTHING`,
          [inserted[0].id, role, name],
        );
      }
    }
  });

  await query("UPDATE import_batches SET applied_count = $2 WHERE id = $1", [
    batch!.id,
    result.plays.length,
  ]);
  await audit(user.id, "plays.imported", "game", gameId, {
    plays: result.plays.length,
    warnings: result.warnings.length,
  });

  // Matching runs automatically once video is ready; queue it so an import
  // after the upload still triggers a pass.
  const ready = await queryOne(
    "SELECT 1 FROM media_assets WHERE game_id = $1 AND status = 'ready' LIMIT 1",
    [gameId],
  );
  if (ready) await enqueueJob("match_plays", "game", gameId);

  const notes = result.warnings.length
    ? ` ${result.warnings.map((w) => w.message).slice(0, 3).join("; ")}`
    : "";
  const sideNote = result.needsSideMapping
    ? " This file had no team column, so the half-inning setting decided which side is ours. Check a few clips."
    : "";
  return back(`Imported ${result.plays.length} plays.${notes}${sideNote}`, true);
}
