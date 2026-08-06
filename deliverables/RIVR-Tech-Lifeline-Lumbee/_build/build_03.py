import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from docx_helpers import *
doc = new_doc()

# ---------------------------------------------------------------------------
# COVER
# ---------------------------------------------------------------------------
cover(
    doc,
    title="Lifeline Operations Manual",
    subtitle="RIVR Tech Lifeline & Lumbee Broadband Affordability Initiative",
    deliverable_no="03 — Lifeline Operations Manual",
    owner="Compliance Officer + Program Owner",
    approvers="________________________  (Compliance Officer / date)   ________________________  (Program Owner / date)",
    version="v0.1 — DRAFT (build phase)",
    extra=("THE ONE HARD RULE. Lumbee tribal membership and residence in Robeson / Hoke / "
           "Scotland / Cumberland County do NOT qualify a customer for the enhanced $34.25 "
           "Tribal Lifeline benefit. Enhanced support requires the principal residence to be on "
           "qualifying Tribal lands per 47 C.F.R. §54.400(e), verified per-address via USAC's "
           "Tribal Lands Verification Tool (SR-4, SR-5)."),
)

toc(doc)

# ---------------------------------------------------------------------------
# 1. EXECUTIVE SUMMARY
# ---------------------------------------------------------------------------
h1(doc, "1. Executive Summary")
para(doc,
     "This Operations Manual is the day-to-day rulebook for RIVR Tech's participation in the "
     "federal Lifeline program. Lifeline is a Federal Communications Commission (FCC) universal "
     "service program, administered by the Universal Service Administrative Company (USAC), that "
     "provides a monthly discount on qualifying broadband or voice service to eligible low-income "
     "households. The standard benefit is up to $9.25/month (SR-1.1). Households whose principal "
     "residence is on qualifying Tribal lands may receive an additional $25/month, for a total of "
     "up to $34.25/month (SR-1.3). RIVR Tech intends to deliver Lifeline over its symmetrical "
     "fiber network, anchored by a proposed affordable Senior 100/100 plan (SR-8.3).")
para(doc,
     "This manual assigns responsibilities, defines the three independent compliance tests, "
     "specifies the USAC systems and filings, and states the privacy, advertising, and "
     "waste-fraud-and-abuse controls every employee and contractor must follow. It is a "
     "build-phase document: RIVR Tech is not yet an ETC and has not completed USAC onboarding "
     "(SR-7.4). Nothing here authorizes marketing as an approved Lifeline provider until the "
     "final NCUC ETC order issues and USAC onboarding is complete.")
callout(doc,
        "THE ONE HARD RULE. Lumbee tribal membership and residence in Robeson / Hoke / Scotland / "
        "Cumberland County do NOT qualify a customer for the enhanced $34.25 Tribal Lifeline "
        "benefit. Enhanced support requires the principal residence to be on qualifying Tribal "
        "lands per 47 C.F.R. §54.400(e), verified per-address via USAC's Tribal Lands "
        "Verification Tool (SR-4, SR-5). Working assumption until a written legal/USAC "
        "determination says otherwise: the Lumbee have no reservation, no land in trust, and no "
        "§54.412 designation, so the number of enhanced-benefit-qualifying subscribers is 0 "
        "(SR-5.5).",
        kind="warn")

# ---------------------------------------------------------------------------
# 2. GOVERNANCE & ROLES
# ---------------------------------------------------------------------------
h1(doc, "2. Program Governance & Roles")
para(doc,
     "Lifeline compliance is a shared responsibility, but every control has a single named owner. "
     "The table below maps each role to its Lifeline responsibilities. Officer certifications "
     "(Forms 481, 498, 555, and the monthly LCS claim) are personal attestations under penalty of "
     "law and may not be delegated below the certifying officer (SR-6.5, SR-6.8, SR-6.9, SR-6.10).")
