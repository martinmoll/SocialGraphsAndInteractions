"""A3.6 and A3.7: flags and tie weights on every press mention, written as mentions_press.parquet.

Run from Anas/ after press_layer.py and bills.py:
    python a3/flags.py --press press_releases --repo <project/ of the group repo>

One row per colleague counted in a release (decision 1: once per release), from the `shared + press layer` hits
with status counted. The shared columns of mentions.parquet (WORK_AND_DEADLINES section 3) come first:
  speaker, named, source (= press), date, doc_id (= release URL), context (of the first mention), is_yield (False)
then
  how, rule_set, layer_rule   the rule of the first mention (see press_layer.py)
  in_shared                   Martin's matcher alone (match_shared.py) also counts this pair: the robustness row
  speaker_party, named_party, cross_party (R-D pairs only), same_state
  named_is_leader             decision 2: the seven leaders in leaders.csv (house.gov/leadership, read 21 Nov)
  co_lead                     the named member is sponsor or original cosponsor of a bill the release cites (A3.5)
  named_bill_role             their best role on those bills: sponsor, original cosponsor, later cosponsor, none
  release_has_bill            the release cites at least one resolved bill
  first_named, in_list        first colleague named in the release; found inside a list of names
  n_named, weight             colleagues counted in the release, and 1 / n_named (decision 8)
  caucus, redistricting       the release names a caucus / is about redistricting (word lists below, decision 6)
  template, shared_text       A3.1 flags (template posts are already left out of the counted hits)
  item_type, listed           from the collector

Decision 6 word lists, fixed 21 Nov before A4 compares any groups (A3_PLAN.md):
"""
import argparse
import os
import re
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HITS, OUT, load_inputs

CAUCUS = ["Problem Solvers Caucus", "Blue Dog", "Freedom Caucus", "Congressional Black Caucus",
          "Congressional Hispanic Caucus", "Hispanic Conference", "Progressive Caucus", "New Democrat Coalition",
          "Republican Study Committee", "Main Street Caucus", "Asian Pacific American Caucus", "Women's Caucus",
          "Bipartisan Caucus"]
REDISTRICTING = [r"redistrict\w*", r"gerrymander\w*", r"new (?:congressional )?map", r"congressional map\w*",
                 r"special session"]
