# RIVR Tech – RCC Student-Athlete Sponsorship & Paid Internship Package

**Status:** OFFICIAL EXECUTION VERSION — **approved by Robeson Community College**
(Version 1.0 — Final, August 24, 2026). The DRAFT banners and pre-execution
review flags have been removed. The agreement becomes binding upon full execution
by all required parties; remaining yellow fields are completed at signing for a
specific student-athlete.

> The document filenames keep the `RIVRTECH_` prefix as stable identifiers; the
> brand shown inside every document is **RIVR Tech**.

## Deliverables

| File | Description |
|------|-------------|
| `RIVRTECH_RCC_Student_Athlete_Sponsorship_Internship_Agreement.docx` | The full 21-page agreement (26 sections + Exhibits A–F + signature blocks). |
| `RIVRTECH_RCC_Student_Athlete_Sponsorship_Internship_Agreement.pdf` | PDF render of the agreement for review/printing. |
| `RIVRTECH_RCC_Proposal_Cover_Letter.docx` | One-page proposal letter to Jake Jones, Athletic Director & Head Baseball Coach. |
| `RIVRTECH_RCC_Approval_Checklist.docx` | Standalone approvals checklist (mirrors Exhibit F). |

Remaining editable placeholders are **highlighted in yellow**. Font is **Arial
11 pt**; 1-inch margins; page numbers and footer on every page; "DRAFT FOR
DISCUSSION AND LEGAL REVIEW" banner in the header.

## Payment structure (Section 6)

**Model:** RIVR Tech pays the Student-Athlete a **$2,000.00 sponsorship in advance**
at the beginning of the semester/term, and the Student-Athlete **earns it through
sales & marketing work** at **$20.00/hour**:

```
Hours to Earn the Sponsorship = Sponsorship Amount ÷ $20.00
$2,000.00 ÷ $20.00 = 100 authorized hours
```

If the amount changes: $2,500 → 125 hrs · $5,000 → 250 hrs · $7,500 → 375 hrs.

**§6.7 unearned portion:** set to **Option A — the student repays** the unearned
portion (Sponsorship − $20 × hours worked), with repayment/deductions to comply
with the FLSA and NC Wage and Hour Act. §6.0 keeps an operative acknowledgment
that the advance/recoupment remains subject to FLSA, NC wage law, tax rules, and
NJCAA/conference eligibility. "Sponsorship" (not "scholarship") is used
deliberately to reduce athletic-aid characterization risk.

## Values filled in

| Field | Value |
|-------|-------|
| Sponsorship / Hours | $2,000.00 paid in advance → earned over 100 hours @ $20.00/hr |
| RIVR Tech work-location ZIP | 28372 (Pembroke, NC — confirmed) |
| RIVR Tech contact email | john.dyson@lumbeeriver.com |
| Effective Date | date of the last signature below |
| Document date / version / status | July 16, 2026 · 0.1 — Draft · Pending review |
| Agreement Term *(proposed)* | September 1, 2026 – May 31, 2027 |
| Maximum Duration *(proposed)* | twelve (12) months |
| Weekly hours cap, §8 *(proposed)* | ten (10) hours/week |
| RIVR Tech Supervisor | John Dyson, Chief Operations Officer (or designee) |
| RCC Athletics / sponsorship-approval contact | Jake Jones, Athletic Director & Head Baseball Coach |

*Proposed* values are sensible defaults — adjust to the actual season calendar.

## Still needs the parties' input (intentionally left yellow — not invented)

- **Student-Athlete** legal name, address, email, phone (once selected).
- **RCC authorized signatory** name, title, email, phone (whoever holds RCC
  contracting authority — typically an officer, not the AD).
- **Phone numbers** for RIVR Tech and RCC; RCC contact **email**.
- **RIVR Tech HR / Athletics-Compliance / Emergency** contacts (Exhibit E).
- **Exhibit B** sponsorship-benefit specifics (signage, social handles, event
  list, approved announcement text) — completed with RCC at execution.
- **NIL fields** (Exhibit D / §13.4) — only if RCC + counsel approve the opt-in.
- Signature blocks for **RCC** and the **Student-Athlete** are intentionally left
  blank for hand-signing.

Resolved in this official version: §6.7 (Option A), §24 venue (Robeson County,
NC), and the §6 / §19 pre-execution review flags (now operative clauses).

## Regenerating the documents

The Word/PDF files are produced by the stdlib + `python-docx` + `reportlab`
scripts under `generator/`. To change the amount or any fixed text and rebuild:

```bash
pip install python-docx reportlab
cd generator
python3 build_agreement.py     ../RIVRTECH_RCC_Student_Athlete_Sponsorship_Internship_Agreement.docx
python3 build_cover_letter.py  ../RIVRTECH_RCC_Proposal_Cover_Letter.docx
python3 build_checklist.py     ../RIVRTECH_RCC_Approval_Checklist.docx
python3 docx2pdf_render.py     ../RIVRTECH_RCC_Student_Athlete_Sponsorship_Internship_Agreement.docx \
                               ../RIVRTECH_RCC_Student_Athlete_Sponsorship_Internship_Agreement.pdf \
                               "RIVR Tech – RCC Student-Athlete Sponsorship & Paid Internship Agreement"
```

(You can also open the `.docx` in Word and print/export to PDF directly.)
