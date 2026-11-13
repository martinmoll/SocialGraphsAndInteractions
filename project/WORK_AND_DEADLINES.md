# Work and deadlines

**Last updated: Friday 13 November 2026.**

This is the one place that says who does what, how far it is, and what is due when. The question and the
design are in [`README.md`](README.md).

**Keep it current.** Whenever something changes (a task starts, finishes, is blocked, is dropped, changes
owner, or a date moves), update the table, change the date above and add a line to the log at the bottom.
This applies to people and to AI assistants working in the repository.

Status words: **Not started**, **In progress**, **Done**, **Blocked** (say by what), **Dropped**.

---

## 1. Deadlines

| Date | What | State |
|---|---|---|
| Wed 18 Nov, before the meeting | The three shared files exist in a first version (M1, M2, A1), so nobody waits on anybody; matcher precision counted (D1) | Open |
| **Wed 18 Nov, 14:00–17:00** | Group meeting: fix the definitions, confirm owners, outline the paper in Overleaf, ask the teachers (section 4) | Open |
| **Sun 22 Nov** | Numbers frozen. No definition changes after this | Open |
| Mon 23 Nov | Final data download, with the date recorded | Open |
| **Tue 24 Nov, 20:00** | Full draft in Overleaf and a first version of the three slides. Everyone reads all of it | Open |
| **Wed 25 Nov, 14:00–17:00** | Group meeting: read aloud, cut to six pages, number check, rehearse | Open |
| Thu 26 Nov | Submit all three PDFs. Friday is buffer only | Open |
| **Fri 27 Nov, 23:59** | **Hand-in deadline on DTU Learn: paper, slides and reflection, all three** | Open |
| **Wed 2 Dec** | **Presentation:** three minutes with the slides handed in on 27 Nov, then questions to whichever member the teachers pick | Open |

**What is handed in on 27 November, as three PDFs:**

1. **Paper:** PNAS template, at most six pages including figures and references.
2. **Slides:** three pages, no animations. The teachers merge every group's slides into one deck, so the
   slides cannot be changed after the deadline.
3. **Reflection:** half a page, ungraded.

`docs/AI_METHODS.md` must also be in the repository.

---

## 2. Who does what

**Owners are carried over from the split proposed for P1 and adapted to the two-maps design. The group
has not confirmed them. Confirm or change on 18 November.** Hours have not been re-estimated.

### Martin: the two maps (network and nulls)

| # | Task | Delivers | Needs | Status |
|---|---|---|---|---|
| M0 | Prototype of the two maps | `prototype_two_maps.ipynb`, one run | | Done (13 Nov) |
| M1 | Move the name matcher out of the notebook into `scripts/`, so floor speeches and press releases use the same one. First version by Wed 18 Nov, as it is in the notebook. The guard against senators and non-members can follow | One shared matcher | | Not started |
| M2 | Write `mentions.parquet` and `named_ties.csv` from the floor speeches. First version by Wed 18 Nov | The two files in section 3 | M1 | Not started |
| M3 | Fix the definitions for part 1 in writing: how the working map is thinned, whether yields count, bill types | Definitions agreed by the group | 18 Nov meeting | Not started |
| M4 | Harder null: rewire while keeping who spoke in the same debate | A second null for the floor map | M2 | Not started |
| M5 | Louvain communities on each map; overlap with party and between maps (NMI) | Numbers for Results | M3 | Not started |
| M6 | Null for the close-up: of a member's own bills, are the cross-party ones announced more often than a random draw? | The fair baseline (fix 1) | A3 | Not started |
| M7 | Figure 1 (the two maps and their division against the nulls); network part of Results | Figure, text | M3–M5 | Not started |
| M8 | The three slides: question and data; the main figure; what it means and how it was checked. PDF, no animations. **Due with the paper on 27 Nov** | Slides PDF | M7, A4, D2 | Not started |

### Anas: the home text (close-up)

| # | Task | Delivers | Needs | Status |
|---|---|---|---|---|
| A1 | Change the collector to store the full text and the date of every release. It does not match names: the shared matcher (M1) does that. First version by Wed 18 Nov. Starting point: `archive/Anas_Claude/pilot/press_pull.py`; new home `scripts/` | A collector that keeps the text (fix 3) | | Not started |
| A2 | Collect the first 20 Republicans, spread over district lean. Then decide whether to go to about 60 | `data/processed/press_releases.parquet` (first part); go or no-go | A1 | Not started |
| A3 | Match each release to its bill by bill number; mark each named colleague as co-lead or not | Release-to-bill table (fix 1) | A2, M1 | Not started |
| A4 | Showcase ties: which Democrats each Republican names at home. Check the named examples (Roy–Cohen, Biggs–Jayapal, Lawler 1 of 10, Bacon 8 of 10) against full text | Table and figure for the close-up | A3 | Not started |
| A5 | Optional: does a release that says "bipartisan" name a real cross-party partner? | One panel | A3 | Not started |
| A6 | Methods; `docs/AI_METHODS.md`; final data download; final assembly | Text and the required file | Ongoing | Not started |

### Diego: validation and literature

