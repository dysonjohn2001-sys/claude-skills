#!/usr/bin/env python3
"""Generic .docx -> .pdf renderer (single source = the Word file).

Reads paragraphs, runs (bold/italic/size/color/yellow-highlight), page breaks,
and tables (with header shading + column widths) from a python-docx Document and
lays them out with reportlab Platypus. Fonts map to Helvetica (metric-equivalent
to Arial). Header shows the DRAFT banner; footer shows title + Page X of Y.
"""
import sys
from xml.sax.saxutils import escape

from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.oxml.ns import qn

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph as RLPara,
                                Table as RLTable, TableStyle, Spacer, PageBreak,
                                KeepTogether, CondPageBreak)
from reportlab.platypus.flowables import Flowable
from reportlab.lib.styles import ParagraphStyle

DRAFT_BANNER = "DRAFT FOR DISCUSSION AND LEGAL REVIEW"

ALIGN_MAP = {
    WD_ALIGN_PARAGRAPH.LEFT: TA_LEFT,
    WD_ALIGN_PARAGRAPH.CENTER: TA_CENTER,
    WD_ALIGN_PARAGRAPH.RIGHT: TA_RIGHT,
    WD_ALIGN_PARAGRAPH.JUSTIFY: TA_JUSTIFY,
    None: TA_LEFT,
}


def run_has_page_break(run):
    for br in run._element.findall(qn("w:br")):
        if br.get(qn("w:type")) == "page":
            return True
    # also lastRenderedPageBreak is not a real break; ignore
    return False


def run_markup(run, default_size=11):
    text = run.text or ""
    if text == "" and not run_has_page_break(run):
        # check for break element -> line break
        if run._element.findall(qn("w:br")):
            return "<br/>"
        return ""
    out = escape(text).replace("\n", "<br/>")
    # line breaks inside run
    for br in run._element.findall(qn("w:br")):
        if br.get(qn("w:type")) != "page":
            out += "<br/>"
    size = run.font.size.pt if run.font.size is not None else default_size
    color = run.font.color.rgb if (run.font.color and run.font.color.type is not None) else None
    bold = bool(run.bold)
    italic = bool(run.italic)
    highlight = run.font.highlight_color == WD_COLOR_INDEX.YELLOW

    attrs = f'size="{size}"'
    if color is not None:
        attrs += f' color="#{str(color)}"'
    if highlight:
        attrs += ' backColor="#FFFF66"'
    inner = out
    if bold:
        inner = f"<b>{inner}</b>"
    if italic:
        inner = f"<i>{inner}</i>"
    return f"<font {attrs}>{inner}</font>"


def para_style(p, idx):
    pf = p.paragraph_format
    align = ALIGN_MAP.get(p.alignment, TA_LEFT)
    left = pf.left_indent.inches * inch if pf.left_indent is not None else 0
    first = pf.first_line_indent.inches * inch if pf.first_line_indent is not None else 0
    sa = pf.space_after.pt if pf.space_after is not None else 4
    sb = pf.space_before.pt if pf.space_before is not None else 0
    # base font size from first run
    size = 11
    for r in p.runs:
        if r.font.size is not None:
            size = r.font.size.pt
            break
    style = ParagraphStyle(
        f"p{idx}", fontName="Helvetica", fontSize=size, leading=size * 1.15,
        alignment=align, spaceAfter=sa, spaceBefore=sb,
        leftIndent=left, firstLineIndent=first, allowWidows=1, allowOrphans=1,
    )
    return style


def render_paragraph(p, idx, flow):
    # page break?
    for r in p.runs:
        if run_has_page_break(r):
            flow.append(PageBreak())
    style_name = p.style.name if p.style is not None else ""
    prefix = ""
    if "List Bullet" in style_name:
        prefix = "•&nbsp;&nbsp;"
    markup = "".join(run_markup(r) for r in p.runs)
    # convert leading tab (manual numbered items) to spaces
    markup = markup.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
    if not markup.strip() and not prefix:
        flow.append(Spacer(1, (p.paragraph_format.space_after.pt if p.paragraph_format.space_after else 6)))
        return
    flow.append(RLPara(prefix + markup, para_style(p, idx)))


