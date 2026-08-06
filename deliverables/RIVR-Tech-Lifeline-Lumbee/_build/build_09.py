import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from docx_helpers import *

OUT = "/home/user/claude-skills/deliverables/RIVR-Tech-Lifeline-Lumbee/09_Customer_Communications_Toolkit.docx"
DRAFT = "[DRAFT — legal/compliance review required]"

doc = new_doc()

cover(
    doc,
    title="Customer Communications Toolkit",
    subtitle="Ready-to-adapt draft copy for the RIVR Tech Lifeline & Lumbee Broadband Affordability Initiative",
    deliverable_no="09 — Customer Communications Toolkit",
    owner="Marketing + Compliance",
    approvers="________________________  (Marketing lead / Compliance counsel / date)",
    version="v0.1 — DRAFT",
    extra=("EVERY piece in this toolkit is DRAFT copy and must clear legal/compliance review before any "
           "public use. Do NOT publish until the NCUC ETC order is final and USAC onboarding is complete. "
           "RIVR prices appear as bracketed placeholders — insert only confirmed figures from the RIVR "
           "price sheet. Never advertise ACP as active (it ended June 1, 2024). Never advertise "
           "\"plus tax\" on broadband (non-taxable per ITFA; other components pending tax review — SR-9.9)."),
)

toc(doc)

# ---------------------------------------------------------------------------
h1(doc, "How to use this toolkit")
para(doc, "This document contains actual draft customer-facing copy — website, FAQ, letters, notices, "
     "email/SMS/social, print, and call-center scripts — for the RIVR Tech Lifeline program. Each piece "
     "is written to be lifted, lightly adapted, and sent, but ONLY after the review gate below.")
bullet(doc, "Owner: Marketing + Compliance (joint). Marketing drafts; Compliance signs off before release.")
bullet(doc, "Every piece is marked \"" + DRAFT + "\" and must clear legal/compliance review before publication.")
bullet(doc, "Bracketed placeholders like \"[$XX.XX — confirm from RIVR price sheet]\" must be replaced with "
       "confirmed figures. Do not invent prices.")
bullet(doc, "Source basis: 00_Regulatory_Source_Register.md (\"SR-x.y\" refs). Re-verify every figure against "
       "the live cited source before go-live.")
callout(doc, "Read Section 1 (Compliance guardrails) before editing any other piece. The prohibited claims "
        "there apply to 100% of customer communications, in every channel, with no exceptions.", kind="stop")

# ---------------------------------------------------------------------------
h1(doc, "1. Compliance guardrails for ALL customer communications")
para(doc, DRAFT, italic=True, color=RED)
callout(doc, "These guardrails are mandatory for every customer-facing communication in every channel "
        "(web, print, email, SMS, social, scripts, letters). If a piece cannot be written without one of "
        "the prohibited claims below, it must not be sent. When in doubt, route to Compliance.", kind="warn")

h3(doc, "Prohibited claims — never state, imply, or suggest any of the following")
bullet(doc, "\"Every Lumbee member receives $34.25.\" — FALSE. The enhanced $25 add-on (total up to "
       "$34.25/mo) is tied to living on qualifying Tribal lands, not to tribal membership (SR-4.2, SR-5.6).")
bullet(doc, "\"All four counties are Tribal lands.\" — FALSE. Robeson, Cumberland, Hoke, and Scotland form a "
       "service delivery area, which is NOT \"Tribal lands\" under 47 C.F.R. §54.400(e) (SR-5.4, SR-5.5).")
bullet(doc, "\"All seniors automatically qualify for Lifeline.\" — FALSE. Age alone does not qualify anyone. "
       "The customer must meet income OR a program-based test and pass National Verifier (SR-1.4–1.6, SR-3.1).")
bullet(doc, "\"The Tribe guarantees approval.\" — FALSE. Eligibility is decided by the USAC National Verifier, "
       "not by RIVR and not by the Tribe (SR-3.1).")
bullet(doc, "\"You can get multiple Lifeline benefits.\" — FALSE. One Lifeline benefit per household (SR-1.8).")
bullet(doc, "\"This is the same as ACP.\" — FALSE. The Affordable Connectivity Program ended June 1, 2024. "
       "Lifeline is a separate, ongoing program. Never present ACP as available (SR-8.6).")

h3(doc, "Additional standing rules")
bullet(doc, "Never advertise \"plus tax\" on the broadband plan. Broadband access is non-taxable (ITFA, "
       "SR-9.1); taxability of equipment/voice/install is pending tax-advisor review (SR-9.9).")
bullet(doc, "Do not market RIVR as an approved Lifeline provider until the final NCUC ETC order issues and "
       "USAC onboarding is complete (SR-7.4).")
