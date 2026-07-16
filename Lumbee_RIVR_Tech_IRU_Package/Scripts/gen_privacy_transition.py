#!/usr/bin/env python3
"""
gen_privacy_transition.py
=========================
Generates two Core Agreement deliverables for the Lumbee Tribe of North Carolina
/ RIVR Tech broadband IRU transaction package:

  DOC 6  -> 02_Core_Agreements/06_Data_Privacy_and_Cybersecurity_Addendum.docx
  DOC 7  -> 02_Core_Agreements/07_Transition_Step_In_and_Successor_Operator_Plan.docx

All formatting, defined terms, deal mechanics, and citations flow from the
canonical common.py module (SINGLE SOURCE OF TRUTH). Default / cure / step-in
language is kept numerically consistent with C.DEAL so it matches the Master
Agreement (02.01) and O&M/SLA (02.03).

These are working drafts, not final legal advice. Unresolved terms are marked
with C.PH() placeholders and the four flag markers.
"""

import sys
import os

sys.path.insert(0, "/home/user/claude-skills/Lumbee_RIVR_Tech_IRU_Package/Scripts")
import common as C


# ---------------------------------------------------------------------------
#  Small local helpers (thin wrappers on the canonical engine)
# ---------------------------------------------------------------------------
def sub(doc, label, body):
    return C.subsection(doc, label, body)


def yrs(n):
    words = {20: "twenty (20)", 25: "twenty-five (25)", 30: "thirty (30)"}
    return words.get(n, f"{n}")


# Convenient shorthands drawn from the canonical module
TRIBE = C.TRIBE_SHORT
OP = C.OPERATOR_SHORT
CURE_M = C.DEAL["cure_monetary_days"]           # 30
CURE_NM = C.DEAL["cure_nonmonetary_days"]        # 60
CURE_EXT = C.DEAL["cure_nonmonetary_extension"]
STEPIN = C.DEAL["stepin_emergency"]
TA_MONTHS = C.DEAL["transition_assistance_months"]   # 12
RET_YRS = C.DEAL["records_retention_years"]           # 3


