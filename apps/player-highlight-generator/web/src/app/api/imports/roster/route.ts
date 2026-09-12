import { NextResponse } from "next/server";

import { requireCoach } from "@/lib/auth";
import { audit, query, queryOne, transaction } from "@/lib/db";
import { parseRosterCsv } from "@/lib/csv";

export const runtime = "nodejs";

export async function POST(request: Request) {
  const user = await requireCoach();
  const form = await request.formData();
  const teamId = String(form.get("teamId") ?? "");
  const dryRun = form.get("dryRun") !== null;
  const file = form.get("file");

  const back = (key: "imported" | "error", message: string) =>
    NextResponse.redirect(
      new URL(`/team/roster?${key}=${encodeURIComponent(message)}`, request.url),
      { status: 303 },
    );

  if (!(file instanceof File)) return back("error", "No file was attached.");
  if (!teamId) return back("error", "No team selected.");

  const result = parseRosterCsv(await file.text());

  const batch = await queryOne<{ id: string }>(
    `INSERT INTO import_batches (team_id, kind, filename, source_label, row_count, status,
                                 column_map, error_log, created_by)
     VALUES ($1, 'roster', $2, 'csv_upload', $3, $4, $5, $6, $7) RETURNING id`,
    [
      teamId,
      file.name,
      result.players.length,
      result.errors.length ? "failed" : dryRun ? "needs_mapping" : "applied",
      JSON.stringify(result.columnMap),
      JSON.stringify([...result.errors, ...result.warnings]),
      user.id,
    ],
  );

  if (result.errors.length) {
    return back("error", `Import rejected: ${result.errors.map((e) => e.message).join("; ")}`);
  }

  if (dryRun) {
    const preview = result.players
      .slice(0, 6)
      .map((p) => `${p.firstName} ${p.lastName}${p.jerseyNumber ? ` #${p.jerseyNumber}` : ""}`)
      .join(", ");
    return back(
      "imported",
      `Preview only: ${result.players.length} players would be imported (${preview}${
        result.players.length > 6 ? ", ..." : ""
      }). Untick "Preview only" to apply.`,
    );
  }

  let applied = 0;
  await transaction(async (run) => {
    for (const p of result.players) {
      // Match on jersey number first, then on name: a coach re-uploading a
      // corrected roster must update players rather than duplicate them.
      const existing = await run<{ id: string }>(
        `SELECT id FROM players
          WHERE team_id = $1 AND is_active
            AND (($2::text IS NOT NULL AND jersey_number = $2)
                 OR (lower(first_name) = lower($3) AND lower(last_name) = lower($4)))
          LIMIT 1`,
        [teamId, p.jerseyNumber, p.firstName, p.lastName],
      );

      const playerId = existing[0]?.id
        ? (
            await run<{ id: string }>(
              `UPDATE players
                  SET first_name = $2, last_name = $3, jersey_number = $4,
                      bats = COALESCE($5, bats), throws = COALESCE($6, throws),
                      birth_year = COALESCE($7, birth_year), updated_at = now()
                WHERE id = $1 RETURNING id`,
              [existing[0].id, p.firstName, p.lastName, p.jerseyNumber, p.bats, p.throws, p.birthYear],
            )
          )[0].id
        : (
            await run<{ id: string }>(
              `INSERT INTO players (team_id, first_name, last_name, jersey_number, bats, throws, birth_year)
               VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING id`,
              [teamId, p.firstName, p.lastName, p.jerseyNumber, p.bats, p.throws, p.birthYear],
            )
          )[0].id;

      await run("DELETE FROM player_positions WHERE player_id = $1", [playerId]);
      for (const [index, position] of p.positions.entries()) {
        await run(
          `INSERT INTO player_positions (player_id, position, is_primary)
           VALUES ($1, $2, $3) ON CONFLICT DO NOTHING`,
          [playerId, position, index === 0],
        );
      }

      // Guardians are staged only. No invitation is sent and no consent is
      // implied by appearing in a spreadsheet.
      for (const g of p.guardians) {
        const guardian = await run<{ id: string }>(
          `INSERT INTO guardians (full_name, email, phone) VALUES ($1, $2, $3) RETURNING id`,
          [g.fullName, g.email, g.phone],
        );
        await run(
          `INSERT INTO player_guardians (player_id, guardian_id, is_primary_contact)
           VALUES ($1, $2, TRUE) ON CONFLICT DO NOTHING`,
          [playerId, guardian[0].id],
        );
      }

      applied += 1;
    }
  });

  await query("UPDATE import_batches SET applied_count = $2 WHERE id = $1", [batch!.id, applied]);
  await audit(user.id, "roster.imported", "team", teamId, {
    players: applied,
    warnings: result.warnings.length,
  });

  const warningNote = result.warnings.length
    ? ` ${result.warnings.length} warning${result.warnings.length === 1 ? "" : "s"}: ${result.warnings
        .slice(0, 3)
        .map((w) => w.message)
        .join("; ")}`
    : "";
  return back("imported", `Imported ${applied} players.${warningNote}`);
}
