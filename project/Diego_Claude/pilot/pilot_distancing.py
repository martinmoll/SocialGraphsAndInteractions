"""Pilot for 'Running from Trump?' (Diego_Claude, 11 Nov 2026).

Reads only project/data/processed. Run from the project folder:
    python Diego_Claude/pilot/pilot_distancing.py
Prints every number quoted in Diego_Claude/02_pilot_findings.md.
"""
import sys
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

P = sys.argv[1] if len(sys.argv) > 1 else "data/processed"
CUT = "2025-12-01"  # early = Jan-Nov 2025, late = Dec 2025-Nov 2026

sp = pd.read_parquet(f"{P}/speeches.parquet")
m = pd.read_csv(f"{P}/members.csv")
d = pd.read_csv(f"{P}/districts.csv")
inc = pd.read_csv(f"{P}/incumbents.csv")
b = pd.read_parquet(f"{P}/bills.parquet")
c = pd.read_parquet(f"{P}/cosponsors.parquet")
pty = m.set_index("bioguide").party

# ---------- TALK: how often Republicans say Trump's name on the floor ----------
sp = sp[sp.n_words >= 50].merge(m[["bioguide", "party"]], on="bioguide")
lt = sp.text.str.lower()
for k, v in {"trump": r"\btrump\b", "the_president": r"\bthe president\b",
             "administration": r"\badministration\b", "biden": r"\bbiden\b"}.items():
    sp[k] = lt.str.count(v)
sp["half"] = sp.day.str[:4] + np.where(sp.day.str[5:7] < "07", "-H1", "-H2")
R = sp[sp.party == "R"]
print("\n[1] Republican rate per 10,000 words, House floor (section H) only")
s = R[R.section == "H"].groupby("half")[["trump", "the_president", "administration", "biden", "n_words"]].sum()
print((s.iloc[:, :4].div(s.n_words, axis=0) * 1e4).round(2).assign(words=s.n_words))

g = R.groupby(["half", "bioguide"])[["trump", "n_words"]].sum()
g = g[g.n_words >= 1000]
print("\n[2] Share of Republicans (>=1,000 words in the half-year) who name Trump at least once per 1,000 words")
print(g.groupby("half").apply(lambda x: ((x.trump / x.n_words * 1e3) >= 1).mean()).round(2))

# ---------- DEEDS: Republican cosponsorships going to Democratic sponsors ----------
cc = c[~c.withdrawn].merge(b[["bill_id", "sponsor"]], on="bill_id")
cc["sp"] = cc.sponsor.map(pty)
cc["cp"] = cc.cosponsor.map(pty)
cc["q"] = pd.PeriodIndex(cc.date, freq="Q").astype(str)
print("\n[3] Cross-party share of cosponsorships, by quarter signed (119th Congress)")
out = {}
for p, other in [("R", "D"), ("D", "R")]:
    x = cc[cc.cp == p]
    out[f"{p}_n"] = x.groupby("q").size()
    out[f"{p}_cross"] = x.groupby("q").apply(lambda y: (y.sp == other).mean()).round(3)
print(pd.DataFrame(out))

# ---------- WHO: per-member change, early vs late ----------
sp["h"] = np.where(sp.day < CUT, "e", "l")
a = sp.groupby(["bioguide", "h"])[["trump", "n_words"]].sum().unstack()
T = pd.DataFrame({"tr_e": a.trump.e / a.n_words.e * 1e4, "tr_l": a.trump.l / a.n_words.l * 1e4,
                  "w_e": a.n_words.e, "w_l": a.n_words.l})
cc["x"] = cc.sp == "D"
cc["h"] = np.where(cc.date < CUT, "e", "l")
w = cc[cc.cp == "R"].groupby(["cosponsor", "h"]).x.agg(["mean", "size"]).unstack()
W = pd.DataFrame({"x_e": w["mean"].e, "x_l": w["mean"].l, "n_e": w["size"].e, "n_l": w["size"].l})
X = (m[m.party == "R"].merge(d[["state", "district", "lean"]], on=["state", "district"], how="left")
     .set_index("bioguide").join(T).join(W))


def ols(df, y, xs):
    df = df.dropna(subset=[y] + xs)
    Z = (df[xs] - df[xs].mean()) / df[xs].std()
    A = np.c_[np.ones(len(df)), Z]
    beta, *_ = np.linalg.lstsq(A, df[y], rcond=None)
    return len(df), dict(zip(["const"] + [f"{x} (per SD)" for x in xs], beta.round(3)))


t = X[(X.w_e >= 1500) & (X.w_l >= 1500)]
print(f"\n[4] TALK per member (>=1,500 words each period): n = {len(t)}, "
      f"median Trump rate {t.tr_e.median():.2f} -> {t.tr_l.median():.2f} per 10k words, "
      f"share whose rate fell {(t.tr_l < t.tr_e).mean():.2f}")
print("    late rate ~ early rate + ideology (NOMINATE) + district lean:", ols(t, "tr_l", ["tr_e", "nominate_dim1", "lean"]))
n = X[(X.n_e >= 10) & (X.n_l >= 10)]
print(f"[5] DEEDS per member (>=10 cosponsorships each period): n = {len(n)}, "
      f"median cross-party share {n.x_e.median():.3f} -> {n.x_l.median():.3f}, share that rose {(n.x_l > n.x_e).mean():.2f}")
print("    late share ~ early share + ideology + lean:", ols(n, "x_l", ["x_e", "nominate_dim1", "lean"]))
both = t.join(n[[]], how="inner").dropna(subset=["x_e", "x_l"])
print("[6] change in words vs change in deeds, Spearman:",
      spearmanr(both.tr_l - both.tr_e, both.x_l - both.x_e))

# ---------- ELECTION: does distancing relate to running ahead of the district? ----------
y = inc.merge(m[["bioguide", "party"]], on="bioguide").merge(d, on=["state", "district"])
y = y[(y.party == "R") & y.fate.isin(["re-elected", "lost general"]) & (y.n_rep == 1) & (y.n_dem == 1) & y.winner.notna()].copy()
y["margin"] = 100 * (y.rep_votes - y.dem_votes) / (y.rep_votes + y.dem_votes)
y["over"] = y.margin - np.polyval(np.polyfit(y.lean, y.margin, 1), y.lean)
y = y.set_index("bioguide").join(T)
y = y[(y.w_e >= 1500) & (y.w_l >= 1500)]
print(f"\n[7] ELECTION (approximate study population, n = {len(y)}): Spearman of overperformance with "
      f"change in Trump rate: {spearmanr(y.tr_l - y.tr_e, y.over)}")
