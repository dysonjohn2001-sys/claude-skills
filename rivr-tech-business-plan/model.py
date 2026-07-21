"""
RIVR Tech (LREMC Technologies, LLC) — Five-Year Business Plan Financial Model
Single source of truth for the .xlsx / .docx / .pptx deliverables.

All computation is deterministic. Scenario = base | conservative | aggressive.
Monthly detail is produced for Year 1 (2027); annual for 2027-2031.

Data-classification tags used throughout the deliverables:
  [ACTUAL] supplied input | [ASSUMPTION] editable | [CALC] derived
  [TARGET] recommended | [PLACEHOLDER] pending management input
"""
from __future__ import annotations
from dataclasses import dataclass, field
import json

YEARS = [2027, 2028, 2029, 2030, 2031]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# ---------------------------------------------------------------------------
# SUPPLIED ACTUALS
# ---------------------------------------------------------------------------
ACTUAL = dict(
    internet_subs_jun2026=4686,
    voice_subs_jun2026=502,
    res_arpu_start=74.0,
    biz_arpu_start=149.0,
    capital_per_year=10_000_000,
    capital_five_year=50_000_000,
    refresh_per_year=400_000,
    refresh_five_year=2_000_000,
    filled_positions=15,
    open_positions=3,
    authorized_positions=18,
)

# ---------------------------------------------------------------------------
# SCENARIO DRIVERS  (editable assumptions)
# ---------------------------------------------------------------------------
@dataclass
class Scenario:
    name: str
    # subscriber opening balances (Jan 2027)  [ASSUMPTION derived from Jun-2026 actual]
    res_open: int
    biz_open: int
    ent_open: int
    voice_open: int
    # annual gross adds by line, per year (index 0..4 = 2027..2031)
    res_gross: list
    biz_gross: list
    ent_gross: list
    voice_gross: list
    # annual churn (fraction of beginning balance)
    res_churn: float
    biz_churn: float
    ent_churn: float
    voice_churn: float
    # ARPU start + annual growth
    res_arpu: float; res_arpu_g: float
    biz_arpu: float; biz_arpu_g: float
    ent_arpu: float; ent_arpu_g: float
    voice_arpu: float; voice_arpu_g: float
    # passings
    res_pass_open: int
    biz_pass_open: int
    res_new_pass: list          # new residential passings / yr
    biz_new_pass: list          # new business passings / yr
    # capital deployment fraction of the $10M available actually deployed each yr
    capital_deploy_frac: list
    # construction cost per passing (for capex-per-passing KPI, informational)
    cost_per_passing: float
    # opex driver knobs
    marketing_per_gross_add: float
    opex_inflation: float
    # attach services
    wifi_attach: float          # % of residential taking managed wifi
    wifi_price: float           # $/mo
    staticip_attach: float      # % of business taking static IP
    staticip_price: float       # $/mo
    # install / nonrecurring
    res_install_fee: float
    biz_install_fee: float
    ent_install_fee: float
    # scenario-level opex efficiency multiplier
    opex_mult: float
    # headcount trajectory (total employees end of each year)  [TARGET]
    headcount: list


def base_scenario() -> Scenario:
    return Scenario(
        name="Base",
        res_open=4450, biz_open=360, ent_open=13, voice_open=512,
        res_gross=[1800, 2050, 2150, 2050, 1900],
        biz_gross=[135, 160, 175, 175, 165],
        ent_gross=[6, 8, 9, 9, 8],
        voice_gross=[120, 130, 130, 120, 110],
        res_churn=0.110, biz_churn=0.080, ent_churn=0.050, voice_churn=0.140,
        res_arpu=74.0, res_arpu_g=0.020,
        biz_arpu=149.0, biz_arpu_g=0.025,
        ent_arpu=850.0, ent_arpu_g=0.020,
        voice_arpu=32.0, voice_arpu_g=0.010,
        res_pass_open=11000, biz_pass_open=1250,
        res_new_pass=[4500, 4200, 3900, 3600, 3300],
        biz_new_pass=[300, 300, 275, 250, 225],
        capital_deploy_frac=[0.96, 0.98, 1.00, 0.98, 0.97],
        cost_per_passing=1200.0,
        marketing_per_gross_add=145.0,
        opex_inflation=0.030,
        wifi_attach=0.35, wifi_price=10.0,
        staticip_attach=0.30, staticip_price=15.0,
        res_install_fee=60.0, biz_install_fee=250.0, ent_install_fee=1500.0,
        opex_mult=1.00,
        headcount=[21, 26, 31, 35, 39],
    )


