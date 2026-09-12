import { NextResponse } from "next/server";

import { requireCoach } from "@/lib/auth";
import { audit, enqueueJob, queryOne } from "@/lib/db";

export async function POST(
  request: Request,
  { params }: { params: Promise<{ gameId: string }> },
) {
  const user = await requireCoach();
  const { gameId } = await params;

  const ready = await queryOne<{ media: number; plays: number }>(
    `SELECT (SELECT count(*) FROM media_assets WHERE game_id = $1 AND status = 'ready')::int AS media,
            (SELECT count(*) FROM plays WHERE game_id = $1)::int AS plays`,
    [gameId],
  );
  if (!ready?.media || !ready.plays) {
    return NextResponse.redirect(
      new URL(
        `/games/${gameId}?error=${encodeURIComponent(
          "Matching needs at least one processed video and an imported play-by-play file.",
        )}`,
        request.url,
      ),
      { status: 303 },
    );
  }

  await enqueueJob("match_plays", "game", gameId);
  await audit(user.id, "game.match_requested", "game", gameId);

  return NextResponse.redirect(
    new URL(
      `/games/${gameId}?notice=${encodeURIComponent(
        "Matching queued. Clips will appear in the review screen as the worker finishes.",
      )}`,
      request.url,
    ),
    { status: 303 },
  );
}
