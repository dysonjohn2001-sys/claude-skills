#!/usr/bin/env python3
"""
gen_exhibits.py — Deliverable 9: the 15 Operational Exhibits (A–O) for the
Lumbee Tribe of North Carolina / RIVR Tech broadband IRU partnership package.

Every document is a working draft. All party names, defined terms, SLA targets,
insurance limits, optical standards, citations, and placeholders come from the
canonical module Scripts/common.py — the single source of truth.

Run:  python3 gen_exhibits.py
Output lands in  Lumbee_RIVR_Tech_IRU_Package/03_Operational_Schedules/
"""

from __future__ import annotations

import sys
sys.path.insert(0, "/home/user/claude-skills/Lumbee_RIVR_Tech_IRU_Package/Scripts")
import common as C

from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

OUT_DIR = "03_Operational_Schedules"


# ---------------------------------------------------------------------------
# small local helpers layered on top of common.py
# ---------------------------------------------------------------------------
def _widths(ws, widths):
    """Set column widths from a list keyed by 1-based column index."""
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w


def _guarded_sum_check(component_range, total_ref):
    """A formula check that tolerates placeholder (text) inputs gracefully."""
    return (f'=IF(AND(ISNUMBER({total_ref}),SUM({component_range})>0),'
            f'IF(SUM({component_range})={total_ref},"PASS — allocations tie to total",'
            f'"FAIL — allocations do not sum to total"),"ENTER STRAND COUNTS")')


def _date_order_check(start_ref, finish_ref):
    return (f'=IF(AND(ISNUMBER({start_ref}),ISNUMBER({finish_ref})),'
            f'IF({finish_ref}>={start_ref},"OK","CHECK — finish precedes start"),'
            f'"ENTER DATES")')


def _cover(doc, exhibit_no, title, subtitle):
    C.add_cover(doc, f"EXHIBIT {exhibit_no}", title, subtitle)
    C.setup_header_footer(doc, f"Exhibit {exhibit_no}")
    C.status_banner(doc)
    C.spacer(doc, 1)


# ===========================================================================
# EXHIBIT A — Project Area and Route Schedule  (DOCX)
# ===========================================================================
def exhibit_A():
    doc = C.new_doc()
    _cover(doc, "A", "PROJECT AREA AND ROUTE SCHEDULE",
           "Service Territory, Route Inventory, and Anchor Institutions")

    C.article(doc, 1, "Service Territory")
    C.section(doc, "1.1", "Description of the Service Territory",
              f"The Service Territory for the {C.NETWORK} lies within {C.GEOGRAPHY}. "
              f"It comprises the Tribal service area of the {C.TRIBE_FULL} and the "
              f"contiguous unserved and underserved areas targeted for buildout under "
              f"the {C.PROGRAM_FULL} ({C.PROGRAM_SHORT}). The precise geographic scope "
              f"is defined by the polygons, county lists, and census blocks identified "
              f"in the funded application and is subject to confirmation against the "
              f"final {C.AGENCY_SHORT} award.")
    C.para(doc,
           f"Approximate served area: {C.PH('total square miles of Service Territory')}. "
           f"Counties: {C.PH('list of North Carolina counties, e.g., Robeson, Hoke, Scotland, Cumberland, Bladen')}. "
           f"Census blocks / broadband serviceable locations: "
           f"{C.PH('count and identifiers of eligible census blocks / BSLs from the funded application')}.")
    C.flag_para(doc, C.FLAG_TECH,
                "Exact Service Territory boundary, county list, and census-block "
                "inventory to be supplied from the GIS / broadband-serviceable-location "
                "layer used in the funded application.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Eligibility of the Service Territory turns on the Lumbee Tribe's "
                "federal-recognition status under the " + C.CITES["lumbee_act"] +
                "; confirm TBCP eligibility footprint against the award before construction.")

    C.section(doc, "1.2", "Map Reference",
              "The Service Territory and all routes in the Route Schedule below are "
              "depicted on the project map set incorporated by reference.")
    C.para(doc, f"Map set reference: {C.PH('map set title, revision number, and date')}. "
                f"Coordinate system: {C.PH('e.g., NAD83 / North Carolina State Plane (2264)')}. "
                f"Authoritative GIS package: {C.PH('file name / repository path for the geospatial deliverable')}.")

    C.article(doc, 2, "Route Schedule")
    C.section(doc, "2.1", "Route Inventory",
              "The following routes constitute the physical plant of the Network. "
              "Ownership indicates whether a route is a grant-funded Tribal Asset owned "
              f"by the {C.TRIBE_SHORT}, an existing {C.OPERATOR_EXISTING} asset owned by "
              f"{C.OPERATOR_SHORT}, or a Jointly Funded Asset.")
    headers = ["Route ID", "Segment (from → to)", "Approx. miles",
               "Fiber count", "Ownership", "Status"]
    rows = [
        [C.PH("R-001"), C.PH("segment endpoints"), C.PH("mi"), C.PH("ct"),
         C.PH("Lumbee Tribe / RIVR Tech / Joint"), C.PH("planned/in-progress/complete")],
        [C.PH("R-002"), C.PH("segment endpoints"), C.PH("mi"), C.PH("ct"),
         C.PH("Lumbee Tribe / RIVR Tech / Joint"), C.PH("status")],
        [C.PH("R-003"), C.PH("segment endpoints"), C.PH("mi"), C.PH("ct"),
         C.PH("Lumbee Tribe / RIVR Tech / Joint"), C.PH("status")],
        [C.PH("MM-001 (middle-mile)"), C.PH("existing backbone segment"), C.PH("mi"),
         C.PH("ct"), C.OPERATOR_SHORT, C.PH("in service")],
    ]
    C.add_table(doc, headers, rows,
                widths=[0.8, 1.9, 0.8, 0.8, 1.2, 1.0], font_size=9)
    C.flag_para(doc, C.FLAG_TECH,
                "Route inventory, mileages, fiber counts, and as-built status to be "
                "populated from the OSP design and GIS route data (see Exhibit E for "
                "as-built / GIS delivery requirements).")

    C.article(doc, 3, "Anchor Institutions")
    C.section(doc, "3.1", "Community Anchor Institutions Served",
              "The following community anchor institutions are prioritized for "
              "connection within the Service Territory:")
    for label in ["Tribal government facilities", "Public schools / education",
                  "Health care / clinics", "Public safety / emergency services",
                  "Libraries and community centers", "Higher education"]:
        C.bullet(doc, f"{label}: {C.PH('facility name(s), address(es), and route/segment reference')}")
    C.flag_para(doc, C.FLAG_TECH,
                "Anchor-institution list, addresses, and required service levels to be "
                "confirmed against the funded application and Exhibit M service tiers.")

    return C.save(doc, OUT_DIR, "Exhibit_A_Project_Area_and_Route_Schedule.docx")


