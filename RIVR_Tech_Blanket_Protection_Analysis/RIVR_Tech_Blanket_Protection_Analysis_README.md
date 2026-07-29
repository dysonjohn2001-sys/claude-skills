# RIVR Tech — Blanket Residential Maintenance Protection Plan Analysis

**Prepared for:** LREMC Technologies, LLC d/b/a RIVR Tech
**Question:** Should RIVR Tech introduce a blanket **$3.99 (A)** or **$4.99 (B)** monthly
Maintenance Protection Plan for **all residential internet customers**, and if so, how should it
be structured?
**Version:** v1.0 (Draft for Executive Review) · **Date:** 2026‑07‑29
**Status:** Recommendations and **labeled assumptions** only — **not legal, tax, or regulatory advice.**

> ⚠️ Numerous provisions require legal, regulatory, accounting, tax, insurance, billing, and
> executive review before adoption. Nothing here is established RIVR Tech policy.

---

## 1. Recommendation (bottom line)

**Do NOT implement a mandatory blanket fee.** Offer the plan as a **voluntary opt‑in at $3.99**
(Standard coverage), delivered as a **hybrid**: enrollees get the plan; customers who decline pay
a per‑visit dispatch charge (≈ $99 suggested). Enroll at installation and again after a first
chargeable call; **no retroactive enrollment; 30‑day waiting period; pre‑existing conditions
excluded.** **Exempt** Lifeline, Tribal Lifeline, and low‑income customers (opt‑in only, never
auto‑charged); **exclude** bulk/managed‑property accounts (handled by contract). **Pilot** before
any system‑wide launch.

### Why not mandatory
A mandatory or opt‑out fee on customers who never need a service call risks incremental churn, and
each churned customer costs the full ~$74 ARPU. The plan's contribution is erased by only:
- **~1.8% incremental annual churn at $3.99 mandatory**
- **~3.1% at $4.99 mandatory**

Voluntary opt‑in customers *choose* the plan, so fee‑driven churn is ~0 — the safer structure, and
the top‑ranked option in the weighted decision matrix.

---

## 2. Key economics (Expected scenario; model outputs on labeled assumptions)

| Metric | $3.99 (A) | $4.99 (B) |
|---|---|---|
| Loaded cost per covered call | $143 | $143 |
| Contribution / enrolled member / yr | $21.04 | $32.68 |
| Contribution margin | 44% | 55% |
| Break‑even utilization (per member) | ~29% | ~37% |
| Break‑even incremental churn (mandatory) | ~1.8% | ~3.1% |
| Covered calls fundable before break‑even (4,686 fully enrolled) | ~1,502 | ~1,879 |
| 5‑yr cumulative net — voluntary opt‑in @35% (plan revenue only) | **~$96,194** | higher |

Pay‑per‑visit at $75–$150 recovers only a portion of the ~$149 fully loaded call cost — no single
per‑visit charge in that range fully covers it, which is itself an argument for the subscription
risk‑pool.

---

## 3. Recommended coverage tiers

- **Basic ($3.99):** 1 covered customer‑caused visit / 12 mo, basic Wi‑Fi troubleshooting,
  customer education, first router relocation, reduced dispatch on extra visits.
- **Standard ($4.99):** 2 covered visits / 12 mo; adds connector replacement, RIVR‑installed
  inside‑wiring diagnostics, pet/lawn‑equipment damage (1st/yr).
- **Premium ($7.99, illustrative):** 4 visits, after‑hours, priority. **$3.99/$4.99 are not
  sufficient for Premium at expected utilization.**

**Always free (RIVR‑owned):** ONT, router/GigaSpire, outdoor drop, and any RIVR network problem.
**Always excluded:** customer devices, construction/remodel damage, acts of God/storms/flood,
willful damage, concealed rewiring, pre‑existing conditions.

## 4. Exemptions / opt‑in‑only groups
Seniors, Lifeline, Tribal Lifeline, low‑income, rarely‑support customers, renters (clarify
landlord‑owned facilities), and multi‑service customers → **opt‑in only**. Bulk/managed properties
→ **excluded** (governed by contract).

---

## 5. Answers to the ten closing questions

1. **Structure & price:** Voluntary opt‑in **$3.99**, hybrid with pay‑per‑visit for decliners.
2. **Coverage:** Standard tier (2 visits/yr + Wi‑Fi/education/inside‑wiring); RIVR‑owned always free.
3. **Exempt/discounted:** Lifeline, Tribal Lifeline, low‑income (opt‑in only); bulk/managed excluded.
4. **Estimated revenue:** Opt‑in @35% ≈ **$78.5K gross / member‑contribution‑positive**; ~**$96K
   cumulative net over 5 years** on plan revenue alone (hybrid PPV adds upside).
5. **Break‑even utilization:** ~29% ($3.99) / ~37% ($4.99) per member.
6. **Maximum acceptable churn increase:** Keep incremental annual churn **< ~1.8%** ($3.99) or the
   plan is net‑negative under a mandatory model; target **≤ 0.5%** in the pilot.
