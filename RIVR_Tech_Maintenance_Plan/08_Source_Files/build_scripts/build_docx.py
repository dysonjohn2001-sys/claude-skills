# -*- coding: utf-8 -*-
"""Builds all RIVR Tech Word deliverables."""
import os
import rivr_content as C
from docx_helpers import (new_doc, cover_page, toc_field, h1, h2, h3, para, bullet,
                          numbered, callout, table, save, _hr)

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
R = C.compute_model()
SC = C.scenario_results()


def p(*parts):
    return os.path.join(BASE, *parts)


# ==========================================================================
# 1. BUSINESS CASE
# ==========================================================================
def business_case():
    doc = new_doc()
    cover_page(doc, "Customer-Premises Maintenance & Billable Trouble-Visit Program",
               "Business Case", "Executive Business Case & Financial Justification")
    toc_field(doc)

    h1(doc, "1. Executive Summary")
    para(doc, f"{C.COMPANY_SHORT} today performs all maintenance and trouble visits at no "
              f"charge, including visits whose root cause is on the customer's side of the "
              f"network — customer-owned equipment, customer actions, damaged inside wiring, "
              f"premises power problems, third-party devices, and Wi-Fi limitations unrelated "
              f"to the {C.COMPANY_SHORT} network. This subsidizes a growing volume of avoidable "
              f"truck rolls and diverts field capacity away from genuine network work.")
    para(doc, "This business case recommends a fair, transparent, customer-friendly program that "
              "keeps all RIVR Tech network and equipment repairs free, introduces reasonable "
              "charges only for documented customer-premises visits, strengthens remote "
              "troubleshooting to prevent unnecessary dispatches, and adds an optional monthly "
              "maintenance-protection plan. The design prioritizes deflection and education over "
              "fee revenue, and protects RIVR Tech's community reputation.")
    callout(doc, "RECOMMENDATION",
            f"Adopt the Balanced fee posture (${C.RES_FEE} residential / ${C.BUS_FEE} business "
            f"customer-premises visit), launch RIVR Tech Home Maintenance Protection at "
            f"${C.PROTECTION_RECOMMENDED:.2f}/month, and lead with a 30-day warning-only grace "
            f"period plus a first-incident courtesy waiver.", "recommendation")

    h2(doc, "1.1 Headline Financials (Expected Scenario)")
    rows = [
        ("Annual dispatch expense (all truck rolls)", C.money(R["annual_dispatch_expense"])),
        ("Annual customer-caused dispatch cost", C.money(R["cust_caused_dispatch_cost"])),
        ("Net trouble-visit fee revenue (Year 1)", C.money(R["net_fee_revenue"])),
        ("Protection-plan contribution margin (Year 1)", C.money(R["protection_margin"])),
        ("Avoided-truck-roll savings (deflection)", C.money(R["deflection_savings"])),
        ("Cost recovery of customer-caused dispatch cost", f"{R['cost_recovery_pct']*100:.0f}%"),
        ("Year 1 net financial effect (after one-time cost)", C.money(R["year1_net"])),
        ("Implementation payback period", f"{R['payback_months']:.1f} months"),
        ("Three-year net financial effect", C.money(R["three_year_net"])),
    ]
    table(doc, ["Metric", "Expected"], rows, col_widths=[4.6, 1.9], first_col_bold=False)
    callout(doc, None, "All figures are model outputs under labeled assumptions. Replace the ten "
            "RIVR Tech data points listed in Section 7 to finalize. See the financial model "
            "workbook for live formulas and scenarios.", "assumption")

    h1(doc, "2. Problem Statement")
    para(doc, "Every truck roll consumes a technician, a vehicle, fuel, and materials. When the "
              "root cause is on the customer's premises, RIVR Tech absorbs the full cost while "
              "the customer receives a free visit that a third-party service would bill. The "
              "consequences:")
    bullet(doc, "Avoidable dispatches crowd out network and installation work.", bold_lead="Capacity drain. ")
    bullet(doc, f"At an estimated {C.money(R['cost_per_dispatch'])} per dispatch, customer-caused "
                f"visits cost roughly {C.money(R['cust_caused_dispatch_cost'])} per year.", bold_lead="Unrecovered cost. ")
    bullet(doc, "No pricing signal exists to encourage self-service or protect customer-owned gear.", bold_lead="No incentive. ")
    bullet(doc, "Customers are surprised later when they learn a neighbor's ISP would have charged.", bold_lead="Inequity. ")

    h1(doc, "3. Program Design Principles")
    for t, d in [
        ("Network repairs stay free", "Confirmed RIVR Tech network or equipment problems are never billed."),
        ("Charge only with evidence", "A fee requires documented findings, tests, and — where relevant — photos."),
        ("No surprise billing", "Advance disclosure and customer acknowledgment before any dispatch that could bill."),
        ("Deflect before dispatch", "Strong remote troubleshooting resolves more issues without a truck."),
        ("Educate, don't blame", "Language is 'customer-premises issue,' never 'customer fault.'"),
        ("Protect the vulnerable", "Hardship, accommodation, and courtesy waivers are built in."),
    ]:
        bullet(doc, d, bold_lead=f"{t}. ")

    h1(doc, "4. Recommended Fee Schedule")
    fee_rows = []
    for label, cons, bal, full, note in C.FEE_ITEMS:
        fmt = lambda x: ("$0" if x == 0 else f"${x}")
        fee_rows.append((label, fmt(cons), fmt(bal), fmt(full)))
    table(doc, ["Fee Item", "Conservative", "Balanced (Rec.)", "Full Recovery"], fee_rows,
          col_widths=[3.3, 1.05, 1.15, 1.05], font_size=8.5)
    para(doc, "Additional labor after the first 30 minutes bills at $35 per 30 minutes on billable "
              "work only. Relocation and inside-wiring items add materials at cost. The first "
              "customer-caused incident is eligible for a one-time educational courtesy waiver.", size=9)
    callout(doc, "RECOMMENDATION", f"The Balanced posture recovers a meaningful share of field cost "
            f"while remaining below typical third-party service-call rates in {C.REGION}, "
            f"preserving RIVR Tech's community-first positioning.", "recommendation")

    h1(doc, "5. Optional Maintenance-Protection Plan")
    para(doc, "RIVR Tech Home Maintenance Protection is an optional monthly plan that covers "
              "standard customer-premises trouble visits, basic inside-wiring diagnostics, Wi-Fi "
              "education, and basic device-connection assistance, with priority scheduling. It is "
              "a service plan — not insurance, not a warranty.")
    prow = []
    for price in C.PROTECTION_PRICES:
        res = C.compute_model({"protection_price": price})
        prow.append((f"${price:.2f}/mo",
                     C.money(res["protection_revenue"]),
                     C.money(res["protection_margin"]),
                     f"${res['protection_be_price_monthly']:.2f}"))
    table(doc, ["Price Point", "Annual Revenue", "Contribution Margin", "Break-even Price"], prow,
          col_widths=[1.4, 1.7, 1.9, 1.5])
    callout(doc, "RECOMMENDATION", f"Launch at ${C.PROTECTION_RECOMMENDED:.2f}/month — the price "
            f"that balances adoption, perceived value, and margin. Requires legal and insurance "
            f"characterization review before launch.", "recommendation")
    callout(doc, None, "The plan must not be marketed or structured as insurance. Confirm "
            "characterization with legal and insurance advisors.", "legal")

    h1(doc, "6. Scenario Analysis")
    srow = []
    for name in ["Low", "Expected", "High"]:
        s = SC[name]
        srow.append((name, C.money(s["net_fee_revenue"]), C.money(s["protection_margin"]),
                     C.money(s["deflection_savings"]), C.money(s["year1_net"]),
                     C.money(s["three_year_net"])))
    table(doc, ["Scenario", "Net Fees", "Plan Margin", "Deflection", "Year 1 Net", "3-Yr Net"],
          srow, col_widths=[1.0, 1.0, 1.05, 1.05, 1.05, 1.05], font_size=9)
    para(doc, "Even the Low scenario delivers positive three-year value, driven primarily by "
              "avoided truck rolls rather than fee revenue — reinforcing that deflection, not "
              "billing, is the main economic engine.", size=9.5, italic=True)

    h1(doc, "7. Assumptions to Replace")
    para(doc, "The following RIVR Tech data points should replace the modeled assumptions before "
              "final approval:")
    for label, _, note in C.assumptions_register()[:12]:
        bullet(doc, f"{label} — {note}")

    h1(doc, "8. Risks & Mitigations")
    risks = [
        ("Customer backlash / reputation", "Lead with education, 30-day grace, courtesy waiver, warm messaging, robust dispute process."),
        ("Perception as a money grab", "Cap fees below market; publish what stays free; emphasize deflection savings over revenue."),
        ("Regulatory / consumer-protection", "Full NC review; clear disclosures; documented findings before any charge."),
        ("Employee inconsistency", "Mandatory training, coding accuracy audits, supervisor approvals, QA review."),
        ("Protection-plan mischaracterization", "Legal/insurance review; avoid insurance/warranty language."),
        ("Churn", "Model includes churn cost; monitor policy-related churn KPI; hardship waivers."),
    ]
    table(doc, ["Risk", "Mitigation"], risks, col_widths=[2.3, 4.2], font_size=9.5)

    h1(doc, "9. Recommendation")
    para(doc, f"Approve the Balanced fee posture, launch the ${C.PROTECTION_RECOMMENDED:.2f} "
              f"protection plan, and proceed with the 90-day phased implementation. Under the "
              f"expected scenario the program returns approximately {C.money(R['year1_net'])} in "
              f"Year 1 (payback ~{R['payback_months']:.1f} months) and {C.money(R['three_year_net'])} "
              f"over three years, while reducing unnecessary truck rolls and keeping all genuine "
              f"network repairs free.")
    callout(doc, None, "This document is a recommendation, not established RIVR Tech policy, and "
            "is not legal advice. Provisions require legal, regulatory, accounting, and insurance "
            "review before adoption.", "warning")

    save(doc, p("RIVR_Tech_Maintenance_Plan", "01_Executive",
                "RIVR_Tech_Maintenance_Business_Case.docx"), "Maintenance Program Business Case")


