# RIVR Tech — Lifeline & Lumbee Broadband Affordability Program

**Entity:** LREMC Technologies, LLC d/b/a RIVR Tech
**Status:** Phase 0 build artifacts — **NCUC ETC application pending**
**Version:** v0.1 (DRAFT for internal review)

This folder contains an implementation-ready program package for applying the federal **Lifeline**
benefit to RIVR Tech internet customers, launching a **100/100 Mbps Senior Internet Plan** at a $10
net customer payment, and coordinating a broadband affordability initiative with the **Lumbee Tribe of
North Carolina**.

## ⚠️ Read first — three hard rules baked into every deliverable

1. **Lumbee membership ≠ enhanced Tribal Lifeline.** The enhanced benefit (up to **$34.25/mo**) requires
   the customer's **principal residence to be on qualifying "Tribal lands"** per 47 C.F.R. §54.400(e),
   verified per-address with USAC's Tribal Lands Verification Tool. The Lumbee currently have **no
   reservation, no trust land, and no FCC §54.412 designation**, so the working assumption is **zero
   enhanced-Tribal-eligible addresses** until a written USAC/legal determination says otherwise.
2. **Nothing launches until the final NCUC ETC order is issued and USAC onboarding is complete.** Do not
   market RIVR Tech as an approved Lifeline provider before then. **ACP has ended (June 2024)** and must
   never be presented as active.
3. **No invented facts.** RIVR Tech's actual plan prices are **not published** and appear here only as
   clearly-labeled placeholders to be replaced from RIVR's confirmed price sheet. Tax treatment and the
   Tribal-lands determination require confirmation by RIVR's tax advisor / regulatory counsel / USAC.
   **No "plus tax" is advertised** until the tax advisor confirms which components are taxable.

## Deliverables

| # | File | Format | Purpose |
|---|------|--------|---------|
| 00 | `00_Regulatory_Source_Register.md` | Markdown | Shared, sourced facts base; every doc cites its `SR-x.y` items |
| 01 | `01_Executive_Implementation_Plan.docx` | Word | Executive summary + plan + **required-decisions table** |
| 02 | `02_Current_Plan_and_Pricing_Audit.xlsx` | Excel | Current-state plan inventory + 6-scenario pricing matrix |
| 03 | `03_Lifeline_Operations_Manual.docx` | Word | How the Lifeline program runs (eligibility, systems, privacy, WFA) |
| 04 | `04_Enrollment_and_Deenrollment_SOPs.docx` | Word | 10 enrollment workflows + de-enrollment lifecycle SOPs |
| 05 | `05_NISC_Configuration_and_Billing_Specification.docx` | Word | Rate/credit codes, tax config, GL mapping, 3-way reconciliation |
| 06 | `06_Lifeline_Financial_Model.xlsx` | Excel | Formula-driven model: pricing, subscriber build, P&L, break-even |
| 07 | `07_Compliance_and_Audit_Checklist.xlsx` | Excel | Cited compliance checklist with owner/status/evidence |
| 08 | `08_Implementation_Roadmap_and_RACI.xlsx` | Excel | Phased roadmap (0–4) + RACI matrix |
| 09 | `09_Customer_Communications_Toolkit.docx` | Word | Website/FAQ/letters/notices/scripts (compliant draft copy) |
| 10 | `10_Employee_Training_Guide.docx` | Word | Role modules + prohibited-statements table + knowledge checks |
| 11 | `11_Lumbee_Tribe_Partnership_MOU_Exhibit.docx` | Word | Draft MOU exhibit (with non-waiver of sovereign immunity) |
| 12 | `12_Executive_Readiness_Scorecard.xlsx` | Excel | Weighted go/no-go gate |
| 13 | `13_Open_Issues_and_Legal_Decisions_Log.xlsx` | Excel | Unresolved questions with recommended decisions & owners |
| 14 | `14_Phase1_Onboarding_Tracker.xlsx` | Excel | **Post-ETC-approval** dated 30/60/90-day USAC onboarding tracker (dates auto-calc from the NCUC order date) |
| 15 | `15_SAC_Request_Cover_Letter.docx` | Word | Draft transmittal to USAC requesting a Study Area Code |
| 16 | `16_Phase1_Kickoff_Memo.docx` | Word | Phase 1 kickoff memo — what approval does/doesn't authorize + critical path |

> **Phase 1 note (files 14–16):** added when NCUC ETC designation was granted. The program has moved from
> Phase 0 (application pending) to Phase 1 (USAC onboarding). Enter the actual NCUC order date on the
> Tracker's Cover tab and every target date recalculates. Approval authorizes the **standard** $9.25
> benefit once onboarded — it does **not** authorize the enhanced $34.25 based on Lumbee membership (see
> Hard Rule 1 above).

## Conventions

- **Excel cell colors:** yellow = editable input; **orange = placeholder to replace with a confirmed
  figure**; blue = federal program constant (re-verify each program year); white = formula (don't edit).
  All models use **visible formulas** and editable assumption cells.
- **Citations:** `SR-x.y` refers to a row in `00_Regulatory_Source_Register.md`, which carries the
  official source URL. Because automated access to fcc.gov/usac.org/ecfr.gov/ncuc.gov was restricted
  during compilation, **every figure should be re-verified against its live cited source before filing
  or customer use.** `[CONFIRM]` marks items needing confirmation.

## How the deliverables were built

The `_build/` folder holds the Python generator scripts (openpyxl / python-docx) used to produce each
file, so the package is fully reproducible. Regenerate any file by re-running its `build_*.py` script.

## Immediate next steps for RIVR Tech

1. Obtain the confirmed RIVR price sheet (all tiers, equipment, voice, install) → unblocks 02 & 06.
2. Obtain the written USAC/legal Tribal-lands determination → unblocks any enhanced-Tribal handling.
3. Obtain the tax-advisor opinion on taxable components → unblocks bill display & "plus tax" language.
4. Confirm the NCUC ETC docket/status and track to the final order.
5. Work the Required Executive Decisions table (01 §11) and the Open Issues log (13).
