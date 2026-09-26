"""
gen_finance_land.py — Generator for two coordinated Definitive Agreements in the
Lumbee Tribe of North Carolina / RIVR Tech TBCP fiber package.

Produces:
  02_Definitive_Agreements/07_Grant_Finance_Reimbursement_Program_Income_and_Audit_Agreement.docx
  02_Definitive_Agreements/08_Land_Easement_ROW_Pole_and_Facility_Instruments.docx

Uses ONLY the canonical engine (Scripts/common.py) for all constants, party names,
defined terms, citations, deal mechanics, precedence, and formatting. Nothing is
invented: award #, routes, prices, useful life, approvals, land rights, and consents
are all left as flagged placeholders per the deal brief.
"""

from __future__ import annotations

import sys
sys.path.insert(0, "/home/user/claude-skills/Lumbee_RIVR_TBCP_Agreement_Package/Scripts")
import common as C


# ---------------------------------------------------------------------------
# Shared building blocks (identical across both documents)
# ---------------------------------------------------------------------------
DOC_FIN = f'07 — {C.AGREEMENTS["finance"]}'
DOC_LAND = f'08 — {C.AGREEMENTS["land"]}'

# Verbatim cross-reference targets
XREF_MASTER = C.AGREEMENTS["master"]
XREF_S9 = f'Schedule S9 ({C.SCHEDULES["S9"]})'
XREF_S8 = f'Schedule S8 ({C.SCHEDULES["S8"]})'
XREF_S3 = f'Schedule S3 ({C.SCHEDULES["S3"]})'
XREF_S14 = f'Schedule S14 ({C.SCHEDULES["S14"]})'
XREF_S10 = f'Schedule S10 ({C.SCHEDULES["S10"]})'
XREF_RETAIL = C.AGREEMENTS["retail"]
XREF_IRU = C.AGREEMENTS["iru"]
XREF_INTER = C.AGREEMENTS["interconnect"]
XREF_LREMC_CONSENT = "the LREMC Consent and Joinder (03 — Governance and Authorizations)"
XREF_PHASE1 = ("the Phase 1 Diligence subrecipient-vs-contractor determination "
               "(01 — Phase 1 Diligence)")


def precedence_article(doc, article_no):
    """Order-of-precedence article — verbatim engine text."""
    C.article(doc, article_no, "Order of Precedence")
    C.section(doc, f"{article_no}.1", "Ranking of Instruments",
              "In the event of any conflict, ambiguity, or inconsistency among the "
              "instruments comprising this transaction, the following order of "
              "precedence controls, from highest to lowest:")
    for i, item in enumerate(C.PRECEDENCE, start=1):
        C.numbered(doc, item)
    C.section(doc, f"{article_no}.2", "Conflict Rule", C.PRECEDENCE_RULE)
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Counsel to confirm that the precedence ranking above is reproduced "
                "verbatim in each Definitive Agreement so no instrument silently reorders it.")


def shared_definitions_article(doc, article_no):
    """Shared-definitions article — verbatim engine text."""
    C.article(doc, article_no, "Defined Terms; Shared Definitions")
    C.section(doc, f"{article_no}.1", "Single Shared Definitions Source",
              C.SHARED_DEFINITIONS_RULE)
    C.para(doc,
           f"Without limitation, the terms {C.TRIBE_DEFINED}, {C.OPERATOR_DEFINED}, "
           f"{C.LREMC_DEFINED}, “{C.NETWORK}”, “{C.GRANT_FUNDED}”, "
           f"“{C.LREMC_ASSETS}”, “{C.FEDERAL_INTEREST}”, "
           f"“{C.PROGRAM_INCOME}”, “{C.SERVICE_TERRITORY}”, and "
           f"“{C.ACTIVE_SUBSCRIBER}” have the meanings given in Article 2 of the "
           f"{XREF_MASTER}.")


def party_intro(doc, agreement_name):
    """Recital / parties intro tailored to a two-party agreement (Tribe + RIVR Tech)."""
    C.para(doc,
           f"This {agreement_name} (this “Agreement”) is entered into as of "
           f"{C.PH('Effective Date')} (the “Effective Date”), by and between "
           f"{C.TRIBE_FULL} (the “{C.TRIBE_SHORT}”), as the {C.PROGRAM_SHORT} award "
           f"recipient and steward and owner of the {C.GRANT_FUNDED}, and "
           f"{C.OPERATOR_FULL} (“{C.OPERATOR_SHORT}”), as design-engineer-procure-construct "
           f"(DEPC) contractor, network operator, and retail service provider. The "
           f"{C.TRIBE_SHORT} and {C.OPERATOR_SHORT} are each a “{C.PARTY_SINGULAR}” and "
           f"together the “{C.PARTIES_COLLECTIVE}.”")


def lremc_notice(doc):
    """Standard LREMC separateness clause reused in both documents."""
    C.flag_para(doc, C.FLAG_ATTORNEY,
                f"{C.LREMC_FULL} (“{C.LREMC_SHORT}”) is a separate legal entity and is "
                f"the owner of the {C.LREMC_ASSETS} (poles, conduit, fiber, easements, huts, "
                f"power, and land). {C.LREMC_SHORT} is not {C.OPERATOR_SHORT}; the "
                f"{C.LREMC_ASSETS} are not owned by {C.OPERATOR_SHORT} and are not "
                f"{C.GRANT_FUNDED}. Nothing in this Agreement transfers, encumbers, guarantees, "
                f"or creates any debt or financing obligation of {C.LREMC_SHORT}, and any use of "
                f"the {C.LREMC_ASSETS} requires {C.LREMC_SHORT}'s separate consent, joinder, and "
                f"signature under {XREF_LREMC_CONSENT}.")


def disclaimer(doc):
    """Standard closing disclaimer that ends the body of every document in the package."""
    C.spacer(doc, 1)
    C.article(doc, "—", "Disclaimer and Reservation")
    C.status_banner(doc)
    C.para(doc,
           "This document is a PRELIMINARY WORKING DRAFT prepared for discussion and "
           "negotiation only. No controlling TBCP award, Notice of Funding Opportunity, "
           "Specific Award Conditions, approved application, or other source document has "
           "been supplied. The provisional baseline used for structuring is the "
           f"{C.NOFO_NAME}. {C.NOFO_LIVE_NOTE}")
    C.para(doc,
           "This draft does not constitute legal, financial, tax, engineering, or grant-"
           "compliance advice, does not create any binding obligation, and is not an offer "
           "capable of acceptance. Award numbers, routes, prices, useful-life figures, "
           "approvals, land rights, and third-party consents shown as bracketed placeholders "
           "have NOT been supplied and must not be assumed, invented, or relied upon. Every "
           "bracketed flag and highlighted placeholder must be resolved, and the controlling "
           "Award confirmed, before any provision is finalized or executed.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Sovereign-immunity, waiver, dispute-resolution, and governing-law provisions "
                "are presented elsewhere in the package as bracketed ALTERNATIVES and require "
                "tribal-counsel and outside-counsel review. No provision waives the sovereign "
                "immunity of the Lumbee Tribe except by an express, written, and duly authorized "
                "waiver; see " + C.CITES["sovereign_immunity"] + ".")


