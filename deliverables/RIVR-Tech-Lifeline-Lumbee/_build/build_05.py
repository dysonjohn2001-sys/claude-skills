import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from docx_helpers import *

OUT = "/home/user/claude-skills/deliverables/RIVR-Tech-Lifeline-Lumbee/05_NISC_Configuration_and_Billing_Specification.docx"

doc = new_doc()

# ---------------------------------------------------------------- COVER
cover(
    doc,
    title="NISC Configuration & Billing Specification",
    subtitle="iVUE (NISC) rate codes, credit codes, tax, GL mapping, reconciliation & controls for the Lifeline / Lumbee Broadband Affordability Initiative",
    deliverable_no="05 — NISC Configuration & Billing Specification",
    owner="Billing Manager + Finance + IT",
    approvers="________________  Billing Manager    ________________  Finance    ________________  IT / Security    (name / title / date)",
    version="v0.1 — DRAFT (build phase)",
    extra=("NISC field, screen, and code names in this document are ILLUSTRATIVE and marked "
           "\"[CONFIRM in NISC]\". They must be reconciled against the live iVUE configuration by "
           "RIVR's NISC administrator before any code is created. Do not treat any NISC internal name "
           "here as authoritative. All RIVR retail prices are placeholders — replace \"[retail — from "
           "RIVR price sheet]\" with confirmed figures per SR-8.6."),
)

toc(doc)

# ================================================================ 1. PURPOSE & SCOPE
h1(doc, "1. Purpose & Scope")
para(doc,
     "This specification defines how the federal Lifeline benefit, the (conditional) enhanced Tribal "
     "benefit, and RIVR- and Tribe-funded affordability discounts are represented, taxed, posted, "
     "billed, and reconciled inside RIVR Tech's NISC iVUE billing / OSS platform. It is the single "
     "source of truth for the Billing Manager, Finance, and IT when configuring rate codes, credit "
     "codes, tax rules, general-ledger (GL) mappings, customer-facing bill text, effective-date logic, "
     "and the monthly close and three-way reconciliation.")
para(doc,
     "Scope: NISC billing configuration only. Eligibility determination (National Verifier), enrollment "
     "(NLAD), and reimbursement claiming (LCS) are governed by their own deliverables; this document "
     "specifies how NISC must mirror and reconcile against those systems. It does NOT replace tax, "
     "legal, or regulatory advice — every item flagged \"[CONFIRM]\" requires named sign-off before "
     "go-live (see Deliverable 13, Open Issues & Legal Decisions Log).")

h3(doc, "Governing constraints carried from the Source Register")
bullet(doc, "Enhanced Tribal benefit is ADDRESS-based, not membership-based. As of research, the Lumbee "
            "have no reservation, no land in trust, and no FCC §54.412 designation, so the working "
            "assumption is ZERO enhanced-Tribal subscribers until a specific address is verified "
            "(SR-4, SR-5.5, SR-5.6).")
bullet(doc, "National Verifier approval must precede NLAD enrollment; NLAD enrollment (with its effective "
            "date) governs when the Lifeline credit may be applied in NISC (SR-3.1, SR-3.2).")
bullet(doc, "The full Lifeline support amount must be passed through to the customer's bill — the carrier "
            "may not retain any part of the subsidy (SR-1.1, SR-1.3, SR-6.8).")
bullet(doc, "Four funding streams stay in SEPARATE GL categories — federal Lifeline (USAC), TBCP/grants, "
            "RIVR-funded discounts, Lumbee Tribe contributions. No commingling (SR-10.2).")

callout(doc,
        "PRIVACY / DATA HANDLING: NEVER store full Social Security Numbers, eligibility source documents "
        "(benefit letters, income proofs), or tribal-roll / enrollment data in unsecured NISC free-text "
        "notes, ticket bodies, or general CRM fields. Eligibility is proven in the National Verifier — "
        "NISC holds only the minimum: the NV/NLAD application ID, benefit type, enrollment effective "
        "date, and the enhanced-Tribal verification flag. Full SSNs must be masked; supporting documents "
        "live only in an access-controlled, audit-logged store (see §11). ALL Lifeline support must be "
        "passed through 100% to the customer bill — no carrier retention (SR-6.8, SR-1.1).",
        kind="warn")

# ================================================================ 2. RATE & CREDIT CODE SCHEDULE
h1(doc, "2. Rate & Credit Code Schedule")
para(doc,
     "The table below is the master schedule of rate and credit codes to be created in NISC. Code IDs "
     "and GL account numbers are ILLUSTRATIVE placeholders [CONFIRM in NISC] — RIVR's NISC administrator "
     "assigns the actual values. Amounts marked \"[retail — from RIVR price sheet]\" are placeholders "
     "pending the confirmed RIVR price sheet (SR-8.6). Federal amounts ($9.25 / $25.00 / $34.25) are "
     "fixed by rule and must be entered exactly (SR-1.1, SR-1.3).")

