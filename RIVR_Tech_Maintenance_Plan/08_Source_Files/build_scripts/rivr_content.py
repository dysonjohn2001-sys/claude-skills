# -*- coding: utf-8 -*-
"""
RIVR Tech Customer-Premises Maintenance Program
Master content + design module.

This module is the single source of truth for the entire deliverable package.
Every Word / Excel / PowerPoint builder imports the data structures here so that
fees, scenarios, codes, assumptions, and financial results stay consistent across
all 16 deliverables.

IMPORTANT (per assignment):
  * All company-specific numbers are ASSUMPTIONS unless a real RIVR Tech value is
    supplied. Assumptions are marked with is_assumption=True and surfaced in an
    "Assumptions Register" so they are easy to find and replace.
  * Nothing here is legal, accounting, insurance, or regulatory advice.
"""

from datetime import date

# ---------------------------------------------------------------------------
# COMPANY IDENTITY
# ---------------------------------------------------------------------------
COMPANY_LEGAL = "LREMC Technologies, LLC d/b/a RIVR Tech"
COMPANY_SHORT = "RIVR Tech"
REGION = "southeastern North Carolina"
DOC_VERSION = "v1.0 (Draft for Executive Review)"
DOC_DATE = "2026-07-20"
EFFECTIVE_DATE_PLACEHOLDER = "[EFFECTIVE DATE — TO BE SET BY EXECUTIVE TEAM]"
PREPARED_BY = "Maintenance Program Working Team (Operations / CX / Finance / Policy)"

# Brand palette (assumed — replace with official RIVR Tech brand colors).
# Water/river-inspired blues for a broadband provider in a river region.
BRAND = {
    "primary":   "0B3D5C",   # deep river blue
    "secondary": "1B87B5",   # bright current blue
    "accent":    "36B39A",   # teal-green
    "dark":      "10222E",   # near-black slate
    "light":     "EAF3F7",   # pale water
    "warn":      "C0562B",   # clay/terracotta (review flag)
    "good":      "2E7D5B",   # green
    "yellow":    "C9A227",   # amber
    "gray":      "6B7A82",
    "white":     "FFFFFF",
}

# ---------------------------------------------------------------------------
# SERVICES COVERED
# ---------------------------------------------------------------------------
SERVICES_COVERED = [
    "Residential internet (fiber / broadband)",
    "Business internet (fiber / broadband)",
    "Managed Wi-Fi",
    "Voice service",
    "RIVR Tech-provided gateways, ONTs, and related network equipment",
]

# ---------------------------------------------------------------------------
# RECOMMENDED FEE SCHEDULE (the "Balanced" recommendation)
# Each fee is tested in the financial model across three postures.
# ---------------------------------------------------------------------------
# Fee item: (label, conservative, balanced_recommended, full_cost_recovery, note)
FEE_ITEMS = [
    ("Confirmed RIVR Tech network or equipment problem", 0, 0, 0,
     "Always free. Core promise of the program."),
    ("Inconclusive findings (no clear cause)", 0, 0, 0,
     "No charge unless management approves on clear evidence."),
    ("Residential customer-premises trouble visit", 60, 75, 89,
     "Primary residential fee. Requires documented findings."),
    ("Business customer-premises trouble visit", 99, 125, 149,
     "Primary business fee. Requires documented findings."),
    ("Additional labor after first 30 minutes (per 30 min)", 30, 35, 40,
     "Applies only to billable customer-premises work."),
    ("Missed appointment or denied access", 25, 35, 45,
     "Flat administrative fee; one courtesy waiver typical."),
    ("Equipment relocation (starting at, plus materials)", 85, 95, 115,
     "Customer-requested move of working equipment."),
    ("Inside-wiring repair (starting at, plus materials)", 65, 75, 95,
     "Customer-side wiring beyond the demarcation point."),
    ("After-hours customer-caused visit surcharge (added)", 60, 75, 90,
     "Added to the standard fee for after-hours dispatch."),
]

# Protection plan price points tested
PROTECTION_PRICES = [7.99, 9.99, 12.99]
PROTECTION_RECOMMENDED = 9.99

RECOMMENDED_POSTURE = "Balanced"

# One-time educational courtesy waiver for a first customer-caused incident
FIRST_INCIDENT_COURTESY_WAIVER = True

