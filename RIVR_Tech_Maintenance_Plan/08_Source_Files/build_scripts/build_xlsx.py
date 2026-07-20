# -*- coding: utf-8 -*-
"""Builds all RIVR Tech Excel workbooks with live formulas + color coding."""
import os
import rivr_content as C
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, NamedStyle
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, LineChart, Reference, Series
from openpyxl.comments import Comment
from openpyxl.worksheet.datavalidation import DataValidation

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))


def p(*parts):
    return os.path.join(BASE, *parts)


BRAND = C.BRAND
# Fills
FILL_HEADER = PatternFill("solid", fgColor=BRAND["primary"])
FILL_SUB = PatternFill("solid", fgColor=BRAND["secondary"])
FILL_INPUT = PatternFill("solid", fgColor="FFF3C4")      # yellow-ish: user input
FILL_CALC = PatternFill("solid", fgColor="E3F0F6")       # light blue: calculated
FILL_REC = PatternFill("solid", fgColor="D7F0E7")        # green: recommended assumption
FILL_WARN = PatternFill("solid", fgColor="F6D9CC")       # clay: review/warning
FILL_LIGHT = PatternFill("solid", fgColor=BRAND["light"])
FILL_TITLE = PatternFill("solid", fgColor=BRAND["dark"])

F_WHITE_BOLD = Font(color="FFFFFF", bold=True, size=11, name="Calibri")
F_WHITE_BOLD_LG = Font(color="FFFFFF", bold=True, size=16, name="Calibri")
F_HDR = Font(color="FFFFFF", bold=True, size=10, name="Calibri")
F_BOLD = Font(bold=True, size=10, name="Calibri")
F_NORM = Font(size=10, name="Calibri")
F_ITAL = Font(size=9, italic=True, color="6B7A82", name="Calibri")
F_PRIMARY = Font(bold=True, size=10, color=BRAND["primary"], name="Calibri")

thin = Side(style="thin", color="C9D6DC")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
RIGHT = Alignment(horizontal="right", vertical="center")
WRAP = Alignment(horizontal="left", vertical="top", wrap_text=True)


def style_header_row(ws, row, ncols, fill=FILL_HEADER, font=F_HDR, start=1):
    for c in range(start, start + ncols):
        cell = ws.cell(row=row, column=c)
        cell.fill = fill
        cell.font = font
        cell.alignment = CENTER
        cell.border = BORDER


def title_block(ws, title, subtitle, ncols=6):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncols)
    c = ws.cell(row=1, column=1, value=f"{C.COMPANY_SHORT} — {title}")
    c.fill = FILL_TITLE
    c.font = F_WHITE_BOLD_LG
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 30
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncols)
    c2 = ws.cell(row=2, column=1, value=subtitle)
    c2.fill = FILL_SUB
    c2.font = Font(color="FFFFFF", size=10, italic=True)
    c2.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=ncols)
    c3 = ws.cell(row=3, column=1, value=f"{C.DOC_VERSION}  |  {C.DOC_DATE}  |  {C.COMPANY_LEGAL}  |  NOT LEGAL ADVICE")
    c3.font = F_ITAL


def legend_block(ws, row, ncols=6):
    items = [("User input", FILL_INPUT), ("Calculated", FILL_CALC),
             ("Recommended", FILL_REC), ("Review / warning", FILL_WARN)]
    col = 1
    ws.cell(row=row, column=col, value="LEGEND:").font = F_BOLD
    col = 2
    for label, fill in items:
        cell = ws.cell(row=row, column=col, value=label)
        cell.fill = fill
        cell.font = F_NORM
        cell.border = BORDER
        cell.alignment = CENTER
        col += 1


# ==========================================================================
# WORKBOOK 1 — RESPONSIBILITY MATRIX
# ==========================================================================
def responsibility_matrix():
    wb = Workbook()
    ws = wb.active
    ws.title = "Responsibility Matrix"
    ncols = len(C.MATRIX_COLUMNS)
    title_block(ws, "Trouble-Visit Responsibility Matrix",
                "Scenario-by-scenario classification, billing, documentation, and customer language",
                ncols=ncols)
    legend_block(ws, 4, ncols)

    hdr_row = 6
    for i, h in enumerate(C.MATRIX_COLUMNS, 1):
        ws.cell(row=hdr_row, column=i, value=h)
    style_header_row(ws, hdr_row, ncols)
    ws.row_dimensions[hdr_row].height = 40

    cls_fill = {
        C.CLS_NET: FILL_REC,
        C.CLS_PREM: FILL_INPUT,
        C.CLS_SHARED: FILL_WARN,
        C.CLS_INC: FILL_CALC,
    }
    r = hdr_row + 1
    for row in C.MATRIX:
        for i, val in enumerate(row, 1):
            cell = ws.cell(row=r, column=i, value=val)
            cell.font = F_NORM
            cell.border = BORDER
            cell.alignment = WRAP
            if i == 1:
                cell.font = F_PRIMARY
        # color the classification cell (col 3)
        ws.cell(row=r, column=3).fill = cls_fill.get(row[2], FILL_LIGHT)
        r += 1

    # Column widths
    widths = [26, 12, 20, 12, 16, 16, 26, 22, 12, 14, 12, 18, 34]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    ws.freeze_panes = "B7"
    ws.auto_filter.ref = f"A{hdr_row}:{get_column_letter(ncols)}{r-1}"

    # Summary / key sheet
    ws2 = wb.create_sheet("Classification Key")
    title_block(ws2, "Classification Key & Fee Reference", "How to read the matrix", ncols=4)
    ws2.cell(row=5, column=1, value="Classification").font = F_HDR
    style_header_row(ws2, 5, 4)
    for j, h in enumerate(["Classification", "Customer Charge", "Approval", "Color"], 1):
        ws2.cell(row=5, column=j, value=h)
    style_header_row(ws2, 5, 4)
    keyrows = [
        (C.CLS_NET, "No customer charge", "None", FILL_REC),
        (C.CLS_PREM, "Fee may apply (with documentation)", "Technician/Supervisor", FILL_INPUT),
        (C.CLS_SHARED, "Reduced fee or waiver", "Supervisor", FILL_WARN),
        (C.CLS_INC, "No charge unless management approves", "Manager", FILL_CALC),
    ]
    rr = 6
    for name, charge, appr, fill in keyrows:
        ws2.cell(row=rr, column=1, value=name).font = F_BOLD
        ws2.cell(row=rr, column=2, value=charge).font = F_NORM
        ws2.cell(row=rr, column=3, value=appr).font = F_NORM
        cc = ws2.cell(row=rr, column=4, value="")
        cc.fill = fill
        for c in range(1, 5):
            ws2.cell(row=rr, column=c).border = BORDER
            ws2.cell(row=rr, column=c).alignment = LEFT
        rr += 1
    rr += 1
    ws2.cell(row=rr, column=1, value="Recommended Fee Schedule (Balanced)").font = F_PRIMARY
    rr += 1
    for j, h in enumerate(["Fee Item", "Conservative", "Balanced (Rec.)", "Full Recovery"], 1):
        ws2.cell(row=rr, column=j, value=h)
    style_header_row(ws2, rr, 4)
    rr += 1
    for label, cons, bal, full, note in C.FEE_ITEMS:
        ws2.cell(row=rr, column=1, value=label).font = F_NORM
        ws2.cell(row=rr, column=2, value=f"${cons}").alignment = CENTER
        c = ws2.cell(row=rr, column=3, value=f"${bal}")
        c.fill = FILL_REC
        c.alignment = CENTER
        ws2.cell(row=rr, column=4, value=f"${full}").alignment = CENTER
        for cc in range(1, 5):
            ws2.cell(row=rr, column=cc).border = BORDER
        rr += 1
    for i, w in enumerate([34, 16, 16, 16], 1):
        ws2.column_dimensions[get_column_letter(i)].width = w

    path = p("RIVR_Tech_Maintenance_Plan", "02_Policy_and_SOP",
             "Trouble_Visit_Responsibility_Matrix.xlsx")
    wb.save(path)
    print(f"  wrote {path}")


