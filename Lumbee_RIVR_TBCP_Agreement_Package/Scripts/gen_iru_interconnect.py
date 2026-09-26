"""
gen_iru_interconnect.py — Generator for two coordinated Definitive Agreements of the
Lumbee Tribe of North Carolina / RIVR Tech TBCP fiber package:

    DOC 1 — 02_Definitive_Agreements/03_IRU_and_Network_Access_Agreement.docx
    DOC 2 — 02_Definitive_Agreements/04_Interconnection_Transport_and_Shared_Facilities_Agreement.docx

All party names, defined terms, citations, deal mechanics, precedence language, and
formatting come from the canonical engine Scripts/common.py (SINGLE SOURCE OF TRUTH).
Nothing about the (unsupplied) award, routes, prices, useful life, approvals, land
rights, or consents is invented — unknowns are marked with C.PH() and the appropriate
flag marker so counsel/grant/technical reviewers can complete them.

These are PRELIMINARY working drafts, not final legal advice.
"""

import sys
sys.path.insert(0, '/home/user/claude-skills/Lumbee_RIVR_TBCP_Agreement_Package/Scripts')
import common as C


# ---------------------------------------------------------------------------
# Shared building blocks reused by both documents
# ---------------------------------------------------------------------------
def precedence_and_shared_definitions(doc, art_no):
    """Order-of-precedence + shared-definitions clauses, verbatim from the engine."""
    C.article(doc, art_no, "Order of Precedence and Shared Definitions")

    C.section(doc, f"{art_no}.1", "Order of Precedence",
              "This Agreement is one of the Definitive Agreements delivered under, and "
              f"is subordinate to, the {C.AGREEMENTS['master']}. In the event of any "
              "conflict, ambiguity, or inconsistency among the instruments comprising "
              "the transaction, the following order of precedence controls, from highest "
              "to lowest:")
    for i, item in enumerate(C.PRECEDENCE, start=1):
        C.numbered(doc, item)
    C.para(doc, C.PRECEDENCE_RULE)

    C.section(doc, f"{art_no}.2", "Shared Definitions", C.SHARED_DEFINITIONS_RULE)
    C.subsection(doc, "a",
                 "Capitalized terms used in this Agreement — including "
                 f"“{C.TRIBE_SHORT},” “{C.OPERATOR_SHORT},” “{C.LREMC_SHORT},” "
                 f"“{C.NETWORK},” “{C.TRIBAL_ASSETS},” “{C.OPERATOR_EXISTING},” "
                 f"“{C.LREMC_ASSETS},” “{C.FEDERAL_INTEREST},” “{C.PROGRAM_INCOME},” "
                 f"“{C.SERVICE_TERRITORY},” “{C.ACTIVE_SUBSCRIBER},” “{C.DEMARCATION},” "
                 f"and “{C.POI}” — have the meanings given in Article 2 (Definitions) of "
                 f"the {C.AGREEMENTS['master']} unless expressly defined herein.")


def sovereign_and_governing_law(doc, art_no):
    """Bracketed sovereign-immunity / governing-law / forum ALTERNATIVES, flagged."""
    C.article(doc, art_no, "Sovereign Immunity, Governing Law, and Dispute Forum")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "This entire Article states bracketed ALTERNATIVES only. Tribal counsel "
                "and the Lumbee Tribal Council must select, negotiate, and authorize any "
                "waiver scope, governing law, and forum. Nothing here effects a waiver "
                "unless expressly and lawfully adopted by the Tribe. See "
                + C.CITES['sovereign_immunity'] + ".")

    C.section(doc, f"{art_no}.1", "Preservation of Sovereign Immunity",
              f"The {C.TRIBE_SHORT} is a sovereign and, except to the limited extent (if "
              "any) expressly waived in writing in accordance with Tribal law, retains "
              "its sovereign immunity from unconsented suit, and no provision of this "
              "Agreement shall be construed as a waiver of that immunity. A clear, "
              "unequivocal, and expressly authorized waiver is required for any limited "
              "waiver to be effective.")
    C.subsection(doc, "a",
                 "[ALTERNATIVE 1 — No waiver: the Tribe grants no waiver of sovereign "
                 "immunity; disputes are resolved exclusively through the non-binding "
                 "escalation and negotiation procedures of the "
                 f"{C.AGREEMENTS['master']}.]")
    C.subsection(doc, "b",
                 "[ALTERNATIVE 2 — Limited waiver for arbitration: the Tribe grants a "
                 "limited, express waiver solely to compel and enforce binding "
                 f"arbitration seated in {C.PH('seat — e.g., Robeson County / agreed venue')}, "
                 "with recovery limited to the assets and revenues expressly pledged and "
                 "expressly excluding any Trust, restricted, or Federal-Interest asset.]")
    C.subsection(doc, "c",
                 "[ALTERNATIVE 3 — Limited waiver for specified courts: the Tribe grants "
                 "a limited, express waiver solely for the "
                 f"{C.PH('forum — Tribal court / federal court / State court, per counsel')}, "
                 "subject to the same asset and remedy limitations.]")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Governing law is bracketed: [Tribal law] / [federal law and, to the "
                f"extent not preempted, the laws of the State of {C.STATE}]. Selection is "
                "a legal decision for Tribal counsel, and must be reconciled with the "
                "Award, applicable federal law, and any land rights under 25 CFR "
                "Parts 162/169 where Trust or restricted land is involved.")


def no_liens_clause(doc, art_no, section_no):
    """No lien / attachment against trust / restricted / Federal-Interest assets."""
    C.section(doc, section_no, "No Liens Against Trust, Restricted, or Federal-Interest Assets",
              "Notwithstanding any other provision of this Agreement or any other "
              "Definitive Agreement, no lien, mortgage, security interest, pledge, "
              "attachment, levy, or other encumbrance may attach to, and no remedy may be "
              f"enforced against, any {C.TRIBAL_ASSETS}, any asset subject to the "
              f"{C.FEDERAL_INTEREST}, or any Tribal trust or restricted asset, in each "
              "case except as expressly authorized in advance and in writing by the "
              f"{C.AGENCY_SHORT}/{C.DOC_FULL} and, where applicable, the Bureau of Indian "
              f"Affairs. This restriction runs with the {C.TRIBAL_ASSETS} and binds every "
              "successor, assignee, and lender.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Confirm against " + C.CITES['real_property'] + ", " + C.CITES['trust']
                + ", and the Specific Award Conditions before finalizing any lender or "
                "security provision.")


def closing_disclaimer(doc):
    """Standard draft disclaimer that ends the body of every document."""
    C.spacer(doc, 1)
    p = doc.add_paragraph()
    r = p.add_run("DISCLAIMER.  ")
    r.bold = True
    r.font.color.rgb = C.RED
    r2 = p.add_run(
        "This document is a PRELIMINARY working draft prepared for discussion only. "
        "No controlling TBCP award or source documents were supplied; the provisional "
        f"baseline is the {C.NOFO_NAME}. " + C.NOFO_LIVE_NOTE + " It is not final legal, "
        "grant-compliance, tax, or financial advice, does not create any binding "
        "obligation, and does not constitute an offer. Party names, defined terms, "
        "economic terms, routes, useful life, approvals, land rights, and consents shown "
        "as placeholders or flags must be verified and completed by qualified Tribal "
        "counsel, grant-compliance counsel, and technical and financial advisors, and "
        "conformed to the executed federal Award, before any reliance or execution.")
    r2.italic = True
    r2.font.color.rgb = C.GREY


