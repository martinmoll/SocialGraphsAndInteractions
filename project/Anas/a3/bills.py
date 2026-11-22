"""A3.5: the bills each release cites, and who leads them (A3_PLAN.md step A3.5, decision 7).

Run from Anas/:  python a3/bills.py --press press_releases --repo <project/ of the group repo>

1. Bill numbers in the release text: H.R. 1234, H.Res. 56, H.J.Res. 7, H.Con.Res. 8 (House) and S. 12, S.Res.,
   S.J.Res., S.Con.Res. (Senate). Spaces and periods are optional ("HR 1234", "H. R. 1234").
2. A House number is looked up in Martin's bills.parquet (119th Congress, govinfo BILLSTATUS). Status:
     resolved          found, and nothing says it is another Congress
     other Congress    "118th Congress", "last Congress", ... within 150 characters, or the bill was introduced
                       after the release date (the number cannot be this Congress's bill yet)
     not in data       no such 119th bill (e.g. introduced after the data was fetched)
     senate            a Senate bill: kept, but House cosponsors do not exist for it
3. For each resolved bill: its sponsor, and the role of the releasing member on it (sponsor, original cosponsor,
   later cosponsor, none), from cosponsors.parquet (withdrawn cosponsors left out).
4. Automatic check: does the release also print the bill's own title? (A long enough part of it: the title without
   "Act"/"of 2025", lower case.) Reported as a share; the rows where it does not are what a reading would look at.
5. Decision 7: how many releases name a 119th House bill only by its title (no number)? Titles are matched only if
   they add more than 5 percentage points of releases with a bill.

Writes out/release_bills.csv (one row per bill cited in a release).
"""
import argparse
import os
import re
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import OUT, load_inputs

BILL = re.compile(r"(?<![A-Za-z.])(H\.?\s?R\.?|H\.?\s?Res\.?|H\.?\s?J\.?\s?Res\.?|H\.?\s?Con\.?\s?Res\.?|"
                  r"S\.?\s?Res\.?|S\.?\s?J\.?\s?Res\.?|S\.?\s?Con\.?\s?Res\.?|S\.)\s?(\d{1,5})\b")
TYPE = {"HR": "hr", "HRES": "hres", "HJRES": "hjres", "HCONRES": "hconres",
        "S": "s", "SRES": "sres", "SJRES": "sjres", "SCONRES": "sconres"}
OTHER = re.compile(r"\b(?:11[0-8]th Congress|last Congress|previous Congress|prior Congress)", re.I)
PAST_YEAR = re.compile(r"\b(?:19\d\d|20[01]\d|202[0-4])\b")     # "In October 2019, ... introduced H.R. 5021"
FILLER = {"to", "for", "and", "of", "in", "on", "a", "an", "by", "with", "from", "under", "s", "u", "states", "united"}


def title_overlap(title, window):
    """Share of the bill title's content words that appear in the text around the number (0 to 1)."""
    tw = [w for w in core(title).split() if w not in FILLER and len(w) > 2]
    if not tw:
        return None
    ww = set(core(window).split())
    return sum(w in ww for w in tw) / len(tw)
WINDOW = 150
STOP = re.compile(r"\b(act|resolution|of 20\d\d|the)\b")


