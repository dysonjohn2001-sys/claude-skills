# RIVR Tech — 2027 Sales Goals (Floor / Target / Stretch)

**Files:** `RIVR_Tech_2027_Sales_Goals.xlsx` (3 tabs, formula-driven) + `RIVR_Tech_2027_Sales_Goals.docx` (Word writeup).

## The model

Three monthly new-sales tiers, each sale worth **$65/month recurring**. Revenue compounds as sales stack up through the year.

| Tier | New sales / mo | FY new sales | FY revenue (in-year) | Dec MRR | Dec ARR run-rate |
|---|---:|---:|---:|---:|---:|
| **Floor** | 150 | 1,800 | $760,500 | $117,000 | $1,404,000 |
| **Target** | 175 | 2,100 | $887,250 | $136,500 | $1,638,000 |
| **Stretch** | 200 | 2,400 | $1,014,000 | $156,000 | $1,872,000 |

Stretch vs Floor: **+600 sales, +$253,500 in-year revenue, +$468,000 of exit ARR.**

## How it works

- Each month the team books new sales (150 / 175 / 200 depending on tier).
- Every sale adds **$65 of monthly recurring revenue (MRR)** and keeps billing every following month.
- **MRR each month = active customers × $65**; **in-year revenue = the sum of the 12 monthly MRR figures**; **exit ARR = December MRR × 12**.
- By December, Stretch reaches 2,400 cumulative sales = $156,000 MRR = $1,872,000 ARR.

## Tabs

| Tab | What it is |
|---|---|
| **Goals Dashboard** | KPI tiles (FY revenue, Dec MRR/ARR, sales/mo per tier) + 4 charts (MRR ramp by tier, FY revenue by tier, active customers, December ARR). |
| **Sales Goals** | Monthly build by tier: new sales, active customers (cumulative), new MRR added, monthly MRR — with quarterly + FY totals and a by-tier annual summary. |
| **Assumptions** | Editable inputs: the three sales tiers, $/sale/month, optional beginning base, optional churn %. |

## Notes

- New sales are modeled **flat** at each tier's monthly rate (no seasonal ramp in this version).
- **Churn = 0** and **beginning base = 0** by default, so figures reflect gross new 2027 sales only — both are optional inputs on the Assumptions tab.
- These are sales-activity goals; the revenue shown is the recurring revenue those sales generate within 2027. Change any blue input (tiers, rate, churn) and the goals, totals, and charts update on open.
