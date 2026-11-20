"""Split press_releases.parquet into parts small enough for GitHub's web upload (25 MB per file).

Run from Anas/:  python collector/split.py <folder with press_releases.parquet> <output folder> [--max-mb 22]

Rules:
- Every member's releases go in ONE part (split on bioguide, never inside a member).
- Members are kept in bioguide order, and a new part starts when the next member would push it over the limit.
- MANIFEST.md says how many parts there are, which members each holds, its rows and a checksum, and how to load
  them; the parts read back together equal the unsplit file (checked here before anything is written as final).
"""
import argparse
import hashlib
import os

import pandas as pd

ap = argparse.ArgumentParser()
ap.add_argument("src")
ap.add_argument("out")
ap.add_argument("--max-mb", type=float, default=22.0)    # margin under 25 MB: compression varies per part
a = ap.parse_args()

full = pd.read_parquet(os.path.join(a.src, "press_releases.parquet"))
full = full.sort_values(["bioguide", "date", "url"]).reset_index(drop=True)
os.makedirs(a.out, exist_ok=True)


def size_mb(df):
    tmp = os.path.join(a.out, "_size_probe.parquet")
    df.to_parquet(tmp, index=False, compression="zstd")
    s = os.path.getsize(tmp) / 1e6
    os.remove(tmp)
    return s


# per-member size estimate from the text length, then exact sizes checked when each part is written
members = full.groupby("bioguide", sort=True)
bytes_per_member = members.text.apply(lambda t: t.str.len().sum())
ratio = size_mb(full) * 1e6 / bytes_per_member.sum()          # compressed bytes per text character
groups, cur, cur_bytes = [], [], 0.0
for b, n in bytes_per_member.items():
    if cur and (cur_bytes + n) * ratio / 1e6 > a.max_mb:
        groups.append(cur)
        cur, cur_bytes = [], 0.0
    cur.append(b)
    cur_bytes += n
groups.append(cur)

k = len(groups)
rows, paths = [], []
for i, g in enumerate(groups, 1):
    part = full[full.bioguide.isin(g)]
    p = os.path.join(a.out, f"press_releases_part{i}of{k}.parquet")
    part.to_parquet(p, index=False, compression="zstd")
    mb = os.path.getsize(p) / 1e6
    assert mb < 25, f"{p} is {mb:.1f} MB; rerun with a lower --max-mb"
    sha = hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
    rows.append((os.path.basename(p), len(part), part.bioguide.nunique(), g[0], g[-1], round(mb, 1), sha))
    paths.append(p)

# the parts together must equal the whole: same rows, same members, same texts
back = pd.concat([pd.read_parquet(p) for p in paths], ignore_index=True)
back = back.sort_values(["bioguide", "date", "url"]).reset_index(drop=True)
assert len(back) == len(full) and back.equals(full), "parts do not add up to the unsplit file"
assert not back.groupby("bioguide").size().index.duplicated().any()
spread = pd.concat([pd.read_parquet(p, columns=["bioguide"]).drop_duplicates().assign(part=i)
                    for i, p in enumerate(paths, 1)])
assert spread.bioguide.is_unique, "a member is spread over more than one part"

lines = [
    "# Press releases: one table in " + str(k) + " parts",
    "",
    f"`press_releases.parquet` ({len(full):,} releases, {full.bioguide.nunique()} members) is split into **{k} parts**",
    "because GitHub's web upload takes files under 25 MB. **Load all parts together**; one part alone is not the data.",
    "Every member is in exactly one part (split by member, in bioguide order), so per-member counts never span files.",
    "",
    "```python",
    "import glob, pandas as pd",
    "d = pd.concat(map(pd.read_parquet, sorted(glob.glob(\"press_releases_part*of" + str(k) + ".parquet\"))), ignore_index=True)",
    f"assert len(d) == {len(full)}  # rows in the unsplit file",
    "```",
    "",
    "| File | Releases | Members | First bioguide | Last bioguide | MB | SHA-256 (first 16) |",
    "|---|---|---|---|---|---|---|",
] + [f"| `{r[0]}` | {r[1]:,} | {r[2]} | {r[3]} | {r[4]} | {r[5]} | `{r[6]}` |" for r in rows] + [
    "",
    "Checked when written: the parts read back together are identical to the unsplit table (rows, columns, values),",
    "and no member appears in more than one part. Column meanings: `collector/README.md`.",
    "",
    f"Releases dated {full.date.min():%d %b %Y} to {full.date.max():%d %b %Y}; rows produced "
    f"{str(full.fetched_at.min())[:10]} to {str(full.fetched_at.max())[:10]}. "
    "`member_status.csv` gives every member's stop reason and completeness, `collect_log.csv` every failed or "
    "excused fetch. Members not collected (listing loads by JavaScript only, or gone): `collector/README.md`, "
    "\"Not collected\".",
]
open(os.path.join(a.out, "MANIFEST.md"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
