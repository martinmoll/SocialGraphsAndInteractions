"""M5: Louvain communities on the two maps; how far they follow party, and how far the two maps agree.

Run from project/:  python Martin/m5_communities.py        (a few minutes)
Reads Martin/mentions.parquet and data/processed/. Writes Martin/m5_table.csv and Martin/m5_communities.csv.

Choices (Martin to confirm; each is a modelling choice):
  1. Maps as in M3 (m3_definitions.py): undirected, unweighted, Republicans and Democrats only. Floor headline =
     phrase-rule yields dropped (G1b); working = sponsor-cosponsor pairs on hr and hjres, withdrawn removed.
     Working map compared at full size, and as random draws at the floor's size (G1a).
  2. Louvain (networkx, resolution 1), unweighted. It is random, so it is run with 50 seeds per map; the table gives
     the mean and range over seeds and the partition with the highest modularity is kept. Alternative: weighted
     working ties (number of shared bills): reported as one robustness row.
  3. Nodes: members with at least one tie in that map. NMI with party is computed on those. NMI between two maps
     is computed on members with a tie in both.
  4. NMI = normalised mutual information (arithmetic mean, sklearn). 1 = the communities are the parties exactly
     (or the two maps' communities are the same); 0 = unrelated. Baseline: the same Louvain on a degree-preserving
     rewiring of each map (20 rewirings), so we can say how much NMI comes from structure, not from chance.
"""
import numpy as np, pandas as pd, networkx as nx
from sklearn.metrics import normalized_mutual_info_score as nmi

DATA, SEED, N_SEEDS, N_DRAWS, N_REWIRE = "data/processed", 2805, 50, 20, 20
rng = np.random.default_rng(SEED)

members = pd.read_csv(f"{DATA}/members.csv")
members = members[members.party.isin(["R", "D"])].set_index("bioguide")
party = members.party
M = pd.read_parquet("Martin/mentions.parquet")
M = M[M.speaker.isin(party.index) & M.named.isin(party.index)]

def graph(a, b, weighted=False):
    df = pd.DataFrame({"a": np.minimum(a, b), "b": np.maximum(a, b)}).value_counts()
    G = nx.Graph()
    G.add_weighted_edges_from((u, v, int(w) if weighted else 1) for (u, v), w in df.items())
    return G

bills = pd.read_parquet(f"{DATA}/bills.parquet")
cos = pd.read_parquet(f"{DATA}/cosponsors.parquet")
links = cos[~cos.withdrawn].merge(bills[bills.type.isin(("hr", "hjres"))][["bill_id", "sponsor"]], on="bill_id")
links = links[links.cosponsor.isin(party.index) & links.sponsor.isin(party.index) & (links.cosponsor != links.sponsor)]

floor = graph(M[~M.is_yield].speaker.values, M[~M.is_yield].named.values)
floor_all = graph(M.speaker.values, M.named.values)
work = graph(links.cosponsor.values, links.sponsor.values)
work_w = graph(links.cosponsor.values, links.sponsor.values, weighted=True)

def draw(G, n):
    e = list(G.edges()); idx = rng.choice(len(e), n, replace=False)
    H = nx.Graph(); H.add_edges_from(e[i] for i in idx); return H

def louvain(G, weight="weight"):
    """All seeds: (best partition as dict node -> community, list of (Q, n communities, NMI with party))."""
    runs, best, bestq = [], None, -1
    for s in range(N_SEEDS):
        C = nx.community.louvain_communities(G, weight=weight, seed=SEED + s)
        q = nx.community.modularity(G, C, weight=weight)
        lab = {v: i for i, c in enumerate(C) for v in c}
        nodes = list(G)
        runs.append((q, len(C), nmi([party[v] for v in nodes], [lab[v] for v in nodes])))
        if q > bestq: best, bestq = lab, q
    return best, np.array(runs)

def rewired_nmi(G):
    out = []
    for k in range(N_REWIRE):
        R = G.copy(); m = R.number_of_edges()
        nx.double_edge_swap(R, nswap=5 * m, max_tries=1000 * m, seed=SEED + k)
        C = nx.community.louvain_communities(R, seed=SEED + k)
        lab = {v: i for i, c in enumerate(C) for v in c}
        out.append(nmi([party[v] for v in R], [lab[v] for v in R]))
    return np.array(out)