bullet(doc, "Enhanced Tribal benefit language must always tie the $25 to a verified ADDRESS on qualifying "
       "Tribal lands, checked with the USAC Tribal Lands Verification Tool — never to membership (SR-4.4).")
bullet(doc, "State amounts as \"up to\" ($9.25 standard; up to $34.25 where the address qualifies). "
       "Never promise a specific dollar credit before National Verifier approval.")
bullet(doc, "Every eligibility statement must point to the National Verifier as the decision-maker.")

# ---------------------------------------------------------------------------
h1(doc, "2. Website landing page copy")
para(doc, DRAFT, italic=True, color=RED)

h3(doc, "Headline")
para(doc, "Affordable high-speed internet for those who qualify — powered by federal Lifeline.", bold=True)
h3(doc, "Subhead")
para(doc, "RIVR Tech is working to bring the federal Lifeline discount to eligible households across our "
     "service area. Standard Lifeline saves you up to $9.25 a month on your internet bill. See if you may "
     "qualify.")
h3(doc, "Value proposition 1 — Real savings")
para(doc, "Up to $9.25 off your monthly internet through the federal Lifeline program — and up to $34.25 "
     "total where your home address is on qualifying Tribal lands (verified per address).")
h3(doc, "Value proposition 2 — Fast, symmetrical fiber")
para(doc, "Our proposed Senior 100/100 plan delivers 100 Mbps download AND 100 Mbps upload, with unlimited "
     "data and no caps — plenty for video calls, streaming, and telehealth.")
h3(doc, "Value proposition 3 — Local support")
para(doc, "Enroll with a local RIVR Tech team in Pembroke. We help you check eligibility, gather documents, "
     "and apply through the official National Verifier.")
h3(doc, "Eligibility teaser")
para(doc, "You may qualify if your household income is at or below 135% of the Federal Poverty Guidelines, "
     "OR if you take part in Medicaid, SNAP, SSI, Federal Public Housing Assistance, or the Veterans & "
     "Survivors Pension Benefit. One benefit per household. Approval is determined by the National Verifier.")
h3(doc, "Call to action")
para(doc, "Check my eligibility  →   Call (910) 843-4131 or visit us at 6090 NC Hwy 711, Pembroke, NC 28372.",
     bold=True)
callout(doc, "Launch gate: this page may not go live until the NCUC ETC order is final (SR-7.4). Insert "
        "confirmed plan price from the RIVR price sheet before publishing. No \"plus tax\" on broadband.",
        kind="warn")

# ---------------------------------------------------------------------------
h1(doc, "3. Frequently Asked Questions")
para(doc, DRAFT, italic=True, color=RED)

