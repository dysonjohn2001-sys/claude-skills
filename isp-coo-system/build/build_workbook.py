"""
ISP / Fiber Broadband — COO Executive Management System
Workbook generator.

Builds a single .xlsx with:
  • Executive Dashboard (one-page COO view, RYG health, MTD/YTD/Rolling-12)
  • Sales / Operations / Financial dashboards (KPIs + charts)
  • Board Report (executive narrative, auto-rolled-up)
  • 11 structured input tabs (Tables, dropdowns, conditional formatting)
  • Calc engine, Data Dictionary, User Guide, Assumptions

Run:  python build/build_workbook.py
Out:  ISP_COO_Executive_Management_System.xlsx
"""
import os
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, FormulaRule, IconSetRule
from openpyxl.chart import LineChart, BarChart, PieChart, Reference, Series
from openpyxl.chart.label import DataLabelList

import styles as S
import data as D

# --------------------------------------------------------------------------
HEADER_ROW = 3
DATA_START = 4
DATA_END = 1003          # generous range so staff can append rows
CUR = '$#,##0'
CUR2 = '$#,##0.00'
NUM = '#,##0'
PCT = '0.0%'
PCT0 = '0%'
DEC1 = '0.0'

wb = Workbook()
wb.remove(wb.active)

# Canonical parameter cells (set on Exec_Dashboard control strip)
PM = "Exec_Dashboard!$C$5"      # selected reporting month (text)
PIDX = "Exec_Dashboard!$D$5"    # period index 1..12 (=MATCH)

# Short sheet handles
FD, CD, OD, ST = "Financial_Data", "Customer_Data", "Operations_Data", "Sales_Targets"
SD, PL, RD = "Sales_Data", "Pipeline", "Revenue_Detail"
PRJ, GR, RR, BA = "Project_Data", "Grant_Data", "Risk_Register", "Board_Actions"


def rng(sheet, col):
    return f"{sheet}!${col}${DATA_START}:${col}${DATA_END}"

def sumifs(val_sheet, val_col, *crit_pairs):
    parts = [rng(val_sheet, val_col)]
    for cr_col, cr in crit_pairs:
        parts.append(rng(val_sheet, cr_col))
        parts.append(cr)
    return "SUMIFS(" + ",".join(parts) + ")"

def avgifs(val_sheet, val_col, *crit_pairs):
    parts = [rng(val_sheet, val_col)]
    for cr_col, cr in crit_pairs:
        parts.append(rng(val_sheet, cr_col))
        parts.append(cr)
    return "AVERAGEIFS(" + ",".join(parts) + ")"

def countifs(sheet, *crit_pairs):
    parts = []
    for cr_col, cr in crit_pairs:
        parts.append(rng(sheet, cr_col))
        parts.append(cr)
    return "COUNTIFS(" + ",".join(parts) + ")"


# ==========================================================================
# 1. LISTS sheet (dropdown sources) — hidden
# ==========================================================================
lists = wb.create_sheet("Lists")
list_cols = {}   # name -> (col_letter, n_values)
ci = 1
for name, vals in D.LISTS.items():
    col = get_column_letter(ci)
    lists.cell(row=1, column=ci, value=name).font = S.F_BODY_B
    for r, v in enumerate(vals, start=2):
        lists.cell(row=r, column=ci, value=v)
    list_cols[name] = (col, len(vals))
    lists.column_dimensions[col].width = 16
    ci += 1

def dv_for(name):
    col, n = list_cols[name]
    f = f"=Lists!${col}$2:${col}${1+n}"
    dv = DataValidation(type="list", formula1=f, allow_blank=True)
    return dv


# ==========================================================================
# Helper to build a standard INPUT sheet with a title band + Excel Table
# ==========================================================================
def build_input_sheet(name, title, instr, headers, rows, fmts=None,
                       widths=None, tab_color=S.STEEL, validations=None,
                       computed=None):
    ws = wb.create_sheet(name)
    S.page_setup(ws, tab_color=tab_color)
    last_col = len(headers)
    last_letter = get_column_letter(last_col)
    # title band
    ws.merge_cells(f"A1:{last_letter}1")
    t = ws["A1"]; t.value = title; t.font = S.F_SECTION; t.fill = S.fill(S.NAVY)
    t.alignment = S.Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 24
    ws.merge_cells(f"A2:{last_letter}2")
    n = ws["A2"]; n.value = instr; n.font = S.F_NOTE; n.fill = S.fill(S.LIGHT_BG)
    n.alignment = S.Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[2].height = 16
    # header row
    for c, h in enumerate(headers, start=1):
        cell = ws.cell(row=HEADER_ROW, column=c, value=h)
    S.style_table_header(ws, HEADER_ROW, 1, last_col)
    # data rows
    r = DATA_START
    for row in rows:
        for c, v in enumerate(row, start=1):
            cell = ws.cell(row=r, column=c, value=v)
            cell.font = S.F_BODY
            cell.border = S.box_thin
            if fmts and c - 1 < len(fmts) and fmts[c - 1]:
                cell.number_format = fmts[c - 1]
        r += 1
    last_data = r - 1
    # computed (per-row formula) columns: list of (col_index, formula_template)
    if computed:
        for rr in range(DATA_START, last_data + 1):
            for col_idx, tmpl in computed:
                ws.cell(row=rr, column=col_idx, value=tmpl.format(r=rr))
    # Excel Table
    tbl_ref = f"A{HEADER_ROW}:{last_letter}{last_data}"
    tname = "tbl_" + name.replace("-", "_")
    tbl = Table(displayName=tname, ref=tbl_ref)
    tbl.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium2", showRowStripes=True, showColumnStripes=False)
    ws.add_table(tbl)
    # widths
    if widths:
        for col, w in widths.items():
            ws.column_dimensions[col].width = w
    else:
        for c in range(1, last_col + 1):
            ws.column_dimensions[get_column_letter(c)].width = 15
    # validations: list of (col_index, list_name)
    if validations:
        for col_idx, lname in validations:
            dv = dv_for(lname)
            ws.add_data_validation(dv)
            L = get_column_letter(col_idx)
            dv.add(f"{L}{DATA_START}:{L}{DATA_END}")
    ws.freeze_panes = f"A{DATA_START}"
    return ws, last_data


# ==========================================================================
# 2. INPUT SHEETS
# ==========================================================================
# --- Customer_Data
build_input_sheet(
    CD, "CUSTOMER DATA  —  Monthly Subscriber Roll-Up",
    "Enter ONE row per month. Total Customers = end-of-month subscriber count. Homes Passed = cumulative. Update weekly/at month close.",
    ["Month", "Period", "Total Customers", "New Sales", "Disconnects", "Homes Passed (cum)"],
    D.CUSTOMERS,
    fmts=[None, "0", NUM, NUM, NUM, NUM],
    widths={"A": 12, "B": 8, "C": 16, "D": 12, "E": 13, "F": 18},
    validations=[(1, "Months")],
)

# --- Financial_Data
build_input_sheet(
    FD, "FINANCIAL DATA  —  Monthly P&L / Capital / Cash",
    "One row per month. Revenue is total billed. OpEx excludes capitalized construction. CapEx = capitalized build. Cash Balance = end-of-month.",
    ["Month", "Period", "Revenue", "MRR", "CapEx", "OpEx", "Labor", "Contractor",
     "Grant Reimb", "Budget Revenue", "Budget OpEx", "Budget CapEx",
     "Forecast Revenue", "Cash Balance"],
    D.FINANCIALS,
    fmts=[None, "0"] + [CUR] * 12,
    widths={"A": 12, "B": 8, "C": 13, "D": 13, "E": 12, "F": 12, "G": 12,
            "H": 12, "I": 12, "J": 14, "K": 13, "L": 13, "M": 15, "N": 14},
    validations=[(1, "Months")],
)

# --- Operations_Data
build_input_sheet(
    OD, "OPERATIONS DATA  —  Monthly Build / Install / Service",
    "One row per month. Homes Passed Added = new this month. Avg Days to Install = order-to-activation. Repeat Tickets = re-opened within 30 days.",
    ["Month", "Period", "Homes Passed Added", "Footage Built", "Drops Completed",
     "Installs Scheduled", "Installs Completed", "Avg Days to Install",
     "Trouble Tickets", "Repeat Tickets", "Outages", "Activations", "Splices Completed"],
    D.OPERATIONS,
    fmts=[None, "0", NUM, NUM, NUM, NUM, NUM, DEC1, NUM, NUM, "0", NUM, NUM],
    widths={"A": 12, "B": 8, "C": 17, "D": 13, "E": 14, "F": 15, "G": 15,
            "H": 16, "I": 13, "J": 13, "K": 9, "L": 12, "M": 15},
    validations=[(1, "Months")],
)

# --- Sales_Targets
build_input_sheet(
    ST, "SALES TARGETS  —  Monthly Goals",
    "One row per month. Sales Goal = net new connects target. Revenue Goal = new MRR target ($).",
    ["Month", "Period", "Sales Goal (units)", "Revenue Goal (new MRR $)"],
    D.TARGETS,
    fmts=[None, "0", NUM, CUR],
    widths={"A": 12, "B": 8, "C": 18, "D": 22},
    validations=[(1, "Months")],
)

# --- Sales_Data
build_input_sheet(
    SD, "SALES DATA  —  Connects & Activity (one row per county / segment / month)",
    "Add rows as deals close. Sales = connects. New MRR = added recurring $. Use dropdowns for County / Segment / Channel / Campaign / Rep.",
    ["Month", "Period", "County", "Segment", "Channel", "Campaign", "Rep",
     "Leads", "Qualified", "Sales (units)", "New MRR ($)", "Door Knocks"],
    D.SALES,
    fmts=[None, "0", None, None, None, None, None, NUM, NUM, NUM, CUR, NUM],
    widths={"A": 12, "B": 8, "C": 12, "D": 12, "E": 14, "F": 17, "G": 15,
            "H": 9, "I": 10, "J": 12, "K": 12, "L": 12},
    validations=[(1, "Months"), (3, "Counties"), (4, "Segments"),
                 (5, "Channels"), (6, "Campaigns"), (7, "Reps")],
)