para(doc, "Legend: (+) = charge to customer; (−) = credit to customer. \"Type\" distinguishes a recurring "
          "plan charge from a subsidy credit, a funded discount, or a one-time / usage charge.",
     italic=True, size=9, color=GREY)

rc_headers = ["Code (illustrative)\n[CONFIRM in NISC]", "Description", "Type", "Amount",
              "GL account (illustrative)", "Bill display text", "Notes"]
rc_rows = [
    ["RC-SEN100", "Senior 100/100 broadband plan — new affordable tier", "Recurring plan charge (+)",
     "[retail — from RIVR price sheet] (program design refs a ~$10 customer charge, SR-3.4)",
     "4000-BB-SEN (revenue — broadband)",
     "Senior 100/100 Internet", "New tier below 250/250 entry (SR-8.3). Speed 100/100 exceeds 25/3 "
     "minimum (SR-2.1). Unlimited data meets 1,280 GB min (SR-2.2)."],

    ["CR-LL-STD", "Federal Lifeline credit — standard", "Subsidy credit (−)",
     "−$9.25 (fixed, SR-1.1)", "2100-LL-USAC (contra-revenue / USAC pass-through)",
     "Federal Lifeline Credit  -$9.25",
     "One per household (SR-1.8). Apply ONLY after NV approval + NLAD enrollment (SR-3.1/3.2). Full "
     "pass-through — never partial (SR-6.8)."],

    ["CR-LL-TRB", "Enhanced Tribal Lifeline credit — additional", "Subsidy credit (−)",
     "−$25.00 additional → −$34.25 total with CR-LL-STD (SR-1.3)",
     "2101-LL-TRIBAL (contra-revenue / USAC Tribal pass-through)",
     "Enhanced Tribal Lifeline Credit  -$25.00",
     "ONLY for USAC Tribal-Lands-Verification-Tool–verified addresses; NLAD \"Lifeline Tribal Benefit?\" "
     "= Yes (SR-4.2/4.4). Working assumption: 0 subscribers until an address verifies (SR-5.5/5.6). "
     "Requires full pass-through certification (SR-1.3)."],

    ["RC-SEN-STD?", "(reference) Standard Senior code alias", "Recurring plan charge (+)",
     "[retail — from RIVR price sheet]", "4000-BB-SEN (revenue — broadband)",
     "Senior 100/100 Internet",
     "Use a single Senior plan code (RC-SEN100). Listed only to avoid duplicate codes for the same tier."],

    ["DC-TRIBE", "Tribe-funded affordability discount", "Funded discount (−)",
     "[amount per Tribe agreement — CONFIRM]", "2200-DISC-TRIBE (Lumbee Tribe contribution — SEPARATE)",
     "Lumbee Tribe Broadband Credit  -$[x]",
     "Funded by Lumbee Tribe contributions (SR-10.2 stream 4). SEPARATE GL from USAC and RIVR. Not a "
     "federal subsidy; not claimed to USAC. Governed by the Tribe funding agreement."],

    ["DC-RIVR", "RIVR-funded affordability discount", "Funded discount (−)",
     "[amount per RIVR policy — CONFIRM]", "2300-DISC-RIVR (RIVR-funded discount — SEPARATE)",
     "RIVR Affordability Credit  -$[x]",
     "Funded by RIVR (SR-10.2 stream 3). SEPARATE GL. Internal marketing/retention discount; not a "
     "federal subsidy; not claimed to USAC."],

    ["EQ-RTR-IN", "Indoor Wi-Fi 6 router rental", "Recurring equipment charge (+)",
     "$5.00 / mo [CONFIRM — site shows conflict free vs $5, SR-8.4]", "4100-EQ-RENT (revenue — equipment rental)",
     "Wi-Fi Router Rental  $5.00",
     "Taxable TPP rental (SR-9.4). Resolve the free-vs-$5 conflict before enabling (SR-8.4)."],

    ["EQ-MESH-OUT", "Outdoor mesh Wi-Fi rental / managed Wi-Fi", "Recurring equipment charge (+)",
     "$10.00 / mo [CONFIRM, SR-8.4]", "4100-EQ-RENT (revenue — equipment rental)",
     "Outdoor Mesh Wi-Fi  $10.00",
     "Managed-Wi-Fi tax treatment is OPEN (SR-9.6) — do not set taxable until tax advisor confirms. See §3."],

    ["INS-INSTALL", "Professional installation (one-time)", "One-time charge (+)",
     "$0 promotional ($99 value) [CONFIRM, SR-8.4]", "4200-INSTALL (revenue — installation)",
     "Professional Installation  $0.00 (promo)",
     "Taxability turns on what the install attaches to (SR-9.5). One-time, not recurring."],

    ["VC-VOICE", "Residential voice add-on (optional)", "Recurring plan charge (+)",
     "[retail — from RIVR price sheet — OBTAIN, SR-8.5]", "4300-VOICE (revenue — voice)",
     "Home Phone (Unlimited)  $[x]",
     "Optional; program is broadband-first. Voice is TAXABLE and triggers 911 + USF (see §3, SR-9.3/9.7/9.8). "
     "Voice-only Lifeline = $5.25 (SR-1.2) — not used if bundled broadband credit applies."],
]
table(doc, rc_headers, rc_rows,
      widths=[0.95, 1.35, 0.9, 1.35, 1.25, 1.35, 2.1], small=True)

