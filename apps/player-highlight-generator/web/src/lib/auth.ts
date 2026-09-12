import { createHash, randomBytes, timingSafeEqual } from "node:crypto";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

import { query, queryOne } from "./db";

export const SESSION_COOKIE = "phg_session";
const SESSION_DAYS = 14;

export type Role = "admin" | "coach" | "assistant_coach" | "guardian";

export interface SessionUser {
  id: string;
  email: string;
  fullName: string;
  role: Role;
}

function hashToken(token: string): string {
  return createHash("sha256").update(token).digest("hex");
}

/** Issue a session and return the opaque cookie value (shown once, never stored). */
export async function createSession(userId: string, ip?: string, userAgent?: string): Promise<string> {
  const token = randomBytes(32).toString("base64url");
  const expires = new Date(Date.now() + SESSION_DAYS * 86_400_000);
  await query(
    `INSERT INTO sessions (user_id, token_hash, expires_at, created_ip, user_agent)
     VALUES ($1, $2, $3, $4, $5)`,
    [userId, hashToken(token), expires, ip ?? null, userAgent ?? null],
  );

  const jar = await cookies();
  jar.set(SESSION_COOKIE, token, {
    httpOnly: true,
    sameSite: "lax",
    secure: process.env.NODE_ENV === "production",
    path: "/",
    expires,
  });
  return token;
}

export async function destroySession(): Promise<void> {
  const jar = await cookies();
  const token = jar.get(SESSION_COOKIE)?.value;
  if (token) await query("DELETE FROM sessions WHERE token_hash = $1", [hashToken(token)]);
  jar.delete(SESSION_COOKIE);
}

export async function currentUser(): Promise<SessionUser | null> {
  const jar = await cookies();
  const token = jar.get(SESSION_COOKIE)?.value;
  if (!token) return null;

  const row = await queryOne<{
    id: string;
    email: string;
    full_name: string;
    role: Role;
  }>(
    `SELECT u.id, u.email, u.full_name, u.role
       FROM sessions s JOIN users u ON u.id = s.user_id
      WHERE s.token_hash = $1 AND s.expires_at > now() AND u.is_active`,
    [hashToken(token)],
  );
  if (!row) return null;
  return { id: row.id, email: row.email, fullName: row.full_name, role: row.role };
}

export async function requireUser(): Promise<SessionUser> {
  const user = await currentUser();
  if (!user) redirect("/login");
  return user;
}

/** Coaches and admins manage data; guardians only ever view their own child's reels. */
export async function requireCoach(): Promise<SessionUser> {
  const user = await requireUser();
  if (user.role === "guardian") redirect("/family");
  return user;
}

/** Guard a team-scoped page: membership is checked, not assumed from the URL. */
export async function requireTeamAccess(teamId: string): Promise<SessionUser> {
  const user = await requireUser();
  if (user.role === "admin") return user;
  const member = await queryOne(
    "SELECT 1 FROM team_members WHERE team_id = $1 AND user_id = $2",
    [teamId, user.id],
  );
  if (!member) redirect("/");
  return user;
}

/** Constant-time compare for share tokens, which arrive from untrusted URLs. */
export function tokenMatches(candidateHash: string, storedHash: string): boolean {
  const a = Buffer.from(candidateHash, "hex");
  const b = Buffer.from(storedHash, "hex");
  return a.length === b.length && timingSafeEqual(a, b);
}

export { hashToken };