# ===========================================================================
#  DOCUMENT 02.03 — IRU AND NETWORK ACCESS AGREEMENT
# ===========================================================================
def build_iru():
    doc = C.new_doc()
    C.add_cover(
        doc,
        "DOCUMENT 02.03 — INDEFEASIBLE RIGHT OF USE AND NETWORK ACCESS AGREEMENT",
        C.AGREEMENTS['iru'],
        "A coordinated TBCP Definitive Agreement — Grant-Funded Assets owned by the "
        "Lumbee Tribe; operated by RIVR Tech under a bare contractual right of use")
    C.setup_header_footer(doc, "IRU and Network Access Agreement")
    C.add_toc(doc)

    # Intro ------------------------------------------------------------------
    C.add_status_and_intro(doc, C.AGREEMENTS['iru'], "02.03")

    # ART 1 — Definitions / interpretation ----------------------------------
    C.article(doc, 1, "Definitions, Interpretation, and Structure")
    C.section(doc, "1.1", "Defined Terms",
              "Capitalized terms have the meanings given in Article 2 (Definitions) of "
              f"the {C.AGREEMENTS['master']}, which is the single shared definitions "
              "source for the package, except where expressly defined in this Agreement. "
              f"“{C.IRU_TERM_DEFINED}” means the indefeasible right of use granted under "
              "Article 3, as further limited by this Agreement.")
    C.section(doc, "1.2", "Interpretation",
              "Headings are for convenience only. References to a Schedule, Exhibit, or "
              "other Definitive Agreement are to that instrument as it may be amended in "
              "accordance with the package. The word “including” means “including without "
              "limitation.” This Agreement is to be construed together with, and subject "
              f"to, the {C.AGREEMENTS['master']} and the Award.")
    C.section(doc, "1.3", "Two Structural Alternatives Presented",
              "This Agreement presents two structures for the long-term network-use "
              "right and recommends the first, subject to the Award:")
    C.subsection(doc, "a",
                 "[RECOMMENDED — Structure A: Indefeasible Right of Use (IRU).] A bare "
                 f"contractual right of use in favor of {C.OPERATOR_SHORT} over defined "
                 f"{C.TRIBAL_ASSETS}, with title retained by the {C.TRIBE_SHORT}, as set "
                 "out in Article 3.1.")
    C.subsection(doc, "b",
                 "[ALTERNATE — Structure B: Long-Term Network-Use License.] A revocable-"
                 "for-cause, non-exclusive network-use license achieving substantially "
                 "the same operating result without use of the “IRU” label, as set out in "
                 "Article 3.2, for use if counsel or the Award disfavors an IRU "
                 "characterization for grant-funded assets.")
    C.flag_para(doc, C.FLAG_GRANT,
                "The choice between Structure A and Structure B, and whether an IRU over "
                "grant-funded assets is permissible at all, must be confirmed against the "
                "executed Award, " + C.CITES['real_property'] + ", " + C.CITES['intangible']
                + ", and the Specific Award Conditions (" + C.CITES['sac'] + ").")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Counsel to confirm the IRU characterization does not create a disposition, "
                "encumbrance, or transfer of a real-property or Federal interest requiring "
                "prior NTIA/DOC (and, where land is involved, BIA) approval.")

    # ART 2 — Recitals -------------------------------------------------------
    C.article(doc, 2, "Recitals and Party Roles")
    C.section(doc, "2.1", "The Grantor / Owner",
              f"The {C.TRIBE_SHORT} is the award recipient and steward and the sole owner "
              f"of the {C.TRIBAL_ASSETS} — the grant-funded infrastructure comprising the "
              f"{C.NETWORK}. In this Agreement the {C.TRIBE_SHORT} acts as the “Grantor” "
              "and owner. The Tribe holds and retains title to the "
              f"{C.TRIBAL_ASSETS} at all times.")
    C.section(doc, "2.2", "The Grantee / Operator",
              f"{C.OPERATOR_FULL} ({C.OPERATOR_DEFINED}) is the operator and retail "
              f"provider of record. In this Agreement {C.OPERATOR_SHORT} acts as the "
              "“Grantee” of the right of use granted herein.")
    C.section(doc, "2.3", "LREMC Is a Separate Owner",
              f"{C.LREMC_FULL} ({C.LREMC_DEFINED}) is a separate entity that owns the "
              f"{C.LREMC_ASSETS} (poles, conduit, fiber, easements, huts, power, and "
              f"land). The {C.LREMC_ASSETS} are NOT {C.TRIBAL_ASSETS}, are NOT owned by "
              f"{C.OPERATOR_SHORT}, and are NOT granted under this Agreement. Any use of "
              f"{C.LREMC_ASSETS} requires a separate {C.LREMC_SHORT} consent, joinder, "
              f"license, lease, pole-attachment, easement, or facility instrument (see "
              f"the {C.AGREEMENTS['land']} and the LREMC Consent), executed by "
              f"{C.LREMC_SHORT} as owner.")
    C.section(doc, "2.4", "RIVR Tech Existing Network Is Separate and Not Free",
              f"{C.OPERATOR_SHORT} owns the {C.OPERATOR_EXISTING} (its pre-existing "
              "fiber, core, transport, NOC, and billing systems), which remains "
              f"{C.OPERATOR_SHORT}’s property and is not granted, conveyed, or made free "
              "to the Tribe by this Agreement. Any use of, or reliance on, the "
              f"{C.OPERATOR_EXISTING}, and any commingling of grant-funded and "
              "commercial capacity, is valued and cost-allocated under the "
              f"{C.AGREEMENTS['interconnect']} and Schedule "
              f"{C.SCHEDULES['S10']}; grant-funded capacity is never provided as free "
              "commercial capacity, and commercial capacity is never provided free.")
    C.section(doc, "2.5", "Purpose",
              "The Parties enter this Agreement to grant "
              f"{C.OPERATOR_SHORT} the operating right of use it needs to deliver retail "
              f"broadband service over the {C.NETWORK} throughout the "
              f"{C.SERVICE_TERRITORY}, while preserving the Tribe’s ownership, the "
              f"{C.FEDERAL_INTEREST}, and full compliance with the {C.PROGRAM_FULL} "
              f"({C.PROGRAM_SHORT}) administered by {C.AGENCY_SHORT}.")

    # ART 3 — Grant / structures --------------------------------------------
    C.article(doc, 3, "Grant of Right of Use")
    C.section(doc, "3.1", "Structure A — Indefeasible Right of Use (Recommended)",
              f"Subject to the Award, to satisfaction of the conditions to activation in "
              f"Article 6.4, and to the limitations of this Agreement, the {C.TRIBE_SHORT} "
              f"grants to {C.OPERATOR_SHORT} an indefeasible right of use in and to the "
              f"IRU assets identified in Article 5, on a per-accepted-segment basis, for "
              "the Term. The IRU is a bare contractual right of use only.")
    C.section(doc, "3.2", "Structure B — Long-Term Network-Use License (Alternate)",
              f"If Structure A is not adopted, the {C.TRIBE_SHORT} instead grants "
              f"{C.OPERATOR_SHORT} a non-exclusive, long-term network-use license over the "
              "same identified assets, revocable for cause and otherwise coextensive with "
              "the operating rights, limitations, and Term of Structure A. All other "
              "Articles of this Agreement apply to Structure B with the term “License” "
              "substituted for “IRU.”")
    C.section(doc, "3.3", "Nature and Limits of the Grant",
              "Under either structure, the grant: (i) conveys no title, ownership, or "
              "equity in any asset; (ii) is non-exclusive as to the Tribe’s reserved "
              "rights and as to the open, nondiscriminatory interconnection obligations "
              f"preserved in the {C.AGREEMENTS['interconnect']}; (iii) is limited to the "
              "permitted uses in Article 7; and (iv) is expressly subordinate to the "
              "Award, applicable federal law, land rights, and all required approvals.")

    # ART 4 — Title does not transfer ---------------------------------------
    C.article(doc, 4, "Title Does Not Transfer; Federal Trust Relationship")
    C.section(doc, "4.1", "Retention of Title",
              f"The {C.TRIBE_SHORT} retains full legal and beneficial title to the "
              f"{C.TRIBAL_ASSETS} at all times. This Agreement grants only a bare "
              f"contractual right of use. No provision transfers, or is intended to "
              f"transfer, title, ownership, or any real-property interest to "
              f"{C.OPERATOR_SHORT}.")
    C.section(doc, "4.2", "Property Trust Relationship",
              f"The {C.TRIBAL_ASSETS} are held subject to the property trust relationship "
              "of " + C.CITES['trust'] + " and the real-property use, encumbrance, and "
              "disposition requirements of " + C.CITES['real_property'] + ". "
              f"{C.OPERATOR_SHORT} takes and holds the right of use expressly subject to "
              "those requirements and to the " + C.FEDERAL_INTEREST + ".")
    C.section(doc, "4.3", "No Act Inconsistent with Title or Federal Interest",
              f"{C.OPERATOR_SHORT} shall not take, permit, or suffer any act that is "
              f"inconsistent with the Tribe’s title, the {C.FEDERAL_INTEREST}, the trust "
              "relationship, or the Award, and shall hold itself out to third parties "
              "only as operator, not owner, of the " + C.TRIBAL_ASSETS + ".")

    # ART 5 — Identification of IRU assets ----------------------------------
    C.article(doc, 5, "Identification of the IRU Assets")
    C.section(doc, "5.1", "Register of IRU Assets",
              "The IRU assets are identified by the register at Schedule "
              f"{C.SCHEDULES['S3']} and the engineering detail at Schedule "
              f"{C.SCHEDULES['S4']}, which together specify, for each accepted segment, "
              "the attributes in Section 5.2.")
    C.section(doc, "5.2", "Identifying Attributes",
              "For each accepted segment, the Schedules identify:")
    for item in [
        f"the route and route identifier ({C.PH('route ID / GIS reference')}, {C.FLAG_TECH});",
        f"the cable(s) and cable identifier(s) ({C.PH('cable count / type')}, {C.FLAG_TECH});",
        f"the buffer tube(s) and tube assignment ({C.PH('tube assignment')}, {C.FLAG_TECH});",
        f"the specific fiber strand(s) granted, by strand number and count "
        f"({C.PH('strand numbers / total strand count')}, {C.FLAG_TECH});",
        f"any PON shared-capacity allocation (split ratio, wavelength plan, and shared "
        f"vs. dedicated designation) ({C.PH('PON split ratio / capacity')}, {C.FLAG_TECH});",
        f"the A-end and Z-end endpoints ({C.PH('endpoint locations')}, {C.FLAG_TECH});",
        f"the splice points and splice enclosures ({C.PH('splice point inventory')}, {C.FLAG_TECH});",
        f"the {C.DEMARCATION}(s) between the {C.NETWORK} and any interconnecting network "
        f"({C.PH('demarcation locations')}, {C.FLAG_TECH});",
        f"the associated electronics and active equipment, and whether they are within "
        f"or outside the IRU grant ({C.PH('electronics in/out of grant')}, {C.FLAG_TECH});",
        f"the facility, hut, cabinet, or site housing the assets, and the owner of that "
        f"facility ({C.PH('facility / owner — note LREMC where applicable')}, {C.FLAG_TECH});",
        f"the GIS reference and as-built record for the segment "
        f"({C.PH('GIS layer / as-built ref')}, {C.FLAG_TECH}).",
    ]:
        C.bullet(doc, item)
    C.flag_para(doc, C.FLAG_TECH,
                "All strand counts, route figures, PON ratios, endpoints, splice, "
                "demarcation, electronics, and GIS references are TO BE SUPPLIED from "
                "approved engineering and as-built records; none are invented here.")
    C.section(doc, "5.3", "Facilities Owned by LREMC",
              f"Where a facility, hut, pole, conduit, easement, power feed, or site "
              f"housing or carrying an IRU asset is a {C.LREMC_ASSETS}, that facility is "
              f"owned by {C.LREMC_SHORT} and is made available, if at all, only under a "
              f"separate {C.LREMC_SHORT} instrument (see the {C.AGREEMENTS['land']} and "
              "the LREMC Consent). This Agreement grants no right in any "
              f"{C.LREMC_ASSETS}.")

    # ART 6 — Term by accepted segment --------------------------------------
    C.article(doc, 6, "Term by Accepted Segment; Renewals; Conditions to Activation")
    C.section(doc, "6.1", "Segment-by-Segment Term Commencement",
              "The Term for each segment commences on the "
              f"{C.DEAL['term_trigger']} in accordance with the "
              f"{C.AGREEMENTS['depc']}, and not before. There is a separate Term for each "
              "accepted segment.")
    C.section(doc, "6.2", "Initial Term",
              f"The initial Term for each accepted segment is twenty (20) years measured "
              f"from that segment’s acceptance date.")
    C.section(doc, "6.3", "Renewals",
              f"The initial Term may be extended by {C.DEAL['iru_renewal']}, each "
              "exercisable only if, at the time of exercise: (i) the Award and applicable "
              "federal law permit the extension; (ii) the underlying land and access "
              "rights extend through the renewal period; and (iii) no uncured material "
              "default exists.")
    C.section(doc, "6.4", "Conditions to Activation",
              "No IRU (or License) right activates for a segment, and no segment Term "
              "commences, until all of the following are met for that segment:")
    for item in [
        f"segment acceptance under the {C.AGREEMENTS['depc']} (design, engineering, "
        "procurement, and construction complete and accepted);",
        "the segment’s IRU-asset attributes are recorded on Schedules "
        f"{C.SCHEDULES['S3']} and {C.SCHEDULES['S4']};",
        "all required federal, Tribal, corporate, landowner, and regulatory approvals "
        f"for that segment are in place (Schedule {C.SCHEDULES['S14']});",
        f"any required {C.LREMC_SHORT} consent or facility instrument for that segment is "
        "executed; and",
        "the segment satisfies the applicable optical acceptance testing.",
    ]:
        C.numbered(doc, item)
    C.flag_para(doc, C.FLAG_GRANT,
                "Cross-check the activation conditions against the segment-acceptance "
                f"mechanics of the {C.AGREEMENTS['depc']} and the Award before finalizing.")
    C.section(doc, "6.5", "Term Ceiling",
              "In no event does any Term (including renewals) extend beyond the earliest "
              "of " + C.DEAL['term_ceiling_note'] + ". If any of those limits is shorter, "
              "it controls, and the affected right of use terminates or is adjusted "
              "accordingly.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Useful life, the Federal Interest period, and the duration of underlying "
                "land/access rights are " + C.PH("NOT SUPPLIED — confirm from the Award, "
                "engineering, and land instruments") + "; the Term ceiling cannot be "
                "finalized until these are fixed.")

    # ART 7 — Permitted uses / access ---------------------------------------
    C.article(doc, 7, "Permitted Uses; Access, Maintenance, and Restoration")
    C.section(doc, "7.1", "Permitted Uses",
              f"{C.OPERATOR_SHORT} may use the IRU assets solely to operate the "
              f"{C.NETWORK} and provide retail broadband and related services within the "
              f"{C.SERVICE_TERRITORY}, consistent with the Award, the service commitments "
              f"at Schedule {C.SCHEDULES['S2']}, the {C.SPEED_FLOOR} service floor, and "
              "the permitted-use limits of this Agreement. Any non-project use, "
              "non-Tribal-customer use, or commercial capacity use is governed and "
              f"cost-allocated under Schedule {C.SCHEDULES['S10']} and is never presumed "
              "free.")
    C.section(doc, "7.2", "Access, Splicing, and Testing",
              f"{C.OPERATOR_SHORT} may access the IRU assets to splice, test, and "
              "commission the granted strands and capacity, subject to the access "
              f"procedures of the {C.AGREEMENTS['interconnect']}, the optical acceptance "
              "standards, and any facility-owner (including "
              f"{C.LREMC_SHORT}) access conditions.")
    C.section(doc, "7.3", "Maintenance, Restoration, and Replacement",
              "Routine and emergency maintenance, restoration, and like-for-like "
              "replacement of IRU-asset elements are performed under, and allocated by, "
              f"the {C.AGREEMENTS['om']} and Schedule {C.SCHEDULES['S6']}. Any replacement "
              f"element funded from Award funds becomes a {C.TRIBAL_ASSETS} owned by the "
              f"Tribe and subject to the {C.FEDERAL_INTEREST}; title does not vest in "
              f"{C.OPERATOR_SHORT} by reason of performing the work.")
    C.section(doc, "7.4", "Optical Acceptance Standards",
              "Segment testing and IRU acceptance use the optical standards of the "
              f"package: {C.OPTICAL['otdr']} at {C.OPTICAL['wavelengths']}; splice loss "
              f"not exceeding {C.OPTICAL['splice_loss_max']}; connector loss not exceeding "
              f"{C.OPTICAL['connector_loss_max']}; reflectance not exceeding "
              f"{C.OPTICAL['reflectance_max']}; and span loss {C.OPTICAL['span_margin']}.")

    # ART 8 — Quiet enjoyment / capacity protection -------------------------
    C.article(doc, 8, "Quiet Enjoyment, Relocations, Casualty, and Capacity Protection")
    C.section(doc, "8.1", "Quiet Enjoyment and Nondisturbance",
              f"So long as {C.OPERATOR_SHORT} is not in uncured material default and "
              "complies with the Award and this Agreement, it may use the IRU assets for "
              "the permitted uses without disturbance by the Tribe, subject to the Tribe’s "
              "reserved rights, the open-interconnection obligations, and the rights of "
              f"facility owners including {C.LREMC_SHORT}.")
    C.section(doc, "8.2", "Relocations",
              f"If any IRU asset must be relocated (for road work, pole change-out, "
              "landowner requirement, or otherwise), the Parties shall coordinate the "
              "relocation to preserve, as nearly as practicable, the granted capacity and "
              f"the {C.NETWORK}’s operation, with cost responsibility and any grant "
              f"treatment determined under the {C.AGREEMENTS['om']}, Schedule "
              f"{C.SCHEDULES['S9']}, and the Award. Relocation of any {C.LREMC_ASSETS} is "
              f"governed by the applicable {C.LREMC_SHORT} instrument.")
    C.section(doc, "8.3", "Casualty",
              "If IRU assets are damaged or destroyed, restoration priority, cost, "
              "insurance recovery, and any grant treatment are handled under the "
              f"{C.AGREEMENTS['om']}, the insurance requirements of the package, and "
              + C.CITES['insurance'] + ". Insurance proceeds for "
              f"{C.TRIBAL_ASSETS} are applied consistent with the {C.FEDERAL_INTEREST}.")
    C.section(doc, "8.4", "Capacity Protection",
              f"The Tribe shall not grant a conflicting right that would impair the "
              f"specific granted strands or PON capacity during the Term, and "
              f"{C.OPERATOR_SHORT} shall not use or configure the assets in a way that "
              "impairs the Tribe’s reserved capacity or the open-interconnection "
              f"obligations. Reserved, project, and commercial capacity are delineated on "
              f"Schedules {C.SCHEDULES['S3']} and {C.SCHEDULES['S10']}.")

    # ART 9 — Federal interest / liens --------------------------------------
    C.article(doc, 9, "Federal-Interest Restrictions; No Encumbrance")
    C.section(doc, "9.1", "Federal Interest",
              f"The {C.TRIBAL_ASSETS} are subject to the {C.FEDERAL_INTEREST} for the "
              "applicable Federal Interest period. Use, encumbrance, and disposition are "
              "governed by " + C.CITES['real_property'] + ", " + C.CITES['equipment']
              + ", " + C.CITES['intangible'] + ", and " + C.CITES['trust'] + ", and by the "
              "Award.")
    no_liens_clause(doc, 9, "9.2")
    C.section(doc, "9.3", "No Unauthorized Encumbrance",
              f"{C.OPERATOR_SHORT} shall not grant, create, or permit any lien, security "
              f"interest, or encumbrance on any {C.TRIBAL_ASSETS} or IRU right, and shall "
              "keep the assets free of any claim arising from its operations, except as "
              "expressly authorized in writing by the Tribe and, where required, "
              f"{C.AGENCY_SHORT}/{C.DOC_FULL} and BIA.")

    # ART 10 — Consideration ------------------------------------------------
    C.article(doc, 10, "Consideration and Program Income")
    C.section(doc, "10.1", "IRU Consideration",
              f"In consideration of the grant, {C.OPERATOR_SHORT} pays and provides "
              + C.DEAL['iru_prepaid_consideration'] + ".")
    C.section(doc, "10.2", "Per-Subscriber Operating Payment",
              f"The primary economic consideration for the operating relationship is the "
              f"per-Active-Subscriber operating payment of {C.DEAL['per_subscriber_amount']}, "
              f"set and administered under the {C.AGREEMENTS['retail']} and the "
              f"{C.AGREEMENTS['finance']} (and Schedule {C.SCHEDULES['S8']}). Payment "
              "characterization alternatives are: "
              + "; ".join(C.DEAL['pay_options'][k] for k in ["A", "B", "C", "D", "E"])
              + f". The recommended model is {C.DEAL['pay_options']['D']}.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                "The per-subscriber amount " + C.DEAL['per_subscriber_amount'] + " is a "
                "placeholder; the actual rate, proration, and included/excluded account "
                "definitions are a business decision to be finalized.")
    C.section(doc, "10.3", "Provisional Characterization; Program Income",
              "The label given to any payment does not control its treatment. "
              + C.DEAL['program_income_note'][0].upper() + C.DEAL['program_income_note'][1:]
              + ". " + C.PROGRAM_INCOME + " is administered under "
              + C.CITES['prog_income'] + " and the Award.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Program-income treatment under " + C.CITES['prog_income'] + " turns on "
                "the controlling Award and a written NTIA determination — not on the "
                "characterization chosen here. Confirm before finalizing.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Consideration characterization (asset-use fee, IRU consideration, revenue "
                "share, per-subscriber payment, or hybrid) is provisional and must be set "
                "by counsel with the financial advisor.")

    # ART 11 — Assignment / lender ------------------------------------------
    C.article(doc, 11, "Assignment, Lender Rights, and Successors")
    C.section(doc, "11.1", "Assignment",
              f"Neither Party may assign this Agreement or the IRU right without the other "
              "Party’s prior written consent and all approvals required by the Award and "
              "applicable law. Any assignment by "
              f"{C.OPERATOR_SHORT} must preserve the Tribe’s title, the "
              f"{C.FEDERAL_INTEREST}, and the operator’s obligations, and the assignee "
              "must expressly assume them.")
    C.section(doc, "11.2", "Lender Rights (Only If Lawful)",
              "Any lender collateral, financing, or leasehold-mortgage-type arrangement is "
              "permitted only to the extent lawful and expressly authorized, and in no "
              f"event may any lien, security interest, or remedy attach to or be enforced "
              f"against any {C.TRIBAL_ASSETS}, any asset subject to the "
              f"{C.FEDERAL_INTEREST}, or any Tribal trust or restricted asset. Lender "
              f"rights, if any, extend only to {C.OPERATOR_SHORT}’s own contractual "
              f"interests and the {C.OPERATOR_EXISTING}, subject to Article 9.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Whether any lender/collateral right is lawful at all for grant-funded, "
                "trust, or Federal-Interest assets requires confirmation against "
                + C.CITES['real_property'] + ", " + C.CITES['trust'] + ", and the Award.")
    C.section(doc, "11.3", "Successor Obligations",
              "This Agreement binds and benefits the Parties and their permitted "
              "successors and assigns. All operating, maintenance, payment, ownership-"
              "protection, and compliance obligations run with the assets and bind every "
              "successor operator.")

    # ART 12 — Termination / transition / disposition -----------------------
    C.article(doc, 12, "Termination, Transition, and Disposition")
    C.section(doc, "12.1", "Termination and Transition",
              "Termination, step-in, continuity, and termination-assistance are governed "
              f"by the {C.AGREEMENTS['transition']} and Schedule {C.SCHEDULES['S13']}. On "
              "termination or expiry of any Term, the affected right of use ends and "
              f"{C.OPERATOR_SHORT} shall cooperate in an orderly transition that keeps the "
              f"{C.NETWORK} in service and preserves the Tribe’s ownership and the "
              f"{C.FEDERAL_INTEREST}.")
    C.section(doc, "12.2", "Disposition",
              f"Any disposition of {C.TRIBAL_ASSETS} is governed by "
              + C.CITES['real_property'] + " and " + C.CITES['equipment'] + " and requires "
              "the approvals mandated by those provisions and the Award. No termination or "
              "transition event effects a disposition except in accordance with those "
              "requirements.")

    # ART 13 — Indefeasible does not override -------------------------------
    C.article(doc, 13, "“Indefeasible” Does Not Override Federal Law, the Award, Land Rights, or Approvals")
    C.para(doc,
           "Notwithstanding the use of the word “indefeasible,” the IRU (and any License "
           "under Structure B) is expressly subordinate to, and does not override, "
           "supersede, or diminish: (i) applicable federal law, including "
           + C.CITES['ug_part'] + "; (ii) the executed federal Award and its Specific "
           "Award Conditions; (iii) the land, easement, right-of-way, pole, site, power, "
           f"and facility rights on which the assets depend, including any {C.LREMC_ASSETS} "
           "and any rights under " + C.CITES['indian_leasing'] + " and "
           + C.CITES['indian_row'] + " where trust or restricted land is involved; or "
           "(iv) any federal, Tribal, corporate, landowner, or regulatory approval "
           "required for the assets or their use. To the extent the word “indefeasible” "
           "would imply otherwise, it is qualified by this Article.")
    C.flag_para(doc, C.FLAG_GRANT,
                "This subordination is mandatory for grant-funded assets; confirm the "
                "exact land-rights and approval dependencies before finalizing.")

    # ART 14 — Precedence / shared definitions ------------------------------
    precedence_and_shared_definitions(doc, 14)

    # ART 15 — Sovereign immunity / governing law ---------------------------
    sovereign_and_governing_law(doc, 15)

    # ART 16 — General ------------------------------------------------------
    C.article(doc, 16, "General Provisions")
    C.section(doc, "16.1", "Notices",
              f"Notices are given as provided in the {C.AGREEMENTS['master']}.")
    C.section(doc, "16.2", "No Third-Party Beneficiaries",
              f"Except for {C.AGENCY_SHORT}/{C.DOC_FULL} as to the {C.FEDERAL_INTEREST} "
              "and grant-compliance rights, this Agreement creates no third-party "
              "beneficiary rights.")
    C.section(doc, "16.3", "Severability and Reformation",
              "If any IRU, exclusivity, payment, or commercial-use term is held invalid "
              "or is rejected under the Award, the remainder remains effective and a "
              "lawful construction and service provision is preserved, and the term is "
              "reformed to the minimum extent necessary, consistent with the precedence "
              "rule.")
    C.section(doc, "16.4", "Entire Agreement Within the Package",
              f"This Agreement, together with the {C.AGREEMENTS['master']}, the other "
              "Definitive Agreements, and the Schedules, is the entire agreement of the "
              "Parties on its subject matter and supersedes prior understandings on that "
              "subject.")

    closing_disclaimer(doc)
    C.signature_block(doc,
                      "Signatory authority, capacity, and any required Tribal Council "
                      "resolution or federal/BIA approval must be confirmed before "
                      "execution.")

    return C.save(doc, "02_Definitive_Agreements", "03_IRU_and_Network_Access_Agreement.docx")