# ===========================================================================
#  DOC 1 — GRANT FINANCE, REIMBURSEMENT, PROGRAM INCOME, AND AUDIT AGREEMENT
# ===========================================================================
def build_finance():
    doc = C.new_doc()
    C.add_cover(doc, DOC_FIN, C.AGREEMENTS["finance"],
                "Cost accounting, reimbursement, program income, Federal Interest, and audit")
    C.setup_header_footer(doc, "07 Grant Finance / Program Income / Audit")
    C.add_toc(doc)

    # --- Preamble ---------------------------------------------------------
    C.status_banner(doc)
    C.spacer(doc, 1)
    party_intro(doc, C.AGREEMENTS["finance"])
    lremc_notice(doc)
    C.flag_para(doc, C.FLAG_GRANT,
                "The financial mechanics in this Agreement are provisional and are subject to "
                "the controlling Award and any written NTIA/DOC determination; see "
                + C.CITES["sac"] + ".")

    # --- ARTICLE 1: Purpose & scope --------------------------------------
    C.article(doc, 1, "Purpose, Scope, and Grant Framework")
    C.section(doc, "1.1", "Purpose",
              f"This Agreement governs cost accounting, actual-cost support, reimbursement, "
              f"cash management, program income, Federal Interest, records, reporting, "
              f"certifications, audit, disallowed-cost responsibility, and closeout for the "
              f"{C.PROGRAM_FULL} ({C.PROGRAM_SHORT}) project undertaken by the "
              f"{C.TRIBE_SHORT} and operated by {C.OPERATOR_SHORT}.")
    C.section(doc, "1.2", "Uniform Guidance Governs",
              f"All financial administration under this Agreement conforms to "
              f"{C.CITES['ug_part']}, as revised ({C.CITES['ug_2024']}), the NTIA/DOC award "
              f"terms, and the controlling Award.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Confirm the executed Award, the controlling NOFO round (Round 3 is live; the "
                "provisional baseline is Round 2 as amended March 2024), and the Specific Award "
                "Conditions before finalizing any figure or method herein.")

    # --- ARTICLE 2: Definitions & shared definitions ---------------------
    shared_definitions_article(doc, 2)

    # --- ARTICLE 3: Precedence -------------------------------------------
    precedence_article(doc, 3)

    # --- ARTICLE 4: Chart of accounts / cost codes -----------------------
    C.article(doc, 4, "Chart of Accounts and Cost Codes")
    C.section(doc, "4.1", "Uniform Cost Coding",
              "The Parties shall maintain a uniform chart of accounts and cost-code "
              "structure that ties every cost to a budget line in the approved budget, a "
              "cost category, and the responsible Party, sufficient to trace each dollar "
              "from source document to reimbursement request to financial report.")
    C.section(doc, "4.2", "Cost Code Register",
              f"The cost-code register is maintained at {C.PH('cost-code register location / system')} "
              f"and reconciled to {XREF_S8} and to the approved budget.")
    _cost_evidence_table(doc)

    # --- ARTICLE 5: Allowability / allocability / reasonableness ---------
    C.article(doc, 5, "Allowability, Allocability, and Reasonableness")
    C.section(doc, "5.1", "Cost Principles",
              f"Every cost charged to the Award, claimed for reimbursement, or offset against "
              f"program income must be allowable, allocable, and reasonable under {C.CITES['allowable']} "
              f"and consistent with the approved budget and the controlling Award.")
    C.section(doc, "5.2", "Prohibited and Restricted Costs",
              f"No cost prohibited by the Award or applicable law (including {C.CITES['telecom_ban']} "
              f"and non-compliant procurement under {C.CITES['procurement']}) may be charged. "
              f"Costs requiring prior approval shall not be incurred without it.")
    C.section(doc, "5.3", "Burden of Support",
              f"The Party incurring a cost bears the burden of demonstrating allowability, "
              f"allocability, and reasonableness with contemporaneous documentation.")

    # --- ARTICLE 6: Actual-cost support ----------------------------------
    C.article(doc, 6, "Actual-Cost Support")
    C.section(doc, "6.1", "Actual Cost Basis",
              "Reimbursement and program-income offsets are based on actual, incurred, and "
              "paid costs, not estimates, standard costs, or list prices, except where a "
              "compliant indirect-cost rate applies under Article 7.")
    C.section(doc, "6.2", "Source Documentation",
              "Each cost must be supported by source documentation adequate to establish the "
              "amount, date, vendor, purpose, allocability to the project, and payment.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Support standards must match the Award's reimbursement basis (actual cost vs. "
                "milestone) once the Award is supplied.")

    # --- ARTICLE 7: Indirect costs / loaded labor / timekeeping ----------
    C.article(doc, 7, "Indirect Costs, Loaded Labor, and Timekeeping")
    C.section(doc, "7.1", "Indirect Cost Rate",
              f"Indirect costs are charged only under a negotiated indirect cost rate agreement "
              f"(NICRA) or the de minimis rate permitted by {C.CITES['ug_part']}, as applicable and "
              f"as the Award permits: {C.PH('indirect cost rate basis — NICRA / de minimis / none')}.")
    C.section(doc, "7.2", "Loaded Labor",
              f"Loaded labor rates must be built from actual base pay plus documented, allowable "
              f"fringe and, where applicable, an approved indirect rate—never marked-up or "
              f"composite rates that embed unallowable costs or profit on federal cost.")
    C.section(doc, "7.3", "Timekeeping",
              "Personnel costs charged to the project must be supported by after-the-fact "
              "records reflecting actual time worked, certified by the employee or a "
              "responsible supervisory official, and reconciled to payroll.")

    # --- ARTICLE 8: Equipment logs ---------------------------------------
    C.article(doc, 8, "Equipment and Property Records")
    C.section(doc, "8.1", "Equipment Records",
              f"Equipment acquired with Award funds is managed and recorded in accordance with "
              f"{C.CITES['equipment']}, including a property record with description, source, "
              f"title holder, acquisition cost and date, federal share, location, use, condition, "
              f"and ultimate disposition.")
    C.section(doc, "8.2", "Physical Inventory and Control",
              f"A physical inventory is reconciled to the property records at least once every "
              f"two years, with a control system to prevent loss, damage, or theft, per "
              f"{C.CITES['equipment']}.")
    C.section(doc, "8.3", "Supplies and Intangibles",
              f"Supplies and intangible property are handled under {C.CITES['supplies']} and "
              f"{C.CITES['intangible']} respectively.")

    # --- ARTICLE 9: Material reconciliation ------------------------------
    C.article(doc, 9, "Material Reconciliation")
    C.section(doc, "9.1", "Materials to Installed Plant",
              "Materials and equipment procured for the project shall be reconciled from "
              "purchase to receipt to installed or inventoried plant, so that quantities "
              "charged match quantities deployed or on hand, with variances explained.")
    C.section(doc, "9.2", "Salvage and Excess",
              "Salvage, excess, and returned materials are tracked and credited to the project "
              "to prevent overcharge.")

    # --- ARTICLE 10: POs / invoices / payment evidence -------------------
    C.article(doc, 10, "Purchase Orders, Invoices, and Payment Evidence")
    C.section(doc, "10.1", "Procurement Trail",
              f"Each procurement shall be supported by a procurement file consistent with "
              f"{C.CITES['procurement']} and {C.CITES['competition']}, including solicitation, "
              f"selection basis, purchase order, invoice, and proof of payment.")
    C.section(doc, "10.2", "Three-Way Match",
              "Payment evidence must permit a three-way match of purchase order, receiving "
              "record, and invoice before a cost is claimed.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Domestic-preference and Build America, Buy America requirements ("
                + C.CITES["baba"] + " and " + C.CITES["domestic"] + ") must be evidenced in the "
                "procurement file where applicable.")

    # --- ARTICLE 11: Budget control & change approval --------------------
    C.article(doc, 11, "Budget Control and Change Approval")
    C.section(doc, "11.1", "Budget Control",
              "Costs are controlled against the approved budget by line and category; overruns "
              "are not reimbursable absent approved budget revision.")
    C.section(doc, "11.2", "Change Approval",
              f"Budget revisions and reprogramming that require prior written NTIA/DOC approval "
              f"under {C.CITES['ug_part']} and the Award shall not be implemented until approved. "
              f"Internal change control: {C.PH('internal budget-change approval workflow')}.")

    # --- ARTICLE 12: Matching / duplicate funding ------------------------
    C.article(doc, 12, "Matching, Nonfederal Sources, and Prevention of Duplicate Funding")
    C.section(doc, "12.1", "Matching / Cost Share",
              f"Matching or cost-share, if any, {C.PH('match / cost-share requirement — confirm from Award')} "
              f"shall be documented, allowable, and verifiable and shall not be drawn from another "
              f"federal source except as expressly authorized.")
    C.section(doc, "12.2", "No Duplicate Funding",
              f"No cost shall be charged to, or reimbursed by, more than one funding source. "
              f"Costs, locations, and routes funded by other programs (including other broadband "
              f"programs) shall be segregated to prevent duplicate funding of the same location or "
              f"facility. Overlap analysis is maintained in {XREF_S3}.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Confirm no location/route overlap with any other federal or state broadband award "
                "before charging costs; duplicate funding is a disallowance and potential enforcement risk.")

    # --- ARTICLE 13: Reimbursement packages ------------------------------
    C.article(doc, 13, "Reimbursement Packages")
    C.section(doc, "13.1", "Package Contents",
              "Each reimbursement request shall assemble the supporting cost documentation "
              "(Article 6), procurement trail (Article 10), timekeeping (Article 7), and cost-"
              "code mapping (Article 4) into a reviewable package tied to the approved budget.")
    C.section(doc, "13.2", "Review and Certification",
              f"The {C.TRIBE_SHORT}, as recipient, reviews and certifies each package before "
              f"submission; {C.OPERATOR_SHORT} provides the underlying support and cooperates in "
              f"review. Submission cadence: {C.PH('reimbursement submission frequency')}.")

    # --- ARTICLE 14: Cash management -------------------------------------
    C.article(doc, 14, "Cash Management")
    C.section(doc, "14.1", "Minimization of Time",
              f"Cash management follows {C.CITES['ug_part']}: the time between draw and "
              f"disbursement is minimized; advance payments, if any, are held and accounted for "
              f"consistent with the Award.")
    C.section(doc, "14.2", "Interest on Advances",
              "Interest earned on any advanced federal funds is accounted for and remitted or "
              "retained only as the Uniform Guidance and the Award permit.")

    # --- ARTICLE 15: Separate ledgers ------------------------------------
    C.article(doc, 15, "Separate Ledgers and Accounting Segregation")
    C.section(doc, "15.1", "Separate Ledgers",
              f"The project is accounted for in SEPARATE LEDGERS that segregate Award-funded "
              f"activity, the {C.GRANT_FUNDED}, program income, and non-project activity from "
              f"{C.OPERATOR_SHORT}'s and the {C.TRIBE_SHORT}'s other operations, so that project "
              f"costs and receipts are identifiable without allocation from commingled accounts.")
    C.section(doc, "15.2", "No Commingling",
              f"Award funds and program income shall not be commingled with unrelated funds "
              f"except as a compliant restricted-account structure permits (Article 18).")

    # --- ARTICLE 16: Customer & wholesale receipts -----------------------
    C.article(doc, 16, "Customer and Wholesale Receipts")
    C.section(doc, "16.1", "Receipt Capture",
              f"All retail customer receipts and any wholesale, transport, or commercial-use "
              f"receipts arising from the {C.GRANT_FUNDED} or the {C.NETWORK} are captured, "
              f"recorded, and reconciled, and are evaluated for program-income treatment under "
              f"Article 17. Retail billing detail is maintained under {XREF_RETAIL} and {XREF_S8}; "
              f"commercial/non-project use under {XREF_S10}.")
    C.section(doc, "16.2", "Per-Active-Subscriber Payment",
              f"The operating payment from {C.OPERATOR_SHORT} to the {C.TRIBE_SHORT} is "
              f"{C.DEAL['per_subscriber_amount']}, determined by the {C.ACTIVE_SUBSCRIBER} "
              f"methodology in {XREF_S8}; its characterization for program-income purposes is "
              f"governed by Article 17.")

    # --- ARTICLE 17: Program income --------------------------------------
    C.article(doc, 17, "Program Income")
    C.section(doc, "17.1", "Program Income Method",
              f"Program income is identified, recorded, and applied under {C.CITES['prog_income']}. "
              f"{C.DEAL['program_income_note']}.")
    C.section(doc, "17.2", "Restricted Project Account",
              f"Program income is deposited to, and disbursed from, a restricted project account "
              f"maintained for the project, and is applied by the method the Award specifies "
              f"(deduction, addition, or cost-sharing/matching) per {C.CITES['prog_income']}.")
    C.flag_para(doc, C.FLAG_GRANT,
                "The program-income METHOD (deduction / addition / cost-sharing) and the treatment "
                "of the per-subscriber payment turn on the controlling Award and a written NTIA "
                "determination, NOT on the payment's label. Confirm before finalizing.")
    _program_income_table(doc)

    # --- ARTICLE 18: Reserves --------------------------------------------
    C.article(doc, 18, "Reserves")
    C.section(doc, "18.1", "Lifecycle and Compliance Reserves",
              f"Reserves for lifecycle refresh, spares, and continuity are funded and accounted "
              f"for as {C.PH('reserve funding source and amount')}; a reserve funded from program "
              f"income remains subject to {C.CITES['prog_income']} and the Award.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Whether a reserve may be funded from program income or the Award, and how it is "
                "treated at closeout, requires Award confirmation.")

    # --- ARTICLE 19: Federal Interest ------------------------------------
    C.article(doc, 19, "Federal Interest")
    C.section(doc, "19.1", "Federal Interest Attaches",
              f"A {C.FEDERAL_INTEREST} attaches to real property and equipment acquired or "
              f"improved with Award funds under {C.CITES['real_property']} "
              f"and {C.CITES['equipment']}, and continues for the period the Award and Uniform "
              f"Guidance require.")
    C.section(doc, "19.2", "Property Trust Relationship",
              f"The {C.TRIBE_SHORT} holds Award-funded real property and equipment in trust for "
              f"the beneficiaries of the Award under {C.CITES['trust']}; use, encumbrance, and "
              f"disposition are restricted under {C.CITES['real_property']}.")
    C.section(doc, "19.3", "No Liens Against Federal-Interest or Trust/Restricted Property",
              f"No lien, security interest, mortgage, foreclosure, attachment, levy, or execution "
              f"shall be created against, or enforced upon, property subject to the "
              f"{C.FEDERAL_INTEREST}, or against trust or restricted property, except as the Award, "
              f"the Uniform Guidance, and applicable federal law expressly permit. Any purported "
              f"encumbrance in violation of this Section is void.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Disposition, sale, or encumbrance of Federal-Interest property requires prior "
                "NTIA/DOC approval; see " + C.CITES["real_property"] + " and " + C.CITES["closeout"] + ".")

    # --- ARTICLE 20: Records retention -----------------------------------
    C.article(doc, 20, "Records Retention")
    C.section(doc, "20.1", "Three-Year Retention",
              f"Financial and programmatic records are retained for {C.DEAL['records_retention_years']} "
              f"years measured as {C.CITES['records']} requires (generally from submission of the "
              f"final expenditure report), and longer if litigation, claim, or audit is pending.")
    C.section(doc, "20.2", "Form and Integrity",
              "Records are maintained in a form that preserves integrity, auditability, and "
              "retrievability for the full retention period.")

    # --- ARTICLE 21: Site & record access --------------------------------
    C.article(doc, 21, "Site and Record Access")
    C.section(doc, "21.1", "Access Rights",
              f"The {C.TRIBE_SHORT}, NTIA, DOC, the Inspector General, the Comptroller General, "
              f"and their authorized representatives shall have timely access to project sites, "
              f"records, and personnel for examination, audit, and copying under {C.CITES['records']}.")
    C.section(doc, "21.2", "Notice",
              f"Routine access is on {C.DEAL['audit_notice_business_days']} business days' notice; "
              f"federal-oversight access is on the notice the Uniform Guidance and the Award require, "
              f"and emergency or fraud-related access is immediate.")

    # --- ARTICLE 22: Single audit ----------------------------------------
    C.article(doc, 22, "Single Audit")
    C.section(doc, "22.1", "Subpart F Audit",
              f"If the {C.TRIBE_SHORT} expends $1,000,000 or more in federal awards in a fiscal "
              f"year, a single or program-specific audit is obtained under {C.CITES['single_audit']}.")
    C.section(doc, "22.2", "Cooperation and Findings",
              f"{C.OPERATOR_SHORT} cooperates with the audit and supplies underlying records; audit "
              f"findings, corrective action plans, and the summary schedule of prior audit findings "
              f"are tracked to resolution.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Confirm the single-audit threshold and applicability once total federal expenditures "
                "are known; see " + C.CITES["single_audit"] + ".")

    # --- ARTICLE 23: Reporting -------------------------------------------
    C.article(doc, 23, "Financial and Performance Reporting")
    C.section(doc, "23.1", "Reports",
              f"Financial and performance reports are prepared and submitted on the cadence and "
              f"forms the Award and NTIA/DOC require: {C.PH('reporting cadence and forms — per Award')}.")
    C.section(doc, "23.2", "Supporting Data",
              f"{C.OPERATOR_SHORT} timely provides subscriber counts, receipts, cost data, and "
              f"deployment metrics needed for reporting, reconciled to the separate ledgers.")

    # --- ARTICLE 24: Certifications --------------------------------------
    C.article(doc, 24, "Certifications")
    C.section(doc, "24.1", "Cost Certifications",
              f"Each reimbursement request and financial report is certified by a responsible "
              f"official as to accuracy, allowability, and compliance, subject to the civil and "
              f"criminal penalties for false claims.")
    C.section(doc, "24.2", "Mandatory Disclosures and Debarment",
              f"The Parties comply with mandatory-disclosure obligations ({C.CITES['disclosures']}) "
              f"and debarment/suspension requirements ({C.CITES['debarment']}), and certify no "
              f"excluded party is used.")

    # --- ARTICLE 25: Disallowed costs & repayment (cause-based) ----------
    C.article(doc, 25, "Disallowed Costs and Repayment Responsibility")
    C.section(doc, "25.1", "Repayment Follows Cause",
              "Responsibility for a disallowed cost, questioned cost, or required repayment "
              "follows the CAUSE of the disallowance: the Party (or its contractor or "
              "subcontractor) whose act, omission, misrepresentation, or noncompliance caused "
              "the disallowance bears the resulting cost, as between the Parties.")
    C.section(doc, "25.2", "Notice and Response Before Allocation",
              f"Before any repayment responsibility is allocated between the Parties, the Party to "
              f"be charged receives written notice describing the disallowance and its asserted "
              f"cause and a reasonable opportunity (not less than {C.DEAL['cure_nonmonetary_days']} "
              f"days) to respond, cure, or contest, and to participate in any response to NTIA/DOC.")
    C.section(doc, "25.3", "Recipient Obligation to the Government",
              f"As between the Parties and the government, the {C.TRIBE_SHORT} remains the recipient "
              f"responsible to NTIA/DOC; this Article allocates the economic burden between the "
              f"Parties and does not limit the government's remedies under {C.CITES['remedies']}.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Cause-based allocation, caps, and interplay with indemnity and limitation of "
                "liability require counsel review and coordination with Schedule S12.")

    # --- ARTICLE 26: Closeout --------------------------------------------
    C.article(doc, 26, "Closeout")
    C.section(doc, "26.1", "Closeout Actions",
              f"At project end, the Parties complete closeout under {C.CITES['closeout']}, including "
              f"final reports, liquidation of obligations, refund of unobligated balances, and "
              f"final program-income accounting.")
    C.section(doc, "26.2", "Property Disposition",
              f"Disposition of Federal-Interest equipment and real property at closeout follows "
              f"{C.CITES['equipment']} and {C.CITES['real_property']} and requires any NTIA/DOC "
              f"approval the Award specifies.")

    # --- ARTICLE 27: Post-closeout obligations ---------------------------
    C.article(doc, 27, "Post-Closeout Obligations")
    C.section(doc, "27.1", "Continuing Responsibilities",
              f"After closeout, the Parties remain subject to post-closeout adjustments, continuing "
              f"property and Federal-Interest restrictions, records retention, audit, and repayment "
              f"obligations under {C.CITES['closeout']} for so long as the Uniform Guidance and the "
              f"Award require.")

    # --- ARTICLE 28: Contractor vs. subrecipient -------------------------
    C.article(doc, 28, "Contractor-vs-Subrecipient Treatment")
    C.section(doc, "28.1", "Determination Cross-Reference",
              f"Whether {C.OPERATOR_SHORT}'s role is that of a contractor or a subrecipient is "
              f"determined under {C.CITES['subrecipient']} and documented in {XREF_PHASE1}. This "
              f"Agreement's financial mechanics apply consistent with that determination.")
    C.section(doc, "28.2", "Pass-Through Requirements If Subrecipient",
              f"If, and to the extent, {C.OPERATOR_SHORT} is a subrecipient, the {C.TRIBE_SHORT} as "
              f"pass-through entity imposes and monitors the requirements of {C.CITES['pass_through']}, "
              f"including a subaward agreement, risk assessment, and subrecipient monitoring.")
    C.flag_para(doc, C.FLAG_GRANT,
                "The contractor-vs-subrecipient determination materially changes flow-down, "
                "monitoring, and audit obligations; confirm the Phase 1 determination before finalizing.")

    # --- Execution --------------------------------------------------------
    C.article(doc, 29, "Execution")
    C.para(doc,
           f"This Agreement is between the {C.TRIBE_SHORT} and {C.OPERATOR_SHORT}. {C.LREMC_SHORT} "
           f"is not a party; its separate consent and joinder, where relevant to the "
           f"{C.LREMC_ASSETS}, are given under {XREF_LREMC_CONSENT}.")
    C.signature_block(doc,
                      extra_note="Confirm signatory authority via tribal resolution (Schedule S1) "
                                 "and RIVR Tech corporate authorization before execution.")

    disclaimer(doc)
    path = C.save(doc, "02_Definitive_Agreements",
                  "07_Grant_Finance_Reimbursement_Program_Income_and_Audit_Agreement.docx")
    return path