# --- Pipeline
build_input_sheet(
    PL, "PIPELINE  —  Open & Recently-Closed Opportunities",
    "Value = annual recurring $ (ARR). Set Stage via dropdown. Closed-Lost rows require a Lost Reason. Enterprise/DIA, HOA/Developer, Bulk are Opp Types.",
    ["Opp ID", "Name", "County", "Segment", "Type", "Stage", "Value (ARR $)",
     "Rep", "Close Month", "Lost Reason"],
    D.PIPELINE,
    fmts=[None, None, None, None, None, None, CUR, None, None, None],
    widths={"A": 11, "B": 26, "C": 12, "D": 12, "E": 16, "F": 13, "G": 14,
            "H": 15, "I": 12, "J": 16},
    validations=[(3, "Counties"), (4, "Segments"), (5, "Opp Type"),
                 (6, "Pipeline Stage"), (8, "Reps"), (9, "Months"), (10, "Lost Reason")],
)

# --- Revenue_Detail
build_input_sheet(
    RD, "REVENUE DETAIL  —  Revenue & COGS by Product / Month",
    "One row per product per month. Used for revenue-by-product and margin-by-service-line. COGS = direct cost of that line.",
    ["Month", "Period", "Product / Service Line", "Segment", "Revenue", "COGS"],
    D.REVENUE_DETAIL,
    fmts=[None, "0", None, None, CUR, CUR],
    widths={"A": 12, "B": 8, "C": 22, "D": 16, "E": 13, "F": 13},
    validations=[(1, "Months"), (3, "Products")],
)

# --- Project_Data (with computed Capital Variance? keep simple)
prj_ws, prj_last = build_input_sheet(
    PRJ, "PROJECT DATA  —  Capital Build Projects",
    "One row per capital project. % Complete 0-1. Status drives RYG. Permitting / Make-Ready / Splicing use Build Phase dropdown. Contractor Score 0-10.",
    ["Project", "County", "Type", "Grant Program", "% Complete", "Status",
     "Homes Passed Target", "Homes Passed Actual", "Footage Target", "Footage Built",
     "Capital Budget", "Capital Spent", "Permitting", "Make-Ready", "Splicing",
     "Contractor", "Contractor Score", "Blocker / Note"],
    D.PROJECTS,
    fmts=[None, None, None, None, PCT0, None, NUM, NUM, NUM, NUM, CUR, CUR,
          None, None, None, None, DEC1, None],
    widths={"A": 22, "B": 12, "C": 15, "D": 13, "E": 11, "F": 11, "G": 16,
            "H": 16, "I": 14, "J": 13, "K": 14, "L": 13, "M": 13, "N": 12,
            "O": 12, "P": 20, "Q": 14, "R": 34},
    validations=[(2, "Counties"), (4, "Grant Program"), (6, "Project Status"),
                 (13, "Build Phase Status"), (14, "Build Phase Status"),
                 (15, "Build Phase Status")],
)

# --- Grant_Data
build_input_sheet(
    GR, "GRANT REIMBURSEMENT DATA  —  Drawdowns (BEAD / CAB / ARPA / State / RDOF)",
    "One row per drawdown request. Status via dropdown. Outstanding = Approved − Received (computed on Financial dashboard).",
    ["Drawdown ID", "Program", "Project", "Amount Requested", "Amount Approved",
     "Amount Received", "Status", "Submission Date", "Expected Date", "Notes"],
    D.GRANTS,
    fmts=[None, None, None, CUR, CUR, CUR, None, None, None, None],
    widths={"A": 14, "B": 11, "C": 24, "D": 16, "E": 16, "F": 16, "G": 14,
            "H": 14, "I": 13, "J": 30},
    validations=[(2, "Grant Program"), (7, "Grant Status")],
)

# --- Risk_Register (computed Score col F, RYG col G)
build_input_sheet(
    RR, "RISK REGISTER",
    "Likelihood × Impact (1-5 each). Score & RYG auto-calc. Owner accountable. Review weekly; close when mitigated.",
    ["Risk ID", "Description", "Category", "Likelihood", "Impact", "Score",
     "RYG", "Owner", "Mitigation", "Status", "Updated"],
    [r[:5] + ["", ""] + r[5:] for r in D.RISKS],   # leave Score/RYG blank for formula
    fmts=[None, None, None, "0", "0", "0", None, None, None, None, None],
    widths={"A": 9, "B": 46, "C": 16, "D": 11, "E": 9, "F": 8, "G": 9,
            "H": 16, "I": 40, "J": 12, "K": 12},
    validations=[(3, "Risk Category"), (4, "Risk Likelihood"), (5, "Risk Impact"),
                 (10, "Risk Status")],
    computed=[(6, "=D{r}*E{r}"),
              (7, '=IF(F{r}>=15,"RED",IF(F{r}>=8,"YELLOW","GREEN"))')],
)

# --- Board_Actions
build_input_sheet(
    BA, "BOARD ACTION ITEMS  —  Decisions & Follow-ups",
    "Track decisions needed from the executive team / board. Set Decision Needed = Yes for board-level approvals.",
    ["Action ID", "Description", "Category", "Owner", "Raised", "Due",
     "Priority", "Status", "Decision Needed"],
    D.BOARD_ACTIONS,
    fmts=[None, None, None, None, None, None, None, None, None],
    widths={"A": 10, "B": 46, "C": 14, "D": 16, "E": 12, "F": 12, "G": 11,
            "H": 13, "I": 15},
    validations=[(7, "Priority"), (8, "Action Status"), (9, "Yes/No")],
)


# ==========================================================================
# 3. CALC engine (derived monthly series for KPIs + charts) — hidden
# ==========================================================================
calc = wb.create_sheet("Calc")
calc_headers = ["Month", "Period", "New Sales", "Disconnects", "Net Adds",
    "Total Customers", "Homes Passed", "Take Rate", "Churn", "Revenue", "MRR",
    "ARPU", "CapEx", "OpEx", "Contractor", "Grant Reimb", "Installs Completed",
    "Installs Scheduled", "Install Backlog", "Avg Days Install", "Trouble Tickets",
    "Repeat Tickets", "Activations", "Footage Built", "Budget Revenue",
    "Budget OpEx", "Cost / Install", "Cost / Home Passed", "Margin %",
    "Rev vs Budget", "Homes Passed Added"]
for c, h in enumerate(calc_headers, start=1):
    cell = calc.cell(row=1, column=c, value=h)
    cell.font = S.F_HDR; cell.fill = S.fill(S.SLATE); cell.alignment = S.CENTER
for i in range(12):
    r = 2 + i              # calc rows 2..13
    dr = DATA_START + i    # matching input data row 4..15
    f = {
        1: f'=Customer_Data!A{dr}',
        2: f'=Customer_Data!B{dr}',
        3: f'=Customer_Data!D{dr}',
        4: f'=Customer_Data!E{dr}',
        5: f'=C{r}-D{r}',
        6: f'=Customer_Data!C{dr}',
        7: f'=Customer_Data!F{dr}',
        8: f'=IF(G{r}=0,0,F{r}/G{r})',
        9: f'=IF({r}=2,0,IF(F{r-1}=0,0,D{r}/F{r-1}))',
        10: f'=Financial_Data!C{dr}',
        11: f'=Financial_Data!D{dr}',
        12: f'=IF(F{r}=0,0,K{r}/F{r})',
        13: f'=Financial_Data!E{dr}',
        14: f'=Financial_Data!F{dr}',
        15: f'=Financial_Data!H{dr}',
        16: f'=Financial_Data!I{dr}',
        17: f'=Operations_Data!G{dr}',
        18: f'=Operations_Data!F{dr}',
        19: f'=IF({r}=2,R{r}-Q{r},S{r-1}+R{r}-Q{r})',  # running backlog
        20: f'=Operations_Data!H{dr}',
        21: f'=Operations_Data!I{dr}',
        22: f'=Operations_Data!J{dr}',
        23: f'=Operations_Data!L{dr}',
        24: f'=Operations_Data!D{dr}',
        25: f'=Financial_Data!J{dr}',
        26: f'=Financial_Data!K{dr}',
        27: f'=IF(Q{r}=0,0,O{r}/Q{r})',                # contractor $ / install
        28: f'=IF(AE{r}=0,0,M{r}/AE{r})',              # capex / homes passed added
        29: f'=IF(J{r}=0,0,(J{r}-(N{r}+O{r}))/J{r})',  # margin
        30: f'=J{r}-Y{r}',                             # rev vs budget
        31: f'=Operations_Data!C{dr}',                 # homes passed added
    }
    for c, formula in f.items():
        cell = calc.cell(row=r, column=c, value=formula)
        if c in (8, 9, 29):
            cell.number_format = PCT
        elif c == 12:
            cell.number_format = CUR2
        elif c in (10, 11, 13, 14, 15, 16, 25, 26, 27, 28, 30):
            cell.number_format = CUR
        elif c == 20:
            cell.number_format = DEC1
        else:
            cell.number_format = NUM
calc.sheet_state = "hidden"
lists.sheet_state = "hidden"

# Calc column letters by header for chart refs
CALC = {h: get_column_letter(i + 1) for i, h in enumerate(calc_headers)}
def calc_ref(header, with_header=True):
    col = CALC[header]
    return Reference(calc, min_col=ord(col) - 64 if len(col) == 1 else None,
                     min_row=1 if with_header else 2, max_row=13)


# ==========================================================================
# Charting helpers
# ==========================================================================
def col_idx(letter):
    n = 0
    for ch in letter:
        n = n * 26 + (ord(ch) - 64)
    return n

def add_line_chart(ws, anchor, title, series_headers, cats_header="Month",
                   width=13, height=7.5, fmt=None):
    ch = LineChart(); ch.title = title; ch.height = height; ch.width = width
    ch.style = 2
    for h in series_headers:
        ci = col_idx(CALC[h])
        ref = Reference(calc, min_col=ci, min_row=1, max_row=13)
        ch.add_data(ref, titles_from_data=True)
    cats = Reference(calc, min_col=col_idx(CALC[cats_header]), min_row=2, max_row=13)
    ch.set_categories(cats)
    ch.x_axis.delete = False; ch.y_axis.delete = False
    ch.x_axis.txPr = None
    if fmt:
        ch.y_axis.numFmt = fmt; ch.y_axis.majorGridlines = ch.y_axis.majorGridlines
    ws.add_chart(ch, anchor)
    return ch