callout(doc,
        "Keep CR-LL-STD, CR-LL-TRB, DC-TRIBE, and DC-RIVR mapped to FOUR SEPARATE GL categories. The two "
        "federal credits are USAC pass-through contra-revenue; the Tribe and RIVR discounts are funded "
        "from different sources and must never be commingled or claimed to USAC (SR-10.2).",
        kind="note")

# ================================================================ 3. TAX TREATMENT
h1(doc, "3. Tax Treatment Configuration")
para(doc,
     "This is NOT tax advice. Every determination below requires confirmation by RIVR's tax advisor "
     "(Deliverable 13 open issue [TAX]). Configure the NISC tax engine per component; do not apply a "
     "blanket tax rule to the whole bill.")
tx_headers = ["Component", "Taxable?", "Basis", "Config note (illustrative) [CONFIRM in NISC]"]
tx_rows = [
    ["Broadband access (Senior 100/100 plan charge)", "NON-taxable",
     "Internet Tax Freedom Act — states/localities may not tax internet access; NC excludes standalone "
     "internet from taxable telecom (SR-9.1, SR-9.2)",
     "Map RC-SEN100 to a NON-TAXABLE tax category. Do NOT attach a sales-tax rule. Watch bundling: if "
     "sold with taxable components the bundle treatment may change — [CONFIRM] (SR-9.2)."],

    ["Equipment rental (router / mesh)", "TAXABLE",
     "Lease/rental of tangible personal property is taxable in NC each billing period (SR-9.4)",
     "Map EQ-RTR-IN to a TAXABLE TPP-rental category, taxed every cycle. Bundling-with-internet "
     "treatment [CONFIRM] (SR-9.4)."],

    ["Installation (one-time)", "TAXABLE-IF (fact-specific)",
     "Installation is within \"sales price\" and taxable when tied to a taxable sale / RMI; turns on "
     "what it attaches to (SR-9.5)",
     "Hold INS-INSTALL tax flag until advisor confirms whether install attaches to taxable equipment "
     "or non-taxable internet [CONFIRM] (SR-9.5)."],

    ["Managed Wi-Fi (EQ-MESH-OUT)", "OPEN — DO NOT SET",
     "Taxability is an open, fact-specific NC question (TPP rental vs. RMI service vs. nontaxable); no "
     "NCDOR ruling located (SR-9.6)",
     "Leave tax category UNSET / non-taxable placeholder and flag for tax advisor. Do not guess "
     "[CONFIRM] (SR-9.6)."],

    ["Voice (optional VC-VOICE)", "TAXABLE + surcharges",
     "NC taxes telecom/voice at 7.00% combined general rate; NC 911 = $0.70/mo per voice connection; "
     "federal USF on interstate voice revenue (SR-9.3, SR-9.7, SR-9.8)",
     "Map VC-VOICE to TAXABLE @ 7.00% [CONFIRM]; add NC 911 fee $0.70/connection as a separate "
     "regulatory line; apply USF contribution pass-through per advisor. Broadband NOT USF-assessed "
     "(SR-9.7)."],
]
table(doc, tx_headers, tx_rows, widths=[1.6, 1.15, 2.35, 2.4], small=True)

callout(doc,
        "DO NOT enable a \"plus tax\" bill line on the Senior BROADBAND plan until the tax advisor "
        "confirms which components are taxable. Broadband access itself is non-taxable under ITFA; only "
        "equipment/voice/install may be. Advertising or billing \"+ tax\" on broadband before "
        "confirmation risks an improper charge (SR-9.9).",
        kind="stop")

# ================================================================ 4. GL MAPPING
h1(doc, "4. General-Ledger Mapping")
para(doc,
     "Every code maps to a GL account that preserves the four-stream separation (SR-10.2) and creates a "
     "clean audit trail from bill line → GL → USAC reimbursement. Account numbers are ILLUSTRATIVE "
     "placeholders [CONFIRM in NISC] — Finance assigns the real chart-of-accounts values.")
