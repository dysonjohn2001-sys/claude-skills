import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from docx_helpers import *

OUT = "/home/user/claude-skills/deliverables/RIVR-Tech-Lifeline-Lumbee/04_Enrollment_and_Deenrollment_SOPs.docx"

doc = new_doc()

cover(
    doc,
    title="Enrollment & De-enrollment SOPs",
    subtitle="Step-by-step operating procedures for the RIVR Tech Lifeline & Lumbee Broadband Affordability Initiative",
    deliverable_no="04 — Enrollment & De-enrollment Standard Operating Procedures",
    owner="Customer Service Manager + Compliance Officer",
    approvers="________________________  (Customer Service Manager)   ________________________  (Compliance Officer)   ____/____/____",
    version="v0.1 — DRAFT (build phase, ETC application pending)",
    extra="These SOPs assume RIVR Tech is a designated ETC with active USAC systems access (NV, NLAD, RAD, LCS). "
          "RIVR Tech is NOT yet a designated ETC (SR-7.4). Do NOT enroll live subscribers until the final NCUC ETC "
          "order issues and USAC onboarding (SAC, 498 ID, NV/NLAD access, Rep IDs) is complete (SR-6). Roles, systems, "
          "and account references below are operational placeholders to be finalized at go-live.",
)

toc(doc)

# ---------------------------------------------------------------------------
# ROLE & SYSTEM LEGEND
# ---------------------------------------------------------------------------
h1(doc, "How to read these SOPs")
para(doc, "Every workflow in this document names WHO performs each step (role), the SYSTEM used, and finishes "
          "with a quality-control (QC) and secure-retention step. The role and system shorthand below is used "
          "throughout.")

h3(doc, "Roles")
table(doc,
      ["Shorthand", "Role", "Primary responsibility"],
      [["ER", "Enrollment Representative", "Front-line intake; must hold a RAD Rep ID (SR-6.6) before enrolling anyone."],
       ["CSR", "Customer Service Rep", "Phone/in-person intake, service orders, notices."],
       ["QC", "QC Reviewer", "Independent second-person review of every completed enrollment before it is claimed."],
       ["CSM", "Customer Service Manager", "Owns the enrollment workflow; escalation point; co-owner of this SOP."],
       ["CO", "Compliance Officer", "Owns NV/NLAD/eligibility integrity, recertification, de-enrollment; co-owner."],
       ["BILL", "Billing Administrator", "Applies/removes the Lifeline credit, sets billing effective dates in NISC."],
       ["TECH", "Field/Provisioning Tech", "Completes service orders / installs on the fiber network."]],
      widths=[1.0, 2.0, 3.8])

h3(doc, "Systems")
table(doc,
      ["System", "What it is", "Rule"],
      [["NV", "USAC National Verifier — eligibility engine", "NV approval is REQUIRED before NLAD enrollment (SR-3.1)."],
       ["NLAD", "National Lifeline Accountability Database", "Enrollment + duplicate check; update within 10 business days of changes (SR-3.2)."],
       ["RAD", "Rep ID registry (LifelineRAD.org)", "Each ER self-registers for a unique Rep ID before enrolling (SR-6.6)."],
       ["LCS", "Lifeline Claims System", "Monthly reimbursement claim built from the 1st-of-month NLAD snapshot (SR-6.8)."],
       ["NISC", "RIVR billing / CIS platform", "Customer account, service order, plan, credit, billing effective date."],
       ["USAC TLVT", "Tribal Lands Verification Tool", "Per-address check of principal residence against qualifying Tribal lands (SR-4.4)."]],
      widths=[1.1, 2.7, 3.0])

callout(doc, "Golden rule, encoded everywhere: an approved National Verifier result must exist BEFORE any NLAD "
             "enrollment. No NV = no enrollment, no credit, no claim. (SR-3.1 / SR-3.2)", kind="stop")

# ---------------------------------------------------------------------------
# A) UNIVERSAL ENROLLMENT CONTROL POINTS
# ---------------------------------------------------------------------------
h1(doc, "A. Universal enrollment control points (the 15 mandatory steps)")
para(doc, "Every enrollment — regardless of channel, customer type, or benefit level — MUST pass through all 15 "
          "control points below. Each of the ten workflows in Section B references these control points by number "
          "(CP-1 … CP-15). If any control point is skipped, the enrollment is not complete and must not be claimed "
          "for reimbursement.")

