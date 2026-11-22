"""The home network of cross-party showing (planned in HOME_NETWORK_PLAN.md).

Run from Anas/ after home_network.py:  python a4/figure_network.py
Democrats in the left column, Republicans in the right. Each member is placed by their lean toward their own party
(crossover and close seats at the top, the safest at the bottom); dot size = cross-party ties. Lines: cross-party
ties named in at least 2 releases. Dark: both ends exposed; light: the rest. Writes a4/out/figure_network.png, .pdf.
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
INK, INK2 = "#0b0b0b", "#52514e"
plt.rcParams.update({"font.family": "sans-serif", "font.size": 8})

t = pd.read_csv(os.path.join(OUT, "member_shares.csv"), index_col=0)
ties = pd.read_csv(os.path.join(OUT, "home_ties.csv"))
own = np.where(t.party == "R", t.lean_2025, -t.lean_2025)
rng = np.random.default_rng(2805)
t["x"] = np.where(t.party == "D", 0.0, 1.0) + rng.uniform(-0.06, 0.06, len(t)) * np.where(t.party == "D", -1, 1)
t["y"] = -own + rng.uniform(-0.4, 0.4, len(t))                     # top = least safe
two = ties[ties.releases >= 2]                       # same definition as home_network.py's "ties >= 2 releases" row
und = two.assign(a=two[["speaker", "named"]].min(axis=1), b=two[["speaker", "named"]].max(axis=1)) \
    .groupby(["a", "b"]).agg(releases=("releases", "sum")).reset_index()
deg = pd.concat([und.a, und.b]).value_counts()
ea, eb = und.a.map(t.exposed), und.b.map(t.exposed)
ee, es = ea & eb, ea ^ eb

fig, ax = plt.subplots(figsize=(4.6, 5.6))
kinds = [(~ee & ~es, "#c9c8c2", "both safe"), (es, "#8a8984", "one exposed"), (ee, "#2b2a27", "both exposed")]
for sel, colr, lab in kinds:                       # same thin line for every kind: density, not ink, tells the story
    for r in und[sel].itertuples():
        ax.plot([t.at[r.a, "x"], t.at[r.b, "x"]], [t.at[r.a, "y"], t.at[r.b, "y"]], color=colr, lw=0.3, alpha=0.3,
                zorder=1, solid_capstyle="round")
    ax.plot([], [], color=colr, lw=1.5, label=f"{lab} ({int(sel.sum())})")
for p in ("D", "R"):
    g = t[t.party == p]
    s = 6 + 1.2 * g.index.map(deg).fillna(0).values
    ax.scatter(g.x, g.y, s=s, facecolors=np.where(g.exposed, COL[p], "white"), edgecolors=COL[p], linewidths=0.8, zorder=3)
ax.axhspan(-5.5, 50, color="#efeeea", zorder=0)
ax.set_ylim(-own.max() - 2, -own.min() + 2)
ax.set_xlim(-0.35, 1.35)
yt = [-40, -30, -20, -10, 0, 10]
ax.set_yticks(yt)
ax.set_yticklabels([f"+{-v}" if v < 0 else ("even" if v == 0 else f"{v} to the other party") for v in yt])
ax.legend(frameon=False, fontsize=7, loc="lower center", bbox_to_anchor=(0.5, -0.12), ncol=3, handlelength=1.2,
          title="Ties (filled dot: exposed member, hollow: safe)", title_fontsize=7)
ax.set_ylabel("Lean toward the member's own party (points)")
ax.set_xticks([0, 1])
ax.set_xticklabels(["Democrats", "Republicans"], fontsize=8.5, weight="bold")
for s_ in ("top", "right", "bottom"):
    ax.spines[s_].set_visible(False)
ax.tick_params(axis="x", length=0)
n_ee, n_all = int(ee.sum()), len(und)
ax.set_title(f"Cross-party press ties: one member named the other in 2+ releases ({n_all})", fontsize=8,
             color=INK, loc="left")
for ext in ("png", "pdf"):
    fig.savefig(os.path.join(OUT, f"figure_network.{ext}"), dpi=300, bbox_inches="tight", facecolor="white")
print("->", os.path.join(OUT, "figure_network.png"), n_all, n_ee)
