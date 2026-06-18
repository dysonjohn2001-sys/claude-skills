"""
Sample data + schema for the ISP COO Executive Management System.

Provides a full fiscal year (Jul-2025 .. Jun-2026) of realistic ISP / fiber
records so every dashboard, KPI, and chart renders live on first open.
All tables are keyed by a Month label and a sequential Period index (1..12)
so month-to-date / year-to-date / rolling-12 rollups are clean.

Context fit: regional fiber ISP operating in southeastern North Carolina
counties (Robeson, Hoke, Cumberland, Scotland, Bladen, Columbus), funded in
part by BEAD / CAB / state grant capital projects.
"""
import random

random.seed(42)

# Fiscal year: Jul-2025 .. Jun-2026 (FY just completed; current month = Jun-2026)
MONTHS = ["Jul-2025", "Aug-2025", "Sep-2025", "Oct-2025", "Nov-2025", "Dec-2025",
          "Jan-2026", "Feb-2026", "Mar-2026", "Apr-2026", "May-2026", "Jun-2026"]
PERIODS = list(range(1, 13))
CURRENT_MONTH = MONTHS[-1]
CURRENT_PERIOD = 12

COUNTIES = ["Robeson", "Hoke", "Cumberland", "Scotland", "Bladen", "Columbus"]
SEGMENTS = ["Residential", "Business", "Enterprise"]
CHANNELS = ["Door-to-Door", "Inbound Call", "Website", "Referral", "Event", "HOA/Developer"]
CAMPAIGNS = ["Spring Fiber Push", "BEAD Awareness", "Referral Rewards", "Business Connect", "HOA Direct"]
REPS = ["Maria Lopez", "James Carter", "Tanya Hunt", "Derek Oxendine", "Sarah Locklear"]
PRODUCTS = ["Residential Internet", "Business Internet", "Enterprise / DIA", "Managed WiFi", "Voice", "Construction / Other"]
STAGES = ["Prospect", "Qualified", "Proposal", "Negotiation", "Closed-Won", "Closed-Lost"]
LOST_REASONS = ["Price", "Competitor Fiber", "No Coverage Yet", "Timing", "Credit/Install Fee", "Lost Contact"]

# ---------------------------------------------------------------------------
# Dropdown / pick-lists (Lists sheet) — column oriented
# ---------------------------------------------------------------------------
LISTS = {
    "Months": MONTHS,
    "Counties": COUNTIES,
    "Segments": SEGMENTS,
    "Channels": CHANNELS,
    "Campaigns": CAMPAIGNS,
    "Reps": REPS,
    "Products": PRODUCTS,
    "Pipeline Stage": STAGES,
    "Opp Type": ["Standard", "HOA/Developer", "Bulk Agreement", "Enterprise/DIA"],
    "Lost Reason": LOST_REASONS,
    "Project Status": ["On Track", "At Risk", "Behind", "Complete"],
    "Build Phase Status": ["Not Started", "In Progress", "Complete"],
    "Grant Program": ["BEAD", "CAB", "ARPA", "State Grant", "RDOF"],
    "Grant Status": ["Not Submitted", "Submitted", "Under Review", "Approved", "Partially Paid", "Paid", "Denied"],
    "Risk Likelihood": [1, 2, 3, 4, 5],
    "Risk Impact": [1, 2, 3, 4, 5],
    "Risk Status": ["Open", "Mitigating", "Monitoring", "Closed"],
    "Risk Category": ["Construction", "Financial", "Regulatory", "Supply Chain", "Staffing", "Market", "Grant/Compliance"],
    "Action Status": ["Not Started", "In Progress", "Blocked", "Complete"],
    "Priority": ["Low", "Medium", "High", "Critical"],
    "Yes/No": ["Yes", "No"],
    "RYG": ["Green", "Yellow", "Red"],
}

