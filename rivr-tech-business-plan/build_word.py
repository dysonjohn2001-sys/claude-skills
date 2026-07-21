"""Build RIVR_Tech_Five_Year_Business_Plan_2027-2031.docx"""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import model

R = {k: model.compute(k) for k in ["base","conservative","aggressive"]}
B = R["base"]
YEARS = model.YEARS
NAVY = RGBColor(0x1F,0x3B,0x4D)
TEAL = RGBColor(0x2E,0x7D,0x8A)
GREY = RGBColor(0x60,0x60,0x60)
LTGREY = "F2F6FA"; NAVYHEX="1F3B4D"; BANDHEX="E9EFF4"

def money(x, dec=0):
    return f"${x:,.{dec}f}" if x>=0 else f"(${abs(x):,.{dec}f})"
def money_m(x):
    return f"${x/1e6:,.1f}M"
def pct(x, dec=1):
    return f"{x*100:.{dec}f}%"
def num(x):
    return f"{x:,.0f}"

doc = Document()

# base styles
st = doc.styles["Normal"]
st.font.name = "Calibri"; st.font.size = Pt(10.5)
st.paragraph_format.space_after = Pt(6)

def set_cell_bg(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'),'clear'); shd.set(qn('w:color'),'auto'); shd.set(qn('w:fill'),hexcolor)
    tcPr.append(shd)

def set_cell_text(cell, text, *, bold=False, color=None, size=9.5, align=None, white=False):
    cell.text = ""
    p = cell.paragraphs[0]
    if align: p.alignment = align
    run = p.add_run(str(text)); run.font.size = Pt(size); run.bold = bold
    run.font.name = "Calibri"
    if white: run.font.color.rgb = RGBColor(0xFF,0xFF,0xFF)
    elif color: run.font.color.rgb = color
    p.paragraph_format.space_after = Pt(2); p.paragraph_format.space_before = Pt(2)

def add_table(headers, rows, colwidths=None, first_col_left=True, total_row=False, band=True, fontsize=9.5):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = "Table Grid"
    hdr = t.rows[0].cells
    for i,h in enumerate(headers):
        set_cell_bg(hdr[i], NAVYHEX)
        set_cell_text(hdr[i], h, bold=True, white=True, size=fontsize,
                      align=WD_ALIGN_PARAGRAPH.CENTER if i>0 or not first_col_left else WD_ALIGN_PARAGRAPH.LEFT)
    for ri,row in enumerate(rows):
        cells = t.add_row().cells
        is_tot = total_row and ri==len(rows)-1
        for ci,val in enumerate(row):
            if band and (ri%2==1) and not is_tot: set_cell_bg(cells[ci], LTGREY)
            if is_tot: set_cell_bg(cells[ci], BANDHEX)
            align = WD_ALIGN_PARAGRAPH.LEFT if (ci==0 and first_col_left) else WD_ALIGN_PARAGRAPH.RIGHT
            set_cell_text(cells[ci], val, bold=is_tot, size=fontsize, align=align)
    if colwidths:
        for row in t.rows:
            for ci,w in enumerate(colwidths):
                row.cells[ci].width = Inches(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t

def h1(text):
    p = doc.add_heading(level=1)
    r = p.add_run(text); r.font.color.rgb = NAVY; r.font.size = Pt(16); r.font.name="Calibri"
    return p
def h2(text):
    p = doc.add_heading(level=2)
    r = p.add_run(text); r.font.color.rgb = TEAL; r.font.size = Pt(12.5); r.font.name="Calibri"
    return p
def h3(text):
    p = doc.add_heading(level=3)
    r = p.add_run(text); r.font.color.rgb = NAVY; r.font.size = Pt(11); r.font.name="Calibri"; r.bold=True
    return p
def para(text, italic=False, size=10.5, color=None, space=6):
    p = doc.add_paragraph()
    r = p.add_run(text); r.italic=italic; r.font.size=Pt(size)
    if color: r.font.color.rgb=color
    p.paragraph_format.space_after=Pt(space)
    return p
def bullet(text, bold_lead=None):
    p = doc.add_paragraph(style="List Bullet")
    if bold_lead:
        r=p.add_run(bold_lead); r.bold=True
        p.add_run(text)
    else:
        p.add_run(text)
    p.paragraph_format.space_after=Pt(3)
    return p
def callout(text):
    t=doc.add_table(rows=1,cols=1); t.style="Table Grid"
    c=t.rows[0].cells[0]; set_cell_bg(c,"FBE9D6")
    set_cell_text(c,text,size=9.5,color=RGBColor(0x8A,0x4B,0x00))
    doc.add_paragraph().paragraph_format.space_after=Pt(2)

YRH = [str(y) for y in YEARS]

# ============================= COVER =============================
for _ in range(3): doc.add_paragraph()
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run("RIVR TECH"); r.bold=True; r.font.size=Pt(40); r.font.color.rgb=NAVY
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run("LREMC Technologies, LLC"); r.font.size=Pt(15); r.font.color.rgb=TEAL
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run("Five-Year Business Plan  ·  FY2027–FY2031"); r.font.size=Pt(18); r.bold=True
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run("Fiber-Optic Broadband for Southeastern North Carolina"); r.font.size=Pt(12); r.italic=True; r.font.color.rgb=GREY
for _ in range(6): doc.add_paragraph()
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run("Prepared for the Chief Executive Officer, Executive Leadership Team, and Board of Directors")
r.font.size=Pt(11); r.font.color.rgb=NAVY
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run("Prepared: July 21, 2026  ·  Version 1.0"); r.font.size=Pt(10); r.font.color.rgb=GREY
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run("CONFIDENTIAL — Contains management assumptions and clearly-labeled placeholders")
r.font.size=Pt(9); r.italic=True; r.font.color.rgb=GREY
doc.add_page_break()

# ============================= TOC =============================
h1("Table of Contents")
para("This document is organized into the sections below. To refresh page numbers in "
     "Microsoft Word, select the table and press F9.", italic=True, size=9.5, color=GREY)
toc_p = doc.add_paragraph()
run = toc_p.add_run()
fldChar = OxmlElement('w:fldChar'); fldChar.set(qn('w:fldCharType'),'begin')
instrText = OxmlElement('w:instrText'); instrText.set(qn('xml:space'),'preserve')
instrText.text = 'TOC \\o "1-2" \\h \\z \\u'
fldChar2 = OxmlElement('w:fldChar'); fldChar2.set(qn('w:fldCharType'),'separate')
t2 = OxmlElement('w:t'); t2.text = "Right-click and Update Field to populate the table of contents."
fldChar3 = OxmlElement('w:fldChar'); fldChar3.set(qn('w:fldCharType'),'end')
run._r.append(fldChar); run._r.append(instrText); run._r.append(fldChar2); run._r.append(t2); run._r.append(fldChar3)
doc.add_page_break()

print("cover+toc done")

# convenience arrays (base)
fb=B["financials"]; kb=B["kpi"]; capb=B["capital"]
def row5(vals, fmt): return [fmt(v) for v in vals]

# ============================= 1 EXECUTIVE SUMMARY =============================
h1("1. Executive Summary")
para("RIVR Tech (LREMC Technologies, LLC) is a fiber-optic broadband provider serving Robeson, "
     "Hoke, Scotland, Cumberland, and surrounding counties in southeastern North Carolina. This "
     "five-year business plan (FY2027–FY2031) integrates strategy, network expansion, staffing, "
     "operations, revenue, operating expense, capital investment, and financial performance into a "
     "single, board-ready plan.")
callout("Data integrity: This plan incorporates RIVR Tech's actual Q2-2026 financial results "
        "(quarter ended 6/30/2026, from the Board of Directors deck) as the baseline — operating "
        "revenue, the full expense structure, depreciation, interest, grant income, and grant awards. "
        "Forward projections build on that actual baseline plus clearly-labeled assumptions. Actual "
        "data, management assumptions, calculated projections, and recommended targets are "
        "distinguished throughout. Subscriber counts, ARPU, and labor rates remain partly estimated; "
        "see the Source-Data Inventory & Assumption Log for the conflict log and remaining placeholders.")
h3("The plan at a glance (Base Case)")
add_table(
 ["Metric","2027","2028","2029","2030","2031"],
 [ ["Ending subscribers (internet)"]+row5(B["subs_total"]["end"], num),
   ["Total revenue"]+row5(fb["revenue"], money_m),
   ["EBITDA"]+row5(fb["ebitda"], money_m),
   ["EBITDA margin"]+row5(fb["ebitda_margin"], pct),
   ["Capital deployed"]+row5(fb["capex"], money_m),
   ["Headcount (EOY)"]+row5(B["labor"]["headcount"], num),
 ],
 colwidths=[2.4,1.0,1.0,1.0,1.0,1.0])
para("Over the plan, the Base Case grows the internet subscriber base from roughly 4,800 at the "
     f"start of 2027 to {num(B['subs_total']['end'][-1])} by year-end 2031, lifts revenue from "
     f"{money_m(fb['revenue'][0])} to {money_m(fb['revenue'][-1])}, and expands EBITDA margin from "
     f"{pct(fb['ebitda_margin'][0])} to {pct(fb['ebitda_margin'][-1])}. The company is EBITDA-positive "
     "in every year of the plan.")
h3("Capital and funding")
bullet(" $10.0M available each year and $50.0M over five years, deployed against 16 capital categories.", bold_lead="Capital program:")
bullet(f" The Base Case deploys {money_m(sum(fb['capex']))} of the {money_m(50e6)} available "
       f"({pct(sum(fb['capex'])/50e6)}), holding the balance as reserve/carryforward rather than "
       "forcing full deployment.", bold_lead="Discipline:")
bullet(" $400,000 per year and $2.0M over five years, treated as part of the $10M in the base model, "
       "with an adjustable setting to fund it outside the $10M.", bold_lead="Equipment refresh:")
bullet(f" Free cash flow before financing is negative during the build (cumulative cash requirement "
       f"peaks near {money_m(min(fb['cum_cash']))}), comfortably inside the $50M funding envelope. "
       "The business funds a heavy fiber build; FCF turns positive beyond the plan horizon.",
       bold_lead="Cash requirement:")
h3("What leadership is asked to approve")
bullet(" Adopt the Base Case as the operating plan.")
bullet(" Approve the five-year capital allocation and capital-governance process.")
bullet(" Authorize filling the three open positions and the trigger-based five-year staffing plan.")
bullet(" Endorse the KPI, forecast-update, and project-ROI disciplines in Section 12.")
doc.add_page_break()

# ============================= 2 COMPANY OVERVIEW =============================
h1("2. Company Overview")
add_table(["Item","Detail"],
 [["Legal entity","LREMC Technologies, LLC"],
  ["Trade name","RIVR Tech"],
  ["Business","Fiber-optic internet, voice, business & enterprise connectivity, managed Wi-Fi, and related broadband services"],
  ["Primary service area","Robeson, Hoke, Scotland, Cumberland, and surrounding counties, southeastern North Carolina"],
  ["Network model","Fiber-to-the-home, business fiber, enterprise circuits, middle-mile fiber, and grant-funded expansion"],
  ["Starting internet subscribers","4,686 (June 2026 month-end) — supplied, unaudited"],
  ["Starting voice subscribers","502 (June 2026 month-end) — supplied, unaudited"],
  ["Starting workforce","15 filled + 3 open = 18 authorized positions"]],
 colwidths=[2.0,4.8], band=True)
para("RIVR Tech operates as the broadband subsidiary of Lumbee River EMC, giving it operational "
     "maturity, community trust, and existing plant. Its strategic objective is to grow into a "
     "financially sustainable regional broadband provider while maintaining strong service "
     "reliability, customer experience, and disciplined capital deployment.")
h2("Current financial position (Q2-2026 actual)")
bl = model.BASELINE_2026
para("Actual results for the quarter ended June 30, 2026 (annualized on a year-to-date basis) "
     "establish the plan's baseline:")
add_table(["Financial baseline (annualized YTD)","Amount"],
 [["Total operating revenue", money(bl["total_op_revenue"])],
  ["Total operating expense (excl. D&A)", money(bl["total_op_expense_ex_da"])],
  ["EBITDA (operating income + D&A)", money(bl["ebitda"])],
  ["Depreciation & amortization", money(bl["da"])],
  ["Operating income (loss)", money(bl["operating_income"])],
  ["Interest expense (existing debt)", money(-bl["interest_expense"])],
  ["Grant income (nonoperating)", money(bl["grant_income"])],
  ["Net income (grant-supported)", money(bl["net_income"])]],
 colwidths=[3.6,2.0])
para("RIVR Tech currently operates at roughly EBITDA break-even (a slight operating loss) on about "
     "$4.1M of annualized revenue, and is net-income-positive because of substantial grant funding. "
     "The five-year plan's central task is to scale subscribers and revenue to durable EBITDA "
     "profitability while managing existing debt service (~$0.46M/yr interest).", size=10, space=6)
h2("Grant awards")
para(f"RIVR Tech has been awarded approximately {money_m(bl['grant_total_awarded'])} in construction "
     "grants that fund network expansion into unserved and underserved areas:")
add_table(["Grant program","Award"],
 [["CAB 2.0 — Hoke County", "$3,295,657"],
  ["CAB 2.0 — Scotland County", "$1,932,610"],
  ["CAB 2.0 — Robeson County", "$3,116,391"],
  ["NC Stop GAP (Hoke/Scotland/Robeson)", "$2,812,776 ($1.6M reimbursed)"],
  ["BTAP (engineering grant)", "$419,000"],
  ["Total identified awards", money(bl["grant_total_awarded"])]],
 colwidths=[3.6,2.0], total_row=True)
para("Grant construction reimbursement offsets a meaningful share of the capital program and is "
     "modeled as a nonoperating funding source; more than $2M of underground new-build has been "
     "identified as eligible for reimbursement.", size=9.5, italic=True, color=GREY)

# ============================= 3 STRATEGIC OBJECTIVES =============================
h1("3. Strategic Objectives")
objs=[("Sustainable growth", f"Grow the internet base to ~{num(B['subs_total']['end'][-1])} by 2031 while holding churn low and lifting EBITDA margin above 25%."),
 ("Disciplined capital deployment","Deploy the $10M/yr program against demand-led, ROI-gated projects; hold reserves rather than force spend."),
 ("Network reliability","Maintain ≥99.85% availability through redundancy, monitoring, and a funded lifecycle-refresh program."),
 ("Customer experience","Shorten installation intervals, reduce repeat trouble tickets, and protect retention."),
 ("Financial sustainability","Reach EBITDA self-sufficiency for operations while the capital program funds expansion; converge toward free-cash-flow breakeven beyond the plan."),
 ("Community & tribal partnerships","Extend service to unserved and underserved areas, leveraging grants and local partnerships including the Lumbee community.")]
for t,d in objs: bullet(" "+d, bold_lead=t+": ")
doc.add_page_break()

# ============================= 4 MARKET & GROWTH STRATEGY =============================
h1("4. Market & Growth Strategy")
para("RIVR Tech competes primarily against DSL, fixed wireless, and incumbent cable in a rural and "
     "semi-rural footprint where fiber remains underbuilt. The company's advantages are reliability, "
     "local service, and symmetrical fiber speeds. Growth is driven by (1) extending the fiber "
     "footprint (new passings), (2) converting passings to subscribers (take rate), and (3) expanding "
     "higher-ARPU business and enterprise revenue.")
h2("Passings, take rate, and penetration")
add_table(["Driver","2027","2028","2029","2030","2031"],
 [["Homes & businesses passed"]+row5(kb["total_pass"], num),
  ["New passings added"]+row5(kb["new_pass"], num),
  ["Ending subscribers"]+row5(B["subs_total"]["end"], num),
  ["Take rate"]+row5(kb["take_rate"], pct),
  ["Blended ARPU (recurring)"]+row5(kb["arpu_blended"], lambda x:money(x,2))],
 colwidths=[2.4,1.0,1.0,1.0,1.0,1.0])
para("Note: take rate dips modestly mid-plan because new passings are added faster than newly-passed "
     "homes are converted — a normal lag during a heavy build. Penetration on maturing plant is a "
     "primary Year 3+ growth lever and a core focus of the sales strategy.", italic=True, size=9.5, color=GREY)
h2("Growth strategy pillars")
bullet(" Sequence construction to demand and grant availability; gate each project on ROI and take-rate thresholds.", bold_lead="Build where demand is: ")
bullet(" Fund door-to-door and digital campaigns on newly-passed plant; add residential sales capacity as passings grow.", bold_lead="Convert faster: ")
bullet(" Grow business fiber, enterprise/DIA circuits, and wholesale/dark-fiber revenue at higher ARPU and margin.", bold_lead="Move up-market: ")
bullet(" Use grant-funded builds to extend into unserved areas with external capital leverage.", bold_lead="Leverage grants: ")
doc.add_page_break()
print("sections 1-4 done")

# ============================= 5 CAPITAL PLAN =============================
h1("5. Capital Plan")
para(f"The capital program provides {money_m(10e6)} per year and {money_m(50e6)} over five years, "
     "allocated across 16 categories. The plan does not force full deployment: capital is deployed "
     "against demand-led, ROI-gated projects, and any balance is held as reserve or carryforward.")
h2("Five-year capital allocation by category (base allocation)")
alloc = capb["alloc"]; cat5 = capb["cat_5yr"]
rows=[]
for k,v in alloc.items():
    rows.append([k, money(v), money(cat5[k]), pct(v/10e6)])
rows.append(["TOTAL", money(sum(alloc.values())), money(sum(cat5.values())), pct(1.0)])
add_table(["Capital category","Annual $","5-Yr $","% of $10M"], rows,
          colwidths=[3.3,1.15,1.15,0.9], total_row=True, fontsize=9)
h2("Annual deployment, reserve, and cumulative (base case)")
add_table(["Capital","2027","2028","2029","2030","2031"],
 [["Available"]+row5(capb["avail"], money_m),
  ["Deployed"]+row5(capb["deployed"], money_m),
  ["Uncommitted (reserve/carryforward)"]+row5(capb["uncommitted"], money),
  ["Cumulative deployed"]+row5(capb["cum_deployed"], money_m)],
 colwidths=[2.6,0.95,0.95,0.95,0.95,0.95])
para("Each category in the Excel model carries a business purpose, expected operational benefit, "
     "expected revenue/cost impact, recommended timing, key dependency, responsible executive, and a "
     "depreciation-period placeholder. Depreciation periods are placeholders pending a fixed-asset "
     "study.", italic=True, size=9.5, color=GREY)
callout("The $10.0M annual allocation reconciles exactly (check cell = 0). The equipment-refresh "
        "program (category 15) is fixed at $400,000/yr and $2.0M over five years and is not scaled by "
        "deployment pace, preventing double-counting.")
doc.add_page_break()

# ============================= 6 EQUIPMENT-REFRESH PLAN =============================
h1("6. Equipment-Refresh Plan")
para("A funded lifecycle-refresh program replaces aging core, access, test, fleet, IT, and security "
     "equipment on a scheduled basis, preventing emergency capital spend and the churn that accompanies "
     "aging-plant failures.")
add_table(["Parameter","Value"],
 [["Annual refresh budget","$400,000"],
  ["Five-year refresh budget","$2,000,000"],
  ["Base-model treatment","Part of the $10M annual allocation (category 15)"],
  ["Adjustable-model treatment","Outside the $10M (+$400K/yr) — toggle on the Excel Scenario Selector"],
  ["Governance","Annual refresh schedule set against equipment-lifecycle standards"]],
 colwidths=[2.4,4.4])
para("The Excel 'Equipment Refresh' tab distributes the $400,000 across core/aggregation, OLT optics, "
     "field test equipment, splicing gear, fleet tools, servers/storage, security appliances, and an "
     "aged-ONT swap pool, with each line carrying a depreciation-period placeholder. Every year totals "
     "exactly $400,000 (check cell = 0).", size=9.5, color=GREY, italic=True)
doc.add_page_break()

# ============================= 7 STAFFING PLAN =============================
h1("7. Staffing Plan")
h2("Current staffing (actual)")
add_table(["Position","Filled","Open","Authorized"],
 [["Chief Operations Officer","1","0","1"],
  ["Director of Outside Plant","1","0","1"],
  ["Supervisors","2","0","2"],
  ["Project Coordinators","2","0","2"],
  ["Sales Coordinator","1","0","1"],
  ["Sales Representatives","3","1","4"],
  ["Fiber Technicians","5","2","7"],
  ["TOTAL","15","3","18"]],
 colwidths=[3.0,1.1,1.1,1.3], total_row=True)
para("A fully-loaded labor-cost method is used throughout (base wage plus overtime, incentive, "
     "payroll taxes, benefits, workers' compensation, training, uniforms/PPE, tools, and recruiting), "
     "not salary alone. Wage rates are editable placeholders pending actual payroll data.")
h2("Five-year staffing plan — trigger-based hiring")
para("Positions are added when measurable business triggers are met, not on fixed calendar dates. "
     "The Excel 'Five-Year Staffing Plan' tab details each role's responsibilities, reason, hiring "
     "trigger, expected benefit, and the risk of not adding it.")
add_table(["Recommended role","Yr","#","Primary trigger"],
 [["Network Engineer","2027","1","Subs >6,000 or 3+ OLT sites"],
  ["NOC Technician","2027","1","Trouble tickets >8 / tech / day"],
  ["Fiber Splicers","2027","2","Fiber-mile build threshold"],
  ["Residential Sales Reps","2028","2","New passings >4,000/yr"],
  ["Customer Support Reps","2028","2","Subs >7,500 / calls per agent"],
  ["Additional Project Coordinator","2028","1","Active projects >6 concurrent"],
  ["Fiber Install/Repair Techs","2028","3","Install interval >10 days"],
  ["Enterprise Sales Rep","2029","1","Qualified enterprise pipeline"],
  ["Construction Inspector","2029","1","Grant-funded miles active"],
  ["GIS / Mapping Specialist","2029","1","Passings >18,000"],
  ["Additional OSP Supervisor","2030","1","Field FTEs/supervisor >8"],
  ["Marketing Specialist","2030","1","Marketing spend >$0.3M/yr"],
  ["Customer Experience Manager","2030","1","Subs >10,000"],
  ["Data Analyst","2031","1","Mature monthly KPI program"],
  ["Warehouse & Inventory Specialist","2031","1","Multiple warehouses"]],
 colwidths=[2.6,0.6,0.5,3.1], fontsize=9)
para(f"Headcount grows from 18 authorized today to {num(B['labor']['headcount'][-1])} by 2031 (base "
     "case), tracked against subscriber and construction triggers. Hiring triggers include total "
     "subscribers, installs/month, tickets per technician, fiber miles, active projects, business/"
     "enterprise revenue, service levels, install interval, overtime, span of control, and support volume.")
h2("Organizational charts")
para("Current structure (2026): COO → Director of Outside Plant → (2 Supervisors, 2 Project "
     "Coordinators, Fiber Technicians); Sales Coordinator → Sales Representatives.")
para("Proposed 2031 structure: COO oversees (a) Network Engineering & NOC, (b) Outside Plant "
     "(2 supervisors, splicers, inspectors, install/repair techs, GIS), (c) Sales & Marketing "
     "(residential + enterprise reps, marketing specialist), (d) Customer Experience & Support, and "
     "(e) Business Operations (project coordinators, data analyst, warehouse/inventory, fleet/"
     "facilities, administrative support). Detailed org charts are provided in Appendix C.")
doc.add_page_break()
print("sections 5-7 done")

# ============================= 8 OPERATIONS PLAN =============================
h1("8. Operations Plan")
para("Operations center on three disciplines: build (construction and splicing), connect (installation "
     "and provisioning), and sustain (maintenance, monitoring, and restoration). The plan funds a NOC "
     "capability, a preventive-maintenance program, and equipment-lifecycle standards.")
h2("Operating-expense structure")
oxb = B["opex"]
add_table(["Expense group","2027","2028","2029","2030","2031"],
 [["Direct cost of service"]+row5(oxb["groups"]["direct"], money_m),
  ["Network operations"]+row5(oxb["groups"]["netops"], money_m),
  ["Sales & marketing"]+row5(oxb["groups"]["sm"], money_m),
  ["General & administrative"]+row5(oxb["groups"]["ga"], money_m),
  ["TOTAL OPERATING EXPENSE"]+row5(oxb["total"], money_m)],
 colwidths=[2.6,0.95,0.95,0.95,0.95,0.95], total_row=True)
h2("Cost behavior and unit economics")
add_table(["Metric","2027","2028","2029","2030","2031"],
 [["Fixed expense"]+row5(oxb["behavior"]["fixed"], money_m),
  ["Variable expense"]+row5(oxb["behavior"]["variable"], money_m),
  ["Semi-variable expense"]+row5(oxb["behavior"]["semivar"], money_m),
  ["Operating cost per subscriber ($/yr)"]+row5(kb["opex_per_sub"], lambda x:money(x)),
  ["Operating expense per revenue dollar"]+row5(kb["opex_per_rev"], lambda x:f"{x:.3f}")],
 colwidths=[2.8,0.9,0.9,0.9,0.9,0.9])
para(f"Operating cost per subscriber falls from about {money(kb['opex_per_sub'][0])} to "
     f"~{money(kb['opex_per_sub'][-1])} as fixed costs are spread over a larger base — the core scale "
     "story of the plan. The operating-expense model is built up from the Q2-2026 actual income-"
     "statement categories (COGS, LREMC intercompany, engineering & operations, marketing, sales & "
     "customer support, G&A, accounting, HR, IT, taxes), each grown on subscriber, headcount, "
     "inflation, and revenue drivers, and classified Fixed / Variable / Semi-variable and Direct / "
     "S&M / NetOps / G&A on the Excel 'Operating Expenses' tab.", size=9.5, italic=True, color=GREY)
h2("Service and reliability targets")
add_table(["Operational KPI","2027","2031 target"],
 [["Network availability","99.85%","≥99.85%"],
  ["Average installation interval","9 days","6 days"],
  ["Trouble-ticket repeat rate","9.0%","6.0%"],
  ["Overtime as % of labor","10%","7%"],
  ["Subscribers per technician",num(kb["subs_per_tech"][0]),num(kb["subs_per_tech"][-1])]],
 colwidths=[3.0,1.9,1.9])
doc.add_page_break()

# ============================= 9 SALES & MARKETING PLAN =============================
h1("9. Sales & Marketing Plan")
para("The commercial engine converts newly-passed plant into paying subscribers and grows higher-ARPU "
     "business and enterprise revenue. Customer-acquisition cost is tracked per gross add and held in a "
     "disciplined band.")
add_table(["Sales & marketing metric","2027","2028","2029","2030","2031"],
 [["Gross additions (internet)"]+row5(B["subs_total"]["gross"], num),
  ["Customer acquisition cost (CAC)"]+row5(kb["cac"], lambda x:money(x)),
  ["Marketing & advertising"]+row5(oxb["cat"]["Marketing & advertising"], money),
  ["Sales & customer support"]+row5(oxb["cat"]["Sales & customer support"], money)],
 colwidths=[2.6,0.95,0.95,0.95,0.95,0.95])
h2("Commercial priorities")
bullet(" Fund door-to-door and digital campaigns timed to newly-passed neighborhoods; add residential sales capacity as passings grow.", bold_lead="Residential: ")
bullet(" Add an enterprise sales representative in 2029 to grow business fiber, dedicated internet access, and wholesale/dark-fiber revenue.", bold_lead="Business & enterprise: ")
bullet(" Bundle managed Wi-Fi, static IP, and voice to lift ARPU and retention.", bold_lead="Attach & bundle: ")
bullet(" Stand up retention programs and a Customer Experience Manager (2030) to protect the base as it scales.", bold_lead="Retention: ")
doc.add_page_break()

# ============================= 10 FIVE-YEAR FINANCIAL SUMMARY =============================
h1("10. Five-Year Financial Summary")
para("The base-case financials below flow from the Excel model, built up from the Q2-2026 actual "
     "baseline. EBITDA turns positive in 2027 and scales; GAAP net income is pressured in later years "
     "by rising depreciation on the expanding $50M plant (a non-cash charge) — EBITDA is the "
     "operating-health metric during the build.")
add_table(["$ (Base Case)","2027","2028","2029","2030","2031"],
 [["Revenue"]+row5(fb["revenue"], money_m),
  ["Operating expense"]+row5(fb["opex"], money_m),
  ["EBITDA"]+row5(fb["ebitda"], money_m),
  ["EBITDA margin"]+row5(fb["ebitda_margin"], pct),
  ["Depreciation & amortization"]+row5(fb["depreciation"], money_m),
  ["Operating income (loss)"]+row5(fb["op_income"], money_m),
  ["Interest expense"]+row5([-x for x in fb["interest"]], money_m),
  ["Grant income (nonoperating)"]+row5(fb["grant_income"], money_m),
  ["Net income (loss)"]+row5(fb["net_income"], money_m),
  ["Capital expenditures"]+row5(fb["capex"], money_m),
  ["Free cash flow (pre-financing)"]+row5(fb["fcf"], money_m),
  ["Grant capital reimbursement"]+row5(fb["grant_capital"], money_m),
  ["Cumulative cash requirement"]+row5(fb["cum_cash"], money_m)],
 colwidths=[2.6,0.95,0.95,0.95,0.95,0.95], fontsize=9)
h2("Capital funding reconciliation")
add_table(["$","2027","2028","2029","2030","2031"],
 [["Capital funding available"]+row5(fb["cap_avail"], money_m),
  ["Capital funding used"]+row5(fb["cap_used"], money_m),
  ["Capital funding remaining"]+row5(fb["cap_remaining"], money)],
 colwidths=[2.6,0.95,0.95,0.95,0.95,0.95])
h2("Key financial and operational KPIs")
add_table(["KPI","2027","2028","2029","2030","2031"],
 [["Revenue per employee"]+row5(kb["rev_per_emp"], lambda x:money(x)),
  ["EBITDA per subscriber ($/yr)"]+row5(kb["ebitda_per_sub"], lambda x:money(x)),
  ["Revenue per passing"]+row5(kb["rev_per_pass"], lambda x:money(x)),
  ["Capital cost per new customer"]+row5(kb["capex_per_net"], lambda x:money(x)),
  ["Blended ARPU (recurring, $/mo)"]+row5(kb["arpu_blended"], lambda x:money(x,2))],
 colwidths=[2.6,0.95,0.95,0.95,0.95,0.95], fontsize=9)
h2("Break-even analysis")
bullet(" The current position is roughly EBITDA break-even (a slight operating loss). The Base Case "
       "crosses to positive EBITDA in 2027 and scales the margin to the mid-20s% by 2031.", bold_lead="EBITDA break-even: ")
bullet(" GAAP net income is positive early (grant-supported) but is pressured in later years by "
       "rising, non-cash depreciation on the growing $50M plant. This is expected during a heavy "
       "fiber build; the business is funded by the capital program and grant reimbursement.", bold_lead="Net income: ")
bullet(" Reached beyond the five-year horizon; sustained fiber-build capital and interest exceed "
       "EBITDA during the plan. Grant reimbursement (~$1.5–2.5M/yr) offsets a meaningful share of capex.", bold_lead="Free-cash-flow break-even: ")
doc.add_page_break()
print("sections 8-10 done")

# ============================= 11 SCENARIO ANALYSIS =============================
h1("11. Scenario Analysis")
para("Three complete scenarios bracket the plan. The Base Case is the recommended operating plan; "
     "the Conservative and Aggressive cases stress the drivers in each direction.")
def scen_metrics(key):
    Rk=R[key]; f=Rk["financials"]
    beg0=Rk["subs_total"]["beg"][0]; end5=Rk["subs_total"]["end"][-1]
    net=end5-beg0
    return dict(rev=sum(f["revenue"]), opex=sum(f["opex"]), ebitda=sum(f["ebitda"]),
                marg=f["ebitda"][-1]/f["revenue"][-1], capex=sum(f["capex"]),
                end=end5, emp=Rk["labor"]["headcount"][-1], fcf=sum(f["fcf"]),
                cap_per_net=sum(f["capex"])/net if net else 0)
cons=scen_metrics("conservative"); base=scen_metrics("base"); aggr=scen_metrics("aggressive")
add_table(["5-Year metric","Conservative","Base","Aggressive"],
 [["Total revenue", money_m(cons["rev"]), money_m(base["rev"]), money_m(aggr["rev"])],
  ["Total operating expense", money_m(cons["opex"]), money_m(base["opex"]), money_m(aggr["opex"])],
  ["Total EBITDA", money_m(cons["ebitda"]), money_m(base["ebitda"]), money_m(aggr["ebitda"])],
  ["EBITDA margin (2031)", pct(cons["marg"]), pct(base["marg"]), pct(aggr["marg"])],
  ["Capital deployed", money_m(cons["capex"]), money_m(base["capex"]), money_m(aggr["capex"])],
  ["Ending subscribers (2031)", num(cons["end"]), num(base["end"]), num(aggr["end"])],
  ["Ending employees (2031)", num(cons["emp"]), num(base["emp"]), num(aggr["emp"])],
  ["Free cash flow (5-yr, pre-financing)", money_m(cons["fcf"]), money_m(base["fcf"]), money_m(aggr["fcf"])],
  ["Capital cost per net new sub", money(cons["cap_per_net"]), money(base["cap_per_net"]), money(aggr["cap_per_net"])]],
 colwidths=[2.8,1.35,1.35,1.35])
h2("Scenario assumptions and major risks")
bullet(" Slower subscriber growth, lower take rate, higher churn, higher construction cost, slower "
       "capital deployment, greater opex pressure. Risk: revenue undershoot pressures margins and "
       "capital efficiency (cost per net sub ~$12,200).", bold_lead="Conservative: ")
bullet(" Realistic management forecast; disciplined annual capital deployment; moderate subscriber and "
       "revenue growth; staffing added as triggers are reached.", bold_lead="Base: ")
bullet(" Faster construction, higher take rate, lower churn, faster hiring, higher acquisition expense, "
       "greater business/enterprise growth. Risk: execution and hiring strain, higher upfront CAC.",
       bold_lead="Aggressive: ")
h2("Sensitivity analysis")
para("The Excel 'Sensitivity Analysis' tab flexes each driver individually against Year-5 EBITDA "
     "(exact where the relationship is linear; contribution-margin approximations are labeled). "
     "Drivers tested: ARPU, churn, take rate, construction cost per passing, new subscribers per "
     "month, labor cost, and annual capital deployment. ARPU and churn are the highest-leverage "
     "levers on EBITDA; construction cost per passing and capital-deployment pace most affect how "
     "much footprint the $50M program builds.")
doc.add_page_break()

# ============================= 12 RISK REGISTER =============================
h1("12. Risk Register")
para("Each risk is scored on probability and impact (1–5 each; score 1–25) with a named owner and "
     "mitigation. Tiers: High ≥16, Medium 9–15, Low <9. The full register is on the Excel 'Risk "
     "Register' tab.")
RISKS=[
("Construction-cost inflation",4,4,"CFO / Dir OSP","Fixed-price contracts; contingency reserve"),
("Grant compliance / clawback",3,5,"CFO / Grants Mgr","Compliance calendar; inspector; audit readiness"),
("Workforce shortages",4,4,"COO / HR","Trigger-based hiring; apprenticeships; retention"),
("Subscriber growth below forecast",3,5,"VP Sales","Take-rate campaigns; pace capex to demand"),
("Cybersecurity breach",3,5,"IT / CISO","Defense-in-depth; MFA; IR plan; security capex"),
("Network outages",3,5,"NOC / Dir OSP","Redundancy; generators; restoration reserve"),
("Cash-flow timing",3,4,"CFO","Capital governance; reserves; milestone billing"),
("Pole-attachment delays",4,3,"Dir OSP","Early applications; make-ready tracking"),
("Overbuilding low-take areas",3,4,"CEO / CFO","Demand-led builds; ROI gate per project"),
("Competitive pricing / overbuild",3,4,"CEO / VP Sales","Differentiate on reliability & local service"),
]
rows=[]
for name,p,im,owner,mit in RISKS:
    sc=p*im; tier="High" if sc>=16 else ("Medium" if sc>=9 else "Low")
    rows.append([name,str(p),str(im),str(sc),tier,owner,mit])
add_table(["Risk","P","I","Score","Tier","Owner","Mitigation"], rows,
          colwidths=[1.9,0.35,0.35,0.55,0.7,1.35,1.9], fontsize=8.5)
para("Table shows the ten highest-priority risks; the Excel register covers all 19 risk categories "
     "including material availability, contractor performance, churn, technology obsolescence, "
     "equipment failure, regulatory change, permitting delays, customer concentration, and vendor "
     "concentration.", italic=True, size=9.5, color=GREY)
doc.add_page_break()
print("sections 11-12 done")

# ============================= 13 STRATEGIC INITIATIVES =============================
h1("13. Strategic Initiatives")
para("Prioritized initiatives, each with an owner, timeline, estimated cost, expected benefit, success "
     "metric, risk, and dependency. Costs are planning estimates (placeholders).")
INIT=[
("Residential subscriber growth","VP Sales","2027-2031","Take rate ↑ to 40%+","New passings, retention"),
("Business & enterprise sales","VP Sales / Eng","2027-2031","Higher-ARPU B2B revenue","Enterprise sales hire"),
("Network expansion","Dir OSP","Continuous","New passings per plan","Permitting, make-ready"),
("Grant-funded construction","CFO / Grants","Per award","External capital leverage","Grant awards"),
("Customer retention","CX Manager","2028+","Lower churn / higher NRR","CX hire, systems"),
("Installation-cycle reduction","Field Ops","2027-2029","Interval 9→6 days","Install techs, WFM"),
("Preventive maintenance","Dir OSP","Continuous","Fewer outages","Maintenance program"),
("Equipment lifecycle mgmt","COO / Net Eng","Annual","Avoid emergency capex","Refresh funding"),
("Workforce development","COO / HR","Continuous","Retention, productivity","Training budget"),
("Automation & systems integration","CIO / COO","2027-2030","Lower cost/sub","OSS/BSS capital"),
("Cybersecurity & disaster recovery","IT / CISO","2027+","Risk reduction","Security capital"),
("Wholesale fiber monetization","VP Sales / Eng","2028+","Incremental transport revenue","Backbone capacity"),
("Community & tribal partnerships","CEO","Continuous","Access & goodwill","Local relationships"),
]
add_table(["Initiative","Owner","Timeline","Expected benefit","Key dependency"],
 [[a,b,c,d,e] for a,b,c,d,e in INIT], colwidths=[2.1,1.2,1.0,1.5,1.4], fontsize=8.5)
doc.add_page_break()

# ============================= 14 IMPLEMENTATION ROADMAP =============================
h1("14. Implementation Roadmap")
h2("Year 1 (2027) — quarterly")
add_table(["Quarter","Priorities"],
 [["Q1 2027","Fill 1 sales rep + 2 fiber technician openings; finalize capital-allocation governance; "
   "establish the $400K equipment-refresh schedule; stand up monthly KPI reporting."],
  ["Q2 2027","Implement construction-prioritization criteria; create hiring triggers; begin quarterly "
   "forecast updates; hire Network Engineer / NOC Technician per triggers."],
  ["Q3 2027","Launch project-level ROI review; establish equipment-lifecycle and replacement standards; "
   "scale residential sales on newly-passed plant."],
  ["Q4 2027","First annual capital-governance review; assess triggers for 2028 hires; refresh forecast; "
   "report Year-1 KPIs to the Board."]],
 colwidths=[1.1,5.7])
h2("Years 2–5 — annual")
add_table(["Year","Focus"],
 [["2028","Scale residential sales and support; add project coordinator and install/repair techs on triggers; grow business fiber."],
  ["2029","Add enterprise sales, construction inspector, and GIS specialist; push penetration on maturing plant; grow wholesale."],
  ["2030","Add OSP supervisor, marketing specialist, and Customer Experience Manager; harden retention; optimize cost per sub."],
  ["2031","Add data analyst and warehouse/inventory specialist; consolidate margins above 27%; plan the next capital cycle."]],
 colwidths=[0.8,6.0])
doc.add_page_break()

# ============================= 15 MANAGEMENT RECOMMENDATIONS =============================
h1("15. Management Recommendations")
h2("Recommended base-case strategy")
para(f"Adopt the Base Case: disciplined $10M/yr deployment, moderate subscriber and revenue growth, "
     f"trigger-based staffing, and EBITDA margin expansion from about {pct(fb['ebitda_margin'][0])} to "
     f"~{pct(fb['ebitda_margin'][-1])} — turning the current slight operating loss into a scaling, "
     "EBITDA-positive business. It balances growth with capital discipline and stays within the $50M "
     "funding envelope, supported by substantial grant awards.")
h2("Recommended five-year capital allocation")
para("Weight capital toward revenue-generating plant — fiber-to-the-home (~24%), distribution (~13%), "
     "backbone (~8%), and business/enterprise (~7%) — while fully funding grant matching (~10%), the "
     "equipment refresh ($400K/yr), and a capital contingency reserve. Deploy against ROI-gated, "
     "demand-led projects and hold uncommitted capital rather than force spend.")
h2("Recommended pace of network expansion")
para(f"Add roughly 3,300–4,800 new passings per year (front-loaded), reaching about "
     f"{num(kb['total_pass'][-1])} homes and businesses passed by 2031, sequenced to demand and grant "
     "availability.")
h2("Staffing additions needed to support growth")
para(f"Grow from 18 authorized positions to about {num(B['labor']['headcount'][-1])} by 2031, led by "
     "network engineering/NOC, splicing, field install/repair, residential and enterprise sales, "
     "customer experience/support, and GIS/data — each gated on a measurable trigger.")
h2("Minimum performance required to justify the investment")
bullet(f" Reach at least ~{num(int(B['subs_total']['end'][-1]*0.85))} internet subscribers by 2031 "
       "(≈85% of base-case target).", bold_lead="Subscribers: ")
bullet(f" Achieve at least ~{money_m(fb['revenue'][-1]*0.85)} of 2031 revenue and hold 2031 EBITDA "
       "margin at or above 20%.", bold_lead="Revenue & margin: ")
bullet(" Keep total capital cost per net new subscriber near or below ~$8,000 on average over the "
       "plan (this metric includes all capital, not just plant).", bold_lead="Capital efficiency: ")
h2("Most important Year-1 decisions")
bullet(" Approve capital-allocation governance and the ROI gate for projects.")
bullet(" Fill the three open positions and ratify the hiring-trigger framework.")
bullet(" Commit to monthly KPI reporting and quarterly forecast updates.")
bullet(" Confirm the equipment-lifecycle standards and $400K refresh schedule.")
h2("Information management must provide to replace placeholders")
bullet(" Actual subscriber split (residential/business/enterprise) and product-line ARPU.")
bullet(" Actual homes/businesses passed and the grant-funded build footprint by year.")
bullet(" Fully-loaded labor rates, benefit loads, and workers'-comp class rates.")
bullet(" Transit, transport, pole-attachment, and voice-platform contract rates.")
bullet(" Existing net plant value and the fixed-asset depreciation schedule.")
bullet(" Grant award terms and any existing debt, lease, or financing obligations.")
h2("90-day action plan")
add_table(["Days","Action"],
 [["0–30","Approve the Base Case and capital governance; open recruiting for the 3 vacancies; stand up the KPI dashboard from the Excel model; assign placeholder-owners to collect actual data."],
  ["31–60","Finalize construction-prioritization and ROI-gate criteria; replace top-priority placeholders (subscriber split, ARPU, passings, labor rates) with actuals; issue the first monthly KPI report."],
  ["61–90","Complete Q1 hires; run the first quarterly forecast update in the model; present a refreshed plan and Year-1 milestones to the Board; lock equipment-lifecycle standards."]],
 colwidths=[0.9,5.9])
doc.add_page_break()

# ============================= 16 APPENDICES =============================
h1("16. Appendices")
h2("Appendix A — Data classification & assumption log")
para("All figures are tagged: [ACTUAL] supplied (unaudited), [ASSUMPTION] editable, [CALC] derived, "
     "[TARGET] recommended, [PLACEHOLDER] pending management input. No source-data conflicts were "
     "identified because no competing internal sources existed. See the accompanying Source-Data "
     "Inventory & Assumption Log and the Excel 'Assumptions' tab.")
h2("Appendix B — Companion files")
bullet(" RIVR_Tech_Five_Year_Financial_Model_2027-2031.xlsx — 18-tab formula-driven model with scenario selector.", bold_lead="Excel: ")
bullet(" RIVR_Tech_Five_Year_Executive_Presentation_2027-2031.pptx — board presentation.", bold_lead="PowerPoint: ")
h2("Appendix C — Organizational charts")
para("Current (2026): Chief Operations Officer at the top; Director of Outside Plant leads 2 "
     "Supervisors, 2 Project Coordinators, and 5 Fiber Technicians (+2 open); Sales Coordinator leads "
     "3 Sales Representatives (+1 open).")
para("Proposed (2031): Chief Operations Officer over five functions — Network Engineering & NOC; "
     "Outside Plant (supervisors, splicers, inspectors, install/repair techs, GIS); Sales & Marketing "
     "(residential + enterprise reps, marketing specialist); Customer Experience & Support; and "
     "Business Operations (project coordinators, data analyst, warehouse/inventory, fleet/facilities, "
     "administrative support).")
h2("Appendix D — Full KPI set")
add_table(["KPI","2027","2028","2029","2030","2031"],
 [["Beginning subscribers"]+row5(B["subs_total"]["beg"], num),
  ["Ending subscribers"]+row5(B["subs_total"]["end"], num),
  ["Gross additions"]+row5(B["subs_total"]["gross"], num),
  ["Net additions"]+row5(kb["net_add"], num),
  ["Homes & businesses passed"]+row5(kb["total_pass"], num),
  ["Take rate"]+row5(kb["take_rate"], pct),
  ["Subscribers per employee"]+row5(kb["subs_per_emp"], lambda x:f"{x:.0f}"),
  ["Subscribers per technician"]+row5(kb["subs_per_tech"], lambda x:f"{x:.0f}"),
  ["Capital cost per passing"]+row5(kb["capex_per_pass"], lambda x:money(x)),
  ["Customer acquisition cost"]+row5(kb["cac"], lambda x:money(x))],
 colwidths=[2.6,0.95,0.95,0.95,0.95,0.95], fontsize=9)

# footer with page numbers
sec = doc.sections[0]
footer = sec.footer
fp = footer.paragraphs[0]; fp.alignment=WD_ALIGN_PARAGRAPH.CENTER
run=fp.add_run("RIVR Tech — Five-Year Business Plan (FY2027–FY2031)  ·  CONFIDENTIAL  ·  Page ")
run.font.size=Pt(8); run.font.color.rgb=GREY
# PAGE field
fldc=OxmlElement('w:fldSimple'); fldc.set(qn('w:instr'),'PAGE')
fp._p.append(fldc)

doc.save("build/RIVR_Tech_Five_Year_Business_Plan_2027-2031.docx")
print("WORD SAVED. paragraphs:", len(doc.paragraphs), "tables:", len(doc.tables))
