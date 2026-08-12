# RIVR Tech — 2027 Master Pro Forma Budget

**Entity:** LREMC Technologies, LLC d/b/a RIVR Tech
**File:** `RIVR_Tech_2027_Master_Proforma_Budget.xlsx` (6 tabs, formula-driven, self-contained)

A single combined **revenue + expense** pro forma that merges the two source workbooks:

- **Revenue** ← `RIVR_Tech_2027_Revenue_Forecast` (Consolidated Revenue, Base scenario)
- **Expenses** ← `RIVR CFO-Style 2027 Budget Workbook` (department budget + the 2027 new-positions plan)

## Headline (FY 2027, Base)

| Line | Amount |
|---|---:|
| Total Operating Revenue | **$7,196,940** |
| Total Operating Expenses | **$7,696,812** |
| **Operating Income (EBIT)** | **($499,872)** — a ~$500K operating loss |
| EBITDA | ($358,998) |
| + Grant + nonoperating income | $1,158,084 |
| **Net Income (pre-tax)** | **$658,212** |
| EBIT margin / Net margin | −6.9% / 9.1% |

**The story for the CFO:** operations run at a ~$500K loss in 2027 and the company is
**net-positive only because of ~$1.16M of grant/nonoperating income.** The **8-FTE new-staffing
plan ($714K)** is what tips operations negative — without it, operations would run a small profit
(~$215K). Toggle it on/off on the Assumptions tab to see the swing.

## Tabs

| Tab | What it is |
|---|---|
| **Budget Dashboard** | KPI tiles + 4 charts (rev vs expense vs net, revenue mix, expense by group, monthly EBIT). |
| **Master Pro Forma** | The combined monthly P&L: Revenue − OpEx = EBIT → EBITDA → + other income → Net income, with Q1–Q4 and FY. |
| **Revenue Detail** | Monthly revenue by segment (Residential, Business, Dark Fiber, Hoke), imported from the revenue model. |
| **Expense Budget** | Department expense budget (2026 vs 2027) with a global % lever + per-line overrides; monthly spread. |
| **New Positions** | The 8-FTE 2027 staffing plan, ramped by start month; feeds the Expense Budget. |
| **Assumptions & Notes** | Control panel (global expense %, include-positions toggle, D&A, tax rate, grant/other income) + sources. |

## How to drive it

All inputs are on **Assumptions & Notes** and the input columns of **Expense Budget / New Positions**:
- **Global expense adjustment %** (`Assumptions!B6`) — flexes every department budget at once.
- **Include new positions** (`Assumptions!B7`, Yes/No) — adds/removes the $714K staffing plan.
- **Per-line expense overrides** — `Expense Budget` columns D (% override) and E (fixed $ adj).
- **D&A, tax rate, grant & nonoperating income** — Assumptions B8–B11.
- Revenue is imported as values (green) from the forecast model — re-import to refresh it.

## Method & notes

- Revenue segment nets tie exactly to the revenue model's Total net revenue ($7,196,940).
- Expenses use the CFO budget's **clean per-department / GL rollup ($7,696,812)**. ⚠️ The source
  Budget Builder's own total row **double-counts expenses** (its total = 2×expenses + revenue);
  this master uses the correct rollup, which ties to the CFO Dashboard and Department Summary.
- The new-positions plan ($714,483) is shown as its own line and **stripped out of the Fiber
  department** to avoid double counting. Base expense lines spread evenly; positions ramp by start month.
- Grant/nonoperating income is shown **below operating income** (the revenue model excludes it).
- Validation: **0 formula errors**, revenue/expense/EBIT/net all reconcile, Q1–Q4 = FY, cached
  values embedded and full-recalc-on-open enabled. Confirm GAAP treatment of grants (and any IRU)
  with the CFO/accountant.