def add_bar_from_block(ws, anchor, title, cat_ref, val_ref, barfmt=None,
                       width=13, height=7.5, color=None, horizontal=False):
    ch = BarChart(); ch.title = title; ch.type = "bar" if horizontal else "col"
    ch.height = height; ch.width = width; ch.legend = None; ch.style = 10
    ch.add_data(val_ref, titles_from_data=True)
    ch.set_categories(cat_ref)
    if barfmt:
        ch.y_axis.numFmt = barfmt
    ws.add_chart(ch, anchor)
    return ch

def add_pie_from_block(ws, anchor, title, cat_ref, val_ref, width=9, height=7.5):
    ch = PieChart(); ch.title = title; ch.height = height; ch.width = width
    ch.add_data(val_ref, titles_from_data=True)
    ch.set_categories(cat_ref)
    ch.dataLabels = DataLabelList(); ch.dataLabels.showPercent = True
    ws.add_chart(ch, anchor)
    return ch


# ==========================================================================
# Conditional-format helpers for RYG status word cells
# ==========================================================================
def apply_ryg_word(ws, cell_range):
    ws.conditional_formatting.add(cell_range, CellIsRule(
        operator="equal", formula=['"GREEN"'],
        fill=S.fill(S.GREEN_BG), font=S.Font(bold=True, color=S.GREEN_TX)))
    ws.conditional_formatting.add(cell_range, CellIsRule(
        operator="equal", formula=['"YELLOW"'],
        fill=S.fill(S.YELLOW_BG), font=S.Font(bold=True, color=S.YELLOW_TX)))
    ws.conditional_formatting.add(cell_range, CellIsRule(
        operator="equal", formula=['"RED"'],
        fill=S.fill(S.RED_BG), font=S.Font(bold=True, color=S.RED_TX)))


# ==========================================================================
# 4. EXECUTIVE DASHBOARD
# ==========================================================================
ex = wb.create_sheet("Exec_Dashboard")
S.page_setup(ex, tab_color=S.ACCENT)
S.set_widths(ex, {get_column_letter(c): 13.5 for c in range(1, 13)})
ex.column_dimensions["A"].width = 3

# Title band
ex.merge_cells("A1:L1")
c = ex["A1"]; c.value = "EXECUTIVE DASHBOARD  —  COO One-Page View"
c.font = S.F_TITLE; c.fill = S.fill(S.NAVY)
c.alignment = S.Alignment(horizontal="left", vertical="center", indent=1)
ex.row_dimensions[1].height = 30
ex.merge_cells("A2:L2")
c = ex["A2"]; c.value = "Regional Fiber Broadband  •  Weekly Executive Review  •  Red / Yellow / Green health  •  All values roll up automatically from the input tabs"
c.font = S.F_SUBTITLE; c.fill = S.fill(S.SLATE)
c.alignment = S.Alignment(horizontal="left", vertical="center", indent=1)
ex.row_dimensions[2].height = 16

# Control strip (row 5): reporting month selector
ex["B4"] = "REPORTING CONTROLS"; ex["B4"].font = S.F_BODY_B
ex["B5"] = "Reporting Month ▶"; ex["B5"].font = S.F_BODY_B
ex["B5"].alignment = S.RIGHT
c = ex["C5"]; c.value = D.CURRENT_MONTH
c.font = S.Font(bold=True, size=12, color=S.WHITE); c.fill = S.fill(S.ACCENT_2)
c.alignment = S.CENTER; c.border = S.box_thin
ex["D5"] = f'=MATCH(C5,Lists!${list_cols["Months"][0]}$2:${list_cols["Months"][0]}${1+list_cols["Months"][1]},0)'
ex["D5"].font = S.F_SMALL; ex["D5"].alignment = S.CENTER
ex["E5"] = "(Period index — drives MTD / YTD / Rolling-12)"; ex["E5"].font = S.F_NOTE
dv = dv_for("Months"); ex.add_data_validation(dv); dv.add("C5")

# ---- KPI cards ----------------------------------------------------------
def exec_card(top, leftcol, label, value_formula, fmt, status_formula_tmpl, sub=""):
    """2-col-wide card. value cell at (top+1,leftcol). status at (top+2,leftcol)."""
    L = get_column_letter(leftcol); R = get_column_letter(leftcol + 1)
    ex.merge_cells(f"{L}{top}:{R}{top}")
    ex.merge_cells(f"{L}{top+1}:{R}{top+1}")
    ex.merge_cells(f"{L}{top+2}:{R}{top+2}")
    lab = ex.cell(row=top, column=leftcol, value=label)
    lab.font = S.F_KPI_LABEL; lab.fill = S.fill(S.CARD_BG)
    lab.alignment = S.Alignment(horizontal="left", vertical="center", indent=1)
    val = ex.cell(row=top + 1, column=leftcol, value=value_formula)
    val.font = S.F_KPI_VALUE_SM; val.fill = S.fill(S.CARD_BG)
    val.alignment = S.Alignment(horizontal="left", vertical="center", indent=1)
    val.number_format = fmt
    vaddr = f"{L}{top+1}"
    st = ex.cell(row=top + 2, column=leftcol,
                 value=status_formula_tmpl.format(V=vaddr) if status_formula_tmpl else sub)
    st.font = S.F_KPI_SUB; st.fill = S.fill(S.CARD_BG)
    st.alignment = S.Alignment(horizontal="left", vertical="center", indent=1)
    # borders around card
    for rr in range(top, top + 3):
        for cc in (leftcol, leftcol + 1):
            ex.cell(row=rr, column=cc).border = S.box_thin
    if status_formula_tmpl:
        apply_ryg_word(ex, f"{L}{top+2}")
    return vaddr

# value formula fragments using current month
tot_cust = sumifs(CD, "C", ("A", PM))
new_sales = sumifs(CD, "D", ("A", PM))
disc = sumifs(CD, "E", ("A", PM))
homes = sumifs(CD, "F", ("A", PM))
prior_cust = sumifs(CD, "C", ("B", f"{PIDX}-1"))
mrr = sumifs(FD, "D", ("A", PM))
rev = sumifs(FD, "C", ("A", PM))
capex_m = sumifs(FD, "E", ("A", PM))
opex_m = sumifs(FD, "F", ("A", PM))
bud_rev = sumifs(FD, "J", ("A", PM))
bud_opex = sumifs(FD, "K", ("A", PM))
inst_sched_ytd = sumifs(OD, "F", ("B", f"\"<=\"&{PIDX}"))
inst_done_ytd = sumifs(OD, "G", ("B", f"\"<=\"&{PIDX}"))
avg_days = avgifs(OD, "H", ("A", PM))
tickets = sumifs(OD, "I", ("A", PM))
cash_now = sumifs(FD, "N", ("A", PM))
fcast_rev = sumifs(FD, "M", ("A", PM))
contractor_m = sumifs(FD, "H", ("A", PM))
grant_recv_ytd = f'SUMIFS({rng(GR,"F")},{rng(GR,"F")},">0")'
grant_outstanding = f'SUM({rng(GR,"E")})-SUM({rng(GR,"F")})'
# active = projects in any non-Complete status (explicit list → robust vs blank-row padding)
active_proj = ("(" + countifs(PRJ, ("F", '"On Track"')) + "+" +
               countifs(PRJ, ("F", '"At Risk"')) + "+" +
               countifs(PRJ, ("F", '"Behind"')) + ")")
behind_proj = countifs(PRJ, ("F", '"Behind"'))
major_risks = f'COUNTIFS({rng(RR,"F")},">=15")'
decisions = countifs(BA, ("I", '"Yes"'), ("H", '"<>Complete"'))

# Row 1 of cards (top=8)
r1 = 8
exec_card(r1, 2, "TOTAL CUSTOMERS", f"={tot_cust}", NUM, None,
          sub="End-of-month subscribers")
exec_card(r1, 4, "NEW SALES (MTD)", f"={new_sales}", NUM,
          '=IF({V}>=SUMIFS(Sales_Targets!$C$4:$C$1003,Sales_Targets!$A$4:$A$1003,'+PM+'),"GREEN",IF({V}>=0.9*SUMIFS(Sales_Targets!$C$4:$C$1003,Sales_Targets!$A$4:$A$1003,'+PM+'),"YELLOW","RED"))')
exec_card(r1, 6, "DISCONNECTS (MTD)", f"={disc}", NUM,
          '=IF({V}<=0.02*'+tot_cust+',"GREEN",IF({V}<=0.03*'+tot_cust+',"YELLOW","RED"))')
exec_card(r1, 8, "NET ADDS (MTD)", f"={new_sales}-{disc}", NUM,
          '=IF({V}>0,"GREEN",IF({V}=0,"YELLOW","RED"))')
exec_card(r1, 10, "TAKE RATE", f"=IF({homes}=0,0,{tot_cust}/{homes})", PCT,
          '=IF({V}>=0.35,"GREEN",IF({V}>=0.25,"YELLOW","RED"))')

# Row 2 (top=13)
r2 = 13
exec_card(r2, 2, "REVENUE (MTD)", f"={rev}", CUR, None, sub="Total billed this month")
exec_card(r2, 4, "ARPU", f"=IF({tot_cust}=0,0,{mrr}/{tot_cust})", CUR2,
          '=IF({V}>=75,"GREEN",IF({V}>=65,"YELLOW","RED"))')
exec_card(r2, 6, "MRR", f"={mrr}", CUR, None, sub="Monthly recurring revenue")
exec_card(r2, 8, "CHURN RATE", f"=IF({prior_cust}=0,0,{disc}/{prior_cust})", PCT,
          '=IF({V}<=0.015,"GREEN",IF({V}<=0.025,"YELLOW","RED"))')
exec_card(r2, 10, "HOMES PASSED", f"={homes}", NUM, None, sub="Cumulative passings")

# Row 3 (top=18)
r3 = 18
exec_card(r3, 2, "ACTIVE PROJECTS", f"={active_proj}", "0", None, sub="Capital builds in flight")
exec_card(r3, 4, "PROJECTS BEHIND", f"={behind_proj}", "0",
          '=IF({V}=0,"GREEN",IF({V}<=1,"YELLOW","RED"))')
exec_card(r3, 6, "INSTALL BACKLOG", f"={inst_sched_ytd}-{inst_done_ytd}", NUM,
          '=IF({V}<=200,"GREEN",IF({V}<=400,"YELLOW","RED"))')
exec_card(r3, 8, "AVG DAYS TO INSTALL", f"={avg_days}", DEC1,
          '=IF({V}<=7,"GREEN",IF({V}<=10,"YELLOW","RED"))')
