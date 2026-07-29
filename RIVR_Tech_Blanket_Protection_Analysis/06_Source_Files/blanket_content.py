# -*- coding: utf-8 -*-
"""
RIVR Tech — Blanket Residential Maintenance Protection Plan Analysis
Master content + compute module (single source of truth).

Evaluates a monthly Maintenance Protection Plan for ALL residential internet
customers at $3.99 (Scenario A) and $4.99 (Scenario B), across three enrollment
models (mandatory / opt-out / opt-in), with utilization, churn, and pay-per-visit
sensitivity.

ALL company-specific figures are labeled ASSUMPTIONS unless supplied by RIVR Tech.
Nothing here is legal, tax, accounting, or regulatory advice.
"""

COMPANY_LEGAL = "LREMC Technologies, LLC d/b/a RIVR Tech"
COMPANY_SHORT = "RIVR Tech"
REGION = "southeastern North Carolina"
DOC_VERSION = "v1.0 (Draft for Executive Review)"
DOC_DATE = "2026-07-29"
EFFECTIVE_DATE_PLACEHOLDER = "[EFFECTIVE DATE — TO BE SET BY EXECUTIVE TEAM]"
PLAN_NAME = "RIVR Tech Home Protection"
PREPARED_BY = "Finance / COO / Customer-Experience Working Team"

# Brand palette (assumed — replace with official RIVR Tech brand colors).
BRAND = {
    "primary": "0B3D5C", "secondary": "1B87B5", "accent": "36B39A",
    "dark": "10222E", "light": "EAF3F7", "warn": "C0562B", "good": "2E7D5B",
    "yellow": "C9A227", "gray": "6B7A82", "white": "FFFFFF",
}

# Subscriber levels to model
SUB_LEVELS = [4686, 5000, 5500, 6000, 7500, 10000]

# Enrollment participation rates to model
OPTOUT_RATES = [0.95, 0.85, 0.75, 0.60, 0.50]
OPTIN_RATES = [0.20, 0.30, 0.40, 0.50, 0.60]

# Utilization + cost sensitivity grids
UTIL_GRID = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40]
COST_GRID = [75, 100, 125, 150, 200, 250]

# Churn sensitivity grid (incremental ANNUAL churn caused by the fee)
CHURN_GRID = [0.0, 0.0025, 0.005, 0.010, 0.020, 0.030, 0.050]

# Pay-per-visit charges to compare
PPV_CHARGES = [75, 99, 125, 150]

PRICE_A = 3.99
PRICE_B = 4.99

# ---------------------------------------------------------------------------
# ASSUMPTIONS  (key, label, value, unit, is_assumption, note)
# ---------------------------------------------------------------------------
A_LIST = [
    ("current_subs",        "Current residential subscribers",          4686,  "count", True,  "Editable — starting residential internet accounts."),
    ("monthly_growth",      "Monthly subscriber growth",                0.010, "pct",   True,  "Assumption — ~12.7%/yr compounded."),
    ("arpu",                "Average residential ARPU (monthly)",       74.00, "usd",   False, "Provided."),
    ("price_a",             "Plan price — Scenario A (monthly)",        3.99,  "usd",   False, "Scenario A."),
    ("price_b",             "Plan price — Scenario B (monthly)",        4.99,  "usd",   False, "Scenario B."),
    ("enroll_pct",          "Enrollment % (driver)",                    0.40,  "pct",   True,  "Default driver — overridden per enrollment model."),
    ("churn_monthly",       "Baseline monthly disconnect/churn",        0.015, "pct",   True,  "Assumption — ~16.6%/yr baseline."),
    ("incr_churn_annual",   "Incremental annual churn from the fee",    0.010, "pct",   True,  "Driver — tested 0%-5%."),
    ("trouble_rate",        "% of customers generating a trouble call/yr", 0.30, "pct", True,  "Assumption."),
    ("cust_caused_pct",     "% of calls that are customer-caused",      0.45,  "pct",   True,  "Assumption — remainder are RIVR-network/equipment (free)."),
    ("util_expected",       "Expected annual covered-visit utilization",0.15,  "pct",   True,  "Share of ENROLLED members using a covered visit/yr."),
    ("tech_labor_hours",    "Technician labor time per call (hr)",      1.00,  "hours", True,  "On-site time."),
    ("tech_rate",           "Fully burdened technician rate (/hr)",     68.00, "usd",   True,  "Wages + benefits + burden."),
    ("dispatch_hours",      "Dispatch & scheduling time (hr)",          0.25,  "hours", True,  "Per truck roll."),
    ("vehicle_cost",        "Vehicle cost per truck roll",              22.00, "usd",   True,  "Depreciation + maintenance."),
    ("fuel_cost",           "Fuel per truck roll",                       9.00, "usd",   True,  "Assumption."),
    ("materials_cost",      "Average materials per call",               12.00, "usd",   True,  "Consumables/connectors."),
    ("repeat_dispatch",     "Repeat-dispatch rate",                     0.12,  "pct",   True,  "Share of calls needing a second roll."),
    ("cc_handling",         "Call-center handling cost per call",        6.00, "usd",   True,  "Per covered interaction."),
    ("billing_cost_yr",     "Billing & collection cost per member/yr",   3.00, "usd",   True,  "Invoice, posting, servicing."),
    ("price_increase",      "Annual price increase",                    0.03,  "pct",   True,  "For 5-year forecast."),
    ("bad_debt",            "Bad-debt / nonpayment %",                  0.03,  "pct",   True,  "Uncollectible plan revenue."),
    ("covered_visits",      "Covered visits allowed annually",          2,     "count", False, "Standard tier default."),
    ("billing_impl",        "Billing-system implementation (one-time)", 25000, "usd",   True,  "NISC codes, config, testing."),
    ("launch_cost",         "Initial launch expense (one-time)",        15000, "usd",   True,  "Comms, print, legal review support."),
    ("program_mgmt",        "Ongoing program management (annual)",      18000, "usd",   True,  "Reporting, QA, admin oversight."),
    ("cust_comm_annual",    "Customer communication expense (annual)",   6000, "usd",   True,  "Bill inserts, email, notices."),
    ("ppv_collection",      "Pay-per-visit collection rate",            0.80,  "pct",   True,  "Share of billed visit fees collected."),
]
A = {r[0]: r[2] for r in A_LIST}


