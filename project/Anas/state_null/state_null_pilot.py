"""Pilot for Martin: how much of each map's party division could come from members of the same state.

Run from project/ (needs Martin/mentions.parquet):
    python Anas/state_null/state_null_pilot.py data/processed Martin/mentions.parquet

Maps are built as in Martin/m3_definitions.py: undirected, unweighted ties between Republicans and Democrats;
working = sponsor-cosponsor pairs on hr and hjres bills, withdrawn cosponsorships removed; floor = mentions with
phrase-rule yields dropped (the headline map, DECISIONS G1b). One run, a pilot: Martin's own code is the reference.

Two nulls, both keep every member's number of ties:
- plain:  degree-preserving rewiring, as in M3 (networkx double_edge_swap).
- state:  ties between two members of the same state are rewired only among same-state ties of that state;
          ties between states only among ties between states, never creating a same-state tie. So every member
          also keeps their number of same-state ties.
"""
import sys
import random
import numpy as np
import pandas as pd
import networkx as nx

DATA, MENTIONS = sys.argv[1], sys.argv[2]
SEED, SWAPS, N_FLOOR, N_WORK = 2805, 5, 50, 10

members = pd.read_csv(f"{DATA}/members.csv")
members = members[members.party.isin(["R", "D"])].set_index("bioguide")
party, state = members.party, members.state
SIDES = [set(party.index[party == "R"]), set(party.index[party == "D"])]


def graph(a, b):
    G = nx.Graph()
    G.add_nodes_from(members.index)
    G.add_edges_from((u, v) for u, v in zip(a, b) if u != v)
    return G


bills = pd.read_parquet(f"{DATA}/bills.parquet")
cos = pd.read_parquet(f"{DATA}/cosponsors.parquet")
links = cos[~cos.withdrawn].merge(bills[bills.type.isin(("hr", "hjres"))][["bill_id", "sponsor"]], on="bill_id")
links = links[links.cosponsor.isin(members.index) & links.sponsor.isin(members.index)]
M = pd.read_parquet(MENTIONS)
M = M[M.speaker.isin(members.index) & M.named.isin(members.index) & ~M.is_yield]
MAPS = {"working (all ties)": graph(links.cosponsor, links.sponsor), "floor (yields dropped)": graph(M.speaker, M.named)}


def describe(G):
    e = np.array(G.edges())
    same = state[e[:, 0]].values == state[e[:, 1]].values
    cross = party[e[:, 0]].values != party[e[:, 1]].values
    return dict(q=nx.community.modularity(G, SIDES, weight=None), cross=cross.mean(), same_state=same.mean(),
                cross_in_state=cross[same].mean(), cross_between=cross[~same].mean())


def state_rewire(G, rng):
    """Stratified double-edge swap: same-state ties within their state, between-state ties among themselves."""
    edges = [tuple(e) for e in G.edges()]
    strata = {}
    for u, v in edges:
        key = state[u] if state[u] == state[v] else "_between"
        strata.setdefault(key, []).append((u, v))
    have = set(frozenset(e) for e in edges)
    for key, E in strata.items():
        m = len(E)
        if m < 2:
            continue
        for _ in range(SWAPS * m * 3):          # tries, not successful swaps; rejected tries leave the map unchanged
            i, j = rng.randrange(m), rng.randrange(m)
            (a, b), (c, d) = E[i], E[j]
            if rng.random() < 0.5:
                c, d = d, c
            n1, n2 = frozenset((a, d)), frozenset((c, b))
            if len({a, b, c, d}) < 4 or n1 in have or n2 in have:
                continue
            if key == "_between" and (state[a] == state[d] or state[c] == state[b]):
                continue
            have -= {frozenset((a, b)), frozenset(E[j])}
            have |= {n1, n2}
            E[i], E[j] = (a, d), (c, b)
    R = nx.Graph()
    R.add_nodes_from(G)
    R.add_edges_from(e for E in strata.values() for e in E)
    return R


rows = []
for name, G in MAPS.items():
    obs = describe(G)
    n = N_WORK if name.startswith("working") else N_FLOOR
    plain, strat = [], []
    for s in range(n):
        R = G.copy()
        nx.double_edge_swap(R, nswap=SWAPS * R.number_of_edges(), max_tries=200 * SWAPS * R.number_of_edges(), seed=SEED + s)
        plain.append(describe(R))
        strat.append(describe(state_rewire(G, random.Random(SEED + s))))
    P, S = pd.DataFrame(plain), pd.DataFrame(strat)
    rows.append({"map": name, "ties": G.number_of_edges(), "draws": n,
                 "same-state share": obs["same_state"], "same-state, plain null": P.same_state.mean(),
                 "cross-party, same-state ties": obs["cross_in_state"],
                 "cross-party, between-state ties": obs["cross_between"],
                 "party Q": obs["q"], "Q plain null": P.q.mean(), "Q state null mean": S.q.mean(),
                 "Q state null max": S.q.max(), "cross-party share": obs["cross"],
                 "cross plain null": P.cross.mean(), "cross state null": S.cross.mean()})
    print("done", name, flush=True)

T = pd.DataFrame(rows).set_index("map").T
pd.set_option("display.width", 200)
print(T.round(3).to_string())
