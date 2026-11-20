"""M7: first draft of Figure 1, the two maps and their division against the nulls. DRAFT, 20 Nov.

Run from project/:  python Martin/m7_figure1.py      Writes Martin/figures/figure1_draft.png (and .pdf).
Reads Martin/m3_table.csv, Martin/m3_random_draws.csv, Martin/mentions.parquet, data/processed/.

A: the headline floor map (phrase yields dropped).  B: one random draw of working ties at the same size (G1a).
Both drawn with the same spring layout settings, nodes coloured by party; the layout is for the eye only.
C: cross-party share of ties: floor maps, the 200 random working draws (range), strongest working ties, and the
degree-preserving null (about 50%). Numbers come from the M3 table, not recomputed here.
"""
import numpy as np, pandas as pd, networkx as nx, matplotlib.pyplot as plt

SEED = 2805
members = pd.read_csv("data/processed/members.csv"); members = members[members.party.isin(["R", "D"])].set_index("bioguide")
party = members.party
COL = {"R": "#c0392b", "D": "#2e6da4"}
M = pd.read_parquet("Martin/mentions.parquet"); M = M[M.speaker.isin(party.index) & M.named.isin(party.index) & ~M.is_yield]
floor = nx.Graph(); floor.add_edges_from(zip(M.speaker, M.named))
bills = pd.read_parquet("data/processed/bills.parquet"); cos = pd.read_parquet("data/processed/cosponsors.parquet")
L = cos[~cos.withdrawn].merge(bills[bills.type.isin(("hr", "hjres"))][["bill_id", "sponsor"]], on="bill_id")
L = L[L.cosponsor.isin(party.index) & L.sponsor.isin(party.index) & (L.cosponsor != L.sponsor)]
work = nx.Graph(); work.add_edges_from(zip(L.cosponsor, L.sponsor))
e = list(work.edges()); idx = np.random.default_rng(SEED).choice(len(e), floor.number_of_edges(), replace=False)
draw = nx.Graph(); draw.add_edges_from(e[i] for i in idx)

T = pd.read_csv("Martin/m3_table.csv").set_index("map")
D = pd.read_csv("Martin/m3_random_draws.csv")

fig = plt.figure(figsize=(12, 4.6))
for k, (G, title) in enumerate([(floor, "A  Floor: who names whom"), (draw, "B  Working: who cosponsors with whom\n(random draw, same number of ties)")]):
    ax = fig.add_subplot(1, 3, k + 1)
    pos = nx.spring_layout(G, seed=SEED, k=0.12, iterations=200)
    cross = [(u, v) for u, v in G.edges() if party[u] != party[v]]
    same = [(u, v) for u, v in G.edges() if party[u] == party[v]]
    nx.draw_networkx_edges(G, pos, edgelist=same, ax=ax, width=0.2, alpha=0.15, edge_color="#777")
    nx.draw_networkx_edges(G, pos, edgelist=cross, ax=ax, width=0.2, alpha=0.25, edge_color="#8e44ad")
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=7, node_color=[COL[party[v]] for v in G], linewidths=0)
    ax.set_title(f"{title}\n{G.number_of_edges():,} ties, {len(cross) / G.number_of_edges():.0%} cross-party", fontsize=9); ax.axis("off")

ax = fig.add_subplot(1, 3, 3)
g = D[D["size of floor"] == "phrase"]["cross-party share"]
rows = [("Floor, yields dropped (headline)", T.loc["Floor: yields dropped, phrase rule", "cross-party share"], None),
        ("Floor, all mentions", T.loc["Floor: all mentions", "cross-party share"], None),
        ("Working, random draws (200)", g.mean(), (g.min(), g.max())),
        ("Working, strongest ties", T.loc["Working: strongest, size of floor (phrase)", "cross-party share"], None),
        ("Working, all ties", T.loc["Working: all ties", "cross-party share"], None)]
y = np.arange(len(rows))[::-1]
for yi, (lab, v, rng_) in zip(y, rows):
    c = "#444" if lab.startswith("Floor") else "#999"
    ax.barh(yi, v * 100, color=c, height=0.6)
    if rng_: ax.errorbar(v * 100, yi, xerr=[[100 * (v - rng_[0])], [100 * (rng_[1] - v)]], color="k", capsize=3, lw=1)
    ax.text((rng_[1] if rng_ else v) * 100 + 1, yi, f"{v:.0%}" + (f" ({rng_[0]:.0%}–{rng_[1]:.0%})" if rng_ else ""), va="center", fontsize=8)
ax.axvline(50, color="#8e44ad", ls="--", lw=1); ax.text(49.5, y[0] + 0.45, "rewired null ≈ 50%", fontsize=7, color="#8e44ad", ha="right")
ax.set_yticks(y, [r[0] for r in rows], fontsize=8); ax.set_xlim(0, 60); ax.set_xlabel("cross-party share of ties (%)", fontsize=8)
ax.set_title("C  How divided each map is", fontsize=9); ax.spines[["top", "right"]].set_visible(False)
fig.text(0.01, 0.01, "DRAFT 20 Nov: numbers subject to the G1c yield check and the G14 hand checks. Red = Republican, blue = Democrat, purple = cross-party tie.", fontsize=7, color="#a00")
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig("Martin/figures/figure1_draft.png", dpi=200); fig.savefig("Martin/figures/figure1_draft.pdf")
print("written Martin/figures/figure1_draft.png")