def _cost_evidence_table(doc):
    C.para(doc, "Table 4-A — Cost Category / Required Evidence Matrix:", bold=True)
    headers = ["Cost Category", "Required Actual-Cost Evidence", "Governing Authority"]
    rows = [
        ["Labor (direct)",
         "Timesheets certified by employee/supervisor; payroll registers; labor-rate buildup",
         C.CITES["allowable"]],
        ["Loaded / indirect labor",
         "NICRA or de minimis rate documentation; fringe support; allocation base",
         C.CITES["ug_part"]],
        ["Equipment",
         "PO; invoice; proof of payment; property record; §889 compliance evidence",
         C.CITES["equipment"] + "; " + C.CITES["telecom_ban"]],
        ["Materials / supplies",
         "PO; invoice; receiving record; material reconciliation to installed plant",
         C.CITES["supplies"]],
        ["Subcontracts / procurement",
         "Solicitation; selection basis; contract; invoice; payment; BABA/domestic-preference support",
         C.CITES["procurement"] + "; " + C.CITES["baba"]],
        ["Program income receipts",
         "Subscriber/wholesale receipt detail; restricted-account deposit records; reconciliation",
         C.CITES["prog_income"]],
        ["Real property",
         "Acquisition/closing documents; Federal-Interest notation; appraisal where required",
         C.CITES["real_property"] + "; " + C.CITES["trust"]],
    ]
    C.add_table(doc, headers, rows, widths=[1.6, 3.4, 2.0])


