"""A5: does a release that says "bipartisan" name a real cross-party partner? Design: a5/PLAN.md (fixed first).

Run from Anas/:  python a5/analysis.py --press press_releases --repo <project/ of the group repo>
Inputs are A3's frozen inputs (checked by a3/common.load_inputs) and A3/A4 outputs: a3/out/mentions_press.parquet,
a3/out/release_bills.csv, a3/out/release_flags.parquet, a3/out/repeated_sentences.csv, a4/out/member_shares.csv
(the A4 members), district_lean/member_lean.csv, and the repo's cosponsors.parquet and bills.parquet.
Writes a5/out/results.csv, a5/out/member_shares.csv, a5/out/release_flags.parquet and the reading-check draw
a5/check/draw.csv (30 "bipartisan" releases with no partner on either measure, seed 2805).
"""
import argparse
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ANAS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ANAS, "a3"))
from common import OUT as A3OUT, load_inputs  # noqa: E402

OUT = os.path.join(HERE, "out")
CHECK = os.path.join(HERE, "check")
WINDOW = ("2025-01-03", "2026-11-20")
WORD = re.compile(r"\bbi-?partisan", re.I)
MIN_BIP, N_PERM, SEED, N_CHECK = 5, 10_000, 2805, 30


def permute_gap(t, col):
    """Exposed minus safe mean of col within each party; two-sided p from shuffling exposure within party (as A4)."""
    rng = np.random.default_rng(SEED)
    out = {}
    for p in ("R", "D"):
        s = t[t.party == p]
        v, e = s[col].values, s.exposed.values.astype(bool)
        obs = v[e].mean() - v[~e].mean()
        null = np.array([(lambda ee: v[ee].mean() - v[~ee].mean())(rng.permutation(e)) for _ in range(N_PERM)])
        out[p] = (v[e].mean(), v[~e].mean(), obs, float((np.abs(null) >= abs(obs) - 1e-12).mean()), int(e.sum()),
                  int((~e).sum()))
    return out


