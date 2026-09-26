"""
gen_master_depc.py — Generator for the two DEFINITIVE AGREEMENTS of the
coordinated TBCP fiber-project package for the Lumbee Tribe of North Carolina
and RIVR Tech (LREMC Technologies, LLC d/b/a RIVR Tech).

Produces:
  02_Definitive_Agreements/01_Master_TBCP_Partnership_and_Implementation_Agreement.docx
  02_Definitive_Agreements/02_Design_Engineering_Procurement_and_Construction_Agreement.docx

The canonical engine Scripts/common.py is the SINGLE SOURCE OF TRUTH for party
names, defined terms, deal mechanics, order of precedence, citations, flags,
and formatting. Nothing in this generator invents award numbers, routes,
prices, useful life, approvals, land rights, or consents — unknowns are emitted
as highlighted placeholders (C.PH) and/or bracketed review flags (C.FLAG_*).
"""

import sys
sys.path.insert(0, '/home/user/claude-skills/Lumbee_RIVR_TBCP_Agreement_Package/Scripts')
import common as C


# ---------------------------------------------------------------------------
# SHARED BUILDING BLOCKS (used verbatim in BOTH agreements)
# ---------------------------------------------------------------------------
DISCLAIMER = (
    "These drafts are provided for business planning and attorney review. They are "
    "preliminary, non-binding working documents prepared without the controlling "
    f"{C.PROGRAM_SHORT} award or any source documents, do not constitute legal, financial, "
    "tax, engineering, or grant-compliance advice, and by themselves create no "
    "obligation, agreement, license, or right in favor of any Party. No Party should "
    "act or refrain from acting in reliance on these drafts. Nothing in these drafts "
    "authorizes any design finalization, construction, ground disturbance, procurement "
    "commitment, expenditure, encumbrance, interconnection, or service activation "
    "absent the executed federal Award and its Specific Award Conditions, confirmation "
    "of the controlling round and award terms, qualified attorney review, and all "
    "required governmental consent."
)


def precedence_and_shared_defs(doc, article_no, first_agreement=False):
    """Order-of-Precedence + Shared-Definitions article — verbatim in every agreement."""
    C.article(doc, article_no, "Order of Precedence and Shared Definitions")

    C.section(doc, f"{article_no}.1", "Order of Precedence",
              "In the event of any conflict, ambiguity, or inconsistency among the "
              "instruments comprising the transaction, the following order of precedence "
              "governs, from highest to lowest authority:")
    for item in C.PRECEDENCE:
        C.numbered(doc, item)

    C.section(doc, f"{article_no}.2", "Precedence Rule", C.PRECEDENCE_RULE)

    C.section(doc, f"{article_no}.3", "Shared Definitions", C.SHARED_DEFINITIONS_RULE)
    if not first_agreement:
        C.para(doc,
               f"This Agreement does not restate the shared glossary. Capitalized terms are "
               f"used as defined in Article 2 (Definitions) of the "
               f"{C.AGREEMENTS['master']}. Where a term is defined both here and in the "
               f"{C.AGREEMENTS['master']}, the {C.AGREEMENTS['master']} controls unless this "
               f"Agreement expressly states otherwise for a term unique to its subject matter.")

    C.section(doc, f"{article_no}.4", "No Enlargement of Federal or Tribal Obligations",
              "No provision of this Agreement, and no schedule, exhibit, certificate, or "
              "form, may be construed to authorize any act prohibited by, or inconsistent "
              "with, the Award, applicable federal law, or the sovereign rights of the "
              f"{C.TRIBE_SHORT}. A rejected or unenforceable commercial term does not "
              "invalidate a lawful construction and service provision; the provisions of "
              "Article on Severability and Reformation apply.")


def disclaimer_block(doc):
    """Standard closing disclaimer immediately before the signature block."""
    C.spacer(doc, 1)
    p = doc.add_paragraph()
    from docx.shared import Pt
    r = p.add_run("NOTICE AND DISCLAIMER")
    r.bold = True
    r.font.color.rgb = C.RED
    r.font.size = Pt(11)
    C.flag_para(doc, C.FLAG_ATTORNEY, DISCLAIMER)


def party_intro(doc, agreement_name):
    """Opening recital sentence naming the Parties and Effective Date."""
    p = doc.add_paragraph()
    r = p.add_run(
        f"This {agreement_name} (this “Agreement”) is entered into as of "
        f"{C.PH('Effective Date')} (the “Effective Date”), by and between "
        f"{C.TRIBE_FULL} (the “{C.TRIBE_SHORT}”), and {C.OPERATOR_FULL} "
        f"(“{C.OPERATOR_SHORT}”). The {C.TRIBE_SHORT} and {C.OPERATOR_SHORT} are "
        f"each a “{C.PARTY_SINGULAR}” and together the “{C.PARTIES_COLLECTIVE}.”"
    )
    C.flag_para(doc, C.FLAG_BUSINESS,
                f"Confirm whether the contracting Tribal party is the {C.TRIBE_FULL} directly "
                f"or {C.TRIBE_ENTITY_ALT}; align the recitals, signatory, and authorizing "
                f"resolution accordingly (Schedule S1).")