exec_card(r3, 10, "TROUBLE TICKETS (MTD)", f"={tickets}", NUM,
          '=IF({V}<=250,"GREEN",IF({V}<=320,"YELLOW","RED"))')

# Row 4 (top=23)
r4 = 23
exec_card(r4, 2, "BUDGET vs ACTUAL (REV)", f"={rev}-{bud_rev}", CUR,
          '=IF({V}>=0,"GREEN",IF({V}>=-0.05*'+bud_rev+',"YELLOW","RED"))')
exec_card(r4, 4, "CASH (END OF MONTH)", f"={cash_now}", CUR,
          '=IF({V}>=3000000,"GREEN",IF({V}>=1500000,"YELLOW","RED"))')
exec_card(r4, 6, "90-DAY CASH FORECAST", f"={cash_now}+3*{fcast_rev}+{grant_outstanding}-3*({opex_m}+{capex_m}+{contractor_m})", CUR,
          '=IF({V}>=1500000,"GREEN",IF({V}>=500000,"YELLOW","RED"))')
exec_card(r4, 8, "GRANT REIMB RECEIVED", f"={grant_recv_ytd}", CUR, None,
          sub="Outstanding shown on Financial tab")
exec_card(r4, 10, "GRANT OUTSTANDING", f"={grant_outstanding}", CUR,
          '=IF({V}<=500000,"GREEN",IF({V}<=1200000,"YELLOW","RED"))')

# Row 5 (top=28): risks + decisions (wider)
r5 = 28
exec_card(r5, 2, "MAJOR RISKS (RED)", f"={major_risks}", "0",
          '=IF({V}=0,"GREEN",IF({V}<=1,"YELLOW","RED"))')
exec_card(r5, 4, "KEY DECISIONS NEEDED", f"={decisions}", "0",
          '=IF({V}=0,"GREEN",IF({V}<=3,"YELLOW","RED"))')
# Generated executive summary line
ex.merge_cells(f"F{r5}:L{r5+2}")
summ = ex.cell(row=r5, column=6)
summ.value = ('="As of "&C5&": "&' + tot_cust + '&" customers, net adds "&(' + new_sales + '-' + disc +
              ')&" ("&TEXT(IF(' + prior_cust + '=0,0,' + disc + '/' + prior_cust + '),"0.0%")&" churn). '
              'Revenue "&TEXT(' + rev + ',"$#,##0")&" vs budget "&TEXT(' + bud_rev + ',"$#,##0")&". '
              '"&' + active_proj + '&" active projects, "&' + behind_proj + '&" behind. '
              'Install backlog "&(' + inst_sched_ytd + '-' + inst_done_ytd + ')&", avg "&TEXT(' + avg_days + ',"0.0")&" days. '
              '"&' + major_risks + '&" red risk(s), "&' + decisions + '&" decision(s) need executive action."')
summ.font = S.F_BODY; summ.alignment = S.LEFT_TOP; summ.fill = S.fill(S.LIGHT_BG)
for rr in range(r5, r5 + 3):
    for cc in range(6, 13):
        ex.cell(row=rr, column=cc).border = S.box_thin
ex.cell(row=r5, column=6)
# label above summary
ex.cell(row=r5 - 0, column=6)
# small caption
ex["F27"] = "AUTO-GENERATED EXECUTIVE SUMMARY"; ex["F27"].font = S.F_KPI_LABEL

# Section header for cards
S.section_header(ex, 7, "COMPANY HEALTH  —  KPI SCORECARD (current reporting month)", 2, 11, S.SLATE)

# ---- MTD / YTD / Rolling-12 rollup table --------------------------------
rt = 33
S.section_header(ex, rt, "TIME-SERIES ROLLUPS  —  This Month / YTD / Rolling-12 / Prior Month / Goal / Variance", 2, 11, S.SLATE)
rt += 1
hdrs = ["Metric", "This Month", "YTD", "Rolling 12", "Prior Month", "Goal (MTD)", "Variance", "Status"]
for i, h in enumerate(hdrs):
    cell = ex.cell(row=rt, column=2 + i, value=h)
    cell.font = S.F_HDR; cell.fill = S.fill(S.TABLE_HDR); cell.alignment = S.CENTER
    cell.border = S.box_thin

rollups = [
    # name, calc-col-header, agg('sum'/'avg'/'last'), fmt, goal_formula, good_dir
    ("New Sales", "New Sales", "sum", NUM,
     f'SUMIFS(Sales_Targets!$C$4:$C$1003,Sales_Targets!$A$4:$A$1003,{PM})', "high"),
    ("Disconnects", "Disconnects", "sum", NUM, "", "low"),
    ("Net Adds", "Net Adds", "sum", NUM, "", "high"),
    ("Revenue", "Revenue", "sum", CUR, f'SUMIFS(Financial_Data!$J$4:$J$1003,Financial_Data!$A$4:$A$1003,{PM})', "high"),
    ("MRR", "MRR", "last", CUR, "", "high"),
    ("CapEx", "CapEx", "sum", CUR, f'SUMIFS(Financial_Data!$L$4:$L$1003,Financial_Data!$A$4:$A$1003,{PM})', "low"),
    ("OpEx", "OpEx", "sum", CUR, f'SUMIFS(Financial_Data!$K$4:$K$1003,Financial_Data!$A$4:$A$1003,{PM})', "low"),
    ("Installs Completed", "Installs Completed", "sum", NUM, "", "high"),
    ("Trouble Tickets", "Trouble Tickets", "sum", NUM, "", "low"),
    ("Activations", "Activations", "sum", NUM, "", "high"),
]
def calc_col_range(header):
    col = CALC[header]
    return f"Calc!${col}$2:${col}$13"

r = rt + 1
for name, header, agg, fmt, goal_f, good in rollups:
    cr = calc_col_range(header)
    pcol = "Calc!$B$2:$B$13"
    this_m = f'=SUMIFS({cr},Calc!$A$2:$A$13,{PM})'
    if agg == "avg":
        this_m = f'=AVERAGEIFS({cr},Calc!$A$2:$A$13,{PM})'
    ytd = f'=SUMIFS({cr},{pcol},"<="&{PIDX})'
    if agg == "last":
        ytd = f'=SUMIFS({cr},Calc!$A$2:$A$13,{PM})'
    roll = f'=SUMIFS({cr},{pcol},">"&({PIDX}-12))'
    if agg == "last":
        roll = f'=SUMIFS({cr},Calc!$A$2:$A$13,{PM})'
    prior = f'=SUMIFS({cr},{pcol},{PIDX}-1)'
    ex.cell(row=r, column=2, value=name).font = S.F_BODY_B
    tmc = ex.cell(row=r, column=3, value=this_m); tmc.number_format = fmt
    yc = ex.cell(row=r, column=4, value=ytd); yc.number_format = fmt
    rc = ex.cell(row=r, column=5, value=roll); rc.number_format = fmt
    pc = ex.cell(row=r, column=6, value=prior); pc.number_format = fmt
    L = get_column_letter(3)
    if goal_f:
        gc = ex.cell(row=r, column=7, value="=" + goal_f); gc.number_format = fmt
        var = ex.cell(row=r, column=8, value=f"=C{r}-G{r}"); var.number_format = fmt
        if good == "high":
            stf = f'=IF(C{r}>=G{r},"GREEN",IF(C{r}>=0.9*G{r},"YELLOW","RED"))'
        else:
            stf = f'=IF(C{r}<=G{r},"GREEN",IF(C{r}<=1.1*G{r},"YELLOW","RED"))'
        ex.cell(row=r, column=9, value=stf).alignment = S.CENTER
    else:
        ex.cell(row=r, column=7, value="—").alignment = S.CENTER
        # variance vs prior month
        var = ex.cell(row=r, column=8, value=f"=C{r}-F{r}"); var.number_format = fmt
        if good == "high":
            stf = f'=IF(C{r}>=F{r},"GREEN",IF(C{r}>=0.95*F{r},"YELLOW","RED"))'
        else:
            stf = f'=IF(C{r}<=F{r},"GREEN",IF(C{r}<=1.05*F{r},"YELLOW","RED"))'
        ex.cell(row=r, column=9, value=stf).alignment = S.CENTER
    for cc in range(2, 10):
        ex.cell(row=r, column=cc).border = S.box_thin
    r += 1
apply_ryg_word(ex, f"I{rt+1}:I{r-1}")

# ---- Top risks + decisions mini-lists -----------------------------------
risk_top = r + 1
S.section_header(ex, risk_top, "TOP OPEN RISKS  (highest score)", 2, 6, S.SLATE)
S.section_header(ex, risk_top, "DECISIONS NEEDED FROM LEADERSHIP / BOARD", 7, 11, S.SLATE)
hr = risk_top + 1
for i, h in enumerate(["Risk", "Score", "RYG"]):
    cc = ex.cell(row=hr, column=2 + i, value=h); cc.font = S.F_HDR
    cc.fill = S.fill(S.TABLE_HDR); cc.alignment = S.CENTER; cc.border = S.box_thin
ex.merge_cells(f"B{hr}:D{hr}") if False else None
# top 5 risks by score using LARGE + INDEX/MATCH
for k in range(1, 6):
    rr = hr + k
    score_cell = f'=LARGE(Risk_Register!$F$4:$F$1003,{k})'
    # description by matching the k-th largest (approx; ties tolerated)
    desc = (f'=IFERROR(INDEX(Risk_Register!$B$4:$B$1003,MATCH(LARGE(Risk_Register!$F$4:$F$1003,{k}),Risk_Register!$F$4:$F$1003,0)),"")')
    ex.merge_cells(f"B{rr}:C{rr}")
    dcell = ex.cell(row=rr, column=2, value=desc); dcell.font = S.F_SMALL
    dcell.alignment = S.LEFT
    scell = ex.cell(row=rr, column=4, value=score_cell); scell.alignment = S.CENTER
    rygc = ex.cell(row=rr, column=5,
                   value=f'=IF(D{rr}>=15,"RED",IF(D{rr}>=8,"YELLOW","GREEN"))')
    rygc.alignment = S.CENTER
    for cc in range(2, 6):
        ex.cell(row=rr, column=cc).border = S.box_thin
