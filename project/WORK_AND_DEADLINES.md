# Work and deadlines

**Last updated: Wednesday 25 November 2026.**

**The analysis is closed (DECISIONS G17, G21; 25 Nov).** Nothing new is added. The home map and A5 stay in the
paper. What is left: decide the split of the report, cut and refine the text, the slides, the reflection, the
hand-in and the presentation.

This is the one place that says who does what, how far it is, and what is due when. The question and the
design are in [`README.md`](README.md). Every decision and its reason is in [`DECISIONS.md`](DECISIONS.md).

**Keep it current.** Whenever something changes (a task starts, finishes, is blocked, is dropped, changes
owner, or a date moves), update the table, change the date above and add a line to the log at the bottom.
This applies to people and to AI assistants working in the repository.

Status words: **Not started**, **In progress**, **Done**, **Blocked** (say by what), **Dropped**.

---

## 1. Deadlines

| Date | What | State |
|---|---|---|
| Wed 18 Nov, before the meeting | The three shared files exist in a first version (M1, M2, A1), so nobody waits on anybody; matcher precision counted (D1) | Passed: all three files and D1 delivered by 20 Nov |
| **Wed 18 Nov, 9:00–11:30** | Group meeting: fix the definitions, confirm owners, set up Overleaf (PNAS template), ask the TAs, test the labelling rules on 20 mentions. Plan and decisions in [`DECISIONS.md`](DECISIONS.md) | Done |
| **Fri 20 Nov** | Press releases for the first 20 Republicans. No data by then: the close-up is dropped (DECISIONS G5) | Done 20 Nov: first 20 collected, then all 412 members (G5 met) |
| **Sat 21 Nov** | Full labelling done, two coders per mention (DECISIONS G8) | Done 18 Nov |
| **Sat 21 Nov** | **Scope frozen (DECISIONS G17)** | Done |
| **Sun 22 Nov** | Numbers frozen. No definition changes after this | Done (after the 22 Nov reruns on the G18/G19 matcher) |
| Mon 23 Nov | Final data download, with the date recorded | Done: no new download. Press releases 20 Nov 2026, everything else 11 Nov (Congressional Record to 9 Nov), committees 22 Nov |
| **Tue 24 Nov, 20:00** | Full draft in Overleaf and a first version of the three slides. Everyone reads all of it | Draft complete in `report/sections/` (part 3 at full length); slides draft in `report/slides/slides.tex`. Move to Overleaf: not recorded here |
| **Wed 25 Nov, 14:00–17:00** | Group meeting: read aloud, cut to six pages, number check, rehearse | Held: home map and A5 kept, analysis closed (G21), G13 and G17 confirmed. **Still to decide: the split of the report and the cuts to six pages** |
| Thu 26 Nov | Submit all three PDFs. Friday is buffer only | Open |
| **Fri 27 Nov, 23:59** | **Hand-in deadline on DTU Learn: paper, slides and reflection, all three** | Open |
| **Wed 2 Dec** | **Presentation:** three minutes with the slides handed in on 27 Nov, then questions to whichever member the teachers pick | Open |

**What is handed in on 27 November, as three PDFs:**

1. **Paper:** PNAS template, at most six pages including figures and references.
2. **Slides:** three pages, no animations. The teachers merge every group's slides into one deck, so the
   slides cannot be changed after the deadline.
3. **Reflection:** half a page, ungraded.

`docs/AI_METHODS.md` must also be in the repository: done, moved there from `Diego/` on 25 Nov.

---

## 2. Who does what

Owners confirmed on 18 Nov (DECISIONS G3). Each member's README explains their parts and final numbers:
[`Martin/README.md`](Martin/README.md), [`Diego/README.md`](Diego/README.md), [`Anas/README.md`](Anas/README.md).

### Martin: the two maps (network and nulls)

