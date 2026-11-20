"""A3.1: mark House-wide template posts and each member's repeated paragraphs, before any name is matched.

Run from Anas/:  python a3/prepare.py --press press_releases --repo <project/ of the group repo>

Decisions (A3_PLAN.md section 6), fixed 20 Nov before any result:
  4. Template: the same text (text_sha1) under 5 or more members ("119th United States Congress Convenes", 34).
     Texts under 2 to 4 members are joint releases: kept, flagged shared_text.
  5. Repeated paragraph: a sentence of 6 or more words in 30% or more of the releases of a member with at least
     10 releases, split exactly as collector/check.py section 5 does (bios, press-contact lines).
Nothing is removed: matching (A3.2) runs on the full text and flags hits that fall in a template or a repeated
sentence, so every count can be rebuilt with other thresholds.

Writes out/release_flags.parquet (url, bioguide, n_members_same_text, template, shared_text) and
out/repeated_sentences.csv (bioguide, sentence, n_releases, share).
"""
import argparse
import os
import re
import sys
from collections import Counter

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import OUT, load_inputs

TEMPLATE_MIN_MEMBERS = 5          # decision 4
REPEAT_SHARE, REPEAT_MIN_RELEASES, REPEAT_MIN_WORDS = 0.30, 10, 6     # decision 5, = check.py section 5
SPLIT = re.compile(r"(?<=[.!?])\s+|\n")                                # = check.py section 5


def sentences(text):
    return {s.strip() for s in SPLIT.split(text) if len(s.split()) >= REPEAT_MIN_WORDS}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--press", required=True)
    ap.add_argument("--repo", required=True)
    a = ap.parse_args()
    d, *_ = load_inputs(a.press, a.repo)

    n_same = d.groupby("text_sha1").bioguide.transform("nunique")
    flags = pd.DataFrame({"url": d.url, "bioguide": d.bioguide, "n_members_same_text": n_same,
                          "template": n_same >= TEMPLATE_MIN_MEMBERS,
                          "shared_text": (n_same >= 2) & (n_same < TEMPLATE_MIN_MEMBERS)})
    flags.to_parquet(os.path.join(OUT, "release_flags.parquet"), index=False)

    rows = []
    for b, g in d.groupby("bioguide"):
        if len(g) < REPEAT_MIN_RELEASES:
            continue
        cnt = Counter()
        for t in g.text:
            cnt.update(sentences(t))
        rows += [(b, s, n, round(n / len(g), 3)) for s, n in cnt.items() if n / len(g) >= REPEAT_SHARE]
    rep = pd.DataFrame(rows, columns=["bioguide", "sentence", "n_releases", "share"]).sort_values(
        ["bioguide", "share"], ascending=[True, False])
    rep.to_csv(os.path.join(OUT, "repeated_sentences.csv"), index=False)

    t = flags[flags.template]
    print(f"releases {len(d):,}; template releases {len(t):,} ({t.url.nunique()} urls, "
          f"{d.loc[flags.template, 'text_sha1'].nunique()} texts); shared_text releases {int(flags.shared_text.sum()):,}")
    print("template texts:", d.loc[flags.template].groupby("text_sha1").agg(
        members=("bioguide", "nunique"), title=("title", "first")).sort_values("members", ascending=False)
        .to_string(index=False))
    print(f"repeated sentences: {len(rep):,} in {rep.bioguide.nunique()} members "
          f"(share median {rep.share.median():.2f}, max {rep.share.max():.2f})")
