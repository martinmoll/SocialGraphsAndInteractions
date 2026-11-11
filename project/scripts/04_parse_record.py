"""Split the Congressional Record into speaker turns and attach each turn to a House member.

    python scripts/04_parse_record.py

How the Record is laid out (plain text inside the .htm files):
  * a new speaker starts a paragraph with two spaces and a name in capitals:
        "  Mr. VAN EPPS. Mr. Speaker, I move to ..."      "  Ms. LEE of Florida. I thank ..."
  * the chair and the clerk start with "  The SPEAKER pro tempore." etc. (not a member's speech: dropped)
  * inserted material (bill text, letters, lists) is indented four or more spaces (dropped)
  * Extensions of Remarks items are one written statement each, headed
        "HON. BETH VAN DUYNE of texas in the house of representatives"

Writes
  data/processed/speeches.parquet          one row per turn: day, item, section, bioguide, n_words, text
  data/processed/record_coverage.json      how many of the indexed Record items were on disk when this ran
  data/processed/record_unresolved.csv     speaker names we could not attach to a member, with counts
  data/processed/speaker_check_sample.csv  60 random turns to check by hand (fill in the `correct` column)
"""
import collections
import csv
import html
import json
import os
import random
import re
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # so `roster` is found from any working directory
from roster import RAW, ROOT, NameMatcher, load_roster

HTML = os.path.join(RAW, "record_html")
OUT = os.path.join(ROOT, "data", "processed")

CAPS = r"(?:[A-Z][a-z]{0,3}[A-Z][A-Za-z'’\-]*|[A-Z]{2,}[A-Za-z'’\-]*)"        # SMITH, McCAUL, LaLOTA, DesJARLAIS
TURN = re.compile(r"^  (?:Mr|Ms|Mrs|Miss|Dr)\.? (" + CAPS + r"(?: " + CAPS + r")*)(?: of ([A-Z][a-z]+(?: [A-Z][a-z]+)*))?\. ")
CHAIR = re.compile(r"^  The (?:Acting |ACTING )?(?:SPEAKER|CHAIR|PRESIDING OFFICER|CLERK|Clerk)")
HON = re.compile(r"HON\. ([A-Z][A-Za-z .,'’\-]+?)\s+of ([a-z ]+?)\s+in the house of representatives", re.S)
WORD = re.compile(r"[A-Za-z']+")


def clean(raw):
    return html.unescape(re.sub(r"<[^>]+>", "", raw))


if __name__ == "__main__":
    roster = load_roster()
    matcher = NameMatcher(roster)
    cache = {}

    def who(name, state):
        key = (name, state)
        if key not in cache:
            cache[key] = matcher.match(name, state)
        return cache[key]

    turns, unresolved = [], collections.Counter()
    files_read = 0

    def keep(day, item, section, bioguide, label, lines):
        text = " ".join(" ".join(lines).split())
        n = len(WORD.findall(text))
        if n == 0:
            return
        if bioguide:
            turns.append((day, item, section, bioguide, n, text))
        else:
            unresolved[label] += n

    for day in sorted(os.listdir(HTML)):
        folder = os.path.join(HTML, day)
        if not os.path.isdir(folder):
            continue
        for fname in sorted(os.listdir(folder)):
            item = fname[:-4]
            files_read += 1
            t = clean(open(os.path.join(folder, fname), encoding="utf8", errors="replace").read())
            if "-PgE" in fname:                                   # Extensions of Remarks: one author per item
                m = HON.search(t)
                if m:
                    body = [l for l in t[m.end():].split("\n") if not l.startswith("    ")]
                    keep(day, item, "E", who(m.group(1).strip(), m.group(2).strip()), f"HON. {m.group(1).strip()} of {m.group(2).strip()}", body)
                continue
            speaker, label, buf = None, None, []                 # House section: walk through the lines
            for line in t.split("\n"):
                m = TURN.match(line)
                if m:
                    if label is not None:
                        keep(day, item, "H", speaker, label, buf)
                    speaker = who(m.group(1), m.group(2))
                    label, buf = m.group(1) + (f" of {m.group(2)}" if m.group(2) else ""), [line[m.end():]]
                elif CHAIR.match(line):
                    if label is not None:
                        keep(day, item, "H", speaker, label, buf)
                    speaker, label, buf = None, None, []
                elif line.startswith("    "):
                    continue
                elif label is not None:
                    buf.append(line)
            if label is not None:
                keep(day, item, "H", speaker, label, buf)

    df = pd.DataFrame(turns, columns=["day", "item", "section", "bioguide", "n_words", "text"])
    # zstd keeps the file under GitHub's 25 MB limit for browser uploads
    df.to_parquet(os.path.join(OUT, "speeches.parquet"), index=False, compression="zstd", compression_level=19)
    with open(os.path.join(RAW, "record_index.csv")) as f:
        indexed = sum(1 for _ in f) - 1
    with open(os.path.join(OUT, "record_coverage.json"), "w") as f:
        json.dump({"items_in_index": indexed, "items_parsed": files_read}, f)
    with open(os.path.join(OUT, "record_unresolved.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name_as_printed", "words"])
        w.writerows(unresolved.most_common())

    random.seed(2805)
    sample = df[df.n_words >= 50].sample(60, random_state=2805)
    with open(os.path.join(OUT, "speaker_check_sample.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["day", "item", "assigned_member", "party", "state", "n_words", "first_300_chars", "source_url", "correct (y/n)"])
        for r in sample.itertuples():
            m = roster[r.bioguide]
            w.writerow([r.day, r.item, m["name"], m["party"], m["state"], r.n_words, r.text[:300],
                        f"https://www.govinfo.gov/content/pkg/CREC-{r.day}/html/{r.item}.htm", ""])

    total_un = sum(unresolved.values())
    print(f"days {df.day.nunique()} | items {df.item.nunique()} | turns {len(df):,} | words attached {df.n_words.sum():,}"
          f" | words not attached {total_un:,} ({total_un / (total_un + df.n_words.sum()):.1%})")
    print("members with any text:", df.bioguide.nunique(), "of", len(roster))
    print("top unresolved:", unresolved.most_common(12))
