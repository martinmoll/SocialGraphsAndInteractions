# Decisions

Every choice that shapes the paper, why we made it, and what we gave up. At the presentation any of us can
be asked to defend any choice, so this file is what we read before then.

**Rule.** When the group or one member decides something that changes a number, a definition, the scope or
who does what, add an entry here the same day. A decision without a reason is not finished: write
**Reason: not recorded** and fill it in. Status changes and dates still go in
[`WORK_AND_DEADLINES.md`](WORK_AND_DEADLINES.md). A definition changed after the freeze on Sun 22 Nov also
goes in `docs/AI_METHODS.md` (README, section 9).

Status words: **Agreed**, **Open** (say when it is decided), **Replaced** (say by which entry).

---

## Template

```
### G<n>. <the decision in one line>
- **Status:** Agreed <date>, by <who> | Open, to decide <when>
- **Decision:**
- **Reason:**
- **Alternative and what it would have changed:**
- **Source:** <meeting, file, commit>
```

---

## Open

### G2. Questions for the TAs (Diego asks, 9:50 to 10:10)
- **Status:** (a) answered Wed 18 Nov, unclear, see G11. (b) and (c) still open.

| # | Question | If the answer is no |
|---|---|---|
| a | Is hand-labelling cross-party floor mentions as agreeing / disagreeing / procedural enough language analysis, or do they want TF-IDF, topics or sentiment too? | **Asked 18 Nov: no clear answer.** We added a text method anyway (G11) |
| b | Is a dataset chosen after the 4 Nov lock OK? | Not yet discussed |
| c | Is the hand-in right: 6 pages including references, 3 slides and the reflection, all by Fri 27 Nov? | Correct the deadlines in `WORK_AND_DEADLINES.md` |

- **Record here:** each answer, who gave it, and what we changed because of it.

---

## Agreed

The three part 1 definitions (G1a to G1c) were decided on Wed 18 Nov, reported by Martin. Before that, three
Claude advisers each reviewed the M3 proposal independently: one as a hostile examiner, one on network methods,
one on congressional politics. They agreed with the proposal on all three points. The group overruled them on
yields (G1b). All three definitions are locked after Sun 22 Nov (G7). Numbers and the original alternatives
are in [`Martin/M3_PROPOSAL.md`](Martin/M3_PROPOSAL.md).

### G1a. Thinning the working map: random ties are the headline
- **Status:** Agreed Wed 18 Nov.
- **Decision:** compare the floor map with **working ties drawn at random, at the same number of ties**. Use
  200 draws and report the range, not one draw. The strongest working ties (6 or more shared bills, 12.6%
  cross-party) are a **second, separate comparison**. The backbone (α = 0.05; 2,328 ties, 15.0%) stays as one
  robustness row in the table, not as a comparison.
- **Reason:** a floor tie means "named at least once", which is cheap and one-off. The like-for-like working tie
  is "signed at least one bill". Random thinning changes only the density and keeps the shape of the map:
  modularity is 0.210 for all ties and 0.202 for the random draw. Cutting to the strongest ties also changes
  *which* ties are kept: its own rewired null falls to 43.1%, while every other map sits near 50%. The
  floor counterpart of a strong partnership would be pairs named many times, and we can't build that because
  floor ties are unweighted.
- **Alternative and what it would have changed:** strongest ties as the headline, a gap of about 22 points
  instead of about 5. A reader could then say the cut made the gap, and our own table would support them.
  Dropping the backbone outright was also considered: it would look selective, because the result is already
  computed.
- **The attack and our answer:** "You picked the rule that shrinks your gap." The 22-point result is still in
  the paper, as its own finding: close allies are more partisan (12.6% against 28.7% for all ties). It just
  isn't the like-for-like comparison.
- **Source:** meeting, 18 Nov; `Martin/M3_PROPOSAL.md`, decision 1.

### G1b. Yields are dropped from the headline
- **Status:** Agreed Wed 18 Nov. **This goes against the M3 proposal and all three advisers.**
- **Decision:** the headline floor map leaves out yields ("I yield 2 minutes to the gentleman from Texas").
  Before the new draws (G1a), that map is 3,284 ties and 38.6% cross-party. The map **with** yields (34.2%) is
  shown directly **below** the headline. M4 leads with its without-yields run: Q = 0.116 observed against
  0.068 under the debate null.
