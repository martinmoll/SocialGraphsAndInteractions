# Council review of P1: what to change, and a first test

Written Friday 13 November 2026 by Martin with Claude (AI-assisted, see section 8).

**Status: a suggestion for the group, not a decision.** This file reviews Anas's proposal P1 in
`research_questions_rating_and_proposals.md`, proposes one addition and three fixes, and reports a first
prototype. Nothing here is agreed. It changes nobody's files. The group chooses on Wednesday 18 November.

It lives on the branch `prototype/two-maps-of-congress`, next to the prototype it describes
(`prototype_two_maps.ipynb`).

---

## 1. The short version

- **P1 is a good question, and we should keep it.** It asks whether the colleagues a member shows their
  voters are a fair picture of the colleagues they really work with.
- **Its answer is easy to guess.** "Republicans in swing seats mention Democrats more" is what most
  readers expect before we show them anything.
- **We suggest adding a bigger, less guessable question in front of it:** is the Congress that members
  *talk about* more or less divided than the Congress that *works together*? We call this "two maps of
  Congress".
- **P1's press releases then become the close-up:** the named pairs that make the story memorable.
- **P1 needs three fixes before more data is collected.** The most important is that its comparison is
  not fair as written (section 5).
- **A first prototype of the two maps ran on data we already have.** On the House floor, about one named
  tie in three crosses the party line. In the working network, about one in eight does. It is one run and
  not yet trustworthy (section 6).

---

## 2. What we are trying to find out, in plain words

Think of a school class.

- There is a list of **who actually does group work with whom**. That is the real picture.
- There is also **who each pupil says they work with** when they talk to their parents. That is the
  shown picture.

P1 asks whether the shown picture matches the real one. A pupil who works mostly with their own friends,
but tells their parents about the one time they helped someone from the other group, is showing a
selected picture.

In our data:

| In the class | In Congress | Where it comes from |
|---|---|---|
| Pupils | 450 House members | `members.csv` |
| The two friend groups | Republicans and Democrats | `members.csv` |
| Who does group work with whom | Who signs whose bills (cosponsorship) | `cosponsors.parquet`, in hand |
| What pupils tell their parents | Who members name in press releases | Not collected, 7 members sampled |
| What pupils say in the classroom | Who members name in floor speeches | `speeches.parquet`, in hand |

---

## 3. How this review was made

Martin found P1 uninteresting as it stood and asked for ways to improve it. Claude set up a "council" of
five AI reviewers. Each one read the repository and judged the same list of eight possible improvements
from one point of view, then voted for its top three.

| Reviewer | What it cared about | What it did |
|---|---|---|
| Course grader | What the week 8 grading text rewards | Read the live week 8 page |
| Political scientist | What is already known | Searched for and read summaries of prior work |
| Data journalist | What a stranger would remember | Read the 280 sampled press releases |
| Feasibility engineer | What fits in the hours we have | Measured the data files |
| Sceptic (networks and text methods) | Whether a result could be trusted | Read the pilot scripts for flaws |

**These are five AI opinions, not five people.** They are useful for finding weak spots. They are not
evidence, and the group should argue with them.

---

## 4. The vote and the recommendation

### The eight options

| | Option | The idea |
|---|---|---|
| A | Hidden and showcase ties | Name the cross-party partnerships that are advertised at home, and the ones that never are |
| B | Works with them, attacks them | Sort each mention into praise, attack or neutral |
| C | The clock | See whether the showing changes as the election gets closer |
| D | The Trump node | Who stops naming Trump at home |
| E | Is it mutual? | When a Republican shows a Democrat, does the Democrat show them back? |
| F | Both parties | Run the same test on Democrats in Trump-won districts |
| G | Two maps of Congress | Compare the Congress members talk about with the Congress that works |
| H | Drop the scrape | Use only the data we already have |

### The result

Three points for a first place, two for a second, one for a third. A veto means "do not do this".