# ---------------------------------------------------------------------------
# FINANCIAL MODEL — INPUTS (editable). is_assumption flags model-fed guesses.
# key: (label, value, unit, is_assumption, note)
# ---------------------------------------------------------------------------
FIN_INPUTS = [
    ("total_customers",        "Total customers",                    18500,  "count",  True,  "Assumption — replace with billing-system count."),
    ("residential_customers",  "Residential customers",              16900,  "count",  True,  "Assumption."),
    ("business_customers",     "Business customers",                  1600,  "count",  True,  "Assumption."),
    ("monthly_tickets",        "Monthly trouble tickets",             1850,  "count",  True,  "Assumption — replace with ticketing export."),
    ("remote_resolution_rate", "Remote-resolution rate",              0.62,  "pct",    True,  "Assumption — baseline before program."),
    ("dispatch_rate",          "Dispatch rate (of tickets)",          0.38,  "pct",    True,  "Derived complement of remote resolution."),
    ("cust_caused_pct",        "Customer-caused % of dispatches",     0.30,  "pct",    True,  "Assumption — validate from historical dispositions."),
    ("billable_pct",           "Billable % of customer-caused",       0.62,  "pct",    True,  "After inconclusive/shared/courtesy removals."),
    ("avg_visit_hours",        "Average billable visit duration (hr)", 0.75, "hours",  True,  "45 minutes on site."),
    ("tech_hourly_cost",       "Loaded technician hourly cost",       68.00, "usd",    True,  "Wages + benefits + burden."),
    ("travel_hours",           "Avg travel time per dispatch (hr)",   0.50,  "hours",  True,  "Windshield time per truck roll."),
    ("vehicle_cost",           "Vehicle cost per visit",              22.00, "usd",    True,  "Depreciation + maintenance allocation."),
    ("fuel_cost",              "Fuel per visit",                       9.00, "usd",    True,  "Assumption."),
    ("materials_cost",         "Materials per visit",                  6.00, "usd",    True,  "Average consumables."),
    ("admin_cost",             "Billing & admin cost per fee",         8.00, "usd",    True,  "Invoice, posting, support handling."),
    ("res_fee",                "Residential fee",                     75.00, "usd",    False, "Recommended (Balanced)."),
    ("bus_fee",                "Business fee",                       125.00, "usd",    False, "Recommended (Balanced)."),
    ("collection_rate",        "Collection rate",                     0.85,  "pct",    True,  "Share of net-of-waiver fees collected."),
    ("waiver_rate",            "Waiver rate",                         0.15,  "pct",    True,  "Courtesy + hardship + dispute waivers."),
    ("bad_debt_rate",          "Bad-debt rate",                      0.06,  "pct",    True,  "Uncollectible assessed fees."),
    ("ancillary_fee_revenue",  "Ancillary fees gross (missed/reloc/wire/AH)", 19000.00, "usd", True, "Annual gross from secondary fees."),
    ("protection_price",       "Protection-plan price (monthly)",     9.99,  "usd",    False, "Recommended price point."),
    ("protection_enrollment",  "Protection-plan enrollment (of res)", 0.10,  "pct",    True,  "Assumption — conservative mature-state target (upside 12-18%)."),
    ("protection_usage_rate",  "Protection-plan annual usage rate",   0.30,  "pct",    True,  "Share of members using a covered visit/yr."),
    ("protection_visit_cost",  "Cost per covered protection visit",   95.00, "usd",    True,  "Loaded cost of a covered service event."),
    ("protection_admin_pct",   "Protection-plan admin (% of rev)",    0.06,  "pct",    True,  "Billing, servicing, marketing."),
    ("churn_impact_pct",       "Policy-related churn impact",         0.003, "pct",    True,  "Incremental annual churn from policy."),
    ("arpu_annual",            "Average annual revenue per customer", 780.00,"usd",    True,  "Blended ARPU (for churn cost)."),
    ("remote_improve_pts",     "Remote-resolution improvement (pts)", 0.05,  "pct",    True,  "Expected lift from triage discipline."),
    ("implementation_cost",    "Implementation cost (one-time)",      42000.00,"usd",  True,  "Project, PM, comms, legal review."),
    ("training_cost",          "Training cost (one-time)",            23000.00,"usd",  True,  "Development + delivery + labor."),
    ("billing_config_cost",    "Billing-system configuration (one-time)",30000.00,"usd",True,"Codes, disclosures, portal."),
]
FIN = {row[0]: row[1:] for row in FIN_INPUTS}  # key -> (label, value, unit, is_assumption, note)


def _v(key):
    return FIN[key][1]


