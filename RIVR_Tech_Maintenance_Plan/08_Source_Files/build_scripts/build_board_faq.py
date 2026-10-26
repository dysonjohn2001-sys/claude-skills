# -*- coding: utf-8 -*-
"""Builds the Maintenance Program FAQ (Word) + Board of Directors talking points (PPTX)."""
import os
import rivr_content as C
from docx_helpers import (new_doc, cover_page, toc_field, h1, h2, h3, para, bullet,
                          numbered, callout, table, save, _hr)

# PPTX
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
R = C.compute_model()
SC = C.scenario_results()


def p(*parts):
    return os.path.join(BASE, *parts)


# ==========================================================================
# PART 1 — MAINTENANCE PROGRAM FAQ (Word)
# ==========================================================================
FAQ_SECTIONS = [
    ("General", [
        ("What is the Customer-Premises Maintenance Program?",
         f"It is a fair, transparent way {C.COMPANY_SHORT} handles service visits. All {C.COMPANY_SHORT} "
         f"network and equipment repairs stay free. A reasonable charge may apply only when a technician "
         f"documents that the cause of a problem is on the customer's premises — their own equipment, wiring, "
         f"or power."),
        ("Why is RIVR Tech introducing this now?",
         f"Today every service visit is free, even when the problem is caused by customer-owned equipment or "
         f"wiring. Those customer-caused truck rolls cost an estimated {C.money(R['cust_caused_dispatch_cost'])} "
         f"per year, fully absorbed by {C.COMPANY_SHORT}, and crowd out genuine network work. The program "
         f"introduces a fair pricing signal while keeping all network repairs free."),
        ("Is this a rate increase?",
         f"No. Monthly internet, voice, and managed Wi-Fi service rates do not change. The program only "
         f"introduces specific fees for documented customer-premises visits, which customers can avoid through "
         f"self-service or the optional protection plan."),
        ("When does the program take effect?",
         f"After a customer-education period and a 30-day warning-only grace period, during which {C.COMPANY_SHORT} "
         f"explains potential charges but does not bill for customer-premises visits. The exact effective date is "
         f"set by the executive team."),
    ]),
    ("What Stays Free vs. What May Be Billable", [
        ("What does RIVR Tech still fix for free?",
         "Network outages; failed RIVR Tech ONTs and gateways; fiber and normal drop failures; no-trouble-found "
         "visits; inconclusive visits; and repeat visits shortly after a RIVR Tech repair. These are never billed."),
        ("When could a visit be billable?",
         "When documented findings show the root cause is a customer-premises responsibility: customer-owned "
         "equipment, customer-damaged wiring, premises power problems, third-party device setup, or a requested "
         "equipment relocation."),
        ("Will I be charged just because a technician was sent?",
         "No. A fee is never assessed solely because a technician was dispatched. A charge requires documented "
         "findings, advance disclosure, and the correct approval."),
        ("What if the technician can't find the problem?",
         "If findings are inconclusive or no trouble is found, there is no charge."),
    ]),
    ("Charges & Billing", [
        ("How much is a customer-premises visit?",
         f"${C.RES_FEE} for residential and ${C.BUS_FEE} for business, plus materials where applicable. Other "
         f"fees: additional labor $35 per 30 minutes after the first 30; missed appointment or denied access $35; "
         f"equipment relocation from $95 + materials; inside-wiring repair from $75 + materials; after-hours "
         f"customer-caused visits add a $75 surcharge."),
        ("How are charges determined?",
         "Only after a technician documents findings, test results, and (where relevant) photographs, and the "
         "visit is classified as a customer-premises responsibility by the responsibility matrix."),
        ("Will I be surprised by a charge?",
         "No. Any potential charge is disclosed before a technician is dispatched, and the customer acknowledges "
         "the disclosure. The acknowledgment confirms only that a charge may apply based on findings — it is not "
         "an admission of fault."),
        ("How will the charge appear?",
         "As a clearly itemized service charge on the customer's statement, with a plain-language description of "
         "the documented cause."),
    ]),
    ("Internet, Wi-Fi & Devices", [
        ("What's the difference between internet and Wi-Fi?",
         "Internet is the connection RIVR Tech delivers to the home. Wi-Fi is the wireless signal inside the home, "
         "which is affected by the customer's devices, walls, and layout."),
        ("Why is my Wi-Fi slow in one room?",
         "Wi-Fi weakens with distance and through walls. A wired test at the gateway usually shows full plan speed. "
         "RIVR Tech can suggest placement changes, mesh, or extenders — often as a courtesy the first time."),
        ("Can one old device slow everything down?",
         "An old or unsupported device can limit its own speed while the RIVR Tech connection still delivers full "
         "plan speed to other devices. That is a customer-premises matter."),
        ("How do I reboot my equipment?",
         "Power off the ONT, then the gateway; wait 30 seconds; power the ONT back on, then the gateway; then "
         "restart the device. This resolves many issues without a visit."),
    ]),
    ("Optional Maintenance-Protection Plan", [
        ("What is the optional protection plan?",
         f"RIVR Tech Home Maintenance Protection is an optional monthly plan (${C.PROTECTION_RECOMMENDED:.2f}/month) "
         f"that covers standard customer-premises trouble visits, basic inside-wiring diagnostics, Wi-Fi education, "
         f"and basic device-connection help, with priority scheduling."),
        ("Is the protection plan insurance?",
         "No. It is an optional service and maintenance plan — not insurance and not a warranty."),
        ("What is not covered by the plan?",
         "Replacement of customer-owned devices, major rewiring, concealed wiring, construction, commercial network "
         "administration, willful damage, gross negligence, and fire or flood damage."),
    ]),
    ("Disputes, Waivers & Fairness", [
        ("How do I dispute a charge?",
         "Contact RIVR Tech. Disputes follow a documented path: frontline explanation, then supervisor review, then "
         "technical review, with a billing adjustment if warranted — all within a defined timeline. No collection "
         "action occurs while a dispute is under review."),
        ("Are there any waivers?",
         "Yes. A first customer-caused incident is eligible for a one-time educational courtesy waiver. RIVR Tech "
         "also offers documentation-error, shared-responsibility, inconclusive, hardship, reasonable-accommodation, "
         "incorrect-disclosure, and retention waivers."),
        ("I have a disability or financial hardship. Can you help?",
         "Yes. RIVR Tech offers reasonable accommodations and hardship waivers, including for Lifeline and "
         "low-income customers. Please let us know so we can help."),
        ("What if the same problem returns after a RIVR Tech repair?",
         "If an issue recurs shortly after RIVR Tech performed a repair, there is no charge."),
    ]),
    ("Business Customers", [
        ("Does this apply to business service?",
         f"Business customer-premises visits are ${C.BUS_FEE}. Custom network configuration may be billed as "
         f"additional labor or referred to the customer's IT provider. The business service agreement governs where "
         f"applicable."),
    ]),
    ("Program & Operational (Internal / Board)", [
        ("How does the program protect RIVR Tech's reputation?",
         "The design leads with what stays free, mandates advance disclosure to prevent surprise billing, keeps "
         "fees below typical third-party rates, includes courtesy and hardship waivers, and uses 'customer-premises "
         "issue' language rather than 'customer fault.'"),
        ("How is consistency ensured across technicians?",
         "A 42-scenario responsibility matrix, standardized ticket and billing codes, mandatory documentation, "
         "supervisor approvals for shared/damage/relocation/repeat cases, and quality-control audits of coding "
         "accuracy and disclosure compliance."),
        ("What is the expected financial effect?",
         f"Under the expected scenario, the program returns about {C.money(R['year1_net'])} in Year 1 "
         f"(payback ~{R['payback_months']:.1f} months) and {C.money(R['three_year_net'])} over three years, "
         f"recovering roughly {R['cost_recovery_pct']*100:.0f}% of customer-caused dispatch cost. The primary "
         f"driver is reduced (avoided) truck rolls, not fee revenue."),
        ("What requires legal or regulatory review?",
         "North Carolina consumer-protection requirements, customer/business agreements, voice-service obligations, "
         "Lifeline treatment, billing and tax practices, the protection-plan (non-insurance) characterization, "
         "record retention, call recording, and electronic acknowledgment. These are flagged for review before "
         "go-live; this material is not legal advice."),
    ]),
]


