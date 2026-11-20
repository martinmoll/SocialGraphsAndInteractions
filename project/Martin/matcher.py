"""M1: the shared name matcher. Finds House members named in a text ("Chairman Cole", "Ms. Van Duyne").

The same matcher is used for floor speeches (Martin) and press releases (Anas). From project/:

    import pandas as pd
    from Martin.matcher import Matcher
    matcher = Matcher(pd.read_csv("data/processed/members.csv"))
    for hit in matcher.find(text):
        if hit.named: ...          # hit.named is a Bioguide ID, or None with the reason in hit.how

It is the matcher of prototype_two_maps.ipynb (choices 3 to 5 there) with three changes, all from Diego's
D1 report. Each one is a modelling choice:

  A. Surnames are compared without case or accents. The prototype compared them exactly, so the 18 members
     whose surname members.csv stores in capitals were never matched and their namesakes got their mentions,
     and "Velazquez" never matched "Velázquez". Cost: none known.
  B. A name printed in capitals ("Mr. VEASEY") is dropped. The Record prints capitals in speaker headings
     and vote-change lines, not in speech. The prototype counted these (71 mentions). Cost: a press release
     that writes a name in capitals loses it.
  C. A surname shared with a territory's delegate no longer crashes the state rule (territories have no
     state name to look for, so the state rule never picks a delegate).

Changes of 20 Nov, from Anas's MATCHER_CHECKLIST.md (item numbers are his). Each one is a modelling choice:

  D. Nicknames count as first names (item 9). A shared surname is pinned by its first name, and members.csv
     has the official one, so "Mr. Bobby Scott", "Mr. Hank Johnson", "Mr. Chris Smith", "Mr. Buddy Carter",
     "Mr. Hal Rogers" and "Mr. Chuy Garcia" were dropped. The 19 nicknames of House members in
     unitedstates/congress-legislators (legislators-current.json) are in nicknames.csv next to this file.
  E. Lists after a plural title (item 1): "Reps. Lawler, Golden, and Fitzpatrick" gives three hits, not none;
     "Representatives Lawler and Golden" gives two, not one. "Reps." is now a title. The names after the
     first are resolved by the same rules and their how starts with "list: ".
  F. A title right after "State" is skipped (item 10): "State Rep. Smith" is a state legislator.
  G. Optional, off by default: full names without a title (item 2), "my friend, Chip Roy". find(text,
     untitled=True) adds them with how "full name, no title". Off for the floor until a hand check of 30 hits
     says they are mostly real mentions; the press side can turn it on.

Not added: carrying a resolved name forward within a turn (item 3; 58 of 783 dropped shared surnames).
"Senator" and "Sen." are not titles, so senators are never matched (item 5; pinned in the self-check).
"""
import re
import unicodedata
from pathlib import Path
from typing import NamedTuple

STATE_WINDOW = 80   # characters either side of the name searched for a state name (prototype choice 4)

STATES = dict(AL="Alabama", AK="Alaska", AZ="Arizona", AR="Arkansas", CA="California", CO="Colorado", CT="Connecticut",
    DE="Delaware", FL="Florida", GA="Georgia", HI="Hawaii", ID="Idaho", IL="Illinois", IN="Indiana", IA="Iowa", KS="Kansas",
    KY="Kentucky", LA="Louisiana", ME="Maine", MD="Maryland", MA="Massachusetts", MI="Michigan", MN="Minnesota",
    MS="Mississippi", MO="Missouri", MT="Montana", NE="Nebraska", NV="Nevada", NH="New Hampshire", NJ="New Jersey",
    NM="New Mexico", NY="New York", NC="North Carolina", ND="North Dakota", OH="Ohio", OK="Oklahoma", OR="Oregon",
    PA="Pennsylvania", RI="Rhode Island", SC="South Carolina", SD="South Dakota", TN="Tennessee", TX="Texas", UT="Utah",
    VT="Vermont", VA="Virginia", WA="Washington", WV="West Virginia", WI="Wisconsin", WY="Wyoming")