# ===========================================================================
#  DOCUMENT 6 — DATA PRIVACY & CYBERSECURITY ADDENDUM
# ===========================================================================
def build_privacy_addendum():
    doc = C.new_doc()

    C.add_cover(
        doc,
        "Document 6 (Schedule 02.06 to the Master Agreement)",
        "Data Privacy & Cybersecurity Addendum",
        "Customer Data, CPNI, Cybersecurity Standards, Incident Response "
        "and Tribal Data Sovereignty",
    )
    C.setup_header_footer(doc, "Data Privacy & Cybersecurity Addendum")
    C.add_toc(doc)

    C.status_banner(doc)
    C.spacer(doc, 1)

    # ---- Preamble ---------------------------------------------------------
    C.para(
        doc,
        f"This Data Privacy & Cybersecurity Addendum (this “Addendum”) is entered "
        f"into as of {C.PH('Effective Date — conform to Master Agreement Effective Date')} "
        f"(the “Effective Date”), by and between {C.TRIBE_FULL} (the “{TRIBE}”), or "
        f"{C.TRIBE_ENTITY_ALT}, and {C.OPERATOR_FULL} (“{OP}”). The {TRIBE} and {OP} "
        f"are each a “{C.PARTY_SINGULAR}” and together the “{C.PARTIES_COLLECTIVE}.” "
        f"This Addendum is Schedule 02.06 to, and is incorporated by reference into, "
        f"the Master IRU and Network Operations Agreement between the Parties "
        f"(the “Master Agreement,” Document 02.01) and supplements the Operations, "
        f"Maintenance and Service Level Agreement (the “O&M/SLA,” Document 02.03).",
    )
    C.flag_para(
        doc,
        C.FLAG_GRANT,
        f"The {TRIBE}’s status as an eligible entity under the {C.PROGRAM_FULL} "
        f"({C.PROGRAM_SHORT}) depends on federal-recognition status. See {C.CITES['lumbee_act']}. "
        f"Confirm eligibility and the flow-down of data, privacy, and security "
        f"conditions from the {C.CITES['sac']} before execution.",
    )
    C.flag_para(
        doc,
        C.FLAG_ATTORNEY,
        "This Addendum allocates rights in customer and network data, defines "
        "security obligations, and recognizes Tribal data sovereignty. It must be "
        "reviewed by counsel for the Tribe and by communications/privacy counsel "
        "(CPNI, FCC breach rules, and state breach-notification law) before execution.",
    )

    # ================= ARTICLE 1 — PURPOSE & SCOPE =========================
    C.article(doc, 1, "Purpose, Scope and Integration")

    C.section(doc, "1.1", "Purpose",
              f"The purpose of this Addendum is to allocate ownership of, and rights "
              f"to use, Customer Data and Network Data relating to the hybrid {C.NETWORK}; "
              f"to establish the privacy, cybersecurity, and incident-response obligations "
              f"of {OP} as operator; to recognize and protect the {TRIBE}’s sovereign "
              f"interest in data of its members and of subscribers within the {C.SERVICE_TERRITORY}; "
              f"and to ensure that Customer Data and records remain available to the {TRIBE} "
              f"or a successor operator on expiration, termination, or transition.")

    C.section(doc, "1.2", "Scope",
              f"This Addendum applies to all Customer Data, CPNI, Personal Information, "
              f"and Network Data that {OP}, its Affiliates, or its subcontractors Process "
              f"in connection with the deployment, operation, maintenance, marketing, "
              f"billing, or support of services over the {C.NETWORK}, including over the "
              f"{C.TRIBAL_ASSETS} and, to the extent used to serve subscribers in the "
              f"{C.SERVICE_TERRITORY}, the {C.OPERATOR_EXISTING}.")

    C.section(doc, "1.3", "Relationship to the Master Agreement and O&M/SLA",
              f"This Addendum supplements and does not limit the Master Agreement or the "
              f"O&M/SLA. Cure periods, default mechanics, and step-in rights referenced "
              f"herein are the same as those in the Master Agreement (Section 02.01) and "
              f"the O&M/SLA (Section 02.03): a {CURE_M}-day cure period for monetary "
              f"defaults and a {CURE_NM}-day cure period for non-monetary defaults, "
              f"with {CURE_EXT}. In the event of a conflict, the order of precedence in "
              f"Section 20.3 governs.")

    C.section(doc, "1.4", "No Diminution of Federal or Tribal Rights",
              f"Nothing in this Addendum waives, subordinates, or diminishes any right of "
              f"the {TRIBE} or of the United States in the {C.TRIBAL_ASSETS} or in any "
              f"records, data, or intangible property in which a {C.FEDERAL_INTEREST} "
              f"exists. Intangible property acquired or improved with {C.PROGRAM_SHORT} "
              f"funds is subject to {C.CITES['intangible']}.")

    # ================= ARTICLE 2 — DEFINITIONS =============================
    C.article(doc, 2, "Definitions")
    C.para(doc, "Capitalized terms used but not defined in this Addendum have the "
                "meanings given in the Master Agreement. As used in this Addendum:")

    defs = [
        ("“Customer Data”", "all information relating to an identified or identifiable "
         "subscriber, applicant, or end user of services provided over the Network, "
         "including account, contact, service-address, usage, billing, payment, "
         "credit, support, and equipment information, and any Personal Information "
         "and CPNI contained therein."),
        ("“CPNI”", "Customer Proprietary Network Information as defined in "
         f"{C.CITES['cpni']}, including information that relates to the quantity, "
         "technical configuration, type, destination, location, and amount of use "
         "of a telecommunications or interconnected VoIP service, and information "
         "contained on the subscriber’s bill."),
        ("“Personal Information”", "any information that identifies, relates to, or "
         "could reasonably be linked with a particular individual or household, as "
         "defined under applicable federal law, the law of "
         f"{C.STATE}, and applicable Tribal law, including Sensitive Personal "
         "Information (e.g., government identifiers, financial-account and payment-"
         "card data, precise geolocation, and credentials)."),
        ("“Network Data”", "operational, configuration, performance, telemetry, "
         "fault, and log data generated by or about the Network, exclusive of the "
         "personal content of subscriber communications."),
        ("“Tribal Data”", "Customer Data and Personal Information of enrolled members "
         f"of the {C.TRIBE_FULL} and of subscribers whose service address is within "
         f"the {C.SERVICE_TERRITORY}, together with any data in which the {TRIBE} "
         "asserts a sovereign or proprietary interest under Article 16."),
        ("“Process” / “Processing”", "any operation performed on data, including "
         "collection, access, use, storage, transmission, disclosure, analysis, "
         "combination, retention, and destruction."),
        ("“Security Incident”", "any actual or reasonably suspected unauthorized "
         "access to, acquisition of, use of, disclosure of, loss of, or interference "
         "with the confidentiality, integrity, or availability of Customer Data, "
         "CPNI, Personal Information, or the systems that Process them."),
        ("“Breach”", "a Security Incident that triggers a notification obligation "
         "under the CPNI rules, the FCC’s customer-data breach rules, or an applicable "
         "state or Tribal breach-notification law."),
        ("“Subprocessor”", "any third party (including an Affiliate) engaged by "
         f"{OP} to Process Customer Data on its behalf."),
        ("“NIST CSF”", "the NIST Cybersecurity Framework (currently version 2.0)."),
        ("“Covered Equipment”", "telecommunications or video-surveillance equipment "
         "or services prohibited under 47 U.S.C. § 1601 et seq. (Section 889) and "
         f"{C.CITES['telecom_ban']}."),
    ]
    for term, body in defs:
        sub(doc, term.strip('“”'), f"{term} means {body}")

    # ============ ARTICLE 3 — OWNERSHIP & PERMITTED USE ====================
    C.article(doc, 3, "Ownership and Permitted Use of Customer Data")

    C.section(doc, "3.1", "Ownership — Alternatives")
    C.para(doc, "The Parties have not finalized the allocation of ownership of "
                "Customer Data. The following alternatives are presented for decision:")
    sub(doc, "a", f"Alternative A — Operator ownership. {OP} owns Customer Data it "
                  f"collects, subject to a perpetual, royalty-free license to the "
                  f"{TRIBE} and the return/portability rights in Articles 17–18.")
    sub(doc, "b", f"Alternative B — Tribal ownership. The {TRIBE} owns all Customer "
                  f"Data relating to subscribers in the {C.SERVICE_TERRITORY}, and "
                  f"{OP} holds a limited license to Process it solely to operate the "
                  f"Network and provide services.")
    sub(doc, "c", f"Alternative C (RECOMMENDED) — Joint framework. The Parties adopt "
                  f"a joint stewardship framework: {OP} owns Network Data and its own "
                  f"derived operational analytics; Customer Data is jointly held, with "
                  f"the {TRIBE} owning all Tribal Data and holding, at all times, a "
                  f"perpetual, irrevocable, royalty-free right to access, copy, and "
                  f"receive Customer Data in portable form, and with exclusive rights "
                  f"vesting in the {TRIBE} on transition to a successor operator "
                  f"(Article 18).")
    C.flag_para(doc, C.FLAG_BUSINESS,
                f"Ownership of Customer Data is a business decision with material "
                f"downstream effects on marketing rights, data monetization, and "
                f"transition leverage. RECOMMENDATION: adopt Alternative C (joint "
                f"framework with {TRIBE} rights on transition). Confirm and set "
                f"{C.PH('selected ownership alternative and any revenue-data carve-outs')}.")

    C.section(doc, "3.2", "Permitted Uses by RIVR Tech",
              f"Regardless of the ownership alternative selected, {OP} may Process "
              f"Customer Data only to: (a) provide, bill for, maintain, and support "
              f"services over the Network; (b) protect the security and integrity of "
              f"the Network and prevent fraud; (c) comply with law and the Award; and "
              f"(d) perform analytics in aggregated or de-identified form that cannot "
              f"reasonably be re-identified. Any other use, including sale, licensing, "
              f"or use for targeted advertising to third parties, requires the {TRIBE}’s "
              f"prior written consent and, where applicable, subscriber consent under "
              f"the CPNI rules.")

    C.section(doc, "3.3", "Restrictions",
              f"{OP} shall not (a) sell Customer Data; (b) disclose Customer Data to "
              f"any third party except a Subprocessor bound under Article 13 or as "
              f"required by law under Article 15; (c) use Tribal Data outside the "
              f"{C.SERVICE_TERRITORY} except as permitted under Article 16; or "
              f"(d) commingle Customer Data with other data in a manner that prevents "
              f"its segregation, extraction, and return under Articles 17–18.")

    C.section(doc, "3.4", "De-identified and Aggregated Data",
              f"{OP} may create and use de-identified or aggregated data derived from "
              f"Customer Data, provided it (a) commits publicly not to attempt "
              f"re-identification, (b) contractually binds recipients to the same "
              f"restriction, and (c) does not disclose any dataset small enough to "
              f"permit re-identification of individuals or households in the "
              f"{C.SERVICE_TERRITORY}.")

    # ============ ARTICLE 4 — CPNI =========================================
    C.article(doc, 4, "Customer Proprietary Network Information (CPNI)")

    C.section(doc, "4.1", "Compliance",
              f"To the extent {OP} provides telecommunications service or interconnected "
              f"VoIP service over the Network, {OP} shall comply with {C.CITES['cpni']} "
              f"and shall maintain and, upon request, provide to the {TRIBE} the annual "
              f"CPNI compliance certificate and accompanying statement filed with the FCC.")

    C.section(doc, "4.2", "Use, Disclosure and Approval",
              "CPNI shall be used, disclosed, and permitted access to only as authorized "
              "by 47 U.S.C. § 222 and the FCC’s implementing rules, including the "
              "opt-in / opt-out approval, notice, and record-keeping requirements of "
              "47 CFR §§ 64.2007–64.2009.")

    C.section(doc, "4.3", "Safeguards and Authentication",
              "RIVR Tech shall implement the CPNI safeguards required by 47 CFR "
              "§§ 64.2009–64.2010, including authentication of subscribers before "
              "disclosing call-detail information, password and back-up authentication "
              "controls, and notification to subscribers of account changes.")

    C.section(doc, "4.4", "CPNI Breach Notification",
              "RIVR Tech shall comply with the FCC’s CPNI and customer-data breach "
              "notification rules, including law-enforcement notification through the "
              "central reporting facility and subscriber notification within the "
              "timeframes required by the rules as then in effect. CPNI breach "
              "handling is coordinated with the incident process in Article 11.")

    # ============ ARTICLE 5 — PRIVACY NOTICES ==============================
    C.article(doc, 5, "Privacy Notices and Consent")
    C.section(doc, "5.1", "Privacy Notice",
              f"{OP} shall maintain a clear, accurate, and accessible privacy notice "
              f"describing the categories of Customer Data Processed, the purposes of "
              f"Processing, retention periods, subscriber choices, and how subscribers "
              f"may exercise their rights. {OP} shall provide the {TRIBE} a copy of "
              f"each notice and each material revision at least "
              f"{C.PH('notice-review period, e.g., 15 business days')} before it takes "
              f"effect for subscribers in the {C.SERVICE_TERRITORY}.")
    C.section(doc, "5.2", "Consent and Choice",
              "Where consent is required by law or by this Addendum, RIVR Tech shall "
              "obtain and document it, and shall honor subscriber requests to access, "
              "correct, delete, or restrict Processing of their Personal Information to "
              "the extent required by applicable law, subject to record-retention and "
              "grant-compliance obligations.")
    C.section(doc, "5.3", "Tribal Notice Coordination",
              f"For subscribers in the {C.SERVICE_TERRITORY}, {OP} shall coordinate "
              f"with the {TRIBE} so that privacy notices are consistent with any "
              f"privacy or data-governance policy adopted by the {TRIBE}.")

    # ============ ARTICLE 6 — DATA RETENTION ===============================
    C.article(doc, 6, "Data Retention and Minimization")
    C.section(doc, "6.1", "Retention Principles",
              "RIVR Tech shall retain Customer Data only as long as necessary for the "
              "purposes for which it was collected, to comply with law and the Award, "
              "and to support billing disputes and audits, and shall then securely "
              "destroy or de-identify it under Article 17.")
    C.section(doc, "6.2", "Grant Records Retention",
              f"Records relating to the Award, including records necessary to "
              f"substantiate {C.PROGRAM_INCOME}, matching, and cost allowability, shall "
              f"be retained for at least {RET_YRS} years in accordance with "
              f"{C.CITES['records']} (measured from submission of the final financial "
              f"report, and longer if litigation, claim, or audit is pending).")
    C.section(doc, "6.3", "CPNI and Billing Retention",
              "CPNI, billing, and call-detail records shall be retained consistent with "
              "47 CFR Part 42 and the CPNI rules, and no shorter than required by "
              "applicable law.")

    C.para(doc, "The following retention schedule is a working default:", italic=True)
    C.add_table(
        doc,
        ["Data Category", "Illustrative Owner (per Art. 3)", "Retention Default", "Authority"],
        [
            ["Subscriber account & contact", "Joint / Tribe (Tribal Data)",
             C.PH("e.g., life of account + 3 yrs"), "Contract; state law"],
            ["Billing & payment records", f"Joint",
             "No less than " + C.PH("e.g., 3–7 yrs"), "47 CFR Pt 42; " + C.CITES['records']],
            ["CPNI / call-detail", f"{OP} steward",
             C.PH("per FCC / 47 CFR Pt 42"), C.CITES['cpni']],
            ["Grant-substantiation records", "Tribe (Federal Interest)",
             f"≥ {RET_YRS} yrs from final report", C.CITES['records']],
            ["Network telemetry / logs", f"{OP}",
             C.PH("e.g., 12–24 months"), "Security best practice"],
            ["Security-incident records", f"Joint",
             C.PH("e.g., ≥ 3 yrs"), "NIST CSF; breach rules"],
        ],
        widths=[1.9, 1.9, 1.6, 2.0],
        col_align=["l", "l", "c", "l"],
    )
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Confirm retention periods against the final CPNI rules, 47 CFR Part 42, "
                "state breach-notification law, and any Tribal records policy. Retention "
                "must not fall below the grant three-year floor for Award-related records.")

    # ============ ARTICLE 7 — CYBERSECURITY PROGRAM ========================
    C.article(doc, 7, "Cybersecurity Program and Standards")
    C.section(doc, "7.1", "Security Program",
              f"{OP} shall establish, maintain, and continuously improve a written "
              f"information-security program that is aligned with the NIST Cybersecurity "
              f"Framework (Govern, Identify, Protect, Detect, Respond, Recover) and that "
              f"implements controls consistent with NIST SP 800-53 (moderate baseline as "
              f"a target) and applicable CISA guidance (including CISA Cyber Performance "
              f"Goals). The program shall be commensurate with the risk and sensitivity "
              f"of the Customer Data and the criticality of the {C.NETWORK}.")
    C.section(doc, "7.2", "Covered-Equipment Prohibition (Section 889)",
              f"{OP} shall not use Award funds to procure or use, and shall not connect "
              f"to the {C.TRIBAL_ASSETS}, any Covered Equipment prohibited under "
              f"{C.CITES['telecom_ban']}. {OP} shall represent compliance and promptly "
              f"disclose any discovered Covered Equipment and its remediation plan.")
    C.section(doc, "7.3", "Governance and Personnel",
              f"{OP} shall designate a security officer accountable for the program, "
              f"conduct background screening consistent with law for personnel with "
              f"access to Customer Data, and provide annual security and privacy "
              f"(including CPNI) training.")
    C.section(doc, "7.4", "Risk Assessment and Testing",
              f"{OP} shall perform at least an annual risk assessment and "
              f"{C.PH('penetration-test / independent assessment cadence, e.g., annual')}, "
              f"remediate findings on a risk-prioritized basis, and provide the {TRIBE} "
              f"a summary of results and remediation status on request.")
    C.section(doc, "7.5", "Audit and Evidence",
              f"On reasonable notice and no more than {C.PH('frequency, e.g., annually')} "
              f"(and after any Breach), the {TRIBE} or its designee may review {OP}’s "
              f"security certifications (e.g., SOC 2 Type II, if any), policies, and "
              f"evidence of control operation, subject to confidentiality.")

    # ============ ARTICLE 8 — ACCESS CONTROLS ==============================
    C.article(doc, 8, "Access Controls")
    C.section(doc, "8.1", "Least Privilege and MFA",
              "RIVR Tech shall enforce role-based, least-privilege access; require "
              "multi-factor authentication for all remote and administrative access to "
              "systems that Process Customer Data; and uniquely identify and "
              "authenticate each user (no shared administrative credentials except in "
              "audited break-glass procedures).")
    C.section(doc, "8.2", "Provisioning and Review",
              "Access shall be provisioned on documented approval, reviewed at least "
              "quarterly, and revoked promptly (within " + C.PH("e.g., 24 hours") +
              ") upon role change or separation.")
    C.section(doc, "8.3", "Logging and Monitoring",
              "RIVR Tech shall log access to and administrative actions on systems that "
              "Process Customer Data, protect logs from tampering, and monitor for "
              "anomalous activity consistent with the Detect function of the NIST CSF.")

    # ============ ARTICLE 9 — ENCRYPTION ===================================
    C.article(doc, 9, "Encryption")
    C.section(doc, "9.1", "Encryption in Transit",
              "RIVR Tech shall encrypt Customer Data in transit over public or "
              "untrusted networks using current, non-deprecated protocols "
              "(e.g., TLS 1.2 or higher) and strong cipher suites.")
    C.section(doc, "9.2", "Encryption at Rest",
              "RIVR Tech shall encrypt Customer Data at rest, including in databases, "
              "backups, and portable media, using industry-standard algorithms "
              "(e.g., AES-256) and shall not store Sensitive Personal Information or "
              "credentials in plaintext.")
    C.section(doc, "9.3", "Key Management",
              "RIVR Tech shall manage cryptographic keys under a documented key-"
              "management process, including secure generation, storage separate from "
              "the data they protect, rotation, and revocation.")

    # ============ ARTICLE 10 — VULNERABILITY MANAGEMENT ====================
    C.article(doc, 10, "Vulnerability and Patch Management")
    C.section(doc, "10.1", "Program",
              "RIVR Tech shall maintain a vulnerability-management program that "
              "identifies, prioritizes, and remediates vulnerabilities on a "
              "risk-based schedule.")
    C.para(doc, "The following remediation targets are a working default:", italic=True)
    C.add_table(
        doc,
        ["Severity", "Illustrative Definition", "Remediation Target"],
        [
            ["Critical", "Actively exploited / remote code execution on exposed system",
             C.PH("e.g., 7 days / emergency")],
            ["High", "Exploitable, significant impact", C.PH("e.g., 30 days")],
            ["Medium", "Limited impact / harder to exploit", C.PH("e.g., 90 days")],
            ["Low", "Minimal impact", C.PH("e.g., next maintenance cycle")],
        ],
        widths=[1.1, 3.6, 2.0],
        col_align=["c", "l", "c"],
    )
    C.section(doc, "10.2", "Secure Development and Change",
              "Changes to systems that Process Customer Data shall follow documented "
              "change-management and secure-configuration practices, with segregation "
              "of duties for production changes.")

    # ============ ARTICLE 11 — INCIDENT & BREACH NOTIFICATION ==============
    C.article(doc, 11, "Security Incident and Breach Notification")
    C.section(doc, "11.1", "Incident Response Plan",
              "RIVR Tech shall maintain a written incident-response plan aligned with "
              "the Respond and Recover functions of the NIST CSF, test it at least "
              "annually, and coordinate incident handling with the O&M/SLA (Document "
              "02.03) severity and escalation model.")
    C.section(doc, "11.2", "Notification to the Tribe")
    C.para(doc, f"{OP} shall notify the {TRIBE} of a Security Incident affecting, or "
                f"reasonably likely to affect, Customer Data or Tribal Data without "
                f"undue delay and no later than {C.PH('e.g., 24–72')} hours after "
                f"{OP} becomes aware of it, and shall provide updates as material facts "
                f"develop.")
    C.para(doc, "The following notification defaults are proposed:", italic=True)
    C.add_table(
        doc,
        ["Event", "Notify Whom", "Default Timeline", "Authority / Cross-ref"],
        [
            ["Suspected Security Incident (Tribal Data)", f"{TRIBE} security contact",
             C.PH("e.g., within 24 hrs of awareness"), "This Art. 11; O&M/SLA 02.03"],
            ["Confirmed Breach of CPNI", "Law enforcement + subscribers + " + TRIBE,
             "Per FCC rule timeline", C.CITES['cpni']],
            ["Breach of Personal Information", f"{TRIBE} + affected individuals + AG",
             C.PH("per state law / e.g., without unreasonable delay"),
             C.STATE + " breach-notification law"],
            ["Ransomware / availability event", f"{TRIBE} + O&M NOC",
             C.PH("e.g., immediately / within 4 hrs"), "Art. 12; O&M/SLA 02.03; CISA"],
            ["Incident threatening the Award", f"{TRIBE} grants contact",
             C.PH("promptly; support 200.113 disclosure"), C.CITES['disclosures']],
        ],
        widths=[2.2, 2.0, 1.7, 1.6],
        col_align=["l", "l", "c", "l"],
    )
    C.section(doc, "11.3", "Cooperation and Content of Notice",
              f"Each notice shall describe, to the extent known, the nature of the "
              f"incident, the categories and volume of data involved, the subscribers or "
              f"members affected in the {C.SERVICE_TERRITORY}, containment and "
              f"remediation steps, and points of contact. {OP} shall preserve evidence, "
              f"cooperate with the {TRIBE}’s reasonable requests, and support any "
              f"disclosure the {TRIBE} must make under {C.CITES['disclosures']}.")
    C.section(doc, "11.4", "Costs and Regulatory Notices",
              f"Where a Breach is caused by {OP}’s act, omission, or failure to meet "
              f"its obligations, {OP} shall bear the reasonable costs of investigation, "
              f"required notifications, credit monitoring where appropriate, and "
              f"regulatory response, subject to the limitation-of-liability provisions "
              f"of the Master Agreement.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Confirm all notification timelines against the FCC CPNI/customer-data "
                "breach rules as then in effect and the North Carolina Identity Theft "
                "Protection Act (and any Tribal breach law). Do not finalize the hour "
                "counts without communications-privacy counsel.")

    # ============ ARTICLE 12 — RANSOMWARE ==================================
    C.article(doc, 12, "Ransomware Response")
    C.section(doc, "12.1", "Preparedness",
              "RIVR Tech shall maintain ransomware-specific safeguards, including "
              "segmented and immutable/offline backups, tested restoration procedures, "
              "email and endpoint protections, and privileged-access controls.")
    C.section(doc, "12.2", "Response",
              f"On a ransomware event, {OP} shall isolate affected systems, activate the "
              f"incident-response and business-continuity plans, notify the {TRIBE} "
              f"under Article 11, and coordinate with law enforcement and CISA as "
              f"appropriate.")
    C.section(doc, "12.3", "Ransom Payments",
              f"{OP} shall not make, facilitate, or cause any ransom or extortion payment "
              f"relating to the {C.NETWORK} or Customer Data without the {TRIBE}’s prior "
              f"written consent, and shall comply with OFAC and other sanctions law. "
              f"{C.PH('confirm ransom-payment decision protocol and OFAC screening')}.")

    # ============ ARTICLE 13 — THIRD-PARTY VENDORS =========================
    C.article(doc, 13, "Third-Party Vendors and Supply Chain")
    C.section(doc, "13.1", "Flow-Down",
              f"{OP} shall bind each Subprocessor by written agreement to data-"
              f"protection, security, confidentiality, incident-notification, and "
              f"return/destruction obligations no less protective than this Addendum, "
              f"including the Covered-Equipment prohibition (Section 7.2) and applicable "
              f"grant flow-downs, and remains responsible for its Subprocessors’ acts "
              f"and omissions.")
    C.section(doc, "13.2", "Subprocessor Transparency",
              f"{OP} shall maintain a current list of Subprocessors that Process Tribal "
              f"Data and provide it to the {TRIBE} on request. The {TRIBE} may object to "
              f"a Subprocessor on reasonable data-protection or sovereignty grounds; the "
              f"Parties shall work in good faith to address the objection.")
    C.section(doc, "13.3", "Software Bill of Materials (SBOM)",
              f"For material software and firmware components used in systems that "
              f"Process Customer Data or control the {C.TRIBAL_ASSETS}, {OP} shall "
              f"obtain or maintain a Software Bill of Materials (SBOM) and use it to "
              f"support vulnerability management and Section 889 screening. "
              f"{C.PH('confirm SBOM scope and format, e.g., SPDX / CycloneDX')}.")

    # ============ ARTICLE 14 — BC/DR =======================================
    C.article(doc, 14, "Business Continuity and Disaster Recovery")
    C.section(doc, "14.1", "Plans",
              f"{OP} shall maintain and test business-continuity and disaster-recovery "
              f"plans for systems that Process Customer Data and operate the "
              f"{C.NETWORK}, coordinated with the resilience, redundancy, and "
              f"restoration commitments in the O&M/SLA (Document 02.03).")
    C.section(doc, "14.2", "Objectives",
              f"Recovery-time and recovery-point objectives (RTO/RPO) for critical "
              f"data and services shall be no less protective than "
              f"{C.PH('RTO / RPO targets — align with O&M/SLA 02.03')}.")
    C.section(doc, "14.3", "Backups",
              "Backups of Customer Data shall be encrypted, access-controlled, "
              "geographically appropriate (subject to Article 16), and tested for "
              "restorability at least annually.")

    # ============ ARTICLE 15 — LAW ENFORCEMENT =============================
    C.article(doc, 15, "Law-Enforcement and Government Requests")
    C.section(doc, "15.1", "Validity and Minimization",
              f"{OP} shall disclose Customer Data in response to a subpoena, warrant, "
              f"court order, or other legal process only to the extent legally required, "
              f"shall review each request for validity and scope, and shall disclose the "
              f"minimum data necessary.")
    C.section(doc, "15.2", "Notice to the Tribe",
              f"Where not legally prohibited, {OP} shall notify the {TRIBE} before "
              f"disclosing Tribal Data in response to legal process, so the {TRIBE} may "
              f"seek to limit or quash the request, and shall reasonably cooperate with "
              f"the {TRIBE}’s lawful efforts to protect the data.")
    C.section(doc, "15.3", "Records",
              "RIVR Tech shall keep a record of law-enforcement requests affecting "
              "Tribal Data and make summary information available to the Tribe on "
              "request, subject to legal limits.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "The interaction of Tribal sovereignty, ECPA/Stored Communications Act, "
                "CALEA, and any protective-order or gag provisions is fact-specific. "
                "Counsel must confirm the notice-to-Tribe mechanics and any limits on "
                "pre-disclosure notice.")

    # ============ ARTICLE 16 — TRIBAL DATA SOVEREIGNTY =====================
    C.article(doc, 16, "Tribal Data Sovereignty")
    C.section(doc, "16.1", "Recognition of Sovereign Interest",
              f"The Parties recognize the {TRIBE}’s inherent sovereign interest in, and "
              f"governance authority over, Tribal Data, including data of enrolled "
              f"members and of subscribers within the {C.SERVICE_TERRITORY}. Tribal Data "
              f"shall be Processed in a manner consistent with the {TRIBE}’s data-"
              f"governance principles and applicable Tribal law, consistent with the "
              f"CARE principles for Indigenous data governance and the concept of "
              f"Indigenous data sovereignty.")
    C.section(doc, "16.2", "Data Residency and Access — Options")
    C.para(doc, "The Parties will select a data-residency and access model:")
    sub(doc, "a", f"Option 1 — U.S.-only Processing. Tribal Data is Processed and "
                  f"stored only within the United States, with no offshore access.")
    sub(doc, "b", f"Option 2 — U.S.-only plus enhanced access controls. Option 1 plus "
                  f"{TRIBE}-visible logging of administrative access to Tribal Data.")
    sub(doc, "c", f"Option 3 (RECOMMENDED baseline) — In-territory/Tribally-designated "
                  f"hosting where feasible. Tribal Data of record is maintained in a "
                  f"repository located in the United States and, where technically and "
                  f"commercially feasible, in a location or under a cloud configuration "
                  f"designated or approved by the {TRIBE}, with the {TRIBE} holding "
                  f"independent access to a copy of its Tribal Data.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                f"Tribal data-residency and access rights implicate sovereignty, "
                f"contract, and technical-feasibility questions. Select the model and "
                f"confirm enforceability and cost with counsel and the {TRIBE}’s "
                f"technical team: {C.PH('selected data-residency / access option and location')}.")
    C.section(doc, "16.3", "Tribal Governance and Audit",
              f"The {TRIBE} may adopt data-governance, privacy, or research-review "
              f"policies applicable to Tribal Data, and may audit {OP}’s handling of "
              f"Tribal Data on reasonable notice, subject to confidentiality.")
    C.section(doc, "16.4", "No Waiver",
              f"Nothing in this Addendum constitutes a waiver of the {TRIBE}’s sovereign "
              f"immunity or sovereign authority. Any waiver must be express, written, "
              f"and limited as provided in the Master Agreement.")

    # ============ ARTICLE 17 — RETURN & DESTRUCTION ========================
    C.article(doc, 17, "Return and Destruction of Data")
    C.section(doc, "17.1", "On Expiration or Termination",
              f"On expiration or termination of the Master Agreement, or on the {TRIBE}’s "
              f"request during a transition under Document 02.07, {OP} shall, at the "
              f"{TRIBE}’s election, return to the {TRIBE} or a successor operator, and/or "
              f"securely destroy, all Customer Data and Tribal Data in {OP}’s possession "
              f"or control, except copies required to be retained by law or the Award.")
    C.section(doc, "17.2", "Secure Destruction",
              "Destruction shall follow recognized media-sanitization standards "
              "(e.g., NIST SP 800-88) such that data cannot be reconstructed, and "
              "RIVR Tech shall certify destruction in writing.")
    C.section(doc, "17.3", "Retained Copies",
              f"Any lawfully retained copies remain subject to the confidentiality, "
              f"security, and use-restriction obligations of this Addendum for as long "
              f"as {OP} retains them, and grant-substantiation records remain subject to "
              f"{C.CITES['records']}.")

    # ============ ARTICLE 18 — TRANSITION / PORTABILITY ====================
    C.article(doc, 18, "Transition to a Successor Operator — Data Portability")
    C.section(doc, "18.1", "Portability",
              f"To ensure continuity of service and to protect the {C.FEDERAL_INTEREST}, "
              f"{OP} shall, on transition, deliver Customer Data, Network Data necessary "
              f"to operate the {C.TRIBAL_ASSETS}, and associated records to the {TRIBE} "
              f"or its designated successor operator in a complete, usable, and "
              f"non-proprietary or documented format, together with data dictionaries "
              f"and reasonable knowledge-transfer support.")
    C.section(doc, "18.2", "Coordination with the Transition Plan",
              f"Data portability under this Article is coordinated with, and subject to "
              f"the mechanics of, the Transition, Step-In and Successor Operator Plan "
              f"(Document 02.07), including the transition-assistance period of "
              f"{TA_MONTHS} months and the protection of the {C.OPERATOR_EXISTING}.")
    C.section(doc, "18.3", "Continuity of Subscriber Relationships",
              f"The Parties shall handle Customer Data during transition so as to "
              f"preserve subscriber service, billing accuracy, and number portability, "
              f"and to comply with the CPNI rules governing carrier changes.")
    C.flag_para(doc, C.FLAG_GRANT,
                f"Because the {C.TRIBAL_ASSETS} and related intangible property carry a "
                f"{C.FEDERAL_INTEREST}, data and records enabling continued operation "
                f"must transfer to the {TRIBE} or a successor. Confirm treatment of "
                f"intangible property under {C.CITES['intangible']} and disposition rules.")

    # ============ ARTICLE 19 — AUDIT & COMPLIANCE ==========================
    C.article(doc, 19, "Audit, Compliance and Records")
    C.section(doc, "19.1", "Federal Audit and Access",
              f"{OP} shall provide the {TRIBE}, {C.AGENCY_SHORT}, the Department of "
              f"Commerce, the Inspector General, and the Comptroller General (and their "
              f"authorized representatives) timely access to records and data relating "
              f"to the Award to the extent required by {C.CITES['records']}, on the "
              f"notice window used across the package ({C.DEAL['audit_notice_business_days']} "
              f"business days, or immediately where required by the auditing authority).")
    C.section(doc, "19.2", "USAC / Universal Service",
              f"Where services over the Network participate in universal-service "
              f"programs, {OP} shall maintain records and comply with "
              f"{C.CITES['usac_lifeline']}, including any Lifeline eligibility and "
              f"recertification data-handling requirements.")
    C.section(doc, "19.3", "Compliance Reporting",
              f"{OP} shall provide the {TRIBE} periodic privacy and security compliance "
              f"reporting at {C.PH('cadence, e.g., quarterly')}, and promptly report any "
              f"matter that could constitute a mandatory disclosure under "
              f"{C.CITES['disclosures']}.")

    # ============ ARTICLE 20 — GENERAL =====================================
    C.article(doc, 20, "General Provisions")
    C.section(doc, "20.1", "Governing Law")
    C.para(doc, f"The governing law of this Addendum is not finalized. The Parties will "
                f"select from: (a) the law of the {C.STATE} (excluding conflicts "
                f"principles); (b) the law of the {C.STATE} for commercial matters with "
                f"the law and jurisdiction of the {C.TRIBE_FULL} governing questions of "
                f"Tribal sovereignty, Tribal Data, and conduct within the "
                f"{C.SERVICE_TERRITORY}; or (c) federal law where it controls the Award. "
                f"{C.PH('selected governing-law alternative')}.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Governing law, dispute resolution, and any limited waiver of sovereign "
                "immunity must not be selected silently. Counsel for the Tribe must "
                "confirm the alternative and its interaction with the Master Agreement.")
    C.section(doc, "20.2", "Sovereign Immunity",
              f"Nothing in this Addendum waives the sovereign immunity of the "
              f"{C.TRIBE_FULL}. Any limited waiver, if agreed, must be express, written, "
              f"specifically identify the claims and remedies covered, and be authorized "
              f"as required by Tribal law. {C.PH('cross-reference Master Agreement sovereign-immunity section')}.")
    C.section(doc, "20.3", "Order of Precedence",
              f"In the event of a conflict, the order of precedence is: (a) the Award "
              f"terms and applicable federal law; (b) the Master Agreement (Document "
              f"02.01); (c) this Addendum (Document 02.06); and (d) the O&M/SLA "
              f"(Document 02.03), except that this Addendum controls on matters of data "
              f"privacy, CPNI, cybersecurity, and Tribal Data sovereignty.")
    C.section(doc, "20.4", "Survival",
              "The obligations relating to confidentiality, CPNI, return/destruction, "
              "records retention, Tribal Data sovereignty, audit, and breach liability "
              "survive expiration or termination for the periods required by law and "
              "the Award.")
    C.section(doc, "20.5", "Amendment",
              "This Addendum may be amended only by a writing signed by both Parties, "
              "subject to any Award-required approvals.")

    C.signature_block(
        doc,
        extra_note="Confirm signatory authority, sovereign-immunity/governing-law "
        "selections, and CPNI/breach-notice timelines before execution.",
    )

    path = C.save(doc, "02_Core_Agreements",
                  "06_Data_Privacy_and_Cybersecurity_Addendum.docx")
    return path


