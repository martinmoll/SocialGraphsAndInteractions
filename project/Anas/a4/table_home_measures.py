"""The home map's network measures as one table (22 Nov, late; Anas's choice: plain bars in the figure, the rest here).

Run from Anas/ after home_measures.py and alpha_centrality.py:  python a4/table_home_measures.py
Reads out/home_measures_centrality.csv, out/home_measures_community_position.csv, out/home_measures_null.csv and
out/alpha_centrality.csv; nothing is computed here. Writes out/table_home_measures.md (for the repo) and
out/table_home_measures.tex (a LaTeX tabular for Overleaf; needs \\usepackage{booktabs}).
"""
import os

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
cen = pd.read_csv(os.path.join(OUT, "home_measures_centrality.csv")).set_index(["measure", "party"])
com = pd.read_csv(os.path.join(OUT, "home_measures_community_position.csv")).set_index("party")
nul = pd.read_csv(os.path.join(OUT, "home_measures_null.csv")).iloc[0]
alc = pd.read_csv(os.path.join(OUT, "alpha_centrality.csv"))
ALPHAS = sorted(alc.alpha.unique())


def fp(p):
    return "< 0.001" if p < 0.001 else f"{p:.3f}" if p < 0.1 else f"{p:.2f}"


def alpha_note(measure, party):
    """At which of the tested alphas the Holm p is below 0.05."""
    a = alc[(alc.measure == measure) & (alc.party == party)].set_index("alpha").p_holm
    sig = [x for x in ALPHAS if a[x] < 0.05]
    if len(sig) == len(ALPHAS):
        return "all"
    if not sig:
        return "none"
    if len(sig) == len(ALPHAS) - 1:
        return "all but " + next(f"{x:g}" for x in ALPHAS if x not in sig)
    if sig == ALPHAS[ALPHAS.index(sig[0]):]:
        return f"{sig[0]:g} and up"
    return ", ".join(f"{x:g}" for x in sig)


rows = []
spec = [("Cross-party ties (full map)", "cross-party degree (full map)", "{:.1f}", 1),
        ("Ties in the backbone (degree)", "degree (backbone)", "{:.1f}", 1),
        ("Betweenness in the backbone (×1,000)", "betweenness (backbone)", "{:.1f}", 1000),
        ("Closeness in the backbone", "closeness (backbone)", "{:.3f}", 1),
        ("Betweenness given degree (residual)", "betweenness given degree (residual)", "{:+.2f}", 1)]
for label, key, f, sc in spec:
    for p in ("R", "D"):
        r = cen.loc[(key, p)]
        rows.append(dict(Measure=label, Party=p, Exposed=f.format(r.exposed_mean * sc), Safe=f.format(r.safe_mean * sc),
                         Ratio="" if pd.isna(r.ratio) else f"{r.ratio:.2f}", p=fp(r.p), Holm=fp(r.p_holm),
                         **{"Holm p < 0.05 at α": "all (full map)" if "full map" in key else alpha_note(key, p)}))
for p in ("R", "D"):
    r = com.loc[p]
    rows.append(dict(Measure="Other party in own Louvain community", Party=p, Exposed=f"{100 * r.exposed:.0f}%",
                     Safe=f"{100 * r.safe:.0f}%", Ratio=f"{r.exposed / r.safe:.2f}", p=fp(r.p), Holm="(own test)",
                     **{"Holm p < 0.05 at α": "(full map)"}))
T = pd.DataFrame(rows)
note = (f"Exposed against safe members within each party: p from 10,000 shuffles of exposure within party; Holm "
        f"corrects across the 10 tests in the first five rows. Backbone: disparity filter at α = 0.01 (main); last "
        f"column: the α values among {', '.join(f'{x:g}' for x in ALPHAS)} at which the Holm p is below 0.05 "
        f"(alpha_centrality.py). Preference beyond activity (degree-preserving rewiring of the cross-party ties, "
        f"1,000 rewirings): {100 * nul.S2_observed:.1f}% of cross-party ties join two exposed members, against "
        f"{100 * nul.S2_rewired_mean:.1f}% rewired (ratio {nul.S2_ratio:.2f}, p {fp(nul.p_S2)}).")

md = ["| " + " | ".join(T.columns) + " |", "|" + "---|" * len(T.columns)]
md += ["| " + " | ".join(str(v) for v in r) + " |" for r in T.itertuples(index=False)]
open(os.path.join(OUT, "table_home_measures.md"), "w").write(
    "# The home map: exposed against safe members\n\n" + "\n".join(md) + "\n\n" + note + "\n")

esc = lambda x: str(x).replace("%", r"\%").replace("<", r"$<$").replace("×", r"$\times$").replace("α", r"$\alpha$")
tex = [r"\begin{tabular}{llrrrrrl}", r"\toprule",
       r"Measure & Party & Exposed & Safe & Ratio & $p$ & Holm $p$ & Holm $p<0.05$ at $\alpha$ \\", r"\midrule"]
for i, r in enumerate(T.itertuples(index=False)):
    tex.append(" & ".join(esc(v) if (j or i % 2 == 0) else "" for j, v in enumerate(r)) + r" \\")
tex += [r"\bottomrule", r"\end{tabular}"]
open(os.path.join(OUT, "table_home_measures.tex"), "w").write("% " + note + "\n" + "\n".join(tex) + "\n")
pd.set_option("display.width", 200)
print(T.to_string(index=False))
print("\n" + note)