faqs = [
    ("What is Lifeline?",
     "Lifeline is a federal program that lowers the monthly cost of phone or internet service for "
     "eligible low-income households. RIVR Tech is applying to offer the Lifeline internet discount. The "
     "program is run by the federal government and administered by USAC; RIVR passes the discount through "
     "to your bill."),
    ("How much is the discount — $9.25 or $34.25?",
     "The standard Lifeline discount is up to $9.25 per month. An enhanced benefit of up to $34.25 per "
     "month total is available ONLY when your home address is located on qualifying Tribal lands. The "
     "enhanced amount is based on WHERE YOU LIVE — a specific address that qualifies — not on tribal "
     "membership. We check each address using the official USAC Tribal Lands Verification Tool."),
    ("Do I get the $34.25 because I'm an enrolled Lumbee member?",
     "No — not by membership alone. The enhanced $25 add-on requires your principal residence to be on "
     "qualifying Tribal lands as defined by federal rules, verified address by address. Lumbee membership "
     "or living in Robeson, Cumberland, Hoke, or Scotland County does not by itself qualify an address. "
     "Today, most local addresses may not qualify for the enhanced amount, but you may still qualify for "
     "the standard $9.25 discount."),
    ("How do I qualify?",
     "Two ways. (1) Income: your household income is at or below 135% of the Federal Poverty Guidelines. "
     "(2) Programs: someone in your household takes part in Medicaid, SNAP (food stamps), SSI, Federal "
     "Public Housing Assistance, or the Veterans & Survivors Pension Benefit. Either path can qualify you. "
     "Final approval is made by the National Verifier."),
    ("Can more than one person in my home get Lifeline?",
     "No. Lifeline is limited to one benefit per household. A \"household\" is everyone living together at "
     "one address who shares income and expenses. If two separate households share one address, each may "
     "apply using the one-per-household worksheet."),
    ("Is the Senior 100/100 plan right for me?",
     "The Senior 100/100 plan is designed to be an affordable, lower-cost option with fast symmetrical "
     "speed (100 Mbps down / 100 Mbps up) and unlimited data. It is open to any qualifying household — you "
     "do not have to be a senior to ask about it, and being a senior does not by itself make you eligible "
     "for Lifeline. Eligibility still depends on income or program participation."),
    ("Do I need to be Lumbee to sign up?",
     "No. Lifeline is a federal program open to any eligible household regardless of tribal membership. "
     "Your eligibility depends on your income or the assistance programs you take part in — not on whether "
     "you are a member of any tribe."),
    ("What does it cost?",
     "The Senior 100/100 plan is expected to be [$XX.XX — confirm from RIVR price sheet] per month before "
     "the Lifeline discount. After the standard Lifeline discount of up to $9.25, your out-of-pocket cost "
     "is lower. Equipment and voice options, if any, are billed separately — ask us for current pricing. "
     "Internet access is not taxed."),
    ("How do I apply?",
     "You can apply three ways: online through the National Verifier, by phone, or in person with our "
     "team in Pembroke. We help you complete the application and check your eligibility. See the "
     "application instructions for step-by-step details."),
    ("What is the National Verifier?",
     "The National Verifier is the official federal system (run by USAC) that confirms whether you qualify "
     "for Lifeline. It checks your identity, address, and eligibility, and makes sure no household gets "
     "more than one benefit. RIVR cannot enroll you until the National Verifier approves your application."),
    ("Do I have to re-apply every year?",
     "Yes. Lifeline requires annual recertification to confirm you still qualify. If the automatic check "
     "cannot confirm your eligibility, you will get a notice and have 60 days to respond. If you do not "
     "respond in time, your benefit ends. We will remind you before your deadline."),
    ("What if I move?",
     "Tell us right away if you change your address. Your address affects your service and can affect "
     "whether you qualify for the enhanced Tribal benefit (which depends on the home being on qualifying "
     "Tribal lands). We must update the federal database within 10 business days of a change."),
    ("Is this the Affordable Connectivity Program (ACP)?",
     "No. The Affordable Connectivity Program (ACP) ended on June 1, 2024, and is no longer available. "
     "Lifeline is a separate, ongoing federal program with its own rules and discount. If you had ACP "
     "before, that benefit has ended — but you may still qualify for Lifeline."),
    ("Can I transfer my Lifeline benefit from another provider?",
     "Yes. If you already receive Lifeline from another company, you can transfer the benefit to RIVR with "
     "your consent. Only one provider can receive the benefit for you at a time. We will explain the "
     "transfer and get your permission before we make any change."),
]
for q, a in faqs:
    h3(doc, "Q: " + q)
    para(doc, "A: " + a)

# ---------------------------------------------------------------------------
h1(doc, "4. Eligibility explainer")
para(doc, DRAFT, italic=True, color=RED)
para(doc, "There are three separate things the program checks. Think of them as three doors — you need to "
     "pass all three to be enrolled.")

h3(doc, "Test 1 — Are you eligible? (income OR program)")
para(doc, "You qualify on eligibility if EITHER is true:")
bullet(doc, "Income: your household income is at or below 135% of the Federal Poverty Guidelines. "
       "Approximate 2026 annual limits (48 states/DC — confirm against the live USAC figures, SR-1.5): "
       "1 person about $21,546; 2 people about $29,214; 3 people about $36,882; 4 people about $44,550 "
       "(add for each additional person; higher in AK/HI).")
bullet(doc, "Programs: someone in the household takes part in Medicaid, SNAP, SSI, Federal Public Housing "
       "Assistance, or the Veterans & Survivors Pension Benefit. Certain Tribal programs (Bureau of Indian "
       "Affairs General Assistance, Tribal TANF, income-qualifying Head Start, FDPIR) also qualify you for "
       "the STANDARD benefit — but they do not by themselves establish Tribal-lands residence for the "
       "enhanced benefit (SR-1.7).")

h3(doc, "Test 2 — One per household")
para(doc, "Only one Lifeline benefit is allowed per household. A household is everyone living together at "
     "one address who shares income and expenses. If two independent households share an address, each may "
     "still apply using the one-per-household worksheet (SR-1.8).")

h3(doc, "Test 3 — National Verifier approval")
para(doc, "The federal National Verifier confirms your identity, address, and eligibility, and checks for "
     "duplicates. RIVR cannot enroll you until the National Verifier returns an approved result (SR-3.1).")

para(doc, "A separate, address-only question decides the enhanced amount: is your home on qualifying Tribal "
     "lands? See Section 6.", italic=True)

# ---------------------------------------------------------------------------
h1(doc, "5. Application instructions")
para(doc, DRAFT, italic=True, color=RED)

