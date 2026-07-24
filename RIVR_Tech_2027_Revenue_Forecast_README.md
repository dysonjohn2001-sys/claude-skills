# RIVR Tech — 2027 Revenue Forecast Model

**Entity:** LREMC Technologies, LLC d/b/a RIVR Tech
**Business:** Rural broadband & fiber-optic infrastructure — Robeson, Hoke, Scotland, Cumberland & surrounding NC counties
**Forecast period:** January 1 – December 31, 2027
**Workbook:** `RIVR_Tech_2027_Revenue_Forecast.xlsx` (10 tabs, fully formula-driven)

> ⚠️ **Every number in this model is built on PLACEHOLDER assumptions.** Nothing here is a
> real RIVR Tech figure. Replace the highlighted inputs before using the output for any
> board, lender, or budgeting purpose. See the *Placeholder Inventory* below.

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
| 2 | **Key Assumptions** | The only tab you edit. All inputs, scenario selector, multiplier table, and the 25-row dark-fiber contract register. |
| 3 | **Residential Forecast** | Monthly customer roll-forward + recurring/one-time revenue, MRR, ARR, effective ARPU. |
| 4 | **Business Forecast** | Small-biz + enterprise roll-forward; recurring separated from installation/construction one-time. |
| 5 | **Dark Fiber Forecast** | Contract-level monthly revenue, IRU recognition, remaining contract value, and RED/YELLOW/GREEN expiration alerts. |
| 6 | **Consolidated Revenue** | All segments combined, with quarterly (Q1–Q4) and full-year subtotals, MoM growth, revenue/day, MRR, ARR, and segment mix. |
| 7 | **Scenario Analysis** | Three fully independent projections (Conservative / Base / Aggressive) with an annual comparison. |
| 8 | **Annual Summary** | One-page management summary + commentary boxes. |
| 9 | **Margin Calculator** | Cost-Volume-Profit tool: enter costs, solve the revenue needed for any target profit. |
| 10 | **Data Dictionary** | Plain-English definition of every term and metric. |

### Using the Margin Calculator (tab 9)

The revenue model doesn't know your costs, so this tab lets you enter them and answers
*"what revenue do we need for an X% profit?"* It uses standard Cost-Volume-Profit math on
**pre-tax operating profit (EBIT)**:

```
Operating profit = Revenue × (1 − variable cost %) − fixed costs
Required revenue for a target margin m = Fixed costs ÷ (1 − variable cost % − m)
Required revenue for a target profit $P = (Fixed costs + P) ÷ (1 − variable cost %)
Breakeven revenue                      = Fixed costs ÷ (1 − variable cost %)
```

**Inputs (yellow, PLACEHOLDER — replace with RIVR Tech actuals):**
- `B5` — variable operating cost as a % of revenue (bandwidth, transport, commissions, processing)
- `B7:B11` — fixed annual costs (network O&M, salaries/G&A, sales & marketing, D&A, other)
- `B29` — your target profit **margin** (e.g. 10%) → `B30` returns the required revenue
- `B36` — a target profit in **dollars** → `B37` returns the required revenue
- `B17` — optional: override the forecast revenue to test any level

**Worked example (with the placeholder costs: 25% variable, $9.0M fixed):**
- Contribution margin = 75%; **breakeven = $12.0M**.
- **For a 10% profit margin you need $13.85M of revenue** ( $9.0M ÷ (1 − 0.25 − 0.10) ).
- The Base forecast is **$14.87M**, which delivers a **14.5% operating margin ($2.15M profit)** —
  already above the 10% target by ~$1.0M of revenue.
- Section D tabulates 0%→30% target margins; Section E shows the operating margin at each
  scenario's revenue (Conservative ≈10.4%, Base ≈14.5%, Aggressive higher).

> The placeholder cost figures make the demo sensible but are **not RIVR Tech numbers** — swap in
> real costs (and confirm the variable/fixed split with the CFO) before relying on the output.

---

## 3. Placeholder inventory — management must complete

All values below are **illustrative placeholders**, not RIVR Tech actuals. The four cells marked
**"PLACEHOLDER—UPDATE REQUIRED"** are highlighted yellow in the workbook; the dark-fiber rows are
prefixed *"PLACEHOLDER —"* in the contract name.

| Location | Input | Placeholder used | Action |
|---|---|---|---|
| `Key Assumptions` B16 | Beginning **residential** subscribers (12/31/2026) | 12,000 | **Enter actual** |
| `Key Assumptions` B35 | Beginning **business** customers (12/31/2026) | 800 | **Enter actual** |
| `Key Assumptions` B57 | Beginning **enterprise** customers (subset) | 50 | **Enter actual** |
| `Key Assumptions` B17–B30 | Residential adds / churn / ARPU / installation / upgrade / discount / bad-debt / other | see cells | Confirm or replace |
| `Key Assumptions` B36–B53 | Business adds / churn / ARPU / DIA / static-IP / Wi-Fi / voice / construction / activation | see cells | Confirm or replace |
| `Key Assumptions` B60–B61 | Default IRU recognition method; default O&M % | Straight-line; 10% | Confirm with accountant |
| `Key Assumptions` rows 66–90 | **All 25 dark-fiber contract rows** (6 sample rows populated, 19 blank) | 6 example contracts | **Replace with real agreements** |
| `Key Assumptions` rows 8–10 | Conservative / Aggressive scenario multipliers | ±15% adds, ±20% churn, etc. | Tune to management view |
| `Annual Summary` A21–A32 | Management commentary (changes / opportunities / risks / assumptions) | blank | Write commentary |

