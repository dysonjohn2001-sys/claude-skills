import { NextResponse } from "next/server";

import { requireCoach } from "@/lib/auth";
import { audit, query } from "@/lib/db";

const TYPES = [
  "media_capture",
  "highlight_generation",
  "family_sharing",
  "team_sharing",
  "external_sharing",
] as const;

/**
 * Record a guardian's consent decisions.
 *
 * Every submission appends new dated rows. Nothing is updated in place, so the
 * record of what was permitted at the time a reel was made survives a later
 * change of mind.
 */
export async function POST(request: Request) {
  const user = await requireCoach();
  const form = await request.formData();
  const playerId = String(form.get("playerId") ?? "");
  const guardianId = String(form.get("guardianId") ?? "");
  const note = String(form.get("note") ?? "").trim() || null;

  if (!playerId || !guardianId) {
    return NextResponse.redirect(
      new URL(`/team/consent?error=${encodeURIComponent("Pick a player and a guardian.")}`, request.url),
      { status: 303 },
    );
  }

  const ip = request.headers.get("x-forwarded-for");

  for (const type of TYPES) {
    // An absent checkbox is an explicit "no", recorded as such rather than
    // left as a silent gap.
    const granted = form.get(type) !== null;
    await query(
      `INSERT INTO consents (player_id, guardian_id, type, granted, recorded_ip, note)
       VALUES ($1, $2, $3, $4, $5, $6)`,
      [playerId, guardianId, type, granted, ip, note],
    );
  }

  // Revoking family sharing must reach reels that are already out there.
  const familyGranted = form.get("family_sharing") !== null;
  if (!familyGranted) {
    await query(
      `UPDATE share_links sl SET revoked_at = now()
         FROM reels r
        WHERE r.id = sl.reel_id AND r.player_id = $1 AND sl.revoked_at IS NULL`,
      [playerId],
    );
  }

  await audit(user.id, "consent.recorded", "player", playerId, {
    guardianId,
    granted: TYPES.filter((t) => form.get(t) !== null),
  });

  return NextResponse.redirect(new URL("/team/consent", request.url), { status: 303 });
}