# ---------------------------------------------------------------------------
# Customer_Data  (one row per month; subscriber counts)
# cols: Month | Period | Total Customers | New Sales | Disconnects | Homes Passed (cum)
# ---------------------------------------------------------------------------
def build_customers():
    rows = []
    total = 4180
    homes = 17800
    for p, m in zip(PERIODS, MONTHS):
        new = random.randint(360, 540)
        disc = random.randint(70, 135)
        total = total + new - disc
        homes += random.randint(900, 1700)
        rows.append([m, p, total, new, disc, homes])
    return rows

CUSTOMERS = build_customers()

# ---------------------------------------------------------------------------
# Financial_Data (one row per month)
# cols: Month|Period|Revenue|MRR|CapEx|OpEx|Labor|Contractor|GrantReimb|
#       BudgetRevenue|BudgetOpEx|BudgetCapEx|ForecastRevenue|CashBalance|
#       InstallsForCost|CostPerInstall_input(blank->calc)
# ARPU & cost-per-x are computed on the dashboard from these + customer/ops data.
# ---------------------------------------------------------------------------
def build_financials():
    rows = []
    cash = 5_200_000
    for i, (cust, p, m) in enumerate(zip(CUSTOMERS, PERIODS, MONTHS)):
        total_cust = cust[2]
        arpu = 77 + i * 0.6
        mrr = round(total_cust * arpu, 0)
        nonrec = random.randint(40000, 90000)        # install fees, equipment
        revenue = round(mrr + nonrec, 0)
        capex = random.randint(520000, 980000)
        labor = random.randint(210000, 250000)
        contractor = random.randint(180000, 360000)
        other_opex = random.randint(120000, 175000)
        opex = labor + other_opex                      # opex excludes contractor capex labor
        grant = random.choice([0, 0, 320000, 410000, 555000, 0, 290000])
        budget_rev = round(revenue * random.uniform(0.95, 1.07), 0)
        budget_opex = round(opex * random.uniform(0.96, 1.06), 0)
        budget_capex = round(capex * random.uniform(0.92, 1.08), 0)
        forecast_rev = round(revenue * random.uniform(0.99, 1.03), 0)
        cash = cash + revenue + grant - opex - capex - contractor
        rows.append([m, p, revenue, mrr, capex, opex, labor, contractor, grant,
                     budget_rev, budget_opex, budget_capex, forecast_rev, round(cash, 0)])
    return rows

FINANCIALS = build_financials()

# ---------------------------------------------------------------------------
# Operations_Data (one row per month)
# cols: Month|Period|HomesPassedAdded|FootageBuilt|DropsCompleted|
#       InstallsScheduled|InstallsCompleted|AvgDaysToInstall|TroubleTickets|
#       RepeatTickets|Outages|Activations|SplicesCompleted
# ---------------------------------------------------------------------------
def build_operations():
    rows = []
    for i, (cust, p, m) in enumerate(zip(CUSTOMERS, PERIODS, MONTHS)):
        hp_added = cust[4] if False else random.randint(900, 1700)
        footage = random.randint(38000, 72000)
        installs_done = cust[3] - random.randint(-20, 40)   # ~ new sales
        installs_done = max(installs_done, 250)
        installs_sched = installs_done + random.randint(40, 140)
        drops = installs_done + random.randint(20, 90)
        avg_days = round(random.uniform(6.5, 13.5) - i * 0.25, 1)
        avg_days = max(avg_days, 5.0)
        tickets = random.randint(180, 340)
        repeat = int(tickets * random.uniform(0.08, 0.16))
        outages = random.randint(1, 6)
        activations = installs_done - random.randint(0, 15)
        splices = random.randint(120, 260)
        rows.append([m, p, hp_added, footage, drops, installs_sched, installs_done,
                     avg_days, tickets, repeat, outages, activations, splices])
    return rows

OPERATIONS = build_operations()

# ---------------------------------------------------------------------------
# Sales_Targets (one row per month)  Month|Period|SalesGoal(units)|RevenueGoal(MRR$)
# ---------------------------------------------------------------------------
def build_targets():
    rows = []
    for cust, p, m in zip(CUSTOMERS, PERIODS, MONTHS):
        goal = int(round((cust[3]) / 10.0) * 10) + random.choice([-30, 0, 20, 40])
        rev_goal = goal * 80
        rows.append([m, p, goal, rev_goal])
    return rows

