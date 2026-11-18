"""D2 / S1: agreement between coders, and the labels the classifier (D5) trains on.

Run from project/ when the sheets are back:
    python Diego/d2_labelling/agreement.py [folder]          default: Diego/d2_labelling/sheets
The folder (and its subfolders) holds one .xlsx per coder, found by the coder's name in the file name, so
Google Sheets downloads such as "D2_Martin (1).xlsx" work:
    humans  Diego (all 100), Martin (rows 1-25), Anas (rows 76-100)
    AI      Claude (rows 26-75), AI1, AI2, AI3 (all 100; in ai/)
Every pair is compared on the rows both coded. The single 20-row sheet D2_coding_sheet.xlsx can also be
given as the argument.

Codes: P procedure, A agreeing, D disagreeing, N neutral, X wrong person (see PROTOCOL.md).
"""
import sys
from itertools import combinations
from math import sqrt
from pathlib import Path
import pandas as pd

HERE = Path(__file__).parent
CODES = list("PADNX")
HUMANS, AIS = ["Diego", "Martin", "Anas"], ["Claude", "AI1", "AI2", "AI3"]
src = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "sheets"


def table(path):
    raw = pd.read_excel(path, header=None, dtype=str).fillna("")
    top = raw.index[raw[0] == "id"][0]                  # the table starts under the code key
    T = raw.iloc[top + 1:].set_axis(raw.iloc[top], axis=1)
    return T[T["id"] != ""].assign(id=lambda d: d["id"].astype(float).astype(int)).set_index("id")


if src.is_dir():
    key = pd.read_csv(HERE / "full_key.csv").set_index("id")
    T = pd.DataFrame(index=key.index)
    for who in HUMANS + AIS:
        files = [f for f in src.rglob("*.xlsx") if who.lower() in f.name.lower() and not f.name.startswith("~$")]
        if len(files) > 1: raise SystemExit(f"more than one file for {who}: {[f.name for f in files]}")
        if files: T[who] = table(files[0])["code"]
    T = T.fillna("")
else:
    key = pd.read_csv(HERE / ("sample_key.csv" if src.name == "D2_coding_sheet.xlsx" else "full_key.csv")).set_index("id")
    T = table(src)
coders = [c for c in HUMANS + AIS if c in T.columns and (T[c].astype(str).str.strip() != "").any()]
C = T[coders].apply(lambda s: s.astype(str).str.strip().str.upper()).join(key[["cross"]])
bad = C[coders].stack(); bad = bad[~bad.isin(CODES + [""])]
if len(bad): raise SystemExit(f"unknown codes: {bad.to_dict()}")
humans, ais = [c for c in coders if c in HUMANS], [c for c in coders if c in AIS]
print("rows coded:", {c: int((C[c] != "").sum()) for c in coders})


def kappa(a, b):
    po = (a == b).mean()
    pe = sum((a == c).mean() * (b == c).mean() for c in CODES)
    return po, (po - pe) / (1 - pe) if pe < 1 else float("nan")


def compare(x, y, cy=None):
    a, b = C[x], (C[y] if cy is None else cy)
    ok = (a != "") & (b != "")
    if ok.sum() == 0: return
    po, k = kappa(a[ok], b[ok])
    print(f"  {x:>11s} vs {y:<11s} n = {ok.sum():3d}  raw agreement {po:4.0%}  Cohen's kappa {k:5.2f}")


print("\n(a) human against human")
for x, y in combinations(humans, 2): compare(x, y)
if "Diego" in coders:
    print("\n(b) each AI coder against Diego")
    for a in ais: compare("Diego", a)
print("\n(c) AI against AI")
for x, y in combinations(ais, 2): compare(x, y)
multi = [a for a in ("AI1", "AI2", "AI3") if a in ais]
if len(multi) == 3 and "Diego" in coders:
    maj = C[multi].apply(lambda r: r.mode().iloc[0] if r.value_counts().iloc[0] >= 2 else "", axis=1)
    print(f"\n(d) majority of AI1-AI3 against Diego (no majority on {int((maj == '').sum())} rows, left out)")
    compare("Diego", "AI majority", cy=maj)
if ais:
    print("\nNote: Claude and AI1-AI3 are the same model, given the same rules and the same rows, each without seeing\n"
          "the others. Their agreement with each other overstates how independent they are: shared mistakes agree.")


def wilson(k, n, z=1.96):
    p = k / n; c = p + z * z / (2 * n); h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)); d = 1 + z * z / n
    return (c - h) / d, (c + h) / d


first = "Diego" if "Diego" in coders else coders[0]
print(f"\nshares from {first}'s codes, with 95% Wilson intervals")
for name, g in C[C[first] != ""].groupby("cross"):
    n = len(g)
    parts = []
    for c in CODES:
        k = int((g[first] == c).sum()); lo, hi = wilson(k, n)
        parts.append(f"{c} {k / n:.0%} ({lo:.0%}-{hi:.0%})")
    print(f"  {'cross-party' if name else 'same-party '} (n = {n}): " + ", ".join(parts))

# ---------------------------------------------------------------- training labels for D5
if "Diego" not in coders:
    raise SystemExit("\nDiego's sheet is not filled in yet: no training labels written.")
L = key[["mention_row", "cross"]].join(C[coders].rename(columns=str.lower))
second_order = [c for c in ("Martin", "Anas", "Claude") if c in coders]
L["second_coder"] = [next((c for c in second_order if C.at[i, c] != ""), "") for i in L.index]
L["second"] = [C.at[i, w] if w else "" for i, w in zip(L.index, L.second_coder)]
L["label"] = L[first.lower()].where(L[first.lower()] != "", L.second)
L.to_csv(HERE / "labels_final.csv")
C[(C[first] != "") & (L.second != "") & (C[first] != L.second)].to_csv(HERE / "disagreements.csv")
print(f"\nlabels_final.csv: {int((L.label != '').sum())} labelled rows for the classifier (label = {first}'s code); "
      "rows where Diego and the second coder differ are in disagreements.csv")
