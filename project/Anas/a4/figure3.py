"""Figure 3 (draft, two panels side by side): exposed members name the other party more at home, in both parties.
Superseded for the paper by a4/figure3_column.py (one column, 23 Nov); kept for the record.

Run from Anas/ after a4/analysis.py:  python a4/figure3.py
A: every member's share of releases naming the other party (co-leads and leaders left out) against the lean of the
   district served, with the mean per 5-point band (bands with >= 5 members). B: the exposed - safe gap per party
   under every robustness row, main row on top. Colour = party. Writes a4/out/figure3_draft.png and .pdf.
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
R = pd.read_csv(os.path.join(OUT, "results.csv"))
rng = np.random.default_rng(2805)

fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 3.2), gridspec_kw={"width_ratios": [1.45, 1.0], "wspace": 0.75})

# A: every member against the lean of the district served, with the mean per 5-point band (n >= 5)
a.axvspan(-5, 5, color="#efeeea", zorder=0)
a.text(0, 0.985, "exposed\nband", transform=a.get_xaxis_transform(), ha="center", va="top", fontsize=6.5, color=INK2)
for p, name in [("D", "Democrats"), ("R", "Republicans")]:
    g = t[t.party == p]
    a.scatter(g.lean_2025, g.share * 100, s=8, color=COL[p], alpha=0.4, linewidths=0, zorder=2)
    g = g.assign(bin=pd.cut(g.lean_2025, np.arange(-45, 50, 5)))
    bb = g.groupby("bin", observed=True).agg(x=("lean_2025", "mean"), y=("share", "mean"), n=("share", "size"))
    bb = bb[bb.n >= 5]
    a.plot(bb.x, bb.y * 100, color=COL[p], lw=2, zorder=3, solid_capstyle="round")
    a.scatter(bb.x, bb.y * 100, s=20, color=COL[p], edgecolors="white", linewidths=1, zorder=4)
    a.text(44 if p == "R" else -44, 33, f"{name}\n{len(t[t.party == p])} members", color=COL[p], fontsize=7,
           va="center", ha="right" if p == "R" else "left", weight="bold")
ticks = np.arange(-40, 41, 20)
a.set_xticks(ticks)
a.set_xticklabels([f"D+{-x}" if x < 0 else (f"R+{x}" if x > 0 else "even") for x in ticks])
a.set_xlim(-48, 48)
a.set_ylim(0, 42)
a.set_xlabel("Lean of the district served (Cook PVI 2025)")
a.set_ylabel("Releases naming the other party (%)")
a.yaxis.grid(True, color=GRID, lw=0.6)
a.set_axisbelow(True)
a.set_title("A  Every member, by district lean", loc="left", fontsize=8.5, color=INK, weight="bold")

# B: gaps under every robustness row
labels = {"main: exposed_2025 (own-party lean <= 5)": "Main: lean within 5",
          "check 4: cut-off +-4": "Cut-off 4", "check 4: cut-off +-6": "Cut-off 6",
          "second lean source: 2024 presidential margin": "2024 presidential margin",
          "check 1: without the 21 relabelled or unknown in 2026": "Without 21 relabelled",
          "check 2: without redistricting releases": "Without redistricting",
          "without caucus releases": "Without caucus releases",
          "outcome with co-leads kept": "Co-leads kept",
          "Martin's matcher alone (shared)": "Floor matcher only"}
R = R.assign(lab=R.check.map(labels))
y = np.arange(len(R))[::-1]
for p, dy in [("R", 0.15), ("D", -0.15)]:
    g = R[f"{p}_gap"].values * 100
    sig = R[f"p_{p}"].values < 0.05
    b.scatter(g, y + dy, s=22, color=COL[p], edgecolors=COL[p], zorder=3, label="Republicans" if p == "R" else "Democrats")
    for gi, yi, si in zip(g, y + dy, sig):
        b.text(gi + 0.25, yi, "" if si else "n.s.", va="center", fontsize=6, color=INK2)
b.axvline(0, color=INK2, lw=0.8)
b.set_yticks(y)
b.set_yticklabels(R.lab, fontsize=7)
b.get_yticklabels()[0].set_weight("bold")
b.set_xlabel("Exposed minus safe (percentage points)")
b.set_xlim(-1, max(8, R[["R_gap", "D_gap"]].values.max() * 100 + 1.5))
b.xaxis.grid(True, color=GRID, lw=0.6)
b.set_axisbelow(True)
b.legend(frameon=False, fontsize=7, loc="lower right", handletextpad=0.2)
b.set_title("B  The gap under each robustness check", loc="left", fontsize=8.5, color=INK, weight="bold")

for ext in ("png", "pdf"):
    fig.savefig(os.path.join(OUT, f"figure3_draft.{ext}"), dpi=300, bbox_inches="tight", facecolor="white")
print("->", os.path.join(OUT, "figure3_draft.png"))
