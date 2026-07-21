# RIVR Tech — Five-Year Business Plan (FY2027–FY2031)

**LREMC Technologies, LLC d/b/a RIVR Tech** · fiber-optic broadband, southeastern North Carolina
Prepared 2026-07-21 for the CEO, Executive Leadership Team, and Board of Directors.

## Deliverables

| File | What it is |
|------|-----------|
| `RIVR_Tech_Five_Year_Business_Plan_2027-2031.docx` | Full board-ready business plan (16 sections + appendices). |
| `RIVR_Tech_Five_Year_Financial_Model_2027-2031.xlsx` | 18-tab, formula-driven financial model with a working scenario selector. |
| `RIVR_Tech_Five_Year_Executive_Presentation_2027-2031.pptx` | 14-slide executive presentation with native charts. |
| `SOURCE_DATA_INVENTORY.md` | Source-data inventory, data-classification legend, and assumption log. |

## How the numbers reconcile

All three documents are generated from a single source of truth, `model.py`, so they
agree to the dollar (within rounding). The Excel workbook re-derives everything with
**live formulas** — nothing calculated is hard-coded — and was validated by recalculating
every formula and comparing against the model (0 error cells; all key rows match).

### Data classification
`[ACTUAL]` supplied (unaudited) · `[ASSUMPTION]` editable · `[CALC]` derived ·
`[TARGET]` recommended · `[PLACEHOLDER]` pending management input. In the Excel model,
**blue** = input, **orange** = placeholder, **green** = key output, white = formula.

### Base-case headlines
- Revenue $6.7M → $14.2M; EBITDA margin ~14% → ~28% (EBITDA-positive every year).
- Internet subscribers ~4,800 → ~11,400; headcount 18 → 39.
- Capital: $10M/yr, $50M/5yr; ~$48.9M deployed, balance held as reserve.
- Equipment refresh: $400K/yr, $2M/5yr (inside the $10M; adjustable to outside).

## Scenario selector (Excel)
Open the **Scenario Selector** tab and choose Base / Conservative / Aggressive from the
drop-down; every tab recomputes via `CHOOSE`. A second toggle moves the equipment-refresh
program inside or outside the $10M allocation.

## Reproducing the files
```
python3 build_excel.py   # → RIVR_Tech_Five_Year_Financial_Model_2027-2031.xlsx
python3 build_word.py    # → RIVR_Tech_Five_Year_Business_Plan_2027-2031.docx
python3 build_pptx.py    # → RIVR_Tech_Five_Year_Executive_Presentation_2027-2031.pptx
python3 qc_check.py      # 14-point QC checklist (all PASS)
```
Requires `openpyxl`, `python-docx`, `python-pptx` (and `formulas` for QC recalculation).

## Important caveats
- No RIVR Tech internal source files were available; every non-supplied figure is a
  clearly-labeled assumption or placeholder. **Replace placeholders with actuals before
  board reliance.** See `SOURCE_DATA_INVENTORY.md` §E for the priority list.
- The model is unlevered (no debt/financing) and applies no entity income tax (LLC
  pass-through) — both are labeled placeholders.
- Depreciation is a labeled placeholder pending a fixed-asset study.
- Automated document rendering (LibreOffice) was unavailable in the build environment;
  the workbook was instead validated by full formula recalculation, and all three files
  were validated structurally and for content.