gl_headers = ["Code (illustrative)", "GL account (illustrative)", "GL account name / purpose", "Funding stream (SR-10.2)"]
gl_rows = [
    ["RC-SEN100", "4000-BB-SEN", "Revenue — broadband (Senior plan)", "RIVR revenue"],
    ["EQ-RTR-IN / EQ-MESH-OUT", "4100-EQ-RENT", "Revenue — equipment rental", "RIVR revenue"],
    ["INS-INSTALL", "4200-INSTALL", "Revenue — installation (one-time)", "RIVR revenue"],
    ["VC-VOICE", "4300-VOICE", "Revenue — voice", "RIVR revenue"],
    ["CR-LL-STD", "2100-LL-USAC", "Contra-revenue — federal Lifeline credit passed to customer",
     "(1) Federal Lifeline / USAC"],
    ["CR-LL-TRB", "2101-LL-TRIBAL", "Contra-revenue — enhanced Tribal credit passed to customer",
     "(1) Federal Lifeline / USAC (Tribal)"],
    ["(receivable)", "1300-USAC-AR", "USAC reimbursement RECEIVABLE — amount claimed via LCS, awaiting "
     "cash", "(1) Federal Lifeline / USAC"],
    ["(receivable, Tribal)", "1301-USAC-AR-TRB", "USAC reimbursement receivable — enhanced Tribal "
     "portion (separate for audit)", "(1) Federal Lifeline / USAC (Tribal)"],
    ["DC-TRIBE", "2200-DISC-TRIBE", "Contra-revenue — Lumbee Tribe-funded discount", "(4) Lumbee Tribe contributions"],
    ["(receivable, Tribe)", "1320-TRIBE-AR", "RECEIVABLE from Lumbee Tribe — discounts funded but not "
     "yet settled", "(4) Lumbee Tribe contributions"],
    ["(settlement, Tribe)", "2400-TRIBE-SETTLE", "Tribe settlement / clearing — invoiced to and paid by "
     "the Tribe", "(4) Lumbee Tribe contributions"],
    ["DC-RIVR", "2300-DISC-RIVR", "Contra-revenue — RIVR-funded affordability discount (RIVR absorbs)",
     "(3) RIVR-funded discounts"],
    ["(grants, if any)", "2500-GRANT-TBCP", "Grant funds (TBCP/other) — DO NOT treat as recurring "
     "consumer subsidy unless the award authorizes it", "(2) TBCP / other grants (SR-10.1)"],
    ["Tax collected", "2600-TAX-PAYABLE", "Sales/use tax & 911 collected — remit to NCDOR / NC 911 Board",
     "(pass-through, not revenue)"],
]
table(doc, gl_headers, gl_rows, widths=[1.55, 1.35, 2.85, 1.75], small=True)

callout(doc,
        "The dedicated USAC reimbursement RECEIVABLE (1300 / 1301) is the bridge between the customer "
        "credit (contra-revenue) and the cash USAC pays. At month close, credits applied in NISC "
        "(2100/2101) must equal the LCS claim, which must equal the receivable booked (1300/1301). Tribe "
        "receivable (1320) and settlement (2400) keep Tribe-funded amounts separately invoiceable and "
        "auditable (SR-10.2).",
        kind="note")

# ================================================================ 5. CUSTOMER-FACING BILL DESCRIPTIONS
h1(doc, "5. Customer-Facing Bill Descriptions")
para(doc,
     "Exact suggested bill-line text. The bill must show the plan charge and each credit as separate, "
     "plain-language lines so the customer sees the full Lifeline benefit passed through (SR-6.8). "
     "Amounts shown as placeholders where retail is unconfirmed.")
bd_headers = ["Order", "Bill line (exact suggested text)", "Code", "Shown when"]
bd_rows = [
    ["1", "Senior 100/100 Internet …………… $[retail — from RIVR price sheet]", "RC-SEN100", "Always (plan)"],
    ["2", "Wi-Fi Router Rental ………………………… $5.00", "EQ-RTR-IN", "If equipment rented [CONFIRM 8.4]"],
    ["3", "Outdoor Mesh Wi-Fi ……………………… $10.00", "EQ-MESH-OUT", "If mesh / managed Wi-Fi"],
    ["4", "Home Phone (Unlimited) …………… $[obtain]", "VC-VOICE", "If voice add-on selected"],
    ["5", "Federal Lifeline Credit ……………… -$9.25", "CR-LL-STD",
     "Only when NV-approved AND NLAD-enrolled"],
    ["6", "Enhanced Tribal Lifeline Credit … -$25.00", "CR-LL-TRB",
     "ONLY for USAC-VERIFIED Tribal-lands addresses (see note)"],
    ["7", "Lumbee Tribe Broadband Credit …… -$[x]", "DC-TRIBE", "If Tribe-funded discount applies"],
    ["8", "RIVR Affordability Credit ……… -$[x]", "DC-RIVR", "If RIVR-funded discount applies"],
    ["9", "NC 911 Service Charge …………………… $0.70", "(voice reg)", "Voice connections only (SR-9.8)"],
    ["10", "Taxes & Fees ……………………………… $[computed]", "(tax engine)",
     "Only on taxable components — NOT broadband (SR-9.1/9.9)"],
]
table(doc, bd_headers, bd_rows, widths=[0.5, 3.35, 1.15, 2.4], small=True)