7. **Approvals:** Legal (negative‑option, Lifeline/Tribal, naming, NC consumer protection), tax,
   accounting, billing/NISC, executive.
8. **Pilot:** 1–2 service areas, 90 days, opt‑in; success = take‑rate ≥ 25%, utilization ≤ 20%,
   churn increase ≤ 0.5%, flat complaints.
9. **Go/no‑go:** Proceed only if pilot hits thresholds and legal clears negative‑option/Lifeline.
10. **Data to collect:** see the model's `Data Needed`‑style list and Section 7 of the memo.

---

## 6. File inventory (relative to `RIVR_Tech_Blanket_Protection_Analysis/`)

| Folder / File | Description |
|---|---|
| `01_Financial_Model/RIVR_Tech_Blanket_Protection_Financial_Model.xlsx` | 11‑sheet live model: Assumptions, Subscriber Forecast, Scenario A ($3.99), Scenario B ($4.99), Enrollment Models, Utilization Analysis, Churn Sensitivity, Pay‑Per‑Visit, Five‑Year Forecast, Executive Dashboard, Recommendation Summary. 2 charts + weighted decision matrix. |
| `02_Executive_Memo/RIVR_Tech_Blanket_Protection_Executive_Memo.docx` | Executive decision memo (business case, financials, risks, structure comparison, recommendation, gates). |
| `03_Plan_Document/RIVR_Tech_Home_Protection_Draft_Plan.docx` | Draft plan: name, eligibility, coverage tiers, exclusions, waiting period, cancellation, limits, responsibilities, abuse, disputes, legal placeholders. |
| `04_Customer_Communications/RIVR_Tech_Blanket_Protection_Customer_Communications.docx` | Bill message, email, website, 14 FAQs, CS script, technician explanation, opt‑in + opt‑out language. |
| `05_Implementation/RIVR_Tech_Blanket_Protection_Implementation_Roadmap.docx` | 30/60/90‑day plan, workstreams, approvals, pilot design, naming/billing, data to collect. |
| `06_Source_Files/blanket_content.py` | Single source of truth (assumptions, compute model, coverage, scoring). |
| `06_Source_Files/build_blanket_xlsx.py` | Builds the financial model. |
| `06_Source_Files/build_blanket_docx.py` | Builds the 4 Word documents (reuses the first project's `docx_helpers`). |
| `RIVR_Tech_Blanket_Protection_Analysis_README.md` | This file. |

---

## 7. Enrollment models evaluated (per the brief)

- **Mandatory** (100%) — highest gross, highest regulatory/trust/churn risk. **Not recommended.**
- **Automatic w/ opt‑out** — participation modeled at 95/85/75/60/50%. Negative‑option legal risk.
- **Voluntary opt‑in** — participation modeled at 20/30/40/50/60%. **Recommended.**

Both price points ($3.99, $4.99) are evaluated for every model in the `Enrollment Models` sheet,
with utilization (5–40% × $75–$250 call cost) and churn (0–5%) sensitivity grids.

---

## 8. How to regenerate / edit

```bash
cd 06_Source_Files
pip install python-docx openpyxl        # one-time
python3 build_blanket_xlsx.py           # financial model
python3 build_blanket_docx.py           # 4 Word documents
```

Edit **`06_Source_Files/blanket_content.py`** (the single source of truth) to change any assumption,
price, coverage row, or decision score, then rebuild. The Excel model uses **live formulas** driven
by the yellow `Assumptions` cells — open in Excel and allow recalculation.

Color coding: 🟨 input · 🟦 calculated · 🟩 recommended/result · 🟧 warning.

---

## 9. Validation performed

- **All financial‑model formulas independently evaluated** with a Python Excel‑formula engine:
  every checked cell matches the reference model exactly, **0 formula errors**. Two layout bugs
  found and fixed during validation (per‑member block row offset; voluntary‑opt‑in churn treatment).
- **All 5 documents/workbook reopen cleanly** (valid Office XML).
- **Decision matrix** (SUMPRODUCT/weights) verified against the Python scores.

### Known limitation — PDF/image rendering
The sandbox's LibreOffice cannot load files for headless PDF/image conversion, so a visual PDF
render was not produced here. Validation was structural (reopening, formula evaluation). Before
distribution, open each file in Office, update Word TOC fields (right‑click → Update Field), and
allow Excel recalculation.

---

## 10. Legal / regulatory review flags
Advance notice · material change to terms · affirmative consent · **negative‑option / auto‑renewal
(FTC ROSCA + state law)** · truthful advertising (no tax/government/network‑fee language) · billing
transparency · NC consumer protection · FCC requirements · **broadband‑label disclosure** ·
**Lifeline & Tribal Lifeline** · tax treatment · existing customer agreements · bulk‑service
contracts · customer‑ vs provider‑owned facilities. **Not legal advice.**