TARGETS = build_targets()

# ---------------------------------------------------------------------------
# Sales_Data (multiple rows per month — one per county, with segment mix)
# cols: Month|Period|County|Segment|Channel|Campaign|Rep|Leads|Qualified|
#       Sales(units)|NewMRR($)|DoorKnocks
# ---------------------------------------------------------------------------
def build_sales():
    rows = []
    for cust, p, m in zip(CUSTOMERS, PERIODS, MONTHS):
        month_new = cust[3]
        # distribute across counties
        weights = [random.uniform(0.8, 1.3) for _ in COUNTIES]
        wsum = sum(weights)
        for c, w in zip(COUNTIES, weights):
            share = w / wsum
            sales = max(1, int(round(month_new * share)))
            seg = random.choices(SEGMENTS, weights=[0.78, 0.18, 0.04])[0]
            channel = random.choice(CHANNELS)
            campaign = random.choice(CAMPAIGNS)
            rep = random.choice(REPS)
            qualified = sales + random.randint(8, 40)
            leads = qualified + random.randint(30, 110)
            arpu = 79 if seg == "Residential" else (180 if seg == "Business" else 850)
            new_mrr = sales * arpu
            knocks = random.randint(150, 600) if channel == "Door-to-Door" else random.randint(0, 60)
            rows.append([m, p, c, seg, channel, campaign, rep, leads, qualified,
                         sales, new_mrr, knocks])
    return rows

SALES = build_sales()

# ---------------------------------------------------------------------------
# Pipeline (open + recently closed opportunities)
# cols: OppID|Name|County|Segment|Type|Stage|Value(ARR$)|Rep|CloseMonth|LostReason
# ---------------------------------------------------------------------------
def build_pipeline():
    names = [
        ("Lumberton Business Park", "Robeson", "Business", "Standard"),
        ("Pembroke Town Center Bulk", "Robeson", "Business", "Bulk Agreement"),
        ("UNCP Campus DIA", "Robeson", "Enterprise", "Enterprise/DIA"),
        ("Raeford Logistics DIA", "Hoke", "Enterprise", "Enterprise/DIA"),
        ("Maxton Industrial", "Robeson", "Business", "Standard"),
        ("Highland Trace HOA", "Cumberland", "Residential", "HOA/Developer"),
        ("Saddlebrook Developer", "Hoke", "Residential", "HOA/Developer"),
        ("St. Pauls Clinic Group", "Robeson", "Business", "Standard"),
        ("Laurinburg Logistics", "Scotland", "Enterprise", "Enterprise/DIA"),
        ("Elizabethtown Retail", "Bladen", "Business", "Standard"),
        ("Whiteville School District", "Columbus", "Enterprise", "Enterprise/DIA"),
        ("Red Springs Apartments Bulk", "Robeson", "Residential", "Bulk Agreement"),
        ("Fayetteville Tech Park", "Cumberland", "Enterprise", "Enterprise/DIA"),
        ("Shannon Farms Developer", "Robeson", "Residential", "HOA/Developer"),
        ("Hope Mills Plaza", "Cumberland", "Business", "Standard"),
        ("Rowland Manufacturing", "Robeson", "Business", "Standard"),
        ("Tar Heel Cold Storage", "Bladen", "Enterprise", "Enterprise/DIA"),
        ("Parkton HOA Phase 2", "Robeson", "Residential", "HOA/Developer"),
        ("Lumber River Medical", "Robeson", "Business", "Standard"),
        ("Scotland Health DIA", "Scotland", "Enterprise", "Enterprise/DIA"),
        ("Bladenboro Bulk MDU", "Bladen", "Residential", "Bulk Agreement"),
        ("Chadbourn Town Hall", "Columbus", "Business", "Standard"),
        ("Aberdeen Distribution", "Hoke", "Enterprise", "Enterprise/DIA"),
        ("McColl Crossing HOA", "Scotland", "Residential", "HOA/Developer"),
        ("Fairmont Business Row", "Robeson", "Business", "Standard"),
    ]
    rows = []
    for i, (nm, county, seg, typ) in enumerate(names, start=1):
        if seg == "Enterprise":
            value = random.randint(60000, 240000)
        elif seg == "Business":
            value = random.randint(9000, 45000)
        else:
            value = random.randint(15000, 80000)  # bulk/HOA aggregate ARR
        # stage distribution: weight toward open stages, a few closed
        stage = random.choices(STAGES, weights=[0.18, 0.22, 0.22, 0.16, 0.12, 0.10])[0]
        rep = random.choice(REPS)
        close_m = random.choice(MONTHS[6:]) if stage not in ("Closed-Won", "Closed-Lost") else random.choice(MONTHS[8:])
        lost = random.choice(LOST_REASONS) if stage == "Closed-Lost" else ""
        rows.append([f"OPP-{1000+i}", nm, county, seg, typ, stage, value, rep, close_m, lost])
    return rows

