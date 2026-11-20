"""A3.2: Martin's shared matcher, unchanged, on every press release (rule_set = "shared").

Run from Anas/:  python a3/match_shared.py --press press_releases --repo <project/ of the group repo>

Every hit is kept, with the reason it does or does not count (principle 4 of A3_PLAN.md: nothing is deleted):
  self            the member names themselves                     not a mention
  unresolved      matcher could not pin the name to one member   not a mention (reason in `how`)
  template        release is a House-wide template (A3.1)         not counted
  in_boilerplate  hit inside one of the member's repeated sentences (A3.1)   not counted
  counted         everything else
Context is cut with Martin's build_mentions.context(), so press and floor contexts look the same.

Writes press_hits_shared.parquet (to press_raw/a3_out/ on Anas's machine, else out/; see common.HITS): one row per hit, columns
  speaker, named, source, date, doc_id, context, is_yield, how, title_word, is_leader_title, rule_set,
  start, end, status, template, in_boilerplate, item_type, listed
"""
import argparse
import os
import re
import sys
import time

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import OUT, load_inputs, HITS
from prepare import SPLIT

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--press", required=True)
    ap.add_argument("--repo", required=True)
    a = ap.parse_args()
    t0 = time.time()
    d, members, Matcher, LEADER_TITLES, bm = load_inputs(a.press, a.repo)
    flags = pd.read_parquet(os.path.join(OUT, "release_flags.parquet")).set_index("url")
    rep = pd.read_csv(os.path.join(OUT, "repeated_sentences.csv"))
    repeated = rep.groupby("bioguide").sentence.apply(set).to_dict()
    mt = Matcher(members)

    rows = []
    for r in d.itertuples():
        hits = mt.find(r.text)
        if not hits:
            continue
        bounds = [0] + [m.end() for m in bm.SENT_END.finditer(r.text)]
        mine = repeated.get(r.bioguide, set())
        # sentence spans exactly as prepare.py split them, to test whether a hit sits in a repeated sentence
        spans = []
        if mine:
            pos = 0
            for m in list(SPLIT.finditer(r.text)) + [None]:
                end = m.start() if m else len(r.text)
                spans.append((pos, end, r.text[pos:end].strip()))
                pos = m.end() if m else end
        tpl = bool(flags.at[r.url, "template"])
        for h in hits:
            in_rep = any(s <= h.start < e and txt in mine for s, e, txt in spans)
            status = ("unresolved" if h.named is None else "self" if h.named == r.bioguide
                      else "template" if tpl else "in_boilerplate" if in_rep else "counted")
            rows.append(dict(speaker=r.bioguide, named=h.named, source="press", date=r.date, doc_id=r.url,
                             context=bm.context(r.text, bounds, h.start, h.end), is_yield=False, how=h.how,
                             title_word=h.title, is_leader_title=h.title in LEADER_TITLES, rule_set="shared",
                             start=h.start, end=h.end, status=status, template=tpl, in_boilerplate=in_rep,
                             item_type=r.item_type, listed=r.listed))
    H = pd.DataFrame(rows)
    H.to_parquet(os.path.join(HITS, "press_hits_shared.parquet"), index=False)

    c = H[H.status == "counted"]
    once = c.drop_duplicates(["doc_id", "named"])                        # decision 1: once per release
    party = members.set_index("bioguide").party
    print(f"releases {len(d):,}; hits {len(H):,} in {H.doc_id.nunique():,} releases ({time.time() - t0:.0f} s)")
    print("status:", H.status.value_counts().to_dict())
    print("unresolved by reason:", H[H.status == "unresolved"].how.value_counts().to_dict())
    print("counted, resolved by:", c.how.value_counts().to_dict())
    print(f"counted mentions {len(c):,}; once per release (decision 1) {len(once):,}; "
          f"releases naming another member {once.doc_id.nunique():,} ({once.doc_id.nunique() / len(d):.1%}); "
          f"speakers {once.speaker.nunique()}, named {once.named.nunique()}")
    rd = once[party.reindex(once.speaker).isin(["R", "D"]).values & party.reindex(once.named).isin(["R", "D"]).values]
    print(f"R and D only: {len(rd):,} release-mentions, cross-party "
          f"{(party.reindex(rd.speaker).values != party.reindex(rd.named).values).mean():.1%}")
    print(f"leadership title: {once.is_leader_title.mean():.1%} | context median {int(c.context.str.len().median())} chars")
