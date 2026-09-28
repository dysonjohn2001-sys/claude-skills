import sys, os, datetime
sys.path.insert(0, os.path.dirname(__file__))
from docx_helpers import *
from docx.shared import Pt

BASE = "/home/user/claude-skills/deliverables/RIVR-Tech-Lifeline-Lumbee/"
TODAY = datetime.date.today().strftime("%B %d, %Y")

# =====================================================================
# 15 — SAC REQUEST COVER LETTER
# =====================================================================
doc = new_doc()
cover(doc, "SAC Request — Cover Letter to USAC",
    "Study Area Code request for a newly-designated ETC (DRAFT)",
    "15 of series", "Compliance Officer (with Finance)",
    version="v0.1 — DRAFT for internal + counsel review",
    extra=("DRAFT. Verify current USAC submission channel, required attachments, and the correct email "
        "address on usac.org before sending. Bracketed [PLACEHOLDER] fields must be completed."))
h1(doc, "How to use this letter")
para(doc, "This is a draft transmittal to accompany RIVR Tech's Study Area Code (SAC) request to USAC after "
    "NCUC ETC designation. Per current USAC guidance (SR-6.4), a new Lifeline provider obtains its SAC from "
    "USAC by submitting the ETC designation order and supporting documentation to the Lifeline Program. "
    "Confirm the live submission method and attachments on usac.org before sending; complete every "
    "[PLACEHOLDER].")
callout(doc, "Sequence reminder: a SAC is required BEFORE the 498 ID / FCC Form 498. Attach the final NCUC "
    "order. Have your FRN ready; SAM.gov UEI + bank account should already be in progress (the ~6-week long pole).", kind="note")

h1(doc, "Draft letter")
para(doc, TODAY)
para(doc, "")
para(doc, "Universal Service Administrative Company")
para(doc, "Lifeline Program")
para(doc, "Via email: LifelineProgram@usac.org  [CONFIRM current address on usac.org]")
para(doc, "")
para(doc, "Re:  Request for Study Area Code (SAC) — New Lifeline ETC", bold=True)
para(doc, "      LREMC Technologies, LLC d/b/a RIVR Tech")
para(doc, "      NCUC Docket No. [PLACEHOLDER]  ·  FCC Registration Number (FRN): [PLACEHOLDER]")
para(doc, "")
para(doc, "To the Lifeline Program Team:")
para(doc, "LREMC Technologies, LLC d/b/a RIVR Tech (“RIVR Tech”) requests the assignment of a Study "
    "Area Code for its newly-designated Lifeline service area in North Carolina. The North Carolina "
    "Utilities Commission designated RIVR Tech as an Eligible Telecommunications Carrier for the limited "
    "purpose of offering the federal Lifeline benefit by order dated [PLACEHOLDER — ORDER DATE] in Docket "
    "No. [PLACEHOLDER]. A copy of the designation order is enclosed.")
para(doc, "RIVR Tech intends to offer Lifeline-supported broadband internet access service (a symmetrical "
    "fiber offering that meets or exceeds the current Lifeline minimum service standards) to qualifying "
    "low-income consumers within its designated service area. The following information is provided to "
    "support the SAC request:")
table(doc, ["Field", "Value"], [
    ["Legal entity name", "LREMC Technologies, LLC"],
    ["d/b/a", "RIVR Tech"],
    ["Principal address", "6090 NC Hwy 711, Pembroke, NC 28372  [CONFIRM]"],
    ["State of operation", "North Carolina"],
    ["FRN", "[PLACEHOLDER — 10-digit FRN from FCC CORES]"],
    ["SAM.gov UEI", "[PLACEHOLDER — or 'in process']"],
    ["NCUC docket / order date", "[PLACEHOLDER] / [PLACEHOLDER]"],
    ["Designated service area", "As set forth in the enclosed NCUC order [attach map/exchange list if applicable]"],
    ["Supported service", "Lifeline broadband internet access (fixed fiber)"],
    ["Company Officer / contact", "[PLACEHOLDER — name, title, email, phone]"],
    ["Study Area contact", "[PLACEHOLDER — name, title, email, phone]"],
], widths=[2.4, 4.9], small=True)
para(doc, "Please advise if any additional documentation is required to complete the SAC assignment. RIVR "
    "Tech's Company Officer and regulatory contact are available to respond promptly. We appreciate your "
    "assistance and look forward to receiving the assigned Study Area Code so that we may proceed with FCC "
    "Form 498 registration and Lifeline systems onboarding.")
