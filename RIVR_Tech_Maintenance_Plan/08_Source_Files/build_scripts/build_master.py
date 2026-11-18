# -*- coding: utf-8 -*-
"""Builds two consolidated master deliverables for the entire Maintenance Program:
   1) Complete Program Manual (Word)
   2) Master Workbook (Excel)
All content is pulled from rivr_content.py so figures stay consistent.
"""
import os
import rivr_content as C
from docx_helpers import (new_doc, cover_page, toc_field, h1, h2, h3, para, bullet,
                          numbered, callout, table, save)

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
R = C.compute_model()
SC = C.scenario_results()


def pth(*parts):
    return os.path.join(BASE, *parts)


# Concise KPI + implementation data for the consolidated deliverables
KPIS = [
    ("Remote-resolution %", "0.67", "≥67% green / 60-67 yellow / <60 red", "higher"),
    ("Customer-premises issue %", "0.30", "informational", "info"),
    ("Billable visits (monthly)", "130", "informational", "info"),
    ("Fees collected (monthly)", "$8,000", "informational", "info"),
    ("Waiver %", "0.15", "≤20% green / 20-30 yellow / >30 red", "lower"),
    ("Dispute rate", "informational", "track monthly", "info"),
    ("Repeat visits within 30 days %", "0.09", "≤9% green / 9-14 yellow / >14 red", "lower"),
    ("Cost per dispatch", "$130", "informational", "info"),
    ("Avoided truck rolls (monthly)", "90", "≥90 green / 60-90 yellow / <60 red", "higher"),
    ("Protection-plan enrollment %", "0.10", "≥10% green / 6-10 yellow / <6 red", "higher"),
    ("Policy-related churn %", "0.003", "≤0.3% green / 0.3-0.6 yellow / >0.6 red", "lower"),
    ("Customer satisfaction (CSAT)", "0.90", "≥90% green / 85-90 yellow / <85 red", "higher"),
    ("Technician coding accuracy %", "0.95", "≥95% green / 90-95 yellow / <90 red", "higher"),
    ("Support disclosure compliance %", "0.98", "≥98% green / 93-98 yellow / <93 red", "higher"),
]

PHASES = [
    ("Phase 1", "Policy, financial validation, legal review, and system design", "Days 1–40"),
    ("Phase 2", "Employee training and customer education", "Days 20–95"),
    ("Phase 3", "30-day warning and courtesy-waiver period", "Days 55–85"),
    ("Phase 4", "Full billing implementation", "Days 85–90"),
    ("Phase 5", "Performance review and optimization", "Days 90–120+"),
]

