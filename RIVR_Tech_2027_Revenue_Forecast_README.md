# RIVR Tech — 2027 Revenue Forecast Model

**Entity:** LREMC Technologies, LLC d/b/a RIVR Tech
**Business:** Rural broadband & fiber-optic infrastructure — Robeson, Hoke, Scotland, Cumberland & surrounding NC counties
**Forecast period:** January 1 – December 31, 2027
**Workbook:** `RIVR_Tech_2027_Revenue_Forecast.xlsx` (11 tabs, fully formula-driven)

> ✅ **Now calibrated to H1 2026 actuals.** The residential and business assumptions are derived
> from your Q1+Q2 2026 income statement (new **2026 Actuals (H1)** tab). Dark fiber is set to the
> actual run-rate, and the **Hoke County project (+$57,000/mo)** is included for 2027. Growth
> assumptions and the dark-fiber contract detail remain editable placeholders — see below.

### What changed in this version (actuals incorporated)

- **New tab `2026 Actuals (H1)`** — your full income statement (Q1, Q2, YTD) with derived monthly
  run-rates and annualized figures. Totals compute from the line items (may differ ~$1 from the
  form due to rounding in the source).
- **Residential & business recalibrated from actuals.** Beginning subscribers are now derived as
  *actual broadband revenue ÷ ARPU* (≈ **4,048 residential**, **249 business** — vs. the old
  placeholder 12,000 / 800). Voice and "other" per-customer/fixed amounts are set from the actual
  H1 lines. Because the base is ~3× smaller, monthly gross adds were reduced (250→60 residential)
  so growth stays realistic; **gross adds is the main growth lever to set to your plan.**
- **Dark fiber set to the actual run-rate** ($1,595/mo ≈ $19K/yr). The elaborate placeholder
  contracts were replaced by one run-rate row — replace it with your real DF agreements and the
  IRU/escalation/expiration engine reactivates.
- **Hoke County project added:** +$57,000/month for all of 2027 (editable amount + start month on
  Key Assumptions), flowing into Consolidated, Scenario, Dashboard, and Annual Summary.
- **Margin Calculator recalibrated** to your real cost structure: variable % = actual COGS/revenue
  (**14.8%**), fixed costs = actual operating expense annualized (**≈$3.99M**).

**Resulting Base-case 2027 net revenue ≈ $5.16M** (Residential 75% · Hoke 13% · Business 11% ·
Dark fiber <1%), a **$5.44M December ARR run-rate**, and a **7.9% operating margin**.

---

## 1. How to update assumptions (read this first)

The model is designed so management **never edits a forecast formula** — you only change inputs.

| Cell style | Meaning | Do you edit it? |
|---|---|---|
| **Light-blue fill, blue text** | Editable input | ✅ Yes |
| **Yellow fill** | Key assumption / must-fill placeholder | ✅ Yes — required |
| **Grey fill, black text** | Calculated formula | ❌ No |
| **Green text** | Link pulled from another tab | ❌ No |

**All inputs live on the `Key Assumptions` tab.** Steps:

1. **Pick the scenario.** `Key Assumptions` cell **B4** — dropdown: *Base / Conservative / Aggressive*. This single cell re-drives every forecast tab and the dashboard.
2. **Residential drivers** — rows 16–31 (beginning subscribers, gross adds, churn %, ARPU, ARPU step-up month/%, installation, upgrades, discounts, bad-debt, revenue-recognition convention).
3. **Business drivers** — rows 35–57 (beginning customers, small-biz & enterprise adds, churn, ARPU, static IP / managed Wi-Fi / voice / DIA rates, construction & activation, discounts, beginning enterprise count).
4. **Dark-fiber globals** — rows 60–61 (default IRU recognition method, default O&M %).
5. **Dark-fiber contracts** — the table at rows 65–90 (25 contract slots). Fill one row per agreement: name, type, status, dates, MRC, escalation, one-time construction/activation, IRU payment/term/method, O&M, renewal probability. **Each contract flows automatically into the Dark Fiber Forecast based on its start and end dates** — no formula editing needed.
6. **Scenario multipliers** — rows 8–10 let you tune how Conservative and Aggressive differ from Base (additions, churn, ARPU, dark-fiber revenue, contract timing, installation/construction).

Because the workbook is set to **recalculate on open**, saved changes take effect the next time the file is opened (or press **F9** / Ctrl+Alt+F9 to force recalc immediately in Excel).

---

## 2. Tab guide

