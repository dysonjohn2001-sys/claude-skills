# -*- coding: utf-8 -*-
"""Builds the RIVR Tech Blanket Protection Plan financial model (11 sheets, live formulas)."""
import os
import blanket_content as C
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.formatting.rule import CellIsRule

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(BASE, "RIVR_Tech_Blanket_Protection_Analysis", "01_Financial_Model",
                   "RIVR_Tech_Blanket_Protection_Financial_Model.xlsx")

BRAND = {"primary": "0B3D5C", "secondary": "1B87B5", "accent": "36B39A",
         "dark": "10222E", "light": "EAF3F7", "warn": "C0562B", "good": "2E7D5B",
         "gray": "6B7A82", "white": "FFFFFF"}
F_HDR = Font(color="FFFFFF", bold=True, size=10)
F_TITLE = Font(color="FFFFFF", bold=True, size=16)
F_SUB = Font(color="FFFFFF", italic=True, size=10)
F_BOLD = Font(bold=True, size=10)
F_NORM = Font(size=10)
F_ITAL = Font(size=9, italic=True, color="6B7A82")
F_PRIM = Font(bold=True, size=11, color=BRAND["primary"])
FILL_HDR = PatternFill("solid", fgColor=BRAND["primary"])
FILL_SUB = PatternFill("solid", fgColor=BRAND["secondary"])
FILL_TITLE = PatternFill("solid", fgColor=BRAND["dark"])
FILL_INPUT = PatternFill("solid", fgColor="FFF3C4")
FILL_CALC = PatternFill("solid", fgColor="E3F0F6")
FILL_REC = PatternFill("solid", fgColor="D7F0E7")
FILL_WARN = PatternFill("solid", fgColor="F6D9CC")
FILL_LIGHT = PatternFill("solid", fgColor=BRAND["light"])
thin = Side(style="thin", color="C9D6DC")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
CEN = Alignment(horizontal="center", vertical="center", wrap_text=True)
RGT = Alignment(horizontal="right", vertical="center")
WRP = Alignment(horizontal="left", vertical="top", wrap_text=True)
USD = "$#,##0"
USD2 = "$#,##0.00"
PCT = "0.0%"
PCT0 = "0%"
NUM = "#,##0"


def hdr(ws, row, ncols, start=1, fill=FILL_HDR, font=F_HDR):
    for c in range(start, start + ncols):
        cell = ws.cell(row=row, column=c)
        cell.fill = fill; cell.font = font; cell.alignment = CEN; cell.border = BORDER


def title(ws, t, sub, ncols=6):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=ncols)
    c = ws.cell(row=1, column=1, value=f"{C.COMPANY_SHORT} — {t}")
    c.fill = FILL_TITLE; c.font = F_TITLE
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 28
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=ncols)
    c2 = ws.cell(row=2, column=1, value=sub); c2.fill = FILL_SUB; c2.font = F_SUB
    c2.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=ncols)
    ws.cell(row=3, column=1,
            value=f"{C.DOC_VERSION} | {C.DOC_DATE} | {C.COMPANY_LEGAL} | NOT LEGAL ADVICE").font = F_ITAL


def legend(ws, row, ncols=6):
    ws.cell(row=row, column=1, value="LEGEND:").font = F_BOLD
    for i, (lab, fill) in enumerate([("User input", FILL_INPUT), ("Calculated", FILL_CALC),
                                     ("Recommended", FILL_REC), ("Warning", FILL_WARN)], 2):
        cell = ws.cell(row=row, column=i, value=lab)
        cell.fill = fill; cell.font = F_NORM; cell.border = BORDER; cell.alignment = CEN


def put(ws, r, c, val, fmt=None, fill=None, font=None, align=None, border=True):
    cell = ws.cell(row=r, column=c, value=val)
    if fmt: cell.number_format = fmt
    if fill: cell.fill = fill
    cell.font = font or F_NORM
    if align: cell.alignment = align
    if border: cell.border = BORDER
    return cell