def cost_per_call(a=None):
    a = a or A
    labor = (a["tech_labor_hours"] + a["dispatch_hours"]) * a["tech_rate"]
    base = labor + a["vehicle_cost"] + a["fuel_cost"] + a["materials_cost"]
    return base * (1 + a["repeat_dispatch"])


def cost_breakdown_per_call(a=None):
    a = a or A
    m = 1 + a["repeat_dispatch"]
    return {
        "labor": (a["tech_labor_hours"] + a["dispatch_hours"]) * a["tech_rate"] * m,
        "vehicle": a["vehicle_cost"] * m,
        "fuel": a["fuel_cost"] * m,
        "materials": a["materials_cost"] * m,
    }


def per_member(price, util=None, cpc=None, a=None):
    """Annual per-enrolled-member economics."""
    a = a or A
    util = a["util_expected"] if util is None else util
    cpc = cost_per_call(a) if cpc is None else cpc
    rev = price * 12
    covered = util * cpc
    cc = util * a["cc_handling"]
    admin = a["billing_cost_yr"]
    bad = rev * a["bad_debt"]
    contribution = rev - covered - cc - admin - bad
    return {
        "rev": rev, "covered": covered, "cc": cc, "admin": admin, "bad_debt": bad,
        "contribution": contribution, "margin_pct": contribution / rev if rev else 0,
    }


def breakeven_util(price, cpc=None, a=None):
    """Utilization at which per-member contribution = 0."""
    a = a or A
    cpc = cost_per_call(a) if cpc is None else cpc
    rev = price * 12
    admin = a["billing_cost_yr"]
    bad = rev * a["bad_debt"]
    denom = cpc + a["cc_handling"]
    return (rev - admin - bad) / denom if denom else 0


