"""M7: Figure 1. The two maps, and how divided each is against the nulls.

Run from project/:  python Martin/m7_figure1.py      Writes Martin/figures/figure1.png (300 dpi) and figure1.pdf.
Every number is read from the result files, not recomputed: m3_table.csv, m3_random_draws.csv (G1a),
m4_results.csv (debate null), m3b_state_null.csv (state null). The two network drawings are rebuilt from the data.

  A  Floor map, headline version (phrase yields dropped, G1b): who names whom on the House floor.
  B  One random draw of working ties (cosponsorship) at the same number of ties (G1a, seed 2805).
  C  Cross-party share of ties in each map; the bar for the random draws shows the range of 200 draws.
  D  Party modularity Q of each map against its nulls (degree-preserving, debate, state).
Size: PNAS full width (17.8 cm). The drawings use a spring layout and are for the eye only; positions mean nothing.
With --side (25 Nov): the same panels at 11.4 cm wide, for a PNAS side-caption figure (SCfigure*): drawings A and B
stacked on the left, C and D stacked on the right. Writes Martin/figures/figure1_side.png and .pdf.
"""
import sys
import numpy as np, pandas as pd, networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

SEED = 2805
plt.rcParams.update({"font.size": 7, "axes.titlesize": 8, "axes.labelsize": 7, "xtick.labelsize": 6.5,
                     "ytick.labelsize": 6.5, "font.family": "DejaVu Sans"})
R_COL, D_COL, X_COL, SAME_COL = "#c0392b", "#2e6da4", "#7d3c98", "#9a9a9a"
FLOOR, WORK = "#2b2b2b", "#8c8c8c"

members = pd.read_csv("data/processed/members.csv"); members = members[members.party.isin(["R", "D"])].set_index("bioguide")
party = members.party
M = pd.read_parquet("Martin/mentions.parquet")
M = M[M.speaker.isin(party.index) & M.named.isin(party.index) & ~M.is_yield & (M.speaker != M.named)]
floor = nx.Graph(); floor.add_edges_from(zip(M.speaker, M.named))
bills = pd.read_parquet("data/processed/bills.parquet"); cos = pd.read_parquet("data/processed/cosponsors.parquet")
L = cos[~cos.withdrawn].merge(bills[bills.type.isin(("hr", "hjres"))][["bill_id", "sponsor"]], on="bill_id")
L = L[L.cosponsor.isin(party.index) & L.sponsor.isin(party.index) & (L.cosponsor != L.sponsor)]
work = nx.Graph(); work.add_edges_from(zip(L.cosponsor, L.sponsor))
e = sorted(work.edges()); idx = np.random.default_rng(SEED).choice(len(e), floor.number_of_edges(), replace=False)
draw = nx.Graph(); draw.add_edges_from(e[i] for i in idx)

T = pd.read_csv("Martin/m3_table.csv").set_index("map")
D = pd.read_csv("Martin/m3_random_draws.csv"); D = D[D["size of floor"] == "phrase"]
M4 = pd.read_csv("Martin/m4_results.csv").set_index(["mentions", "null", "measure"])
SN = pd.read_csv("Martin/m3b_state_null.csv").set_index("map")
head = "Floor: yields dropped, phrase rule"
assert int(T.loc[head, "ties"]) == floor.number_of_edges(), "m3_table.csv is not from the current mentions.parquet"

# 25 Nov: 5.6 -> 4.9 in tall, to cut whitespace in the paper. The drawings lose height (positions mean nothing),
# the bar panels keep theirs.
SIDE = "--side" in sys.argv
if SIDE:   # 11.4 cm wide; the caption sits beside the figure
    fig = plt.figure(figsize=(11.4 / 2.54, 4.7))
    top = fig.add_gridspec(2, 1, left=0.0, right=0.33, top=0.90, bottom=0.10, hspace=0.36)
    bot = fig.add_gridspec(2, 1, left=0.635, right=0.985, top=0.95, bottom=0.125, hspace=0.42,
                           height_ratios=[5.6, 7])