MAPS = {"Floor: yields dropped (headline)": (floor, None), "Floor: all mentions": (floor_all, None),
        "Working: all ties": (work, None), "Working: all ties, weighted by shared bills": (work_w, "weight")}
rows, best = [], {}
for name, (G, w) in MAPS.items():
    lab, runs = louvain(G, weight=w)
    best[name] = lab
    base = rewired_nmi(G) if w is None and G is not work else np.array([np.nan])
    sizes = pd.Series(lab).value_counts()
    rows.append({"map": name, "members": G.number_of_nodes(), "ties": G.number_of_edges(),
                 "Louvain Q mean": runs[:, 0].mean(), "Q min": runs[:, 0].min(), "Q max": runs[:, 0].max(),
                 "communities (best)": len(sizes), "communities with 10+ members": int((sizes >= 10).sum()),
                 "NMI with party mean": runs[:, 2].mean(), "NMI min": runs[:, 2].min(), "NMI max": runs[:, 2].max(),
                 "NMI with party, rewired null mean": base.mean()})
    print("done:", name, flush=True)

# working map at the floor's size: N_DRAWS random draws, Louvain with 10 seeds each
n_floor, dr = floor.number_of_edges(), []
draw_labs = []
for d in range(N_DRAWS):
    H = draw(work, n_floor)
    C = max((nx.community.louvain_communities(H, seed=SEED + s) for s in range(10)), key=lambda C: nx.community.modularity(H, C))
    lab = {v: i for i, c in enumerate(C) for v in c}; draw_labs.append(lab)
    dr.append((nx.community.modularity(H, C), len(C), nmi([party[v] for v in H], [lab[v] for v in H])))
dr = np.array(dr)
rows.append({"map": f"Working: random draws at floor size ({N_DRAWS} draws)", "members": np.nan, "ties": n_floor,
             "Louvain Q mean": dr[:, 0].mean(), "Q min": dr[:, 0].min(), "Q max": dr[:, 0].max(),
             "communities (best)": np.nan, "communities with 10+ members": np.nan,
             "NMI with party mean": dr[:, 2].mean(), "NMI min": dr[:, 2].min(), "NMI max": dr[:, 2].max(),
             "NMI with party, rewired null mean": np.nan})
T = pd.DataFrame(rows).set_index("map")

# between maps
def between(a, b):
    common = sorted(set(a) & set(b)); return nmi([a[v] for v in common], [b[v] for v in common]), len(common)
f, w = best["Floor: yields dropped (headline)"], best["Working: all ties"]
nm, n_common = between(f, w)
draw_between = np.array([between(f, l)[0] for l in draw_labs])
# what NMI the floor would have with the working map if its communities were the parties exactly
party_only = {v: party[v] for v in f}
nm_party, _ = between(party_only, w)
print(f"\nNMI floor (headline) vs working (all ties): {nm:.3f} on {n_common} members "
      f"| floor vs working draws at floor size: {draw_between.mean():.3f} ({draw_between.min():.3f} to {draw_between.max():.3f}) "
      f"| party labels vs working: {nm_party:.3f}")
T.loc["Between: floor headline vs working all ties", "NMI with party mean"] = np.nan
T["note"] = ""
T.loc["Between: floor headline vs working all ties", "note"] = (f"NMI {nm:.3f} on {n_common} members; vs working draws at floor size "
    f"{draw_between.mean():.3f} ({draw_between.min():.3f}-{draw_between.max():.3f}); party labels vs working {nm_party:.3f}")
T.round(4).to_csv("Martin/m5_table.csv")

# composition of the best partitions, for the text and Figure 1
comp = []
for name in ("Floor: yields dropped (headline)", "Working: all ties"):
    lab = pd.Series(best[name])
    for c, g in lab.groupby(lab):
        comp.append({"map": name, "community": c, "members": len(g), "R": int((party[g.index] == "R").sum()),
                     "D": int((party[g.index] == "D").sum())})
C = pd.DataFrame(comp).sort_values(["map", "members"], ascending=[True, False])
pd.DataFrame([{"bioguide": v, "map": name, "community": c} for name in ("Floor: yields dropped (headline)", "Working: all ties")
              for v, c in best[name].items()]).to_csv("Martin/m5_communities.csv", index=False)
pd.set_option("display.width", 250)
print("\n" + T.drop(columns="note").round(3).to_string())
print("\nCommunities with 10+ members (best partition):")
print(C[C.members >= 10].to_string(index=False))
