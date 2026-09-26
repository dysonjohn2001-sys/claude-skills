"""
common.py — Canonical constants and formatting engine for the
Lumbee Tribe of North Carolina / RIVR Tech broadband IRU transaction package.

SINGLE SOURCE OF TRUTH. Every document-generation script imports this module so
that party names, defined terms, IRU term options, placeholders, flag markers,
citations, and formatting stay consistent across the entire package.

Status of every generated document:
    "DRAFT FOR DISCUSSION – SUBJECT TO LEGAL, GRANT AND FINANCIAL REVIEW"

These are working drafts, not final legal advice.
"""

from __future__ import annotations

import datetime
import os

from docx import Document
from docx.shared import Pt, Inches, RGBColor, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ---------------------------------------------------------------------------
# 0.  PATHS
# ---------------------------------------------------------------------------
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PKG_DIR = os.path.dirname(SCRIPTS_DIR)          # Lumbee_RIVR_Tech_IRU_Package/


def out(*parts) -> str:
    """Absolute path inside the package."""
    return os.path.join(PKG_DIR, *parts)


# ---------------------------------------------------------------------------
# 1.  CANONICAL CONSTANTS  (defined terms must match verbatim across documents)
# ---------------------------------------------------------------------------
VERSION_DATE = "September 26, 2026"
DRAFT_STATUS = ("PRELIMINARY DRAFT – NO CONTROLLING TBCP AWARD OR SOURCE DOCUMENTS SUPPLIED – "
                "PROVISIONAL BASELINE: MARCH 2024 AMENDED ROUND 2 NOFO – SUBJECT TO LEGAL, GRANT AND FINANCIAL REVIEW")
DRAFT_STATUS_SHORT = "PRELIMINARY DRAFT – SUBJECT TO LEGAL, GRANT AND FINANCIAL REVIEW"
DRAFT_VERSION = "Preliminary Draft v0.1"
CONFIDENTIAL = "CONFIDENTIAL – ATTORNEY WORK PRODUCT / SUBJECT TO COMMON-INTEREST PRIVILEGE"

# Parties -------------------------------------------------------------------
TRIBE_FULL = "Lumbee Tribe of North Carolina"
TRIBE_SHORT = "Lumbee Tribe"       # defined short-form term for the Tribal party
TRIBE_ENTITY_ALT = "a wholly owned Tribal entity or Tribally chartered instrumentality designated by the Lumbee Tribe"
TRIBE_DEFINED = '"Lumbee Tribe"'   # how it is introduced parenthetically

OPERATOR_FULL = "LREMC Technologies, LLC d/b/a RIVR Tech"
OPERATOR_SHORT = "RIVR Tech"
OPERATOR_DEFINED = '"RIVR Tech"'

# LREMC — the affiliate that OWNS poles/fiber/easements/huts/power/land/facilities.
# Distinct from RIVR Tech (LREMC Technologies, LLC). Assets covered ONLY by a
# separate owner-approved agreement or joinder — never assumed owned by RIVR Tech.
LREMC_FULL = "Lumbee River Electric Membership Corporation d/b/a Lumbee River EMC"
LREMC_SHORT = "LREMC"
LREMC_DEFINED = '"LREMC"'

PARTIES_COLLECTIVE = "Parties"
PARTY_SINGULAR = "Party"

# Program / agency ----------------------------------------------------------
PROGRAM_FULL = "Tribal Broadband Connectivity Program"
PROGRAM_SHORT = "TBCP"
AGENCY_FULL = "National Telecommunications and Information Administration"
AGENCY_SHORT = "NTIA"
DOC_FULL = "U.S. Department of Commerce"
# PROVISIONAL baseline is Round 2 (March 2024 amendment) per the assignment,
# because no controlling round/award was supplied. Round 3 is the live round as
# of the version date and MUST be confirmed before finalizing.
NOFO_NAME = "TBCP Round 2 Notice of Funding Opportunity, as amended March 2024 (PROVISIONAL BASELINE)"
NOFO_SHORT = "NOFO"
NOFO_LIVE_NOTE = ("Round 3 is the live TBCP round as of the version date; the controlling round and "
                  "executed award must be confirmed before any definitive clause is finalized.")

# Network / asset defined terms --------------------------------------------
NETWORK = "Tribal Network"          # the grant-funded network owned by the Lumbee Tribe
TRIBAL_ASSETS = "Grant-Funded Assets"   # grant-funded infrastructure owned by the Lumbee Tribe
GRANT_FUNDED = "Grant-Funded Assets"
OPERATOR_ASSETS = "RIVR Tech Assets"           # RIVR Tech pre-existing network/systems
OPERATOR_EXISTING = "RIVR Tech Existing Network"   # existing fiber/core/transport/NOC/billing
LREMC_ASSETS = "LREMC Facilities"              # LREMC-owned poles/conduit/fiber/easements/huts/power/land
JOINT_ASSETS = "Jointly Funded Assets"
DEMARCATION = "Demarcation Point"
IRU_TERM_DEFINED = "IRU"
FEDERAL_INTEREST = "Federal Interest"
PROGRAM_INCOME = "Program Income"
SERVICE_TERRITORY = "Approved Project Area"
ACTIVE_SUBSCRIBER = "Active Subscriber"
POI = "Point of Interconnection"

