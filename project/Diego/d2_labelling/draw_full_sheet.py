"""D2: the 100-mention sheet. Run from project/:  python Diego/d2_labelling/draw_full_sheet.py Martin/mentions.parquet

100 floor mentions: 75 cross-party and 25 same-party. Rows 1 to 20 are the 20 of D2_coding_sheet.xlsx, in
the same order and with the same ids. Rows 21 to 100 are 60 more cross-party and 20 more same-party, drawn
at random (seed 2805) from the rest and shuffled.

Who codes what: Diego all 100; Martin rows 1 to 25; Anas rows 76 to 100; Claude rows 26 to 75, from
claude_codes.csv, written without seeing any human code. Every row has two coders. Party is hidden; the
named member's surname is marked ‹like this›.

Writes D2_full_sheet.xlsx (everyone in one sheet, cells nobody fills are grey) and one file per person in
sheets/: D2_Diego.xlsx, D2_Martin.xlsx, D2_Anas.xlsx, D2_Claude.xlsx, each with only that person's rows.
"""
import sys
from pathlib import Path
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

HERE = Path(__file__).parent
sys.argv += [] if len(sys.argv) > 1 else ["Martin/mentions.parquet"]
import draw_labelling_sample as base      # noqa: E402  (reuses the filters, the marker and the code key; does not rewrite the 20-row sheet)

SEED = 2805
BOOK = HERE / "D2_full_sheet.xlsx"
m, members = base.m, base.members
first20 = pd.read_csv(HERE / "sample_key.csv").set_index("mention_row")
rest = m.drop(first20.index)
more = pd.concat([rest[rest.cross].sample(60, random_state=SEED), rest[~rest.cross].sample(20, random_state=SEED)])
more = more.sample(frac=1, random_state=SEED)
S = pd.concat([m.loc[first20.index], more]).reset_index(names="mention_row")
S.insert(0, "id", range(1, len(S) + 1))
assert (S.mention_row[:20].values == first20.index.values).all()
S["speaker_name"], S["named_name"] = members.name[S.speaker].values, members.name[S.named].values
S["context_marked"] = [base.mark(c, b) for c, b in zip(S.context, S.named)]
ROWS = {"Diego": range(1, 101), "Martin": range(1, 26), "Anas": range(76, 101), "Claude": range(26, 76)}
S.drop(columns=["context_marked"]).to_csv(HERE / "full_key.csv", index=False)

if "--draw-only" in sys.argv:
    sys.exit(0)
claude = pd.read_csv(HERE / "claude_codes.csv").set_index("id").code
assert set(claude.index) == set(ROWS["Claude"]), "claude_codes.csv must hold rows 26 to 75"

KEY = base.KEY[:-1] + [base.KEY[-1],
    "Fill only the yellow cells in your own column: Diego all 100, Martin rows 1-25, Anas rows 76-100. The Claude column (rows 26-75) is the AI's coding, checked against Diego's."]
CODERS = ["Diego", "Martin", "Anas", "Claude"]
HEAD, CODE, GREY = (PatternFill("solid", fgColor=c) for c in ("DDE4EE", "FFF4CC", "D9D9D9"))
COLS = [("id", 5), ("speaker", 20), ("named member", 20), ("date", 11), ("context", 95)] + [(c, 9) for c in CODERS] + [("notes", 30)]
wb = Workbook(); ws = wb.active; ws.title = "Labelling"
ws.cell(row=1, column=1, value="D2: what does a floor mention mean? (100 mentions)").font = Font(bold=True, size=14)
for r, text in enumerate(KEY, start=2):
    ws.cell(row=r, column=1, value=text).font = Font(bold=(r == 2 or r == len(KEY) + 1))
top = len(KEY) + 3
for j, (h, w) in enumerate(COLS, start=1):
    c = ws.cell(row=top, column=j, value=h); c.font, c.fill = Font(bold=True), HEAD
    ws.column_dimensions[c.column_letter].width = w
dv = DataValidation(type="list", formula1='"P,A,D,N,X"', allow_blank=True, error="Use P, A, D, N or X", errorTitle="Code")
ws.add_data_validation(dv)
for i, r in enumerate(S.itertuples(), start=top + 1):
    for j, v in enumerate([r.id, r.speaker_name, r.named_name, r.date, r.context_marked], start=1):
        ws.cell(row=i, column=j, value=v).alignment = Alignment(wrap_text=(j == 5), vertical="top")
    for j, who in enumerate(CODERS, start=6):
        c = ws.cell(row=i, column=j)
        if r.id not in ROWS[who]:
            c.fill = GREY
        elif who == "Claude":
            c.value = claude[r.id]
        else:
            c.fill = CODE; dv.add(c.coordinate)
ws.freeze_panes = ws.cell(row=top + 1, column=1)
wb.save(BOOK)
print(f"{len(S)} mentions: {int(S.cross.sum())} cross-party, {int((~S.cross).sum())} same-party; wrote {BOOK}")


# ---------------------------------------------------------------- one file per person
OUT = HERE / "sheets"
OUT.mkdir(exist_ok=True)
PCOLS = [("id", 5), ("speaker", 20), ("named member", 20), ("date", 11), ("context", 95), ("code", 8), ("notes", 40)]
for who, rows in ROWS.items():
    path = OUT / f"D2_{who}.xlsx"
    if path.exists() and who != "Claude":
        print(f"{path.name} exists, not overwritten"); continue
    part = S[S.id.isin(rows)]
    wb = Workbook(); ws = wb.active; ws.title = who
    ws.cell(row=1, column=1, value=f"D2: what does a floor mention mean? {who}, rows {rows.start} to {rows.stop - 1}").font = Font(bold=True, size=14)
    for r, text in enumerate(base.KEY, start=2):
        ws.cell(row=r, column=1, value=text).font = Font(bold=(r == 2))
    top = len(base.KEY) + 3
    for j, (h, w) in enumerate(PCOLS, start=1):
        c = ws.cell(row=top, column=j, value=h); c.font, c.fill = Font(bold=True), HEAD
        ws.column_dimensions[c.column_letter].width = w
    dv = DataValidation(type="list", formula1='"P,A,D,N,X"', allow_blank=True, error="Use P, A, D, N or X", errorTitle="Code")
    ws.add_data_validation(dv)
    for i, r in enumerate(part.itertuples(), start=top + 1):
        for j, v in enumerate([r.id, r.speaker_name, r.named_name, r.date, r.context_marked], start=1):
            ws.cell(row=i, column=j, value=v).alignment = Alignment(wrap_text=(j == 5), vertical="top")
        c = ws.cell(row=i, column=6)
        if who == "Claude":
            c.value = claude[r.id]
            ws.cell(row=i, column=7, value=pd.read_csv(HERE / "claude_codes.csv").set_index("id").note[r.id])
        else:
            c.fill = CODE; dv.add(c.coordinate)
    ws.freeze_panes = ws.cell(row=top + 1, column=1)
    wb.save(path)
    print("wrote", path.name, len(part), "rows")