h3(doc, "Before you start — have these ready")
bullet(doc, "A photo ID and your date of birth (for identity verification).")
bullet(doc, "Your service address.")
bullet(doc, "Proof of a qualifying program (e.g., Medicaid or SNAP card/letter) OR proof of income "
       "(e.g., prior-year tax return, three consecutive pay stubs, or a benefit statement).")

h3(doc, "Option A — Apply online")
numbered(doc, "Go to the official National Verifier at CheckLifeline.org (the federal application site).")
numbered(doc, "Create an account and complete the eligibility application.")
numbered(doc, "Upload your documents if asked.")
numbered(doc, "Once approved, contact RIVR Tech to activate service and apply the discount to your bill.")

h3(doc, "Option B — Apply by phone")
numbered(doc, "Call RIVR Tech at (910) 843-4131.")
numbered(doc, "A representative will walk you through the National Verifier application over the phone.")
numbered(doc, "Have your documents nearby in case verification needs them.")

h3(doc, "Option C — Apply in person")
numbered(doc, "Visit RIVR Tech at 6090 NC Hwy 711, Pembroke, NC 28372.")
numbered(doc, "Bring your ID and proof of eligibility.")
numbered(doc, "Our team helps you complete the National Verifier application and, once approved, sets up "
         "your discounted service.")
callout(doc, "RIVR staff must be RAD-registered (Rep ID) before enrolling any subscriber, and may only "
        "enroll after an approved National Verifier result (SR-6.6, SR-3.1). Internal note — not customer copy.",
        kind="note")

# ---------------------------------------------------------------------------
h1(doc, "6. Tribal-lands eligibility — how the enhanced benefit works")
para(doc, DRAFT, italic=True, color=RED)
callout(doc, "This is the highest-risk topic in the whole program. The copy below is written carefully to "
        "avoid the prohibited claims in Section 1. Do not paraphrase in a way that ties the $25 to "
        "membership or to the four counties.", kind="warn")

para(doc, "The federal Lifeline program offers an enhanced benefit of up to an extra $25 per month — up to "
     "$34.25 total — for people who live on qualifying Tribal lands. Here is what that means in plain terms:")
bullet(doc, "The enhanced benefit is based on WHERE YOU LIVE, not on who you are. Your principal home "
       "address must be on land that federal rules count as \"Tribal lands.\"")
bullet(doc, "Being an enrolled member of the Lumbee Tribe — or any tribe — does not by itself qualify your "
       "address for the enhanced benefit.")
bullet(doc, "Living in Robeson, Cumberland, Hoke, or Scotland County does not by itself make an address "
       "qualify. These counties are a service delivery area, which is not the same as \"Tribal lands\" "
       "under the federal rule.")
bullet(doc, "We check each specific address using the official USAC Tribal Lands Verification Tool. The "
       "federal database only flags an address for the enhanced benefit when that address is verified.")
bullet(doc, "As things stand today, many — possibly most — local addresses may not qualify for the enhanced "
       "amount, because the qualifying-lands rules turn on federally designated reservation, trust, or "
       "FCC-designated land, which may not yet apply here.")
bullet(doc, "This can change. If land is taken into trust or the FCC designates additional qualifying "
       "lands in the future, more addresses could qualify. We will re-check when that happens.")
para(doc, "Bottom line: everyone eligible can get the standard discount of up to $9.25. The enhanced amount "
     "is added only for addresses the USAC tool verifies as qualifying Tribal lands. We will tell you "
     "honestly what your address qualifies for.", bold=True)

# ---------------------------------------------------------------------------
h1(doc, "7. Senior 100/100 plan explanation")
para(doc, DRAFT, italic=True, color=RED)
para(doc, "The Senior 100/100 plan is a new, affordable fiber internet tier designed for households that "
     "want a dependable connection at a lower price.")
bullet(doc, "Price: target [$10 — confirm from RIVR price sheet] per month before any Lifeline discount.")
bullet(doc, "Speed: 100 Mbps download AND 100 Mbps upload — symmetrical, so uploads are as fast as "
       "downloads. Great for video calls, telehealth, and sharing photos.")
bullet(doc, "Data: unlimited, with no caps and no overage charges.")
bullet(doc, "Who it's for: any qualifying household that wants an affordable plan. You do not have to be a "
       "senior to ask about it, and being a senior does not by itself make you eligible for Lifeline — "
       "eligibility still depends on income or program participation.")
bullet(doc, "Equipment: Wi-Fi router/mesh options may be available for an additional monthly charge "
       "[confirm equipment pricing and policy from RIVR — SR-8.4].")
bullet(doc, "Voice: an optional home phone add-on may be available [confirm voice pricing from RIVR — SR-8.5].")
para(doc, "Internet access is not taxed. We do not advertise \"plus tax\" on this plan. If any equipment or "
     "voice add-ons are taxable, we show that separately once confirmed (SR-9.9).", italic=True)

