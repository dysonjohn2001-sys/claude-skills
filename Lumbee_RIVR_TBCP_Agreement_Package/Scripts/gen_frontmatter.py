"""
gen_frontmatter.py — FRONT-MATTER + COMPLIANCE generator for the coordinated
Lumbee Tribe of North Carolina / RIVR Tech TBCP fiber agreement package.

Builds 4 files using the canonical engine common.py (SINGLE SOURCE OF TRUTH):
  1. 00_START_HERE/01_Executive_Summary_and_Transaction_Structure.docx
  2. 00_START_HERE/02_Agreement_Register_and_Signing_Sequence.docx
  3. 06_Compliance/01_Clause_by_Clause_Compliance_Crosswalk.xlsx
  4. 06_Compliance/02_Closing_and_Implementation_Plan.xlsx

PRELIMINARY DRAFT. No controlling award or source documents supplied.
Never invents facts — unknowns are placeholders / flags.
"""

from __future__ import annotations

import sys
sys.path.insert(0, '/home/user/claude-skills/Lumbee_RIVR_TBCP_Agreement_Package/Scripts')
import common as C  # noqa: E402

from docx.shared import Pt  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.worksheet.datavalidation import DataValidation  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402


# ---------------------------------------------------------------------------
# Shared closing disclaimer for Word bodies
# ---------------------------------------------------------------------------
DISCLAIMER_TEXT = (
    "This document is a preliminary working draft prepared for discussion only. It is not final "
    "legal, grant, or financial advice and creates no binding obligation on any party. No controlling "
    "TBCP award, Notice of Funding Opportunity in executed form, Specific Award Conditions, or other "
    "source documents were supplied; the provisional baseline is the March 2024 amended Round 2 NOFO, "
    "and the controlling round and executed award must be confirmed before any provision is finalized. "
    "All party names, defined terms, economics, dates, and citations are subject to legal, grant, and "
    "financial review. Capitalized terms used and not otherwise defined have the meanings given in "
    "Article 2 (Definitions) of the " + C.AGREEMENTS["master"] + ", the single shared definitions "
    "source for the package. Nothing herein should be relied upon as fact where marked as a placeholder "
    "or flagged for review."
)


def closing_disclaimer(doc):
    C.spacer(doc, 1)
    C.status_banner(doc)
    p = doc.add_paragraph()
    r = p.add_run(DISCLAIMER_TEXT)
    r.italic = True
    r.font.size = Pt(9)
    r.font.color.rgb = C.GREY
    p2 = doc.add_paragraph()
    r2 = p2.add_run(C.CONFIDENTIAL)
    r2.italic = True
    r2.font.size = Pt(9)
    r2.font.color.rgb = C.GREY


# ===========================================================================
#  GOVERNANCE / AUTHORIZATION DOCUMENTS (03_Governance_Authorizations, 7)
#  These titles match the ACTUAL files present in 03_Governance_Authorizations/.
#  Do not add titles not in that folder.
# ===========================================================================
GOVERNANCE = {
    "G1": "Lumbee Tribal Council Resolution",
    "G2": "RIVR Tech Member/Manager Authorization",
    "G3": "LREMC Consent and Joinder",
    "G4": "Limited Waiver of Sovereign Immunity (bracketed alternatives — FOR COUNSEL)",
    "G5": "Tax, TERO, Permitting, and Regulatory Schedule",
    "G6": "Insurance Schedule",
    "G7": "Service Level Schedule",
}


