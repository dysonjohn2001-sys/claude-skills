import { readFileSync } from "node:fs";
import path from "node:path";

/**
 * CSV import for roster and play-by-play files.
 *
 * Header aliases come from shared/column-aliases.json, the same file the Python
 * importer reads, so the two cannot disagree about what a column means. It is
 * loaded from disk rather than imported as a module because it sits outside the
 * Next.js project root.
 */

interface AliasFile {
  roster: Record<string, string[]>;
  play_by_play: Record<string, string[]>;
}

const ALIAS_PATH =
  process.env.PHG_COLUMN_ALIASES ??
  path.resolve(process.cwd(), "..", "shared", "column-aliases.json");

let aliasCache: AliasFile | null = null;

function aliases(): AliasFile {
  if (!aliasCache) {
    aliasCache = JSON.parse(readFileSync(ALIAS_PATH, "utf-8")) as AliasFile;
  }
  return aliasCache;
}

export interface Issue {
  row: number;
  message: string;
}

// ---------------------------------------------------------------------------
// CSV reader
// ---------------------------------------------------------------------------

/** RFC 4180 reader: handles quoted fields, embedded commas, doubled quotes, CRLF. */
export function parseCsv(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let field = "";
  let quoted = false;

  const content = text.charCodeAt(0) === 0xfeff ? text.slice(1) : text;

  for (let i = 0; i < content.length; i += 1) {
    const ch = content[i];
    if (quoted) {
      if (ch === '"') {
        if (content[i + 1] === '"') {
          field += '"';
          i += 1;
        } else {
          quoted = false;
        }
      } else {
        field += ch;
      }
      continue;
    }
    if (ch === '"') quoted = true;
    else if (ch === ",") {
      row.push(field);
      field = "";
    } else if (ch === "\n") {
      row.push(field);
      rows.push(row);
      row = [];
      field = "";
    } else if (ch !== "\r") {
      field += ch;
    }
  }
  if (field.length || row.length) {
    row.push(field);
    rows.push(row);
  }
  return rows.filter((r) => r.some((cell) => cell.trim() !== ""));
}

export function normalizeHeader(header: string): string {
  return header
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "_")
    .replace(/^_+|_+$/g, "");
}

export function buildColumnMap(
  headers: string[],
  table: Record<string, string[]>,
): { map: Record<string, number>; unmatched: string[] } {
  const normalized = headers.map(normalizeHeader);
  const map: Record<string, number> = {};
  const claimed = new Set<number>();

  for (const [field, options] of Object.entries(table)) {
    for (const option of options) {
      const index = normalized.indexOf(option);
      if (index >= 0 && !claimed.has(index)) {
        map[field] = index;
        claimed.add(index);
        break;
      }
    }
  }
  const unmatched = headers.filter((_, i) => !claimed.has(i));
  return { map, unmatched };
}

// ---------------------------------------------------------------------------
// Roster
// ---------------------------------------------------------------------------

export interface GuardianRow {
  fullName: string;
  email: string;
  phone: string | null;
}

export interface RosterPlayer {
  firstName: string;
  lastName: string;
  jerseyNumber: string | null;
  positions: string[];
  bats: string | null;
  throws: string | null;
  birthYear: number | null;
  battingOrder: number | null;
  guardians: GuardianRow[];
  sourceRow: number;
}

export interface RosterResult {
  players: RosterPlayer[];
  errors: Issue[];
  warnings: Issue[];
  columnMap: Record<string, number>;
  unmatchedHeaders: string[];
}

const VALID_POSITIONS = new Set([
  "P", "C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "DH", "EH", "UTIL",
]);

function splitName(full: string): [string, string] {
  const trimmed = full.trim();
  if (trimmed.includes(",")) {
    const [last, ...rest] = trimmed.split(",");
    return [rest.join(",").trim(), last.trim()];
  }
  const parts = trimmed.split(/\s+/);
  if (parts.length === 1) return [parts[0], ""];
  return [parts.slice(0, -1).join(" "), parts[parts.length - 1]];
}