POLICY_SECTIONS = [
    ("Purpose", "Establish how RIVR Tech determines responsibility for maintenance and trouble visits, when a charge may apply, and how customers are protected from surprise billing. Network and equipment repairs stay free."),
    ("Scope", "All residential and business customers of RIVR Tech broadband, managed Wi-Fi, and voice services, and all employees/contractors who triage, dispatch, or perform visits."),
    ("Effective Date", C.EFFECTIVE_DATE_PLACEHOLDER + " — billing begins only after the education period and a 30-day warning-only grace period."),
    ("Services Covered", "; ".join(C.SERVICES_COVERED)),
    ("Responsibility Classifications", "Four categories: RIVR Tech responsibility ($0); Customer-premises responsibility (fee may apply with documentation); Shared responsibility (supervisor review, reduced/waived); Inconclusive ($0 unless management approves on clear evidence)."),
    ("RIVR Tech Responsibilities", "Maintain/repair the network, fiber, drops, ONTs, and gateways free; perform strong remote troubleshooting; disclose potential charges in advance; document findings before any fee; offer waivers; provide a fair dispute process."),
    ("Customer Responsibilities", "Maintain customer-owned equipment, inside wiring, and premises power; provide safe access and an authorized adult (residential); cooperate with remote troubleshooting; acknowledge advance disclosure."),
    ("Billable Visits", "A visit may be billable when documented findings show a customer-premises root cause (customer equipment, damaged wiring, premises power, third-party devices, relocation, missed appointment, denied access)."),
    ("Nonbillable Visits", "Confirmed network/equipment problems, normal fiber/drop failures, no-trouble-found, inconclusive findings, and repeat visits shortly after a RIVR Tech repair are never billed."),
    ("Shared-Responsibility Cases", "When cause is partly RIVR Tech and partly premises, a supervisor reviews and may apply a reduced fee or full waiver."),
    ("Inconclusive Findings", "No clear cause or not reproduced = no charge unless management approves on clear, documented evidence."),
    ("Inside-Wiring Work", "Inside wiring beyond the demarcation is customer responsibility; basic diagnostics may be billable; no major rewiring/concealed-wiring/construction under this policy."),
    ("Customer-Owned Equipment", "Configuration/failure of customer routers/mesh/devices is customer-premises; a bypass test proving the RIVR Tech service is healthy must be documented."),
    ("RIVR Tech-Owned Equipment", "Failure of RIVR Tech ONTs/gateways is repaired/replaced free, absent customer damage."),
    ("Customer-Damaged Company Equipment", "Damage to RIVR Tech equipment (physical, water, pet/pest, unauthorized modification) may incur a charge, subject to documentation, supervisor review, and hardship consideration."),
    ("Wi-Fi Coverage Limitations", "Coverage limits from home size/construction/placement are customer-premises; visits are typically educational and often courtesy on first occurrence."),
    ("Individual-Device Limitations", "When one device underperforms while a wired test shows plan speed, it is a customer-premises matter."),
    ("Equipment Relocation", "Customer-requested relocation of working equipment is billable starting at $95 plus materials."),
    ("Missed Appointments", "$35 administrative fee, with a typical first-time courtesy waiver."),
    ("Denied Access", "If access is denied and work cannot be completed, a $35 fee may apply."),
    ("After-Hours Service", "Customer-caused after-hours visits add a $75 surcharge; network emergencies remain free at all hours."),
    ("Residential Customer Rules", "Authorized adult (18+) present; residential fee $75; courtesy/hardship/accommodation waivers apply."),
    ("Business Customer Rules", "Business fee $125; custom configuration may be additional labor or referred to IT; business SLAs govern where applicable (legal review)."),
    ("Emergency & Safety Exceptions", "Safety hazards addressed first regardless of billing; charges (if any) reviewed by a supervisor after safety is ensured."),
    ("Hardship & Reasonable-Accommodation Exceptions", "Documented hardship (incl. Lifeline/low-income) and disability/medical accommodations qualify for waivers/alternatives, with manager approval."),
    ("Advance Customer Disclosure", "Before any dispatch that could bill, support discloses that a fee may apply based on documented findings and records acknowledgment. No fee is valid without proper disclosure."),
    ("Customer Acknowledgment", "The customer acknowledges only that a charge may apply based on findings — not an admission of responsibility."),
    ("Technician Documentation", "Findings, test results, and (where applicable) photographs are recorded before any fee, using standardized codes."),
    ("Billing Authorization", "A charge is authorized only when classification, documentation, disclosure, and the required approval level are all satisfied. Technicians never collect cash."),
    ("Dispute & Appeal Process", "Frontline explanation → supervisor review → technical review → billing adjustment, within a defined timeline, with executive escalation criteria."),
    ("Manager Waiver Authority", "Managers may waive fees under defined categories; waivers are tracked."),
    ("Quality-Control Review", "A sample of billable tickets is audited for classification, documentation, disclosure, and coding accuracy."),
    ("Policy Review Schedule", "Reviewed at least annually and after material changes in cost, regulation, or customer feedback."),
]


