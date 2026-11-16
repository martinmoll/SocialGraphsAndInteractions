# M3: definitions for part 1, proposal for 18 November

Martin Møllenhus with Claude, 16 November 2026. For the group to decide at the meeting. Every number comes
from [`m3_definitions.py`](m3_definitions.py) (one run, seed 2805) and is in [`m3_table.csv`](m3_table.csv).
**Observations, not results.**

## The three decisions

| # | Decision | Proposal |
|---|---|---|
| 1 | How the working map is thinned | Compare the floor map with **working ties drawn at random, same number of ties**. Report the strongest ties as a second, separate comparison. Drop the backbone |
| 2 | Whether yields count in the headline | **Keep yields in the headline number.** Report the map without yields in the row below it |
| 3 | How a yield is recognised | **Replace the 60-character window with the phrase rule** in `mentions.parquet` |

**What the proposal does to the paper.** Under it the headline is no longer "one floor tie in three crosses
the aisle against one working tie in eight". It is: **the floor map is a little less divided than working
ties in general (34% against 30% cross-party) and much less divided than strong working ties (13%)**. The
first gap is small enough that matcher errors could close it. See "What could close the gap" below.

## The table

Party modularity and cross-party share of each map, with the same degree-preserving rewiring as the
prototype (200 rewirings; 20 for the all-ties map).

| Map | Ties | Cross-party share | After rewiring | Party modularity |
|---|---|---|---|---|
| Floor: all mentions | 3,777 | 34.2% | 50.1% | 0.156 |
| Floor: yields dropped, window rule | 3,305 | 38.2% | 49.9% | 0.116 |
| Floor: yields dropped, phrase rule | 3,284 | 38.6% | 50.0% | 0.111 |
| Floor: phrase yields and leadership titles dropped | 2,739 | 39.6% | 50.0% | 0.102 |
| Working: all ties | 46,513 | 28.7% | 49.7% | 0.210 |
| Working: random ties, same size as floor | 3,777 | 29.5% | 49.9% | 0.202 |
| Working: strongest ties, same size as floor | 3,777 | 12.6% | 43.1% | 0.301 |
| Working: strongest ties, same size as floor without yields | 3,284 | 12.6% | 42.9% | 0.297 |
| Working: backbone α = 0.05 | 2,328 | 15.0% | 49.4% | 0.342 |

- Every map is more divided than its rewired null: the largest modularity in any rewiring is 0.025.
- The floor map is less divided than the working map under every thinning rule. The size of the gap depends
  almost entirely on the rule: 22 points against the strongest ties, 5 points against random ties.
- Against the prototype (13 November), the floor map moved from 3,718 ties and 34.5% to 3,777 ties and
  34.2% with the new matcher.

## Decision 1: thinning the working map

Modularity depends on density, so the working map (46,513 ties) has to be cut to the size of the floor map
(3,777) before the two are compared. Three ways to cut it:

| Rule | What it keeps | Cross-party share | What it means for the comparison |
|---|---|---|---|
| **Random ties** (new) | 3,777 ties drawn at random | 29.5% | Changes only the density. A tie still means "signed at least one bill", which matches the floor tie, "named at least once" |
| Strongest ties | Pairs with at least 6 shared bills | 12.6% | Changes the density **and** selects close allies, who are mostly in one party. Compares strong working ties with floor ties of any strength |
| Backbone α = 0.05 | Ties surprisingly strong for either member | 15.0% | As the strongest ties, with one more parameter and a different size (2,328) |

**Proposal: random ties as the main comparison, strongest ties as a second one.** The floor map counts a
pair that named each other once. The like-for-like working tie is a pair that signed one bill. The
strongest-ties rule answers a different question (are close allies more partisan than acquaintances?), and
the answer is yes on its own: 12.6% against 28.7%. Reporting both keeps the strong result while making
clear which part of it is the thinning.

