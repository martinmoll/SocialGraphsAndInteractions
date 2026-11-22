"""M6: the null for the close-up. Of a member's own bills, are the cross-party ones announced at home more often
than a random draw of that member's bills would be?

Run from project/:  python Martin/m6_closeup_null.py        (about a minute)
Reads data/processed/ (bills, cosponsors, members), Anas's release-to-bill table (Anas/a3/out/release_bills.csv,
A3.5) and the press releases (Anas/press_releases/, only to know whose releases were collected).
Writes Martin/m6_results.csv.

Choices (agreed by Martin 22 Nov, DECISIONS G20):
  1. A member's own bills: the bills they sponsored (main). Robustness: the bills they were an original cosponsor of.
  2. Bill types hr and hjres, as in the working map (M3). Robustness: all four House types (with hres, hconres).
  3. Cross-party bill: at least one original cosponsor (not withdrawn) from the other party, i.e. a bipartisan
     co-lead at introduction. For the original-cosponsor robustness row: the sponsor or another original cosponsor
     is from the other party. Robustness: any cosponsor from the other party, at any time.
  4. Announced: at least one of the member's releases cites the bill (A3.5 status "resolved"; by number or exact
     title). Window: all releases collected, 3 Jan 2025 to 20 Nov 2026 (Anas's proposal for G13, accepted).
  5. Members: Republicans and Democrats with collected releases and at least 3 own bills of whom at least one is
     cross-party and one is not (only those members carry information for this test).
  6. Null: within each member, shuffle which of their own bills are cross-party (10,000 shuffles, seed 2805). It keeps
     how many bills each member announces and how many cross-party bills they have, and removes only the link
     between the two. Statistic: the number of announced cross-party bills, summed over members. p is one-sided
     (more than the null) and two-sided.
  7. Checks: Republicans and Democrats separately; only bills with at least one original cosponsor (so the test is
     cross-party co-leads against same-party co-leads, not against solo bills); only bills found by number (not by
     title); members with at least 10 releases.

Not controlled: whether a bill moved (passed the House, became law). Bills that move are announced more, and
bipartisan bills may move more often; the data has no status field, so this is a limitation, not a check.
"""
import glob
import numpy as np, pandas as pd

DATA, SEED, N = "data/processed", 2805, 10_000
members = pd.read_csv(f"{DATA}/members.csv").set_index("bioguide")
party = members.party[members.party.isin(["R", "D"])]
bills = pd.read_parquet(f"{DATA}/bills.parquet")
cos = pd.read_parquet(f"{DATA}/cosponsors.parquet")
cos = cos[~cos.withdrawn & cos.cosponsor.isin(party.index)]
rb = pd.read_csv("Anas/a3/out/release_bills.csv")
rb = rb[rb.status == "resolved"]
press = pd.concat(pd.read_parquet(f, columns=["bioguide"]) for f in sorted(glob.glob("Anas/press_releases/press_releases_part*of3.parquet")))
n_rel = press.bioguide.value_counts()

def table(types, own, cross_def, number_only=False):
    """One row per (member, own bill): member, bill_id, cross (bool), announced (bool)."""
    B = bills[bills.type.isin(types) & bills.sponsor.isin(party.index)]
    C = cos[cos.bill_id.isin(B.bill_id)]
    if own == "sponsor":
        T = B[["bill_id", "sponsor"]].rename(columns={"sponsor": "member"})
    else:                                                    # original cosponsor
        T = C[C.original][["bill_id", "cosponsor"]].rename(columns={"cosponsor": "member"})
    T = T[T.member.isin(n_rel.index)].copy()
    sp = B.set_index("bill_id").sponsor
    C2 = C[C.original] if cross_def == "original" else C
    # the bill's other leaders (or, for "any", all cosponsors), plus the sponsor when the member is a cosponsor
    others = pd.concat([C2[["bill_id", "cosponsor"]].rename(columns={"cosponsor": "other"}),
                        sp.rename("other").reset_index()])
    others = others.merge(T, on="bill_id")
    others = others[others.other != others.member]
    others["x"] = party[others.other].values != party[others.member].values
    cross = others.groupby(["member", "bill_id"]).x.any()
    T["cross"] = [bool(cross.get((m, b), False)) for m, b in zip(T.member, T.bill_id)]
    R = rb if not number_only else rb[rb.how == "number"]
    ann = set(zip(R.bioguide, R.bill_id))
    T["announced"] = [(m, b) in ann for m, b in zip(T.member, T.bill_id)]
    return T

def test(T, label, min_releases=1, co_led_only=False, B=None):
    T = T[T.member.map(n_rel).fillna(0) >= min_releases]
    if co_led_only:
        led = set(cos[cos.original].bill_id)
        T = T[T.bill_id.isin(led)]
    g = T.groupby("member").cross.agg(["size", "sum"])
    keep = g.index[(g["size"] >= 3) & (g["sum"] >= 1) & (g["sum"] < g["size"])]
    T = T[T.member.isin(keep)].sort_values("member").reset_index(drop=True)
    cross, ann = T.cross.to_numpy(), T.announced.to_numpy()
    obs = int((cross & ann).sum())
    rng = np.random.default_rng(SEED)
    codes = pd.factorize(T.member)[0]
    null = np.empty(N)
    for i in range(N):                                       # shuffle the cross labels within each member
        order = np.lexsort((rng.random(len(T)), codes))
        null[i] = (cross[order] & ann).sum()
    p_one = (np.sum(null >= obs) + 1) / (N + 1)
    p_two = (np.sum(np.abs(null - null.mean()) >= abs(obs - null.mean())) + 1) / (N + 1)
    return {"check": label, "members": T.member.nunique(), "bills": len(T), "cross-party bills": int(cross.sum()),
            "announced, cross-party": ann[cross].mean(), "announced, same-party": ann[~cross].mean(),
            "announced cross-party bills": obs, "null mean": null.mean(), "null 2.5%": np.percentile(null, 2.5),
            "null 97.5%": np.percentile(null, 97.5), "ratio to null": obs / null.mean(), "p one-sided": p_one,
            "p two-sided": p_two}

HR = ["hr", "hjres"]
main = table(HR, "sponsor", "original")
rows = [test(main, "Main: sponsored hr/hjres, cross-party = an original cosponsor of the other party")]
for pty in ("R", "D"):
    rows.append(test(main[main.member.map(party) == pty], f"Only {'Republicans' if pty == 'R' else 'Democrats'}"))
rows += [
    test(main, "Only bills with at least one original cosponsor (cross- vs same-party co-leads)", co_led_only=True),
    test(main, "Members with at least 10 releases", min_releases=10),
    test(table(HR, "sponsor", "original", number_only=True), "Announced = cited by bill number only (no title matches)"),
    test(table(HR, "sponsor", "any"), "Cross-party = any cosponsor of the other party, at any time"),
    test(table(["hr", "hjres", "hres", "hconres"], "sponsor", "original"), "All four House bill types"),
    test(table(HR, "original", "original"), "Own bills = bills the member was an original cosponsor of"),
]
out = pd.DataFrame(rows)
out.round(4).to_csv("Martin/m6_results.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 70)
show = out.copy()
for c in ("announced, cross-party", "announced, same-party"): show[c] = (100 * show[c]).round(1).astype(str) + "%"
print(show[["check", "members", "bills", "cross-party bills", "announced, cross-party", "announced, same-party",
            "announced cross-party bills", "null mean", "ratio to null", "p one-sided", "p two-sided"]].round(3).to_string(index=False))
