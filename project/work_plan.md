# Work plan: Blocs in the wave

Written 11 November 2026. Hand-in is **Friday 27 November, 23:59**. The plan submits on **Thursday 26
November** and keeps Friday as a buffer only.

**Question.** Is the House Republican party one bloc or several: do the blocs found in the cosponsorship
network also speak differently, and did the 2026 wave hit them equally?

Starting point: `martin_blocs.ipynb` and `martin_blocs.html` (exploration), built on Anas's data and
definitions in `walk_or_talk.ipynb`.

## How we avoid friction

- **One stream per person, one notebook per stream.** Nobody edits another person's notebook, so there are
  no notebook merge conflicts.
- **One shared file joins the streams:** `data/processed/blocs.csv` (member ID, bloc). Martin writes it; the
  text and election notebooks only read it. When it changes, Martin says so in the group chat.
- **Each person writes the Results and Methods paragraphs for their own stream** in Overleaf, in their own
  section, so two people rarely type in the same place.
- **Definitions are fixed before results are looked at again.** Any change after that is written down in
  `docs/AI_METHODS.md` with the date and the reason.
- **Everyone must be able to explain everything.** Each meeting ends with each person explaining someone
  else's method.

| Stream | Owner | Owns |
|---|---|---|
| Network: backbone, blocs, robustness, caucus validation | Martin | `martin_blocs.ipynb`, `blocs.csv`, figure 1 |
| Text: speaker check, word lists, bloc vocabulary | Diego | text notebook, figure or table 2, references |
| Election and data: results, lean, state effects | Anas | `scripts/`, `data/`, election notebook, figure 3, Overleaf file, `AI_METHODS.md` |

Hours outside meetings: Martin and Diego about 8 a week, in evenings and weekends. Anas has more time, so
Anas owns the tasks that others wait for and the final assembly, about 3 hours a week more.

## By Friday 13 November (short tasks that unblock the others)

- **Martin:** write `blocs.csv` from the current notebook and post it. (0.5 h)
- **Anas:** create the Overleaf project from the PNAS template with the section headings and an owner per
  section. (1 h)
- **State check: done on 11 November** (`martin_blocs.ipynb`, section 5). Shuffling results within state,
  bloc explains 17% of running ahead against 16% by chance (p = 0.42). State alone explains 66%. The uneven
  wave is a difference between states, not between blocs, so the election cannot be the headline.
- **Anas:** find out why states differ so much in running ahead. Start with the lean figures for the
  redrawn states, which could produce part of it. (2 h)

## Ready before Wednesday 18 November, 14:00

**Martin (about 8 h)**
- Repeat the bloc detection for the other filter settings and report how much membership moves. Decide
  whether a consensus partition is needed. Fix the final `blocs.csv`.
- Collect membership lists of known caucuses (Freedom Caucus, Problem Solvers, Republican Study Committee,
  Main Street) and measure agreement with the blocs.
- Draft figure 1 (the network with blocs, with the null next to it).
- Half a page of Methods for the network part.

**Diego (about 8 h)**
- Hand-check the 60 sampled speaker turns in `speaker_check_sample.csv` and report the agreement.
- Read the top words per bloc and settle the stop lists. Do this before looking at election numbers.
- Rerun the text check on the final `blocs.csv`, including the different-states version.
- Draft the bloc vocabulary table or figure.
- Read the three core references (Canes-Wrone et al. 2002, Fowler 2006, Gentzkow et al. 2019) and find
  three or four more. Check that Kessler 2017 and Monroe et al. 2008 exist as cited.

**Anas (about 11 h)**
- Fix the two name-matcher gaps (GRIJALVA, PEREZ) in `scripts/roster.py`.
- Check district lean for the nine redrawn states against the Cook Political Report release.
- Rerun the election test with both nulls (lean and state) on the final `blocs.csv`.
- Draft figure 3 (running ahead of the district, by bloc, with the null).
- Start `docs/AI_METHODS.md`: every place a model touched the results and how it was checked.

## During the meeting, Wednesday 18 November, 14:00–17:00

| Time | What |
|---|---|
| 14:00–14:30 | Each person shows one figure and one number: what holds, what broke. Ten minutes each. |
| 14:30–15:15 | Decide the main claim and write it as one sentence. Decide the three figures. The election result did not survive the state check, so the working headline is "blocs exist and speak differently; the uneven wave is explained by state". Confirm or change it here; this decision is final. |
| 15:15–16:15 | Write the outline in Overleaf together: one line per paragraph, with an owner. Write the list of limitations. |
| 16:15–17:00 | Each person explains another person's method at the whiteboard. Note every question nobody could answer. |

Use the course session that morning to ask the teachers whether the main claim is specific enough.

## Ready before Wednesday 25 November, 14:00

A **complete draft** is in Overleaf by **Tuesday 24 November, 20:00**. Everyone reads all of it and leaves
comments before the meeting.

**Martin (about 8 h):** Results and Methods for the network part; figure 1 final at PNAS column width; first
version of the three slides.

**Diego (about 8 h):** Introduction with the literature; Results and Methods for the text part; figure or
table 2 final; reference list checked entry by entry; draft of the half-page reflection.

**Anas (about 11 h):** final results download on **Monday 23 November**, with the date recorded, and all
notebooks rerun on it; Results and Methods for the election part; figure 3 final; Discussion and
limitations; first draft of the Abstract and Significance Statement; `AI_METHODS.md` complete.

## During the meeting, Wednesday 25 November, 14:00–17:00

| Time | What |
|---|---|
| 14:00–15:00 | Read the paper aloud from start to end. Cut to six pages. Resolve every comment. |
| 15:00–15:45 | Number check: one person reads each number in the paper, another finds it in a notebook. Check every caption says what is plotted, the comparison, and what to see. |
| 15:45–16:30 | Rehearse the three-minute talk twice with a timer. Then a question drill: each person answers three questions on a part they did not write. |
| 16:30–17:00 | Write the author contributions. List what is left for Thursday, with an owner for each item. |

Use the course session that morning to show the teachers the main figure.

## Thursday 26 and Friday 27 November

- **Thursday evening:** Anas makes the last edits and exports the three PDFs (paper, slides, reflection).
  Martin and Diego proofread the PDFs (one hour each). **Anas submits on DTU Learn on Thursday.**
- **Friday:** buffer. Nothing is planned.

## Before the presentation, Wednesday 2 December

- Tuesday 1 December, evening: a 30-minute call. Run the talk twice and repeat the question drill.

## What could go wrong

| Risk | What we do |
|---|---|
| The election result is a state effect | Confirmed on 11 November; the paper leads with blocs and vocabulary, and reports the state finding as the answer to the third part of the question |
| Bloc membership changes with the filter setting | Report the range; use a consensus partition; repeat the checks on each setting |
| Lean for redrawn districts is wrong | Report every election number with and without the nine states |
| Results change before hand-in | One final download on 23 November; the date goes in Methods |
| Someone falls behind | Say so in the chat by Sunday evening; Anas takes the task or the group cuts it |