# ---------------------------------------------------------------------------
h1(doc, "8. Bill insert (short)")
para(doc, DRAFT, italic=True, color=RED)
callout(doc, "You may be able to lower your internet bill. RIVR Tech is bringing the federal Lifeline "
        "discount to eligible households — up to $9.25 off each month (more where your address qualifies "
        "as Tribal lands). Qualify by income or by a program like Medicaid, SNAP, or SSI. One benefit per "
        "household; approval by the National Verifier. Call (910) 843-4131 to see if you qualify.",
        kind="note")

# ---------------------------------------------------------------------------
h1(doc, "9. New-customer enrollment letter")
para(doc, DRAFT, italic=True, color=RED)
para(doc, "Dear [Customer name],")
para(doc, "Welcome to RIVR Tech, and thank you for choosing us for your internet service.")
para(doc, "We are pleased to confirm that your Lifeline discount has been applied to your account following "
     "your approval by the federal National Verifier. Here is a summary of your service:")
bullet(doc, "Plan: [plan name — e.g., Senior 100/100]")
bullet(doc, "Monthly price before discount: [$XX.XX — confirm from RIVR price sheet]")
bullet(doc, "Lifeline discount applied: up to $9.25 per month (the enhanced Tribal amount applies only if "
       "your address is verified as qualifying Tribal lands)")
bullet(doc, "Your estimated monthly total: [$XX.XX — confirm]")
para(doc, "A few important things to know:")
bullet(doc, "Lifeline is limited to one benefit per household.")
bullet(doc, "You must recertify once a year to keep your discount. We will remind you before your deadline.")
bullet(doc, "Tell us right away if you move or if your household changes — your address can affect your "
       "eligibility and your benefit amount.")
para(doc, "If you have any questions, call us at (910) 843-4131 or visit 6090 NC Hwy 711, Pembroke, NC "
     "28372. We're glad to have you with us.")
para(doc, "Sincerely,")
para(doc, "The RIVR Tech Team")

# ---------------------------------------------------------------------------
h1(doc, "10. Existing-customer migration letter")
para(doc, DRAFT, italic=True, color=RED)
para(doc, "Dear [Customer name],")
para(doc, "Good news — RIVR Tech now offers the federal Lifeline discount, and as one of our valued "
     "customers you may be able to lower your monthly internet bill.")
para(doc, "Lifeline can reduce your bill by up to $9.25 per month. A larger discount (up to $34.25 total) "
     "is available only if your home address is verified as being on qualifying Tribal lands — this is "
     "based on your address, not on tribal membership, and we check it with an official federal tool.")
para(doc, "You may qualify if your household income is at or below 135% of the Federal Poverty Guidelines, "
     "or if someone in your home takes part in Medicaid, SNAP, SSI, Federal Public Housing Assistance, or "
     "the Veterans & Survivors Pension Benefit. Only one benefit is allowed per household, and final "
     "approval comes from the National Verifier.")
para(doc, "To see if you qualify and switch your account to a Lifeline-discounted plan, call us at "
     "(910) 843-4131 or stop by our Pembroke office. We'll walk you through the short application.")
para(doc, "Note: The Affordable Connectivity Program (ACP) that some customers used in the past ended on "
     "June 1, 2024. Lifeline is a separate program that is still available.")
para(doc, "Sincerely,")
para(doc, "The RIVR Tech Team")

# ---------------------------------------------------------------------------
h1(doc, "11. Approval notice")
para(doc, DRAFT, italic=True, color=RED)
para(doc, "Dear [Customer name],")
para(doc, "Congratulations — your Lifeline application has been approved by the National Verifier.")
para(doc, "Your federal Lifeline discount of up to $9.25 per month has been applied to your RIVR Tech "
     "account, effective [date]. [If applicable: Because your address was verified as qualifying Tribal "
     "lands, your enhanced discount of up to $34.25 total has been applied.]")
bullet(doc, "Plan: [plan name]")
bullet(doc, "Discount applied: [$X.XX] per month")
bullet(doc, "New estimated monthly total: [$XX.XX — confirm]")
para(doc, "Please remember: your benefit must be recertified every year, and you must let us know within a "
     "few days if you move or your household changes. One Lifeline benefit is allowed per household.")
para(doc, "Questions? Call (910) 843-4131. Thank you for being a RIVR Tech customer.")
para(doc, "Sincerely,")
para(doc, "The RIVR Tech Team")

