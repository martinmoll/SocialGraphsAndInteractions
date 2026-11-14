"""D1: draw the matches to be hand-checked.

Rebuilds the mention table exactly as section 1 of prototype_two_maps.ipynb does (same regex, same
resolution rules, same turn filter), then draws

  * the main sample: 100 mentions at random, seed 2805. The first 30 are the 30 printed in section 2
    of the notebook (same seed, same order), so the notebook's check is a subset of this one.
  * a supplementary sample: 20 more mentions from each of the three resolution routes that are rare in
    the main sample (state nearby, first name, Speaker rule), seed 2806.

Run from project/:  python Diego_Claude/d1_matcher_precision/draw_sample.py
Writes sample_main.csv and sample_supplement.csv next to this file, without labels.
"""
import re
from pathlib import Path
import pandas as pd

DATA, SEED = "data/processed", 2805
MIN_TURN_WORDS, STATE_WINDOW, YIELD_WINDOW = 50, 80, 60
WIDE = 400                      # characters of context either side given to the reader
OUT = Path(__file__).parent

members = pd.read_csv(f"{DATA}/members.csv")
members = members[members.party.isin(["R", "D"])].set_index("bioguide")
party, last = members.party, members["last"]
speeches = pd.read_parquet(f"{DATA}/speeches.parquet")

STATES = dict(AL="Alabama", AK="Alaska", AZ="Arizona", AR="Arkansas", CA="California", CO="Colorado", CT="Connecticut",
    DE="Delaware", FL="Florida", GA="Georgia", HI="Hawaii", ID="Idaho", IL="Illinois", IN="Indiana", IA="Iowa", KS="Kansas",
    KY="Kentucky", LA="Louisiana", ME="Maine", MD="Maryland", MA="Massachusetts", MI="Michigan", MN="Minnesota",
    MS="Mississippi", MO="Missouri", MT="Montana", NE="Nebraska", NV="Nevada", NH="New Hampshire", NJ="New Jersey",
    NM="New Mexico", NY="New York", NC="North Carolina", ND="North Dakota", OH="Ohio", OK="Oklahoma", OR="Oregon",
    PA="Pennsylvania", RI="Rhode Island", SC="South Carolina", SD="South Dakota", TN="Tennessee", TX="Texas", UT="Utah",
    VT="Vermont", VA="Virginia", WA="Washington", WV="West Virginia", WI="Wisconsin", WY="Wyoming")

by_last = members.reset_index().groupby("last").bioguide.apply(list).to_dict()
SPEAKER = members.index[(last == "Johnson") & (members.state == "LA")][0]
TITLE = r"(Mr\.|Ms\.|Mrs\.|Speaker|Leader|Whip|Representatives?|Rep\.|Congressm[ae]n|Congresswom[ae]n|Chairm[ae]n|Chairwoman|Ranking Member)"
LEADER_TITLES = {"Speaker", "Leader", "Whip", "Chairman", "Chairmen", "Chairwoman", "Ranking Member"}
RX = re.compile(r"\b" + TITLE + r"\s+((?:[A-Z][A-Za-z'’\-]+\s){0,3}[A-Z][A-Za-z'’\-]+)")


def resolve(title, words, text, a, b):
    words = [w.title() if w.isupper() else w for w in words]
    for n in (3, 2, 1):
        key = " ".join(words[-n:])
        if len(words) >= n and key in by_last:
            cands, before = by_last[key], words[:-n]
            if len(cands) == 1: return cands[0], "unique surname"
            if title == "Speaker" and key == "Johnson": return SPEAKER, "Speaker rule"
            first = [c for c in cands if members.first[c] in before]
            if len(first) == 1: return first[0], "first name"
            near = text[max(0, a - STATE_WINDOW): b + STATE_WINDOW]
            st = [c for c in cands if STATES[members.state[c]] in near]
            if len(st) == 1: return st[0], "state nearby"
            return None, "shared surname, dropped"
    return None, "not a member"


turns = speeches[(speeches.section == "H") & (speeches.n_words >= MIN_TURN_WORDS) & speeches.bioguide.isin(members.index)]
rows, dropped = [], 0
for idx, src, day, text in zip(turns.index, turns.bioguide, turns.day, turns.text):
    for mm in RX.finditer(text):
        who, how = resolve(mm.group(1), mm.group(2).split(), text, mm.start(), mm.end())
        if how == "shared surname, dropped": dropped += 1
        if who is None or who == src: continue
        ctx = text[max(0, mm.start() - YIELD_WINDOW): mm.end() + YIELD_WINDOW]
        wide = text[max(0, mm.start() - WIDE): mm.start()] + "[[" + mm.group(0) + "]]" + text[mm.end(): mm.end() + WIDE]
        rows.append((src, who, how, "yield" in ctx.lower(), mm.group(1) in LEADER_TITLES, ctx.replace("\n", " "),
                     idx, day, mm.group(0), wide.replace("\n", " ")))
M = pd.DataFrame(rows, columns=["speaker", "named", "how", "is_yield", "is_leader_title", "context",
                                "turn_row", "day", "matched_text", "wide_context"])
M["cross"] = party[M.speaker].values != party[M.named].values
print(f"mentions: {len(M):,} | resolved: {M.how.value_counts().to_dict()} | dropped: {dropped}")
assert len(M) == 7931 and dropped == 717, "does not reproduce the notebook's mention table"


def dress(S):
    S = S.copy()
    S.insert(0, "mention_row", S.index)
    S["speaker_name"] = members.name[S.speaker].values
    S["speaker_party"] = party[S.speaker].values
    S["named_name"] = members.name[S.named].values
    S["named_party"] = party[S.named].values
    S["named_state"] = members.state[S.named].values
    return S[["mention_row", "day", "speaker", "speaker_name", "speaker_party", "named", "named_name", "named_party",
              "named_state", "cross", "how", "is_yield", "is_leader_title", "matched_text", "context", "wide_context", "turn_row"]]


main = M.sample(100, random_state=SEED)
assert list(main.index[:30]) == list(M.sample(30, random_state=SEED).index), "first 30 are not the notebook's 30"
main = dress(main); main.insert(0, "item", range(1, 101)); main.insert(1, "in_notebook_30", main["item"] <= 30)
main.to_csv(OUT / "sample_main.csv", index=False)

rest = M.drop(main.mention_row)
supp = pd.concat([rest[rest.how == h].sample(20, random_state=SEED + 1) for h in ("state nearby", "first name", "Speaker rule")])
supp = dress(supp); supp.insert(0, "item", [f"S{i}" for i in range(1, len(supp) + 1)])
supp.to_csv(OUT / "sample_supplement.csv", index=False)
print("main sample by route:", main.how.value_counts().to_dict())
print("population by route:", M.how.value_counts(normalize=True).round(3).to_dict())
