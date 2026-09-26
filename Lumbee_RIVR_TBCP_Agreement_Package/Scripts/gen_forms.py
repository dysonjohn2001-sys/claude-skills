"""
gen_forms.py — OPERATIONAL FORMS generator for the coordinated TBCP fiber
package (Lumbee Tribe of North Carolina / RIVR Tech).

Builds the eight (8) operational-form deliverables into 04_Operational_Forms/.
Every constant, defined term, placeholder, flag, citation, and cross-reference
comes from the canonical engine common.py — SINGLE SOURCE OF TRUTH.

    Word (.docx):   Construction forms bundle; Segment IRU Activation Certificate;
                    Incident / Outage / RCA / Restoration forms.
    Excel (.xlsx):  Monthly Grant Evidence Checklist + Reimbursement Certification;
                    Monthly Subscriber Reconciliation + Payment Report;
                    Annual Budget / Capital-Refresh / Reserve / Sustainability;
                    Project Registers (5 sheets); Program Checklists (5 sheets).

Status of every generated document:
    "PRELIMINARY DRAFT – SUBJECT TO LEGAL, GRANT AND FINANCIAL REVIEW"
"""

from __future__ import annotations

import sys
sys.path.insert(0, '/home/user/claude-skills/Lumbee_RIVR_TBCP_Agreement_Package/Scripts')
import common as C  # noqa: E402

from docx.shared import Inches, Pt  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Font, Alignment, PatternFill  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402
from openpyxl.worksheet.datavalidation import DataValidation  # noqa: E402

OUT_DIR = "04_Operational_Forms"


# ===========================================================================
#  SHARED DOCX HELPERS (built on the common.py engine)
# ===========================================================================
def form_title(doc, number, name):
    """A form heading that is picked up by the Table of Contents (H1)."""
    return C.article(doc, number, name)


