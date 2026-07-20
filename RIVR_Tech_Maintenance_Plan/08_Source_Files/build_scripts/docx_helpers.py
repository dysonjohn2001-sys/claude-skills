# -*- coding: utf-8 -*-
"""Shared python-docx helpers for consistent RIVR Tech formatting."""
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import rivr_content as C

BRAND = C.BRAND


def _rgb(hexstr):
    return RGBColor.from_string(hexstr)


def new_doc():
    doc = Document()
    # Base font
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10.5)
    style.paragraph_format.space_after = Pt(6)
    style.paragraph_format.line_spacing = 1.12
    # Margins
    for section in doc.sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)
    # Heading styles
    for lvl, size, color, bold in [(1, 16, BRAND["primary"], True),
                                    (2, 13, BRAND["secondary"], True),
                                    (3, 11.5, BRAND["dark"], True)]:
        h = doc.styles[f"Heading {lvl}"]
        h.font.name = "Calibri"
        h.font.size = Pt(size)
        h.font.color.rgb = _rgb(color)
        h.font.bold = bold
        h.paragraph_format.space_before = Pt(12 if lvl == 1 else 9)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
    return doc


def set_cell_bg(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def _set_cell_margins(cell, top=40, bottom=40, left=80, right=80):
    tcPr = cell._tc.get_or_add_tcPr()
    m = OxmlElement("w:tcMar")
    for name, val in (("top", top), ("bottom", bottom), ("start", left), ("end", right)):
        node = OxmlElement(f"w:{name}")
        node.set(qn("w:w"), str(val))
        node.set(qn("w:type"), "dxa")
        m.append(node)
    tcPr.append(m)


def cover_page(doc, title, subtitle, doc_type="", extra_lines=None):
    section = doc.sections[0]
    # Top color band
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(60)
    run = p.add_run(C.COMPANY_SHORT.upper())
    run.font.size = Pt(30)
    run.font.bold = True
    run.font.color.rgb = _rgb(BRAND["primary"])
    p2 = doc.add_paragraph()
    r2 = p2.add_run(C.COMPANY_LEGAL)
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = _rgb(BRAND["gray"])
    r2.italic = True

    # rule
    _hr(doc, BRAND["secondary"])

    pt = doc.add_paragraph()
    pt.paragraph_format.space_before = Pt(40)
    rt = pt.add_run(title)
    rt.font.size = Pt(24)
    rt.font.bold = True
    rt.font.color.rgb = _rgb(BRAND["dark"])

    if subtitle:
        ps = doc.add_paragraph()
        rs = ps.add_run(subtitle)
        rs.font.size = Pt(13)
        rs.font.color.rgb = _rgb(BRAND["secondary"])

    if doc_type:
        pd = doc.add_paragraph()
        rd = pd.add_run(doc_type)
        rd.font.size = Pt(11)
        rd.font.color.rgb = _rgb(BRAND["gray"])

    # Meta block near bottom
    doc.add_paragraph().paragraph_format.space_before = Pt(120)
    meta = [
        ("Document Version", C.DOC_VERSION),
        ("Date", C.DOC_DATE),
        ("Effective Date", C.EFFECTIVE_DATE_PLACEHOLDER),
        ("Prepared By", C.PREPARED_BY),
        ("Region", f"Broadband services in {C.REGION}"),
    ]
    if extra_lines:
        meta.extend(extra_lines)
    t = doc.add_table(rows=0, cols=2)
    t.allow_autofit = True
    for k, v in meta:
        row = t.add_row().cells
        rk = row[0].paragraphs[0].add_run(k)
        rk.font.bold = True
        rk.font.size = Pt(9.5)
        rk.font.color.rgb = _rgb(BRAND["primary"])
        rv = row[1].paragraphs[0].add_run(v)
        rv.font.size = Pt(9.5)
        row[0].width = Inches(1.8)
        row[1].width = Inches(4.7)

    # Confidential / not legal advice notice
    doc.add_paragraph()
    note = doc.add_paragraph()
    rn = note.add_run("INTERNAL DRAFT FOR EXECUTIVE REVIEW — NOT LEGAL ADVICE. "
                      "Contains recommendations and labeled assumptions requiring "
                      "legal, regulatory, accounting, and insurance review before adoption.")
    rn.font.size = Pt(8.5)
    rn.font.color.rgb = _rgb(BRAND["warn"])
    rn.italic = True
    doc.add_page_break()


def _hr(doc, color=None):
    color = color or BRAND["secondary"]
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "18")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), color)
    pbdr.append(bottom)
    pPr.append(pbdr)
    return p


def add_footer(doc, doc_title):
    section = doc.sections[0]
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.text = ""
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    # left: title, right: page number
    run = p.add_run(f"{C.COMPANY_SHORT}  |  {doc_title}  |  {C.DOC_VERSION}  |  Page ")
    run.font.size = Pt(8)
    run.font.color.rgb = _rgb(BRAND["gray"])
    _add_page_field(p)
    run2 = p.add_run(" of ")
    run2.font.size = Pt(8)
    run2.font.color.rgb = _rgb(BRAND["gray"])
    _add_pages_field(p)