apply_ryg_word(ex, f"E{hr+1}:E{hr+5}")
# Decisions list
for i, h in enumerate(["Decision / Action", "Owner", "Priority"]):
    cc = ex.cell(row=hr, column=7 + (i if i == 0 else i + 1), value=h)
def _decis_idx(k):
    # k-th row offset (1-based within data) of board actions needing a decision,
    # non-array via AGGREGATE (ignores the #DIV/0! produced for non-matching rows)
    return (f'AGGREGATE(15,6,(ROW(Board_Actions!$I$4:$I$1003)-3)/'
            f'((Board_Actions!$I$4:$I$1003="Yes")*(Board_Actions!$H$4:$H$1003<>"Complete")),{k})')
for k in range(1, 6):
    rr = hr + k
    ex.merge_cells(f"G{rr}:I{rr}")
    idxf = _decis_idx(k)
    desc = f'=IFERROR(INDEX(Board_Actions!$B$4:$B$1003,{idxf}),"")'
    dcell = ex.cell(row=rr, column=7, value=desc); dcell.font = S.F_SMALL
    dcell.alignment = S.LEFT
    own = f'=IFERROR(INDEX(Board_Actions!$D$4:$D$1003,{idxf}),"")'
    pr = f'=IFERROR(INDEX(Board_Actions!$G$4:$G$1003,{idxf}),"")'
    ex.merge_cells(f"J{rr}:J{rr}")
    ex.cell(row=rr, column=10, value=own).font = S.F_SMALL
    ex.cell(row=rr, column=11, value=pr).alignment = S.CENTER
    for cc in range(7, 12):
        ex.cell(row=rr, column=cc).border = S.box_thin
# fix decisions header cells
ex.cell(row=hr, column=7, value="Decision / Action").font = S.F_HDR
ex.merge_cells(f"G{hr}:I{hr}")
ex.cell(row=hr, column=7).fill = S.fill(S.TABLE_HDR)
ex.cell(row=hr, column=7).font = S.F_HDR
ex.cell(row=hr, column=7).alignment = S.CENTER
ex.cell(row=hr, column=10, value="Owner").font = S.F_HDR
ex.cell(row=hr, column=10).fill = S.fill(S.TABLE_HDR); ex.cell(row=hr, column=10).alignment = S.CENTER
ex.cell(row=hr, column=11, value="Priority").font = S.F_HDR
ex.cell(row=hr, column=11).fill = S.fill(S.TABLE_HDR); ex.cell(row=hr, column=11).alignment = S.CENTER
for cc in (7, 10, 11):
    ex.cell(row=hr, column=cc).border = S.box_thin

# ---- Exec charts --------------------------------------------------------
chart_row = hr + 8
S.section_header(ex, chart_row, "TREND CHARTS", 2, 11, S.SLATE)
add_line_chart(ex, f"B{chart_row+1}", "Net Adds Trend", ["New Sales", "Disconnects", "Net Adds"])
add_line_chart(ex, f"H{chart_row+1}", "Revenue vs Budget", ["Revenue", "Budget Revenue"], fmt=CUR)
add_line_chart(ex, f"B{chart_row+17}", "Avg Days to Install", ["Avg Days Install"], fmt=DEC1)
add_line_chart(ex, f"H{chart_row+17}", "Install Backlog (running)", ["Install Backlog"])

ex.freeze_panes = "A6"


# ==========================================================================
# 5. SALES DASHBOARD
# ==========================================================================
sa = wb.create_sheet("Sales_Dashboard")
S.page_setup(sa, tab_color=S.ACCENT_2)
S.set_widths(sa, {get_column_letter(c): 13 for c in range(1, 14)})
sa.column_dimensions["A"].width = 3
sa.merge_cells("A1:M1")
c = sa["A1"]; c.value = "SALES MANAGEMENT DASHBOARD"; c.font = S.F_TITLE
c.fill = S.fill(S.NAVY); c.alignment = S.Alignment(horizontal="left", vertical="center", indent=1)
sa.row_dimensions[1].height = 28
sa.merge_cells("A2:M2")
c = sa["A2"]; c.value = "Leads → Qualified → Connects  •  pipeline, channels, counties, reps, goal vs actual  •  reporting month set on Exec Dashboard"
c.font = S.F_SUBTITLE; c.fill = S.fill(S.SLATE)
c.alignment = S.Alignment(horizontal="left", vertical="center", indent=1)

# KPI cards (reuse exec_card-style inline)
def card(ws, top, leftcol, label, value_formula, fmt, status_tmpl=None, sub=""):
    L = get_column_letter(leftcol); R = get_column_letter(leftcol + 1)
    ws.merge_cells(f"{L}{top}:{R}{top}"); ws.merge_cells(f"{L}{top+1}:{R}{top+1}")
    ws.merge_cells(f"{L}{top+2}:{R}{top+2}")
    lab = ws.cell(row=top, column=leftcol, value=label); lab.font = S.F_KPI_LABEL
    lab.fill = S.fill(S.CARD_BG); lab.alignment = S.Alignment(horizontal="left", vertical="center", indent=1)
    val = ws.cell(row=top + 1, column=leftcol, value=value_formula); val.font = S.F_KPI_VALUE_SM
    val.fill = S.fill(S.CARD_BG); val.number_format = fmt
    val.alignment = S.Alignment(horizontal="left", vertical="center", indent=1)
    vaddr = f"{L}{top+1}"
    st = ws.cell(row=top + 2, column=leftcol,
                 value=status_tmpl.format(V=vaddr) if status_tmpl else sub)
    st.font = S.F_KPI_SUB; st.fill = S.fill(S.CARD_BG)
    st.alignment = S.Alignment(horizontal="left", vertical="center", indent=1)
    for rr in range(top, top + 3):
        for cc in (leftcol, leftcol + 1):
            ws.cell(row=rr, column=cc).border = S.box_thin
    if status_tmpl:
        apply_ryg_word(ws, f"{L}{top+2}")
    return vaddr

S.section_header(sa, 4, "SALES KPIs (current reporting month)", 2, 13, S.SLATE)
leads = sumifs(SD, "H", ("A", PM))
qual = sumifs(SD, "I", ("A", PM))
salesm = sumifs(SD, "J", ("A", PM))
newmrr = sumifs(SD, "K", ("A", PM))
goal = f'SUMIFS({rng(ST,"C")},{rng(ST,"A")},{PM})'
pipe_open = f'SUMIFS({rng(PL,"G")},{rng(PL,"F")},"<>Closed-Won",{rng(PL,"F")},"<>Closed-Lost")'
won_rev = f'SUMIFS({rng(PL,"G")},{rng(PL,"F")},"Closed-Won")'
ent_opps = f'COUNTIFS({rng(PL,"E")},"Enterprise/DIA",{rng(PL,"F")},"<>Closed-Lost",{rng(PL,"F")},"<>Closed-Won")'
hoa_opps = f'COUNTIFS({rng(PL,"E")},"HOA/Developer")'
bulk_opps = f'COUNTIFS({rng(PL,"E")},"Bulk Agreement")'
lost_cnt = f'COUNTIFS({rng(PL,"F")},"Closed-Lost")'
knocks = sumifs(SD, "L", ("A", PM))
res_sales = sumifs(SD, "J", ("A", PM), ("D", '"Residential"'))
bus_sales = sumifs(SD, "J", ("A", PM), ("D", '"Business"'))

r = 5
card(sa, r, 2, "LEADS (MTD)", f"={leads}", NUM, sub="Top of funnel")
card(sa, r, 4, "QUALIFIED (MTD)", f"={qual}", NUM, sub="Sales-qualified")
card(sa, r, 6, "CONVERSION RATE", f"=IF({leads}=0,0,{salesm}/{leads})", PCT,
     '=IF({V}>=0.25,"GREEN",IF({V}>=0.15,"YELLOW","RED"))')
card(sa, r, 8, "CONNECTS (MTD)", f"={salesm}", NUM, sub="Closed-won units")
card(sa, r, 10, "GOAL (MTD)", f"={goal}", NUM, sub="Monthly target")
card(sa, r, 12, "VARIANCE TO GOAL", f"={salesm}-{goal}", NUM,
     '=IF({V}>=0,"GREEN",IF({V}>=-0.1*'+goal+',"YELLOW","RED"))')
r = 10
card(sa, r, 2, "NEW MRR ADDED", f"={newmrr}", CUR, sub="Recurring $ added")
card(sa, r, 4, "RESIDENTIAL SALES", f"={res_sales}", NUM)
card(sa, r, 6, "BUSINESS SALES", f"={bus_sales}", NUM)
card(sa, r, 8, "PIPELINE VALUE (OPEN)", f"={pipe_open}", CUR,
     '=IF({V}>=1500000,"GREEN",IF({V}>=800000,"YELLOW","RED"))')
card(sa, r, 10, "CLOSED-WON (ARR)", f"={won_rev}", CUR)
card(sa, r, 12, "LOST OPPORTUNITIES", f"={lost_cnt}", "0")
r = 15
card(sa, r, 2, "ENTERPRISE OPPS (OPEN)", f"={ent_opps}", "0", sub="DIA pipeline count")
card(sa, r, 4, "HOA / DEVELOPER OPPS", f"={hoa_opps}", "0")
card(sa, r, 6, "BULK AGREEMENT OPPS", f"={bulk_opps}", "0")
card(sa, r, 8, "DOOR KNOCKS (MTD)", f"={knocks}", NUM, sub="D2D activity")
card(sa, r, 10, "QUAL → CLOSE RATE", f"=IF({qual}=0,0,{salesm}/{qual})", PCT,
     '=IF({V}>=0.5,"GREEN",IF({V}>=0.3,"YELLOW","RED"))')
card(sa, r, 12, "AVG NEW MRR / CONNECT", f"=IF({salesm}=0,0,{newmrr}/{salesm})", CUR2)

# ---- Aggregation blocks for charts (by county / channel / rep / stage) --
def agg_block(ws, top, left, title, label_list, value_formula_fn, fmt=NUM):
    ws.cell(row=top, column=left, value=title).font = S.F_BODY_B
    hr = top + 1
    ws.cell(row=hr, column=left, value="Category").font = S.F_HDR
    ws.cell(row=hr, column=left).fill = S.fill(S.TABLE_HDR)
    ws.cell(row=hr, column=left + 1, value="Value").font = S.F_HDR
    ws.cell(row=hr, column=left + 1).fill = S.fill(S.TABLE_HDR)
    for i, lab in enumerate(label_list):
        rr = hr + 1 + i
        ws.cell(row=rr, column=left, value=lab).font = S.F_SMALL
        v = ws.cell(row=rr, column=left + 1, value=value_formula_fn(lab))
        v.number_format = fmt; v.font = S.F_SMALL
    cat = Reference(ws, min_col=left, min_row=hr + 1, max_row=hr + len(label_list))
    val = Reference(ws, min_col=left + 1, min_row=hr, max_row=hr + len(label_list))
    return cat, val

