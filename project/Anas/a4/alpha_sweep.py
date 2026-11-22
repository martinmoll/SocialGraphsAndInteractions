"""How the disparity-filter alpha of the home map was checked (22 Nov): the same graph and filter as
figure_home_map.py and home_measures.py, at a range of alpha values.

Run from Anas/:  python a4/alpha_sweep.py
Prints, for each alpha: ties kept, share of the total weight kept, cross-party ties, mean degree, density, the
largest component, the number of components and of members left with no tie. Writes a4/out/alpha_sweep.csv.
"""
import os, sys
import networkx as nx
import numpy as np
import pandas as pd

A = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t = pd.read_csv(os.path.join(A, "a4/out/member_shares.csv"), index_col=0)
M = pd.read_parquet(os.path.join(A, "a3/out/mentions_press.parquet"))
m = M[M.speaker.isin(t.index) & M.named.isin(t.index) & ~M.named_is_leader]
m = m.assign(a=m[["speaker", "named"]].min(axis=1), b=m[["speaker", "named"]].max(axis=1))
w = m.groupby(["a", "b"]).weight.sum().reset_index()
party, exposed = t.party.to_dict(), t.exposed.to_dict()
G = nx.Graph(); G.add_nodes_from(t.index); G.add_weighted_edges_from(w[["a", "b", "weight"]].itertuples(index=False))
s, k = dict(G.degree(weight="weight")), dict(G.degree())
al = {(u, v): min(((1 - d["weight"] / s[x]) ** (k[x] - 1) if k[x] > 1 else 1.0) for x in (u, v))
      for u, v, d in G.edges(data=True)}
tot_w = sum(d["weight"] for *_, d in G.edges(data=True))
rows = []
for a_ in (0.001, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 1.01):
    B = nx.Graph(); B.add_nodes_from(G)
    B.add_edges_from((u, v, G[u][v]) for (u, v), x in al.items() if x < a_)
    E = B.number_of_edges()
    cr = sum(party[u] != party[v] for u, v in B.edges())
    comps = sorted((len(c) for c in nx.connected_components(B)), reverse=True)
    iso = sum(1 for n in B if B.degree(n) == 0)
    wkept = sum(d["weight"] for *_, d in B.edges(data=True)) / tot_w
    rows.append(dict(alpha=a_ if a_ <= 1 else "none (full)", ties=E, share_of_ties=E / G.number_of_edges(),
                     weight_kept=wkept, cross=cr, cross_share=cr / max(E, 1), mean_degree=2 * E / B.number_of_nodes(),
                     density=nx.density(B), giant=comps[0], components=len(comps), isolates=iso))
pd.set_option("display.width", 200)
R = pd.DataFrame(rows)
R.round(4).to_csv(os.path.join(A, "a4/out/alpha_sweep.csv"), index=False)
print(R.round(3).to_string(index=False))