callout(doc,
        "The Enhanced Tribal Lifeline Credit line (row 6) must appear ONLY on bills for addresses "
        "verified via the USAC Tribal Lands Verification Tool with NLAD \"Lifeline Tribal Benefit?\" = "
        "Yes. Under the current working assumption there are ZERO such addresses in the Lumbee service "
        "area, so this line should not appear on any bill until an address is verified (SR-4.4, SR-5.5, "
        "SR-5.6).",
        kind="warn")

# ================================================================ 6. EFFECTIVE-DATE & PARTIAL-MONTH
h1(doc, "6. Effective-Date & Partial-Month Logic")
para(doc,
     "The Lifeline credit's NISC effective date must be tied to the NLAD enrollment date (which itself "
     "follows National Verifier approval). NISC must never apply a Lifeline credit for a period the "
     "subscriber was not NLAD-enrolled (SR-3.1, SR-3.2).")
h3(doc, "6.1 Credit effective-date rules")
bullet(doc, "Lifeline credit (CR-LL-STD / CR-LL-TRB) effective date = the NLAD enrollment effective date, "
            "which requires a prior approved National Verifier result (SR-3.1, SR-3.2). Enter the NLAD "
            "enrollment date into NISC as the credit start date [CONFIRM in NISC field name].")
bullet(doc, "Enhanced Tribal credit (CR-LL-TRB) additionally requires the USAC address verification and "
            "NLAD Tribal flag = Yes as of the effective date (SR-4.4).")
bullet(doc, "Plan charge (RC-SEN100) billing effective date = service activation / install completion "
            "date, independent of the credit date. A subscriber may be billed for service before the "
            "Lifeline credit begins if NLAD enrollment lags activation.")
h3(doc, "6.2 Partial-month proration policy")
bullet(doc, "Both the plan charge and the Lifeline credit prorate on the same basis so the pass-through "
            "stays whole. RIVR's standard proration convention applies [CONFIRM: daily proration vs. "
            "full-month]; whichever is chosen, apply it identically to charge and credit so the customer "
            "receives the full benefit for the covered days (SR-6.8).")
bullet(doc, "If a subscriber is NLAD-enrolled mid-cycle, prorate the Lifeline credit from the NLAD "
            "effective date to cycle end. Do not grant a full-month credit for a partial month of "
            "enrollment.")
bullet(doc, "If service starts mid-cycle but NLAD enrollment completes in a later cycle, the credit "
            "begins in the cycle covering the NLAD effective date — never backdated into the earlier "
            "cycle (see §7).")

# ================================================================ 7. RETROACTIVE ADJUSTMENT RESTRICTIONS
h1(doc, "7. Retroactive-Adjustment Restrictions")
callout(doc,
        "NISC must NOT apply improper retroactive Lifeline credits or retroactive Lifeline billing. A "
        "Lifeline credit may only cover periods for which the subscriber was NV-approved and NLAD-enrolled. "
        "Fabricating a backdated credit to cover a pre-enrollment period would misstate the USAC claim.",
        kind="stop")
bullet(doc, "No retroactive Lifeline credit before the NLAD enrollment effective date. Period. The credit "
            "start date is bounded by NLAD (SR-3.2).")
bullet(doc, "Subsidy reversals are FUTURE-DATED / prospective (see §8). When eligibility ends, stop the "
            "credit prospectively; do not claw back prior properly-earned credits.")
bullet(doc, "Documented exceptions only: a genuine NISC posting error (e.g., a credit keyed to the wrong "
            "account or a data-entry typo) may be corrected to align NISC with the true NLAD status. Each "
            "correction requires: (a) written reason, (b) the NLAD record it aligns to, (c) Billing "
            "Manager + Finance approval, (d) an entry in the exception log. Corrections must move NISC "
            "toward NLAD truth — never away from it.")
bullet(doc, "USAC over-claim / duplicate: if reconciliation (§10) shows a credit was claimed that should "
            "not have been, the correction is a claim adjustment / refund to USAC, not a customer "
            "clawback of a valid benefit.")