table(doc,
      ["CP #", "Control point", "Owner", "System", "Source / rule"],
      [["CP-1", "Identity & address collection — legal name, DOB (last 4 SSN or Tribal ID as accepted by NV), and full principal-residence address.", "ER/CSR", "Intake form → NV", "SR-3.1"],
       ["CP-2", "National Verifier application — submit eligibility application (program-based or income) and obtain a result.", "ER", "NV", "SR-3.1"],
       ["CP-3", "Household worksheet (when applicable) — complete the one-per-household worksheet when more than one household may share the address.", "ER", "NV / paper", "SR-1.8"],
       ["CP-4", "Customer consent — obtain the customer's certification/consent to eligibility statements and data use.", "ER/CSR", "NV / signed form", "SR-3.1"],
       ["CP-5", "Benefit-transfer consent (when applicable) — if the customer already receives Lifeline elsewhere, obtain explicit benefit-transfer consent.", "ER", "NLAD", "SR-3.6"],
       ["CP-6", "Tribal-lands verification — run the USAC Tribal Lands Verification Tool on the principal residence for ANY enhanced-Tribal request.", "ER/CO", "USAC TLVT", "SR-4.4"],
       ["CP-7", "Tribal membership verification (only when relevant to a separate Tribe-funded program) — privacy-preserving confirmation with the Lumbee Tribe; NOT used for enhanced Tribal.", "CO", "Tribe MOU process", "SR-5.6"],
       ["CP-8", "NV approval confirmed — a valid, unexpired APPROVED NV result exists. REQUIRED before CP-9.", "ER/CO", "NV", "SR-3.1"],
       ["CP-9", "NLAD enrollment — create the subscriber record; duplicate check clears; set the Tribal benefit flag only if CP-6 verified.", "ER", "NLAD", "SR-3.2 / SR-4.4"],
       ["CP-10", "NISC account update — create/attach the customer account and select the correct plan.", "CSR/BILL", "NISC", "Program control"],
       ["CP-11", "Service-order completion — provision or confirm active broadband service (install or plan change).", "TECH/CSR", "NISC", "SR-2.1/2.2"],
       ["CP-12", "Billing effective date — set the Lifeline credit effective date aligned to service start and NLAD enrollment date.", "BILL", "NISC", "Program control"],
       ["CP-13", "Confirmation notice — send the customer a written confirmation of enrollment, plan, credit amount, and their rights.", "CSR", "NISC/notice", "SR-6.12"],
       ["CP-14", "Quality-control review — independent QC reviewer confirms CP-1…CP-13 before the record is eligible to be claimed.", "QC", "Checklist", "Section F"],
       ["CP-15", "Secure document retention — store all eligibility/consent/verification records securely for the required period.", "CO", "Records system", "SR-6.11 (§54.417)"]],
      widths=[0.5, 3.4, 0.7, 0.9, 1.0], small=True)

callout(doc, "Retention (CP-15): keep compliance records at least 3 full preceding calendar years; keep each "
             "subscriber's eligibility documentation for as long as they receive service and a minimum of 3 years "
             "thereafter. This is the §54.417 Lifeline rule — NOT the 10-year high-cost rule. (SR-6.11)", kind="note")
callout(doc, "NV-before-NLAD (CP-8 before CP-9) is a hard sequence. NLAD enrollment without an approved NV result "
             "is an improper enrollment and cannot be reimbursed. (SR-3.1 / SR-3.2)", kind="warn")

# ---------------------------------------------------------------------------
# B) TEN WORKFLOWS
# ---------------------------------------------------------------------------
h1(doc, "B. Enrollment workflows (ten scenarios)")
para(doc, "Each workflow is a concrete, ordered procedure. Steps name the role, the system, and finish with QC "
          "(CP-14) and retention (CP-15). All workflows share the golden rule: NV approval (CP-8) precedes NLAD "
          "enrollment (CP-9).")

def workflow(title, intro, steps, notes=None):
    h2(doc, title)
    if intro:
        para(doc, intro, italic=True, color=GREY)
    for s in steps:
        numbered(doc, s)
    if notes:
        for n in notes:
            callout(doc, n[0], kind=n[1])

# 1 --------------------------------------------------------------
workflow(
    "B.1 New RIVR Tech customer",
    "Applicant has no existing RIVR service. Standard broadband-first Lifeline path. Touches CP-1 through CP-15.",
    [
        "ER (RAD Rep ID active) collects legal name, DOB, principal-residence address, and eligibility basis (program or income). [CP-1]",
        "ER submits the National Verifier application in NV and selects the customer's qualifying program or income path. [CP-2]",
        "If more than one household may share the address, ER completes the one-per-household worksheet. [CP-3]",
        "ER captures the customer's consent/certification to the eligibility statements and data-use terms. [CP-4]",
        "ER checks NV for a duplicate/existing Lifeline benefit; if the customer is enrolled with another provider, switch to Workflow B.3 (benefit transfer). [CP-5]",
        "ER waits for and confirms an APPROVED NV result. If pending or rejected, do NOT proceed; resolve documentation with the customer. [CP-8]",
        "ER enrolls the subscriber in NLAD; duplicate check must clear. Tribal benefit flag left OFF unless enhanced Tribal was separately verified via TLVT (see B.9). [CP-9]",
        "CSR/BILL creates the RIVR account in NISC and selects the correct plan (default: Senior $10 plan or applicable retail plan the credit attaches to). [CP-10]",
        "TECH schedules and completes the fiber install / service order; confirms active 25/3-or-better service (RIVR plans exceed minimums). [CP-11]",
        "BILL sets the Lifeline credit and billing effective date aligned to service start and the NLAD enrollment date. [CP-12]",
        "CSR sends the written enrollment confirmation notice (plan, credit amount, recertification obligation, rights). [CP-13]",
        "QC performs the independent second-person review against the Section F checklist before the record is claimed. [CP-14]",
        "CO files all eligibility/consent/verification records to secure retention per §54.417. [CP-15]",
    ],
    [("Enhanced Tribal ($25 add-on) is NOT applied here by default. It requires a per-address TLVT verification (Workflow B.9). Working assumption today: 0 qualifying addresses (SR-5.5).", "warn")],
)