def field(doc, label, value, indent=0.12):
    """A labeled fill-in line: bold label + highlighted placeholder value."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(indent)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(f"{label}  ")
    r.bold = True
    C._emit_runs(p, value)
    return p


def fields(doc, pairs, indent=0.12):
    for label, value in pairs:
        field(doc, label, value, indent=indent)


def sig_block(doc, roles, note=None):
    """
    Approval / signature rows as a table.
    roles: list of role-label strings (e.g. "RIVR Tech Project Manager").
    """
    C.spacer(doc, 1)
    p = doc.add_paragraph()
    r = p.add_run("APPROVALS / SIGNATURES")
    r.bold = True
    r.font.color.rgb = C.NAVY
    r.font.size = Pt(10)
    headers = ["Approval / Role", "Signature", "Printed Name", "Title", "Date"]
    rows = []
    for role in roles:
        rows.append([
            role,
            "____________________",
            C.PH("printed name"),
            C.PH("title"),
            "____________",
        ])
    C.add_table(doc, headers, rows,
                widths=[1.9, 1.5, 1.5, 1.2, 0.9], font_size=8)
    if note:
        C.flag_para(doc, C.FLAG_ATTORNEY, note)


def disclaimer(doc):
    """Standard closing disclaimer for every Word body."""
    C.spacer(doc, 1)
    p = doc.add_paragraph()
    r = p.add_run("DISCLAIMER.  ")
    r.bold = True
    r.font.color.rgb = C.RED
    r.font.size = Pt(9)
    body = (
        "This operational form is a PRELIMINARY working draft. No controlling "
        f"{C.PROGRAM_SHORT} award or source documents were supplied; the provisional "
        f"baseline is the {C.NOFO_NAME}. {C.NOFO_LIVE_NOTE} This form is not final "
        "legal, grant, or financial advice and creates no binding obligation. "
        "Highlighted bracketed placeholders and the flag markers "
        f"{C.FLAG_BUSINESS}, {C.FLAG_ATTORNEY}, {C.FLAG_GRANT}, and {C.FLAG_TECH} "
        "must be resolved by the responsible reviewer before use. "
        f"{C.SHARED_DEFINITIONS_RULE} {C.PRECEDENCE_RULE}"
    )
    # emit with placeholder/flag styling, italic + grey base
    p2 = doc.add_paragraph()
    p2.paragraph_format.space_after = Pt(3)
    C._emit_runs(p2, body, italic=True)
    for rr in p2.runs:
        if rr.font.color.rgb is None:
            rr.font.color.rgb = C.GREY


def open_doc(doc_number, title, subtitle, short_title):
    doc = C.new_doc()
    C.add_cover(doc, doc_number, title, subtitle)
    C.setup_header_footer(doc, short_title)
    C.add_toc(doc)
    C.status_banner(doc)
    C.spacer(doc, 1)
    return doc


def crossref(doc, text):
    C.flag_para(doc, C.FLAG_GRANT, text) if "Award" in text else None


# ===========================================================================
#  FILE 1 — CONSTRUCTION FORMS BUNDLE (.docx)
# ===========================================================================
def build_construction_forms():
    doc = open_doc(
        "FORM SET 01 — CONSTRUCTION & COMPLETION FORMS",
        "Construction, Inspection, Completion, Warranty, and Acceptance Forms",
        "Notice to Proceed · Change Order · Daily Report · Material Log · "
        "Inspection · Punch List · Completion · Warranty · Segment Acceptance",
        "Construction & Completion Forms",
    )
    C.para(doc,
           f"This form set operationalizes the {C.AGREEMENTS['depc']} and is read "
           f"together with Schedule {'S4'} ({C.SCHEDULES['S4']}) and Schedule S5 "
           f"({C.SCHEDULES['S5']}). All construction of the {C.GRANT_FUNDED} is "
           f"performed by {C.OPERATOR_FULL} (\"{C.OPERATOR_SHORT}\") for the benefit "
           f"of {C.TRIBE_FULL} (the \"{C.TRIBE_SHORT}\") as owner. Facilities owned "
           f"by {C.LREMC_FULL} (\"{C.LREMC_SHORT}\") are addressed only under a "
           f"separate owner-approved instrument or joinder and are never assumed "
           f"owned by {C.OPERATOR_SHORT}.")
    C.flag_para(doc, C.FLAG_GRANT,
                f"Every construction action funded by the Award must comply with "
                f"{C.CITES['baba']}; {C.CITES['procurement']}; {C.CITES['nepa']}; "
                f"{C.CITES['nhpa']}; and {C.CITES['telecom_ban']}.")

    # --- Form 1.1 Notice to Proceed -------------------------------------
    form_title(doc, "1.1", "Notice to Proceed (NTP)")
    C.para(doc, f"The {C.TRIBE_SHORT}, as owner, authorizes {C.OPERATOR_SHORT} to "
                f"commence the Work described below under the {C.AGREEMENTS['depc']}.")
    fields(doc, [
        ("NTP No.:", C.PH("sequential NTP number")),
        ("Date Issued:", C.PH("date")),
        ("Project / Award (FAIN):", C.PH("Federal Award Identification Number — NOT SUPPLIED")),
        ("Segment / Route Authorized:", C.PH("segment ID, route, and limits per Schedule S2/S4")),
        ("Approved Project Area:", C.PH("portion of the Approved Project Area covered")),
        ("Scope of Work Authorized:", C.PH("description of authorized Work")),
        ("Scheduled Commencement Date:", C.PH("date")),
        ("Scheduled Substantial Completion:", C.PH("date")),
        ("Contract Sum for this Segment:", C.PH("$ amount per Schedule S5")),
        ("Preconditions Confirmed:", "Environmental review, permits, locates, insurance, "
         "and procurement/BABA compliance are confirmed satisfied — " + C.PH("list references")),
    ])
    C.flag_para(doc, C.FLAG_GRANT,
                f"NTP may not issue until NEPA ({C.CITES['nepa']}) and NHPA §106 "
                f"({C.CITES['nhpa']}) reviews are complete and all applicable permits, "
                f"811 locates ({C.CITES['nc_dig']}), and pole/ROW authorizations "
                f"({C.CITES['nc_pole']}; {C.CITES['nc_ncdot']}) are in hand.")
    sig_block(doc, ["RIVR Tech Project Manager", C.TRIBE_SHORT + " (authorized representative)",
                    "Grant Counsel / Grant-Compliance Officer"])

    # --- Form 1.2 Change Order ------------------------------------------
    form_title(doc, "1.2", "Change Order")
    C.para(doc, "A Change Order documents a change in the Work, Contract Sum, or "
                "schedule. No change is effective until executed by the required "
                "approvers and, where the change affects grant compliance, "
                "concurred in by Grant Counsel.")
    fields(doc, [
        ("Change Order No.:", C.PH("sequential CO number")),
        ("Related NTP / Segment:", C.PH("NTP no. / segment ID")),
        ("Date:", C.PH("date")),
        ("Description of Change:", C.PH("detailed description of the change in Work")),
        ("Reason / Origin:", C.PH("owner request / field condition / design change / other")),
        ("Change in Contract Sum:", C.PH("+/- $ amount")),
        ("Revised Contract Sum:", C.PH("$ amount")),
        ("Change in Contract Time:", C.PH("+/- calendar days")),
        ("Revised Completion Date:", C.PH("date")),
    ])
    C.section(doc, "1.2.1", "Grant-Compliance Impact Assessment (mandatory)")
    C.para(doc, "Complete for every Change Order. Any \"Yes\" requires Grant "
                "Counsel concurrence and may require prior NTIA notice or approval.")
    C.add_table(doc,
                ["Compliance Dimension", "Impact? (Y/N)", "Re-Review / Action Required"],
                [
                    ["BABA / domestic content (" + C.CITES['baba'] + ")",
                     C.PH("Y/N"), "Confirm domestic content or waiver; " + C.PH("action")],
                    ["Procurement standards (" + C.CITES['procurement'] + ")",
                     C.PH("Y/N"), "Re-verify competition/method (" + C.CITES['methods'] + "); " + C.PH("action")],
                    ["Environmental — NEPA (" + C.CITES['nepa'] + ")",
                     C.PH("Y/N"), "Environmental re-review for new ground disturbance; " + C.PH("action")],
                    ["Historic — NHPA §106 (" + C.CITES['nhpa'] + ")",
                     C.PH("Y/N"), "§106 re-review for new/altered footprint; " + C.PH("action")],
                    ["Covered telecom / §889 (" + C.CITES['telecom_ban'] + ")",
                     C.PH("Y/N"), "Re-screen equipment; " + C.PH("action")],
                    ["Budget / cost allowability (" + C.CITES['allowable'] + ")",
                     C.PH("Y/N"), "Confirm allowable/allocable/reasonable; " + C.PH("action")],
                    ["Scope / eligible locations & routes (Schedule S2)",
                     C.PH("Y/N"), "Confirm within approved scope; NTIA notice if material; " + C.PH("action")],
                ],
                widths=[3.0, 1.0, 2.5], font_size=8)
    C.flag_para(doc, C.FLAG_GRANT,
                "A scope, route, budget, or equipment change may require prior written "
                f"NTIA/DOC approval under the Award and {C.CITES['sac']}; do not proceed "
                "on grant-affecting changes without Grant Counsel sign-off.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                "Confirm funding source for the added cost (Award vs. non-federal) and "
                "any effect on the per-Active-Subscriber economics.")
    sig_block(doc, ["RIVR Tech Project Manager", C.TRIBE_SHORT + " (authorized representative)",
                    "Grant Counsel / Grant-Compliance Officer"])

    # --- Form 1.3 Daily Construction Report -----------------------------
    form_title(doc, "1.3", "Daily Construction Report")
    fields(doc, [
        ("Report Date:", C.PH("date")),
        ("Segment / Route:", C.PH("segment ID / route")),
        ("Weather / Conditions:", C.PH("weather, temperature, ground conditions")),
        ("Crew(s) On Site:", C.PH("crew names / headcount / subcontractors")),
        ("Equipment On Site:", C.PH("equipment list")),
        ("Work Performed Today:", C.PH("footage placed, splices, structures, etc.")),
        ("Quantities Installed:", C.PH("cable ft / conduit ft / handholes / splices")),
        ("Materials Received / Used:", C.PH("BABA-compliant materials; reference material log")),
        ("Inspections / Tests Today:", C.PH("locate tickets, tests, agency visits")),
        ("Safety Incidents / Near-Misses:", C.PH("none or describe")),
        ("Delays / Issues:", C.PH("none or describe")),
        ("Photos / Attachments Ref:", C.PH("file references")),
    ])
    C.flag_para(doc, C.FLAG_GRANT,
                f"Daily reports are project records retained under {C.CITES['records']} "
                "and support reimbursement evidence.")
    sig_block(doc, ["RIVR Tech Field Superintendent (prepared by)",
                    "RIVR Tech Project Manager (reviewed by)"])

    # --- Form 1.4 Material Checkout / Return Log ------------------------
    form_title(doc, "1.4", "Material Checkout / Return Log")
    C.para(doc, "Tracks issuance and return of Award-funded materials and "
                "equipment; supports material reconciliation and asset control.")
    fields(doc, [
        ("Log Period / Warehouse:", C.PH("period and location")),
        ("Segment / Cost Code:", C.PH("segment ID / cost code")),
    ])
    C.add_table(doc,
                ["Item / Material", "BABA-Compliant? / Cert Ref", "Qty Out",
                 "Date Out", "Issued To", "Qty Returned", "Date In", "Reconciled?"],
                [[C.PH("item"), C.PH("Y/N + cert ref"), C.PH("qty"), C.PH("date"),
                  C.PH("name"), C.PH("qty"), C.PH("date"), C.PH("Y/N")] for _ in range(2)],
                widths=[1.4, 1.3, 0.7, 0.8, 1.0, 0.8, 0.8, 0.7], font_size=7)
    C.flag_para(doc, C.FLAG_GRANT,
                f"Material records support BABA compliance ({C.CITES['baba']}) and "
                f"equipment/supplies management ({C.CITES['equipment']}; {C.CITES['supplies']}).")
    sig_block(doc, ["RIVR Tech Warehouse / Materials Custodian",
                    "RIVR Tech Project Manager"])

    # --- Form 1.5 Inspection Report -------------------------------------
    form_title(doc, "1.5", "Inspection Report")
    fields(doc, [
        ("Inspection No. / Date:", C.PH("number / date")),
        ("Segment / Route Inspected:", C.PH("segment ID / route / limits")),
        ("Type of Inspection:", C.PH("in-progress / pre-cover / final / agency")),
        ("Standards Applied:", f"Schedule S4 engineering standards and, for optical "
         f"work, {C.OPTICAL['otdr']} testing at {C.OPTICAL['wavelengths']} — " + C.PH("spec ref")),
        ("Observations:", C.PH("conformance / non-conformance details")),
        ("Deficiencies Noted:", C.PH("none or list — carry to Punch List")),
        ("Result:", C.PH("Pass / Conditional Pass / Fail")),
        ("Photos / Test Data Ref:", C.PH("OTDR trace files, photos")),
    ])
    C.flag_para(doc, C.FLAG_TECH,
                f"Attach optical test results: splice loss {C.OPTICAL['splice_loss_max']}, "
                f"connector loss {C.OPTICAL['connector_loss_max']}, reflectance "
                f"{C.OPTICAL['reflectance_max']}, within {C.OPTICAL['span_margin']}.")
    sig_block(doc, ["Inspector / QA (RIVR Tech or independent)",
                    "RIVR Tech Project Manager",
                    C.TRIBE_SHORT + " (owner witness, optional)"])

    # --- Form 1.6 Punch List --------------------------------------------
    form_title(doc, "1.6", "Punch List")
    fields(doc, [
        ("Segment / Route:", C.PH("segment ID / route")),
        ("Date Issued:", C.PH("date")),
        ("Target Clearance Date:", C.PH("date")),
    ])
    C.add_table(doc,
                ["#", "Location / Item", "Deficiency", "Responsible",
                 "Target Date", "Date Cleared", "Verified By"],
                [[str(i), C.PH("location"), C.PH("deficiency"), C.PH("party"),
                  C.PH("date"), C.PH("date"), C.PH("initials")] for i in range(1, 3)],
                widths=[0.4, 1.3, 1.9, 1.0, 0.8, 0.8, 0.9], font_size=7)
    sig_block(doc, ["RIVR Tech Project Manager",
                    C.TRIBE_SHORT + " (owner acceptance of punch list)"])

    # --- Form 1.7 Substantial / Final Completion ------------------------
    form_title(doc, "1.7", "Certificate of Substantial / Final Completion")
    fields(doc, [
        ("Certificate Type:", C.PH("Substantial Completion  /  Final Completion")),
        ("Segment / Route:", C.PH("segment ID / route")),
        ("Related NTP:", C.PH("NTP no.")),
        ("Date of Completion:", C.PH("date")),
        ("Description of Work Completed:", C.PH("scope completed")),
        ("Punch List Status:", C.PH("attached / all items cleared / open items listed")),
        ("As-Built Records Delivered:", C.PH("as-builts, GIS, test data references")),
        ("Warranty Start Date:", C.PH("date — start of warranty period")),
        ("Warranty Duration:", C.PH("duration per Schedule S5")),
        ("Retainage Status:", C.PH("amount held / release conditions per Schedule S5")),
    ])
    C.flag_para(doc, C.FLAG_GRANT,
                "Final Completion supports the reimbursement and closeout record "
                f"({C.CITES['records']}; {C.CITES['closeout']}); confirm BABA and "
                "as-built documentation are complete before acceptance.")
    sig_block(doc, ["RIVR Tech Project Manager",
                    C.TRIBE_SHORT + " (owner acceptance)",
                    "Grant Counsel / Grant-Compliance Officer"])

    # --- Form 1.8 Warranty Claim ----------------------------------------
    form_title(doc, "1.8", "Warranty Claim")
    fields(doc, [
        ("Claim No. / Date:", C.PH("number / date")),
        ("Segment / Asset Affected:", C.PH("segment ID / asset / component")),
        ("Warranty Reference:", C.PH("completion certificate / warranty duration")),
        ("Description of Defect:", C.PH("defect / failure description")),
        ("Date Discovered:", C.PH("date")),
        ("Impact on Service:", C.PH("none / degraded / outage — link to Outage Report if any")),
        ("Requested Remedy:", C.PH("repair / replace / re-perform")),
        ("Warrantor / Contractor:", C.PH("responsible warrantor")),
        ("Required Completion:", C.PH("date")),
        ("Resolution / Verification:", C.PH("work performed / re-test / verified by")),
    ])
    sig_block(doc, ["Submitted By (RIVR Tech or " + C.TRIBE_SHORT + ")",
                    "RIVR Tech Project Manager",
                    "Warrantor / Contractor (acknowledgment)"])

    # --- Form 1.9 Segment Acceptance ------------------------------------
    form_title(doc, "1.9", "Segment Acceptance Form")
    C.para(doc, f"The {C.TRIBE_SHORT}, as owner, accepts the completed Network "
                f"segment into the {C.GRANT_FUNDED}. Acceptance triggers the "
                f"{C.TERM_TRIGGER} for IRU/term purposes and precedes issuance of "
                f"the Segment IRU Activation Certificate.")
    fields(doc, [
        ("Segment / Route Accepted:", C.PH("segment ID / route / limits / strand count")),
        ("Related Completion Certificate:", C.PH("Form 1.7 reference")),
        ("Acceptance Date:", C.PH("date")),
        ("Test Results Reference:", f"{C.OPTICAL['otdr']} results at {C.OPTICAL['wavelengths']} — " +
         C.PH("OTDR trace file references")),
        ("Open Items / Exceptions:", C.PH("none or list")),
        ("As-Built / GIS Delivered:", C.PH("references")),
        ("Federal Interest Recorded:", "Entered in the Asset Register and Federal-Interest "
         "Register — " + C.PH("register references")),
    ])
    C.flag_para(doc, C.FLAG_GRANT,
                f"On acceptance, record the segment in the property records per "
                f"{C.CITES['equipment']} and the Federal Interest per {C.CITES['trust']}.")
    C.para(doc, f"Cross-reference: {C.AGREEMENTS['iru']} and {C.AGREEMENTS['depc']}.")
    sig_block(doc, ["RIVR Tech Project Manager",
                    C.TRIBE_SHORT + " (owner acceptance)",
                    "Grant Counsel / Grant-Compliance Officer"])

    disclaimer(doc)
    return C.save(doc, OUT_DIR,
                  "01_Construction_Forms_NTP_ChangeOrder_Inspection_PunchList_Acceptance.docx")


# ===========================================================================
#  FILE 2 — SEGMENT IRU ACTIVATION CERTIFICATE (.docx)
# ===========================================================================
def build_iru_activation_certificate():
    doc = open_doc(
        "FORM 02 — SEGMENT IRU ACTIVATION CERTIFICATE",
        "Segment IRU Activation Certificate",
        "Placing an accepted Network segment in service under the IRU",
        "Segment IRU Activation Certificate",
    )
    C.para(doc,
           f"This Segment IRU Activation Certificate (this \"Certificate\") is "
           f"delivered under the {C.AGREEMENTS['iru']} and confirms that the Network "
           f"segment identified below, constructed under the {C.AGREEMENTS['depc']}, "
           f"has been accepted and placed in service, and that the {C.IRU_TERM_DEFINED} "
           f"granted to {C.OPERATOR_SHORT} in that segment has commenced.")

    C.article(doc, 1, "Segment and In-Service Data")
    fields(doc, [
        ("Certificate No.:", C.PH("sequential certificate number")),
        ("Segment / Route:", C.PH("segment ID, route description, and limits")),
        ("Grant-Funded Assets Covered:", C.PH("cable, structures, huts, electronics per Schedule S3/S4")),
        ("Strand / Fiber Count Granted:", C.PH("number of strands / fibers subject to the IRU")),
        ("In-Service Date:", C.PH("date the segment was placed in service")),
        ("Segment Acceptance Reference:", C.PH("Segment Acceptance Form 1.9 reference / date")),
    ])

    C.article(doc, 2, "Acceptance Test Results")
    fields(doc, [
        ("Optical Test Method:", f"{C.OPTICAL['otdr']} at {C.OPTICAL['wavelengths']}"),
        ("Splice Loss (avg / max):", C.OPTICAL['splice_loss_max'] + " — " + C.PH("measured results")),
        ("Connector Loss:", C.OPTICAL['connector_loss_max'] + " — " + C.PH("measured results")),
        ("Reflectance:", C.OPTICAL['reflectance_max'] + " — " + C.PH("measured results")),
        ("Span-Loss Budget:", C.OPTICAL['span_margin'] + " — " + C.PH("computed vs. measured")),
        ("Test Results Reference:", C.PH("OTDR trace files, test report reference and date")),
    ])
    C.flag_para(doc, C.FLAG_TECH,
                "Attach the complete bi-directional OTDR test package; discrepancies "
                "beyond the stated thresholds must be cleared or listed as open items.")

    C.article(doc, 3, "Consideration")
    C.para(doc, f"Consideration for the {C.IRU_TERM_DEFINED} is {C.DEAL['iru_prepaid_consideration']}, "
                f"together with the per-Active-Subscriber operating payment "
                f"({C.DEAL['per_subscriber_amount']}) and the other obligations set "
                f"forth in the {C.AGREEMENTS['iru']} and the "
                f"{C.AGREEMENTS['retail']}.")
    C.flag_para(doc, C.FLAG_GRANT, C.DEAL['program_income_note'] +
                f" ({C.CITES['prog_income']}).")

    C.article(doc, 4, "Required Approvals Obtained")
    C.para(doc, "The following approvals and consents have been obtained for this "
                "segment (attach evidence):")
    C.add_table(doc,
                ["Approval / Consent", "Obtained? (Y/N)", "Reference / Date"],
                [
                    ["NTIA / DOC consent to the IRU / operating arrangement",
                     C.PH("Y/N"), C.PH("reference")],
                    ["BIA approval (if trust/restricted land) — " + C.CITES['bia_approval'],
                     C.PH("Y/N / N-A"), C.PH("reference")],
                    ["LREMC owner consent / joinder (LREMC Facilities)",
                     C.PH("Y/N / N-A"), C.PH("reference")],
                    ["Landowner / easement / ROW consents",
                     C.PH("Y/N"), C.PH("reference")],
                    ["Lender consent (if financed assets)",
                     C.PH("Y/N / N-A"), C.PH("reference")],
                ],
                widths=[3.4, 1.2, 1.9], font_size=8)

    C.article(doc, 5, "Open Items")
    fields(doc, [
        ("Open Items / Exceptions:", C.PH("none or list open punch/test/approval items")),
        ("Target Resolution Date:", C.PH("date")),
    ])

    C.article(doc, 6, "Term")
    C.para(doc, f"The {C.IRU_TERM_DEFINED} term for this segment is "
                f"{C.IRU_TERM_RECOMMENDED} years commencing on the In-Service Date "
                f"(the \"Segment Term Commencement Date\"), followed by "
                f"{C.DEAL['iru_renewal']}, subject to {C.DEAL['term_ceiling_note']}.")
    fields(doc, [
        ("Term Start (In-Service Date):", C.PH("date")),
        ("Initial Term Expiration:", C.PH("In-Service Date + 20 years")),
        ("Renewal Options:", C.DEAL['iru_renewal']),
    ])
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Confirm the segment term does not exceed the useful life of the "
                "assets, the underlying land/access rights, the Federal Interest "
                "period, or the controlling Award.")

    C.para(doc, f"Cross-reference: {C.AGREEMENTS['iru']} and {C.AGREEMENTS['depc']}. "
                f"{C.SHARED_DEFINITIONS_RULE}")

    # Two-party execution: Tribe + RIVR Tech
    C.signature_block(doc,
                      extra_note="This Certificate is a working draft; confirm all "
                      "approvals and the term ceiling before execution.")
    disclaimer(doc)
    return C.save(doc, OUT_DIR, "02_Segment_IRU_Activation_Certificate.docx")


# ===========================================================================
#  FILE 3 — MONTHLY GRANT EVIDENCE CHECKLIST + REIMBURSEMENT CERT (.xlsx)
# ===========================================================================
STATUS_LIST = '"Not Started,In Progress,Complete,N/A"'


def _status_validation(ws, col_letter, first_row, last_row):
    dv = DataValidation(type="list", formula1=STATUS_LIST, allow_blank=True)
    dv.error = "Choose: Not Started / In Progress / Complete / N/A"
    dv.prompt = "Select a status"
    ws.add_data_validation(dv)
    dv.add(f"{col_letter}{first_row}:{col_letter}{last_row}")


def build_grant_evidence_checklist():
    wb = Workbook()
    C.xl_instructions(wb, [
        "## Monthly Grant Evidence Checklist & Reimbursement Certification",
        "Purpose: assemble and certify the evidence supporting each monthly "
        "reimbursement request under the TBCP Award.",
        "• Amber INPUT cells are for you to complete. Put a Doc Ref for every item.",
        "• Set Status from the dropdown (Not Started / In Progress / Complete / N/A).",
        "• Every reimbursed cost must be allowable, allocable, and reasonable per "
        + C.CITES['allowable'] + ".",
        "• Retain all records for at least " + str(C.DEAL['records_retention_years']) +
        " years per " + C.CITES['records'] + ".",
        "• Cross-reference: " + C.AGREEMENTS['finance'] + " and Schedule S8 (" +
        C.SCHEDULES['S8'] + ").",
        "• " + C.DRAFT_STATUS_SHORT,
    ])

    ws = wb.create_sheet("Evidence Checklist")
    ws.sheet_properties.tabColor = "1F3864"
    C.xl_title(ws, "Monthly Grant Evidence Checklist",
               subtitle="Reimbursement period: " + C.PH("month / year") +
               "   ·   FAIN: " + C.PH("Federal Award ID — NOT SUPPLIED"), span=7)
    widths = [4, 26, 40, 16, 22, 16, 30]
    for i, w in enumerate(widths):
        ws.column_dimensions[get_column_letter(i + 1)].width = w
    hdr_row = 5
    C.xl_header_row(ws, hdr_row,
                    ["#", "Evidence Category", "Required Document(s)", "Status",
                     "Doc Ref", "Reviewer", "Notes"])
    items = [
        ("Vendor invoices", "Itemized invoices tied to approved budget lines"),
        ("Purchase orders", "POs matching invoices and procurement records"),
        ("Payment proof", "Bank/ACH confirmations or canceled checks showing disbursement"),
        ("Timekeeping / payroll", "Certified time-and-effort for allocable labor (" + C.CITES['allowable'] + ")"),
        ("Equipment logs", "Equipment records per " + C.CITES['equipment']),
        ("Material reconciliation", "Material checkout/return logs reconciled to installed quantities"),
        ("BABA documentation", "Domestic-content certifications and any approved waivers (" + C.CITES['baba'] + ")"),
        ("Procurement files", "Solicitation, competition, and method documentation (" + C.CITES['procurement'] + ")"),
        ("§889 / covered telecom", "Screening certifications (" + C.CITES['telecom_ban'] + ")"),
        ("Cost allocation support", "Basis for allocation across segments / cost objectives"),
        ("Match / cost-share", "Documentation of any required non-federal share"),
        ("Prior-period adjustments", "Corrections, credits, or disallowed-cost removals"),
    ]
    r = hdr_row + 1
    first_data = r
    for i, (cat, doc_desc) in enumerate(items, start=1):
        C.xl_cell(ws, r, 1, i, "text", align="center")
        C.xl_cell(ws, r, 2, cat, "text", wrap=True)
        C.xl_cell(ws, r, 3, doc_desc, "text", wrap=True)
        C.xl_cell(ws, r, 4, C.PH("status"), "input", align="center")
        C.xl_cell(ws, r, 5, C.PH("document reference"), "input", wrap=True)
        C.xl_cell(ws, r, 6, C.PH("reviewer initials"), "input", align="center")
        C.xl_cell(ws, r, 7, C.PH("notes"), "input", wrap=True)
        r += 1
    last_data = r - 1
    _status_validation(ws, "D", first_data, last_data)

    # Completeness check
    r += 1
    C.xl_check(ws, r, 2,
               f'=IF(COUNTIF(D{first_data}:D{last_data},"Complete")+'
               f'COUNTIF(D{first_data}:D{last_data},"N/A")={last_data-first_data+1},'
               f'"PASS — all items resolved","FAIL — open items remain")',
               "Completeness check (all items Complete or N/A):")

    # Certification block
    r += 3
    C.xl_cell(ws, r, 1, "REIMBURSEMENT CERTIFICATION", "section")
    for cc in range(2, 8):
        C.xl_cell(ws, r, cc, "", "section")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7)
    r += 1
    cert_text = ("I certify, to the best of my knowledge and belief, that the costs "
                 "in this reimbursement request are allowable, allocable, and "
                 "reasonable under " + C.CITES['allowable'] + "; are supported by the "
                 "records referenced above and retained per " + C.CITES['records'] +
                 "; have not been previously reimbursed; and comply with the Award, "
                 "the controlling NOFO, and applicable federal requirements including "
                 "BABA and §889. (18 U.S.C. §§ 287, 1001 false-claims exposure applies.)")
    ws.merge_cells(start_row=r, start_column=1, end_row=r + 2, end_column=7)
    cc = ws.cell(row=r, column=1, value=cert_text)
    cc.alignment = Alignment(wrap_text=True, vertical="top")
    cc.font = Font(size=10, italic=True)
    r += 4
    for label in [("Total amount this request:", C.PH("$ amount")),
                  ("RIVR Tech authorized officer (name / title):", C.PH("name / title")),
                  ("Signature / Date:", C.PH("signature / date")),
                  (C.TRIBE_SHORT + " Grant Counsel / Finance (name / title):", C.PH("name / title")),
                  ("Signature / Date:", C.PH("signature / date"))]:
        C.xl_cell(ws, r, 1, label[0], "text", bold=True)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
        C.xl_cell(ws, r, 4, label[1], "input", wrap=True)
        ws.merge_cells(start_row=r, start_column=4, end_row=r, end_column=7)
        r += 1

    return C.xl_save(wb, OUT_DIR,
                     "03_Monthly_Grant_Evidence_Checklist_and_Reimbursement_Certification.xlsx")


# ===========================================================================
#  FILE 4 — MONTHLY SUBSCRIBER RECONCILIATION + PAYMENT REPORT (.xlsx)
# ===========================================================================
def build_subscriber_reconciliation():
    wb = Workbook()
    C.xl_instructions(wb, [
        "## Monthly Subscriber Reconciliation & Payment Report",
        "Purpose: reconcile Active Subscribers and compute the per-Active-Subscriber "
        "operating payment due to " + C.TRIBE_FULL + ".",
        "• One row per served location / account. Amber INPUT cells are for you.",
        "• 'Countable Active Subs' is computed: it counts a location only if it is "
        "NOT excluded and the Status is Active.",
        "• Active Subscriber counting rules (Schedule S8 / Retail Agreement):",
    ] + ["    – " + e for e in C.DEAL['active_subscriber_elements']] + [
        "• Payment = Countable Active Subs × the per-subscriber rate (" +
        C.DEAL['per_subscriber_amount'] + ").",
        "• Net payable = payment less credits, refunds, and uncollectible adjustments.",
        "• Checks: counted must be ≤ served; every excluded row must carry a valid reason.",
        "• Cross-reference: " + C.AGREEMENTS['retail'] + " and Schedule S8 (" +
        C.SCHEDULES['S8'] + ").",
        "• " + C.DRAFT_STATUS_SHORT,
    ])

    ws = wb.create_sheet("Subscriber Reconciliation")
    ws.sheet_properties.tabColor = "1F3864"
    C.xl_title(ws, "Monthly Subscriber Reconciliation & Payment Report",
               subtitle="Service month: " + C.PH("month / year"), span=8)
    widths = [26, 16, 16, 14, 12, 30, 16, 30]
    for i, w in enumerate(widths):
        ws.column_dimensions[get_column_letter(i + 1)].width = w
    hdr_row = 5
    C.xl_header_row(ws, hdr_row,
                    ["Location / Account", "Activation Date", "Disconnect Date",
                     "Status", "Billable Units", "Excluded? (reason)",
                     "Countable Active Subs", "Notes"])
    # Status validation values for reconciliation
    dv = DataValidation(type="list",
                        formula1='"Active,Suspended,Disconnected,Pending"',
                        allow_blank=True)
    ws.add_data_validation(dv)

    n_rows = 6
    first = hdr_row + 1
    r = first
    for _ in range(n_rows):
        C.xl_cell(ws, r, 1, C.PH("location / account ID"), "input", wrap=True)
        C.xl_cell(ws, r, 2, C.PH("activation date"), "input", align="center")
        C.xl_cell(ws, r, 3, C.PH("disconnect date / blank"), "input", align="center")
        C.xl_cell(ws, r, 4, C.PH("status"), "input", align="center")
        C.xl_cell(ws, r, 5, C.PH("units"), "input", fmt=C.FMT_NUM, align="center")
        C.xl_cell(ws, r, 6, C.PH("blank if counted; else reason"), "input", wrap=True)
        # Countable: count only if not excluded (F blank) and Status = Active.
        # IFERROR guards against placeholder text in Billable Units.
        C.xl_cell(ws, r, 7,
                  f'=IFERROR(IF(AND(TRIM(F{r})="",D{r}="Active"),E{r},0),0)',
                  "formula", fmt=C.FMT_NUM, align="center")
        C.xl_cell(ws, r, 8, C.PH("notes"), "input", wrap=True)
        r += 1
    last = r - 1
    dv.add(f"D{first}:D{last}")

    # Totals row
    tot = r
    C.xl_cell(ws, tot, 1, "TOTALS", "section")
    for cc in (2, 3, 4, 8):
        C.xl_cell(ws, tot, cc, "", "section")
    C.xl_cell(ws, tot, 5, f"=SUM(E{first}:E{last})", "output", fmt=C.FMT_NUM, bold=True)
    C.xl_cell(ws, tot, 6, "", "section")
    C.xl_cell(ws, tot, 7, f"=SUM(G{first}:G{last})", "output", fmt=C.FMT_NUM, bold=True)

    # Payment computation block
    r = tot + 2
    C.xl_cell(ws, r, 1, "PAYMENT COMPUTATION", "section")
    for cc in range(2, 9):
        C.xl_cell(ws, r, cc, "", "section")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
    lines = [
        ("Served locations (total billable units):", f"=E{tot}", "output", C.FMT_NUM),
        ("Countable Active Subscribers:", f"=G{tot}", "output", C.FMT_NUM),
        ("Per-Active-Subscriber rate ($/sub/month):",
         C.PH("$[X] rate — per Schedule S8"), "input", C.FMT_USD2),
        ("Gross payment (countable × rate):",
         f"=IFERROR(G{tot}*B{r+3},0)", "formula", C.FMT_USD),
        ("Less: credits:", C.PH("$ credits"), "input", C.FMT_USD),
        ("Less: refunds:", C.PH("$ refunds"), "input", C.FMT_USD),
        ("Less: uncollectible adjustments:", C.PH("$ uncollectible"), "input", C.FMT_USD),
    ]
    r += 1
    pay_start = r
    for label, val, kind, fmt in lines:
        C.xl_cell(ws, r, 1, label, "text", bold=True)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=1)
        C.xl_cell(ws, r, 2, val, kind, fmt=fmt)
        r += 1
    # rows: pay_start=served, +1 countable, +2 rate, +3 gross, +4 credits, +5 refunds, +6 uncollectible
    gross = pay_start + 3
    credits = pay_start + 4
    refunds = pay_start + 5
    uncoll = pay_start + 6
    C.xl_cell(ws, r, 1, "NET PAYABLE to " + C.TRIBE_SHORT + ":", "output", bold=True)
    C.xl_cell(ws, r, 2,
              f"=IFERROR(B{gross}-B{credits}-B{refunds}-B{uncoll},0)",
              "output", fmt=C.FMT_USD, bold=True)
    net_row = r

    # Formula checks
    r = net_row + 2
    C.xl_cell(ws, r, 1, "FORMULA CHECKS", "section")
    for cc in range(2, 9):
        C.xl_cell(ws, r, cc, "", "section")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
    r += 1
    C.xl_check(ws, r, 1,
               f'=IF(G{tot}<=E{tot},"PASS — counted ≤ served",'
               f'"FAIL — counted exceeds served")',
               "Counted Active Subs ≤ served billable units:")
    r += 1
    C.xl_check(ws, r, 1,
               f'=IF(SUMPRODUCT(--(TRIM(F{first}:F{last})<>""),'
               f'--(G{first}:G{last}>0))=0,"PASS — excluded rows not counted",'
               f'"FAIL — an excluded row was counted")',
               "Excluded rows carry a reason and are not counted:")
    r += 1
    C.xl_check(ws, r, 1,
               f'=IF(B{net_row}>=0,"PASS — net payable not negative",'
               f'"REVIEW — adjustments exceed gross payment")',
               "Net payable is not negative:")

    r += 2
    C.xl_legend(ws, r)
    return C.xl_save(wb, OUT_DIR,
                     "04_Monthly_Subscriber_Reconciliation_and_Payment_Report.xlsx")


# ===========================================================================
#  FILE 5 — ANNUAL BUDGET / CAPITAL REFRESH / RESERVE / SUSTAINABILITY (.xlsx)
# ===========================================================================
def build_annual_budget():
    wb = Workbook()
    C.xl_instructions(wb, [
        "## Annual Budget, Capital-Refresh, Replacement-Reserve & Sustainability",
        "Purpose: plan the annual operating budget, capital-refresh, and "
        "replacement-reserve funding, and test long-run sustainability of the "
        + C.NETWORK + ".",
        "• Amber INPUT cells are yours; blue FORMULA and green OUTPUT cells compute.",
        "• Checks flag if the replacement reserve is underfunded or if revenue "
        "does not cover operating expense.",
        "• Cross-reference: " + C.AGREEMENTS['om'] + " and Schedule S6 (" +
        C.SCHEDULES['S6'] + ").",
        "• " + C.DRAFT_STATUS_SHORT,
    ])

    # ---- Sheet A: Operating Budget ----
    ws = wb.create_sheet("Operating Budget")
    ws.sheet_properties.tabColor = "1F3864"
    C.xl_title(ws, "Annual Operating Budget",
               subtitle="Budget year: " + C.PH("year"), span=4)
    for col, w in zip("ABCD", [40, 18, 18, 30]):
        ws.column_dimensions[col].width = w
    hr = 5
    C.xl_header_row(ws, hr, ["Line Item", "Amount", "% of Revenue", "Notes"])
    r = hr + 1
    C.xl_cell(ws, r, 1, "REVENUE", "section")
    for cc in (2, 3, 4):
        C.xl_cell(ws, r, cc, "", "section")
    r += 1
    rev_first = r
    for item in ["Per-Active-Subscriber operating revenue", "Other retail revenue",
                 "Approved commercial / non-project use revenue", "Other income"]:
        C.xl_cell(ws, r, 1, item, "text")
        C.xl_cell(ws, r, 2, C.PH("$ amount"), "input", fmt=C.FMT_USD)
        C.xl_cell(ws, r, 3, f"=IFERROR(B{r}/$B${r+1+ (0)},0)", "formula", fmt=C.FMT_PCT)
        C.xl_cell(ws, r, 4, C.PH("notes"), "input", wrap=True)
        r += 1
    rev_last = r - 1
    rev_tot = r
    C.xl_cell(ws, r, 1, "Total Revenue", "output", bold=True)
    C.xl_cell(ws, r, 2, f"=SUM(B{rev_first}:B{rev_last})", "output", fmt=C.FMT_USD, bold=True)
    C.xl_cell(ws, r, 3, "=IFERROR(B{0}/B{0},0)".format(r), "output", fmt=C.FMT_PCT)
    r += 1
    # fix revenue % column now that total known
    for rr in range(rev_first, rev_last + 1):
        ws.cell(row=rr, column=3).value = f"=IFERROR(B{rr}/$B${rev_tot},0)"

    r += 1
    C.xl_cell(ws, r, 1, "OPERATING EXPENSE", "section")
    for cc in (2, 3, 4):
        C.xl_cell(ws, r, cc, "", "section")
    r += 1
    opex_first = r
    for item in ["Network operations & maintenance (O&M)", "NOC / monitoring (24x7x365)",
                 "Field labor & vehicles", "Power & site costs",
                 "Pole / easement / ROW / LREMC facility fees", "Transport & IP transit",
                 "Billing, customer care & collections", "Insurance",
                 "Software & licenses", "Administrative & compliance", "Taxes & regulatory fees"]:
        C.xl_cell(ws, r, 1, item, "text")
        C.xl_cell(ws, r, 2, C.PH("$ amount"), "input", fmt=C.FMT_USD)
        C.xl_cell(ws, r, 3, f"=IFERROR(B{r}/$B${rev_tot},0)", "formula", fmt=C.FMT_PCT)
        C.xl_cell(ws, r, 4, C.PH("notes"), "input", wrap=True)
        r += 1
    opex_last = r - 1
    opex_tot = r
    C.xl_cell(ws, r, 1, "Total Operating Expense", "output", bold=True)
    C.xl_cell(ws, r, 2, f"=SUM(B{opex_first}:B{opex_last})", "output", fmt=C.FMT_USD, bold=True)
    C.xl_cell(ws, r, 3, f"=IFERROR(B{opex_tot}/$B${rev_tot},0)", "output", fmt=C.FMT_PCT)
    r += 2
    noi = r
    C.xl_cell(ws, r, 1, "Net Operating Income (Revenue − Opex)", "output", bold=True)
    C.xl_cell(ws, r, 2, f"=B{rev_tot}-B{opex_tot}", "output", fmt=C.FMT_USD, bold=True)
    r += 1
    C.xl_cell(ws, r, 1, "Reserve contribution (from Reserve Schedule):", "text", bold=True)
    C.xl_cell(ws, r, 2, "='Reserve Schedule'!B7", "formula", fmt=C.FMT_USD)
    resv_contrib_ref = f"B{r}"
    r += 1
    C.xl_cell(ws, r, 1, "Net after reserve contribution", "output", bold=True)
    C.xl_cell(ws, r, 2, f"=B{noi}-{resv_contrib_ref}", "output", fmt=C.FMT_USD, bold=True)

    r += 2
    C.xl_cell(ws, r, 1, "FORMULA CHECKS", "section")
    for cc in (2, 3, 4):
        C.xl_cell(ws, r, cc, "", "section")
    r += 1
    C.xl_check(ws, r, 1,
               f'=IF(B{rev_tot}>=B{opex_tot},"PASS — revenue covers opex",'
               f'"FLAG — revenue below opex; sustainability risk")',
               "Revenue ≥ Operating Expense:")
    r += 2
    C.xl_legend(ws, r)

    # ---- Sheet B: Capital Refresh Plan ----
    ws2 = wb.create_sheet("Capital Refresh")
    C.xl_title(ws2, "Capital-Refresh Plan", span=6)
    for col, w in zip("ABCDEF", [30, 14, 14, 16, 18, 26]):
        ws2.column_dimensions[col].width = w
    hr = 5
    C.xl_header_row(ws2, hr,
                    ["Asset Class", "In-Service Year", "Expected Useful Life (yrs)",
                     "Next Refresh Year", "Estimated Refresh Cost", "Notes"])
    r = hr + 1
    cap_first = r
    for cls in ["Outside-plant fiber / cable", "Splice enclosures / hardware",
                "OLT / access electronics", "Core / aggregation electronics",
                "Optical network terminals (ONTs / CPE)", "Power / backup / batteries",
                "Huts / cabinets / enclosures", "Network monitoring / software"]:
        C.xl_cell(ws2, r, 1, cls, "text")
        C.xl_cell(ws2, r, 2, C.PH("year"), "input", align="center")
        C.xl_cell(ws2, r, 3, C.PH("life"), "input", align="center")
        C.xl_cell(ws2, r, 4, f"=IFERROR(B{r}+C{r},\"\")", "formula", align="center")
        C.xl_cell(ws2, r, 5, C.PH("$ cost"), "input", fmt=C.FMT_USD)
        C.xl_cell(ws2, r, 6, C.PH("notes"), "input", wrap=True)
        r += 1
    cap_last = r - 1
    C.xl_cell(ws2, r, 1, "Total planned refresh cost", "output", bold=True)
    C.xl_cell(ws2, r, 5, f"=SUM(E{cap_first}:E{cap_last})", "output", fmt=C.FMT_USD, bold=True)
    cap_total_row = r
    r += 2
    C.xl_legend(ws2, r)

    # ---- Sheet C: Replacement Reserve Schedule ----
    ws3 = wb.create_sheet("Reserve Schedule")
    C.xl_title(ws3, "Replacement-Reserve Schedule", span=3)
    for col, w in zip("ABC", [46, 20, 30]):
        ws3.column_dimensions[col].width = w
    hr = 4
    C.xl_header_row(ws3, hr, ["Reserve Line", "Amount", "Notes"])
    # NOTE: Operating Budget references 'Reserve Schedule'!B7 for the contribution.
    rows = [
        ("Opening reserve balance", C.PH("$ balance"), "input", C.FMT_USD, C.PH("notes")),
        ("Annual reserve contribution", C.PH("$ contribution"), "input", C.FMT_USD,
         "Feeds the Operating Budget"),
        ("Reserve draws (refresh / replacement)", C.PH("$ draws"), "input", C.FMT_USD, C.PH("notes")),
    ]
    r = hr + 1
    open_row = r          # B5 opening
    for label, val, kind, fmt, note in rows:
        C.xl_cell(ws3, r, 1, label, "text", bold=True)
        C.xl_cell(ws3, r, 2, val, kind, fmt=fmt)
        C.xl_cell(ws3, r, 3, note, "text", wrap=True)
        r += 1
    contrib_row = open_row + 1  # B6
    draws_row = open_row + 2    # B7 -> but budget expects B7 = contribution; adjust:
    # Ensure contribution is at B7 as referenced by Operating Budget.
    # Reorder: opening B5, draws B6, contribution B7? Simpler: place closing/required below
    # and point budget to the contribution row explicitly.
    # (Operating Budget formula uses 'Reserve Schedule'!B7 — make contribution land on row 7.)
    # rows above put: B5 opening, B6 contribution, B7 draws. Budget expects contribution.
    # Fix: repoint budget was B7; instead set budget to B6. We'll adjust after.
    closing_row = r
    C.xl_cell(ws3, r, 1, "Closing reserve balance (opening + contribution − draws)",
              "output", bold=True)
    C.xl_cell(ws3, r, 2,
              f"=IFERROR(B{open_row}+B{contrib_row}-B{draws_row},0)",
              "output", fmt=C.FMT_USD, bold=True)
    r += 1
    req_row = r
    C.xl_cell(ws3, r, 1, "Required reserve (target funding level)", "input", bold=True)
    C.xl_cell(ws3, r, 2, C.PH("$ required reserve target"), "input", fmt=C.FMT_USD)
    r += 2
    C.xl_cell(ws3, r, 1, "FORMULA CHECKS", "section")
    C.xl_cell(ws3, r, 2, "", "section")
    C.xl_cell(ws3, r, 3, "", "section")
    r += 1
    C.xl_check(ws3, r, 1,
               f'=IF(B{closing_row}>=B{req_row},"PASS — reserve funded",'
               f'"FLAG — reserve underfunded")',
               "Closing reserve ≥ required target:")
    r += 2
    C.xl_legend(ws3, r)

    # Repoint Operating Budget reserve-contribution reference to the true row.
    ws.cell(row=noi + 1, column=2).value = f"='Reserve Schedule'!B{contrib_row}"

    # ---- Sheet D: Capacity Forecast ----
    ws4 = wb.create_sheet("Capacity Forecast")
    C.xl_title(ws4, "Capacity & Subscriber Forecast", span=5)
    for col, w in zip("ABCDE", [28, 16, 16, 16, 16]):
        ws4.column_dimensions[col].width = w
    hr = 5
    C.xl_header_row(ws4, hr,
                    ["Metric", "Year 1", "Year 2", "Year 3", "Year 5"])
    r = hr + 1
    for metric in ["Locations passed", "Active Subscribers", "Take rate",
                   "Peak utilization (%)", "Headroom to capacity (%)"]:
        C.xl_cell(ws4, r, 1, metric, "text")
        for cc in range(2, 6):
            fmt = C.FMT_PCT if "%" in metric or "rate" in metric else C.FMT_NUM
            C.xl_cell(ws4, r, cc, C.PH("value"), "input", fmt=fmt, align="center")
        r += 1
    r += 1
    C.xl_legend(ws4, r)

    # ---- Sheet E: Sustainability Review ----
    ws5 = wb.create_sheet("Sustainability")
    C.xl_title(ws5, "Annual Sustainability Review", span=3)
    for col, w in zip("ABC", [46, 20, 34]):
        ws5.column_dimensions[col].width = w
    hr = 5
    C.xl_header_row(ws5, hr, ["Indicator", "Value", "Assessment"])
    r = hr + 1
    C.xl_cell(ws5, r, 1, "Total revenue", "text")
    C.xl_cell(ws5, r, 2, f"='Operating Budget'!B{rev_tot}", "formula", fmt=C.FMT_USD)
    C.xl_cell(ws5, r, 3, C.PH("assessment"), "input", wrap=True)
    r += 1
    C.xl_cell(ws5, r, 1, "Total operating expense", "text")
    C.xl_cell(ws5, r, 2, f"='Operating Budget'!B{opex_tot}", "formula", fmt=C.FMT_USD)
    C.xl_cell(ws5, r, 3, C.PH("assessment"), "input", wrap=True)
    r += 1
    C.xl_cell(ws5, r, 1, "Net operating income", "text")
    C.xl_cell(ws5, r, 2, f"='Operating Budget'!B{noi}", "formula", fmt=C.FMT_USD)
    C.xl_cell(ws5, r, 3, C.PH("assessment"), "input", wrap=True)
    r += 1
    C.xl_cell(ws5, r, 1, "Operating margin", "text")
    C.xl_cell(ws5, r, 2,
              f"=IFERROR('Operating Budget'!B{noi}/'Operating Budget'!B{rev_tot},0)",
              "formula", fmt=C.FMT_PCT)
    C.xl_cell(ws5, r, 3, C.PH("assessment"), "input", wrap=True)
    r += 1
    C.xl_cell(ws5, r, 1, "Reserve funding status", "text")
    C.xl_cell(ws5, r, 2,
              f"=IF('Reserve Schedule'!B{closing_row}>='Reserve Schedule'!B{req_row},"
              f'"Funded","Underfunded")', "formula")
    C.xl_cell(ws5, r, 3, C.PH("assessment"), "input", wrap=True)
    r += 2
    C.xl_cell(ws5, r, 1, "FORMULA CHECKS", "section")
    C.xl_cell(ws5, r, 2, "", "section")
    C.xl_cell(ws5, r, 3, "", "section")
    r += 1
    C.xl_check(ws5, r, 1,
               f"=IF('Operating Budget'!B{rev_tot}>='Operating Budget'!B{opex_tot},"
               f'"PASS — self-sustaining on opex","FLAG — subsidy required")',
               "Revenue ≥ Opex (self-sustaining):")
    r += 1
    C.xl_check(ws5, r, 1,
               f"=IF('Reserve Schedule'!B{closing_row}>='Reserve Schedule'!B{req_row},"
               f'"PASS — reserve funded","FLAG — reserve underfunded")',
               "Replacement reserve funded:")
    r += 2
    C.xl_legend(ws5, r)

    return C.xl_save(wb, OUT_DIR,
                     "05_Annual_Budget_Capital_Refresh_Reserve_and_Sustainability.xlsx")


# ===========================================================================
#  FILE 6 — PROJECT REGISTERS (5 sheets) (.xlsx)
# ===========================================================================
def _register_sheet(wb, name, tab, title, subtitle, headers, widths, sample_rows=3):
    ws = wb.create_sheet(name)
    ws.sheet_properties.tabColor = tab
    C.xl_title(ws, title, subtitle=subtitle, span=len(headers))
    for i, w in enumerate(widths):
        ws.column_dimensions[get_column_letter(i + 1)].width = w
    hr = 5
    C.xl_header_row(ws, hr, headers)  # freeze + filter on by default
    r = hr + 1
    for _ in range(sample_rows):
        for cidx, h in enumerate(headers, start=1):
            C.xl_cell(ws, r, cidx, C.PH(h.split("(")[0].strip().lower()), "input", wrap=True)
        r += 1
    return ws


def build_project_registers():
    wb = Workbook()
    C.xl_instructions(wb, [
        "## Project Registers",
        "Five statutory/operational registers for the " + C.NETWORK + ".",
        "• Each sheet has frozen, filterable headers. Amber INPUT rows are yours.",
        "• Asset Register captures the property-record fields required by " +
        C.CITES['equipment'] + " (see 200.313(d)).",
        "• Federal-Interest Register tracks the property trust relationship under " +
        C.CITES['trust'] + ".",
        "• Land-Rights Register cross-references Schedule S9 (" + C.SCHEDULES['S9'] +
        "); trust/restricted land requires BIA approval (" + C.CITES['bia_approval'] + ").",
        "• Software/License Register supports §889 screening (" + C.CITES['telecom_ban'] + ").",
        "• Approval/Consent Register tracks NTIA / BIA / LREMC / landowner / lender consents.",
        "• " + C.DRAFT_STATUS_SHORT,
    ])

    # 1. Asset Register — 2 CFR 200.313(d) fields
    _register_sheet(
        wb, "Asset Register", "1F3864",
        "Asset Register", "Property records per " + C.CITES['equipment'] + " (200.313(d))",
        ["Asset ID / Tag", "Description", "Serial / Model No.", "Funding Source (FAIN)",
         "Title Holder", "Acquisition Date", "Acquisition Cost", "% Federal Participation",
         "Location", "Use & Condition", "Ultimate Disposition"],
        [14, 24, 16, 20, 18, 14, 14, 14, 20, 18, 20])

    # 2. Federal-Interest Register — 2 CFR 200.316
    _register_sheet(
        wb, "Federal-Interest Register", "7F007F",
        "Federal-Interest Register", "Property trust relationship per " + C.CITES['trust'],
        ["Asset / Property", "Federal Interest Type", "Award / FAIN", "Federal Share %",
         "Federal Interest Start", "Federal Interest End", "Encumbrance / Disposition Restriction",
         "NTIA Approval Ref", "Notes"],
        [24, 20, 18, 14, 16, 16, 26, 18, 24])

    # 3. Land-Rights Register — cross-ref S9; BIA approvals
    _register_sheet(
        wb, "Land-Rights Register", "375623",
        "Land-Rights Register",
        "Parcels / instruments / BIA approvals — cross-ref Schedule S9 (" + C.SCHEDULES['S9'] + ")",
        ["Parcel / Site ID", "Location / Address", "Interest Type (easement/lease/ROW/fee/license)",
         "Instrument / Recording Ref", "Grantor / Owner", "Grantee", "Term / Expiration",
         "Trust / Restricted Land? (Y/N)", "BIA Approval Ref (25 CFR 162/169)",
         "Consent / Joinder (LREMC / landowner)", "Notes"],
        [14, 22, 26, 22, 18, 14, 16, 16, 22, 24, 22])

    # 4. Software / License Register
    _register_sheet(
        wb, "Software-License Register", "BF8F00",
        "Software / License Register", "Software, licenses, and §889 screening (" +
        C.CITES['telecom_ban'] + ")",
        ["Software / System", "Vendor", "License Type", "Seats / Scope", "Term / Renewal",
         "Annual Cost", "Federal Funds? (Y/N)", "§889 Screened? (Y/N)",
         "Assignable on Transition? (Y/N)", "Notes"],
        [22, 18, 16, 16, 16, 14, 14, 14, 18, 24])

    # 5. Approval / Consent Register
    _register_sheet(
        wb, "Approval-Consent Register", "C00000",
        "Approval / Consent Register",
        "NTIA / BIA / LREMC / landowner / lender / NCDOT approvals and consents",
        ["Approval / Consent", "Authority (NTIA/BIA/LREMC/Landowner/Lender/NCDOT)",
         "Required For", "Status", "Reference / Doc", "Date Obtained", "Expiration",
         "Conditions", "Notes"],
        [24, 28, 22, 16, 20, 14, 14, 22, 22])

    return C.xl_save(wb, OUT_DIR, "06_Project_Registers.xlsx")


# ===========================================================================
#  FILE 7 — INCIDENT / OUTAGE / RCA / RESTORATION FORMS (.docx)
# ===========================================================================
def build_incident_forms():
    doc = open_doc(
        "FORM SET 07 — INCIDENT, OUTAGE, RCA & RESTORATION FORMS",
        "Incident, Outage, Root-Cause, Disaster, and Restoration Forms",
        "Incident Notice · Outage Report · Root-Cause Analysis · "
        "Disaster Declaration · Restoration Completion",
        "Incident & Restoration Forms",
    )
    sla = C.DEAL['sla']
    C.para(doc,
           f"These forms operationalize the incident, outage, and restoration "
           f"obligations under the {C.AGREEMENTS['om']} and the "
           f"{C.AGREEMENTS['privacy']}. Severity classifications tie to the "
           f"service-level targets in Schedule S6 ({C.SCHEDULES['S6']}) and "
           f"Schedule S11 ({C.SCHEDULES['S11']}). The Network Operations Center "
           f"operates {sla['noc']}.")

    # Severity reference table (from C.DEAL['sla'])
    C.section(doc, "7.0", "Severity & Service-Level Reference")
    C.add_table(doc,
                ["Severity", "Response", "Dispatch", "Restore Target"],
                [
                    ["P1 — Critical / major outage",
                     f"{sla['P1_response_min']} min", f"{sla['P1_dispatch_hr']} hr",
                     f"{sla['P1_restore_hr']} hr"],
                    ["P2 — Significant degradation",
                     f"{sla['P2_response_min']} min", f"{sla['P2_dispatch_hr']} hr",
                     f"{sla['P2_restore_hr']} hr"],
                    ["P3 — Minor / limited impact",
                     f"{sla['P3_response_hr']} hr", f"{sla['P3_dispatch_hr']} hr",
                     f"{sla['P3_restore_days']} days"],
                    ["P4 — Informational / low",
                     f"{sla['P4_response_hr']} hr", "—",
                     f"{sla['P4_restore_days']} days"],
                ],
                widths=[2.6, 1.3, 1.3, 1.4], font_size=8)
    C.para(doc, f"Availability target: {sla['availability_target']}; latency "
                f"≤ {sla['latency_ms']} ms; packet loss ≤ {sla['packet_loss']}; "
                f"jitter ≤ {sla['jitter_ms']} ms.")

    # --- Form 7.1 Incident Notice ---------------------------------------
    form_title(doc, "7.1", "Incident Notice")
    fields(doc, [
        ("Incident No. / Date-Time:", C.PH("number / date-time detected")),
        ("Reported By / Source:", C.PH("NOC / customer / monitoring / field")),
        ("Severity (P1–P4):", C.PH("severity per Section 7.0")),
        ("Affected Segment / Assets:", C.PH("segment ID / assets / equipment")),
        ("Affected Area / Subscribers:", C.PH("area / estimated subscriber count")),
        ("Nature of Incident:", C.PH("outage / degradation / security / physical / environmental")),
        ("Security / Data Involved?:", C.PH("Y/N — if Y, follow privacy addendum")),
        ("Immediate Actions Taken:", C.PH("actions")),
        ("Notifications Made:", C.PH("Tribe, NTIA (if required), law enforcement, customers")),
    ])
    C.flag_para(doc, C.FLAG_GRANT,
                "If the incident involves a data breach, covered telecom, or a "
                f"material Award compliance matter, assess mandatory disclosure "
                f"under {C.CITES['disclosures']} and CPNI obligations "
                f"({C.CITES['cpni']}).")
    sig_block(doc, ["RIVR Tech NOC / Incident Lead",
                    C.TRIBE_SHORT + " (notified)"])

    # --- Form 7.2 Outage Report -----------------------------------------
    form_title(doc, "7.2", "Outage Report")
    fields(doc, [
        ("Outage No. / Related Incident:", C.PH("number / incident ref")),
        ("Severity (P1–P4):", C.PH("severity")),
        ("Start Date-Time:", C.PH("detected / actual start")),
        ("Response Time:", C.PH("time to response — compare to SLA target")),
        ("Dispatch Time:", C.PH("time to dispatch — compare to SLA target")),
        ("Restoration Date-Time:", C.PH("service restored")),
        ("Total Duration:", C.PH("duration")),
        ("Affected Subscribers / Locations:", C.PH("count / list")),
        ("Root Cause (preliminary):", C.PH("preliminary cause — full RCA on Form 7.3")),
        ("SLA Compliance:", C.PH("met / missed each target — reference Section 7.0")),
        ("Credits / Remedies Due:", C.PH("per SLA credit schedule, if any")),
    ])
    C.flag_para(doc, C.FLAG_TECH,
                "Compare actual response, dispatch, and restoration against the "
                "Section 7.0 targets and flag any SLA miss for the credit calculation.")
    sig_block(doc, ["RIVR Tech NOC / Operations Manager",
                    C.TRIBE_SHORT + " (reviewed)"])

    # --- Form 7.3 Root-Cause Analysis -----------------------------------
    form_title(doc, "7.3", "Root-Cause Analysis (RCA)")
    fields(doc, [
        ("RCA No. / Related Outage:", C.PH("number / outage ref")),
        ("Incident Summary:", C.PH("what happened")),
        ("Timeline:", C.PH("detection → response → dispatch → restoration milestones")),
        ("Direct Cause:", C.PH("immediate technical cause")),
        ("Root Cause(s):", C.PH("underlying root cause(s) — 5-why / fault tree")),
        ("Contributing Factors:", C.PH("process, environmental, third-party, supply-chain")),
        ("Corrective Actions:", C.PH("actions to prevent recurrence")),
        ("Preventive / Systemic Actions:", C.PH("longer-term systemic fixes")),
        ("Owner / Due Date:", C.PH("responsible party / date for each action")),
        ("Verification of Effectiveness:", C.PH("how effectiveness will be confirmed")),
    ])
    sig_block(doc, ["RIVR Tech Operations Manager",
                    "RIVR Tech Engineering",
                    C.TRIBE_SHORT + " (accepted)"])

    # --- Form 7.4 Disaster Declaration ----------------------------------
    form_title(doc, "7.4", "Disaster Declaration")
    C.para(doc, "Declares a disaster or major-event condition invoking the "
                "business-continuity and disaster-recovery provisions of the "
                f"{C.AGREEMENTS['privacy']} and Schedule S11.")
    fields(doc, [
        ("Declaration No. / Date-Time:", C.PH("number / date-time")),
        ("Declared By:", C.PH("authorized RIVR Tech officer")),
        ("Event Type:", C.PH("storm / flood / fire / cyber / power / other")),
        ("Geographic Scope:", C.PH("affected portion of the Approved Project Area")),
        ("Assets / Services Affected:", C.PH("assets, segments, services")),
        ("Estimated Impact:", C.PH("subscribers affected / duration estimate")),
        ("Continuity Plan Activated:", C.PH("BC/DR plan reference activated")),
        ("Step-In Considered?:", f"{C.PH('Y/N')} — {C.DEAL['stepin_emergency']}"),
        ("External Coordination:", C.PH("emergency management, mutual aid, LREMC, NTIA")),
        ("Expected Recovery Objective:", C.PH("RTO / RPO targets")),
    ])
    C.flag_para(doc, C.FLAG_BUSINESS,
                "A disaster declaration may trigger emergency step-in, mutual-aid, "
                "insurance, and force-majeure provisions across the agreements; "
                "notify the Tribe and, where required, NTIA promptly.")
    sig_block(doc, ["RIVR Tech authorized officer",
                    C.TRIBE_SHORT + " (notified / concurrence)"])

    # --- Form 7.5 Restoration Completion --------------------------------
    form_title(doc, "7.5", "Restoration-Completion Form")
    fields(doc, [
        ("Related Incident / Outage / Declaration:", C.PH("references")),
        ("Restoration Completion Date-Time:", C.PH("date-time")),
        ("Scope of Restoration:", C.PH("what was restored / replaced / repaired")),
        ("Temporary vs. Permanent:", C.PH("temporary fix in place? permanent repair scheduled?")),
        ("Test Results / Verification:", f"{C.OPTICAL['otdr']} / service tests — " +
         C.PH("results confirming restoration")),
        ("Service Confirmed With Subscribers:", C.PH("verification method")),
        ("Follow-Up / Open Items:", C.PH("permanent repair, warranty claim, RCA actions")),
        ("SLA / Credit Reconciliation:", C.PH("final SLA determination and credits")),
    ])
    C.flag_para(doc, C.FLAG_TECH,
                "Confirm optical and service performance meet the Section 7.0 "
                "targets before closing the event.")
    sig_block(doc, ["RIVR Tech Operations Manager",
                    C.TRIBE_SHORT + " (acceptance of restoration)"])

    C.para(doc, f"Cross-reference: {C.AGREEMENTS['om']} and {C.AGREEMENTS['privacy']}.")
    disclaimer(doc)
    return C.save(doc, OUT_DIR,
                  "07_Incident_Outage_RCA_and_Restoration_Forms.docx")


# ===========================================================================
#  FILE 8 — PROGRAM CHECKLISTS (5 sheets) (.xlsx)
# ===========================================================================
def _checklist_sheet(wb, name, tab, title, subtitle, items):
    ws = wb.create_sheet(name)
    ws.sheet_properties.tabColor = tab
    C.xl_title(ws, title, subtitle=subtitle, span=5)
    for col, w in zip("ABCDE", [52, 22, 16, 22, 34]):
        ws.column_dimensions[col].width = w
    hr = 5
    C.xl_header_row(ws, hr, ["Item", "Responsible", "Status", "Doc Ref", "Notes"])
    r = hr + 1
    first = r
    for text, resp in items:
        C.xl_cell(ws, r, 1, text, "text", wrap=True)
        C.xl_cell(ws, r, 2, resp, "text", wrap=True)
        C.xl_cell(ws, r, 3, C.PH("status"), "input", align="center")
        C.xl_cell(ws, r, 4, C.PH("doc ref"), "input", wrap=True)
        C.xl_cell(ws, r, 5, C.PH("notes"), "input", wrap=True)
        r += 1
    last = r - 1
    _status_validation(ws, "C", first, last)
    # progress check
    r += 1
    C.xl_check(ws, r, 1,
               f'=IF(COUNTIF(C{first}:C{last},"Complete")+'
               f'COUNTIF(C{first}:C{last},"N/A")={last-first+1},'
               f'"PASS — all items resolved","IN PROGRESS — open items remain")',
               "All items Complete or N/A:")
    return ws


def build_program_checklists():
    wb = Workbook()
    C.xl_instructions(wb, [
        "## Program Checklists",
        "Five program checklists spanning the transaction lifecycle for the "
        + C.PROGRAM_SHORT + " project.",
        "• Each sheet has frozen, filterable headers and a Status dropdown "
        "(Not Started / In Progress / Complete / N/A).",
        "• Amber INPUT columns (Status / Doc Ref / Notes) are yours to complete.",
        "• Cross-references: the Definitive Agreements and Schedules S1–S14.",
        "• " + C.DRAFT_STATUS_SHORT,
    ])
    T, R, RT, L = C.TRIBE_SHORT, C.OPERATOR_SHORT, C.OPERATOR_SHORT, C.LREMC_SHORT

    _checklist_sheet(
        wb, "Closing Checklist", "1F3864", "Closing Checklist",
        "Conditions to closing the coordinated TBCP transaction",
        [
            ("Executed federal Award confirmed (controlling round / FAIN)", "Grant Counsel"),
            (C.AGREEMENTS['master'] + " executed", "Both Parties"),
            ("All Definitive Agreements executed", "Both Parties"),
            ("Tribal Council resolutions / authorizations", T),
            ("Corporate authorizations (RIVR Tech / LREMC)", RT + " / " + L),
            ("Document-precedence schedule (S1) finalized", "Grant Counsel"),
            ("Land / easement / ROW instruments recorded (S9)", T + " / " + L),
            ("BIA approvals for trust / restricted land (25 CFR 162/169)", "Grant Counsel"),
            ("Insurance certificates in force (Exhibit I limits)", RT),
            ("Lender consents obtained (if financed assets)", RT + " / " + L),
            ("NTIA consent to IRU / operating arrangement", "Grant Counsel"),
            ("§889 / covered-telecom certifications (" + C.CITES['telecom_ban'] + ")", RT),
            ("SAM.gov registration active", "Grant Counsel"),
            ("Conflict-of-interest disclosures (" + C.CITES['conflict'] + ")", "Both Parties"),
        ])

    _checklist_sheet(
        wb, "Construction-Release", "375623", "Construction-Release Checklist",
        "Conditions to releasing construction (per segment)",
        [
            ("Notice to Proceed issued (Form 1.1)", RT + " PM"),
            ("NEPA environmental review complete (" + C.CITES['nepa'] + ")", "Grant Counsel"),
            ("NHPA §106 review complete (" + C.CITES['nhpa'] + ")", "Grant Counsel"),
            ("Permits obtained (NCDOT / encroachment — " + C.CITES['nc_ncdot'] + ")", RT),
            ("Pole attachment authorizations (" + C.CITES['nc_pole'] + ")", RT + " / " + L),
            ("811 utility locates complete (" + C.CITES['nc_dig'] + ")", RT),
            ("BABA compliance plan in place (" + C.CITES['baba'] + ")", "Grant Counsel"),
            ("Procurement performed per " + C.CITES['procurement'], "Grant Counsel"),
            ("Bill of materials / engineering approved (S4)", T + " / " + RT),
            ("Construction pricing / milestones set (S5)", "Both Parties"),
            ("Builders-risk / construction insurance in force", RT),
            ("Site safety plan in place", RT),
        ])

    _checklist_sheet(
        wb, "Service-Launch", "7F007F", "Service-Launch Checklist",
        "Conditions to launching retail service on a segment",
        [
            ("Segment Acceptance Form executed (Form 1.9)", T + " / " + RT),
            ("OTDR / optical test results on file (" + C.OPTICAL['otdr'] + ")", RT),
            ("Segment IRU Activation Certificate executed (Form 02)", "Both Parties"),
            ("Retail provider-of-record readiness (S7)", RT),
            ("Billing / collections system live", RT),
            ("Affordability program enrollment (Lifeline/ETC — " + C.CITES['usac_lifeline'] + ")", RT),
            ("Subscriber onboarding process ready", RT),
            ("NOC 24x7x365 monitoring live", RT),
            ("SLA monitoring & reporting configured (S6)", RT),
            ("CPNI / privacy controls in place (" + C.CITES['cpni'] + ")", RT),
            ("Data privacy & cybersecurity addendum in effect (S11)", "Both Parties"),
            ("Subscriber payment / reconciliation process ready (S8)", RT + " / " + T),
        ])

    _checklist_sheet(
        wb, "Annual-Compliance", "BF8F00", "Annual-Compliance Checklist",
        "Recurring annual compliance obligations",
        [
            ("Single audit filed if expenditures ≥ $1,000,000 (" + C.CITES['single_audit'] + ")",
             T + " / Auditor"),
            ("Performance & financial reports to NTIA", "Grant Counsel"),
            ("Program-income reporting (" + C.CITES['prog_income'] + ")", "Grant Counsel"),
            ("Asset / property register updated (" + C.CITES['equipment'] + ")", RT),
            ("Federal-Interest register reconciled (" + C.CITES['trust'] + ")", "Grant Counsel"),
            ("Reimbursement records retained (" + C.CITES['records'] + ")", "Grant Counsel"),
            ("BABA ongoing compliance confirmed", "Grant Counsel"),
            ("§889 re-certification (" + C.CITES['telecom_ban'] + ")", RT),
            ("Insurance renewals confirmed", RT),
            ("SLA performance review (S6)", "Both Parties"),
            ("Replacement-reserve funding reviewed (S6)", "Both Parties"),
            ("Conflict-of-interest annual disclosures (" + C.CITES['conflict'] + ")", "Both Parties"),
            ("Annual budget / sustainability review completed (Form 05)", "Both Parties"),
        ])

    _checklist_sheet(
        wb, "Termination-Transition", "C00000", "Termination / Transition Checklist",
        "Steps on default, termination, or transition of operations",
        [
            ("Default / cure status determined (cure: " +
             str(C.DEAL['cure_monetary_days']) + "d monetary / " +
             str(C.DEAL['cure_nonmonetary_days']) + "d non-monetary)", "Grant Counsel"),
            ("Step-in triggers assessed (" + C.DEAL['stepin_emergency'][:40] + "…)", "Both Parties"),
            ("Transition-assistance plan activated (" +
             str(C.DEAL['transition_assistance_months']) + " months)", RT),
            ("Records & asset transfer to " + T, RT),
            ("Software / license assignment (assignable licenses)", RT),
            ("Subscriber notification & continuity", RT),
            ("NTIA notification of transition / termination", "Grant Counsel"),
            ("Federal-interest disposition (" + C.CITES['real_property'] + "; " +
             C.CITES['trust'] + ")", "Grant Counsel"),
            ("Award closeout (" + C.CITES['closeout'] + ")", "Grant Counsel"),
            ("Post-closeout obligations acknowledged (200.345)", "Grant Counsel"),
            ("Lien releases / lender payoff (if any)", RT + " / " + L),
            ("Final reconciliation & payment (Form 04)", "Both Parties"),
        ])

    return C.xl_save(wb, OUT_DIR, "08_Program_Checklists.xlsx")


# ===========================================================================
#  MAIN
# ===========================================================================
def main():
    builders = [
        ("01 Construction Forms (docx)", build_construction_forms),
        ("02 Segment IRU Activation Certificate (docx)", build_iru_activation_certificate),
        ("03 Grant Evidence Checklist + Cert (xlsx)", build_grant_evidence_checklist),
        ("04 Subscriber Reconciliation + Payment (xlsx)", build_subscriber_reconciliation),
        ("05 Annual Budget / Reserve / Sustainability (xlsx)", build_annual_budget),
        ("06 Project Registers (xlsx)", build_project_registers),
        ("07 Incident / Outage / RCA / Restoration (docx)", build_incident_forms),
        ("08 Program Checklists (xlsx)", build_program_checklists),
    ]
    results = []
    for label, fn in builders:
        path = fn()
        results.append((label, path))
        print(f"[OK] {label}\n     -> {path}")
    print(f"\nGenerated {len(results)} operational-form files into {OUT_DIR}/")
    return results


if __name__ == "__main__":
    main()
