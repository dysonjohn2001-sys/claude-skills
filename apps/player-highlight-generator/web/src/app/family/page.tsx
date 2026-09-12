import { requireUser } from "@/lib/auth";
import { query } from "@/lib/db";
import { duration } from "@/lib/format";

export const dynamic = "force-dynamic";

/**
 * The guardian view. It is scoped by the guardian's own record, not by anything
 * in the URL, so a parent cannot reach another family's reels by guessing ids.
 */
export default async function FamilyPage() {
  const user = await requireUser();

  const reels = await query<{
    id: string;
    title: string;
    aspect: string;
    scope: string;
    duration_seconds: string | null;
    output_key: string | null;
    rendered_at: string | null;
    player_name: string;
    allow_download: boolean;
  }>(
    `SELECT DISTINCT r.id, r.title, r.aspect, r.scope, r.duration_seconds, r.output_key,
            r.rendered_at,
            p.first_name || ' ' || p.last_name AS player_name,
            bool_or(sl.allow_download) AS allow_download
       FROM guardians gu
       JOIN player_guardians pg   ON pg.guardian_id = gu.id
       JOIN players p             ON p.id = pg.player_id
       JOIN reels r               ON r.player_id = p.id
       JOIN share_links sl        ON sl.reel_id = r.id AND sl.revoked_at IS NULL
                                 AND sl.expires_at > now()
       JOIN share_link_grants slg ON slg.share_link_id = sl.id AND slg.guardian_id = gu.id
      WHERE gu.user_id = $1 AND r.output_key IS NOT NULL
   GROUP BY r.id, p.first_name, p.last_name
   ORDER BY r.rendered_at DESC NULLS LAST`,
    [user.id],
  );

  return (
    <>
      <h2>Your family&apos;s highlights</h2>
      <p className="subtitle">
        Reels your coach has shared with you. These are private to your account and are not listed
        publicly anywhere.
      </p>

      {reels.length === 0 && (
        <div className="notice">
          Nothing has been shared with you yet. Your coach shares reels once they have been reviewed.
        </div>
      )}

      <div className="grid cols-2">
        {reels.map((r) => (
          <div key={r.id} className="card">
            <h3 style={{ marginTop: 0 }}>{r.title}</h3>
            <p className="muted small">
              {r.player_name} · {r.scope} · {r.aspect}
              {r.duration_seconds ? ` · ${duration(Number(r.duration_seconds))}` : ""}
            </p>
            <video controls preload="metadata" src={`/api/media/${encodeURI(r.output_key!)}`} />
            {r.allow_download && (
              <p className="small" style={{ marginBottom: 0 }}>
                <a href={`/api/media/${encodeURI(r.output_key!)}?download=1`}>Download MP4</a>
              </p>
            )}
          </div>
        ))}
      </div>
    </>
  );
}