def _program_income_table(doc):
    C.para(doc, "Table 17-A — Program-Income Treatment Decision Matrix (provisional):", bold=True)
    C.flag_para(doc, C.FLAG_GRANT,
                "This matrix is a decision aid only; the controlling method is fixed by the Award and "
                "a written NTIA determination under " + C.CITES["prog_income"] + ".")
    headers = ["Receipt Type", "Likely Characterization", "Method Options (Award-controlled)", "Restricted Account?"]
    rows = [
        ["Per-Active-Subscriber operating payment (" + C.DEAL["per_subscriber_amount"] + ")",
         C.PH("program income vs. asset-use consideration — Award-dependent"),
         "Deduction / Addition / Cost-share",
         "Yes, pending determination"],
        ["Retail broadband subscriber revenue",
         C.PH("program income if earned from Grant-Funded Assets — confirm"),
         "Deduction / Addition / Cost-share",
         "Yes, pending determination"],
        ["Wholesale / transport / commercial-use receipts",
         C.PH("program income — confirm scope vs. Schedule S10"),
         "Deduction / Addition / Cost-share",
         "Yes, pending determination"],
        ["Interest on advanced federal funds",
         "Not program income; remit/retain per Uniform Guidance",
         "Remit or retain per rule",
         "Segregate and account"],
        ["Proceeds of disposition of Federal-Interest property",
         "Subject to disposition rules, not ordinary program income",
         "Per " + C.CITES["closeout"],
         "Yes; NTIA/DOC approval"],
    ]
    C.add_table(doc, headers, rows, widths=[1.9, 2.2, 1.7, 1.2])


