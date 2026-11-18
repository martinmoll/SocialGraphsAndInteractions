"""M3: the numbers behind the three definitions the group fixes on 18 November.

Run from project/:  python Martin/m3_definitions.py        (about a quarter of an hour: the rewirings)
Reads Martin/mentions.parquet, data/processed/ and Diego's labelled matches. Writes Martin/m3_table.csv.

  1. A phrase-based yield rule, tested against the 150 correct rows Diego's D1 labelled as yield or other.
  2. The prototype's table (prototype_two_maps.ipynb, sections 3 and 4) on the new mentions, with the
     floor map under each yield rule and the working map under each thinning rule.

Everything not named here is as in the prototype: bill types hr and hjres, withdrawn cosponsorships
removed, undirected unweighted ties, degree-preserving rewiring with 5 swaps per tie, seed 2805.
"""
import re
import numpy as np, pandas as pd, networkx as nx
from matcher import Matcher

DATA, SEED = "data/processed", 2805
ALPHA, SWAPS_PER_TIE, N_REWIRE, N_REWIRE_DENSE = 0.05, 5, 200, 20
MIN_TURN_WORDS = 50
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- 1. the phrase-based yield rule
TITLE_DOT = re.compile(r"\b(Mr|Ms|Mrs|Rep|Dr|Messrs)\.")
YIELD_TO = re.compile(r"\byield(?:s|ed)?\b(?!\s+(?:back|myself))[^.;?!]*$", re.I)     # "... yield 2 minutes to the gentleman from Texas ("
FOR_YIELDING = re.compile(r"^[^.;?!]*\bfor\s+yielding", re.I)                          # ") for yielding"

def yield_phrase(text, a, b):
    """True when the name at text[a:b] is the member yielded to, or the member thanked for yielding:
    "yield" (not "yield back", not "yield myself") earlier in the same sentence, or "for yielding" later in it."""
    before, after = TITLE_DOT.sub(r"\1", text[max(0, a - 200):a]), TITLE_DOT.sub(r"\1", text[b:b + 120])
    return bool(YIELD_TO.search(before) or FOR_YIELDING.search(after))

L = pd.read_csv("Diego/d1_matcher_precision/labels.csv")
L = L[L.verdict == "correct"]
L = L.assign(phrase=[yield_phrase(c.replace("[[", "").replace("]]", ""), c.index("[["), c.index("]]") - 2) for c in L.wide_context])
print("== Yield rules against D1's labels (150 correct matches: 30 yields, 120 other) ==")
for name, flag in (("window: 'yield' within 60 characters", L.is_yield), ("phrase", L.phrase)):
    hit = (flag & (L.kind == "yield")).sum()
    print(f"{name:40s} finds {hit} of 30 yields (recall {hit / 30:.0%}); {hit} of its {flag.sum()} flags are yields (precision {hit / flag.sum():.0%})")

# ---------------------------------------------------------------- the mentions, with the phrase flag added
members_all = pd.read_csv(f"{DATA}/members.csv")
speeches = pd.read_parquet(f"{DATA}/speeches.parquet")
matcher = Matcher(members_all)
turns = speeches[(speeches.section == "H") & (speeches.n_words >= MIN_TURN_WORDS) & speeches.bioguide.isin(members_all.bioguide)]
flags = [(t.bioguide, h.named, yield_phrase(t.text, h.start, h.end)) for t in turns.itertuples()
         for h in matcher.find(t.text) if h.named and h.named != t.bioguide]
M = pd.read_parquet("Martin/mentions.parquet")
M["is_yield"] = M.is_yield_window   # since 18 Nov is_yield holds the phrase rule; this script compares the two
assert [f[:2] for f in flags] == list(zip(M.speaker, M.named)), "mentions.parquet is not what build_mentions.py writes"
M["is_yield_phrase"] = [f[2] for f in flags]

members = members_all[members_all.party.isin(["R", "D"])].set_index("bioguide")
party = members.party
M = M[M.speaker.isin(members.index) & M.named.isin(members.index)]
print(f"\n{len(M):,} mentions between Republicans and Democrats. Flagged as yields: window {M.is_yield.sum():,} ({M.is_yield.mean():.1%}), "
      f"phrase {M.is_yield_phrase.sum():,} ({M.is_yield_phrase.mean():.1%}), both {(M.is_yield & M.is_yield_phrase).sum():,}")
cross = party[M.speaker].values != party[M.named].values
for name, flag in (("window", M.is_yield), ("phrase", M.is_yield_phrase)):
    print(f"cross-party share of mentions flagged by the {name} rule: {cross[flag.values].mean():.1%}; of the rest: {cross[~flag.values].mean():.1%}")