# ===========================================================================
#  DOCUMENT 02.04 — INTERCONNECTION, TRANSPORT, AND SHARED FACILITIES
# ===========================================================================
def build_interconnect():
    doc = C.new_doc()
    C.add_cover(
        doc,
        "DOCUMENT 02.04 — NETWORK INTERCONNECTION, TRANSPORT, EQUIPMENT, AND SHARED FACILITIES AGREEMENT",
        C.AGREEMENTS['interconnect'],
        "Physical and logical interconnection between the Tribal Network and the RIVR "
        "Tech Existing Network — with open, nondiscriminatory middle-mile obligations "
        "preserved and no capacity provided free")
    C.setup_header_footer(doc, "Interconnection, Transport, and Shared Facilities Agreement")
    C.add_toc(doc)

    C.add_status_and_intro(doc, C.AGREEMENTS['interconnect'], "02.04")

    # ART 1 — Definitions ---------------------------------------------------
    C.article(doc, 1, "Definitions, Interpretation, and Structure")
    C.section(doc, "1.1", "Defined Terms",
              "Capitalized terms have the meanings given in Article 2 (Definitions) of "
              f"the {C.AGREEMENTS['master']}, except where expressly defined herein.")
    C.section(doc, "1.2", "Purpose and Scope",
              f"This Agreement governs the physical and logical interconnection between "
              f"the {C.NETWORK} (grant-funded, owned by the {C.TRIBE_SHORT}) and the "
              f"{C.OPERATOR_EXISTING} (owned by {C.OPERATOR_SHORT}), and the shared "
              "facilities, transport, and equipment on which that interconnection "
              "depends. It does not convey title to any asset and is subordinate to the "
              "Award.")
    C.section(doc, "1.3", "Three Networks / Three Owners",
              f"The Parties acknowledge three distinct asset sets: (i) the "
              f"{C.TRIBAL_ASSETS} comprising the {C.NETWORK}, owned by the "
              f"{C.TRIBE_SHORT}; (ii) the {C.OPERATOR_EXISTING}, owned by "
              f"{C.OPERATOR_SHORT}; and (iii) the {C.LREMC_ASSETS}, owned by "
              f"{C.LREMC_SHORT}. Each set retains its own owner; interconnection does not "
              "merge ownership.")

    # ART 2 — POI / demarcation ---------------------------------------------
    C.article(doc, 2, "Points of Interconnection and Demarcation")
    C.section(doc, "2.1", "Points of Interconnection",
              f"Each {C.POI} between the {C.NETWORK} and the {C.OPERATOR_EXISTING} is "
              f"identified, located, and specified on Schedule {C.SCHEDULES['S4']}, "
              f"including the facility, rack, panel, and port for each {C.POI} "
              f"({C.PH('POI locations / port assignments')}, {C.FLAG_TECH}).")
    C.section(doc, "2.2", "Demarcation",
              f"The {C.DEMARCATION} at each {C.POI} is the physical and logical boundary "
              f"between the {C.NETWORK} and the {C.OPERATOR_EXISTING}, and fixes the "
              "boundary of operational, maintenance, and cost responsibility. Demarcation "
              f"details are recorded on Schedule {C.SCHEDULES['S4']}.")
    C.section(doc, "2.3", "Where a POI Sits in an LREMC Facility",
              f"Where a {C.POI} or {C.DEMARCATION} is located in or on a {C.LREMC_ASSETS} "
              f"(hut, cabinet, pole, or site), the underlying facility is owned by "
              f"{C.LREMC_SHORT} and access to it requires a separate {C.LREMC_SHORT} "
              "instrument; this Agreement fixes the interconnection boundary but does not "
              f"grant any right in the {C.LREMC_ASSETS}.")

    # ART 3 — Optical / Ethernet specs --------------------------------------
    C.article(doc, 3, "Optical and Ethernet Specifications; Fiber Assignment")
    C.section(doc, "3.1", "Optical Specifications",
              f"Optical interconnection uses {C.OPTICAL['wavelengths']} with acceptance "
              f"by {C.OPTICAL['otdr']}; splice loss not exceeding "
              f"{C.OPTICAL['splice_loss_max']}; connector loss not exceeding "
              f"{C.OPTICAL['connector_loss_max']}; reflectance not exceeding "
              f"{C.OPTICAL['reflectance_max']}; and span loss {C.OPTICAL['span_margin']}.")
    C.section(doc, "3.2", "Ethernet and Handoff Specifications",
              f"Ethernet handoff rates, framing, MTU, LAG, and VLAN conventions at each "
              f"{C.POI} are specified on Schedule {C.SCHEDULES['S4']} "
              f"({C.PH('handoff rate / framing / VLAN plan')}, {C.FLAG_TECH}).")
    C.section(doc, "3.3", "Fiber Pairs and Strands",
              f"The specific fiber pairs and strands assigned to interconnection at each "
              f"{C.POI}, and whether they are dedicated or shared, are recorded on "
              f"Schedules {C.SCHEDULES['S3']} and {C.SCHEDULES['S4']} "
              f"({C.PH('pair/strand assignments')}, {C.FLAG_TECH}).")

    # ART 4 — PON / electronics ---------------------------------------------
    C.article(doc, 4, "PON Architecture and Active Electronics")
    C.section(doc, "4.1", "PON Architecture",
              f"The passive optical network architecture, including split ratios, splitter "
              f"placement, and wavelength plan, is specified on Schedule "
              f"{C.SCHEDULES['S4']} ({C.PH('PON architecture / split ratios')}, "
              f"{C.FLAG_TECH}).")
    C.section(doc, "4.2", "OLT / ONT / Splitter Responsibility",
              f"Responsibility for the optical line terminals (OLT), optical network "
              f"terminals (ONT), and splitters — ownership, funding source, operation, and "
              f"maintenance — is allocated on Schedule {C.SCHEDULES['S4']}, distinguishing "
              f"grant-funded elements (owned by the {C.TRIBE_SHORT}, subject to the "
              f"{C.FEDERAL_INTEREST}) from {C.OPERATOR_SHORT}-owned elements "
              f"({C.PH('OLT/ONT/splitter ownership matrix')}, {C.FLAG_TECH}).")
    C.section(doc, "4.3", "Routers and Switches",
              f"The routers, switches, and aggregation equipment at each {C.POI}, and "
              f"their ownership and management boundary, are specified on Schedule "
              f"{C.SCHEDULES['S4']} ({C.PH('router/switch inventory and ownership')}, "
              f"{C.FLAG_TECH}).")

    # ART 5 — Transit / backhaul / IP / voice -------------------------------
    C.article(doc, 5, "Internet Transit, Backhaul, IP Addressing, and Voice")
    C.section(doc, "5.1", "Internet Transit",
              f"Internet transit provisioning, capacity, and cost responsibility are "
              f"specified on Schedule {C.SCHEDULES['S4']}; any transit supplied over the "
              f"{C.OPERATOR_EXISTING} is valued and cost-allocated under Article 13 and "
              f"Schedule {C.SCHEDULES['S10']} and is not provided free "
              f"({C.PH('transit source / capacity')}, {C.FLAG_TECH}).")
    C.section(doc, "5.2", "Backhaul",
              f"Backhaul paths, capacities, protection, and any reliance on the "
              f"{C.OPERATOR_EXISTING} or on {C.LREMC_ASSETS} routes are specified on "
              f"Schedule {C.SCHEDULES['S4']} ({C.PH('backhaul paths / capacities')}, "
              f"{C.FLAG_TECH}).")
    C.section(doc, "5.3", "IP Addressing and DNS",
              f"IP address blocks, routing (including any BGP/ASN arrangements), and DNS "
              f"responsibility are allocated on Schedule {C.SCHEDULES['S4']} "
              f"({C.PH('IP/ASN/DNS assignments')}, {C.FLAG_TECH}).")
    C.section(doc, "5.4", "Voice Dependencies",
              f"Any voice service dependencies (softswitch, SBC, E911/NG911, and "
              f"interconnection with the public network) are specified on Schedule "
              f"{C.SCHEDULES['S4']}, with regulatory obligations noted "
              f"({C.PH('voice architecture / E911')}, {C.FLAG_TECH}).")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Voice/E911 arrangements may trigger USAC/FCC obligations "
                "(" + C.CITES['usac_lifeline'] + ") and CPNI duties "
                "(" + C.CITES['cpni'] + "); confirm applicability.")

    # ART 6 — Rack / power / facilities -------------------------------------
    C.article(doc, 6, "Rack Space, Huts, Power, Environment, and Grounding")
    C.section(doc, "6.1", "Rack Space, Huts, and Cabinets",
              f"Rack space, huts, and cabinets used for interconnection are specified on "
              f"Schedules {C.SCHEDULES['S4']} and {C.SCHEDULES['S9']}, noting the owner of "
              f"each ({C.PH('rack/hut/cabinet inventory and owner')}, {C.FLAG_TECH}).")
    C.section(doc, "6.2", "Power, Generators, HVAC, and Grounding",
              f"Power feeds, backup generators, HVAC, and grounding at each shared site "
              f"are specified on Schedule {C.SCHEDULES['S9']} "
              f"({C.PH('power/generator/HVAC/grounding detail')}, {C.FLAG_TECH}).")
    C.section(doc, "6.3", "LREMC-Owned Facilities and Power",
              f"Where a hut, cabinet, site, pole, easement, land, or power feed is a "
              f"{C.LREMC_ASSETS}, it is owned by {C.LREMC_SHORT} and made available, if at "
              f"all, only under a separate {C.LREMC_SHORT} consent, license, lease, "
              f"pole-attachment, easement, or facility instrument (see Article 15, the "
              f"{C.AGREEMENTS['land']}, and the LREMC Consent). Nothing in this Agreement "
              f"grants {C.OPERATOR_SHORT} or the Tribe any right in the {C.LREMC_ASSETS}, "
              f"and any {C.LREMC_ASSETS} use is valued and never assumed free.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Every LREMC pole/easement/site/power dependency requires a separate, "
                "owner-executed instrument; confirm N.C. pole-attachment "
                "(" + C.CITES['nc_pole'] + ") and dig-safety "
                "(" + C.CITES['nc_dig'] + ") requirements.")

    # ART 7 — Monitoring / software / spares / security ---------------------
    C.article(doc, 7, "Monitoring, Software, Spares, and Security")
    C.section(doc, "7.1", "Monitoring",
              f"Network monitoring, NOC responsibility, alarms, and performance data "
              f"sharing operate on a {C.DEAL['sla']['noc']} basis, coordinated with the "
              f"{C.AGREEMENTS['om']} and Schedule {C.SCHEDULES['S6']}.")
    C.section(doc, "7.2", "Software Licenses",
              f"Element-management, OSS/BSS, and equipment software licenses used at the "
              f"interconnection, and their assignability and cost, are identified on "
              f"Schedule {C.SCHEDULES['S4']}; grant-funded intangibles are handled under "
              + C.CITES['intangible'] + ".")
    C.section(doc, "7.3", "Spares",
              f"Interconnection spares, sparing ratios, and replenishment are handled "
              f"under the {C.AGREEMENTS['om']} and Schedule {C.SCHEDULES['S6']}.")
    C.section(doc, "7.4", "Security and Supply-Chain",
              f"Physical and logical security, and supply-chain restrictions, follow the "
              f"{C.AGREEMENTS['privacy']} and Schedule {C.SCHEDULES['S11']}. No covered "
              f"telecommunications or video-surveillance equipment prohibited by "
              + C.CITES['telecom_ban'] + " may be used, and Build America, Buy America "
              "requirements (" + C.CITES['baba'] + ") apply to grant-funded elements.")

    # ART 8 — Capacity / testing --------------------------------------------
    C.article(doc, 8, "Capacity Forecasts, Augmentation, and Testing")
    C.section(doc, "8.1", "Capacity Forecasts and Augmentation",
              f"The Parties exchange capacity forecasts and coordinate augmentation of "
              f"interconnection capacity so that neither the {C.NETWORK} nor the "
              f"{C.OPERATOR_EXISTING} is congested; augmentation cost is allocated under "
              f"Article 13. Reserved Tribal/project capacity is protected per Schedule "
              f"{C.SCHEDULES['S10']} ({C.PH('forecast horizon / augmentation triggers')}, "
              f"{C.FLAG_TECH}).")
    C.section(doc, "8.2", "Testing",
              f"Interconnection commissioning and periodic testing use the optical "
              f"acceptance standards of Article 3 and the procedures of Schedule "
              f"{C.SCHEDULES['S4']}.")

    # ART 9 — Maintenance / outages / restoration / SLA ---------------------
    C.article(doc, 9, "Maintenance, Outage Coordination, Restoration, and Service Levels")
    C.section(doc, "9.1", "Planned Maintenance and Outage Coordination",
              f"Planned maintenance is coordinated with advance notice and maintenance "
              f"windows, and outages are jointly managed, under the {C.AGREEMENTS['om']} "
              f"and Schedule {C.SCHEDULES['S6']}.")
    C.section(doc, "9.2", "Restoration Priority",
              f"Restoration priority follows the severity model of the "
              f"{C.AGREEMENTS['om']} and Schedule {C.SCHEDULES['S6']}, prioritizing "
              "continuity of Essential Services and public safety.")
    C.section(doc, "9.3", "Service Levels",
              f"Interconnection service levels are those of Schedule {C.SCHEDULES['S6']} "
              f"and the {C.AGREEMENTS['om']}, including the availability target of "
              f"{C.DEAL['sla']['availability_target']} and the severity response, "
              "dispatch, and restoration targets summarized below:")
    C.add_table(
        doc,
        ["Severity", "Response", "Dispatch", "Restore"],
        [
            ["P1 (Critical)", f"{C.DEAL['sla']['P1_response_min']} min",
             f"{C.DEAL['sla']['P1_dispatch_hr']} hr", f"{C.DEAL['sla']['P1_restore_hr']} hr"],
            ["P2 (Major)", f"{C.DEAL['sla']['P2_response_min']} min",
             f"{C.DEAL['sla']['P2_dispatch_hr']} hr", f"{C.DEAL['sla']['P2_restore_hr']} hr"],
            ["P3 (Minor)", f"{C.DEAL['sla']['P3_response_hr']} hr",
             f"{C.DEAL['sla']['P3_dispatch_hr']} hr", f"{C.DEAL['sla']['P3_restore_days']} days"],
            ["P4 (Low)", f"{C.DEAL['sla']['P4_response_hr']} hr", "—",
             f"{C.DEAL['sla']['P4_restore_days']} days"],
        ],
        widths=[1.7, 1.4, 1.4, 1.4], col_align=[None, "c", "c", "c"])
    C.para(doc,
           f"Performance targets: latency ≤ {C.DEAL['sla']['latency_ms']} ms; packet loss "
           f"≤ {C.DEAL['sla']['packet_loss']}; jitter ≤ {C.DEAL['sla']['jitter_ms']} ms. "
           f"These targets are canonical to the package and must match the "
           f"{C.AGREEMENTS['om']} and Schedule {C.SCHEDULES['S6']}.")

    # ART 10 — Access procedures --------------------------------------------
    C.article(doc, 10, "Access Procedures")
    C.section(doc, "10.1", "Access to Interconnection Facilities",
              f"Access to interconnection facilities follows the access procedures of "
              f"Schedule {C.SCHEDULES['S9']}, including notice, escort, safety, and "
              "security requirements, and any facility-owner conditions.")
    C.section(doc, "10.2", "Access to LREMC-Owned Facilities",
              f"Access to any {C.LREMC_ASSETS} is governed solely by the applicable "
              f"{C.LREMC_SHORT} instrument and {C.LREMC_SHORT}’s safety and access rules; "
              "this Agreement confers no independent access right to those facilities.")

    # ART 11 — Third-party interconnection / open middle-mile ---------------
    C.article(doc, 11, "Third-Party Interconnection and Open, Nondiscriminatory Middle Mile")
    C.section(doc, "11.1", "Open, Nondiscriminatory Interconnection Preserved",
              f"The {C.NETWORK}’s open, nondiscriminatory middle-mile interconnection "
              f"obligation is preserved. Qualified third parties may interconnect with the "
              f"{C.NETWORK} on reasonable, nondiscriminatory terms, consistent with the "
              "Award and applicable law, and this Agreement does not, and shall not be "
              "construed to, grant any blanket exclusivity to "
              f"{C.OPERATOR_SHORT} across all Tribal lands or over the {C.NETWORK}.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Open-access / nondiscriminatory interconnection is a TBCP-sensitive "
                "condition; confirm scope against the Award and NOFO ("
                + C.CITES['nofo'] + ") before finalizing any priority or preference.")
    C.section(doc, "11.2", "Third-Party Terms",
              f"Terms for third-party interconnection, including any cost recovery and "
              f"capacity protection, are set consistent with Schedule "
              f"{C.SCHEDULES['S10']} and do not impair the Tribe’s reserved capacity or "
              "the service commitments.")

    # ART 12 — Cost allocation ----------------------------------------------
    C.article(doc, 12, "Cost Allocation; Nothing Provided Free")
    C.section(doc, "12.1", "Valuation and Consideration",
              f"Use of the {C.OPERATOR_EXISTING} and of any {C.LREMC_ASSETS} is valued and "
              f"supported by consideration or cost allocation under Schedule "
              f"{C.SCHEDULES['S10']}. The {C.OPERATOR_EXISTING} is never provided free to "
              f"the Tribe, grant-funded capacity is never provided as free commercial "
              f"capacity, and {C.LREMC_ASSETS} are never assumed free.")
    C.section(doc, "12.2", "Cost Categories",
              f"Interconnection, transit, backhaul, transport, colocation, power, and "
              f"augmentation costs are categorized and allocated per Schedule "
              f"{C.SCHEDULES['S10']}, distinguishing project (grant-eligible) from "
              "non-project and commercial use.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Cost allocation between grant-eligible project use and commercial use "
                "must satisfy " + C.CITES['allowable'] + " and the Award; confirm the "
                "valuation methodology with grant-compliance counsel and the financial "
                "advisor.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                "The valuation basis and rates for the RIVR Tech Existing Network and any "
                "LREMC Facilities are a business decision and are "
                + C.PH("NOT SUPPLIED — to be set in Schedule S10") + ".")

    # ART 13 — Title / risk / replacement / decommissioning -----------------
    C.article(doc, 13, "Title, Risk of Loss, Replacement, and Decommissioning")
    C.section(doc, "13.1", "Title",
              f"Interconnection does not transfer title. Grant-funded elements remain "
              f"{C.TRIBAL_ASSETS} owned by the {C.TRIBE_SHORT} and subject to the "
              f"{C.FEDERAL_INTEREST}; {C.OPERATOR_SHORT}-funded elements remain part of "
              f"the {C.OPERATOR_EXISTING}; and {C.LREMC_ASSETS} remain owned by "
              f"{C.LREMC_SHORT}.")
    C.section(doc, "13.2", "Risk of Loss",
              f"Risk of loss for each element follows its owner, subject to the insurance "
              f"requirements of the package and " + C.CITES['insurance'] + ", and subject "
              f"to the demarcation of responsibility at each {C.POI}.")
    C.section(doc, "13.3", "Replacement",
              f"Like-for-like replacement of interconnection elements is handled under the "
              f"{C.AGREEMENTS['om']}; any element funded from Award funds becomes a "
              f"{C.TRIBAL_ASSETS} subject to the {C.FEDERAL_INTEREST}.")
    C.section(doc, "13.4", "Decommissioning",
              f"Decommissioning of interconnection facilities follows the "
              f"{C.AGREEMENTS['transition']} and Schedule {C.SCHEDULES['S13']}, and any "
              f"disposition of {C.TRIBAL_ASSETS} complies with " + C.CITES['real_property']
              + " and " + C.CITES['equipment'] + ".")

    # ART 14 — Separate LREMC instruments -----------------------------------
    C.article(doc, 14, "Separate LREMC Instruments Required")
    C.para(doc,
           f"Any required {C.LREMC_SHORT} consent, license, lease, pole-attachment, "
           f"easement, land, power, or facility instrument is a SEPARATE signature "
           f"document executed by {C.LREMC_SHORT} as owner (see the "
           f"{C.AGREEMENTS['land']} and the LREMC Consent). This Agreement is not, and "
           f"does not substitute for, any such instrument, and no interconnection right "
           f"over any {C.LREMC_ASSETS} exists until the applicable {C.LREMC_SHORT} "
           f"instrument is executed.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Identify every LREMC-owned dependency and confirm a separate executed "
                "instrument exists for each before activation. Land rights, consents, and "
                "owner approvals are " + C.PH("NOT SUPPLIED") + " and must not be assumed.")

    # ART 15 — Precedence / shared definitions ------------------------------
    precedence_and_shared_definitions(doc, 15)

    # ART 16 — General ------------------------------------------------------
    C.article(doc, 16, "General Provisions")
    C.section(doc, "16.1", "No Third-Party Beneficiaries",
              f"Except for {C.AGENCY_SHORT}/{C.DOC_FULL} as to the {C.FEDERAL_INTEREST} "
              "and grant-compliance rights, and except for the preserved rights of "
              "qualified third-party interconnectors under Article 11, this Agreement "
              "creates no third-party beneficiary rights.")
    C.section(doc, "16.2", "Severability and Reformation",
              "If any interconnection, exclusivity, cost-allocation, or commercial-use "
              "term is held invalid or is rejected under the Award, the remainder remains "
              "effective and a lawful interconnection and service provision is preserved, "
              "consistent with the precedence rule.")

    closing_disclaimer(doc)
    C.signature_block(doc,
                      "Confirm signatory authority for RIVR Tech and the Tribe, and note "
                      "that LREMC is NOT a signatory to this Agreement — LREMC executes "
                      "its own separate instruments.")

    return C.save(doc, "02_Definitive_Agreements", "04_Interconnection_Transport_and_Shared_Facilities_Agreement.docx")


if __name__ == "__main__":
    p1 = build_iru()
    p2 = build_interconnect()
    print("IRU / Network Access Agreement ->", p1)
    print("Interconnection / Transport / Shared Facilities Agreement ->", p2)