# ===========================================================================
#  DOC 2 — LAND, EASEMENT, ROW, POLE, SITE, POWER, AND FACILITY INSTRUMENTS
# ===========================================================================

# Common clauses reused by every land-instrument form -----------------------
def _term_clause(doc, label):
    C.subsection(doc, "term", C.PH(label) + "; provided that the term shall run for a period "
                 "at least as long as the related network-use obligation for the "
                 f"{C.NETWORK} and the {C.GRANT_FUNDED} it supports (including the "
                 f"{C.DEAL['iru_term_recommended']}-year IRU term and {C.DEAL['iru_renewal']}), or "
                 "shall provide a lawful and enforceable replacement or relocation remedy that "
                 "preserves continuity of the network-use rights for that period, but in no event "
                 "longer than the underlying grantor's own interest permits.")


def _common_form_clauses(doc, permitted_use, grantor_label, grantee_label, extra_recording=True):
    """Emit the standard clause set required for every land instrument form."""
    C.subsection(doc, "permitted use", permitted_use)
    C.subsection(doc, "construction & maintenance access",
                 f"{grantee_label} and its authorized contractors may access the premises to "
                 f"survey, construct, install, inspect, test, operate, maintain, repair, and "
                 f"replace the facilities, subject to reasonable prior notice and the grantor's "
                 f"reasonable safety and operating rules.")
    C.subsection(doc, "emergency access",
                 "Immediate access is permitted, without prior notice, to respond to an outage, "
                 "hazard, or threat to public safety or service continuity, with prompt notice "
                 "given as soon as practicable.")
    C.subsection(doc, "restoration",
                 "After any work, the premises shall be restored to a condition reasonably "
                 "equivalent to its prior condition, ordinary wear excepted.")
    C.subsection(doc, "relocation",
                 f"Relocation of facilities, if required, shall follow {C.PH('relocation terms — cost responsibility and notice')}; "
                 f"where relocation would defeat the network-use obligation, a replacement right of "
                 f"equivalent utility shall be provided so continuity is preserved.")
    C.subsection(doc, "assignment",
                 f"Assignment requires {C.PH('assignment consent standard')}; permitted assignments "
                 f"run to successors and assigns and to any operator of the {C.NETWORK}, subject to "
                 f"grant, Award, and (for trust/restricted or {C.LREMC_SHORT} interests) required approvals.")
    C.subsection(doc, "successor recognition",
                 "This instrument binds and benefits the parties' heirs, successors, and permitted "
                 "assigns, and shall be recognized by any successor owner or operator of the affected land or facilities.")
    if extra_recording:
        C.subsection(doc, "recording",
                     f"This instrument (or a memorandum of it) may be recorded in the appropriate "
                     f"public records at {C.PH('recording office / county')}, subject to any approval "
                     f"required before recording.")
    C.subsection(doc, "taxes & fees",
                 f"Taxes, fees, and charges, if any, are allocated as {C.PH('tax / fee allocation')}; "
                 f"nothing herein waives any applicable governmental or tribal exemption.")


