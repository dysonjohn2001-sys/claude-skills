"""
gen_executive.py — Deliverable 1: Executive Deal Summary & Term Sheet
Lumbee Tribe of North Carolina / RIVR Tech broadband IRU transaction package.

Generates 01_Executive/Lumbee_RIVR_Executive_Deal_Summary_and_Term_Sheet.docx
using the canonical constants and formatting engine in common.py.

All commercial economics, routes, fiber counts, and grant figures are placeholders
(C.PH). Governing-law, jurisdiction, dispute-resolution and sovereign-immunity
positions are presented as bracketed ALTERNATIVES flagged for attorney review and are
never silently selected. The Lumbee federal-recognition threshold issue is flagged,
not resolved.
"""

import sys
sys.path.insert(0, '/home/user/claude-skills/Lumbee_RIVR_Tech_IRU_Package/Scripts')
import common as C


def build():
    doc = C.new_doc()

    # -- Cover / front matter -------------------------------------------------
    C.add_cover(
        doc,
        "DOCUMENT 01 — EXECUTIVE DEAL SUMMARY & TERM SHEET",
        "Executive Deal Summary and Term Sheet",
        f"{C.TRIBE_FULL} / {C.OPERATOR_SHORT} Broadband Partnership",
    )
    C.setup_header_footer(doc, "Executive Deal Summary & Term Sheet")
    C.add_toc(doc)
    C.status_banner(doc)
    C.para(
        doc,
        "This Executive Deal Summary and Term Sheet (this “Summary”) describes the "
        f"proposed broadband partnership by and between {C.TRIBE_FULL} (the “{C.TRIBE_SHORT}”), "
        f"or {C.TRIBE_ENTITY_ALT}, and {C.OPERATOR_FULL} (“{C.OPERATOR_SHORT}”). It is a "
        "non-binding working draft prepared to frame the transaction, isolate open business "
        "issues, and drive the definitive documents. It does not create legal obligations, is "
        "not an offer, and is subject in all respects to legal, grant-compliance, and financial "
        f"review. Defined terms used but not defined here have the meanings given in the "
        "definitive agreements.",
        italic=True,
    )
    C.spacer(doc, 1)

    # ============================================================ ARTICLE 1
    C.article(doc, 1, "Executive Summary")
    C.section(
        doc, "1.1", "The Opportunity",
        f"The {C.TRIBE_SHORT} intends to apply for, and if awarded to accept, funding under the "
        f"{C.PROGRAM_FULL} ({C.PROGRAM_SHORT}) administered by the {C.AGENCY_FULL} ({C.AGENCY_SHORT}) "
        f"under the {C.NOFO_NAME} to deploy last-mile and distribution fiber broadband "
        f"infrastructure serving unserved and underserved locations in {C.GEOGRAPHY}. The "
        f"{C.TRIBE_SHORT} will be the grant {C.PROGRAM_INCOME and 'recipient'} of record, the legal "
        f"owner of all grant-funded infrastructure, and the entity accountable to {C.AGENCY_SHORT} "
        f"for compliance with the Award. {C.OPERATOR_SHORT} will design, engineer, construct, "
        f"activate, operate, maintain, and commercialize the resulting {C.NETWORK} and will deliver "
        f"residential, business, and enterprise broadband, voice, and related services.")
    C.section(
        doc, "1.2", "The Core Bargain",
        f"The transaction is structured as a public-private partnership in which grant-funded "
        f"assets are owned by the {C.TRIBE_SHORT} and interconnected with {C.OPERATOR_SHORT}’s "
        f"existing middle-mile, backbone, and core network. The {C.TRIBE_SHORT} retains title to the "
        f"{C.TRIBAL_ASSETS} at all times; {C.OPERATOR_SHORT} receives a long-term {C.IRU_TERM_DEFINED} "
        f"({C.IRU_TERM_DEFINED}) to operate and commercialize the {C.TRIBAL_ASSETS} in exchange for "
        f"assuming construction delivery, operating and maintenance obligations, capital-at-risk, "
        f"grant-compliance performance support, and revenue sharing back to the {C.TRIBE_SHORT}. "
        f"Title never transfers to {C.OPERATOR_SHORT}.")
    C.bullet(doc, f"Recommended {C.IRU_TERM_DEFINED} term: {C.IRU_TERM_RECOMMENDED} years, with "
                  f"{C.DEAL['iru_renewal']}, subject to grant-compliance and Federal-Interest "
                  f"constraints.")
    C.bullet(doc, f"Recommended revenue-sharing structure: {C.DEAL['rev_options']['D']} "
                  f"(described in Article 11).")
    C.bullet(doc, f"Clear {C.DEMARCATION} discipline separates {C.TRIBAL_ASSETS} from "
                  f"{C.OPERATOR_ASSETS} so that Federal-Interest, audit, and disposition rules attach "
                  f"only to grant-funded property.")
    C.section(
        doc, "1.3", "Why This Structure",
        f"The ownership-plus-{C.IRU_TERM_DEFINED} model lets the {C.TRIBE_SHORT} satisfy the "
        f"{C.PROGRAM_SHORT} requirement that grant assets be owned and controlled by the Tribal "
        f"government while transferring operational execution and commercial risk to an experienced "
        f"operator that already owns adjacent middle-mile facilities. It preserves Tribal sovereignty "
        f"and long-term asset value, accelerates deployment, and avoids the {C.TRIBE_SHORT} having to "
        f"stand up a full telecommunications operating company. It also keeps the Federal Interest "
        f"cleanly identifiable, which is essential for {C.AGENCY_SHORT} reporting, audit, and "
        f"disposition.")

    # Prominent threshold-issue box
    C.spacer(doc, 1)
    C.para(doc, "THRESHOLD ELIGIBILITY ISSUE — MUST BE RESOLVED BEFORE APPLICATION", bold=True)
    C.flag_para(
        doc, C.FLAG_GRANT,
        f"The {C.TRIBE_SHORT}’s status under the {C.CITES['lumbee_act']} directly affects whether "
        f"the {C.TRIBE_SHORT} qualifies as a “Tribal Government” eligible for {C.PROGRAM_SHORT} "
        f"funding. The Lumbee Act granted federal recognition of the Lumbee as Indians but has been "
        f"historically construed to withhold eligibility for certain federal Indian programs and "
        f"services. Whether the {C.TRIBE_SHORT} (or a designated Tribal entity) meets the "
        f"{C.PROGRAM_SHORT} definition of an eligible entity is a gating question that determines "
        f"whether this transaction can proceed at all.")
    C.flag_para(
        doc, C.FLAG_ATTORNEY,
        f"Eligibility counsel and grant counsel must confirm, in writing and before any application "
        f"is filed, the eligibility basis on which the {C.TRIBE_SHORT} will apply (e.g., statutory "
        f"recognition, applicable {C.AGENCY_SHORT} guidance, or an alternative eligible applicant/"
        f"co-applicant structure). This Summary does not resolve the question and assumes, solely for "
        f"drafting purposes, that eligibility is or will be established. All downstream provisions are "
        f"contingent on that confirmation. {C.PH('eligibility determination basis and supporting opinion')}.")

    # ============================================================ ARTICLE 2
    C.article(doc, 2, "Purpose of the Partnership")
    C.section(
        doc, "2.1", "Shared Objectives",
        f"The Parties intend to close the broadband gap in {C.GEOGRAPHY} by deploying a modern "
        f"fiber-optic {C.NETWORK} capable of delivering service at or above the {C.PROGRAM_SHORT} "
        f"speed floor of {C.SPEED_FLOOR}, prioritizing unserved and underserved Tribal and "
        f"community locations, anchor institutions, and Tribal government facilities.")
    C.bullet(doc, f"For the {C.TRIBE_SHORT}: durable Tribally owned infrastructure, digital equity for "
                  f"members, revenue to the Tribal government, reserved capacity for Tribal use, and "
                  f"full compliance with the Award.")
    C.bullet(doc, f"For {C.OPERATOR_SHORT}: a long-term operating footprint that leverages existing "
                  f"backbone assets, a subscriber base, and a predictable commercial return over the "
                  f"{C.IRU_TERM_DEFINED} term.")
    C.section(
        doc, "2.2", "Guiding Principles",
        "The definitive documents will be drafted to honor five principles that govern every "
        "downstream provision:")
    C.numbered(doc, f"Tribal ownership and sovereignty are preserved; title to {C.TRIBAL_ASSETS} never "
                    f"leaves the {C.TRIBE_SHORT}.")
    C.numbered(doc, "Grant compliance is paramount; no commercial term may override the Award, "
                    f"{C.CITES['ug_part']}, or {C.AGENCY_SHORT} conditions.")
    C.numbered(doc, "Risk follows capability; the Party best able to manage a given risk bears it.")
    C.numbered(doc, "Economics are transparent, auditable, and separable from the Federal Interest.")
    C.numbered(doc, "Continuity of service to Tribal members and anchor institutions is protected "
                    "through step-in and transition rights.")

    # ============================================================ ARTICLE 3
    C.article(doc, 3, "Proposed Transaction Structure")
    C.section(
        doc, "3.1", "Documentary Architecture",
        "The relationship is expected to be implemented through a suite of definitive documents, "
        "each cross-referencing this Summary’s allocation of ownership, risk, and economics:")
    C.add_table(
        doc,
        ["Instrument", "Primary Purpose", "Primary Party Obligations"],
        [
            ["Master Partnership / Framework Agreement",
             "Umbrella terms, defined terms, conditions precedent, compliance covenants",
             f"Both {C.PARTIES_COLLECTIVE}"],
            [f"{C.IRU_TERM_DEFINED} Agreement",
             f"Grant of the long-term right to use and commercialize the {C.TRIBAL_ASSETS}",
             f"{C.TRIBE_SHORT} grants; {C.OPERATOR_SHORT} holds"],
            ["Design-Build / Construction Agreement",
             "Engineering, procurement, and construction of the Grant-Funded Infrastructure",
             f"{C.OPERATOR_SHORT} performs"],
            ["Operations & Maintenance (O&M) Agreement",
             "Operation, maintenance, NOC, and SLA performance",
             f"{C.OPERATOR_SHORT} performs"],
            ["Revenue-Share / Financial Schedule",
             "Consideration, revenue definitions, sharing mechanics, reporting",
             f"Both {C.PARTIES_COLLECTIVE}"],
            ["Grant-Compliance & Federal-Interest Rider",
             f"Flow-down of Award, {C.CITES['ug_2024']}, BABA, NEPA/NHPA obligations",
             f"Both {C.PARTIES_COLLECTIVE}"],
        ],
        widths=[1.9, 2.6, 2.0],
    )
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Whether these are separate executed instruments or exhibits to a single master "
                "agreement is a structuring choice with tax, assignment, and lender-consent "
                "consequences. Counsel to confirm the documentary architecture.")
    C.section(
        doc, "3.2", "Alternative Structures Considered",
        "Two alternatives were considered and are not recommended, for the reasons noted:")
    C.bullet(doc, f"Alternative 1 — Outright transfer/lease of assets to {C.OPERATOR_SHORT}. "
                  f"Rejected: inconsistent with {C.PROGRAM_SHORT} ownership requirements and "
                  f"Federal-Interest/disposition rules; erodes Tribal sovereignty.")
    C.bullet(doc, f"Alternative 2 — {C.TRIBE_SHORT} self-operates the entire {C.NETWORK}. "
                  f"Rejected (for now): requires the {C.TRIBE_SHORT} to build full telecom operating "
                  f"capability and bear operating risk; slower to market. Retained as a fallback "
                  f"through step-in and transition rights (Article 18).")
    C.para(doc, f"Recommendation: proceed with the ownership-plus-{C.IRU_TERM_DEFINED} structure "
                f"described in Section 1.2.", bold=True)

    # ============================================================ ARTICLE 4
    C.article(doc, 4, "Roles of the Tribe and RIVR Tech")
    C.section(doc, "4.1", f"Role of the {C.TRIBE_SHORT}",
              f"The {C.TRIBE_SHORT} acts as grant recipient, asset owner, and compliance principal.")
    for t in [
        f"Applies for and, if awarded, accepts and administers the {C.PROGRAM_SHORT} Award as the "
        f"recipient of record and pass-through entity where applicable ({C.CITES['pass_through']}).",
        f"Holds and retains title to all {C.TRIBAL_ASSETS} and maintains the property and "
        f"inventory records required by {C.CITES['equipment']} and {C.CITES['real_property']}.",
        "Grants the IRU to RIVR Tech and enforces the definitive documents.",
        "Exercises governmental functions: rights-of-way on Tribal land, resolutions, and "
        "any limited waiver of sovereign immunity that the Tribal government elects to grant.",
        f"Receives revenue share and reserved capacity, and consumes Tribal government and "
        f"anchor-institution services (Articles 15–16).",
    ]:
        C.bullet(doc, t)
    C.section(doc, "4.2", f"Role of {C.OPERATOR_SHORT}",
              f"{C.OPERATOR_SHORT} acts as developer, operator, and commercial service provider.")
    for t in [
        "Designs, engineers, procures for, constructs, tests, and activates the Grant-Funded "
        "Infrastructure under the Design-Build Agreement.",
        f"Interconnects the {C.TRIBAL_ASSETS} with the {C.OPERATOR_EXISTING} at the {C.DEMARCATION}.",
        f"Operates and maintains the {C.NETWORK}, staffs the NOC "
        f"({C.DEAL['sla']['noc']}), and meets the SLA (Article 7).",
        "Markets and sells services; owns the retail customer relationship, billing, and "
        "collections (Articles 9–10).",
        f"Supports the {C.TRIBE_SHORT}’s grant-compliance, BABA, environmental/historic, "
        f"reporting, and audit obligations by supplying data and certifications.",
        "Pays the agreed consideration and revenue share to the Tribe.",
    ]:
        C.bullet(doc, t)
    C.flag_para(doc, C.FLAG_ATTORNEY,
                f"The definitive documents must characterize {C.OPERATOR_SHORT}’s status "
                f"(contractor vs. subrecipient) under {C.CITES['subrecipient']}; the determination "
                f"drives which compliance obligations flow down and how audit responsibility is "
                f"allocated. This is a legal determination, not a labeling choice.")

    # ============================================================ ARTICLE 5
    C.article(doc, 5, "Asset Ownership Structure")
    C.section(
        doc, "5.1", "Three Asset Classes",
        f"The {C.NETWORK} is a hybrid of three asset classes, each with a distinct ownership and "
        f"compliance profile. The {C.DEMARCATION} is the physical and legal boundary that separates "
        f"them.")
    C.add_table(
        doc,
        ["Asset Class", "Owner", "Funding Source", "Federal Interest / Compliance"],
        [
            [f"{C.TRIBAL_ASSETS} ({C.GRANT_FUNDED})",
             C.TRIBE_SHORT, f"{C.PROGRAM_SHORT} grant funds ({C.PH('grant amount')})",
             f"Federal Interest attaches; full {C.CITES['ug_part']} disposition/audit rules apply"],
            [f"{C.OPERATOR_ASSETS} ({C.OPERATOR_EXISTING})",
             C.OPERATOR_SHORT, f"{C.OPERATOR_SHORT} private capital",
             "No Federal Interest; owned and controlled by RIVR Tech"],
            [C.JOINT_ASSETS,
             f"Allocated by contribution {C.PH('ownership split methodology')}",
             "Mixed grant + private (if any)",
             "Federal Interest attaches pro-rata to grant-funded portion; segregated accounting"],
        ],
        widths=[1.9, 1.4, 1.9, 2.3],
    )
    C.section(
        doc, "5.2", "Demarcation Discipline",
        f"A written, as-built {C.DEMARCATION} schedule will identify, at each interconnection, the "
        f"exact panel, port, splice, handhole, or rack unit at which {C.TRIBAL_ASSETS} end and "
        f"{C.OPERATOR_ASSETS} begin. This schedule governs Federal-Interest scope, insurance, "
        f"maintenance responsibility, and disposition. It is maintained as a controlled document and "
        f"updated as-built.")
    C.flag_para(doc, C.FLAG_TECH,
                f"The precise physical demarcation points, fiber counts on each side, and the "
                f"interconnection method are to be fixed in the final network design. "
                f"{C.PH('demarcation schedule: sites, panels/ports, fiber counts, GPS coordinates')}.")
    C.section(
        doc, "5.3", "Title, Encumbrance, and Disposition",
        f"Title to the {C.TRIBAL_ASSETS} vests in the {C.TRIBE_SHORT} upon acquisition/installation "
        f"and remains with the {C.TRIBE_SHORT}. The {C.IRU_TERM_DEFINED} is a right of use, not a "
        f"conveyance of title. Any encumbrance, lien, sale, or disposition of {C.TRIBAL_ASSETS} is "
        f"subject to {C.CITES['real_property']} and {C.CITES['equipment']} and requires "
        f"{C.AGENCY_SHORT} approval during the Federal-Interest period.")
    C.flag_para(doc, C.FLAG_GRANT,
                f"Any lender collateral assignment of the {C.IRU_TERM_DEFINED} or leasehold-style "
                f"financing by {C.OPERATOR_SHORT} must be reconciled with the prohibition on "
                f"encumbering federally funded property without {C.AGENCY_SHORT} consent.")

    # ============================================================ ARTICLE 6
    C.article(doc, 6, "IRU Structure — Term, Renewal, and Recommendation")
    C.section(
        doc, "6.1", "Nature of the IRU",
        f"The {C.TRIBE_SHORT} grants {C.OPERATOR_SHORT} an indefeasible right to use, operate, "
        f"manage, and commercialize the {C.TRIBAL_ASSETS} and the resulting {C.NETWORK} for the IRU "
        f"term, subject to the {C.TRIBE_SHORT}’s retained title, reserved capacity, and the "
        f"Award. The {C.IRU_TERM_DEFINED} is exclusive as to commercial operation but subject to the "
        f"{C.TRIBE_SHORT}’s reserved fiber and government-use rights (Article 15) and to "
        f"step-in rights (Article 18).")
    C.section(doc, "6.2", "Term Alternatives Modeled",
              "Three IRU terms were modeled. The economics and Federal-Interest exposure differ; the "
              "longer the term, the greater RIVR Tech’s incentive to invest and the lower the "
              "annualized cost of capital, balanced against Tribal flexibility.")
    C.add_table(
        doc,
        ["Alternative", "Initial Term", "Renewals", "Assessment"],
        [
            ["Alt. 1", "20 years", C.DEAL['iru_renewal'],
             "Shortest; maximum Tribal flexibility; highest annualized operator return required; "
             "weakest investment incentive"],
            ["Alt. 2", "25 years", C.DEAL['iru_renewal'],
             "Balanced; aligns with typical fiber depreciation life; moderate flexibility"],
            ["Alt. 3 (recommended)", "30 years", C.DEAL['iru_renewal'],
             "Longest initial term; strongest investment incentive and lowest annualized cost; "
             "matches long-life fiber assets; requires robust step-in and mid-term review"],
        ],
        widths=[1.3, 1.2, 2.0, 3.0],
        col_align=["c", "c", None, None],
    )
    C.para(doc, f"Recommendation: adopt a {C.IRU_TERM_RECOMMENDED}-year initial term with "
                f"{C.DEAL['iru_renewal']}. A {C.IRU_TERM_RECOMMENDED}-year term best matches the "
                f"physical and economic life of fiber plant, secures {C.OPERATOR_SHORT}’s "
                f"long-term investment, and lowers the return the operator must charge — improving "
                f"the revenue share available to the {C.TRIBE_SHORT} — while renewals and step-in "
                f"rights preserve Tribal control.", bold=True)
    C.section(doc, "6.3", "Consideration for the IRU",
              f"The IRU consideration is {C.DEAL['iru_prepaid_consideration']}. The economic core of "
              f"the bargain is the bundle of construction, operating, maintenance, capital-at-risk, "
              f"and revenue-sharing obligations, not a lump-sum purchase price.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                f"Whether any up-front IRU payment is made to the {C.TRIBE_SHORT} at closing, and its "
                f"amount, is an open commercial term. {C.PH('up-front IRU payment, if any')}.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                f"An IRU term (plus renewals) that could approach or exceed the useful life or the "
                f"Federal-Interest period must be checked against {C.CITES['equipment']} and Award "
                f"terms so that it is not recharacterized as a disposition of federally funded "
                f"property. Renewal exercise during the Federal-Interest period may require "
                f"{C.AGENCY_SHORT} notice or consent.")

    # ============================================================ ARTICLE 7
    C.article(doc, 7, "Operating Model")
    C.section(
        doc, "7.1", "Operator Responsibility",
        f"{C.OPERATOR_SHORT} operates the {C.NETWORK} as a single integrated system, blending the "
        f"{C.TRIBAL_ASSETS} with the {C.OPERATOR_EXISTING} to deliver end-to-end services. "
        f"{C.OPERATOR_SHORT} staffs and runs the Network Operations Center "
        f"({C.DEAL['sla']['noc']}), performs monitoring, provisioning, fault management, and field "
        f"operations, and is accountable for network performance.")
    C.section(doc, "7.2", "Service-Level Framework",
              "Operations are governed by an SLA with severity-based response, dispatch, and "
              "restoration targets and a network-availability commitment. The canonical targets are:")
    C.add_table(
        doc,
        ["Metric", "Target"],
        [
            ["Network availability", C.DEAL['sla']['availability_target']],
            ["P1 (critical) response / dispatch / restore",
             f"{C.DEAL['sla']['P1_response_min']} min / {C.DEAL['sla']['P1_dispatch_hr']} hr / "
             f"{C.DEAL['sla']['P1_restore_hr']} hr"],
            ["P2 (major) response / dispatch / restore",
             f"{C.DEAL['sla']['P2_response_min']} min / {C.DEAL['sla']['P2_dispatch_hr']} hr / "
             f"{C.DEAL['sla']['P2_restore_hr']} hr"],
            ["P3 (minor) response / dispatch / restore",
             f"{C.DEAL['sla']['P3_response_hr']} hr / {C.DEAL['sla']['P3_dispatch_hr']} hr / "
             f"{C.DEAL['sla']['P3_restore_days']} days"],
            ["Latency / packet loss / jitter",
             f"≤ {C.DEAL['sla']['latency_ms']} ms / ≤ {C.DEAL['sla']['packet_loss']} / "
             f"≤ {C.DEAL['sla']['jitter_ms']} ms"],
        ],
        widths=[3.4, 3.6],
    )
    C.para(doc, "Detailed SLA definitions, measurement methods, and remedies (credits/escalation) "
                "are set out in the O&M Agreement and its SLA exhibit.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                "SLA credits, chronic-failure thresholds, and any performance-linked adjustment to "
                "the revenue share are open commercial terms.")

    # ============================================================ ARTICLE 8
    C.article(doc, 8, "Construction Model")
    C.section(
        doc, "8.1", "Design-Build Delivery",
        f"{C.OPERATOR_SHORT} delivers the Grant-Funded Infrastructure under a design-build model: "
        f"final engineering, procurement, construction, splicing, testing, and activation, to an "
        f"agreed scope, schedule, and acceptance standard. Assets are built to the "
        f"{C.TRIBE_SHORT}’s account and titled to the {C.TRIBE_SHORT} as installed.")
    C.section(doc, "8.2", "Grant-Compliant Procurement and Materials",
              f"Because construction is funded by the Award, procurement and materials must comply "
              f"with federal requirements even though {C.OPERATOR_SHORT} performs the work:")
    C.bullet(doc, f"Procurement standards and competition: {C.CITES['procurement']}, "
                  f"{C.CITES['competition']}, {C.CITES['methods']}.")
    C.bullet(doc, f"Build America, Buy America: {C.CITES['baba']} — iron, steel, manufactured "
                  f"products, and construction materials must meet BABA unless a waiver applies.")
    C.bullet(doc, f"Covered-equipment prohibition: {C.CITES['telecom_ban']} (§889).")
    C.bullet(doc, f"Domestic preference and conflict-of-interest rules: {C.CITES['domestic']}, "
                  f"{C.CITES['conflict']}.")
    C.section(doc, "8.3", "Environmental and Historic Review",
              f"Construction may not begin on affected segments until required environmental and "
              f"historic-preservation review is complete: {C.CITES['nepa']} and "
              f"{C.CITES['nhpa']}. The {C.TRIBE_SHORT} (as recipient) is responsible to "
              f"{C.AGENCY_SHORT}; {C.OPERATOR_SHORT} supports the reviews and honors any conditions, "
              f"including Tribal Historic Preservation consultation.")
    C.section(doc, "8.4", "Testing and Acceptance",
              f"Completed plant is accepted against optical and functional standards before the "
              f"asset is placed in service and before the corresponding IRU operating rights attach. "
              f"Acceptance testing uses {C.OPTICAL['otdr']} at {C.OPTICAL['wavelengths']} with splice "
              f"loss ≤ {C.OPTICAL['splice_loss_max']} and connector loss "
              f"≤ {C.OPTICAL['connector_loss_max']}.")
    C.flag_para(doc, C.FLAG_TECH,
                f"Final route miles, fiber counts, homes/locations passed, and the construction "
                f"schedule are to be fixed in the design. "
                f"{C.PH('route miles, fiber counts, locations passed, milestone schedule')}.")

    # ============================================================ ARTICLE 9
    C.article(doc, 9, "Customer Relationship Model")
    C.section(
        doc, "9.1", "Retail Relationship Owned by RIVR Tech",
        f"{C.OPERATOR_SHORT} owns the retail relationship with residential, business, and enterprise "
        f"subscribers: service offers, provisioning, support, and contracts are between "
        f"{C.OPERATOR_SHORT} and the end user. {C.OPERATOR_SHORT} is the service provider of record "
        f"and holds any required authorizations.")
    C.bullet(doc, f"{C.OPERATOR_SHORT} bears customer-acquisition and churn risk.")
    C.bullet(doc, f"Customer data is handled under applicable privacy law, including CPNI "
                  f"({C.CITES['cpni']}); the {C.TRIBE_SHORT} receives aggregate reporting, not "
                  f"individual customer data, except as needed for Tribal-member programs it "
                  f"sponsors.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                f"If any low-income or Lifeline/ETC subsidy is used, {C.CITES['usac_lifeline']} "
                f"eligibility, ETC designation, and USAC obligations must be addressed. Ownership of "
                f"the subscriber base on termination is addressed in Articles 17–18.")
    C.section(doc, "9.2", "Tribal-Member Benefits",
              f"The Parties intend a Tribal-member benefit (e.g., preferential pricing, priority "
              f"connection, or a digital-equity program). Scope and funding are open.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                f"Tribal-member pricing/benefit design and who funds it. "
                f"{C.PH('Tribal-member benefit program terms')}.")

    # ============================================================ ARTICLE 10
    C.article(doc, 10, "Revenue Collection Model")
    C.section(
        doc, "10.1", "Billing and Collections",
        f"{C.OPERATOR_SHORT} bills subscribers and collects all service revenue, bearing bad-debt "
        f"and collection risk. Gross service revenue is booked by {C.OPERATOR_SHORT} and then shared "
        f"with the {C.TRIBE_SHORT} per the elected revenue-share option (Article 11).")
    C.section(
        doc, "10.2", "Program Income Characterization",
        f"Revenue derived from the use of grant-funded property may constitute Program Income under "
        f"{C.CITES['prog_income']}. The treatment of that income (added to the project, deducted, or "
        f"matched) must be fixed with grant counsel, because it affects how the revenue share may be "
        f"structured and reported during the Federal-Interest period.")
    C.flag_para(doc, C.FLAG_GRANT,
                f"Program-income treatment ({C.CITES['prog_income']}) is a gating compliance "
                f"determination that constrains the revenue-share mechanics. It must be resolved "
                f"before the Financial Schedule is finalized.")
    C.section(doc, "10.3", "Reporting and Audit Trail",
              f"{C.OPERATOR_SHORT} maintains auditable revenue records and provides the "
              f"{C.TRIBE_SHORT} with periodic statements and audit access sufficient to support "
              f"{C.AGENCY_SHORT} reporting and single-audit requirements "
              f"({C.CITES['records']}; {C.CITES['single_audit']}).")

    # ============================================================ ARTICLE 11
    C.article(doc, 11, "Revenue-Sharing Alternatives")
    C.section(
        doc, "11.1", "Five Modeled Options",
        f"Five revenue-sharing structures were modeled. Each shares upside with the {C.TRIBE_SHORT} "
        f"differently and allocates revenue and cost risk differently between the {C.PARTIES_COLLECTIVE}. "
        f"All percentages and dollar figures below are placeholders for the Financial Model.")
    C.add_table(
        doc,
        ["Option", "Mechanic", "Tribe Bears", "Operator Bears", "Notes"],
        [
            [C.DEAL['rev_options']['A'],
             f"Fixed annual payment to the {C.TRIBE_SHORT} ({C.PH('fixed annual amount')})",
             "No revenue-volatility upside", "All revenue and cost risk",
             "Most predictable for the Tribe; no upside participation"],
            [C.DEAL['rev_options']['B'],
             f"{C.PH('% of gross revenue')} of gross service revenue "
             f"(placeholder {C.DEAL['rev_share_pct_placeholder']})",
             "Revenue risk (shares downside)", "Cost risk",
             "Simple, auditable; ignores operator cost structure"],
            [C.DEAL['rev_options']['C'],
             f"{C.PH('% of adjusted operating cash flow')} of adjusted operating cash flow "
             f"(placeholder {C.DEAL['cashflow_share_pct_placeholder']})",
             "Revenue and cost risk", "Cost risk (definitions matter)",
             "Aligns to profitability; requires tight definitions/audit of costs"],
            [f"{C.DEAL['rev_options']['D']} (recommended)",
             f"Fixed base ({C.PH('base amount')}) plus {C.PH('% share')} revenue share",
             "Partial revenue risk above the base", "Cost risk; guarantees the base",
             "Floor for the Tribe plus upside; balances predictability and alignment"],
            [C.DEAL['rev_options']['E'],
             f"Initial payment holiday, then stepped payments ({C.PH('step schedule')})",
             "Deferred cash in early years", "Ramp/adoption risk",
             "Eases early operator cash flow during build/ramp; back-loads Tribal cash"],
        ],
        widths=[1.6, 2.0, 1.3, 1.3, 1.8],
        font_size=8,
    )
    C.section(
        doc, "11.2", "Recommendation",
        f"Recommendation: adopt {C.DEAL['rev_options']['D']}. Option D gives the {C.TRIBE_SHORT} a "
        f"guaranteed annual floor (protecting the Tribal government against ramp and revenue "
        f"volatility) while preserving meaningful upside participation as subscribership grows. It "
        f"is more auditable than a pure cash-flow share (Option C), whose cost definitions invite "
        f"dispute, and more equitable than a flat fixed payment (Option A), which strands Tribal "
        f"upside. A modest early-year step (borrowing from Option E) can be layered into the base to "
        f"accommodate the build/ramp period.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                f"The base amount, share percentage, revenue definition, and any early-year step are "
                f"the central commercial negotiation. "
                f"{C.PH('Option D base, share %, revenue definition, step schedule')}.")
    C.flag_para(doc, C.FLAG_GRANT,
                f"Whatever option is chosen must be reconciled with Program-Income rules "
                f"({C.CITES['prog_income']}) during the Federal-Interest period.")

    # ============================================================ ARTICLE 12
    C.article(doc, 12, "Maintenance-Cost Allocation")
    C.section(
        doc, "12.1", "Routine and Preventive Maintenance",
        f"{C.OPERATOR_SHORT} performs and bears the cost of routine, preventive, and corrective "
        f"maintenance of the {C.NETWORK} necessary to meet the SLA, as part of its operating "
        f"obligations. Maintenance of {C.OPERATOR_ASSETS} is entirely {C.OPERATOR_SHORT}’s.")
    C.section(
        doc, "12.2", "Extraordinary and Third-Party-Caused Damage",
        f"Costs to repair damage caused by third parties (e.g., dig-ins, vehicle strikes) are "
        f"pursued against the responsible party; net unrecovered costs and force-majeure/catastrophic "
        f"restoration are allocated per the O&M Agreement. Utility-locate and pole-attachment "
        f"obligations follow {C.CITES['nc_dig']} and {C.CITES['nc_pole']}.")
    C.add_table(
        doc,
        ["Maintenance Category", "Cost Borne By", "Basis"],
        [
            ["Routine / preventive / SLA-corrective (Tribal + Operator assets)",
             C.OPERATOR_SHORT, "Part of operating obligation"],
            ["Third-party-caused damage",
             "Responsible third party; net shortfall per O&M",
             "Subrogation / cost-recovery first"],
            ["Catastrophic / force-majeure restoration of Tribal Assets",
             f"{C.PH('allocation — insurance first, then shared/Tribal')}",
             f"Insurance ({C.CITES['insurance']}) then allocation"],
            ["Maintenance of RIVR Tech Assets",
             C.OPERATOR_SHORT, "Operator-owned facilities"],
        ],
        widths=[3.0, 2.2, 1.8],
    )
    C.flag_para(doc, C.FLAG_BUSINESS,
                "The catastrophic/force-majeure cost-sharing formula for Tribal Assets (after "
                "insurance) is an open term.")

    # ============================================================ ARTICLE 13
    C.article(doc, 13, "Replacement-Capital Responsibility")
    C.section(
        doc, "13.1", "Lifecycle Replacement and Renewal",
        f"Fiber plant is long-lived, but electronics, optics, and certain passive components require "
        f"periodic replacement within the {C.IRU_TERM_DEFINED} term. Responsibility for replacement "
        f"capital (capex) must be allocated so that the {C.TRIBE_SHORT} receives the {C.NETWORK} in "
        f"good condition at expiry and {C.OPERATOR_SHORT} has incentives to maintain and modernize.")
    C.bullet(doc, f"Electronics/active equipment (often {C.OPERATOR_ASSETS}): replaced by "
                  f"{C.OPERATOR_SHORT} at its cost as part of operating the {C.NETWORK}.")
    C.bullet(doc, f"Grant-funded {C.TRIBAL_ASSETS} replacement: allocation options include a "
                  f"{C.OPERATOR_SHORT}-funded renewal obligation, a jointly funded reserve, or a "
                  f"Tribal reserve funded from revenue share.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                f"Replacement-capital responsibility and any capital-reserve funding mechanism are "
                f"open. Recommended default: {C.OPERATOR_SHORT} funds like-for-like replacement of "
                f"Tribal Assets needed to sustain service, with a hand-back condition standard at "
                f"expiry. {C.PH('capex allocation and reserve mechanism')}.")
    C.flag_para(doc, C.FLAG_GRANT,
                f"Replacement of grant-funded property, and any use of insurance/replacement proceeds, "
                f"is subject to {C.CITES['equipment']} and {C.CITES['intangible']} during the "
                f"Federal-Interest period.")

    # ============================================================ ARTICLE 14
    C.article(doc, 14, "Grant-Compliance Responsibilities")
    C.section(
        doc, "14.1", "Recipient Accountability, Operator Support",
        f"The {C.TRIBE_SHORT} is accountable to {C.AGENCY_SHORT} for the Award. Compliance duties are "
        f"flowed down to {C.OPERATOR_SHORT} through the Grant-Compliance Rider so that the entity "
        f"performing the work also performs the associated compliance and recordkeeping.")
    C.add_table(
        doc,
        ["Compliance Domain", "Authority", "Lead", "Support"],
        [
            ["Uniform Guidance administration", C.CITES['ug_2024'], C.TRIBE_SHORT, C.OPERATOR_SHORT],
            ["Procurement & competition", C.CITES['procurement'], C.OPERATOR_SHORT, "Grant counsel"],
            ["Build America, Buy America", C.CITES['baba'], C.OPERATOR_SHORT, C.TRIBE_SHORT],
            ["Covered-equipment (§889)", C.CITES['telecom_ban'], C.OPERATOR_SHORT, C.TRIBE_SHORT],
            ["Environmental / historic", f"{C.CITES['nepa']}; {C.CITES['nhpa']}", C.TRIBE_SHORT, C.OPERATOR_SHORT],
            ["Property & inventory records", C.CITES['equipment'], C.TRIBE_SHORT, C.OPERATOR_SHORT],
            ["Program income", C.CITES['prog_income'], C.TRIBE_SHORT, C.OPERATOR_SHORT],
            ["Records retention & access", C.CITES['records'], "Both", "Both"],
            ["Single audit", C.CITES['single_audit'], C.TRIBE_SHORT, C.OPERATOR_SHORT],
            ["Reporting to NTIA", C.CITES['sac'], C.TRIBE_SHORT, C.OPERATOR_SHORT],
        ],
        widths=[1.9, 2.7, 1.2, 1.2],
        font_size=8,
    )
    C.flag_para(doc, C.FLAG_GRANT,
                f"The compliance flow-down and the contractor-vs-subrecipient determination "
                f"({C.CITES['subrecipient']}) govern which obligations bind {C.OPERATOR_SHORT} "
                f"directly. Grant counsel to finalize the Rider.")

    # ============================================================ ARTICLE 15
    C.article(doc, 15, "Reserved Tribal Fiber and Capacity")
    C.section(
        doc, "15.1", "Reserved Strands and Capacity",
        f"The {C.TRIBE_SHORT} reserves, for its own governmental and community use, dedicated dark "
        f"fiber strands and/or lit capacity on the {C.TRIBAL_ASSETS}, at no recurring charge or at a "
        f"cost-based rate, exempt from the commercial {C.IRU_TERM_DEFINED}. This reservation is "
        f"carved out of {C.OPERATOR_SHORT}’s operating rights and survives assignment.")
    C.bullet(doc, f"Reserved dark fiber: {C.PH('number of reserved strands per segment')}.")
    C.bullet(doc, f"Reserved lit capacity for Tribal government/anchor sites: "
                  f"{C.PH('reserved bandwidth per site')}.")
    C.bullet(doc, f"Priority restoration for reserved capacity following {C.OPERATOR_SHORT}’s "
                  f"own critical services.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                "Quantity of reserved strands/capacity, pricing (free vs. cost-based), and priority "
                "level are open commercial terms.")

    # ============================================================ ARTICLE 16
    C.article(doc, 16, "Tribal Government and Anchor-Institution Services")
    C.section(
        doc, "16.1", "Government and Anchor Connectivity",
        f"{C.OPERATOR_SHORT} will connect and serve Tribal government facilities and community "
        f"anchor institutions (e.g., schools, libraries, health/clinic, public-safety, and "
        f"administrative sites) at defined service levels and preferential rates, consistent with "
        f"the {C.PROGRAM_SHORT} emphasis on anchor connectivity.")
    C.add_table(
        doc,
        ["Service", "Beneficiary", "Commercial Basis"],
        [
            ["Dedicated government WAN / Internet", "Tribal government facilities",
             f"{C.PH('preferential / cost-based rate')}"],
            ["Anchor-institution broadband", "Schools, library, clinic, public safety",
             f"{C.PH('anchor rate schedule')}"],
            ["Reserved capacity (see Article 15)", "Tribe", "No charge / cost-based"],
        ],
        widths=[2.6, 2.4, 2.0],
    )
    C.flag_para(doc, C.FLAG_BUSINESS,
                "Anchor-institution site list, service levels, and rate schedule are open. "
                f"{C.PH('anchor site list and SLAs')}.")

    # ============================================================ ARTICLE 17
    C.article(doc, 17, "Renewal and Termination Structure")
    C.section(
        doc, "17.1", "Renewal",
        f"The {C.IRU_TERM_DEFINED} provides {C.DEAL['iru_renewal']} exercisable by "
        f"{C.OPERATOR_SHORT} on notice, provided {C.OPERATOR_SHORT} is not in uncured material "
        f"default and the {C.NETWORK} meets a hand-back/condition standard, subject to any "
        f"{C.AGENCY_SHORT} consent then required.")
    C.section(doc, "17.2", "Termination for Cause and Cure",
              "Either Party may terminate for the other’s uncured material default, subject to "
              "notice and cure:")
    C.bullet(doc, f"Monetary default: cure period of {C.DEAL['cure_monetary_days']} days after "
                  f"notice.")
    C.bullet(doc, f"Non-monetary default: cure period of {C.DEAL['cure_nonmonetary_days']} days, "
                  f"with {C.DEAL['cure_nonmonetary_extension']}.")
    C.bullet(doc, f"Default notice period: {C.DEAL['notice_default_days']} days.")
    C.section(doc, "17.3", "Termination for Grant/Compliance Events",
              f"The definitive documents must address termination or suspension arising from Award "
              f"termination, {C.AGENCY_SHORT} action, or compliance failure "
              f"({C.CITES['remedies']}), including which Party’s conduct triggered the event and "
              f"the consequences for the {C.IRU_TERM_DEFINED} and revenue share.")
    C.section(doc, "17.4", "Effect of Termination and Expiry",
              f"On termination or expiry, operational control of the {C.TRIBAL_ASSETS} returns to "
              f"the {C.TRIBE_SHORT} (or its designee) in the required condition; the {C.TRIBE_SHORT} "
              f"retains title throughout; and the {C.PARTIES_COLLECTIVE} implement the transition "
              f"plan (Article 18). Post-termination obligations, records access, and Program-Income "
              f"true-up survive.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Termination triggers, cross-defaults among the definitive documents, and the "
                "consequences of a grant-driven termination (including whether it is a Tribe-side or "
                "Operator-side risk) must be tailored by counsel.")

    # ============================================================ ARTICLE 18
    C.article(doc, 18, "Step-In and Transition Rights")
    C.section(
        doc, "18.1", "Tribal Step-In Rights",
        f"To protect continuity of Essential Services and Award compliance, the {C.TRIBE_SHORT} (or "
        f"its designee) may step in to operate or cause operation of the {C.NETWORK} upon defined "
        f"triggers, including {C.OPERATOR_SHORT} insolvency, abandonment, chronic SLA failure, or a "
        f"compliance breach that imperils the Award. Emergency step-in is "
        f"{C.DEAL['stepin_emergency']}.")
    C.section(doc, "18.2", "Transition Assistance",
              f"On expiry or termination, {C.OPERATOR_SHORT} provides transition assistance for up to "
              f"{C.DEAL['transition_assistance_months']} months: knowledge transfer, records, "
              f"network documentation, key third-party assignments, and continuity of subscriber "
              f"service, so the {C.TRIBE_SHORT} or a successor operator can assume operations without "
              f"service interruption.")
    C.bullet(doc, "Delivery of as-built records, the demarcation schedule, and network management "
                  "access/credentials.")
    C.bullet(doc, "Assignment or replacement of essential third-party agreements (transport, poles, "
                  "peering) where assignable.")
    C.bullet(doc, "Treatment of the subscriber base and in-flight service obligations.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Step-in triggers, the scope of any limited sovereign-immunity considerations when "
                "the Tribe operates, subscriber-base ownership on transition, and lender step-in/"
                "cure rights must be reconciled by counsel.")

    # ============================================================ ARTICLE 19
    C.article(doc, 19, "Major Unresolved Business Issues")
    C.para(doc, "The following material commercial terms are open and must be resolved before the "
                "definitive documents can be finalized. Each is a placeholder to be filled from the "
                "Financial Model and negotiation.")
    for issue in [
        f"Grant amount and matching-fund requirement. {C.PH('grant amount; match, if any')}.",
        f"Revenue-share economics under recommended Option D: base, share %, revenue definition, "
        f"early-year step. {C.PH('Option D economics')}.",
        f"Any up-front IRU payment to the {C.TRIBE_SHORT}. {C.PH('up-front payment, if any')}.",
        f"Replacement-capital responsibility and capital-reserve mechanism. {C.PH('capex/reserve terms')}.",
        f"Catastrophic/force-majeure cost-sharing for {C.TRIBAL_ASSETS} after insurance. "
        f"{C.PH('cost-share formula')}.",
        f"Reserved Tribal fiber/capacity quantity, pricing, and priority. {C.PH('reserved capacity terms')}.",
        f"Anchor-institution site list, SLAs, and rate schedule. {C.PH('anchor terms')}.",
        f"Tribal-member benefit/pricing program and its funding. {C.PH('member program terms')}.",
        f"SLA credits, chronic-failure thresholds, and any performance-linked share adjustment. "
        f"{C.PH('SLA remedy economics')}.",
        f"Final route, fiber counts, and locations passed. {C.PH('network design metrics')}.",
    ]:
        C.numbered(doc, issue)
    C.flag_para(doc, C.FLAG_BUSINESS,
                "This list is the negotiation agenda; none of these terms is settled by this Summary.")

    # ============================================================ ARTICLE 20
    C.article(doc, 20, "Recommended Negotiating Positions for RIVR Tech")
    C.para(doc, f"The following positions protect {C.OPERATOR_SHORT}’s ability to invest, "
                f"operate, and earn a return, and are offered as advocacy positions for "
                f"{C.OPERATOR_SHORT} — not as balanced or final terms.")
    for pos in [
        f"Secure the {C.IRU_TERM_RECOMMENDED}-year term plus {C.DEAL['iru_renewal']} to justify "
        f"long-term capital and lower the required return.",
        "Exclusive commercial operating rights (subject only to the Tribe’s reserved capacity) "
        "to protect the subscriber investment.",
        "Adopt Option D with a moderate base and meaningful share, plus an early-year step to "
        "protect ramp-period cash flow.",
        "Cap operator exposure for catastrophic restoration of Tribal Assets to insurance proceeds "
        "plus a defined amount; the balance funded by reserve or Tribe.",
        "Obtain lender-friendly provisions: collateral assignment of the IRU and revenues (subject "
        "to grant constraints), lender cure and step-in rights, and estoppel/consent.",
        "Cure periods no shorter than the canonical defaults; SLA credits capped and sole-remedy "
        "for performance shortfalls short of chronic failure.",
        "Clear demarcation so operator-owned assets and existing backbone remain free of Federal "
        "Interest and Tribal claims.",
        "A workable limited waiver of sovereign immunity and a neutral, enforceable dispute forum "
        "(see Article 22 alternatives).",
    ]:
        C.bullet(doc, pos)
    C.flag_para(doc, C.FLAG_ATTORNEY,
                f"These are one-sided starting positions for {C.OPERATOR_SHORT}; they are not "
                f"legal advice to the {C.TRIBE_SHORT} and several depend on {C.AGENCY_SHORT} and "
                f"grant-compliance constraints.")

    # ============================================================ ARTICLE 21
    C.article(doc, 21, "Recommended Protections for the Tribe")
    C.para(doc, f"The following protections preserve the {C.TRIBE_SHORT}’s ownership, "
                f"sovereignty, compliance posture, and long-term value. They are offered as "
                f"safeguards the {C.TRIBE_SHORT} should seek.")
    for prot in [
        "Retained title to all Tribal Assets at all times; the IRU is a use right only, expressly "
        "not a conveyance.",
        "Robust step-in rights and up-to-12-month transition assistance to guarantee continuity if "
        "the operator fails.",
        "A guaranteed revenue floor (Option D base) so the Tribal government is paid regardless of "
        "adoption ramp.",
        "Reserved dark fiber and lit capacity for Tribal government and community use, carved out "
        "of the IRU and surviving assignment.",
        "Hand-back/condition standard and operator-funded lifecycle replacement so the Network is "
        "returned in good order.",
        "Full audit and records access; operator indemnity for compliance failures caused by the "
        "operator; insurance naming the Tribe as additional insured.",
        "Approval rights over assignment, change of control, and any encumbrance of the IRU; "
        "anti-forfeiture protection of Tribal Assets from operator creditors.",
        "A narrowly scoped, expressly limited waiver of sovereign immunity (if any) that does not "
        "reach Tribal assets beyond this transaction, and Tribal-forum or mutually neutral dispute "
        "resolution (see Article 22 alternatives).",
        "Priority protection of grant compliance over any commercial term, with the operator bearing "
        "consequences of operator-caused compliance breaches.",
    ]:
        C.bullet(doc, prot)
    C.flag_para(doc, C.FLAG_ATTORNEY,
                f"Sovereign-immunity scope, assignment/change-of-control controls, and lender "
                f"accommodations must be tailored so Tribal protections and operator/lender needs are "
                f"reconciled without waiving more than the {C.TRIBE_SHORT} intends.")

    # ============================================================ ARTICLE 22
    C.article(doc, 22, "Items Requiring Legal or NTIA Approval")
    C.para(doc, "The following items cannot be finalized in this Summary and require legal opinion, "
                "grant-compliance sign-off, and/or NTIA approval or non-objection. None is silently "
                "resolved here.")
    C.section(doc, "22.1", "Threshold and Compliance Approvals")
    for it in [
        f"Lumbee federal-recognition / TBCP eligibility determination ({C.CITES['lumbee_act']}). "
        f"{C.FLAG_GRANT} {C.FLAG_ATTORNEY}",
        f"Contractor-vs-subrecipient determination for {C.OPERATOR_SHORT} "
        f"({C.CITES['subrecipient']}). {C.FLAG_GRANT}",
        f"Program-income treatment of shared revenue ({C.CITES['prog_income']}). {C.FLAG_GRANT}",
        f"Federal-Interest, encumbrance, and disposition consents for any IRU/collateral "
        f"assignment ({C.CITES['real_property']}; {C.CITES['equipment']}). {C.FLAG_GRANT}",
        f"BABA compliance/waivers and §889 covered-equipment certification "
        f"({C.CITES['baba']}; {C.CITES['telecom_ban']}). {C.FLAG_GRANT}",
        f"NEPA/NHPA clearances before construction ({C.CITES['nepa']}; {C.CITES['nhpa']}). "
        f"{C.FLAG_GRANT}",
    ]:
        C.bullet(doc, it)
    C.section(doc, "22.2", "Governing Law, Jurisdiction, and Dispute Resolution — Alternatives")
    C.para(doc, "Governing law, forum, and dispute-resolution mechanism are NOT selected in this "
                "Summary. The following bracketed alternatives are presented for negotiation and "
                "attorney review:")
    C.bullet(doc, f"[ALT-A: Laws of the {C.STATE}, with disputes in {C.STATE} state/federal courts.] "
                  f"{C.FLAG_ATTORNEY}")
    C.bullet(doc, f"[ALT-B: Tribal law of the {C.TRIBE_SHORT} and the jurisdiction of the Tribal "
                  f"court/forum.] {C.FLAG_ATTORNEY}")
    C.bullet(doc, f"[ALT-C: Federal law where applicable, with binding arbitration (e.g., AAA/JAMS) "
                  f"in a neutral seat and limited judicial review.] {C.FLAG_ATTORNEY}")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Governing law, jurisdiction, and dispute resolution interact with sovereign "
                "immunity and enforceability; they must be selected together by counsel, not "
                "individually or by default.")
    C.section(doc, "22.3", "Sovereign Immunity — Alternatives")
    C.para(doc, f"Whether and how the {C.TRIBE_SHORT} waives sovereign immunity is NOT decided here. "
                f"Alternatives:")
    C.bullet(doc, "[ALT-1: No waiver; disputes resolved through non-binding processes and Tribal "
                  f"forum only.] {C.FLAG_ATTORNEY}")
    C.bullet(doc, "[ALT-2: Narrow limited waiver solely for enforcement of this transaction, capped "
                  f"to specified assets/revenues and a specified forum, with exhaustion requirements.] "
                  f"{C.FLAG_ATTORNEY}")
    C.bullet(doc, "[ALT-3: Limited waiver for arbitration and for confirmation/enforcement of an "
                  f"award in a designated court only.] {C.FLAG_ATTORNEY}")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                f"Any waiver must be authorized by the proper Tribal governing body per Tribal law, "
                f"expressly limited, and never broader than necessary. This is a sovereign act of the "
                f"{C.TRIBE_SHORT}, not a drafting default.")

    # ============================================================ ARTICLE 23
    C.article(doc, 23, "Term Sheet")
    C.para(doc, "The following term sheet summarizes the proposed transaction. Bracketed items and "
                "highlighted placeholders are open; alternatives are presented where no default may "
                "be silently selected.")
    C.add_table(
        doc,
        ["Term", "Position / Placeholder"],
        [
            ["Parties",
             f"{C.TRIBE_FULL} (the “{C.TRIBE_SHORT}”), or {C.TRIBE_ENTITY_ALT}; and "
             f"{C.OPERATOR_FULL} (“{C.OPERATOR_SHORT}”)."],
            ["Program / Agency",
             f"{C.PROGRAM_FULL} ({C.PROGRAM_SHORT}), {C.AGENCY_FULL} ({C.AGENCY_SHORT}); {C.NOFO_NAME}."],
            ["Eligibility threshold",
             f"{C.FLAG_GRANT} {C.FLAG_ATTORNEY} Lumbee federal-recognition/TBCP eligibility "
             f"({C.CITES['lumbee_act']}) must be confirmed before application."],
            ["Structure",
             f"Tribally owned, grant-funded {C.TRIBAL_ASSETS} interconnected with the "
             f"{C.OPERATOR_EXISTING}; {C.OPERATOR_SHORT} operates and commercializes under a "
             f"long-term {C.IRU_TERM_DEFINED}. Title never transfers."],
            ["Ownership",
             f"{C.TRIBE_SHORT} holds and retains title to all {C.TRIBAL_ASSETS}; {C.OPERATOR_SHORT} "
             f"owns {C.OPERATOR_ASSETS}. Boundary fixed by the {C.DEMARCATION} schedule."],
            ["IRU term & renewal",
             f"Recommended {C.IRU_TERM_RECOMMENDED}-year initial term (alternatives 20/25/30) plus "
             f"{C.DEAL['iru_renewal']}, subject to Federal-Interest constraints and "
             f"{C.AGENCY_SHORT} consent where required."],
            ["Consideration",
             f"{C.DEAL['iru_prepaid_consideration']}. {C.FLAG_BUSINESS} Up-front payment, if any: "
             f"{C.PH('up-front IRU payment')}."],
            ["Revenue share",
             f"Recommended {C.DEAL['rev_options']['D']}. {C.FLAG_BUSINESS} Base "
             f"{C.PH('base amount')} + {C.PH('share %')} of {C.PH('defined revenue')}; alternatives "
             f"A–E per Article 11."],
            ["Maintenance",
             f"{C.OPERATOR_SHORT} bears routine/preventive/SLA-corrective maintenance; catastrophic "
             f"restoration of Tribal Assets: insurance first then {C.PH('cost-share formula')}."],
            ["Replacement capital",
             f"{C.FLAG_BUSINESS} Recommended: {C.OPERATOR_SHORT}-funded like-for-like replacement of "
             f"Tribal Assets to sustain service; reserve mechanism {C.PH('capex/reserve terms')}."],
            ["Reserved Tribal capacity",
             f"Reserved dark fiber/lit capacity carved out of the IRU: {C.PH('reserved strands/bandwidth')}."],
            ["Service levels",
             f"Availability {C.DEAL['sla']['availability_target']}; severity-based SLA; NOC "
             f"{C.DEAL['sla']['noc']}."],
            ["Term / termination",
             f"For cause with cure: {C.DEAL['cure_monetary_days']}-day monetary / "
             f"{C.DEAL['cure_nonmonetary_days']}-day non-monetary; grant/compliance termination per "
             f"{C.CITES['remedies']}; title returns to Tribe."],
            ["Step-in / transition",
             f"Tribal step-in on defined triggers (emergency step-in {C.DEAL['stepin_emergency']}); "
             f"up to {C.DEAL['transition_assistance_months']} months transition assistance."],
            ["Grant compliance",
             f"{C.FLAG_GRANT} {C.CITES['ug_2024']}, BABA, §889, NEPA/NHPA, program income, "
             f"records/audit flowed down via the Grant-Compliance Rider."],
            ["Insurance",
             f"CGL {C.DEAL['insurance']['cgl_occurrence']}/occurrence "
             f"({C.DEAL['insurance']['cgl_aggregate']} agg.); umbrella "
             f"{C.DEAL['insurance']['umbrella']}; cyber {C.DEAL['insurance']['cyber']}; "
             f"builders risk {C.DEAL['insurance']['property_builders_risk']}; Tribe as additional "
             f"insured. ({C.CITES['insurance']})"],
            ["Governing law",
             f"NOT SELECTED. [ALT-A: {C.STATE} law/courts] / [ALT-B: Tribal law/forum] / "
             f"[ALT-C: arbitration, neutral seat]. {C.FLAG_ATTORNEY}"],
            ["Sovereign immunity",
             f"NOT DECIDED. [ALT-1: no waiver] / [ALT-2: narrow limited waiver, capped assets/forum] "
             f"/ [ALT-3: waiver for arbitration + enforcement]. {C.FLAG_ATTORNEY}"],
            ["Conditions precedent",
             f"Eligibility confirmation; {C.PROGRAM_SHORT} Award; Tribal Council authorization; "
             f"NTIA approvals/non-objection; NEPA/NHPA clearance; financing; final network design; "
             f"definitive documents. {C.FLAG_GRANT} {C.FLAG_ATTORNEY}"],
        ],
        widths=[1.7, 5.3],
        font_size=8,
    )

    # ============================================================ ARTICLE 24
    C.article(doc, 24, "Responsibility Matrix (RACI)")
    C.para(doc, "The following RACI matrix allocates each key activity across the four principal "
                "actors. It is a planning tool; the definitive documents control in the event of any "
                "conflict.")
    C.add_table(
        doc,
        ["Key Activity", C.TRIBE_SHORT, C.OPERATOR_SHORT, "Grant Counsel", C.AGENCY_SHORT],
        [
            ["Grant application", "A", "C", "R", "I"],
            ["Network design", "C", "A/R", "I", "I"],
            ["Environmental / historic review (NEPA/NHPA)", "A", "R", "C", "I"],
            ["Permitting / easements / rights-of-way", "A", "R", "C", "I"],
            ["Procurement (grant-compliant)", "A", "R", "C", "I"],
            ["Construction", "I", "A/R", "I", "I"],
            ["Testing / acceptance", "A", "R", "I", "I"],
            ["Asset ownership records / inventory", "A/R", "C", "C", "I"],
            ["Operations (NOC / network mgmt)", "I", "A/R", "I", "I"],
            ["Billing / collections", "I", "A/R", "I", "I"],
            ["Customer service", "I", "A/R", "I", "I"],
            ["Marketing / sales", "I", "A/R", "I", "I"],
            ["Regulatory compliance (telecom)", "C", "A/R", "C", "I"],
            ["Grant reporting to NTIA", "A", "R", "C", "I"],
            ["Audit (single audit / Award)", "A", "R", "C", "I"],
            ["Maintenance", "I", "A/R", "I", "I"],
            ["Capital replacement", "C", "A/R", "I", "I"],
            ["Cybersecurity", "C", "A/R", "C", "I"],
            ["Step-in / transition", "A/R", "C", "C", "I"],
        ],
        widths=[3.0, 1.0, 1.1, 1.0, 0.9],
        font_size=8,
        col_align=[None, "c", "c", "c", "c"],
    )
    C.section(doc, "24.1", "RACI Legend")
    C.bullet(doc, "R — Responsible: performs the work / executes the activity.")
    C.bullet(doc, "A — Accountable: owns the outcome and answers for it (one accountable party "
                  "per activity; “A/R” where the same actor both owns and performs).")
    C.bullet(doc, "C — Consulted: provides input/expertise before or during the activity.")
    C.bullet(doc, "I — Informed: kept apprised of progress and outcomes.")
    C.flag_para(doc, C.FLAG_GRANT,
                f"{C.AGENCY_SHORT} is shown as Informed for planning purposes; several activities in "
                f"fact require {C.AGENCY_SHORT} approval or non-objection (Article 22). The "
                f"contractor-vs-subrecipient determination may shift certain Operator cells between "
                f"Responsible and Accountable.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "This matrix is indicative; final responsibility allocation is set by the definitive "
                "documents and the compliance determinations noted above.")

    # -- Closing / signature --------------------------------------------------
    C.article(doc, 25, "Status, Reservations, and Execution")
    C.para(doc, "This Summary is a non-binding working draft for discussion. It does not obligate "
                "either Party, is not an offer capable of acceptance, and creates no partnership, "
                "joint venture, agency, or fiduciary relationship. Binding obligations arise only "
                "upon execution of the definitive documents, after satisfaction of the conditions "
                "precedent and the approvals identified in Article 22.", italic=True)
    C.flag_para(doc, C.FLAG_ATTORNEY,
                f"For discussion only; the signature block below is provided to frame execution of a "
                f"future term sheet and does not itself create a binding agreement. All open terms, "
                f"eligibility, and approvals must be resolved first.")
    C.signature_block(
        doc,
        extra_note="Signature authority for the Tribe requires proper Tribal Council authorization; "
                   "signature authority for RIVR Tech requires corporate authorization. Confirm both "
                   "before execution.")

    return C.save(doc, "01_Executive",
                  "Lumbee_RIVR_Executive_Deal_Summary_and_Term_Sheet.docx")


if __name__ == "__main__":
    path = build()
    print("SAVED ->", path)
