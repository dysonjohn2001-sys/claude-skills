# -*- coding: utf-8 -*-
"""Builds the 4 Word deliverables for the Blanket Protection Plan analysis."""
import os
import sys

# reuse the docx helper library from the first project, patched to this content module
FIRST = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..",
                                     "RIVR_Tech_Maintenance_Plan", "08_Source_Files", "build_scripts"))
sys.path.insert(0, FIRST)
sys.path.insert(0, os.path.dirname(__file__))

import blanket_content as C
import docx_helpers as H
# Patch the helper module to use blanket_content's constants + brand
H.C = C
H.BRAND = C.BRAND
from docx_helpers import (new_doc, cover_page, toc_field, h1, h2, h3, para, bullet,
                          numbered, callout, table, save, _hr)

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CPC = C.cost_per_call()
PM_A = C.per_member(C.PRICE_A)
PM_B = C.per_member(C.PRICE_B)
BE_A = C.breakeven_util(C.PRICE_A)
BE_B = C.breakeven_util(C.PRICE_B)
OFF_A = C.churn_offset_pct(C.PRICE_A, C.A["current_subs"], 1.0, churn_base="all")
OFF_B = C.churn_offset_pct(C.PRICE_B, C.A["current_subs"], 1.0, churn_base="all")
WS = C.weighted_scores()
BROW = C.breakeven_calls(C.PRICE_A, C.A["current_subs"])
BROWB = C.breakeven_calls(C.PRICE_B, C.A["current_subs"])
FIVEYR = C.five_year(C.PRICE_A, C.A["current_subs"], 0.35, a={**C.A, "incr_churn_annual": 0.0})


def p(*parts):
    return os.path.join(BASE, *parts)


