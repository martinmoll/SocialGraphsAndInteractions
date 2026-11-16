"""D1: precision of the name matcher from labels.csv, and how far each error type reaches in all mentions.

Run from project/:  python Diego/d1_matcher_precision/score.py
"""
import sys
from math import sqrt
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import draw_sample as d          # rebuilds the notebook's mention table M (and rewrites the two sample files, unchanged)

M, members, party = d.M, d.members, d.party
L = pd.read_csv(HERE / "labels.csv", dtype={"item": str}, keep_default_na=False)
L["verdict"] = np.where(L.diego_check.isin(["", "ok"]), L.verdict, L.diego_check)     # Diego's check overrules
main, supp = L[L["sample"] == "main"], L[L["sample"] == "supplement"]


def wilson(k, n, z=1.96):
    p = k / n; c = p + z * z / (2 * n); h = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)); den = 1 + z * z / n
    return f"{k}/{n} = {p:.0%} (95% interval {(c - h) / den:.0%} to {(c + h) / den:.0%})"


print(f"\nrows checked by Diego: {(L.diego_check != '').sum()} of {len(L)}")
print("\n== Main sample: 100 random mentions ==")
ok = main.verdict == "correct"
print("precision, strict (right member and said by the speaker):", wilson(ok.sum(), len(main)))
print("right member, whoever said it:                           ", wilson((main.verdict != "wrong_person").sum(), len(main)))
print("the 30 printed in the notebook:                          ", wilson(ok[:30].sum(), 30))
for name, g in main.groupby("cross"):
    print(f"  {'cross-party' if name else 'same-party '} mentions:", wilson((g.verdict == "correct").sum(), len(g)))
print("  errors that are cross-party:", int(main[~ok].cross.sum()), "of", int((~ok).sum()))
print("\n== By resolution route (main + supplement) ==")
for how, g in L.groupby("how"):
    print(f"  {how:15s}", wilson((g.verdict == "correct").sum(), len(g)))

good = L[L.verdict == "correct"]
t = pd.crosstab(good.is_yield, good.kind)
print("\n== The notebook's yield flag against the label, correct rows of both samples ==\n", t.to_string())
print(f"flag recall {t.loc[True, 'yield'] / t['yield'].sum():.0%}, flag precision {t.loc[True, 'yield'] / t.loc[True].sum():.0%}")

print("\n== How far each error type reaches in all", f"{len(M):,}", "mentions ==")
caps = M.matched_text.str.split().str[-1].str.isupper()
print(f"1. Surname printed in capitals (speaker headings, vote-change lines): {caps.sum()} mentions, {M[caps].cross.mean():.0%} cross-party")
roster = pd.read_csv("data/processed/members.csv")
shout = roster[roster["last"].str.isupper()]
print(f"2. Roster rows whose surname is stored in capitals, so the matcher never finds them: {len(shout)}")
print("   ", ", ".join(shout.name))
clash = {l.title() for l in shout["last"]} & set(d.by_last)
for s in sorted(clash):
    got = [members.name[b] for b in d.by_last[s]]; lost = list(shout[shout["last"].str.title() == s].name)
    print(f"   surname {s}: mentions go to {got}; invisible namesake {lost}; mentions matched: {M.named.isin(d.by_last[s]).sum()}")
al = M[(M.named == "G000553")]
print(f"   'Chairman Green' credited to Al Green, who chairs no committee: {(al.matched_text.str.startswith('Chair')).sum()} of {len(al)} Al Green mentions")
ag, early = M[M.named == "G000606"], M.day.astype(str) < "2025-09-01"      # Raúl Grijalva died in March 2025; his daughter was elected that autumn
print(f"   mentions credited to Adelita Grijalva dated before September 2025, all tributes to her father: {early[ag.index].sum()} of {len(ag)}")
mt = M[M.named == "T000463"]
print(f"   mentions credited to Michael Turner by Democrats in March 2025 (Sylvester Turner died 5 March 2025): "
      f"{((mt.day.astype(str).str[:7] == '2025-03') & (party[mt.speaker].values == 'D')).sum()} of {len(mt)}")
honorific = M.matched_text.str.startswith(("Mrs.", "Ms."))
print(f"3. 'Mrs.' or 'Ms.' matches: {honorific.sum()} (a title of the wrong sex is how the two constituent errors look; "
      "the roster has no column to test this with)")


def tie_share(X):
    pairs = pd.DataFrame({"a": np.minimum(X.speaker, X.named), "b": np.maximum(X.speaker, X.named)}).drop_duplicates()
    return len(pairs), (party[pairs.a].values != party[pairs.b].values).mean()


drop = caps | ((M.named == "G000553") & M.matched_text.str.startswith("Chair")) | ((M.named == "G000606") & early)
for label, X in (("as in the notebook", M), ("capital-surname, 'Chairman Green' and early-Grijalva mentions removed", M[~drop])):
    n, c = tie_share(X)
    print(f"floor map, {label}: {n:,} ties, {c:.1%} cross-party")