# ==========================================================================
# 2. EXECUTIVE DECISION SUMMARY
# ==========================================================================
def exec_summary():
    doc = new_doc()
    cover_page(doc, "Executive Decision Summary",
               "Customer-Premises Maintenance & Billable Trouble-Visit Program",
               "One-Read Briefing for the Executive Team")

    h1(doc, "The Ask")
    para(doc, f"Approve a fair, transparent program that keeps all {C.COMPANY_SHORT} network and "
              f"equipment repairs free, adds reasonable charges only for documented "
              f"customer-premises trouble visits, and offers an optional monthly maintenance-"
              f"protection plan. The program prioritizes deflection and education over fee revenue.")

    h1(doc, "Why Now")
    bullet(doc, f"Customer-caused truck rolls cost an estimated {C.money(R['cust_caused_dispatch_cost'])} per year today, fully absorbed by RIVR Tech.")
    bullet(doc, "No pricing signal exists to reduce avoidable visits or protect customer-owned gear.")
    bullet(doc, "Competitors and third-party technicians already charge for this work.")

    h1(doc, "What the Customer Sees")
    bullet(doc, "RIVR Tech network or equipment problem: always $0.", bold_lead="Free. ")
    bullet(doc, "Inconclusive / no-trouble-found visit: $0.", bold_lead="Free. ")
    bullet(doc, f"Documented customer-premises visit: ${C.RES_FEE} residential / ${C.BUS_FEE} business — disclosed in advance, with a first-time courtesy waiver.", bold_lead="Fair. ")
    bullet(doc, "Optional protection plan avoids per-visit charges for a low monthly fee.", bold_lead="Optional. ")

    h1(doc, "Expected Financial Result")
    rows = [
        ("Year 1 net financial effect", C.money(R["year1_net"])),
        ("Payback period", f"{R['payback_months']:.1f} months"),
        ("Three-year net financial effect", C.money(R["three_year_net"])),
        ("Cost recovery (customer-caused dispatch cost)", f"{R['cost_recovery_pct']*100:.0f}%"),
        ("Primary economic driver", "Avoided truck rolls (deflection), not fees"),
    ]
    table(doc, ["Metric", "Expected Scenario"], rows, col_widths=[4.2, 2.3])

    h1(doc, "The Five Decisions We Need")
    for i, (title, desc, owner) in enumerate(C.EXEC_DECISIONS, 1):
        para(doc, f"{i}. {title}", bold=True, size=11, color=C.BRAND["primary"], space_after=1)
        para(doc, f"{desc}  (Owner: {owner})", size=10, space_after=6)

    h1(doc, "Recommended Answers")
    bullet(doc, "Balanced fee posture ($75 / $125).", bold_lead="Fee posture: ")
    bullet(doc, f"Launch at ${C.PROTECTION_RECOMMENDED:.2f}/month.", bold_lead="Protection plan: ")
    bullet(doc, "Yes — 30-day warning-only period + first-incident courtesy waiver.", bold_lead="Grace period: ")
    bullet(doc, f"Fund ~{C.money(R['one_time_cost'])} one-time; set effective date after training + legal sign-off.", bold_lead="Budget & date: ")
    bullet(doc, "Authorize NC consumer-protection, tax, and insurance-characterization review.", bold_lead="Legal scope: ")

    h1(doc, "Top Risks (with mitigations)")
    table(doc, ["Risk", "Mitigation"], [
        ("Reputation / backlash", "Education-first, grace period, courtesy waiver, dispute process."),
        ("Regulatory exposure", "NC review; documented findings before any charge."),
        ("Insurance mischaracterization", "Legal/insurance review of the protection plan."),
    ], col_widths=[2.3, 4.2], font_size=9.5)

    callout(doc, None, "Recommendations and labeled assumptions only — not established policy and "
            "not legal advice. Requires legal, regulatory, accounting, and insurance review.", "warning")
    save(doc, p("RIVR_Tech_Maintenance_Plan", "01_Executive",
                "RIVR_Tech_Executive_Decision_Summary.docx"), "Executive Decision Summary")


