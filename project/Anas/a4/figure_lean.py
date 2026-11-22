"""The A4 pattern across all members: share of releases naming the other party against district lean.

Run from Anas/ after a4/analysis.py:  python a4/figure_lean.py
This draws check 4's "lean as a number" (methods_drafts.md), which uses every member, not only two groups.
x = Cook PVI 2025 of the district served (negative = leans Democratic), y = the A4 outcome per member.
Dots: members (n = 406). Lines: mean per 5-point bin of lean, per party, where a bin holds at least 5 members.
The grey band is where seats count as exposed for both parties (within 5 points of even); a Republican to the left
of R+5 and a Democrat to the right of D+5 are exposed. Writes a4/out/figure_lean.png and .pdf.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
COL = {"R": "#e34948", "D": "#2a78d6"}
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e6e5e1"
plt.rcParams.update({"font.family": "sans-serif", "font.size": 8, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False})

t = pd.read_csv(os.path.join(OUT, "member_shares.csv"), index_col=0)
sl = pd.read_csv(os.path.join(OUT, "lean_slope.csv")).set_index("party")
fig, ax = plt.subplots(figsize=(6.4, 3.4))
ax.axvspan(-5, 5, color="#efeeea", zorder=0)
ax.text(0, 0.985, "within 5 points\nof even", transform=ax.get_xaxis_transform(), ha="center", va="top",
        fontsize=7, color=INK2)
for p, name in [("D", "Democrats"), ("R", "Republicans")]:
    g = t[t.party == p]
    ax.scatter(g.lean_2025, g.share * 100, s=11, color=COL[p], alpha=0.45, linewidths=0, zorder=2)
    bins = np.arange(-45, 50, 5)
    g = g.assign(bin=pd.cut(g.lean_2025, bins))
    b = g.groupby("bin", observed=True).agg(x=("lean_2025", "mean"), y=("share", "mean"), n=("share", "size"))
    b = b[b.n >= 5]
    ax.plot(b.x, b.y * 100, color=COL[p], lw=2, zorder=3, solid_capstyle="round")
    ax.scatter(b.x, b.y * 100, s=26, color=COL[p], edgecolors="white", linewidths=1.2, zorder=4)
    ax.text(44 if p == "R" else -44, 24, f"{name}\n{len(t[t.party == p])} members", color=COL[p], fontsize=7.5,
            va="center", ha="right" if p == "R" else "left", weight="bold")
ax.set_xlabel("District lean, Cook PVI 2025 of the district served (D+ ← 0 → R+)")
ax.set_ylabel("Releases naming the other party (%)")
ticks = np.arange(-40, 41, 10)
ax.set_xticks(ticks)
ax.set_xticklabels([f"D+{-x}" if x < 0 else (f"R+{x}" if x > 0 else "even") for x in ticks])
ax.set_xlim(-48, 48)
ax.set_ylim(0, 45)
ax.yaxis.grid(True, color=GRID, lw=0.6)
ax.set_axisbelow(True)
ax.set_title("Members in the closest seats name the other party most, in both parties", loc="left",
             fontsize=8.5, color=INK, weight="bold")
for ext in ("png", "pdf"):
    fig.savefig(os.path.join(OUT, f"figure_lean.{ext}"), dpi=300, bbox_inches="tight", facecolor="white")
print("->", os.path.join(OUT, "figure_lean.png"))