def compute_model(overrides=None):
    """Mirror of the Excel model math. Returns a dict of computed results.
    The Excel workbook implements the identical formulas so the narrative and
    the workbook always agree under the same inputs."""
    g = {k: FIN[k][1] for k in FIN}
    if overrides:
        g.update(overrides)

    r = {}
    # Volumes
    r["annual_tickets"] = g["monthly_tickets"] * 12
    r["annual_dispatches"] = r["annual_tickets"] * g["dispatch_rate"]
    r["remote_resolved"] = r["annual_tickets"] * g["remote_resolution_rate"]
    r["cust_caused_dispatches"] = r["annual_dispatches"] * g["cust_caused_pct"]
    r["billable_visits"] = r["cust_caused_dispatches"] * g["billable_pct"]

    # Res/business split of billable visits by customer mix
    res_share = g["residential_customers"] / g["total_customers"]
    bus_share = g["business_customers"] / g["total_customers"]
    r["res_billable"] = r["billable_visits"] * res_share
    r["bus_billable"] = r["billable_visits"] * bus_share

    # Cost per dispatch
    labor = (g["avg_visit_hours"] + g["travel_hours"]) * g["tech_hourly_cost"]
    r["cost_per_dispatch"] = labor + g["vehicle_cost"] + g["fuel_cost"] + g["materials_cost"] + g["admin_cost"]

    # Dispatch expense
    r["annual_dispatch_expense"] = r["annual_dispatches"] * r["cost_per_dispatch"]
    r["cust_caused_dispatch_cost"] = r["cust_caused_dispatches"] * r["cost_per_dispatch"]

    # Fee revenue
    r["gross_fee_revenue"] = r["res_billable"] * g["res_fee"] + r["bus_billable"] * g["bus_fee"]
    r["gross_fee_revenue"] += g["ancillary_fee_revenue"]
    after_waiver = r["gross_fee_revenue"] * (1 - g["waiver_rate"])
    after_baddebt = after_waiver * (1 - g["bad_debt_rate"])
    r["net_fee_revenue"] = after_baddebt * g["collection_rate"]

    # Protection plan
    r["protection_members"] = g["residential_customers"] * g["protection_enrollment"]
    r["protection_revenue"] = r["protection_members"] * g["protection_price"] * 12
    covered_events = r["protection_members"] * g["protection_usage_rate"]
    r["protection_service_cost"] = covered_events * g["protection_visit_cost"]
    r["protection_admin"] = r["protection_revenue"] * g["protection_admin_pct"]
    r["protection_margin"] = r["protection_revenue"] - r["protection_service_cost"] - r["protection_admin"]

    # Deflection / avoided truck rolls
    r["avoided_dispatches"] = r["annual_tickets"] * g["remote_improve_pts"]
    r["deflection_savings"] = r["avoided_dispatches"] * r["cost_per_dispatch"]

    # Churn cost
    r["churn_cost"] = g["total_customers"] * g["churn_impact_pct"] * g["arpu_annual"]

    # Recovery
    r["total_cost_recovery"] = r["net_fee_revenue"] + r["protection_margin"] + r["deflection_savings"]
    r["cost_recovery_pct"] = (r["net_fee_revenue"] + r["protection_margin"]) / r["cust_caused_dispatch_cost"] if r["cust_caused_dispatch_cost"] else 0

    # One-time + payback
    r["one_time_cost"] = g["implementation_cost"] + g["training_cost"] + g["billing_config_cost"]
    r["year1_net"] = r["total_cost_recovery"] - r["churn_cost"] - r["one_time_cost"]
    r["annual_recurring_net"] = r["total_cost_recovery"] - r["churn_cost"]
    r["payback_months"] = (r["one_time_cost"] / (r["annual_recurring_net"] / 12)) if r["annual_recurring_net"] > 0 else None

    # Three-year (protection ramps 60%/85%/100% of mature enrollment; deflection compounds mildly)
    y1 = r["annual_recurring_net"] * 0.72 - r["one_time_cost"]  # partial-year ramp in Y1 net-of-onetime already; keep simple
    # Simpler, transparent 3-yr: Y1 as computed year1_net, Y2/Y3 recurring with modest growth
    r["y1_total"] = r["year1_net"]
    r["y2_total"] = r["annual_recurring_net"] * 1.05
    r["y3_total"] = r["annual_recurring_net"] * 1.10
    r["three_year_net"] = r["y1_total"] + r["y2_total"] + r["y3_total"]

    # Protection break-even (members to cover per-member service+admin at price)
    per_member_annual_rev = g["protection_price"] * 12
    per_member_service = g["protection_usage_rate"] * g["protection_visit_cost"]
    per_member_admin = per_member_annual_rev * g["protection_admin_pct"]
    r["protection_be_price_monthly"] = (per_member_service + per_member_admin) / 12 / (1 - 0) if True else 0
    # break-even price = monthly price at which margin per member = 0
    r["protection_be_price_monthly"] = (per_member_service) / (12 * (1 - g["protection_admin_pct"]))
    r["protection_margin_per_member"] = per_member_annual_rev - per_member_service - per_member_admin

    return r


def scenario_results():
    """Low / Expected / High postures used across narrative + dashboard."""
    low = compute_model({
        "cust_caused_pct": 0.22, "billable_pct": 0.50, "protection_enrollment": 0.07,
        "remote_improve_pts": 0.03, "collection_rate": 0.78, "waiver_rate": 0.22,
    })
    expected = compute_model()
    high = compute_model({
        "cust_caused_pct": 0.36, "billable_pct": 0.70, "protection_enrollment": 0.18,
        "remote_improve_pts": 0.09, "collection_rate": 0.90, "waiver_rate": 0.10,
    })
    return {"Low": low, "Expected": expected, "High": high}