# ==========================================================================
# 3. POLICY
# ==========================================================================
def policy():
    doc = new_doc()
    cover_page(doc, "RIVR Tech Customer-Premises Maintenance and Technician Visit Policy",
               "Formal Policy (Proposed)", "For Executive and Legal Review")
    toc_field(doc)

    def section(title, body_paras=None, bullets=None):
        h2(doc, title)
        for b in (body_paras or []):
            para(doc, b)
        for bl in (bullets or []):
            bullet(doc, bl)

    h1(doc, "Policy Overview")
    callout(doc, "PROPOSED POLICY", "This document is a proposed policy for review and approval. "
            "It is not established RIVR Tech policy and not legal advice until adopted by the "
            "executive team and cleared by legal and regulatory review.", "policy")

    section("1. Purpose", [
        f"This policy establishes how {C.COMPANY_LEGAL} ('{C.COMPANY_SHORT}') determines "
        f"responsibility for maintenance and trouble visits, when a service charge may apply, "
        f"and how RIVR Tech protects customers from surprise billing. RIVR Tech network and "
        f"equipment repairs remain free. Charges apply only to documented customer-premises work."])

    section("2. Scope", [
        f"This policy applies to all residential and business customers of RIVR Tech broadband, "
        f"managed Wi-Fi, and voice services in {C.REGION}, and to all RIVR Tech employees and "
        f"contractors who triage, dispatch, or perform service visits."])

    section("3. Effective Date", [C.EFFECTIVE_DATE_PLACEHOLDER + ". Billing begins only after "
            "the customer-education period and the 30-day warning-only grace period conclude."])

    h2(doc, "4. Services Covered")
    for s in C.SERVICES_COVERED:
        bullet(doc, s)

    h2(doc, "5. Definitions")
    defs = [
        ("Demarcation point", "The physical point separating the RIVR Tech network from customer inside wiring and equipment."),
        ("RIVR Tech equipment", "ONT, gateway/router, and related devices owned by RIVR Tech."),
        ("Customer-owned equipment", "Any device the customer owns: routers, mesh, switches, cameras, TVs, consoles, smart-home gear."),
        ("Customer-premises issue", "A problem originating on the customer's side of the demarcation point."),
        ("Trouble visit / truck roll", "A technician dispatch to diagnose or repair a reported problem."),
        ("Billable visit", "A customer-premises visit with documented findings supporting a charge."),
        ("Inconclusive", "A visit where no clear cause is determined or the issue is not reproduced."),
    ]
    table(doc, ["Term", "Definition"], defs, col_widths=[1.8, 4.7], font_size=9.5)

    h2(doc, "6. Responsibility Classifications")
    para(doc, "Every visit is classified into exactly one of four categories. A fee must not be "
              "assessed solely because a technician was dispatched.")
    table(doc, ["Classification", "Customer Charge"], [
        ("1. RIVR Tech responsibility", "No customer charge."),
        ("2. Customer-premises responsibility", "A fee may apply when supported by documented findings."),
        ("3. Shared responsibility", "Supervisor review; reduced fee or waiver may apply."),
        ("4. Inconclusive", "No charge unless management approves based on clear evidence."),
    ], col_widths=[2.6, 3.9])

    section("7. RIVR Tech Responsibilities", bullets=[
        "Maintain and repair the RIVR Tech network, fiber, drops, ONTs, and gateways at no charge.",
        "Perform strong remote troubleshooting before dispatch.",
        "Disclose any potential charge in advance and obtain customer acknowledgment.",
        "Document findings, tests, and photos before assessing any fee.",
        "Offer courtesy, hardship, and accommodation waivers.",
        "Provide a clear, fair dispute and appeal process."])

    section("8. Customer Responsibilities", bullets=[
        "Maintain customer-owned equipment, inside wiring, and premises power.",
        "Provide safe access and an authorized adult (residential) for scheduled visits.",
        "Cooperate with remote troubleshooting before a dispatch.",
        "Acknowledge advance disclosure that a charge may apply based on findings."])

    section("9. Billable Visits", [
        "A visit may be billable when documented findings show the root cause is a customer-"
        "premises responsibility. Examples: customer-owned equipment failure, customer-damaged "
        "wiring, premises power problems, third-party device configuration, requested equipment "
        "relocation, missed appointments, or denied access."])

    section("10. Nonbillable Visits", [
        "Confirmed RIVR Tech network or equipment problems, normal fiber/drop failures, no-"
        "trouble-found visits, inconclusive findings, and repeat visits shortly after a RIVR "
        "Tech repair are never billed."])

    section("11. Shared-Responsibility Cases", [
        "When the cause is partly RIVR Tech and partly the premises (e.g., a pre-existing "
        "condition worsened during service), a supervisor reviews the ticket and may apply a "
        "reduced fee or a full waiver."])

    section("12. Inconclusive Findings", [
        "If no clear cause is determined or the issue is not reproduced, there is no charge "
        "unless management approves a charge based on clear, documented evidence."])

    section("13. Inside-Wiring Work", [
        "Inside wiring beyond the demarcation point is the customer's responsibility. Basic "
        "diagnostics may be billable; RIVR Tech does not perform major rewiring, concealed-wiring, "
        "or construction work under this policy."])

    section("14. Customer-Owned Equipment", [
        "RIVR Tech supports connectivity to the demarcation point. Configuration or failure of "
        "customer-owned routers, mesh, and devices is a customer-premises responsibility; a bypass "
        "test proving the RIVR Tech service is healthy must be documented."])

    section("15. RIVR Tech-Owned Equipment", [
        "Failure of RIVR Tech ONTs and gateways is repaired or replaced at no charge, absent "
        "customer damage."])

    section("16. Customer-Damaged Company Equipment", [
        "When a customer damages RIVR Tech equipment (physical, water, pet/pest, unauthorized "
        "modification), a repair/replacement charge may apply, subject to documentation and, for "
        "significant damage, supervisor review and hardship consideration."])

    section("17. Wi-Fi Coverage Limitations", [
        "Wi-Fi coverage depends on home size, construction, and device placement. Coverage "
        "limitations unrelated to the RIVR Tech network are customer-premises matters; visits are "
        "typically educational and often courtesy on first occurrence."])

    section("18. Individual-Device Limitations", [
        "When a single device (old, unsupported, malware-affected) underperforms while the RIVR "
        "Tech service tests at plan speed via a wired connection, the issue is a customer-premises "
        "responsibility."])

    section("19. Equipment Relocation", [
        "Customer-requested relocation of working RIVR Tech equipment is billable starting at "
        "$95 plus materials."])

    section("20. Missed Appointments", [
        "A missed appointment (no authorized adult present, customer not home) may incur a $35 "
        "administrative fee, with a first-time courtesy waiver typically applied."])

    section("21. Denied Access", [
        "If access to the premises or equipment is denied and work cannot be completed, a $35 fee "
        "may apply and the ticket is dispositioned accordingly."])

    section("22. After-Hours Service", [
        "Customer-caused visits performed after standard hours add a $75 surcharge to the standard "
        "fee. RIVR Tech network emergencies remain free at all hours."])

    section("23. Residential Customer Rules", [
        "An authorized adult (18+) must be present. The residential customer-premises fee is $75. "
        "First-incident courtesy, hardship, and accommodation waivers apply."])

    section("24. Business Customer Rules", [
        "The business customer-premises fee is $125. Custom network configuration may be billed at "
        "additional labor or referred to the customer's IT provider. Business SLAs govern where "
        "they conflict; legal review required."])

    section("25. Emergency and Safety Exceptions", [
        "Safety hazards (exposed wiring, fire, electrical, downed lines) are addressed first "
        "regardless of billing. Charges, if any, are reviewed by a supervisor after safety is "
        "ensured."])

    section("26. Hardship and Reasonable-Accommodation Exceptions", [
        "Documented financial hardship (including Lifeline/low-income customers) and disability/"
        "medical accommodations qualify for fee waivers or alternative arrangements, subject to "
        "manager approval."])

    section("27. Advance Customer Disclosure", [
        "Before any dispatch that could result in a charge, support must disclose that a fee may "
        "apply based on the technician's documented findings, and record the customer's "
        "acknowledgment. No fee is valid without proper advance disclosure."])

    section("28. Customer Acknowledgment", [
        "The customer acknowledges only that a charge may apply based on documented findings. The "
        "customer is not required to admit responsibility before the investigation is complete."])

    section("29. Technician Documentation", [
        "Before any fee is assessed, the technician must record findings, test results, and (where "
        "applicable) photographs, using the standardized ticket and billing codes."])

    section("30. Billing Authorization", [
        "A charge is authorized only when the classification, documentation, disclosure, and "
        "required approval level are all satisfied. Technicians never collect cash."])

    section("31. Dispute and Appeal Process", [
        "Customers may dispute any charge. Disputes follow a documented path: frontline explanation "
        "→ supervisor review → technical review → billing adjustment, within a defined response "
        "timeline, with executive escalation criteria for unresolved cases."])

    section("32. Manager Waiver Authority", [
        "Managers may waive fees under defined categories (first-time courtesy, documentation "
        "error, shared responsibility, inconclusive, hardship, accommodation, incorrect disclosure, "
        "repeat failure after a RIVR Tech repair, retention). Waivers are tracked."])

    section("33. Quality-Control Review", [
        "A sample of billable tickets is audited for correct classification, documentation, "
        "disclosure, and coding accuracy. Findings feed coaching and policy refinement."])

    section("34. Policy Review Schedule", [
        "This policy is reviewed at least annually, and after any material change in cost, "
        "regulation, or customer feedback. Version and effective dates are maintained on the cover."])

    h2(doc, "Appendix A — Waiver Categories")
    table(doc, ["Category", "Basis", "Approval"],
          [(a, b, c) for a, b, c in C.WAIVER_CATEGORIES], col_widths=[1.9, 3.2, 1.4], font_size=9)

    h2(doc, "Appendix B — Legal & Regulatory Review Flags")
    table(doc, ["Item", "What to Review", "Owner"],
          [(a, b, c) for a, b, c in C.LEGAL_FLAGS], col_widths=[1.9, 3.3, 1.3], font_size=8.5)
    callout(doc, None, "This policy contains provisions requiring legal, regulatory, accounting, "
            "and insurance review. It is not legal advice.", "legal")

    save(doc, p("RIVR_Tech_Maintenance_Plan", "02_Policy_and_SOP",
                "Customer_Premises_Maintenance_Policy.docx"),
         "Customer-Premises Maintenance Policy")


