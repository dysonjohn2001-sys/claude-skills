import { createHash, randomBytes } from "node:crypto";

import { audit, query, queryOne } from "./db";

export type ConsentType =
  | "media_capture"
  | "highlight_generation"
  | "family_sharing"
  | "team_sharing"
  | "external_sharing";

export interface ConsentState {
  playerId: string;
  mediaCapture: boolean;
  highlightGeneration: boolean;
  familySharing: boolean;
  teamSharing: boolean;
  externalSharing: boolean;
}

/**
 * Read the current consent state for a player.
 *
 * Consent is append-only in the database: a revocation is a new row, so this
 * reads the `effective_consents` view rather than the raw table.
 */
export async function consentFor(playerId: string): Promise<ConsentState> {
  const rows = await query<{ type: ConsentType; is_active: boolean }>(
    "SELECT type, is_active FROM effective_consents WHERE player_id = $1",
    [playerId],
  );
  const active = new Set(rows.filter((r) => r.is_active).map((r) => r.type));
  return {
    playerId,
    mediaCapture: active.has("media_capture"),
    highlightGeneration: active.has("highlight_generation"),
    familySharing: active.has("family_sharing"),
    teamSharing: active.has("team_sharing"),
    externalSharing: active.has("external_sharing"),
  };
}

export interface ConsentGate {
  allowed: boolean;
  missing: ConsentType[];
  message: string;
}

/** Whether a reel may be built for this player at all. */
export async function canGenerateHighlights(playerId: string): Promise<ConsentGate> {
  const c = await consentFor(playerId);
  const missing: ConsentType[] = [];
  if (!c.mediaCapture) missing.push("media_capture");
  if (!c.highlightGeneration) missing.push("highlight_generation");
  return {
    allowed: missing.length === 0,
    missing,
    message: missing.length
      ? "A parent or guardian has not granted the consent needed to build this player's highlights."
      : "",
  };
}

/** Whether a reel may be shared, and how far. */
export async function canShare(
  playerId: string,
  audience: "family" | "team" | "external",
): Promise<ConsentGate> {
  const c = await consentFor(playerId);
  const need: Record<typeof audience, ConsentType> = {
    family: "family_sharing",
    team: "team_sharing",
    external: "external_sharing",
  } as const;
  const required = need[audience];
  const held = {
    family_sharing: c.familySharing,
    team_sharing: c.teamSharing,
    external_sharing: c.externalSharing,
  }[required as "family_sharing" | "team_sharing" | "external_sharing"];

  return {
    allowed: held,
    missing: held ? [] : [required],
    message: held ? "" : `Sharing to ${audience} requires the ${required.replace("_", " ")} consent.`,
  };
}

// ---------------------------------------------------------------------------
// Share links
// ---------------------------------------------------------------------------

export interface ShareLinkInput {
  reelId: string;
  guardianIds: string[];
  expiresInDays: number;
  allowDownload: boolean;
  label?: string;
  createdBy: string;
}

/**
 * Mint a share link bound to named guardians.
 *
 * There is no "anyone with the link" option anywhere in this application. A
 * token that is not on a grant list opens nothing, so a forwarded URL is inert
 * for anyone who was not invited.
 */
export async function createShareLink(input: ShareLinkInput): Promise<{ token: string; id: string }> {
  if (input.guardianIds.length === 0) {
    throw new Error("a share link must name at least one guardian");
  }

  const reel = await queryOne<{ player_id: string }>("SELECT player_id FROM reels WHERE id = $1", [
    input.reelId,
  ]);
  if (!reel) throw new Error("reel not found");

  const gate = await canShare(reel.player_id, "family");
  if (!gate.allowed) throw new Error(gate.message);

  const token = randomBytes(32).toString("base64url");
  const tokenHash = createHash("sha256").update(token).digest("hex");
  const expires = new Date(Date.now() + input.expiresInDays * 86_400_000);

  const row = await queryOne<{ id: string }>(
    `INSERT INTO share_links (reel_id, token_hash, label, allow_download, expires_at, created_by)
     VALUES ($1, $2, $3, $4, $5, $6) RETURNING id`,
    [input.reelId, tokenHash, input.label ?? null, input.allowDownload, expires, input.createdBy],
  );

  for (const guardianId of input.guardianIds) {
    await query(
      "INSERT INTO share_link_grants (share_link_id, guardian_id) VALUES ($1, $2)",
      [row!.id, guardianId],
    );
  }

  await audit(input.createdBy, "share_link.created", "reel", input.reelId, {
    guardians: input.guardianIds.length,
    allowDownload: input.allowDownload,
    expiresAt: expires.toISOString(),
  });

  return { token, id: row!.id };
}

