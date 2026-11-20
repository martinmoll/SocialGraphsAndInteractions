"""Draw the three hand checks for the 20 Nov matcher (Anas's checklist items 11, 2 and 1). Fixed seed.

Run from project/:  python Martin/m1_checks_20nov/draw_checks.py
Writes, next to this script, a sheet to fill in and a key not to open until done, for each check:
  recall_sheet.csv / recall_key.csv     30 floor turns: list every member named; the key has the matcher's hits
  untitled_sheet.csv / untitled_key.csv 30 full names without a title ("Chip Roy"): a mention of the member, or not
  list_sheet.csv                        20 of the new list hits ("Reps. A, B and C"): right member, or not
"""
import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0, "Martin")
from matcher import Matcher

HERE, SEED = Path(__file__).parent, 2005
members = pd.read_csv("data/processed/members.csv")
name = members.set_index("bioguide")["name"]
speeches = pd.read_parquet("data/processed/speeches.parquet")
mt = Matcher(members)
turns = speeches[(speeches.section == "H") & (speeches.n_words >= 50) & speeches.bioguide.isin(members.bioguide)]

# ---- recall: 30 turns, at most 1,000 words each so the check fits in about an hour
pool = turns[turns.n_words <= 1000]
R = pool.sample(30, random_state=SEED).reset_index(drop=True)
R.insert(0, "id", range(1, 31))
found = [sorted({h.named for h in mt.find(t) if h.named and h.named != b}) for t, b in zip(R.text, R.bioguide)]
R.assign(speaker_name=R.bioguide.map(name), named_members="", note="")[
    ["id", "day", "item", "speaker_name", "n_words", "text", "named_members", "note"]].to_csv(HERE / "recall_sheet.csv", index=False)
pd.DataFrame({"id": R.id, "matcher_found": [";".join(f) for f in found],
              "matcher_found_names": ["; ".join(name[b] for b in f) for f in found]}).to_csv(HERE / "recall_key.csv", index=False)
print(f"recall: 30 of {len(pool):,} turns up to 1,000 words ({len(pool) / len(turns):.0%} of the {len(turns):,} turns); "
      f"{sum(map(len, found))} members found by the matcher in them")

# ---- untitled full names, floor
U = []
for t in turns.itertuples():
    for h in mt.find(t.text, untitled=True):
        if h.how == "full name, no title" and h.named != t.bioguide:
            a, b = max(0, h.start - 250), h.end + 150
            U.append(dict(doc_id=t.item, speaker=t.bioguide, named=h.named,
                          context=("…" if a else "") + t.text[a:h.start] + "[[" + t.text[h.start:h.end] + "]]" + t.text[h.end:b] + "…"))
U = pd.DataFrame(U)
S = U.sample(30, random_state=SEED).reset_index(drop=True)
S.insert(0, "id", range(1, 31))
S.assign(speaker_name=S.speaker.map(name), named_name=S.named.map(name), code="", note="")[
    ["id", "speaker_name", "named_name", "context", "code", "note"]].to_csv(HERE / "untitled_sheet.csv", index=False)
S[["id", "doc_id", "speaker", "named"]].to_csv(HERE / "untitled_key.csv", index=False)
print(f"untitled: {len(U):,} untitled full-name hits on the floor (not in mentions.parquet); 30 drawn")

# ---- list hits, from the current mentions.parquet
M = pd.read_parquet("Martin/mentions.parquet")
L = M[M.how.str.startswith("list: ")].sample(20, random_state=SEED)
L = L.reset_index(names="mention_row").assign(speaker_name=lambda d: d.speaker.map(name), named_name=lambda d: d.named.map(name), code="", note="")
L.insert(0, "id", range(1, 21))
L[["id", "mention_row", "speaker_name", "named_name", "context", "code", "note"]].to_csv(HERE / "list_sheet.csv", index=False)
print(f"lists: {M.how.str.startswith('list: ').sum()} list hits in mentions.parquet; 20 drawn")
