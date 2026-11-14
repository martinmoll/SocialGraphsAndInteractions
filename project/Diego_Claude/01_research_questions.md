# 01 · Research questions: recommendation, alternatives, scrutiny

Judged against the grading categories on the course's week 8 page (read live 11 Nov 2026, section 2,
Cmd+F "How it is graded"): research question; data and scope; showcasing the course; analysis and checks;
figures; references and literature; overall impression; presentation and questions. One 0-3 score overall.

Two tests the group has applied to every idea so far, and which are applied here too:

- **Obvious-answer test.** Would a reader guess the answer before reading? If yes, the question is a figure,
  not a paper.
- **Bent-to-the-data test.** Is the question something we would ask anyway, or something we wrote because
  we had the tables?

Scores below are our honest estimate of the course's 0-3 score with competent execution in 16 days. They
are judgement, not data.

---

## Scrutiny of the two questions already in the repo

### A. Walk or talk (`readme.md`, `walk_or_talk.ipynb`)

> Among Republican House members who stood for re-election in 2026, did the ones who cooperated across the
> aisle, or the ones who sounded less like their party, run ahead of their district?

- **Obvious-answer test: fails partly.** Canes-Wrone, Brady and Cogan (2002) already answer it for roll
  calls ("out of step, out of office"). Our version swaps roll calls for cosponsorship and speech.
- **Result:** walk ρ = +0.14 inside its null; talk ρ = −0.20 that does not survive dropping the redrawn
  states (p = 0.17). Talk score split-half reliability about 0.58.
- **Structural problem:** lean explains 83% of margins and, per Martin's check, state explains 66% of
  running ahead. Any member-level predictor fights for a few points with n = 162. This will stay weak.
- **Expected score: 1-2.** Good checks, weak question, weak result.

### B. Blocs in the wave (`work_plan.md`, `martin_blocs.ipynb`)

> Is the House Republican party one bloc or several: do the blocs found in the cosponsorship network also
> speak differently, and did the 2026 wave hit them equally?

- **Execution is strong.** Backbone, Louvain with a rewired null (0.532 vs 0.358 ± 0.006), stability over
  settings, caucus validation planned, text similarity with a shuffle null and a different-state guard.
- **Obvious-answer test: fails.** "Is a 226-member party one bloc or several?" Everyone expects several.
  The blocs found are partly state delegations (NMI 0.41 vs 0.24 shuffled) and their distinctive words look
  like committee portfolios (bloc B: russian, ukraine, sanctions; bloc C: irs, deduction, tax; bloc D: grid,
  reliability, pipelines). "Members who sit on the same committees and come from the same state sign each
  other's bills and use the same words" is what a reader assumes.
- **The third part is already dead,** by the plan's own state check (p = 0.42). The working headline,
  "blocs exist and speak differently; the uneven wave is explained by state", is two expected findings and
  a null.
- **Bent-to-the-data test: borderline.** The question grew out of what the cosponsorship network can show.
- **Expected score: 2** with this execution, held down by the research-question category.
- **Keep the machinery.** Martin's blocs are exactly the "who" grouping the recommended question needs (see
  below). None of that work is lost.

---

## 1 · Recommended: Running from Trump?

> As Trump became unpopular in 2025-26, did House Republicans distance themselves from him, in what they
> said on the floor and in whom they cosponsored with, more than they did in his first term (2017-18), and
> who led the distancing: the swing-seat members facing the wave, or the party's hardline wing?

**What we measure**

| Half | Measurement | Captures | Misses |
|---|---|---|---|
| Words | Rate of "Trump" per 10,000 floor words, per member and per half-year; share of members who name him at all; week-6 comparison of which words Republicans dropped and adopted between periods | How much a member ties themselves to Trump by name on the floor | Stance (a mention can be praise or criticism, so we hand-label it), everything said off the floor |
| Deeds | Share of a Republican's cosponsorships that go to Democratic sponsors, per quarter; modularity of the party split per period, with a label-shuffle null | Whom a member is willing to put their name next to | Why they signed; bills that never needed cosponsors |
| Who | Each member's change in words and in deeds, against district lean (exposure), NOMINATE (ideology) and Martin's blocs | Whether distancing came from exposure or ideology | Causation: nothing here is causal |
| Baseline | Everything above for the 115th Congress (2017-18) | Whether 2025-26 differs from a normal Trump-era Republican House heading into a wave | Differences between the two terms other than approval |
| Election | Running ahead of the district against distancing (secondary) | Whether distancing paid | Challenger, money, local issues; small n |

**Pros**

- The obvious-answer test passes. The pilot (see `02`) found three things nobody would bet on in advance:
  the drop in Trump mentions is led by the hardline wing, not the swing seats; the members who went quiet
  are not the ones who crossed over (ρ = 0.06); and distancing does not relate to running ahead
  (ρ = 0.08, n = 140).
- Diego's original angle (Republican voters vs their candidates; unpopular Trump decisions) lives inside it:
  the candidate side of the disconnect is the measurement, the voter side is the election backdrop, and
  issue-by-issue silence on tariffs, Medicaid, Epstein and Iran can be one panel (see alternative 4).
