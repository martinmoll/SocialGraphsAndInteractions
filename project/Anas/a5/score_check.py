"""A5 reading check: score the three blind readers. Run from Anas/ after the readers' CSVs are in a5/check/readers/:
    python a5/score_check.py
Majority code per item (2 of 3 or 3 of 3); items with no majority, or where any reader differs, are listed in
a5/check/disagreements_auto.md; the readable version for Anas, with excerpts and tick boxes, is a5/check/DIFFERENCES.md
(written by hand, never overwritten by this script). Anas's final codes, once read, go in a5/check/anas_codes.csv
(item,code); the script then uses them for every item listed there.
Writes a5/check/scored.csv and prints the code shares, with Wilson 95% intervals.
"""
import glob
import os
from math import sqrt

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "check")
CODES = ["H", "S", "O", "V", "X"]


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


files = sorted(glob.glob(os.path.join(CHECK, "readers", "reader*.csv")))
R = {os.path.basename(f)[:-4]: pd.read_csv(f, dtype=str).set_index("item") for f in files}
draw = pd.read_csv(os.path.join(CHECK, "draw.csv")).set_index("item")
items = list(draw.index)
for k, r in R.items():
    assert list(r.index) == items, f"{k}: items differ from the draw"
    assert r.code.str.strip().isin(CODES).all(), f"{k}: unknown code {set(r.code) - set(CODES)}"
codes = pd.DataFrame({k: r.code.str.strip() for k, r in R.items()})
maj = codes.apply(lambda row: row.value_counts().idxmax() if row.value_counts().max() >= 2 else None, axis=1)
unanimous = codes.nunique(axis=1) == 1
out = codes.assign(majority=maj, unanimous=unanimous)
anas_path = os.path.join(CHECK, "anas_codes.csv")
if os.path.exists(anas_path):
    A = pd.read_csv(anas_path, dtype=str).set_index("item").code.str.strip()
    out["anas"] = A.reindex(out.index)
    out["final"] = out.anas.fillna(out.majority)
else:
    out["final"] = out.majority
out.to_csv(os.path.join(CHECK, "scored.csv"))

print(f"readers: {list(R)}; items: {len(items)}; unanimous: {int(unanimous.sum())}; "
      f"no majority: {int(maj.isna().sum())}")
pairs = [(a, b) for i, a in enumerate(codes.columns) for b in codes.columns[i + 1:]]
for a, b in pairs:
    print(f"  agreement {a}-{b}: {(codes[a] == codes[b]).mean():.0%}")
f = out.final.dropna()
print(f"\nfinal codes ({'Anas where read, else majority' if 'anas' in out else 'majority'}), n = {len(f)}:")
for c in CODES:
    k = int((f == c).sum())
    lo, hi = wilson(k, len(f))
    print(f"  {c}: {k:2d} ({k / len(f):.0%}, 95% {lo:.0%} to {hi:.0%})")
inst = int(f.isin(["H", "S"]).sum())
print(f"partner missed by the instrument (H or S): {inst} of {len(f)}; no partner at all (V or X): "
      f"{int(f.isin(['V', 'X']).sum())}")

diff = out[~out.unanimous]
lines = ["# A5 reading check: items where the readers differ", "",
         f"{len(diff)} of {len(items)} items. Read the release (`check/packet/items.txt`, same item id) and give your code",
         "in `check/anas_codes.csv` (columns item,code). Codes as in `check/packet/reader_instructions.md`.", ""]
for item, row in diff.iterrows():
    lines.append(f"## {item}: {draw.at[item, 'member']} ({draw.at[item, 'member_party']}), {draw.at[item, 'date']}")
    lines.append(f"Title: {draw.at[item, 'title']}  ")
    for k, r in R.items():
        pn = r.at[item, "partner_named"] if isinstance(r.at[item, "partner_named"], str) else ""
        lines.append(f"- {k}: **{r.at[item, 'code']}** {('(' + pn + ') ') if pn else ''}{r.at[item, 'reason']}")
    lines.append("")
open(os.path.join(CHECK, "disagreements_auto.md"), "w").write("\n".join(lines))
print(f"\n{len(diff)} items with any disagreement -> check/disagreements_auto.md (the readable version for Anas is check/DIFFERENCES.md)")