# ===========================================================================
#  FILE 1 — Executive Summary and Transaction Structure
# ===========================================================================
def build_executive_summary():
    doc = C.new_doc()
    C.add_cover(
        doc,
        "00 · START HERE — DOCUMENT 01",
        "Executive Summary and Transaction Structure",
        "Coordinated TBCP Fiber Agreement Package — Lumbee Tribe of North Carolina and RIVR Tech",
    )
    C.setup_header_footer(doc, "Executive Summary & Transaction Structure")
    C.add_toc(doc)

    # ARTICLE 1 — Preliminary status --------------------------------------
    C.article(doc, 1, "Preliminary Status, Baseline, and Reliance Limitations")
    C.section(doc, "1.1", "Preliminary Draft — No Controlling Award Supplied")
    C.para(doc,
           "This package is a PRELIMINARY draft prepared without any controlling TBCP award, executed "
           "Notice of Funding Opportunity, Specific Award Conditions, approved application, budget, or "
           "other source documents. " + C.FLAG_GRANT + " " + C.FLAG_ATTORNEY + " The provisional "
           "baseline used throughout is the " + C.NOFO_NAME + ". Every substantive position is a "
           "default drafting posture for negotiation, not a final term, and every unsupplied fact is "
           "shown as a highlighted placeholder — no facts have been invented.")
    C.section(doc, "1.2", "Round 3 Is Live — Controlling Round Must Be Confirmed")
    C.para(doc, C.NOFO_LIVE_NOTE)
    C.flag_para(doc, C.FLAG_GRANT,
                "Confirm the controlling TBCP round and the executed award (Round 2 baseline vs. the "
                "live Round 3 as of the version date) before any definitive clause is finalized.")
    C.section(doc, "1.3", "Order of Precedence")
    C.para(doc, "The instruments in this package rank, from highest to lowest authority, as follows:")
    for i, item in enumerate(C.PRECEDENCE, start=1):
        C.numbered(doc, item)
    C.para(doc, C.PRECEDENCE_RULE)

    # ARTICLE 2 — Parties and roles ---------------------------------------
    C.article(doc, 2, "Parties and Roles")
    C.para(doc,
           "Three entities are central to the transaction, each with a distinct role. They must not be "
           "conflated; in particular, " + C.OPERATOR_SHORT + " and " + C.LREMC_SHORT + " are separate "
           "entities with separate assets.")
    role_headers = ["Party (Defined Term)", "Full Legal Name", "Role in the Transaction"]
    role_rows = [
        [C.TRIBE_SHORT, C.TRIBE_FULL,
         "TBCP award recipient and steward; owner of the " + C.GRANT_FUNDED + "; holds the "
         "Federal Interest and grant-compliance obligations."],
        [C.OPERATOR_SHORT, C.OPERATOR_FULL,
         "Design/engineering/procurement/construction party (DEPC), network operator, and retail "
         "provider of record via the IRU; paid on a per-Active-Subscriber basis. Contractor-vs-"
         "subrecipient status to be determined (2 CFR 200.331)."],
        [C.LREMC_SHORT, C.LREMC_FULL,
         "Separate asset owner of " + C.LREMC_ASSETS + " (poles, conduit, fiber, easements, huts, "
         "power, land). Participates by consent/joinder only; its assets are never assumed owned by "
         + C.OPERATOR_SHORT + "."],
    ]
    C.add_table(doc, role_headers, role_rows, widths=[1.3, 2.4, 2.8])

    # ARTICLE 3 — Recommended transaction structure -----------------------
    C.article(doc, 3, "Recommended Transaction Structure and Business Model")
    C.section(doc, "3.1", "Business Model in Brief")
    C.bullet(doc, "The " + C.TRIBE_SHORT + " owns the " + C.GRANT_FUNDED + " (the grant-funded "
             "portion of the " + C.NETWORK + ") and holds the " + C.FEDERAL_INTEREST + ".")
    C.bullet(doc, C.OPERATOR_SHORT + " receives an " + C.IRU_TERM_DEFINED + " (Indefeasible Right of "
             "Use) and network-access rights, and acts as operator and retail provider of record within "
             "the " + C.SERVICE_TERRITORY + ".")
    C.bullet(doc, C.OPERATOR_SHORT + " pays the " + C.TRIBE_SHORT + " a per-Active-Subscriber "
             "operating payment (" + C.DEAL["per_subscriber_amount"] + "); economic characterization "
             "is provisional (see Article 6).")
    C.bullet(doc, C.LREMC_SHORT + " contributes " + C.LREMC_ASSETS + " only under a separate "
             "owner-approved agreement, consent, or joinder — never by assumption.")
    C.bullet(doc, "Term: " + str(C.IRU_TERM_RECOMMENDED) + " years from " + C.TERM_TRIGGER + ", plus "
             + C.IRU_RENEWAL_DEFAULT + ", subject to " + C.DEAL["term_ceiling_note"] + ".")
    C.section(doc, "3.2", "Responsibility Allocation")
    resp_headers = ["Function", "Primary", "Support / Consent"]
    resp_rows = [
        ["Asset ownership & Federal Interest", C.TRIBE_SHORT, C.OPERATOR_SHORT + " (steward duties)"],
        ["Design / engineering / procurement / construction", C.OPERATOR_SHORT + " (DEPC)", C.TRIBE_SHORT + " (approval)"],
        ["Network operations, maintenance, lifecycle", C.OPERATOR_SHORT, C.TRIBE_SHORT + " (oversight)"],
        ["Retail service, billing, subscribers", C.OPERATOR_SHORT + " (provider of record)", C.TRIBE_SHORT],
        ["Grant compliance, reporting, audit", C.TRIBE_SHORT + " (recipient)", C.OPERATOR_SHORT + " (records/support)"],
        ["Poles / conduit / land / power", C.LREMC_SHORT + " (owner)", "Tribe / RIVR Tech (consent/joinder)"],
    ]
    C.add_table(doc, resp_headers, resp_rows, widths=[2.6, 2.1, 1.8])

    C.section(doc, "3.3", "Asset Ownership Summary")
    asset_headers = ["Asset Class", "Owner", "Instrument Governing Use"]
    asset_rows = [
        [C.GRANT_FUNDED + " (grant-funded fiber/electronics)", C.TRIBE_SHORT, C.AGREEMENTS["iru"]],
        [C.OPERATOR_EXISTING + " (core/transport/NOC/billing)", C.OPERATOR_SHORT, C.AGREEMENTS["interconnect"]],
        [C.LREMC_ASSETS + " (poles/conduit/easements/huts/power/land)", C.LREMC_SHORT, C.AGREEMENTS["land"] + " (consent/joinder)"],
        [C.JOINT_ASSETS + " (if any)", "Per S3 register", C.AGREEMENTS["master"] + " + S3/S10"],
    ]
    C.add_table(doc, asset_headers, asset_rows, widths=[2.9, 1.5, 2.1])

    C.section(doc, "3.4", "Payment Flow Summary")
    pay_headers = ["Flow", "From → To", "Basis / Note"]
    pay_rows = [
        ["Retail revenue", "Subscribers → " + C.OPERATOR_SHORT, "Provider of record; net of taxes/fees"],
        ["Operating payment", C.OPERATOR_SHORT + " → " + C.TRIBE_SHORT, C.DEAL["per_subscriber_amount"] + " (primary model)"],
        ["Program income (if characterized)", C.TRIBE_SHORT + " → Award", "Per 2 CFR 200.307 and written NTIA determination"],
        ["Owner consideration (if any)", "Parties → " + C.LREMC_SHORT, "Per separate " + C.LREMC_SHORT + " agreement " + C.PH("terms")],
        ["Construction payments", C.TRIBE_SHORT + " → " + C.OPERATOR_SHORT, "DEPC milestones/retainage (S5)"],
    ]
    C.add_table(doc, pay_headers, pay_rows, widths=[2.1, 2.3, 2.1])

    # ARTICLE 4 — Threshold legal issues ----------------------------------
    C.article(doc, 4, "Threshold Legal Issues")
    C.section(doc, "4.1", "Lumbee Federal-Recognition Status (Threshold Eligibility)")
    C.para(doc,
           "Whether the " + C.TRIBE_SHORT + " qualifies as an eligible TBCP entity turns on its "
           "federal-recognition status under the " + C.CITES["lumbee_act"] + ". This is a threshold "
           "eligibility question that must be resolved before the parties rely on any term of this "
           "package. " + C.FLAG_GRANT + " " + C.FLAG_ATTORNEY)
    C.section(doc, "4.2", "Contractor vs. Subrecipient Determination")
    C.para(doc,
           C.OPERATOR_SHORT + "'s status must be determined under " + C.CITES["subrecipient"] + " and "
           "pass-through obligations under " + C.CITES["pass_through"] + ". The recommended structure "
           "positions " + C.OPERATOR_SHORT + " as a lean contractor (procuring services at defined "
           "prices, not administering the subaward), but the determination is substance-over-form and "
           "must be confirmed. " + C.FLAG_GRANT)
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "A contractor characterization avoids passing subrecipient monitoring duties to "
                + C.OPERATOR_SHORT + "; confirm against the controlling award and 2 CFR 200.331 factors.")

    # ARTICLE 5 — Package contents ----------------------------------------
    C.article(doc, 5, "Package Contents Summary")
    C.section(doc, "5.1", "The Ten Definitive Agreements (02_Definitive_Agreements)")
    ag_headers = ["#", "Definitive Agreement"]
    ag_rows = []
    for i, key in enumerate(["master", "depc", "iru", "interconnect", "om", "retail",
                             "finance", "land", "privacy", "transition"], start=1):
        ag_rows.append([f"{i:02d}", C.AGREEMENTS[key]])
    C.add_table(doc, ag_headers, ag_rows, widths=[0.5, 6.0], col_align=["c", "l"])

    C.section(doc, "5.2", "The Fourteen Schedules (05_Schedules)")
    sc_headers = ["S#", "Schedule"]
    sc_rows = [[k, v] for k, v in C.SCHEDULES.items()]
    C.add_table(doc, sc_headers, sc_rows, widths=[0.6, 5.9])

    C.section(doc, "5.3", "Governance & Authorizations (03_Governance_Authorizations, 7)")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Governance titles below are illustrative structural placeholders; exact instruments "
                "and content are subject to counsel confirmation.")
    gv_headers = ["#", "Governance / Authorization Document"]
    gv_rows = [[k, v] for k, v in GOVERNANCE.items()]
    C.add_table(doc, gv_headers, gv_rows, widths=[0.6, 5.9])

    C.section(doc, "5.4", "Other Package Components")
    C.bullet(doc, "01_Phase1_Diligence — 9 diligence work products.")
    C.bullet(doc, "04_Operational_Forms — 8 operational forms (NTP, acceptance, activation, etc.).")
    C.bullet(doc, "06_Compliance — clause-by-clause crosswalk and closing/implementation plan.")

    # ARTICLE 6 — Primary economics ---------------------------------------
    C.article(doc, 6, "Primary Economics and Payment Characterization")
    C.section(doc, "6.1", "Per-Active-Subscriber Operating Payment")
    C.para(doc,
           "The primary economic model is a per-Active-Subscriber operating payment of "
           + C.DEAL["per_subscriber_amount"] + ". An " + C.ACTIVE_SUBSCRIBER + " is counted per the "
           "canonical elements below.")
    for el in C.DEAL["active_subscriber_elements"]:
        C.bullet(doc, el)
    C.section(doc, "6.2", "Characterization Alternatives (Provisional)")
    C.para(doc, "The payment characterization is provisional; the label does not control program-income "
           "treatment. The alternatives are:")
    for opt_key in ["A", "B", "C", "D", "E"]:
        txt = C.DEAL["pay_options"][opt_key]
        if opt_key == C.DEAL["pay_recommended"]:
            txt += "  " + C.FLAG_BUSINESS + " RECOMMENDED"
        C.bullet(doc, txt)
    C.para(doc, C.DEAL["program_income_note"] + ". " + C.FLAG_GRANT)

    # ARTICLE 7 — Major open decisions ------------------------------------
    C.article(doc, 7, "Major Open Decisions")
    open_headers = ["Open Decision", "Type", "Recommended Position"]
    open_rows = [
        ["Controlling round / executed award", C.FLAG_GRANT, "Confirm Round 2 vs. live Round 3; obtain executed award"],
        ["Lumbee federal-recognition eligibility", C.FLAG_ATTORNEY, "Obtain eligibility opinion before reliance"],
        ["Contractor vs. subrecipient status", C.FLAG_GRANT, "Position RIVR Tech as lean contractor (200.331)"],
        ["Payment characterization", C.FLAG_BUSINESS, "Option " + C.DEAL["pay_recommended"] + " (per-subscriber); confirm program-income treatment"],
        ["Per-Active-Subscriber amount", C.FLAG_BUSINESS, C.PH("insert $ amount — not supplied")],
        ["Sovereign-immunity waiver scope", C.FLAG_ATTORNEY, "Narrow, express limited waiver for defined disputes"],
        ["LREMC consent / joinder terms", C.FLAG_BUSINESS, "Separate owner-approved instrument; no assumption"],
    ]
    C.add_table(doc, open_headers, open_rows, widths=[2.5, 1.6, 2.4])

    # ARTICLE 8 — Risk summary + recommended positions --------------------
    C.article(doc, 8, "Risk Summary and Recommended Positions")
    risk_headers = ["Risk", "Exposure", "Recommended Mitigation"]
    risk_rows = [
        ["No controlling award supplied", "All terms provisional; possible rework", "Confirm award/round before finalizing; keep placeholders"],
        ["Eligibility (Lumbee recognition)", "Threshold — award may be unavailable", "Eligibility opinion; NTIA confirmation"],
        ["Federal Interest on assets", "Encumbrance/disposition limits", "Reflect 200.311/.316 in IRU and Land Instruments"],
        ["§889 / BABA noncompliance", "Cost disallowance; termination", "Vendor screening in DEPC; certifications (S4/S5)"],
        ["Program-income mistreatment", "Audit finding; repayment", "Written NTIA determination on characterization"],
        ["Sovereign-immunity ambiguity", "Unenforceable remedies", "Express limited waiver with defined scope"],
    ]
    C.add_table(doc, risk_headers, risk_rows, widths=[2.1, 2.0, 2.4])
    C.para(doc, "Recommended overall posture: keep every economic and eligibility term provisional and "
           "flagged until the controlling award and the eligibility opinion are in hand; never treat a "
           "placeholder as a fact.")

    closing_disclaimer(doc)
    return C.save(doc, "00_START_HERE", "01_Executive_Summary_and_Transaction_Structure.docx")


