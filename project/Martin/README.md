# Martin: the two maps (name matcher, networks, nulls, Figure 1)

Martin Møllenhus's part of the project "Two maps of Congress", done with Claude (Anthropic's AI assistant; Claude
wrote the code, every choice is Martin's to defend). This folder holds **only Martin's own work**: each part, its
data, its code and what it found. The shared paper is in [`../report/`](../report/README.md); this folder explains
the pieces of it that come from Martin, so that anyone, or any teammate's Claude, can use them in the paper and
answer questions about them at the presentation.

Each member writes only in their own folder (`Diego/`, `Martin/`, `Anas/`). Every decision and its reason is in
[`../DECISIONS.md`](../DECISIONS.md) (Martin's: G1a–G1c, G14–G20); who did what and when is in
[`../WORK_AND_DEADLINES.md`](../WORK_AND_DEADLINES.md).

## The project in two sentences

We draw the 119th US House twice on the same 450 Republicans and Democrats: a **working map** (A is tied to B when
A cosponsors B's bill) and a **floor map** (A is tied to B when A names B in a floor speech), and ask whether the
floor map is less divided by party. It is: 38.7% of floor ties cross the aisle, against 28.6% of working ties
drawn at random at the same size, and that part (part 1 of Results, Figure 1, and the Methods for data, matching
and networks) is Martin's.

## Martin's text in the paper (final versions)

| Text | Source here | In the paper |
|---|---|---|
| Results part 1, "the two maps", and the Figure 1 caption | [`results_part1.md`](results_part1.md) | `report/sections/from_martin_results.tex`, `from_martin_caption1.tex` |
| The M6 paragraph for Anas's part 3 | [`results_part1.md`](results_part1.md), last section | `report/sections/from_martin_m6.tex` |
| Methods: data, name matching, yields, the two maps, nulls, communities | [`methods_networks.md`](methods_networks.md) | `report/sections/from_martin_methods.tex` |
| Figure 1 | [`figures/figure1.pdf`](figures/figure1.pdf), made by [`m7_figure1.py`](m7_figure1.py) | `report/figures/figure1.pdf` |

The `.tex` files are generated from the two markdown files by `python report/md2tex.py` (run from `project/`;
checked 25 Nov: the generated files match). Edit the markdown, not the `.tex`. Square brackets in the markdown name
the source of each number and are dropped in the paper. Each markdown file ends with "Notes for us (not for the
paper)": the limits to say out loud and what was cut.

## The headline numbers (frozen 22 Nov, after G19)

| What | Number | File |
|---|---|---|
| Floor map, yields dropped (headline) | 3,970 ties from 8,469 mentions, **38.7%** cross-party, party modularity Q 0.112 | `m3_table.csv` |
| Working map, 200 random draws of 3,970 ties | **28.6%** (26.8% to 30.6%), Q 0.211 (0.193 to 0.230); no draw reaches the floor map | `m3_random_draws.csv` |
| Gap | **10.1 points** | |
| Floor map with yields kept | 4,423 ties, 35.2%, against 28.7% (26.9% to 30.3%) | `m3_table.csv` |
| Strongest 3,970 working ties | 12.8% | `m3_table.csv` |
| Full working map | 46,513 ties, 28.7%, Q 0.210 | `m3_table.csv` |
| Degree-preserving rewiring (both maps) | about 50% cross-party, Q about 0 | `m3_table.csv`, `m4_results.csv` |
| Debate null (M4), headline map | Q 0.074 (0.065 to 0.082) against 0.112: debates explain about two thirds of the division; observed beyond all 200 | `m4_results.csv` |
| State null (G16) | Q 0.001 (at most 0.023) against 0.112: state explains almost none | `m3b_state_null.csv` |
| Communities (M5) | Working map: the two parties (NMI with party 0.83). Floor map: 8 communities across party (NMI 0.03; 0.29 for working draws of the same size) | `m5_table.csv` |
| What the floor communities are | Committees: 44% of floor ties join two members of one committee, against 17.1% under rewiring (working map 22% against 18.7%); 50% of cross-party floor ties | `m5_committees/committee_table.csv` |
| Close-up null (M6) | Cross-party sponsored bills announced in press releases 52.7% against 45.1% (p < 0.001); against same-party co-led bills only 52.6% against 49.1% (p 0.02) | `m6_results.csv` |
| Matcher checks | Precision 98 of 100 (Diego's D2 sample); recall 12 of 13 (92%, 67% to 99%); untitled names 30 of 30; list hits 20 of 20; yield rule 15 of 15 | `m1_checks_20nov/`, `m3_yield_check/` |

## The parts, in the order they were done

| Part | Question it answers | Main result | Where |
|---|---|---|---|
| **M1** Shared name matcher | Which member does "Mr. Cole" in a speech or press release mean? | One rule-based matcher used by floor and press; checked by hand (above) | [`matcher.py`](matcher.py), [`nicknames.csv`](nicknames.csv), [`m1_checks_20nov/`](m1_checks_20nov/README.md) |
| **M2** Floor mentions | Who names whom on the floor? | 9,988 mentions, 5,400 directed pairs | [`build_mentions.py`](build_mentions.py) → [`mentions.parquet`](mentions.parquet), [`named_ties.csv`](named_ties.csv) |
| **M3** Definitions | How are the two maps made comparable, and do yields count? | Random working draws at the floor map's size as headline; yields dropped by a phrase rule | [`m3_definitions.py`](m3_definitions.py), [`m3_table.csv`](m3_table.csv), [`m3_random_draws.csv`](m3_random_draws.csv), [`m3_yield_check/`](m3_yield_check/README.md); [`M3_PROPOSAL.md`](M3_PROPOSAL.md) is the 16 Nov proposal, partly overruled on 18 Nov |
| **M3b** State null | Is the division just geography? | No (Q 0.001 against 0.112) | [`m3b_state_null.py`](m3b_state_null.py), [`m3b_state_null.csv`](m3b_state_null.csv) |
| **M4** Debate null | Is the floor map divided only because debates have casts? | Two thirds of it, yes; the rest is beyond every shuffle | [`m4_debate_null.ipynb`](m4_debate_null.ipynb), [`m4_results.csv`](m4_results.csv), [`figures/m4_debate_null.png`](figures/m4_debate_null.png) |
| **M5** Communities | What groups does each map fall into? | Working: parties. Floor: committees | [`m5_communities.py`](m5_communities.py), [`m5_communities.csv`](m5_communities.csv), [`m5_table.csv`](m5_table.csv), [`m5_committees/`](m5_committees/committee_check.py) |
| **M6** Close-up null | Do members announce their cross-party bills more than their other bills? | A little, mostly because co-led bills are announced more | [`m6_closeup_null.py`](m6_closeup_null.py), [`m6_results.csv`](m6_results.csv) |
| **M7** Figure 1 and Results part 1 | | Four panels: maps A–B, cross-party share C, modularity against all nulls D | [`m7_figure1.py`](m7_figure1.py), [`figures/`](figures/), [`results_part1.md`](results_part1.md) |
| **Delegation check** (25 Nov, post-hoc, G23) | Do exposed members name the other party at home only because their state delegation is mixed? | No: shuffling exposure within party and band of the delegation's other-party share leaves the whole gap (p < 0.01); for Democrats about 1.1 of the 2.6 points are names of home-state Republicans | [`delegation_check/`](delegation_check/PLAN.md) (plan written before running, `delegation_check.py`, `results.csv`, `readout.txt`) |
| **Methods** | Enough to redo part 1 | About 620 words | [`methods_networks.md`](methods_networks.md) |

M8 (the three slides) is in `../report/slides/`, shared. The near-final paper is in
[`../report/final_report/`](../report/final_report/) (moved there from this folder on 26 Nov; it is the group's paper).

## Each part in plain words, with what to say if asked

**M1, the matcher.** Code that finds members' names in text. It reads a House title before a surname ("Mr. Cole",
"Chairman Cole", "Speaker Johnson"), lists after a plural title ("Representatives Lawler, Golden, and
Fitzpatrick"), and full names without a title ("my friend, Chip Roy"). A shared surname is settled by first name
(official or nickname), then by a state name within 80 characters, else dropped. Possessives ("Mr. Cole's
amendment") and middle initials are read through; names after "Senator", "Governor", "State" and similar are
skipped; a member naming themselves does not count. Surnames are compared without case or accents (the prototype
missed 18 members stored in capitals and every accented name); names printed in capitals are dropped, because they
are speaker headings and vote-change lines, not speech. *If asked "how do you know the names are right?":* Diego
read 100 random mentions (98 right); Martin read 30 random turns and the matcher found 12 of the 13 members a
reader found (the miss is a shared surname with nothing nearby to settle it); each new name form was checked
separately (untitled 30 of 30, lists 20 of 20) by a rule fixed before coding (G14, G19). Anas uses the same matcher
on press releases (`from Martin.matcher import Matcher`).

**M2, floor mentions.** The Congressional Record, 6 Jan 2025 to 9 Nov 2026, split into speaker turns; House-floor
turns of at least 50 words spoken by a member (17,824). One row of `mentions.parquet` is one name found in one turn:
`speaker`, `named` (Bioguide IDs), `source`, `date`, `doc_id` (the Record item, used as "a debate"), `context`
(the sentence with the name and one either side, at most 1,000 characters), `is_yield`, plus `how` (the rule
that found it), `is_leader_title` and `is_yield_window` (the old yield rule). `named_ties.csv` has one row per
directed (speaker, named) pair. 18 Nov row numbers map to today's through `m1_checks_20nov/row_map.csv`.

**M3, definitions.** Two choices make the maps comparable. *Thinning (G1a):* the working map has 46,513 ties, the
floor map 3,970, and a sparse map can look different just by being sparse, so the floor map is compared with 200
random draws of 3,970 working ties; the 3,970 strongest working ties (pairs sharing the most bills) are a second
comparison and are far more partisan (12.8%). *Yields (G1b, G1c):* "I yield two minutes to the gentleman from
Texas" is procedure, not a choice to name someone, so yields are left out of the headline. A mention is a yield
when "yield" (not "yield back") comes before the name in the same sentence, or "for yielding" after it. On the 30
mentions where this rule and the older 60-character window disagreed, Martin found all 15 that only the phrase rule
flagged were yields, and 14 of the 15 that only the window flagged were not. *If asked "does dropping yields make
the gap?":* no, with yields kept it is 35.2% against 28.7%.

**M3b and M4, the nulls.** *Degree-preserving rewiring* (double-edge swaps, five per tie) keeps how many ties each
member has: then about half of ties cross the aisle and Q is about zero, so both maps are far more divided than
chance. *The debate null* shuffles, within each Record item, which member is named, so each speaker keeps the
mentions they made there and each member the mentions they received there: Q falls from 0.112 to 0.074, so debate
structure (a manager from each party, a cast per bill) explains about two thirds of the floor map's division, and
members still name their own side more than all 200 shuffles. *The state null* (Anas's proposal, G16) also keeps
each member's number of same-state ties: Q 0.001, so state delegations are not the explanation. Seed 2805
throughout; 200 draws each (20 for the full working map, which is slow).

**M5, communities.** Louvain (the course's method, week 4), resolution 1, 50 random starts, best partition kept,
compared with party by normalised mutual information (G15). The working map splits into the two parties; the floor
map into 8 communities of 28 to 80 members that each hold both parties. Joined with today's House committee lists
(unitedstates/congress-legislators): in 7 of the 8, one committee is 3.0 to 7.9 times as common as in the House
(Appropriations 82% of members, Ways and Means 79%, Energy and Commerce 67%, …); the 8th holds the party leaders.
*If asked what it means:* crossing the aisle on the floor is largely committee work named in public, which fits
part 2 (cross-party mentions are mostly credit). *Limits:* committee lists are today's, not the start of the term;
committee managers share debates, which the debate null holds fixed but not the committee.

**M6, close-up null (for part 3).** Of each member's own sponsored House bills and joint resolutions, a bill is
cross-party if an original cosponsor is from the other party, and announced if it is cited in the member's press
releases (Anas's A3.5 table). The null shuffles, within each member, which bills are cross-party (10,000 shuffles),
so members who announce everything do not dominate (G20).

| Check | Members | Bills | Announced: cross-party | Announced: other | Observed / null | p (one-sided) |
|---|---|---|---|---|---|---|
| **Main:** sponsored bills | 388 | 10,125 | **52.7%** | **45.1%** | 1.08 | < 0.001 |
| Republicans only | 201 | 5,489 | 54.8% | 45.7% | 1.09 | < 0.001 |
| Democrats only | 187 | 4,636 | 50.2% | 44.5% | 1.06 | < 0.001 |
| **Co-led bills only** (against same-party co-leads) | 368 | 6,736 | **52.6%** | **49.1%** | 1.02 | 0.023 |
| Cited by bill number only | 388 | 10,125 | 17.6% | 15.2% | 1.12 | < 0.001 |
| Cross-party = any cosponsor of the other party | 392 | 10,218 | 52.8% | 44.6% | 1.08 | < 0.001 |
| All four House bill types | 393 | 11,811 | 46.3% | 40.1% | 1.07 | < 0.001 |
| Bills the member was an original cosponsor of | 410 | 51,641 | 8.6% | 2.9% | 1.33 | < 0.001 |

*The honest reading:* most of the gap separates co-led bills from solo bills; the other party adds 3.5 points.
*Main limit:* no control for whether a bill moved (our data has no bill status), and bipartisan bills may pass more.

**M7, Figure 1.** (A) the floor map, (B) one random draw of the working map at the same size, (C) the share of
ties that cross the aisle, with the range over 200 draws and the rewiring level, (D) party modularity of each map
against its nulls. Full PNAS width (17.8 cm); rebuilt from the result files by `m7_figure1.py`, which also checks
that no labels overlap. `m7_figure1.py --side` writes `figures/figure1_side.pdf`, the 11.4 cm side-caption version
used in the near-final paper; the full-width file stays for the slides.

## Choices made here and why (the full record is in DECISIONS)

| Choice | Alternative and what it would change |
|---|---|
| Surnames compared without case or accents | Exact comparison: 18 members invisible, their namesakes take their mentions |
| Names printed in capitals dropped (93 hits) | Counts speaker headings and vote-change lines as speech |
| The one independent (Kiley) kept in `mentions.parquet`, left out of the two-party maps | Dropping him loses his mentions for anyone using the file |
| Context = three sentences, cut to 1,000 characters | 60 characters either side, as in the prototype: too short to label tone (Diego's D2) |
| Shared surname with no first name or state nearby: dropped (828 titled names) | Guessing would add cross-party errors |
| Maps undirected and unweighted | Weighted ties: one pair named fifty times would dominate; the reason the thinning is random (G1a) |
| A debate = one Record item (`doc_id`) | All items of one day: about 39 unrelated items mixed, a null nearly as easy as plain rewiring |
| Debate null swaps named members within a debate; self-mentions rejected; single-name debates kept fixed | Redrawing from the debate's speakers loses the 30% of mentions naming an absent member |
| Louvain with 50 starts, best kept | One run is random; a forced two-way split would hide the committees |
| M6: own bills = sponsored; within-member shuffle | Original-cosponsored bills as the main unit (ratio 1.33, but the bills are someone else's); a pooled comparison |

## To rerun

From `project/`, with pandas, pyarrow, networkx and matplotlib. If a matcher rule changes, rerun in this order:

```
python Martin/matcher.py                          # self-check on known cases
python Martin/build_mentions.py                   # mentions.parquet, named_ties.csv
PYTHONPATH=Martin python Martin/m3_definitions.py # M3 table; about a quarter of an hour
# Martin/m4_debate_null.ipynb (run from Martin/; a few minutes)
python Martin/m3b_state_null.py
python Martin/m5_communities.py
python Martin/m5_committees/committee_check.py
python Martin/m6_closeup_null.py
python Martin/m7_figure1.py
python Martin/m1_checks_20nov/score_checks.py     # scores the coded hand-check sheets
python report/md2tex.py                           # regenerates Martin's sections of the paper
```

Run with Python 3.14 and pandas 3.0.3.