# ================================================================ 8. CREDIT REVERSAL & LOST ELIGIBILITY
h1(doc, "8. Credit Reversal & Lost-Eligibility Procedures")
para(doc,
     "When a subscriber loses eligibility, fails recertification, transfers their benefit, or requests "
     "de-enrollment, NISC must stop the Lifeline credit prospectively and the NLAD record must be updated "
     "within the required window.")
le_headers = ["Trigger", "NLAD action", "NISC action", "Timing / rule"]
le_rows = [
    ["Failed annual recertification", "De-enroll after the 60-day cure window closes with no valid "
     "response", "End CR-LL-STD/CR-LL-TRB effective the de-enrollment date; keep prior credits",
     "Subscriber has 60 days to respond or is de-enrolled (SR-3.3, SR-3.5)"],
    ["Loss of program/income eligibility", "De-enroll for ineligibility", "Stop credit prospectively "
     "from de-enrollment date; continue billing plan at retail unless another discount applies",
     "Prospective only — no clawback of valid prior credits (§7)"],
    ["One-per-household / duplicate found", "De-enroll the duplicate", "Remove the improper credit; if "
     "it was claimed, adjust the USAC claim (§10)", "De-enrollment required (SR-3.5)"],
    ["Subscriber requests cancellation", "De-enroll on request", "End credit and (if cancelling service) "
     "close the plan; final-bill proration per §6", "De-enrollment on subscriber request (SR-3.5)"],
    ["Benefit transfer to another provider", "Consent-based benefit transfer in NLAD moves the subscriber "
     "out", "End RIVR's credit as of the transfer date; the gaining provider claims thereafter",
     "One benefit per subscriber — no double claim (SR-3.6)"],
    ["Enhanced-Tribal flag becomes invalid (address change off Tribal lands / verification lapses)",
     "Update NLAD Tribal flag to No within 10 business days of the change", "End CR-LL-TRB (keep CR-LL-STD "
     "if still eligible); stop the -$25 line prospectively", "Update NLAD within 10 business days of change "
     "(SR-3.2, SR-4.4)"],
    ["Non-usage (only if service has $0 customer charge)", "De-enroll after 30-day non-use + 15-day cure",
     "N/A if Senior plan carries a >$0 charge — [CONFIRM with counsel given the ~$10 charge]",
     "Non-usage rule generally inapplicable when customer pays a fee (SR-3.4)"],
]
table(doc, le_headers, le_rows, widths=[1.9, 1.9, 2.05, 1.85], small=True)
para(doc,
     "De-enrollment handling in NISC: the credit-end date must equal the NLAD de-enrollment date; NISC "
     "must not continue a credit past de-enrollment (which would create an unsupported USAC claim). "
     "Benefit-transfer handling: on a consent-based transfer, RIVR ceases claiming for that subscriber "
     "immediately — the gaining provider owns the benefit going forward (SR-3.6).",
     size=9.5)

# ================================================================ 9. EXCEPTION REPORTS
h1(doc, "9. Standing Exception Reports")
para(doc,
     "These reports run at least monthly (several daily/weekly) to surface mismatches between NISC, NLAD, "
     "and LCS before the LCS claim is certified. Each exception routes to a named owner for clearance. "
     "Report/field names are illustrative [CONFIRM in NISC].")
ex_headers = ["Exception report", "What it catches", "Owner / action"]
ex_rows = [
    ["Lifeline credit applied but not in NLAD", "NISC shows CR-LL-STD/TRB but no matching NLAD "
     "enrollment → unsupported credit / potential improper claim", "Billing Manager — remove credit or "
     "complete NLAD enrollment before claiming"],
    ["NLAD-enrolled but no NISC credit", "Subscriber is NLAD-enrolled (RIVR is claiming or will claim) "
     "but the customer's bill shows no Lifeline credit → pass-through failure (SR-6.8)", "Billing Manager "
     "— apply the credit; the customer is owed the full benefit"],
    ["Enhanced Tribal credit on unverified address", "CR-LL-TRB present where the address is NOT "
     "USAC-verified / NLAD Tribal flag ≠ Yes (SR-4.4)", "Compliance — remove -$25 immediately; adjust "
     "claim if already claimed"],
    ["Credit greater than retail", "Total credits exceed the plan retail (credit > charge), which can "
     "signal misconfiguration or over-subsidy", "Finance — review; a Lifeline credit should not exceed "
     "the amount of the supported charge"],
    ["Duplicate household at address", "More than one Lifeline benefit at a single address without a "
     "completed one-per-household worksheet (SR-1.8)", "Compliance — resolve duplicate; de-enroll the "
     "improper benefit"],
    ["Credit continued past de-enrollment", "CR-LL still active in NISC after NLAD de-enrollment date",
     "Billing Manager — end credit as of de-enrollment date (§8)"],
    ["Recert-due within 60 days / lapsed", "Subscribers approaching or past the recertification response "
     "window (SR-3.3)", "Billing/Compliance — outreach; prepare to de-enroll uncured cases"],
    ["Credit amount ≠ rule amount", "CR-LL-STD ≠ -$9.25 or CR-LL-TRB ≠ -$25.00 (data-entry drift)",
     "Billing Manager — correct to the fixed federal amount (SR-1.1/1.3)"],
    ["NLAD update overdue (>10 business days)", "A subscriber info change not reflected in NLAD within "
     "the 10-business-day window (SR-3.2)", "Billing Manager — update NLAD"],
]
table(doc, ex_headers, ex_rows, widths=[2.15, 3.55, 2.0], small=True)

