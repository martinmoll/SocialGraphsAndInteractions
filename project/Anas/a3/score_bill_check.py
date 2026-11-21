"""A3.5 check: score the bill-link sample (draw_bill_check.py) from the blind readers' answers.

Run from Anas/:  python a3/score_bill_check.py

Per item, the majority answer of the readers (yes / companion / no / unsure; a tie counts as unsure). Precision of
a link = yes / (yes + companion + no), with a Wilson 95% interval, separately for bill numbers and for titles.
'companion' counts as wrong for the link (it names the same legislation, but not this bill's sponsor and
cosponsors); it is also shown on its own. Decision 7: titles are used only if their precision is at least 0.95.
Prints the items where the readers disagree, or where the majority is not yes: those go to Anas.
"""
import math
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.join(HERE, "bill_check")


def wilson(k, n, z=1.96):
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h


key = pd.read_csv(os.path.join(F, "bill_check_key.csv"))
files = sorted(f for f in os.listdir(os.path.join(F, "raters")) if f.endswith(".csv"))
A = pd.concat([pd.read_csv(os.path.join(F, "raters", f), dtype=str).fillna("").assign(reader=f[:-4]) for f in files])
A["answer"] = A.answer.str.strip().str.lower()
wide = A.pivot_table(index="item_id", columns="reader", values="answer", aggfunc="first")
print(f"readers: {list(wide.columns)}; items answered by all: {int(wide.notna().all(axis=1).sum())} of {len(key)}")


def majority(row):
    v = row.dropna().value_counts()
    return v.index[0] if len(v) and (len(v) == 1 or v.iloc[0] > v.iloc[1]) else "unsure"


wide["majority"] = wide.apply(majority, axis=1)
wide["unanimous"] = wide.drop(columns="majority").nunique(axis=1) == 1
K = key.merge(wide[["majority", "unanimous"]], left_on="item_id", right_index=True, how="left")
for kind in ["number", "title"]:
    g = K[K.kind == kind]
    y, c, n, u = [(g.majority == x).sum() for x in ("yes", "companion", "no", "unsure")]
    lo, hi = wilson(y, y + c + n)
    print(f"{kind}: yes {y}, companion {c}, no {n}, unsure {u} -> precision {y / max(1, y + c + n):.3f} "
          f"(Wilson {lo:.2f}-{hi:.2f}); unanimous {int(g.unanimous.sum())} of {len(g)}")
print(f"decision 7: titles used only if precision >= 0.95")
show = K[(K.majority != "yes") | ~K.unanimous]
notes = A.groupby("item_id").apply(lambda x: " | ".join(f"{r}: {a} {n}".strip() for r, a, n in zip(x.reader, x.answer, x.note)))
print("\nfor Anas (not unanimous, or majority not yes):")
for r in show.itertuples():
    print(f"  {r.item_id} [{r.kind}] {r.bill_id}: majority {r.majority} -- {notes.get(r.item_id, '')}")
K.to_csv(os.path.join(F, "bill_check_scored.csv"), index=False)
