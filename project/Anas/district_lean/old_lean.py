"""District lean on the map members served in (2025), next to the 2026 lean we already have.

Run from project/:
    python Anas/district_lean/old_lean.py data/processed Anas/district_lean

Source: the 2025 Cook PVI table ("By congressional district") in the Wikipedia article "Cook Partisan Voting
Index", as it stood on 25 May 2025 (revision 1292130997). That is after Cook's 2025 release (2020 and 2024
presidential results) and before any state redrew its map for 2026. The current version of the article has
been updated to the 2026 maps, so it gives the same numbers as districts.csv and cannot be used for this.

Pinning the revision id makes the download reproducible: the same request returns the same table later.

Writes district_lean.csv: one row per district (435) with
    lean_2025  lean of the district as it was in 2025, the one the member served (positive = Republican)
    lean_2026  lean of the 2026 district with the same number (from districts.csv)
    redrawn_state, changed (lean_2025 != lean_2026)
and prints the checks and the exposed counts under both leans.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

import numpy as np
import pandas as pd

PROC, OUT = sys.argv[1], sys.argv[2]
REVID = 1292130997
STATES = {"alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA", "colorado": "CO",
          "connecticut": "CT", "delaware": "DE", "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID",
          "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS", "kentucky": "KY", "louisiana": "LA",
          "maine": "ME", "maryland": "MD", "massachusetts": "MA", "michigan": "MI", "minnesota": "MN",
          "mississippi": "MS", "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV",
          "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY", "north carolina": "NC",
          "north dakota": "ND", "ohio": "OH", "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA",
          "rhode island": "RI", "south carolina": "SC", "south dakota": "SD", "tennessee": "TN", "texas": "TX",
          "utah": "UT", "vermont": "VT", "virginia": "VA", "washington": "WA", "west virginia": "WV",
          "wisconsin": "WI", "wyoming": "WY"}

q = urllib.parse.urlencode(dict(action="query", prop="revisions", revids=REVID, rvprop="ids|timestamp|content",
                                rvslots="main", format="json"))
req = urllib.request.Request("https://en.wikipedia.org/w/api.php?" + q, headers={"User-Agent": "course-project/0.1"})
rev = list(json.load(urllib.request.urlopen(req, timeout=60))["query"]["pages"].values())[0]["revisions"][0]
text = rev["slots"]["main"]["*"]
print(f"revision {rev['revid']} of {rev['timestamp']}")

rows = []
for chunk in text.split("\n|-"):                                    # one table row per chunk
    m = re.search(r"\{\{ushr\|([^|}]+)\|([^|}]+)\|X\}\}", chunk)
    p = re.search(r"Shading PVI\|([RDE])[A-Z]*\|?(?:value=)?(\d*)", chunk, re.I)
    if not m or not p:
        continue
    lean = 0 if p.group(1).upper() == "E" else int(p.group(2)) * (1 if p.group(1) == "R" else -1)
    dist = 0 if m.group(2).upper() in ("AL", "AT-LARGE") else int(m.group(2))
    rows.append((STATES[m.group(1).strip().lower()], dist, lean))
old = pd.DataFrame(rows, columns=["state", "district", "lean_2025"]).drop_duplicates()
assert len(old) == 435 and not old.duplicated(["state", "district"]).any(), len(old)

d = pd.read_csv(os.path.join(PROC, "districts.csv"))[["state", "district", "lean", "redrawn_state"]]
t = d.rename(columns={"lean": "lean_2026"}).merge(old, on=["state", "district"], how="outer", validate="1:1")
assert t.lean_2025.notna().all() and t.lean_2026.notna().all()
t["changed"] = t.lean_2025 != t.lean_2026
t = t[["state", "district", "lean_2025", "lean_2026", "redrawn_state", "changed"]].sort_values(["state", "district"])
os.makedirs(OUT, exist_ok=True)
t.to_csv(os.path.join(OUT, "district_lean.csv"), index=False)

# ---- checks ----
nr, rd = t[~t.redrawn_state], t[t.redrawn_state]
print(f"states not redrawn: {(~nr.changed).sum()} of {len(nr)} districts have the same lean in both tables")
print(f"redrawn states: {rd.changed.sum()} of {len(rd)} districts changed lean")
print("changed, by redrawn state:", rd.groupby("state").changed.sum().to_dict())

# ---- one row per current member: the district served and the district run in, each with its own lean ----
# The 2026 district a member ran in is taken from incumbents.csv, not from the district number they served:
# after a redraw some members ran under a different number (Bera served CA-6 and ran in CA-3).
m = pd.read_csv(os.path.join(PROC, "members.csv"))
m = m[m.current & m.party.isin(["R", "D"])][["bioguide", "name", "party", "state", "district"]]
inc = pd.read_csv(os.path.join(PROC, "incumbents.csv"))[["bioguide", "state", "district", "fate"]]
inc = inc.rename(columns={"state": "state_2026", "district": "district_2026"})
m = m.merge(t[["state", "district", "lean_2025", "redrawn_state"]], on=["state", "district"], how="left")
m = m.merge(inc, on="bioguide", how="left")
lean26 = t.set_index(["state", "district"]).lean_2026
m["lean_2026_ran"] = [lean26.get((s, int(d))) if pd.notna(d) else None for s, d in zip(m.state_2026, m.district_2026)]
m["moved"] = m.district_2026.notna() & ((m.state != m.state_2026) | (m.district != m.district_2026))


def exposed(party, lean):
    return ((party == "R") & (lean <= 5)) | ((party == "D") & (lean >= -5))


m["exposed_2025"] = exposed(m.party, m.lean_2025)
m["exposed_2026"] = exposed(m.party, m.lean_2026_ran.astype(float)).astype("boolean")
m.loc[m.lean_2026_ran.isna(), "exposed_2026"] = pd.NA       # no 2026 contest row: unknown, not "safe"
cols = ["bioguide", "name", "party", "state", "district", "lean_2025", "exposed_2025", "redrawn_state",
        "district_2026", "lean_2026_ran", "exposed_2026", "moved", "fate"]
m[cols].sort_values(["state", "district"]).to_csv(os.path.join(OUT, "member_lean.csv"), index=False)

print(f"current members (R, D): {len(m)}; with a 2026 contest row: {m.district_2026.notna().sum()}; "
      f"ran under a different district number: {int(m.moved.sum())}")
print("fate in 2026:", m.fate.value_counts(dropna=False).to_dict())
for col in ["exposed_2025", "exposed_2026"]:
    print(f"{col}: R {int(((m[col] == True) & (m.party == 'R')).sum())}, D {int(((m[col] == True) & (m.party == 'D')).sum())}")
both = m[m.exposed_2026.notna()]
sw = both[both.exposed_2025 != both.exposed_2026.astype(bool)]
print(f"members whose label differs (served vs ran-in district): {len(sw)}; all in redrawn states: {sw.redrawn_state.all()}")
print(sw.sort_values(["party", "state", "district"])[["name", "party", "state", "district", "lean_2025", "district_2026",
                                                        "lean_2026_ran", "exposed_2025", "exposed_2026"]].to_string(index=False))

# ---- second instrument: 2024 presidential margin on the districts members served (The Downballot) ----
# "2020 and 2024 results according to the district lines used in 2024", https://www.the-downballot.com/data
# Their terms: cite and link, do not reproduce the whole spreadsheet. Only the 2024 margin column is kept here.
SHEET = ("https://docs.google.com/spreadsheets/d/1ng1i_Dm_RMDnEvauH44pgE6JCUsapcuu8F2pCfeLWFo/export"
         "?format=csv&gid=620838163")
import csv, io
raw = urllib.request.urlopen(urllib.request.Request(SHEET, headers={"User-Agent": "course-project/0.1"}), timeout=60)
pres = []
for r in csv.reader(io.StringIO(raw.read().decode("utf-8"))):
    mm = re.fullmatch(r"([A-Z]{2})-(AL|\d\d)", (r[0] if r else "").strip())
    if mm:
        dist = 0 if mm.group(2) == "AL" else int(mm.group(2))
        # sheet margin = Harris - Trump in points; flip so that positive = Republican, like the lean
        pres.append((mm.group(1), dist, r[1].strip(), -float(r[5])))
p = pd.DataFrame(pres, columns=["state", "district", "db_incumbent", "pres_margin_2024"])
assert len(p) == 435 and not p.duplicated(["state", "district"]).any(), len(p)

# check 1: same districts? the incumbent named in the sheet should be the member who served the district
chk = m.merge(p, on=["state", "district"], how="left")
last = chk.name.str.split().str[-1].str.lower().str.replace(r"[^a-z]", "", regex=True)
hit = [l in re.sub(r"[^a-z ]", "", str(i).lower().replace("-", "")) for l, i in zip(last, chk.db_incumbent)]
print(f"\nDownballot 2024 lines: 435 districts; incumbent in the sheet matches our member's surname for "
      f"{sum(hit)} of {len(chk)} members")
print("no surname match:", chk.loc[[not h for h in hit], ["name", "state", "district", "db_incumbent"]].to_string(index=False))

# check 2: how closely the two instruments agree, and the margin that corresponds to a lean of +-5
t = t.merge(p[["state", "district", "pres_margin_2024"]], on=["state", "district"], how="left")
both_ = t.dropna(subset=["pres_margin_2024"])
b, a = np.polyfit(both_.pres_margin_2024, both_.lean_2025, 1)
print(f"Pearson r(lean_2025, pres_margin_2024) = {both_.lean_2025.corr(both_.pres_margin_2024):.3f}; "
      f"Spearman = {both_.lean_2025.corr(both_.pres_margin_2024, method='spearman'):.3f}; "
      f"fit lean = {a:.2f} + {b:.3f} * margin")
cut_r, cut_d = (5 - a) / b, (-5 - a) / b       # margins equivalent to lean +5 and -5 on the fitted line
print(f"lean +5 ~ Trump margin {cut_r:+.1f}; lean -5 ~ Trump margin {cut_d:+.1f}")
m = m.merge(p[["state", "district", "pres_margin_2024"]], on=["state", "district"], how="left")
m["exposed_pres"] = ((m.party == "R") & (m.pres_margin_2024 <= cut_r)) | ((m.party == "D") & (m.pres_margin_2024 >= cut_d))
print(f"exposed by pres margin: R {int((m.exposed_pres & (m.party == 'R')).sum())}, D {int((m.exposed_pres & (m.party == 'D')).sum())}")
dis = m[m.exposed_pres != m.exposed_2025]
print(f"members whose label differs between lean_2025 and the 2024 margin: {len(dis)}")
print(dis.sort_values(["party", "state", "district"])[["name", "party", "state", "district", "lean_2025",
                                                         "pres_margin_2024", "exposed_2025", "exposed_pres"]].to_string(index=False))

cols = cols[:6] + ["pres_margin_2024", "exposed_pres"] + cols[6:]
m[cols].sort_values(["state", "district"]).to_csv(os.path.join(OUT, "member_lean.csv"), index=False)
t[["state", "district", "lean_2025", "lean_2026", "redrawn_state", "changed", "pres_margin_2024"]].to_csv(
    os.path.join(OUT, "district_lean.csv"), index=False)
