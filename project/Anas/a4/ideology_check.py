"""Check I (a4/CHECKS_PLAN_23NOV.md, fixed before computing): is "exposed" just "moderate"?
Run from Anas/ after a4/analysis.py:  python -I a4/ideology_check.py --repo <project/ of the group repo>
Statistic: A4's gap (mean share exposed - safe, within each party), unchanged.
Null A: exposed shuffled among a party's members (A4 as reported; rerun here as a check of this code).
Null B: exposed shuffled only within the same party and ideology band (quintiles, and terciles as robustness, of
extremity = DW-NOMINATE dim1 for R, -dim1 for D). Null B's mean is the gap ideology alone gives.
p (null B) = share of shuffles with |null - mean(null)| >= |observed - mean(null)| (as in NETWORK_METHODS.md).
10,000 shuffles, seed 2805. Writes a4/out/ideology_check.csv.
"""
import argparse
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
N, SEED = 10_000, 2805


def gap(s, e):
    return s[e].mean() - s[~e].mean()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    a = ap.parse_args()
    t = pd.read_csv(os.path.join(OUT, "member_shares.csv"), index_col=0)
    m = pd.read_csv(os.path.join(a.repo, "data", "processed", "members.csv")).set_index("bioguide")
    t["dim1"] = m.nominate_dim1.reindex(t.index)
    assert t.dim1.notna().all(), "a member has no NOMINATE score"
    t["extremity"] = np.where(t.party == "R", t.dim1, -t.dim1)
    t["exposed"] = t.exposed.astype(bool)

    rows = []
    for party in ("R", "D"):
        g = t[t.party == party]
        s, e = g.share.values, g.exposed.values
        obs = gap(s, e)
        rng = np.random.default_rng(SEED)
        nullA = np.array([gap(s, rng.permutation(e)) for _ in range(N)])
        pA = float((np.abs(nullA) >= abs(obs) - 1e-12).mean())
        rows.append(dict(party=party, null="A: within party (A4)", bands=1, observed=obs, null_mean=nullA.mean(),
                         beyond=obs - nullA.mean(), p=pA, exposed=int(e.sum()), safe=int((~e).sum()), note=""))
        for k, name in ((5, "quintiles"), (3, "terciles")):
            band = pd.qcut(g.extremity, k, labels=False).values
            per = ", ".join(f"{int(e[band == b].sum())}/{int((band == b).sum())}" for b in range(k))
            rng = np.random.default_rng(SEED)
            nullB = np.empty(N)
            for i in range(N):
                ee = e.copy()
                for b in range(k):
                    ix = np.where(band == b)[0]
                    ee[ix] = rng.permutation(e[ix])
                nullB[i] = gap(s, ee)
            mu = nullB.mean()
            pB = float((np.abs(nullB - mu) >= abs(obs - mu) - 1e-12).mean())
            rows.append(dict(party=party, null=f"B: within party and ideology {name}", bands=k, observed=obs,
                             null_mean=mu, beyond=obs - mu, p=pB, exposed=int(e.sum()), safe=int((~e).sum()),
                             note=f"exposed/members per band, moderate to extreme: {per}"))
    R = pd.DataFrame(rows)
    R.to_csv(os.path.join(OUT, "ideology_check.csv"), index=False)
    pd.set_option("display.width", 220)
    show = R.assign(**{c: (R[c] * 100).round(2) for c in ("observed", "null_mean", "beyond")}, p=R.p.round(4))
    print(show[["party", "null", "observed", "null_mean", "beyond", "p", "note"]].to_string(index=False))
    print("\n(observed, null_mean, beyond in percentage points)")
