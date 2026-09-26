# Lumbee Tribe of North Carolina / RIVR Tech — TBCP Agreement Package

**PRELIMINARY DRAFT – NO CONTROLLING TBCP AWARD OR SOURCE DOCUMENTS SUPPLIED**
**Provisional baseline: March 2024 amended TBCP Round 2 NOFO**
**Version: Preliminary Draft v0.1 · Version date: September 26, 2026**

> **These drafts are provided for business planning and attorney review. They do not
> constitute legal advice, establish that any federal or Tribal approval has been
> obtained, or supersede the TBCP award, applicable law, or required governmental
> consent.** Every document carries this status and is intentionally seeded with
> review flags and placeholders that must be resolved before execution.

---

## 0. Read this first — posture & the two threshold issues

**No source documents were supplied to this session** — no executed award / CD-450,
no NOFO PDFs (the NTIA and eCFR domains are network-blocked here), no resolutions,
title records, easements, pole agreements, or existing RIVR Tech / LREMC contracts.
Per the assignment, this is therefore a **clearly-labeled preliminary draft** that
uses the **March 2024 amended TBCP Round 2 NOFO as a provisional baseline only**, does
not finalize award-dependent clauses, and **invents no** award number, route, price,
useful life, agency approval, land right, or consent — every such item is a highlighted
placeholder `[■ …]` or `[COUNSEL TO CONFIRM]`.

Two issues gate the whole transaction and are flagged, not resolved, throughout:

1. **Round / award confirmation.** TBCP **Round 3 is the live round** as of the version
   date. The controlling round and the executed award must be confirmed before any
   definitive clause is finalized. Round 2 cost caps / reporting dates are **not**
   carried forward.
2. **Lumbee federal-recognition status** (Lumbee Act of 1956) — the threshold
   TBCP-eligibility question — flagged `[GRANT COMPLIANCE REVIEW REQUIRED]` +
   `[ATTORNEY REVIEW REQUIRED]`.

A third structural determination runs through the package: **contractor vs.
subrecipient** for RIVR Tech under 2 CFR 200.331 (drafted leaning contractor/vendor;
final call reserved for grant counsel).

## 1. The transaction in one paragraph

The **Lumbee Tribe of North Carolina** ("Lumbee Tribe") is the TBCP applicant and, if
funded, the **award recipient, grant steward, and owner** of the **Grant-Funded Assets**.
**LREMC Technologies, LLC d/b/a RIVR Tech** ("RIVR Tech") designs, builds, operates,
and maintains the **Tribal Network** and is the proposed **retail provider of record**,
operating under a long-term **IRU** (20 years from each segment's acceptance, plus two
optional 5-year renewals) and paying the Lumbee Tribe **$[X] per Active Subscriber per
month** (characterization provisional — see below). **Lumbee River EMC ("LREMC")** is a
**separate** entity that owns poles, fiber, easements, huts, power, and land; its assets
are reached only through a **separate consent/joinder**, never assumed owned by RIVR Tech.

## 2. Deliverables (52 documents)

- **00_START_HERE** — `01_Executive_Summary_and_Transaction_Structure`,
  `02_Agreement_Register_and_Signing_Sequence`, this README, and the disclaimer.
- **01_Phase1_Diligence (9)** — source/assumptions register; missing-information request;
  red-flag & approval memo; **contractor-vs-subrecipient (200.331) analysis**;
  procurement & OCI checklist; responsibility + transaction matrix; asset-ownership &
  rights matrix; term sheet & decision register; federal-approval request.
