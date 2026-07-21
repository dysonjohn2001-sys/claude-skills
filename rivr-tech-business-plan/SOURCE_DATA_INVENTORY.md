# RIVR Tech Five-Year Business Plan — Source-Data Inventory & Assumption Log

**Prepared:** 2026-07-21
**Entity:** LREMC Technologies, LLC d/b/a RIVR Tech
**Planning period:** FY2027–FY2031

---

## A. Working-directory source scan

A full scan of the working directory (`/home/user/claude-skills`) was performed for
any RIVR Tech / LREMC company files (financials, subscriber reports, GL exports,
capital schedules, staffing rosters, rate cards, grant award letters).

**Result: NO company-specific source files were found.** The working directory
contains only the `claude-skills` open-source library. Therefore **no internal
RIVR Tech data was available to verify**, and this plan is built entirely from:

1. The figures supplied in the engagement request (treated as the only **ACTUAL** inputs), and
2. Clearly-labeled **MANAGEMENT ASSUMPTIONS** and **CALCULATED PROJECTIONS**.

No conflicting source values were encountered (there were no competing sources).
Every non-supplied number in this plan is a placeholder and is flagged as such.

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

## F. Assumption-conflict log

**No conflicts identified.** No competing source values existed. Should management
supply actuals that differ from the placeholders above, log the conflict here with
the chosen value and rationale before overriding the model.
