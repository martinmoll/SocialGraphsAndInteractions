# Martin's direction: Blocs in the wave

Written 11 November 2026 by Martin.

**This is one proposed direction, not the plan for the project.** It covers the question I explored and the
work that would follow from it. Anas and Diego may bring their own directions. Nothing here is agreed by the
group, and no task below is assigned to anyone until the group chooses.

The file has three parts, so that pieces can be taken or left:

1. **The direction:** the question, what the exploration found, and what is open.
2. **Work modules:** self-contained pieces of work. Each one says what it needs and what it delivers, so a
   module can be used in this direction, moved into another direction, or dropped.
3. **A frame for any direction:** dates and a meeting format that do not depend on which direction wins.

---

## 1. The direction

**Question.** Is the House Republican party one bloc or several: do the blocs found in the cosponsorship
network also speak differently, and did the 2026 wave hit them equally?

**Where it stands** (`martin_blocs.ipynb`, shown in `martin_blocs.html`; built on Anas's data and
definitions in `walk_or_talk.ipynb`):

| Part of the question | Finding on 11 November | How solid |
|---|---|---|
| Are there blocs? | 11 blocs; modularity 0.53 against 0.36 for rewired networks | Real as a pattern. Membership moves when the filter setting changes |
| What are they? | Partly ideology (35% explained), partly state delegations | Solid |
| Do they speak differently? | Yes, also between members from different states (p < 0.001) | Solid for one setting; not repeated on others |
| Did the wave hit them equally? | No more than chance once results stay inside their state (p = 0.42). State alone explains 66% | A negative result. The test has limited power |

**What this direction can claim today:** blocs exist and speak differently; the uneven wave is a difference
between states, not between blocs.

**What speaks against it**

- The election, which is the reason for the topic, ends as a negative result.
- Bloc membership depends on a setting we chose.
- Why states differ so much in running ahead is not explained.

**How it could combine with other directions**

- The bloc assignments are a member-level label. Any other direction can use them as a grouping, for
  example to compare how blocs talked about one event over time.
- The state finding stands on its own and may matter to any direction that uses the election result.
- The network part can serve as the network half of a direction whose main interest is text.

---

## 2. Work modules

Sizes are rough hours. "Needs" lists what must exist first. No owners are set.

| Module | What it does | Needs | Delivers | Size | Useful outside this direction? |
|---|---|---|---|---|---|
| **N1 Bloc file** | Write the bloc of every member to `data/processed/blocs.csv` | `martin_blocs.ipynb` | One shared file other notebooks read | 0.5 h | Yes: a grouping any direction can use |
| **N2 Bloc robustness** | Repeat detection for other filter settings; decide on a consensus partition | N1 | Final bloc file; a number for how much membership moves | 4 h | Only if blocs are used |
| **N3 Caucus validation** | Collect lists of known caucuses and measure agreement with the blocs | N1 | An outside check of the blocs | 3 h | Only if blocs are used |
| **T1 Speaker check** | Hand-check the 60 sampled speaker turns | Nothing | Agreement rate for Methods | 1.5 h | Yes: every direction that uses the speeches |
| **T2 Stop lists** | Read the top words and settle the stop lists | Nothing | Fixed vocabulary | 2 h | Yes: every direction that uses the speeches |
| **T3 Bloc vocabulary** | Rerun the text check on the final blocs; table of bloc words | N2, T2 | Text result and figure | 3 h | Only if blocs are used |
| **E1 Data fixes** | Fix the two name-matcher gaps; final results download with the date | Nothing | Clean, dated data | 3 h | Yes: every direction |
| **E2 Redrawn lean** | Check district lean in the nine redrawn states against the Cook release | Nothing | Verified lean, or a list of districts to drop | 3 h | Yes: every direction that uses the election |
| **E3 State differences** | Find out why states differ so much in running ahead | E2 | An explanation, or a stated limit | 3 h | Yes: every direction that uses the election |
| **E4 Election by bloc** | Rerun the election test with both nulls on the final blocs | N2, E2 | Election result and figure | 2 h | Only if blocs are used |
| **W1 Paper** | Introduction, Results, Methods, Discussion, Abstract in Overleaf | The modules above | Six pages | 15 h | The section owners change with the direction |
| **W2 Slides and reflection** | Three slides; half-page reflection | W1 | Two PDFs | 3 h | Yes |
| **W3 AI methods file** | `docs/AI_METHODS.md`: every place a model touched the results and how it was checked | Ongoing | Required file | 2 h | Yes: required for any direction |

**Modules worth doing whatever the group chooses:** T1, T2, E1, E2, W3. They cost about 12 hours and no
direction can skip them.

**If the group takes this direction, a possible split** (about 8 hours a week for Martin and Diego, more
for Anas; this is a suggestion to discuss):

| Stream | Modules | Suggested owner |
|---|---|---|
| Network | N1, N2, N3, network part of W1, slides | Martin |
| Text | T1, T2, T3, Introduction and references, reflection | Diego |
| Election and data | E1, E2, E3, E4, Discussion and Abstract, W3, final assembly | Anas |

One stream per person and one notebook per stream, joined only by the bloc file, so nobody edits another
person's notebook.

---

## 3. A frame for any direction

These follow from the course dates, not from this direction. They are a suggestion for the group.

**Dates**

- Wednesday 18 November, 14:00–17:00: meeting.
- Wednesday 25 November, 14:00–17:00: meeting.
- Friday 27 November, 23:59: hand-in. Aim to submit on Thursday 26 November and keep Friday as a buffer.
- Wednesday 2 December: presentation.

**Before 18 November:** each person brings their direction in a form the others can judge: the question in
one sentence, one figure, and what speaks against it. The modules marked "whatever the group chooses" can
start now.

**During 18 November**

| Time | What |
|---|---|
| 14:00–14:45 | Each person presents their direction. Fifteen minutes each, including questions. |
| 14:45–15:30 | Choose one direction, or combine parts. Write the main claim as one sentence and choose the three figures. This decision is final. |
| 15:30–16:15 | Outline the paper in Overleaf: one line per paragraph, with an owner. Assign the modules. |
| 16:15–17:00 | Each person explains a method they did not build. Note every question nobody could answer. |

**Before 25 November:** a complete draft in Overleaf by Tuesday 24 November, 20:00. Everyone reads all of
it and leaves comments. Final results download on Monday 23 November.

**During 25 November**

| Time | What |
|---|---|
| 14:00–15:00 | Read the paper aloud. Cut to six pages. Resolve every comment. |
| 15:00–15:45 | Number check: one person reads each number, another finds it in a notebook. Check every caption. |
| 15:45–16:30 | Rehearse the three-minute talk twice with a timer. Question drill on parts each person did not write. |
| 16:30–17:00 | Write the author contributions. List what is left for Thursday, with an owner for each item. |

**Rules that reduce friction in any direction**

- Fix definitions before looking at results again. Record any later change in `docs/AI_METHODS.md`.
- Nobody edits another person's notebook. Shared inputs are files in `data/processed/`.
- If someone falls behind, they say so in the chat by Sunday evening.