# ==========================================================================
# 1. EXECUTIVE DECISION MEMO
# ==========================================================================
def memo():
    doc = new_doc()
    cover_page(doc, "Blanket Residential Maintenance Protection Plan",
               "Executive Decision Memo",
               "Should RIVR Tech introduce a $3.99 or $4.99 monthly plan for all residential customers?")
    toc_field(doc)

    h1(doc, "1. Purpose & Question")
    para(doc, f"This memo evaluates whether {C.COMPANY_SHORT} should introduce a blanket monthly "
              f"Maintenance Protection Plan for all residential internet customers at either "
              f"$3.99 (Scenario A) or $4.99 (Scenario B) per month, and whether it should be "
              f"structured as mandatory, automatic-with-opt-out, or voluntary opt-in. Analysis "
              f"uses a starting base of {C.A['current_subs']:,} residential subscribers (editable) "
              f"and industry planning assumptions where RIVR Tech data is not yet available.")
    callout(doc, "BOTTOM LINE", "Do NOT implement a mandatory blanket fee. Offer the plan as a "
            f"VOLUNTARY opt-in at $3.99 (Standard coverage), delivered as a HYBRID with a "
            f"per-visit dispatch charge for customers who decline. Exempt Lifeline, Tribal "
            f"Lifeline, and low-income customers (opt-in only); exclude bulk/managed properties. "
            f"Pilot before any system-wide launch.", "recommendation")

    h1(doc, "2. Business Case")
    para(doc, f"{C.COMPANY_SHORT} does not routinely charge residential customers for service "
              f"calls, even when the cause is customer equipment, wiring, damage, misuse, or Wi-Fi "
              f"placement. A protection plan could recover some of that cost, smooth maintenance "
              f"expense, and reduce per-visit billing disputes. The economics are attractive on "
              f"paper — but the decision is dominated by customer trust, churn, and regulatory "
              f"risk, not by gross revenue.")
    para(doc, "Per-covered-member economics (at expected 15% utilization):", bold=True)
    table(doc, ["Metric", "$3.99 (A)", "$4.99 (B)"], [
        ("Plan revenue / member / yr", C.money2(PM_A["rev"]), C.money2(PM_B["rev"])),
        ("Covered + call-center + admin + bad debt", C.money2(PM_A["rev"]-PM_A["contribution"]), C.money2(PM_B["rev"]-PM_B["contribution"])),
        ("Contribution / member / yr", C.money2(PM_A["contribution"]), C.money2(PM_B["contribution"])),
        ("Contribution margin", f"{PM_A['margin_pct']*100:.0f}%", f"{PM_B['margin_pct']*100:.0f}%"),
        ("Break-even utilization", f"{BE_A*100:.0f}%", f"{BE_B*100:.0f}%"),
    ], col_widths=[3.5, 1.5, 1.5])
    para(doc, f"Loaded cost per covered service call is estimated at {C.money2(CPC)} (assumption). "
              f"Each plan stays profitable per member until utilization exceeds ~{BE_A*100:.0f}% "
              f"($3.99) or ~{BE_B*100:.0f}% ($4.99).", size=9.5, italic=True)

    h1(doc, "3. Financial Results by Structure")
    rows = []
    for label, part, cbase in [("Mandatory (100%)", 1.00, "all"),
                               ("Opt-out @ 85%", 0.85, "all"),
                               ("Opt-out @ 60%", 0.60, "all"),
                               ("Opt-in @ 40%", 0.40, "enrolled"),
                               ("Opt-in @ 30%", 0.30, "enrolled"),
                               ("Opt-in @ 20%", 0.20, "enrolled")]:
        ta = C.program_totals(C.PRICE_A, C.A["current_subs"], part, churn_base=cbase, include_onetime=False)
        tb = C.program_totals(C.PRICE_B, C.A["current_subs"], part, churn_base=cbase, include_onetime=False)
        rows.append((label, C.money(ta["gross_annual"]), C.money(ta["net_annual"]),
                     C.money(tb["gross_annual"]), C.money(tb["net_annual"])))
    table(doc, ["Structure", "Gross $3.99", "Net $3.99", "Gross $4.99", "Net $4.99"], rows,
          col_widths=[1.9, 1.2, 1.2, 1.2, 1.2], font_size=9)
    para(doc, f"At {C.A['current_subs']:,} subscribers, a mandatory plan generates the most gross "
              f"revenue, but see the churn analysis: it is also the most fragile. Opt-in structures "
              f"generate less gross revenue but avoid the trust and regulatory exposure.", size=9.5)

    h1(doc, "4. The Churn Problem (why not mandatory)")
    para(doc, "A mandatory or opt-out fee applied to customers who never need a service call risks "
              "incremental churn. Because a churned customer costs the full internet ARPU, only a "
              "small amount of fee-driven churn erases the plan's gain:")
    bullet(doc, f"At $3.99 mandatory, incremental annual churn of just ~{OFF_A*100:.1f}% fully "
                f"offsets the plan's net contribution.", bold_lead="$3.99: ")
    bullet(doc, f"At $4.99 mandatory, the break-even churn is ~{OFF_B*100:.1f}%.", bold_lead="$4.99: ")
    para(doc, f"With ${C.A['arpu']:.0f} monthly ARPU, one churned customer wipes out roughly "
              f"{C.A['arpu']*12/PM_A['contribution']:.0f} members' worth of $3.99 plan contribution. "
              f"For a community-focused cooperative provider, that trade is not worth the "
              f"reputational risk.")
    callout(doc, None, "Voluntary opt-in customers choose the plan, so fee-driven churn is "
            "effectively zero — which is why opt-in is the safer structure.", "recommendation")

    h1(doc, "5. Customer & Regulatory Risks")
    for t, d in [
        ("Negative-option billing", "Auto-enroll/opt-out may trigger FTC ROSCA and state auto-renewal rules — legal review required."),
        ("Lifeline / Tribal Lifeline", "Low-income subscribers should never be auto-charged; opt-in only."),
        ("Truthful naming", "The fee must not be called a tax, government, regulatory, or network fee."),
        ("Broadband label / disclosure", "Confirm whether the charge must appear on the FCC broadband label."),
        ("NC consumer protection", "Advance notice, transparency, and material-change requirements."),
        ("Fairness", "Charging non-users a mandatory fee is the core fairness objection."),
    ]:
        bullet(doc, d, bold_lead=f"{t}. ")

    h1(doc, "6. Structure Comparison (weighted decision matrix)")
    order = sorted(C.OPTIONS, key=lambda o: -WS[o])
    table(doc, ["Rank", "Option", "Weighted Score (1-5)"],
          [(str(i), o, f"{WS[o]:.2f}") for i, o in enumerate(order, 1)],
          col_widths=[0.7, 3.8, 2.0], font_size=9.5)
    para(doc, "Scores weight regulatory risk, financial benefit, and churn risk most heavily. "
              "Voluntary opt-in ($3.99) and the hybrid model rank highest; mandatory options rank "
              "lowest despite higher gross revenue.", size=9.5, italic=True)

    h1(doc, "7. Recommendation")
    bullet(doc, "Voluntary opt-in at $3.99/month, Standard coverage.", bold_lead="Structure & price: ")
    bullet(doc, "Enrollees get the plan; decliners pay a per-visit dispatch charge ($99 suggested).", bold_lead="Hybrid: ")
    bullet(doc, "Offer at installation and again after a customer's first chargeable service call; no retroactive enrollment; 30-day waiting period; pre-existing conditions excluded.", bold_lead="Enrollment mechanics: ")
    bullet(doc, "Lifeline, Tribal Lifeline, and low-income: opt-in only, never auto-charged. Bulk/managed properties excluded (handled by contract).", bold_lead="Exemptions: ")
    bullet(doc, f"Opt-in plan revenue alone yields ~{C.money(FIVEYR[-1]['cum_net'])} cumulative net "
                f"over five years (excludes pay-per-visit upside).", bold_lead="Five-year outlook: ")

    h1(doc, "8. Implementation Conditions & Decision Gates")
    for g in ["Legal sign-off on negative-option, Lifeline, naming, and NC consumer-protection questions.",
              "NISC billing-code and tax configuration confirmed and tested.",
              "Replace the ten planning assumptions with real RIVR Tech data.",
              "Run a 90-day pilot; proceed only if enrollment ≥ target and complaints/churn within limits.",
              "Executive go/no-go after pilot review."]:
        numbered(doc, g)
    callout(doc, None, "Recommendations and labeled assumptions only — not established policy and "
            "not legal advice. Requires legal, regulatory, tax, accounting, and executive review.", "warning")

    save(doc, p("RIVR_Tech_Blanket_Protection_Analysis", "02_Executive_Memo",
                "RIVR_Tech_Blanket_Protection_Executive_Memo.docx"), "Blanket Protection Executive Memo")