# 2 --------------------------------------------------------------
workflow(
    "B.2 Existing RIVR Tech customer (already has internet — apply Lifeline credit to current plan)",
    "Customer already buys RIVR broadband; we are adding the Lifeline credit to their existing service, not provisioning new service.",
    [
        "CSR pulls the existing NISC account and confirms the service is active and in the customer's name at the principal residence. [CP-1]",
        "ER submits the National Verifier application for the customer (program or income basis). [CP-2]",
        "ER completes the one-per-household worksheet if the address may contain multiple households. [CP-3]",
        "ER obtains the customer's consent/certification. [CP-4]",
        "ER checks for an existing Lifeline benefit elsewhere; if found, route to B.3 benefit transfer. [CP-5]",
        "ER confirms an APPROVED NV result before any NLAD action. [CP-8]",
        "ER enrolls the subscriber in NLAD; duplicate check clears. [CP-9]",
        "BILL keeps the customer on their current plan and attaches the Lifeline credit to that plan in NISC (no new service order unless the customer also downgrades to the Senior $10 plan). [CP-10]",
        "CSR confirms no provisioning change is needed; service remains active. [CP-11]",
        "BILL sets the credit effective date to the next clean billing cycle on/after the NLAD enrollment date — never retroactively beyond the enrollment date. [CP-12]",
        "CSR sends confirmation showing the credit applied to the existing plan and the new net amount. [CP-13]",
        "QC reviews against Section F. [CP-14]",
        "CO retains all records. [CP-15]",
    ],
    [("Do NOT back-date the credit to before the NLAD enrollment date. Subsidies apply prospectively (see Section D reversal rule).", "warn")],
)

# 3 --------------------------------------------------------------
workflow(
    "B.3 Benefit transfer from another provider",
    "The applicant already receives Lifeline from another carrier — NLAD shows a duplicate. The benefit moves to RIVR via consent-based transfer (SR-3.6).",
    [
        "ER collects identity/address and attempts NLAD enrollment; the duplicate-benefit condition is returned. [CP-1]",
        "ER confirms (or submits) the NV application so an approved eligibility result underlies the transfer. [CP-2]",
        "ER completes the one-per-household worksheet if applicable. [CP-3]",
        "ER explains the transfer to the customer and obtains explicit BENEFIT-TRANSFER consent — the customer's affirmative acknowledgment that moving the benefit ends it at the prior provider. [CP-5 / CP-4]",
        "ER confirms the APPROVED NV result. [CP-8]",
        "ER executes the consent-based benefit transfer in NLAD (transfer transaction, not a fresh duplicate enrollment). [CP-9]",
        "CSR/BILL sets up or updates the NISC account and plan. [CP-10]",
        "TECH provisions service if the customer is new to RIVR; otherwise confirm active service. [CP-11]",
        "BILL sets the credit effective date from the transfer date. [CP-12]",
        "CSR sends confirmation noting the transfer and that the benefit no longer applies at the prior carrier. [CP-13]",
        "QC verifies the transfer transaction (not a duplicate) and consent record. [CP-14]",
        "CO retains the transfer-consent record with the eligibility file. [CP-15]",
    ],
    [("A transfer requires the customer's affirmative consent and moves — not duplicates — the single per-household benefit (SR-1.8, SR-3.6). Never create a second concurrent benefit.", "stop")],
)

# 4 --------------------------------------------------------------
workflow(
    "B.4 Customer applying online",
    "Applicant initiates via the RIVR website / self-service link. Channel differs; the 15 control points do not.",
    [
        "Customer submits the online intake (name, DOB, address, eligibility basis); system captures CP-1 data.",
        "ER reviews the submission for completeness and initiates/monitors the NV application (customer may complete the consumer-facing NV flow directly). [CP-2]",
        "System prompts the one-per-household worksheet if the address flags multiple households. [CP-3]",
        "Customer e-signs the consent/certification; ER confirms it is captured. [CP-4]",
        "ER checks for an existing benefit; if present, route to B.3. [CP-5]",
        "ER confirms the APPROVED NV result before NLAD. [CP-8]",
        "ER completes NLAD enrollment. [CP-9]",
        "CSR/BILL creates/updates the NISC account and plan. [CP-10]",
        "TECH schedules install (new) or confirms active service (existing). [CP-11]",
        "BILL sets credit and billing effective date. [CP-12]",
        "CSR emails the written confirmation notice. [CP-13]",
        "QC reviews the online enrollment against Section F, with extra attention to identity-match quality. [CP-14]",
        "CO retains e-signature, consent, and NV/NLAD records. [CP-15]",
    ],
    [("Online channel must still capture verifiable identity and consent. Do not enroll on an unverified web form; NV approval governs (CP-8).", "note")],
)

# 5 --------------------------------------------------------------
workflow(
    "B.5 Customer applying by telephone",
    "CSR/ER assists the applicant on a recorded line. Verbal consent must be captured to the standard NV/consent requirements.",
    [
        "CSR verifies the caller's identity and captures name, DOB, address, and eligibility basis. [CP-1]",
        "ER submits the NV application on the customer's behalf. [CP-2]",
        "CSR administers the one-per-household worksheet verbally if applicable and records the answers. [CP-3]",
        "CSR reads the certification/consent script and captures the customer's verbal consent on the recorded line (and via follow-up e-sign where required). [CP-4]",
        "ER checks for an existing benefit; route to B.3 if present. [CP-5]",
        "ER confirms the APPROVED NV result. [CP-8]",
        "ER completes NLAD enrollment. [CP-9]",
        "CSR/BILL creates/updates the NISC account and plan. [CP-10]",
        "TECH schedules install or confirms active service. [CP-11]",
        "BILL sets credit and billing effective date. [CP-12]",
        "CSR sends the written confirmation notice by mail/email. [CP-13]",
        "QC reviews, confirming the consent recording/reference is logged. [CP-14]",
        "CO retains the call reference, consent, and NV/NLAD records. [CP-15]",
    ],
    [("Log the call/consent reference ID with the file. A telephone enrollment without a retrievable consent record fails QC.", "warn")],
)