# ==========================================================================
# 1) COMPLETE PROGRAM MANUAL (Word)
# ==========================================================================
def build_manual():
    doc = new_doc()
    cover_page(doc, "Customer-Premises Maintenance & Billable Trouble-Visit Program",
               "Complete Program Manual",
               "Consolidated reference — policy, fees, operations, financials, training, communications, and implementation")
    toc_field(doc)

    # 1 Executive summary
    h1(doc, "1. Executive Summary")
    para(doc, f"{C.COMPANY_SHORT} keeps all network and equipment repairs free and introduces reasonable, "
              f"fully documented charges only for customer-premises trouble visits. The program prioritizes "
              f"deflection and education over fee revenue and protects {C.COMPANY_SHORT}'s community reputation "
              f"through advance disclosure, a first-incident courtesy waiver, and a 30-day warning-only grace period.")
    table(doc, ["Metric (Expected scenario)", "Value"], [
        ("Cost per dispatch (loaded)", C.money(R["cost_per_dispatch"])),
        ("Annual customer-caused dispatch cost (absorbed today)", C.money(R["cust_caused_dispatch_cost"])),
        ("Net trouble-visit fee revenue (Year 1)", C.money(R["net_fee_revenue"])),
        ("Protection-plan contribution margin (Year 1)", C.money(R["protection_margin"])),
        ("Avoided-truck-roll (deflection) savings", C.money(R["deflection_savings"])),
        ("Cost recovery of customer-caused dispatch cost", f"{R['cost_recovery_pct']*100:.0f}%"),
        ("Year 1 net financial effect (after one-time cost)", C.money(R["year1_net"])),
        ("Implementation payback period", f"{R['payback_months']:.1f} months"),
        ("Three-year net financial effect", C.money(R["three_year_net"])),
    ], col_widths=[4.6, 1.9])
    callout(doc, "KEY PRINCIPLE", "A fee is never assessed solely because a technician was dispatched. A charge "
            "requires documented findings, advance disclosure, and the correct approval.", "recommendation")

    # 2 Design principles
    h1(doc, "2. Program Design Principles")
    for t, d in [
        ("Network repairs stay free", "Confirmed network/equipment problems are never billed."),
        ("Charge only with evidence", "A fee requires documented findings, tests, and — where relevant — photos."),
        ("No surprise billing", "Advance disclosure and acknowledgment before any dispatch that could bill."),
        ("Deflect before dispatch", "Strong remote troubleshooting resolves more issues without a truck."),
        ("Educate, don't blame", "Language is 'customer-premises issue,' never 'customer fault.'"),
        ("Protect the vulnerable", "Hardship, accommodation, and courtesy waivers are built in."),
    ]:
        bullet(doc, d, bold_lead=f"{t}. ")

    # 3 Fee schedule
    h1(doc, "3. Fee Schedule")
    fee_rows = []
    for label, cons, bal, full, note in C.FEE_ITEMS:
        fmt = lambda x: ("$0" if x == 0 else f"${x}")
        fee_rows.append((label, fmt(cons), fmt(bal), fmt(full)))
    table(doc, ["Fee Item", "Conservative", "Balanced (Rec.)", "Full Recovery"], fee_rows,
          col_widths=[3.3, 1.05, 1.15, 1.05], font_size=8.5)
    para(doc, "Additional labor bills at $35 per 30 minutes after the first 30 on billable work only. "
              "Relocation and inside-wiring add materials at cost. The first customer-caused incident is eligible "
              "for a one-time educational courtesy waiver. Recommended posture: Balanced.", size=9, italic=True)

    # 4 Responsibility classifications + matrix reference
    h1(doc, "4. Responsibility Classifications")
    table(doc, ["Classification", "Customer Charge"], [
        ("1. RIVR Tech responsibility", "No customer charge."),
        ("2. Customer-premises responsibility", "A fee may apply when supported by documented findings."),
        ("3. Shared responsibility", "Supervisor review; reduced fee or waiver may apply."),
        ("4. Inconclusive", "No charge unless management approves based on clear evidence."),
    ], col_widths=[2.6, 3.9])
    h2(doc, "4.1 Responsibility Matrix (all scenarios)")
    para(doc, "The full 42-scenario matrix is reproduced in the Master Workbook. Summary of classification + "
              "recommended charge:", size=9.5)
    mrows = [(row[0], row[1], row[2], row[5]) for row in C.MATRIX]
    table(doc, ["Scenario", "Segment", "Classification", "Recommended Charge"], mrows,
          col_widths=[2.6, 0.85, 1.75, 1.4], font_size=8)

    # 5 Policy (condensed-complete, all 34 sections)
    h1(doc, "5. Customer-Premises Maintenance Policy")
    callout(doc, "PROPOSED POLICY", "This is a proposed policy for review and approval — not established policy "
            "and not legal advice until adopted and cleared by legal/regulatory review.", "policy")
    for i, (title, body) in enumerate(POLICY_SECTIONS, 1):
        para(doc, f"5.{i} {title}", bold=True, size=11, color=C.BRAND["secondary"], space_after=1)
        para(doc, body, size=10, space_after=6)

    # 6 Operations (SOP summary)
    h1(doc, "6. Operations — Support Triage & Field SOP")
    h2(doc, "6.1 Remote Troubleshooting (before any dispatch)")
    for s in ["Verify customer & account; check for outages; review history.",
              "Review ONT/gateway status, alarms, optical levels; confirm power, cables, connections.",
              "Reboot in order (ONT → gateway → device); separate internet from Wi-Fi and whole-home from single-device.",
              "Run approved speed test; request wired test; identify third-party equipment.",
              "Educate when resolvable remotely; disclose potential charges and record acknowledgment before dispatch.",
              "Select the correct dispatch + billing code; escalate network issues to Network Operations."]:
        bullet(doc, s)
    h2(doc, "6.2 Field Technician Sequence")
    for s in ["Arrive and communicate without blaming language; review support notes.",
              "Test optical, ONT, gateway, wired, wireless; bypass customer gear to prove the RIVR Tech service is healthy.",
              "Evaluate inside wiring; photograph damage/power/wiring; document all results.",
              "Disposition the ticket with the correct code; explain findings plainly; capture electronic acknowledgment.",
              "Route shared/damage/relocation/repeat items for supervisor review; expect QA audits."]:
        bullet(doc, s)
    h2(doc, "6.3 Technicians Must Not")
    for x in ["Collect cash.", "Guarantee a charge will be removed.",
              "Classify a visit as billable without evidence.", "Use blaming language.",
              "Perform unapproved major wiring or construction."]:
        bullet(doc, x)

    # 7 Ticket & billing codes
    h1(doc, "7. Ticket & Billing Codes")
    crows = [(c[0], c[1], c[3], c[5], c[6]) for c in C.CODES]
    table(doc, ["Code", "Name", "Billable", "Approval", "Billing"], crows,
          col_widths=[1.0, 1.9, 1.0, 1.3, 1.0], font_size=8.5)

    # 8 Customer authorization
    h1(doc, "8. Customer Authorization (disclosure)")
    para(doc, "Before any dispatch that could bill, disclose that a charge MAY apply based on documented findings "
              "and record acknowledgment. The customer acknowledges only potential charge — not fault. Standard "
              "wording exists for recorded call, email, SMS, portal, work order, and paper acknowledgment "
              "(see the Support & Field Operations SOP).")

    # 9 Financials
    h1(doc, "9. Financial Summary")
    srow = []
    for name in ["Low", "Expected", "High"]:
        s = SC[name]
        srow.append((name, C.money(s["net_fee_revenue"]), C.money(s["protection_margin"]),
                     C.money(s["deflection_savings"]), C.money(s["year1_net"]), C.money(s["three_year_net"])))
    table(doc, ["Scenario", "Net Fees", "Plan Margin", "Deflection", "Year 1 Net", "3-Yr Net"], srow,
          col_widths=[1.0, 1.0, 1.05, 1.05, 1.05, 1.05], font_size=9)
    para(doc, "Even the Low scenario delivers positive three-year value, driven primarily by avoided truck rolls. "
              "Full live model: Maintenance_Program_Financial_Model.xlsx.", size=9.5, italic=True)

    # 10 Protection plan
    h1(doc, "10. Optional Maintenance-Protection Plan")
    para(doc, f"RIVR Tech Home Maintenance Protection — ${C.PROTECTION_RECOMMENDED:.2f}/month (optional). Covers "
              f"standard customer-premises trouble visits, basic inside-wiring diagnostics, Wi-Fi education, and "
              f"basic device-connection help, with priority scheduling. It is a service plan — not insurance. "
              f"Excludes replacement of customer devices, major rewiring, concealed wiring, construction, commercial "
              f"network administration, willful damage, and fire/flood damage.")
    callout(doc, None, "The protection plan must be characterized as a service/maintenance plan, not insurance. "
            "Confirm with legal and insurance advisers.", "legal")

    # 11 Training
    h1(doc, "11. Employee Training")
    para(doc, "A 60-minute training covers: why the policy is changing; free vs. billable; the four classifications; "
              "remote troubleshooting; advance disclosure; documentation; empathetic communication; billing, "
              "disputes, and waivers; scenario exercises; and an 18-question knowledge check (80% pass). Role-specific "
              "coaching exists for customer service, support, dispatch, field techs, billing, sales, business reps, "
              "supervisors, managers, network operations, and marketing.")

    # 12 Customer communications
    h1(doc, "12. Customer Communications")
    para(doc, "A 60-day education program spans website, email, bill message, bill insert, social media, portal, "
              "IVR/hold message, technician leave-behind, new-customer materials, and a business-customer letter. "
              "Language is warm, local, simple, and respectful, and always leads with what stays free. Full templates "
              "and 22 FAQs are in the Customer Communication Package; a standalone 28-item FAQ is also available.")

    # 13 Disputes & waivers
    h1(doc, "13. Disputes & Waivers")
    para(doc, "Dispute path: frontline explanation → supervisor review → technical review → billing adjustment, "
              "within a defined timeline; no collection action while a dispute is open. Waiver categories:")
    table(doc, ["Category", "Basis", "Approval"], [(a, b, c) for a, b, c in C.WAIVER_CATEGORIES],
          col_widths=[1.9, 3.2, 1.4], font_size=9)

    # 14 Implementation
    h1(doc, "14. Implementation (90 days)")
    table(doc, ["Phase", "Focus", "Window"], PHASES, col_widths=[1.2, 4.0, 1.3], font_size=10)
    para(doc, "Customers are educated first; billing begins only after the 30-day grace period. Full task-level "
              "tracker: 90_Day_Implementation_Tracker.xlsx.", size=9.5, italic=True)

    # 15 KPIs
    h1(doc, "15. KPIs & Targets")
    table(doc, ["KPI", "Target", "Thresholds"], [(k, t, th) for k, t, th, _ in KPIS],
          col_widths=[2.4, 1.3, 2.9], font_size=8.5)

    # 16 Legal flags
    h1(doc, "16. Legal & Regulatory Review Flags")
    table(doc, ["Item", "What to Review", "Owner"], [(a, b, c) for a, b, c in C.LEGAL_FLAGS],
          col_widths=[1.9, 3.3, 1.3], font_size=8)

    # 17 Executive decisions + data needed
    h1(doc, "17. Executive Decisions & Data Needed")
    h2(doc, "17.1 Decisions Requiring Executive Approval")
    for i, (title, desc, owner) in enumerate(C.EXEC_DECISIONS, 1):
        bullet(doc, f"{title} — {desc} (Owner: {owner})")
    h2(doc, "17.2 Data Points to Replace Assumptions")
    for name, why, src in C.DATA_NEEDED:
        bullet(doc, f"{name} — {why} ({src})")

    # 18 Assumptions register
    h1(doc, "18. Assumptions Register")
    table(doc, ["Assumption", "Value", "Note"], C.assumptions_register(),
          col_widths=[2.3, 1.1, 3.1], font_size=8.5)
    callout(doc, None, "This manual consolidates the program and labeled assumptions. It is not legal advice; "
            "provisions require legal, regulatory, accounting, and insurance review before adoption.", "warning")

    save(doc, pth("RIVR_Tech_Maintenance_Plan", "RIVR_Tech_Maintenance_Program_Complete_Manual.docx"),
         "Complete Program Manual")