> **IRU accounting flag:** The treatment of upfront IRU proceeds (recognize immediately vs.
> straight-line over the term vs. a manual schedule) **materially changes reported revenue** and
> **must be reviewed by RIVR Tech's CFO and external accountant under ASC 606** before these
> figures are relied upon. The model defaults to straight-line and exposes the choice per contract.

---

## 4. Formula-validation summary

The workbook was recalculated with an independent formula engine and every check below passed.

| # | Validation test | Result |
|---|---|---|
| 1 | January beginning counts link to the 12/31/2026 inputs | ✅ Res Jan begin = KA B16 (12,000); Bus = KA B35 |
| 2 | Each month's beginning = prior month's ending | ✅ Chain verified Jan→Dec (both segments) |
| 3 | Customer counts never negative | ✅ `MAX(0, …)` guards; 0 negative months |
| 4 | Monthly segment revenue sums to consolidated | ✅ Σ segment nets = $14,870,324.61 = Consolidated |
| 5 | Quarterly totals = the three constituent months | ✅ Q1+Q2+Q3+Q4 = FY |
| 6 | Annual totals = Jan…Dec | ✅ Σ 12 months = FY |
| 7 | Dark-fiber revenue only during active contract periods | ✅ e.g. the 8/31/2027 contract drops out of Sep–Dec |
| 8 | Scenario selection updates the forecast | ✅ Conservative $13.92M / Base $14.87M / Aggressive $15.81M |
| 9 | MRR excludes one-time revenue | ✅ Jan MRR $1,110,365 < Jan net $1,130,069 |
| 10 | ARR run rate = December MRR × 12 | ✅ $1,246,937 × 12 = $14,963,246 |
| 11 | Dashboard reconciles to underlying tabs | ✅ Dashboard total tile = Consolidated FY |
| 12 | No `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#N/A` | ✅ 0 error cells across 2,452 formulas |

*Engineering note:* The file ships with cached results **and** live formulas, and is flagged to
fully recalculate on open, so it displays correct numbers immediately and refreshes the moment any
assumption changes.

---

## 5. Executive interpretation — Base scenario

**Headline:** Base-case 2027 net revenue is **≈ $14.87 million**, exiting December at a
**$14.96 million ARR run-rate** (December MRR $1.25M × 12).

- **Primary revenue driver — Residential.** Residential contributes **$11.69M (78.6%)** of net
  revenue. The business is a subscriber-scale story: ~12,000 beginning subs growing on ~250 gross
  adds/month against ~1.5% monthly churn, at a $74 ARPU that steps to ~$76 mid-year. Small changes
  in this segment move the whole forecast.
- **Revenue concentration.** Business broadband adds **$2.48M (16.7%)** and dark fiber **$0.70M
  (4.7%)**. The book is therefore **heavily concentrated in residential** — a strength for
  predictability but a single-segment dependency worth diversifying.
- **Recurring vs. one-time.** Revenue quality is high: **recurring ≈ $14.19M (95%+)** vs. one-time
  installation/construction/activation of **≈ $1.02M** and IRU recognition of **$0.075M**. The
  business is a subscription engine, not a project-revenue engine — MRR/ARR are the metrics that
  matter.
- **Churn sensitivity.** Residential churn is the model's sharpest lever. At ~1.5%/month the base
  loses ~180 subs/month to churn; the Conservative case (churn ×1.20) alone is a meaningful driver
  of the ~$0.95M downside gap. **Retention initiatives compound** — every tenth of a point of
  monthly churn avoided flows to ARR twelve-fold.
- **ARPU sensitivity.** The mid-year ARPU step (+3% in July) and the ARPU multiplier are second-order
  but reliable levers. Because ARPU multiplies the entire subscriber base, a 3% ARPU move is worth
  roughly the same as several months of net adds — pricing discipline is as valuable as acquisition.
- **Dark-fiber contract risk.** Dark fiber is small in dollars but **lumpy and concentrated**: a
  handful of contracts, several with one-time construction spikes (the model peaks in **March** on
  a $250K IRU build) and IRU proceeds whose accounting treatment swings recognized revenue. Two of
  the sample contracts carry **near-term expiration flags** (the 8/31/2027 public-safety lease shows
  YELLOW/RED). Renewal management and the CFO/accountant IRU decision are the key watch-items here.

**Scenario range:** Conservative **$13.92M** → Base **$14.87M** → Aggressive **$15.81M** — a
**±6–7%** band around the base, driven mostly by residential adds/churn and business/enterprise
sales pace.

---

## 6. Files delivered

- `RIVR_Tech_2027_Revenue_Forecast.xlsx` — the working model.
- `RIVR_Tech_2027_Revenue_Forecast_README.md` — this document (update guide, placeholder inventory, validation summary, executive interpretation).