# ---------------------------------------------------------------------------
# RESPONSIBILITY MATRIX — 42 scenarios
# Fields: scenario, segment, classification, billable, fee_category, charge,
#         tech_notes, test_results, photos, cust_ack, sup_approval, waiver, cust_explanation
# classification: NETWORK / PREMISES / SHARED / INCONCLUSIVE
# ---------------------------------------------------------------------------
CLS_NET = "RIVR Tech responsibility"
CLS_PREM = "Customer-premises responsibility"
CLS_SHARED = "Shared responsibility"
CLS_INC = "Inconclusive"

# charge uses tokens resolved against the recommended (Balanced) schedule
RES_FEE = 75
BUS_FEE = 125
MISS_FEE = 35
RELOC_FEE = 95
WIRE_FEE = 75

MATRIX = [
    # scenario, segment, classification, billable, fee_category, charge, notes, tests, photos, ack, sup, waiver, cust_explanation
    ("Network outage (area-wide)", "Both", CLS_NET, "No", "None", "$0",
     "Confirm outage ticket / mass event ID", "OLT/region alarms", "No", "No", "No", "N/A",
     "This was a RIVR Tech network outage. There is no charge."),
    ("Failed RIVR Tech ONT", "Both", CLS_NET, "No", "None", "$0",
     "Serial, alarm, replacement performed", "Optical levels pre/post, link status", "Yes (unit)", "No", "No", "N/A",
     "Your RIVR Tech equipment failed and we replaced it at no charge."),
    ("Failed RIVR Tech gateway/router", "Both", CLS_NET, "No", "None", "$0",
     "Serial, firmware, swap performed", "LAN/WAN status pre/post", "Yes (unit)", "No", "No", "N/A",
     "The RIVR Tech gateway failed and was replaced free of charge."),
    ("RIVR Tech fiber failure (feeder/distribution)", "Both", CLS_NET, "No", "None", "$0",
     "Fiber fault location, splice/repair", "OTDR / optical levels", "Yes (fault)", "No", "No", "N/A",
     "A RIVR Tech fiber issue was repaired at no charge."),
    ("Normal drop failure (no external cause)", "Both", CLS_NET, "No", "None", "$0",
     "Drop replaced, no damage evident", "Optical/continuity pre/post", "Yes (drop)", "No", "No", "N/A",
     "Your service drop failed normally and was repaired free."),
    ("Customer-cut drop (mowing/digging)", "Both", CLS_PREM, "May apply", "Physical damage", "$75 / $125 + materials",
     "Cause of cut, location, repair", "Continuity pre/post", "Yes (damage)", "Yes", "Yes", "First-time courtesy",
     "The drop was damaged at the premises. A repair charge may apply."),
    ("Contractor-cut drop (3rd-party dig)", "Both", CLS_SHARED, "Review", "Physical damage", "Supervisor review",
     "Who caused it, locate status", "Continuity pre/post", "Yes (damage)", "Yes", "Yes", "Shared/locate review",
     "Damage from a third party. We will review responsibility with you."),
    ("Pet damage to wiring/equipment", "Residential", CLS_PREM, "May apply", "Physical damage", "$75 + materials",
     "Evidence of chew/damage", "Continuity/optical", "Yes", "Yes", "No", "First-time courtesy",
     "Pet damage occurred at the premises; a repair charge may apply."),
    ("Pest/rodent damage", "Both", CLS_PREM, "May apply", "Physical damage", "$75 + materials",
     "Evidence of pest damage", "Continuity/optical", "Yes", "Yes", "No", "First-time courtesy",
     "Pest damage occurred at the premises; a repair charge may apply."),
    ("Water damage to inside equipment", "Both", CLS_PREM, "May apply", "Physical damage", "$75 + materials",
     "Source of water, affected gear", "Function test", "Yes", "Yes", "Yes", "Hardship review",
     "Water damage at the premises; a repair charge may apply."),
    ("Fire/smoke damage to equipment", "Both", CLS_SHARED, "Review", "Physical damage", "Supervisor review",
     "Extent, safety, insurance note", "Function test", "Yes", "Yes", "Yes", "Hardship/insurance",
     "We will handle this carefully and review any charge with you."),
    ("Customer unplugged equipment", "Both", CLS_PREM, "May apply", "Wi-Fi/education", "$75 (often courtesy)",
     "What was unplugged, restored", "Link restored", "No", "Yes", "No", "First-time courtesy",
     "Equipment was unplugged at the premises; often waived as courtesy."),
    ("Failed customer power outlet", "Both", CLS_PREM, "May apply", "Customer power", "$75",
     "Outlet dead, electrician referral", "Voltage/no power confirmed", "Yes (outlet)", "Yes", "No", "First-time courtesy",
     "A premises power problem, not the RIVR Tech network. A charge may apply."),
    ("Power strip / surge protector off", "Both", CLS_PREM, "May apply", "Customer power", "$75 (often courtesy)",
     "Strip switched off/tripped", "Power restored", "Optional", "Yes", "No", "First-time courtesy",
     "A power strip was off; often waived the first time."),
    ("Customer-owned router failure", "Both", CLS_PREM, "May apply", "Customer equipment", "$75 / $125",
     "Make/model, failure mode", "Bypass test proves RIVR OK", "Yes (device)", "Yes", "No", "First-time courtesy",
     "Your own router failed. The RIVR Tech service tested good."),
    ("Customer-owned mesh system problem", "Both", CLS_PREM, "May apply", "Third-party network", "$75 / $125",
     "Mesh brand, config issue", "Wired test proves RIVR OK", "Yes", "Yes", "No", "First-time courtesy",
     "A third-party mesh issue; the RIVR Tech connection tested good."),
    ("Customer-owned Ethernet cable fault", "Both", CLS_PREM, "May apply", "Customer equipment", "$75",
     "Cable identified/replaced by cust", "Cable fail, swap proves it", "Yes (cable)", "Yes", "No", "First-time courtesy",
     "A customer-owned cable was faulty; the network tested good."),
    ("Inside-wiring damage (customer side)", "Both", CLS_PREM, "May apply", "Inside wiring", "$75 + materials",
     "Wiring segment, repair scope", "Continuity pre/post", "Yes", "Yes", "No", "Shared if pre-existing",
     "Inside wiring beyond our equipment needed repair; a charge may apply."),
    ("Customer relocated the gateway", "Both", CLS_PREM, "May apply", "Relocation", "$95 + materials",
     "Old/new location, cabling", "Link verified at new spot", "Yes", "Yes", "No", "N/A",
     "You asked to move the gateway; a relocation charge may apply."),
    ("Customer removed/relocated the ONT", "Both", CLS_PREM, "May apply", "Relocation", "$95 + materials",
     "Why moved, re-terminate", "Optical pre/post", "Yes", "Yes", "Yes", "Shared if unsafe original",
     "The ONT was moved at the premises; a relocation charge may apply."),
    ("Equipment relocation request (working gear)", "Both", CLS_PREM, "May apply", "Relocation", "$95 + materials",
     "Requested move, scope", "Link verified post-move", "Yes", "Yes", "No", "N/A",
     "A requested move of working equipment; a relocation charge applies."),
    ("Slow performance from old customer device", "Both", CLS_PREM, "May apply", "Individual device", "$75 (often education)",
     "Device specs vs plan speed", "Wired speed at gateway = plan", "Optional", "Yes", "No", "First-time courtesy",
     "An older device limited speed; the RIVR Tech service delivered full speed."),
    ("Unsupported customer device", "Both", CLS_PREM, "May apply", "Individual device", "$75 (often education)",
     "Device/OS unsupported", "RIVR service verified good", "Optional", "Yes", "No", "First-time courtesy",
     "The device isn't supported; the RIVR Tech connection tested good."),
    ("Device on wrong Wi-Fi band (2.4 vs 5 GHz)", "Both", CLS_PREM, "May apply", "Wi-Fi/education", "$75 (usually education)",
     "Band steering, guidance given", "Speed improves on correct band", "No", "Yes", "No", "First-time courtesy",
     "A device was on the wrong Wi-Fi band; we showed you how to fix it."),
    ("Poor coverage outside intended area", "Both", CLS_PREM, "May apply", "Wi-Fi/education", "$75 (education/upsell)",
     "Coverage map, extender option", "Signal at edge vs core", "Optional", "Yes", "No", "First-time courtesy",
     "Wi-Fi weakens far from the gateway; options include mesh/extenders."),
    ("Building-material Wi-Fi interference", "Both", CLS_PREM, "May apply", "Wi-Fi/education", "$75 (education)",
     "Walls/materials noted", "Signal survey", "Optional", "Yes", "No", "First-time courtesy",
     "Home construction affects Wi-Fi; we explained placement options."),
    ("Malware / device software issue", "Both", CLS_PREM, "May apply", "Individual device", "$75 (referral)",
     "Symptoms, IT referral", "RIVR service verified good", "Optional", "Yes", "No", "First-time courtesy",
     "A device software issue; the RIVR Tech connection tested good."),
    ("Television setup / streaming app help", "Residential", CLS_PREM, "May apply", "Individual device", "$75 (often courtesy)",
     "TV/app configured", "Stream works on good link", "No", "Yes", "No", "First-time courtesy",
     "TV/app setup at the premises; often a courtesy the first time."),
    ("Camera setup / configuration", "Both", CLS_PREM, "May apply", "Third-party network", "$75 / $125",
     "Camera brand, config", "Connectivity verified", "Optional", "Yes", "No", "First-time courtesy",
     "Third-party camera setup; the RIVR Tech connection tested good."),
    ("Gaming-system setup / NAT/port help", "Residential", CLS_PREM, "May apply", "Individual device", "$75 (often education)",
     "Console, NAT guidance", "Wired test good", "No", "Yes", "No", "First-time courtesy",
     "Gaming-console setup; the RIVR Tech connection tested good."),
    ("Smart-home device setup", "Both", CLS_PREM, "May apply", "Third-party network", "$75",
     "Devices, hub config", "Connectivity verified", "Optional", "Yes", "No", "First-time courtesy",
     "Smart-home setup at the premises; the connection tested good."),
    ("Third-party firewall config", "Business", CLS_PREM, "May apply", "Third-party network", "$125 (referral)",
     "Firewall brand, refer to IT", "RIVR handoff verified", "Optional", "Yes", "Yes", "N/A",
     "Third-party firewall config is beyond RIVR Tech; we can refer IT."),
    ("Business network configuration (VLAN/static)", "Business", CLS_PREM, "May apply", "Third-party network", "$125 + labor",
     "Scope, IT coordination", "RIVR handoff verified", "Optional", "Yes", "Yes", "N/A",
     "Custom business network config; a charge may apply, or refer IT."),
    ("No adult present (residential appt)", "Residential", CLS_PREM, "May apply", "No access", "$35",
     "Arrival time, policy", "N/A", "Yes (door)", "Yes", "No", "First-time courtesy",
     "No adult was present; a missed-appointment fee may apply."),
    ("Customer not home for appointment", "Both", CLS_PREM, "May apply", "Customer not home", "$35",
     "Arrival, contact attempts", "N/A", "Yes (door)", "Yes", "No", "First-time courtesy",
     "No one was home; a missed-appointment fee may apply."),
    ("Denied access to equipment/premises", "Both", CLS_PREM, "May apply", "No access", "$35",
     "What was denied, safety", "N/A", "Yes (door)", "Yes", "Yes", "First-time courtesy",
     "Access was denied; a fee may apply and we could not complete work."),
    ("No trouble found (service normal)", "Both", CLS_INC, "No (unless mgmt)", "No trouble found", "$0",
     "All tests normal, education", "Full test suite passed", "Optional", "Yes", "Yes", "Auto-waiver",
     "Everything tested normal. There is no charge for this visit."),
    ("Intermittent condition not reproduced", "Both", CLS_INC, "No (unless mgmt)", "Inconclusive", "$0",
     "Symptom not reproduced, monitor", "Tests at visit normal", "Optional", "Yes", "Yes", "Auto-waiver",
     "We could not reproduce the issue; no charge. We will monitor."),
    ("Weather-related damage (storm/lightning)", "Both", CLS_SHARED, "Review", "Physical damage", "Supervisor review",
     "Storm evidence, scope", "Function test", "Yes", "Yes", "Yes", "Hardship/insurance",
     "Storm-related damage; we will review any charge with you."),
    ("Repeat education visit (same topic)", "Both", CLS_PREM, "May apply", "Repeat premises", "$75",
     "Prior education dates", "Service verified good", "Optional", "Yes", "Yes", "Manager review",
     "A repeat visit on the same topic; a charge may apply."),
    ("Repeat visit after a RIVR Tech repair", "Both", CLS_NET, "No", "Repeat after RIVR fix", "$0",
     "Link to prior RIVR ticket", "Re-test of prior repair", "Yes", "No", "No", "Auto-waiver",
     "This follows a recent RIVR Tech repair; there is no charge."),
    ("Customer-caused after-hours emergency", "Both", CLS_PREM, "May apply", "After hours", "Fee + $75",
     "After-hours reason, scope", "Cause documented", "Yes", "Yes", "Yes", "Hardship review",
     "An after-hours premises issue; the standard fee plus a surcharge may apply."),
]

