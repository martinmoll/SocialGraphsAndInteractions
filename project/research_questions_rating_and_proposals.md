# Research questions: ratings and proposals

Written Thursday 12 November 2026 by Anas with Claude (AI-assisted, see section 10).

**Status: an overview for the group, not a decision.** This file gathers every research question raised so
far, rates each against the course's own grading text, records what four small pilots found, and puts one
refined question and two fallbacks on the table. Nothing here is agreed. The group chooses on Wednesday
18 November (the meeting format in `martin_work_plan.md`, section 3).

It changes nobody's files. Martin's direction is in `martin_work_plan.md` and `martin_blocs.ipynb` (main).
Diego's is in `Diego_Claude/` on the branch `diego-claude-research-question`. The first prototype is in
`readme.md` and `walk_or_talk.ipynb` (main).

Every pilot number below is **one run on 12 November with definitions chosen that day**. They are
observations, not results. The scripts are in `Anas_Claude/pilot/`.

---

## 1. Where the framing stands

| Date | Step | Outcome |
|---|---|---|
| 11 Nov | **Walk or talk?** (Anas, `readme.md`) | Network half solid; talk score noisy; election link small and not robust |
| 11 Nov | **Blocs in the wave** (Martin, `martin_work_plan.md`) | Blocs exist and speak differently; the wave did not hit them differently (p = 0.42) |
| 11 Nov | **Running from Trump?** (Diego, `Diego_Claude/`) | Trump mentions fall; cross-party share rises; a 2017-18 baseline is planned as the kill test |
| 12 Nov | **This review** | Three pilots on the existing tables, two new ideas tried and killed, one refined question scouted on new text |
| 18 Nov | Group meeting | Choose one direction or combine parts |

**The short version**

- None of the three questions reaches a 3 in the research-question category as written.
- They share two problems. Every *member-level* result has failed (running ahead of the district, the talk
  score, per-member change scores). And network and text sit in separate panels, where the course's model
  questions set them against each other on the same nodes.
- The proposal in section 6 changes the unit from the member to the *working relationship* and asks which
  relationships members show their voters. A small sample of press releases suggests the measurement is
  not empty. The data for it is not collected.

---

## 2. How the questions were rated

Source: the week 8 page, <https://sunelehmann.com/socialgraphs2026-web/weeks/week8.html>, read 12 Nov 2026.

- **Scale:** the course's 0–3. Each table gives the score for the *research question* category first ("Is
  there one, is it interesting, and is it specific enough to be answered?", section 2 of the page, "How it
  is graded"), then the score we expect overall with clean execution.
- **Tests applied to each question:**
  - the five rules for a question (section 6): question before method; say what each analysis measures;
    validate; one story; a comparison that rules out the boring explanation;
  - the five dataset questions (section 5): both halves; a few hundred to a few thousand nodes; obtainable;
    a domain we care about; something unknown;
  - the two tests Diego introduced in `Diego_Claude/01_research_questions.md`: would a reader guess the
    answer (obvious-answer test), and would we ask this without the tables (bent-to-the-data test).
- **The scores are judgement, not data.** They are one reader's estimate.

---

## 3. Ratings

