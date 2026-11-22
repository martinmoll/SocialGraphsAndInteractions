"""The home map: who names whom in press releases, drawn with the course's tools (weeks 3 and 4).

Run from Anas/ after a4/analysis.py:  python a4/figure_home_map.py
Network: the 406 members of the A4 test. An undirected tie joins two members when one named the other in a release
(leaders as the named member left out; co-leads kept). Its weight is the sum of decision 8's 1/n release weights, so
a long signatory list adds little. All ties, same-party and cross-party.
Backbone: the disparity filter (week 4; Serrano et al. 2009) at alpha = ALPHA, which keeps every member connected
with about 1,660 of the 29,163 ties. Alpha was chosen for readability, as in the course's 4.11.
Layout: ForceAtlas2 (networkx), 2,000 iterations, scaling 5, strong gravity, weighted, seed 11 (the 4.11 recipe).
A: the map. Colour = party; filled = exposed seat, hollow = safe (as in Figure 3). Dot size = the member's
cross-party ties in the full network. Dark lines: cross-party ties in the backbone; light: same-party ties.
B: plain numbers: cross-party ties per member, by party and seat.
Also prints a readout of the picture: for each member, the share of their 10 nearest neighbours in the layout who
belong to the other party (exposed against safe). It describes the drawing; it is not a test.
Writes a4/out/figure_home_map.png and .pdf.
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ANAS = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")
ALPHA, SEED = 0.01, 11
COL = {"R": "#e34948", "D": "#2a78d6"}
INK, INK2 = "#0b0b0b", "#52514e"
plt.rcParams.update({"font.family": "sans-serif", "font.size": 8})

t = pd.read_csv(os.path.join(OUT, "member_shares.csv"), index_col=0)
lean = pd.read_csv(os.path.join(ANAS, "district_lean", "member_lean.csv")).set_index("bioguide")
M = pd.read_parquet(os.path.join(ANAS, "a3", "out", "mentions_press.parquet"))
m = M[M.speaker.isin(t.index) & M.named.isin(t.index) & ~M.named_is_leader]
m = m.assign(a=m[["speaker", "named"]].min(axis=1), b=m[["speaker", "named"]].max(axis=1))
w = m.groupby(["a", "b"]).weight.sum().reset_index()
party, exposed = t.party.to_dict(), t.exposed.to_dict()

G = nx.Graph()
G.add_nodes_from(t.index)
G.add_weighted_edges_from(w[["a", "b", "weight"]].itertuples(index=False))
cross_deg = pd.Series({n: sum(party[x] != party[n] for x in G[n]) for n in G})
s, k = dict(G.degree(weight="weight")), dict(G.degree())


def alpha_ij(u, v, wt):
    return min(((1 - wt / s[x]) ** (k[x] - 1) if k[x] > 1 else 1.0) for x in (u, v))


B = nx.Graph()
B.add_nodes_from(G)
B.add_edges_from((u, v, d) for u, v, d in G.edges(data=True) if alpha_ij(u, v, d["weight"]) < ALPHA)
nodes = list(B)


def layout(seed):
    return nx.forceatlas2_layout(B, max_iter=2000, scaling_ratio=5, strong_gravity=True, weight="weight", seed=seed)


def readout(pos):
    """Share of each member's 10 nearest neighbours in the drawing who belong to the other party."""
    P = np.array([pos[n] for n in nodes])
    d2 = ((P[:, None, :] - P[None, :, :]) ** 2).sum(-1)
    np.fill_diagonal(d2, np.inf)
    nn = np.argsort(d2, axis=1)[:, :10]
    return np.array([[party[nodes[j]] != party[nodes[i]] for j in row] for i, row in enumerate(nn)]).mean(1)


pos = layout(SEED)
other = readout(pos)
ro = pd.DataFrame({"other": other, "exposed": [exposed[n] for n in nodes], "party": [party[n] for n in nodes]})
print(f"backbone alpha {ALPHA}: {B.number_of_edges()} ties ({sum(party[u] != party[v] for u, v in B.edges())} "
      f"cross-party) of {G.number_of_edges()}; nodes {B.number_of_nodes()}")
ex = np.array([exposed[n] for n in nodes])
for sd in (SEED, 12, 13):
    o = other if sd == SEED else readout(layout(sd))
    print(f"seed {sd}: other-party share of 10 nearest drawn neighbours: exposed {o[ex].mean():.3f}, "
          f"safe {o[~ex].mean():.3f}")

fig = plt.figure(figsize=(7.6, 4.7))
gs = fig.add_gridspec(1, 2, width_ratios=[1.6, 1], wspace=0.18)
a = fig.add_subplot(gs[0, 0])
from scipy.stats import gaussian_kde
P = np.array([pos[n] for n in nodes])
W, H = np.ptp(P[:, 0]), np.ptp(P[:, 1])
xx, yy = np.meshgrid(np.linspace(P[:, 0].min() - 0.1 * W, P[:, 0].max() + 0.1 * W, 200),
                     np.linspace(P[:, 1].min() - 0.1 * H, P[:, 1].max() + 0.1 * H, 200))