# ---------------------------------------------------------------- 2. the maps (as in the prototype)
def graph(a, b):
    """Undirected graph on all 450 members; weight = number of times the pair occurs."""
    df = pd.DataFrame({"a": np.minimum(a, b), "b": np.maximum(a, b)}).value_counts()
    G = nx.Graph(); G.add_nodes_from(members.index)
    G.add_weighted_edges_from((u, v, int(w)) for (u, v), w in df.items())
    return G

def backbone(G, alpha):
    """Disparity filter: keep a tie if it is surprisingly strong for either member."""
    H = nx.Graph(); H.add_nodes_from(G)
    for u in G:
        k, s = G.degree(u), G.degree(u, weight="weight")
        if k < 2: continue
        for v in G[u]:
            if (1 - G[u][v]["weight"] / s) ** (k - 1) < alpha: H.add_edge(u, v, weight=G[u][v]["weight"])
    return H

def keep(G, n, by_weight):
    """n ties of G: the strongest (equal weights broken at random), or n at random."""
    e = pd.DataFrame([(u, v, d["weight"]) for u, v, d in G.edges(data=True)], columns=["u", "v", "w"]).assign(r=rng.random(G.number_of_edges()))
    e = e.sort_values(["w", "r"] if by_weight else ["r"], ascending=False).head(n)
    H = nx.Graph(); H.add_nodes_from(G); H.add_weighted_edges_from(e[["u", "v", "w"]].itertuples(index=False))
    return H, int(e.w.min())

def floor(rows):
    return graph(rows.speaker.values, rows.named.values)

bills = pd.read_parquet(f"{DATA}/bills.parquet")
cosponsors = pd.read_parquet(f"{DATA}/cosponsors.parquet")
links = cosponsors[~cosponsors.withdrawn].merge(bills[bills.type.isin(("hr", "hjres"))][["bill_id", "sponsor"]], on="bill_id")
links = links[links.cosponsor.isin(members.index) & links.sponsor.isin(members.index) & (links.cosponsor != links.sponsor)]
work = graph(links.cosponsor.values, links.sponsor.values)

F_all, F_win, F_phr = floor(M), floor(M[~M.is_yield]), floor(M[~M.is_yield_phrase])
top_all, cut_all = keep(work, F_all.number_of_edges(), True)
top_phr, cut_phr = keep(work, F_phr.number_of_edges(), True)
LAYERS = {
    "Floor: all mentions":                              F_all,
    "Floor: yields dropped, window rule":               F_win,
    "Floor: yields dropped, phrase rule":               F_phr,
    "Floor: phrase yields and leadership titles dropped": floor(M[~M.is_yield_phrase & ~M.is_leader_title]),
    "Working: all ties":                                work,
    "Working: backbone alpha 0.05":                     backbone(work, ALPHA),
    "Working: strongest, size of floor (all)":          top_all,
    "Working: strongest, size of floor (phrase)":       top_phr,
    "Working: random ties, size of floor (all)":        keep(work, F_all.number_of_edges(), False)[0],
}
print(f"\ncosponsorships used: {len(links):,} on {links.bill_id.nunique():,} bills. "
      f"'Strongest' keeps ties on at least {cut_all} bills (size of floor, all) and {cut_phr} bills (size of floor, phrase)")

SIDES = [set(party.index[party == "R"]), set(party.index[party == "D"])]
def stats(G):
    return nx.community.modularity(G, SIDES, weight=None), np.mean([party[u] != party[v] for u, v in G.edges()])

rows = []
for name, G in LAYERS.items():
    q, c = stats(G); m = G.number_of_edges(); null = []
    for s in range(N_REWIRE_DENSE if G is work else N_REWIRE):
        R = G.copy(); nx.double_edge_swap(R, nswap=SWAPS_PER_TIE * m, max_tries=200 * SWAPS_PER_TIE * m, seed=SEED + s)
        null.append(stats(R))
    null = np.array(null)
    rows.append({"map": name, "ties": m, "members with a tie": sum(d > 0 for _, d in G.degree()), "cross-party share": c,
                 "after rewiring": null[:, 1].mean(), "ratio": c / null[:, 1].mean(), "party Q": q,
                 "null Q mean": null[:, 0].mean(), "null Q max": null[:, 0].max(), "rewirings": len(null)})
    print(f"done: {name}", flush=True)
T = pd.DataFrame(rows).set_index("map")
T.round(4).to_csv("Martin/m3_table.csv")
pd.set_option("display.width", 250)
print("\n" + T.round(3).to_string())
