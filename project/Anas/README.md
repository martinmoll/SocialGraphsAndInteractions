# Anas

Anas's own folder. Each member writes only in their own folder (`Diego/`, `Martin/`, `Anas/`) and never edits or deletes another's.

**Start here: [`STATUS.md`](STATUS.md)** (updated 22 Nov). **A3 and A4 are complete (rerun 22 Nov on the new
matcher); A5 is one check from done.** What needs Martin and Diego is listed first.

**New, 22 Nov evening: A3 and A4 rerun on Martin's 22 Nov matcher** ([`RERUN_22NOV.md`](RERUN_22NOV.md)).
- **Why:** Martin adopted checklist items 12 and 15 (G18), so floor and press now count the same name forms again.
- **A3:** 129,473 press mentions (was 129,052), still 14.4% cross-party; recall with the layer unchanged (0.97).
- **A4:** Republicans 13.3% against 9.2%, Democrats 11.6% against 9.0%, interaction +1.5 (p 0.36). Every reading
  and every robustness row holds.
- **Home network:** NMI with party 0.20 (was 0.22); configuration-model p 0.015 (was 0.025); the close-seat
  community has 35 members, 19 exposed (was 37). **Correction:** Republican closeness no longer survives Holm.
- **For Martin:** M6 is unaffected; `a3/out/release_bills.csv` has the same rows.

**Also new, 22 Nov, late:**
- **Results part 3 draft for the paper:** [`results_part3.tex`](results_part3.tex), about 335 words, to `\input` in
  `report/sections/results.tex` under "Close-up" (Martin's M6 paragraph stays after it). Over the ~200-word budget:
  the network paragraph is the first to cut on Wednesday, and the A5 paragraph is marked optional.
- **The home-map figure, redesigned** ([`a4/README.md`](a4/README.md), `a4/out/figure_home_map.png`): purple ties
  across the aisle, grey within a party; names beside the map; panel B is plain bars of cross-party ties per member.
  The other network measures are a table: `a4/table_home_measures.py` (`.md` and `.tex`).
- **Disparity-filter α checked:** α = 0.01 is the strictest that keeps all 406 members connected
  (`a4/alpha_sweep.py`). Backbone centrality at six α values (`a4/alpha_centrality.py`): every result points the
  same way; Republican betweenness and closeness and the Democrats' "brokering" pass Holm from α 0.02 up, not at 0.01.
  `a4/NETWORK_METHODS.md` §1 and §3d.
- **A5, nearly done** ([`a5/README.md`](a5/README.md)): 64% of releases that say "bipartisan" have a House partner of
  the other party, against 9% of other releases; of 30 without one, 29 name no partner. One check left (Mon 23 Nov).
  Optional under G17: please keep or cut.

**For Martin and Diego (please read):**

- **Martin: [`MATCHER_CHECKLIST.md`](MATCHER_CHECKLIST.md) items 12 to 15.** Done 22 Nov: 12 and 15 adopted (G18),
  14 adopted with G19, 13 left as harmless.
  - **12, possessives:** "Mr. Cole’s amendment" is never matched. A rerun with the possessive removed gives +417
    floor mentions (4.8%).
  - **15, middle initials:** "Congressman Riley M. Moore" is read as Josh Riley.
  - Both are worth one edit before the freeze. Items 13 and 14 are harmless, so we can answer for them if asked.
  - STATUS section 0, row 9.
- **Both: [`G13_UPDATE.md`](G13_UPDATE.md).** Anas's choice for G13's open points, to paste into `DECISIONS.md` if
  you agree.
  - **Swing seat:** `exposed_2025`, lean within 5 points toward the member's own party, on the district served.
  - **Window:** 3 Jan 2025 to 20 Nov 2026.
  - It is written here and not in `DECISIONS.md` itself because Martin's newest `DECISIONS.md` was then on an
    unmerged branch. It is merged now (22 Nov), and G13 is still the "Draft for G13" there.
- **Both: G17 (scope freeze).** Anas's A4 network extension (`a4/HOME_NETWORK_PLAN.md`, `a4/NETWORK_METHODS.md`) is
  new analysis after the freeze. Please accept it or cut it.

**New since the last upload (20 Nov evening):**

- **A3 now uses Martin's 20 Nov matcher** (G14), code unchanged, with press input (untitled names, members' own first
  names) and a thin layer: [`A3_MATCHER_SWITCH.md`](A3_MATCHER_SWITCH.md).
  - **17 hits disagree** with the old layer, and the new version is right in all 17.
  - **Press mentions:** 129,052 once per release, 14.4% cross-party (33.0% weighted by 1/n); 129,473 since the
    22 Nov rerun.
- **A3.4, recall** ([`a3/README.md`](a3/README.md)):
  - **Readers:** 40 releases read by five blind AI readers, with Anas checking every disagreement
    (`a3/recall_check/DIFFERENCES.md`).
  - **Result:** press recall 0.97 and precision 0.96 with the layer; 0.73 and 0.93 for the floor matcher alone.
  - **It found the middle-initial bug,** now corrected on the press side.
- **A3.5, bills:** 18,177 bill links in 25% of releases, found by number and by exact title. Precision 30 of 30
  each, by three blind readers.
- **A3.6 and A3.7:** **[`a3/out/mentions_press.parquet`](a3/out/mentions_press.parquet)**, the press-mention file,
  with flags (co-lead, leader, same state, list, caucus, redistricting) and 1/n weights. The named examples are
  checked: all mutual pairs hold, but the pilot's Lawler and Bacon figures do not.
