"""Write the untitled and list check sheets as formatted Excel files with a coding guide. Run from project/:
    python Martin/m1_checks_20nov/make_xlsx.py
Reads untitled_sheet.csv and list_sheet.csv; the CSVs stay the source the scorer reads (convert back after coding).
In the list sheet, the one list hit the row is about is marked [[like this]], found by rerunning the matcher on the
context: it is the hit with that member and a "list: " rule (the first one if the same member is listed twice).
"""
import sys
from pathlib import Path
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
sys.path.insert(0, "Martin")
from matcher import Matcher

HERE = Path(__file__).parent
mt = Matcher(pd.read_csv("data/processed/members.csv"))
YELLOW, TOP = PatternFill("solid", fgColor="FFF7CC"), Alignment(wrap_text=True, vertical="top")

def mark_list_hit(context, named):
    hits = [h for h in mt.find(context) if h.named == named and h.how.startswith("list: ")]
    if not hits:
        return context, False
    h = hits[0]
    return context[:h.start] + "[[" + context[h.start:h.end] + "]]" + context[h.end:], True

def build(df, widths, codes, guide, out):
    wb = Workbook(); ws = wb.active; ws.title = "sheet1"
    cols = list(df.columns); ws.append(cols)
    for row in df.itertuples(index=False): ws.append(list(row))
    for i, c in enumerate(cols, 1): ws.column_dimensions[get_column_letter(i)].width = widths.get(c, 12)
    for cell in ws[1]: cell.font = Font(bold=True)
    for k, row in enumerate(ws.iter_rows(min_row=2), start=2):
        for cell in row:
            cell.alignment = TOP; cell.font = Font(size=10)
            if cols[cell.column - 1] in ("code", "note"): cell.fill = YELLOW
        n = len(str(df.context.iloc[k - 2]))
        ws.row_dimensions[k].height = min(409, max(30, (n // int(widths["context"] * 1.15) + 2) * 13.5))
    col = get_column_letter(cols.index("code") + 1)
    dv = DataValidation(type="list", formula1='"' + ",".join(codes) + '"', allow_blank=True)
    ws.add_data_validation(dv); dv.add(f"{col}2:{col}{len(df) + 1}")
    ws.freeze_panes = "A2"
    g = wb.create_sheet("how to code")
    for line in guide: g.append([line])
    g.column_dimensions["A"].width = 120
    for r in g.iter_rows():
        for c in r: c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(out)

U = pd.read_csv(HERE / "untitled_sheet.csv", keep_default_na=False)
build(U, {"id": 5, "speaker_name": 18, "named_name": 20, "context": 110, "code": 7, "note": 30}, ["M", "P", "X"], [
    "UNTITLED FULL NAMES: is the marked full name a mention of that House member?",
    "Each row: a member's first and last name written WITHOUT a title ('my friend Chip Roy'), marked [[like this]].",
    "named_name is the member the rule would count. Pick a code from the drop-down:",
    "",
    "M  = a mention of that House member: the speaker talks about them or to them ('my colleague and friend, [[Chip Roy]]').",
    "P  = it is that member, but procedure, not a choice to name them: tellers, appointments, a list read by the Clerk,",
    "     conferees, a roll call ('the Chair appoints [[Bryan Steil]] and Joseph Morelle as tellers').",
    "X  = not that member: someone else with the same name (a constituent, a former member, a president), a bill or",
    "     building named after someone, or a quote of a name that is not this member.",
    "",
    "Unsure? Pick the closest code and write why in note. Do not open untitled_key.csv until you are done.",
    "",
    "RULE SET IN ADVANCE (G14, agreed 21 Nov): if 24 or more of the 30 are M, untitled names go into the floor data too.",
    "If fewer, they stay press-only and Methods says the floor counts titled names only.",
    "",
    "WHY IT MATTERS: the floor matcher only finds names after a title ('Mr. Roy'). There are about 930 untitled full",
    "names on the floor. If most are real mentions, the floor map misses them and the press side (which counts them)",
    "would follow a different rule; if many are procedure or other people, adding them would add wrong ties. 30 rows",
    "decide which, before the numbers freeze.",
], HERE / "untitled_sheet.xlsx")

L = pd.read_csv(HERE / "list_sheet.csv", keep_default_na=False)
marked = [mark_list_hit(c, b) for c, b in zip(L.context, pd.read_parquet("Martin/mentions.parquet").loc[L.mention_row].named)]
L["context"] = [m[0] for m in marked]
print(f"list sheet: {sum(m[1] for m in marked)} of {len(L)} rows marked")
build(L, {"id": 5, "mention_row": 8, "speaker_name": 18, "named_name": 20, "context": 110, "code": 7, "note": 30}, ["OK", "X"], [
    "LIST HITS: did the matcher pick the right member out of a list?",
    "Each row: a member found in a list after a plural title ('I thank Representatives Lawler, Golden, and Fitzpatrick').",
    "The name the row is about is marked [[like this]]; named_name is the member the matcher chose. Pick a code:",
    "",
    "OK = named_name is the member the speaker names at the marked place.",
    "X  = it is not: a different person, a non-member, or the marked word is not a name at all. Say what it is in note.",
    "",
    "Only judge WHO it is. Whether thanking a list is a 'real' mention is not the question here (lists count, G14).",
    "",
    "WHY IT MATTERS: list hits are 511 of the 9,058 floor mentions (about 6%), added on 20 Nov (G14). Diego's precision",
    "check (98 of 100) was measured before they existed, so these 20 rows are the only human check on them. If several",
    "are wrong, the list rule has to change before the freeze; if they are right, Methods can say so.",
], HERE / "list_sheet.xlsx")
print("written untitled_sheet.xlsx and list_sheet.xlsx")