# ==========================================================================
# 2. DRAFT MAINTENANCE PROTECTION PLAN
# ==========================================================================
def plan_document():
    doc = new_doc()
    cover_page(doc, f"{C.PLAN_NAME} — Draft Plan Terms",
               "Optional Residential Maintenance Protection Plan",
               "Draft for Legal Review — This is NOT insurance")
    toc_field(doc)

    callout(doc, "DRAFT — REVIEW REQUIRED", "This is a draft plan for review. It is not established "
            "policy, not insurance, and not a warranty. All terms require legal, regulatory, and "
            "insurance-characterization review before use.", "policy")

    h1(doc, "1. Program Name")
    para(doc, f"{C.PLAN_NAME} (working name; alternatives: RIVR Tech Care, RIVR Tech Home Assist, "
              f"RIVR Tech Service Shield). The name must not imply insurance, warranty, or a "
              f"government/regulatory fee.")

    h1(doc, "2. Eligibility")
    para(doc, "Available to active residential internet customers in good standing. Offered at "
              "installation and after a first chargeable service call. Lifeline, Tribal Lifeline, "
              "and low-income customers may enroll voluntarily but are never auto-enrolled. Bulk "
              "and managed-property accounts are governed by their property contracts and are "
              "excluded from individual enrollment.")

    h1(doc, "3. Coverage")
    para(doc, "Coverage tiers are offered; the recommended default is Standard at $4.99 (or a "
              "$3.99 Basic tier). Coverage applies to qualifying customer-premises service calls:")
    table(doc, ["Item", "RIVR-Owned (free)", "Basic", "Standard", "Premium"],
          [(row[0], row[1], row[2], row[3], row[4]) for row in C.COVERAGE_ROWS],
          col_widths=[2.5, 1.5, 0.85, 0.9, 0.85], font_size=8)
    para(doc, "RIVR Tech-owned equipment (ONT, router/GigaSpire, outdoor drop) and RIVR network "
              "problems are always repaired free regardless of plan status.", size=9, italic=True)

    h1(doc, "4. What the Plan Does NOT Cover (Exclusions)")
    for x in ["Replacement of customer-owned routers, computers, TVs, phones, cameras, or smart-home devices.",
              "Damage from construction or remodeling.",
              "Acts of God, storms, flooding, or utility damage.",
              "Willful damage, gross negligence, or unauthorized equipment modification.",
              "Concealed wiring, major rewiring, or construction.",
              "Pre-existing conditions present before enrollment.",
              "Unlimited repeat visits for the same customer-owned device."]:
        bullet(doc, x)

    h1(doc, "5. Effective Date & Waiting Period")
    para(doc, f"Effective date: {C.EFFECTIVE_DATE_PLACEHOLDER}. Coverage begins after a 30-day "
              f"waiting period from enrollment. Service calls requested before or during the "
              f"waiting period are not covered.")

    h1(doc, "6. Service-Call Limits")
    para(doc, "Basic: one covered visit per rolling 12 months (additional visits at a reduced "
              "dispatch charge). Standard: two covered visits per rolling 12 months. Premium: up "
              "to four. Limits reset on a rolling 12-month basis.")

    h1(doc, "7. Charges")
    para(doc, f"Monthly charge: $3.99 (Basic) or $4.99 (Standard), billed as a clearly labeled "
              f"line item. Non-enrolled customers pay a per-visit dispatch charge for "
              f"customer-caused calls. Price changes require advance notice per policy and law.")

    h1(doc, "8. Cancellation")
    para(doc, "Customers may cancel at any time; coverage ends at the close of the current billing "
              "cycle. No long-term commitment. Re-enrollment is subject to a new waiting period to "
              "prevent adverse selection.")

    h1(doc, "9. Customer Responsibilities")
    for x in ["Maintain customer-owned equipment and premises power.",
              "Provide safe access for scheduled visits.",
              "Cooperate with remote troubleshooting.",
              "Use the plan in good faith (no abuse/misuse)."]:
        bullet(doc, x)

    h1(doc, "10. RIVR Tech Responsibilities")
    for x in ["Repair RIVR-owned equipment and network problems free of charge.",
              "Disclose coverage, limits, and any separate charges in advance.",
              "Document findings before assessing any non-covered charge.",
              "Provide a fair dispute process."]:
        bullet(doc, x)

    h1(doc, "11. Abuse & Misuse Provisions")
    para(doc, "RIVR Tech may decline coverage or remove a customer from the plan for repeated "
              "avoidable calls on the same customer-owned device, willful damage, misrepresentation, "
              "or attempts to enroll after a problem has occurred. Retroactive enrollment is not "
              "permitted.")

    h1(doc, "12. Dispute Process")
    para(doc, "Disputes follow: frontline explanation → supervisor review → technical review → "
              "billing adjustment, within a defined response timeline. Refunds are issued for "
              "documentation errors or incorrect disclosure.")

    h1(doc, "13. Legal-Review Placeholders")
    for a, b, c in C.LEGAL_FLAGS:
        bullet(doc, f"{a} — {b} (Review: {c})")
    callout(doc, None, "The plan must be characterized and marketed as an optional service/"
            "maintenance plan, NOT insurance or a warranty. Confirm with legal and insurance "
            "advisers.", "legal")

    save(doc, p("RIVR_Tech_Blanket_Protection_Analysis", "03_Plan_Document",
                "RIVR_Tech_Home_Protection_Draft_Plan.docx"), "Draft Home Protection Plan")


