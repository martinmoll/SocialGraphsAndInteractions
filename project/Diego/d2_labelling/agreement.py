"""D2 / S1: agreement between the three coders and the distribution of codes.

Run from project/ when the sheet is filled in:
    python Diego/d2_labelling/agreement.py [path/to/D2_coding_sheet.xlsx]
If it was filled in Google Sheets, download it as .xlsx first (File > Download > Microsoft Excel).
Codes: P procedure, A agreeing, D disagreeing, N neutral, X wrong person (see PROTOCOL.md).
"""
import sys
from itertools import combinations
from pathlib import Path
import pandas as pd

HERE = Path(__file__).parent
CODES, CODERS = list("PADNX"), ["Diego", "Martin", "Anas"]
book = sys.argv[1] if len(sys.argv) > 1 else HERE / "D2_coding_sheet.xlsx"
key = pd.read_csv(HERE / "sample_key.csv").set_index("id")
raw = pd.read_excel(book, header=None, dtype=str).fillna("")
top = raw.index[raw[0] == "id"][0]                      # the table starts under the code key
T = raw.iloc[top + 1:].set_axis(raw.iloc[top], axis=1)
T = T[T["id"] != ""].assign(id=lambda d: d["id"].astype(float).astype(int)).set_index("id")
C = T[CODERS].apply(lambda s: s.str.strip().str.upper()).join(key[["cross"]])
bad = C[~C[CODERS].isin(CODES).all(axis=1)]
if len(bad): raise SystemExit(f"{len(bad)} rows are uncoded or carry an unknown code: {list(bad.index)}")


def kappa(a, b):
    po = (a == b).mean()
    pe = sum((a == c).mean() * (b == c).mean() for c in CODES)
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")


for x, y in combinations(CODERS, 2):
    po, k = kappa(C[x], C[y])
    print(f"{x} and {y}: raw agreement {po:.0%}, Cohen's kappa {k:.2f}")
P = pd.DataFrame({c: (C[CODERS] == c).sum(axis=1) for c in CODES})       # Fleiss' kappa over the three coders
p_i = ((P * (P - 1)).sum(axis=1) / (3 * 2)).mean()
p_e = ((P.sum() / P.values.sum()) ** 2).sum()
print(f"all three (Fleiss' kappa): {(p_i - p_e) / (1 - p_e):.2f}; all three agree on {(P.max(axis=1) == 3).sum()} of {len(C)}")
C["majority"] = [r.mode().iloc[0] if r.value_counts().iloc[0] >= 2 else "?" for _, r in C[CODERS].iterrows()]
print("\nmajority code (? = all three differ), by type of mention:")
print(pd.crosstab(C.cross.map({True: "cross-party", False: "same-party"}), C.majority).to_string())
C[C[CODERS].nunique(axis=1) > 1].to_csv(HERE / "disagreements.csv")
print("\nrows where coders differ are in disagreements.csv")