def _grantor_grantee_sig(doc, grantor_full, grantee_full, approval_block=None):
    C.spacer(doc, 1)
    p = doc.add_paragraph()
    r = p.add_run("EXECUTION — this form to be executed by the named grantor and grantee:")
    r.italic = True
    for role, full in [("GRANTOR", grantor_full), ("GRANTEE", grantee_full)]:
        p = doc.add_paragraph()
        rr = p.add_run(f"{role}:  {full}")
        rr.bold = True
        rr.font.color.rgb = C.NAVY
        for label in ["By: ____________________________________",
                      f"Name: {C.PH('authorized signatory')}",
                      f"Title: {C.PH('title')}",
                      "Date: ____________________________________"]:
            lp = doc.add_paragraph()
            lp.paragraph_format.left_indent = C.Inches(0.25)
            C._emit_runs(lp, label)
        C.spacer(doc, 1)
    if approval_block:
        approval_block(doc)


def _bia_approval_block(doc):
    p = doc.add_paragraph()
    r = p.add_run("REQUIRED FEDERAL APPROVAL — Bureau of Indian Affairs:")
    r.bold = True
    r.font.color.rgb = C.RED
    C.para(doc,
           f"This instrument affects trust or restricted Indian land and is not effective until "
           f"approved by the Bureau of Indian Affairs (BIA) as required by {C.CITES['bia_approval']}, "
           f"{C.CITES['indian_leasing']}, and {C.CITES['indian_row']}, as applicable.")
    for label in ["Approved by (BIA): ____________________________________",
                  f"Name/Title: {C.PH('BIA approving official')}",
                  "Date: ____________________________________"]:
        lp = doc.add_paragraph()
        lp.paragraph_format.left_indent = C.Inches(0.25)
        C._emit_runs(lp, label)
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Confirm whether the affected land is trust, restricted, or fee, and the exact BIA "
                "approval pathway, before use; the Lumbee Tribe's land status must be verified.")


def _lremc_consent_block(doc):
    p = doc.add_paragraph()
    r = p.add_run(f"REQUIRED SEPARATE CONSENT — {C.LREMC_SHORT}:")
    r.bold = True
    r.font.color.rgb = C.RED
    C.para(doc,
           f"The facilities licensed under this form are {C.LREMC_ASSETS} owned by {C.LREMC_FULL} "
           f"(“{C.LREMC_SHORT}”), a separate entity that is not {C.OPERATOR_SHORT}. This form "
           f"is not effective as to any {C.LREMC_ASSETS} without {C.LREMC_SHORT}'s own signature and "
           f"consent under {XREF_LREMC_CONSENT}. Nothing herein transfers ownership of, or creates any "
           f"debt, guarantee, or financing obligation of, {C.LREMC_SHORT}.")
    p = doc.add_paragraph()
    rr = p.add_run(f"CONSENTING OWNER:  {C.LREMC_FULL}")
    rr.bold = True
    rr.font.color.rgb = C.NAVY
    for label in ["By: ____________________________________",
                  f"Name: {C.PH('authorized LREMC signatory')}",
                  f"Title: {C.PH('title')}",
                  "Date: ____________________________________"]:
        lp = doc.add_paragraph()
        lp.paragraph_format.left_indent = C.Inches(0.25)
        C._emit_runs(lp, label)


