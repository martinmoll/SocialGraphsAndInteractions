"""A3.3 after the 21 Nov matcher switch: what happens to the 180 rows read on 20 Nov (A3_MATCHER_SWITCH.md, point 5).

Run from Anas/ after press_layer.py, on Anas's machine (needs press_hits_layer_75c67ae.parquet, the 20 Nov hits, in
common.HITS):   python a3/rescore_switch.py

Each read row is one hit of the 20 Nov layer (release URL, start, rule). For each, the new hits at that place:
  same            the new version finds the same member there with the same status: the reading carries over
  member changed  a different member at that place
  status changed  same member, other status (e.g. counted -> title guard)
  gone            the new version finds nothing there
Readings are taken with resolutions.csv (as in score_precision.py). Nothing is relabelled.
"""
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import HITS

HERE = os.path.dirname(os.path.abspath(__file__))
PC = os.path.join(HERE, "precision_check")
old = pd.read_parquet(os.path.join(HITS, "press_hits_layer_75c67ae.parquet"))
new = pd.read_parquet(os.path.join(HITS, "press_hits_layer.parquet"))
res = pd.read_csv(os.path.join(PC, "resolutions.csv")).set_index("sample_id").resolved
sheets = pd.read_excel(os.path.join(PC, "precision_sheets.xlsx"), sheet_name=None, dtype={"correct": str})
new_by_doc = {k: g for k, g in new.groupby("doc_id")}

rows = []
for tab, s in sheets.items():
    if tab == "How to read":
        continue
    for r in s.itertuples():
        o = old[(old.doc_id == r.url) & (old.start == r.start) & (old.layer_rule == r.rule)]
        if o.empty:                  # state_legislator_23 (Omar): the 20 Nov guard fix put it back to a shared hit
            o = old[(old.doc_id == r.url) & (old.start == r.start)]
        if len(o) != 1:
            sys.exit(f"{r.sample_id}: {len(o)} old hits at that place")
        o = o.iloc[0]
        g = new_by_doc.get(r.url, pd.DataFrame(columns=new.columns))
        at = g[(g.start <= r.start) & (g.end > r.start)]
        if at.empty:
            outcome, nr = "gone", None
        else:
            n = at.iloc[0]
            outcome = ("same" if n.named == o.named and n.status == o.status else
                       "member changed" if n.named != o.named else "status changed")
            nr = n.layer_rule if isinstance(n.layer_rule, str) else "shared"
        reading = str(res.get(r.sample_id, r.correct if isinstance(r.correct, str) else "")).strip().lower()
        rows.append(dict(sample_id=r.sample_id, old_rule=r.rule, old_status=o.status, reading=reading,
                         outcome=outcome, new_rule=nr))
T = pd.DataFrame(rows)
T.to_csv(os.path.join(PC, "rescore_switch.csv"), index=False)
print(pd.crosstab([T.old_rule], T.outcome, margins=True).to_string())
print("\nread n (wrong) rows and what happened to them:")
print(T[T.reading == "n"].to_string(index=False))
print("\nrows not 'same':")
print(T[T.outcome != "same"].to_string(index=False))
c = T[(T.outcome == "same") & T.old_status.eq("counted")]
print(f"\ncarried-over counted rows: {len(c)}, read y {int((c.reading == 'y').sum())}, n {int((c.reading == 'n').sum())}")