- **Reason:** the question is who members talk *about*. A yield is a floor manager handing out speaking
  time under House rules, mostly to their own side (6.6% of yields cross the aisle). It isn't one member
  talking about another, so it doesn't belong in the map.
- **Alternative and what it would have changed:** keeping yields in the headline (the proposal). That gives a
  gap of 4.7 points instead of 9.1. It was the cautious choice, because dropping yields moves the result in our
  favour, and it kept the headline independent of the yield rule.
- **The attack and our answer:** "You picked the version that helps you." The with-yields row sits directly
  under the headline, and the floor map is less divided than random working ties either way. Part 2 codes
  yields as procedural, which supports treating them as procedure.
- **What it costs:** the headline now depends on the yield rule, so G1c's test must be done before the
  freeze. The headline also needs random working draws at 3,284 ties: the 29.5% figure was drawn at 3,777.
  **The 9.1-point gap is not the final number.**
- **Done 20 Nov (after G14):** 200 random working draws at the headline size (3,573 ties): **28.6%** cross-party
  (range 26.5% to 30.4%), party Q 0.211. Headline floor map 39.2%, Q 0.106: a gap of **10.6 points**, and no draw
  reaches the floor's share. With yields: 35.1% against 28.7% (26.9% to 30.7%) at 4,058 ties. Still subject to
  the G1c yield check and the G14 hand checks. `Martin/m3_table.csv`, `Martin/m3_random_draws.csv`.
- **Updated 22 Nov (after G18 and G19):** 3,970 ties, floor **38.7%** against 28.6% (26.8% to 30.6%), Q 0.112 against
  0.211: a gap of **10.1 points**; no draw reaches the floor. With yields: 35.2% against 28.7% at 4,423 ties.
- **Source:** meeting, 18 Nov; `Martin/M3_PROPOSAL.md`, decision 2.

### G1c. Yield rule: the phrase rule, tested on fresh rows before the freeze
- **Status:** Agreed Wed 18 Nov.
- **Decision:** `is_yield` uses the **phrase rule**. It flags "yield" before the name (not "yield back" or
  "yield myself"), or "for yielding" after the name, in the same sentence. Before Sun 22 Nov it is tested on rows
  it has never seen:
  1. **the main test:** about 30 hand-checked mentions where the window rule and the phrase rule disagree.
     Martin does these. Those are the rows where the two rules can be told apart;
  2. the yields in Diego's labelling sample. It has 100 rows, so we expect only about 9 yields (about 2
     cross-party and 7 same-party, estimated from the yield shares in the M3 proposal). That's enough to catch
     a gross failure, not to measure recall.
- **Done 18 Nov, after Diego finished coding:** `is_yield` in `Martin/mentions.parquet` is now the phrase rule
  (1,427 of 8,041 R–D mentions). The old flag is kept as `is_yield_window` (1,406); the two disagree on **285**
  mentions, which is the pool Martin's 30 rows are drawn from. Checked: same rows, same order, every other
  column identical, Diego's `full_key.csv` and `sample_key.csv` still point at the same mentions.
- **Timing, as agreed:** the phrase-rule flag was written into `Martin/mentions.parquet` only **after Diego had
  finished coding** his 100 rows. His sheets and `full_key.csv` point into that file by row number (`mention_row`), and
  `Diego/d5_classifier/classify.py` reads it. Until then the phrase rule is computed in memory for Martin's
  analysis, and only the `is_yield` column changes, never the rows or their order.