def build_land():
    doc = C.new_doc()
    C.add_cover(doc, DOC_LAND, C.AGREEMENTS["land"],
                "Form instruments and parcel/facility register for network land and access rights")
    C.setup_header_footer(doc, "08 Land / Easement / ROW / Pole / Facility Instruments")
    C.add_toc(doc)

    # --- Preamble ---------------------------------------------------------
    C.status_banner(doc)
    C.spacer(doc, 1)
    C.para(doc,
           f"This document assembles the FORM land, easement, right-of-way, pole, site, power, "
           f"and facility instruments required to site and access the {C.NETWORK} and the "
           f"{C.GRANT_FUNDED}, together with a parcel/facility register cross-referenced to "
           f"{XREF_S9}. Each form is a template to be completed for a specific parcel or facility; "
           f"none is effective until completed, approved as required, and executed by the correct owner.")
    lremc_notice(doc)

    # --- ARTICLE 1: General provisions -----------------------------------
    C.article(doc, 1, "General Provisions Applicable to All Instruments")
    C.section(doc, "1.1", "Tribe Cannot Grant What It Does Not Own",
              f"The {C.TRIBE_SHORT} may grant only those land, access, and facility rights it "
              f"actually owns or is lawfully authorized to convey. The {C.TRIBE_SHORT} does not, and "
              f"cannot, grant any interest in land or facilities it does not own, including the "
              f"{C.LREMC_ASSETS}, individually owned (allotted) land, public rights-of-way, NCDOT "
              f"corridors, railroad corridors, or third-party property.")
    C.section(doc, "1.2", "LREMC-Owned Facilities Require LREMC's Separate Signature",
              f"Any right to attach to, place within, or use the {C.LREMC_ASSETS} (poles, conduit, "
              f"fiber, easements, huts, power, and land owned by {C.LREMC_SHORT}) requires "
              f"{C.LREMC_SHORT}'s own separate consent and signature under {XREF_LREMC_CONSENT}. "
              f"{C.OPERATOR_SHORT} does not own the {C.LREMC_ASSETS} and cannot grant rights in them.")
    C.section(doc, "1.3", "No Liens Against Trust or Restricted Land",
              f"No lien, mortgage, security interest, attachment, levy, execution, or foreclosure "
              f"shall be created against or enforced upon trust or restricted Indian land, or upon "
              f"property subject to the {C.FEDERAL_INTEREST}, except as federal law expressly permits. "
              f"Any purported encumbrance in violation of this Section is void.")
    C.section(doc, "1.4", "Required Approvals",
              f"Instruments affecting trust or restricted land require BIA approval "
              f"({C.CITES['bia_approval']}, {C.CITES['indian_leasing']}, {C.CITES['indian_row']}); "
              f"instruments in NCDOT corridors require NCDOT encroachment authorization "
              f"({C.CITES['nc_ncdot']}); pole attachments engage {C.CITES['nc_pole']}; and all are "
              f"subject to the Award and {XREF_S14}.")
    C.section(doc, "1.5", "Term Floor",
              f"Every access instrument shall have a term at least as long as the related "
              f"network-use obligation it supports, or shall provide a lawful replacement or "
              f"relocation remedy preserving continuity; see the term clause in each form.")

    # --- ARTICLE 2: Shared definitions -----------------------------------
    shared_definitions_article(doc, 2)

    # --- ARTICLE 3: Precedence -------------------------------------------
    precedence_article(doc, 3)

    # --- ARTICLE 4: Parcel / facility register ---------------------------
    C.article(doc, 4, "Parcel and Facility Register")
    C.section(doc, "4.1", "Register",
              f"The parcels, sites, poles, corridors, and facilities used by the {C.NETWORK}, their "
              f"ownership, the instrument type used, and the approvals required are recorded in the "
              f"register below and maintained in full in {XREF_S9}.")
    _register_table(doc)
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Ownership, legal descriptions, land status (fee / trust / restricted / allotted), and "
                "required approvals in the register are placeholders and must be verified for each "
                "parcel and facility before any instrument is used.")

    # --- ARTICLE 5: FORMS -------------------------------------------------
    C.article(doc, 5, "Form Instruments")

    # FORM 1 — Tribal fee-land lease
    C.section(doc, "5.1", "FORM 1 — Tribal Fee-Land Lease")
    C.para(doc,
           f"For land owned by the {C.TRIBE_SHORT} in fee (not trust or restricted). Use only where "
           f"tribal fee ownership is confirmed.")
    C.subsection(doc, "parties",
                 f"Landlord: {C.TRIBE_FULL}. Tenant: {C.PH('tenant — Tribe / RIVR Tech / network entity')}.")
    C.subsection(doc, "legal description", C.PH("legal description of the tribal fee parcel"))
    _term_clause(doc, "term of the fee-land lease")
    _common_form_clauses(doc,
                         permitted_use=f"Siting, construction, operation, and maintenance of the "
                                       f"{C.GRANT_FUNDED} and related network facilities.",
                         grantor_label="Landlord", grantee_label="Tenant")
    _grantor_grantee_sig(doc, C.TRIBE_FULL, C.PH("tenant entity"))

    # FORM 2 — Trust/restricted land lease [BIA]
    C.section(doc, "5.2", "FORM 2 — Trust / Restricted Indian Land Lease [BIA APPROVAL]")
    C.para(doc,
           f"For land held in trust or restricted status. Governed by {C.CITES['indian_leasing']} and "
           f"subject to BIA approval under {C.CITES['bia_approval']}.")
    C.subsection(doc, "parties",
                 f"Lessor: {C.PH('trust/restricted landowner — Tribe or United States in trust')}. "
                 f"Lessee: {C.PH('lessee — network entity / RIVR Tech')}.")
    C.subsection(doc, "legal description",
                 C.PH("legal description + trust/restricted status and tract number"))
    _term_clause(doc, "term of the trust/restricted-land lease (within limits BIA approval permits)")
    _common_form_clauses(doc,
                         permitted_use=f"Siting, construction, operation, and maintenance of the "
                                       f"{C.GRANT_FUNDED}, subject to {C.CITES['indian_leasing']}.",
                         grantor_label="Lessor", grantee_label="Lessee")
    C.flag_para(doc, C.FLAG_GRANT,
                "No lien, foreclosure, or attachment against the trust/restricted land is permitted; "
                "confirm compatibility with the Federal Interest and " + C.CITES["trust"] + ".")
    _grantor_grantee_sig(doc, C.PH("trust/restricted lessor"), C.PH("lessee entity"),
                         approval_block=_bia_approval_block)

    # FORM 3 — ROW easement (incl. trust-land ROW under Part 169)
    C.section(doc, "5.3", "FORM 3 — Right-of-Way Easement")
    C.para(doc,
           f"For linear crossings and corridors. Where the ROW crosses trust or restricted Indian "
           f"land, {C.CITES['indian_row']} and BIA approval ({C.CITES['bia_approval']}) apply; where "
           f"it crosses individually owned (allotted) land, allottee consent and BIA approval apply.")
    C.subsection(doc, "parties",
                 f"Grantor: {C.PH('ROW grantor — landowner / allottee(s) / United States in trust')}. "
                 f"Grantee: {C.PH('ROW grantee — network entity / RIVR Tech')}.")
    C.subsection(doc, "legal description",
                 C.PH("centerline / corridor description, width, and station limits"))
    _term_clause(doc, "term of the right-of-way easement")
    _common_form_clauses(doc,
                         permitted_use="A right-of-way for the construction, operation, and "
                                       "maintenance of fiber and appurtenant facilities within the described corridor.",
                         grantor_label="Grantor", grantee_label="Grantee")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Select the correct ROW pathway (fee / public / trust under " + C.CITES["indian_row"] +
                " / allotted with allottee consent) per parcel; do not assume land status.")
    _grantor_grantee_sig(doc, C.PH("ROW grantor"), C.PH("ROW grantee"))

    # FORM 3A — Individually owned (allotted) land note
    C.subsection(doc, "allotted-land variant",
                 f"Where the parcel is individually owned (allotted) Indian land, add the consent of "
                 f"the required percentage of allottee interests and BIA approval "
                 f"({C.CITES['bia_approval']}, {C.CITES['indian_row']}); the {C.TRIBE_SHORT} cannot "
                 f"grant an interest in allotted land it does not own.")

    # FORM 4 — Pole / conduit / facility license (LREMC)
    C.section(doc, "5.4", "FORM 4 — Pole, Conduit, and Facility License [LREMC CONSENT]")
    C.para(doc,
           f"For attachment to or use of the {C.LREMC_ASSETS} (LREMC-owned poles, conduit, fiber, "
           f"huts, power, and land). {C.CITES['nc_pole']} governs broadband pole attachments. This "
           f"form is NOT effective without {C.LREMC_SHORT}'s separate signature.")
    C.subsection(doc, "parties",
                 f"Licensor: {C.LREMC_FULL} (“{C.LREMC_SHORT}”). Licensee: "
                 f"{C.PH('licensee — network entity / RIVR Tech')}.")
    C.subsection(doc, "facilities licensed",
                 C.PH("pole IDs / conduit segments / hut & power specifications — from Schedule S9"))
    _term_clause(doc, "term of the pole/conduit/facility license")
    _common_form_clauses(doc,
                         permitted_use=f"Attachment to and use of designated {C.LREMC_ASSETS} for the "
                                       f"{C.NETWORK}, subject to {C.CITES['nc_pole']}, make-ready, and "
                                       f"{C.LREMC_SHORT}'s construction and safety standards.",
                         grantor_label="Licensor", grantee_label="Licensee")
    C.subsection(doc, "make-ready & power",
                 C.PH("make-ready, attachment fees, and metered/unmetered power terms — per LREMC"))
    _grantor_grantee_sig(doc, C.LREMC_FULL, C.PH("licensee entity"),
                         approval_block=_lremc_consent_block)

    # FORM 5 — NCDOT encroachment
    C.section(doc, "5.5", "FORM 5 — NCDOT Encroachment Agreement")
    C.para(doc,
           f"For facilities within North Carolina Department of Transportation corridors. Governed "
           f"by {C.CITES['nc_ncdot']} and the NCDOT utility accommodation policy. This is a state "
           f"encroachment authorization; the {C.TRIBE_SHORT} does not own the NCDOT corridor.")
    C.subsection(doc, "parties",
                 f"Authority: North Carolina Department of Transportation. Applicant/Encroaching Party: "
                 f"{C.PH('applicant — network entity / RIVR Tech')}.")
    C.subsection(doc, "location", C.PH("route / highway / county / station limits within NCDOT ROW"))
    _term_clause(doc, "term / duration of the NCDOT encroachment authorization")
    _common_form_clauses(doc,
                         permitted_use="Placement, operation, and maintenance of fiber and appurtenant "
                                       "facilities within the NCDOT right-of-way, subject to NCDOT permit conditions.",
                         grantor_label="NCDOT", grantee_label="Encroaching Party",
                         extra_recording=False)
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "NCDOT uses its own encroachment forms and conditions; this template maps required "
                "terms and must be conformed to the current NCDOT instrument (" + C.CITES["nc_ncdot"] + ").")
    _grantor_grantee_sig(doc, "North Carolina Department of Transportation", C.PH("encroaching party"))

    # FORM 6 — Third-party consent (incl. railroad crossings, other facilities)
    C.section(doc, "5.6", "FORM 6 — Third-Party Consent, License, or Crossing Agreement")
    C.para(doc,
           f"For public rights-of-way not owned by the {C.TRIBE_SHORT}, railroad crossings, and any "
           f"other third-party land or facilities. The {C.TRIBE_SHORT} cannot grant rights in "
           f"third-party property; the third-party owner must sign.")
    C.subsection(doc, "parties",
                 f"Owner/Authority: {C.PH('third party — railroad / municipality / utility / landowner')}. "
                 f"Grantee: {C.PH('grantee — network entity / RIVR Tech')}.")
    C.subsection(doc, "facility / crossing",
                 C.PH("crossing / license description — e.g., railroad crossing point, public ROW segment"))
    _term_clause(doc, "term of the third-party consent / crossing agreement")
    _common_form_clauses(doc,
                         permitted_use="Placement, crossing, operation, and maintenance of network "
                                       "facilities on or across the third party's property, subject to its conditions.",
                         grantor_label="Owner", grantee_label="Grantee")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Railroad and utility owners typically require their own crossing/license forms, "
                "insurance, and fees; conform this template to each owner's instrument.")
    _grantor_grantee_sig(doc, C.PH("third-party owner/authority"), C.PH("grantee entity"))

    # --- ARTICLE 6: Approvals & recording summary ------------------------
    C.article(doc, 6, "Approvals, Recording, and Coordination")
    C.section(doc, "6.1", "Approvals Are Conditions Precedent",
              f"Each required approval (BIA, NCDOT, {C.LREMC_SHORT} consent, allottee consent, third-"
              f"party owner signature, and any NTIA/DOC approval affecting the Federal Interest) is a "
              f"condition precedent to the effectiveness of the corresponding instrument. Required "
              f"approvals are tracked in {XREF_S14}.")
    C.section(doc, "6.2", "Coordination with Federal Interest",
              f"No instrument shall encumber or dispose of Federal-Interest or trust/restricted property "
              f"contrary to {C.CITES['real_property']}, {C.CITES['trust']}, or the Award.")

    disclaimer(doc)
    path = C.save(doc, "02_Definitive_Agreements",
                  "08_Land_Easement_ROW_Pole_and_Facility_Instruments.docx")
    return path


