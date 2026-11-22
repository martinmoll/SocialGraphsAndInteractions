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
    hand-labelling), cut to 1,000 characters centred on the name where the splitter finds no break.
    The prototype kept 60 characters either side.
  - NEW (18 Nov, DECISIONS G1c): is_yield is the phrase rule from m3_definitions.py: "yield" (not "yield back",
    not "yield myself") earlier in the same sentence as the name, or "for yielding" later in it. It found 30 of
    30 of D1's labelled yields; not yet tested on rows it has not seen.
  - NEW (22 Nov, DECISIONS G19): full names without a title count too ("my friend Chip Roy"), how = "full name, no
    title", after 30 of 30 hand-checked hits were real mentions.
  - Three columns beyond the agreed seven: how (the matcher rule), is_leader_title (prototype choice 6b) and
    is_yield_window, the old flag ("yield" within 60 characters of the name), kept for comparing the rules.
"""
import bisect
import re
from pathlib import Path
import pandas as pd
from matcher import Matcher, LEADER_TITLES

DATA, OUT = Path("data/processed"), Path(__file__).parent
MIN_TURN_WORDS, YIELD_WINDOW = 50, 60
MAX_CONTEXT = 1000   # characters; a longer context is cut to a window centred on the name, marked with …

# The phrase-based yield rule, as in m3_definitions.py (DECISIONS G1c).
TITLE_DOT = re.compile(r"\b(Mr|Ms|Mrs|Rep|Dr|Messrs)\.")
YIELD_TO = re.compile(r"\byield(?:s|ed)?\b(?!\s+(?:back|myself))[^.;?!]*$", re.I)     # "... yield 2 minutes to the gentleman from Texas ("
FOR_YIELDING = re.compile(r"^[^.;?!]*\bfor\s+yielding", re.I)                          # ") for yielding"


def yield_phrase(text, a, b):
    """True when the name at text[a:b] is the member yielded to, or the member thanked for yielding."""
    before, after = TITLE_DOT.sub(r"\1", text[max(0, a - 200):a]), TITLE_DOT.sub(r"\1", text[b:b + 120])
    return bool(YIELD_TO.search(before) or FOR_YIELDING.search(after))

# ponytail: naive sentence splitter. A sentence ends at . ? ! followed by a space and a capital, unless the
# word before is a title or an initial ("Mr. Cole", "H.R. 1"). It over-joins after "U.S. The" and the like,
# which only makes a context longer. Swap in a real tokenizer if the labellers find contexts cut wrongly.
SENT_END = re.compile(r"(?<!\bMr)(?<!\bMs)(?<!\bMrs)(?<!\bDr)(?<!\bRep)(?<!\bSen)(?<!\bSt)(?<!\bNo)(?<![A-Z])[.?!][\"”']?\s+(?=[A-Z“\"])")


def context(text, bounds, a, b):
    """The sentence(s) holding text[a:b] plus one sentence either side. bounds = sorted sentence starts."""
    i, j = bisect.bisect_right(bounds, a) - 1, bisect.bisect_right(bounds, b - 1) - 1
    lo, hi = bounds[max(i - 1, 0)], bounds[j + 2] if j + 2 < len(bounds) else len(text)
    if hi - lo > MAX_CONTEXT:                       # no sentence break found: cut a window centred on the name
        cut_lo = max(lo, min((a + b - MAX_CONTEXT) // 2, hi - MAX_CONTEXT))
        cut_hi = min(hi, cut_lo + MAX_CONTEXT)
        return ("… " if cut_lo > lo else "") + " ".join(text[cut_lo:cut_hi].split()) + (" …" if cut_hi < hi else "")
    return " ".join(text[lo:hi].split())


def main():
    members = pd.read_csv(DATA / "members.csv")
    speeches = pd.read_parquet(DATA / "speeches.parquet")
    matcher = Matcher(members)
    turns = speeches[(speeches.section == "H") & (speeches.n_words >= MIN_TURN_WORDS) & speeches.bioguide.isin(members.bioguide)]

    rows, dropped = [], {}
    for t in turns.itertuples():
        bounds = [0] + [m.end() for m in SENT_END.finditer(t.text)]
        for h in matcher.find(t.text, untitled=True):          # untitled names on for the floor since 22 Nov (G19)
            if h.named is None:
                dropped[h.how] = dropped.get(h.how, 0) + 1
            elif h.named != t.bioguide:
                near = t.text[max(0, h.start - YIELD_WINDOW): h.end + YIELD_WINDOW].lower()
                rows.append(dict(speaker=t.bioguide, named=h.named, source="floor", date=t.day, doc_id=t.item,
                                 context=context(t.text, bounds, h.start, h.end),
                                 is_yield=yield_phrase(t.text, h.start, h.end),
                                 how=h.how, is_leader_title=h.title in LEADER_TITLES, is_yield_window="yield" in near))
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
    print(f"yield (phrase rule): {M.is_yield.mean():.1%} | yield (old window rule): {M.is_yield_window.mean():.1%} | "
          f"leadership title: {M.is_leader_title.mean():.0%}")
    print(f"R and D only: {len(pairs):,} undirected ties, {(party[pairs.a].values != party[pairs.b].values).mean():.1%} cross-party "
          f"(prototype: 3,718 ties, 34.5%)")
    print(f"context length in characters: median {int(M.context.str.len().median())}, max {M.context.str.len().max()}")


if __name__ == "__main__":
    main()