| Option | Points | On how many of 5 ballots | Vetoes |
|---|---|---|---|
| **G. Two maps of Congress** | 8 | 5 | 0 |
| **B. Works with them, attacks them** | 8 | 4 | 1 |
| **A. Hidden and showcase ties** | 7 | 3 | 1 |
| Write-in: fairer comparison (fix 1 below) | 3 | 1 | 0 |
| Write-in: backed "bipartisan" | 2 | 1 | 0 |
| E. Is it mutual? | 2 | 1 | 1 |
| C. The clock | 0 | 0 | 2 |
| D, F, H | 0 | 0 | 0 |

**G wins.** It tied B on points, but it is the only option every reviewer voted for and nobody vetoed.

### The recommendation, part by part

**1. Make the two maps (G) the main question.**

- **What it is.** Draw Congress twice. In the first map, two members are joined if one names the other in
  a speech. In the second, they are joined if one signs the other's bill. Then measure how strongly each
  map splits into a red side and a blue side.
- **Why.** Nobody can guess the answer. Earlier research points both ways: one study suggests public talk
  is more partisan than quiet cooperation, another suggests it is less. A question whose answer we cannot
  guess is what the grading text calls interesting.
- **What it improves.**
  - It uses the network half of the course properly: two networks on the same members, compared against
    a random baseline. The week 8 page's own example of a good result has this shape.
  - It runs on data we already have. If collecting press releases goes badly, we still have a paper.

**2. Use the press releases (A) as the close-up.**

- **What it is.** After the big picture, zoom in on named pairs. Which Democrats does a Republican put in
  front of voters?
- **Why.** People remember names, not percentages. Two examples from the sample:
  - Of their ten strongest Democratic partners, Lawler names 1 in his press releases and Bacon names 8.
  - The Democrats that hard-line Republicans do show are not moderates: Chip Roy with Steve Cohen on
    presidential emergency powers, Andy Biggs with Pramila Jayapal on bank surveillance.
- **What it improves.** It gives the paper and the three-minute talk something concrete.
- **A limit we must keep.** We can say who is *shown*. We cannot say who is *hidden*. Forty press releases
  per member is too few to tell "never mentioned" from "not mentioned in this sample".

**3. Keep the language work small and by hand (a cut-down B).**

- **What it is.** Two of us read a sample of mentions and label each one as agreeing, disagreeing or
  procedural. P1 already plans this as its sub-question 4.
- **Why not an automatic praise/attack classifier.** There is very little attack to find. In press
  releases, the attacks are aimed at Hochul, Biden or party leaders, not at the colleagues a member works
  with. On the floor, a simple word list finds negative words near only about 4% of cross-party mentions.
- **What it improves.** It gives the text half real substance beyond matching surnames, and the grading
  text rewards a hand-labelled sample with its agreement score reported.

**4. If there are hours left: check the word "bipartisan".**

- **What it is.** For each press release that says "bipartisan", check whether it names a colleague from
  the other party whom the member really works with.
- **Why.** The closest earlier study (Westwood) found that members use the word "bipartisan" whether or
  not they behave that way. This test extends his finding from a word to real partners. Lawler uses the
  word in 98% of his releases.

### What to drop

