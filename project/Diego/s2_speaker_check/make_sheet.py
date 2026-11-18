"""S2: Diego's copy of data/processed/speaker_check_sample.csv for the hand check, as a spreadsheet.

Run from project/:  python Diego/s2_speaker_check/make_sheet.py
Same 60 rows; columns reordered so 'correct (y/n)' is second to last (y/n dropdown) and source_url is last
(clickable). The shared CSV is not changed.
"""
from pathlib import Path
import sys
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

OUT = Path(__file__).parent / "speaker_check.xlsx"
if OUT.exists():
    sys.exit(f"{OUT} exists; checking may have started, so it was not overwritten.")
s = pd.read_csv("data/processed/speaker_check_sample.csv")
cols = [c for c in s.columns if c not in ("correct (y/n)", "source_url")] + ["correct (y/n)", "source_url"]
s = s[cols]
widths = {"day": 11, "item": 8, "assigned_member": 24, "party": 6, "state": 6, "n_words": 8,
          "first_300_chars": 90, "correct (y/n)": 12, "source_url": 40}
wb = Workbook(); ws = wb.active; ws.title = "S2 speaker check"
for j, c in enumerate(cols, start=1):
    h = ws.cell(row=1, column=j, value=c); h.font = Font(bold=True); h.fill = PatternFill("solid", fgColor="DDE4EE")
    ws.column_dimensions[h.column_letter].width = widths.get(c, 12)
yn = DataValidation(type="list", formula1='"y,n"', allow_blank=True); ws.add_data_validation(yn)
for i, row in enumerate(s.itertuples(index=False), start=2):
    for j, (c, v) in enumerate(zip(cols, row), start=1):
        v = None if pd.isna(v) else v
        cell = ws.cell(row=i, column=j, value=v)
        cell.alignment = Alignment(wrap_text=(c == "first_300_chars"), vertical="top")
        if c == "source_url" and v:
            cell.hyperlink, cell.font = v, Font(color="0563C1", underline="single")
        if c == "correct (y/n)":
            cell.fill = PatternFill("solid", fgColor="FFF4CC"); yn.add(cell.coordinate)
ws.freeze_panes = "A2"
wb.save(OUT)
print("wrote", OUT, len(s), "rows")