| # | Tab | Purpose |
|---|---|---|
| 1 | **Executive Dashboard** | 15 KPI tiles + 7 charts (revenue trend, segment mix, subscriber trends, MRR trend, scenario comparison). |
| 2 | **Key Assumptions** | The only tab you edit. All inputs, scenario selector, multiplier table, the 25-row dark-fiber contract register, and the Hoke County project inputs. |
| 3 | **2026 Actuals (H1)** | Your Q1+Q2 2026 income statement with monthly run-rates; feeds the 2027 calibration. |
| 4 | **Residential Forecast** | Monthly customer roll-forward + recurring/one-time revenue, MRR, ARR, effective ARPU. |
| 5 | **Business Forecast** | Small-biz + enterprise roll-forward; recurring separated from installation/construction one-time. |
| 6 | **Dark Fiber Forecast** | Contract-level monthly revenue, IRU recognition, remaining contract value, and RED/YELLOW/GREEN expiration alerts. |
| 7 | **Consolidated Revenue** | All segments + Hoke project combined, with quarterly (Q1–Q4) and full-year subtotals, MoM growth, revenue/day, MRR, ARR, and segment mix. |
| 8 | **Scenario Analysis** | Three fully independent projections (Conservative / Base / Aggressive) with an annual comparison. |
| 9 | **Annual Summary** | One-page management summary + commentary boxes. |
| 10 | **Margin Calculator** | Cost-Volume-Profit tool: enter costs, solve the revenue needed for any target profit. |
| 11 | **Data Dictionary** | Plain-English definition of every term and metric. |

### Using the Margin Calculator (tab 10)

The revenue model doesn't know your costs, so this tab lets you enter them and answers
*"what revenue do we need for an X% profit?"* It uses standard Cost-Volume-Profit math on
**pre-tax operating profit (EBIT)**:

```
Operating profit = Revenue × (1 − variable cost %) − fixed costs
Required revenue for a target margin m = Fixed costs ÷ (1 − variable cost % − m)
Required revenue for a target profit $P = (Fixed costs + P) ÷ (1 − variable cost %)
Breakeven revenue                      = Fixed costs ÷ (1 − variable cost %)
```

**Inputs (now calibrated from H1 2026 actuals — editable):**
- `B5` — variable operating cost % (linked to actual COGS/revenue = **14.8%**; overwrite to plan)
- `B7:B11` — fixed annual costs (linked to actual operating expense, annualized = H1 × 2 ≈ **$3.99M**)
- `B29` — your target profit **margin** (e.g. 10%) → `B30` returns the required revenue
- `B36` — a target profit in **dollars** → `B37` returns the required revenue
- `B17` — optional: override the forecast revenue to test any level

**Worked example (calibrated costs: 14.8% variable, ≈$3.99M fixed):**
- Contribution margin = 85.2%; **breakeven ≈ $4.68M**.
- **For a 10% profit margin you need ≈$5.31M of revenue** ( $3.99M ÷ (1 − 0.148 − 0.10) ).
- The Base 2027 forecast is **$5.16M**, delivering a **7.9% operating margin (≈$0.41M profit)** —
  about **$145K of revenue short** of the 10% target. Closing that gap ≈ 2–3 months of Hoke revenue,
  a small ARPU increase, or ~200 net residential adds.
- Section D tabulates 0%→30% target margins; Section E shows the operating margin at each
  scenario's revenue.

> Costs are calibrated from your H1 2026 actuals (annualized) and remain editable. Variable = COGS;
> fixed = all other operating expense incl. D&A. Excludes interest, income taxes, and nonoperating
> grant activity — confirm the 2027 cost plan with the CFO.

---

## 3. What's calibrated vs. still needs management input

