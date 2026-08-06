# 00 — Regulatory Source Register & Verified-Facts Base

**Program:** RIVR Tech Lifeline & Lumbee Broadband Affordability Initiative
**Entity:** LREMC Technologies, LLC d/b/a RIVR Tech
**Owner:** Program Owner + Regulatory Counsel
**Version:** v0.1 (build phase — Phase 0, ETC application pending)
**Compiled:** during program build; **re-verify every figure against the live cited source before go-live.**

> **How this file is used.** Every other deliverable (01–13) cites the item numbers here (e.g., "SR-1.1"). This keeps one authoritative, sourced facts base so numbers never drift between documents. Items marked **[CONFIRM]** require a live check by RIVR Tech, its regulatory attorney, its tax advisor, USAC, the FCC, or the NCUC before reliance.
>
> **Research caveat.** During compilation, automated fetching of `fcc.gov`, `usac.org`, `ecfr.gov`, `ncuc.gov`, `ncdor.gov`, and `congress.gov` was blocked by egress policy; facts were drawn from search extracts of those official pages. **The URLs are the official sources — open each to confirm exact/current wording before any filing or customer-facing use.**

---

## SR-1 — Federal Lifeline benefit amounts & eligibility

| # | Fact | Source |
|---|------|--------|
| SR-1.1 | **Standard Lifeline benefit = up to $9.25/mo** for broadband or bundled voice+broadband. | 47 C.F.R. §54.403 — https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-54/subpart-E/section-54.403 ; https://www.usac.org/lifeline/ |
| SR-1.2 | **Voice-ONLY support = $5.25/mo**, phase-out **paused through Nov 30, 2026**. (Program is broadband-first; voice optional.) | https://www.usac.org/lifeline/rules-and-requirements/minimum-service-standards/ |
| SR-1.3 | **Enhanced Tribal benefit = additional up to $25/mo** on top of standard → **total up to $34.25/mo**. Carrier must certify full pass-through. | 47 C.F.R. §54.403(a)(3); https://www.usac.org/lifeline/enhanced-tribal-benefit/ |
| SR-1.4 | **Income eligibility = household income ≤ 135% of Federal Poverty Guidelines.** | 47 C.F.R. §54.409(a); https://www.usac.org/lifeline/consumer-eligibility/ |
| SR-1.5 | **2026 income $ thresholds (135% FPG, 48 states/DC)** — 1 person $21,546; 2 $29,214; 3 $36,882; 4 $44,550 (higher for AK/HI). **[CONFIRM against live USAC PDF.]** | https://www.usac.org/wp-content/uploads/lifeline/documents/handouts/Income_Requirements.pdf |
| SR-1.6 | **Program-based eligibility:** Medicaid; SNAP; SSI; Federal Public Housing Assistance; Veterans & Survivors Pension Benefit. | 47 C.F.R. §54.409(b); https://www.usac.org/lifeline/consumer-eligibility/ |
| SR-1.7 | **Tribal-specific programs:** Bureau of Indian Affairs General Assistance; Tribal TANF; Head Start (income-qualifying only); FDPIR. *These qualify a person for **standard** Lifeline — they do NOT establish Tribal-lands residence for the enhanced benefit.* | 47 C.F.R. §54.409(b); https://www.usac.org/lifeline/consumer-eligibility/ |
| SR-1.8 | **One Lifeline benefit per household.** "Household" = individuals living together at one address as one **economic unit** (adults sharing income & expenses). One-per-household worksheet used where multiple households share an address. | 47 C.F.R. §§54.400, 54.409; https://www.usac.org/lifeline/consumer-eligibility/ |

## SR-2 — Minimum service standards (current program year)

