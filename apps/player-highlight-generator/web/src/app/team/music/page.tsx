import { requireCoach } from "@/lib/auth";
import { query, queryOne } from "@/lib/db";
import { duration } from "@/lib/format";

export const dynamic = "force-dynamic";

export default async function MusicPage({
  searchParams,
}: {
  searchParams: Promise<{ notice?: string; error?: string }>;
}) {
  await requireCoach();
  const flash = await searchParams;

  const team = await queryOne<{ id: string }>("SELECT id FROM teams ORDER BY created_at LIMIT 1");
  const tracks = await query<{
    id: string;
    title: string;
    artist: string | null;
    license: string;
    duration_seconds: string | null;
    is_default: boolean;
  }>("SELECT * FROM music_tracks ORDER BY is_default DESC, title");

  return (
    <>
      <h2>Background music</h2>
      <p className="subtitle">
        Music is mixed under the clip audio and ducked when there is crowd or bat noise, so the reel
        still sounds like a ballgame rather than a commercial.
      </p>

      {flash.notice && <div className="notice">{flash.notice}</div>}
      {flash.error && <div className="notice error">{flash.error}</div>}

      <div className="notice warn">
        Upload only music you have the right to use. Commercial tracks will get a reel muted or taken
        down the moment a parent reposts it, and the licence you record here is what you will be
        asked for if that happens.
      </div>

      <form action="/api/music" method="post" encType="multipart/form-data" className="card">
        <input type="hidden" name="teamId" value={team?.id ?? ""} />
        <div className="row">
          <div className="field" style={{ flex: "1 1 220px" }}>
            <label htmlFor="title">Track title</label>
            <input id="title" name="title" required />
          </div>
          <div className="field" style={{ flex: "1 1 180px" }}>
            <label htmlFor="artist">Artist</label>
            <input id="artist" name="artist" />
          </div>
          <div className="field" style={{ flex: "1 1 200px" }}>
            <label htmlFor="license">Licence</label>
            <input id="license" name="license" placeholder="CC0 / Epidemic Sound #12345" required />
          </div>
        </div>
        <div className="row">
          <div className="field" style={{ flex: "1 1 260px" }}>
            <label htmlFor="audio">Audio file (MP3, M4A, WAV)</label>
            <input id="audio" name="file" type="file" accept="audio/*" required />
          </div>
          <div className="field">
            <label>
              <input type="checkbox" name="isDefault" style={{ width: "auto", marginRight: 8 }} />
              Use as the team default
            </label>
          </div>
          <div className="field">
            <button type="submit" className="primary">Add track</button>
          </div>
        </div>
      </form>

      <div className="card" style={{ padding: 0 }}>
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Artist</th>
              <th>Licence</th>
              <th>Length</th>
              <th>Default</th>
            </tr>
          </thead>
          <tbody>
            {tracks.map((t) => (
              <tr key={t.id}>
                <td>{t.title}</td>
                <td className="muted small">{t.artist ?? "-"}</td>
                <td className="mono small">{t.license}</td>
                <td>{t.duration_seconds ? duration(Number(t.duration_seconds)) : "-"}</td>
                <td>{t.is_default ? <span className="badge high">default</span> : ""}</td>
              </tr>
            ))}
            {tracks.length === 0 && (
              <tr><td colSpan={5} className="muted">No tracks yet. Reels render with clip audio only.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </>
  );
}
