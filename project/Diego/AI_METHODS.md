# AI methods: where a model touched the results, and how it was checked

Required by the course ("The new way of working": the project repository contains an `AI_METHODS.md` documenting
every place a model touched the results and how it was checked). Written by Diego with Claude on 22 November 2026
from the repository itself. Task A6 was Anas's; the group moved this file to Diego's folder to save Anas's time.
**Before hand-in, copy it to the repository's `docs/AI_METHODS.md`**, where the work plan says it lives.

## How we used AI, in one paragraph

All three of us worked with Claude (Anthropic's AI assistant) throughout, each in our own sessions. Claude wrote
most of the code, ran the analyses, drafted most documents and much of the paper's text, proposed several modelling
choices, and in a few places labelled data. We decided, checked and defended the choices: every one is recorded
with its reason and alternative in `project/DECISIONS.md`. The rule we kept was the course's: **model output is not
a measurement until a person has checked a sample of it**, and "the model said so" is not a method. Most commits
in the repository are authored by Claude on our behalf.

## Where a model produced or changed a number in the paper

| # | Where | What the model did | How it was checked | Result of the check |
|---|---|---|---|---|
| 1 | Name matcher (part 1, all parts) | Claude wrote the rule-based matcher (`Martin/matcher.py`); no model runs inside it | Hand checks by people of what it finds and misses (rows 2, 3 and 4) | See rows 2 to 4 |
| 2 | Matcher precision, first version (D1) | Claude labelled 160 matches of the prototype matcher | Diego read 95 of the 100 random ones and overruled none; 5 were shown wrongly and are marked | 93 of 100 correct (86–97%); 5 of 7 errors cross-party. Led to the fixes in G14 and G18 |
| 3 | Matcher precision, current version (G10) | None: taken from the hand-labelled D2 sample (code "not that member") | Human codes | 98 of 100 |
| 4 | Matcher recall and new rules (G14, G18, G19) | Claude drew the check sheets | Martin read 30 floor turns (recall), 30 untitled names and 20 lists by hand | Recall 12 of 13 (92%); untitled 30 of 30; lists 20 of 20 |
| 5 | Yield rule (G1c) | Claude proposed the phrase rule | Martin hand-coded 30 rows where the two rules disagree | Phrase rule right on 15 of 15; window rule wrong on 14 of 15 |
| 6 | What a mention does (part 2, D2) | Claude was second coder on 50 of 100 mentions; three more Claude runs coded all 100 | Diego coded all 100, Martin and Anas 25 each. Human κ reported separately from AI κ | Humans κ 0.64. Diego–Claude κ 0.72; the extra AI runs agree with each other 99–100%, so they show stability, not correctness |
| 7 | Two codes changed after seeing AI flags (D2) | The AI coders flagged rows 38 and 86 as wrong matches | Diego reread both and agreed; recorded as not independent of the AI | Both were clear matcher errors |
| 8 | Text classifier (D5) | A TF-IDF and logistic-regression model trained on the hand labels | Leave-one-out against the 100 human labels, against a majority baseline | 73% against 72%: not used as a measurement |
| 9 | Press-release recall (A3) | Five blind AI readers (Claude Opus and Sonnet) listed members named in 40 releases | Anas read all 7 cases where readers and matcher differed and agreed with the readers | Reported in `Anas/a3/README.md`; same model family, so not independent |
| 10 | Press-release precision (A3) | Claude resolved rows Anas could not confirm (`resolutions.csv`); three blind AI raters re-read 180 rows | Anas read 30 per rule by hand first | Agreement 179 of 180; own-surname rule rests on Claude's reading (29 of 30), reported as such |
| 11 | District lean, redrawn states (A4) | Claude collected and cross-checked sources | Second sources for every number (The Downballot r = 0.999; official redraw pages) | All nine redraw dates agree |
| 12 | Literature (D3) | Claude found and summarised references | Every reference looked up in Crossref; Westwood read at the publisher | 14 references, all verified to exist; summaries from abstracts, stated as such |
| 13 | Paper text | Claude drafted most sections from our results files | Each owner reads and revises their part; the group reads all of it (S3) | [to fill in after the 25 Nov read-through] |

## What was not checked

- **Speaker attribution** (S2): whether each floor turn is assigned to the right member. 60 turns sampled, not yet
  read. [Diego: fill in when done.]
- **AI coders against each other** add little: the same model agrees with itself almost perfectly. We report AI
  agreement only against human codes.
- **Analysis code** was checked by its results (hand samples, tests in the matcher, reruns that reproduce earlier
  numbers), not by a line-by-line human review of every script.

## Where to look

- Decisions and reasons: `project/DECISIONS.md`
- Matcher checks: `Diego/d1_matcher_precision/`, `Martin/m1_checks_20nov/`, `Martin/m3_yield_check/`
- Labelling: `Diego/d2_labelling/RESULTS.md`, `PROTOCOL.md`
- Classifier: `Diego/d5_classifier/README.md`
- Press-release checks: `Anas/a3/README.md`
