# RIVRTECH – RCC Student-Athlete Sponsorship & Paid Internship Package

**Status:** DRAFT FOR DISCUSSION AND LEGAL REVIEW — not for execution until reviewed
and approved by authorized representatives and legal counsel for **Robeson Community
College** and **LREMC Technologies, LLC d/b/a RIVRTECH**.

## Deliverables

| File | Description |
|------|-------------|
| `RIVRTECH_RCC_Student_Athlete_Sponsorship_Internship_Agreement.docx` | The full 21-page agreement (26 sections + Exhibits A–F + signature blocks). |
| `RIVRTECH_RCC_Student_Athlete_Sponsorship_Internship_Agreement.pdf` | PDF render of the agreement for review/printing. |
| `RIVRTECH_RCC_Proposal_Cover_Letter.docx` | One-page proposal letter to Jake Jones, Athletic Director & Head Baseball Coach. |
| `RIVRTECH_RCC_Approval_Checklist.docx` | Standalone approvals checklist (mirrors Exhibit F). |

All editable placeholders are **highlighted in yellow** (e.g., `[ZIP CODE]`,
`$[MAXIMUM DOLLAR AMOUNT]`, `[EFFECTIVE DATE]`). Font is **Arial 11 pt**; 1-inch
margins; page numbers and footer on every page; "DRAFT FOR DISCUSSION AND LEGAL
REVIEW" banner in the header.

## Maximum-hours calculation

The wage rate is fixed at **$20.00/hour**. Maximum hours are derived from the
sponsorship amount you enter:

```
Maximum Internship Hours = Maximum Dollar Amount ÷ $20.00
```

| Maximum Dollar Amount | Maximum Authorized Hours |
|----------------------:|-------------------------:|
| $2,500  | 125 |
| $5,000  | 250 |
| $7,500  | 375 |
| $10,000 | 500 |

Insert the agreed amount in Section 6.2, Exhibit A, and the checklist; the hours
figure is simply that amount divided by 20.

## Regenerating the documents

The Word/PDF files are produced by the stdlib + `python-docx` + `reportlab`
scripts under `generator/`. To change the dollar amount or any fixed text and
rebuild:

```bash
pip install python-docx reportlab
cd generator
python3 build_agreement.py     ../RIVRTECH_RCC_Student_Athlete_Sponsorship_Internship_Agreement.docx
python3 build_cover_letter.py  ../RIVRTECH_RCC_Proposal_Cover_Letter.docx
python3 build_checklist.py     ../RIVRTECH_RCC_Approval_Checklist.docx
python3 docx2pdf_render.py     ../RIVRTECH_RCC_Student_Athlete_Sponsorship_Internship_Agreement.docx \
                               ../RIVRTECH_RCC_Student_Athlete_Sponsorship_Internship_Agreement.pdf \
                               "RIVRTECH – RCC Student-Athlete Sponsorship & Paid Internship Agreement"
```

(You can also open the `.docx` in Word and print/export to PDF directly.)