# 6 --------------------------------------------------------------
workflow(
    "B.6 Customer applying in person",
    "Applicant visits a RIVR location / community event. ER assists face-to-face; physical documents can be imaged on the spot.",
    [
        "ER checks photo ID and captures name, DOB, address, and eligibility basis; images supporting documents. [CP-1]",
        "ER submits the NV application. [CP-2]",
        "ER completes the one-per-household worksheet with the customer if applicable. [CP-3]",
        "ER obtains a wet or e-signature on the certification/consent form. [CP-4]",
        "ER checks for an existing benefit; route to B.3 if present. [CP-5]",
        "ER confirms the APPROVED NV result. [CP-8]",
        "ER completes NLAD enrollment. [CP-9]",
        "CSR/BILL creates/updates the NISC account and plan. [CP-10]",
        "TECH schedules install or confirms active service. [CP-11]",
        "BILL sets credit and billing effective date. [CP-12]",
        "CSR provides/sends the written confirmation notice. [CP-13]",
        "QC reviews the imaged documents and signatures against Section F. [CP-14]",
        "CO retains imaged documents, signed consent, and NV/NLAD records. [CP-15]",
    ],
    [("Never retain more personal document data than needed. Image only what NV/QC require and store it in the secure records system (CP-15).", "note")],
)

# 7 --------------------------------------------------------------
workflow(
    "B.7 Senior applicant",
    "Age alone does NOT qualify anyone for Lifeline. A senior still needs an approved NV result. The commercial default is the $10 Senior 100/100 plan; the Lifeline credit (if the senior also qualifies) reduces that further via top-up. Handle the four sub-cases explicitly.",
    [
        "CSR/ER greets the senior and explains: the $10 Senior plan is a RIVR commercial offer; the federal Lifeline credit is a SEPARATE eligibility question that requires NV. [CP-1]",
        "ER attempts an NV eligibility application (program or income). Age is captured for plan routing only, not as a qualifier. [CP-2]",
        "ER completes the one-per-household worksheet if applicable. [CP-3]",
        "ER obtains consent/certification. [CP-4]",
        "Determine the sub-case (below) and route accordingly.",
        "SUB-CASE (a) — Senior QUALIFIES for Lifeline: confirm APPROVED NV [CP-8] → NLAD enroll [CP-9] → NISC place on Senior $10 plan and apply the up-to-$9.25 standard credit as a top-up/offset [CP-10] → service [CP-11] → billing effective date [CP-12] → confirmation [CP-13].",
        "SUB-CASE (b) — Senior is a LUMBEE MEMBER: membership is verified via the Tribe (privacy-preserving) but does NOT grant enhanced Tribal and does NOT by itself grant Lifeline. Still requires an approved NV result to receive any Lifeline credit; if approved, treat as (a). If a Tribe-funded benefit MOU exists, apply that separately (see B.8).",
        "SUB-CASE (c) — Senior's ADDRESS qualifies for enhanced Tribal: run the USAC TLVT on the principal residence [CP-6]; if verified on qualifying Tribal lands, set the NLAD Tribal flag and apply up to $34.25 total. (Assume 0 qualifying today — SR-5.5.)",
        "SUB-CASE (d) — Senior qualifies for NONE of the above: no Lifeline credit. Offer the $10 Senior commercial plan (or other retail plan) with no federal subsidy; do NOT enroll in NLAD.",
        "QC reviews the sub-case routing and confirms no NLAD enrollment occurred in sub-case (d). [CP-14]",
        "CO retains all records for enrolled sub-cases; retains the declination note for sub-case (d). [CP-15]",
    ],
    [("Age is not a Lifeline qualifier. The $10 Senior plan can be sold to any senior; the Lifeline credit only attaches when NV approves eligibility (SR-1.4/1.6).", "warn"),
     ("Lumbee membership ≠ enhanced Tribal and ≠ Lifeline eligibility. Enhanced $25 is address-based via TLVT only (SR-5.6).", "stop")],
)

# 8 --------------------------------------------------------------
workflow(
    "B.8 Lumbee tribal member",
    "Membership is confirmed with the Tribe in a privacy-preserving way. Membership does NOT confer enhanced Tribal support and does NOT by itself confer Lifeline. The member may access a Tribe-funded benefit only if an MOU exists.",
    [
        "CSR/ER collects identity/address and notes the customer's stated Lumbee membership. [CP-1]",
        "CO (or designated liaison) confirms membership through the Tribe's privacy-preserving verification channel — minimum data, no bulk roster storage. [CP-7]",
        "ER submits the NV eligibility application — membership is NOT a substitute for NV. [CP-2]",
        "ER completes the one-per-household worksheet if applicable. [CP-3]",
        "ER obtains consent/certification, including consent to Tribe verification where required. [CP-4]",
        "If the member also requests enhanced Tribal, run the USAC TLVT on the residence [CP-6]; membership alone never sets the Tribal flag.",
        "ER confirms the APPROVED NV result before NLAD. [CP-8]",
        "ER completes NLAD enrollment with the standard (up to $9.25) benefit unless TLVT verified the address for enhanced. [CP-9]",
        "BILL applies any separately funded LUMBEE TRIBE benefit ONLY if an MOU authorizes it, and books it to the Tribe-contribution GL category — never commingled with USAC Lifeline funds (SR-10.2). [CP-10]",
        "TECH provisions/confirms service; BILL sets credit and effective date. [CP-11 / CP-12]",
        "CSR sends confirmation itemizing the federal credit and any Tribe-funded benefit distinctly. [CP-13]",
        "QC confirms membership verification was privacy-preserving and funding streams are separated. [CP-14]",
        "CO retains records; membership confirmation stored per minimization rules. [CP-15]",
    ],
    [("Keep the four funding streams separate: federal Lifeline (USAC), TBCP/grants, RIVR-funded discounts, and Lumbee Tribe contributions. No commingling (SR-10.2).", "note")],
)

