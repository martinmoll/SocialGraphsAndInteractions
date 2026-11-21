"""A3.7: the named examples and mutual pairs (A3_PLAN step A3.7), read against mentions_press.parquet.

Run from Anas/ after flags.py:  python a3/examples.py --press press_releases --repo <repo>

The examples come from the pilot (13 to 18 Nov, pilot name rules, 10 to 20 releases per member):
  pairs        Roy -> Cohen, Biggs -> Jayapal
  members      Lawler (1 of 10 pilot releases named the other side), Bacon (8 of 10)
  mutual       Golden <-> Lawler, Golden <-> Fitzpatrick, Kaptur <-> Fitzpatrick
For each pair: releases by A naming B and by B naming A, with how many of them are co-lead links, and one context.
For each member: releases, and the A4 outcome (share of releases naming the other party, co-leads and leaders
left out), plain and with co-leads kept. Writes out/named_examples.csv.
"""
import argparse
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import OUT, load_inputs

PAIRS = [("Roy", "Cohen"), ("Biggs", "Jayapal"), ("Golden", "Lawler"), ("Golden", "Fitzpatrick"), ("Kaptur", "Fitzpatrick")]
MEMBERS = ["Lawler", "Bacon", "Golden", "Fitzpatrick", "Kaptur", "Roy", "Biggs"]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--press", required=True)
    ap.add_argument("--repo", required=True)
    a = ap.parse_args()
    d, members, *_ = load_inputs(a.press, a.repo)
    M = pd.read_parquet(os.path.join(OUT, "mentions_press.parquet"))
    m = members.set_index("bioguide")

    def bio(last):
        x = m[m["last"].str.lower() == last.lower()]
        if last == "Biggs":
            x = x[x.state == "AZ"]
        assert len(x) == 1, (last, x.index.tolist())
        return x.index[0]
    rows = []
    print("pairs (releases naming the other, of them co-lead):")
    for A, Bn in PAIRS:
        a_, b_ = bio(A), bio(Bn)
        for s, t, sn, tn in [(a_, b_, A, Bn), (b_, a_, Bn, A)]:
            x = M[(M.speaker == s) & (M.named == t)]
            ctx = x.context.iloc[0][:200].replace("\n", " ") if len(x) else ""
            rows.append(dict(kind="pair", who=f"{sn} -> {tn}", releases=len(x), co_lead=int(x.co_lead.sum()),
                             example=ctx, example_url=x.doc_id.iloc[0] if len(x) else ""))
            print(f"  {sn:12s} -> {tn:12s} {len(x):4d} (co-lead {int(x.co_lead.sum())})  {ctx[:110]}")
    print("\nmembers: releases; share naming the other party (A4 outcome: co-leads and leaders left out | co-leads kept)")
    for last in MEMBERS:
        b = bio(last)
        rel = d[d.bioguide == b].url
        x = M[(M.speaker == b) & M.cross_party.fillna(False).astype(bool) & ~M.named_is_leader]
        out = x[~x.co_lead].doc_id.nunique() / len(rel)
        kept = x.doc_id.nunique() / len(rel)
        rows.append(dict(kind="member", who=last, releases=len(rel), share_other_party=round(out, 3),
                         share_with_coleads=round(kept, 3)))
        print(f"  {last:12s} ({m.at[b, 'party']}) {len(rel):5d} releases; {out:.1%} | {kept:.1%}")
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "named_examples.csv"), index=False)