| # | Task | Delivers | Needs | Status |
|---|---|---|---|---|
| M0 | Prototype of the two maps | `prototype_two_maps.ipynb`, one run | | Done (13 Nov) |
| M1 | Move the name matcher out of the notebook into `scripts/`, so floor speeches and press releases use the same one. First version by Wed 18 Nov, as it is in the notebook. The guard against senators and non-members can follow | One shared matcher: `Martin/matcher.py` | | Done. Fixes G14 (20 Nov), G18 and G19 (22 Nov). Hand checks done (`Martin/m1_checks_20nov/`): recall 12 of 13 on 30 turns, untitled names 30 of 30, list hits 20 of 20 |
| M2 | Write `mentions.parquet` and `named_ties.csv` from the floor speeches. First version by Wed 18 Nov | The two files in section 3, in `Martin/` | M1 | Done: rebuilt 20 Nov with the G14 matcher: 9,988 floor mentions (22 Nov, G19), 5,400 directed pairs. Old rows all kept; row numbers map through `Martin/m1_checks_20nov/row_map.csv` |
| M3 | Fix the definitions for part 1 in writing: how the working map is thinned, whether yields count, bill types | Definitions agreed by the group: `Martin/M3_PROPOSAL.md` | 18 Nov meeting | Decided 18 Nov (DECISIONS G1a–G1c): random working ties as headline, 200 draws; yields dropped from the headline; phrase rule. Applied. 20 Nov: 200 random working draws at the headline size done (28.6% against the floor's 38.7% after G19, G1a). Yield check done 21 Nov: phrase rule 15 of 15 right, window-only flags 14 (strictly 14, corrected 15) of 15 not yields (G1c). State null accepted (G16) |
| M4 | Harder null: rewire while keeping who spoke in the same debate | A second null for the floor map: `Martin/m4_debate_null.ipynb` | M2 | Done: rerun 22 Nov on the G19 mentions. Headline map Q 0.112 against 0.074 under the debate null (more divided than all 200): debates explain about two thirds |
| M5 | Louvain communities on each map; overlap with party and between maps (NMI) | Numbers for Results: `Martin/m5_communities.py`, `Martin/m5_committees/` | M3 | Done 20 Nov (choices agreed 21 Nov, G15): working map splits into the parties (NMI 0.83); floor map into 8 cross-party communities that follow committees. Final, after the 22 Nov rerun: NMI 0.03; 44% of floor ties inside a committee against 17.1% under rewiring |
| M6 | Null for the close-up: of a member's own bills, are the cross-party ones announced more often than a random draw? | The fair baseline (fix 1): `Martin/m6_closeup_null.py` | A3 | Done 22 Nov (G20): cross-party bills announced 52.7% against 45.1%; against same-party co-leads only +3.5 points (p 0.02). Anas: use the co-led row next to the main one in part 3 |
| M7 | Figure 1 (the two maps and their division against the nulls); network part of Results | Figure, text | M3–M5 | Figure 1 done 22 Nov (`Martin/figures/figure1.pdf`); Results text part 1 written (`Martin/results_part1.md`), in the paper as `report/sections/from_martin_results.tex` |
| M8 | The three slides: question and data; the main figure; what it means and how it was checked. PDF, no animations. **Due with the paper on 27 Nov** | Slides PDF | M7, A4, D2 | In progress: draft by Diego with Claude, `report/slides/slides.tex` (three frames: question and data, Figure 1, what it means; part 3 is one bullet on frames 1 and 3). Owner Martin. Due with the paper |

### Anas: the home text (close-up)

| # | Task | Delivers | Needs | Status |
|---|---|---|---|---|
| A1 | Change the collector to store the full text and the date of every release. It does not match names: the shared matcher (M1) does that. First version by Wed 18 Nov. Starting point: `archive/Anas_Claude/pilot/press_pull.py`; new home `scripts/` | A collector that keeps the text (fix 3) | | Done 20 Nov: collector keeps full text and dates (`Anas/collector/README.md`) |
| A2 | Collect the first 20 Republicans, spread over district lean. Then decide whether to go to about 60 | `data/processed/press_releases.parquet` (first part); go or no-go | A1 | Done 20 Nov: 55,023 releases from 412 members, snapshot 20 Nov (`Anas/press_releases/MANIFEST.md`) |
| A3 | Match each release to its bill by bill number; mark each named colleague as co-lead or not | Release-to-bill table (fix 1) | A2, M1 | Done 22 Nov; rerun 22 Nov on the G18/G19 matcher (`Anas/RERUN_22NOV.md`). Precision 0.96, recall 0.97, bill links 30/30 and 30/30 |
| A4 | Showcase ties: which Democrats each Republican names at home. Check the named examples (Roy–Cohen, Biggs–Jayapal, Lawler 1 of 10, Bacon 8 of 10) against full text | Table and figure for the close-up | A3 | Done 23 Nov: test, robustness, Figure 3 (one column, `Anas/a4/out/figure3.pdf`) and caption; checks T (names mostly partners) and I (seat and ideology inseparable), `Anas/a4/README.md`; home map. Part 3 text in `report/sections/results_part3.tex`, at full length until the split is decided (G21) |
| A5 | Optional: does a release that says "bipartisan" name a real cross-party partner? | One panel | A3 | Done 23 Nov (`Anas/a5/README.md`): both checks finished (28 of 30 named members are partners). Kept in the paper (G21) |
| A6 | Methods; `docs/AI_METHODS.md`; final data download; final assembly | Text and the required file | Ongoing | Methods on press releases done 23 Nov (`report/sections/methods_press.tex`); data snapshot 20 Nov 2026 (final, `Anas/press_releases/MANIFEST.md`). `AI_METHODS.md` with Diego (rows for A3.5, A5 and check T added 25 Nov). Final assembly: `report/` |

### Diego: validation and literature

| # | Task | Delivers | Needs | Status |
|---|---|---|---|---|
| D1 | Count the 30 matches printed in the prototype notebook; extend to about 100; report precision | Matcher precision for Methods: `Diego/d1_matcher_precision/REPORT.md` | | Done: 93 of 100 correct (95% interval 86 to 97%) on the prototype's matcher, which led to the fixes in G14 and G18. The current matcher's precision, 98 of 100, comes from code X in the D2 sample (DECISIONS G10) |
| D2 | Labelling protocol for cross-party floor mentions: agreeing, disagreeing or procedural. Draw the sample from `mentions.parquet` | Protocol and sample: `Diego/d2_labelling/PROTOCOL.md` | M2 for the sample; the protocol can start now | Done: **coding complete** 18 Nov. Pooled human κ 0.64. Cross-party: 69% agreeing, 7% disagreeing, 23% neutral. `Diego/d2_labelling/RESULTS.md` |
| D3 | Read Westwood and Harbridge: three lines on what each found. Settle Westwood's year. Find three or four more references | Note on prior work; reference list: `Diego/d3_prior_work.md`, `references.bib` | | Done: eight references verified; Westwood read at the publisher (2022, online Jan 2021) |
| D4 | Introduction and Discussion; the half-page reflection. **The Introduction and Discussion are now written together (DECISIONS G3)** | Text: `report/sections/introduction.tex`, `discussion.tex` (snapshot in `Diego/d4_introduction_discussion/`) | D3 | Drafted by Diego with Claude and revised with Martin (G3), together with the abstract and significance statement. Reflection draft in `Diego/reflection_draft.md`, for Diego to rewrite. Cuts follow the split |
| D5 | TF-IDF and logistic-regression classifier trained on the 100 hand labels (D2), checked by leave-one-out against them, applied to all floor mentions: share of P/A/D/N/X for cross-party and same-party mentions | `Diego/d5_classifier/`: results, shares table, one figure | D2 labels | Done: 73% against a 72% always-agreeing baseline, so not used as a measurement. Rerun 22 Nov on the 9,988-mention file (applied to 9,909 R–D mentions); unchanged |

### Everyone

| # | Task | Delivers | Status |
|---|---|---|---|
| S1 | Second-code the labelling sample from D2: Martin rows 1–25, Anas rows 76–100 (Claude coded 26–75). Report κ per pair | Agreement score for part 2 | Done 18 Nov: Diego–Martin κ 0.59, Diego–Anas κ 0.69 (25 rows each) |
| S2 | Hand-check the 60 sampled speaker turns in `data/processed/speaker_check_sample.csv` | Agreement rate for Methods | Done 22 Nov (Diego): 60 of 60 turns assigned to the right speaker (95% interval 94–100%). `Diego/s2_speaker_check/` |
| S3 | Read the full draft and comment. Explain out loud one method you did not build | Everyone can answer for the whole paper | Not started |

---

## 3. Working without waiting on each other

> The plan of 18 Nov, kept as the record; every step in it is done. The shared files ended up in the owners'
> folders: `Martin/mentions.parquet`, `Martin/named_ties.csv` and `Anas/press_releases/` (three parts).

Each person has their own notebook and their own script. The streams meet only in three shared files in
`data/processed/`. **The columns below are the agreement.** Anyone can build against them before the file
is complete, and nobody changes a column without saying so in the chat.

| File | Written by | Read by | One row is | Columns |
|---|---|---|---|---|
| `mentions.parquet` | Martin (floor), Anas (press), both with the shared matcher | Diego (D1, D2), Martin, Anas | One mention of a member | `speaker`, `named` (Bioguide IDs), `source` (`floor` or `press`), `date`, `doc_id`, `context` (the sentence), `is_yield` |
| `named_ties.csv` | Martin | Martin, Anas | One pair of members per source | `speaker`, `named`, `source`, `n_mentions` |
| `press_releases.parquet` | Anas | Anas, Martin (M6) | One press release | `bioguide`, `url`, `date`, `title`, `text` |

**Can start today, with nothing from anyone else**

- Martin: M1, M2, then M4 and M5.
- Anas: A1, A2.
- Diego: D1 (the matches are printed in the prototype notebook), D3, the protocol half of D2.
- Everyone: S2.

**The places where one person waits on another**

| Waiting | On | How to keep it short |
|---|---|---|
| Diego's labelling sample (D2) | Martin's `mentions.parquet` (M2) | Martin writes a first version by Wed 18 Nov straight from the prototype. A better matcher later only adds rows |
| Anas's bill matching (A3) | Martin's shared matcher (M1) | Same date. Until then Anas collects text, which needs no matcher |
| Martin's close-up null (M6) | Anas's release-to-bill table (A3) | The latest link in the chain. Martin builds it against the columns above with the 280 sampled releases |
| Martin's definitions (M3) | The 18 Nov meeting | Everything before M5 runs on the prototype's definitions |
| The slides (M8) | One figure from each stream | Each stream delivers its figure by the draft on Tue 24 Nov |

**Two things that cannot be done alone:** the second coding of the labelling sample (S1), and reading
each other's parts (S3).

**The order that matters most:** D2 and S1 decide the headline of part 1 ("less divided" or "talks across
the aisle to argue"). Do them early.

**If the collection fails after A2:** parts 1 and 2 still make a paper. Drop A3–A5 and M6.

---

## 4. Open questions for 18 November

> All answered: 1 by G3, 2 by G1a to G1c, 3 by G13 (both parties), 4 by G2 and G11, 5 by G6 (figure 3 became naming
> by district lean).

1. **Confirm the owners in section 2.**
2. **Definitions for part 1 (M3):** which thinning rule for the working map; whether yields are in the
   headline number.
3. **Republicans only, or both parties**, in the press-release collection.
4. **Ask the teachers:** does "naming against working", with a hand-labelled sample, count as enough
   language analysis? Is a dataset chosen after the 4 November lock accepted?
   **18 Nov:** no clear answer from the teachers. Decided: plan B, a classifier on the hand labels (D5), so the
   language part uses the course's own NLP tools and not reading alone.
5. **Three figures:** proposed are the two maps; what a cross-party mention means; the showcase ties.

---

## 5. No longer needed

From the earlier plans in `archive/`, and since the scope freeze (G17). Listed so nobody keeps working on them.

| Task | From | Why dropped |
|---|---|---|
| New analyses, data sources, nulls, figures or checks not listed in section 2 | Everyone, from 21 Nov | Scope frozen (G17). New ideas go into the Discussion as future work |
| Optional items not finished by Sun 22 Nov: the redrawn-state before/after check; the curve of cross-party share against ties kept (A5 was finished and kept) | Anas, Martin | Scope frozen (G17) |
| The committee test of why exposed Republicans and Democrats connect across the aisle differently in the home map | Anas | Analysis closed (G21); part 3 says "we did not test why" |
| 2017–18 kill test | Diego, for directions C and P2 | Those directions were not chosen |
| `blocs.csv`; rerunning pilot 4.3 on backbone blocs; checking pilot 4.1 against the blocs notebook | Martin, pre-meeting tasks | Blocs are not part of the design. They can return as an optional grouping |
| Stop lists and the talk score | Walk or talk | No vocabulary score in the design |
| Redrawn-district lean; state differences in running ahead | Walk or talk; blocs | The election is the setting, not the outcome. (Later, district lean became the core of part 3: G13) |
| Change over time ("the clock"), mutual showing, Democrats in Trump districts, the Trump node | Council options C, E, F, D | Too thin, or need more collection than we have time for. (Democrats and mutual pairs came back with G13; mutual pairs are documented, not in the paper) |

---

## 6. Log

Newest first. One line per change.

- **25 Nov 2026.** Martin (with Claude): the paper cut to 6 pages from the printed comments (DECISIONS G22), in
  `Martin/final_report/two_maps_full_draft_overleaf/` with `main.pdf` next to `main.tex` and an Overleaf zip beside
  the folder. `AI_METHODS.md` moved to `docs/`. Figure 4 for the paper without the note under panel B
  (`figure_home_map.py --no-note`). No number changed.
- **25 Nov 2026.** Martin (with Claude), layout pass on the full draft (`Martin/final_report/two_maps_full_draft_overleaf/`),
  no text changed: tighter float spacing; Figure 1 (`m7_figure1.py`) 0.7 in shorter; Figure 4 (`Anas/a4/figure_home_map.py`)
  legends moved under panel B; a side-by-side Figure 3 (`figure3_column.py --wide`, switch in `main.tex`); Figure 4 placed
  on page 5. Then: Figure 1 a side-caption figure (SCfigure*, 11.4 cm, `m7_figure1.py --side` writes
  `figure1_side.pdf`; the full-width file stays for the slides); Figure 4 kept full width so the purple ties show;
  Figure 3 one column with panel B 0.7 in shorter and near-black axes; Figure 4 panel B axes near-black; Figure 2
  4.4 cm tall (`figure2.py --short`). Still 7 pages; page 7 has 52 free lines in its right column. Text take-aways from Sekara et al. (PNAS 2016) saved in `Martin/final_report/TEXT_TAKEAWAYS.md`
  for the pruning pass, which waits for the group's printed feedback.
- **25 Nov 2026.** Anas (with Claude): G17 confirmed by Anas and Diego; new G21 (home map and A5 kept, analysis
  closed, committee test not run); G6's open dependency settled. This file brought to the final state (deadlines,
  task statuses, owners note, sections 3 to 5). `DICTIONARY.md` rewritten in plain language with an A to Z index.
  `report/README.md` and the contributions line updated; `serrano2009` and a Voteview reference placed in part 3;
  Anas's four rows added to `Diego/AI_METHODS.md` (Diego's note invites additions). No number changed.