# ===========================================================================
# EXHIBIT B — Asset Ownership and Demarcation Matrix  (XLSX)
# ===========================================================================
def exhibit_B():
    wb = Workbook()
    C.xl_instructions(wb, [
        "## Exhibit B — Asset Ownership and Demarcation Matrix",
        "Purpose: classify every physical and intangible network asset by funding "
        "source, owner, federal-interest status, and demarcation point.",
        "",
        "## How to use",
        "• AMBER cells are inputs — replace each [■ ...] placeholder with confirmed data.",
        "• Grant-funded Tribal Assets are owned by the Lumbee Tribe and carry a Federal Interest "
        "(YES) under 2 CFR 200.313 and the property-trust relationship of 2 CFR 200.316.",
        "• RIVR Tech Existing Network (middle-mile backbone, core electronics) is owned by "
        "RIVR Tech and carries NO federal interest.",
        "• The Demarcation Point is the physical boundary where ownership, operational "
        "responsibility, and maintenance obligation pass between the Parties.",
        "",
        "## Governing authority",
        "• " + C.CITES["equipment"],
        "• " + C.CITES["trust"],
        "• " + C.CITES["intangible"],
        "• " + C.CITES["real_property"],
        "",
        "## Status",
        "• " + C.DRAFT_STATUS,
    ])

    ws = wb.create_sheet("Asset Matrix")
    C.xl_title(ws, "EXHIBIT B — ASSET OWNERSHIP AND DEMARCATION MATRIX",
               subtitle=f"{C.TRIBE_FULL} and {C.OPERATOR_FULL}", span=8)
    headers = ["Asset Category", "Description", "Funding Source",
               "Owner (Lumbee Tribe/RIVR Tech/Joint)", "Federal Interest (Y/N)",
               "Demarcation Point", "Location Ref", "Notes"]
    hrow = 5
    C.xl_header_row(ws, hrow, headers)
    _widths(ws, [22, 34, 22, 18, 14, 30, 16, 34])

    T = "Lumbee Tribe"; O = C.OPERATOR_SHORT
    GF = "TBCP grant-funded (Tribal Assets)"
    EX = f"{O} pre-existing capital ({C.OPERATOR_EXISTING})"
    # (category, description, funding, owner, fed_interest, demarc, notes)
    data = [
        ("Fiber strands (access/distribution)", "Grant-funded OSP fiber serving BSLs",
         GF, T, "YES", "Strand hand-off at the demarcation panel / meet-me point",
         C.PH("route/segment ref"), "Reserved Tribal strands per Exhibit C"),
        ("Conduit / innerduct", "Underground conduit path for OSP fiber",
         GF, T, "YES", "Property line / right-of-way boundary at handhole",
         C.PH("route ref"), "Grant-funded real-property-adjacent asset"),
        ("Handholes / vaults", "Access structures along the route",
         GF, T, "YES", "At structure", C.PH("GIS point ID"), C.PH("qty")),
        ("Splice enclosures / closures", "Fusion-splice housings",
         GF, T, "YES", "At enclosure", C.PH("GIS point ID"), C.PH("qty")),
        ("Huts", "Prefabricated equipment huts",
         GF, T, "YES", "Hut wall penetration / entrance facility",
         C.PH("site ref"), C.PH("shared vs. dedicated")),
        ("Cabinets", "Outdoor field cabinets",
         GF, T, "YES", "Cabinet bulkhead", C.PH("site ref"), C.PH("qty")),
        ("Shelters", "Equipment shelters",
         GF, T, "YES", "Shelter entrance", C.PH("site ref"), C.PH("qty")),
        ("Termination panels / FDPs", "Fiber distribution / termination panels",
         GF, T, "YES", "Panel port — hand-off boundary", C.PH("site ref"),
         "Primary physical demarcation for strand hand-off"),
        ("OLTs", "Optical line terminals (access electronics)",
         GF, T, "YES", "Equipment rack / OLT chassis", C.PH("site ref"),
         C.PH("make/model")),
        ("ONTs", "Optical network terminals (customer premises)",
         GF, T, "YES", "Customer-side of the ONT (UNI port)",
         C.PH("premises ref"), "Subscriber demarcation"),
        ("Routers / switches (access/agg)", "Grant-funded aggregation electronics",
         GF, T, "YES", "Rack unit / uplink port", C.PH("site ref"), C.PH("make/model")),
        ("Core electronics", "Backbone routing/switching core",
         EX, O, "NO", "Core uplink port to Tribal aggregation", C.PH("POP ref"),
         f"{O} existing asset — no federal interest"),
        ("Middle-mile interconnect", "Existing middle-mile backbone segments",
         EX, O, "NO", "Meet-me point / interconnection panel at POP",
         C.PH("POP ref"), "Clear demarcation to Tribal access plant"),
        ("Easement / IRU rights (intangible)", "Route easements and license rights",
         C.PH("grant-funded vs. contributed — confirm per parcel"),
         C.PH("Lumbee Tribe / RIVR Tech / Joint"), C.PH("Y/N — per 2 CFR 200.315/200.311"),
         "N/A (intangible)", C.PH("parcel/agreement ref"),
         "Intangible property — see 2 CFR 200.315"),
        ("Poles / pole attachments", "Attachments to third-party utility poles",
         C.PH("attachment make-ready funding source"),
         C.PH("Lumbee Tribe / RIVR Tech / pole owner"), C.PH("Y/N"),
         "Attachment point on pole", C.PH("pole owner / tag"),
         "Subject to N.C. Gen. Stat. § 62-350"),
    ]
    r = hrow + 1
    for row in data:
        cat, desc, fund, owner, fed, demarc, loc, notes = row
        C.xl_cell(ws, r, 1, cat, "text", bold=True, wrap=True)
        C.xl_cell(ws, r, 2, desc, "text", wrap=True)
        C.xl_cell(ws, r, 3, fund, "input" if fund.startswith("[■") else "text", wrap=True)
        C.xl_cell(ws, r, 4, owner, "input" if owner.startswith("[■") else "output", wrap=True)
        C.xl_cell(ws, r, 5, fed, "input" if fed.startswith("[■") else "output",
                  align="center")
        C.xl_cell(ws, r, 6, demarc, "text", wrap=True)
        C.xl_cell(ws, r, 7, loc, "input", wrap=True)
        C.xl_cell(ws, r, 8, notes, "text", wrap=True)
        r += 1

    # legend + demarcation explanation
    C.xl_legend(ws, r + 1)
    r += 3
    C.xl_cell(ws, r, 1, "Demarcation legend", "section")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
    r += 1
    for note in [
        "The Demarcation Point is the physical (or logical) boundary at which "
        "ownership, operational control, maintenance responsibility, and risk of loss "
        "pass between the Lumbee Tribe (Tribal Assets) and RIVR Tech (RIVR Tech Existing "
        "Network / core).",
        "On the Lumbee Tribe's side of each Demarcation Point the plant is a grant-funded "
        "Tribal Asset subject to the Federal Interest and the property-trust "
        "relationship (2 CFR 200.316) until disposition per 2 CFR 200.313.",
        "On RIVR Tech's side the plant is a pre-existing RIVR Tech capital asset with "
        "no federal interest; RIVR Tech operates the Tribal Assets under the IRU.",
        "Where a single structure houses both Parties' equipment (e.g., a shared hut), "
        "the Demarcation Point is the panel/port hand-off identified above, not the "
        "structure itself.",
    ]:
        C.xl_cell(ws, r, 1, "• " + note, "text", wrap=True)
        ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
        ws.row_dimensions[r].height = 30
        r += 1

    return C.xl_save(wb, OUT_DIR, "Exhibit_B_Asset_Ownership_and_Demarcation_Matrix.xlsx")


# ===========================================================================
# EXHIBIT C — Fiber Allocation and Reserved Capacity  (XLSX)
# ===========================================================================
def exhibit_C():
    wb = Workbook()
    C.xl_instructions(wb, [
        "## Exhibit C — Fiber Allocation and Reserved Capacity",
        "Purpose: allocate strand capacity on each route among RIVR Tech operating use, "
        "RESERVED TRIBAL capacity, anchor-institution use, and dark/spare.",
        "",
        "## How to use",
        "• AMBER cells are inputs — enter integer strand counts (replace [■ ...]).",
        "• BLUE cells are formulas — the allocated total is summed automatically.",
        "• The CHECK column verifies that RIVR Tech + Reserved Tribal + Anchor + "
        "Dark/Spare equals the Total strand count for each route.",
        "• Reserved Tribal strands are held for the Lumbee Tribe's own governmental, "
        "educational, health, and public-safety use and are not marketed by RIVR Tech.",
        "",
        "## Status",
        "• " + C.DRAFT_STATUS,
    ])

    ws = wb.create_sheet("Fiber Allocation")
    C.xl_title(ws, "EXHIBIT C — FIBER ALLOCATION AND RESERVED CAPACITY",
               subtitle="Strand allocation with automatic tie-out to total count",
               span=8)
    headers = ["Route", "Total strands", "RIVR Tech operating strands",
               "RESERVED TRIBAL strands", "Anchor-institution strands",
               "Dark / spare", "Allocated (formula)", "Notes"]
    hrow = 5
    C.xl_header_row(ws, hrow, headers)
    _widths(ws, [16, 13, 20, 20, 20, 13, 16, 30])

    routes = [C.PH("R-001"), C.PH("R-002"), C.PH("R-003"), C.PH("MM-001 (middle-mile)")]
    first = hrow + 1
    r = first
    for route in routes:
        C.xl_cell(ws, r, 1, route, "input", wrap=True)
        C.xl_cell(ws, r, 2, C.PH("total"), "input", align="center")   # B
        C.xl_cell(ws, r, 3, C.PH("count"), "input", align="center")   # C RIVR
        C.xl_cell(ws, r, 4, C.PH("count"), "input", align="center")   # D reserved tribal
        C.xl_cell(ws, r, 5, C.PH("count"), "input", align="center")   # E anchor
        C.xl_cell(ws, r, 6, C.PH("count"), "input", align="center")   # F dark/spare
        # G = SUM(C:F) allocated
        C.xl_cell(ws, r, 7, f"=SUM(C{r}:F{r})", "formula",
                  fmt=C.FMT_NUM, align="center")
        C.xl_cell(ws, r, 8, C.PH("route-specific notes"), "text", wrap=True)
        r += 1
    last = r - 1

    # per-route tie-out checks
    r += 1
    C.xl_cell(ws, r, 1, "Allocation tie-out checks", "section")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
    r += 1
    for rr in range(first, last + 1):
        C.xl_check(ws, r, 1,
                   f'=IF(AND(ISNUMBER(B{rr}),G{rr}>0),'
                   f'IF(G{rr}=B{rr},"PASS","FAIL — allocated <> total"),"ENTER COUNTS")',
                   f"Route on row {rr}: allocated (G{rr}) = total (B{rr})?")
        r += 1

    # Reserved Tribal capacity section
    r += 1
    C.xl_cell(ws, r, 1, "Reserved Tribal Capacity — dedicated public-purpose use", "section")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8)
    r += 1
    sub_hdr = ["Reserved use", "Strands reserved", "Route(s)", "Priority", "Notes"]
    for i, h in enumerate(sub_hdr):
        C.xl_cell(ws, r, i + 1, h, "section")
    r += 1
    reserved = [
        ("Tribal government / administration", C.PH("count"), C.PH("route ref"),
         "High", "Continuity of essential Tribal services"),
        ("Public schools / education", C.PH("count"), C.PH("route ref"),
         "High", "Anchor institution"),
        ("Health care / clinics", C.PH("count"), C.PH("route ref"),
         "High", "Life-safety dependent"),
        ("Public safety / emergency services", C.PH("count"), C.PH("route ref"),
         "Highest", "911 / first responders — hardened path preferred"),
    ]
    res_first = r
    for use, cnt, rt, prio, note in reserved:
        C.xl_cell(ws, r, 1, use, "text", wrap=True)
        C.xl_cell(ws, r, 2, cnt, "input", align="center")
        C.xl_cell(ws, r, 3, rt, "input", wrap=True)
        C.xl_cell(ws, r, 4, prio, "text", align="center")
        C.xl_cell(ws, r, 5, note, "text", wrap=True)
        r += 1
    res_last = r - 1
    C.xl_cell(ws, r, 1, "Total reserved (formula)", "text", bold=True)
    C.xl_cell(ws, r, 2, f"=SUM(B{res_first}:B{res_last})", "formula",
              fmt=C.FMT_NUM, align="center")

    return C.xl_save(wb, OUT_DIR, "Exhibit_C_Fiber_Allocation_and_Reserved_Capacity.xlsx")


