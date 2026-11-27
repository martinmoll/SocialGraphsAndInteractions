"""Slide 1's two networks, re-drawn for a projector (DECISIONS G25). Same data, ties and layout seed as Figure 1
(Martin/m7_figure1.py); only the styling differs: same-party ties nearly invisible, cross-party ties bold purple, so
the floor map lights up and the working map stays two blobs. Don Bacon (the talk's thread member) is ringed.

Run from project/:  python report/slides/make_slide_networks.py
Writes report/slides/figures/net_floor.pdf, net_work.pdf (and .png). No number is computed here except the
cross-party share, which is asserted against Figure 1's values.
"""
import numpy as np, pandas as pd, networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SEED = 2805
R_COL, D_COL, X_COL, SAME_COL = "#c0392b", "#2e6da4", "#7d3c98", "#9a9a9a"
BACON = "B001298"

# Data loading copied from Martin/m7_figure1.py so the ties are identical.
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


def network(G, name, expected):
    pos = nx.spring_layout(G, seed=SEED, k=0.12, iterations=200)
    cross = [(u, v) for u, v in G.edges() if party[u] != party[v]]
    same = [(u, v) for u, v in G.edges() if party[u] == party[v]]
    share = len(cross) / G.number_of_edges()
    assert abs(share - expected) < 0.0005, f"{name}: {share:.4f} is not Figure 1's {expected}"
    # 27 Nov: wider canvas (2.17:1, the slide column's shape) and a frame fitted to the 1st-99th percentile of node
    # positions, so the dense core fills the slide. Positions carry no meaning, so the stretch changes nothing read
    # from the map; the few outlying nodes that fall outside the frame are counted and printed.
    fig = plt.figure(figsize=(4.4, 2.03)); ax = fig.add_axes([0, 0, 1, 1])
    P = np.array(list(pos.values()))
    lo, hi = np.percentile(P, 1, axis=0), np.percentile(P, 99, axis=0)
    pad = 0.04 * (hi - lo); lo, hi = lo - pad, hi + pad
    outside = int(((P < lo) | (P > hi)).any(axis=1).sum())
    nx.draw_networkx_edges(G, pos, edgelist=same, ax=ax, width=0.2, alpha=0.10, edge_color=SAME_COL)
    nx.draw_networkx_edges(G, pos, edgelist=cross, ax=ax, width=0.45, alpha=0.55, edge_color=X_COL)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=6, linewidths=0,
                           node_color=[R_COL if party[v] == "R" else D_COL for v in G])
    if BACON in pos:
        x, y = pos[BACON]
        ax.scatter([x], [y], s=110, facecolors="none", edgecolors="black", linewidths=1.4, zorder=5)
        ax.annotate("Bacon", (x, y), xytext=(8, 8), textcoords="offset points", fontsize=8, weight="bold")
    ax.set_xlim(lo[0], hi[0]); ax.set_ylim(lo[1], hi[1]); ax.axis("off")
    for ext in ("pdf", "png"):
        fig.savefig(f"report/slides/figures/{name}.{ext}", dpi=300)
    print(name, f"{G.number_of_edges():,} ties, {share:.1%} cross-party, Bacon drawn: {BACON in pos}, "
          f"{outside} of {len(P)} nodes outside the frame")


network(floor, "net_floor", 0.387)
network(draw, "net_work", 0.293)   # the one draw drawn, as Figure 1B; the slide's 28.6% is the mean of 200 draws
