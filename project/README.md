# Two maps of Congress

Final project in **02805 Social Graphs and Interactions** (DTU, autumn 2026).
Group: Anas Mir, Martin Møllenhus, Diego A. Mijares.

**Status (13 November 2026): direction chosen, analysis not done.** The group has settled on the question
below. One prototype has run once. No number in this file is a result yet.

- **What to do next and who does it:** [`WORK_AND_DEADLINES.md`](WORK_AND_DEADLINES.md)
- **How we got here** (earlier questions, ratings, the review, pilots): [`archive/`](archive/README.md)

---

## 1. The question

**Is the Congress that members *talk about* more or less divided by party than the Congress that *works
together*?**

We draw the US House of Representatives (119th Congress, 2025–26) as a network several times, on the same
450 members, and measure how strongly each drawing splits into a Republican side and a Democratic side.

| Map | Two members are joined if | Source | State |
|---|---|---|---|
| **Working map** | one signed a bill the other sponsored | `cosponsors.parquet` | In hand |
| **Floor map** | one names the other in a House floor speech | `speeches.parquet` | In hand |
| **Home map** | one names the other in a press release | members' house.gov sites | Not collected; 7 members sampled |

Nobody can guess the answer in advance. Public talk could be more partisan than quiet cooperation (members
attack the other side in public and cooperate in private), or less (members advertise the few cross-party
partners they have).

**The close-up.** After the big picture we zoom in on named pairs: which cross-party partners does a
member put in front of voters? This is the press-release layer. It gives the paper its concrete examples.

**The 2026 midterm is the setting, not the outcome.** Republicans in exposed seats had a reason to look
independent. We do not try to explain who won.

## 2. The parts of the paper

| Part | What it does | Network or text | Check |
|---|---|---|---|
| **1. Two maps** | Party division of the floor map against the working map | Two networks on the same nodes; party modularity; cross-party share | Degree-preserving rewired null; size-matched comparison; a harder null that keeps the debate structure |
| **2. What a mention means** | A sample of cross-party mentions labelled as agreeing, disagreeing or procedural | Text, read by hand | Two coders, agreement (κ) reported |
| **3. Close-up: showcase ties** | Which Democrats a Republican names at home, and which of their own bills get a press release | Text joined to the network on each tie | Releases matched to bills by bill number; random draw from the member's own bills |
| **4. Optional** | Does a release that says "bipartisan" name a real cross-party partner? | Text joined to the network | Extends Westwood's finding from a word to partners |

Part 2 decides how part 1 is read. If most cross-party mentions are disagreement, the headline is "members
talk across the aisle to argue", not "the talked-about Congress is less divided".

## 3. What each measurement captures and misses

- **A working tie** captures whom a member puts their name next to. It misses informal cooperation and
  why they signed.
- **A floor mention** captures that one member referred to another in Washington. It misses the tone until
  part 2. Many mentions are procedural (yielding time, thanking the chair).
- **A press-release mention** captures whom a member chooses to show voters and the press. It misses
  newsletters, ads and social media. With about 40 releases per member we can say who is **shown**. We
  cannot say who is **hidden**.
- **Party modularity** captures how much more ties stay inside a party than chance predicts. It is not
  comparable between maps of different density, so we compare maps cut to the same number of ties.

## 4. Where the prototype stands

Notebook: [`prototype_two_maps.ipynb`](prototype_two_maps.ipynb). Figure:
[`figures/prototype_two_maps.png`](figures/prototype_two_maps.png). Section 0 of the notebook lists every
modelling choice with its alternative. **One run, 13 November 2026, definitions chosen that day.**

| Map | Ties | Cross-party share | After rewiring | Party modularity |
|---|---|---|---|---|
| Floor | 3,718 | 34% | 50% | 0.15 |
| Floor, yields dropped | 3,249 | 38% | 50% | 0.11 |
| Floor, yields and leadership titles dropped | 2,717 | 39% | 50% | 0.11 |
| Working, strongest ties, same size as floor | 3,718 | 12% | 43% | 0.30 |
| Working, backbone α = 0.05 | 2,328 | 15% | 49% | 0.34 |
| Working, all ties | 46,513 | 29% | 50% | 0.21 |

- Both maps are split by party: the largest modularity in any rewired network is 0.03.
- At the same number of ties, the floor map is much less split than the working map.
- Dropping yields and leadership courtesies does not remove the difference.

**Why it is not a result yet**

- Naming is not cooperating. Tone is unmeasured (part 2).
- Part of the gap comes from how the working map is thinned. With all ties kept it is 29% cross-party.
- The name matcher is not validated. One printed match is clearly wrong ("Mrs. Peters", a constituent).
- The rewired null ignores that every floor debate has a manager from each party.
- The floor is not voter-facing. The home map is not built.

