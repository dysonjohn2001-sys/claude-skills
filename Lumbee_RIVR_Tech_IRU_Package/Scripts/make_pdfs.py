"""
make_pdfs.py — Convert every .docx in the package to PDF in 07_PDF_Copies/
using LibreOffice headless. Mirrors the source subfolder in the filename prefix
so the flat PDF folder stays organized.

Usage: python3 make_pdfs.py
"""
import os
import subprocess
import sys
import glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

PKG = C.PKG_DIR
PDF_DIR = os.path.join(PKG, "07_PDF_Copies")
os.makedirs(PDF_DIR, exist_ok=True)

SRC_FOLDERS = ["01_Executive", "02_Core_Agreements", "03_Operational_Schedules",
               "05_Authorizations", "06_Review_Materials"]

soffice = None
for cand in ("libreoffice", "soffice"):
    from shutil import which
    if which(cand):
        soffice = cand
        break

if not soffice:
    print("LibreOffice not found — skipping PDF conversion.")
    sys.exit(0)

converted, failed = [], []
for folder in SRC_FOLDERS:
    src = os.path.join(PKG, folder)
    if not os.path.isdir(src):
        continue
    for path in sorted(glob.glob(os.path.join(src, "*.docx"))):
        try:
            # Convert into PDF_DIR; LibreOffice keeps the base name.
            r = subprocess.run(
                [soffice, "--headless", "--convert-to", "pdf", "--outdir", PDF_DIR, path],
                capture_output=True, text=True, timeout=180,
            )
            base = os.path.splitext(os.path.basename(path))[0] + ".pdf"
            out_pdf = os.path.join(PDF_DIR, base)
            if os.path.exists(out_pdf):
                converted.append(base)
            else:
                failed.append((os.path.basename(path), r.stderr.strip()[:200]))
        except Exception as e:
            failed.append((os.path.basename(path), str(e)[:200]))

print(f"Converted {len(converted)} documents to PDF in 07_PDF_Copies/")
for c in converted:
    print("  +", c)
if failed:
    print(f"\n{len(failed)} conversion(s) failed:")
    for name, err in failed:
        print("  -", name, "::", err)