**What it costs.** The headline gap falls from 22 points to 5. One random draw was made; a second draw
would move 29.5% by under one point (a share of 0.3 over 3,777 ties has a standard error of 0.7 points).

**Alternative.** Keep the strongest ties as the headline, as in the prototype, and defend it as "the ties
that matter". A reader can then say the gap is made by the cut, and the table above would support them.

## Decision 2: yields in the headline

A yield is one member handing speaking time to another. The phrase rule flags 1,427 of the 8,041 mentions
(17.7%). Only 6.6% of them cross the aisle, against 42.4% of all other mentions.

| Choice | Floor map | Gap to working, random ties (29.5%) |
|---|---|---|
| **Yields kept** | 34.2% cross-party, modularity 0.156 | 4.7 points |
| Yields dropped | 38.6% cross-party, modularity 0.111 | 9.1 points |

**Proposal: keep yields in the headline and show the map without them directly below.** Dropping yields
moves the floor map in the direction of our own finding, so keeping them is the cautious choice. The
headline then also does not depend on how well the yield rule works.

**Alternative.** Drop them, on the argument that handing over time is House procedure and not one member
talking about another. That is a fair reading of the question, and part 2 (the hand labels) will say how
much of the rest is procedure too. If the group prefers this, the same choice should be applied in M4,
where the floor map is tested with and without yields already.

## Decision 3: the yield rule

| Rule | Yields found, of 30 | Its flags that are yields |
|---|---|---|
| Window: "yield" within 60 characters of the name (now) | 26 (87%) | 26 of 29 (90%) |
| **Phrase** | 30 (100%) | 30 of 30 (100%) |

Tested on the 150 correct matches of Diego's D1 that carry a yield label. The phrase rule flags a name when
either holds, within the same sentence:

- "yield" comes before the name, and is not "yield back" or "yield myself" ("I yield 2 minutes to the
  gentleman from Texas (Mr. Roy)");
- "for yielding" comes after the name ("I thank Chairman Cole for yielding").

**Proposal: use the phrase rule.** It fixes both kinds of error D1 found: yields with a long phrase before
the name, and substantive mentions flagged because a yield was nearby ("I cannot agree with Chairman
Cole"). On the full file the two rules agree on 1,274 mentions; the map barely moves (38.2% to 38.6%).

**How far the test goes.** Thirty yields is a small sample: with 30 of 30 the 95% interval for recall
starts at 89%. The rule was written after D1's report described the errors, on the same rows it is tested
on, so it has not been tested on rows it has never seen. The yield labels are Claude's first pass.

**What it changes for the others.** `is_yield` in `mentions.parquet` keeps its name and changes its
meaning. Diego's labelling sample reports how many of its rows are flagged, nothing more.

## What could close the gap

With the proposal, the main comparison is 34.2% (floor) against 29.5% (working). Three things bear on
whether that difference is real:

- **Matcher errors push the floor share up.** In D1, 7 of 100 matches were wrong and 5 of those 7 were
  cross-party. If the same held for ties, the floor share without errors would be about 31%: a rough
  figure, from seven errors measured on the prototype's matcher. The new matcher removes the kind of error
  behind 5 of the 7. **Its precision has not been re-measured, and this is now the number the headline
  rests on.**
- **Tone is unmeasured.** A cross-party mention may be a disagreement (part 2).
- **The debate structure** explains about half of the floor map's own division (M4), and has no
  counterpart in the working map.

This is the second condition in section 6 of the project README ("the gap disappears under a fair thinning
rule"). It has not disappeared, but it has shrunk from 22 points to 5.

## Not looked at

- **Bill types.** Still `hr` and `hjres` (8,701 bills, 126,475 cosponsorships). Adding simple and
  concurrent resolutions was not tried.
- **Direction and weight** of floor ties. Still undirected and unweighted.
- **A test of the 5-point gap.** No interval has been put on the difference between the two maps.
