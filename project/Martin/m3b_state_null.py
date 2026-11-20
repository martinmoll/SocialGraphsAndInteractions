"""M3b: the state null as a robustness row for part 1 (Anas's proposal, accepted by Martin 20 Nov; DECISIONS G16).

Run from project/:  python Martin/m3b_state_null.py        (about 10 minutes)
Writes Martin/m3b_state_null.csv.

The null: rewire each map so that every member keeps their number of ties AND their number of ties to members of
their own state. Same-state ties are swapped only with same-state ties of that state; ties between states only
with ties between states, never creating a same-state tie. The function is Anas's (Anas/state_null/
state_null_pilot.py, reviewed by Martin with Claude 20 Nov), unchanged except for the number of draws: 200 for the
floor maps and 20 for the working map, as in M3. Maps as in m3_definitions.py.

Question it answers: is part of the party division just members tying to their own state's delegation, which is
often one party? If Q under this null stays near zero, state explains none of it.
"""
import random
import numpy as np, pandas as pd, networkx as nx

DATA, SEED, SWAPS = "data/processed", 2805, 5
members = pd.read_csv(f"{DATA}/members.csv")
members = members[members.party.isin(["R", "D"])].set_index("bioguide")
party, state = members.party, members.state
SIDES = [set(party.index[party == "R"]), set(party.index[party == "D"])]

def graph(a, b):
    G = nx.Graph(); G.add_nodes_from(party.index); G.add_edges_from((u, v) for u, v in zip(a, b) if u != v); return G

def describe(G):
    e = np.array(G.edges())
    same = state[e[:, 0]].values == state[e[:, 1]].values
    cross = party[e[:, 0]].values != party[e[:, 1]].values
    return dict(q=nx.community.modularity(G, SIDES, weight=None), cross=cross.mean(), same_state=same.mean())

def state_rewire(G, rng):
    """Anas's stratified double-edge swap."""
    strata = {}
    for u, v in G.edges():
        strata.setdefault(state[u] if state[u] == state[v] else "_between", []).append((u, v))
    have = set(frozenset(e) for e in G.edges())
    for key, E in strata.items():
        m = len(E)
        if m < 2: continue
        for _ in range(SWAPS * m * 3):
            i, j = rng.randrange(m), rng.randrange(m)
            (a, b), (c, d) = E[i], E[j]
            if rng.random() < 0.5: c, d = d, c
            n1, n2 = frozenset((a, d)), frozenset((c, b))
            if len({a, b, c, d}) < 4 or n1 in have or n2 in have: continue
            if key == "_between" and (state[a] == state[d] or state[c] == state[b]): continue
            have -= {frozenset((a, b)), frozenset((c, d))}; have |= {n1, n2}
            E[i], E[j] = (a, d), (c, b)
    R = nx.Graph(); R.add_nodes_from(G); R.add_edges_from(e for E in strata.values() for e in E); return R

M = pd.read_parquet("Martin/mentions.parquet")
M = M[M.speaker.isin(party.index) & M.named.isin(party.index)]
bills = pd.read_parquet(f"{DATA}/bills.parquet"); cos = pd.read_parquet(f"{DATA}/cosponsors.parquet")
L = cos[~cos.withdrawn].merge(bills[bills.type.isin(("hr", "hjres"))][["bill_id", "sponsor"]], on="bill_id")
L = L[L.cosponsor.isin(party.index) & L.sponsor.isin(party.index)]
MAPS = {"Floor: yields dropped (headline)": (graph(M[~M.is_yield].speaker, M[~M.is_yield].named), 200),
        "Floor: all mentions": (graph(M.speaker, M.named), 200),
        "Working: all ties": (graph(L.cosponsor, L.sponsor), 20)}
rows = []
for name, (G, n) in MAPS.items():
    obs = describe(G)
    S = pd.DataFrame([describe(state_rewire(G, random.Random(SEED + s))) for s in range(n)])
    assert np.allclose(S.same_state, obs["same_state"]), "the state null must keep the same-state share"
    rows.append({"map": name, "ties": G.number_of_edges(), "same-state share": obs["same_state"],
                 "party Q": obs["q"], "state null Q mean": S.q.mean(), "state null Q max": S.q.max(),
                 "cross-party share": obs["cross"], "state null cross mean": S.cross.mean(),
                 "draws at least as divided": int((S.q >= obs["q"]).sum()), "draws": n})
    print("done:", name, flush=True)
T = pd.DataFrame(rows).set_index("map")
T.round(4).to_csv("Martin/m3b_state_null.csv")
pd.set_option("display.width", 250); print(T.round(3).to_string())
