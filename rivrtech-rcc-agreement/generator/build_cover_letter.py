#!/usr/bin/env python3
"""Build the RIVR Tech / RCC proposal cover letter (one page)."""
import sys
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docgen import (new_document, add_header_footer, para, add_rich, _set_run_font)

OUT = sys.argv[1] if len(sys.argv) > 1 else "cover_letter.docx"
FOOTER = "RIVR Tech – RCC Partnership Proposal"

doc = new_document()
# Business letters are single-spaced
doc.styles["Normal"].paragraph_format.line_spacing = 1.0

# Letterhead
para(doc, "LREMC Technologies, LLC d/b/a RIVR Tech", size=14, bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
para(doc, "6090 NC Highway 711 North · Pembroke, North Carolina 28372",
     size=9, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1,
     color=RGBColor(0x55, 0x55, 0x55))
para(doc, "john.dyson@lumbeeriver.com · [PHONE]", size=9, align=WD_ALIGN_PARAGRAPH.CENTER,
     space_after=8, color=RGBColor(0x55, 0x55, 0x55))

para(doc, "July 16, 2026", space_after=6)

# Addressee
para(doc, "Jake Jones", bold=True, space_after=0)
para(doc, "Athletic Director and Head Baseball Coach", space_after=0)
para(doc, "Robeson Community College", space_after=0)
para(doc, "5160 Fayetteville Road", space_after=0)
para(doc, "Lumberton, North Carolina 28360", space_after=8)

para(doc, "Re:  Proposed Corporate Sponsorship and Paid Student-Athlete "
          "Internship Partnership — Diamond Eagles Baseball Program", bold=True,
     space_after=6)

para(doc, "Dear Coach Jones:", space_after=5)

para(doc, "On behalf of LREMC Technologies, LLC d/b/a RIVR Tech (“RIVR Tech”), "
          "I am writing to propose a partnership with Robeson Community College "
          "that invests directly in your student-athletes and in our shared "
          "community. As a local company, we believe strongly in developing "
          "career-ready talent right here in Pembroke and Robeson County — and we "
          "would be proud to support the Diamond Eagles Baseball Program while "
          "doing it.", space_after=5)

para(doc, "Our proposed program combines two things: recognition of RIVR Tech as a "
          "local corporate sponsor of the baseball program, and a paid, "
          "career-building internship for a participating student-athlete. The "
          "intern would join our team as a Sales and Marketing Student Intern and "
          "gain real-world experience in sales, marketing, customer engagement, and "
          "business operations.", space_after=5)

para(doc, "We have designed the internship to work around your athletes, not the "
          "other way around. Scheduling would be flexible and built around classes, "
          "practices, games, travel, and examinations, with academics and athletics "
          "always taking priority. Our proposal is to provide a $2,000 sponsorship "
          "at the beginning of the semester, which the student-athlete then earns "
          "through paid sales and marketing work for RIVR Tech at $20.00 per hour "
          "(about 100 hours) — structured as legitimate, professional work "
          "experience, entirely separate from anything related to athletic "
          "performance, playing time, or team status.", space_after=5)

para(doc, "We recognize that a program like this must be done the right way. All "
          "terms remain subject to review and approval by Robeson Community "
          "College and to applicable employment and athletics-compliance "
          "requirements, including any applicable RCC, NJCAA, and conference rules. "
          "We are committed to full compliance and to following your lead on "
          "institutional policies and approvals.", space_after=5)

para(doc, "The agreement and an approvals checklist accompany this letter. "
          "I would welcome the opportunity to meet with you and the appropriate "
          "members of your administration, human resources, and compliance teams to "
          "finalize the structure in a way that works for the College. Thank you "
          "for considering this partnership and for all you do for your "
          "student-athletes — I look forward to the conversation.", space_after=12)

para(doc, "Sincerely,", space_after=12)
para(doc, "John Dyson", bold=True, space_after=0)
para(doc, "Chief Operations Officer", space_after=0)
para(doc, "LREMC Technologies, LLC d/b/a RIVR Tech", space_after=8)

para(doc, "Enclosures:  (1) Student-Athlete Corporate Sponsorship and Paid "
          "Internship Agreement (Official Version — Approved by Robeson Community "
          "College); (2) Required Approvals Checklist.", size=9,
     color=RGBColor(0x55, 0x55, 0x55))

add_header_footer(doc, FOOTER, header_banner="")
doc.save(OUT)
print("Saved", OUT)