# ===========================================================================
# EXHIBIT D — Construction Milestones  (XLSX)
# ===========================================================================
def exhibit_D():
    wb = Workbook()
    C.xl_instructions(wb, [
        "## Exhibit D — Construction Milestones",
        "Purpose: sequence the buildout, tie milestones to payment/triggers and grant "
        "reporting, and enforce that no construction begins before environmental "
        "clearance and NTIA authorization to construct.",
        "",
        "## Hard sequencing rule",
        "• NO CONSTRUCTION may begin before NEPA/NHPA environmental clearance and "
        "NTIA authorization to construct are obtained.",
        "• " + C.CITES["nepa"],
        "• " + C.CITES["nhpa"],
        "",
        "## How to use",
        "• AMBER cells are inputs — enter dates and % complete.",
        "• The CHECK column verifies Planned Finish >= Planned Start for each milestone.",
        "• Enter dates as real Excel dates so the checks evaluate numerically.",
        "",
        "## Status",
        "• " + C.DRAFT_STATUS,
    ])

    ws = wb.create_sheet("Milestones")
    C.xl_title(ws, "EXHIBIT D — CONSTRUCTION MILESTONES",
               subtitle="Environmental clearance and NTIA authorization gate all construction",
               span=9)
    headers = ["Milestone #", "Description", "Predecessor", "Planned Start",
               "Planned Finish", "% Complete", "Payment / Trigger",
               "Grant Reporting Tie", "Finish>=Start (check)"]
    hrow = 5
    C.xl_header_row(ws, hrow, headers)
    _widths(ws, [11, 40, 12, 14, 14, 11, 26, 26, 22])

    ms = [
        ("M1", "NEPA/NHPA environmental clearance AND NTIA authorization to construct "
               "(GATE — no construction before this milestone)", "—",
         "Env. review complete; ATC issued",
         "NTIA authorization to construct; environmental determination on file"),
        ("M2", "Permitting, easements, pole-attachment agreements, and 811 locates",
         "M1", "Right-of-way secured", "Permit/easement package to grant file"),
        ("M3", "Material procurement (BABA-compliant; §889 screening)", "M1",
         "PO issuance / material delivery",
         "BABA compliance certification; " + "Buy-America documentation"),
        ("M4", "Outside-plant (OSP) construction — conduit, fiber placement", "M2, M3",
         "Progress draw(s) by route segment", "Construction progress / disbursement report"),
        ("M5", "Splicing and termination", "M4", "Splice completion by segment",
         "As-built splice records"),
        ("M6", "Electronics installation (OLTs, aggregation, core interconnect)", "M4",
         "Equipment acceptance", "Equipment inventory update (Exhibit K)"),
        ("M7", "Testing and acceptance (Exhibit E standards)", "M5, M6",
         "Acceptance certificate (Exhibit G)", "Acceptance test results filed"),
        ("M8", "Service activation / place in service", "M7",
         "First subscribers; in-service date set",
         "Place-in-service date (federal-interest / depreciation)"),
        ("M9", "Buildout complete / project closeout readiness", "M8",
         "Final draw / retainage release", "Closeout package — " + C.CITES["closeout"]),
    ]
    first = hrow + 1
    r = first
    for num, desc, pred, trig, gtie in ms:
        C.xl_cell(ws, r, 1, num, "text", bold=True, align="center")
        C.xl_cell(ws, r, 2, desc, "text", wrap=True)
        C.xl_cell(ws, r, 3, pred, "text", align="center")
        C.xl_cell(ws, r, 4, C.PH("start date"), "input", align="center")   # D
        C.xl_cell(ws, r, 5, C.PH("finish date"), "input", align="center")  # E
        C.xl_cell(ws, r, 6, C.PH("%"), "input", fmt=C.FMT_PCT, align="center")
        C.xl_cell(ws, r, 7, trig, "text", wrap=True)
        C.xl_cell(ws, r, 8, gtie, "text", wrap=True)
        C.xl_cell(ws, r, 9, _date_order_check(f"D{r}", f"E{r}"), "formula",
                  align="center")
        r += 1
    last = r - 1

    # gate + overall completion
    r += 1
    C.xl_cell(ws, r, 1, "Gate & rollup checks", "section")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=9)
    r += 1
    C.xl_check(ws, r, 1,
               f'=IF(ISNUMBER(D{first}),"OK — M1 environmental gate dated",'
               f'"ENTER M1 CLEARANCE DATE (no construction before M1)")',
               "Environmental/authorization gate (M1) is scheduled first:")
    r += 1
    C.xl_check(ws, r, 1,
               f'=IF(COUNT(F{first}:F{last})=0,"ENTER % COMPLETE",'
               f'ROUND(AVERAGE(F{first}:F{last}),4))',
               "Average % complete across milestones:")

    return C.xl_save(wb, OUT_DIR, "Exhibit_D_Construction_Milestones.xlsx")


# ===========================================================================
# EXHIBIT E — Acceptance Testing Standards  (DOCX)
# ===========================================================================
def exhibit_E():
    doc = C.new_doc()
    _cover(doc, "E", "ACCEPTANCE TESTING STANDARDS",
           "Optical Test Procedures, Pass/Fail Thresholds, and Documentation")

    O = C.OPTICAL
    C.article(doc, 1, "Scope and General Requirements")
    C.section(doc, "1.1", "Scope",
              f"This Exhibit sets the optical acceptance-testing standards that each "
              f"route, segment, and span of the Network — and in particular each "
              f"grant-funded Tribal Asset — must satisfy before it is accepted and "
              f"placed in service. Acceptance is documented on the Network Acceptance "
              f"Certificate in Exhibit G.")
    C.section(doc, "1.2", "Test Wavelengths and Method",
              f"All fiber shall be tested using {O['otdr']} at {O['wavelengths']}. "
              f"Testing shall be performed in both directions on each fiber and the "
              f"results averaged (bi-directional averaging) to establish the certified "
              f"splice and span loss.")
    C.section(doc, "1.3", "Instruments and Calibration",
              f"OTDR, optical power meter, and light source shall be within current "
              f"calibration. Calibration certificates: {C.PH('instrument make/model, serial, and calibration dates')}.")

    C.article(doc, 2, "Test Parameters and Pass/Fail Thresholds")
    C.para(doc, "Each fiber and span shall meet or exceed the following thresholds:")
    headers = ["Test / Parameter", "Wavelength(s)", "Method", "Pass / Fail threshold"]
    rows = [
        ["Fusion splice loss", O["wavelengths"], f"{O['otdr']} (bi-dir avg)",
         O["splice_loss_max"]],
        ["Mated connector loss", O["wavelengths"], "OTDR / insertion loss",
         O["connector_loss_max"]],
        ["Connector reflectance", O["wavelengths"], "OTDR",
         O["reflectance_max"]],
        ["Span / link loss (end-to-end)", O["wavelengths"],
         "Power meter (LSPM) + OTDR", O["span_margin"]],
        ["Continuity / polarity", O["wavelengths"], "Visual / power meter",
         "100% continuity; correct polarity; no high-loss events"],
        ["Length / distance", "1550 nm", "OTDR", C.PH("design length ± tolerance")],
    ]
    C.add_table(doc, headers, rows, widths=[1.9, 1.1, 1.7, 1.8], font_size=9)
    C.flag_para(doc, C.FLAG_TECH,
                "Design span-loss budget per route to be computed from as-built lengths, "
                "splice count, and connector count and attached to the test record.")

    C.article(doc, 3, "Span-Loss Budget")
    C.section(doc, "3.1", "Calculation",
              f"The maximum allowable span loss shall be calculated as the sum of fiber "
              f"attenuation ({O['span_margin']}), plus the number of splices times the "
              f"splice-loss allowance, plus the number of mated connector pairs times "
              f"the connector-loss allowance, plus a design safety margin of "
              f"{C.PH('design margin in dB')}. Measured span loss shall not exceed the "
              f"calculated budget.")

    C.article(doc, 4, "Power-Meter Testing")
    C.section(doc, "4.1", "Insertion-Loss Test",
              f"End-to-end insertion loss shall be measured with a stabilized light "
              f"source and optical power meter (LSPM) at {O['wavelengths']}, referenced "
              f"per a one-jumper (or equivalent) reference method, and shall fall within "
              f"the calculated span-loss budget.")

    C.article(doc, 5, "Test Documentation")
    C.section(doc, "5.1", "Required Deliverables",
              "The following test records shall be delivered for each accepted segment:")
    for item in [
        "OTDR traces (bi-directional) for every fiber, at both wavelengths, in native "
        "and PDF format",
        "Splice-loss and connector-loss tables keyed to the splice diagram",
        "End-to-end insertion-loss (power-meter) results at both wavelengths",
        "Calculated span-loss budget vs. measured loss, with pass/fail per span",
        "Instrument calibration certificates",
        "Fiber assignment / strand mapping keyed to Exhibit C",
    ]:
        C.bullet(doc, item)

    C.section(doc, "5.2", "As-Built and GIS Delivery",
              f"As-built drawings and GIS data shall be delivered as a condition of "
              f"acceptance, including route geometry, splice locations, structure "
              f"inventory, and strand assignments in the coordinate system identified in "
              f"Exhibit A. GIS deliverable format: {C.PH('e.g., Esri File Geodatabase / GeoPackage / shapefile + metadata')}.")
    C.flag_para(doc, C.FLAG_GRANT,
                "As-built and GIS deliverables support the equipment/property records "
                "required by " + C.CITES["equipment"] + " and the asset inventory in "
                "Exhibit K.")

    C.article(doc, 6, "Punch List, Retesting, and Acceptance")
    C.section(doc, "6.1", "Punch-List Process",
              f"Any span, splice, or connector failing a threshold shall be recorded on "
              f"a punch list identifying the deficiency, location, and corrective action. "
              f"RIVR Tech shall remediate and retest the affected element.")
    C.section(doc, "6.2", "Retesting",
              "Remediated elements shall be retested using the same method and "
              "thresholds. A segment is not accepted until all punch-list items are "
              "cleared and the retest passes.")
    C.section(doc, "6.3", "Acceptance Certificate",
              "Upon clearance of the punch list and delivery of the required test "
              "documentation, as-built drawings, and GIS data, the segment is accepted "
              "by execution of the Network Acceptance Certificate (Exhibit G), which "
              "establishes the date placed in service.")

    return C.save(doc, OUT_DIR, "Exhibit_E_Acceptance_Testing_Standards.docx")


