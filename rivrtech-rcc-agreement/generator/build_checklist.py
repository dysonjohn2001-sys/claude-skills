#!/usr/bin/env python3
"""Build the RIVR Tech / RCC Required Approvals Checklist (standalone)."""
import sys
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docgen import (new_document, add_header_footer, para, make_table, add_rich)

OUT = sys.argv[1] if len(sys.argv) > 1 else "checklist.docx"
FOOTER = "RIVR Tech – RCC Required Approvals Checklist"

doc = new_document()

para(doc, "RIVR Tech – ROBESON COMMUNITY COLLEGE", size=13, bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
para(doc, "Required Approvals Checklist", size=16, bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
para(doc, "Student-Athlete Corporate Sponsorship and Paid Internship Agreement",
     size=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

# Document control
make_table(doc, ["Field", "Detail"], [
    ["Version", "1.0 — Final"],
    ["Date", "August 24, 2026"],
    ["Owner", "John Dyson, Chief Operations Officer, LREMC Technologies, LLC d/b/a RIVR Tech"],
    ["Student-Athlete", "[STUDENT-ATHLETE’S FULL LEGAL NAME]"],
    ["Approval Status", "RCC approved; execution approvals pending"],
], col_widths=[1.8, 4.7])

para(doc, "This Agreement is not effective until the applicable approvals below are "
          "completed. Items marked “if applicable” depend on the "
          "circumstances (for example, whether the Student-Athlete is under 18 or "
          "whether NIL use is approved). This checklist mirrors Exhibit F of the "
          "Agreement.", size=10, space_before=6, space_after=8)

para(doc, "A.  RCC Approvals", size=12, bold=True, space_after=3)
make_table(doc, ["✓", "Item", "Responsible Party", "Date"], [
    ["[X]", "RCC Athletic Director approval", "[NAME]", "[  ]"],
    ["[X]", "RCC administration approval", "[NAME]", "[  ]"],
    ["[X]", "RCC legal review", "[NAME]", "[  ]"],
    ["[X]", "RCC athletics/NJCAA compliance review", "[NAME]", "[  ]"],
    ["[  ]", "Logo and trademark approval", "[NAME]", "[  ]"],
    ["[  ]", "Financial-aid disclosure", "[NAME]", "[  ]"],
], col_widths=[0.5, 3.3, 1.8, 0.9])

para(doc, "B.  RIVR Tech Approvals & Onboarding", size=12, bold=True,
     space_before=6, space_after=3)
make_table(doc, ["✓", "Item", "Responsible Party", "Date"], [
    ["[  ]", "RIVR Tech HR approval", "[NAME]", "[  ]"],
    ["[  ]", "RIVR Tech legal review", "[NAME]", "[  ]"],
    ["[  ]", "Payroll onboarding completed", "[NAME]", "[  ]"],
    ["[  ]", "Form I-9 completed", "[NAME]", "[  ]"],
    ["[  ]", "Federal and state tax forms completed", "[NAME]", "[  ]"],
    ["[  ]", "Direct-deposit or payroll election completed", "[NAME]", "[  ]"],
    ["[  ]", "Background check, if required", "[NAME]", "[  ]"],
    ["[  ]", "Confidentiality acknowledgment", "[NAME]", "[  ]"],
    ["[  ]", "Technology-policy acknowledgment", "[NAME]", "[  ]"],
], col_widths=[0.5, 3.3, 1.8, 0.9])

para(doc, "C.  Conditional / Situational Items", size=12, bold=True,
     space_before=6, space_after=3)
make_table(doc, ["✓", "Item", "Responsible Party", "Date"], [
    ["[  ]", "NIL authorization, if applicable", "[NAME]", "[  ]"],
    ["[  ]", "Youth Employment Certificate, if applicable", "[NAME]", "[  ]"],
    ["[  ]", "Parent/guardian consent, if applicable", "[NAME]", "[  ]"],
    ["[  ]", "Transportation acknowledgment", "[NAME]", "[  ]"],
    ["[  ]", "Emergency contact completed", "[NAME]", "[  ]"],
], col_widths=[0.5, 3.3, 1.8, 0.9])

para(doc, "Sign-Off", size=12, bold=True, space_before=8, space_after=3)
para(doc, "The undersigned confirm that the applicable approvals above have been "
          "completed and that the Agreement is cleared for execution.", size=10,
     space_after=8)
for role in ["RIVR Tech (John Dyson, Chief Operations Officer)",
             "Robeson Community College [AUTHORIZED REPRESENTATIVE / TITLE]"]:
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(10)
    add_rich(p, f"{role}\nSignature: ______________________________   Date: ____________")

add_header_footer(doc, FOOTER, header_banner="")
doc.save(OUT)
print("Saved", OUT)
