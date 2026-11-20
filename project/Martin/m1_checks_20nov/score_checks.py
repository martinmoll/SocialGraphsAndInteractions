"""Score Martin's hand checks once the sheets are filled in. Run from project/:
    python Martin/m1_checks_20nov/score_checks.py
Scores whichever sheets have codes; skips the rest. Intervals are Wilson 95% intervals.
  recall    m1_checks_20nov/recall_sheet.csv against recall_key.csv (matched by surname, accents and case ignored)
  untitled  m1_checks_20nov/untitled_sheet.csv: share coded M, and the proposed 24-of-30 rule
  lists     m1_checks_20nov/list_sheet.csv: share coded OK
  yields    m3_yield_check/yield_check_sheet.csv against yield_check_key.csv (DECISIONS G1c)
"""
import math, sys, unicodedata
from pathlib import Path
import pandas as pd

HERE = Path(__file__).parent
YIELD = HERE.parent / "m3_yield_check"
members = pd.read_csv("data/processed/members.csv").set_index("bioguide")

def key(s):
    return unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower().strip()

def wilson(k, n):
    if n == 0: return "n = 0"
    p, z = k / n, 1.96
    c, h = (p + z * z / (2 * n)) / (1 + z * z / n), z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return f"{k} of {n} = {p:.0%} (95% interval {c - h:.0%} to {c + h:.0%})"

def filled(df, col):
    return df[col].fillna("").astype(str).str.strip().ne("").any()

# ---- recall
R = pd.read_csv(HERE / "recall_sheet.csv", keep_default_na=False)
if filled(R, "named_members"):
    K = pd.read_csv(HERE / "recall_key.csv", keep_default_na=False).set_index("id")
    tp = fn = extra = unsure = 0; missed = []
    for r in R.itertuples():
        mine = [x for x in str(r.named_members).split(";") if x.strip()]
        unsure += sum("?" in x for x in mine)
        mine = [key(x.replace("?", "")) for x in mine]
        found = {key(members["last"][b]) for b in K.matcher_found[r.id].split(";") if b}   # full surnames: "van duyne"
        hit = lambda m: [f for f in found if f" {f} " in f" {m.replace(',', ' ').replace('.', ' ')} "]
        tp += sum(bool(hit(m)) for m in mine); fn += sum(not hit(m) for m in mine)
        extra += len(found - {f for m in mine for f in hit(m)})
        miss = [m for m in mine if not hit(m)]
        missed += [f"turn {r.id}: {m}" for m in miss]
    print("RECALL (floor):", wilson(tp, tp + fn))
    print(f"  found by the matcher but not on your list: {extra} (a wrong match, or a name you skipped: look at them)")
    print(f"  names you marked '?': {unsure}")
    for m in missed: print("  missed:", m)
else:
    print("recall: not coded yet")

# ---- untitled
U = pd.read_csv(HERE / "untitled_sheet.csv", keep_default_na=False)
if filled(U, "code"):
    c = U.code.str.upper().str.strip(); n = int(c.isin(list("MPX")).sum())
    print("\nUNTITLED full names:", wilson(int((c == "M").sum()), n), f"| P {int((c == 'P').sum())}, X {int((c == 'X').sum())}")
    print("  proposed rule (24 of 30 M): " + ("switch on for the floor" if (c == "M").sum() >= 24 else "press only, say so in Methods"))
else:
    print("\nuntitled: not coded yet")

# ---- lists
L = pd.read_csv(HERE / "list_sheet.csv", keep_default_na=False)
if filled(L, "code"):
    c = L.code.str.upper().str.strip(); n = int(c.isin(["OK", "X"]).sum())
    print("\nLIST hits correct:", wilson(int((c == "OK").sum()), n))
    for r in L[c == "X"].itertuples(): print(f"  wrong: row {r.id}, {r.named_name}: {r.note}")
else:
    print("\nlists: not coded yet")

# ---- yields (G1c)
Y = pd.read_csv(YIELD / "yield_check_sheet.csv", keep_default_na=False)
if filled(Y, "code"):
    K = pd.read_csv(YIELD / "yield_check_key.csv").set_index("id")
    Y = Y.assign(code=Y.code.str.upper().str.strip(), side=K.side.reindex(Y.id).values)
    ph, wi = Y[Y.side == "phrase only"], Y[Y.side == "window only"]
    print("\nYIELD rule (G1c), rows where the two rules disagree:")
    print(f"  flagged only by the phrase rule, really yields (Y): {(ph.code == 'Y').sum()} of {len(ph)}; false flags (N): {(ph.code == 'N').sum()}")
    print(f"  flagged only by the window rule, really yields the phrase rule misses (Y): {(wi.code == 'Y').sum()} of {len(wi)}")
    print(f"  unsure (?): {(Y.code == '?').sum()}")
else:
    print("\nyields: not coded yet")
