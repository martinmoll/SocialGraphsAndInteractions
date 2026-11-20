"""Compare mentions.parquet after the 20 Nov matcher changes with the 18 Nov version, and map old rows to new.

Run from project/:  python Martin/m1_checks_20nov/compare_18nov.py
Reads the 18 Nov file from git (commit 25926974, the last one before the change) and the current file.
Writes row_map.csv (mention_row in the 18 Nov file -> row in the current file) next to this script, and checks
that every row Diego's D2 keys and Martin's yield-check key point at is still there, with the same mention.
"""
import io, subprocess
from pathlib import Path
import pandas as pd

HERE = Path(__file__).parent
old = pd.read_parquet(io.BytesIO(subprocess.run(["git", "show", "25926974:project/Martin/mentions.parquet"],
                                                 capture_output=True, check=True).stdout))
new = pd.read_parquet("Martin/mentions.parquet")
K = ["doc_id", "speaker", "named", "context"]
for d in (old, new):
    d["occ"] = d.groupby(K).cumcount()                  # the same name twice in one context
m = old.reset_index(names="row_18nov").merge(new.reset_index(names="row_20nov"), on=K + ["occ"], how="outer",
                                             suffixes=("_18nov", "_20nov"), indicator=True)
print(f"18 Nov: {len(old):,} rows | 20 Nov: {len(new):,} rows | kept {(m._merge == 'both').sum():,}, "
      f"lost {(m._merge == 'left_only').sum():,}, new {(m._merge == 'right_only').sum():,}")
print("new rows by rule:", m[m._merge == "right_only"].how_20nov.value_counts().to_dict())
kept = m[m._merge == "both"]
print("kept rows whose rule label changed:", (kept.how_18nov != kept.how_20nov).sum(),
      "| whose is_yield changed:", (kept.is_yield_18nov != kept.is_yield_20nov).sum())
rm = kept[["row_18nov", "row_20nov"]].astype(int).sort_values("row_18nov")
rm.to_csv(HERE / "row_map.csv", index=False)

rmap = rm.set_index("row_18nov").row_20nov
for f in ["Diego/d2_labelling/full_key.csv", "Diego/d2_labelling/sample_key.csv", "Martin/m3_yield_check/yield_check_key.csv"]:
    k = pd.read_csv(f)
    assert k.mention_row.isin(rmap.index).all(), f"{f}: a row is gone"
    rows = new.loc[rmap[k.mention_row].values]
    assert (rows.speaker.values == k.speaker.values).all() and (rows.named.values == k.named.values).all(), f
    if "context" in k:
        assert (rows.context.values == k.context.values).all(), f
    print(f"{f}: all {len(k)} rows found in the current file (old mention_row -> row_map.csv)")