**Calibrated from your H1 2026 actuals (green cells — verify, don't re-key):** beginning residential
subscribers (`B16`), beginning business customers (`B35`), residential voice & other (`B29`, `B30`),
business voice (`B47`), and all Margin Calculator costs.

**Still requires a management decision (highlighted):**

| Location | Input | Current value | Action |
|---|---|---|---|
| `Key Assumptions` B17 | Residential monthly gross adds | 60 (≈ churn, ~flat) | **Set your growth plan** — the single biggest lever |
| `Key Assumptions` B36–B37 | Business gross adds (small / enterprise) | 4 / 1 | Set your growth plan |
| `Key Assumptions` B18 / B38 | Residential / business monthly churn % | 1.5% / 1.0% | Confirm against actual churn |
| `Key Assumptions` B21 / B41 | Residential / business ARPU | $74 / $149 | Confirm (drives the implied sub counts) |
| `Key Assumptions` B93–B94 | **Hoke County project** revenue / start month | $57,000 / month 1 | Confirm amount & timing |
| `Key Assumptions` rows 66–90 | **Dark-fiber contracts** (1 run-rate row, 24 blank) | $1,595/mo aggregate | **Replace with real agreements** to grow DF & activate IRU logic |
| `Key Assumptions` B60–B61 | Default IRU recognition method; default O&M % | Straight-line; 10% | Confirm with accountant |
| `Key Assumptions` rows 8–10 | Conservative / Aggressive scenario multipliers | ±15% adds, etc. | Tune to management view |
| `Margin Calculator` B5–B11 | 2027 cost plan (pre-filled from actuals) | 14.8% var / $3.99M fixed | Confirm / enter plan |
| `Annual Summary` A21–A32 | Management commentary | blank | Write commentary |

> **IRU accounting flag:** The treatment of upfront IRU proceeds (recognize immediately vs.
> straight-line over the term vs. a manual schedule) **materially changes reported revenue** and
> **must be reviewed by RIVR Tech's CFO and external accountant under ASC 606** before these
> figures are relied upon. The current single DF row carries no IRU; add real contracts to use it.

---

## 4. Formula-validation summary

The workbook was recalculated with an independent formula engine and every check below passed.

| # | Validation test | Result |
|---|---|---|
| 0 | 2026 Actuals tab ties to the income statement | ✅ Total op rev $2,170,915, Net income $222,441 (±$1 source rounding) |
| 1 | Beginning counts calibrated from actual broadband ÷ ARPU | ✅ Res ≈ 4,048; Bus ≈ 249 |
| 2 | Each month's beginning = prior month's ending | ✅ Chain verified Jan→Dec (both segments) |
| 3 | Customer counts never negative | ✅ `MAX(0, …)` guards; 0 negative months |
| 4 | Monthly segment revenue sums to consolidated | ✅ Σ segments + Hoke = $5,162,584 = Consolidated |
| 5 | Quarterly totals = the three constituent months | ✅ Q1+Q2+Q3+Q4 = FY |
| 6 | Annual totals = Jan…Dec | ✅ Σ 12 months = FY |
| 7 | Dark-fiber revenue = actual run-rate | ✅ $19,140/yr = $1,595/mo × 12 |
| 8 | Hoke project = $57,000 every month | ✅ $684,000 FY, in Consolidated / Scenario / Dashboard / Annual |
| 9 | Scenario selection updates the forecast | ✅ Conservative $5.51M / Base $5.16M / Aggressive $6.17M |
| 10 | MRR excludes one-time; ARR = Dec MRR × 12 | ✅ Dec ARR = $5.44M |
| 11 | Dashboard reconciles to underlying tabs | ✅ Dashboard total tile = Consolidated FY = $5,162,584 |
| 12 | No `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#N/A` | ✅ 0 error cells across 2,669 formulas |

*Engineering note:* The file ships with cached results **and** live formulas, and is flagged to
fully recalculate on open, so it displays correct numbers immediately and refreshes the moment any
assumption changes.

---

## 5. Executive interpretation — Base scenario (calibrated to H1 2026 actuals)

**Headline:** Base-case 2027 net revenue is **≈ $5.16 million**, exiting December at a
**≈ $5.44 million ARR run-rate**, on a base of **~4,050 residential** and **~250 business**
customers implied by the H1 2026 broadband run-rate.

- **Primary revenue driver — Residential.** Residential contributes **$3.89M (75%)** of net revenue,
  a subscriber-scale story anchored to the actual ~$300K/mo broadband run-rate at a $74 ARPU. Because
  the base is now grounded in actuals, the model's biggest uncertainty is **net adds**, not the
  starting point.
- **The Hoke County project is now the #2 line.** At $57,000/mo it adds **$684K (13%)** for 2027 —
  larger than the entire business segment and ~36× the current dark-fiber book. Its timing (`B94`)
  and amount (`B93`) are worth confirming, as it materially moves both revenue and margin.
- **Business & dark fiber are small.** Business broadband is **$0.57M (11%)**; dark fiber is set to
  the actual **$19K/yr** run-rate (<1%). Dark fiber is upside optionality — populate the contract
  table with real agreements (and their IRUs) to grow it.
- **Growth is modeled flat by default.** With gross adds ≈ monthly churn, the base holds subscribers
  roughly steady (residential 4,048 → 4,072). **This is a conservative placeholder** — set
  `Key Assumptions B17` (residential adds) and `B36/B37` (business adds) to management's real plan;
  it is the single largest swing factor in the forecast.
- **Churn & ARPU sensitivity.** Residential churn (~1.5%/mo) roughly offsets current adds, so
  retention directly determines whether the base grows or shrinks. ARPU multiplies the whole base —
  the mid-year +3% step and any pricing move are high-leverage, low-effort levers.
- **Profitability.** Against the actual cost structure (14.8% variable, ~$3.99M fixed), the base
  forecast yields a **7.9% operating margin (~$0.41M)** — **below a 10% target by ~$145K of revenue**.
  Breakeven is ~$4.68M. Note H1 2026 was an operating **loss**; 2027 turns positive largely on the
  Hoke project and a full year of the current base, so both are load-bearing assumptions. (Grant /
  BTAP / CAB nonoperating income, which drove H1 net income, is **not** in this revenue-only model.)

**Scenario range:** Conservative **$5.51M** → Base **$5.16M** → Aggressive **$6.17M** — a **±6–7%**
band around the base, driven mostly by residential adds/churn and ARPU. (Hoke is held constant across
scenarios as a contracted project.)

---

## 6. Files delivered

- `RIVR_Tech_2027_Revenue_Forecast.xlsx` — the working model.
- `RIVR_Tech_2027_Revenue_Forecast_README.md` — this document (update guide, placeholder inventory, validation summary, executive interpretation).