# ==========================================================================
# 4. SUPPORT & FIELD OPERATIONS SOP
# ==========================================================================
def sop():
    doc = new_doc()
    cover_page(doc, "Support & Field Operations SOP",
               "Remote Triage + Field-Technician Standard Operating Procedures",
               "Operational Procedures for Support, Dispatch, and Field Teams")
    toc_field(doc)

    h1(doc, "Part A — Remote Troubleshooting (Support Triage) SOP")
    para(doc, "Support must complete these steps, when technically appropriate, before any "
              "dispatch. Strong remote troubleshooting is the primary tool for reducing "
              "unnecessary truck rolls.")
    steps = [
        "Verify the customer and account.",
        "Check for a known area or facility outage.",
        "Review service and ticket history for repeats and prior repairs.",
        "Review ONT and gateway status remotely.",
        "Review alarms and optical levels.",
        "Confirm premises power (outlets, strips, adapters).",
        "Confirm cables and connections.",
        "Reboot equipment in the correct order (ONT → gateway → device).",
        "Separate internet-delivery problems from Wi-Fi problems.",
        "Separate whole-home problems from individual-device problems.",
        "Perform an approved speed test.",
        "Request a wired test when available (device connected directly to the gateway).",
        "Identify any third-party networking equipment (mesh, firewall, extenders).",
        "Educate the customer when the issue can be resolved remotely.",
        "Explain potential charges before dispatch and record acknowledgment.",
        "Select the appropriate dispatch and billing code.",
        "Escalate network-related problems to Network Operations.",
    ]
    for s in steps:
        numbered(doc, s)

    h2(doc, "A.1 Triage Decision Tree")
    para(doc, "Use this decision logic after the steps above:")
    tree = [
        ("Resolved remotely?", "Close as remote resolution. Educate. No dispatch."),
        ("Network alarm / optical fault / outage?", "Escalate to Network Operations. Nonbillable dispatch if needed."),
        ("Wired test at gateway = plan speed, problem persists on customer gear?", "Potentially billable dispatch. Disclose fee. Record acknowledgment."),
        ("Whole-home outage, no customer cause visible?", "Nonbillable dispatch (suspected RIVR Tech)."),
        ("Third-party equipment / business custom config?", "Educate; offer referral to third-party IT; potentially billable if RIVR performs work."),
        ("Ambiguous or safety concern?", "Escalate to Supervisor before dispatch."),
    ]
    table(doc, ["Condition", "Route"], tree, col_widths=[3.2, 3.3], font_size=9.5)
    callout(doc, None, "A dispatch code is NOT a billing decision. Billing is determined only "
            "after documented field findings.", "warning")

    h1(doc, "Part B — Field-Technician SOP")
    para(doc, "Field technicians follow this sequence on every trouble visit:")
    fsteps = [
        ("Arrival & customer communication", "Introduce yourself, confirm the reported issue, set expectations. Never use blaming language."),
        ("Review support notes", "Read the triage history, prior tickets, and any disclosure already made."),
        ("Optical testing", "Measure optical levels at the ONT; compare to spec."),
        ("ONT testing", "Confirm ONT status, alarms, and provisioning."),
        ("Gateway testing", "Verify gateway WAN/LAN status and firmware."),
        ("Wired testing", "Run a wired speed test at the gateway to isolate delivery vs. Wi-Fi."),
        ("Wireless testing", "Survey Wi-Fi signal; check bands and placement."),
        ("Customer-owned equipment", "Identify make/model; bypass to prove RIVR Tech service is healthy."),
        ("Inside-wiring evaluation", "Check continuity where relevant; note pre-existing conditions."),
        ("Photographs", "Photograph damage, power issues, and relevant conditions."),
        ("Test-result documentation", "Record all pre/post results in the ticket."),
        ("Ticket disposition", "Select the correct classification and billing code."),
        ("Customer explanation", "Explain findings plainly using 'customer-premises issue' language."),
        ("Electronic acknowledgment", "Capture the customer's acknowledgment that a charge may apply."),
        ("Supervisor review", "Route shared/damage/relocation/repeat items for approval."),
        ("Repeat-ticket handling", "Link prior tickets; waive if it follows a recent RIVR Tech repair."),
        ("Quality audits", "Expect random QA review of documentation and coding accuracy."),
    ]
    for t, d in fsteps:
        para(doc, t, bold=True, size=10.5, color=C.BRAND["secondary"], space_after=1)
        para(doc, d, size=10, space_after=6)

    h2(doc, "B.1 Technicians Must Not")
    for x in ["Collect cash from customers.",
              "Guarantee that a charge will be removed.",
              "Classify a visit as billable without documented evidence.",
              "Use blaming language ('your fault').",
              "Perform unapproved major wiring or construction work."]:
        bullet(doc, x)
    callout(doc, None, "Always say 'customer-premises issue' or 'issue outside the RIVR Tech "
            "network' — never 'customer fault.'", "recommendation")

    h1(doc, "Part C — Ticket & Billing Codes")
    table(doc, ["Code", "Name", "Billable", "Approval", "Billing"],
          [(c[0], c[1], c[3], c[5], c[6]) for c in C.CODES],
          col_widths=[1.0, 1.9, 1.0, 1.3, 1.0], font_size=8.5)
    para(doc, "Full code documentation (descriptions, required documentation, and customer-facing "
              "language) is maintained in the Responsibility Matrix workbook.", size=9, italic=True)

    h1(doc, "Part D — Customer Authorization Language")
    para(doc, "Use the approved disclosure across every channel. The customer acknowledges only "
              "that a charge MAY apply based on documented findings — not that they are at fault.")
    for ch, txt in [
        ("Recorded telephone call", "\"Before we send a technician, I want you to know that if the issue is found to be with equipment or wiring at your home or business — not the RIVR Tech network — a service charge may apply based on what the technician documents. There's no charge if it's our network or equipment. May I note your acknowledgment?\""),
        ("Email", "\"A technician visit may include a service charge only if the documented cause is on your premises (your equipment, wiring, or power). RIVR Tech network and equipment repairs are always free.\""),
        ("SMS", "\"RIVR Tech: A visit fee may apply only if the issue is on your premises (not our network). Reply YES to acknowledge and confirm your appointment.\""),
        ("Customer portal", "\"I understand a service charge may apply only if the documented cause is a customer-premises issue. RIVR Tech network/equipment repairs are free.\""),
        ("Technician work order", "\"Findings recorded on this order determine whether a charge applies. Signing acknowledges the visit and disclosure — not responsibility.\""),
        ("Paper acknowledgment", "\"I acknowledge RIVR Tech disclosed that a charge may apply based on documented findings if the cause is a customer-premises issue.\""),
    ]:
        para(doc, ch, bold=True, size=10, color=C.BRAND["primary"], space_after=1)
        para(doc, txt, size=9.5, space_after=6)
    callout(doc, None, "Call recording, e-acknowledgment (E-SIGN/UETA), and disclosure wording "
            "require legal review.", "legal")

    save(doc, p("RIVR_Tech_Maintenance_Plan", "02_Policy_and_SOP",
                "Support_and_Field_Operations_SOP.docx"), "Support & Field Operations SOP")