for p in ("R", "D"):                                  # where each party's members sit: a soft area, not a boundary
    sel = np.array([party[n] == p for n in nodes])
    z = gaussian_kde(P[sel].T, bw_method=0.35)(np.vstack([xx.ravel(), yy.ravel()])).reshape(xx.shape)
    a.contourf(xx, yy, z, levels=[np.quantile(z, 0.80), z.max()], colors=[COL[p]], alpha=0.07, zorder=0)
# A (22 Nov, second redesign): four kinds of tie, told apart by colour as well as weight. Cross-party ties are purple
# (red + blue), darker the more exposed members they join; same-party ties stay pale grey in the background.
kinds = {"same": [], "cross00": [], "cross01": [], "cross11": []}
for u, v in B.edges():
    kinds["same" if party[u] == party[v] else f"cross{min(exposed[u], exposed[v]):d}{max(exposed[u], exposed[v]):d}"].append((u, v))
# grey = within a party, purple = across the aisle (darker the more exposed ends); 22 Nov (late): within-party grey made
# stronger, and safe-safe cross ties moved from grey to pale purple so the two greys no longer mean different things
TIE = {"same": ("#a3a29c", 0.35, 0.55, "within a party"),
       "cross00": ("#d3c2e6", 0.4, 0.8, "across, two safe members"),
       "cross01": ("#b48fd6", 0.55, 0.75, "across, one exposed member"),
       "cross11": ("#5a1f8c", 0.8, 0.9, "across, both exposed")}
for kname in ("same", "cross00", "cross01", "cross11"):
    colr, lw, al, _ = TIE[kname]
    for u, v in kinds[kname]:
        a.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=colr, lw=lw, alpha=al, zorder=1,
               solid_capstyle="round")
size = 4 + 0.4 * cross_deg.reindex(nodes).values
for i, n in enumerate(nodes):                        # safe members first, faded
    if not exposed[n]:
        a.scatter(*pos[n], s=size[i], facecolor="white", edgecolor=COL[party[n]], linewidths=0.6, alpha=0.45, zorder=2)
for i, n in enumerate(nodes):                        # exposed members on top, full colour with a white edge
    if exposed[n]:
        a.scatter(*pos[n], s=size[i], facecolor=COL[party[n]], edgecolor="white", linewidths=0.5, zorder=3)
# names: in two columns at the sides of the map, each with a thin line to its member's dot
named = list(cross_deg.sort_values(ascending=False).index[:6])
for b_ in ("G000592", "K000009"):                    # the other halves of the A3.7 mutual pairs
    if b_ in pos and b_ not in named:
        named.append(b_)
for n in named:                                      # labelled members drawn again on top, so their own dot shows
    i = nodes.index(n)
    a.scatter(*pos[n], s=size[i], facecolor=COL[party[n]] if exposed[n] else "white", edgecolor="white" if exposed[n]
              else COL[party[n]], linewidths=0.6 if exposed[n] else 1.0, zorder=5)
cx = np.median(P[:, 0])
x_left, x_right = P[:, 0].min() - 0.08 * W, P[:, 0].max() + 0.08 * W
for side, xcol in ((-1, x_left), (1, x_right)):
    grp = sorted([n for n in named if (pos[n][0] >= cx) == (side > 0)], key=lambda n: -pos[n][1])
    ys, last = [], None
    for n in grp:                                    # keep each name near its dot's height, at least a line apart
        y = pos[n][1] if last is None else min(pos[n][1], last - 0.075 * H)
        ys.append(y)
        last = y
    for n, y in zip(grp, ys):
        nm = lean.at[n, "name"].split()[-1]
        nm = {"Jr.": lean.at[n, "name"].split()[-2]}.get(nm, nm)
        a.annotate(nm, pos[n], xytext=(xcol, y), textcoords="data", fontsize=6.3, color=COL[party[n]], zorder=6,
                   ha="right" if side < 0 else "left", va="center",
                   arrowprops=dict(arrowstyle="-", color=COL[party[n]], lw=0.45, alpha=0.7, shrinkA=1.5, shrinkB=1.5,
                                   connectionstyle="arc3,rad=0"))
medR = np.median(P[[party[n] == "R" for n in nodes], 0])
medD = np.median(P[[party[n] == "D" for n in nodes], 0])
for p, nm, med in [("R", "Republicans", medR), ("D", "Democrats", medD)]:
    left = med < (medR + medD) / 2                   # put each name on its own side of the map
    a.text(P[:, 0].min() if left else P[:, 0].max(), P[:, 1].max() + 0.06 * H, nm,
           ha="left" if left else "right", fontsize=8.5, weight="bold", color=COL[p])
