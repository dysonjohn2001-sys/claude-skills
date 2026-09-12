import { NextResponse } from "next/server";

import { requireCoach } from "@/lib/auth";
import { createShareLink, revokeShareLink } from "@/lib/permissions";

export async function POST(request: Request) {
  const user = await requireCoach();
  const form = await request.formData();
  const reelId = String(form.get("reelId") ?? "");
  const action = String(form.get("action") ?? "create");

  const back = (key: "notice" | "error", message: string) =>
    NextResponse.redirect(
      new URL(`/reels/${reelId}/share?${key}=${encodeURIComponent(message)}`, request.url),
      { status: 303 },
    );

  if (action === "revoke") {
    await revokeShareLink(String(form.get("shareLinkId") ?? ""), user.id);
    return back("notice", "That link no longer works for anyone.");
  }

  const guardianIds = form.getAll("guardianIds").map(String).filter(Boolean);
  if (guardianIds.length === 0) {
    return back("error", "Choose at least one family to share with.");
  }

  try {
    const { token } = await createShareLink({
      reelId,
      guardianIds,
      expiresInDays: Math.min(365, Math.max(1, Number(form.get("expiresInDays") ?? 30))),
      allowDownload: form.get("allowDownload") !== null,
      label: String(form.get("label") ?? "") || undefined,
      createdBy: user.id,
    });
    const url = new URL(`/share/${token}`, request.url).toString();
    return back(
      "notice",
      `Link created. Send this to the families you selected: ${url}  (It is shown once and cannot be recovered.)`,
    );
  } catch (error) {
    return back("error", error instanceof Error ? error.message : "Could not create the link.");
  }
}
