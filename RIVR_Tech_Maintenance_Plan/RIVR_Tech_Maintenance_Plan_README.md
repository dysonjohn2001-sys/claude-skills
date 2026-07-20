# RIVR Tech — Customer-Premises Maintenance & Billable Trouble-Visit Program

**Prepared for:** LREMC Technologies, LLC d/b/a RIVR Tech
**Region:** Southeastern North Carolina broadband, managed Wi‑Fi, and voice services
**Version:** v1.0 (Draft for Executive Review) · **Date:** 2026‑07‑20
**Status:** Internal working package — **recommendations and labeled assumptions only.**

> ⚠️ **This package is not legal advice.** It contains draft recommendations and clearly
> labeled assumptions. Numerous provisions require legal, regulatory, accounting, insurance,
> and executive review before adoption. Nothing here is established RIVR Tech policy until
> approved.

---

## 1. What This Package Is

A complete, editable program that lets RIVR Tech **keep all network and equipment repairs
free** while introducing **fair, documented charges only for customer‑premises trouble
visits**, backed by strong remote troubleshooting, advance disclosure, an optional
maintenance‑protection plan, employee training, customer education, a financial model, and a
90‑day implementation plan.

**Design promise:** A fee is *never* charged just because a technician was dispatched. A fee
requires a documented customer‑premises cause, advance disclosure, and the correct approval.

---

## 2. Recommended Program (at a glance)

| Element | Recommendation |
|---|---|
| Fee posture | **Balanced** |
| Residential customer‑premises visit | **$75** |
| Business customer‑premises visit | **$125** |
| Additional labor (after first 30 min) | $35 per 30 min |
| Missed appointment / denied access | $35 (first‑time courtesy typical) |
| Equipment relocation | from $95 + materials |
| Inside‑wiring repair | from $75 + materials |
| After‑hours customer‑caused surcharge | +$75 |
| Confirmed RIVR Tech network/equipment problem | **$0 (always free)** |
| Inconclusive / no‑trouble‑found | **$0** |
| Optional protection plan | **RIVR Tech Home Maintenance Protection — $9.99/month** |
| First customer‑caused incident | One‑time educational courtesy waiver when appropriate |
| Grace period | 30‑day warning‑only period before billing begins |

Alternatives modeled: **Conservative** ($60/$99) and **Full‑Cost‑Recovery** ($89/$149).

---

## 3. Projected Financial Result — Expected Scenario

> Model outputs under **labeled assumptions**. Replace the ten RIVR Tech data points (Section 7)
> to finalize. Live formulas are in `03_Financial_Model/Maintenance_Program_Financial_Model.xlsx`.

| Metric | Expected |
|---|---|
| Cost per dispatch (loaded) | $130 |
| Annual customer‑caused dispatch cost (today, absorbed) | $329,004 |
| Net trouble‑visit fee revenue (Year 1) | $97,436 |
| Protection‑plan contribution margin (Year 1) | $142,276 |
| Avoided‑truck‑roll (deflection) savings | $144,300 |
| Cost recovery of customer‑caused dispatch cost | **73%** |
| **Year 1 net financial effect** (after ~$95K one‑time) | **$245,722** |
| Implementation payback period | **3.3 months** |
| **Three‑year net financial effect** | **$978,275** |

The primary economic driver is **avoided truck rolls (deflection)**, not fee revenue.

---

## 4. Five Decisions Requiring Executive Approval

1. **Approve the fee posture** — adopt Balanced ($75/$125) vs. Conservative or Full‑Cost‑Recovery. *(CEO/CFO/COO)*
2. **Approve the protection‑plan launch and price** — $9.99/mo, pending insurance/legal review. *(CEO/CFO)*
3. **Approve the courtesy‑waiver and 30‑day grace period.** *(COO/CX)*
4. **Approve the effective date and ~$95K one‑time rollout budget.** *(CEO/CFO)*
5. **Approve legal/regulatory review scope** — NC consumer‑protection, tax, insurance characterization. *(CEO/General Counsel)*

---

## 5. Ten RIVR Tech Data Points Needed (replace assumptions)

1. Total and segment (residential vs. business) customer counts
2. 12‑month trouble‑ticket volume, dispatch rate, remote‑resolution rate
3. Historical dispatch dispositions (customer‑caused vs. network share)
4. Actual fully loaded technician hourly cost
5. True cost per truck roll (vehicle, fuel, materials, admin)
6. Average on‑site + travel time per visit
7. Current collection and bad‑debt rates on customer charges
8. Protection‑plan interest / take‑rate benchmark
9. Blended ARPU and current churn baseline
10. Real implementation, billing‑config, and training quotes

All modeled assumptions are flagged in the workbook (`Inputs` sheet, yellow cells) and in each
document's assumption callouts.

---

## 6. File Inventory

All paths are relative to `RIVR_Tech_Maintenance_Plan/`.

### 01_Executive
| File | Description |
|---|---|
| `RIVR_Tech_Maintenance_Business_Case.docx` | Full business case, financials, risks, recommendation |
| `RIVR_Tech_Executive_Decision_Summary.docx` | One‑read executive briefing + the five decisions |

### 02_Policy_and_SOP
| File | Description |
|---|---|
| `Customer_Premises_Maintenance_Policy.docx` | Formal 34‑section policy (proposed) + appendices |
| `Support_and_Field_Operations_SOP.docx` | Remote‑triage SOP, field‑tech SOP, codes, authorization language |
| `Trouble_Visit_Responsibility_Matrix.xlsx` | 42‑scenario responsibility matrix + classification key + fee schedule |