| # | Fact | Source |
|---|------|--------|
| SR-2.1 | **Fixed broadband minimum speed = 25/3 Mbps.** The proposed Senior **100/100 plan exceeds this comfortably.** | 47 C.F.R. §54.408; https://www.usac.org/lifeline/rules-and-requirements/minimum-service-standards/ |
| SR-2.2 | **Fixed broadband minimum data allowance = 1,280 GB/mo** (since Dec 1, 2023). RIVR plans are **unlimited/no cap**, so this is met. | FCC DA-24-740; https://docs.fcc.gov/public/attachments/DA-24-740A1.pdf |
| SR-2.3 | **Mobile broadband data = 4.5 GB/mo** (increase paused through Dec 1, 2026). *N/A to fixed fiber but noted.* | https://www.usac.org/lifeline/rules-and-requirements/minimum-service-standards/ |
| SR-2.4 | Mobile voice minutes standard **[CONFIRM]** — not independently verified; N/A if voice not offered as mobile. | https://www.usac.org/lifeline/rules-and-requirements/minimum-service-standards/ |

## SR-3 — National Verifier, NLAD, recertification, de-enrollment

| # | Fact | Source |
|---|------|--------|
| SR-3.1 | **National Verifier (NV) approval REQUIRED before NLAD enrollment.** NV checks identity, address, program/income, and duplicates. | https://www.usac.org/lifeline/national-verifier/ ; https://www.usac.org/lifeline/national-verifier/how-to-use-nv/ |
| SR-3.2 | **NLAD** = enrollment + duplicate-prevention database. Enroll only after approved NV result. Must update NLAD **within 10 business days** of subscriber info changes. | https://www.usac.org/lifeline/national-lifeline-accountability-database-nlad/ |
| SR-3.3 | **Annual recertification** required; failed data-source check → subscriber has **60 days** to respond or is **de-enrolled**. | 47 C.F.R. §54.410(f); https://www.usac.org/lifeline/national-verifier/recertification/ |
| SR-3.4 | **Non-usage rule** (only for services with no monthly fee to subscriber): 30 consecutive days non-use → 15-day cure notice → terminate if uncured. *If the Senior plan carries a >$0 customer charge, the non-usage rule generally does not apply — **[CONFIRM]** with counsel given the $10 charge.* | 47 C.F.R. §54.405(e)(3), §54.407(c)(2) |
| SR-3.5 | **De-enrollment** required for failure to recertify, one-per-household failures, duplicate, ineligibility, or subscriber request. | 47 C.F.R. §54.405(e) |
| SR-3.6 | **Benefit transfer** — a subscriber already in NLAD (with another provider) transfers via consent-based benefit transfer in NLAD. | https://www.usac.org/lifeline/national-lifeline-accountability-database-nlad/subscriber-management/dispute-resolution/ |

## SR-4 — Enhanced Tribal benefit is ADDRESS-based (the central compliance rule)

| # | Fact | Source |
|---|------|--------|
| SR-4.1 | **"Tribal lands" definition** (enumerated): federally recognized tribe's **reservation, pueblo, or colony** (incl. former reservations in Oklahoma); ANCSA Alaska Native regions; Indian allotments; Hawaiian Home Lands; **and any land the FCC designates via the §54.412 process.** | 47 C.F.R. §54.400(e) — https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-54/subpart-E/section-54.400 |
| SR-4.2 | **Enhanced benefit requires the subscriber to be an "eligible resident of Tribal lands"** — i.e., **principal residence physically ON qualifying Tribal lands**, NOT tribal membership. | 47 C.F.R. §54.403(a)(3); https://www.usac.org/lifeline/enhanced-tribal-benefit/ |
| SR-4.3 | **Off-reservation designation process (§54.412):** land outside existing Tribal lands becomes Lifeline "Tribal lands" ONLY if the FCC (Wireline Competition Bureau + Office of Native Affairs & Policy) designates it, **upon request by a duly authorized official of the federally recognized Tribe.** | 47 C.F.R. §54.412 — https://www.law.cornell.edu/cfr/text/47/54.412 |
| SR-4.4 | **Verification method:** USAC **Tribal Lands Verification Tool** checks a specific street address / lat-long against the qualifying-lands dataset. NLAD "Lifeline Tribal Benefit?" flag set to Yes only for verified addresses. AMS error path requires coordinates to validate. | https://www.usac.org/lifeline/enhanced-tribal-benefit/ |

## SR-5 — Lumbee Tribe status (why enhanced Tribal ≠ automatic)