# ===========================================================================
# EXHIBIT F — Change Order Form  (DOCX)
# ===========================================================================
def exhibit_F():
    doc = C.new_doc()
    _cover(doc, "F", "CHANGE ORDER FORM",
           "Form of Change Order — Scope, Cost, Schedule, and Grant-Compliance Review")

    C.article(doc, 1, "Change Order")
    C.para(doc, "This Change Order, when fully executed, modifies the scope, cost, "
                "and/or schedule of the Network buildout. No change is effective until "
                "approved by all required signatories below.")

    headers = ["Field", "Entry"]
    ident = [
        ["Change Order No.", C.PH("CO-###")],
        ["Date", C.PH("date")],
        ["Project / Award", C.PH("project name and NTIA award number")],
        ["Requested by", C.PH("name / Party")],
        ["Affected route(s) / segment(s)", C.PH("route or segment IDs (see Exhibit A)")],
    ]
    C.add_table(doc, headers, ident, widths=[2.3, 4.0], font_size=10)

    C.section(doc, "1.1", "Description of Change")
    C.para(doc, C.PH("detailed description of the change in scope, materials, route, or method"))
    C.section(doc, "1.2", "Reason for Change")
    C.para(doc, C.PH("reason / justification (e.g., field condition, redesign, permitting, availability)"))

    C.article(doc, 2, "Impact Assessment")
    impact = [
        ["Cost impact", C.PH("$ increase / decrease; basis of cost")],
        ["Schedule impact", C.PH("days added/removed; affected milestones (Exhibit D)")],
        ["Effect on Reserved Tribal capacity", C.PH("none / describe (Exhibit C)")],
        ["Effect on asset ownership / demarcation", C.PH("none / describe (Exhibit B)")],
    ]
    C.add_table(doc, headers, impact, widths=[2.3, 4.0], font_size=10)

    C.article(doc, 3, "Grant-Compliance Review")
    comp = [
        ["BABA / Buy America impact", C.PH("none / requires re-certification — describe")],
        ["Procurement impact", C.PH("within existing procurement / new procurement required")],
        ["Environmental re-review (NEPA/NHPA)", C.PH("not triggered / re-review required")],
        ["Federal-interest / cost-allowability impact", C.PH("none / describe")],
        ["Budget / award modification required", C.PH("no / yes — describe")],
    ]
    C.add_table(doc, headers, comp, widths=[2.3, 4.0], font_size=10)
    C.flag_para(doc, C.FLAG_GRANT,
                "Any change touching BABA, procurement method, or environmental scope "
                "must be cleared by Grant Counsel before work proceeds; some changes "
                "require prior NTIA approval. See " + C.CITES["baba"] + " and " +
                C.CITES["procurement"] + ".")
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Confirm whether the change requires a formal award modification or "
                "prior written approval from the awarding agency.")

    C.article(doc, 4, "Approvals")
    C.para(doc, "This Change Order is not effective until signed by each of the "
                "following. Grant Counsel approval is required for any item flagged "
                "above as a grant-compliance impact.")
    appr = [
        ["RIVR Tech — Project Manager", "____________________  Date: __________"],
        ["Lumbee Tribe — Authorized Representative", "____________________  Date: __________"],
        ["Grant Counsel", "____________________  Date: __________"],
    ]
    C.add_table(doc, ["Approver", "Signature / Date"], appr,
                widths=[2.6, 3.7], font_size=10)

    return C.save(doc, OUT_DIR, "Exhibit_F_Change_Order_Form.docx")


# ===========================================================================
# EXHIBIT G — Network Acceptance Certificate  (DOCX)
# ===========================================================================
def exhibit_G():
    doc = C.new_doc()
    _cover(doc, "G", "NETWORK ACCEPTANCE CERTIFICATE",
           "Form of Acceptance — Places a Segment in Service")

    C.article(doc, 1, "Segment Identification")
    headers = ["Field", "Entry"]
    ident = [
        ["Acceptance Certificate No.", C.PH("AC-###")],
        ["Route / segment", C.PH("route ID and endpoints (Exhibit A)")],
        ["Strand assignment", C.PH("strands accepted (Exhibit C)")],
        ["Ownership / owner", C.PH("Lumbee Tribe / RIVR Tech / Joint (Exhibit B)")],
        ["Date of testing", C.PH("date")],
    ]
    C.add_table(doc, headers, ident, widths=[2.4, 3.9], font_size=10)

    C.article(doc, 2, "Test Results Summary")
    C.para(doc, "Testing was performed to the standards in Exhibit E "
                "(Acceptance Testing Standards).")
    results = [
        ["Bi-directional OTDR at 1310 nm / 1550 nm", C.PH("pass / fail summary")],
        ["Splice loss within threshold", C.PH("yes / no — worst-case value")],
        ["Connector loss within threshold", C.PH("yes / no — worst-case value")],
        ["Span/link loss within budget", C.PH("yes / no — margin")],
        ["Test documentation delivered", C.PH("yes / no")],
    ]
    C.add_table(doc, ["Test", "Result"], results, widths=[3.4, 2.9], font_size=10)

    C.article(doc, 3, "Punch List and Deliverables")
    deliv = [
        ["Punch-list status", C.PH("no open items / list attached with target dates")],
        ["As-built drawings delivered (Y/N)", C.PH("Y / N")],
        ["GIS data delivered (Y/N)", C.PH("Y / N")],
        ["Strand mapping updated (Exhibit C)", C.PH("Y / N")],
        ["Asset inventory updated (Exhibit K)", C.PH("Y / N")],
    ]
    C.add_table(doc, ["Item", "Status"], deliv, widths=[3.4, 2.9], font_size=10)

    C.article(doc, 4, "Placed-In-Service")
    C.para(doc, f"Date placed in service: {C.PH('in-service date')}.")
    C.flag_para(doc, C.FLAG_GRANT,
                "The date placed in service is relevant to the Federal Interest, "
                "depreciation, and the property records required under " +
                C.CITES["equipment"] + ". Confirm the in-service date is recorded in "
                "the Exhibit K asset inventory.")

    C.article(doc, 5, "Certification and Acceptance")
    C.para(doc, "RIVR Tech certifies that the segment identified above was constructed "
                "and tested in accordance with Exhibit E and is complete except for any "
                "punch-list items noted. The Lumbee Tribe accepts the segment subject to "
                "clearance of any open punch-list items.")
    appr = [
        ["RIVR Tech — certifying engineer/PM",
         C.PH("name / title") + "  ____________________  Date: ______"],
        ["Lumbee Tribe — authorized acceptance",
         C.PH("name / title") + "  ____________________  Date: ______"],
    ]
    C.add_table(doc, ["Party", "Signature / Date"], appr,
                widths=[2.6, 3.7], font_size=10)
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "Confirm that acceptance here does not waive warranty rights or "
                "punch-list obligations under the O&M / IRU agreements.")

    return C.save(doc, OUT_DIR, "Exhibit_G_Network_Acceptance_Certificate.docx")