- **02_Definitive_Agreements (10)** — 01 Master (umbrella + **shared definitions
  glossary, Article 2**); 02 DEPC (design/engineering/procurement/construction);
  03 IRU & Network Access; 04 Interconnection/Transport/Shared Facilities; 05 O&M &
  Lifecycle; 06 Retail/Billing/**Subscriber-Revenue** (per-Active-Subscriber schedule);
  07 Grant Finance/Reimbursement/Program-Income/Audit; 08 Land/Easement/ROW/Pole/Facility
  instruments; 09 Data Privacy/Cybersecurity/Continuity; 10 Continuity/Step-In/Transition.
- **03_Governance_Authorizations (7)** — Tribal Council resolution; RIVR Tech
  authorization; **LREMC consent & joinder**; **limited sovereign-immunity waiver
  (bracketed alternatives)**; Tax/TERO/permitting schedule; insurance schedule; SLA schedule.
- **04_Operational_Forms (8)** — construction forms (NTP/change-order/inspection/
  punch-list/acceptance/warranty/completion); segment IRU activation certificate; monthly
  grant-evidence & reimbursement certification; **monthly subscriber reconciliation &
  payment report**; annual budget/refresh/reserve/sustainability; project registers
  (asset/federal-interest/land/software/approvals); incident/outage/RCA/restoration forms;
  program checklists.
- **05_Schedules (S1–S14)** — award/precedence; scope/routes/milestones; asset/federal-
  interest/IRU register; engineering standards/BOM/demarcation; construction pricing;
  operations/SLA/lifecycle; provider-of-record/affordability; subscriber payment/program
  income; land/poles/permits/consents; commercial-capacity/non-project-use; data/cyber/
  supply-chain; insurance/indemnity/liability; default/cure/step-in/transition; required
  approvals.
- **06_Compliance (2)** — **clause-by-clause compliance crosswalk** (requirement →
  controlling authority → where addressed → mandatory/negotiable → status); **closing &
  implementation plan** (every open item with owner, due date, dependency, status).
- **Sources/** — authorities & baseline posture. **Scripts/** — the canonical engine
  (`common.py` — one source of truth for defined terms, deal mechanics, citations,
  precedence, and formatting), the ten generators, and `consistency_check.py`.

## 3. Recommended review order

1. This README → `00_START_HERE/01_Executive_Summary`.
2. `01_Phase1_Diligence` 01–09 (esp. 03 red-flags, 04 contractor/subrecipient, 08 term sheet).
3. `02_Definitive_Agreements/07_Grant_Finance…` and `06_Compliance/01_Crosswalk` (the federal rules that bind everything).
4. `02/01 Master` → `02/03 IRU` → `02/02 DEPC` → `02/04 Interconnection` → `02/05 O&M` → `02/06 Retail/Subscriber` → `02/08 Land` → `02/09 Privacy` → `02/10 Transition`.
5. `03_Governance` (resolutions, LREMC consent, sovereign-immunity alternatives) and `04_Operational_Forms`.
6. `05_Schedules S1–S14`; `06_Compliance/02_Closing_and_Implementation_Plan`.

## 4. Payment characterization (provisional — this is the key economic decision)

Primary model: **$[X] per Active Subscriber per month**, with a precise Active
Subscriber definition (activations/disconnects/suspensions/seasonal/free-subsidized/
partial-months/multi-service/bulk/credits/refunds/taxes/uncollectibles) in the Retail
Agreement (02/06) and Schedule S8. **The label does not control program-income treatment
under 2 CFR 200.307.** Five characterization alternatives are presented (asset-use /
IRU consideration / revenue share / per-subscriber / hybrid), Option D recommended, all
flagged for post-award legal review and a written NTIA determination.

## 5. Major open decisions
See `01_Phase1_Diligence/08_Term_Sheet_and_Decision_Register` and
`06_Compliance/02_Closing_and_Implementation_Plan`. Highlights: controlling round/award;
eligibility; per-subscriber amount **and** characterization; term/renewal; commercial /
non-project capacity limits; reserved fiber; LREMC scope; sovereign-immunity approach;
governing law / forum; affordability tier; data-rights allocation.

## 6. Items requiring attorney review
Sovereign immunity & any limited waiver; governing law; Tribal vs. federal jurisdiction;
arbitration; exhaustion of Tribal remedies; contractor-vs-subrecipient; program income;
procurement; private-benefit; asset encumbrance & Federal Interest; BIA / 25 CFR 162/169
approvals; easements/ROW; tax/TERO; regulatory (FCC/USAC/ETC); customer ownership &
data rights; rate-setting; assignment/change-of-control; default/step-in; grant-clawback;
transition obligations; **Lumbee federal recognition**.

## 7. Items requiring grant / NTIA review
Eligibility; property/Federal-Interest (200.311/.316); equipment records (200.313(d));
procurement (200.317–.327); contractor/subrecipient (200.331); program income (200.307);
BABA + §889 (200.216); NEPA/NHPA; records (200.334); single audit (Subpart F);
disposition; affordability/100-20; **whether the IRU + per-subscriber payment + any
commercial/non-project capacity are permissible** — each needs a written determination
(see `01_Phase1_Diligence/09_Federal_Approval_Request`).

## 8. Updating placeholders & running the checks
Every unresolved item is a yellow `[■ …]` placeholder or one of the four flags
(`[BUSINESS DECISION REQUIRED]`, `[ATTORNEY REVIEW REQUIRED]`,
`[GRANT COMPLIANCE REVIEW REQUIRED]`, `[TECHNICAL INFORMATION REQUIRED]`). Resolve them
directly in Word/Excel, or edit the shared constants in `Scripts/common.py` (`DEAL`,
party names, term, citations) and re-run the relevant `Scripts/gen_*.py` so the change
flows consistently to every document. After any edit run
`python3 Scripts/consistency_check.py` (should report **0 FAIL**; current run:
**11 PASS / 0 WARN / 0 FAIL** across 52 files). In Word, press **Ctrl+A → F9** to
populate each document's Table of Contents and page numbers.

## 9. Order of precedence (verbatim in every agreement)
Award (and incorporated NOFO/SAC/approved application/budget/routes/commitments) →
applicable federal law & 2 CFR Part 200 → approved project documents → Master Agreement →
other Definitive Agreements → Schedules/Exhibits/Forms. **No commercial agreement
authorizes an act prohibited by the Award;** severability/reformation preserve lawful
construction and service provisions if an IRU/exclusivity/payment/commercial-use term is
rejected. Capitalized terms are defined once in Master Article 2 (the shared glossary).

---

*Prepared September 26, 2026 as working drafts. Not legal advice. Confirm every figure,
authority, and bracketed alternative — and the controlling TBCP award — with qualified
counsel and advisors before execution.*