MATRIX_COLUMNS = [
    "Scenario", "Residential/Business", "Responsibility Classification", "Billable Status",
    "Fee Category", "Recommended Charge", "Required Technician Notes", "Required Test Results",
    "Required Photographs", "Customer Acknowledgment", "Supervisor Approval",
    "Waiver Eligibility", "Customer-Facing Explanation",
]

# ---------------------------------------------------------------------------
# TICKET & BILLING CODES
# code, name, description, billable, required_docs, approval, billing_code, cust_desc
# ---------------------------------------------------------------------------
CODES = [
    ("NET-OUT", "Network failure", "Area or facility network outage.", "No",
     "Outage/event ID, region alarms", "None", "NB-000", "RIVR Tech network issue — no charge."),
    ("EQP-FAIL", "Company equipment failure", "RIVR Tech ONT/gateway failed.", "No",
     "Serial, alarm, swap record", "None", "NB-000", "RIVR Tech equipment replaced — no charge."),
    ("FIB-DROP", "Fiber/drop failure", "RIVR Tech fiber or drop failed (no external cause).", "No",
     "Fault/location, optical levels", "None", "NB-000", "RIVR Tech line repaired — no charge."),
    ("PWR-CUST", "Customer power", "Premises power/outlet/strip problem.", "May apply",
     "No-power confirmation, photo", "Technician", "BL-PWR", "Premises power issue — a charge may apply."),
    ("EQP-CUST", "Customer equipment", "Customer-owned device failed/misconfigured.", "May apply",
     "Make/model, bypass test proving RIVR good", "Technician", "BL-CEQ", "Your equipment — RIVR service tested good."),
    ("WIR-INSD", "Inside wiring", "Customer-side inside wiring repair.", "May apply",
     "Segment, continuity pre/post, photo", "Technician", "BL-WIR", "Inside-wiring repair — a charge may apply."),
    ("DMG-PHYS", "Physical damage", "Cut/pet/pest/water/fire damage at premises.", "May apply",
     "Cause, photo, repair scope", "Supervisor", "BL-DMG", "Premises damage repaired — a charge may apply."),
    ("WIFI-EDU", "Wi-Fi education", "Coverage/band/placement education.", "May apply",
     "Guidance given, wired test = plan", "Technician", "BL-EDU", "Wi-Fi guidance — often a courtesy."),
    ("DEV-INDV", "Individual-device problem", "Single device limited/unsupported.", "May apply",
     "Device specs, service verified good", "Technician", "BL-DEV", "One device affected — RIVR service tested good."),
    ("NET-3RDP", "Third-party network", "Mesh/firewall/camera/smart-home config.", "May apply",
     "Brand, config, RIVR handoff verified", "Technician", "BL-3PN", "Third-party equipment — RIVR connection tested good."),
    ("ACC-NONE", "No access", "Denied access to premises/equipment.", "May apply",
     "What denied, arrival time, photo", "Technician", "BL-ACC", "Access denied — a fee may apply."),
    ("ACC-NOHM", "Customer not home", "No one present for appointment.", "May apply",
     "Arrival, contact attempts, photo", "Technician", "BL-ACC", "Missed appointment — a fee may apply."),
    ("NTF-000", "No trouble found", "All tests normal; service healthy.", "No",
     "Full test suite results", "Supervisor (to bill)", "NB-000", "Everything tested normal — no charge."),
    ("INC-000", "Inconclusive", "Cause not determined / not reproduced.", "No",
     "Tests performed, monitoring plan", "Manager (to bill)", "NB-000", "No clear cause found — no charge."),
    ("RPT-CUST", "Repeat customer-premises issue", "Repeat premises visit, same cause.", "May apply",
     "Prior ticket links, findings", "Manager", "BL-RPT", "A repeat premises issue — a charge may apply."),
    ("REL-MOVE", "Relocation", "Move of working RIVR Tech equipment.", "May apply",
     "Old/new location, link verified", "Technician", "BL-REL", "Requested equipment move — a charge applies."),
    ("WVR-MGR", "Manager waiver", "Discretionary fee waiver by manager.", "No",
     "Reason code, prior fee ref", "Manager", "WV-MGR", "Fee waived by RIVR Tech."),
    ("WVR-HRD", "Hardship waiver", "Hardship / accommodation waiver.", "No",
     "Hardship basis (documented)", "Manager", "WV-HRD", "Fee waived — hardship accommodation."),
]
CODE_COLUMNS = ["Code", "Code Name", "Description", "Billable Status",
                "Required Documentation", "Approval Level", "Billing Code", "Customer-Facing Description"]