# ================================================================ 10. MONTHLY RECONCILIATION + THREE-WAY
h1(doc, "10. Monthly Reconciliation & Three-Way Reconciliation")
para(doc,
     "The monthly close proves that what NISC bills, what NLAD holds, and what LCS claims all agree — so "
     "USAC is reimbursed for exactly the benefits passed through to customers, and Tribe- and RIVR-funded "
     "amounts settle to the correct source.")

h2(doc, "10.1 Three-way reconciliation (NISC ↔ NLAD ↔ LCS)")
para(doc,
     "For every active Lifeline subscriber, the three systems must reconcile: the credit APPLIED in NISC "
     "(customer bill) ↔ the subscriber ENROLLED in NLAD ↔ the benefit CLAIMED in LCS. Any row that does "
     "not match three ways is an exception routed for correction BEFORE the 497 Officer certifies the "
     "claim (SR-6.8).")
tw_headers = ["Subscriber (acct)", "NISC credit applied", "NLAD enrolled?", "LCS claimed?",
              "Benefit type", "Match (3-way)?", "Exception / action"]
tw_rows = [
    ["1001 — J. Doe", "-$9.25", "Yes", "Yes", "Standard", "MATCH", "None"],
    ["1002 — M. Smith", "-$9.25", "Yes", "No", "Standard", "NO", "In NLAD but not claimed — add to LCS "
     "claim before certification"],
    ["1003 — A. Locklear", "-$9.25", "No", "No", "Standard", "NO", "Credit applied, not in NLAD — remove "
     "credit OR complete NLAD enrollment (§9)"],
    ["1004 — R. Oxendine", "-$34.25", "Yes (Tribal=Yes)", "Yes (Tribal)", "Enhanced Tribal", "MATCH",
     "Confirm address still USAC-verified (SR-4.4)"],
    ["1005 — T. Chavis", "-$34.25", "Yes (Tribal=No)", "Yes (standard)", "Enhanced Tribal",
     "NO", "Enhanced credit on UNVERIFIED address — remove -$25; adjust claim (§9)"],
    ["1006 — (blank)", "$0.00", "Yes", "Yes", "Standard", "NO", "NLAD-enrolled but no NISC credit — "
     "apply credit; customer owed pass-through (SR-6.8)"],
    ["…", "…", "…", "…", "…", "…", "Repeat for every active Lifeline subscriber"],
]
table(doc, tw_headers, tw_rows, widths=[1.25, 1.05, 0.95, 0.95, 1.1, 0.85, 1.55], small=True)
para(doc, "The three-way table is the certification evidence: the 497 Officer certifies the LCS claim "
          "only after every row reconciles or every exception is documented and cleared.",
     italic=True, size=9, color=GREY)

h2(doc, "10.2 Monthly close sequence")
para(doc, "Run in order each month; each step gates the next.", size=9.5)
numbered(doc, "NLAD Subscriber Snapshot on the 1st of the month — the authoritative count for the claim "
              "(SR-6.8).")
numbered(doc, "Subscriber-count reconciliation — reconcile the NLAD snapshot count against NISC active "
              "Lifeline accounts; investigate variances.")
numbered(doc, "LCS claim preparation — build the monthly claim (one per SAC) from the NLAD snapshot "
              "(SR-6.8).")
numbered(doc, "Certification by the 497 Officer — Officer certifies the claim; filed by the 8th, paid end "
              "of same month (SR-6.8).")
numbered(doc, "Compare NISC credits to NLAD and LCS — run the three-way reconciliation (§10.1); credits "
              "applied (GL 2100/2101) must equal NLAD-enrolled must equal LCS-claimed.")
numbered(doc, "Enhanced-Tribal verification pass — confirm every CR-LL-TRB row maps to a still-verified "
              "USAC address with NLAD Tribal flag = Yes (SR-4.4).")
