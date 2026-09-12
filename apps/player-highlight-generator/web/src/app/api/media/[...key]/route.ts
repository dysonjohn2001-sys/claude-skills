import { createReadStream } from "node:fs";
import { stat } from "node:fs/promises";
import path from "node:path";
import { Readable } from "node:stream";

import { NextResponse } from "next/server";

import { currentUser } from "@/lib/auth";
import { queryOne } from "@/lib/db";

const MEDIA_ROOT = process.env.PHG_MEDIA_ROOT ?? "/var/lib/phg/media";

const CONTENT_TYPES: Record<string, string> = {
  ".mp4": "video/mp4",
  ".m4v": "video/mp4",
  ".mov": "video/quicktime",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
  ".mp3": "audio/mpeg",
  ".m4a": "audio/mp4",
};

/**
 * Serve a media file to an authorised viewer, with HTTP range support so the
 * review screen can scrub a three-hour recording without downloading it.
 *
 * In production put this behind signed URLs from object storage instead. This
 * route exists so the application runs end to end on a single machine.
 */
export async function GET(
  request: Request,
  { params }: { params: Promise<{ key: string[] }> },
) {
  const user = await currentUser();
  if (!user) return new NextResponse("Sign in required", { status: 401 });

  const { key } = await params;
  const storageKey = key.join("/");

  // Resolve and confine: a key containing .. must not escape the media root.
  const absolute = path.resolve(MEDIA_ROOT, storageKey);
  if (!absolute.startsWith(path.resolve(MEDIA_ROOT) + path.sep)) {
    return new NextResponse("Not found", { status: 404 });
  }

  if (!(await isAuthorised(user.id, user.role, storageKey))) {
    return new NextResponse("Not found", { status: 404 });
  }

  let info;
  try {
    info = await stat(absolute);
  } catch {
    return new NextResponse("Not found", { status: 404 });
  }

  const contentType = CONTENT_TYPES[path.extname(absolute).toLowerCase()] ?? "application/octet-stream";
  const download = new URL(request.url).searchParams.get("download") === "1";
  const disposition = download
    ? `attachment; filename="${path.basename(absolute)}"`
    : "inline";

  const range = request.headers.get("range");
  if (range) {
    const match = /bytes=(\d*)-(\d*)/.exec(range);
    const start = match?.[1] ? Number(match[1]) : 0;
    const end = match?.[2] ? Number(match[2]) : info.size - 1;
    if (start >= info.size || end >= info.size || start > end) {
      return new NextResponse(null, {
        status: 416,
        headers: { "content-range": `bytes */${info.size}` },
      });
    }
    const stream = createReadStream(absolute, { start, end });
    return new NextResponse(Readable.toWeb(stream) as ReadableStream, {
      status: 206,
      headers: {
        "content-type": contentType,
        "content-length": String(end - start + 1),
        "content-range": `bytes ${start}-${end}/${info.size}`,
        "accept-ranges": "bytes",
        "content-disposition": disposition,
        "cache-control": "private, max-age=0, no-store",
      },
    });
  }

  const stream = createReadStream(absolute);
  return new NextResponse(Readable.toWeb(stream) as ReadableStream, {
    headers: {
      "content-type": contentType,
      "content-length": String(info.size),
      "accept-ranges": "bytes",
      "content-disposition": disposition,
      "cache-control": "private, max-age=0, no-store",
    },
  });
}

/**
 * Coaches may read anything their team owns. Guardians may read only reel
 * outputs shared with them by an active, unexpired link.
 */
async function isAuthorised(userId: string, role: string, storageKey: string): Promise<boolean> {
  if (role !== "guardian") return true;

  const allowed = await queryOne(
    `SELECT 1
       FROM guardians gu
       JOIN share_link_grants slg ON slg.guardian_id = gu.id
       JOIN share_links sl        ON sl.id = slg.share_link_id
       JOIN reels r               ON r.id = sl.reel_id
      WHERE gu.user_id = $1
        AND r.output_key = $2
        AND sl.revoked_at IS NULL
        AND sl.expires_at > now()`,
    [userId, storageKey],
  );
  return allowed !== null;
}