a.set_aspect("equal")
a.set_xlim(x_left - 0.17 * W, x_right + 0.17 * W)
a.axis("off")
a.set_title("A  Who names whom in press releases", loc="left", fontsize=8.5, weight="bold", color=INK)
from matplotlib.lines import Line2D
nodes_h = [Line2D([], [], ls="", marker="o", ms=5, mfc=COL[p], mec="white", label=f"{nm}, exposed seat") for p, nm in
           (("D", "Democrat"), ("R", "Republican"))] + \
          [Line2D([], [], ls="", marker="o", ms=5, mfc="white", mec=COL[p], alpha=0.6, label=f"{nm}, safe seat") for p, nm in
           (("D", "Democrat"), ("R", "Republican"))]
ties_h = [Line2D([], [], color=TIE[k][0], lw=max(1.2, 1.6 * TIE[k][1]), label=f"{TIE[k][3]} ({len(kinds[k]):,})")
          for k in ("cross11", "cross01", "cross00", "same")]
lg1 = a.legend(handles=nodes_h, frameon=False, fontsize=6.2, loc="upper left", bbox_to_anchor=(0.0, 0.02), ncol=1,
               handletextpad=0.2, title="Members (dot size: cross-party ties)", title_fontsize=6.2, alignment="left")
a.add_artist(lg1)
a.legend(handles=ties_h, frameon=False, fontsize=6.2, loc="upper left", bbox_to_anchor=(0.52, 0.02), ncol=1,
         handletextpad=0.4, title="Ties in the backbone", title_fontsize=6.2, alignment="left")

# B (22 Nov late, third version, Anas's choice "simple bars + table"): one measure, plain bars. Cross-party ties per member,
# the result that holds in both parties, after Holm and at every alpha. The other measures are in the table
# (table_home_measures.py). Values and Holm p straight from the result file.
cen = pd.read_csv(os.path.join(OUT, "home_measures_centrality.csv")).set_index(["measure", "party"])
b = fig.add_subplot(gs[0, 1].subgridspec(3, 1, height_ratios=[0.55, 1, 0.75])[1])
grp = [("D", True, "Exposed Democrats"), ("D", False, "Safe Democrats"),
       ("R", True, "Exposed Republicans"), ("R", False, "Safe Republicans")]
ns = {(p, e): sum(1 for n in t.index if party[n] == p and exposed[n] == e) for p, e, _ in grp}
ypos = [3.9, 2.6, 1.3, 0.0]                           # a gap between the two parties
for yi, (p, e, lab) in zip(ypos, grp):
    v = cen.at[("cross-party degree (full map)", p), "exposed_mean" if e else "safe_mean"]
    b.barh(yi, v, height=0.6, color=COL[p] if e else "white", edgecolor=COL[p], linewidth=1.2)
    b.text(v + 1.2, yi, f"{v:.0f}", va="center", fontsize=8, color=INK, weight="bold" if e else "normal")
    b.text(0, yi + 0.42, f"{lab} ({ns[(p, e)]})", va="bottom", ha="left", fontsize=6.6, color=COL[p])
for p, (y_e, y_s) in (("D", (3.9, 2.6)), ("R", (1.3, 0.0))):   # one bracket per party: exposed against safe
    hp = cen.at[("cross-party degree (full map)", p), "p_holm"]
    xb = max(cen.at[("cross-party degree (full map)", p), k] for k in ("exposed_mean", "safe_mean")) + 9
    b.plot([xb - 1.2, xb, xb, xb - 1.2], [y_e, y_e, y_s, y_s], color=INK2, lw=0.7)
    b.text(xb + 1.2, (y_e + y_s) / 2, f"×{cen.at[('cross-party degree (full map)', p), 'ratio']:.1f}\n"
           + ("p < 0.001" if hp < 0.001 else f"p {hp:.3f}"), va="center", fontsize=6.4, color=INK2, linespacing=1.3)
b.set_yticks([])
b.set_xlim(0, 80)
b.set_ylim(-0.45, 4.55)
b.set_xticks([0, 20, 40, 60])
b.tick_params(axis="x", labelsize=6.5, length=2)
for s_ in ("top", "right", "left"):
    b.spines[s_].set_visible(False)
b.spines["bottom"].set_bounds(0, 60)
b.set_xlabel("Members of the other party each one\nnames or is named by (mean)", fontsize=6.8)
b.set_title("B  Cross-party ties per member", loc="left", fontsize=8.5, weight="bold", color=INK, pad=8)
fig.text(0.985, 0.25, "×: exposed members' mean as a multiple of safe members'. p: shuffling exposure within party\n"
         "(10,000 shuffles), Holm-corrected across the 10 network tests. Other measures: table.",
         fontsize=5.6, color=INK2, ha="right", va="top")

for ext in ("png", "pdf"):
    fig.savefig(os.path.join(OUT, f"figure_home_map.{ext}"), dpi=300, bbox_inches="tight", facecolor="white")
ro.to_csv(os.path.join(OUT, "home_map_layout_readout.csv"), index=False)
print("->", os.path.join(OUT, "figure_home_map.png"))
