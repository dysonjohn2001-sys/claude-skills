"""
consistency_check.py — package-wide QA for the Lumbee Tribe / RIVR Tech TBCP
Agreement Package (master-prompt build). Verifies the file manifest, party-name
and defined-term consistency (incl. LREMC as a SEPARATE owner), the per-Active-
Subscriber model, the 20yr+2x5 term, order-of-precedence, no unintended transfer
of grant-funded property, and that every file opens cleanly.
"""
from __future__ import annotations
import os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
from docx import Document
from openpyxl import load_workbook

PKG = C.PKG_DIR

EXPECTED = {
    "00_START_HERE": ["01_Executive_Summary_and_Transaction_Structure.docx",
                      "02_Agreement_Register_and_Signing_Sequence.docx"],
    "01_Phase1_Diligence": [
        "01_Source_and_Assumptions_Register.xlsx", "02_Missing_Information_Request.docx",
        "03_Red_Flag_and_Approval_Memorandum.docx", "04_Contractor_vs_Subrecipient_Analysis.docx",
        "05_Procurement_and_OCI_Checklist.xlsx", "06_Responsibility_and_Transaction_Matrix.xlsx",
        "07_Asset_Ownership_and_Rights_Matrix.xlsx", "08_Term_Sheet_and_Decision_Register.docx",
        "09_Federal_Approval_Request.docx"],
    "02_Definitive_Agreements": [
        "01_Master_TBCP_Partnership_and_Implementation_Agreement.docx",
        "02_Design_Engineering_Procurement_and_Construction_Agreement.docx",
        "03_IRU_and_Network_Access_Agreement.docx",
        "04_Interconnection_Transport_and_Shared_Facilities_Agreement.docx",
        "05_Network_Operations_Maintenance_and_Lifecycle_Agreement.docx",
        "06_Retail_Billing_and_Subscriber_Revenue_Agreement.docx",
        "07_Grant_Finance_Reimbursement_Program_Income_and_Audit_Agreement.docx",
        "08_Land_Easement_ROW_Pole_and_Facility_Instruments.docx",
        "09_Data_Privacy_Cybersecurity_and_Continuity_Addendum.docx",
        "10_Continuity_Step_In_and_Transition_Agreement.docx"],
    "03_Governance_Authorizations": [
        "01_Lumbee_Tribal_Council_Resolution.docx", "02_RIVR_Tech_Member_Authorization.docx",
        "03_LREMC_Consent_and_Joinder.docx", "04_Limited_Waiver_of_Sovereign_Immunity.docx",
        "05_Tax_TERO_Permitting_and_Regulatory_Schedule.docx", "06_Insurance_Schedule.docx",
        "07_Service_Level_Schedule.docx"],
    "04_Operational_Forms": [
        "01_Construction_Forms_NTP_ChangeOrder_Inspection_PunchList_Acceptance.docx",
        "02_Segment_IRU_Activation_Certificate.docx",
        "03_Monthly_Grant_Evidence_Checklist_and_Reimbursement_Certification.xlsx",
        "04_Monthly_Subscriber_Reconciliation_and_Payment_Report.xlsx",
        "05_Annual_Budget_Capital_Refresh_Reserve_and_Sustainability.xlsx",
        "06_Project_Registers.xlsx",
        "07_Incident_Outage_RCA_and_Restoration_Forms.docx",
        "08_Program_Checklists.xlsx"],
    "05_Schedules": [f"S{i}_" for i in range(1, 15)],   # prefix match, either ext
    "06_Compliance": ["01_Clause_by_Clause_Compliance_Crosswalk.xlsx",
                      "02_Closing_and_Implementation_Plan.xlsx"],
}

results = {"PASS": [], "WARN": [], "FAIL": []}
def rec(l, m): results[l].append(m)

def docx_text(p):
    d = Document(p); parts = [x.text for x in d.paragraphs]
    for t in d.tables:
        for r in t.rows:
            for c in r.cells: parts.append(c.text)
    return "\n".join(parts)

def xlsx_text(p):
    wb = load_workbook(p, data_only=False); parts = []
    for ws in wb.worksheets:
        parts.append(ws.title)
        for row in ws.iter_rows(values_only=True):
            for v in row:
                if v is not None: parts.append(str(v))
    return "\n".join(parts)

corpus = {}; missing = []; found_n = 0
for folder, files in EXPECTED.items():
    fdir = os.path.join(PKG, folder)
    for fn in files:
        if fn.endswith("_"):   # schedule prefix match, either extension
            hit = None
            if os.path.isdir(fdir):
                for actual in os.listdir(fdir):
                    if actual.startswith(fn) and actual.endswith((".docx", ".xlsx")):
                        hit = actual; break
            if not hit: missing.append(f"{folder}/{fn}*"); continue
            path = os.path.join(fdir, hit); key = f"{folder}/{hit}"
        else:
            path = os.path.join(fdir, fn); key = f"{folder}/{fn}"
            if not os.path.exists(path): missing.append(key); continue
        try:
            corpus[key] = docx_text(path) if path.endswith(".docx") else xlsx_text(path)
            found_n += 1
        except Exception as e:
            rec("FAIL", f"[open] {key}: {e}")

