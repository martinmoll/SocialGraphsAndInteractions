"""M2: write mentions.parquet and named_ties.csv from the House floor speeches.

Run from project/:  python Martin/build_mentions.py
Reads data/processed/members.csv and speeches.parquet. Writes both files next to this script (each member
writes only in their own folder), with the columns agreed in WORK_AND_DEADLINES.md section 3.

Choices, as in prototype_two_maps.ipynb unless marked NEW:
  - Turns: House floor only (section "H"), at least 50 words, spoken by a member in members.csv.
  - A member naming themselves is not a mention.
  - NEW: the independent in members.csv (Kiley) is kept as speaker and as named. The prototype dropped him;
    anyone who needs two party sides filters on party, as Diego's sampling script does.
  - NEW: context is the sentence with the name plus one sentence either side (Diego's request for the
    hand-labelling). The prototype kept 60 characters either side.
  - is_yield: the word "yield" within 60 characters of the name, unchanged. D1 measured this flag at 87%
    recall and 90% precision; whether to replace it is for M3.
  - Two columns beyond the agreed seven: how (the matcher rule) and is_leader_title (prototype choice 6b).
"""
import bisect
import re
from pathlib import Path
import pandas as pd
from matcher import Matcher, LEADER_TITLES

DATA, OUT = Path("data/processed"), Path(__file__).parent
MIN_TURN_WORDS, YIELD_WINDOW = 50, 60

# ponytail: naive sentence splitter. A sentence ends at . ? ! followed by a space and a capital, unless the
# word before is a title or an initial ("Mr. Cole", "H.R. 1"). It over-joins after "U.S. The" and the like,
# which only makes a context longer. Swap in a real tokenizer if the labellers find contexts cut wrongly.
SENT_END = re.compile(r"(?<!\bMr)(?<!\bMs)(?<!\bMrs)(?<!\bDr)(?<!\bRep)(?<!\bSen)(?<!\bSt)(?<!\bNo)(?<![A-Z])[.?!][\"”']?\s+(?=[A-Z“\"])")


def context(text, bounds, a, b):
    """The sentence(s) holding text[a:b] plus one sentence either side. bounds = sorted sentence starts."""
    i, j = bisect.bisect_right(bounds, a) - 1, bisect.bisect_right(bounds, b - 1) - 1
    lo, hi = bounds[max(i - 1, 0)], bounds[j + 2] if j + 2 < len(bounds) else len(text)
    return " ".join(text[lo:hi].split())


def main():
    members = pd.read_csv(DATA / "members.csv")
    speeches = pd.read_parquet(DATA / "speeches.parquet")
    matcher = Matcher(members)
    turns = speeches[(speeches.section == "H") & (speeches.n_words >= MIN_TURN_WORDS) & speeches.bioguide.isin(members.bioguide)]

    rows, dropped = [], {}
    for t in turns.itertuples():
        bounds = [0] + [m.end() for m in SENT_END.finditer(t.text)]
        for h in matcher.find(t.text):
            if h.named is None:
                dropped[h.how] = dropped.get(h.how, 0) + 1
            elif h.named != t.bioguide:
                near = t.text[max(0, h.start - YIELD_WINDOW): h.end + YIELD_WINDOW].lower()
                rows.append(dict(speaker=t.bioguide, named=h.named, source="floor", date=t.day, doc_id=t.item,
                                 context=context(t.text, bounds, h.start, h.end), is_yield="yield" in near,
                                 how=h.how, is_leader_title=h.title in LEADER_TITLES))
    M = pd.DataFrame(rows)
    M.to_parquet(OUT / "mentions.parquet", index=False)
    ties = M.groupby(["speaker", "named", "source"]).size().rename("n_mentions").reset_index()
    ties.to_csv(OUT / "named_ties.csv", index=False)

    party = members.set_index("bioguide").party
    rd = M[party[M.speaker].isin(["R", "D"]).values & party[M.named].isin(["R", "D"]).values]
    pairs = pd.DataFrame({"a": rd[["speaker", "named"]].min(axis=1), "b": rd[["speaker", "named"]].max(axis=1)}).drop_duplicates()
    print(f"turns read: {len(turns):,} from {turns.bioguide.nunique()} speakers, {turns.day.min()} to {turns.day.max()}")
    print(f"mentions: {len(M):,} | directed pairs: {len(ties):,} | dropped: {dropped}")
    print("resolved by:", M.how.value_counts().to_dict())
    print(f"near a yield: {M.is_yield.mean():.0%} | leadership title: {M.is_leader_title.mean():.0%}")
    print(f"R and D only: {len(pairs):,} undirected ties, {(party[pairs.a].values != party[pairs.b].values).mean():.1%} cross-party "
          f"(prototype: 3,718 ties, 34.5%)")
    print(f"context length in characters: median {int(M.context.str.len().median())}, max {M.context.str.len().max()}")


if __name__ == "__main__":
    main()
