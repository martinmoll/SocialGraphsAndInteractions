"""Delegation check (PLAN.md, written before running): is part 3's exposure gap just "many other-party colleagues
from the same state"?

Run from project/:  python Martin/delegation_check/delegation_check.py
Reuses A4's own code (Anas/a4/analysis.py: member_table, gaps, permute) on the frozen inputs, so the outcome is
built exactly as in the paper. Writes Martin/delegation_check/results.csv and prints a readout.
"""
import os
import sys

import numpy as np
import pandas as pd

PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ANAS = os.path.join(PROJECT, "Anas")
sys.path.insert(0, os.path.join(ANAS, "a4"))
from analysis import WINDOW, gaps, member_table, permute  # noqa: E402  (A4's own functions, unchanged)

OUT = os.path.dirname(os.path.abspath(__file__))
N, SEED = 10_000, 2805

# ---- inputs, filtered exactly as analysis.py does (window, template posts left out)
d = pd.concat([pd.read_parquet(os.path.join(ANAS, "press_releases", f"press_releases_part{i}of3.parquet"),
                               columns=["url", "bioguide", "date"]) for i in (1, 2, 3)], ignore_index=True)
flags = pd.read_parquet(os.path.join(ANAS, "a3", "out", "release_flags.parquet")).set_index("url")
d["date"] = pd.to_datetime(d.date).dt.strftime("%Y-%m-%d")
rel = d[(d.date >= WINDOW[0]) & (d.date <= WINDOW[1]) & ~d.url.map(flags.template).fillna(False)][["url", "bioguide"]]
M = pd.read_parquet(os.path.join(ANAS, "a3", "out", "mentions_press.parquet"))
lean = pd.read_csv(os.path.join(ANAS, "district_lean", "member_lean.csv")).set_index("bioguide")

# ---- test 0: reproduce A4's main gaps
main = member_table(rel, M, lean)
ref = pd.read_csv(os.path.join(ANAS, "a4", "out", "member_shares.csv"), index_col=0)
assert set(main.index) == set(ref.index) and np.allclose(main.share, ref.share.reindex(main.index)), \
    "A4's member shares do not reproduce from the inputs"
g0 = gaps(main.share.values, main.party.values, main.exposed.values)
print(f"test 0: reproduced A4: {len(main)} members, R gap {g0['R'] * 100:.2f}, D gap {g0['D'] * 100:.2f} points")

# ---- delegation measures
mem = pd.read_csv(os.path.join(PROJECT, "data", "processed", "members.csv"))
mem = mem[mem.party.isin(["R", "D"])]


def delegation(m):
    """opp_n: other-party House members from the same state; opp_share: opp_n over the rest of the delegation."""
    out = {}
    for b, st, pa in m[["bioguide", "state", "party"]].itertuples(index=False):
        same = m[(m.state == st) & (m.bioguide != b)]
        opp = int((same.party != pa).sum())
        out[b] = (opp, opp / len(same) if len(same) else 0.0)
    return pd.DataFrame.from_dict(out, orient="index", columns=["opp_n", "opp_share"])


dele = delegation(mem)
dele_cur = delegation(mem[mem.current]).add_suffix("_current")
main = main.join(dele).join(dele_cur)
assert main.opp_n.notna().all(), "a member of the test is missing from members.csv"

rows = []
print("\ntest 1: other-party colleagues from the same state (mean)")
for p in ("R", "D"):
    t = main[main.party == p]
    for e in (True, False):
        s = t[t.exposed == e]
        print(f"  {p} {'exposed' if e else 'safe   '} (n={len(s):3d}): opp_n {s.opp_n.mean():5.1f}, "
              f"opp_share {s.opp_share.mean():.2f}, with none at home {int((s.opp_n == 0).sum())}")
        rows.append(dict(test="1 overlap", party=p, group="exposed" if e else "safe", n=len(s),
                         opp_n=s.opp_n.mean(), opp_share=s.opp_share.mean(), none_at_home=int((s.opp_n == 0).sum())))