def _register_table(doc):
    C.para(doc, "Table 4-A — Parcel / Facility Register (cross-ref " + XREF_S9 + "):", bold=True)
    headers = ["Ref", "Parcel / Facility", "Owner", "Land Status", "Instrument (Form)", "Required Approval"]
    rows = [
        ["1", C.PH("tribal fee parcel"), C.TRIBE_SHORT, "Fee", "Form 1 — Tribal Fee Lease", "Tribal authorization"],
        ["2", C.PH("trust/restricted tract"), C.PH("Tribe / U.S. in trust"), "Trust/Restricted",
         "Form 2 — Trust-Land Lease", "BIA (" + C.CITES["bia_approval"] + ")"],
        ["3", C.PH("allotted parcel"), C.PH("individual allottee(s)"), "Allotted",
         "Form 3 — ROW Easement", "Allottee consent + BIA"],
        ["4", C.PH("ROW corridor"), C.PH("landowner"), C.PH("fee/public/trust"),
         "Form 3 — ROW Easement", C.PH("per land status")],
        ["5", C.PH("pole line / conduit"), C.LREMC_SHORT, C.LREMC_ASSETS,
         "Form 4 — Pole/Facility License", C.LREMC_SHORT + " consent (" + C.CITES["nc_pole"] + ")"],
        ["6", C.PH("hut / cabinet / power site"), C.PH("LREMC / other"), C.PH("owned by non-Tribe party"),
         "Form 4 / Form 6", C.PH("owner consent")],
        ["7", C.PH("NCDOT corridor segment"), "NCDOT", "State ROW",
         "Form 5 — NCDOT Encroachment", "NCDOT (" + C.CITES["nc_ncdot"] + ")"],
        ["8", C.PH("railroad crossing"), C.PH("railroad"), "Railroad corridor",
         "Form 6 — Third-Party Consent", "Railroad crossing agreement"],
        ["9", C.PH("public ROW / third-party site"), C.PH("municipality / third party"), "Third-party",
         "Form 6 — Third-Party Consent", "Owner signature"],
    ]
    C.add_table(doc, headers, rows, widths=[0.4, 1.3, 1.1, 1.0, 1.5, 1.7], font_size=8)


# ===========================================================================
if __name__ == "__main__":
    p1 = build_finance()
    p2 = build_land()
    print("GENERATED:")
    print("  DOC 1:", p1)
    print("  DOC 2:", p2)
