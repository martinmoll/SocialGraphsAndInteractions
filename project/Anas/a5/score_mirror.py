"""A5 mirror check: score the three blind readers. Run from Anas/ after the readers' CSVs are in a5/mirror/readers/:
    python -I a5/score_mirror.py
Majority code per item (2 of 3 or 3 of 3). Items where any reader differs are listed in a5/mirror/disagreements_auto.md;
the readable version for Anas, with excerpts, links and tick boxes, is a5/mirror/DIFFERENCES.md (written by hand,
never overwritten by this script). Anas's codes go in a5/mirror/anas_codes.csv (item,code) and replace the majority
for every item listed there. Writes a5/mirror/scored.csv and prints the code shares with Wilson 95% intervals, and the
decision rule fixed in a5/PLAN.md (addendum of 23 Nov): P >= 27 of 30.
"""
import glob
import os
from math import sqrt

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
MIRROR = os.path.join(HERE, "mirror")
CODES = ["P", "C", "M", "N"]
P_MIN = 27


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


files = sorted(glob.glob(os.path.join(MIRROR, "readers", "reader*.csv")))
R = {os.path.basename(f)[:-4]: pd.read_csv(f, dtype=str).set_index("item") for f in files}
draw = pd.read_csv(os.path.join(MIRROR, "draw.csv")).set_index("item")
items = list(draw.index)
for k, r in R.items():
    assert list(r.index) == items, f"{k}: items differ from the draw"
    assert r.code.str.strip().isin(CODES).all(), f"{k}: unknown code {set(r.code) - set(CODES)}"
codes = pd.DataFrame({k: r.code.str.strip() for k, r in R.items()})
maj = codes.apply(lambda row: row.value_counts().idxmax() if row.value_counts().max() >= 2 else None, axis=1)
unanimous = codes.nunique(axis=1) == 1
out = codes.assign(majority=maj, unanimous=unanimous)
anas_path = os.path.join(MIRROR, "anas_codes.csv")
if os.path.exists(anas_path):
    A = pd.read_csv(anas_path, dtype=str).set_index("item").code.str.strip()
    assert A.isin(CODES).all(), f"anas_codes: unknown code {set(A) - set(CODES)}"
    out["anas"] = A.reindex(out.index)
    out["final"] = out.anas.fillna(out.majority)
else:
    out["final"] = out.majority
out.to_csv(os.path.join(MIRROR, "scored.csv"))

print(f"readers: {list(R)}; items: {len(items)}; unanimous: {int(unanimous.sum())}; "
      f"no majority: {int(maj.isna().sum())}")
cols = list(codes.columns)
for i, a in enumerate(cols):
    for b in cols[i + 1:]:
        print(f"  agreement {a}-{b}: {(codes[a] == codes[b]).mean():.0%}")
f = out.final.dropna()
src = "Anas where read, else majority" if "anas" in out else "majority"
print(f"\nfinal codes ({src}), n = {len(f)}{'' if len(f) == len(items) else ' (items without a final code left out)'}:")
for c in CODES:
    k = int((f == c).sum())
    lo, hi = wilson(k, len(f))
    print(f"  {c}: {k:2d} ({k / len(f):.0%}, 95% {lo:.0%} to {hi:.0%})")
kp = int((f == "P").sum())
print(f"\ndecision rule (P >= {P_MIN} of 30): P = {kp} of {len(f)} -> "
      + ("named and either figures stand, with the P share as their check" if kp >= P_MIN and len(f) == len(items)
         else "not met (or not all items final): lead with on-record, give named with its P share"))

diff = out[~out.unanimous]
lines = ["# A5 mirror check: items where the readers differ", "",
         f"{len(diff)} of {len(items)} items. Same item ids as `mirror/packet/items.txt`; codes as in "
         "`mirror/packet/reader_instructions.md`.", ""]
for item, row in diff.iterrows():
    lines.append(f"## {item}: {draw.at[item, 'member']} ({draw.at[item, 'member_party']}), {draw.at[item, 'date']}")
    lines.append(f"Title: {draw.at[item, 'title']}  ")
    for k, r in R.items():
        lines.append(f"- {k}: **{r.at[item, 'code']}** ({r.at[item, 'member']}) {r.at[item, 'reason']}")
    lines.append("")
open(os.path.join(MIRROR, "disagreements_auto.md"), "w").write("\n".join(lines))
print(f"\n{len(diff)} items with any disagreement -> mirror/disagreements_auto.md")