# ==========================================================================
# 2) MASTER WORKBOOK (Excel)
# ==========================================================================
BR = C.BRAND
F_TITLE = Font(color="FFFFFF", bold=True, size=16)
F_SUB = Font(color="FFFFFF", italic=True, size=10)
F_HDR = Font(color="FFFFFF", bold=True, size=10)
F_BOLD = Font(bold=True, size=10)
F_NORM = Font(size=10)
F_ITAL = Font(size=9, italic=True, color=BR["gray"])
F_PRIM = Font(bold=True, size=11, color=BR["primary"])
FILL_TITLE = PatternFill("solid", fgColor=BR["dark"])
FILL_SUB = PatternFill("solid", fgColor=BR["secondary"])
FILL_HDR = PatternFill("solid", fgColor=BR["primary"])
FILL_INPUT = PatternFill("solid", fgColor="FFF3C4")
FILL_CALC = PatternFill("solid", fgColor="E3F0F6")
FILL_REC = PatternFill("solid", fgColor="D7F0E7")
FILL_WARN = PatternFill("solid", fgColor="F6D9CC")
FILL_LIGHT = PatternFill("solid", fgColor=BR["light"])
thin = Side(style="thin", color="C9D6DC")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
CEN = Alignment(horizontal="center", vertical="center", wrap_text=True)
RGT = Alignment(horizontal="right", vertical="center")
WRP = Alignment(horizontal="left", vertical="top", wrap_text=True)