def paired_signflip(diff):
    """Two-sided p for a mean paired difference, by flipping signs at random."""
    rng = np.random.default_rng(SEED)
    obs = diff.mean()
    null = np.array([(diff * rng.choice([-1, 1], len(diff))).mean() for _ in range(N_PERM)])
    return float((np.abs(null) >= abs(obs) - 1e-12).mean())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--press", required=True)
    ap.add_argument("--repo", required=True)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(CHECK, exist_ok=True)
    d, members, *_ = load_inputs(a.press, a.repo)
    party = members.set_index("bioguide").party.to_dict()
    name = members.set_index("bioguide").name.to_dict()

    # 1. releases in the window, templates out; "says bipartisan" after removing the member's repeated sentences
    flags = pd.read_parquet(os.path.join(A3OUT, "release_flags.parquet")).set_index("url")
    d["date"] = pd.to_datetime(d.date).dt.strftime("%Y-%m-%d")
    d = d[(d.date >= WINDOW[0]) & (d.date <= WINDOW[1]) & ~d.url.map(flags.template).fillna(False)].copy()
    rep = pd.read_csv(os.path.join(A3OUT, "repeated_sentences.csv")).groupby("bioguide").sentence.apply(list).to_dict()

    def own_text(b, title, text):
        t = text or ""
        for sent in rep.get(b, []):
            t = t.replace(sent, " ")
        return (title or "") + " \n " + t

    d["says"] = [bool(WORD.search(own_text(b, ti, tx))) for b, ti, tx in zip(d.bioguide, d.title, d.text)]
    d["says_raw"] = [bool(WORD.search((ti or "") + " " + (tx or ""))) for ti, tx in zip(d.title, d.text)]

    # 2a. named partner: a House member of the other party named in the release, leaders left out, co-leads kept
    M = pd.read_parquet(os.path.join(A3OUT, "mentions_press.parquet"))
    named = set(M[M.cross_party.fillna(False).astype(bool) & ~M.named_is_leader].doc_id)
    d["named"] = d.url.isin(named)

    # 2b. partner on record: a cited House bill whose sponsor or a non-withdrawn original cosponsor is of the other party
    rb = pd.read_csv(os.path.join(A3OUT, "release_bills.csv"))
    rb = rb[rb.status == "resolved"]
    cos = pd.read_parquet(os.path.join(a.repo, "data", "processed", "cosponsors.parquet"))
    bills = pd.read_parquet(os.path.join(a.repo, "data", "processed", "bills.parquet"))
    leads = pd.concat([bills[["bill_id", "sponsor"]].rename(columns={"sponsor": "m"}),
                       cos[cos.original & ~cos.withdrawn][["bill_id", "cosponsor"]].rename(columns={"cosponsor": "m"})])
    leads["p"] = leads.m.map(party)
    bill_parties = leads.dropna(subset=["p"]).groupby("bill_id").p.apply(set).to_dict()
    rb = rb.assign(rp=rb.bioguide.map(party))
    rb["other"] = [rp in ("R", "D") and bool(bill_parties.get(bi, set()) & ({"R", "D"} - {rp}))
                   for bi, rp in zip(rb.bill_id, rb.rp)]
    on_record = set(rb[rb.other].url)
    d["on_record"] = d.url.isin(on_record)
    d["cites_house_bill"] = d.url.isin(set(rb.url))
    d["either"] = d.named | d.on_record
    d[["url", "bioguide", "date", "says", "says_raw", "named", "on_record", "either", "cites_house_bill"]].to_parquet(
        os.path.join(OUT, "release_flags.parquet"), index=False)

    # 3. member shares, A4's members (>= 10 releases, with lean), at least MIN_BIP "bipartisan" releases
    a4 = pd.read_csv(os.path.join(ANAS, "a4", "out", "member_shares.csv"), index_col=0)
    x = d[d.bioguide.isin(a4.index)]
    g = x.groupby(["bioguide", "says"])
    parts = []
    for k in ("either", "named", "on_record"):
        u = g[k].mean().unstack().rename(columns={True: f"{k}_bip", False: f"{k}_other"})
        parts.append(u)
    t = pd.concat(parts, axis=1)
    t["n_bip"] = x[x.says].groupby("bioguide").size()
    t["n_other"] = x[~x.says].groupby("bioguide").size()
    t = t.join(a4[["party", "exposed"]], how="inner")
    t = t[(t.n_bip >= MIN_BIP) & (t.n_other >= 1)]
    t.to_csv(os.path.join(OUT, "member_shares.csv"))

    rows = []
    for k in ("either", "named", "on_record"):
        diff = (t[f"{k}_bip"] - t[f"{k}_other"]).values
        rows.append(dict(measure=k, members=len(t), member_mean_bip=t[f"{k}_bip"].mean(),
                         member_mean_other=t[f"{k}_other"].mean(), paired_diff=diff.mean(), p_paired=paired_signflip(diff),
                         pooled_bip=x[x.says][k].mean(), pooled_other=x[~x.says][k].mean(),
                         releases_bip=int(x.says.sum()), releases_other=int((~x.says).sum())))
    seat = permute_gap(t.assign(exposed=t.exposed.astype(bool)), "either_bip")
    for p, (me, ms, gap, pv, ne, ns) in seat.items():
        rows.append(dict(measure=f"either, bipartisan releases, {p}: exposed vs safe", members=ne + ns,
                         member_mean_bip=me, member_mean_other=ms, paired_diff=gap, p_paired=pv))
    R = pd.DataFrame(rows)
    R.to_csv(os.path.join(OUT, "results.csv"), index=False)

    # 4. the reading check: 30 "bipartisan" releases of A4 members with no partner on either measure
    pool = x[x.says & ~x.either]
    draw = pool.sample(N_CHECK, random_state=SEED)[["url", "bioguide", "date", "title", "text"]]
    draw.insert(0, "item", [f"a5_{i + 1:02d}" for i in range(len(draw))])
    draw["member"] = draw.bioguide.map(name)
    draw["member_party"] = draw.bioguide.map(party)
    draw.to_csv(os.path.join(CHECK, "draw.csv"), index=False)

    pd.set_option("display.width", 200)
    print(f"releases (A4 members, window, no templates): {len(x):,}; say bipartisan: {int(x.says.sum()):,} "
          f"({x.says.mean():.1%}); raw word incl. repeated sentences: {int(x.says_raw.sum()):,}")
    print(f"members with >= {MIN_BIP} bipartisan releases: {len(t)} of {x.bioguide.nunique()}")
    print(R.round(4).to_string(index=False))
    print(f"\npartner-less bipartisan releases: {len(pool):,} ({len(pool) / x.says.sum():.1%}); check draw: {len(draw)}")
    print("of the partner-less, citing a House bill at all:", f"{pool.cites_house_bill.mean():.1%}")