def conservative_scenario() -> Scenario:
    s = base_scenario()
    s.name = "Conservative"
    s.res_gross = [1350, 1500, 1600, 1550, 1450]
    s.biz_gross = [100, 115, 125, 125, 120]
    s.ent_gross = [4, 5, 6, 6, 6]
    s.voice_gross = [95, 100, 100, 95, 85]
    s.res_churn, s.biz_churn, s.ent_churn, s.voice_churn = 0.140, 0.100, 0.070, 0.170
    s.res_arpu_g, s.biz_arpu_g = 0.010, 0.015
    s.res_new_pass = [3600, 3400, 3200, 3000, 2800]
    s.biz_new_pass = [240, 240, 220, 200, 180]
    s.capital_deploy_frac = [0.85, 0.88, 0.90, 0.90, 0.90]
    s.cost_per_passing = 1400.0
    s.marketing_per_gross_add = 175.0
    s.opex_inflation = 0.040
    s.wifi_attach, s.staticip_attach = 0.28, 0.25
    s.opex_mult = 1.06
    s.headcount = [20, 23, 27, 30, 33]
    return s


def aggressive_scenario() -> Scenario:
    s = base_scenario()
    s.name = "Aggressive"
    s.res_gross = [2300, 2700, 2850, 2750, 2550]
    s.biz_gross = [175, 205, 225, 230, 215]
    s.ent_gross = [8, 11, 12, 13, 12]
    s.voice_gross = [140, 150, 150, 140, 130]
    s.res_churn, s.biz_churn, s.ent_churn, s.voice_churn = 0.090, 0.065, 0.040, 0.120
    s.res_arpu_g, s.biz_arpu_g = 0.025, 0.030
    s.res_new_pass = [5400, 5100, 4700, 4300, 3900]
    s.biz_new_pass = [360, 360, 330, 300, 270]
    s.capital_deploy_frac = [1.00, 1.00, 1.00, 1.00, 1.00]
    s.cost_per_passing = 1100.0
    s.marketing_per_gross_add = 210.0
    s.opex_inflation = 0.030
    s.wifi_attach, s.staticip_attach = 0.42, 0.35
    s.opex_mult = 0.98
    s.headcount = [23, 29, 35, 40, 45]
    return s


SCENARIOS = {
    "base": base_scenario,
    "conservative": conservative_scenario,
    "aggressive": aggressive_scenario,
}

# ---------------------------------------------------------------------------
# ROLL-FORWARD ENGINE
# ---------------------------------------------------------------------------
def roll_line(opening, gross_list, churn_annual):
    """Annual roll-forward: disconnects = churn * beginning balance."""
    rows = []
    beg = opening
    for gross in gross_list:
        disc = round(churn_annual * beg)
        end = beg + gross - disc
        rows.append(dict(beg=beg, gross=gross, disc=disc, net=gross - disc, end=end))
        beg = end
    return rows


def monthly_line_year1(opening, annual_gross, churn_annual):
    """Monthly roll-forward for Year 1. Gross adds spread with a modest ramp;
    disconnects use monthly churn = churn_annual/12 on beginning-of-month."""
    m_churn = churn_annual / 12.0
    # ramp weights sum to 1.0 (slower start, build through spring/summer)
    weights = [0.070, 0.072, 0.078, 0.085, 0.090, 0.092,
               0.092, 0.090, 0.086, 0.083, 0.082, 0.080]
    # normalize (safety)
    tot = sum(weights)
    weights = [w / tot for w in weights]
    rows = []
    beg = opening
    allocated = 0
    for i, w in enumerate(weights):
        if i < 11:
            g = round(annual_gross * w)
        else:
            g = annual_gross - allocated       # plug last month to hit annual exactly
        allocated += g
        disc = round(m_churn * beg)
        end = beg + g - disc
        rows.append(dict(month=MONTHS[i], beg=beg, gross=g, disc=disc,
                         net=g - disc, end=end))
        beg = end
    return rows


