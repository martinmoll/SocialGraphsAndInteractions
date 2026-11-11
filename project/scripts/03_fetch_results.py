"""Election results (NBC News feed) and district context (Wikipedia) for the 2026 House elections.

    python scripts/03_fetch_results.py

Sources
  NBC   https://www.nbcnews.com/firecracker/api/v2/state-results/2026-elections/<state>-house-results
        The request NBC's own results pages make; one per state. Unofficial counts.
        Snapshots are kept in data/raw/nbc_<date>/ because the feed changes as counting ends.
  Wiki  "2026 United States House of Representatives elections" (wikitext via the Wikipedia API),
        snapshot in data/raw/. Gives each district's lean (Cook PVI), incumbent and what happened to them.

Writes
  data/processed/members.csv    everyone who served in the House this Congress (from Voteview + current-member file)
  data/processed/districts.csv  one row per district: lean, votes by party, flags for unusual contests
  data/processed/incumbents.csv one row per sitting member: district they ran in and their fate
"""
import csv
import datetime
import glob
import json
import os
import re
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # so `roster` is found from any working directory
from roster import ABBR, RAW, ROOT, STATES, NameMatcher, load_roster

OUT = os.path.join(ROOT, "data", "processed")
WIKI_PAGE = "2026 United States House of Representatives elections"


REFERENCE_FILES = {      # small reference tables, fetched once
    "voteview_H119_members.csv": "https://voteview.com/static/data/out/members/H119_members.csv",
    "legislators-current.json": "https://unitedstates.github.io/congress-legislators/legislators-current.json",
}


def fetch_reference():
    os.makedirs(RAW, exist_ok=True)
    for name, url in REFERENCE_FILES.items():
        path = os.path.join(RAW, name)
        if not os.path.exists(path):
            req = urllib.request.Request(url, headers={"User-Agent": "course-project/0.1"})
            with open(path, "wb") as f:
                f.write(urllib.request.urlopen(req, timeout=120).read())


def nbc_dir():
    existing = sorted(glob.glob(os.path.join(RAW, "nbc_*")))
    if existing:
        return existing[-1]
    path = os.path.join(RAW, f"nbc_{datetime.date.today()}")
    os.makedirs(path)
    return path


def fetch_nbc(folder):
    for name in STATES.values():
        slug = name.lower().replace(" ", "-")
        path = os.path.join(folder, slug + ".json")
        if os.path.exists(path):
            continue
        url = f"https://www.nbcnews.com/firecracker/api/v2/state-results/2026-elections/{slug}-house-results"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with open(path, "wb") as f:
            f.write(urllib.request.urlopen(req, timeout=60).read())
        time.sleep(1)                                   # 50 requests, one per second


def fetch_wiki():
    existing = sorted(glob.glob(os.path.join(RAW, "wikipedia_2026_house_elections_*.json")))
    if existing:
        return existing[-1]
    import urllib.parse
    q = urllib.parse.urlencode(dict(action="parse", page=WIKI_PAGE, prop="wikitext", format="json"))
    req = urllib.request.Request("https://en.wikipedia.org/w/api.php?" + q, headers={"User-Agent": "course-project/0.1"})
    path = os.path.join(RAW, f"wikipedia_2026_house_elections_{datetime.date.today()}.json")
    with open(path, "wb") as f:
        f.write(urllib.request.urlopen(req, timeout=60).read())
    return path


def parse_nbc(folder):
    """One dict per district, keyed (state, district). At-large districts are district 0... except NBC calls them 1."""
    out = {}
    for path in sorted(glob.glob(os.path.join(folder, "*.json"))):
        d = json.load(open(path))
        st = d["stateAbbr"]
        areas = d["races"][0]["areas"]
        for a in areas:
            votes = {"gop": 0, "dem": 0, "other": 0}
            n = {"gop": 0, "dem": 0, "other": 0}
            inc, winner = [], None
            for c in a["candidates"]:
                p = c["party"] if c["party"] in ("gop", "dem") else "other"
                votes[p] += c.get("votes") or 0
                n[p] += 1
                if c.get("isIncumbent"):
                    inc.append(f"{c['name']} ({c['party']})")
                if c.get("isWinner"):
                    winner = c["party"]
            out[(st, a["district"] if len(areas) > 1 else 0)] = dict(
                rep_votes=votes["gop"], dem_votes=votes["dem"], other_votes=votes["other"],
                n_rep=n["gop"], n_dem=n["dem"], total_votes=a.get("votes"), pct_in=a.get("percentIn"),
                winner=winner, nbc_incumbents="; ".join(inc), ranked_choice=bool(a.get("isRankedChoiceVotingRace")))
    return out


