"""Checks on collected releases, run before anything uses them.

Run from Anas/:  python collector/check.py <parts folder> press_scope/scope_by_member.csv [bioguide,...]

1. Releases per member against the scope scan's count (a different method: dates on listing pages).
2. Share of releases with a date, and where the date came from.
3. Very short texts (under 60 words): a sign the article body was missed.
4. Duplicates: the same URL twice, the same text under two URLs of one member, the same text across members
   (joint releases, kept but counted).
5. Boilerplate: a sentence that recurs in at least 30% of one member's releases is probably a sidebar, a
   signature or a standard closing, which would put the same names into every release.
6. Failed fetches, by reason.
"""
import glob
import os
import re
import sys
from collections import Counter

import pandas as pd

parts, scope = sys.argv[1], pd.read_csv(sys.argv[2])
only = sys.argv[3].split(",") if len(sys.argv) > 3 else None
files = [f for f in glob.glob(os.path.join(parts, "*.parquet")) if not only or os.path.basename(f)[:-8] in only]
d = pd.concat([pd.read_parquet(f) for f in files], ignore_index=True)
logs = pd.concat([pd.read_csv(f) for f in glob.glob(os.path.join(parts, "*.log.csv"))
                  if not only or os.path.basename(f).split(".")[0] in only], ignore_index=True)
d["date"] = pd.to_datetime(d.date)
print(f"members {d.bioguide.nunique()}, releases {len(d)}")

# 1. counts against the scope scan (scan counted releases dated >= 3 Jan 2025 up to 18 Nov 2026)
c = d[d.date.isna() | (d.date <= "2026-11-18")].groupby("bioguide").size().rename("collected")
cmp = scope.set_index("bioguide")[["name", "kind", "count"]].join(c, how="inner")
cmp["ratio"] = (cmp.collected / cmp["count"]).round(2)
print("\n1. collected vs scope scan (ratio 1 = same count):")
print(cmp.sort_values("ratio").to_string())
print(f"   median ratio {cmp.ratio.median():.2f}; members outside 0.9-1.1: {int(((cmp.ratio < .9) | (cmp.ratio > 1.1)).sum())}")

# 2. dates
print(f"\n2. with a date: {d.date.notna().mean():.1%}; sources: {d.date_source.value_counts(dropna=False).to_dict()}")
print(f"   dates after today or before 3 Jan 2025: {int((d.date > pd.Timestamp.today()).sum())}, "
      f"{int((d.date < '2025-01-03').sum())}")

# 3. short texts
short = d[d.n_words < 60]
print(f"\n3. under 60 words: {len(short)} ({len(short) / len(d):.1%}); median words {d.n_words.median():.0f}")
for r in short.head(8).itertuples():
    print(f"   {r.bioguide} {r.n_words}w {r.url}")

# 4. duplicates
print(f"\n4. duplicate URLs: {int(d.url.duplicated().sum())}; same text twice within a member: "
      f"{int(d.duplicated(['bioguide', 'text_sha1']).sum())}; texts posted by more than one member: "
      f"{int(d.drop_duplicates(['bioguide', 'text_sha1']).text_sha1.duplicated(keep=False).sum())}")

# 5. boilerplate sentences
print("\n5. sentences in >= 30% of a member's releases (member, share, sentence):")
found = 0
for b, g in d.groupby("bioguide"):
    if len(g) < 10:
        continue
    cnt = Counter()
    for t in g.text:
        cnt.update({s.strip() for s in re.split(r"(?<=[.!?])\s+|\n", t) if len(s.split()) >= 6})
    for s, n in cnt.most_common(3):
        if n / len(g) >= 0.3:
            found += 1
            print(f"   {b} {n / len(g):.0%}: {s[:150]}")
print(f"   {found} found")

# 6. failures
print(f"\n6. failed fetches: {len(logs)}; by reason: {logs.reason.value_counts().to_dict() if len(logs) else {}}")
print(f"   item types: {d.item_type.value_counts().to_dict()}")