# ===========================================================================
# EXHIBIT H — Maintenance Escalation List  (DOCX)
# ===========================================================================
def exhibit_H():
    doc = C.new_doc()
    _cover(doc, "H", "MAINTENANCE ESCALATION LIST",
           "Contact Tiers, Severity Thresholds, and After-Hours / Storm-Mode Contacts")

    sla = C.DEAL["sla"]
    C.article(doc, 1, "Network Operations Center")
    C.para(doc, f"The Network Operations Center (NOC) operates {sla['noc']} and is the "
                f"single point of contact for fault reporting and escalation.")
    C.add_table(doc, ["NOC function", "Contact"],
                [["NOC — trouble reporting (24x7)",
                  C.PH("phone / email / ticket portal")],
                 ["NOC ticketing / portal", C.PH("URL / instructions")]],
                widths=[2.6, 3.7], font_size=10)

    C.article(doc, 2, "Escalation Tiers")
    C.para(doc, "Contacts escalate in order. If a tier does not acknowledge or resolve "
                "within the threshold for the applicable severity, the next tier is engaged.")
    headers = ["Tier", "Role", "Name", "Phone", "Email", "Escalate after"]
    rows = [
        ["Tier 1", "NOC operator / dispatch", C.PH("name"), C.PH("phone"),
         C.PH("email"), "Per severity SLA (below)"],
        ["Tier 2", "Field technician / OSP", C.PH("name"), C.PH("phone"),
         C.PH("email"), "Missed dispatch window"],
        ["Tier 3", "Network engineering", C.PH("name"), C.PH("phone"),
         C.PH("email"), "Missed restore window"],
        ["Tier 4", "Operations management", C.PH("name"), C.PH("phone"),
         C.PH("email"), "Restore breach / major outage"],
        ["Lumbee Tribe liaison", "Tribal point of contact", C.PH("name"), C.PH("phone"),
         C.PH("email"), "Any P1, or public-safety impact"],
        ["Emergency", "24x7 emergency / on-call", C.PH("name"), C.PH("phone"),
         C.PH("email"), "Immediate for P1 / safety"],
    ]
    C.add_table(doc, headers, rows,
                widths=[0.9, 1.5, 1.0, 1.0, 1.1, 1.0], font_size=8)

    C.article(doc, 3, "Severity Thresholds (SLA)")
    C.para(doc, "Escalation timing is driven by incident severity as defined in the "
                "O&M / SLA agreement:")
    sev = [
        ["P1 — Critical (outage / public safety)",
         f"{sla['P1_response_min']} min", f"{sla['P1_dispatch_hr']} hr",
         f"{sla['P1_restore_hr']} hr"],
        ["P2 — Major (partial / degraded)",
         f"{sla['P2_response_min']} min", f"{sla['P2_dispatch_hr']} hr",
         f"{sla['P2_restore_hr']} hr"],
        ["P3 — Minor (single site / non-urgent)",
         f"{sla['P3_response_hr']} hr", f"{sla['P3_dispatch_hr']} hr",
         f"{sla['P3_restore_days']} days"],
        ["P4 — Informational / scheduled",
         f"{sla['P4_response_hr']} hr", "As scheduled",
         f"{sla['P4_restore_days']} days"],
    ]
    C.add_table(doc, ["Severity", "Response", "Dispatch", "Restore"], sev,
                widths=[2.9, 1.1, 1.1, 1.2], font_size=9)

    C.article(doc, 4, "After-Hours and Storm-Mode Contacts")
    C.section(doc, "4.1", "After-Hours",
              f"Outside business hours, all reporting routes through the 24x7 NOC, which "
              f"engages the on-call tiers above. After-hours on-call: "
              f"{C.PH('on-call rotation / phone')}.")
    C.section(doc, "4.2", "Storm Mode / Major Event",
              f"During declared storms or major events, storm-mode staffing and "
              f"prioritization apply, with public-safety and health-care circuits "
              f"restored first. Storm-mode command contact: {C.PH('name / phone / email')}. "
              f"Lumbee Tribe emergency-management coordination: {C.PH('EM contact')}.")
    C.flag_para(doc, C.FLAG_TECH,
                "All names, phone numbers, and email addresses to be supplied and kept "
                "current; distribute updates to the Lumbee Tribe liaison.")

    return C.save(doc, OUT_DIR, "Exhibit_H_Maintenance_Escalation_List.docx")


# ===========================================================================
# EXHIBIT I — Insurance Requirements  (DOCX)
# ===========================================================================
def exhibit_I():
    doc = C.new_doc()
    _cover(doc, "I", "INSURANCE REQUIREMENTS",
           "Minimum Coverages, Limits, and Endorsements")

    ins = C.DEAL["insurance"]
    C.article(doc, 1, "Required Coverages and Minimum Limits")
    C.para(doc, f"RIVR Tech shall maintain, at its expense, at least the following "
                f"coverages throughout the term and shall cause its contractors to carry "
                f"appropriate coverage. Consistent with {C.CITES['insurance']}, the "
                f"Tribal Assets shall be insured to protect the Federal Interest.")
    headers = ["Coverage", "Minimum Limit", "Notes"]
    rows = [
        ["Commercial General Liability (CGL)",
         f"{ins['cgl_occurrence']} per occurrence / {ins['cgl_aggregate']} aggregate",
         "Bodily injury, property damage, products/completed operations"],
        ["Automobile Liability",
         f"{ins['auto']} combined single limit",
         "Owned, hired, and non-owned autos"],
        ["Umbrella / Excess Liability",
         f"{ins['umbrella']}",
         "Excess of CGL, auto, and employers' liability"],
        ["Workers' Compensation",
         f"{ins['workers_comp']}",
         "As required by North Carolina law"],
        ["Employers' Liability",
         f"{ins['employers_liability']}",
         "Each accident / disease"],
        ["Professional / Technology E&O",
         f"{ins['professional_tech_eo']}",
         "Errors & omissions in design/engineering/operations"],
        ["Cyber / Network Security & Privacy",
         f"{ins['cyber']}",
         "Data breach, network security, privacy liability"],
        ["Property / Builder's Risk",
         f"{ins['property_builders_risk']}",
         "Covering the Tribal Assets during and after construction"],
        ["Contractor's Pollution Liability",
         f"{ins['pollution']}",
         "Environmental / pollution incidents during construction"],
    ]
    C.add_table(doc, headers, rows, widths=[2.1, 2.0, 2.2], font_size=9)
    C.flag_para(doc, C.FLAG_ATTORNEY,
                "All limits are placeholders for negotiation and must be confirmed "
                "against the funded application, lender/leasing requirements, the value "
                "of the Tribal Assets, and any NTIA award conditions.")

    C.article(doc, 2, "Endorsements and Conditions")
    for label, body in [
        ("Additional insured", f"The {C.TRIBE_FULL} (and, where required, its "
         "instrumentalities and the United States as its interest may appear) shall be "
         "named as additional insured on the CGL, auto, umbrella, and pollution policies."),
        ("Waiver of subrogation", "Each liability and property policy shall include a "
         "waiver of subrogation in favor of the Lumbee Tribe."),
        ("Primary and non-contributory", "RIVR Tech's coverage shall be primary and "
         "non-contributory with respect to any insurance maintained by the Lumbee Tribe."),
        ("Property coverage of Tribal Assets", f"Property / builder's-risk coverage "
         f"shall be written for the full replacement cost of the Tribal Assets to "
         f"protect the Federal Interest consistent with {C.CITES['insurance']}, with "
         f"the Lumbee Tribe as loss payee as its interest appears."),
        ("Certificates of insurance", f"RIVR Tech shall deliver certificates (and "
         f"endorsements on request) evidencing the required coverages before "
         f"commencing work and upon each renewal. Certificate holder: {C.PH('Lumbee Tribe notice address')}."),
        ("Notice of cancellation", "RIVR Tech shall provide the Lumbee Tribe at least thirty "
         "(30) days' written notice (ten (10) days for non-payment) of cancellation, "
         "non-renewal, or material reduction in coverage."),
        ("Insurer rating", f"Insurers shall carry an A.M. Best rating of at least "
         f"{C.PH('e.g., A- VII')} and be authorized to do business in North Carolina."),
    ]:
        C.section(doc, "", label)
        C.para(doc, body, indent=0.25)

    C.flag_para(doc, C.FLAG_GRANT,
                "Insurance of the Tribal Assets supports the property-trust relationship "
                "(" + C.CITES["trust"] + ") and the insurance requirement of " +
                C.CITES["insurance"] + ".")

    return C.save(doc, OUT_DIR, "Exhibit_I_Insurance_Requirements.docx")


