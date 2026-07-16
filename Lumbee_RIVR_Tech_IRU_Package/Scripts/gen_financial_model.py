"""
gen_financial_model.py — Deliverable 10: 30-Year Editable Financial Model (Excel)
Lumbee Tribe of North Carolina  /  LREMC Technologies, LLC d/b/a RIVR Tech
Broadband IRU partnership — TBCP grant-funded hybrid network, southeastern NC.

ALL economics are PLACEHOLDERS for negotiation. Every computed value is an
openpyxl formula referencing amber INPUT cells — nothing is hard-coded inside a
formula. Three switches drive the model:
    * Scenario switch  (1=Low / 2=Base / 3=High)  -> CHOOSE-based Active drivers
    * IRU term switch  (20 / 25 / 30 years)       -> NPV/IRR horizon; rev beyond=0
    * Rev-share option (1=A .. 5=E)               -> Tribal payment structure

Run:  python3 Scripts/gen_financial_model.py
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

# ---------------------------------------------------------------------------
# Layout constants for the year-based sheets (years are ROWS)
# ---------------------------------------------------------------------------
HDR = 5                       # header row on every yearly sheet
Y0 = 6                        # Year 0 data row
YEARS = list(range(0, 31))    # Year 0 (construction) .. Year 30 (operations)
LASTROW = Y0 + 30             # 36
def yr_row(y): return Y0 + y

def col(n): return get_column_letter(n)
def a(sheet, r, c):           # absolute cross-sheet cell address
    return f"{sheet}!${col(c)}${r}"
def rng(sheet, c, r1, r2):    # absolute cross-sheet column range
    return f"{sheet}!${col(c)}${r1}:${col(c)}${r2}"

GREEN = C.XL_CHECK_OK
RED = C.XL_CHECK_BAD
CHECK_CELLS = []              # (sheet, cell_addr_no_sheet) for dashboard roll-up

def pass_fail_cf(ws, cell):
    """Green when the cell contains PASS, red otherwise."""
    anchor = cell.replace("$", "")
    ws.conditional_formatting.add(cell, FormulaRule(
        formula=['ISNUMBER(SEARCH("PASS",%s))' % anchor], stopIfTrue=True,
        fill=PatternFill("solid", fgColor=GREEN)))
    ws.conditional_formatting.add(cell, FormulaRule(
        formula=['NOT(ISNUMBER(SEARCH("PASS",%s)))' % anchor],
        fill=PatternFill("solid", fgColor=RED)))

def check(ws, row, cndlabel, formula, sheet_name):
    """Write an italic label + PASS/FAIL formula cell; register for roll-up."""
    ws.cell(row=row, column=2, value=cndlabel).font = Font(size=9, italic=True)
    cc = ws.cell(row=row, column=6, value=formula)
    cc.font = Font(bold=True, size=9)
    cc.border = C.BORDER
    cell = f"{col(6)}{row}"
    pass_fail_cf(ws, cell)
    CHECK_CELLS.append((sheet_name, cell))
    return cc

def yearly_header(ws, headers, title, subtitle=None):
    C.xl_title(ws, title, subtitle, span=len(headers))
    C.xl_header_row(ws, HDR, headers)
    for y in YEARS:                      # Year label column
        C.xl_cell(ws, yr_row(y), 1, y, "text", fmt=C.FMT_NUM)

# ===========================================================================
wb = Workbook()

# ---------------------------------------------------------------------------
# Reference registry: key -> cell address on Assumptions
# ---------------------------------------------------------------------------
REF = {}     # single input OR active(F) address
CASE = {}    # case-varying: (lowAddr, baseAddr, highAddr)

# ===========================================================================
# SHEET: Assumptions  (must be built first — everything references it)
# ===========================================================================
As = wb.create_sheet("Assumptions")
C.xl_title(As, "ASSUMPTIONS — All Editable Input Drivers",
           "Amber cells are INPUTS you may edit. Blue cells are FORMULAS (do not edit).")
As.column_dimensions["A"].width = 3
As.column_dimensions["B"].width = 46
for cc in "CDEF":
    As.column_dimensions[cc].width = 15
As.column_dimensions["G"].width = 40
C.xl_legend(As, 4)

# --- Switches --------------------------------------------------------------
r = 6
C.xl_cell(As, r, 2, "MODEL SWITCHES", "section");
for cX in range(3,8): C.xl_cell(As, r, cX, None, "section")
r += 1
SCEN_ROW = r
C.xl_cell(As, r, 2, "Scenario switch  (1 = Low, 2 = Base, 3 = High)", "text")
C.xl_cell(As, r, 3, 2, "input", fmt=C.FMT_NUM)
C.xl_cell(As, r, 4, "=CHOOSE($C$%d,\"LOW\",\"BASE\",\"HIGH\")" % r, "formula")
C.xl_cell(As, r, 7, "Drives every scenario-dependent driver via CHOOSE.", "text")
SCEN = "$C$%d" % r
r += 1
TERM_ROW = r
C.xl_cell(As, r, 2, "IRU term switch  (20 / 25 / 30 years — recommend 30)", "text")
C.xl_cell(As, r, 3, C.DEAL["iru_term_recommended"], "input", fmt=C.FMT_NUM)
C.xl_cell(As, r, 7, "Analysis horizon for NPV/IRR. Revenue & payments beyond term = 0.", "text")
TERM = "$C$%d" % r
r += 1
OPT_ROW = r
C.xl_cell(As, r, 2, "Revenue-share option switch  (1=A 2=B 3=C 4=D 5=E)", "text")
C.xl_cell(As, r, 3, 4, "input", fmt=C.FMT_NUM)   # 4 -> Option D (recommended)
C.xl_cell(As, r, 4, "=CHOOSE($C$%d,\"A\",\"B\",\"C\",\"D\",\"E\")" % r, "formula")
C.xl_cell(As, r, 7, "Recommended: D (Hybrid). All five computed side-by-side.", "text")
OPT = "$C$%d" % r
r += 1
OPTNAME_ROW = r
C.xl_cell(As, r, 2, "Active option name", "text")
C.xl_cell(As, r, 3,
          '=CHOOSE($C$%d,"A — Fixed Annual","B — %% Gross Revenue","C — %% Operating Cash Flow","D — Hybrid (Base + Share)","E — Holiday then Stepped")' % OPT_ROW,
          "formula")
As.merge_cells(start_row=r, start_column=3, end_row=r, end_column=7)
REF["opt_name"] = "$C$%d" % r

# data validations for the switches
dv_s = DataValidation(type="whole", operator="between", formula1="1", formula2="3", allow_blank=False)
dv_t = DataValidation(type="list", formula1='"20,25,30"', allow_blank=False)
dv_o = DataValidation(type="whole", operator="between", formula1="1", formula2="5", allow_blank=False)
As.add_data_validation(dv_s); dv_s.add(As["C%d" % SCEN_ROW])
As.add_data_validation(dv_t); dv_t.add(As["C%d" % TERM_ROW])
As.add_data_validation(dv_o); dv_o.add(As["C%d" % OPT_ROW])

REF["scenario"] = SCEN; REF["term"] = TERM; REF["option"] = OPT

# --- Case-varying drivers (Low / Base / High / Active) ---------------------
r += 2
C.xl_cell(As, r, 2, "SCENARIO-DEPENDENT DRIVERS", "section")
for cX in range(3,8): C.xl_cell(As, r, cX, None, "section")
r += 1
C.xl_header_row(As, r, ["Driver", "Low", "Base", "High", "Active", "Units / Notes"],
                start_col=2, freeze=False, filt=False)
r += 1

def case_param(key, name, low, base, high, units, fmt):
    global r
    C.xl_cell(As, r, 2, name, "text")
    C.xl_cell(As, r, 3, low, "input", fmt=fmt)
    C.xl_cell(As, r, 4, base, "input", fmt=fmt)
    C.xl_cell(As, r, 5, high, "input", fmt=fmt)
    C.xl_cell(As, r, 6, "=CHOOSE(%s,$C$%d,$D$%d,$E$%d)" % (SCEN, r, r, r), "formula", fmt=fmt)
    C.xl_cell(As, r, 7, units, "text")
    CASE[key] = ("$C$%d" % r, "$D$%d" % r, "$E$%d" % r)
    REF[key] = "$F$%d" % r
    r += 1

case_param("term_take", "Terminal take rate (net penetration)", 0.35, 0.45, 0.55, "% of homes passed", C.FMT_PCT)
case_param("take_ramp", "Take-rate ramp (years to terminal)", 6, 5, 4, "years", C.FMT_NUM)
case_param("res_arpu", "Residential ARPU (monthly)", 65, 75, 85, "$/sub/month", C.FMT_USD)
case_param("bus_arpu", "Business ARPU (monthly)", 200, 250, 300, "$/sub/month", C.FMT_USD)
case_param("ent_arpu", "Enterprise ARPU (monthly)", 800, 1000, 1200, "$/sub/month", C.FMT_USD)
case_param("voice_arpu", "Voice ARPU (monthly)", 30, 35, 40, "$/sub/month", C.FMT_USD)
case_param("ent_max", "Enterprise subscribers at maturity", 15, 25, 40, "count", C.FMT_NUM)
case_param("wholesale", "Wholesale revenue at maturity (annual)", 300000, 500000, 750000, "$/year", C.FMT_USD)
case_param("churn", "Annual customer churn", 0.18, 0.14, 0.10, "% per year", C.FMT_PCT)
case_param("baddebt", "Bad debt", 0.025, 0.015, 0.010, "% of recurring rev", C.FMT_PCT)
case_param("infl", "Operating-cost inflation", 0.035, 0.030, 0.025, "% per year", C.FMT_PCT)
case_param("cfactor", "Construction cost factor", 1.15, 1.00, 0.90, "x on budget (High=cheaper)", C.FMT_MULT)

# --- Single (non-case) inputs ---------------------------------------------
r += 1
C.xl_cell(As, r, 2, "SINGLE INPUTS (not case-varying)", "section")
for cX in range(3,8): C.xl_cell(As, r, cX, None, "section")
r += 1
C.xl_header_row(As, r, ["Input", "Value", "", "", "", "Units / Notes"],
                start_col=2, freeze=False, filt=False)
r += 1

def single(key, name, val, units, fmt):
    global r
    C.xl_cell(As, r, 2, name, "text")
    C.xl_cell(As, r, 3, val, "input", fmt=fmt)
    C.xl_cell(As, r, 7, units, "text")
    REF[key] = "$C$%d" % r
    r += 1

single("grant", "TBCP grant amount (funds Tribal Assets)", 25000000, "$ (placeholder $25M)", C.FMT_USD)
single("homes", "Homes passed (total)", 8500, "premises (placeholder 8,500)", C.FMT_NUM)
single("buildout", "Build-out period", 3, "years to complete homes passed", C.FMT_NUM)
single("biz_pen", "Business penetration", 0.04, "% of homes passed", C.FMT_PCT)
single("voice_attach", "Voice attach rate", 0.40, "% of residential subs", C.FMT_PCT)
single("install_fee", "Installation fee (one-time)", 100, "$/new connect", C.FMT_USD)
single("arpu_esc", "ARPU / price escalation", 0.02, "% per year (set 0 to disable)", C.FMT_PCT)
single("netops", "Network operations cost", 120, "$/subscriber/year", C.FMT_USD)
single("maint_pct", "Network maintenance", 0.03, "% of construction cost/yr", C.FMT_PCT)
single("heads", "Staffing headcount", 12, "FTEs", C.FMT_NUM)
single("fte_cost", "Loaded cost per FTE", 85000, "$/FTE/year", C.FMT_USD)
single("mkt_pct", "Marketing", 0.06, "% of gross revenue", C.FMT_PCT)
single("ga_pct", "G&A / overhead", 0.08, "% of gross revenue", C.FMT_PCT)
single("elec_cycle", "Electronics replacement cycle", 7, "years", C.FMT_NUM)
single("reserve_pct", "Capital-replacement reserve", 0.04, "% of gross revenue", C.FMT_PCT)
single("disc", "Discount rate (NPV)", 0.09, "% WACC/hurdle", C.FMT_PCT)
single("rivr_upfront", "RIVR Tech upfront investment", 2000000, "$ (electronics/integration/WC)", C.FMT_USD)
single("res_cap_val", "Reserved-capacity value to Tribe", 150000, "$/yr in-kind (memo)", C.FMT_USD)
# Revenue-share option inputs
r += 1
C.xl_cell(As, r, 2, "REVENUE-SHARE OPTION INPUTS", "section")
for cX in range(3,8): C.xl_cell(As, r, cX, None, "section")
r += 1
single("optA_fixed", "Option A — fixed annual payment", 500000, "$/yr (escalated)", C.FMT_USD)
single("optA_esc", "Option A — annual escalator", 0.02, "% per year", C.FMT_PCT)
single("optB_pct", "Option B — share of gross revenue", 0.05, "% (placeholder 5%)", C.FMT_PCT)
single("optC_pct", "Option C — share of operating cash flow", 0.20, "% (placeholder 20%)", C.FMT_PCT)
single("optD_base", "Option D — hybrid fixed base", 250000, "$/yr", C.FMT_USD)
single("optD_pct", "Option D — hybrid revenue share", 0.025, "% of gross revenue", C.FMT_PCT)
single("optE_holiday", "Option E — payment-holiday period", 2, "years at $0", C.FMT_NUM)
single("optE_first", "Option E — first payment after holiday", 300000, "$/yr", C.FMT_USD)
single("optE_step", "Option E — annual step-up", 0.05, "% per year", C.FMT_PCT)

ASSUM_LASTROW = r

# ===========================================================================
# SHEET: Construction_Budget
# ===========================================================================
Cb = wb.create_sheet("Construction_Budget")
yearly_header  # noqa (not a yearly sheet)
C.xl_title(Cb, "CONSTRUCTION BUDGET — Capital Line Items (Year 0)",
           "Qty x Unit Cost = Extended. Construction cost factor (scenario) applied to the total.")
for w, cc in [(42,"B"),(14,"C"),(16,"D"),(18,"E"),(40,"F")]:
    Cb.column_dimensions[cc].width = w
C.xl_header_row(Cb, HDR, ["Capital Line Item", "Quantity", "Unit Cost", "Extended", "Notes"], start_col=2)
lines = [
    ("Outside-plant (OSP) fiber", 250, 45000, "route miles x $/mi"),
    ("Conduit / directional bore", 80, 30000, "miles x $/mi"),
    ("Electronics (OLT / aggregation / core)", 1, 4000000, "lump — basis for replacement cycle"),
    ("Fiber huts / cabinets / power", 25, 60000, "sites x $/site"),
    ("Service drops", 3825, 650, "connects x $/drop"),
    ("Engineering & design", 1, 1500000, "lump"),
    ("Permitting, make-ready & pole attach", 1, 1200000, "lump"),
]
rr = HDR + 1
elec_ext_row = None
first_line_row = rr
for name, qty, unit, note in lines:
    C.xl_cell(Cb, rr, 2, name, "text")
    C.xl_cell(Cb, rr, 3, qty, "input", fmt=C.FMT_NUM)
    C.xl_cell(Cb, rr, 4, unit, "input", fmt=C.FMT_USD)
    C.xl_cell(Cb, rr, 5, "=$C%d*$D%d" % (rr, rr), "formula", fmt=C.FMT_USD)
    C.xl_cell(Cb, rr, 6, note, "text")
    if name.startswith("Electronics"):
        elec_ext_row = rr
    rr += 1
last_line_row = rr - 1
# Subtotal
C.xl_cell(Cb, rr, 2, "Subtotal (direct construction)", "text", bold=True)
C.xl_cell(Cb, rr, 5, "=SUM($E%d:$E%d)" % (first_line_row, last_line_row), "formula", fmt=C.FMT_USD, bold=True)
subtotal_row = rr; rr += 1
# Contingency
C.xl_cell(Cb, rr, 2, "Contingency", "text")
C.xl_cell(Cb, rr, 3, 0.10, "input", fmt=C.FMT_PCT)
C.xl_cell(Cb, rr, 5, "=$C%d*$E%d" % (rr, subtotal_row), "formula", fmt=C.FMT_USD)
cont_row = rr; rr += 1
# Subtotal + contingency
C.xl_cell(Cb, rr, 2, "Subtotal + contingency", "text", bold=True)
C.xl_cell(Cb, rr, 5, "=$E%d+$E%d" % (subtotal_row, cont_row), "formula", fmt=C.FMT_USD, bold=True)
subcont_row = rr; rr += 1
# Construction cost factor (active)
C.xl_cell(Cb, rr, 2, "Construction cost factor (active scenario)", "text")
C.xl_cell(Cb, rr, 5, "=%s" % a("Assumptions", int(REF["cfactor"][3:]), 6), "formula", fmt=C.FMT_MULT)
factor_row = rr; rr += 1
# Total construction
C.xl_cell(Cb, rr, 2, "TOTAL CONSTRUCTION COST", "output", bold=True)
C.xl_cell(Cb, rr, 5, "=$E%d*$E%d" % (subcont_row, factor_row), "output", fmt=C.FMT_USD, bold=True)
total_row = rr; rr += 1

# expose addresses
CB_TOTAL = a("Construction_Budget", total_row, 5)
CB_SUBCONT = a("Construction_Budget", subcont_row, 5)
CB_ELEC = a("Construction_Budget", elec_ext_row, 5)
CB_FACTOR = a("Construction_Budget", factor_row, 5)
# electronics replacement basis (factored)
rr += 1
C.xl_cell(Cb, rr, 2, "Electronics replacement basis (factored)", "text")
C.xl_cell(Cb, rr, 5, "=%s*%s" % (CB_ELEC, CB_FACTOR), "formula", fmt=C.FMT_USD)
CB_ELEC_FACT = a("Construction_Budget", rr, 5)
rr += 2
check(Cb, rr, "CHECK: no #REF / all line items numeric",
      '=IF(ISNUMBER($E%d),"PASS","FAIL")' % total_row, "Construction_Budget")

# ===========================================================================
# SHEET: Grant_Funding  (sources & uses)
# ===========================================================================
Gf = wb.create_sheet("Grant_Funding")
C.xl_title(Gf, "GRANT FUNDING — Sources & Uses",
           "TBCP funds the Tribal Assets. TBCP does not require non-federal match. Sources must equal Uses.")
for w, cc in [(46,"B"),(18,"C"),(40,"D")]:
    Gf.column_dimensions[cc].width = w
C.xl_header_row(Gf, HDR, ["Sources & Uses", "Amount", "Notes"], start_col=2)
gr = HDR + 1
C.xl_cell(Gf, gr, 2, "SOURCES", "section"); C.xl_cell(Gf, gr, 3, None, "section"); C.xl_cell(Gf, gr, 4, None, "section"); gr += 1
C.xl_cell(Gf, gr, 2, "TBCP federal grant", "text")
C.xl_cell(Gf, gr, 3, "=%s" % REF["grant"].replace("$C$", "Assumptions!$C$"), "formula", fmt=C.FMT_USD)
C.xl_cell(Gf, gr, 4, "Placeholder $25,000,000 — funds Tribal Assets", "text")
grant_row = gr; gr += 1
C.xl_cell(Gf, gr, 2, "Non-federal match (not required by TBCP)", "text")
C.xl_cell(Gf, gr, 3, 0, "input", fmt=C.FMT_USD)
C.xl_cell(Gf, gr, 4, "Editable — TBCP Round 3 requires no match", "text")
match_row = gr; gr += 1
C.xl_cell(Gf, gr, 2, "TOTAL SOURCES", "output", bold=True)
C.xl_cell(Gf, gr, 3, "=SUM($C%d:$C%d)" % (grant_row, match_row), "output", fmt=C.FMT_USD, bold=True)
sources_row = gr; gr += 2
C.xl_cell(Gf, gr, 2, "USES", "section"); C.xl_cell(Gf, gr, 3, None, "section"); C.xl_cell(Gf, gr, 4, None, "section"); gr += 1
C.xl_cell(Gf, gr, 2, "Total construction cost", "text")
C.xl_cell(Gf, gr, 3, "=%s" % CB_TOTAL, "formula", fmt=C.FMT_USD)
C.xl_cell(Gf, gr, 4, "From Construction_Budget", "text")
uses_constr_row = gr; gr += 1
C.xl_cell(Gf, gr, 2, "Surplus / (funding gap) plug", "text")
C.xl_cell(Gf, gr, 3, "=$C%d-$C%d" % (sources_row, uses_constr_row), "formula", fmt=C.FMT_USD)
C.xl_cell(Gf, gr, 4, "Positive = surplus for contingency; negative = gap (flag)", "text")
plug_row = gr; gr += 1
C.xl_cell(Gf, gr, 2, "TOTAL USES", "output", bold=True)
C.xl_cell(Gf, gr, 3, "=SUM($C%d:$C%d)" % (uses_constr_row, plug_row), "output", fmt=C.FMT_USD, bold=True)
uses_row = gr; gr += 2
check(Gf, gr, "CHECK: Sources = Uses (reconciles)",
      '=IF(ABS($C%d-$C%d)<1,"PASS","FAIL")' % (sources_row, uses_row), "Grant_Funding"); gr += 1
check(Gf, gr, "CHECK: Uses do not exceed grant sources (no funding gap)",
      '=IF($C%d>=$C%d,"PASS","FAIL — FUNDING GAP")' % (sources_row, uses_constr_row), "Grant_Funding")

# ===========================================================================
# SHEET: Homes_Passed
# ===========================================================================
Hp = wb.create_sheet("Homes_Passed")
yearly_header(Hp, ["Year", "Homes Passed (cum.)", "New Homes Passed", "% Complete"],
              "HOMES PASSED — Build-out Schedule",
              "Year 0 = construction. Serviceable homes ramp over the build-out period.")
for w, cc in [(20,"B"),(20,"C"),(16,"D")]:
    Hp.column_dimensions[cc].width = w
homes_a = REF["homes"].replace("$C$", "Assumptions!$C$")
build_a = REF["buildout"].replace("$C$", "Assumptions!$C$")
for y in YEARS:
    rr = yr_row(y)
    if y == 0:
        C.xl_cell(Hp, rr, 2, 0, "formula", fmt=C.FMT_NUM)
    else:
        C.xl_cell(Hp, rr, 2, "=%s*MIN(1,$A%d/%s)" % (homes_a, rr, build_a), "formula", fmt=C.FMT_NUM)
    prev = "0" if y == 0 else "$B%d" % (rr - 1)
    C.xl_cell(Hp, rr, 3, "=$B%d-%s" % (rr, prev), "formula", fmt=C.FMT_NUM)
    C.xl_cell(Hp, rr, 4, "=$B%d/%s" % (rr, homes_a), "formula", fmt=C.FMT_PCT)
HP_HOMES = lambda y: a("Homes_Passed", yr_row(y), 2)
crow = LASTROW + 2
check(Hp, crow, "CHECK: homes passed never exceed total (Assumptions)",
      '=IF(MAX($B%d:$B%d)<=%s+0.5,"PASS","FAIL")' % (Y0, LASTROW, homes_a), "Homes_Passed")

# ===========================================================================
# SHEET: Take_Rate_Customers
# ===========================================================================
Tr = wb.create_sheet("Take_Rate_Customers")
yearly_header(Tr, ["Year", "Take Rate", "Residential Subs", "Business Subs",
                   "Enterprise Subs", "Voice Subs", "Total Premise Subs", "Gross Adds"],
              "TAKE RATE & CUSTOMERS",
              "Net penetration ramps to terminal. Gross adds (incl. churn replacement) drive install revenue.")
for cc in "BCDEFGH":
    Tr.column_dimensions[cc].width = 16
tt = lambda k: REF[k].replace("$C$", "Assumptions!$C$").replace("$F$", "Assumptions!$F$")
term_take = REF["term_take"].replace("$F$", "Assumptions!$F$")
take_ramp = REF["take_ramp"].replace("$F$", "Assumptions!$F$")
biz_pen = REF["biz_pen"].replace("$C$", "Assumptions!$C$")
ent_max = REF["ent_max"].replace("$F$", "Assumptions!$F$")
voice_att = REF["voice_attach"].replace("$C$", "Assumptions!$C$")
churn_a = REF["churn"].replace("$F$", "Assumptions!$F$")
for y in YEARS:
    rr = yr_row(y)
    homes = HP_HOMES(y)
    if y == 0:
        for cX in range(2, 9):
            C.xl_cell(Tr, rr, cX, 0, "formula", fmt=(C.FMT_PCT if cX == 2 else C.FMT_NUM))
        continue
    C.xl_cell(Tr, rr, 2, "=%s*MIN(1,$A%d/%s)" % (term_take, rr, take_ramp), "formula", fmt=C.FMT_PCT)
    C.xl_cell(Tr, rr, 3, "=%s*$B%d" % (homes, rr), "formula", fmt=C.FMT_NUM)          # residential
    C.xl_cell(Tr, rr, 4, "=%s*%s" % (homes, biz_pen), "formula", fmt=C.FMT_NUM)        # business
    C.xl_cell(Tr, rr, 5, "=%s*MIN(1,$A%d/%s)" % (ent_max, rr, take_ramp), "formula", fmt=C.FMT_NUM)  # enterprise
    C.xl_cell(Tr, rr, 6, "=$C%d*%s" % (rr, voice_att), "formula", fmt=C.FMT_NUM)        # voice
    C.xl_cell(Tr, rr, 7, "=$C%d+$D%d+$E%d" % (rr, rr, rr), "formula", fmt=C.FMT_NUM)    # total premise
    prev_tot = "0" if y == 1 else "$G%d" % (rr - 1)
    C.xl_cell(Tr, rr, 8, "=MAX(0,$G%d-%s)+%s*%s" % (rr, prev_tot, prev_tot, churn_a),
              "formula", fmt=C.FMT_NUM)     # gross adds = net adds + churn replacement
TR_RES = lambda y: a("Take_Rate_Customers", yr_row(y), 3)
TR_BUS = lambda y: a("Take_Rate_Customers", yr_row(y), 4)
TR_ENT = lambda y: a("Take_Rate_Customers", yr_row(y), 5)
TR_VOICE = lambda y: a("Take_Rate_Customers", yr_row(y), 6)
TR_TOT = lambda y: a("Take_Rate_Customers", yr_row(y), 7)
TR_ADDS = lambda y: a("Take_Rate_Customers", yr_row(y), 8)
crow = LASTROW + 2
check(Tr, crow, "CHECK: residential subs never exceed homes passed",
      '=IF(SUMPRODUCT(--($C%d:$C%d>%s!$B%d:$B%d))=0,"PASS","FAIL")'
      % (Y0, LASTROW, "Homes_Passed", Y0, LASTROW), "Take_Rate_Customers")

# ===========================================================================
# SHEET: Revenue
# ===========================================================================
Rv = wb.create_sheet("Revenue")
yearly_header(Rv, ["Year", "Residential", "Business", "Enterprise", "Voice",
                   "Wholesale", "Installation", "Recurring Subtotal", "TOTAL GROSS REVENUE"],
              "REVENUE — ARPU x Customers",
              "Monthly ARPU x 12. Revenue beyond the selected IRU term is zero (term gate).")
for cc in "BCDEFGHI":
    Rv.column_dimensions[cc].width = 15
res_arpu = REF["res_arpu"].replace("$F$", "Assumptions!$F$")
bus_arpu = REF["bus_arpu"].replace("$F$", "Assumptions!$F$")
ent_arpu = REF["ent_arpu"].replace("$F$", "Assumptions!$F$")
voice_arpu = REF["voice_arpu"].replace("$F$", "Assumptions!$F$")
whole_a = REF["wholesale"].replace("$F$", "Assumptions!$F$")
install_a = REF["install_fee"].replace("$C$", "Assumptions!$C$")
arpu_esc_a = REF["arpu_esc"].replace("$C$", "Assumptions!$C$")
term_a = REF["term"].replace("$C$", "Assumptions!$C$")
build_a2 = build_a
for y in YEARS:
    rr = yr_row(y)
    gate = "IF($A%d>%s,0,1)" % (rr, term_a)     # term gate (0 beyond term or year 0)
    esc = "(1+%s)^($A%d-1)" % (arpu_esc_a, rr)  # ARPU price escalation
    if y == 0:
        for cX in range(2, 10):
            C.xl_cell(Rv, rr, cX, 0, "formula", fmt=C.FMT_USD)
        continue
    C.xl_cell(Rv, rr, 2, "=%s*%s*%s*12*%s" % (TR_RES(y), res_arpu, esc, gate), "formula", fmt=C.FMT_USD)
    C.xl_cell(Rv, rr, 3, "=%s*%s*%s*12*%s" % (TR_BUS(y), bus_arpu, esc, gate), "formula", fmt=C.FMT_USD)
    C.xl_cell(Rv, rr, 4, "=%s*%s*%s*12*%s" % (TR_ENT(y), ent_arpu, esc, gate), "formula", fmt=C.FMT_USD)
    C.xl_cell(Rv, rr, 5, "=%s*%s*%s*12*%s" % (TR_VOICE(y), voice_arpu, esc, gate), "formula", fmt=C.FMT_USD)
    C.xl_cell(Rv, rr, 6, "=%s*MIN(1,$A%d/%s)*%s" % (whole_a, rr, build_a2, gate), "formula", fmt=C.FMT_USD)
    C.xl_cell(Rv, rr, 7, "=%s*%s*%s" % (TR_ADDS(y), install_a, gate), "formula", fmt=C.FMT_USD)
    C.xl_cell(Rv, rr, 8, "=SUM($B%d:$F%d)" % (rr, rr), "formula", fmt=C.FMT_USD)
    C.xl_cell(Rv, rr, 9, "=$H%d+$G%d" % (rr, rr), "output", fmt=C.FMT_USD, bold=True)
RV_TOT = lambda y: a("Revenue", yr_row(y), 9)
RV_REC = lambda y: a("Revenue", yr_row(y), 8)
crow = LASTROW + 2
check(Rv, crow, "CHECK: no #REF errors in total gross revenue column",
      '=IF(SUMPRODUCT(--ISERROR($I%d:$I%d))=0,"PASS","FAIL")' % (Y0, LASTROW), "Revenue")

# ===========================================================================
# SHEET: Operating_Expenses
# ===========================================================================
Oe = wb.create_sheet("Operating_Expenses")
yearly_header(Oe, ["Year", "Infl. Factor", "Network Ops", "Maintenance", "Staffing",
                   "Marketing", "G&A", "Bad Debt", "TOTAL OPEX", "Electronics (memo)"],
              "OPERATING EXPENSES",
              "Fixed components inflate; %-of-revenue components scale with revenue. Electronics replacement is a MEMO here — the capital charge lives in Capital_Replacement to avoid double counting.")
for cc in "BCDEFGHIJ":
    Oe.column_dimensions[cc].width = 14
infl_a = REF["infl"].replace("$F$", "Assumptions!$F$")
netops_a = REF["netops"].replace("$C$", "Assumptions!$C$")
maint_a = REF["maint_pct"].replace("$C$", "Assumptions!$C$")
heads_a = REF["heads"].replace("$C$", "Assumptions!$C$")
fte_a = REF["fte_cost"].replace("$C$", "Assumptions!$C$")
mkt_a = REF["mkt_pct"].replace("$C$", "Assumptions!$C$")
ga_a = REF["ga_pct"].replace("$C$", "Assumptions!$C$")
bd_a = REF["baddebt"].replace("$F$", "Assumptions!$F$")
cycle_a = REF["elec_cycle"].replace("$C$", "Assumptions!$C$")
for y in YEARS:
    rr = yr_row(y)
    if y == 0:
        for cX in range(2, 11):
            C.xl_cell(Oe, rr, cX, 0 if cX != 2 else 1, "formula", fmt=(C.FMT_MULT if cX == 2 else C.FMT_USD))
        continue
    C.xl_cell(Oe, rr, 2, "=(1+%s)^($A%d-1)" % (infl_a, rr), "formula", fmt=C.FMT_MULT)      # inflation factor
    C.xl_cell(Oe, rr, 3, "=%s*%s*$B%d" % (TR_TOT(y), netops_a, rr), "formula", fmt=C.FMT_USD)  # network ops
    C.xl_cell(Oe, rr, 4, "=%s*%s*$B%d" % (maint_a, CB_TOTAL, rr), "formula", fmt=C.FMT_USD)      # maintenance
    C.xl_cell(Oe, rr, 5, "=%s*%s*$B%d" % (heads_a, fte_a, rr), "formula", fmt=C.FMT_USD)         # staffing
    C.xl_cell(Oe, rr, 6, "=%s*%s" % (mkt_a, RV_TOT(y)), "formula", fmt=C.FMT_USD)                # marketing
    C.xl_cell(Oe, rr, 7, "=%s*%s" % (ga_a, RV_TOT(y)), "formula", fmt=C.FMT_USD)                 # G&A
    C.xl_cell(Oe, rr, 8, "=%s*%s" % (bd_a, RV_REC(y)), "formula", fmt=C.FMT_USD)                 # bad debt
    C.xl_cell(Oe, rr, 9, "=SUM($C%d:$H%d)" % (rr, rr), "output", fmt=C.FMT_USD, bold=True)       # total opex
    C.xl_cell(Oe, rr, 10, "=%s/%s*$B%d" % (CB_ELEC_FACT, cycle_a, rr), "formula", fmt=C.FMT_USD)  # electronics memo
OE_TOT = lambda y: a("Operating_Expenses", yr_row(y), 9)
crow = LASTROW + 2
check(Oe, crow, "CHECK: total opex is non-negative and error-free",
      '=IF(AND(MIN($I%d:$I%d)>=0,SUMPRODUCT(--ISERROR($I%d:$I%d))=0),"PASS","FAIL")'
      % (Y0, LASTROW, Y0, LASTROW), "Operating_Expenses")

# ===========================================================================
# SHEET: Capital_Replacement
# ===========================================================================
Cr = wb.create_sheet("Capital_Replacement")
yearly_header(Cr, ["Year", "Annualized Elec. Charge", "Lumpy Refresh (memo)",
                   "Reserve Funding", "Cum. Reserve", "Cum. Refresh Spend"],
              "CAPITAL REPLACEMENT — Electronics Refresh & Reserve",
              "Annualized charge flows to cash flow. Lumpy refresh + reserve funding test reserve adequacy.")
for cc in "BCDEF":
    Cr.column_dimensions[cc].width = 20
reserve_a = REF["reserve_pct"].replace("$C$", "Assumptions!$C$")
for y in YEARS:
    rr = yr_row(y)
    if y == 0:
        for cX in range(2, 7):
            C.xl_cell(Cr, rr, cX, 0, "formula", fmt=C.FMT_USD)
        continue
    infl_fac = "(1+%s)^($A%d-1)" % (infl_a, rr)
    C.xl_cell(Cr, rr, 2, "=%s/%s*%s" % (CB_ELEC_FACT, cycle_a, infl_fac), "formula", fmt=C.FMT_USD)   # annualized
    C.xl_cell(Cr, rr, 3, "=IF(AND($A%d>0,MOD($A%d,%s)=0),%s*(1+%s)^$A%d,0)"
              % (rr, rr, cycle_a, CB_ELEC_FACT, infl_a, rr), "formula", fmt=C.FMT_USD)                # lumpy
    C.xl_cell(Cr, rr, 4, "=%s*%s" % (reserve_a, RV_TOT(y)), "formula", fmt=C.FMT_USD)                 # reserve funding
    prevres = "0" if y == 1 else "$E%d" % (rr - 1)
    prevsp = "0" if y == 1 else "$F%d" % (rr - 1)
    C.xl_cell(Cr, rr, 5, "=%s+$D%d" % (prevres, rr), "formula", fmt=C.FMT_USD)
    C.xl_cell(Cr, rr, 6, "=%s+$C%d" % (prevsp, rr), "formula", fmt=C.FMT_USD)
CR_ANN = lambda y: a("Capital_Replacement", yr_row(y), 2)
crow = LASTROW + 2
check(Cr, crow, "CHECK: reserve funding covers cumulative refresh spend at horizon",
      '=IF($E%d>=$F%d,"PASS","FAIL — under-reserved")' % (LASTROW, LASTROW), "Capital_Replacement")

# ===========================================================================
# SHEET: Revenue_Share_Options  (A..E side by side + selected)
# ===========================================================================
Rs = wb.create_sheet("Revenue_Share_Options")
yearly_header(Rs, ["Year", "Gross Revenue", "Adj. Op. Cash Flow",
                   "A: Fixed", "B: % Gross", "C: % Op CF", "D: Hybrid", "E: Holiday/Step",
                   "SELECTED (active option)"],
              "REVENUE-SHARE OPTIONS — Tribal Payment by Option",
              "All five computed every year; SELECTED follows the option switch. Payments beyond term = 0.")
for cc in "BCDEFGHI":
    Rs.column_dimensions[cc].width = 15
optA_fixed = REF["optA_fixed"].replace("$C$", "Assumptions!$C$")
optA_esc = REF["optA_esc"].replace("$C$", "Assumptions!$C$")
optB_pct = REF["optB_pct"].replace("$C$", "Assumptions!$C$")
optC_pct = REF["optC_pct"].replace("$C$", "Assumptions!$C$")
optD_base = REF["optD_base"].replace("$C$", "Assumptions!$C$")
optD_pct = REF["optD_pct"].replace("$C$", "Assumptions!$C$")
optE_hol = REF["optE_holiday"].replace("$C$", "Assumptions!$C$")
optE_first = REF["optE_first"].replace("$C$", "Assumptions!$C$")
optE_step = REF["optE_step"].replace("$C$", "Assumptions!$C$")
opt_a = REF["option"].replace("$C$", "Assumptions!$C$")
for y in YEARS:
    rr = yr_row(y)
    gate = "IF($A%d>%s,0,1)" % (rr, term_a)
    if y == 0:
        for cX in range(2, 10):
            C.xl_cell(Rs, rr, cX, 0, "formula", fmt=C.FMT_USD)
        continue
    C.xl_cell(Rs, rr, 2, "=%s" % RV_TOT(y), "formula", fmt=C.FMT_USD)
    C.xl_cell(Rs, rr, 3, "=%s-%s-%s" % (RV_TOT(y), OE_TOT(y), CR_ANN(y)), "formula", fmt=C.FMT_USD)
    # Option A: fixed escalated
    C.xl_cell(Rs, rr, 4, "=%s*(1+%s)^($A%d-1)*%s" % (optA_fixed, optA_esc, rr, gate), "formula", fmt=C.FMT_USD)
    # Option B: % of gross
    C.xl_cell(Rs, rr, 5, "=%s*$B%d*%s" % (optB_pct, rr, gate), "formula", fmt=C.FMT_USD)
    # Option C: % of positive op CF
    C.xl_cell(Rs, rr, 6, "=%s*MAX(0,$C%d)*%s" % (optC_pct, rr, gate), "formula", fmt=C.FMT_USD)
    # Option D: hybrid base + share
    C.xl_cell(Rs, rr, 7, "=(%s+%s*$B%d)*%s" % (optD_base, optD_pct, rr, gate), "formula", fmt=C.FMT_USD)
    # Option E: holiday then stepped
    C.xl_cell(Rs, rr, 8, "=IF($A%d<=%s,0,%s*(1+%s)^($A%d-%s-1))*%s"
              % (rr, optE_hol, optE_first, optE_step, rr, optE_hol, gate), "formula", fmt=C.FMT_USD)
    # Selected
    C.xl_cell(Rs, rr, 9, "=CHOOSE(%s,$D%d,$E%d,$F%d,$G%d,$H%d)" % (opt_a, rr, rr, rr, rr, rr),
              "output", fmt=C.FMT_USD, bold=True)
RS_SEL = lambda y: a("Revenue_Share_Options", yr_row(y), 9)
RS_ADJ = lambda y: a("Revenue_Share_Options", yr_row(y), 3)
crow = LASTROW + 2
check(Rs, crow, "CHECK: SELECTED equals the option chosen by the switch",
      '=IF(SUMPRODUCT(--(ABS($I%d:$I%d-CHOOSE(%s,$D%d:$D%d,$E%d:$E%d,$F%d:$F%d,$G%d:$G%d,$H%d:$H%d))>0.5))=0,"PASS","FAIL")'
      % (Y0, LASTROW, opt_a, Y0, LASTROW, Y0, LASTROW, Y0, LASTROW, Y0, LASTROW, Y0, LASTROW),
      "Revenue_Share_Options")

# ===========================================================================
# SHEET: Annual_Cash_Flow
# ===========================================================================
Ac = wb.create_sheet("Annual_Cash_Flow")
yearly_header(Ac, ["Year", "Gross Revenue", "Operating Expenses", "Capital Replacement",
                   "Adj. Operating CF", "Tribal Payment", "RIVR Net Cash Flow", "RIVR Cumulative"],
              "ANNUAL CASH FLOW — Consolidated",
              "Gross revenue - opex - capital replacement - Tribal payment = RIVR net. Year 0 = RIVR upfront investment.")
for cc in "BCDEFGH":
    Ac.column_dimensions[cc].width = 17
rivr_up = REF["rivr_upfront"].replace("$C$", "Assumptions!$C$")
for y in YEARS:
    rr = yr_row(y)
    if y == 0:
        C.xl_cell(Ac, rr, 2, 0, "formula", fmt=C.FMT_USD)
        C.xl_cell(Ac, rr, 3, 0, "formula", fmt=C.FMT_USD)
        C.xl_cell(Ac, rr, 4, 0, "formula", fmt=C.FMT_USD)
        C.xl_cell(Ac, rr, 5, 0, "formula", fmt=C.FMT_USD)
        C.xl_cell(Ac, rr, 6, 0, "formula", fmt=C.FMT_USD)
        C.xl_cell(Ac, rr, 7, "=-%s" % rivr_up, "output", fmt=C.FMT_USD, bold=True)  # upfront outflow
        C.xl_cell(Ac, rr, 8, "=$G%d" % rr, "formula", fmt=C.FMT_USD)
        continue
    C.xl_cell(Ac, rr, 2, "=%s" % RV_TOT(y), "formula", fmt=C.FMT_USD)
    C.xl_cell(Ac, rr, 3, "=%s" % OE_TOT(y), "formula", fmt=C.FMT_USD)
    C.xl_cell(Ac, rr, 4, "=%s" % CR_ANN(y), "formula", fmt=C.FMT_USD)
    C.xl_cell(Ac, rr, 5, "=$B%d-$C%d-$D%d" % (rr, rr, rr), "formula", fmt=C.FMT_USD)
    C.xl_cell(Ac, rr, 6, "=%s" % RS_SEL(y), "formula", fmt=C.FMT_USD)
    C.xl_cell(Ac, rr, 7, "=$E%d-$F%d" % (rr, rr), "output", fmt=C.FMT_USD, bold=True)
    C.xl_cell(Ac, rr, 8, "=$H%d+$G%d" % (rr - 1, rr), "formula", fmt=C.FMT_USD)
AC_RIVR = lambda y: a("Annual_Cash_Flow", yr_row(y), 7)
crow = LASTROW + 2
check(Ac, crow, "CHECK: RIVR net = adj op CF - Tribal payment (identity holds)",
      '=IF(SUMPRODUCT(--(ABS($G%d:$G%d-($E%d:$E%d-$F%d:$F%d))>0.5))=0,"PASS","FAIL")'
      % (Y0 + 1, LASTROW, Y0 + 1, LASTROW, Y0 + 1, LASTROW), "Annual_Cash_Flow")

# ===========================================================================
# SHEET: RIVR_Tech_Economics
# ===========================================================================
Re = wb.create_sheet("RIVR_Tech_Economics")
yearly_header(Re, ["Year", "RIVR Net Cash Flow", "Cumulative", "Payback Helper"],
              "RIVR TECH ECONOMICS — Cash Flow, NPV, IRR",
              "From the active scenario / term / option. NPV discounts Years 1-30; Year 0 at time zero.")
for cc in "BCD":
    Re.column_dimensions[cc].width = 20
disc_a = REF["disc"].replace("$C$", "Assumptions!$C$")
for y in YEARS:
    rr = yr_row(y)
    C.xl_cell(Re, rr, 2, "=%s" % AC_RIVR(y), "formula", fmt=C.FMT_USD)
    prev = "0" if y == 0 else "$C%d" % (rr - 1)
    C.xl_cell(Re, rr, 3, "=%s+$B%d" % (prev, rr), "formula", fmt=C.FMT_USD)
    C.xl_cell(Re, rr, 4, "=IF($C%d>=0,$A%d,9999)" % (rr, rr), "formula", fmt=C.FMT_NUM)
# summary block
sb = LASTROW + 2
C.xl_cell(Re, sb, 1, "SUMMARY", "section")
for cX in range(2, 5): C.xl_cell(Re, sb, cX, None, "section")
sb += 1
C.xl_cell(Re, sb, 1, "RIVR NPV (active)", "text")
C.xl_cell(Re, sb, 2, "=$B%d+NPV(%s,$B%d:$B%d)" % (Y0, disc_a, Y0 + 1, LASTROW), "output", fmt=C.FMT_USD, bold=True)
RIVR_NPV = a("RIVR_Tech_Economics", sb, 2); sb += 1
C.xl_cell(Re, sb, 1, "RIVR IRR (active)", "text")
C.xl_cell(Re, sb, 2, '=IFERROR(IRR($B%d:$B%d),"n/m")' % (Y0, LASTROW), "output", fmt=C.FMT_PCT, bold=True)
RIVR_IRR = a("RIVR_Tech_Economics", sb, 2); sb += 1
C.xl_cell(Re, sb, 1, "Payback (year cum. >= 0)", "text")
C.xl_cell(Re, sb, 2, '=IF(MIN($D%d:$D%d)=9999,"beyond horizon",MIN($D%d:$D%d))'
          % (Y0, LASTROW, Y0, LASTROW), "output", fmt=C.FMT_NUM, bold=True)
RIVR_PAYBACK = a("RIVR_Tech_Economics", sb, 2)

# ===========================================================================
# SHEET: Tribal_Economics
# ===========================================================================
Te = wb.create_sheet("Tribal_Economics")
yearly_header(Te, ["Year", "Tribal Payment", "Reserved-Capacity Value", "Total Tribal Receipts", "Cumulative"],
              "TRIBAL ECONOMICS — Receipts, NPV",
              "IRU/revenue-share payment plus reserved-capacity in-kind value. Grant funds the asset (no Tribal cash outlay).")
for cc in "BCDE":
    Te.column_dimensions[cc].width = 20
rescap_a = REF["res_cap_val"].replace("$C$", "Assumptions!$C$")
for y in YEARS:
    rr = yr_row(y)
    C.xl_cell(Te, rr, 2, "=%s" % RS_SEL(y), "formula", fmt=C.FMT_USD)
    if y == 0:
        C.xl_cell(Te, rr, 3, 0, "formula", fmt=C.FMT_USD)
    else:
        C.xl_cell(Te, rr, 3, "=%s*IF($A%d>%s,0,1)*MIN(1,$A%d/%s)" % (rescap_a, rr, term_a, rr, build_a),
                  "formula", fmt=C.FMT_USD)
    C.xl_cell(Te, rr, 4, "=$B%d+$C%d" % (rr, rr), "formula", fmt=C.FMT_USD)
    prev = "0" if y == 0 else "$E%d" % (rr - 1)
    C.xl_cell(Te, rr, 5, "=%s+$D%d" % (prev, rr), "output", fmt=C.FMT_USD)
sb = LASTROW + 2
C.xl_cell(Te, sb, 1, "Tribal NPV (active)", "text")
C.xl_cell(Te, sb, 2, "=NPV(%s,$D%d:$D%d)" % (disc_a, Y0 + 1, LASTROW), "output", fmt=C.FMT_USD, bold=True)
TRIBAL_NPV = a("Tribal_Economics", sb, 2); sb += 1
C.xl_cell(Te, sb, 1, "Total Tribal receipts (undiscounted)", "text")
C.xl_cell(Te, sb, 2, "=$E%d" % LASTROW, "output", fmt=C.FMT_USD, bold=True)
TRIBAL_TOTAL = a("Tribal_Economics", sb, 2)

# ===========================================================================
# SHEET: Consolidated_Project
# ===========================================================================
Cp = wb.create_sheet("Consolidated_Project")
yearly_header(Cp, ["Year", "Gross Revenue", "Operating Expenses", "Capital (constr./replace.)",
                   "Project Net Cash Flow", "Cumulative"],
              "CONSOLIDATED PROJECT ECONOMICS — Blended",
              "Total project view. Tribal payment is an internal transfer and nets out. Year 0 = construction + RIVR upfront.")
for cc in "BCDEF":
    Cp.column_dimensions[cc].width = 18
for y in YEARS:
    rr = yr_row(y)
    if y == 0:
        C.xl_cell(Cp, rr, 2, 0, "formula", fmt=C.FMT_USD)
        C.xl_cell(Cp, rr, 3, 0, "formula", fmt=C.FMT_USD)
        C.xl_cell(Cp, rr, 4, "=%s+%s" % (CB_TOTAL, rivr_up), "formula", fmt=C.FMT_USD)
        C.xl_cell(Cp, rr, 5, "=-$D%d" % rr, "output", fmt=C.FMT_USD, bold=True)
        C.xl_cell(Cp, rr, 6, "=$E%d" % rr, "formula", fmt=C.FMT_USD)
        continue
    C.xl_cell(Cp, rr, 2, "=%s" % RV_TOT(y), "formula", fmt=C.FMT_USD)
    C.xl_cell(Cp, rr, 3, "=%s" % OE_TOT(y), "formula", fmt=C.FMT_USD)
    C.xl_cell(Cp, rr, 4, "=%s" % CR_ANN(y), "formula", fmt=C.FMT_USD)
    C.xl_cell(Cp, rr, 5, "=$B%d-$C%d-$D%d" % (rr, rr, rr), "output", fmt=C.FMT_USD, bold=True)
    C.xl_cell(Cp, rr, 6, "=$F%d+$E%d" % (rr - 1, rr), "formula", fmt=C.FMT_USD)
sb = LASTROW + 2
C.xl_cell(Cp, sb, 1, "Project NPV (active)", "text")
C.xl_cell(Cp, sb, 2, "=$E%d+NPV(%s,$E%d:$E%d)" % (Y0, disc_a, Y0 + 1, LASTROW), "output", fmt=C.FMT_USD, bold=True)
PROJ_NPV = a("Consolidated_Project", sb, 2); sb += 1
C.xl_cell(Cp, sb, 1, "Project IRR (active)", "text")
C.xl_cell(Cp, sb, 2, '=IFERROR(IRR($E%d:$E%d),"n/m")' % (Y0, LASTROW), "output", fmt=C.FMT_PCT, bold=True)
PROJ_IRR = a("Consolidated_Project", sb, 2); sb += 1
crow = sb + 1
check(Cp, crow, "CHECK: project net = revenue - opex - capital (identity)",
      '=IF(SUMPRODUCT(--(ABS($E%d:$E%d-($B%d:$B%d-$C%d:$C%d-$D%d:$D%d))>0.5))=0,"PASS","FAIL")'
      % (Y0 + 1, LASTROW, Y0 + 1, LASTROW, Y0 + 1, LASTROW, Y0 + 1, LASTROW), "Consolidated_Project")

# ===========================================================================
# SHEET: Case_Engine  (scenario-independent mini-model, all three cases)
#   Powers NPV_IRR (3x3) and Scenario_Comparison honestly via formulas.
# ===========================================================================
Ce = wb.create_sheet("Case_Engine")
C.xl_title(Ce, "CASE ENGINE — Low / Base / High Parallel Cash Flows",
           "Formula computation blocks used by NPV_IRR and Scenario_Comparison. Each block reads its own Low/Base/High driver column and holds the OPTION switch constant.", span=13)
CE_HEADERS = ["Year", "Homes", "TakeRate", "Res Subs", "Bus Subs", "Ent Subs",
              "Gross Rev", "Opex", "Capital", "Adj Op CF", "Tribal Pmt", "RIVR Net", "Proj Net"]
for i in range(len(CE_HEADERS)):
    Ce.column_dimensions[col(2 + i)].width = 12

# assumption cells by case index (0=Low C, 1=Base D, 2=High E)
def ccell(key, i):
    return "Assumptions!%s" % CASE[key][i]

CE_BLOCKS = {}   # case_name -> (y0_row, rivr_col, proj_col)
block_start = HDR + 1
for ci, cname in enumerate(["Low", "Base", "High"]):
    br = block_start
    # block sub-title on its own row, then header, then data
    C.xl_cell(Ce, br, 2, "%s CASE" % cname.upper(), "section")
    for k in range(1, len(CE_HEADERS)):
        C.xl_cell(Ce, br, 2 + k, None, "section")
    C.xl_header_row(Ce, br + 1, CE_HEADERS, start_col=2, freeze=False, filt=False)
    data0 = br + 2
    tt_term = ccell("term_take", ci); tr_ramp = ccell("take_ramp", ci)
    ra = ccell("res_arpu", ci); ba = ccell("bus_arpu", ci); ea = ccell("ent_arpu", ci)
    va = ccell("voice_arpu", ci); emax = ccell("ent_max", ci); who = ccell("wholesale", ci)
    ch = ccell("churn", ci); bd = ccell("baddebt", ci); inf = ccell("infl", ci); cf = ccell("cfactor", ci)
    # per-case construction total & electronics basis
    constr_case = "(%s*%s)" % (CB_SUBCONT, cf)
    elec_case = "(%s*%s)" % (CB_ELEC, cf)
    for y in YEARS:
        rr = data0 + y
        C.xl_cell(Ce, rr, 2, y, "text", fmt=C.FMT_NUM)
        if y == 0:
            for k in range(3, 14):
                C.xl_cell(Ce, rr, 1 + k, 0, "formula", fmt=C.FMT_USD)
            # year 0 project net = -(constr_case + rivr upfront); rivr net = -upfront
            C.xl_cell(Ce, rr, 13, "=-%s" % rivr_up, "formula", fmt=C.FMT_USD)
            C.xl_cell(Ce, rr, 14, "=-(%s+%s)" % (constr_case, rivr_up), "formula", fmt=C.FMT_USD)
            continue
        homes = "%s*MIN(1,$B%d/%s)" % (homes_a, rr, build_a)
        C.xl_cell(Ce, rr, 3, "=%s" % homes, "formula", fmt=C.FMT_NUM)                       # C homes
        C.xl_cell(Ce, rr, 4, "=%s*MIN(1,$B%d/%s)" % (tt_term, rr, tr_ramp), "formula", fmt=C.FMT_PCT)  # D take
        C.xl_cell(Ce, rr, 5, "=$C%d*$D%d" % (rr, rr), "formula", fmt=C.FMT_NUM)             # E res
        C.xl_cell(Ce, rr, 6, "=$C%d*%s" % (rr, biz_pen), "formula", fmt=C.FMT_NUM)          # F bus
        C.xl_cell(Ce, rr, 7, "=%s*MIN(1,$B%d/%s)" % (emax, rr, tr_ramp), "formula", fmt=C.FMT_NUM)  # G ent
        voice = "$E%d*%s" % (rr, voice_att)
        adds = "MAX(0,($E%d+$F%d+$G%d)-(%s))+(%s)*%s" % (
            rr, rr, rr,
            "0" if y == 1 else "($E%d+$F%d+$G%d)" % (rr - 1, rr - 1, rr - 1),
            "0" if y == 1 else "($E%d+$F%d+$G%d)" % (rr - 1, rr - 1, rr - 1), ch)
        esc = "(1+%s)^($B%d-1)" % (arpu_esc_a, rr)
        rec = "($E%d*%s+$F%d*%s+$G%d*%s+(%s)*%s)*12*%s" % (rr, ra, rr, ba, rr, ea, voice, va, esc)
        whole = "%s*MIN(1,$B%d/%s)" % (who, rr, build_a)
        install = "(%s)*%s" % (adds, install_a)
        gross = "(%s)+(%s)+(%s)" % (rec, whole, install)
        C.xl_cell(Ce, rr, 8, "=%s" % gross, "formula", fmt=C.FMT_USD)                        # H gross rev
        inf_fac = "(1+%s)^($B%d-1)" % (inf, rr)
        opex = "%s*%s*%s+%s*%s*%s+%s*%s*%s+%s*$H%d+%s*$H%d+%s*(%s)" % (
            "($E%d+$F%d+$G%d)" % (rr, rr, rr), netops_a, inf_fac,   # network ops
            maint_a, constr_case, inf_fac,                          # maintenance
            heads_a, fte_a, inf_fac,                                # staffing
            mkt_a, rr, ga_a, rr,                                    # marketing + G&A
            bd, "(%s)+(%s)" % (rec, whole))                         # bad debt on recurring+wholesale
        C.xl_cell(Ce, rr, 9, "=%s" % opex, "formula", fmt=C.FMT_USD)                         # I opex
        cap = "%s/%s*%s" % (elec_case, cycle_a, inf_fac)
        C.xl_cell(Ce, rr, 10, "=%s" % cap, "formula", fmt=C.FMT_USD)                         # J capital
        C.xl_cell(Ce, rr, 11, "=$H%d-$I%d-$J%d" % (rr, rr, rr), "formula", fmt=C.FMT_USD)    # K adj op CF
        # Tribal payment (same option switch)
        pA = "%s*(1+%s)^($B%d-1)" % (optA_fixed, optA_esc, rr)
        pB = "%s*$H%d" % (optB_pct, rr)
        pC = "%s*MAX(0,$K%d)" % (optC_pct, rr)
        pD = "%s+%s*$H%d" % (optD_base, optD_pct, rr)
        pE = "IF($B%d<=%s,0,%s*(1+%s)^($B%d-%s-1))" % (rr, optE_hol, optE_first, optE_step, rr, optE_hol)
        C.xl_cell(Ce, rr, 12, "=CHOOSE(%s,%s,%s,%s,%s,%s)" % (opt_a, pA, pB, pC, pD, pE),
                  "formula", fmt=C.FMT_USD)                                                   # L tribal
        C.xl_cell(Ce, rr, 13, "=$K%d-$L%d" % (rr, rr), "formula", fmt=C.FMT_USD)             # M RIVR net
        C.xl_cell(Ce, rr, 14, "=$H%d-$I%d-$J%d" % (rr, rr, rr), "formula", fmt=C.FMT_USD)    # N proj net
    CE_BLOCKS[cname] = (data0, 13, 14)   # y0 row, rivr col(M=13), proj col(N=14)
    block_start = data0 + 31 + 2

# reconciliation check: Base case Year30 gross rev == live Revenue Year30 when scenario=2
recon_row = block_start
C.xl_cell(Ce, recon_row, 2, "Reconciliation (valid when Scenario switch = 2 / Base):", "text")
base_y0 = CE_BLOCKS["Base"][0]
scen_cell = "Assumptions!%s" % SCEN
check(Ce, recon_row + 1,
      "CHECK: Base-case Y30 gross revenue reconciles to live Revenue sheet (set Scenario=2)",
      '=IF(OR(%s<>2,ABS($H%d-%s)<50),"PASS","FAIL")'
      % (scen_cell, base_y0 + 30, RV_TOT(30)), "Case_Engine")

# ===========================================================================
# SHEET: NPV_IRR  (3 cases x 3 terms, formula-driven from Case_Engine)
# ===========================================================================
Ni = wb.create_sheet("NPV_IRR")
C.xl_title(Ni, "NPV & IRR — 3 Cases x 3 IRU Terms",
           "Computed from Case_Engine parallel cash flows. NPV discounts Years 1..T; IRR over Years 0..T. Discount rate & option follow Assumptions.", span=6)
for w, cc in [(30,"B"),(16,"C"),(16,"D"),(16,"E")]:
    Ni.column_dimensions[cc].width = w
terms = [20, 25, 30]
def npv_block(title, start, colidx):
    C.xl_cell(Ni, start, 2, title, "section")
    for cX in range(3, 6): C.xl_cell(Ni, start, cX, None, "section")
    hr = start + 1
    C.xl_header_row(Ni, hr, ["Metric \\ Term", "20-yr", "25-yr", "30-yr"], start_col=2, freeze=False, filt=False)
    # NPV row
    C.xl_cell(Ni, hr + 1, 2, "NPV", "text")
    C.xl_cell(Ni, hr + 2, 2, "IRR", "text")
    for j, cname in enumerate(["Low", "Base", "High"]):
        pass
    return hr

# Layout: three metric tables (Low / Base / High), each Term columns; within each,
# NPV & IRR rows for both RIVR and Project.
row = HDR + 1
for cname in ["Low", "Base", "High"]:
    y0, rivr_c, proj_c = CE_BLOCKS[cname]
    C.xl_cell(Ni, row, 2, "%s CASE" % cname.upper(), "section")
    for cX in range(3, 6): C.xl_cell(Ni, row, cX, None, "section")
    row += 1
    C.xl_header_row(Ni, row, ["Metric \\ IRU Term", "20-yr", "25-yr", "30-yr"],
                    start_col=2, freeze=False, filt=False)
    row += 1
    for label, cc, kind in [("RIVR NPV", rivr_c, "npv"), ("RIVR IRR", rivr_c, "irr"),
                            ("Project NPV", proj_c, "npv"), ("Project IRR", proj_c, "irr")]:
        C.xl_cell(Ni, row, 2, "%s (%s case)" % (label, cname), "text")
        for j, T in enumerate(terms):
            yT = y0 + T
            if kind == "npv":
                f = "=Case_Engine!$%s$%d+NPV(%s,Case_Engine!$%s$%d:$%s$%d)" % (
                    col(cc), y0, disc_a, col(cc), y0 + 1, col(cc), yT)
                C.xl_cell(Ni, row, 3 + j, f, "output", fmt=C.FMT_USD)
            else:
                f = '=IFERROR(IRR(Case_Engine!$%s$%d:$%s$%d),"n/m")' % (col(cc), y0, col(cc), yT)
                C.xl_cell(Ni, row, 3 + j, f, "output", fmt=C.FMT_PCT)
        row += 1
    row += 1

# ===========================================================================
# SHEET: Sensitivity  (one- and two-way, formula tables)
# ===========================================================================
Se = wb.create_sheet("Sensitivity")
C.xl_title(Se, "SENSITIVITY — Take Rate & ARPU vs RIVR NPV",
           "Formula-driven. Recomputes a simplified 30-yr RIVR NPV as take rate and residential ARPU flex around the active case.", span=9)
for cc in "BCDEFGHI":
    Se.column_dimensions[cc].width = 13
# We build a compact NPV proxy that recomputes from scratch using overridden
# take-rate / ARPU while holding all other active drivers constant.
# Proxy: level-annuity approximation using terminal-year economics is avoided;
# instead we reference a helper 2-way grid computed with closed-form per-year sums.
# For transparency & to stay formula-based, use a simplified steady-state model:
#   annual net ~ (homes*take*res_arpu*12*(1-opex_load) - tribalB) ; NPV via PV factor.
# Header explains the simplification.
sr = HDR
C.xl_cell(Se, sr, 2, "Two-way sensitivity: Residential ARPU (rows) x Terminal Take Rate (cols)", "section")
for cX in range(3, 10): C.xl_cell(Se, sr, cX, None, "section")
sr += 1
C.xl_cell(Se, sr, 2, "Simplified steady-state RIVR NPV proxy ($). Holds other active drivers fixed; for directional read only.", "text")
Se.merge_cells(start_row=sr, start_column=2, end_row=sr, end_column=9)
sr += 2
# axes
take_axis = [0.30, 0.375, 0.45, 0.525, 0.60]
arpu_axis = [55, 65, 75, 85, 95]
# corner label + column headers (take rates)
C.xl_cell(Se, sr, 2, "ARPU \\ Take", "formula", bold=True)
tr_cols = {}
for j, tv in enumerate(take_axis):
    C.xl_cell(Se, sr, 3 + j, tv, "input", fmt=C.FMT_PCT)
    tr_cols[j] = 3 + j
take_hdr_row = sr
sr += 1
homes_ref = homes_a
disc_ref = disc_a
netops_ref = netops_a
mkt_ref = mkt_a
ga_ref = ga_a
optB_ref = optB_pct
# PV of a growing-to-terminal stream approximated as level annuity at terminal over 30 yrs
# annual_net = homes*take*arpu*12 - opex_load - tribal(optionB proxy)
# opex_load ~ (mkt%+ga%)*rev + homes*take*netops ; NPV = annual_net * PV_annuity(disc,30)
for i, av in enumerate(arpu_axis):
    C.xl_cell(Se, sr, 2, av, "input", fmt=C.FMT_USD)
    for j, tv in enumerate(take_axis):
        take_c = "%s%d" % (col(3 + j), take_hdr_row)          # take rate header cell
        arpu_c = "$B%d" % sr                                   # arpu cell
        rev = "%s*%s*%s*12" % (homes_ref, take_c, arpu_c)
        opex = "(%s+%s)*(%s)+%s*%s*%s" % (mkt_ref, ga_ref, rev, homes_ref, take_c, netops_ref)
        tribal = "%s*(%s)" % (optB_ref, rev)
        net = "(%s)-(%s)-(%s)" % (rev, opex, tribal)
        pvann = "(1-(1+%s)^-30)/%s" % (disc_ref, disc_ref)
        C.xl_cell(Se, sr, 3 + j, "=(%s)*(%s)" % (net, pvann), "output", fmt=C.FMT_USD)
    sr += 1
# one-way sensitivity (take rate vs NPV proxy) below
sr += 1
C.xl_cell(Se, sr, 2, "One-way sensitivity: Terminal Take Rate vs RIVR NPV proxy (residential ARPU = active case)", "section")
for cX in range(3, 10): C.xl_cell(Se, sr, cX, None, "section")
sr += 1
C.xl_header_row(Se, sr, ["Terminal Take Rate", "RIVR NPV proxy ($)"], start_col=2, freeze=False, filt=False)
sr += 1
res_active = REF["res_arpu"].replace("$F$", "Assumptions!$F$")
for tv in take_axis:
    C.xl_cell(Se, sr, 2, tv, "input", fmt=C.FMT_PCT)
    take_c = "$B%d" % sr
    rev = "%s*%s*%s*12" % (homes_ref, take_c, res_active)
    opex = "(%s+%s)*(%s)+%s*%s*%s" % (mkt_ref, ga_ref, rev, homes_ref, take_c, netops_ref)
    tribal = "%s*(%s)" % (optB_ref, rev)
    net = "(%s)-(%s)-(%s)" % (rev, opex, tribal)
    pvann = "(1-(1+%s)^-30)/%s" % (disc_ref, disc_ref)
    C.xl_cell(Se, sr, 3, "=(%s)*(%s)" % (net, pvann), "output", fmt=C.FMT_USD)
    sr += 1

# ===========================================================================
# SHEET: Scenario_Comparison
# ===========================================================================
Sc = wb.create_sheet("Scenario_Comparison")
C.xl_title(Sc, "SCENARIO COMPARISON — Low / Base / High",
           "Key outputs from Case_Engine (30-yr horizon, active option). Independent of the Scenario switch.", span=5)
for w, cc in [(38,"B"),(18,"C"),(18,"D"),(18,"E")]:
    Sc.column_dimensions[cc].width = w
C.xl_header_row(Sc, HDR, ["Output Metric", "Low", "Base", "High"], start_col=2)
metrics_rows = []
def scen_row(rr, label, builder, fmt):
    C.xl_cell(Sc, rr, 2, label, "text")
    for j, cname in enumerate(["Low", "Base", "High"]):
        y0, rivr_c, proj_c = CE_BLOCKS[cname]
        C.xl_cell(Sc, rr, 3 + j, builder(y0, rivr_c, proj_c), "output", fmt=fmt)
scr = HDR + 1
scen_row(scr, "Year-30 gross revenue",
         lambda y0, rc, pc: "=Case_Engine!$H$%d" % (y0 + 30), C.FMT_USD); scr += 1
scen_row(scr, "Cumulative Tribal payments (30 yr)",
         lambda y0, rc, pc: "=SUM(Case_Engine!$L$%d:$L$%d)" % (y0, y0 + 30), C.FMT_USD); scr += 1
scen_row(scr, "RIVR NPV (30-yr term)",
         lambda y0, rc, pc: "=Case_Engine!$%s$%d+NPV(%s,Case_Engine!$%s$%d:$%s$%d)"
         % (col(rc), y0, disc_a, col(rc), y0 + 1, col(rc), y0 + 30), C.FMT_USD); scr += 1
scen_row(scr, "RIVR IRR (30-yr term)",
         lambda y0, rc, pc: '=IFERROR(IRR(Case_Engine!$%s$%d:$%s$%d),"n/m")'
         % (col(rc), y0, col(rc), y0 + 30), C.FMT_PCT); scr += 1
scen_row(scr, "Project NPV (30-yr term)",
         lambda y0, rc, pc: "=Case_Engine!$%s$%d+NPV(%s,Case_Engine!$%s$%d:$%s$%d)"
         % (col(pc), y0, disc_a, col(pc), y0 + 1, col(pc), y0 + 30), C.FMT_USD); scr += 1

# ===========================================================================
# SHEET: Dashboard
# ===========================================================================
Db = wb.create_sheet("Dashboard")
Db.sheet_properties.tabColor = "1F3864"
C.xl_title(Db, "EXECUTIVE DASHBOARD",
           "Active scenario / term / option, headline outputs, and formula-check roll-up. All values are live formulas.", span=6)
for w, cc in [(42,"B"),(24,"C"),(6,"D"),(42,"E"),(24,"F")]:
    Db.column_dimensions[cc].width = w
C.xl_legend(Db, 4)
dr = 6
C.xl_cell(Db, dr, 2, "ACTIVE SETTINGS", "section"); C.xl_cell(Db, dr, 3, None, "section"); dr += 1
C.xl_cell(Db, dr, 2, "Scenario", "text")
C.xl_cell(Db, dr, 3, "=Assumptions!$D$%d" % SCEN_ROW, "formula"); dr += 1
C.xl_cell(Db, dr, 2, "IRU term (years)", "text")
C.xl_cell(Db, dr, 3, "=Assumptions!%s" % TERM, "formula", fmt=C.FMT_NUM); dr += 1
C.xl_cell(Db, dr, 2, "Revenue-share option", "text")
C.xl_cell(Db, dr, 3, "=Assumptions!%s" % REF["opt_name"], "formula")
Db.merge_cells(start_row=dr, start_column=3, end_row=dr, end_column=4); dr += 1
C.xl_cell(Db, dr, 2, "TBCP grant amount", "text")
C.xl_cell(Db, dr, 3, "=Assumptions!%s" % REF["grant"], "formula", fmt=C.FMT_USD); dr += 1
C.xl_cell(Db, dr, 2, "Homes passed (total)", "text")
C.xl_cell(Db, dr, 3, "=Assumptions!%s" % REF["homes"], "formula", fmt=C.FMT_NUM); dr += 1
C.xl_cell(Db, dr, 2, "Discount rate (NPV)", "text")
C.xl_cell(Db, dr, 3, "=Assumptions!%s" % REF["disc"], "formula", fmt=C.FMT_PCT); dr += 2

C.xl_cell(Db, dr, 2, "HEADLINE OUTPUTS (active case)", "section"); C.xl_cell(Db, dr, 3, None, "section"); dr += 1
C.xl_cell(Db, dr, 2, "Year-30 gross revenue", "text")
C.xl_cell(Db, dr, 3, "=%s" % RV_TOT(30), "output", fmt=C.FMT_USD, bold=True); dr += 1
C.xl_cell(Db, dr, 2, "Total Tribal receipts (undiscounted)", "text")
C.xl_cell(Db, dr, 3, "=%s" % TRIBAL_TOTAL, "output", fmt=C.FMT_USD, bold=True); dr += 1
C.xl_cell(Db, dr, 2, "Tribal NPV", "text")
C.xl_cell(Db, dr, 3, "=%s" % TRIBAL_NPV, "output", fmt=C.FMT_USD, bold=True); dr += 1
C.xl_cell(Db, dr, 2, "RIVR Tech NPV", "text")
C.xl_cell(Db, dr, 3, "=%s" % RIVR_NPV, "output", fmt=C.FMT_USD, bold=True); dr += 1
C.xl_cell(Db, dr, 2, "RIVR Tech IRR", "text")
C.xl_cell(Db, dr, 3, "=%s" % RIVR_IRR, "output", fmt=C.FMT_PCT, bold=True); dr += 1
C.xl_cell(Db, dr, 2, "RIVR payback (year)", "text")
C.xl_cell(Db, dr, 3, "=%s" % RIVR_PAYBACK, "output", fmt=C.FMT_NUM, bold=True); dr += 1
C.xl_cell(Db, dr, 2, "Project NPV", "text")
C.xl_cell(Db, dr, 3, "=%s" % PROJ_NPV, "output", fmt=C.FMT_USD, bold=True); dr += 1
C.xl_cell(Db, dr, 2, "Project IRR", "text")
C.xl_cell(Db, dr, 3, "=%s" % PROJ_IRR, "output", fmt=C.FMT_PCT, bold=True); dr += 2

# formula-check roll-up
C.xl_cell(Db, dr, 2, "FORMULA-CHECK ROLL-UP", "section"); C.xl_cell(Db, dr, 3, None, "section"); dr += 1
rollup_terms = "+".join('--(%s!%s="PASS")' % (s, c) for s, c in CHECK_CELLS)
n = len(CHECK_CELLS)
C.xl_cell(Db, dr, 2, "Checks passing", "text")
C.xl_cell(Db, dr, 3, "=%s" % ("+".join('--(%s!%s="PASS")' % (s, c) for s, c in CHECK_CELLS)),
          "formula", fmt=C.FMT_NUM); dr += 1
C.xl_cell(Db, dr, 2, "Total checks", "text")
C.xl_cell(Db, dr, 3, n, "formula", fmt=C.FMT_NUM); dr += 1
C.xl_cell(Db, dr, 2, "OVERALL STATUS", "text", bold=True)
status = '=IF((%s)=%d,"ALL CHECKS PASS","REVIEW — SEE FAILED CHECKS")' % (rollup_terms, n)
cc = C.xl_cell(Db, dr, 3, status, "output", bold=True)
pass_fail_cf(Db, "%s%d" % (col(3), dr))
Db.merge_cells(start_row=dr, start_column=3, end_row=dr, end_column=4)
# list each check on the right side
er = 6
C.xl_cell(Db, er, 5, "INDIVIDUAL CHECKS", "section"); C.xl_cell(Db, er, 6, None, "section"); er += 1
for s, c in CHECK_CELLS:
    C.xl_cell(Db, er, 5, s, "text")
    C.xl_cell(Db, er, 6, "=%s!%s" % (s, c), "formula")
    pass_fail_cf(Db, "%s%d" % (col(6), er))
    er += 1

# ===========================================================================
# SHEET: Instructions  (built last; content references final structure)
# ===========================================================================
instr = [
    "## Deliverable 10 — 30-Year Editable Financial Model",
    "Lumbee Tribe of North Carolina  &  LREMC Technologies, LLC d/b/a RIVR Tech",
    "TBCP grant-funded hybrid broadband network — southeastern North Carolina.",
    "",
    "## DRAFT / PLACEHOLDER WARNING",
    "Every dollar figure, rate, and count in this workbook is a PLACEHOLDER for negotiation. "
    "The model is a working draft — subject to legal, grant, and financial review. Do NOT rely "
    "on any output as a final term. Replace the amber input cells with negotiated values.",
    "",
    "## COLOR LEGEND",
    "• AMBER  = INPUT — edit these. All assumptions live on the Assumptions sheet.",
    "• BLUE   = FORMULA — do not edit; these compute from inputs.",
    "• GREEN  = OUTPUT / RESULT — headline numbers and NPV/IRR.",
    "The model is designed to be used WITHOUT editing any formula — change inputs only.",
    "",
    "## THE THREE SWITCHES (all on the Assumptions sheet, top block)",
    "• Scenario switch  — type 1 (Low), 2 (Base), or 3 (High). Drives every scenario-dependent "
    "driver (take rate, ARPU, churn, bad debt, inflation, construction cost) via CHOOSE.",
    "• IRU term switch  — choose 20, 25, or 30 years (recommended 30). Revenue and Tribal "
    "payments beyond the selected term are set to zero, controlling the NPV/IRR horizon.",
    "• Revenue-share option switch — type 1=A, 2=B, 3=C, 4=D (recommended), 5=E. Selects which "
    "Tribal-payment structure flows into the cash flows; all five are shown side-by-side on "
    "Revenue_Share_Options.",
    "",
    "## PRIMARY INPUT CELLS (edit these first)",
    "• Assumptions!C%d — Scenario switch (1/2/3)" % SCEN_ROW,
    "• Assumptions!C%d — IRU term (20/25/30)" % TERM_ROW,
    "• Assumptions!C%d — Revenue-share option (1-5)" % OPT_ROW,
    "• Assumptions — SCENARIO-DEPENDENT DRIVERS block: Low/Base/High columns for take rate, "
    "ARPU (res/bus/ent/voice), enterprise count, wholesale, churn, bad debt, inflation, "
    "construction cost factor.",
    "• Assumptions — SINGLE INPUTS block: grant amount, homes passed, build-out years, "
    "penetration/attach rates, install fee, opex components, staffing, electronics cycle, "
    "reserve %, discount rate, RIVR upfront, reserved-capacity value.",
    "• Assumptions — REVENUE-SHARE OPTION INPUTS block: fixed payment & escalator (A), gross "
    "share % (B), cash-flow share % (C), hybrid base + share (D), holiday/first/step (E).",
    "• Construction_Budget — quantities, unit costs, and contingency % (amber).",
    "• Grant_Funding — non-federal match (0; TBCP requires none).",
    "",
    "## HOW THE SHEETS FLOW",
    "Assumptions -> Construction_Budget -> Grant_Funding (sources=uses check) ; "
    "Homes_Passed -> Take_Rate_Customers -> Revenue -> Operating_Expenses / Capital_Replacement "
    "-> Revenue_Share_Options -> Annual_Cash_Flow -> RIVR_Tech_Economics / Tribal_Economics / "
    "Consolidated_Project. Case_Engine computes all three cases in parallel to power NPV_IRR "
    "(3 cases x 3 terms), Sensitivity, and Scenario_Comparison. Dashboard rolls everything up.",
    "",
    "## FORMULA CHECKS",
    "Each computation sheet carries a PASS/FAIL check (green/red). The Dashboard shows an "
    "overall roll-up: sources=uses, homes>=customers, no #REF, reserve adequacy, option "
    "reconciliation, cash-flow identities, and Base-case reconciliation. If any check reads "
    "FAIL, investigate before relying on outputs.",
    "",
    "## RECALCULATION NOTE",
    "This file is generated by a script and stores formulas (not cached results). Open it in "
    "Excel / LibreOffice and allow calculation (F9) so every blue/green cell evaluates.",
]
C.xl_instructions(wb, instr, title="INSTRUCTIONS — READ FIRST")

# move Instructions + Dashboard to the front for usability
wb.move_sheet("Instructions", -(len(wb.sheetnames)))
order = ["Instructions", "Dashboard", "Assumptions", "Construction_Budget", "Grant_Funding",
         "Homes_Passed", "Take_Rate_Customers", "Revenue", "Operating_Expenses",
         "Capital_Replacement", "Revenue_Share_Options", "Annual_Cash_Flow",
         "RIVR_Tech_Economics", "Tribal_Economics", "Consolidated_Project",
         "Case_Engine", "NPV_IRR", "Sensitivity", "Scenario_Comparison"]
wb._sheets.sort(key=lambda s: order.index(s.title) if s.title in order else 99)

path = C.xl_save(wb, "04_Financial_Model", "Lumbee_RIVR_Tech_IRU_Financial_Model.xlsx")
print("SAVED ->", path)
print("SHEETS:", len(wb.sheetnames))
for s in wb.sheetnames:
    print("  -", s)
print("CHECKS registered:", len(CHECK_CELLS))