def compute(scenario_key="base"):
    s = SCENARIOS[scenario_key]()
    R = dict(scenario=s.name, key=scenario_key, years=YEARS)

    # --- Year 1 monthly (computed FIRST so annual Y1 ties to it exactly) ---
    R["monthly"] = dict(
        res=monthly_line_year1(s.res_open, s.res_gross[0], s.res_churn),
        biz=monthly_line_year1(s.biz_open, s.biz_gross[0], s.biz_churn),
        ent=monthly_line_year1(s.ent_open, s.ent_gross[0], s.ent_churn),
        voice=monthly_line_year1(s.voice_open, s.voice_gross[0], s.voice_churn),
    )

    # --- subscriber roll-forwards (annual); Year 1 derived from monthly ---
    def annual_from_monthly(opening, monthly_rows):
        disc = sum(m["disc"] for m in monthly_rows)
        gross = sum(m["gross"] for m in monthly_rows)
        end = monthly_rows[-1]["end"]
        return dict(beg=opening, gross=gross, disc=disc, net=gross - disc, end=end)

    def roll_from(y1row, gross_list, churn_annual):
        rows = [y1row]
        beg = y1row["end"]
        for gross in gross_list[1:]:
            d = round(churn_annual * beg)
            end = beg + gross - d
            rows.append(dict(beg=beg, gross=gross, disc=d, net=gross - d, end=end))
            beg = end
        return rows

    res = roll_from(annual_from_monthly(s.res_open, R["monthly"]["res"]), s.res_gross, s.res_churn)
    biz = roll_from(annual_from_monthly(s.biz_open, R["monthly"]["biz"]), s.biz_gross, s.biz_churn)
    ent = roll_from(annual_from_monthly(s.ent_open, R["monthly"]["ent"]), s.ent_gross, s.ent_churn)
    voice = roll_from(annual_from_monthly(s.voice_open, R["monthly"]["voice"]), s.voice_gross, s.voice_churn)
    R["subs"] = dict(res=res, biz=biz, ent=ent, voice=voice)

    # --- passings ---
    res_pass = []
    p = s.res_pass_open
    for i in range(5):
        p += s.res_new_pass[i]
        res_pass.append(p)
    biz_pass = []
    p = s.biz_pass_open
    for i in range(5):
        p += s.biz_new_pass[i]
        biz_pass.append(p)
    R["passings"] = dict(res=res_pass, biz=biz_pass,
                         res_new=s.res_new_pass, biz_new=s.biz_new_pass)

    # --- ARPU by year ---
    def arpu_series(start, g):
        return [round(start * (1 + g) ** i, 2) for i in range(5)]
    res_arpu = arpu_series(s.res_arpu, s.res_arpu_g)
    biz_arpu = arpu_series(s.biz_arpu, s.biz_arpu_g)
    ent_arpu = arpu_series(s.ent_arpu, s.ent_arpu_g)
    voice_arpu = arpu_series(s.voice_arpu, s.voice_arpu_g)
    R["arpu"] = dict(res=res_arpu, biz=biz_arpu, ent=ent_arpu, voice=voice_arpu)

    # --- revenue ---
    rev = {k: [] for k in ["res", "biz", "ent", "voice", "wifi", "staticip",
                           "install", "equip", "wholesale", "grant", "other",
                           "recurring", "nonrecurring", "total"]}
    for i in range(5):
        avg_res = (res[i]["beg"] + res[i]["end"]) / 2
        avg_biz = (biz[i]["beg"] + biz[i]["end"]) / 2
        avg_ent = (ent[i]["beg"] + ent[i]["end"]) / 2
        avg_voice = (voice[i]["beg"] + voice[i]["end"]) / 2

        res_rev = avg_res * res_arpu[i] * 12
        biz_rev = avg_biz * biz_arpu[i] * 12
        ent_rev = avg_ent * ent_arpu[i] * 12
        voice_rev = avg_voice * voice_arpu[i] * 12
        wifi_rev = avg_res * s.wifi_attach * s.wifi_price * 12
        staticip_rev = avg_biz * s.staticip_attach * s.staticip_price * 12
        # equipment fee: $6/mo per residential + business sub (ONT/router lease) [ASSUMPTION]
        equip_rev = (avg_res + avg_biz) * 6.0 * 12
        # nonrecurring install/construction
        install_rev = (res[i]["gross"] * s.res_install_fee
                       + biz[i]["gross"] * s.biz_install_fee
                       + ent[i]["gross"] * s.ent_install_fee)
        # wholesale/dark fiber/IRU/transport [PLACEHOLDER, grows]
        wholesale_rev = [180_000, 240_000, 320_000, 410_000, 500_000][i]
        # grant admin revenue if allowable [PLACEHOLDER]
        grant_rev = [50_000, 60_000, 70_000, 70_000, 60_000][i]
        # other telecom services [PLACEHOLDER]
        other_rev = [40_000, 55_000, 70_000, 85_000, 100_000][i]

        recurring = (res_rev + biz_rev + ent_rev + voice_rev + wifi_rev
                     + staticip_rev + equip_rev + wholesale_rev + grant_rev + other_rev)
        nonrecurring = install_rev
        total = recurring + nonrecurring

        rev["res"].append(res_rev); rev["biz"].append(biz_rev)
        rev["ent"].append(ent_rev); rev["voice"].append(voice_rev)
        rev["wifi"].append(wifi_rev); rev["staticip"].append(staticip_rev)
        rev["install"].append(install_rev); rev["equip"].append(equip_rev)
        rev["wholesale"].append(wholesale_rev); rev["grant"].append(grant_rev)
        rev["other"].append(other_rev)
        rev["recurring"].append(recurring); rev["nonrecurring"].append(nonrecurring)
        rev["total"].append(total)
    R["revenue"] = rev

    # --- ending subs totals & KPIs helpers ---
    end_total = [res[i]["end"] + biz[i]["end"] + ent[i]["end"] for i in range(5)]
    beg_total = [res[i]["beg"] + biz[i]["beg"] + ent[i]["beg"] for i in range(5)]
    gross_total = [res[i]["gross"] + biz[i]["gross"] + ent[i]["gross"] for i in range(5)]
    disc_total = [res[i]["disc"] + biz[i]["disc"] + ent[i]["disc"] for i in range(5)]
    R["subs_total"] = dict(beg=beg_total, end=end_total,
                           gross=gross_total, disc=disc_total)

    # --- labor (fully loaded) ---
    labor = compute_labor(s)
    R["labor"] = labor

    # --- operating expenses ---
    opex = compute_opex(s, R, labor)
    R["opex"] = opex

    # --- capital ---
    cap = compute_capital(s)
    R["capital"] = cap

    # --- depreciation (placeholder) ---
    dep = compute_depreciation(cap)
    R["depreciation"] = dep

    # --- financial statements ---
    fin = {}
    fin["revenue"] = rev["total"]
    fin["opex"] = opex["total"]
    fin["ebitda"] = [rev["total"][i] - opex["total"][i] for i in range(5)]
    fin["ebitda_margin"] = [fin["ebitda"][i] / rev["total"][i] for i in range(5)]
    fin["depreciation"] = dep["total"]
    fin["op_income"] = [fin["ebitda"][i] - dep["total"][i] for i in range(5)]
    fin["capex"] = cap["deployed"]
    fin["fcf"] = [fin["ebitda"][i] - cap["deployed"][i] for i in range(5)]
    fin["cum_cash"] = []
    c = 0.0
    for i in range(5):
        c += fin["fcf"][i]
        fin["cum_cash"].append(c)
    fin["cap_avail"] = [ACTUAL["capital_per_year"]] * 5
    fin["cap_used"] = cap["deployed"]
    fin["cap_remaining"] = [fin["cap_avail"][i] - fin["cap_used"][i] for i in range(5)]
    R["financials"] = fin

    # --- KPIs ---
    R["kpi"] = compute_kpi(s, R)
    return R