S.section_header(sa, 20, "ANALYTICS", 2, 13, S.SLATE)
# blocks placed far right / lower to feed charts (rows 21+)
blk_row = 60
c_cat, c_val = agg_block(sa, blk_row, 16, "Sales by County",
    D.COUNTIES, lambda x: f'=SUMIFS({rng(SD,"J")},{rng(SD,"C")},"{x}")')
ch_cat, ch_val = agg_block(sa, blk_row, 19, "Sales by Channel",
    D.CHANNELS, lambda x: f'=SUMIFS({rng(SD,"J")},{rng(SD,"E")},"{x}")')
rp_cat, rp_val = agg_block(sa, blk_row, 22, "Sales by Rep",
    D.REPS, lambda x: f'=SUMIFS({rng(SD,"J")},{rng(SD,"G")},"{x}")')
st_cat, st_val = agg_block(sa, blk_row, 25, "Pipeline by Stage",
    D.STAGES[:-1], lambda x: f'=SUMIFS({rng(PL,"G")},{rng(PL,"F")},"{x}")', fmt=CUR)
ls_cat, ls_val = agg_block(sa, blk_row, 28, "Lost Reasons",
    D.LOST_REASONS, lambda x: f'=COUNTIFS({rng(PL,"J")},"{x}")')

# Sales trend (monthly connects) from Calc New Sales + goal: build a small series on Sales sheet
# Goal-vs-actual monthly block
gva_row = 75
sa.cell(row=gva_row, column=16, value="Goal vs Actual (monthly)").font = S.F_BODY_B
sa.cell(row=gva_row + 1, column=16, value="Month").font = S.F_HDR
sa.cell(row=gva_row + 1, column=17, value="Actual").font = S.F_HDR
sa.cell(row=gva_row + 1, column=18, value="Goal").font = S.F_HDR
for i in range(12):
    rr = gva_row + 2 + i
    sa.cell(row=rr, column=16, value=f"=Sales_Targets!A{DATA_START+i}")
    sa.cell(row=rr, column=17, value=f'=SUMIFS({rng(SD,"J")},{rng(SD,"B")},Sales_Targets!B{DATA_START+i})')
    sa.cell(row=rr, column=18, value=f"=Sales_Targets!C{DATA_START+i}")
gva_cat = Reference(sa, min_col=16, min_row=gva_row + 2, max_row=gva_row + 13)
gva_val = Reference(sa, min_col=17, min_row=gva_row + 1, max_row=gva_row + 13)
gva_goal = Reference(sa, min_col=18, min_row=gva_row + 1, max_row=gva_row + 13)

# Charts
add_bar_from_block(sa, "B21", "Sales by County (connects)", c_cat, c_val)
add_pie_from_block(sa, "F21", "Sales by Channel", ch_cat, ch_val)
add_bar_from_block(sa, "B37", "Rep Performance (connects)", rp_cat, rp_val, horizontal=True)
add_bar_from_block(sa, "F37", "Pipeline by Stage ($)", st_cat, st_val, barfmt=CUR)
# Goal vs actual line + sales trend
gv = LineChart(); gv.title = "Goal vs Actual (monthly connects)"; gv.height = 7.5; gv.width = 13
gv.add_data(gva_val, titles_from_data=True); gv.add_data(gva_goal, titles_from_data=True)
gv.set_categories(gva_cat); sa.add_chart(gv, "J21")
add_pie_from_block(sa, "J37", "Lost Reasons", ls_cat, ls_val)
sa.freeze_panes = "A5"


# ==========================================================================
# 6. OPERATIONS DASHBOARD
# ==========================================================================
op = wb.create_sheet("Ops_Dashboard")
S.page_setup(op, tab_color="7C3AED")
S.set_widths(op, {get_column_letter(c): 13 for c in range(1, 14)})
op.column_dimensions["A"].width = 3
op.merge_cells("A1:M1")
c = op["A1"]; c.value = "OPERATIONS MANAGEMENT DASHBOARD"; c.font = S.F_TITLE
c.fill = S.fill(S.NAVY); c.alignment = S.Alignment(horizontal="left", vertical="center", indent=1)
op.row_dimensions[1].height = 28
op.merge_cells("A2:M2")
c = op["A2"]; c.value = "Build → Drop → Install → Activate  •  trouble tickets, contractors, project health  •  reporting month set on Exec Dashboard"
c.font = S.F_SUBTITLE; c.fill = S.fill(S.SLATE)
c.alignment = S.Alignment(horizontal="left", vertical="center", indent=1)

S.section_header(op, 4, "OPERATIONS KPIs (current reporting month)", 2, 13, S.SLATE)
hp_add = sumifs(OD, "C", ("A", PM))
footage = sumifs(OD, "D", ("A", PM))
drops = sumifs(OD, "E", ("A", PM))
isched = sumifs(OD, "F", ("A", PM))
idone = sumifs(OD, "G", ("A", PM))
adays = avgifs(OD, "H", ("A", PM))
tix = sumifs(OD, "I", ("A", PM))
rtix = sumifs(OD, "J", ("A", PM))
outg = sumifs(OD, "K", ("A", PM))
acts = sumifs(OD, "L", ("A", PM))
splices = sumifs(OD, "M", ("A", PM))
cphp = f'IF({hp_add}=0,0,{capex_m}/{hp_add})'
backlog = f'{inst_sched_ytd}-{inst_done_ytd}'
proj_ontrack = countifs(PRJ, ("F", '"On Track"'))
proj_atrisk = countifs(PRJ, ("F", '"At Risk"'))
proj_behind = countifs(PRJ, ("F", '"Behind"'))

r = 5
card(op, r, 2, "HOMES PASSED ADDED", f"={hp_add}", NUM, sub="This month")
card(op, r, 4, "FOOTAGE BUILT", f"={footage}", NUM, sub="Linear feet")
card(op, r, 6, "COST / HOME PASSED", f"={cphp}", CUR,
     '=IF({V}<=700,"GREEN",IF({V}<=950,"YELLOW","RED"))')
card(op, r, 8, "DROPS COMPLETED", f"={drops}", NUM)
card(op, r, 10, "SPLICES COMPLETED", f"={splices}", NUM)
card(op, r, 12, "ACTIVATIONS", f"={acts}", NUM)
r = 10
card(op, r, 2, "INSTALLS SCHEDULED", f"={isched}", NUM)
card(op, r, 4, "INSTALLS COMPLETED", f"={idone}", NUM,
     '=IF({V}>={isched_val},"GREEN",IF({V}>=0.85*{isched_val},"YELLOW","RED"))'.replace("{isched_val}", isched))
card(op, r, 6, "INSTALL BACKLOG", f"={backlog}", NUM,
     '=IF({V}<=200,"GREEN",IF({V}<=400,"YELLOW","RED"))')
card(op, r, 8, "AVG DAYS TO INSTALL", f"={adays}", DEC1,
     '=IF({V}<=7,"GREEN",IF({V}<=10,"YELLOW","RED"))')
card(op, r, 10, "TROUBLE TICKETS", f"={tix}", NUM,
     '=IF({V}<=250,"GREEN",IF({V}<=320,"YELLOW","RED"))')
card(op, r, 12, "REPEAT TICKET %", f"=IF({tix}=0,0,{rtix}/{tix})", PCT,
     '=IF({V}<=0.1,"GREEN",IF({V}<=0.15,"YELLOW","RED"))')
r = 15
card(op, r, 2, "OUTAGES (MTD)", f"={outg}", "0",
     '=IF({V}<=2,"GREEN",IF({V}<=4,"YELLOW","RED"))')
card(op, r, 4, "PROJECTS ON TRACK", f"={proj_ontrack}", "0")
card(op, r, 6, "PROJECTS AT RISK", f"={proj_atrisk}", "0",
     '=IF({V}=0,"GREEN",IF({V}<=2,"YELLOW","RED"))')
card(op, r, 8, "PROJECTS BEHIND", f"={proj_behind}", "0",
     '=IF({V}=0,"GREEN",IF({V}<=1,"YELLOW","RED"))')
card(op, r, 10, "AVG PROJECT % COMPLETE", f'=AVERAGE({rng(PRJ,"E")})', PCT0)
card(op, r, 12, "AVG CONTRACTOR SCORE", f'=AVERAGE({rng(PRJ,"Q")})', DEC1,
     '=IF({V}>=8,"GREEN",IF({V}>=6.5,"YELLOW","RED"))')

# Project build-progress block (per project) for chart
S.section_header(op, 20, "PROJECT HEALTH & ANALYTICS", 2, 13, S.SLATE)
pb_row = 60
op.cell(row=pb_row, column=16, value="Build Progress by Project").font = S.F_BODY_B
op.cell(row=pb_row + 1, column=16, value="Project").font = S.F_HDR
op.cell(row=pb_row + 1, column=17, value="% Complete").font = S.F_HDR
for i in range(prj_last - DATA_START + 1):
    rr = pb_row + 2 + i
    op.cell(row=rr, column=16, value=f"=Project_Data!A{DATA_START+i}")
    op.cell(row=rr, column=17, value=f"=Project_Data!E{DATA_START+i}").number_format = PCT0
pb_cat = Reference(op, min_col=16, min_row=pb_row + 2, max_row=pb_row + 1 + (prj_last - DATA_START + 1))
pb_val = Reference(op, min_col=17, min_row=pb_row + 1, max_row=pb_row + 1 + (prj_last - DATA_START + 1))

# Project status pie block
ps_row = 80
op.cell(row=ps_row, column=16, value="Project Status").font = S.F_BODY_B
op.cell(row=ps_row + 1, column=16, value="Status").font = S.F_HDR
op.cell(row=ps_row + 1, column=17, value="Count").font = S.F_HDR
for i, sname in enumerate(["On Track", "At Risk", "Behind", "Complete"]):
    rr = ps_row + 2 + i
    op.cell(row=rr, column=16, value=sname)
    op.cell(row=rr, column=17, value=f'=COUNTIFS({rng(PRJ,"F")},"{sname}")')