# ==========================================================================
# 3. CUSTOMER COMMUNICATIONS PACKAGE
# ==========================================================================
FAQS = [
    ("Is this a new required charge?", "No. The RIVR Tech Home Protection plan is optional. You choose whether to enroll. Repairs to RIVR Tech-owned equipment and our network are always free."),
    ("What does the plan cover?", "Qualifying customer-premises service calls — basic Wi-Fi troubleshooting, RIVR-installed inside wiring, connector issues, router relocation, customer education, and one to two covered technician visits per year depending on tier."),
    ("What is not covered?", "Your own routers and devices, damage from construction, storms or floods, willful damage, concealed rewiring, and pre-existing problems."),
    ("How much is it?", "$3.99/month for Basic or $4.99/month for Standard coverage, shown as a clearly labeled line item on your bill."),
    ("Is this insurance?", "No. It is an optional service and maintenance plan, not insurance or a warranty."),
    ("What if I never need a service call?", "Then you may prefer not to enroll — it's completely optional. Customers who decline simply pay a per-visit charge only if they ever need a customer-caused service call."),
    ("When does coverage start?", "30 days after you enroll. Problems that exist before enrollment or during the waiting period aren't covered."),
    ("Can I cancel?", "Yes, anytime. Coverage ends at the close of your current billing cycle."),
    ("Can I enroll after I already have a problem?", "No. To keep the plan fair for everyone, you can't enroll retroactively after requesting a service call for an existing issue."),
    ("Do Lifeline or Tribal Lifeline customers have to pay this?", "No. It is never automatically added. Lifeline and Tribal Lifeline customers may choose to enroll but are never auto-charged."),
    ("What if I rent my home?", "You can still enroll. Some wiring may be owned by your landlord or property; we'll explain what's covered."),
    ("How do I dispute a charge?", "Contact RIVR Tech. We start with a frontline explanation, then supervisor and technical review, and adjust billing if warranted."),
    ("Will my internet rate go up?", "No. This is a separate optional plan and does not change your internet service rate."),
    ("How do I sign up?", "At installation, by contacting RIVR Tech, or through your account portal."),
]