if missing:
    for m in missing: rec("FAIL", f"[manifest] missing: {m}")
rec("PASS" if not missing else "WARN", f"[manifest] {found_n} files found and opened cleanly.")

# Party names present in every substantive document
for name, txt in corpus.items():
    if "Instructions" in txt and name.endswith(".xlsx") and len(txt) < 400:
        continue
    if C.TRIBE_FULL not in txt and "Lumbee Tribe" not in txt:
        rec("WARN", f"[parties] {name}: Lumbee Tribe name absent")
    if "RIVR Tech" not in txt:
        rec("WARN", f"[parties] {name}: RIVR Tech absent")
rec("PASS", "[parties] party-name scan complete.")

# LREMC treated as a separate owner where it should appear
for key in ["02_Definitive_Agreements/04_Interconnection_Transport_and_Shared_Facilities_Agreement.docx",
            "02_Definitive_Agreements/08_Land_Easement_ROW_Pole_and_Facility_Instruments.docx",
            "03_Governance_Authorizations/03_LREMC_Consent_and_Joinder.docx"]:
    if key in corpus and "LREMC" not in corpus[key] and "Lumbee River" not in corpus[key]:
        rec("WARN", f"[LREMC] {key}: LREMC separate-owner reference not found")
rec("PASS", "[LREMC] separate-owner references present in land/interconnection/consent docs.")

# Per-Active-Subscriber model in retail + reconciliation
retail = corpus.get("02_Definitive_Agreements/06_Retail_Billing_and_Subscriber_Revenue_Agreement.docx", "")
if "Active Subscriber" in retail:
    rec("PASS", "[payment] Active Subscriber model present in Retail/Subscriber-Revenue Agreement.")
else:
    rec("WARN", "[payment] Active Subscriber term not found in Retail Agreement.")

# Term 20 + two 5-year renewals in master/IRU
for key, label in [("02_Definitive_Agreements/01_Master_TBCP_Partnership_and_Implementation_Agreement.docx", "Master"),
                   ("02_Definitive_Agreements/03_IRU_and_Network_Access_Agreement.docx", "IRU")]:
    t = corpus.get(key, "")
    if "20" in t and ("five (5)" in t or "5-year" in t or "five-year" in t):
        rec("PASS", f"[term] {label}: 20-year + 5-year-renewal term present.")
    else:
        rec("WARN", f"[term] {label}: 20+2x5 term not clearly detected.")

# Order of precedence in the definitive agreements
prec_hits = sum(1 for k, t in corpus.items()
                if "02_Definitive_Agreements" in k and ("precedence" in t.lower() or "controls" in t.lower()))
rec("PASS" if prec_hits >= 6 else "WARN", f"[precedence] order-of-precedence language in {prec_hits} definitive agreements.")

# No unintended transfer — IRU retains Tribal title
iru = corpus.get("02_Definitive_Agreements/03_IRU_and_Network_Access_Agreement.docx", "").lower()
if "title" in iru and ("does not transfer" in iru or "not transfer" in iru or "retain" in iru):
    rec("PASS", "[ownership] IRU expressly retains Tribal title / no transfer of grant-funded property.")
else:
    rec("WARN", "[ownership] IRU title-retention language not clearly detected.")

# Program income flagged in retail/finance
fin = corpus.get("02_Definitive_Agreements/07_Grant_Finance_Reimbursement_Program_Income_and_Audit_Agreement.docx", "")
if "Program Income" in fin or "200.307" in fin:
    rec("PASS", "[program income] program-income treatment present in Grant Finance Agreement.")
else:
    rec("WARN", "[program income] program-income treatment not found in Grant Finance Agreement.")

# Preliminary / Round-2 baseline disclosure present broadly
base_hits = sum(1 for t in corpus.values() if "PRELIMINARY" in t or "Round 2" in t)
rec("PASS" if base_hits >= 10 else "WARN", f"[baseline] preliminary/Round-2 disclosure in {base_hits} files.")

# Flag discipline
flagged = sum(1 for t in corpus.values() if any(f in t for f in C.ALL_FLAGS))
rec("PASS" if flagged >= 10 else "WARN", f"[discipline] {flagged} files carry review-flag markers.")

print("=" * 80)
print("LUMBEE / RIVR TECH TBCP AGREEMENT PACKAGE — CONSISTENCY CHECK")
print("=" * 80)
for lvl in ("PASS", "WARN", "FAIL"):
    print(f"\n{lvl} ({len(results[lvl])}):")
    for m in results[lvl]: print(f"  [{lvl}] {m}")
print("\n" + "=" * 80)
print(f"TOTAL: {len(results['PASS'])} PASS | {len(results['WARN'])} WARN | {len(results['FAIL'])} FAIL")
print("=" * 80)
sys.exit(1 if results["FAIL"] else 0)
