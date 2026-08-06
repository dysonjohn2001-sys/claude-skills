"""06_Lifeline_Financial_Model.xlsx — formula-driven, editable-assumption workbook.

All customer-facing math uses VISIBLE FORMULAS referencing the Assumptions tab.
RIVR Tech retail prices/costs are ILLUSTRATIVE PLACEHOLDERS (orange) that must be
replaced with confirmed figures. Federal benefit amounts are program constants
(blue) to re-verify each program year.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from style_helpers import (title, subtitle, header_row, cell, widths, legend,
    USD, USD0, PCT, NUM, NAVY, BLUE, YELLOW, ORANGE, LIGHT_BLUE, GREEN, RED, WHITE)

wb = Workbook()

# =====================================================================
# COVER
# =====================================================================
ws = wb.active
ws.title = "Cover"
ws.sheet_view.showGridLines = False
widths(ws, {"A": 3, "B": 90})
title(ws, "B2", "RIVR Tech — Lifeline & Lumbee Broadband Affordability", 18)
title(ws, "B3", "Financial Model  (Deliverable 06)", 14)
subtitle(ws, "B5", "LREMC Technologies, LLC d/b/a RIVR Tech")
rows = [
    ("B7", "Document owner:", "Finance / FP&A  (with Program Owner)"),
    ("B8", "Version:", "v0.1 — DRAFT for internal review"),
    ("B9", "Prepared:", "Program build phase (Phase 0 — ETC application pending)"),
    ("B10", "Status:", "PRE-DECISION. All retail prices, costs and volumes are ILLUSTRATIVE PLACEHOLDERS."),
]
for coord, k, v in rows:
    ws[coord] = f"{k}  {v}"
    ws[coord].font = Font(size=11, bold=(k.endswith(':') and 'owner' in k))
ws["B12"] = ("HOW TO USE:  Edit only the yellow (INPUT) and orange (PLACEHOLDER) cells. "
    "Orange cells contain illustrative numbers that MUST be replaced with figures "
    "confirmed by RIVR Tech (retail rates, costs) or USAC (benefit amounts) before any "
    "decision relies on this model. Blue cells are federal program constants — re-verify "
    "each program year against the cited source. White cells are formulas; do not hand-edit.")
ws["B12"].alignment = Alignment(wrap_text=True, vertical="top")
ws.row_dimensions[12].height = 90
ws["B14"] = ("CRITICAL COMPLIANCE NOTE:  The enhanced Tribal Lifeline benefit ($34.25) is "
    "modeled ONLY for subscribers whose PRINCIPAL RESIDENCE is confirmed on qualifying "
    "Tribal lands per 47 C.F.R. 54.400(e). Lumbee tribal membership does NOT by itself "
    "qualify a customer for enhanced support. Until a written USAC/legal determination "
    "confirms qualifying Tribal lands exist in the service area, set the enhanced-Tribal "
    "subscriber count to ZERO in the Assumptions tab.")
ws["B14"].alignment = Alignment(wrap_text=True, vertical="top")
ws["B14"].font = Font(color=RED, bold=True, size=10)
ws.row_dimensions[14].height = 90
legend(ws, 17, col=2)

# =====================================================================
# ASSUMPTIONS
# =====================================================================
a = wb.create_sheet("Assumptions")
a.sheet_view.showGridLines = False
widths(a, {"A": 3, "B": 48, "C": 14, "D": 10, "E": 60})
title(a, "B2", "Editable Assumptions", 15)
subtitle(a, "B3", "Named ranges drive every other tab. Confirm every orange cell before use.")
header_row(a, 5, ["Assumption", "Value", "Unit", "Source / note"], start_col=2)

r = 6
def arow(label, value, kind, unit, note, num=None, name=None):
    global r
    cell(a, f"B{r}", label, "grey", bold=True)
    c = cell(a, f"C{r}", value, kind, num=num or USD)
    cell(a, f"D{r}", unit, "grey")
    cell(a, f"E{r}", note, "grey", wrap=True, size=9)
    if name:
        wb.defined_names.add(__import__("openpyxl").workbook.defined_name.DefinedName(
            name, attr_text=f"Assumptions!$C${r}"))
    a.row_dimensions[r].height = 28
    r += 1

# --- Federal program constants ---
cell(a, "B5", "Assumption", "constant", bold=True)  # keep header styled
a.cell(row=r, column=2, value="— FEDERAL PROGRAM CONSTANTS (re-verify each program year) —").font = Font(bold=True, italic=True, color=BLUE)
r += 1
arow("Standard Lifeline benefit (broadband)", 9.25, "constant", "$/mo",
     "47 C.F.R. 54.403(a). Confirm current amount at USAC.", USD, "LL_STD")
arow("Enhanced Tribal ADDITIONAL support", 25.00, "constant", "$/mo",
     "47 C.F.R. 54.403(a)(3). Added ON TOP of standard; total up to $34.25.", USD, "LL_TRIBAL_ADD")
arow("Enhanced Tribal TOTAL benefit", "=LL_STD+LL_TRIBAL_ADD", "calc", "$/mo",
     "Standard + Tribal enhancement.", USD, "LL_TRIBAL_TOTAL")
arow("Lifeline income threshold", 1.35, "constant", "x FPG",
     "135% of Federal Poverty Guidelines — 47 C.F.R. 54.409(a). Verify annual $ figures.", PCT)

a.cell(row=r, column=2, value="— RIVR TECH RETAIL & COST INPUTS (PLACEHOLDER — replace with confirmed figures) —").font = Font(bold=True, italic=True, color=RED)
r += 1
arow("Senior 100/100 plan — retail (list) rate", 55.00, "placeholder", "$/mo",
     "ILLUSTRATIVE. NEW tier below current 250/250 entry. Confirm rate w/ RIVR.", USD, "RETAIL_SENIOR")
arow("Current ENTRY tier (250/250 sym.) retail rate", 69.95, "placeholder", "$/mo",
     "ILLUSTRATIVE. RIVR's lowest current tier is 250/250. Confirm price w/ RIVR.", USD, "RETAIL_STD")
arow("Senior plan target CUSTOMER payment", 10.00, "input", "$/mo",
     "Program design target (before tax). Executive decision.", USD, "TARGET_PAY")
arow("Equipment / managed Wi-Fi charge (monthly)", 5.00, "placeholder", "$/mo",
     "RIVR site: $5/mo indoor Wi-Fi 6 router (/$10 outdoor mesh). Confirm & decide if waived for program. Sep. tax.", USD, "EQUIP_MO")
arow("Installation charge (one-time)", 0.00, "placeholder", "$ one-time",
     "RIVR site: install advertised free ($99 value, promotional). Confirm program policy.", USD, "INSTALL")
arow("Optional voice add-on charge", 0.00, "placeholder", "$/mo",
     "ILLUSTRATIVE. Voice is optional; Lifeline min-standard is broadband.", USD, "VOICE_MO")
arow("Variable network + support cost / sub", 22.00, "placeholder", "$/mo",
     "ILLUSTRATIVE avoided/served cost per subscriber. Confirm w/ Finance.", USD, "VAR_COST")
arow("Billing + compliance labor / sub / mo", 3.50, "placeholder", "$/mo",
     "ILLUSTRATIVE fully-loaded ongoing admin per active Lifeline sub.", USD, "ADMIN_COST")
arow("Customer acquisition cost (one-time)", 45.00, "placeholder", "$/enroll",
     "ILLUSTRATIVE. Outreach, enrollment labor, QC per new enrollee.", USD, "CAC")
arow("Bad-debt rate (on customer-paid portion)", 0.04, "input", "% ",
     "ILLUSTRATIVE. Lifeline reduces customer bill so exposure is low.", PCT, "BADDEBT")
arow("USAC reimbursement lag", 1, "input", "months",
     "Claim filed after service month; cash received after. Confirm cycle.", NUM, "USAC_LAG")

a.cell(row=r, column=2, value="— OPTIONAL PROGRAM DISCOUNTS (executive decisions) —").font = Font(bold=True, italic=True, color=NAVY)
r += 1
arow("RIVR-funded discount / sub (non-Lifeline senior)", 0.00, "input", "$/mo",
     "Company subsidy to reach target for seniors w/o Lifeline (Alt A).", USD, "RIVR_DISC")
arow("Lumbee Tribe-funded discount / sub", 0.00, "input", "$/mo",
     "ONLY if Tribe funds it under a signed MOU. Separate accounting.", USD, "TRIBE_DISC")

a.cell(row=r, column=2, value="— SUBSCRIBER VOLUMES (Expected scenario — see Subscriber Model for all 3) —").font = Font(bold=True, italic=True, color=NAVY)
r += 1
arow("Std-Lifeline senior subs (steady-state)", 300, "input", "subs",
     "Seniors approved for STANDARD Lifeline via National Verifier.", NUM, "N_STD")
arow("Enhanced-Tribal subs (steady-state)", 0, "input", "subs",
     "SET TO 0 until qualifying Tribal lands confirmed by USAC/legal.", NUM, "N_TRIBAL")
arow("Senior subs, NO Lifeline (company-funded)", 150, "input", "subs",
     "Seniors on the $10 plan who do not qualify for Lifeline.", NUM, "N_NOLL")
arow("Avg. monthly gross enrollments (ramp)", 40, "input", "subs/mo",
     "New approved enrollments per month during ramp.", NUM, "ENROLL_MO")
arow("Monthly de-enrollment / churn rate", 0.02, "input", "%/mo",
     "Failure to recertify, moves, loss of eligibility, non-pay.", PCT, "CHURN")

a.cell(row=r, column=2, value="Break-even / sustainability check ↓").font = Font(bold=True)
r += 2
legend(a, r, col=2)

# =====================================================================
# PRICING MATRIX  (6 scenarios x line items)
# =====================================================================
p = wb.create_sheet("Pricing Matrix")
p.sheet_view.showGridLines = False
widths(p, {"A": 3, "B": 34, "C": 15, "D": 15, "E": 15, "F": 15, "G": 15, "H": 17})
title(p, "B2", "Pricing & Subsidy Matrix — per-subscriber monthly economics", 14)
subtitle(p, "B3", "All figures pre-tax. 'Plus tax' disclosure pending RIVR tax-advisor confirmation. Formulas reference Assumptions.")
scen = ["(1) Regular retail", "(2) + Standard Lifeline", "(3) + Enhanced Tribal",
        "(4) + RIVR discount", "(5) + Tribe discount", "(6) Senior 100/100 target"]
header_row(p, 5, ["Line item"] + scen, start_col=2)
p.row_dimensions[5].height = 40

# columns C..H = scenarios 1..6
# Row map
lines = [
    ("Retail (list) price", [
        "=RETAIL_STD", "=RETAIL_STD", "=RETAIL_STD", "=RETAIL_SENIOR", "=RETAIL_SENIOR", "=RETAIL_SENIOR"]),
    ("Less: Standard Lifeline credit", [
        0, "=-LL_STD", "=-LL_STD", "=-LL_STD", "=-LL_STD", "=-LL_STD"]),
    ("Less: Tribal enhancement credit", [
        0, 0, "=-LL_TRIBAL_ADD", 0, 0, 0]),
    ("Less: RIVR-funded discount", [
        0, 0, 0, "=-RIVR_DISC", "=-RIVR_DISC",
        "=-(MAX(0,RETAIL_SENIOR-LL_STD-TARGET_PAY))"]),
    ("Less: Tribe-funded discount", [
        0, 0, 0, 0, "=-TRIBE_DISC", "=-TRIBE_DISC"]),
    ("Plus: Equipment / mgd Wi-Fi", [
        "=EQUIP_MO"]*6),
    ("Plus: Optional voice", [
        "=VOICE_MO", "=VOICE_MO", "=VOICE_MO", "=VOICE_MO", "=VOICE_MO", "=VOICE_MO"]),
]
rr = 6
line_rows = {}
for label, vals in lines:
    cell(p, f"B{rr}", label, "grey", bold=True, size=9)
    for i, v in enumerate(vals):
        col = chr(ord('C') + i)
        cell(p, f"{col}{rr}", v, "calc", num=USD)
    line_rows[label] = rr
    rr += 1
# subtotal: final customer payment (pre-tax)
cell(p, f"B{rr}", "= FINAL CUSTOMER PAYMENT (pre-tax)", "good", bold=True, size=9)
for i in range(6):
    col = chr(ord('C') + i)
    cols = [f"{col}{line_rows[l]}" for l in ["Retail (list) price","Less: Standard Lifeline credit",
        "Less: Tribal enhancement credit","Less: RIVR-funded discount","Less: Tribe-funded discount",
        "Plus: Equipment / mgd Wi-Fi","Plus: Optional voice"]]
    cell(p, f"{col}{rr}", "=" + "+".join(cols), "good", num=USD, bold=True)
pay_row = rr
rr += 1
# Taxes note row
cell(p, f"B{rr}", "Applicable taxes & fees", "grey", size=9)
for i in range(6):
    col = chr(ord('C') + i)
    cell(p, f"{col}{rr}", "TBD", "placeholder", size=9, align="center")
rr += 1
cell(p, f"B{rr}", "USAC reimbursement to RIVR", "grey", bold=True, size=9)
usac_vals = [0, "=LL_STD", "=LL_TRIBAL_TOTAL", "=LL_STD", "=LL_STD", "=LL_STD"]
for i, v in enumerate(usac_vals):
    col = chr(ord('C') + i)
    cell(p, f"{col}{rr}", v, "calc", num=USD)
usac_row = rr
rr += 1
# RIVR net revenue = customer payment (excl tax & excl tribe/rivr discount cost?) + USAC reimb - discounts funded by RIVR
cell(p, f"B{rr}", "RIVR gross revenue (cust pay + USAC)", "grey", bold=True, size=9)
for i in range(6):
    col = chr(ord('C') + i)
    # customer payment MINUS voice/equip pass-through kept, PLUS USAC. Tribe discount is funded by Tribe (revenue to RIVR).
    cell(p, f"{col}{rr}", f"={col}{pay_row}+{col}{usac_row}+(-1)*{col}{line_rows['Less: Tribe-funded discount']}", "calc", num=USD)
gross_row = rr
rr += 1
cell(p, f"B{rr}", "Less: variable + admin cost", "grey", size=9)
for i in range(6):
    col = chr(ord('C') + i)
    cell(p, f"{col}{rr}", "=-(VAR_COST+ADMIN_COST)", "calc", num=USD)
cost_row = rr
rr += 1
cell(p, f"B{rr}", "= CONTRIBUTION MARGIN / sub / mo", "good", bold=True, size=9)
for i in range(6):
    col = chr(ord('C') + i)
    cell(p, f"{col}{rr}", f"={col}{gross_row}+{col}{cost_row}", "good", num=USD, bold=True)
rr += 2
cell(p, f"B{rr}", ("Notes: (3) applies ONLY where the principal residence is confirmed on qualifying "
    "Tribal lands. (6) shows the Senior 100/100 target under Alternative D (Lifeline first, then "
    "RIVR/Tribe top-up to reach the $10 target). Tribe-funded discount is treated as revenue to "
    "RIVR under a settlement, kept in a separate GL category. Taxes shown as TBD pending tax-advisor review."),
    "grey", wrap=True, size=8)
p.merge_cells(f"B{rr}:H{rr+2}")

# =====================================================================
# SENIOR PLAN ALTERNATIVES  A/B/C/D
# =====================================================================
alt = wb.create_sheet("Senior Alternatives")
alt.sheet_view.showGridLines = False
widths(alt, {"A": 3, "B": 40, "C": 16, "D": 16, "E": 16, "F": 16, "G": 40})
title(alt, "B2", "Senior 100/100 Plan — Alternatives A/B/C/D", 14)
subtitle(alt, "B3", "Per-subscriber monthly economics under each design. Recommend Alternative D (see Exec Plan).")
header_row(alt, 5, ["Metric", "Alt A: Universal $10", "Alt B: $10 net after Std LL",
    "Alt C: $10 net after Tribal", "Alt D: Blended", "Comment"], start_col=2)
alt.row_dimensions[5].height = 40
altrows = [
    ("Retail (list) rate set", ["=RETAIL_SENIOR", "=TARGET_PAY+LL_STD", "=TARGET_PAY+LL_TRIBAL_TOTAL", "=RETAIL_SENIOR",
        "List stays at retail; subsidies layer to reach target"]),
    ("Customer pays — has Std Lifeline", ["=TARGET_PAY", "=TARGET_PAY", "=MAX(0,ALT_C_RATE_MINUS)", "=TARGET_PAY",
        "Alt C leaves std-LL seniors ABOVE $10 unless topped up"]),
    ("Customer pays — has Enhanced Tribal", ["=TARGET_PAY", "=MAX(0,TARGET_PAY+LL_STD-LL_TRIBAL_TOTAL)", "=TARGET_PAY", "=TARGET_PAY",
        "Alt B risks OVER-recovery for tribal (pays < $10 / negative)"]),
    ("Customer pays — NO Lifeline", ["=TARGET_PAY", "=TARGET_PAY+LL_STD", "=TARGET_PAY+LL_TRIBAL_TOTAL", "=TARGET_PAY",
        "Alt A & D shield non-LL seniors; B & C do not"]),
    ("RIVR-funded subsidy — has Std LL", ["=RETAIL_SENIOR-LL_STD-TARGET_PAY", 0, 0, "=MAX(0,RETAIL_SENIOR-LL_STD-TARGET_PAY-TRIBE_DISC)",
        "Company exposure per subsidized sub"]),
    ("RIVR-funded subsidy — NO Lifeline", ["=RETAIL_SENIOR-TARGET_PAY", 0, 0, "=RETAIL_SENIOR-TARGET_PAY-TRIBE_DISC",
        "Largest company exposure (no USAC offset)"]),
    ("Compliance risk", ["Low-Med", "Med (over-recovery on tribal)", "High (misapplies tribal)", "Low",
        "Alt C mis-signals tribal eligibility"]),
]
rr = 6
for label, vals in altrows:
    cell(alt, f"B{rr}", label, "grey", bold=True, size=9)
    for i, v in enumerate(vals[:4]):
        col = chr(ord('C') + i)
        is_num = isinstance(v, (int, float)) or (isinstance(v, str) and v.startswith("="))
        cell(alt, f"{col}{rr}", v, "calc", num=USD if is_num else None, size=9,
             align=None if is_num else "center")
    cell(alt, f"G{rr}", vals[4], "grey", wrap=True, size=8)
    alt.row_dimensions[rr].height = 26
    rr += 1
# helper named cell for Alt C std-LL customer pays (retail set for tribal, std-LL sub only gets 9.25 off)
wb.defined_names.add(__import__("openpyxl").workbook.defined_name.DefinedName(
    "ALT_C_RATE_MINUS", attr_text="'Senior Alternatives'!$H$20"))
alt["H20"] = "=(TARGET_PAY+LL_TRIBAL_TOTAL)-LL_STD"
alt["H20"].number_format = USD
alt["H19"] = "helper:"
rr += 1
cell(alt, f"B{rr}", ("Alt A = universal $10 retail; RIVR absorbs the gap for non-Lifeline seniors and "
    "applies Lifeline only where permissible. Alt B sets retail so the bill nets to $10 after the "
    "$9.25 standard credit — but a tribal-qualified sub would net BELOW $10 (over-recovery risk). "
    "Alt C sets retail so the bill nets to $10 after the $34.25 tribal credit — but this only works "
    "for the (currently zero) tribal-lands population and leaves standard-LL seniors above $10. "
    "Alt D applies Lifeline first, then a defined RIVR/Tribe top-up so EVERY approved participant "
    "reaches the $10 target — recommended for compliance simplicity and NISC administrability."),
    "grey", wrap=True, size=8)
alt.merge_cells(f"B{rr}:G{rr+3}")

# =====================================================================
# SUBSCRIBER MODEL (12-month, 3 scenarios)
# =====================================================================
s = wb.create_sheet("Subscriber Model")
s.sheet_view.showGridLines = False
widths(s, {"A": 3, "B": 34})
for i in range(12):
    s.column_dimensions[chr(ord('C')+i)].width = 9
title(s, "B2", "Subscriber Build — 12 months (Expected scenario)", 13)
subtitle(s, "B3", "Scenario multipliers: Conservative 0.6x / Expected 1.0x / Aggressive 1.5x applied to enrollments.")
header_row(s, 5, ["Metric"] + [f"M{i+1}" for i in range(12)], start_col=2)
# scenario multiplier input
cell(s, "B6", "Scenario multiplier (0.6/1.0/1.5)", "input", num='0.0')
s["C6"] = 1.0
s["C6"].fill = PatternFill("solid", fgColor=YELLOW)
wb.defined_names.add(__import__("openpyxl").workbook.defined_name.DefinedName(
    "SCEN_MULT", attr_text="Subscriber Model!$C$6"))
# rows: beginning subs, gross enroll, churn, ending subs (all three cohorts combined for simplicity)
cell(s, "B8", "Beginning active subs", "grey", bold=True, size=9)
cell(s, "B9", "Gross new enrollments", "grey", size=9)
cell(s, "B10", "De-enrollments (churn)", "grey", size=9)
cell(s, "B11", "Ending active subs", "grey", bold=True, size=9)
for i in range(12):
    col = chr(ord('C')+i)
    prev = chr(ord('C')+i-1)
    # beginning
    if i == 0:
        cell(s, f"{col}8", 0, "calc", num=NUM)
    else:
        cell(s, f"{col}8", f"={prev}11", "calc", num=NUM)
    cell(s, f"{col}9", "=ROUND(ENROLL_MO*SCEN_MULT,0)", "calc", num=NUM)
    cell(s, f"{col}10", f"=-ROUND({col}8*CHURN,0)", "calc", num=NUM)
    cell(s, f"{col}11", f"={col}8+{col}9+{col}10", "calc", num=NUM, bold=True)
cell(s, "B13", ("Cohort split (of ending subs) — apply steady-state mix from Assumptions once ramped. "
    "Enhanced-Tribal cohort held at 0 until qualifying Tribal lands confirmed."), "grey", wrap=True, size=8)
s.merge_cells("B13:N13")

# =====================================================================
# P&L 12-MONTH
# =====================================================================
pl = wb.create_sheet("P&L 12mo")
pl.sheet_view.showGridLines = False
widths(pl, {"A": 3, "B": 34})
for i in range(12):
    pl.column_dimensions[chr(ord('C')+i)].width = 10
title(pl, "B2", "Contribution P&L — 12 months (Expected)", 13)
subtitle(pl, "B3", "Uses ending subs from Subscriber Model x per-sub economics. USAC cash lagged by USAC_LAG.")
header_row(pl, 5, ["Line ($/month)"] + [f"M{i+1}" for i in range(12)], start_col=2)
labels = [
    ("Active subs (end)", "='Subscriber Model'!{c}11"),
    ("Customer payments", "={c}6*TARGET_PAY"),
    ("USAC reimbursement (accrued)", "={c}6*((N_STD+N_NOLL_ZERO)/1)"),  # placeholder; refined below
]
# Simpler explicit rows:
pl_rows = [
    ("Active subs (end)",            lambda c,p: f"='Subscriber Model'!{c}11"),
    ("Customer payments ($)",         lambda c,p: f"={c}7*TARGET_PAY"),
    ("USAC reimb — accrued ($)",      lambda c,p: f"=({c}7)*LL_STD"),
    ("USAC reimb — CASH (lagged) ($)",lambda c,p: (f"=0" if p is None else f"={p}9")),
    ("RIVR-funded subsidy ($)",       lambda c,p: f"=-{c}7*RIVR_DISC"),
    ("Tribe settlement ($)",          lambda c,p: f"={c}7*TRIBE_DISC"),
    ("Variable+admin cost ($)",       lambda c,p: f"=-{c}7*(VAR_COST+ADMIN_COST)"),
    ("Acquisition cost ($)",          lambda c,p: f"=-'Subscriber Model'!{c}9*CAC"),
    ("Bad debt ($)",                  lambda c,p: f"=-{c}7*TARGET_PAY*BADDEBT"),
]
# put active subs at row 7 for reference
rr = 6
row_of = {}
for label, fn in pl_rows:
    cell(pl, f"B{rr}", label, "grey", bold=("CONTRIB" in label), size=9)
    for i in range(12):
        col = chr(ord('C')+i)
        prev = chr(ord('C')+i-1) if i>0 else None
        cell(pl, f"{col}{rr}", fn(col, prev), "calc", num=NUM if "subs" in label else USD0)
    row_of[label] = rr
    rr += 1
# contribution margin (accrual)
cell(pl, f"B{rr}", "= CONTRIBUTION MARGIN (accrual $)", "good", bold=True, size=9)
comp = ["Customer payments ($)","USAC reimb — accrued ($)","RIVR-funded subsidy ($)","Tribe settlement ($)",
        "Variable+admin cost ($)","Acquisition cost ($)","Bad debt ($)"]
for i in range(12):
    col = chr(ord('C')+i)
    cell(pl, f"{col}{rr}", "="+"+".join(f"{col}{row_of[l]}" for l in comp), "good", num=USD0, bold=True)
rr += 2
cell(pl, f"B{rr}", "Note: 'active subs' here uses the blended ending count. For mixed cohorts, extend the "
    "model per cohort (std-LL, tribal, no-LL). USAC cash column lags accrual by 1 month (USAC_LAG).",
    "grey", wrap=True, size=8)
pl.merge_cells(f"B{rr}:N{rr}")

# =====================================================================
# BREAK-EVEN
# =====================================================================
be = wb.create_sheet("Break-even")
be.sheet_view.showGridLines = False
widths(be, {"A": 3, "B": 46, "C": 16, "D": 60})
title(be, "B2", "Break-even & Sustainability", 14)
header_row(be, 5, ["Metric", "Value", "Note"], start_col=2)
be_rows = [
    ("Contribution margin / std-LL senior / mo", "='Pricing Matrix'!H18", "From Pricing Matrix, scenario (6)"),
    ("Contribution margin / no-LL senior / mo", "=TARGET_PAY-VAR_COST-ADMIN_COST-(RETAIL_SENIOR-LL_STD-TARGET_PAY)", "Company funds full gap; often negative"),
    ("Monthly RIVR subsidy — no-LL cohort", "=N_NOLL*(RETAIL_SENIOR-TARGET_PAY-TRIBE_DISC)", "Alt D company exposure, no-LL seniors"),
    ("Monthly RIVR subsidy — std-LL cohort", "=N_STD*MAX(0,RETAIL_SENIOR-LL_STD-TARGET_PAY-TRIBE_DISC)", "Alt D company exposure, std-LL seniors"),
    ("Total monthly company subsidy", "=B10+B11", "Sum of company-funded exposure"),
    ("Annual company subsidy", "=C12*12", "For budgeting"),
    ("USAC monthly reimbursement (all LL subs)", "=N_STD*LL_STD+N_TRIBAL*LL_TRIBAL_TOTAL", "Federal support inflow"),
]
rr = 6
for label, formula, note in be_rows:
    cell(be, f"B{rr}", label, "grey", bold=True, size=9)
    cell(be, f"C{rr}", formula, "calc", num=USD0)
    cell(be, f"D{rr}", note, "grey", wrap=True, size=8)
    rr += 1
cell(be, f"B{rr+1}", ("Sustainability test: the program is self-sustaining when contribution margin across the "
    "Lifeline-supported cohorts covers the company-funded subsidy to the non-Lifeline cohort plus fixed "
    "program overhead. Maximizing National Verifier approval rate (moving seniors from the no-LL cohort to "
    "the std-LL cohort) is the single biggest lever."), "grey", wrap=True, size=9)
be.merge_cells(f"B{rr+1}:D{rr+3}")

# =====================================================================
# 36-MONTH SUMMARY
# =====================================================================
y3 = wb.create_sheet("36mo Scenarios")
y3.sheet_view.showGridLines = False
widths(y3, {"A": 3, "B": 40, "C": 16, "D": 16, "E": 16})
title(y3, "B2", "36-Month Scenario Summary", 14)
subtitle(y3, "B3", "Steady-state annualized view. Adjust volumes in Assumptions; multiplier column shows sensitivity.")
header_row(y3, 5, ["Metric (annual, steady-state)", "Conservative 0.6x", "Expected 1.0x", "Aggressive 1.5x"], start_col=2)
y3_rows = [
    ("Total Lifeline subs", "=ROUND((N_STD+N_TRIBAL)*{m},0)", NUM),
    ("USAC reimbursement / yr", "=(N_STD*LL_STD+N_TRIBAL*LL_TRIBAL_TOTAL)*12*{m}", USD0),
    ("Customer payments / yr", "=(N_STD+N_TRIBAL+N_NOLL)*TARGET_PAY*12*{m}", USD0),
    ("Company subsidy / yr", "=(N_NOLL*(RETAIL_SENIOR-TARGET_PAY)+N_STD*MAX(0,RETAIL_SENIOR-LL_STD-TARGET_PAY))*12*{m}", USD0),
    ("Variable+admin cost / yr", "=(N_STD+N_TRIBAL+N_NOLL)*(VAR_COST+ADMIN_COST)*12*{m}", USD0),
    ("Contribution margin / yr", "=C7+C8-C9-C10", USD0),
]
mults = {"C": 0.6, "D": 1.0, "E": 1.5}
rr = 6
for label, formula, num in y3_rows:
    cell(y3, f"B{rr}", label, "grey", bold=True, size=9)
    for col, m in mults.items():
        if "C7+C8" in formula:  # contribution needs col-specific refs
            f = formula.replace("C7", f"{col}7").replace("C8", f"{col}8").replace("C9", f"{col}9").replace("C10", f"{col}10")
        else:
            f = formula.replace("{m}", str(m))
        cell(y3, f"{col}{rr}", f, "calc", num=num)
    rr += 1
cell(y3, f"B{rr+1}", "Contribution margin here = customer payments + USAC − company subsidy − variable/admin. "
    "Sign depends heavily on the (placeholder) retail rate and cost inputs; replace before relying on it.",
    "grey", wrap=True, size=8)
y3.merge_cells(f"B{rr+1}:E{rr+2}")

# add a benign named cell used by P&L formula
wb.defined_names.add(__import__("openpyxl").workbook.defined_name.DefinedName(
    "N_NOLL_ZERO", attr_text="Assumptions!$C$6"))

out = "/home/user/claude-skills/deliverables/RIVR-Tech-Lifeline-Lumbee/06_Lifeline_Financial_Model.xlsx"
wb.save(out)
print("saved", out)
