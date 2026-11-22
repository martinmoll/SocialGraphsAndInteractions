"""A4 extension: the home network of cross-party showing. Design fixed in HOME_NETWORK_PLAN.md before computing.

Run from Anas/ after a4/analysis.py:  python a4/home_network.py
Nodes: the 406 members of the A4 test (a4/out/member_shares.csv). Directed tie A -> B: A named B in at least
MIN_REL releases (a3/out/mentions_press.parquet; leaders as the named member left out; co-leads kept). Cross-party
network: R-D ties. Statistics S1 to S4 and the shared null (exposure shuffled within party, 10,000, seed 2805) as
in the plan. Writes a4/out/home_network.csv (all rows), home_ties.csv (the cross-party ties of the main row).
"""
import os

import networkx as nx
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ANAS = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")
N_PERM, SEED = 10_000, 2805


def assort_binary(eu, ev, x):
    """Attribute assortativity of an undirected graph for a 0/1 attribute (same as networkx's for two classes)."""
    a, b = np.concatenate([x[eu], x[ev]]), np.concatenate([x[ev], x[eu]])      # both ends of every edge
    e11, e00 = np.mean(a & b), np.mean(~a & ~b)
    p1 = a.mean()
    s = p1 ** 2 + (1 - p1) ** 2
    return (e11 + e00 - s) / (1 - s) if s < 1 else np.nan


def stats(x, U, D):
    """x: exposed per node (bool). U: undirected cross-party edges (u, v). D: directed cross-party edges with
    columns s, t, recip, same_state."""
    s1 = assort_binary(U[:, 0], U[:, 1], x)
    s2 = np.mean(x[U[:, 0]] & x[U[:, 1]])
    ee = x[D.s] & x[D.t]
    s3 = D.recip[ee].mean() - D.recip[~ee].mean() if ee.any() and (~ee).any() else np.nan
    ex = x[D.s]
    s4 = D.same_state[~ex].mean() - D.same_state[ex].mean()
    return np.array([s1, s2, s3, s4])


def run(t, M, label, min_rel=1, coleads=True, exposed_col="exposed"):
    idx = {b: i for i, b in enumerate(t.index)}
    party = t.party.values
    m = M[M.speaker.isin(idx) & M.named.isin(idx) & ~M.named_is_leader]
    if not coleads:
        m = m[~m.co_lead]
    pairs = m.groupby(["speaker", "named"]).size().rename("releases").reset_index()
    pairs = pairs[pairs.releases >= min_rel]
    pairs["s"], pairs["t"] = pairs.speaker.map(idx), pairs.named.map(idx)
    pairs = pairs[party[pairs.s] != party[pairs.t]].copy()                    # cross-party only
    key = set(zip(pairs.s, pairs.t))
    D = pd.DataFrame({"s": pairs.s.values, "t": pairs.t.values,
                      "recip": [(b, a) in key for a, b in zip(pairs.s, pairs.t)],
                      "same_state": t.state.values[pairs.s.values] == t.state.values[pairs.t.values]})
    D = {k: D[k].values for k in D}
    D = pd.Series(D)
    U = np.array(sorted({tuple(sorted(e)) for e in key}))
    x = t[exposed_col].values.astype(bool)
    obs = stats(x, U, D)
    rng = np.random.default_rng(SEED)
    groups = [np.where(party == p)[0] for p in ("R", "D")]
    null = np.empty((N_PERM, 4))
    for i in range(N_PERM):
        y = x.copy()
        for g in groups:
            y[g] = rng.permutation(x[g])
        null[i] = stats(y, U, D)
    p = [(np.abs(null[:, k] - np.nanmean(null[:, k])) >= abs(obs[k] - np.nanmean(null[:, k])) - 1e-12).mean()
         for k in range(4)]
    # descriptives
    ee_u = x[U[:, 0]] & x[U[:, 1]]
    row = dict(check=label, nodes=len(t), cross_ties=len(U), directed=len(pairs), mutual_pairs=int(D.recip.sum() / 2),
               S1_assortativity=obs[0], S1_null=np.nanmean(null[:, 0]), p_S1=p[0],
               S2_share_exposed_exposed=obs[1], S2_null=np.nanmean(null[:, 1]), S2_ratio=obs[1] / np.nanmean(null[:, 1]),
               p_S2=p[1],
               S3_recip_EE_minus_other=obs[2], recip_EE=D.recip[x[D.s] & x[D.t]].mean(),
               recip_other=D.recip[~(x[D.s] & x[D.t])].mean(), p_S3=p[2],
               S4_samestate_safe_minus_exposed=obs[3], samestate_safe=D.same_state[~x[D.s]].mean(),
               samestate_exposed=D.same_state[x[D.s]].mean(), p_S4=p[3],
               EE_ties=int(ee_u.sum()), EE_mutual=int((D.recip & x[D.s] & x[D.t]).sum() / 2))
    return row, pairs, U, D