table(doc,
      ["Role", "Lifeline responsibilities"],
      [
        ["Executive Sponsor", "Owns the program mandate and budget; accountable to ownership/board; approves go/no-go at each phase gate; ensures resourcing for compliance."],
        ["Program Owner", "Runs the program end-to-end; owns this manual, phase-gate schedule, and cross-functional coordination; co-owner of sign-off with Compliance Officer."],
        ["Compliance Officer", "Owns Lifeline rule compliance; maintains the Source Register (00); approves customer-facing claims; owns recert/de-enrollment discipline, WFA controls, and audit readiness. Co-signs this manual."],
        ["Regulatory Counsel", "Owns FCC/USAC/NCUC legal interpretation; issues the written §54.400(e)/§54.412 Tribal-lands determination; reviews advertising and material claims; escalation point for gray areas."],
        ["Finance", "Owns USF reimbursement forecasting and the four-stream funding separation (SR-10.2); reconciles USAC disbursements; monitors budget vs. actuals."],
        ["Accounting", "Maintains separate GL categories for Lifeline / grants / RIVR discounts / Tribe contributions (SR-10.2); books USAC receipts; supports Form 481/555 revenue reporting."],
        ["Billing", "Applies the correct Lifeline discount to enrolled subscribers only (NLAD-confirmed); ensures full pass-through of the benefit; prevents double-discounting; handles proration and de-enrollment billing changes."],
        ["IT", "Owns USAC system access provisioning (One Portal, NV, NLAD, LCS, RAD), role-based access controls, secure eligibility-document storage, audit logs, and NLAD 10-business-day update integration (SR-3.2, SR-6.7)."],
        ["Customer Service", "Handles enrollment support, recertification outreach, transfer/dispute handling, and de-enrollment notices; trained never to promise the enhanced benefit or guarantee approval."],
        ["Sales / Enrollment Reps", "Each rep self-registers for a RAD Rep ID before enrolling anyone (SR-6.6); collects consent; initiates National Verifier checks; never enrolls before an approved NV result (SR-3.1)."],
        ["Marketing", "Executes the §54.405(b) advertising obligation (SR-6.12); ensures no prohibited claims (Section 10); routes all Lifeline/Tribal messaging through Compliance + Counsel."],
        ["Network Operations", "Delivers and maintains service meeting minimum service standards (SR-2); provisions the Senior 100/100 plan; supports non-usage determinations where applicable."],
        ["Lumbee Tribe Representatives", "Partner on outreach to likely-eligible members; provide culturally appropriate education; help fund Tribe-sponsored discounts (a separate funding stream, SR-10.2). Not a substitute for federal eligibility verification."],
        ["Internal Audit", "Independently tests enrollment, recert, claims, and record-retention controls; verifies claims match NLAD; reports findings to Executive Sponsor; supports USAC audits."],
      ],
      widths=[1.9, 4.6])

# ---------------------------------------------------------------------------
# 3. THE THREE (FOUR) SEPARATE COMPLIANCE TESTS
# ---------------------------------------------------------------------------
h1(doc, "3. The Separate Compliance Tests (CRITICAL)")
para(doc,
     "The single most important operational concept in this program: eligibility is decided by "
     "several INDEPENDENT tests. Passing one says nothing about the others. In particular, "
     "standard Lifeline eligibility, enhanced Tribal eligibility, Lumbee membership, and senior "
     "status are four separate things. An employee who conflates them will cause improper claims, "
     "USAC recovery, and reputational harm. Read the table below as four locked doors, each with "
     "its own key.", bold=True)
table(doc,
      ["Test", "What it establishes", "How verified", "What it does NOT establish"],
      [
        ["(a) Standard Lifeline eligibility",
         "The household qualifies for the standard up-to-$9.25/mo benefit via income (≤135% FPG) or a qualifying program (SR-1.4, SR-1.6, SR-1.7).",
         "National Verifier approval (identity, address, program/income, duplicate check) BEFORE enrollment (SR-3.1).",
         "Does NOT establish Tribal-lands residence, does NOT establish the enhanced $25, does NOT establish Lumbee membership."],
        ["(b) Enhanced Tribal eligibility",
         "The household's principal residence is physically ON qualifying Tribal lands, unlocking the additional up-to-$25/mo (total up to $34.25) (SR-1.3, SR-4.2).",
         "Per-address check against USAC's Tribal Lands Verification Tool; NLAD Tribal flag set to Yes only for verified addresses (SR-4.4). Written legal/USAC determination required first.",
         "Does NOT follow from tribal membership, county of residence, or any tribal program. Address-based only."],
        ["(c) Lumbee tribal membership",
         "The customer is an enrolled member of the Lumbee Tribe — relevant to OUTREACH and Tribe-funded discounts only.",
         "Lumbee Tribal enrollment records, handled by the Tribe. Used for outreach targeting and Tribe-funded benefits, not federal Lifeline.",
         "Does NOT confer standard Lifeline, does NOT confer the enhanced Tribal benefit, does NOT verify income or Tribal-lands residence (SR-5.6)."],
        ["(d) Senior status (age)",
         "The customer meets an age threshold — relevant to the marketing name of the Senior 100/100 plan only.",
         "Age documentation for RIVR's own plan targeting (if used at all).",
         "Age ALONE is NOT a Lifeline qualifier. Seniors must still pass test (a) via income or a qualifying program. There is no automatic senior Lifeline."],
      ],
      widths=[1.5, 1.9, 1.9, 1.9], small=True)