def core(title):
    """Lower-case title without 'Act', 'of 2025', 'the': the part a release would repeat."""
    t = re.sub(r"[^a-z0-9 ]", " ", str(title).lower())
    return re.sub(r"\s+", " ", STOP.sub(" ", t)).strip()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--press", required=True)
    ap.add_argument("--repo", required=True)
    a = ap.parse_args()
    d, members, *_ = load_inputs(a.press, a.repo)
    bills = pd.read_parquet(os.path.join(a.repo, "data", "processed", "bills.parquet")).set_index("bill_id")
    cos = pd.read_parquet(os.path.join(a.repo, "data", "processed", "cosponsors.parquet"))
    cos = cos[~cos.withdrawn]
    role = {(b, c): ("original cosponsor" if o else "later cosponsor") for b, c, o in zip(cos.bill_id, cos.cosponsor, cos.original)}
    n_orig = cos[cos.original].groupby("bill_id").size()

    rows = []
    for r in d.itertuples():
        t = r.text
        seen, ct = set(), None
        for m in BILL.finditer(t):
            typ = TYPE.get(m.group(1).replace(" ", "").replace(".", "").upper())
            if typ is None:
                continue
            bid = f"{typ}{int(m.group(2))}"
            if bid in seen:
                continue
            seen.add(bid)
            near = t[max(0, m.start() - WINDOW): m.end() + WINDOW]
            row = dict(url=r.url, bioguide=r.bioguide, date=str(r.date)[:10], bill_id=bid, as_written=m.group(0),
                       start=m.start(), sponsor=None, releaser_role=None, n_original=0, title=None, title_in_text=None)
            if typ.startswith("s"):
                row["status"] = "senate"
            elif bid not in bills.index:
                row["status"] = "not in data"
            else:
                b = bills.loc[bid]
                sentence = t[max(0, t.rfind(".", 0, max(0, m.start() - 1)) + 1): t.find(".", m.end()) + 1 or len(t)]
                if OTHER.search(near) or b.introduced > row["date"] or PAST_YEAR.search(sentence):
                    row["status"] = "other Congress"
                else:
                    row["status"] = "resolved"
                    row["sponsor"], row["title"], row["n_original"] = b.sponsor, b.title, int(n_orig.get(bid, 0))
                    row["releaser_role"] = ("sponsor" if b.sponsor == r.bioguide else role.get((bid, r.bioguide), "none"))
                    c = core(b.title)
                    ct = ct if ct is not None else core(t)
                    row["title_in_text"] = bool(c) and len(c) >= 6 and c in ct
                    row["title_overlap"] = title_overlap(b.title, t[max(0, m.start() - 400): m.end() + 400])
            rows.append(row)
    B = pd.DataFrame(rows)

    print(f"bill numbers cited: {len(B):,} in {B.url.nunique():,} releases ({B.url.nunique() / len(d):.1%})")
    print("status:", B.status.value_counts().to_dict())
    R = B[B.status == "resolved"]
    print(f"resolved: {len(R):,} in {R.url.nunique():,} releases; releaser role:", R.releaser_role.value_counts().to_dict())
    print(f"automatic check: the release also prints the bill's title in {R.title_in_text.mean():.1%} of resolved rows")
    ov = R.title_overlap
    print(f"  title words within 400 chars of the number: >= half in {(ov >= 0.5).mean():.1%}, none in "
          f"{(ov == 0).mean():.1%}, title has no content words {ov.isna().mean():.1%}")

    # decision 7: titles without a number
    hb = bills[bills.type == "hr"]
    titles = {tuple(core(x).split()) for x in hb.title if len(core(x).split()) >= 3}
    by_start = {}                                       # first two words -> lengths of titles starting with them
    for k in titles:
        by_start.setdefault(k[:2], set()).add(len(k))
    cited = set(B.url)

    def has_title(text):
        w = core(text).split()
        for i in range(len(w) - 1):
            for n in by_start.get((w[i], w[i + 1]), ()):
                if tuple(w[i:i + n]) in titles:
                    return True
        return False
    title_only = [u for u, t in zip(d.url, d.text) if u not in cited and has_title(t)]
    base = B[B.status == "resolved"].url.nunique()
    print(f"decision 7, loose (title words without 'Act', 3+ words): {len(title_only):,} releases "
          f"= +{len(title_only) / len(d) * 100:.1f} points (bill-number releases: {base / len(d) * 100:.1f}%)")
    # stricter: the exact official title, 'Act' included, and only titles that belong to one bill
    tc = hb.title.str.strip().value_counts()
    exact = [x for x in tc[tc == 1].index if re.search(r"\bAct\b", x) and len(x.split()) >= 3 and not x.startswith("To ")]
    by2, title_bill = {}, {x.lower(): bid for bid, x in hb.title.str.strip().items() if x in set(exact)}
    for x in exact:
        w = x.lower().split()
        by2.setdefault(tuple(w[:2]), []).append(x.lower())
    strict = []
    meta = d.set_index("url")
    for u, t in zip(d.url, d.text):
        if u in cited:
            continue
        low = re.sub(r"\s+", " ", t).lower()
        w = low.split()
        cand = sorted({x for i in range(len(w) - 1) for x in by2.get((w[i], w[i + 1]), ())}, key=len, reverse=True)
        taken = []
        for x in cand:                                  # longest first; a shorter title inside a longer one is skipped
            mm = re.search(r"(?<![\w])" + re.escape(x) + r"(?![\w])", low)
            if mm and all(mm.end() <= a0 or mm.start() >= b0 for a0, b0 in taken):
                taken.append((mm.start(), mm.end()))
                bid = title_bill[x]
                strict.append(dict(url=u, bioguide=meta.at[u, "bioguide"], date=str(meta.at[u, "date"])[:10],
                                   bill_id=bid, title=bills.at[bid, "title"], start=mm.start(), how="title",
                                   introduced=bills.at[bid, "introduced"], sponsor=bills.at[bid, "sponsor"]))
    S = pd.DataFrame(strict)
    print(f"decision 7, strict (exact official title with 'Act', unique to one bill): {S.url.nunique():,} releases "
          f"= +{S.url.nunique() / len(d) * 100:.1f} points; title introduced after the release: "
          f"{(S.introduced > S.date).mean():.1%}")
    S.to_csv(os.path.join(OUT, "title_only_releases.csv"), index=False)

    # Decision 7 met (21 Nov): titles add 15.3 points > 5, and the blind check read 30 of 30 title links right
    # (bill_check/, score_bill_check.py). So title links join release_bills.csv, how = "title".
    S["status"] = ["other Congress" if i > dt else "resolved" for i, dt in zip(S.introduced, S.date)]
    S["releaser_role"] = [("sponsor" if sp == b else role.get((bid, b), "none")) if st == "resolved" else None
                          for sp, b, bid, st in zip(S.sponsor, S.bioguide, S.bill_id, S.status)]
    S["n_original"] = S.bill_id.map(n_orig).fillna(0).astype(int)
    S["as_written"] = S.title
    B["how"] = "number"
    ALL = pd.concat([B, S.drop(columns=["introduced"])], ignore_index=True)
    ALL.to_csv(os.path.join(OUT, "release_bills.csv"), index=False)
    RR = ALL[ALL.status == "resolved"]
    print(f"release_bills.csv: {len(ALL):,} rows; resolved {len(RR):,} in {RR.url.nunique():,} releases "
          f"({RR.url.nunique() / len(d):.1%}); by how: {RR.how.value_counts().to_dict()}; "
          f"releaser role: {RR.releaser_role.value_counts().to_dict()}")