PIPELINE = build_pipeline()

# ---------------------------------------------------------------------------
# Revenue_Detail (Month x Product)  cols: Month|Period|Product|Segment|Revenue|COGS
# ---------------------------------------------------------------------------
def build_revenue_detail():
    seg_for = {
        "Residential Internet": "Residential", "Managed WiFi": "Residential",
        "Business Internet": "Business", "Voice": "Business",
        "Enterprise / DIA": "Enterprise", "Construction / Other": "Wholesale/Other",
    }
    mix = {
        "Residential Internet": 0.52, "Business Internet": 0.18, "Enterprise / DIA": 0.13,
        "Managed WiFi": 0.05, "Voice": 0.04, "Construction / Other": 0.08,
    }
    cogs_pct = {
        "Residential Internet": 0.28, "Business Internet": 0.26, "Enterprise / DIA": 0.34,
        "Managed WiFi": 0.40, "Voice": 0.45, "Construction / Other": 0.62,
    }
    rows = []
    for fin, p, m in zip(FINANCIALS, PERIODS, MONTHS):
        revenue = fin[2]
        for prod in PRODUCTS:
            rev = round(revenue * mix[prod] * random.uniform(0.92, 1.08), 0)
            cogs = round(rev * cogs_pct[prod] * random.uniform(0.95, 1.05), 0)
            rows.append([m, p, prod, seg_for[prod], rev, cogs])
    return rows

REVENUE_DETAIL = build_revenue_detail()

