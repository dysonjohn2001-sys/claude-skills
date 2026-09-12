# Privacy and consent

Every subject in this application is a child. That single fact drove more design
decisions than any technical constraint.

This document describes what the application does. It is not legal advice. If
you operate this for a club rather than your own team, talk to someone who knows
your jurisdiction: COPPA in the United States, UK GDPR and the Age Appropriate
Design Code in the United Kingdom, GDPR Article 8 across the EU, and state
biometric laws such as Illinois BIPA all have something to say about video of
minors.

---

## The five consents

Consent is recorded per player, per purpose. They are separate because they are
genuinely different decisions, and bundling them would make the broadest one the
price of the narrowest.

| Consent | What it permits | Effect when absent |
|---|---|---|
| `media_capture` | The child may appear in team-recorded video at all | No clips are cut |
| `highlight_generation` | Personal highlight reels may be built | The matcher skips this player entirely |
| `family_sharing` | Reels may be shared with this child's own guardians | No share link can be created |
| `team_sharing` | Reels may be visible to other families on the team | Team-wide sharing is refused |
| `external_sharing` | Reels may be downloaded and posted off-platform | Download is off |

`external_sharing` is off by default in the seed data, and deliberately so. A
parent who is happy for their child to appear in a team video is not thereby
happy for that video to be on a public account.

---

## Where the gate is enforced

In three places, on purpose:

1. **The interface.** Blocked players show the reason and the render button is
   disabled.
2. **The API.** `/api/reels` re-checks `canGenerateHighlights` before queuing
   anything, so a crafted request gets the same answer as the button.
3. **The worker.** `match_plays` loads the consented player set and skips
   everyone else before any clip row is written.

A check in the UI alone is a suggestion. A check at every layer is a rule.

---

## Consent is append-only

```sql
CREATE TABLE consents (
  player_id   UUID NOT NULL,
  guardian_id UUID NOT NULL,
  type        consent_type NOT NULL,
  granted     BOOLEAN NOT NULL,
  granted_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  revoked_at  TIMESTAMPTZ,
  ...
);
```

Rows are never updated. A revocation is a new dated row, and current state is
read through the `effective_consents` view.

This matters because the question that gets asked after something goes wrong is
not "what is permitted now" but "what was permitted when this reel was made".
An `UPDATE` destroys the only record that answers it.

An unticked checkbox is recorded as an explicit `granted = false`, not left as a
silent gap, so "they said no" and "nobody asked" are distinguishable.

`guardian_id` is `ON DELETE RESTRICT`: deleting a guardian record must not
silently erase the consent they gave.

---

## Revocation reaches things that already exist

Revoking `highlight_generation` stops new clips at the next matching run.

Revoking `family_sharing` does more: in the same transaction, every share link
for that player is revoked. Those URLs stop working immediately, for everyone
who has them.

```sql
UPDATE share_links sl SET revoked_at = now()
  FROM reels r
 WHERE r.id = sl.reel_id AND r.player_id = $1 AND sl.revoked_at IS NULL;
```

A consent model where withdrawal only affects the future is not much of a
consent model.

---

## No facial recognition

There is no face detection, no face embedding, no biometric template of any
kind, anywhere in this codebase.

The only thing extracted from a video frame is **printed digits on fabric**. The
pipeline finds person-shaped boxes with OpenCV's stock HOG pedestrian detector,
crops the upper-back band, and reads it with Tesseract restricted to digits. A
person detector locates a rectangle; it does not identify anyone.

That is also why jersey recognition is secondary rather than primary. The
scorebook already knows who was batting. Reaching for computer vision to answer
a question the data answers, on footage of children, would be the wrong trade
even if it worked better — and on 1080p footage shot from the bleachers, it does
not work better.

Every digit read is stored in `jersey_observations` with its timestamp,
confidence and bounding box, so the claim that it never overrides the scorebook
is checkable rather than promised. It can move a confidence score by at most
0.18, and only for clips already flagged as uncertain.

---

## What is stored, and what is not

**Stored**

- Name, preferred name, jersey number, positions, batting hand, throwing hand.
- **Birth year only.** Not a full date of birth.
- Guardian name, email and optionally phone.
- Video the coach uploaded, clips cut from it, rendered reels.
- Play-by-play as imported, including the original CSV row.
- Confidence and ranking factors, so decisions can be explained.
- Jersey digit observations with bounding boxes.
- An audit log of logins, uploads, imports, review decisions, consent changes
  and share activity.

**Not stored**

- Full dates of birth.
- Home addresses.
- Any biometric identifier, template or face embedding.
- Anything at all about children on the opposing team. Opponent players appear
  in the footage but are never named, matched, clipped or given a record. Plays
  where the opposition is batting exist only to credit **our** fielders and
  pitcher.

---

## Sharing

**There is no public link option.** Not disabled, not discouraged — absent from
the schema.

Every share link is bound to named guardians through `share_link_grants`. A
token that is not on a grant list opens nothing, so a forwarded URL is inert for
anyone who was not invited: they still have to sign in as a guardian the coach
named.

Links carry:

- An expiry, defaulting to 30 days.
- An optional view cap.
- A per-link download flag, off by default.
- Revocation at any time, by the coach or automatically by consent withdrawal.

Tokens are 256 bits from a cryptographic source, stored as SHA-256 hashes. The
raw token is shown once at creation and cannot be recovered — if a coach loses
it, they mint a new one.

Every view is logged: which guardian, when, from which address.

The parent view is scoped by the guardian's own record rather than by anything
in the URL, so a parent cannot reach another family's reels by guessing ids. The
media route enforces the same rule at the file level: a guardian can read a reel
file only while an active, unexpired link names them.

---

## Retention

No automatic deletion is implemented, because the right policy depends on the
club and getting it wrong destroys memories. What exists is the machinery to
enforce one:

- `ON DELETE CASCADE` from players through clips and reels, so removing a player
  removes their derived media in one statement.
- Storage keys are relative, so orphan-file cleanup is a directory walk against
  the database.
- The audit log records what existed and when, so deletion can be evidenced.

A reasonable policy for a club to adopt: source recordings deleted at the end of
the season, reels retained while the player is on the roster, everything removed
within 30 days of a parent asking.

---

## Operational notes

- **Put TLS in front of it.** The compose file binds to `127.0.0.1` on purpose.
  Nothing here is designed to face the internet directly.
- **Every page sends `X-Robots-Tag: noindex, nofollow, noarchive`.** A private
  application should not be discoverable.
- **Media responses are `Cache-Control: private, no-store`**, so a shared
  computer does not keep a copy in the browser cache.
- **Accounts are created by the coach**, with `scripts/create-user.py`. There is
  no self-service registration and no seeded account with a known password.
- **The demo seed creates no users.** A seeded login with a published password is
  how a private application stops being private.

---

## A checklist before the first real game

- [ ] Every family has seen, in writing, what this does and what will be shared.
- [ ] Consent is recorded for every player, with the unticked boxes recorded as
      explicit noes.
- [ ] The consent page shows nobody unexpectedly blocked.
- [ ] TLS is terminating in front of the application.
- [ ] `POSTGRES_PASSWORD` is not the value from `.env.example`.
- [ ] You know who to contact, and how fast, if a parent asks for removal.
- [ ] Music you uploaded has its licence recorded.
