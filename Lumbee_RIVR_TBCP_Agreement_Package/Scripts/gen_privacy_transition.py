"""
gen_privacy_transition.py — Generator for two coordinated TBCP Definitive Agreements
in the Lumbee Tribe of North Carolina / RIVR Tech fiber package.

DOC 1: 02_Definitive_Agreements/09_Data_Privacy_Cybersecurity_and_Continuity_Addendum.docx
DOC 2: 02_Definitive_Agreements/10_Continuity_Step_In_and_Transition_Agreement.docx

Uses the canonical engine Scripts/common.py as the SINGLE SOURCE OF TRUTH for party
names, defined terms, deal mechanics, citations, cross-references, and formatting.
Nothing in the deal brief is invented here: every party, amount, cure period,
step-in term, transition period, retention period, citation, schedule, and
agreement name is pulled from common.py.
"""

import sys
sys.path.insert(0, '/home/user/claude-skills/Lumbee_RIVR_TBCP_Agreement_Package/Scripts')
import common as C


# ---------------------------------------------------------------------------
# Shared building blocks reused by both agreements
# ---------------------------------------------------------------------------
def intro(doc, agreement_name):
    """Status banner + standard two-party intro sentence."""
    C.status_banner(doc)
    C.spacer(doc, 1)
    C.para(
        doc,
        f"This {agreement_name} (this “Agreement”) is entered into as of "
        f"{C.PH('Effective Date')} (the “Effective Date”), by and between "
        f"{C.TRIBE_FULL} (the “{C.TRIBE_SHORT}”), and {C.OPERATOR_FULL} "
        f"(“{C.OPERATOR_SHORT}”). The {C.TRIBE_SHORT} and {C.OPERATOR_SHORT} "
        f"are each a “{C.PARTY_SINGULAR}” and together the “{C.PARTIES_COLLECTIVE}.”",
    )
    C.para(
        doc,
        f"This Agreement is one of the Definitive Agreements executed under, and is "
        f"subordinate to, the {C.AGREEMENTS['master']}. It supports the {C.PROGRAM_FULL} "
        f"({C.PROGRAM_SHORT}) award administered by the {C.AGENCY_FULL} ({C.AGENCY_SHORT}), "
        f"{C.DOC_FULL}.",
    )
    C.flag_para(
        doc, C.FLAG_GRANT,
        f"No controlling {C.PROGRAM_SHORT} award or source documents were supplied. "
        f"Provisional baseline: {C.NOFO_NAME}. {C.NOFO_LIVE_NOTE}",
    )


def precedence_article(doc, art_num, this_agreement_key):
    """Order-of-precedence + shared-definitions article (verbatim engine text)."""
    C.article(doc, art_num, "Order of Precedence, Shared Definitions, and Interpretation")

    C.section(doc, f"{art_num}.1", "Order of Precedence",
              "In the event of any conflict, ambiguity, or inconsistency among the "
              "instruments governing this transaction, the following order of precedence "
              "applies, from highest to lowest:")
    for i, item in enumerate(C.PRECEDENCE, start=1):
        C.numbered(doc, item)
    C.para(doc, C.PRECEDENCE_RULE)

    C.section(doc, f"{art_num}.2", "Shared Definitions", C.SHARED_DEFINITIONS_RULE)
    C.para(
        doc,
        f"This Agreement is the {C.AGREEMENTS[this_agreement_key]} referenced in that "
        f"definitions source, and capitalized terms defined in this Agreement have the "
        f"meanings given here for purposes of this Agreement.",
    )

    C.section(doc, f"{art_num}.3", "Interpretation",
              "Headings are for convenience only. References to statutes and regulations "
              "include successor provisions. “Including” means “including "
              "without limitation.” Cross-references to Schedules and other Definitive "
              "Agreements are to the instruments named in the Schedule and Agreement "
              "registers maintained in the Master Agreement.")
    C.flag_para(
        doc, C.FLAG_ATTORNEY,
        "Sovereign immunity and governing-law provisions are stated as bracketed "
        "ALTERNATIVES in the Master Agreement and are incorporated by reference; a clear, "
        "express, and limited waiver of the Lumbee Tribe's sovereign immunity (if any) must "
        "be negotiated and confirmed by counsel and Tribal Council, and nothing in this "
        "Agreement waives sovereign immunity by implication.")


def disclaimer(doc):
    """Standard closing disclaimer required at the end of the body."""
    C.spacer(doc, 1)
    C.article(doc, "—", "Disclaimer")
    C.para(
        doc,
        f"{C.DRAFT_STATUS} This document is a working draft prepared for discussion and "
        f"negotiation only. It is not executed, is not a complete or final agreement, and "
        f"does not constitute legal, financial, tax, regulatory, or grant-compliance advice. "
        f"All bracketed items, placeholders (highlighted), and flagged provisions must be "
        f"completed and confirmed by the Parties and their advisors. All terms remain subject "
        f"to legal, grant, and financial review and to the controlling federal Award once "
        f"supplied.",
        italic=True,
    )
    C.status_banner(doc)


