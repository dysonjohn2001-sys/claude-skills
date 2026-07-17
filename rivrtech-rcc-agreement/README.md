# RIVR Tech – RCC Student-Athlete Sponsorship & Paid Internship Package

**Status:** DRAFT FOR DISCUSSION AND LEGAL REVIEW — not for execution until reviewed
and approved by authorized representatives and legal counsel for **Robeson Community
College** and **LREMC Technologies, LLC d/b/a RIVR Tech**.

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

> **⚠ This advance-then-work-off model is flagged for legal + compliance review.**
> Paying a student-athlete up front and recouping it through work implicates the
> FLSA and the NC Wage and Hour Act (deduction limits; minimum wage each pay
> period), payroll/tax timing, and **NJCAA/conference eligibility**. Section 6.7
> leaves an explicit **Option A (repay unearned portion) / Option B (no repayment)**
> choice for counsel and athletics compliance to decide. "Sponsorship" (not
> "scholarship") is used deliberately to reduce athletic-aid characterization risk.

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
- **Section 6.7** — choose Option A or Option B for any unearned portion.
- **Exhibit B** sponsorship-benefit specifics (signage, social handles, event
  list, approved announcement text) — negotiated with RCC.
- **NIL fields** (Exhibit D / §13.4) — only if RCC + counsel approve the opt-in.
- Legal-review notes in **§6 (payment structure)**, **§19 (indemnity)**, and
  **§24 (venue)** stay flagged.
- Signature blocks for **RCC** and the **Student-Athlete** are intentionally left
  blank for hand-signing.

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
