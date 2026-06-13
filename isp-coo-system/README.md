# ISP / Fiber Broadband — COO Executive Management System

A single, board-ready Excel workbook that lets a COO run **Sales, Operations, and
Financials** for a regional fiber/FTTH ISP, with reporting that rolls up cleanly to
the **CEO and Board of Directors**. Built for a **weekly executive review**, a
**monthly COO financial review**, and a **quarterly board report**.

> **Deliverable:** [`ISP_COO_Executive_Management_System.xlsx`](./ISP_COO_Executive_Management_System.xlsx)

Everything on the dashboards is a **live formula** that reads the input tabs. Staff
type data into the input tabs weekly; the dashboards, KPIs, RYG health indicators,
charts, and the board narrative update automatically.

---

## What's inside the workbook (21 tabs)

### Dashboards (read-only, auto-calculated)
| Tab | Purpose |
|-----|---------|
| **Exec_Dashboard** | One-page COO view: 22 KPI cards, RYG health, a MTD/YTD/Rolling-12 rollup table, top risks, decisions needed, auto-generated executive summary, and 4 trend charts. **Set the Reporting Month here (cell C5).** |
| **Sales_Dashboard** | Leads → qualified → connects, conversion, goal vs actual, pipeline by stage, sales by county/channel/rep, lost reasons. 6 charts. |
| **Ops_Dashboard** | Homes passed, footage, drops, splicing, installs, backlog, days-to-install, tickets, outages, project health, contractor performance. 6 charts. |
| **Financial_Dashboard** | Revenue, MRR, ARPU, CapEx/OpEx, budget vs actual, cash trend, grant pipeline, revenue & margin by product, capital spend by project. 8 charts. |
| **Board_Report** | Executive-format monthly COO report / quarterly board report. 8 sections, mostly auto-populated from the inputs. |

### Input tabs (structured Excel Tables + dropdowns — this is where staff type)
`Customer_Data` · `Sales_Data` · `Pipeline` · `Operations_Data` · `Project_Data` ·
`Financial_Data` · `Revenue_Detail` · `Sales_Targets` · `Grant_Data` ·
`Risk_Register` · `Board_Actions`

