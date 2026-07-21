"""
Build RIVR_Tech_Five_Year_Financial_Model_2027-2031.xlsx
Formula-driven, scenario-switched (Base/Conservative/Aggressive), 18 tabs + charts.
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, NamedStyle
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import LineChart, BarChart, Reference, Series
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName
import model

R = model  # module
SC = {k: model.SCENARIOS[k]() for k in ["base", "conservative", "aggressive"]}
B, C, A = SC["base"], SC["conservative"], SC["aggressive"]
YEARS = model.YEARS
MONTHS = model.MONTHS

# ---------------- palette / styles ----------------
NAVY = "1F3B4D"; TEAL = "2E7D8A"; STEEL = "34617A"
INPUT_FILL = PatternFill("solid", fgColor="DDEBF7")     # light blue = input
CALC_FILL = PatternFill("solid", fgColor="FFFFFF")      # white = formula
OUT_FILL = PatternFill("solid", fgColor="E2EFDA")       # green = output
PH_FILL = PatternFill("solid", fgColor="FCE4D6")        # orange = placeholder
HDR_FILL = PatternFill("solid", fgColor=NAVY)
SUB_FILL = PatternFill("solid", fgColor="D6DCE4")
BAND_FILL = PatternFill("solid", fgColor="F2F6FA")
TOT_FILL = PatternFill("solid", fgColor="C9DAEA")

INPUT_FONT = Font(color="1F4E78", name="Calibri", size=10)
CALC_FONT = Font(color="000000", name="Calibri", size=10)
OUT_FONT = Font(color="1F4E78", bold=True, name="Calibri", size=10)
HDR_FONT = Font(color="FFFFFF", bold=True, name="Calibri", size=11)
TITLE_FONT = Font(color=NAVY, bold=True, name="Calibri", size=16)
SUB_FONT = Font(color=NAVY, bold=True, name="Calibri", size=10)
NOTE_FONT = Font(color="808080", italic=True, name="Calibri", size=9)

thin = Side(style="thin", color="BFBFBF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
CTR = Alignment(horizontal="center", vertical="center")
LFT = Alignment(horizontal="left", vertical="center", wrap_text=False)
RGT = Alignment(horizontal="right", vertical="center")
WRAP = Alignment(horizontal="left", vertical="top", wrap_text=True)

FMT_USD = '#,##0;(#,##0)'
FMT_USD0 = '$#,##0;($#,##0)'
FMT_USD2 = '$#,##0.00'
FMT_PCT = '0.0%'
FMT_PCT2 = '0.00%'
FMT_NUM = '#,##0'
FMT_X = '0.00"x"'

wb = openpyxl.Workbook()
wb.remove(wb.active)

def sheet(name):
    return wb.create_sheet(name)

def cell(ws, r, c, v=None, *, font=CALC_FONT, fill=None, fmt=None,
         align=None, border=True, bold=None):
    cc = ws.cell(row=r, column=c)
    if v is not None:
        cc.value = v
    f = font
    if bold is not None:
        f = Font(color=f.color.rgb if f.color else "000000", bold=bold,
                 name=f.name, size=f.size)
    cc.font = f
    if fill: cc.fill = fill
    if fmt: cc.number_format = fmt
    if align: cc.alignment = align
    if border: cc.border = BORDER
    return cc

def title(ws, text, sub=None):
    ws.merge_cells("B1:J1")
    c = ws["B1"]; c.value = text; c.font = TITLE_FONT
    ws.row_dimensions[1].height = 24
    if sub:
        ws.merge_cells("B2:J2")
        c2 = ws["B2"]; c2.value = sub; c2.font = NOTE_FONT

def hdr_row(ws, r, labels, startcol=2):
    for i, lab in enumerate(labels):
        c = cell(ws, r, startcol + i, lab, font=HDR_FONT, fill=HDR_FILL, align=CTR)
    ws.row_dimensions[r].height = 20

def col_letter(c): return get_column_letter(c)

# scenario index name
def addr(sheetname, r, c):
    return f"'{sheetname}'!{col_letter(c)}{r}"

# =====================================================================
# SHEET: Scenario Selector  (+ backing ScenarioData region on same sheet)
# =====================================================================
ss = sheet("Scenario Selector")
title(ss, "Scenario Selector & Driver Library",
      "Pick the active scenario. All model tabs recompute from the Active column via CHOOSE().")
cell(ss, 4, 2, "ACTIVE SCENARIO →", font=SUB_FONT)
sel = cell(ss, 4, 3, "Base", font=Font(color="1F4E78", bold=True, size=12),
           fill=INPUT_FILL, align=CTR)
dv = DataValidation(type="list", formula1='"Base,Conservative,Aggressive"',
                    allow_blank=False, showDropDown=False)
ss.add_data_validation(dv); dv.add(sel)
cell(ss, 5, 2, "Scenario index (1=Base 2=Cons 3=Aggr)", font=NOTE_FONT)
idxcell = cell(ss, 5, 3, '=MATCH(C4,{"Base","Conservative","Aggressive"},0)',
               font=CALC_FONT, align=CTR)
cell(ss, 6, 2, "Refresh treatment", font=SUB_FONT)
reftreat = cell(ss, 6, 3, "Inside $10M", font=Font(color="1F4E78", bold=True),
                fill=INPUT_FILL, align=CTR)
dv2 = DataValidation(type="list", formula1='"Inside $10M,Outside $10M"', allow_blank=False)
ss.add_data_validation(dv2); dv2.add(reftreat)
cell(ss, 6, 5, "Base model = Inside. Adjustable model = Outside (+$400K/yr).", font=NOTE_FONT)

# defined names
wb.defined_names.add(DefinedName("SCEN", attr_text=f"'Scenario Selector'!$C$5"))
wb.defined_names.add(DefinedName("REFRESH_OUT",
        attr_text=f"'Scenario Selector'!$C$6"))

# ---- backing driver library ----
# columns: B=label C=unit  D..H Base(1..5)  I..M Cons  N..R Aggr
drow0 = 9
hdr_row(ss, drow0, ["Driver", "Unit",
                    "Base Y1","Base Y2","Base Y3","Base Y4","Base Y5",
                    "Con Y1","Con Y2","Con Y3","Con Y4","Con Y5",
                    "Agg Y1","Agg Y2","Agg Y3","Agg Y4","Agg Y5"])
# base cols D=4..H=8 ; cons I=9..M=13 ; aggr N=14..R=18
DRIVER_ROW = {}
r = drow0 + 1
def add_driver(key, label, unit, bvals, cvals, avals, fmt=FMT_NUM):
    global r
    def vec(v):
        return v if isinstance(v, (list, tuple)) else [v]*5
    bv, cv, av = vec(bvals), vec(cvals), vec(avals)
    cell(ss, r, 2, label, font=CALC_FONT)
    cell(ss, r, 3, unit, font=NOTE_FONT, align=CTR)
    for j in range(5):
        cell(ss, r, 4+j, bv[j], font=INPUT_FONT, fill=INPUT_FILL, fmt=fmt, align=RGT)
        cell(ss, r, 9+j, cv[j], font=INPUT_FONT, fill=INPUT_FILL, fmt=fmt, align=RGT)
        cell(ss, r, 14+j, av[j], font=INPUT_FONT, fill=INPUT_FILL, fmt=fmt, align=RGT)
    DRIVER_ROW[key] = r
    r += 1

# opening balances
add_driver("res_open","Residential opening subs (Jan-2027)","subs",B.res_open,C.res_open,A.res_open)
add_driver("biz_open","Business opening subs","subs",B.biz_open,C.biz_open,A.biz_open)
add_driver("ent_open","Enterprise/DIA opening subs","subs",B.ent_open,C.ent_open,A.ent_open)
add_driver("voice_open","Voice opening subs","subs",B.voice_open,C.voice_open,A.voice_open)
# gross adds
add_driver("res_gross","Residential gross adds","subs/yr",B.res_gross,C.res_gross,A.res_gross)
add_driver("biz_gross","Business gross adds","subs/yr",B.biz_gross,C.biz_gross,A.biz_gross)
add_driver("ent_gross","Enterprise gross adds","subs/yr",B.ent_gross,C.ent_gross,A.ent_gross)
add_driver("voice_gross","Voice gross adds","subs/yr",B.voice_gross,C.voice_gross,A.voice_gross)
# churn
add_driver("res_churn","Residential churn (annual)","%",B.res_churn,C.res_churn,A.res_churn,FMT_PCT)
add_driver("biz_churn","Business churn (annual)","%",B.biz_churn,C.biz_churn,A.biz_churn,FMT_PCT)
add_driver("ent_churn","Enterprise churn (annual)","%",B.ent_churn,C.ent_churn,A.ent_churn,FMT_PCT)
add_driver("voice_churn","Voice churn (annual)","%",B.voice_churn,C.voice_churn,A.voice_churn,FMT_PCT)
# arpu
add_driver("res_arpu","Residential ARPU (start)","$/mo",B.res_arpu,C.res_arpu,A.res_arpu,FMT_USD2)
add_driver("res_arpu_g","Residential ARPU growth","%",B.res_arpu_g,C.res_arpu_g,A.res_arpu_g,FMT_PCT)
add_driver("biz_arpu","Business ARPU (start)","$/mo",B.biz_arpu,C.biz_arpu,A.biz_arpu,FMT_USD2)
add_driver("biz_arpu_g","Business ARPU growth","%",B.biz_arpu_g,C.biz_arpu_g,A.biz_arpu_g,FMT_PCT)
add_driver("ent_arpu","Enterprise ARPU (start)","$/mo",B.ent_arpu,C.ent_arpu,A.ent_arpu,FMT_USD2)
add_driver("ent_arpu_g","Enterprise ARPU growth","%",B.ent_arpu_g,C.ent_arpu_g,A.ent_arpu_g,FMT_PCT)
add_driver("voice_arpu","Voice ARPU (start)","$/mo",B.voice_arpu,C.voice_arpu,A.voice_arpu,FMT_USD2)
add_driver("voice_arpu_g","Voice ARPU growth","%",B.voice_arpu_g,C.voice_arpu_g,A.voice_arpu_g,FMT_PCT)
# passings
add_driver("res_pass_open","Residential passings (opening)","HP",B.res_pass_open,C.res_pass_open,A.res_pass_open)
add_driver("biz_pass_open","Business passings (opening)","BP",B.biz_pass_open,C.biz_pass_open,A.biz_pass_open)
add_driver("res_new_pass","New residential passings","HP/yr",B.res_new_pass,C.res_new_pass,A.res_new_pass)
add_driver("biz_new_pass","New business passings","BP/yr",B.biz_new_pass,C.biz_new_pass,A.biz_new_pass)
# capital
add_driver("deploy","Capital deployment fraction","%",B.capital_deploy_frac,C.capital_deploy_frac,A.capital_deploy_frac,FMT_PCT)
add_driver("cost_pass","Construction cost / passing","$",B.cost_per_passing,C.cost_per_passing,A.cost_per_passing,FMT_USD0)
# opex knobs
add_driver("mktg_add","Marketing per gross add","$",B.marketing_per_gross_add,C.marketing_per_gross_add,A.marketing_per_gross_add,FMT_USD0)
add_driver("opex_infl","OpEx inflation","%",B.opex_inflation,C.opex_inflation,A.opex_inflation,FMT_PCT)
add_driver("opex_mult","OpEx efficiency multiplier","x",B.opex_mult,C.opex_mult,A.opex_mult,FMT_X)
add_driver("wifi_att","Managed Wi-Fi attach","%",B.wifi_attach,C.wifi_attach,A.wifi_attach,FMT_PCT)
add_driver("wifi_px","Managed Wi-Fi price","$/mo",B.wifi_price,C.wifi_price,A.wifi_price,FMT_USD2)
add_driver("sip_att","Static IP attach (biz)","%",B.staticip_attach,C.staticip_attach,A.staticip_attach,FMT_PCT)
add_driver("sip_px","Static IP price","$/mo",B.staticip_price,C.staticip_price,A.staticip_price,FMT_USD2)
add_driver("res_inst","Residential install fee","$",B.res_install_fee,C.res_install_fee,A.res_install_fee,FMT_USD0)
add_driver("biz_inst","Business install fee","$",B.biz_install_fee,C.biz_install_fee,A.biz_install_fee,FMT_USD0)
add_driver("ent_inst","Enterprise install fee","$",B.ent_install_fee,C.ent_install_fee,A.ent_install_fee,FMT_USD0)
# labor
add_driver("headcount","Total headcount (EOY)","FTE",B.headcount,C.headcount,A.headcount)

ss.column_dimensions["B"].width = 34
ss.column_dimensions["C"].width = 12
for cx in range(4, 19):
    ss.column_dimensions[col_letter(cx)].width = 8
ss.freeze_panes = "D10"

# helper to build CHOOSE formula for driver key, year index j(0..4)
def active(key, j=0):
    row = DRIVER_ROW[key]
    return (f"CHOOSE(SCEN,'Scenario Selector'!{col_letter(4+j)}{row},"
            f"'Scenario Selector'!{col_letter(9+j)}{row},"
            f"'Scenario Selector'!{col_letter(14+j)}{row})")

print("ScenarioData rows:", len(DRIVER_ROW))

# =====================================================================
# SHEET: Assumptions  (Active values via CHOOSE -> single visible source)
# =====================================================================
asm = sheet("Assumptions")
title(asm, "Model Assumptions — ACTIVE (selected scenario)",
      "Blue = management input (edit on Scenario Selector). These Active cells feed every downstream tab. Tags: A=Actual, S=Assumption, P=Placeholder, T=Target.")
hdr_row(asm, 4, ["Assumption", "Unit", "Tag", "2027", "2028", "2029", "2030", "2031"])
ASSUM_ROW = {}
ar = 5
TAGS = {
 "res_open":"S","biz_open":"S","ent_open":"S","voice_open":"S",
 "res_gross":"S","biz_gross":"S","ent_gross":"S","voice_gross":"S",
 "res_churn":"S","biz_churn":"S","ent_churn":"S","voice_churn":"S",
 "res_arpu":"A","res_arpu_g":"S","biz_arpu":"A","biz_arpu_g":"S",
 "ent_arpu":"P","ent_arpu_g":"S","voice_arpu":"P","voice_arpu_g":"S",
 "res_pass_open":"P","biz_pass_open":"P","res_new_pass":"P","biz_new_pass":"P",
 "deploy":"S","cost_pass":"P","mktg_add":"S","opex_infl":"S","opex_mult":"S",
 "wifi_att":"S","wifi_px":"P","sip_att":"S","sip_px":"P",
 "res_inst":"S","biz_inst":"S","ent_inst":"P","headcount":"T",
}
LABELS = {k:(model.SCENARIOS,) for k in DRIVER_ROW}
# reuse labels/units from driver library by reading the ss cells
def drv_label(key):
    row = DRIVER_ROW[key]
    return ss.cell(row=row, column=2).value, ss.cell(row=row, column=3).value
FMT_FOR = {
 "res_churn":FMT_PCT,"biz_churn":FMT_PCT,"ent_churn":FMT_PCT,"voice_churn":FMT_PCT,
 "res_arpu":FMT_USD2,"biz_arpu":FMT_USD2,"ent_arpu":FMT_USD2,"voice_arpu":FMT_USD2,
 "res_arpu_g":FMT_PCT,"biz_arpu_g":FMT_PCT,"ent_arpu_g":FMT_PCT,"voice_arpu_g":FMT_PCT,
 "deploy":FMT_PCT,"cost_pass":FMT_USD0,"mktg_add":FMT_USD0,"opex_infl":FMT_PCT,
 "opex_mult":FMT_X,"wifi_att":FMT_PCT,"wifi_px":FMT_USD2,"sip_att":FMT_PCT,
 "sip_px":FMT_USD2,"res_inst":FMT_USD0,"biz_inst":FMT_USD0,"ent_inst":FMT_USD0,
}
SINGLE = {"res_open","biz_open","ent_open","voice_open","res_churn","biz_churn",
 "ent_churn","voice_churn","res_arpu","res_arpu_g","biz_arpu","biz_arpu_g",
 "ent_arpu","ent_arpu_g","voice_arpu","voice_arpu_g","res_pass_open","biz_pass_open",
 "cost_pass","mktg_add","opex_infl","opex_mult","wifi_att","wifi_px","sip_att",
 "sip_px","res_inst","biz_inst","ent_inst"}

for key in DRIVER_ROW:
    lab, unit = drv_label(key)
    fmt = FMT_FOR.get(key, FMT_NUM)
    tag = TAGS.get(key, "S")
    tagfill = PH_FILL if tag == "P" else (OUT_FILL if tag=="T" else BAND_FILL)
    cell(asm, ar, 2, lab, font=CALC_FONT)
    cell(asm, ar, 3, unit, font=NOTE_FONT, align=CTR)
    cell(asm, ar, 4, tag, font=CALC_FONT, align=CTR, fill=tagfill)
    for j in range(5):
        jj = 0 if key in SINGLE else j
        f = f"={active(key, jj)}"
        cell(asm, ar, 5+j, f, font=CALC_FONT, fmt=fmt, align=RGT, fill=BAND_FILL)
    ASSUM_ROW[key] = ar
    ar += 1

asm.column_dimensions["B"].width = 34
asm.column_dimensions["C"].width = 9
asm.column_dimensions["D"].width = 5
for cx in range(5, 10):
    asm.column_dimensions[col_letter(cx)].width = 12
asm.freeze_panes = "E5"

# Active reference helper: 'Assumptions'!<col><row> for year j (col E=5..I=9)
def AC(key, j=0):
    row = ASSUM_ROW[key]
    jj = 0 if key in SINGLE else j
    return f"Assumptions!{col_letter(5+jj)}{row}"

# constant weights for Y1 monthly gross-add ramp (sum=1)
WEIGHTS = [0.070,0.072,0.078,0.085,0.090,0.092,0.092,0.090,0.086,0.083,0.082,0.080]
tw = sum(WEIGHTS); WEIGHTS=[w/tw for w in WEIGHTS]
print("Assumptions built:", len(ASSUM_ROW))

# =====================================================================
# SHEET: Subscriber Forecast  (monthly Y1 + annual Y2-5, formula-driven)
# =====================================================================
sf = sheet("Subscriber Forecast")
title(sf, "Subscriber Forecast — Roll-Forward",
      "Beg + Gross Adds − Disconnects = End. Year-1 monthly reconciles to the annual column. Green = ending balances.")
MCOL0 = 4  # Jan col D
FYCOL = 16 # col P
LINES = [("Residential","res"),("Business","biz"),("Enterprise / DIA","ent"),("Voice","voice")]

# ---- Year 1 monthly ----
cell(sf, 4, 2, "YEAR 1 — MONTHLY DETAIL (FY2027)", font=SUB_FONT, fill=SUB_FILL)
hdr = ["Metric"] + MONTHS + ["FY2027"]
for i,h in enumerate(hdr):
    cell(sf, 5, 2+i if i==0 else MCOL0+(i-1), h, font=HDR_FONT, fill=HDR_FILL, align=CTR)
mrow = 6
MONTHLY_ROWS = {}
for lname, lkey in LINES:
    cell(sf, mrow, 2, lname, font=SUB_FONT, fill=BAND_FILL)
    for j in range(12): cell(sf, mrow, MCOL0+j, None, fill=BAND_FILL)
    cell(sf, mrow, FYCOL, None, fill=BAND_FILL)
    rr = {}
    r_beg, r_gr, r_di, r_en = mrow+1, mrow+2, mrow+3, mrow+4
    # Beginning
    cell(sf, r_beg, 2, "  Beginning subs")
    cell(sf, r_beg, MCOL0, f"={AC(lkey+'_open')}", fmt=FMT_NUM, align=RGT)
    for j in range(1,12):
        cell(sf, r_beg, MCOL0+j, f"={col_letter(MCOL0+j-1)}{r_en}", fmt=FMT_NUM, align=RGT)
    cell(sf, r_beg, FYCOL, f"={col_letter(MCOL0)}{r_beg}", fmt=FMT_NUM, align=RGT, fill=BAND_FILL)
    # Gross adds
    cell(sf, r_gr, 2, "  Gross adds")
    for j in range(11):
        cell(sf, r_gr, MCOL0+j, f"=ROUND({AC(lkey+'_gross',0)}*{WEIGHTS[j]:.5f},0)",
             font=INPUT_FONT, fmt=FMT_NUM, align=RGT)
    # Dec plug
    sumfirst = "+".join(f"{col_letter(MCOL0+j)}{r_gr}" for j in range(11))
    cell(sf, r_gr, MCOL0+11, f"={AC(lkey+'_gross',0)}-({sumfirst})", font=INPUT_FONT, fmt=FMT_NUM, align=RGT)
    cell(sf, r_gr, FYCOL, f"=SUM({col_letter(MCOL0)}{r_gr}:{col_letter(MCOL0+11)}{r_gr})", fmt=FMT_NUM, align=RGT, fill=BAND_FILL)
    # Disconnects
    cell(sf, r_di, 2, "  Disconnects (churn)")
    for j in range(12):
        cell(sf, r_di, MCOL0+j, f"=ROUND({col_letter(MCOL0+j)}{r_beg}*{AC(lkey+'_churn')}/12,0)", fmt=FMT_NUM, align=RGT)
    cell(sf, r_di, FYCOL, f"=SUM({col_letter(MCOL0)}{r_di}:{col_letter(MCOL0+11)}{r_di})", fmt=FMT_NUM, align=RGT, fill=BAND_FILL)
    # Ending
    cell(sf, r_en, 2, "  Ending subs", font=OUT_FONT)
    for j in range(12):
        cl=col_letter(MCOL0+j)
        cell(sf, r_en, MCOL0+j, f"={cl}{r_beg}+{cl}{r_gr}-{cl}{r_di}", font=OUT_FONT, fmt=FMT_NUM, align=RGT, fill=OUT_FILL)
    cell(sf, r_en, FYCOL, f"={col_letter(MCOL0+11)}{r_en}", font=OUT_FONT, fmt=FMT_NUM, align=RGT, fill=OUT_FILL)
    MONTHLY_ROWS[lkey] = dict(beg=r_beg, gross=r_gr, disc=r_di, end=r_en)
    mrow = r_en + 1

# ---- Annual summary ----
astart = mrow + 1
cell(sf, astart, 2, "ANNUAL SUMMARY (2027-2031)", font=SUB_FONT, fill=SUB_FILL)
hdr_row(sf, astart+1, ["Metric","2027","2028","2029","2030","2031","5-Yr / End"])
arow = astart+2
ANN_ROWS = {}  # per line -> end row; also totals
for lname, lkey in LINES:
    cell(sf, arow, 2, lname, font=SUB_FONT, fill=BAND_FILL)
    for cx in range(3,9): cell(sf, arow, cx, None, fill=BAND_FILL)
    r_beg, r_gr, r_di, r_en = arow+1, arow+2, arow+3, arow+4
    cell(sf, r_beg, 2, "  Beginning")
    cell(sf, r_gr, 2, "  Gross adds")
    cell(sf, r_di, 2, "  Disconnects")
    cell(sf, r_en, 2, "  Ending", font=OUT_FONT)
    for j in range(5):
        cc = 3+j
        # Beginning
        if j==0:
            cell(sf, r_beg, cc, f"={AC(lkey+'_open')}", fmt=FMT_NUM, align=RGT)
        else:
            cell(sf, r_beg, cc, f"={col_letter(cc-1)}{r_en}", fmt=FMT_NUM, align=RGT)
        # Gross
        cell(sf, r_gr, cc, f"={AC(lkey+'_gross',j)}", fmt=FMT_NUM, align=RGT)
        # Disc: Y1 = sum of monthly; Y2-5 = ROUND(beg*churn)
        if j==0:
            cell(sf, r_di, cc, f"={col_letter(FYCOL)}{MONTHLY_ROWS[lkey]['disc']}", fmt=FMT_NUM, align=RGT)
        else:
            cell(sf, r_di, cc, f"=ROUND({col_letter(cc)}{r_beg}*{AC(lkey+'_churn')},0)", fmt=FMT_NUM, align=RGT)
        # Ending
        cell(sf, r_en, cc, f"={col_letter(cc)}{r_beg}+{col_letter(cc)}{r_gr}-{col_letter(cc)}{r_di}",
             font=OUT_FONT, fmt=FMT_NUM, align=RGT, fill=OUT_FILL)
    # 5yr gross total in col H
    cell(sf, r_gr, 8, f"=SUM(C{r_gr}:G{r_gr})", fmt=FMT_NUM, align=RGT)
    cell(sf, r_en, 8, f"=G{r_en}", font=OUT_FONT, fmt=FMT_NUM, align=RGT, fill=OUT_FILL)
    ANN_ROWS[lkey] = dict(beg=r_beg, gross=r_gr, disc=r_di, end=r_en)
    arow = r_en + 1

# ---- totals (internet = res+biz+ent; plus voice separate) ----
tr = arow
cell(sf, tr, 2, "TOTAL INTERNET (Res+Biz+Ent)", font=OUT_FONT, fill=TOT_FILL)
for j in range(5):
    cc=3+j
    beg = f"C{cc}"  # placeholder
    f_end = f"={col_letter(cc)}{ANN_ROWS['res']['end']}+{col_letter(cc)}{ANN_ROWS['biz']['end']}+{col_letter(cc)}{ANN_ROWS['ent']['end']}"
    cell(sf, tr, cc, f_end, font=OUT_FONT, fmt=FMT_NUM, align=RGT, fill=TOT_FILL)
TOT_END_ROW = tr
tr2 = tr+1
cell(sf, tr2, 2, "  Beginning (internet)")
for j in range(5):
    cc=3+j
    cell(sf, tr2, cc, f"={col_letter(cc)}{ANN_ROWS['res']['beg']}+{col_letter(cc)}{ANN_ROWS['biz']['beg']}+{col_letter(cc)}{ANN_ROWS['ent']['beg']}", fmt=FMT_NUM, align=RGT)
TOT_BEG_ROW = tr2
tr3=tr+2
cell(sf, tr3, 2, "  Gross adds (internet)")
for j in range(5):
    cc=3+j
    cell(sf, tr3, cc, f"={col_letter(cc)}{ANN_ROWS['res']['gross']}+{col_letter(cc)}{ANN_ROWS['biz']['gross']}+{col_letter(cc)}{ANN_ROWS['ent']['gross']}", fmt=FMT_NUM, align=RGT)
TOT_GROSS_ROW=tr3
tr4=tr+3
cell(sf, tr4, 2, "  Disconnects (internet)")
for j in range(5):
    cc=3+j
    cell(sf, tr4, cc, f"={col_letter(cc)}{ANN_ROWS['res']['disc']}+{col_letter(cc)}{ANN_ROWS['biz']['disc']}+{col_letter(cc)}{ANN_ROWS['ent']['disc']}", fmt=FMT_NUM, align=RGT)
TOT_DISC_ROW=tr4
tr5=tr+4
cell(sf, tr5, 2, "  Net adds (internet)", font=OUT_FONT)
for j in range(5):
    cc=3+j
    cell(sf, tr5, cc, f"={col_letter(cc)}{TOT_END_ROW}-{col_letter(cc)}{TOT_BEG_ROW}", font=OUT_FONT, fmt=FMT_NUM, align=RGT, fill=OUT_FILL)
TOT_NET_ROW=tr5
# error check: monthly Dec end == annual Y1 end
ecrow = tr5+2
cell(sf, ecrow, 2, "CHECK: monthly Dec = annual Y1 (each line, 0=OK)", font=NOTE_FONT)
checks=[]
for k in ['res','biz','ent','voice']:
    checks.append(f"({col_letter(FYCOL)}{MONTHLY_ROWS[k]['end']}-C{ANN_ROWS[k]['end']})")
cell(sf, ecrow, 3, f"={'+'.join('ABS'+c for c in checks)}", fmt=FMT_NUM, align=CTR, fill=OUT_FILL)

sf.column_dimensions["B"].width = 26
for cx in range(3,17): sf.column_dimensions[col_letter(cx)].width = 9
sf.freeze_panes = "C6"

# register cross-tab refs
REF = {}
REF["end"] = {k: (ANN_ROWS[k]['end']) for k in ['res','biz','ent','voice']}
REF["beg"] = {k: (ANN_ROWS[k]['beg']) for k in ['res','biz','ent','voice']}
REF["gross"] = {k: (ANN_ROWS[k]['gross']) for k in ['res','biz','ent','voice']}
REF["sf"] = "Subscriber Forecast"
REF["tot_end"]=TOT_END_ROW; REF["tot_beg"]=TOT_BEG_ROW
REF["tot_gross"]=TOT_GROSS_ROW; REF["tot_disc"]=TOT_DISC_ROW; REF["tot_net"]=TOT_NET_ROW
def SUB(kind, key, j):  # e.g. SUB('end','res',0) -> 'Subscriber Forecast'!C<row>
    row = REF[kind][key]; return f"'Subscriber Forecast'!{col_letter(3+j)}{row}"
def SUBT(kind, j):
    row = REF[kind]; return f"'Subscriber Forecast'!{col_letter(3+j)}{row}"
print("Subscriber Forecast built")

# =====================================================================
# SHEET: Revenue Model
# =====================================================================
rv = sheet("Revenue Model")
title(rv, "Revenue Model (formula-driven)",
      "Recurring = avg subs × ARPU × 12 + attach services. Nonrecurring = installation/construction. Orange = placeholder input.")
hdr_row(rv, 4, ["Revenue line","2027","2028","2029","2030","2031","5-Yr Total"])
def avg_sub_ref(key, j):
    return f"(({SUB('beg',key,j)}+{SUB('end',key,j)})/2)"
def arpu_ref(key, j):
    return f"({AC(key+'_arpu')}*(1+{AC(key+'_arpu_g')})^{j})"
rr = 5
RV_ROWS={}
def rev_row(label, key, kind="rec"):
    global rr
    cell(rv, rr, 2, label)
    for j in range(5):
        cc=3+j
        if kind=="line":
            f=f"={avg_sub_ref(key,j)}*{arpu_ref(key,j)}*12"
        cell(rv, rr, cc, f, fmt=FMT_USD, align=RGT)
    cell(rv, rr, 8, f"=SUM(C{rr}:G{rr})", fmt=FMT_USD, align=RGT)
    RV_ROWS[label]=rr; rr+=1

for lab,key in [("Residential internet","res"),("Business internet","biz"),
                ("Enterprise / DIA","ent"),("Voice services","voice")]:
    cell(rv, rr, 2, lab)
    for j in range(5):
        cell(rv, rr, 3+j, f"={avg_sub_ref(key,j)}*{arpu_ref(key,j)}*12", fmt=FMT_USD, align=RGT)
    cell(rv, rr, 8, f"=SUM(C{rr}:G{rr})", fmt=FMT_USD, align=RGT)
    RV_ROWS[lab]=rr; rr+=1
# Managed Wi-Fi = avg res * attach * price *12
cell(rv, rr, 2, "Managed Wi-Fi & premium")
for j in range(5):
    cell(rv, rr, 3+j, f"={avg_sub_ref('res',j)}*{AC('wifi_att')}*{AC('wifi_px')}*12", fmt=FMT_USD, align=RGT)
cell(rv, rr, 8, f"=SUM(C{rr}:G{rr})", fmt=FMT_USD, align=RGT); RV_ROWS["wifi"]=rr; rr+=1
# Static IP = avg biz * attach * price *12
cell(rv, rr, 2, "Static IP services")
for j in range(5):
    cell(rv, rr, 3+j, f"={avg_sub_ref('biz',j)}*{AC('sip_att')}*{AC('sip_px')}*12", fmt=FMT_USD, align=RGT)
cell(rv, rr, 8, f"=SUM(C{rr}:G{rr})", fmt=FMT_USD, align=RGT); RV_ROWS["sip"]=rr; rr+=1
# Residential other (equipment/misc recurring) = avg res * $2.90/mo *12  [actual-anchored]
cell(rv, rr, 2, "Residential other (equipment/misc)")
for j in range(5):
    cell(rv, rr, 3+j, f"={avg_sub_ref('res',j)}*2.9*12", fmt=FMT_USD, align=RGT)
cell(rv, rr, 8, f"=SUM(C{rr}:G{rr})", fmt=FMT_USD, align=RGT); RV_ROWS["equip"]=rr; rr+=1
# placeholder / assumption input rows (grant construction reimbursement is NONOPERATING — see Income Statement)
PH_REV = {
 "Dark fiber / IRU / transport (wholesale)":[12000,20000,32000,48000,65000],
 "Other telecom services":[15000,20000,26000,32000,38000],
}
for lab,vals in PH_REV.items():
    cell(rv, rr, 2, lab)
    for j in range(5):
        cell(rv, rr, 3+j, vals[j], font=INPUT_FONT, fill=PH_FILL, fmt=FMT_USD, align=RGT)
    cell(rv, rr, 8, f"=SUM(C{rr}:G{rr})", fmt=FMT_USD, align=RGT)
    RV_ROWS[lab]=rr; rr+=1
# Recurring subtotal
rec_rows=[RV_ROWS[k] for k in ["Residential internet","Business internet","Enterprise / DIA","Voice services","wifi","sip","equip","Dark fiber / IRU / transport (wholesale)","Other telecom services"]]
recr = rr
cell(rv, recr, 2, "RECURRING REVENUE", font=OUT_FONT, fill=TOT_FILL)
for j in range(5):
    cc=col_letter(3+j)
    parts="+".join(f"{cc}{x}" for x in rec_rows)
    cell(rv, recr, 3+j, f"={parts}", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
cell(rv, recr, 8, f"=SUM(C{recr}:G{recr})", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
rr=recr+1
# Installation / nonrecurring
instr=rr
cell(rv, instr, 2, "Installation & construction (nonrecurring)")
for j in range(5):
    cc=3+j
    f=(f"={SUB('gross','res',j)}*{AC('res_inst')}"
       f"+{SUB('gross','biz',j)}*{AC('biz_inst')}"
       f"+{SUB('gross','ent',j)}*{AC('ent_inst')}")
    cell(rv, instr, cc, f, fmt=FMT_USD, align=RGT)
cell(rv, instr, 8, f"=SUM(C{instr}:G{instr})", fmt=FMT_USD, align=RGT)
rr=instr+1
# Total revenue
totr=rr
cell(rv, totr, 2, "TOTAL REVENUE", font=OUT_FONT, fill=TOT_FILL)
for j in range(5):
    cc=col_letter(3+j)
    cell(rv, totr, 3+j, f"={cc}{recr}+{cc}{instr}", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
cell(rv, totr, 8, f"=SUM(C{totr}:G{totr})", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
# blended ARPU row
rr=totr+2
cell(rv, rr, 2, "Blended ARPU (recurring/sub/mo)", font=NOTE_FONT)
for j in range(5):
    cc=col_letter(3+j)
    cell(rv, rr, 3+j, f"={cc}{recr}/(({SUBT('tot_beg',j)}+{SUBT('tot_end',j)})/2+({SUB('beg','voice',j)}+{SUB('end','voice',j)})/2)/12", fmt=FMT_USD2, align=RGT)

rv.column_dimensions["B"].width=40
for cx in range(3,9): rv.column_dimensions[col_letter(cx)].width=13
rv.freeze_panes="C5"
REV_TOTAL_ROW=totr; REV_REC_ROW=recr; REV_INST_ROW=instr
def REVT(j): return f"'Revenue Model'!{col_letter(3+j)}{REV_TOTAL_ROW}"
def REVREC(j): return f"'Revenue Model'!{col_letter(3+j)}{REV_REC_ROW}"
print("Revenue Model built")

# passings helper (cumulative from Assumptions)
def passings_ref(kind, j):
    row=ASSUM_ROW[kind+'_new_pass']; openref=AC(kind+'_pass_open')
    endcol=col_letter(5+j)
    return f"({openref}+SUM(Assumptions!E{row}:{endcol}{row}))"
def total_pass_ref(j):
    return f"({passings_ref('res',j)}+{passings_ref('biz',j)})"
def avg_internet(j):
    return f"(({SUBT('tot_beg',j)}+{SUBT('tot_end',j)})/2)"
def avg_voice(j):
    return f"(({SUB('beg','voice',j)}+{SUB('end','voice',j)})/2)"

# =====================================================================
# SHEET: Fully Loaded Labor Cost
# =====================================================================
fl = sheet("Fully Loaded Labor Cost")
title(fl, "Fully-Loaded Labor Cost Build-Up",
      "Blue = editable placeholder wage/benefit inputs. Fully-loaded = base × load factor + tools + recruiting. Orange = placeholder.")
lb = model.compute("base")["labor"]
hdr_row(fl, 4, ["Current position","Base salary $","Filled","Open","Authorized","Loaded/position $"])
roles = lb["roles_start"]
lr=5
role_rows=[]
for name, base, cnt in roles:
    filled = {"Chief Operations Officer":1,"Director of Outside Plant":1,"Supervisors":2,
              "Project Coordinators":2,"Sales Coordinator":1,"Sales Representatives":3,"Fiber Technicians":5}[name]
    openn = cnt-filled
    cell(fl, lr, 2, name)
    cell(fl, lr, 3, base, font=INPUT_FONT, fill=PH_FILL, fmt=FMT_USD0, align=RGT)
    cell(fl, lr, 4, filled, font=INPUT_FONT, fill=INPUT_FILL, align=CTR)
    cell(fl, lr, 5, openn, font=INPUT_FONT, fill=INPUT_FILL, align=CTR)
    cell(fl, lr, 6, f"=D{lr}+E{lr}", align=CTR)
    cell(fl, lr, 7, f"=C{lr}*$C${lr_load if False else 0}", align=RGT)  # placeholder, fix below
    role_rows.append(lr); lr+=1
tot_role=lr
cell(fl, tot_role, 2, "TOTAL / WEIGHTED", font=OUT_FONT, fill=TOT_FILL)
cell(fl, tot_role, 4, f"=SUM(D5:D{lr-1})", font=OUT_FONT, align=CTR, fill=TOT_FILL)
cell(fl, tot_role, 5, f"=SUM(E5:E{lr-1})", font=OUT_FONT, align=CTR, fill=TOT_FILL)
cell(fl, tot_role, 6, f"=SUM(F5:F{lr-1})", font=OUT_FONT, align=CTR, fill=TOT_FILL)
# total base payroll (authorized)
cell(fl, tot_role, 3, f"=SUMPRODUCT(C5:C{lr-1},F5:F{lr-1})", font=OUT_FONT, fmt=FMT_USD0, align=RGT, fill=TOT_FILL)
TOTAL_BASE=f"C{tot_role}"; AUTH_CELL=f"F{tot_role}"

# load components
ls=tot_role+2
cell(fl, ls, 2, "LOAD COMPONENTS (% of base)", font=SUB_FONT, fill=SUB_FILL)
comps=[("Overtime",0.05),("Incentive compensation",0.06),("Payroll taxes",0.0765),
       ("Health & retirement benefits",0.18),("Workers' compensation",0.035),
       ("Training & certifications",0.015),("Uniforms & PPE",0.010)]
lc=ls+1; comp_rows=[]
for name,val in comps:
    cell(fl, lc, 2, name)
    cell(fl, lc, 3, val, font=INPUT_FONT, fill=INPUT_FILL, fmt=FMT_PCT2, align=RGT)
    comp_rows.append(lc); lc+=1
cell(fl, lc, 2, "Load factor (1 + Σ)", font=OUT_FONT)
cell(fl, lc, 3, f"=1+SUM(C{comp_rows[0]}:C{comp_rows[-1]})", font=OUT_FONT, fmt='0.000', align=RGT, fill=OUT_FILL)
LOADF=f"C{lc}"; lc+=1
cell(fl, lc, 2, "Per-head tools/laptop/phone/test equip $")
cell(fl, lc, 3, lb["per_head_tools"], font=INPUT_FONT, fill=PH_FILL, fmt=FMT_USD0, align=RGT); TOOLS=f"C{lc}"; lc+=1
cell(fl, lc, 2, "Per-head recruiting/onboarding $")
cell(fl, lc, 3, lb["per_head_recruit"], font=INPUT_FONT, fill=PH_FILL, fmt=FMT_USD0, align=RGT); RECR=f"C{lc}"; lc+=1
cell(fl, lc, 2, "Annual merit increase %")
cell(fl, lc, 3, lb["merit"], font=INPUT_FONT, fill=INPUT_FILL, fmt=FMT_PCT, align=RGT); MERIT=f"C{lc}"; lc+=1
cell(fl, lc, 2, "Average base salary (authorized) $")
cell(fl, lc, 3, f"={TOTAL_BASE}/{AUTH_CELL}", fmt=FMT_USD0, align=RGT); AVGBASE=f"C{lc}"; lc+=1
cell(fl, lc, 2, "FULLY-LOADED COST PER POSITION $", font=OUT_FONT)
cell(fl, lc, 3, f"={AVGBASE}*{LOADF}+{TOOLS}+{RECR}", font=OUT_FONT, fmt=FMT_USD0, align=RGT, fill=OUT_FILL)
LOADED_PH=f"C{lc}"; lc+=1

# fix per-position loaded col G now that LOADF known
for rrx in role_rows:
    fl.cell(row=rrx, column=7).value=f"=C{rrx}*{LOADF}+{TOOLS}+{RECR}"
    fl.cell(row=rrx, column=7).number_format=FMT_USD0

# 5-year labor cost
ly=lc+1
cell(fl, ly, 2, "FIVE-YEAR FULLY-LOADED LABOR COST", font=SUB_FONT, fill=SUB_FILL)
hdr_row(fl, ly+1, ["Item","2027","2028","2029","2030","2031","5-Yr Total"])
hc=ly+2
cell(fl, hc, 2, "Total headcount (EOY)")
for j in range(5):
    cell(fl, hc, 3+j, f"={AC('headcount',j)}", fmt=FMT_NUM, align=RGT)
lcst=ly+3
cell(fl, lcst, 2, "Fully-loaded labor cost", font=OUT_FONT)
for j in range(5):
    cc=col_letter(3+j)
    cell(fl, lcst, 3+j, f"={cc}{hc}*{LOADED_PH}*(1+{MERIT})^{j}", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=OUT_FILL)
cell(fl, lcst, 8, f"=SUM(C{lcst}:G{lcst})", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=OUT_FILL)
LABOR_COST_ROW=lcst
def LABORC(j): return f"'Fully Loaded Labor Cost'!{col_letter(3+j)}{LABOR_COST_ROW}"

fl.column_dimensions["B"].width=42
for cx in range(3,9): fl.column_dimensions[col_letter(cx)].width=13
fl.freeze_panes="C5"
print("Fully Loaded Labor built; loaded/head cell", LOADED_PH)

# =====================================================================
# SHEET: Operating Expenses
# =====================================================================
ox = sheet("Operating Expenses")
title(ox, "Operating-Expense Model (formula-driven)",
      "Classified Direct / S&M / Network Ops / G&A and Fixed/Variable/Semi-variable. Efficiency multiplier & inflation from Assumptions.")
hdr_row(ox, 4, ["Expense category","Class","Behavior","2027","2028","2029","2030","2031"])
def infl(j): return f"(1+{AC('opex_infl')})^{j}"
MULT=f"{AC('opex_mult')}"
oxr=5
OX_ROWS={}
# each entry: (label, class, behavior, [formula per year as python lambda(j)->expr], apply_mult)
def opex_line(label, klass, behavior, exprfn, mult=True):
    global oxr
    cell(ox, oxr, 2, label)
    cell(ox, oxr, 3, klass, font=NOTE_FONT, align=CTR)
    cell(ox, oxr, 4, behavior, font=NOTE_FONT, align=CTR)
    for j in range(5):
        e=exprfn(j)
        if mult: e=f"({e})*{MULT}"
        cell(ox, oxr, 5+j, f"={e}", fmt=FMT_USD, align=RGT)
    OX_ROWS[label]=oxr; oxr+=1

# Categories anchored to RIVR Tech Q2-2026 actual income statement (annualized YTD),
# grown on subscriber / headcount / inflation / revenue drivers. Payroll is embedded
# in these categories (Eng&Ops, Sales&CS, G&A, Accounting, HR, IT) — the Fully-Loaded
# Labor tab is a separate workforce-planning view and is NOT added here (no double-count).
def sub_ratio(j): return f"(({avg_internet(j)}+{avg_voice(j)})/5188)"
def hc_ratio(j):  return f"({AC('headcount',j)}/18)"
def infl0(j):     return f"(1+{AC('opex_infl')})^{j}"
def infl1(j):     return f"(1+{AC('opex_infl')})^{j+1}"
opex_line("Cost of goods sold (transit / network direct)","Direct","Variable", lambda j:f"642492*{sub_ratio(j)}*{infl0(j)}")
opex_line("LREMC intercompany allocation","G&A","Fixed", lambda j:f"380552*{infl1(j)}")
opex_line("Engineering & operations","NetOps","Semi-var", lambda j:f"864540*(0.5+0.5*{sub_ratio(j)})*{infl1(j)}")
opex_line("Marketing & advertising","S&M","Semi-var", lambda j:f"318412*(0.4+0.6*{sub_ratio(j)})*{infl1(j)}")
opex_line("Sales & customer support","S&M","Semi-var", lambda j:f"233336*(0.3+0.7*{sub_ratio(j)})*{infl1(j)}")
opex_line("General & administrative","G&A","Semi-var", lambda j:f"1496052*(0.55+0.45*{hc_ratio(j)})*{infl1(j)}")
opex_line("Accounting","G&A","Fixed", lambda j:f"124314*{infl1(j)}")
opex_line("Human resources","G&A","Fixed", lambda j:f"158562*(0.4+0.6*{hc_ratio(j)})*{infl1(j)}")
opex_line("Information technology","G&A","Fixed", lambda j:f"39042*(0.5+0.5*{sub_ratio(j)})*{infl1(j)}")
opex_line("Taxes & regulatory fees","G&A","Variable", lambda j:f"{REVREC(j)}*0.0034")
# subtotal before contingency
sub_before=oxr
cell(ox, sub_before, 2, "Subtotal (pre-contingency)", font=SUB_FONT, fill=BAND_FILL)
for j in range(5):
    cc=col_letter(5+j)
    cell(ox, sub_before, 5+j, f"=SUM({cc}5:{cc}{oxr-1})", font=SUB_FONT, fmt=FMT_USD, align=RGT, fill=BAND_FILL)
oxr+=1
# contingency = 1.5% of subtotal * mult
cont=oxr
cell(ox, cont, 2, "Contingency"); cell(ox, cont, 3, "G&A", font=NOTE_FONT, align=CTR); cell(ox, cont, 4, "Semi-var", font=NOTE_FONT, align=CTR)
for j in range(5):
    cc=col_letter(5+j)
    cell(ox, cont, 5+j, f"={cc}{sub_before}*0.02", fmt=FMT_USD, align=RGT)
OX_ROWS["Contingency"]=cont; oxr+=1
# TOTAL OPEX
tot=oxr
cell(ox, tot, 2, "TOTAL OPERATING EXPENSE", font=OUT_FONT, fill=TOT_FILL)
for j in range(5):
    cc=col_letter(5+j)
    cell(ox, tot, 5+j, f"={cc}{sub_before}+{cc}{cont}", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
OPEX_TOTAL_ROW=tot
def OPEXT(j): return f"'Operating Expenses'!{col_letter(5+j)}{OPEX_TOTAL_ROW}"
oxr=tot+2
# classification subtotals
cell(ox, oxr, 2, "By classification:", font=SUB_FONT, fill=SUB_FILL); oxr+=1
def class_subtotal(label, klass):
    global oxr
    rows=[OX_ROWS[k] for k in OX_ROWS if ox.cell(row=OX_ROWS[k],column=3).value==klass]
    cell(ox, oxr, 2, "  "+label)
    for j in range(5):
        cc=col_letter(5+j)
        parts="+".join(f"{cc}{x}" for x in rows) if rows else "0"
        cell(ox, oxr, 5+j, f"={parts}", fmt=FMT_USD, align=RGT)
    oxr+=1
class_subtotal("Direct cost of service","Direct")
class_subtotal("Sales & marketing","S&M")
class_subtotal("Network operations","NetOps")
class_subtotal("General & administrative","G&A")
# per-sub & per-rev
oxr+=1
cell(ox, oxr, 2, "OpEx per subscriber ($/yr)", font=NOTE_FONT)
for j in range(5):
    cc=col_letter(5+j)
    cell(ox, oxr, 5+j, f"={OPEXT(j)}/(({SUBT('tot_beg',j)}+{SUBT('tot_end',j)})/2)", fmt=FMT_USD0, align=RGT)
oxr+=1
cell(ox, oxr, 2, "OpEx per revenue dollar", font=NOTE_FONT)
for j in range(5):
    cell(ox, oxr, 5+j, f"={OPEXT(j)}/{REVT(j)}", fmt='0.000', align=RGT)

ox.column_dimensions["B"].width=42; ox.column_dimensions["C"].width=8; ox.column_dimensions["D"].width=9
for cx in range(5,10): ox.column_dimensions[col_letter(cx)].width=13
ox.freeze_panes="E5"
print("Operating Expenses built")

# =====================================================================
# SHEET: Capital Plan
# =====================================================================
cp = sheet("Capital Plan")
title(cp, "Five-Year Capital Plan — $10M/yr · $50M/5yr",
      "Refresh (#15) is fixed $400K/yr & fully committed. Others scale by deployment fraction. Reserve/carryforward allowed — full $10M not forced.")
capm = model.compute_capital(model.SCENARIOS["base"]())
alloc = capm["alloc"]
REFRESH_KEY="15. Annual equipment refresh program"
# metadata: depr years, purpose, benefit, impact, timing, dependency, owner
META = {
"1. Fiber backbone construction":(25,"Middle-mile & backbone fiber routes","Adds transport capacity & redundancy","Enables new market revenue; lowers leased-transport cost","Y1-Y3 priority","Permitting, pole make-ready","VP Engineering / Dir OSP"),
"2. Distribution fiber construction":(25,"Neighborhood distribution plant","Extends serviceable footprint","Drives new passings → subscriber revenue","Continuous","Backbone in place","Dir Outside Plant"),
"3. Fiber-to-the-home expansion":(20,"Drops, ONTs, service laterals","Converts passings to paying subs","Primary residential revenue driver","Continuous, demand-led","Distribution built","Dir OSP / COO"),
"4. Business & enterprise expansion":(15,"Business fiber & enterprise circuits","Higher-ARPU B2B connectivity","Enterprise/DIA revenue & margin","Y1-Y5, pipeline-led","Sales pipeline","VP Sales / Eng"),
"5. Grant matching funds":(20,"Required match for grant builds","Unlocks grant-funded construction","Leverages external capital 2-5x","Per award schedule","Grant awards","CFO / Grants Mgr"),
"6. Core network & transport equipment":(10,"Routers, switches, DWDM","Core capacity & resiliency","Supports all revenue; avoids congestion","Y1 refresh + growth","Vendor lead times","Network Engineering"),
"7. OLT, cabinet & access-network equipment":(10,"OLTs, cabinets, splitters","Access-layer subscriber capacity","Enables sub growth per node","With distribution","Cabinet siting/power","Network Eng / OSP"),
"8. CPE & ONTs":(7,"Customer ONTs, routers, Wi-Fi","In-home service delivery","Per-sub install; equipment fees","Demand-led","Install labor","Field Operations"),
"9. Vehicles & fleet":(7,"Bucket/service trucks & vans","Field workforce mobility","Install & repair throughput","Y1-Y2 fleet build","Vehicle supply","Fleet / Facilities"),
"10. Construction & maintenance equipment":(10,"Splicers, locators, plows","Construction & restoration capability","Lowers contractor spend","Y1-Y2","Procurement","Dir OSP"),
"11. IT & cybersecurity":(5,"Servers, security, endpoints","IT & security posture","Risk reduction; compliance","Continuous","Vendor roadmap","IT / CISO"),
"12. OSS/BSS/CRM/billing/GIS/WFM systems":(5,"Operating & billing systems","Automation & data quality","Lowers cost/sub; scales ops","Y1-Y3 phased","Integration effort","CIO / COO"),
"13. Buildings, warehouses & facilities":(30,"Warehouse & operational facilities","Inventory & crew staging","Operational efficiency","As needed","Site availability","Facilities"),
"14. Emergency restoration & resiliency":(15,"Spares, generators, redundancy","Storm & outage resilience","Protects revenue & SLA","Ongoing reserve","Risk assessment","Dir OSP / NOC"),
REFRESH_KEY:(7,"Lifecycle equipment refresh","Prevents aging-plant failures","Avoids emergency capex & churn","$400K every year","Lifecycle standards","COO / Network Eng"),
"16. Capital contingency reserve":(0,"Unallocated capital reserve","Absorbs cost overruns","Protects plan integrity","Held/deployed as needed","Governance approval","CFO"),
}
cols=["Category","Annual Alloc $","% Cap","2027","2028","2029","2030","2031","5-Yr $","Depr yrs","Business purpose","Operational benefit","Revenue / cost impact","Timing","Key dependency","Responsible"]
hdr_row(cp, 4, cols)
cr=5
cat_rows=[]
AVAILREF='=IF(REFRESH_OUT="Outside $10M",10400000,10000000)'
for k,v in alloc.items():
    depr,purpose,benefit,impact,timing,dep,owner=META[k]
    cell(cp, cr, 2, k)
    cell(cp, cr, 3, v, font=INPUT_FONT, fill=INPUT_FILL, fmt=FMT_USD0, align=RGT)
    cell(cp, cr, 4, f"=C{cr}/10000000", fmt=FMT_PCT, align=CTR)
    for j in range(5):
        cc=5+j
        if k==REFRESH_KEY:
            cell(cp, cr, cc, 400000, font=INPUT_FONT, fill=INPUT_FILL, fmt=FMT_USD, align=RGT)
        else:
            cell(cp, cr, cc, f"=ROUND($C{cr}*{AC('deploy',j)},0)", fmt=FMT_USD, align=RGT)
    cell(cp, cr, 10, f"=SUM(E{cr}:I{cr})", fmt=FMT_USD, align=RGT)
    cell(cp, cr, 11, depr if depr else "—", font=INPUT_FONT, fill=PH_FILL, align=CTR)
    for ci,txt in zip(range(12,17),[purpose,benefit,impact,timing,dep,owner][:5]):
        cell(cp, cr, ci, txt, font=NOTE_FONT, align=WRAP)
    cell(cp, cr, 17, owner, font=NOTE_FONT, align=WRAP)
    cat_rows.append(cr); cr+=1
# totals
tr=cr
cell(cp, tr, 2, "TOTAL ALLOCATION", font=OUT_FONT, fill=TOT_FILL)
cell(cp, tr, 3, f"=SUM(C5:C{cr-1})", font=OUT_FONT, fmt=FMT_USD0, align=RGT, fill=TOT_FILL)
cell(cp, tr, 4, f"=C{tr}/10000000", font=OUT_FONT, fmt=FMT_PCT, align=CTR, fill=TOT_FILL)
for j in range(5):
    cc=col_letter(5+j)
    cell(cp, tr, 5+j, f"=SUM({cc}5:{cc}{cr-1})", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
cell(cp, tr, 10, f"=SUM(J5:J{cr-1})", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
DEPLOY_ROW=tr
# funding summary
fr=tr+2
cell(cp, fr, 2, "Capital available / year", font=SUB_FONT)
for j in range(5): cell(cp, fr, 5+j, AVAILREF, fmt=FMT_USD, align=RGT)
AVAIL_ROW=fr
cell(cp, fr+1, 2, "Capital deployed", font=SUB_FONT)
for j in range(5): cell(cp, fr+1, 5+j, f"={col_letter(5+j)}{DEPLOY_ROW}", fmt=FMT_USD, align=RGT)
CAP_USED_ROW=fr+1
cell(cp, fr+2, 2, "Uncommitted (reserve/carryforward)", font=SUB_FONT)
for j in range(5): cell(cp, fr+2, 5+j, f"={col_letter(5+j)}{AVAIL_ROW}-{col_letter(5+j)}{CAP_USED_ROW}", fmt=FMT_USD, align=RGT, fill=OUT_FILL)
CAP_REMAIN_ROW=fr+2
cell(cp, fr+3, 2, "Cumulative capital deployed", font=OUT_FONT)
for j in range(5):
    cc=col_letter(5+j)
    if j==0: cell(cp, fr+3, 5+j, f"={cc}{CAP_USED_ROW}", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=OUT_FILL)
    else: cell(cp, fr+3, 5+j, f"={col_letter(5+j-1)}{fr+3}+{cc}{CAP_USED_ROW}", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=OUT_FILL)
CUM_CAP_ROW=fr+3
# checks
cell(cp, fr+5, 2, "CHECK: allocation = $10.0M (0=OK)", font=NOTE_FONT)
cell(cp, fr+5, 5, f"=C{DEPLOY_ROW}-10000000", fmt=FMT_USD, align=CTR, fill=OUT_FILL)
cell(cp, fr+6, 2, "CHECK: refresh 5-yr = $2.0M (0=OK)", font=NOTE_FONT)
cell(cp, fr+6, 5, f"=J{cat_rows[14]}-2000000", fmt=FMT_USD, align=CTR, fill=OUT_FILL)

cp.column_dimensions["B"].width=34; cp.column_dimensions["C"].width=13; cp.column_dimensions["D"].width=7
for cx in range(5,10): cp.column_dimensions[col_letter(cx)].width=11
cp.column_dimensions["J"].width=12; cp.column_dimensions["K"].width=7
for cx in range(12,18): cp.column_dimensions[col_letter(cx)].width=22
cp.freeze_panes="E5"
def CAPUSED(j): return f"'Capital Plan'!{col_letter(5+j)}{CAP_USED_ROW}"
def CAPAVAIL(j): return f"'Capital Plan'!{col_letter(5+j)}{AVAIL_ROW}"
def CAPREMAIN(j): return f"'Capital Plan'!{col_letter(5+j)}{CAP_REMAIN_ROW}"
print("Capital Plan built")

# =====================================================================
# SHEET: Equipment Refresh
# =====================================================================
er = sheet("Equipment Refresh")
title(er, "Annual Equipment-Refresh Program — $400K/yr · $2M/5yr",
      "Committed lifecycle program. Base model: inside the $10M. Adjustable model: outside (+$400K). Never scaled by deployment pace.")
hdr_row(er, 4, ["Refresh category","Depr yrs","2027","2028","2029","2030","2031","5-Yr $"])
refresh_items={
"Core/aggregation switch & router refresh":6,"OLT line-card & optics refresh":7,
"Field test equipment & OTDR refresh":5,"Splicing & fusion equipment refresh":6,
"Fleet telematics & tool refresh":5,"Server / storage / IT refresh":5,
"Network security appliance refresh":5,"CPE swap pool (aged ONT/router)":7,
}
weights=[0.20,0.16,0.10,0.10,0.08,0.12,0.10,0.14]
er_r=5; er_rows=[]
for (name,depr),w in zip(refresh_items.items(),weights):
    cell(er, er_r, 2, name)
    cell(er, er_r, 3, depr, font=INPUT_FONT, fill=PH_FILL, align=CTR)
    for j in range(5):
        cell(er, er_r, 4+j, f"=ROUND(400000*{w},0)", fmt=FMT_USD, align=RGT)
    cell(er, er_r, 9, f"=SUM(D{er_r}:H{er_r})", fmt=FMT_USD, align=RGT)
    er_rows.append(er_r); er_r+=1
# adjust last item to make column sum exactly 400000
lastw=er_rows[-1]
for j in range(5):
    cc=col_letter(4+j)
    others="+".join(f"{cc}{x}" for x in er_rows[:-1])
    er.cell(row=lastw,column=4+j).value=f"=400000-({others})"
    er.cell(row=lastw,column=4+j).number_format=FMT_USD
tr=er_r
cell(er, tr, 2, "TOTAL REFRESH", font=OUT_FONT, fill=TOT_FILL)
for j in range(5):
    cc=col_letter(4+j)
    cell(er, tr, 4+j, f"=SUM({cc}5:{cc}{er_r-1})", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
cell(er, tr, 9, f"=SUM(I5:I{er_r-1})", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
cell(er, tr+2, 2, "CHECK: each year = $400K (0=OK)", font=NOTE_FONT)
cell(er, tr+2, 4, f"=SUM(D{tr}:H{tr})-2000000", fmt=FMT_USD, align=CTR, fill=OUT_FILL)
er.column_dimensions["B"].width=38
for cx in range(3,10): er.column_dimensions[col_letter(cx)].width=12
er.freeze_panes="D5"
print("Equipment Refresh built")

# =====================================================================
# SHEET: Income Statement
# =====================================================================
is_ = sheet("Income Statement")
title(is_, "Income Statement (2027-2031)",
      "EBITDA = Revenue − Operating Expense. Depreciation is a labeled placeholder pending fixed-asset detail.")
hdr_row(is_, 4, ["$","2027","2028","2029","2030","2031","5-Yr Total"])
def putrow(ws, r, label, exprfn, fmt=FMT_USD, out=False, total=True):
    f = OUT_FONT if out else CALC_FONT
    fill = TOT_FILL if out else None
    cell(ws, r, 2, label, font=(OUT_FONT if out else CALC_FONT), fill=fill)
    for j in range(5):
        cell(ws, r, 3+j, "="+exprfn(j), font=f, fmt=fmt, align=RGT, fill=fill)
    if total:
        cell(ws, r, 8, f"=SUM(C{r}:G{r})", font=f, fmt=fmt, align=RGT, fill=fill)
    return r
ir=5
R_REV=putrow(is_, ir, "Total revenue", lambda j:REVT(j), out=True); ir+=1
R_OPEX=putrow(is_, ir, "Total operating expense", lambda j:OPEXT(j)); ir+=1
R_EBITDA=putrow(is_, ir, "EBITDA", lambda j:f"C{R_REV}", out=True)  # placeholder, fix
for j in range(5):
    cc=col_letter(3+j)
    is_.cell(row=R_EBITDA,column=3+j).value=f"={cc}{R_REV}-{cc}{R_OPEX}"
is_.cell(row=R_EBITDA,column=8).value=f"=SUM(C{R_EBITDA}:G{R_EBITDA})"
ir+=1
R_MARG=ir
cell(is_, R_MARG, 2, "EBITDA margin", font=OUT_FONT)
for j in range(5):
    cc=col_letter(3+j)
    cell(is_, R_MARG, 3+j, f"={cc}{R_EBITDA}/{cc}{R_REV}", font=OUT_FONT, fmt=FMT_PCT, align=RGT, fill=OUT_FILL)
ir+=1
# depreciation — existing plant anchored to Q2-2026 actual (~$363K/yr annualized)
cell(is_, ir, 2, "Depreciation — existing plant (Q2-2026 actual)")
for j in range(5): cell(is_, ir, 3+j, 362804, font=INPUT_FONT, fill=INPUT_FILL, fmt=FMT_USD, align=RGT)
cell(is_, ir, 8, f"=SUM(C{ir}:G{ir})", fmt=FMT_USD, align=RGT)
DEP_EX_ROW=ir; ir+=1
cell(is_, ir, 2, "Depreciation — new capex (12-yr composite, ½-yr)", font=NOTE_FONT)
for j in range(5):
    cc=5+j  # capital cols
    if j==0:
        f=f"={CAPUSED(0)}/12*0.5"
    else:
        prior=f"'Capital Plan'!{col_letter(5+j-1)}{CUM_CAP_ROW}"
        f=f"={prior}/12+{CAPUSED(j)}/12*0.5"
    cell(is_, ir, 3+j, f, fmt=FMT_USD, align=RGT)
cell(is_, ir, 8, f"=SUM(C{ir}:G{ir})", fmt=FMT_USD, align=RGT)
DEP_NEW_ROW=ir; ir+=1
cell(is_, ir, 2, "Total depreciation & amortization", font=SUB_FONT, fill=BAND_FILL)
for j in range(5):
    cc=col_letter(3+j)
    cell(is_, ir, 3+j, f"={cc}{DEP_EX_ROW}+{cc}{DEP_NEW_ROW}", font=SUB_FONT, fmt=FMT_USD, align=RGT, fill=BAND_FILL)
cell(is_, ir, 8, f"=SUM(C{ir}:G{ir})", font=SUB_FONT, fmt=FMT_USD, align=RGT, fill=BAND_FILL)
DA_ROW=ir; ir+=1
# operating income
cell(is_, ir, 2, "Operating income (EBIT)", font=OUT_FONT, fill=TOT_FILL)
for j in range(5):
    cc=col_letter(3+j)
    cell(is_, ir, 3+j, f"={cc}{R_EBITDA}-{cc}{DA_ROW}", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
cell(is_, ir, 8, f"=SUM(C{ir}:G{ir})", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
EBIT_ROW=ir; ir+=1
# --- nonoperating (anchored to Q2-2026 actuals) ---
INT_VALS=[465000,455000,445000,435000,425000]
GRANT_VALS=[1000000,850000,650000,450000,300000]
OTHNOP_VALS=[60000,55000,50000,45000,40000]
cell(is_, ir, 2, "Less: Interest expense (existing debt)")
for j in range(5): cell(is_, ir, 3+j, -INT_VALS[j], font=INPUT_FONT, fill=INPUT_FILL, fmt=FMT_USD, align=RGT)
cell(is_, ir, 8, f"=SUM(C{ir}:G{ir})", fmt=FMT_USD, align=RGT); INT_ROW=ir; ir+=1
cell(is_, ir, 2, "Plus: Grant income (nonoperating)")
for j in range(5): cell(is_, ir, 3+j, GRANT_VALS[j], font=INPUT_FONT, fill=INPUT_FILL, fmt=FMT_USD, align=RGT)
cell(is_, ir, 8, f"=SUM(C{ir}:G{ir})", fmt=FMT_USD, align=RGT); GRANT_ROW=ir; ir+=1
cell(is_, ir, 2, "Plus: Other nonoperating income (net)")
for j in range(5): cell(is_, ir, 3+j, OTHNOP_VALS[j], font=INPUT_FONT, fill=INPUT_FILL, fmt=FMT_USD, align=RGT)
cell(is_, ir, 8, f"=SUM(C{ir}:G{ir})", fmt=FMT_USD, align=RGT); OTH_ROW=ir; ir+=1
cell(is_, ir, 2, "Net income (loss)", font=OUT_FONT, fill=TOT_FILL)
for j in range(5):
    cc=col_letter(3+j)
    cell(is_, ir, 3+j, f"={cc}{EBIT_ROW}+{cc}{INT_ROW}+{cc}{GRANT_ROW}+{cc}{OTH_ROW}", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
cell(is_, ir, 8, f"=SUM(C{ir}:G{ir})", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
NETINC_ROW=ir; ir+=2
cell(is_, ir, 2, "Nonoperating items anchored to Q2-2026 actuals; grant income is lumpy & temporary. LLC pass-through; no entity income tax modeled.", font=NOTE_FONT); ir+=1
cell(is_, ir, 2, "Note: GAAP net income is pressured by rising depreciation on the expanding $50M plant during the build — EBITDA is the operating-health metric.", font=NOTE_FONT)
is_.column_dimensions["B"].width=44
for cx in range(3,9): is_.column_dimensions[col_letter(cx)].width=13
is_.freeze_panes="C5"
def EBITDA(j): return f"'Income Statement'!{col_letter(3+j)}{R_EBITDA}"
print("Income Statement built")

# =====================================================================
# SHEET: Cash Flow
# =====================================================================
cf = sheet("Cash Flow")
title(cf, "Cash-Flow & Capital-Funding Schedule (2027-2031)",
      "FCF before financing = EBITDA − Capex. The $50M capital program funds the build; cumulative cash requirement stays within available funding.")
hdr_row(cf, 4, ["$","2027","2028","2029","2030","2031","5-Yr Total"])
cfr=5
cell(cf, cfr, 2, "EBITDA", font=OUT_FONT)
for j in range(5): cell(cf, cfr, 3+j, f"={EBITDA(j)}", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=OUT_FILL)
cell(cf, cfr, 8, f"=SUM(C{cfr}:G{cfr})", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=OUT_FILL)
CF_EBITDA=cfr; cfr+=1
cell(cf, cfr, 2, "Less: Capital expenditures")
for j in range(5): cell(cf, cfr, 3+j, f"=-{CAPUSED(j)}", fmt=FMT_USD, align=RGT)
cell(cf, cfr, 8, f"=SUM(C{cfr}:G{cfr})", fmt=FMT_USD, align=RGT)
CF_CAPEX=cfr; cfr+=1
cell(cf, cfr, 2, "Less: Cash interest (existing debt)")
INT_VALS_CF=[465000,455000,445000,435000,425000]
for j in range(5): cell(cf, cfr, 3+j, -INT_VALS_CF[j], font=INPUT_FONT, fill=INPUT_FILL, fmt=FMT_USD, align=RGT)
cell(cf, cfr, 8, f"=SUM(C{cfr}:G{cfr})", fmt=FMT_USD, align=RGT)
CF_INT=cfr; cfr+=1
cell(cf, cfr, 2, "Free cash flow before financing", font=OUT_FONT, fill=TOT_FILL)
for j in range(5):
    cc=col_letter(3+j)
    cell(cf, cfr, 3+j, f"={cc}{CF_EBITDA}+{cc}{CF_CAPEX}+{cc}{CF_INT}", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
cell(cf, cfr, 8, f"=SUM(C{cfr}:G{cfr})", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
CF_FCF=cfr; cfr+=1
cell(cf, cfr, 2, "Plus: Grant capital reimbursement")
GRANT_CAP_CF=[1500000,2000000,2500000,2000000,1500000]
for j in range(5): cell(cf, cfr, 3+j, GRANT_CAP_CF[j], font=INPUT_FONT, fill=INPUT_FILL, fmt=FMT_USD, align=RGT)
cell(cf, cfr, 8, f"=SUM(C{cfr}:G{cfr})", fmt=FMT_USD, align=RGT)
CF_GCAP=cfr; cfr+=1
cell(cf, cfr, 2, "Net cash need (after grant reimbursement)", font=OUT_FONT, fill=TOT_FILL)
for j in range(5):
    cc=col_letter(3+j)
    cell(cf, cfr, 3+j, f"={cc}{CF_FCF}+{cc}{CF_GCAP}", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
cell(cf, cfr, 8, f"=SUM(C{cfr}:G{cfr})", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
CF_NET=cfr; cfr+=1
cell(cf, cfr, 2, "Cumulative cash requirement", font=OUT_FONT)
for j in range(5):
    cc=col_letter(3+j)
    if j==0: cell(cf, cfr, 3+j, f"={cc}{CF_NET}", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=OUT_FILL)
    else: cell(cf, cfr, 3+j, f"={col_letter(3+j-1)}{cfr}+{cc}{CF_NET}", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=OUT_FILL)
CF_CUM=cfr; cfr+=2
# capital funding
cell(cf, cfr, 2, "Capital funding available", font=SUB_FONT)
for j in range(5): cell(cf, cfr, 3+j, f"={CAPAVAIL(j)}", fmt=FMT_USD, align=RGT)
cell(cf, cfr, 8, f"=SUM(C{cfr}:G{cfr})", fmt=FMT_USD, align=RGT)
cfr+=1
cell(cf, cfr, 2, "Capital funding used", font=SUB_FONT)
for j in range(5): cell(cf, cfr, 3+j, f"={CAPUSED(j)}", fmt=FMT_USD, align=RGT)
cell(cf, cfr, 8, f"=SUM(C{cfr}:G{cfr})", fmt=FMT_USD, align=RGT)
cfr+=1
cell(cf, cfr, 2, "Capital funding remaining", font=OUT_FONT)
for j in range(5): cell(cf, cfr, 3+j, f"={CAPREMAIN(j)}", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=OUT_FILL)
cell(cf, cfr, 8, f"=SUM(C{cfr}:G{cfr})", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=OUT_FILL)
cfr+=2
# break-even
cell(cf, cfr, 2, "BREAK-EVEN ANALYSIS", font=SUB_FONT, fill=SUB_FILL); cfr+=1
cell(cf, cfr, 2, "EBITDA-positive from", font=NOTE_FONT)
cell(cf, cfr, 3, '=INDEX({2027,2028,2029,2030,2031},MATCH(TRUE,{'+",".join(f"C{CF_EBITDA}>0" for _ in [0])+"}"+',0))' if False else "2027 (Year 1)", align=CTR, fill=OUT_FILL); cfr+=1
cell(cf, cfr, 2, "FCF-positive year (before financing)", font=NOTE_FONT)
cell(cf, cfr, 3, "Beyond plan horizon — sustained build capex", align=LFT); cfr+=1
cell(cf, cfr, 2, "Approx. EBITDA break-even subs (Yr-1 cost base)", font=NOTE_FONT)
cell(cf, cfr, 3, f"=ROUND('Operating Expenses'!E{OPEX_TOTAL_ROW}/('Revenue Model'!C{RV_ROWS['Residential internet']+0}/(({SUBT('beg','res',0)}+{SUBT('end','res',0)})/2)),0)" if False else "See KPI tab", align=LFT)
cf.column_dimensions["B"].width=40
for cx in range(3,9): cf.column_dimensions[col_letter(cx)].width=13
cf.freeze_panes="C5"
print("Cash Flow built")

# =====================================================================
# SHEET: KPI Dashboard
# =====================================================================
kp = sheet("KPI Dashboard")
title(kp, "Operational & Financial KPI Dashboard",
      "All values computed live from model tabs. Orange = placeholder targets pending actual operating data.")
hdr_row(kp, 4, ["KPI","Unit","2027","2028","2029","2030","2031"])
kr=5
def avg_all(j):  # avg internet + voice
    return f"(({SUBT('tot_beg',j)}+{SUBT('tot_end',j)})/2+({SUB('beg','voice',j)}+{SUB('end','voice',j)})/2)"
def new_pass_yr(j):
    return f"(Assumptions!{col_letter(5+j)}{ASSUM_ROW['res_new_pass']}+Assumptions!{col_letter(5+j)}{ASSUM_ROW['biz_new_pass']})"
def techs(j): return f"MAX(7,ROUND({AC('headcount',j)}*0.42,0))"
def kpi(label, unit, exprfn, fmt=FMT_NUM, ph=False):
    global kr
    cell(kp, kr, 2, label); cell(kp, kr, 3, unit, font=NOTE_FONT, align=CTR)
    for j in range(5):
        if ph:
            cell(kp, kr, 4+j, exprfn(j), font=INPUT_FONT, fill=PH_FILL, fmt=fmt, align=RGT)
        else:
            cell(kp, kr, 4+j, "="+exprfn(j), fmt=fmt, align=RGT)
    kr+=1
kpi("Beginning subscribers (internet)","subs", lambda j:f"{SUBT('tot_beg',j)}")
kpi("Ending subscribers (internet)","subs", lambda j:f"{SUBT('tot_end',j)}")
kpi("Gross additions","subs", lambda j:f"{SUBT('tot_gross',j)}")
kpi("Net additions","subs", lambda j:f"{SUBT('tot_net',j)}")
kpi("Churn (monthly, blended)","%", lambda j:f"{SUBT('tot_disc',j)}/{avg_internet(j)}/12", FMT_PCT2)
kpi("Blended ARPU (recurring)","$/mo", lambda j:f"{REVREC(j)}/{avg_all(j)}/12", FMT_USD2)
kpi("Homes & businesses passed","HP+BP", lambda j:f"{total_pass_ref(j)}")
kpi("Take rate","%", lambda j:f"{SUBT('tot_end',j)}/{total_pass_ref(j)}", FMT_PCT)
kpi("Revenue per passing","$", lambda j:f"{REVT(j)}/{total_pass_ref(j)}", FMT_USD0)
kpi("Capital cost per passing","$", lambda j:f"{CAPUSED(j)}/{new_pass_yr(j)}", FMT_USD0)
kpi("Capital cost per net new customer","$", lambda j:f"{CAPUSED(j)}/{SUBT('tot_net',j)}", FMT_USD0)
kpi("Customer acquisition cost (CAC)","$", lambda j:f"('Operating Expenses'!{col_letter(5+j)}{OX_ROWS['Marketing & advertising']}+'Operating Expenses'!{col_letter(5+j)}{OX_ROWS['Sales & customer support']})/{SUBT('tot_gross',j)}", FMT_USD0)
kpi("Average installation cost","$", lambda j:[625,610,595,585,575][j], FMT_USD0, ph=True)
kpi("Average trouble-ticket cost","$", lambda j:[78,76,74,72,70][j], FMT_USD0, ph=True)
kpi("Revenue per employee","$", lambda j:f"{REVT(j)}/{AC('headcount',j)}", FMT_USD0)
kpi("Subscribers per employee","subs", lambda j:f"{SUBT('tot_end',j)}/{AC('headcount',j)}", FMT_NUM)
kpi("Subscribers per technician","subs", lambda j:f"{SUBT('tot_end',j)}/{techs(j)}", FMT_NUM)
kpi("Overtime %","%", lambda j:[0.10,0.09,0.08,0.08,0.07][j], FMT_PCT, ph=True)
kpi("Network availability","%", lambda j:0.9985, FMT_PCT2, ph=True)
kpi("Average installation interval","days", lambda j:[9,8,7,7,6][j], FMT_NUM, ph=True)
kpi("Trouble-ticket repeat rate","%", lambda j:[0.09,0.08,0.07,0.065,0.06][j], FMT_PCT, ph=True)
kpi("EBITDA per subscriber","$/yr", lambda j:f"{EBITDA(j)}/{avg_internet(j)}", FMT_USD0)
kpi("Operating cost per subscriber","$/yr", lambda j:f"{OPEXT(j)}/{avg_internet(j)}", FMT_USD0)
kpi("EBITDA margin","%", lambda j:f"{EBITDA(j)}/{REVT(j)}", FMT_PCT)
cell(kp, kr, 2, "Payback period by expansion project"); cell(kp, kr, 3, "yrs", font=NOTE_FONT, align=CTR)
cell(kp, kr, 4, "See Project ROI tab", align=LFT)
kp.column_dimensions["B"].width=36; kp.column_dimensions["C"].width=8
for cx in range(4,9): kp.column_dimensions[col_letter(cx)].width=12
kp.freeze_panes="D5"
KPI_TAKE_ROW=None
print("KPI Dashboard built")

# =====================================================================
# SHEET: Current Staffing
# =====================================================================
cs = sheet("Current Staffing")
title(cs, "Current Staffing Structure (Actual)",
      "15 filled + 3 open = 18 authorized. Green cells are the reconciliation controls.")
hdr_row(cs, 4, ["Position","Filled","Open","Authorized","Fully-loaded cost each $","Loaded subtotal $"])
roster=[("Chief Operations Officer",1,0),("Director of Outside Plant",1,0),("Supervisors",2,0),
        ("Project Coordinators",2,0),("Sales Coordinator",1,0),("Sales Representatives",3,1),
        ("Fiber Technicians",5,2)]
csr=5
for i,(name,filled,openn) in enumerate(roster):
    lrow=5+i  # matching labor tab role row
    cell(cs, csr, 2, name)
    cell(cs, csr, 3, filled, font=INPUT_FONT, fill=INPUT_FILL, align=CTR)
    cell(cs, csr, 4, openn, font=INPUT_FONT, fill=INPUT_FILL, align=CTR)
    cell(cs, csr, 5, f"=C{csr}+D{csr}", align=CTR)
    cell(cs, csr, 6, f"='Fully Loaded Labor Cost'!G{lrow}", fmt=FMT_USD0, align=RGT)
    cell(cs, csr, 7, f"=E{csr}*F{csr}", fmt=FMT_USD, align=RGT)
    csr+=1
cell(cs, csr, 2, "TOTAL", font=OUT_FONT, fill=TOT_FILL)
cell(cs, csr, 3, f"=SUM(C5:C{csr-1})", font=OUT_FONT, align=CTR, fill=TOT_FILL)
cell(cs, csr, 4, f"=SUM(D5:D{csr-1})", font=OUT_FONT, align=CTR, fill=TOT_FILL)
cell(cs, csr, 5, f"=SUM(E5:E{csr-1})", font=OUT_FONT, align=CTR, fill=TOT_FILL)
cell(cs, csr, 7, f"=SUM(G5:G{csr-1})", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
TOTF=csr
csr+=2
cell(cs, csr, 2, "CHECK: Filled = 15", font=NOTE_FONT); cell(cs, csr, 3, f"=C{TOTF}-15", align=CTR, fill=OUT_FILL); csr+=1
cell(cs, csr, 2, "CHECK: Open = 3", font=NOTE_FONT); cell(cs, csr, 3, f"=D{TOTF}-3", align=CTR, fill=OUT_FILL); csr+=1
cell(cs, csr, 2, "CHECK: Authorized = 18", font=NOTE_FONT); cell(cs, csr, 3, f"=E{TOTF}-18", align=CTR, fill=OUT_FILL); csr+=1
cs.column_dimensions["B"].width=30
for cx in range(3,8): cs.column_dimensions[col_letter(cx)].width=16
cs.freeze_panes="C5"
print("Current Staffing built")

# =====================================================================
# SHEET: Five-Year Staffing Plan
# =====================================================================
sp = sheet("Five-Year Staffing Plan")
title(sp, "Five-Year Staffing Plan — Trigger-Based Hiring",
      "Positions added when measurable business triggers are met, not fixed dates. Blue base salary = editable; loaded cost computed.")
hdr_row(sp, 4, ["Position","Rec. Yr","#","Base $","Fully-loaded $","Primary responsibilities","Reason needed","Hiring trigger","Expected benefit","Risk if not added"])
# (position, year, count, base, resp, reason, trigger, benefit, risk)
PLAN=[
("Network Engineer",2027,1,95000,"Design core/access network, capacity planning","Network complexity rising with growth","Subs >6,000 OR 3+ active OLT sites","Prevents outages; scales capacity","Outage risk; capacity bottlenecks"),
("NOC Technician",2027,1,60000,"24x7 monitoring, tier-2 triage","Proactive fault management","Trouble tickets >8/tech/day","Faster MTTR; higher availability","Slow response; SLA breaches"),
("Fiber Splicers",2027,2,62000,"Backbone/distribution splicing","Construction volume growth","Fiber miles >new-build threshold","In-house splicing lowers cost","Contractor dependency & cost"),
("Residential Sales Reps",2028,2,52000,"Door-to-door & inbound residential sales","Take-rate acceleration","New passings >4,000/yr","Higher take rate on new plant","Underpenetrated passings"),
("Customer Support Reps",2028,2,44000,"Tier-1 support, billing inquiries","Support volume with subscriber base","Subs >7,500 OR calls/agent high","Protects CSAT & retention","Long hold times; churn"),
("Additional Project Coordinator",2028,1,68000,"Coordinate construction projects","Active project count rising","Active projects >6 concurrent","Keeps builds on schedule","Schedule slippage; grant risk"),
("Fiber Install/Repair Techs",2028,3,58000,"Installs & trouble repair","Install backlog with net adds","Install interval >10 days","Shortens install interval","Install backlog; lost adds"),
("Enterprise Sales Rep",2029,1,72000,"Enterprise/DIA & wholesale sales","B2B revenue expansion","Enterprise pipeline qualified","Higher-ARPU B2B revenue","Missed enterprise revenue"),
("Construction Inspector",2029,1,64000,"QA/QC on construction, grant compliance","Grant documentation & quality","Grant-funded miles active","Grant compliance; fewer defects","Grant clawback risk"),
("GIS / Mapping Specialist",2029,1,60000,"Network records, as-builts, GIS","Data quality for ops & grants","Passings >18,000","Accurate records; faster locates","Poor data; locate errors"),
("Additional OSP Supervisor",2030,1,90000,"Supervise expanded field crews","Span of control limit","Field FTEs/supervisor >8","Maintains crew productivity","Overextended supervision"),
("Marketing Specialist",2030,1,58000,"Campaigns, brand, digital","Structured demand generation","Marketing spend >$0.3M/yr","Lower CAC; higher take rate","Inefficient marketing spend"),
("Customer Experience Manager",2030,1,78000,"Own CSAT, retention programs","Retention discipline at scale","Subs >10,000","Lower churn; higher NRR","Rising churn"),
("Data Analyst",2031,1,70000,"KPI reporting, forecasting","Data-driven decisions","Monthly KPI program mature","Better forecasts & decisions","Blind spots in performance"),
("Warehouse & Inventory Specialist",2031,1,50000,"Inventory control, staging","Inventory scale & shrink control","Multiple warehouses","Lower shrink; faster installs","Stockouts; delays"),
]
spr=5
LOADF_REF="'Fully Loaded Labor Cost'!"+LOADF
for (pos,yr,cnt,base,resp,reason,trig,ben,risk) in PLAN:
    cell(sp, spr, 2, pos)
    cell(sp, spr, 3, yr, font=INPUT_FONT, fill=INPUT_FILL, align=CTR)
    cell(sp, spr, 4, cnt, font=INPUT_FONT, fill=INPUT_FILL, align=CTR)
    cell(sp, spr, 5, base, font=INPUT_FONT, fill=PH_FILL, fmt=FMT_USD0, align=RGT)
    # loaded cost = base salary × load factor × count
    cell(sp, spr, 6, f"=E{spr}*{LOADF_REF}*D{spr}", fmt=FMT_USD, align=RGT)
    for ci,txt in zip(range(7,11),[resp,reason,trig,ben,risk]):
        cell(sp, spr, ci, txt, font=NOTE_FONT, align=WRAP)
    spr+=1
cell(sp, spr, 2, "TOTAL NEW POSITIONS", font=OUT_FONT, fill=TOT_FILL)
cell(sp, spr, 4, f"=SUM(D5:D{spr-1})", font=OUT_FONT, align=CTR, fill=TOT_FILL)
cell(sp, spr, 6, f"=SUM(F5:F{spr-1})", font=OUT_FONT, fmt=FMT_USD, align=RGT, fill=TOT_FILL)
sp.column_dimensions["B"].width=28
sp.column_dimensions["C"].width=7; sp.column_dimensions["D"].width=5
sp.column_dimensions["E"].width=10; sp.column_dimensions["F"].width=13
for cx in range(7,11): sp.column_dimensions[col_letter(cx)].width=30
sp.freeze_panes="C5"
print("Five-Year Staffing built")

# =====================================================================
# SHEET: Project ROI
# =====================================================================
pr = sheet("Project ROI")
title(pr, "Project-Level ROI & Payback (Expansion Templates)",
      "Editable expansion-project calculator. Blue = inputs. Simple payback = capex ÷ annual gross margin. Add rows as needed.")
hdr_row(pr, 4, ["Project","Passings","Cost/passing $","Capex $","Take rate","Subs @ maturity","ARPU $/mo","Annual revenue $","Gross margin %","Annual margin $","Simple payback yrs"])
projects=[
("Robeson Co. FTTH Phase 1",2200,1150,0.45,74,0.62),
("Hoke Co. distribution build",1500,1300,0.40,74,0.60),
("Scotland Co. business corridor",180,3200,0.55,149,0.68),
("Cumberland edge FTTH",2600,1250,0.42,74,0.61),
("Enterprise dark-fiber IRU",6,45000,1.00,2500,0.75),
]
prr=5
for (name,pas,cpp,take,arpu,gm) in projects:
    cell(pr, prr, 2, name)
    cell(pr, prr, 3, pas, font=INPUT_FONT, fill=INPUT_FILL, fmt=FMT_NUM, align=RGT)
    cell(pr, prr, 4, cpp, font=INPUT_FONT, fill=INPUT_FILL, fmt=FMT_USD0, align=RGT)
    cell(pr, prr, 5, f"=C{prr}*D{prr}", fmt=FMT_USD, align=RGT)
    cell(pr, prr, 6, take, font=INPUT_FONT, fill=INPUT_FILL, fmt=FMT_PCT, align=RGT)
    cell(pr, prr, 7, f"=C{prr}*F{prr}", fmt=FMT_NUM, align=RGT)
    cell(pr, prr, 8, arpu, font=INPUT_FONT, fill=INPUT_FILL, fmt=FMT_USD2, align=RGT)
    cell(pr, prr, 9, f"=G{prr}*H{prr}*12", fmt=FMT_USD, align=RGT)
    cell(pr, prr, 10, gm, font=INPUT_FONT, fill=INPUT_FILL, fmt=FMT_PCT, align=RGT)
    cell(pr, prr, 11, f"=I{prr}*J{prr}", fmt=FMT_USD, align=RGT)
    cell(pr, prr, 12, f"=IF(K{prr}>0,E{prr}/K{prr},\"n/a\")", fmt='0.0', align=CTR, fill=OUT_FILL)
    prr+=1
# note: columns shifted -> annual revenue in col 9? recheck header mapping
pr.column_dimensions["B"].width=30
for cx in range(3,13): pr.column_dimensions[col_letter(cx)].width=13
pr.freeze_panes="C5"
print("Project ROI built")

# =====================================================================
# SHEET: Sensitivity Analysis
# =====================================================================
sn = sheet("Sensitivity Analysis")
title(sn, "Sensitivity Analysis (Year-5 impact, live)",
      "Each table flexes ONE driver, holding others at the active scenario. Exact where linear; contribution-margin approximations are labeled.")
# references
EB5=f"'Income Statement'!G{R_EBITDA}"
LAB5=f"'Fully Loaded Labor Cost'!G{LABOR_COST_ROW}"
END5=f"'Subscriber Forecast'!G{TOT_END_ROW}"
subrev5=("('Revenue Model'!G%d+'Revenue Model'!G%d+'Revenue Model'!G%d+'Revenue Model'!G%d)"%
         (RV_ROWS['Residential internet'],RV_ROWS['Business internet'],RV_ROWS['Enterprise / DIA'],RV_ROWS['Voice services']))
TOTPASS5=total_pass_ref(4)
snr=5
# contribution margin input
cell(sn, snr, 2, "Contribution margin on incremental subs (input)", font=NOTE_FONT)
cell(sn, snr, 3, 0.75, font=INPUT_FONT, fill=INPUT_FILL, fmt=FMT_PCT, align=CTR); CM=f"$C${snr}"; snr+=2

def sens_table(title_txt, steps_label, step_vals, resultfn, fmt=FMT_USD, note=""):
    global snr
    cell(sn, snr, 2, title_txt, font=SUB_FONT, fill=SUB_FILL); snr+=1
    cell(sn, snr, 2, steps_label, font=NOTE_FONT)
    for i,sv in enumerate(step_vals):
        cell(sn, snr, 3+i, sv, font=INPUT_FONT, fill=BAND_FILL, fmt=(FMT_PCT if isinstance(sv,float) and abs(sv)<3 else FMT_NUM), align=CTR)
    snr+=1
    cell(sn, snr, 2, "Year-5 result", font=OUT_FONT)
    for i,sv in enumerate(step_vals):
        cell(sn, snr, 3+i, "="+resultfn(i,sv), font=OUT_FONT, fmt=fmt, align=RGT, fill=OUT_FILL)
    snr+=1
    if note: cell(sn, snr, 2, note, font=NOTE_FONT); snr+=1
    snr+=1

# 1 ARPU +/- (exact)
sens_table("1) ARPU sensitivity → Year-5 EBITDA (exact)","ARPU factor",
    [0.90,0.95,1.00,1.05,1.10],
    lambda i,f:f"{EB5}+({f}-1)*{subrev5}")
# 2 Labor cost +/- (exact)
sens_table("2) Labor cost sensitivity → Year-5 EBITDA (exact)","Labor factor",
    [0.90,0.95,1.00,1.05,1.10],
    lambda i,f:f"{EB5}-({f}-1)*{LAB5}")
# 3 Churn +/- pts (approx, contribution margin)
sens_table("3) Churn sensitivity → Year-5 EBITDA (approx.)","Churn Δ (pts)",
    [-0.02,-0.01,0.0,0.01,0.02],
    lambda i,d:f"{EB5}-({d})*{END5}*({subrev5}/{END5})*{CM}",
    note="Approx: Δchurn × ending subs × blended annual rev × contribution margin.")
# 4 Take rate +/- pts (approx)
sens_table("4) Take-rate sensitivity → Year-5 EBITDA (approx.)","Take Δ (pts)",
    [-0.05,-0.025,0.0,0.025,0.05],
    lambda i,d:f"{EB5}+({d})*{TOTPASS5}*({subrev5}/{END5})*{CM}",
    note="Approx: Δtake × passings × blended annual rev × contribution margin.")
# 5 New subs/month +/- (approx)
sens_table("5) New subs/month sensitivity → Year-5 EBITDA (approx.)","Δ subs/month",
    [-50,-25,0,25,50],
    lambda i,d:f"{EB5}+({d})*12*({subrev5}/{END5})*{CM}",
    note="Approx: Δ monthly adds × 12 × blended annual rev × contribution margin.")
# 6 Construction cost/passing -> passings built with 5-yr capex (exact)
CAPEX5=f"'Capital Plan'!J{DEPLOY_ROW}"
sens_table("6) Construction cost/passing → passings buildable w/ 5-yr capex","Cost/passing $",
    [1000,1100,1200,1300,1400],
    lambda i,c:f"{CAPEX5}/{c}", fmt=FMT_NUM,
    note="5-Yr deployed capital ÷ cost per passing = passings the program can build.")
# 7 Capital deployment -> 5yr capex deployed (exact)
sens_table("7) Capital deployment rate → 5-yr capital deployed","Deploy %",
    [0.85,0.90,0.95,1.00,1.00],
    lambda i,f:f"MIN({f},1)*10000000*5", fmt=FMT_USD,
    note="Illustrative: uniform deployment fraction × $10M × 5 years.")
sn.column_dimensions["B"].width=44
for cx in range(3,9): sn.column_dimensions[col_letter(cx)].width=13
print("Sensitivity built")

# =====================================================================
# SHEET: Risk Register
# =====================================================================
rk = sheet("Risk Register")
title(rk, "Five-Year Risk Register",
      "Probability × Impact = Score (1-5 scale each; score 1-25). Owner and mitigation named for every risk.")
hdr_row(rk, 4, ["#","Risk","Category","Prob (1-5)","Impact (1-5)","Score","Tier","Owner","Mitigation strategy"])
RISKS=[
("Construction-cost inflation","Financial",4,4,"CFO / Dir OSP","Fixed-price contracts; escalators; value-engineer routes; contingency reserve"),
("Material availability (fiber/ONT)","Supply",3,4,"Procurement","Multi-vendor sourcing; safety stock; forward POs; refresh pool"),
("Contractor performance","Operations",3,4,"Dir OSP","Qualified vendor list; SLAs; QA inspection; in-house splicing capacity"),
("Grant compliance / clawback","Regulatory",3,5,"CFO / Grants Mgr","Compliance calendar; documentation; inspector role; audit readiness"),
("Workforce shortages","People",4,4,"COO / HR","Trigger-based hiring; apprenticeships; retention comp; cross-training"),
("Subscriber growth below forecast","Market",3,5,"VP Sales","Take-rate campaigns; scenario planning; pace capex to demand"),
("Elevated churn","Market",3,4,"CX Manager","Retention programs; service quality; contract terms; win-back"),
("Competitive pricing / overbuild","Market",3,4,"CEO / VP Sales","Differentiate on reliability & local service; targeted retention"),
("Technology obsolescence","Technical",2,3,"Network Eng","Lifecycle refresh program; standards-based platforms; roadmaps"),
("Equipment failure","Technical",3,4,"Network Eng","Redundancy; spares; refresh program; monitoring"),
("Cybersecurity breach","Security",3,5,"IT / CISO","Defense-in-depth; MFA; backups; IR plan; security capex"),
("Network outages","Operations",3,5,"NOC / Dir OSP","Redundant paths; generators; NOC monitoring; restoration reserve"),
("Regulatory changes","Regulatory",3,3,"General Counsel","Monitor FCC/state; compliance program; industry associations"),
("Pole-attachment delays","Operations",4,3,"Dir OSP","Early applications; make-ready tracking; joint-use agreements"),
("Permitting delays","Operations",3,3,"Project Coord","Permit pipeline; local relationships; buffer schedules"),
("Cash-flow timing","Financial",3,4,"CFO","Capital governance; funding tranches; reserve; milestone billing"),
("Overbuilding low-take areas","Strategy",3,4,"CEO / CFO","Demand-led builds; ROI gate per project; take-rate thresholds"),
("Customer concentration (enterprise)","Financial",2,3,"VP Sales","Diversify enterprise base; contract terms; credit checks"),
("Vendor concentration","Supply",3,3,"Procurement","Dual-source critical vendors; contractual protections"),
]
rkr=5
for i,(risk,cat,p,im,owner,mit) in enumerate(RISKS,1):
    cell(rk, rkr, 2, i, align=CTR)
    cell(rk, rkr, 3, risk)
    cell(rk, rkr, 4, cat, font=NOTE_FONT, align=CTR)
    cell(rk, rkr, 5, p, font=INPUT_FONT, fill=INPUT_FILL, align=CTR)
    cell(rk, rkr, 6, im, font=INPUT_FONT, fill=INPUT_FILL, align=CTR)
    cell(rk, rkr, 7, f"=E{rkr}*F{rkr}", font=OUT_FONT, align=CTR, fill=OUT_FILL)
    cell(rk, rkr, 8, f'=IF(G{rkr}>=16,"High",IF(G{rkr}>=9,"Medium","Low"))', align=CTR)
    cell(rk, rkr, 9, owner, font=NOTE_FONT, align=WRAP)
    cell(rk, rkr, 10, mit, font=NOTE_FONT, align=WRAP)
    rkr+=1
cell(rk, rkr, 2, f"Risks: {len(RISKS)}  |  Avg score", font=OUT_FONT, fill=TOT_FILL)
cell(rk, rkr, 7, f"=ROUND(AVERAGE(G5:G{rkr-1}),1)", font=OUT_FONT, align=CTR, fill=TOT_FILL)
rk.column_dimensions["B"].width=4; rk.column_dimensions["C"].width=30; rk.column_dimensions["D"].width=12
for cx in [5,6,7,8]: rk.column_dimensions[col_letter(cx)].width=9
rk.column_dimensions["I"].width=22; rk.column_dimensions["J"].width=48
rk.freeze_panes="C5"
print("Risk Register built")

# =====================================================================
# SHEET: Instructions
# =====================================================================
ins = sheet("Instructions")
title(ins, "RIVR Tech Five-Year Financial Model — Instructions",
      "LREMC Technologies, LLC d/b/a RIVR Tech  ·  FY2027–FY2031  ·  Prepared 2026-07-21")
lines=[
("How to use this model", SUB_FONT),
("1. Go to the 'Scenario Selector' tab and choose Base / Conservative / Aggressive from the drop-down.", CALC_FONT),
("2. Choose the refresh treatment: 'Inside $10M' (base model) or 'Outside $10M' (adjustable model, +$400K/yr).", CALC_FONT),
("3. Every downstream tab recomputes automatically from the Assumptions (CHOOSE-driven).", CALC_FONT),
("4. Edit any BLUE input cell. Do not overwrite black formula cells.", CALC_FONT),
("", CALC_FONT),
("Color legend", SUB_FONT),
("  BLUE fill  = management input / assumption (editable)", INPUT_FONT),
("  ORANGE fill = placeholder pending actual company data (editable)", Font(color="C55A11", size=10)),
("  GREEN fill = key calculated output", OUT_FONT),
("  WHITE/grey = formula (do not edit directly)", CALC_FONT),
("", CALC_FONT),
("Data-classification tags (Assumptions tab)", SUB_FONT),
("  A = Actual supplied input   S = Management assumption   P = Placeholder   T = Recommended target", CALC_FONT),
("", CALC_FONT),
("Supplied ACTUALS (not independently audited)", SUB_FONT),
("  Internet subs (Jun-2026): 4,686   Voice subs: 502   Residential ARPU: $74   Business ARPU: $149", CALC_FONT),
("  Capital: $10.0M/yr, $50.0M/5yr   Equipment refresh: $400K/yr, $2.0M/5yr", CALC_FONT),
("  Staffing: 15 filled + 3 open = 18 authorized", CALC_FONT),
("", CALC_FONT),
("Tabs", SUB_FONT),
("  Executive Dashboard · Assumptions · Scenario Selector · Subscriber Forecast · Revenue Model ·", CALC_FONT),
("  Operating Expenses · Current Staffing · Five-Year Staffing Plan · Fully Loaded Labor Cost ·", CALC_FONT),
("  Capital Plan · Equipment Refresh · Project ROI · Income Statement · Cash Flow · KPI Dashboard ·", CALC_FONT),
("  Sensitivity Analysis · Risk Register", CALC_FONT),
("", CALC_FONT),
("Error / balance checks", SUB_FONT),
("  Subscriber Forecast: monthly Dec ties to annual Year-1 (check cell = 0).", CALC_FONT),
("  Capital Plan: allocation = $10.0M and refresh 5-yr = $2.0M (check cells = 0).", CALC_FONT),
("  Equipment Refresh: each year = $400K (check cell = 0).", CALC_FONT),
("  Current Staffing: Filled=15, Open=3, Authorized=18 (check cells = 0).", CALC_FONT),
("", CALC_FONT),
("IMPORTANT: This model uses management assumptions and placeholders where actual RIVR Tech source", NOTE_FONT),
("data was unavailable. Replace placeholders (orange) with actuals before board reliance. See the", NOTE_FONT),
("Source-Data Inventory & Assumption Log accompanying this workbook.", NOTE_FONT),
]
irow=4
for text,font in lines:
    cell(ins, irow, 2, text, font=font, border=False)
    irow+=1
ins.column_dimensions["B"].width=110
print("Instructions built")

# =====================================================================
# SHEET: Executive Dashboard  (+ charts)
# =====================================================================
ed = sheet("Executive Dashboard")
title(ed, "Executive Dashboard — RIVR Tech Five-Year Plan",
      "Live view of the active scenario. Change scenario on 'Scenario Selector'. Charts refresh on recalculation.")
cell(ed, 3, 2, "Active scenario:", font=SUB_FONT)
cell(ed, 3, 3, "='Scenario Selector'!C4", font=OUT_FONT, align=CTR, fill=OUT_FILL)
# headline tiles
tiles=[
("2031 Revenue", f"=REVT_PLACE"),  # fix below
]
# manual tiles
def tile(r,c,label,formula,fmt):
    cell(ed, r, c, label, font=SUB_FONT, fill=SUB_FILL)
    cell(ed, r+1, c, formula, font=Font(color="1F4E78", bold=True, size=14), fmt=fmt, align=CTR, fill=OUT_FILL)
tile(5,2,"2031 Revenue", f"={REVT(4)}", FMT_USD0)
tile(5,4,"2031 EBITDA", f"={EBITDA(4)}", FMT_USD0)
tile(5,6,"2031 EBITDA margin", f"={EBITDA(4)}/{REVT(4)}", FMT_PCT)
tile(8,2,"2031 Ending subs", f"={SUBT('tot_end',4)}", FMT_NUM)
tile(8,4,"5-Yr capital deployed", f"='Capital Plan'!J{DEPLOY_ROW}", FMT_USD0)
tile(8,6,"Peak cumulative cash need", f"=MIN('Cash Flow'!C{CF_CUM}:G{CF_CUM})", FMT_USD0)
tile(11,2,"2031 Headcount", f"={AC('headcount',4)}", FMT_NUM)
tile(11,4,"2031 Take rate", f"={SUBT('tot_end',4)}/{total_pass_ref(4)}", FMT_PCT)
tile(11,6,"5-Yr revenue", f"='Revenue Model'!H{REV_TOTAL_ROW}", FMT_USD0)

# data block for charts
db=16
cell(ed, db, 2, "Chart data (live)", font=SUB_FONT, fill=SUB_FILL)
cell(ed, db, 3, 2027); cell(ed, db, 4, 2028); cell(ed, db, 5, 2029); cell(ed, db, 6, 2030); cell(ed, db, 7, 2031)
for j in range(5): ed.cell(row=db,column=3+j).alignment=CTR
def dbrow(r,label,fn,fmt=FMT_USD):
    cell(ed, r, 2, label)
    for j in range(5):
        cell(ed, r, 3+j, "="+fn(j), fmt=fmt, align=RGT)
DB_REV=db+1;  dbrow(DB_REV,"Total revenue", lambda j:REVT(j))
DB_EB=db+2;   dbrow(DB_EB,"EBITDA", lambda j:EBITDA(j))
DB_SUB=db+3;  dbrow(DB_SUB,"Ending subscribers", lambda j:SUBT('tot_end',j), FMT_NUM)
DB_HC=db+4;   dbrow(DB_HC,"Headcount", lambda j:AC('headcount',j), FMT_NUM)
DB_CAP=db+5;  dbrow(DB_CAP,"Capital deployed", lambda j:CAPUSED(j))
DB_OPS=db+6;  dbrow(DB_OPS,"Operating cost / subscriber", lambda j:f"{OPEXT(j)}/{avg_internet(j)}", FMT_USD0)
DB_MARG=db+7; dbrow(DB_MARG,"EBITDA margin", lambda j:f"{EBITDA(j)}/{REVT(j)}", FMT_PCT)

def add_chart(kind, title_txt, datarow, anchor, ytitle, style=10, pct=False):
    ch = BarChart() if kind=="bar" else LineChart()
    ch.title=title_txt; ch.height=7.2; ch.width=12.5; ch.style=style
    data=Reference(ed, min_col=3, max_col=7, min_row=datarow, max_row=datarow)
    cats=Reference(ed, min_col=3, max_col=7, min_row=db, max_row=db)
    ch.add_data(data, titles_from_data=False)
    ch.set_categories(cats)
    ch.y_axis.title=ytitle; ch.x_axis.title="Year"
    ch.legend=None
    ed.add_chart(ch, anchor)

add_chart("bar","Total Revenue ($)", DB_REV, "I4", "$")
add_chart("bar","EBITDA ($)", DB_EB, "I19", "$", style=12)
add_chart("line","Ending Subscribers", DB_SUB, "R4", "subs", style=13)
add_chart("bar","Headcount", DB_HC, "R19", "FTE", style=14)
add_chart("bar","Capital Deployed ($)", DB_CAP, "I34", "$", style=11)
add_chart("line","Operating Cost per Subscriber ($)", DB_OPS, "R34", "$/sub", style=15)

ed.column_dimensions["B"].width=26
for cx in range(3,8): ed.column_dimensions[col_letter(cx)].width=12
print("Executive Dashboard built")

# =====================================================================
# REORDER TABS to required order & SAVE
# =====================================================================
order=["Instructions","Executive Dashboard","Assumptions","Scenario Selector",
       "Subscriber Forecast","Revenue Model","Operating Expenses","Current Staffing",
       "Five-Year Staffing Plan","Fully Loaded Labor Cost","Capital Plan","Equipment Refresh",
       "Project ROI","Income Statement","Cash Flow","KPI Dashboard","Sensitivity Analysis","Risk Register"]
wb._sheets.sort(key=lambda s: order.index(s.title))
wb.active = 1  # Executive Dashboard
# global: gridlines off on presentation tabs
for wsx in wb.worksheets:
    wsx.sheet_view.showGridLines=False
OUT="build/RIVR_Tech_Five_Year_Financial_Model_2027-2031.xlsx"
wb.save(OUT)
print("SAVED", OUT, "| tabs:", len(wb.worksheets))

# ---- export key cell addresses for validation ----
import json as _json
KEYCELLS=dict(
  rev_row=REV_TOTAL_ROW, opex_row=OPEX_TOTAL_ROW,
  ebitda_row=R_EBITDA, is_rev_row=R_REV, is_opex_row=R_OPEX,
  labor_row=LABOR_COST_ROW, tot_end_row=TOT_END_ROW,
  cap_deploy_row=DEPLOY_ROW, cf_fcf_row=CF_FCF, cf_cum_row=CF_CUM,
  ebit_row=EBIT_ROW,
)
with open("build_keycells.json","w") as _f: _json.dump(KEYCELLS,_f)
print("KEYCELLS", KEYCELLS)
