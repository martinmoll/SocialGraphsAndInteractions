# Report skeleton: what goes where

Diego Mijares with Claude, 18 November 2026. A plan for the paper, the reflection and the slides, not
text. For the group to change at the meeting. Task ids are those of `../WORK_AND_DEADLINES.md`.

**Headline after D2 (18 Nov):** cross-party floor mentions are mostly agreeing (69%: thanks, credit,
partnership) and rarely disagreeing (7%). So the floor map is less divided because members credit
colleagues across the aisle, not because they argue with them. Write every section to this reading; the
"talk across the aisle to argue" version is out. Numbers in `d2_labelling/RESULTS.md`.

**Hand-in, Fri 27 Nov 23:59 on DTU Learn, three PDFs:** paper (PNAS LaTeX template, at most 6 pages
including figures and references), slides (3-page PDF, no animations), reflection (ungraded, about half a
page, one page at most). `docs/AI_METHODS.md` must be in the repository.

**Course rules that shape the paper:** sections are Abstract, Significance Statement, Introduction,
Results, Discussion, Methods, References, Author contributions. Abstract 150 words. Captions readable on
their own. Methods states for the data what, from where, collected when, how many. Every number a model
produced is checked on examples we read ourselves, with agreement reported. Author contributions specific.

## Page budget

| Part | Pages | Owner of the text |
|---|---|---|
| Title, abstract, significance statement | 0.5 | Diego (drafts), all |
| Introduction | 0.75 | Diego (D4) |
| Results, including Figures 1 to 3 | 2.25 | Martin (part 1), Diego (part 2), Anas (part 3) |
| Discussion, with limitations | 0.75 | Diego (D4) |
| Methods, including data | 1.25 | Anas (A6) assembles; each writes their own part |
| References and author contributions | 0.5 | Diego (D3), Anas |
| **Total** | **6** | |

Figures take about 1.25 of the 2.25 Results pages. If the close-up is dropped (plan B in the work file),
its half page goes to Results part 1.

---

## Abstract (150 words) and significance statement (120 words)

- One sentence each: the question; the two maps on the same 450 members; the main number at equal density
  (floor against working cross-party share, M3/M5); what the hand labels say (D2); what the classifier
  adds (D5); the close-up in one clause (A4); the one-line meaning.
- Significance statement: why it matters that division depends on which record is read, for readers
  outside network science. No numbers beyond one.
- Written last, after the freeze on Sun 22 Nov.

## Introduction (0.75 page)

- Congress looks divided whatever is measured: votes, words (Gentzkow et al. 2019), cosponsorship networks
  (Neal 2020).
- But the level depends on the record: votes against cosponsorship (Harbridge 2015); communication venues
  (Green et al. 2024).
- Members manage how divided they look: bipartisan image pays with some voters (Harbridge and Malhotra
  2011); the word "bipartisan" is detached from votes (Westwood 2022).
- Our step: names, not words. Two networks on identical nodes, compared with the same measure against
  rewired nulls. Novelty only as "to our knowledge" (D3).
- Why the answer is not obvious: attack in public and cooperate quietly, or display the few partners.
- One-sentence preview of the answer.
- Cites: all of `references.bib` except the method references.

## Results (2.25 pages)

**Part 1: two maps (about 1 page with Figure 1). Owner Martin, M3 to M5, M7.**
- Floor map and working map: ties, cross-party share, party modularity against the degree-preserving null.
- The fair comparison as the group decides in M3: random working ties at equal size and the strongest ties;
  a curve of cross-party share against ties kept would show the thinning choice openly.
- The harder null that keeps who spoke in the same debate (M4): how much of the floor map's division
  survives it.
- Louvain communities on each map and their overlap with party (NMI), M5.
- Yields in or out (M3), one sentence.
- **Figure 1** (Martin, M7): the two maps side by side at equal size, and division against both nulls.

**Part 2: what a mention means (about 0.75 page with Figure 2). Owner Diego, D2 and D5.**
- Shares of procedure, agreeing, disagreeing, neutral and wrong-person among cross-party and same-party
  mentions, hand labels, with intervals (D2).
