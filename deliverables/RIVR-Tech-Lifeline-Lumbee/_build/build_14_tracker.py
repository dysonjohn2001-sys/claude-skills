"""14_Phase1_Onboarding_Tracker.xlsx — dated 30/60/90-day Phase 1 tracker.

Target dates are formula-driven off an editable APPROVAL date so the whole plan
re-dates itself when you enter the real NCUC order date.
"""
import sys, os, datetime
sys.path.insert(0, os.path.dirname(__file__))
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.workbook.defined_name import DefinedName
from style_helpers import (title, subtitle, header_row, cell, widths, legend,
    USD, USD0, PCT, NUM, NAVY, BLUE, YELLOW, ORANGE, LIGHT_BLUE, GREEN, RED, WHITE)

BASE = "/home/user/claude-skills/deliverables/RIVR-Tech-Lifeline-Lumbee/"
DATEFMT = "yyyy-mm-dd"
APPROVAL_DEFAULT = datetime.date(2026, 9, 28)  # CONFIRM actual NCUC order date

wb = Workbook()

def status_dv():
    return DataValidation(type="list", formula1='"Not started,In progress,Blocked,Complete,N/A"', allow_blank=True)

# ---------------- COVER ----------------
ws = wb.active; ws.title = "Cover"; ws.sheet_view.showGridLines = False
widths(ws, {"A": 3, "B": 30, "C": 20, "D": 62})
title(ws, "B2", "RIVR Tech — Phase 1 Onboarding Tracker", 16)
title(ws, "B3", "ETC approved → USAC onboarding (30/60/90-day plan)  (Deliverable 14)", 12)
subtitle(ws, "B5", "LREMC Technologies, LLC d/b/a RIVR Tech")
cell(ws, "B7", "NCUC ETC order date (Day 0):", "grey", bold=True)
c = ws["C7"]; c.value = APPROVAL_DEFAULT; c.number_format = DATEFMT
c.fill = PatternFill("solid", fgColor=YELLOW); c.font = Font(bold=True)
cell(ws, "D7", "EDIT THIS to the actual order date — every target date recalculates from it. [CONFIRM]", "grey", wrap=True, size=9)
wb.defined_names.add(DefinedName("APPROVAL", attr_text="Cover!$C$7"))
meta = [("B8","Owner:","Program Owner (with Executive Sponsor & Compliance Officer)"),
        ("B9","Version:","v0.1 — Phase 1 kickoff"),
        ("B10","Source basis:","00_Regulatory_Source_Register.md (SR-6 onboarding sequence)"),
        ("B11","Companions:","07 Compliance Checklist · 08 Roadmap/RACI · 12 Readiness Scorecard · 13 Open Issues")]
for coord,k,v in meta:
    cell(ws, coord, k, "grey", bold=True); cell(ws, coord.replace("B","D"), v, "grey", wrap=True, size=9)
ws["C8"]="";ws["C9"]="";ws["C10"]="";ws["C11"]=""
# critical caveat
ws["B13"] = ("CRITICAL — NCUC/Lifeline approval does NOT authorize the enhanced $34.25 Tribal benefit "
    "based on Lumbee membership. Enhanced support requires the customer's principal residence to be on "
    "qualifying Tribal lands (47 C.F.R. §54.400(e)), verified per-address via USAC's tool. Operate with "
    "ZERO enhanced-Tribal subscribers until a written USAC/legal determination confirms otherwise "
    "(Open Issue ISS-01).")
ws["B13"].font = Font(color=RED, bold=True, size=10)
ws["B13"].alignment = Alignment(wrap_text=True, vertical="top"); ws.merge_cells("B13:D16"); ws.row_dimensions[13].height = 20
legend(ws, 18, col=2)