def compute_labor(s: Scenario):
    """Fully-loaded labor. Base wages are PLACEHOLDER assumptions."""
    # position -> (base_salary, count_start)   [PLACEHOLDER wages]
    roles_start = [
        ("Chief Operations Officer", 165000, 1),
        ("Director of Outside Plant", 130000, 1),
        ("Supervisors", 92000, 2),
        ("Project Coordinators", 68000, 2),
        ("Sales Coordinator", 62000, 1),
        ("Sales Representatives", 55000, 4),   # 3 filled + 1 opening = 4 authorized
        ("Fiber Technicians", 58000, 7),       # 5 filled + 2 openings = 7 authorized
    ]
    # loaded factor components (fractions of base) [ASSUMPTION]
    load = dict(overtime=0.05, incentive=0.06, payroll_tax=0.0765,
                benefits=0.18, workers_comp=0.035, training=0.015,
                uniforms_ppe=0.010)
    load_factor = 1 + sum(load.values())    # ~1.4145
    # per-head one-time-ish annual allocations [PLACEHOLDER]
    per_head_tools = 3500     # laptop/phone/tools/test equip amortized
    per_head_recruit = 1200   # recruiting/onboarding blended

    authorized = sum(c for _, _, c in roles_start)   # 18
    filled = 15

    # fully loaded per authorized position (weighted)
    total_base = sum(b * c for _, b, c in roles_start)
    avg_base = total_base / authorized
    loaded_per_head = avg_base * load_factor + per_head_tools + per_head_recruit

    # Year-by-year total labor cost keyed to headcount trajectory + merit 3%/yr
    merit = 0.03
    headcount = s.headcount
    labor_cost = []
    for i in range(5):
        base_infl = (1 + merit) ** i
        cost = headcount[i] * loaded_per_head * base_infl
        labor_cost.append(cost)
    return dict(roles_start=roles_start, load=load, load_factor=load_factor,
                per_head_tools=per_head_tools, per_head_recruit=per_head_recruit,
                authorized=authorized, filled=filled, avg_base=avg_base,
                loaded_per_head=loaded_per_head, headcount=headcount,
                labor_cost=labor_cost, merit=merit)