# ===========================================================================
#  DOCUMENT 7 — TRANSITION, STEP-IN & SUCCESSOR OPERATOR PLAN
# ===========================================================================
def build_transition_plan():
    doc = C.new_doc()

    C.add_cover(
        doc,
        "Document 7 (Schedule 02.07 to the Master Agreement)",
        "Transition, Step-In & Successor Operator Plan",
        "Triggering Events, Cure, Emergency Tribal Step-In, Transition "
        "Assistance and Asset Protection",
    )
    C.setup_header_footer(doc, "Transition, Step-In & Successor Operator Plan")
    C.add_toc(doc)

    C.status_banner(doc)
    C.spacer(doc, 1)

    # ---- Preamble ---------------------------------------------------------
    C.para(
        doc,
        f"This Transition, Step-In and Successor Operator Plan (this “Plan”) is "
        f"entered into as of {C.PH('Effective Date — conform to Master Agreement')} "
        f"(the “Effective Date”), by and between {C.TRIBE_FULL} (the “{TRIBE}”), or "
        f"{C.TRIBE_ENTITY_ALT}, and {C.OPERATOR_FULL} (“{OP}”). This Plan is Schedule "
        f"02.07 to, and is incorporated by reference into, the Master IRU and Network "
        f"Operations Agreement (the “Master Agreement,” Document 02.01) and is read "
        f"together with the O&M/SLA (Document 02.03) and the Data Privacy & "
        f"Cybersecurity Addendum (Document 02.06).",
    )
    C.para(
        doc,
        f"The purpose of this Plan is to protect continuity of Essential Services over "
        f"the {C.NETWORK}, to safeguard the {C.TRIBAL_ASSETS} and the "
        f"{C.FEDERAL_INTEREST}, and to provide an orderly framework for cure, temporary "
        f"Tribal step-in, and, if necessary, transition to a successor operator — while "
        f"protecting {OP}’s ownership of the {C.OPERATOR_EXISTING} and its {C.IRU_TERM_DEFINED} "
        f"and lender-protection rights.",
    )
    C.flag_para(doc, C.FLAG_GRANT,
                f"A step-in or successor-operator transition must preserve the "
                f"{C.FEDERAL_INTEREST} in the {C.TRIBAL_ASSETS} and comply with "
                f"{C.CITES['real_property']}, {C.CITES['equipment']}, and "
                f"{C.CITES['intangible']}. {C.CITES['lumbee_act']} bears on the "
                f"{TRIBE}’s eligibility to hold the Award; confirm before execution.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Step-in, assignment, lender-protection, sovereign-immunity, and "
                "governing-law mechanics must be reviewed by counsel for the Tribe and "
                "by finance/lender counsel before execution.")

    # ================= ARTICLE 1 — PURPOSE & DEFINITIONS ===================
    C.article(doc, 1, "Purpose, Scope and Definitions")
    C.section(doc, "1.1", "Consistency with Master Agreement and O&M/SLA",
              f"The default, notice, cure, and step-in mechanics in this Plan are the "
              f"same as those in the Master Agreement (Section 02.01) and the O&M/SLA "
              f"(Section 02.03): a {C.DEAL['notice_default_days']}-day notice-and-cure "
              f"period for monetary defaults ({CURE_M} days) and a {CURE_NM}-day cure "
              f"period for non-monetary defaults, with {CURE_EXT}. Emergency step-in is "
              f"{STEPIN}.")
    C.section(doc, "1.2", "Definitions")
    C.para(doc, "Capitalized terms not defined here have the meanings given in the "
                "Master Agreement. In addition:")
    for term, body in [
        ("“Essential Services”", f"broadband, voice, and any public-safety or "
         f"institutional connectivity provided over the {C.NETWORK} whose interruption "
         f"would materially harm subscribers, public safety, or the Award."),
        ("“Step-In”", f"the temporary assumption by the {TRIBE} or its designee of "
         f"operational control of the {C.TRIBAL_ASSETS} (and only the rights necessary "
         f"for continuity) as provided in Articles 5–7."),
        ("“Successor Operator”", f"a qualified operator (which may be the {TRIBE}, a "
         f"Tribal entity, or a third party) that assumes operation of the "
         f"{C.TRIBAL_ASSETS} following transition."),
        ("“Transition-Assistance Period”", f"the period, initially {TA_MONTHS} months "
         f"and extendable under Section 15.2, during which {OP} supports transition."),
        ("“Leasehold/IRU Interest”", f"{OP}’s {C.IRU_TERM_DEFINED} and related rights "
         f"in capacity or fiber, protected under Article 17."),
        ("“Lender”", f"a bona fide third-party financing source holding a security "
         f"interest in {OP}’s assets or {C.IRU_TERM_DEFINED} interest, entitled to the "
         f"protections in Section 17.4."),
    ]:
        sub(doc, term.strip('“”'), f"{term} means {body}")

    # ================= ARTICLE 2 — TRIGGERING EVENTS =======================
    C.article(doc, 2, "Triggering Events")
    C.para(doc, "Each of the following is a “Triggering Event” that may give rise to "
                "cure, Step-In, or transition rights as provided in this Plan:")
    for lbl, txt in [
        ("a", "Uncured Default. A default by RIVR Tech under the Master Agreement or "
              "O&M/SLA that remains uncured after the applicable notice-and-cure "
              "period in Article 4."),
        ("b", "Insolvency. RIVR Tech’s insolvency, general assignment for the benefit "
              "of creditors, or the filing of a bankruptcy or receivership proceeding "
              "that is not dismissed within " + C.PH("e.g., 60") + " days, subject to "
              "applicable bankruptcy law."),
        ("c", "Abandonment. RIVR Tech’s abandonment of, or sustained failure to "
              f"operate, the {C.TRIBAL_ASSETS} or Essential Services."),
        ("d", "Loss of Authorizations. Loss, suspension, or non-renewal of a license, "
              "franchise, ETC designation, pole-attachment right, spectrum, or other "
              "authorization materially necessary to operate the Network."),
        ("e", "Chronic SLA Failure. Chronic or repeated failure to meet the material "
              "service levels in the O&M/SLA (Document 02.03) at the thresholds defined "
              "there (e.g., repeated missed availability or restoration targets)."),
        ("f", "Grant-Compliance Failure. A failure to comply with the Award or "
              "applicable federal requirements that threatens the Award, the "
              f"{C.FEDERAL_INTEREST}, or the {TRIBE}’s standing as recipient, including "
              f"a matter requiring disclosure under {C.CITES['disclosures']}."),
        ("g", "Change in Control without Consent. A change in control of RIVR Tech, or "
              f"an assignment or encumbrance of its rights, without any consent required "
              f"by the Master Agreement or the Award."),
        ("h", "Covered-Equipment / Security Failure. Use of prohibited Covered Equipment "
              f"({C.CITES['telecom_ban']}) or a material security failure under Document "
              f"02.06 that imminently threatens Customer Data or continuity."),
    ]:
        sub(doc, lbl, txt)

    # ================= ARTICLE 3 — NOTICE ==================================
    C.article(doc, 3, "Notice")
    C.section(doc, "3.1", "Notice of Triggering Event",
              f"On the occurrence of a Triggering Event, the {TRIBE} shall give {OP} "
              f"written notice describing the event, the asserted basis, and (where a "
              f"cure is available) the cure required, except that no prior notice is "
              f"required to exercise Emergency Step-In under Article 5 where the "
              f"conditions in Section 5.1 are met.")
    C.section(doc, "3.2", "Notice to Lenders and NTIA",
              f"Where required, the {TRIBE} shall also provide notice to a Lender "
              f"entitled to notice under Section 17.4 and shall coordinate with "
              f"{C.AGENCY_SHORT} to the extent the Award requires notice of events "
              f"affecting the {C.FEDERAL_INTEREST}.")

    # ================= ARTICLE 4 — CURE ====================================
    C.article(doc, 4, "Cure Periods")
    C.section(doc, "4.1", "Monetary Default",
              f"RIVR Tech shall have {CURE_M} days after written notice to cure a "
              f"monetary default.")
    C.section(doc, "4.2", "Non-Monetary Default",
              f"RIVR Tech shall have {CURE_NM} days after written notice to cure a "
              f"non-monetary default, with {CURE_EXT}.")
    C.section(doc, "4.3", "No Cure for Certain Events",
              "Emergency conditions under Article 5, and Triggering Events that are by "
              "nature not curable (e.g., certain losses of authorization), may permit "
              "Step-In or transition without a cure period, subject to applicable law "
              "and the protections of Articles 17–18.")
    C.section(doc, "4.4", "Effect of Cure",
              "A timely and complete cure reinstates the status quo and terminates the "
              "related Step-In or transition rights arising from that Triggering Event, "
              "without prejudice to rights arising from subsequent events.")

    # ================= ARTICLE 5 — EMERGENCY STEP-IN =======================
    C.article(doc, 5, "Emergency Tribal Step-In")
    C.section(doc, "5.1", "Right of Emergency Step-In",
              f"The {TRIBE} (or its designee) may exercise Emergency Step-In "
              f"{STEPIN}. Emergency Step-In may be exercised without a prior cure period "
              f"but with notice given as promptly as practicable, including "
              f"contemporaneous or after-the-fact notice where advance notice is not "
              f"feasible.")
    C.section(doc, "5.2", "Scope Limited to Tribal Assets",
              f"Emergency Step-In extends only to operational control of the "
              f"{C.TRIBAL_ASSETS} and to the rights (including access, credentials, and "
              f"vendor cooperation) reasonably necessary to maintain Essential Services. "
              f"It does not transfer ownership of any asset and does not extend to the "
              f"{C.OPERATOR_EXISTING} except for the non-exclusive interconnection and "
              f"transport rights necessary for continuity under Section 6.3.")
    C.section(doc, "5.3", "Duration and Wind-Down",
              f"Emergency Step-In continues only so long as the emergency conditions "
              f"persist. On resolution, control returns to {OP} unless a Triggering "
              f"Event otherwise supports continued Step-In or transition.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Emergency step-in without cure must be reconciled with lender rights, "
                "bankruptcy automatic-stay considerations, and any Award requirements. "
                "Confirm scope and notice mechanics with counsel.")

    # ================= ARTICLE 6 — TEMPORARY OPERATION =====================
    C.article(doc, 6, "Temporary Operation During Step-In")
    C.section(doc, "6.1", "Operation by the Tribe or Designee",
              f"During a Step-In, the {TRIBE} or its designated operator may operate, "
              f"maintain, and manage the {C.TRIBAL_ASSETS} and provide Essential "
              f"Services, using the access, records, credentials, and cooperation "
              f"provided under Articles 7–14.")
    C.section(doc, "6.2", "Protection of RIVR Tech Existing Network",
              f"The Step-In is limited to the {C.TRIBAL_ASSETS}. The {TRIBE} shall not "
              f"assume ownership or control of the {C.OPERATOR_EXISTING} (RIVR Tech’s "
              f"proprietary middle-mile/backbone and core), and shall protect {OP}’s "
              f"confidential and proprietary systems, except to the limited extent of "
              f"Section 6.3.")
    C.section(doc, "6.3", "Continuity Interconnection",
              f"To the extent Essential Services depend on transport across the "
              f"{C.OPERATOR_EXISTING}, {OP} shall continue to provide, and the {TRIBE} "
              f"or its designee may use, non-exclusive interconnection and transport on "
              f"the terms then in effect (or on cost-based terms under Section 16 if "
              f"none apply) solely for continuity during Step-In. This does not grant "
              f"any ownership or long-term right in the {C.OPERATOR_EXISTING}.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                f"Confirm the commercial terms and duration of continuity "
                f"interconnection across the {C.OPERATOR_EXISTING} during Step-In "
                f"(e.g., existing wholesale rate vs. cost-based transition rate): "
                f"{C.PH('interconnection terms during step-in')}.")

    # ================= ARTICLE 7 — ACCESS TO SYSTEMS =======================
    C.article(doc, 7, "Access to Systems and Credentials")
    C.section(doc, "7.1", "Access",
              f"On Step-In or transition, {OP} shall provide the {TRIBE} or Successor "
              f"Operator prompt access to the operational, monitoring, provisioning, "
              f"and support systems necessary to operate the {C.TRIBAL_ASSETS}, and to "
              f"the physical sites, subject to safety and security controls.")
    C.section(doc, "7.2", "Network Credentials",
              f"{OP} shall deliver or reset, as appropriate, network credentials, "
              f"administrative accounts, certificates, and keys necessary to operate "
              f"the {C.TRIBAL_ASSETS}, and shall support secure re-keying so continuity "
              f"is preserved while protecting the {C.OPERATOR_EXISTING}.")
    C.section(doc, "7.3", "Security During Access",
              f"Access and credential transfer shall follow the security and "
              f"access-control requirements of Document 02.06, including least "
              f"privilege, logging, and prompt revocation of superseded credentials.")

    # ================= ARTICLE 8 — CUSTOMER CONTINUITY =====================
    C.article(doc, 8, "Customer Continuity")
    C.section(doc, "8.1", "Uninterrupted Service",
              f"The Parties shall cooperate to keep Essential Services uninterrupted "
              f"during Step-In and transition, including maintaining billing, support, "
              f"and provisioning for subscribers in the {C.SERVICE_TERRITORY}.")
    C.section(doc, "8.2", "Subscriber Communications",
              f"Subscriber communications about a transition shall be coordinated with "
              f"the {TRIBE} and shall comply with the CPNI carrier-change rules and the "
              f"privacy obligations of Document 02.06.")

    # ================= ARTICLE 9 — RECORDS =================================
    C.article(doc, 9, "Transfer of Records")
    C.section(doc, "9.1", "Operational and Grant Records",
              f"{OP} shall transfer to the {TRIBE} or Successor Operator copies of the "
              f"records necessary to operate the {C.TRIBAL_ASSETS} and to substantiate "
              f"the Award, retaining copies only as permitted, consistent with "
              f"{C.CITES['records']}.")
    C.section(doc, "9.2", "As-Builts and Documentation",
              "Transferred records shall include as-built drawings, fiber records, GIS "
              "data, splice and OTDR records, equipment inventories, configurations, "
              "warranties, permits, and maintenance histories, in usable formats.")
    C.section(doc, "9.3", "Customer Data",
              f"Customer Data shall be transferred in portable form and handled under "
              f"Articles 17–18 of Document 02.06 (return, destruction, and portability).")

    # ================= ARTICLE 10 — NUMBERS / ACCOUNTS =====================
    C.article(doc, 10, "Transfer of Telephone Numbers and Service Accounts")
    C.section(doc, "10.1", "Local Number Portability",
              f"{OP} shall cooperate to port subscriber telephone numbers to the "
              f"{TRIBE} or Successor Operator (or its underlying carrier) consistent "
              f"with FCC local-number-portability (LNP) rules, and shall not block or "
              f"delay ports.")
    C.section(doc, "10.2", "Service Accounts",
              f"{OP} shall transfer or assist in re-establishing subscriber service "
              f"accounts, including account identifiers, service configurations, and "
              f"provisioning data necessary for continuity.")

    # ================= ARTICLE 11 — VENDOR CONTRACTS =======================
    C.article(doc, 11, "Vendor Contracts")
    C.section(doc, "11.1", "Assignment / Step-In",
              f"To the extent assignable, {OP} shall, at the {TRIBE}’s election, assign "
              f"to the {TRIBE} or Successor Operator, or permit step-in to, third-party "
              f"vendor and maintenance contracts that are dedicated to or materially "
              f"necessary for operating the {C.TRIBAL_ASSETS}.")
    C.section(doc, "11.2", "Consent and Shared Contracts",
              f"For contracts requiring vendor consent or that are shared with the "
              f"{C.OPERATOR_EXISTING}, {OP} shall use commercially reasonable efforts to "
              f"obtain consent or to arrange substitute arrangements for the "
              f"{C.TRIBAL_ASSETS} portion, without impairing {OP}’s own operations.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                f"Identify which vendor and maintenance contracts are dedicated vs. "
                f"shared, and the assignment/step-in mechanics for each: "
                f"{C.PH('vendor-contract assignment schedule')}.")

    # ================= ARTICLE 12 — SOFTWARE LICENSES ======================
    C.article(doc, 12, "Software Licenses and Escrow")
    C.section(doc, "12.1", "Assignability",
              f"{OP} shall identify software and firmware licenses necessary to operate "
              f"the {C.TRIBAL_ASSETS} and, to the extent permitted, assign or sublicense "
              f"them to the {TRIBE} or Successor Operator, or facilitate replacement "
              f"licenses.")
    C.section(doc, "12.2", "Source-Code / Configuration Escrow",
              f"For custom or operations-critical software owned or controlled by {OP}, "
              f"the Parties shall consider a source-code and/or configuration escrow "
              f"with release conditions tied to the Triggering Events, so continuity is "
              f"preserved. {C.PH('confirm escrow scope, agent, and release conditions')}.")

    # ================= ARTICLE 13 — INVENTORY / SPARES / TRAINING ==========
    C.article(doc, 13, "Inventory, Spare Materials and Training")
    C.section(doc, "13.1", "Inventory and Spares",
              f"{OP} shall maintain and, on transition, transfer to the {TRIBE} or "
              f"Successor Operator the spare materials, tools, and consumables "
              f"reasonably necessary to maintain the {C.TRIBAL_ASSETS}, at "
              f"{C.PH('valuation basis, e.g., cost / book value')}.")
    C.section(doc, "13.2", "Training and Knowledge Transfer",
              f"{OP} shall provide reasonable training and knowledge transfer to the "
              f"personnel of the {TRIBE} or Successor Operator on the operation and "
              f"maintenance of the {C.TRIBAL_ASSETS} during the Transition-Assistance "
              f"Period.")

    # ================= ARTICLE 14 — SUCCESSOR COOPERATION ==================
    C.article(doc, 14, "Successor-Operator Cooperation")
    C.section(doc, "14.1", "Good-Faith Cooperation",
              f"{OP} shall cooperate in good faith with the {TRIBE} and any Successor "
              f"Operator to effect an orderly transition, including reasonable "
              f"availability of knowledgeable personnel, responses to information "
              f"requests, and joint transition planning.")
    C.section(doc, "14.2", "Transition Manager",
              f"Each Party shall designate a transition manager. "
              f"{C.PH('name/role of each Party’s transition manager')}.")

    # ================= ARTICLE 15 — TRANSITION-ASSISTANCE PERIOD ===========
    C.article(doc, 15, "Transition-Assistance Period")
    C.section(doc, "15.1", "Duration",
              f"The Transition-Assistance Period is {TA_MONTHS} months from the "
              f"commencement of transition, during which {OP} provides the assistance "
              f"described in this Plan.")
    C.section(doc, "15.2", "Extension",
              f"The {TRIBE} may extend the Transition-Assistance Period for up to "
              f"{C.PH('e.g., one or more additional 3-month periods')} on notice, where "
              f"reasonably necessary to complete transition, subject to the transition "
              f"pricing in Article 16.")
    C.section(doc, "15.3", "Standard of Performance",
              f"During the Transition-Assistance Period, {OP} shall continue to meet the "
              f"material service levels of the O&M/SLA (Document 02.03) for the "
              f"{C.TRIBAL_ASSETS} unless and until operational responsibility has "
              f"transferred.")

    # ================= ARTICLE 16 — TRANSITION PRICING =====================
    C.article(doc, 16, "Transition Pricing")
    C.section(doc, "16.1", "Cost-Based and Capped",
              f"Transition-assistance services (including Step-In support, training, "
              f"continuity interconnection, and knowledge transfer) shall be provided at "
              f"cost-based pricing, capped so as not to exceed {C.PH('cap basis, e.g., "
              "RIVR Tech’s fully-loaded cost plus a fixed percentage, not to exceed a "
              "stated ceiling')}. Emergency Step-In support during a genuine emergency "
              f"shall be provided without markup.")
    C.section(doc, "16.2", "No Windfall; No Leverage",
              f"Transition pricing shall not be used to impede transition or to extract "
              f"value disproportionate to cost. Amounts owed are subject to the final "
              f"reconciliation in Article 19.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                f"Set the cost-based transition-pricing formula and cap: "
                f"{C.PH('transition-pricing formula, cap, and emergency carve-out')}.")

    # ================= ARTICLE 17 — PROTECTION OF RIVR TECH ================
    C.article(doc, 17, "Protection of RIVR Tech-Owned Infrastructure")
    C.section(doc, "17.1", "Retained Ownership",
              f"{OP} retains ownership of the {C.OPERATOR_EXISTING} and all "
              f"{C.OPERATOR_ASSETS} that are not {C.TRIBAL_ASSETS}. Step-In and "
              f"transition extend only to the {C.TRIBAL_ASSETS} and the rights "
              f"necessary for continuity, and do not transfer, encumber, or grant any "
              f"long-term interest in the {C.OPERATOR_EXISTING}.")
    C.section(doc, "17.2", "IRU Protection",
              f"{OP}’s {C.IRU_TERM_DEFINED} and related capacity rights (recommended "
              f"term of {yrs(C.IRU_TERM_RECOMMENDED)} years) survive Step-In and "
              f"transition except to the extent terminated for uncured default under "
              f"the Master Agreement, and {OP} retains its own cure rights before any "
              f"termination of the {C.IRU_TERM_DEFINED}.")
    C.section(doc, "17.3", "RIVR Tech Cure Rights",
              f"Nothing in this Plan deprives {OP} of the notice-and-cure rights in "
              f"Article 4. Termination of {OP}’s core rights requires exhaustion of the "
              f"applicable cure period, except in the emergency circumstances of "
              f"Article 5 (which are temporary and continuity-limited).")
    C.section(doc, "17.4", "Lender Protection",
              f"A Lender shall be entitled to (a) notice of a Triggering Event and a "
              f"reasonable opportunity to cure on {OP}’s behalf; (b) the right to step "
              f"into or assign {OP}’s financed rights to a qualified transferee, subject "
              f"to the {TRIBE}’s reasonable consent and the Award; and (c) recognition "
              f"of its security interest in {OP}-owned assets — provided that no Lender "
              f"right may encumber the {C.TRIBAL_ASSETS} contrary to Article 18. "
              f"{C.PH('confirm lender-protection / consent-to-assignment terms')}.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Lender-protection, IRU-survival, and cure-on-behalf provisions must be "
                "reconciled with the Award’s restrictions on the Tribal Assets and with "
                "any financing documents. Do not finalize without finance counsel.")

    # ================= ARTICLE 18 — PROTECTION OF TRIBAL ASSETS ============
    C.article(doc, 18, "Protection of Tribal Assets")
    C.section(doc, "18.1", "Tribal Ownership Preserved",
              f"The {C.TRIBAL_ASSETS} are and remain the property of the {TRIBE}. "
              f"Neither Step-In, transition, nor any Lender or successor arrangement may "
              f"transfer title to, or grant a security interest in, the {C.TRIBAL_ASSETS} "
              f"except as permitted by the Award and applicable federal law.")
    C.section(doc, "18.2", "No Encumbrance Contrary to 2 CFR 200.311",
              f"No Successor Operator, Lender, or other party may use, encumber, or "
              f"dispose of the {C.TRIBAL_ASSETS} contrary to {C.CITES['real_property']} "
              f"(and, for equipment and intangible property, {C.CITES['equipment']} and "
              f"{C.CITES['intangible']}). Any disposition requires compliance with the "
              f"Award’s disposition and Federal-Interest provisions.")
    C.section(doc, "18.3", "Continuing Federal Interest",
              f"The {C.FEDERAL_INTEREST} continues through Step-In and transition. The "
              f"Parties shall take no action that would impair the {C.FEDERAL_INTEREST} "
              f"or the {TRIBE}’s ability to satisfy Award and closeout obligations "
              f"({C.CITES['closeout']}).")

    # ================= ARTICLE 19 — FINAL RECONCILIATION ===================
    C.article(doc, 19, "Final Reconciliation")
    C.section(doc, "19.1", "Financial True-Up",
              f"On completion of transition, the Parties shall perform a financial "
              f"true-up covering amounts owed for transition assistance (Article 16), "
              f"any accrued but unpaid operating or revenue-share amounts under the "
              f"Master Agreement, and any offsets or credits.")
    C.section(doc, "19.2", "Deposits, Reserves and Escrows",
              f"Any deposits, reserves, maintenance escrows, or holdbacks shall be "
              f"reconciled and the balance returned to the entitled Party, net of "
              f"documented obligations.")
    C.section(doc, "19.3", "Program-Income Accounting",
              f"The Parties shall account for {C.PROGRAM_INCOME} through the transition "
              f"date consistent with {C.CITES['prog_income']}, and shall document the "
              f"treatment of any {C.PROGRAM_INCOME} earned during Step-In or the "
              f"Transition-Assistance Period.")
    C.section(doc, "19.4", "Records and Closeout",
              f"Final-reconciliation records shall be retained under {C.CITES['records']} "
              f"and shall support Award closeout and any post-closeout adjustments "
              f"({C.CITES['closeout']}).")
    C.flag_para(doc, C.FLAG_GRANT,
                f"Program-income and disposition accounting on transition are grant-"
                f"compliance sensitive. Confirm treatment with grant counsel / the "
                f"{TRIBE}’s finance team and, where required, {C.AGENCY_SHORT}.")

    # ================= STEP-IN TRIGGER -> ACTION TABLE =====================
    C.article(doc, 20, "Step-In Trigger → Action Matrix")
    C.para(doc, "The following matrix summarizes the relationship between Triggering "
                "Events and available actions. It is a summary only; the operative "
                "terms are in Articles 2–19.", italic=True)
    C.add_table(
        doc,
        ["Triggering Event", "Cure Available?", "Primary Action", "Asset Scope / Safeguard"],
        [
            ["Uncured monetary default",
             f"Yes — {CURE_M} days", "Suspension of payments; potential transition",
             "Tribal Assets; RIVR IRU cure rights (17.3)"],
            ["Uncured non-monetary default",
             f"Yes — {CURE_NM} days (+ ext.)", "Step-In or transition after cure lapses",
             "Tribal Assets only; Existing Network protected (6.2)"],
            ["Insolvency / bankruptcy",
             "Limited (per law)", "Step-In to preserve continuity; assess assumption",
             "Subject to automatic stay; lender notice (17.4)"],
            ["Abandonment",
             "Case-by-case", "Emergency Step-In (Art. 5)",
             "Continuity interconnection (6.3)"],
            ["Loss of authorizations",
             "Often no", "Step-In / expedited transition",
             "Preserve Federal Interest (18.3)"],
            ["Chronic SLA failure",
             f"Yes — {CURE_NM} days", "Cure plan; transition if chronic",
             "Per O&M/SLA 02.03 thresholds"],
            ["Grant-compliance failure",
             "If curable", "Immediate coordination; Step-In if Award threatened",
             "200.113 disclosure; NTIA notice (3.2)"],
            ["Change in control w/o consent",
             "Cure = unwind/obtain consent", "Consent or transition",
             "No encumbrance of Tribal Assets (18.2)"],
            ["Emergency (safety/continuity/Award)",
             "No — immediate", f"Emergency Step-In ({STEPIN.split(',')[0]})",
             "Temporary; Tribal Assets only (5.2)"],
        ],
        widths=[1.9, 1.5, 2.1, 2.0],
        col_align=["l", "c", "l", "l"],
    )

    # ================= TRANSITION CHECKLIST TABLE ==========================
    C.article(doc, 21, "Transition Checklist")
    C.para(doc, "The following checklist operationalizes the transition. Owners and "
                "target timeframes are working defaults to be confirmed.", italic=True)
    C.add_table(
        doc,
        ["#", "Transition Task", "Owner", "Target Timeframe", "Cross-Reference"],
        [
            ["1", "Issue notice / declare Triggering Event", TRIBE,
             "Day 0", "Art. 3"],
            ["2", "Cure period runs (if applicable)", OP,
             f"{CURE_M}/{CURE_NM} days", "Art. 4"],
            ["3", "Emergency Step-In (if needed)", f"{TRIBE}/designee",
             "Immediate", "Art. 5"],
            ["4", "Transfer credentials & system access", OP,
             C.PH("e.g., ≤ 5 business days"), "Art. 7"],
            ["5", "Confirm customer continuity & billing", "Both",
             "Continuous", "Art. 8"],
            ["6", "Transfer operational & grant records", OP,
             C.PH("e.g., ≤ 15 days"), "Art. 9; " + C.CITES['records']],
            ["7", "Port numbers / transfer accounts", OP,
             "Per LNP rules", "Art. 10"],
            ["8", "Assign / step into vendor contracts", OP,
             C.PH("e.g., ≤ 30 days"), "Art. 11"],
            ["9", "Assign / replace software; escrow release", OP,
             C.PH("e.g., ≤ 30 days"), "Art. 12"],
            ["10", "Transfer inventory, spares; train staff", OP,
             "During TA period", "Art. 13"],
            ["11", "Transfer / destroy Customer Data", OP,
             "Per 02.06 Arts. 17–18", "Doc 02.06"],
            ["12", "Complete Transition-Assistance Period", "Both",
             f"{TA_MONTHS} months (extendable)", "Art. 15"],
            ["13", "Final reconciliation & program-income accounting", "Both",
             C.PH("e.g., ≤ 60 days after cutover"), "Art. 19"],
            ["14", "Confirm Tribal Asset title & Federal Interest intact", TRIBE,
             "Before closeout", "Art. 18; " + C.CITES['closeout']],
        ],
        widths=[0.4, 2.5, 1.0, 1.6, 1.8],
        col_align=["c", "l", "c", "c", "l"],
    )

    # ================= ARTICLE 22 — GENERAL ================================
    C.article(doc, 22, "General Provisions")
    C.section(doc, "22.1", "Governing Law")
    C.para(doc, f"The governing law of this Plan is not finalized. The Parties will "
                f"select from: (a) the law of the {C.STATE} (excluding conflicts "
                f"principles); (b) the law of the {C.STATE} for commercial matters with "
                f"the law and jurisdiction of the {C.TRIBE_FULL} governing questions of "
                f"Tribal sovereignty and conduct within the {C.SERVICE_TERRITORY}; or "
                f"(c) federal law where it controls the Award. "
                f"{C.PH('selected governing-law alternative')}.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Governing law, dispute resolution, and any limited waiver of sovereign "
                "immunity must not be selected silently. Reconcile with the Master "
                "Agreement and confirm with counsel for the Tribe.")
    C.section(doc, "22.2", "Sovereign Immunity",
              f"Nothing in this Plan waives the sovereign immunity of the "
              f"{C.TRIBE_FULL}. Any limited waiver must be express, written, specific as "
              f"to claims and remedies, and authorized under Tribal law. "
              f"{C.PH('cross-reference Master Agreement sovereign-immunity section')}.")
    C.section(doc, "22.3", "Order of Precedence",
              f"In the event of a conflict, the order of precedence is: (a) the Award "
              f"terms and applicable federal law; (b) the Master Agreement (Document "
              f"02.01); (c) this Plan (Document 02.07) on matters of transition, "
              f"step-in, and successor operation; and (d) the O&M/SLA (Document 02.03).")
    C.section(doc, "22.4", "Survival",
              "Provisions relating to asset protection, Federal Interest, records "
              "retention, final reconciliation, and confidentiality survive completion "
              "of transition for the periods required by law and the Award.")
    C.section(doc, "22.5", "Amendment",
              "This Plan may be amended only by a writing signed by both Parties, "
              "subject to any Award-required approvals.")

    C.signature_block(
        doc,
        extra_note="Confirm signatory authority, lender-protection terms, sovereign-"
        "immunity/governing-law selections, and program-income accounting before "
        "execution.",
    )

    path = C.save(doc, "02_Core_Agreements",
                  "07_Transition_Step_In_and_Successor_Operator_Plan.docx")
    return path


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    p6 = build_privacy_addendum()
    p7 = build_transition_plan()
    print("GENERATED:")
    print("  DOC 6 ->", p6)
    print("  DOC 7 ->", p7)
