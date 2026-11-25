# Two maps of Congress

Final project in **02805 Social Graphs and Interactions** (DTU, autumn 2026).
Group: Anas Mir, Martin Møllenhus, Diego A. Mijares.

**Status (25 November 2026): the analysis is closed.** Every number is frozen (since 22 Nov) and no new analyses are
added; we write, cut and rehearse. The paper is in [`report/`](report/README.md): hand-in Fri 27 Nov (paper,
slides, reflection), presentation Wed 2 Dec. This file describes the project as it ended; the design as chosen on
13 Nov and the prototype are in the git history and [`archive/`](archive/README.md).

- **Each part, its numbers and what to say if asked:** [`Martin/README.md`](Martin/README.md) (part 1),
  [`Diego/README.md`](Diego/README.md) (part 2), [`Anas/README.md`](Anas/README.md) (part 3)
- **Who does what, and the log of every change:** [`WORK_AND_DEADLINES.md`](WORK_AND_DEADLINES.md)
- **Every decision, its reason and the alternative:** [`DECISIONS.md`](DECISIONS.md)
- **Every term we use, in plain words** (final versions of all three parts, 25 Nov): [`DICTIONARY.md`](DICTIONARY.md)
- **Methods from outside the course**, with references and why each fits: [`OFF_CURRICULUM.md`](OFF_CURRICULUM.md)
- **Where a model touched the results, and how it was checked:** [`Diego/AI_METHODS.md`](Diego/AI_METHODS.md)
  (copied to `docs/AI_METHODS.md` before hand-in)
- **How we got here** (earlier questions, ratings, the review, pilots): [`archive/`](archive/README.md)

---

## 1. The question, and the answer

**Is the Congress that members *talk about* more or less divided by party than the Congress that *works
together*?**

We draw the US House of Representatives (119th Congress, 2025–26) as networks on the same members and measure how
strongly each drawing splits into a Republican side and a Democratic side.

**Answer:** less divided. At equal size, 38.7% of floor ties cross the party line against 28.6% of working ties.
Both maps are far more divided than chance; debate procedure explains about two thirds of the floor map's
division, and its communities follow committees, not parties. Cross-party mentions are mostly thanks and credit
(69%) and rarely disagreement (7%). At home, in press releases, members in exposed seats name the other party more
often than members in safe seats, in both parties, and mostly name partners; the seat cannot be separated from the
members' ideology. How divided Congress looks depends on which record is read.

## 2. The three networks

| Map | Two members are tied if | Members | Ties | Source |
|---|---|---|---|---|
| **Working map** | one cosponsored a bill or joint resolution the other sponsored | 450 R and D | 46,513 | govinfo BILLSTATUS |
| **Floor map** | one named the other in a House floor speech (yields of debate time left out) | 450 R and D | 3,970, from 8,469 mentions | Congressional Record (govinfo) |
| **Home map** | one named the other in a press release (part 3) | 406 with ≥ 10 releases | 6,765 cross-party | Members' `house.gov` sites, 55,023 releases |

The working and floor maps are the paper's headline (part 1). The home map belongs to the close-up (part 3).

## 3. The parts of the paper

| Part | Owner | Question | Result | Main check |
|---|---|---|---|---|
| **1. Two maps** | Martin | Is the floor map less divided than the working map? | Yes: 38.7% against 28.6% cross-party (200 random working draws of the same size); Q 0.112 against 0.211 | Degree-preserving rewiring; a debate null (two thirds of the division is procedure); a state null (almost none is geography); communities against committees |
| **2. What a mention means** | Diego | Are cross-party mentions praise, attack or procedure? | 69% agreeing, 23% neutral, 7% disagreeing, none procedure | 100 mentions hand-coded, two coders, κ 0.64; a text classifier failed to beat the baseline and is not used |
| **3. Close-up at home** | Anas | Do members in exposed seats name the other party more in their press releases? | Yes, in both parties (R 13.3% against 9.2%, D 11.6% against 9.0%); the parties differ in how they bridge in the home map and in backing "bipartisan" with a partner | Every check fixed in advance holds; 77% of counted names are partners (check T); seat and ideology cannot be separated (check I) |
| **Close-up null (M6)** | Martin | Do members announce their cross-party bills more than their other bills? | A little: 52.7% against 45.1%, mostly because co-led bills are announced more | Within-member shuffle of which bills are cross-party |
| **Introduction, Discussion** | Diego and Martin | | | |
| **Methods** | each for their part | | | |