# ---------------------------------------------------------------------------
# WAIVER CATEGORIES
# ---------------------------------------------------------------------------
WAIVER_CATEGORIES = [
    ("First-time courtesy", "One-time educational courtesy for a customer's first customer-caused incident.", "Frontline / Supervisor"),
    ("Documentation error", "Required findings, tests, or photos are missing or inconsistent.", "Supervisor"),
    ("Shared responsibility", "Cause is partly RIVR Tech, partly premises.", "Supervisor"),
    ("Inconclusive findings", "No clear cause; issue not reproduced.", "Supervisor (auto)"),
    ("Hardship", "Documented financial hardship.", "Manager"),
    ("Reasonable accommodation", "Disability / medical / access accommodation.", "Manager"),
    ("Incorrect disclosure", "Advance charge disclosure was not properly given.", "Supervisor"),
    ("Repeat failure after RIVR repair", "Same issue recurs shortly after a RIVR Tech repair.", "Supervisor (auto)"),
    ("Customer-retention exception", "Discretionary retention decision.", "Manager"),
]

# ---------------------------------------------------------------------------
# LEGAL / REVIEW FLAGS
# ---------------------------------------------------------------------------
LEGAL_FLAGS = [
    ("North Carolina consumer-protection requirements", "Confirm fee disclosures and billing practices comply with NC UDAP / Chapter 75 and NCUC expectations.", "Legal / Regulatory"),
    ("Customer agreements (residential)", "Add maintenance/fee terms to the residential terms of service.", "Legal"),
    ("Business service agreements", "Align business SLAs and fee terms with MSAs.", "Legal"),
    ("Service-level agreements", "Ensure billable-visit rules do not conflict with SLA credits.", "Legal / Ops"),
    ("Voice-service obligations", "Confirm treatment of voice/E911 lines and any regulated maintenance duties.", "Regulatory"),
    ("Lifeline / low-income customers", "Define hardship handling for Lifeline/low-income subscribers.", "Regulatory / CX"),
    ("Reasonable accommodations", "ADA / accessibility accommodations for scheduling and access.", "Legal / HR"),
    ("Billing practices", "Invoice clarity, dispute rights, timing, and error-correction.", "Finance / Legal"),
    ("Tax treatment", "Sales/telecom tax treatment of trouble-visit fees and the protection plan.", "Tax / Accounting"),
    ("Protection-plan structure", "Confirm the plan is a service/maintenance offering, NOT insurance.", "Legal / Insurance"),
    ("Insurance characterization", "Ensure marketing/terms avoid implying insurance or warranty.", "Insurance / Legal"),
    ("Record retention", "Retention schedule for tickets, photos, acknowledgments, recordings.", "Legal / Compliance"),
    ("Call recording", "Two-party/one-party consent and disclosure for recorded disclosures.", "Legal"),
    ("Electronic acknowledgment", "E-SIGN / UETA validity of portal, SMS, and work-order acknowledgments.", "Legal"),
]