# ===========================================================================
# EXHIBIT J — Monthly Performance Report  (XLSX)
# ===========================================================================
def exhibit_J():
    wb = Workbook()
    C.xl_instructions(wb, [
        "## Exhibit J — Monthly Performance Report",
        "Purpose: track monthly SLA performance against contractual targets and support "
        "FCC/NTIA performance reporting.",
        "",
        "## How to use",
        "• Targets (green) come from the O&M/SLA agreement and are fixed.",
        "• AMBER cells are inputs — enter the month's actuals.",
        "• BLUE Pass/Fail cells evaluate automatically. Availability, latency, loss, and "
        "jitter use higher/lower-is-better logic appropriate to each metric.",
        "",
        "## Status",
        "• " + C.DRAFT_STATUS,
    ])

    sla = C.DEAL["sla"]
    ws = wb.create_sheet("Performance")
    C.xl_title(ws, "EXHIBIT J — MONTHLY PERFORMANCE REPORT",
               subtitle=f"Reporting month: {C.PH('MM/YYYY')}", span=6)
    headers = ["Metric", "Target", "Actual (input)", "Pass/Fail (formula)",
               "Direction", "Notes"]
    hrow = 5
    C.xl_header_row(ws, hrow, headers)
    _widths(ws, [34, 16, 16, 20, 16, 30])

    def num(s):
        return float(str(s).replace("%", "").replace("ms", "").strip())

    # (label, target_value, direction, fmt, note)  direction: ">=" better or "<=" better
    metrics = [
        ("Network availability", num(sla["availability_target"]) / 100.0, ">=",
         C.FMT_PCT, "Uptime vs. 99.9% target"),
        ("Latency (round-trip)", sla["latency_ms"], "<=", C.FMT_NUM, "ms"),
        ("Packet loss", num(sla["packet_loss"]) / 100.0, "<=", C.FMT_PCT, ""),
        ("Jitter", sla["jitter_ms"], "<=", C.FMT_NUM, "ms"),
        ("P1 incidents — MTTR (hrs)", sla["P1_restore_hr"], "<=", C.FMT_NUM,
         "Mean time to restore vs. P1 target"),
        ("P2 incidents — MTTR (hrs)", sla["P2_restore_hr"], "<=", C.FMT_NUM, ""),
        ("P3 incidents — MTTR (days)", sla["P3_restore_days"], "<=", C.FMT_NUM, ""),
        ("P4 incidents — MTTR (days)", sla["P4_restore_days"], "<=", C.FMT_NUM, ""),
        ("Mean time to repair (all)", C.PH("target"), "<=", None,
         "Overall MTTR target — confirm"),
        ("Speed-test compliance (>= 100/20)", 1.0, ">=", C.FMT_PCT,
         "% of tests meeting the 100/20 floor"),
        ("Service credits owed", 0, "<=", C.FMT_USD,
         "Credits triggered by SLA breach"),
    ]
    # count-style rows (no simple target compare)
    counts = [
        ("P1 incident count", "P2 incident count", "P3 incident count",
         "P4 incident count", "Tickets opened", "Tickets closed", "Truck rolls"),
    ]

    first = hrow + 1
    r = first
    for label, target, direction, fmt, note in metrics:
        C.xl_cell(ws, r, 1, label, "text", wrap=True)
        if isinstance(target, str):  # placeholder target
            C.xl_cell(ws, r, 2, target, "input", align="center")
        else:
            C.xl_cell(ws, r, 2, target, "output", fmt=fmt, align="center")
        C.xl_cell(ws, r, 3, C.PH("actual"), "input", align="center")
        # pass/fail formula guarded for numeric actual
        if isinstance(target, str):
            pf = f'=IF(ISNUMBER(C{r}),"REVIEW vs target","ENTER ACTUAL")'
        else:
            op = ">=" if direction == ">=" else "<="
            pf = (f'=IF(ISNUMBER(C{r}),IF(C{r}{op}B{r},"PASS","FAIL"),'
                  f'"ENTER ACTUAL")')
        C.xl_cell(ws, r, 4, pf, "formula", align="center")
        C.xl_cell(ws, r, 5, "higher is better" if direction == ">=" else "lower is better",
                  "text", align="center")
        C.xl_cell(ws, r, 6, note, "text", wrap=True)
        r += 1

    # count metrics (tracked, not pass/fail)
    r += 1
    C.xl_cell(ws, r, 1, "Volume metrics (tracked)", "section")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    r += 1
    for label in counts[0]:
        C.xl_cell(ws, r, 1, label, "text")
        C.xl_cell(ws, r, 2, "—", "text", align="center")
        C.xl_cell(ws, r, 3, C.PH("count"), "input", align="center")
        C.xl_cell(ws, r, 4, "n/a", "text", align="center")
        C.xl_cell(ws, r, 5, "tracked", "text", align="center")
        C.xl_cell(ws, r, 6, "", "text")
        r += 1

    # overall SLA pass check
    r += 1
    C.xl_check(ws, r, 1,
               f'=IF(COUNTIF(D{first}:D{first+len(metrics)-1},"FAIL")=0,'
               f'IF(COUNTIF(D{first}:D{first+len(metrics)-1},"ENTER ACTUAL")>0,'
               f'"INCOMPLETE — enter actuals","PASS — all SLAs met"),'
               f'"FAIL — one or more SLAs breached")',
               "Overall SLA result for the month:")

    # FCC/NTIA reporting section
    r += 2
    C.xl_cell(ws, r, 1, "FCC / NTIA performance reporting", "section")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    r += 1
    fcc = [
        ("Locations served / passed (cumulative)", C.PH("count")),
        ("Subscribers connected (cumulative)", C.PH("count")),
        ("Speeds delivered (min tier)", C.SPEED_FLOOR + " floor"),
        ("Affordability / low-cost plan enrollment", C.PH("count")),
        ("Reporting period", C.PH("quarter / annual per award terms")),
        ("Data source / system of record", C.PH("OSS/BSS or reporting tool")),
    ]
    for label, val in fcc:
        C.xl_cell(ws, r, 1, label, "text", wrap=True)
        C.xl_cell(ws, r, 3, val, "input" if str(val).startswith("[■") else "text",
                  wrap=True)
        r += 1
    C.xl_cell(ws, r + 1, 1,
              "Note: performance reporting supports NTIA award conditions and, where "
              "applicable, FCC broadband data collection.", "text", wrap=True)
    ws.merge_cells(start_row=r + 1, start_column=1, end_row=r + 1, end_column=6)

    return C.xl_save(wb, OUT_DIR, "Exhibit_J_Monthly_Performance_Report.xlsx")


# ===========================================================================
# EXHIBIT K — Grant Asset Inventory  (XLSX)  — 2 CFR 200.313(d)
# ===========================================================================
def exhibit_K():
    wb = Workbook()
    C.xl_instructions(wb, [
        "## Exhibit K — Grant Asset Inventory",
        "Purpose: maintain the property records required for grant-funded equipment and "
        "the Tribal Assets.",
        "",
        "## Required record fields (2 CFR 200.313(d))",
        "• Description; serial/model number; source of funds (federal award number); "
        "who holds title; acquisition date and cost; federal share (%); location, use, "
        "and condition; ultimate disposition data (date of disposal, sale price, or "
        "method).",
        "",
        "## How to use",
        "• AMBER cells are inputs — one row per asset or asset group.",
        "• Federal Share (%) is an input; Federal Share ($) is a formula "
        "(= acquisition cost × federal share %).",
        "• Perform a physical inventory and reconcile to these records at least once "
        "every two (2) years (2 CFR 200.313(d)(2)).",
        "",
        "## Governing authority",
        "• " + C.CITES["equipment"],
        "• " + C.CITES["trust"],
        "",
        "## Status",
        "• " + C.DRAFT_STATUS,
    ])

    ws = wb.create_sheet("Asset Inventory")
    C.xl_title(ws, "EXHIBIT K — GRANT ASSET INVENTORY",
               subtitle="Property records per 2 CFR 200.313(d)", span=11)
    headers = ["Asset ID / Tag", "Description", "Serial / Model",
               "Source of Funds (Federal Award #)", "Acquisition Date",
               "Acquisition Cost", "Federal Share %", "Federal Share ($) (formula)",
               "Location", "Use / Condition", "Ultimate Disposition Data"]
    hrow = 5
    C.xl_header_row(ws, hrow, headers)
    _widths(ws, [14, 26, 16, 26, 14, 15, 12, 18, 18, 18, 26])

    first = hrow + 1
    for i in range(first, first + 8):
        C.xl_cell(ws, i, 1, C.PH("tag"), "input")
        C.xl_cell(ws, i, 2, C.PH("description"), "input", wrap=True)
        C.xl_cell(ws, i, 3, C.PH("serial / model"), "input", wrap=True)
        C.xl_cell(ws, i, 4, C.PH("NTIA award #"), "input", wrap=True)
        C.xl_cell(ws, i, 5, C.PH("date"), "input", align="center")
        C.xl_cell(ws, i, 6, C.PH("cost"), "input", fmt=C.FMT_USD, align="right")   # F
        C.xl_cell(ws, i, 7, C.PH("%"), "input", fmt=C.FMT_PCT, align="center")     # G
        C.xl_cell(ws, i, 8, f"=IF(AND(ISNUMBER(F{i}),ISNUMBER(G{i})),F{i}*G{i},"
                            f'"ENTER COST & SHARE")', "formula", fmt=C.FMT_USD,
                  align="right")
        C.xl_cell(ws, i, 9, C.PH("location"), "input", wrap=True)
        C.xl_cell(ws, i, 10, C.PH("use / condition"), "input", wrap=True)
        C.xl_cell(ws, i, 11, C.PH("disposition (date / sale price / method)"), "input",
                  wrap=True)
    last = first + 7

    r = last + 2
    C.xl_cell(ws, r, 1, "Rollup & reconciliation", "section")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=11)
    r += 1
    C.xl_cell(ws, r, 5, "Total acquisition cost:", "text", bold=True, align="right")
    C.xl_cell(ws, r, 6, f"=IF(COUNT(F{first}:F{last})=0,\"ENTER COSTS\","
                        f"SUM(F{first}:F{last}))", "formula", fmt=C.FMT_USD,
              align="right")
    C.xl_cell(ws, r, 7, "Total federal share:", "text", bold=True, align="right")
    C.xl_cell(ws, r, 8, f"=IF(COUNT(F{first}:F{last})=0,\"—\","
                        f"SUMPRODUCT(F{first}:F{last},G{first}:G{last}))",
              "formula", fmt=C.FMT_USD, align="right")
    r += 2
    C.xl_cell(ws, r, 1,
              "Physical-inventory reconciliation: a physical inventory of the assets "
              "above must be taken and reconciled to these records at least once every "
              "two (2) years per 2 CFR 200.313(d)(2). Last reconciliation date: "
              + "________.  Next due: ________.", "text", wrap=True)
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=11)
    ws.row_dimensions[r].height = 45
    r += 1
    C.xl_cell(ws, r, 1,
              "Property-trust note: grant-funded assets are held in trust for the "
              "beneficiaries of the project per " + C.CITES["trust"] +
              " and remain subject to the Federal Interest until disposition under " +
              C.CITES["equipment"] + ".", "text", wrap=True)
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=11)
    ws.row_dimensions[r].height = 45

    return C.xl_save(wb, OUT_DIR, "Exhibit_K_Grant_Asset_Inventory.xlsx")


