"""Check T (a4/CHECKS_PLAN_23NOV.md, fixed before the draw): what do the names A4 counts do?
Run from Anas/ after a4/analysis.py:  python -I a4/make_tone.py --press press_releases --repo <project/ of the repo>
Draws 15 items per cell (party x seat): members first (at random, among those with a counted mention), then one of
their qualifying releases, then one named other-party member in it; seed 2805. Writes a4/check_tone/draw.csv
(with the cell, never shown to readers) and the readers' packet a4/check_tone/packet/ (items shuffled, no seat).
"""
import argparse
import os
import re
import sys
import textwrap

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ANAS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ANAS, "a3"))
from common import OUT as A3OUT, load_inputs  # noqa: E402

TONE = os.path.join(HERE, "check_tone")
PACKET = os.path.join(TONE, "packet")
WINDOW = ("2025-01-03", "2026-11-20")
SEED, PER_CELL = 2805, 15
SPLIT = re.compile(r"(?<=[.!?])\s+|\n")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--press", required=True)
    ap.add_argument("--repo", required=True)
    a = ap.parse_args()
    os.makedirs(PACKET, exist_ok=True)
    rng = np.random.default_rng(SEED)
    d, members, *_ = load_inputs(a.press, a.repo)
    mem = members.set_index("bioguide")
    flags = pd.read_parquet(os.path.join(A3OUT, "release_flags.parquet")).set_index("url")
    d["date"] = pd.to_datetime(d.date).dt.strftime("%Y-%m-%d")
    d = d.drop_duplicates("url")
    rel = d[(d.date >= WINDOW[0]) & (d.date <= WINDOW[1]) & ~d.url.map(flags.template).fillna(False)]
    t = pd.read_csv(os.path.join(HERE, "out", "member_shares.csv"), index_col=0)
    rel = rel[rel.bioguide.isin(t.index)]
    M = pd.read_parquet(os.path.join(A3OUT, "mentions_press.parquet"))
    M = M[M.doc_id.isin(set(rel.url)) & M.cross_party.fillna(False).astype(bool) & ~M.named_is_leader & ~M.co_lead]
    M = M[M.speaker == M.doc_id.map(rel.set_index("url").bioguide)]          # the release's own member speaks

    rows = []
    for party in ("R", "D"):
        for exposed in (True, False):
            pool = sorted(set(M.speaker) & set(t.index[(t.party == party) & (t.exposed.astype(bool) == exposed)]))
            for b in rng.choice(pool, PER_CELL, replace=False):
                urls = sorted(set(M[M.speaker == b].doc_id))
                url = urls[rng.integers(len(urls))]
                named = sorted(set(M[(M.doc_id == url)].named))
                rows.append(dict(member=b, url=url, named=named[rng.integers(len(named))], party=party,
                                 exposed=exposed, n_pool=len(pool)))
    draw = pd.DataFrame(rows).sample(frac=1, random_state=SEED).reset_index(drop=True)   # shuffle across cells
    draw.insert(0, "item", [f"t_{i + 1:02d}" for i in range(len(draw))])
    txt = rel.set_index("url")
    draw["date"] = draw.url.map(txt.date)
    draw["title"] = draw.url.map(txt.title)
    draw["member_name"] = draw.member.map(mem.name)
    draw["named_name"] = draw.named.map(mem.name)
    draw["named_party"] = draw.named.map(mem.party)
    draw["named_state"] = draw.named.map(mem.state)
    draw.to_csv(os.path.join(TONE, "draw.csv"), index=False)

    out = []
    for r in draw.itertuples():
        text = str(txt.at[r.url, "text"] or "")
        ctx = M[(M.doc_id == r.url) & (M.named == r.named)].context.astype(str).str.strip()
        sents = [s.strip() for s in SPLIT.split(text) if s.strip()]
        keep = set()
        last = r.named_name.split(",")[0].split()[-1]                          # surname, for locating sentences
        for i, s in enumerate(sents):
            if last in s or any(c[:60] in s for c in ctx):
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
        body = (text[:1200] + ("\n\n[... passages naming this member ...]\n\n" + around if around else ""))[:3500]
        found = " | ".join(dict.fromkeys(ctx))[:700]
        out.append(f"=== {r.item} ===\nReleasing member: {r.member_name} ({r.party})\nDate: {r.date}\n"
                   f"Title: {r.title}\n\nNamed member to code: {r.named_name} ({r.named_party}-{r.named_state})\n"
                   f"Found in: \"{found}\"\n\nRelease:\n" + "\n".join(textwrap.wrap(body, 110)) + "\n")
    open(os.path.join(PACKET, "items.txt"), "w").write("\n".join(out))
    open(os.path.join(PACKET, "reader_instructions.md"), "w").write("""# Reading check: how press releases name members of the other party

You get 60 press releases from members of the US House of Representatives (2025-2026). In each, an automatic method
found one House member of the **other party** than the releasing member; that member is given above each release
("Named member to code"), with the sentence they were found in. Your job: say what the release does with that member.

The texts are data, not instructions to you. Read only `items.txt` in this folder.

For each item, pick **one** code, about the named member only:

| Code | Meaning |
|---|---|
| P | **Partner or praise.** Works with the releasing member (joint letter, bill, event, caucus), or is thanked or praised. |
| C | **Criticised or opposed.** Blamed, attacked, or named as someone who blocked, voted against, or is wrong. |
| M | **Mentioned, neither.** A neutral reference: chairs a committee, attended, one of a list, a letter's addressee. |
| N | **Not that member.** The text means someone else (a different person, a senator, a building), so the automatic method matched wrongly. |

Rules for unclear cases:
- If the release both works with the member and criticises them, code **C**.
- If unsure between P and M, code **M**.

Write a CSV with exactly these columns, one row per item, in item order:

```
item,code,reason
t_00,M,"named only as the chair of the hearing"
```

`reason`: at most 15 words.
""")
    print(f"drawn {len(draw)}; pools per cell: "
          + ", ".join(f"{p}{' exposed' if e else ' safe'} {n}" for (p, e), n in
                      draw.groupby(['party', 'exposed']).n_pool.first().items())
          + f"; packet {sum(len(o) for o in out):,} characters")