def compute_opex(s: Scenario, R, labor):
    rev = R["revenue"]
    subs = R["subs_total"]
    passings = R["passings"]
    voice = R["subs"]["voice"]
    n = 5
    infl = [(1 + s.opex_inflation) ** i for i in range(n)]

    def avg_sub(i):
        return (subs["beg"][i] + subs["end"][i]) / 2

    cat = {}
    # --- Direct cost of service ---
    cat["Internet transit / bandwidth"] = [avg_sub(i) * 2.5 * 12 * infl[i] for i in range(n)]      # $/sub/mo
    cat["Fiber leases & transport"] = [ (180_000 + 12_000*i) * infl[i] for i in range(n)]
    cat["Pole attachment expense"] = [ (passings["res"][i]+passings["biz"][i]) * 0.55 * infl[i] for i in range(n)]  # $/passing/yr aerial portion
    cat["Fiber maintenance"] = [ (95_000 + 15_000*i) * infl[i] for i in range(n)]
    cat["Network monitoring / NOC"] = [ (140_000 + 10_000*i) * infl[i] for i in range(n)]
    cat["Voice platform"] = [ ((voice[i]["beg"]+voice[i]["end"])/2) * 8.0 * 12 * infl[i] for i in range(n)]
    cat["Emergency restoration"] = [ 75_000 * infl[i] for i in range(n)]
    direct_keys = list(cat.keys())

    # --- Sales & marketing ---
    cat["Marketing & advertising"] = [ (R["subs_total"]["gross"][i]) * s.marketing_per_gross_add + 120_000*infl[i] for i in range(n)]
    cat["Sales commissions"] = [ rev["recurring"][i] * 0.015 for i in range(n)]
    sm_keys = ["Marketing & advertising", "Sales commissions"]

    # --- Network operations (non-labor) ---
    cat["Vehicle fleet (fuel/repairs/insurance/lease)"] = [ (9500 * _fleet(labor["headcount"][i])) * infl[i] for i in range(n)]
    cat["Tools, test & safety equipment"] = [ (45_000 + 4_000*i) * infl[i] for i in range(n)]
    cat["Warehouse & inventory"] = [ (60_000 + 5_000*i) * infl[i] for i in range(n)]
    cat["Contractor labor"] = [ (650_000 + 60_000*i) * infl[i] for i in range(n)]
    netops_keys = ["Vehicle fleet (fuel/repairs/insurance/lease)", "Tools, test & safety equipment",
                   "Warehouse & inventory", "Contractor labor"]

    # --- G&A ---
    cat["Salaries, OT, benefits (fully loaded labor)"] = list(labor["labor_cost"])
    cat["Software / OSS / BSS / CRM / GIS / billing"] = [ (260_000 + 20_000*i) * infl[i] for i in range(n)]
    cat["Billing & payment processing fees"] = [ rev["recurring"][i] * 0.020 for i in range(n)]
    cat["Customer support"] = [ (110_000 + 25_000*i) * infl[i] for i in range(n)]
    cat["Property & casualty insurance"] = [ (185_000 + 10_000*i) * infl[i] for i in range(n)]
    cat["Professional / legal / consulting / regulatory"] = [ (210_000 + 12_000*i) * infl[i] for i in range(n)]
    cat["Training & travel"] = [ (65_000 + 6_000*i) * infl[i] for i in range(n)]
    cat["Office & administrative"] = [ (140_000 + 12_000*i) * infl[i] for i in range(n)]
    cat["Utilities"] = [ (70_000 + 6_000*i) * infl[i] for i in range(n)]
    cat["Bad debt"] = [ rev["total"][i] * 0.008 for i in range(n)]
    cat["Taxes & regulatory fees (USF etc.)"] = [ rev["recurring"][i] * 0.015 for i in range(n)]
    ga_keys = ["Salaries, OT, benefits (fully loaded labor)",
               "Software / OSS / BSS / CRM / GIS / billing",
               "Billing & payment processing fees", "Customer support",
               "Property & casualty insurance",
               "Professional / legal / consulting / regulatory",
               "Training & travel", "Office & administrative", "Utilities",
               "Bad debt", "Taxes & regulatory fees (USF etc.)"]

    # apply scenario opex efficiency multiplier to all categories EXCEPT the
    # fully-loaded labor line (labor is already scenario-driven via headcount).
    labor_line = "Salaries, OT, benefits (fully loaded labor)"
    for k in cat:
        if k == labor_line:
            continue
        cat[k] = [v * s.opex_mult for v in cat[k]]

    # contingency = 1.5% of subtotal
    subtotal = [sum(cat[k][i] for k in cat) for i in range(n)]
    cat["Contingency"] = [subtotal[i] * 0.015 for i in range(n)]
    ga_keys.append("Contingency")

    total = [sum(cat[k][i] for k in cat) for i in range(n)]

    # classification buckets
    groups = dict(
        direct=[sum(cat[k][i] for k in direct_keys) for i in range(n)],
        sm=[sum(cat[k][i] for k in sm_keys) for i in range(n)],
        netops=[sum(cat[k][i] for k in netops_keys) for i in range(n)],
        ga=[sum(cat[k][i] for k in ga_keys) for i in range(n)],
    )

    # fixed / variable / semi-variable classification
    fixed_keys = ["Fiber leases & transport", "Fiber maintenance", "Network monitoring / NOC",
                  "Emergency restoration", "Tools, test & safety equipment", "Warehouse & inventory",
                  "Software / OSS / BSS / CRM / GIS / billing", "Property & casualty insurance",
                  "Professional / legal / consulting / regulatory", "Office & administrative",
                  "Utilities", "Salaries, OT, benefits (fully loaded labor)"]
    variable_keys = ["Internet transit / bandwidth", "Voice platform", "Sales commissions",
                     "Billing & payment processing fees", "Bad debt",
                     "Taxes & regulatory fees (USF etc.)", "Pole attachment expense"]
    semivar_keys = ["Marketing & advertising", "Vehicle fleet (fuel/repairs/insurance/lease)",
                    "Contractor labor", "Customer support", "Training & travel", "Contingency"]
    behavior = dict(
        fixed=[sum(cat[k][i] for k in fixed_keys) for i in range(n)],
        variable=[sum(cat[k][i] for k in variable_keys) for i in range(n)],
        semivar=[sum(cat[k][i] for k in semivar_keys) for i in range(n)],
    )

    return dict(cat=cat, total=total, groups=groups, behavior=behavior,
                direct_keys=direct_keys, sm_keys=sm_keys, netops_keys=netops_keys,
                ga_keys=ga_keys, fixed_keys=fixed_keys, variable_keys=variable_keys,
                semivar_keys=semivar_keys)


