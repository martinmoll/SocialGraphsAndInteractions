"""The home network at group level: who names whom across the aisle, by party and seat.

Run from Anas/ after home_network.py:  python a4/figure_network_groups.py
Four nodes: exposed and safe members of each party (circle area = members; filled = exposed, hollow = safe, as in
Figure 3). Four cross-party links; link width and label = tie density, the share of possible member pairs between
the two groups that are tied (one named the other in at least one release; leaders as named left out, co-leads kept;
a4/out/home_ties.csv, the main row of home_network.py). Under each node: cross-party ties per member.
Writes a4/out/figure_network_groups.png and .pdf.
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
INK, INK2, LINK = "#0b0b0b", "#52514e", "#8a8984"
plt.rcParams.update({"font.family": "sans-serif", "font.size": 8})

t = pd.read_csv(os.path.join(OUT, "member_shares.csv"), index_col=0)
T = pd.read_csv(os.path.join(OUT, "home_ties.csv"))
grp = {b: ("E" if e else "S") + p for b, e, p in zip(t.index, t.exposed, t.party)}
und = T.assign(a=T[["speaker", "named"]].min(axis=1), b=T[["speaker", "named"]].max(axis=1)).drop_duplicates(["a", "b"])
und["pair"] = [tuple(sorted((grp[a], grp[b]))) for a, b in zip(und.a, und.b)]
n = pd.Series(grp).value_counts()
deg = pd.concat([und.a, und.b]).value_counts().reindex(t.index).fillna(0)
per = deg.groupby(pd.Series(grp)).mean()

pos = {"ED": (0, 1), "SD": (0, 0), "ER": (1, 1), "SR": (1, 0)}
name = {"ED": "Exposed\nDemocrats", "SD": "Safe\nDemocrats", "ER": "Exposed\nRepublicans", "SR": "Safe\nRepublicans"}
fig, ax = plt.subplots(figsize=(5.2, 3.9))

# links, drawn first; width proportional to density
links = []
for (a, b), c in und.pair.value_counts().items():
    links.append((a, b, c, c / (n[a] * n[b])))
for a, b, c, dens in sorted(links, key=lambda x: x[3]):
    (x0, y0), (x1, y1) = pos[a], pos[b]
    ax.plot([x0, x1], [y0, y1], color=LINK, lw=1.5 + dens * 40, alpha=0.6, solid_capstyle="butt", zorder=1)
    # label at the middle of the straight links; on the two crossing diagonals, a quarter of the way from the
    # exposed (top) end, so the two labels sit apart on either side of the crossing
    f = 0.5 if y0 == y1 else 0.25
    lx, ly = x0 + f * (x1 - x0), y0 + f * (y1 - y0)
    ax.text(lx, ly, f"{dens:.0%}\n{c:,} ties", ha="center", va="center", fontsize=7.5, color=INK, zorder=4,
            linespacing=1.15, bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=LINK, lw=0.6))

# nodes
for g, (x, y) in pos.items():
    p = g[1]
    r = 0.055 + 0.075 * np.sqrt(n[g] / n.max())
    circ = plt.Circle((x, y), r, facecolor=COL[p] if g[0] == "E" else "white", edgecolor=COL[p], lw=2, zorder=3)
    ax.add_patch(circ)
    side = -1 if x == 0 else 1
    ax.text(x + side * (r + 0.05), y, f"{name[g]}\n{n[g]} members\n{per[g]:.0f} cross-party ties each",
            ha="right" if side < 0 else "left", va="center", fontsize=7.5, color=INK, linespacing=1.25)

ax.set_xlim(-0.75, 1.75)
ax.set_ylim(-0.22, 1.22)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Who names whom across the aisle in press releases", loc="left", fontsize=9, color=INK,
             weight="bold")
fig.text(0.02, 0.0, "Percentage on each link: of all possible member pairs between the two groups, the share where one "
         "named the other in a press release\n(3 Jan 2025 to 20 Nov 2026). Link width follows it. Exposed: the "
         "district served leans no more than 5 points toward the member's own party.", fontsize=6.5, color=INK2)
for ext in ("png", "pdf"):
    fig.savefig(os.path.join(OUT, f"figure_network_groups.{ext}"), dpi=300, bbox_inches="tight", facecolor="white")
print("->", os.path.join(OUT, "figure_network_groups.png"))
