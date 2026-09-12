import { headers } from "next/headers";

import { currentUser } from "@/lib/auth";
import { recordShareView, resolveShare } from "@/lib/permissions";

export const dynamic = "force-dynamic";

export default async function SharePage({ params }: { params: Promise<{ token: string }> }) {
  const { token } = await params;
  const user = await currentUser();
  const { share, reason } = await resolveShare(token, user?.id ?? null);

  if (!share) {
    return (
      <div style={{ maxWidth: 480, margin: "10vh auto" }}>
        <h2>This reel is not available</h2>
        <p className="subtitle">{reason}</p>
        {!user && (
          <p>
            <a className="btn primary" href={`/login?next=/share/${token}`}>Sign in</a>
          </p>
        )}
      </div>
    );
  }

  const headerList = await headers();
  await recordShareView(
    share.shareLinkId,
    user?.id ?? null,
    headerList.get("x-forwarded-for") ?? undefined,
    headerList.get("user-agent") ?? undefined,
  );

  return (
    <div style={{ maxWidth: 900, margin: "4vh auto" }}>
      <h2>{share.title}</h2>
      <p className="subtitle">{share.playerName}</p>
      <video controls autoPlay preload="metadata" src={`/api/media/${encodeURI(share.outputKey!)}`} />
      <p className="small muted" style={{ marginTop: 12 }}>
        {share.allowDownload ? (
          <a href={`/api/media/${encodeURI(share.outputKey!)}?download=1`}>Download MP4</a>
        ) : (
          "Downloading is turned off for this link."
        )}
        {" · "}
        This link was shared with your account specifically. Forwarding it does not grant access to
        anyone else.
      </p>
    </div>
  );
}