TITLE = r"(Mr\.|Ms\.|Mrs\.|Speaker|Leader|Whip|Representatives?|Reps?\.|Congressm[ae]n|Congresswom[ae]n|Chairm[ae]n|Chairwoman|Ranking Member)"
LEADER_TITLES = {"Speaker", "Leader", "Whip", "Chairman", "Chairmen", "Chairwoman", "Ranking Member"}
WORD = r"[A-ZÀ-Þ][A-Za-zÀ-ÿ'’\-]+"
NAME = r"(?:" + WORD + r"\s){0,3}" + WORD
RX = re.compile(r"\b" + TITLE + r"\s+(" + NAME + ")")
PLURAL = {"Representatives", "Reps.", "Congressmen", "Congresswomen", "Chairmen"}
# after a plural title: more names, each after ", ", " and ", ", and " (change E)
LIST_NEXT = re.compile(r"(?:\s*,\s*(?:and\s+)?|\s+and\s+)(" + NAME + ")")
STATE_BEFORE = re.compile(r"\bState\s+$")          # "State Rep. Smith" (change F)
NICKNAMES = Path(__file__).with_name("nicknames.csv")


def key(s):
    """Lower case, accents removed: 'GARCÍA' -> 'garcia', 'De La Cruz' -> 'de la cruz'."""
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def in_capitals(word):
    """'VEASEY' and 'McGOVERN' are; 'McCaul' and 'DeLauro' are not."""
    return sum(c.isupper() for c in word) > sum(c.islower() for c in word)


class Hit(NamedTuple):
    start: int      # where the title starts in the text
    end: int        # where the name ends
    title: str
    named: str      # Bioguide ID, or None
    how: str        # the rule that resolved it, or why it was dropped


class Matcher:
    def __init__(self, members, nicknames=NICKNAMES):
        """members: the table in data/processed/members.csv (bioguide, first, last, state).
        nicknames: a csv with bioguide and nickname, or None for official first names only."""
        m = members.set_index("bioguide")
        self.first = {b: {key(f)} for b, f in m["first"].items()}
        if nicknames is not None:
            import csv
            for r in csv.DictReader(open(nicknames, encoding="utf-8")):
                if r["bioguide"] in self.first:
                    self.first[r["bioguide"]].add(key(r["nickname"]))
        self.state = m["state"].to_dict()
        self.by_last = {}
        for b, last in m["last"].items():
            self.by_last.setdefault(key(last), []).append(b)
        self.speaker = next(b for b in self.by_last["johnson"] if self.state[b] == "LA")
        full = {}                                            # "chip roy" -> bioguide, for change G
        for b, last in m["last"].items():
            for f in self.first[b]:
                full.setdefault(f + " " + key(last), set()).add(b)
        self.full = {k: v.pop() for k, v in full.items() if len(v) == 1}
        self.full_rx = re.compile(r"\b(" + WORD + r")\s+(?:[A-Z]\.\s+)?((?:" + WORD + r"\s){0,2}" + WORD + r")\b")

    def resolve(self, title, words, text, a, b):
        """(named, how) for the name words found at text[a:b] after title, or None if no member has the surname."""
        keys = [key(w) for w in words]
        for n in (3, 2, 1):                                   # longest surname first: 'Van Drew' before 'Drew'
            cands = self.by_last.get(" ".join(keys[-n:])) if len(words) >= n else None
            if not cands:
                continue
            before = keys[:-n]
            first = [c for c in cands if self.first[c] & set(before)]
            near = text[max(0, a - STATE_WINDOW): b + STATE_WINDOW]
            state = [c for c in cands if STATES.get(self.state[c], "\0") in near]
            if all(in_capitals(w) for w in words[-n:]): return None, "printed in capitals, dropped"
            if len(cands) == 1:                          return cands[0], "unique surname"
            if title == "Speaker" and keys[-1] == "johnson": return self.speaker, "Speaker rule"
            if len(first) == 1:                          return first[0], "first name"
            if len(state) == 1:                          return state[0], "state nearby"
            return None, "shared surname, dropped"
        return None

    def find(self, text, untitled=False):
        """Every title followed by a member's surname, as a list of Hit. Names that are no member's
        surname are left out; names that are but could not be pinned to one member have named=None.
        untitled=True also finds "First Last" without a title (change G)."""
        hits = []
        for mm in RX.finditer(text):
            title = mm.group(1)
            if STATE_BEFORE.search(text[max(0, mm.start() - 12):mm.start()]):
                continue                                      # change F
            r = self.resolve(title, mm.group(2).split(), text, mm.start(), mm.end())
            if r:
                hits.append(Hit(mm.start(), mm.end(), title, *r))
            if title in PLURAL:                               # change E
                pos = mm.end()
                while (nx := LIST_NEXT.match(text, pos)):
                    r = self.resolve(title, nx.group(1).split(), text, nx.start(1), nx.end(1))
                    if r:
                        hits.append(Hit(nx.start(1), nx.end(1), title, r[0], "list: " + r[1]))
                    pos = nx.end()
        if untitled:
            taken = [(h.start, h.end) for h in hits]
            for mm in self.full_rx.finditer(text):
                words = (mm.group(1) + " " + mm.group(2)).split()
                for n in (len(words), 3, 2):                  # "Chip Roy", or the last words of a longer run
                    b = self.full.get(" ".join(key(w) for w in [words[0]] + words[-(n - 1):])) if n >= 2 else None
                    if b and not any(s <= mm.start() < e or s < mm.end() <= e for s, e in taken) \
                            and not all(in_capitals(w) for w in words[1:]):
                        hits.append(Hit(mm.start(), mm.end(), "", b, "full name, no title"))
                        break
            hits.sort()
        return hits


