"""A4 extension, addendum to HOME_NETWORK_PLAN.md: N1 null model, N2 centrality, N3 communities.

Run from Anas/ after a4/home_network.py:  python a4/home_measures.py
Design fixed before computing (HOME_NETWORK_PLAN.md, addendum). Writes a4/out/home_measures_*.csv.
"""
import os
import sys

import networkx as nx
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import home_network as H

OUT, ANAS = H.OUT, H.ANAS
SEED, N_PERM, N_REWIRE, SWAPS = 2805, 10_000, 1000, 10
ALPHA = 0.01

t = pd.read_csv(os.path.join(OUT, "member_shares.csv"), index_col=0)
party, exposed = t.party.to_dict(), t.exposed.to_dict()
M = pd.read_parquet(os.path.join(ANAS, "a3", "out", "mentions_press.parquet"))

# ---- the full weighted home map and its backbone (as figure_home_map.py)
m = M[M.speaker.isin(t.index) & M.named.isin(t.index) & ~M.named_is_leader]
m = m.assign(a=m[["speaker", "named"]].min(axis=1), b=m[["speaker", "named"]].max(axis=1))
w = m.groupby(["a", "b"]).weight.sum().reset_index()
G = nx.Graph()
G.add_nodes_from(t.index)
G.add_weighted_edges_from(w[["a", "b", "weight"]].itertuples(index=False))
s, k = dict(G.degree(weight="weight")), dict(G.degree())
alpha = lambda u, v, x: min(((1 - x / s[z]) ** (k[z] - 1) if k[z] > 1 else 1.0) for z in (u, v))
B = nx.Graph()
B.add_nodes_from(G)
B.add_edges_from((u, v) for u, v, d in G.edges(data=True) if alpha(u, v, d["weight"]) < ALPHA)
nodes = list(t.index)
x = np.array([exposed[n] for n in nodes], dtype=bool)
pty = np.array([party[n] for n in nodes])
rng = np.random.default_rng(SEED)


def perm_gap(vals, n_perm=N_PERM, seed=SEED):
    """Exposed minus safe mean per party, two-sided p from shuffling exposure within party."""
    r = np.random.default_rng(seed)
    out = {}
    for p in ("R", "D"):
        ix = pty == p
        v, e = vals[ix], x[ix]
        obs = v[e].mean() - v[~e].mean()
        null = np.empty(n_perm)
        for i in range(n_perm):
            ee = r.permutation(e)
            null[i] = v[ee].mean() - v[~ee].mean()
        out[p] = (obs, (np.abs(null) >= abs(obs) - 1e-15).mean(), v[e].mean(), v[~e].mean())
    return out


# ---- N1: degree-preserving rewiring of the cross-party ties
row, pairs, U, D = H.run(t, M, "main")
r_end = np.where(pty[U[:, 0]] == "R", U[:, 0], U[:, 1])
d_end = np.where(pty[U[:, 0]] == "R", U[:, 1], U[:, 0])
E = len(U)
obs_S2 = np.mean(x[r_end] & x[d_end])
obs_S1 = H.assort_binary(r_end, d_end, x)
S2s, S1s = np.empty(N_REWIRE), np.empty(N_REWIRE)
for i in range(N_REWIRE):
    R_, D_ = r_end.copy(), d_end.copy()
    present = set(zip(R_.tolist(), D_.tolist()))
    a_idx = rng.integers(0, E, SWAPS * E)
    b_idx = rng.integers(0, E, SWAPS * E)
    for a, b in zip(a_idx, b_idx):
        r1, d1, r2, d2 = R_[a], D_[a], R_[b], D_[b]
        if a == b or d1 == d2 or (r1, d2) in present or (r2, d1) in present:
            continue
        present.discard((r1, d1)); present.discard((r2, d2))
        present.add((r1, d2)); present.add((r2, d1))
        D_[a], D_[b] = d2, d1
    S2s[i] = np.mean(x[R_] & x[D_])
    S1s[i] = H.assort_binary(R_, D_, x)
n1 = dict(S2_observed=obs_S2, S2_rewired_mean=S2s.mean(), S2_rewired_lo=np.percentile(S2s, 2.5),
          S2_rewired_hi=np.percentile(S2s, 97.5), S2_ratio=obs_S2 / S2s.mean(),
          p_S2=(np.abs(S2s - S2s.mean()) >= abs(obs_S2 - S2s.mean())).mean(),
          S1_observed=obs_S1, S1_rewired_mean=S1s.mean(), p_S1=(np.abs(S1s - S1s.mean()) >= abs(obs_S1 - S1s.mean())).mean())
pd.DataFrame([n1]).to_csv(os.path.join(OUT, "home_measures_null.csv"), index=False)
print(f"N1 rewiring ({N_REWIRE} x {SWAPS} swaps/tie): S2 observed {obs_S2:.3f}, rewired {S2s.mean():.3f} "
      f"[{n1['S2_rewired_lo']:.3f}, {n1['S2_rewired_hi']:.3f}], ratio {n1['S2_ratio']:.2f}, p {n1['p_S2']:.3f}; "
      f"S1 observed {obs_S1:+.3f}, rewired {S1s.mean():+.3f}, p {n1['p_S1']:.3f}")

