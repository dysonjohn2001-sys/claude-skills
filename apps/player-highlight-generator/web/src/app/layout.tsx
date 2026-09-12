import type { Metadata } from "next";

import { currentUser } from "@/lib/auth";

import "./globals.css";

export const metadata: Metadata = {
  title: "Player Highlight Generator",
  description: "Private highlight reels for a youth baseball team.",
  robots: { index: false, follow: false },
};

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const user = await currentUser();
  const isCoach = user && user.role !== "guardian";

  return (
    <html lang="en">
      <body>
        <div className="shell">
          <aside className="sidebar">
            <h1>Player Highlight Generator</h1>
            <p className="tagline">{user ? user.fullName : "Not signed in"}</p>

            {isCoach && (
              <nav>
                <a href="/">Dashboard</a>
                <a href="/games">Games</a>
                <a href="/review">Review queue</a>
                <a href="/players">Players</a>
                <div className="section">Setup</div>
                <a href="/team">Team &amp; branding</a>
                <a href="/team/roster">Roster</a>
                <a href="/team/consent">Consent</a>
                <a href="/team/music">Music</a>
              </nav>
            )}

            {user?.role === "guardian" && (
              <nav>
                <a href="/family">My family&apos;s reels</a>
              </nav>
            )}

            {user && (
              <form action="/api/auth/logout" method="post" style={{ marginTop: 24 }}>
                <button type="submit">Sign out</button>
              </form>
            )}
          </aside>
          <main>{children}</main>
        </div>
      </body>
    </html>
  );
}