else:
    fig = plt.figure(figsize=(7.0, 4.9))
    top = fig.add_gridspec(1, 2, left=0.01, right=0.99, top=0.925, bottom=0.565, wspace=0.04)
    bot = fig.add_gridspec(1, 2, left=0.20, right=0.985, top=0.45, bottom=0.085, wspace=0.72)

def network(ax, G, title, note=""):
    pos = nx.spring_layout(G, seed=SEED, k=0.12, iterations=200)
    cross = [(u, v) for u, v in G.edges() if party[u] != party[v]]
    same = [(u, v) for u, v in G.edges() if party[u] == party[v]]
    nx.draw_networkx_edges(G, pos, edgelist=same, ax=ax, width=0.15, alpha=0.18, edge_color=SAME_COL)
    nx.draw_networkx_edges(G, pos, edgelist=cross, ax=ax, width=0.15, alpha=0.30, edge_color=X_COL)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=4, node_color=[R_COL if party[v] == "R" else D_COL for v in G], linewidths=0)
    ax.set_title(f"{title}\n{note}{G.number_of_edges():,} ties, {len(cross) / G.number_of_edges():.1%} cross-party", loc="left", fontsize=7.5)
    ax.margins(0.01); ax.axis("off")

if SIDE:    # narrow column: the same titles, broken over more lines
    network(fig.add_subplot(top[0, 0]), floor, "A  Floor: who names whom\nin floor speeches")
    network(fig.add_subplot(top[1, 0]), draw, "B  Working: who cosponsors\nwith whom", "random draw, floor's size:\n")
else:
    network(fig.add_subplot(top[0, 0]), floor, "A  Floor: who names whom in floor speeches")
    network(fig.add_subplot(top[0, 1]), draw, "B  Working: who cosponsors with whom", "random draw, floor's size: ")
fig.legend(handles=[Line2D([], [], marker="o", ls="", color=R_COL, ms=4, label="Republican"),
                    Line2D([], [], marker="o", ls="", color=D_COL, ms=4, label="Democrat"),
                    Line2D([], [], color=X_COL, lw=1.2, label="cross-party tie"),
                    Line2D([], [], color=SAME_COL, lw=1.2, label="same-party tie")],
           loc="center", ncol=2 if SIDE else 4, frameon=False, bbox_to_anchor=(0.185, 0.045) if SIDE else (0.5, 0.535),
           fontsize=6.5, columnspacing=0.8 if SIDE else 2.0, handlelength=1.5 if SIDE else 2.0)

# ---- C: cross-party share
ax = fig.add_subplot(bot[0, 0])
g = D["cross-party share"]
rows = [("Floor, yields dropped\n(headline)", T.loc[head, "cross-party share"], None, FLOOR),
        ("Floor, all mentions", T.loc["Floor: all mentions", "cross-party share"], None, FLOOR),
        ("Working, random draws\nat floor size (200)", g.mean(), (g.min(), g.max()), WORK),
        ("Working, strongest ties\nat floor size", T.loc["Working: strongest, size of floor (phrase)", "cross-party share"], None, WORK),
        ("Working, all ties", T.loc["Working: all ties", "cross-party share"], None, WORK)]
y = np.arange(len(rows))[::-1]
for yi, (lab, v, r, col) in zip(y, rows):
    ax.barh(yi, 100 * v, color=col, height=0.62)
    if r:
        ax.errorbar(100 * v, yi, xerr=[[100 * (v - r[0])], [100 * (r[1] - v)]], color="k", capsize=2, lw=0.8)
    ax.text(100 * (r[1] if r else v) + 1, yi, f"{v:.1%}", va="center", fontsize=6.5)
ax.axvline(50, color=X_COL, ls="--", lw=0.8)
ax.text(49, y[0] + 0.5, "ties rewired at random ≈ 50%", ha="right", fontsize=6, color=X_COL)
ax.set_yticks(y, [r[0] for r in rows]); ax.set_xlim(0, 56); ax.set_ylim(-0.6, len(rows) - 0.2)
ax.set_xticks(range(0, 51, 10))   # the ticks matplotlib showed; set so no hidden tick sits past the axis
ax.set_xlabel("cross-party share of ties (%)")
ax.set_title("C  How often ties cross the aisle", loc="left", x=-0.62 if SIDE else 0)
ax.spines[["top", "right"]].set_visible(False)