# ==========================================================================
# WORKBOOK 2 — FINANCIAL MODEL
# ==========================================================================
def financial_model():
    wb = Workbook()

    # ---- INPUTS SHEET (drives everything via named-ish references) ----
    wi = wb.active
    wi.title = "Inputs"
    title_block(wi, "Financial Model — Inputs", "Edit yellow cells. Everything else recalculates.", ncols=5)
    legend_block(wi, 4, 5)
    wi.cell(row=6, column=1, value="Input").font = F_HDR
    for j, h in enumerate(["Input", "Value", "Unit", "Type", "Note"], 1):
        wi.cell(row=6, column=j, value=h)
    style_header_row(wi, 6, 5)

    # Write inputs; value cells at column B, keyed rows. Store row map.
    rowmap = {}
    r = 7
    for key, label, value, unit, is_assump, note in C.FIN_INPUTS:
        wi.cell(row=r, column=1, value=label).font = F_NORM
        vcell = wi.cell(row=r, column=2, value=value)
        vcell.fill = FILL_INPUT if is_assump else FILL_REC
        vcell.font = F_BOLD
        vcell.alignment = CENTER
        if unit == "pct":
            vcell.number_format = "0.0%"
        elif unit == "usd":
            vcell.number_format = "$#,##0.00"
        else:
            vcell.number_format = "#,##0"
        wi.cell(row=r, column=3, value=unit).alignment = CENTER
        wi.cell(row=r, column=4, value=("Assumption" if is_assump else "Recommended")).font = F_NORM
        wi.cell(row=r, column=5, value=note).font = F_ITAL
        for c in range(1, 6):
            wi.cell(row=r, column=c).border = BORDER
        rowmap[key] = r
        r += 1
    for i, w in enumerate([34, 14, 8, 14, 50], 1):
        wi.column_dimensions[get_column_letter(i)].width = w

    def ref(key):
        return f"Inputs!$B${rowmap[key]}"

    # ---- CURRENT STATE ----
    wc = wb.create_sheet("Current State")
    title_block(wc, "Current State (No Program)", "Today's cost of the free-visit model", ncols=3)
    rows = [
        ("Annual trouble tickets", f"={ref('monthly_tickets')}*12", "#,##0"),
        ("Annual dispatches", f"='Current State'!B4*{ref('dispatch_rate')}", "#,##0"),
        ("Remote-resolved tickets", f"='Current State'!B4*{ref('remote_resolution_rate')}", "#,##0"),
        ("Customer-caused dispatches", f"='Current State'!B5*{ref('cust_caused_pct')}", "#,##0"),
        ("Labor per dispatch", f"=({ref('avg_visit_hours')}+{ref('travel_hours')})*{ref('tech_hourly_cost')}", "$#,##0.00"),
        ("Cost per dispatch (loaded)", f"='Current State'!B8+{ref('vehicle_cost')}+{ref('fuel_cost')}+{ref('materials_cost')}+{ref('admin_cost')}", "$#,##0.00"),
        ("Annual dispatch expense", "='Current State'!B5*'Current State'!B9", "$#,##0"),
        ("Annual customer-caused dispatch cost", "='Current State'!B7*'Current State'!B9", "$#,##0"),
    ]
    r = 4
    for label, formula, fmt in rows:
        wc.cell(row=r, column=1, value=label).font = F_BOLD
        cell = wc.cell(row=r, column=2, value=formula)
        cell.number_format = fmt
        cell.fill = FILL_CALC
        cell.font = F_NORM
        cell.alignment = RIGHT
        for c in range(1, 3):
            wc.cell(row=r, column=c).border = BORDER
        r += 1
    wc.column_dimensions["A"].width = 36
    wc.column_dimensions["B"].width = 18
    wc.cell(row=r+1, column=1, value="The customer-caused dispatch cost is what the program aims to partly recover.").font = F_ITAL
    # store references for reuse
    CPD = "'Current State'!$B$9"          # cost per dispatch
    CCDC = "'Current State'!$B$11"        # customer-caused dispatch cost
    ANN_DISP = "'Current State'!$B$5"     # annual dispatches
    ANN_TICK = "'Current State'!$B$4"     # annual tickets
    CC_DISP = "'Current State'!$B$7"      # customer-caused dispatches

    # ---- FEE SCENARIOS ----
    wf = wb.create_sheet("Fee Scenarios")
    title_block(wf, "Fee Scenarios", "Gross and net trouble-visit fee revenue", ncols=3)
    res_share = f"({ref('residential_customers')}/{ref('total_customers')})"
    bus_share = f"({ref('business_customers')}/{ref('total_customers')})"
    frows = [
        ("Billable visits (customer-caused x billable %)", f"={CC_DISP}*{ref('billable_pct')}", "#,##0"),
        ("Residential billable visits", f"='Fee Scenarios'!B4*{res_share}", "#,##0"),
        ("Business billable visits", f"='Fee Scenarios'!B4*{bus_share}", "#,##0"),
        ("Gross fee revenue (visits)", f"='Fee Scenarios'!B5*{ref('res_fee')}+'Fee Scenarios'!B6*{ref('bus_fee')}", "$#,##0"),
        ("Ancillary fees (gross)", f"={ref('ancillary_fee_revenue')}", "$#,##0"),
        ("Total gross fee revenue", "='Fee Scenarios'!B7+'Fee Scenarios'!B8", "$#,##0"),
        ("Less waivers", f"=-'Fee Scenarios'!B9*{ref('waiver_rate')}", "$#,##0"),
        ("Less bad debt", f"=-('Fee Scenarios'!B9+'Fee Scenarios'!B10)*{ref('bad_debt_rate')}", "$#,##0"),
        ("Net billable (after waivers & bad debt)", "='Fee Scenarios'!B9+'Fee Scenarios'!B10+'Fee Scenarios'!B11", "$#,##0"),
        ("Net fee revenue (x collection rate)", f"='Fee Scenarios'!B12*{ref('collection_rate')}", "$#,##0"),
    ]
    r = 4
    for label, formula, fmt in frows:
        wf.cell(row=r, column=1, value=label).font = F_BOLD if "Net fee revenue" in label else F_NORM
        cell = wf.cell(row=r, column=2, value=formula)
        cell.number_format = fmt
        cell.fill = FILL_REC if "Net fee revenue" in label else FILL_CALC
        cell.alignment = RIGHT
        for c in range(1, 3):
            wf.cell(row=r, column=c).border = BORDER
        r += 1
    wf.column_dimensions["A"].width = 40
    wf.column_dimensions["B"].width = 16
    NET_FEE = "'Fee Scenarios'!$B$13"

    # ---- PROTECTION PLAN ----
    wp = wb.create_sheet("Protection Plan")
    title_block(wp, "Protection Plan", "Optional maintenance-protection economics", ncols=4)
    prows = [
        ("Enrolled members (of residential)", f"={ref('residential_customers')}*{ref('protection_enrollment')}", "#,##0"),
        ("Annual plan revenue", f"='Protection Plan'!B4*{ref('protection_price')}*12", "$#,##0"),
        ("Covered service events/year", f"='Protection Plan'!B4*{ref('protection_usage_rate')}", "#,##0"),
        ("Plan service cost", f"='Protection Plan'!B6*{ref('protection_visit_cost')}", "$#,##0"),
        ("Plan admin cost", f"='Protection Plan'!B5*{ref('protection_admin_pct')}", "$#,##0"),
        ("Contribution margin", "='Protection Plan'!B5-'Protection Plan'!B7-'Protection Plan'!B8", "$#,##0"),
        ("Margin per member (annual)", "=IF('Protection Plan'!B4=0,0,'Protection Plan'!B9/'Protection Plan'!B4)", "$#,##0.00"),
        ("Break-even monthly price", f"=({ref('protection_usage_rate')}*{ref('protection_visit_cost')})/(12*(1-{ref('protection_admin_pct')}))", "$#,##0.00"),
        ("Break-even enrollment (members to cover admin at $0 usage)", "=0", "#,##0"),
    ]
    r = 4
    for label, formula, fmt in prows:
        wp.cell(row=r, column=1, value=label).font = F_BOLD if "margin" in label.lower() or "Break-even" in label else F_NORM
        cell = wp.cell(row=r, column=2, value=formula)
        cell.number_format = fmt
        cell.fill = FILL_REC if "Contribution margin" in label else FILL_CALC
        cell.alignment = RIGHT
        for c in range(1, 3):
            wp.cell(row=r, column=c).border = BORDER
        r += 1
    # Price comparison table
    r += 1
    wp.cell(row=r, column=1, value="Price-Point Comparison").font = F_PRIMARY
    r += 1
    for j, h in enumerate(["Monthly Price", "Annual Revenue", "Contribution Margin", "Margin/Member"], 1):
        wp.cell(row=r, column=j, value=h)
    style_header_row(wp, r, 4)
    r += 1
    for price in C.PROTECTION_PRICES:
        res = C.compute_model({"protection_price": price})
        wp.cell(row=r, column=1, value=f"${price:.2f}").alignment = CENTER
        wp.cell(row=r, column=2, value=res["protection_revenue"]).number_format = "$#,##0"
        mc = wp.cell(row=r, column=3, value=res["protection_margin"])
        mc.number_format = "$#,##0"
        wp.cell(row=r, column=4, value=res["protection_margin"]/res["protection_members"]).number_format = "$#,##0.00"
        if abs(price - C.PROTECTION_RECOMMENDED) < 0.01:
            for c in range(1, 5):
                wp.cell(row=r, column=c).fill = FILL_REC
        for c in range(1, 5):
            wp.cell(row=r, column=c).border = BORDER
            wp.cell(row=r, column=c).font = F_NORM
        r += 1
    wp.cell(row=r+1, column=1, value="NOTE: Price-comparison values are static snapshots; the live cells above respond to Inputs.").font = F_ITAL
    wp.cell(row=r+2, column=1, value="REVIEW: Confirm plan is a service plan, NOT insurance (legal/insurance review).").font = Font(size=9, italic=True, color=BRAND["warn"])
    wp.column_dimensions["A"].width = 44
    for col in "BCD":
        wp.column_dimensions[col].width = 18
    PLAN_MARGIN = "'Protection Plan'!$B$9"

    # ---- DEFLECTION + RECOVERY (part of Fee/Exec) computed on Exec sheet ----

    # ---- THREE-YEAR FORECAST ----
    wy = wb.create_sheet("Three-Year Forecast")
    title_block(wy, "Three-Year Forecast", "Net financial effect over three years", ncols=4)
    # Deflection savings
    wy.cell(row=4, column=1, value="Avoided dispatches (deflection)").font = F_NORM
    wy.cell(row=4, column=2, value=f"={ANN_TICK}*{ref('remote_improve_pts')}").number_format = "#,##0"
    wy.cell(row=5, column=1, value="Deflection savings").font = F_NORM
    wy.cell(row=5, column=2, value=f"='Three-Year Forecast'!B4*{CPD}").number_format = "$#,##0"
    wy.cell(row=6, column=1, value="Churn cost").font = F_NORM
    wy.cell(row=6, column=2, value=f"={ref('total_customers')}*{ref('churn_impact_pct')}*{ref('arpu_annual')}").number_format = "$#,##0"
    wy.cell(row=7, column=1, value="Annual recurring net (fees+plan+deflection-churn)").font = F_BOLD
    wy.cell(row=7, column=2, value=f"={NET_FEE}+{PLAN_MARGIN}+'Three-Year Forecast'!B5-'Three-Year Forecast'!B6").number_format = "$#,##0"
    wy.cell(row=8, column=1, value="One-time cost").font = F_NORM
    wy.cell(row=8, column=2, value=f"={ref('implementation_cost')}+{ref('training_cost')}+{ref('billing_config_cost')}").number_format = "$#,##0"
    for rr in range(4, 9):
        wy.cell(row=rr, column=2).fill = FILL_CALC
        for c in range(1, 3):
            wy.cell(row=rr, column=c).border = BORDER
    # Year table
    hr = 10
    for j, h in enumerate(["", "Year 1", "Year 2", "Year 3", "3-Year Total"], 1):
        wy.cell(row=hr, column=j, value=h)
    style_header_row(wy, hr, 5)
    wy.cell(row=hr+1, column=1, value="Recurring net").font = F_NORM
    wy.cell(row=hr+1, column=2, value="='Three-Year Forecast'!B7").number_format = "$#,##0"
    wy.cell(row=hr+1, column=3, value="='Three-Year Forecast'!B7*1.05").number_format = "$#,##0"
    wy.cell(row=hr+1, column=4, value="='Three-Year Forecast'!B7*1.10").number_format = "$#,##0"
    wy.cell(row=hr+2, column=1, value="Less one-time (Year 1)").font = F_NORM
    wy.cell(row=hr+2, column=2, value="=-'Three-Year Forecast'!B8").number_format = "$#,##0"
    wy.cell(row=hr+2, column=3, value=0).number_format = "$#,##0"
    wy.cell(row=hr+2, column=4, value=0).number_format = "$#,##0"
    wy.cell(row=hr+3, column=1, value="Net effect").font = F_BOLD
    for col, L in [(2, "B"), (3, "C"), (4, "D")]:
        cell = wy.cell(row=hr+3, column=col, value=f"=SUM({L}{hr+1}:{L}{hr+2})")
        cell.number_format = "$#,##0"
        cell.fill = FILL_REC
        cell.font = F_BOLD
    wy.cell(row=hr+3, column=5, value=f"=SUM(B{hr+3}:D{hr+3})").number_format = "$#,##0"
    wy.cell(row=hr+3, column=5).fill = FILL_REC
    wy.cell(row=hr+3, column=5).font = F_BOLD
    for rr in range(hr, hr+4):
        for c in range(1, 6):
            wy.cell(row=rr, column=c).border = BORDER
    wy.column_dimensions["A"].width = 40
    for col in "BCDE":
        wy.column_dimensions[col].width = 15
    Y1 = "'Three-Year Forecast'!$B$13"
    Y3TOTAL = "'Three-Year Forecast'!$E$13"
    DEFLECT = "'Three-Year Forecast'!$B$5"
    ANN_REC = "'Three-Year Forecast'!$B$7"
    ONETIME = "'Three-Year Forecast'!$B$8"

    # ---- SENSITIVITY ANALYSIS ----
    wsn = wb.create_sheet("Sensitivity Analysis")
    title_block(wsn, "Sensitivity Analysis", "How key drivers move net fee revenue & plan margin", ncols=6)
    # Table 1: customer-caused % 10-40 vs net fee revenue (static computed)
    def block(ws, top, header, xs, fn, fmt="$#,##0", label=""):
        ws.cell(row=top, column=1, value=header).font = F_PRIMARY
        ws.cell(row=top+1, column=1, value=label).font = F_BOLD
        for j, x in enumerate(xs, 2):
            ws.cell(row=top+1, column=j, value=x).font = F_HDR
            ws.cell(row=top+1, column=j).fill = FILL_SUB
            ws.cell(row=top+1, column=j).alignment = CENTER
        ws.cell(row=top+2, column=1, value="Result").font = F_NORM
        for j, x in enumerate(xs, 2):
            v = fn(x)
            cell = ws.cell(row=top+2, column=j, value=v)
            cell.number_format = fmt
            cell.fill = FILL_CALC
            cell.alignment = CENTER
        for rr in range(top+1, top+3):
            for c in range(1, len(xs)+2):
                ws.cell(row=rr, column=c).border = BORDER

    block(wsn, 5, "1) Customer-caused % of dispatches -> Net fee revenue",
          [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40],
          lambda x: C.compute_model({"cust_caused_pct": x})["net_fee_revenue"], label="Cust-caused %")
    # format headers as pct
    for j in range(2, 9):
        wsn.cell(row=6, column=j).number_format = "0%"

    block(wsn, 10, "2) Residential visit fee ($50-$100) -> Net fee revenue",
          [50, 60, 70, 75, 80, 90, 100],
          lambda x: C.compute_model({"res_fee": x, "bus_fee": x+50})["net_fee_revenue"], label="Res fee $")

    block(wsn, 15, "3) Protection-plan enrollment (5%-30%) -> Plan contribution margin",
          [0.05, 0.10, 0.15, 0.20, 0.25, 0.30],
          lambda x: C.compute_model({"protection_enrollment": x})["protection_margin"], label="Enrollment %")
    for j in range(2, 8):
        wsn.cell(row=16, column=j).number_format = "0%"

    block(wsn, 20, "4) Remote-resolution improvement (5%-20%) -> Deflection savings",
          [0.05, 0.08, 0.10, 0.12, 0.15, 0.20],
          lambda x: C.compute_model({"remote_improve_pts": x})["deflection_savings"], label="Improvement pts")
    for j in range(2, 8):
        wsn.cell(row=21, column=j).number_format = "0%"
    wsn.column_dimensions["A"].width = 20
    for col in "BCDEFGH":
        wsn.column_dimensions[col].width = 12
    wsn.cell(row=25, column=1, value="Sensitivity tables are computed snapshots to illustrate driver impact; the Inputs sheet drives the live model.").font = F_ITAL

    # ---- KPI DEFINITIONS ----
    wk = wb.create_sheet("KPI Definitions")
    title_block(wk, "KPI Definitions", "How each metric is defined and measured", ncols=3)
    for j, h in enumerate(["KPI", "Definition", "Source"], 1):
        wk.cell(row=5, column=j, value=h)
    style_header_row(wk, 5, 3)
    kpis = [
        ("Remote-resolution %", "Tickets closed without dispatch / total tickets.", "Ticketing"),
        ("Customer-premises issue %", "Dispatches classified as customer-premises / dispatches.", "Field disposition"),
        ("Billable visits", "Customer-premises visits with documented findings & disclosure.", "Billing"),
        ("Fees assessed / collected / waived", "Gross fees, collected fees, and waived fees.", "Billing / AR"),
        ("Waiver %", "Waived fees / assessed fees.", "Billing"),
        ("Dispute rate / approved disputes", "Disputes / billable visits; approved / disputes.", "CX"),
        ("Repeat visits (7/14/30 days)", "Repeat dispatches within window / dispatches.", "Ticketing"),
        ("Cost per dispatch", "Loaded labor + vehicle + fuel + materials + admin.", "Finance"),
        ("Avoided truck rolls", "Deflected dispatches from improved remote resolution.", "Ops"),
        ("Protection enrollment / revenue / cost", "Members, plan revenue, and plan service cost.", "Billing"),
        ("Policy-related churn", "Churn attributable to the policy.", "CX / Finance"),
        ("Technician coding accuracy", "Correctly coded tickets / audited tickets.", "QA"),
        ("Support disclosure compliance", "Tickets with proper advance disclosure / eligible.", "QA"),
    ]
    r = 6
    for k, d, s in kpis:
        wk.cell(row=r, column=1, value=k).font = F_BOLD
        wk.cell(row=r, column=2, value=d).font = F_NORM
        wk.cell(row=r, column=3, value=s).font = F_NORM
        for c in range(1, 4):
            wk.cell(row=r, column=c).border = BORDER
            wk.cell(row=r, column=c).alignment = WRAP
        r += 1
    wk.column_dimensions["A"].width = 30
    wk.column_dimensions["B"].width = 55
    wk.column_dimensions["C"].width = 18

    # ---- DATA NEEDED ----
    wd = wb.create_sheet("Data Needed")
    title_block(wd, "Data Needed", "Ten RIVR Tech data points to replace assumptions", ncols=3)
    for j, h in enumerate(["Data Point", "Why It Matters", "Source"], 1):
        wd.cell(row=5, column=j, value=h)
    style_header_row(wd, 5, 3)
    r = 6
    for name, why, src in C.DATA_NEEDED:
        wd.cell(row=r, column=1, value=name).font = F_BOLD
        wd.cell(row=r, column=2, value=why).font = F_NORM
        wd.cell(row=r, column=3, value=src).font = F_NORM
        for c in range(1, 4):
            wd.cell(row=r, column=c).border = BORDER
            wd.cell(row=r, column=c).alignment = WRAP
        r += 1
    wd.column_dimensions["A"].width = 30
    wd.column_dimensions["B"].width = 50
    wd.column_dimensions["C"].width = 22

    # ---- EXECUTIVE DASHBOARD (first sheet visually) ----
    we = wb.create_sheet("Executive Dashboard", 0)
    title_block(we, "Executive Dashboard", "Headline results — Expected scenario (live)", ncols=6)
    legend_block(we, 4, 6)
    # KPI tiles as labeled cells
    tiles = [
        ("Cost per dispatch", CPD, "$#,##0.00"),
        ("Annual dispatch expense", "'Current State'!$B$10", "$#,##0"),
        ("Customer-caused dispatch cost", CCDC, "$#,##0"),
        ("Net fee revenue (Yr 1)", NET_FEE, "$#,##0"),
        ("Protection margin (Yr 1)", PLAN_MARGIN, "$#,##0"),
        ("Deflection savings", DEFLECT, "$#,##0"),
        ("Year 1 net effect", Y1, "$#,##0"),
        ("Three-year net effect", Y3TOTAL, "$#,##0"),
    ]
    r = 6
    col = 1
    for i, (label, refcell, fmt) in enumerate(tiles):
        lc = we.cell(row=r, column=col, value=label)
        lc.font = F_WHITE_BOLD
        lc.fill = FILL_SUB
        lc.alignment = CENTER
        lc.border = BORDER
        vc = we.cell(row=r+1, column=col, value=f"={refcell}")
        vc.number_format = fmt
        vc.font = Font(bold=True, size=14, color=BRAND["primary"])
        vc.fill = FILL_CALC
        vc.alignment = CENTER
        vc.border = BORDER
        we.merge_cells(start_row=r, start_column=col, end_row=r, end_column=col+1)
        we.merge_cells(start_row=r+1, start_column=col, end_row=r+2, end_column=col+1)
        col += 2
        if col > 6:
            col = 1
            r += 4
    for i in range(1, 7):
        we.column_dimensions[get_column_letter(i)].width = 17

    # Cost-recovery % callout
    rr = r + 4
    we.cell(row=rr, column=1, value="Cost recovery of customer-caused dispatch cost:").font = F_BOLD
    crc = we.cell(row=rr, column=3, value=f"=({NET_FEE}+{PLAN_MARGIN})/{CCDC}")
    crc.number_format = "0%"
    crc.font = Font(bold=True, size=13, color=BRAND["good"])
    crc.fill = FILL_REC
    crc.border = BORDER

    # ---- Data area for charts on dashboard ----
    dchart_row = rr + 3
    we.cell(row=dchart_row, column=1, value="Chart Data (Scenario comparison)").font = F_PRIMARY
    hdr = dchart_row + 1
    for j, h in enumerate(["Scenario", "Net Fees", "Plan Margin", "Deflection", "Year 1 Net", "3-Yr Net"], 1):
        we.cell(row=hdr, column=j, value=h)
    style_header_row(we, hdr, 6)
    rdata = hdr + 1
    for name in ["Low", "Expected", "High"]:
        s = C.scenario_results()[name]
        we.cell(row=rdata, column=1, value=name).font = F_BOLD
        we.cell(row=rdata, column=2, value=round(s["net_fee_revenue"])).number_format = "$#,##0"
        we.cell(row=rdata, column=3, value=round(s["protection_margin"])).number_format = "$#,##0"
        we.cell(row=rdata, column=4, value=round(s["deflection_savings"])).number_format = "$#,##0"
        we.cell(row=rdata, column=5, value=round(s["year1_net"])).number_format = "$#,##0"
        we.cell(row=rdata, column=6, value=round(s["three_year_net"])).number_format = "$#,##0"
        for c in range(1, 7):
            we.cell(row=rdata, column=c).border = BORDER
        rdata += 1

    # Chart 1: Net revenue by scenario (Year 1 net + 3yr)
    chart1 = BarChart()
    chart1.title = "Net Financial Effect by Scenario"
    chart1.type = "col"
    chart1.style = 10
    data = Reference(we, min_col=5, min_row=hdr, max_col=6, max_row=rdata-1)
    cats = Reference(we, min_col=1, min_row=hdr+1, max_row=rdata-1)
    chart1.add_data(data, titles_from_data=True)
    chart1.set_categories(cats)
    chart1.y_axis.numFmt = '$#,##0'
    chart1.height = 7.5
    chart1.width = 13
    we.add_chart(chart1, f"A{rdata+2}")

    # Chart 2: Revenue components (Expected)
    chart2 = BarChart()
    chart2.title = "Program Revenue Components by Scenario"
    chart2.type = "col"
    chart2.style = 12
    data2 = Reference(we, min_col=2, min_row=hdr, max_col=4, max_row=rdata-1)
    chart2.add_data(data2, titles_from_data=True)
    chart2.set_categories(cats)
    chart2.y_axis.numFmt = '$#,##0'
    chart2.height = 7.5
    chart2.width = 13
    we.add_chart(chart2, f"H{rdata+2}")

    # Protection break-even chart data
    pbe_row = rdata + 20
    we.cell(row=pbe_row, column=1, value="Protection Plan — Margin by Price Point").font = F_PRIMARY
    for j, h in enumerate(["Price", "Contribution Margin"], 1):
        we.cell(row=pbe_row+1, column=j, value=h)
    style_header_row(we, pbe_row+1, 2)
    pr = pbe_row + 2
    for price in C.PROTECTION_PRICES:
        res = C.compute_model({"protection_price": price})
        we.cell(row=pr, column=1, value=f"${price:.2f}").font = F_BOLD
        we.cell(row=pr, column=2, value=round(res["protection_margin"])).number_format = "$#,##0"
        for c in range(1, 3):
            we.cell(row=pr, column=c).border = BORDER
        pr += 1
    chart3 = BarChart()
    chart3.title = "Protection Plan Margin by Price"
    chart3.type = "col"
    chart3.style = 11
    d3 = Reference(we, min_col=2, min_row=pbe_row+1, max_row=pr-1)
    c3 = Reference(we, min_col=1, min_row=pbe_row+2, max_row=pr-1)
    chart3.add_data(d3, titles_from_data=True)
    chart3.set_categories(c3)
    chart3.y_axis.numFmt = '$#,##0'
    chart3.height = 7
    chart3.width = 12
    we.add_chart(chart3, f"A{pr+2}")

    path = p("RIVR_Tech_Maintenance_Plan", "03_Financial_Model",
             "Maintenance_Program_Financial_Model.xlsx")
    wb.save(path)
    print(f"  wrote {path}")


