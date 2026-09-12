export const dynamic = "force-dynamic";

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ error?: string; next?: string }>;
}) {
  const params = await searchParams;

  return (
    <div style={{ maxWidth: 380, margin: "8vh auto" }}>
      <h2>Sign in</h2>
      <p className="subtitle">
        This application is private to one team. Accounts are created by the coach.
      </p>

      {params.error && <div className="notice error">{params.error}</div>}

      <form action="/api/auth/login" method="post" className="card">
        <input type="hidden" name="next" value={params.next ?? "/"} />
        <div className="field">
          <label htmlFor="email">Email</label>
          <input id="email" name="email" type="email" autoComplete="email" required />
        </div>
        <div className="field">
          <label htmlFor="password">Password</label>
          <input id="password" name="password" type="password" autoComplete="current-password" required />
        </div>
        <button type="submit" className="primary" style={{ width: "100%" }}>
          Sign in
        </button>
      </form>

      <p className="small muted">
        Parents: use the email address your coach invited. Your sign-in only shows reels for your own
        child.
      </p>
    </div>
  );
}