- Agreement: Diego against Martin, against Anas, against Claude, reported separately (S1).
- Classifier (D5): 73% against 72% for always "agreeing", 0 of 5 disagreements found. It does not earn a
  place as a measurement; one sentence saying so, as the check.
- The headline part 2 allows: cross-party mentions are mostly credit (69% agreeing, 7% disagreeing), so
  "less divided" stands and "talks across the aisle to argue" is out.
- **Figure 2** (Diego, D2): shares by code with intervals, cross-party against same-party, from the hand
  labels. The classifier is not in the figure.

**Part 3: close-up (about 0.5 page with Figure 3). Owner Anas, A3 to A4, with M6.**
- Which Democrats Republicans name at home, against their own bills as the baseline (M6).
- Named examples checked against full text (A4).
- **Figure 3** (Anas, A4): the showcase ties. Dropped if the collection stops after A2.

## Discussion (0.75 page)

- What the result means, in one paragraph, read through part 2.
- What it does not mean: a mention is not cooperation; floor procedure gives each debate a manager from each
  party (answered by M4); the comparison depends on how the working map is thinned (M3).
- **Limitations we found ourselves:** matcher precision 93% (86 to 97%) on the prototype matcher, errors
  biased towards cross-party ties, recall unmeasured (D1); a small labelled sample and how far the
  classifier can carry it (D2, D5); one Congress, one chamber; the floor is not voter-facing.
- Link back to Westwood: words against named partners.
- What would extend it: other Congresses, signed ties throughout.

## Methods (1.25 pages)

- **Data** (Anas assembles; sources from `README.md` section 7): members (Voteview, congress-legislators);
  bills and cosponsors (govinfo BILLSTATUS); House floor turns of 50 words or more from the Congressional
  Record (govinfo), 6 Jan 2025 to 9 Nov 2026, downloaded 11 Nov 2026, 17,824 turns; press releases (A2:
  members, dates, count). What, from where, when, how many for each.
- **Networks** (Martin): tie definitions, thinning, modularity, the two nulls, Louvain.
- **Name matching** (Martin, with D1): the rule; precision 93% on 100 mentions labelled by an AI assistant
  and read by a group member; error types; the fixes in the current matcher.
- **Labelling** (Diego, D2): 100 mentions, 75 cross-party, party hidden, five codes, rules fixed in advance,
  second coders, κ.
- **Classifier** (Diego, D5): TF-IDF on words and word pairs, surname masked, weighted logistic regression,
  leave-one-out against the hand labels.
- **Press releases** (Anas): collection, matching to bills by number.
- **AI use**: one sentence pointing to `AI_METHODS.md`.

## References and author contributions (0.5 page)

- References from `references.bib` (D3) plus Martin's method references (disparity filter, rewiring,
  modularity, Louvain). About 12 to 15 entries.
- Author contributions, one line per person, specific: who built which map and null, who collected, who
  matched, who labelled which rows, who built the classifier, who wrote which section. Plus one line on the
  AI assistant.

---

## Reflection (separate PDF, about half a page, ungraded)

- The course's question: did the "From an AI-drafted report" boxes change how we read our own draft, and
  where did we use them or not? "They did not help" is an accepted answer.
- Where they bit: the week 8 box (a number with no null) against our nulls and size-matched comparison; the
  week 7 box (names that are not resolved entities) against our matcher check, where the printed matches
  looked right and counting showed otherwise.
- Where we did not use them: to be filled in after reading the full draft on Tue 24 Nov.
- One closing line in the group's own words.

## Slides (3 pages, handed in with the paper; Martin, M8)

1. **Question and data.** Two maps of the same House; one line each on the two records; the 450 members.
2. **The main figure.** Figure 1, or a single cleaner version of it, with the headline number in large
   type.
3. **What it means and how we checked it.** The part 2 result in one line (what cross-party mentions do);
   the checks in three short lines: the two nulls, the hand labels with κ, the matcher's precision.

Three minutes in all, then questions to any of us: everyone must be able to explain every part.
