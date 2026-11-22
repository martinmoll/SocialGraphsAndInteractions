"""Does the backbone centrality result depend on alpha? (22 Nov, after the alpha sweep)

Run from Anas/ after home_measures.py:  python a4/alpha_centrality.py
Repeats home_measures.py's N2 test exactly (same graph, same disparity filter, same measures, same within-party
shuffle of exposure with 10,000 shuffles and seed 2805, same Holm correction over the 10 tests) at several alpha
values. Only the backbone changes; cross-party degree on the full map is the same at every alpha and is kept so each
Holm family has the same 10 tests as the main run.
At alpha 0.005 the backbone is not connected (6 members lose every tie): networkx closeness then uses each member's
reachable part (Wasserman-Faust scaling), and members with no tie get betweenness and closeness 0.
Writes a4/out/alpha_centrality.csv.
"""
import os

import networkx as nx
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ANAS = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")
SEED, N_PERM = 2805, 10_000
ALPHAS = (0.005, 0.01, 0.02, 0.05, 0.1, 0.2)

t = pd.read_csv(os.path.join(OUT, "member_shares.csv"), index_col=0)
party, exposed = t.party.to_dict(), t.exposed.to_dict()
M = pd.read_parquet(os.path.join(ANAS, "a3", "out", "mentions_press.parquet"))
m = M[M.speaker.isin(t.index) & M.named.isin(t.index) & ~M.named_is_leader]
m = m.assign(a=m[["speaker", "named"]].min(axis=1), b=m[["speaker", "named"]].max(axis=1))
w = m.groupby(["a", "b"]).weight.sum().reset_index()
G = nx.Graph()
G.add_nodes_from(t.index)
G.add_weighted_edges_from(w[["a", "b", "weight"]].itertuples(index=False))
s, k = dict(G.degree(weight="weight")), dict(G.degree())
alpha_of = {(u, v): min(((1 - d["weight"] / s[z]) ** (k[z] - 1) if k[z] > 1 else 1.0) for z in (u, v))
            for u, v, d in G.edges(data=True)}
nodes = list(t.index)
x = np.array([exposed[n] for n in nodes], dtype=bool)
pty = np.array([party[n] for n in nodes])
cross = np.array([sum(party[v] != party[n] for v in G[n]) for n in nodes], dtype=float)


def perm_gap(vals):
    """As home_measures.perm_gap: exposed minus safe mean per party, two-sided p from shuffling exposure in party."""
    r = np.random.default_rng(SEED)
    out = {}
    for p in ("R", "D"):
        ix = pty == p
        v, e = vals[ix], x[ix]
        obs = v[e].mean() - v[~e].mean()
        null = np.array([(lambda ee: v[ee].mean() - v[~ee].mean())(r.permutation(e)) for _ in range(N_PERM)])
        out[p] = (obs, (np.abs(null) >= abs(obs) - 1e-15).mean(), v[e].mean(), v[~e].mean())
    return out


def holm(p):
    p = np.maximum(p, 1 / N_PERM)
    order, run, adj = np.argsort(p), 0.0, np.empty(len(p))
    for r, i in enumerate(order):
        run = max(run, min(1.0, (len(p) - r) * p[i]))
        adj[i] = run
    return adj


rows = []
for al in ALPHAS:
    B = nx.Graph()
    B.add_nodes_from(G)
    B.add_edges_from(e for e, a_ in alpha_of.items() if a_ < al)
    deg = np.array([B.degree(n) for n in nodes], dtype=float)
    btw_d = nx.betweenness_centrality(B, normalized=True)
    clo_d = nx.closeness_centrality(B)
    btw = np.array([btw_d[n] for n in nodes])
    clo = np.array([clo_d[n] for n in nodes])
    resid = np.empty(len(nodes))
    for p in ("R", "D"):
        ix = pty == p
        yv, xv = np.log(btw[ix] + 1e-6), np.log(np.maximum(deg[ix], 1))
        b1, b0 = np.polyfit(xv, yv, 1)
        resid[ix] = yv - (b0 + b1 * xv)
    part = []
    for name, vals in [("degree (backbone)", deg), ("cross-party degree (full map)", cross),
                       ("betweenness (backbone)", btw), ("closeness (backbone)", clo),
                       ("betweenness given degree (residual)", resid)]:
        g = perm_gap(vals)
        for p in ("R", "D"):
            obs, pv, me, ms = g[p]
            part.append(dict(alpha=al, ties=B.number_of_edges(), components=nx.number_connected_components(B),
                             measure=name, party=p, exposed_mean=me, safe_mean=ms, gap=obs, p=pv,
                             ratio=me / ms if ms and "residual" not in name else np.nan))
    part = pd.DataFrame(part)
    part["p_holm"] = holm(part.p.values)
    rows.append(part)
    print(f"alpha {al}: {B.number_of_edges()} ties, {nx.number_connected_components(B)} component(s)")
R = pd.concat(rows, ignore_index=True)
R.to_csv(os.path.join(OUT, "alpha_centrality.csv"), index=False)
pd.set_option("display.width", 200)
show = R[~R.measure.str.startswith("cross-party")].assign(cell=lambda d: d.apply(
    lambda r: f"{r.ratio:.2f} ({r.p_holm:.3f})" if pd.notna(r.ratio) else f"{r.gap:+.2f} ({r.p_holm:.3f})", axis=1))
print("\nexposed / safe ratio (Holm p); residual: gap (Holm p)")
print(show.pivot_table(index=["measure", "party"], columns="alpha", values="cell", aggfunc="first").to_string())