callout(doc,
        "These four tests are independent. Never say 'you're a Lumbee senior in Robeson County, so "
        "you qualify.' Each door needs its own key: (a) National Verifier, (b) the Tribal Lands "
        "Verification Tool, (c) Tribal enrollment records (outreach only), (d) age (marketing "
        "only). Confusing them is the program's top compliance risk.",
        kind="stop")

# ---------------------------------------------------------------------------
# 4. STANDARD LIFELINE ELIGIBILITY
# ---------------------------------------------------------------------------
h1(doc, "4. Standard Lifeline Eligibility")
h2(doc, "4.1 Income-based path")
para(doc,
     "A household qualifies on income if its total household income is at or below 135% of the "
     "Federal Poverty Guidelines (FPG) (SR-1.4). The 2026 dollar thresholds below are illustrative "
     "and must be confirmed against the live USAC Income Requirements PDF before use (SR-1.5) "
     "[CONFIRM].")
table(doc,
      ["Household size", "135% FPG annual income (48 states / DC) [CONFIRM]"],
      [["1 person", "$21,546"],
       ["2 people", "$29,214"],
       ["3 people", "$36,882"],
       ["4 people", "$44,550"],
       ["Each additional person / AK & HI", "Higher — see live USAC PDF [CONFIRM]"]],
      widths=[3.0, 3.5])
para(doc,
     "Income is documented with the proofs the National Verifier accepts (e.g., prior-year tax "
     "return, current income statements, or three consecutive months of pay stubs). RIVR staff do "
     "not adjudicate income themselves — the National Verifier does (SR-3.1).",
     italic=True, size=9.5)

h2(doc, "4.2 Program-based path")
para(doc,
     "A household also qualifies if any member participates in a qualifying federal program "
     "(SR-1.6). Enrollment in one of these is sufficient; income need not also be checked.")
table(doc,
      ["Qualifying program", "Category", "Benefit tier"],
      [
        ["Medicaid", "Federal program (SR-1.6)", "Standard Lifeline"],
        ["Supplemental Nutrition Assistance Program (SNAP)", "Federal program (SR-1.6)", "Standard Lifeline"],
        ["Supplemental Security Income (SSI)", "Federal program (SR-1.6)", "Standard Lifeline"],
        ["Federal Public Housing Assistance (FPHA)", "Federal program (SR-1.6)", "Standard Lifeline"],
        ["Veterans & Survivors Pension Benefit", "Federal program (SR-1.6)", "Standard Lifeline"],
        ["Bureau of Indian Affairs (BIA) General Assistance", "Tribal-specific program (SR-1.7)", "Standard Lifeline ONLY"],
        ["Tribal TANF", "Tribal-specific program (SR-1.7)", "Standard Lifeline ONLY"],
        ["Head Start (income-qualifying only)", "Tribal-specific program (SR-1.7)", "Standard Lifeline ONLY"],
        ["Food Distribution Program on Indian Reservations (FDPIR)", "Tribal-specific program (SR-1.7)", "Standard Lifeline ONLY"],
      ],
      widths=[3.2, 2.1, 1.5], small=True)
callout(doc,
        "The four Tribal-specific programs (BIA General Assistance, Tribal TANF, income-qualifying "
        "Head Start, FDPIR) qualify a person for STANDARD Lifeline only. They do NOT establish "
        "Tribal-lands residence and do NOT unlock the enhanced $25 benefit (SR-1.7). Enhanced "
        "support is address-based and address-based only (see Section 5).",
        kind="warn")

h2(doc, "4.3 One benefit per household")
para(doc,
     "Only one Lifeline benefit is allowed per household (SR-1.8). A 'household' is everyone living "
     "together at one address who shares income and expenses as a single economic unit. Adults at "
     "the same address who are financially independent (separate income and expenses) may be "
     "separate households — documented with USAC's one-per-household worksheet where multiple "
     "households share an address (SR-1.8).")