# ---------------------------------------------------------------------------
h1(doc, "12. Denial / incomplete-application notice")
para(doc, DRAFT, italic=True, color=RED)
para(doc, "Dear [Customer name],")
para(doc, "Thank you for applying for the Lifeline discount. We are writing because your application could "
     "not be approved at this time. This decision was made by the federal National Verifier, based on the "
     "following reason:")
bullet(doc, "[ ] We could not confirm your eligibility (income or program participation).")
bullet(doc, "[ ] We could not verify your identity.")
bullet(doc, "[ ] We could not verify your address.")
bullet(doc, "[ ] Your application was incomplete or missing documents.")
bullet(doc, "[ ] A Lifeline benefit already exists for your household.")
para(doc, "What you can do next:")
numbered(doc, "If a document was missing, send us the item(s) noted above and we will resubmit your "
         "application.")
numbered(doc, "If you think this decision is wrong, you have the right to ask for a review. You may also "
         "have a family member, friend, or advocate act as your representative — just let us know in "
         "writing that you give them permission to help.")
numbered(doc, "If you qualify through a different program or your circumstances change, you can reapply at "
         "any time.")
para(doc, "We're here to help. Call us at (910) 843-4131 or visit our Pembroke office and we'll go through "
     "your options together. Being denied for one reason does not mean you can't qualify another way.")
para(doc, "Sincerely,")
para(doc, "The RIVR Tech Team")

# ---------------------------------------------------------------------------
h1(doc, "13. Recertification reminder (60-day window)")
para(doc, DRAFT, italic=True, color=RED)
para(doc, "Dear [Customer name],")
para(doc, "It's time to recertify your Lifeline benefit. To keep your monthly discount, the federal program "
     "must confirm once a year that you still qualify.")
para(doc, "Your deadline to respond is [date] — that is 60 days from the date of this notice. If we do not "
     "hear from you by then, your Lifeline discount will end and your bill will return to the full price.")
para(doc, "How to recertify:")
numbered(doc, "Recertify online at the National Verifier (CheckLifeline.org), OR")
numbered(doc, "Call us at (910) 843-4131 and we'll help you complete it, OR")
numbered(doc, "Visit our Pembroke office with any documents that show you still qualify.")
para(doc, "Recertifying takes only a few minutes. Please don't wait — once the deadline passes, you would "
     "have to reapply from the start.")
para(doc, "Sincerely,")
para(doc, "The RIVR Tech Team")

# ---------------------------------------------------------------------------
h1(doc, "14. De-enrollment notice")
para(doc, DRAFT, italic=True, color=RED)
para(doc, "Dear [Customer name],")
para(doc, "We are writing to let you know that your federal Lifeline discount has ended, effective [date], "
     "for the following reason:")
bullet(doc, "[ ] You did not recertify by your deadline.")
bullet(doc, "[ ] The program determined the household no longer qualifies.")
bullet(doc, "[ ] A duplicate benefit or one-per-household issue was found.")
bullet(doc, "[ ] You asked us to remove the benefit.")
para(doc, "What this means: your internet service continues, but your bill will return to the standard "
     "price of [$XX.XX — confirm from RIVR price sheet] per month starting [date].")
para(doc, "If you believe this is a mistake, or if your situation has changed and you now qualify, you can "
     "reapply at any time. Call us at (910) 843-4131 or visit our Pembroke office and we'll help you "
     "restart the application.")
para(doc, "We value you as a customer and want to keep your service affordable. Please reach out — we're "
     "happy to review your options.")
para(doc, "Sincerely,")
para(doc, "The RIVR Tech Team")

# ---------------------------------------------------------------------------
h1(doc, "15. Address-change notice")
para(doc, DRAFT, italic=True, color=RED)
para(doc, "Dear [Customer name],")
para(doc, "Thank you for letting us know you're moving. We've updated your RIVR Tech account with your new "
     "service address: [new address].")
para(doc, "Why your address matters for Lifeline:")
bullet(doc, "Lifeline benefits are tied to your home address. We are required to update the federal "
       "database within 10 business days of a change.")
bullet(doc, "Your address also decides whether you qualify for the enhanced Tribal benefit (up to $34.25 "
       "total). That benefit applies only when your home is on qualifying Tribal lands, verified with the "
       "official USAC tool. A move may add, remove, or leave unchanged the enhanced amount — we will "
       "re-check your new address and tell you the result.")
bullet(doc, "Your standard discount of up to $9.25 continues as long as you remain eligible.")
para(doc, "If you have questions about your discount at the new address, call us at (910) 843-4131.")
para(doc, "Sincerely,")
para(doc, "The RIVR Tech Team")

# ---------------------------------------------------------------------------
h1(doc, "16. Benefit-transfer disclosure and consent")
para(doc, DRAFT, italic=True, color=RED)
para(doc, "If you already receive a Lifeline benefit from another company, you can transfer it to RIVR "
     "Tech. Federal rules require your informed consent before we do this. Please read and confirm:")
