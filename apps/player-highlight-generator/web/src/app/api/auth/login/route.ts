import { scrypt, timingSafeEqual } from "node:crypto";
import { promisify } from "node:util";

import { NextResponse } from "next/server";

import { audit, queryOne } from "@/lib/db";
import { createSession } from "@/lib/auth";

const scryptAsync = promisify(scrypt) as (
  password: string,
  salt: string,
  keylen: number,
) => Promise<Buffer>;

/** Stored format: scrypt$<saltHex>$<hashHex>. */
async function verify(password: string, stored: string): Promise<boolean> {
  const [scheme, salt, expected] = stored.split("$");
  if (scheme !== "scrypt" || !salt || !expected) return false;
  const derived = await scryptAsync(password, salt, 64);
  const expectedBuffer = Buffer.from(expected, "hex");
  return derived.length === expectedBuffer.length && timingSafeEqual(derived, expectedBuffer);
}

export async function POST(request: Request) {
  const form = await request.formData();
  const email = String(form.get("email") ?? "").trim();
  const password = String(form.get("password") ?? "");
  const next = String(form.get("next") ?? "/");
  const fail = (message: string) =>
    NextResponse.redirect(
      new URL(`/login?error=${encodeURIComponent(message)}`, request.url),
      { status: 303 },
    );

  if (!email || !password) return fail("Enter your email and password.");

  const user = await queryOne<{ id: string; password_hash: string | null; role: string }>(
    "SELECT id, password_hash, role FROM users WHERE email = $1 AND is_active",
    [email],
  );

  // Same message either way, so this endpoint does not confirm which emails exist.
  if (!user?.password_hash || !(await verify(password, user.password_hash))) {
    await audit(null, "auth.login_failed", "user", null, { email });
    return fail("That email and password did not match.");
  }

  const headers = request.headers;
  await createSession(
    user.id,
    headers.get("x-forwarded-for") ?? undefined,
    headers.get("user-agent") ?? undefined,
  );
  await queryOne("UPDATE users SET last_login_at = now() WHERE id = $1 RETURNING id", [user.id]);
  await audit(user.id, "auth.login", "user", user.id);

  const destination = user.role === "guardian" ? "/family" : next;
  return NextResponse.redirect(new URL(destination, request.url), { status: 303 });
}
