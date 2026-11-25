# Anas: the close-up at home (press releases, exposed seats, the home map, "bipartisan")

Anas Mir's part of the project "Two maps of Congress", done with Claude (Anthropic's AI assistant; Claude wrote the
code, every choice is Anas's to defend). This folder holds **only Anas's own work**: each part, its data, its code
and what it found. The shared paper is in [`../report/`](../report/README.md); this folder explains the pieces of it
that come from Anas, so that anyone, or any teammate's Claude, can use them in the paper and answer questions about
them at the presentation.

Each member writes only in their own folder (`Diego/`, `Martin/`, `Anas/`). Every decision and its reason is in
[`../DECISIONS.md`](../DECISIONS.md) (Anas's: G13, the swing seat and window, agreed by all three; G14, G16 and G18 came from Anas's proposals); who did what and when
is in [`../WORK_AND_DEADLINES.md`](../WORK_AND_DEADLINES.md).

**Cleaned up on 25 Nov 2026**, after the group accepted the home map and A5 into the paper and closed the analysis
(no new analyses from here on). Everything below is the final state. What was removed and how to get it back is at
the bottom.

## The project in two sentences, and part 3 in two more

We draw the 119th US House twice on the same members: a **working map** (A is tied to B when A cosponsors B's bill)
and a **floor map** (A is tied to B when A names B in a floor speech), and find the floor map less divided by party
(Martin's part 1; Diego's part 2 says what a named colleague means).

Part 3 asks the same question one step closer to voters: **whom do members name in their own press releases, and do
members whose seat is at risk name the other party more?** They do, in both parties; most of those names are
partners; the gap cannot be separated from the members' ideology; and the network of who names whom, and the word
"bipartisan", show the two parties doing it in different ways.

## Anas's text in the paper (final versions)

| Text | Source here | In the paper |
|---|---|---|
| Results part 3, "Close-up: whom members name at home" (about 930 words, six paragraphs) | [`results_part3.tex`](results_part3.tex) | `report/sections/results_part3.tex`, loaded in `results.tex` (Martin's M6 paragraph follows it) |
| Figure 3 | [`a4/out/figure3.pdf`](a4/out/figure3.pdf), made by [`a4/figure3_column.py`](a4/figure3_column.py) | `report/figures/figure3.pdf` (identical) |
| Figure 3 caption | [`figure3_caption.tex`](figure3_caption.tex) | inside `report/sections/results.tex` (identical) |
| Methods: press releases, names and bills, exposure and tests, the two checks, "bipartisan" | [`methods_press.tex`](methods_press.tex) | `report/sections/methods_press.tex`, loaded in `methods.tex` |
| References added by Anas | | `report/references.bib`: `holm1979`, `wilson1927`, `cohen1960`, `cook2025pvi`, `wikipedia2025pvi`, `downballot2024` |

The `report/` copies are the same files. Edit here and copy over, or edit `report/` once the paper has moved to
Overleaf; say which in the log. Each `.tex` file starts with `%` comment lines naming the result file behind every
number.

## The headline numbers (frozen 22 Nov, after the rerun on Martin's G18 matcher)

Inputs frozen by checksum at repo commit `bc1c2344` ([`a3/out/inputs.json`](a3/out/inputs.json)). Seed 2805
throughout.

| What | Number | File |
|---|---|---|
| Press releases collected | **55,023** from 412 members, 3 Jan 2025 to 20 Nov 2026 | [`press_releases/MANIFEST.md`](press_releases/MANIFEST.md) |
| In the test | **406 members** with ≥ 10 releases (37 exposed and 171 safe Republicans, 54 exposed and 144 safe Democrats), 53,664 releases | `a4/out/member_shares.csv` |
| Press mentions (matcher + press layer) | 129,473 (release, member) pairs; 14.4% cross-party | `a3/out/mentions_press.parquet` |
| Matcher on press, 40 releases read by 5 blind AI readers | recall **0.97**, precision **0.96** (floor matcher alone 0.75 and 0.95) | `a3/recall_check/` |
| Bill links | 18,177 in 13,944 releases (25%); 30 of 30 right by number, 30 of 30 by title | `a3/out/release_bills.csv`, `a3/bill_check/` |
| **Main result:** share of releases naming the other party (not a co-lead, not a leader) | Republicans exposed **13.3%** against safe **9.2%** (+4.1, p 0.004); Democrats **11.6%** against **9.0%** (+2.6, p 0.004); interaction +1.5 (p 0.36) | `a4/out/results.csv` |
| Closest seats | Crossover seats: R 19.2% (8 members), D 14.2% (10); beyond 5 points of lean 7.9% to 10.1% | `a4/out/member_shares.csv`, Figure 3A |
| Robustness | All 8 checks fixed in advance: positive gap in both parties, every p < 0.05; leave-one-state-out R +3.6 to +4.9, D +2.1 to +3.1 | `a4/out/results.csv`, `leave_one_state_out.csv` |
| Check T: what the names do | 60 names, 3 blind readers: **46 partner or praise (77%, 65–86%)**, 9 neutral, 4 wrong match, 1 criticism | `a4/check_tone/scored.csv` |
| Check I: ideology | Gap ideology alone gives: R 2.9 of 4.1 points, D 2.4 of 2.6; remainder R 1.1 (p 0.39), D 0.2 (p 0.76) | `a4/out/ideology_check.csv` |
| Home map: hubs | Exposed members are 22% of members, send 35% and receive 34% of cross-party ties; cross-party ties per member R 54 against 28 (×1.9), D 46 against 30 (×1.5), Holm p 0.001 each | `a4/out/home_ties.csv`, `a4/out/home_measures_centrality.csv` |
| Home map: backbone | Exposed R 1.5× backbone ties (Holm p 0.013), betweenness ×1.8 and closeness borderline (Holm 0.059, 0.055); exposed D brokering given ties Holm 0.08 at α 0.01, < 0.05 from α 0.02 up | `a4/out/home_measures_centrality.csv`, `alpha_centrality.csv` |
| Home map: exposed with exposed | 10.7% of cross-party ties against 10.2% (9.8–10.6) under rewiring, p 0.015 | `a4/out/home_measures_null.csv` |
| A5: "bipartisan" | 13,744 releases (25.6%) say it; a House partner of the other party in **63.9%** of them against 8.6% of others (370 members, p < 0.001) | `a5/out/results.csv` |
| A5 by seat | D exposed 63.0% against safe 56.7% (p 0.012); R 72.1% against 69.1% (p 0.40) | `a5/out/results.csv` |
| A5 checks | 30 with a named member: 28 partners, 0 opponents; 30 without: 29 name no partner | `a5/mirror/scored.csv`, `a5/check/scored.csv` |

## How part 3 reads: one aim, four layers that do not fully agree

Part 3 is written as one story with the disagreements kept, because they are where the result is interesting.

1. **The text count** finds the same gap in both parties, too close to tell apart (interaction p 0.36): a seat
   effect, not a president's-party effect, by the reading fixed in advance.
2. **The ideology check** says that seat and ideology cannot be separated: exposed members are mostly their party's
   moderates. More of the Republican gap than of the Democratic gap is left after ideology (1.1 of 4.1 against 0.2
   of 2.6), a first hint that the parties differ.
3. **The home map** splits the one gap into two roles: exposed Republicans bridge **by volume** (more backbone
   ties), exposed Democrats **by position** (more shortest paths than their ties predict). We did not test why.
4. **A5** turns it around again: exposed Democrats back the word "bipartisan" with a partner more often than safe
   Democrats, while among Republicans exposed and safe do not differ (and both are above Democrats, not tested).

So the party difference that the text count cannot see turns up in the network and in A5, in different places.
None of it is causal: "consistent with", never "because".

## The parts, in the order they were done

| Part | Question it answers | Main result | Where |
|---|---|---|---|
| **Scope scan** (18 Nov) | How many releases has each member posted, and can they be collected? | ~410 countable members; collect everyone, not a sample | [`press_scope/`](press_scope/README.md) |
| **District lean** (19–20 Nov) | Which seats are exposed, given that nine states redrew for 2026? | Lean of the district each member *served*; second source r 0.999 | [`district_lean/`](district_lean/README.md) |
| **A1, A2** Collector and collection | All press releases, with full text and date | 55,023 releases, 412 of 413 countable members, audited against outside counts | [`collector/`](collector/README.md), [`press_releases/`](press_releases/MANIFEST.md) |
| **A3** Names and bills | Whom does each release name, and which bills does it cite? | Martin's matcher plus a thin press layer: recall 0.97, precision 0.96; 18,177 bill links | [`a3/`](a3/README.md), plan [`A3_PLAN.md`](A3_PLAN.md), switch [`A3_MATCHER_SWITCH.md`](A3_MATCHER_SWITCH.md) |
| **A4** The test and Figure 3 | Do exposed members name the other party more? | Yes, in both parties, mostly in the closest seats | [`a4/`](a4/README.md) (`analysis.py`, `figure_lean.py`, `figure3_column.py`) |
| **Check T** | Are the counted names partners or attacks? | 77% partners or praise, 1 of 60 criticism | `a4/make_tone.py`, `a4/score_tone.py`, `a4/check_tone/` |
| **Check I** | Is "exposed" just "moderate"? | Cannot be separated | `a4/ideology_check.py` |
| **Home map** | Who names whom: where do exposed members sit in the network? | Hubs in both parties; bridge by volume (R) and by position (D) | `a4/home_network.py`, `home_measures.py`, `alpha_*.py`, `figure_home_map.py`, [`a4/NETWORK_METHODS.md`](a4/NETWORK_METHODS.md) |
| **A5** "Bipartisan" | Does a release that says "bipartisan" name a real partner? | Two times in three; a seat difference among Democrats only | [`a5/`](a5/README.md) |
| **A6** Methods | Enough to redo part 3 | About 490 words with Martin's M6 sentence | [`methods_press.tex`](methods_press.tex); outside-course methods argued in [`../OFF_CURRICULUM.md`](../OFF_CURRICULUM.md) |
| **Rerun** (22 Nov) | Does anything change on Martin's G18 matcher? | Every reading holds; R closeness no longer passes Holm | [`RERUN_22NOV.md`](RERUN_22NOV.md) |

## Each part in plain words, with what to say if asked

**The collection (A1, A2).** A collector visits every member's `house.gov` press listing (allowed by each site's
`robots.txt`), follows it back to 3 January 2025, and stores each release's full text and date. 55,023 releases from
412 members, snapshot of 20 November 2026. Not collected: four sites whose listing loads only with JavaScript or is
gone, Jim Jordan (listing ends in 2024) and the 12 who left office. *If asked "how do you know it is complete?":*
the first version reported members as complete that were not (Jeffries 10 of 709 releases); an outside count caught
it. Every fix was tested on all members, the final table is one run of the final code, and 37 members whose sites
have the WordPress API were compared with it (26 equal, every other difference explained). Files over GitHub's
limit are split into three parts by member; `MANIFEST.md` shows how to load them.

**Exposed seats (`district_lean/`).** A member is *exposed* when the district they served leans toward their own
party by 5 points or less (Cook PVI 2025), which includes seats leaning to the other party; the rest are *safe*.
Nine states redrew their maps for 2026, so we use the district the member **served**, not the 2026 one: the
releases were written for its voters (Cohen's TN-9 is D+23 as served, R+9 on the new map). The lean comes from a
pinned Wikipedia revision of 25 May 2025, before any redraw, and agrees with the 2024 presidential margin from The
Downballot at r 0.999. *If asked "why not the member's own vote share?":* it is partly caused by what members do at
home, press releases included; presidential votes in the district are not.

**Names and bills (A3).** The same matcher as the floor (Martin's M1), run on releases with two inputs switched on
(untitled full names, the first names members use for themselves) and a thin press layer: party-state tags ("Rep.
Smith (R-NE)"), lists across tags, quoted nicknames, middle initials, and guards against state legislators. Every
hit says which rule found it, so the floor-only version stays visible. Bills are linked by number or by an official
title that belongs to one bill only; a **co-lead** is the bill's sponsor or an original cosponsor. *If asked "how
do you know the names are right?":* 40 releases drawn without using the matcher were read by five blind AI readers
(Claude), who listed every House member named and agreed on all 77; Anas read the 7 cases where readers and matcher
differed and agreed with the readers each time. The matcher found 75 of 77 (recall 0.97) with 3 wrong (precision
0.96). This check found the middle-initial bug ("Congressman Riley M. Moore" read as Josh Riley), which was then
fixed for floor and press alike (G18).

**The test (A4).** For each member, the share of their releases that name a House member of the other party who is
neither a party leader nor a co-lead of a bill the release cites (a co-lead is named because of the bill, not by
choice). Exposed against safe within each party, by shuffling the exposed label among the party's members (10,000
shuffles); the difference between the two parties' gaps is the interaction. The plan, the outcome and how each
result would be read were written on 20 Nov before any release was analysed (`methods_drafts.md`). *If asked "is
it just the cut-off?":* every check fixed in advance holds (cut-off 4 or 6, the presidential margin as lean,
without the 21 members relabelled by the new maps, without releases about redistricting or caucuses, with co-leads,
the floor matcher alone, any one state left out). The cut-off changes how big the gap is, not which way it points,
because the gap sits in the closest and crossover seats (Figure 3A).

**Check T, what the names do.** A count of names says nothing about tone. 60 of exactly the names A4 counts, 15 per
party and seat, were coded by three blind AI readers who did not see the seat: 46 partner or praise, 9 neutral (a
committee chair addressed in a letter), 4 wrong matches, 1 criticism (a safe Republican on a Democrat's remarks).
They agreed on 56; Anas read the other four. *What to say:* at home, as on the floor (Diego's 69%), cross-party
names are mostly acknowledgement, so "name" in the paper means mostly "partner", and exposed and safe seats do not
differ in criticism.

**Check I, ideology.** Exposed members are also their party's moderates (DW-NOMINATE, first dimension, from
Voteview): 22 of 37 exposed Republicans and 27 of 54 exposed Democrats are in their party's most moderate fifth. The
exposed label was shuffled only among members of the same party and ideology band; that leaves 1.1 (R) and 0.2 (D)
points of the gap, not distinguishable from chance. *If asked "so it is ideology, not the seat?":* no. NOMINATE is
built from roll-call votes, and members may vote moderately *because* their seat is close, so holding it fixed can
remove part of a real seat effect. The honest statement is that seat and ideology go together and this design
cannot say which drives the naming. The Discussion names it as a limitation.

**The home map.** Each of the 406 members is a node; two members are tied when one named the other in a release
(co-leads kept: a named partner is a tie; leaders left out as the named member). Cross-party: 6,765 ties, 2,060 of
them mutual. The *backbone* keeps each member's strongest ties with the disparity filter (week 4) at α 0.01, the
strictest level that keeps all 406 connected (1,656 of 29,210 weighted ties). Exposed and safe members are compared
on ten measures (five measures × two parties) with the same within-party shuffle and **Holm's correction**, which
keeps the chance of any false positive among the ten at 5%. *What holds:* exposed members have far more cross-party
ties in both parties, and exposed Republicans more backbone ties. *What is borderline:* Republican betweenness and
closeness (Holm 0.059, 0.055) and the Democrats' brokering given their ties (0.08 at α 0.01, below 0.05 at every α
from 0.02 to 0.2). The text reports these as the twist, with their Holm values. Ties between two exposed members
are compared with a rewiring that keeps every member's number of cross-party ties: 10.7% against 10.2%, a real but
small preference. *If asked why Holm, which the course does not teach:* see `../OFF_CURRICULUM.md` (without it all five
raw p < 0.05 would have been reported).

**A5, "bipartisan".** A release *says* "bipartisan" when the word appears outside sentences the member repeats in
every release; it *has a partner* when it names a House member of the other party (not a leader) or cites a bill
with one as co-lead. Means over the 370 members with at least five such releases; p from flipping the sign of each
member's difference. Two checks by three blind AI readers, each rule fixed first ([`a5/PLAN.md`](a5/PLAN.md)): of 30
releases with a named member of the other party, 28 name a partner and none an opponent (rule: 27 or more); of 30
partner-less releases, 29 really name no partner (one names a senator, whom the matcher does not count). Anas read
the 2 disagreements and the 2 close calls that decided the rule. *What to say:* at home the word mostly comes with
a named partner (Westwood 2022 found floor "bipartisan" talk unrelated to bipartisan votes; the Discussion makes
the comparison); the third without a partner uses it for a bill, a vote or past funding.

## Found, but not in the paper text (for deciding the split)

All of this is documented and checked; none of it is in `results_part3.tex` now.

- **A community of close-seat members.** Louvain on the full weighted home map (best of 50 seeds): 11 communities,
  NMI with party 0.20 (the working map's is 0.83). Two party cores (120 members, 112 R; 95, 89 D), and one
  35-member bipartisan community of which **19 are exposed** (17 R, 18 D; mostly New York and Michigan: Bacon,
  LaLota, Gillen, Scholten, Golden, Josh Riley, Kaptur, Cuellar, Mannion). The other mixed communities are state or
  regional delegations. `a4/out/home_measures_communities.csv`, `home_communities_members.csv`.
- **Exposed members sit in more mixed communities:** 37% (R) and 39% (D) of their community is the other party,
  against 26% for safe members (p 0.012, 0.002). `a4/out/home_measures_community_position.csv`.
- **Mutual naming** between two exposed members is more common (62% against 45%), but fades with stricter tie rules
  and co-leads left out: suggestive only. **Same-state ties:** safe members' cross-party ties are no more local than
  exposed members' (11.1% against 10.7%, p 0.79). `a4/out/home_network.csv`.
- **Lean as a straight line:** R −0.24 and D −0.14 points per point of lean (p 0.003, < 0.001), but the picture is
  a peak in the closest seats, not a line. `a4/out/lean_slope.csv`, `a4/out/figure_lean.png`.
- **The one hint of a president's-party effect:** at cut-off 4 the interaction is +3.6 points, p 0.051. A hint,
  not a finding.
- **Named examples:** the three mutual pairs hold (Golden–Fitzpatrick, Kaptur–Fitzpatrick, Golden–Lawler); the
  pilot's Lawler (1 of 10) and Bacon (8 of 10) figures do not (19.8% and 32.5% of all their releases).
  `a3/out/named_examples.csv`.
- **A5 in parts:** named in the release 53.4% against 4.3%; on record through a cited bill 36.9% against 5.3%.
- **The home-map figure and table, ready if wanted:** `a4/out/figure_home_map.png` (ForceAtlas2 layout on the
  backbone; purple ties across the aisle, darker the more exposed ends; panel B the cross-party ties per member) and
  `a4/out/table_home_measures.tex` (every measure, with the α at which it passes Holm). The caption draft is in
  `a4/README.md`. The paper has three figures now, so this one is for the slides or an appendix unless the split
  makes room.
- **Not done, and will not be** (analysis closed 25 Nov): the committee test of why the parties bridge differently
  (the text says "we did not test why"), and the before/after check on the redrawn states (check 3, dropped under
  G17).

## Choices made here and why

| Choice | Alternative and what it would change |
|---|---|
| Collect every countable member (412), not a sample | A sample of ~60: sampling choices to defend, too few exposed members per party |
| Snapshot 20 Nov 2026, never patched by hand | A later download: windows differ between parts; a fix would be a full rerun, logged |
| Lean of the district **served** (`lean_2025`) | The 2026 map: 12 members change label and 9 are unknown; the lean would describe voters they never had |
| Exposed = own-party lean ≤ 5, crossover seats included | Cut-off 4 or 6, or the presidential margin: same direction, different size (robustness rows) |
| Outcome leaves out co-leads and party leaders | Counting them: gaps grow to 7.0 and 6.3, but measure bills and leadership, not choice |
| Members with ≥ 10 releases (406) | Fewer releases: shares from a handful of releases are mostly noise |
| Shuffle within party | Across parties: party differences in posting and naming would enter the null |
| One shared matcher plus a separate press layer | A press-only matcher: floor and press would no longer be comparable |
| Each name in a release weighs 1/n on the home map | Plain counts: one 40-name signatory list would outweigh 39 releases (14.4% cross-party plain, 33.0% weighted) |
| Backbone at α 0.01, the strictest that keeps all 406 connected | Looser α: every comparison points the same way; the borderline ones pass Holm from 0.02 up (`alpha_centrality.csv`) |
| Holm over the ten network comparisons | Raw p: five "significant" results instead of three |
| Blind AI readers, Anas reads every disagreement and the close calls that decide a rule | Hand-reading everything: too slow for six checks; the readers are one model family, so they show stability, not truth, which is why a human reads every split |
| Designs written before running (A4 plan, home map, T and I, A5) | Choices after seeing results: the paper could not say "fixed before the analysis" |

## Contributions to the other parts

| What | For | Where |
|---|---|---|
| Matcher checklist: 15 items with evidence (nicknames, lists, untitled names, state legislators, possessives, middle initials, ...) | Part 1, Martin's matcher: G14 and G18 | [`MATCHER_CHECKLIST.md`](MATCHER_CHECKLIST.md), scripts in [`matcher_check/`](matcher_check/) |
| State null: shuffles ties within states | Part 1: Martin's M3b, G16 (state explains almost none of the division) | [`state_null/`](state_null/README.md) |
| Second coder for Diego's D2 rows 76 to 100 | Part 2 (S1) | `../Diego/d2_labelling/sheets/` |
| Release-to-bill table | Martin's M6 close-up null (reads `a3/out/release_bills.csv` and `press_releases/`) | [`a3/`](a3/README.md) |
| Swing-seat definition and window | `DECISIONS.md` G13 (agreed by Martin and Diego; entered 25 Nov) | [`../DECISIONS.md`](../DECISIONS.md) |
| The project's glossary (moved to the project folder 25 Nov) | Everyone | [`../DICTIONARY.md`](../DICTIONARY.md) |

## Files that are not obvious

- **Plans written before the results** (kept as the record that the paper's "fixed in advance" rests on):
  [`methods_drafts.md`](methods_drafts.md) (the A4 analysis plan of 20 Nov, the planned checks, data sources; its
  draft Methods sentences are superseded by `methods_press.tex`), [`A3_PLAN.md`](A3_PLAN.md),
  [`a4/HOME_NETWORK_PLAN.md`](a4/HOME_NETWORK_PLAN.md), [`a4/CHECKS_PLAN_23NOV.md`](a4/CHECKS_PLAN_23NOV.md),
  [`a5/PLAN.md`](a5/PLAN.md).
- **Reader checks, two layouts.**
  - `a4/check_tone/`, `a5/check/`, `a5/mirror/`: `packet/` (exactly what the blind readers saw), `readers/` (their
    answers), `scored.csv`, `DIFFERENCES.md` (the disagreements, with Anas's ticks) and `anas_codes.csv`.
  - `a3/recall_check/`, `a3/bill_check/`, `a3/precision_check/` (the earlier A3 checks): `raters/` (the readers'
    answers), the items they saw (`reader_items.txt` or the `.xlsx` sheets), `recall_scored.csv` or
    `bill_check_scored.csv`; the recall check's disagreements with Anas's ticks are in `recall_check/DIFFERENCES.md`.
    `precision_check/switch_sheet.xlsx` was left unread by decision (21 Nov; the recall check measured the same thing).
- **`a3/out/mentions_press.parquet`:** one row per (release, named member), with the flags A4 uses (co-lead, leader,
  same state, list, caucus, redistricting) and the 1/n weight. The two large raw hit files are not uploaded; the
  scripts rebuild them in about two minutes.
- **`a4/out/`:** `results.csv` (A4 and every check), `member_shares.csv` (one row per member), `home_ties.csv`
  (every home-map tie), `home_measures_*.csv`, `alpha_*.csv`, `ideology_check.csv`, the figures.
- **`press_scope/`:** the 18 Nov scan behind G4 and G13; its `scope_by_member.csv` is still the collector's input.
- **[`RERUN_22NOV.md`](RERUN_22NOV.md):** every number before and after the 22 Nov rerun.

## Still open (not analysis)

Nothing in this folder. `\cite{serrano2009}` (part 3) and the Voteview reference (`voteview2026`, Methods) were
placed on 25 Nov. What is left is shared: the split of the report and the cuts (`../WORK_AND_DEADLINES.md`).

## To rerun

Run from `Anas/`, with Python from Anaconda (`python -I`), pandas, pyarrow, networkx, matplotlib and openpyxl.
`<repo>` is the `project/` folder of a checkout of the group repo at `bc1c2344` or later; `a3/freeze.py` stops if
Martin's matcher, `members.csv` or the press files differ from the frozen checksums. Reader samples are stored, so
scoring reruns without new reading.

```bash
python -I a3/freeze.py       --press press_releases --repo <repo>   # A3.0, checksums
python -I a3/prepare.py      --press press_releases --repo <repo>   # A3.1
python -I a3/match_shared.py --press press_releases --repo <repo>   # A3.2, the floor's matcher
python -I a3/press_layer.py  --press press_releases --repo <repo>   # A3.3, plus the press layer
python -I a3/score_recall.py                                        # A3.4
python -I a3/rescore_switch.py                                      # needs the 20 Nov hit file (Anas's machine only)
python -I a3/bills.py        --press press_releases --repo <repo>   # A3.5
python -I a3/flags.py        --press press_releases --repo <repo>   # A3.6-7: out/mentions_press.parquet
python -I a3/examples.py     --press press_releases --repo <repo>
python -I a4/analysis.py     --press press_releases --repo <repo>   # A4 and its checks, about 10 s
python -I a4/figure_lean.py
python -I a4/figure3_column.py                                      # Figure 3 for the paper
python -I a4/score_tone.py                                          # check T
python -I a4/ideology_check.py --repo <repo>                        # check I
python -I a4/home_network.py
python -I a4/home_network_posthoc.py
python -I a4/home_measures.py
python -I a4/alpha_sweep.py
python -I a4/alpha_centrality.py
python -I a4/table_home_measures.py
python -I a4/figure_home_map.py
python -I a5/analysis.py     --press press_releases --repo <repo>   # A5, about 5 s
python -I a5/score_check.py
python -I a5/score_mirror.py
```

The collector itself (`collector/README.md`) is only rerun if the snapshot changes, and then in full.

## Removed on 25 Nov 2026

Outdated working files, removed so the folder shows only the final state. They are in the git history: `git show
81740143:project/Anas/<file>`.

| Removed | Why |
|---|---|
| `STATUS.md` | 20–22 Nov status, proposals to Martin and Diego and a priority list, all settled; its findings are in this README |
| `REVISIONS_19NOV.md` | Pointer to `STATUS.md` |
| `references_additions.bib` | All six entries are in `report/references.bib` |
| `a4/figure3.py`, `a4/out/figure3_draft.*` | Side-by-side draft of Figure 3, replaced by the one-column `figure3_column.py` |
| `a4/figure_network.py`, `a4/figure_network_groups.py` and their figures | Earlier drafts of the home-map figure, replaced by `figure_home_map.py` |
| `state_seats/` | Seats per state (19 Nov), descriptive; no result or number in the paper comes from it |
| `.gitkeep` | The folder is not empty |
| `G13_UPDATE.md` | Entered into `DECISIONS.md` G13 on 25 Nov, after Martin and Diego agreed |
| `dictionary.md`, `OFF_CURRICULUM.md` | Moved to the project folder (`../DICTIONARY.md`, `../OFF_CURRICULUM.md`) and updated for all three parts |