# ===========================================================================
# EXHIBIT L — Responsibility RACI Matrix  (XLSX)
# ===========================================================================
def exhibit_L():
    wb = Workbook()
    C.xl_instructions(wb, [
        "## Exhibit L — Responsibility (RACI) Matrix",
        "Purpose: assign Responsible / Accountable / Consulted / Informed for each "
        "activity across the Lumbee Tribe, RIVR Tech, Grant Counsel, and NTIA.",
        "",
        "## RACI legend",
        "• R = Responsible (does the work)",
        "• A = Accountable (owns the outcome — exactly one per row)",
        "• C = Consulted (two-way input)",
        "• I = Informed (kept up to date)",
        "",
        "## How to use",
        "• Each activity cell has a dropdown limited to R, A, C, or I.",
        "• Confirm exactly one 'A' per row.",
        "",
        "## Status",
        "• " + C.DRAFT_STATUS,
    ])

    ws = wb.create_sheet("RACI")
    C.xl_title(ws, "EXHIBIT L — RESPONSIBILITY (RACI) MATRIX",
               subtitle="R = Responsible · A = Accountable · C = Consulted · I = Informed",
               span=5)
    parties = ["Lumbee Tribe", "RIVR Tech", "Grant Counsel", "NTIA"]
    headers = ["Activity"] + parties
    hrow = 5
    C.xl_header_row(ws, hrow, headers)
    _widths(ws, [40, 14, 14, 16, 12])

    # (activity, Lumbee Tribe, RIVR, Counsel, NTIA) — sensible defaults; user adjusts
    activities = [
        ("Grant application & award management", "A", "C", "C", "I"),
        ("Network design / engineering", "C", "A", "I", "I"),
        ("Environmental review (NEPA/NHPA)", "A", "C", "C", "A"),
        ("Permitting & easements", "C", "A", "C", "I"),
        ("Procurement (incl. BABA / §889)", "A", "R", "C", "I"),
        ("Construction", "I", "A", "I", "I"),
        ("Testing & acceptance", "A", "R", "I", "I"),
        ("Asset & property records (2 CFR 200.313)", "A", "C", "C", "I"),
        ("Network operations", "I", "A", "I", "I"),
        ("Billing & collections", "I", "A", "I", "I"),
        ("Customer service", "C", "A", "I", "I"),
        ("Marketing & outreach", "C", "A", "I", "I"),
        ("Regulatory compliance (FCC/NTIA)", "A", "R", "C", "I"),
        ("Grant reporting", "A", "C", "C", "I"),
        ("Audit (single audit / program)", "A", "C", "C", "I"),
        ("Maintenance & repair", "I", "A", "I", "I"),
        ("Capital replacement / renewal", "A", "C", "C", "I"),
        ("Cybersecurity", "C", "A", "C", "I"),
        ("Step-in / continuity of essential services", "A", "R", "C", "I"),
        ("Asset disposition (2 CFR 200.313)", "A", "C", "C", "A"),
    ]
    dv = DataValidation(type="list", formula1='"R,A,C,I"', allow_blank=True,
                        showErrorMessage=True)
    dv.error = "Enter one of R, A, C, or I."
    dv.errorTitle = "RACI value"
    ws.add_data_validation(dv)

    first = hrow + 1
    r = first
    for act, t, o, gc, nt in activities:
        C.xl_cell(ws, r, 1, act, "text", wrap=True)
        for ci, val in enumerate([t, o, gc, nt], start=2):
            C.xl_cell(ws, r, ci, val, "input", align="center")
            dv.add(ws.cell(row=r, column=ci))
        r += 1
    last = r - 1

    # accountability check: exactly one A per row
    r += 1
    C.xl_cell(ws, r, 1, "Accountability checks (exactly one 'A' per row)", "section")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5)
    r += 1
    for rr in range(first, last + 1):
        C.xl_check(ws, r, 1,
                   f'=IF(COUNTIF(B{rr}:E{rr},"A")=1,"OK",'
                   f'"CHECK — need exactly one A")',
                   f"Row {rr}:")
        r += 1

    return C.xl_save(wb, OUT_DIR, "Exhibit_L_Responsibility_RACI_Matrix.xlsx")


# ===========================================================================
# EXHIBIT M — Service Area and Pricing Schedule  (XLSX)
# ===========================================================================
def exhibit_M():
    wb = Workbook()
    C.xl_instructions(wb, [
        "## Exhibit M — Service Area and Pricing Schedule",
        "Purpose: define the retail service tiers and pricing offered across the "
        "Service Territory, including the required low-cost / affordable option.",
        "",
        "## TBCP affordability requirement",
        "• A low-cost / affordable broadband option meeting at least the 100/20 Mbps "
        "floor must be offered; rates are subject to the affordability obligations of "
        "the award.",
        "",
        "## How to use",
        "• AMBER cells are inputs — enter speeds, prices, and install fees.",
        "• All pricing is a BUSINESS DECISION and subject to legal/grant review.",
        "",
        "## Status",
        "• " + C.DRAFT_STATUS,
    ])

    ws = wb.create_sheet("Pricing")
    C.xl_title(ws, "EXHIBIT M — SERVICE AREA AND PRICING SCHEDULE",
               subtitle="Retail tiers across the Service Territory (southeastern NC)",
               span=6)
    headers = ["Tier", "Speed (down/up)", "Monthly price", "Install fee",
               "Category", "Notes"]
    hrow = 5
    C.xl_header_row(ws, hrow, headers)
    _widths(ws, [26, 18, 16, 14, 16, 34])

    tiers = [
        ("Low-cost / Affordable (TBCP)", C.SPEED_FLOOR, C.PH("$/mo"),
         C.PH("$ / waived"), "Residential",
         "REQUIRED affordable option — subject to affordability obligations"),
        ("Residential Standard", C.PH("e.g., 300/300"), C.PH("$/mo"),
         C.PH("$"), "Residential", C.PH("promo / term")),
        ("Residential Gig", C.PH("e.g., 1000/1000"), C.PH("$/mo"),
         C.PH("$"), "Residential", ""),
        ("Business Basic", C.PH("symmetrical"), C.PH("$/mo"),
         C.PH("$"), "Business", C.PH("SLA tier")),
        ("Business Pro", C.PH("symmetrical"), C.PH("$/mo"),
         C.PH("$"), "Business", C.PH("SLA tier")),
        ("Enterprise / Dedicated", C.PH("custom"), C.PH("$/mo (ICB)"),
         C.PH("$ (ICB)"), "Enterprise", "Individually priced; dedicated access"),
        ("Voice (VoIP)", "N/A", C.PH("$/mo per line"), C.PH("$"),
         "Add-on", C.PH("911 / regulatory fees apply")),
        ("Anchor institution", C.PH("per tier"), C.PH("$ / per agreement"),
         C.PH("$"), "Anchor", "Per Exhibit A anchor list"),
    ]
    first = hrow + 1
    r = first
    for name, spd, price, inst, cat, note in tiers:
        C.xl_cell(ws, r, 1, name, "text", bold=(r == first), wrap=True)
        C.xl_cell(ws, r, 2, spd, "input" if str(spd).startswith("[■") else "text",
                  align="center")
        C.xl_cell(ws, r, 3, price, "input", align="center")
        C.xl_cell(ws, r, 4, inst, "input", align="center")
        C.xl_cell(ws, r, 5, cat, "text", align="center")
        C.xl_cell(ws, r, 6, note, "input" if str(note).startswith("[■") else "text",
                  wrap=True)
        r += 1

    r += 1
    C.xl_cell(ws, r, 1,
              "[BUSINESS DECISION REQUIRED] All tiers, speeds, and prices are "
              "placeholders and constitute a business decision requiring legal and "
              "grant review; the low-cost 100/20 option and rates remain subject to "
              "the affordability obligations of the TBCP award.", "text", wrap=True)
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    ws.row_dimensions[r].height = 45
    r += 1
    C.xl_cell(ws, r, 1,
              "Check: a low-cost option at or above the " + C.SPEED_FLOOR +
              " floor is listed as the first tier above.", "text", wrap=True)
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)

    return C.xl_save(wb, OUT_DIR, "Exhibit_M_Service_Area_and_Pricing_Schedule.xlsx")