# ==========================================================================
# 5. EMPLOYEE QUICK REFERENCE GUIDE
# ==========================================================================
def quick_reference():
    doc = new_doc()
    cover_page(doc, "Employee Quick Reference Guide",
               "Customer-Premises Maintenance Program", "Pocket Guide for All Customer-Facing Roles")

    h1(doc, "The One Rule")
    callout(doc, "REMEMBER", "A fee is NEVER charged just because we sent a technician. A fee "
            "requires a documented customer-premises cause, advance disclosure, and the right "
            "approval.", "recommendation")

    h1(doc, "Free vs. May-Be-Billable (at a glance)")
    table(doc, ["Always FREE ($0)", "May Be Billable"], [
        ("RIVR Tech network outage", "Customer-owned router/mesh failure"),
        ("Failed RIVR Tech ONT / gateway", "Customer-damaged wiring or drop"),
        ("Fiber / normal drop failure", "Premises power problem"),
        ("No trouble found", "Third-party device / camera / firewall setup"),
        ("Inconclusive / not reproduced", "Requested equipment relocation"),
        ("Repeat visit after a RIVR Tech repair", "Missed appointment / denied access"),
    ], col_widths=[3.2, 3.3], font_size=10)

    h1(doc, "The Four Classifications")
    table(doc, ["Classification", "Charge"], [
        ("RIVR Tech responsibility", "$0"),
        ("Customer-premises responsibility", "Fee may apply (with documentation)"),
        ("Shared responsibility", "Supervisor review; reduced/waived"),
        ("Inconclusive", "$0 unless management approves"),
    ], col_widths=[3.0, 3.5], font_size=10)

    h1(doc, "Recommended Fees")
    table(doc, ["Item", "Fee"], [
        ("Residential customer-premises visit", f"${C.RES_FEE}"),
        ("Business customer-premises visit", f"${C.BUS_FEE}"),
        ("Extra labor (per 30 min after first 30)", "$35"),
        ("Missed appointment / denied access", "$35"),
        ("Equipment relocation", "$95 + materials"),
        ("Inside-wiring repair", "$75 + materials"),
        ("After-hours surcharge", "+$75"),
        (f"Protection plan", f"${C.PROTECTION_RECOMMENDED:.2f}/mo"),
    ], col_widths=[3.8, 2.7], font_size=10)

    h1(doc, "Before You Dispatch (Support)")
    for s in ["Run full remote troubleshooting (verify, outage, status, power, reboot, wired test).",
              "Separate internet from Wi-Fi, and whole-home from single-device.",
              "If it could bill, DISCLOSE the possible charge and record acknowledgment.",
              "Pick the correct dispatch + billing code.",
              "Escalate network issues to Network Operations."]:
        bullet(doc, s)

    h1(doc, "On Site (Technician)")
    for s in ["Test optical, ONT, gateway, wired, wireless.",
              "Bypass customer gear to prove the RIVR Tech service is healthy.",
              "Photograph damage / power / wiring conditions.",
              "Document findings + tests, then pick the code.",
              "Explain plainly; capture e-acknowledgment; route approvals.",
              "Never collect cash. Never say 'your fault.'"]:
        bullet(doc, s)

    h1(doc, "Say This, Not That")
    table(doc, ["Say This", "Not That"], [
        ("\"This is a customer-premises issue.\"", "\"This is your fault.\""),
        ("\"The RIVR Tech service tested good.\"", "\"Your stuff is broken.\""),
        ("\"A charge may apply based on findings.\"", "\"You're getting charged.\""),
        ("\"Let me show you how to fix this.\"", "\"There's nothing I can do.\""),
    ], col_widths=[3.3, 3.2], font_size=10)

    h1(doc, "Waivers You Can Point To")
    for a, b, c in C.WAIVER_CATEGORIES:
        bullet(doc, f"{a} — {b} (Approval: {c})")

    save(doc, p("RIVR_Tech_Maintenance_Plan", "04_Training",
                "Employee_Quick_Reference_Guide.docx"), "Employee Quick Reference Guide")


# ==========================================================================
# 6. FACILITATOR & MANAGER COACHING GUIDE
# ==========================================================================
def coaching_guide():
    doc = new_doc()
    cover_page(doc, "Facilitator & Manager Coaching Guide",
               "Customer-Premises Maintenance Program Training",
               "For Trainers, Supervisors, and Managers")
    toc_field(doc)

    h1(doc, "1. How to Use This Guide")
    para(doc, "This guide supports the 60-minute employee training session and ongoing coaching. "
              "It provides facilitation notes, timing, discussion prompts, role-play scenarios, "
              "and coaching rubrics. Pair it with the training deck, quick reference guide, and "
              "knowledge assessment.")

    h1(doc, "2. Session Agenda (60 minutes)")
    table(doc, ["Time", "Segment", "Facilitator Focus"], [
        ("0:00–0:05", "Why the policy is changing", "Frame as fairness + free network repairs, not revenue."),
        ("0:05–0:15", "Free vs. billable + classifications", "Drill the four classifications; use the matrix."),
        ("0:15–0:25", "Remote troubleshooting", "Emphasize deflection; walk the decision tree."),
        ("0:25–0:35", "Advance disclosure + documentation", "No surprise billing; findings before fees."),
        ("0:35–0:45", "Empathetic communication", "'Customer-premises,' never 'fault.' Role-play."),
        ("0:45–0:55", "Billing, disputes, waivers", "Show the dispute path and waiver categories."),
        ("0:55–1:00", "Knowledge check + Q&A", "Administer assessment; confirm passing score."),
    ], col_widths=[1.2, 2.2, 3.1], font_size=9.5)

    h1(doc, "3. Role-Specific Coaching Points")
    roles = [
        ("Customer service", "Lead with what stays free. Practice the disclosure verbatim."),
        ("Technical support", "Master the triage tree; log wired-test results; disclose before dispatch."),
        ("Dispatch", "Match ticket codes to triage findings; flag potential-billable clearly."),
        ("Field technicians", "Document findings/tests/photos first; plain-language explanations."),
        ("Billing", "Only bill fully documented + disclosed + approved tickets."),
        ("Sales", "Position the protection plan honestly — a service plan, not insurance."),
        ("Business-account reps", "Handle SLAs and custom-config referrals; know the $125 fee."),
        ("Supervisors", "Own shared/damage/relocation/repeat approvals and waivers."),
        ("Managers", "Own hardship/accommodation/retention waivers; watch coding accuracy."),
        ("Network operations", "Fast escalation path; confirm network causes to keep visits free."),
        ("Marketing", "Warm, local, simple messaging; publish what stays free."),
    ]
    table(doc, ["Role", "Coaching Point"], roles, col_widths=[2.1, 4.4], font_size=9.5)

    h1(doc, "4. Role-Play Scenarios")
    plays = [
        ("The surprised customer", "Customer expects a free visit; technician found a failed customer router.",
         "Practice: acknowledge feelings, explain findings, note first-time courtesy waiver, offer plan."),
        ("The Wi-Fi complaint", "Slow Wi-Fi far from the gateway in a large home.",
         "Practice: separate internet from Wi-Fi, educate on placement/mesh, keep it non-blaming."),
        ("The disputed charge", "Customer disputes a $75 fee after a documented premises issue.",
         "Practice: frontline explanation, offer supervisor review, explain the dispute timeline."),
        ("The hardship case", "Low-income customer with a genuine premises issue.",
         "Practice: empathy, hardship waiver path, avoid judgment, document the accommodation."),
    ]
    for title, setup, coach in plays:
        para(doc, title, bold=True, size=11, color=C.BRAND["secondary"], space_after=1)
        para(doc, "Setup: " + setup, size=10, space_after=1)
        para(doc, "Coach: " + coach, size=10, italic=True, space_after=6)

    h1(doc, "5. Coaching Rubric (observe & score)")
    table(doc, ["Behavior", "Meets", "Needs Work"], [
        ("Discloses potential charge in advance", "Every eligible ticket", "Skips or is vague"),
        ("Uses 'customer-premises' language", "Consistently", "Uses 'fault'/blaming"),
        ("Documents findings before billing", "Always", "Bills without evidence"),
        ("Selects correct code", ">95% accuracy", "Frequent miscoding"),
        ("Handles disputes calmly", "Follows the path", "Argues or over-promises"),
    ], col_widths=[2.6, 2.0, 1.9], font_size=9.5)

    h1(doc, "6. Common Mistakes to Correct")
    for m in ["Treating every unsuccessful visit as billable.",
              "Forgetting advance disclosure, then trying to bill.",
              "Saying 'your fault' or arguing with the customer.",
              "Billing an inconclusive or no-trouble-found visit.",
              "Skipping the wired test that isolates delivery from Wi-Fi."]:
        bullet(doc, m)

    h1(doc, "7. Reinforcement Plan")
    para(doc, "Weeks 1–2: shadow + live coaching. Weeks 3–4: QA sampling with feedback. Monthly: "
              "review coding accuracy, disclosure compliance, and dispute outcomes; refresh where "
              "KPIs miss target.")
    save(doc, p("RIVR_Tech_Maintenance_Plan", "04_Training",
                "Facilitator_and_Manager_Coaching_Guide.docx"), "Facilitator & Manager Coaching Guide")