def build_faq():
    doc = new_doc()
    cover_page(doc, "Customer-Premises Maintenance Program",
               "Frequently Asked Questions",
               "Program FAQ for Customers, Staff, and Leadership")
    toc_field(doc)

    h1(doc, "About This FAQ")
    para(doc, f"This FAQ explains the {C.COMPANY_SHORT} Customer-Premises Maintenance and Billable "
              f"Trouble-Visit Program in plain language. It is organized by topic. The one rule to "
              f"remember: {C.COMPANY_SHORT} network and equipment repairs are always free, and a "
              f"charge applies only when documented findings show a customer-premises cause.")
    callout(doc, "KEY PRINCIPLE", "A fee is never charged just because a technician was dispatched. "
            "A charge requires documented findings, advance disclosure, and the correct approval.",
            "recommendation")

    qnum = 0
    for section, items in FAQ_SECTIONS:
        h1(doc, section)
        for q, a in items:
            qnum += 1
            para(doc, f"Q{qnum}. {q}", bold=True, size=11, color=C.BRAND["secondary"], space_after=1)
            para(doc, a, size=10.5, space_after=8)

    h1(doc, "Quick Reference — Free vs. May Be Billable")
    table(doc, ["Always FREE ($0)", "May Be Billable (with documentation)"], [
        ("RIVR Tech network outage", "Customer-owned router / mesh failure"),
        ("Failed RIVR Tech ONT / gateway", "Customer-damaged wiring or drop"),
        ("Fiber / normal drop failure", "Premises power problem"),
        ("No trouble found", "Third-party camera / TV / smart-home setup"),
        ("Inconclusive / not reproduced", "Requested equipment relocation"),
        ("Repeat visit after a RIVR Tech repair", "Missed appointment / denied access"),
    ], col_widths=[3.2, 3.3], font_size=10)

    callout(doc, None, "This FAQ reflects the proposed program and labeled assumptions. It is not "
            "legal advice; provisions require legal, regulatory, and executive review before adoption.",
            "warning")

    save(doc, p("RIVR_Tech_Maintenance_Plan", "05_Customer_Communications",
                "RIVR_Tech_Maintenance_Program_FAQ.docx"), "Maintenance Program FAQ")


