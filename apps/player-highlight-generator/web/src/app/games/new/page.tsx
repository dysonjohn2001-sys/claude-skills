import { requireCoach } from "@/lib/auth";
import { query } from "@/lib/db";

export const dynamic = "force-dynamic";

export default async function NewGamePage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string }>;
}) {
  await requireCoach();
  const params = await searchParams;

  const seasons = await query<{ id: string; name: string; team_name: string }>(
    `SELECT s.id, s.name, t.name AS team_name
       FROM seasons s JOIN teams t ON t.id = s.team_id
      WHERE s.is_active ORDER BY s.starts_on DESC`,
  );
  const tournaments = await query<{ id: string; name: string; season_id: string }>(
    "SELECT id, name, season_id FROM tournaments ORDER BY starts_on DESC",
  );

  return (
    <>
      <h2>Add a game</h2>
      <p className="subtitle">
        The date, opponent and first-pitch time are what let the matcher line plays up with footage.
      </p>

      {params.error && <div className="notice error">{params.error}</div>}

      <form action="/api/games/new" method="post" className="card">
        <div className="row">
          <div className="field" style={{ flex: "1 1 220px" }}>
            <label htmlFor="seasonId">Season</label>
            <select id="seasonId" name="seasonId" required>
              {seasons.map((s) => (
                <option key={s.id} value={s.id}>{s.team_name} — {s.name}</option>
              ))}
            </select>
          </div>
          <div className="field" style={{ flex: "1 1 220px" }}>
            <label htmlFor="tournamentId">Tournament (optional)</label>
            <select id="tournamentId" name="tournamentId" defaultValue="">
              <option value="">Regular season game</option>
              {tournaments.map((t) => (
                <option key={t.id} value={t.id}>{t.name}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="row">
          <div className="field" style={{ flex: "0 0 180px" }}>
            <label htmlFor="playedOn">Date</label>
            <input id="playedOn" name="playedOn" type="date" required />
          </div>
          <div className="field" style={{ flex: "0 0 220px" }}>
            <label htmlFor="firstPitchAt">First pitch</label>
            <input id="firstPitchAt" name="firstPitchAt" type="datetime-local" />
          </div>
          <div className="field" style={{ flex: "1 1 220px" }}>
            <label htmlFor="opponentName">Opponent</label>
            <input id="opponentName" name="opponentName" required />
          </div>
          <div className="field" style={{ flex: "0 0 140px" }}>
            <label htmlFor="homeAway">Home or away</label>
            <select id="homeAway" name="homeAway" defaultValue="home">
              <option value="home">Home</option>
              <option value="away">Away</option>
              <option value="neutral">Neutral site</option>
            </select>
          </div>
        </div>

        <div className="field">
          <label htmlFor="location">Location</label>
          <input id="location" name="location" placeholder="Riverside Complex, Field 3" />
        </div>

        <p className="muted small">
          First pitch is optional but worth entering. Without any timestamps in the play-by-play file,
          it is the only thing that lets the matcher pace plays through the recording.
        </p>

        <button type="submit" className="primary">Create game</button>
      </form>
    </>
  );
}