# 9 --------------------------------------------------------------
workflow(
    "B.9 Customer seeking enhanced Tribal support",
    "The ONLY path to the additional up-to-$25 (total up to $34.25). Enhanced Tribal is ADDRESS-based, not membership-based (SR-4/SR-5).",
    [
        "ER collects the exact principal-residence street address (and lat/long if the AMS error path requires it). [CP-1]",
        "ER (or CO) runs the USAC Tribal Lands Verification Tool on that principal residence. This step is MANDATORY and cannot be inferred from membership or county. [CP-6]",
        "DECISION: If TLVT returns NOT on qualifying Tribal lands → the customer gets STANDARD Lifeline only (up to $9.25). Do NOT set the NLAD Tribal flag. Proceed as Workflow B.1 for the standard benefit.",
        "DECISION: If TLVT VERIFIES the address on qualifying Tribal lands → continue with the enhanced path below.",
        "ER submits/confirms the NV eligibility application (program or income). [CP-2]",
        "ER completes the one-per-household worksheet if applicable, and obtains consent. [CP-3 / CP-4]",
        "ER confirms the APPROVED NV result. [CP-8]",
        "ER enrolls in NLAD and sets the 'Lifeline Tribal Benefit?' flag to YES only because TLVT verified the address. [CP-9]",
        "BILL applies the total up-to-$34.25 credit and certifies full pass-through to the subscriber. [CP-10 / CP-12]",
        "CSR sends confirmation stating the enhanced amount and that it derives from verified Tribal-lands residence. [CP-13]",
        "QC re-checks that a TLVT verification record exists for the exact address before the enhanced claim is made. [CP-14]",
        "CO retains the TLVT verification result with the file. [CP-15]",
    ],
    [("Lumbee membership and four-county residence do NOT qualify anyone for enhanced Tribal. The enhanced $25 requires the principal residence to be on qualifying Tribal lands per §54.400(e), verified per-address via the USAC TLVT (SR-4.2, SR-5.6).", "stop"),
     ("Working assumption today: the Lumbee have no reservation, no land in trust, and no §54.412 designation — so assume 0 qualifying addresses until USAC/FCC confirms otherwise (SR-5.5). Every enhanced request should currently resolve to standard-only.", "warn")],
)

# 10 --------------------------------------------------------------
workflow(
    "B.10 Customer with a temporary address or shared household",
    "Handles the one-per-household rule, the economic-unit test, and temporary-address situations.",
    [
        "ER collects the address and asks the household-composition questions: does anyone else at this address receive Lifeline? Are occupants one economic unit? [CP-1]",
        "ER applies the ECONOMIC-UNIT test: a 'household' is the people at one address who share income and expenses. Separate economic units at one address can each hold one benefit. [CP-3]",
        "ER completes the one-per-household worksheet whenever multiple households may share the address; the customer certifies the worksheet. [CP-3 / CP-4]",
        "For a TEMPORARY address, ER records it as the principal residence for now and flags the account for address re-verification; the customer must update within the required window if it changes (see Section D address-change SOP). [CP-1]",
        "ER submits the NV application. [CP-2]",
        "ER checks for an existing benefit at the address; if a duplicate exists, resolve via worksheet or B.3 transfer. [CP-5]",
        "ER confirms the APPROVED NV result. [CP-8]",
        "ER completes NLAD enrollment; the duplicate-address check must clear or be resolved by the worksheet. [CP-9]",
        "CSR/BILL sets up the NISC account and plan; TECH provisions/confirms service. [CP-10 / CP-11]",
        "BILL sets the credit effective date; CSR sends confirmation and explains the address-update duty. [CP-12 / CP-13]",
        "QC verifies the worksheet and economic-unit determination. [CP-14]",
        "CO retains the worksheet and address records. [CP-15]",
    ],
    [("One Lifeline benefit per household; 'household' = people at one address sharing income and expenses as one economic unit (SR-1.8). A temporary address must be re-verified — especially for any Tribal-lands determination.", "note")],
)

# ---------------------------------------------------------------------------
# C) DECISION TREE
# ---------------------------------------------------------------------------
h1(doc, "C. Decision tree — which benefit does this customer get?")
para(doc, "Walk this tree for every applicant. It resolves the benefit level and the plan the credit attaches to. "
          "Read the table top-to-bottom; the first matching row is the outcome.")

table(doc,
      ["Step", "Question", "If YES", "If NO"],
      [["1", "Standard-eligible? (approved NV result — program or income ≤135% FPG)", "Go to step 2.", "No Lifeline. Offer retail plan (incl. $10 Senior commercial plan if a senior). STOP."],
       ["2", "Tribal-lands ADDRESS verified via USAC TLVT on the principal residence?", "Enhanced Tribal: total up to $34.25/mo. Set NLAD Tribal flag. (Assume 0 qualifying today — SR-5.5.)", "Go to step 3."],
       ["3", "(Address not on Tribal lands.) Apply STANDARD Lifeline.", "Standard Lifeline: up to $9.25/mo. Go to step 4 for plan routing.", "—"],
       ["4", "Is the applicant a senior (plan routing only)?", "Route to the $10 Senior 100/100 plan; apply the up-to-$9.25 credit as a top-up/offset against the $10.", "Apply the up-to-$9.25 credit to the applicable RIVR plan the customer selects."]],
      widths=[0.5, 3.0, 2.0, 2.0], small=True)