# Term (this package) — 20 years from segment acceptance + two 5-yr renewals ---
IRU_TERMS_YEARS = [20]
IRU_TERM_RECOMMENDED = 20
IRU_RENEWAL_DEFAULT = "two (2) optional renewal terms of five (5) years each"
TERM_TRIGGER = "acceptance of each Network segment"

# Geography -----------------------------------------------------------------
GEOGRAPHY = "southeastern North Carolina"
STATE = "North Carolina"

# Speed / service floors (from TBCP guidance) ------------------------------
SPEED_FLOOR = "100/20 Mbps"

# ---------------------------------------------------------------------------
# 2.  FLAG MARKERS  (rendered bold + colored; some also highlighted)
# ---------------------------------------------------------------------------
FLAG_BUSINESS = "[BUSINESS DECISION REQUIRED]"
FLAG_ATTORNEY = "[ATTORNEY REVIEW REQUIRED]"
FLAG_GRANT = "[GRANT COMPLIANCE REVIEW REQUIRED]"
FLAG_TECH = "[TECHNICAL INFORMATION REQUIRED]"
ALL_FLAGS = [FLAG_BUSINESS, FLAG_ATTORNEY, FLAG_GRANT, FLAG_TECH]

FLAG_COLORS = {
    FLAG_BUSINESS: RGBColor(0xC0, 0x00, 0x00),   # dark red
    FLAG_ATTORNEY: RGBColor(0x00, 0x00, 0xC0),   # blue
    FLAG_GRANT:    RGBColor(0x7F, 0x00, 0x7F),   # purple
    FLAG_TECH:     RGBColor(0x00, 0x70, 0x00),   # green
}

# Placeholder helper: caller wraps a description; always highlighted yellow.
def PH(desc: str) -> str:
    return f"[■ {desc}]"


# ---------------------------------------------------------------------------
# 3.  AUTHORITATIVE CITATIONS  (kept in one place; used across compliance docs)
# ---------------------------------------------------------------------------
CITES = {
    "ug_part": "2 CFR Part 200 (Uniform Administrative Requirements, Cost Principles, and Audit Requirements for Federal Awards)",
    "ug_2024": "2 CFR Part 200, as revised effective October 1, 2024 (equipment/supplies and disposition threshold $10,000; single-audit threshold $1,000,000)",
    "real_property": "2 CFR 200.311 (Real property — use, encumbrance, and disposition)",
    "fed_owned": "2 CFR 200.312 (Federally-owned and exempt property)",
    "equipment": "2 CFR 200.313 (Equipment — use, management, and disposition)",
    "supplies": "2 CFR 200.314 (Supplies)",
    "intangible": "2 CFR 200.315 (Intangible property)",
    "trust": "2 CFR 200.316 (Property trust relationship)",
    "insurance": "2 CFR 200.310 (Insurance coverage)",
    "prog_income": "2 CFR 200.307 (Program income)",
    "procurement": "2 CFR 200.317–200.327 (Procurement standards)",
    "competition": "2 CFR 200.319 (Competition)",
    "methods": "2 CFR 200.320 (Methods of procurement)",
    "domestic": "2 CFR 200.322 (Domestic preferences for procurements)",
    "conflict": "2 CFR 200.318(c) and 2 CFR 200.112 (Conflict of interest)",
    "subrecipient": "2 CFR 200.331 (Subrecipient and contractor determinations)",
    "pass_through": "2 CFR 200.332 (Requirements for pass-through entities)",
    "records": "2 CFR 200.334–200.337 (Record retention and access; three-year retention)",
    "single_audit": "2 CFR Part 200, Subpart F (Audit Requirements; single-audit threshold $1,000,000)",
    "allowable": "2 CFR Part 200, Subpart E (Cost Principles — allowability, allocability, reasonableness)",
    "closeout": "2 CFR 200.344 (Closeout) and 2 CFR 200.345 (Post-closeout adjustments and continuing responsibilities)",
    "remedies": "2 CFR 200.339–200.343 (Remedies for noncompliance; termination)",
    "disclosures": "2 CFR 200.113 (Mandatory disclosures)",
    "debarment": "2 CFR Part 180 and 2 CFR Part 1327 (Governmentwide debarment and suspension — DOC/NTIA adoption)",
    "telecom_ban": "2 CFR 200.216 (Prohibition on certain telecommunications and video surveillance — §889 covered equipment)",
    "baba": "Build America, Buy America Act, IIJA §§ 70911–70917 (Pub. L. 117-58); 2 CFR Part 184; and NTIA BABA award terms",
    "nepa": "National Environmental Policy Act (NEPA), 42 U.S.C. § 4321 et seq., and DOC/NTIA implementing procedures",
    "nhpa": "National Historic Preservation Act § 106, 54 U.S.C. § 306108 (36 CFR Part 800)",
    "iija": "Infrastructure Investment and Jobs Act, Pub. L. 117-58 (2021), and Consolidated Appropriations Act, 2021, Pub. L. 116-260",
    "nofo": "TBCP Round 2 Notice of Funding Opportunity, as amended March 2024 (PROVISIONAL BASELINE — "
        "controlling round/award NOT supplied; confirm before finalizing)",
    "id_guidance": "TBCP Infrastructure Deployment Application Guidance (NTIA) — confirm the version "
        "matching the controlling award",
    "sac": "NTIA Standard Terms and Conditions, DOC Financial Assistance Standard Terms and Conditions, "
        "and the award's Specific Award Conditions (NOT supplied)",
    "usac_lifeline": "47 CFR Part 54 (USAC/FCC universal service, Lifeline, and ETC requirements)",
    "cpni": "47 U.S.C. § 222 and 47 CFR §§ 64.2001–64.2011 (Customer Proprietary Network Information)",
    "lumbee_act": "Lumbee Act of 1956, Pub. L. 84-570, 70 Stat. 254 (federal-recognition status affecting TBCP eligibility)",
    "indian_leasing": "25 CFR Part 162 (leases of Indian land) — where trust/restricted land is used",
    "indian_row": "25 CFR Part 169 (rights-of-way over Indian land) — where trust/restricted land is crossed",
    "bia_approval": "25 U.S.C. §§ 415, 81 and 25 CFR Parts 162/169 (BIA approval of certain leases/ROW/contracts on Indian land)",
    "sovereign_immunity": "Santa Clara Pueblo v. Martinez, 436 U.S. 49 (1978); C&L Enterprises v. Citizen Band Potawatomi, 532 U.S. 411 (2001); Michigan v. Bay Mills, 572 U.S. 782 (2014) (tribal sovereign immunity; clear express waiver required)",
    "tero": "Applicable Tribal Employment Rights Ordinance (TERO) and Tribal preference requirements [COUNSEL TO CONFIRM applicability to the Lumbee Tribe]",
    "nc_dig": "N.C. Gen. Stat. Ch. 87, Art. 8A (Underground Utility Safety and Damage Prevention Act / 811 locates)",
    "nc_pole": "N.C. Gen. Stat. § 62-350 (broadband attachment to utility poles)",
    "nc_ncdot": "N.C. Gen. Stat. § 136-18 and NCDOT utility accommodation policy (encroachment/ROW in NCDOT corridors)",
    "oci": "2 CFR 200.318(c)(1)-(2) (organizational conflict of interest and written standards of conduct)",

}