| # | Fact | Source |
|---|------|--------|
| SR-5.1 | **Full federal recognition via Public Law 119-60**, enacted as **§8803 of the NDAA for FY2026, 139 Stat. 1973, signed Dec 18, 2025.** | https://www.congress.gov/bill/119th-congress/senate-bill/107/text ; https://www.congress.gov/crs-product/R48888 |
| SR-5.2 | DOI added the Lumbee to the official list of federally recognized tribes (~Jan 30, 2026). | https://www.doi.gov/pressreleases/lumbee-tribe-added-official-list-federally-recognized-tribes |
| SR-5.3 | **The law AUTHORIZES (does not execute) land-into-trust.** Robeson County trust applications are to be **treated as "on reservation"** under 25 C.F.R. part 151 — a *future pathway*, not an existing reservation. | https://www.congress.gov/bill/119th-congress/senate-bill/107/text |
| SR-5.4 | **Service delivery area = Robeson, Cumberland, Hoke, Scotland Counties** — for delivery of federal *services* to members. **A service delivery area is NOT "Tribal lands" under §54.400(e).** | S.107 text; CRS R48888 |
| SR-5.5 | **As of this research: the Lumbee have NO reservation, NO land held in trust, and NO FCC §54.412 designation.** Therefore addresses in the four counties are **NOT presumptively Tribal lands** and do **NOT** qualify for the enhanced $25 benefit by default. | Synthesis of SR-4 + SR-5; **[CONFIRM] no pending/granted §54.412 designation with USAC/FCC ONAP; [CONFIRM] no land yet taken into trust with BIA.** |
| SR-5.6 | **Net rule to encode everywhere:** *Lumbee membership and four-county residence do NOT confer enhanced Tribal Lifeline. Enhanced $25 requires the principal residence to be on qualifying Tribal lands per §54.400(e), verified per-address via the USAC Tribal Lands Verification Tool.* | — |

## SR-6 — ETC onboarding & USAC systems (sequence)