# ===========================================================================
#  DOCUMENT 1 — MASTER TBCP PARTNERSHIP AND IMPLEMENTATION AGREEMENT
# ===========================================================================
def build_master():
    doc = C.new_doc()
    C.add_cover(
        doc,
        "DOCUMENT 02.01 — DEFINITIVE AGREEMENTS",
        "Master TBCP Partnership and Implementation Agreement",
        "The umbrella agreement and single shared-definitions source for the "
        "coordinated TBCP fiber-project package",
    )
    C.setup_header_footer(doc, "Master TBCP Agreement")
    C.add_toc(doc)
    C.status_banner(doc)
    C.spacer(doc, 1)

    # ---- ARTICLE 1 : Parties, Recitals, Background -----------------------
    C.article(doc, 1, "Parties, Recitals, and Background")
    party_intro(doc, C.AGREEMENTS["master"])

    C.section(doc, "1.1", "Recitals")
    C.subsection(doc, "a",
                 f"The {C.TRIBE_SHORT} is a federally recognized Indian Tribe. Federal "
                 f"recognition status affecting {C.PROGRAM_SHORT} eligibility is governed by the "
                 f"{C.CITES['lumbee_act']}. {C.FLAG_GRANT} Counsel must confirm the "
                 f"{C.TRIBE_SHORT}'s recognition status and {C.PROGRAM_SHORT} eligibility "
                 f"basis against the controlling Award and NTIA determinations.")
    C.subsection(doc, "b",
                 f"The {C.TRIBE_SHORT} is (or expects to be) the award recipient and grant "
                 f"steward under the {C.PROGRAM_FULL} ({C.PROGRAM_SHORT}) administered by the "
                 f"{C.AGENCY_FULL} ({C.AGENCY_SHORT}), {C.DOC_FULL}, and will own the "
                 f"{C.TRIBAL_ASSETS} funded by the Award.")
    C.subsection(doc, "c",
                 f"{C.OPERATOR_FULL} (“{C.OPERATOR_SHORT}”) is the design, engineering, "
                 f"procurement, and construction party, the operator, and the retail broadband "
                 f"provider of record for the {C.NETWORK}, and owns and operates the "
                 f"{C.OPERATOR_EXISTING}.")
    C.subsection(doc, "d",
                 f"{C.LREMC_FULL} (“{C.LREMC_SHORT}”) is a separate legal entity that "
                 f"owns the {C.LREMC_ASSETS}, including poles, conduit, fiber, easements, huts, "
                 f"power, and land used in connection with the project. {C.LREMC_SHORT} is not a "
                 f"Party to this Agreement; {C.LREMC_ASSETS} are made available, if at all, only "
                 f"under the {C.AGREEMENTS['land']} and a separate {C.LREMC_SHORT} consent or "
                 f"joinder. {C.FLAG_ATTORNEY} No provision of this Agreement conveys, or assumes "
                 f"{C.OPERATOR_SHORT} ownership or control of, any {C.LREMC_ASSETS}.")
    C.subsection(doc, "e",
                 f"No controlling {C.PROGRAM_SHORT} award or source documents have been supplied. "
                 f"This Agreement uses, as a provisional baseline, the {C.NOFO_NAME}. "
                 f"{C.NOFO_LIVE_NOTE} {C.FLAG_GRANT}")
    C.subsection(doc, "f",
                 f"The {C.PARTIES_COLLECTIVE} intend to deploy a fiber-to-the-home ({C.SPEED_FLOOR} "
                 f"or greater) network serving eligible locations within the {C.SERVICE_TERRITORY} "
                 f"in {C.GEOGRAPHY}, in a manner that preserves the {C.TRIBE_SHORT}'s grant "
                 f"stewardship and the {C.FEDERAL_INTEREST} while giving {C.OPERATOR_SHORT} the "
                 f"operational control necessary to build, operate, and serve.")

    C.section(doc, "1.2", "Structure of the Transaction",
              f"This Agreement is the umbrella (Master) agreement. It establishes the shared "
              f"glossary, governance, order of precedence, and cross-cutting terms for the "
              f"coordinated set of {C.AGREEMENTS['master']} and related Definitive Agreements, "
              f"Schedules, Exhibits, Certificates, and Operational Forms described in Article 4. "
              f"Each subordinate instrument incorporates this Agreement by reference and is "
              f"subject to the order of precedence in Article 5.")

    # ---- ARTICLE 2 : Definitions (SHARED GLOSSARY) -----------------------
    C.article(doc, 2, "Definitions")
    C.section(doc, "2.1", "Shared Glossary",
              f"This Article 2 is the single shared definitions source for the entire package. "
              f"{C.SHARED_DEFINITIONS_RULE} Capitalized terms have the meanings set forth below; "
              f"terms defined elsewhere in this Agreement have the meanings there given.")

    defs = [
        ("Active Subscriber",
         f"a location within the {C.SERVICE_TERRITORY} receiving provisioned, billable retail "
         f"broadband service, counted and measured as set forth in the {C.AGREEMENTS['retail']} "
         f"and Schedule S8, including that activation is dated to first successful service "
         f"provisioning and disconnection to service cease; that one location with multiple "
         f"services counts as a single {C.ACTIVE_SUBSCRIBER} unless separately agreed; and that "
         f"the count is net of credits, refunds, and uncollectible amounts and exclusive of taxes "
         f"and regulatory fees. {C.FLAG_BUSINESS}"),
        ("Approved Project Area",
         f"the geographic area, and the eligible locations within it, approved for the project "
         f"under the Award and the approved application, as set forth in Schedule S2. "
         f"{C.PH('specific routes, census blocks/eligible locations — NOT SUPPLIED')} {C.FLAG_GRANT}"),
        ("Award",
         f"the executed federal financial-assistance award to the {C.TRIBE_SHORT} under the "
         f"{C.PROGRAM_SHORT}, including the controlling {C.NOFO_SHORT}, the Specific Award "
         f"Conditions, the approved application, budget, routes, and service commitments, and any "
         f"later written {C.AGENCY_SHORT}/{C.DOC_FULL} determination. "
         f"{C.PH('award number — NOT SUPPLIED; do not invent')} {C.FLAG_GRANT}"),
        ("Definitive Agreements",
         "this Agreement and the other agreements listed in Article 4, collectively, together "
         "with their Schedules, Exhibits, Certificates, and Operational Forms."),
        ("Demarcation Point",
         f"the physical and logical point of demarcation between the {C.TRIBAL_ASSETS} and the "
         f"{C.OPERATOR_EXISTING} (or subscriber-side equipment), as fixed for each segment in "
         f"Schedule S4 and confirmed at {C.ACTIVE_SUBSCRIBER} installation."),
        ("Federal Interest",
         f"the federal interest in real and personal property acquired or improved with Award "
         f"funds, arising under {C.CITES['real_property']}, {C.CITES['equipment']}, and "
         f"{C.CITES['intangible']}, and the property trust relationship under {C.CITES['trust']}, "
         f"for the applicable Federal Interest period."),
        ("Grant-Funded Assets",
         f"the infrastructure, equipment, and intangible property acquired or improved with Award "
         f"funds and owned by the {C.TRIBE_SHORT}, comprising the {C.NETWORK}, as registered in "
         f"Schedule S3. {C.TRIBAL_ASSETS} are subject to the {C.FEDERAL_INTEREST} and the "
         f"disposition rules of 2 CFR Part 200."),
        ("LREMC",
         f"{C.LREMC_FULL}, the separate owner of the {C.LREMC_ASSETS}. {C.LREMC_SHORT} is not a "
         f"Party to this Agreement."),
        ("LREMC Facilities",
         f"the poles, conduit, fiber, easements, rights-of-way, huts, power, sites, land, and "
         f"related facilities owned or controlled by {C.LREMC_SHORT}, made available (if at all) "
         f"only under the {C.AGREEMENTS['land']} and a separate {C.LREMC_SHORT} consent or "
         f"joinder, and never assumed to be owned or controlled by {C.OPERATOR_SHORT}."),
        ("Lumbee Tribe",
         f"{C.TRIBE_FULL}, the award recipient and grant steward, or {C.TRIBE_ENTITY_ALT}, as "
         f"confirmed in Schedule S1."),
        ("Point of Interconnection",
         f"the point(s) at which the {C.NETWORK} interconnects with the {C.OPERATOR_EXISTING} "
         f"or third-party networks for transport, as set forth in the "
         f"{C.AGREEMENTS['interconnect']} and Schedule S4."),
        ("Program Income",
         f"gross income earned that is directly generated by an Award-supported activity or "
         f"earned as a result of the Award, as determined under {C.CITES['prog_income']}; "
         f"characterization is provisional and {C.DEAL['program_income_note']}. {C.FLAG_GRANT}"),
        ("RIVR Tech",
         f"{C.OPERATOR_FULL}, the design/engineering/procurement/construction party, operator, and "
         f"retail provider of record."),
        ("RIVR Tech Existing Network",
         f"the fiber, core, transport, network operations center, billing, and related systems and "
         f"facilities owned by {C.OPERATOR_SHORT} prior to and independent of the Award, which "
         f"remain {C.OPERATOR_SHORT}'s property. Any use of, or reliance on, the "
         f"{C.OPERATOR_EXISTING} in connection with the project is identified, valued, and "
         f"cost-allocated under Schedule S10 and the {C.AGREEMENTS['interconnect']}, and is never "
         f"provided free of charge; grant-funded capacity is never furnished as free commercial "
         f"capacity. {C.FLAG_GRANT}"),
        ("Schedules",
         "the numbered Schedules S1 through S14 listed in Article 4, as they may be completed and "
         "amended in accordance with this Agreement."),
        ("Tribal Network",
         f"the {C.SPEED_FLOOR}-or-greater fiber-to-the-home network comprising the "
         f"{C.TRIBAL_ASSETS}, owned by the {C.TRIBE_SHORT} and operated by {C.OPERATOR_SHORT} "
         f"under the Definitive Agreements."),
        ("Effective Date",
         f"the date first written above; {C.PH('Effective Date — to be inserted upon execution')}."),
        ("Essential Services",
         "the broadband and voice services the interruption of which would imminently threaten "
         "public safety, continuity of critical communications, or compliance with the Award, as "
         "further described in the O&M and transition instruments."),
    ]
    for term, meaning in defs:
        C.subsection(doc, "▪", f"“{term}” means {meaning}")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "This glossary is a working set. Counsel and the grant administrator must reconcile "
                "each defined term against the controlling Award, the approved application, and the "
                "other Definitive Agreements before execution. Additional defined terms (e.g., "
                "Segment, Substantial Completion, Final Completion, Notice to Proceed, IRU, "
                "Disallowed Cost) are defined in context in this Agreement and the subordinate "
                "instruments and carry those meanings package-wide.")

    # ---- ARTICLE 3 : Purpose, Relationship -------------------------------
    C.article(doc, 3, "Purpose, Relationship, and Independent Status")
    C.section(doc, "3.1", "Purpose",
              f"The {C.PARTIES_COLLECTIVE} enter into this Agreement to coordinate the design, "
              f"construction, ownership, operation, and retail provision of the {C.NETWORK} in a "
              f"manner that (a) preserves the {C.TRIBE_SHORT}'s role as recipient and steward of "
              f"the Award and protects the {C.FEDERAL_INTEREST}; (b) gives {C.OPERATOR_SHORT} the "
              f"operational control necessary to perform; and (c) separates grant-funded activity "
              f"and assets from commercial activity and assets.")
    C.section(doc, "3.2", "Relationship of the Parties",
              f"The {C.PARTIES_COLLECTIVE} are independent contracting parties. Nothing in the "
              f"Definitive Agreements creates a partnership, joint venture, agency, or fiduciary "
              f"relationship except as expressly stated, and neither {C.PARTY_SINGULAR} may bind "
              f"the other except as expressly authorized. Use of the words “partnership” "
              f"or “partner” is for convenience and does not create a legal partnership.")
    C.section(doc, "3.3", "Separation of Grant and Commercial Activity",
              f"The {C.PARTIES_COLLECTIVE} will at all times maintain a clear separation between "
              f"(a) the {C.TRIBAL_ASSETS} and Award-funded activity, and (b) the "
              f"{C.OPERATOR_EXISTING} and {C.OPERATOR_SHORT}'s commercial activity, including "
              f"separate books, records, and cost allocation sufficient to demonstrate that "
              f"grant-funded capacity is not provided as free commercial capacity and that "
              f"commercial use does not receive an unallowable federal subsidy (Schedule S10; "
              f"{C.AGREEMENTS['finance']}). {C.FLAG_GRANT}")

    # ---- ARTICLE 4 : Package Architecture --------------------------------
    C.article(doc, 4, "The Definitive Agreements, Schedules, and Package Architecture")
    C.section(doc, "4.1", "Definitive Agreements",
              "This Agreement is executed together with the following coordinated agreements, "
              "each incorporated by reference and subject to the order of precedence in Article 5:")
    ag_rows = [[k.upper(), C.AGREEMENTS[k]] for k in C.AGREEMENTS]
    C.add_table(doc, ["Ref.", "Definitive Agreement (verbatim title)"], ag_rows,
                widths=[1.1, 5.4], col_align=["c", "l"])
    C.para(doc,
           f"The subordinate agreements include the {C.AGREEMENTS['depc']}; the "
           f"{C.AGREEMENTS['iru']}; the {C.AGREEMENTS['interconnect']}; the {C.AGREEMENTS['om']}; "
           f"the {C.AGREEMENTS['retail']}; the {C.AGREEMENTS['finance']}; the "
           f"{C.AGREEMENTS['land']}; the {C.AGREEMENTS['privacy']}; and the "
           f"{C.AGREEMENTS['transition']}.")
    C.section(doc, "4.2", "Schedules",
              "The following Schedules are incorporated into and form part of the Definitive "
              "Agreements. Blank or bracketed schedule content must be completed and reconciled to "
              "the Award before the affected clauses are finalized:")
    sch_rows = [[k, C.SCHEDULES[k]] for k in C.SCHEDULES]
    C.add_table(doc, ["Sched.", "Subject Matter (verbatim title)"], sch_rows,
                widths=[0.9, 5.6], col_align=["c", "l"])
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Each Schedule is a working shell pending the controlling Award and source "
                "documents; none may be treated as final until completed and reviewed.")

    # ---- ARTICLE 5 : Order of Precedence & Shared Definitions ------------
    precedence_and_shared_defs(doc, 5, first_agreement=True)

    # ---- ARTICLE 6 : Representations and Warranties ----------------------
    C.article(doc, 6, "Representations and Warranties")
    C.section(doc, "6.1", "Mutual Representations",
              f"Each {C.PARTY_SINGULAR} represents and warrants that it is duly organized and "
              f"validly existing; that, subject to the conditions precedent in Article 10 and to "
              f"all required governmental and Tribal approvals, it has (or upon such approvals will "
              f"have) the power and authority to enter into and perform the Definitive Agreements; "
              f"and that its execution has been duly authorized. {C.FLAG_ATTORNEY} Authority is "
              f"subject to the authorizing resolutions and approvals in Schedule S1 and "
              f"Schedule S14.")
    C.section(doc, "6.2", "Lumbee Tribe Representations",
              f"The {C.TRIBE_SHORT} represents, to its knowledge and subject to confirmation "
              f"against the controlling Award, that it is (or expects to be) the recipient of the "
              f"Award and that it does not warrant any award number, routes, prices, useful life, "
              f"approvals, land rights, or consents not yet supplied. {C.FLAG_GRANT} "
              f"{C.PH('Tribal-specific representations to be confirmed against the Award')}")
    C.section(doc, "6.3", "RIVR Tech Representations",
              f"{C.OPERATOR_SHORT} represents that it owns and operates the {C.OPERATOR_EXISTING}; "
              f"that it is not debarred or suspended ({C.CITES['debarment']}); that it will comply "
              f"with the flow-down requirements of Article 11; and that it does not represent any "
              f"ownership or control of the {C.LREMC_ASSETS}. {C.FLAG_ATTORNEY}")
    C.section(doc, "6.4", "No Reliance on Unsupplied Facts",
              f"Because no controlling Award or source documents have been supplied, no "
              f"{C.PARTY_SINGULAR} makes any representation as to award amount, eligible locations, "
              f"routes, pricing, useful life, or approvals; all such matters are "
              f"{C.PH('to be confirmed against the Award')} and are subject to Article 10. "
              f"{C.FLAG_GRANT}")

    # ---- ARTICLE 7 : Governance ------------------------------------------
    C.article(doc, 7, "Governance, Steering Committee, and Escalation")
    C.section(doc, "7.1", "Steering Committee",
              f"The {C.PARTIES_COLLECTIVE} will establish a Steering Committee with equal "
              f"representation from the {C.TRIBE_SHORT} and {C.OPERATOR_SHORT} to oversee "
              f"coordination, review progress against Schedule S2 milestones, and address disputes "
              f"below the level requiring formal dispute resolution. "
              f"{C.PH('committee size, members, and quorum')} {C.FLAG_BUSINESS}")
    C.section(doc, "7.2", "Meetings and Reporting",
              f"The Steering Committee will meet not less than {C.PH('frequency, e.g., monthly')} "
              f"and receive reporting sufficient for the {C.TRIBE_SHORT} to discharge its "
              f"stewardship and reporting obligations under the Award and Article 9.")
    C.section(doc, "7.3", "Escalation",
              f"Matters not resolved by the Steering Committee within {C.PH('number')} business "
              f"days escalate to the Parties' respective executive sponsors, and thereafter to the "
              f"dispute-resolution process in Article 24. Escalation does not stay any Award-"
              f"compliance obligation or the {C.TRIBE_SHORT}'s reserved decisions under "
              f"Article 8.")

    # ---- ARTICLE 8 : Roles and Reserved Decisions ------------------------
    C.article(doc, 8, "Roles, Responsibilities, and Reserved Decisions")
    C.section(doc, "8.1", "RIVR Tech Operational Control",
              f"Subject to the {C.TRIBE_SHORT}'s reserved decisions and the Award, "
              f"{C.OPERATOR_SHORT} has operational control over the design, construction, "
              f"operation, maintenance, and retail provision of the {C.NETWORK}, as detailed in "
              f"the {C.AGREEMENTS['depc']}, {C.AGREEMENTS['om']}, and {C.AGREEMENTS['retail']}.")
    C.section(doc, "8.2", "Reserved Decisions of the Lumbee Tribe",
              f"The following decisions are reserved to the {C.TRIBE_SHORT} as recipient and "
              f"steward and may not be made or overridden by {C.OPERATOR_SHORT}:")
    for d in [
        "acceptance of, and any change to, the Award, the approved application, budget, routes, "
        "and service commitments, and all communications with NTIA/DOC on Award matters;",
        f"any disposition, encumbrance, lien, or transfer of, or grant of any interest in, the "
        f"{C.TRIBAL_ASSETS} or any asset subject to the {C.FEDERAL_INTEREST};",
        "any determination affecting the property trust relationship, program-income treatment, "
        "or federal-interest release;",
        "matters implicating Tribal sovereignty, any waiver of sovereign immunity, and governing-"
        "law/forum elections (Article 24);",
        f"approval of the {C.SERVICE_TERRITORY}, eligible-location list, and any commercial or "
        f"non-project use of the {C.TRIBAL_ASSETS} (Schedule S10).",
    ]:
        C.numbered(doc, d)
    C.flag_para(doc, C.FLAG_GRANT,
                "Reserved decisions must be reconciled with the Award, 2 CFR Part 200 property and "
                "program-income rules, and any NTIA prior-approval requirements.")

    # ---- ARTICLE 9 : Grant-Recipient Authority & Stewardship -------------
    C.article(doc, 9, "Grant-Recipient Authority and Stewardship")
    C.section(doc, "9.1", "Recipient Responsibility",
              f"The {C.TRIBE_SHORT} retains ultimate responsibility to NTIA/DOC for the Award, "
              f"including performance, reporting, financial management, and property stewardship. "
              f"No delegation of operational functions to {C.OPERATOR_SHORT} relieves the "
              f"{C.TRIBE_SHORT} of, or transfers, that recipient responsibility.")
    C.section(doc, "9.2", "Property Stewardship",
              f"The {C.TRIBAL_ASSETS} are held and used in accordance with {C.CITES['real_property']}, "
              f"{C.CITES['equipment']}, {C.CITES['intangible']}, and the property trust "
              f"relationship under {C.CITES['trust']}. {C.OPERATOR_SHORT} operates the "
              f"{C.TRIBAL_ASSETS} as a custodian for the {C.TRIBE_SHORT} and acquires no ownership "
              f"interest therein. {C.FLAG_GRANT}")
    C.section(doc, "9.3", "No Liens or Attachment",
              f"No {C.PARTY_SINGULAR} may create, permit, or suffer any lien, security interest, "
              f"levy, attachment, or encumbrance against the {C.TRIBAL_ASSETS} or any trust, "
              f"restricted, or {C.FEDERAL_INTEREST} asset. {C.OPERATOR_SHORT} will keep such "
              f"assets free of all claims arising from its acts and will discharge any such lien "
              f"promptly. {C.FLAG_ATTORNEY}")
    C.section(doc, "9.4", "Records and Access",
              f"Each {C.PARTY_SINGULAR} will maintain records and provide access consistent with "
              f"{C.CITES['records']}, retaining records for not less than "
              f"{C.DEAL['records_retention_years']} years measured from submission of the final "
              f"report, and will cooperate with audit on not less than "
              f"{C.DEAL['audit_notice_business_days']} business days' notice (or immediately where "
              f"required by law or the Award).")

    # ---- ARTICLE 10 : Conditions Precedent (segment-level) ---------------
    C.article(doc, 10, "Conditions Precedent (Segment-Level)")
    C.section(doc, "10.1", "No Activity Until Conditions Met",
              f"No design finalization for construction, construction, ground disturbance, IRU "
              f"activation, or service activation may occur for any {C.NETWORK} segment until all "
              f"of the following conditions have been satisfied (or expressly waived in writing by "
              f"the Party entitled to the benefit, and, where required, by NTIA/DOC) for that "
              f"segment:")
    for cp in [
        "confirmed funding and budget authority for the segment under the Award;",
        f"completed procurement in compliance with {C.CITES['procurement']} and domestic-"
        f"preference/BABA requirements;",
        f"completed environmental and historic-preservation review and clearances under "
        f"{C.CITES['nepa']} and {C.CITES['nhpa']} before any ground disturbance;",
        f"secured land, easement, right-of-way, pole, site, and power rights for the segment "
        f"under the {C.AGREEMENTS['land']}, including any required {C.LREMC_SHORT} consent or "
        f"joinder and any approvals for trust/restricted land ({C.CITES['indian_leasing']}, "
        f"{C.CITES['indian_row']}, {C.CITES['bia_approval']});",
        "all required permits and authorizations for the segment;",
        f"insurance in force meeting Schedule S12 and Article 15;",
        "all required federal, Tribal, corporate, landowner, lender, and regulatory approvals "
        "(Schedule S14); and",
        "issuance of a Notice to Proceed for the segment.",
    ]:
        C.numbered(doc, cp)
    C.section(doc, "10.2", "Segment-by-Segment Application",
              f"Conditions precedent apply on a segment-by-segment basis; satisfaction for one "
              f"segment does not satisfy them for another. Segment acceptance under the "
              f"{C.AGREEMENTS['depc']} triggers the Term and IRU activation for that segment only "
              f"(Article 22; {C.AGREEMENTS['iru']}).")
    C.flag_para(doc, C.FLAG_GRANT,
                "The condition list must be reconciled to the Specific Award Conditions and any "
                "NTIA prior-approval or pre-construction requirements before finalization.")

    # ---- ARTICLE 11 : Compliance Flow-Downs ------------------------------
    C.article(doc, 11, "Compliance Flow-Downs")
    C.section(doc, "11.1", "Uniform Guidance",
              f"{C.OPERATOR_SHORT} will comply with, and flow down to its subcontractors, the "
              f"applicable requirements of {C.CITES['ug_part']}, as revised "
              f"({C.CITES['ug_2024']}), including cost principles ({C.CITES['allowable']}), "
              f"procurement standards ({C.CITES['procurement']}), and audit requirements "
              f"({C.CITES['single_audit']}). {C.FLAG_GRANT}")
    C.section(doc, "11.2", "Domestic Preference and Build America, Buy America",
              f"All procurement is subject to domestic-preference requirements ("
              f"{C.CITES['domestic']}) and the {C.CITES['baba']}.")
    C.section(doc, "11.3", "Prohibited Telecommunications Equipment",
              f"No covered telecommunications equipment or services may be procured, used, or "
              f"extended, consistent with {C.CITES['telecom_ban']} (Section 889).")
    C.section(doc, "11.4", "Environmental and Historic Preservation",
              f"All activity is subject to {C.CITES['nepa']} and {C.CITES['nhpa']}; required "
              f"reviews and clearances must be completed before ground disturbance (Article 10).")
    C.section(doc, "11.5", "Records, Disclosures, and Debarment",
              f"The {C.PARTIES_COLLECTIVE} will comply with record-retention and access rules "
              f"({C.CITES['records']}), mandatory disclosures ({C.CITES['disclosures']}), and "
              f"debarment/suspension rules ({C.CITES['debarment']}).")
    C.section(doc, "11.6", "Conflict of Interest",
              f"The {C.PARTIES_COLLECTIVE} will maintain written standards of conduct and manage "
              f"organizational and personal conflicts of interest consistent with "
              f"{C.CITES['conflict']} and {C.CITES['oci']}, recognizing the affiliation between "
              f"{C.OPERATOR_SHORT} and {C.LREMC_SHORT}. {C.FLAG_GRANT}")

    # ---- ARTICLE 12 : Contractor vs. Subrecipient ------------------------
    C.article(doc, 12, "Contractor Versus Subrecipient Determination")
    C.section(doc, "12.1", "Preliminary Characterization",
              f"For purposes of these preliminary drafts, the {C.PARTIES_COLLECTIVE} anticipate "
              f"that {C.OPERATOR_SHORT} is engaged as a contractor (procurement relationship) "
              f"rather than a subrecipient, under {C.CITES['subrecipient']}, because "
              f"{C.OPERATOR_SHORT} provides goods and services within its normal business "
              f"operations, in a competitive environment, for the benefit of the "
              f"{C.TRIBE_SHORT}'s Award-funded program, and does not itself determine eligibility "
              f"or administer the federal program.")
    C.section(doc, "12.2", "Substance Over Form; Deferred Analysis",
              f"The determination turns on the substance of the relationship, not its label, and "
              f"must be confirmed by the Phase-1 diligence analysis and reflected in the "
              f"{C.AGREEMENTS['finance']}. Where a subrecipient relationship is determined, the "
              f"pass-through requirements of {C.CITES['pass_through']} apply. {C.FLAG_GRANT} "
              f"{C.FLAG_ATTORNEY}")

    # ---- ARTICLE 13 : Change Control -------------------------------------
    C.article(doc, 13, "Change Control")
    C.section(doc, "13.1", "Change Control Process",
              f"Changes to scope, routes, schedule, price, or the Definitive Agreements are made "
              f"only through a written change process. Changes affecting the Award, the "
              f"{C.SERVICE_TERRITORY}, the {C.TRIBAL_ASSETS}, or the {C.FEDERAL_INTEREST} require "
              f"the {C.TRIBE_SHORT}'s reserved-decision approval (Article 8) and, where required, "
              f"NTIA/DOC prior approval. Construction change orders are processed under the "
              f"{C.AGREEMENTS['depc']} and the Operational Forms (Document 04).")
    C.section(doc, "13.2", "No Unauthorized Changes",
              f"No change is effective, and no cost arising from an unauthorized change is "
              f"allowable or payable, unless approved under this Article. {C.FLAG_GRANT}")

    # ---- ARTICLE 14 : Confidentiality ------------------------------------
    C.article(doc, 14, "Confidentiality")
    C.section(doc, "14.1", "Confidential Information",
              f"Each {C.PARTY_SINGULAR} will protect the other's confidential information and use "
              f"it only for the purposes of the Definitive Agreements.")
    C.section(doc, "14.2", "Subject to Audit and Public Law",
              f"Confidentiality is subject to, and does not override, (a) federal audit and access "
              f"rights ({C.CITES['records']}); (b) NTIA/DOC oversight and reporting; and (c) any "
              f"public-records, Tribal-law, or freedom-of-information obligations applicable to the "
              f"{C.TRIBE_SHORT}. {C.FLAG_ATTORNEY} Subscriber information is additionally subject "
              f"to {C.CITES['cpni']} and the {C.AGREEMENTS['privacy']}.")

    # ---- ARTICLE 15 : Publicity and Branding -----------------------------
    C.article(doc, 15, "Publicity and Branding")
    C.section(doc, "15.1", "Award Attribution",
              f"Public communications will accurately attribute Award funding to the "
              f"{C.PROGRAM_SHORT}/{C.AGENCY_SHORT} as required by the Award, and will not imply "
              f"that {C.OPERATOR_SHORT} owns the {C.TRIBAL_ASSETS} or the Award. "
              f"{C.PH('required funding-attribution language from the Award')} {C.FLAG_GRANT}")
    C.section(doc, "15.2", "Use of Names and Marks",
              f"Neither {C.PARTY_SINGULAR} may use the other's, or the {C.TRIBE_SHORT}'s, names, "
              f"marks, or the {C.LREMC_SHORT} name without prior written consent, except as "
              f"required by the Award or law. {C.FLAG_BUSINESS}")

    # ---- ARTICLE 16 : Insurance ------------------------------------------
    C.article(doc, 16, "Insurance")
    C.section(doc, "16.1", "Required Coverage",
              f"{C.OPERATOR_SHORT} will procure and maintain, and cause its subcontractors to "
              f"maintain, insurance consistent with {C.CITES['insurance']}, Schedule S12, and the "
              f"Insurance Exhibit, in not less than the following limits (subject to confirmation "
              f"against the Award and the {C.TRIBE_SHORT}'s requirements):")
    ins = C.DEAL["insurance"]
    ins_rows = [
        ["Commercial General Liability (per occurrence)", ins["cgl_occurrence"]],
        ["Commercial General Liability (aggregate)", ins["cgl_aggregate"]],
        ["Automobile Liability", ins["auto"]],
        ["Umbrella / Excess Liability", ins["umbrella"]],
        ["Workers' Compensation", ins["workers_comp"]],
        ["Employer's Liability", ins["employers_liability"]],
        ["Professional / Technology E&O", ins["professional_tech_eo"]],
        ["Cyber Liability", ins["cyber"]],
        ["Property / Builder's Risk", ins["property_builders_risk"]],
        ["Contractor's Pollution Liability", ins["pollution"]],
    ]
    C.add_table(doc, ["Coverage", "Minimum Limit"], ins_rows,
                widths=[4.3, 2.2], col_align=["l", "c"])
    C.section(doc, "16.2", "Additional Insured; Waiver; Certificates",
              f"The {C.TRIBE_SHORT} (and, where required, NTIA/DOC and {C.LREMC_SHORT}) will be "
              f"named as additional insured as their interests appear; certificates and endorsements "
              f"will be provided before any Notice to Proceed. {C.FLAG_ATTORNEY}")

    # ---- ARTICLE 17 : Indemnification ------------------------------------
    C.article(doc, 17, "Indemnification")
    C.section(doc, "17.1", "RIVR Tech Indemnity",
              f"{C.OPERATOR_SHORT} will indemnify, defend, and hold harmless the {C.TRIBE_SHORT} "
              f"(and its officials, officers, employees, and agents) from third-party claims, "
              f"losses, and liabilities to the extent arising from {C.OPERATOR_SHORT}'s breach, "
              f"negligence, willful misconduct, or noncompliance with the Award or applicable law, "
              f"including any Disallowed Cost caused thereby. {C.FLAG_ATTORNEY}")
    C.section(doc, "17.2", "Allocation and Sovereignty",
              f"Indemnity is allocated according to fault and control and does not, by itself, "
              f"waive or diminish the {C.TRIBE_SHORT}'s sovereign immunity, which is addressed only "
              f"under Article 24. {C.PH('reciprocal or limited Tribal indemnity, if any')} "
              f"{C.FLAG_ATTORNEY}")

    # ---- ARTICLE 18 : Limitation of Liability ----------------------------
    C.article(doc, 18, "Limitation of Liability")
    C.section(doc, "18.1", "Liability Tied to Control and Breach",
              f"Except for indemnity obligations, liability for Disallowed Costs, breaches of "
              f"confidentiality, and a Party's gross negligence or willful misconduct, each Party's "
              f"liability is limited as set forth in Schedule S12, and is tied to the Party's "
              f"control over, breach of, or noncompliance with the relevant obligation. "
              f"{C.PH('liability cap methodology and amount')} {C.FLAG_BUSINESS} {C.FLAG_ATTORNEY}")
    C.section(doc, "18.2", "Consequential Damages",
              "Neither Party is liable for indirect, incidental, or consequential damages except "
              "as expressly provided, subject to counsel's review against the Award and applicable "
              "law.")

    # ---- ARTICLE 19 : Force Majeure --------------------------------------
    C.article(doc, 19, "Force Majeure")
    C.section(doc, "19.1", "Excused Delay",
              "Neither Party is liable for failure or delay in performance (other than payment "
              "obligations already due) caused by events beyond its reasonable control, provided it "
              "gives prompt notice, uses commercially reasonable efforts to mitigate, and resumes "
              "performance as soon as practicable.")
    C.section(doc, "19.2", "Award Compliance Not Excused",
              f"Force majeure does not excuse noncompliance with the Award or applicable federal "
              f"law; where a force-majeure event affects Award performance, the {C.TRIBE_SHORT} "
              f"will pursue any relief available from NTIA/DOC. {C.FLAG_GRANT}")

    # ---- ARTICLE 20 : Default and Cure -----------------------------------
    C.article(doc, 20, "Default and Cure")
    C.section(doc, "20.1", "Events of Default",
              f"An event of default occurs upon a material breach not cured within the applicable "
              f"cure period, insolvency, or a persistent failure to comply with the Award after "
              f"notice.")
    C.section(doc, "20.2", "Cure Periods",
              f"A defaulting Party has {C.DEAL['cure_monetary_days']} days to cure a monetary "
              f"default and {C.DEAL['cure_nonmonetary_days']} days to cure a non-monetary default "
              f"after written notice, with {C.DEAL['cure_nonmonetary_extension']}. Notice of "
              f"default is given not less than {C.DEAL['notice_default_days']} days before "
              f"exercising remedies, except where immediate action is required to protect "
              f"Essential Services, public safety, or Award compliance.")
    C.section(doc, "20.3", "Remedies and Noncompliance",
              f"Remedies are cumulative and are exercised consistent with {C.CITES['remedies']}. A "
              f"Disallowed Cost or noncompliance caused by a Party is that Party's responsibility, "
              f"subject to notice and cure. {C.FLAG_GRANT}")

    # ---- ARTICLE 21 : Suspension -----------------------------------------
    C.article(doc, 21, "Suspension")
    C.section(doc, "21.1", "Suspension of Work",
              f"The {C.TRIBE_SHORT} may suspend affected work upon notice where continued "
              f"performance would violate the Award or applicable law, threaten the "
              f"{C.FEDERAL_INTEREST}, or where NTIA/DOC directs suspension. Suspension is limited "
              f"to the affected scope and duration and does not, by itself, terminate the "
              f"Definitive Agreements.")

    # ---- ARTICLE 22 : Step-In --------------------------------------------
    C.article(doc, 22, "Step-In Rights")
    C.section(doc, "22.1", "Step-In to Preserve Continuity",
              f"Where necessary to preserve Essential Services, protect public safety, or maintain "
              f"Award compliance, the {C.TRIBE_SHORT} (or its designee) may step in "
              f"({C.DEAL['stepin_emergency']}), as detailed in the {C.AGREEMENTS['transition']} "
              f"and Schedule S13. Step-in is temporary, proportionate, and without prejudice to "
              f"other remedies. {C.FLAG_ATTORNEY}")

    # ---- ARTICLE 23 : Term and Renewal -----------------------------------
    C.article(doc, 23, "Term and Renewal")
    C.section(doc, "23.1", "Term",
              f"The term for each {C.NETWORK} segment is {C.DEAL['iru_term_recommended']} years "
              f"commencing on {C.DEAL['term_trigger']}, subject to {C.DEAL['iru_renewal']}, and in "
              f"no event extending beyond {C.DEAL['term_ceiling_note']}.")
    C.section(doc, "23.2", "Renewal Conditions",
              f"Each renewal is subject to continued compliance with the Award and applicable law, "
              f"the {C.TRIBE_SHORT}'s reserved decisions, and the availability of the underlying "
              f"land/access rights and useful life. {C.FLAG_BUSINESS}")

    # ---- ARTICLE 24 : Dispute Resolution / Sovereignty -------------------
    C.article(doc, 24, "Dispute Resolution, Tribal Sovereignty, and Limited Waiver of Sovereign Immunity")
    C.section(doc, "24.1", "Escalation and Negotiation",
              "The Parties will first attempt to resolve disputes through the escalation process "
              "in Article 7 before invoking any binding process.")
    C.section(doc, "24.2", "Tribal Sovereign Immunity — Alternatives Only",
              f"The {C.TRIBE_SHORT} possesses sovereign immunity, which is not waived except by an "
              f"express, written, and specifically authorized waiver. The following are bracketed "
              f"ALTERNATIVES for counsel; none is selected:")
    C.subsection(doc, "Alt. 1",
                 "[No waiver of sovereign immunity; disputes resolved by non-binding processes and "
                 "by the Parties' respective self-help and termination remedies only.]")
    C.subsection(doc, "Alt. 2",
                 "[Limited, express waiver of sovereign immunity solely for the purpose of binding "
                 "arbitration of contract disputes, limited to available insurance and specified "
                 "assets, expressly excluding the Grant-Funded Assets and any trust, restricted, or "
                 "Federal-Interest assets, and requiring authorization by "
                 f"{C.PH('the Tribal governing body by resolution')}.]")
    C.subsection(doc, "Alt. 3",
                 "[Limited, express waiver solely for a designated federal or state forum, with a "
                 "cap and asset carve-outs as in Alternative 2, subject to counsel's forum and "
                 "enforceability analysis.]")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                f"Sovereign immunity, any limited waiver, governing law, forum, and dispute-"
                f"resolution mechanism are reserved decisions of the {C.TRIBE_SHORT} and must be "
                f"drafted and authorized by counsel. See {C.CITES['sovereign_immunity']}. Any "
                f"waiver must be clear and express and must exclude the {C.TRIBAL_ASSETS} and "
                f"trust/restricted/Federal-Interest assets. Cross-reference the parallel provisions "
                f"in the governance/authorization instruments (Document 03) and the "
                f"{C.AGREEMENTS['transition']} (Document 04 forms).")
    C.section(doc, "24.3", "Governing Law and Forum — Alternatives Only",
              f"{C.PH('Governing law and forum — bracketed alternatives for counsel: Tribal law/forum; federal law/forum; or specified state law/forum')} {C.FLAG_ATTORNEY}")

    # ---- ARTICLE 25 : Assignment -----------------------------------------
    C.article(doc, 25, "Assignment, Change of Control, and Successors")
    C.section(doc, "25.1", "Restriction on Assignment",
              f"Neither Party may assign the Definitive Agreements, nor may {C.OPERATOR_SHORT} "
              f"undergo a change of control, without the other Party's prior written consent and, "
              f"where required, NTIA/DOC approval. Any assignment or change of control must "
              f"preserve the {C.FEDERAL_INTEREST}, the {C.TRIBE_SHORT}'s interests and reserved "
              f"decisions, and the flow-down obligations of Article 11. {C.FLAG_ATTORNEY} "
              f"{C.FLAG_GRANT}")
    C.section(doc, "25.2", "Successors Bound",
              "Permitted successors and assigns are bound by the Definitive Agreements, including "
              "the property, compliance, and non-lien provisions protecting the Grant-Funded "
              "Assets.")

    # ---- ARTICLE 26 : Survival -------------------------------------------
    C.article(doc, 26, "Survival")
    C.section(doc, "26.1", "Surviving Provisions",
              f"Provisions that by their nature survive expiration or termination — including "
              f"confidentiality, records and audit, indemnity, limitation of liability, non-lien "
              f"protection of the {C.TRIBAL_ASSETS}, program-income and closeout obligations "
              f"({C.CITES['closeout']}), dispute resolution, and sovereignty provisions — survive.")

    # ---- ARTICLE 27 : General Provisions ---------------------------------
    C.article(doc, 27, "General Provisions")
    C.section(doc, "27.1", "Severability and Reformation",
              "If any provision is held invalid or unenforceable, it is reformed to the minimum "
              "extent necessary to make it enforceable and consistent with the Award, and the "
              "remaining provisions continue in effect; a lawful construction and service provision "
              "is not invalidated by a rejected IRU, exclusivity, payment, or commercial-use term.")
    C.section(doc, "27.2", "Notices",
              f"Notices are in writing to the addresses in Schedule S1. "
              f"{C.PH('notice addresses and designated recipients')}")
    C.section(doc, "27.3", "Amendments",
              "Amendments are effective only in a writing signed by both Parties and, where "
              "required, approved by NTIA/DOC and by Tribal authorization.")
    C.section(doc, "27.4", "Counterparts and Electronic Signature",
              "This Agreement may be executed in counterparts and by electronic signature.")

    # ---- ARTICLE 28 : Entire Agreement -----------------------------------
    C.article(doc, 28, "Entire Agreement")
    C.section(doc, "28.1", "Integration",
              f"The Definitive Agreements, together with the Schedules, Exhibits, Certificates, "
              f"Operational Forms, and the Award, constitute the entire agreement of the Parties on "
              f"their subject matter and supersede prior understandings, subject to the order of "
              f"precedence in Article 5.")

    disclaimer_block(doc)
    C.signature_block(doc,
                      extra_note="Signatory authority, titles, and authorizing resolutions must be "
                      "confirmed in Schedule S1 and Schedule S14 before execution.")

    return C.save(doc, "02_Definitive_Agreements",
                  "01_Master_TBCP_Partnership_and_Implementation_Agreement.docx")