para(doc, "Same logic as nested bullets:")
bullet(doc, "Standard-eligible (NV approved)?")
bullet(doc, "NO → No Lifeline. Retail plan only (a senior may still buy the $10 Senior commercial plan, but with no federal subsidy).", level=1)
bullet(doc, "YES → Tribal-lands address verified via TLVT?", level=1)
bullet(doc, "YES → Enhanced Tribal: up to $34.25/mo (assume 0 qualifying today — SR-5.5).", level=1)
bullet(doc, "NO → Standard Lifeline: up to $9.25/mo.", level=1)
bullet(doc, "Senior? → route to $10 Senior plan; the $9.25 credit tops up / offsets the $10.", level=1)
bullet(doc, "Not a senior? → apply the $9.25 credit to the customer's chosen RIVR plan.", level=1)

callout(doc, "Enhanced Tribal is address-based and, on today's facts, resolves to 0 qualifying subscribers. Never "
             "route to $34.25 on the basis of Lumbee membership or four-county residence (SR-5.5, SR-5.6).", kind="stop")

# ---------------------------------------------------------------------------
# D) DE-ENROLLMENT & LIFECYCLE SOPs
# ---------------------------------------------------------------------------
h1(doc, "D. De-enrollment & lifecycle SOPs")
para(doc, "These procedures govern the subscriber lifecycle after enrollment. The overriding financial rule: "
          "removing a benefit reverses FUTURE subsidies only. There is NO improper retroactive billing of the "
          "customer for periods already served in good faith.")

callout(doc, "Reversal rule (applies to every SOP in this section): stop or adjust the subsidy going FORWARD from "
             "the effective de-enrollment/change date. Do NOT retroactively bill the customer for prior periods "
             "already covered by the credit. Recover improperly claimed reimbursement from USAC per USAC process, "
             "never from the subscriber.", kind="stop")

h2(doc, "D.1 Annual recertification")
para(doc, "Each subscriber must recertify eligibility annually.", italic=True, color=GREY)
numbered(doc, "CO monitors USAC's recertification schedule and the automated data-source check result for each subscriber (SR-3.3).")
numbered(doc, "If the data-source check PASSES, CO records the pass; no customer action needed.")
numbered(doc, "If the data-source check FAILS, CSR notifies the subscriber that they must respond and recertify.")
numbered(doc, "The subscriber has 60 days from the recertification failure/notice to respond or is de-enrolled (SR-3.3).")
numbered(doc, "CSR sends reminder notices within the 60-day window (e.g., at day 15, 30, 50).")
numbered(doc, "If the subscriber recertifies in time, CO records the result; benefit continues.")
numbered(doc, "If the 60-day window closes with no valid response, CO de-enrolls the subscriber in NLAD (see D.7).")
numbered(doc, "BILL removes the credit effective from the de-enrollment date (future only). CSR sends the de-enrollment notice.")
numbered(doc, "QC/CO retain the recertification correspondence and outcome (CP-15).")

h2(doc, "D.2 Customer-reported loss of eligibility")
numbered(doc, "Subscriber notifies RIVR they no longer qualify (e.g., left Medicaid/SNAP, income rose).")
numbered(doc, "CSR logs the report with date and reason; CO reviews.")
numbered(doc, "CO de-enrolls the subscriber in NLAD promptly (SR-3.5).")
numbered(doc, "BILL removes the credit effective from the loss-of-eligibility date going forward; no retroactive customer billing.")
numbered(doc, "CSR offers conversion to a standard retail plan (see D.10) and sends the de-enrollment/transition notice.")
numbered(doc, "CO retains the customer's report and the de-enrollment record.")

h2(doc, "D.3 Duplicate-benefit notification")
numbered(doc, "USAC/NLAD flags a duplicate benefit (same subscriber or same household).")
numbered(doc, "CO investigates: is it a true duplicate, a household/economic-unit issue, or a pending transfer?")
numbered(doc, "If a genuine duplicate at RIVR, CO resolves by de-enrolling the improper record (usually the later one) in NLAD.")
numbered(doc, "If it is a one-per-household worksheet issue, CO obtains/reviews the worksheet and corrects the record.")
numbered(doc, "BILL adjusts the credit forward from resolution; CSR notifies the subscriber of the outcome.")
numbered(doc, "CO retains the investigation notes and NLAD actions.")

h2(doc, "D.4 Address change")
numbered(doc, "Subscriber reports a new principal-residence address; CSR captures it in NISC.")
numbered(doc, "CO RE-RUNS the USAC TLVT on the NEW address whenever any Tribal benefit is or could be involved (SR-4.4). Enhanced status does NOT travel with the customer.")
numbered(doc, "If the new address is NOT on qualifying Tribal lands, CO removes the NLAD Tribal flag and steps the benefit down to standard (up to $9.25) going forward.")
numbered(doc, "CO updates the subscriber's address in NLAD within 10 business days of the change (SR-3.2).")
numbered(doc, "CO re-checks for a duplicate at the new address (one-per-household).")
numbered(doc, "BILL adjusts any credit change forward from the move date; CSR sends confirmation of the new address and benefit level.")
numbered(doc, "CO retains the updated TLVT result and address-change record.")

