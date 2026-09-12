import { NextResponse } from "next/server";
import { z } from "zod";

import { requireCoach } from "@/lib/auth";
import { audit, queryOne } from "@/lib/db";

const Schema = z.object({
  mediaAssetId: z.string().uuid(),
  videoSeconds: z.number().min(0),
  playId: z.string().uuid().nullable().optional(),
  wallClockAt: z.string().datetime().nullable().optional(),
});

/**
 * Record a sync point: "this moment in the video is this moment in the game".
 *
 * One anchor fixes the offset between the camera clock and the scorekeeper's.
 * Two or more also let the worker solve for drift, which matters over a
 * three-hour recording where a phone clock can wander by several seconds.
 */
export async function POST(
  request: Request,
  { params }: { params: Promise<{ gameId: string }> },
) {
  const user = await requireCoach();
  const { gameId } = await params;

  const parsed = Schema.safeParse(await request.json());
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.issues[0].message }, { status: 400 });
  }
  const { mediaAssetId, videoSeconds, playId, wallClockAt } = parsed.data;

  const asset = await queryOne<{ id: string }>(
    "SELECT id FROM media_assets WHERE id = $1 AND game_id = $2",
    [mediaAssetId, gameId],
  );
  if (!asset) return NextResponse.json({ error: "Video not found for this game" }, { status: 404 });

  if (!playId && !wallClockAt) {
    return NextResponse.json(
      { error: "Select a clip first, or supply a wall-clock time, so the anchor has something to point at." },
      { status: 400 },
    );
  }

  // Anchoring to the same spot twice should move the anchor, not stack two.
  await queryOne(
    `DELETE FROM media_sync_anchors
      WHERE media_asset_id = $1 AND abs(video_seconds - $2) < 2 RETURNING id`,
    [mediaAssetId, videoSeconds],
  );

  const anchor = await queryOne<{ id: string }>(
    `INSERT INTO media_sync_anchors (media_asset_id, video_seconds, play_id, wall_clock_at, created_by)
     VALUES ($1, $2, $3, $4, $5) RETURNING id`,
    [mediaAssetId, videoSeconds, playId ?? null, wallClockAt ? new Date(wallClockAt) : null, user.id],
  );

  await audit(user.id, "media.anchor_set", "media_asset", mediaAssetId, { videoSeconds, playId });

  const count = await queryOne<{ n: number }>(
    "SELECT count(*)::int AS n FROM media_sync_anchors WHERE media_asset_id = $1",
    [mediaAssetId],
  );

  return NextResponse.json({ id: anchor!.id, anchorCount: count?.n ?? 1 });
}
