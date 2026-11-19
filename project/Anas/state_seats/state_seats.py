"""Seats per state: who holds them, how many are exposed, and how many press releases each state's members posted.

Run from project/:
    python Anas/state_seats/state_seats.py data/processed Anas/press_scope/scope_by_member.csv Anas/state_seats

Writes seats_by_state.csv and seats_by_state.png to the output folder and prints the summary numbers.

"Exposed" here is the scope scan's working rule (a Republican in a district with lean <= 5, a Democrat with
lean >= -5, lean = 2026 Cook PVI, positive = Republican). It is not the group's definition (DECISIONS G13, open
point 2), and in redrawn states it describes the 2026 district, not the one the member served in.
"""
import sys
import os
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

proc, scope_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)

d = pd.read_csv(os.path.join(proc, "districts.csv"))          # one row per voting seat (435)
m = pd.read_csv(os.path.join(proc, "members.csv"))
cur = m[m.current][["bioguide", "state", "district", "party"]]  # delegates are current=False in this file
seats = d.merge(cur, on=["state", "district"], how="left")
assert len(seats) == 435 and not seats.duplicated(["state", "district"]).any()

seats["holder"] = seats.party.fillna("vacant")
seats["exposed"] = ((seats.holder == "R") & (seats.lean <= 5)) | ((seats.holder == "D") & (seats.lean >= -5))
seats["group"] = "other"
seats.loc[(seats.holder == "R") & ~seats.exposed, "group"] = "safe R"
seats.loc[(seats.holder == "R") & seats.exposed, "group"] = "exposed R"
seats.loc[(seats.holder == "D") & seats.exposed, "group"] = "exposed D"
seats.loc[(seats.holder == "D") & ~seats.exposed, "group"] = "safe D"

# press releases counted in the scope scan, by state and party (status ok only)
s = pd.read_csv(scope_path)
s = s[s.status.isin(["ok"]) & s["count"].notna()] if "status" in s else s
rel = s.groupby(["state", "party"])["count"].sum().unstack(fill_value=0)

groups = ["safe D", "exposed D", "other", "exposed R", "safe R"]
t = seats.groupby("state").agg(
    seats=("district", "size"),
    R=("holder", lambda x: (x == "R").sum()),
    D=("holder", lambda x: (x == "D").sum()),
    other=("holder", lambda x: (~x.isin(["R", "D"])).sum()),
    exposed_R=("group", lambda x: (x == "exposed R").sum()),
    exposed_D=("group", lambda x: (x == "exposed D").sum()),
    median_lean=("lean", "median"),
    redrawn=("redrawn_state", "first"),
)
t["share_of_house"] = (t.seats / 435).round(3)
t["releases_D"] = rel.get("D", pd.Series(dtype=float)).reindex(t.index).fillna(0).astype(int)
t["releases_R"] = rel.get("R", pd.Series(dtype=float)).reindex(t.index).fillna(0).astype(int)
t = t.sort_values(["seats", "state"], ascending=[False, True])
t.to_csv(os.path.join(out, "seats_by_state.csv"))

# ---- summary numbers ----
n = len(t)
top4 = t.head(4)
exp = seats[seats.exposed]
print(f"states {n}; seats {t.seats.sum()}; holders R {int(t.R.sum())} D {int(t.D.sum())} other {int(t.other.sum())}")
print(f"single-seat states: {sorted(t[t.seats == 1].index)}")
print(f"top 4 {list(top4.index)}: {top4.seats.sum()} seats = {top4.seats.sum() / 435:.1%}")
print(f"median seats per state {t.seats.median():.0f}")
print(f"exposed: R {int(t.exposed_R.sum())}, D {int(t.exposed_D.sum())}")
for p in ["R", "D"]:
    e = exp[exp.holder == p].groupby("state").size().sort_values(ascending=False)
    print(f"exposed {p} by state, top: {e.head(6).to_dict()}; states with any: {len(e)}; top-4 share {e.head(4).sum() / e.sum():.0%}")
    print(f"  exposed {p} in redrawn states: {int(exp[(exp.holder == p) & exp.redrawn_state].shape[0])}")
print(f"redrawn states: {sorted(t[t.redrawn].index)}, {int(t[t.redrawn].seats.sum())} seats")
split = t[(t.R > 0) & (t.D > 0)]
print(f"states with members of both parties: {len(split)}; one-party delegations with 2+ seats: "
      f"{sorted(t[(t.seats > 1) & ((t.R == 0) | (t.D == 0))].index)}")

# ---- figure: stacked bars, one per state ----
colors = {"safe D": "#1c5cab", "exposed D": "#86b6ef", "other": "#b8b6b0",
          "exposed R": "#ec8a83", "safe R": "#a62f2e"}
counts = seats.groupby(["state", "group"]).size().unstack(fill_value=0).reindex(t.index)
for g in groups:
    if g not in counts:
        counts[g] = 0

fig, ax = plt.subplots(figsize=(8, 11.5), dpi=150)
fig.patch.set_facecolor("#fcfcfb")
ax.set_facecolor("#fcfcfb")
y = range(len(t))[::-1]
left = pd.Series(0, index=t.index)
for g in groups:
    ax.barh(list(y), counts[g], left=left, color=colors[g], height=0.72,
            edgecolor="#fcfcfb", linewidth=1.0, label=g)
    left = left + counts[g]
for yi, st in zip(y, t.index):
    ax.text(t.loc[st, "seats"] + 0.6, yi, str(int(t.loc[st, "seats"])), va="center", fontsize=7, color="#52514e")
labels = [f"{st}*" if t.loc[st, "redrawn"] else st for st in t.index]
ax.set_yticks(list(y))
ax.set_yticklabels(labels, fontsize=7.5, color="#0b0b0b")
ax.set_ylim(-0.7, len(t) - 0.3)
ax.set_xlabel("House seats (current holder)", fontsize=8.5, color="#52514e")
ax.tick_params(axis="x", labelsize=7.5, colors="#52514e", length=0)
ax.tick_params(axis="y", length=0)
ax.grid(axis="x", color="#e6e5e1", linewidth=0.6)
ax.set_axisbelow(True)
for sp in ax.spines.values():
    sp.set_visible(False)
ax.legend(ncol=5, loc="lower left", bbox_to_anchor=(0, 1.0), frameon=False, fontsize=7.5,
          handlelength=1.2, columnspacing=1.0, labelcolor="#0b0b0b")
fig.suptitle("Seats per state in the 119th House, by party and exposure", x=0.06, ha="left",
             fontsize=11, color="#0b0b0b", y=0.995)
fig.text(0.06, 0.008, "Exposed = working rule of the scope scan (R lean <= 5, D lean >= -5, 2026 Cook PVI); not the "
         "group's definition.\n* redrawn state: lean describes the 2026 district. 'other' = 1 independent "
         "and 2 vacant seats.\nSources: districts.csv, members.csv (current members), downloaded 11 Nov 2026.",
         fontsize=6.5, color="#52514e", ha="left")
fig.tight_layout(rect=(0, 0.04, 1, 0.985))
fig.savefig(os.path.join(out, "seats_by_state.png"), facecolor=fig.get_facecolor())
print("wrote", os.path.join(out, "seats_by_state.csv"), "and seats_by_state.png")
