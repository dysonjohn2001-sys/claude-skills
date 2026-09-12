import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";

import { NextResponse } from "next/server";

import { requireCoach } from "@/lib/auth";
import { audit, query, queryOne } from "@/lib/db";

const MEDIA_ROOT = process.env.PHG_MEDIA_ROOT ?? "/var/lib/phg/media";
const ALLOWED = new Set([".mp3", ".m4a", ".wav", ".aac", ".ogg"]);

export const runtime = "nodejs";

export async function POST(request: Request) {
  const user = await requireCoach();
  const form = await request.formData();
  const teamId = String(form.get("teamId") ?? "");
  const file = form.get("file");

  const back = (key: "notice" | "error", message: string) =>
    NextResponse.redirect(
      new URL(`/team/music?${key}=${encodeURIComponent(message)}`, request.url),
      { status: 303 },
    );

  if (!(file instanceof File)) return back("error", "No audio file was attached.");
  const extension = path.extname(file.name).toLowerCase();
  if (!ALLOWED.has(extension)) return back("error", `Unsupported audio type ${extension}.`);

  const track = await queryOne<{ id: string }>(
    `INSERT INTO music_tracks (team_id, title, artist, license, storage_key, is_default)
     VALUES ($1, $2, NULLIF($3,''), $4, '', $5) RETURNING id`,
    [
      teamId,
      String(form.get("title") ?? "Untitled"),
      String(form.get("artist") ?? ""),
      String(form.get("license") ?? "unspecified"),
      form.get("isDefault") !== null,
    ],
  );

  const storageKey = `music/${track!.id}${extension}`;
  const destination = path.join(MEDIA_ROOT, storageKey);
  await mkdir(path.dirname(destination), { recursive: true });
  await writeFile(destination, Buffer.from(await file.arrayBuffer()));

  await query("UPDATE music_tracks SET storage_key = $2 WHERE id = $1", [track!.id, storageKey]);

  if (form.get("isDefault") !== null) {
    await query("UPDATE music_tracks SET is_default = FALSE WHERE team_id = $1 AND id <> $2", [
      teamId,
      track!.id,
    ]);
    await query(
      `INSERT INTO team_settings (team_id, default_music_track_id)
       VALUES ($1, $2)
       ON CONFLICT (team_id) DO UPDATE SET default_music_track_id = EXCLUDED.default_music_track_id`,
      [teamId, track!.id],
    );
  }

  await audit(user.id, "music.uploaded", "music_track", track!.id, { filename: file.name });
  return back("notice", "Track added.");
}
