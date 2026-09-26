"""
gen_om_retail.py — Generator for two coordinated TBCP Definitive Agreements:

  DOC 1  02_Definitive_Agreements/05_Network_Operations_Maintenance_and_Lifecycle_Agreement.docx
  DOC 2  02_Definitive_Agreements/06_Retail_Billing_and_Subscriber_Revenue_Agreement.docx

Both agreements are part of the Lumbee Tribe of North Carolina / RIVR Tech
coordinated TBCP fiber package. All party names, defined terms, SLA values,
citations, precedence rules, and payment mechanics come from the canonical
engine Scripts/common.py — nothing is invented here.

Run:  python3 gen_om_retail.py
"""

from __future__ import annotations

import sys
sys.path.insert(0, '/home/user/claude-skills/Lumbee_RIVR_TBCP_Agreement_Package/Scripts')
import common as C


# ---------------------------------------------------------------------------
# Shared building blocks reused by both agreements
# ---------------------------------------------------------------------------

def intro_recital(doc, agreement_name):
    """Opening execution sentence + package context recitals."""
    C.status_banner(doc)
    C.spacer(doc, 1)
    p = doc.add_paragraph()
    p.add_run(
        f"This {agreement_name} (this “Agreement”) is entered into as of "
        f"{C.PH('Effective Date')} (the “Effective Date”), by and between "
        f"{C.TRIBE_FULL} (the “{C.TRIBE_SHORT}”), acting directly or through "
        f"{C.TRIBE_ENTITY_ALT}, and {C.OPERATOR_FULL} (“{C.OPERATOR_SHORT}”). "
        f"The {C.TRIBE_SHORT} and {C.OPERATOR_SHORT} are each a “{C.PARTY_SINGULAR}” "
        f"and together the “{C.PARTIES_COLLECTIVE}.”"
    )
    C.spacer(doc, 1)
    C.para(doc, "RECITALS", bold=True)
    C.para(doc,
        f"A.  The {C.TRIBE_SHORT} is the recipient and steward of an award (or proposed award) "
        f"under the {C.PROGRAM_FULL} ({C.PROGRAM_SHORT}) administered by the {C.AGENCY_FULL} "
        f"({C.AGENCY_SHORT}), {C.DOC_FULL}, and owns the {C.GRANT_FUNDED} funded thereunder, which "
        f"comprise the {C.NETWORK} serving the {C.SERVICE_TERRITORY} in {C.GEOGRAPHY}.")
    C.para(doc,
        f"B.  {C.OPERATOR_SHORT} is the {C.TRIBE_SHORT}'s designated operator and, subject to "
        f"{C.AGENCY_SHORT}/{C.DOC_FULL} Award approval, the proposed retail provider of record for "
        f"the {C.NETWORK}. {C.OPERATOR_SHORT} owns and separately maintains the {C.OPERATOR_EXISTING} "
        f"and its billing, provisioning, and support systems, which remain {C.OPERATOR_SHORT}'s "
        f"property and are never contributed to the {C.TRIBE_SHORT} or made available without "
        f"separately agreed, Award-permitted consideration.")
    C.para(doc,
        f"C.  {C.LREMC_FULL} (“{C.LREMC_SHORT}”) is a separate owner of certain "
        f"{C.LREMC_ASSETS} used in connection with the {C.NETWORK}; those assets are addressed only "
        f"under a separate owner-approved instrument or joinder and are not covered by this Agreement.")
    C.para(doc,
        f"D.  This Agreement is one of several coordinated Definitive Agreements executed under the "
        f"{C.AGREEMENTS['master']} and must be read together with, and subject to, the executed Award. "
        f"{C.FLAG_GRANT}  No controlling {C.PROGRAM_SHORT} award or source documents were supplied; "
        f"the provisional baseline is the {C.NOFO_NAME}. {C.NOFO_LIVE_NOTE}")
    C.spacer(doc, 1)
    C.para(doc,
        "NOW, THEREFORE, in consideration of the mutual covenants below and other good and valuable "
        "consideration, the receipt and sufficiency of which are acknowledged, the Parties agree as follows:")
    C.spacer(doc, 1)


def art_definitions(doc, art_no, local_terms):
    """Definitions article: shared-definitions rule + a short local glossary."""
    C.article(doc, art_no, "Definitions, Interpretation, and Shared Definitions")
    C.section(doc, f"{art_no}.1", "Shared Definitions Source", C.SHARED_DEFINITIONS_RULE)
    C.section(doc, f"{art_no}.2", "Local Defined Terms",
        "In addition to the shared definitions, the following terms have the meanings given below "
        "when used in this Agreement:")
    for term, meaning in local_terms:
        C.subsection(doc, term, meaning)
    C.section(doc, f"{art_no}.3", "Interpretation",
        "Headings are for convenience only. “Including” means “including without "
        "limitation.” References to statutes, regulations, and the Award include successor and "
        "amended versions applicable to the controlling Award. Time periods stated in Business Days "
        "exclude weekends and federal and Tribal holidays.")
    return art_no + 1


def art_precedence(doc, art_no):
    C.article(doc, art_no, "Order of Precedence")
    C.section(doc, f"{art_no}.1", "Controlling Order",
        "In the event of any conflict or inconsistency, the following instruments control in "
        "descending order of precedence:")
    for i, item in enumerate(C.PRECEDENCE, start=1):
        C.numbered(doc, item)
    C.section(doc, f"{art_no}.2", "Precedence Rule", C.PRECEDENCE_RULE)
    C.flag_para(doc, C.FLAG_GRANT,
        "Nothing in this Agreement may be performed in a manner inconsistent with the Award, 2 CFR "
        "Part 200, or applicable NTIA/DOC award terms; conflicting commercial terms yield to the "
        "higher-ranked instrument.")
    return art_no + 1


