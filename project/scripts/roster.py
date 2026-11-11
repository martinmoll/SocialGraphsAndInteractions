"""Shared helpers: the list of House members and a name matcher.

The roster is everyone who served in the House in the 119th Congress according to Voteview
(so members who died or resigned are included), enriched with the current-member file for
full names. Members are keyed by Bioguide ID, the identifier all our sources share.
"""
import collections
import csv
import json
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")

STATES = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
          "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
          "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
          "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
          "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
          "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
          "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
          "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
          "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
          "WI": "Wisconsin", "WY": "Wyoming"}
ABBR = {v.lower(): k for k, v in STATES.items()}
PARTY = {"200": "R", "100": "D", "328": "I"}
SUFFIXES = {"jr", "sr", "ii", "iii", "iv"}


def norm(s):
    """Lower-case letters only, accents removed: 'De La Cruz' -> 'delacruz'."""
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z]", "", s)


def load_roster():
    """Return {bioguide: dict(name, first, last, state, district, party, nominate_dim1, ...)}."""
    roster = {}
    with open(os.path.join(RAW, "voteview_H119_members.csv"), newline="") as f:
        for r in csv.DictReader(f):
            if r["chamber"] != "House" or not r["bioguide_id"]:
                continue
            last, _, rest = r["bioname"].partition(",")
            first = re.sub(r"\(.*?\)", "", rest).split()
            roster[r["bioguide_id"]] = dict(
                bioguide=r["bioguide_id"], name=f"{' '.join(first)} {last.title()}".strip(),
                first=first[0] if first else "", last=last.strip(), state=r["state_abbrev"],
                district=int(r["district_code"]), party=PARTY.get(r["party_code"], "?"),
                nominate_dim1=float(r["nominate_dim1"]) if r["nominate_dim1"] else None,
                nominate_dim2=float(r["nominate_dim2"]) if r["nominate_dim2"] else None,
                n_votes=int(float(r["nominate_number_of_votes"])) if r["nominate_number_of_votes"] else 0,
                current=False, nickname="")
    for x in json.load(open(os.path.join(RAW, "legislators-current.json"))):
        b, t = x["id"]["bioguide"], x["terms"][-1]
        if t["type"] != "rep" or t["state"] not in STATES:
            continue
        m = roster.setdefault(b, dict(bioguide=b, state=t["state"], district=t.get("district", 0),
                                      party=t["party"][0], nominate_dim1=None, nominate_dim2=None, n_votes=0))
        m.update(name=x["name"].get("official_full") or f"{x['name']['first']} {x['name']['last']}",
                 first=x["name"]["first"], last=x["name"]["last"], nickname=x["name"].get("nickname", ""),
                 current=True, district=t.get("district", m["district"]))
    return roster


class NameMatcher:
    """Match a name as printed in a source ('VAN EPPS', 'AUSTIN SCOTT', 'Kean Jr.') plus an optional
    state to one roster member. Returns a Bioguide ID, or None when zero or several members fit."""

    def __init__(self, roster):
        self.roster = roster
        self.by_last = collections.defaultdict(list)
        for b, m in roster.items():
            self.by_last[norm(m["last"])].append(b)

    def match(self, name, state=None):
        tokens = [w for w in re.split(r"[\s,]+", name.replace("&nbsp;", " ")) if w and norm(w) not in SUFFIXES and norm(w)]
        if state and len(state) > 2:
            state = ABBR.get(state.lower())
        # try the longest tail of the name as the surname first: 'VAN EPPS' before 'EPPS'
        for k in range(len(tokens), 0, -1):
            cands = self.by_last.get(norm("".join(tokens[-k:])), [])
            if state:
                cands = [b for b in cands if self.roster[b]["state"] == state]
            if len(cands) > 1 and k < len(tokens):          # several Scotts in Georgia: use the first name
                given = norm(tokens[0])
                narrowed = [b for b in cands if given and (
                    norm(self.roster[b]["first"]).startswith(given[:4]) or norm(self.roster[b]["nickname"]).startswith(given[:4])
                    or given in norm(self.roster[b]["name"]))]
                cands = narrowed or cands
            if len(cands) == 1:
                return cands[0]
            if cands:
                return None                                   # ambiguous: do not guess
        return None