para(doc, "")
para(doc, "Respectfully,")
para(doc, "")
para(doc, "[PLACEHOLDER — Name]", bold=True)
para(doc, "[PLACEHOLDER — Title], LREMC Technologies, LLC d/b/a RIVR Tech")
para(doc, "[PLACEHOLDER — email]  ·  [PLACEHOLDER — phone]")
para(doc, "")
para(doc, "Enclosure: NCUC ETC Designation Order (Docket No. [PLACEHOLDER])", italic=True, size=9, color=GREY)
footer_revhist(doc)
p15 = BASE+"15_SAC_Request_Cover_Letter.docx"
doc.save(p15); Document(p15); print("OK 15")

# =====================================================================
# 16 — PHASE 1 KICKOFF MEMO
# =====================================================================
doc = new_doc()
cover(doc, "Phase 1 Kickoff Memo",
    "ETC approved → USAC onboarding: what happens now",
    "16 of series", "Program Owner (with Executive Sponsor)",
    version="v0.1 — Phase 1 kickoff",
    extra=("Internal kickoff memo issued on NCUC ETC approval. Pair with the Phase 1 Onboarding Tracker "
        "(Deliverable 14) for dated tasks/owners and the Compliance Checklist (07) for evidence."))
toc(doc)

h1(doc, "1. Where we are")
para(doc, "The North Carolina Utilities Commission has designated RIVR Tech as an Eligible "
    "Telecommunications Carrier for Lifeline. That closes Phase 0 (application pending) and opens Phase 1 "
    "(USAC onboarding). This memo states what the approval does and does not authorize, the critical path "
    "to first enrollment, the decisions due now, and the gate before public launch.")
callout(doc, "What approval authorizes: RIVR Tech may complete USAC onboarding and, once onboarded, provide "
    "the STANDARD Lifeline benefit (up to $9.25/mo) to eligible customers in the designated service area, "
    "and publicize its availability (47 C.F.R. §54.405(b)).", kind="ok")
callout(doc, "What approval does NOT authorize: paying the ENHANCED $34.25 Tribal benefit based on Lumbee "
    "membership or four-county residence. Enhanced support requires the customer's principal residence to "
    "be on qualifying “Tribal lands” (47 C.F.R. §54.400(e)), verified per-address via USAC's Tribal "
    "Lands Verification Tool. Until a written USAC/legal determination confirms qualifying Tribal lands "
    "exist in the area, we operate with ZERO enhanced-Tribal subscribers (Open Issue ISS-01).", kind="stop")

h1(doc, "2. Two things to start on Day 1")
numbered(doc, "SAM.gov registration (UEI + active bank account). This can take ~6 weeks and blocks USF "
    "disbursement — it is the critical path. Begin immediately, in parallel with everything else.")
numbered(doc, "The written Tribal-lands determination (ISS-01). Engage regulatory counsel / USAC now so the "
    "enhanced-benefit question is answered on paper before any customer is told about $34.25.")

h1(doc, "3. Critical path to first enrollment (USAC onboarding)")
para(doc, "Do these in order; several run in parallel. Dated targets and owners are in Deliverable 14; "
    "evidence columns are in Deliverable 07. Source: SR-6.")