def closing_disclaimer(doc):
    C.spacer(doc, 1)
    p = doc.add_paragraph()
    r = p.add_run("DISCLAIMER.  ")
    r.bold = True
    r.font.color.rgb = C.RED
    r2 = p.add_run(
        f"{C.DRAFT_STATUS}  This is a working draft prepared for discussion and negotiation only. "
        f"It is not executed, is not legal, tax, accounting, or grant-compliance advice, and does not "
        f"create any binding obligation. All bracketed placeholders, alternatives, prices, routes, "
        f"approvals, and characterizations are provisional and must be confirmed against the executed "
        f"Award and reviewed by qualified counsel and grant, financial, and technical advisors before "
        f"any reliance. {C.FLAG_ATTORNEY}  {C.FLAG_GRANT}")
    r2.italic = True


def gov_law_article(doc, art_no):
    """Governing law + sovereign immunity as bracketed attorney-review ALTERNATIVES."""
    C.article(doc, art_no, "Governing Law, Dispute Resolution, and Sovereign Immunity")
    C.section(doc, f"{art_no}.1", "Governing Law — ALTERNATIVES",
        "The Parties must select one governing-law framework. The following are presented as bracketed "
        "alternatives for counsel to resolve:")
    C.subsection(doc, "Alt. 1", f"[The laws of the State of {C.STATE}, without regard to its "
        "conflict-of-laws rules], to the extent not preempted by federal law or Tribal law.")
    C.subsection(doc, "Alt. 2", "[The laws of the Lumbee Tribe, with federal law governing all "
        "Award-related matters], and Tribal forum as the primary venue.")
    C.subsection(doc, "Alt. 3", "[A hybrid: federal law and the Award govern grant-compliance matters; "
        f"{C.STATE} law governs ordinary commercial matters not preempted].")
    C.flag_para(doc, C.FLAG_ATTORNEY,
        "Governing law, venue, and choice-of-forum are bracketed alternatives requiring counsel "
        "selection; do not finalize without Tribal and outside counsel review.")
    C.section(doc, f"{art_no}.2", "Sovereign Immunity — ALTERNATIVES",
        f"The {C.TRIBE_SHORT} is a sovereign and retains its sovereign immunity except to the extent, "
        f"if any, of an express, written, and limited waiver duly authorized by the governing Tribal "
        f"body. Any waiver must be clear and unequivocal. The following are bracketed alternatives:")
    C.subsection(doc, "Alt. A", "[No waiver of sovereign immunity; disputes resolved solely through "
        "non-binding processes and Award remedies].")
    C.subsection(doc, "Alt. B", "[Limited, express waiver solely for the purpose of enforcing this "
        "Agreement, capped in amount and scope, and limited to a designated forum].")
    C.subsection(doc, "Alt. C", "[Limited waiver limited to specified equitable remedies (e.g., step-in "
        "and transition) and excluding money damages].")
    C.flag_para(doc, C.FLAG_ATTORNEY,
        "A clear express waiver is required for any enforceable relief against the Tribe per "
        f"{C.CITES['sovereign_immunity']}. Scope, cap, forum, and authorizing resolution are "
        "attorney-review items and must not be assumed.")
    C.section(doc, f"{art_no}.3", "Dispute Escalation",
        "The Parties will attempt good-faith resolution through designated senior representatives before "
        "pursuing any authorized remedy, without waiving Award remedies or the emergency step-in rights "
        f"cross-referenced to the {C.AGREEMENTS['transition']}.")
    return art_no + 1


# ===========================================================================
#  DOC 1 — NETWORK OPERATIONS, MAINTENANCE, AND LIFECYCLE AGREEMENT
# ===========================================================================