def _fleet(headcount):
    """Approx fleet vehicles as function of headcount (field-heavy)."""
    return max(8, round(headcount * 0.55))


def compute_capital(s: Scenario, refresh_outside=False):
    """16 capital categories. Base allocations sum to $10.0M incl. $400K refresh.

    refresh_outside=False  -> refresh is PART of the $10M (base model).
    refresh_outside=True   -> refresh is ADDITIONAL to the $10M (adjustable model).
    Refresh is a committed program: $400K/yr and $2M/5yr, NEVER scaled by deploy pace.
    """
    avail = ACTUAL["capital_per_year"]
    refresh = ACTUAL["refresh_per_year"]
    # category -> base annual allocation ($). Includes refresh (#15) inside the $10M.
    alloc = {
        "1. Fiber backbone construction": 800_000,
        "2. Distribution fiber construction": 1_300_000,
        "3. Fiber-to-the-home expansion": 2_350_000,
        "4. Business & enterprise expansion": 700_000,
        "5. Grant matching funds": 1_000_000,
        "6. Core network & transport equipment": 500_000,
        "7. OLT, cabinet & access-network equipment": 650_000,
        "8. CPE & ONTs": 600_000,
        "9. Vehicles & fleet": 250_000,
        "10. Construction & maintenance equipment": 280_000,
        "11. IT & cybersecurity": 300_000,
        "12. OSS/BSS/CRM/billing/GIS/WFM systems": 340_000,
        "13. Buildings, warehouses & facilities": 230_000,
        "14. Emergency restoration & resiliency": 200_000,
        "15. Annual equipment refresh program": 400_000,
        "16. Capital contingency reserve": 100_000,
    }
    assert sum(alloc.values()) == avail, sum(alloc.values())
    refresh_key = "15. Annual equipment refresh program"

    # Non-refresh (construction/equipment) pool that scales with deploy pace.
    nonrefresh_pool = avail - refresh    # $9.6M in base model

    # Per-category annual: refresh is fixed & fully committed each year; the other
    # 15 categories scale by the deployment fraction (uncommitted is carried/reserved).
    cat_annual = {}
    for k, v in alloc.items():
        if k == refresh_key:
            cat_annual[k] = [refresh] * 5            # ALWAYS $400K, never scaled
        else:
            cat_annual[k] = [round(v * s.capital_deploy_frac[i]) for i in range(5)]
    cat_5yr = {k: sum(cat_annual[k]) for k in cat_annual}

    deployed = [sum(cat_annual[k][i] for k in cat_annual) for i in range(5)]

    # available depends on the inside/outside toggle
    if refresh_outside:
        avail_year = avail + refresh          # $10.4M
    else:
        avail_year = avail                    # $10.0M (refresh inside)
    uncommitted = [avail_year - deployed[i] for i in range(5)]
    cum_deployed = []
    c = 0
    for i in range(5):
        c += deployed[i]
        cum_deployed.append(c)

    return dict(alloc=alloc, deployed=deployed, uncommitted=uncommitted,
                cum_deployed=cum_deployed, cat_annual=cat_annual, cat_5yr=cat_5yr,
                avail=[avail_year]*5, refresh_outside=refresh_outside,
                nonrefresh_pool=nonrefresh_pool, refresh=refresh)