# ---------------------------------------------------------------------------
# Project_Data (capital build projects — static rows, not monthly)
# cols: Project|County|Type|Grant Program|% Complete|Status|HomesPassed Target|
#       HomesPassed Actual|Footage Target|Footage Built|Capital Budget|
#       Capital Spent|Permitting|Make-Ready|Splicing|Contractor|Contractor Score|Blocker
# ---------------------------------------------------------------------------
PROJECTS = [
    ["Robeson BEAD Zone 1", "Robeson", "Greenfield", "BEAD", 0.78, "On Track", 3200, 2496, 165000, 128700, 4_100_000, 3_050_000, "Complete", "Complete", "In Progress", "FiberBuild Co", 8.6, ""],
    ["Hoke CAB Expansion", "Hoke", "Greenfield", "CAB", 0.54, "At Risk", 2100, 1134, 110000, 61600, 2_650_000, 1_590_000, "In Progress", "In Progress", "Not Started", "Sandhill Construction", 6.9, "Make-ready pole attach delays (utility)"],
    ["Pembroke Core Ring", "Robeson", "Backbone", "State Grant", 0.92, "On Track", 1400, 1288, 48000, 44200, 1_200_000, 1_080_000, "Complete", "Complete", "Complete", "FiberBuild Co", 9.1, ""],
    ["Scotland RDOF Area", "Scotland", "Greenfield", "RDOF", 0.41, "Behind", 2600, 1066, 138000, 56600, 3_300_000, 1_420_000, "In Progress", "Not Started", "Not Started", "Cape Fear Underground", 5.8, "Permitting backlog + wet-weather standdown"],
    ["Cumberland Fiber Fill-in", "Cumberland", "Overbuild", "BEAD", 0.66, "On Track", 1900, 1254, 92000, 60700, 2_050_000, 1_330_000, "Complete", "In Progress", "In Progress", "Sandhill Construction", 7.4, ""],
    ["Bladen ARPA Rural", "Bladen", "Greenfield", "ARPA", 0.33, "At Risk", 1500, 495, 102000, 33700, 2_400_000, 760_000, "In Progress", "Not Started", "Not Started", "Cape Fear Underground", 6.2, "Material lead time on conduit"],
    ["Columbus BEAD Zone 2", "Columbus", "Greenfield", "BEAD", 0.18, "Behind", 2800, 504, 150000, 27000, 3_500_000, 590_000, "In Progress", "Not Started", "Not Started", "Sandhill Construction", 6.5, "Design rework after make-ready survey"],
    ["Lumberton MDU Drops", "Robeson", "Drop/Activation", "State Grant", 0.85, "On Track", 900, 765, 18000, 15300, 540_000, 451_000, "Complete", "Complete", "Complete", "In-House Crew", 8.9, ""],
    ["Raeford Business Loop", "Hoke", "Backbone", "CAB", 0.71, "On Track", 600, 426, 26000, 18900, 980_000, 690_000, "Complete", "In Progress", "In Progress", "FiberBuild Co", 8.2, ""],
    ["Maxton Edge Extension", "Robeson", "Overbuild", "BEAD", 0.49, "At Risk", 1100, 539, 64000, 31400, 1_350_000, 690_000, "In Progress", "In Progress", "Not Started", "Sandhill Construction", 7.0, "Crew availability shared with Hoke CAB"],
]

# ---------------------------------------------------------------------------
# Grant_Data (reimbursement drawdowns)
# cols: Drawdown ID|Program|Project|Amount Requested|Amount Approved|Amount Received|
#       Status|Submission Date|Expected Date|Notes
# ---------------------------------------------------------------------------
GRANTS = [
    ["DRW-2025-014", "BEAD", "Robeson BEAD Zone 1", 980000, 980000, 980000, "Paid", "2025-08-12", "2025-10-01", "Milestone 2 paid in full"],
    ["DRW-2025-021", "BEAD", "Robeson BEAD Zone 1", 1150000, 1150000, 575000, "Partially Paid", "2025-11-03", "2026-01-15", "50% advanced; balance on inspection"],
    ["DRW-2025-009", "CAB", "Hoke CAB Expansion", 640000, 590000, 590000, "Paid", "2025-09-20", "2025-11-30", "Approved below request (ineligible poles)"],
    ["DRW-2026-002", "CAB", "Hoke CAB Expansion", 720000, 0, 0, "Under Review", "2026-02-10", "2026-05-01", "Awaiting make-ready documentation"],
    ["DRW-2025-031", "State Grant", "Pembroke Core Ring", 480000, 480000, 480000, "Paid", "2025-10-15", "2025-12-15", ""],
    ["DRW-2026-007", "RDOF", "Scotland RDOF Area", 560000, 0, 0, "Submitted", "2026-03-22", "2026-06-30", "Behind-schedule project; risk to drawdown"],
    ["DRW-2026-011", "ARPA", "Bladen ARPA Rural", 410000, 410000, 0, "Approved", "2026-04-05", "2026-07-15", "Payment scheduled next quarter"],
    ["DRW-2026-015", "BEAD", "Columbus BEAD Zone 2", 620000, 0, 0, "Not Submitted", "", "2026-08-01", "Pending Milestone 1 completion"],
]