export function parseRosterCsv(text: string): RosterResult {
  const rows = parseCsv(text);
  const errors: Issue[] = [];
  const warnings: Issue[] = [];

  if (rows.length < 2) {
    return { players: [], errors: [{ row: 0, message: "file has no data rows" }], warnings, columnMap: {}, unmatchedHeaders: [] };
  }

  const [headers, ...body] = rows;
  const { map, unmatched } = buildColumnMap(headers, aliases().roster);

  const hasName =
    map.full_name !== undefined ||
    (map.first_name !== undefined && map.last_name !== undefined);
  if (!hasName) {
    errors.push({
      row: 0,
      message: "no name column found; expected 'name' or 'first_name' + 'last_name'",
    });
    return { players: [], errors, warnings, columnMap: map, unmatchedHeaders: unmatched };
  }

  const players: RosterPlayer[] = [];
  const seenJerseys = new Map<string, number>();

  body.forEach((row, index) => {
    const lineNo = index + 2;
    const get = (field: string) =>
      map[field] !== undefined ? (row[map[field]] ?? "").trim() : "";

    let firstName: string;
    let lastName: string;
    if (map.first_name !== undefined && map.last_name !== undefined) {
      firstName = get("first_name");
      lastName = get("last_name");
    } else {
      [firstName, lastName] = splitName(get("full_name"));
    }
    if (!firstName && !lastName) return;
    if (!lastName) {
      warnings.push({ row: lineNo, message: `'${firstName}' has no last name; matching will be weaker` });
    }

    let jerseyNumber: string | null = get("jersey_number").replace(/^#/, "").trim() || null;
    if (jerseyNumber) {
      if (!/^\d+$/.test(jerseyNumber)) {
        warnings.push({ row: lineNo, message: `jersey '${jerseyNumber}' is not numeric; kept as text` });
      } else if (seenJerseys.has(jerseyNumber)) {
        errors.push({
          row: lineNo,
          message: `jersey #${jerseyNumber} is already used on row ${seenJerseys.get(jerseyNumber)}`,
        });
      } else {
        seenJerseys.set(jerseyNumber, lineNo);
      }
    }

    const positions: string[] = [];
    for (const token of get("positions").split(/[,;/]/)) {
      const value = token.trim().toUpperCase();
      if (!value) continue;
      if (VALID_POSITIONS.has(value)) positions.push(value);
      else warnings.push({ row: lineNo, message: `unrecognised position '${value}' ignored` });
    }

    const batsRaw = get("bats").toUpperCase().slice(0, 1);
    const throwsRaw = get("throws").toUpperCase().slice(0, 1);
    const bats = ["L", "R", "S"].includes(batsRaw) ? batsRaw : null;
    const throwsHand = ["L", "R"].includes(throwsRaw) ? throwsRaw : null;

    const guardians: GuardianRow[] = [];
    const email = get("guardian_email");
    if (email) {
      guardians.push({
        fullName: get("guardian_name") || `${firstName} ${lastName} guardian`,
        email,
        phone: get("guardian_phone") || null,
      });
    }

    players.push({
      firstName,
      lastName,
      jerseyNumber,
      positions,
      bats,
      throws: throwsHand,
      birthYear: /^\d{4}$/.test(get("birth_year")) ? Number(get("birth_year")) : null,
      battingOrder: /^\d+$/.test(get("batting_order")) ? Number(get("batting_order")) : null,
      guardians,
      sourceRow: lineNo,
    });
  });

  if (players.length === 0) errors.push({ row: 0, message: "file contained no player rows" });
  return { players, errors, warnings, columnMap: map, unmatchedHeaders: unmatched };
}

// ---------------------------------------------------------------------------
// Play-by-play
// ---------------------------------------------------------------------------

export interface PlayRowParsed {
  sequenceNo: number;
  inning: number;
  half: "top" | "bottom";
  playType: string;
  description: string;
  isOurOffense: boolean;
  occurredAt: Date | null;
  result: string | null;
  batter: string | null;
  pitcher: string | null;
  runners: string[];
  putoutBy: string[];
  assistBy: string[];
  errorBy: string[];
  battingOrder: number | null;
  rbi: number;
  runsScored: number;
  outsBefore: number | null;
  balls: number | null;
  strikes: number | null;
  scoreUs: number | null;
  scoreThem: number | null;
  leverageTag: string | null;
  inferredPlayType: boolean;
  sourceRow: number;
  raw: Record<string, string>;
}

export interface PlayResult {
  plays: PlayRowParsed[];
  errors: Issue[];
  warnings: Issue[];
  columnMap: Record<string, number>;
  unmatchedHeaders: string[];
  needsSideMapping: boolean;
}

// Ordered: the first pattern to match wins, so a double play is not read as a
// double. Mirrors the list in worker/phg/importers/playbyplay_csv.py.
const PLAY_PATTERNS: [string, RegExp][] = [
  ["triple_play", /\btriple play\b|\bTP\b/i],
  ["double_play", /\bdouble play\b|\bDP\b/i],
  ["home_run", /\bhome ?runs?\b|\bHR\b|\bgrand slam\b|\bhomers?\b/i],
  ["triple", /\btriples?\b|\b3B\b/i],
  ["double", /\bdoubles?\b|\bground ?rule doubles?\b|\b2B\b/i],
  ["single", /\bsingles?\b|\b1B\b|\bbase hit\b/i],
  ["strikeout", /\bstrikes? out\b|\bstrikeout\b|\bstruck out\b|\bK\b|\bSO\b/],
  ["walk", /\bwalks?\b|\bwalked\b|\bbase on balls\b|\bBB\b/i],
  ["hit_by_pitch", /\bhit by pitch\b|\bHBP\b/i],
  ["sacrifice_fly", /\bsac(rifice)? fly\b|\bSF\b/i],
  ["sacrifice_bunt", /\bsac(rifice)? bunt\b|\bSAC\b/i],
  ["stolen_base", /\bstolen base\b|\bsteals?\b|\bSB\b/i],
  ["caught_stealing", /\bcaught stealing\b|\bCS\b/i],
  ["picked_off", /\bpicked off\b|\bpickoff\b/i],
  ["wild_pitch", /\bwild pitch\b|\bWP\b/i],
  ["balk", /\bbalk\b/i],
  ["fielders_choice", /\bfielder'?s choice\b|\bFC\b/i],
  ["error_reached", /\breach(es|ed)? on (an )?error\b|\bROE\b/i],
  ["groundout", /\bground(s|ed)? out\b|\bgroundout\b|\bgrounder to\b/i],
  ["flyout", /\bfl(y|ies|ied) out\b|\bflyout\b|\bfly ball to\b/i],
  ["lineout", /\bline(s|d)? out\b|\blineout\b|\bliner to\b/i],
  ["popout", /\bpop(s|ped)? out\b|\bpopout\b|\bpop fly\b/i],
];

export function classifyPlay(description: string, result?: string | null): [string, boolean] {
  const explicit = (result ?? "").trim().toLowerCase().replace(/[\s-]+/g, "_");
  if (explicit && PLAY_PATTERNS.some(([name]) => name === explicit)) return [explicit, false];
  const text = `${description} ${result ?? ""}`;
  for (const [name, pattern] of PLAY_PATTERNS) {
    if (pattern.test(text)) return [name, true];
  }
  return ["other", true];
}

function splitNames(raw: string): string[] {
  return raw
    .split(/[;,/|]/)
    .map((s) => s.trim())
    .filter(Boolean);
}

function toInt(raw: string, fallback: number | null = null): number | null {
  return /^-?\d+$/.test(raw.trim()) ? Number(raw.trim()) : fallback;
}

export function parsePlayByPlayCsv(
  text: string,
  options: { ourTeamName?: string | null; weBatIn?: "top" | "bottom" | null } = {},
): PlayResult {
  const rows = parseCsv(text);
  const errors: Issue[] = [];
  const warnings: Issue[] = [];

  if (rows.length < 2) {
    return {
      plays: [], errors: [{ row: 0, message: "file has no data rows" }], warnings,
      columnMap: {}, unmatchedHeaders: [], needsSideMapping: false,
    };
  }

  const [headers, ...body] = rows;
  const { map, unmatched } = buildColumnMap(headers, aliases().play_by_play);

  if (map.inning === undefined) errors.push({ row: 0, message: "no inning column found" });
  if (map.description === undefined && map.play_type === undefined && map.result === undefined) {
    errors.push({
      row: 0,
      message: "file has no description, play_type or result column to read plays from",
    });
  }
  if (errors.length) {
    return { plays: [], errors, warnings, columnMap: map, unmatchedHeaders: unmatched, needsSideMapping: false };
  }

  const hasTeamColumn = map.team !== undefined;
  const needsSideMapping =
    !hasTeamColumn && options.weBatIn !== "top" && options.weBatIn !== "bottom";

  const plays: PlayRowParsed[] = [];
  let lastHalf: "top" | "bottom" = "top";

  body.forEach((row, index) => {
    const lineNo = index + 2;
    const get = (field: string) =>
      map[field] !== undefined ? (row[map[field]] ?? "").trim() : "";

    const inning = toInt(get("inning"));
    if (inning === null) {
      warnings.push({ row: lineNo, message: "row has no inning; skipped" });
      return;
    }

    const halfRaw = get("half").toLowerCase();
    const half: "top" | "bottom" = halfRaw.startsWith("t") || halfRaw.startsWith("^")
      ? "top"
      : halfRaw.startsWith("b") || halfRaw.startsWith("v")
        ? "bottom"
        : lastHalf;
    lastHalf = half;

    const description = get("description") || get("result") || get("play_type");
    if (!description) {
      warnings.push({ row: lineNo, message: "row has no play text; skipped" });
      return;
    }

    const explicitType = get("play_type").trim().toLowerCase().replace(/\s+/g, "_");
    const [playType, inferred] = explicitType
      ? [explicitType, false]
      : classifyPlay(description, get("result") || null);

    let isOurOffense: boolean;
    if (hasTeamColumn && options.ourTeamName) {
      isOurOffense = get("team").toLowerCase() === options.ourTeamName.trim().toLowerCase();
    } else if (options.weBatIn === "top" || options.weBatIn === "bottom") {
      isOurOffense = half === options.weBatIn;
    } else {
      isOurOffense = half === "top";
    }

    let occurredAt: Date | null = null;
    const rawTime = get("occurred_at");
    if (rawTime) {
      const parsed = new Date(rawTime);
      if (Number.isNaN(parsed.getTime())) {
        warnings.push({ row: lineNo, message: `could not read timestamp '${rawTime}'` });
      } else {
        occurredAt = parsed;
      }
    }

    let putoutBy = splitNames(get("putout_by"));
    if (putoutBy.length === 0 && !isOurOffense) {
      const hit = /\bto (?:the )?([A-Z][a-zA-Z'-]+(?: [A-Z][a-zA-Z'-]+)?)/.exec(description);
      if (hit) putoutBy = [hit[1]];
    }

    const scoreUs = toInt(get("score_us"));
    const scoreThem = toInt(get("score_them"));
    let leverageTag: string | null = null;
    if (scoreUs !== null && scoreThem !== null && Math.abs(scoreUs - scoreThem) <= 1) {
      leverageTag = inning >= 5 ? "tying_run" : "risp";
    }

    const raw: Record<string, string> = {};
    headers.forEach((h, i) => (raw[h] = row[i] ?? ""));

    plays.push({
      sequenceNo: toInt(get("sequence_no"), plays.length + 1)!,
      inning,
      half,
      playType,
      description,
      isOurOffense,
      occurredAt,
      result: get("result") || null,
      batter: get("batter") || null,
      pitcher: get("pitcher") || null,
      runners: splitNames(get("runners")),
      putoutBy,
      assistBy: splitNames(get("assist_by")),
      errorBy: splitNames(get("error_by")),
      battingOrder: toInt(get("batting_order")),
      rbi: toInt(get("rbi"), 0)!,
      runsScored: toInt(get("runs_scored"), 0)!,
      outsBefore: toInt(get("outs_before")),
      balls: toInt(get("balls")),
      strikes: toInt(get("strikes")),
      scoreUs,
      scoreThem,
      leverageTag,
      inferredPlayType: inferred,
      sourceRow: lineNo,
      raw,
    });
  });

  if (plays.length === 0) errors.push({ row: 0, message: "file contained no readable plays" });

  const inferredCount = plays.filter((p) => p.inferredPlayType).length;
  if (inferredCount) {
    warnings.push({
      row: 0,
      message: `${inferredCount} of ${plays.length} play types were inferred from text`,
    });
  }
  if (!plays.some((p) => p.occurredAt)) {
    warnings.push({ row: 0, message: "no timestamps in this file; plays will be paced from first pitch" });
  }

  return { plays, errors, warnings, columnMap: map, unmatchedHeaders: unmatched, needsSideMapping };
}