# ===========================================================================
#  FILE 2 — Agreement Register and Signing Sequence
# ===========================================================================
def build_agreement_register():
    doc = C.new_doc()
    C.add_cover(
        doc,
        "00 · START HERE — DOCUMENT 02",
        "Agreement Register and Signing Sequence",
        "Coordinated TBCP Fiber Agreement Package — Lumbee Tribe of North Carolina and RIVR Tech",
    )
    C.setup_header_footer(doc, "Agreement Register & Signing Sequence")
    C.add_toc(doc)

    C.article(doc, 1, "Purpose")
    C.para(doc, "This register lists each Definitive Agreement and Governance/Authorization document, "
           "its parties, purpose, place in the signing sequence, conditions precedent, and the "
           "Schedules it requires. Document names and Schedule numbers are used verbatim from the "
           "canonical register. " + C.FLAG_ATTORNEY + " " + C.FLAG_GRANT)

    # Register data: (name, parties, purpose, seq#, conditions precedent, required schedules)
    T, O, L = C.TRIBE_SHORT, C.OPERATOR_SHORT, C.LREMC_SHORT
    reg_rows = [
        # Definitive Agreements
        [C.AGREEMENTS["master"], f"{T}; {O}",
         "Umbrella framework, shared definitions, precedence, governance",
         "3", "Governance authorizations executed; award confirmed", "S1, S2, S3, S14"],
        [C.AGREEMENTS["depc"], f"{T}; {O}",
         "Design, engineering, procurement, construction of Grant-Funded Assets",
         "4", "Master executed; environmental/NHPA clearances", "S2, S4, S5"],
        [C.AGREEMENTS["iru"], f"{T}; {O}",
         "Grants RIVR Tech the IRU and network-access/retail rights",
         "5", "Master executed; asset register (S3) settled", "S3, S10"],
        [C.AGREEMENTS["interconnect"], f"{T}; {O}",
         "Interconnection, transport, equipment, shared facilities",
         "6", "IRU executed; demarcation (S4) fixed", "S4, S9, S10"],
        [C.AGREEMENTS["om"], f"{T}; {O}",
         "Operations, maintenance, lifecycle, service levels",
         "7", "IRU executed; SLA schedule (S6) agreed", "S6, S12"],
        [C.AGREEMENTS["retail"], f"{T}; {O}",
         "Retail service, billing, collections, subscriber revenue",
         "8", "IRU executed; provider-of-record terms (S7) set", "S7, S8"],
        [C.AGREEMENTS["finance"], f"{T}; {O}",
         "Grant finance, reimbursement, program income, audit",
         "9", "Master executed; contractor/subrecipient determination", "S1, S8"],
        [C.AGREEMENTS["land"], f"{T}; {O}; {L} (consent/joinder)",
         "Land, easement, ROW, pole, site, power, facility instruments",
         "10", "LREMC consent; BIA/ROW approvals where applicable", "S9, S14"],
        [C.AGREEMENTS["privacy"], f"{T}; {O}",
         "Data privacy, cybersecurity, supply-chain risk, continuity",
         "11", "Retail and O&M executed", "S11"],
        [C.AGREEMENTS["transition"], f"{T}; {O}",
         "Continuity, step-in, termination assistance, transition",
         "12", "Master and O&M executed", "S13"],
        # Governance / Authorizations
        [GOVERNANCE["G1"], T,
         "Tribal Council authorizes award acceptance, transaction, signatories",
         "1", "Award/round confirmed; eligibility opinion", "S1"],
        [GOVERNANCE["G2"], O,
         "RIVR Tech entity authorization of the transaction and signatories",
         "1", "Corporate records current", "S1"],
        [GOVERNANCE["G3"], f"{L}; {T}; {O}",
         "LREMC board consent and joinder for use of LREMC Facilities",
         "2", "Facility inventory (S9) identified", "S9, S14"],
        [GOVERNANCE["G4"], f"{T}; {O}",
         "Limited express waiver of sovereign immunity; dispute consent",
         "2", "Scope of waiver approved by Tribal Council", "S1, S13"],
        [GOVERNANCE["G5"], f"{T}; {O}; {L}",
         "Signatory authority, incumbency, corporate/Tribal existence",
         "2", "Governance resolutions (G1/G2/G3) adopted", "S1"],
        [GOVERNANCE["G6"], f"{T} (with NTIA/DOC)",
         "Log of NTIA/DOC notices, consents, written determinations",
         "2", "Award confirmed; questions framed to NTIA", "S1, S14"],
        [GOVERNANCE["G7"], f"{T}; {O}; {L}",
         "Common-interest, confidentiality, attorney work-product",
         "1", "Parties identified", "—"],
    ]
    reg_headers = ["Document", "Parties", "Purpose", "Seq #", "Conditions Precedent", "Required Schedules"]
    C.add_table(doc, reg_headers, reg_rows,
                widths=[1.9, 1.15, 1.55, 0.45, 1.35, 0.9], font_size=8)

    C.article(doc, 2, "Signing-Sequence Narrative")
    C.para(doc, "The sequence numbers above group the closing into ordered stages. No commercial "
           "agreement is signed before the authority to sign it exists, and no segment goes live "
           "before the compliance predicates are satisfied.")
    C.section(doc, "2.1", "Stage 1 — Resolutions and Authorizations First")
    C.para(doc, "The Tribal Council authorizing resolution (G1), the RIVR Tech entity authorization "
           "(G2), the certificate of authorized signatories (G5), and the common-interest agreement "
           "(G7) come first. These establish who may bind each party and confirm the threshold "
           "eligibility and award posture. " + C.FLAG_ATTORNEY)
    C.section(doc, "2.2", "Stage 2 — Consents, Waiver, and Agency Coordination")
    C.para(doc, "The LREMC board consent/joinder (G3), the limited sovereign-immunity waiver (G4), and "
           "the NTIA/DOC notice-and-determination log (G6) are settled next, because later agreements "
           "depend on LREMC Facility access, enforceable remedies, and confirmed award treatment.")
    C.section(doc, "2.3", "Stage 3 — Master Agreement")
    C.para(doc, "The " + C.AGREEMENTS["master"] + " is executed next (sequence 3). It supplies the shared "
           "definitions, order of precedence, and governance that every downstream agreement "
           "incorporates.")
    C.section(doc, "2.4", "Stage 4 — The Remaining Definitive Agreements")
    C.para(doc, "The DEPC, IRU, Interconnection, O&M, Retail, Grant Finance, Land Instruments, and "
           "Privacy/Cyber agreements are executed in dependency order (sequences 4–11): construction "
           "and the IRU precede operations, retail, and finance, which precede the privacy addendum.")
    C.section(doc, "2.5", "Stage 5 — LREMC Consent Confirmed and Land Instruments")
    C.para(doc, "LREMC consent is confirmed in force and the Land Instruments (sequence 10) are "
           "recorded, together with any BIA/ROW approvals required where trust/restricted land is used "
           "or crossed. " + C.FLAG_GRANT)
    C.section(doc, "2.6", "Stage 6 — Segment NTP, Acceptance, and Activation Last")
    C.para(doc, "Notice to Proceed, segment acceptance, and subscriber activation occur last, once the "
           "controlling award, eligibility, environmental/NHPA clearances, and all approvals are "
           "confirmed. The " + str(C.IRU_TERM_RECOMMENDED) + "-year term runs from " + C.TERM_TRIGGER
           + ". " + C.FLAG_GRANT)

    closing_disclaimer(doc)
    return C.save(doc, "00_START_HERE", "02_Agreement_Register_and_Signing_Sequence.docx")