h2(doc, "4.4 National Verifier gate")
callout(doc,
        "No enrollment before an approved National Verifier result. The NV checks identity, "
        "address, program/income eligibility, and duplicates. NLAD enrollment happens only after "
        "NV approval (SR-3.1, SR-3.2). This gate is absolute.",
        kind="stop")

# ---------------------------------------------------------------------------
# 5. ENHANCED TRIBAL LIFELINE
# ---------------------------------------------------------------------------
h1(doc, "5. Enhanced Tribal Lifeline (Address-Based)")
callout(doc,
        "STOP. Do not apply, claim, or advertise the enhanced $25 / $34.25 benefit for ANY RIVR "
        "subscriber until Regulatory Counsel and USAC have issued a written determination that a "
        "specific address is on qualifying Tribal lands. Working assumption today: 0 qualifying "
        "subscribers (SR-5.5). Claiming the enhanced benefit without an on-Tribal-lands address is "
        "an improper claim subject to USAC recovery and penalties.",
        kind="stop")
h2(doc, "5.1 What counts as 'Tribal lands'")
para(doc,
     "'Tribal lands' for Lifeline is a defined, enumerated term (SR-4.1): a federally recognized "
     "tribe's reservation, pueblo, or colony (including former reservations in Oklahoma); Alaska "
     "Native regions established under ANCSA; Indian allotments; Hawaiian Home Lands; AND any land "
     "the FCC designates as Tribal lands through the §54.412 process. If land does not fall into "
     "one of those buckets, it is not Tribal lands for Lifeline purposes.")
h2(doc, "5.2 The test is the address, not the person")
para(doc,
     "The enhanced benefit requires the subscriber to be an 'eligible resident of Tribal lands' — "
     "meaning the principal residence is physically ON qualifying Tribal lands (SR-4.2). It is not "
     "conferred by tribal membership, by ethnicity, or by living in a county associated with a "
     "tribe. Two members of the same tribe can get different answers depending solely on where "
     "each one lives.")
h2(doc, "5.3 The §54.412 designation process")
para(doc,
     "Land outside the enumerated categories becomes Lifeline 'Tribal lands' only if the FCC "
     "(Wireline Competition Bureau together with the Office of Native Affairs and Policy) formally "
     "designates it, and only upon a request from a duly authorized official of the federally "
     "recognized Tribe (SR-4.3). This is a deliberate regulatory process, not an automatic "
     "consequence of recognition.")
h2(doc, "5.4 USAC Tribal Lands Verification Tool")
para(doc,
     "Verification is per-address: USAC's Tribal Lands Verification Tool checks a specific street "
     "address (or lat/long) against the qualifying-lands dataset. The NLAD 'Lifeline Tribal "
     "Benefit?' flag is set to Yes only for addresses the tool verifies; the AMS error path "
     "requires coordinates to validate (SR-4.4). No verified address means no enhanced flag.")
h2(doc, "5.5 Lumbee status specifically")
para(doc,
     "The Lumbee Tribe received full federal recognition via Public Law 119-60, enacted as §8803 "
     "of the NDAA for FY2026 (139 Stat. 1973), signed December 18, 2025 (SR-5.1); the Department "
     "of the Interior added the Lumbee to the official federally recognized list around January "
     "30, 2026 (SR-5.2). Recognition is real and significant — but for Lifeline it does not, by "
     "itself, create Tribal lands. The law authorizes (does not execute) land-into-trust, with "
     "Robeson County trust applications to be treated as 'on reservation' under 25 C.F.R. part "
     "151 — a future pathway, not an existing reservation (SR-5.3). The four-county area (Robeson, "
     "Cumberland, Hoke, Scotland) is a service delivery area for federal services, which is NOT "
     "'Tribal lands' under §54.400(e) (SR-5.4).")
