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

Still missing (planned, see M1): a guard against senators and non-members ("Mrs. Peters", a constituent).
"""
import re
import unicodedata
from typing import NamedTuple

STATE_WINDOW = 80   # characters either side of the name searched for a state name (prototype choice 4)

STATES = dict(AL="Alabama", AK="Alaska", AZ="Arizona", AR="Arkansas", CA="California", CO="Colorado", CT="Connecticut",
    DE="Delaware", FL="Florida", GA="Georgia", HI="Hawaii", ID="Idaho", IL="Illinois", IN="Indiana", IA="Iowa", KS="Kansas",
    KY="Kentucky", LA="Louisiana", ME="Maine", MD="Maryland", MA="Massachusetts", MI="Michigan", MN="Minnesota",
    MS="Mississippi", MO="Missouri", MT="Montana", NE="Nebraska", NV="Nevada", NH="New Hampshire", NJ="New Jersey",
    NM="New Mexico", NY="New York", NC="North Carolina", ND="North Dakota", OH="Ohio", OK="Oklahoma", OR="Oregon",
    PA="Pennsylvania", RI="Rhode Island", SC="South Carolina", SD="South Dakota", TN="Tennessee", TX="Texas", UT="Utah",
    VT="Vermont", VA="Virginia", WA="Washington", WV="West Virginia", WI="Wisconsin", WY="Wyoming")

TITLE = r"(Mr\.|Ms\.|Mrs\.|Speaker|Leader|Whip|Representatives?|Rep\.|Congressm[ae]n|Congresswom[ae]n|Chairm[ae]n|Chairwoman|Ranking Member)"
LEADER_TITLES = {"Speaker", "Leader", "Whip", "Chairman", "Chairmen", "Chairwoman", "Ranking Member"}
WORD = r"[A-ZÀ-Þ][A-Za-zÀ-ÿ'’\-]+"
RX = re.compile(r"\b" + TITLE + r"\s+((?:" + WORD + r"\s){0,3}" + WORD + ")")


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
    def __init__(self, members):
        """members: the table in data/processed/members.csv (bioguide, first, last, state)."""
        m = members.set_index("bioguide")
        self.first, self.state = m["first"].map(key).to_dict(), m["state"].to_dict()
        self.by_last = {}
        for b, last in m["last"].items():
            self.by_last.setdefault(key(last), []).append(b)
        self.speaker = next(b for b in self.by_last["johnson"] if self.state[b] == "LA")

    def find(self, text):
        """Every title followed by a member's surname, as a list of Hit. Names that are no member's
        surname are left out; names that are but could not be pinned to one member have named=None."""
        hits = []
        for mm in RX.finditer(text):
            title, words = mm.group(1), mm.group(2).split()
            keys = [key(w) for w in words]
            for n in (3, 2, 1):                               # longest surname first: 'Van Drew' before 'Drew'
                cands = self.by_last.get(" ".join(keys[-n:])) if len(words) >= n else None
                if not cands:
                    continue
                before = keys[:-n]
                first = [c for c in cands if self.first[c] in before]
                near = text[max(0, mm.start() - STATE_WINDOW): mm.end() + STATE_WINDOW]
                state = [c for c in cands if STATES.get(self.state[c], "\0") in near]
                if all(in_capitals(w) for w in words[-n:]): named, how = None, "printed in capitals, dropped"
                elif len(cands) == 1:                         named, how = cands[0], "unique surname"
                elif title == "Speaker" and keys[-1] == "johnson": named, how = self.speaker, "Speaker rule"
                elif len(first) == 1:                         named, how = first[0], "first name"
                elif len(state) == 1:                         named, how = state[0], "state nearby"
                else:                                         named, how = None, "shared surname, dropped"
                hits.append(Hit(mm.start(), mm.end(), title, named, how))
                break
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
    print("matcher self-check passed")