def program_totals(price, subs, enroll_pct, util=None, cpc=None,
                   incr_churn=None, churn_base="enrolled", a=None, include_onetime=True):
    """Annual program totals at a subscriber level and enrollment rate."""
    a = a or A
    util = a["util_expected"] if util is None else util
    cpc = cost_per_call(a) if cpc is None else cpc
    incr_churn = a["incr_churn_annual"] if incr_churn is None else incr_churn
    enrolled = subs * enroll_pct
    pm = per_member(price, util, cpc, a)

    gross_monthly = enrolled * price
    gross_annual = gross_monthly * 12
    covered_expense = enrolled * pm["covered"]
    cc_expense = enrolled * pm["cc"]
    admin_expense = enrolled * pm["admin"]
    bad_debt_expense = gross_annual * a["bad_debt"]

    # covered expense components
    bd = cost_breakdown_per_call(a)
    covered_calls = enrolled * util
    labor_exp = covered_calls * bd["labor"]
    vehicle_exp = covered_calls * bd["vehicle"]
    fuel_exp = covered_calls * bd["fuel"]
    materials_exp = covered_calls * bd["materials"]

    fixed = a["program_mgmt"] + a["cust_comm_annual"]
    onetime = (a["billing_impl"] + a["launch_cost"]) if include_onetime else 0

    affected = enrolled if churn_base == "enrolled" else subs
    churn_loss = affected * incr_churn * a["arpu"] * 12

    contribution_margin = gross_annual - covered_expense - cc_expense - admin_expense - bad_debt_expense
    net_annual = contribution_margin - fixed - onetime - churn_loss
    return {
        "enrolled": enrolled, "covered_calls": covered_calls,
        "gross_monthly": gross_monthly, "gross_annual": gross_annual,
        "net_monthly": net_annual / 12, "net_annual": net_annual,
        "rev_per_sub": gross_annual / subs if subs else 0,
        "covered_expense": covered_expense, "cc_expense": cc_expense,
        "admin_expense": admin_expense, "bad_debt_expense": bad_debt_expense,
        "labor_exp": labor_exp, "vehicle_exp": vehicle_exp, "fuel_exp": fuel_exp,
        "materials_exp": materials_exp, "fixed": fixed, "onetime": onetime,
        "churn_loss": churn_loss, "contribution_margin": contribution_margin,
        "net_margin_pct": net_annual / gross_annual if gross_annual else 0,
    }


def breakeven_enrollment(price, subs, a=None):
    """Enrollment count where net (incl. fixed + onetime, no churn) = 0."""
    a = a or A
    pm = per_member(price, a=a)
    fixed = a["program_mgmt"] + a["cust_comm_annual"] + a["billing_impl"] + a["launch_cost"]
    return fixed / pm["contribution"] if pm["contribution"] > 0 else None


def breakeven_calls(price, enrolled, a=None):
    """How many covered calls can be funded before gross plan revenue is exhausted."""
    a = a or A
    gross_annual = enrolled * price * 12
    return gross_annual / (cost_per_call(a) + a["cc_handling"])


def churn_offset_pct(price, subs, enroll_pct, churn_base="enrolled", a=None):
    """Incremental annual churn % at which net contribution is fully offset."""
    a = a or A
    pm = per_member(price, a=a)
    enrolled = subs * enroll_pct
    contribution = enrolled * pm["contribution"] - (a["program_mgmt"] + a["cust_comm_annual"])
    affected = enrolled if churn_base == "enrolled" else subs
    denom = affected * a["arpu"] * 12
    return contribution / denom if denom else 0


def five_year(price, subs0, enroll_pct, a=None, churn_base="enrolled"):
    a = a or A
    rows = []
    subs = subs0
    price_y = price
    cum_gross = 0
    cum_net = 0
    for y in range(1, 6):
        t = program_totals(price_y, subs, enroll_pct, a=a,
                           include_onetime=(y == 1), churn_base=churn_base)
        cum_gross += t["gross_annual"]
        cum_net += t["net_annual"]
        rows.append({"year": y, "subs": subs, "price": price_y,
                     "gross": t["gross_annual"], "net": t["net_annual"],
                     "cum_gross": cum_gross, "cum_net": cum_net})
        subs = subs * ((1 + a["monthly_growth"]) ** 12)
        price_y = price_y * (1 + a["price_increase"])
    return rows


def ppv_revenue(charge, subs, a=None):
    a = a or A
    calls = subs * a["trouble_rate"] * a["cust_caused_pct"]
    gross = calls * charge
    net = gross * a["ppv_collection"] - calls * (cost_per_call(a) + a["cc_handling"])
    return {"calls": calls, "gross": gross, "collected": gross * a["ppv_collection"],
            "cost": calls * (cost_per_call(a) + a["cc_handling"]), "net": net}


