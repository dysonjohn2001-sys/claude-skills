import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

import { NextResponse } from "next/server";

import { requireCoach } from "@/lib/auth";
import { audit, query } from "@/lib/db";

const MEDIA_ROOT = process.env.PHG_MEDIA_ROOT ?? "/var/lib/phg/media";
const HEX = /^#[0-9a-fA-F]{6}$/;

export const runtime = "nodejs";

export async function POST(request: Request) {
  const user = await requireCoach();
  const form = await request.formData();
  const teamId = String(form.get("teamId") ?? "");

  const text = (key: string) => String(form.get(key) ?? "").trim();
  const num = (key: string, fallback: number) => {
    const value = Number(form.get(key));
    return Number.isFinite(value) ? value : fallback;
  };
  const flag = (key: string) => form.get(key) !== null;

  const primary = HEX.test(text("primaryColor")) ? text("primaryColor") : "#0F2B5B";
  const secondary = HEX.test(text("secondaryColor")) ? text("secondaryColor") : "#C8102E";

  let logoKey: string | null = null;
  const logo = form.get("logo");
  if (logo instanceof File && logo.size > 0) {
    const extension = path.extname(logo.name).toLowerCase() || ".png";
    logoKey = `teams/${teamId}/logo${extension}`;
    const destination = path.join(MEDIA_ROOT, logoKey);
    await mkdir(path.dirname(destination), { recursive: true });
    await writeFile(destination, Buffer.from(await logo.arrayBuffer()));
  }

  await query(
    `UPDATE teams SET name = $2, age_group = NULLIF($3,''), timezone = $4,
            primary_color = $5, secondary_color = $6,
            logo_key = COALESCE($7, logo_key), updated_at = now()
      WHERE id = $1`,
    [teamId, text("name"), text("ageGroup"), text("timezone") || "America/New_York",
     primary, secondary, logoKey],
  );

  // Thresholds are clamped rather than trusted: a coach who types 0 into
  // "auto-approve" would ship every uncertain clip without review.
  const autoApprove = Math.min(1, Math.max(0.5, num("autoApprove", 0.8)));
  const reviewFloor = Math.min(autoApprove - 0.05, Math.max(0, num("reviewFloor", 0.45)));

  await query(
    `INSERT INTO team_settings (
        team_id, pre_roll_seconds, post_roll_seconds, dead_time_removal,
        auto_approve_threshold, review_floor_threshold, jersey_ocr_enabled,
        music_volume_db, duck_music_on_action,
        show_intro_card, show_score_overlay, show_stat_overlay, updated_at)
     VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12, now())
     ON CONFLICT (team_id) DO UPDATE SET
        pre_roll_seconds = EXCLUDED.pre_roll_seconds,
        post_roll_seconds = EXCLUDED.post_roll_seconds,
        dead_time_removal = EXCLUDED.dead_time_removal,
        auto_approve_threshold = EXCLUDED.auto_approve_threshold,
        review_floor_threshold = EXCLUDED.review_floor_threshold,
        jersey_ocr_enabled = EXCLUDED.jersey_ocr_enabled,
        music_volume_db = EXCLUDED.music_volume_db,
        duck_music_on_action = EXCLUDED.duck_music_on_action,
        show_intro_card = EXCLUDED.show_intro_card,
        show_score_overlay = EXCLUDED.show_score_overlay,
        show_stat_overlay = EXCLUDED.show_stat_overlay,
        updated_at = now()`,
    [
      teamId,
      Math.min(30, Math.max(0, num("preRoll", 5))),
      Math.min(60, Math.max(0, num("postRoll", 8))),
      flag("deadTimeRemoval"),
      autoApprove,
      reviewFloor,
      flag("jerseyOcr"),
      Math.min(0, Math.max(-40, num("musicVolume", -18))),
      flag("duckMusic"),
      flag("showIntroCard"),
      flag("showScoreOverlay"),
      flag("showStatOverlay"),
    ],
  );

  await audit(user.id, "team.settings_updated", "team", teamId, { autoApprove, reviewFloor });
  return NextResponse.redirect(new URL("/team", request.url), { status: 303 });
}