table(doc,
      ["Question", "Current answer", "Source"],
      [
        ["Is the Lumbee Tribe federally recognized?", "Yes — PL 119-60 / §8803 NDAA FY2026, signed Dec 18, 2025.", "SR-5.1, SR-5.2"],
        ["Does the Lumbee Tribe have a reservation?", "No reservation today.", "SR-5.5"],
        ["Any Lumbee land held in trust?", "None yet; land-into-trust is authorized, not executed. [CONFIRM with BIA]", "SR-5.3, SR-5.5"],
        ["Any FCC §54.412 designation for Lumbee land?", "None found. [CONFIRM with USAC / FCC ONAP]", "SR-5.5"],
        ["Do the four counties qualify as Tribal lands?", "No — a service delivery area is not §54.400(e) Tribal lands.", "SR-5.4"],
        ["Qualifying enhanced-benefit subscribers today?", "Working assumption: 0, until a written determination says otherwise.", "SR-5.5"],
      ],
      widths=[2.6, 2.9, 1.0], small=True)
callout(doc,
        "Require a written legal/USAC determination before any enhanced claim. Until Regulatory "
        "Counsel confirms in writing that a specific address satisfies §54.400(e) (or that a "
        "§54.412 designation or trust acquisition has occurred), every RIVR subscriber is treated "
        "as standard-Lifeline-only (SR-5.6).",
        kind="warn")

# ---------------------------------------------------------------------------
# 6. MINIMUM SERVICE STANDARDS
# ---------------------------------------------------------------------------
h1(doc, "6. Minimum Service Standards")
para(doc,
     "A Lifeline-supported fixed broadband service must meet the FCC's current minimum service "
     "standards. RIVR's symmetrical fiber comfortably exceeds them.")
table(doc,
      ["Standard", "FCC minimum", "RIVR Senior 100/100 plan", "Source"],
      [
        ["Fixed broadband speed", "25 / 3 Mbps", "100 / 100 Mbps — exceeds", "SR-2.1"],
        ["Fixed broadband data allowance", "1,280 GB / month", "Unlimited / no cap — exceeds", "SR-2.2"],
        ["Mobile broadband data (N/A to fixed fiber)", "4.5 GB / month (increase paused through Dec 1, 2026)", "N/A — fixed service", "SR-2.3"],
      ],
      widths=[1.9, 2.0, 1.8, 0.8], small=True)
callout(doc,
        "ACP has ENDED. The Affordable Connectivity Program (ACP) stopped funding new benefits on "
        "June 1, 2024. ACP is a separate, now-terminated program — never present it as active, and "
        "never conflate the Lifeline benefit with ACP in any customer-facing material.",
        kind="warn")

# ---------------------------------------------------------------------------
# 7. USAC SYSTEMS OVERVIEW
# ---------------------------------------------------------------------------
h1(doc, "7. USAC Systems Overview")
h2(doc, "7.1 National Verifier (NV)")
para(doc,
     "The National Verifier is the eligibility engine. Before any subscriber is enrolled, the NV "
     "checks identity, address, program/income eligibility, and duplicates and returns an approved "
     "or denied result. Enrollment cannot proceed without an approved NV result (SR-3.1).")
h2(doc, "7.2 National Lifeline Accountability Database (NLAD)")
para(doc,
     "NLAD is the enrollment and duplicate-prevention database. RIVR enrolls a subscriber in NLAD "
     "only after an approved NV result, and must update NLAD within 10 business days of any change "
     "to subscriber information (SR-3.2). NLAD also carries the 'Lifeline Tribal Benefit?' flag "
     "(Section 5.4) and supports consent-based benefit transfers when a subscriber moves from "
     "another provider (SR-3.6).")
h2(doc, "7.3 Lifeline Claims System (LCS)")
para(doc,
     "LCS is where RIVR files its monthly reimbursement claim — one claim per Study Area Code "
     "(SAC), built from the NLAD Subscriber Snapshot taken on the 1st of the month. Certified "
     "claims filed by the 8th are paid at the end of the same month; the 497 Officer certifies. "
     "The legacy Form 497 is retired (SR-6.8).")
h2(doc, "7.4 Representative Accountability Database (RAD)")
para(doc,
     "Every enrollment representative must self-register at LifelineRAD.org for a unique Rep ID "
     "before enrolling any subscriber (SR-6.6). The Rep ID ties each enrollment to an accountable "
     "individual and is a front-line waste-fraud-and-abuse control.")

# ---------------------------------------------------------------------------
# 8. RECERTIFICATION & DE-ENROLLMENT
# ---------------------------------------------------------------------------
h1(doc, "8. Recertification & De-Enrollment")
para(doc,
     "Every Lifeline subscriber must be recertified annually to confirm continued eligibility "
     "(SR-3.3). If the automated data-source check fails, the subscriber has 60 days to respond "
     "with proof; failure to respond within the window results in de-enrollment (SR-3.3).")
