"""Join the per-member parts into press_releases.parquet and collect_log.csv.

Run from Anas/:  python collector/combine.py <parts folder> <output folder>

Rows: one per release; the same release posted by two members stays as two rows (each chose to post it), and
`text_sha1` shows which rows share a text. Exact duplicate URLs within a member are dropped.
"""
import glob
import json
import os
import sys

import pandas as pd

parts, out = sys.argv[1], sys.argv[2]
d = pd.concat([pd.read_parquet(f) for f in sorted(glob.glob(os.path.join(parts, "*.parquet")))], ignore_index=True)
d = d.drop_duplicates(["bioguide", "url"])
d["date"] = pd.to_datetime(d.date)
# each member's run status travels with the rows, so a partial member is never mistaken for a full one
st = pd.DataFrame([json.load(open(f)) for f in sorted(glob.glob(os.path.join(parts, "*.status.json")))])
st = st.rename(columns={"complete": "member_complete", "stop": "member_stop"})[["bioguide", "member_complete", "member_stop"]]
d = d.merge(st, on="bioguide", how="left")
d["member_complete"] = d.member_complete.fillna(False).astype(bool)
cols = ["bioguide", "url", "date", "title", "text", "listing_url", "layout", "date_source", "body_selector",
        "n_words", "text_sha1", "item_type", "fetched_at", "listed", "member_complete", "member_stop"]
# parts written before the listed flag existed hold only listed releases
d["listed"] = d["listed"].fillna(True).astype(bool) if "listed" in d else True
d = d[cols].sort_values(["bioguide", "date"])
d.to_parquet(os.path.join(out, "press_releases.parquet"), index=False, compression="zstd")
st.to_csv(os.path.join(out, "member_status.csv"), index=False)
logs = [pd.read_csv(f) for f in sorted(glob.glob(os.path.join(parts, "*.log.csv")))]
pd.concat(logs, ignore_index=True).to_csv(os.path.join(out, "collect_log.csv"), index=False)
size = os.path.getsize(os.path.join(out, "press_releases.parquet")) / 1e6
print(f"{d.bioguide.nunique()} members, {len(d)} releases, {size:.1f} MB")
inc = st[~st.member_complete.fillna(False).astype(bool)]
print(f"incomplete members: {len(inc)} ({d[~d.member_complete].shape[0]} rows): "
      + ", ".join(f"{b} ({s})" for b, s in zip(inc.bioguide, inc.member_stop)))
