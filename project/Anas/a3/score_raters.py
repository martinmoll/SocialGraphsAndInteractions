"""A3.3 check: compare blind second readers of the precision workbook with Anas's reading.

Run from Anas/ after the raters' labels are in precision_check/raters/rater{1,2,3}.csv (sample_id, correct, note):
    python a3/score_raters.py

The raters are LLM sub-agents given only a blank copy of precision_sheets.xlsx (`correct` and `note` emptied), its
"How to read" tab and a list of House members; no other file, no web, no matcher output. Printed:
1. precision per rule for each rater, for the majority of the three (2 of 3 agreeing; otherwise "?"), for Anas as
   read, and for Anas with resolutions.csv;
2. agreement: Fleiss' kappa of the three raters and raw percent agreement (kappa is low when nearly every label is
   y, the "kappa paradox", so both are shown), and each rater's agreement with the majority and with Anas;
3. every row where the majority is not y, or where the majority and Anas (resolved) differ.
State-legislator row 23 is left out of the guard's score after the 20 Nov guard fix (it is no longer a guard hit).
"""
import math
import os
from collections import Counter

import pandas as pd


def wilson(k, n, z=1.96):  # same as score_precision.py (importing it would run its report)
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h


HERE = os.path.dirname(os.path.abspath(__file__))
PC = os.path.join(HERE, "precision_check")
OUT_OF_POOL = {"state_legislator_23"}  # no longer removed by the guard after the 20 Nov fix

sheets = pd.read_excel(os.path.join(PC, "precision_sheets.xlsx"), sheet_name=None, dtype={"correct": str})
rows = pd.concat([s.assign(tab=t) for t, s in sheets.items() if t != "How to read"])
rows = rows.set_index("sample_id")
labels = pd.DataFrame(index=rows.index)
labels["tab"] = rows.tab
labels["anas"] = rows.correct.fillna("").str.strip().str.lower()
res = pd.read_csv(os.path.join(PC, "resolutions.csv")).set_index("sample_id")
labels["anas_resolved"] = pd.Series(labels.index.map(res.resolved), index=labels.index).fillna(labels.anas)
raters = []
for i in (1, 2, 3):
    p = os.path.join(PC, "raters", f"rater{i}.csv")
    r = pd.read_csv(p, dtype=str).set_index("sample_id")
    assert set(r.index) == set(labels.index), f"rater{i}: sample ids differ from the workbook"
    labels[f"rater{i}"] = r.correct.str.strip().str.lower()
    labels[f"rater{i}_note"] = r.note
    raters.append(f"rater{i}")
assert labels[raters].isin(["y", "n", "?"]).all().all(), "labels must be y, n or ?"


def majority(r):
    v, k = Counter(r[raters]).most_common(1)[0]
    return v if k >= 2 else "?"


labels["majority"] = labels.apply(majority, axis=1)


def prec(col):
    out = []
    for tab, g in labels.drop(index=list(OUT_OF_POOL)).groupby("tab", sort=False):
        c = g[col]
        y, n, q = (c == "y").sum(), (c == "n").sum(), (c == "?").sum()
        lo, hi = wilson(y, y + n)
        out.append((tab, f"{y}/{y + n}" + (f" ({q}?)" if q else ""), f"{y / (y + n):.2f} ({lo:.2f}-{hi:.2f})" if y + n else ""))
    return out


cols = raters + ["majority", "anas", "anas_resolved"]
table = pd.DataFrame({c: {tab: f"{frac}  {p}" for tab, frac, p in prec(c)} for c in cols})
print("1. Precision per rule (y / (y+n), Wilson 95%); state legislator scored on 29 rows after the guard fix\n")
print(table.to_string())


def fleiss(df):
    cats = ["y", "n", "?"]
    n = df.shape[1]
    counts = pd.DataFrame({c: (df == c).sum(axis=1) for c in cats})
    p_i = ((counts ** 2).sum(axis=1) - n) / (n * (n - 1))
    p_j = counts.sum() / (len(df) * n)
    pe = (p_j ** 2).sum()
    return (p_i.mean() - pe) / (1 - pe) if pe < 1 else float("nan")


all3 = (labels[raters].nunique(axis=1) == 1).mean()
print(f"\n2. Agreement over all {len(labels)} rows")
print(f"   three raters identical: {all3:.1%}; Fleiss' kappa {fleiss(labels[raters]):.2f}")
for c in raters + ["anas", "anas_resolved"]:
    print(f"   {c:14s} agrees with majority on {(labels[c] == labels.majority).mean():.1%}"
          f", with Anas (resolved) on {(labels[c] == labels.anas_resolved).mean():.1%}")
for tab, g in labels.groupby("tab", sort=False):
    print(f"   {tab:20s} three identical {(g[raters].nunique(axis=1) == 1).mean():.0%}, "
          f"majority = Anas (resolved) {(g.majority == g.anas_resolved).mean():.0%}")

flag = labels[(labels.majority != "y") | (labels.majority != labels.anas_resolved)]
print(f"\n3. Rows where the majority is not y or differs from Anas (resolved): {len(flag)}")
for sid, r in flag.iterrows():
    print(f"   {sid}: raters {r.rater1}/{r.rater2}/{r.rater3} -> {r.majority}; Anas {r.anas or '-'}"
          f" (resolved {r.anas_resolved})")
    for c in raters:
        if r[c] != "y" and isinstance(r[f'{c}_note'], str):
            print(f"      {c}: {r[f'{c}_note'][:160]}")
labels.drop(columns=[f"{c}_note" for c in raters]).to_csv(os.path.join(PC, "raters", "all_labels.csv"))
