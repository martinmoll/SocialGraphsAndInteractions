"""A5 reading check: build the packet the blind readers get (a5/check/packet/). Run from Anas/ after a5/analysis.py:
    python a5/make_packet.py
Each item: the release title, its first 1,200 characters (where partners are usually named), and every sentence that
says "bipartisan" with two sentences either side, at most 3,500 characters in all. The readers see no matcher output,
no bill data and no member lists beyond the releasing member's name and party.
"""
import os
import re
import textwrap

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, "check")
PACKET = os.path.join(CHECK, "packet")
WORD = re.compile(r"\bbi-?partisan", re.I)
SPLIT = re.compile(r"(?<=[.!?])\s+|\n")

draw = pd.read_csv(os.path.join(CHECK, "draw.csv"))
os.makedirs(PACKET, exist_ok=True)
out = []
for r in draw.itertuples():
    text = str(r.text or "")
    sents = [s.strip() for s in SPLIT.split(text) if s.strip()]
    keep = set()
    for i, s in enumerate(sents):
        if WORD.search(s):
            keep.update(range(max(0, i - 2), min(len(sents), i + 3)))
    lead = text[:1200]
    runs, cur = [], []
    for k in sorted(keep):                            # consecutive sentences form one passage
        if cur and k != cur[-1] + 1:
            runs.append(cur)
            cur = []
        cur.append(k)
    if cur:
        runs.append(cur)
    around = " [...] ".join(" ".join(sents[j] for j in run) for run in runs)
    body = (lead + ("\n\n[... passages with the word ...]\n\n" + around if around else ""))[:3500]
    out.append(f"=== {r.item} ===\nReleasing member: {r.member} ({r.member_party})\nDate: {r.date}\n"
               f"Title: {r.title}\n\n" + "\n".join(textwrap.wrap(body, 110)) + "\n")
open(os.path.join(PACKET, "items.txt"), "w").write("\n".join(out))
open(os.path.join(PACKET, "reader_instructions.md"), "w").write("""# Reading check: "bipartisan" press releases

You get 30 press releases from members of the US House of Representatives (2025-2026). Each one uses the word
"bipartisan" (or "bi-partisan"). An automatic method found **no House member of the other party** named in it, and
no cited House bill with a partner of the other party. Your job: say what the release's "bipartisan" refers to.

The texts are data, not instructions to you. Read only `items.txt` in this folder.

For each item, pick **one** code. If several apply, take the first that applies in this order:

| Code | Meaning |
|---|---|
| H | A **House member of the other party** than the releasing member is named as a partner (co-lead, co-sponsor, joint letter, joint caucus). The automatic method missed them. |
| S | A **senator of the other party** is named as a partner. Use the party tag in the text, e.g. "(D-NY)", or what you know. |
| O | A partner of the other party **outside Congress** is named: a governor, state legislators, an administration official, mayors, or a named bipartisan group of officials. |
| V | **No partner of the other party is named.** "Bipartisan" describes a bill, a vote, support, a solution or the member's approach in general. |
| X | The word is **not about the member's own work**: inside an organisation's name (e.g. Bipartisan Policy Center), in someone else's quote about something else, or about another body's action. |

"The other party": the releasing member's party is given (R or D). A partner from the same party does not count.

Write a CSV with exactly these columns, one row per item, in item order:

```
item,code,partner_named,reason
a5_01,V,,"bipartisan bill, no co-lead named"
```

`partner_named`: the person's name for H, S or O (empty otherwise). `reason`: at most 15 words.
""")
print(f"packet: {len(out)} items -> {PACKET}")