### 03_Financial_Model
| File | Description |
|---|---|
| `Maintenance_Program_Financial_Model.xlsx` | 9‑sheet live model (formulas), 3 dashboard charts, scenarios, sensitivity |

### 04_Training
| File | Description |
|---|---|
| `Maintenance_Program_Employee_Training.pptx` | 20‑slide, 60‑minute training deck (all roles) |
| `Employee_Quick_Reference_Guide.docx` | Pocket guide: free vs. billable, fees, scripts |
| `Facilitator_and_Manager_Coaching_Guide.docx` | Agenda, role coaching, role‑plays, rubric |
| `Employee_Knowledge_Assessment.docx` | 18 questions + answer key (80% pass) |

### 05_Customer_Communications
| File | Description |
|---|---|
| `Customer_Communication_Package.docx` | 60‑day plan, announcement, email, bill message/insert, 22 FAQs, scripts, notices |
| `Customer_Maintenance_Handout.docx` | Technician leave‑behind / new‑customer handout |

### 06_Implementation
| File | Description |
|---|---|
| `90_Day_Implementation_Tracker.xlsx` | 18‑task, 5‑phase tracker (owners, dates, risks, exec decisions) |
| `Maintenance_Program_KPI_Dashboard.xlsx` | 25 KPIs with editable targets, R/Y/G thresholds + waiver‑tracking log |

### 07_Final_Presentation
| File | Description |
|---|---|
| `Maintenance_Program_Executive_Presentation.pptx` | 11‑slide executive decision deck |

### 08_Source_Files
| File | Description |
|---|---|
| `build_scripts/rivr_content.py` | **Single source of truth** — content, fees, matrix, codes, financial model |
| `build_scripts/docx_helpers.py` | Shared Word formatting helpers |
| `build_scripts/build_docx.py` | Builds all 9 Word documents |
| `build_scripts/build_xlsx.py` | Builds all 4 Excel workbooks |
| `build_scripts/build_pptx.py` | Builds both PowerPoint decks |
| `build_scripts/validate.py` | Structural validation of every deliverable |

### Root
| File | Description |
|---|---|
| `RIVR_Tech_Maintenance_Plan_README.md` | This file |

---

## 7. How to Regenerate / Edit

The entire package is generated from Python so it stays internally consistent. To change a fee,
an assumption, or a scenario, edit **`08_Source_Files/build_scripts/rivr_content.py`** (the single
source of truth) and rebuild:

```bash
cd 08_Source_Files/build_scripts
pip install python-docx openpyxl python-pptx        # one-time
python3 build_docx.py     # 9 Word docs
python3 build_xlsx.py     # 4 Excel workbooks
python3 build_pptx.py     # 2 PowerPoint decks
python3 validate.py       # structural validation
```

Editing the delivered `.docx/.xlsx/.pptx` files directly in Office also works — they are fully
editable. The Excel model uses **live formulas** driven by the yellow `Inputs` cells, so changing
an input recalculates everything (open in Excel and allow recalculation).

---

## 8. Color Coding (Excel workbooks)

| Color | Meaning |
|---|---|
| 🟨 Yellow | User input (edit these) |
| 🟦 Light blue | Calculated (formula) |
| 🟩 Green | Recommended assumption / headline result |
| 🟧 Clay | Review / warning / executive‑decision flag |

---

## 9. Validation Performed

- **Financial model formulas independently evaluated** with a Python Excel‑formula engine:
  all checked cells match the reference model exactly, **0 formula errors**. Fixed one
  off‑by‑one cell reference discovered during validation.
- **All 15 document/workbook deliverables reopen cleanly** (valid Office XML).
- **PowerPoint decks:** 0 shapes overflow slide bounds; 0 empty slides.
- **Word tables:** no table exceeds usable page width.
- **Existing files:** none overwritten — this is a net‑new folder with no prior RIVR Tech source
  files present in the working directory.

### Known limitation — PDF/image rendering

The sandbox's LibreOffice could not load any file for headless PDF/image conversion
(`Error: source file could not be loaded` on every input, including trivial test files), so a
visual PDF render was **not** produced in this environment. Validation was therefore performed
**structurally** (reopening files, evaluating formulas, and geometric overflow checks) rather
than by visual page inspection. Before executive distribution, open each file in Microsoft
Office (or a working LibreOffice) and:
1. In each Word doc, right‑click the Table of Contents → **Update Field** to build page numbers.
2. In the Excel model, allow recalculation (the formula engine confirmed values already match).
3. Skim each deck/doc for any environment‑specific font substitution.

---

## 10. Legal, Regulatory & Insurance Review Flags

The following require review before adoption (detailed in the Policy, Appendix B):
NC consumer‑protection requirements · residential & business customer agreements · SLAs ·
voice‑service obligations · Lifeline/low‑income customers · reasonable accommodations · billing
practices · tax treatment · **protection‑plan structure (must NOT be insurance)** · insurance
characterization · record retention · call recording · electronic acknowledgment (E‑SIGN/UETA).

---

## 11. Terminology Discipline

- Use **RIVR Tech** consistently; **LREMC Technologies, LLC d/b/a RIVR Tech** where legally
  appropriate.
- Say **"customer‑premises issue"** or **"issue outside the RIVR Tech network"** — never
  "customer fault."
- The protection plan is a **service/maintenance plan**, not insurance or a warranty.