# ==========================================================================
# 7. KNOWLEDGE ASSESSMENT
# ==========================================================================
ASSESSMENT = [
    ("A technician is dispatched but finds the RIVR Tech network is the cause. What is the charge?",
     ["$75", "$125", "$0", "Supervisor decides"], "C",
     "RIVR Tech network/equipment problems are always free."),
    ("What must exist before any fee is assessed?",
     ["A dispatch", "Documented findings + disclosure + approval", "A customer complaint", "A manager's mood"], "B",
     "A fee requires documented customer-premises findings, advance disclosure, and approval."),
    ("A visit is 'inconclusive.' Default billing outcome?",
     ["$75", "$0 unless management approves on clear evidence", "$35", "Always billable"], "B",
     "Inconclusive = no charge unless management approves on clear evidence."),
    ("Which phrase is approved?",
     ["'This is your fault.'", "'Your equipment is broken.'", "'This is a customer-premises issue.'", "'You broke it.'"], "C",
     "Use 'customer-premises issue,' never blaming language."),
    ("Recommended residential customer-premises visit fee?",
     ["$50", "$75", "$95", "$125"], "B", "Balanced posture: $75 residential."),
    ("Recommended business customer-premises visit fee?",
     ["$75", "$99", "$125", "$150"], "C", "Balanced posture: $125 business."),
    ("A customer's first customer-caused incident. What often applies?",
     ["Double fee", "One-time educational courtesy waiver", "Immediate disconnection", "After-hours surcharge"], "B",
     "First-incident courtesy waiver when appropriate."),
    ("Before dispatch, support must do what regarding charges?",
     ["Nothing", "Disclose that a charge may apply and record acknowledgment", "Guarantee no charge", "Collect payment"], "B",
     "Advance disclosure prevents surprise billing."),
    ("Which is ALWAYS free?",
     ["Customer-owned router failure", "Equipment relocation", "No trouble found", "Inside-wiring repair"], "C",
     "No-trouble-found visits are never billed."),
    ("What proves the RIVR Tech service is healthy at the premises?",
     ["A reboot", "A wired test at the gateway meeting plan speed", "Customer's word", "A photo of the router"], "B",
     "A wired test isolates delivery from Wi-Fi/device issues."),
    ("Technicians may NOT:",
     ["Take photos", "Collect cash", "Run tests", "Explain findings"], "B",
     "Technicians never collect cash."),
    ("A customer disputes a charge. First step?",
     ["Disconnect service", "Frontline explanation, then supervisor review", "Ignore it", "Refer to legal immediately"], "B",
     "Disputes start with frontline explanation and escalate through supervisor/technical review."),
    ("Missed appointment or denied access fee?",
     ["$0 always", "$35 (often courtesy first time)", "$125", "$95"], "B",
     "$35 administrative fee with typical first-time courtesy."),
    ("The protection plan is best described as:",
     ["Insurance", "A warranty", "An optional service/maintenance plan", "A loan"], "C",
     "It is a service plan — NOT insurance or a warranty."),
    ("After-hours customer-caused visit pricing?",
     ["Free", "Standard fee + $75 surcharge", "$35 flat", "$10"], "B",
     "Standard fee plus a $75 after-hours surcharge."),
    ("Shared-responsibility case handling?",
     ["Always full fee", "Supervisor review; reduced fee or waiver may apply", "Always free", "Customer decides"], "B",
     "Shared responsibility → supervisor review; reduced or waived."),
    ("Which requires photographs per policy?",
     ["Every visit", "Physical damage / power / wiring conditions", "Only network outages", "Never"], "B",
     "Damage, power, and wiring conditions require photos to support any charge."),
    ("A repeat visit shortly after a RIVR Tech repair is:",
     ["Billable", "Free (auto-waiver)", "$35", "Supervisor's choice"], "B",
     "Repeat after a RIVR Tech repair is not billed."),
]


def assessment():
    doc = new_doc()
    cover_page(doc, "Employee Knowledge Assessment",
               "Customer-Premises Maintenance Program", "Assessment + Answer Key (Passing Score: 80%)")

    h1(doc, "Instructions")
    para(doc, f"This assessment has {len(ASSESSMENT)} questions. Choose the single best answer. "
              f"A passing score is 80% ({int(round(len(ASSESSMENT)*0.8))} of {len(ASSESSMENT)} "
              f"correct). Employees in customer-facing roles must pass before the program's "
              f"effective date. Retakes are permitted after coaching.")

    h1(doc, "Assessment")
    for i, (q, opts, ans, exp) in enumerate(ASSESSMENT, 1):
        para(doc, f"{i}. {q}", bold=True, size=10.5, space_after=1)
        for j, opt in enumerate(opts):
            letter = "ABCD"[j]
            bullet(doc, f"{letter}. {opt}")
    doc.add_page_break()

    h1(doc, "Answer Key")
    key_rows = []
    for i, (q, opts, ans, exp) in enumerate(ASSESSMENT, 1):
        key_rows.append((str(i), ans, exp))
    table(doc, ["#", "Answer", "Explanation"], key_rows, col_widths=[0.5, 0.9, 5.1], font_size=9)

    h1(doc, "Scoring")
    table(doc, ["Score", "Result", "Action"], [
        (f"{int(round(len(ASSESSMENT)*0.8))}+/{len(ASSESSMENT)} (80%+)", "Pass", "Cleared for the program."),
        (f"< 80%", "Not yet", "Coaching + retake before effective date."),
    ], col_widths=[1.8, 1.3, 3.4], font_size=10)

    save(doc, p("RIVR_Tech_Maintenance_Plan", "04_Training",
                "Employee_Knowledge_Assessment.docx"), "Employee Knowledge Assessment")