- **Test done 21 Nov (Martin coded the 30 rows blind):** of the 15 mentions only the phrase rule flags, **15 are yields**
  (no false flags). Of the 15 only the window rule flags, **14 are not yields**; the one coded Y (#18) is the second
  mention of the same member in one sentence, where the sheet marked both occurrences, and that mention is not a
  yield ("for initiating"). Strict reading 1 of 15, corrected 0 of 15. The phrase rule stands; the headline's
  dependence on it (G1b) is now tested. `Martin/m3_yield_check/README.md`.
- **Reason:** the window rule found 26 of 30 labelled yields with 3 false flags; the phrase rule found 30 of 30
  with none. But the phrase rule was written after reading D1's errors and scored on those same 30 rows, so
  "30 of 30" is a fit to the data, not a test. Because of G1b the headline now depends on it.
- **Alternative and what it would have changed:** keeping the 60-character window rule. The map barely moves
  (38.2% against 38.6% without yields), but the rule makes both kinds of error D1 found.
- **What the paper may write:** "checked on N hand-labelled held-out mentions", with the real N. Never
  "100% recall". The test catches gross failures, but at this size it won't give a tight recall figure.
- **Source:** meeting, 18 Nov; `Martin/M3_PROPOSAL.md`, decision 3.

### G12. Asking a member to yield is not a yield
- **Status:** Agreed Wed 18 Nov, by Martin.
- **Decision:** "Will the gentleman yield?" (asking the named member to yield) does **not** count as a yield. Only
  handing time *to* the named member, or thanking them *for* yielding, counts. The mention stays in the headline
  floor map. In the hand check of the yield rule (`Martin/m3_yield_check/`) such rows are coded N.
- **Reason** (confirmed by Martin, 18 Nov): no floor time passes to the named member. The
  speaker is addressing that member, usually in the middle of an argument, which is "talking to or about"
  them, so it is what the floor map is meant to capture (G1b). It also matches what the phrase rule
  already does: it doesn't flag these.
- **Alternative and what it would have changed:** count it as a yield, since it is floor-time procedure too. More
  mentions would be dropped from the headline map, and the phrase rule would need a third pattern.
- **Source:** Martin, 18 Nov, while preparing the yield-rule check.

### G14. Matcher changes of 20 Nov: nicknames, lists, "State Rep." (applied before the freeze)
- **Status:** Applied Fri 20 Nov by Martin (with Claude), from Anas's `Anas/MATCHER_CHECKLIST.md`. **Agreed Sat 21 Nov
  by Martin**, including the 24-of-30 rule for untitled names. The 530 new rows are not yet hand-checked
  (`Martin/m1_checks_20nov/`).
- **Floor recall measured 22 Nov** (Martin, 30 random turns): the matcher found 12 of the 13 House members named
  (92%, 95% interval 67% to 99%). The one miss is a shared surname with no first name or state nearby ("Congressman
  Evans"), dropped by design. `Martin/m1_checks_20nov/README.md`, result 1.
- **Press side (agreed 21 Nov):** Anas switches A3 to this version of the matcher, so floor and press releases use
  one name matcher. What his press layer still adds on top is his to record.
- **Decision:** in `Martin/matcher.py`: (9) nicknames count as first names, so Bobby Scott, Chuy García, Chris
  Smith, Hank Johnson, Buddy Carter and Hal Rogers are no longer dropped; (1) names in a list after a plural title
  ("Reps. A, B, and C") are each a mention; (10) a title right after "State" is skipped; (5) senators stay
  unmatched, pinned by a test. Not done: (2) untitled full names stay off for the floor until a 30-row hand
  check (at least 24 of 30 real mentions to switch on; threshold proposed by Claude, agreed by Martin 21 Nov, before coding); (3) carrying a name forward in a turn.
- **Effect:** 8,092 → 8,622 floor mentions, no old row lost (Diego's 100 D2 rows checked; old row numbers map
  through `Martin/m1_checks_20nov/row_map.csv`). Headline floor map (phrase yields dropped): 3,284 → 3,573 ties,
  38.6% → **39.2%** cross-party. Without the list hits: 38.6%. So the change moves the headline by under one point.
- **Reason:** the matcher missed names for a reason that can be fixed and named in Methods. List hits are more
  cross-party than other mentions (49.5% against 36.0% of R–D mentions; none are yields), so leaving them out
  would under-count cross-party naming. **Note the direction:** the fix raises the floor share, which favours our
  headline; the row without list hits (38.6%) is in the M3 table for that reason.
- **Alternative and what it would have changed:** leave the matcher as on 18 Nov and report the misses as a
  limitation. The numbers would stay as measured by G10, but recall would be lower and the six nickname members
  would be under-counted. Or drop list hits as "less chosen" than a named thank-you: 38.6% instead of 39.2%,
  a row in the M3 table.
- **Costs:** G10's 98/100 precision was measured on the 18 Nov rows. The new rows need their own check (20 list
  rows, `list_sheet.csv`) or a Methods sentence saying they were not checked. Long thank-you lists (up to about
  15 names) each add many ties.
- **Source:** `Anas/MATCHER_CHECKLIST.md` items 1, 2, 3, 5, 9, 10; `Martin/m1_checks_20nov/README.md`.

### G15. M5: how communities are found and compared
- **Status:** Agreed Sat 21 Nov by Martin. Run 20 Nov with the choices below (`Martin/m5_communities.py`).
- **Decision (proposed):** Louvain (resolution 1) on the same unweighted maps as M3, 50 seeds per map, best
  partition kept; NMI with party on members with a tie, NMI between maps on members in both; baseline = Louvain on
  degree-preserving rewirings. Committees from today's membership (unitedstates/congress-legislators), full
  committees only; a tie "shares a committee" if the two members sit on one.
- **Reason:** same maps and nulls as the rest of part 1, so the numbers can be read side by side. Louvain is the
  course's method (week 4). Several seeds because one Louvain run is random.
- **Alternatives and what they would change:** weighted working ties (NMI with party 0.75 instead of 0.83, one row
  in `m5_table.csv`); a fixed number of communities, e.g. two, to force a party test (would hide the committee
  structure); committee membership at the start of the term (not in our data; today's lists misplace members who
  moved).
- **What it found (first run):** working map = the two parties (NMI 0.83); floor map = 8 communities across party
  (NMI 0.03); in 7 of them one committee is 3.0 to 7.9 times as common as in the House (22 Nov run, after G19). 46% of floor ties join committee colleagues, 17.5% under rewiring.
- **Source:** `Martin/m5_table.csv`, `Martin/m5_committees/committee_table.csv`.

### G16. The state null is one robustness row in part 1
- **Status:** Agreed Fri 20 Nov by Martin, on Anas's proposal (`Anas/state_null/`, STATUS.md section 0, row 2).
- **Decision:** add a null that keeps every member's number of ties and number of same-state ties
  (`Martin/m3b_state_null.py`, Anas's function, 200 draws for the floor maps and 20 for the working map). One row
  in the robustness table and one sentence in Results.
- **Reason:** many state delegations are mostly one party, so a reader can ask whether the division is geography.
  The answer is no: Q 0.001 under the null (max 0.023, 22 Nov run after G19) against 0.112 for the headline floor map, and 0.006
  against 0.210 for the working map. Same-state ties are over-represented (floor 9.0% against 3.7% by chance) but
  are not what makes the maps divided.
- **Alternative and what it would have changed:** leave it out. One fewer row; the geography objection is
  unanswered.
- **Source:** `Martin/m3b_state_null.csv`; Anas's pilot.

### G17. Scope is frozen from Sat 21 Nov
- **Status:** Agreed Sat 21 Nov by Martin. **Anas and Diego to confirm in the chat**; record their answer here.
- **Decision:** nothing new is added to the project: no new analysis, data source, null model, figure, check or
  extension. The scope is what `WORK_AND_DEADLINES.md` section 2 lists and what G1 to G16 decide. From now on we
  only:
  1. finish the listed tasks (the hand checks and the reruns they cause, A3, A4, M6, the matcher table);
  2. fix errors;
  3. write, cut and rehearse.
- **Optional items:** each owner may still finish one by **Sun 22 Nov**; if it is not finished then, it is dropped
  and is not mentioned as planned work:
  - A5, "bipartisan" releases (Anas);
  - the before/after check on the redrawn states, `Anas/methods_drafts.md` check 3 (Anas);
  - the curve of cross-party share against ties kept, from the report skeleton (Martin).
- **New ideas** that come up while writing go into the Discussion as future work, one line each, not into the
  analysis.
- **Reason:** the draft is due Tue 24 Nov at 20:00 and the paper is six pages. Since 18 Nov the scope has grown
  every day (Democrats in the close-up, G13; the state null, G16; the committee reading of M5; the press layer and
  recall checks). Each addition is one more thing to finish, fit on the page and defend out loud, and at the
  presentation any of us can be asked about any of it.
- **Alternative and what it would have changed:** keep adding until the numbers freeze on Sun 22 Nov. Perhaps a
  little more polish, but a real risk of an unfinished draft on Tuesday and less time to rehearse the defence.
- **Source:** Martin, 21 Nov, in the group chat.

### G18. Matcher fixes of 22 Nov: possessives and middle initials (error fixes before the freeze)
- **Status:** Agreed Sun 22 Nov by Martin, from Anas's `MATCHER_CHECKLIST.md` items 12 and 15. Error fixes, allowed
  under G17.
- **Decision:** (H) a possessive is read as the name: "Mr. Cole's amendment" now gives Cole; (I) a single middle
  initial is read past: "Rep. James P. McGovern" gives McGovern, not John James. Tests added to `matcher.py`.
- **Effect:** 8,622 → 9,058 floor mentions: +440 (375 with a possessive), and 4 removed that were wrong (non-members
  such as "Mr. James R. Willis" read as John James). Headline map 3,573 → 3,675 ties, 39.2% → **39.3%** cross-party;
  random working draws 28.6% (26.6% to 30.3%). M4, M5, the committee check and the state null rerun; every reading
  holds. Diego's 100 rows and the yield-check rows are all still there (`row_map.csv`). Claude read 15 new rows at
  random: all right.
- **Reason:** both were errors with a known cause, and "Mr. Cole's amendment" is the kind of example an examiner
  reads. The added mentions are about as cross-party as the rest, so the headline barely moves.
- **Alternative and what it would have changed:** leave them and write a Methods sentence. Numbers frozen as on
  20 Nov; 4 wrong mentions kept; recall lower by about 5%.
- **Not fixed (known, harmless):** "Washington" the city can settle a shared surname as the state (2 floor
  mentions); untitled names have no guard after "Sen." (off for the floor). Checklist items 13 and 14.
- **Source:** `Anas/MATCHER_CHECKLIST.md`; commit of 22 Nov.

### G19. Untitled full names count on the floor too, with a title guard
- **Status:** Agreed Sun 22 Nov by Martin, by the rule fixed before coding (G14: 24 or more of 30 real mentions).
- **Decision:** floor mentions include full names without a title ("my colleague and friend, Chip Roy"),
  `how = "full name, no title"`. A name right after a non-House title is skipped ("Senator", "Governor", "Mayor",
  "Secretary", "State" and others; Anas's checklist item 14).
- **The check:** Martin coded 30 random untitled hits: 30 are mentions of that member (two after a second reading:
  "Jim Clyburn" and, in the list check, "Dave Taylor" are the members, by nickname), none procedural, none another
  person. 95% interval 89% to 100%. The list check: 20 of 20 right.
- **Effect:** 9,058 → 9,988 floor mentions (+930), no row lost. Headline map 3,675 → 3,970 ties, 39.3% → **38.7%**
  cross-party, Q 0.106 → 0.112, against 28.6% (26.8% to 30.6%) for random working draws: a gap of 10.1 points. The
  untitled mentions are 35% cross-party, like the rest; half of them make floor ties that did not exist before.
  Recall in Martin's 30 turns is unchanged (12 of 13). All of M3 to M5, the committee check and the state null rerun;
  every reading holds.
- **Reason:** floor and press now count the same name forms, and the check found no errors in the new form.
- **Alternative and what it would have changed:** titled names only on the floor. 39.3% instead of 38.7%, and the
  floor and press would count names differently, which Methods would have to explain.
- **Source:** `Martin/m1_checks_20nov/README.md`, results 2 and 3.

### G9. Yields stay in the labelling sample
- **Status:** Agreed Wed 18 Nov.
- **Decision:** Diego's labelling sample (100 rows, already drawn) keeps the yields among them.
- **Reason:** those rows are the held-out test of the yield rule (G1c), and the protocol's procedural code
  already handles them.
- **Alternative:** redrawing without yields. That costs time already spent coding, and the yield rule loses
  a fresh test.
- **Source:** meeting, 18 Nov.

### G10. The new matcher's precision is re-measured before the freeze
- **Status:** Agreed Wed 18 Nov. In progress.
- **Decision:** the precision of the new matcher (M1) comes from the labelling sample itself. Its 100 rows
  were drawn from `Martin/mentions.parquet`, which the new matcher wrote, and code **X (not a mention)** marks
  each wrong match. Precision = 1 − (share of X), from Diego's codes on all 100 rows. Martin's codes on rows
  1–25 (and Anas's on 76–100) give a second coder for the X decisions. No separate matcher check is run.
- **Reason:** the headline rests on it more than on any of G1a to G1c. In D1, 7 of 100 matches on the *old*
  matcher were wrong and 5 of the 7 were cross-party. Wrong matches push the floor share up. If the same held
  on the new matcher, a rough estimate puts the floor share near 31%, close to the working share. The new
  matcher's precision was never measured. All three advisers raised this without being asked.
- **Alternative:** citing D1's 93%. That was measured on a different matcher. Or a separate D1-style check:
  more rows, but no time for it.
- **Limits:** 100 rows gives an interval of several points on precision. The sample is 75% cross-party by
  design, so precision has to be reported per stratum (cross-party, same-party) or reweighted, not as one
  raw share.
- **Source:** meeting, 18 Nov.

### G3. Owners
- **Status:** Agreed in the meeting plan, Wed 18 Nov.
- **Decision:** Martin does the networks and nulls. Anas does the press releases. Diego does validation and
  the language analysis (labelling). **The Introduction and Discussion are written together.**
- **Change from before:** the Introduction and Discussion were Diego's task D4.
- **Reason:** not recorded.
- **Source:** meeting plan, 18 Nov.

### ~~G4. Press releases: Republicans only, swing seats against safe seats~~ Overwritten by G13
<del>
- **Status:** Agreed in the meeting plan, Wed 18 Nov.
- **Decision:** collect press releases from Republicans only, and compare members in swing seats with
  members in safe seats. The question: do swing-seat Republicans name Democrats more at home?
- **Reason:** not recorded beyond the question itself. The README already argues that Republicans in exposed
  seats had a reason to look independent (section 1).
- **Alternative:** both parties (open question 3 in the work plan). That would mean roughly twice the
  collection, and the swing-seat argument would need a Democratic version.
- **Change from before:** the README (section 1) and the work plan (section 5) say district lean is used
  **only to spread the sample**. It is now a comparison in its own right, so the sample has to be balanced
  between swing and safe seats, and we need a definition of a swing seat. **Not yet defined.**
- **Source:** meeting plan, 18 Nov.
</del>

### Draft for G13

Two edits:

1. In **G4**, replace the Status line with the one under "Edit 1".
2. Insert **G13** directly after G4, before G5.

---

#### Edit 1: the Status line of G4
- **Status:** Replaced by G13 (Wed 18 Nov): Democrats are now included, with a smaller role.

---

#### Edit 2: new entry G13, after G4

##### G13. Press releases: both parties, the Democrats as a small second side of the close-up
- **Status:** Agreed Wed 18 Nov, by the group (after the meeting). Replaces G4. Three details are open (below).
- **Decision:** the press-release close-up covers Democrats as well as Republicans. The Republicans stay the
  main case. The Democrats get one role: a comparison that shows whether naming the other side at home goes
  with an exposed seat, or with belonging to the president's party in a midterm year. They do not get their
  own figure or their own section. They appear as one panel or inset in figure 3 (G6), or as one paragraph
  if the panel adds nothing. The two maps (part 1) stay the headline.
- **What the Democrats add, concretely:**
  - **Exposure or party.** If exposed Democrats name Republicans about as often as exposed Republicans name
    Democrats, showing the other side is about the seat. If only Republicans do it, it is about being in the
    president's party. With Republicans alone the first reading cannot be told from the second.
  - **Mutual showing.** With both sides collected, a pair can be checked from both ends: when a Republican
    shows a Democrat at home, does that Democrat show the Republican back? This was council option E, dropped
    on 13 Nov for lack of data (work plan, section 5).
- **Reason:**
  - **The cost in G4 turned out smaller than expected.** G4's reason against was "roughly twice the
    collection". A scan of every member's site (`Anas/press_scope/`, one run, 18 Nov) found and counted the
    press-release listing for 407 of 450 members, 198 Democrats and 209 Republicans, with the same scripts
    for both parties. The extra work is download time, not new collectors.
  - **The material is there.** Since 3 Jan 2025 the median Democrat has published 152 releases and the median
    Republican 90. 56 Democrats and 36 Republicans in exposed seats can be counted (2026 lean within 5 points, or
    leaning to the other party; not the group's definition, see below).
  - **A first look says the comparison is not empty.** 20 recent releases each from 16 members: releases that
    name a House member of the other party, party leaders excluded: exposed Democrats 21% (4 members), safe
    Democrats 5% (4), exposed Republicans 36% (4), safe Republicans 8% (4). Pairs that name each other in
    that sample: Golden and Lawler, Golden and Fitzpatrick, Kaptur and Fitzpatrick. Too small to report, and
    made with the pilot's name rules, not the shared matcher. It shows only that both sides have something to
    count.
  - **It makes the close-up less guessable.** The council review (13 Nov) called "swing-seat Republicans
    mention Democrats more" easy to guess. Whether Democrats do the same is not.
- **Alternative and what it would have changed:** Republicans only (G4). Half the collection and a simpler
  figure 3, but the close-up could not tell a seat effect from a party effect, and mutual showing stays dropped.
- **Limits:**
  - G5 still applies: no data for the first 20 members by Fri 20 Nov and the close-up is dropped, Democrats
    included.
  - 27 Republican sites and 5 Democratic ones stopped posting before September 2026. The two parties must be
    compared over one common date window.
  - 31 of the counted exposed members (21 D, 10 R) are in redrawn states, where the 2026 lean describes a
    district they did not serve in.
- **Open, to decide by Fri 20 Nov:**
  1. **The first 20 members.** Proposed: 12 Republicans and 8 Democrats, each spread over exposed and safe
     seats.
  2. **The swing-seat definition** G4 left open, now needed for both parties. It must work in redrawn states
     (old district, not 2026 lean).
  3. **The date window** both parties are compared over.
- **Consequences for other files (not yet changed):** the work plan's A2 and A4 still say Republicans only;
  its open question 3 is answered by this entry; "mutual showing" and "Democrats in Trump districts" in its
  section 5 are partly back. README section 2, part 3, still reads "which Democrats a Republican names".
- **Source:** group discussion, Wed 18 Nov, after the meeting; numbers from `Anas/press_scope/README.md`.


### G5. Stop rule for the close-up
- **Status:** Agreed in the meeting plan, Wed 18 Nov.
- **Decision:** Anas gives a date for the first 20 members. If there is no data by **Fri 20 Nov**, we drop
  the close-up.
- **Reason:** the paper still works without it. Parts 1 and 2 stand on their own (README, section 6), so
  the risk to the paper is capped.
- **Consequence if triggered:** drop A3 to A5 and M6 (work plan, section 3). Figure 3 is affected (G6).
- **Source:** meeting plan, 18 Nov.

### G6. The three figures
- **Status:** Agreed in the meeting plan, Wed 18 Nov.
- **Decision:** (1) the two networks; (2) what a cross-party mention means; (3) example ties.
- **Reason:** not recorded. They match parts 1, 2 and 3 of the paper (README, section 2).
- **Open dependency:** figure 3 comes from the close-up. If G5 drops the close-up, figure 3 has to come from
  the floor map or be replaced. **Not decided.**
- **Source:** meeting plan, 18 Nov.

### G7. Definitions are locked after Sunday
- **Status:** Agreed in the meeting plan, Wed 18 Nov.
- **Decision:** the part 1 definitions (G1) cannot change after Sun 22 Nov.
- **Reason:** numbers have to be frozen before the draft on Tue 24 Nov, and definitions are fixed before
  results are looked at again (README, section 9).
- **Source:** meeting plan, 18 Nov; work plan, section 1.

### G8. How the labelling is done
- **Status:** Agreed in the meeting plan, Wed 18 Nov. **Changed the same morning by Diego (see "Changed"
  below).** The rules themselves are fixed from 11:15 on.
- **Decision:** Diego draws about 150 cross-party mentions from `Martin/mentions.parquet` into a shared sheet.
  At 10:45 all three of us label the same 20 and compare, to test the rules. The rules are fixed after that
  comparison. Then every mention is labelled by two people. Due **Sat 21 Nov**.
- **Reason:** two coders per mention give an agreement score (κ). The protocol already sets what happens if
  κ on cross-party mentions is below 0.6 ([`Diego/d2_labelling/PROTOCOL.md`](Diego/d2_labelling/PROTOCOL.md)).
  Testing on 20 first catches unclear rules before they reach all 150.
- **Changed, 18 Nov, by Diego under Claude's guidance** (`Diego/d2_labelling/PROTOCOL.md`, footnote "hundred"):
  **100 mentions** (75 cross-party, 25 same-party), not 150 or 200. Diego codes all 100. The second coder is
  Martin for rows 1–25, **Claude for rows 26–75**, and Anas for rows 76–100. Reason given: fits the time the
  group has. Agreement is reported separately for Diego against Claude, and the paper says which rows had an
  AI as second coder.
- **What the change costs:** an interval of about ±11 points on a share near one half (the protocol's figure),
  against about ±8 with 150. Half the rows have **two coders but only one human**. The course asks for model
  output to be validated against human labels, so the 50 Claude rows count as validated only if the
  Diego-against-Claude agreement is reported and holds up. **The group has not discussed this change yet.**
- **Record here at 11:15:** every rule changed after the 20-mention test, and why.
- **Source:** meeting plan, 18 Nov; Diego's commits `0a401d39`, `dd8a7fe3`.

### G11. A TF-IDF classifier carries the hand labels to all floor mentions (plan B, D5)
- **Status:** Decided Wed 18 Nov by Diego, recorded in the work plan (section 4). Not yet discussed by the group.
- **Decision:** train TF-IDF with logistic regression on the 100 hand labels. Check it by leave-one-out against
  those labels, then apply it to all 8,041 floor mentions between the two parties. The named member's surname
  is masked as `NAMED`.
- **Reason:** the TAs gave no clear answer to G2a. This way the language part uses the course's own NLP tools
  (week 6), not reading alone.
- **Alternative and what it would have changed:** hand labels only. Less work and no risk of a weak
  classifier, but the paper might not meet the bar for language analysis.
- **Known risk:** the placeholder run (Claude's 50 codes) predicts "agreeing" for almost everything: 80%
  accuracy against 76% for always guessing "agreeing", and 1 of 5 disagreements found. The plan in
  `Diego/d5_classifier/README.md`: **the hand labels carry the result and the classifier is the extension.** If
  it doesn't clearly beat the baseline, the paper says so as a finding.
- **Source:** work plan section 4 (Diego, 18 Nov); `Diego/d5_classifier/README.md`; commit `d77a5692`.

---

## Decisions recorded elsewhere

These were made before this file existed. They are not copied here. Each place lists the choice and its
alternative.

| Where | What |
|---|---|
| [`prototype_two_maps.ipynb`](prototype_two_maps.ipynb), section 0 | Every modelling choice in the prototype (13 Nov) |
| [`Martin/README.md`](Martin/README.md), "Choices made here" | Matcher and `mentions.parquet`: 6 choices, confirmed by Martin on 16 Nov |
| [`Martin/README.md`](Martin/README.md), M4 | The debate-preserving null: 7 choices |
| [`Martin/M3_PROPOSAL.md`](Martin/M3_PROPOSAL.md) | The three M3 decisions, with the alternatives (G1) |
| [`Diego/README.md`](Diego/README.md), "Decisions taken" | Diego's choices in D1 to D4 |
| [`Diego/d2_labelling/PROTOCOL.md`](Diego/d2_labelling/PROTOCOL.md) | Labelling codes, hard-case rules, κ threshold |
| [`archive/`](archive/README.md) | How the research question was chosen |