# ---- N2: centrality on the backbone (degree, betweenness, closeness) and cross-party degree on the full map
deg = np.array([B.degree(n) for n in nodes], dtype=float)
cross = np.array([sum(party[v] != party[n] for v in G[n]) for n in nodes], dtype=float)
btw_d = nx.betweenness_centrality(B, normalized=True)
clo_d = nx.closeness_centrality(B)
btw = np.array([btw_d[n] for n in nodes])
clo = np.array([clo_d[n] for n in nodes])
resid = np.empty(len(nodes))
for p in ("R", "D"):
    ix = pty == p
    yv, xv = np.log(btw[ix] + 1e-6), np.log(deg[ix])
    b1, b0 = np.polyfit(xv, yv, 1)
    resid[ix] = yv - (b0 + b1 * xv)
rows = []
for name, vals in [("degree (backbone)", deg), ("cross-party degree (full map)", cross), ("betweenness (backbone)", btw),
                   ("closeness (backbone)", clo), ("betweenness given degree (residual)", resid)]:
    g = perm_gap(vals)
    for p in ("R", "D"):
        obs, pv, me, ms = g[p]
        rows.append(dict(measure=name, party=p, exposed_mean=me, safe_mean=ms, gap=obs, p=pv,
                         ratio=me / ms if ms not in (0,) and name != "betweenness given degree (residual)" else np.nan))
N2 = pd.DataFrame(rows)
# Holm correction over the 10 tests (5 measures x 2 parties); p = 0 means none of 10,000 shuffles -> use 1/10,000
pv = np.maximum(N2.p.values, 1 / N_PERM)
order, run, adj = np.argsort(pv), 0.0, np.empty(len(pv))
for r, i in enumerate(order):
    run = max(run, min(1.0, (len(pv) - r) * pv[i]))
    adj[i] = run
N2["p_holm"] = adj
N2.to_csv(os.path.join(OUT, "home_measures_centrality.csv"), index=False)
cv = pd.Series(clo).groupby(pty).agg(["mean", "std", "min", "max"])
print(f"\nN2 centrality, backbone alpha {ALPHA}: {B.number_of_edges()} ties; closeness spread by party:\n{cv.round(3)}")
print(N2.round(4).to_string(index=False))

# ---- N3: Louvain communities on the full weighted map
best, bestQ = None, -1
for sd in range(50):
    c = nx.community.louvain_communities(G, weight="weight", resolution=1, seed=sd)
    q = nx.community.modularity(G, c, weight="weight")
    if q > bestQ:
        best, bestQ = c, q
comm = {n: i for i, c in enumerate(best) for n in c}
from sklearn.metrics import normalized_mutual_info_score as nmi
lab = [comm[n] for n in nodes]
party_parts = [set(n for n in nodes if party[n] == p) for p in ("R", "D")]
Qparty_w = nx.community.modularity(G, party_parts, weight="weight")
Qparty_u = nx.community.modularity(G, party_parts, weight=None)
other_share = np.array([np.mean([party[v] != party[n] for v in best[comm[n]] if v != n]) for n in nodes])
g3 = perm_gap(other_share)
comp = pd.DataFrame([dict(community=i, size=len(c), R=sum(party[n] == "R" for n in c), D=sum(party[n] == "D" for n in c),
                          exposed=sum(exposed[n] for n in c)) for i, c in enumerate(best)]).sort_values("size", ascending=False)
comp.to_csv(os.path.join(OUT, "home_measures_communities.csv"), index=False)
# members of each community, read by figure_home_map.py (written here since the 22 Nov rerun; on 21 Nov this file was
# made by hand from the same partition, so it went stale when the data changed)
lean_names = pd.read_csv(os.path.join(ANAS, "district_lean", "member_lean.csv")).set_index("bioguide")
pd.DataFrame([dict(community=comm[n], bioguide=n, name=lean_names.at[n, "name"], party=party[n],
                   state=lean_names.at[n, "state"], exposed=bool(exposed[n])) for n in nodes]) \
    .sort_values(["community", "party", "name"]).to_csv(os.path.join(OUT, "home_communities_members.csv"), index=False)
print(f"\nN3 Louvain (50 seeds, best Q): {len(best)} communities, modularity {bestQ:.3f}; NMI with party "
      f"{nmi(pty, lab):.3f}; party split Q weighted {Qparty_w:.3f}, unweighted {Qparty_u:.3f}")
print(comp.to_string(index=False))
for p in ("R", "D"):
    obs, pv, me, ms = g3[p]
    print(f"  {p}: share of own community from the other party: exposed {me:.3f}, safe {ms:.3f}, gap {obs:+.3f}, p {pv:.4f}")
pd.DataFrame([dict(party=p, exposed=g3[p][2], safe=g3[p][3], gap=g3[p][0], p=g3[p][1]) for p in ("R", "D")]) \
    .assign(n_communities=len(best), modularity=bestQ, nmi_party=nmi(pty, lab), Q_party_weighted=Qparty_w,
            Q_party_unweighted=Qparty_u).to_csv(os.path.join(OUT, "home_measures_community_position.csv"), index=False)
