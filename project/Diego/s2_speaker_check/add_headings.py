"""S2 helper: write speaker_check_with_headings.xlsx, the 60-row sheet plus the Congressional Record's own speaker
heading for each turn ("Mr. PERRY."), so Diego can compare it with assigned_member without opening every page.

Run from project/:  python Diego/s2_speaker_check/add_headings.py <folder with the 60 downloaded .htm pages>
The pages are the source_url of each row (govinfo.gov), saved as 0.htm ... 59.htm. For each turn the script finds
its first 80 characters in the page and takes the nearest heading before it, skipping the presiding officer
("The SPEAKER", "Mr. CHAIRMAN"). It does NOT fill in 'correct (y/n)': that column is Diego's.
"""
import html
import re
import sys
from pathlib import Path
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

HERE = Path(__file__).parent
pages = Path(sys.argv[1])
s = pd.read_csv("data/processed/speaker_check_sample.csv")
HEAD = re.compile(r"(?:Mr|Ms|Mrs|Miss|Madam)\. [A-Z][A-Z'\-]+(?: [A-Z][A-Z'\-]+)*(?: of [A-Z][a-z]+(?: [A-Z][a-z]+)?)?\.")
CHAIR = re.compile(r"(?:Mr|Ms|Mrs|Madam)\. (?:SPEAKER|CHAIR|CHAIRMAN)\.")
norm = lambda t: re.sub(r"\s+", " ", t)
heads, notes = [], []
for i, r in s.iterrows():
    page = norm(html.unescape(re.sub(r"<[^>]+>", " ", (pages / f"{i}.htm").read_text(encoding="utf-8", errors="ignore"))))
    key = norm(r.first_300_chars)[:80]
    k = page.find(key)
    if k < 0:
        k = page.find(key[:40])
    m = HEAD.match(page[k:k + 80]) if k >= 0 else None
    if k < 0:
        heads.append(""); notes.append("turn not found on the page: open the link")
    elif m:
        heads.append(m.group(0)); notes.append("")
    else:
        before = [h for h in HEAD.finditer(page[:k]) if not CHAIR.match(h.group(0))]
        if before and k - before[-1].end() <= 5:
            heads.append(before[-1].group(0)); notes.append("")
        else:
            heads.append(before[-1].group(0) if before else "")
            notes.append("no heading right before the turn: open the link and check who is speaking")
s["record_heading"], s["check_link"] = heads, notes

cols = ["day", "item", "assigned_member", "party", "state", "record_heading", "check_link", "first_300_chars",
        "correct (y/n)", "source_url"]
widths = {"day": 11, "item": 8, "assigned_member": 22, "party": 6, "state": 6, "record_heading": 26, "check_link": 30,
          "first_300_chars": 80, "correct (y/n)": 12, "source_url": 30}
wb = Workbook(); ws = wb.active; ws.title = "S2 speaker check"
for j, c in enumerate(cols, start=1):
    h = ws.cell(row=1, column=j, value=c); h.font = Font(bold=True); h.fill = PatternFill("solid", fgColor="DDE4EE")
    ws.column_dimensions[h.column_letter].width = widths[c]
yn = DataValidation(type="list", formula1='"y,n"', allow_blank=True); ws.add_data_validation(yn)
for i, row in enumerate(s[cols].itertuples(index=False), start=2):
    for j, (c, v) in enumerate(zip(cols, row), start=1):
        v = None if pd.isna(v) or v == "" else v
        cell = ws.cell(row=i, column=j, value=v)
        cell.alignment = Alignment(wrap_text=c in ("first_300_chars", "check_link"), vertical="top")
        if c == "source_url" and v:
            cell.hyperlink, cell.font = v, Font(color="0563C1", underline="single")
        if c == "correct (y/n)":
            cell.fill = PatternFill("solid", fgColor="FFF4CC"); yn.add(cell.coordinate)
        if c == "check_link" and v:
            cell.fill = PatternFill("solid", fgColor="F8D7DA")
ws.freeze_panes = "A2"
out = HERE / "speaker_check_with_headings.xlsx"
wb.save(out)
print(f"wrote {out}; rows needing the link: {sum(bool(n) for n in notes)} ({[i + 1 for i, n in enumerate(notes) if n]})")