Figures: Figure 1, the two maps (Martin); Figure 2, what mentions do (Diego); Figure 3, naming by district lean
(Anas).

## 4. What each measurement captures and misses

- **A working tie** captures whom a member puts their name next to. It misses informal cooperation and why
  they signed.
- **A floor mention** captures that one member named another in Washington. Part 2 reads what it does; yields
  of debate time are procedure and are left out. Much of it follows the debate's cast and the committee system.
- **A press-release mention** captures whom a member chooses to name to voters and the press. It misses
  newsletters, ads and social media. We say "name", not "praise": tone is measured on a sample (check T).
- **Party modularity** captures how much more ties stay inside a party than chance predicts. It depends on
  density, so maps are compared at the same number of ties.
- **The matcher** decides all three maps. Precision 98 of 100 (floor) and 0.96 (press); recall 12 of 13 (floor)
  and 0.97 (press).

## 5. From the prototype to the paper

The 13 Nov prototype (`prototype_two_maps.ipynb`, one run) already showed the floor map less divided at the same
size (38% against 12% for the strongest working ties). It was not a result yet. Each objection then is now checked:

| Objection on 13 Nov | What we did | Outcome |
|---|---|---|
| Naming is not cooperating; tone unmeasured | Part 2 (floor) and check T (press) | Mostly credit and partners, rarely attack |
| The gap depends on how the working map is thinned | Random draws of the same size as headline (G1a); strongest ties as a second comparison | The gap holds (10.1 points); strongest ties are more partisan still |
| The matcher is not validated | Precision and recall measured on both sources; fixes G14, G18, G19 | Precision 0.96 to 0.98, recall 0.92 to 0.97 |
| The rewired null ignores the debate structure | Debate null (M4) | Explains about two thirds, not all |
| The floor is not voter-facing; no home map | 55,023 press releases collected (A1) | Part 3 and the home map |
| A fair baseline for the close-up | Releases matched to bills, co-leads marked (A3); M6 | Co-leads left out of the part 3 outcome |

The three things that would have made us change course did not happen: cross-party floor mentions are not mostly
procedure or wrong matches, the gap survives fair thinning and the harder null, and press releases name colleagues
well beyond the leaders.

## 6. Limits we found ourselves

- A mention is a reference, not cooperation, and House procedure brings both parties into the same debates.
- The thinning rule sets the size of the gap (ten points against random ties, much more against the strongest).
- Matcher errors tend to join members of different parties, pushing the floor map towards looking less divided;
  at 98% precision the effect is small.
- 100 hand labels give wide intervals and too few disagreements for a classifier.
- Exposed members are also their party's moderates; the seat and ideology cannot be separated.
- One Congress, one chamber.

## 7. Data

All tables are keyed by **Bioguide ID**.