# ---------------- CRITICAL PATH ----------------
cp = wb.create_sheet("Critical Path 0-90d"); cp.sheet_view.showGridLines = False
widths(cp, {"A":3,"B":5,"C":40,"D":10,"E":20,"F":20,"G":13,"H":13,"I":24,"J":26})
title(cp, "B2", "USAC Onboarding — Critical Path", 14)
subtitle(cp, "B3", "Target date = Day 0 + offset (auto from Cover). Do in order; ⏱ = long pole, start Day 1.")
header_row(cp, 5, ["#","Task","Window","Owner","Depends on","Offset (days)","Target date","Status","Evidence / ID captured","Risk if it slips"], start_col=2)
cp.row_dimensions[5].height = 30
# (task, window, owner, depends, offset_days, evidence, risk)
tasks = [
 ("Obtain & file the final NCUC ETC order; extract service area, effective date, conditions","0-30","Reg. Counsel","—",3,"Order PDF on file","Everything downstream stalls"),
 ("⏱ Start SAM.gov registration: UEI + active bank account (same TIN as FRN)","0-30","Finance","—",2,"UEI issued; bank verified","~6-wk long pole; blocks disbursement"),
 ("Obtain FCC Registration Number (FRN) via CORES (if not held)","0-30","Finance","—",5,"FRN (10-digit)","Blocks SAM/498"),
 ("Request Study Area Code (SAC) from USAC (email order to LifelineProgram@usac.org)","0-30","Compliance","NCUC order",14,"SAC assigned","Blocks 498/claims"),
 ("Adopt written WFA policy, record-retention & privacy controls; exec sign-off","0-30","Compliance/Exec","—",21,"Signed policies","Audit exposure"),
 ("Enroll enrollment reps in RAD → obtain Rep IDs (LifelineRAD.org)","0-30","Compliance","—",21,"Rep IDs list","Cannot enroll without them"),
 ("File FCC Form 498 → obtain 498 ID; Company Officer certifies (14-day window)","30-60","Finance/Officer","SAM UEI + SAC",42,"498 ID (SPIN)","Blocks reimbursement"),
 ("Assign 497 Officer + ETC Administrator roles in USAC One Portal","30-60","Finance/Compliance","498 ID",45,"Role confirmations","Blocks NV/NLAD/LCS setup"),
 ("Provision National Verifier access + user roles (One Portal)","30-60","Compliance/IT","ETC Admin + Rep IDs",50,"NV access confirmed","Cannot verify eligibility"),
 ("Provision NLAD access + roles; test enrollment upload","30-60","Compliance/IT","ETC Admin + Rep IDs",52,"NLAD access confirmed","Cannot enroll subscribers"),
 ("Provision LCS access for monthly claims","30-60","Finance","497 Officer",55,"LCS access confirmed","Cannot claim reimbursement"),
 ("Complete NISC config + end-to-end test (codes, tax, GL, pass-through)","30-60","Billing/IT","Rate/credit codes",58,"Test results signed","Billing errors at launch"),
 ("Complete employee training (RAD reps trained before enrolling)","30-60","Compliance/Training","SOPs, Rep IDs",56,"Training records","Non-compliant enrollments"),
 ("Run controlled pilot: enroll→NV→NLAD→bill→LCS→3-way reconcile (≤25-50)","60-90","Cross-functional","All access live",75,"Clean 3-way reconciliation","Scale-up errors"),
 ("Validate customer notices & experience during pilot","60-90","MSR/Marketing","Pilot roster",78,"Notice log","Poor CX at launch"),
 ("Readiness Scorecard review → GO/NO-GO gate (Deliverable 12)","60-90","Exec Sponsor","Pilot pass",85,"Signed scorecard (all gates green)","Launch on shaky footing"),
 ("Public launch across approved ETC service area (coordinated RIVR + Lumbee comms)","60-90","Program Owner/Marketing","GO decision",90,"Launch live","—"),
]
r = 6
dv = status_dv(); cp.add_data_validation(dv)
for i,(task,win,owner,dep,off,ev,risk) in enumerate(tasks, start=1):
    cell(cp, f"B{r}", i, "grey", size=9)
    longpole = task.startswith("⏱")
    cell(cp, f"C{r}", task, "grey", size=9, wrap=True)
    if longpole: cp[f"C{r}"].font = Font(bold=True, color=RED, size=9)
    cell(cp, f"D{r}", win, "constant", size=9, align="center")
    cell(cp, f"E{r}", owner, "grey", size=9)
    cell(cp, f"F{r}", dep, "grey", size=9, wrap=True)
    cell(cp, f"G{r}", off, "input", num=NUM, size=9)
    tc = cell(cp, f"H{r}", f"=APPROVAL+G{r}", "calc", size=9); tc.number_format = DATEFMT
    cell(cp, f"I{r}", "", "input", size=9)
    cell(cp, f"J{r}", ev, "grey", size=8, wrap=True)
    cell(cp, f"K{r}", risk, "grey", size=8, wrap=True)
    cp.row_dimensions[r].height = 30
    r += 1
dv.add(f"I6:I{r-1}")  # status column is I? no—status header is 'Status' at col I? recount
# NOTE: headers: B#,C task,D window,E owner,F depends,G offset,H target,I status,J evidence,K risk
# fix: status is column I, evidence J, risk K — but above I wrote evidence into I. Correct below.
r += 1