export interface ResolvedShare {
  reelId: string;
  playerName: string;
  title: string;
  outputKey: string | null;
  allowDownload: boolean;
  shareLinkId: string;
}

/**
 * Resolve a share token for a signed-in guardian.
 *
 * Four things must all hold: the token exists, it is unexpired and unrevoked,
 * it is under its view cap, and the viewer is on its grant list.
 */
export async function resolveShare(
  token: string,
  viewerUserId: string | null,
): Promise<{ share: ResolvedShare | null; reason: string }> {
  const tokenHash = createHash("sha256").update(token).digest("hex");

  const row = await queryOne<{
    id: string;
    reel_id: string;
    allow_download: boolean;
    expires_at: Date;
    revoked_at: Date | null;
    max_views: number | null;
    view_count: number;
    title: string;
    output_key: string | null;
    player_name: string;
    granted: boolean;
  }>(
    `SELECT sl.id, sl.reel_id, sl.allow_download, sl.expires_at, sl.revoked_at,
            sl.max_views, sl.view_count,
            r.title, r.output_key,
            p.first_name || ' ' || p.last_name AS player_name,
            EXISTS (
              SELECT 1 FROM share_link_grants g
                JOIN guardians gu ON gu.id = g.guardian_id
               WHERE g.share_link_id = sl.id AND gu.user_id = $2
            ) AS granted
       FROM share_links sl
       JOIN reels r   ON r.id = sl.reel_id
       JOIN players p ON p.id = r.player_id
      WHERE sl.token_hash = $1`,
    [tokenHash, viewerUserId],
  );

  if (!row) return { share: null, reason: "This link is not valid." };
  if (row.revoked_at) return { share: null, reason: "This link has been turned off by the coach." };
  if (row.expires_at < new Date()) return { share: null, reason: "This link has expired." };
  if (row.max_views !== null && row.view_count >= row.max_views) {
    return { share: null, reason: "This link has reached its view limit." };
  }
  if (!viewerUserId) return { share: null, reason: "Please sign in with the email the coach invited." };
  if (!row.granted) {
    return {
      share: null,
      reason: "This link was shared with specific families, and your account is not one of them.",
    };
  }
  if (!row.output_key) return { share: null, reason: "This reel is still rendering. Check back shortly." };

  return {
    share: {
      reelId: row.reel_id,
      playerName: row.player_name,
      title: row.title,
      outputKey: row.output_key,
      allowDownload: row.allow_download,
      shareLinkId: row.id,
    },
    reason: "",
  };
}

export async function recordShareView(
  shareLinkId: string,
  viewerUserId: string | null,
  ip?: string,
  userAgent?: string,
): Promise<void> {
  const guardian = viewerUserId
    ? await queryOne<{ id: string }>("SELECT id FROM guardians WHERE user_id = $1", [viewerUserId])
    : null;
  await query(
    `INSERT INTO share_views (share_link_id, guardian_id, ip, user_agent) VALUES ($1, $2, $3, $4)`,
    [shareLinkId, guardian?.id ?? null, ip ?? null, userAgent ?? null],
  );
  await query("UPDATE share_links SET view_count = view_count + 1 WHERE id = $1", [shareLinkId]);
}

export async function revokeShareLink(shareLinkId: string, actorId: string): Promise<void> {
  await query("UPDATE share_links SET revoked_at = now() WHERE id = $1 AND revoked_at IS NULL", [
    shareLinkId,
  ]);
  await audit(actorId, "share_link.revoked", "share_link", shareLinkId);
}