# ---- D: party modularity against the nulls
ax = fig.add_subplot(bot[1, 0] if SIDE else bot[0, 1])
deb = M4.loc[("Yields dropped", "debate", "party Q")]
degf = M4.loc[("Yields dropped", "degree", "party Q")]
sn = SN.loc["Floor: yields dropped (headline)"]
q = D["party Q"]
items = [  # label, value, (low, high) or None, filled?, colour
    ("Floor map", T.loc[head, "party Q"], None, True, FLOOR),
    ("Floor null:\nshuffled in debates", deb["null mean"], (deb["null min"], deb["null max"]), False, FLOOR),
    ("Floor null:\nsame-state ties kept", sn["state null Q mean"], (sn["state null Q mean"], sn["state null Q max"]), False, FLOOR),
    ("Floor null:\ndegrees kept", degf["null mean"], (degf["null min"], degf["null max"]), False, FLOOR),
    ("Working, random\ndraws (200)", q.mean(), (q.min(), q.max()), True, WORK),
    ("Working, all ties", T.loc["Working: all ties", "party Q"], None, True, WORK),
    ("Working null:\ndegrees kept", T.loc["Working: all ties", "null Q mean"], (T.loc["Working: all ties", "null Q mean"], T.loc["Working: all ties", "null Q max"]), False, WORK)]
y = np.arange(len(items))[::-1]
for yi, (lab, v, r, filled, col) in zip(y, items):
    if r:
        ax.plot([r[0], r[1]], [yi, yi], color=col, lw=1.6, alpha=0.6, solid_capstyle="butt")
    ax.plot(v, yi, "o", ms=4.5, color=col, mfc=col if filled else "white", mew=1)
    ax.text(max(v, r[1] if r else v) + 0.008, yi, f"{v:.3f}", va="center", fontsize=6)
ax.axvline(0, color="#cccccc", lw=0.6)
ax.set_yticks(y, [i[0] for i in items]); ax.set_xlim(-0.03, 0.27); ax.set_ylim(-0.6, len(items) - 0.4)
ax.set_xticks(np.arange(0, 0.26, 0.05))   # as above
ax.set_xlabel("party modularity Q\n(0 = no division by party)" if SIDE else "party modularity Q (0 = no division by party)")
ax.set_title("D  Party division against the nulls", loc="left", x=-0.62 if SIDE else 0)
ax.spines[["top", "right"]].set_visible(False)

fig.canvas.draw(); rend = fig.canvas.get_renderer()
if SIDE:   # no two visible labels may overlap, and none may leave the figure
    texts = [t for t in fig.findobj(matplotlib.text.Text) if t.get_visible() and t.get_text().strip()]
    boxes = [(t.get_text().replace("\n", " "), t.get_window_extent(rend)) for t in texts]
    clash = [(a, b) for i, (a, ea) in enumerate(boxes) for b, eb in boxes[i + 1:] if ea.overlaps(eb)]
    assert not clash, f"overlapping labels: {clash}"
    off = [a for a, e in boxes if e.x0 < 0 or e.y0 < 0 or e.x1 > fig.bbox.width or e.y1 > fig.bbox.height]
    assert not off, f"labels outside the figure: {off}"
else:      # no text of panel D may reach into panel C (labels, value labels): checked on the drawn figure
    axC, axD = fig.axes[-2], fig.axes[-1]
    c_right = max([axC.get_window_extent(rend).x1] + [t.get_window_extent(rend).x1 for t in axC.texts])
    d_left = min(t.get_window_extent(rend).x0 for t in axD.get_yticklabels())
    assert d_left > c_right + 4, f"panel D labels overlap panel C ({d_left:.0f} <= {c_right:.0f} px)"
name = "figure1_side" if SIDE else "figure1"
fig.savefig(f"Martin/figures/{name}.png", dpi=300); fig.savefig(f"Martin/figures/{name}.pdf")
print(f"written Martin/figures/{name}.png and .pdf")
