export function timecode(seconds: number): string {
  const total = Math.max(0, Math.floor(seconds));
  const h = Math.floor(total / 3600);
  const m = Math.floor((total % 3600) / 60);
  const s = total % 60;
  const mm = String(m).padStart(h > 0 ? 2 : 1, "0");
  const ss = String(s).padStart(2, "0");
  return h > 0 ? `${h}:${mm}:${ss}` : `${mm}:${ss}`;
}

export function duration(seconds: number): string {
  if (seconds < 60) return `${seconds.toFixed(1)}s`;
  return timecode(seconds);
}

export function confidenceLabel(score: number): {
  label: string;
  tone: "high" | "medium" | "low";
} {
  if (score >= 0.8) return { label: `${Math.round(score * 100)}% confident`, tone: "high" };
  if (score >= 0.6) return { label: `${Math.round(score * 100)}% - check this`, tone: "medium" };
  return { label: `${Math.round(score * 100)}% - likely wrong`, tone: "low" };
}

export const CATEGORY_LABEL: Record<string, string> = {
  offense: "Offense",
  defense: "Defense",
  pitching: "Pitching",
  baserunning: "Baserunning",
};

export function gameLabel(row: { played_on: string | Date; opponent_name: string }): string {
  const date = new Date(row.played_on);
  return `${date.toLocaleDateString(undefined, { month: "short", day: "numeric" })} vs ${row.opponent_name}`;
}

/** Human-readable reasons the matcher was unsure, from `confidence_factors`. */
export function explainConfidence(factors: Record<string, number>): string[] {
  const out: string[] = [];
  if ((factors.name_resolution ?? 1) === 0) out.push("The scorebook name did not match anyone on the roster.");
  else if ((factors.name_resolution ?? 1) < 0.75) out.push("The scorebook name only matched approximately.");
  if ((factors.timeline_precision ?? 1) < 0.5) out.push("The video timing for this play is uncertain.");
  if ((factors.batting_order ?? 1) < 0.3) out.push("This player is not in the expected batting slot.");
  if ((factors.lineup_presence ?? 1) < 0.5) out.push("The lineup does not show this player in the game yet.");
  if ((factors.position_fit ?? 1) < 0.5) out.push("This player is not listed at the position the play implies.");
  if ((factors.jersey_agreement ?? 0) < -0.4) out.push("Jersey numbers read in this clip mostly disagree.");
  return out;
}
