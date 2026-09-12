import { requireCoach } from "@/lib/auth";
import { queryOne } from "@/lib/db";

export const dynamic = "force-dynamic";

export default async function TeamSettingsPage() {
  await requireCoach();

  const team = await queryOne<{
    id: string;
    name: string;
    organization: string | null;
    age_group: string | null;
    primary_color: string;
    secondary_color: string;
    logo_key: string | null;
    timezone: string;
    pre_roll_seconds: string;
    post_roll_seconds: string;
    dead_time_removal: boolean;
    auto_approve_threshold: string;
    review_floor_threshold: string;
    jersey_ocr_enabled: boolean;
    music_volume_db: string;
    duck_music_on_action: boolean;
    show_intro_card: boolean;
    show_score_overlay: boolean;
    show_stat_overlay: boolean;
  }>(
    `SELECT t.*, ts.* FROM teams t LEFT JOIN team_settings ts ON ts.team_id = t.id
      ORDER BY t.created_at LIMIT 1`,
  );

  if (!team) {
    return (
      <>
        <h2>Team</h2>
        <div className="notice warn">
          No team exists yet. Run the seed script, or create one from the setup guide.
        </div>
      </>
    );
  }

  return (
    <>
      <h2>Team &amp; branding</h2>
      <p className="subtitle">
        These settings apply to every clip and reel the worker produces from now on. Changing them
        does not re-render reels that already exist.
      </p>

      <form action="/api/team" method="post" encType="multipart/form-data">
        <input type="hidden" name="teamId" value={team.id} />

        <section className="card">
          <h3 style={{ marginTop: 0 }}>Identity</h3>
          <div className="row">
            <div className="field" style={{ flex: "2 1 240px" }}>
              <label htmlFor="name">Team name</label>
              <input id="name" name="name" defaultValue={team.name} required />
            </div>
            <div className="field" style={{ flex: "1 1 160px" }}>
              <label htmlFor="ageGroup">Age group</label>
              <input id="ageGroup" name="ageGroup" defaultValue={team.age_group ?? ""} placeholder="12U" />
            </div>
            <div className="field" style={{ flex: "1 1 200px" }}>
              <label htmlFor="timezone">Timezone</label>
              <input id="timezone" name="timezone" defaultValue={team.timezone} />
            </div>
          </div>
          <div className="row">
            <div className="field" style={{ flex: "0 0 160px" }}>
              <label htmlFor="primaryColor">Primary colour</label>
              <input id="primaryColor" name="primaryColor" type="color" defaultValue={team.primary_color} />
            </div>
            <div className="field" style={{ flex: "0 0 160px" }}>
              <label htmlFor="secondaryColor">Accent colour</label>
              <input id="secondaryColor" name="secondaryColor" type="color" defaultValue={team.secondary_color} />
            </div>
            <div className="field" style={{ flex: "1 1 240px" }}>
              <label htmlFor="logo">Logo (PNG with transparency)</label>
              <input id="logo" name="logo" type="file" accept="image/png,image/svg+xml" />
            </div>
          </div>
          <p className="muted small" style={{ margin: 0 }}>
            The intro card picks black or white text automatically, whichever reads against your
            primary colour.
          </p>
        </section>

        <section className="card">
          <h3 style={{ marginTop: 0 }}>Clip timing</h3>
          <div className="row">
            <div className="field" style={{ flex: "0 0 170px" }}>
              <label htmlFor="preRoll">Seconds before the play</label>
              <input id="preRoll" name="preRoll" type="number" min={0} max={30} step={0.5}
                     defaultValue={Number(team.pre_roll_seconds)} />
            </div>
            <div className="field" style={{ flex: "0 0 170px" }}>
              <label htmlFor="postRoll">Seconds after the play</label>
              <input id="postRoll" name="postRoll" type="number" min={0} max={60} step={0.5}
                     defaultValue={Number(team.post_roll_seconds)} />
            </div>
            <div className="field" style={{ flex: "1 1 240px" }}>
              <label>
                <input type="checkbox" name="deadTimeRemoval" defaultChecked={team.dead_time_removal}
                       style={{ width: "auto", marginRight: 8 }} />
                Trim dead time inside each clip
              </label>
            </div>
          </div>
          <p className="muted small" style={{ margin: 0 }}>
            Defaults are 5 seconds before and 8 seconds after, which covers the wind-up and the throw
            to first. Dead-time trimming never cuts a clip below 4 seconds.
          </p>
        </section>

        <section className="card">
          <h3 style={{ marginTop: 0 }}>Matching thresholds</h3>
          <div className="row">
            <div className="field" style={{ flex: "0 0 200px" }}>
              <label htmlFor="autoApprove">Auto-approve at or above</label>
              <input id="autoApprove" name="autoApprove" type="number" min={0.5} max={1} step={0.01}
                     defaultValue={Number(team.auto_approve_threshold)} />
            </div>
            <div className="field" style={{ flex: "0 0 200px" }}>
              <label htmlFor="reviewFloor">Discard below</label>
              <input id="reviewFloor" name="reviewFloor" type="number" min={0} max={0.8} step={0.01}
                     defaultValue={Number(team.review_floor_threshold)} />
            </div>
            <div className="field" style={{ flex: "1 1 260px" }}>
              <label>
                <input type="checkbox" name="jerseyOcr" defaultChecked={team.jersey_ocr_enabled}
                       style={{ width: "auto", marginRight: 8 }} />
                Use jersey-number recognition as a tiebreaker
              </label>
            </div>
          </div>
          <p className="muted small" style={{ margin: 0 }}>
            Anything between these two numbers lands in your review queue. Jersey recognition only
            runs on those middling cases, and can move a score by at most 0.18 in either direction.
            No facial recognition is used anywhere in this application.
          </p>
        </section>

        <section className="card">
          <h3 style={{ marginTop: 0 }}>Reel presentation</h3>
          <div className="row">
            <label style={{ flex: "1 1 200px" }}>
              <input type="checkbox" name="showIntroCard" defaultChecked={team.show_intro_card}
                     style={{ width: "auto", marginRight: 8 }} />
              Player introduction card
            </label>
            <label style={{ flex: "1 1 200px" }}>
              <input type="checkbox" name="showScoreOverlay" defaultChecked={team.show_score_overlay}
                     style={{ width: "auto", marginRight: 8 }} />
              Score and inning overlay
            </label>
            <label style={{ flex: "1 1 200px" }}>
              <input type="checkbox" name="showStatOverlay" defaultChecked={team.show_stat_overlay}
                     style={{ width: "auto", marginRight: 8 }} />
              Statistics lower-third
            </label>
          </div>
          <div className="row">
            <div className="field" style={{ flex: "0 0 200px" }}>
              <label htmlFor="musicVolume">Music volume (dB)</label>
              <input id="musicVolume" name="musicVolume" type="number" min={-40} max={0} step={1}
                     defaultValue={Number(team.music_volume_db)} />
            </div>
            <label style={{ flex: "1 1 260px" }}>
              <input type="checkbox" name="duckMusic" defaultChecked={team.duck_music_on_action}
                     style={{ width: "auto", marginRight: 8 }} />
              Duck the music under crowd and bat noise
            </label>
          </div>
        </section>

        <button type="submit" className="primary">Save settings</button>
      </form>
    </>
  );
}