| # | Question | From | Question (0–3) | Overall (0–3) | Main reason |
|---|---|---|---|---|---|
| A | Walk or talk | Anas, `readme.md` | 1 | 1–2 | Specific and answerable, but the answer is a null and the literature already has it. District lean explains 83% of margins |
| B | Blocs in the wave | Martin, `martin_work_plan.md` | 1–2 | 2 | Three questions in one sentence; "several blocs" is what a reader expects; the election part is a null. Strongest checks in the repository |
| C | Running from Trump? | Diego, `Diego_Claude/` | 2 | 2 | The only one a reader would ask unprompted, with a real baseline. Two of its three legs are weaker than written (section 4) |
| C2 | Blocs, refocused on movement | Diego, alternative 2 | 1–2 | 2 | Still "blocs exist" unless time is added, and then it becomes C |
| C3 | Walk or talk, fixed | Diego, alternative 3 | 1 | 1–2 | Same dead outcome |
| C4 | Silence on unpopular decisions | Diego, alternative 4 | 1–2 | 1–2 | Obvious direction; hand-picked events. Good as one panel or a zoom-in |
| C5 | The voter-side disconnect | Diego, alternative 5 | 1 | 1 | Electoral arithmetic; network and text become predictors of the dead outcome |
| C6 | The dissent network | Diego, alternative 6 | 1 | 1 | Too few bills and members |
| D1 | Administration decisions (Iran war, financing Israel) | `readme.md`, section 11 | 1 | not rated | "Damaged the Republicans' case" is a causal claim with one election. Works as a zoom-in case |
| D2 | Newsletter sentiment | `readme.md`, section 11 | 1 | not rated | Outcome is dead; data needs an account; sentiment needs its own validation |
| **P1** | **Which working relationships do members show their voters?** | this file, section 6 | **3** | 2–3 | Tie-level, non-obvious, a built-in comparison. Data not collected |
| P2 | Does a president's party leave him in words, in deeds, or neither? Six midterms | this file, section 7 | 2 | 2, 3 possible | C with a real baseline and the party as unit |
| P3 | Do Republicans who work across the aisle carry Democratic words into their party? | this file, section 7 | 2–3 | not rated | Close to diffusion on networks, but leans on noisy per-member word measures |

Not rated: the citation-network prototype on the branch `final-project-prototype` (not read for this review).

### Reasoning for the three main questions