# ---------------------------------------------------------------------------
# EXECUTIVE DECISIONS + DATA NEEDED
# ---------------------------------------------------------------------------
EXEC_DECISIONS = [
    ("Approve the fee posture", "Adopt the recommended Balanced fee schedule ($75 residential / $125 business) versus Conservative or Full-Cost-Recovery.", "CEO / CFO / COO"),
    ("Approve the protection-plan launch and price", "Launch RIVR Tech Home Maintenance Protection at $9.99/mo (vs. $7.99 or $12.99), pending insurance/legal review.", "CEO / CFO"),
    ("Approve the courtesy-waiver and grace period", "Adopt the first-incident courtesy waiver and a 30-day warning-only period before billing begins.", "COO / CX"),
    ("Approve the effective date and rollout budget", "Set the effective date and fund the ~$95K one-time implementation.", "CEO / CFO"),
    ("Approve legal/regulatory review scope", "Authorize NC consumer-protection, tax, and insurance-characterization review before go-live.", "CEO / General Counsel"),
]

DATA_NEEDED = [
    ("Total and segment customer counts", "Exact residential vs. business active-service counts.", "Billing system"),
    ("12-month trouble-ticket volume", "Monthly tickets, dispatch rate, and remote-resolution rate.", "Ticketing / support platform"),
    ("Historical dispatch dispositions", "Share of dispatches that were customer-caused vs. network.", "Field/ops records"),
    ("Actual loaded technician cost", "Fully burdened hourly cost per field technician.", "Finance / HR"),
    ("True cost per truck roll", "Vehicle, fuel, materials, and admin per dispatch.", "Finance / Fleet"),
    ("Average and travel time per visit", "On-site plus windshield time per dispatch.", "Field ops"),
    ("Current collection & bad-debt rates", "Collection and write-off experience on customer charges.", "Finance / AR"),
    ("Protection-plan interest / benchmark", "Take-rate benchmark or survey for the optional plan.", "Marketing / CX"),
    ("Blended ARPU and churn baseline", "Revenue per customer and current churn for impact modeling.", "Finance"),
    ("Implementation and billing-config quotes", "Real quotes for billing changes, portal, and training.", "IT / Finance / Vendors"),
]

