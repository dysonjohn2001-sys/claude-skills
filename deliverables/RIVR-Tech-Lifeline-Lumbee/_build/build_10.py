"""10_Employee_Training_Guide.docx — trainable employee guide for RIVR Tech
Lifeline & Lumbee Broadband Affordability Initiative.

Centerpiece: the PROHIBITED STATEMENTS table and the role-specific modules.
All regulatory facts cite the Regulatory Source Register (SR-x.y). No RIVR
prices are invented; open items are marked [CONFIRM].
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from docx_helpers import *

doc = new_doc()

OUT = "/home/user/claude-skills/deliverables/RIVR-Tech-Lifeline-Lumbee/10_Employee_Training_Guide.docx"

# =====================================================================
# COVER + TOC
# =====================================================================
cover(
    doc,
    title="Employee Training Guide",
    subtitle="Lifeline & Lumbee Broadband Affordability Initiative",
    deliverable_no="10 — Employee Training Guide",
    owner="Compliance Officer + Training Lead",
    approvers="________________________  (Compliance Officer / date)",
    version="v0.1 — DRAFT (build phase)",
    extra=("This guide is a build-phase training artifact. RIVR Tech is NOT yet an "
           "approved Lifeline provider — the NCUC ETC order is PENDING (SR-7.4). Do not "
           "enroll, market, or bill Lifeline until the final order issues and USAC "
           "onboarding completes. Every dollar figure below is a federal program constant "
           "(re-verify each program year) — RIVR retail prices are NOT set here."),
)

toc(doc)

# =====================================================================
# 1. WHY THIS TRAINING MATTERS
# =====================================================================
h1(doc, "1. Why This Training Matters")
para(doc,
     "The Lumbee Tribe of North Carolina received full federal recognition in December 2025 "
     "(SR-5.1) and was added to the official list of federally recognized tribes in January 2026 "
     "(SR-5.2). This is a landmark for our community — and it creates a real risk of an honest, "
     "well-meaning mistake that can cost RIVR Tech money and its reputation, and can cost a "
     "customer the benefit they were counting on.")
para(doc,
     "The mistake is simple to make: assuming that because someone is Lumbee, or because they live "
     "in Robeson, Cumberland, Hoke, or Scotland County, they automatically get the higher 'enhanced "
     "Tribal' Lifeline benefit. They do not. This guide exists so that every employee — no matter "
     "the role — says the same accurate thing to every customer, every time.")
para(doc,
     "Why it matters concretely: Lifeline is a FEDERAL program funded by the Universal Service Fund. "
     "Every enrollment we claim is audited. Claiming an enhanced Tribal benefit for a customer who "
     "does not qualify is an improper claim — it must be repaid, it can trigger penalties, and it "
     "puts our ETC designation at risk. Telling a customer they qualify when they do not sets them "
     "up for a denial and a bad experience. Getting this right protects the customer, the company, "
     "and the program.", size=10.5)

para(doc, "The one rule that governs everything in this guide:", bold=True, size=11)
callout(doc,
    "Lumbee membership and residence in the four counties (Robeson, Cumberland, Hoke, Scotland) do "
    "NOT qualify a customer for the enhanced Tribal Lifeline benefit ($34.25/mo). Enhanced support "
    "requires the customer's PRINCIPAL RESIDENCE to be physically ON qualifying Tribal lands, "
    "verified PER-ADDRESS using USAC's Tribal Lands Verification Tool. No verified address = no "
    "enhanced benefit. Standard Lifeline is $9.25/mo (SR-1.1); enhanced is up to $34.25/mo (SR-1.3); "
    "the difference turns entirely on the ADDRESS, not on who the person is (SR-4.2, SR-5.5, SR-5.6).",
    kind="stop")
para(doc,
     "As of this build, the Lumbee have no reservation, no land held in trust, and no FCC "
     "§54.412 designation — so no four-county address is presumptively 'Tribal lands,' and the "
     "working assumption is ZERO enhanced-Tribal subscribers until a written USAC/legal "
     "determination says otherwise (SR-5.5). If that ever changes, this guide will be updated first.",
     italic=True, size=9.5, color=GREY)

# =====================================================================
# 2. PROHIBITED STATEMENTS (CENTERPIECE)
# =====================================================================
h1(doc, "2. Prohibited Statements — Never Say These")
callout(doc,
    "The six statements below are PROHIBITED in any customer conversation, script, email, text, "
    "social post, flyer, or voicemail. They are inaccurate, and repeating them creates compliance "
    "exposure for RIVR Tech and false expectations for the customer. Learn the 'What to say instead' "
    "column — it is the approved language. If you are ever unsure, say less and route to Compliance.",
    kind="warn")

rows = [
    ["“Every Lumbee member receives $34.25.”",
     "Enhanced Tribal support is ADDRESS-based, not membership-based. It requires the principal "
     "residence to be on qualifying Tribal lands, verified per-address (SR-4.2). Lumbee membership "
     "confers no enhanced benefit by itself (SR-5.6). Today the working assumption is that NO "
     "four-county address qualifies (SR-5.5).",
     "“Lifeline is a federal benefit — standard support is $9.25 a month. There’s a higher "
     "$34.25 amount ONLY for customers whose home address is verified as being on qualifying Tribal "
     "lands. Being Lumbee doesn’t decide that; the address does, and we check it with the federal "
     "verification tool. Let’s confirm whether you qualify for standard Lifeline first.”"],

    ["“All four counties are Tribal lands.”",
     "Robeson, Cumberland, Hoke and Scotland are the Tribe’s SERVICE DELIVERY AREA for federal "
     "services (SR-5.4). A service delivery area is NOT ‘Tribal lands’ under 47 C.F.R. "
     "§54.400(e) (SR-5.4). ‘Tribal lands’ means a reservation, trust land, or an "
     "FCC-designated area — none of which exist for the Lumbee yet (SR-5.5).",
     "“Those four counties are the Tribe’s service area, which is different from federally "
     "designated ‘Tribal lands.’ For the enhanced Lifeline amount, the government checks the "
     "specific street address against its Tribal-lands map. Let me note your address and we’ll "
     "verify it the right way.”"],

    ["“All senior citizens automatically qualify for Lifeline.”",
     "Age is NOT a Lifeline eligibility criterion. Lifeline requires income ≤135% of the Federal "
     "Poverty Guidelines OR participation in a qualifying program (Medicaid, SNAP, SSI, FPHA, "
     "Veterans/Survivors Pension) (SR-1.4, SR-1.6). A senior may or may not meet those tests.",
     "“Lifeline isn’t based on age — it’s based on household income or being in a "
     "program like Medicaid, SNAP, SSI, federal housing assistance, or the Veterans Pension. Many "
     "seniors do qualify, so let’s check: are you in any of those programs, or would your "
     "household income be at or below the Lifeline limit?”"],

    ["“The Tribe guarantees approval.”",
     "The Lumbee Tribe does not approve Lifeline. Eligibility is determined by USAC’s National "
     "Verifier BEFORE any enrollment (SR-3.1). No one at RIVR Tech, and no Tribal official, can "
     "guarantee a federal eligibility result.",
     "“No one can guarantee approval — Lifeline eligibility is decided by the federal National "
     "Verifier, not by RIVR Tech or the Tribe. What I can do is help you apply and make sure the "
     "information is complete so the check goes smoothly. If you’re approved, here’s what "
     "happens next.”"],

    ["“Customers can receive multiple Lifeline benefits.”",
     "The rule is ONE Lifeline benefit per household (SR-1.8). A ‘household’ is everyone "
     "living at one address as a single economic unit. A customer cannot keep a Lifeline benefit "
     "with another provider AND take one from us (SR-3.6).",
     "“Lifeline is one benefit per household — you can’t have two at once. If you already "
     "have Lifeline with another company, you can TRANSFER it to us with your consent; you just "
     "can’t keep both. Do you currently have a Lifeline phone or internet with anyone else?”"],

    ["“This program is the same as ACP.”",
     "The Affordable Connectivity Program (ACP) has ENDED. Lifeline is a separate, ongoing program "
     "with different rules and amounts (SR-8.6). Presenting Lifeline as ACP, or implying ACP is still "
     "active, is inaccurate.",
     "“The ACP program you may remember has ended. This is Lifeline — a separate federal program "
     "that’s still active. The eligibility rules and the benefit amount are different from ACP, "
     "so let’s go through the Lifeline requirements specifically.”"],
]
table(doc,
      ["Prohibited statement", "Why it’s wrong", "What to say instead"],
      rows, widths=[1.7, 2.5, 3.0], small=True)
para(doc,
     "Rule of thumb: if a sentence promises a specific dollar amount, a guaranteed approval, or "
     "treats ‘Lumbee’ / ‘four counties’ / ‘senior’ as automatic "
     "qualification, stop and use the approved language above.",
     italic=True, size=9.5, color=GREY)

# =====================================================================
# 3. CORE CONCEPTS
# =====================================================================
h1(doc, "3. Core Concepts Every Employee Must Know")

h2(doc, "3.1 Four separate tests — never blur them together")
para(doc,
     "Most mistakes come from collapsing four independent things into one. They are separate. A "
     "customer can pass some and fail others. Evaluate each on its own:")
table(doc,
      ["Test", "What it decides", "What it does NOT decide"],
      [["1. Standard Lifeline eligibility",
        "Whether the customer gets the standard $9.25/mo benefit — via income ≤135% FPG or a "
        "qualifying program (SR-1.4, SR-1.6).",
        "Does not decide the enhanced amount; does not depend on tribe or age."],
       ["2. Enhanced Tribal eligibility",
        "Whether the customer gets the extra $25 (total up to $34.25) — requires the principal "
        "residence ON qualifying Tribal lands, verified per-address (SR-4.2, SR-4.4).",
        "Not decided by membership, county of residence, or income."],
       ["3. Lumbee membership",
        "A separate status relevant to Tribe-funded or outreach programs only. Handled through "
        "outreach / Tribe-funded channels, not federal Lifeline (SR-5.6).",
        "Does not confer standard OR enhanced Lifeline. Not a federal eligibility test."],
       ["4. Senior status",
        "Relevant to company-funded senior offerings and outreach targeting.",
        "Age alone is NOT a Lifeline eligibility factor (SR-1.4). A senior must still pass Test 1."]],
      widths=[1.9, 3.1, 2.2], small=True)

h2(doc, "3.2 The two benefit amounts")
bullet(doc, "Standard Lifeline: up to $9.25/mo for broadband or bundled voice+broadband (SR-1.1).")
bullet(doc, "Enhanced Tribal: an ADDITIONAL up to $25/mo on top of standard = total up to $34.25/mo "
            "(SR-1.3). The carrier must certify full pass-through to the subscriber.")
para(doc, "These are FEDERAL amounts, re-verified each program year. They are NOT RIVR retail prices. "
          "Never tell a customer a final out-of-pocket price in training scenarios — RIVR's Senior-plan "
          "pricing is set separately and is not established in this guide [CONFIRM current price sheet].",
     italic=True, size=9.5, color=GREY)

h2(doc, "3.3 How someone becomes eligible for standard Lifeline")
para(doc, "Either path qualifies:")
numbered(doc, "Income: total household income at or below 135% of the Federal Poverty Guidelines "
              "(SR-1.4). 2026 thresholds are on the USAC handout [CONFIRM against live USAC PDF] "
              "(SR-1.5) — do not quote a dollar figure from memory.")
numbered(doc, "Program participation: Medicaid, SNAP, SSI, Federal Public Housing Assistance, or the "
              "Veterans & Survivors Pension Benefit (SR-1.6). Certain Tribal programs (BIA General "
              "Assistance, Tribal TANF, income-qualifying Head Start, FDPIR) also qualify a person for "
              "STANDARD Lifeline — but they do NOT establish Tribal-lands residence for the enhanced "
              "benefit (SR-1.7).")

h2(doc, "3.4 One benefit per household")
para(doc, "One Lifeline benefit per household (SR-1.8). A 'household' is everyone living together at "
          "one address as a single economic unit (adults sharing income and expenses). Where multiple "
          "genuinely-separate households share an address, a one-per-household worksheet is used.")

h2(doc, "3.5 The National Verifier comes BEFORE enrollment")
para(doc, "No one is enrolled on the strength of a conversation. USAC's National Verifier must approve "
          "identity, address, and program/income eligibility, and screen for duplicates, BEFORE we "
          "enroll anyone in NLAD (SR-3.1, SR-3.2). Our job is to help the customer apply accurately — "
          "the Verifier decides.")

h2(doc, "3.6 ACP has ended — never present it as active")
para(doc, "The Affordable Connectivity Program has ended (SR-8.6). Lifeline is separate and ongoing. "
          "Never call this 'ACP,' never say ACP is coming back, and never merge the two sets of rules.")

# =====================================================================
# 4. FOUR SENIOR SUB-POPULATIONS
# =====================================================================
h1(doc, "4. The Four Senior Sub-Populations")
para(doc,
     "Because RIVR serves a community with many Lumbee members and many seniors, employees will meet "
     "seniors who fall into very different buckets. Treat each senior as an individual and figure out "
     "which bucket they are actually in — do not assume. A single customer can even move between "
     "buckets (e.g., a senior who is a Lumbee member AND qualifies for standard Lifeline).")
table(doc,
      ["Senior sub-population", "What they get", "What the employee must verify", "Watch out for"],
      [["A. Seniors who qualify for Lifeline",
        "Standard $9.25/mo (SR-1.1) after National Verifier approval.",
        "Income ≤135% FPG OR a qualifying program (SR-1.4, SR-1.6); NV approval before enrollment "
        "(SR-3.1).",
        "Do NOT assume age qualified them — confirm the actual income/program test."],
       ["B. Seniors who are Lumbee members",
        "Nothing federal FROM membership. Any benefit here is Tribe-funded / outreach or "
        "company-funded only (SR-5.6).",
        "Membership status is handled via outreach / Tribe-funded channels — kept SEPARATE from "
        "federal Lifeline claims.",
        "Do NOT convert membership into an enhanced-Tribal Lifeline claim."],
       ["C. Seniors whose ADDRESS qualifies for enhanced Tribal",
        "Enhanced up to $34.25/mo (SR-1.3) — only if the address verifies.",
        "Principal residence ON qualifying Tribal lands, verified per-address via USAC tool "
        "(SR-4.2, SR-4.4). Today the working assumption is ZERO such addresses (SR-5.5).",
        "Requires a VERIFIED address. No verified address = standard only."],
       ["D. Seniors who qualify for NO federal support",
        "No federal Lifeline. Eligible only for any RIVR company-funded senior offering, if one "
        "exists.",
        "Confirm they fail BOTH the income and program tests; then route to the company-funded "
        "option (pricing not set in this guide) [CONFIRM].",
        "Do NOT force-fit them into Lifeline. Be honest that federal support doesn’t apply."]],
      widths=[1.7, 1.7, 2.4, 1.6], small=True)

# =====================================================================
# 5. ROLE-SPECIFIC MODULES
# =====================================================================
h1(doc, "5. Role-Specific Modules")
para(doc,
     "Every employee learns Sections 1–4. This section adds what each role must do differently. "
     "Complete YOUR module and the knowledge check at the end of it. Supervisors and Compliance "
     "Staff complete all modules relevant to the teams they oversee.")

def module(title_txt, key_tasks, must_know, mistakes, quiz):
    h2(doc, title_txt)
    para(doc, "Key tasks", bold=True, size=10.5, color=NAVY)
    for t in key_tasks: bullet(doc, t)
    para(doc, "Must-know rules", bold=True, size=10.5, color=NAVY)
    for t in must_know: bullet(doc, t)
    para(doc, "Common mistakes", bold=True, size=10.5, color=RED)
    for t in mistakes: bullet(doc, t)
    para(doc, "Knowledge check", bold=True, size=10.5, color=NAVY)
    for q in quiz: numbered(doc, q)

module(
    "5.1 Member Service Representatives (MSRs)",
    ["Answer inbound questions about Lifeline and the Senior plan using approved language (Section 2).",
     "Screen for the correct test path (income vs. program) and set the customer's expectation that the "
     "National Verifier decides (SR-3.1).",
     "Log the customer's address so enhanced-Tribal eligibility is decided by the USAC tool, never by "
     "assumption (SR-4.4).",
     "Route enhanced-Tribal, membership, and pricing questions to the right channel; escalate anything "
     "uncertain to Compliance."],
    ["Standard = $9.25 (SR-1.1); enhanced = up to $34.25 only for verified Tribal-lands addresses "
     "(SR-1.3, SR-4.2).",
     "Never guarantee approval; the Verifier decides (SR-3.1). One benefit per household (SR-1.8).",
     "Working assumption today: ZERO four-county addresses qualify for enhanced (SR-5.5)."],
    ["Telling a Lumbee caller they ‘get $34.25’ (prohibited — Section 2).",
     "Treating a senior as auto-qualified because of age (SR-1.4).",
     "Quoting an income dollar figure from memory instead of the current USAC handout (SR-1.5)."],
    ["A Lumbee caller asks if they get $34.25 because they’re a member. What do you say?",
     "A caller is 71 and wants Lifeline. What must you verify before saying they qualify?",
     "What has to happen BEFORE you enroll anyone?",
     "A caller already has Lifeline internet with another company and wants ours too. What’s the rule?",
     "True/False: any address in Robeson County qualifies for the enhanced $34.25 benefit."]
)

module(
    "5.2 Sales Representatives",
    ["Present the Senior plan and Lifeline accurately; never over-promise a dollar amount or approval.",
     "Self-register at LifelineRAD.org for a unique Rep ID before enrolling any subscriber (SR-6.6).",
     "Collect complete, accurate information so the National Verifier check succeeds the first time.",
     "Capture the service address for per-address Tribal-lands verification (SR-4.4)."],
    ["Sales incentives NEVER justify an inaccurate eligibility statement — Section 2 is absolute.",
     "You cannot enroll before National Verifier approval (SR-3.1); you cannot claim enhanced without "
     "a verified address (SR-4.2).",
     "RIVR is not yet an approved Lifeline provider — do not market as one until the ETC order issues "
     "(SR-7.4)."],
    ["Closing a sale by promising the enhanced $34.25 to a Lumbee prospect (prohibited).",
     "Implying ‘the Tribe guarantees approval’ to reduce hesitation (prohibited — SR-3.1).",
     "Presenting Lifeline as ‘the ACP program’ to a customer who remembers ACP (SR-8.6)."],
    ["Can you promise a customer the $34.25 rate to close a deal? Why or why not?",
     "What must you obtain before you enroll your first subscriber? (Hint: RAD.)",
     "A prospect says ‘just sign me up today.’ Why can’t you complete enrollment on the spot?",
     "How do you handle a prospect who insists ACP is still active?",
     "What single piece of information decides enhanced-Tribal eligibility?"]
)

module(
    "5.3 Technical Support",
    ["Support the Senior 100/100 plan and equipment (indoor Wi-Fi 6 router / outdoor mesh) without "
     "making eligibility or price promises.",
     "Recognize that speed/service quality is unrelated to Lifeline eligibility, and route eligibility "
     "questions to MSR/Compliance.",
     "Document any service address changes so they flow to NLAD within 10 business days (SR-3.2)."],
    ["The Senior 100/100 plan exceeds the 25/3 Mbps minimum and the data-allowance minimum; plans are "
     "unlimited (SR-2.1, SR-2.2).",
     "You are not the eligibility authority — never confirm or deny a customer’s Lifeline status.",
     "An address change can affect NLAD and (potentially) Tribal-lands status — flag it, don’t "
     "quietly fix it."],
    ["Answering ‘do I qualify for the discount?’ with a guess instead of a routing.",
     "Changing a subscriber’s address in systems without notifying the enrollment/compliance path (SR-3.2).",
     "Telling a customer the plan ‘isn’t fast enough to count’ — it meets all minimums (SR-2.1)."],
    ["Does the Senior 100/100 plan meet the federal minimum speed standard?",
     "A customer asks you whether they qualify for enhanced Tribal support. What do you do?",
     "Within how many business days must a subscriber info change reach NLAD?",
     "Is internet speed part of Lifeline ELIGIBILITY? Explain briefly.",
     "Who owns the eligibility answer — you, or the National Verifier?"]
)

module(
    "5.4 Billing",
    ["Apply the correct benefit amount to the bill: $9.25 standard, or up to $34.25 ONLY where the "
     "enhanced flag is set from a verified address (SR-1.1, SR-1.3, SR-4.4).",
     "Ensure the benefit is passed through fully to the subscriber (carrier certifies pass-through, SR-1.3).",
     "Keep RIVR-funded discounts, Lifeline credits, TBCP/grant funds, and Tribe contributions in "
     "SEPARATE billing/GL categories — never commingled (SR-10.2)."],
    ["Never bill an enhanced credit without a verified Tribal-lands address on file (SR-4.2).",
     "Do not advertise ‘plus tax’ on the Senior plan until the tax advisor confirms which "
     "components are taxable (SR-9.9).",
     "The non-usage rule generally does not apply where there is a >$0 customer charge — [CONFIRM] "
     "with counsel given the plan charge (SR-3.4)."],
    ["Applying $34.25 based on a customer being Lumbee rather than a verified address (SR-5.6).",
     "Commingling Lifeline credits with company-funded or grant discounts (SR-10.2).",
     "Adding ‘plus tax’ to broadband, which is non-taxable under ITFA (SR-9.1, SR-9.9)."],
    ["What must be on file before you apply the $34.25 enhanced credit?",
     "Can you list ‘plus tax’ on the Senior broadband plan today? Why or why not?",
     "Name two of the four funding streams that must stay in separate categories.",
     "A Lumbee customer’s address did NOT verify as Tribal lands. Which benefit amount applies?",
     "Who certifies that the benefit is fully passed through to the subscriber?"]
)

module(
    "5.5 Accounting",
    ["Maintain four separate GL categories: federal Lifeline (USAC), TBCP/other grants, RIVR-funded "
     "discounts, and Lumbee Tribe contributions (SR-10.2).",
     "Support monthly Lifeline claims built from the NLAD Subscriber Snapshot (1st of month), certified "
     "by the 8th (SR-6.8).",
     "Retain compliance and subscriber-eligibility records for the required period (SR-6.11)."],
    ["Do NOT characterize TBCP grant funds as a recurring consumer subsidy unless the specific award "
     "expressly authorizes it (SR-10.1).",
     "Record retention: compliance records ≥ 3 full preceding calendar years; eligibility docs for "
     "as long as service continues, minimum 3 years — NOT the 10-year high-cost rule (SR-6.11).",
     "Claims are per Study Area Code (SAC); one claim per SAC per month (SR-6.8)."],
    ["Booking grant funds as consumer subsidy without award authorization (SR-10.1).",
     "Commingling the four funding streams (SR-10.2).",
     "Applying the wrong (10-year) retention period to Lifeline records (SR-6.11)."],
    ["How many separate funding categories must you maintain, and name them.",
     "What is the Lifeline record-retention minimum — and what is the WRONG number people cite?",
     "Can TBCP funds be booked as a recurring consumer subsidy by default?",
     "The monthly claim is built from which NLAD artifact, taken on what date?",
     "Claims are filed per what unit of account?"]
)

module(
    "5.6 Marketing",
    ["Produce outreach that publicizes Lifeline availability to those likely to qualify (SR-6.12), using "
     "only approved, accurate language (Section 2).",
     "Target seniors and the Lumbee community for AWARENESS — without stating or implying automatic "
     "qualification.",
     "Route all Lifeline-related copy through Compliance review before publication."],
    ["Never publish any of the six prohibited statements (Section 2) in any channel.",
     "Do not market RIVR as an approved Lifeline provider until the ETC order issues (SR-7.4).",
     "Do not present Lifeline as ACP, and never imply the enhanced $34.25 is automatic for Lumbee "
     "members or four-county residents (SR-5.6, SR-8.6)."],
    ["A flyer reading ‘Lumbee members save $34.25/mo’ (prohibited — SR-5.6).",
     "A social post implying seniors ‘automatically qualify’ (SR-1.4).",
     "Reusing old ACP creative and calling this program ACP (SR-8.6)."],
    ["Can a flyer say ‘Lumbee members get the enhanced $34.25 benefit’? Why not?",
     "What approval must be in place before we market RIVR as a Lifeline provider?",
     "How should outreach frame the enhanced benefit so it’s accurate?",
     "What must every piece of Lifeline copy pass through before publishing?",
     "Is it acceptable to reuse ACP branding for this program?"]
)

module(
    "5.7 Field Technicians",
    ["Install and service the Senior plan at the customer’s address without making eligibility or "
     "price promises.",
     "Confirm and record the exact service address (and, where needed, coordinates) so the USAC "
     "Tribal-lands verification is accurate (SR-4.4).",
     "Report any address discrepancy between the work order and the physical location to the enrollment/"
     "compliance path."],
    ["The service address is the linchpin of enhanced-Tribal eligibility — accuracy matters (SR-4.2, SR-4.4).",
     "You are not the eligibility authority; never tell a customer on-site that they ‘qualify’ for "
     "a benefit amount.",
     "Address changes must reach NLAD within 10 business days (SR-3.2)."],
    ["Casually telling a customer at install ‘you’ll get the $34.25 Tribal rate’ (prohibited).",
     "Recording an approximate or incorrect service address (breaks per-address verification, SR-4.4).",
     "Not reporting that the physical install address differs from the work order."],
    ["Why is recording the exact service address so important for this program?",
     "A customer asks at install whether they get the enhanced Tribal rate. What do you say/do?",
     "Within how many business days must an address change reach NLAD?",
     "Are you the person who decides a customer’s eligibility? Who is?",
     "What do you do if the physical address differs from the work order?"]
)

module(
    "5.8 Supervisors",
    ["Ensure everyone on your team has completed training and passed their knowledge check "
     "(certification, Section 9).",
     "Monitor calls/interactions for any use of prohibited statements and coach immediately.",
     "Ensure enrollment reps have RAD Rep IDs before enrolling (SR-6.6) and that NV-before-enrollment is "
     "followed (SR-3.1).",
     "Reinforce funding-stream separation and record-retention discipline in daily operations "
     "(SR-10.2, SR-6.11)."],
    ["You are accountable for your team saying the SAME accurate thing every time (Section 2).",
     "No enrollment without National Verifier approval; no enhanced credit without a verified address "
     "(SR-3.1, SR-4.2).",
     "Escalate systemic issues (recurring prohibited statements, address-verification gaps) to Compliance."],
    ["Letting a ‘close the sale’ culture tolerate over-promising eligibility.",
     "Signing off certification without an actual passed knowledge check.",
     "Not escalating a repeated compliance pattern to Compliance Staff."],
    ["What are you accountable for regarding your team’s customer statements?",
     "What two gates must never be skipped (before enrollment; before enhanced credit)?",
     "When do you escalate to Compliance rather than coach in-team?",
     "What must a rep have before enrolling any subscriber?",
     "How do you verify a team member is trained — attendance, or a passed check?"]
)

module(
    "5.9 Compliance Staff",
    ["Own the accuracy of every customer-facing statement and script; approve Lifeline marketing copy "
     "before publication.",
     "Maintain the written determination on whether ANY Lumbee land currently satisfies §54.400(e) / has "
     "a §54.412 designation — default answer today is NO (SR-5.5, Open Issue #1).",
     "Own National Verifier / NLAD discipline, recertification (60-day window, SR-3.3), de-enrollment "
     "(SR-3.5), and record retention (SR-6.11).",
     "Run per-address Tribal-lands verification governance and the annual FCC Form 555/481 obligations "
     "(SR-6.9, SR-6.10)."],
    ["The net rule to enforce everywhere: membership + four-county residence ≠ enhanced Tribal; "
     "enhanced requires a verified on-Tribal-lands address (SR-5.6).",
     "Set enhanced-Tribal subscriber count to ZERO until a written USAC/legal determination confirms "
     "qualifying lands (SR-5.5, Open Issue #1).",
     "Keep the four funding streams separated and grant characterization lawful (SR-10.1, SR-10.2)."],
    ["Allowing an enhanced claim before a documented §54.400(e)/§54.412 determination (SR-5.5).",
     "Letting marketing publish any prohibited statement (Section 2).",
     "Missing a recertification (60-day) or de-enrollment trigger (SR-3.3, SR-3.5)."],
    ["What is the current documented answer on whether Lumbee land qualifies under §54.400(e)?",
     "Until that determination changes, what enhanced-Tribal subscriber count do we assume?",
     "What is the recertification response window before de-enrollment?",
     "Which annual FCC forms cover the Lifeline certification and carrier annual report?",
     "State the one-sentence net rule this whole program encodes."]
)

# =====================================================================
# 6. HANDLING COMMON QUESTIONS / OBJECTIONS
# =====================================================================
h1(doc, "6. Handling Common Customer Questions & Objections")
para(doc, "Use these approved scripts verbatim or close to it. They keep every employee on the same "
          "accurate message.")

h3(doc, "“I’m Lumbee — do I get $34.25?”")
callout(doc,
    "“Congratulations on the Tribe’s recognition — that’s wonderful. On Lifeline, "
    "though, the higher $34.25 amount isn’t based on being Lumbee. It’s based on whether your "
    "home address is on federally designated Tribal lands, which the government checks address by "
    "address. Right now that higher amount isn’t available just for living in the four counties. "
    "What I can do is check whether you qualify for standard Lifeline at $9.25 — can we start "
    "there?”  (SR-5.6, SR-4.2)", kind="note")

h3(doc, "“I’m a senior — I automatically qualify, right?”")
callout(doc,
    "“Lifeline actually isn’t based on age — it’s based on household income or being "
    "in a program like Medicaid, SNAP, SSI, federal housing assistance, or the Veterans Pension. Plenty "
    "of seniors qualify, so let’s check: are you in any of those programs, or is your household "
    "income at or below the Lifeline limit? Then the federal Verifier confirms it before we enroll "
    "you.”  (SR-1.4, SR-1.6, SR-3.1)", kind="note")

h3(doc, "“Can I keep my other Lifeline phone AND this?”")
callout(doc,
    "“Lifeline is one benefit per household, so you can’t have two at once. But you don’t "
    "have to lose anything — with your consent we can TRANSFER your existing Lifeline benefit over "
    "to us. Would you like me to walk you through the transfer?”  (SR-1.8, SR-3.6)", kind="note")

h3(doc, "“Is this ACP?”")
callout(doc,
    "“Good question — no. The ACP program ended. This is Lifeline, a separate federal program "
    "that’s still active, with its own rules and its own benefit amount. Let’s go through the "
    "Lifeline requirements so we get you the right answer.”  (SR-8.6)", kind="note")

# =====================================================================
# 7. PRIVACY & DATA HANDLING
# =====================================================================
h1(doc, "7. Privacy & Data Handling for Employees")
para(doc, "Lifeline enrollment involves sensitive personal information (identity, income, program "
          "participation, and sometimes tribal-roll status). Handle it with care:")
bullet(doc, "Never place full Social Security Numbers, eligibility documents, or tribal-roll information "
            "in unsecured fields — no free-text notes, chat, email bodies, or shared spreadsheets.")
bullet(doc, "Collect only what is needed for the National Verifier check, and only through approved, "
            "secure systems.")
bullet(doc, "Obtain the customer’s consent before collecting eligibility information and before any "
            "benefit transfer (SR-3.6).")
bullet(doc, "Access is role-based: view only the customer data your role requires. Do not look up, share, "
            "or discuss customer records outside your task.")
bullet(doc, "Retain eligibility records only in the approved system per the retention rule (SR-6.11); "
            "never keep private copies.")
callout(doc, "If you believe sensitive data (an SSN, an eligibility document, tribal-roll info) has been "
             "entered into an unsecured field or exposed, stop and report it to Compliance immediately. "
             "Do not attempt to quietly delete or fix it yourself.", kind="warn")

# =====================================================================
# 8. ESCALATION PATHS
# =====================================================================
h1(doc, "8. Escalation Paths")
para(doc, "When in doubt, route it. It is always better to pause and escalate than to give a customer an "
          "inaccurate answer.")
table(doc,
      ["Situation", "Route to", "Why"],
      [["Any question about enhanced Tribal eligibility, §54.400(e)/§54.412 status, or whether a "
        "four-county address qualifies",
        "Compliance Staff (and Tribe Liaison for membership/outreach questions)",
        "The enhanced determination is a legal/USAC matter with a working answer of NO today (SR-5.5)."],
       ["A Lumbee-membership or Tribe-funded / outreach benefit question",
        "Tribe Liaison (via Compliance)",
        "Membership benefits are separate from federal Lifeline and Tribe-funded (SR-5.6)."],
       ["A customer disputes a National Verifier result or a de-enrollment",
        "Compliance Staff",
        "Recertification (60-day) and de-enrollment are regulated processes (SR-3.3, SR-3.5)."],
       ["Suspected prohibited statement was made, or appears in copy",
        "Supervisor → Compliance Staff",
        "Requires correction and, if published, remediation (Section 2)."],
       ["Suspected exposure of SSN / eligibility docs / tribal-roll data",
        "Compliance Staff (immediately)",
        "Privacy incident handling; do not self-remediate (Section 7)."],
       ["Pricing, taxability (‘plus tax’), or which plan components are taxable",
        "Billing → Finance / Tax advisor",
        "Taxability is unresolved for several components [CONFIRM] (SR-9.9)."]],
      widths=[3.0, 2.0, 2.2], small=True)

# =====================================================================
# 9. CERTIFICATION OF COMPLETION
# =====================================================================
h1(doc, "9. Certification of Completion")
para(doc, "Every employee must complete Sections 1–4 and their role module (Section 5), pass the "
          "role knowledge check, and sign below. Supervisors verify a PASSED check — not merely "
          "attendance — before sign-off. Compliance retains completed certifications.")
callout(doc, "Passing standard: a score of at least 80% (4 of 5) on the role knowledge check, AND zero "
             "incorrect answers on any prohibited-statement item. Anyone who misses a prohibited-statement "
             "question must be re-trained on Section 2 and re-tested before taking customer contact.",
        kind="note")
table(doc,
      ["Employee (print + sign)", "Role / module", "Date", "Trainer", "Score (of 5)"],
      [["", "", "", "", ""],
       ["", "", "", "", ""],
       ["", "", "", "", ""],
       ["", "", "", "", ""],
       ["", "", "", "", ""],
       ["", "", "", "", ""]],
      widths=[2.4, 1.7, 0.9, 1.5, 0.9])
para(doc, "By signing, the employee affirms they understand the one non-negotiable rule (Section 1), will "
          "never use the prohibited statements (Section 2), and will route uncertain situations per the "
          "escalation paths (Section 8).", italic=True, size=9.5, color=GREY)

# =====================================================================
# FOOTER / REVISION HISTORY
# =====================================================================
footer_revhist(doc)

doc.save(OUT)

# reload to confirm integrity
from docx import Document
_ = Document(OUT)
print("OK 10")
