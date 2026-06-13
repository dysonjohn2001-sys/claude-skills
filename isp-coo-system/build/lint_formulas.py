import openpyxl, re, sys
wb = openpyxl.load_workbook('ISP_COO_Executive_Management_System.xlsx')
sheets = set(wb.sheetnames)
issues = []
sheet_ref = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)!")
n_formulas = 0
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for cell in row:
            v = cell.value
            if isinstance(v, str) and v.startswith('='):
                n_formulas += 1
                f = v
                # balanced parens
                if f.count('(') != f.count(')'):
                    issues.append((ws.title, cell.coordinate, 'UNBALANCED PARENS', f[:80]))
                # balanced quotes
                if f.count('"') % 2 != 0:
                    issues.append((ws.title, cell.coordinate, 'UNBALANCED QUOTES', f[:80]))
                # referenced sheets exist
                for m in set(sheet_ref.findall(f)):
                    # skip function-name false positives by requiring it be a known-ish token; check membership
                    if m not in sheets and m.upper() not in ('IF','IFERROR','SUMIFS','COUNTIFS','AVERAGEIFS','INDEX','MATCH','LARGE','SMALL','AGGREGATE','ROW','TEXT','AVERAGE','SUM'):
                        # only flag if it looks like an intended sheet (Capitalized_ with underscore or known data tabs)
                        issues.append((ws.title, cell.coordinate, f'UNKNOWN SHEET REF: {m}', f[:80]))
print(f"Formulas scanned: {n_formulas}")
print(f"Issues: {len(issues)}")
for it in issues[:60]:
    print(' -', it)