def cell_flow(cell, idx):
    parts = []
    for j, p in enumerate(cell.paragraphs):
        markup = "".join(run_markup(r) for r in p.runs)
        markup = markup.replace("\t", "&nbsp;&nbsp;")
        style_name = p.style.name if p.style is not None else ""
        prefix = "•&nbsp;" if "List Bullet" in style_name else ""
        align = ALIGN_MAP.get(p.alignment, TA_LEFT)
        size = 10
        for r in p.runs:
            if r.font.size is not None:
                size = r.font.size.pt
                break
        st = ParagraphStyle(f"c{idx}_{j}", fontName="Helvetica", fontSize=size,
                            leading=size * 1.2, alignment=align, spaceAfter=2)
        parts.append(RLPara(prefix + (markup if markup.strip() else "&nbsp;"), st))
    return parts


def cell_shading(cell):
    tcPr = cell._tc.find(qn("w:tcPr"))
    if tcPr is None:
        return None
    shd = tcPr.find(qn("w:shd"))
    if shd is None:
        return None
    fill = shd.get(qn("w:fill"))
    if fill and fill.lower() not in ("auto", "ffffff"):
        return colors.HexColor("#" + fill)
    return None


def render_table(tbl, idx, flow, avail_width):
    n_cols = len(tbl.columns)
    # column widths from cell width if set, else equal
    widths = []
    try:
        first_row = tbl.rows[0].cells
        for c in first_row:
            w = c.width
            widths.append(w.inches * inch if w is not None else None)
    except Exception:
        widths = [None] * n_cols
    if any(w is None for w in widths) or sum(w for w in widths if w) == 0:
        widths = [avail_width / n_cols] * n_cols
    else:
        scale = avail_width / sum(widths)
        widths = [w * scale for w in widths]

    data = []
    style_cmds = [
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BFBFBF")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    for ri, row in enumerate(tbl.rows):
        cells = row.cells
        data_row = []
        seen = set()
        for ci in range(n_cols):
            cell = cells[ci] if ci < len(cells) else cells[-1]
            data_row.append(cell_flow(cell, f"{idx}_{ri}_{ci}"))
            fill = cell_shading(cell)
            if fill is not None:
                style_cmds.append(("BACKGROUND", (ci, ri), (ci, ri), fill))
        data.append(data_row)
    t = RLTable(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle(style_cmds))
    flow.append(Spacer(1, 2))
    flow.append(t)
    flow.append(Spacer(1, 4))


class NumberedCanvas:
    pass


def build(docx_path, pdf_path, footer_title):
    doc = Document(docx_path)
    page_w, page_h = letter
    margin = inch
    avail_width = page_w - 2 * margin

    flow = []
    idx = 0
    body = doc.element.body
    for child in body.iterchildren():
        if child.tag == qn("w:p"):
            render_paragraph(Paragraph(child, doc), idx, flow)
        elif child.tag == qn("w:tbl"):
            render_table(Table(child, doc), idx, flow, avail_width)
        idx += 1

    # two-pass for "Page X of Y"
    from reportlab.pdfgen import canvas as canvasmod

    class TwoPassCanvas(canvasmod.Canvas):
        def __init__(self, *a, **kw):
            super().__init__(*a, **kw)
            self._saved = []

        def showPage(self):
            self._saved.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            total = len(self._saved)
            for state in self._saved:
                self.__dict__.update(state)
                self._draw_hf(total)
                canvasmod.Canvas.showPage(self)
            canvasmod.Canvas.save(self)

        def _draw_hf(self, total):
            self.saveState()
            # header banner
            self.setFont("Helvetica-Bold", 9)
            self.setFillColor(colors.HexColor("#B00000"))
            self.drawCentredString(page_w / 2, page_h - margin + 20, DRAFT_BANNER)
            self.setStrokeColor(colors.HexColor("#999999"))
            self.setLineWidth(0.5)
            self.line(margin, page_h - margin + 14, page_w - margin, page_h - margin + 14)
            # footer
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#555555"))
            self.line(margin, margin - 12, page_w - margin, margin - 12)
            self.drawString(margin, margin - 24, footer_title)
            self.drawRightString(page_w - margin, margin - 24,
                                 f"Page {self._pageNumber} of {total}")
            self.restoreState()

    frame = Frame(margin, margin, avail_width, page_h - 2 * margin,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    tmpl = PageTemplate(id="main", frames=[frame])
    pdf = BaseDocTemplate(pdf_path, pagesize=letter,
                          leftMargin=margin, rightMargin=margin,
                          topMargin=margin, bottomMargin=margin,
                          pageTemplates=[tmpl])
    pdf.build(flow, canvasmaker=TwoPassCanvas)
    print("Saved", pdf_path)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
