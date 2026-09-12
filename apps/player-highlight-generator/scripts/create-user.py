#!/usr/bin/env python3
"""Create or update a user account.

    python3 scripts/create-user.py coach@example.com "Sam Rivera" --role coach

The password is read from stdin or prompted, never taken as an argument, so it
does not end up in shell history or the process list. Hashes are scrypt with a
random 16-byte salt, matching what web/src/app/api/auth/login/route.ts verifies.
"""

from __future__ import annotations

import argparse
import getpass
import hashlib
import os
import secrets
import sys

try:
    import psycopg
except ImportError:
    sys.exit("psycopg is required: pip install 'psycopg[binary]'")

ROLES = ("admin", "coach", "assistant_coach", "guardian")


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    derived = hashlib.scrypt(password.encode(), salt=salt.encode(), n=16384, r=8, p=1, dklen=64)
    return f"scrypt${salt}${derived.hex()}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("email")
    parser.add_argument("full_name")
    parser.add_argument("--role", choices=ROLES, default="coach")
    parser.add_argument("--team-id", help="also add the user to this team")
    parser.add_argument("--dsn", default=os.environ.get("DATABASE_URL"))
    args = parser.parse_args()

    if not args.dsn:
        return fail("set DATABASE_URL or pass --dsn")

    password = (
        sys.stdin.read().strip()
        if not sys.stdin.isatty()
        else getpass.getpass("Password: ")
    )
    if len(password) < 10:
        return fail("use at least 10 characters")
    if sys.stdin.isatty() and password != getpass.getpass("Confirm: "):
        return fail("passwords did not match")

    with psycopg.connect(args.dsn) as conn, conn.cursor() as cur:
        cur.execute(
            """INSERT INTO users (email, full_name, password_hash, role)
               VALUES (%s, %s, %s, %s)
               ON CONFLICT (email) DO UPDATE
                 SET full_name = EXCLUDED.full_name,
                     password_hash = EXCLUDED.password_hash,
                     role = EXCLUDED.role,
                     updated_at = now()
               RETURNING id""",
            (args.email, args.full_name, hash_password(password), args.role),
        )
        user_id = cur.fetchone()[0]

        if args.team_id:
            cur.execute(
                """INSERT INTO team_members (team_id, user_id, role)
                   VALUES (%s, %s, %s) ON CONFLICT (team_id, user_id) DO UPDATE
                     SET role = EXCLUDED.role""",
                (args.team_id, user_id, args.role),
            )

        # A guardian account only becomes useful once it is linked to the
        # guardian record the roster import created.
        if args.role == "guardian":
            cur.execute(
                "UPDATE guardians SET user_id = %s WHERE lower(email) = lower(%s) AND user_id IS NULL",
                (user_id, args.email),
            )
            if cur.rowcount == 0:
                print(
                    f"note: no guardian record matches {args.email}; "
                    "add them to a player on the roster page so they can see reels",
                    file=sys.stderr,
                )

    print(f"{args.email} ready as {args.role} ({user_id})")
    return 0


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
