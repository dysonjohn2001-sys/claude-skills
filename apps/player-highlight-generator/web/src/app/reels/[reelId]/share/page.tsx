import { notFound } from "next/navigation";

import { requireCoach } from "@/lib/auth";
import { query, queryOne } from "@/lib/db";
import { canShare } from "@/lib/permissions";

export const dynamic = "force-dynamic";

export default async function ShareReelPage({
  params,
  searchParams,
}: {
  params: Promise<{ reelId: string }>;
  searchParams: Promise<{ notice?: string; error?: string }>;
}) {
  await requireCoach();
  const { reelId } = await params;
  const flash = await searchParams;

  const reel = await queryOne<{
    id: string;
    title: string;
    player_id: string;
    player_name: string;
    output_key: string | null;
  }>(
    `SELECT r.id, r.title, r.player_id, r.output_key,
            p.first_name || ' ' || p.last_name AS player_name
       FROM reels r JOIN players p ON p.id = r.player_id WHERE r.id = $1`,
    [reelId],
  );
  if (!reel) notFound();

  const gate = await canShare(reel.player_id, "family");

  const guardians = await query<{ id: string; full_name: string; email: string; has_account: boolean }>(
    `SELECT g.id, g.full_name, g.email, g.user_id IS NOT NULL AS has_account
       FROM player_guardians pg JOIN guardians g ON g.id = pg.guardian_id
      WHERE pg.player_id = $1 ORDER BY g.full_name`,
    [reel.player_id],
  );

  const links = await query<{
    id: string;
    label: string | null;
    expires_at: string;
    allow_download: boolean;
    view_count: number;
    revoked_at: string | null;
    recipients: string;
  }>(
    `SELECT sl.id, sl.label, sl.expires_at, sl.allow_download, sl.view_count, sl.revoked_at,
            string_agg(g.full_name, ', ') AS recipients
       FROM share_links sl
  LEFT JOIN share_link_grants slg ON slg.share_link_id = sl.id
  LEFT JOIN guardians g           ON g.id = slg.guardian_id
      WHERE sl.reel_id = $1
   GROUP BY sl.id
   ORDER BY sl.created_at DESC`,
    [reelId],
  );

  return (
    <>
      <h2>Share · {reel.title}</h2>
      <p className="subtitle">
        Links are bound to the families you name here. Forwarding one does not grant anybody else
        access, because the recipient still has to sign in as an invited guardian.
      </p>

      {flash.notice && <div className="notice">{flash.notice}</div>}
      {flash.error && <div className="notice error">{flash.error}</div>}
      {!gate.allowed && <div className="notice error">{gate.message}</div>}
      {!reel.output_key && (
        <div className="notice warn">This reel has not finished rendering yet.</div>
      )}

      <form action="/api/share" method="post" className="card">
        <input type="hidden" name="reelId" value={reelId} />
        <input type="hidden" name="action" value="create" />

        <div className="field">
          <label>Share with</label>
          {guardians.length === 0 && (
            <p className="muted small">
              No guardians on file for {reel.player_name}. <a href="/team/roster">Add them</a> first.
            </p>
          )}
          {guardians.map((g) => (
            <label key={g.id} style={{ color: "var(--text)", marginBottom: 6 }}>
              <input type="checkbox" name="guardianIds" value={g.id}
                     style={{ width: "auto", marginRight: 8 }} />
              {g.full_name} <span className="muted small">{g.email}</span>
              {!g.has_account && <span className="badge neutral" style={{ marginLeft: 8 }}>no account yet</span>}
            </label>
          ))}
        </div>

        <div className="row">
          <div className="field" style={{ flex: "0 0 160px" }}>
            <label htmlFor="expiresInDays">Expires in (days)</label>
            <input id="expiresInDays" name="expiresInDays" type="number" min={1} max={365} defaultValue={30} />
          </div>
          <div className="field" style={{ flex: "1 1 220px" }}>
            <label htmlFor="label">Label (for your reference)</label>
            <input id="label" name="label" placeholder="Grandparents" />
          </div>
          <div className="field" style={{ flex: "1 1 220px" }}>
            <label>
              <input type="checkbox" name="allowDownload" style={{ width: "auto", marginRight: 8 }} />
              Allow downloading the MP4
            </label>
          </div>
        </div>

        <button type="submit" className="primary" disabled={!gate.allowed || !reel.output_key}>
          Create link
        </button>
      </form>

      <h3>Existing links</h3>
      <div className="card" style={{ padding: 0 }}>
        <table>
          <thead>
            <tr>
              <th>Label</th>
              <th>Recipients</th>
              <th>Expires</th>
              <th>Download</th>
              <th>Views</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {links.map((l) => (
              <tr key={l.id} style={{ opacity: l.revoked_at ? 0.5 : 1 }}>
                <td>{l.label ?? "-"}</td>
                <td className="small">{l.recipients ?? "-"}</td>
                <td className="small">{new Date(l.expires_at).toLocaleDateString()}</td>
                <td>{l.allow_download ? "yes" : "no"}</td>
                <td>{l.view_count}</td>
                <td>
                  {l.revoked_at ? (
                    <span className="badge neutral">revoked</span>
                  ) : (
                    <form action="/api/share" method="post">
                      <input type="hidden" name="reelId" value={reelId} />
                      <input type="hidden" name="action" value="revoke" />
                      <input type="hidden" name="shareLinkId" value={l.id} />
                      <button type="submit" className="danger">Revoke</button>
                    </form>
                  )}
                </td>
              </tr>
            ))}
            {links.length === 0 && (
              <tr><td colSpan={6} className="muted">No links yet.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}
