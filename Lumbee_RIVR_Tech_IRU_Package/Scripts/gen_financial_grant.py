"""
gen_financial_grant.py
======================
Generates two documents for the Lumbee Tribe of North Carolina / RIVR Tech
broadband IRU package:

  Deliverable 5 — 02_Core_Agreements/04_Financial_and_Revenue_Sharing_Schedule.docx
  Deliverable 6 — 02_Core_Agreements/05_TBCP_Grant_Compliance_and_Federal_Interest_Addendum.docx

All formatting, party names, defined terms, placeholders, flags, and citations
come from the canonical module Scripts/common.py (single source of truth).

These are DRAFT working documents — not final legal advice. Economics are NOT
finalized; unresolved items are marked with flags and yellow placeholders.
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, "/home/user/claude-skills/Lumbee_RIVR_Tech_IRU_Package/Scripts")
import common as C


# ---------------------------------------------------------------------------
# Convenience wrappers
# ---------------------------------------------------------------------------
def P(doc, text, **kw):
    return C.para(doc, text, **kw)


def SUB(doc, label, body):
    return C.subsection(doc, label, body)


# ===========================================================================
#  DELIVERABLE 5 — FINANCIAL & REVENUE-SHARING SCHEDULE
# ===========================================================================
def build_financial_schedule():
    doc = C.new_doc()

    C.add_cover(
        doc,
        "DELIVERABLE 5 · SCHEDULE 04 TO THE CORE AGREEMENTS",
        "Financial and Revenue-Sharing Schedule",
        "Consideration, Payment Structures, Definitions, and Financial Controls "
        "for the Indefeasible Right of Use (IRU) and Operating Arrangement",
    )
    C.setup_header_footer(doc, "Financial & Revenue-Sharing Schedule")
    C.add_toc(doc)

    # ---- Preamble ---------------------------------------------------------
    C.status_banner(doc)
    C.spacer(doc, 1)
    P(doc,
      f"This Financial and Revenue-Sharing Schedule (this “Schedule”) is Schedule 04 "
      f"to, and is incorporated by reference into, the Indefeasible Right of Use and "
      f"Operating Agreement and the other Core Agreements (collectively, the "
      f"“Agreement”) entered into as of {C.PH('Effective Date')} (the “Effective Date”) "
      f"by and between {C.TRIBE_FULL} (the “{C.TRIBE_SHORT}”), or "
      f"{C.TRIBE_ENTITY_ALT}, and {C.OPERATOR_FULL} (“{C.OPERATOR_SHORT}”). The "
      f"{C.TRIBE_SHORT} and {C.OPERATOR_SHORT} are each a “{C.PARTY_SINGULAR}” and "
      f"together the “{C.PARTIES_COLLECTIVE}.” Capitalized terms used but not defined "
      f"in this Schedule have the meanings given in the Agreement.")
    C.spacer(doc, 1)

    # ============ ARTICLE 1 ============
    C.article(doc, 1, "Purpose, Scope, and Relationship to Other Documents")

    C.section(doc, "1.1", "Purpose",
              f"This Schedule sets forth the financial consideration for the {C.IRU_TERM_DEFINED}, "
              f"the alternative payment and revenue-sharing structures under evaluation, the "
              f"defined revenue and expense terms on which every such structure depends, and the "
              f"financial-control, audit, reconciliation, and reserve mechanics that apply once "
              f"a structure is selected. This Schedule governs the flow of money between the "
              f"{C.PARTIES_COLLECTIVE}; it does not modify the grant-compliance obligations, which "
              f"are addressed in the TBCP Grant Compliance and Federal Interest Addendum "
              f"(Deliverable 6).")

    C.section(doc, "1.2", "Relationship to the Financial Model")
    P(doc,
      f"The dollar figures, rate assumptions, take-rate ramps, ARPU inputs, expense "
      f"allocations, reserve balances, and payment computations referenced in this Schedule "
      f"are maintained in, and MUST correspond to, the separate financial model workbook "
      f"delivered as {C.PH('04_Financial_Model (Financial Model workbook)')} (the “Financial "
      f"Model”). Where this Schedule states a mechanism (for example, “{C.DEAL['rev_share_pct_placeholder']} "
      f"of Gross Revenue”), the corresponding calculated amounts, sensitivities, and year-by-year "
      f"schedules live in the Financial Model. In the event of any arithmetic inconsistency "
      f"between an illustrative figure in this Schedule and the Financial Model, the "
      f"{C.PARTIES_COLLECTIVE} shall conform the figure to the Financial Model as updated with "
      f"final, negotiated inputs.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                "The economics in this Schedule are not finalized. The specific payment amount, "
                "revenue-share percentage, cash-flow-share percentage, fixed base, threshold, and "
                "reserve funding rate are open business points to be fixed in negotiation and "
                "carried into the Financial Model.")

    C.section(doc, "1.3", "Draft and Placeholder Nature")
    P(doc,
      "This Schedule is a working draft. Bracketed, highlighted items denote placeholders for "
      "figures or terms that are not yet fixed. Flag markers denote items requiring business, "
      "legal, grant-compliance, or technical review before execution. No figure in this "
      "Schedule is binding until the Agreement is executed and the Financial Model inputs are "
      "final.")

    C.section(doc, "1.4", "Program Income — Threshold Compliance Note")
    P(doc,
      f"Revenue derived from, or generated by the use of, the {C.TRIBAL_ASSETS} (the "
      f"grant-funded infrastructure owned by the {C.TRIBE_SHORT}) may constitute "
      f"“{C.PROGRAM_INCOME}” within the meaning of {C.CITES['prog_income']}. Program "
      f"income is NOT the {C.TRIBE_SHORT}’s unrestricted revenue: it must be identified, "
      f"tracked, and applied in accordance with the {C.PROGRAM_SHORT} Award and the method "
      f"(deduction, addition, or cost-sharing/matching) specified or approved by "
      f"{C.AGENCY_SHORT}. Every payment structure in this Schedule is therefore subject to, and "
      f"must be reconciled against, the program-income treatment set out in Article 4 of this "
      f"Schedule and Article 5 of the Grant Compliance Addendum.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Confirm with grant counsel and NTIA which program-income method (deduction, "
                "addition, or cost sharing) applies to revenue generated by the Tribal Assets, and "
                "whether that treatment continues after the period of performance. The selected "
                "payment structure must not cause the Lumbee Tribe to mis-apply program income.")

    # ============ ARTICLE 2 ============
    C.article(doc, 2, "Definitions — Revenue, Exclusions, and Expenses")
    P(doc,
      "The following definitions are common to all payment structures in Article 3. A single "
      "defined-term set prevents the arithmetic from changing merely because a different "
      "structure is selected.")

    C.section(doc, "2.1", "Gross Revenue")
    P(doc,
      f"“Gross Revenue” means all revenue actually received by {C.OPERATOR_SHORT} (and its "
      f"affiliates, to the extent derived from the {C.NETWORK} or the {C.TRIBAL_ASSETS}), "
      f"determined on an accrual basis in accordance with U.S. generally accepted accounting "
      f"principles (“GAAP”), from the sale, resale, or provision of broadband, data, "
      f"transport, voice, video, and related communications services and facilities over or by "
      f"means of the {C.NETWORK}, before deduction of any Operating Expenses, and INCLUDING the "
      f"following components:")
    C.bullet(doc, "Recurring subscription revenue for residential and business Internet-access and data services;")
    C.bullet(doc, "Installation Revenue (as defined in Section 2.2);")
    C.bullet(doc, "Voice Revenue (as defined in Section 2.3);")
    C.bullet(doc, "Equipment Revenue (as defined in Section 2.4);")
    C.bullet(doc, "Late Fees (as defined in Section 2.5);")
    C.bullet(doc, "Wholesale Revenue and Enterprise Revenue (as defined in Sections 2.14 and 2.15); and")
    C.bullet(doc, "Any other consideration received for use of, or access to, the Network, however characterized, that is not an item of Excluded Revenue under Section 2.6.")

    C.section(doc, "2.2", "Installation Revenue")
    P(doc,
      "“Installation Revenue” means non-recurring charges billed to and collected from "
      "subscribers or third parties for service installation, activation, connection, drop "
      "construction, and premises equipment set-up. Installation Revenue is INCLUDED in Gross "
      "Revenue when and to the extent it is not reimbursed from, or already counted as, grant "
      "funds under Section 2.6(a).")

    C.section(doc, "2.3", "Voice Revenue")
    P(doc,
      "“Voice Revenue” means recurring and usage-based charges for interconnected VoIP, "
      "fixed voice, and related telephony services provided over the Network, net of the "
      "regulatory pass-through amounts excluded under Section 2.6(b). Voice Revenue is INCLUDED "
      "in Gross Revenue.")

    C.section(doc, "2.4", "Equipment Revenue")
    P(doc,
      "“Equipment Revenue” means amounts billed to subscribers or third parties for the "
      "sale, lease, or rental of customer-premises equipment (routers, optical network "
      "terminals, mesh units, and similar devices). Equipment Revenue is INCLUDED in Gross "
      "Revenue. Refundable equipment deposits are excluded until forfeited or applied.")

    C.section(doc, "2.5", "Late Fees")
    P(doc,
      "“Late Fees” means administrative charges billed for delinquent payment, "
      "reconnection, and returned-payment handling. Late Fees are INCLUDED in Gross Revenue "
      "when actually collected, and are excluded to the extent later reversed or refunded.")

    C.section(doc, "2.6", "Excluded Revenue")
    P(doc,
      "“Excluded Revenue” means, without duplication, the following, each of which is "
      "EXCLUDED from Gross Revenue:")
    SUB(doc, "a", f"Grant Funds — NEVER Revenue. Any funds received from or through the "
                  f"{C.PROGRAM_SHORT} Award, any other federal, state, Tribal, or philanthropic "
                  f"grant, subsidy, or contribution-in-aid-of-construction, and any matching or "
                  f"cost-share funds. Grant funds are capital sources for building the "
                  f"{C.TRIBAL_ASSETS}; they are NOT operating revenue and shall never be included "
                  f"in Gross Revenue, in the payment base of any structure in Article 3, or in the "
                  f"{C.OPERATOR_SHORT} cash-flow computation. Grant funds may, however, constitute "
                  f"{C.PROGRAM_INCOME} to the extent they generate revenue — see Section 1.4 and "
                  f"Article 4.")
    SUB(doc, "b", "Taxes (Excluded Pass-Through). Sales, use, excise, gross-receipts, universal-"
                  "service, 911, right-of-way, franchise, and similar taxes, fees, and surcharges "
                  "that are billed to and collected from subscribers for remittance to a taxing or "
                  "regulatory authority, and that are in fact remitted. Amounts retained by "
                  f"{C.OPERATOR_SHORT} (for example, a billing or administrative fee it is permitted "
                  "to keep) are NOT excluded.")
    SUB(doc, "c", "Refunds. Amounts credited, rebated, or refunded to subscribers, and adjustments "
                  "for billing errors, to the extent those amounts were previously included in Gross "
                  "Revenue. Refunds are a deduction from Gross Revenue in the period in which they "
                  "are made, not a separate expense.")
    SUB(doc, "d", "Bad Debt. Amounts billed but not collected and written off as uncollectible in "
                  "accordance with a consistently applied write-off policy, up to a cap of "
                  f"{C.PH('bad-debt cap, e.g., 2% of Gross Revenue per year')}; recoveries of "
                  "previously written-off amounts are added back to Gross Revenue when received. "
                  "Because Gross Revenue is measured on an accrual basis, bad-debt treatment "
                  "prevents the payment base from including cash the Operator never receives.")
    SUB(doc, "e", "Non-operating and extraordinary items. Interest income, gains on asset sales, "
                  "insurance proceeds (except business-interruption proceeds that replace excluded "
                  "operating revenue), and intercompany financing receipts.")

    C.section(doc, "2.7", "Capital Expenses")
    P(doc,
      "“Capital Expenses” (or “CapEx”) means expenditures that are capitalized "
      "under GAAP, including network construction, fiber and electronics, capitalized labor, and "
      "capital improvements. Capital Expenses are NOT deducted in computing Gross Revenue, are "
      "not Operating Expenses, and are addressed separately in the Adjusted Operating Cash Flow "
      "definition (Section 2.13) and the capital-replacement reserve (Section 4.7). CapEx funded "
      "by grant funds is tracked as part of the Tribal Assets, not as an Operator cost recoverable "
      "against the payment base.")

    C.section(doc, "2.8", "Operating Expenses")
    P(doc,
      "“Operating Expenses” (or “OpEx”) means the ordinary, necessary, and "
      "documented cash costs of operating and maintaining the Network in the ordinary course, "
      "determined under GAAP and consistently applied, including network operations and "
      "maintenance, transport and backhaul, power and colocation, customer support and billing, "
      "field labor, vehicle and fuel, software and licensing, insurance premiums allocable to the "
      "Network, property taxes on the Tribal Assets, and bad-debt expense to the extent not "
      "already excluded under Section 2.6(d). Operating Expenses EXCLUDE: Capital Expenses; "
      "depreciation and amortization; income taxes; financing costs and interest; related-party "
      "charges in excess of the arm’s-length standard (Section 2.11); and corporate overhead in "
      "excess of the cap and allocation method (Section 2.12).")

    C.section(doc, "2.9", "Shared Expenses")
    P(doc,
      f"“Shared Expenses” means Operating Expenses that benefit both the {C.TRIBAL_ASSETS} "
      f"and the {C.OPERATOR_EXISTING} (or other {C.OPERATOR_SHORT} operations) and therefore must "
      f"be allocated rather than charged in full to the Network. Shared Expenses shall be "
      f"allocated on a consistent, documented, and auditable basis that reasonably reflects "
      f"relative use — for example, by proportional route-miles, subscriber count, circuit "
      f"count, or capacity — with the allocation methodology disclosed in the Financial Model "
      f"and fixed at {C.PH('agreed allocation basis and driver')}. No Shared Expense may be "
      f"charged more than once, whether to the Network, to another cost center, or to a federal "
      f"award.")

    C.section(doc, "2.10", "Related-Party Charges (Arm’s-Length Standard)")
    P(doc,
      f"“Related-Party Charges” means any charge, fee, price, or cost billed to the "
      f"Network by {C.OPERATOR_SHORT} or any of its affiliates, members, or commonly controlled "
      f"entities (including the parent electric cooperative and its subsidiaries). Related-Party "
      f"Charges are recognized as Operating Expenses ONLY to the extent they do not exceed the "
      f"price that would be charged in an arm’s-length transaction between unrelated parties "
      f"for comparable goods or services, and only to the extent supported by contemporaneous, "
      f"auditable documentation. Any Related-Party Charge in excess of the arm’s-length "
      f"standard is disregarded in every payment computation. This standard applies in addition "
      f"to — and does not displace — the federal cost-reasonableness and cost-allocation "
      f"requirements referenced in the Grant Compliance Addendum.")

    C.section(doc, "2.11", "Corporate Overhead (Cap and Allocation Method)")
    P(doc,
      f"“Corporate Overhead” means general and administrative costs of {C.OPERATOR_SHORT} "
      f"and its affiliates not directly attributable to the Network (executive, finance, legal, "
      f"human-resources, and shared back-office functions). Corporate Overhead is recognized as an "
      f"Operating Expense only (i) up to a cap of {C.PH('overhead cap, e.g., 8% of Network Operating Expenses or 5% of Gross Revenue')}, and (ii) allocated to the Network by a "
      f"documented, consistently applied method (for example, a ratio of Network direct costs to "
      f"total direct costs) disclosed in the Financial Model. Corporate Overhead above the cap, or "
      f"not supported by the disclosed allocation, is disregarded in every payment computation.")

    C.section(doc, "2.12", "Non-Tribal Customers")
    P(doc,
      f"“Non-Tribal Customers” means subscribers and account holders who are not enrolled "
      f"members of the {C.TRIBE_SHORT} and who are served over the {C.NETWORK} within or beyond "
      f"the {C.SERVICE_TERRITORY}. Revenue from Non-Tribal Customers that is derived from the "
      f"{C.TRIBAL_ASSETS} is INCLUDED in Gross Revenue on the same basis as revenue from Tribal "
      f"members and is subject to the same program-income analysis; service to Non-Tribal "
      f"Customers must remain consistent with the {C.PROGRAM_SHORT} Award’s eligible-service-"
      f"area and priority-of-service requirements.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Confirm the extent to which the Award permits service to, and revenue from, "
                "Non-Tribal Customers over grant-funded assets, and how that revenue is treated as "
                "program income.")

    C.section(doc, "2.13", "Adjusted Operating Cash Flow")
    P(doc,
      "“Adjusted Operating Cash Flow” (or “AOCF”) means, for any measurement "
      "period, Gross Revenue for that period LESS Operating Expenses for that period (as each is "
      "defined above, after application of the related-party and overhead limits), and further "
      "LESS a normalized allowance for the capital-replacement reserve funded under Section 4.7. "
      "AOCF EXCLUDES Capital Expenses, depreciation, amortization, interest, income taxes, and "
      "grant funds. AOCF is the base for Option C and the variable component of Option D and is "
      "computed line-by-line in the Financial Model.")

    C.section(doc, "2.14", "Wholesale Revenue")
    P(doc,
      "“Wholesale Revenue” means revenue from the sale of capacity, dark or lit fiber, "
      "lambda/wavelength, transport, IP transit, or other bulk services to carriers, ISPs, "
      "governments, or other resellers over the Network. Wholesale Revenue is INCLUDED in Gross "
      "Revenue; to the extent it is derived from capacity on the Tribal Assets, it is subject to "
      "the program-income analysis in Article 4.")

    C.section(doc, "2.15", "Enterprise Revenue")
    P(doc,
      "“Enterprise Revenue” means revenue from dedicated business, institutional, "
      "anchor-tenant, and government services (including dedicated Internet access, managed "
      "services, and private connectivity) sold over the Network. Enterprise Revenue is INCLUDED "
      "in Gross Revenue.")

    # ============ ARTICLE 3 ============
    C.article(doc, 3, "The Five Alternative Payment Structures")

    C.section(doc, "3.1", "Overview and Comparison")
    P(doc,
      f"The {C.PARTIES_COLLECTIVE} are evaluating the five alternative structures below for the "
      f"consideration payable in respect of the {C.IRU_TERM_DEFINED} and the operation of the "
      f"{C.TRIBAL_ASSETS}. Each structure uses the SAME defined terms from Article 2; they differ "
      f"only in how the payment to the {C.TRIBE_SHORT} is computed. Each is illustrated with "
      f"placeholder figures that tie to the Financial Model. The {C.OPERATOR_SHORT} recommendation "
      f"is Option D (Section 3.7).")

    comp_headers = ["Option", "Mechanism", f"{C.TRIBE_SHORT} upside",
                    f"{C.TRIBE_SHORT} risk", f"{C.OPERATOR_SHORT} cash-flow impact", "Best when"]
    comp_rows = [
        ["A — Fixed Annual Payment",
         "Flat annual IRU / operating payment, fixed (with optional escalator).",
         "Predictable, certain; no exposure to operating results.",
         "No participation in upside if take rates or ARPU exceed plan; fixed amount can lag inflation.",
         "Highest early fixed obligation; simplest to model and finance.",
         "The Lumbee Tribe values certainty and simplicity over upside."],
        ["B — % of Gross Revenue",
         f"{C.DEAL['rev_share_pct_placeholder']} (placeholder) of Gross Revenue, top-line, no expense deduction.",
         "Direct participation in top-line growth; hard to manipulate; simple to audit.",
         "Paid even in loss years; indifferent to Operator cost discipline; can strain early cash flow.",
         "Scales with revenue regardless of margin; pressures thin early-year margins.",
         "The Lumbee Tribe wants growth participation and a simple, tamper-resistant base."],
        ["C — % of Adjusted Operating Cash Flow",
         f"{C.DEAL['cashflow_share_pct_placeholder']} (placeholder) of AOCF (Gross Revenue less OpEx and reserve).",
         "Aligns with true profitability; shares in margin improvement.",
         "Exposed to expense inflation and allocation/overhead judgment; can be zero in early years.",
         "Self-adjusting to affordability; lowest strain when margins are thin.",
         "The Lumbee Tribe accepts expense-side complexity in exchange for margin alignment."],
        ["D — Hybrid (Fixed Base + Revenue Share)",
         f"Fixed base {C.PH('base amount')} PLUS {C.DEAL['rev_share_pct_placeholder']} (placeholder) of "
         f"Gross Revenue above a {C.PH('threshold')}.",
         "Floor of certainty AND a share of upside; balances both objectives.",
         "More moving parts; base still owed in weak years, though set conservatively.",
         "Manageable fixed floor plus a variable layer that grows with success.",
         "The Lumbee Tribe wants a guaranteed minimum and meaningful upside — the recommended balance."],
        ["E — Payment Holiday then Stepped Payments",
         f"No / nominal payment for an initial {C.PH('holiday period, e.g., 24–36 months')}, then "
         f"payments that step up on a fixed schedule.",
         "Matches payments to the network’s revenue ramp; larger later payments possible.",
         "Little or no early cash; back-loaded; depends on the ramp materializing.",
         "Protects fragile construction- and ramp-phase cash flow; back-loads the obligation.",
         "The build has a long ramp and early-year cash must be preserved."],
    ]
    C.add_table(doc, comp_headers, comp_rows,
                widths=[1.05, 1.55, 1.1, 1.15, 1.1, 1.2], font_size=8)
    C.flag_para(doc, C.FLAG_BUSINESS,
                "The percentages, base, threshold, escalators, and holiday period shown are "
                "placeholders. Selection among A–E and calibration of each figure are business "
                "decisions to be finalized with the Financial Model.")

    # Shared assumptions used by every worked example
    C.section(doc, "3.2", "Shared Illustrative Assumptions")
    P(doc, "The worked examples in Sections 3.3–3.6 use the following placeholder inputs, all of "
           "which are carried in, and must reconcile to, the Financial Model:")
    assum_rows = [
        ["Grant award (capital source — NOT revenue)", C.DEAL["ph_grant_amount"] + "  " + C.PH("placeholder")],
        ["Homes / passings", C.DEAL["ph_homes_passed"] + "  " + C.PH("placeholder")],
        ["Terminal take rate", C.DEAL["ph_base_take_rate"] + "  " + C.PH("placeholder")],
        ["Residential ARPU (monthly)", C.DEAL["ph_res_arpu"] + "  " + C.PH("placeholder")],
        ["Business ARPU (monthly)", C.DEAL["ph_bus_arpu"] + "  " + C.PH("placeholder")],
        ["Stabilized-year Gross Revenue (derived)", C.PH("stabilized-year Gross Revenue — from 04_Financial_Model")],
        ["Stabilized-year Operating Expenses (derived)", C.PH("stabilized-year OpEx — from 04_Financial_Model")],
        ["Stabilized-year AOCF (derived)", C.PH("stabilized-year AOCF — from 04_Financial_Model")],
    ]
    C.add_table(doc, ["Assumption", "Illustrative value"], assum_rows,
                widths=[3.4, 3.1], font_size=9)
    C.flag_para(doc, C.FLAG_TECH,
                "Confirm homes passed, take-rate ramp, and residential/business mix against the "
                "engineering design and market study before the Financial Model is finalized.")

    # ---- Option A
    C.section(doc, "3.3", C.DEAL["rev_options"]["A"])
    P(doc,
      f"Mechanism. {C.OPERATOR_SHORT} pays the {C.TRIBE_SHORT} a fixed annual amount of "
      f"{C.PH('fixed annual payment, e.g., $150,000–$400,000/yr')} in respect of the "
      f"{C.IRU_TERM_DEFINED} and the operation of the {C.TRIBAL_ASSETS}, payable in equal "
      f"{C.PH('monthly or quarterly')} installments, with an annual escalator of "
      f"{C.PH('escalator, e.g., CPI or fixed 2–3%')}. Gross Revenue, expenses, and AOCF do "
      f"not affect the amount; the defined terms in Article 2 nonetheless govern the audit, "
      f"records, and program-income analysis.")
    C.add_table(doc,
                ["Year", "Fixed annual payment", "Escalator applied", "Payment to Lumbee Tribe"],
                [["1", C.PH("base amount"), "—", C.PH("base amount")],
                 ["2", C.PH("base amount"), C.PH("escalator %"), C.PH("year-2 amount")],
                 ["3", C.PH("base amount"), C.PH("escalator %"), C.PH("year-3 amount")],
                 ["…", "…", "…", "…"],
                 [f"{C.IRU_TERM_RECOMMENDED}", C.PH("base amount"), C.PH("escalator %"), C.PH("final-year amount")]],
                widths=[0.9, 1.9, 1.7, 2.0], font_size=9)

    # ---- Option B
    C.section(doc, "3.4", C.DEAL["rev_options"]["B"])
    P(doc,
      f"Mechanism. {C.OPERATOR_SHORT} pays the {C.TRIBE_SHORT} "
      f"{C.DEAL['rev_share_pct_placeholder']} (placeholder) of Gross Revenue (Section 2.1), with "
      f"no deduction for Operating Expenses. Excluded Revenue (Section 2.6), including grant "
      f"funds, remitted taxes, refunds, and capped bad debt, is not in the base. Installation, "
      f"Voice, Equipment, Late Fees, Wholesale, and Enterprise revenue ARE in the base; revenue "
      f"from Non-Tribal Customers derived from the Tribal Assets is included and subject to "
      f"program-income treatment.")
    C.add_table(doc,
                ["Line", "Illustrative amount"],
                [["Gross Revenue (stabilized year)", C.PH("Gross Revenue — 04_Financial_Model")],
                 ["Less: Excluded Revenue (grant/taxes/refunds/bad debt)", C.PH("excluded amount")],
                 ["Revenue-share base", C.PH("share base")],
                 [f"× Revenue-share rate ({C.DEAL['rev_share_pct_placeholder']})",
                  C.DEAL["rev_share_pct_placeholder"]],
                 ["= Payment to Lumbee Tribe (stabilized year)", C.PH("Option B payment")]],
                widths=[3.6, 2.9], font_size=9)

    # ---- Option C
    C.section(doc, "3.5", C.DEAL["rev_options"]["C"])
    P(doc,
      f"Mechanism. {C.OPERATOR_SHORT} pays the {C.TRIBE_SHORT} "
      f"{C.DEAL['cashflow_share_pct_placeholder']} (placeholder) of Adjusted Operating Cash Flow "
      f"(Section 2.13). Because AOCF nets Operating Expenses (after the related-party and "
      f"overhead limits) and the reserve allowance against Gross Revenue, the arm’s-length "
      f"standard (Section 2.10), the overhead cap (Section 2.11), and the Shared-Expense "
      f"allocation (Section 2.9) directly protect the {C.TRIBE_SHORT}’s payment.")
    C.add_table(doc,
                ["Line", "Illustrative amount"],
                [["Gross Revenue (stabilized year)", C.PH("Gross Revenue")],
                 ["Less: Operating Expenses (arm’s-length; overhead-capped)", C.PH("OpEx")],
                 ["Less: capital-replacement reserve allowance", C.PH("reserve allowance")],
                 ["= Adjusted Operating Cash Flow (AOCF)", C.PH("AOCF")],
                 [f"× Cash-flow-share rate ({C.DEAL['cashflow_share_pct_placeholder']})",
                  C.DEAL["cashflow_share_pct_placeholder"]],
                 ["= Payment to Lumbee Tribe (stabilized year)", C.PH("Option C payment")]],
                widths=[3.6, 2.9], font_size=9)

    # ---- Option D (recommended)
    C.section(doc, "3.6", C.DEAL["rev_options"]["D"])
    P(doc,
      f"Mechanism. {C.OPERATOR_SHORT} pays the {C.TRIBE_SHORT} (i) a fixed base payment of "
      f"{C.PH('fixed base, e.g., $100,000–$250,000/yr')} PLUS (ii) a revenue share of "
      f"{C.DEAL['rev_share_pct_placeholder']} (placeholder) of Gross Revenue above an annual "
      f"threshold of {C.PH('threshold, e.g., $2,000,000')}. The fixed base provides a certain "
      f"floor (as in Option A); the revenue-share layer provides upside participation (as in "
      f"Option B) once the network reaches scale. A cap or collar on the variable layer may be "
      f"added at {C.PH('optional cap/collar terms')}.")
    C.add_table(doc,
                ["Line", "Illustrative amount"],
                [["Fixed base payment (floor)", C.PH("fixed base")],
                 ["Gross Revenue (stabilized year)", C.PH("Gross Revenue")],
                 ["Less: revenue-share threshold", C.PH("threshold")],
                 ["Gross Revenue above threshold", C.PH("excess over threshold")],
                 [f"× Revenue-share rate ({C.DEAL['rev_share_pct_placeholder']})",
                  C.DEAL["rev_share_pct_placeholder"]],
                 ["= Variable layer", C.PH("variable layer")],
                 ["= Total payment to Lumbee Tribe (base + variable)", C.PH("Option D payment")]],
                widths=[3.6, 2.9], font_size=9)

    # ---- Option E
    C.section(doc, "3.7", C.DEAL["rev_options"]["E"])
    P(doc,
      f"Mechanism. No payment (or a nominal {C.PH('nominal amount, e.g., $1/yr')}) accrues "
      f"during an initial payment holiday of {C.PH('holiday, e.g., 24–36 months')} to "
      f"preserve construction- and ramp-phase cash flow, after which payments step up on a fixed "
      f"schedule keyed to the Financial Model’s revenue ramp. The stepped amounts may be "
      f"expressed as fixed dollars (Option A style) or as a revenue share (Option B style) once "
      f"the holiday ends.")
    C.add_table(doc,
                ["Period", "Payment basis", "Payment to Lumbee Tribe"],
                [[C.PH("holiday years"), "Payment holiday (nominal)", C.PH("$1 / nominal")],
                 [C.PH("step-1 years"), "First step", C.PH("step-1 amount")],
                 [C.PH("step-2 years"), "Second step", C.PH("step-2 amount")],
                 [C.PH("step-3 years"), "Stabilized step", C.PH("stabilized amount")]],
                widths=[1.9, 2.3, 2.3], font_size=9)

    # ---- Recommendation
    C.section(doc, "3.8", "Recommendation — Option D (Hybrid)")
    P(doc,
      f"{C.OPERATOR_SHORT} recommends Option D — Hybrid (Fixed Base plus Revenue Share). "
      f"Option D is recommended because it:")
    C.numbered(doc, f"gives the {C.TRIBE_SHORT} a certain, budgetable floor (the fixed base) that is "
                    f"owed regardless of operating results, addressing the {C.TRIBE_SHORT}’s need "
                    f"for reliable cash — the strength of Option A;")
    C.numbered(doc, f"preserves genuine upside for the {C.TRIBE_SHORT} through the revenue-share layer, "
                    f"so that if take rates or ARPU exceed plan the {C.TRIBE_SHORT} participates — "
                    f"the strength of Option B;")
    C.numbered(doc, "uses Gross Revenue (not AOCF) for the variable layer, so the variable payment is "
                    "tamper-resistant and simple to audit, avoiding the expense-allocation and overhead "
                    "disputes that make Option C harder to administer;")
    C.numbered(doc, f"sets the fixed base conservatively and places the revenue share above a threshold, "
                    f"which protects {C.OPERATOR_SHORT}’s fragile early-year cash flow better than a "
                    f"pure top-line share (Option B) while still delivering more early certainty to the "
                    f"{C.TRIBE_SHORT} than Option E’s back-loaded holiday; and")
    C.numbered(doc, "maps cleanly to program-income tracking, because both the fixed base and the "
                    "revenue-share layer are computed from clearly defined, auditable revenue rather than "
                    "from a negotiated net-cash-flow figure.")
    P(doc,
      f"Option D should be selected only after the fixed base, revenue-share percentage, and "
      f"threshold are calibrated in the Financial Model so that the blended payment is affordable "
      f"across the ramp yet delivers a fair return to the {C.TRIBE_SHORT} over the "
      f"{C.IRU_TERM_RECOMMENDED}-year {C.IRU_TERM_DEFINED} term.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                "Final selection among Options A–E, and calibration of Option D’s base, "
                "percentage, and threshold, are business decisions for the Lumbee Tribe and RIVR Tech, to "
                "be confirmed against the Financial Model and grant counsel’s program-income "
                "guidance.")

    # ============ ARTICLE 4 ============
    C.article(doc, 4, "Financial Administration, Controls, and Program Income")
    P(doc, "The following provisions apply to whichever payment structure the "
           f"{C.PARTIES_COLLECTIVE} select under Article 3.")

    C.section(doc, "4.1", "Payment Timing")
    P(doc,
      f"Payments accrue on a {C.PH('monthly / quarterly')} basis and are due within "
      f"{C.PH('e.g., thirty (30)')} days after the end of each period, accompanied by a "
      f"statement showing the computation (Gross Revenue, Excluded Revenue, any expense and "
      f"reserve deductions applicable to the selected structure, and the resulting payment). "
      f"An annual true-up payment or credit is made following the reconciliation under "
      f"Section 4.2. Late payments accrue interest at {C.PH('interest rate, e.g., the lesser of 1.5%/month or the maximum lawful rate')}.")

    C.section(doc, "4.2", "Reconciliation")
    P(doc,
      "Within ninety (90) days after the end of each contract year, RIVR Tech shall deliver an "
      "annual reconciliation statement that recomputes Gross Revenue, Excluded Revenue, "
      "Operating Expenses, AOCF (if applicable), the reserve, and the payment for the year, and "
      "reconciles them to the audited or reviewed financial statements and to the Financial "
      "Model. Any underpayment is paid, and any overpayment is credited, within thirty (30) days "
      "of the reconciliation, subject to the underpayment remedies in Section 4.6.")

    C.section(doc, "4.3", "Financial Statements")
    P(doc,
      f"RIVR Tech shall provide the {C.TRIBE_SHORT}: (a) unaudited quarterly financial statements "
      f"and a Network operating report within {C.PH('e.g., forty-five (45)')} days after each "
      f"quarter; and (b) annual financial statements, {C.PH('audited or reviewed')} by an "
      f"independent CPA, within {C.PH('e.g., one hundred twenty (120)')} days after each fiscal "
      f"year, in each case segmenting Network revenue and expenses sufficiently to verify the "
      f"payment computation.")

    C.section(doc, "4.4", "Books and Records")
    P(doc,
      f"RIVR Tech shall keep complete and accurate books and records of all Gross Revenue, "
      f"Excluded Revenue, Operating Expenses, Capital Expenses, Shared-Expense allocations, "
      f"Related-Party Charges, Corporate Overhead allocations, reserves, and payments, in "
      f"accordance with GAAP, consistently applied, and shall retain them for not less than "
      f"{C.DEAL['records_retention_years']} years (or longer if required by the Award or applicable "
      f"law — see the Grant Compliance Addendum). Records must be sufficient to permit the "
      f"{C.TRIBE_SHORT}, its auditors, and federal awarding-agency and oversight officials to "
      f"verify every figure in a payment computation.")

    C.section(doc, "4.5", "Audit Rights")
    P(doc,
      f"The {C.TRIBE_SHORT} (and its designated independent auditor) may, on not less than "
      f"{C.DEAL['audit_notice_business_days']} business days’ written notice and not more than "
      f"{C.PH('e.g., once')} per contract year (and more often on reasonable suspicion of "
      f"underpayment or upon a federal audit finding), examine and copy RIVR Tech’s books and "
      f"records relating to the payment computation, during normal business hours. This audit "
      f"right is in addition to, and does not limit, the federal audit-access rights described in "
      f"the Grant Compliance Addendum.")

    C.section(doc, "4.6", "Underpayment Remedies")
    P(doc,
      f"If an audit or reconciliation determines that RIVR Tech underpaid, RIVR Tech shall pay the "
      f"shortfall plus interest at {C.PH('interest rate, e.g., 1.5% per month')} from the date each "
      f"underpaid amount was due. If the underpayment for the audited period exceeds "
      f"{C.PH('audit-cost-shift threshold, e.g., the greater of 5% of amounts due or $25,000')}, "
      f"RIVR Tech shall also reimburse the {C.TRIBE_SHORT}’s reasonable audit costs. Repeated "
      f"or willful underpayment is an event of default under the Agreement.")

    C.section(doc, "4.7", "Capital Replacement Reserve")
    P(doc,
      f"RIVR Tech shall fund and maintain a capital-replacement reserve for the {C.TRIBAL_ASSETS} "
      f"by depositing {C.PH('reserve funding %, e.g., 2–4% of Network Gross Revenue')} of "
      f"Network Gross Revenue each period into a segregated, {C.TRIBE_SHORT}-visible reserve "
      f"account, to fund lifecycle replacement of electronics, fiber, and equipment so that the "
      f"{C.TRIBAL_ASSETS} are returned to the {C.TRIBE_SHORT} at the end of the "
      f"{C.IRU_TERM_DEFINED} term in good operating condition. The reserve is a Network cost for "
      f"AOCF purposes (Section 2.13) but is not otherwise deducted from Gross Revenue in Options B "
      f"or D. Reserve funding, use, and reporting shall be documented in the Financial Model.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                "Set the reserve funding rate and the conditions for drawing on the reserve; "
                "coordinate with the O&M Agreement and end-of-term hand-back condition standard.")

    C.section(doc, "4.8", "Treatment of Future Grants")
    P(doc,
      f"Any future grant, subsidy, or contribution-in-aid-of-construction obtained for the "
      f"{C.NETWORK} (whether by the {C.TRIBE_SHORT} or, with the {C.TRIBE_SHORT}’s consent, by "
      f"RIVR Tech) is a capital source and Excluded Revenue under Section 2.6(a); it is never Gross "
      f"Revenue and never enters any payment base. Future grants may, however, generate program "
      f"income and may carry their own federal or state conditions, which control over this "
      f"Schedule to the extent of any conflict. Neither Party may pursue a future grant for the "
      f"Network in a manner that would duplicate funding, jeopardize the {C.PROGRAM_SHORT} Award, "
      f"or impair the {C.TRIBE_SHORT}’s title to or {C.FEDERAL_INTEREST} in the "
      f"{C.TRIBAL_ASSETS}.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Any additional federal award over the same assets requires a duplication-of-"
                "funding review and may change program-income and disposition treatment.")

    C.section(doc, "4.9", "Program Income — Application to Payments")
    P(doc,
      f"To the extent revenue generated by the {C.TRIBAL_ASSETS} constitutes {C.PROGRAM_INCOME} "
      f"under {C.CITES['prog_income']}, the {C.TRIBE_SHORT}’s share of that revenue (however "
      f"computed under the selected structure) must be identified, accounted for, and applied in "
      f"accordance with the method specified or approved by {C.AGENCY_SHORT} in the Award. The "
      f"payment mechanics in this Schedule are structured so that the {C.TRIBE_SHORT} can trace "
      f"and report program income; they do not, and cannot, override the Award’s program-"
      f"income requirements, which control. See Article 5 of the Grant Compliance Addendum.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Grant counsel must confirm the program-income method and the treatment of the "
                "Lumbee Tribe’s revenue share before any payment structure is executed.")

    # ============ ARTICLE 5 ============
    C.article(doc, 5, "Interpretation and Order of Precedence")
    C.section(doc, "5.1", "Conformance to the Financial Model")
    P(doc,
      "Illustrative figures in this Schedule are for explanation only. The controlling figures "
      "are those in the Financial Model as populated with final, negotiated inputs. The "
      f"{C.PARTIES_COLLECTIVE} shall update this Schedule and the Financial Model together so "
      f"that they remain consistent.")
    C.section(doc, "5.2", "Precedence")
    P(doc,
      f"In the event of a conflict between this Schedule and (a) the {C.PROGRAM_SHORT} Award, "
      f"{C.CITES['ug_part']}, or other federal requirements, the Award and federal requirements "
      f"control; and (b) the body of the Agreement, the Agreement controls except as to the "
      f"financial mechanics expressly addressed here. The Grant Compliance and Federal Interest "
      f"Addendum (Deliverable 6) governs all grant-compliance questions arising under this "
      f"Schedule.")

    C.signature_block(
        doc,
        extra_note="Confirm signatory authority for financial commitments and whether the Tribal "
                   "party is the Lumbee Tribe directly or a designated Tribal entity/instrumentality.")

    path = C.save(doc, "02_Core_Agreements", "04_Financial_and_Revenue_Sharing_Schedule.docx")
    return path


# ===========================================================================
#  DELIVERABLE 6 — TBCP GRANT COMPLIANCE & FEDERAL INTEREST ADDENDUM
# ===========================================================================
def build_grant_addendum():
    doc = C.new_doc()

    C.add_cover(
        doc,
        "DELIVERABLE 6 · ADDENDUM 05 TO THE CORE AGREEMENTS",
        "TBCP Grant Compliance and Federal Interest Addendum",
        "Federal Award Requirements, Federal Interest, Property, Procurement, "
        "Program Income, Audit, and Disposition Controls Governing the IRU",
    )
    C.setup_header_footer(doc, "TBCP Grant Compliance & Federal Interest Addendum")
    C.add_toc(doc)

    C.status_banner(doc)
    C.spacer(doc, 1)
    P(doc,
      f"This TBCP Grant Compliance and Federal Interest Addendum (this “Addendum”) is "
      f"Addendum 05 to, and is incorporated by reference into, the Core Agreements (the "
      f"“Agreement”) between {C.TRIBE_FULL} (the “{C.TRIBE_SHORT}”), or "
      f"{C.TRIBE_ENTITY_ALT}, and {C.OPERATOR_FULL} (“{C.OPERATOR_SHORT}”). This Addendum "
      f"is the compliance backbone of the transaction. Its purpose is to ensure that the "
      f"{C.IRU_TERM_DEFINED}, the operation of the {C.TRIBAL_ASSETS}, and every payment and "
      f"activity under the Agreement remain consistent with the {C.PROGRAM_FULL} ({C.PROGRAM_SHORT}) "
      f"Award and all applicable federal requirements. Every major provision cites the controlling "
      f"authority.")
    C.spacer(doc, 1)

    # ============ ARTICLE 1 ============
    C.article(doc, 1, "Purpose, Award Identification, and Order of Precedence")

    C.section(doc, "1.1", "Purpose and Incorporation")
    P(doc,
      f"This Addendum supplements the Agreement with the federal terms and conditions applicable "
      f"to the {C.TRIBAL_ASSETS} as {C.PROGRAM_SHORT}-funded infrastructure. It applies to both "
      f"{C.PARTIES_COLLECTIVE} and, through the flow-down provisions of Article 11, to "
      f"subcontractors and lower-tier providers.")

    C.section(doc, "1.2", "Federal Award Identification")
    P(doc,
      f"The {C.TRIBAL_ASSETS} are funded, in whole or in part, under the {C.PROGRAM_SHORT} "
      f"administered by the {C.AGENCY_FULL} ({C.AGENCY_SHORT}), pursuant to the "
      f"{C.CITES['nofo']}, the {C.CITES['id_guidance']}, and the executed award, including the "
      f"{C.CITES['sac']} (collectively, the “Award”). The program is authorized by the "
      f"{C.CITES['iija']}. The {C.TRIBE_SHORT} is the {C.PROGRAM_SHORT} grant RECIPIENT and the "
      f"owner of the grant-funded infrastructure, and retains title thereto.")

    C.section(doc, "1.3", "Lumbee Federal-Recognition Status — Eligibility Predicate")
    P(doc,
      f"The {C.TRIBE_SHORT}’s eligibility for the {C.PROGRAM_SHORT} depends on its status "
      f"under federal law. The {C.CITES['lumbee_act']} recognized the Lumbee people but has "
      f"historically been construed to withhold the full federal-Indian benefits and services "
      f"relationship, which bears directly on {C.PROGRAM_SHORT} eligibility, the nature of any "
      f"trust or {C.FEDERAL_INTEREST}, and the applicability of certain federal-Indian program "
      f"authorities. Nothing in the Agreement or this Addendum determines that status; the "
      f"{C.PARTIES_COLLECTIVE} rely on the eligibility basis stated in the Award.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Confirm with NTIA and grant counsel the exact eligibility basis on which the "
                "Award was made, given the Lumbee Act of 1956, and whether any condition, "
                "limitation, or alternative eligibility pathway applies to this Award.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Federal-recognition status affects trust relationship, jurisdiction, sovereign "
                "immunity, and the enforceability of federal-Indian program terms. Tribal and "
                "federal-Indian-law counsel must review before execution.")

    C.section(doc, "1.4", "Order of Precedence — Award and 2 CFR 200 Control")
    P(doc,
      f"If any provision of the Agreement, this Addendum, or any commercial term conflicts with "
      f"the Award, {C.CITES['ug_part']}, or any other applicable federal requirement, the Award "
      f"and the federal requirement CONTROL, and the conflicting commercial provision is "
      f"superseded to the extent of the conflict. No commercial arrangement between the "
      f"{C.PARTIES_COLLECTIVE} may waive, diminish, or defeat a federal requirement or the "
      f"{C.FEDERAL_INTEREST}.")

    # ============ ARTICLE 2 ============
    C.article(doc, 2, "Grant-Funded Property and the Federal Interest")

    C.section(doc, "2.1", "Grant-Funded Property")
    P(doc,
      f"The {C.TRIBAL_ASSETS} are property acquired or improved with federal funds and are "
      f"subject to the property-management standards of {C.CITES['equipment']} (equipment) and "
      f"{C.CITES['real_property']} (real property), as applicable to each asset class, together "
      f"with {C.CITES['intangible']} for intangible property such as software and IRUs held by "
      f"the {C.TRIBE_SHORT}. The {C.TRIBE_SHORT} shall use the {C.TRIBAL_ASSETS} for the "
      f"authorized {C.PROGRAM_SHORT} purpose for the duration of the {C.FEDERAL_INTEREST}.")

    C.section(doc, "2.2", "Federal Interest and Property Trust Relationship")
    P(doc,
      f"A {C.FEDERAL_INTEREST} exists in the {C.TRIBAL_ASSETS} for so long as required by the "
      f"Award. Under {C.CITES['trust']}, real property, equipment, and (as applicable) intangible "
      f"property acquired or improved with federal funds are held in trust by the recipient as "
      f"trustee for the beneficiaries of the program; the property must be used for the authorized "
      f"purpose and may not be encumbered or disposed of except as permitted by the awarding "
      f"agency. The {C.FEDERAL_INTEREST} runs with the {C.TRIBAL_ASSETS} regardless of the "
      f"{C.IRU_TERM_DEFINED} granted to {C.OPERATOR_SHORT}.")

    C.section(doc, "2.3", "Title Retained by the Lumbee Tribe")
    P(doc,
      f"Title to the {C.TRIBAL_ASSETS} vests in and remains with the {C.TRIBE_SHORT} at all "
      f"times. The {C.IRU_TERM_DEFINED} conveys a right to use capacity, not title; nothing in the "
      f"Agreement transfers, or may be construed to transfer, ownership of the {C.TRIBAL_ASSETS} "
      f"to {C.OPERATOR_SHORT}. The clear demarcation between the {C.TRIBAL_ASSETS} and the "
      f"{C.OPERATOR_EXISTING} is maintained in Exhibit K.")

    C.section(doc, "2.4", "Property Records and Asset Inventory")
    P(doc,
      f"The {C.TRIBE_SHORT} shall maintain property records for the {C.TRIBAL_ASSETS} meeting "
      f"{C.CITES['equipment']}(d), including a description of the property, a serial or other "
      f"identification number, the source of funding (including the {C.PROGRAM_SHORT} award "
      f"identification number), who holds title, the acquisition date and cost, the federal share "
      f"of the cost, location, use and condition, and ultimate disposition data. A physical "
      f"inventory shall be reconciled to the records at least once every two years. The asset "
      f"inventory and demarcation schedule are maintained in Exhibit K, to which this Article "
      f"cross-refers.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Confirm which Party physically maintains the inventory and who bears the every-"
                "two-year reconciliation duty; the recordkeeping obligation is the recipient "
                "Lumbee Tribe’s and may be delegated to RIVR Tech only by written flow-down.")

    C.section(doc, "2.5", "Insurance of Grant-Funded Property")
    P(doc,
      f"The {C.TRIBAL_ASSETS} shall be insured at least to the extent required by "
      f"{C.CITES['insurance']} — equivalent insurance coverage for property acquired or "
      f"improved with federal funds as is provided to other property owned by the recipient — "
      f"and to the limits set out in Exhibit I of the Agreement.")

    # ============ ARTICLE 3 ============
    C.article(doc, 3, "Contractor vs. Subrecipient Determination")

    C.section(doc, "3.1", "Framework")
    P(doc,
      f"Whether {C.OPERATOR_SHORT} is a “subrecipient” or a “contractor” "
      f"(vendor) of the {C.TRIBE_SHORT} with respect to {C.PROGRAM_SHORT} funds is governed by "
      f"{C.CITES['subrecipient']}. The determination is based on the substance of the "
      f"relationship, not its label. The characterization has significant consequences: a "
      f"subrecipient is subject to the full suite of federal award requirements and the "
      f"{C.TRIBE_SHORT} must monitor it as a pass-through entity under {C.CITES['pass_through']}; "
      f"a contractor is procured under the procurement standards (Article 4) and is generally "
      f"subject only to the contract terms and specific flow-down clauses.")

    C.section(doc, "3.2", "Five-Factor Analysis Applied to RIVR Tech")
    P(doc,
      f"The following table applies the {C.CITES['subrecipient']} characteristics to "
      f"{C.OPERATOR_SHORT}’s role under the Agreement.")
    sr_headers = ["#", "Subrecipient characteristic (200.331(a))",
                  "Contractor characteristic (200.331(b))",
                  "As applied to RIVR Tech", "Points toward"]
    sr_rows = [
        ["1",
         "Determines who is eligible to receive federal assistance.",
         "Provides goods and services within normal business operations.",
         "RIVR Tech does not determine eligibility for federal assistance; it builds, operates, "
         "and sells services over the Network in its ordinary course.",
         "Contractor"],
        ["2",
         "Has its performance measured against whether program objectives are met.",
         "Provides similar goods or services to many different purchasers.",
         "RIVR Tech’s performance is measured against SLA/O&M and commercial metrics; it "
         "offers broadband and transport to many customers, not solely this program.",
         "Contractor"],
        ["3",
         "Has responsibility for programmatic decision-making.",
         "Normally operates in a competitive environment.",
         "Programmatic decisions (service area, priorities, program-income use) rest with the "
         "Lumbee Tribe as recipient; RIVR Tech operates as a competitive commercial provider.",
         "Contractor"],
        ["4",
         "Is responsible for adherence to applicable federal program requirements.",
         "Provides goods or services that are ancillary to the operation of the federal program.",
         "The Lumbee Tribe, as recipient, is responsible for program compliance; RIVR Tech’s "
         "operating role is ancillary and is bound only through flow-down terms.",
         "Contractor"],
        ["5",
         "Uses the federal funds to carry out a program for a public purpose, not to provide "
         "goods or services for the pass-through entity’s benefit.",
         "Is not subject to the compliance requirements of the federal program as a result of "
         "the agreement (though similar requirements may apply for other reasons).",
         "The Lumbee Tribe carries out the public broadband program; RIVR Tech provides operating "
         "services under the IRU. Note the Lumbee Tribe does receive the benefit of the operating "
         "services — a factor to weigh, though not dispositive.",
         "Mixed → Contractor (weight)"],
    ]
    C.add_table(doc, sr_headers, sr_rows,
                widths=[0.3, 1.55, 1.55, 1.95, 0.85], font_size=8)

    C.section(doc, "3.3", "Recommended Characterization")
    P(doc,
      f"On balance, {C.OPERATOR_SHORT} exhibits predominantly CONTRACTOR (vendor) characteristics "
      f"under {C.CITES['subrecipient']}: it provides operating and construction services within "
      f"its normal business operations, to many purchasers, in a competitive environment, and it "
      f"does not determine assistance eligibility or hold programmatic responsibility. The "
      f"recommended characterization is therefore CONTRACTOR / vendor, procured under the "
      f"procurement standards of Article 4. This characterization must not be adopted silently or "
      f"by default.")
    C.flag_para(doc, C.FLAG_GRANT,
                "The contractor-vs-subrecipient determination must be confirmed in writing by "
                "grant counsel and, if required, NTIA. Do not proceed on the contractor "
                "characterization without that confirmation.")
    P(doc,
      f"Implications either way. If {C.OPERATOR_SHORT} is a CONTRACTOR: the {C.TRIBE_SHORT} must "
      f"have procured it consistent with {C.CITES['procurement']}, and only specific federal "
      f"clauses flow down (Article 11). If {C.OPERATOR_SHORT} is instead a SUBRECIPIENT: the "
      f"{C.TRIBE_SHORT} becomes a pass-through entity under {C.CITES['pass_through']} and must, "
      f"among other things, provide a subaward with required data elements, conduct a risk "
      f"assessment, impose subrecipient monitoring, verify audit status, and flow down the full "
      f"applicable requirements. The two paths carry materially different monitoring, audit, and "
      f"documentation burdens; the choice must be deliberate and documented.")

    # ============ ARTICLE 4 ============
    C.article(doc, 4, "Procurement Standards")
    C.section(doc, "4.1", "Applicability")
    P(doc,
      f"To the extent the {C.TRIBE_SHORT} uses {C.PROGRAM_SHORT} funds to procure property or "
      f"services (including {C.OPERATOR_SHORT}’s services, if characterized as a contractor), "
      f"the procurement must comply with {C.CITES['procurement']}.")
    C.section(doc, "4.2", "Competition and Methods")
    P(doc,
      f"Procurements must provide full and open competition consistent with "
      f"{C.CITES['competition']} and use an appropriate method of procurement under "
      f"{C.CITES['methods']}. Where a noncompetitive (sole-source) procurement is asserted — "
      f"for example, on the basis of {C.OPERATOR_SHORT}’s unique existing middle-mile assets "
      f"— the {C.TRIBE_SHORT} must document that one of the limited circumstances permitting "
      f"noncompetitive procurement is met and, where required, obtain awarding-agency approval.")
    C.flag_para(doc, C.FLAG_GRANT,
                "If RIVR Tech was selected without full and open competition, document the sole-"
                "source justification under 200.320 and confirm whether NTIA pre-approval is "
                "required. This is a common audit-finding area.")
    C.section(doc, "4.3", "Domestic Preference")
    P(doc,
      f"Procurements are subject to the domestic-preference provisions of {C.CITES['domestic']}, "
      f"in addition to the Build America, Buy America requirements addressed in Article 6.")
    C.section(doc, "4.4", "Conflict of Interest")
    P(doc,
      f"The {C.TRIBE_SHORT} shall maintain and enforce written conflict-of-interest and, if "
      f"applicable, organizational-conflict-of-interest standards consistent with "
      f"{C.CITES['conflict']}, and shall make the mandatory disclosures required by "
      f"{C.CITES['disclosures']}. Any relationship between the {C.TRIBE_SHORT}, its officials, "
      f"{C.OPERATOR_SHORT}, and the parent cooperative that could present a conflict must be "
      f"disclosed and managed.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Map any overlapping officials, ownership, or affiliations between the Lumbee Tribe, "
                "RIVR Tech, and LREMC / the parent cooperative, and confirm the COI safeguards.")
    C.section(doc, "4.5", "Debarment and Suspension")
    P(doc,
      f"Neither {C.OPERATOR_SHORT} nor any subcontractor may be debarred, suspended, or otherwise "
      f"excluded, consistent with {C.CITES['debarment']}. The {C.TRIBE_SHORT} shall verify "
      f"exclusion status (e.g., via SAM.gov) before award and flow down the requirement to lower "
      f"tiers.")

    # ============ ARTICLE 5 ============
    C.article(doc, 5, "Program Income")
    P(doc,
      f"Revenue generated by the {C.TRIBAL_ASSETS} may constitute {C.PROGRAM_INCOME} under "
      f"{C.CITES['prog_income']}. Program income must be identified, accounted for, and applied "
      f"under the method (deduction, addition, or cost sharing/matching) specified or approved by "
      f"{C.AGENCY_SHORT} in the Award, both during and (if required) after the period of "
      f"performance. The Financial and Revenue-Sharing Schedule (Deliverable 5) is structured so "
      f"the {C.TRIBE_SHORT} can trace, account for, and report program income, but the Award’s "
      f"program-income terms control over any commercial payment mechanic.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Grant counsel must fix the program-income method and its post-period-of-"
                "performance treatment; this drives how the Lumbee Tribe may use its revenue share.")

    # ============ ARTICLE 6 ============
    C.article(doc, 6, "Domestic Sourcing, BABA, and Prohibited Equipment")
    C.section(doc, "6.1", "Build America, Buy America")
    P(doc,
      f"All iron, steel, manufactured products, and construction materials incorporated into the "
      f"{C.TRIBAL_ASSETS} are subject to the Build America, Buy America (BABA) requirements of "
      f"{C.CITES['baba']}, unless a waiver (public-interest, non-availability, or unreasonable-"
      f"cost) has been issued by {C.AGENCY_SHORT}. {C.OPERATOR_SHORT} shall provide supplier "
      f"certifications and maintain documentation sufficient to demonstrate BABA compliance for "
      f"all covered items.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Confirm BABA applicability to each material class and whether any waiver has "
                "been granted; collect supplier certifications before procurement.")
    C.section(doc, "6.2", "Prohibited Telecommunications Equipment (§889)")
    P(doc,
      f"No covered telecommunications equipment or services (as defined by Section 889 of the "
      f"FY2019 NDAA) may be procured, obtained, or used in the {C.NETWORK}, consistent with "
      f"{C.CITES['telecom_ban']}. {C.OPERATOR_SHORT} shall certify that neither the "
      f"{C.TRIBAL_ASSETS} nor the interconnected {C.OPERATOR_EXISTING} used to provide the "
      f"services incorporate prohibited equipment.")

    # ============ ARTICLE 7 ============
    C.article(doc, 7, "Environmental, Historic Preservation, and Construction Restrictions")
    C.section(doc, "7.1", "NEPA")
    P(doc,
      f"Construction of the {C.TRIBAL_ASSETS} is subject to the {C.CITES['nepa']}. The "
      f"environmental review must be completed, and any required documentation approved, before "
      f"ground-disturbing or other covered activity begins.")
    C.section(doc, "7.2", "NHPA Section 106")
    P(doc,
      f"The project is subject to Section 106 of the {C.CITES['nhpa']}, including consultation "
      f"with the State Historic Preservation Officer and any Tribal Historic Preservation Officer, "
      f"and identification and treatment of historic properties, before covered construction.")
    C.section(doc, "7.3", "No Construction Before Clearance and NTIA Authorization")
    P(doc,
      f"{C.OPERATOR_SHORT} shall NOT commence construction, ground disturbance, or installation on "
      f"any segment of the {C.TRIBAL_ASSETS} until the applicable environmental (NEPA) and "
      f"historic-preservation (NHPA §106) reviews are complete for that segment AND "
      f"{C.AGENCY_SHORT} has issued written authorization to proceed. Premature construction can "
      f"render costs unallowable and jeopardize the Award.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Do not begin any covered construction before NEPA/NHPA clearance and written "
                "NTIA notice-to-proceed for the relevant segment; track authorizations by segment.")

    # ============ ARTICLE 8 ============
    C.article(doc, 8, "Service, Affordability, and Duplication of Funding")
    C.section(doc, "8.1", "Service and Affordability Commitments")
    P(doc,
      f"The {C.NETWORK} shall deliver service meeting or exceeding the {C.PROGRAM_SHORT} "
      f"performance floor of {C.SPEED_FLOOR} to served locations, and shall offer a low-cost "
      f"service option to eligible subscribers, in each case as required by the {C.CITES['nofo']} "
      f"and the {C.CITES['sac']}. Affordability, non-discrimination, and any priority-of-service "
      f"commitments in the Award flow through to {C.OPERATOR_SHORT}’s operation of the "
      f"Network.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                "Confirm the exact low-cost plan price point and eligibility criteria required by "
                "the Award and reflect them in the retail pricing schedule.")
    C.section(doc, "8.2", "Duplication of Funding")
    P(doc,
      f"No cost of the {C.TRIBAL_ASSETS} may be paid by, and no portion of the {C.PROGRAM_SHORT} "
      f"service area may overlap with, another federal award or an enforceable federal or state "
      f"funding commitment, except as expressly permitted by the Award. The "
      f"{C.PARTIES_COLLECTIVE} shall avoid any duplication of funding and shall promptly disclose "
      f"any potential overlap to {C.AGENCY_SHORT}.")

    # ============ ARTICLE 9 ============
    C.article(doc, 9, "Audit, Records, Reporting, and Allowable Costs")
    C.section(doc, "9.1", "Audit Access and Single Audit")
    P(doc,
      f"The {C.TRIBE_SHORT}, {C.OPERATOR_SHORT}, and their subcontractors shall provide the "
      f"awarding agency, the Inspector General, the Comptroller General, and their authorized "
      f"representatives access to records and the right to audit under {C.CITES['records']}, "
      f"including the access provisions equivalent to 2 CFR 200.337. A non-federal entity that "
      f"expends {C.PH('$1,000,000')} or more in federal awards in its fiscal year is subject to "
      f"the single-audit requirements of {C.CITES['single_audit']}.")
    C.section(doc, "9.2", "Record Retention")
    P(doc,
      f"Financial and programmatic records, supporting documents, and all records pertinent to "
      f"the Award shall be retained for {C.DEAL['records_retention_years']} years from the date "
      f"of submission of the final expenditure report, consistent with {C.CITES['records']}, and "
      f"longer if litigation, claim, or audit is started before the period expires.")
    C.section(doc, "9.3", "Reporting")
    P(doc,
      f"The {C.TRIBE_SHORT} (with {C.OPERATOR_SHORT}’s cooperation and data) shall submit the "
      f"reports required by the Award, including semi-annual financial and technical/performance "
      f"progress reports and an annual performance report, and any additional reporting specified "
      f"in the {C.CITES['sac']}. {C.OPERATOR_SHORT} shall provide complete and accurate data on "
      f"the schedule needed for the {C.TRIBE_SHORT} to meet each federal deadline.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Confirm the exact reporting cadence, forms, and system (e.g., NTIA reporting "
                "portal) in the Award; the semi-annual/annual cadence stated here is the program "
                "default and must be verified.")
    C.section(doc, "9.4", "Allowable Costs and Cost Allocation")
    P(doc,
      f"All costs charged to or supported by the Award must be allowable, allocable, and "
      f"reasonable under the cost principles of {C.CITES['allowable']}. Shared and indirect costs "
      f"must be allocated by a documented, consistently applied method, and no cost may be charged "
      f"to more than one award or cost objective. This federal standard operates alongside, and is "
      f"not satisfied merely by, the arm’s-length and overhead-cap provisions of the Financial "
      f"and Revenue-Sharing Schedule.")
    C.section(doc, "9.5", "Government Access Rights")
    P(doc,
      f"The federal government and the {C.TRIBE_SHORT} retain the right to enter, inspect, and "
      f"observe the {C.TRIBAL_ASSETS} and related records to verify compliance, on reasonable "
      f"notice, throughout the {C.FEDERAL_INTEREST} period.")

    # ============ ARTICLE 10 ============
    C.article(doc, 10, "Asset Disposition and Transfer Restrictions")
    C.section(doc, "10.1", "Disposition Procedures")
    P(doc,
      f"Disposition of the {C.TRIBAL_ASSETS} is governed by {C.CITES['real_property']} and "
      f"{C.CITES['equipment']}. When equipment with a current per-unit fair market value "
      f"exceeding {C.PH('$10,000')} is no longer needed for the program, and for any disposition "
      f"of real property, the recipient must follow the disposition procedures and obtain awarding-"
      f"agency (NTIA) instructions, which may require sale with a federal-share refund, transfer, "
      f"or retention with compensation to the federal government.")
    C.section(doc, "10.2", "Sale, Lease, Assignment, and Encumbrance Restrictions")
    P(doc,
      f"The {C.TRIBAL_ASSETS} may NOT be sold, leased, assigned, transferred, mortgaged, pledged, "
      f"encumbered, or otherwise disposed of, in whole or in part, without the prior written "
      f"approval of {C.AGENCY_SHORT} where such approval is required by {C.CITES['real_property']}, "
      f"{C.CITES['equipment']}, or {C.CITES['trust']}. The {C.IRU_TERM_DEFINED} granted to "
      f"{C.OPERATOR_SHORT}, and any collateral assignment, step-in, or lender security related to "
      f"it, must be structured so that it does NOT constitute an impermissible sale, lease, "
      f"encumbrance, or disposition of the {C.FEDERAL_INTEREST} in the {C.TRIBAL_ASSETS}.")
    C.flag_para(doc, C.FLAG_GRANT,
                "The IRU, any lender collateral package, and any step-in rights must be reviewed "
                "against the disposition/encumbrance rules; obtain NTIA prior approval where "
                "required before granting the IRU or any security interest over grant-funded "
                "assets.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Structure the IRU so a long-term exclusive right of use is not recharacterized as "
                "a disposition or encumbrance of the federally funded assets; coordinate with "
                "any financing.")

    # ============ ARTICLE 11 ============
    C.article(doc, 11, "Remedies, Flow-Down, and Precedence")
    C.section(doc, "11.1", "Remedies for Noncompliance")
    P(doc,
      f"Noncompliance with the Award or federal requirements may result in the remedies available "
      f"under {C.CITES['remedies']}, including temporarily withholding payments, disallowing "
      f"costs, suspending or terminating the award, and other legal remedies. {C.OPERATOR_SHORT} "
      f"shall indemnify and cooperate with the {C.TRIBE_SHORT} to cure any noncompliance "
      f"attributable to {C.OPERATOR_SHORT}, and a disallowance or clawback caused by "
      f"{C.OPERATOR_SHORT}’s act or omission is allocable to {C.OPERATOR_SHORT}.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Reconcile the allocation of federal disallowance/clawback risk with the "
                "indemnity, limitation-of-liability, and insurance provisions of the Agreement.")
    C.section(doc, "11.2", "Flow-Down Requirements")
    P(doc,
      f"{C.OPERATOR_SHORT} shall include, in every subcontract and lower-tier agreement relating "
      f"to the {C.TRIBAL_ASSETS}, the federal terms required by the Award and {C.CITES['ug_part']} "
      f"— including property management, BABA and §889 prohibitions, domestic preference, "
      f"debarment/suspension, conflict-of-interest, record retention and audit access, "
      f"environmental and historic-preservation, and remedies provisions — and shall bind its "
      f"subcontractors to them so the {C.TRIBE_SHORT}’s and the federal government’s "
      f"rights are preserved down the chain.")
    C.section(doc, "11.3", "Order of Precedence (Restated)")
    P(doc,
      f"For the avoidance of doubt: if a commercial provision of the Agreement, any Schedule, or "
      f"any Exhibit conflicts with the Award or {C.CITES['ug_part']} or other federal requirement, "
      f"the Award and federal requirement CONTROL. This Addendum is to be read to give maximum "
      f"effect to the federal requirements and the {C.FEDERAL_INTEREST}.")

    # ============ ARTICLE 12 ============
    C.article(doc, 12, "Compliance Responsibility Matrix")
    P(doc,
      "The following matrix summarizes the principal compliance requirements, their controlling "
      "citations, the responsible Party, and cross-references. It is a summary aid; the operative "
      "obligations are those in the Articles above and in the Award.")
    rm_headers = ["Requirement", "Citation", "Responsible Party", "Cross-ref"]
    rm_rows = [
        ["Title / property trust relationship & federal interest", C.CITES["trust"],
         f"{C.TRIBE_SHORT} (recipient)", "Art. 2; Ex. K"],
        ["Property records & biennial inventory", C.CITES["equipment"] + "(d)",
         f"{C.TRIBE_SHORT}; {C.OPERATOR_SHORT} (data)", "§2.4; Ex. K"],
        ["Real-property use / encumbrance / disposition", C.CITES["real_property"],
         f"{C.TRIBE_SHORT} + {C.AGENCY_SHORT} approval", "Art. 10"],
        ["Insurance of grant-funded property", C.CITES["insurance"],
         f"{C.OPERATOR_SHORT} / {C.TRIBE_SHORT}", "§2.5; Ex. I"],
        ["Contractor vs. subrecipient determination", C.CITES["subrecipient"],
         f"{C.TRIBE_SHORT} + grant counsel", "Art. 3"],
        ["Pass-through monitoring (if subrecipient)", C.CITES["pass_through"],
         f"{C.TRIBE_SHORT}", "§3.3"],
        ["Procurement standards", C.CITES["procurement"],
         f"{C.TRIBE_SHORT}", "Art. 4"],
        ["Competition / methods / sole-source justification", C.CITES["methods"],
         f"{C.TRIBE_SHORT}", "§4.2"],
        ["Conflict of interest & mandatory disclosures", C.CITES["conflict"],
         f"{C.TRIBE_SHORT}; {C.OPERATOR_SHORT}", "§4.4"],
        ["Debarment & suspension", C.CITES["debarment"],
         f"{C.TRIBE_SHORT} (verify); flow-down", "§4.5; §11.2"],
        ["Program income", C.CITES["prog_income"],
         f"{C.TRIBE_SHORT}", "Art. 5; Deliv. 5 §4.9"],
        ["Build America, Buy America", C.CITES["baba"],
         f"{C.OPERATOR_SHORT} (certify)", "§6.1"],
        ["Prohibited §889 telecom equipment", C.CITES["telecom_ban"],
         f"{C.OPERATOR_SHORT} (certify)", "§6.2"],
        ["NEPA environmental review", C.CITES["nepa"],
         f"{C.TRIBE_SHORT} + {C.AGENCY_SHORT}", "§7.1, 7.3"],
        ["NHPA §106 historic preservation", C.CITES["nhpa"],
         f"{C.TRIBE_SHORT} + {C.AGENCY_SHORT}", "§7.2, 7.3"],
        ["No construction before clearance / NTIA authorization", C.CITES["sac"],
         f"{C.OPERATOR_SHORT}", "§7.3"],
        ["Service floor & low-cost option", C.CITES["nofo"],
         f"{C.OPERATOR_SHORT}", "§8.1"],
        ["Duplication of funding", C.CITES["nofo"],
         f"{C.PARTIES_COLLECTIVE}", "§8.2"],
        ["Audit access & single audit", C.CITES["single_audit"],
         f"{C.TRIBE_SHORT}; {C.OPERATOR_SHORT}", "§9.1"],
        ["Record retention (3 years)", C.CITES["records"],
         f"{C.TRIBE_SHORT}; {C.OPERATOR_SHORT}", "§9.2; Deliv. 5 §4.4"],
        ["Reporting (semi-annual / annual)", C.CITES["sac"],
         f"{C.TRIBE_SHORT} (with {C.OPERATOR_SHORT} data)", "§9.3"],
        ["Allowable costs & cost allocation", C.CITES["allowable"],
         f"{C.TRIBE_SHORT}; {C.OPERATOR_SHORT}", "§9.4"],
        ["Asset disposition (≥ $10,000 threshold)", C.CITES["equipment"],
         f"{C.TRIBE_SHORT} + {C.AGENCY_SHORT} instructions", "Art. 10"],
        ["Sale/lease/assignment/encumbrance restriction; IRU structuring", C.CITES["real_property"],
         f"{C.TRIBE_SHORT} + {C.AGENCY_SHORT} prior approval", "§10.2"],
        ["Remedies for noncompliance", C.CITES["remedies"],
         f"{C.TRIBE_SHORT}; {C.OPERATOR_SHORT}", "§11.1"],
        ["Flow-down to subcontractors", C.CITES["pass_through"],
         f"{C.OPERATOR_SHORT}", "§11.2"],
        ["Lumbee recognition / eligibility predicate", C.CITES["lumbee_act"],
         f"{C.TRIBE_SHORT} + counsel + {C.AGENCY_SHORT}", "§1.3"],
        ["Order of precedence (Award & 2 CFR 200 control)", C.CITES["ug_part"],
         f"{C.PARTIES_COLLECTIVE}", "§1.4, 11.3"],
    ]
    C.add_table(doc, rm_headers, rm_rows,
                widths=[2.35, 2.55, 1.5, 1.05], font_size=7.5)

    # ---- Acknowledgment / signature block
    C.spacer(doc, 1)
    C.section(doc, "12.1", "Acknowledgment")
    P(doc,
      f"Each Party acknowledges that it has read this Addendum, understands that the "
      f"{C.PROGRAM_SHORT} Award and {C.CITES['ug_part']} control over any conflicting commercial "
      f"term, and agrees to perform its obligations so as to preserve the {C.FEDERAL_INTEREST} in, "
      f"and the {C.TRIBE_SHORT}’s title to, the {C.TRIBAL_ASSETS}. This Addendum does not "
      f"constitute legal or grant-compliance advice and remains subject to review by the "
      f"{C.PARTIES_COLLECTIVE}’ respective counsel and by {C.AGENCY_SHORT}.")

    C.signature_block(
        doc,
        extra_note="This Addendum must be confirmed by grant counsel and, where indicated, by NTIA "
                   "before execution. The contractor-vs-subrecipient determination, the Lumbee "
                   "eligibility predicate, and the IRU disposition/encumbrance structuring are "
                   "gating items.")

    path = C.save(doc, "02_Core_Agreements", "05_TBCP_Grant_Compliance_and_Federal_Interest_Addendum.docx")
    return path


# ===========================================================================
#  MAIN
# ===========================================================================
if __name__ == "__main__":
    p1 = build_financial_schedule()
    p2 = build_grant_addendum()
    print("GENERATED:")
    print("  Deliverable 5:", p1)
    print("  Deliverable 6:", p2)