table(doc,
      ["Event", "Rule", "Action", "Source"],
      [
        ["Annual recertification", "Required every year for each subscriber.", "USAC or RIVR initiates; confirm continued eligibility.", "SR-3.3"],
        ["Failed data-source check", "Subscriber has a 60-day window to respond.", "Send notice; collect proof; de-enroll if no timely response.", "SR-3.3"],
        ["Non-usage (fee-free services only)", "30 consecutive days non-use → 15-day cure notice → terminate if uncured.", "Applies only where the subscriber pays $0. [CONFIRM with counsel given the $10 charge — a >$0 charge generally means the non-usage rule does not apply.]", "SR-3.4"],
        ["De-enrollment triggers", "Failure to recertify; one-per-household failure; duplicate; ineligibility; or subscriber request.", "De-enroll in NLAD; stop claiming; adjust billing.", "SR-3.5"],
        ["Benefit transfer", "Subscriber already in NLAD with another provider.", "Consent-based benefit transfer in NLAD (not a new enrollment).", "SR-3.6"],
      ],
      widths=[1.6, 2.1, 2.0, 0.8], small=True)
callout(doc,
        "[CONFIRM] Non-usage rule applicability. The non-usage rule applies only to services with "
        "no monthly fee to the subscriber. If the Senior plan carries a >$0 customer charge (e.g., "
        "the referenced $10 charge), the non-usage rule generally does not apply — confirm with "
        "Regulatory Counsel before implementing any non-usage de-enrollment (SR-3.4).",
        kind="note")

# ---------------------------------------------------------------------------
# 9. ONE-LIFELINE-PER-HOUSEHOLD CONTROLS
# ---------------------------------------------------------------------------
h1(doc, "9. One-Lifeline-Per-Household Controls")
para(doc,
     "Only one Lifeline benefit per household is permitted (SR-1.8). RIVR enforces this at "
     "enrollment and on an ongoing basis:")
bullet(doc, "Rely on the National Verifier and NLAD duplicate checks at enrollment — the NV screens for duplicates before any enrollment is allowed (SR-3.1, SR-3.2).")
bullet(doc, "Apply the economic-unit definition: a household is everyone at one address sharing income and expenses; financially independent adults at a shared address may be separate households (SR-1.8).")
bullet(doc, "Use USAC's one-per-household worksheet whenever multiple households share a single address, and retain it with the subscriber's eligibility record (SR-1.8).")
bullet(doc, "Train enrollment reps that a second benefit to the same economic unit is prohibited and is a de-enrollment trigger (SR-3.5).")
bullet(doc, "Never claim reimbursement for a subscriber flagged as a duplicate; resolve through NLAD dispute resolution (SR-3.6).")

# ---------------------------------------------------------------------------
# 10. ADVERTISING
# ---------------------------------------------------------------------------
h1(doc, "10. Advertising Obligation & Prohibited Claims")
h2(doc, "10.1 The advertising obligation")
para(doc,
     "As an ETC, RIVR must publicize the availability of Lifeline service in a manner reasonably "
     "designed to reach those likely to qualify (§54.405(b), SR-6.12). This is an affirmative "
     "obligation, not merely a courtesy: outreach materials, in Tribal-community-appropriate "
     "channels, are part of compliance.")
h2(doc, "10.2 Prohibited advertising claims")
para(doc,
     "The following statements are FALSE and are prohibited in any RIVR advertising, sales script, "
     "social post, flyer, or verbal representation. Each is corrected below.", bold=True)
table(doc,
      ["Prohibited claim (do NOT say this)", "Why it is false / the correct statement"],
      [
        ["\"Every Lumbee member receives $34.25.\"", "False. The enhanced $34.25 requires an address on qualifying Tribal lands; membership alone confers nothing (SR-4.2, SR-5.6). Working assumption today: 0 qualifying subscribers."],
        ["\"All four counties are Tribal lands.\"", "False. Robeson/Cumberland/Hoke/Scotland form a service delivery area, which is NOT §54.400(e) Tribal lands (SR-5.4)."],
        ["\"All seniors automatically qualify.\"", "False. Age alone is not a Lifeline qualifier; seniors must pass income or program eligibility via the National Verifier (Section 3(d), SR-1.4/1.6)."],
        ["\"The Tribe guarantees approval.\"", "False. Eligibility is determined by the National Verifier and USAC systems, not by the Tribe. No one can guarantee approval."],
        ["\"You can get multiple Lifeline benefits.\"", "False. One Lifeline benefit per household (SR-1.8)."],
        ["\"Lifeline is the same as ACP.\"", "False. ACP is a separate program that ended June 1, 2024; Lifeline is a distinct, ongoing program (Section 6)."],
      ],
      widths=[2.7, 3.8], small=True)
