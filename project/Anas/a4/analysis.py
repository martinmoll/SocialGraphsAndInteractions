"""A4: do members in exposed seats name the other party more at home, and does that differ by party?

Run from Anas/:  python a4/analysis.py --press press_releases --repo <project/ of the group repo>

Implements the A4 analysis plan in ../methods_drafts.md (written 20 Nov, before any release text was analysed):

  unit      one member (R or D) with a 2025 lean and at least MIN_RELEASES releases in the window
  outcome   share of the member's releases (template posts left out) naming at least one House member of the
            other party who is neither a co-lead of a bill the release cites nor a party leader
            (from a3/out/mentions_press.parquet: cross_party, co_lead, named_is_leader)
  groups    party x exposed_2025 (district_lean/member_lean.csv): a Republican is exposed when the lean of the
            district served is R+5 or less, a Democrat when it is D+5 or less (lean_2025 <= 5 / >= -5)
  tested    the R gap (exposed - safe), the D gap, and the interaction (R gap - D gap)
  test      permutation: exposed_2025 shuffled among the members of each party, 10,000 times, seed 2805;
            two-sided p = share of shuffles with |value| >= |observed|
Robustness rows (each the same test), all fixed in methods_drafts.md:
  check 1 without the 21 members whose 2026 label differs or is unknown; check 2 without redistricting releases;
  check 4 cut-offs +-4 and +-6, and lean as a number (within-party slope of the share on own-party lean);
  the second lean source (2024 presidential margin); without caucus releases; the outcome with co-leads kept;
  Martin's matcher alone (in_shared, decision 3); leave one state out.
The window is the full snapshot (3 Jan 2025 to 20 Nov 2026) until the group fixes it (G13/G7). Writes a4/out/.
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ANAS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ANAS, "a3"))
from common import OUT as A3OUT, load_inputs

MIN_RELEASES, N_PERM, SEED = 10, 10_000, 2805
WINDOW = ("2025-01-03", "2026-11-20")
OUTDIR = os.path.join(HERE, "out")


def member_table(rel, M, lean, *, drop_releases=None, keep_coleads=False, shared_only=False, exposed="exposed_2025"):
    """One row per member: party, exposed, releases, share naming the other side."""
    r = rel if drop_releases is None else rel[~rel.url.isin(drop_releases)]
    x = M[M.doc_id.isin(set(r.url)) & M.cross_party.fillna(False).astype(bool) & ~M.named_is_leader]
    if not keep_coleads:
        x = x[~x.co_lead]
    if shared_only:
        x = x[x.in_shared]
    hit = set(x.doc_id)
    t = r.assign(hit=r.url.isin(hit)).groupby("bioguide").agg(releases=("url", "size"), named=("hit", "sum"))
    t["share"] = t.named / t.releases
    t = t.join(lean[["party", "state", "lean_2025", exposed]].rename(columns={exposed: "exposed"}), how="inner")
    t = t[t.party.isin(["R", "D"]) & t.exposed.notna() & (t.releases >= MIN_RELEASES)]
    t["exposed"] = t.exposed.astype(bool)
    return t


def gaps(share, party, exposed):
    out = {}
    for p in ("R", "D"):
        s, e = share[party == p], exposed[party == p]
        out[p] = s[e].mean() - s[~e].mean()
    out["interaction"] = out["R"] - out["D"]
    return out


def permute(t, n=N_PERM, seed=SEED):
    """Shuffle exposure within each party; return observed gaps, p-values and the null draws."""
    rng = np.random.default_rng(seed)
    share, party, exp = t.share.values, t.party.values, t.exposed.values
    obs = gaps(share, party, exp)
    null = {k: np.empty(n) for k in obs}
    idx = {p: np.where(party == p)[0] for p in ("R", "D")}
    for i in range(n):
        e = exp.copy()
        for p, ix in idx.items():
            e[ix] = rng.permutation(exp[ix])
        g = gaps(share, party, e)
        for k in g:
            null[k][i] = g[k]
    p = {k: float((np.abs(null[k]) >= abs(obs[k]) - 1e-12).mean()) for k in obs}
    return obs, p, null


def slope_test(t, n=N_PERM, seed=SEED):
    """Lean as a number: within each party, OLS slope of share on own-party lean (points of safety)."""
    rng = np.random.default_rng(seed)
    safety = np.where(t.party == "R", t.lean_2025, -t.lean_2025)
    out = {}
    for p in ("R", "D"):
        m = (t.party == p).values
        x, y = safety[m], t.share.values[m]
        b = np.polyfit(x, y, 1)[0]
        null = np.array([np.polyfit(rng.permutation(x), y, 1)[0] for _ in range(2000)])
        out[p] = (b, float((np.abs(null) >= abs(b)).mean()))
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--press", required=True)
    ap.add_argument("--repo", required=True)
    a = ap.parse_args()
    os.makedirs(OUTDIR, exist_ok=True)
    d, members, *_ = load_inputs(a.press, a.repo)
    flags = pd.read_parquet(os.path.join(A3OUT, "release_flags.parquet")).set_index("url")
    d["date"] = pd.to_datetime(d.date).dt.strftime("%Y-%m-%d")
    rel = d[(d.date >= WINDOW[0]) & (d.date <= WINDOW[1]) & ~d.url.map(flags.template).fillna(False)][["url", "bioguide"]]
    M = pd.read_parquet(os.path.join(A3OUT, "mentions_press.parquet"))
    lean = pd.read_csv(os.path.join(ANAS, "district_lean", "member_lean.csv")).set_index("bioguide")
    # cut-offs (check 4): exposed when the lean toward the member's own party is at most c points
    own = np.where(lean.party == "R", lean.lean_2025, -lean.lean_2025)
    for c in (4, 5, 6):
        lean[f"exposed_c{c}"] = np.where(lean.lean_2025.isna(), np.nan, own <= c)
    assert (lean.exposed_c5.dropna().astype(bool) == lean.exposed_2025[lean.exposed_c5.notna()].astype(bool)).all(), \
        "exposed_2025 is not 'own-party lean <= 5'"
    relabelled = lean.index[(lean.exposed_2026.isna() | (lean.exposed_2026 != lean.exposed_2025)) & lean.exposed_2025.notna()]

    # releases dropped by checks
    rd = set(M[M.redistricting].doc_id) | set(d.url[d.text.str.contains(r"\bredistrict|\bgerrymander", case=False, regex=True)])
    ca = set(M[M.caucus].doc_id)

    main = member_table(rel, M, lean)
    main.to_csv(os.path.join(OUTDIR, "member_shares.csv"))
    obs, p, null = permute(main)
    np.save(os.path.join(OUTDIR, "null_main.npy"), np.vstack([null["R"], null["D"], null["interaction"]]))
    rows = [("main: exposed_2025 (own-party lean <= 5)", main, obs, p)]

    def add(label, t):
        o, pp, _ = permute(t)
        rows.append((label, t, o, pp))

    add("check 4: cut-off +-4", member_table(rel, M, lean, exposed="exposed_c4"))
    add("check 4: cut-off +-6", member_table(rel, M, lean, exposed="exposed_c6"))
    add("second lean source: 2024 presidential margin", member_table(rel, M, lean, exposed="exposed_pres"))
    add(f"check 1: without the {len(relabelled)} relabelled or unknown in 2026", main.drop(relabelled, errors="ignore"))
    add("check 2: without redistricting releases", member_table(rel, M, lean, drop_releases=rd))
    add("without caucus releases", member_table(rel, M, lean, drop_releases=ca))
    add("outcome with co-leads kept", member_table(rel, M, lean, keep_coleads=True))
    add("Martin's matcher alone (shared)", member_table(rel, M, lean, shared_only=True))

    res = []
    for label, t, o, pp in rows:
        g = t.groupby(["party", "exposed"]).share.agg(["mean", "size"])
        res.append(dict(check=label, n_R_exposed=int(g.loc[("R", True), "size"]), n_R_safe=int(g.loc[("R", False), "size"]),
                        n_D_exposed=int(g.loc[("D", True), "size"]), n_D_safe=int(g.loc[("D", False), "size"]),
                        R_exposed=g.loc[("R", True), "mean"], R_safe=g.loc[("R", False), "mean"],
                        D_exposed=g.loc[("D", True), "mean"], D_safe=g.loc[("D", False), "mean"],
                        R_gap=o["R"], p_R=pp["R"], D_gap=o["D"], p_D=pp["D"], interaction=o["interaction"],
                        p_interaction=pp["interaction"]))
    R = pd.DataFrame(res)
    # leave one state out: range of the three quantities
    loso = []
    for s in sorted(main.state.unique()):
        t = main[main.state != s]
        g = gaps(t.share.values, t.party.values, t.exposed.values)
        loso.append(dict(state=s, **g))
    L = pd.DataFrame(loso)
    L.to_csv(os.path.join(OUTDIR, "leave_one_state_out.csv"), index=False)
    sl = slope_test(main)
    R.to_csv(os.path.join(OUTDIR, "results.csv"), index=False)

    pd.set_option("display.width", 200)
    print(f"window {WINDOW}; members in the test: {len(main)} (min {MIN_RELEASES} releases); "
          f"releases {int(main.releases.sum()):,}")
    show = R[["check", "n_R_exposed", "n_R_safe", "n_D_exposed", "n_D_safe", "R_exposed", "R_safe", "D_exposed",
              "D_safe", "R_gap", "p_R", "D_gap", "p_D", "interaction", "p_interaction"]]
    print(show.round(3).to_string(index=False))
    print(f"\nleave one state out (min to max): R gap {L.R.min():.3f} to {L.R.max():.3f}; D gap {L.D.min():.3f} to "
          f"{L.D.max():.3f}; interaction {L.interaction.min():.3f} to {L.interaction.max():.3f}")
    print(f"lean as a number (slope of share per point of own-party lean; negative = safer seats name the other side "
          f"less): R {sl['R'][0]:.4f} (p {sl['R'][1]:.3f}), D {sl['D'][0]:.4f} (p {sl['D'][1]:.3f})")
    pd.DataFrame([dict(party=k, slope=v[0], p=v[1]) for k, v in sl.items()]).to_csv(os.path.join(OUTDIR, "lean_slope.csv"), index=False)