- A real control (2017-18), not just a shuffle. "A comparison that rules out the boring explanation" is
  exactly the phrase the week 8 page uses for a convincing analysis (Section 6, Cmd+F "Know what makes an
  analysis convincing").
- Uses all existing data. The 115th Congress comes from the same govinfo bulk and Record addresses, with the
  same scripts pointed at 2017-18. Verified reachable 11 Nov 2026 (BILLSTATUS-115-hr.zip is 28.7 MB;
  CREC-2017-05-03 mods.xml returns 200).
- Martin's blocs and walk/talk definitions slot straight in. Nothing is thrown away.
- Literature exists to place it against: presidential coattails and midterm loss, Canes-Wrone et al. (2002),
  Fowler (2006) for cosponsorship, Gentzkow, Shapiro and Taddy (2019) for speech. We should add work on
  members distancing from unpopular presidents (to find and verify, not from memory).

**Cons**

- **The baseline could kill the headline.** Part of the cosponsorship rise is clearly normal: in a 2017-18
  sample Republicans also went from 8.0% cross-party in 2017Q1 to 12-17% after. "Biden" mentions also fell
  (8.86 to 1.55 per 10k floor words), so part of the Trump drop may be a general fade of national names as
  the term goes on. The 2017-18 Record will tell us. If it shows the same pattern, the honest paper is
  "this is the normal Republican cycle, not a reaction to Trump's unpopularity". A negative result with a
  convincing check is acceptable to the course, but scores lower.
- **Name mentions are a crude measure.** "Trump" can be praise, criticism or a bill title. Needs a
  hand-labelled sample (100 mentions, two coders, kappa).
- **Role effects.** Several of the biggest droppers (Jordan, Steil, Joyce) manage floor debate as chairs. When
  the floor schedule changes, their words change. Needs a check that drops committee chairs or procedural
  turns.
- **Two Congresses double the Record download** (about 30 minutes and 530 MB temp space for the 119th).
- **The approval series is patchy.** Wikipedia's polling page has monthly sections with gaps (no August
  2025 to January 2026 sections). Use it as context only, not as a regressor.
- **Does not answer "why Republicans lost".** It answers what they did beforehand. Reviewers may ask about
  the link; the answer is the secondary election test and the state finding.

**Data availability (checked 11 Nov 2026):** all 119th tables in `data/processed/` (pilot ran on them);
115th bills on govinfo bulk (sampled 1,233 bills, 19,356 cosponsorships); 115th Record on govinfo; results
on NBC feed and Wikipedia (D 255, R 168, 97.2% declared); approval aggregates on Wikipedia (Silver Bulletin
37.3% approve, 1 Nov 2026).

**Expected score: 2, with 3 possible.** The 3 needs: the 2017-18 contrast is clear in at least one half, the
stance hand-label holds (kappa ≥ 0.6), and three figures that each carry one claim.

---

## 2 · Alternative: Blocs in the wave, refocused

Keep Martin's question but drop the election and make the "who" the point: *Which Republican blocs moved
toward Democrats in 2025-26, and do the blocs that moved also change their vocabulary?*

- **Pros:** most of the work exists; strong network methods.
- **Cons:** still mostly "blocs exist"; without the time dimension it repeats B; with the time dimension it
  becomes the recommended question with less text.
- **Data:** in hand. **Expected score: 2.**

## 3 · Alternative: Walk or talk, fixed

Same question with a more reliable talk score (phrases, fewer words, press releases).

- **Pros:** the pipeline is done; pre-registered definitions.
- **Cons:** known answer in the literature; the election link is structurally weak (state effect); more text
  costs days.
- **Data:** in hand, press releases not checked. **Expected score: 1-2.**

## 4 · Alternative: Silence on unpopular decisions

*On the administration's unpopular decisions (tariffs, Medicaid cuts, the Epstein files, the Iran conflict,
ICE operations), did Republicans defend them on the floor or go quiet, and who broke ranks by cosponsoring
Democratic challenges (war-powers resolutions, tariff relief, ACA credit extensions, the Epstein Files
Transparency Act)?*

- **Pros:** directly Diego's "unpopular Trump decisions" angle; vivid. The pilot shows clear spikes, e.g.
  Republicans said "tariff" at 0.0-23.6 per 100k words per month against Democrats' 0.0-112.6, and "iran" at
  113.1 per 100k in March 2026.
- **Cons:** "the opposition talks more about the government's failures" is obvious. The dissent network is
  small: few Democratic-sponsored challenge bills, few Republican cosigners (Massie-type members), so it
  becomes anecdotes. Choosing the events is a judgement reviewers will question.
- **Data:** in hand. **Expected score: 1-2 alone. Best used as one panel inside question 1.**

## 5 · Alternative: The voter-side disconnect

*In districts Trump won in 2024, did Republicans lose because Trump's voters stayed home (Republican votes
fell) or because voters switched (Democratic votes rose), and did the candidate's profile matter?*

- **Pros:** the most direct version of Diego's "Republican voters vs their candidates".
- **Cons:** needs 2024 presidential results on the 2026 district lines; nine states redrew (AL, CA, FL, LA, NC,
  OH, TN, TX, UT), so these are not in hand and not verified. Turnout is driven by state races (Martin's
  66%). The network and text halves become predictors again, which have shown nothing at member level.
  Most of the paper becomes electoral arithmetic, not course methods.
- **Data:** not verified. **Expected score: 1-2.** Not recommended.

## 6 · Alternative: The dissent network

*Which Republicans cosigned Democratic challenges to the administration, and do they form one group or
several (economic moderates vs anti-war or anti-establishment hardliners)?*

- **Pros:** sharp, fun, good zoom-in.
- **Cons:** too few bills and members for network statistics. A paragraph, not a paper.
- **Expected score: 1.** Use as a zoom-in inside question 1 if it holds up.

---

## Bottom line

Pick **1, Running from Trump?** It is the only candidate that passes the obvious-answer test with data
already in hand, has a real control, and keeps Martin's blocs and the existing pipeline. What would change
this recommendation: if on Sunday 15 November the 2017-18 Record shows the same drop in Trump mentions and
the cosponsorship gap between the two Congresses is under about 3 points, fall back to 2 (blocs, refocused
on movement over time) and write the 2017-18 comparison into it.