# ===========================================================================
#  FILE 3 — Clause-by-Clause Compliance Crosswalk (xlsx)
# ===========================================================================
def build_compliance_crosswalk():
    wb = Workbook()
    C.xl_instructions(wb, [
        "## Clause-by-Clause Compliance Crosswalk",
        "This workbook maps each federal compliance requirement to its controlling authority, where it "
        "is addressed in the package, its rule type, current status, and notes.",
        "",
        "## How to use",
        "• Filter the header row to focus on OPEN items or a single rule type.",
        "• The 'Where Addressed' column points to the governing agreement and Schedule(s).",
        "• The 'Type' column classifies each requirement as Mandatory / Interpretation / Recommended / Negotiable.",
        "• Status values: OPEN, IN PROGRESS, ADDRESSED, N/A.",
        "",
        "## Reliance limits",
        "• PRELIMINARY: no controlling award or source documents were supplied.",
        "• Provisional baseline is the March 2024 amended Round 2 NOFO; Round 3 is live and must be confirmed.",
        "• Citations are drawn from the canonical citation table; confirm against the executed award.",
    ], title="Compliance Crosswalk")

    ws = wb.create_sheet("Crosswalk")
    ws.sheet_properties.tabColor = "1F3864"
    C.xl_title(ws, "Clause-by-Clause Compliance Crosswalk",
               subtitle="Lumbee Tribe / RIVR Tech TBCP fiber package — " + C.DRAFT_VERSION, span=6)

    headers = ["Requirement", "Controlling Authority", "Where Addressed (Agreement / Schedule)",
               "Type", "Status", "Notes"]
    hdr_row = 5
    C.xl_header_row(ws, hdr_row, headers, freeze=True, filt=True)

    A = C.AGREEMENTS
    rows = [
        ["Recipient / entity eligibility (Tribal recognition)", C.CITES["lumbee_act"],
         A["master"] + "; S1/S14; Eligibility Opinion", "Mandatory", "OPEN",
         C.FLAG_GRANT + " " + C.FLAG_ATTORNEY + " Threshold eligibility; confirm before reliance."],
        ["Real property use, encumbrance, disposition; property trust",
         C.CITES["real_property"] + "; " + C.CITES["trust"],
         A["iru"] + "; " + A["land"] + "; S3/S9", "Mandatory", "OPEN",
         "Federal Interest limits on encumbrance/disposition must flow into IRU and land instruments."],
        ["Equipment management, records, and disposition (200.313(d))", C.CITES["equipment"],
         A["om"] + "; " + A["finance"] + "; S3/S6", "Mandatory", "OPEN",
         "Property records, physical inventory, control, and disposition procedures required."],
        ["Procurement standards, competition, methods",
         C.CITES["procurement"] + "; " + C.CITES["competition"] + "; " + C.CITES["methods"],
         A["depc"] + "; " + A["finance"] + "; S5", "Mandatory", "OPEN",
         C.FLAG_GRANT + " Confirm procurement record supports the DEPC pricing."],
        ["Contractor vs. subrecipient determination; pass-through duties",
         C.CITES["subrecipient"] + "; " + C.CITES["pass_through"],
         A["master"] + "; " + A["finance"] + "; S1", "Mandatory", "OPEN",
         C.FLAG_GRANT + " Position RIVR Tech as lean contractor; substance-over-form."],
        ["Program income", C.CITES["prog_income"],
         A["retail"] + "; " + A["finance"] + "; S8", "Interpretation", "OPEN",
         C.DEAL["program_income_note"] + "."],
        ["Build America, Buy America (domestic content)", C.CITES["baba"],
         A["depc"] + "; S4/S5", "Mandatory", "OPEN",
         "Iron/steel, manufactured products, construction materials; certifications required."],
        ["Prohibited telecommunications equipment (§889 covered)", C.CITES["telecom_ban"],
         A["depc"] + "; " + A["privacy"] + "; S4/S11", "Mandatory", "OPEN",
         "Vendor screening and certifications; no covered equipment/services."],
        ["NEPA environmental review", C.CITES["nepa"],
         A["master"] + "; " + A["depc"] + "; S2/S9", "Mandatory", "OPEN",
         "Complete before ground-disturbing construction / NTP."],
        ["NHPA Section 106 historic-preservation review", C.CITES["nhpa"],
         A["depc"] + "; " + A["land"] + "; S9", "Mandatory", "OPEN",
         "Tribal/SHPO consultation; complete before NTP."],
        ["Record retention and access (3 years)", C.CITES["records"],
         A["finance"] + "; all agreements; S8", "Mandatory", "OPEN",
         "Retention measured from final report; access for auditors."],
        ["Single audit (Subpart F)", C.CITES["single_audit"],
         A["finance"] + "; S8", "Mandatory", "OPEN",
         "Applies at/above the $1,000,000 federal-award expenditure threshold."],
        ["Property disposition on termination/closeout",
         C.CITES["real_property"] + "; " + C.CITES["equipment"],
         A["iru"] + "; " + A["om"] + "; " + A["transition"] + "; S3/S13", "Mandatory", "OPEN",
         "Disposition instructions per Federal Interest; step-in continuity."],
        ["Cost principles (allowability/allocability/reasonableness)", C.CITES["allowable"],
         A["finance"] + "; " + A["depc"] + "; S5/S8", "Mandatory", "OPEN",
         "Costs charged to the award must satisfy Subpart E."],
        ["Domestic preferences for procurements", C.CITES["domestic"],
         A["depc"] + "; S5", "Recommended", "OPEN",
         "Preference for domestic goods/services to the extent practicable."],
        ["Conflict of interest / standards of conduct",
         C.CITES["conflict"] + "; " + C.CITES["oci"],
         A["master"] + "; Governance; S1", "Mandatory", "OPEN",
         "Written standards of conduct; organizational COI screening (LREMC affiliation)."],
        ["Remedies for noncompliance; termination", C.CITES["remedies"],
         A["master"] + "; " + A["transition"] + "; S13", "Mandatory", "OPEN",
         "Enforcement, disallowance, suspension, termination pathways."],
        ["Closeout and post-closeout adjustments", C.CITES["closeout"],
         A["finance"] + "; " + A["transition"] + "; S8/S13", "Mandatory", "OPEN",
         "Final reports, liquidation, continuing obligations."],
        ["Affordability and 100/20 Mbps service floor",
         "TBCP NOFO / ID Guidance; " + C.CITES["usac_lifeline"],
         A["retail"] + "; S7", "Mandatory", "OPEN",
         "Service floor " + C.SPEED_FLOOR + "; affordability commitments per award."],
        ["Open, nondiscriminatory middle-mile interconnection",
         C.CITES["nofo"] + "; " + C.CITES["id_guidance"],
         A["interconnect"] + "; S4/S10", "Interpretation", "OPEN",
         "Open-access/interconnection expectations; confirm scope in controlling award."],
    ]

    r = hdr_row + 1
    for row in rows:
        C.xl_cell(ws, r, 1, row[0], kind="text", wrap=True, align="left")
        C.xl_cell(ws, r, 2, row[1], kind="text", wrap=True, align="left")
        C.xl_cell(ws, r, 3, row[2], kind="text", wrap=True, align="left")
        C.xl_cell(ws, r, 4, row[3], kind="input", wrap=True, align="center")
        C.xl_cell(ws, r, 5, row[4], kind="input", align="center")
        C.xl_cell(ws, r, 6, row[5], kind="text", wrap=True, align="left")
        r += 1

    # Column widths
    for col, w in zip("ABCDEF", [34, 40, 34, 16, 12, 46]):
        ws.column_dimensions[col].width = w

    # Data validation on Type and Status
    dv_type = DataValidation(type="list",
                             formula1='"Mandatory,Interpretation,Recommended,Negotiable"',
                             allow_blank=True)
    ws.add_data_validation(dv_type)
    dv_type.add(f"D{hdr_row+1}:D{r-1}")
    dv_status = DataValidation(type="list",
                               formula1='"OPEN,IN PROGRESS,ADDRESSED,N/A"',
                               allow_blank=True)
    ws.add_data_validation(dv_status)
    dv_status.add(f"E{hdr_row+1}:E{r-1}")

    return C.xl_save(wb, "06_Compliance", "01_Clause_by_Clause_Compliance_Crosswalk.xlsx")