- **C, the clock.** Under two press releases a month per member is too thin to see change over time. Both
  earlier time comparisons in this repository turned out to be calendar effects (sections 4.1 and 4.2 of
  Anas's file).
- **E and F.** Both need many more press-release sites, and collecting is the scarcest thing we have.
- **D, the Trump node.** Trump signs no bills, so he has no place in the working network.
- **H, drop the scrape.** It removes the voter-facing text, which is the one thing earlier research does
  not have. The two maps already give us a fallback.

---

## 5. Three fixes to P1

These are needed whichever additions the group picks.

### Fix 1. The comparison is not fair as written

**The problem, in plain words.** Suppose you want to know whether a pupil brags about working with the
other group. You read their letters home. But the letters are almost all about *their own* projects, and
they name whoever led the project with them. So the letters can only ever name project co-leaders.

Comparing those names with *everyone the pupil ever helped* is unfair. A pupil who leads many mixed
projects will name many pupils from the other group, without bragging at all.

**In our data.**

- A press release usually announces a bill the member leads, and names the co-leads.
- P1's baseline draws from all of a member's cosponsorship partners. Most of those are members whose
  bills they signed, which never get a press release.
- So a swing-seat Republican could seem to "over-show Democrats" only because they lead more bills
  together with Democrats.

**The fix.**

- Match each press release to its bill by the bill number (H.R. 1234). This is far more reliable than
  matching surnames.
- Mark each named colleague as a co-lead of that bill or not.
- Then ask two fairer questions:
  - Of a member's own bills, which ones get a press release? Are the bipartisan ones announced more
    often than a random pick of their bills?
  - Among named colleagues who are *not* co-leads of the announced bill, does P1's original test still
    show a gap?

**What it improves.** Without this, a reviewer can explain our main result away in one sentence. With
it, the result means what we say it means.

### Fix 2. The name finder cannot see about one member in seven

**The problem.** The pilot scripts find a member by surname, and only when the surname is unique.

- 56 of the 450 members share a surname with another member (Johnson, Smith, Moore, Biggs and others).
  They can never be matched. That includes the Speaker, Mike Johnson, who is the most-named member on
  the floor once he can be seen.
- 11 members have a surname of more than one word (Van Drew, Wasserman Schultz, De La Cruz). The
  floor-speech pilot only looks at the last word and loses them.
- Nothing stops a senator or an official with the same surname from being counted as a House member.

**Why it matters.** The missing members are not a random handful. Andy Biggs is one of the seven sampled
members, and his ties cannot be matched at all.

**The fix.** The prototype notebook already does part of it: it matches full multi-word surnames, and it
settles a shared surname by a first name in the text or by the member's state mentioned nearby. That
recovered 765 mentions. Another 717 were still unclear and were dropped.

### Fix 3. The collector throws away the text

**The problem.** `press_pull.py` keeps only the first 200 characters of each press release. It keeps no
full text, and for 86 of the 280 releases no full date.

**Why it matters.** Without the text we cannot read how a colleague is described, cannot find the bill
number for fix 1, and cannot check a match by reading it.

**The fix.** Change the collector to store the whole text, the date and the sentence around each name.
It is about two hours of work and should happen before any more sites are collected. There is also a
small bug to fix at the same time: the script turns "Davis's" into "Davi".

---

## 6. The prototype: two maps of Congress

Notebook: `prototype_two_maps.ipynb`. Figure: `figures/prototype_two_maps.png`. It reads only
`data/processed/` and takes about five minutes to run. Section 0 of the notebook lists every modelling
choice with its alternative.

### What was measured

- **Named map.** Two members are joined if one names the other in a House floor speech. 7,931 mentions
  gave 3,718 ties among 441 members.
- **Working map.** Two members are joined if one signed a bill the other sponsored.
- **How divided a map is.** Two numbers:
  - **Cross-party share:** of all ties, how many join a Republican and a Democrat.
  - **Party modularity:** how much more the ties stay inside a party than chance predicts. Zero means
    party does not matter. Higher means more divided.
- **The baseline.** Shuffle the ties at random while every member keeps the same number of ties. If the
  real map is no more divided than the shuffled ones, party does not matter. This is the
  degree-preserving null from week 2.
- **A fair comparison.** A map with more ties looks less divided for that reason alone. So the working
  map is cut down to its strongest ties until it has exactly as many ties as the named map.

### What came out

| Map | Ties | Cross-party share | After shuffling | Party modularity |
|---|---|---|---|---|
| Named on the floor | 3,718 | 34% | 50% | 0.15 |
| Named, yields dropped | 3,249 | 38% | 50% | 0.11 |
| Named, yields and leadership titles dropped | 2,717 | 39% | 50% | 0.11 |
| Working, strongest ties, same size as named | 3,718 | 12% | 43% | 0.30 |
| Working, backbone α = 0.05 | 2,328 | 15% | 49% | 0.34 |
| Working, all ties | 46,513 | 29% | 50% | 0.21 |

- **Both maps are split by party.** No shuffled map comes close: the largest modularity in any shuffle
  is 0.03.
- **The named map is much less split.** At the same size, about one named tie in three crosses the party
  line, against about one working tie in eight.
- **Two boring explanations were tested and did not remove it.**
  - *Yields.* A member handing speaking time to another names them, and this goes mostly to their own
    side. Dropping these makes the named map less split, not more.
  - *Courtesy.* Speakers routinely thank a committee's chairman and its ranking member, who are from
    opposite parties. Dropping every mention made with such a title (20% of mentions) barely changes
    the number.

### Why not to trust it yet

- **Naming someone is not working with them.** Members name opponents to argue with them. "I cannot agree
  with Chairman Cole" is in the sample. If most cross-party mentions are disagreement, the finding is
  "members talk across the aisle to argue", which is a different and still interesting story. Reading a
  sample by hand decides this (recommendation 3).
- **Part of the gap comes from how the working map is cut.** Keeping only the strongest ties (six shared
  bills or more) picks close allies, who are mostly in the same party. With all ties kept, 29% cross the
  party line, much closer to the named map.
- **The name finder makes mistakes.** The notebook prints 30 random matches to read. Nobody has counted
  them. One is clearly wrong: "Mrs. Peters", a constituent, was matched to Rep. Scott Peters.
- **The baseline may be too easy.** A floor debate always has one manager from each party speaking in
  turn. A baseline that keeps "who spoke in the same debate" fixed would be a harder test.
- **This is the Washington picture only.** Floor speeches are not written for voters. The voter-facing
  half still needs the press releases.

---

## 7. What this would change in the plan

| | P1 as proposed | With this review |
|---|---|---|
| Main question | Do members show voters a selected picture of their partners? | Is the Congress members talk about more or less divided than the Congress that works? |
| Role of press releases | The main test | The close-up, and the voter-facing layer of the two maps |
| Role of floor speeches | A comparison | One of the two main maps |
| Baseline for the press-release test | All cosponsorship partners | The member's own bills, matched by bill number |
| If the collection fails | No main result | The floor map against the working map still stands |

**Before Wednesday 18 November, if the group agrees:**

- Change the collector to keep the full text (fix 3), before collecting more.
- Count the 30 printed matches in the notebook, and label a first sample of cross-party mentions as
  agreeing, disagreeing or procedural.
- Ask the teachers whether "naming against working" counts as enough language analysis.

---

## 8. Verified, not verified, and how this was made

**Checked on 13 November 2026**

- Every number in section 6 is printed by `prototype_two_maps.ipynb` on `data/processed/` as committed.
- 56 of 450 members share a surname and 11 have a multi-word surname (counted in `members.csv`).
- The collector stores 200 characters per release (stated in `Anas_Claude/README.md`).

**`[UNVERIFIED]`**

- **Everything the five reviewers reported that is not listed above.** Martin and Claude did not recheck
  it. This includes: Lawler naming 1 and Bacon 8 of their ten strongest Democratic partners; the
  Roy-Cohen and Biggs-Jayapal examples (read from 200-character headers, not full releases); the 4%
  negative-word figure; the 86 releases without a full date; the "Davi" bug.
- **What the prior work found.** The political-scientist reviewer read summaries, not the papers. The
  Westwood paper was behind a paywall. It appears to have been published in 2022, not 2021 as cited in
  Anas's file. How to check: read the abstracts.
- **The claim that nobody has compared named colleagues with cosponsorship ties.** One search session
  found no such study. That is not proof there is none.
- **The prototype's name finder:** precision and recall not measured.
- **The prototype's result:** one run, definitions chosen on the day.
- **The vote.** Five AI reviewers given a list written by Claude. A different list or different reviewers
  could give a different winner.

**How this was made.** Claude (Anthropic) read the repository, ran five subagents as the council on 12
November 2026, tallied their ballots, and built and ran the prototype notebook on 13 November. Martin
directed the review, asked for the council and the prototype, and chose to share it. The recommendation
is meant to be argued with.
