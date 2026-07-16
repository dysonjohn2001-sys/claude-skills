"""
gen_master.py — Generator for Deliverable 2, Document 02.01:
MASTER DEVELOPMENT, CONSTRUCTION AND OPERATING AGREEMENT.

Largest document in the Lumbee Tribe of North Carolina / RIVR Tech broadband
IRU transaction package. Imports the canonical Scripts/common.py engine for all
party names, defined terms, deal mechanics, citations, placeholders, and flags.

Run:  python3 gen_master.py
Output: 02_Core_Agreements/01_Master_Development_Construction_and_Operating_Agreement.docx
"""

import sys
import os

sys.path.insert(0, "/home/user/claude-skills/Lumbee_RIVR_Tech_IRU_Package/Scripts")
import common as C


# ---------------------------------------------------------------------------
# Convenience wrappers so the body reads cleanly.
# ---------------------------------------------------------------------------
def S(doc, num, head, body=None):
    return C.section(doc, num, head, body)


def P(doc, text, **kw):
    return C.para(doc, text, **kw)


def SUB(doc, label, text):
    return C.subsection(doc, label, text)


def B(doc, text, level=0):
    return C.bullet(doc, text, level=level)


def FL(doc, marker, text):
    return C.flag_para(doc, marker, text)


def cite(key):
    return C.CITES[key]


# Frequently used term shortcuts (verbatim from common.py) ------------------
TR = C.TRIBE_SHORT
TRF = C.TRIBE_FULL
OP = C.OPERATOR_SHORT
OPF = C.OPERATOR_FULL
NET = C.NETWORK
TA = C.TRIBAL_ASSETS
OA = C.OPERATOR_ASSETS
OE = C.OPERATOR_EXISTING
JA = C.JOINT_ASSETS
DEM = C.DEMARCATION
GF = C.GRANT_FUNDED
FI = C.FEDERAL_INTEREST
PI = C.PROGRAM_INCOME
ST = C.SERVICE_TERRITORY
IRU = C.IRU_TERM_DEFINED
D = C.DEAL