ps_cat = Reference(op, min_col=16, min_row=ps_row + 2, max_row=ps_row + 5)
ps_val = Reference(op, min_col=17, min_row=ps_row + 1, max_row=ps_row + 5)

# Contractor performance block (avg score by contractor)
contractors = sorted(set(p[15] for p in D.PROJECTS))
cp_row = 90
op.cell(row=cp_row, column=16, value="Contractor Performance").font = S.F_BODY_B
op.cell(row=cp_row + 1, column=16, value="Contractor").font = S.F_HDR
op.cell(row=cp_row + 1, column=17, value="Avg Score").font = S.F_HDR
for i, cn in enumerate(contractors):
    rr = cp_row + 2 + i
    op.cell(row=rr, column=16, value=cn)
    op.cell(row=rr, column=17, value=f'=IFERROR(AVERAGEIFS({rng(PRJ,"Q")},{rng(PRJ,"P")},"{cn}"),0)').number_format = DEC1
cp_cat = Reference(op, min_col=16, min_row=cp_row + 2, max_row=cp_row + 1 + len(contractors))
cp_val = Reference(op, min_col=17, min_row=cp_row + 1, max_row=cp_row + 1 + len(contractors))

# Trouble ticket categories (editable helper block) for pie
tc_row = 100
op.cell(row=tc_row, column=16, value="Trouble Tickets by Category (editable)").font = S.F_BODY_B
op.cell(row=tc_row + 1, column=16, value="Category").font = S.F_HDR
op.cell(row=tc_row + 1, column=17, value="Count").font = S.F_HDR
tcats = [("No Signal / Down", 92), ("Slow Speed", 64), ("Intermittent", 58),
         ("ONT / Equipment", 41), ("Outside Plant", 33), ("Billing-related", 22)]
for i, (cn, cv) in enumerate(tcats):
    rr = tc_row + 2 + i
    op.cell(row=rr, column=16, value=cn)
    op.cell(row=rr, column=17, value=cv)
tc_cat = Reference(op, min_col=16, min_row=tc_row + 2, max_row=tc_row + 1 + len(tcats))
tc_val = Reference(op, min_col=17, min_row=tc_row + 1, max_row=tc_row + 1 + len(tcats))

# Charts
add_bar_from_block(op, "B21", "Build Progress by Project", pb_cat, pb_val, barfmt=PCT0, horizontal=True, width=14)
add_pie_from_block(op, "H21", "Projects On Track / At Risk / Behind", ps_cat, ps_val)
add_line_chart(op, "B37", "Avg Days to Install Trend", ["Avg Days Install"], fmt=DEC1)
add_line_chart(op, "H37", "Install Backlog Trend", ["Install Backlog"])
add_bar_from_block(op, "B53", "Contractor Performance (avg score)", cp_cat, cp_val, barfmt=DEC1, horizontal=True)
add_pie_from_block(op, "H53", "Trouble Tickets by Category", tc_cat, tc_val)
op.freeze_panes = "A5"


# ==========================================================================
# 7. FINANCIAL DASHBOARD
# ==========================================================================
fi = wb.create_sheet("Financial_Dashboard")
S.page_setup(fi, tab_color="0E7C86")
S.set_widths(fi, {get_column_letter(c): 13 for c in range(1, 14)})
fi.column_dimensions["A"].width = 3
fi.merge_cells("A1:M1")
c = fi["A1"]; c.value = "FINANCIAL MANAGEMENT DASHBOARD"; c.font = S.F_TITLE
c.fill = S.fill(S.NAVY); c.alignment = S.Alignment(horizontal="left", vertical="center", indent=1)
fi.row_dimensions[1].height = 28
fi.merge_cells("A2:M2")
c = fi["A2"]; c.value = "Revenue • CapEx/OpEx • budget vs actual • cash forecast • grant reimbursement • margin by service line  •  reporting month set on Exec Dashboard"
c.font = S.F_SUBTITLE; c.fill = S.fill(S.SLATE)
c.alignment = S.Alignment(horizontal="left", vertical="center", indent=1)

S.section_header(fi, 4, "FINANCIAL KPIs (current reporting month)", 2, 13, S.SLATE)
labor_m = sumifs(FD, "G", ("A", PM))
grant_m = sumifs(FD, "I", ("A", PM))
bud_capex = sumifs(FD, "L", ("A", PM))
cost_install = f'IF({idone}=0,0,{contractor_m}/{idone})'
ytd_rev = f'SUMIFS({rng(FD,"C")},{rng(FD,"B")},"<="&{PIDX})'
ytd_capex = f'SUMIFS({rng(FD,"E")},{rng(FD,"B")},"<="&{PIDX})'
ytd_opex = f'SUMIFS({rng(FD,"F")},{rng(FD,"B")},"<="&{PIDX})'
ytd_grant = f'SUMIFS({rng(FD,"I")},{rng(FD,"B")},"<="&{PIDX})'

r = 5
card(fi, r, 2, "REVENUE (MTD)", f"={rev}", CUR,
     '=IF({V}>='+bud_rev+',"GREEN",IF({V}>=0.95*'+bud_rev+',"YELLOW","RED"))')
card(fi, r, 4, "MRR", f"={mrr}", CUR)
card(fi, r, 6, "ARPU", f"=IF({tot_cust}=0,0,{mrr}/{tot_cust})", CUR2,
     '=IF({V}>=75,"GREEN",IF({V}>=65,"YELLOW","RED"))')
card(fi, r, 8, "CAPITAL SPEND (MTD)", f"={capex_m}", CUR,
     '=IF({V}<='+bud_capex+',"GREEN",IF({V}<=1.1*'+bud_capex+',"YELLOW","RED"))')
card(fi, r, 10, "OPERATING EXPENSE", f"={opex_m}", CUR,
     '=IF({V}<='+bud_opex+',"GREEN",IF({V}<=1.05*'+bud_opex+',"YELLOW","RED"))')
card(fi, r, 12, "LABOR COST", f"={labor_m}", CUR)
r = 10
card(fi, r, 2, "CONTRACTOR COST", f"={contractor_m}", CUR)
card(fi, r, 4, "GRANT REIMB (MTD)", f"={grant_m}", CUR)
card(fi, r, 6, "BUDGET VAR (REV)", f"={rev}-{bud_rev}", CUR,
     '=IF({V}>=0,"GREEN",IF({V}>=-0.05*'+bud_rev+',"YELLOW","RED"))')
card(fi, r, 8, "FORECAST VAR (REV)", f"={rev}-{fcast_rev}", CUR,
     '=IF({V}>=-0.03*'+fcast_rev+',"GREEN",IF({V}>=-0.07*'+fcast_rev+',"YELLOW","RED"))')
card(fi, r, 10, "CASH (END OF MONTH)", f"={cash_now}", CUR,
     '=IF({V}>=3000000,"GREEN",IF({V}>=1500000,"YELLOW","RED"))')
card(fi, r, 12, "90-DAY CASH NEED", f"=3*({opex_m}+{capex_m}+{contractor_m})-3*{fcast_rev}-{grant_outstanding}", CUR,
     '=IF({V}<={cash},"GREEN",IF({V}<=1.5*{cash},"YELLOW","RED"))'.replace("{cash}", cash_now))
r = 15
card(fi, r, 2, "COST / INSTALL", f"={cost_install}", CUR,
     '=IF({V}<=600,"GREEN",IF({V}<=850,"YELLOW","RED"))')
card(fi, r, 4, "COST / HOME PASSED", f"={cphp}", CUR,
     '=IF({V}<=700,"GREEN",IF({V}<=950,"YELLOW","RED"))')
card(fi, r, 6, "GROSS MARGIN %", f"=IF({rev}=0,0,({rev}-({opex_m}+{contractor_m}))/{rev})", PCT,
     '=IF({V}>=0.4,"GREEN",IF({V}>=0.25,"YELLOW","RED"))')
card(fi, r, 8, "REVENUE YTD", f"={ytd_rev}", CUR)
card(fi, r, 10, "CAPEX YTD", f"={ytd_capex}", CUR)
card(fi, r, 12, "GRANT REIMB YTD", f"={ytd_grant}", CUR)

S.section_header(fi, 20, "FINANCIAL ANALYTICS", 2, 13, S.SLATE)
# Expense by category block (current month)
ec_row = 60
fi.cell(row=ec_row, column=16, value="Expense by Category (MTD)").font = S.F_BODY_B
fi.cell(row=ec_row + 1, column=16, value="Category").font = S.F_HDR
fi.cell(row=ec_row + 1, column=17, value="Amount").font = S.F_HDR
exp_cats = [("Labor", labor_m), ("Contractor", contractor_m),
            ("Other OpEx", f"{opex_m}-{labor_m}"), ("CapEx", capex_m)]
for i, (nm, f) in enumerate(exp_cats):
    rr = ec_row + 2 + i
    fi.cell(row=rr, column=16, value=nm)
    fi.cell(row=rr, column=17, value="=" + f).number_format = CUR
ec_cat = Reference(fi, min_col=16, min_row=ec_row + 2, max_row=ec_row + 5)
ec_val = Reference(fi, min_col=17, min_row=ec_row + 1, max_row=ec_row + 5)

# Revenue by product block (current month) + margin
rp_row = 70
fi.cell(row=rp_row, column=16, value="Revenue & Margin by Product (MTD)").font = S.F_BODY_B
for j, h in enumerate(["Product", "Revenue", "Margin %"]):
    fi.cell(row=rp_row + 1, column=16 + j, value=h).font = S.F_HDR
for i, prod in enumerate(D.PRODUCTS):
    rr = rp_row + 2 + i
    fi.cell(row=rr, column=16, value=prod)
    revf = f'SUMIFS({rng(RD,"E")},{rng(RD,"A")},{PM},{rng(RD,"C")},"{prod}")'
    cogf = f'SUMIFS({rng(RD,"F")},{rng(RD,"A")},{PM},{rng(RD,"C")},"{prod}")'
    fi.cell(row=rr, column=17, value="=" + revf).number_format = CUR
    fi.cell(row=rr, column=18, value=f'=IF({revf}=0,0,({revf}-{cogf})/{revf})').number_format = PCT