def _title(ws, t, sub, ncols):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncols)
    c = ws.cell(row=1, column=1, value=f"{C.COMPANY_SHORT} — {t}")
    c.fill = FILL_TITLE; c.font = F_TITLE
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 28
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncols)
    c2 = ws.cell(row=2, column=1, value=sub); c2.fill = FILL_SUB; c2.font = F_SUB
    c2.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=ncols)
    ws.cell(row=3, column=1, value=f"{C.DOC_VERSION} | {C.DOC_DATE} | {C.COMPANY_LEGAL} | NOT LEGAL ADVICE").font = F_ITAL


def _hdr(ws, row, ncols, start=1):
    for c in range(start, start + ncols):
        cell = ws.cell(row=row, column=c)
        cell.fill = FILL_HDR; cell.font = F_HDR; cell.alignment = CEN; cell.border = BORDER


def _rows(ws, start_row, data, widths=None, first_bold=True, fills=None, zebra=True, fontsize=9):
    r = start_row
    for ri, row in enumerate(data):
        for ci, val in enumerate(row, 1):
            cell = ws.cell(row=r, column=ci, value=val)
            cell.font = Font(size=fontsize, bold=(first_bold and ci == 1),
                             color=(BR["primary"] if first_bold and ci == 1 else "000000"))
            cell.border = BORDER
            cell.alignment = WRP
            if zebra and ri % 2 == 1:
                cell.fill = FILL_LIGHT
        if fills:
            fills(ws, r, row)
        r += 1
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
    return r