# ---- test 2 and 3: drop same-state names from the outcome
other_state = member_table(rel, M[~M.same_state.fillna(False).astype(bool)], lean)
other_state = other_state.reindex(main.index)
lost = (main.named - other_state.named)                       # releases that counted only because of same-state names
print("\ntest 2: releases that count only because they name an other-party member from the same state")
for p in ("R", "D"):
    for e in (True, False):
        m_ = (main.party == p) & (main.exposed == e)
        share_lost = lost[m_].sum() / main.named[m_].sum()
        print(f"  {p} {'exposed' if e else 'safe   '}: {share_lost * 100:4.1f}% of counted releases")
        rows.append(dict(test="2 same-state only", party=p, group="exposed" if e else "safe",
                         share_of_counted=share_lost))

obs3, p3, _ = permute(other_state)
print("\ntest 3: outcome without same-state names (within-party shuffle, 10,000)")
for p in ("R", "D"):
    t = other_state[other_state.party == p]
    ex, sa = t.share[t.exposed].mean(), t.share[~t.exposed].mean()
    print(f"  {p}: exposed {ex * 100:.1f}%, safe {sa * 100:.1f}%, gap {obs3[p] * 100:.2f} points "
          f"(was {g0[p] * 100:.2f}), p = {p3[p]:.4f}")
    rows.append(dict(test="3 without same-state names", party=p, exposed_share=ex, safe_share=sa, observed=obs3[p],
                     p=p3[p], main_gap=g0[p]))


# ---- test 4 and 5: shuffle exposure within party and delegation band (as Anas/a4/ideology_check.py)
def gap(s, e):
    return s[e].mean() - s[~e].mean()


def banded(t, col, k):
    """Within each party: observed gap, the mean gap the bands alone give, what is beyond it, and its p."""
    res = {}
    for p in ("R", "D"):
        g = t[t.party == p]
        s, e = g.share.values, g.exposed.values.astype(bool)
        band = pd.qcut(g[col], k, labels=False, duplicates="drop").values
        nb = int(np.nanmax(band)) + 1
        per = ", ".join(f"{int(e[band == b].sum())}/{int((band == b).sum())}" for b in range(nb))
        rng = np.random.default_rng(SEED)
        null = np.empty(N)
        idx = [np.where(band == b)[0] for b in range(nb)]
        for i in range(N):
            ee = e.copy()
            for ix in idx:
                ee[ix] = rng.permutation(e[ix])
            null[i] = gap(s, ee)
        obs, mu = gap(s, e), null.mean()
        pv = float((np.abs(null - mu) >= abs(obs - mu) - 1e-12).mean())
        res[p] = dict(observed=obs, null_mean=mu, beyond=obs - mu, p=pv, bands=nb, per_band=per)
    return res


print("\ntests 4 and 5: exposure shuffled within party and delegation band (10,000)")
print("  (points; 'from delegation' = mean gap the bands alone give; 'beyond' = observed minus that)")
for label, t in (("4 main outcome", main), ("5 without same-state names", other_state.join(dele).join(dele_cur))):
    for col in ("opp_share", "opp_n", "opp_share_current"):
        for k in (5, 3):
            r = banded(t, col, k)
            for p in ("R", "D"):
                x = r[p]
                print(f"  {label:27s} {col:17s} k={k} ({x['bands']} bands) {p}: observed {x['observed'] * 100:5.2f}, "
                      f"from delegation {x['null_mean'] * 100:5.2f}, beyond {x['beyond'] * 100:5.2f}, p = {x['p']:.4f}"
                      f"   [exposed/members per band, few to many at home: {x['per_band']}]")
                rows.append(dict(test=label, party=p, band_on=col, k=k, **x))

pd.DataFrame(rows).to_csv(os.path.join(OUT, "results.csv"), index=False)
print(f"\n-> {os.path.join(OUT, 'results.csv')}")