rp_cat = Reference(fi, min_col=16, min_row=rp_row + 2, max_row=rp_row + 1 + len(D.PRODUCTS))
rp_val = Reference(fi, min_col=17, min_row=rp_row + 1, max_row=rp_row + 1 + len(D.PRODUCTS))
mg_val = Reference(fi, min_col=18, min_row=rp_row + 1, max_row=rp_row + 1 + len(D.PRODUCTS))

# Grant reimbursement pipeline block (Received vs Outstanding by program)
gp_row = 82
fi.cell(row=gp_row, column=16, value="Grant Reimbursement Pipeline").font = S.F_BODY_B
for j, h in enumerate(["Program", "Received", "Outstanding"]):
    fi.cell(row=gp_row + 1, column=16 + j, value=h).font = S.F_HDR
for i, prog in enumerate(D.LISTS["Grant Program"]):
    rr = gp_row + 2 + i
    fi.cell(row=rr, column=16, value=prog)
    fi.cell(row=rr, column=17, value=f'=SUMIFS({rng(GR,"F")},{rng(GR,"B")},"{prog}")').number_format = CUR
    fi.cell(row=rr, column=18, value=f'=SUMIFS({rng(GR,"E")},{rng(GR,"B")},"{prog}")-SUMIFS({rng(GR,"F")},{rng(GR,"B")},"{prog}")').number_format = CUR
gp_cat = Reference(fi, min_col=16, min_row=gp_row + 2, max_row=gp_row + 1 + len(D.LISTS["Grant Program"]))
gp_recv = Reference(fi, min_col=17, min_row=gp_row + 1, max_row=gp_row + 1 + len(D.LISTS["Grant Program"]))
gp_out = Reference(fi, min_col=18, min_row=gp_row + 1, max_row=gp_row + 1 + len(D.LISTS["Grant Program"]))

# Capital spend by project block
cs_row = 92
fi.cell(row=cs_row, column=16, value="Capital Spend by Project").font = S.F_BODY_B
for j, h in enumerate(["Project", "Spent"]):
    fi.cell(row=cs_row + 1, column=16 + j, value=h).font = S.F_HDR
for i in range(prj_last - DATA_START + 1):
    rr = cs_row + 2 + i
    fi.cell(row=rr, column=16, value=f"=Project_Data!A{DATA_START+i}")
    fi.cell(row=rr, column=17, value=f"=Project_Data!L{DATA_START+i}").number_format = CUR
cs_cat = Reference(fi, min_col=16, min_row=cs_row + 2, max_row=cs_row + 1 + (prj_last - DATA_START + 1))
cs_val = Reference(fi, min_col=17, min_row=cs_row + 1, max_row=cs_row + 1 + (prj_last - DATA_START + 1))

# Charts
add_line_chart(fi, "B21", "Revenue Trend vs Budget", ["Revenue", "Budget Revenue"], fmt=CUR)
# Budget vs actual clustered (revenue & opex) — build from Calc
bva = BarChart(); bva.type = "col"; bva.title = "Budget vs Actual (Rev & OpEx, monthly)"
bva.height = 7.5; bva.width = 13
bva.add_data(Reference(calc, min_col=col_idx(CALC["Revenue"]), min_row=1, max_row=13), titles_from_data=True)
bva.add_data(Reference(calc, min_col=col_idx(CALC["Budget Revenue"]), min_row=1, max_row=13), titles_from_data=True)
bva.add_data(Reference(calc, min_col=col_idx(CALC["OpEx"]), min_row=1, max_row=13), titles_from_data=True)
bva.add_data(Reference(calc, min_col=col_idx(CALC["Budget OpEx"]), min_row=1, max_row=13), titles_from_data=True)
bva.set_categories(Reference(calc, min_col=col_idx(CALC["Month"]), min_row=2, max_row=13))
bva.y_axis.numFmt = CUR
fi.add_chart(bva, "H21")
add_line_chart(fi, "B37", "Cash Balance Forecast", ["CapEx"], fmt=CUR)  # placeholder replaced below
# Cash trend from Financial cash column via Calc? cash not in Calc; build small block
cashb_row = 102
fi.cell(row=cashb_row, column=16, value="Cash Trend").font = S.F_BODY_B
fi.cell(row=cashb_row + 1, column=16, value="Month").font = S.F_HDR
fi.cell(row=cashb_row + 1, column=17, value="Cash Balance").font = S.F_HDR
for i in range(12):
    rr = cashb_row + 2 + i
    fi.cell(row=rr, column=16, value=f"=Financial_Data!A{DATA_START+i}")
    fi.cell(row=rr, column=17, value=f"=Financial_Data!N{DATA_START+i}").number_format = CUR
cashb_cat = Reference(fi, min_col=16, min_row=cashb_row + 2, max_row=cashb_row + 13)
cashb_val = Reference(fi, min_col=17, min_row=cashb_row + 1, max_row=cashb_row + 13)
# replace the placeholder cash chart with a proper line chart
cashchart = LineChart(); cashchart.title = "Cash Balance Trend"; cashchart.height = 7.5; cashchart.width = 13
cashchart.add_data(cashb_val, titles_from_data=True); cashchart.set_categories(cashb_cat)
cashchart.y_axis.numFmt = CUR
fi.add_chart(cashchart, "B37")
add_pie_from_block(fi, "H37", "Expense by Category (MTD)", ec_cat, ec_val)
add_bar_from_block(fi, "B53", "Revenue by Product (MTD)", rp_cat, rp_val, barfmt=CUR, horizontal=True)
# grant pipeline clustered
gpc = BarChart(); gpc.type = "col"; gpc.title = "Grant Reimbursement Pipeline"; gpc.height = 7.5; gpc.width = 13
gpc.add_data(gp_recv, titles_from_data=True); gpc.add_data(gp_out, titles_from_data=True)
gpc.set_categories(gp_cat); gpc.y_axis.numFmt = CUR
fi.add_chart(gpc, "H53")
add_bar_from_block(fi, "B69", "Capital Spend by Project", cs_cat, cs_val, barfmt=CUR, horizontal=True, width=14)
fi.freeze_panes = "A5"

print("Dashboards built. Continuing to board report + reference tabs...")

# Save partial so we can import builder2 logic in same file
wb_path = os.path.join(os.path.dirname(__file__), "..", "ISP_COO_Executive_Management_System.xlsx")

# Board report + reference tabs are added by build_part2()
import build_part2
build_part2.add_board_and_reference(
    wb, S, D, dict(PM=PM, PIDX=PIDX, rng=rng, sumifs=sumifs, countifs=countifs,
                   apply_ryg_word=apply_ryg_word, DATA_START=DATA_START,
                   DATA_END=DATA_END, CUR=CUR, NUM=NUM, PCT=PCT, DEC1=DEC1,
                   list_cols=list_cols, FD=FD, CD=CD, OD=OD, ST=ST, SD=SD,
                   PL=PL, RD=RD, PRJ=PRJ, GR=GR, RR=RR, BA=BA,
                   prj_last=prj_last))

# Conditional formatting on input tabs
# Project status colouring
def cf_text(ws, rng_str, mapping):
    for word, (bg, tx) in mapping.items():
        ws.conditional_formatting.add(rng_str, CellIsRule(
            operator="equal", formula=[f'"{word}"'], fill=S.fill(bg),
            font=S.Font(bold=True, color=tx)))

proj = wb[PRJ]
cf_text(proj, f"F{DATA_START}:F{DATA_END}", {
    "On Track": (S.GREEN_BG, S.GREEN_TX), "At Risk": (S.YELLOW_BG, S.YELLOW_TX),
    "Behind": (S.RED_BG, S.RED_TX), "Complete": ("D9E1F2", "1F3864")})
cf_text(proj, f"M{DATA_START}:O{DATA_END}", {
    "Complete": (S.GREEN_BG, S.GREEN_TX), "In Progress": (S.YELLOW_BG, S.YELLOW_TX),
    "Not Started": (S.RED_BG, S.RED_TX)})
# % complete data bar
proj.conditional_formatting.add(f"E{DATA_START}:E{DATA_END}",
    ColorScaleRule(start_type="num", start_value=0, start_color="F8CBCB",
                   mid_type="num", mid_value=0.5, mid_color="FFF2CC",
                   end_type="num", end_value=1, end_color="C6EFCE"))
risk = wb[RR]
apply_ryg_word(risk, f"G{DATA_START}:G{DATA_END}")
risk.conditional_formatting.add(f"F{DATA_START}:F{DATA_END}",
    ColorScaleRule(start_type="num", start_value=1, start_color="C6EFCE",
                   mid_type="num", mid_value=10, mid_color="FFF2CC",
                   end_type="num", end_value=25, end_color="F8CBCB"))
grant = wb[GR]
cf_text(grant, f"G{DATA_START}:G{DATA_END}", {
    "Paid": (S.GREEN_BG, S.GREEN_TX), "Partially Paid": (S.GREEN_BG, S.GREEN_TX),
    "Approved": ("D9E1F2", "1F3864"), "Under Review": (S.YELLOW_BG, S.YELLOW_TX),
    "Submitted": (S.YELLOW_BG, S.YELLOW_TX), "Not Submitted": (S.RED_BG, S.RED_TX),
    "Denied": (S.RED_BG, S.RED_TX)})
ba = wb[BA]
cf_text(ba, f"H{DATA_START}:H{DATA_END}", {
    "Complete": (S.GREEN_BG, S.GREEN_TX), "In Progress": (S.YELLOW_BG, S.YELLOW_TX),
    "Blocked": (S.RED_BG, S.RED_TX), "Not Started": ("D9E1F2", "1F3864")})
cf_text(ba, f"G{DATA_START}:G{DATA_END}", {
    "Critical": (S.RED_BG, S.RED_TX), "High": (S.YELLOW_BG, S.YELLOW_TX)})

# ---- Sheet order & active ----
order = ["Exec_Dashboard", "Sales_Dashboard", "Ops_Dashboard", "Financial_Dashboard",
         "Board_Report", CD, SD, PL, OD, PRJ, FD, RD, GR, ST, RR, BA,
         "Data_Dictionary", "User_Guide", "Assumptions", "Calc", "Lists"]
wb._sheets.sort(key=lambda s: order.index(s.title) if s.title in order else 99)
wb.active = wb.sheetnames.index("Exec_Dashboard")

wb.save(wb_path)
print("Saved:", os.path.abspath(wb_path))