if __name__ == "__main__":
    t = pd.read_csv(os.path.join(OUT, "member_shares.csv"), index_col=0)
    lean = pd.read_csv(os.path.join(ANAS, "district_lean", "member_lean.csv")).set_index("bioguide")
    own = np.where(lean.party == "R", lean.lean_2025, -lean.lean_2025)
    for c in (4, 6):
        lean[f"exposed_c{c}"] = own <= c
        t[f"exposed_c{c}"] = lean[f"exposed_c{c}"].reindex(t.index)
    M = pd.read_parquet(os.path.join(ANAS, "a3", "out", "mentions_press.parquet"))
    rows = []
    main, pairs, U, D = run(t, M, "main: ties >= 1 release, co-leads kept, cut-off 5")
    rows.append(main)
    rows.append(run(t, M, "ties >= 2 releases", min_rel=2)[0])
    rows.append(run(t, M, "co-leads left out", coleads=False)[0])
    rows.append(run(t, M, "cut-off 4", exposed_col="exposed_c4")[0])
    rows.append(run(t, M, "cut-off 6", exposed_col="exposed_c6")[0])
    R = pd.DataFrame(rows)
    R.to_csv(os.path.join(OUT, "home_network.csv"), index=False)
    names = pd.read_csv(os.path.join(ANAS, "district_lean", "member_lean.csv")).set_index("bioguide").name
    pairs.assign(speaker_name=pairs.speaker.map(names), named_name=pairs.named.map(names),
                 mutual=pairs.apply(lambda r: ((r.t, r.s) in set(zip(pairs.s, pairs.t))), axis=1),
                 speaker_exposed=pairs.speaker.map(t.exposed), named_exposed=pairs.named.map(t.exposed)) \
        .drop(columns=["s", "t"]).to_csv(os.path.join(OUT, "home_ties.csv"), index=False)
    pd.set_option("display.width", 220)
    for r in rows:
        print(f"\n== {r['check']} ==  nodes {r['nodes']}, cross-party ties {r['cross_ties']} (directed {r['directed']}, "
              f"mutual pairs {r['mutual_pairs']})")
        print(f"  S1 exposure assortativity {r['S1_assortativity']:+.3f} (null {r['S1_null']:+.3f}), p {r['p_S1']:.4f}")
        print(f"  S2 ties joining two exposed members {r['S2_share_exposed_exposed']:.1%} (null {r['S2_null']:.1%}, "
              f"x{r['S2_ratio']:.2f}), p {r['p_S2']:.4f}; {r['EE_ties']} ties, {r['EE_mutual']} mutual")
        print(f"  S3 reciprocity exposed-exposed {r['recip_EE']:.1%} vs other {r['recip_other']:.1%} "
              f"(diff {r['S3_recip_EE_minus_other']:+.3f}), p {r['p_S3']:.4f}")
        print(f"  S4 same-state share: safe speakers {r['samestate_safe']:.1%} vs exposed {r['samestate_exposed']:.1%} "
              f"(diff {r['S4_samestate_safe_minus_exposed']:+.3f}), p {r['p_S4']:.4f}")