# ---------------------------------------------------------------------------
# 3b. CANONICAL DEAL MECHANICS  (must be identical across every document)
#     These are default/placeholder positions for negotiation, not final terms.
# ---------------------------------------------------------------------------
DEAL = {
    # Legal mechanics -------------------------------------------------------
    "cure_monetary_days": 30,
    "cure_nonmonetary_days": 60,
    "cure_nonmonetary_extension": "an additional sixty (60) days if the breach is not "
        "reasonably curable within the initial period and the defaulting Party is "
        "diligently pursuing cure",
    "notice_default_days": 30,
    "stepin_emergency": "immediate, upon notice, where continuity of Essential Services, "
        "public safety, or compliance with the Award is imminently threatened",
    "transition_assistance_months": 12,
    "records_retention_years": 3,      # 2 CFR 200.334 (measured from final report)
    "audit_notice_business_days": 10,
    # Term (this package) — 20 yrs from segment acceptance + two 5-yr renewals -
    "iru_terms": [20],
    "iru_term_recommended": 20,
    "iru_renewal": "two (2) optional renewal terms of five (5) years each",
    "term_trigger": "acceptance of each Network segment",
    "term_ceiling_note": "the useful life of the Grant-Funded Assets, the duration of the "
        "underlying land/access rights, the Federal Interest period, and the controlling Award",
    "iru_prepaid_consideration": "one dollar ($1.00) and other good and valuable "
        "consideration, plus the operating, maintenance, and payment obligations set forth herein",
    # PRIMARY economic model: per-Active-Subscriber payment ------------------
    "per_subscriber_amount": "$[X] per Active Subscriber per month",
    "active_subscriber_elements": [
        "counted only for a location within the Approved Project Area receiving "
            "provisioned, billable retail broadband service",
        "activation dated to first successful service provisioning; disconnect dated to service cease",
        "partial months prorated on a daily basis [BUSINESS DECISION REQUIRED: prorate vs. full-month]",
        "excludes accounts suspended for nonpayment beyond [30] days, and courtesy/free/subsidized "
            "accounts unless separately agreed and Award-permitted",
        "one location with multiple services counts as a single Active Subscriber unless separately agreed",
        "bulk / multi-dwelling accounts counted per billable unit per an agreed methodology",
        "net of credits, refunds, and uncollectible amounts; exclusive of taxes and regulatory fees",
    ],
    # Payment CHARACTERIZATION alternatives (label does not control program income)
    "pay_options": {
        "A": "Option A — Asset-Use / License Consideration for the IRU and operating rights",
        "B": "Option B — IRU Consideration (prepaid or periodic) for defined capacity",
        "C": "Option C — Operating Revenue Share (percentage of defined retail revenue)",
        "D": "Option D — Per-Active-Subscriber Operating Payment (primary model in this package)",
        "E": "Option E — Hybrid (base asset-use fee plus per-subscriber component)",
    },
    "pay_recommended": "D",
    "program_income_note": "characterization is provisional; program-income treatment under "
        "2 CFR 200.307 turns on the controlling Award and written NTIA determination, not the label",
    # Retained legacy revenue-share labels (financial illustration only) -----
    "rev_options": {
        "A": "Option A — Fixed Annual Asset-Use Payment",
        "B": "Option B — Percentage of Gross Retail Revenue",
        "C": "Option C — Percentage of Adjusted Operating Cash Flow",
        "D": "Option D — Per-Active-Subscriber Payment (primary)",
        "E": "Option E — Hybrid (Fixed Base plus Per-Subscriber)",
    },
    "rev_recommended": "D",
    # Placeholder economics (clearly marked inputs) -------------------------
    "ph_award_amount": "$[X] (award amount — NOT SUPPLIED; do not invent)",
    "ph_homes_passed": "[X] (locations — per approved application; NOT SUPPLIED)",
    "ph_per_sub": "$[X] per Active Subscriber per month",
    "ph_res_arpu": "$[X]",
    "ph_bus_arpu": "$[X]",
    "rev_share_pct_placeholder": "[X]%",
    "cashflow_share_pct_placeholder": "[X]%",
    # SLA severity targets (canonical — must match O&M/SLA and exhibits) ----
    "sla": {
        "P1_response_min": 15, "P1_dispatch_hr": 2, "P1_restore_hr": 8,
        "P2_response_min": 30, "P2_dispatch_hr": 4, "P2_restore_hr": 24,
        "P3_response_hr": 4,   "P3_dispatch_hr": 24, "P3_restore_days": 5,
        "P4_response_hr": 8,   "P4_restore_days": 30,
        "availability_target": "99.9%",
        "latency_ms": 100, "packet_loss": "0.1%", "jitter_ms": 30,
        "noc": "24 hours per day, 7 days per week, 365 days per year",
    },
    # Insurance limits (canonical — Exhibit I and every agreement) ----------
    "insurance": {
        "cgl_occurrence": "$2,000,000",
        "cgl_aggregate": "$4,000,000",
        "auto": "$1,000,000",
        "umbrella": "$10,000,000",
        "workers_comp": "statutory limits",
        "employers_liability": "$1,000,000",
        "professional_tech_eo": "$5,000,000",
        "cyber": "$5,000,000",
        "property_builders_risk": "full replacement cost of the Tribal Assets",
        "pollution": "$1,000,000",
    },
}

