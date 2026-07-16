#!/usr/bin/env python3
"""Build the STUDENT-ATHLETE CORPORATE SPONSORSHIP AND PAID INTERNSHIP AGREEMENT."""
import sys
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docgen import (new_document, add_header_footer, para, section_heading,
                    sub_heading, bullet, numbered, page_break, quote_block,
                    add_rich, make_table, shade_cell, set_cell_text, _set_run_font)

OUT = sys.argv[1] if len(sys.argv) > 1 else "agreement.docx"

RIVR_FULL = "LREMC Technologies, LLC d/b/a RIVRTECH"
FOOTER = "RIVRTECH – RCC Student-Athlete Sponsorship & Paid Internship Agreement"

doc = new_document()

# =====================================================================
# TITLE PAGE
# =====================================================================
para(doc, "", space_after=40)
p = para(doc, "STUDENT-ATHLETE CORPORATE SPONSORSHIP", size=22, bold=True,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
para(doc, "AND PAID INTERNSHIP AGREEMENT", size=22, bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=18)

# thin rule via paragraph border
para(doc, "— DRAFT FOR DISCUSSION AND LEGAL REVIEW —", size=12, bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, color=RGBColor(0xB0, 0x00, 0x00), space_after=40)

para(doc, "By and among:", size=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)
para(doc, "LREMC Technologies, LLC d/b/a RIVRTECH", size=13, bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
para(doc, "Robeson Community College", size=13, bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
para(doc, "and", size=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
para(doc, "[STUDENT-ATHLETE’S FULL LEGAL NAME]", size=13, bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=40)

para(doc, "Robeson Community College Diamond Eagles Baseball Program",
     size=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
para(doc, "(subject to confirmation by Robeson Community College)",
     size=10, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
para(doc, "2026–2027 Baseball Season", size=11, italic=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=50)

para(doc, "Prepared by / on behalf of the corporate sponsor:", size=10,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
para(doc, "LREMC Technologies, LLC d/b/a RIVRTECH", size=11, bold=True,
     align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
para(doc, "6090 NC Highway 711 North, Pembroke, North Carolina 28372",
     size=10, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)

page_break(doc)

# =====================================================================
# DOCUMENT CONTROL + LEGAL REVIEW NOTE + CONTENTS
# =====================================================================
para(doc, "Document Control", size=14, bold=True, space_after=6)
make_table(
    doc,
    ["Field", "Detail"],
    [
        ["Document Title", "Student-Athlete Corporate Sponsorship and Paid Internship Agreement"],
        ["Version", "0.1 — Draft"],
        ["Date", "July 16, 2026"],
        ["Document Owner", "John Dyson, Chief Operations Officer, LREMC Technologies, LLC d/b/a RIVRTECH"],
        ["Prepared For", "Robeson Community College – Athletic Department & Administration"],
        ["Approval Status", "Draft — Pending business, HR, athletics-compliance, and legal review"],
        ["Classification", "Confidential – Draft for Discussion"],
    ],
    col_widths=[2.0, 4.5],
)

para(doc, "", space_after=6)
para(doc, "Legal Review Note", size=14, bold=True, space_before=8, space_after=4)
p = doc.add_paragraph()
p.paragraph_format.left_indent = Inches(0.2)
p.paragraph_format.right_indent = Inches(0.2)
p.paragraph_format.space_after = Pt(6)
add_rich(p, "“This draft is provided for discussion and planning purposes. "
            "It must be reviewed and approved by authorized representatives and legal "
            "counsel for Robeson Community College and LREMC Technologies, LLC d/b/a "
            "RIVRTECH before execution.”", italic=True, bold=True)

para(doc, "This document has not been reviewed or approved by Robeson Community "
          "College, its Athletic Department, its administration, the NJCAA, or any "
          "conference. It does not create any binding obligation until fully executed "
          "by all required parties and approved through the processes identified in "
          "Exhibit F.", size=10, space_after=10)

# Contents overview (no page numbers to avoid mismatch)
para(doc, "Contents", size=14, bold=True, space_before=6, space_after=4)
contents = [
    "Recitals", "1. Parties and Effective Date", "2. Purpose of the Partnership",
    "3. Agreement Term", "4. Sponsorship Recognition", "5. Paid Internship Position",
    "6. Compensation and Maximum Hours", "7. Internship Duties",
    "8. Work Schedule and Academic Priority", "9. Work Location and Transportation",
    "10. Dress and Professional Appearance",
    "11. Supervision and Performance Expectations",
    "12. Student-Athlete Eligibility and Athletics Compliance",
    "13. Name, Image, and Likeness (NIL)",
    "14. Confidentiality and Customer Information",
    "15. Technology, Social Media, and Public Statements",
    "16. Workplace Conduct",
    "17. Employment Status, Benefits, and Workers’ Compensation",
    "18. Financial Aid and Tax Disclosure",
    "19. Insurance and Allocation of Responsibility", "20. Termination",
    "21. No Guarantee of Team Position or Playing Time",
    "22. Independent Parties and No Agency", "23. Compliance With Law",
    "24. Governing Law and Venue", "25. Notices", "26. Standard Contract Terms",
    "Signature Blocks",
    "Exhibit A – Internship Position Description",
    "Exhibit B – Sponsorship Recognition and Benefits Schedule",
    "Exhibit C – Student-Athlete Schedule and Timesheet",
    "Exhibit D – Limited NIL and Media Authorization",
    "Exhibit E – Program Contacts and Reporting Procedures",
    "Exhibit F – Required Approvals Checklist",
]
for c in contents:
    cp = doc.add_paragraph()
    cp.paragraph_format.left_indent = Inches(0.25)
    cp.paragraph_format.space_after = Pt(1)
    add_rich(cp, c, size=10)

page_break(doc)

# =====================================================================
# PREAMBLE + RECITALS
# =====================================================================
para(doc, "STUDENT-ATHLETE CORPORATE SPONSORSHIP AND PAID INTERNSHIP AGREEMENT",
     size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)

para(doc, "This Student-Athlete Corporate Sponsorship and Paid Internship "
          "Agreement (this “Agreement”) is entered into as of the date of the "
          "last signature below "
          "(the “Effective Date”), by and among LREMC Technologies, LLC d/b/a "
          "RIVRTECH (“RIVRTECH”); Robeson Community College (“RCC” or the "
          "“College”); and [STUDENT-ATHLETE’S FULL LEGAL NAME] (the "
          "“Student-Athlete”). RIVRTECH, RCC, and the Student-Athlete are "
          "each a “Party” and together the “Parties.”")

sub_heading(doc, "Recitals")
recitals = [
    ("A.", "RCC operates an intercollegiate athletics program that includes a "
     "baseball program (the “Robeson Community College Diamond Eagles Baseball "
     "Program,” subject to confirmation by RCC)."),
    ("B.", "RIVRTECH is a local company that desires to support local "
     "student-athletes and the surrounding community while providing meaningful "
     "professional development and real-world work experience."),
    ("C.", "RCC supports appropriate workforce-development and professional "
     "opportunities for its students, provided that such opportunities do not "
     "interfere with a student-athlete’s education, athletic participation, "
     "eligibility, or other College responsibilities."),
    ("D.", "The Student-Athlete desires to participate in a paid internship with "
     "RIVRTECH and agrees to perform all assigned duties professionally, "
     "reliably, and in accordance with applicable policies and law."),
    ("E.", "The Parties intend for this Agreement, and all activities under it, to "
     "comply with applicable federal and North Carolina law, RCC policies, "
     "applicable NJCAA rules, applicable conference rules, and other applicable "
     "athletics requirements. [Confirm applicable athletics governing bodies and "
     "rules with RCC.]"),
    ("F.", "The Parties acknowledge that any compensation paid under this Agreement "
     "is provided solely in exchange for legitimate work and professional services "
     "actually performed, and not for athletic performance or any athletics-related "
     "consideration described in Section 6."),
]
for tag, text in recitals:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.55)
    p.paragraph_format.first_line_indent = Inches(-0.3)
    p.paragraph_format.space_after = Pt(4)
    add_rich(p, f"{tag}\t{text}")

para(doc, "NOW, THEREFORE, in consideration of the mutual promises and covenants "
          "set forth in this Agreement, and for other good and valuable "
          "consideration, the receipt and sufficiency of which are acknowledged, "
          "the Parties agree as follows:", space_before=6)

# =====================================================================
# SECTION 1 - PARTIES AND EFFECTIVE DATE
# =====================================================================
section_heading(doc, 1, "Parties and Effective Date")
para(doc, "1.1  Effective Date. This Agreement is effective as of the Effective "
          "Date stated above and continues for the Agreement Term described in "
          "Section 3, unless earlier terminated.")
para(doc, "1.2  Parties and Contact Information. The Parties and their contact "
          "information are:")

make_table(
    doc,
    ["Party", "Address", "Email / Telephone"],
    [
        ["LREMC Technologies, LLC d/b/a RIVRTECH (“RIVRTECH”)",
         "6090 NC Highway 711 North, Pembroke, North Carolina 28372",
         "Email: john.dyson@lumbeeriver.com\nTelephone: [PHONE]"],
        ["Robeson Community College (“RCC”)",
         "5160 Fayetteville Road, Lumberton, North Carolina 28360",
         "Email: [EMAIL]\nTelephone: [PHONE]"],
        ["[STUDENT-ATHLETE’S FULL LEGAL NAME]",
         "[STUDENT-ATHLETE ADDRESS]",
         "Email: [EMAIL]\nTelephone: [PHONE]"],
    ],
    col_widths=[1.9, 2.5, 2.1],
)
para(doc, "1.3  Primary RIVRTECH Work Location. The primary work location for the "
          "internship is LREMC Technologies, LLC d/b/a RIVRTECH, 6090 NC Highway 711 "
          "North, Pembroke, North Carolina 28372, and such other approved work "
          "or event locations as RIVRTECH may reasonably assign.", space_before=4)

# =====================================================================
# SECTION 2 - PURPOSE OF THE PARTNERSHIP
# =====================================================================
section_heading(doc, 2, "Purpose of the Partnership")
para(doc, "2.1  This Agreement establishes a community partnership between RIVRTECH "
          "and RCC, supported by the Student-Athlete’s participation in a paid "
          "internship. The Parties share a commitment to developing career-ready "
          "student-athletes and strengthening the local workforce.")
para(doc, "2.2  The partnership is intended to support:")
for item in [
    "local workforce development and economic opportunity in the Pembroke and "
    "Robeson County community;",
    "career readiness and professional development for the Student-Athlete;",
    "real-world experience in sales, marketing, customer engagement, and business "
    "operations;",
    "community engagement and outreach;",
    "RCC athletics, including appropriate support for the Diamond Eagles Baseball "
    "Program (subject to confirmation by RCC); and",
    "the academic and athletic success of the Student-Athlete.",
]:
    bullet(doc, item)
para(doc, "2.3  The Parties intend that the internship enhance — and never "
          "detract from — the Student-Athlete’s education, athletic "
          "participation, and eligibility.", space_before=2)

# =====================================================================
# SECTION 3 - AGREEMENT TERM
# =====================================================================
section_heading(doc, 3, "Agreement Term")
para(doc, "3.1  Term. This Agreement begins on September 1, 2026 and, unless "
          "earlier terminated under Section 20, ends on May 31, 2027 (the "
          "“Agreement Term”).")
para(doc, "3.2  Season. The Agreement Term corresponds to activities associated "
          "with the 2026–2027 baseball season, unless the Parties agree "
          "otherwise in writing.")
para(doc, "3.3  Maximum Duration. In no event will the Agreement Term exceed "
          "twelve (12) months without a written extension.")
para(doc, "3.4  Extension. Any extension or renewal of this Agreement must be "
          "approved in writing and signed by all required parties, including any "
          "approvals required under Exhibit F.")

# =====================================================================
# SECTION 4 - SPONSORSHIP RECOGNITION
# =====================================================================
section_heading(doc, 4, "Sponsorship Recognition")
para(doc, "4.1  Recognition Opportunities. Subject to RCC’s prior written "
          "approval and applicable policies, RCC may provide RIVRTECH with "
          "reasonable, school-approved recognition as a local corporate sponsor "
          "supporting the Diamond Eagles Baseball Program and the Student-Athlete, "
          "which may include:")
for item in [
    "identification of RIVRTECH as a corporate sponsor of the program;",
    "approved recognition on RCC athletics materials;",
    "approved social media recognition;",
    "recognition at selected baseball events;",
    "opportunities for RIVRTECH representatives to attend approved athletic or "
    "community events; and",
    "other mutually agreed promotional opportunities.",
]:
    bullet(doc, item)
para(doc, "4.2  Approvals and Institutional Control. The Parties acknowledge and "
          "agree that:", space_before=2)
for item in [
    "all uses of RCC’s name, logo, colors, trademarks, photographs, uniforms, "
    "facilities, and branding require RCC’s prior written approval;",
    "RIVRTECH does not automatically receive exclusive sponsorship rights of any "
    "kind;",
    "RCC retains full control of its institutional marks and its athletics "
    "operations; and",
    "the final, agreed recognition benefits will be listed in the attached "
    "Sponsorship Benefits Schedule (Exhibit B).",
]:
    bullet(doc, item)
para(doc, "4.3  Compliance. All sponsorship recognition is subject to applicable "
          "RCC policies and applicable NJCAA and conference rules. [Confirm "
          "permissible recognition with RCC athletics compliance.]", space_before=2)

# =====================================================================
# SECTION 5 - PAID INTERNSHIP POSITION
# =====================================================================
section_heading(doc, 5, "Paid Internship Position")
para(doc, "5.1  Position. RIVRTECH will employ the Student-Athlete in the position "
          "of “Sales and Marketing Student Intern” (the “Internship”).")
para(doc, "5.2  Classification. The Student-Athlete is employed by RIVRTECH as a "
          "temporary, part-time, non-exempt, paid employee. The Student-Athlete is "
          "not an employee or agent of RCC for any purpose under this Agreement.")
para(doc, "5.3  No Guarantee of Future Employment. The Internship is temporary and "
          "does not guarantee or imply any offer of continued or future employment "
          "with RIVRTECH.")

# =====================================================================
# SECTION 6 - COMPENSATION AND MAXIMUM HOURS
# =====================================================================
section_heading(doc, 6, "Compensation and Maximum Hours")
para(doc, "6.1  Wage Rate. RIVRTECH will pay the Student-Athlete $20.00 per hour "
          "for actual, authorized hours worked.")
para(doc, "6.2  Maximum Compensation. The Student-Athlete may earn up to "
          "$2,000.00 in total gross wages during the Agreement Term "
          "(the “Maximum Compensation”).")
para(doc, "6.3  Maximum Authorized Hours. Because the wage rate is fixed at $20.00 "
          "per hour, the maximum number of internship hours is calculated as:")
quote_block(doc, "Maximum Internship Hours = Maximum Dollar Amount ÷ $20.00")
p = doc.add_paragraph()
p.paragraph_format.left_indent = Inches(0.4)
p.paragraph_format.space_after = Pt(6)
add_rich(p, "“At a maximum compensation amount of $2,000.00 and "
            "an hourly wage of $20.00, the Student-Athlete may work up to "
            "100 authorized hours during the Agreement Term.”", italic=True)

para(doc, "6.4  Payroll. All wages are paid through RIVRTECH’s normal payroll "
          "process on RIVRTECH’s regular payroll schedule, less all legally "
          "required deductions and withholdings.", space_before=4)
para(doc, "6.5  Pay for Hours Actually Worked; No Advance Wages. The Student-Athlete "
          "is paid only for actual hours worked. Compensation will not be paid in "
          "advance as wages for hours that have not yet been worked.")
para(doc, "6.6  Timekeeping and Authorization. The Student-Athlete must accurately "
          "record all time worked and submit timesheets for approval by the "
          "designated RIVRTECH supervisor (see Exhibit C). All work must be "
          "authorized in advance. Off-the-clock work is prohibited.")
para(doc, "6.7  Overtime. Unauthorized overtime is prohibited, and overtime hours "
          "should not be scheduled without advance written approval. If, however, "
          "the Student-Athlete works more than forty (40) hours in a workweek, "
          "RIVRTECH will pay all legally required overtime in accordance with "
          "applicable law.")
para(doc, "6.8  No Debt for Unworked Hours. Failure to work the maximum number of "
          "available hours does not create any debt owed by the Student-Athlete to "
          "RIVRTECH. The Student-Athlete will simply be paid for the actual, "
          "approved hours worked.")
para(doc, "6.9  Nature of Compensation. The Parties expressly agree that all "
          "compensation under this Agreement is paid solely for legitimate work and "
          "professional services actually performed. It is NOT, in whole or in part, "
          "compensation for any of the following:")
for item in [
    "athletic performance;", "statistics or awards;", "playing time;",
    "enrollment at RCC;", "remaining on the baseball team;",
    "recruiting commitments;", "attendance at a particular college;",
    "winning games; or",
    "any improper influence over an athletic decision.",
]:
    bullet(doc, item)

# =====================================================================
# SECTION 7 - INTERNSHIP DUTIES
# =====================================================================
section_heading(doc, 7, "Internship Duties")
para(doc, "7.1  Duties. The Student-Athlete’s duties may include the following, "
          "as assigned and supervised by RIVRTECH:")
for item in [
    "assisting with community sales and marketing events;",
    "representing RIVRTECH at approved outreach events;",
    "supporting residential and business sales initiatives;",
    "assisting with prospective-customer outreach;",
    "entering and organizing authorized sales leads;",
    "making supervised follow-up calls;",
    "assisting with promotional campaigns;",
    "preparing event materials;",
    "supporting customer-education initiatives;",
    "helping with office-based sales activities;",
    "conducting basic market research;",
    "assisting with social media or digital marketing content when authorized;",
    "helping organize sponsorship and community events;",
    "attending sales and product training;",
    "maintaining accurate activity records; and",
    "performing other reasonable, non-hazardous duties related to sales, "
    "marketing, and professional development.",
]:
    bullet(doc, item)
para(doc, "7.2  Limitations on Authority and Duties. The Student-Athlete is NOT "
          "authorized to, and will not:", space_before=2)
for item in [
    "sign contracts;",
    "make binding commitments for RIVRTECH;",
    "collect or personally retain customer payments;",
    "access customer information without authorization;",
    "represent that the Student-Athlete can guarantee service availability;",
    "drive a company vehicle without separate written authorization;",
    "perform construction, electrical, fiber-splicing, climbing, or other "
    "hazardous work; or",
    "perform any work prohibited by law or by RIVRTECH policy.",
]:
    bullet(doc, item)

# =====================================================================
# SECTION 8 - WORK SCHEDULE AND ACADEMIC PRIORITY
# =====================================================================
section_heading(doc, 8, "Work Schedule and Academic Priority")
para(doc, "8.1  The Parties agree that academics and required athletic activities "
          "take priority over the Internship. Specifically:")
for item in [
    "work hours will be scheduled by mutual agreement;",
    "the Student-Athlete’s academic requirements and required athletic "
    "activities will be reasonably accommodated;",
    "the Student-Athlete must provide reasonable advance notice of classes, "
    "practices, games, travel, examinations, and schedule changes;",
    "work will not be performed during required class time;",
    "the normal work schedule will not exceed ten (10) hours per week unless "
    "approved in advance;",
    "the Internship must not interfere with the Student-Athlete’s academic "
    "progress or athletic eligibility; and",
    "RCC may communicate scheduling concerns to RIVRTECH, subject to applicable "
    "privacy rules and the Student-Athlete’s written authorization.",
]:
    bullet(doc, item)

# =====================================================================
# SECTION 9 - WORK LOCATION AND TRANSPORTATION
# =====================================================================
section_heading(doc, 9, "Work Location and Transportation")
quote_block(doc, "The Student-Athlete is responsible for maintaining dependable "
                 "transportation to and from the primary RIVRTECH work location at "
                 "6090 NC Highway 711 North, Pembroke, North Carolina, and to other "
                 "approved work or event locations. Transportation to and from the "
                 "Student-Athlete’s regular work location is the "
                 "Student-Athlete’s responsibility and is not considered "
                 "compensable work time, except where otherwise required by law.")
para(doc, "9.1  Travel Between Work Locations. Travel between assigned work "
          "locations during the workday will be handled under RIVRTECH’s "
          "applicable travel-time and mileage-reimbursement policies.")

# =====================================================================
# SECTION 10 - DRESS AND PROFESSIONAL APPEARANCE
# =====================================================================
section_heading(doc, 10, "Dress and Professional Appearance")
quote_block(doc, "During office hours, meetings, sales activities, and other "
                 "assigned working hours, the Student-Athlete must wear "
                 "business-casual attire unless RIVRTECH approves event-specific "
                 "apparel. Clothing must be clean, professional, appropriate for the "
                 "assigned duties, and consistent with RIVRTECH workplace policies.")
para(doc, "10.1  RIVRTECH-branded clothing is permitted, and may be required, for "
          "approved community and marketing events.")

# =====================================================================
# SECTION 11 - SUPERVISION AND PERFORMANCE
# =====================================================================
section_heading(doc, 11, "Supervision and Performance Expectations")
para(doc, "11.1  Supervision. The Student-Athlete will report to a designated "
          "RIVRTECH supervisor (the “Supervisor,” identified in Exhibit E). "
          "A designated RCC athletics contact will serve as the College’s point "
          "of contact for program coordination (also identified in Exhibit E).")
para(doc, "11.2  Expectations. The Student-Athlete agrees to:")
for item in [
    "complete orientation and training as directed;",
    "maintain punctuality and reliable attendance;",
    "provide advance notice of absences whenever possible;",
    "communicate professionally with employees and customers;",
    "treat employees, customers, and community members with respect;",
    "complete assigned work in a timely and accurate manner;",
    "adhere to RIVRTECH company policies; and",
    "participate in periodic progress reviews.",
]:
    bullet(doc, item)
para(doc, "11.3  Evaluation. At the conclusion of the Internship, RIVRTECH will "
          "provide an end-of-program evaluation or certificate of completion.",
     space_before=2)

# =====================================================================
# SECTION 12 - ELIGIBILITY AND ATHLETICS COMPLIANCE
# =====================================================================
section_heading(doc, 12, "Student-Athlete Eligibility and Athletics Compliance")
para(doc, "12.1  The Parties acknowledge and agree that:")
for item in [
    "the Student-Athlete must disclose this arrangement to RCC as and to the extent "
    "required by applicable RCC, NJCAA, or conference rules;",
    "this arrangement is subject to applicable RCC, NJCAA, conference, and other "
    "applicable athletics rules;",
    "RCC does not guarantee the Student-Athlete’s continued athletic "
    "eligibility;",
    "compensation is based solely on legitimate work actually performed;",
    "compensation is not contingent upon athletic participation, performance, "
    "playing time, recruiting, enrollment, or team status;",
    "coaches will not control payroll, hours, or employment evaluations;",
    "employment decisions will be made solely by RIVRTECH;",
    "this arrangement does not require the Student-Athlete to attend or remain "
    "enrolled at RCC if such a requirement would violate applicable athletics "
    "rules; and",
    "the Parties will promptly modify or terminate any provision determined to "
    "violate applicable law or applicable athletics requirements.",
]:
    bullet(doc, item)
para(doc, "12.2  Compliance Confirmation. [Confirm all applicable disclosure and "
          "approval requirements with RCC’s athletics compliance office before "
          "execution.]", size=10, space_before=2)

# =====================================================================
# SECTION 13 - NIL
# =====================================================================
section_heading(doc, 13, "Name, Image, and Likeness (NIL)")
para(doc, "13.1  Limited NIL Provision — Applies Only If Separately Approved. "
          "This Section 13 applies ONLY if RCC and the Student-Athlete approve NIL "
          "use in writing (see Exhibit D). Hourly wages under Section 6 do not "
          "purchase, and are not intended to purchase, any NIL rights.")
para(doc, "13.2  If approved in writing, the limited NIL authorization may include:")
for item in [
    "approved use of the Student-Athlete’s name, image, voice, likeness, "
    "biography, and approved photographs;",
    "defined media and promotional purposes;",
    "an approval process for all promotional content;",
    "specific beginning and ending dates;",
    "defined geographic and media scope;",
    "a prohibition on implying RCC endorsement beyond approved sponsorship "
    "recognition;",
    "no use of RCC uniforms, logos, facilities, or marks without RCC’s prior "
    "written approval;",
    "Student-Athlete representations that the approved materials do not violate any "
    "other agreement;",
    "RIVRTECH’s right to revoke future use for material breach or for legal or "
    "compliance reasons; and",
    "removal of future promotional use after this Agreement ends, subject to "
    "reasonable archival use.",
]:
    bullet(doc, item)
para(doc, "13.3  No Assumption of Rights. The Parties do not assume that hourly "
          "wages automatically grant RIVRTECH any unrestricted NIL rights. Any NIL "
          "use must be separately approved as set out in Exhibit D.", space_before=2)

sub_heading(doc, "13.4  Optional Separate NIL Fee — USE ONLY IF APPROVED BY RCC "
                 "AND LEGAL COUNSEL")
para(doc, "If RIVRTECH will pay a separate NIL fee, the following optional terms "
          "apply and are separate from the hourly internship wages in Section 6:")
for item in [
    "Separate NIL compensation amount: $[NIL FEE AMOUNT];",
    "Specific promotional deliverables: [DESCRIBE DELIVERABLES];",
    "Payment schedule: [NIL PAYMENT SCHEDULE];",
    "Approval requirements: written approval by RCC and the Student-Athlete, and "
    "legal-counsel review; and",
    "Confirmation: the NIL fee is separate from, and in addition to, the hourly "
    "internship wages, and is not payment for athletic performance or any other "
    "item listed in Section 6.9.",
]:
    bullet(doc, item)
para(doc, "[USE ONLY IF APPROVED BY RCC AND LEGAL COUNSEL.]", size=10, bold=True,
     space_before=2)

# =====================================================================
# SECTION 14 - CONFIDENTIALITY
# =====================================================================
section_heading(doc, 14, "Confidentiality and Customer Information")
para(doc, "14.1  Confidential Information. During and after the Internship, the "
          "Student-Athlete will protect and keep confidential the following "
          "information belonging to RIVRTECH or its customers:")
for item in [
    "customer information;", "prospective-customer information;",
    "pricing information;", "sales strategies;", "internal business records;",
    "network information;", "employee information;", "passwords and systems;",
    "proprietary materials; and", "other confidential information.",
]:
    bullet(doc, item)
para(doc, "14.2  Return and Deletion. When the Internship ends (or upon "
          "RIVRTECH’s request), the Student-Athlete will promptly return and, "
          "as directed, delete all RIVRTECH information and materials in the "
          "Student-Athlete’s possession.", space_before=2)
para(doc, "14.3  General Skills Preserved. Nothing in this Section prevents the "
          "Student-Athlete from using the general skills, knowledge, and experience "
          "gained during the Internship. This provision is not intended to operate "
          "as an unreasonably broad restriction.")

# =====================================================================
# SECTION 15 - TECHNOLOGY / SOCIAL MEDIA
# =====================================================================
section_heading(doc, 15, "Technology, Social Media, and Public Statements")
para(doc, "15.1  Policy Compliance. The Student-Athlete will comply with "
          "RIVRTECH’s applicable policies, including its:")
for item in [
    "acceptable-use policies;", "cybersecurity rules;", "social media policies;",
    "customer privacy requirements; and", "brand standards.",
]:
    bullet(doc, item)
para(doc, "15.2  No Unauthorized Statements. The Student-Athlete may not make any "
          "unauthorized statements on behalf of RIVRTECH or RCC.", space_before=2)

# =====================================================================
# SECTION 16 - WORKPLACE CONDUCT
# =====================================================================
section_heading(doc, 16, "Workplace Conduct")
para(doc, "16.1  Standards. The Student-Athlete will comply with applicable "
          "conduct standards, including:")
for item in [
    "anti-discrimination rules;", "anti-harassment rules;",
    "workplace safety requirements;", "drug-free workplace policies;",
    "violence-prevention policies;", "professional conduct standards; and",
    "applicable RCC student conduct requirements.",
]:
    bullet(doc, item)
para(doc, "16.2  Reporting. Workplace or program concerns may be reported to the "
          "contacts listed in Exhibit E, including RIVRTECH Human Resources and the "
          "RCC athletics contact.", space_before=2)

# =====================================================================
# SECTION 17 - EMPLOYMENT STATUS
# =====================================================================
section_heading(doc, 17, "Employment Status, Benefits, and Workers’ Compensation")
para(doc, "17.1  The Parties acknowledge and agree that:")
for item in [
    "RIVRTECH is the sole employer for the paid Internship;",
    "the Student-Athlete is a temporary, part-time, non-exempt employee of "
    "RIVRTECH;",
    "the Student-Athlete will receive only those benefits required by law or "
    "expressly stated in RIVRTECH policy;",
    "RIVRTECH will provide workers’ compensation coverage as required by law;",
    "RCC is not responsible for payroll, taxes, workers’ compensation, or "
    "employment supervision for the Internship; and",
    "nothing in this Agreement creates an employment relationship between RCC and "
    "the Student-Athlete.",
]:
    bullet(doc, item)

# =====================================================================
# SECTION 18 - FINANCIAL AID AND TAX
# =====================================================================
section_heading(doc, 18, "Financial Aid and Tax Disclosure")
para(doc, "18.1  The Parties acknowledge and agree that:")
for item in [
    "wages and any separate NIL payments may have tax consequences;",
    "compensation may affect financial-aid reporting or other benefit eligibility;",
    "the Student-Athlete is responsible for making any required disclosures;",
    "RCC may advise the Student-Athlete to consult the RCC Financial Aid Office; "
    "and",
    "the Parties are not providing personal tax advice to the Student-Athlete.",
]:
    bullet(doc, item)

# =====================================================================
# SECTION 19 - INSURANCE / ALLOCATION
# =====================================================================
section_heading(doc, 19, "Insurance and Allocation of Responsibility")
para(doc, "[FLAG FOR LEGAL REVIEW — RCC is a North Carolina public community "
          "college; indemnification and liability terms are subject to limitations "
          "under North Carolina law and must be reviewed and approved by RCC legal "
          "counsel.]", size=10, bold=True)
para(doc, "19.1  Each Party’s Responsibilities. Subject to and to the extent "
          "permitted by North Carolina law:")
for item in [
    "RIVRTECH is responsible for its own workplace and its employees;",
    "RCC is responsible for its own premises and institutional activities;",
    "each Party is responsible for its own negligent acts or omissions, to the "
    "extent allowed by North Carolina law; and",
    "each Party will maintain applicable insurance coverage consistent with its "
    "responsibilities.",
]:
    bullet(doc, item)
para(doc, "19.2  No Student-Athlete Indemnity. No broad indemnification obligation "
          "is imposed on the Student-Athlete under this Agreement.", space_before=2)
para(doc, "19.3  Public-College Limitations. Nothing in this Agreement is intended "
          "to require RCC to indemnify any Party in a manner inconsistent with "
          "limitations applicable to a North Carolina public community college. "
          "[Confirm permissible allocation and insurance terms with RCC counsel.]")

# =====================================================================
# SECTION 20 - TERMINATION
# =====================================================================
section_heading(doc, 20, "Termination")
para(doc, "20.1  Termination Events. This Agreement (and/or the Internship) may be "
          "terminated:")
for item in [
    "by mutual written agreement of the Parties;",
    "by RIVRTECH for misconduct, attendance problems, policy violations, poor "
    "performance, safety concerns, or legitimate business reasons;",
    "by RCC for athletics compliance, student welfare, academic, institutional, or "
    "policy concerns;",
    "by the Student-Athlete upon written notice;",
    "automatically upon expiration of the Agreement Term;",
    "if the arrangement becomes legally impermissible; or",
    "if the Student-Athlete is no longer eligible to participate, when the "
    "Student-Athlete’s continued participation is essential to the approved "
    "sponsorship component.",
]:
    bullet(doc, item)
para(doc, "20.2  Payment on Termination. Upon any termination, the Student-Athlete "
          "will be paid all wages legally due for hours already worked.",
     space_before=2)

# =====================================================================
# SECTION 21 - NO GUARANTEE OF POSITION
# =====================================================================
section_heading(doc, 21, "No Guarantee of Team Position or Playing Time")
para(doc, "21.1  The Parties clearly agree that:")
for item in [
    "RIVRTECH has no control over team selection, playing time, coaching "
    "decisions, discipline, scholarships, or athletics eligibility;",
    "RCC and its coaches retain exclusive authority over all athletics decisions; "
    "and",
    "neither the Internship nor the sponsorship guarantees roster placement or "
    "playing time.",
]:
    bullet(doc, item)

# =====================================================================
# SECTION 22 - INDEPENDENT PARTIES
# =====================================================================
section_heading(doc, 22, "Independent Parties and No Agency")
para(doc, "22.1  RCC and RIVRTECH remain independent entities. Neither may bind the "
          "other, and neither is the agent, partner, or joint venturer of the other, "
          "without express written authority.")

# =====================================================================
# SECTION 23 - COMPLIANCE WITH LAW
# =====================================================================
section_heading(doc, 23, "Compliance With Law")
para(doc, "23.1  Applicable Requirements. The Parties will comply with applicable "
          "law and requirements, including:")
for item in [
    "the Fair Labor Standards Act (FLSA);",
    "the North Carolina Wage and Hour Act;",
    "applicable tax and payroll requirements;",
    "applicable youth-employment requirements if the Student-Athlete is under 18;",
    "applicable RCC policies;",
    "applicable NJCAA requirements;",
    "applicable conference rules; and",
    "other governing requirements.",
]:
    bullet(doc, item)
sub_heading(doc, "23.2  Minors (If the Student-Athlete Is Under 18)")
para(doc, "If the Student-Athlete is under 18 at any time during the Agreement Term, "
          "the following also apply:")
for item in [
    "parent or guardian consent is required;",
    "a North Carolina Youth Employment Certificate is required, if applicable;",
    "applicable restrictions on hours and job duties will be followed; and",
    "the additional parent/guardian signature block must be completed.",
]:
    bullet(doc, item)

# =====================================================================
# SECTION 24 - GOVERNING LAW AND VENUE
# =====================================================================
section_heading(doc, 24, "Governing Law and Venue")
para(doc, "24.1  Governing Law. This Agreement is governed by the laws of the State "
          "of North Carolina, without regard to its conflict-of-laws principles.")
para(doc, "24.2  Venue. Venue for any dispute will be [VENUE — TO BE CONFIRMED "
          "BY RCC AND RIVRTECH COUNSEL]. [Legal-review note: do not finalize venue "
          "until RCC and RIVRTECH counsel approve; venue for a North Carolina public "
          "community college may be subject to specific requirements.]")

# =====================================================================
# SECTION 25 - NOTICES
# =====================================================================
section_heading(doc, 25, "Notices")
para(doc, "25.1  All notices under this Agreement must be in writing and delivered "
          "to the following (or to such updated contact as a Party designates in "
          "writing):")

make_table(
    doc,
    ["RIVRTECH", "RCC", "Student-Athlete"],
    [[
        "John Dyson\nChief Operations Officer\nLREMC Technologies, LLC d/b/a "
        "RIVRTECH\n6090 NC Highway 711 North\nPembroke, North Carolina 28372\n"
        "Email: john.dyson@lumbeeriver.com\nTelephone: [PHONE]",
        "[AUTHORIZED RCC REPRESENTATIVE]\n[TITLE]\nRobeson Community College\n"
        "5160 Fayetteville Road\nLumberton, North Carolina 28360\nEmail: [EMAIL]\n"
        "Telephone: [PHONE]",
        "[NAME]\n[ADDRESS]\nEmail: [EMAIL]\nTelephone: [PHONE]",
    ]],
    col_widths=[2.2, 2.2, 2.1],
)

# =====================================================================
# SECTION 26 - STANDARD TERMS
# =====================================================================
section_heading(doc, 26, "Standard Contract Terms")
terms = [
    ("Entire Agreement.", "This Agreement, together with its Exhibits, is the "
     "entire agreement among the Parties on its subject matter and supersedes prior "
     "discussions and understandings."),
    ("Amendments.", "This Agreement may be amended only by a written document signed "
     "by all required parties."),
    ("Waiver.", "No waiver is effective unless in writing, and no single waiver is a "
     "continuing waiver."),
    ("Severability.", "If any provision is held invalid or unenforceable, the "
     "remaining provisions continue in full force, and the Parties will replace the "
     "invalid provision consistent with its intent and applicable law."),
    ("Assignment.", "No Party may assign this Agreement without the prior written "
     "consent of the other Parties, except as required by law."),
    ("Counterparts.", "This Agreement may be signed in counterparts, each of which "
     "is an original and all of which together form one agreement."),
    ("Electronic Signatures.", "Electronic and scanned signatures are valid and "
     "binding to the extent permitted by applicable law."),
    ("Headings.", "Headings are for convenience only and do not affect "
     "interpretation."),
    ("Survival.", "The confidentiality obligations (Section 14) and payment "
     "obligations for hours already worked (Section 6 and Section 20) survive "
     "termination or expiration."),
    ("No Third-Party Beneficiaries.", "This Agreement does not create any rights in "
     "any person who is not a Party."),
    ("Authority to Sign.", "Each person signing this Agreement represents that they "
     "are authorized to sign on behalf of the applicable Party."),
]
for i, (label, text) in enumerate(terms, start=1):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.55)
    p.paragraph_format.first_line_indent = Inches(-0.3)
    p.paragraph_format.space_after = Pt(3)
    add_rich(p, f"26.{i}\t")
    r = p.add_run(label + " ")
    _set_run_font(r, size=11, bold=True)
    add_rich(p, text)

# =====================================================================
# SIGNATURE BLOCKS
# =====================================================================
page_break(doc)
para(doc, "Signature Blocks", size=14, bold=True, space_after=4)
para(doc, "By signing below, the Parties agree to the terms of this Agreement, "
          "subject to the approvals identified in Exhibit F.", space_after=10)

def sig_block(title, lines):
    para(doc, title, size=11, bold=True, space_before=8, space_after=4)
    for label, value in lines:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(8)
        add_rich(p, f"{label}: ", bold=True)
        if value:
            add_rich(p, value)
        else:
            add_rich(p, "______________________________________________")

sig_block("LREMC Technologies, LLC d/b/a RIVRTECH", [
    ("By", "John Dyson"),
    ("Title", "Chief Operations Officer"),
    ("Signature", None),
    ("Date", None),
])
sig_block("ROBESON COMMUNITY COLLEGE", [
    ("By", None),
    ("Title", None),
    ("Signature", None),
    ("Date", None),
])
sig_block("STUDENT-ATHLETE", [
    ("Name", None),
    ("Signature", None),
    ("Date", None),
])
para(doc, "PARENT OR LEGAL GUARDIAN", size=11, bold=True, space_before=8,
     space_after=1)
para(doc, "(Required only if the Student-Athlete is under 18)", size=10,
     italic=True, space_after=4)
for label in ["Name", "Relationship", "Signature", "Date"]:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    add_rich(p, f"{label}: ", bold=True)
    add_rich(p, "______________________________________________")

sig_block("RCC ATHLETICS/COMPLIANCE ACKNOWLEDGMENT", [
    ("By", None),
    ("Title", None),
    ("Signature", None),
    ("Date", None),
])

# =====================================================================
# EXHIBITS
# =====================================================================
def exhibit_title(letter, name):
    page_break(doc)
    para(doc, f"Exhibit {letter}", size=16, bold=True,
         align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    para(doc, name, size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER,
         space_after=10)

# ---- Exhibit A
exhibit_title("A", "Internship Position Description")
make_table(doc, ["Item", "Detail"], [
    ["Position Title", "Sales and Marketing Student Intern"],
    ["Supervisor", "John Dyson, Chief Operations Officer (or designee)"],
    ["Work Location", "6090 NC Highway 711 North, Pembroke, North Carolina 28372, and approved work/event locations"],
    ["Hourly Rate", "$20.00 per hour"],
    ["Maximum Compensation", "$2,000.00 gross"],
    ["Maximum Hours", "100 authorized hours"],
    ["Schedule", "By mutual agreement; not to exceed ten (10) hours/week; academics and required athletics prioritized"],
], col_widths=[2.0, 4.5])
para(doc, "Duties", size=11, bold=True, space_before=8, space_after=2)
para(doc, "As described in Section 7 of the Agreement, including community sales "
          "and marketing events, prospective-customer outreach, lead entry, "
          "supervised follow-up calls, promotional campaign support, event "
          "materials, market research, authorized social/digital content, and "
          "training — excluding all prohibited or hazardous duties.")
para(doc, "Learning Objectives", size=11, bold=True, space_before=6, space_after=2)
for item in [
    "develop professional sales and marketing skills;",
    "build customer-engagement and communication experience;",
    "gain exposure to business operations and market research; and",
    "strengthen workplace professionalism and career readiness.",
]:
    bullet(doc, item)
para(doc, "Performance Standards", size=11, bold=True, space_before=6, space_after=2)
for item in [
    "reliable attendance and punctuality;",
    "accurate timekeeping and activity records;",
    "professional communication and conduct; and",
    "timely completion of assigned work.",
]:
    bullet(doc, item)

# ---- Exhibit B
exhibit_title("B", "Sponsorship Recognition and Benefits Schedule")
para(doc, "All items below are subject to RCC’s prior written approval and "
          "applicable NJCAA/conference rules. This schedule becomes effective only "
          "when approved and signed by RCC.", size=10, italic=True)
make_table(doc, ["Benefit / Item", "Description", "Approved? (RCC)"], [
    ["Corporate sponsor identification", "[DESCRIBE]", "[ ] Yes  [ ] No"],
    ["Recognition on athletics materials", "[DESCRIBE]", "[ ] Yes  [ ] No"],
    ["Social media recognition", "[DESCRIBE / HANDLES]", "[ ] Yes  [ ] No"],
    ["Event recognition", "[EVENT(S)]", "[ ] Yes  [ ] No"],
    ["Signage", "[SIZE / LOCATION]", "[ ] Yes  [ ] No"],
    ["Logo use", "[SCOPE / PLACEMENT]", "[ ] Yes  [ ] No"],
    ["Announcement language", "[APPROVED TEXT]", "[ ] Yes  [ ] No"],
], col_widths=[2.0, 3.0, 1.5])
make_table(doc, ["Coordination", "Detail"], [
    ["Approval Contact(s)", "Jake Jones, Athletic Director & Head Baseball Coach"],
    ["Dates / Deadlines", "[DATES]"],
], col_widths=[2.0, 4.5])

# ---- Exhibit C
exhibit_title("C", "Student-Athlete Schedule and Timesheet")
para(doc, "Complete for each workday. Only authorized, actual hours worked are "
          "paid. Off-the-clock work is prohibited.", size=10, italic=True)
make_table(doc,
    ["Date", "Start", "End", "Unpaid Meal", "Total Hrs", "Description of Work"],
    [["[  ]", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"] for _ in range(8)],
    col_widths=[0.9, 0.8, 0.8, 0.9, 0.8, 2.3])
para(doc, "Student-Athlete Certification", size=11, bold=True, space_before=8,
     space_after=2)
para(doc, "I certify that the hours recorded above are true and accurate and "
          "reflect only authorized work actually performed.")
p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(10)
add_rich(p, "Student-Athlete Signature: __________________________   Date: ____________")
para(doc, "Supervisor Approval", size=11, bold=True, space_after=2)
p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(6)
add_rich(p, "RIVRTECH Supervisor Signature: __________________________   Date: ____________")

# ---- Exhibit D
exhibit_title("D", "Limited NIL and Media Authorization")
para(doc, "USE ONLY IF APPROVED — This authorization is effective only if "
          "approved in writing by RCC and the Student-Athlete and reviewed by legal "
          "counsel. Hourly internship wages do not purchase NIL rights.",
     size=10, bold=True)
make_table(doc, ["Item", "Detail"], [
    ["Approved Photographs / Media", "[LIST / ATTACH]"],
    ["Approved Uses", "[MARKETING / PROMOTIONAL PURPOSES]"],
    ["Approved Platforms", "[WEBSITE / SOCIAL / PRINT / ETC.]"],
    ["Term (Begin – End)", "[START DATE] – [END DATE]"],
    ["Geographic / Media Scope", "[SCOPE]"],
    ["Content Approval Process", "[WHO APPROVES / HOW]"],
    ["Separate NIL Compensation (if any)", "$[NIL FEE AMOUNT] — separate from hourly wages"],
    ["Revocation / End-of-Term", "Future use revocable for material breach or legal/compliance reasons; future promotional use removed after term, subject to reasonable archival use"],
], col_widths=[2.2, 4.3])
para(doc, "No RCC endorsement is implied beyond approved sponsorship recognition. "
          "No RCC uniforms, logos, facilities, or marks may be used without "
          "RCC’s prior written approval.", size=10, space_before=4)
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(8); p.paragraph_format.space_after = Pt(8)
add_rich(p, "Student-Athlete (NIL) Signature: __________________________   Date: ____________")
p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(8)
add_rich(p, "RCC Approval (NIL) Signature: __________________________   Date: ____________")

# ---- Exhibit E
exhibit_title("E", "Program Contacts and Reporting Procedures")
make_table(doc, ["Role", "Name / Title", "Email / Phone"], [
    ["RIVRTECH Supervisor", "John Dyson, Chief Operations Officer (or designee)", "john.dyson@lumbeeriver.com / [PHONE]"],
    ["RCC Athletics Contact", "Jake Jones, Athletic Director & Head Baseball Coach", "[EMAIL / PHONE]"],
    ["RIVRTECH Human Resources", "[NAME / TITLE]", "[EMAIL / PHONE]"],
    ["Athletics/Compliance Contact", "[NAME / TITLE]", "[EMAIL / PHONE]"],
    ["Emergency Contact", "[NAME / RELATIONSHIP]", "[EMAIL / PHONE]"],
], col_widths=[1.9, 2.3, 2.3])
para(doc, "Reporting a Workplace or Program Concern", size=11, bold=True,
     space_before=8, space_after=2)
for item in [
    "Report workplace concerns, including harassment or safety concerns, to the "
    "RIVRTECH Supervisor or RIVRTECH Human Resources contact above.",
    "Report athletics or student-welfare concerns to the RCC Athletics Contact "
    "and/or Athletics/Compliance Contact above.",
    "In an emergency, contact local emergency services (911) first.",
    "Concerns may be raised without fear of retaliation, consistent with "
    "applicable policy and law.",
]:
    bullet(doc, item)

# ---- Exhibit F
exhibit_title("F", "Required Approvals Checklist")
para(doc, "This Agreement is not effective until the applicable approvals below are "
          "completed. Items marked “if applicable” depend on the "
          "circumstances (for example, whether the Student-Athlete is under 18 or "
          "whether NIL use is approved).", size=10, italic=True)
approvals = [
    "RCC Athletic Director approval",
    "RCC administration approval",
    "RCC legal review",
    "RCC athletics/NJCAA compliance review",
    "RIVRTECH HR approval",
    "RIVRTECH legal review",
    "Payroll onboarding completed",
    "Form I-9 completed",
    "Federal and state tax forms completed",
    "Direct-deposit or payroll election completed",
    "Background check, if required",
    "Confidentiality acknowledgment",
    "Technology-policy acknowledgment",
    "NIL authorization, if applicable",
    "Logo and trademark approval",
    "Financial-aid disclosure",
    "Youth Employment Certificate, if applicable",
    "Parent/guardian consent, if applicable",
    "Transportation acknowledgment",
    "Emergency contact completed",
]
make_table(doc, ["✓", "Approval Item", "Responsible Party / Date"],
    [["[  ]", a, "[  ]"] for a in approvals],
    col_widths=[0.5, 4.0, 2.0])

# =====================================================================
add_header_footer(doc, FOOTER)
doc.save(OUT)
print("Saved", OUT)
