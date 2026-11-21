"""POST HOC (added 21 Nov after seeing home_network.py's results): S2 and S3 under a degree-matched null.

Run from Anas/ after home_network.py:  python a4/home_network_posthoc.py
Why: the planned null shuffles exposure within party, which also moves the label away from members with many
cross-party ties. Exposed members have more such ties (A4), so S2 (share of ties joining two exposed members) can
exceed that null just because exposed members are hubs. HOME_NETWORK_PLAN.md wrongly said the planned null rules
this out. This check shuffles exposure within party AND within quintiles of cross-party degree, so exposed and safe
members of similar activity swap labels. It is reported as post hoc, next to (not instead of) the planned test.
Also reports the share of cross-party tie ends held by exposed members.
"""
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import home_network as H

OUT, ANAS = H.OUT, H.ANAS
N, SEED = 10_000, 2805

if __name__ == "__main__":
    t = pd.read_csv(os.path.join(OUT, "member_shares.csv"), index_col=0)
    M = pd.read_parquet(os.path.join(ANAS, "a3", "out", "mentions_press.parquet"))
    rows = []
    for label, kw in [("main", {}), ("ties >= 2 releases", {"min_rel": 2}), ("co-leads left out", {"coleads": False})]:
        row, pairs, U, D = H.run(t, M, label, **kw)
        x = t.exposed.values.astype(bool)
        party = t.party.values
        deg = np.bincount(U.ravel(), minlength=len(t))
        ends_exposed = deg[x].sum() / deg.sum()
        strata = []
        for p in ("R", "D"):
            ix = np.where(party == p)[0]
            q = pd.qcut(deg[ix], 5, labels=False, duplicates="drop")
            strata += [ix[q == k] for k in np.unique(q)]
        obs = H.stats(x, U, D)
        rng = np.random.default_rng(SEED)
        null = np.empty((N, 4))
        for i in range(N):
            y = x.copy()
            for g in strata:
                y[g] = rng.permutation(x[g])
            null[i] = H.stats(y, U, D)
        pv = [(np.abs(null[:, k] - null[:, k].mean()) >= abs(obs[k] - null[:, k].mean()) - 1e-12).mean() for k in range(4)]
        rows.append(dict(check=label, exposed_share_of_members=x.mean(), exposed_share_of_tie_ends=ends_exposed,
                         S2=obs[1], S2_null_degree_matched=null[:, 1].mean(), S2_ratio=obs[1] / null[:, 1].mean(), p_S2=pv[1],
                         S3=obs[2], S3_null=null[:, 2].mean(), p_S3=pv[2]))
        r = rows[-1]
        print(f"== {label}: exposed = {r['exposed_share_of_members']:.1%} of members, {r['exposed_share_of_tie_ends']:.1%} of "
              f"cross-party tie ends")
        print(f"   S2 {r['S2']:.1%} vs degree-matched null {r['S2_null_degree_matched']:.1%} (x{r['S2_ratio']:.2f}), p {r['p_S2']:.4f}")
        print(f"   S3 {r['S3']:+.3f} vs null {r['S3_null']:+.3f}, p {r['p_S3']:.4f}")
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "home_network_posthoc.csv"), index=False)