bullet(doc, "I understand that Lifeline is limited to one benefit, and that transferring my benefit to "
       "RIVR Tech will end my Lifeline benefit with my current provider.")
bullet(doc, "I understand that only one company can receive the Lifeline benefit on my behalf at a time.")
bullet(doc, "I understand that this transfer applies to my Lifeline benefit and I am choosing to receive "
       "it through RIVR Tech going forward.")
bullet(doc, "I understand I can transfer my benefit to a different provider in the future if I choose.")
bullet(doc, "I give RIVR Tech permission to complete this benefit transfer in the federal database on my "
       "behalf.")
para(doc, "Customer signature: ______________________________   Date: ______________", bold=True)
para(doc, "Consent may also be captured by phone or electronically per USAC requirements. Retain the "
     "consent record with the subscriber's file (SR-3.6).", italic=True, size=9, color=GREY)

# ---------------------------------------------------------------------------
h1(doc, "17. Short-form and multichannel copy")
para(doc, DRAFT, italic=True, color=RED)

h2(doc, "17a. Email (short)")
para(doc, "Subject: You may qualify to lower your internet bill", bold=True)
para(doc, "Hi [First name],")
para(doc, "RIVR Tech is bringing the federal Lifeline discount to eligible households — up to $9.25 off "
     "your internet each month. You may qualify by income or through a program like Medicaid, SNAP, or "
     "SSI. One benefit per household; approval is made by the National Verifier.")
para(doc, "See if you qualify: call (910) 843-4131 or reply to this email. — The RIVR Tech Team")

h2(doc, "17b. SMS (160-character compliant)")
para(doc, "RIVR Tech: You may qualify for up to $9.25/mo off internet via federal Lifeline. Income or "
     "Medicaid/SNAP/SSI. 1 per household. Call 910-843-4131. Reply STOP to opt out", bold=True)
para(doc, "(Character count target: keep at or under 160. Reply STOP language required for compliance.)",
     italic=True, size=9, color=GREY)

h2(doc, "17c. Social media posts")
h3(doc, "Post 1 — Awareness")
para(doc, "Could your household save on internet? RIVR Tech is bringing the federal Lifeline discount to "
     "eligible households — up to $9.25/mo off. Qualify by income or programs like Medicaid, SNAP, or SSI. "
     "One benefit per household; the National Verifier decides eligibility. Call (910) 843-4131. "
     "#Lifeline #AffordableInternet")
h3(doc, "Post 2 — Myth-buster (address vs. membership)")
para(doc, "Setting the record straight: the enhanced Lifeline discount is based on WHERE YOU LIVE — a home "
     "address verified as qualifying Tribal lands — not on tribal membership. Everyone eligible can get "
     "the standard discount of up to $9.25/mo. We'll check your address honestly. Call (910) 843-4131.")
h3(doc, "Post 3 — Senior 100/100")
para(doc, "Fast, affordable fiber: our Senior 100/100 plan offers 100 Mbps up AND down with unlimited "
     "data. Open to any qualifying household. Ask about pairing it with the federal Lifeline discount. "
     "Eligibility depends on income or program participation — the National Verifier decides. "
     "Call (910) 843-4131.")

h2(doc, "17d. Printed flyer copy")
para(doc, "LOWER YOUR INTERNET BILL", bold=True, size=14, color=NAVY)
para(doc, "The federal Lifeline program — now coming to RIVR Tech", bold=True)
bullet(doc, "Save up to $9.25/month on internet (more where your address qualifies as Tribal lands)")
bullet(doc, "Qualify by income (135% of the Federal Poverty Guidelines) OR programs like Medicaid, SNAP, SSI")
bullet(doc, "Fast symmetrical fiber — ask about the affordable Senior 100/100 plan")
bullet(doc, "One benefit per household. Approval by the National Verifier.")
para(doc, "See if you qualify: (910) 843-4131  |  6090 NC Hwy 711, Pembroke, NC 28372  |  rivrtech.net",
     bold=True)
para(doc, "The Affordable Connectivity Program (ACP) ended June 1, 2024. Lifeline is a separate program.",
     italic=True, size=9, color=GREY)

h2(doc, "17e. Office signage copy")
para(doc, "ASK US ABOUT LIFELINE", bold=True, size=14, color=NAVY)
para(doc, "You may qualify to lower your internet bill.", bold=True)
para(doc, "Up to $9.25/month off through the federal Lifeline program. Qualify by income or by a program "
     "like Medicaid, SNAP, or SSI. One benefit per household. We'll help you apply through the National "
     "Verifier — no cost to ask.")