# ===========================================================================
#  DOC 1 — Data Privacy, Cybersecurity, Supply-Chain Risk, and
#          Business Continuity Addendum
# ===========================================================================
def build_privacy():
    title = C.AGREEMENTS["privacy"]
    doc = C.new_doc()
    C.add_cover(doc, "DEFINITIVE AGREEMENT NO. 09", title,
                "Data Privacy, Cybersecurity, Supply-Chain Risk, and Business Continuity")
    C.setup_header_footer(doc, "Privacy / Cyber / Continuity Addendum")
    C.add_toc(doc)

    intro(doc, title)

    # ---- ARTICLE 1 — Purpose, Scope, and Cross-References ----------------
    C.article(doc, 1, "Purpose, Scope, and Cross-References")
    C.section(doc, "1.1", "Purpose",
              f"This Agreement establishes the data-privacy, cybersecurity, supply-chain-risk, "
              f"and business-continuity controls that {C.OPERATOR_SHORT} shall maintain in "
              f"operating, maintaining, and providing retail service over the {C.NETWORK} and "
              f"the {C.GRANT_FUNDED}, and in handling data generated by or relating to the "
              f"{C.PROGRAM_SHORT} project.")
    C.section(doc, "1.2", "Scope",
              f"This Agreement applies to all systems, software, hardware, facilities, "
              f"personnel, and subcontractors used by {C.OPERATOR_SHORT} to deliver services "
              f"under the Definitive Agreements, including the {C.OPERATOR_EXISTING} to the "
              f"extent it stores, processes, transmits, or secures {C.PROGRAM_SHORT} project "
              f"data or interconnects with the {C.GRANT_FUNDED}.")
    C.section(doc, "1.3", "Controlling Schedule and Cross-References",
              f"The detailed technical requirements, control baselines, incident-response "
              f"runbooks, and disaster-recovery parameters for this Agreement are set out in "
              f"Schedule S11 ({C.SCHEDULES['S11']}). Insurance requirements are set out in "
              f"Schedule S12 ({C.SCHEDULES['S12']}). Continuity, step-in, and transition "
              f"obligations are addressed in the {C.AGREEMENTS['transition']} and Schedule S13 "
              f"({C.SCHEDULES['S13']}). In any conflict between this Agreement and Schedule "
              f"S11, this Agreement controls as to legal allocation and Schedule S11 controls "
              f"as to technical detail, subject to Article 16.")
    C.flag_para(doc, C.FLAG_TECH,
                "Confirm that Schedule S11 control baselines are mapped to a recognized "
                "framework (e.g., NIST SP 800-53 / CSF or equivalent) and to any award-specific "
                "cybersecurity conditions once the controlling Award is supplied.")

    # ---- ARTICLE 2 — Definitions -----------------------------------------
    C.article(doc, 2, "Definitions")
    C.para(doc, "For purposes of this Agreement:")
    C.subsection(doc, "a", "“Project Data” means all data created, collected, "
                 "received, stored, processed, or transmitted in connection with the "
                 f"{C.PROGRAM_SHORT} project, including subscriber, network, operational, "
                 "financial, and compliance data.")
    C.subsection(doc, "b", "“Customer Personal Data” means personally identifiable "
                 "information of subscribers and applicants, including account, contact, "
                 "usage, and payment information.")
    C.subsection(doc, "c", f"“CPNI” means Customer Proprietary Network Information "
                 f"as defined under {C.CITES['cpni']}.")
    C.subsection(doc, "d", "“Security Incident” means any actual or reasonably "
                 "suspected unauthorized access to, acquisition of, disclosure of, loss of, "
                 "alteration of, or interference with Project Data or systems; a "
                 "“Material Incident” is a Security Incident meeting the materiality "
                 "criteria in Article 10.")
    C.subsection(doc, "e", f"“Prohibited Equipment” means covered telecommunications "
                 f"and video-surveillance equipment and services described in "
                 f"{C.CITES['telecom_ban']} (Section 889 covered equipment).")

    # ---- ARTICLE 3 — Data Classification ---------------------------------
    C.article(doc, 3, "Data Classification")
    C.section(doc, "3.1", "Classification Program",
              f"{C.OPERATOR_SHORT} shall classify Project Data into the categories below and "
              f"apply the minimum handling controls for each category. Handling controls are "
              f"cumulative with the technical baselines in Schedule S11.")
    C.add_table(
        doc,
        ["Classification", "Examples", "Minimum Handling Controls"],
        [
            ["Restricted", "Customer Personal Data; CPNI; payment/card data; credentials; "
             "encryption keys", "Encryption at rest and in transit; MFA; least-privilege "
             "RBAC; full logging; no export except as permitted under Article 15"],
            ["Confidential", "Network configuration; engineering records; contracts; "
             "financial and program-income data", "Encryption in transit; RBAC; logging; "
             "need-to-know access"],
            ["Internal", "Operational tickets; internal communications", "RBAC; logging"],
            ["Public", "Published service and coverage information", "Integrity controls only"],
        ],
        widths=[1.4, 2.6, 2.6],
    )
    C.flag_para(doc, C.FLAG_GRANT,
                "Data-classification categories must be reconciled with Tribal data-governance "
                "requirements and with any data-handling conditions in the controlling Award.")

    # ---- ARTICLE 4 — Access Control (Least-Privilege / RBAC) -------------
    C.article(doc, 4, "Access Control — Least Privilege and Role-Based Access")
    C.section(doc, "4.1", "Least Privilege",
              f"{C.OPERATOR_SHORT} shall grant access to Project Data and systems on a "
              f"least-privilege, need-to-know basis, limited to what each role requires.")
    C.section(doc, "4.2", "Role-Based Access Control (RBAC)",
              "Access shall be provisioned through documented roles with defined entitlements. "
              "Access rights shall be reviewed at least quarterly and revoked promptly upon "
              "role change or separation (target: within [■ number] business hours).")
    C.section(doc, "4.3", "Privileged Access",
              "Administrative and privileged access shall be individually attributable, "
              "separately logged, time-bounded where feasible, and subject to enhanced "
              "monitoring.")

    # ---- ARTICLE 5 — Multi-Factor Authentication -------------------------
    C.article(doc, 5, "Multi-Factor Authentication")
    C.section(doc, "5.1", "MFA Required",
              f"{C.OPERATOR_SHORT} shall require phishing-resistant multi-factor "
              f"authentication (MFA) for all remote access, all administrative and privileged "
              f"access, and all access to systems storing or processing Restricted or "
              f"Confidential Project Data.")
    C.section(doc, "5.2", "No Shared Credentials",
              "Shared or generic credentials are prohibited for access to Restricted or "
              "Confidential Project Data except where individually attributable and approved "
              "in writing.")

    # ---- ARTICLE 6 — Encryption ------------------------------------------
    C.article(doc, 6, "Encryption")
    C.section(doc, "6.1", "Encryption in Transit",
              "Project Data classified Confidential or Restricted shall be encrypted in "
              "transit using current, industry-accepted protocols (e.g., TLS 1.2+ or "
              "equivalent), with the specific standards set out in Schedule S11.")
    C.section(doc, "6.2", "Encryption at Rest",
              "Project Data classified Confidential or Restricted shall be encrypted at rest "
              "using current, industry-accepted algorithms and key lengths.")
    C.section(doc, "6.3", "Key Management",
              "Encryption keys shall be managed under documented key-management procedures, "
              "stored separately from the data they protect, rotated on a defined schedule, "
              "and access-controlled as Restricted Project Data.")

    # ---- ARTICLE 7 — Logging and Monitoring ------------------------------
    C.article(doc, 7, "Logging and Monitoring")
    C.section(doc, "7.1", "Security Logging",
              "Security-relevant events (authentication, authorization, privileged actions, "
              "configuration changes, and data access) shall be logged, time-synchronized, "
              "protected against tampering, and retained for the period set out in Schedule "
              "S11 and consistent with the records-retention period in Article 12.")
    C.section(doc, "7.2", "Monitoring and Alerting",
              "Logs shall be monitored for anomalous and unauthorized activity, with alerting "
              "to designated security personnel.")

    # ---- ARTICLE 8 — Vulnerability and Patch Management ------------------
    C.article(doc, 8, "Vulnerability and Patch Management")
    C.section(doc, "8.1", "Vulnerability Management",
              "{operator} shall maintain a vulnerability-management program with regular "
              "scanning of systems supporting the project and risk-based remediation."
              .format(operator=C.OPERATOR_SHORT))
    C.section(doc, "8.2", "Patch Timelines",
              "Security patches shall be applied on a risk-based schedule, with critical "
              "vulnerabilities remediated within [■ number] days of a fix becoming available "
              "and other vulnerabilities within timelines defined in Schedule S11.")

    # ---- ARTICLE 9 — Backups and Recovery Testing ------------------------
    C.article(doc, 9, "Backups and Recovery Testing")
    C.section(doc, "9.1", "Backups",
              f"{C.OPERATOR_SHORT} shall maintain regular, encrypted backups of Project Data "
              f"and critical system configurations, stored with geographic separation and "
              f"protected against ransomware (including immutable or offline copies).")
    C.section(doc, "9.2", "Recovery Testing",
              "Backups shall be tested by restoration at least annually (and after material "
              "changes), with results documented and provided to the {tribe} on request."
              .format(tribe=C.TRIBE_SHORT))

    # ---- ARTICLE 10 — Incident Response and Material-Incident Notice -----
    C.article(doc, 10, "Incident Response and Material-Incident Notice")
    C.section(doc, "10.1", "Incident-Response Plan",
              f"{C.OPERATOR_SHORT} shall maintain and follow a written incident-response plan "
              f"(set out in or referenced by Schedule S11) covering detection, triage, "
              f"containment, eradication, recovery, and post-incident review.")
    C.section(doc, "10.2", "Material-Incident Notice",
              f"{C.OPERATOR_SHORT} shall notify the {C.TRIBE_SHORT} of any Material Incident "
              f"without undue delay and in any event within {C.PH('24')} hours after "
              f"discovery, or sooner if required by the controlling Award, applicable law, or "
              f"any breach-notification statute. Notice shall include the information then "
              f"known and shall be supplemented as the investigation proceeds.")
    C.section(doc, "10.3", "Materiality Criteria",
              "An incident is a Material Incident if it involves (a) unauthorized access to or "
              "acquisition of Restricted Project Data (including Customer Personal Data or "
              "CPNI); (b) a reasonable likelihood of harm to subscribers; (c) a material "
              "disruption of service; or (d) any event triggering a legal or Award "
              "notification obligation.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Confirm the 24-hour notice window against the controlling Award's specific "
                "conditions and against all applicable federal and North Carolina "
                "breach-notification laws; the shorter of the applicable periods governs.")

    # ---- ARTICLE 11 — Subcontractor and Supply-Chain Controls ------------
    C.article(doc, 11, "Subcontractor and Supply-Chain Controls")
    C.section(doc, "11.1", "Subcontractor Controls",
              f"{C.OPERATOR_SHORT} shall bind each subcontractor with access to Project Data "
              f"or project systems to written obligations no less protective than this "
              f"Agreement and shall remain responsible for subcontractor performance.")
    C.section(doc, "11.2", "Software and Hardware Inventory",
              f"{C.OPERATOR_SHORT} shall maintain a current inventory of software and hardware "
              f"(including firmware and key third-party components) used in the {C.NETWORK} "
              f"and the {C.GRANT_FUNDED}, sufficient to support supply-chain-risk review.")
    C.section(doc, "11.3", "Supply-Chain Attestations",
              "{operator} shall obtain and retain supply-chain attestations from suppliers "
              "and subcontractors confirming compliance with the prohibited-equipment "
              "requirements of Section 11.4 and with applicable domestic-preference and "
              "Buy-America requirements referenced in the Master Agreement."
              .format(operator=C.OPERATOR_SHORT))
    C.section(doc, "11.4", "Prohibited Equipment (Section 889 Covered Equipment)",
              f"{C.OPERATOR_SHORT} shall not use, procure, obtain, or extend or renew a "
              f"contract to procure or obtain, any Prohibited Equipment in the project, in "
              f"accordance with {C.CITES['telecom_ban']}. If Prohibited Equipment is "
              f"identified, {C.OPERATOR_SHORT} shall promptly notify the {C.TRIBE_SHORT}, "
              f"remove and replace it at {C.OPERATOR_SHORT}'s cost unless otherwise agreed, "
              f"and document remediation.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Prohibited-equipment and supply-chain-attestation obligations must be "
                "reconciled with the Award's Specific Award Conditions and with 2 CFR Part 200 "
                "procurement standards once the controlling Award is supplied.")

    # ---- ARTICLE 12 — Customer Notification, Cooperation, Evidence -------
    C.article(doc, 12, "Customer Notification, Cooperation, and Evidence Preservation")
    C.section(doc, "12.1", "Customer Notification",
              f"Where a Security Incident triggers a customer-notification obligation, the "
              f"Parties shall coordinate on the content and timing of notifications; "
              f"{C.OPERATOR_SHORT}, as retail provider of record, shall issue notifications "
              f"as required by law, subject to the {C.TRIBE_SHORT}'s reasonable review, and "
              f"the Award's requirements.")
    C.section(doc, "12.2", "Cooperation",
              f"{C.OPERATOR_SHORT} shall cooperate with the {C.TRIBE_SHORT}, {C.AGENCY_SHORT}, "
              f"and law-enforcement or regulatory authorities in investigating and responding "
              f"to Security Incidents.")
    C.section(doc, "12.3", "Evidence Preservation",
              "Upon discovery of a Security Incident, {operator} shall preserve relevant logs, "
              "images, and evidence in a forensically sound manner for the period required by "
              "law and in any event for not less than {yrs} years, consistent with the "
              "records-retention requirements of {cite}."
              .format(operator=C.OPERATOR_SHORT, yrs=C.DEAL['records_retention_years'],
                      cite=C.CITES['records']))

    # ---- ARTICLE 13 — Cyber Insurance ------------------------------------
    C.article(doc, 13, "Cyber Insurance")
    C.section(doc, "13.1", "Coverage",
              f"{C.OPERATOR_SHORT} shall maintain cyber-liability insurance with limits of not "
              f"less than {C.DEAL['insurance']['cyber']}, covering breach response, "
              f"notification, forensic, liability, and business-interruption costs, on the "
              f"terms set out in the Insurance Schedule (Schedule S12 — "
              f"{C.SCHEDULES['S12']}).")
    C.section(doc, "13.2", "Cross-Reference",
              "The cyber-insurance requirement in this Article is cumulative with, and "
              "governed by, the insurance, indemnity, and claims provisions of Schedule S12 "
              "and the applicable Definitive Agreements.")

    # ---- ARTICLE 14 — Business Continuity and Disaster Recovery ----------
    C.article(doc, 14, "Business Continuity and Disaster Recovery")
    C.section(doc, "14.1", "Disaster-Recovery Plan",
              f"{C.OPERATOR_SHORT} shall maintain a disaster-recovery and business-continuity "
              f"plan (set out in or referenced by Schedule S11) addressing loss of facilities, "
              f"systems, data, and key personnel.")
    C.section(doc, "14.2", "Recovery Objectives (RTO / RPO)",
              f"The plan shall establish a Recovery Time Objective (RTO) of {C.PH('RTO hours by service tier')} "
              f"and a Recovery Point Objective (RPO) of {C.PH('RPO hours by data type')} for "
              f"critical services and Project Data, with the specific per-tier objectives set "
              f"out in Schedule S11.")
    C.section(doc, "14.3", "Annual Testing",
              "The disaster-recovery and business-continuity plan shall be tested at least "
              "annually, with results documented and material deficiencies remediated on a "
              "defined schedule.")
    C.section(doc, "14.4", "Secure Data and Configuration Export at Transition",
              f"On expiration or termination of the operating arrangement, or upon a step-in "
              f"or transition event, {C.OPERATOR_SHORT} shall provide a secure, complete, and "
              f"usable export of Project Data and system configurations in accordance with the "
              f"{C.AGREEMENTS['transition']}, subject to the data-rights allocation in Article "
              f"15 and to legal-permissibility limits on Customer Personal Data.")

    # ---- ARTICLE 15 — Data-Rights Allocation by Category -----------------
    C.article(doc, 15, "Data-Rights Allocation by Category")
    C.section(doc, "15.1", "Allocation Principle",
              f"Rights and roles in Project Data are allocated by data category. Neither Party "
              f"acquires rights in the other's data beyond those necessary to perform the "
              f"Definitive Agreements and to comply with law and the Award. For the avoidance "
              f"of doubt, {C.OPERATOR_SHORT} does not own Customer Personal Data; "
              f"{C.OPERATOR_SHORT} processes it as retail provider of record subject to law, "
              f"this Agreement, and the Award.")
    C.add_table(
        doc,
        ["Data Category", "Controller / Owner", "Processor / Service Provider", "Governing Constraints"],
        [
            ["Customer Personal Data",
             f"Subscriber retains rights in own PII; {C.OPERATOR_SHORT} is retail provider of "
             f"record / controller for retail relationship (never unqualified “owner”)",
             f"{C.OPERATOR_SHORT} processes; subcontractors as sub-processors",
             "Applicable privacy law; customer-notification duties; Article 15.4"],
            ["CPNI",
             "Subscriber-protected; carrier duties apply",
             f"{C.OPERATOR_SHORT} as carrier subject to CPNI rules",
             C.CITES['cpni']],
            ["Network / Configuration Data for Grant-Funded Assets",
             f"{C.TRIBE_SHORT} (owner of the {C.GRANT_FUNDED})",
             f"{C.OPERATOR_SHORT} as operator",
             f"Federal Interest; must be exportable at transition"],
            ["RIVR Tech Existing Network data",
             f"{C.OPERATOR_SHORT} (owner of the {C.OPERATOR_EXISTING})",
             "n/a",
             "Remains RIVR Tech's; not a Grant-Funded Asset"],
            ["Program / Compliance / Financial project data",
             f"{C.TRIBE_SHORT} as award recipient / steward",
             f"{C.OPERATOR_SHORT} generates and reports",
             "2 CFR Part 200; records retention; audit access"],
        ],
        widths=[1.7, 1.9, 1.6, 1.6],
    )
    C.section(doc, "15.2", "Tribal Data Sovereignty",
              f"The {C.TRIBE_SHORT} retains sovereign authority over Tribal data and over data "
              f"concerning the {C.PROGRAM_SHORT} project consistent with Tribal law and "
              f"data-governance policy. Nothing in this Agreement transfers ownership of Tribal "
              f"data or Grant-Funded Assets data to {C.OPERATOR_SHORT}, and any secondary or "
              f"non-project use of such data requires the {C.TRIBE_SHORT}'s prior written "
              f"consent and must be Award-permitted.")
    C.section(doc, "15.3", "No Unqualified Ownership of Customer Personal Data",
              f"{C.OPERATOR_SHORT} shall not assert, and this Agreement does not grant, "
              f"unqualified ownership of Customer Personal Data. {C.OPERATOR_SHORT}'s rights "
              f"are limited to those necessary to provide, bill, and support retail service and "
              f"to comply with law and the Award.")
    C.section(doc, "15.4", "Cross-Reference",
              f"The detailed data-rights, privacy, and CPNI provisions are further specified in "
              f"Schedule S11 ({C.SCHEDULES['S11']}); this Article controls as to legal "
              f"allocation of ownership and roles.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "The controller/processor characterization and CPNI handling must be confirmed "
                "against 47 U.S.C. § 222, FCC CPNI rules, and applicable privacy statutes; "
                "the retail-relationship characterization affects notification and consent duties.")

    # ---- ARTICLE 16 — Precedence + shared definitions --------------------
    precedence_article(doc, 16, "privacy")

    disclaimer(doc)
    C.signature_block(
        doc,
        extra_note="Execution is subject to Tribal Council authorization, RIVR Tech corporate "
                   "authorization, confirmation of the controlling Award, and completion of all "
                   "bracketed and flagged items.")

    return C.save(doc, "02_Definitive_Agreements",
                  "09_Data_Privacy_Cybersecurity_and_Continuity_Addendum.docx")