# ==========================================================================
# WORKBOOK 3 — 90-DAY IMPLEMENTATION TRACKER
# ==========================================================================
def implementation_tracker():
    wb = Workbook()
    ws = wb.active
    ws.title = "90-Day Tracker"
    cols = ["Task", "Workstream", "Phase", "Owner", "Start", "Due", "Dependency",
            "Status", "Risk", "Mitigation", "Exec Decision Required"]
    title_block(ws, "90-Day Implementation Tracker",
                "Five phases from policy to full billing and optimization", ncols=len(cols))
    legend_block(ws, 4, len(cols))
    hr = 6
    for j, h in enumerate(cols, 1):
        ws.cell(row=hr, column=j, value=h)
    style_header_row(ws, hr, len(cols))
    ws.row_dimensions[hr].height = 30

    tasks = [
        # Task, Workstream, Phase, Owner, Start, Due, Dependency, Status, Risk, Mitigation, ExecDecision
        ("Finalize policy draft", "Policy", "1", "Policy Lead", "Day 1", "Day 10", "-", "Not started", "Med", "Reuse this draft; legal review", "Yes — approve posture"),
        ("Validate financial model with real data", "Finance", "1", "Finance", "Day 1", "Day 12", "Data pull", "Not started", "Med", "Replace 10 assumptions", "Yes — approve fees"),
        ("Legal & regulatory review (NC)", "Legal", "1", "General Counsel", "Day 3", "Day 20", "Policy draft", "Not started", "High", "Engage counsel early", "Yes — scope"),
        ("Insurance characterization (plan)", "Legal", "1", "GC / Insurance", "Day 3", "Day 20", "Plan design", "Not started", "High", "Confirm not insurance", "Yes — plan launch"),
        ("Design ticket & billing codes", "Systems", "1", "IT / Billing", "Day 5", "Day 25", "Policy", "Not started", "Med", "Use code list in SOP", "No"),
        ("Configure billing system", "Systems", "1", "IT / Billing", "Day 15", "Day 35", "Codes", "Not started", "High", "Vendor quote; test env", "No"),
        ("Build portal / e-acknowledgment", "Systems", "1", "IT", "Day 15", "Day 40", "Legal (E-SIGN)", "Not started", "Med", "UETA/E-SIGN review", "No"),
        ("Develop training materials", "Training", "2", "Enablement", "Day 20", "Day 40", "Policy final", "Not started", "Low", "Deck + QRG + assessment ready", "No"),
        ("Train all employee roles", "Training", "2", "Enablement", "Day 40", "Day 55", "Materials", "Not started", "Med", "Passing score 80%", "No"),
        ("Launch 60-day customer education", "Comms", "2", "Marketing", "Day 35", "Day 95", "Legal wording", "Not started", "Med", "Warm, local messaging", "No"),
        ("Publish website policy & FAQs", "Comms", "2", "Marketing", "Day 40", "Day 50", "Legal wording", "Not started", "Low", "Use comms package", "No"),
        ("Begin 30-day warning-only period", "Ops", "3", "Support Ops", "Day 55", "Day 85", "Training done", "Not started", "Med", "Disclose, don't bill", "Yes — grace period"),
        ("Apply first-incident courtesy waivers", "Ops", "3", "Supervisors", "Day 55", "Ongoing", "Warning period", "Not started", "Low", "Track waivers", "No"),
        ("Dry-run dispute & waiver workflows", "CX", "3", "CX Lead", "Day 60", "Day 80", "Systems", "Not started", "Med", "Simulate disputes", "No"),
        ("Go-live: full billing implementation", "Ops", "4", "Support Ops", "Day 85", "Day 90", "All above", "Not started", "High", "Exec sign-off gate", "Yes — go/no-go"),
        ("Monitor KPIs & coding accuracy", "Quality", "4", "QA", "Day 85", "Ongoing", "Go-live", "Not started", "Med", "KPI dashboard", "No"),
        ("30-day post-launch review", "Exec", "5", "COO", "Day 115", "Day 120", "Go-live", "Not started", "Low", "Optimize fees/waivers", "Yes — adjust"),
        ("Optimize remote-resolution playbooks", "Ops", "5", "Support Ops", "Day 100", "Ongoing", "KPIs", "Not started", "Low", "Raise deflection", "No"),
    ]
    r = hr + 1
    status_fill = {"Not started": FILL_LIGHT, "In progress": FILL_INPUT, "Complete": FILL_REC, "Blocked": FILL_WARN}
    risk_fill = {"Low": FILL_REC, "Med": FILL_INPUT, "High": FILL_WARN}
    for t in tasks:
        for j, val in enumerate(t, 1):
            cell = ws.cell(row=r, column=j, value=val)
            cell.font = F_NORM
            cell.border = BORDER
            cell.alignment = WRAP
            if j == 1:
                cell.font = F_PRIMARY
        ws.cell(row=r, column=8).fill = status_fill.get(t[7], FILL_LIGHT)
        ws.cell(row=r, column=9).fill = risk_fill.get(t[8], FILL_LIGHT)
        if str(t[10]).lower().startswith("yes"):
            ws.cell(row=r, column=11).fill = FILL_WARN
        r += 1
    widths = [30, 12, 7, 16, 9, 9, 16, 13, 7, 26, 22]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A7"
    ws.auto_filter.ref = f"A{hr}:{get_column_letter(len(cols))}{r-1}"

    # Data validation dropdowns for Status
    dv = DataValidation(type="list", formula1='"Not started,In progress,Complete,Blocked"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"H{hr+1}:H{r-1}")
    dvr = DataValidation(type="list", formula1='"Low,Med,High"', allow_blank=True)
    ws.add_data_validation(dvr)
    dvr.add(f"I{hr+1}:I{r-1}")

    # Phase summary sheet
    ws2 = wb.create_sheet("Phase Overview")
    title_block(ws2, "Implementation Phases", "Five-phase rollout", ncols=3)
    for j, h in enumerate(["Phase", "Focus", "Window"], 1):
        ws2.cell(row=5, column=j, value=h)
    style_header_row(ws2, 5, 3)
    phases = [
        ("Phase 1", "Policy, financial validation, legal review, and system design", "Days 1–40"),
        ("Phase 2", "Employee training and customer education", "Days 20–95"),
        ("Phase 3", "30-day warning and courtesy-waiver period", "Days 55–85"),
        ("Phase 4", "Full billing implementation", "Days 85–90"),
        ("Phase 5", "Performance review and optimization", "Days 90–120+"),
    ]
    r = 6
    for ph, focus, win in phases:
        ws2.cell(row=r, column=1, value=ph).font = F_BOLD
        ws2.cell(row=r, column=2, value=focus).font = F_NORM
        ws2.cell(row=r, column=3, value=win).font = F_NORM
        for c in range(1, 4):
            ws2.cell(row=r, column=c).border = BORDER
            ws2.cell(row=r, column=c).alignment = WRAP
        r += 1
    ws2.column_dimensions["A"].width = 12
    ws2.column_dimensions["B"].width = 60
    ws2.column_dimensions["C"].width = 16

    path = p("RIVR_Tech_Maintenance_Plan", "06_Implementation",
             "90_Day_Implementation_Tracker.xlsx")
    wb.save(path)
    print(f"  wrote {path}")


# ==========================================================================
# WORKBOOK 4 — KPI DASHBOARD
# ==========================================================================
def kpi_dashboard():
    wb = Workbook()
    ws = wb.active
    ws.title = "KPI Dashboard"
    cols = ["KPI", "Target", "Green (>=)", "Yellow", "Red (<=)", "Current (entry)", "Status"]
    title_block(ws, "Maintenance Program KPI Dashboard",
                "Editable targets with red/yellow/green thresholds", ncols=len(cols))
    legend_block(ws, 4, len(cols))
    hr = 6
    for j, h in enumerate(cols, 1):
        ws.cell(row=hr, column=j, value=h)
    style_header_row(ws, hr, len(cols))

    # kpi, target, green, yellow_low, red, unit(fmt), higher_is_better
    kpis = [
        ("Total trouble tickets (monthly)", 1850, None, None, None, "#,##0", None),
        ("Total dispatches (monthly)", 700, None, None, None, "#,##0", None),
        ("Remote-resolution %", 0.67, 0.67, 0.60, 0.55, "0%", True),
        ("Customer-premises issue %", 0.30, None, None, None, "0%", None),
        ("Billable visits (monthly)", 130, None, None, None, "#,##0", None),
        ("Fees assessed (monthly)", 10000, None, None, None, "$#,##0", None),
        ("Fees collected (monthly)", 8000, None, None, None, "$#,##0", None),
        ("Fees waived (monthly)", 1500, None, None, None, "$#,##0", None),
        ("Waiver %", 0.15, 0.20, 0.30, 0.40, "0%", False),
        ("Disputes (monthly)", 12, None, None, None, "#,##0", None),
        ("Approved disputes %", 0.30, None, None, None, "0%", None),
        ("Repeat visits within 7 days %", 0.04, 0.04, 0.07, 0.10, "0%", False),
        ("Repeat visits within 14 days %", 0.06, 0.06, 0.10, 0.14, "0%", False),
        ("Repeat visits within 30 days %", 0.09, 0.09, 0.14, 0.18, "0%", False),
        ("Average visit duration (hr)", 0.75, None, None, None, "0.00", None),
        ("Cost per dispatch", 130, None, None, None, "$#,##0", None),
        ("Avoided truck rolls (monthly)", 90, 90, 60, 40, "#,##0", True),
        ("Protection-plan enrollment %", 0.10, 0.10, 0.06, 0.04, "0%", True),
        ("Protection-plan revenue (monthly)", 14000, None, None, None, "$#,##0", None),
        ("Protection-plan cost (monthly)", 4000, None, None, None, "$#,##0", None),
        ("Complaints (monthly)", 15, 15, 30, 45, "#,##0", False),
        ("Policy-related churn %", 0.003, 0.003, 0.006, 0.010, "0.0%", False),
        ("Customer satisfaction (CSAT)", 0.90, 0.90, 0.85, 0.80, "0%", True),
        ("Technician coding accuracy %", 0.95, 0.95, 0.90, 0.85, "0%", True),
        ("Support disclosure compliance %", 0.98, 0.98, 0.93, 0.88, "0%", True),
    ]
    r = hr + 1
    for name, target, green, yellow, red, fmt, hib in kpis:
        ws.cell(row=r, column=1, value=name).font = F_BOLD
        tc = ws.cell(row=r, column=2, value=target)
        tc.number_format = fmt
        tc.fill = FILL_INPUT
        tc.alignment = CENTER
        for col, val in [(3, green), (4, yellow), (5, red)]:
            cc = ws.cell(row=r, column=col, value=val)
            cc.number_format = fmt
            cc.alignment = CENTER
            cc.font = F_NORM
        # current entry cell (user fills)
        cur = ws.cell(row=r, column=6, value=None)
        cur.fill = FILL_INPUT
        cur.number_format = fmt
        cur.alignment = CENTER
        # status formula (only where thresholds + direction defined)
        st = ws.cell(row=r, column=7)
        if green is not None and hib is not None:
            gcell = f"C{r}"
            rcell = f"E{r}"
            curcell = f"F{r}"
            if hib:
                st.value = (f'=IF({curcell}="","—",IF({curcell}>={gcell},"GREEN",'
                            f'IF({curcell}<={rcell},"RED","YELLOW")))')
            else:
                st.value = (f'=IF({curcell}="","—",IF({curcell}<={gcell},"GREEN",'
                            f'IF({curcell}>={rcell},"RED","YELLOW")))')
        else:
            st.value = "—"
        st.alignment = CENTER
        st.font = F_BOLD
        for c in range(1, len(cols)+1):
            ws.cell(row=r, column=c).border = BORDER
        r += 1

    # Conditional formatting for status column
    from openpyxl.formatting.rule import CellIsRule
    green_fill = PatternFill("solid", fgColor="C6EFCE")
    yellow_fill = PatternFill("solid", fgColor="FFEB9C")
    red_fill = PatternFill("solid", fgColor="FFC7CE")
    rng = f"G{hr+1}:G{r-1}"
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"GREEN"'], fill=green_fill))
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"YELLOW"'], fill=yellow_fill))
    ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"RED"'], fill=red_fill))

    widths = [34, 12, 12, 12, 12, 14, 12]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A7"
    ws.cell(row=r+1, column=1, value="Enter the Current value (yellow) each period; Status auto-colors where a direction is defined. Some volume metrics are informational (no threshold).").font = F_ITAL

    # Waiver tracking sheet
    ws2 = wb.create_sheet("Waiver Tracking")
    title_block(ws2, "Waiver Tracking Log", "Track waivers by employee, technician, reason, area, type, and amount", ncols=8)
    wcols = ["Date", "Employee", "Technician", "Reason", "Service Area", "Customer Type", "Fee Amount", "Supervisor"]
    for j, h in enumerate(wcols, 1):
        ws2.cell(row=5, column=j, value=h)
    style_header_row(ws2, 5, 8)
    # a few sample rows + blank rows
    sample = [
        ("[date]", "[name]", "[tech]", "First-time courtesy", "[area]", "Residential", 75, "[sup]"),
        ("[date]", "[name]", "[tech]", "Hardship", "[area]", "Residential", 75, "[mgr]"),
        ("[date]", "[name]", "[tech]", "Documentation error", "[area]", "Business", 125, "[sup]"),
    ]
    r = 6
    for row in sample + [("",)*8 for _ in range(12)]:
        for j, val in enumerate(row, 1):
            cell = ws2.cell(row=r, column=j, value=val if val != "" else None)
            cell.border = BORDER
            cell.font = F_NORM
            cell.alignment = CENTER
            if j == 7 and isinstance(val, (int, float)):
                cell.number_format = "$#,##0"
        r += 1
    dvw = DataValidation(type="list",
                         formula1='"' + ",".join(a for a, _, _ in C.WAIVER_CATEGORIES) + '"',
                         allow_blank=True)
    ws2.add_data_validation(dvw)
    dvw.add(f"D6:D{r-1}")
    dvt = DataValidation(type="list", formula1='"Residential,Business"', allow_blank=True)
    ws2.add_data_validation(dvt)
    dvt.add(f"F6:F{r-1}")
    for i, w in enumerate([12, 16, 16, 22, 16, 14, 12, 14], 1):
        ws2.column_dimensions[get_column_letter(i)].width = w
    ws2.cell(row=r+1, column=1, value="Totals:").font = F_BOLD
    ws2.cell(row=r+1, column=7, value=f"=SUM(G6:G{r-1})").number_format = "$#,##0"
    ws2.cell(row=r+1, column=7).font = F_BOLD

    path = p("RIVR_Tech_Maintenance_Plan", "06_Implementation",
             "Maintenance_Program_KPI_Dashboard.xlsx")
    wb.save(path)
    print(f"  wrote {path}")


if __name__ == "__main__":
    print("Building Excel workbooks...")
    responsibility_matrix()
    financial_model()
    implementation_tracker()
    kpi_dashboard()
    print("Excel workbooks complete.")
