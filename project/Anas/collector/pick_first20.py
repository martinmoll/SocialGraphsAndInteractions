"""The first 20 members (G5 test of the collector), chosen by a rule written before any text was collected.

Rule: among members whose listing the scope scan counted (status ok, not guessed), for each of the five site
layouts (drupal, drupal1, asp, wp, param:PageNum_rs) draw 2 Republicans and 2 Democrats at random, seed 2805.
That covers every pager and both parties. It is a test of the collector, not the analysis sample: the
analysis uses every countable member (STATUS.md).

Run from Anas/:  python collector/pick_first20.py press_scope/scope_by_member.csv district_lean/member_lean.csv
Writes collector/first20.csv.
"""
import sys
import pandas as pd

scope, lean = pd.read_csv(sys.argv[1]), pd.read_csv(sys.argv[2])
s = scope[(scope.status == "ok") & scope.guessed.isna() & scope.party.isin(["R", "D"])]
s = s.merge(lean[["bioguide", "exposed_2025", "redrawn_state"]], on="bioguide", how="left", suffixes=("_scope", ""))
picks = []
for kind in ["drupal", "drupal1", "asp", "wp", "param:PageNum_rs"]:
    for party in ["R", "D"]:
        g = s[(s.kind == kind) & (s.party == party)]
        picks.append(g.sample(2, random_state=2805))
p = pd.concat(picks)[["bioguide", "name", "party", "state", "district", "kind", "count", "exposed_2025", "redrawn_state"]]
p.to_csv("collector/first20.csv", index=False)
print(p.to_string(index=False))
print(f"\nexposed (served district): {int(p.exposed_2025.sum())}; in redrawn states: {int(p.redrawn_state.sum())}; "
      f"releases expected (scope count): {int(p['count'].sum())}")
