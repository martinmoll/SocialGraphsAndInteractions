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

fig = plt.figure(figsize=(7.6, 5.0))
gs = fig.add_gridspec(2, 2, width_ratios=[2.2, 1], height_ratios=[1.45, 1], wspace=0.5, hspace=0.5)
a = fig.add_subplot(gs[:, 0])
cpan = fig.add_subplot(gs[0, 1])
b = fig.add_subplot(gs[1, 1])
from scipy.stats import gaussian_kde
P = np.array([pos[n] for n in nodes])
xx, yy = np.meshgrid(np.linspace(P[:, 0].min() - 0.1 * np.ptp(P[:, 0]), P[:, 0].max() + 0.1 * np.ptp(P[:, 0]), 200),
                     np.linspace(P[:, 1].min() - 0.1 * np.ptp(P[:, 1]), P[:, 1].max() + 0.1 * np.ptp(P[:, 1]), 200))
for p in ("R", "D"):                                  # where each party's members sit: a soft area, not a boundary
    sel = np.array([party[n] == p for n in nodes])
    z = gaussian_kde(P[sel].T, bw_method=0.35)(np.vstack([xx.ravel(), yy.ravel()])).reshape(xx.shape)
    a.contourf(xx, yy, z, levels=[np.quantile(z, 0.80), z.max()], colors=[COL[p]], alpha=0.08, zorder=0)
same = [(u, v) for u, v in B.edges() if party[u] == party[v]]
cross = [(u, v) for u, v in B.edges() if party[u] != party[v]]
for edges, colr, lw, al in [(same, "#c9c8c2", 0.25, 0.25), (cross, "#55544f", 0.35, 0.28)]:
    for u, v in edges:
        a.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=colr, lw=lw, alpha=al, zorder=1)
size = 4 + 0.4 * cross_deg.reindex(nodes).values
order = np.argsort([exposed[n] for n in nodes])                       # exposed drawn on top
for i in order:
    n = nodes[i]
    a.scatter(*pos[n], s=size[i], facecolor=COL[party[n]] if exposed[n] else "white", edgecolor=COL[party[n]],
              linewidths=0.8, zorder=3 if exposed[n] else 2)
top = cross_deg.sort_values(ascending=False).index[:6]
placed = []
for n in top:                                        # the six members with most cross-party ties; nudge apart
    nm = lean.at[n, "name"].split()[-1] if n in lean.index else n
    x, y = pos[n]
    dy = 6
    while any(abs(x - px) < 0.12 * np.ptp(P[:, 0]) and abs(y - py) < 0.04 * np.ptp(P[:, 1]) for px, py in placed):
        y += 0.045 * np.ptp(P[:, 1])
        dy += 0
    placed.append((x, y))
    a.annotate(nm, (pos[n][0], pos[n][1]), xytext=(x, y), textcoords="data", fontsize=6.8, color=INK, zorder=5,
               ha="left", va="bottom", arrowprops=dict(arrowstyle="-", color=INK2, lw=0.5),
               bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.85))
C = pd.read_csv(os.path.join(OUT, "home_communities_members.csv"))
comp = C.groupby("community").agg(n=("bioguide", "size"), R=("party", lambda v: (v == "R").sum()),
                                  D=("party", lambda v: (v == "D").sum()), exp=("exposed", "sum"),
                                  states=("state", lambda v: ", ".join(v.value_counts().index[:2])))
comp = comp[comp.n >= 10]


def clabel(r):
    if r.R / r.n > 0.9:
        return "Republican core"
    if r.D / r.n > 0.9:
        return "Democratic core"
    if r.exp / r.n >= 0.5:
        return "Close seats (" + r.states + ")"
    return r.states


comp["label"] = comp.apply(clabel, axis=1)
close = comp[comp.label.str.startswith("Close seats")]
if len(close):
    # ring each member of the close-seat community (an outline around them all would cover many non-members)
    ids = set(C[C.community == close.index[0]].bioguide)
    for n in nodes:
        if n in ids:
            a.scatter(*pos[n], s=size[nodes.index(n)] + 38, facecolor="none", edgecolor=INK, linewidths=0.9, zorder=4)
    a.scatter([], [], s=40, facecolor="none", edgecolor=INK, linewidths=0.9,
              label=f"in the close-seat community ({int(close.n.iloc[0])})")