def build_om():
    sla = C.DEAL["sla"]
    doc = C.new_doc()
    title = C.AGREEMENTS["om"]
    C.add_cover(doc, "DEFINITIVE AGREEMENT 05", title,
                f"{C.TRIBE_SHORT} • {C.OPERATOR_SHORT} • {C.PROGRAM_SHORT} Fiber Package")
    C.setup_header_footer(doc, "05 — O&M and Lifecycle Agreement")
    C.add_toc(doc)
    intro_recital(doc, title)

    a = 1
    a = art_definitions(doc, a, [
        ("NOC", "the network operations center providing continuous monitoring, alarm management, "
                "trouble-ticketing, and dispatch coordination for the " + C.NETWORK + "."),
        ("Fault Severity", "the priority classification (P1–P4) assigned to an event under the "
                "Severity Matrix in this Agreement."),
        ("Restoration", "the point at which affected retail broadband service is measurably restored to "
                "the applicable performance targets, distinct from permanent repair."),
        ("Replacement Reserve", "the funded reserve established and maintained for capital refresh, "
                "obsolescence, and end-of-life replacement of the " + C.GRANT_FUNDED + "."),
        ("Extraordinary Work", "work outside routine and preventive operations and maintenance, "
                "including force-majeure restoration, third-party damage repair, and Tribe-directed changes."),
    ])
    a = art_precedence(doc, a)

    # Scope & roles
    C.article(doc, a, "Scope of Services, Roles, and Responsibilities")
    C.section(doc, f"{a}.1", "Operator Responsibility",
        f"{C.OPERATOR_SHORT} is responsible for the day-to-day operation, monitoring, maintenance, "
        f"repair, and lifecycle management of the {C.GRANT_FUNDED} comprising the {C.NETWORK}, all in "
        f"accordance with the Award, this Agreement, and {C.SCHEDULES['S6']}.")
    C.section(doc, f"{a}.2", "Tribe Oversight",
        f"The {C.TRIBE_SHORT} retains ownership of the {C.GRANT_FUNDED}, oversight of Award compliance, "
        f"and the review, audit, annual-review, and step-in rights set out in this Agreement.")
    C.section(doc, f"{a}.3", "Standard of Care",
        "Services must meet or exceed prudent-industry telecommunications standards, manufacturer "
        "specifications, applicable law, and the service levels in this Agreement.")
    C.section(doc, f"{a}.4", "Boundary of Assets",
        f"This Agreement governs the {C.GRANT_FUNDED} only. The {C.OPERATOR_EXISTING} and {C.LREMC_ASSETS} "
        f"are governed by their respective instruments; use of either for the project is never presumed "
        f"free and requires separately agreed, Award-permitted terms.")
    a += 1

    # Monitoring & NOC
    C.article(doc, a, "Network Monitoring and NOC")
    C.section(doc, f"{a}.1", "24x7x365 NOC",
        f"{C.OPERATOR_SHORT} will operate, or cause to be operated, a NOC providing monitoring and "
        f"first response {sla['noc']}.")
    C.section(doc, f"{a}.2", "Continuous Monitoring",
        "The NOC will continuously monitor availability, utilization, optical and transport health, "
        "power and environmental alarms, and security events, and will generate and track trouble "
        "tickets for all qualifying events.")
    C.section(doc, f"{a}.3", "Performance Targets",
        f"Steady-state network performance targets are: availability {sla['availability_target']}; "
        f"round-trip latency ≤ {sla['latency_ms']} ms; packet loss ≤ {sla['packet_loss']}; "
        f"jitter ≤ {sla['jitter_ms']} ms, measured as set out in {C.SCHEDULES['S6']}.")
    a += 1

    # Preventive maintenance
    C.article(doc, a, "Preventive and Scheduled Maintenance")
    C.section(doc, f"{a}.1", "Preventive Maintenance Program",
        "Operator will maintain a documented preventive-maintenance program covering fiber plant, "
        "electronics, power systems, batteries/generators, HVAC, and physical sites, on a schedule "
        f"no less protective than manufacturer requirements and {C.SCHEDULES['S6']}.")
    C.section(doc, f"{a}.2", "Inspections and Testing",
        "Program includes periodic optical testing consistent with the acceptance standards, battery "
        "and generator load testing, and site and enclosure inspections, with records retained and "
        "made available to the Tribe.")
    a += 1

    # Locates
    C.article(doc, a, "Locates and Underground Damage Prevention")
    C.section(doc, f"{a}.1", "NC 811 Locates",
        f"Operator is responsible for timely and accurate positive-response locates and marking of "
        f"buried {C.GRANT_FUNDED} in accordance with North Carolina 811 requirements and "
        f"{C.CITES['nc_dig']}.")
    C.section(doc, f"{a}.2", "Membership and Records",
        "Operator will maintain 811 one-call center membership as required, respond within statutory "
        "timeframes, and retain locate tickets and positive-response records for audit.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
        "Confirm allocation of locate liability and any indemnity for mislocates; coordinate with the "
        "land/ROW instruments and any pole/attachment terms.")
    a += 1

    # Repair, dispatch, escalation, restoration + SEVERITY MATRIX
    C.article(doc, a, "Fault Severity, Repair, Dispatch, Escalation, and Restoration")
    C.section(doc, f"{a}.1", "Severity Classification",
        "Each event is classified P1 (critical) through P4 (low) per the Severity Matrix below. "
        "Response is measured to acknowledgement; dispatch to field mobilization; restoration to "
        "measurable service recovery.")
    C.para(doc, "Severity Matrix (P1–P4):", bold=True)
    C.add_table(doc,
        ["Severity", "Definition / Examples", "Response (Acknowledge)", "Dispatch", "Restoration Target"],
        [
            ["P1 — Critical",
             "Total outage of a segment/site; loss of core transport; life-safety or public-safety impact",
             f"{sla['P1_response_min']} minutes", f"{sla['P1_dispatch_hr']} hours", f"{sla['P1_restore_hr']} hours"],
            ["P2 — Major",
             "Partial outage; significant degradation; redundancy lost but service continuing",
             f"{sla['P2_response_min']} minutes", f"{sla['P2_dispatch_hr']} hours", f"{sla['P2_restore_hr']} hours"],
            ["P3 — Minor",
             "Localized degradation; single-subscriber or non-service-affecting fault",
             f"{sla['P3_response_hr']} hours", f"{sla['P3_dispatch_hr']} hours", f"{sla['P3_restore_days']} days"],
            ["P4 — Low",
             "Cosmetic, informational, or scheduled-work items; no service impact",
             f"{sla['P4_response_hr']} hours", "As scheduled", f"{sla['P4_restore_days']} days"],
        ],
        widths=[1.1, 2.5, 1.2, 0.9, 1.1], col_align=[None, None, "c", "c", "c"])
    C.section(doc, f"{a}.2", "Routine and Emergency Repair",
        "Operator will perform routine repair within the applicable severity targets and emergency "
        "repair immediately where continuity of Essential Services or public safety is threatened.")
    C.section(doc, f"{a}.3", "Dispatch",
        "Operator will maintain dispatch capability sufficient to meet the dispatch targets above, "
        "including after-hours and holiday coverage.")
    C.section(doc, f"{a}.4", "Escalation",
        "Unresolved events escalate on a documented time-based ladder (technician → supervisor "
        "→ manager → executive sponsor → Tribe notification), with escalation contacts "
        f"and thresholds maintained in {C.SCHEDULES['S6']}.")
    a += 1

    # Outages, trouble tickets, metrics
    C.article(doc, a, "Outage Definitions, Trouble Tickets, and Performance Metrics")
    C.section(doc, f"{a}.1", "Outage Definition",
        "An “Outage” is a loss of, or degradation below the performance targets for, retail "
        "broadband service at one or more locations, measured from NOC detection or first valid report "
        "to Restoration, excluding approved planned-maintenance windows and customer-caused events.")
    C.section(doc, f"{a}.2", "Trouble-Ticket Metrics",
        "Operator will track and report per event: detection source and time, severity, response, "
        "dispatch, restoration, permanent-repair time, root cause, and affected locations; and monthly "
        "aggregates including MTTR by severity, ticket volumes, and repeat-fault counts.")
    a += 1

    # Planned maintenance windows
    C.article(doc, a, "Planned Maintenance Windows")
    C.section(doc, f"{a}.1", "Standard Windows",
        f"Planned maintenance is performed within pre-agreed maintenance windows "
        f"{C.PH('e.g., low-traffic overnight window(s) per week')}, with advance notice per "
        f"{C.SCHEDULES['S6']}; emergency maintenance may occur outside windows with prompt notice.")
    C.section(doc, f"{a}.2", "Customer Notice Coordination",
        f"Planned-work notices affecting customers are coordinated with the retail provider of record "
        f"under the {C.AGREEMENTS['retail']}.")
    a += 1

    # Spares + vendor management + storm
    C.article(doc, a, "Spare Inventory, Vendor Management, and Storm Response")
    C.section(doc, f"{a}.1", "Spare Parts Inventory",
        f"Operator will maintain a critical-spares inventory sufficient to meet restoration targets, "
        f"tracked and reported in {C.SCHEDULES['S6']}, with minimum stocking levels for long-lead items.")
    C.section(doc, f"{a}.2", "Vendor Management",
        "Operator will manage subcontractors and vendors under flow-down of Award and this Agreement's "
        "requirements, maintaining qualified vendors for splicing, construction, and electronics support.")
    C.section(doc, f"{a}.3", "Storm and Emergency Response",
        f"Operator will maintain a storm/emergency response plan addressing pre-event readiness, mutual "
        f"aid, prioritized restoration of Essential Services, and coordination with {C.LREMC_SHORT} for "
        f"power and shared facilities, consistent with {C.GEOGRAPHY} hurricane exposure.")
    C.flag_para(doc, C.FLAG_TECH,
        "Confirm critical-spares list, stocking levels, and long-lead items against the approved bill of "
        "materials and equipment schedule.")
    a += 1

    # Firmware/software + cybersecurity
    C.article(doc, a, "Firmware, Software, and Cybersecurity Coordination")
    C.section(doc, f"{a}.1", "Firmware/Software Management",
        "Operator will manage firmware and software versions, security patches, configuration baselines, "
        "and change control, testing changes before deployment where practicable and maintaining "
        "rollback capability.")
    C.section(doc, f"{a}.2", "Cybersecurity Coordination",
        f"Cybersecurity monitoring, incident response, supply-chain risk, and covered-equipment "
        f"prohibitions are coordinated under the {C.AGREEMENTS['privacy']} and {C.SCHEDULES['S11']}; in "
        f"any conflict that Addendum controls security matters. {C.FLAG_GRANT}  Covered "
        f"telecommunications equipment is prohibited per {C.CITES['telecom_ban']}.")
    a += 1

    # Performance reporting + service credits + SERVICE CREDIT TABLE
    C.article(doc, a, "Performance Reporting and Service Credits")
    C.section(doc, f"{a}.1", "Monthly Performance Reporting",
        f"Operator will deliver a monthly performance report (cross-reference: 04 Operational Forms — "
        f"Monthly Performance Report and {C.SCHEDULES['S6']}) covering availability, latency, loss, jitter, "
        f"severity-based response/dispatch/restoration attainment, ticket metrics, and open items.")
    C.section(doc, f"{a}.2", "Service Credits",
        f"Where Operator fails to meet a committed service level, service credits apply as set out below "
        f"and in {C.SCHEDULES['S6']}. Service credits are the agreed monetary adjustment for the measured "
        f"miss and do not limit step-in or persistent-failure remedies. {C.FLAG_BUSINESS}  Credit amounts, "
        f"caps, and whether credits offset operating payments or the per-subscriber payment are business "
        f"decisions to be confirmed.")
    C.para(doc, "Service-Credit Schedule:", bold=True)
    C.add_table(doc,
        ["Service Level", "Committed Target", "Measurement Period", "Miss Threshold", "Service Credit"],
        [
            ["Availability", sla["availability_target"], "Monthly",
             f"Below {sla['availability_target']}", C.PH("credit % of monthly amount / step schedule")],
            ["P1 Restoration", f"{sla['P1_restore_hr']} hours", "Per event / monthly",
             "Target missed", C.PH("per-event credit")],
            ["P2 Restoration", f"{sla['P2_restore_hr']} hours", "Per event / monthly",
             "Target missed", C.PH("per-event credit")],
            ["Latency / Loss / Jitter",
             f"≤{sla['latency_ms']}ms / ≤{sla['packet_loss']} / ≤{sla['jitter_ms']}ms",
             "Monthly", "Sustained breach", C.PH("credit % of monthly amount")],
            ["Chronic / Repeat Fault", "No repeat P1/P2 at same location within [30] days", "Rolling",
             "Repeat within window", C.PH("escalated credit + remediation plan")],
        ],
        widths=[1.4, 1.5, 1.1, 1.2, 1.3])
    a += 1

    # Extraordinary work
    C.article(doc, a, "Extraordinary Work")
    C.section(doc, f"{a}.1", "Scope and Authorization",
        "Extraordinary Work is outside routine/preventive O&M and requires prior written authorization "
        "and an agreed change order specifying scope, price basis, and Award-cost eligibility.")
    C.section(doc, f"{a}.2", "Pricing Basis",
        f"Extraordinary Work is priced on {C.PH('agreed rate card / time-and-materials / lump sum')} "
        f"basis, subject to {C.CITES['allowable']} where costs are charged to the Award. {C.FLAG_BUSINESS}")
    a += 1

    # Operating budget + capital refresh + replacement reserve + EOL
    C.article(doc, a, "Operating Budget, Capital Refresh, Replacement Reserve, and End-of-Life")
    C.section(doc, f"{a}.1", "Annual Operating Budget",
        f"The Parties will agree an annual operating budget for the {C.NETWORK} covering monitoring, "
        f"maintenance, spares, and support, reconciled annually. {C.FLAG_BUSINESS}")
    C.section(doc, f"{a}.2", "Capital Refresh and Obsolescence",
        "Operator will maintain a rolling multi-year capital-refresh and obsolescence plan identifying "
        "electronics and systems approaching end-of-support, with recommended replacement timing.")
    C.section(doc, f"{a}.3", "Replacement Reserve",
        f"A Replacement Reserve will be established and funded to support capital refresh and end-of-life "
        f"replacement of the {C.GRANT_FUNDED}. {C.FLAG_BUSINESS}  Funding source, contribution amount, "
        f"custody, and permitted uses are to be confirmed. {C.FLAG_GRANT}  Reserve funding and use must "
        f"be consistent with the Award, allowable-cost rules ({C.CITES['allowable']}), and any "
        f"program-income treatment ({C.CITES['prog_income']}).")
    C.section(doc, f"{a}.4", "End-of-Life Planning",
        "Operator will provide end-of-life planning for major assets, including migration and "
        "decommissioning recommendations, to preserve continuity and protect the Federal Interest.")
    a += 1

    # Insurance
    C.article(doc, a, "Insurance")
    ins = C.DEAL["insurance"]
    C.section(doc, f"{a}.1", "Required Coverages",
        f"Operator will maintain, at minimum: commercial general liability {ins['cgl_occurrence']} per "
        f"occurrence / {ins['cgl_aggregate']} aggregate; automobile liability {ins['auto']}; umbrella/"
        f"excess {ins['umbrella']}; workers' compensation at {ins['workers_comp']} with employers' "
        f"liability {ins['employers_liability']}; professional/technology E&O {ins['professional_tech_eo']}; "
        f"cyber {ins['cyber']}; and property/builders' risk at {ins['property_builders_risk']}, all "
        f"consistent with {C.SCHEDULES['S12']} and {C.CITES['insurance']}.")
    C.section(doc, f"{a}.2", "Endorsements",
        f"Policies will name the {C.TRIBE_SHORT} as additional insured as its interests appear, provide "
        f"waivers of subrogation where available, and require notice of cancellation.")
    C.flag_para(doc, C.FLAG_ATTORNEY, "Confirm limits, additional-insured status, and coordination with "
        "indemnity and any lender/landowner insurance requirements.")
    a += 1

    # Annual review + audit rights
    C.article(doc, a, "Annual Review and Audit Rights")
    C.section(doc, f"{a}.1", "Annual Review",
        "The Parties will conduct an annual operational review of performance, budget, spares, refresh, "
        "and reserve adequacy, documenting agreed corrective actions.")
    C.section(doc, f"{a}.2", "Audit Rights",
        f"The {C.TRIBE_SHORT}, {C.AGENCY_SHORT}/{C.DOC_FULL}, and their authorized representatives may "
        f"audit Operator's records relating to the {C.GRANT_FUNDED} and Award-charged costs on "
        f"{C.DEAL['audit_notice_business_days']} Business Days' notice, with records retained for "
        f"{C.DEAL['records_retention_years']} years per {C.CITES['records']}.")
    a += 1

    # Persistent-failure remedies / step-in
    C.article(doc, a, "Persistent-Failure Remedies and Step-In")
    C.section(doc, f"{a}.1", "Cure",
        f"Monetary defaults have a {C.DEAL['cure_monetary_days']}-day cure period; non-monetary defaults "
        f"have a {C.DEAL['cure_nonmonetary_days']}-day cure period, with {C.DEAL['cure_nonmonetary_extension']}.")
    C.section(doc, f"{a}.2", "Persistent Failure",
        "Repeated or chronic failure to meet critical service levels, uncured after notice, is a "
        "persistent failure entitling the Tribe to escalated remedies, including remediation plans, "
        "increased credits, and step-in.")
    C.section(doc, f"{a}.3", "Step-In",
        f"Emergency step-in is available {C.DEAL['stepin_emergency']}. Step-in, continuity, termination "
        f"assistance, and transition are governed by the {C.AGREEMENTS['transition']}, which controls "
        f"those procedures; transition assistance continues for up to "
        f"{C.DEAL['transition_assistance_months']} months.")
    a += 1

    a = gov_law_article(doc, a)

    closing_disclaimer(doc)
    C.signature_block(doc,
        extra_note="Confirm signatory authority, authorizing Tribal resolution, and Award-approval "
                   "prerequisites before execution.")
    return C.save(doc, "02_Definitive_Agreements",
                  "05_Network_Operations_Maintenance_and_Lifecycle_Agreement.docx")


