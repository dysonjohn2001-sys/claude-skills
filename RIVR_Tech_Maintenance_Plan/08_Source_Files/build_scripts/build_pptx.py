# -*- coding: utf-8 -*-
"""Builds RIVR Tech PowerPoint decks: employee training + executive presentation."""
import os
import rivr_content as C
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
R = C.compute_model()


def p(*parts):
    return os.path.join(BASE, *parts)


def rgb(h):
    return RGBColor.from_string(h)


B = {k: rgb(v) for k, v in C.BRAND.items()}
SW, SH = Inches(13.333), Inches(7.5)


def new_deck():
    prs = Presentation()
    prs.slide_width = SW
    prs.slide_height = SH
    return prs


def _blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def _bg(slide, color):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def _box(slide, l, t, w, h):
    return slide.shapes.add_textbox(l, t, w, h)


def _rect(slide, l, t, w, h, color, line=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    if line:
        shp.line.color.rgb = line
        shp.line.width = Pt(1)
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def _text(tf_or_slide, text, size=18, color=None, bold=False, italic=False,
          align=PP_ALIGN.LEFT, para=False, space_after=6, level=0):
    if hasattr(tf_or_slide, "text_frame"):
        tf = tf_or_slide.text_frame
    else:
        tf = tf_or_slide
    if para or tf.paragraphs[0].runs:
        para_obj = tf.add_paragraph()
    else:
        para_obj = tf.paragraphs[0]
    para_obj.alignment = align
    para_obj.level = level
    para_obj.space_after = Pt(space_after)
    run = para_obj.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = "Calibri"
    run.font.color.rgb = color if color else B["dark"]
    return para_obj


def footer(slide, deck_name, page):
    bar = _rect(slide, 0, Inches(7.1), SW, Inches(0.4), B["primary"])
    tb = _box(slide, Inches(0.3), Inches(7.12), Inches(12), Inches(0.35))
    _text(tb, f"{C.COMPANY_SHORT}  |  {deck_name}  |  {C.DOC_VERSION}", 9, B["white"])
    pg = _box(slide, Inches(12.4), Inches(7.12), Inches(0.8), Inches(0.35))
    _text(pg, str(page), 9, B["white"], align=PP_ALIGN.RIGHT)


def title_slide(prs, title, subtitle, tag, deck_name):
    s = _blank(prs)
    _bg(s, B["primary"])
    _rect(s, 0, Inches(2.7), SW, Inches(0.06), B["accent"])
    tb = _box(s, Inches(0.9), Inches(0.7), Inches(11.5), Inches(1.0))
    _text(tb, C.COMPANY_SHORT.upper(), 40, B["white"], bold=True)
    sb = _box(s, Inches(0.9), Inches(1.55), Inches(11.5), Inches(0.5))
    _text(sb, C.COMPANY_LEGAL, 13, B["light"], italic=True)
    mb = _box(s, Inches(0.9), Inches(3.0), Inches(11.5), Inches(2.0))
    _text(mb, title, 34, B["white"], bold=True)
    _text(mb, subtitle, 20, B["light"], para=True, space_after=4)
    _text(mb, tag, 15, B["accent"], para=True)
    fb = _box(s, Inches(0.9), Inches(6.3), Inches(11.5), Inches(0.7))
    _text(fb, f"{C.DOC_VERSION}   |   {C.DOC_DATE}   |   INTERNAL — NOT LEGAL ADVICE",
          11, B["light"], italic=True)
    return s


def section_slide(prs, num, title, deck_name, page):
    s = _blank(prs)
    _bg(s, B["dark"])
    nb = _box(s, Inches(0.9), Inches(2.4), Inches(2.5), Inches(2.0))
    _text(nb, num, 90, B["accent"], bold=True)
    tb = _box(s, Inches(3.4), Inches(2.9), Inches(9), Inches(1.5))
    _text(tb, title, 34, B["white"], bold=True)
    _rect(s, Inches(3.5), Inches(4.1), Inches(4), Inches(0.05), B["accent"])
    return s


def content_slide(prs, title, deck_name, page, kicker=None):
    s = _blank(prs)
    _bg(s, B["white"])
    _rect(s, 0, 0, SW, Inches(1.15), B["primary"])
    _rect(s, 0, Inches(1.15), SW, Inches(0.05), B["accent"])
    tb = _box(s, Inches(0.6), Inches(0.18), Inches(12.1), Inches(0.95))
    if kicker:
        _text(tb, kicker, 12, B["light"], bold=True, space_after=2)
    _text(tb, title, 26, B["white"], bold=True, para=bool(kicker))
    footer(s, deck_name, page)
    return s


def bullets(slide, items, left=Inches(0.7), top=Inches(1.5), width=Inches(12),
            height=Inches(5.3), size=17, gap=8):
    box = _box(slide, left, top, width, height)
    box.text_frame.word_wrap = True
    for i, item in enumerate(items):
        if isinstance(item, tuple):
            txt, lvl = item
        else:
            txt, lvl = item, 0
        bullet_char = "•  " if lvl == 0 else "–  "
        para = _text(box, bullet_char + txt, size - (lvl * 2), B["dark"] if lvl == 0 else B["gray"],
                     para=(i > 0), space_after=gap, level=lvl, bold=(lvl == 0 and txt.endswith(":")))
    return box


def two_col_table(slide, headers, rows, left=Inches(0.7), top=Inches(1.5),
                  width=Inches(12), col_widths=None, size=13, header_color=None):
    header_color = header_color or B["primary"]
    ncols = len(headers)
    nrows = len(rows) + 1
    tbl_shape = slide.shapes.add_table(nrows, ncols, left, top, width, Inches(0.4 * nrows))
    table = tbl_shape.table
    if col_widths:
        for i, w in enumerate(col_widths):
            table.columns[i].width = Inches(w)
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_color
        tf = cell.text_frame
        tf.word_wrap = True
        para = tf.paragraphs[0]
        run = para.add_run(); run.text = h
        run.font.size = Pt(size); run.font.bold = True
        run.font.color.rgb = B["white"]; run.font.name = "Calibri"
    for i, row in enumerate(rows, 1):
        for j, val in enumerate(row):
            cell = table.cell(i, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = B["light"] if i % 2 else B["white"]
            tf = cell.text_frame
            tf.word_wrap = True
            para = tf.paragraphs[0]
            run = para.add_run(); run.text = str(val)
            run.font.size = Pt(size - 1); run.font.name = "Calibri"
            run.font.color.rgb = B["dark"]
            if j == 0:
                run.font.bold = True
    return table


def stat_tiles(slide, tiles, top=Inches(1.6)):
    n = len(tiles)
    margin = Inches(0.6)
    gap = Inches(0.3)
    total_w = SW - 2 * margin - gap * (n - 1)
    tile_w = Emu(int(total_w / n))
    x = margin
    for label, value, sub in tiles:
        card = _rect(slide, x, top, tile_w, Inches(2.2), B["light"])
        vb = _box(slide, x, top + Inches(0.35), tile_w, Inches(1.0))
        _text(vb, value, 30, B["primary"], bold=True, align=PP_ALIGN.CENTER)
        lb = _box(slide, x + Inches(0.1), top + Inches(1.4), tile_w - Inches(0.2), Inches(0.7))
        _text(lb, label, 13, B["dark"], bold=True, align=PP_ALIGN.CENTER)
        if sub:
            _text(lb, sub, 10, B["gray"], italic=True, align=PP_ALIGN.CENTER, para=True, space_after=0)
        x = Emu(int(x + tile_w + gap))


def callout_bar(slide, text, top=Inches(6.2), color=None):
    color = color or B["accent"]
    bar = _rect(slide, Inches(0.7), top, Inches(12), Inches(0.7), color)
    tb = _box(slide, Inches(0.9), top + Inches(0.08), Inches(11.6), Inches(0.55))
    _text(tb, text, 13, B["white"], bold=True, align=PP_ALIGN.CENTER)


# ==========================================================================
# EMPLOYEE TRAINING DECK (60 minutes)
# ==========================================================================
def training_deck():
    DECK = "Employee Training"
    prs = new_deck()
    pg = [1]

    def nextpg():
        pg[0] += 1
        return pg[0]

    title_slide(prs, "Customer-Premises Maintenance Program",
                "Employee Training — 60 Minutes",
                "Free network repairs • Fair, documented charges • No surprises", DECK)

    # Agenda
    s = content_slide(prs, "Today's Agenda (60 minutes)", DECK, nextpg())
    two_col_table(s, ["Time", "Segment"], [
        ("0:00–0:05", "Why the policy is changing"),
        ("0:05–0:15", "Free vs. billable + the four classifications"),
        ("0:15–0:25", "Remote troubleshooting (deflection)"),
        ("0:25–0:35", "Advance disclosure + documentation"),
        ("0:35–0:45", "Empathetic customer communication"),
        ("0:45–0:55", "Billing, disputes, and waivers"),
        ("0:55–1:00", "Scenario exercises + knowledge check"),
    ], col_widths=[2.5, 9.5], size=15, top=Inches(1.5))

    # 1. Why changing
    section_slide(prs, "1", "Why the Policy Is Changing", DECK, nextpg())
    s = content_slide(prs, "Why We're Changing", DECK, nextpg(), kicker="SEGMENT 1")
    bullets(s, [
        "RIVR Tech network and equipment repairs stay FREE — always.",
        f"Customer-caused truck rolls cost about {C.money(R['cust_caused_dispatch_cost'])} per year today.",
        "No pricing signal exists to reduce avoidable visits or protect customer gear.",
        "Third-party technicians already charge for premises work.",
        "This is about fairness and capacity — not squeezing customers.",
        ("Our job: keep it fair, transparent, and warm.", 1),
    ])
    callout_bar(s, "We lead with what stays free. We never lead with fees.")

    # 2. Free vs billable
    section_slide(prs, "2", "Free vs. Billable + Classifications", DECK, nextpg())
    s = content_slide(prs, "Always Free vs. May Be Billable", DECK, nextpg(), kicker="SEGMENT 2")
    two_col_table(s, ["Always FREE ($0)", "May Be Billable"], [
        ("RIVR Tech network outage", "Customer-owned router/mesh failure"),
        ("Failed RIVR Tech ONT / gateway", "Customer-damaged wiring or drop"),
        ("Fiber / normal drop failure", "Premises power problem"),
        ("No trouble found", "Third-party camera / TV / smart-home setup"),
        ("Inconclusive / not reproduced", "Requested equipment relocation"),
        ("Repeat after a RIVR Tech repair", "Missed appointment / denied access"),
    ], col_widths=[6, 6], size=14)

    s = content_slide(prs, "The Four Classifications", DECK, nextpg(), kicker="SEGMENT 2")
    two_col_table(s, ["Classification", "Customer Charge"], [
        ("1. RIVR Tech responsibility", "$0 — never billed"),
        ("2. Customer-premises responsibility", "Fee may apply — with documented findings"),
        ("3. Shared responsibility", "Supervisor review — reduced fee or waiver"),
        ("4. Inconclusive", "$0 unless management approves on clear evidence"),
    ], col_widths=[5, 7], size=15, top=Inches(1.7))
    callout_bar(s, "A fee is NEVER charged just because we sent a technician.", color=B["warn"])

    s = content_slide(prs, "Recommended Fees", DECK, nextpg(), kicker="SEGMENT 2")
    stat_tiles(s, [
        ("Residential visit", f"${C.RES_FEE}", "customer-premises"),
        ("Business visit", f"${C.BUS_FEE}", "customer-premises"),
        ("Missed appt / denied", "$35", "often courtesy 1st time"),
        ("Protection plan", f"${C.PROTECTION_RECOMMENDED:.2f}", "per month, optional"),
    ])
    bullets(s, [
        "Extra labor: $35 per 30 min after the first 30 (billable work only).",
        "Relocation: $95 + materials.  Inside wiring: $75 + materials.  After-hours: +$75.",
        "First customer-caused incident: one-time educational courtesy waiver when appropriate.",
    ], top=Inches(4.1), height=Inches(2.8), size=15)

    # 3. Remote troubleshooting
    section_slide(prs, "3", "Remote Troubleshooting (Deflection)", DECK, nextpg())
    s = content_slide(prs, "Strong Triage Before Any Truck", DECK, nextpg(), kicker="SEGMENT 3")
    bullets(s, [
        "Verify account → check outages → review history & equipment status.",
        "Confirm power, cables, connections. Reboot in order: ONT → gateway → device.",
        "Separate INTERNET from WI-FI. Separate WHOLE-HOME from ONE DEVICE.",
        "Run an approved speed test; request a WIRED test at the gateway.",
        "Identify third-party gear (mesh, firewall, extenders).",
        "Educate when it can be fixed remotely — that's a win, not a failure.",
        ("If dispatch is needed and it could bill: DISCLOSE first.", 1),
    ], size=16)
    callout_bar(s, f"Every avoided truck roll saves about {C.money(R['cost_per_dispatch'])}. Deflection is the real win.")

    # 4. Disclosure + documentation
    section_slide(prs, "4", "Advance Disclosure + Documentation", DECK, nextpg())
    s = content_slide(prs, "No Surprise Billing", DECK, nextpg(), kicker="SEGMENT 4")
    bullets(s, [
        "Before any dispatch that could bill, DISCLOSE that a charge may apply.",
        "Record the customer's acknowledgment (call, SMS, email, portal, or work order).",
        "The customer acknowledges only that a charge MAY apply — not that they're at fault.",
        "Technicians document findings, tests, and photos BEFORE any fee.",
        "Pick the correct ticket + billing code.",
        ("No disclosure = no valid charge.", 1),
    ], size=17)
    callout_bar(s, "Findings before fees. Disclosure before dispatch.", color=B["secondary"])

    s = content_slide(prs, "Technician Documentation Checklist", DECK, nextpg(), kicker="SEGMENT 4")
    two_col_table(s, ["Step", "What to Capture"], [
        ("Test", "Optical, ONT, gateway, wired, wireless results"),
        ("Prove", "Bypass customer gear — show RIVR service is healthy"),
        ("Photograph", "Damage, power, wiring conditions"),
        ("Classify", "Correct classification + billing code"),
        ("Explain", "Plain language: 'customer-premises issue'"),
        ("Acknowledge", "Capture electronic acknowledgment"),
        ("Route", "Shared/damage/relocation/repeat → supervisor"),
    ], col_widths=[3, 9], size=14)

    # 5. Communication
    section_slide(prs, "5", "Empathetic Communication", DECK, nextpg())
    s = content_slide(prs, "Say This, Not That", DECK, nextpg(), kicker="SEGMENT 5")
    two_col_table(s, ["Say This", "Not That"], [
        ("\"This is a customer-premises issue.\"", "\"This is your fault.\""),
        ("\"The RIVR Tech service tested good.\"", "\"Your stuff is broken.\""),
        ("\"A charge may apply based on findings.\"", "\"You're getting charged.\""),
        ("\"Let me show you how to fix this.\"", "\"Nothing I can do.\""),
    ], col_widths=[6, 6], size=14, top=Inches(1.7))
    callout_bar(s, "Never say 'fault.' We're local, we're helpful, we explain.")

    # 6. Billing/disputes/waivers
    section_slide(prs, "6", "Billing, Disputes & Waivers", DECK, nextpg())
    s = content_slide(prs, "Disputes & Waivers", DECK, nextpg(), kicker="SEGMENT 6")
    bullets(s, [
        "Dispute path: frontline explanation → supervisor → technical review → billing adjustment.",
        "No collection action while a dispute is under review.",
        "Waiver categories you can point to:",
        ("First-time courtesy • Documentation error • Shared responsibility • Inconclusive", 1),
        ("Hardship • Reasonable accommodation • Incorrect disclosure • Repeat after RIVR repair • Retention", 1),
        "Technicians never collect cash and never guarantee a charge will be removed.",
    ], size=16)

    # Scenario exercises
    section_slide(prs, "7", "Scenario Exercises + Knowledge Check", DECK, nextpg())
    s = content_slide(prs, "Scenario Exercises", DECK, nextpg(), kicker="PRACTICE")
    two_col_table(s, ["Scenario", "Classification?", "Charge?"], [
        ("Area-wide network outage", "RIVR Tech", "$0"),
        ("Customer's own router failed (wired test = plan speed)", "Customer-premises", f"${C.RES_FEE} (1st courtesy)"),
        ("No trouble found, all tests normal", "Inconclusive", "$0"),
        ("Customer asks to move a working gateway", "Customer-premises", "$95 + materials"),
        ("Storm-damaged drop", "Shared", "Supervisor review"),
        ("Repeat visit 3 days after our repair", "RIVR Tech", "$0"),
    ], col_widths=[6.5, 3, 2.5], size=13)

    s = content_slide(prs, "Knowledge Check", DECK, nextpg(), kicker="ASSESSMENT")
    bullets(s, [
        "Complete the 18-question Employee Knowledge Assessment.",
        "Passing score: 80% (15 of 18 correct).",
        "Retakes allowed after quick coaching.",
        "Keep your Quick Reference Guide handy on every interaction.",
        ("Questions? Ask your supervisor or the enablement team.", 1),
    ], size=18)
    callout_bar(s, "Free network repairs. Fair, documented charges. No surprises.")

    path = p("RIVR_Tech_Maintenance_Plan", "04_Training",
             "Maintenance_Program_Employee_Training.pptx")
    prs.save(path)
    print(f"  wrote {path} ({len(prs.slides.__iter__.__self__._sldIdLst)} slides)")


# ==========================================================================
# EXECUTIVE PRESENTATION
# ==========================================================================
def exec_deck():
    DECK = "Executive Presentation"
    prs = new_deck()
    pg = [1]

    def nextpg():
        pg[0] += 1
        return pg[0]

    title_slide(prs, "Customer-Premises Maintenance & Trouble-Visit Program",
                "Executive Presentation",
                "Recommendation, financials, and the five decisions we need", DECK)

    # The ask
    s = content_slide(prs, "The Ask", DECK, nextpg())
    bullets(s, [
        "Approve a fair program that keeps ALL network & equipment repairs free.",
        "Add reasonable charges only for DOCUMENTED customer-premises visits.",
        "Launch an optional monthly maintenance-protection plan.",
        "Lead with education, a 30-day grace period, and a first-incident courtesy waiver.",
        ("Deflection and fairness — not fee revenue — drive the economics.", 1),
    ], size=18)
    callout_bar(s, f"Recommended: Balanced fees (${C.RES_FEE}/${C.BUS_FEE}) + ${C.PROTECTION_RECOMMENDED:.2f} protection plan.")

    # Problem
    s = content_slide(prs, "The Problem Today", DECK, nextpg())
    stat_tiles(s, [
        ("Cost per truck roll", C.money(R["cost_per_dispatch"]), "loaded"),
        ("Annual dispatch cost", C.money(R["annual_dispatch_expense"]), "all visits"),
        ("Customer-caused cost", C.money(R["cust_caused_dispatch_cost"]), "absorbed today"),
        ("Recovery today", "$0", "fully subsidized"),
    ])
    bullets(s, [
        "Every customer-caused truck roll is free today — and crowds out network work.",
        "No incentive for self-service or for protecting customer-owned equipment.",
    ], top=Inches(4.2), height=Inches(2.7), size=16)

    # What customer sees
    s = content_slide(prs, "What the Customer Experiences", DECK, nextpg())
    two_col_table(s, ["Situation", "Customer Charge"], [
        ("RIVR Tech network or equipment problem", "$0 — always free"),
        ("Inconclusive / no trouble found", "$0"),
        ("Documented customer-premises visit (residential)", f"${C.RES_FEE} — disclosed first"),
        ("Documented customer-premises visit (business)", f"${C.BUS_FEE} — disclosed first"),
        ("First customer-caused incident", "Courtesy waiver when appropriate"),
        ("Optional protection plan", f"${C.PROTECTION_RECOMMENDED:.2f}/month"),
    ], col_widths=[8, 4], size=14)
    callout_bar(s, "No surprise billing: we disclose before we dispatch and document before we bill.")

    # Financials
    s = content_slide(prs, "Expected Financial Result (Year 1)", DECK, nextpg())
    stat_tiles(s, [
        ("Net fee revenue", C.money(R["net_fee_revenue"]), "after waivers"),
        ("Plan margin", C.money(R["protection_margin"]), "contribution"),
        ("Deflection savings", C.money(R["deflection_savings"]), "avoided rolls"),
        ("Year 1 net", C.money(R["year1_net"]), f"payback {R['payback_months']:.1f} mo"),
    ])
    bullets(s, [
        f"Cost recovery of customer-caused dispatch cost: {R['cost_recovery_pct']*100:.0f}%.",
        f"Three-year net financial effect: {C.money(R['three_year_net'])}.",
        "Primary driver is avoided truck rolls (deflection), not fees.",
    ], top=Inches(4.2), height=Inches(2.7), size=16)
    callout_bar(s, "Model outputs under labeled assumptions — see the financial workbook.", color=B["gray"])

    # Scenarios
    s = content_slide(prs, "Scenarios: Low / Expected / High", DECK, nextpg())
    SCd = C.scenario_results()
    two_col_table(s, ["Scenario", "Net Fees", "Plan Margin", "Deflection", "Year 1 Net", "3-Yr Net"], [
        (name, C.money(SCd[name]["net_fee_revenue"]), C.money(SCd[name]["protection_margin"]),
         C.money(SCd[name]["deflection_savings"]), C.money(SCd[name]["year1_net"]),
         C.money(SCd[name]["three_year_net"]))
        for name in ["Low", "Expected", "High"]
    ], col_widths=[2.4, 2, 2.1, 2, 2, 1.5], size=13, top=Inches(1.8))
    callout_bar(s, "Even the Low scenario delivers positive three-year value.")

    # Protection plan
    s = content_slide(prs, "Optional Protection Plan", DECK, nextpg())
    two_col_table(s, ["Price Point", "Annual Revenue", "Contribution Margin"], [
        (f"${price:.2f}/mo", C.money(C.compute_model({'protection_price': price})["protection_revenue"]),
         C.money(C.compute_model({'protection_price': price})["protection_margin"]))
        for price in C.PROTECTION_PRICES
    ], col_widths=[4, 4, 4], size=15, top=Inches(1.7))
    bullets(s, [
        f"Recommended price: ${C.PROTECTION_RECOMMENDED:.2f}/month.",
        "Covers standard premises visits, inside-wiring diagnostics, Wi-Fi education, device help.",
        "It is a service plan — NOT insurance. Requires legal/insurance review.",
    ], top=Inches(4.2), height=Inches(2.7), size=15)

    # Rollout
    s = content_slide(prs, "90-Day Phased Rollout", DECK, nextpg())
    two_col_table(s, ["Phase", "Focus", "Window"], [
        ("1", "Policy, financial validation, legal review, system design", "Days 1–40"),
        ("2", "Employee training and customer education", "Days 20–95"),
        ("3", "30-day warning and courtesy-waiver period", "Days 55–85"),
        ("4", "Full billing implementation", "Days 85–90"),
        ("5", "Performance review and optimization", "Days 90–120+"),
    ], col_widths=[1.2, 8.3, 2.5], size=14, top=Inches(1.7))
    callout_bar(s, "Customers are educated first; billing starts only after a 30-day grace period.")

    # Risks
    s = content_slide(prs, "Top Risks & Mitigations", DECK, nextpg())
    two_col_table(s, ["Risk", "Mitigation"], [
        ("Reputation / backlash", "Education-first, grace period, courtesy waiver, dispute process"),
        ("Regulatory exposure (NC)", "Legal review; documented findings before any charge"),
        ("Perceived money grab", "Fees below market; publish what stays free; emphasize deflection"),
        ("Insurance mischaracterization", "Legal/insurance review of the protection plan"),
        ("Employee inconsistency", "Mandatory training; coding-accuracy audits; approvals"),
    ], col_widths=[4, 8], size=14, top=Inches(1.7))

    # Five decisions
    s = content_slide(prs, "The Five Decisions We Need", DECK, nextpg())
    two_col_table(s, ["#", "Decision", "Owner"], [
        (str(i), title, owner) for i, (title, desc, owner) in enumerate(C.EXEC_DECISIONS, 1)
    ], col_widths=[0.7, 9.3, 2], size=14, top=Inches(1.7))
    callout_bar(s, "Recommended: Balanced fees • $9.99 plan • grace + courtesy • fund ~$95K • authorize legal review.")

    # Close
    s = content_slide(prs, "Recommendation", DECK, nextpg())
    bullets(s, [
        "Approve the Balanced fee posture and the $9.99 protection plan.",
        "Proceed with the 90-day phased, education-first rollout.",
        f"Expected Year 1 net ≈ {C.money(R['year1_net'])} (payback ≈ {R['payback_months']:.1f} months).",
        f"Three-year net ≈ {C.money(R['three_year_net'])}, keeping all network repairs free.",
        ("Replace the ten data points, complete legal/insurance review, then set the effective date.", 1),
    ], size=18)
    callout_bar(s, "Fair to customers. Fair to RIVR Tech. Not legal advice — review required.", color=B["warn"])

    path = p("RIVR_Tech_Maintenance_Plan", "07_Final_Presentation",
             "Maintenance_Program_Executive_Presentation.pptx")
    prs.save(path)
    print(f"  wrote {path} ({len(prs.slides._sldIdLst)} slides)")


if __name__ == "__main__":
    print("Building PowerPoint decks...")
    training_deck()
    exec_deck()
    print("PowerPoint decks complete.")
