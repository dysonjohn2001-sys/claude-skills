"""Builds Excel deliverables 02, 07, 08, 12, 13."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation
from style_helpers import (title, subtitle, header_row, cell, widths, legend,
    USD, USD0, PCT, NUM, NAVY, BLUE, YELLOW, ORANGE, LIGHT_BLUE, GREEN, RED, WHITE)

BASE = "/home/user/claude-skills/deliverables/RIVR-Tech-Lifeline-Lumbee/"

def status_dv():
    dv = DataValidation(type="list", formula1='"Not started,In progress,Blocked,Complete,N/A"', allow_blank=True)
    return dv
def rag_dv():
    return DataValidation(type="list", formula1='"Red,Amber,Green"', allow_blank=True)

def cover_sheet(wb, tnum, tname, note):
    ws = wb.active; ws.title = "Cover"; ws.sheet_view.showGridLines = False
    widths(ws, {"A": 3, "B": 95})
    title(ws, "B2", f"RIVR Tech — Lifeline & Lumbee Broadband Affordability", 16)
    title(ws, "B3", f"{tname}  (Deliverable {tnum})", 13)
    subtitle(ws, "B5", "LREMC Technologies, LLC d/b/a RIVR Tech")
    meta = [("B7","Owner:","Program Owner + noted functional owners"),
            ("B8","Version:","v0.1 — DRAFT (build phase, ETC application pending)"),
            ("B9","Source basis:","00_Regulatory_Source_Register.md (refs 'SR-x.y')"),
            ("B10","Status:","PRE-DECISION. Confirm all placeholder figures before reliance.")]
    for c,k,v in meta:
        ws[c] = f"{k}  {v}"; ws[c].font = Font(size=11)
    ws["B12"] = note; ws["B12"].alignment = Alignment(wrap_text=True, vertical="top")
    ws["B12"].font = Font(size=10, color=RED, bold=True); ws.row_dimensions[12].height = 80
    legend(ws, 15, col=2)
    return ws

# =====================================================================
# 02 — CURRENT PLAN & PRICING AUDIT
# =====================================================================
wb = Workbook()
cover_sheet(wb, "02", "Current Plan & Pricing Audit",
    "Speeds are confirmed (symmetrical fiber 250/500/1000). PRICES ARE NOT PUBLISHED — every price "
    "cell is a PLACEHOLDER to be replaced from RIVR Tech's confirmed price sheet. Do not rely on any "
    "price here until Finance/Product confirms and signs the 'Confirmed?' column.")

inv = wb.create_sheet("Plan Inventory")
inv.sheet_view.showGridLines = False
widths(inv, {"A":3,"B":22,"C":12,"D":12,"E":13,"F":11,"G":12,"H":12,"I":11,"J":30})
title(inv, "B2", "Current-State Residential Plan Inventory", 13)
subtitle(inv, "B3", "SR-8.2. Fill Price + Confirmed? from RIVR price sheet. Add business plans below.")
header_row(inv, 5, ["Plan / tier","Download","Upload","Data","Monthly price","Confirmed?","Promo price","Contract","Voice incl.?","Notes"], start_col=2)
plans = [
    ["Fiber 250 (entry)","250 Mbps","250 Mbps","Unlimited",None,"NO",None,"[TBD]","No","Current lowest tier"],
    ["Fiber 500","500 Mbps","500 Mbps","Unlimited",None,"NO",None,"[TBD]","No",""],
    ["Fiber 1 Gig","1000 Mbps","1000 Mbps","Unlimited",None,"NO",None,"[TBD]","No","Up to 2 Gbps referenced"],
    ["PROPOSED Senior 100/100","100 Mbps","100 Mbps","Unlimited","≈$10 target","N/A",None,"None (program)","Optional","NEW tier below entry"],
    ["(add business tiers)","","","",None,"NO",None,"","",""],
]
r = 6
for p in plans:
    for i, v in enumerate(p):
        col = chr(ord('B')+i)
        kind = "placeholder" if (i in (4,6) and v is None) else ("good" if "Senior" in str(p[0]) and i==0 else "grey")
        cell(inv, f"{col}{r}", v, kind, size=9, wrap=(i==9))
    r += 1
inv.add_data_validation(_dv := DataValidation(type="list", formula1='"YES,NO"', allow_blank=True))
_dv.add(f"G6:G{r-1}")
cell(inv, f"B{r+1}", "Voice service: unlimited calling offered; PRICE NOT PUBLISHED — obtain from RIVR (SR-8.5).", "grey", wrap=True, size=9)

eq = wb.create_sheet("Equipment & Fees")
eq.sheet_view.showGridLines = False
widths(eq, {"A":3,"B":30,"C":14,"D":12,"E":16,"F":40})
title(eq, "B2", "Equipment, Installation & Fees", 13)
header_row(eq, 4, ["Item","Charge","Confirmed?","Taxable? (TBD)","Note / source"], start_col=2)
eqrows = [
    ["Indoor Wi-Fi 6 router (rental)","$5.00/mo","NO","TBD — TPP rental likely (SR-9.4)","RIVR site; CONFLICTS w/ 'free rental' claim (SR-8.4)"],
    ["Outdoor mesh unit (rental)","$10.00/mo","NO","TBD (SR-9.4)","RIVR site"],
    ["Installation","Free ($99 value)","NO","TBD (SR-9.5)","Advertised promotional; confirm program policy"],
    ["Managed Wi-Fi ('Wi-Fi Pro')","[obtain]","NO","OPEN QUESTION (SR-9.6)","Fact-specific; tax advisor must rule"],
    ["Static IP / premium","[obtain]","NO","TBD","Exclude from Senior plan (premium)"],
    ["Voice add-on","[obtain]","NO","Voice taxable 7% (SR-9.3)","+911 $0.70/line, +USF (SR-9.7/9.8)"],
]
r = 5
for e in eqrows:
    for i, v in enumerate(e):
        col = chr(ord('B')+i)
        cell(eq, f"{col}{r}", v, "placeholder" if i in (1,3) else "grey", size=9, wrap=(i>=3))
    eq.row_dimensions[r].height = 26
    r += 1

pm = wb.create_sheet("Pricing Matrix")
pm.sheet_view.showGridLines = False
widths(pm, {"A":3,"B":34,"C":13,"D":13,"E":13,"F":13,"G":13,"H":15})
title(pm, "B2", "Per-Subscriber Pricing & Subsidy Matrix (mirrors Financial Model)", 12)
subtitle(pm, "B3", "Pre-tax. See 06_Financial_Model for live formulas. This tab is the printable summary.")
header_row(pm, 5, ["Line item ($/mo)","(1) Retail","(2) +Std LL","(3) +Tribal","(4) +RIVR disc","(5) +Tribe disc","(6) Senior $10"], start_col=2)
matrix = [
    ["Retail (list) price","69.95","69.95","69.95","55.00","55.00","55.00"],
    ["Less: Standard Lifeline credit","0.00","(9.25)","(9.25)","(9.25)","(9.25)","(9.25)"],
    ["Less: Tribal enhancement","0.00","0.00","(25.00)","0.00","0.00","0.00"],
    ["Less: RIVR-funded discount","0.00","0.00","0.00","(varies)","(varies)","(to $10)"],
    ["Less: Tribe-funded discount","0.00","0.00","0.00","0.00","(varies)","(varies)"],
    ["Equipment / mgd Wi-Fi","TBD","TBD","TBD","TBD","TBD","TBD"],
    ["Taxes & fees","TBD","TBD","TBD","TBD","TBD","TBD"],
    ["= Customer payment (pre-tax)","69.95","60.70","35.70","10.00","10.00","10.00"],
    ["USAC reimbursement to RIVR","0.00","9.25","34.25","9.25","9.25","9.25"],
]
r = 6
for m in matrix:
    for i, v in enumerate(m):
        col = chr(ord('B')+i)
        is_total = m[0].startswith("=")
        cell(pm, f"{col}{r}", v, "good" if is_total else ("grey" if i==0 else "calc"), size=9,
             bold=is_total)
    r += 1
cell(pm, f"B{r+1}", "ILLUSTRATIVE using $69.95/$55.00 placeholder retail. Scenario (3) applies ONLY where "
    "the residence is verified on qualifying Tribal lands (SR-4/SR-5) — currently expected 0 subscribers.",
    "placeholder", wrap=True, size=9)
pm.merge_cells(f"B{r+1}:H{r+2}")

disc = wb.create_sheet("Discrepancy Log")
disc.sheet_view.showGridLines = False
widths(disc, {"A":3,"B":36,"C":24,"D":24,"E":20,"F":16})
title(disc, "B2", "Conflicts & Discrepancies to Resolve", 12)
header_row(disc, 4, ["Discrepancy","Source A","Source B","Owner to resolve","Status"], start_col=2)
drows = [
    ["Router rental: 'free' vs $5/mo","RIVR site (free w/ plan)","RIVR site ($5/mo)","Product / Billing","Open"],
    ["Monthly plan prices not published","Website (no prices)","(none)","Product / Finance","Open"],
    ["Voice price not published","Website (unlimited, no $)","(none)","Product","Open"],
    ["NCUC ETC docket not found","Search (none found)","(none)","Reg. Counsel","Open"],
]
r = 5
disc.add_data_validation(sdv := status_dv());
for d in drows:
    for i, v in enumerate(d):
        col = chr(ord('B')+i)
        cell(disc, f"{col}{r}", v, "input" if i==4 else "grey", size=9, wrap=True)
    r += 1
sdv.add(f"F5:F{r-1}")
wb.save(BASE+"02_Current_Plan_and_Pricing_Audit.xlsx")
print("02 done")

# =====================================================================
# 07 — COMPLIANCE & AUDIT CHECKLIST
# =====================================================================
wb = Workbook()
cover_sheet(wb, "07", "Compliance & Audit Checklist",
    "Every row cites the governing rule (SR ref). 'Status' and 'Evidence' are for the Compliance "
    "Officer to complete. NO customer may be enrolled, and NO reimbursement claimed, until the "
    "onboarding rows are Complete and the final NCUC ETC order is in hand.")
ck = wb.create_sheet("Checklist")
ck.sheet_view.showGridLines = False
widths(ck, {"A":3,"B":6,"C":50,"D":18,"E":16,"F":14,"G":24,"H":14})
title(ck, "B2", "Lifeline Compliance & Audit Checklist", 13)
header_row(ck, 4, ["#","Requirement","Citation (SR ref)","Owner","Status","Evidence / doc link","Due"], start_col=2)
sections = {
 "A. ETC designation & USAC onboarding": [
    ["Final NCUC ETC designation order received","SR-6.1/SR-7.4","Reg. Counsel"],
    ["Confirmed ETC service area documented","SR-6.1/SR-7.1","Reg. Counsel"],
    ["FCC Registration Number (FRN) via CORES","SR-6.2","Finance"],
    ["SAM.gov UEI active + bank account","SR-6.3","Finance"],
    ["Study Area Code (SAC) issued by USAC","SR-6.4","Compliance"],
    ["498 ID / FCC Form 498 filed & officer-certified","SR-6.5","Finance/Officer"],
    ["RAD Rep IDs for all enrollment reps","SR-6.6","Compliance"],
    ["National Verifier access + roles provisioned","SR-6.7","Compliance/IT"],
    ["NLAD access + roles provisioned","SR-6.7","Compliance/IT"],
    ["LCS access + 497 Officer assigned","SR-6.8","Finance/Officer"],
 ],
 "B. Eligibility & enrollment": [
    ["National Verifier approval BEFORE every NLAD enroll","SR-3.1","MSR/Compliance"],
    ["One-per-household worksheet where applicable","SR-1.8","MSR"],
    ["Income (135% FPG) / program eligibility captured","SR-1.4/1.6","MSR"],
    ["Consent + benefit-transfer consent on file","SR-3.6","MSR"],
    ["Tribal-lands per-address verification via USAC tool","SR-4.4","Compliance"],
    ["Enhanced $25 claimed ONLY for verified Tribal-lands addr","SR-4.2/5.5","Compliance"],
    ["NLAD updated within 10 business days of changes","SR-3.2","Billing"],
 ],
 "C. Billing & pass-through": [
    ["Full Lifeline support passed through on the bill","SR-6.8","Billing"],
    ["Separate GL for Lifeline / grant / RIVR / Tribe funds","SR-10.2","Accounting"],
    ["Min service standards met (25/3, 1280GB) — 100/100 OK","SR-2.1/2.2","Network"],
    ["No 'plus tax' advertised until tax advisor confirms","SR-9.9","Marketing/Tax"],
 ],
 "D. Recertification & de-enrollment": [
    ["Annual recertification process (60-day window)","SR-3.3","Compliance"],
    ["Non-usage rule handling (if $0-fee applies)","SR-3.4","Billing/Legal"],
    ["De-enrollment on failure/ineligibility/duplicate","SR-3.5","Compliance"],
 ],
 "E. Reporting & records": [
    ["FCC Form 481 filed by July 1 (confirm year deadline)","SR-6.9","Compliance"],
    ["FCC Form 555 filed by Jan 31 (+ECFS 14-171)","SR-6.10","Compliance"],
    ["Record retention ≥3 yrs / duration of service","SR-6.11","Compliance"],
    ["Lifeline advertising / publicizing availability","SR-6.12","Marketing"],
    ["NC reporting to NCUC as required","SR-7.1","Reg. Counsel"],
 ],
 "F. Waste, fraud & abuse / audit readiness": [
    ["Written WFA policy adopted & executive-signed","SR-6.*","Compliance/Exec"],
    ["No duplicate benefits; NLAD de-dup enforced","SR-1.8/3.2","Compliance"],
    ["Claim only for properly NLAD-enrolled subscribers","SR-6.8","Finance"],
    ["Audit trail / logs retained; access role-based","SR-6.11","IT/Compliance"],
    ["Officer certifications on 481/555/LCS","SR-6.8/6.9/6.10","Officer"],
 ],
}
r = 5
ck.add_data_validation(sdv := status_dv())
n = 1
for sec, items in sections.items():
    cell(ck, f"B{r}", "", "grey"); c = ck.cell(row=r, column=3, value=sec)
    c.font = Font(bold=True, color=WHITE); c.fill = PatternFill("solid", fgColor=NAVY)
    for cc in range(2,9): ck.cell(row=r, column=cc).fill = PatternFill("solid", fgColor=NAVY)
    r += 1
    for it in items:
        cell(ck, f"B{r}", n, "grey", size=9)
        cell(ck, f"C{r}", it[0], "grey", size=9, wrap=True)
        cell(ck, f"D{r}", it[1], "constant", size=9)
        cell(ck, f"E{r}", it[2], "grey", size=9)
        cell(ck, f"F{r}", "", "input", size=9)
        cell(ck, f"G{r}", "", "input", size=9)
        cell(ck, f"H{r}", "", "input", size=9)
        n += 1; r += 1
sdv.add(f"F5:F{r}")
wb.save(BASE+"07_Compliance_and_Audit_Checklist.xlsx")
print("07 done")

# =====================================================================
# 08 — IMPLEMENTATION ROADMAP & RACI
# =====================================================================
wb = Workbook()
cover_sheet(wb, "08", "Implementation Roadmap & RACI",
    "Phased plan (0–4). No public marketing as an approved Lifeline provider until Phase 1 completes "
    "(final ETC order + USAC onboarding). Pilot (Phase 2) precedes public launch (Phase 3).")
rm = wb.create_sheet("Roadmap")
rm.sheet_view.showGridLines = False
widths(rm, {"A":3,"B":40,"C":16,"D":20,"E":11,"F":11,"G":18,"H":18,"I":22,"J":12})
title(rm, "B2", "Phased Implementation Roadmap", 13)
subtitle(rm, "B3", "Dates are relative placeholders — set absolute dates once the ETC order date is known.")
header_row(rm, 5, ["Task","Owner","Dependency","Start","Target","Approval","Evidence of completion","Risk if delayed","Status"], start_col=2)
phases = {
 "PHASE 0 — ETC application pending (now)": [
    ["Complete regulatory research & source register","Reg. Counsel","—","T-0","T+2w","Program Owner","Signed source register","Design on wrong assumptions"],
    ["Obtain Lumbee Tribal-lands legal/USAC determination","Reg. Counsel","Research","T-0","T+8w","Exec Sponsor","Written determination","Mis-set enhanced benefit"],
    ["Confirm RIVR price sheet (all tiers/equip/voice)","Product/Finance","—","T-0","T+3w","CFO","Confirmed price sheet","Bad financial model"],
    ["Financial model + scenarios","Finance","Prices","T+3w","T+6w","CFO","Approved model","Unclear viability"],
    ["Draft policies/SOPs/NISC spec","Program Owner","Research","T-0","T+8w","Compliance","Draft docs","Slow launch"],
    ["Lumbee MOU discussions (no obligations yet)","Exec Sponsor","—","T-0","T+10w","Board","Term sheet","No partnership"],
 ],
 "PHASE 1 — ETC approval & USAC onboarding": [
    ["Receive final NCUC ETC order","Reg. Counsel","NCUC","T+Xw","—","—","Order on file","Cannot proceed"],
    ["FRN, SAM.gov UEI, SAC, 498 ID","Finance","ETC order","+1w","+6w","Officer","System IDs","No reimbursement"],
    ["RAD Rep IDs; NV/NLAD/LCS access","Compliance/IT","498 ID","+2w","+6w","Compliance","Access confirmed","Cannot enroll"],
    ["NISC configuration + test","Billing/IT","Spec","+2w","+8w","Compliance","Test results","Billing errors"],
    ["Employee training complete","Training","SOPs","+4w","+9w","Compliance","Training records","Non-compliant reps"],
 ],
 "PHASE 2 — Controlled pilot": [
    ["Select ≤25–50 existing customers","Program Owner","Phase 1","+9w","+10w","Compliance","Pilot roster","Untested process"],
    ["Run enrollment → NLAD → bill → LCS → reconcile","Cross-functional","Pilot roster","+10w","+14w","Compliance","3-way recon","Scale errors"],
    ["Validate notices & customer experience","MSR/Marketing","Pilot","+10w","+14w","Program Owner","Notice log","Poor CX"],
 ],
 "PHASE 3 — Public launch": [
    ["Coordinated RIVR + Lumbee comms","Marketing","Pilot pass","+14w","+16w","Exec/Tribe","Launch assets","Weak uptake"],
    ["Open enrollment across ETC area","MSR","Launch","+16w","—","Program Owner","Enrollment vol.","—"],
 ],
 "PHASE 4 — Stabilization": [
    ["30/60/90-day reviews","Program Owner","Launch","+20w","+30w","Exec Sponsor","Review memos","Unfixed issues"],
    ["Correct enrollment/billing/claims/training","Cross-functional","Reviews","+20w","+30w","Compliance","Corrective log","Recurring errors"],
 ],
}
r = 6
rm.add_data_validation(sdv := status_dv())
for ph, tasks in phases.items():
    c = rm.cell(row=r, column=2, value=ph); c.font = Font(bold=True, color=WHITE)
    for cc in range(2,11): rm.cell(row=r, column=cc).fill = PatternFill("solid", fgColor=NAVY)
    r += 1
    for t in tasks:
        for i, v in enumerate(t):
            col = chr(ord('B')+i)
            cell(rm, f"{col}{r}", v, "grey", size=8, wrap=(i in (0,6,7)))
        cell(rm, f"J{r}", "", "input", size=8)
        rm.row_dimensions[r].height = 26
        r += 1
sdv.add(f"J6:J{r}")

raci = wb.create_sheet("RACI")
raci.sheet_view.showGridLines = False
roles = ["Exec Sponsor","Program Owner","Compliance","Reg. Counsel","Finance","Accounting","Billing","IT","MSR/CS","Sales","Marketing","Network","Lumbee Tribe","Internal Audit"]
widths(raci, {"A":3,"B":38})
for i in range(len(roles)):
    raci.column_dimensions[chr(ord('C')+i)].width = 6
title(raci, "B2", "RACI Matrix (R=Responsible A=Accountable C=Consulted I=Informed)", 12)
header_row(raci, 5, ["Task / workstream"]+roles, start_col=2)
raci.row_dimensions[5].height = 70
for i in range(len(roles)):
    raci.cell(row=5, column=3+i).alignment = Alignment(text_rotation=90, horizontal="center", vertical="bottom")
raci_rows = [
 ("ETC designation & regulatory filings", {"Reg. Counsel":"A","Program Owner":"R","Compliance":"C","Exec Sponsor":"I","Finance":"I"}),
 ("USAC onboarding (FRN/SAC/498/RAD)", {"Finance":"A","Compliance":"R","IT":"C","Program Owner":"I"}),
 ("Eligibility determination (NV)", {"Compliance":"A","MSR/CS":"R","Reg. Counsel":"C","Internal Audit":"I"}),
 ("Tribal-lands verification", {"Compliance":"A","Reg. Counsel":"R","MSR/CS":"C","Lumbee Tribe":"C","Exec Sponsor":"I"}),
 ("Enrollment & NLAD", {"MSR/CS":"R","Compliance":"A","Billing":"C","IT":"I"}),
 ("NISC billing configuration", {"Billing":"A","IT":"R","Finance":"C","Compliance":"C"}),
 ("Monthly LCS claim & reconciliation", {"Finance":"A","Accounting":"R","Compliance":"C","Internal Audit":"I"}),
 ("Recertification & de-enrollment", {"Compliance":"A","MSR/CS":"R","Billing":"C"}),
 ("Privacy & data security", {"IT":"A","Compliance":"R","Reg. Counsel":"C","Internal Audit":"I"}),
 ("Financial model & budget", {"Finance":"A","Accounting":"R","Exec Sponsor":"C","Program Owner":"I"}),
 ("Customer communications", {"Marketing":"A","MSR/CS":"R","Compliance":"C","Lumbee Tribe":"C"}),
 ("Employee training", {"Compliance":"A","Program Owner":"R","MSR/CS":"I","Sales":"I"}),
 ("Lumbee partnership & MOU", {"Exec Sponsor":"A","Program Owner":"R","Reg. Counsel":"C","Lumbee Tribe":"C"}),
 ("Field install / service", {"Network":"A","IT":"R","MSR/CS":"C"}),
 ("Internal audit & WFA controls", {"Internal Audit":"A","Compliance":"R","Exec Sponsor":"I"}),
]
r = 6
for task, m in raci_rows:
    cell(raci, f"B{r}", task, "grey", size=9, wrap=True)
    for i, role in enumerate(roles):
        col = chr(ord('C')+i)
        v = m.get(role, "")
        fill = {"A":"C00000","R":"2E5496","C":"BDD7EE","I":"F2F2F2"}.get(v)
        c = cell(raci, f"{col}{r}", v, "calc", size=9, align="center")
        if fill: c.fill = PatternFill("solid", fgColor=fill)
        if v in ("A","R"): c.font = Font(bold=True, color=WHITE, size=9)
    r += 1
wb.save(BASE+"08_Implementation_Roadmap_and_RACI.xlsx")
print("08 done")

# =====================================================================
# 12 — EXECUTIVE READINESS SCORECARD
# =====================================================================
wb = Workbook()
cover_sheet(wb, "12", "Executive Readiness Scorecard",
    "Weighted go/no-go gate. The program MUST NOT launch while any 'Gate' item is Red. Enhanced-Tribal "
    "readiness is intentionally gated on a written Tribal-lands determination.")
sc = wb.create_sheet("Scorecard")
sc.sheet_view.showGridLines = False
widths(sc, {"A":3,"B":40,"C":10,"D":12,"E":12,"F":10,"G":34})
title(sc, "B2", "Executive Readiness Scorecard", 13)
subtitle(sc, "B3", "Score each 0–5. Weighted score = score × weight. Gate items in red block launch if not Green.")
header_row(sc, 5, ["Readiness dimension","Weight","Score (0-5)","Weighted","RAG","Notes"], start_col=2)
dims = [
 ("Final NCUC ETC order in hand (GATE)",0.15,0,True),
 ("USAC onboarding complete (SAC/498/NLAD/LCS) (GATE)",0.12,0,True),
 ("Tribal-lands legal determination obtained (GATE)",0.10,0,True),
 ("Confirmed RIVR price sheet & tax review",0.10,0,False),
 ("Financial model approved / sustainable",0.10,0,False),
 ("NISC configured & tested",0.10,0,False),
 ("Enrollment SOPs & QC ready",0.08,0,False),
 ("Employee training complete",0.07,0,False),
 ("Privacy & data-security controls live",0.08,0,False),
 ("Customer comms approved (no ACP/false claims)",0.05,0,False),
 ("Lumbee MOU executed (if partnering)",0.05,0,False),
]
r = 6
sc.add_data_validation(rdv := rag_dv())
for name, w, s, gate in dims:
    cell(sc, f"B{r}", name, "grey", size=9, wrap=True, bold=gate, color=None)
    if gate: sc[f"B{r}"].font = Font(bold=True, color=RED, size=9)
    cell(sc, f"C{r}", w, "constant", num=PCT)
    cell(sc, f"D{r}", s, "input", num=NUM)
    cell(sc, f"E{r}", f"=C{r}*D{r}", "calc", num='0.00')
    cell(sc, f"F{r}", "", "input", size=9)
    cell(sc, f"G{r}", "", "input", size=9)
    r += 1
cell(sc, f"B{r}", "WEIGHTED TOTAL (max 5.0)", "good", bold=True)
cell(sc, f"E{r}", f"=SUM(E6:E{r-1})", "good", num='0.00', bold=True)
rdv.add(f"F6:F{r-1}")
r += 2
cell(sc, f"B{r}", "GO / NO-GO RULE", "grey", bold=True)
cell(sc, f"B{r+1}", "GO only if: weighted total ≥ 4.0 AND every GATE dimension = Green. Enhanced Tribal "
    "benefit remains OFF (0 subs) until the Tribal-lands determination is Green.", "grey", wrap=True, size=9)
sc.merge_cells(f"B{r+1}:G{r+2}")
wb.save(BASE+"12_Executive_Readiness_Scorecard.xlsx")
print("12 done")

# =====================================================================
# 13 — OPEN ISSUES & LEGAL DECISIONS LOG
# =====================================================================
wb = Workbook()
cover_sheet(wb, "13", "Open Issues & Legal Decisions Log",
    "Single source of truth for unresolved questions. Each has a recommended decision, rationale, "
    "named decision-maker, and required-by date. Enhanced-Tribal eligibility (ISS-01) is the "
    "highest-severity item and gates any enhanced-benefit claim.")
lg = wb.create_sheet("Open Issues")
lg.sheet_view.showGridLines = False
widths(lg, {"A":3,"B":7,"C":34,"D":9,"E":34,"F":30,"G":16,"H":13,"I":11})
title(lg, "B2", "Open Issues & Legal Decisions Log", 13)
header_row(lg, 4, ["ID","Issue / decision","Sev","Recommended decision","Rationale","Decision-maker","Required by","Status"], start_col=2)
issues = [
 ["ISS-01","Do any Lumbee lands qualify as FCC 'Tribal lands' (§54.400(e)/§54.412)?","HIGH",
  "Assume NO qualifying Tribal lands; set enhanced $25 to 0 subs until written USAC/legal determination confirms otherwise.",
  "No reservation/trust land; four-county service area ≠ Tribal lands; no §54.412 designation (SR-4/SR-5).",
  "Reg. Counsel + USAC/FCC ONAP","Before enroll","Open"],
 ["ISS-02","Which Senior-plan components are taxable?","HIGH",
  "Tax advisor written opinion; do not advertise 'plus tax' until received (broadband access non-taxable per ITFA).",
  "NC taxes voice/equip; ITFA bars internet-access tax; managed Wi-Fi open (SR-9).",
  "Tax Advisor + CFO","Before launch","Open"],
 ["ISS-03","Senior eligibility age: 60 / 62 / 65?","MED",
  "Recommend 62 (Social Security early-retirement anchor; balances reach vs. exposure).",
  "65 = fewer, safer; 60 = broadest, costliest; 62 = middle (see Exec Plan).",
  "Exec Sponsor","Phase 0 end","Open"],
 ["ISS-04","Is $10 the retail price or net-after-subsidy?","HIGH",
  "Recommend Alternative D: $10 is the NET target after Lifeline + defined top-up (retail stays list).",
  "Avoids over-recovery on tribal; simplest NISC admin; protects non-LL seniors (SR-1/Fin Model).",
  "Exec Sponsor + CFO","Phase 0 end","Open"],
 ["ISS-05","Do non-Lifeline seniors get a company-funded discount?","MED",
  "Yes under Alt D, capped; model exposure; revisit if uptake high.",
  "Equity of a 'senior plan'; but full company cost w/o USAC offset.",
  "CFO","Phase 0 end","Open"],
 ["ISS-06","Does the Lumbee Tribe contribute funding?","MED",
  "Pursue via MOU but do not assume; model with $0 Tribe funding as base case.",
  "Separate accounting required; no commitment yet (SR-10).",
  "Exec Sponsor + Tribe","Phase 1","Open"],
 ["ISS-07","Equipment & install charges for the Senior plan?","MED",
  "Recommend waive/lower equipment to protect the $10 target; confirm tax.",
  "$5/mo router would break the $10 target unless folded in (SR-8.4).",
  "Product + CFO","Phase 0 end","Open"],
 ["ISS-08","Can voice be bundled?","LOW",
  "Offer voice as OPTIONAL add-on; keep out of the $10 broadband target; disclose voice taxes/911/USF.",
  "Voice is taxable & assessed; Lifeline min-standard is broadband (SR-2/SR-9).",
  "Product + Tax","Phase 1","Open"],
 ["ISS-09","Non-usage rule applicability with a $10 charge?","MED",
  "Confirm with counsel; if a >$0 fee applies, the 30/15-day non-usage rule likely does not.",
  "Rule targets $0-fee services (SR-3.4).",
  "Reg. Counsel","Phase 1","Open"],
 ["ISS-10","NCUC ETC docket status for LREMC/RIVR?","HIGH",
  "Confirm docket number & status via NCUC portal/staff; track to final order.",
  "Not found via search (SR-7.3).",
  "Reg. Counsel","Phase 0","Open"],
 ["ISS-11","TBCP/grant funds for recurring bills?","MED",
  "Do NOT use for recurring consumer subsidy unless award terms expressly allow; keep separate GL.",
  "Grant terms govern; commingling risk (SR-10).",
  "CFO + Reg. Counsel","Before use","Open"],
 ["ISS-12","Membership verification method w/ the Tribe (privacy)?","MED",
  "Tribe-run attestation / hashed match; NO transfer of full tribal roll to RIVR.",
  "Data minimization; privacy (see MOU & Privacy sec).",
  "Program Owner + Tribe","Phase 1","Open"],
 ["ISS-13","Pilot size & launch date?","LOW",
  "≤25–50 pilot customers; set launch after pilot 3-way recon passes.",
  "De-risk before scale.","Program Owner","Phase 2","Open"],
 ["ISS-14","Branding / Tribe name & logo use approval?","LOW",
  "Written Tribe approval before any joint asset uses name/logo.",
  "Sovereignty & brand control (MOU).","Marketing + Tribe","Phase 3","Open"],
]
r = 5
lg.add_data_validation(sdv2 := DataValidation(type="list", formula1='"Open,In progress,Decided,Deferred"', allow_blank=True))
for row in issues:
    for i, v in enumerate(row):
        col = chr(ord('B')+i)
        kind = "grey"
        if i == 3: kind = "constant"
        if i == 8: kind = "input"
        c = cell(lg, f"{col}{r}", v, kind, size=8, wrap=(i in (2,4,5)))
        if i == 3 and row[3]:  # severity color on sev col actually i==3? sev is i==3? No sev is index3?
            pass
    # color severity cell (index 3 -> col E? Actually columns: B=ID,C=issue,D=sev,E=rec,...)
    sev = row[3]  # wait mapping
    r += 1
# Fix severity coloring: sev is 3rd element -> column D
r2 = 5
for row in issues:
    sev = row[2]
    c = lg[f"D{r2}"]
    fillmap = {"HIGH":"C00000","MED":"ED7D31","LOW":"BDD7EE"}
    c.fill = PatternFill("solid", fgColor=fillmap.get(sev,"F2F2F2"))
    c.font = Font(bold=True, color=WHITE if sev in ("HIGH","MED") else RED, size=9)
    lg.row_dimensions[r2].height = 40
    r2 += 1
sdv2.add(f"I5:I{r-1}")
wb.save(BASE+"13_Open_Issues_and_Legal_Decisions_Log.xlsx")
print("13 done")
print("ALL EXCEL DONE")