# ---------------------------------------------------------------------------
# Risk_Register  cols: Risk ID|Description|Category|Likelihood|Impact|Owner|Mitigation|Status|Updated
# (Score + RYG computed in-sheet)
# ---------------------------------------------------------------------------
RISKS = [
    ["RSK-01", "Scotland RDOF build behind schedule threatens grant drawdown eligibility", "Grant/Compliance", 4, 5, "VP Construction", "Add second crew; weekly state check-in; replan milestones", "Mitigating", "2026-06-05"],
    ["RSK-02", "Make-ready / pole attachment delays from incumbent utility", "Regulatory", 4, 4, "COO", "Escalate to NCUC; pre-file remaining attachments", "Open", "2026-06-08"],
    ["RSK-03", "Contractor capacity shared across Hoke + Maxton slowing both", "Staffing", 3, 4, "VP Construction", "Negotiate dedicated crew; evaluate 2nd contractor", "Mitigating", "2026-06-02"],
    ["RSK-04", "Conduit / fiber material lead times (Bladen)", "Supply Chain", 3, 3, "Director of Supply", "Pre-order long-lead items; buffer stock", "Monitoring", "2026-05-28"],
    ["RSK-05", "Cash timing gap from delayed BEAD reimbursements", "Financial", 3, 5, "CFO", "Draw on revolver; accelerate drawdown documentation", "Open", "2026-06-10"],
    ["RSK-06", "Competitor fiber overbuild announced in Cumberland", "Market", 3, 3, "VP Sales", "Accelerate take-rate campaign; lock HOA agreements", "Monitoring", "2026-06-01"],
    ["RSK-07", "Repeat trouble tickets indicate splice quality issue in Zone 1", "Construction", 2, 3, "VP Operations", "QA audit on splice crews; rework plan", "Mitigating", "2026-06-06"],
    ["RSK-08", "Install backlog rising vs crew capacity in Robeson", "Staffing", 3, 3, "VP Operations", "Add install crew; offer install-fee promo off-peak", "Open", "2026-06-09"],
    ["RSK-09", "Columbus Zone 2 design rework may slip Milestone 1 + grant", "Grant/Compliance", 4, 4, "VP Construction", "Expedite redesign; parallel-path permitting", "Open", "2026-06-07"],
    ["RSK-10", "Key enterprise DIA deals concentrated with single rep", "Market", 2, 3, "VP Sales", "Cross-staff accounts; document pipeline", "Monitoring", "2026-05-20"],
]

# ---------------------------------------------------------------------------
# Board_Actions  cols: ID|Description|Category|Owner|Raised|Due|Priority|Status|Decision Needed
# ---------------------------------------------------------------------------
BOARD_ACTIONS = [
    ["ACT-01", "Approve $1.2M revolver draw to bridge BEAD reimbursement timing", "Financial", "CFO / Board", "2026-06-01", "2026-06-20", "Critical", "In Progress", "Yes"],
    ["ACT-02", "Authorize second construction contractor for Scotland + Columbus", "Construction", "COO", "2026-05-28", "2026-06-25", "High", "Not Started", "Yes"],
    ["ACT-03", "Approve revised capital plan reforecast (Q3 FY26)", "Financial", "CFO", "2026-06-05", "2026-07-01", "High", "Not Started", "Yes"],
    ["ACT-04", "Ratify HOA / bulk agreement pricing policy", "Commercial", "VP Sales", "2026-05-15", "2026-06-30", "Medium", "In Progress", "Yes"],
    ["ACT-05", "Approve install-crew headcount add (2 FTE) to clear backlog", "Operations", "VP Operations", "2026-06-08", "2026-06-22", "High", "Not Started", "Yes"],
    ["ACT-06", "Review competitive response plan for Cumberland overbuild", "Market", "VP Sales", "2026-06-02", "2026-07-10", "Medium", "Not Started", "No"],
    ["ACT-07", "Sign off on Q4 board reporting calendar", "Governance", "Chief of Staff", "2026-05-30", "2026-06-18", "Low", "Complete", "No"],
    ["ACT-08", "Approve splice-QA remediation budget for Zone 1", "Operations", "VP Operations", "2026-06-06", "2026-06-28", "Medium", "In Progress", "Yes"],
]
