import { createHash } from "node:crypto";
import { createWriteStream } from "node:fs";
import { mkdir } from "node:fs/promises";
import path from "node:path";
import { pipeline } from "node:stream/promises";
import { Readable } from "node:stream";

import { NextResponse } from "next/server";

import { requireCoach } from "@/lib/auth";
import { audit, enqueueJob, queryOne } from "@/lib/db";

const MEDIA_ROOT = process.env.PHG_MEDIA_ROOT ?? "/var/lib/phg/media";
const MAX_BYTES = Number(process.env.PHG_MAX_UPLOAD_BYTES ?? 16 * 1024 * 1024 * 1024);
const ALLOWED = new Set([".mp4", ".mov", ".m4v", ".mkv", ".avi"]);

export const runtime = "nodejs";
export const maxDuration = 600;

/**
 * Accept a coach-authorised video upload.
 *
 * The file is streamed straight to disk rather than buffered: a full-game
 * recording is routinely several gigabytes, and holding one in memory would
 * take the whole application down.
 */
export async function POST(request: Request) {
  const user = await requireCoach();
  const form = await request.formData();

  const gameId = String(form.get("gameId") ?? "");
  const kind = String(form.get("kind") ?? "full_game");
  const recordingStartedAt = String(form.get("recordingStartedAt") ?? "").trim();
  const file = form.get("file");

  const back = (message: string, ok = false) =>
    NextResponse.redirect(
      new URL(`/games/${gameId}?${ok ? "notice" : "error"}=${encodeURIComponent(message)}`, request.url),
      { status: 303 },
    );

  if (!(file instanceof File)) return back("No file was attached.");
  if (file.size > MAX_BYTES) return back("That file is larger than this server accepts.");

  const extension = path.extname(file.name).toLowerCase();
  if (!ALLOWED.has(extension)) {
    return back(`Unsupported file type ${extension}. Upload MP4, MOV, M4V, MKV or AVI.`);
  }

  const game = await queryOne<{ id: string }>("SELECT id FROM games WHERE id = $1", [gameId]);
  if (!game) return back("That game does not exist.");

  const asset = await queryOne<{ id: string }>(
    `INSERT INTO media_assets
       (game_id, kind, storage_key, original_filename, byte_size, recording_started_at,
        status, uploaded_by)
     VALUES ($1, $2, '', $3, $4, $5, 'uploading', $6)
     RETURNING id`,
    [
      gameId,
      kind === "clip" ? "clip" : "full_game",
      file.name,
      file.size,
      recordingStartedAt ? new Date(recordingStartedAt) : null,
      user.id,
    ],
  );

  const storageKey = `games/${gameId}/${asset!.id}${extension}`;
  const destination = path.join(MEDIA_ROOT, storageKey);
  await mkdir(path.dirname(destination), { recursive: true });

  const hash = createHash("sha256");
  const source = Readable.fromWeb(file.stream() as never);
  source.on("data", (chunk) => hash.update(chunk));

  try {
    await pipeline(source, createWriteStream(destination));
  } catch (error) {
    await queryOne(
      "UPDATE media_assets SET status = 'failed', error_message = $2 WHERE id = $1 RETURNING id",
      [asset!.id, error instanceof Error ? error.message : "write failed"],
    );
    return back("The upload did not finish. Try again.");
  }

  await queryOne(
    `UPDATE media_assets SET storage_key = $2, checksum_sha256 = $3, status = 'stored'
      WHERE id = $1 RETURNING id`,
    [asset!.id, storageKey, hash.digest("hex")],
  );

  // The worker probes the file, then queues matching for the whole game.
  await enqueueJob("probe_media", "media_asset", asset!.id, { storage_key: storageKey, game_id: gameId });
  await audit(user.id, "media.uploaded", "media_asset", asset!.id, {
    filename: file.name,
    bytes: file.size,
    gameId,
  });

  return back("Upload received. Processing has started.", true);
}
