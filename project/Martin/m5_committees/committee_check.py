"""M5, follow-up: are the floor map's communities committees?

Run from project/:  python Martin/m5_committees/committee_check.py
Reads committee-membership-current.yaml and committees-current.yaml (unitedstates/congress-legislators, main
branch, downloaded 20 Nov 2026; current membership, so members who changed committees during the term are
placed on their current ones), Martin/mentions.parquet, Martin/m5_communities.csv.

Choices:
  1. Full House committees only (codes starting with H and four characters, e.g. HSAP); subcommittees ignored.
  2. A tie "shares a committee" if both members sit on at least one common full committee.
  3. Null: the same degree-preserving rewiring as M3 (5 swaps per tie, 200 rewirings for the floor, 20 for the
     working map). It keeps how many ties each member has, so busy committee leaders stay busy.
"""
import yaml, numpy as np, pandas as pd, networkx as nx
from pathlib import Path

HERE, SEED = Path(__file__).parent, 2805
members = pd.read_csv("data/processed/members.csv")
members = members[members.party.isin(["R", "D"])].set_index("bioguide")
names = {c["thomas_id"]: c["name"] for c in yaml.safe_load(open(HERE / "committees-current.yaml")) if c["type"] == "house"}
memb = yaml.safe_load(open(HERE / "committee-membership-current.yaml"))
comm = {}
for code, people in memb.items():
    if code.startswith("H") and len(code) == 4:
        for p in people:
            if p.get("bioguide") in members.index:
                comm.setdefault(p["bioguide"], set()).add(code)
print(f"{len(comm)} of {len(members)} members on at least one full House committee; {len({c for s in comm.values() for c in s})} committees")

def share(G):
    return np.mean([bool(comm.get(u, set()) & comm.get(v, set())) for u, v in G.edges()])

def null(G, n):
    out = []
    for k in range(n):
        R = G.copy(); m = R.number_of_edges()
        nx.double_edge_swap(R, nswap=5 * m, max_tries=1000 * m, seed=SEED + k); out.append(share(R))
    return np.array(out)

M = pd.read_parquet("Martin/mentions.parquet")
M = M[M.speaker.isin(members.index) & M.named.isin(members.index)]
def graph(a, b):
    G = nx.Graph(); G.add_edges_from(zip(a, b)); return G
bills = pd.read_parquet("data/processed/bills.parquet"); cos = pd.read_parquet("data/processed/cosponsors.parquet")
L = cos[~cos.withdrawn].merge(bills[bills.type.isin(("hr", "hjres"))][["bill_id", "sponsor"]], on="bill_id")
L = L[L.cosponsor.isin(members.index) & L.sponsor.isin(members.index) & (L.cosponsor != L.sponsor)]
party = members.party
F = graph(M[~M.is_yield].speaker, M[~M.is_yield].named)
W = graph(L.cosponsor, L.sponsor)
rows = []
for name, G, n in (("Floor: yields dropped (headline)", F, 200), ("Working: all ties", W, 20)):
    for side in ("all", "cross-party", "same party"):
        H = G if side == "all" else nx.Graph([(u, v) for u, v in G.edges() if (party[u] != party[v]) == (side == "cross-party")])
        obs = share(H)
        nl = null(G, n) if side == "all" else np.array([np.nan])
        rows.append({"map": name, "ties": side, "n ties": H.number_of_edges(), "share sharing a committee": obs,
                     "rewired null mean": nl.mean(), "null max": nl.max()})
T = pd.DataFrame(rows)
T.round(4).to_csv(HERE / "committee_table.csv", index=False)
print(T.round(3).to_string(index=False))

# each floor community: the committee most over-represented among its members
C = pd.read_csv("Martin/m5_communities.csv"); C = C[C["map"].str.startswith("Floor")]
base = pd.Series([c for s in comm.values() for c in s]).value_counts() / len(comm)
out = []
for k, g in C.groupby("community"):
    on = pd.Series([c for b in g.bioguide for c in comm.get(b, ())]).value_counts() / len(g)
    lift = (on / base).dropna()
    top = lift[on[lift.index] >= 0.25].sort_values(ascending=False).head(2)
    out.append({"community": k, "members": len(g), "R": int((party[g.bioguide] == "R").sum()), "D": int((party[g.bioguide] == "D").sum()),
                "top committee": "; ".join(f"{names.get(c, c)} ({on[c]:.0%} of members, {base[c]:.0%} of the House)" for c in top.index)})
O = pd.DataFrame(out).sort_values("members", ascending=False)
O.to_csv(HERE / "community_committees.csv", index=False)
print("\n" + O.to_string(index=False))