h2(doc, "D.5 Death of subscriber")
numbered(doc, "RIVR is notified of the subscriber's death (family, returned mail, obituary, or account contact).")
numbered(doc, "CSR logs the notification and date; CO verifies to a reasonable standard.")
numbered(doc, "CO de-enrolls the deceased subscriber in NLAD effective from the notification/verification date.")
numbered(doc, "BILL stops the credit going forward; no retroactive clawback from the estate for covered periods.")
numbered(doc, "CSR handles the account (close, transfer to a surviving eligible household member via a NEW enrollment, or convert to retail).")
numbered(doc, "CO retains the notification and de-enrollment record.")

h2(doc, "D.6 Non-usage rule")
para(doc, "The federal non-usage rule (30 days non-use → 15-day cure → terminate) applies ONLY to services with no "
          "monthly fee to the subscriber (SR-3.4).", italic=True, color=GREY)
numbered(doc, "CO first determines applicability: because the Senior plan carries a >$0 customer charge ($10), the non-usage rule generally does NOT apply. [CONFIRM applicability with counsel given the $10 charge — SR-3.4].")
numbered(doc, "IF (and only if) a $0-to-subscriber service is ever offered: CO monitors for 30 consecutive days of non-use.")
numbered(doc, "At 30 days non-use, CSR sends the 15-day cure notice.")
numbered(doc, "If the subscriber uses the service within 15 days, the benefit continues.")
numbered(doc, "If uncured after 15 days, CO de-enrolls in NLAD; BILL stops the credit going forward.")
numbered(doc, "CO retains the usage log, cure notice, and outcome.")
callout(doc, "[CONFIRM] Do not implement automated non-usage de-enrollment on any plan that charges the subscriber "
             "a monthly fee until counsel confirms the rule's applicability to the $10 Senior plan (SR-3.4).", kind="warn")

h2(doc, "D.7 Failure to recertify → de-enroll")
numbered(doc, "The 60-day recertification window (D.1) closes with no valid subscriber response (SR-3.3).")
numbered(doc, "CO confirms no response is on file and no pending documentation exists.")
numbered(doc, "CO de-enrolls the subscriber in NLAD, citing failure to recertify (SR-3.5).")
numbered(doc, "BILL removes the credit effective from the de-enrollment date (future only).")
numbered(doc, "CSR sends the de-enrollment notice explaining how to re-apply and offering a retail plan (D.10).")
numbered(doc, "CO retains the recertification history and de-enrollment record.")

h2(doc, "D.8 Benefit transfer OUT (customer moves to another provider)")
numbered(doc, "Another carrier initiates a consent-based benefit transfer in NLAD; RIVR sees the transfer-out (SR-3.6).")
numbered(doc, "CO confirms the transfer is legitimate (customer-initiated with consent at the new provider).")
numbered(doc, "CO records that the benefit has left RIVR; the NLAD record moves to the new provider.")
numbered(doc, "BILL removes the Lifeline credit at RIVR going forward from the transfer date.")
numbered(doc, "CSR contacts the customer to confirm whether they wish to keep RIVR service on a retail plan (D.10) or cancel.")
numbered(doc, "CO retains the transfer-out record.")

h2(doc, "D.9 Program termination")
para(doc, "Applies if RIVR exits Lifeline or the program winds down.", italic=True, color=GREY)
numbered(doc, "CO obtains the internal decision/date to terminate Lifeline participation and any required USAC/NCUC notice obligations.")
numbered(doc, "CSR sends advance written notice to all affected subscribers with the termination date and their options.")
numbered(doc, "CO de-enrolls subscribers in NLAD per the orderly wind-down schedule; benefits stop going forward only.")
numbered(doc, "BILL transitions each subscriber to a retail plan (D.10) or processes cancellation per the customer's choice.")
numbered(doc, "CO files the final claims and retains all records for the full §54.417 retention period (SR-6.11).")
numbered(doc, "CO documents the termination and notice delivery for audit.")

h2(doc, "D.10 Conversion to standard retail plan")
numbered(doc, "Trigger: any de-enrollment (D.1–D.9) where the customer wants to keep RIVR service without the Lifeline credit.")
numbered(doc, "CSR explains the new net price (retail price without the credit) and confirms the customer's choice.")
numbered(doc, "BILL removes the Lifeline credit and moves the account to the selected retail plan in NISC, effective the next clean cycle.")
numbered(doc, "CSR sends written confirmation of the plan change and new billing amount BEFORE the first full retail charge.")
numbered(doc, "CO confirms the subscriber is de-enrolled from NLAD so no further Lifeline claim is made.")
numbered(doc, "CO retains the conversion record.")

h2(doc, "D.11 Required customer notices & timing")
table(doc,
      ["Event", "Notice to customer", "Timing"],
      [["Enrollment confirmed", "Plan, credit amount, recertification duty, rights (CP-13)", "At enrollment"],
       ["Recertification due / failed check", "Must respond to keep benefit", "At failure; reminders through the 60-day window (SR-3.3)"],
       ["Non-usage (only if applicable)", "15-day cure notice", "At 30 days non-use (SR-3.4) [CONFIRM]"],
       ["Address change processed", "New address + resulting benefit level", "After NLAD update (≤10 business days, SR-3.2)"],
       ["De-enrollment (any cause)", "Reason, effective date, re-apply path, retail options", "At or before the effective de-enrollment date"],
       ["Conversion to retail", "New net price before first full retail charge", "Before the first retail billing cycle"],
       ["Program termination", "Termination date + options", "Advance written notice before termination"]],
      widths=[1.6, 3.0, 2.0], small=True)