CAUCUS_RX = re.compile("|".join(re.escape(c) for c in CAUCUS).replace("Women's", "Women[’']s"), re.I)
REDIST_RX = re.compile(r"\b(?:" + "|".join(REDISTRICTING) + r")\b", re.I)
__doc__ += f"  caucus: {CAUCUS}\n  redistricting: {REDISTRICTING}\n"
HERE = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--press", required=True)
    ap.add_argument("--repo", required=True)
    a = ap.parse_args()
    d, members, *_ = load_inputs(a.press, a.repo)
    m = members.set_index("bioguide")
    party, state = m.party, m.state
    leaders = pd.read_csv(os.path.join(HERE, "leaders.csv"))
    assert leaders.bioguide.isin(m.index).all(), "a leader is not in members.csv"

    L = pd.read_parquet(os.path.join(HITS, "press_hits_layer.parquet"))
    S = pd.read_parquet(os.path.join(HITS, "press_hits_shared.parquet"), columns=["doc_id", "named", "status"])
    shared_pairs = set(zip(S[S.status == "counted"].doc_id, S[S.status == "counted"].named))
    c = L[L.status == "counted"].sort_values(["doc_id", "start"])
    first_start = c.groupby("doc_id").start.min()
    M = c.drop_duplicates(["doc_id", "named"]).copy()          # first mention of each colleague in each release
    M["in_list"] = c.assign(lst=c.how.str.startswith("list") | c.layer_rule.isin(["list", "list across tags"])) \
        .groupby(["doc_id", "named"]).lst.any().reindex(list(zip(M.doc_id, M.named))).values

    # bills (A3.5)
    B = pd.read_csv(os.path.join(OUT, "release_bills.csv"))
    B = B[B.status == "resolved"]
    cos = pd.read_parquet(os.path.join(a.repo, "data", "processed", "cosponsors.parquet"))
    cos = cos[~cos.withdrawn]
    rank = {"sponsor": 3, "original cosponsor": 2, "later cosponsor": 1}
    best = {}
    bills_of = B.groupby("url").bill_id.apply(set).to_dict()
    sponsor_of = dict(zip(B.bill_id, B.sponsor))
    cos_role = {(b, x): ("original cosponsor" if o else "later cosponsor") for b, x, o in zip(cos.bill_id, cos.cosponsor, cos.original)}
    role_col = []
    for u, n in zip(M.doc_id, M.named):
        r = "none"
        for b in bills_of.get(u, ()):
            x = "sponsor" if sponsor_of.get(b) == n else cos_role.get((b, n), "none")
            if rank.get(x, 0) > rank.get(r, 0):
                r = x
        role_col.append(r)
    M["named_bill_role"] = role_col
    M["co_lead"] = M.named_bill_role.isin(["sponsor", "original cosponsor"])
    M["release_has_bill"] = M.doc_id.isin(bills_of)

    # parties, state, leaders, order, weights
    M["speaker_party"], M["named_party"] = M.speaker.map(party), M.named.map(party)
    rd = M.speaker_party.isin(["R", "D"]) & M.named_party.isin(["R", "D"])
    M["cross_party"] = (rd & (M.speaker_party != M.named_party)).astype("boolean")
    M.loc[~rd, "cross_party"] = pd.NA                          # independent (Kiley) on either end
    M["same_state"] = M.speaker.map(state) == M.named.map(state)
    M["named_is_leader"] = M.named.isin(set(leaders.bioguide))
    M["first_named"] = M.start.values == M.doc_id.map(first_start).values
    M["n_named"] = M.doc_id.map(M.groupby("doc_id").size())
    M["weight"] = 1 / M.n_named
    M["in_shared"] = [(u, n) in shared_pairs for u, n in zip(M.doc_id, M.named)]

    # release-level flags
    txt = dict(zip(d.url, d.text))
    title = dict(zip(d.url, d.title))
    rel = pd.DataFrame({"doc_id": M.doc_id.unique()})
    rel["caucus"] = [bool(CAUCUS_RX.search(txt[u] + " " + str(title[u]))) for u in rel.doc_id]
    rel["redistricting"] = [bool(REDIST_RX.search(txt[u] + " " + str(title[u]))) for u in rel.doc_id]
    M = M.merge(rel, on="doc_id", how="left")
    fl = pd.read_parquet(os.path.join(OUT, "release_flags.parquet")).set_index("url")
    M["shared_text"] = M.doc_id.map(fl.shared_text)

    cols = ["speaker", "named", "source", "date", "doc_id", "context", "is_yield", "how", "rule_set", "layer_rule",
            "in_shared", "speaker_party", "named_party", "cross_party", "same_state", "named_is_leader", "co_lead",
            "named_bill_role", "release_has_bill", "first_named", "in_list", "n_named", "weight", "caucus",
            "redistricting", "template", "shared_text", "item_type", "listed"]
    M = M[cols].reset_index(drop=True)
    path = os.path.join(OUT, "mentions_press.parquet")
    M.to_parquet(path, index=False, compression="zstd")

    print(f"mentions_press.parquet: {len(M):,} rows ({os.path.getsize(path) / 1e6:.1f} MB), {M.doc_id.nunique():,} releases, "
          f"{M.speaker.nunique()} speakers, {M.named.nunique()} named")
    print(f"cross-party (R-D rows): {M.cross_party.dropna().astype(bool).mean():.1%}; weighted by 1/n: "
          f"{(M.cross_party.fillna(False).astype(float) * M.weight)[M.cross_party.notna()].sum() / M.weight[M.cross_party.notna()].sum():.1%}")
    for f in ["in_shared", "same_state", "named_is_leader", "co_lead", "release_has_bill", "first_named", "in_list",
              "caucus", "redistricting", "shared_text"]:
        v = M[f].astype(bool)
        print(f"  {f:17s} {v.mean():6.1%}   cross-party among them {M.cross_party[v].dropna().astype(bool).mean():.1%}")
    print("named_bill_role:", M.named_bill_role.value_counts().to_dict())
    print(f"n_named: median {int(M.drop_duplicates('doc_id').n_named.median())}, releases naming 10+: "
          f"{(M.drop_duplicates('doc_id').n_named >= 10).mean():.1%}")
