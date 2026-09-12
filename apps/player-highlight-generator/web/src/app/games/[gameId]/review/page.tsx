import { notFound } from "next/navigation";

import ReviewWorkspace, {
  type ReviewClip,
  type ReviewMedia,
  type RosterOption,
} from "@/components/ReviewWorkspace";
import { requireCoach } from "@/lib/auth";
import { query, queryOne } from "@/lib/db";
import { gameLabel } from "@/lib/format";

export const dynamic = "force-dynamic";

export default async function ReviewPage({ params }: { params: Promise<{ gameId: string }> }) {
  await requireCoach();
  const { gameId } = await params;

  const game = await queryOne<{ id: string; played_on: string; opponent_name: string }>(
    "SELECT id, played_on, opponent_name FROM games WHERE id = $1",
    [gameId],
  );
  if (!game) notFound();

  const mediaRows = await query<{
    id: string;
    original_filename: string;
    storage_key: string;
    duration_seconds: string | null;
    kind: string;
  }>(
    `SELECT id, original_filename, storage_key, duration_seconds, kind
       FROM media_assets
      WHERE game_id = $1 AND status = 'ready'
   ORDER BY created_at`,
    [gameId],
  );

  const media: ReviewMedia[] = mediaRows.map((m) => ({
    id: m.id,
    label: `${m.original_filename}${m.kind === "clip" ? " (clip)" : ""}`,
    url: `/api/media/${encodeURI(m.storage_key)}`,
    durationSeconds: Number(m.duration_seconds ?? 0),
  }));

  const clipRows = await query<{
    id: string;
    player_id: string;
    player_name: string;
    jersey_number: string | null;
    media_asset_id: string;
    category: ReviewClip["category"];
    source_start_seconds: string;
    source_end_seconds: string;
    pre_roll_seconds: string;
    post_roll_seconds: string;
    match_confidence: string;
    match_method: string;
    confidence_factors: Record<string, number>;
    review_status: ReviewClip["reviewStatus"];
    rank_score: string;
    title: string | null;
    play_description: string | null;
    inning: number | null;
    half: string | null;
    play_id: string | null;
    thumbnail_key: string | null;
  }>(
    `SELECT c.id, c.player_id, c.media_asset_id, c.category,
            c.source_start_seconds, c.source_end_seconds,
            c.pre_roll_seconds, c.post_roll_seconds,
            c.match_confidence, c.match_method, c.confidence_factors,
            c.review_status, c.rank_score, c.title, c.thumbnail_key,
            pl.first_name || ' ' || pl.last_name AS player_name,
            pl.jersey_number,
            p.description AS play_description, p.inning, p.half, p.id AS play_id
       FROM clips c
       JOIN players pl ON pl.id = c.player_id
  LEFT JOIN plays p    ON p.id = c.play_id
      WHERE p.game_id = $1
   ORDER BY c.source_start_seconds`,
    [gameId],
  );

  const clips: ReviewClip[] = clipRows.map((c) => ({
    id: c.id,
    playerId: c.player_id,
    playerName: c.player_name,
    jerseyNumber: c.jersey_number,
    mediaAssetId: c.media_asset_id,
    category: c.category,
    sourceStart: Number(c.source_start_seconds),
    sourceEnd: Number(c.source_end_seconds),
    preRoll: Number(c.pre_roll_seconds),
    postRoll: Number(c.post_roll_seconds),
    matchConfidence: Number(c.match_confidence),
    matchMethod: c.match_method,
    confidenceFactors: c.confidence_factors ?? {},
    reviewStatus: c.review_status,
    rankScore: Number(c.rank_score),
    title: c.title ?? "",
    playDescription: c.play_description,
    inning: c.inning,
    half: c.half,
    playId: c.play_id,
    thumbnailUrl: c.thumbnail_key ? `/api/media/${encodeURI(c.thumbnail_key)}` : null,
  }));

  const rosterRows = await query<{ id: string; name: string; jersey_number: string | null }>(
    `SELECT p.id, p.first_name || ' ' || p.last_name AS name, p.jersey_number
       FROM games g
       JOIN seasons s ON s.id = g.season_id
       JOIN players p ON p.team_id = s.team_id AND p.is_active
      WHERE g.id = $1
   ORDER BY p.last_name, p.first_name`,
    [gameId],
  );
  const roster: RosterOption[] = rosterRows.map((r) => ({
    id: r.id,
    name: r.name,
    jerseyNumber: r.jersey_number,
  }));

  const pending = clips.filter((c) => c.reviewStatus === "needs_review").length;

  return (
    <>
      <h2>Review · {gameLabel(game)}</h2>
      <p className="subtitle">
        {clips.length} clips matched, {pending} flagged as uncertain. Approving a clip makes it
        eligible for that player&apos;s reels; rejecting it removes it for good.
      </p>
      <p className="small">
        <a href={`/games/${gameId}`}>Back to game</a>
      </p>

      <ReviewWorkspace gameId={gameId} media={media} clips={clips} roster={roster} />
    </>
  );
}