# ==========================================================================
# 8. CUSTOMER COMMUNICATION PACKAGE
# ==========================================================================
FAQS = [
    ("Is RIVR Tech charging for all service visits now?",
     "No. RIVR Tech network and equipment repairs are always free. A charge may apply only when a documented issue is on your premises — your equipment, wiring, or power."),
    ("What does RIVR Tech still fix for free?",
     "Network outages, failed RIVR Tech ONTs and gateways, fiber and normal drop failures, no-trouble-found visits, and repeat visits after a RIVR Tech repair."),
    ("When could a visit be billable?",
     "When the documented cause is a customer-premises issue: customer-owned equipment, customer-damaged wiring, premises power problems, third-party device setup, or a requested equipment relocation."),
    ("How much is a customer-premises visit?",
     f"${C.RES_FEE} for residential and ${C.BUS_FEE} for business, plus any materials. Other fees (relocation, inside wiring, after-hours) are disclosed in advance."),
    ("Will I be surprised by a charge?",
     "No. We disclose any potential charge before we send a technician and ask you to acknowledge it. You are only acknowledging that a charge may apply based on findings — not admitting fault."),
    ("What if the technician can't find the problem?",
     "If findings are inconclusive or no trouble is found, there is no charge."),
    ("What's the difference between internet and Wi-Fi?",
     "Internet is the connection RIVR Tech delivers to your home. Wi-Fi is the wireless signal inside your home, which is affected by your devices, walls, and layout."),
    ("Why is my Wi-Fi slow in one room?",
     "Wi-Fi weakens with distance and through walls. A wired test at the gateway usually shows full speed. We can suggest placement changes, mesh, or extenders."),
    ("Can one old device slow everything down?",
     "An old or unsupported device can limit its own speed. The RIVR Tech connection can still be delivering full plan speed to other devices."),
    ("How do I reboot my equipment?",
     "Power off the ONT, then the gateway; wait 30 seconds; power the ONT back on, then the gateway; then restart your device."),
    ("How are charges determined?",
     "Only after a technician documents findings, test results, and (where relevant) photos, and the visit is classified as a customer-premises responsibility."),
    ("How do I dispute a charge?",
     "Contact RIVR Tech. We start with a frontline explanation, then supervisor and technical review, and adjust billing if warranted, within a defined timeline."),
    ("Do you offer any way to avoid these charges?",
     f"Yes — the optional RIVR Tech Home Maintenance Protection plan (${C.PROTECTION_RECOMMENDED:.2f}/month) covers standard customer-premises visits and more."),
    ("Is the protection plan insurance?",
     "No. It is an optional service and maintenance plan, not insurance or a warranty."),
    ("What does the protection plan cover?",
     "Standard customer-premises trouble visits, basic inside-wiring diagnostics, Wi-Fi education, basic device-connection help, and priority scheduling."),
    ("What is not covered by the plan?",
     "Replacing your own devices, major rewiring, concealed wiring, construction, commercial network administration, willful damage, and fire or flood damage."),
    ("What if I miss my appointment?",
     "A $35 fee may apply, and we typically waive it the first time. Please let us know if you need to reschedule."),
    ("I have a disability or financial hardship. Can you help?",
     "Yes. We offer reasonable accommodations and hardship waivers. Please tell us so we can help."),
    ("Does this apply to my business service?",
     "Business customer-premises visits are $125. Custom network configuration may be additional or referred to your IT provider. Your service agreement governs where applicable."),
    ("When does this start?",
     "After a customer-education period and a 30-day warning-only grace period, during which we explain charges but do not bill customer-premises visits."),
    ("What if the same problem comes back after a RIVR Tech repair?",
     "If it recurs shortly after we repaired something, there is no charge."),
    ("Will my rates go up because of this?",
     "No. This program does not change your monthly service rate. It only introduces fees for specific customer-premises visits, which you can avoid with self-service or the optional plan."),
]


def customer_package():
    doc = new_doc()
    cover_page(doc, "Customer Communication Package",
               "Customer-Premises Maintenance Program",
               "Templates for a 60-Day Customer Education Program")
    toc_field(doc)

    h1(doc, "1. 60-Day Customer Education Plan")
    table(doc, ["Days", "Channel", "Message"], [
        ("Day 1–10", "Website + Customer portal", "Publish the policy, FAQs, and 'what stays free.'"),
        ("Day 5–15", "Email #1", "Announcement: fairer program, network repairs stay free."),
        ("Day 10–20", "Bill message", "Short notice + link to learn more."),
        ("Day 15–30", "Social media", "Warm, local posts: internet vs. Wi-Fi, self-help tips."),
        ("Day 20–35", "Bill insert", "One-page explainer mailed with statements."),
        ("Day 25–40", "IVR / hold message", "Brief spoken summary + where to learn more."),
        ("Day 30–45", "Email #2", "Reminder + protection-plan introduction."),
        ("Day 35–50", "Technician leave-behind", "Handout at every visit."),
        ("Day 40–55", "New-customer materials", "Include disclosure in onboarding."),
        ("Day 45–60", "Business-customer letter", "Direct outreach to business accounts."),
    ], col_widths=[1.3, 1.9, 3.3], font_size=9.5)
    callout(doc, "RECOMMENDATION", "Keep every message warm, local, simple, and respectful. Lead "
            "with what stays free. Never lead with fees.", "recommendation")

    h1(doc, "2. Policy Announcement")
    para(doc, f"A Fairer, Clearer Way to Handle Service Visits", bold=True, size=12, color=C.BRAND["primary"])
    para(doc, f"At {C.COMPANY_SHORT}, keeping your neighbors connected is personal. That's why "
              f"repairs to the {C.COMPANY_SHORT} network and equipment will always be free. "
              f"Starting soon, a fair service charge may apply only when a documented problem is "
              f"on your side — your own equipment, wiring, or power. We'll always tell you before "
              f"we send a technician, and there's never a charge if it's our network. You'll also "
              f"be able to choose an optional low-cost protection plan for extra peace of mind.")

    h1(doc, "3. Customer Email")
    para(doc, "Subject: Free network repairs — and a clearer, fairer service-visit policy", bold=True, size=10.5)
    para(doc, f"Dear [Customer Name],")
    para(doc, f"We're writing to share a clearer, fairer approach to service visits. {C.COMPANY_SHORT} "
              f"network and equipment repairs remain free — always. A service charge may apply only "
              f"when a technician documents that the cause is on your premises (for example, your "
              f"own router, inside wiring, or a power issue). We will always disclose any potential "
              f"charge before we dispatch, and there is no charge for inconclusive or no-trouble-"
              f"found visits.")
    para(doc, f"To help you avoid charges, we're offering an optional RIVR Tech Home Maintenance "
              f"Protection plan for ${C.PROTECTION_RECOMMENDED:.2f}/month. Learn more at [link].")
    para(doc, f"Questions? We're local, and we're here to help. — The {C.COMPANY_SHORT} Team")

    h1(doc, "4. Bill Message")
    para(doc, f"\"Good news: {C.COMPANY_SHORT} network & equipment repairs are always free. A fair "
              f"charge may apply only for documented customer-premises visits. We'll always tell "
              f"you first. Learn more: [link].\"", italic=True)

    h1(doc, "5. Bill Insert (one page)")
    para(doc, "What RIVR Tech maintains (free):", bold=True, color=C.BRAND["good"])
    for x in ["The RIVR Tech network, fiber, and drops", "Your RIVR Tech ONT and gateway", "No-trouble-found and inconclusive visits"]:
        bullet(doc, x)
    para(doc, "What you maintain (may be billable if we're dispatched):", bold=True, color=C.BRAND["warn"])
    for x in ["Your own router, mesh, and devices", "Inside wiring and premises power", "Third-party cameras, TVs, and smart-home gear"]:
        bullet(doc, x)
    para(doc, "Before any charge, we disclose it and document findings. Ask about the optional "
              f"protection plan (${C.PROTECTION_RECOMMENDED:.2f}/mo).")

    h1(doc, "6. Website Policy (customer-facing summary)")
    para(doc, f"{C.COMPANY_SHORT} keeps all network and equipment repairs free. When a documented "
              f"issue is on your premises, a fair service charge may apply: ${C.RES_FEE} residential "
              f"/ ${C.BUS_FEE} business, plus materials for relocation or inside wiring. We disclose "
              f"potential charges in advance, never bill inconclusive visits, and offer courtesy, "
              f"hardship, and accommodation waivers. An optional protection plan is available.")

    h1(doc, "7. Frequently Asked Questions")
    for i, (q, a) in enumerate(FAQS, 1):
        para(doc, f"Q{i}. {q}", bold=True, size=10, color=C.BRAND["secondary"], space_after=1)
        para(doc, a, size=10, space_after=6)

    h1(doc, "8. Call-Center Script")
    para(doc, "Opening: \"Thanks for calling RIVR Tech, this is [name]. I can help with that.\"")
    para(doc, "Disclosure (if potentially billable): \"Before I schedule a technician, I want to be "
              "upfront: if the technician documents that the cause is on your premises — like your "
              "own equipment, wiring, or power — a service charge may apply. If it's our network or "
              "equipment, there's no charge. Is it okay if I note your acknowledgment?\"")
    para(doc, "Close: \"You'll only be charged if findings show a customer-premises cause, and we'll "
              "explain everything. Would an optional protection plan be helpful for peace of mind?\"")

    h1(doc, "9. Dispatch Disclosure (verbatim)")
    para(doc, "\"A service charge may apply only if the technician documents a customer-premises "
              "cause. RIVR Tech network/equipment repairs are free. Do you acknowledge this "
              "disclosure?\"", italic=True)

    h1(doc, "10. SMS Confirmation")
    para(doc, f"\"RIVR Tech: Appt confirmed for [date/time]. A visit fee may apply only if the issue "
              f"is on your premises (not our network). Reply YES to acknowledge. Reply R to "
              f"reschedule.\"", italic=True)

    h1(doc, "11. Technician Script (on site)")
    para(doc, "\"Here's what I found and tested. The RIVR Tech service is testing good to your "
              "gateway. The issue is a customer-premises one — [plain explanation]. Because of that, "
              "a service charge may apply. I'll document everything, and you can always ask about a "
              "waiver or the protection plan.\"", italic=True)

    h1(doc, "12. Charge Notice")
    para(doc, f"\"Following your recent visit on [date], our documented findings show a customer-"
              f"premises cause ([code/summary]). A service charge of ${C.RES_FEE} applies and will "
              f"appear on your next statement. If you have questions or wish to dispute, contact us "
              f"within [timeline].\"", italic=True)

    h1(doc, "13. Dispute Acknowledgment")
    para(doc, "\"We've received your dispute regarding the charge on [date]. A supervisor will "
              "review the technician's findings and respond within [timeline]. No collection action "
              "occurs while your dispute is under review.\"", italic=True)

    h1(doc, "14. Approved Waiver Notice")
    para(doc, "\"Good news — we've waived the service charge from your visit on [date] as a "
              "[courtesy/hardship/accommodation]. No action is needed. Thank you for being a RIVR "
              "Tech customer.\"", italic=True)

    h1(doc, "15. Denied Dispute Notice")
    para(doc, "\"We carefully reviewed your dispute and the technician's documented findings "
              "([summary]). The customer-premises charge stands. Here's what we found: [detail]. "
              "You may escalate to [role] within [timeline].\"", italic=True)

    h1(doc, "16. Business-Customer Letter")
    para(doc, f"Dear [Business Name], As part of a clearer service-visit policy, {C.COMPANY_SHORT} "
              f"will continue to repair all network and equipment issues at no charge. Documented "
              f"customer-premises visits are billed at ${C.BUS_FEE}; custom network configuration "
              f"may be additional or referred to your IT provider. Your service agreement governs "
              f"where applicable. Ask about priority protection options for your accounts.")

    h1(doc, "17. New-Customer Disclosure")
    para(doc, f"\"Welcome to {C.COMPANY_SHORT}! Please note: our network and equipment repairs are "
              f"always free. If a future visit documents a customer-premises cause (your equipment, "
              f"wiring, or power), a service charge may apply — always disclosed in advance. An "
              f"optional protection plan is available.\"", italic=True)

    h1(doc, "18. Protection-Plan Sales Script")
    para(doc, f"\"For ${C.PROTECTION_RECOMMENDED:.2f} a month, RIVR Tech Home Maintenance Protection "
              f"covers standard customer-premises trouble visits, basic inside-wiring diagnostics, "
              f"Wi-Fi education, and basic device help, with priority scheduling. It's an optional "
              f"service plan — not insurance — and it can save you money if you ever need a premises "
              f"visit. Would you like to add it?\"", italic=True)
    callout(doc, None, "All customer-facing wording, disclosures, call recording, and the "
            "protection-plan description require legal and insurance review before use.", "legal")

    save(doc, p("RIVR_Tech_Maintenance_Plan", "05_Customer_Communications",
                "Customer_Communication_Package.docx"), "Customer Communication Package")


