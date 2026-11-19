"""Merge the probe results, join party and 2026 lean, print the scope tables and write scope_by_member.csv.

From project/:  python Anas/press_scope/scope_table.py data/processed Anas/press_scope
"""
import json, sys, pandas as pd
P, D = sys.argv[1], sys.argv[2]
res = {r["bioguide"]: r for r in json.load(open(f"{D}/stage2b.json"))}
for r in json.load(open(f"{D}/guess2.json")):          # path guesses only replace members still unresolved
    if r["status"] == "ok" or res[r["bioguide"]]["status"] != "ok":
        r["guessed"] = True; res[r["bioguide"]] = r
df = pd.DataFrame(res.values())
m = pd.read_csv(f"{P}/members.csv"); d = pd.read_csv(f"{P}/districts.csv")
m = m.merge(d[["state", "district", "lean", "redrawn_state"]], on=["state", "district"], how="left")
x = m[m.party.isin(["R", "D"])].merge(df[["bioguide", "status", "count", "listing", "kind", "newest", "guessed"]], on="bioguide", how="left")
x["status"] = x["status"].fillna("left office")
x.loc[(x.status == "ok") & (x["count"] == 0), "status"] = "listing abandoned"
x.loc[x.bioguide.isin(["M001137"]), "status"] = "uncertain (pager repeats)"   # Meeks: site serves repeated pages
x["exposed"] = ((x.party == "R") & (x.lean <= 5)) | ((x.party == "D") & (x.lean >= -5))
x["stopped_before_sep"] = x.newest < "2026-09-01"
pd.set_option("display.width", 200)
st = x.status.where(x.status.isin(["ok", "left office", "listing abandoned"]), "needs hand work")
print(pd.crosstab(st, x.party, margins=True))
ok = x[x.status == "ok"]
print("\nreleases since 3 Jan 2025 (members with a count):")
print(ok.groupby("party")["count"].describe(percentiles=[.25, .5, .75]).round(0)[["count", "25%", "50%", "75%", "max"]])
print("total", int(ok["count"].sum()), ok.groupby("party")["count"].sum().astype(int).to_dict())
print("\nby exposure:")
print(ok.groupby(["party", "exposed"]).agg(members=("count", "size"), median=("count", "median"), total=("count", "sum"),
                                           stopped_before_sep=("stopped_before_sep", "sum")))
print("\nexposed in redrawn states:", x[x.exposed].groupby("party").redrawn_state.sum().to_dict())
print("\nneeds hand work:", x[~st.isin(["ok", "left office", "listing abandoned"])].apply(lambda r: f"{r['name']} ({r.party})", axis=1).tolist())
x.to_csv(f"{D}/scope_by_member.csv", index=False)