callout(doc,
        "All Lifeline and Tribal-benefit messaging must be reviewed and approved by the Compliance "
        "Officer and Regulatory Counsel before publication. Reps may not improvise eligibility "
        "promises.",
        kind="warn")

# ---------------------------------------------------------------------------
# 11. RECORD RETENTION
# ---------------------------------------------------------------------------
h1(doc, "11. Record Retention")
para(doc,
     "Under §54.417, RIVR must retain Lifeline compliance records for at least the three full "
     "preceding calendar years, and must retain subscriber-eligibility documentation for as long "
     "as the subscriber receives Lifeline-supported service, subject to a minimum of three years "
     "(SR-6.11).")
callout(doc,
        "Retention is ≥ 3 years / duration of service — NOT 10 years. The 10-year requirement is a "
        "separate high-cost rule (§54.320) that does not apply to Lifeline records. Do not "
        "over-retain or under-retain; follow §54.417 (SR-6.11).",
        kind="note")
table(doc,
      ["Record type", "Minimum retention", "Source"],
      [
        ["Subscriber eligibility documentation", "Duration of service, minimum 3 years", "SR-6.11 (§54.417)"],
        ["Enrollment / NV approval records", "≥ 3 full preceding calendar years", "SR-6.11"],
        ["Recertification records", "≥ 3 full preceding calendar years", "SR-6.11"],
        ["One-per-household worksheets", "With the subscriber record (duration of service, min 3 yrs)", "SR-1.8, SR-6.11"],
        ["Claims / LCS support", "≥ 3 full preceding calendar years", "SR-6.11"],
      ],
      widths=[2.6, 3.0, 0.9], small=True)

# ---------------------------------------------------------------------------
# 12. ANNUAL FILINGS
# ---------------------------------------------------------------------------
h1(doc, "12. Annual Filings")
table(doc,
      ["Filing", "What it is", "Due", "Where / how", "Source"],
      [
        ["FCC Form 481", "Carrier Annual Report, filed per SAC; officer certification required.", "July 1 [CONFIRM current-year deadline; FCC has waived/extended some years].", "USAC / One Portal.", "SR-6.9"],
        ["FCC Form 555", "Annual Lifeline ETC Certification (recertification results), per SAC.", "January 31.", "One Portal + ECFS Docket 14-171 + state commission (NCUC) + relevant Tribal governments.", "SR-6.10"],
      ],
      widths=[1.1, 2.2, 1.4, 1.9, 0.7], small=True)
callout(doc,
        "[CONFIRM] the current-year Form 481 deadline. The FCC has waived or extended the July 1 "
        "date in some years — verify the live deadline before filing (SR-6.9).",
        kind="note")

# ---------------------------------------------------------------------------
# 13. PRIVACY & INFORMATION SECURITY
# ---------------------------------------------------------------------------
h1(doc, "13. Privacy & Information Security")
para(doc,
     "Lifeline enrollment collects sensitive personal information — identity data, addresses, "
     "income and program-participation proofs, and, for outreach, Tribal-enrollment status. RIVR "
     "treats this data as high-sensitivity and applies the following controls. These controls are "
     "mandatory for every employee, contractor, and vendor.")