def build():
    doc = C.new_doc()

    # -------------------------------------------------------------------
    # COVER / HEADER / TOC / STATUS
    # -------------------------------------------------------------------
    C.add_cover(
        doc,
        "DOCUMENT 02.01 — MASTER DEVELOPMENT, CONSTRUCTION AND OPERATING AGREEMENT",
        "Master Development, Construction and Operating Agreement",
        "The controlling commercial instrument for the Tribally owned, "
        "grant-funded broadband Network and its operation by RIVR Tech",
    )
    C.setup_header_footer(doc, "Master Agreement")
    C.add_toc(doc)
    C.status_banner(doc)

    # -------------------------------------------------------------------
    # PREAMBLE + RECITALS
    # -------------------------------------------------------------------
    C.spacer(doc, 1)
    P(
        doc,
        f"This MASTER DEVELOPMENT, CONSTRUCTION AND OPERATING AGREEMENT (this "
        f"“Agreement” or the “Master Agreement”) is made and entered into as "
        f"of {C.PH('Effective Date')} (the “Effective Date”), by and between "
        f"{TRF}, a federally ‐recognized-status Indian tribe organized under its own "
        f"governing documents (together with, where the context requires, "
        f"{C.TRIBE_ENTITY_ALT}, collectively the “{TR}”), and {OPF}, a limited "
        f"liability company (“{OP}”). The {TR} and {OP} are each referred to herein "
        f"as a “{C.PARTY_SINGULAR}” and together as the “{C.PARTIES_COLLECTIVE}.”",
    )
    FL(
        doc,
        C.FLAG_GRANT,
        f"The {TR}'s eligibility to hold and administer a {C.PROGRAM_SHORT} award turns on its "
        f"federal-recognition status under the {cite('lumbee_act')}. Grant counsel must confirm "
        f"the {TR}'s standing as an eligible entity and the correct contracting party (the {TR} "
        f"directly, or a designated Tribal entity or instrumentality) BEFORE execution. This "
        f"Agreement does not resolve that question.",
    )
    FL(
        doc,
        C.FLAG_ATTORNEY,
        "The precise legal name, organizational form, and signing authority of each Party, and "
        "whether a Tribal instrumentality is inserted as the contracting entity, must be verified "
        "against organizational documents and Tribal Council authorizing resolutions before "
        "execution.",
    )

    C.spacer(doc, 1)
    p = doc.add_paragraph()
    r = p.add_run("RECITALS")
    r.bold = True
    r.font.color.rgb = C.NAVY
    r.font.size = C.Pt(12)

    recitals = [
        (
            "A",
            f"WHEREAS, the {TR} intends to apply for, and if awarded to accept and administer, a "
            f"grant under the {C.PROGRAM_FULL} ({C.PROGRAM_SHORT}) administered by the "
            f"{C.AGENCY_FULL} ({C.AGENCY_SHORT}) pursuant to the {cite('nofo')} and the "
            f"{cite('iija')}, to fund the deployment of last-mile and related broadband "
            f"infrastructure serving unserved and underserved locations in {C.GEOGRAPHY} (the "
            f"“{ST}”);",
        ),
        (
            "B",
            f"WHEREAS, if the award is made, the {TR} will be the {C.PROGRAM_SHORT} grant "
            f"recipient and the legal owner of, and will hold and retain title to, all "
            f"grant-funded infrastructure and assets (the “{TA}”, also referred to as the "
            f"“{GF}”), which are and will remain subject to the continuing {FI} of the "
            f"United States under {cite('real_property')}, {cite('equipment')}, and "
            f"{cite('intangible')};",
        ),
        (
            "C",
            f"WHEREAS, {OP} is an experienced broadband developer and operator that owns and "
            f"operates existing middle-mile, backbone, and core network facilities in and around "
            f"the {ST} (the “{OE}”) and has the technical, operational, and financial "
            f"capacity to design, engineer, construct, activate, operate, and maintain the "
            f"grant-funded infrastructure and to provide residential, business, and enterprise "
            f"broadband, voice, and related services;",
        ),
        (
            "D",
            f"WHEREAS, the {TR} desires to engage {OP} as the developer and operator of the "
            f"grant-funded infrastructure, and to grant {OP} a long-term indefeasible right of use "
            f"(the “{IRU}”) in the {TA} so that the {TA} may be interconnected with the "
            f"{OE} to form a single, functional hybrid network (the “{NET}”) delivering "
            f"service to end users, all without any transfer of title to the {TA};",
        ),
        (
            "E",
            f"WHEREAS, the {C.PARTIES_COLLECTIVE} intend that this Agreement, together with the "
            f"companion documents identified in the order-of-precedence provisions, will govern the "
            f"development, construction, ownership, interconnection, operation, and maintenance of "
            f"the {NET}, and that all such arrangements comply with the {C.PROGRAM_SHORT} award, "
            f"the {cite('ug_part')}, and all other applicable federal requirements; and",
        ),
        (
            "F",
            f"WHEREAS, the {C.PARTIES_COLLECTIVE} acknowledge that this Agreement is a working "
            f"draft prepared for negotiation and is subject to legal, grant-compliance, and "
            f"financial review, and that certain commercial, technical, and legal terms remain "
            f"open and are marked accordingly;",
        ),
    ]
    for lbl, txt in recitals:
        SUB(doc, lbl, txt)

    P(
        doc,
        f"NOW, THEREFORE, in consideration of the mutual covenants and agreements set forth herein, "
        f"and for other good and valuable consideration, the receipt and sufficiency of which are "
        f"hereby acknowledged, the {C.PARTIES_COLLECTIVE} agree as follows:",
    )

    # ==================================================================
    # ARTICLE 1 — DEFINITIONS AND INTERPRETATION
    # ==================================================================
    C.article(doc, 1, "Definitions and Rules of Interpretation")
    S(
        doc,
        "1.1",
        "Defined Terms",
        "As used in this Agreement, the following capitalized terms have the meanings set forth "
        "below. Defined terms are used consistently across every document in the transaction "
        "package and must not be varied without a conforming amendment to each affected document.",
    )

    defs = [
        ("Agreement", "this Master Development, Construction and Operating Agreement, together with all exhibits, schedules, and addenda, as amended from time to time."),
        ("Acceptance", f"the {TR}'s acceptance of a Segment or of the {NET} in accordance with the testing-and-acceptance provisions of Article 13 and Exhibits E and G."),
        ("Applicable Law", "all federal, State, Tribal, and local statutes, regulations, codes, ordinances, orders, permits, and legally binding requirements applicable to a Party or to the Network, including the Award Requirements."),
        ("Award", f"the {C.PROGRAM_SHORT} grant award, if and when made to the {TR} by {C.AGENCY_SHORT}, including the notice of award, the approved budget and scope, and all terms and conditions incorporated therein."),
        ("Award Requirements", f"collectively, the Award; the {cite('sac')}; the {cite('nofo')}; the {cite('ug_part')}; and all other federal statutes, regulations, and guidance applicable to the Award."),
        ("As-Built Documentation", "the complete, accurate record drawings, GIS data, splice records, test results, and related deliverables described in Article 14 and Exhibit E."),
        ("BABA", f"the {cite('baba')}, together with any waiver granted thereunder."),
        (C.DEMARCATION, f"each physical and logical point of interconnection between the {TA} and the {OE} at which ownership, operational responsibility, and the boundary of the {FI} are delineated, as described in Article 16 and depicted in Exhibit B."),
        ("Effective Date", "the date first written above on which this Agreement becomes effective."),
        ("Essential Services", "broadband internet access service and, where provided, voice service to active end users, and the network functions necessary to sustain them, the interruption of which materially threatens public safety, health, or continuity of service."),
        (C.FEDERAL_INTEREST, f"the continuing interest of the United States in the {TA} and related property arising under the Award and {cite('real_property')}, {cite('equipment')}, {cite('intangible')}, and {cite('trust')}, including federal rights with respect to use, encumbrance, and disposition."),
        (C.GRANT_FUNDED, f"the infrastructure, equipment, and other property acquired, constructed, or improved in whole or in part with {C.PROGRAM_SHORT} funds; also referred to as the {TA}."),
        (IRU, f"the indefeasible right of use granted to {OP} in the {TA} under this Agreement and more fully set forth in the IRU Agreement (Document 02.02), which conveys an exclusive operational right of use for the IRU Term without any transfer of title."),
        ("IRU Term", f"the initial term of the {IRU}, which the {C.PARTIES_COLLECTIVE} are modeling at {', '.join(str(y) for y in C.IRU_TERMS_YEARS)} years (recommended: {C.IRU_TERM_RECOMMENDED} years), subject to {C.IRU_RENEWAL_DEFAULT}, as finalized in Document 02.02."),
        (JA, f"assets funded partly with {C.PROGRAM_SHORT} funds and partly with {OP} or third-party funds, the ownership and cost-allocation of which are addressed in Article 15."),
        (NET, f"the single, functional hybrid broadband network formed by interconnecting the {TA} with the {OE}, as described in the recitals and Article 16."),
        (PI, f"gross income earned by the {TR} that is directly generated by a supported activity or earned as a result of the Award during the period of performance, as defined at {cite('prog_income')}."),
        ("Segment", "a defined portion of the Network (for example, a route, fiber ring, or service area) that is designed, constructed, tested, and accepted as a unit, as identified in Exhibit D."),
        (ST, f"the geographic area in {C.GEOGRAPHY} in which the Network is to be deployed and service provided, as delineated in Exhibit A and the Award."),
        ("Subrecipient / Contractor", f"the characterization of {OP}'s legal relationship to the Award for federal purposes, to be determined under the analysis in Article 6 and {cite('subrecipient')}."),
        (TA, f"the {GF}, owned by and titled in the {TR}, subject to the {FI}, and made available to {OP} under the {IRU}."),
        (OA, f"network facilities, equipment, and property owned by {OP} that are not funded with {C.PROGRAM_SHORT} funds, including the {OE}."),
        (OE, f"{OP}'s existing middle-mile, backbone, and core network facilities to which the {TA} interconnect."),
    ]
    C.add_table(
        doc,
        ["Defined Term", "Meaning"],
        [[f"“{t}”", m] for t, m in defs],
        widths=[1.9, 4.9],
        font_size=8,
    )
    FL(
        doc,
        C.FLAG_ATTORNEY,
        "This defined-terms table is representative and must be reconciled against the final "
        "definitions in Documents 02.02–02.07 and the Exhibits so that every capitalized term "
        "carries one consistent meaning across the package.",
    )

    S(
        doc,
        "1.2",
        "Rules of Interpretation",
        "In this Agreement, unless the context requires otherwise:",
    )
    for lbl, txt in [
        ("a", "the singular includes the plural and vice versa, and references to any gender include all genders;"),
        ("b", "“including,” “include,” and “includes” mean including without limitation;"),
        ("c", "references to a statute, regulation, or Award Requirement are to that authority as amended, superseded, or replaced from time to time, and to any successor authority;"),
        ("d", "headings and captions are for convenience only and do not affect interpretation;"),
        ("e", "references to Articles, Sections, Exhibits, and Schedules are to this Agreement unless otherwise stated;"),
        ("f", "in the event of any conflict, the order-of-precedence provisions in Article 29 govern; and"),
        ("g", "no rule of construction against the drafting Party applies, this Agreement having been negotiated by sophisticated parties with the benefit of counsel."),
    ]:
        SUB(doc, lbl, txt)

    # ==================================================================
    # ARTICLE 2 — PURPOSE AND RELATIONSHIP OF THE PARTIES
    # ==================================================================
    C.article(doc, 2, "Purpose and Relationship of the Parties")
    S(
        doc,
        "2.1",
        "Purpose",
        f"The purpose of this Agreement is to establish the framework under which {OP} will "
        f"develop, construct, activate, operate, and maintain the {TA} and interconnect them with "
        f"the {OE} to deliver broadband, voice, and related services to end users in the {ST}, "
        f"while the {TR} retains ownership of and title to the {TA} at all times and administers the "
        f"Award in compliance with the Award Requirements.",
    )
    S(
        doc,
        "2.2",
        "Title Retained by the Tribe",
        f"Legal title to the {TA} vests in and remains with the {TR} at all times. Nothing in this "
        f"Agreement, the {IRU}, or any companion document transfers, or is intended to transfer, "
        f"title to the {TA} to {OP}. {OP}'s rights in the {TA} are limited to the operational right "
        f"of use conveyed by the {IRU}. This allocation is a material term and a condition of the "
        f"Award. See {cite('real_property')} and {cite('equipment')}.",
    )
    S(
        doc,
        "2.3",
        "Independent Contractor; No Partnership",
        f"{OP} performs under this Agreement as an independent contractor. Except as expressly "
        f"provided, nothing in this Agreement creates a partnership, joint venture, agency, or "
        f"fiduciary relationship between the {C.PARTIES_COLLECTIVE}, and neither Party may bind the "
        f"other except as expressly authorized. The characterization of {OP} for federal-award "
        f"purposes is governed by Article 6.",
    )
    S(
        doc,
        "2.4",
        "Relationship to Companion Documents",
        "This Agreement is the master commercial instrument for the transaction and is implemented "
        "through the following companion documents, each of which is incorporated by reference:",
    )
    for txt in [
        "the IRU Agreement (Document 02.02), which conveys and details the indefeasible right of use in the Tribal Assets;",
        "the Operations, Maintenance and Service-Level Agreement (Document 02.03), which sets operational, maintenance, and service-level obligations;",
        "the Financial and Revenue-Sharing Schedule (Document 02.04), which sets consideration, revenue-sharing, and financial terms;",
        "the Grant Compliance and Federal Interest Addendum (Document 02.05), which sets federal-award compliance obligations and Federal Interest protections;",
        "the Data Privacy and Cybersecurity Addendum (Document 02.06), which sets data-protection and security obligations;",
        "the Transition and Step-In Plan (Document 02.07), which sets step-in, transition, and successor-operator procedures; and",
        "Exhibits A through O, which set the Service Territory, network design, schedule, testing, insurance, and related operative detail.",
    ]:
        B(doc, txt)

    # ==================================================================
    # ARTICLE 3 — CONDITIONS PRECEDENT
    # ==================================================================
    C.article(doc, 3, "Conditions Precedent")
    S(
        doc,
        "3.1",
        "Conditions to Effectiveness and to Construction",
        f"The obligations of the {C.PARTIES_COLLECTIVE} to proceed with construction of the {TA} "
        f"are subject to the satisfaction (or written waiver by the Party entitled to the benefit) "
        f"of each of the following conditions precedent:",
    )
    for lbl, txt in [
        ("a", f"the {TR} shall have been made the recipient of the Award, and the Award shall be in full force and effect with a scope and budget consistent with this Agreement;"),
        ("b", f"grant counsel shall have confirmed the {TR}'s eligibility and standing to hold the Award notwithstanding the federal-recognition question flagged in the recitals ({cite('lumbee_act')});"),
        ("c", f"the environmental and historic-preservation reviews required by Article 8 shall have been completed and clearance issued for the applicable Segment ({cite('nepa')}; {cite('nhpa')}) — no construction may commence before clearance;"),
        ("d", "all governing-body authorizations, including any required Tribal Council resolution and any required consents, shall have been obtained;"),
        ("e", f"{OP} shall have delivered evidence of the insurance required by Article 22 and Exhibit I;"),
        ("f", "the companion documents (Documents 02.02–02.07) and the applicable Exhibits shall have been executed or agreed in a form consistent with this Agreement; and"),
        ("g", f"any conditions in the {cite('sac')} that must be satisfied before construction shall have been satisfied."),
    ]:
        SUB(doc, lbl, txt)
    FL(
        doc,
        C.FLAG_GRANT,
        "The sequencing of conditions (award, environmental/historic clearance, and any "
        "pre-construction Specific Award Conditions) must be confirmed against the final Award "
        "terms. Federal funds may not be drawn, and construction may not begin, until all "
        "pre-construction conditions in the Award are met.",
    )
    S(
        doc,
        "3.2",
        "Failure of Conditions",
        f"If a condition precedent is not satisfied or waived by {C.PH('outside date')} (the "
        f"“Outside Date”), either Party may terminate this Agreement upon notice without "
        f"liability, except for obligations that expressly survive. The {C.PARTIES_COLLECTIVE} shall "
        f"cooperate in good faith to satisfy the conditions.",
    )

    # ==================================================================
    # ARTICLE 4 — GRANT APPLICATION AND AWARD RESPONSIBILITIES
    # ==================================================================
    C.article(doc, 4, "Grant Application and Award Responsibilities")
    S(
        doc,
        "4.1",
        "Applicant and Recipient",
        f"The {TR} is the applicant for, and if awarded will be the recipient of, the Award. The "
        f"{TR} holds ultimate responsibility to {C.AGENCY_SHORT} for administration of the Award in "
        f"accordance with the Award Requirements, including as a pass-through entity to the extent "
        f"{OP} is later determined to be a subrecipient under Article 6 ({cite('pass_through')}).",
    )
    S(
        doc,
        "4.2",
        "Application Support by RIVR Tech",
        f"{OP} shall provide the {TR} with technical, engineering, mapping, cost-estimate, and "
        f"narrative support reasonably necessary for the application and for any post-award budget, "
        f"scope, or environmental submissions, and shall furnish supporting data in {OP}'s "
        f"possession. {OP} shall not submit any filing directly to {C.AGENCY_SHORT} on the {TR}'s "
        f"behalf except as the {TR} authorizes in writing.",
    )
    S(
        doc,
        "4.3",
        "Accuracy and Certifications",
        f"Each Party shall ensure that information it furnishes for the application and for Award "
        f"administration is accurate and complete in all material respects, and shall comply with "
        f"the mandatory-disclosure requirements of {cite('disclosures')}. {OP} shall provide "
        f"certifications regarding debarment and suspension ({cite('debarment')}) and prohibited "
        f"telecommunications equipment ({cite('telecom_ban')}) as required.",
    )
    S(
        doc,
        "4.4",
        "Award Acceptance and Amendments",
        f"The decision to accept the Award, and any decision to seek an amendment, budget revision, "
        f"or scope change requiring {C.AGENCY_SHORT} approval, rests with the {TR}. {OP} shall "
        f"support the {TR} in preparing any such request and shall not take action that would "
        f"require {C.AGENCY_SHORT} prior approval without the {TR}'s written direction.",
    )

    # ==================================================================
    # ARTICLE 5 — RIVR TECH AS DEVELOPER AND OPERATOR
    # ==================================================================
    C.article(doc, 5, "RIVR Tech's Role as Developer and Operator")
    S(
        doc,
        "5.1",
        "Scope of Engagement",
        f"Subject to the terms of this Agreement, the {TR} engages {OP}, and {OP} accepts the "
        f"engagement, to serve as the sole developer and operator of the {TA} and the {NET} in the "
        f"{ST}, including to: (i) design and engineer the {TA}; (ii) procure materials and services; "
        f"(iii) construct, install, and activate the {TA}; (iv) interconnect the {TA} with the {OE}; "
        f"(v) operate, maintain, monitor, and repair the {NET}; and (vi) market, sell, provision, "
        f"bill, and support broadband, voice, and related services to end users.",
    )
    S(
        doc,
        "5.2",
        "Standard of Performance",
        f"{OP} shall perform in a good, workmanlike, and professional manner, consistent with "
        f"prudent telecommunications industry practice, the engineering standards of Article 7, the "
        f"service levels of Document 02.03, and all Applicable Law and Award Requirements. {OP} "
        f"shall staff the engagement with qualified personnel and maintain all licenses and "
        f"certifications necessary to perform.",
    )
    S(
        doc,
        "5.3",
        "Exclusivity and Coordination",
        f"During the IRU Term, {OP} shall be the exclusive operator of the {TA}, and the {TR} shall "
        f"not grant conflicting operating rights, subject to the {TR}'s step-in and successor-"
        f"operator rights under Articles 25 and Document 02.07 and to the Award Requirements. {OP} "
        f"shall coordinate its use of the {TA} with the {OE} so that the {NET} operates as a single "
        f"functional system.",
    )

    # ==================================================================
    # ARTICLE 6 — CONTRACTOR / SUBRECIPIENT / OPERATOR DETERMINATION
    # ==================================================================
    C.article(doc, 6, "Determination of Contractor vs. Subrecipient vs. Operator")
    S(
        doc,
        "6.1",
        "Why the Determination Matters",
        f"Federal law requires the {TR}, as the pass-through entity, to determine whether {OP}'s "
        f"relationship to the Award is that of a subrecipient or a contractor (vendor) for each "
        f"agreement it makes, applying the substance-over-form factors of {cite('subrecipient')}. "
        f"The determination controls which federal requirements flow down to {OP}, the {TR}'s "
        f"monitoring obligations, and the treatment of payments. The {C.PARTIES_COLLECTIVE} must "
        f"not decide this by label alone.",
    )
    S(
        doc,
        "6.2",
        "Subrecipient Indicators (2 CFR 200.331(a))",
        "Characteristics indicating a subrecipient relationship include that the entity: determines "
        "who is eligible to receive federal assistance; has its performance measured against whether "
        "objectives of the federal program are met; has responsibility for programmatic "
        "decision-making; is responsible for adherence to applicable federal program requirements; "
        "and uses the federal funds to carry out a program of the entity (rather than providing "
        "goods or services for the pass-through entity's own use).",
    )
    S(
        doc,
        "6.3",
        "Contractor / Vendor Indicators (2 CFR 200.331(b))",
        "Characteristics indicating a contractor (procurement) relationship include that the entity: "
        "provides the goods and services within normal business operations; provides similar goods "
        "or services to many different purchasers; normally operates in a competitive environment; "
        "provides goods or services that are ancillary to the operation of the federal program; and "
        "is not subject to compliance requirements of the federal program as a result of the "
        "agreement (though similar requirements may apply for other reasons).",
    )
    S(
        doc,
        "6.4",
        "Bracketed Characterization (To Be Confirmed by Grant Counsel)",
        "The Parties present, and do NOT here resolve, the following alternatives:",
    )
    for lbl, txt in [
        ("A", f"[ALTERNATIVE A — CONTRACTOR / VENDOR: {OP} is treated as a contractor providing construction and operating services to the {TR} for the {TR}'s program. Procurement standards (Article 10) govern the selection and the flow-down is limited to the clauses required for contracts under {cite('procurement')} and Appendix II to Part 200.]"),
        ("B", f"[ALTERNATIVE B — SUBRECIPIENT: {OP} is treated as a subrecipient carrying out a portion of the {TR}'s program, in which case the {TR} must make a subaward, monitor {OP} under {cite('pass_through')}, and flow down applicable federal requirements.]"),
        ("C", "[ALTERNATIVE C — HYBRID / DUAL ROLE: distinct scopes are characterized separately (e.g., construction as a procurement/contractor relationship; long-term operation under a different characterization), with each scope documented and monitored accordingly.]"),
    ]:
        SUB(doc, lbl, txt)
    P(
        doc,
        f"Recommended preliminary characterization: the Parties note that a for-profit operator "
        f"providing construction and broadband-operating services within its normal business "
        f"operations, in a competitive environment, is likely characterized as a CONTRACTOR / "
        f"VENDOR under {cite('subrecipient')}; however, the long-term operating and revenue-sharing "
        f"structure has subrecipient-like features that must be evaluated. This is a preliminary "
        f"view only.",
    )
    FL(
        doc,
        C.FLAG_GRANT,
        f"The contractor-vs-subrecipient determination under {cite('subrecipient')} is reserved for "
        f"grant counsel and must be documented by the {TR} as the pass-through entity. Do not treat "
        f"the recommended CONTRACTOR/VENDOR characterization as final. The determination changes the "
        f"flow-down clauses, monitoring obligations, and payment treatment throughout this package.",
    )
    FL(
        doc,
        C.FLAG_ATTORNEY,
        "Counsel should confirm that the operative documents (this Agreement, the IRU Agreement, and "
        "the Financial Schedule) are internally consistent with the characterization ultimately "
        "selected, and that the procurement history supports it if CONTRACTOR is chosen.",
    )

    # ==================================================================
    # ARTICLE 7 — NETWORK DESIGN AND ENGINEERING STANDARDS
    # ==================================================================
    C.article(doc, 7, "Network Design and Engineering Standards")
    S(
        doc,
        "7.1",
        "Network Design",
        f"{OP} shall prepare and maintain the detailed design of the {TA} and the {NET}, including "
        f"route plans, fiber counts, splice plans, electronics, and service-area maps, consistent "
        f"with the Award scope and Exhibit A ({ST}) and Exhibit B (network design and demarcation). "
        f"The design shall provide capacity to meet the service floor of {C.SPEED_FLOOR} and the "
        f"scalability required to meet Award performance obligations.",
    )
    FL(
        doc,
        C.FLAG_TECH,
        f"Final route miles, fiber counts, hut/cabinet locations, electronics platform, and homes/"
        f"businesses passed are {C.PH('to be provided by RIVR Tech engineering and confirmed against the Award scope')}."
        f" Two-to-three design alternatives (e.g., centralized-split vs. distributed-"
        f"split PON; ring vs. hub-and-spoke) should be evaluated in Exhibit B with a recommendation.",
    )
    S(
        doc,
        "7.2",
        "Engineering Standards",
        f"The {TA} shall be designed and built to recognized industry standards, including "
        f"applicable Telcordia/GR, IEEE, ANSI/TIA, and manufacturer specifications, and to the "
        f"optical performance criteria in Exhibit E, including bi-directional OTDR testing at "
        f"{C.OPTICAL['wavelengths']}, maximum splice loss of {C.OPTICAL['splice_loss_max']}, and "
        f"maximum connector loss of {C.OPTICAL['connector_loss_max']}.",
    )
    S(
        doc,
        "7.3",
        "Design Review and Approval",
        f"{OP} shall submit the design (and material design changes) to the {TR} for review. The "
        f"{TR} may review for consistency with the Award scope and this Agreement; {TR} review does "
        f"not relieve {OP} of responsibility for the adequacy of the design. Design changes that "
        f"affect the Award scope or budget require the {TR}'s prior written approval and, where "
        f"required, {C.AGENCY_SHORT} approval.",
    )

    # ==================================================================
    # ARTICLE 8 — ENVIRONMENTAL AND HISTORIC PRESERVATION
    # ==================================================================
    C.article(doc, 8, "Environmental and Historic Preservation (NEPA / NHPA)")
    S(
        doc,
        "8.1",
        "No Construction Before Clearance",
        f"Notwithstanding any other provision, no ground-disturbing or construction activity funded "
        f"in whole or in part by the Award may commence for any Segment until all environmental "
        f"review under the {cite('nepa')} and all historic-preservation review under {cite('nhpa')} "
        f"have been completed and the {TR} has received written clearance or authorization to proceed "
        f"from {C.AGENCY_SHORT} for that Segment. This is a strict condition and a Federal "
        f"requirement.",
    )
    FL(
        doc,
        C.FLAG_GRANT,
        f"NEPA and NHPA Section 106 review must be completed and documented, and clearance obtained, "
        f"before any construction. Premature ground disturbance can jeopardize the Award and trigger "
        f"disallowed costs. See {cite('nepa')} and {cite('nhpa')}.",
    )
    S(
        doc,
        "8.2",
        "RIVR Tech Support of Review",
        f"{OP} shall prepare and furnish the environmental and cultural-resource information, site "
        f"data, maps, and studies reasonably necessary to support the review, shall support "
        f"government-to-government and Tribal Historic Preservation consultation, and shall "
        f"incorporate any resulting conditions, mitigation measures, or route modifications into the "
        f"design and construction at no separate charge except as the {C.PARTIES_COLLECTIVE} agree.",
    )
    S(
        doc,
        "8.3",
        "Inadvertent Discoveries",
        f"{OP} shall implement an inadvertent-discovery protocol requiring immediate work stoppage in "
        f"the affected area, protection of the find, and notice to the {TR} and appropriate "
        f"authorities upon discovery of any archaeological, cultural, or human remains, and shall not "
        f"resume until authorized. The protocol shall respect the {TR}'s cultural authority.",
    )

    # ==================================================================
    # ARTICLE 9 — PERMITTING AND EASEMENTS
    # ==================================================================
    C.article(doc, 9, "Permitting, Rights-of-Way, and Easements")
    S(
        doc,
        "9.1",
        "Permits and Authorizations",
        f"{OP} shall, at its cost (subject to allowability and the budget), obtain and maintain all "
        f"permits, licenses, pole-attachment agreements, railroad and highway crossings, and other "
        f"authorizations necessary to construct and operate the {TA}, including compliance with "
        f"North Carolina underground-utility damage-prevention/811 locate requirements "
        f"({cite('nc_dig')}) and utility-pole attachment requirements ({cite('nc_pole')}).",
    )
    S(
        doc,
        "9.2",
        "Rights-of-Way and Easements on Tribal and Other Lands",
        f"The {C.PARTIES_COLLECTIVE} shall cooperate to secure rights-of-way and easements. On lands "
        f"owned or controlled by the {TR}, the {TR} shall grant or facilitate the easements, "
        f"licenses, or use rights necessary for the {TA}, on terms consistent with the {FI} and the "
        f"{IRU}. On other lands, {OP} shall obtain the necessary rights in the name of, or for the "
        f"benefit of, the {TR} as owner of the {TA}, with the {IRU} rights running to {OP}.",
    )
    FL(
        doc,
        C.FLAG_ATTORNEY,
        "The form of easement/right-of-way instruments, whether they run to the Tribe as owner, and "
        "any recording, Tribal-land status, and BIA-approval questions must be reviewed by counsel. "
        "Easements encumbering grant-funded real property implicate the encumbrance restrictions of "
        f"{cite('real_property')}.",
    )

    # ==================================================================
    # ARTICLE 10 — PROCUREMENT, MATERIALS MANAGEMENT, AND BABA
    # ==================================================================
    C.article(doc, 10, "Procurement, Materials Management, and Domestic Preference")
    S(
        doc,
        "10.1",
        "Procurement Standards",
        f"All procurement of property and services charged in whole or in part to the Award shall "
        f"comply with the procurement standards at {cite('procurement')}, including full and open "
        f"competition ({cite('competition')}), the permissible methods of procurement "
        f"({cite('methods')}), and written procurement procedures. Conflicts of interest shall be "
        f"avoided and managed under {cite('conflict')}.",
    )
    FL(
        doc,
        C.FLAG_GRANT,
        f"If {OP} is characterized as a CONTRACTOR under Article 6, {OP}'s own selection must be "
        f"supported by a compliant procurement (or a documented sole-source justification) under "
        f"{cite('methods')}. Grant counsel must confirm the procurement basis for engaging {OP} and "
        f"for {OP}'s downstream subcontracts.",
    )
    S(
        doc,
        "10.2",
        "Build America, Buy America (BABA)",
        f"All iron, steel, manufactured products, and construction materials incorporated into the "
        f"{TA} shall comply with {cite('baba')}, unless a waiver applies. {OP} shall obtain and "
        f"retain supplier certifications of BABA compliance and shall support any waiver request the "
        f"{TR} elects to pursue.",
    )
    S(
        doc,
        "10.3",
        "Prohibited Telecommunications Equipment",
        f"{OP} shall not procure or install any covered telecommunications equipment or services "
        f"prohibited under {cite('telecom_ban')}, and shall certify compliance for the {TA}.",
    )
    S(
        doc,
        "10.4",
        "Debarment and Suspension",
        f"{OP} and its subcontractors at any tier shall not be debarred, suspended, or otherwise "
        f"excluded, and {OP} shall verify status consistent with {cite('debarment')} before award "
        f"of any covered subcontract.",
    )
    S(
        doc,
        "10.5",
        "Materials Management",
        f"{OP} shall manage materials and equipment purchased for the {TA} using inventory controls "
        f"consistent with {cite('equipment')} and {cite('supplies')}, including tagging, property "
        f"records, physical inventories, and safeguards against loss, damage, or theft. Title to "
        f"materials incorporated into the {TA} vests in the {TR} as owner, subject to the {FI}.",
    )

    # ==================================================================
    # ARTICLE 11 — CONSTRUCTION MANAGEMENT AND CONTRACTOR OVERSIGHT
    # ==================================================================
    C.article(doc, 11, "Construction Management and Contractor Oversight")
    S(
        doc,
        "11.1",
        "Construction Management",
        f"{OP} shall manage all construction of the {TA}, including mobilization, make-ready, "
        f"placement of conduit and fiber, splicing, electronics installation, and restoration, in "
        f"accordance with the design, the schedule (Exhibit D), Applicable Law, and the safety "
        f"requirements of prudent industry practice.",
    )
    S(
        doc,
        "11.2",
        "Subcontractors and Oversight",
        f"{OP} may engage qualified subcontractors but remains responsible for their performance and "
        f"for flow-down of applicable Award Requirements. {OP} shall oversee subcontractors, verify "
        f"licensing and insurance, enforce safety and quality, and maintain records sufficient to "
        f"demonstrate compliance and to support the {TR}'s reporting and audit obligations.",
    )
    S(
        doc,
        "11.3",
        "Safety and Compliance",
        f"{OP} shall maintain a written safety program, comply with OSHA and applicable safety "
        f"standards, and require the same of subcontractors. {OP} shall promptly notify the {TR} of "
        f"any material safety incident, citation, or stop-work order affecting the {TA}.",
    )

    # ==================================================================
    # ARTICLE 12 — SCHEDULE, MILESTONES, AND CHANGE ORDERS
    # ==================================================================
    C.article(doc, 12, "Construction Schedule, Milestones, and Change Orders")
    S(
        doc,
        "12.1",
        "Schedule and Milestones",
        f"{OP} shall construct the {TA} in accordance with the schedule and milestones in Exhibit D, "
        f"which shall be consistent with the Award's build-out and performance deadlines. {OP} shall "
        f"report progress against milestones and shall promptly notify the {TR} of any anticipated "
        f"delay and its mitigation plan.",
    )
    FL(
        doc,
        C.FLAG_GRANT,
        "Milestone dates must be reconciled with the Award's build-out deadlines and any interim "
        "performance milestones; failure to meet federal build-out deadlines can trigger remedies "
        f"for noncompliance under {cite('remedies')}.",
    )
    S(
        doc,
        "12.2",
        "Change Orders",
        f"Changes to the scope, schedule, or cost of construction shall be documented through the "
        f"change-order process in Exhibit F. Any change that affects the Award scope or budget, or "
        f"that requires {C.AGENCY_SHORT} prior approval, requires the {TR}'s prior written approval "
        f"and, where applicable, {C.AGENCY_SHORT} approval before the work proceeds.",
    )
    S(
        doc,
        "12.3",
        "Delay and Liquidated-Damages Placeholder",
        f"The {C.PARTIES_COLLECTIVE} shall address remedies for {OP} delay, including any milestone "
        f"credits or liquidated damages, at {C.PH('to be negotiated — milestone credit / liquidated-damage structure')}.",
    )
    FL(
        doc,
        C.FLAG_BUSINESS,
        "Whether to include milestone credits or liquidated damages for late completion, and at what "
        "level, is a business decision to be negotiated and reconciled with the Financial Schedule "
        "(Document 02.04).",
    )

    # ==================================================================
    # ARTICLE 13 — INSPECTIONS, TESTING, AND ACCEPTANCE
    # ==================================================================
    C.article(doc, 13, "Inspections, Testing, and Acceptance")
    S(
        doc,
        "13.1",
        "Inspections",
        f"The {TR} and its representatives (and {C.AGENCY_SHORT}) may inspect the {TA} and the work "
        f"at reasonable times. Inspection does not relieve {OP} of responsibility for conformance. "
        f"{OP} shall correct nonconforming work at its cost, subject to allowability.",
    )
    S(
        doc,
        "13.2",
        "Testing and Acceptance",
        f"Each Segment shall be tested in accordance with Exhibit E (optical and network acceptance "
        f"testing) and accepted in accordance with the acceptance procedures and punch-list process "
        f"in Exhibit G. Acceptance occurs only when the Segment meets the acceptance criteria and "
        f"{OP} has delivered the required test results and As-Built Documentation. Acceptance does "
        f"not waive latent-defect or warranty rights.",
    )
    S(
        doc,
        "13.3",
        "Warranty",
        f"{OP} shall warrant the construction of the {TA} against defects in materials and "
        f"workmanship for a period of {C.PH('warranty period — e.g., 12–24 months')} from "
        f"Acceptance, and shall pass through manufacturer warranties to the {TR} as owner.",
    )
    FL(
        doc,
        C.FLAG_BUSINESS,
        "Construction warranty duration and scope, and the interaction with the O&M obligations in "
        "Document 02.03, are to be negotiated.",
    )

    # ==================================================================
    # ARTICLE 14 — AS-BUILT DOCUMENTATION AND GIS
    # ==================================================================
    C.article(doc, 14, "As-Built Documentation and GIS")
    S(
        doc,
        "14.1",
        "As-Built Deliverables",
        f"Within {C.PH('number of days')} after Acceptance of each Segment, {OP} shall deliver to "
        f"the {TR} complete As-Built Documentation, including record drawings, GIS data in a mutually "
        f"agreed format, splice and fiber-assignment records, equipment inventories, and the test "
        f"results required by Exhibit E.",
    )
    S(
        doc,
        "14.2",
        "Ownership and Access to Records",
        f"As-Built Documentation and GIS data relating to the {TA} are the property of the {TR} as "
        f"owner of the {TA}, subject to {OP}'s license to use them for operations. Such records are "
        f"program records subject to the retention and access requirements of {cite('records')}.",
    )
    S(
        doc,
        "14.3",
        "Updates",
        f"{OP} shall keep the As-Built Documentation and GIS current throughout the IRU Term as the "
        f"{TA} are modified, and shall provide updated records to the {TR} on a periodic basis and "
        f"upon transition under Document 02.07.",
    )

    # ==================================================================
    # ARTICLE 15 — OWNERSHIP OF ASSETS
    # ==================================================================
    C.article(doc, 15, "Ownership of Assets")
    S(
        doc,
        "15.1",
        "General Principle",
        f"Ownership of assets follows the source of funds and the {FI}. The categories below govern "
        f"the {NET}. Asset boundaries are delineated at the {DEM}s under Article 16 and Exhibit B.",
    )
    S(
        doc,
        "15.2",
        f"Grant-Funded Assets ({TA})",
        f"All {TA} — the {GF} acquired, constructed, or improved with Award funds — are owned "
        f"by and titled in the {TR} and are subject to the continuing {FI}. Title does not transfer "
        f"to {OP}. Use, encumbrance, and disposition of the {TA} are governed by {cite('real_property')}, "
        f"{cite('equipment')}, {cite('intangible')}, and {cite('trust')}, and by the Grant Compliance "
        f"and Federal Interest Addendum (Document 02.05).",
    )
    S(
        doc,
        "15.3",
        f"Preexisting RIVR Tech Assets ({OA} / {OE})",
        f"The {OE} and other {OA} that predate or are funded outside the Award remain the sole "
        f"property of {OP}. No {FI} attaches to {OA} by reason of interconnection alone. {OP} is "
        f"responsible for the cost, maintenance, and replacement of {OA}, and the {TR} acquires no "
        f"ownership interest in them.",
    )
    S(
        doc,
        "15.4",
        f"Jointly Funded Assets ({JA})",
        f"For any asset funded partly with Award funds and partly with {OP} or third-party funds, "
        f"the {C.PARTIES_COLLECTIVE} shall document the cost allocation and the resulting ownership "
        f"and {FI} treatment before construction. The federally funded share, and any asset that "
        f"cannot be cleanly severed, is presumed subject to the {FI} and owned by the {TR} unless "
        f"grant counsel confirms a compliant alternative allocation.",
    )
    FL(
        doc,
        C.FLAG_GRANT,
        f"Cost allocation for {JA} and the resulting Federal Interest must be documented and confirmed "
        f"with grant counsel to avoid commingling that would extend the {FI} to {OP}'s own assets or "
        f"create disposition problems at closeout ({cite('closeout')}).",
    )
    S(
        doc,
        "15.5",
        "Future Improvements",
        f"Improvements, upgrades, and additions made during the IRU Term shall be characterized by "
        f"source of funds: Award-funded improvements become {TA} owned by the {TR} and subject to the "
        f"{FI}; {OP}-funded improvements to the {TA} shall be addressed as agreed (as {OP} property "
        f"removable at transition, as a betterment credited under Document 02.04, or as a donation to "
        f"the {TR}), and improvements to {OA} remain {OP} property. The treatment of {OP}-funded "
        f"electronics installed on the {TA} is {C.PH('to be specified — removable vs. transferred at transition')}.",
    )
    FL(
        doc,
        C.FLAG_BUSINESS,
        "The treatment of operator-funded upgrades and electronics (removable, credited, or donated), "
        "and their handling at transition, is a commercial point to be settled in Documents 02.02 "
        "and 02.04.",
    )

    # ==================================================================
    # ARTICLE 16 — INTERCONNECTION AND DEMARCATION
    # ==================================================================
    C.article(doc, 16, "Interconnection With RIVR Tech's Middle-Mile Network; Demarcation")
    S(
        doc,
        "16.1",
        "Interconnection",
        f"{OP} shall interconnect the {TA} with the {OE} at the {DEM}s so that the {NET} functions as "
        f"a single, seamless system delivering service to end users. {OP} shall provision, groom, and "
        f"maintain the interconnection and provide the transport, transit, and core services "
        f"necessary for the {TA} to reach the public internet and voice networks.",
    )
    S(
        doc,
        "16.2",
        "Demarcation Points",
        f"Each {DEM} marks the boundary between the {TR}-owned {TA} (subject to the {FI}) and the "
        f"{OP}-owned {OE}. The {DEM}s shall be documented in Exhibit B by physical location, port/"
        f"panel identification, and logical boundary, so that ownership, the extent of the {FI}, and "
        f"operational responsibility are unambiguous at every interconnection.",
    )
    FL(
        doc,
        C.FLAG_TECH,
        f"The specific {DEM} locations, port assignments, and the physical/logical boundary at each "
        f"interconnection are {C.PH('to be provided by RIVR Tech engineering in Exhibit B')}. Clean "
        f"demarcation is essential so the Federal Interest does not bleed into {OP}'s existing "
        f"network.",
    )
    S(
        doc,
        "16.3",
        "Continuity at the Demarcation",
        f"On expiration or termination, the {TR} (or a successor operator) must be able to "
        f"interconnect the {TA} at the {DEM}s and continue Essential Services. {OP} shall provide the "
        f"interconnection information, transitional transport, and cooperation required by Document "
        f"02.07 so that the {TA} remain usable independent of {OP}'s continued participation.",
    )

    # ==================================================================
    # ARTICLE 17 — OPERATIONS AND CUSTOMER-FACING FUNCTIONS
    # ==================================================================
    C.article(doc, 17, "Operations, Customer Installations, and Support")
    S(
        doc,
        "17.1",
        "Operations",
        f"{OP} shall operate and maintain the {NET} in accordance with Document 02.03 (Operations, "
        f"Maintenance and Service-Level Agreement), including preventive and corrective maintenance, "
        f"fault management, and capacity management, and shall meet the service levels stated there.",
    )
    S(
        doc,
        "17.2",
        "Network Monitoring",
        f"{OP} shall monitor the {NET} on a {D['sla']['noc']} basis from a network operations center, "
        f"targeting {D['sla']['availability_target']} availability, latency at or below "
        f"{D['sla']['latency_ms']} ms, packet loss at or below {D['sla']['packet_loss']}, and jitter "
        f"at or below {D['sla']['jitter_ms']} ms, all as further specified in Document 02.03.",
    )
    S(
        doc,
        "17.3",
        "Customer Installations and Provisioning",
        f"{OP} shall market, sell, install, and provision service to end users in the {ST}, including "
        f"scheduling, drop installation, customer-premises equipment, and activation, in a "
        f"non-discriminatory manner consistent with the Award's service obligations.",
    )
    S(
        doc,
        "17.4",
        "Billing and Collections",
        f"{OP} shall bill end users and collect revenue for services delivered over the {NET}, "
        f"maintain accurate billing records, and account for revenue as required by the Financial and "
        f"Revenue-Sharing Schedule (Document 02.04) and the Program Income provisions of Article 24.",
    )
    S(
        doc,
        "17.5",
        "Customer Service and Technical Support",
        f"{OP} shall provide customer service and technical support to end users, including a "
        f"trouble-ticketing process and support hours consistent with Document 02.03, and shall "
        f"handle customer complaints, including any escalation to the {TR} or regulators as required.",
    )

    # ==================================================================
    # ARTICLE 18 — MARKETING, SALES, AND RATE-SETTING
    # ==================================================================
    C.article(doc, 18, "Marketing, Sales, and Rate-Setting")
    S(
        doc,
        "18.1",
        "Marketing and Sales",
        f"{OP} shall market and sell services over the {NET} using its brand and channels, subject to "
        f"the {TR}'s reasonable approval of the use of the {TR}'s name, marks, or endorsement and to "
        f"the public-announcement provisions of Article 27. Marketing shall accurately describe the "
        f"service and any Award-required low-cost option.",
    )
    S(
        doc,
        "18.2",
        "Rate-Setting",
        f"{OP} shall set retail rates for services over the {NET}, subject to (i) the affordable-"
        f"service obligations of Article 19 and the Award, (ii) any applicable regulatory "
        f"requirements, and (iii) the revenue-sharing framework of Document 02.04. Rate structures "
        f"and any rate caps or floors are {C.PH('to be negotiated in Document 02.04')}.",
    )
    FL(
        doc,
        C.FLAG_BUSINESS,
        "Retail pricing, rate caps/floors, promotional pricing, and any Tribal approval right over "
        "rates are commercial terms to be negotiated in the Financial and Revenue-Sharing Schedule "
        "(Document 02.04). Do not fix pricing in this Master Agreement.",
    )

    # ==================================================================
    # ARTICLE 19 — AFFORDABLE-SERVICE AND VOICE OBLIGATIONS
    # ==================================================================
    C.article(doc, 19, "Affordable-Service and Voice Obligations")
    S(
        doc,
        "19.1",
        "Low-Cost Broadband Option",
        f"{OP} shall offer and publicize a low-cost broadband service option providing at least "
        f"{C.SPEED_FLOOR} service, consistent with the Award's affordability requirements and any "
        f"applicable low-cost service-option obligations, throughout the {ST}. The price, features, "
        f"and eligibility of the low-cost option shall satisfy the Award and are "
        f"{C.PH('to be confirmed against the Award terms')}.",
    )
    FL(
        doc,
        C.FLAG_GRANT,
        "The specific low-cost/affordable service-option terms (speed, price benchmark, and any "
        "eligibility conditions) must be confirmed against the Award and TBCP guidance and kept "
        "consistent with Document 02.04.",
    )
    S(
        doc,
        "19.2",
        "Voice Service",
        f"To the extent {OP} provides voice service over the {NET}, {OP} shall comply with applicable "
        f"telecommunications requirements, including 911/E-911, and shall be responsible for the "
        f"voice platform, interconnection, and regulatory obligations associated with voice.",
    )

    # ==================================================================
    # ARTICLE 20 — REGULATORY COMPLIANCE
    # ==================================================================
    C.article(doc, 20, "Regulatory Compliance (FCC / USAC / ETC)")
    S(
        doc,
        "20.1",
        "Communications Regulation",
        f"{OP} shall obtain and maintain all authorizations necessary to provide service over the "
        f"{NET} and shall comply with applicable Federal Communications Commission requirements. "
        f"Where universal-service, Lifeline, or Eligible Telecommunications Carrier (ETC) programs "
        f"apply, the responsible Party shall comply with {cite('usac_lifeline')}.",
    )
    S(
        doc,
        "20.2",
        "CPNI and Customer Data",
        f"{OP} shall protect customer proprietary network information in accordance with "
        f"{cite('cpni')}, and shall handle customer data in accordance with the Data Privacy and "
        f"Cybersecurity Addendum (Document 02.06).",
    )
    S(
        doc,
        "20.3",
        "Regulatory Filings and Cooperation",
        f"Each Party shall reasonably cooperate with the other regarding regulatory filings, "
        f"reporting, and inquiries relating to the {NET}, and shall promptly notify the other of any "
        f"regulatory action that could materially affect the {NET} or the Award.",
    )

    # ==================================================================
    # ARTICLE 21 — CYBERSECURITY AND DATA PRIVACY
    # ==================================================================
    C.article(doc, 21, "Cybersecurity and Data Privacy")
    S(
        doc,
        "21.1",
        "Cybersecurity",
        f"{OP} shall implement and maintain an information-security program protecting the {NET} and "
        f"the data it carries, consistent with the Data Privacy and Cybersecurity Addendum (Document "
        f"02.06), including access controls, monitoring, vulnerability management, and incident "
        f"response. {OP} shall not use prohibited equipment ({cite('telecom_ban')}).",
    )
    S(
        doc,
        "21.2",
        "Data Privacy",
        f"Each Party shall handle personal and customer data in accordance with Document 02.06 and "
        f"Applicable Law, including {cite('cpni')}. Incident notification, breach response, and data-"
        f"handling obligations are as set forth in Document 02.06.",
    )
    S(
        doc,
        "21.3",
        "Precedence of the Addendum",
        f"In the event of a conflict between this Article and Document 02.06, Document 02.06 governs "
        f"as to data-privacy and cybersecurity matters, subject to the overall order of precedence in "
        f"Article 29.",
    )

    # ==================================================================
    # ARTICLE 22 — INSURANCE
    # ==================================================================
    C.article(doc, 22, "Insurance")
    S(
        doc,
        "22.1",
        "Required Coverages",
        f"Throughout the term, {OP} shall maintain, at minimum, the insurance set forth in Exhibit I "
        f"and summarized below, with insurers reasonably acceptable to the {TR}, and shall name the "
        f"{TR} (and {C.AGENCY_SHORT} where required) as additional insured where appropriate. "
        f"Property/builder's risk coverage shall reflect the {FI} in the {TA}. See "
        f"{cite('insurance')}.",
    )
    ins = D["insurance"]
    C.add_table(
        doc,
        ["Coverage", "Minimum Limit (placeholder — confirm in Exhibit I)"],
        [
            ["Commercial General Liability (per occurrence)", ins["cgl_occurrence"]],
            ["Commercial General Liability (aggregate)", ins["cgl_aggregate"]],
            ["Automobile Liability", ins["auto"]],
            ["Umbrella / Excess Liability", ins["umbrella"]],
            ["Workers' Compensation", ins["workers_comp"]],
            ["Employer's Liability", ins["employers_liability"]],
            ["Professional / Technology E&O", ins["professional_tech_eo"]],
            ["Cyber Liability", ins["cyber"]],
            ["Property / Builder's Risk", ins["property_builders_risk"]],
            ["Pollution / Environmental", ins["pollution"]],
        ],
        widths=[3.4, 3.4],
        font_size=9,
    )
    FL(
        doc,
        C.FLAG_ATTORNEY,
        "Insurance limits shown are placeholders drawn from the canonical deal parameters and must be "
        "confirmed by the Tribe's risk advisor and reconciled with Exhibit I, including additional-"
        "insured, waiver-of-subrogation, and Federal Interest requirements.",
    )
    S(
        doc,
        "22.2",
        "Evidence and Notice",
        f"{OP} shall furnish certificates of insurance before construction and upon renewal, and "
        f"shall provide notice of cancellation or material change consistent with Exhibit I.",
    )

    # ==================================================================
    # ARTICLE 23 — INDEMNIFICATION AND LIMITATION OF LIABILITY
    # ==================================================================
    C.article(doc, 23, "Indemnification and Limitation of Liability")
    S(
        doc,
        "23.1",
        "Indemnification by RIVR Tech",
        f"{OP} shall indemnify, defend, and hold harmless the {TR}, its officials, employees, and "
        f"instrumentalities from and against third-party claims, losses, and liabilities to the "
        f"extent arising out of {OP}'s negligence, willful misconduct, breach of this Agreement, "
        f"violation of Applicable Law, infringement of intellectual property, or acts or omissions "
        f"in constructing or operating the {NET}, subject to the limitations in Section 23.3.",
    )
    S(
        doc,
        "23.2",
        "Indemnification by the Tribe",
        f"To the extent permitted by Applicable Law and subject to Article 28 (sovereignty and any "
        f"limited waiver), the {TR} shall be responsible for third-party claims to the extent arising "
        f"out of the {TR}'s breach of this Agreement or willful misconduct. Nothing in this Section "
        f"waives the {TR}'s sovereign immunity except as expressly provided in Article 28.",
    )
    FL(
        doc,
        C.FLAG_ATTORNEY,
        "The Tribe's indemnity, and any monetary exposure, are constrained by sovereign immunity. The "
        "scope of any Tribal indemnity must be reconciled with the sovereign-immunity provisions of "
        "Article 28 and cannot be read as an implied waiver.",
    )
    S(
        doc,
        "23.3",
        "Limitation of Liability",
        f"Except for the excluded matters below, and to the extent permitted by Applicable Law, "
        f"neither Party shall be liable for indirect, incidental, consequential, special, or "
        f"punitive damages, and each Party's aggregate liability shall be capped at "
        f"{C.PH('liability cap — to be negotiated (e.g., a stated dollar amount or a multiple of "
        f"fees)')}. The cap and exclusions do not apply to indemnification for third-party claims, "
        f"breaches of confidentiality, a Party's willful misconduct, or amounts required to cure a "
        f"loss of the {FI} or disallowed costs.",
    )
    FL(
        doc,
        C.FLAG_BUSINESS,
        "The liability cap, carve-outs, and whether damage to the Federal Interest / disallowed costs "
        "sit outside the cap are commercial and legal points to be negotiated.",
    )

    # ==================================================================
    # ARTICLE 24 — AUDIT, RECORDS, PROGRAM INCOME, AND REPORTING
    # ==================================================================
    C.article(doc, 24, "Audit Rights, Record Retention, Program Income, and Reporting")
    S(
        doc,
        "24.1",
        "Audit Rights",
        f"The {TR}, {C.AGENCY_SHORT}, the Department of Commerce Office of Inspector General, the "
        f"Comptroller General, and their authorized representatives shall have the right to examine "
        f"and audit {OP}'s records relating to the {NET} and the Award, on at least "
        f"{D['audit_notice_business_days']} business days' notice (or immediately where fraud or "
        f"imminent noncompliance is suspected), consistent with {cite('records')}. {OP} shall "
        f"cooperate with any single audit conducted under {cite('single_audit')}.",
    )
    S(
        doc,
        "24.2",
        "Record Retention",
        f"{OP} shall retain all records relating to the {NET} and the Award for at least "
        f"{D['records_retention_years']} years, measured as provided in {cite('records')} (generally "
        f"from submission of the final expenditure report), and longer if any litigation, claim, or "
        f"audit is started before expiration of the period, in which case records shall be retained "
        f"until resolution.",
    )
    S(
        doc,
        "24.3",
        f"{PI}",
        f"Revenue that constitutes {PI} under {cite('prog_income')} shall be identified, tracked, and "
        f"applied in accordance with the method required by the Award (deduction, addition, or cost-"
        f"sharing/matching) and as detailed in Documents 02.04 and 02.05. The {C.PARTIES_COLLECTIVE} "
        f"shall not treat revenue as ordinary commercial revenue to the extent it is {PI}.",
    )
    FL(
        doc,
        C.FLAG_GRANT,
        f"The Program-Income method (deduction / addition / cost-sharing) under {cite('prog_income')} "
        f"must be confirmed against the Award and coordinated with the revenue-sharing structure in "
        f"Document 02.04. Mischaracterizing revenue-share payments as non-program income is a common "
        f"finding.",
    )
    S(
        doc,
        "24.4",
        "Financial, Grant, and Performance Reporting",
        f"{OP} shall provide the {TR}, on a timely basis, the financial, construction, operational, "
        f"and performance data the {TR} needs to meet its Award reporting obligations, including "
        f"federal financial reports, performance-progress reports, build-out/subscriber data, and any "
        f"BABA or environmental certifications. Reporting formats and cadence are as set in Document "
        f"02.05 and the Exhibits.",
    )

    # ==================================================================
    # ARTICLE 25 — DEFAULT, CURE, STEP-IN, AND TRANSITION
    # ==================================================================
    C.article(doc, 25, "Default, Cure, Step-In, and Transition")
    S(
        doc,
        "25.1",
        "Events of Default",
        "An event of default occurs when a Party fails to perform a material obligation, makes a "
        "material misrepresentation, becomes insolvent, or (as to RIVR Tech) fails to maintain "
        "required insurance, abandons the work, or causes a loss of the Federal Interest or a "
        "material Award noncompliance that is not timely cured.",
    )
    S(
        doc,
        "25.2",
        "Notice and Cure",
        f"The non-defaulting Party shall give written notice describing the default. The defaulting "
        f"Party shall have {D['cure_monetary_days']} days to cure a monetary default and "
        f"{D['cure_nonmonetary_days']} days to cure a non-monetary default, with "
        f"{D['cure_nonmonetary_extension']}. Cure periods do not apply to emergencies threatening "
        f"Essential Services, safety, or Award compliance, which are addressed by step-in.",
    )
    S(
        doc,
        "25.3",
        "Tribal Step-In Rights",
        f"If {OP} fails to perform such that Essential Services, public safety, or Award compliance is "
        f"imminently threatened, the {TR} may step in — {D['stepin_emergency']} — to perform "
        f"or have a third party perform {OP}'s obligations, at {OP}'s cost to the extent the "
        f"condition is attributable to {OP}, in accordance with the Transition and Step-In Plan "
        f"(Document 02.07). Step-in does not, by itself, terminate the {IRU} or transfer {OA}.",
    )
    S(
        doc,
        "25.4",
        "RIVR Tech Cure and Protection Rights",
        f"{OP} shall have the right to receive notice and a reasonable opportunity to cure before the "
        f"{TR} exercises termination remedies, and reasonable protection of its {OA}, its lawful "
        f"interest in {OP}-funded improvements, and any financing party's rights, all subject to the "
        f"paramount {FI} and the requirement that the {TA} remain owned by the {TR}. Lender "
        f"protections, if any, are {C.PH('to be addressed if RIVR Tech financing requires them')}.",
    )
    FL(
        doc,
        C.FLAG_ATTORNEY,
        "Any lender/financing-party cure rights, collateral assignment, or leasehold-mortgage-style "
        "protection for RIVR Tech must be reconciled with the prohibition on encumbering grant-funded "
        f"real property ({cite('real_property')}) and the Federal Interest. Do not grant security "
        "interests in the Tribal Assets.",
    )
    S(
        doc,
        "25.5",
        "Transition to a Successor Operator",
        f"On expiration, termination, or a step-in that becomes permanent, {OP} shall provide up to "
        f"{D['transition_assistance_months']} months of transition assistance to the {TR} or a "
        f"successor operator in accordance with Document 02.07, including operational continuity, "
        f"transfer of As-Built Documentation and records, interconnection continuity at the {DEM}s, "
        f"and orderly handoff of customer relationships, so that Essential Services continue "
        f"uninterrupted.",
    )

    # ==================================================================
    # ARTICLE 26 — TERM, TERMINATION, ASSIGNMENT, CHANGE IN CONTROL
    # ==================================================================
    C.article(doc, 26, "Term, Termination, Assignment, and Change in Control")
    S(
        doc,
        "26.1",
        "Term",
        f"This Agreement takes effect on the Effective Date and, unless earlier terminated, continues "
        f"for a term coterminous with the IRU Term under Document 02.02 (initial term modeled at "
        f"{', '.join(str(y) for y in C.IRU_TERMS_YEARS)} years; recommended {C.IRU_TERM_RECOMMENDED} "
        f"years), plus {C.IRU_RENEWAL_DEFAULT} if exercised.",
    )
    S(
        doc,
        "26.2",
        "Termination",
        f"This Agreement may be terminated: (i) by the non-defaulting Party for an uncured event of "
        f"default; (ii) by mutual written agreement; (iii) as required to comply with the Award or a "
        f"direction of {C.AGENCY_SHORT} (including termination of the Award under {cite('remedies')}); "
        f"or (iv) on failure of a condition precedent under Article 3. The consequences of "
        f"termination, including transition, are governed by Article 25 and Document 02.07.",
    )
    S(
        doc,
        "26.3",
        "Assignment",
        f"Neither Party may assign this Agreement without the other's prior written consent, except "
        f"that assignment is in all cases subject to the {FI} and the Award Requirements, and any "
        f"assignment affecting the {TA} or the Award requires such consents and approvals (including "
        f"{C.AGENCY_SHORT} approval) as the Award Requirements demand. Any purported assignment in "
        f"violation of this Section is void.",
    )
    S(
        doc,
        "26.4",
        "Change in Control",
        f"A change in control of {OP} shall be treated as an assignment requiring the {TR}'s prior "
        f"written consent, and shall be subject to the {TR}'s right to evaluate the successor's "
        f"qualifications and Award-compliance capacity. {OP} shall notify the {TR} in advance of any "
        f"proposed change in control.",
    )
    FL(
        doc,
        C.FLAG_ATTORNEY,
        "Assignment and change-in-control mechanics must be reconciled with the IRU Agreement "
        "(Document 02.02) and with any Award requirement for federal approval of changes affecting "
        "the grant-funded assets.",
    )

    # ==================================================================
    # ARTICLE 27 — FORCE MAJEURE, CONFIDENTIALITY, ANNOUNCEMENTS
    # ==================================================================
    C.article(doc, 27, "Force Majeure, Confidentiality, and Public Announcements")
    S(
        doc,
        "27.1",
        "Force Majeure",
        f"Neither Party is liable for failure or delay in performance (other than payment obligations) "
        f"caused by events beyond its reasonable control, including natural disasters, severe weather, "
        f"acts of government, labor disputes, supply-chain disruption, and widespread utility or "
        f"telecommunications failures, provided the affected Party gives prompt notice, uses "
        f"reasonable efforts to mitigate, and resumes performance when able. Prolonged force majeure "
        f"beyond {C.PH('threshold — e.g., 90–180 days')} entitles either Party to pursue "
        f"transition or termination remedies without penalty.",
    )
    S(
        doc,
        "27.2",
        "Confidentiality",
        f"Each Party shall protect the other's confidential information and use it only to perform "
        f"this Agreement, subject to exceptions for information that is public, independently "
        f"developed, or lawfully obtained, and subject to required disclosures to {C.AGENCY_SHORT}, "
        f"auditors, and as required by Applicable Law (including any Tribal or public-records "
        f"obligations). Customer data is additionally governed by Document 02.06.",
    )
    S(
        doc,
        "27.3",
        "Public Announcements",
        f"Neither Party shall issue a public announcement using the other's name or marks without "
        f"prior written approval, except as required by law or the Award. Federally required "
        f"acknowledgment of {C.AGENCY_SHORT} funding shall be made as the Award directs.",
    )

    # ==================================================================
    # ARTICLE 28 — GOVERNING LAW, DISPUTES, SOVEREIGNTY, IMMUNITY
    # ==================================================================
    C.article(doc, 28, "Governing Law, Dispute Resolution, Sovereignty, and Limited Waiver of Sovereign Immunity")
    S(
        doc,
        "28.1",
        "Governing Law (Bracketed Alternatives — Not Selected)",
        "The Parties have NOT selected governing law. The following alternatives are presented for "
        "negotiation and legal review:",
    )
    for lbl, txt in [
        ("A", f"[ALTERNATIVE A — NORTH CAROLINA LAW: this Agreement is governed by the laws of the State of {C.STATE}, without regard to conflict-of-laws principles, except where federal law or Tribal law controls.]"),
        ("B", f"[ALTERNATIVE B — TRIBAL LAW: this Agreement is governed by the laws of the {TRF}, with State law applied only as a gap-filler where Tribal law is silent.]"),
        ("C", "[ALTERNATIVE C — FEDERAL LAW WHERE APPLICABLE: federal law and the Award Requirements govern matters they address; the Parties select a stated body of law (Tribal or State) for all other matters.]"),
    ]:
        SUB(doc, lbl, txt)
    FL(
        doc,
        C.FLAG_ATTORNEY,
        "Governing law is a threshold negotiation and sovereignty question and must be selected by "
        "counsel for both Parties. It is deliberately left unselected here. Federal law and the "
        "Award Requirements control the matters they address regardless of the choice made.",
    )
    S(
        doc,
        "28.2",
        "Dispute Resolution (Bracketed Alternatives — Not Selected)",
        "The Parties have NOT selected a dispute-resolution path. Alternatives:",
    )
    for lbl, txt in [
        ("A", "[ALTERNATIVE A — ESCALATION THEN ARBITRATION: good-faith executive negotiation, then non-binding mediation, then binding arbitration before a neutral under stated rules, seat, and number of arbitrators, with a carve-out for injunctive relief.]"),
        ("B", "[ALTERNATIVE B — LITIGATION: after negotiation and mediation, disputes are resolved by litigation in a specified forum (Tribal court, State court, or federal court, as the forum-selection clause provides).]"),
        ("C", "[ALTERNATIVE C — EXHAUSTION OF TRIBAL REMEDIES: disputes are first submitted to the Tribal forum for exhaustion of Tribal remedies before any external forum, consistent with federal Indian-law doctrine.]"),
    ]:
        SUB(doc, lbl, txt)
    FL(
        doc,
        C.FLAG_ATTORNEY,
        "Dispute resolution, forum selection, and any Tribal-exhaustion requirement are reserved for "
        "counsel. The choice interacts directly with the sovereign-immunity waiver in Section 28.4 "
        "and must be negotiated together.",
    )
    S(
        doc,
        "28.3",
        "Tribal Sovereignty",
        f"Nothing in this Agreement diminishes the sovereign status, governmental authority, or "
        f"self-governance of the {TRF}. No provision constitutes a consent to suit, a waiver of "
        f"sovereign immunity, or a transfer of jurisdiction except as, and only to the extent, "
        f"expressly provided in Section 28.4. Ambiguities are resolved in favor of preserving "
        f"sovereignty and immunity.",
    )
    S(
        doc,
        "28.4",
        "Limited Waiver of Sovereign Immunity (Bracketed Alternatives — Not Selected)",
        f"The {TR} has NOT agreed to any waiver of sovereign immunity in this draft. The following "
        f"alternatives are presented, unselected, for the {TR}'s governing body and counsel to "
        f"consider:",
    )
    for lbl, txt in [
        ("A", "[ALTERNATIVE A — NO WAIVER: the Tribe grants no waiver of sovereign immunity; RIVR Tech's remedies are limited to those that do not require suit against the Tribe (e.g., step-out/transition, non-renewal, set-off, and remedies against Tribal instrumentalities only if separately and expressly authorized).]"),
        ("B", "[ALTERNATIVE B — LIMITED WAIVER FOR DEFINED CLAIMS AND REMEDIES: the Tribe grants a narrow, express waiver solely for claims arising under this Agreement, limited to specified remedies (e.g., specific performance and contract damages capped at a stated amount or at available insurance/revenue), limited to a designated forum, expressly excluding any waiver of immunity as to third parties, and not extending to Tribal assets other than those specifically identified.]"),
        ("C", "[ALTERNATIVE C — ARBITRATION-ONLY WAIVER: the Tribe consents to binding arbitration and to enforcement of the arbitral award in a specified court solely to compel arbitration and confirm/enforce the award, with no other waiver, capped and bounded as in Alternative B.]"),
    ]:
        SUB(doc, lbl, txt)
    FL(
        doc,
        C.FLAG_ATTORNEY,
        "Sovereign immunity and any limited waiver are among the most consequential decisions in this "
        "transaction. This draft does NOT choose. Any waiver must be authorized by the Tribe's "
        "governing body by resolution, drafted narrowly (defined claims, capped remedies, designated "
        "forum, identified assets only), and reconciled with the governing-law and dispute-resolution "
        "choices in Sections 28.1–28.2. Do not infer a waiver from any other provision of this "
        "Agreement.",
    )

    # ==================================================================
    # ARTICLE 29 — ORDER OF PRECEDENCE AND GENERAL PROVISIONS
    # ==================================================================
    C.article(doc, 29, "Order of Precedence, Entire Agreement, and General Provisions")
    S(
        doc,
        "29.1",
        "Order of Precedence",
        "In the event of a conflict among the documents comprising the transaction, the following "
        "order of precedence controls, with federal requirements paramount:",
    )
    for lbl, txt in [
        ("a", f"first, the Award, the {cite('sac')}, and all applicable federal statutes, regulations, and guidance (including the {cite('ug_part')}, {cite('baba')}, {cite('nepa')}, and {cite('nhpa')}) — which control over any conflicting commercial term;"),
        ("b", "second, the Grant Compliance and Federal Interest Addendum (Document 02.05);"),
        ("c", "third, this Master Agreement (Document 02.01);"),
        ("d", "fourth, the IRU Agreement (Document 02.02);"),
        ("e", "fifth, the O&M/SLA (Document 02.03), the Financial and Revenue-Sharing Schedule (Document 02.04), and the Data Privacy and Cybersecurity Addendum (Document 02.06); and"),
        ("f", "sixth, the Exhibits A through O and the Transition and Step-In Plan (Document 02.07), except that a more specific technical or operational requirement in an Exhibit governs over a general statement in the body as to that technical detail."),
    ]:
        SUB(doc, lbl, txt)
    FL(
        doc,
        C.FLAG_GRANT,
        f"The Award and federal requirements must control over any conflicting commercial term. If any "
        f"provision of this package would cause noncompliance with the Award, the Award governs and "
        f"the provision is deemed modified to the minimum extent necessary to comply "
        f"({cite('remedies')}).",
    )
    S(
        doc,
        "29.2",
        "Entire Agreement",
        "This Agreement, together with the companion documents and Exhibits incorporated by "
        "reference, constitutes the entire agreement between the Parties on its subject matter and "
        "supersedes all prior understandings. It may be amended only by a writing signed by both "
        "Parties and, where required, approved by the appropriate federal authority.",
    )
    S(
        doc,
        "29.3",
        "Notices",
        f"Notices shall be in writing and delivered to the addresses in {C.PH('notice addresses — "
        f"to be inserted')}, by hand, recognized courier, or certified mail (and, if the Parties "
        f"agree, by email with confirmation), effective on receipt.",
    )
    S(
        doc,
        "29.4",
        "Miscellaneous",
        "The following standard provisions apply: severability (an invalid provision is reformed or "
        "severed without affecting the remainder); no waiver (a waiver must be in writing and is not "
        "a continuing waiver); survival (provisions that by their nature survive — including "
        "records, audit, indemnity, confidentiality, Federal Interest, and transition — survive "
        "expiration or termination); counterparts and electronic signatures; further assurances; and "
        "no third-party beneficiaries, except that the United States/NTIA is an intended beneficiary "
        "of the Federal Interest and Award-compliance provisions.",
    )

    # -------------------------------------------------------------------
    # SIGNATURES
    # -------------------------------------------------------------------
    C.article(doc, 30, "Signatures")
    P(
        doc,
        "The Parties execute this Agreement, subject to the outstanding legal, grant-compliance, and "
        "financial review flagged throughout, as of the Effective Date.",
    )
    C.signature_block(
        doc,
        extra_note="Signatory authority for the Tribe (including any required Tribal Council "
        "resolution) and for RIVR Tech must be confirmed before execution; if a designated Tribal "
        "instrumentality is the contracting party, conform the signature block accordingly.",
    )

    # -------------------------------------------------------------------
    # SAVE
    # -------------------------------------------------------------------
    path = C.save(
        doc,
        "02_Core_Agreements",
        "01_Master_Development_Construction_and_Operating_Agreement.docx",
    )
    return path


if __name__ == "__main__":
    p = build()
    print("SAVED ->", p)
