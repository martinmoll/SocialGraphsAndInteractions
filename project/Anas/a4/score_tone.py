"""Check T: score the three blind readers (design: a4/CHECKS_PLAN_23NOV.md). Run from Anas/:
    python -I a4/score_tone.py
Majority code per item; Anas's codes (a4/check_tone/anas_codes.csv, item,code) replace it where given. Items where
any reader differs: a4/check_tone/disagreements_auto.md (the readable version for Anas, DIFFERENCES.md, is written
by hand and never overwritten). Prints code shares per cell (party x seat) and exposed vs safe within each party,
with Wilson 95% intervals; the C-share difference exposed - safe with a permutation p (seat shuffled among each
party's 30 items, 10,000 times, seed 2805); and the reading rule fixed in the plan. Writes a4/check_tone/scored.csv.
"""
import glob
import os
from math import sqrt

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TONE = os.path.join(HERE, "check_tone")
CODES = ["P", "C", "M", "N"]


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def fmt(k, n):
    lo, hi = wilson(k, n)
    return f"{k:2d}/{n} ({k / n:4.0%}, {lo:.0%}-{hi:.0%})"


files = sorted(glob.glob(os.path.join(TONE, "readers", "reader*.csv")))
R = {os.path.basename(f)[:-4]: pd.read_csv(f, dtype=str).set_index("item") for f in files}
draw = pd.read_csv(os.path.join(TONE, "draw.csv")).set_index("item")
items = list(draw.index)
for k, r in R.items():
    assert list(r.index) == items, f"{k}: items differ from the draw"
    assert r.code.str.strip().isin(CODES).all(), f"{k}: unknown code {set(r.code) - set(CODES)}"
codes = pd.DataFrame({k: r.code.str.strip() for k, r in R.items()})
maj = codes.apply(lambda row: row.value_counts().idxmax() if row.value_counts().max() >= 2 else None, axis=1)
out = codes.assign(majority=maj, unanimous=codes.nunique(axis=1) == 1)
ap = os.path.join(TONE, "anas_codes.csv")
if os.path.exists(ap):
    A = pd.read_csv(ap, dtype=str).set_index("item").code.str.strip()
    assert A.isin(CODES).all()
    out["anas"] = A.reindex(out.index)
    out["final"] = out.anas.fillna(out.majority)
else:
    out["final"] = out.majority
out = out.join(draw[["party", "exposed"]])
out.to_csv(os.path.join(TONE, "scored.csv"))

print(f"readers {list(R)}; unanimous {int(out.unanimous.sum())} of {len(out)}; no majority {int(maj.isna().sum())}")
cols = list(codes.columns)
for i, a in enumerate(cols):
    for b in cols[i + 1:]:
        print(f"  agreement {a}-{b}: {(codes[a] == codes[b]).mean():.0%}")
f = out.dropna(subset=["final"])
print(f"\nfinal codes ({'Anas where read, else majority' if 'anas' in out else 'majority'}), n = {len(f)}")
print(f"{'cell':22s}" + "".join(f"{c:>24s}" for c in CODES))
for (p, e), g in f.groupby(["party", "exposed"]):
    print(f"{p + (' exposed' if e else ' safe'):22s}" + "".join(f"{fmt(int((g.final == c).sum()), len(g)):>24s}" for c in CODES))
for e, g in f.groupby("exposed"):
    print(f"{'all ' + ('exposed' if e else 'safe'):22s}" + "".join(f"{fmt(int((g.final == c).sum()), len(g)):>24s}" for c in CODES))
print(f"{'all 60':22s}" + "".join(f"{fmt(int((f.final == c).sum()), len(f)):>24s}" for c in CODES))

print("\nC share, exposed - safe, permutation p (seat shuffled within party, 10,000, seed 2805):")
rng = np.random.default_rng(2805)
for p in ("R", "D"):
    g = f[f.party == p]
    c, e = (g.final == "C").values, g.exposed.values.astype(bool)
    obs = c[e].mean() - c[~e].mean()
    null = np.array([(lambda ee: c[ee].mean() - c[~ee].mean())(rng.permutation(e)) for _ in range(10_000)])
    print(f"  {p}: {obs * 100:+.1f} points, p {float((np.abs(null) >= abs(obs) - 1e-12).mean()):.3f}")

cell_c = f.groupby(["party", "exposed"]).final.apply(lambda s: (s == "C").mean())
diff = {p: cell_c[(p, True)] - cell_c[(p, False)] for p in ("R", "D")}
if (cell_c <= 0.25).all():
    rule = "C is 25% or less in every cell: counted names are mostly partnership or neutral; 'name' stands"
elif max(diff.values()) >= 0.20:
    rule = "C clearly higher in exposed seats (>= 20 points): part of the exposed gap is attack"
else:
    rule = "C over 25% in some cell, no clear exposed-safe difference: 'name, often to criticise'"
print(f"\nreading rule (fixed in the plan): {rule}")

diff_items = out[~out.unanimous]
lines = ["# Check T: items where the readers differ", "",
         f"{len(diff_items)} of {len(items)}. Same ids as `check_tone/packet/items.txt`.", ""]
for item, row in diff_items.iterrows():
    d = draw.loc[item]
    lines.append(f"## {item}: {d.member_name} ({d.party}) names {d.named_name} ({d.named_party}), {d.date}")
    lines.append(f"Title: {d.title}  ")
    for k, r in R.items():
        lines.append(f"- {k}: **{r.at[item, 'code']}** {r.at[item, 'reason']}")
    lines.append("")
open(os.path.join(TONE, "disagreements_auto.md"), "w").write("\n".join(lines))
print(f"\n{len(diff_items)} items with any disagreement -> check_tone/disagreements_auto.md")
