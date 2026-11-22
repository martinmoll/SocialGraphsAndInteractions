"""A3.3 check: score the filled-in precision workbook (precision_check/precision_sheets.xlsx).

Run from Anas/:  python a3/score_precision.py
Per rule (one tab each): y, n, ? counts, precision = y / (y + n) with a Wilson 95% interval, and whether the rule
passes the 95% bar of decision 3 (judged on the point estimate; 30 of 30 still has a lower bound near 0.89).
Tabs with empty `correct` cells are reported as not yet fully read.
"""
import math
import os

import pandas as pd


def wilson(k, n, z=1.96):
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h


import sys

folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "precision_check")
# python a3/score_precision.py switch_sheet.xlsx  scores the 21 Nov switch sample instead (A3_MATCHER_SWITCH.md)
book = sys.argv[1] if len(sys.argv) > 1 else "precision_sheets.xlsx"
sheets = pd.read_excel(os.path.join(folder, book), sheet_name=None, dtype={"correct": str})
# resolutions.csv: Claude's resolution of rows Anas read n or ? where his note says "could not verify" (or, on the
# removal tabs, where y/n was flipped). The workbook's `correct` is never changed; both versions are scored.
res_path = os.path.join(folder, "resolutions.csv")
res = pd.read_csv(res_path).set_index("sample_id") if os.path.exists(res_path) else pd.DataFrame(columns=["resolved"])


def score(label):
    rows = []
    for tab, s in sheets.items():
        if tab == "How to read":
            continue
        c = s.correct.fillna("").str.strip().str.lower()
        if label == "resolved":
            c = s.sample_id.map(res.resolved).fillna(c)
        y, n, q, empty = (c == "y").sum(), (c == "n").sum(), (c == "?").sum(), (c == "").sum()
        lo, hi = wilson(y, y + n)
        rows.append(dict(rule=tab, read=len(s) - empty, of=len(s), y=y, n=n, unsure=q,
                         changed=int(s.sample_id.isin(res.index).sum()) if label == "resolved" else 0,
                         precision=round(y / (y + n), 3) if y + n else None,
                         ci95=f"{lo:.2f}-{hi:.2f}" if y + n else "",
                         passes_95=(y / (y + n) >= 0.95) if y + n and empty == 0 else None))
    return pd.DataFrame(rows)


print("As read by Anas:")
print(score("as read").drop(columns="changed").to_string(index=False))
if len(res):
    print("\nWith resolutions.csv (rows changed by Claude in `changed`):")
    print(score("resolved").to_string(index=False))
