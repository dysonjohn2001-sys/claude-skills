import { NextResponse } from "next/server";
import { z } from "zod";

import { requireCoach } from "@/lib/auth";
import { audit, enqueueJob, queryOne } from "@/lib/db";

const PatchSchema = z.object({
  reviewStatus: z.enum(["approved", "rejected", "needs_review"]).optional(),
  playerId: z.string().uuid().optional(),
  category: z.enum(["offense", "defense", "pitching", "baserunning"]).optional(),
  preRoll: z.number().min(0).max(30).optional(),
  postRoll: z.number().min(0).max(60).optional(),
  coachNote: z.string().max(2000).optional(),
  slowmo: z
    .object({
      start: z.number().min(0),
      end: z.number().min(0),
      rate: z.number().min(0.1).max(1),
    })
    .nullable()
    .optional(),
});

/**
 * Apply a coach's review decision to one clip.
 *
 * Manual edits set match_method to 'manual' and confidence to 1.0: once a human
 * has named the player, the matcher's uncertainty about that clip is settled,
 * and a later re-match must not undo it.
 */
export async function PATCH(
  request: Request,
  { params }: { params: Promise<{ clipId: string }> },
) {
  const user = await requireCoach();
  const { clipId } = await params;

  const parsed = PatchSchema.safeParse(await request.json());
  if (!parsed.success) {
    return NextResponse.json({ error: parsed.error.issues[0].message }, { status: 400 });
  }
  const body = parsed.data;

  const before = await queryOne<{
    id: string;
    player_id: string;
    pre_roll_seconds: string;
    post_roll_seconds: string;
    source_start_seconds: string;
    source_end_seconds: string;
  }>("SELECT * FROM clips WHERE id = $1", [clipId]);
  if (!before) return NextResponse.json({ error: "Clip not found" }, { status: 404 });

  // Changing the roll moves the window around the same play instant.
  const oldPre = Number(before.pre_roll_seconds);
  const oldPost = Number(before.post_roll_seconds);
  const playAt = Number(before.source_start_seconds) + oldPre;
  const newPre = body.preRoll ?? oldPre;
  const newPost = body.postRoll ?? oldPost;

  const manual = body.playerId !== undefined || body.category !== undefined;

  const updated = await queryOne<Record<string, unknown>>(
    `UPDATE clips SET
        player_id            = COALESCE($2, player_id),
        category             = COALESCE($3::clip_category, category),
        pre_roll_seconds     = $4,
        post_roll_seconds    = $5,
        source_start_seconds = GREATEST(0, $6),
        source_end_seconds   = $7,
        review_status        = COALESCE($8::review_status, review_status),
        coach_note           = COALESCE($9, coach_note),
        slowmo_start_seconds = $10,
        slowmo_end_seconds   = $11,
        slowmo_rate          = $12,
        match_method         = CASE WHEN $13 THEN 'manual'::match_method ELSE match_method END,
        match_confidence     = CASE WHEN $13 THEN 1.0 ELSE match_confidence END,
        reviewed_by          = $14,
        reviewed_at          = now(),
        updated_at           = now()
      WHERE id = $1
      RETURNING id, player_id, category, pre_roll_seconds, post_roll_seconds,
                source_start_seconds, source_end_seconds, review_status,
                match_method, match_confidence, confidence_factors, rank_score`,
    [
      clipId,
      body.playerId ?? null,
      body.category ?? null,
      newPre,
      newPost,
      playAt - newPre,
      playAt + newPost,
      body.reviewStatus ?? null,
      body.coachNote ?? null,
      body.slowmo?.start ?? null,
      body.slowmo?.end ?? null,
      body.slowmo?.rate ?? null,
      manual,
      user.id,
    ],
  );

  await audit(user.id, "clip.reviewed", "clip", clipId, body as Record<string, unknown>);

  // Any change to the window or the slow-motion section needs a fresh cut.
  const windowChanged =
    body.preRoll !== undefined || body.postRoll !== undefined || body.slowmo !== undefined;
  if (windowChanged && body.reviewStatus !== "rejected") {
    await enqueueJob("cut_clip", "clip", clipId);
  }

  return NextResponse.json({
    id: updated!.id,
    playerId: updated!.player_id,
    category: updated!.category,
    preRoll: Number(updated!.pre_roll_seconds),
    postRoll: Number(updated!.post_roll_seconds),
    sourceStart: Number(updated!.source_start_seconds),
    sourceEnd: Number(updated!.source_end_seconds),
    reviewStatus: updated!.review_status,
    matchMethod: updated!.match_method,
    matchConfidence: Number(updated!.match_confidence),
    confidenceFactors: updated!.confidence_factors,
    rankScore: Number(updated!.rank_score),
  });
}
