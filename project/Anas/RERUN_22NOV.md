# A3 and A4 rerun on the 22 Nov matcher (Sun 22 Nov, evening)

Anas with Claude. **Why:** Martin's matcher changed on 22 Nov (DECISIONS G18: possessives and middle initials, Anas's
checklist items 12 and 15; G19: a title guard on untitled names). A3 had been frozen on the 20 Nov matcher (commit
`7bdbc18c`), so floor and press would have counted names differently ("Rep. Lawler's bill" counted on the floor, not
in press releases). Anas chose to rerun before the numbers freeze (G7). **Every reading holds; the numbers below
replace the 21 Nov ones.**

**Order of events, for the record:** before deciding, Claude estimated the effect on A4 from the raw new matcher
(shares about 0.3 points up, gaps unchanged). Anas then chose to rerun for consistency with the floor, not for a
result. The specification of every test is unchanged, and both sets of numbers are kept (21 Nov files in
`press_raw/backup_2026-11-22_pre_rerun/` and in the repo history).

## What was done

- **Inputs re-frozen** on the group repo at `bc1c2344` (main, 22 Nov 20:28). Only Martin's `matcher.py` and
  `build_mentions.py` changed; the press releases, `members.csv`, `nicknames.csv` and `aliases.csv` are the same
  files (`a3/out/inputs.json`).
- **One change to the press layer** (`a3/press_layer.py`):
  - **Middle initial:** Martin's matcher now reads "Riley M. Moore" itself. The layer's rule now acts only where
    its reading differs from his, or he found nothing: 105 hits (36 counted, 67 self, 2 unresolved), against 4,669
    before (824 counted). The rest are now his own hits, with the same member. **All 105 are places where his
    matcher finds nothing**; in none does it name a different member. In 140 "no member" cases ("Mr. James R. Willis") his matcher already finds nothing.
  - **Possessive in the tag and own-surname resolver:** "Smith's (R-NJ)" is read as Smith, the same pattern as his
    change H.
- **Rerun in order:** freeze, prepare, match_shared, press_layer, score_recall, rescore_switch, bills, flags,
  examples; then analysis, figure3, figure_lean, home_network, home_network_posthoc, home_measures,
  figure_home_map, figure_network, figure_network_groups.
- **`home_measures.py` now writes `a4/out/home_communities_members.csv` itself.** On 21 Nov that file was made by
  hand from the same partition, so it would have gone stale (the home-map figure reads it).
- **Backup of everything before the rerun:** `press_raw/backup_2026-11-22_pre_rerun/` (course folder, not uploaded).

## A3: what changed

