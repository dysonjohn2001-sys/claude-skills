"""
Shared design system for the ISP COO Executive Management System workbook.
Executive-friendly, board-ready palette and reusable style helpers.
"""
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, NamedStyle
from openpyxl.utils import get_column_letter

# ---------------------------------------------------------------------------
# Brand palette (deep navy + slate, with RYG status colors)
# ---------------------------------------------------------------------------
NAVY       = "1F2A44"   # primary header background
NAVY_DK    = "16203A"
SLATE      = "33415C"   # section sub-headers
STEEL       = "5B6B86"
LIGHT_BG    = "F4F6FA"   # page background-ish fills
CARD_BG     = "FFFFFF"
CARD_LABEL  = "64748B"
ACCENT      = "0E7C86"   # teal accent
ACCENT_2    = "2563EB"   # blue accent
WHITE       = "FFFFFF"
GRID        = "D7DEE8"
TABLE_HDR   = "1F2A44"

# Status (Red / Yellow / Green) — fills + fonts
GREEN_BG   = "C6EFCE"; GREEN_TX = "0B6B2F"
YELLOW_BG  = "FFF2CC"; YELLOW_TX = "9C6500"
RED_BG     = "F8CBCB"; RED_TX   = "9C1B1B"
GREEN_SOLID = "2E9E5B"
YELLOW_SOLID = "E8B800"
RED_SOLID  = "D14343"

# ---------------------------------------------------------------------------
# Reusable fills / fonts / borders
# ---------------------------------------------------------------------------
def fill(color):
    return PatternFill("solid", fgColor=color)

thin = Side(style="thin", color=GRID)
medium = Side(style="medium", color=NAVY)
box_thin = Border(left=thin, right=thin, top=thin, bottom=thin)

F_TITLE   = Font(name="Calibri", size=20, bold=True, color=WHITE)
F_SUBTITLE = Font(name="Calibri", size=11, color="C7D0E0")
F_SECTION = Font(name="Calibri", size=13, bold=True, color=WHITE)
F_KPI_LABEL = Font(name="Calibri", size=9, bold=True, color=CARD_LABEL)
F_KPI_VALUE = Font(name="Calibri", size=18, bold=True, color=NAVY)
F_KPI_VALUE_SM = Font(name="Calibri", size=14, bold=True, color=NAVY)
F_KPI_SUB = Font(name="Calibri", size=8, color=STEEL)
F_HDR     = Font(name="Calibri", size=10, bold=True, color=WHITE)
F_BODY    = Font(name="Calibri", size=10, color="1A2233")
F_BODY_B  = Font(name="Calibri", size=10, bold=True, color="1A2233")
F_SMALL   = Font(name="Calibri", size=9, color=STEEL)
F_NOTE    = Font(name="Calibri", size=9, italic=True, color=STEEL)

CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT   = Alignment(horizontal="left", vertical="center", wrap_text=True)
LEFT_TOP = Alignment(horizontal="left", vertical="top", wrap_text=True)
RIGHT  = Alignment(horizontal="right", vertical="center")


def page_setup(ws, tab_color=NAVY, hide_grid=True, zoom=100):
    ws.sheet_view.showGridLines = not hide_grid
    ws.sheet_properties.tabColor = tab_color
    ws.sheet_view.zoomScale = zoom


def title_band(ws, title, subtitle, last_col="N", row=1):
    """Full-width navy title band with title + subtitle."""
    ws.merge_cells(f"A{row}:{last_col}{row+1}")
    c = ws[f"A{row}"]
    c.value = title
    c.font = F_TITLE
    c.fill = fill(NAVY)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[row].height = 30
    ws.row_dimensions[row+1].height = 16
    sub = ws.cell(row=row+1, column=1)
    # subtitle sits in merged band; set via a second merged row band below
    # Use a thin band for subtitle
    ws.merge_cells(f"A{row+2}:{last_col}{row+2}")
    s = ws[f"A{row+2}"]
    s.value = subtitle
    s.font = F_SUBTITLE
    s.fill = fill(SLATE)
    s.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[row+2].height = 18
    return row + 3  # next free row


def section_header(ws, row, text, first_col=1, last_col=14, color=SLATE):
    last = get_column_letter(last_col)
    first = get_column_letter(first_col)
    ws.merge_cells(f"{first}{row}:{last}{row}")
    c = ws.cell(row=row, column=first_col)
    c.value = text
    c.font = F_SECTION
    c.fill = fill(color)
    c.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[row].height = 22
    return row + 1


def kpi_card(ws, top_row, col, label, value, sub=None, value_font=None,
             number_format=None, health_cell=False):
    """
    Render a 1-column-wide x 3-row KPI card starting at (top_row, col).
    Returns nothing; caller positions cards on a grid.
    Layout:
       row0: label
       row1: big value
       row2: sub / health
    """
    letter = get_column_letter(col)
    # card border box across 3 rows
    for r in range(top_row, top_row + 3):
        cell = ws.cell(row=r, column=col)
        cell.fill = fill(CARD_BG)
        cell.border = box_thin
    lab = ws.cell(row=top_row, column=col, value=label)
    lab.font = F_KPI_LABEL
    lab.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    val = ws.cell(row=top_row + 1, column=col, value=value)
    val.font = value_font or F_KPI_VALUE
    val.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    if number_format:
        val.number_format = number_format
    sb = ws.cell(row=top_row + 2, column=col, value=sub if sub is not None else "")
    sb.font = F_KPI_SUB
    sb.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    return val, sb


def style_table_header(ws, row, first_col, last_col):
    for col in range(first_col, last_col + 1):
        c = ws.cell(row=row, column=col)
        c.font = F_HDR
        c.fill = fill(TABLE_HDR)
        c.alignment = CENTER
        c.border = box_thin


def write_row(ws, row, start_col, values, font=None, fmts=None, aligns=None,
              border=True, fills=None):
    for i, v in enumerate(values):
        c = ws.cell(row=row, column=start_col + i, value=v)
        c.font = font or F_BODY
        if border:
            c.border = box_thin
        if fmts and i < len(fmts) and fmts[i]:
            c.number_format = fmts[i]
        if aligns and i < len(aligns) and aligns[i]:
            c.alignment = aligns[i]
        else:
            c.alignment = LEFT
        if fills and i < len(fills) and fills[i]:
            c.fill = fill(fills[i])
    return row + 1


def set_widths(ws, widths: dict):
    for col, w in widths.items():
        ws.column_dimensions[col].width = w