numbered(doc, "Exceptions & corrections — clear every exception from §9 and §10.1; prospective/documented "
              "corrections only (§7).")
numbered(doc, "Cash-receipt posting — when USAC pays, post cash against the USAC receivable (GL "
              "1300/1301).")
numbered(doc, "A/R reconciliation — reconcile the USAC receivable: credits claimed vs. cash received; "
              "age and investigate any unpaid balance.")
numbered(doc, "Tribe settlement invoicing — invoice the Lumbee Tribe for Tribe-funded discounts (GL "
              "2200 → receivable 1320 → settlement 2400); keep separate from USAC (SR-10.2).")
numbered(doc, "Finance & compliance approvals — Finance and Compliance sign off on the close and the "
              "certified claim.")
numbered(doc, "Retain documentation — retain the snapshot, claim, three-way reconciliation, exceptions, "
              "and approvals ≥ 3 full preceding calendar years; eligibility docs for as long as the "
              "subscriber receives service, minimum 3 years (SR-6.11).")

h2(doc, "10.3 Standing monthly reconciliation reports")
bullet(doc, "NISC-to-NLAD subscriber reconciliation (count + line-level match).")
bullet(doc, "NLAD-to-LCS claim reconciliation (snapshot vs. certified claim).")
bullet(doc, "USAC receivable aging (claimed vs. paid, GL 1300/1301).")
bullet(doc, "Credit pass-through report (total Lifeline credits applied = total claimed = total to be "
            "reimbursed; SR-6.8).")
bullet(doc, "Tribe-funded settlement report (GL 2200/1320/2400) and RIVR-funded discount report (GL "
            "2300), each isolated by stream (SR-10.2).")

# ================================================================ 11. DATA SECURITY & ACCESS
h1(doc, "11. Data Security & Access Controls in NISC")
para(doc,
     "Lifeline processing touches sensitive personal and eligibility data. NISC configuration and IT "
     "controls must minimize what is stored, mask what is displayed, and log who touches it.")
sec_headers = ["Control", "Requirement", "Config note (illustrative) [CONFIRM in NISC]"]
sec_rows = [
    ["Data minimization", "Store only the minimum in NISC: NV/NLAD application ID, benefit type, "
     "enrollment effective date, Tribal-verification flag. NO full SSNs, eligibility documents, or "
     "tribal-roll data in NISC notes/CRM fields", "Disable free-text capture of SSN/eligibility proofs; "
     "route documents to the secure store (below)"],
    ["Masked SSN", "Any SSN reference displayed as masked (e.g., xxx-xx-1234); full SSN never rendered "
     "in NISC UI, notes, tickets, or reports", "Enable SSN masking at the field and report level; "
     "restrict unmask to no one / break-glass only"],
    ["Role-based access (RBAC)", "Least-privilege roles: Billing clerk, Billing Manager, Finance, "
     "Compliance, 497 Officer, IT admin — each sees only what the role needs; enrollment reps need Rep "
     "IDs (SR-6.6)", "Define NISC roles mapped to job function; no shared logins; quarterly access review"],
    ["Audit logs", "Immutable logs of who created/edited/removed credits, who unmasked data, who ran "
     "eligibility reports; retained per §54.417 (SR-6.11)", "Enable change auditing on rate/credit codes "
     "and on customer records; export logs to a retained store"],
    ["Secure document store", "Eligibility source documents (if any are retained at all) live only in an "
     "encrypted, access-controlled, audit-logged repository separate from NISC free text",
     "Point document workflows to the secure store; NISC holds a reference ID only"],
    ["Vendor / NISC access", "NISC (vendor) support access governed by least-privilege, logged, and "
     "time-bound; covered by the vendor DPA / confidentiality terms", "Restrict and log vendor support "
     "sessions; review vendor access in the quarterly access review"],
    ["Retention & disposal", "Retain compliance records ≥ 3 full preceding calendar years; eligibility "
     "docs for the life of service (min 3 yrs); dispose securely thereafter (SR-6.11)", "Configure "
     "retention policy and secure deletion; document the schedule"],
]
table(doc, sec_headers, sec_rows, widths=[1.6, 3.35, 2.75], small=True)

callout(doc,
        "Re-affirming §1: NEVER place full SSNs, benefit letters, income proofs, or tribal-roll / "
        "enrollment data into unsecured NISC notes or general CRM fields. Eligibility is proven and held "
        "in the National Verifier; NISC keeps only the minimal reference data. This is the single most "
        "important privacy control in the billing configuration.",
        kind="warn")

footer_revhist(doc)

doc.save(OUT)

# reload to verify
from docx import Document as _D
_re = _D(OUT)
print("OK 05")
