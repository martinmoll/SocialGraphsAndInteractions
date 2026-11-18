"""G1c: draw the hand check of the yield rule, from the mentions where the old and new rule disagree.

Run from project/:  python Martin/m3_yield_check/draw_yield_check.py
Reads Martin/mentions.parquet and data/processed/members.csv. Writes, next to this script:
  yield_check_sheet.csv  what Martin codes: no rule shown, rows shuffled
  yield_check_key.csv    which rule flagged each row, and mention_row into mentions.parquet. Do not open before coding.

Choices (DECISIONS G1c):
  - Pool: mentions between a Republican and a Democrat (either direction) where is_yield (phrase rule) and
    is_yield_window (old 60-character rule) disagree: 153 flagged by the phrase rule only, 132 by the window only.
  - 15 drawn from each side, seed 2805, so the check measures both false flags of the phrase rule
    (phrase only) and yields it misses (window only). Report the two sides separately, not as one share.
  - The surname of the named member is marked [[like this]] in the context, every time it appears.
"""
import re
from pathlib import Path
import pandas as pd

HERE, SEED, PER_SIDE = Path(__file__).parent, 2805, 15

M = pd.read_parquet("Martin/mentions.parquet").reset_index(names="mention_row")
members = pd.read_csv("data/processed/members.csv").set_index("bioguide")
rd = members.index[members.party.isin(["R", "D"])]
M = M[M.speaker.isin(rd) & M.named.isin(rd) & (M.is_yield != M.is_yield_window)]
M["side"] = M.is_yield.map({True: "phrase only", False: "window only"})

draw = (M.groupby("side", group_keys=False).sample(PER_SIDE, random_state=SEED)
         .sample(frac=1, random_state=SEED).reset_index(drop=True))
draw.insert(0, "id", range(1, len(draw) + 1))


def mark(text, surname):
    return re.sub(rf"\b({re.escape(surname)})\b", r"[[\1]]", text, flags=re.I)


sheet = pd.DataFrame({
    "id": draw.id,
    "speaker": members.name.reindex(draw.speaker).values,
    "named": members.name.reindex(draw.named).values,
    "date": draw.date,
    "doc_id": draw.doc_id,
    "context": [mark(c, members.at[n, "last"]) for c, n in zip(draw.context, draw.named)],
    "code": "",
    "note": "",
})
sheet.to_csv(HERE / "yield_check_sheet.csv", index=False, encoding="utf-8-sig")   # BOM so Excel shows accents
draw[["id", "mention_row", "side", "is_yield", "is_yield_window", "speaker", "named"]].to_csv(
    HERE / "yield_check_key.csv", index=False)
unmarked = (~sheet.context.str.contains(r"\[\[", regex=True)).sum()
print(f"pool: {M.side.value_counts().to_dict()} | drawn: {draw.side.value_counts().to_dict()} | "
      f"rows where the surname could not be marked: {unmarked}")