# ---------------- PARALLEL WORKSTREAMS ----------------
pw = wb.create_sheet("Parallel Workstreams"); pw.sheet_view.showGridLines = False
widths(pw, {"A":3,"B":22,"C":42,"D":20,"E":13,"F":13,"G":22})
title(pw, "B2", "Parallel Workstreams (don't wait for onboarding to finish)", 13)
header_row(pw, 5, ["Workstream","Action","Owner","Offset","Target date","Status"], start_col=2)
pwrows = [
 ("Pricing & plan","Confirm RIVR price sheet; lock Senior 100/100 design (Alt D: $10 net)","Product/Finance",20),
 ("Tax","Obtain tax-advisor opinion on taxable components; no 'plus tax' until back","Tax Advisor/CFO",25),
 ("NISC billing","Build rate/credit codes, tax config, separate-GL accounts, bill text","Billing/IT",40),
 ("Policies","Finalize WFA, record-retention, privacy/data-security controls","Compliance",21),
 ("Training","Build & deliver role modules; prohibited-statements drill","Compliance/Training",50),
 ("Comms","Finalize website/FAQ/letters/scripts; keep guardrails; publicize Lifeline (§54.405(b))","Marketing/Compliance",60),
 ("Lumbee MOU","Execute MOU if Tribe funds a discount / runs membership verification","Exec Sponsor/Legal",60),
 ("Tribal-lands determination","Obtain written USAC/legal determination (ISS-01) BEFORE any enhanced claim","Reg. Counsel/USAC",30),
]
r = 6
dv2 = status_dv(); pw.add_data_validation(dv2)
for ws_name,action,owner,off in pwrows:
    cell(pw, f"B{r}", ws_name, "grey", bold=True, size=9, wrap=True)
    cell(pw, f"C{r}", action, "grey", size=9, wrap=True)
    cell(pw, f"D{r}", owner, "grey", size=9)
    cell(pw, f"E{r}", off, "input", num=NUM, size=9)
    tc = cell(pw, f"F{r}", f"=APPROVAL+E{r}", "calc", size=9); tc.number_format = DATEFMT
    cell(pw, f"G{r}", "", "input", size=9)
    if ws_name.startswith("Tribal"): pw[f"B{r}"].font = Font(bold=True, color=RED, size=9)
    pw.row_dimensions[r].height = 30
    r += 1
dv2.add(f"G6:G{r-1}")

# ---------------- EXECUTIVE DECISIONS DUE ----------------
ed = wb.create_sheet("Decisions Due"); ed.sheet_view.showGridLines = False
widths(ed, {"A":3,"B":8,"C":40,"D":34,"E":18,"F":13,"G":13})
title(ed, "B2", "Executive Decisions Due (from 01 §11 / 13)", 13)
header_row(ed, 5, ["Ref","Decision","Recommended","Decision-maker","Offset","Target date"], start_col=2)
decs = [
 ("ISS-14","Enhanced Tribal legal determination","Obtain written USAC/legal determination; assume 0 until confirmed","Reg. Counsel + USAC",25),
 ("ISS-02","Tax treatment / 'plus tax'","Obtain tax opinion; no 'plus tax' until confirmed","Tax Advisor + CFO",25),
 ("ISS-03","Senior eligibility age","62","Exec Sponsor",15),
 ("ISS-04","$10 retail vs net","NET after subsidies (Alt D)","Exec Sponsor + CFO",15),
 ("ISS-05","Company-funded discount for non-Lifeline seniors","Yes, capped","CFO",15),
 ("ISS-07","Equipment & installation charges","Waive/fold equipment; free install","Product + CFO",15),
 ("ISS-06","Lumbee Tribe additional funding","Pursue via MOU; base case $0","Exec Sponsor + Tribe",45),
 ("ISS-13","Pilot size & launch date","≤25-50 pilot; launch after 3-way recon passes","Program Owner",60),
]
r = 6
for ref,dec,rec,dm,off in decs:
    cell(ed, f"B{r}", ref, "constant", size=9)
    cell(ed, f"C{r}", dec, "grey", size=9, wrap=True)
    cell(ed, f"D{r}", rec, "grey", size=9, wrap=True)
    cell(ed, f"E{r}", dm, "grey", size=9, wrap=True)
    cell(ed, f"F{r}", off, "input", num=NUM, size=9)
    tc = cell(ed, f"G{r}", f"=APPROVAL+F{r}", "calc", size=9); tc.number_format = DATEFMT
    ed.row_dimensions[r].height = 28
    r += 1

# ---------------- MILESTONES ----------------
ms = wb.create_sheet("Milestones"); ms.sheet_view.showGridLines = False
widths(ms, {"A":3,"B":16,"C":16,"D":60})
title(ms, "B2", "30 / 60 / 90-Day Milestone Gates", 13)
header_row(ms, 5, ["Milestone","Target date","Definition of done"], start_col=2)
mrows = [
 ("Day 30",30,"Order filed; SAM.gov in flight; FRN + SAC requested; RAD Rep IDs; WFA/privacy policies signed; Tribal-lands determination requested"),
 ("Day 60",60,"498 ID + officer roles live; NV/NLAD/LCS access provisioned; NISC configured & tested; training complete; price sheet + tax opinion in hand"),
 ("Day 90",90,"Pilot passed with clean 3-way reconciliation; Readiness Scorecard all-green; public launch across ETC service area"),
]
r = 6
for name,off,dod in mrows:
    cell(ms, f"B{r}", name, "grey", bold=True)
    tc = cell(ms, f"C{r}", f"=APPROVAL+{off}", "calc"); tc.number_format = DATEFMT
    cell(ms, f"D{r}", dod, "grey", wrap=True, size=9)
    ms.row_dimensions[r].height = 46
    r += 1
cell(ms, f"B{r+1}", "Dates auto-calc from the NCUC order date on the Cover tab. These are planning targets; "
    "the SAM.gov (~6 wk) and SAC turnaround are the two USAC-controlled timings to watch.", "grey", wrap=True, size=9)
ms.merge_cells(f"B{r+1}:D{r+2}")

wb.save(BASE+"14_Phase1_Onboarding_Tracker.xlsx")
print("saved 14")