# ---------------------------------------------------------------------------
# COVERAGE TIERS
# ---------------------------------------------------------------------------
COVERAGE_ROWS = [
    # item, RIVR-owned-free, Basic, Standard, Premium, excluded
    ("RIVR Tech-owned ONT", "Always free (RIVR-owned)", "—", "—", "—"),
    ("RIVR Tech router / GigaSpire", "Always free (RIVR-owned)", "—", "—", "—"),
    ("Standard indoor wiring installed by RIVR Tech", "Repair if RIVR defect", "✔", "✔", "✔"),
    ("Standard outdoor drop facilities", "Always free (RIVR-owned)", "✔", "✔", "✔"),
    ("Connector replacement", "If RIVR-side", "✔", "✔", "✔"),
    ("Basic Wi-Fi troubleshooting", "n/a", "✔", "✔", "✔"),
    ("Customer education", "n/a", "✔", "✔", "✔"),
    ("Router relocation", "n/a", "1st free/yr", "✔", "✔"),
    ("One standard visit / 12 mo", "n/a", "✔ (1)", "✔ (2)", "✔ (4)"),
    ("Additional visits (rolling 12 mo)", "n/a", "Reduced dispatch", "✔ (to limit)", "✔ (to limit)"),
    ("After-hours service", "Emergencies free", "Excluded", "Reduced", "✔"),
    ("Damage caused by pets", "n/a", "Excluded", "1st/yr", "✔"),
    ("Damage caused by lawn equipment", "n/a", "Excluded", "1st/yr", "✔"),
    ("Damage from construction / remodeling", "n/a", "Excluded", "Excluded", "Excluded"),
    ("Damage from customer negligence", "n/a", "Excluded", "Excluded", "Reduced"),
    ("Customer-owned routers", "n/a", "Education only", "Education only", "Setup help"),
    ("Customer devices (PC/TV/phone/camera/IoT)", "n/a", "Excluded", "Excluded", "Basic help"),
    ("RIVR network performance problems", "Always free (RIVR-owned)", "—", "—", "—"),
    ("Acts of God / storms / flood / utility damage", "n/a", "Excluded", "Excluded", "Excluded"),
]
TIER_PRICES = {"Basic": 3.99, "Standard": 4.99, "Premium": 7.99}

# ---------------------------------------------------------------------------
# AFFORDABILITY GROUPS
# ---------------------------------------------------------------------------
AFFORD_GROUPS = [
    ("Senior citizens", "Fixed incomes; sensitive to add-on fees.", "Opt-in only; never auto-enroll."),
    ("Lifeline customers", "Federal low-income program participants.", "Exempt from any mandatory/opt-out; opt-in only."),
    ("Tribal Lifeline customers", "Enhanced Tribal benefit participants.", "Exempt; opt-in only; specific Tribal Lifeline review."),
    ("Low-income customers", "Affordability-constrained households.", "Opt-in only; consider discounted tier."),
    ("Rarely-support customers", "Almost never request a truck roll.", "A mandatory fee is unfair; opt-in only."),
    ("Multi-service customers", "Bundle internet + voice/other.", "Offer as bundle add-on; opt-in."),
    ("Renters", "May not own premises wiring.", "Opt-in; clarify landlord-owned facilities."),
    ("Bulk / managed-property accounts", "Governed by property contracts.", "Exclude from blanket fee; handle via contract."),
]

# ---------------------------------------------------------------------------
# WEIGHTED DECISION MATRIX
# categories with weights (sum 100); higher score (1-5) always = better
# ---------------------------------------------------------------------------
CRITERIA = [
    ("Net financial benefit", 15),
    ("Customer fairness", 12),
    ("Customer acceptance", 12),
    ("Regulatory risk (5=low risk)", 15),
    ("Operational simplicity", 8),
    ("Revenue predictability", 8),
    ("Churn risk (5=low risk)", 12),
    ("Brand impact", 10),
    ("Scalability", 4),
    ("Ease of implementation", 4),
]
OPTIONS = [
    "Mandatory $3.99", "Mandatory $4.99",
    "Opt-out $3.99", "Opt-out $4.99",
    "Opt-in $3.99", "Opt-in $4.99",
    "Pay-per-visit only", "Hybrid (opt-in + PPV)", "Do not implement",
]
# scores per option across the 10 criteria (order matches CRITERIA)
SCORES = {
    "Mandatory $3.99":        [5, 1, 1, 1, 4, 5, 1, 1, 5, 3],
    "Mandatory $4.99":        [5, 1, 1, 1, 4, 5, 1, 1, 5, 3],
    "Opt-out $3.99":          [4, 2, 2, 2, 3, 4, 2, 2, 4, 3],
    "Opt-out $4.99":          [4, 2, 2, 2, 3, 4, 2, 2, 4, 3],
    "Opt-in $3.99":           [3, 5, 5, 5, 3, 3, 5, 5, 4, 4],
    "Opt-in $4.99":           [3, 5, 4, 5, 3, 3, 5, 5, 4, 4],
    "Pay-per-visit only":     [2, 4, 3, 4, 2, 1, 4, 3, 3, 3],
    "Hybrid (opt-in + PPV)":  [4, 5, 4, 4, 2, 3, 5, 5, 4, 3],
    "Do not implement":       [1, 4, 5, 5, 5, 1, 5, 4, 2, 5],
}