def _add_field(paragraph, instr):
    run = paragraph.add_run()
    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")
    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = instr
    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "end")
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run.font.size = Pt(8)
    run.font.color.rgb = _rgb(BRAND["gray"])


def _add_page_field(p):
    _add_field(p, "PAGE")


def _add_pages_field(p):
    _add_field(p, "NUMPAGES")


def h1(doc, text):
    return doc.add_heading(text, level=1)


def h2(doc, text):
    return doc.add_heading(text, level=2)


def h3(doc, text):
    return doc.add_heading(text, level=3)


def para(doc, text, bold=False, italic=False, size=10.5, color=None, space_after=6):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.font.bold = bold
    r.font.italic = italic
    r.font.size = Pt(size)
    if color:
        r.font.color.rgb = _rgb(color)
    p.paragraph_format.space_after = Pt(space_after)
    return p


def bullet(doc, text, level=0, bold_lead=None):
    p = doc.add_paragraph(style="List Bullet" if level == 0 else "List Bullet 2")
    if bold_lead:
        r = p.add_run(bold_lead)
        r.font.bold = True
        r.font.size = Pt(10.5)
        r2 = p.add_run(text)
        r2.font.size = Pt(10.5)
    else:
        r = p.add_run(text)
        r.font.size = Pt(10.5)
    return p


def numbered(doc, text):
    p = doc.add_paragraph(style="List Number")
    r = p.add_run(text)
    r.font.size = Pt(10.5)
    return p


def callout(doc, label, text, kind="assumption"):
    """Colored single-cell box. kind: assumption, legal, recommendation, decision, warning."""
    colors = {
        "assumption": (BRAND["yellow"], "ASSUMPTION"),
        "legal": (BRAND["warn"], "LEGAL / REGULATORY REVIEW"),
        "recommendation": (BRAND["accent"], "RECOMMENDATION"),
        "decision": (BRAND["primary"], "EXECUTIVE DECISION"),
        "warning": (BRAND["warn"], "REVIEW REQUIRED"),
        "policy": (BRAND["secondary"], "ESTABLISHED POLICY (PROPOSED)"),
    }
    color, default_label = colors.get(kind, (BRAND["gray"], "NOTE"))
    label = label or default_label
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.rows[0].cells[0]
    set_cell_bg(cell, BRAND["light"])
    _set_cell_margins(cell, 80, 80, 120, 120)
    _left_border_accent(cell, color)
    pl = cell.paragraphs[0]
    rl = pl.add_run(label + "  ")
    rl.font.bold = True
    rl.font.size = Pt(9)
    rl.font.color.rgb = _rgb(color)
    rt = pl.add_run(text)
    rt.font.size = Pt(9.5)
    rt.font.color.rgb = _rgb(BRAND["dark"])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def _left_border_accent(cell, color):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "24")
    left.set(qn("w:space"), "0")
    left.set(qn("w:color"), color)
    borders.append(left)
    tcPr.append(borders)


def table(doc, headers, rows, col_widths=None, header_bg=None, font_size=9,
          zebra=True, first_col_bold=False):
    header_bg = header_bg or BRAND["primary"]
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.allow_autofit = False
    # header
    hdr = t.rows[0].cells
    for i, htext in enumerate(headers):
        set_cell_bg(hdr[i], header_bg)
        _set_cell_margins(hdr[i])
        p = hdr[i].paragraphs[0]
        r = p.add_run(str(htext))
        r.font.bold = True
        r.font.size = Pt(font_size)
        r.font.color.rgb = _rgb(BRAND["white"])
    # body
    for ridx, row in enumerate(rows):
        cells = t.add_row().cells
        for i, val in enumerate(row):
            _set_cell_margins(cells[i])
            if zebra and ridx % 2 == 1:
                set_cell_bg(cells[i], BRAND["light"])
            p = cells[i].paragraphs[0]
            r = p.add_run("" if val is None else str(val))
            r.font.size = Pt(font_size)
            if first_col_bold and i == 0:
                r.font.bold = True
                r.font.color.rgb = _rgb(BRAND["primary"])
    if col_widths:
        for i, w in enumerate(col_widths):
            for row in t.rows:
                row.cells[i].width = Inches(w)
    return t


def toc_field(doc):
    para(doc, "Table of Contents", bold=True, size=13, color=BRAND["primary"])
    p = doc.add_paragraph()
    run = p.add_run()
    fldChar = OxmlElement("w:fldChar")
    fldChar.set(qn("w:fldCharType"), "begin")
    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = 'TOC \\o "1-3" \\h \\z \\u'
    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "separate")
    t = OxmlElement("w:t")
    t.text = "Right-click and choose 'Update Field' to build the table of contents."
    fldChar3 = OxmlElement("w:fldChar")
    fldChar3.set(qn("w:fldCharType"), "end")
    run._r.append(fldChar)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(t)
    run._r.append(fldChar3)
    doc.add_page_break()


def save(doc, path, doc_title):
    add_footer(doc, doc_title)
    doc.save(path)
    print(f"  wrote {path}")