- **25 Nov 2026.** Anas (with Claude): G13 entered in `DECISIONS.md` (swing seat and window, agreed by Martin on
  23 Nov and Diego; draft scaffolding removed; `Anas/G13_UPDATE.md` removed). `README.md` rewritten to the project's
  final state (question and answer, the three networks, the parts, limits, data, layout). `DICTIONARY.md`: a kind for
  every term (general, politics, course, statistics, data, ours) and a new section 0 on words we use more narrowly
  than usual (moderate, exposed, name, partner, divided, bipartisan, ...). No number changed.
- **25 Nov 2026.** Anas (with Claude): the glossary and the list of methods from outside the course moved from
  `Anas/` to the project folder (`DICTIONARY.md`, `OFF_CURRICULUM.md`) and updated to the final versions of all three
  parts; linked from `README.md`. Open in them: `serrano2009` not yet cited in part 3, `landis1977` unused, no
  Voteview reference. Martin confirmed G13 (swing seat) on 23 Nov; Diego's answer is still needed before pasting it.
- **25 Nov 2026.** Anas (with Claude): `Anas/` holds only the final state of part 3. The home map and A5 are
  accepted into the paper and the analysis is closed (the committee test of the network twist is not run).
  `Anas/README.md` rewritten so a teammate's Claude can use and explain each part (text in the paper, headline
  numbers, where the methods disagree, findings not in the paper). Removed: `STATUS.md`, `REVISIONS_19NOV.md`,
  `references_additions.bib` (all in `report/references.bib`), the Figure 3 and home-map figure drafts, `state_seats/`.
  Status lines updated in place; in `report/sections/` only `%` comment lines of part 3 changed. No number changed.
