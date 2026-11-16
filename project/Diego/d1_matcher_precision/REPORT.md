# D1: precision of the name matcher

Diego Mijares with Claude, 14 November 2026. Matcher and data as in `prototype_two_maps.ipynb` (one run,
13 November). Numbers below come from `score.py` and change if a label in `labels.csv` changes.

**Status: first-pass labels by Claude. Diego has checked 0 of 160 rows.** Under the group's rule that model
output is not a measurement until a human has checked it, the precision below is provisional until the
`diego_check` column of `labels.csv` is filled in. The seven rows marked as errors and the notes column are
the fastest place to start.

## Result

| Sample | Correct | Precision | 95% interval (Wilson) |
|---|---|---|---|
| Main sample, 100 random mentions | 93 | 93% | 86% to 97% |
| of which the 30 printed in the notebook | 29 | 97% | 83% to 99% |
| Same-party mentions in the main sample | 54 of 56 | 96% | 88% to 99% |
| Cross-party mentions in the main sample | 39 of 44 | 89% | 76% to 95% |

A match counts as correct when the text refers to the House member the matcher chose and the speaker said
it.[^strict] Four of the seven errors name the wrong person. Three name the right member in text the
speaker never said.

**Sentence for Methods (provisional).** We read a random sample of 100 of the 7,931 matched mentions with
their surrounding text. 93 referred to the matched member in the speaker's own words (95% interval 86% to
97%); four pointed at a different person and three were Congressional Record boilerplate attributed to the
speaker.

## The seven errors

| Item | Matched | What the text refers to | Parties |
|---|---|---|---|
| 5 | "Mrs. Peters" → Scott Peters | Carol Peters, a constituent of the speaker | R → D |
| 99 | "Mrs. Cole" → Tom Cole | Bettie Cole, for whom a post office is named | D → R |
| 37 | "Chairman Green" → Al Green | Mark Green (R-TN), then chair of Homeland Security | R → D |
| 75 | "Mr. Turner" → Michael Turner | Sylvester Turner (D-TX), who had died the day before | D → R |
| 56 | "Mr. VEASEY" → Marc Veasey | Vote-change line printed after a vote | D → D |
| 96 | "Ms. SCHOLTEN" → Hillary Scholten | Vote-change line printed after a vote | D → D |
| 68 | "Mr. HOYER" → Steny Hoyer | Hoyer's own speaker heading, left inside Brian Mast's turn | R → D |

Five of the seven errors are cross-party, against 44% of the sample. That is what a wrong match should look
like: a constituent or a namesake is on the other side about half the time, while real mentions stay inside
the party more often. Errors therefore push the floor map towards looking less divided, which is the
direction of the prototype's finding. With seven errors the difference between 96% and 89% is not
statistically reliable, but the direction matters for how the paper words its caveat.

## Where the errors come from, measured on all 7,931 mentions

**1. Eighteen members are invisible to the matcher.** In `members.csv` the surnames of the 18 rows with
`current == False` are stored in capitals (`GREEN`, `TURNER`, `GRIJALVA`). The matcher looks surnames up in
mixed case and never finds them. The rows are twelve members who appear to have left or died during the
Congress and the six delegates and resident commissioner: Radewagen, Raúl Grijalva, LaMalfa, Swalwell, Norton, Waltz, Cherfilus-McCormick, David Scott,
Marjorie Taylor Greene, Moylan, King-Hinds, Sherrill, Hernández, Mark Green, Sylvester Turner, Tony
Gonzales, Connolly and Plaskett. Two consequences:

- No mention of any of them is counted, although several speak often.
- Where one shares a surname with a visible member, the surname is treated as unique and the visible
  member receives the mentions. Al Green is credited with "Chairman Green" 11 times in 51 mentions, though
  he chairs nothing. Adelita Grijalva is credited with 20 mentions dated before September 2025, all
  tributes to her father. Michael Turner receives 6 mentions from Democrats in March 2025, the month
  Sylvester Turner died. David Scott's mentions go to Austin Scott or Bobby Scott, or are dropped.

This explains items 37 and 75. The fix is one line in `scripts/roster.py` or in the matcher (normalise the
case of `last`), after which Green, Turner, Scott and Grijalva go through the shared-surname rules.

**2. Record boilerplate inside a turn.** 71 mentions have the surname in capitals in the matched text
("Mr. VEASEY"). The Record prints names in capitals in speaker headings and vote-change lines, not in
speech. The matcher lower-cases them on purpose and so lets them in. Dropping matches whose surname is in
capitals removes items 56, 68 and 96 and their kind. Item 68 also shows a turn that the parser did not
split, which belongs with the speaker-assignment check (S2).

**3. Constituents and other non-members.** "Mrs." in front of a male member's surname is the visible sign
in items 5 and 99. There are 905 "Mrs." or "Ms." matches and the roster has no column for sex, so this
could not be counted. A column from `unitedstates/congress-legislators` (`gender`) would allow a title
check.

**4. The state rule.** In the supplementary sample, "Mr. Smith" twice became Adam Smith of Washington
because a speech about the filibuster film *Mr. Smith Goes to Washington* has "Washington" within 80
characters. State-nearby matches were 21 of 24 correct across both samples (one of the three errors is a
vote-change line). First-name matches were 22 of 22 and the Speaker rule 25 of 25.

**How much do the mechanical errors move the headline?** Removing the capital-surname mentions, the
"Chairman Green" mentions and the early Grijalva mentions takes the floor map from 3,718 ties and 34.5%
cross-party to 3,661 ties and 34.4%. The errors found so far do not explain the gap to the working map
(12% at the same size). The constituent errors are not in this figure because they cannot be identified
without reading.

## The yield flag

Among the 150 correct rows of both samples, the notebook's flag ("yield" within 60 characters) found 26 of
30 real yields (recall 87%) and 26 of its 29 flags were real yields (precision 90%). The misses are yields
with a long phrase in between ("I yield such time as he may consume to the gentleman from Texas"). The
false flags include item 12, "I cannot agree with Chairman Cole", the notebook's own example of
disagreement, flagged because the speaker had just thanked someone else for yielding. Relevant to M3: a
map with "yields dropped" also drops some substantive mentions. Matching the yielding phrase itself
(`yield[^.]{0,80}\(M[rs]s?\. Name\)` and "thank ... for yielding") would be more exact than a window.

## What was done, and what was not

- `draw_sample.py` rebuilds the notebook's mention table (it asserts 7,931 mentions and 717 dropped) and
  draws 100 mentions with the notebook's seed. The first 30 are the 30 printed in the notebook, in the same
  order. It also draws 20 more from each of the three rare resolution routes (seed 2806).[^supp]
- `make_labels.py` holds every label and the reason for each error. `labels.csv` is its output, with the
  context that was read.
- `score.py` computes everything above. A value in `diego_check` other than `ok` overrules the first-pass
  verdict.
- **Not measured: recall.** The sample contains only mentions the matcher made. The 717 shared-surname
  mentions it dropped, the 18 invisible members, and names used without a title are all outside it.
- The labels rest on 400 characters of context either side, and the full turn for the doubtful rows. No
  second coder has seen them.

[^strict]: Whether a vote-change line counts as an error is a choice. The lenient reading (right member,
    whoever said it) gives 96 of 100. We report the strict one because a tie in the floor map is meant to
    record one member naming another. Diego took this decision under Claude's guidance.
[^supp]: The supplementary 60 are not part of the 93%. They are there because a random 100 holds only 11
    matches made by the first-name, state and Speaker rules, too few to say anything about them. Diego took
    this decision under Claude's guidance.