# ==========================================================================
# PART 2 — BOARD OF DIRECTORS TALKING POINTS (PPTX)
# ==========================================================================
B = {k: RGBColor.from_string(v) for k, v in C.BRAND.items()}
SW, SH = Inches(13.333), Inches(7.5)
DECK = "Board Talking Points"


def _blank(prs): return prs.slides.add_slide(prs.slide_layouts[6])


def _bg(s, c):
    s.background.fill.solid(); s.background.fill.fore_color.rgb = c


def _box(s, l, t, w, h): return s.shapes.add_textbox(l, t, w, h)


def _rect(s, l, t, w, h, c):
    shp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    shp.fill.solid(); shp.fill.fore_color.rgb = c; shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def _text(tf_or_s, text, size=18, color=None, bold=False, italic=False,
          align=PP_ALIGN.LEFT, para=False, space_after=6, level=0):
    tf = tf_or_s.text_frame if hasattr(tf_or_s, "text_frame") else tf_or_s
    po = tf.add_paragraph() if (para or tf.paragraphs[0].runs) else tf.paragraphs[0]
    po.alignment = align; po.level = level; po.space_after = Pt(space_after)
    r = po.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
    r.font.name = "Calibri"; r.font.color.rgb = color if color else B["dark"]
    return po


def _footer(s, pg):
    _rect(s, 0, Inches(7.1), SW, Inches(0.4), B["primary"])
    _text(_box(s, Inches(0.3), Inches(7.12), Inches(11), Inches(0.35)),
          f"{C.COMPANY_SHORT}  |  Board of Directors — Maintenance Program  |  Confidential Draft", 9, B["white"])
    _text(_box(s, Inches(12.4), Inches(7.12), Inches(0.8), Inches(0.35)), str(pg), 9, B["white"], align=PP_ALIGN.RIGHT)