| # | Fact | Source |
|---|------|--------|
| SR-6.1 | **ETC designation** by the state commission (NCUC) under Telecom Act §254(e) is a prerequisite to Lifeline support. | 47 C.F.R. §§54.201–54.203; https://www.usac.org/lifeline/get-started/join-lifeline-as-an-etc/ |
| SR-6.2 | **FRN** via FCC CORES (no fee); same TIN used later for SAM.gov. | https://www.fcc.gov/licensing-databases/commission-registration-system-fcc |
| SR-6.3 | **SAM.gov UEI + active bank account** required for USF disbursement; annual renewal; can take ~6 weeks. | https://www.usac.org/about/sam-gov-uei-requirement/ |
| SR-6.4 | **Study Area Code (SAC)** issued by USAC after review of the ETC designation order; ≥1 per state; unit of account for claims/481/555. Obtain **before** 498 ID. | https://www.usac.org/lifeline/get-started/join-lifeline-as-an-etc/ |
| SR-6.5 | **498 ID / FCC Form 498** (SPIN) — banking/contact for disbursement; Company Officer certifies (14-day window). | https://www.usac.org/service-providers/participating-in-a-usf-program/register-for-a-498-id/ |
| SR-6.6 | **RAD** — every enrollment representative self-registers at **LifelineRAD.org** for a unique **Rep ID** before enrolling subscribers. | https://www.usac.org/lifeline/rad/ |
| SR-6.7 | **NV + NLAD access** via One Portal; 497 Officer creates org account, assigns ETC Administrator; roles need Rep IDs; "NV-Only" ETC Agent role for sales. | https://www.usac.org/lifeline/national-verifier/how-to-use-nv/ |
| SR-6.8 | **LCS** — monthly claim, one per SAC; built from NLAD **Subscriber Snapshot** taken **1st of month**; certified claims filed **by the 8th** paid end of same month. 497 Officer certifies. Legacy Form 497 retired. | https://www.usac.org/lifeline/lifeline-claims-system-lcs/how-to-claim-reimbursement/ |
| SR-6.9 | **FCC Form 481** (Carrier Annual Report) — filed per SAC, **due July 1** (FCC has waived/extended in some years — **[CONFIRM] current-year deadline**). Officer certification required. | https://www.usac.org/high-cost/annual-requirements/file-fcc-form-481/ |
| SR-6.10 | **FCC Form 555** (Annual Lifeline ETC Certification / recert results) — per SAC, **due Jan 31**, filed via One Portal + ECFS **Docket 14-171** + state commission + relevant Tribal governments. | https://www.usac.org/lifeline/rules-and-requirements/forms/annual-filings/ |
| SR-6.11 | **Record retention (§54.417):** retain compliance records **≥ 3 full preceding calendar years**; subscriber-eligibility docs for **as long as the subscriber receives service, minimum 3 years.** (NOT 10 years — that's the separate high-cost rule §54.320.) | 47 C.F.R. §54.417 — https://www.ecfr.gov/current/title-47/chapter-I/subchapter-B/part-54/subpart-E/section-54.417 |
| SR-6.12 | **Advertising obligation (§54.405(b)):** ETC must publicize Lifeline availability in a manner reasonably designed to reach those likely to qualify. | 47 C.F.R. §54.405(b) |

## SR-7 — North Carolina (NCUC) requirements

| # | Fact | Source |
|---|------|--------|
| SR-7.1 | **NCUC Rule R9-6** (Chapter 9): ETCs designated under Telecom Act §254(e) must provide Lifeline & Link Up and submit implementing info to NCUC, FCC, and USAC. **[CONFIRM verbatim subparts from the PDF.]** | https://www.ncuc.gov/ncrules/Chapter09.pdf |
| SR-7.2 | ETC designation is by the NCUC; USAC disburses; NCUC oversees. Related Lifeline rulemaking: Docket **M-100, Sub 196**. | https://www.ncuc.gov/industries/telecom/telecom.html |
| SR-7.3 | **No public NCUC docket naming LREMC Technologies / RIVR Tech was found via search. [CONFIRM]** ETC application/docket status via the NCUC docket portal and staff. | https://starw1.ncuc.gov/NCUC/page/Dockets/portal.aspx |
| SR-7.4 | **RIVR Tech ETC designation order** — **[PENDING]**. Do not market as an approved Lifeline provider until the final order issues and USAC onboarding is complete. | — |

## SR-8 — RIVR Tech current-state (confirmed vs. to-obtain)

| # | Fact | Source / status |
|---|------|-----------------|
| SR-8.1 | Public site **rivrtech.net**; HQ **6090 NC Hwy 711, Pembroke, NC 28372**; **(910) 843-4131**. | https://rivrtech.net/ |
| SR-8.2 | **Symmetrical fiber lineup: 250/250 (entry) → 500/500 → 1 Gig (1000/1000)**, up to 2 Gbps referenced. **Unlimited data, no caps.** *Confirmed by RIVR (speeds); entry tier = 250/250.* | User-confirmed + https://rivrtech.net/residential/internet/ |
| SR-8.3 | **Proposed Senior 100/100 is a NEW tier below the 250/250 entry** — deliberately lower-speed/affordable; trivially deliverable on symmetrical fiber. | Program design |
| SR-8.4 | Equipment: **indoor Wi-Fi 6 router $5/mo; outdoor mesh $10/mo**; install advertised **free ($99 value, promotional)**. **CONFLICT** between "free router rental" and "$5/mo" on site — **[CONFIRM]** current policy. | https://rivrtech.net/support/ |
| SR-8.5 | Residential **voice** = unlimited calling; **price not published — [OBTAIN from RIVR].** | https://rivrtech.net/residential/voice/ |
| SR-8.6 | **Monthly plan prices for 250/500/1000 tiers NOT published/retrievable — [OBTAIN from RIVR price sheet].** No published senior/low-income discount found. RIVR previously participated in **ACP (now ended)** — distinct from Lifeline. | https://rivrtech.net/ |

## SR-9 — Tax treatment (NOT tax advice — for RIVR tax-advisor confirmation)

| # | Fact | Source |
|---|------|--------|
| SR-9.1 | **Internet Tax Freedom Act permanent (since Feb 24, 2016)** — states/localities may **NOT tax internet access**. Grandfather clause expired June 30, 2020. | https://www.congress.gov/crs-product/IF11947 |
| SR-9.2 | **NC does NOT tax standalone internet access** (excluded from "telecommunications service"). Bundling with taxable services may affect the bundle. **[CONFIRM]** | https://www.ncdor.gov/taxes-forms/sales-and-use-tax/telecommunications-service-and-ancillary-service |
| SR-9.3 | **NC taxes telecommunications/voice at the 7.00% combined general rate** (Form E-500E); statute §105-164.4(a)(4c). **[CONFIRM applicability to RIVR's voice/VoIP.]** | https://ncleg.net/EnactedLegislation/Statutes/HTML/BySection/Chapter_105/GS_105-164.4.html |
| SR-9.4 | **Equipment lease/rental (router/mesh) = taxable TPP** in NC, taxed each billing period. Bundling-with-internet treatment **[CONFIRM]**. | https://www.ncdor.gov/taxes-forms/sales-and-use-tax/lease-or-rental-tangible-personal-property |
| SR-9.5 | **Installation** charges are within "sales price" and taxable when tied to a taxable sale; RMI services generally taxable. Turns on what the install attaches to. **[CONFIRM]** | https://www.ncdor.gov/taxes-forms/sales-and-use-tax/taxable-items/repair-maintenance-and-installation-services-and-other-repair-information |
| SR-9.6 | **"Managed Wi-Fi" taxability = open, fact-specific question** (TPP rental vs. RMI service vs. nontaxable). No NCDOR ruling located. **[CONFIRM]** | https://www.ncdor.gov/taxes-forms/sales-and-use-tax/taxable-items |
| SR-9.7 | **Federal USF contribution** on interstate voice revenue (Q2 2026 factor 37.0%); broadband not assessed. **[CONFIRM]** pass-through mechanics for RIVR voice. | https://www.usac.org/service-providers/making-payments/contribution-factors/ |
| SR-9.8 | **NC 911 charge = $0.70/mo per voice connection** (non-prepaid), §143B-1403; prepaid wireless $0.55/transaction. Voice only, not broadband. **[CONFIRM]** | https://www.ncleg.gov/EnactedLegislation/Statutes/PDF/BySection/Chapter_143B/GS_143B-1403.pdf |
| SR-9.9 | **Do not advertise "plus tax" on the Senior broadband plan until the tax advisor confirms which components (broadband/equipment/voice/install) are taxable.** Broadband access itself is non-taxable per ITFA; equipment/voice may be. | Synthesis SR-9.1–9.8 |

## SR-10 — TBCP / funding separation

| # | Fact | Source / rule |
|---|------|---------------|
| SR-10.1 | **Do NOT characterize Tribal Broadband Connectivity Program (TBCP) funds as a recurring consumer subsidy** unless the specific award, budget, and grant terms expressly authorize that use. | NTIA TBCP program rules — **[CONFIRM against the specific award if any]** https://www.internetforall.gov/program/tribal-broadband-connectivity-program |
| SR-10.2 | **Keep four funding streams in separate GL/accounting categories:** (1) federal Lifeline (USAC), (2) TBCP/other grants, (3) RIVR-funded discounts, (4) Lumbee Tribe contributions. No commingling. | Program control (see NISC spec) |

---

### Open determinations requiring named sign-off (see 13_Open_Issues log)
1. **[LEGAL/USAC]** Written determination whether ANY Lumbee service-area, trust, or dependent-community land currently satisfies §54.400(e) / has a §54.412 designation. *Working assumption: NO qualifying Tribal lands today → enhanced $25 = $0 subscribers until confirmed.*
2. **[TAX]** Which Senior-plan components are taxable (broadband vs. equipment vs. voice vs. install).
3. **[REGULATORY]** Final NCUC ETC order + confirmed service area + SAC.
4. **[RIVR]** Confirmed current price sheet (all tiers, equipment, voice, install, existing discounts).
5. **[TBCP]** Whether any grant funds may lawfully offset recurring consumer bills.
