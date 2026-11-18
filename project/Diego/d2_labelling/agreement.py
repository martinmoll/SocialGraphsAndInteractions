"""D2 / S1: agreement between coders and the distribution of codes.

Run from project/ when the sheet is filled in:
    python Diego/d2_labelling/agreement.py [path/to/D2_full_sheet.xlsx, or a folder of D2_<name>.xlsx files]
If it was filled in Google Sheets, download it as .xlsx first (File > Download > Microsoft Excel).
Works on either sheet: every pair of coders is compared on the rows both have coded.
Codes: P procedure, A agreeing, D disagreeing, N neutral, X wrong person (see PROTOCOL.md).
"""
import sys
from itertools import combinations
from pathlib import Path
import pandas as pd

HERE = Path(__file__).parent
CODES = list("PADNX")
book = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "D2_full_sheet.xlsx"
key = pd.read_csv(HERE / ("sample_key.csv" if book.name == "D2_coding_sheet.xlsx" else "full_key.csv")).set_index("id")
def table(path):
    raw = pd.read_excel(path, header=None, dtype=str).fillna("")
    top = raw.index[raw[0] == "id"][0]                  # the table starts under the code key
    T = raw.iloc[top + 1:].set_axis(raw.iloc[top], axis=1)
    return T[T["id"] != ""].assign(id=lambda d: d["id"].astype(float).astype(int)).set_index("id")


if book.is_dir():                                       # one file per person: D2_Diego.xlsx, D2_Martin.xlsx, ...
    key = pd.read_csv(HERE / "full_key.csv").set_index("id")
    T = pd.DataFrame(index=key.index)
    for f in sorted(book.glob("D2_*.xlsx")):
        T[f.stem[3:]] = table(f)["code"]
    T = T.fillna("")
else:
    T = table(book)
coders = [c for c in ("Diego", "Martin", "Anas", "Claude") if c in T.columns]
C = T[coders].apply(lambda s: s.str.strip().str.upper()).join(key[["cross"]])
bad = C[coders].stack(); bad = bad[~bad.isin(CODES + [""])]
if len(bad): raise SystemExit(f"unknown codes: {bad.to_dict()}")
print("rows coded:", {c: int((C[c] != "").sum()) for c in coders})


def kappa(a, b):
    po = (a == b).mean()
    pe = sum((a == c).mean() * (b == c).mean() for c in CODES)
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")


for x, y in combinations(coders, 2):
    both = C[(C[x] != "") & (C[y] != "")]
    if len(both):
        po, k = kappa(both[x], both[y])
        print(f"{x} and {y}: n = {len(both)}, raw agreement {po:.0%}, Cohen's kappa {k:.2f}")

# one code per row: Diego's where the second coder agrees; disagreements listed for the group to settle
second = C[[c for c in coders if c != "Diego"]].replace("", pd.NA).bfill(axis=1).iloc[:, 0].fillna("")
C["second"] = second
C["final"] = [d if d == s or s == "" else "?" for d, s in zip(C.get("Diego", second), second)]
print("\nfinal codes (? = the two coders differ), by type of mention:")
print(pd.crosstab(C.cross.map({True: "cross-party", False: "same-party"}), C.final, margins=True).to_string())
C[C.final == "?"].to_csv(HERE / "disagreements.csv")
print("\nrows where coders differ are in disagreements.csv")
