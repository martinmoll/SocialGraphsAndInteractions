# Where Anas stands, and proposed revisions to parts 1 to 3

Anas, Thursday 19 November 2026. **Proposals, not decisions.** Parts 1 and 2 belong to Martin and Diego, who
decide on anything in them. Agreed changes go into `DECISIONS.md` before the freeze on Sun 22 Nov (G7).

## Where I stand

| Done (in this folder) | Not started |
|---|---|
| Press-release scope scan, both parties (`press_scope/`), rechecked 19 Nov | A1 collector: first build tonight or tomorrow |
| Matcher checklist for Martin (`MATCHER_CHECKLIST.md`) | A2 to A6 |
| Seats per state, exposure and redrawn states (`state_seats/`) | `docs/AI_METHODS.md` |
| Proposal and pilot for a state null (`state_null/`) | |
| Glossary of every term we use (`dictionary.md`) | |
| S1: second coding of D2 rows 76 to 100 (κ 0.69 with Diego), in Diego's folder | |

Not in the repo yet: the G13 decision text (Democrats included, small), drafted on my computer. I will paste it
into `DECISIONS.md` with GitHub's editor.

### Checked on 19 Nov

- Repo: no commits since 18 Nov 11:11.
- Members: the official current list (`unitedstates/congress-legislators`) has 439 representatives, our 433
  plus the 6 delegates. Nobody joined or left since our download on 11 Nov. FL-20 and TX-23 are still vacant.
- Press sites: of the 31 sites the scan could not count, 6 answer the WordPress API (Crane, Himes, Nunn,
  Goodlander, Jeffries, Jayapal), so their full text can be collected. 3 exposed Democrats (Budzinski,
  Gottheimer, Gluesenkamp Perez) use a newer site layout with a "See More" button; I will leave them out of the
  first rounds and say so in Methods.
- The api-anything catalog still has nothing for house.gov.
- Correction: 21 exposed Democrats and **10** (not 12) exposed Republicans in redrawn states, among the members
  whose releases could be counted. Fixed in `press_scope/README.md` and in the G13 draft.

## Where each new layer goes

| Layer | Part 1 (two maps) | Part 2 (what a mention means) | Part 3 (close-up) |
|---|---|---|---|
| Democrats as a comparison | Already in: both maps include all members | Already in: labels cover both directions | **New (G13):** exposed against safe within each party; mutual showing |
| Exposure (district lean, safe or exposed) | No | No | **Yes, the core comparison** |
| State membership | **Optional:** one robustness row, the state null, if Martin wants it | No | **Yes, as checks:** sample spread over states, leave one state out, same-state names marked |
| Seats per state | No | No | Context for the sample and Methods |
| Redrawn states | No | No | **Yes:** the swing-seat rule uses the old district |

## Part 1: the two maps (Martin)

**Proposed: one optional robustness row, a null that keeps members' own states.** Details, the pilot and a
drop-in function in [`state_null/`](state_null/README.md).

- **Why:** many state delegations are mostly one party, so ties inside a state could look like party division.
  Same-state ties are over-represented (floor 9.0% against 3.7% by chance; working 6.7% against 4.3%). The pilot
  says this explains almost none of the division: party Q under the state null is about 0.005, against 0.210
  (working) and 0.111 (floor). So it would be one row and one sentence that answers a likely objection.
- **Not proposed:** exposure in part 1. Floor speeches and cosponsorship are public too (C-SPAN, the Record,
  bill pages), so exposure could matter there, but adding it now would be a new question after seeing
  results, on six pages.
- **Unchanged:** M1 to M8 as in the work plan; the matcher (decisions in `MATCHER_CHECKLIST.md` are Martin's);
  G1a to G1c, G12; the plain and the debate null; Figure 1; the slides.

## Part 2: what a mention means (Diego)

**Proposed: nothing.**

- **Why:** the labelling is done, and 75 cross-party rows split by exposure or state would leave groups of 10 to
  15, too few to say anything.
- **Unchanged:** D1 to D5, the protocol, the κ results, the D5 decision, the drafts.

## Part 3: the close-up (Anas)

Half a page and Figure 3, as in the report skeleton. The two maps stay the headline. G5 still applies: no press
data for the first 20 members means no close-up, Democrats included.

| Task | Before | Revised | Why |
|---|---|---|---|
| **A1** Collector | Change the pilot collector to keep full text and date | Same output (`bioguide, url, date, title, text`). Built on the scope scan: listing discovery and the pagers for the four layouts from `probe2.py`, the WordPress API where a site has it, a stop when a page repeats, and dates far from the page's median ignored | The scope scan found the layouts, and the two bugs the old approach would hit |
| **A2** First 20, then about 60 | 20 Republicans spread over lean | **Both parties**, proposed 12 R and 8 D, exposed and safe in each; **spread over states**; one **common date window**; exposed members in redrawn states labelled by their old district | G13; 27 R against 5 D sites stopped posting; California and New York could dominate a sample drawn by exposure alone (`state_seats/`) |
| **A3** Release to bill; co-lead marks | Match by bill number; mark named colleagues co-lead or not | Same, plus a mark for **same state** and the **party** of each named member. The press side uses the list rule ("Reps. A, B and C") and the untitled full-name rule, whatever is decided for the floor | `MATCHER_CHECKLIST.md` items 1 and 2; `state_seats/` |
| **A4** Figure 3 and text | Which Democrats Republicans name at home; check Roy–Cohen, Biggs–Jayapal, Lawler 1 of 10, Bacon 8 of 10 | (Exposed − safe) **within each party**, compared between parties: seat or party. Shares **per member**, not pooled over releases. Democrats as one panel or one paragraph. Mutual pairs if the data has them. Check without each large state. Worded "consistent with", never "because" | G13; parties publish at different rates and differ in majority status, so their levels can't be compared directly; one state should not carry the result |
| **A5** "Bipartisan" | Optional | Still optional. If there is room: a short list of partnership phrases counted per release (word-list method, week 7) | |
| **A6** Methods, AI file, download | Data paragraph, `docs/AI_METHODS.md`, final download Mon 23 Nov | Also in Methods: 435 seats, 6 delegates, 2 vacancies; the exposed-seat rule and the redrawn-state fix; the date window; who could not be collected and why. Definitions can come from `dictionary.md` | Roster check; scope scan; recheck |

**Unchanged in part 3:** the question (whom members show at home); the shared columns of
`press_releases.parquet` and `mentions.parquet` (`source = press`); Martin's matcher as the one name finder;
M6, the null on members' own bills (Martin); the four named examples to check; the page budget.

### Open, to settle before A2

| Decision | Proposal |
|---|---|
| Swing-seat definition | Lean within 5 points, or leaning to the other party; old district in redrawn states |
| The first 20 | 12 R and 8 D, exposed and safe in each, spread over states |
| Date window | 3 Jan 2025 to a cutoff before the summer drop-off in posting |
| Same-state names | A check only, reported if it changes the result |

## What I need from you

- **Martin:** a yes or no on the state null (`state_null/`), and the matcher items (`MATCHER_CHECKLIST.md`),
  ideally before Sun 22 Nov.
- **Both:** objections to the three open decisions above, before I collect the first 20.