def weighted_scores():
    weights = [w for _, w in CRITERIA]
    out = {}
    for opt in OPTIONS:
        s = SCORES[opt]
        total = sum(sc * w for sc, w in zip(s, weights)) / sum(weights)
        out[opt] = total
    return out


# ---------------------------------------------------------------------------
# REGULATORY / LEGAL FLAGS
# ---------------------------------------------------------------------------
LEGAL_FLAGS = [
    ("Advance customer notice", "Timing/method of notice for a new recurring charge.", "Legal / Regulatory"),
    ("Material change to customer terms", "Whether this is a material ToS change requiring notice/consent.", "Legal"),
    ("Affirmative consent", "Whether opt-in affirmative consent is required.", "Legal"),
    ("Negative-option / auto-renewal rules", "FTC/ROSCA + state auto-renewal laws for opt-out billing.", "Legal / Regulatory"),
    ("Truthful advertising", "No 'insurance', 'tax', 'regulatory', or 'network fee' language unless accurate.", "Legal / Marketing"),
    ("Billing transparency", "Clear separate line item and plain-language name.", "Billing / Legal"),
    ("State consumer-protection laws (NC)", "NC UDAP / Chapter 75; unfair-practice exposure.", "Regulatory"),
    ("FCC requirements", "Applicability of FCC rules to a broadband add-on charge.", "Regulatory"),
    ("Broadband-label disclosures", "Whether the fee must appear on the FCC broadband label.", "Regulatory"),
    ("Lifeline rules", "Lifeline subscribers cannot be forced into add-on fees.", "Regulatory"),
    ("Tribal Lifeline requirements", "Enhanced Tribal benefit protections.", "Regulatory"),
    ("Tax treatment", "Sales/telecom tax treatment of a maintenance plan.", "Tax / Accounting"),
    ("Existing customer agreements", "Consistency with current residential ToS.", "Legal"),
    ("Bulk-service contracts", "Managed-property agreements override blanket fees.", "Legal"),
    ("Customer- vs provider-owned facilities", "Coverage must track ownership of equipment/wiring.", "Legal / Ops"),
]

# ---------------------------------------------------------------------------
# DATA NEEDED BEFORE FINAL APPROVAL
# ---------------------------------------------------------------------------
DATA_NEEDED = [
    "Actual 12-month residential trouble-call volume and % customer-caused.",
    "True fully loaded cost per truck roll (labor, vehicle, fuel, materials, repeat rate).",
    "Baseline residential churn and any prior fee-change churn experience.",
    "Count of Lifeline / Tribal Lifeline / low-income residential accounts.",
    "Count of bulk / managed-property and renter accounts.",
    "NISC billing-code and tax-configuration effort/quote.",
    "Real collection and bad-debt experience on customer charges.",
    "Customer willingness-to-pay / survey for a protection plan.",
    "Legal opinion on negative-option/opt-out billing in NC.",
    "Expected enrollment take-rate from a pilot.",
]


def money(x):
    return f"${x:,.0f}"


def money2(x):
    return f"${x:,.2f}"


if __name__ == "__main__":
    cpc = cost_per_call()
    print(f"Cost per covered call (loaded): ${cpc:,.2f}")
    for price, name in [(PRICE_A, "A $3.99"), (PRICE_B, "B $4.99")]:
        pm = per_member(price)
        print(f"\n{name}: per-member contribution ${pm['contribution']:.2f} "
              f"(margin {pm['margin_pct']*100:.0f}%), break-even util {breakeven_util(price)*100:.1f}%")
        t = program_totals(price, 4686, 1.0, incr_churn=0.0)
        print(f"  Mandatory@4686: gross ${t['gross_annual']:,.0f}  net(Y1) ${t['net_annual']:,.0f}")
        off = churn_offset_pct(price, 4686, 1.0, churn_base="all")
        print(f"  Churn-offset (mandatory, base=all): {off*100:.2f}% incremental annual churn")
        be_calls = breakeven_calls(price, 4686)
        print(f"  Break-even covered calls @4686 fully enrolled: {be_calls:,.0f}")
    print("\nWeighted decision scores:")
    for opt, sc in sorted(weighted_scores().items(), key=lambda x: -x[1]):
        print(f"  {opt:26s} {sc:.2f}")