def comms():
    doc = new_doc()
    cover_page(doc, "Customer Communications Package",
               f"{C.PLAN_NAME} (Optional Plan)",
               "Bill, Email, Website, FAQ, Scripts, and Opt-In/Opt-Out Language")
    toc_field(doc)

    callout(doc, "TONE", "Warm, local, simple, respectful. The plan is OPTIONAL. Never imply it is "
            "required, insurance, or a tax. All wording requires legal review before use.", "recommendation")

    h1(doc, "1. Bill Message")
    para(doc, f"\"NEW (optional): {C.PLAN_NAME} — protect against customer-premises service-call "
              f"charges for as little as $3.99/mo. RIVR Tech network & equipment repairs are always "
              f"free. Enrollment is optional. Learn more: [link].\"", italic=True)

    h1(doc, "2. Email Announcement")
    para(doc, "Subject: An optional new way to protect against service-call costs", bold=True)
    para(doc, "Dear [Customer Name],")
    para(doc, f"At {C.COMPANY_SHORT}, repairs to our network and our equipment are always free. "
              f"For added peace of mind, we're introducing an optional plan — {C.PLAN_NAME} — that "
              f"covers qualifying customer-premises service calls (like basic Wi-Fi help, RIVR-"
              f"installed inside wiring, and covered technician visits) for $3.99–$4.99/month.")
    para(doc, "Enrollment is completely optional, there's no long-term commitment, and you can "
              "cancel anytime. It is a service plan — not insurance. Learn more or enroll at [link].")
    para(doc, f"— The {C.COMPANY_SHORT} Team")

    h1(doc, "3. Website Announcement")
    para(doc, f"{C.PLAN_NAME} is an optional monthly plan that helps protect you against charges "
              f"for qualifying customer-premises service calls. RIVR Tech-owned equipment and "
              f"network repairs are always free. Choose Basic ($3.99/mo) or Standard ($4.99/mo). "
              f"Coverage begins 30 days after enrollment. Optional, cancel anytime, not insurance.")

    h1(doc, "4. Frequently Asked Questions")
    for i, (q, a) in enumerate(FAQS, 1):
        para(doc, f"Q{i}. {q}", bold=True, size=10, color=C.BRAND["secondary"], space_after=1)
        para(doc, a, size=10, space_after=6)

    h1(doc, "5. Customer-Service Script")
    para(doc, "Offer (never pressure): \"We have an optional plan called RIVR Tech Home Protection "
              "for $3.99 to $4.99 a month. It covers qualifying service calls for things on your "
              "side — like Wi-Fi help and covered technician visits. Our network and equipment "
              "repairs are always free either way. Would you like to hear what's covered?\"")
    para(doc, "If declined: \"No problem at all — it's completely optional. You'd simply pay per "
              "visit only if you ever need a customer-caused service call.\"")

    h1(doc, "6. Technician Explanation")
    para(doc, "\"The RIVR Tech service is testing good to your equipment; today's issue is on the "
              "premises side. If you're enrolled in Home Protection, this visit is covered. If not, "
              "it's optional to enroll for next time — there's a 30-day waiting period, so it won't "
              "change today's visit.\"")

    h1(doc, "7. Opt-In Language (recommended)")
    para(doc, "\"Yes, please enroll me in RIVR Tech Home Protection at $[3.99/4.99]/month. I "
              "understand it is optional, is a service plan (not insurance), begins after a 30-day "
              "waiting period, excludes pre-existing conditions, and can be cancelled anytime.\"", italic=True)

    h1(doc, "8. Opt-Out Language (only if an opt-out model is ever approved)")
    callout(doc, None, "An automatic-enrollment/opt-out model is NOT recommended and would require "
            "specific legal clearance (negative-option rules). Use only if legal approves.", "legal")
    para(doc, "\"You are currently enrolled in the optional RIVR Tech Home Protection plan at "
              "$[price]/month. To decline, reply STOP, call [number], or visit [link] by [date]. "
              "Declining will not affect your internet service.\"", italic=True)

    save(doc, p("RIVR_Tech_Blanket_Protection_Analysis", "04_Customer_Communications",
                "RIVR_Tech_Blanket_Protection_Customer_Communications.docx"),
         "Blanket Protection Customer Communications")