def parse_wiki(path, matcher):
    t = json.load(open(path))["parse"]["wikitext"]["*"]
    t = re.sub(r"<ref[^>]*?/>|<ref.*?</ref>", "", t, flags=re.S)

    # states where new district lines were enacted before this election
    summary = t[t.find("Summary of mid-decade changes"):t.find("===Newly created seats===")]
    status_cells = {m.group(1): re.sub(r"data-sort-value=\S+\s*", "", m.group(2))[:70]
                    for m in re.finditer(r"\n!\[\[#([^|\]]+)\|[^\]]*\]\]\s*\n\|([^\n]*)", summary) if m.group(1).lower() in ABBR}
    redrawn = sorted(ABBR[k.lower()] for k, v in status_cells.items() if "{{ya" in v)
    print("status of each state in Wikipedia's redistricting table (redrawn = marked {{ya}}):")
    for k, v in status_cells.items():
        print(f"   {'REDRAWN' if '{{ya' in v else '       '}  {k:<16}{v}")

    # the page's own list of incumbents who lost in November
    sec = t[t.find("== Incumbents defeated in general elections =="):t.find("== Open seats that changed parties ==")]
    defeated = {}
    for m in re.finditer(r"#\{\{ushr\|(\w+)\|(\w+)\|[Xx]\}\}:\s*\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", sec):
        if m.group(1) in STATES:
            b = matcher.match(re.sub(r"\(.*?\)", "", m.group(4) or m.group(3)), m.group(1))
            defeated[b or f"UNMATCHED {m.group(3)}"] = (m.group(1), m.group(2))

    body = t[t.find("==Alabama=="):t.find("==See also==")]
    districts, incumbents, unmatched = {}, [], []
    for row in re.split(r"\n\|-\n!\s*(?:rowspan=\d+\s*\|)?\s*\{\{ushr\|", body)[1:]:
        m = re.match(r"([^|]+)\|([^|}]+)", row)
        st = m.group(1).strip()
        st = st if st in STATES else ABBR.get(st.lower())
        if st is None:
            continue                                    # delegates (DC, territories)
        dist = 0 if m.group(2).strip().upper() == "AL" else int(m.group(2))
        pvi = re.search(r"\{\{shading PVI\|([RD])\|(\d+)\}\}", row)
        lean = None
        if pvi:
            lean = int(pvi.group(2)) * (1 if pvi.group(1) == "R" else -1)
        elif re.search(r"shading PVI\|EVEN|\bEVEN\b", row.split("{{plainlist}}")[0]):
            lean = 0
        districts[(st, dist)] = dict(state=st, district=dist, lean=lean)
        head = row.split("{{plainlist}}")[0]
        cells = head.split("\n|")
        for i, c in enumerate(cells):
            sm = re.search(r"\{\{sortname\|([^|}]+)\|([^|}]+)", c)
            if not sm:
                continue
            status = next((x for x in cells[i + 1:i + 5] if "ncumbent" in x), "")
            status = re.sub(r"\{\{[^}]*\}\}|<br\s*/?>|'''|\[\[[^\]|]*\||\]\]|\[\[", " ", status).strip(" |")
            s = status.lower()
            fate = ("re-elected" if "re-elected" in s or "reelected" in s
                    else "lost general" if "lost re-election" in s or "lost reelection" in s
                    else "lost primary" if "renomination" in s or "lost nomination" in s
                    else "did not run" if "retir" in s or "run for" in s or "resign" in s or "died" in s or "withdrew" in s
                    else "uncalled")
            b = matcher.match(f"{sm.group(1)} {sm.group(2)}", st)
            if b is None:
                unmatched.append((st, dist, sm.group(1), sm.group(2)))
                continue
            incumbents.append(dict(bioguide=b, state=st, district=dist, fate=fate, status=status[:120]))
    return districts, incumbents, unmatched, redrawn, defeated


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    fetch_reference()
    roster = load_roster()
    matcher = NameMatcher(roster)
    with open(os.path.join(OUT, "members.csv"), "w", newline="") as f:
        cols = ["bioguide", "name", "first", "last", "state", "district", "party", "current", "nominate_dim1", "nominate_dim2", "n_votes"]
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(sorted(roster.values(), key=lambda m: (m["state"], m["district"])))

    folder = nbc_dir()
    fetch_nbc(folder)
    nbc = parse_nbc(folder)
    districts, incumbents, unmatched, redrawn, defeated = parse_wiki(fetch_wiki(), matcher)

    # the page's explicit list of defeated incumbents overrides the status cell
    for inc in incumbents:
        if inc["bioguide"] in defeated:
            inc["fate"] = "lost general"
    listed = {i["bioguide"] for i in incumbents}

    rows = []
    for key in sorted(set(districts) | set(nbc)):
        row = dict(state=key[0], district=key[1], lean=None)
        row.update(districts.get(key, {}))
        row.update(nbc.get(key, {}))
        row["redrawn_state"] = key[0] in redrawn
        row["in_wiki"], row["in_nbc"] = key in districts, key in nbc
        rows.append(row)
    cols = ["state", "district", "lean", "redrawn_state", "rep_votes", "dem_votes", "other_votes", "n_rep", "n_dem",
            "total_votes", "pct_in", "winner", "ranked_choice", "nbc_incumbents", "in_wiki", "in_nbc"]
    with open(os.path.join(OUT, "districts.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(OUT, "incumbents.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["bioguide", "state", "district", "fate", "status"])
        w.writeheader()
        w.writerows(incumbents)

    import collections
    print("NBC snapshot:", os.path.basename(folder), "| districts in NBC:", len(nbc), "| in Wikipedia:", len(districts),
          "| in both:", sum(r["in_wiki"] and r["in_nbc"] for r in rows))
    print("lean missing:", sum(r["lean"] is None for r in rows), "| redrawn states:", redrawn)
    print("incumbents matched:", len(incumbents), "| unmatched:", unmatched)
    print("fate by party:", dict(collections.Counter((roster[i["bioguide"]]["party"], i["fate"]) for i in incumbents)))
    print("defeated list on the page:", len(defeated), "| not matched to a district row:",
          [k for k in defeated if k not in listed])
