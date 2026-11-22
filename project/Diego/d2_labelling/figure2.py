"""Figure 2: what floor mentions do, from the 100 hand-labelled mentions (Diego's codes), with 95% Wilson intervals.

Run from project/:  python Diego/d2_labelling/figure2.py
Writes report/figures/figure2.pdf and .png (PNAS single column, 8.7 cm wide).
"""
from math import sqrt
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
OUT = Path("report/figures")
L = pd.read_csv(HERE / "labels_final.csv", keep_default_na=False)
CODES = ["A", "N", "D", "P", "X"]
NAMES = {"A": "Agreeing", "N": "Neutral", "D": "Disagreeing", "P": "Procedure", "X": "Not that member"}


def wilson(k, n, z=1.96):
    p = k / n; c = p + z * z / (2 * n); h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)); d = 1 + z * z / n
    return p, (c - h) / d, (c + h) / d


plt.rcParams.update({"font.size": 7, "font.family": "sans-serif"})
fig, ax = plt.subplots(figsize=(8.7 / 2.54, 5.6 / 2.54))
y = np.arange(len(CODES))
for k, (cross, colour, label) in enumerate([(True, "#7D3C98", "Cross-party (n = 75)"), (False, "#999999", "Same-party (n = 25)")]):
    g = L[L.cross == cross]
    stats = [wilson((g.diego == c).sum(), len(g)) for c in CODES]
    p = np.array([s[0] for s in stats]); lo = p - np.array([s[1] for s in stats]); hi = np.array([s[2] for s in stats]) - p
    ax.barh(y + (k - 0.5) * 0.38, p * 100, 0.36, xerr=[lo * 100, hi * 100], color=colour, label=label,
            error_kw={"elinewidth": 0.6, "capsize": 1.5})
ax.set_yticks(y, [NAMES[c] for c in CODES]); ax.invert_yaxis()
ax.set_xlabel("Share of hand-labelled floor mentions (%)"); ax.set_xlim(0, 100)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, loc="lower right")
fig.tight_layout()
OUT.mkdir(parents=True, exist_ok=True)
fig.savefig(OUT / "figure2.pdf"); fig.savefig(OUT / "figure2.png", dpi=300)
print("wrote", OUT / "figure2.pdf")
