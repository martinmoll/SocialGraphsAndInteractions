# Martin: the two maps (network and nulls)

Martin's own folder. Each member writes only in their own folder (`Diego/`, `Martin/`, `Anas/`) and never edits or deletes another's.

Martin Møllenhus working with Claude (Anthropic's AI assistant). Claude wrote the code; every choice is
Martin's to defend. **Start here: this top part is the current state (20 Nov). Everything from "What the others
need to know" down is the 16–18 Nov record, kept for the reasons behind each choice.**

## Where things stand, 20 November

**Headline numbers (draft, not frozen; see "Still open" below):**

| What | Number | Where |
|---|---|---|
| Floor map, yields dropped (headline, G1b) | 3,573 ties, **39.2%** cross-party, party Q 0.106 | `m3_table.csv` |
| Working ties, 200 random draws of the same size (G1a) | **28.6%** (26.5% to 30.4%), Q 0.211; no draw reaches the floor | `m3_random_draws.csv` |
| Gap | **10.6 points** | |
| Floor map with yields | 4,058 ties, 35.1%, against 28.7% (26.9% to 30.7%) | `m3_table.csv` |
| Strongest working ties (second comparison, G1a) | 12.5% | `m3_table.csv` |
| Debate null (M4), headline map | Q 0.106 observed, 0.070 (0.059 to 0.079) under the null: debates explain about two thirds of the division; observed beyond all 200 | `m4_debate_null.ipynb` |
| Communities (M5) | Working map: Louvain finds the two parties (NMI with party 0.83). Floor map: 8 communities that cut across party (NMI 0.02; 0.26 for working draws of the same size) | `m5_table.csv` |
| Anas's state null, rerun on these mentions | Q 0.003 under the null (max 0.016, 50 draws) against 0.106: state explains almost none of the floor map's division. Same-state ties 9.0% against 3.7% by chance. Yes/no is Martin's | `../Anas/state_null/` |
| What the floor communities are (M5) | **Committees.** 46% of floor ties join two members of one committee, against 17.5% under rewiring (working: 22% against 18.7%); 53% of cross-party floor ties. 7 of 8 communities match a committee (Appropriations, Ways and Means, Energy and Commerce, …); the 8th is leadership | `m5_committees/` |

| Task | Files | State |
|---|---|---|
| M1 Shared name matcher | [`matcher.py`](matcher.py), [`nicknames.csv`](nicknames.csv) | 20 Nov changes (G14). Hand checks open: [`m1_checks_20nov/`](m1_checks_20nov/README.md) |
| M2 Floor mentions | [`build_mentions.py`](build_mentions.py) → [`mentions.parquet`](mentions.parquet), [`named_ties.csv`](named_ties.csv) | 8,626 mentions, 4,931 directed pairs. 18 Nov rows all kept; row numbers moved ([`row_map.csv`](m1_checks_20nov/row_map.csv)) |
| M3 Definitions | [`m3_definitions.py`](m3_definitions.py), [`m3_table.csv`](m3_table.csv), [`m3_random_draws.csv`](m3_random_draws.csv) | Decided 18 Nov (G1a–G1c), applied. Yield check not yet coded ([`m3_yield_check/`](m3_yield_check/README.md)). [`M3_PROPOSAL.md`](M3_PROPOSAL.md) is the 16 Nov proposal, partly overruled |
| M4 Debate null | [`m4_debate_null.ipynb`](m4_debate_null.ipynb) | Rerun 20 Nov on the new mentions |
| M5 Communities | [`m5_communities.py`](m5_communities.py), [`m5_table.csv`](m5_table.csv), [`m5_committees/`](m5_committees/committee_check.py) | First run 20 Nov. Choices listed at the top of each script, **not yet confirmed by Martin** |
| M6 Close-up null | | Not started: needs Anas's release-to-bill table (A3) |
| M7 Figure 1 | [`m7_figure1.py`](m7_figure1.py) → [`figures/figure1_draft.png`](figures/figure1_draft.png) | First draft |
| M8 Slides | | Not started |

**Still open before the freeze (Sun 22 Nov), Martin's:** code the three sheets in `m1_checks_20nov/` and the
yield check; confirm G14 and the M5 choices; yes or no to Anas's state null. When a hand check changes a rule,
rerun in this order: `build_mentions.py`, `m3_definitions.py`, `m4_debate_null.ipynb`, `m5_communities.py`,
`m5_committees/committee_check.py`, `m7_figure1.py`.

**What the committee result could mean for the paper (an idea, not a decision):** the floor map is less divided
than the working map, and its cross-party ties sit mostly inside committees, between members who manage the same
bills. That fits part 2 (cross-party mentions are mostly credit): crossing the aisle on the floor is largely
committee work being thanked in public. Limits: committee membership is today's
(unitedstates/congress-legislators, downloaded 20 Nov), and committee managers name each other partly because
House procedure puts them in the same debates, which the M4 null already partly holds fixed.

## What the others need to know (16–18 Nov)

1. **Diego (D2):** draw the sample with
   `python Diego/d2_labelling/draw_labelling_sample.py Martin/mentions.parquet`. `context` is the sentence
   with the name plus one sentence either side, as you asked. The median is 349 characters. Where the
   Record has no sentence break (184 of 8,092 mentions) the context is cut to 1,000 characters centred on
   the name, with … at each cut end.
2. **Anas (A3):** from `project/`, `from Martin.matcher import Matcher`; the docstring in `matcher.py`
   shows the three lines needed. It takes any text, so it runs on press releases as it is.
3. **Everyone:** `mentions.parquet` has three columns beyond the agreed seven: `how` (the rule that resolved
   the name), `is_leader_title` and `is_yield_window`. **Since 18 Nov `is_yield` is the phrase rule** (1,427 of the
   8,041 R–D mentions; the window rule flagged 1,406; they disagree on 285). Rows, their order and every other
   column are unchanged, so `mention_row` in Diego's D2 keys still points at the same mentions (checked).
   **Since 20 Nov the file has 534 more rows from the new matcher and the row numbers moved:** look up an
   18 Nov `mention_row` through [`m1_checks_20nov/row_map.csv`](m1_checks_20nov/row_map.csv). All 100 D2 rows are still there. `named_ties.csv` is directed: one row per (speaker, named).

## Choices made here

Martin confirmed all six on 16 November, after reading the numbers behind each. The group can still change
them on 18 November. Two go to that meeting as open questions: the yield rule (choice 5, part of M3) and
whether the shared files move to `scripts/` and `data/processed/` as the work plan says.

| # | Choice | Alternative and what it would change |
|---|---|---|
| 1 | Surnames are compared without case or accents | The prototype compared exactly: 18 members stored in capitals were invisible, their namesakes took their mentions, and unaccented spellings were lost |
| 2 | A name printed in capitals is dropped (93 hits) | Keeping them counts speaker headings and vote-change lines as speech (3 of the 7 errors in D1) |
| 3 | The independent (Kiley) stays in the file | The prototype dropped him. Filter on party where two sides are needed |
| 4 | Context is three sentences, from a simple splitter, cut to 1,000 characters centred on the name when longer (184 mentions) | 60 characters either side, as in the prototype: too short to label tone. Without the cap the longest context was 7,192 characters |
| 5 | **Changed 18 Nov (DECISIONS G1c):** `is_yield` is the phrase rule. The old flag, "yield" within 60 characters, is kept as `is_yield_window` | The window rule: 87% recall, 90% precision in D1. The phrase rule found 30 of 30 on the same rows, not yet tested on unseen ones |
| 6 | Everything else as in the prototype (its choices 2 to 5): House floor turns of 50 words or more, a title before the surname, shared surnames resolved by first name, then state within 80 characters, else dropped | See section 0 of `../prototype_two_maps.ipynb` |

## M3: what the group has to decide on 18 November

The full proposal, with the table and the alternatives, is in [`M3_PROPOSAL.md`](M3_PROPOSAL.md). In short:

1. **Thinning the working map:** compare the floor map with working ties drawn at random at the same size
   (29.5% cross-party), and report the strongest ties (12.6%) as a second comparison. The floor map is at
   34.2%.
2. **Yields:** keep them in the headline, show the map without them (38.6%) below.
3. **Yield rule:** replace the 60-character window with a phrase rule (30 of 30 labelled yields found, no
   false flags, against 26 of 30 and three false flags).

Under this proposal the headline gap is 5 points, small enough that matcher errors could close it. The new
matcher's precision has not been measured.

## M4: the floor map against a null that keeps the debates

**One run, 16 November 2026. Observations, not results.** Inside each debate the named ends of the mentions
are shuffled; nothing moves between debates.

| Mentions | Measure | Observed | Degree-preserving null | Debate null (smallest to largest) |
|---|---|---|---|---|
| All (8,041) | Party modularity Q | 0.156 | -0.003 | 0.077 (0.061 to 0.090) |
| | Cross-party share of ties | 34.2% | 50.1% | 42.2% (40.9% to 43.8%) |
| | Cross-party share of mentions | 36.0% | | 43.8% (42.8% to 44.9%) |
| Yields dropped (6,635) | Party modularity Q | 0.116 | -0.001 | 0.068 (0.058 to 0.083) |
| | Cross-party share of ties | 38.2% | 49.9% | 42.9% (41.4% to 43.9%) |
| | Cross-party share of mentions | 41.5% | | 45.5% (44.7% to 46.4%) |

- The debate structure explains about half of the floor map's party division: shuffled inside debates, the
  map still has Q = 0.077, against about zero for plain rewiring.
- The other half is not explained by it. The observed map is more divided than every one of the 200
  rewirings, on all three measures, with and without yields.
- It does not test the gap to the working map, which has no debates, and it says nothing about tone.

The null's choices, confirmed by Martin before the run:

| # | Choice | Alternative and what it would change |
|---|---|---|
| 1 | A debate is one Congressional Record item (`doc_id`) | All items of one day: about 39 unrelated items mixed, a null nearly as easy as plain rewiring |
| 2 | Inside a debate the named ends are shuffled. Each speaker keeps the mentions made there, each member the mentions received there | Redraw targets from those who spoke in the debate: loses the 30% of mentions that name an absent member |
| 3 | Two mentions of a debate swap their named member; a swap that makes a member name themselves is rejected. 5 swaps per mention, 200 rewirings, seed 2805 | Fewer swaps leave the null close to the data |
| 4 | Mentions in a debate with one named member (12%; 15% without yields) stay in the map, fixed | Dropping them changes the observed map too. Keeping them makes the null harder to beat |
| 5 | Measured: party modularity and cross-party share of the map, and cross-party share per mention | Per tie only, as in the prototype |
| 6 | Run on all mentions and with yields dropped | One of the two, before the group has decided whether yields count |
| 7 | Nodes are the 450 Republicans and Democrats (8,041 of the 8,092 mentions) | Keeping the independent, who has no party side |

Limits: after shuffling only about half of the mentions point at a different member, so the null is
conservative. A long debate split over several Record items counts as several debates. A rewired map does
not have exactly the observed number of ties.

## What changed against the prototype

| | Prototype (13 Nov) | This version |
|---|---|---|
| Mentions | 7,931 | 8,092 |
| Shared-surname mentions dropped | 717 | 783 |
| Printed in capitals, dropped | counted as mentions | 93 |
| Ties between Republicans and Democrats | 3,718 | 3,777 |
| Cross-party share of those ties | 34.5% | 34.2% |

More shared-surname drops is expected: Green, Turner, Scott, Grijalva and García now have a visible
namesake and go through the shared-surname rules. The 17 formerly invisible members now receive 203
mentions. **Not re-validated:** the 93% precision in D1 was measured on the prototype's matcher, not this one.

## To rerun

From `project/`, with pandas and pyarrow:

```
python Martin/matcher.py           # self-check: 20 known cases
python Martin/build_mentions.py    # writes mentions.parquet and named_ties.csv, prints the counts above
PYTHONPATH=Martin python Martin/m3_definitions.py   # the M3 table and the yield-rule test; about a quarter of an hour
```

Then run `m4_debate_null.ipynb` from this folder (it also needs networkx and matplotlib; a few minutes).

Run on 16 November with Python 3.14 and pandas 3.0.3.