- **25 Nov 2026.** Martin (with Claude): `Martin/` holds only Martin's own parts. No whole-paper draft is on `main`
  in `Martin/`; Martin's full draft (`Martin/paper_v1/`, 24 Nov) exists only on the unmerged branch
  `claude/nice-bardeen-snc57e` and is not to be merged. `Martin/README.md` rewritten so a teammate's Claude can use
  and explain each part (M1–M7, Methods, Figure 1); the final texts stay in `results_part1.md` and
  `methods_networks.md` (checked: `report/md2tex.py` output matches the paper's sections).
- **23 Nov 2026.** Martin (with Claude), in `report/`: citations placed in the text of the Methods (Martin's: Fowler,
  Newman, Maslov–Sneppen, Blondel, Danon; Diego's paragraph: Cohen, Wilson) instead of a bare list at the end;
  repository link added; S2 result written into `Martin/methods_networks.md`. Discussion: the home-map sentence now
  says seat and ideology cannot be separated (Anas's check I: 1.1 of 4.1 and 0.2 of 2.6 points left within
  ideology bands). Still to cite: `serrano2009` for the home map's backbone (Anas).
  Later the same evening: the Wilson citation moved to its first use (the S2 sentence in Martin's Methods).
- **23 Nov 2026.** Anas (with Claude): two checks on part 3, designs written before running (`Anas/a4/CHECKS_PLAN_23NOV.md`). T: of 60 counted cross-party press names, 77% are partners or praise and 1 is criticism (three blind AI readers; Anas read the 4 differences). I: exposed members are mostly their party's moderates (DW-NOMINATE); within ideology bands the gap mostly disappears (R 1.1 of 4.1 points left, D 0.2 of 2.6; p 0.39, 0.76), so seat and ideology cannot be separated. Part 3 rewritten at full length with these and the methods' disagreements kept (`report/sections/results_part3.tex`), for the 25 Nov cut. Discussion wording for Martin and Diego in the group chat.
- **23 Nov 2026.** Anas (with Claude): A5 done: of 30 "bipartisan" releases with a named member of the other party, 28 name a partner and none an opponent (rule fixed first: 27). Part 3 placed in `report/` (Results, Methods `methods_press.tex`, Figure 3 one column with caption); `holm1979`, `wilson1927`, `cohen1960` added to `references.bib` (checked). Methods from outside the course listed with reasons in `Anas/OFF_CURRICULUM.md`.
- **22 Nov 2026.** Anas (with Claude): A5 nearly done (`Anas/a5/`, design fixed first in `a5/PLAN.md`). 64% of releases that say "bipartisan" have a House partner of the other party (named or on a cited bill), against 9% of other releases; of 30 without one, three blind readers find 29 name no partner (one names a senator); Anas read the 2 disagreements. One check left (Mon 23 Nov): whether the named partners are partners. Optional under G17: Martin and Diego to keep or cut.
- **22 Nov 2026.** Anas (with Claude): Results part 3 drafted (`Anas/results_part3.tex`, about 335 words, over the ~200 budget; network paragraph first to cut). Home-map figure redesigned and the network measures put in a table (`Anas/a4/`). Disparity-filter alpha checked: 0.01 is the strictest that keeps all members connected; centrality results point the same way at six alphas (`Anas/a4/NETWORK_METHODS.md`).
- **22 Nov 2026.** Anas (with Claude): A3 and A4 rerun on Martin's 22 Nov matcher (G18). Press mentions 129,052 → 129,473; part 3 now Republicans 13.3% against 9.2%, Democrats 11.6% against 9.0%, interaction +1.5 (p 0.36); every reading holds. Republican closeness no longer survives Holm. M6 unaffected (same bill table). `Anas/RERUN_22NOV.md`.

- **22 Nov 2026.** S2 done by Diego: 60 of 60 sampled turns are assigned to the member the Record names as speaker
  (94–100%). Filled into the report's Methods (via `report/md2tex.py`; Martin: the sentence in
  `Martin/methods_networks.md` can be replaced with it) and Discussion.
- **22 Nov 2026.** Diego (with Claude): paper set up in `report/` for Overleaf (PNAS `main.tex`, sections,
  figures 1 to 3, `references.bib` with Blondel 2008 and Danon 2005 added as Martin asked); Martin's Results part 1
  and Methods converted by `report/md2tex.py`; Results part 2, Figure 2 and Methods for labelling and classifier
  written; first drafts of Introduction, Discussion, abstract, significance statement and contributions. D5 rerun
  on the new mentions (unchanged). `AI_METHODS.md` moved from Anas (A6) to Diego at Diego's request. Slides draft
  (M8) started. A1 to A4 rows updated from `Anas/STATUS.md`. S2 still not started (Diego).
- **22 Nov 2026.** Methods text for data, name matching and networks drafted (`Martin/methods_networks.md`). Needs S2
  (speaker check, not started) and two references (Blondel 2008, Danon 2005) in `references.bib`.
- **22 Nov 2026.** M7: Figure 1 final (four panels) and the part 1 Results text with caption (`Martin/results_part1.md`),
  plus a ready M6 paragraph for part 3. The optional thinning curve is dropped (G17).
- **22 Nov 2026.** M6 first run (G20): members announce their cross-party bills more often than their other bills
  (52.7% against 45.1%), mostly because co-led bills are announced more than solo ones (+3.5 points against
  same-party co-leads, p 0.02). No control for whether a bill moved.
- **22 Nov 2026.** Untitled (30 of 30) and list (20 of 20) checks coded by Martin. By the rule fixed in advance,
  untitled full names now count on the floor (G19): 9,988 mentions. Everything rerun: headline 38.7% against 28.6%
  (3,970 ties), debate null 0.074 against 0.112, communities still follow committees. All of Martin's hand checks
  are done.
- **22 Nov 2026.** Floor recall check coded by Martin: 12 of 13 named members found (92%, 67–99%); the miss is an
  unresolvable shared surname. Diego: this is the number for your recall sentence in part 2.
- **22 Nov 2026.** Matcher fixes G18 (possessives, middle initials; Anas's checklist items 12 and 15): 9,058 floor
  mentions (+440, 4 wrong ones removed). M3 to M5, committee check, state null and Figure 1 rerun: headline 39.3% against
  28.6% (3,675 ties); every reading holds. Diego: rerun D5 on the new file.
- **21 Nov 2026.** G1c yield check coded by Martin: the phrase rule's 15 extra flags are all yields; 14 of the window
  rule's 15 are not (the 15th is a sheet ambiguity). Headline unchanged.
- **21 Nov 2026.** **Scope frozen (G17)**, proposed by Martin; Anas and Diego to confirm. G14 (matcher, with the
  24-of-30 rule) and G15 (M5 choices) agreed by Martin. Anas switches A3 to the current matcher. Past deadlines in
  section 1 marked done.
- **20 Nov 2026.** Martin (with Claude): state null accepted as a part 1 robustness row (G16; Q 0.002 against
  0.106); scoring script for the hand checks; first draft of the part 1 Results text (`Martin/results_part1_draft.md`).
- **20 Nov 2026.** Audit (Martin with Claude): the list rule double-counted 4 names that followed a list with their own
  title; fixed with a test (8,626 → 8,622 mentions, no tie changed, M4 rerun). Claims corrected: only four of the six
  nickname members gain floor rows; the untitled-name threshold is Claude's proposal, not agreed.
- **20 Nov 2026.** Martin (with Claude): M4 rerun on the new mentions (debates explain about two thirds of the
  headline map's division); M5 first run (floor communities are committees, not parties; G15 open); first draft of
  Figure 1; Anas's state null rerun on the new mentions (Q 0.003 against 0.106). `Martin/README.md` now opens with
  the current state.
- **20 Nov 2026.** Martin (with Claude): matcher changes from Anas's checklist applied (G14); `mentions.parquet`
  rebuilt, 8,092 → 8,622 mentions, none lost, Diego's D2 rows checked. M3 table rerun with G1a's 200 random draws:
  headline floor map 39.2% cross-party (3,573 ties) against 28.6% (26.5–30.4%) for random working ties. Three hand
  checks for Martin drawn in `Martin/m1_checks_20nov/`. Not reflected here yet: Anas's 20 Nov A1 progress (see
  `Anas/STATUS.md`).

- **19 Nov 2026.** Anas: press-release scope (both parties), matcher checklist, seats per state, state-null proposal for Martin and a project dictionary uploaded to `Anas/`. Proposed revisions to parts 1–3 and the open part 3 decisions in `Anas/REVISIONS_19NOV.md`. G13 added (Democrats included, small). A1 not started.

- **18 Nov 2026.** D2: Diego changed rows 38 and 86 to X (matcher errors the AI coders flagged). Matcher
  precision in the sample 98 of 100 (G10). Pooled human κ 0.64. Cross-party: 69% agreeing, 7% disagreeing.
  Headline: cross-party mentions are mostly credit, the "argue" reading is out.
- **18 Nov 2026.** M3: phrase yield rule applied in `Martin/mentions.parquet` (`is_yield`; the old flag is kept as
  `is_yield_window`). 1,427 against 1,406 flags on the R–D mentions, 285 disagreements. Rows unchanged; Diego's D2
  keys checked. Diego: rerunning D5 carries the new flag into `predictions.parquet`.

- **18 Nov 2026.** **D2 coding is complete**, so G1c can go ahead on `mentions.parquet`. Human κ 0.59 and 0.76
  (pooled 0.67, above the 0.6 set in advance). Cross-party mentions: 71% agreeing, 7% disagreeing, 23% neutral,
  0% procedure. D5 classifier does not beat always-agreeing (74% against 73%): hand-labelled shares carry part 2.
  Two rows (38, 86) look like matcher errors that Diego coded as real mentions; his to recheck.
- **18 Nov 2026.** Merged with Diego's D2 and D5 commits. DECISIONS corrected: G10 (precision from code X in the
  100-row D2 sample, no separate check), G8 (100 rows, Claude second coder on 26–75, not yet discussed by the
  group), G2a and G11 (no clear TA answer, D5 classifier), G1c (about 9 yields in the sample, so the 30
  rule-disagreement rows are the main test; `mentions.parquet` unchanged until Diego finishes coding).

- **18 Nov 2026.** M3 decided (DECISIONS G1a–G1c): random working ties as the headline (200 draws), strongest ties
  second, backbone as a robustness row; **yields dropped from the headline**, against the proposal; phrase yield
  rule, tested on fresh rows before the freeze. Added before Sun 22 Nov: random draws at 3,284 ties and about 30
  rule-disagreement rows (Martin); new matcher precision re-measured (Diego, Martin checks about 25; G10). Yields stay in
  the labelling sample (G9).

- **18 Nov 2026.** `DECISIONS.md` created: every decision with its reason and alternative. Meeting moved to
  9:00–11:30. From the meeting plan: owners (Introduction and Discussion now written together), press releases
  Republicans only, swing against safe seats, close-up dropped if no data by Fri 20 Nov, three figures,
  labelling by two coders due Sat 21 Nov. M3 definitions and the TA answers still open.

- **18 Nov 2026.** D2: three more independent AI codings of all 100 mentions (AI1 to AI3), at Diego's request.
  They agree with each other on 99 to 100 of 100, so they add stability, not independence. Scored against
  Diego's codes when his sheet is in.
- **18 Nov 2026.** D3 done: Westwood's abstract read at the publisher and the note corrected (floor votes,
  1994–2018). Report skeleton with page budget and owners in `Diego/report_skeleton.md`.
- **18 Nov 2026.** Plan B for the language part: D5 added (TF-IDF classifier trained on the D2 labels, checked
  against them, applied to all floor mentions). Pipeline runs on a placeholder. S1 updated to the 25-row split.
- **18 Nov 2026.** D2: labelling set at 100 mentions (75 cross-party, 25 same-party) in
  `Diego/d2_labelling/D2_full_sheet.xlsx`. Diego codes all; Martin rows 1–25, Anas rows 76–100, Claude rows
  26–75 as second coders. S1 is now 25 rows each for Martin and Anas.
- **16 Nov 2026.** M3 started (Martin with Claude): proposal for the part 1 definitions written in
  `Martin/M3_PROPOSAL.md`. Against working ties drawn at random at the same size, the floor map is 34.2%
  cross-party against 29.5%, a gap of 5 points, not the 22 against the strongest ties. A phrase-based yield
  rule finds 30 of 30 yields labelled in D1. Open for D1: the new matcher's precision is not measured.

- **16 Nov 2026.** M4 started (Martin with Claude): first run of the null that shuffles names inside each
  debate. Party modularity of the floor map 0.156 against 0.077 under the null (0.116 against 0.068 with
  yields dropped); observed beyond all 200 rewirings. One run, prototype definitions. Details in
  `Martin/README.md`.

- **16 Nov 2026.** M1 and M2 started (Martin with Claude): first versions of the shared matcher and of
  `mentions.parquet` and `named_ties.csv`. They are in `Martin/`, not `scripts/` and `data/processed/`,
  because of the folder rule: D2 unblocked, pass `Martin/mentions.parquet` to the sampling script. Details
  in `Martin/README.md`.

- **16 Nov 2026.** D1: Diego checked 95 of the 100 labelled matches and overruled none; precision 93% stands.
  New for M1: accented surnames (Velázquez, Barragán, Sánchez, García) are never matched.
- **16 Nov 2026.** Folders `Diego/`, `Martin/` and `Anas/` created in `project/`; each member writes only in
  their own. Diego's work moved there from `Diego_Claude/`. Pushed to `main` at Diego's request.
- **14 Nov 2026.** Diego's stream started in `Diego/` (Diego with Claude). D1: 93 of 100 random
  matches correct, first-pass labels awaiting Diego's check; the roster stores 18 surnames in capitals, so
  those members are never matched and four namesakes receive their mentions (for M1). D2 protocol version 1,
  D3 note and D4 drafts written.
- **13 Nov 2026.** First versions of the shared files (M1, M2, A1) moved from Sun 15 Nov to Wed 18 Nov,
  before the meeting.
- **13 Nov 2026.** Pull request 5 merged to `main`. Slides are due with the paper on 27 Nov, not at the
  presentation: deadlines updated and slides made their own task (M8). Section 3 rewritten: columns of the
  three shared files fixed, first versions due Sun 15 Nov, A1 no longer depends on the matcher.
- **13 Nov 2026.** File created. Direction settled: two maps of Congress as the main question, press
  releases as the close-up, three fixes to the press-release test. Earlier plans moved to `archive/`.
  Prototype M0 done. Owners proposed, not confirmed.