# ===========================================================================
#  FILE 4 — Closing and Implementation Plan (xlsx)
# ===========================================================================
def build_closing_plan():
    wb = Workbook()
    C.xl_instructions(wb, [
        "## Closing and Implementation Plan",
        "This workbook tracks every open item to closing, with an accountable owner, due date, "
        "dependency, and status.",
        "",
        "## How to use",
        "• Filter the header row to focus on OPEN or BLOCKED items or a single owner.",
        "• Due dates are placeholders until the closing calendar is fixed.",
        "• Status values: OPEN, IN PROGRESS, BLOCKED, COMPLETE, N/A.",
        "",
        "## Reliance limits",
        "• PRELIMINARY: no controlling award or source documents supplied.",
        "• Confirming the controlling round/award is the gating item for most others.",
    ], title="Closing Plan")

    ws = wb.create_sheet("Plan")
    ws.sheet_properties.tabColor = "1F3864"
    C.xl_title(ws, "Closing and Implementation Plan",
               subtitle="Lumbee Tribe / RIVR Tech TBCP fiber package — " + C.DRAFT_VERSION, span=6)

    headers = ["#", "Open Item", "Accountable Owner", "Due Date", "Dependency", "Status"]
    hdr_row = 5
    C.xl_header_row(ws, hdr_row, headers, freeze=True, filt=True)

    items = [
        ["Confirm controlling TBCP round and executed award", "Tribe (grant lead) + Grant Counsel",
         "Predecessor to nearly all definitive terms"],
        ["Obtain Lumbee federal-recognition / eligibility opinion", "Tribal Counsel",
         "Confirm controlling round/award"],
        ["Assemble procurement record supporting DEPC pricing", "RIVR Tech + Tribe (grant lead)",
         "Controlling award; procurement standards (200.317-.327)"],
        ["Make contractor vs. subrecipient determination", "Grant Counsel + Tribe",
         "Award terms; 2 CFR 200.331 factors"],
        ["Complete NEPA / NHPA §106 environmental & historic review",
         "Environmental Consultant + Tribe (THPO/SHPO)", "Route/scope (S2/S9); award"],
        ["Secure land / ROW and BIA approvals where applicable", "Tribal Counsel + Real Estate",
         "Facility inventory (S9); NHPA clearance"],
        ["Obtain LREMC board consent / joinder for LREMC Facilities", "LREMC + Tribe + RIVR Tech",
         "Facility inventory (S9)"],
        ["Adopt limited sovereign-immunity waiver action", "Tribal Council + Tribal Counsel",
         "Waiver scope approved (G4)"],
        ["Bind required insurance coverages", "RIVR Tech (risk) + Broker",
         "Insurance schedule (S12) finalized"],
        ["Set per-Active-Subscriber amount and confirm characterization",
         "Tribe + RIVR Tech (business) + Grant Counsel", "Program-income determination (200.307)"],
        ["Obtain NTIA/DOC written determinations (award, precedence, program income)",
         "Tribe (grant lead) + Grant Counsel", "Award confirmed; questions framed to NTIA"],
        ["Issue segment Notice to Proceed (NTP)", "Tribe (with RIVR Tech)",
         "Environmental clearance; permits; approvals complete"],
        ["Achieve segment acceptance (starts term clock)", "RIVR Tech + Tribe (acceptance)",
         "NTP; acceptance testing per S4"],
        ["Begin subscriber activation / provider-of-record operations", "RIVR Tech",
         "Segment acceptance; retail readiness (S7)"],
    ]

    r = hdr_row + 1
    first = r
    for i, it in enumerate(items, start=1):
        C.xl_cell(ws, r, 1, i, kind="text", align="center")
        C.xl_cell(ws, r, 2, it[0], kind="text", wrap=True, align="left")
        C.xl_cell(ws, r, 3, it[1], kind="input", wrap=True, align="left")
        C.xl_cell(ws, r, 4, C.PH("date"), kind="input", align="center")
        C.xl_cell(ws, r, 5, it[2], kind="text", wrap=True, align="left")
        C.xl_cell(ws, r, 6, "OPEN", kind="input", align="center")
        r += 1
    last = r - 1

    for col, w in zip("ABCDEF", [5, 46, 34, 16, 40, 14]):
        ws.column_dimensions[col].width = w

    # Status data validation
    dv_status = DataValidation(type="list",
                               formula1='"OPEN,IN PROGRESS,BLOCKED,COMPLETE,N/A"',
                               allow_blank=True)
    ws.add_data_validation(dv_status)
    dv_status.add(f"F{first}:F{last}")

    return C.xl_save(wb, "06_Compliance", "02_Closing_and_Implementation_Plan.xlsx")


# ===========================================================================
#  MAIN
# ===========================================================================
if __name__ == "__main__":
    paths = []
    paths.append(build_executive_summary())
    paths.append(build_agreement_register())
    paths.append(build_compliance_crosswalk())
    paths.append(build_closing_plan())
    print("GENERATED:")
    for p in paths:
        print("  ", p)