if __name__ == "__main__":      # self-check: python Martin/matcher.py, from project/
    import pandas as pd
    members = pd.read_csv("data/processed/members.csv")
    name = members.set_index("bioguide")["name"]
    mt = Matcher(members)

    def one(text):
        (hit,) = mt.find(text)
        return (name[hit.named] if hit.named else None), hit.how

    assert one("I thank Chairman Cole for his work.") == ("Tom Cole", "unique surname")
    assert one("Ms. Van Duyne spoke.")[0] == "Beth Van Duyne"                     # multi-word surname
    assert one("Congresswoman Velazquez led.")[0] == "Nydia M. Velázquez"         # change A: accents
    assert one("Speaker Johnson said so.")[1] == "Speaker rule"
    assert one("Mr. Austin Scott rose.") == ("Austin Scott", "first name")
    assert one("Mr. Scott rose.") == (None, "shared surname, dropped")            # change A: David SCOTT now seen
    assert one("the gentleman from Tennessee (Mr. Green)")[0] == "Mark E. Green"  # change A: was Al Green
    assert one("Mr. VEASEY changed his vote.") == (None, "printed in capitals, dropped")   # change B
    assert mt.find("Mr. Speaker, I thank Mrs. Nobody.") == []
    # 20 Nov changes
    assert one("Mr. Bobby Scott rose.") == ("Robert C. \"Bobby\" Scott", "first name")             # D: nickname
    for t, who in [("Mr. Hank Johnson", "J000288"), ("Mr. Chris Smith", "S000522"), ("Mr. Buddy Carter", "C001103"),
                   ("Mr. Hal Rogers", "R000395"), ("Mr. Chuy Garcia", "G000586"), ("Rep. Henry Johnson", "J000288")]:
        assert mt.find(t + " spoke.")[0].named == who, t
    many = lambda t: [name[h.named] for h in mt.find(t)]
    assert many("Reps. Lawler, Golden, and Fitzpatrick introduced the bill.") == \
        ["Michael Lawler", "Jared F. Golden", "Brian K. Fitzpatrick"]                         # E: lists
    assert many("Representatives Lawler and Golden introduced it.") == ["Michael Lawler", "Jared F. Golden"]
    assert many("Congressmen Bacon and Golden wrote.") == ["Don Bacon", "Jared F. Golden"]
    assert many("Representative Lawler and Golden Gate Park") == ["Michael Lawler"]           # singular: no list
    assert mt.find("I met State Rep. Lawler and State Representative Golden.") == []          # F
    assert mt.find("I thank Senator Collins and Sen. Kennedy.") == []                         # item 5: senators
    assert mt.find("my colleague and friend, Chip Roy, said") == []                           # G is off by default
    assert [h.how for h in mt.find("my colleague and friend, Chip Roy, said", untitled=True)] == ["full name, no title"]
    assert len(mt.find("I thank Mr. Chip Roy.", untitled=True)) == 1                           # no double count
    print("matcher self-check passed")