# ---------------------------------------------------------------------------
# 3c. ORDER OF PRECEDENCE + AGREEMENT REGISTER (verbatim across every document)
# ---------------------------------------------------------------------------
PRECEDENCE = [
    "the executed federal Award and all requirements incorporated into it (including the "
        "controlling NOFO, the Specific Award Conditions, the approved application, budget, "
        "routes, and service commitments, and any later written NTIA/DOC determination)",
    "applicable federal statutes and regulations, including 2 CFR Part 200 and NTIA/DOC award terms",
    "the approved project documents",
    "the Master TBCP Partnership and Implementation Agreement",
    "the other Definitive Agreements",
    "the Schedules, Exhibits, Certificates, and Operational Forms",
]
PRECEDENCE_RULE = ("No commercial agreement, schedule, or form authorizes any act prohibited by, or "
    "inconsistent with, the Award or applicable federal law; in any conflict the higher-ranked "
    "instrument controls, and a lawful construction and service provision is not invalidated by a "
    "rejected IRU, exclusivity, payment, or commercial-use term (severability and reformation apply).")
SHARED_DEFINITIONS_RULE = ("Capitalized terms used and not otherwise defined in a document have the "
    "meanings given in Article 2 (Definitions) of the Master TBCP Partnership and Implementation "
    "Agreement, which is the single shared definitions source for the package.")

