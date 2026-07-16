"""
gen_iru_sla.py — Generates Deliverable 3 and Deliverable 4 of the
Lumbee Tribe of North Carolina / RIVR Tech broadband IRU package:

    Document 02.02 — Indefeasible Right of Use Agreement
        -> 02_Core_Agreements/02_Indefeasible_Right_of_Use_Agreement.docx
    Document 02.03 — Network Operations, Maintenance & SLA
        -> 02_Core_Agreements/03_Network_Operations_Maintenance_and_SLA.docx

Every operative value flows from the canonical Scripts/common.py so defined
terms, SLA targets, insurance limits, IRU term options, and citations stay
consistent across the entire package. Unresolved items are marked with flags
and placeholders; governing law and sovereign-immunity waiver are NEVER
silently chosen — bracketed alternatives + [ATTORNEY REVIEW REQUIRED].
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C


# ===========================================================================
#  DOCUMENT 02.02 — INDEFEASIBLE RIGHT OF USE AGREEMENT
# ===========================================================================
def build_iru():
    doc = C.new_doc()
    C.add_cover(
        doc,
        "DOCUMENT 02.02 — INDEFEASIBLE RIGHT OF USE AGREEMENT",
        "Indefeasible Right of Use Agreement",
        "Grant of a bare contractual right of use in Tribally owned, "
        "grant-funded broadband infrastructure — title retained by the Tribe",
    )
    C.setup_header_footer(doc, "IRU Agreement (Doc 02.02)")
    C.add_toc(doc)
    C.status_banner(doc)
    C.spacer(doc, 1)

    # --- Preamble --------------------------------------------------------
    C.para(
        doc,
        f"This Indefeasible Right of Use Agreement (this “Agreement” or "
        f"the “IRU Agreement”) is made and entered into as of "
        f"{C.PH('Effective Date')} (the “Effective Date”), by and between "
        f"{C.TRIBE_FULL}, a federally recognized Indian tribe "
        f"(together with, where applicable, {C.TRIBE_ENTITY_ALT}, the "
        f"“{C.TRIBE_SHORT}” and, in its capacity as grantor hereunder, the "
        f"“IRU Grantor”), and {C.OPERATOR_FULL} (“{C.OPERATOR_SHORT}” "
        f"and, in its capacity as grantee hereunder, the “IRU Grantee”). "
        f"The {C.TRIBE_SHORT} and {C.OPERATOR_SHORT} are each a “{C.PARTY_SINGULAR}” "
        f"and together the “{C.PARTIES_COLLECTIVE}.”",
    )
    C.flag_para(
        doc, C.FLAG_ATTORNEY,
        "Confirm the exact contracting Tribal party. If a wholly owned Tribal "
        "entity or Tribally chartered instrumentality is designated as IRU "
        "Grantor in lieu of the Tribe itself, conform the preamble, signature "
        "block, and Exhibit A ownership recitals accordingly, and confirm that "
        "the designated entity holds record title to the Tribal Assets.",
    )
    C.flag_para(
        doc, C.FLAG_GRANT,
        "Federal-recognition and TBCP eligibility gate: the Lumbee Tribe's "
        "recognition status under the Lumbee Act of 1956 (Pub. L. 84-570) has "
        "historically been read to limit access to certain federal Indian "
        "programs. TBCP eligibility, the identity of the eligible entity, and "
        "the ability to hold the Award and the grant-funded assets in the "
        f"Tribe's name must be confirmed with {C.AGENCY_SHORT} before execution. "
        "See " + C.CITES["lumbee_act"] + ".",
    )

    # ---------------- ARTICLE 1 — RECITALS -------------------------------
    C.article(doc, 1, "Recitals and Background")
    recitals = [
        (f"The {C.TRIBE_SHORT} is the recipient (or designated eligible entity) of a "
         f"federal award under the {C.PROGRAM_FULL} ({C.PROGRAM_SHORT}) administered by "
         f"the {C.AGENCY_FULL} ({C.AGENCY_SHORT}) (the “Award”), pursuant to the "
         f"{C.NOFO_NAME} and the associated Specific Award Conditions, for the "
         f"deployment of qualifying broadband infrastructure serving {C.GEOGRAPHY} "
         f"(the “{C.SERVICE_TERRITORY}”)."),
        (f"With Award funds, the {C.TRIBE_SHORT} has designed, constructed, or caused "
         f"to be constructed certain broadband infrastructure that is owned by the "
         f"{C.TRIBE_SHORT} and subject to a continuing federal interest (the "
         f"“{C.TRIBAL_ASSETS}”), as more particularly identified in the Exhibits."),
        (f"{C.OPERATOR_SHORT} owns and operates an existing middle-mile, backbone, and "
         f"core network, together with related electronics, transport, and support "
         f"systems (the “{C.OPERATOR_EXISTING}”), which the {C.TRIBAL_ASSETS} "
         f"interconnect with at defined {C.DEMARCATION}s to form a single, integrated, "
         f"hybrid broadband {C.NETWORK} (the “{C.NETWORK}”)."),
        (f"The {C.TRIBE_SHORT} desires to grant to {C.OPERATOR_SHORT}, and "
         f"{C.OPERATOR_SHORT} desires to accept, an indefeasible right to use "
         f"specified capacity in the {C.TRIBAL_ASSETS} (the “{C.IRU_TERM_DEFINED}”) "
         f"for the purpose of operating the {C.NETWORK} and delivering broadband and "
         f"related services throughout the {C.SERVICE_TERRITORY}, all as a bare "
         f"contractual right and without any transfer of title."),
        (f"The {C.PARTIES_COLLECTIVE} intend that this Agreement, and all rights "
         f"granted hereunder, be fully subordinate to and consistent with the Award, "
         f"the requirements of {C.CITES['ug_part']}, and all other applicable federal "
         f"requirements, and that nothing herein impair the {C.FEDERAL_INTEREST} in the "
         f"{C.TRIBAL_ASSETS}."),
    ]
    C.para(doc, "The Parties enter into this Agreement on the basis of the following, "
                "each of which is incorporated into the operative provisions:")
    for i, r in enumerate(recitals, 1):
        C.subsection(doc, chr(64 + i), r)  # A, B, C...
    C.para(doc, "NOW, THEREFORE, in consideration of the mutual covenants and "
                "conditions set forth herein, and for other good and valuable "
                "consideration, the receipt and sufficiency of which are acknowledged, "
                "the Parties agree as follows:")

    # ---------------- ARTICLE 2 — DEFINITIONS ----------------------------
    C.article(doc, 2, "Definitions and Interpretation")
    C.section(doc, "2.1", "Defined Terms")
    C.para(doc, "Capitalized terms have the meanings given below or where first "
                "defined in this Agreement. Terms defined in the Award, the "
                f"{C.NOFO_SHORT}, or {C.CITES['ug_part']} have the meanings given there "
                "unless the context requires otherwise.")
    defs = [
        ("Award", "the TBCP federal financial assistance award (including the notice "
                  "of award, budget, Specific Award Conditions, and NTIA Standard "
                  "Terms and Conditions) under which the Tribal Assets were funded."),
        ("Demarcation Point", "each physical and logical point of interconnection, "
                  "identified in Exhibit B, at which responsibility, ownership, and "
                  "operational control transition between the Tribal Assets and the "
                  "RIVR Tech Existing Network."),
        ("Federal Interest", "the continuing interest of the United States, acting "
                  "through NTIA, in the Tribal Assets and any proceeds thereof, arising "
                  "under the Award and " + C.CITES["real_property"] + ", "
                  + C.CITES["equipment"] + ", and " + C.CITES["trust"] + "."),
        ("IRU Capacity", "the specific fiber strands, wavelengths, conduit, and passive "
                  "capacity in the Tribal Assets in which the right of use is granted, "
                  "as allocated in Exhibit C, exclusive of the Reserved Tribal Capacity."),
        ("Reserved Tribal Capacity", "the fiber strands, wavelengths, and related "
                  "capacity reserved to the Tribe under Article 8, dedicated to Tribal "
                  "government, public safety, and anchor-institution use."),
        ("Tribal Assets", "the grant-funded broadband infrastructure owned by the "
                  "Tribe and identified in the Exhibits, together with all associated "
                  "Federal Interest, as further described in Section 4.2."),
        ("Essential Services", "911/E-911, public-safety, Tribal-government, and "
                  "anchor-institution connectivity, and any service designated as "
                  "essential under the Award or applicable law."),
    ]
    C.add_table(
        doc,
        ["Defined Term", "Meaning"],
        [[f'“{t}”', m] for t, m in defs],
        widths=[1.9, 4.6], font_size=9,
    )
    C.section(doc, "2.2", "Rules of Interpretation",
              "Headings are for convenience only. “Including” means "
              "“including without limitation.” References to statutes, "
              "regulations, and the Award include successors and amendments. In any "
              "conflict between the body of this Agreement and an Exhibit, the body "
              "controls except as to technical descriptions, which are governed by the "
              "Exhibits. In any conflict between this Agreement and the Award or "
              "applicable federal requirements, the Award and federal requirements "
              "control, as provided in Article 14.")

    # ---------------- ARTICLE 3 — GRANT OF IRU ---------------------------
    C.article(doc, 3, "Grant of Indefeasible Right of Use")
    C.section(doc, "3.1", "Grant",
              f"Subject to the terms of this Agreement and the Award, the {C.TRIBE_SHORT}, "
              f"as IRU Grantor, hereby grants to {C.OPERATOR_SHORT}, as IRU Grantee, an "
              f"exclusive (as to third parties, but subject to the Reserved Tribal "
              f"Capacity and the Tribe's retained rights) indefeasible right to use the "
              f"IRU Capacity in the {C.TRIBAL_ASSETS} for the Permitted Uses during the "
              f"Term. The {C.IRU_TERM_DEFINED} granted hereunder is a right of use only.")
    C.section(doc, "3.2", "Nature of the Right",
              "The IRU is a bare contractual right of use. It is not a lease of real "
              "property, does not create any leasehold, tenancy, easement in gross, or "
              "possessory estate in favor of RIVR Tech, and does not convey any right, "
              "title, or ownership interest in the Tribal Assets, the underlying real "
              "property, or any easement or access right, all of which are and remain "
              "vested in the Tribe.")

    C.section(doc, "3.3", "TITLE DOES NOT TRANSFER; Tribe Retains Ownership")
    C.para(doc, "NOTWITHSTANDING ANYTHING TO THE CONTRARY IN THIS AGREEMENT: legal and "
                "equitable title to, and fee ownership of, the Tribal Assets is retained "
                f"at all times by the {C.TRIBE_SHORT} and does NOT transfer to "
                f"{C.OPERATOR_SHORT} under this Agreement, upon delivery, upon acceptance, "
                "upon payment of any consideration, or upon expiration or termination. "
                f"{C.OPERATOR_SHORT} acquires only the contractual right of use expressly "
                "granted in Section 3.1.", bold=True)
    C.subsection(doc, "a",
                 f"The {C.TRIBAL_ASSETS} were acquired with federal award funds and are "
                 f"subject to the {C.FEDERAL_INTEREST} and to a property trust "
                 f"relationship under " + C.CITES["trust"] + ", pursuant to which the "
                 f"{C.TRIBE_SHORT} holds the {C.TRIBAL_ASSETS} in trust for the "
                 "beneficiaries of the Award and may not use, encumber, or dispose of "
                 "them except as permitted by " + C.CITES["real_property"] + " and "
                 + C.CITES["equipment"] + ".")
    C.subsection(doc, "b",
                 f"{C.OPERATOR_SHORT} acknowledges the {C.FEDERAL_INTEREST}, disclaims "
                 f"any ownership claim to the {C.TRIBAL_ASSETS}, and agrees that this "
                 "Agreement is consistent with the use and encumbrance limitations of "
                 + C.CITES["real_property"] + " and the disposition rules of "
                 + C.CITES["equipment"] + " (as revised by " + C.CITES["ug_2024"] + ").")
    C.subsection(doc, "c",
                 f"Nothing herein grants {C.OPERATOR_SHORT} any reversionary, residual, "
                 f"or purchase right in the {C.TRIBAL_ASSETS}. Any change in ownership, "
                 f"disposition, or transfer of the {C.TRIBAL_ASSETS} is governed solely "
                 f"by the Award, {C.CITES['ug_part']}, and prior written {C.AGENCY_SHORT} "
                 "approval where required.")

    # ---------------- ARTICLE 4 — IRU ASSETS / EXHIBITS ------------------
    C.article(doc, 4, "IRU Assets, Exhibits, and Demarcation Points")
    C.section(doc, "4.1", "Identification via Exhibits",
              "The Tribal Assets and the IRU Capacity are identified in, and this "
              "Agreement incorporates by reference, the following Exhibits:")
    C.add_table(
        doc,
        ["Exhibit", "Contents"],
        [
            ["Exhibit A — Route Schedule", "Route-by-route description of the Tribal "
             "Assets, including segment identifiers, endpoints, mileage, and ownership "
             "attestation. " + C.PH("route list, segment IDs, and mileage to be attached")],
            ["Exhibit B — Asset / Demarcation Matrix", "Category-by-category inventory "
             "of Tribal Assets and the corresponding Demarcation Points where the "
             "Tribal Assets meet the RIVR Tech Existing Network."],
            ["Exhibit C — Fiber Allocation", "Strand- and wavelength-level allocation "
             "of IRU Capacity to RIVR Tech versus Reserved Tribal Capacity. "
             + C.PH("fiber-count allocation table to be attached")],
            ["Exhibit E / Exhibit G — Acceptance", "Delivery, testing, and acceptance "
             "procedures and forms (cross-referenced in Article 6)."],
            ["Exhibit I — Insurance", "Insurance requirements and evidence "
             "(cross-referenced in Article 15)."],
        ],
        widths=[2.1, 4.4], font_size=9,
    )
    C.section(doc, "4.2", "Categories of Tribal Assets")
    C.para(doc, f"The {C.TRIBAL_ASSETS} include, without limitation, the following "
                "categories of grant-funded infrastructure, each as detailed in "
                "Exhibits A and B:")
    for item in [
        "dark and lit fiber-optic strands and cables;",
        "conduit, innerduct, and microduct;",
        "handholes, vaults, manholes, and pull boxes;",
        "splice enclosures, splice closures, and splice trays;",
        "fiber huts, equipment shelters, cabinets, and pedestals;",
        "fiber-distribution and termination panels (patch panels / FDH / OTB);",
        "easement, license, pole-attachment, and access rights appurtenant to the "
        "foregoing (as record rights of the Tribe, licensed for access under Article 9); and",
        "all related passive infrastructure, grounding, and support structures.",
    ]:
        C.bullet(doc, item)
    C.section(doc, "4.3", "Demarcation Points",
              f"Each {C.DEMARCATION} is fixed in Exhibit B and marks the boundary "
              f"between the {C.TRIBAL_ASSETS} (Tribe-owned) and the {C.OPERATOR_EXISTING} "
              f"(RIVR Tech-owned). On the Tribal-Asset side of each {C.DEMARCATION}, the "
              f"assets are Tribal Assets subject to this Agreement and the Federal "
              f"Interest; on the RIVR Tech side, the assets are {C.OPERATOR_ASSETS} "
              f"owned by {C.OPERATOR_SHORT}. Operational, maintenance, and cost "
              f"responsibility follow the {C.DEMARCATION} as set forth in Document 02.03 "
              f"(Network Operations, Maintenance & SLA).")
    C.flag_para(doc, C.FLAG_TECH,
                "Exact route list, segment identifiers, mileage, fiber counts, and "
                "Demarcation Point coordinates are pending final as-built records and "
                "must be inserted into Exhibits A, B, and C before execution.")

    # ---------------- ARTICLE 5 — TERM -----------------------------------
    C.article(doc, 5, "Term, Term Alternatives, and Renewal")
    C.section(doc, "5.1", "IRU Term",
              "The term of the IRU (the “Term”) commences on the Commencement "
              "Date (Article 6) and continues for the period selected by the Parties "
              "from the alternatives in Section 5.2, unless earlier terminated in "
              "accordance with this Agreement.")
    C.section(doc, "5.2", "Term Alternatives (20 / 25 / 30 Years)")
    C.para(doc, "The Parties have modeled the following Term alternatives. The "
                "recommended Term is thirty (30) years, which best aligns the useful "
                "life of the fiber plant with the operator's cost-recovery horizon "
                "while remaining within the Federal Interest period for planning "
                "purposes:")
    terms = C.DEAL["iru_terms"]
    rec = C.DEAL["iru_term_recommended"]
    C.add_table(
        doc,
        ["Alternative", "IRU Term", "Renewal Options", "Assessment", "Recommendation"],
        [
            ["Alt. 1", f"{terms[0]} years",
             C.DEAL["iru_renewal"],
             "Shortest commitment; earliest re-pricing/re-competition; may under-recover "
             "long-life fiber investment.", "Not recommended"],
            ["Alt. 2", f"{terms[1]} years",
             C.DEAL["iru_renewal"],
             "Intermediate; balances flexibility and investment recovery.",
             "Acceptable fallback"],
            ["Alt. 3", f"{terms[2]} years",
             C.DEAL["iru_renewal"],
             "Matches fiber useful life; strongest investment certainty for the "
             "operator; longest capacity commitment by the Tribe.",
             "RECOMMENDED"],
        ],
        widths=[0.8, 0.9, 1.6, 2.2, 1.0], font_size=9,
        col_align=["c", "c", None, None, "c"],
    )
    C.para(doc, f"Selected Term: {C.PH('select 20 / 25 / 30 years — recommended 30')}. "
                f"Absent a contrary selection recorded here and in the Financial "
                f"Schedule (Document 02.04), the recommended Term of {rec} years applies.")
    C.section(doc, "5.3", "Renewal",
              f"Provided RIVR Tech is not then in uncured material default and subject to "
              f"any then-required {C.AGENCY_SHORT} consent and continued consistency with "
              f"the Award, RIVR Tech may extend the Term for {C.DEAL['iru_renewal']}, "
              f"upon not less than {C.PH('renewal notice period, e.g., twelve (12) months')} "
              f"prior written notice, on the same terms except as to consideration, which "
              f"shall be as provided in the Financial Schedule (Document 02.04). Renewal "
              f"is a business decision to be confirmed at each renewal point.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                "Confirm Term selection (20/25/30) and renewal notice period and "
                "renewal pricing mechanism; these interact with the financial model and "
                "the Federal Interest period.")

    # ---------------- ARTICLE 6 — COMMENCEMENT / ACCEPTANCE --------------
    C.article(doc, 6, "Conditions to Commencement; Delivery and Acceptance")
    C.section(doc, "6.1", "Conditions to Commencement",
              "The Commencement Date occurs on the last to be satisfied of: (a) "
              "substantial completion and energization of the applicable Tribal Assets; "
              "(b) successful completion of acceptance testing under Section 6.3; (c) "
              f"receipt of all consents required under the Award, including any "
              f"{C.AGENCY_SHORT} approval required for the grant of this IRU; and (d) "
              "delivery of the insurance certificates required by Article 15.")
    C.section(doc, "6.2", "Delivery",
              "The Tribe shall make the IRU Capacity available at the Demarcation Points "
              "described in Exhibit B. Delivery of a segment does not transfer title and "
              "does not relieve the Tribe of its ownership obligations under the Award.")
    C.section(doc, "6.3", "Acceptance Testing")
    C.para(doc, "Acceptance testing shall be performed in accordance with Exhibit E / "
                "Exhibit G and the following optical acceptance standards, which are the "
                "canonical acceptance criteria for the package:")
    C.add_table(
        doc,
        ["Test Parameter", "Acceptance Criterion"],
        [
            ["Test wavelengths", C.OPTICAL["wavelengths"]],
            ["OTDR method", C.OPTICAL["otdr"]],
            ["Fusion-splice loss", C.OPTICAL["splice_loss_max"]],
            ["Connector loss", C.OPTICAL["connector_loss_max"]],
            ["Span-loss budget", C.OPTICAL["span_margin"]],
            ["Reflectance (return loss)", C.OPTICAL["reflectance_max"]],
        ],
        widths=[2.2, 4.3], font_size=9,
    )
    C.para(doc, "A segment is deemed accepted upon RIVR Tech's countersignature of the "
                "acceptance form, or upon RIVR Tech's placing the segment into revenue "
                "service, whichever is earlier. Acceptance does not waive latent-defect "
                "or warranty rights and does not transfer title.")

    # ---------------- ARTICLE 7 — PERMITTED USES -------------------------
    C.article(doc, 7, "Permitted Uses")
    C.section(doc, "7.1", "Permitted Uses",
              "RIVR Tech may use the IRU Capacity to operate the Network and to provide "
              "the following services in the Service Territory, in each case consistent "
              "with the Award and applicable law: (a) residential broadband internet "
              "access at or above the applicable service floor (" + C.SPEED_FLOOR + "); "
              "(b) business and enterprise broadband; (c) voice/VoIP and associated "
              "communications services; and (d) related managed and transport services.")
    C.section(doc, "7.2", "Wholesale / Open-Access Use",
              "Whether RIVR Tech may provide wholesale, open-access, dark-fiber, or "
              "carrier-of-carriers services over the IRU Capacity is reserved as a "
              "business decision, subject to any open-access or nondiscrimination "
              "obligations in the Award and to the Reserved Tribal Capacity.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                "Decide whether wholesale/open-access resale over grant-funded Tribal "
                "Assets is permitted, and on what terms; this may be constrained or "
                "required by the Award's open-access conditions.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Confirm permitted-use scope against the Award's service, open-access, "
                "and nondiscrimination conditions and against any Program-income "
                "treatment under " + C.CITES["prog_income"] + ".")
    C.section(doc, "7.3", "Use Restrictions",
              "RIVR Tech shall not use the IRU Capacity for any unlawful purpose, in a "
              "manner that impairs the Reserved Tribal Capacity or Essential Services, "
              "or in any manner inconsistent with the Award or the Federal Interest. "
              "RIVR Tech shall comply with " + C.CITES["telecom_ban"] + " and shall not "
              "install covered telecommunications equipment on the Tribal Assets.")

    # ---------------- ARTICLE 8 — RESERVED TRIBAL CAPACITY ---------------
    C.article(doc, 8, "Reserved Tribal Fiber and Capacity")
    C.section(doc, "8.1", "Reservation",
              f"Notwithstanding the grant in Article 3, the {C.TRIBE_SHORT} reserves to "
              f"itself, at no charge and for the entire Term and any renewal, dedicated "
              f"strands and capacity in the {C.TRIBAL_ASSETS} (the “Reserved Tribal "
              f"Capacity”) for Tribal-government, public-safety, and "
              f"anchor-institution use, in the amount of "
              + C.PH("reserved strand count per segment, e.g., [N] strands / [X]% of capacity")
              + ", as allocated in Exhibit C.")
    C.section(doc, "8.2", "Priority and Non-Impairment",
              "The Reserved Tribal Capacity is senior to the IRU Capacity. RIVR Tech's "
              "use, maintenance, and restoration activities shall not degrade, "
              "reallocate, or impair the Reserved Tribal Capacity, and Essential "
              "Services carried on the Reserved Tribal Capacity receive Priority 1 "
              "handling under Document 02.03.")
    C.section(doc, "8.3", "Tribal Anchor Institutions",
              "The Tribe may use the Reserved Tribal Capacity to connect Tribal "
              "government facilities, public-safety answering points, schools, health "
              "facilities, libraries, and other anchor institutions "
              + C.PH("list of anchor institutions and connection points") + ".")

    # ---------------- ARTICLE 9 — INTERCONNECTION / COLLOCATION / ACCESS -
    C.article(doc, 9, "Interconnection, Collocation, and Access Rights")
    C.section(doc, "9.1", "Interconnection",
              f"The Parties shall interconnect the {C.TRIBAL_ASSETS} and the "
              f"{C.OPERATOR_EXISTING} at the {C.DEMARCATION}s in Exhibit B and shall "
              "maintain the interconnection in good working order for the Term.")
    C.section(doc, "9.2", "Collocation",
              "Each Party grants the other reasonable collocation rights in its huts, "
              "shelters, cabinets, and racks at and around the Demarcation Points, "
              "solely as needed to interconnect and operate the Network, subject to "
              "space, power, and safety availability and to the Reserved Tribal "
              "Capacity. Collocation on the Tribal Assets does not transfer title.")
    C.section(doc, "9.3", "Access Rights",
              f"The {C.TRIBE_SHORT} grants {C.OPERATOR_SHORT} a license (not an easement "
              f"in gross) to access the {C.TRIBAL_ASSETS} and the associated rights-of-way "
              f"for operation, maintenance, and restoration, in accordance with the "
              f"Tribe's access, safety, and cultural-resource protocols and with "
              f"applicable easement and pole-attachment agreements (including "
              + C.CITES["nc_pole"] + "). The Tribe retains all record easement and "
              "access rights.")

    # ---------------- ARTICLE 10 — MAINTENANCE ---------------------------
    C.article(doc, 10, "Splicing, Maintenance, and Emergency Repair")
    C.section(doc, "10.1", "Splicing Procedures",
              "All splicing on the Tribal Assets shall meet the optical acceptance "
              "standards in Section 6.3 (fusion-splice loss " + C.OPTICAL["splice_loss_max"]
              + "), be documented in splice records provided to the Tribe, and be "
              "performed so as not to disturb the Reserved Tribal Capacity or Essential "
              "Services.")
    C.section(doc, "10.2", "Maintenance",
              "Operation, maintenance, and repair of the Network are governed by "
              "Document 02.03 (Network Operations, Maintenance & SLA), which is "
              "incorporated by reference. RIVR Tech shall maintain the Tribal Assets in "
              "at least the condition delivered, ordinary wear excepted, and shall not "
              "diminish their value or the Federal Interest.")
    C.section(doc, "10.3", "Emergency Repair",
              "Either Party may perform emergency repairs to prevent imminent harm to "
              "persons, property, Essential Services, or continuity of service, with "
              "prompt notice to the other Party and reconciliation of cost responsibility "
              "under Document 02.03.")

    # ---------------- ARTICLE 11 — RELOCATION / CASUALTY -----------------
    C.article(doc, 11, "Relocation, Replacement, Casualty, and Condemnation")
    C.section(doc, "11.1", "Relocation",
              "If any Tribal Asset must be relocated (e.g., by governmental order, "
              "road project, or right-of-way change), the Parties shall cooperate to "
              "relocate the affected segment with minimal service interruption. "
              "Relocated assets remain Tribal Assets subject to the Federal Interest and "
              "this IRU. Cost allocation for relocation is "
              + C.PH("relocation cost allocation — party responsible / shared formula")
              + ".")
    C.section(doc, "11.2", "Replacement",
              "Assets replaced in the ordinary course become Tribal Assets and are "
              "subject to this Agreement and the Federal Interest; the IRU continues in "
              "the replacement capacity without additional consideration.")
    C.section(doc, "11.3", "Casualty",
              "Upon material damage or destruction of Tribal Assets, RIVR Tech shall "
              "restore the affected assets in accordance with Document 02.03 and the "
              "insurance proceeds provisions of Article 15; insurance proceeds relating "
              "to Tribal Assets are applied first to restoration. The Federal Interest "
              "attaches to insurance proceeds and to replacement property under "
              + C.CITES["insurance"] + " and " + C.CITES["equipment"] + ".")
    C.section(doc, "11.4", "Condemnation",
              "If Tribal Assets are taken by eminent domain, the award attributable to "
              f"the Tribal Assets belongs to the {C.TRIBE_SHORT} subject to the Federal "
              "Interest; RIVR Tech may pursue a separate award for its own relocation "
              "and business losses to the extent permitted by law. The IRU abates "
              "proportionally as to any taken capacity.")

    # ---------------- ARTICLE 12 — ASSIGNMENT / SUB-IRU ------------------
    C.article(doc, 12, "Restrictions on Assignment and Sub-IRU")
    C.section(doc, "12.1", "No Assignment Without Consent",
              f"RIVR Tech shall not assign, transfer, sublicense, grant a sub-IRU in, or "
              f"otherwise convey any interest in the IRU or the Tribal Assets, in whole "
              f"or in part, without the prior written consent of the {C.TRIBE_SHORT} and, "
              f"where required, of {C.AGENCY_SHORT}, which Tribal consent shall not be "
              f"unreasonably withheld for a permitted collateral purpose that does not "
              f"impair the Federal Interest.")
    C.section(doc, "12.2", "Federal-Interest Limits",
              "No assignment or sub-IRU may (a) transfer title to any Tribal Asset, "
              "(b) create any Federal-Interest-impairing encumbrance, or (c) be made to "
              "a debarred or suspended party (" + C.CITES["debarment"] + ") or to a party "
              "using covered telecommunications equipment (" + C.CITES["telecom_ban"] + ").")
    C.section(doc, "12.3", "Permitted Transfers",
              "RIVR Tech may assign to an affiliate or successor by merger that assumes "
              "all obligations and meets the Federal-Interest limits, upon notice and "
              "subject to any Award-required consent. Any successor operator is also "
              "governed by Document 02.07 (Transition).")

    # ---------------- ARTICLE 13 — CONSIDERATION -------------------------
    C.article(doc, 13, "Consideration, Maintenance Payments, and Revenue Sharing")
    C.section(doc, "13.1", "IRU Consideration",
              f"In consideration of the grant of the IRU, RIVR Tech shall pay "
              f"{C.DEAL['iru_prepaid_consideration']}. The prepaid/nominal structure "
              f"reflects that the substantial consideration to the Tribe is delivered "
              f"through the operating, maintenance, and revenue-sharing obligations and "
              f"the Reserved Tribal Capacity.")
    C.section(doc, "13.2", "Annual Maintenance Payments",
              "RIVR Tech shall pay annual maintenance charges as set forth in Document "
              "02.04 (Financial Schedule), in the amount of "
              + C.PH("annual maintenance payment / per-mile or per-strand rate")
              + ", subject to the escalation and true-up mechanics described there.")
    C.section(doc, "13.3", "Revenue Sharing",
              "Revenue sharing between the Parties is governed by Document 02.04, which "
              "presents the modeled options (fixed, percentage-of-revenue, "
              "percentage-of-cash-flow, hybrid, and stepped) and the recommended "
              "structure. Amounts characterized as Program Income are subject to "
              + C.CITES["prog_income"] + ".")
    C.flag_para(doc, C.FLAG_GRANT,
                "Confirm characterization of IRU consideration, maintenance payments, "
                "and revenue share as Program Income (or not) under "
                + C.CITES["prog_income"] + ", and confirm the required disposition/"
                "addition treatment with " + C.AGENCY_SHORT + ".")

    # ---------------- ARTICLE 14 — FEDERAL GRANT PRIORITY / ENCUMBRANCE --
    C.article(doc, 14, "Federal Grant Priority; Restrictions on Encumbering Grant-Funded Assets")
    C.section(doc, "14.1", "Federal Grant Priority")
    C.para(doc, "This Agreement is at all times subordinate to, and shall be construed "
                f"consistently with, the Award and all applicable federal requirements, "
                f"including {C.CITES['ug_part']}. In any conflict between this Agreement "
                f"and the Award or such federal requirements, the Award and federal "
                f"requirements control, and the affected provision of this Agreement is "
                f"deemed modified to the minimum extent necessary to conform. No "
                f"provision of this Agreement waives, diminishes, or subordinates the "
                f"{C.FEDERAL_INTEREST} or any {C.AGENCY_SHORT} right.", bold=True)
    C.section(doc, "14.2", "Prohibition on Encumbering Grant-Funded Assets")
    C.para(doc, f"{C.OPERATOR_SHORT} shall not, and shall not permit any person "
                f"claiming through it to, mortgage, pledge, hypothecate, grant a "
                f"security interest in, create a lien on, or otherwise encumber the "
                f"{C.TRIBAL_ASSETS} or the {C.FEDERAL_INTEREST}, in whole or in part, "
                f"without the prior written consent of {C.AGENCY_SHORT} and the "
                f"{C.TRIBE_SHORT}. Any purported encumbrance in violation of this Section "
                f"is void ab initio.", bold=True)
    C.subsection(doc, "a",
                 "Use, encumbrance, and disposition of real property comprising Tribal "
                 "Assets are governed by " + C.CITES["real_property"] + "; equipment by "
                 + C.CITES["equipment"] + "; and the property trust relationship by "
                 + C.CITES["trust"] + ".")
    C.subsection(doc, "b",
                 f"Any disposition, sale, or transfer of the {C.TRIBAL_ASSETS}, or any "
                 f"use inconsistent with the Award, requires prior {C.AGENCY_SHORT} "
                 f"approval and compliance with the applicable disposition threshold and "
                 f"procedures (" + C.CITES["ug_2024"] + ").")
    C.subsection(doc, "c",
                 "This Article survives expiration or termination and inures to the "
                 "benefit of the United States and " + C.AGENCY_SHORT + " as intended "
                 "third-party beneficiaries for purposes of the Federal Interest.")

    # ---------------- ARTICLE 15 — LIENS / TAXES / INSURANCE -------------
    C.article(doc, 15, "Liens, Taxes, and Insurance")
    C.section(doc, "15.1", "Liens",
              f"RIVR Tech shall keep the {C.TRIBAL_ASSETS} free of all mechanics', "
              f"materialmen's, tax, judgment, and other liens arising from its acts or "
              f"omissions, and shall discharge or bond any such lien within "
              f"{C.PH('lien discharge period, e.g., thirty (30) days')} of notice. No "
              f"lien may attach to the {C.FEDERAL_INTEREST}.")
    C.section(doc, "15.2", "Taxes",
              "RIVR Tech is responsible for taxes attributable to its use and operations. "
              "The Parties acknowledge the Tribe's sovereign status and any applicable "
              "exemptions; allocation of ad valorem and possessory-interest taxes, if "
              "any, is " + C.PH("tax allocation — to be confirmed with tax counsel") + ".")
    C.section(doc, "15.3", "Insurance")
    C.para(doc, "RIVR Tech shall procure and maintain, and cause its contractors to "
                "maintain, the following minimum insurance for the Term, naming the "
                f"{C.TRIBE_SHORT} and the United States/{C.AGENCY_SHORT} as "
                "additional insureds where applicable, with evidence delivered per "
                "Exhibit I and consistent with " + C.CITES["insurance"] + ":")
    ins = C.DEAL["insurance"]
    C.add_table(
        doc,
        ["Coverage", "Minimum Limit"],
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
        widths=[3.4, 3.1], font_size=9,
    )
    C.para(doc, "Property and builder's-risk proceeds for Tribal Assets are applied "
                "first to restoration; the Federal Interest attaches to such proceeds.")

    # ---------------- ARTICLE 16 — DEFAULT / TRANSITION ------------------
    C.article(doc, 16, "Default, Abandonment, Expiration, and Transition")
    C.section(doc, "16.1", "Events of Default",
              f"An Event of Default occurs if a Party (a) fails to pay any amount when "
              f"due and does not cure within {C.DEAL['cure_monetary_days']} days of "
              f"notice; (b) fails to perform any other material obligation and does not "
              f"cure within {C.DEAL['cure_nonmonetary_days']} days of notice (extended by "
              f"{C.DEAL['cure_nonmonetary_extension']}); (c) abandons the Network or "
              f"Essential Services; or (d) suffers an insolvency event.")
    C.section(doc, "16.2", "Remedies",
              "Upon an uncured Event of Default, the non-defaulting Party may pursue all "
              "remedies at law or in equity, subject to Article 20 and to the Tribe's "
              "step-in and successor-operator rights under Document 02.07. Award-related "
              "remedies for noncompliance are governed by " + C.CITES["remedies"] + ".")
    C.section(doc, "16.3", "Abandonment; Continuity of Essential Services",
              "RIVR Tech shall not abandon the Network or discontinue Essential Services. "
              "Upon threatened abandonment or chronic failure, the Tribe may exercise "
              "step-in rights (" + C.DEAL["stepin_emergency"] + ") and transition to a "
              "successor operator under Document 02.07.")
    C.section(doc, "16.4", "Expiration and Transition",
              f"Upon expiration or termination, the IRU terminates, all rights of use "
              f"revert to the {C.TRIBE_SHORT} (title having never left the Tribe), and "
              f"RIVR Tech shall cooperate in an orderly transition over up to "
              f"{C.DEAL['transition_assistance_months']} months as provided in Document "
              f"02.07, including delivery of records, keys, credentials, and as-builts, "
              f"and continuity of Essential Services.")
    C.section(doc, "16.5", "Successor Operator",
              "The Tribe may designate a successor operator to assume operation of the "
              "Network; RIVR Tech shall provide reasonable transition assistance and "
              "shall not impair the successor's ability to operate the Tribal Assets.")

    # ---------------- ARTICLE 17 — REPS / INDEMNITY ----------------------
    C.article(doc, 17, "Representations, Indemnification, and Limitation of Liability")
    C.section(doc, "17.1", "Representations and Warranties",
              "Each Party represents that it is duly organized and authorized to enter "
              "into this Agreement; that execution has been duly authorized; and that "
              "this Agreement is enforceable against it, subject to Article 18 "
              "(sovereign immunity) and applicable federal requirements.")
    C.section(doc, "17.2", "Indemnification",
              f"Each Party shall indemnify the other against third-party claims arising "
              f"from its negligence, willful misconduct, or breach, subject to the "
              f"limitations herein. {C.OPERATOR_SHORT} shall indemnify the "
              f"{C.TRIBE_SHORT} against liens, encumbrances, and Federal-Interest "
              f"impairments arising from RIVR Tech's acts. Indemnity by the Tribe, if "
              f"any, is subject to and does not exceed any limited immunity waiver in "
              f"Article 18. " + C.PH("mutual vs. one-way indemnity scope to be confirmed"))
    C.section(doc, "17.3", "Limitation of Liability",
              "Except for indemnity obligations, Federal-Interest and lien breaches, and "
              "willful misconduct, neither Party is liable for consequential, incidental, "
              "or punitive damages. Any aggregate cap is "
              + C.PH("liability cap, if any — business/legal decision") + ".")

    # ---------------- ARTICLE 18 — GENERAL / GOV LAW ---------------------
    C.article(doc, 18, "Sovereign Immunity, Governing Law, and General Provisions")
    C.section(doc, "18.1", "Sovereign Immunity; Dispute Resolution")
    C.para(doc, f"The {C.TRIBE_SHORT} is a sovereign and possesses sovereign immunity. "
                f"Any waiver of sovereign immunity is limited, express, and must be "
                f"specifically approved by the Tribe's governing body. The Parties have "
                f"NOT pre-selected a waiver scope or dispute forum; the following "
                f"alternatives are presented for negotiation and legal review:")
    C.subsection(doc, "Alt. 1",
                 "No waiver of sovereign immunity; disputes resolved exclusively by "
                 "binding arbitration with a limited, express, specifically identified "
                 "waiver solely for the purpose of compelling arbitration and enforcing "
                 "an award, with recovery limited to specified assets (not the Tribal "
                 "Assets or the Federal Interest).")
    C.subsection(doc, "Alt. 2",
                 "Limited waiver for the exclusive jurisdiction of "
                 + C.PH("[Tribal Court] / [designated forum]") + ", exhausting Tribal "
                 "remedies first, with defined caps and carve-outs.")
    C.subsection(doc, "Alt. 3",
                 "Limited waiver consenting to a specified federal or state court solely "
                 "for defined claims, with immunity otherwise fully retained.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Sovereign-immunity waiver scope and dispute forum are reserved for the "
                "Tribe's governing body and counsel. Do NOT adopt any alternative "
                "without express Tribal authorization. Any waiver must exclude the "
                "Tribal Assets and the Federal Interest from execution/attachment.")
    C.section(doc, "18.2", "Governing Law")
    C.para(doc, "Governing law is NOT pre-selected. The Parties shall choose among: "
                + C.PH("[the laws of the Lumbee Tribe of North Carolina] / "
                       "[the laws of the State of North Carolina] / "
                       "[applicable federal law], to the extent not preempted by the "
                       "Award and federal requirements") + ".")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Select governing law by bracketed alternative only; coordinate with the "
                "sovereign-immunity and dispute-resolution choice. Federal requirements "
                "and the Award control regardless of the governing-law choice (Article 14).")
    C.section(doc, "18.3", "Notices",
              "Notices shall be in writing and delivered to the addresses in "
              + C.PH("notice addresses for each Party") + ", effective on receipt.")
    C.section(doc, "18.4", "Force Majeure",
              "Neither Party is liable for delay caused by events beyond its reasonable "
              "control, provided Essential-Services continuity and storm-restoration "
              "obligations under Document 02.03 remain in effect.")
    C.section(doc, "18.5", "Entire Agreement; Amendment; Order of Precedence",
              "This Agreement and its Exhibits, together with the related package "
              "documents, constitute the entire agreement on their subject matter. "
              "Amendments must be in writing and signed; amendments affecting the "
              "Federal Interest require any Award-required consent. The Award and "
              "federal requirements control per Article 14.")
    C.section(doc, "18.6", "Third-Party Beneficiary",
              "The United States and " + C.AGENCY_SHORT + " are intended third-party "
              "beneficiaries solely as to the Federal Interest and the encumbrance and "
              "disposition restrictions in Article 14.")
    C.section(doc, "18.7", "Survival",
              "Articles 3.3 (title), 8 (Reserved Tribal Capacity, as to accrued rights), "
              "14 (Federal Grant Priority and encumbrance), 16.4 (transition), 17 "
              "(indemnity/limitation), and 18 survive expiration or termination.")

    # ---------------- ARTICLE 19 — EXHIBITS LIST -------------------------
    C.article(doc, 19, "Exhibits")
    C.para(doc, "The following Exhibits are attached and incorporated:")
    for ex in [
        "Exhibit A — Route Schedule (Tribal Assets)",
        "Exhibit B — Asset / Demarcation Matrix",
        "Exhibit C — Fiber Allocation (IRU Capacity vs. Reserved Tribal Capacity)",
        "Exhibit E / G — Delivery, Testing, and Acceptance Procedures and Forms",
        "Exhibit I — Insurance Requirements and Evidence",
    ]:
        C.bullet(doc, ex)

    C.signature_block(
        doc,
        extra_note="Confirm authorized signatories and any required Tribal Council / "
                   "governing-body resolution and NTIA consent before execution; attach "
                   "the authorizing resolution as an execution exhibit.",
    )
    return C.save(doc, "02_Core_Agreements", "02_Indefeasible_Right_of_Use_Agreement.docx")


# ===========================================================================
#  DOCUMENT 02.03 — NETWORK OPERATIONS, MAINTENANCE & SLA
# ===========================================================================
def build_sla():
    S = C.DEAL["sla"]
    doc = C.new_doc()
    C.add_cover(
        doc,
        "DOCUMENT 02.03 — NETWORK OPERATIONS, MAINTENANCE & SERVICE LEVEL AGREEMENT",
        "Network Operations, Maintenance & SLA",
        "Measurable operations, maintenance, restoration, and performance "
        "commitments for the hybrid Tribal/RIVR Tech broadband Network",
    )
    C.setup_header_footer(doc, "O&M / SLA (Doc 02.03)")
    C.add_toc(doc)
    C.status_banner(doc)
    C.spacer(doc, 1)

    C.para(
        doc,
        f"This Network Operations, Maintenance & Service Level Agreement (this "
        f"“O&M/SLA”) is entered into as of {C.PH('Effective Date')} by and "
        f"between {C.TRIBE_FULL} (the “{C.TRIBE_SHORT}”) and {C.OPERATOR_FULL} "
        f"(“{C.OPERATOR_SHORT}”), and supplements and is incorporated into the "
        f"Indefeasible Right of Use Agreement (Document 02.02). It sets measurable "
        f"operations, maintenance, restoration, and performance requirements for the "
        f"{C.NETWORK}, including the {C.TRIBAL_ASSETS} and their interconnection with the "
        f"{C.OPERATOR_EXISTING} at the {C.DEMARCATION}s.",
    )

    # ---------------- ARTICLE 1 — DEFINITIONS / SCOPE --------------------
    C.article(doc, 1, "Scope, Definitions, and Responsibility Boundary")
    C.section(doc, "1.1", "Scope",
              f"{C.OPERATOR_SHORT} shall operate, monitor, maintain, and restore the "
              f"{C.NETWORK} to the standards in this O&M/SLA. Responsibility follows the "
              f"{C.DEMARCATION}: RIVR Tech is responsible for both the {C.OPERATOR_EXISTING} "
              f"and, under this O&M/SLA, for operating and maintaining the {C.TRIBAL_ASSETS} "
              f"on the Tribe's behalf, without acquiring title (see Document 02.02, "
              f"Article 3.3).")
    C.section(doc, "1.2", "Priority Definitions",
              "Trouble is classified Priority 1 (P1) through Priority 4 (P4) per the "
              "Severity Matrix in Article 3. “Response” means acknowledgment "
              "and ticketing; “Dispatch” means a technician en route or remote "
              "work commenced; “Restoration” means service restored to "
              "specification. Times run from detection or report, whichever is earlier.")
    C.section(doc, "1.3", "Essential Services Priority",
              "911/E-911, public-safety, Tribal-government, and anchor-institution "
              "traffic on the Reserved Tribal Capacity always receive Priority 1 "
              "handling regardless of the number of affected end users.")

    # ---------------- ARTICLE 2 — NOC / MONITORING -----------------------
    C.article(doc, 2, "Network Operations Center and 24/7 Monitoring")
    C.section(doc, "2.1", "24/7/365 NOC",
              f"RIVR Tech shall operate, or cause to be operated, a Network Operations "
              f"Center staffed {S['noc']}, providing continuous surveillance of the "
              f"{C.NETWORK}, alarm management, and trouble coordination.")
    C.section(doc, "2.2", "Monitoring Requirements",
              "The NOC shall continuously monitor optical power, link state, node "
              "availability, environmental and power alarms at huts/shelters, and "
              "performance counters (availability, latency, packet loss, jitter). "
              "Polling interval shall not exceed "
              + C.PH("polling interval, e.g., five (5) minutes") + ", and critical "
              "alarms shall generate an automatic ticket within "
              + C.PH("auto-ticket interval, e.g., five (5) minutes") + ".")
    C.section(doc, "2.3", "Trouble Reporting",
              "RIVR Tech shall provide the Tribe a 24/7 trouble-reporting method "
              "(toll-free number, email/portal, and escalation contacts per Exhibit H). "
              "The Tribe, anchor institutions, and end users may report trouble; each "
              "report receives a ticket number and initial classification.")

    # ---------------- ARTICLE 3 — SEVERITY MATRIX ------------------------
    C.article(doc, 3, "Outage Classification and Severity Matrix")
    C.para(doc, "The following Severity Matrix is the canonical classification and "
                "commitment table for the package. All times are maximums and run from "
                "detection or report, whichever is earlier:")
    C.add_table(
        doc,
        ["Priority", "Definition / Examples", "Response", "Dispatch",
         "Restoration Target", "Notification / Escalation"],
        [
            ["P1 — Critical",
             "Complete outage of a core/backbone segment or hut; loss of Essential "
             "Services or 911; fiber cut affecting a large service area; Reserved Tribal "
             "Capacity down.",
             f"{S['P1_response_min']} min",
             f"{S['P1_dispatch_hr']} hr",
             f"{S['P1_restore_hr']} hr",
             "Immediate notice to Tribe; hourly updates; auto-escalate to management "
             "per Exhibit H."],
            ["P2 — Major",
             "Partial outage or degraded service affecting multiple customers; loss of "
             "redundancy/protection; single-node failure without Essential-Services impact.",
             f"{S['P2_response_min']} min",
             f"{S['P2_dispatch_hr']} hr",
             f"{S['P2_restore_hr']} hr",
             "Notice to Tribe within response window; updates every "
             + C.PH("P2 update interval, e.g., 4 hr") + "; escalate if restoration at risk."],
            ["P3 — Minor",
             "Single-customer outage or intermittent/degraded performance; non-critical "
             "alarm; minor equipment fault with workaround.",
             f"{S['P3_response_hr']} hr",
             f"{S['P3_dispatch_hr']} hr",
             f"{S['P3_restore_days']} business days",
             "Ticketed; daily updates until cleared; escalate on aging."],
            ["P4 — Maintenance / Cosmetic",
             "Non-service-affecting condition; documentation or cosmetic issue; planned "
             "corrective item; informational alarm.",
             f"{S['P4_response_hr']} hr",
             "As scheduled",
             f"{S['P4_restore_days']} days",
             "Logged; addressed in next maintenance window; report in monthly summary."],
        ],
        widths=[1.0, 2.0, 0.75, 0.7, 1.05, 1.6], font_size=8,
        col_align=["c", None, "c", "c", "c", None],
    )
    C.flag_para(doc, C.FLAG_TECH,
                "Confirm the outage-scope thresholds (number of customers / segments) "
                "that map an incident to each Priority, and the P2 update cadence, in "
                "the final Exhibit H escalation matrix.")

    # ---------------- ARTICLE 4 — RESPONSE / ESCALATION ------------------
    C.article(doc, 4, "Response, Dispatch, Restoration, and Escalation")
    C.section(doc, "4.1", "Commitments",
              f"RIVR Tech shall meet the response ({S['P1_response_min']}-minute P1), "
              f"dispatch ({S['P1_dispatch_hr']}-hour P1), and restoration "
              f"({S['P1_restore_hr']}-hour P1) targets in the Severity Matrix for each "
              f"Priority, and shall record actual times on each ticket for reporting and "
              f"service-credit determination.")
    C.section(doc, "4.2", "Escalation Procedures",
              "RIVR Tech shall maintain a tiered escalation chain (Tier 1 NOC → Tier "
              "2 field/engineering → management → executive) with named contacts "
              "and time-based auto-escalation, as detailed in Exhibit H (Escalation "
              "Matrix). Essential-Services incidents escalate immediately to management.")
    C.flag_para(doc, C.FLAG_TECH,
                "Attach Exhibit H (Escalation Matrix) with named 24/7 contacts, phone "
                "numbers, and time-based escalation triggers.")

    # ---------------- ARTICLE 5 — SCHEDULED MAINTENANCE ------------------
    C.article(doc, 5, "Scheduled Maintenance and Customer Notifications")
    C.section(doc, "5.1", "Maintenance Windows",
              "Planned, service-affecting maintenance shall occur within standard "
              "maintenance windows " + C.PH("standard window, e.g., Sun 00:00–06:00 ET")
              + " and be limited to " + C.PH("max planned-maintenance minutes/month")
              + " of service-affecting time, excluded from availability calculations only "
              "if properly noticed.")
    C.section(doc, "5.2", "Advance Notice",
              "RIVR Tech shall provide the Tribe and affected customers at least "
              + C.PH("planned-maintenance notice, e.g., ten (10) business days")
              + " advance notice of planned service-affecting maintenance, and as much "
              "notice as practicable for urgent maintenance.")
    C.section(doc, "5.3", "Customer Notifications",
              "RIVR Tech shall notify affected end users of outages and restoration "
              "status through " + C.PH("notification channels — SMS/email/IVR/portal")
              + ", and shall provide the Tribe outage summaries for Essential-Services "
              "sites in real time.")

    # ---------------- ARTICLE 6 — LOCATES / DAMAGE PREVENTION ------------
    C.article(doc, 6, "Fiber Locates, Damage Prevention, and Cable Cuts")
    C.section(doc, "6.1", "Locates (NC 811)",
              "RIVR Tech shall participate in the North Carolina 811 one-call system and "
              "comply with " + C.CITES["nc_dig"] + ", providing timely and accurate "
              "locates of the Tribal Assets and marking within statutory timeframes.")
    C.section(doc, "6.2", "Damage Prevention",
              "RIVR Tech shall maintain a damage-prevention program including as-built "
              "records, locate ticket management, potholing where required, and "
              "contractor education, to protect the Tribal Assets and the Federal "
              "Interest.")
    C.section(doc, "6.3", "Cable Cuts",
              f"Fiber cuts are P1 or P2 per the Severity Matrix based on scope. RIVR Tech "
              f"shall stage splice crews and materials to meet the {S['P1_restore_hr']}-"
              f"hour P1 restoration target for large-area cuts and shall preserve "
              f"evidence for third-party damage recovery under Article 14.")

    # ---------------- ARTICLE 7 — STORM / SPARES / PM --------------------
    C.article(doc, 7, "Storm Restoration, Spare Materials, and Preventive Maintenance")
    C.section(doc, "7.1", "Storm and Emergency Restoration",
              "RIVR Tech shall maintain a storm/emergency restoration plan for "
              "hurricane, flood, and ice events common to " + C.GEOGRAPHY + ", including "
              "mutual-aid arrangements, staging, and prioritization of Essential Services "
              "and public-safety sites. During a declared emergency, restoration "
              "sequencing prioritizes life-safety and Reserved Tribal Capacity.")
    C.section(doc, "7.2", "Spare Materials",
              "RIVR Tech shall maintain a spares inventory (fiber cable, splice "
              "enclosures, connectors, optics, power, and critical electronics) "
              "sufficient to meet the restoration targets, in the quantities set out in "
              + C.PH("spares inventory schedule — quantities by material") + ".")
    C.section(doc, "7.3", "Preventive Maintenance",
              "RIVR Tech shall perform scheduled preventive maintenance (hut/shelter "
              "inspections, generator/battery testing, connector cleaning, vegetation "
              "and pole inspections, and optical audits) on the cycle in "
              + C.PH("PM schedule — activities and frequency") + ", and log all PM "
              "activity for the monthly report.")

    # ---------------- ARTICLE 8 — ELECTRONICS / SOFTWARE -----------------
    C.article(doc, 8, "Electronics Replacement, Software, and Firmware")
    C.section(doc, "8.1", "Electronics Replacement",
              "RIVR Tech shall replace failed or end-of-life active electronics to "
              "sustain the performance standards, and shall manage refresh cycles so as "
              "not to degrade Essential Services or the Reserved Tribal Capacity. "
              "Replacement of Tribal-Asset-side electronics does not transfer title "
              "(Document 02.02, Article 11.2).")
    C.section(doc, "8.2", "Software and Firmware Updates",
              "RIVR Tech shall keep network element software and firmware on vendor-"
              "supported, security-patched releases, applying critical security patches "
              "within " + C.PH("critical-patch window, e.g., 30 days") + " and other "
              "updates on a managed cadence, with change control and rollback.")

    # ---------------- ARTICLE 9 — CYBER / DR / POWER ---------------------
    C.article(doc, 9, "Cybersecurity, Disaster Recovery, and Backup Power")
    C.section(doc, "9.1", "Cybersecurity Incident Response",
              "RIVR Tech shall maintain a cybersecurity program and incident-response "
              "plan consistent with Document 02.06 (Cybersecurity), including "
              "detection, containment, notification, and remediation, and shall notify "
              "the Tribe of reportable incidents within "
              + C.PH("cyber-incident notice window, e.g., 24 hours") + ".")
    C.section(doc, "9.2", "Disaster Recovery",
              "RIVR Tech shall maintain disaster-recovery and business-continuity plans "
              "for NOC, OSS/BSS, and critical network functions, with defined RTO/RPO "
              + C.PH("RTO/RPO targets") + " and periodic testing.")
    C.section(doc, "9.3", "Backup Power",
              "Critical sites (huts, core nodes, Essential-Services locations) shall have "
              "backup power (battery plus generator where applicable) sized for at least "
              + C.PH("backup-power runtime, e.g., 24–72 hours") + ", with automatic "
              "transfer, monitoring, and periodic load testing.")

    # ---------------- ARTICLE 10 — PERFORMANCE STANDARDS -----------------
    C.article(doc, 10, "Network Performance Standards")
    C.para(doc, "RIVR Tech shall meet or exceed the following measurable performance "
                "standards, measured monthly at the Demarcation Points and representative "
                "customer endpoints:")
    C.add_table(
        doc,
        ["Performance Metric", "Committed Standard", "Measurement Method"],
        [
            ["Network availability", S["availability_target"],
             "Monthly uptime %, excluding properly-noticed planned maintenance."],
            ["Latency (round-trip)", f"≤ {S['latency_ms']} ms",
             "Average RTT across the Network core, monthly."],
            ["Packet loss", f"≤ {S['packet_loss']}",
             "Monthly average over active monitoring probes."],
            ["Jitter", f"≤ {S['jitter_ms']} ms",
             "Monthly average packet-delay variation."],
            ["Broadband speed (service floor)", f"≥ {C.SPEED_FLOOR}",
             "Speed testing to " + C.PH("speed-test methodology / FCC MBA-style probes")
             + "; provisioned rate met/exceeded."],
        ],
        widths=[1.9, 1.5, 3.1], font_size=9,
    )
    C.section(doc, "10.1", "Broadband Speed Testing",
              f"RIVR Tech shall conduct routine speed testing demonstrating delivery of "
              f"at least the applicable service floor ({C.SPEED_FLOOR}) and any higher "
              f"provisioned tier, using a documented methodology, and shall retain "
              f"results for reporting and FCC/NTIA verification.")

    # ---------------- ARTICLE 11 — FCC / NTIA REQUIREMENTS ---------------
    C.article(doc, 11, "FCC and NTIA Performance Requirements")
    C.section(doc, "11.1", "Compliance",
              f"RIVR Tech shall operate the {C.NETWORK} in compliance with all "
              f"applicable FCC and {C.AGENCY_SHORT} performance, service, and reporting "
              f"requirements, including the Award's service milestones and speed/latency "
              f"conditions, and shall support the Tribe's Award reporting obligations "
              f"under {C.CITES['ug_part']}.")
    C.section(doc, "11.2", "Data for Award Reporting",
              "RIVR Tech shall provide the performance, availability, subscriber, and "
              "buildout data the Tribe needs for TBCP and FCC reporting, including "
              "location-level service data, in the formats and on the schedule the Tribe "
              "reasonably requires.")

    # ---------------- ARTICLE 12 — REPORTING -----------------------------
    C.article(doc, 12, "Monthly and Annual Reporting")
    C.section(doc, "12.1", "Monthly Report",
              "Within " + C.PH("monthly report due day, e.g., 10 business days") + " after "
              "each month, RIVR Tech shall deliver a report (per Exhibit J) covering: "
              "availability and performance versus standard; ticket log with Priority, "
              "response/dispatch/restoration times, and SLA attainment; outage causes; "
              "planned and preventive maintenance performed; locate activity and "
              "damages; spares status; and any service credits due.")
    C.section(doc, "12.2", "Annual Report",
              "Annually, RIVR Tech shall deliver a consolidated report including trend "
              "analysis, chronic-problem review, capital/electronics refresh status, "
              "cybersecurity/DR test results, and a forward maintenance plan, supporting "
              "the Tribe's Award and performance reporting.")
    C.flag_para(doc, C.FLAG_TECH,
                "Attach Exhibit J (Reporting Templates) defining exact monthly/annual "
                "report fields and delivery format.")

    # ---------------- ARTICLE 13 — SERVICE CREDITS -----------------------
    C.article(doc, 13, "Service Credits, Corrective Action, and Chronic Failure")
    C.section(doc, "13.1", "Service Credits")
    C.para(doc, "Failure to meet the committed standards entitles the Tribe to service "
                "credits against amounts otherwise payable to RIVR Tech (or, where no "
                "such amounts exist, to the credit accrual mechanism in Document 02.04), "
                "on the following schedule. Credits are a remedy for performance misses "
                "and are without prejudice to step-in and default remedies:")
    C.add_table(
        doc,
        ["Miss Category", "Threshold", "Service Credit"],
        [
            ["Availability shortfall",
             f"Below {S['availability_target']} in a month",
             C.PH("credit %, e.g., 5% of monthly maintenance fee per 0.1% below target, "
                  "up to a monthly cap")],
            ["P1 restoration miss",
             f"Restoration exceeds {S['P1_restore_hr']} hr",
             C.PH("per-incident credit for P1 miss")],
            ["P2 restoration miss",
             f"Restoration exceeds {S['P2_restore_hr']} hr",
             C.PH("per-incident credit for P2 miss")],
            ["Latency / loss / jitter miss",
             f"Exceeds {S['latency_ms']} ms / {S['packet_loss']} / {S['jitter_ms']} ms",
             C.PH("credit for sustained performance miss")],
            ["Essential-Services / 911 impact",
             "Any avoidable Essential-Services outage",
             C.PH("enhanced credit + mandatory root-cause and corrective action")],
        ],
        widths=[1.9, 1.9, 2.7], font_size=9,
    )
    C.flag_para(doc, C.FLAG_BUSINESS,
                "Set the service-credit percentages, per-incident amounts, monthly caps, "
                "and the interaction with the maintenance fee and revenue share in "
                "Document 02.04.")
    C.section(doc, "13.2", "Corrective Action",
              "On any repeated or Essential-Services miss, RIVR Tech shall deliver a "
              "root-cause analysis and corrective-action plan within "
              + C.PH("RCA/CAP window, e.g., 10 business days") + " and implement it on an "
              "agreed schedule.")
    C.section(doc, "13.3", "Chronic Failure",
              "Chronic failure (e.g., " + C.PH("chronic threshold, e.g., 3 P1 misses in "
              "6 months or repeated availability shortfalls") + ") is a material "
              "performance default that triggers enhanced credits, mandatory corrective "
              "action, and the Tribe's step-in and successor-operator rights.")
    C.section(doc, "13.4", "Tribal Step-In Rights",
              f"Upon chronic failure, threatened abandonment, or an uncured "
              f"Essential-Services default, the {C.TRIBE_SHORT} may exercise step-in "
              f"rights (" + C.DEAL["stepin_emergency"] + ") and, if necessary, transition "
              f"operations to a successor operator, all as provided in Document 02.07 "
              f"(Transition) and Document 02.02, Article 16.")

    # ---------------- ARTICLE 14 — PRICING / DAMAGE RECOVERY -------------
    C.article(doc, 14, "Maintenance Pricing, Third-Party Damage Recovery, and Uninsured Costs")
    C.section(doc, "14.1", "Maintenance Pricing",
              "Compensation for the operations and maintenance services under this "
              "O&M/SLA is set in Document 02.04 (Financial Schedule), in the amount of "
              + C.PH("annual O&M price / per-mile or per-strand maintenance rate")
              + ", subject to escalation and the service-credit offsets in Article 13.")
    C.section(doc, "14.2", "Third-Party Damage Recovery",
              "RIVR Tech shall pursue recovery from third parties responsible for damage "
              "to the Network (e.g., dig-ins, vehicle strikes), documenting costs and "
              "coordinating with the Tribe. Recoveries relating to Tribal Assets are "
              "applied first to restoration and to make the Tribe whole; the Federal "
              "Interest attaches to recoveries relating to Tribal Assets.")
    C.section(doc, "14.3", "Responsibility for Uninsured Costs",
              "Allocation of restoration costs not covered by insurance or third-party "
              "recovery is " + C.PH("uninsured-cost allocation — operator / shared / "
              "reserve-funded formula") + ". RIVR Tech shall not diminish the Tribal "
              "Assets or the Federal Interest by deferring necessary restoration for "
              "cost-allocation disputes.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                "Set the O&M pricing basis and the allocation of uninsured/unrecovered "
                "restoration costs; coordinate with the insurance limits (Document 02.02, "
                "Article 15) and the financial model (Document 02.04).")

    # ---------------- ARTICLE 15 — GENERAL / EXECUTION -------------------
    C.article(doc, 15, "General Provisions and Execution")
    C.section(doc, "15.1", "Relationship to IRU Agreement",
              "This O&M/SLA is subordinate to and incorporated into Document 02.02. In "
              "any conflict, Document 02.02 controls as to title, Federal Interest, and "
              "encumbrance; this O&M/SLA controls as to operational and performance "
              "standards. The Award and federal requirements control over both.")
    C.section(doc, "15.2", "Amendments",
              "Performance standards and pricing may be adjusted only by written "
              "amendment; no amendment may reduce Essential-Services protection or "
              "impair the Federal Interest without any Award-required consent.")
    C.section(doc, "15.3", "Referenced Exhibits",
              "Exhibit H (Escalation Matrix) and Exhibit J (Reporting Templates) are "
              "incorporated by reference and shall be attached before execution.")

    C.signature_block(
        doc,
        extra_note="Confirm operational contacts, Exhibit H escalation matrix, and "
                   "Exhibit J reporting templates, and reconcile all bracketed "
                   "operational thresholds with the final network design before execution.",
    )
    return C.save(doc, "02_Core_Agreements", "03_Network_Operations_Maintenance_and_SLA.docx")


if __name__ == "__main__":
    p1 = build_iru()
    p2 = build_sla()
    print("IRU  ->", p1)
    print("SLA  ->", p2)