para(doc, "Speak with a RIVR Tech representative today.", bold=True)

# ---------------------------------------------------------------------------
h1(doc, "18. Call-center scripts")
para(doc, DRAFT, italic=True, color=RED)
callout(doc, "Scripts are for RIVR-trained, RAD-registered representatives. Never guarantee approval; the "
        "National Verifier decides. Never tie the enhanced $25 to membership or the four counties. Capture "
        "consent before any benefit transfer.", kind="warn")

h2(doc, "18a. Inbound interest script")
para(doc, "Rep: \"Thank you for calling RIVR Tech, this is [name]. I understand you're interested in the "
     "Lifeline discount — I'd be glad to help. Lifeline is a federal program that can lower your internet "
     "bill by up to $9.25 a month if your household qualifies. May I ask you a few quick questions to see "
     "if you might be eligible? There's no cost and no obligation.\"")
para(doc, "[If yes, proceed to the eligibility pre-screen. If the caller asks about a bigger discount, use "
     "the objection-handling script in 18c.]")
para(doc, "Rep (closing): \"Based on what you've told me, you may qualify. The final decision is made by the "
     "federal National Verifier. I can help you apply now over the phone, or you can visit our Pembroke "
     "office. Which works best for you?\"")

h2(doc, "18b. Eligibility pre-screen script")
para(doc, "Rep: \"I'll ask about two things — income or programs. You only need one to qualify.\"")
numbered(doc, "\"First, does anyone in your household take part in Medicaid, SNAP or food stamps, SSI, "
         "Federal Public Housing Assistance, or the Veterans and Survivors Pension?\" [If yes → likely "
         "program-eligible; note which.]")
numbered(doc, "\"If not, may I ask about household income? Lifeline is for households at or below 135% of "
         "the Federal Poverty Guidelines. For a household of [size], that's about [$ amount] per year.\" "
         "[Confirm against current USAC figures.]")
numbered(doc, "\"How many people live in your home and share income and expenses? Lifeline allows one "
         "benefit per household.\"")
numbered(doc, "\"Do you currently receive a Lifeline discount from another internet or phone company?\" "
         "[If yes → benefit-transfer script, 18d.]")
para(doc, "Rep (disclaimer): \"Everything you've shared points to possible eligibility, but I can't "
     "guarantee approval — that's up to the National Verifier. Let's start your application so they can "
     "confirm.\"")

h2(doc, "18c. Objection handling — \"I'm Lumbee, so do I get the $34.25?\"")
para(doc, "Caller: \"I'm an enrolled Lumbee member — that means I get the $34.25, right?\"")
para(doc, "Rep: \"That's a great question, and I want to give you an honest answer. The larger amount — up "
     "to $34.25 a month — is the enhanced Tribal benefit, and under federal rules it's based on WHERE YOU "
     "LIVE, not on tribal membership. Your home address has to be on land that the federal government "
     "counts as qualifying Tribal lands. We check each address using an official federal tool.\"")
para(doc, "Rep (continued): \"Being an enrolled Lumbee member, and living in Robeson, Cumberland, Hoke, or "
     "Scotland County, doesn't by itself qualify an address — those counties are a service area, which is "
     "different from Tribal lands under the rule. Honestly, many addresses in our area may not qualify for "
     "the enhanced amount today. That could change in the future if land is placed into trust or the FCC "
     "designates additional lands.\"")
para(doc, "Rep (reassure and redirect): \"Here's the good news: if you're eligible, you can still get the "
     "standard Lifeline discount of up to $9.25 a month. I'll check your specific address for the enhanced "
     "amount and tell you exactly what it qualifies for — no guessing. Would you like me to do that now?\"")

h2(doc, "18d. Benefit-transfer script")
para(doc, "Rep: \"Since you already receive Lifeline from another company, I can transfer that benefit to "
     "RIVR Tech — but only with your permission, and I need to make sure you understand a few things "
     "first.\"")
numbered(doc, "\"Lifeline is limited to one benefit. Transferring it to RIVR Tech will end your Lifeline "
         "benefit with your current provider. Do you understand?\"")
numbered(doc, "\"Only one company can receive the benefit for you at a time. You're choosing to receive it "
         "through RIVR Tech going forward. Is that correct?\"")
numbered(doc, "\"You can transfer to a different provider again in the future if you ever want to.\"")
numbered(doc, "\"Do I have your permission to complete this transfer in the federal system on your behalf?\"")
para(doc, "Rep: \"Thank you. I'm recording your consent as required. [Capture consent per USAC method.] "
     "You're all set — I'll complete the transfer and confirm once it's done.\"")

footer_revhist(doc)

doc.save(OUT)

from docx import Document
_ = Document(OUT)
print("OK 09")
