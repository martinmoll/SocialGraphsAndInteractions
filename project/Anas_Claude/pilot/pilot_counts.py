"""Exploratory, 12 Nov 2026: Republican cosponsorship signatures per quarter, by the sponsor's party.
Shows that the cross-party share rises because same-party signatures fall. All bill types, withdrawn dropped.
Run from project/:  python Anas_Claude/pilot/pilot_counts.py data/processed"""
import sys
import pandas as pd

P = sys.argv[1] if len(sys.argv) > 1 else "data/processed"
m = pd.read_csv(f"{P}/members.csv")
b = pd.read_parquet(f"{P}/bills.parquet")
c = pd.read_parquet(f"{P}/cosponsors.parquet")
pty = m.set_index("bioguide").party

cc = c[~c.withdrawn].merge(b[["bill_id", "sponsor"]], on="bill_id")
cc["sp"] = cc.sponsor.map(pty)
cc["cp"] = cc.cosponsor.map(pty)
cc["q"] = pd.PeriodIndex(cc.date, freq="Q").astype(str)

r = cc[cc.cp == "R"]
t = r.groupby(["q", "sp"]).size().unstack(fill_value=0)[["R", "D"]]
t["share_D"] = (t.D / (t.R + t.D)).round(3)
print("Republican cosponsorship signatures by quarter, by sponsor party\n", t)

b["q"] = pd.PeriodIndex(b.introduced, freq="Q").astype(str)
b["sp"] = b.sponsor.map(pty)
print("\nBills introduced per quarter, by sponsor party\n", b.groupby(["q", "sp"]).size().unstack(fill_value=0)[["R", "D"]])