- **A4, first run:** [`a4/README.md`](a4/README.md), Figure 3 draft `a4/out/figure3_draft.png`.
  - **Result:** exposed members name the other party more in **both** parties. Republicans 13.3% against 9.2%,
    Democrats 11.6% against 9.0%, each p < 0.01 (22 Nov rerun). The difference between the parties is small and not significant.
    By the reading fixed in advance, that is a seat effect, not a president's-party effect.
  - **Robustness:** it holds in every pre-registered check (cut-offs 4 and 6, second lean source, without
    relabelled members, without redistricting or caucus releases, leave one state out, floor matcher alone).
  - **The effect sits in the closest and crossover seats** (`a4/out/figure_lean.png`).
- **A4 extension, the home map** (needs G17 acceptance; [`a4/NETWORK_METHODS.md`](a4/NETWORK_METHODS.md) has every
  value and formula):
  - **Hubs:** exposed members are the hubs of cross-party naming. They are 22% of members but take part in 35% of
    cross-party ties.
  - **Each other:** they tie to each other 5% beyond their activity (configuration-model null).
  - **Communities:** Louvain finds a 35-member bipartisan community, 19 of them exposed (37 before the rerun). The other mixed
    communities are state delegations.
  - **Same state:** safe members' cross-party ties are no more local.
  - **Centrality:** exposed members have far more cross-party ties; the rest is Holm-corrected in the methods file.

| File or folder | What | Date |
|---|---|---|
| [`STATUS.md`](STATUS.md) | Status, findings, proposed revisions to parts 1 to 3, priority list | updated 22 Nov 2026 |
| [`a5/README.md`](a5/README.md) | A5: "bipartisan" releases and real partners (design `a5/PLAN.md` fixed first; blind-reader check). One check left, 23 Nov | 22 Nov 2026 |
| [`results_part3.tex`](results_part3.tex) | Results part 3 draft for the paper (A4 and the home map), to `\input` in `report/sections/results.tex` | 22 Nov 2026 |
| [`RERUN_22NOV.md`](RERUN_22NOV.md) | A3 and A4 rerun on Martin's 22 Nov matcher: old against new for every number | 22 Nov 2026 |
| [`a4/`](a4/README.md) | **A4:** the test (`analysis.py`), Figure 3 draft, the all-members lean plot, the home-map network extension (plan, tests, null model, centrality, communities, figures) and [`NETWORK_METHODS.md`](a4/NETWORK_METHODS.md) with every value and formula | 21 to 22 Nov 2026 |
| [`G13_UPDATE.md`](G13_UPDATE.md) | Anas's swing-seat definition and date window, to paste into `DECISIONS.md` G13 if agreed | 21 Nov 2026 |
| [`A3_MATCHER_SWITCH.md`](A3_MATCHER_SWITCH.md) | Why and how A3 moved to Martin's 20 Nov matcher, what the press side adds, and what was found | 21 Nov 2026 |
| [`press_releases/`](press_releases/MANIFEST.md) | **The press data:** 55,023 releases from 412 members, 3 Jan 2025 to 20 Nov 2026, in three parquet files split by member. Read `MANIFEST.md` for how to load them | 20 Nov 2026 |
| [`A3_PLAN.md`](A3_PLAN.md) | A3 plan: steps A3.0 to A3.7, the eight decisions, traps, fallbacks, the confusion-table template | 20 Nov 2026 |
| [`a3/`](a3/README.md) | **A3 scripts and results, A3.0 to A3.7:** frozen inputs (commit `7bdbc18c`), Martin's matcher and the press layer, precision, recall (`recall_check/`), bills (`bill_check/`), flags and the press-mention file (`out/mentions_press.parquet`), named examples. The two large hit files are not uploaded; the scripts rebuild them in about two minutes | 20 to 21 Nov 2026 |
| [`collector/`](collector/README.md) | **A1:** the press-release collector, its checks and every fix, the WordPress API cross-check, `split.py` | 20 Nov 2026 |
| [`MATCHER_CHECKLIST.md`](MATCHER_CHECKLIST.md) | For Martin: 15 matcher items with evidence, a recommendation and a deadline for each. Items 12 to 15 new 21 Nov (possessives, Washington, untitled guard, middle initials). Scripts in `matcher_check/` | 18 Nov; 9 to 11 added 20 Nov; 12 to 15 on 21 Nov |
| [`methods_drafts.md`](methods_drafts.md) | Draft Methods and limitation sentences (A6), five checks fixed before the results, data sources table | 19 to 20 Nov |
| [`district_lean/`](district_lean/README.md) | `member_lean.csv` (the file to use): district served and its lean, the 2026 district run in, a second lean measure (2024 presidential margin), fate in 2026. `redraw_dates.csv`: when each of the nine new maps was settled, checked against official sources | 19 to 20 Nov |
| [`press_scope/`](press_scope/README.md) | How many press releases every House member has published since Jan 2025, both parties; layouts of the sites; a small name pilot; recheck of the uncounted sites. No release text collected | 18 Nov, rechecked 19 Nov |
| [`state_seats/`](state_seats/README.md) | Seats per state by party and exposure, redrawn states, releases per state; what the state layer is useful for | 19 Nov |
| [`state_null/`](state_null/README.md) | **For Martin:** proposal and pilot for a null that keeps members' own states. Pilot: state explains almost none of the party division in either map | 19 Nov |
| [`dictionary.md`](dictionary.md) | Every term the project uses, in plain words, so the three of us read them the same way | 19 to 20 Nov |
| [`REVISIONS_19NOV.md`](REVISIONS_19NOV.md) | Replaced by `STATUS.md` | 19 Nov |