table(doc, ["Step", "Owner", "Blocks"], [
    ["File final NCUC order; capture service area, effective date, conditions", "Reg. Counsel", "All downstream"],
    ["SAM.gov UEI + bank account (⏱ long pole)", "Finance", "Disbursement"],
    ["FRN via FCC CORES (if not held)", "Finance", "SAM / 498"],
    ["Study Area Code (SAC) from USAC — submit the order", "Compliance", "498 / claims"],
    ["FCC Form 498 → 498 ID; Company Officer certifies", "Finance/Officer", "Reimbursement"],
    ["Assign 497 Officer + ETC Administrator", "Finance/Compliance", "NV/NLAD/LCS setup"],
    ["RAD Rep IDs for all enrollment reps (LifelineRAD.org)", "Compliance", "Enrolling anyone"],
    ["National Verifier access + roles", "Compliance/IT", "Eligibility checks"],
    ["NLAD access + roles", "Compliance/IT", "Enrollment"],
    ["LCS access", "Finance", "Monthly claims"],
], widths=[3.6, 1.9, 1.8], small=True)

h1(doc, "4. Parallel workstreams")
for t in [
    "Pricing & plan: confirm the RIVR price sheet; lock the Senior 100/100 design (recommended Alternative D — $10 net after subsidies).",
    "Tax: obtain the tax-advisor opinion on which components are taxable; no “plus tax” advertising until it is back (broadband access is non-taxable under ITFA).",
    "NISC: build rate/credit codes, tax config, separate-GL accounts (Lifeline / grant / RIVR / Tribe), bill descriptions, and full pass-through; test before the pilot.",
    "Policies: finalize WFA, record-retention (≥3 yrs / duration of service), and privacy/data-security controls (no full SSNs, eligibility docs, or tribal-roll in unsecured fields).",
    "Training: train RAD-registered reps before they enroll anyone; drill the prohibited-statements list.",
    "Comms: finalize website/FAQ/letters/scripts (Deliverable 09) within the guardrails; begin publicizing Lifeline availability.",
    "Lumbee MOU: execute if the Tribe will fund a discount or run privacy-preserving membership verification (Deliverable 11).",
]:
    bullet(doc, t)

h1(doc, "5. Decisions due now")
para(doc, "Formalize these (full table in Deliverable 01 §11; log in Deliverable 13; dated in Deliverable 14):")
table(doc, ["Ref", "Decision", "Recommended", "Owner"], [
    ["ISS-14", "Enhanced Tribal legal determination", "Obtain written USAC/legal determination; assume 0 until confirmed", "Reg. Counsel + USAC"],
    ["ISS-02", "Tax treatment / 'plus tax'", "Tax opinion first; no 'plus tax' until confirmed", "Tax Advisor + CFO"],
    ["ISS-03", "Senior eligibility age", "62", "Exec Sponsor"],
    ["ISS-04", "$10 retail vs net", "NET after subsidies (Alt D)", "Exec Sponsor + CFO"],
    ["ISS-05", "Discount for non-Lifeline seniors", "Yes, capped", "CFO"],
    ["ISS-07", "Equipment & installation", "Waive/fold equipment; free install", "Product + CFO"],
    ["ISS-06", "Lumbee Tribe funding", "Pursue via MOU; base case $0", "Exec Sponsor + Tribe"],
], widths=[0.7, 2.3, 3.0, 1.3], small=True)

h1(doc, "6. Gate before public launch")
para(doc, "No public launch until: (a) all onboarding steps in §3 are complete; (b) a controlled pilot "
    "(≤25–50 existing customers) passes a clean three-way reconciliation (NISC ↔ NLAD ↔ LCS); and "
    "(c) the Executive Readiness Scorecard (Deliverable 12) is green on every gate — including the "
    "Tribal-lands determination. Then set the annual filing calendar: FCC Form 481 (~July 1) and "
    "Form 555 (~Jan 31, + ECFS Docket 14-171).")
callout(doc, "Re-verify current benefit amounts, minimum service standards, and form deadlines against the "
    "live USAC/FCC pages at onboarding — the source register was compiled earlier in 2026.", kind="warn")
footer_revhist(doc)
p16 = BASE+"16_Phase1_Kickoff_Memo.docx"
doc.save(p16); Document(p16); print("OK 16")