def compute_depreciation(cap):
    """PLACEHOLDER composite depreciation. Existing plant flat + new capex 12yr composite,
    half-year convention in year of spend."""
    existing = 2_400_000     # [PLACEHOLDER] existing net plant depreciation
    life = 12.0
    rate = 1 / life
    dep_new = []
    cum_prior = 0
    for i in range(5):
        this_year = cap["deployed"][i]
        # half-year on current-year spend + full-year on prior cumulative
        d = (cum_prior * rate) + (this_year * rate * 0.5)
        dep_new.append(round(d))
        cum_prior += this_year
    total = [existing + dep_new[i] for i in range(5)]
    return dict(existing=[existing]*5, new=dep_new, total=total, life=life)


def compute_kpi(s: Scenario, R):
    n = 5
    subs = R["subs_total"]
    rev = R["revenue"]
    fin = R["financials"]
    opex = R["opex"]
    passings = R["passings"]
    labor = R["labor"]
    cap = R["capital"]

    def avg_sub(i):
        return (subs["beg"][i] + subs["end"][i]) / 2

    total_pass = [passings["res"][i] + passings["biz"][i] for i in range(n)]
    take_rate = [subs["end"][i] / total_pass[i] for i in range(n)]
    arpu_blended = [rev["recurring"][i] / (avg_sub(i) * 12) for i in range(n)]
    rev_per_pass = [rev["total"][i] / total_pass[i] for i in range(n)]
    new_pass = [passings["res_new"][i] + passings["biz_new"][i] for i in range(n)]
    capex_per_pass = [cap["deployed"][i] / new_pass[i] for i in range(n)]
    net_add = [subs["end"][i] - subs["beg"][i] for i in range(n)]
    capex_per_net = [cap["deployed"][i] / net_add[i] if net_add[i] else 0 for i in range(n)]
    cac = [ (opex["cat"]["Marketing & advertising"][i] + opex["cat"]["Sales commissions"][i]) / subs["gross"][i] for i in range(n)]
    rev_per_emp = [rev["total"][i] / labor["headcount"][i] for i in range(n)]
    subs_per_emp = [subs["end"][i] / labor["headcount"][i] for i in range(n)]
    techs = [max(7, round(labor["headcount"][i] * 0.42)) for i in range(n)]
    subs_per_tech = [subs["end"][i] / techs[i] for i in range(n)]
    churn_month = [ (s.res_churn/12) for _ in range(n)]  # representative blended monthly
    ebitda_per_sub = [fin["ebitda"][i] / avg_sub(i) for i in range(n)]
    opex_per_sub = [opex["total"][i] / avg_sub(i) for i in range(n)]
    opex_per_rev = [opex["total"][i] / rev["total"][i] for i in range(n)]

    return dict(
        total_pass=total_pass, take_rate=take_rate, arpu_blended=arpu_blended,
        rev_per_pass=rev_per_pass, capex_per_pass=capex_per_pass,
        capex_per_net=capex_per_net, cac=cac, rev_per_emp=rev_per_emp,
        subs_per_emp=subs_per_emp, techs=techs, subs_per_tech=subs_per_tech,
        net_add=net_add, ebitda_per_sub=ebitda_per_sub, opex_per_sub=opex_per_sub,
        opex_per_rev=opex_per_rev, new_pass=new_pass,
        # static placeholders (targets)
        network_availability=[0.9985]*n,
        install_interval_days=[9, 8, 7, 7, 6],
        ticket_repeat_rate=[0.09, 0.08, 0.07, 0.065, 0.06],
        overtime_pct=[0.10, 0.09, 0.08, 0.08, 0.07],
        avg_install_cost=[625, 610, 595, 585, 575],
        avg_ticket_cost=[78, 76, 74, 72, 70],
    )


if __name__ == "__main__":
    for key in ["base", "conservative", "aggressive"]:
        R = compute(key)
        f = R["financials"]
        print(f"\n===== {R['scenario'].upper()} =====")
        print("Ending subs :", R["subs_total"]["end"])
        print("Revenue     :", [round(x) for x in f["revenue"]])
        print("OpEx        :", [round(x) for x in f["opex"]])
        print("EBITDA      :", [round(x) for x in f["ebitda"]])
        print("EBITDA %    :", [round(x*100,1) for x in f["ebitda_margin"]])
        print("Capex       :", f["capex"])
        print("FCF         :", [round(x) for x in f["fcf"]])
        print("CumCash     :", [round(x) for x in f["cum_cash"]])
        print("Headcount   :", R["labor"]["headcount"])