medR = np.median(P[[party[n] == "R" for n in nodes], 0])
medD = np.median(P[[party[n] == "D" for n in nodes], 0])
for p, nm, med in [("R", "Republicans", medR), ("D", "Democrats", medD)]:
    left = med < (medR + medD) / 2                   # put each name on its own side of the map
    a.text(P[:, 0].min() if left else P[:, 0].max(), P[:, 1].max() + 0.05 * np.ptp(P[:, 1]), nm,
           ha="left" if left else "right", fontsize=8.5, weight="bold", color=COL[p])
a.set_aspect("equal")
a.axis("off")
a.set_title("A  The home map: who names whom in press releases", loc="left", fontsize=8.5, weight="bold", color=INK)
for p, nm in [("D", "Democrats"), ("R", "Republicans")]:
    a.scatter([], [], s=30, facecolor=COL[p], edgecolor=COL[p], label=f"{nm}, exposed seat")
    a.scatter([], [], s=30, facecolor="white", edgecolor=COL[p], label=f"{nm}, safe seat")
a.plot([], [], color="#3d3c38", lw=1.2, label="tie across the aisle")
a.plot([], [], color="#c9c8c2", lw=1.2, label="tie within a party")
a.legend(frameon=False, fontsize=6.5, loc="upper center", bbox_to_anchor=(0.5, 0.03), ncol=2, handletextpad=0.3,
         columnspacing=1.0)

# C (top right): what each community is made of
cc = comp.sort_values("n", ascending=True)
yy_ = np.arange(len(cc))
cpan.barh(yy_, cc.R, color=COL["R"], height=0.65, edgecolor="white", linewidth=0.6)
cpan.barh(yy_, cc.D, left=cc.R, color=COL["D"], height=0.65, edgecolor="white", linewidth=0.6)
for yi, r in zip(yy_, cc.itertuples()):
    cpan.text(r.n + 3, yi, f"{r.label}  ·  {int(r.exp)} exposed", va="center", fontsize=6.2, color=INK)
cpan.set_yticks([])
cpan.set_xlim(0, cc.n.max() * 2.4)
for s_ in ("top", "right", "left"):
    cpan.spines[s_].set_visible(False)
cpan.set_xlabel("Members (red: Republicans, blue: Democrats)", fontsize=6.8)
cpan.set_title("B  Communities (Louvain)", loc="left", fontsize=8.5, weight="bold", color=INK)

# B: cross-party ties per member, by group (full network)
grp = [("D", True, "Exposed Democrats"), ("D", False, "Safe Democrats"),
       ("R", True, "Exposed Republicans"), ("R", False, "Safe Republicans")]
vals = [cross_deg[[n for n in t.index if party[n] == p and exposed[n] == e]].mean() for p, e, _ in grp]
ns = [sum(1 for n in t.index if party[n] == p and exposed[n] == e) for p, e, _ in grp]
y = np.arange(len(grp))[::-1]
for yi, (p, e, lab), v, n in zip(y, grp, vals, ns):
    b.barh(yi, v, height=0.6, color=COL[p] if e else "white", edgecolor=COL[p], linewidth=1.2)
    b.text(v + 1, yi, f"{v:.0f}", va="center", fontsize=7.5, color=INK)
b.set_yticks(y)
b.set_yticklabels([f"{lab} ({n})" for (p, e, lab), n in zip(grp, ns)], fontsize=6.8)
b.tick_params(axis="y", length=0)

b.set_xlim(0, max(vals) * 1.25)
b.set_ylim(-0.6, len(grp) - 0.4)
for s_ in ("top", "right", "left"):
    b.spines[s_].set_visible(False)
b.set_xlabel("Members of the other party each one\nnames or is named by (mean)", fontsize=7)
b.set_title("C  Cross-party ties per member", loc="left", fontsize=8.5, weight="bold", color=INK)
for ext in ("png", "pdf"):
    fig.savefig(os.path.join(OUT, f"figure_home_map.{ext}"), dpi=300, bbox_inches="tight", facecolor="white")
ro.to_csv(os.path.join(OUT, "home_map_layout_readout.csv"), index=False)
print("->", os.path.join(OUT, "figure_home_map.png"))