| | 21 Nov (`7bdbc18c`) | 22 Nov (`bc1c2344`) |
|---|---|---|
| Press mentions (once per release, A4's file) | 129,052 in 21,672 releases | **129,473 in 21,867 releases** |
| Cross-party (R–D rows) | 14.4%; 33.0% weighted by 1/n | **14.4%; 33.0%** (14.44%, 33.04%) |
| Martin's matcher alone, once per release | — | 53,625, 23.0% cross-party |
| `in_shared` share of rows | 39.7% | 41.4% |
| `in_list` share of rows | 11.5% | 12.5% |
| Other flags (`co_lead`, `same_state`, leaders, caucus, bills) | | unchanged to 0.1 point |

- **Release–member pairs:** 424 new, 3 gone.
  - **The 3 gone** were wrong: "James P. McGovern" in a list read as John James. Martin's change I fixes them.
  - **The 424 new** are mostly possessives (227 "unique surname", 112 in lists, 29 by the Speaker rule).
  - **299 of the 424** show the named member's surname in the possessive in the context. Most of the other 125
    are lists that now continue past an initial ("H. Johnson, Khanna, McGovern": change I).
  - **Read by Claude, 20 drawn at random from the 424** (lists, untitled names, tags included): 20 of 20 are the
    member named. Before the rerun, Claude also read 20 cross-party possessive hits from the estimate run: all right.
    Not read by Anas or by blind readers.
- **Recall (A3.4, same 40 releases, same readers):** with the layer 75 of 77, **0.97**, unchanged; Martin's matcher
  alone 58 of 77, **0.75** (was 56, 0.73). Pairs counted but not in the key: 3 with the layer, as before, and 3 for the
  matcher alone (was 4). So precision with the layer stays **0.96**; the matcher alone is now 0.95 (58 of 61; was 0.93).
- **Precision rows read on 20 Nov** (`rescore_switch.py`): same outcome for all 180 (150 y, 1 n, 1 ? carried over).
- **Bills (A3.5):** `release_bills.csv` has exactly the same rows (only the order differs). **Martin's M6 does not
  need a rerun.**
- **Named examples (A3.7):** unchanged (Lawler 19.8%, Bacon 32.5%, Roy 5.0%; the mutual pairs hold).

## A4: what changed (`a4/out/results.csv`)

| Check | R exposed / safe | R gap (p) | D exposed / safe | D gap (p) | Interaction (p) |
|---|---|---|---|---|---|
| **Main** | **13.3 / 9.2** (was 13.2 / 9.2) | **+4.1** (0.004) | **11.6 / 9.0** (was 11.5 / 8.9) | **+2.6** (0.004) | **+1.5 (0.36)** (was +1.4, 0.40) |
| Cut-off 4 | 15.6 / 9.1 | +6.4 (<0.001) | 11.9 / 9.0 | +2.9 (0.002) | +3.6 (0.051) (was 0.061) |
| Cut-off 6 | 12.8 / 9.2 | +3.6 (0.006) | 11.5 / 9.0 | +2.5 (0.003) | +1.1 (0.48) |
| 2024 presidential margin | 14.7 / 9.1 | +5.6 (<0.001) | 11.8 / 8.9 | +2.9 (0.001) | +2.7 (0.12) |
| Without the 21 relabelled (check 1) | 13.2 / 9.3 | +4.0 (0.007) | 11.3 / 9.2 | +2.1 (0.019) | +1.8 (0.29) |
| Without redistricting releases (check 2) | 13.4 / 9.2 | +4.1 (0.004) | 11.6 / 9.1 | +2.6 (0.004) | +1.6 (0.35) |
| Without caucus releases | 13.0 / 9.0 | +4.0 (0.003) | 11.4 / 8.7 | +2.7 (0.002) | +1.3 (0.42) |
| Co-leads kept | 23.7 / 16.6 | +7.0 (0.003) | 19.8 / 13.5 | +6.3 (<0.001) | +0.7 (0.80) |
| Martin's matcher alone | 11.6 / 7.9 | +3.8 (0.003) | 9.7 / 7.5 | +2.2 (0.003) | +1.6 (0.29) |

- **Leave one state out:** R gap +3.6 to +4.9, D +2.1 to +3.1, interaction +1.0 to +2.5.
- **Lean as a number:** slopes R −0.24 points per point (p 0.003), D −0.14 (p < 0.001); unchanged.
- **Lean bands** (crossover / 0–5 / 5–10 / 10–20 / over 20): R 19.2, 11.7, 9.8, 9.2, 8.2%; D 14.2, 11.0, 9.2, 9.7,
  7.9%. Each about 0.1 point up; the peak in the closest seats is unchanged.
- **One thing to watch:** the cut-off-4 interaction is now p 0.051 (was 0.061). Still "a hint, not a finding", by
  the rule fixed in advance (p < 0.05 nowhere).

## The home network: what changed

| | 21 Nov | 22 Nov |
|---|---|---|
| Cross-party ties (undirected), mutual pairs | 6,732; 2,055 | 6,765; 2,060 |
| Ties in 2+ releases | 2,492 | 2,504 |
| Exposed share of members; of ties sent / received; of 2+ ties | 22%; 35% / 34%; 38% | 22%; 35% / 34%; 38% |
| S2 against the degree-preserving rewiring (N1) | 10.8% against 10.3%, ratio 1.05, p 0.025 | **10.7% against 10.2%, ratio 1.05, p 0.015** |
| S1 assortativity against N1 | −0.010 against −0.031, p 0.025 | −0.011 against −0.032, p 0.015 |
| S3 mutual, exposed–exposed against other | 62% against 45% | 62% against 45% |
| S4 same state, safe against exposed | 11.2% against 10.7% (p 0.76) | 11.1% against 10.7% (p 0.79) |
| Post hoc degree-matched S2 | ×1.11, p 0.02 | ×1.12, p 0.014 |
| Louvain: communities, modularity, **NMI with party** | 11, 0.273, **0.22** | 11, 0.272, **0.20** |
| Party cores | 124 (117 R), 101 (95 D) | 120 (112 R), 95 (89 D) |
| The close-seat community | 37 (19 R, 18 D), 19 exposed | **35 (17 R, 18 D), 19 exposed**: Malliotakis, Latta and Matsui left, McBride joined. Same partition otherwise (adjusted Rand 0.88 overall) |
| Other-party share of an exposed member's community (R / D) | 36% / 38% against 24% / 23% (p 0.010, < 0.001) | 37% / 39% against 26% / 26% (p 0.012, 0.002) |
| Backbone (α 0.01) | 1,659 of 29,163 ties | 1,656 of 29,210 (630 cross-party) |
| Nearest-neighbour readout of the drawing (3 seeds) | exposed 47–50%, safe 31–38% | exposed 46–50%, safe 30–41% |

**Centrality, after Holm (10 tests):**

| Measure | 21 Nov: p, Holm | 22 Nov: p, Holm |
|---|---|---|
| Cross-party degree, R and D | < 0.001, 0.001 | < 0.001, 0.001 |
| Degree (backbone), R | 0.001, 0.010 | 0.002, **0.013** |
| **Closeness (backbone), R** | 0.005, **0.034** (held) | 0.008, **0.055 (no longer holds)** |
| Betweenness (backbone), R | 0.010, 0.058 | 0.010, 0.059 |
| Betweenness given degree, D | 0.024, 0.12 | 0.016, 0.079 |
| Betweenness given degree, R | 0.068, 0.27 | 0.12, 0.47 |

**Correction:** "the Republicans' degree and closeness hold after Holm" becomes "**degree holds; closeness and
betweenness are borderline (Holm 0.055 and 0.059)**". Closeness hardly varies anyway (standard deviation 0.02 to 0.03).

## Figures

- **Redrawn:** `figure3_draft`, `figure_lean`, `figure_home_map`, `figure_network`, `figure_network_groups`.
- **The paper's `report/figures/figure3.pdf` is still the 21 Nov file.** Replace it with the new
  `a4/out/figure3_draft.pdf` when part 3 is written.
- **`figure_home_map`: the rings marked the wrong community** after the rerun (the 10-member California–Hawaii group).
  **Fixed 22 Nov:** the figure now picks the largest close-seat community (35, New York–Michigan). The figure is
  being redone anyway (open point 1 of the handoff).

## What to change elsewhere

- **The paper, part 3 (`report/sections/results.tex`):** the numbers are 13.3 against 9.2 and 11.6 against 9.0, and
  the interaction is 1.5 points, p = 0.36.
- **The abstract, introduction and discussion carry no part-3 numbers** and need no change. The Discussion's "show"
  should read "name" (Diego's file).
- **For Martin:** M6 is unaffected (same bill table).