def _content(prs, title, pg, kicker=None):
    s = _blank(prs); _bg(s, B["white"])
    _rect(s, 0, 0, SW, Inches(1.15), B["primary"]); _rect(s, 0, Inches(1.15), SW, Inches(0.05), B["accent"])
    tb = _box(s, Inches(0.6), Inches(0.16), Inches(12.1), Inches(0.95))
    if kicker: _text(tb, kicker, 12, B["light"], bold=True, space_after=2)
    _text(tb, title, 26, B["white"], bold=True, para=bool(kicker))
    _footer(s, pg)
    return s


def _bullets(s, items, top=Inches(1.5), size=17, left=Inches(0.7), width=Inches(12), height=Inches(5.2), gap=9):
    box = _box(s, left, top, width, height); box.text_frame.word_wrap = True
    for i, it in enumerate(items):
        txt, lvl = (it if isinstance(it, tuple) else (it, 0))
        _text(box, ("•  " if lvl == 0 else "–  ") + txt, size - lvl*2,
              B["dark"] if lvl == 0 else B["gray"], para=(i > 0), space_after=gap, level=lvl,
              bold=(lvl == 0 and txt.endswith(":")))
    return box


def _tiles(s, tiles, top=Inches(1.7)):
    n = len(tiles); margin = Inches(0.6); gap = Inches(0.3)
    tw = Emu(int((SW - 2*margin - gap*(n-1))/n)); x = margin
    for label, value, sub in tiles:
        _rect(s, x, top, tw, Inches(2.1), B["light"])
        _text(_box(s, x, top+Inches(0.3), tw, Inches(1.0)), value, 30, B["primary"], bold=True, align=PP_ALIGN.CENTER)
        lb = _box(s, x+Inches(0.1), top+Inches(1.3), tw-Inches(0.2), Inches(0.7))
        _text(lb, label, 13, B["dark"], bold=True, align=PP_ALIGN.CENTER)
        if sub: _text(lb, sub, 10, B["gray"], italic=True, align=PP_ALIGN.CENTER, para=True, space_after=0)
        x = Emu(int(x + tw + gap))


def _table(s, headers, rows, top=Inches(1.7), col_widths=None, size=13):
    nr, nc = len(rows)+1, len(headers)
    t = s.shapes.add_table(nr, nc, Inches(0.7), top, Inches(12), Inches(0.4*nr)).table
    if col_widths:
        for i, w in enumerate(col_widths): t.columns[i].width = Inches(w)
    for j, h in enumerate(headers):
        c = t.cell(0, j); c.fill.solid(); c.fill.fore_color.rgb = B["primary"]
        r = c.text_frame.paragraphs[0].add_run(); r.text = h
        r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = B["white"]; r.font.name = "Calibri"
    for i, row in enumerate(rows, 1):
        for j, val in enumerate(row):
            c = t.cell(i, j); c.fill.solid(); c.fill.fore_color.rgb = B["light"] if i % 2 else B["white"]
            c.text_frame.word_wrap = True
            r = c.text_frame.paragraphs[0].add_run(); r.text = str(val)
            r.font.size = Pt(size-1); r.font.name = "Calibri"; r.font.color.rgb = B["dark"]
            if j == 0: r.font.bold = True
    return t