# ===========================================================================
#  DOC 2 — RETAIL, BILLING, AND SUBSCRIBER-REVENUE AGREEMENT
# ===========================================================================

def active_subscriber_definition_para(doc, sec_prefix):
    """Precise Active Subscriber definition assembled from canonical elements."""
    C.section(doc, f"{sec_prefix}", "Active Subscriber — Definition",
        f"“{C.ACTIVE_SUBSCRIBER}” means a subscriber account that meets all of the following, "
        f"determined monthly:")
    for el in C.DEAL["active_subscriber_elements"]:
        C.bullet(doc, el)


def build_retail():
    doc = C.new_doc()
    title = C.AGREEMENTS["retail"]
    C.add_cover(doc, "DEFINITIVE AGREEMENT 06", title,
                f"{C.TRIBE_SHORT} • {C.OPERATOR_SHORT} • {C.PROGRAM_SHORT} Fiber Package")
    C.setup_header_footer(doc, "06 — Retail, Billing, and Subscriber-Revenue Agreement")
    C.add_toc(doc)
    intro_recital(doc, title)

    a = 1
    a = art_definitions(doc, a, [
        ("Active Subscriber", "as defined in the Per-Active-Subscriber Payment article of this Agreement "
                "(the controlling definition for payment purposes)."),
        ("Retail Provider of Record", "the entity holding retail branding, customer contracts, pricing "
                "administration, sales, billing, collections, and customer-facing regulatory obligations, "
                "subject to Award approval."),
        ("Customer Data", "data relating to end-user customers, categorized in the Data Rights article; "
                "no single Party is characterized as unqualified owner of customer personal data."),
        ("Program Income", "income treatment determined under " + C.CITES["prog_income"] + " by the "
                "controlling Award, not by the label the Parties assign."),
    ])
    a = art_precedence(doc, a)

    # Appointment as retail provider of record
    C.article(doc, a, "Appointment as Retail Provider of Record")
    C.section(doc, f"{a}.1", "Appointment",
        f"Subject to {C.AGENCY_SHORT}/{C.DOC_FULL} Award approval, the {C.TRIBE_SHORT} appoints "
        f"{C.OPERATOR_SHORT} as the retail provider of record for broadband service over the {C.NETWORK} "
        f"in the {C.SERVICE_TERRITORY}.")
    C.section(doc, f"{a}.2", "Scope of Role",
        f"As Retail Provider of Record, {C.OPERATOR_SHORT} holds responsibility for branding, customer "
        f"contracts, pricing administration, sales, billing, collections, ordinary bad-debt risk, and "
        f"customer-facing regulatory and customer-service obligations.")
    C.flag_para(doc, C.FLAG_GRANT,
        "The retail-provider-of-record designation is subject to Award approval; confirm against the "
        "executed Award and any Specific Award Conditions before finalizing.")
    a += 1

    # Branding
    C.article(doc, a, "Branding")
    C.section(doc, f"{a}.1", "Retail Brand",
        f"{C.OPERATOR_SHORT} may market retail service under its brand, subject to any Tribal "
        f"acknowledgement and Award attribution/co-branding requirements. {C.FLAG_BUSINESS}")
    C.section(doc, f"{a}.2", "Tribal and Federal Attribution",
        f"Customer-facing materials will include any required {C.TRIBE_SHORT} and {C.PROGRAM_SHORT}/"
        f"{C.AGENCY_SHORT} attribution and non-discrimination notices.")
    a += 1

    # Product design
    C.article(doc, a, "Product Design and Service Offerings")
    C.section(doc, f"{a}.1", "Service Tiers",
        f"{C.OPERATOR_SHORT} will design retail tiers meeting or exceeding the {C.PROGRAM_SHORT} service "
        f"floor of {C.SPEED_FLOOR}, consistent with {C.SCHEDULES['S7']}.")
    C.section(doc, f"{a}.2", "Changes",
        "Material changes to core offerings serving Award commitments will be coordinated with the Tribe "
        "and confirmed against Award service commitments.")
    a += 1

    # Pricing + affordability
    C.article(doc, a, "Pricing Authority and Affordability Commitments")
    C.section(doc, f"{a}.1", "Pricing Authority",
        f"{C.OPERATOR_SHORT} administers retail pricing, subject to the affordability commitments below "
        f"and any Award-required rate commitments. {C.FLAG_BUSINESS}")
    C.section(doc, f"{a}.2", "Affordability — Low-Cost Option",
        f"{C.OPERATOR_SHORT} will offer a low-cost service option of at least {C.SPEED_FLOOR} "
        f"(the “Low-Cost Option”) meeting the affordability commitments applicable to the Award, "
        f"at a rate {C.PH('confirm Award-required low-cost rate / methodology')}. {C.FLAG_GRANT}")
    C.section(doc, f"{a}.3", "Nondiscrimination",
        "Service will be offered on a nondiscriminatory basis throughout the Approved Project Area "
        "consistent with Award commitments.")
    a += 1

    # Eligibility, orders, installations
    C.article(doc, a, "Customer Eligibility, Orders, and Installations")
    C.section(doc, f"{a}.1", "Eligibility",
        "Customer eligibility follows the Approved Project Area and any Award location eligibility, with "
        "no unlawful discrimination.")
    C.section(doc, f"{a}.2", "Orders and Installations",
        "Operator manages order intake, scheduling, and installation to the Demarcation Point, "
        f"coordinating field work with O&M under the {C.AGREEMENTS['om']}.")
    a += 1

    # Customer contracts + AUP/privacy
    C.article(doc, a, "Customer Contracts; Acceptable-Use and Privacy Terms")
    C.section(doc, f"{a}.1", "Customer Contracts",
        f"{C.OPERATOR_SHORT} contracts with end-user customers in its own name as Retail Provider of "
        f"Record, using terms consistent with this Agreement and the Award.")
    C.section(doc, f"{a}.2", "Acceptable Use and Privacy",
        f"Customer terms include an acceptable-use policy and a privacy notice consistent with the "
        f"{C.AGREEMENTS['privacy']} and {C.SCHEDULES['S11']}, which control data-protection matters.")
    a += 1

    # Customer support + complaints
    C.article(doc, a, "Customer Support and Complaints")
    C.section(doc, f"{a}.1", "Support",
        "Operator provides customer support (contact channels, hours, and response standards) per "
        f"{C.SCHEDULES['S7']}.")
    C.section(doc, f"{a}.2", "Complaints",
        "Operator maintains a complaint-handling process with logging, resolution timeframes, and "
        "reporting, and escalates regulatory complaints as required.")
    a += 1

    # Billing / payment / credits / refunds
    C.article(doc, a, "Billing, Payment Processing, Credits, and Refunds")
    C.section(doc, f"{a}.1", "Billing",
        "Operator bills customers, administers payment processing, and issues accurate, itemized "
        "invoices reflecting taxes and regulatory fees.")
    C.section(doc, f"{a}.2", "Credits and Refunds",
        "Operator administers billing credits and refunds under a documented policy; credits and refunds "
        "reduce amounts counted toward the per-subscriber payment as provided in the Payment article.")
    a += 1

    # Collections / nonpayment / disconnection
    C.article(doc, a, "Collections, Nonpayment, and Disconnection")
    C.section(doc, f"{a}.1", "Collections and Nonpayment",
        f"Operator manages collections and bears ordinary bad-debt risk. Accounts suspended for "
        f"nonpayment beyond {C.PH('[30] days')} are excluded from Active Subscriber counts as provided "
        f"in the Payment article.")
    C.section(doc, f"{a}.2", "Disconnection",
        "Disconnection follows applicable notice and consumer-protection requirements, including any "
        "medical/lifeline protections.")
    a += 1

    # Regulatory + outage notices + taxes/fees + bad debt
    C.article(doc, a, "Regulatory Compliance, Outage Notices, Taxes, Fees, and Bad Debt")
    C.section(doc, f"{a}.1", "Regulatory Compliance",
        f"Operator complies with applicable FCC/USAC and, where applicable, ETC and Lifeline requirements "
        f"({C.CITES['usac_lifeline']}) and CPNI protections ({C.CITES['cpni']}).")
    C.section(doc, f"{a}.2", "Outage Notices",
        f"Operator provides customer outage notices and any required regulatory outage reporting, "
        f"coordinating with O&M under the {C.AGREEMENTS['om']}.")
    C.section(doc, f"{a}.3", "Taxes and Fees",
        f"Operator administers, collects, and remits applicable taxes, USF/regulatory fees, and "
        f"pass-through charges. {C.FLAG_BUSINESS}  Treatment of taxes and fees in the per-subscriber "
        f"payment base is addressed in the Payment article.")
    C.section(doc, f"{a}.4", "Bad Debt",
        "Ordinary bad debt is Operator's risk; uncollectible amounts are excluded from the per-subscriber "
        "payment base as provided in the Payment article.")
    a += 1

    # Data rights (by category)
    C.article(doc, a, "Data Rights")
    C.section(doc, f"{a}.1", "No Unqualified Ownership of Personal Data",
        f"No Party is the unqualified “owner” of customer personal data. Roles and rights are "
        f"allocated by data category below, coordinated with the {C.AGREEMENTS['privacy']} and "
        f"{C.SCHEDULES['S11']}, which control data-protection, security, and breach matters.")
    C.section(doc, f"{a}.2", "Allocation by Data Category",
        "The following table allocates controller/owner versus processor/service-provider roles and "
        "rights (access, permitted use, retention, security, breach notice, portability, deletion) by "
        "data category:")
    C.add_table(doc,
        ["Data Category", "Controller / Owner", "Processor / Service Provider",
         "Access", "Permitted Use", "Retention", "Deletion / Portability"],
        [
            ["Customer personal / account data",
             f"Shared: {C.OPERATOR_SHORT} as Retail Provider of Record; {C.TRIBE_SHORT} project-level "
             f"oversight [confirm]", f"{C.OPERATOR_SHORT} systems",
             f"{C.TRIBE_SHORT} + government: project-level oversight access", "Service delivery, billing, "
             "regulatory", C.PH("period"), "Per privacy addendum + law"],
            ["CPNI",
             f"{C.OPERATOR_SHORT} (carrier duties)", f"{C.OPERATOR_SHORT}",
             "Restricted per CPNI rules", f"Per {C.CITES['cpni']}", "Per rule", "Per rule"],
            ["Aggregated / de-identified service data",
             "Shared per addendum", f"{C.OPERATOR_SHORT}",
             f"{C.TRIBE_SHORT} + government project reporting", "Reporting, planning, Award compliance",
             C.PH("period"), "As agreed"],
            ["Network / operational performance data",
             f"{C.TRIBE_SHORT} (Grant-Funded Assets) [confirm]", f"{C.OPERATOR_SHORT} operator",
             f"{C.TRIBE_SHORT} + government full access", "O&M, oversight, Award reporting",
             f"{C.DEAL['records_retention_years']} yrs+", "Return/transition on exit"],
            ["Award-compliance / reporting data",
             f"{C.TRIBE_SHORT} (recipient)", f"{C.OPERATOR_SHORT} supports",
             f"{C.TRIBE_SHORT} + {C.AGENCY_SHORT}/{C.DOC_FULL} full access", "Award compliance",
             f"Per {C.CITES['records']}", "Retain per Award"],
        ],
        widths=[1.3, 1.4, 1.0, 1.0, 1.1, 0.7, 1.0], font_size=8)
    C.section(doc, f"{a}.3", "Tribe and Government Oversight Access",
        f"The {C.TRIBE_SHORT} and {C.AGENCY_SHORT}/{C.DOC_FULL} have project-level oversight access to "
        f"data necessary for Award compliance and stewardship, subject to customer-privacy protections "
        f"and the {C.AGREEMENTS['privacy']}.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
        "Controller/processor allocation, access scope, and deletion/portability by category are legal "
        "determinations; reconcile with the privacy addendum and applicable law.")
    a += 1

    # Record access
    C.article(doc, a, "Record Access")
    C.section(doc, f"{a}.1", "Records and Access",
        f"Operator maintains billing, subscriber, and compliance records and provides the {C.TRIBE_SHORT} "
        f"and {C.AGENCY_SHORT}/{C.DOC_FULL} access per {C.CITES['records']}, retained for "
        f"{C.DEAL['records_retention_years']} years, subject to customer-privacy protections.")
    a += 1

    # Transition
    C.article(doc, a, "Transition")
    C.section(doc, f"{a}.1", "Continuity and Transition",
        f"On expiration, termination, step-in, or change of provider, transition of customers, data, and "
        f"retail functions is governed by the {C.AGREEMENTS['transition']}, which controls those "
        f"procedures; transition assistance continues for up to {C.DEAL['transition_assistance_months']} "
        f"months.")
    a += 1

    # ---- PER-ACTIVE-SUBSCRIBER PAYMENT SCHEDULE (own article + tables) ----
    C.article(doc, a, "Per-Active-Subscriber Payment Schedule")
    pay = a
    C.section(doc, f"{pay}.1", "Primary Payment",
        f"As the primary economic model of this package, {C.OPERATOR_SHORT} will pay the {C.TRIBE_SHORT} "
        f"{C.DEAL['per_subscriber_amount']} for each Active Subscriber, determined monthly as set out in "
        f"this Article. {C.FLAG_BUSINESS}  The per-subscriber amount is a placeholder to be confirmed.")

    active_subscriber_definition_para(doc, f"{pay}.2")

    C.section(doc, f"{pay}.3", "Exclusions and Counting Rules",
        "The following are expressly excluded from, or governed by special rules within, the Active "
        "Subscriber count:")
    C.add_table(doc,
        ["Item", "Treatment"],
        [
            ["Activations", "Counted from first successful service provisioning"],
            ["Disconnects", "Excluded from the date service ceases"],
            ["Suspensions (nonpayment)", C.PH("excluded beyond [30] days of suspension")],
            ["Seasonal / vacation accounts", C.PH("counted / excluded — confirm methodology")],
            ["Free / courtesy / subsidized accounts", "Excluded unless separately agreed and Award-permitted"],
            ["Partial months", C.PH("prorated daily vs. full-month — confirm")],
            ["Multi-service at one location", "One location = one Active Subscriber unless separately agreed"],
            ["Bulk / multi-dwelling accounts", "Counted per billable unit per agreed methodology"],
            ["Credits / refunds", "Net out of the payment base"],
            ["Taxes / regulatory fees", "Excluded from the payment base"],
            ["Uncollectibles / bad debt", "Excluded (net of uncollectible amounts)"],
        ],
        widths=[2.6, 3.9])

    C.section(doc, f"{pay}.4", "Monthly Subscriber Reconciliation Report",
        f"Operator will deliver a monthly subscriber reconciliation report (cross-reference: 04 "
        f"Operational Forms — Monthly Subscriber Reconciliation and {C.SCHEDULES['S8']}) reconciling "
        f"opening count, activations, disconnects, suspensions, and exclusions to the closing Active "
        f"Subscriber count and the payment due.")

    C.section(doc, f"{pay}.5", "Invoicing, Payment Timing, Disputes, Corrections, and True-Ups",
        f"Operator will invoice and pay within {C.PH('[__] days')} after month-end. Disputed amounts are "
        f"paid when undisputed and resolved under a documented dispute process; late payments accrue "
        f"{C.PH('late charge / interest')}. Errors are corrected and reconciled through periodic "
        f"true-ups. {C.FLAG_BUSINESS}")

    C.section(doc, f"{pay}.6", "Audit and Verification with Customer-Privacy Protection",
        f"The {C.TRIBE_SHORT} may audit and verify subscriber counts and payment calculations on "
        f"{C.DEAL['audit_notice_business_days']} Business Days' notice, using privacy-protective methods "
        f"(aggregated data, redaction, or independent verification) consistent with CPNI and the "
        f"{C.AGREEMENTS['privacy']}.")

    C.section(doc, f"{pay}.7", "Treatment During vs. After the Federal Performance Period",
        f"During the federal performance period, payment amounts and any program-income treatment are "
        f"administered per the Award and {C.CITES['prog_income']}. After the performance period, "
        f"treatment is {C.PH('confirm post-performance-period treatment')}. {C.FLAG_GRANT}")

    C.section(doc, f"{pay}.8", "Gross vs. Net; Taxes, Fees, and Processing Charges",
        f"The payment base is measured net of credits, refunds, and uncollectibles and exclusive of taxes "
        f"and regulatory fees. {C.FLAG_BUSINESS}  Whether the base is gross or net of payment-processing "
        f"charges, and the allocation of regulatory assessments, are business decisions to be confirmed.")

    C.section(doc, f"{pay}.9", "Program-Income Controls and Restricted Project Account",
        f"Amounts constituting Program Income are subject to {C.CITES['prog_income']} controls, including "
        f"any required restricted project account and permitted-use restrictions. {C.FLAG_GRANT}  "
        f"{C.DEAL['program_income_note']}.")

    C.section(doc, f"{pay}.10", "Annual Review and Escalation (if approved)",
        f"If approved under the Award, the per-subscriber amount is subject to annual review and "
        f"escalation per {C.PH('index / methodology')}. {C.FLAG_BUSINESS}  {C.FLAG_GRANT}")

    C.section(doc, f"{pay}.11", "Treatment on Expiration, Termination, Step-In, or Change of Provider",
        f"On expiration, termination, step-in, customer migration, or change of provider, payment "
        f"obligations are prorated to the transition date and reconciled, with continuity governed by the "
        f"{C.AGREEMENTS['transition']}.")

    C.section(doc, f"{pay}.12", "Payment Characterization Alternatives",
        "The label the Parties assign to the payment does not control program-income treatment. The "
        "following characterization alternatives are presented; the recommended alternative is Option D:")
    C.add_table(doc,
        ["Option", "Characterization", "Recommended"],
        [[k, v, "✓ RECOMMENDED" if k == C.DEAL["pay_recommended"] else ""]
         for k, v in C.DEAL["pay_options"].items()],
        widths=[0.8, 4.7, 1.0], col_align=[None, None, "c"])
    C.flag_para(doc, C.FLAG_GRANT,
        f"{C.DEAL['program_income_note']}. Program-income treatment turns on the controlling Award and a "
        f"written {C.AGENCY_SHORT} determination, not on the characterization label.")
    C.flag_para(doc, C.FLAG_ATTORNEY,
        "Confirm the recommended Option D characterization with grant counsel and financial advisors "
        "before finalizing.")
    a += 1

    a = gov_law_article(doc, a)

    closing_disclaimer(doc)
    C.signature_block(doc,
        extra_note="Retail-provider-of-record designation and payment characterization are subject to "
                   "Award approval; confirm signatory authority and authorizing resolution before execution.")
    return C.save(doc, "02_Definitive_Agreements",
                  "06_Retail_Billing_and_Subscriber_Revenue_Agreement.docx")


if __name__ == "__main__":
    p1 = build_om()
    p2 = build_retail()
    print("DOC 1 (O&M / Lifecycle):", p1)
    print("DOC 2 (Retail / Billing / Subscriber Revenue):", p2)
