"""Build RIVR_Tech_Five_Year_Executive_Presentation_2027-2031.pptx"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
import model

R = {k: model.compute(k) for k in ["base","conservative","aggressive"]}
B = R["base"]; fb=B["financials"]; kb=B["kpi"]; capb=B["capital"]
YEARS=[str(y) for y in model.YEARS]
NAVY=RGBColor(0x1F,0x3B,0x4D); TEAL=RGBColor(0x2E,0x7D,0x8A)
GREY=RGBColor(0x60,0x60,0x60); WHITE=RGBColor(0xFF,0xFF,0xFF)
LT=RGBColor(0xF2,0xF6,0xFA); ACCENT=RGBColor(0xE1,0x8A,0x2B); GREEN=RGBColor(0x2E,0x7D,0x5A)

prs=Presentation()
prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
SW,SH=prs.slide_width,prs.slide_height
BLANK=prs.slide_layouts[6]

def money_m(x): return f"${x/1e6:,.1f}M"
def pct(x): return f"{x*100:.0f}%"
def num(x): return f"{x:,.0f}"

def slide():
    return prs.slides.add_slide(BLANK)
def rect(s,l,t,w,h,color):
    sh=s.shapes.add_shape(1,l,t,w,h); sh.fill.solid(); sh.fill.fore_color.rgb=color
    sh.line.fill.background(); sh.shadow.inherit=False; return sh
def txt(s,l,t,w,h,text,size=18,color=NAVY,bold=False,align=PP_ALIGN.LEFT,italic=False,font="Calibri",anchor=MSO_ANCHOR.TOP):
    tb=s.shapes.add_textbox(l,t,w,h); tf=tb.text_frame; tf.word_wrap=True
    tf.vertical_anchor=anchor
    p=tf.paragraphs[0]; p.alignment=align
    r=p.add_run(); r.text=text; f=r.font; f.size=Pt(size); f.bold=bold; f.italic=italic
    f.color.rgb=color; f.name=font
    return tb
def bullets(s,l,t,w,h,items,size=16,color=NAVY,gap=6):
    tb=s.shapes.add_textbox(l,t,w,h); tf=tb.text_frame; tf.word_wrap=True
    for i,(lead,rest) in enumerate(items):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.space_after=Pt(gap); p.alignment=PP_ALIGN.LEFT
        rb=p.add_run(); rb.text="▸ "+lead; rb.font.size=Pt(size); rb.font.bold=True; rb.font.color.rgb=TEAL; rb.font.name="Calibri"
        if rest:
            rr=p.add_run(); rr.text=rest; rr.font.size=Pt(size); rr.font.color.rgb=color; rr.font.name="Calibri"
    return tb
def header(s,title,kicker=None):
    rect(s,0,0,SW,Inches(1.15),NAVY)
    rect(s,0,Inches(1.15),SW,Inches(0.06),TEAL)
    txt(s,Inches(0.5),Inches(0.24),Inches(12),Inches(0.75),title,size=26,color=WHITE,bold=True,anchor=MSO_ANCHOR.MIDDLE)
    if kicker:
        txt(s,Inches(0.5),Inches(0.02),Inches(12),Inches(0.3),kicker,size=11,color=RGBColor(0x9E,0xC3,0xCC),bold=True)
def footer(s,n):
    txt(s,Inches(0.5),Inches(7.05),Inches(9),Inches(0.35),
        "RIVR Tech · LREMC Technologies, LLC · Five-Year Plan FY2027–FY2031 · CONFIDENTIAL",
        size=9,color=GREY)
    txt(s,Inches(12.3),Inches(7.05),Inches(0.8),Inches(0.35),str(n),size=10,color=GREY,align=PP_ALIGN.RIGHT)
def tile(s,l,t,w,h,label,value,vcolor=NAVY):
    rect(s,l,t,w,h,LT)
    rect(s,l,t,w,Inches(0.09),TEAL)
    txt(s,l+Inches(0.12),t+Inches(0.18),w-Inches(0.24),Inches(0.4),label,size=12,color=GREY,bold=True)
    txt(s,l+Inches(0.12),t+Inches(0.55),w-Inches(0.24),Inches(0.7),value,size=26,color=vcolor,bold=True)
def add_chart(s,ctype,l,t,w,h,cats,series,legend=False,colors=None,numfmt=None):
    cd=CategoryChartData(); cd.categories=cats
    for nm,vals in series: cd.add_series(nm,vals)
    gf=s.shapes.add_chart(ctype,l,t,w,h,cd); ch=gf.chart
    ch.has_title=False
    if legend:
        ch.has_legend=True; ch.legend.position=XL_LEGEND_POSITION.BOTTOM; ch.legend.include_in_layout=False
        ch.legend.font.size=Pt(10)
    else: ch.has_legend=False
    try:
        plot=ch.plots[0]; plot.has_data_labels=False
        cats_ax=ch.category_axis; cats_ax.tick_labels.font.size=Pt(10)
        val_ax=ch.value_axis; val_ax.tick_labels.font.size=Pt(9)
        if numfmt: val_ax.tick_labels.number_format=numfmt; val_ax.tick_labels.number_format_is_linked=False
    except Exception: pass
    if colors:
        for i,ser in enumerate(ch.series):
            try: ser.format.fill.solid(); ser.format.fill.fore_color.rgb=colors[i%len(colors)]
            except Exception: pass
    return ch

N=[0]
def pg(): N[0]+=1; return N[0]

# ================= SLIDE 1 TITLE =================
s=slide()
rect(s,0,0,SW,SH,NAVY)
rect(s,0,Inches(4.15),SW,Inches(0.08),TEAL)
txt(s,Inches(0.9),Inches(2.0),Inches(11.5),Inches(1.2),"RIVR Tech",size=58,color=WHITE,bold=True)
txt(s,Inches(0.95),Inches(3.15),Inches(11.5),Inches(0.6),"LREMC Technologies, LLC",size=22,color=RGBColor(0x9E,0xC3,0xCC))
txt(s,Inches(0.95),Inches(4.35),Inches(11.5),Inches(0.7),"Five-Year Business Plan  ·  FY2027–FY2031",size=26,color=WHITE,bold=True)
txt(s,Inches(0.95),Inches(5.2),Inches(11.5),Inches(0.5),"Fiber-Optic Broadband for Southeastern North Carolina",size=16,color=RGBColor(0xC9,0xDA,0xEA),italic=True)
txt(s,Inches(0.95),Inches(6.5),Inches(11.5),Inches(0.5),"Prepared for the CEO, Executive Leadership Team & Board of Directors  ·  July 2026",size=12,color=GREY)

# ================= SLIDE 2 STRATEGIC VISION =================
s=slide(); n=pg(); header(s,"Strategic Vision","WHERE WE ARE GOING")
bullets(s,Inches(0.6),Inches(1.5),Inches(7.4),Inches(5),[
 ("Mission — ","Grow RIVR Tech into a financially sustainable regional broadband provider for southeastern North Carolina."),
 ("Reliability first — ","Maintain ≥99.85% availability with redundancy, monitoring, and a funded lifecycle-refresh program."),
 ("Disciplined capital — ","Deploy $10M/yr against demand-led, ROI-gated projects; hold reserves rather than force spend."),
 ("Move up-market — ","Grow higher-ARPU business, enterprise, and wholesale fiber alongside residential."),
 ("Community & tribal partnerships — ","Extend fiber to unserved and underserved areas, leveraging grants."),
],size=16,gap=14)
tile(s,Inches(8.4),Inches(1.6),Inches(4.3),Inches(1.4),"2031 revenue target",money_m(fb["revenue"][-1]),TEAL)
tile(s,Inches(8.4),Inches(3.2),Inches(4.3),Inches(1.4),"2031 subscribers",num(B["subs_total"]["end"][-1]),NAVY)
tile(s,Inches(8.4),Inches(4.8),Inches(4.3),Inches(1.4),"2031 EBITDA margin",pct(fb["ebitda_margin"][-1]),GREEN)
footer(s,n)

# ================= SLIDE 3 CURRENT POSITION =================
s=slide(); n=pg(); header(s,"Current Operating Position","STARTING POINT — JUNE 2026")
for i,(lab,val,c) in enumerate([
    ("Internet subscribers","4,686",NAVY),("Voice subscribers","502",NAVY),
    ("Residential ARPU","$74",TEAL),("Business ARPU","$149",TEAL)]):
    tile(s,Inches(0.6+i*3.05),Inches(1.5),Inches(2.85),Inches(1.35),lab,val,c)
for i,(lab,val,c) in enumerate([
    ("Filled positions","15",NAVY),("Open positions","3",ACCENT),
    ("Authorized positions","18",NAVY),("Counties served","4 +",TEAL)]):
    tile(s,Inches(0.6+i*3.05),Inches(3.1),Inches(2.85),Inches(1.35),lab,val,c)
txt(s,Inches(0.6),Inches(4.85),Inches(12),Inches(1.8),
    "Supplied figures are treated as management-provided and unaudited. RIVR Tech source files were "
    "not available; all projections rest on these inputs plus clearly-labeled assumptions and "
    "placeholders. Product-line subscriber splits, ARPU detail, passings, and labor rates are the "
    "top placeholders to replace with actuals.",size=13,color=GREY,italic=True)
footer(s,n)

# ================= SLIDE 4 FIVE-YEAR GOALS =================
s=slide(); n=pg(); header(s,"Five-Year Goals (Base Case)","THE PLAN AT A GLANCE")
cats=YEARS
add_chart(s,XL_CHART_TYPE.COLUMN_CLUSTERED,Inches(0.6),Inches(1.5),Inches(6.1),Inches(3.1),
    cats,[("Revenue",[round(x) for x in fb["revenue"]])],colors=[TEAL],numfmt='$#,##0,,"M"')
txt(s,Inches(0.6),Inches(4.6),Inches(6.1),Inches(0.4),"Revenue ($)",size=12,color=GREY,bold=True,align=PP_ALIGN.CENTER)
add_chart(s,XL_CHART_TYPE.LINE_MARKERS,Inches(6.9),Inches(1.5),Inches(6.0),Inches(3.1),
    cats,[("Subscribers",[B["subs_total"]["end"][i] for i in range(5)])],colors=[NAVY],numfmt='#,##0')
txt(s,Inches(6.9),Inches(4.6),Inches(6.0),Inches(0.4),"Ending subscribers",size=12,color=GREY,bold=True,align=PP_ALIGN.CENTER)
tile(s,Inches(0.6),Inches(5.25),Inches(3.0),Inches(1.4),"Revenue 2027→2031",f"{money_m(fb['revenue'][0])}→{money_m(fb['revenue'][-1])}",TEAL)
tile(s,Inches(3.75),Inches(5.25),Inches(3.0),Inches(1.4),"EBITDA margin",f"{pct(fb['ebitda_margin'][0])}→{pct(fb['ebitda_margin'][-1])}",GREEN)
tile(s,Inches(6.9),Inches(5.25),Inches(3.0),Inches(1.4),"Subscribers",f"{num(B['subs_total']['end'][0])}→{num(B['subs_total']['end'][-1])}",NAVY)
tile(s,Inches(10.05),Inches(5.25),Inches(2.7),Inches(1.4),"Headcount",f"18→{num(B['labor']['headcount'][-1])}",NAVY)
footer(s,n)

# ================= SLIDE 5 CAPITAL PLAN =================
s=slide(); n=pg(); header(s,"$50 Million Capital Plan","$10M PER YEAR · DISCIPLINED DEPLOYMENT")
# top categories
alloc=capb["alloc"]
top=sorted(alloc.items(), key=lambda kv:-kv[1])[:6]
cats_c=[k.split(". ",1)[1][:22] for k,_ in top]
add_chart(s,XL_CHART_TYPE.BAR_CLUSTERED,Inches(0.6),Inches(1.5),Inches(6.4),Inches(4.6),
    cats_c[::-1],[("5-yr $",[round(v*5) for _,v in top][::-1])],colors=[TEAL],numfmt='$#,##0,,"M"')
txt(s,Inches(0.6),Inches(6.15),Inches(6.4),Inches(0.4),"Top capital categories — 5-year $",size=11,color=GREY,bold=True,align=PP_ALIGN.CENTER)
bullets(s,Inches(7.3),Inches(1.6),Inches(5.5),Inches(4.6),[
 ("$50.0M over five years — ","$10.0M available each year across 16 categories."),
 (f"{money_m(sum(fb['capex']))} deployed — ","balance held as reserve/carryforward; full spend not forced."),
 ("Revenue-generating plant first — ","FTTH, distribution, backbone, business/enterprise ≈ 52%."),
 ("Grant matching fully funded — ","leverages external capital into unserved areas."),
 ("ROI-gated, demand-led — ","every project cleared on payback and take-rate thresholds."),
],size=15,gap=12)
footer(s,n)

# ================= SLIDE 6 EQUIPMENT REFRESH =================
s=slide(); n=pg(); header(s,"$2 Million Equipment-Refresh Plan","LIFECYCLE DISCIPLINE")
tile(s,Inches(0.6),Inches(1.6),Inches(3.8),Inches(1.5),"Per year","$400,000",TEAL)
tile(s,Inches(4.6),Inches(1.6),Inches(3.8),Inches(1.5),"Over five years","$2,000,000",TEAL)
tile(s,Inches(8.6),Inches(1.6),Inches(4.1),Inches(1.5),"Treatment","Inside $10M (adjustable)",NAVY)
bullets(s,Inches(0.6),Inches(3.5),Inches(12),Inches(3),[
 ("Committed, not scaled — ","the refresh is fixed at $400K every year and is never reduced by deployment pace."),
 ("No double-counting — ","in the base model it sits inside the $10M; an adjustable setting funds it outside (+$400K/yr)."),
 ("What it covers — ","core/aggregation, OLT optics, field test gear, splicing tools, fleet tools, servers/storage, security appliances, and an aged-ONT swap pool."),
 ("Why it matters — ","prevents aging-plant failures, emergency capital spend, and the churn that follows outages."),
],size=15,gap=14)
footer(s,n)

# ================= SLIDE 7 SUBSCRIBER & REVENUE GROWTH =================
s=slide(); n=pg(); header(s,"Subscriber & Revenue Growth","BASE CASE")
add_chart(s,XL_CHART_TYPE.COLUMN_STACKED,Inches(0.6),Inches(1.5),Inches(6.2),Inches(4.4),YEARS,
   [("Residential",[B["subs"]["res"][i]["end"] for i in range(5)]),
    ("Business",[B["subs"]["biz"][i]["end"] for i in range(5)]),
    ("Enterprise",[B["subs"]["ent"][i]["end"] for i in range(5)])],
   legend=True,colors=[NAVY,TEAL,ACCENT],numfmt='#,##0')
txt(s,Inches(0.6),Inches(5.95),Inches(6.2),Inches(0.4),"Ending subscribers by segment",size=11,color=GREY,bold=True,align=PP_ALIGN.CENTER)
add_chart(s,XL_CHART_TYPE.COLUMN_CLUSTERED,Inches(7.1),Inches(1.5),Inches(5.7),Inches(4.4),YEARS,
   [("EBITDA",[round(x) for x in fb["ebitda"]])],colors=[GREEN],numfmt='$#,##0,,"M"')
txt(s,Inches(7.1),Inches(5.95),Inches(5.7),Inches(0.4),"EBITDA ($)",size=11,color=GREY,bold=True,align=PP_ALIGN.CENTER)
footer(s,n)

# ================= SLIDE 8 STAFFING =================
s=slide(); n=pg(); header(s,"Staffing Requirements","TRIGGER-BASED HIRING")
add_chart(s,XL_CHART_TYPE.COLUMN_CLUSTERED,Inches(0.6),Inches(1.5),Inches(6.0),Inches(4.4),
   ["2026"]+YEARS,[("Headcount",[18]+B["labor"]["headcount"])],colors=[NAVY],numfmt='#,##0')
txt(s,Inches(0.6),Inches(5.95),Inches(6.0),Inches(0.4),"Total headcount (EOY)",size=11,color=GREY,bold=True,align=PP_ALIGN.CENTER)
bullets(s,Inches(7.0),Inches(1.6),Inches(5.8),Inches(4.6),[
 ("Fill 3 vacancies first — ","1 sales rep + 2 fiber technicians in Year 1."),
 ("Hire on triggers, not dates — ","subscribers, installs/month, tickets/tech, fiber miles, projects, span of control."),
 ("2027 — ","Network Engineer, NOC Technician, Fiber Splicers."),
 ("2028–29 — ","sales, support, install/repair, enterprise sales, inspector, GIS."),
 ("2030–31 — ","OSP supervisor, marketing, Customer Experience Manager, data analyst."),
 (f"18 → {num(B['labor']['headcount'][-1])} by 2031 — ","fully-loaded labor costing throughout."),
],size=14,gap=10)
footer(s,n)

# ================= SLIDE 9 FINANCIAL OUTLOOK =================
s=slide(); n=pg(); header(s,"Financial Outlook","BASE CASE — $ MILLIONS")
rows=[("Revenue",fb["revenue"]),("Operating expense",fb["opex"]),("EBITDA",fb["ebitda"]),
      ("Capital expenditures",fb["capex"]),("Free cash flow (pre-fin.)",fb["fcf"])]
# table
from pptx.util import Cm
tbl=s.shapes.add_table(len(rows)+1,6,Inches(0.6),Inches(1.5),Inches(8.0),Inches(3.6)).table
tbl.cell(0,0).text=""
for j,y in enumerate(YEARS):
    c=tbl.cell(0,j+1); c.text=y
for i,(lab,vals) in enumerate(rows):
    tbl.cell(i+1,0).text=lab
    for j,v in enumerate(vals): tbl.cell(i+1,j+1).text=money_m(v)
for r in range(len(rows)+1):
    for c in range(6):
        cell=tbl.cell(r,c)
        for p in cell.text_frame.paragraphs:
            p.alignment=PP_ALIGN.LEFT if c==0 else PP_ALIGN.RIGHT
            for run in p.runs:
                run.font.size=Pt(11); run.font.name="Calibri"
                if r==0: run.font.bold=True; run.font.color.rgb=WHITE
                else: run.font.color.rgb=NAVY
        if r==0: cell.fill.solid(); cell.fill.fore_color.rgb=NAVY
        elif r%2==0: cell.fill.solid(); cell.fill.fore_color.rgb=LT
        else: cell.fill.solid(); cell.fill.fore_color.rgb=WHITE
tile(s,Inches(9.0),Inches(1.6),Inches(3.7),Inches(1.05),"EBITDA-positive","Every year",GREEN)
tile(s,Inches(9.0),Inches(2.75),Inches(3.7),Inches(1.05),"Peak cash need",money_m(min(fb["cum_cash"])),ACCENT)
tile(s,Inches(9.0),Inches(3.9),Inches(3.7),Inches(1.05),"Funding envelope","$50M (ample)",TEAL)
txt(s,Inches(0.6),Inches(5.4),Inches(12),Inches(1.4),
    "Break-even: EBITDA-positive from Year 1. Free cash flow is negative during the fiber build and is "
    "funded within the $50M capital program; FCF break-even follows beyond the plan horizon — the "
    "expected profile for an expanding fiber operator.",size=13,color=GREY,italic=True)
footer(s,n)

# ================= SLIDE 10 SCENARIO COMPARISON =================
s=slide(); n=pg(); header(s,"Scenario Comparison","CONSERVATIVE · BASE · AGGRESSIVE")
def sm(key):
    Rk=R[key]; f=Rk["financials"]
    return dict(rev=sum(f["revenue"]),ebitda=sum(f["ebitda"]),marg=f["ebitda"][-1]/f["revenue"][-1],
                capex=sum(f["capex"]),end=Rk["subs_total"]["end"][-1],emp=Rk["labor"]["headcount"][-1])
C,BS,A=sm("conservative"),sm("base"),sm("aggressive")
tbl=s.shapes.add_table(7,4,Inches(0.6),Inches(1.5),Inches(7.6),Inches(4.6)).table
data=[["5-Year metric","Conservative","Base","Aggressive"],
 ["Total revenue",money_m(C["rev"]),money_m(BS["rev"]),money_m(A["rev"])],
 ["Total EBITDA",money_m(C["ebitda"]),money_m(BS["ebitda"]),money_m(A["ebitda"])],
 ["EBITDA margin (2031)",pct(C["marg"]),pct(BS["marg"]),pct(A["marg"])],
 ["Capital deployed",money_m(C["capex"]),money_m(BS["capex"]),money_m(A["capex"])],
 ["Ending subscribers",num(C["end"]),num(BS["end"]),num(A["end"])],
 ["Ending employees",num(C["emp"]),num(BS["emp"]),num(A["emp"])]]
for r in range(7):
    for c in range(4):
        cell=tbl.cell(r,c); cell.text=data[r][c]
        for p in cell.text_frame.paragraphs:
            p.alignment=PP_ALIGN.LEFT if c==0 else PP_ALIGN.CENTER
            for run in p.runs:
                run.font.size=Pt(12); run.font.name="Calibri"
                if r==0: run.font.bold=True; run.font.color.rgb=WHITE
                elif c==2: run.font.bold=True; run.font.color.rgb=NAVY
                else: run.font.color.rgb=NAVY
        if r==0: cell.fill.solid(); cell.fill.fore_color.rgb=NAVY
        elif c==2: cell.fill.solid(); cell.fill.fore_color.rgb=RGBColor(0xE2,0xEF,0xDA)
        elif r%2==0: cell.fill.solid(); cell.fill.fore_color.rgb=LT
        else: cell.fill.solid(); cell.fill.fore_color.rgb=WHITE
txt(s,Inches(8.5),Inches(1.6),Inches(4.3),Inches(4.4),"",size=12)
bullets(s,Inches(8.5),Inches(1.6),Inches(4.3),Inches(4.6),[
 ("Base is recommended — ","balances growth with capital discipline."),
 ("Conservative — ","tests slower take-up and higher cost; margins thin."),
 ("Aggressive — ","faster build lifts EBITDA to ~38% but strains hiring & CAC."),
 ("All three — ","stay within the $50M funding envelope."),
],size=13,gap=12)
footer(s,n)

# ================= SLIDE 11 PRINCIPAL RISKS =================
s=slide(); n=pg(); header(s,"Principal Risks","SCORED · OWNED · MITIGATED")
risks=[("Construction-cost inflation","High","CFO / Dir OSP"),
 ("Grant compliance / clawback","High","CFO / Grants Mgr"),
 ("Subscriber growth below forecast","High","VP Sales"),
 ("Cybersecurity & network outages","High","IT / CISO / NOC"),
 ("Workforce shortages","High","COO / HR"),
 ("Pole-attachment & permitting delays","Medium","Dir OSP"),
 ("Cash-flow timing","Medium","CFO"),
 ("Overbuilding low-take areas","Medium","CEO / CFO")]
tbl=s.shapes.add_table(len(risks)+1,3,Inches(0.6),Inches(1.5),Inches(12.1),Inches(4.6)).table
tbl.cell(0,0).text="Risk"; tbl.cell(0,1).text="Tier"; tbl.cell(0,2).text="Owner"
for i,(rk,tier,owner) in enumerate(risks):
    tbl.cell(i+1,0).text=rk; tbl.cell(i+1,1).text=tier; tbl.cell(i+1,2).text=owner
for r in range(len(risks)+1):
    for c in range(3):
        cell=tbl.cell(r,c)
        for p in cell.text_frame.paragraphs:
            p.alignment=PP_ALIGN.LEFT if c!=1 else PP_ALIGN.CENTER
            for run in p.runs:
                run.font.size=Pt(12); run.font.name="Calibri"
                if r==0: run.font.bold=True; run.font.color.rgb=WHITE
                else:
                    run.font.color.rgb=NAVY
                    if c==1 and run.text=="High": run.font.color.rgb=ACCENT; run.font.bold=True
        if r==0: cell.fill.solid(); cell.fill.fore_color.rgb=NAVY
        elif r%2==0: cell.fill.solid(); cell.fill.fore_color.rgb=LT
        else: cell.fill.solid(); cell.fill.fore_color.rgb=WHITE
txt(s,Inches(0.6),Inches(6.25),Inches(12),Inches(0.5),
    "Full 19-risk register with probability × impact scoring on the Excel 'Risk Register' tab.",
    size=11,color=GREY,italic=True)
footer(s,n)

# ================= SLIDE 12 YEAR 1 PRIORITIES =================
s=slide(); n=pg(); header(s,"Year 1 Priorities (2027)","EXECUTE THE FOUNDATION")
bullets(s,Inches(0.6),Inches(1.5),Inches(6.1),Inches(5),[
 ("Fill the 3 vacancies — ","1 sales rep + 2 fiber technicians."),
 ("Capital governance — ","finalize allocation governance & the ROI gate."),
 ("Equipment refresh — ","establish the $400K schedule & lifecycle standards."),
 ("Construction priorities — ","set prioritization criteria for the build."),
 ("KPI reporting — ","stand up monthly KPI reporting from the model."),
],size=15,gap=12)
bullets(s,Inches(6.9),Inches(1.5),Inches(6.0),Inches(5),[
 ("Hiring triggers — ","publish the trigger framework for future roles."),
 ("Quarterly forecasts — ","begin quarterly forecast updates."),
 ("Project ROI reviews — ","launch project-level ROI review."),
 ("Lifecycle standards — ","adopt equipment replacement standards."),
 ("Board cadence — ","Year-1 KPI review to the Board each quarter."),
],size=15,gap=12)
footer(s,n)

# ================= SLIDE 13 DECISIONS REQUIRED =================
s=slide(); n=pg(); header(s,"Decisions Required from Leadership","THE ASK")
bullets(s,Inches(0.7),Inches(1.6),Inches(12),Inches(4.8),[
 ("1. Adopt the Base Case ","as the operating plan for FY2027–FY2031."),
 ("2. Approve the $50M capital allocation ","and the capital-governance / ROI-gate process."),
 ("3. Authorize the equipment-refresh program ","at $400K/yr ($2M / 5yr) and lifecycle standards."),
 ("4. Approve trigger-based staffing ","— fill 3 vacancies now; add roles as triggers are met."),
 ("5. Endorse the KPI & forecast disciplines ","— monthly KPIs, quarterly forecasts, project ROI reviews."),
 ("6. Direct data collection ","to replace placeholders (subscriber split, ARPU, passings, labor rates, plant/depreciation, grant terms)."),
],size=17,gap=16)
rect(s,Inches(0.7),Inches(6.35),Inches(11.9),Inches(0.7),LT)
txt(s,Inches(0.9),Inches(6.45),Inches(11.5),Inches(0.5),
    "Minimum to justify the investment: ≈9,700+ subscribers and ≥$12M revenue by 2031, 2031 EBITDA margin ≥22%.",
    size=13,color=NAVY,bold=True,anchor=MSO_ANCHOR.MIDDLE)
footer(s,n)

# ================= SLIDE 14 CLOSING =================
s=slide(); n=pg()
rect(s,0,0,SW,SH,NAVY)
rect(s,0,Inches(3.6),SW,Inches(0.08),TEAL)
txt(s,Inches(0.9),Inches(2.4),Inches(11.5),Inches(1.0),"Building RIVR Tech's Fiber Future",size=36,color=WHITE,bold=True)
txt(s,Inches(0.95),Inches(3.8),Inches(11.5),Inches(0.8),
    f"{money_m(fb['revenue'][-1])} revenue · {pct(fb['ebitda_margin'][-1])} EBITDA margin · {num(B['subs_total']['end'][-1])} subscribers by 2031",
    size=20,color=RGBColor(0x9E,0xC3,0xCC))
txt(s,Inches(0.95),Inches(5.0),Inches(11.5),Inches(0.6),"Disciplined $50M build · $2M lifecycle refresh · trigger-based staffing",size=15,color=RGBColor(0xC9,0xDA,0xEA))
txt(s,Inches(0.95),Inches(6.6),Inches(11.5),Inches(0.5),"Companion files: Excel financial model + Word business plan  ·  CONFIDENTIAL",size=11,color=GREY)

prs.save("build/RIVR_Tech_Five_Year_Executive_Presentation_2027-2031.pptx")
print("PPTX SAVED. slides:", len(prs.slides._sldIdLst))
