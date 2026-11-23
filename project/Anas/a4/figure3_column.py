"""Figure 3 for the paper, one PNAS column (8.7 cm), panel A above panel B. Same data and encodings as
a4/figure3.py (the two-panel draft of 22 Nov), remade 23 Nov because the paper places Figure 3 in one column, where
the side-by-side draft's text would shrink to about 3 pt.

Run from Anas/ after a4/analysis.py:  python -I a4/figure3_column.py
A: every member's share of releases naming the other party (co-leads and leaders left out) against the lean of the
   district served, with the mean per 5-point band (bands with >= 5 members). B: the exposed - safe gap per party
   under every robustness row, main row on top. Colour = party only. Saved at its print size (no tight bbox), so
   fonts print at their set size (6.5-7.5 pt; PNAS minimum 6 pt). Checks that no two text labels overlap.
Writes a4/out/figure3.png and a4/out/figure3.pdf.
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
W, H = 8.7 / 2.54, 5.9                       # inches: one PNAS column wide
plt.rcParams.update({"font.family": "sans-serif", "font.size": 7, "axes.edgecolor": INK2, "axes.labelcolor": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.linewidth": 0.6,
                     "xtick.major.width": 0.6, "ytick.major.width": 0.6, "pdf.fonttype": 42})

t = pd.read_csv(os.path.join(OUT, "member_shares.csv"), index_col=0)
R = pd.read_csv(os.path.join(OUT, "results.csv"))

fig = plt.figure(figsize=(W, H))
a = fig.add_axes([0.17, 0.565, 0.79, 0.385])   # [left, bottom, width, height] in figure fractions
b = fig.add_axes([0.42, 0.075, 0.54, 0.385])

# A
a.axvspan(-5, 5, color="#efeeea", zorder=0)
a.text(0, 0.985, "within 5\nof even", transform=a.get_xaxis_transform(), ha="center", va="top", fontsize=6,
       color=INK2)
for p, name in [("D", "Democrats"), ("R", "Republicans")]:
    g = t[t.party == p]
    a.scatter(g.lean_2025, g.share * 100, s=4, color=COL[p], alpha=0.4, linewidths=0, zorder=2)
    g = g.assign(bin=pd.cut(g.lean_2025, np.arange(-45, 50, 5)))
    bb = g.groupby("bin", observed=True).agg(x=("lean_2025", "mean"), y=("share", "mean"), n=("share", "size"))
    bb = bb[bb.n >= 5]
    a.plot(bb.x, bb.y * 100, color=COL[p], lw=1.4, zorder=3, solid_capstyle="round")
    a.scatter(bb.x, bb.y * 100, s=11, color=COL[p], edgecolors="white", linewidths=0.7, zorder=4)
    a.text(46 if p == "R" else -46, 34, f"{name}\n{len(t[t.party == p])} members", color=COL[p], fontsize=7,
           va="center", ha="right" if p == "R" else "left", weight="bold")
ticks = np.arange(-40, 41, 20)
a.set_xticks(ticks)
a.set_xticklabels([f"D+{-x}" if x < 0 else (f"R+{x}" if x > 0 else "even") for x in ticks])
a.set_xlim(-48, 48)
a.set_ylim(0, 42)
a.set_yticks(range(0, 41, 10))
a.set_xlabel("Lean of the district served (Cook PVI 2025)", labelpad=2)
a.set_ylabel("Releases naming the\nother party (%)", labelpad=2)
a.yaxis.grid(True, color=GRID, lw=0.5)
a.set_axisbelow(True)
a.set_title("A  Every member, by district lean", loc="left", fontsize=7.5, color=INK, weight="bold", x=-0.19)

# B
labels = {"main: exposed_2025 (own-party lean <= 5)": "Main: lean within 5",
          "check 4: cut-off +-4": "Cut-off 4", "check 4: cut-off +-6": "Cut-off 6",
          "second lean source: 2024 presidential margin": "2024 presidential margin",
          "check 1: without the 21 relabelled or unknown in 2026": "Without 21 relabelled",
          "check 2: without redistricting releases": "Without redistricting",
          "without caucus releases": "Without caucus releases",
          "outcome with co-leads kept": "Co-leads kept",
          "Martin's matcher alone (shared)": "Floor matcher only"}
R = R.assign(lab=R.check.map(labels))
assert R.lab.notna().all(), "a robustness row has no label"
y = np.arange(len(R))[::-1]
for p, dy in [("R", 0.17), ("D", -0.17)]:
    g = R[f"{p}_gap"].values * 100
    sig = R[f"p_{p}"].values < 0.05
    b.scatter(g, y + dy, s=12, color=COL[p], zorder=3, label="Republicans" if p == "R" else "Democrats")
    for gi, yi, si in zip(g, y + dy, sig):
        if not si:
            b.text(gi + 0.25, yi, "n.s.", va="center", fontsize=6, color=INK2)
b.axvline(0, color=INK2, lw=0.6)
b.set_yticks(y)
b.set_yticklabels(R.lab)
b.get_yticklabels()[0].set_weight("bold")
b.set_ylim(-0.6, len(R) - 0.4)
b.set_xlabel("Exposed minus safe (percentage points)", labelpad=2)
xmax = max(8, R[["R_gap", "D_gap"]].values.max() * 100 + 1)
b.set_xlim(-0.5, xmax)
b.set_xticks(range(0, int(xmax) + 1, 2))
b.xaxis.grid(True, color=GRID, lw=0.5)
b.set_axisbelow(True)
b.legend(frameon=False, fontsize=6.5, loc="lower right", bbox_to_anchor=(1.02, 1.0), ncol=2, handletextpad=0.1,
         columnspacing=0.8, borderaxespad=0.2, markerscale=1.2)   # above the plot area: never covers a point
b.set_title("B  The gap under each check", loc="left", fontsize=7.5, color=INK, weight="bold", x=-0.72)

# overlap check: every pair of visible text labels (titles, tick labels, axis labels, annotations, legend)
fig.canvas.draw()
r = fig.canvas.get_renderer()
texts = [x for x in fig.findobj(matplotlib.text.Text) if x.get_visible() and x.get_text().strip()]
boxes = [(x.get_text().replace("\n", " "), x.get_window_extent(r)) for x in texts]
clash = [(s1, s2) for i, (s1, e1) in enumerate(boxes) for s2, e2 in boxes[i + 1:] if e1.overlaps(e2)]
assert not clash, f"overlapping labels: {clash}"
off = [s for s, e in boxes if e.x0 < 0 or e.y0 < 0 or e.x1 > fig.bbox.width or e.y1 > fig.bbox.height]
assert not off, f"labels outside the figure: {off}"

for ext in ("png", "pdf"):
    fig.savefig(os.path.join(OUT, f"figure3.{ext}"), dpi=600 if ext == "png" else None, facecolor="white")
print(f"-> {os.path.join(OUT, 'figure3.pdf')}  ({W * 2.54:.1f} x {H * 2.54:.1f} cm); {len(boxes)} labels, no overlaps")
