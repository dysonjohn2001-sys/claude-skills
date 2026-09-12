import { requireCoach } from "@/lib/auth";
import { query } from "@/lib/db";

export const dynamic = "force-dynamic";

const CONSENT_TYPES = [
  { key: "media_capture", label: "Appears in team video" },
  { key: "highlight_generation", label: "Highlight reels may be built" },
  { key: "family_sharing", label: "Share with own family" },
  { key: "team_sharing", label: "Visible to other team families" },
  { key: "external_sharing", label: "Download / post elsewhere" },
] as const;

/**
 * Consent is the gate on everything else in the application. A player with no
 * highlight_generation consent gets no clips at all, so this page is where a
 * coach finds out why a reel is empty.
 */
export default async function ConsentPage() {
  await requireCoach();

  const players = await query<{
    id: string;
    name: string;
    jersey_number: string | null;
    guardians: { id: string; name: string; email: string }[];
    granted: string[];
  }>(`
    SELECT p.id,
           p.first_name || ' ' || p.last_name AS name,
           p.jersey_number,
           COALESCE(
             json_agg(DISTINCT jsonb_build_object('id', g.id, 'name', g.full_name, 'email', g.email))
               FILTER (WHERE g.id IS NOT NULL), '[]') AS guardians,
           COALESCE(array_agg(DISTINCT ec.type::text) FILTER (WHERE ec.is_active), '{}') AS granted
      FROM players p
 LEFT JOIN player_guardians pg ON pg.player_id = p.id
 LEFT JOIN guardians g         ON g.id = pg.guardian_id
 LEFT JOIN effective_consents ec ON ec.player_id = p.id
     WHERE p.is_active
  GROUP BY p.id
  ORDER BY p.last_name, p.first_name
  `);

  const blocked = players.filter((p) => !p.granted.includes("highlight_generation"));

  return (
    <>
      <h2>Parental consent</h2>
      <p className="subtitle">
        These are minors. Nothing is generated, stored as a reel, or shared without a guardian
        granting it, and every grant and revocation is kept as its own dated record.
      </p>

      {blocked.length > 0 && (
        <div className="notice warn">
          {blocked.length} player{blocked.length === 1 ? " has" : "s have"} no highlight-generation
          consent. The matcher skips them entirely, so they will not appear in any reel and no clips
          are cut for them.
        </div>
      )}

      <div className="card" style={{ padding: 0, overflowX: "auto" }}>
        <table>
          <thead>
            <tr>
              <th>Player</th>
              <th>Guardian</th>
              {CONSENT_TYPES.map((c) => (
                <th key={c.key} style={{ minWidth: 110 }}>{c.label}</th>
              ))}
              <th></th>
            </tr>
          </thead>
          <tbody>
            {players.map((p) => (
              <tr key={p.id}>
                <td>
                  {p.name} {p.jersey_number && <span className="muted mono">#{p.jersey_number}</span>}
                </td>
                <td className="small muted">
                  {p.guardians.length === 0
                    ? <span className="badge low">none on file</span>
                    : p.guardians.map((g) => g.name).join(", ")}
                </td>
                {CONSENT_TYPES.map((c) => (
                  <td key={c.key}>
                    <span className={`badge ${p.granted.includes(c.key) ? "high" : "neutral"}`}>
                      {p.granted.includes(c.key) ? "yes" : "no"}
                    </span>
                  </td>
                ))}
                <td className="small">
                  {p.guardians[0] && (
                    <form action="/api/consent" method="post">
                      <input type="hidden" name="playerId" value={p.id} />
                      <input type="hidden" name="guardianId" value={p.guardians[0].id} />
                      <button type="submit">Record form</button>
                    </form>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h3>How consent is handled</h3>
      <div className="card small">
        <ul style={{ margin: 0, paddingLeft: 18 }}>
          <li>
            Each consent is recorded per player, per purpose, with the guardian who granted it, the
            time, and optionally a scan of the signed form.
          </li>
          <li>
            Revoking is a new dated record rather than an edit, so the history of what was permitted
            when is never overwritten.
          </li>
          <li>
            Revoking <strong>highlight generation</strong> stops new clips immediately. Revoking{" "}
            <strong>family sharing</strong> turns off every existing share link for that player.
          </li>
          <li>
            Only a year of birth is stored, never a full date, and no facial recognition or biometric
            template is created at any point.
          </li>
          <li>
            Share links are always bound to named guardian accounts. There is no public link option
            anywhere in this application.
          </li>
        </ul>
      </div>
    </>
  );
}
