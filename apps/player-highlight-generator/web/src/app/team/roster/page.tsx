import { requireCoach } from "@/lib/auth";
import { query, queryOne } from "@/lib/db";

export const dynamic = "force-dynamic";

export default async function RosterPage({
  searchParams,
}: {
  searchParams: Promise<{ imported?: string; error?: string }>;
}) {
  await requireCoach();
  const params = await searchParams;

  const team = await queryOne<{ id: string; name: string }>(
    "SELECT id, name FROM teams ORDER BY created_at LIMIT 1",
  );

  const players = await query<{
    id: string;
    name: string;
    jersey_number: string | null;
    positions: string[];
    bats: string | null;
    throws: string | null;
    guardian_count: number;
  }>(`
    SELECT p.id, p.first_name || ' ' || p.last_name AS name, p.jersey_number,
           COALESCE(array_agg(DISTINCT pp.position) FILTER (WHERE pp.position IS NOT NULL), '{}') AS positions,
           p.bats, p.throws,
           count(DISTINCT pg.guardian_id)::int AS guardian_count
      FROM players p
 LEFT JOIN player_positions pp ON pp.player_id = p.id
 LEFT JOIN player_guardians pg ON pg.player_id = p.id
     WHERE p.is_active
  GROUP BY p.id
  ORDER BY p.last_name, p.first_name
  `);

  return (
    <>
      <h2>Roster</h2>
      <p className="subtitle">
        Accurate names and jersey numbers are what makes matching work. A duplicate jersey number is
        rejected at import, because two players sharing #7 breaks every number-based check.
      </p>

      {params.imported && <div className="notice">{params.imported}</div>}
      {params.error && <div className="notice error">{params.error}</div>}

      <section className="card">
        <h3 style={{ marginTop: 0 }}>Import a roster CSV</h3>
        <p className="small muted">
          Accepted columns: a single <span className="mono">name</span> column (either{" "}
          <span className="mono">First Last</span> or <span className="mono">Last, First</span>) or
          separate <span className="mono">first_name</span> and <span className="mono">last_name</span>;
          plus any of <span className="mono">number</span>, <span className="mono">position</span>,{" "}
          <span className="mono">bats</span>, <span className="mono">throws</span>,{" "}
          <span className="mono">batting order</span>, <span className="mono">parent name</span>,{" "}
          <span className="mono">parent email</span>, <span className="mono">parent phone</span>.
        </p>
        <form action="/api/imports/roster" method="post" encType="multipart/form-data">
          <input type="hidden" name="teamId" value={team?.id ?? ""} />
          <div className="row">
            <div className="field" style={{ flex: "1 1 280px" }}>
              <label htmlFor="rosterFile">Roster CSV</label>
              <input id="rosterFile" name="file" type="file" accept=".csv,text/csv" required />
            </div>
            <div className="field">
              <label>
                <input type="checkbox" name="dryRun" defaultChecked style={{ width: "auto", marginRight: 8 }} />
                Preview only
              </label>
            </div>
            <div className="field">
              <button type="submit" className="primary">Import</button>
            </div>
          </div>
        </form>
      </section>

      <div className="card" style={{ padding: 0 }}>
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th>Player</th>
              <th>Positions</th>
              <th>B/T</th>
              <th>Guardians</th>
            </tr>
          </thead>
          <tbody>
            {players.map((p) => (
              <tr key={p.id}>
                <td className="mono">{p.jersey_number ?? "-"}</td>
                <td><a href={`/players/${p.id}`}>{p.name}</a></td>
                <td className="small muted">{p.positions.join(", ") || "-"}</td>
                <td className="small muted">
                  {p.bats ?? "-"}/{p.throws ?? "-"}
                </td>
                <td>
                  {p.guardian_count === 0 ? (
                    <span className="badge low">none on file</span>
                  ) : (
                    p.guardian_count
                  )}
                </td>
              </tr>
            ))}
            {players.length === 0 && (
              <tr><td colSpan={5} className="muted">No players yet.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}