| Table | Rows | What it holds | Source, date |
|---|---|---|---|
| `data/processed/members.csv` | 451 | Member, party (226 R, 224 D, 1 I), state, district, DW-NOMINATE | Voteview; unitedstates/congress-legislators (11 Nov 2026) |
| `data/processed/bills.parquet` | 12,987 | Bill, type, sponsor, date, policy area, title | govinfo BILLSTATUS (11 Nov) |
| `data/processed/cosponsors.parquet` | 149,015 | Bill, cosponsor, date, original, withdrawn | govinfo BILLSTATUS (11 Nov) |
| `data/processed/speeches.parquet` | 35,629 | Speaker turn, 6 Jan 2025 to 9 Nov 2026 (17,824 kept: House floor, ≥ 50 words) | Congressional Record, govinfo (11 Nov) |
| `data/processed/districts.csv`, `incumbents.csv` | 435 | 2026 district lean, 2026 result, incumbent | NBC News results feed; Wikipedia |
| `Martin/mentions.parquet`, `named_ties.csv` | 9,988; 5,400 | Floor mentions with context and yield flag; directed pairs | Martin's matcher (M1, M2) |
| `Anas/press_releases/` (three parts) | 55,023 | Press releases, full text and date, 3 Jan 2025 to 20 Nov 2026 | Members' `house.gov` sites (snapshot 20 Nov) |
| `Anas/district_lean/member_lean.csv` | one per member | Lean of the district served (Cook PVI 2025), 2026 district run in, 2024 presidential margin | Wikipedia revision of 25 May 2025; The Downballot |
| `Anas/a3/out/mentions_press.parquet` | 129,473 | Press mentions with flags (co-lead, leader, caucus, ...) and 1/n weights | Martin's matcher plus the press layer (A3) |
| `Martin/m5_committees/` | | Current House committee assignments | unitedstates/congress-legislators (22 Nov) |

The speaker assignment was checked by hand (S2: 60 of 60 right). The 2026 election counts are unofficial.

## 8. Folder layout

```
project/
  README.md                  this file: the question, the answer, where everything is
  WORK_AND_DEADLINES.md      who does what, dates, and the log of every change
  DECISIONS.md               every decision with its reason and alternative (G1–G20)
  DICTIONARY.md              every term, in plain words
  OFF_CURRICULUM.md          methods from outside the course, with references
  Martin/                    part 1: matcher, floor mentions, the two maps, nulls, communities, Figure 1, M6
  Diego/                     part 2: precision, labelling, classifier, literature, Introduction and Discussion
                             drafts, speaker check, AI_METHODS.md, reflection draft
  Anas/                      part 3: press releases, district lean, names and bills, the close-up, home map, A5
  report/                    the paper (PNAS, for Overleaf), figures, references, slides
  scripts/                   01–04 download and parse the data; roster.py is the member list
  data/processed/            the shared tables
  data/raw/                  downloads as they came (only record_index.csv is in the repository)
  figures/                   the prototype's figure
  prototype_two_maps.ipynb   the 13 Nov prototype, the starting point for part 1
  archive/                   everything from before the direction was chosen
```

To rebuild the shared data from nothing, run `scripts/01_fetch_record.py` to `scripts/04_parse_record.py` in order
from this folder (`01` takes about half an hour). Each member's README says how to rerun their part. Python 3.14,
pandas 3.0.3 (Anas: Anaconda, `python -I`).

## 9. Working rules

- Each member writes only in their own folder; project-level files and `report/` are shared, and every change to
  them is logged in `WORK_AND_DEADLINES.md`.
- Definitions were fixed before results were looked at; every later change is a decision in `DECISIONS.md`.
- Every claim has a check: a null, a second method or a hand-labelled sample.
- Model output is not a measurement until a person has checked a sample of it (`Diego/AI_METHODS.md`).
- Numbers in the paper come from result files, never from memory.

## 10. Literature

The paper's 20 references are in [`report/references.bib`](report/references.bib). The literature was compiled
and checked in Crossref by Diego (D3, [`Diego/d3_prior_work.md`](Diego/d3_prior_work.md)); the methods references
were checked in Crossref or OpenAlex and the three web references (Cook PVI, Wikipedia, The Downballot) looked up
on 23 Nov ([`OFF_CURRICULUM.md`](OFF_CURRICULUM.md)). The closest study is Westwood (2022): a member's bipartisan rhetoric on the floor is unrelated to
their bipartisan votes. That nobody has compared named colleagues with cosponsorship ties is claimed only "to our
knowledge".