# ===========================================================================
# EXHIBIT N — Form of Asset Addition Certificate  (DOCX)
# ===========================================================================
def exhibit_N():
    doc = C.new_doc()
    _cover(doc, "N", "FORM OF ASSET ADDITION CERTIFICATE",
           "Adds Newly Constructed or Acquired Assets to the Tribal Asset Inventory and IRU")

    C.article(doc, 1, "Purpose")
    C.para(doc, f"This Asset Addition Certificate adds the asset(s) described below to "
                f"the {C.TRIBAL_ASSETS} inventory, determines the Federal Interest, and, "
                f"where applicable, brings the asset(s) under the {C.IRU_TERM_DEFINED}. "
                f"Upon execution, the referenced exhibits are updated.")

    C.article(doc, 2, "Asset Description")
    headers = ["Field", "Entry"]
    rows = [
        ["Certificate No.", C.PH("AA-###")],
        ["Date", C.PH("date")],
        ["Asset description", C.PH("description of newly constructed/acquired asset(s)")],
        ["Route / segment / location", C.PH("route ID, segment, or site (Exhibit A)")],
        ["Serial / model (if equipment)", C.PH("serial / model")],
        ["Funding source", C.PH("TBCP award # / other federal / non-federal")],
        ["Acquisition / construction cost", C.PH("$ cost")],
        ["Federal share %", C.PH("%")],
        ["Date placed in service", C.PH("in-service date")],
    ]
    C.add_table(doc, headers, rows, widths=[2.4, 3.9], font_size=10)

    C.article(doc, 3, "Federal-Interest Determination")
    C.para(doc, f"Federal Interest: {C.PH('YES (grant-funded Tribal Asset) / NO (RIVR Tech asset) / partial — describe')}.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Grant-funded additions carry a Federal Interest and become Tribal "
                "Assets subject to " + C.CITES["equipment"] + " and " +
                C.CITES["trust"] + ". Confirm cost allowability and BABA compliance.")

    C.article(doc, 4, "Exhibit Updates")
    C.para(doc, "Upon execution, the following exhibits are updated to reflect this addition:")
    for item in [
        "Exhibit B (Asset Ownership and Demarcation Matrix) — new asset row and demarcation",
        "Exhibit C (Fiber Allocation and Reserved Capacity) — strand allocation, if applicable",
        "Exhibit K (Grant Asset Inventory) — property record per 2 CFR 200.313(d)",
    ]:
        C.bullet(doc, item)
    updates = [
        ["Exhibit B updated (Y/N)", C.PH("Y / N")],
        ["Exhibit C updated (Y/N)", C.PH("Y / N / N-A")],
        ["Exhibit K updated (Y/N)", C.PH("Y / N")],
        ["Brought under IRU (Y/N)", C.PH("Y / N — reference IRU Route Order, Exhibit O")],
    ]
    C.add_table(doc, ["Item", "Status"], updates, widths=[3.2, 3.1], font_size=10)

    C.article(doc, 5, "Approvals")
    appr = [
        ["Lumbee Tribe — authorized representative",
         C.PH("name / title") + "  ____________________  Date: ______"],
        ["RIVR Tech — authorized representative",
         C.PH("name / title") + "  ____________________  Date: ______"],
        ["Grant Counsel (federal-interest / compliance)",
         C.PH("name / title") + "  ____________________  Date: ______"],
    ]
    C.add_table(doc, ["Approver", "Signature / Date"], appr,
                widths=[2.9, 3.4], font_size=10)

    return C.save(doc, OUT_DIR, "Exhibit_N_Form_of_Asset_Addition_Certificate.docx")


# ===========================================================================
# EXHIBIT O — Form of IRU Route Order  (DOCX)
# ===========================================================================
def exhibit_O():
    doc = C.new_doc()
    _cover(doc, "O", "FORM OF IRU ROUTE ORDER",
           "Places a Specific Route or Segment Under the IRU")

    C.article(doc, 1, "Route Order")
    C.para(doc, f"This IRU Route Order is issued under, and incorporates by reference, "
                f"the Indefeasible Right of Use Agreement (Document 02.02) between the "
                f"{C.TRIBE_FULL} and {C.OPERATOR_FULL}. It places the route or segment "
                f"described below under the {C.IRU_TERM_DEFINED} for the term stated. In "
                f"the event of conflict, the IRU Agreement (02.02) controls.")

    C.article(doc, 2, "Route Identification")
    headers = ["Field", "Entry"]
    rows = [
        ["Route Order No.", C.PH("RO-###")],
        ["Order date", C.PH("date")],
        ["Route ID / segment", C.PH("route ID and endpoints (Exhibit A)")],
        ["Strands granted under IRU", C.PH("strand count / IDs (Exhibit C)")],
        ["Approx. route mileage", C.PH("miles")],
        ["Acceptance reference", C.PH("Acceptance Certificate No. (Exhibit G)")],
    ]
    C.add_table(doc, headers, rows, widths=[2.4, 3.9], font_size=10)

    C.article(doc, 3, "Term")
    C.para(doc, f"Term commencement date: {C.PH('commencement date (typically the date placed in service)')}. "
                f"IRU term: {C.PH('term in years')} "
                f"(recommended {C.IRU_TERM_RECOMMENDED} years; options {', '.join(str(t) for t in C.IRU_TERMS_YEARS)} years), "
                f"consistent with the IRU Agreement (02.02) and its renewal provisions "
                f"({C.DEAL['iru_renewal']}).")
    C.flag_para(doc, C.FLAG_BUSINESS,
                "Confirm the IRU term for this route (recommended 30 years) and any "
                "route-specific renewal or early-termination terms.")

    C.article(doc, 4, "Consideration Allocation")
    C.para(doc, f"Consideration allocated to this route: "
                f"{C.PH('allocation of IRU consideration / operating payment to this route')}. "
                f"The prepaid IRU consideration and ongoing obligations are as set forth "
                f"in the IRU Agreement (02.02): {C.DEAL['iru_prepaid_consideration']}.")
    C.flag_para(doc, C.FLAG_BUSINESS,
                "Route-level consideration allocation is a business decision; confirm "
                "against the term sheet and financial model.")
    C.flag_para(doc, C.FLAG_GRANT,
                "Confirm that the IRU grant and any consideration are consistent with "
                "the Federal Interest in the grant-funded Tribal Assets and do not "
                "constitute a prohibited encumbrance or disposition under " +
                C.CITES["real_property"] + " / " + C.CITES["equipment"] + ".")

    C.article(doc, 5, "Cross-References and Execution")
    C.para(doc, "This Route Order is subject to the IRU Agreement (02.02), the asset "
                "classification in Exhibit B, the strand allocation in Exhibit C, and "
                "the acceptance in Exhibit G.")
    appr = [
        ["Lumbee Tribe — authorized representative",
         C.PH("name / title") + "  ____________________  Date: ______"],
        ["RIVR Tech — authorized representative",
         C.PH("name / title") + "  ____________________  Date: ______"],
    ]
    C.add_table(doc, ["Party", "Signature / Date"], appr,
                widths=[2.9, 3.4], font_size=10)

    return C.save(doc, OUT_DIR, "Exhibit_O_Form_of_IRU_Route_Order.docx")


# ===========================================================================
# MAIN
# ===========================================================================
BUILDERS = [
    exhibit_A, exhibit_B, exhibit_C, exhibit_D, exhibit_E,
    exhibit_F, exhibit_G, exhibit_H, exhibit_I, exhibit_J,
    exhibit_K, exhibit_L, exhibit_M, exhibit_N, exhibit_O,
]


def main():
    paths = []
    for fn in BUILDERS:
        p = fn()
        paths.append(p)
        print(f"  built  {fn.__name__:12s} -> {p}")
    print("\nAll", len(paths), "exhibits built.")
    return paths


if __name__ == "__main__":
    main()