h2(doc, "13.1 Collection & consent")
bullet(doc, "Collect written, informed customer consent before initiating a National Verifier check or sharing data with USAC (SR-3.1).")
bullet(doc, "Data minimization: collect only what is required to establish eligibility and provide service — nothing more.")
bullet(doc, "State the purpose of collection at the point of collection; do not collect eligibility data for any undisclosed purpose.")
h2(doc, "13.2 Storage & access")
bullet(doc, "Never place full Social Security Numbers, eligibility documents, or Tribal-roll information in unsecured notes, email bodies, chat, or general CRM free-text fields.")
bullet(doc, "Store eligibility documents only in the designated secure, access-controlled document store (IT-managed), never on local drives or personal devices.")
bullet(doc, "Enforce role-based access control: each USAC system role (NV, NLAD, LCS, RAD) is provisioned to named individuals with the minimum access needed; sales reps use the 'NV-Only' ETC Agent role (SR-6.7).")
bullet(doc, "Maintain audit logs of who accessed which subscriber record and when; review logs periodically for anomalous access.")
h2(doc, "13.3 Use limitations")
bullet(doc, "Prohibition on secondary use: eligibility data (income, program participation, Tribal status) must NEVER be used for unrelated marketing, cross-sell, or list-building.")
bullet(doc, "Tribal-enrollment status may be used for Lifeline outreach and Tribe-funded benefits only, and only with appropriate consent and Tribe coordination.")
h2(doc, "13.4 Retention, destruction & incident response")
bullet(doc, "Follow the §54.417 retention schedule (Section 11); do not keep eligibility documents longer than required (SR-6.11).")
bullet(doc, "Securely destroy documents (shredding / cryptographic erasure) at end of the retention period, with a destruction log.")
bullet(doc, "Incident response: any suspected loss or unauthorized disclosure of subscriber data is reported immediately to the Compliance Officer and IT; contain, assess, notify per applicable law, and document. [CONFIRM breach-notification obligations with Regulatory Counsel.]")
h2(doc, "13.5 People & vendors")
bullet(doc, "All employees and contractors with data access sign a confidentiality agreement and complete privacy training before access is granted.")
bullet(doc, "Vendor access controls: any vendor touching subscriber data is bound by a written data-protection agreement, granted least-privilege access, and monitored; access is revoked promptly at offboarding.")

# ---------------------------------------------------------------------------
# 14. WASTE, FRAUD & ABUSE
# ---------------------------------------------------------------------------
h1(doc, "14. Waste, Fraud & Abuse (WFA) Policy")
para(doc,
     "Lifeline reimbursement comes from the federal Universal Service Fund. Improper claims are "
     "subject to recovery, penalties, and program bars. RIVR maintains a zero-tolerance WFA "
     "posture built on the following controls.")
bullet(doc, "Enrollment gate: never enroll before an approved National Verifier result; never claim for a subscriber not currently enrolled in NLAD (SR-3.1, SR-6.8).")
bullet(doc, "Claim integrity: the monthly LCS claim is built strictly from the NLAD Subscriber Snapshot; RIVR claims only for NLAD-enrolled subscribers, one benefit per household (SR-6.8, SR-1.8).")
bullet(doc, "Duplicate prevention: rely on NV/NLAD duplicate screening; resolve flagged duplicates through NLAD dispute resolution before claiming (SR-3.2, SR-3.6).")
bullet(doc, "Enhanced-benefit discipline: claim the enhanced $25 only for addresses verified on Tribal lands with a written determination — otherwise treat as standard-only (Section 5, SR-5.6).")
bullet(doc, "Rep accountability: every enrollment is tied to a registered RAD Rep ID; falsified enrollments are grounds for termination and referral (SR-6.6).")
bullet(doc, "Officer certifications: Forms 481, 498, 555, and the monthly LCS claim are certified personally by the responsible officer under penalty of law; certifiers review supporting data before signing (SR-6.5, SR-6.8, SR-6.9, SR-6.10).")
bullet(doc, "Funding separation: keep the four funding streams (federal Lifeline, TBCP/grants, RIVR-funded discounts, Lumbee Tribe contributions) in separate GL categories; no commingling (SR-10.2).")
bullet(doc, "Internal audit: Internal Audit independently tests enrollment, recertification, claims, and retention controls; verifies claims reconcile to NLAD; and reports findings to the Executive Sponsor.")
bullet(doc, "Whistleblower path: employees may report suspected WFA to the Compliance Officer confidentially and without retaliation.")
callout(doc,
        "Golden rule of claims: if the subscriber is not currently enrolled in NLAD with an "
        "approved NV result, RIVR does not claim reimbursement for them — period. Enhanced-benefit "
        "claims additionally require a written on-Tribal-lands determination.",
        kind="stop")

# ---------------------------------------------------------------------------
footer_revhist(doc)

out = "/home/user/claude-skills/deliverables/RIVR-Tech-Lifeline-Lumbee/03_Lifeline_Operations_Manual.docx"
doc.save(out)

# reload to confirm it opens
from docx import Document as _D
_D(out)
print("OK 03")