## 5. Three fixes that come before more collection

Full reasoning is in [`archive/martin_council_review.md`](archive/martin_council_review.md), section 5.

1. **A fair baseline for the close-up.** A press release usually announces the member's own bill and names
   its co-leads. Comparing those names with *all* cosponsorship partners is unfair. Match each release to
   its bill by bill number, mark each named colleague as co-lead or not, and test against the member's own
   bills.
2. **A name matcher that sees everyone.** 56 of 450 members share a surname and 11 have a surname of more
   than one word. The prototype notebook resolves part of this (first name, state nearby). It still drops
   717 mentions and has no guard against senators.
3. **A collector that keeps the text.** The pilot collector stores 200 characters per release and no full
   date for many. Store the whole text, the date and the sentence around each name.

## 6. What would make us change course

- **Most cross-party floor mentions are procedural or mistaken matches.** Then the floor map measures House
  procedure, not what members say about each other.
- **The gap disappears under a fair thinning rule or the harder null.** Then the finding is "both maps are
  equally split", a weaker paper.
- **Press releases name almost nobody but leaders.** Then the close-up is empty. Test on the first 20
  members before collecting more. Parts 1 and 2 stand without it.

## 7. Data

All tables are keyed by **Bioguide ID**. Downloads were made on 11 November 2026.

| Table in `data/processed/` | Rows | What it holds | Source |
|---|---|---|---|
| `members.csv` | 451 | Member, party (226 R, 224 D, 1 I), state, district, roll-call scores | Voteview; unitedstates/congress-legislators |
| `bills.parquet` | 12,987 | Bill, type, sponsor, date, policy area, title | govinfo BILLSTATUS bulk data |
| `cosponsors.parquet` | 149,015 | Bill, cosponsor, date, original, withdrawn | govinfo BILLSTATUS bulk data |
| `speeches.parquet` | 35,629 | Speaker turn: day, section, member, words, text | Congressional Record (govinfo) |
| `districts.csv`, `incumbents.csv` | 435 | District lean, 2026 result, incumbent | NBC News results feed; Wikipedia |

Addresses, snapshot dates and the known gaps of each source are in
[`archive/walk_or_talk_outline.md`](archive/walk_or_talk_outline.md), sections 4 and 8. Two of them still
apply: nobody has hand-checked speaker assignment (`data/processed/speaker_check_sample.csv`, 60 turns),
and the election counts are unofficial.

To be written: `mentions.parquet`, `named_ties.csv` and
`press_releases.parquet`. Their columns are fixed in [`WORK_AND_DEADLINES.md`](WORK_AND_DEADLINES.md), section 3.

## 8. Folder layout

```
project/
  README.md                  this file: the question and the design
  WORK_AND_DEADLINES.md      who does what, status, dates. Kept up to date
  prototype_two_maps.ipynb   the two-maps prototype: the starting point for part 1
  figures/                   figures written by the live notebooks
  scripts/                   01–04 download and parse the data; roster.py is the member list
  data/processed/            the tables the notebooks read
  data/raw/                  downloads as they came (only record_index.csv is in the repository)
  archive/                   everything from before the direction was chosen
```

To rebuild the data from nothing, run `scripts/01_fetch_record.py` to `scripts/04_parse_record.py` in
order from this folder. `01` takes about half an hour. The notebooks need only `data/processed/`.

Environment for the prototype: Python 3.14, pandas 3.0.3, networkx 3.5, matplotlib 3.11.2.

## 9. Working rules

- One stream per person and one notebook per stream. Nobody edits another person's notebook.
- Shared inputs are files in `data/processed/`.
- Fix definitions before looking at results again. Record any later change in `docs/AI_METHODS.md`.
- Every claim gets a check: a null, a second method or a hand-labelled sample.
- Model output is not a measurement until a human has checked a sample of it.

## 10. Literature to start from

Existence checked, **not read** (see the archive files for DOIs):

- Fowler (2006), "Connecting the Congress", *Political Analysis*. Defines the cosponsorship network.
- Neal (2020), "A sign of the times? Weak and strong polarization in the U.S. Congress", *Social Networks*.
- Harbridge (2015), *Is Bipartisanship Dead?*, Cambridge University Press.
- Westwood, "The Partisanship of Bipartisanship", *Political Behavior*. The closest study. Cited as 2021
  in the archive; it appears to have been published in 2022. `[UNVERIFIED]`
- Gentzkow, Shapiro and Taddy (2019), *Econometrica*. Partisanship of congressional speech.

`[UNVERIFIED]`: that nobody has compared named colleagues with cosponsorship ties. One search session
found no such study.