# ===========================================================================
#  DOCUMENT 2 — DESIGN, ENGINEERING, PROCUREMENT, AND CONSTRUCTION AGREEMENT
# ===========================================================================
def build_depc():
    doc = C.new_doc()
    C.add_cover(
        doc,
        "DOCUMENT 02.02 — DEFINITIVE AGREEMENTS",
        "Design, Engineering, Procurement, and Construction Agreement",
        "The DEPC agreement for the coordinated TBCP fiber-project package "
        "(subordinate to the Master Agreement)",
    )
    C.setup_header_footer(doc, "DEPC Agreement")
    C.add_toc(doc)
    C.status_banner(doc)
    C.spacer(doc, 1)

    # ---- ARTICLE 1 : Parties, Recitals, Incorporation --------------------
    C.article(doc, 1, "Parties, Recitals, and Incorporation")
    party_intro(doc, C.AGREEMENTS["depc"])
    C.section(doc, "1.1", "Incorporation of the Master Agreement",
              f"This Agreement is one of the Definitive Agreements and is subordinate to and "
              f"incorporates the {C.AGREEMENTS['master']}, including its Article 2 (Definitions), "
              f"the order of precedence, and the cross-cutting terms. In any conflict, the order of "
              f"precedence in Article 3 governs.")
    C.section(doc, "1.2", "Purpose",
              f"{C.OPERATOR_SHORT} will design, engineer, procure, and construct the "
              f"{C.NETWORK} (the {C.TRIBAL_ASSETS}) within the {C.SERVICE_TERRITORY}, on a "
              f"segment-by-segment basis, in compliance with the Award and applicable federal law, "
              f"for ownership by the {C.TRIBE_SHORT}.")
    C.section(doc, "1.3", "LREMC Facilities Not Conveyed",
              f"This Agreement does not convey, and does not assume {C.OPERATOR_SHORT} ownership or "
              f"control of, any {C.LREMC_ASSETS}. Use of {C.LREMC_ASSETS} (poles, conduit, "
              f"easements, huts, power, land) requires the {C.AGREEMENTS['land']} and a separate "
              f"{C.LREMC_SHORT} consent or joinder. {C.FLAG_ATTORNEY}")

    # ---- ARTICLE 2 : Definitions -----------------------------------------
    C.article(doc, 2, "Definitions")
    C.section(doc, "2.1", "Shared Definitions Govern",
              f"{C.SHARED_DEFINITIONS_RULE} This Agreement does not restate the shared glossary. "
              f"Terms defined below are unique to the design and construction subject matter of "
              f"this Agreement.")
    depc_defs = [
        ("Segment", "a defined portion of the Tribal Network designed, constructed, tested, and "
                    "accepted as a unit, as identified in Schedule S2."),
        ("Notice to Proceed",
         "the written authorization issued for a Segment after all segment-level conditions "
         "precedent are satisfied, authorizing construction to begin for that Segment."),
        ("Substantial Completion",
         "the point at which a Segment is sufficiently complete to be used for its intended "
         "purpose, subject only to punch-list items, as certified under Article 23."),
        ("Final Completion",
         "the point at which all work for a Segment, including punch-list items, as-builts, and "
         "required documentation, is complete and accepted under Article 23."),
        ("Segment Acceptance",
         "the Tribe's acceptance of a Segment following successful testing and completion, which "
         "triggers commencement of the Term and IRU activation for that Segment (Article 24)."),
        ("Disallowed Cost",
         "any cost determined by NTIA/DOC, audit, or the Award to be unallowable, unallocable, "
         "unreasonable, or unsupported under 2 CFR Part 200 or the Award."),
    ]
    for term, meaning in depc_defs:
        C.subsection(doc, "▪", f"“{term}” means {meaning}")

    # ---- ARTICLE 3 : Order of Precedence & Shared Definitions ------------
    precedence_and_shared_defs(doc, 3, first_agreement=False)

    # ---- ARTICLE 4 : Scope of Work ---------------------------------------
    C.article(doc, 4, "Scope of Work")
    C.section(doc, "4.1", "DEPC Services",
              f"{C.OPERATOR_SHORT} will provide all design, engineering, procurement, "
              f"construction, testing, and commissioning services necessary to deliver the "
              f"{C.TRIBAL_ASSETS} for each Segment, in accordance with the design standards "
              f"(Article 5), the approved routes (Article 6), and Schedules S2, S4, and S5.")
    C.section(doc, "4.2", "Segment-by-Segment Delivery",
              f"Work proceeds Segment by Segment. No work may begin on a Segment before its Notice "
              f"to Proceed (Article 29), and no ground disturbance may occur before environmental "
              f"and historic clearances (Article 13).")
    C.section(doc, "4.3", "Ownership of Work Product",
              f"The {C.TRIBAL_ASSETS}, including installed materials, designs, and as-builts funded "
              f"by the Award, are owned by the {C.TRIBE_SHORT} and are subject to the "
              f"{C.FEDERAL_INTEREST}; {C.OPERATOR_SHORT} acquires no ownership therein. The "
              f"{C.OPERATOR_EXISTING} remains {C.OPERATOR_SHORT}'s property. {C.FLAG_GRANT}")

    # ---- ARTICLE 5 : Design Standards ------------------------------------
    C.article(doc, 5, "Design Standards")
    C.section(doc, "5.1", "FTTH Architecture",
              f"The {C.NETWORK} is a fiber-to-the-home (FTTH) network delivering not less than "
              f"{C.SPEED_FLOOR} (and the higher speeds required by the Award), using a passive "
              f"optical network architecture. {C.PH('XGS-PON and/or GPON election and split ratios')} "
              f"{C.FLAG_TECH}")
    C.section(doc, "5.2", "Optical and Electronics Standards",
              f"Design will conform to recognized FTTH engineering standards and the bill of "
              f"materials in Schedule S4, using Calix-class (or approved-equivalent) access "
              f"electronics. {C.PH('specific OLT/ONT platforms, electronics, and firmware')} "
              f"{C.FLAG_TECH}")
    C.section(doc, "5.3", "Interconnection and Demarcation",
              f"Design will fix the {C.POI} and {C.DEMARCATION} for each Segment per Schedule S4 "
              f"and the {C.AGREEMENTS['interconnect']}, maintaining separation between the "
              f"{C.TRIBAL_ASSETS} and the {C.OPERATOR_EXISTING}.")
    C.section(doc, "5.4", "Design Review and Approval",
              f"Design deliverables are submitted for review; changes to approved routes or "
              f"standards follow change control (Article 18 and Master Article 13). "
              f"{C.FLAG_TECH}")

    # ---- ARTICLE 6 : Routes ----------------------------------------------
    C.article(doc, 6, "Routes and Approved Project Area")
    C.section(doc, "6.1", "Approved Routes",
              f"Construction follows the approved routes and eligible locations within the "
              f"{C.SERVICE_TERRITORY} as set forth in Schedule S2. "
              f"{C.PH('route maps, mileage, eligible-location list — NOT SUPPLIED; do not invent')} "
              f"{C.FLAG_GRANT}")
    C.section(doc, "6.2", "Route Changes",
              f"Any deviation from approved routes requires change control and, where it affects the "
              f"Award or {C.SERVICE_TERRITORY}, the {C.TRIBE_SHORT}'s reserved-decision approval and "
              f"any required NTIA/DOC approval. {C.FLAG_GRANT}")

    # ---- ARTICLE 7 : Bills of Materials ----------------------------------
    C.article(doc, 7, "Bills of Materials and Approved Manufacturers")
    C.section(doc, "7.1", "Bill of Materials",
              f"Materials and equipment conform to the bill of materials and approved-manufacturer "
              f"list in Schedule S4. {C.PH('final BOM and approved-manufacturer list')} {C.FLAG_TECH}")
    C.section(doc, "7.2", "Compliance of Materials",
              f"All materials and equipment comply with domestic-preference/BABA requirements "
              f"({C.CITES['baba']}; {C.CITES['domestic']}) and the Section 889 prohibition "
              f"({C.CITES['telecom_ban']}). Substitutions require approval and re-verification of "
              f"compliance. {C.FLAG_GRANT}")

    # ---- ARTICLE 8 : Estimates and Pricing -------------------------------
    C.article(doc, 8, "Estimates, Unit Pricing, and Milestone Pricing")
    C.section(doc, "8.1", "Pricing Basis",
              f"Construction pricing, unit prices, milestone payments, retainage, and warranties "
              f"are set forth in Schedule S5. {C.PH('unit prices, milestone schedule, GMP or unit-price basis — NOT SUPPLIED')} {C.FLAG_BUSINESS}")
    C.section(doc, "8.2", "Cost Reasonableness",
              f"All prices must be reasonable, allocable, and supportable under the cost principles "
              f"({C.CITES['allowable']}) and the procurement standards ({C.CITES['procurement']}). "
              f"{C.FLAG_GRANT}")

    # ---- ARTICLE 9 : Eligible-Cost Support -------------------------------
    C.article(doc, 9, "Eligible-Cost Support and Prohibition on Duplicate or Unsupported Charges")
    C.section(doc, "9.1", "Support for Eligible Costs",
              f"{C.OPERATOR_SHORT} will provide documentation sufficient to support eligible costs "
              f"for reimbursement under the {C.AGREEMENTS['finance']} and Schedule S8, consistent "
              f"with {C.CITES['allowable']} and {C.CITES['records']}.")
    C.section(doc, "9.2", "No Duplicate or Unsupported Charges",
              f"{C.OPERATOR_SHORT} will not charge to the Award any cost that is duplicated, "
              f"unsupported, attributable to the {C.OPERATOR_EXISTING} or commercial activity, or "
              f"otherwise unallowable. Costs associated with the {C.OPERATOR_EXISTING} are "
              f"identified, valued, and cost-allocated under Schedule S10 and are never charged to "
              f"the Award as if grant-funded, and grant-funded capacity is never furnished as free "
              f"commercial capacity. {C.FLAG_GRANT}")

    # ---- ARTICLE 10 : Subcontracting -------------------------------------
    C.article(doc, 10, "Subcontracting and Procurement Flow-Downs")
    C.section(doc, "10.1", "Procurement Standards",
              f"All procurement and subcontracting comply with {C.CITES['procurement']}, including "
              f"competition ({C.CITES['competition']}) and methods of procurement "
              f"({C.CITES['methods']}), and flow down applicable Award and 2 CFR Part 200 "
              f"requirements to subcontractors. {C.FLAG_GRANT}")
    C.section(doc, "10.2", "Conflicts and Debarment",
              f"{C.OPERATOR_SHORT} will manage conflicts of interest ({C.CITES['conflict']}, "
              f"{C.CITES['oci']}), including its affiliation with {C.LREMC_SHORT}, and will not "
              f"subcontract to debarred or suspended parties ({C.CITES['debarment']}).")

    # ---- ARTICLE 11 : Domestic Preference / BABA -------------------------
    C.article(doc, 11, "Domestic Preference and Build America, Buy America")
    C.section(doc, "11.1", "BABA Compliance",
              f"All iron, steel, manufactured products, and construction materials comply with the "
              f"{C.CITES['baba']} and domestic-preference requirements ({C.CITES['domestic']}), "
              f"unless a valid waiver applies. {C.PH('applicable BABA waivers, if any')} "
              f"{C.FLAG_GRANT}")

    # ---- ARTICLE 12 : Section 889 ----------------------------------------
    C.article(doc, 12, "Prohibited Telecommunications and Video Surveillance Equipment")
    C.section(doc, "12.1", "Section 889 Prohibition",
              f"No covered telecommunications equipment or services (Section 889) may be procured, "
              f"used, or extended, consistent with {C.CITES['telecom_ban']}. {C.OPERATOR_SHORT} "
              f"will represent and certify compliance and flow the prohibition down. {C.FLAG_GRANT}")

    # ---- ARTICLE 13 : Environmental / Historic ---------------------------
    C.article(doc, 13, "Environmental and Historic-Preservation Clearances")
    C.section(doc, "13.1", "Clearances Before Ground Disturbance",
              f"No ground-disturbing activity may occur on a Segment until required environmental "
              f"and historic-preservation reviews and clearances under {C.CITES['nepa']} and "
              f"{C.CITES['nhpa']} are completed for that Segment. {C.FLAG_GRANT}")
    C.section(doc, "13.2", "Unanticipated Discoveries",
              f"{C.OPERATOR_SHORT} will implement stop-work and notification procedures for "
              f"unanticipated archaeological or historic discoveries, consistent with "
              f"{C.CITES['nhpa']} and any tribal-monitoring requirements. "
              f"{C.PH('unanticipated-discovery and monitoring protocol')} {C.FLAG_ATTORNEY}")

    # ---- ARTICLE 14 : Permits --------------------------------------------
    C.article(doc, 14, "Permits and Authorizations")
    C.section(doc, "14.1", "Permits",
              f"{C.OPERATOR_SHORT} will obtain and maintain all required permits and authorizations "
              f"for each Segment (Schedule S9; Schedule S14), including any pole-attachment "
              f"({C.CITES['nc_pole']}), encroachment/ROW ({C.CITES['nc_ncdot']}), and utility-"
              f"locate ({C.CITES['nc_dig']}) requirements, and any approvals for trust/restricted "
              f"land ({C.CITES['indian_row']}, {C.CITES['bia_approval']}). {C.FLAG_ATTORNEY}")

    # ---- ARTICLE 15 : Safety ---------------------------------------------
    C.article(doc, 15, "Safety")
    C.section(doc, "15.1", "Safety Program",
              f"{C.OPERATOR_SHORT} will maintain a safety program compliant with applicable OSHA "
              f"and utility-safety requirements, including underground-utility damage prevention "
              f"({C.CITES['nc_dig']}), and coordinate with {C.LREMC_SHORT} for work in the vicinity "
              f"of {C.LREMC_ASSETS} and energized facilities. {C.FLAG_TECH}")

    # ---- ARTICLE 16 : Schedule and Milestones ----------------------------
    C.article(doc, 16, "Schedule and Milestones")
    C.section(doc, "16.1", "Project Schedule",
              f"{C.OPERATOR_SHORT} will perform in accordance with the schedule and milestones in "
              f"Schedule S2, including the Award's service-commitment and buildout deadlines. "
              f"{C.PH('milestone dates and buildout deadlines — per the Award')} {C.FLAG_GRANT}")

    # ---- ARTICLE 17 : Delay ----------------------------------------------
    C.article(doc, 17, "Delay")
    C.section(doc, "17.1", "Excusable and Non-Excusable Delay",
              f"Excusable delay (including force majeure per Master Article 19 and Owner-caused "
              f"delay) entitles {C.OPERATOR_SHORT} to an equitable time extension; non-excusable "
              f"delay may entitle the {C.TRIBE_SHORT} to remedies under Schedule S5. "
              f"{C.PH('liquidated damages or delay remedies, if any')} {C.FLAG_BUSINESS}")

    # ---- ARTICLE 18 : Change Orders --------------------------------------
    C.article(doc, 18, "Change Orders")
    C.section(doc, "18.1", "Change Order Process",
              f"Changes to scope, price, or schedule are made only by written change order using "
              f"the Construction Forms in Document 04, consistent with the change-control provisions "
              f"of the {C.AGREEMENTS['master']} (Master Article 13). Changes affecting the Award, "
              f"routes, or {C.SERVICE_TERRITORY} require the {C.TRIBE_SHORT}'s reserved-decision "
              f"approval and any NTIA/DOC approval. {C.FLAG_GRANT}")
    C.section(doc, "18.2", "No Payment for Unauthorized Changes",
              "No cost arising from an unauthorized change is payable or allowable.")

    # ---- ARTICLE 19 : Material Controls ----------------------------------
    C.article(doc, 19, "Material Controls and Stored Materials")
    C.section(doc, "19.1", "Custody and Title",
              f"{C.OPERATOR_SHORT} will maintain inventory and custody controls for materials, "
              f"including stored materials. Title to Award-funded materials vests in the "
              f"{C.TRIBE_SHORT} upon the earlier of payment or incorporation into the "
              f"{C.TRIBAL_ASSETS}, free of liens (Master Article 9). {C.PH('stored-materials payment and insurance conditions')} {C.FLAG_ATTORNEY}")

    # ---- ARTICLE 20 : Inspection -----------------------------------------
    C.article(doc, 20, "Inspection")
    C.section(doc, "20.1", "Right to Inspect",
              f"The {C.TRIBE_SHORT}, NTIA/DOC, and their representatives may inspect the work and "
              f"records at reasonable times ({C.CITES['records']}); inspection does not relieve "
              f"{C.OPERATOR_SHORT} of responsibility for compliant work.")

    # ---- ARTICLE 21 : Testing --------------------------------------------
    C.article(doc, 21, "Testing and Optical Acceptance")
    C.section(doc, "21.1", "Optical Testing",
              f"Each Segment is tested using {C.OPTICAL['otdr']} at {C.OPTICAL['wavelengths']}, "
              f"with results meeting the following loss and reflectance limits:")
    opt_rows = [
        ["Test method", f"{C.OPTICAL['otdr']} at {C.OPTICAL['wavelengths']}"],
        ["Fusion splice loss", C.OPTICAL["splice_loss_max"]],
        ["Mated connector loss", C.OPTICAL["connector_loss_max"]],
        ["Span loss budget", C.OPTICAL["span_margin"]],
        ["Reflectance (max)", C.OPTICAL["reflectance_max"]],
    ]
    C.add_table(doc, ["Parameter", "Acceptance Limit"], opt_rows,
                widths=[2.3, 4.2], col_align=["l", "l"])
    C.section(doc, "21.2", "Test Records",
              f"Bi-directional OTDR traces, power-meter readings, and test records are delivered as "
              f"part of the acceptance package and as-builts (Article 25). {C.FLAG_TECH}")

    # ---- ARTICLE 22 : Punch Lists ----------------------------------------
    C.article(doc, 22, "Punch Lists")
    C.section(doc, "22.1", "Punch-List Procedure",
              "At Substantial Completion, the Parties develop a punch list; punch-list items are "
              "completed before Final Completion and Segment Acceptance.")

    # ---- ARTICLE 23 : Completion -----------------------------------------
    C.article(doc, 23, "Substantial and Final Completion")
    C.section(doc, "23.1", "Substantial Completion",
              "Substantial Completion is certified when a Segment is usable for its intended "
              "purpose, subject only to punch-list items.")
    C.section(doc, "23.2", "Final Completion",
              "Final Completion is certified when all work, punch-list items, as-builts, test "
              "records, and required documentation are complete and accepted.")

    # ---- ARTICLE 24 : Segment Acceptance ---------------------------------
    C.article(doc, 24, "Segment Acceptance")
    C.section(doc, "24.1", "Acceptance and Its Effects",
              f"Upon Final Completion and satisfaction of acceptance criteria, the {C.TRIBE_SHORT} "
              f"issues Segment Acceptance for the Segment. Segment Acceptance (a) commences the "
              f"{C.DEAL['iru_term_recommended']}-year Term for that Segment (Master Article 23); "
              f"and (b) activates the IRU for that Segment under the {C.AGREEMENTS['iru']}, using "
              f"the Segment Activation Certificate in Document 04. {C.FLAG_GRANT}")
    C.section(doc, "24.2", "No Activation Before Acceptance",
              f"No IRU activation or service activation for a Segment may occur before Segment "
              f"Acceptance and satisfaction of all applicable conditions precedent (Master "
              f"Article 10).")

    # ---- ARTICLE 25 : As-Builts ------------------------------------------
    C.article(doc, 25, "As-Builts and GIS Records")
    C.section(doc, "25.1", "As-Built Deliverables",
              f"{C.OPERATOR_SHORT} will deliver as-built drawings, GIS records, and asset data for "
              f"each Segment in the format required by Schedule S4, for the {C.TRIBE_SHORT}'s "
              f"records and Award reporting. {C.PH('GIS/as-built format and data standard')} "
              f"{C.FLAG_TECH}")

    # ---- ARTICLE 26 : Warranties and Retainage ---------------------------
    C.article(doc, 26, "Warranties and Retainage")
    C.section(doc, "26.1", "Warranties",
              f"{C.OPERATOR_SHORT} warrants that the work is free from defects in materials and "
              f"workmanship for the warranty period in Schedule S5, and assigns manufacturer "
              f"warranties to the {C.TRIBE_SHORT}. {C.PH('warranty period and terms')} "
              f"{C.FLAG_BUSINESS}")
    C.section(doc, "26.2", "Retainage",
              f"Retainage is withheld and released as set forth in Schedule S5. "
              f"{C.PH('retainage percentage and release conditions')} {C.FLAG_BUSINESS}")

    # ---- ARTICLE 27 : Payment --------------------------------------------
    C.article(doc, 27, "Payment and Payment Evidence")
    C.section(doc, "27.1", "Payment Applications",
              f"Payment applications are supported by evidence sufficient for reimbursement under "
              f"the {C.AGREEMENTS['finance']} and Schedule S8, including lien waivers, test records, "
              f"and cost documentation ({C.CITES['records']}). {C.FLAG_GRANT}")
    C.section(doc, "27.2", "Conditions to Payment",
              "Payment is conditioned on compliant work, satisfactory documentation, and, for "
              "milestone payments, achievement of the milestone in Schedule S5.")

    # ---- ARTICLE 28 : Recovery for Defective/Disallowed Work -------------
    C.article(doc, 28, "Recovery for Defective or Disallowed Work")
    C.section(doc, "28.1", "RIVR Tech Responsibility",
              f"{C.OPERATOR_SHORT} is responsible, subject to notice and cure (Master Article 20), "
              f"for the cost of correcting defective work and for any Disallowed Cost caused by its "
              f"breach, negligence, or noncompliance, and will reimburse the {C.TRIBE_SHORT} for "
              f"such Disallowed Costs. {C.FLAG_GRANT} {C.FLAG_ATTORNEY}")

    # ---- ARTICLE 29 : Notice to Proceed ----------------------------------
    C.article(doc, 29, "Notice to Proceed")
    C.section(doc, "29.1", "Issuance",
              f"A Notice to Proceed is issued for a Segment only after all segment-level conditions "
              f"precedent (Master Article 10) are satisfied for that Segment, including funding, "
              f"procurement, environmental/historic clearances, land/permit rights, insurance, and "
              f"required approvals. Construction on a Segment may not begin before its Notice to "
              f"Proceed. {C.FLAG_GRANT}")

    # ---- ARTICLE 30 : General Provisions ---------------------------------
    C.article(doc, 30, "General Provisions")
    C.section(doc, "30.1", "Severability and Reformation",
              "If any provision is held invalid, it is reformed to the minimum extent necessary and "
              "the remainder continues; a lawful construction and service provision is not "
              "invalidated by a rejected commercial term.")
    C.section(doc, "30.2", "Dispute Resolution and Sovereignty",
              f"Dispute resolution, Tribal sovereignty, any limited waiver of sovereign immunity, "
              f"and governing law/forum are governed by Master Article 24 (bracketed ALTERNATIVES "
              f"only). {C.FLAG_ATTORNEY} See {C.CITES['sovereign_immunity']}.")
    C.section(doc, "30.3", "Amendments and Counterparts",
              "Amendments require a signed writing and, where required, NTIA/DOC and Tribal "
              "approval; this Agreement may be executed in counterparts and by electronic "
              "signature.")

    disclaimer_block(doc)
    C.signature_block(doc,
                      extra_note="Construction pricing, milestones, warranties, and retainage "
                      "(Schedule S5), and all approvals (Schedule S14), must be completed and "
                      "confirmed against the Award before execution.")

    return C.save(doc, "02_Definitive_Agreements",
                  "02_Design_Engineering_Procurement_and_Construction_Agreement.docx")


if __name__ == "__main__":
    p1 = build_master()
    p2 = build_depc()
    print("MASTER ->", p1)
    print("DEPC   ->", p2)
