"""A3.4: score the matcher's recall on the 40 drawn releases against five blind AI readers.

Run from Anas/ after press_layer.py:  python a3/score_recall.py

Changed 21 Nov (Anas): the answer key comes from five blind LLM readers (3 Opus, 2 Sonnet), not from Anas's own
reading. Each saw only INSTRUCTIONS.md (rules identical to recall_sheet.xlsx), the member list and the 40 release
texts: no matcher output, no project files. Their lists are in recall_check/raters/reader1..5.csv.

Answer key: a (release, member) pair listed by at least 3 of the 5 readers with a bioguide (majority). Pairs listed
by 1 or 2 readers are reported, not scored. Then, for shared and for shared + press layer:
  found     the matcher has a hit for that member in that release (any status but unresolved: counted, or found
            and left out by design: template, repeated paragraph, title guard, state legislator)
  counted   found with status counted
  recall    found / key (Wilson 95% interval; a second interval by bootstrap over releases, because names come in
            lists and are not independent)
Also: matcher-counted pairs that no majority lists (for a human look), and the 10 releases outside the surname pool.
Writes recall_check/recall_scored.csv (one row per key pair or disagreement).
"""
import math
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HITS

HERE = os.path.dirname(os.path.abspath(__file__))
RC = os.path.join(HERE, "recall_check")
MAJORITY = 3


def wilson(k, n, z=1.96):
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    c = (p + z * z / (2 * n)) / (1 + z * z / n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return c - h, c + h


def boot(df, col, B=2000, seed=2805):
    g = df.groupby("sample_id")[col].agg(["sum", "count"])
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(g), (B, len(g)))
    s, c = g["sum"].values[idx].sum(1), g["count"].values[idx].sum(1)
    r = s / np.where(c == 0, np.nan, c)
    return np.nanpercentile(r, 2.5), np.nanpercentile(r, 97.5)


draw = pd.read_csv(os.path.join(RC, "recall_draw.csv"))
readers = []
for i in range(1, 6):
    r = pd.read_csv(os.path.join(RC, "raters", f"reader{i}.csv"), dtype=str).fillna("")
    r["reader"] = i
    readers.append(r)
R = pd.concat(readers)
R["bioguide"] = R.bioguide.str.strip()
missing = {i: sorted(set(draw.sample_id) - set(R[R.reader == i].sample_id)) for i in range(1, 6)}
print("releases missing per reader:", {k: v for k, v in missing.items() if v} or "none")
named = R[~R.bioguide.isin(["NONE", "?", ""])].drop_duplicates(["reader", "sample_id", "bioguide"])
votes = named.groupby(["sample_id", "bioguide"]).agg(n_readers=("reader", "nunique"),
                                                     as_written=("as_written", "first")).reset_index()
key = votes[votes.n_readers >= MAJORITY].merge(draw, on="sample_id")
minority = votes[votes.n_readers < MAJORITY]
unsure = R[R.bioguide == "?"]

url = dict(zip(draw.sample_id, draw.url))
out = []
for name, f in [("shared", "press_hits_shared.parquet"), ("shared + press layer", "press_hits_layer.parquet")]:
    H = pd.read_parquet(os.path.join(HITS, f), columns=["doc_id", "named", "status", "how"])
    H = H[H.doc_id.isin(draw.url) & H.named.notna()]
    found = {(u, b): s for u, b, s in zip(H.doc_id, H.named, H.status)}
    counted = set(zip(H[H.status == "counted"].doc_id, H[H.status == "counted"].named))
    k = key.copy()
    k["found"] = [(u, b) in found for u, b in zip(k.url, k.bioguide)]
    k["counted"] = [(u, b) in counted for u, b in zip(k.url, k.bioguide)]
    k["status"] = [found.get((u, b), "missed") for u, b in zip(k.url, k.bioguide)]
    k["rule_set"] = name
    out.append(k)
    print(f"\n== {name} ==")
    for grp in ["pool", "outside"]:
        g = k[k.group == grp]
        if not len(g):
            print(f"  {grp}: no key pairs (the readers' majority names nobody in these releases)")
            continue
        lo, hi = wilson(g.found.sum(), len(g))
        blo, bhi = boot(g, "found")
        print(f"  {grp}: key pairs {len(g)} in {g.sample_id.nunique()} releases; found {g.found.sum()} "
              f"= recall {g.found.mean():.3f} (Wilson {lo:.2f}-{hi:.2f}; bootstrap over releases {blo:.2f}-{bhi:.2f}); "
              f"counted {g.counted.sum()}; found but left out by design: "
              f"{g[g.found & ~g.counted].status.value_counts().to_dict()}")
    miss = k[~k.found]
    print("  missed:", [f"{r.sample_id} {r.bioguide} '{r.as_written}'" for r in miss.itertuples()])
    # matcher-counted pairs no majority lists
    keyset = set(zip(key.url, key.bioguide))
    extra = [(u, b) for u, b in counted if (u, b) not in keyset]
    sid = {v: s for s, v in url.items()}
    print("  counted by the matcher, not in the key:", [f"{sid[u]} {b}" for u, b in sorted(extra)])
    out.append(pd.DataFrame([dict(sample_id=sid[u], url=u, bioguide=b, rule_set=name, status="counted, not in key")
                             for u, b in extra]))

print(f"\nkey: {len(key)} pairs ({MAJORITY}+ of 5 readers); minority pairs (1-2 readers): {len(minority)}; "
      f"'?' lines: {len(unsure)}")
print("agreement: pairs listed by all 5:", int((votes.n_readers == 5).sum()), "of", len(votes))
print("minority pairs:", [f"{r.sample_id} {r.bioguide} ({r.n_readers}) '{r.as_written}'" for r in minority.itertuples()])
pd.concat(out, ignore_index=True).to_csv(os.path.join(RC, "recall_scored.csv"), index=False)
