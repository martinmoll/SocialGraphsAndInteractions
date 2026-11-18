"""D2: draw the labelling sample from mentions.parquet and write the one-sheet coding file.

Run from project/:
    python Diego/d2_labelling/draw_labelling_sample.py Martin/mentions.parquet

20 floor mentions (15 cross-party, 5 same-party), drawn at random with seed 2805 and shuffled together.
All three of us code all 20, each in our own column (see PROTOCOL.md).

Writes, next to this file:
  sample_key.csv          ids with parties and flags (not for coders)
  D2_coding_sheet.xlsx    one sheet: the code key at the top, then the 20 mentions
Party is not shown. The named member's surname is marked ‹like this› in the context.
"""
import re
import sys
import unicodedata
from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

SEED, N_CROSS, N_SAME = 2805, 15, 5
CODERS = ["Diego", "Martin", "Anas"]
HERE = Path(__file__).parent
src = sys.argv[1] if len(sys.argv) > 1 else "Martin/mentions.parquet"
BOOK = HERE / "D2_coding_sheet.xlsx"
MAIN = __name__ == "__main__"
if MAIN and BOOK.exists():
    sys.exit(f"{BOOK} already exists. Coding may have started, so nothing was overwritten.")

members = pd.read_csv("data/processed/members.csv").set_index("bioguide")
m = pd.read_parquet(src)
m = m[(m.source == "floor") & m.speaker.isin(members.index) & m.named.isin(members.index)].copy()
m["speaker_party"], m["named_party"] = members.party[m.speaker].values, members.party[m.named].values
m = m[m.speaker_party.isin(["R", "D"]) & m.named_party.isin(["R", "D"])]
m["cross"] = m.speaker_party != m.named_party

S = pd.concat([m[m.cross].sample(N_CROSS, random_state=SEED), m[~m.cross].sample(N_SAME, random_state=SEED)])
S = S.sample(frac=1, random_state=SEED).reset_index(names="mention_row")
S.insert(0, "id", range(1, len(S) + 1))
S["speaker_name"], S["named_name"] = members.name[S.speaker].values, members.name[S.named].values


def plain(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def mark(context, bioguide):
    """Put ‹ › around every occurrence of the named member's surname, ignoring case and accents."""
    last, folded = plain(members["last"][bioguide]), plain(context)
    if len(folded) != len(context):          # accents changed the length: fall back to an exact search
        return re.sub(re.escape(members["last"][bioguide]), lambda x: f"‹{x.group(0)}›", context, flags=re.I)
    out, k = [], 0
    for hit in re.finditer(r"\b" + re.escape(last) + r"\b", folded):
        out += [context[k:hit.start()], "‹", context[hit.start():hit.end()], "›"]
        k = hit.end()
    return "".join(out) + context[k:]


S["context_marked"] = [mark(c, b) for c, b in zip(S.context, S.named)]
if MAIN:
    S.drop(columns=["context_marked"]).to_csv(HERE / "sample_key.csv", index=False)

KEY = [
    "What is the speaker doing towards the named member (marked ‹like this›)? Put one letter in your own column.",
    "P  Procedure: handing over or thanking for speaking time.   'I yield 2 minutes to the gentlewoman from New Mexico (Ms. ‹Stansbury›)'",
    "A  Agreeing: thanks, praise, working together, supporting their bill.   'a bipartisan bill I am leading with my good friend (Mr. ‹Peters›)'",
    "D  Disagreeing: arguing with, criticising or blaming them.   'sadly, I cannot agree with Chairman ‹Cole›'",
    "N  Neutral: just mentions them.   'my letter to Speaker Mike ‹Johnson›'",
    "X  Wrong person: not this member, or not said by the speaker.   'Mrs. ‹Peters› now holds classes on raising livestock' (a constituent)",
    "Two codes fit? Take the first in this order: X, P, D, A, N.  Thanking a chairman for bringing a bill is A.  Not sure? Best guess, and write 'unsure' in notes.",
]
HEAD = PatternFill("solid", fgColor="DDE4EE")
CODE = PatternFill("solid", fgColor="FFF4CC")
COLS = [("id", 5), ("speaker", 20), ("named member", 20), ("date", 11), ("context", 95)] + [(c, 9) for c in CODERS] + [("notes", 30)]

def write_book():
    """Write the 20-row sheet. Skipped when draw_full_sheet.py imports this file."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Labelling"
    ws.cell(row=1, column=1, value="D2: what does a floor mention mean?").font = Font(bold=True, size=14)
    for r, text in enumerate(KEY, start=2):
        c = ws.cell(row=r, column=1, value=text)
        c.font = Font(bold=(r == 2))
    top = len(KEY) + 3                                   # header row of the table
    for j, (h, w) in enumerate(COLS, start=1):
        cell = ws.cell(row=top, column=j, value=h)
        cell.font, cell.fill = Font(bold=True), HEAD
        ws.column_dimensions[cell.column_letter].width = w
    for i, r in enumerate(S.itertuples(), start=top + 1):
        for j, v in enumerate([r.id, r.speaker_name, r.named_name, r.date, r.context_marked], start=1):
            ws.cell(row=i, column=j, value=v).alignment = Alignment(wrap_text=(j == 5), vertical="top")
        for j in range(6, 6 + len(CODERS)):
            ws.cell(row=i, column=j).fill = CODE
    dv = DataValidation(type="list", formula1='"P,A,D,N,X"', allow_blank=True, error="Use P, A, D, N or X", errorTitle="Code")
    ws.add_data_validation(dv)
    dv.add(f"F{top + 1}:{ws.cell(row=top + len(S), column=5 + len(CODERS)).coordinate}")
    ws.freeze_panes = ws.cell(row=top + 1, column=1)
    wb.save(BOOK)
    print(f"{len(S)} mentions: {int(S.cross.sum())} cross-party, {int((~S.cross).sum())} same-party; "
          f"surname marked in {sum('‹' in c for c in S.context_marked)} of {len(S)}")
    print("wrote", BOOK)


if MAIN:
    write_book()
