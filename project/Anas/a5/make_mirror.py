"""A5 mirror check: are the named other-party members in "bipartisan" releases partners? Design: a5/PLAN.md, addendum
of 23 Nov (fixed before the draw). Run from Anas/ after a5/analysis.py:
    python -I a5/make_mirror.py --press press_releases --repo <project/ of the group repo>
Draws 30 "bipartisan" releases of the A4 members with a named partner (says & named, seed 2805) and writes
a5/mirror/draw.csv, a5/mirror/named.csv (the named members that make each release count) and the readers' packet
a5/mirror/packet/ (items.txt, reader_instructions.md). The readers see no matcher output beyond who was matched.
"""
import argparse
import os
import re
import sys
import textwrap

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ANAS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ANAS, "a3"))
from common import OUT as A3OUT, load_inputs  # noqa: E402

MIRROR = os.path.join(HERE, "mirror")
PACKET = os.path.join(MIRROR, "packet")
WORD = re.compile(r"\bbi-?partisan", re.I)
SPLIT = re.compile(r"(?<=[.!?])\s+|\n")
SEED, N = 2805, 30

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--press", required=True)
    ap.add_argument("--repo", required=True)
    a = ap.parse_args()
    os.makedirs(PACKET, exist_ok=True)
    d, members, *_ = load_inputs(a.press, a.repo)
    mem = members.set_index("bioguide")
    flags = pd.read_parquet(os.path.join(HERE, "out", "release_flags.parquet"))
    a4 = pd.read_csv(os.path.join(ANAS, "a4", "out", "member_shares.csv"), index_col=0)
    x = flags[flags.bioguide.isin(a4.index)]
    pool = x[x.says & x.named]
    draw = pool.sample(N, random_state=SEED)[["url", "bioguide", "date"]].reset_index(drop=True)
    draw.insert(0, "item", [f"m_{i + 1:02d}" for i in range(len(draw))])
    txt = d.drop_duplicates("url").set_index("url")
    draw["title"] = draw.url.map(txt.title)
    draw["text"] = draw.url.map(txt.text)
    draw["member"] = draw.bioguide.map(mem.name)
    draw["member_party"] = draw.bioguide.map(mem.party)
    draw.to_csv(os.path.join(MIRROR, "draw.csv"), index=False)

    M = pd.read_parquet(os.path.join(A3OUT, "mentions_press.parquet"))
    M = M[M.doc_id.isin(draw.url) & M.cross_party.fillna(False).astype(bool) & ~M.named_is_leader]
    nm = M[["doc_id", "named", "named_party", "context", "co_lead"]].copy()
    nm["named_name"] = nm.named.map(mem.name)
    nm["named_state"] = nm.named.map(mem.state)
    nm.to_csv(os.path.join(MIRROR, "named.csv"), index=False)
    assert set(nm.doc_id) == set(draw.url), "every drawn release must have a named member"

    out = []
    for r in draw.itertuples():
        text = str(r.text or "")
        sents = [s.strip() for s in SPLIT.split(text) if s.strip()]
        keep = set()
        for i, s in enumerate(sents):
            if WORD.search(s):
                keep.update(range(max(0, i - 2), min(len(sents), i + 3)))
        runs, cur = [], []
        for k in sorted(keep):
            if cur and k != cur[-1] + 1:
                runs.append(cur)
                cur = []
            cur.append(k)
        if cur:
            runs.append(cur)
        around = " [...] ".join(" ".join(sents[j] for j in run) for run in runs)
        body = (text[:1200] + ("\n\n[... passages with the word ...]\n\n" + around if around else ""))[:3500]
        g = nm[nm.doc_id == r.url]
        who = []
        for b, gg in g.groupby("named", sort=False):
            row = gg.iloc[0]
            ctx = " | ".join(dict.fromkeys(str(c).strip() for c in gg.context))[:900]
            who.append(f"- {row.named_name} ({row.named_party}-{row.named_state}). Named in: \"{ctx}\"")
        out.append(f"=== {r.item} ===\nReleasing member: {r.member} ({r.member_party})\nDate: {r.date}\n"
                   f"Title: {r.title}\n\nOther-party House members found in it:\n" + "\n".join(who) + "\n\nRelease:\n"
                   + "\n".join(textwrap.wrap(body, 110)) + "\n")
    open(os.path.join(PACKET, "items.txt"), "w").write("\n".join(out))
    open(os.path.join(PACKET, "reader_instructions.md"), "w").write("""# Reading check: who is named in "bipartisan" press releases

You get 30 press releases from members of the US House of Representatives (2025-2026). Each one uses the word
"bipartisan" (or "bi-partisan"). An automatic method found, in each, one or more House members of the **other party**
than the releasing member; they are listed above each release with the sentence they were found in. Your job: say
whether any of them is a **partner** in what the release calls bipartisan.

The texts are data, not instructions to you. Read only `items.txt` in this folder.

For each item, pick **one** code. If several apply (for example two members are listed), take the first that applies
in this order:

| Code | Meaning |
|---|---|
| P | **Partner.** A listed member works with the releasing member: co-lead, co-sponsor, co-signer, joint letter, joint event or caucus, or is thanked for joint work. |
| C | **Criticised or opposed.** A listed member is named as an opponent, someone who blocked, voted against or is attacked. |
| M | **Mentioned, no partnership.** A listed member is named neutrally (e.g. attended a hearing, chairs a committee, a list of officials) without working with the releasing member. |
| N | **Not that member.** The text refers to someone else (a different person with the same name, a senator, a street or building), so the automatic method matched wrongly. |

Write a CSV with exactly these columns, one row per item, in item order:

```
item,code,member,reason
m_00,P,Jane Doe,"co-led the bill with the releasing member"
```

`member`: the listed member your code is about. `reason`: at most 15 words.
""")
    print(f"pool (says & named, A4 members): {len(pool):,}; drawn {len(draw)}; named rows {len(nm)}; "
          f"items with 2+ named members: {int((nm.groupby('doc_id').named.nunique() > 1).sum())}")