# ===========================================================================
#  DOC 2 — Continuity, Step-In, Termination Assistance, and Transition
#          Agreement
# ===========================================================================
def build_transition():
    title = C.AGREEMENTS["transition"]
    doc = C.new_doc()
    C.add_cover(doc, "DEFINITIVE AGREEMENT NO. 10", title,
                "Continuity, Step-In, Termination Assistance, and Transition")
    C.setup_header_footer(doc, "Continuity / Step-In / Transition Agreement")
    C.add_toc(doc)

    intro(doc, title)

    # ---- ARTICLE 1 — Purpose, Scope, and Cross-References ----------------
    C.article(doc, 1, "Purpose, Scope, and Cross-References")
    C.section(doc, "1.1", "Purpose",
              f"This Agreement provides for continuity of Essential Services, for the "
              f"{C.TRIBE_SHORT}'s (or its designee's) step-in and substitution rights, and for "
              f"orderly termination assistance and transition, so that retail broadband service "
              f"over the {C.NETWORK} and the {C.GRANT_FUNDED} continues and the {C.PROGRAM_SHORT} "
              f"Award is protected if {C.OPERATOR_SHORT} cannot or does not perform.")
    C.section(doc, "1.2", "Controlling Schedule and Cross-References",
              f"The detailed default, cure, step-in, continuity, transition, and "
              f"termination-assistance mechanics for this Agreement are set out in Schedule S13 "
              f"({C.SCHEDULES['S13']}). This Agreement is coordinated with the {C.AGREEMENTS['master']}, "
              f"the {C.AGREEMENTS['om']}, the {C.AGREEMENTS['retail']}, the {C.AGREEMENTS['iru']}, "
              f"and the {C.AGREEMENTS['privacy']}.")

    # ---- ARTICLE 2 — Definitions -----------------------------------------
    C.article(doc, 2, "Definitions")
    C.para(doc, "For purposes of this Agreement:")
    C.subsection(doc, "a", "“Step-In” means the {tribe}'s (or its designee's or a "
                 "Substitute Operator's) temporary or permanent assumption of some or all "
                 "operating functions, proportional to the triggering condition."
                 .format(tribe=C.TRIBE_SHORT))
    C.subsection(doc, "b", "“Substitute Operator” means a qualified operator engaged "
                 "to continue service, meeting the standards in Article 5.")
    C.subsection(doc, "c", "“Essential Services” means the retail broadband and "
                 "supporting services necessary to maintain subscriber connectivity, public "
                 "safety, and Award compliance.")
    C.subsection(doc, "d", f"“Transition Period” means the period of "
                 f"{C.DEAL['transition_assistance_months']} months of transition assistance "
                 f"described in Article 11, extendable as provided therein.")

    # ---- ARTICLE 3 — Default and Cure ------------------------------------
    C.article(doc, 3, "Default and Cure")
    C.section(doc, "3.1", "Monetary Default",
              f"A monetary default occurs if a Party fails to pay an undisputed amount when "
              f"due and does not cure within {C.DEAL['cure_monetary_days']} days after written "
              f"notice.")
    C.section(doc, "3.2", "Non-Monetary Default",
              f"A non-monetary default occurs if a Party fails to perform a material "
              f"obligation and does not cure within {C.DEAL['cure_nonmonetary_days']} days "
              f"after written notice, with {C.DEAL['cure_nonmonetary_extension']}.")
    C.section(doc, "3.3", "Notice",
              f"Default notices shall be given in accordance with the notice provisions of the "
              f"Master Agreement, with not less than {C.DEAL['notice_default_days']} days' "
              f"notice where a notice-and-cure period applies.")

    # ---- ARTICLE 4 — Step-In Triggers and Limits -------------------------
    C.article(doc, 4, "Step-In Triggers and Limits")
    C.section(doc, "4.1", "Triggers",
              f"Subject to the limits in Section 4.2, the {C.TRIBE_SHORT} (or its designee) may "
              f"exercise Step-In upon any of the following:")
    for t in [
        "an uncured default under Article 3 (following expiration of the applicable cure period);",
        "insolvency, bankruptcy, receivership, or assignment for the benefit of creditors of "
        f"{C.OPERATOR_SHORT};",
        "abandonment of the operation or discontinuance of Essential Services;",
        "loss, suspension, or revocation of a license, authorization, or certification "
        "necessary to operate;",
        "chronic or repeated SLA failure as defined in the {om} and Schedule S13;".format(
            om=C.AGREEMENTS['om']),
        "a grant-compliance failure that threatens the Award, the Federal Interest, or the "
        "Tribe's standing as recipient;",
    ]:
        C.bullet(doc, t)
    C.section(doc, "4.2", "Limits — Proportionality",
              f"Step-In shall be proportional to the triggering condition and no broader or "
              f"longer than reasonably necessary to restore continuity, protect public safety, "
              f"and protect the Award. Emergency Step-In is {C.DEAL['stepin_emergency']}; "
              f"non-emergency Step-In follows notice and any applicable cure period. Step-In is "
              f"limited to the {C.GRANT_FUNDED} and the rights necessary for continuity and does "
              f"not extend to the {C.OPERATOR_EXISTING} except as provided in Article 12.")

    C.section(doc, "4.3", "Step-In Trigger → Action Table", None)
    C.add_table(
        doc,
        ["Trigger", "Proportional Action", "Emergency?", "Notice / Cure"],
        [
            ["Uncured monetary default",
             "Assume billing/collections or withhold; escalate to Substitute Operator if "
             "unresolved",
             "No",
             f"{C.DEAL['cure_monetary_days']}-day cure after notice"],
            ["Uncured non-monetary default",
             "Assume affected function(s); direct cure at operator cost",
             "No",
             f"{C.DEAL['cure_nonmonetary_days']}-day cure (+ extension) after notice"],
            ["Insolvency / bankruptcy",
             "Immediate protective Step-In of Grant-Funded Assets operations",
             "Yes",
             "Immediate upon notice"],
            ["Abandonment / service discontinuance",
             "Immediate continuity Step-In; engage Substitute Operator",
             "Yes",
             "Immediate upon notice"],
            ["Loss of authorizations",
             "Step-In and/or Substitute Operator to preserve lawful operation",
             "Yes, if service at risk",
             "Immediate or per cure period as applicable"],
            ["Chronic SLA failure",
             "Assume affected operations; performance improvement or substitution",
             "No",
             "Per Schedule S13 thresholds and cure"],
            ["Grant-compliance failure threatening Award",
             "Protective Step-In limited to restoring compliance and Award standing",
             "Yes, if Award imminently threatened",
             "Immediate or per cure period as applicable"],
        ],
        widths=[1.9, 2.4, 1.1, 1.6],
        col_align=[None, None, "c", None],
    )
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Step-In triggers, thresholds, and any lender/IRU-holder cure and notice rights "
                "must be reconciled with financing documents and with the controlling Award; "
                "emergency Step-In must not exceed what is lawful and proportional.")

    # ---- ARTICLE 5 — Continued Service and Substitute-Operator Standards -
    C.article(doc, 5, "Continued Service and Substitute-Operator Standards")
    C.section(doc, "5.1", "Continued Service",
              "During any Step-In or transition, Essential Services shall continue without "
              "avoidable interruption to subscribers.")
    C.section(doc, "5.2", "Substitute-Operator Standards",
              f"Any Substitute Operator shall meet the operational, technical, financial, "
              f"insurance, and compliance standards required of {C.OPERATOR_SHORT} under the "
              f"Definitive Agreements and shall be acceptable under the Award. Selection of a "
              f"Substitute Operator shall comply with applicable procurement standards "
              f"({C.CITES['procurement']}).")

    # ---- ARTICLE 6 — Access to Facilities and Systems; Emergency Licenses
    C.article(doc, 6, "Access to Facilities and Systems; Emergency Licenses")
    C.section(doc, "6.1", "Access",
              f"Upon a Step-In or transition event, {C.OPERATOR_SHORT} shall provide the "
              f"{C.TRIBE_SHORT}, its designee, or the Substitute Operator with access to the "
              f"{C.GRANT_FUNDED}, associated facilities, systems, and records necessary for "
              f"continuity, subject to security and confidentiality obligations.")
    C.section(doc, "6.2", "Emergency Licenses",
              f"{C.OPERATOR_SHORT} hereby grants, effective upon an emergency Step-In event and "
              f"for the duration reasonably necessary for continuity, a non-exclusive, "
              f"royalty-bearing (cost-based per Article 10) license to use software, "
              f"configurations, and documentation solely as required to operate the "
              f"{C.GRANT_FUNDED} and provide Essential Services, subject to third-party license "
              f"terms and Article 9.")

    # ---- ARTICLE 7 — Customer Communications; Number Portability ---------
    C.article(doc, 7, "Customer Communications and Number Portability")
    C.section(doc, "7.1", "Customer Communications",
              "The Parties shall coordinate subscriber communications during Step-In or "
              "transition to minimize confusion and service disruption, consistent with the "
              f"{C.AGREEMENTS['retail']}.")
    C.section(doc, "7.2", "Number Portability",
              "Where telephone numbers are provided, the Parties shall support number "
              "portability and porting of subscriber numbers to the extent applicable and "
              "legally permitted, subject to Article 14.")

    # ---- ARTICLE 8 — Data, Billing, Configuration, and Asset Records -----
    C.article(doc, 8, "Data, Billing, Configuration, and Asset Records")
    C.section(doc, "8.1", "Data and Billing Exports",
              f"{C.OPERATOR_SHORT} shall provide secure, complete, and usable exports of "
              f"Project Data, billing data, and subscriber records necessary for continuity, "
              f"in accordance with the {C.AGREEMENTS['privacy']} and subject to legal "
              f"permissibility for Customer Personal Data (Article 14).")
    C.section(doc, "8.2", "Configuration and Asset Records",
              f"{C.OPERATOR_SHORT} shall provide current configuration records, network "
              f"documentation, and asset records for the {C.GRANT_FUNDED} sufficient to operate "
              f"and maintain them.")

    # ---- ARTICLE 9 — Spares, Trouble Tickets, AR, Deposits, IP, Training -
    C.article(doc, 9, "Spares, Open Items, Receivables, IP Licenses, and Training")
    C.section(doc, "9.1", "Spares",
              f"Spares and consumables allocable to the {C.GRANT_FUNDED} shall be inventoried "
              f"and made available for continuity, with cost reconciliation under Article 15.")
    C.section(doc, "9.2", "Open Trouble Tickets",
              "Open trouble tickets and maintenance items shall be documented and handed over "
              "with status, so continuity is not disrupted.")
    C.section(doc, "9.3", "Accounts Receivable and Deposits",
              "Accounts receivable, customer deposits, and prepayments shall be identified, "
              "reconciled, and allocated in the final reconciliation under Article 15, "
              "consistent with the {retail} and program-income accounting."
              .format(retail=C.AGREEMENTS['retail']))
    C.section(doc, "9.4", "IP Licenses",
              f"To the extent necessary for continuity, {C.OPERATOR_SHORT} shall license or "
              f"assist in obtaining licenses to intellectual property used to operate the "
              f"{C.GRANT_FUNDED}, subject to third-party terms; {C.OPERATOR_SHORT}'s "
              f"proprietary and pre-existing IP remains {C.OPERATOR_SHORT}'s.")
    C.section(doc, "9.5", "Training",
              "{operator} shall provide reasonable training and knowledge transfer to the "
              "{tribe}, its designee, or the Substitute Operator during the Transition Period."
              .format(operator=C.OPERATOR_SHORT, tribe=C.TRIBE_SHORT))

    # ---- ARTICLE 10 — Transition Pricing ---------------------------------
    C.article(doc, 10, "Transition Pricing")
    C.section(doc, "10.1", "Cost-Based and Capped",
              f"Transition assistance and emergency-license fees shall be cost-based (documented, "
              f"reasonable, allocable costs without profit mark-up) and capped at "
              f"{C.PH('transition-pricing cap amount or methodology')}. Charges shall be "
              f"itemized and subject to the {C.TRIBE_SHORT}'s reasonable review and audit.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                "The transition-pricing cap amount or methodology is a business decision; set a "
                "not-to-exceed figure or a rate schedule so continuity is not held up by pricing "
                "disputes.")

    # ---- ARTICLE 11 — Transition Period ----------------------------------
    C.article(doc, 11, "Transition Period")
    C.section(doc, "11.1", "Duration",
              f"The Transition Period is {C.DEAL['transition_assistance_months']} months, "
              f"extendable by written agreement (or as reasonably necessary and Award-permitted "
              f"to complete an orderly transition and protect continuity).")
    C.section(doc, "11.2", "Transition Checklist", None)
    C.add_table(
        doc,
        ["#", "Transition Item", "Responsible", "Legal-Permissibility Gate"],
        [
            ["1", "Continuity of Essential Services confirmed",
             f"{C.OPERATOR_SHORT} → Substitute Operator", "—"],
            ["2", "Data and billing exports delivered (Article 8.1)",
             C.OPERATOR_SHORT, "Customer Personal Data only if legally permitted (Art. 14)"],
            ["3", "Configuration and asset records delivered (Article 8.2)",
             C.OPERATOR_SHORT, "—"],
            ["4", "Customer contracts transfer",
             "Parties", "Only when legally permitted (Art. 14)"],
            ["5", "Telephone numbers ported",
             "Parties", "Only when applicable and legally permitted (Art. 14)"],
            ["6", "Licenses / authorizations transferred or reissued",
             "Parties", "Only when legally permitted; regulator consent (Art. 14)"],
            ["7", "Customer personal information transfer",
             C.OPERATOR_SHORT, "Only when legally permitted (Art. 14)"],
            ["8", "Spares, open tickets, AR, deposits reconciled (Article 9)",
             "Parties", "—"],
            ["9", "IP licenses / emergency licenses confirmed (Arts. 6, 9)",
             C.OPERATOR_SHORT, "Subject to third-party terms"],
            ["10", "Training / knowledge transfer completed (Article 9.5)",
             C.OPERATOR_SHORT, "—"],
            ["11", "Final reconciliation and true-up (Article 15)",
             "Parties", "Program-income accounting (200.307)"],
            ["12", "Asset return; confidentiality wind-down (Article 16)",
             C.OPERATOR_SHORT, "—"],
        ],
        widths=[0.4, 2.6, 1.7, 2.3],
        col_align=["c", None, None, None],
    )

    # ---- ARTICLE 12 — Protection of RIVR Tech-Owned Infrastructure -------
    C.article(doc, 12, "Protection of RIVR Tech-Owned Infrastructure")
    C.section(doc, "12.1", "Retained Ownership",
              f"{C.OPERATOR_SHORT} retains ownership of the {C.OPERATOR_EXISTING} and its "
              f"pre-existing systems. Step-In and transition rights are limited to the "
              f"{C.GRANT_FUNDED} and to the rights reasonably necessary for continuity, and do "
              f"not transfer ownership of, or a permanent right in, the {C.OPERATOR_EXISTING}.")
    C.section(doc, "12.2", "Continuity Rights Over Existing Network",
              f"Where continuity of Essential Services depends on interconnection with, or "
              f"transport over, the {C.OPERATOR_EXISTING}, {C.OPERATOR_SHORT} shall provide "
              f"continued access on the terms of the {C.AGREEMENTS['interconnect']} and any "
              f"applicable IRU, at cost-based rates, for the duration necessary for continuity.")
    C.section(doc, "12.3", "IRU Cure and Lender Rights",
              f"Where an indefeasible right of use (IRU) over {C.OPERATOR_SHORT} or "
              f"{C.LREMC_SHORT} facilities is implicated, the holder and its lenders shall have "
              f"reasonable cure and notice rights, and any lender rights shall be honored to the "
              f"extent lawful and consistent with the Award and {C.CITES['real_property']}.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                f"Confirm that continuity access to the {C.OPERATOR_EXISTING} and any "
                f"{C.LREMC_SHORT}-owned facilities is supported by the interconnection/IRU "
                f"instruments and owner consents; {C.LREMC_SHORT} facilities require a separate "
                f"owner-approved agreement or joinder.")

    # ---- ARTICLE 13 — Protection of Tribal / Grant-Funded Assets ---------
    C.article(doc, 13, "Protection of Tribal and Grant-Funded Assets")
    C.section(doc, "13.1", "Tribal Ownership",
              f"The {C.GRANT_FUNDED} remain the property of the {C.TRIBE_SHORT}. No Step-In, "
              f"transition, or substitution transfers ownership of the {C.GRANT_FUNDED} to "
              f"{C.OPERATOR_SHORT} or any Substitute Operator.")
    C.section(doc, "13.2", "No Contrary Encumbrance",
              f"No successor, Substitute Operator, or other person may encumber, pledge, or "
              f"dispose of the {C.GRANT_FUNDED} contrary to {C.CITES['real_property']} or the "
              f"Federal Interest, and any purported encumbrance in violation of this Section is "
              f"void.")
    C.section(doc, "13.3", "No Attachment Against Protected Assets",
              f"There shall be no attachment, lien, levy, or execution against trust, "
              f"restricted, or Federal-Interest assets, and continuity rights shall not be "
              f"construed to permit any such attachment. Real-property use, encumbrance, and "
              f"disposition are governed by {C.CITES['real_property']}.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Encumbrance and disposition limits must be confirmed against the controlling "
                "Award, the Federal Interest period, and 2 CFR 200.311; where trust/restricted "
                "land is involved, 25 CFR Parts 162/169 and BIA approval may apply.")

    # ---- ARTICLE 14 — Legally-Permitted Transfers -----------------------
    C.article(doc, 14, "Transfer of Customer Contracts, Numbers, Licenses, and Personal Information")
    C.section(doc, "14.1", "Permissibility Gate",
              f"Customer contracts, telephone numbers, licenses and authorizations, and "
              f"customer personal information shall be transferred ONLY when, and to the extent, "
              f"legally permitted, and subject to any required subscriber, regulatory, or "
              f"third-party consent. Where a transfer is not legally permitted, the Parties "
              f"shall implement the least-disruptive lawful alternative to preserve continuity.")
    C.section(doc, "14.2", "Privacy Compliance",
              f"Transfers of customer personal information shall comply with the "
              f"{C.AGREEMENTS['privacy']}, applicable privacy law, and CPNI requirements "
              f"({C.CITES['cpni']}).")

    # ---- ARTICLE 15 — Final Reconciliation -------------------------------
    C.article(doc, 15, "Final Reconciliation")
    C.section(doc, "15.1", "True-Up and Reserves",
              "Upon transition, the Parties shall perform a final reconciliation and true-up of "
              "amounts owed, including per-Active-Subscriber payments "
              f"({C.DEAL['per_subscriber_amount']}), receivables, deposits, prepayments, "
              "spares, and reserves.")
    C.section(doc, "15.2", "Program-Income Accounting",
              f"Any program income shall be accounted for and treated in accordance with "
              f"{C.CITES['prog_income']}; characterization is subject to the controlling Award "
              f"and any written {C.AGENCY_SHORT} determination, not the label used by the "
              f"Parties.")
    C.section(doc, "15.3", "Records and Audit",
              f"The Parties shall retain reconciliation records for not less than "
              f"{C.DEAL['records_retention_years']} years consistent with {C.CITES['records']}, "
              f"subject to audit access.")

    # ---- ARTICLE 16 — Confidentiality, Security, Asset Return, Survival --
    C.article(doc, 16, "Confidentiality, Security, Asset Return, and Survival")
    C.section(doc, "16.1", "Confidentiality and Security",
              f"During and after any Step-In or transition, the Parties shall maintain "
              f"confidentiality and the security controls of the {C.AGREEMENTS['privacy']} and "
              f"Schedule S11.")
    C.section(doc, "16.2", "Asset Return",
              f"Upon completion of transition, each Party shall return or securely dispose of "
              f"the other Party's confidential information and shall return the {C.GRANT_FUNDED} "
              f"and related records to the {C.TRIBE_SHORT} or its designee.")
    C.section(doc, "16.3", "Survival",
              "Provisions concerning ownership, confidentiality, data protection, "
              "indemnification, records retention, program income, asset protection, and "
              "dispute resolution survive termination or expiration.")

    # ---- ARTICLE 17 — Precedence + shared definitions --------------------
    precedence_article(doc, 17, "transition")

    disclaimer(doc)
    C.signature_block(
        doc,
        extra_note="Execution is subject to Tribal Council authorization, RIVR Tech corporate "
                   "authorization, any required lender / IRU-holder and LREMC owner consents, "
                   "confirmation of the controlling Award, and completion of all bracketed and "
                   "flagged items.")

    return C.save(doc, "02_Definitive_Agreements",
                  "10_Continuity_Step_In_and_Transition_Agreement.docx")


if __name__ == "__main__":
    p1 = build_privacy()
    p2 = build_transition()
    print("DOC 1 ->", p1)
    print("DOC 2 ->", p2)