def build():
    wb = Workbook()

    # ================= ASSUMPTIONS =================
    wa = wb.active
    wa.title = "Assumptions"
    title(wa, "Assumptions", "Edit yellow cells — all scenarios recalculate from here.", 5)
    legend(wa, 4, 5)
    for j, h in enumerate(["Assumption", "Value", "Unit", "Type", "Note"], 1):
        wa.cell(row=6, column=j, value=h)
    hdr(wa, 6, 5)
    rowmap = {}
    r = 7
    for key, label, value, unit, is_assump, note in C.A_LIST:
        put(wa, r, 1, label, font=F_NORM, align=WRP)
        fmt = PCT if unit == "pct" else (USD2 if unit == "usd" else NUM)
        vc = put(wa, r, 2, value, fmt=fmt, fill=(FILL_INPUT if is_assump else FILL_REC),
                 font=F_BOLD, align=CEN)
        put(wa, r, 3, unit, align=CEN)
        put(wa, r, 4, "Assumption" if is_assump else "Given/Scenario")
        put(wa, r, 5, note, font=F_ITAL, align=WRP)
        rowmap[key] = r
        r += 1
    # cost-per-call computed cell
    put(wa, r, 1, "Cost per covered call (loaded, computed)", font=F_BOLD)
    def ref(k): return f"Assumptions!$B${rowmap[k]}"
    CPC = (f"(({ref('tech_labor_hours')}+{ref('dispatch_hours')})*{ref('tech_rate')}"
           f"+{ref('vehicle_cost')}+{ref('fuel_cost')}+{ref('materials_cost')})*(1+{ref('repeat_dispatch')})")
    put(wa, r, 2, f"={CPC}", fmt=USD2, fill=FILL_CALC, font=F_BOLD, align=CEN)
    cpc_cell = f"Assumptions!$B${r}"
    rowmap["_cpc"] = r
    for i, w in enumerate([40, 14, 8, 16, 48], 1):
        wa.column_dimensions[get_column_letter(i)].width = w
    wa.freeze_panes = "A7"

    # helper formula builders (reference Assumptions)
    def per_member_contrib(price_ref, util_ref):
        # price_ref/util_ref are formula fragments or cell refs
        return (f"({price_ref}*12 - {util_ref}*{cpc_cell} - {util_ref}*{ref('cc_handling')} "
                f"- {ref('billing_cost_yr')} - {price_ref}*12*{ref('bad_debt')})")

    # ================= SUBSCRIBER FORECAST =================
    ws = wb.create_sheet("Subscriber Forecast")
    title(ws, "Subscriber Forecast", "Modeled subscriber levels + 5-year organic growth", 4)
    put(ws, 5, 1, "Modeled subscriber levels", font=F_PRIM, border=False)
    for j, h in enumerate(["Subscriber Level", "Monthly Plan Rev @ $3.99 (100%)", "Monthly Plan Rev @ $4.99 (100%)"], 1):
        ws.cell(row=6, column=j, value=h)
    hdr(ws, 6, 3)
    rr = 7
    for lvl in C.SUB_LEVELS:
        put(ws, rr, 1, lvl, fmt=NUM, fill=FILL_INPUT, font=F_BOLD, align=CEN)
        put(ws, rr, 2, f"=A{rr}*{ref('price_a')}", fmt=USD, fill=FILL_CALC, align=RGT)
        put(ws, rr, 3, f"=A{rr}*{ref('price_b')}", fmt=USD, fill=FILL_CALC, align=RGT)
        rr += 1
    # 5-year growth from current_subs
    rr += 1
    put(ws, rr, 1, "5-Year organic growth (from current subscribers)", font=F_PRIM, border=False)
    rr += 1
    for j, h in enumerate(["Year", "Subscribers", "@ $3.99 100% Annual", "@ $4.99 100% Annual"], 1):
        ws.cell(row=rr, column=j, value=h)
    hdr(ws, rr, 4)
    start = rr + 1
    for y in range(5):
        rrow = start + y
        if y == 0:
            subf = f"={ref('current_subs')}"
        else:
            subf = f"=B{rrow-1}*(1+{ref('monthly_growth')})^12"
        put(ws, rrow, 1, y + 1, align=CEN)
        put(ws, rrow, 2, subf, fmt=NUM, fill=FILL_CALC, align=RGT)
        put(ws, rrow, 3, f"=B{rrow}*{ref('price_a')}*12", fmt=USD, fill=FILL_CALC, align=RGT)
        put(ws, rrow, 4, f"=B{rrow}*{ref('price_b')}*12", fmt=USD, fill=FILL_CALC, align=RGT)
    for i, w in enumerate([22, 20, 26, 26], 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    # ================= SCENARIO A / B =================
    def scenario_sheet(name, price_key, price_label):
        s = wb.create_sheet(name)
        title(s, f"Scenario {name[-1]} — {price_label}/month", "Per-member economics + mandatory totals across subscriber levels", 6)
        # per-member block
        put(s, 5, 1, "Per-enrolled-member annual economics (at expected utilization)", font=F_PRIM, border=False)
        pr = ref(price_key)
        ue = ref("util_expected")
        rows = [
            ("Plan revenue / member", f"={pr}*12", USD2),
            ("Covered service-call expense / member", f"={ue}*{cpc_cell}", USD2),
            ("Call-center expense / member", f"={ue}*{ref('cc_handling')}", USD2),
            ("Billing & admin / member", f"={ref('billing_cost_yr')}", USD2),
            ("Bad debt / member", f"={pr}*12*{ref('bad_debt')}", USD2),
            ("Contribution / member", f"=B7-B8-B9-B10-B11", USD2),
            ("Contribution margin %", f"=B12/B7", PCT),
            ("Break-even utilization", f"=(B7-B10-B11)/({cpc_cell}+{ref('cc_handling')})", PCT),
        ]
        r0 = 7
        for i, (lab, f, fmt) in enumerate(rows):
            rr = r0 + i
            put(s, rr, 1, lab, font=(F_BOLD if "Contribution" in lab or "Break-even" in lab else F_NORM))
            fill = FILL_REC if ("Contribution / member" in lab or "Break-even" in lab) else FILL_CALC
            put(s, rr, 2, f, fmt=fmt, fill=fill, align=RGT)
        # mandatory totals across sub levels
        tr = r0 + len(rows) + 2
        put(s, tr, 1, "Mandatory (100% enrolled) annual totals by subscriber level", font=F_PRIM, border=False)
        tr += 1
        cols = ["Subs", "Enrolled", "Gross Annual", "Covered Exp", "CC Exp", "Admin", "Bad Debt",
                "Fixed", "Churn Loss", "Net Annual (Y2+)", "Net Margin %"]
        for j, h in enumerate(cols, 1):
            s.cell(row=tr, column=j, value=h)
        hdr(s, tr, len(cols))
        contrib_cell = f"'{name}'!$B$12"
        base = tr + 1
        for i, lvl in enumerate(C.SUB_LEVELS):
            rr = base + i
            put(s, rr, 1, lvl, fmt=NUM, fill=FILL_INPUT, align=CEN)
            put(s, rr, 2, f"=A{rr}*1", fmt=NUM, align=RGT)  # mandatory=100%
            put(s, rr, 3, f"=B{rr}*{pr}*12", fmt=USD, align=RGT)
            put(s, rr, 4, f"=B{rr}*{ue}*{cpc_cell}", fmt=USD, align=RGT)
            put(s, rr, 5, f"=B{rr}*{ue}*{ref('cc_handling')}", fmt=USD, align=RGT)
            put(s, rr, 6, f"=B{rr}*{ref('billing_cost_yr')}", fmt=USD, align=RGT)
            put(s, rr, 7, f"=C{rr}*{ref('bad_debt')}", fmt=USD, align=RGT)
            put(s, rr, 8, f"={ref('program_mgmt')}+{ref('cust_comm_annual')}", fmt=USD, align=RGT)
            put(s, rr, 9, f"=A{rr}*{ref('incr_churn_annual')}*{ref('arpu')}*12", fmt=USD, align=RGT)
            net = f"=C{rr}-D{rr}-E{rr}-F{rr}-G{rr}-H{rr}-I{rr}"
            put(s, rr, 10, net, fmt=USD, fill=FILL_REC, font=F_BOLD, align=RGT)
            put(s, rr, 11, f"=J{rr}/C{rr}", fmt=PCT, align=RGT)
        s.cell(row=base + len(C.SUB_LEVELS) + 1, column=1,
               value="Net Annual excludes one-time launch/billing costs (see Five-Year & Dashboard). Churn Loss uses incremental-churn assumption on full base.").font = F_ITAL
        for i, w in enumerate([9, 10, 13, 12, 10, 10, 10, 11, 12, 15, 12], 1):
            s.column_dimensions[get_column_letter(i)].width = w
        return s

    scenario_sheet("Scenario A", "price_a", "$3.99")
    scenario_sheet("Scenario B", "price_b", "$4.99")

    # ================= ENROLLMENT MODELS =================
    we = wb.create_sheet("Enrollment Models")
    title(we, "Enrollment-Model Comparison", "Mandatory / Opt-out / Opt-in at current subscribers", 6)
    put(we, 5, 1, f"At current subscribers (Assumptions) — Gross & Net annual by model and price", font=F_PRIM, border=False)
    cols = ["Model", "Participation", "Enrolled", "Gross Annual $3.99", "Net Annual $3.99",
            "Gross Annual $4.99", "Net Annual $4.99"]
    for j, h in enumerate(cols, 1):
        we.cell(row=6, column=j, value=h)
    hdr(we, 6, len(cols))
    subs = ref("current_subs")
    ue = ref("util_expected")
    fixed = f"({ref('program_mgmt')}+{ref('cust_comm_annual')})"

    def net_formula(enrolled_cell, price_ref, churn_base_cell):
        gross = f"{enrolled_cell}*{price_ref}*12"
        covered = f"{enrolled_cell}*{ue}*{cpc_cell}"
        cc = f"{enrolled_cell}*{ue}*{ref('cc_handling')}"
        admin = f"{enrolled_cell}*{ref('billing_cost_yr')}"
        bad = f"{gross}*{ref('bad_debt')}"
        churn = f"{churn_base_cell}*{ref('incr_churn_annual')}*{ref('arpu')}*12"
        return f"={gross}-({covered})-({cc})-({admin})-({bad})-{fixed}-({churn})"

    model_rows = [("Mandatory", 1.00, "all")]
    for rt in C.OPTOUT_RATES:
        model_rows.append((f"Opt-out", rt, "all"))
    for rt in C.OPTIN_RATES:
        model_rows.append((f"Opt-in", rt, "enrolled"))
    rr = 7
    for label, part, cbase in model_rows:
        put(we, rr, 1, label, font=F_BOLD)
        put(we, rr, 2, part, fmt=PCT0, fill=FILL_INPUT, align=CEN)
        put(we, rr, 3, f"={subs}*B{rr}", fmt=NUM, fill=FILL_CALC, align=RGT)
        churn_base = f"{subs}" if cbase == "all" else f"C{rr}"
        put(we, rr, 4, f"=C{rr}*{ref('price_a')}*12", fmt=USD, align=RGT)
        put(we, rr, 5, net_formula(f"C{rr}", ref('price_a'), churn_base), fmt=USD, fill=FILL_CALC, align=RGT, font=F_BOLD)
        put(we, rr, 6, f"=C{rr}*{ref('price_b')}*12", fmt=USD, align=RGT)
        put(we, rr, 7, net_formula(f"C{rr}", ref('price_b'), churn_base), fmt=USD, fill=FILL_CALC, align=RGT, font=F_BOLD)
        rr += 1
    we.cell(row=rr + 1, column=1, value="Net excludes one-time costs; churn applied to full base for mandatory/opt-out, enrolled base for opt-in.").font = F_ITAL
    for i, w in enumerate([14, 13, 11, 18, 17, 18, 17], 1):
        we.column_dimensions[get_column_letter(i)].width = w

    # ================= UTILIZATION ANALYSIS =================
    wu = wb.create_sheet("Utilization Analysis")
    title(wu, "Service-Call Utilization Sensitivity", "Per-member contribution by utilization × loaded call cost (negative = unprofitable)", 8)
    for price_key, top, plabel in [("price_a", 5, "$3.99"), ("price_b", 16, "$4.99")]:
        put(wu, top, 1, f"{plabel} — per-member annual contribution (rows=utilization, cols=loaded cost/call)", font=F_PRIM, border=False)
        put(wu, top + 1, 1, "Util \\ Cost", font=F_HDR, fill=FILL_SUB, align=CEN)
        for j, cost in enumerate(C.COST_GRID, 2):
            put(wu, top + 1, j, cost, fmt=USD, fill=FILL_SUB, font=F_HDR, align=CEN)
        pr = ref(price_key)
        for i, util in enumerate(C.UTIL_GRID):
            rr = top + 2 + i
            put(wu, rr, 1, util, fmt=PCT0, fill=FILL_INPUT, align=CEN)
            for j, cost in enumerate(C.COST_GRID, 2):
                costcell = f"{get_column_letter(j)}${top+1}"
                utilcell = f"$A{rr}"
                # contribution = price*12 - util*cost - util*cc - admin - price*12*baddebt
                f = (f"={pr}*12 - {utilcell}*{costcell} - {utilcell}*{ref('cc_handling')} "
                     f"- {ref('billing_cost_yr')} - {pr}*12*{ref('bad_debt')}")
                put(wu, rr, j, f, fmt=USD2, align=RGT)
        # conditional formatting: red if <0, green if >0
        rng = f"B{top+2}:{get_column_letter(1+len(C.COST_GRID))}{top+1+len(C.UTIL_GRID)}"
        wu.conditional_formatting.add(rng, CellIsRule(operator="lessThan", formula=["0"], fill=FILL_WARN))
        wu.conditional_formatting.add(rng, CellIsRule(operator="greaterThan", formula=["0"], fill=FILL_REC))
    wu.column_dimensions["A"].width = 12
    for j in range(2, 2 + len(C.COST_GRID)):
        wu.column_dimensions[get_column_letter(j)].width = 12
    wu.cell(row=27, column=1, value="Green = profitable per member; Clay = unprofitable. Loaded cost/call default is computed on Assumptions.").font = F_ITAL

    # ================= CHURN SENSITIVITY =================
    wc = wb.create_sheet("Churn Sensitivity")
    title(wc, "Churn Sensitivity", "Net annual effect vs. incremental annual churn (mandatory, current subs)", 5)
    put(wc, 5, 1, "Incremental churn wipes out plan value once net turns negative.", font=F_PRIM, border=False)
    for j, h in enumerate(["Incremental Annual Churn", "Churned Customers", "Lost Internet Rev",
                           "Net $3.99 (Mandatory)", "Net $4.99 (Mandatory)"], 1):
        wc.cell(row=6, column=j, value=h)
    hdr(wc, 6, 5)
    subs = ref("current_subs")
    ue = ref("util_expected")
    for i, ch in enumerate(C.CHURN_GRID):
        rr = 7 + i
        put(wc, rr, 1, ch, fmt="0.00%", fill=FILL_INPUT, align=CEN)
        put(wc, rr, 2, f"={subs}*A{rr}", fmt=NUM, fill=FILL_CALC, align=RGT)
        put(wc, rr, 3, f"=B{rr}*{ref('arpu')}*12", fmt=USD, fill=FILL_CALC, align=RGT)
        # mandatory net at price A/B minus this churn loss (recompute gross/costs at 100%)
        for col, pk in [(4, "price_a"), (5, "price_b")]:
            pr = ref(pk)
            gross = f"{subs}*{pr}*12"
            covered = f"{subs}*{ue}*{cpc_cell}"
            cc = f"{subs}*{ue}*{ref('cc_handling')}"
            admin = f"{subs}*{ref('billing_cost_yr')}"
            bad = f"{gross}*{ref('bad_debt')}"
            fixed = f"({ref('program_mgmt')}+{ref('cust_comm_annual')})"
            f = f"={gross}-({covered})-({cc})-({admin})-({bad})-{fixed}-C{rr}"
            put(wc, rr, col, f, fmt=USD, fill=FILL_CALC, font=F_BOLD, align=RGT)
    wc.conditional_formatting.add(f"D7:E{6+len(C.CHURN_GRID)}",
                                  CellIsRule(operator="lessThan", formula=["0"], fill=FILL_WARN))
    wc.conditional_formatting.add(f"D7:E{6+len(C.CHURN_GRID)}",
                                  CellIsRule(operator="greaterThan", formula=["0"], fill=FILL_REC))
    for i, w in enumerate([24, 18, 18, 22, 22], 1):
        wc.column_dimensions[get_column_letter(i)].width = w
    off_a = C.churn_offset_pct(C.PRICE_A, C.A["current_subs"], 1.0, churn_base="all")
    off_b = C.churn_offset_pct(C.PRICE_B, C.A["current_subs"], 1.0, churn_base="all")
    wc.cell(row=8 + len(C.CHURN_GRID), column=1,
            value=f"Break-even incremental churn (mandatory): $3.99 ≈ {off_a*100:.2f}% · $4.99 ≈ {off_b*100:.2f}% (computed).").font = F_ITAL

    # ================= PAY-PER-VISIT =================
    wp = wb.create_sheet("Pay-Per-Visit")
    title(wp, "Pay-Per-Visit Comparison", "Charge non-enrolled customers per customer-caused visit", 5)
    for j, h in enumerate(["Charge / Visit", "Customer-Caused Calls/yr", "Gross Billed",
                           "Collected (recovered)", "Loaded Cost (incurred anyway)", "Cost Recovery %"], 1):
        wp.cell(row=6, column=j, value=h)
    hdr(wp, 6, 6)
    subs = ref("current_subs")
    calls = f"{subs}*{ref('trouble_rate')}*{ref('cust_caused_pct')}"
    for i, ch in enumerate(C.PPV_CHARGES):
        rr = 7 + i
        put(wp, rr, 1, ch, fmt=USD, fill=FILL_INPUT, align=CEN)
        put(wp, rr, 2, f"={calls}", fmt=NUM, fill=FILL_CALC, align=RGT)
        put(wp, rr, 3, f"=B{rr}*A{rr}", fmt=USD, align=RGT)
        put(wp, rr, 4, f"=C{rr}*{ref('ppv_collection')}", fmt=USD, fill=FILL_REC, font=F_BOLD, align=RGT)
        put(wp, rr, 5, f"=B{rr}*({cpc_cell}+{ref('cc_handling')})", fmt=USD, align=RGT)
        put(wp, rr, 6, f"=D{rr}/E{rr}", fmt=PCT, align=RGT)
        rr += 1
    put(wp, 7 + len(C.PPV_CHARGES), 1,
        "Cost is incurred whether or not RIVR bills; 'Collected' is revenue recovered against an "
        "otherwise-absorbed cost. No single charge in this range fully covers the loaded call cost "
        "— an argument for the subscription risk-pool.", font=F_ITAL, border=False)
    r2 = 7 + len(C.PPV_CHARGES) + 1
    put(wp, r2, 1, "Qualitative comparison", font=F_PRIM, border=False)
    r2 += 1
    for j, h in enumerate(["Dimension", "Monthly Plan", "Pay-Per-Visit"], 1):
        wp.cell(row=r2, column=j, value=h)
    hdr(wp, r2, 3)
    qual = [
        ("Revenue predictability", "High (recurring)", "Low (event-driven)"),
        ("Customer acceptance", "Mixed (if mandatory)", "Higher (only users pay)"),
        ("Administrative complexity", "Higher (enrollment/billing)", "Lower per event, disputes per visit"),
        ("Technician documentation", "Lighter (covered)", "Heavy (must justify each charge)"),
        ("Billing disputes", "Fewer per-visit disputes", "More per-visit disputes"),
        ("Collection risk", "Spread across base", "Concentrated at billing"),
        ("Utilization risk", "Provider bears it", "Customer bears it"),
        ("Fairness to non-users", "Low (all pay)", "High (only users pay)"),
    ]
    for i, row in enumerate(qual):
        rr = r2 + 1 + i
        for j, val in enumerate(row, 1):
            put(wp, rr, j, val, font=(F_BOLD if j == 1 else F_NORM), align=WRP)
    for i, w in enumerate([16, 26, 30], 1):
        wp.column_dimensions[get_column_letter(i)].width = w

    # ================= FIVE-YEAR FORECAST =================
    wy = wb.create_sheet("Five-Year Forecast")
    title(wy, "Five-Year Forecast", "Recommended structure: voluntary opt-in $3.99 at expected enrollment", 6)
    put(wy, 5, 1, "Recommended enrollment (opt-in, editable):", font=F_BOLD, border=False)
    put(wy, 5, 3, 0.35, fmt=PCT0, fill=FILL_INPUT, align=CEN)
    enroll_cell = "'Five-Year Forecast'!$C$5"
    for j, h in enumerate(["Year", "Subscribers", "Enrolled", "Price", "Gross Annual",
                           "Net Annual", "Cum. Gross", "Cum. Net"], 1):
        wy.cell(row=7, column=j, value=h)
    hdr(wy, 7, 8)
    ue = ref("util_expected")
    fixed = f"({ref('program_mgmt')}+{ref('cust_comm_annual')})"
    onetime = f"({ref('billing_impl')}+{ref('launch_cost')})"
    for y in range(5):
        rr = 8 + y
        if y == 0:
            subf = f"={ref('current_subs')}"
            pricef = f"={ref('price_a')}"
        else:
            subf = f"=B{rr-1}*(1+{ref('monthly_growth')})^12"
            pricef = f"=D{rr-1}*(1+{ref('price_increase')})"
        put(wy, rr, 1, y + 1, align=CEN)
        put(wy, rr, 2, subf, fmt=NUM, fill=FILL_CALC, align=RGT)
        put(wy, rr, 3, f"=B{rr}*{enroll_cell}", fmt=NUM, fill=FILL_CALC, align=RGT)
        put(wy, rr, 4, pricef, fmt=USD2, fill=FILL_CALC, align=RGT)
        put(wy, rr, 5, f"=C{rr}*D{rr}*12", fmt=USD, fill=FILL_CALC, align=RGT)
        covered = f"C{rr}*{ue}*{cpc_cell}"
        cc = f"C{rr}*{ue}*{ref('cc_handling')}"
        admin = f"C{rr}*{ref('billing_cost_yr')}"
        bad = f"E{rr}*{ref('bad_debt')}"
        ot = onetime if y == 0 else "0"
        # Voluntary opt-in: enrollees chose the plan, so fee-driven churn is treated as ~0 here.
        put(wy, rr, 6, f"=E{rr}-({covered})-({cc})-({admin})-({bad})-{fixed}-{ot}",
            fmt=USD, fill=FILL_REC, font=F_BOLD, align=RGT)
        if y == 0:
            put(wy, rr, 7, f"=E{rr}", fmt=USD, align=RGT)
            put(wy, rr, 8, f"=F{rr}", fmt=USD, align=RGT)
        else:
            put(wy, rr, 7, f"=G{rr-1}+E{rr}", fmt=USD, align=RGT)
            put(wy, rr, 8, f"=H{rr-1}+F{rr}", fmt=USD, align=RGT)
    for i, w in enumerate([7, 13, 11, 10, 14, 14, 14, 14], 1):
        wy.column_dimensions[get_column_letter(i)].width = w
    wy.cell(row=14, column=1,
            value="Voluntary opt-in assumes ~0 fee-driven churn (enrollees chose the plan). "
                  "Excludes pay-per-visit revenue from decliners — the hybrid adds that upside. "
                  "Year 1 net absorbs one-time launch/billing costs.").font = F_ITAL

    # ================= EXECUTIVE DASHBOARD =================
    wd = wb.create_sheet("Executive Dashboard", 0)
    title(wd, "Executive Dashboard", "Blanket Maintenance Protection Plan — headline analysis", 8)
    legend(wd, 4, 8)
    # tiles pulling from other sheets
    tiles = [
        ("Loaded cost / call", f"={cpc_cell}", USD2),
        ("Break-even util $3.99", "='Scenario A'!$B$14", PCT),
        ("Break-even util $4.99", "='Scenario B'!$B$14", PCT),
        ("Contribution/member $3.99", "='Scenario A'!$B$12", USD2),
        ("Contribution/member $4.99", "='Scenario B'!$B$12", USD2),
        ("Mandatory net $3.99 (curr)", "='Scenario A'!$J$19", USD),
        ("Mandatory net $4.99 (curr)", "='Scenario B'!$J$19", USD),
        ("5-yr cum net (opt-in $3.99)", "='Five-Year Forecast'!$H$12", USD),
    ]
    r = 6; col = 1
    for label, f, fmt in tiles:
        lc = put(wd, r, col, label, fill=FILL_SUB, font=F_HDR, align=CEN)
        vc = put(wd, r + 1, col, f, fmt=fmt, fill=FILL_CALC, align=CEN,
                 font=Font(bold=True, size=13, color=BRAND["primary"]))
        wd.merge_cells(start_row=r, start_column=col, end_row=r, end_column=col + 1)
        wd.merge_cells(start_row=r + 1, start_column=col, end_row=r + 2, end_column=col + 1)
        col += 2
        if col > 8:
            col = 1; r += 4
    for i in range(1, 9):
        wd.column_dimensions[get_column_letter(i)].width = 15

    # chart data (static snapshots computed in Python for charting)
    dr = r + 5
    put(wd, dr, 1, "Enrollment-Model Net Annual (chart data, computed snapshot)", font=F_PRIM, border=False)
    dr += 1
    for j, h in enumerate(["Model", "Net $3.99", "Net $4.99"], 1):
        wd.cell(row=dr, column=j, value=h)
    hdr(wd, dr, 3)
    snap = [
        ("Mandatory", 1.00, "all"),
        ("Opt-out 85%", 0.85, "all"),
        ("Opt-out 60%", 0.60, "all"),
        ("Opt-in 40%", 0.40, "enrolled"),
        ("Opt-in 30%", 0.30, "enrolled"),
        ("Opt-in 20%", 0.20, "enrolled"),
    ]
    d0 = dr + 1
    for i, (lab, part, cbase) in enumerate(snap):
        rr = d0 + i
        na = C.program_totals(C.PRICE_A, C.A["current_subs"], part, churn_base=cbase, include_onetime=False)["net_annual"]
        nb = C.program_totals(C.PRICE_B, C.A["current_subs"], part, churn_base=cbase, include_onetime=False)["net_annual"]
        put(wd, rr, 1, lab, font=F_BOLD)
        put(wd, rr, 2, round(na), fmt=USD, align=RGT)
        put(wd, rr, 3, round(nb), fmt=USD, align=RGT)
    ch = BarChart(); ch.type = "col"; ch.title = "Net Annual by Enrollment Model"; ch.style = 10
    data = Reference(wd, min_col=2, min_row=dr, max_col=3, max_row=d0 + len(snap) - 1)
    cats = Reference(wd, min_col=1, min_row=d0, max_row=d0 + len(snap) - 1)
    ch.add_data(data, titles_from_data=True); ch.set_categories(cats)
    ch.y_axis.numFmt = USD; ch.height = 7.5; ch.width = 14
    wd.add_chart(ch, f"A{d0 + len(snap) + 2}")

    # churn chart data
    cr = d0 + len(snap) + 18
    put(wd, cr, 1, "Churn Sensitivity — Net $3.99 Mandatory (snapshot)", font=F_PRIM, border=False)
    cr += 1
    for j, h in enumerate(["Incr. Churn", "Net $3.99", "Net $4.99"], 1):
        wd.cell(row=cr, column=j, value=h)
    hdr(wd, cr, 3)
    c0 = cr + 1
    for i, chn in enumerate(C.CHURN_GRID):
        rr = c0 + i
        na = C.program_totals(C.PRICE_A, C.A["current_subs"], 1.0, incr_churn=chn, churn_base="all", include_onetime=False)["net_annual"]
        nb = C.program_totals(C.PRICE_B, C.A["current_subs"], 1.0, incr_churn=chn, churn_base="all", include_onetime=False)["net_annual"]
        put(wd, rr, 1, f"{chn*100:.2f}%", align=CEN)
        put(wd, rr, 2, round(na), fmt=USD, align=RGT)
        put(wd, rr, 3, round(nb), fmt=USD, align=RGT)
    lch = LineChart(); lch.title = "Net Annual vs. Incremental Churn (Mandatory)"; lch.style = 12
    ldata = Reference(wd, min_col=2, min_row=cr, max_col=3, max_row=c0 + len(C.CHURN_GRID) - 1)
    lcats = Reference(wd, min_col=1, min_row=c0, max_row=c0 + len(C.CHURN_GRID) - 1)
    lch.add_data(ldata, titles_from_data=True); lch.set_categories(lcats)
    lch.y_axis.numFmt = USD; lch.height = 7.5; lch.width = 14
    wd.add_chart(lch, f"A{c0 + len(C.CHURN_GRID) + 2}")

    # ================= RECOMMENDATION SUMMARY =================
    wr = wb.create_sheet("Recommendation Summary")
    title(wr, "Recommendation Summary", "Weighted decision matrix (scores 1-5; higher = better)", 4)
    # criteria weights table
    put(wr, 5, 1, "Criteria & Weights", font=F_PRIM, border=False)
    for j, h in enumerate(["Criterion", "Weight %"], 1):
        wr.cell(row=6, column=j, value=h)
    hdr(wr, 6, 2)
    for i, (crit, w) in enumerate(C.CRITERIA):
        rr = 7 + i
        put(wr, rr, 1, crit, font=F_NORM, align=WRP)
        put(wr, rr, 2, w, fmt=NUM, fill=FILL_INPUT, align=CEN)
    weight_first = 7
    weight_last = 6 + len(C.CRITERIA)
    # scoring matrix
    top = weight_last + 2
    put(wr, top, 1, "Weighted Scores by Option", font=F_PRIM, border=False)
    top += 1
    header = ["Option"] + [c for c, _ in C.CRITERIA] + ["Weighted Score", "Rank"]
    for j, h in enumerate(header, 1):
        wr.cell(row=top, column=j, value=h)
    hdr(wr, top, len(header))
    wr.row_dimensions[top].height = 54
    base = top + 1
    ncrit = len(C.CRITERIA)
    for i, opt in enumerate(C.OPTIONS):
        rr = base + i
        put(wr, rr, 1, opt, font=F_BOLD, align=WRP)
        for j, sc in enumerate(C.SCORES[opt]):
            put(wr, rr, 2 + j, sc, fmt=NUM, fill=FILL_INPUT, align=CEN)
        # weighted score = SUMPRODUCT(scores, weights)/SUM(weights)
        score_rng = f"B{rr}:{get_column_letter(1+ncrit)}{rr}"
        weight_rng = f"$B${weight_first}:$B${weight_last}"
        put(wr, rr, 2 + ncrit, f"=SUMPRODUCT({score_rng},TRANSPOSE({weight_rng}))/SUM({weight_rng})",
            fmt="0.00", fill=FILL_REC, font=F_BOLD, align=CEN)
        # rank
        wscol = get_column_letter(2 + ncrit)
        put(wr, rr, 3 + ncrit,
            f"=RANK({wscol}{rr},{wscol}{base}:{wscol}{base+len(C.OPTIONS)-1})", fmt=NUM, align=CEN)
    # Note: SUMPRODUCT with TRANSPOSE needs array; provide simpler fallback too
    for i, w in enumerate([24] + [7] * ncrit + [14, 6], 1):
        wr.column_dimensions[get_column_letter(i)].width = w
    rec_row = base + len(C.OPTIONS) + 2
    put(wr, rec_row, 1, "RECOMMENDATION", font=Font(bold=True, size=12, color=BRAND["good"]), border=False)
    put(wr, rec_row + 1, 1,
        "Voluntary opt-in at $3.99 (Basic/Standard coverage) delivered as a HYBRID: enrollees "
        "get the plan; customers who decline pay a per-visit dispatch charge. Do NOT implement a "
        "mandatory blanket fee. Exempt Lifeline/Tribal/low-income (opt-in only); exclude bulk/managed "
        "properties. Requires legal review of negative-option/consumer-protection rules.",
        font=F_NORM, align=WRP, border=False)
    wr.merge_cells(start_row=rec_row + 1, start_column=1, end_row=rec_row + 3, end_column=13)

    wb.save(OUT)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    build()
