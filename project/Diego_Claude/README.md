# Diego_Claude: a sharper research question for the midterms project

Written 11 November 2026 by Diego with Claude (AI-assisted, see "How this was made" below).
Nothing here changes anyone else's files. Martin's `work_plan.md` and `martin_blocs.ipynb` and the
`walk_or_talk.ipynb` prototype are untouched.

## Read in this order

| File | What it is | Time to read |
|---|---|---|
| `README.md` | This page: the recommendation in one screen | 3 min |
| `01_research_questions.md` | The recommended question, five alternatives, honest pros and cons, data checked, expected score | 10 min |
| `02_pilot_findings.md` | Numbers from a one-evening pilot on our existing data, with what they do and do not show | 8 min |
| `03_plan_if_chosen.md` | Measurements, checks, figures and kill tests for the recommended question. The division of labour is written only after the group picks | 5 min |
| `pilot/pilot_distancing.py` | Reproduces every number in `02`. Run from `project/`: `python Diego_Claude/pilot/pilot_distancing.py` | |
| `pilot/billstatus115_sample.js` | The 2017-18 baseline sample (browser console on govinfo.gov) | |

## The recommendation

**Research question.** As Trump became unpopular in 2025-26, did House Republicans distance themselves
from him, in what they said on the floor and in whom they cosponsored with, more than they did in his
first term (2017-18), and who led the distancing: the swing-seat members facing the wave, or the party's
hardline wing?

Short title: **Running from Trump?**

Why this one:

1. **It is the question a reader actually has after 3 November.** Democrats won the House 255 to 168 with
   97.2% of races declared (Wikipedia, 11 Nov 2026), and Trump's approval stood at 34.0% to 39.0% across
   aggregators on 1 Nov 2026. "Did his own party see it coming and run?" is the obvious human question,
   and the answer is not obvious (see 2).
2. **The pilot already shows a non-obvious pattern.** Republicans on the House floor said "Trump" 13.94
   times per 10,000 words in the first half of 2025 and 4.92 times in the second half of 2026. The share
   of active Republicans who name him at least once per 1,000 words fell from 33% to 6%. At the same time
   their cross-party cosponsorship rose from 9.0% to about 20%. But the members who went quiet are not the
   members who crossed over (Spearman 0.06), and the quiet ones lean to the hardline wing, not the swing
   seats. Words and deeds came apart. That is a story.
3. **It has a built-in control, which is what the course grades hardest.** 2017-18 was Trump's first
   term, a Republican House and a Democratic midterm wave. Same president, same majority, same outcome.
   If Republicans also drifted in 2017-18, our 2025-26 result is "normal Congress cycle", and we will
   know it. A pilot sample of 2017-18 already shows that part of the cosponsorship rise is normal
   (8.0% in 2017Q1 to 12-17% later), so this check is not decoration: it decides the claim.
4. **It reuses almost everything we already have.** Same speeches, bills, cosponsors, members and
   results tables. The only new data is the 115th Congress (2017-18), from the same govinfo sources and
   scripts, verified reachable on 11 Nov 2026.
5. **It covers both halves of the course properly.** Network: cross-party cosponsorship over time with a
   label-shuffle null, party-split modularity per period, and Martin's blocs as the "who". Text: word
   rates over time, the week-6 two-group comparison per period, and a hand-labelled stance sample (week 7).
6. **It does not depend on the election link, which is weak in every version we tried.** Martin's own
   state check shows state explains 66% of running ahead and blocs add nothing within states (p = 0.42).
   In this question the election is the backdrop plus one honest secondary test.

Expected score, honestly: **2 if executed cleanly, 3 possible** if the 2017-18 comparison is clear, the
stance hand-label agrees, and the figures are tight. It is **not** a 3 by default. The two current
questions are, in our judgement, a 1-2 (walk or talk) and a 2 at best (blocs), mainly because the question
category is weak. Details and the full scrutiny are in `01_research_questions.md`.

**The kill test** is Sunday 15 November: if 2017-18 shows the same drop in Trump mentions and the same rise
in cross-party cosponsorship, the headline becomes "this is what every Republican House does before a bad
midterm". That is still a valid paper but a weaker one, and the group should decide on Wednesday 18
November whether to keep it.

## What the group needs to decide

1. Which question (this one, blocs, walk or talk, or another from `01`).
2. Once picked: Claude writes the division of labour for three people, built on Martin's existing
   `work_plan.md` structure (one stream per person, one shared file, nobody edits another's notebook),
   with what must be ready before each Wednesday meeting (18 and 25 November, 14:00-17:00) and what gets
   done in the room.

## How this was made

Claude (Anthropic) read the course's week 8 page live on 11 Nov 2026, the whole `project/` folder, and ran
the pilot on `data/processed/`. The 2017-18 sample and the election and approval figures were fetched in a
browser on 11 Nov 2026. Every number here comes from `pilot/` or a named page. Nothing has been hand-checked
by a human yet, and the stance of Trump mentions has not been read at all: that is the first check in `03`.
