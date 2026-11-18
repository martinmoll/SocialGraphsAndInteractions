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

### G1. Part 1 definitions (M3): thinning the working map, yields, and the yield rule
- **Status:** Open, to be decided at the meeting on Wed 18 Nov, 9:00. Martin presents it in 5 minutes. Locked
  after Sun 22 Nov.
- **Proposal** (full text, numbers and alternatives in [`Martin/M3_PROPOSAL.md`](Martin/M3_PROPOSAL.md)):
  1. Compare the floor map with **working ties drawn at random at the same size** (29.5% cross-party).
     Report the strongest ties (12.6%) as a second comparison. Drop the backbone.
  2. **Keep yields** ("I yield to...") in the headline number (34.2%). Show the map without yields (38.6%)
     directly below.
  3. Replace the 60-character yield window with the **phrase rule** (30 of 30 labelled yields found).
- **What is at stake:** under the proposal the headline gap is 5 points, not 22, and matcher errors could
  close it.
- **Record here after the meeting:** what was chosen on each of the three points, the reason, and whether
  M4 follows the same yield choice.

### G2. Questions for the TAs (Diego asks, 9:50 to 10:10)
- **Status:** Open, answers expected Wed 18 Nov.

| # | Question | If the answer is no |
|---|---|---|
| a | Is hand-labelling cross-party floor mentions as agreeing / disagreeing / procedural enough language analysis, or do they want TF-IDF, topics or sentiment too? | Add a text method. That is new work before the freeze on Sun 22 Nov |
| b | Is a dataset chosen after the 4 Nov lock OK? | Not yet discussed |
| c | Is the hand-in right: 6 pages including references, 3 slides and the reflection, all by Fri 27 Nov? | Correct the deadlines in `WORK_AND_DEADLINES.md` |

- **Record here:** each answer, who gave it, and what we changed because of it.

---

## Agreed

### G3. Owners
- **Status:** Agreed in the meeting plan, Wed 18 Nov.
- **Decision:** Martin does the networks and nulls. Anas does the press releases. Diego does validation and
  the language analysis (labelling). **The Introduction and Discussion are written together.**
- **Change from before:** the Introduction and Discussion were Diego's task D4.
- **Reason:** not recorded.
- **Source:** meeting plan, 18 Nov.

### G4. Press releases: Republicans only, swing seats against safe seats
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
- **Status:** Agreed in the meeting plan, Wed 18 Nov. The rules themselves are fixed from 11:15 on.
- **Decision:** Diego draws about 150 cross-party mentions from `Martin/mentions.parquet` into a shared sheet.
  At 10:45 all three of us label the same 20 and compare, to test the rules. The rules are fixed after that
  comparison. Then every mention is labelled by two people. Due **Sat 21 Nov**.
- **Reason:** two coders per mention give an agreement score (κ). The protocol already sets what happens if
  κ on cross-party mentions is below 0.6 ([`Diego/d2_labelling/PROTOCOL.md`](Diego/d2_labelling/PROTOCOL.md)).
  Testing on 20 first catches unclear rules before they reach all 150.
- **Record here at 11:15:** every rule changed after the 20-mention test, and why.
- **Source:** meeting plan, 18 Nov.

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