# Canonical document names (for cross-references — use verbatim) --------------
AGREEMENTS = {
    "master": "Master TBCP Partnership and Implementation Agreement",
    "depc": "Design, Engineering, Procurement, and Construction Agreement",
    "iru": "Indefeasible Right of Use and Network Access Agreement",
    "interconnect": "Network Interconnection, Transport, Equipment, and Shared Facilities Agreement",
    "om": "Network Operations, Maintenance, and Lifecycle Agreement",
    "retail": "Retail Customer Service, Billing, Collections, and Subscriber Revenue Agreement",
    "finance": "Grant Finance, Reimbursement, Program Income, and Audit Agreement",
    "land": "Land, Easement, Right-of-Way, Pole, Site, Power, and Facility Instruments",
    "privacy": "Data Privacy, Cybersecurity, Supply-Chain Risk, and Business Continuity Addendum",
    "transition": "Continuity, Step-In, Termination Assistance, and Transition Agreement",
}
SCHEDULES = {
    "S1": "Award, Authority, Resolutions, Signatories, and Document Precedence",
    "S2": "Approved Project Scope, Eligible Locations, Routes, Milestones, and Service Commitments",
    "S3": "Asset Ownership, Funding Source, Federal Interest, and IRU/Network-Rights Register",
    "S4": "Engineering Standards, Bill of Materials, Equipment, Interconnection, and Demarcation",
    "S5": "Construction Pricing, Payment Milestones, Retainage, and Warranties",
    "S6": "Operations, Service Levels, Lifecycle, Spares, Refresh, and Reserves",
    "S7": "Provider-of-Record, Customer Products, Affordability, Support, Billing, and Complaints",
    "S8": "Subscriber Payment, Revenue, Program Income, Taxes, Fees, Cash Controls, and Audit",
    "S9": "Land, Poles, Sites, Power, Permits, Shared Facilities, and Owner Consents",
    "S10": "Approved Commercial Capacity, Non-Project Use, Non-Tribal Customers, Valuation, and Cost Allocation",
    "S11": "Data, Privacy, Cybersecurity, Supply-Chain Risk, Incident Response, and Disaster Recovery",
    "S12": "Insurance, Indemnity, Liability Allocation, and Claims Procedures",
    "S13": "Default, Cure, Step-In, Continuity, Transition, and Termination Assistance",
    "S14": "Required Federal, Tribal, Corporate, Landowner, Lender, and Regulatory Approvals",
}


# Optical acceptance-testing standards (Exhibit E + IRU acceptance) ----------
OPTICAL = {
    "wavelengths": "1310 nm and 1550 nm",
    "otdr": "bi-directional OTDR",
    "splice_loss_max": "0.10 dB (average) / 0.30 dB (maximum) per fusion splice",
    "connector_loss_max": "0.50 dB per mated connector pair",
    "span_margin": "consistent with the span-loss budget calculated at "
        "0.35 dB/km at 1310 nm and 0.25 dB/km at 1550 nm, plus splice and connector losses",
    "reflectance_max": "-40 dB (UPC) / -55 dB (APC)",
}


# ---------------------------------------------------------------------------
# 4.  COLORS / STYLE CONSTANTS
# ---------------------------------------------------------------------------
NAVY = RGBColor(0x1F, 0x38, 0x64)
GREY = RGBColor(0x59, 0x59, 0x59)
RED = RGBColor(0xC0, 0x00, 0x00)
BLACK = RGBColor(0x00, 0x00, 0x00)
BASE_FONT = "Calibri"
HEAD_FONT = "Calibri"

# Excel palette (ARGB hex strings for openpyxl)
XL_INPUT = "FFF2CC"       # light amber  -> input cells
XL_FORMULA = "DDEBF7"     # light blue   -> formula cells
XL_OUTPUT = "E2EFDA"      # light green  -> output/result cells
XL_HEADER = "1F3864"      # navy header
XL_HEADER_TXT = "FFFFFF"
XL_CHECK_OK = "C6EFCE"
XL_CHECK_BAD = "FFC7CE"
XL_SECTION = "D9E1F2"


# ===========================================================================
#  WORD (.docx) ENGINE
# ===========================================================================
def _set_cell_bg(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)


def _field(paragraph, instr):
    """Insert a Word field (e.g. PAGE, NUMPAGES, TOC) into a paragraph run."""
    run = paragraph.add_run()
    fldBegin = OxmlElement("w:fldChar")
    fldBegin.set(qn("w:fldCharType"), "begin")
    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = instr
    fldSep = OxmlElement("w:fldChar")
    fldSep.set(qn("w:fldCharType"), "separate")
    fldEnd = OxmlElement("w:fldChar")
    fldEnd.set(qn("w:fldCharType"), "end")
    r = run._r
    r.append(fldBegin)
    r.append(instrText)
    r.append(fldSep)
    r.append(fldEnd)
    return run


def new_doc():
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = BASE_FONT
    style.font.size = Pt(11)
    style.paragraph_format.space_after = Pt(6)
    style.paragraph_format.line_spacing = 1.08
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
    return doc


