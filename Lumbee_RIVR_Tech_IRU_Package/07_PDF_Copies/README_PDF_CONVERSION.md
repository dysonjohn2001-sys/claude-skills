# PDF Copies — Conversion Instructions

**DRAFT FOR DISCUSSION – SUBJECT TO LEGAL, GRANT AND FINANCIAL REVIEW**

Automated PDF generation could **not** be completed in the build environment.
LibreOffice is installed but is non-functional in this sandbox — it returns
`Error: source file could not be loaded` for every input file, including a
trivial test document. No PDFs were produced here (so none are misrepresented
as final).

The conversion script is ready to run in any environment with a working
LibreOffice/OpenOffice. From the package root:

```bash
python3 Scripts/make_pdfs.py
```

That converts every `.docx` in `01_Executive`, `02_Core_Agreements`,
`03_Operational_Schedules`, `05_Authorizations`, and `06_Review_Materials`
into PDF here in `07_PDF_Copies/`.

Or convert a single file directly:

```bash
soffice --headless --convert-to pdf --outdir 07_PDF_Copies \
  "02_Core_Agreements/01_Master_Development_Construction_and_Operating_Agreement.docx"
```

**Before converting:** open each `.docx` in Microsoft Word and run
*Update Field* (Ctrl+A, then F9) so the Table of Contents and page-number
fields populate — LibreOffice/Word render these on open, but a headless
convert may leave a TOC placeholder until fields are updated.

The Excel workbooks (`.xlsx`) are working models and are intended to remain in
spreadsheet form, not PDF.