# ==========================================================================
# 4. IMPLEMENTATION ROADMAP
# ==========================================================================
def roadmap():
    doc = new_doc()
    cover_page(doc, "Implementation Roadmap",
               f"{C.PLAN_NAME} — 30/60/90-Day Plan",
               "Operational Rollout, Approvals, and Pilot Design")
    toc_field(doc)

    h1(doc, "1. Phased Timeline")
    table(doc, ["Phase", "Focus"], [
        ("Days 1–30", "Design & approvals: coverage tiers, pricing, legal/tax review, NISC billing-code and product/service-code setup, eligibility rules, terms & conditions."),
        ("Days 31–60", "Build & train: billing configuration, work-order/trouble-ticket reason codes, technician findings + photo documentation, dispute/refund procedures, employee + MSR training, website/T&C/bill messages/FAQ."),
        ("Days 61–90", "Pilot & review: limited-market pilot, enrollment and opt-in flows, quality-control audits, monthly reporting, post-pilot go/no-go."),
    ], col_widths=[1.3, 5.2], font_size=9.5)

    h1(doc, "2. Workstream Detail")
    table(doc, ["Workstream", "Key Tasks", "Owner", "Approval"], [
        ("Billing / NISC", "Product & service codes, line-item name, tax review, adjustments", "Billing / IT", "CFO / Tax"),
        ("Legal / Regulatory", "Negative-option, Lifeline, naming, NC consumer protection, T&C", "General Counsel", "CEO"),
        ("Operations", "Work-order coding, reason codes, tech findings, photos, materials tracking", "COO / Field Ops", "COO"),
        ("Customer Experience", "Scripts, dispute/appeal, refunds, QA audits", "CX Lead", "COO"),
        ("Marketing", "Website, bill messages, email, direct mail, FAQ", "Marketing", "Legal"),
        ("Training", "Technician, support, sales, MSR training", "Enablement", "COO"),
        ("Finance", "Model validation, pilot metrics, reporting", "Finance", "CFO"),
    ], col_widths=[1.5, 3.0, 1.2, 0.8], font_size=8.5)

    h1(doc, "3. Required Approvals & Decision Gates")
    for g in ["Legal opinion on negative-option/opt-out billing and Lifeline/Tribal Lifeline treatment.",
              "Tax determination on the plan charge.",
              "Executive approval of price, coverage tier, and enrollment structure.",
              "NISC configuration tested in a non-production environment.",
              "Pilot success criteria met before system-wide launch."]:
        numbered(doc, g)

    h1(doc, "4. Pilot Design (recommended)")
    for x in ["Scope: one or two representative service areas; voluntary opt-in only.",
              "Duration: 90 days.",
              "Enrollment offer: at installation and after first chargeable call.",
              "Metrics: enrollment take-rate, utilization %, cost per covered call, complaints, churn, dispute rate, coding accuracy.",
              "Success thresholds (editable): take-rate ≥ 25%, utilization ≤ 20%, complaint rate flat, churn increase ≤ 0.5%.",
              "Decision: go/no-go and price/tier adjustment after review."]:
        bullet(doc, x)

    h1(doc, "5. Post-Launch Review")
    para(doc, "Review at 30, 60, and 90 days post-launch: financial performance vs. model, "
              "utilization, complaints and disputes, churn, and coding accuracy. Adjust price, "
              "coverage, or exemptions as needed. Report monthly to executives.")

    h1(doc, "6. Naming & Billing Display")
    para(doc, f"Recommended customer-facing name: {C.PLAN_NAME} (optional). Display as a clearly "
              f"labeled optional line item. Do NOT describe the charge as a government fee, tax, "
              f"mandatory regulatory fee, or network fee unless legally accurate.")
    callout(doc, None, "Billing display, naming, and disclosures require legal and billing review.", "legal")

    h1(doc, "7. Data to Collect Before Final Approval")
    for d in C.DATA_NEEDED:
        bullet(doc, d)

    save(doc, p("RIVR_Tech_Blanket_Protection_Analysis", "05_Implementation",
                "RIVR_Tech_Blanket_Protection_Implementation_Roadmap.docx"),
         "Blanket Protection Implementation Roadmap")


if __name__ == "__main__":
    print("Building blanket-plan Word documents...")
    memo()
    plan_document()
    comms()
    roadmap()
    print("Done.")