# ==========================================================================
# 9. CUSTOMER MAINTENANCE HANDOUT (leave-behind)
# ==========================================================================
def customer_handout():
    doc = new_doc()
    # Compact 2-page leave-behind, no cover
    para(doc, C.COMPANY_SHORT, bold=True, size=26, color=C.BRAND["primary"], space_after=0)
    para(doc, "Your Guide to Service Visits — What's Free, What's Not, and How to Save",
         bold=True, size=13, color=C.BRAND["secondary"])
    _hr(doc)

    para(doc, "We're your local broadband team. Keeping the RIVR Tech network and your RIVR Tech "
              "equipment working is always free. Here's how service visits work.", size=10.5)

    h2(doc, "Always Free")
    for x in ["RIVR Tech network outages", "Failed RIVR Tech ONT or gateway",
              "Fiber and normal drop repairs", "No-trouble-found and inconclusive visits",
              "Repeat visits after a RIVR Tech repair"]:
        bullet(doc, x)

    h2(doc, "May Have a Charge (we always tell you first)")
    for x in ["Your own router, mesh, or devices", "Inside wiring or premises power",
              "Third-party cameras, TVs, gaming, smart-home setup",
              "Requested equipment relocation", "Missed appointment or denied access"]:
        bullet(doc, x)
    para(doc, f"Residential visit: ${C.RES_FEE}   •   Business visit: ${C.BUS_FEE}   •   "
              f"Materials extra for relocation/wiring", bold=True, size=10, color=C.BRAND["dark"])

    h2(doc, "Internet vs. Wi-Fi (a quick tip)")
    para(doc, "Internet is what we deliver to your home. Wi-Fi is the wireless signal inside your "
              "home — it's affected by walls, distance, and your devices. A wired test at the "
              "gateway usually shows full speed even when Wi-Fi feels slow in a far room.", size=10)

    h2(doc, "Try This First (it often fixes it)")
    for x in ["Power off the ONT, then the gateway.", "Wait 30 seconds.",
              "Power the ONT back on, then the gateway.", "Restart your device and reconnect."]:
        numbered(doc, x)

    h2(doc, "Save With Optional Protection")
    para(doc, f"RIVR Tech Home Maintenance Protection — ${C.PROTECTION_RECOMMENDED:.2f}/month. Covers "
              f"standard customer-premises visits, basic inside-wiring diagnostics, Wi-Fi education, "
              f"and basic device help, with priority scheduling. It's a service plan, not insurance. "
              f"Ask us to add it.", size=10.5)

    h2(doc, "Questions or a Charge to Discuss?")
    para(doc, "Call us — we're local and here to help. We offer courtesy, hardship, and "
              "accommodation waivers, and a fair dispute process. You're never charged just because "
              "we sent a technician; a charge requires documented findings.", size=10)
    callout(doc, None, "Customer-facing handout — wording and the protection-plan description "
            "require legal and insurance review before printing.", "legal")

    save(doc, p("RIVR_Tech_Maintenance_Plan", "05_Customer_Communications",
                "Customer_Maintenance_Handout.docx"), "Customer Maintenance Handout")


if __name__ == "__main__":
    print("Building Word documents...")
    business_case()
    exec_summary()
    policy()
    sop()
    quick_reference()
    coaching_guide()
    assessment()
    customer_package()
    customer_handout()
    print("Word documents complete.")
