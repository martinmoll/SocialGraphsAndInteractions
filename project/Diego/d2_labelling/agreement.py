"""D2 / S1: agreement between the two coders of every mention, and the distribution of codes.

Run from project/ when the three sheets are filled in:  python Diego/d2_labelling/agreement.py
Codes: A agreeing, D disagreeing, P procedural, N neutral, X not a mention of that member (see PROTOCOL.md).
"""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).parent
CODES = list("ADPNX")
key = pd.read_csv(HERE / "sample_key.csv").set_index("id")
read = lambda who: pd.read_csv(HERE / f"sheet_{who}.csv", keep_default_na=False).set_index("id").code.str.strip().str.upper()
first, second = read("diego"), pd.concat([read("martin"), read("anas")])
both = pd.DataFrame({"first": first, "second": second}).join(key[["cross", "is_yield", "second_coder"]])
bad = both[~both["first"].isin(CODES) | ~both["second"].isin(CODES)]
if len(bad): raise SystemExit(f"{len(bad)} rows are uncoded or carry an unknown code: {list(bad.index[:10])}")


def kappa(a, b):
    po = (a == b).mean()
    pe = sum((a == c).mean() * (b == c).mean() for c in CODES)
    return po, (po - pe) / (1 - pe)


for label, g in [("all 200", both), ("cross-party only", both[both.cross]),
                 ("Diego and Martin", both[both.second_coder == "martin"]), ("Diego and Anas", both[both.second_coder == "anas"])]:
    po, k = kappa(g["first"], g["second"])
    print(f"{label:18s} n = {len(g):3d}  raw agreement {po:.0%}  Cohen's kappa {k:.2f}")
print("\nconfusion (rows: Diego, columns: second coder)\n", pd.crosstab(both["first"], both["second"]).to_string())
agreed = both[both["first"] == both["second"]]
print(f"\ncodes where both coders agree ({len(agreed)} of {len(both)}), as shares:")
print(pd.crosstab(agreed.cross.map({True: "cross-party", False: "same-party"}), agreed["first"], normalize="index").round(2).to_string())
both[both["first"] != both["second"]].to_csv(HERE / "disagreements.csv")
print("\nrows the coders disagree on are in disagreements.csv, to be settled by the third member")