| # | Task | Delivers | Needs | Status |
|---|---|---|---|---|
| D1 | Count the 30 matches printed in the prototype notebook; extend to about 100; report precision | Matcher precision for Methods | | Not started |
| D2 | Labelling protocol for cross-party floor mentions: agreeing, disagreeing or procedural. Draw the sample from `mentions.parquet` | Protocol and sample | M2 for the sample; the protocol can start now | Not started |
| D3 | Read Westwood and Harbridge: three lines on what each found. Settle Westwood's year. Find three or four more references | Note on prior work; reference list | | Not started |
| D4 | Introduction and Discussion; the half-page reflection | Text | D3 | Not started |

### Everyone

| # | Task | Delivers | Status |
|---|---|---|---|
| S1 | Second-code the labelling sample from D2, so every mention has two coders. Report κ | Agreement score for part 2 | Not started |
| S2 | Hand-check the 60 sampled speaker turns in `data/processed/speaker_check_sample.csv` | Agreement rate for Methods | Not started |
| S3 | Read the full draft and comment. Explain out loud one method you did not build | Everyone can answer for the whole paper | Not started |

---

## 3. Working without waiting on each other

Each person has their own notebook and their own script. The streams meet only in three shared files in
`data/processed/`. **The columns below are the agreement.** Anyone can build against them before the file
is complete, and nobody changes a column without saying so in the chat.

| File | Written by | Read by | One row is | Columns |
|---|---|---|---|---|
| `mentions.parquet` | Martin (floor), Anas (press), both with the shared matcher | Diego (D1, D2), Martin, Anas | One mention of a member | `speaker`, `named` (Bioguide IDs), `source` (`floor` or `press`), `date`, `doc_id`, `context` (the sentence), `is_yield` |
| `named_ties.csv` | Martin | Martin, Anas | One pair of members per source | `speaker`, `named`, `source`, `n_mentions` |
| `press_releases.parquet` | Anas | Anas, Martin (M6) | One press release | `bioguide`, `url`, `date`, `title`, `text` |

**Can start today, with nothing from anyone else**

- Martin: M1, M2, then M4 and M5.
- Anas: A1, A2.
- Diego: D1 (the matches are printed in the prototype notebook), D3, the protocol half of D2.
- Everyone: S2.

**The places where one person waits on another**

| Waiting | On | How to keep it short |
|---|---|---|
| Diego's labelling sample (D2) | Martin's `mentions.parquet` (M2) | Martin writes a first version by Wed 18 Nov straight from the prototype. A better matcher later only adds rows |
| Anas's bill matching (A3) | Martin's shared matcher (M1) | Same date. Until then Anas collects text, which needs no matcher |
| Martin's close-up null (M6) | Anas's release-to-bill table (A3) | The latest link in the chain. Martin builds it against the columns above with the 280 sampled releases |
| Martin's definitions (M3) | The 18 Nov meeting | Everything before M5 runs on the prototype's definitions |
| The slides (M8) | One figure from each stream | Each stream delivers its figure by the draft on Tue 24 Nov |

**Two things that cannot be done alone:** the second coding of the labelling sample (S1), and reading
each other's parts (S3).

**The order that matters most:** D2 and S1 decide the headline of part 1 ("less divided" or "talks across
the aisle to argue"). Do them early.

**If the collection fails after A2:** parts 1 and 2 still make a paper. Drop A3–A5 and M6.

---

## 4. Open questions for 18 November

1. **Confirm the owners in section 2.**
2. **Definitions for part 1 (M3):** which thinning rule for the working map; whether yields are in the
   headline number.
3. **Republicans only, or both parties**, in the press-release collection.
4. **Ask the teachers:** does "naming against working", with a hand-labelled sample, count as enough
   language analysis? Is a dataset chosen after the 4 November lock accepted?
5. **Three figures:** proposed are the two maps; what a cross-party mention means; the showcase ties.

---

## 5. No longer needed

From the earlier plans in `archive/`. Listed so nobody keeps working on them.

| Task | From | Why dropped |
|---|---|---|
| 2017–18 kill test | Diego, for directions C and P2 | Those directions were not chosen |
| `blocs.csv`; rerunning pilot 4.3 on backbone blocs; checking pilot 4.1 against the blocs notebook | Martin, pre-meeting tasks | Blocs are not part of the design. They can return as an optional grouping |
| Stop lists and the talk score | Walk or talk | No vocabulary score in the design |
| Redrawn-district lean; state differences in running ahead | Walk or talk; blocs | The election is the setting, not the outcome. Lean is used only to spread the press-release sample |
| Change over time ("the clock"), mutual showing, Democrats in Trump districts, the Trump node | Council options C, E, F, D | Too thin, or need more collection than we have time for |

---

## 6. Log

Newest first. One line per change.

- **13 Nov 2026.** First versions of the shared files (M1, M2, A1) moved from Sun 15 Nov to Wed 18 Nov,
  before the meeting.
- **13 Nov 2026.** Pull request 5 merged to `main`. Slides are due with the paper on 27 Nov, not at the
  presentation: deadlines updated and slides made their own task (M8). Section 3 rewritten: columns of the
  three shared files fixed, first versions due Sun 15 Nov, A1 no longer depends on the matcher.
- **13 Nov 2026.** File created. Direction settled: two maps of Congress as the main question, press
  releases as the close-up, three fixes to the press-release test. Earlier plans moved to `archive/`.
  Prototype M0 done. Owners proposed, not confirmed.