### Reference tabs
`Data_Dictionary` (every KPI defined + how it's calculated) · `User_Guide`
(weekly/monthly/quarterly processes) · `Assumptions` (assumptions + future-automation
recommendations). `Calc` and `Lists` are hidden engine tabs.

**By the numbers:** 24 charts · 11 Excel Tables · 35 dropdown validations · 908 formulas
(statically linted + recalculated, 0 errors) · RYG conditional formatting throughout.

---

## The one control you set: Reporting Month

On **Exec_Dashboard cell C5** there is a dropdown. Pick the month you are reporting on.
Every dashboard and the Board Report follow that selection for This-Month / MTD / YTD /
Rolling-12 math. (A period index in D5 is derived automatically.)

---

## Weekly update process (≈20 min)

1. **Customer_Data** — confirm/adjust the current month row (Total Customers, New Sales, Disconnects, Homes Passed).
2. **Sales_Data** — add rows for connects closed this week (Month, County, Segment, Channel, Campaign, Rep, units, New MRR).
3. **Pipeline** — update opportunity **Stage**; mark Closed-Won / Closed-Lost (add a Lost Reason for losses).
4. **Operations_Data** — installs scheduled/completed, drops, splices, tickets, outages, avg days to install.
5. **Project_Data** — % Complete, Status, phase statuses, capital spent, any new Blocker.
6. **Risk_Register** — review scores/owners/mitigations; close resolved, add new.
7. **Board_Actions** — log decisions needed; update statuses.
8. Open **Exec_Dashboard** — confirm RYG health and the auto-summary read correctly.

## Monthly COO reporting process (≈45 min)

1. Complete the month in **Financial_Data** (Revenue, MRR, CapEx, OpEx, Labor, Contractor, Grant, Budget, Cash).
2. Complete **Revenue_Detail** rows for the month (revenue & COGS by product) for accurate margin-by-line.
3. Update **Grant_Data** drawdown statuses (Submitted / Approved / Partially Paid / Paid).
4. Set **Exec_Dashboard C5** to the closed month; review all four dashboards.
5. Open **Board_Report** — Section 1 (Executive Summary) + the financial/customer/ops tables auto-populate.
6. Edit the qualitative cells in Section 2 (Going Well / Behind / Needs Attention) for the month's narrative.
7. Print/PDF the **Board_Report** tab for distribution.

## Quarterly board reporting process

1. Run the monthly process for the quarter-end month (gives YTD figures through the quarter).
2. Review Board_Report Sections 3–8 (Financial, Customer & Ops, Project Updates, Grant Summary, Risks, Decisions).
3. Refresh the Section-2 narrative for the quarter; confirm Decisions Needed reflects board-level asks.
4. Export Board_Report (and optionally each dashboard) to PDF: **File ▸ Export ▸ PDF** or **Print ▸ Save as PDF**.

---

## Reading the health colors

- 🟢 **GREEN** = on/above target · 🟡 **YELLOW** = watch / within tolerance · 🔴 **RED** = off target, act.
- Thresholds are documented in **Data_Dictionary** and encoded in each KPI card's status formula.
- To change a threshold, edit the `IF()` in the small status cell beneath the KPI value.

## Adding rows / new months

- Input tabs are **Excel Tables** — type under the table and it expands automatically.
- Rollup formulas read rows 4–1003 on each input tab, so new rows are picked up with **no formula edits**.
- For a new fiscal year: copy the workbook, clear input rows, reset `Sales_Targets` and budgets.

---

## ISP / fiber terminology used

Homes passed · take rate · drops · installs · activations · churn · ARPU · MRR ·
enterprise sales · DIA (Dedicated Internet Access) · construction footage · make-ready ·
permitting · splicing · ONT · grant reimbursement · CAB · BEAD · capital project ·
service area · county-level reporting.

---

## Assumptions (summary)

Full list is on the **Assumptions** tab. Key ones:

- Profile: a regional fiber ISP across southeastern NC counties (Robeson, Hoke, Cumberland, Scotland, Bladen, Columbus), part-funded by BEAD / CAB / ARPA / State / RDOF.
- Fiscal year shown is **Jul-2025 → Jun-2026**; current reporting month defaults to **Jun-2026**.
- **Sample data is illustrative** and seeded for realism — replace with your actuals; all formulas stay valid.
- Revenue = total billed (recurring + non-recurring); OpEx excludes capitalized build; CapEx = capitalized construction (contractor cost shown separately).
- Cost/Install ≈ contractor cost ÷ installs; Cost/Home-Passed ≈ CapEx ÷ homes passed added — directional unit economics.
- Install backlog = YTD scheduled − YTD completed; churn = monthly disconnects ÷ prior-month customers (logo churn).
- Risk score = Likelihood × Impact (1–5 each); RED ≥ 15, YELLOW ≥ 8. RYG thresholds are tunable defaults.

## Recommendations for future automation (summary)

Full list is on the **Assumptions** tab. Highlights:

1. Connect input tabs to source systems (billing/CRM, OSS/field service, GIS/construction, accounting) via **Power Query** for scheduled refresh.
2. Publish dashboards in **Power BI / Looker Studio** using this workbook as the data model.
3. Add a subscriber-event ledger to derive cohorts, **revenue churn**, and LTV.
4. Automate **grant-drawdown** tracking against milestones with reimbursement-aging and cash-timing alerts.
5. Add operational SLAs (install SLA %, outage MTTR) and auto-graded contractor scorecards.
6. Auto-save a dated **PDF of Board_Report** to the board folder each month (Power Automate).
7. Add a rolling **13-week cash-flow** model for treasury off the same Financial & Grant inputs.

---

## Regenerating the workbook

The workbook is generated by stdlib + `openpyxl` Python scripts in [`build/`](./build):

```bash
pip install openpyxl
cd build && python build_workbook.py
# → ../ISP_COO_Executive_Management_System.xlsx
```

- `build/styles.py` — design system (palette, fonts, KPI cards, headers).
- `build/data.py` — schema + a full fiscal year of illustrative sample data.
- `build/build_workbook.py` — input tabs, Calc engine, 4 dashboards, charts, conditional formatting.
- `build/build_part2.py` — Board Report + Data Dictionary + User Guide + Assumptions.
- `build/lint_formulas.py` — static formula linter (sheet refs, balanced parens/quotes).

Formulas were validated two ways: a static lint (908 formulas, 0 issues) and a full
recalculation via the `formulas` engine (0 runtime errors).