def build_workbook():
    wb = Workbook()

    # ---- Contents ----
    wc = wb.active
    wc.title = "Contents"
    _title(wc, "Maintenance Program — Master Workbook", "One workbook for the entire program", 2)
    _hdr(wc, 5, 2)
    wc.cell(row=5, column=1, value="Sheet"); wc.cell(row=5, column=2, value="What's in it")
    contents = [
        ("Fee Schedule", "Conservative / Balanced (recommended) / Full-recovery fee options."),
        ("Responsibility Matrix", "All 42 scenarios: classification, billable status, charge, documentation, customer language."),
        ("Ticket & Billing Codes", "18 standardized codes with billable status, approval, and customer-facing text."),
        ("Financial Summary", "Headline results across Low / Expected / High scenarios."),
        ("KPIs & Targets", "Program KPIs with targets and red/yellow/green thresholds."),
        ("Implementation", "90-day, five-phase rollout plan."),
        ("Waivers", "Waiver categories, basis, and approval level."),
        ("Legal Flags", "Items requiring legal, regulatory, tax, or insurance review."),
        ("Assumptions", "Editable assumptions behind the financial figures."),
    ]
    _rows(wc, 6, contents, widths=[26, 80])
    wc.cell(row=6 + len(contents) + 1, column=1,
            value="Detailed live model, full matrix workbook, implementation tracker, and KPI dashboard remain as separate files in the program folders.").font = F_ITAL

    # ---- Fee Schedule ----
    wf = wb.create_sheet("Fee Schedule")
    _title(wf, "Fee Schedule", "Balanced posture recommended", 5)
    _hdr(wf, 5, 5)
    for j, h in enumerate(["Fee Item", "Conservative", "Balanced (Rec.)", "Full Recovery", "Note"], 1):
        wf.cell(row=5, column=j, value=h)
    _hdr(wf, 5, 5)
    r = 6
    for label, cons, bal, full, note in C.FEE_ITEMS:
        wf.cell(row=r, column=1, value=label).font = F_NORM
        wf.cell(row=r, column=2, value=(f"${cons}" if cons else "$0")).alignment = CEN
        bc = wf.cell(row=r, column=3, value=(f"${bal}" if bal else "$0")); bc.fill = FILL_REC; bc.alignment = CEN; bc.font = F_BOLD
        wf.cell(row=r, column=4, value=(f"${full}" if full else "$0")).alignment = CEN
        wf.cell(row=r, column=5, value=note).font = F_ITAL
        for c in range(1, 6):
            wf.cell(row=r, column=c).border = BORDER
        r += 1
    for i, w in enumerate([38, 14, 15, 14, 48], 1):
        wf.column_dimensions[get_column_letter(i)].width = w

    # ---- Responsibility Matrix ----
    wm = wb.create_sheet("Responsibility Matrix")
    _title(wm, "Trouble-Visit Responsibility Matrix", "All 42 scenarios", len(C.MATRIX_COLUMNS))
    for j, h in enumerate(C.MATRIX_COLUMNS, 1):
        wm.cell(row=5, column=j, value=h)
    _hdr(wm, 5, len(C.MATRIX_COLUMNS))
    wm.row_dimensions[5].height = 40
    cls_fill = {C.CLS_NET: FILL_REC, C.CLS_PREM: FILL_INPUT, C.CLS_SHARED: FILL_WARN, C.CLS_INC: FILL_CALC}
    r = 6
    for row in C.MATRIX:
        for j, val in enumerate(row, 1):
            cell = wm.cell(row=r, column=j, value=val)
            cell.font = Font(size=8, bold=(j == 1), color=(BR["primary"] if j == 1 else "000000"))
            cell.border = BORDER; cell.alignment = WRP
        wm.cell(row=r, column=3).fill = cls_fill.get(row[2], FILL_LIGHT)
        r += 1
    for i, w in enumerate([26, 12, 20, 12, 16, 16, 26, 22, 12, 14, 12, 18, 34], 1):
        wm.column_dimensions[get_column_letter(i)].width = w
    wm.freeze_panes = "B6"
    wm.auto_filter.ref = f"A5:{get_column_letter(len(C.MATRIX_COLUMNS))}{r-1}"

    # ---- Ticket & Billing Codes ----
    wk = wb.create_sheet("Ticket & Billing Codes")
    _title(wk, "Ticket & Billing Codes", "Standardized dispatch and billing codes", len(C.CODE_COLUMNS))
    for j, h in enumerate(C.CODE_COLUMNS, 1):
        wk.cell(row=5, column=j, value=h)
    _hdr(wk, 5, len(C.CODE_COLUMNS))
    r = 6
    for row in C.CODES:
        for j, val in enumerate(row, 1):
            cell = wk.cell(row=r, column=j, value=val)
            cell.font = Font(size=9, bold=(j == 1), color=(BR["primary"] if j == 1 else "000000"))
            cell.border = BORDER; cell.alignment = WRP
            if r % 2 == 1:
                cell.fill = FILL_LIGHT
        r += 1
    for i, w in enumerate([10, 22, 30, 12, 26, 14, 10, 30], 1):
        wk.column_dimensions[get_column_letter(i)].width = w

    # ---- Financial Summary ----
    ws = wb.create_sheet("Financial Summary")
    _title(ws, "Financial Summary", "Headline results by scenario (model outputs under assumptions)", 6)
    for j, h in enumerate(["Metric", "Low", "Expected", "High", "", ""], 1):
        ws.cell(row=5, column=j, value=h)
    _hdr(ws, 5, 4)
    metrics = [
        ("Net fee revenue (Year 1)", "net_fee_revenue"),
        ("Protection-plan margin (Year 1)", "protection_margin"),
        ("Deflection savings", "deflection_savings"),
        ("Year 1 net financial effect", "year1_net"),
        ("Three-year net financial effect", "three_year_net"),
    ]
    r = 6
    for label, key in metrics:
        ws.cell(row=r, column=1, value=label).font = F_BOLD
        for ci, name in enumerate(["Low", "Expected", "High"], 2):
            cell = ws.cell(row=r, column=ci, value=round(SC[name][key]))
            cell.number_format = "$#,##0"; cell.alignment = RGT
            if name == "Expected":
                cell.fill = FILL_REC; cell.font = F_BOLD
            else:
                cell.fill = FILL_CALC
        for c in range(1, 5):
            ws.cell(row=r, column=c).border = BORDER
        r += 1
    # extra single-value metrics
    r += 1
    extra = [
        ("Cost per dispatch (loaded)", R["cost_per_dispatch"], "$#,##0.00"),
        ("Annual customer-caused dispatch cost", R["cust_caused_dispatch_cost"], "$#,##0"),
        ("Cost recovery %", R["cost_recovery_pct"], "0%"),
        ("Implementation payback (months)", R["payback_months"], "0.0"),
        ("One-time implementation cost", R["one_time_cost"], "$#,##0"),
    ]
    for label, val, fmt in extra:
        ws.cell(row=r, column=1, value=label).font = F_NORM
        cell = ws.cell(row=r, column=2, value=round(val, 2)); cell.number_format = fmt
        cell.fill = FILL_CALC; cell.alignment = RGT
        for c in range(1, 3):
            ws.cell(row=r, column=c).border = BORDER
        r += 1
    for i, w in enumerate([36, 14, 14, 14], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.cell(row=r + 1, column=1, value="Full live formulas: Maintenance_Program_Financial_Model.xlsx.").font = F_ITAL

    # ---- KPIs ----
    wki = wb.create_sheet("KPIs & Targets")
    _title(wki, "KPIs & Targets", "Editable targets with red/yellow/green guidance", 4)
    for j, h in enumerate(["KPI", "Target", "Thresholds", "Current (entry)"], 1):
        wki.cell(row=5, column=j, value=h)
    _hdr(wki, 5, 4)
    r = 6
    for k, t, th, _ in KPIS:
        wki.cell(row=r, column=1, value=k).font = F_BOLD
        wki.cell(row=r, column=2, value=t).alignment = CEN
        wki.cell(row=r, column=3, value=th).font = F_NORM
        cur = wki.cell(row=r, column=4); cur.fill = FILL_INPUT
        for c in range(1, 5):
            wki.cell(row=r, column=c).border = BORDER
            wki.cell(row=r, column=c).alignment = WRP if c in (1, 3) else CEN
        r += 1
    for i, w in enumerate([30, 14, 44, 16], 1):
        wki.column_dimensions[get_column_letter(i)].width = w

    # ---- Implementation ----
    wi = wb.create_sheet("Implementation")
    _title(wi, "90-Day Implementation", "Five-phase rollout", 3)
    for j, h in enumerate(["Phase", "Focus", "Window"], 1):
        wi.cell(row=5, column=j, value=h)
    _hdr(wi, 5, 3)
    _rows(wi, 6, PHASES, widths=[12, 60, 16])

    # ---- Waivers ----
    ww = wb.create_sheet("Waivers")
    _title(ww, "Waiver Categories", "Approved waiver categories and approval levels", 3)
    for j, h in enumerate(["Category", "Basis", "Approval"], 1):
        ww.cell(row=5, column=j, value=h)
    _hdr(ww, 5, 3)
    _rows(ww, 6, [(a, b, c) for a, b, c in C.WAIVER_CATEGORIES], widths=[26, 52, 22])

    # ---- Legal Flags ----
    wl = wb.create_sheet("Legal Flags")
    _title(wl, "Legal & Regulatory Review Flags", "Items requiring professional review", 3)
    for j, h in enumerate(["Item", "What to Review", "Owner"], 1):
        wl.cell(row=5, column=j, value=h)
    _hdr(wl, 5, 3)
    _rows(wl, 6, [(a, b, c) for a, b, c in C.LEGAL_FLAGS], widths=[30, 60, 22])

    # ---- Assumptions ----
    wa = wb.create_sheet("Assumptions")
    _title(wa, "Assumptions Register", "Replace with RIVR Tech data before final approval", 3)
    for j, h in enumerate(["Assumption", "Value", "Note"], 1):
        wa.cell(row=5, column=j, value=h)
    _hdr(wa, 5, 3)
    r = 6
    for label, shown, note in C.assumptions_register():
        wa.cell(row=r, column=1, value=label).font = F_NORM
        vc = wa.cell(row=r, column=2, value=shown); vc.fill = FILL_INPUT; vc.alignment = CEN; vc.font = F_BOLD
        wa.cell(row=r, column=3, value=note).font = F_ITAL
        for c in range(1, 4):
            wa.cell(row=r, column=c).border = BORDER
            wa.cell(row=r, column=c).alignment = WRP if c in (1, 3) else CEN
        r += 1
    for i, w in enumerate([34, 14, 56], 1):
        wa.column_dimensions[get_column_letter(i)].width = w

    path = pth("RIVR_Tech_Maintenance_Plan", "RIVR_Tech_Maintenance_Program_Master_Workbook.xlsx")
    wb.save(path)
    print(f"  wrote {path} ({len(wb.sheetnames)} sheets)")


if __name__ == "__main__":
    print("Building consolidated master deliverables...")
    build_manual()
    build_workbook()
    print("Done.")