def _callout(s, text, top=Inches(6.2), color=None):
    color = color or B["accent"]
    _rect(s, Inches(0.7), top, Inches(12), Inches(0.7), color)
    _text(_box(s, Inches(0.9), top+Inches(0.08), Inches(11.6), Inches(0.55)), text, 13, B["white"],
          bold=True, align=PP_ALIGN.CENTER)


def _notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def build_board_deck():
    prs = Presentation(); prs.slide_width = SW; prs.slide_height = SH
    pg = [1]
    def n(): pg[0] += 1; return pg[0]

    # Title
    s = _blank(prs); _bg(s, B["primary"])
    _rect(s, 0, Inches(2.7), SW, Inches(0.06), B["accent"])
    _text(_box(s, Inches(0.9), Inches(0.7), Inches(11.5), Inches(1.0)), C.COMPANY_SHORT.upper(), 40, B["white"], bold=True)
    _text(_box(s, Inches(0.9), Inches(1.55), Inches(11.5), Inches(0.5)), C.COMPANY_LEGAL, 13, B["light"], italic=True)
    mb = _box(s, Inches(0.9), Inches(3.0), Inches(11.5), Inches(2.2))
    _text(mb, "Customer-Premises Maintenance Program", 32, B["white"], bold=True)
    _text(mb, "Board of Directors — High-Level Talking Points", 19, B["light"], para=True, space_after=4)
    _text(mb, "Free network repairs • Fair, documented charges • No surprises", 15, B["accent"], para=True)
    _text(_box(s, Inches(0.9), Inches(6.3), Inches(11.5), Inches(0.7)),
          f"{C.DOC_VERSION}   |   {C.DOC_DATE}   |   CONFIDENTIAL — NOT LEGAL ADVICE", 11, B["light"], italic=True)
    _notes(s, "Purpose: give the Board a clear, high-level view of the proposed program, the economics, the "
              "customer-protection safeguards, and the decisions we are asking the Board to support. "
              "Emphasize this is education-first and reputation-protective, not a revenue grab.")

    # 1. The one-sentence story
    s = _content(prs, "The Story in One Sentence", n(), kicker="WHY WE'RE HERE")
    _bullets(s, [
        f"{C.COMPANY_SHORT} will keep every network and equipment repair free — and begin charging a fair, "
        f"fully documented fee only when a problem is caused on the customer's own premises.",
        ("This is about fairness and field capacity, not squeezing our members.", 1),
        ("We lead with what stays free. We never lead with fees.", 1),
    ], top=Inches(1.7), size=20)
    _callout(s, "Fair to customers. Fair to RIVR Tech. Reputation-protective by design.")
    _notes(s, "Open with the one-sentence framing. The Board's first question is usually 'will this upset our "
              "members?' — answer it immediately: network repairs stay free, charges are only for documented "
              "customer-caused work, disclosed in advance, with a courtesy waiver and a 30-day grace period.")

    # 2. Why now
    s = _content(prs, "Why Now", n())
    _bullets(s, [
        f"Today, every service visit is free — even when the cause is customer-owned equipment, wiring, or power.",
        f"Customer-caused truck rolls cost an estimated {C.money(R['cust_caused_dispatch_cost'])} per year, "
        f"fully absorbed by {C.COMPANY_SHORT}.",
        f"At about {C.money(R['cost_per_dispatch'])} per truck roll, these visits divert capacity from real "
        f"network and installation work.",
        "There is no pricing signal today to encourage self-service or protect customer-owned equipment.",
        "Third-party technicians already charge for this work — our members are often surprised we don't.",
    ], top=Inches(1.5), size=17)
    _notes(s, "Frame the problem in cost and capacity terms. Stress that doing nothing has a real, recurring cost "
              "and that the fee is below typical market rates. Avoid implying members are at fault — use "
              "'customer-premises.'")

    # 3. What the member experiences
    s = _content(prs, "What Our Members Experience", n())
    _table(s, ["Situation", "Charge"], [
        ("RIVR Tech network or equipment problem", "$0 — always free"),
        ("No trouble found / inconclusive", "$0"),
        ("Documented customer-premises visit (residential)", f"${C.RES_FEE} — disclosed in advance"),
        ("Documented customer-premises visit (business)", f"${C.BUS_FEE} — disclosed in advance"),
        ("First customer-caused incident", "Courtesy waiver when appropriate"),
        ("Optional protection plan", f"${C.PROTECTION_RECOMMENDED:.2f}/month"),
    ], top=Inches(1.6), col_widths=[8, 4], size=14)
    _callout(s, "No surprise billing: we disclose before we dispatch and document before we bill.")
    _notes(s, "Walk the table top-down so the Board sees 'free' first. The courtesy waiver and advance disclosure "
              "are the two safeguards that most reduce member friction.")

    # 4. How members are protected
    s = _content(prs, "How Members Are Protected", n(), kicker="REPUTATION SAFEGUARDS")
    _bullets(s, [
        "Advance disclosure before any dispatch that could bill — and recorded acknowledgment.",
        "A fee is never charged just because a technician was sent — documented findings are required.",
        "First-incident courtesy waiver, plus hardship and reasonable-accommodation waivers.",
        "A clear dispute and appeal process; no collection action while a dispute is open.",
        "30-day warning-only grace period before any billing begins.",
        "Fees kept below typical third-party service-call rates.",
    ], top=Inches(1.5), size=17)
    _notes(s, "This is the slide that answers the reputation risk head-on. Emphasize the cooperative/community "
              "relationship — these safeguards exist specifically to protect member trust.")

    # 5. Financial picture
    s = _content(prs, "The Financial Picture (Expected)", n())
    _tiles(s, [
        ("Year 1 net effect", C.money(R["year1_net"]), f"payback ~{R['payback_months']:.1f} mo"),
        ("3-year net effect", C.money(R["three_year_net"]), "cumulative"),
        ("Cost recovery", f"{R['cost_recovery_pct']*100:.0f}%", "of customer-caused cost"),
        ("Main driver", "Fewer truck rolls", "deflection, not fees"),
    ], top=Inches(1.7))
    _bullets(s, [
        f"Net fee revenue ~{C.money(R['net_fee_revenue'])}; optional protection-plan margin "
        f"~{C.money(R['protection_margin'])}; avoided-truck-roll savings ~{C.money(R['deflection_savings'])}.",
        "Even the conservative (Low) scenario is positive over three years.",
    ], top=Inches(4.2), height=Inches(1.7), size=15)
    _callout(s, "Model outputs under labeled assumptions — to be finalized with RIVR Tech data.", color=B["gray"])
    _notes(s, "Lead with the headline: positive Year 1, fast payback, and — critically — the biggest dollar lever "
              "is AVOIDED truck rolls from better remote troubleshooting, not the fees themselves. That reframes "
              "the program as an efficiency play the Board can support without reputational worry.")

    # 6. Scenarios
    s = _content(prs, "Range of Outcomes", n())
    _table(s, ["Scenario", "Year 1 Net", "3-Year Net"], [
        (name, C.money(SC[name]["year1_net"]), C.money(SC[name]["three_year_net"]))
        for name in ["Low", "Expected", "High"]
    ], top=Inches(1.8), col_widths=[4, 4, 4], size=15)
    _callout(s, "Downside is protected; the primary value is operational, not fee revenue.")
    _notes(s, "Show the Board the floor and the ceiling. The point: this is a low-regret decision — positive across "
              "scenarios, with the main benefit being reduced truck rolls.")

    # 7. Risks
    s = _content(prs, "Risks & How We Manage Them", n())
    _table(s, ["Risk", "Mitigation"], [
        ("Member backlash / reputation", "Education-first, 30-day grace, courtesy waiver, warm messaging, dispute process"),
        ("Perceived as a money grab", "Fees below market; publish what stays free; emphasize deflection over revenue"),
        ("Regulatory / consumer protection (NC)", "Legal review; documented findings before any charge"),
        ("Protection-plan characterization", "Legal/insurance review; it is a service plan, not insurance"),
        ("Employee inconsistency", "Mandatory training, coding audits, supervisor approvals"),
    ], top=Inches(1.5), col_widths=[4, 8], size=13)
    _notes(s, "Be candid about risks — the Board will trust the recommendation more. Each risk has a concrete, "
              "funded mitigation. The biggest one is reputation, and the grace period + courtesy waiver directly "
              "address it.")

    # 8. What we're asking the Board
    s = _content(prs, "What We're Asking the Board", n(), kicker="DECISIONS")
    _bullets(s, [
        "Endorse the Balanced fee posture ($75 residential / $125 business).",
        f"Support launching the optional protection plan at ${C.PROTECTION_RECOMMENDED:.2f}/month, pending "
        f"legal/insurance review.",
        "Support the education-first rollout: 30-day grace period + first-incident courtesy waiver.",
        f"Approve the one-time implementation investment (~{C.money(R['one_time_cost'])}) and the effective date.",
        "Authorize the NC consumer-protection, tax, and insurance-characterization review.",
    ], top=Inches(1.5), size=17)
    _callout(s, "Five decisions — all reversible except the public commitment to keep network repairs free.")
    _notes(s, "These mirror the five executive decisions. Frame them as directional endorsements, not operational "
              "detail. Emphasize that legal review is a precondition to go-live, not an afterthought.")

    # 9. Timeline
    s = _content(prs, "Rollout Timeline (90 Days)", n())
    _table(s, ["Phase", "Focus", "Window"], [
        ("1", "Policy, financial validation, legal review, system design", "Days 1–40"),
        ("2", "Employee training and member education", "Days 20–95"),
        ("3", "30-day warning-only grace period", "Days 55–85"),
        ("4", "Full billing begins", "Days 85–90"),
        ("5", "Performance review and optimization", "Days 90+"),
    ], top=Inches(1.7), col_widths=[1.2, 8.3, 2.5], size=14)
    _callout(s, "Members are educated first; billing starts only after a 30-day grace period.")
    _notes(s, "Reassure the Board on sequencing: nothing bills until training is done, members are educated, and a "
              "grace period has elapsed. Phase 5 brings results back for review.")

    # 10. The ask / close
    s = _content(prs, "Recommendation", n())
    _bullets(s, [
        "Approve the Balanced posture and the optional $9.99 protection plan.",
        "Proceed with the 90-day, education-first rollout, contingent on legal sign-off.",
        f"Expected Year 1 net ~{C.money(R['year1_net'])}; three-year net ~{C.money(R['three_year_net'])}.",
        "Keep every RIVR Tech network and equipment repair free — permanently.",
        ("A fair, community-first program that protects both our members and RIVR Tech.", 1),
    ], top=Inches(1.6), size=18)
    _callout(s, "Fair to members. Fair to RIVR Tech. Not legal advice — review required.", color=B["warn"])
    _notes(s, "Close on the cooperative/community value. Restate the permanent free-network-repair promise — it is "
              "the trust anchor of the whole program. Invite questions.")

    path = p("RIVR_Tech_Maintenance_Plan", "07_Final_Presentation",
             "RIVR_Tech_Board_Talking_Points.pptx")
    prs.save(path)
    print(f"  wrote {path} ({len(prs.slides._sldIdLst)} slides)")


if __name__ == "__main__":
    print("Building FAQ + Board talking points...")
    build_faq()
    build_board_deck()
    print("Done.")