def add_cover(doc, doc_number, title, subtitle=None):
    """Professional cover page with status banner, parties, version, confidentiality."""
    # Status banner
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(DRAFT_STATUS)
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = RED
    _highlight_run(r, "yellow")

    for _ in range(3):
        doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(doc_number)
    r.font.size = Pt(12)
    r.font.color.rgb = GREY
    r.bold = True

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(title)
    r.bold = True
    r.font.size = Pt(24)
    r.font.color.rgb = NAVY

    if subtitle:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(subtitle)
        r.font.size = Pt(14)
        r.font.color.rgb = GREY

    for _ in range(2):
        doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("by and between")
    r.italic = True
    r.font.size = Pt(11)

    for name in (TRIBE_FULL, "and", OPERATOR_FULL):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(name)
        r.bold = name != "and"
        r.italic = name == "and"
        r.font.size = Pt(14 if name != "and" else 11)
        if name != "and":
            r.font.color.rgb = NAVY

    for _ in range(4):
        doc.add_paragraph()

    # Metadata block
    for label, val in [
        ("Version", DRAFT_VERSION),
        ("Version Date", VERSION_DATE),
        ("Document Status", "Working draft — not executed; not final legal advice"),
        ("Program", f"{PROGRAM_FULL} ({PROGRAM_SHORT}), {AGENCY_FULL} ({AGENCY_SHORT})"),
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(f"{label}:  ")
        r.bold = True
        r.font.size = Pt(10)
        r2 = p.add_run(val)
        r2.font.size = Pt(10)

    for _ in range(2):
        doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(CONFIDENTIAL)
    r.italic = True
    r.font.size = Pt(9)
    r.font.color.rgb = GREY

    doc.add_page_break()


def add_toc(doc, note_short=True):
    """Insert an auto-updating Table of Contents field (Word populates on open)."""
    h = doc.add_paragraph()
    r = h.add_run("TABLE OF CONTENTS")
    r.bold = True
    r.font.size = Pt(14)
    r.font.color.rgb = NAVY
    note = doc.add_paragraph()
    nr = note.add_run("(Right-click and choose “Update Field” in Microsoft Word to populate page numbers.)")
    nr.italic = True
    nr.font.size = Pt(9)
    nr.font.color.rgb = GREY
    p = doc.add_paragraph()
    _field(p, r'TOC \o "1-3" \h \z \u')
    doc.add_page_break()


def setup_header_footer(doc, short_title):
    """Header: short title + status. Footer: confidentiality | Page X of Y | version."""
    section = doc.sections[0]
    section.different_first_page_header_footer = True

    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.text = ""
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = hp.add_run(f"{short_title}  —  {DRAFT_STATUS_SHORT}")
    r.font.size = Pt(8)
    r.font.color.rgb = GREY
    r.italic = True

    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.text = ""
    # tab stops: left / center / right
    from docx.shared import Inches as _In
    fp.paragraph_format.tab_stops.add_tab_stop(_In(3.25), WD_TAB_ALIGNMENT.CENTER)
    fp.paragraph_format.tab_stops.add_tab_stop(_In(6.5), WD_TAB_ALIGNMENT.RIGHT)
    lr = fp.add_run(f"{DRAFT_VERSION} | {VERSION_DATE}")
    lr.font.size = Pt(8)
    lr.font.color.rgb = GREY
    fp.add_run("\t")
    _field(fp, "PAGE")
    mid = fp.add_run(" of ")
    _field(fp, "NUMPAGES")
    for rr in fp.runs:
        rr.font.size = Pt(8)
        rr.font.color.rgb = GREY
    fp.add_run("\t")
    rr = fp.add_run("Confidential — Draft")
    rr.font.size = Pt(8)
    rr.font.color.rgb = GREY


def _highlight_run(run, color="yellow"):
    from docx.enum.text import WD_COLOR_INDEX
    mapping = {"yellow": WD_COLOR_INDEX.YELLOW}
    run.font.highlight_color = mapping.get(color, WD_COLOR_INDEX.YELLOW)


def title_line(doc, text, size=16):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(size)
    r.font.color.rgb = NAVY
    return p


def status_banner(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(DRAFT_STATUS)
    r.bold = True
    r.font.color.rgb = RED
    _highlight_run(r)
    return p


def article(doc, number, text):
    """ARTICLE heading (H1 -> picked up by TOC)."""
    p = doc.add_heading(level=1)
    run = p.add_run(f"ARTICLE {number}.  {text.upper()}")
    run.bold = True
    run.font.size = Pt(13)
    run.font.color.rgb = NAVY
    run.font.name = HEAD_FONT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    return p


def section(doc, number, heading, body=None):
    """Numbered Section heading (H2). Optionally add body text."""
    p = doc.add_heading(level=2)
    run = p.add_run(f"{number}  {heading}")
    run.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = BLACK
    run.font.name = HEAD_FONT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    if body:
        para(doc, body)
    return p


def subsection(doc, label, body):
    """Lettered/numbered sub-provision, e.g. (a) ..."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.35)
    r = p.add_run(f"({label})  ")
    r.bold = True
    _emit_runs(p, body)
    return p


def para(doc, text, indent=0.0, italic=False, bold=False):
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.left_indent = Inches(indent)
    _emit_runs(p, text, italic=italic, bold=bold)
    return p


def bullet(doc, text, level=0):
    p = doc.add_paragraph(style="List Bullet")
    if level:
        p.paragraph_format.left_indent = Inches(0.5 + 0.25 * level)
    _emit_runs(p, text)
    return p


def numbered(doc, text):
    p = doc.add_paragraph(style="List Number")
    _emit_runs(p, text)
    return p


def _emit_runs(paragraph, text, italic=False, bold=False):
    """
    Emit text, auto-styling flag markers (colored/bold) and placeholders
    (highlighted yellow). Placeholders use the pattern [■ ...]. Flags use the
    ALL_FLAGS literals. Splitting keeps everything in one paragraph.
    """
    import re
    tokens = []
    pattern = re.compile(r"(\[■[^\]]*\]|" + "|".join(re.escape(f) for f in ALL_FLAGS) + r")")
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            tokens.append(("text", text[pos:m.start()]))
        tok = m.group(1)
        if tok in FLAG_COLORS:
            tokens.append(("flag", tok))
        else:
            tokens.append(("ph", tok))
        pos = m.end()
    if pos < len(text):
        tokens.append(("text", text[pos:]))
    if not tokens:
        tokens = [("text", text)]
    for kind, val in tokens:
        r = paragraph.add_run(val)
        r.italic = italic
        r.bold = bold
        if kind == "flag":
            r.bold = True
            r.font.color.rgb = FLAG_COLORS[val]
        elif kind == "ph":
            _highlight_run(r)
            r.font.color.rgb = RGBColor(0x80, 0x40, 0x00)


def flag_para(doc, marker, text, indent=0.35):
    """A standalone flagged note paragraph."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(indent)
    r = p.add_run(marker + "  ")
    r.bold = True
    r.font.color.rgb = FLAG_COLORS[marker]
    r2 = p.add_run(text)
    r2.italic = True
    r2.font.color.rgb = GREY
    return p


def spacer(doc, n=1):
    for _ in range(n):
        doc.add_paragraph()


def add_table(doc, headers, rows, widths=None, header_fill=XL_HEADER, font_size=9,
              col_align=None):
    """Styled table with navy header row, banded body, optional column widths (inches)."""
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        _set_cell_bg(hdr[i], header_fill)
        cell_p = hdr[i].paragraphs[0]
        cell_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = cell_p.add_run(str(h))
        r.bold = True
        r.font.size = Pt(font_size)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        hdr[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    for ridx, row in enumerate(rows):
        cells = table.add_row().cells
        for i, val in enumerate(row):
            if ridx % 2 == 1:
                _set_cell_bg(cells[i], "F2F2F2")
            cp = cells[i].paragraphs[0]
            if col_align and col_align[i] == "c":
                cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            _emit_runs(cp, str(val))
            for rr in cp.runs:
                rr.font.size = Pt(font_size)
            cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    if widths:
        for i, w in enumerate(widths):
            for row in table.rows:
                row.cells[i].width = Inches(w)
    return table


def signature_block(doc, extra_note=None):
    """Standard two-party execution block with placeholder signatory lines."""
    spacer(doc, 1)
    p = doc.add_paragraph()
    r = p.add_run("IN WITNESS WHEREOF, the Parties have caused this instrument to be "
                  "executed by their duly authorized representatives as of the Effective Date.")
    r.italic = True
    spacer(doc, 1)

    blocks = [
        (TRIBE_FULL, [
            ("By:", "____________________________________"),
            ("Name:", PH("authorized Tribal signatory")),
            ("Title:", PH("e.g., Chairman, Lumbee Tribal Council / Tribal Administrator")),
            ("Date:", "____________________________________"),
        ]),
        (OPERATOR_FULL, [
            ("By:", "____________________________________"),
            ("Name:", PH("authorized RIVR Tech signatory")),
            ("Title:", PH("e.g., Chief Executive Officer / Manager")),
            ("Date:", "____________________________________"),
        ]),
    ]
    for party, lines in blocks:
        p = doc.add_paragraph()
        r = p.add_run(party)
        r.bold = True
        r.font.color.rgb = NAVY
        for label, val in lines:
            lp = doc.add_paragraph()
            lp.paragraph_format.left_indent = Inches(0.25)
            lr = lp.add_run(f"{label}  ")
            lr.bold = True
            _emit_runs(lp, val)
        spacer(doc, 1)
    if extra_note:
        flag_para(doc, FLAG_ATTORNEY, extra_note)


def save(doc, *path_parts):
    path = out(*path_parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    doc.save(path)
    return path


# ===========================================================================
#  EXCEL (.xlsx) ENGINE
# ===========================================================================
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, NamedStyle
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

FMT_USD = '"$"#,##0;("$"#,##0)'
FMT_USD2 = '"$"#,##0.00;("$"#,##0.00)'
FMT_PCT = '0.0%'
FMT_PCT2 = '0.00%'
FMT_NUM = '#,##0'
FMT_MULT = '0.00"x"'

THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def xl_header_row(ws, row, headers, start_col=1, fill=XL_HEADER, freeze=True, filt=True):
    for i, h in enumerate(headers):
        c = ws.cell(row=row, column=start_col + i, value=h)
        c.font = Font(bold=True, color=XL_HEADER_TXT, size=10)
        c.fill = PatternFill("solid", fgColor=fill)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BORDER
    if freeze:
        ws.freeze_panes = ws.cell(row=row + 1, column=start_col)
    if filt:
        last = get_column_letter(start_col + len(headers) - 1)
        ws.auto_filter.ref = f"{get_column_letter(start_col)}{row}:{last}{row}"


def xl_cell(ws, row, col, value, kind="text", fmt=None, bold=False, wrap=False,
            align=None):
    """kind: input | formula | output | text | section."""
    c = ws.cell(row=row, column=col, value=value)
    fills = {"input": XL_INPUT, "formula": XL_FORMULA, "output": XL_OUTPUT,
             "section": XL_SECTION}
    if kind in fills:
        c.fill = PatternFill("solid", fgColor=fills[kind])
    if kind == "section":
        bold = True
    if fmt:
        c.number_format = fmt
    c.font = Font(bold=bold, size=10)
    c.border = BORDER
    if wrap or align:
        c.alignment = Alignment(wrap_text=wrap, horizontal=align or "general",
                                vertical="center")
    return c


def xl_title(ws, title, subtitle=None, span=8):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=span)
    c = ws.cell(row=1, column=1, value=title)
    c.font = Font(bold=True, size=14, color="1F3864")
    c.alignment = Alignment(horizontal="left", vertical="center")
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=span)
    c2 = ws.cell(row=2, column=1, value=DRAFT_STATUS)
    c2.font = Font(bold=True, italic=True, size=9, color="C00000")
    if subtitle:
        ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=span)
        c3 = ws.cell(row=3, column=1, value=subtitle)
        c3.font = Font(italic=True, size=9, color="595959")


def xl_legend(ws, row, col=1):
    """Colour legend so users know inputs vs formulas vs outputs."""
    items = [("INPUT (edit these)", XL_INPUT), ("FORMULA (do not edit)", XL_FORMULA),
             ("OUTPUT / RESULT", XL_OUTPUT)]
    c = ws.cell(row=row, column=col, value="Legend:")
    c.font = Font(bold=True, size=9)
    for i, (label, fill) in enumerate(items):
        cc = ws.cell(row=row, column=col + 1 + i, value=label)
        cc.fill = PatternFill("solid", fgColor=fill)
        cc.font = Font(size=9)
        cc.border = BORDER


def xl_check(ws, row, col, formula, label):
    """Formula-check cell that turns green PASS / red FAIL via conditional format."""
    lc = ws.cell(row=row, column=col, value=label)
    lc.font = Font(size=9, italic=True)
    cc = ws.cell(row=row, column=col + 1, value=formula)
    cc.font = Font(bold=True, size=9)
    cc.border = BORDER
    return cc


def xl_instructions(wb, lines, title="INSTRUCTIONS"):
    ws = wb.active if wb.active.title == "Sheet" else wb.create_sheet(title, 0)
    ws.title = "Instructions"
    ws.sheet_properties.tabColor = "1F3864"
    xl_title(ws, title, span=2)
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 110
    r = 5
    for ln in lines:
        c = ws.cell(row=r, column=2, value=ln)
        if ln.startswith("##"):
            c.value = ln[2:].strip()
            c.font = Font(bold=True, size=11, color="1F3864")
        elif ln.startswith("•"):
            c.font = Font(size=10)
        else:
            c.font = Font(size=10)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        r += 1
    xl_legend(ws, r + 1)
    return ws


def xl_save(wb, *path_parts):
    path = out(*path_parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wb.save(path)
    return path


# Convenience: standard recitals/definitions blocks reused by several agreements
def add_status_and_intro(doc, agreement_name, doc_number):
    status_banner(doc)
    spacer(doc, 1)
    p = doc.add_paragraph()
    r = p.add_run(
        f"This {agreement_name} (this “Agreement”) is entered into as of "
        f"{PH('Effective Date')} (the “Effective Date”), by and between "
        f"{TRIBE_FULL} (the “{TRIBE_SHORT}”)"
        f"{' or ' + TRIBE_ENTITY_ALT + ' [see Section on Tribal Party]' if False else ''}"
        f", and {OPERATOR_FULL} (“{OPERATOR_SHORT}”). The {TRIBE_SHORT} and {OPERATOR_SHORT} "
        f"are each a “Party” and together the “Parties.”"
    )
    return p


if __name__ == "__main__":
    # Self-test: emit a tiny doc + workbook to verify the engine loads.
    d = new_doc()
    add_cover(d, "SELF-TEST", "Engine Self-Test", "verifying common.py")
    setup_header_footer(d, "Self-Test")
    add_toc(d)
    article(d, 1, "Test Article")
    section(d, "1.1", "Test Section", f"This references the {PH('placeholder')} and {FLAG_ATTORNEY}.")
    add_table(d, ["A", "B"], [["1", "2"], ["3", "4"]])
    signature_block(d)
    p = save(d, "Scripts", "_selftest.docx")
    wb = Workbook()
    xl_instructions(wb, ["## Test", "• bullet one", "plain line"])
    ws = wb.create_sheet("Data")
    xl_title(ws, "Test Sheet")
    xl_header_row(ws, 5, ["Input", "Formula", "Output"])
    xl_cell(ws, 6, 1, 10, "input", FMT_USD)
    xl_cell(ws, 6, 2, "=A6*2", "formula", FMT_USD)
    xl_cell(ws, 6, 3, "=B6", "output", FMT_USD)
    xp = xl_save(wb, "Scripts", "_selftest.xlsx")
    print("OK ->", p, xp)
