# RIVR Tech Five-Year Business Plan — Source-Data Inventory & Assumption Log

**Prepared:** 2026-07-21
**Entity:** LREMC Technologies, LLC d/b/a RIVR Tech
**Planning period:** FY2027–FY2031

---

## A. Source scan & inventory

| # | Source | Status | Contents used |
|---|--------|--------|---------------|
| 1 | Engagement request | Supplied | Subscriber counts (Jun-2026), ARPU starting assumptions, capital & refresh program, staffing roster |
| 2 | **RIVR_Tech_Charts_2nd_Q_2026_BOD.pptx** (Board of Directors deck, quarter ended 6/30/2026) | **Provided by client** | **Actual Q2-2026 income statement** (operating revenue by product, full expense structure, D&A, interest, grant income, net income) and **grant awards** (CAB 2.0, NC Stop GAP, BTAP) |

The initial working-directory scan found no RIVR Tech files. The client subsequently
provided the **Q2-2026 Board deck (source #2)**, which supplies **actual financial
results**. Those actuals are now the plan's baseline; forward projections build on them
plus clearly-labeled assumptions. Subscriber counts, ARPU by product, homes passed, and
labor rates remain partly estimated (see §E and the conflict log §F).

---

## B. Data-classification legend

| Tag | Meaning |
|-----|---------|
| **[ACTUAL]** | Supplied in the engagement request; treated as management-provided fact (not independently audited). |
| **[ASSUMPTION]** | Management planning assumption chosen for modeling; editable. |
| **[CALC]** | Calculated/derived by formula from actuals + assumptions. |
| **[TARGET]** | Recommended target set by this plan. |
| **[PLACEHOLDER]** | Value unknown; editable placeholder pending management input. |

---

## C. Supplied inputs treated as ACTUAL

| Item | Value | Tag | Notes |
|------|-------|-----|-------|
| Legal entity | LREMC Technologies, LLC | [ACTUAL] | |
| Trade name | RIVR Tech | [ACTUAL] | |
| Service area | Robeson, Hoke, Scotland, Cumberland + surrounding NC counties | [ACTUAL] | |
| Annual capital funding | $10,000,000 / year | [ACTUAL] | |
| Five-year capital funding | $50,000,000 | [ACTUAL] | |
| Equipment-refresh program | $400,000 / year; $2,000,000 / 5 yr | [ACTUAL] | |
| Internet subscribers (June 2026 ME) | 4,686 | [ACTUAL] | Not audited. |
| Voice subscribers (June 2026 ME) | 502 | [ACTUAL] | Not audited. |
| Residential ARPU (starting) | $74 | [ACTUAL] | Starting assumption per request. |
| Business ARPU (starting) | $149 | [ACTUAL] | Starting assumption per request. |
| Current filled positions | 15 | [ACTUAL] | |
| Current open positions | 3 | [ACTUAL] | |
| Authorized positions (after fills) | 18 | [ACTUAL] | |

### Current staffing roster [ACTUAL]

| Position | Filled | Open |
|----------|-------:|-----:|
| Chief Operations Officer | 1 | 0 |
| Director of Outside Plant | 1 | 0 |
| Supervisors | 2 | 0 |
| Project Coordinators | 2 | 0 |
| Sales Coordinator | 1 | 0 |
| Sales Representatives | 3 | 1 |
| Fiber Technicians | 5 | 2 |
| **Total** | **15** | **3** |

---

## D. Key management assumptions (editable) — base case

These are NOT audited data. They are the starting assumptions used to drive the model.
Every one is exposed on the Excel **Assumptions** tab and can be overridden.

### D.1 Subscriber mix at June 2026 (split of the 4,686 internet subs) [ASSUMPTION]
| Line | Count | Basis |
|------|------:|-------|
| Residential internet | 4,324 | ~92.3% of internet base (placeholder split) |
| Business internet | 350 | ~7.5% of internet base (placeholder split) |
| Enterprise / DIA circuits | 12 | ~0.3% high-capacity accounts (placeholder split) |
| **Internet total** | **4,686** | Reconciles to actual |
| Voice | 502 | [ACTUAL] |

### D.2 Year-1 opening balances (Jan 2027) [ASSUMPTION]
Derived from June 2026 actuals plus assumed H2-2026 organic net adds (placeholder).
| Line | June 2026 | H2-2026 net (assumed) | Jan 2027 opening |
|------|----------:|----------------------:|-----------------:|
| Residential | 4,324 | +126 | 4,450 |
| Business | 350 | +10 | 360 |
| Enterprise/DIA | 12 | +1 | 13 |
| Voice | 502 | +10 | 512 |

### D.3 ARPU growth [ASSUMPTION]
Residential $74 → +2.0%/yr · Business $149 → +2.5%/yr · Enterprise $850/mo [PLACEHOLDER] → +2.0%/yr · Voice $32/mo [PLACEHOLDER] → +1.0%/yr.

### D.4 Churn (annual, on beginning balance) [ASSUMPTION]
Residential 11.0% · Business 8.0% · Enterprise 5.0% · Voice 14.0% (base case).

### D.5 Homes/businesses passed [PLACEHOLDER / ASSUMPTION]
Residential passings start 11,000 (Jan 2027); business passings start 1,250.
New passings/yr and take-rate ramp are on the Assumptions tab.

### D.6 Fully-loaded labor, opex ratios, capital allocations, depreciation lives
All are **[PLACEHOLDER]** / **[ASSUMPTION]** values documented on their respective
Excel tabs (Fully-Loaded Labor, Operating Expenses, Capital Plan, Equipment Refresh).
Depreciation is a labeled placeholder (composite lives pending fixed-asset detail).

---

## E. Items management must provide to replace placeholders

1. Actual residential / business / enterprise subscriber split at June 2026.
2. Audited/actual ARPU by product line and any promotional roll-off schedule.
3. Actual homes & businesses passed, and the grant-funded build footprint by year.
4. Actual fully-loaded labor rates (wages, benefit load %, workers' comp class rates).
5. Historical monthly churn and disconnect reason coding.
6. Transit, transport, pole-attachment, and voice-platform contract rates.
7. Existing net plant value and fixed-asset depreciation schedule (for D&A).
8. Grant award terms (match %, eligible costs, allowable operating/admin revenue).
9. Any existing debt, lease, or financing obligations (this model is unlevered).
10. Actual installation cost per drop and average trouble-ticket cost.

---

## F. Actual Q2-2026 financials [ACTUAL — source #2] and assumption-conflict log

### F.1 Actual Q2-2026 income statement (annualized on a YTD/H1 basis, ×2)
| Item | Annualized | Tag |
|------|-----------:|-----|
| Total operating revenue | $4,130,718 | [ACTUAL] |
| Total operating expense (excl. D&A) | $4,271,408 | [ACTUAL] |
| EBITDA (op. income + D&A) | −$140,688 | [CALC from ACTUAL] |
| Depreciation & amortization | $362,804 | [ACTUAL] |
| Operating income (loss) | −$503,492 | [ACTUAL] |
| Interest expense (existing debt) | $464,220 | [ACTUAL] |
| Grant income (nonoperating) | $1,063,160 | [ACTUAL] |
| Net income (grant-supported) | ~$512,854 | [ACTUAL] |

Revenue detail (annualized): residential broadband $3.44M, residential voice $96K,
residential Wi-Fi $2.9K, residential other $168K, business broadband $455K, business
voice $29K, dark fiber $10K.

### F.2 Grant awards [ACTUAL — source #2]
CAB 2.0: Hoke $3,295,657 + Scotland $1,932,610 + Robeson $3,116,391 = **$8,344,658**;
NC Stop GAP: **$2,812,776** ($1.6M reimbursed); BTAP: **$419,000**. Total identified
awards ≈ **$11,576,434**. $2M+ underground new-build identified as eligible reimbursement.

### F.3 Conflict-resolution log
Per instruction, conflicts between the earlier engagement assumptions and the actual
Q2-2026 data are logged here with the chosen value and rationale (not silently overridden):

| # | Item | Prior assumption | Actual (source #2) | Resolution |
|---|------|------------------|--------------------|------------|
| 1 | 2027 starting revenue | ~$6.66M (built from subs × ARPU) | ~$4.13M run-rate | **Use actual.** Recalibrated ARPU/revenue so the plan starts from the actual run-rate. |
| 2 | Residential ARPU | $74 (total-residential proxy) | $66 broadband/mo | **Use actual $66** for broadband; residential voice/other modeled as separate lines. |
| 3 | Business ARPU | $149 | ~$110 broadband/mo | **Use actual ~$110.** |
| 4 | Voice ARPU | $32 | ~$21/mo | **Use actual ~$21.** |
| 5 | Managed Wi-Fi | 35% attach × $10 | ~$2.9K/yr total (negligible) | **Use actual;** Wi-Fi attach cut to ~1%. |
| 6 | Current EBITDA | +$0.90M (Year-1 base) | −$0.14M (slightly negative) | **Use actual baseline;** plan now shows the path from ~break-even to positive. |
| 7 | Depreciation | $2.4M/yr placeholder | $0.363M/yr actual | **Use actual** as the existing-plant base + new-capex composite. |
| 8 | Capital structure | Unlevered (no interest) | ~$0.464M/yr interest | **Add interest expense** to net income and cash flow. |
| 9 | Grant revenue | ~$50–70K/yr admin placeholder | ~$1.06M/yr grant income + $11.6M awarded | **Reclassify to nonoperating** grant income (declining) + grant capital reimbursement. |
| 10 | Dark fiber/wholesale | $180K→$500K placeholder | ~$10K/yr actual | **Use actual** as the starting point, growing modestly. |

### F.4 Items still to be provided (unchanged from §E)
Actual subscriber split by product, homes/businesses passed by year, fully-loaded labor
rates, and the fixed-asset/debt schedules remain the top placeholders to replace.