h2(doc, "D.12 Reversal of FUTURE subsidies only — no improper retroactive billing")
para(doc, "This is a standalone control that governs every de-enrollment and downgrade above.")
numbered(doc, "When any de-enrollment or benefit downgrade occurs, BILL adjusts the subsidy PROSPECTIVELY from the effective date.")
numbered(doc, "The subscriber is NEVER retroactively billed for prior periods that were properly covered by the credit.")
numbered(doc, "Where RIVR over-claimed reimbursement from USAC, CO handles recovery through the USAC true-up/repayment process — not by charging the customer.")
numbered(doc, "Where enhanced Tribal was applied and later found not address-qualified, step down to standard going forward and, if the enhanced amount was improperly claimed, remediate with USAC — do not back-bill the subscriber.")
numbered(doc, "CO documents every reversal with its effective date and the reason.")

# ---------------------------------------------------------------------------
# E) ACCOMMODATIONS & AUTHORIZED REPRESENTATIVES
# ---------------------------------------------------------------------------
h1(doc, "E. Reasonable accommodations & authorized representatives")

h2(doc, "E.1 Reasonable accommodations (ADA)")
numbered(doc, "At first contact, CSR/ER offers accommodations for customers with disabilities (large-print or accessible notices, extended time, alternative-format documents, TTY/relay, in-person or phone assistance).")
numbered(doc, "CSR records the accommodation requested and provided in the account notes (data-minimized — do not record diagnosis).")
numbered(doc, "The accommodation must not change the eligibility standard: NV approval (CP-8) is still required; only the manner of assistance flexes.")
numbered(doc, "CSR ensures notices in Section D.11 are delivered in the customer's accessible format and, where needed, in the customer's preferred language.")
numbered(doc, "CO retains the accommodation note with the file.")

h2(doc, "E.2 Authorized representatives")
numbered(doc, "A customer may designate an authorized representative (e.g., caregiver, family member) to enroll or manage the benefit on their behalf.")
numbered(doc, "CSR/ER captures the customer's written consent authorizing the representative, including the scope (enroll, recertify, change plan).")
numbered(doc, "The representative provides their own identity; the ELIGIBILITY and certifications still pertain to the subscriber, who must consent to the eligibility statements (CP-4).")
numbered(doc, "For NV, follow USAC's authorized/assisting-party rules; the ER's RAD Rep ID still governs who submits the enrollment.")
numbered(doc, "CSR verifies the representative's authority before disclosing account details or making changes.")
numbered(doc, "CO retains the authorization and consent records with the file (CP-15).")
callout(doc, "An authorized representative can act for the customer, but the customer remains the subscriber and the "
             "eligibility/consent (CP-4) is theirs. Verify the authorization before any account change.", kind="note")

# ---------------------------------------------------------------------------
# F) QC CHECKLIST
# ---------------------------------------------------------------------------
h1(doc, "F. Quality-control checklist (reviewed on EVERY enrollment)")
para(doc, "The QC Reviewer (independent of the enrolling ER) completes this checklist for each enrollment before "
          "it becomes eligible to be claimed in LCS. Any 'No' blocks the claim until remediated.")

table(doc,
      ["#", "QC checks (must all be YES)", "Control point", "Source"],
      [["1", "Identity & full principal-residence address captured and legible.", "CP-1", "SR-3.1"],
       ["2", "National Verifier application submitted and result attached.", "CP-2", "SR-3.1"],
       ["3", "APPROVED NV result exists and is unexpired — dated BEFORE NLAD enrollment.", "CP-8", "SR-3.1"],
       ["4", "One-per-household worksheet completed where the address may hold multiple households.", "CP-3", "SR-1.8"],
       ["5", "Customer consent/certification captured (signed/verbal-logged/e-signed).", "CP-4", "SR-3.1"],
       ["6", "Benefit-transfer consent captured where a prior benefit existed (transfer, not duplicate).", "CP-5", "SR-3.6"],
       ["7", "Enhanced Tribal ONLY if a TLVT verification exists for the exact principal-residence address.", "CP-6", "SR-4.4 / SR-5.6"],
       ["8", "NLAD enrollment complete; duplicate check cleared; Tribal flag matches TLVT result.", "CP-9", "SR-3.2"],
       ["9", "NISC account and correct plan attached; credit amount matches benefit level.", "CP-10", "Program"],
       ["10", "Service active / order complete; meets minimum service standards.", "CP-11", "SR-2.1/2.2"],
       ["11", "Billing effective date set prospectively — not back-dated before NLAD enrollment.", "CP-12", "Section D"],
       ["12", "Written confirmation notice sent to the customer.", "CP-13", "SR-6.12"],
       ["13", "Funding streams correctly separated (USAC vs. Tribe vs. RIVR vs. grant).", "CP-10", "SR-10.2"],
       ["14", "All eligibility/consent/verification records filed to secure retention (§54.417).", "CP-15", "SR-6.11"],
       ["15", "For declinations (no NV / not eligible): confirm NO NLAD enrollment occurred.", "CP-14", "SR-3.1"]],
      widths=[0.4, 3.6, 0.9, 1.1], small=True)

callout(doc, "QC is a hard gate. An enrollment that fails any check must not be included in the monthly LCS claim "
             "until the finding is remediated and re-reviewed (SR-6.8).", kind="warn")

footer_revhist(doc)

doc.save(OUT)

# reload to confirm
from docx import Document
_check = Document(OUT)
print("OK 04")