**A. Walk or talk** (Anas's own prototype, rated as hard as the others)

- The question is clear and was answered: walk ρ = +0.14 inside its null; talk ρ = −0.20, which does not
  survive dropping the nine redrawn states (p = 0.17). Numbers from `readme.md`, section 6.
- Canes-Wrone, Brady and Cogan (2002) already answer the roll-call version.
- The talk score is noisy: odd-day and even-day halves agree at ρ = 0.41, which implies a reliability of
  about 0.58 for the full score.
- Anything with "running ahead of the district" as the outcome inherits this.

**B. Blocs in the wave** (Martin)

- Strong on checks: rewired null (modularity 0.53 against 0.36), a different-state guard on the text
  result, caucus validation planned.
- The question has three parts. The first has the answer everyone expects, the second is partly committee
  and state vocabulary (Diego's reading in `01_research_questions.md`), the third is a null.
- **Worth keeping whatever is chosen:** the bloc file as a grouping, and the finding that state alone
  explains 66% of running ahead.

**C. Running from Trump?** (Diego)

- Passes the interest test, has a planned 2017-18 baseline, and its write-up is honest about its own risks.
- Two findings from the pilots on 12 November (section 4) weaken it as written:
  - the rise in cross-party cosponsorship share is a calendar effect, not Republicans signing more
    Democratic bills;
  - "who led the distancing" is mostly where each member started.
- Its baseline is one Congress against one Congress. Nothing yet says how large a 3–6 point gap between
  two Congresses is.
- The words leg (the fall in Trump mentions) stands, untested against 2017-18. P2 in section 7 is this
  question rebuilt around that leg.

---

## 4. What the pilots on the existing tables found

All on `data/processed/` as committed on main.

**4.1 The cross-party share rises because same-party signatures fall** (`pilot_counts.py`)

Republican cosponsorship signatures by quarter and sponsor's party, all bill types:

| Quarter | On Republican bills | On Democratic bills | Share on Democratic bills |
|---|---|---|---|
| 2025Q1 | 12,754 | 1,256 | 9.0% |
| 2025Q2 | 6,597 | 1,222 | 15.6% |
| 2025Q3 | 5,155 | 1,175 | 18.6% |
| 2025Q4 | 4,391 | 1,197 | 21.4% |
| 2026Q1 | 4,349 | 961 | 18.1% |
| 2026Q2 | 4,864 | 1,226 | 20.1% |
| 2026Q3 | 3,819 | 986 | 20.5% |
| 2026Q4 | 769 | 345 | 31.0% |

- Signatures on Democratic bills are flat at roughly 1,000–1,250 a quarter. The share doubles because
  signatures on Republican bills fall by two thirds after the first quarter.
- Diego's pilot already flags the first quarter as structurally odd. This table shows the whole rise is
  that effect. **Use counts, or bills matched by quarter of introduction, not shares.**

**4.2 Per-member change is mostly start level** (`pilot_together.py`)

- Raw change in a Republican's Trump-mention rate does track ideology (Spearman −0.24, p = 0.001) and
  district lean (−0.15, p = 0.047), n = 179.
- Once the member's early rate is in the model, ideology and lean together add under one point of explained
  variance (R² 0.428 → 0.436). Members who started high fell more, and the conservative wing started high.
- The same holds for the change in cross-party share (R² 0.631 → 0.655, n = 214).

**4.3 No sign that members moved together with the people they work with** (`pilot_together.py`)

- Neighbours' adjusted change in the Republican cosponsorship network sits inside the shuffle band (words:
  0.03, band −0.25 to 0.14; deeds: 0.05, band −0.23 to 0.12).
- Louvain blocs explain no more of the change than chance (three seeds, p between 0.36 and 0.99).
- **Limits:** this used the unfiltered network (density 0.59), not Martin's backbone blocs. Read it as "no
  signal at this power", not "blocs explain nothing".

**4.4 Symbolic bills are a small part of cross-party work** (`pilot_symbolic.py`)

- Bills flagged as symbolic by a title rule (coins, medals, post offices, commemorations): 3.6% of bills,
  7.4% of cross-party signatures, 5.0% of same-party signatures.
- The party split is strong in both layers: modularity of the party split 0.206 on symbolic bills and
  0.274 on the rest, against about 0 for shuffled labels.
- So "cross-party cosponsorship is mostly cheap, symbolic bills" is not supported.

---

## 5. Ideas tried and killed on 12 November

Kept here as insurance, as the week 8 page advises ("The road not taken").

| Idea | What was tried | Why it was dropped |
|---|---|---|
| **Exposure or network?** Does distancing follow a member's own seat risk or the people they work with? | 4.2 and 4.3 | No signal on either side |
| **What do Republicans cross the aisle for?** Score bill titles with floor vocabulary; ask whether Republicans sign Democratic bills that sound Democratic | `pilot_bills.py`: titles alone tell the sponsor's party with AUC 0.64; Democratic bills in the most Democratic-sounding fifth have a Republican cosponsor 27% of the time, the most Republican-sounding fifth 48% | The direction is what a reader expects; the change over time is again first quarter against the rest; six-word titles are thin text; 4.4 removed the symbolic-bills story |

---

## 6. Proposal P1: which working relationships do members show their voters?

**Question.** Which of the people they work with do members of Congress show their voters?

Every cosponsorship tie a member has is either shown at home (the partner is named in the member's press
releases) or not. The question is whether the shown ties are a fair sample of the real ones or a selected
picture, and what does the selecting. The 2026 midterm is the setting: Republicans in exposed seats had a
reason to look independent of an unpopular president.

### Why this version

- **The unit is the tie, not the member.** Thousands of ties instead of a few hundred noisy member scores,
  which is where every earlier attempt failed.
- **Each member is compared with their own ties.** "Swing-seat members name more Democrats because they
  work with more Democrats" can no longer produce the result.
- **It can fail in two places.** Prediction: swing-seat Republicans over-show their Democratic partners;
  safe-seat Republicans hide theirs. Either half may be false.
- **Network and text meet on each tie.** This is the "text as network" join in the week 8 Essentials, and
  the same shape as our week 7 named-against-linked figure.
- **It has a built-in comparison.** Floor-speech names give the Washington picture, so the home picture is
  tested against both deeds and Washington words.
- **It carries each of our angles:** words against deeds (Anas), the gap between candidates and their
  voters (Diego), the network and the blocs as a grouping (Martin), and the readme's idea of text written
  for constituents.

### Sub-questions and their checks

| # | Sub-question | Measurement | Check |
|---|---|---|---|
| 1 | Is the home picture selected? | Of a member's cosponsorship partners, the share of other-party partners among those named at home, against their share of the ties | Null: draw the same number of named partners at random from the member's real partners, weighted by tie strength |
| 2 | Does the selection flip with seat safety? | The same gap, pooled over swing-seat and over safe-seat members | Shuffle seat labels; also by ideology fifth and by Martin's blocs |
| 3 | Is it only at home? | The same test on names in floor speeches | If the floor is a fair sample and home is not, the selection is aimed at voters |
| 4 | Who is named without a tie, and how? | Colleagues named but never worked with | Hand-label a sample as partner, target or neutral; two coders; report κ. This also validates what a "name" measures |

Optional panel if space allows: 2025 against 2026. Optional zoom-in: the member whose two pictures
disagree most, or the weeks of the Iran war (the administration-decisions angle).

### What each measurement captures and misses

- **A cosponsorship tie** captures whom a member puts their name next to. It misses informal cooperation
  and why they signed.
- **A name in a press release** captures whom a member chooses to put in front of voters and the press. It
  misses tone until sub-question 4, and everything said in newsletters, ads and social media.
- **A name in a floor speech** captures whom a member addresses in Washington. Many are procedural
  (yielding time) and need filtering.

### What scouting found (12 November)

**Press releases on members' own house.gov sites** (`press_pull.py`): 40 releases each from seven
Republicans, hand-picked. An eighth site did not parse.

| Seat | Releases | Name any House colleague | Name a House Democrat | Name a House Republican |
|---|---|---|---|---|
| Swing (Lawler, Bacon, Fitzpatrick, Ciscomani) | 160 | 43% | 38% | 18% |
| Safe (Roy, Hageman, Biggs) | 120 | 19% | 5% | 14% |

- Names are not sparse: Bacon names a Democrat in 65% of releases, Fitzpatrick in 48%, Lawler in 28%,
  Hageman in none.
- The word "bipartisan" is not a usable measure: Lawler uses it in 98% of releases, in a fifth of them only
  in the closing lines.
- Listing pages paginate on three site templates, which covered seven of eight sites. The RSS feeds hold
  ten items each and are often years old.
- **Limits:** seven members chosen by hand; matched names not read for false hits; dates confirmed as
  2025–26 for six of the seven.

**Floor-speech names** (`pilot_names.py`, on `speeches.parquet`, House section only):

- 6,824 member-to-member mentions over 3,849 pairs from 409 speakers.
- 25 random matches were read: all pointed at the right member; about four were procedural yields.
- 74% of named pairs also share a cosponsorship tie, against 55% (± 0.5) under a shuffle that keeps each
  speaker's count and each target's popularity and party.
- At member level the cross-party share in names tracks the cross-party share in cosponsorships: Spearman
  0.37 for Republicans (n = 101), 0.29 for Democrats (n = 92), both outside the shuffle band (±0.2).
- This is the Washington layer (sub-question 3). It is not voter-facing and does not answer the main
  question on its own.

**Newsletters (DCinbox):** the site's own search request answers without a login but returns five emails per
query and ignores filters. Its counter shows 224,291 emails since 2010 across both chambers. Full text and
export need an account, requested by email from the maintainer (address on dcinbox.com). Not requested.
Name density unknown.

### Data and scope

| | |
|---|---|
| Nodes | House members of the 119th Congress (451 in `members.csv`); the collection can start with Republicans |
| Links | Cosponsorship ties (`cosponsors.parquet`, in hand) |
| Text 1, home | Press releases from members' own sites. **Not collected.** Because the unit is the tie, a sample of about 60 Republicans spread over district lean should carry it, at up to 40 releases each |
| Text 2, Washington | Floor speeches (`speeches.parquet`, in hand) |
| Grouping | District lean (`districts.csv`), NOMINATE (`members.csv`), Martin's blocs |
| Election | The setting, not the outcome |

Collection cost is not measured. The sample of seven sites took a few minutes of requests; the open work is
the remaining site templates and reading matched names.

### What would make us abandon it

- **Sparse or star-shaped names.** If most members name nobody except party leaders and the president,
  sub-question 1 is empty. Test on the first 20 members before collecting more.
- **No selection.** If named partners look like a random draw from real partners in both seat groups, the
  finding is "the home picture is fair". That is a result, but a weaker paper.
- **Prior work.** Westwood (2021) looks like the closest study (section 9). If it already answers
  sub-question 1, our addition is the tie-level view, the home-against-Washington comparison and 2026.

### Expected score

Research question 3. Overall 2 to 3: it depends on the collection, the hand-labelling, and three figures
that each carry one claim.

---

## 7. Fallbacks

**P2. Does a president's party leave him in words, in deeds, or neither?** Six midterm Congresses,
2005–2026 (109th, 111th, 113th, 115th, 117th, 119th; the president's party in the House each time).

- This is Diego's question with the party over time as the unit and five baselines instead of one.
- Expected finding if 4.1 holds in other Congresses: words move, deeds do not.
- Sub-questions: (1) does the party name its president less as the term goes on, more so when approval
  falls further, with a fade control and a hand-labelled stance sample; (2) does cross-party cosponsorship
  rise once the calendar is removed; (3) do the two move together across Congress-quarters, and do swing
  and safe seats differ as pooled groups; (4) zoom-in on the Iran war weeks.
- Data: the govinfo bill files for the 109th, 111th and 113th and one 2010 Record day answered HTTP 200 on
  12 Nov. Their internal structure and our parser on older Record formats are `[UNVERIFIED]`.
- Kill test: Diego's, already planned for Sunday 15 November. If 2017-18 shows the same fall in the
  president's name, the headline becomes "every party does this".
- Expected score: 2, with 3 possible.

**P3. Do the Republicans who work across the aisle carry Democratic words into their own party?**

- Network position predicts who adopts the other side's vocabulary first; the reverse flow (Republican
  words among Democrats) is the comparison.
- Not piloted. It leans on per-member word measures, which were noisy in the prototype.

---

## 8. Work distribution

**A proposal to discuss, not an assignment.** It keeps the rules in `martin_work_plan.md`: one stream per
person, one notebook per stream, shared inputs as files in `data/processed/`, nobody edits another person's
notebook, definitions fixed before results are looked at again. Hours are rough guesses.

### Before the choice on 18 November (useful for any direction)

| Who | What | Delivers |
|---|---|---|
| **Diego** | Run the 2017-18 kill test already planned in `Diego_Claude/03_plan_if_chosen.md` (decides C and P2). Read Westwood (2021) and Harbridge (2015) and write three lines on what each found | Two tables for 2017-18; a note on prior work |
| **Martin** | Write the bloc file (module N1). Rerun 4.3 on the backbone blocs. Check 4.1 against `martin_blocs.ipynb` in case it changes any bloc result | `data/processed/blocs.csv`; a yes or no on blocs and change |
| **Anas** | Extend the press release sample from 7 to about 20 Republicans spread over district lean; read 50 matched names for precision; draft the tie-level figure for sub-questions 1 and 2. Request the DCinbox account | `data/processed/press_releases.parquet` (first part); one figure |
| **All** | Hand-check the 60 sampled speaker turns (Martin's module T1); bring a direction as one sentence, one figure and what speaks against it | Agreement rate for Methods |

### If the group picks P1

| Stream | Owner | Work | Rough hours |
|---|---|---|---|
| **Home text** | Anas | Press release collector for the remaining site templates, about 60 Republicans; name matcher and its precision check; the shown-ties table; data refresh; Methods; `docs/AI_METHODS.md`; final assembly | 20 |
| **Network and nulls** | Martin | Tie table with strengths from the cosponsorship data; the partner-draw null (sub-question 1); pooling by seat safety, ideology and blocs (sub-question 2); figures 1 and 2; network part of Results; slides | 15 |
| **Washington text and validation** | Diego | Floor-speech names with procedural yields filtered (sub-question 3); labelling protocol and sample for sub-question 4; literature; Introduction and Discussion; reflection | 15 |
| **Shared** | All three | Each mention in the labelling sample is coded by two people; everyone reads the full draft; each explains a method they did not build | 4 each |

Shared files that join the streams: `press_releases.parquet`, `named_ties.csv` (member, named colleague,
source, date, count), `blocs.csv`.

### If the group picks another direction

- **P2 or C:** Diego's streams in `Diego_Claude/03_plan_if_chosen.md`, with 4.1 applied to the deeds
  measure and "who led" compared as pooled groups.
- **B:** the streams in `martin_work_plan.md`, section 2.

### Dates

| Date | What |
|---|---|
| Sun 15 Nov | Diego's 2017-18 kill test; first 20 members of press releases |
| Wed 18 Nov, 14:00–17:00 | Each presents a direction; the group chooses; outline in Overleaf |
| Sun 22 Nov | Numbers frozen |
| Tue 24 Nov, 20:00 | Full draft in Overleaf |
| Wed 25 Nov, 14:00–17:00 | Read aloud, cut to six pages, number check, rehearse |
| Thu 26 Nov | Submit; Friday is buffer only |
| Fri 27 Nov, 23:59 | Hand-in deadline |
| Wed 2 Dec | Presentation |

---

## 9. Decisions for the group

1. **Which direction:** P1, P2, B, C, or a combination. P1 and P2 can share the floor-speech layer and the
   zoom-in.
2. **If P1: is the press release collection worth the days it costs?** Decide after the first 20 members.
3. **Republicans only, or both parties?** Republicans only halves the collection and matches the setting.
4. **Do we ask the teachers** about the direction on Wednesday 18 November, before or after choosing?
5. **Whatever is chosen:** stop using the cross-party *share* over time as evidence of movement (4.1).

---

## 10. Verified, not verified, and how this was made

**Checked on 12 November 2026**

- The week 8 page was read live; the grading categories and the section references are from it.
- All numbers in sections 4, 5 and 6 are printed by the scripts in `Anas_Claude/pilot/`.
- These references exist as cited (Crossref lookup): Harbridge (2015), *Is Bipartisanship Dead?*, Cambridge
  University Press, doi:10.1017/cbo9781139942324; Westwood (2021), "The Partisanship of Bipartisanship: How
  Representatives Use Bipartisan Assertions to Cultivate Support", *Political Behavior*,
  doi:10.1007/s11109-020-09659-6; Jacobson (2015), "It's Nothing Personal: The Decline of the Incumbency
  Advantage in US House Elections", *Journal of Politics*, doi:10.1086/681670; Neal (2020), "A sign of the
  times? Weak and strong polarization in the U.S. Congress, 1973–2016", *Social Networks*,
  doi:10.1016/j.socnet.2018.07.007.

**`[UNVERIFIED]`**

- **What those four references found.** Only their existence was checked. Nobody has read them. How to
  check: read the abstracts and, for Westwood, the measure of bipartisan behaviour it uses.
- **Every pilot number:** one run, definitions chosen on the day, no second instrument. Rerun after the
  definitions are fixed.
- **The press release name matcher:** not read for false hits. Surnames that are also common words or shared
  by senators can mismatch.
- **The symbolic-bill title rule** (4.4): eight sampled titles looked right; no precision or recall measured.
- **Older Congresses** (P2): only that the files answer. Structure and parser not tested.
- **The scores in section 3.**

**How this was made.** Claude (Anthropic) read both branches of the repository and the week 8 page, ran the
pilots on `data/processed/`, and fetched the press release sample and the DCinbox preview on 12 November
2026. Anas directed the review and chose the direction of P1. The ratings of Martin's and Diego's questions
are one reader's judgement and are meant to be argued with.