# ---------------------------------------------------------------------------
# ASSUMPTIONS REGISTER (auto-built from inputs flagged is_assumption)
# ---------------------------------------------------------------------------
def assumptions_register():
    rows = []
    for key, label, value, unit, is_assump, note in FIN_INPUTS:
        if is_assump:
            if unit == "pct":
                shown = f"{value*100:.1f}%"
            elif unit == "usd":
                shown = f"${value:,.2f}"
            else:
                shown = f"{value:,.0f}" if isinstance(value, (int, float)) and value >= 100 else str(value)
            rows.append((label, shown, note))
    return rows


def money(x):
    return f"${x:,.0f}"


def money2(x):
    return f"${x:,.2f}"


if __name__ == "__main__":
    r = compute_model()
    print("=== EXPECTED SCENARIO (from assumptions) ===")
    for k in ["annual_dispatches", "cost_per_dispatch", "annual_dispatch_expense",
              "cust_caused_dispatch_cost", "billable_visits", "net_fee_revenue",
              "protection_members", "protection_revenue", "protection_margin",
              "deflection_savings", "total_cost_recovery", "cost_recovery_pct",
              "one_time_cost", "year1_net", "payback_months", "three_year_net"]:
        v = r[k]
        if v is None:
            print(f"{k:32s} = n/a")
        elif "pct" in k:
            print(f"{k:32s} = {v*100:.1f}%")
        elif any(t in k for t in ["cost", "revenue", "net", "savings", "recovery", "expense"]) and "pct" not in k:
            print(f"{k:32s} = ${v:,.0f}")
        else:
            print(f"{k:32s} = {v:,.1f}")
