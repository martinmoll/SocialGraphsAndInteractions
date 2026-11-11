# Project outline: Walk or talk?

A working outline for the project in **02805 Social Graphs and Interactions** (DTU, autumn 2026).
Group: Anas Mir, Martin Møllenhus, Diego A. Mijares.

**Status (11 November 2026): an outline, not a decided project.** We have gathered data around one topic of
interest, the 2026 US midterms, and tried one question on it. The research question, the datasets, the figures
and the story are all still open to change. Nothing here has been agreed by the whole group or shown to the
teachers.

This folder is separate from the weekly exercises in the rest of the repository (`posts/`, `Notebooks/`,
`Figures/`, `Data/`). It was built in one day to see whether the topic can carry a paper. This file records what
was tried, what was found and what is still open, so that work can continue from here.

**Other angles we have not explored yet** (see section 11):

- How the Trump administration's decisions (for example the Iran war and the financing of Israel) damaged the
  Republicans' case.
- Sentiment in members' newsletters: how it related to their results, and whether the tone of Republicans and
  of Democrats changed over the period.

---

## 1. The idea in one paragraph

In the midterm elections of 3 November 2026 the Democrats won the US House by a wide margin. We ask which
Republican House members held up best. The network half of the course gives one answer (who *worked* with
Democrats), the language half gives another (who *sounded* less partisan), and the election gives a ground truth
that neither half produced.

**Research question.** Among Republican House members who stood for re-election in 2026, did the ones who
cooperated across the aisle, or the ones who sounded less like their party, run ahead of their district?

| | What we build | Score | Course tools |
|---|---|---|---|
| **Walk** (networks) | Cosponsorship network of the 119th House: a link from each cosponsor to the bill's sponsor | Share of a member's cosponsorships that go to the other party | Directed weighted network, label-shuffle null, modularity, Louvain, NMI |
| **Talk** (language) | Every member's floor speeches from the Congressional Record | How Republican the member's vocabulary is, with their own speeches held out | Tokenisation, stopwords, word rates, the week-6 two-group comparison, concordance |
| **Verdict** | 2026 result per district | Margin minus what the district's lean predicts | Shuffle null within groups of similar districts |
| **Zoom-in** | One member chosen by a rule | Who they cosponsor with, which words set them apart | Ego network, word comparison |

The intended story has four steps: (1) the network is split by party, (2) so is the vocabulary, (3) do the two
agree on *who* in the party is the outsider, (4) and does the election say that either mattered. Section 6 says
how far the prototype supports each step.

## 2. What the course asks for

Source: <https://sunelehmann.com/socialgraphs2026-web/weeks/week8.html> (read 11 Nov 2026).

- **Paper:** PNAS LaTeX template, at most six pages including figures and references. Abstract, Significance
  Statement, Introduction, Results, Discussion, Methods, References, specific author contributions.
- **Slides:** three slides, three minutes, then questions. Anyone in the group can be asked anything.
- **Reflection:** half a page, ungraded.
- **Deadlines:** hand-in Friday **27 November 2026, 23:59**; presentations Wednesday **2 December 2026**.
  Project sessions on 11, 18 and 25 November. The course's dataset lock was 4 November, so check with the
  teachers that a choice made on 11 November is fine.
- **Graded on (0–3 each):** research question; data and scope; showcasing the course; analysis and checks;
  figures; references and literature; overall impression; presentation and questions.
- **Dataset test from the page:** both halves present; a few hundred to a few thousand nodes; obtainable
  without too much effort; a domain we care about; something unknown about it.
- **The page's own warnings:** the question comes before the method; one story, not a pile of techniques;
  two or three figures; every measurement gets one sentence on what it captures and one on what it misses;
  every claim gets a check (a null, a second method, or a hand-labelled sample).

## 3. Why this project, and what speaks against it

**For**

- Both halves do real work, and each measures something the other cannot.
- The election is an outside ground truth. Most projects in this course have none.
- 450 nodes: inside the course's recommended range.
- Four sources joined on one shared ID, on an event one week old. Little chance another group has it.
- All data are public and about elected officials acting in public. The two largest sources (bills and the
  Congressional Record) are US government publications.
- The checks the course grades are built in: a shuffle null, a second method (roll-call scores), hand-read samples.
- Half the story (walk against talk) needs no election data, so it survives if the results stay messy.

**Against**

- The idea is not new. Whether members who vote with their party less do better at the polls is an established
  research topic (see section 10). Our contribution is the 2026 data and setting cooperation against language.
- The headline result is weak (section 6). District lean explains 83% of the variation in margins.
- The talk score is noisy: two halves of the same member's speeches agree only moderately (section 6).
- Only 30 Republicans in the study lost. Anything about "who lost" rests on a small group.
- Nothing here is causal. Members in swing districts cooperate more *and* lose more.
- Floor speeches are a narrow kind of text: a lot of tributes, local mentions and bill management.
- Election counts are unofficial and still moving. Eight Republican races were not called on 11 November.
- 16 days were left when this was written.

## 4. Data

All tables are keyed by **Bioguide ID**, the identifier every source shares, so nothing is joined by name inside
the notebook. All downloads were made on **11 November 2026**.

| Source | What it gives | Address | Size after cleaning |
|---|---|---|---|
| govinfo bulk data, BILLSTATUS | Sponsor and cosponsors of every House bill | `govinfo.gov/bulkdata/BILLSTATUS/119/<type>/BILLSTATUS-119-<type>.zip` | 12,987 bills and resolutions, 149,015 cosponsorships |
| Congressional Record (govinfo) | Text of House floor speeches and written Extensions of Remarks | `govinfo.gov/metadata/pkg/CREC-<day>/mods.xml` and `govinfo.gov/content/pkg/CREC-<day>/html/<item>.htm` | 31,421 items on 339 days; 35,629 speaker turns; 8,421,560 words attached to a member |
| Voteview | Member list for the 119th House and roll-call (NOMINATE) scores | `voteview.com/static/data/out/members/H119_members.csv` | 451 members (226 R, 224 D, 1 I), including those who left mid-term |
| unitedstates/congress-legislators | Full names of current members | `unitedstates.github.io/congress-legislators/legislators-current.json` | 539 members of both chambers |
| NBC News results feed | Votes per candidate in every House district | `nbcnews.com/firecracker/api/v2/state-results/2026-elections/<state>-house-results` | 435 districts, 50 requests |
| Wikipedia | District lean (Cook PVI), incumbent, what happened to them, redrawn states, list of defeated incumbents | Page "2026 United States House of Representatives elections", wikitext via the API | 435 districts, 424 incumbents matched |

- The NBC address is the request NBC's own results pages make. It is undocumented, unofficial, and it changes
  as counting finishes. A dated snapshot is kept in `data/raw/nbc_2026-11-11/`.
- The Wikipedia page also changes daily. A dated snapshot is kept in `data/raw/`.
- No API key was needed for any of this. (The govinfo *API* needs a key; the bulk and content addresses do not.)

### Folder layout

```
project/
  readme.md                 this file
  walk_or_talk.ipynb        the prototype: every reported number is computed here
  figures/                  fig1–fig4, written by the notebook
  scripts/
    roster.py               member list + name matcher, shared by the scripts
    01_fetch_record.py      downloads the Congressional Record
    02_fetch_bills.py       downloads bills, writes bills.parquet and cosponsors.parquet
    03_fetch_results.py     downloads NBC results, parses Wikipedia, writes members/districts/incumbents
    04_parse_record.py      splits the Record into speaker turns, writes speeches.parquet
  data/
    raw/                    downloads as they came (285 MB). Not in the repository, except record_index.csv;
                            the scripts rebuild the rest
    processed/              the tables the notebook reads (15 MB)
```

To rebuild from nothing, run the four scripts in order from the `project` folder, then the notebook:

```bash
python scripts/01_fetch_record.py
```
```bash
python scripts/02_fetch_bills.py
```
```bash
python scripts/03_fetch_results.py
```
```bash
python scripts/04_parse_record.py
```

- `01` is the slow one: roughly half an hour on our connection (not timed precisely). It needs about 530 MB of
  temporary space for metadata, which it puts in the system temp folder, not in the project.
- `03` reuses the dated NBC and Wikipedia snapshots if they exist. Delete them to fetch fresh results; the numbers
  will then change.
- Environment used: Anaconda `base`, Python 3.14.6, pandas 3.0.3, networkx 3.6.1, scikit-learn 1.9.0, pyarrow 23.
- The notebook needs only `data/processed/` and `data/raw/record_index.csv`, so it runs straight from the
  repository. The scripts are needed only to refresh or extend the data.
- `project/.gitignore` keeps the rest of `data/raw/` out of the repository if you run the scripts in a clone.
- The notebook itself was generated by a throwaway script and then run; from here on, edit the notebook directly.

## 5. Definitions

These were written down **before** the election results were joined to the scores. They live as named
parameters in the first code cell of the notebook.

**Study population.** Republican House members who were on the November ballot as the only incumbent, against
exactly one Democrat, in a race NBC had called. That is 162 members: 132 held their seat, 30 lost.
Left out, and listed in the notebook: 40 who did not run or lost a primary, 8 in uncalled races, 4 in contests
that were not one Republican against one Democrat. Four Republicans who lost are outside the study for those
reasons (Young Kim, Lauren Boebert, Greg Murphy, Virginia Foxx).

**Walk.** Bills and joint resolutions only (`hr`, `hjres`); withdrawn cosponsorships dropped; no cap on bill
size. Score = share of the member's cosponsorships whose sponsor is in the other party. Needs at least 10
cosponsorships.

**Talk.**
1. Speaker turns of at least 50 words, from the House section and from Extensions of Remarks.
2. Lower-case, letters only, three letters or more.
3. Removed: ordinary English stopwords; a hand-written list of procedural House words; members' first and last
   names; state names; months and weekdays.
4. A word is kept if at least 20 members use it (9,337 words).
5. A word's rate in a party is the average of its members' own rates per 10,000 words, so every member counts once.
6. Word partisanship = log2((Republican rate + 0.1) / (Democratic rate + 0.1)).
7. A member's talk score is the count-weighted average partisanship of their words, computed with their own
   speeches left out of their party's rates. Rescaled so the average Democrat is −1 and the average Republican +1.
8. Needs at least 3,000 words.

**Outcome.** Two-party margin in points from raw votes: 100 × (R − D) / (R + D). Overperformance = margin minus
a straight-line prediction from district lean, fitted on the study population.

**Test.** Spearman correlation of overperformance with walk and with talk. Null: shuffle overperformance among
members in districts of similar lean (five equal groups), 5,000 times.

**Rule stated in advance.** If neither correlation falls outside the middle 95% of its null, we report "no
detectable relation".

**Zoom-in rule.** The Republican who ran furthest ahead of a district leaning at most R+5 and who has both scores.

## 6. What the prototype found

Numbers from the notebook run of 11 November 2026 on the complete downloads. They will change when the results
feed is refreshed.

**The network (walk)**

- 450 members, 62,292 directed links from 126,687 cosponsorships on 8,714 bills. Density 0.31.
- 21% of cosponsorships cross the aisle. If party were irrelevant it would be 50% (label-shuffle null 0.501 ± 0.003).
- Louvain finds 2 communities; agreement with party NMI = 0.79; modularity 0.292 (plain party split: 0.269).
- Median walk: Republicans 0.11, Democrats 0.20.
- Party split against a null: the modularity of the plain party split is 0.269; with party labels shuffled it
  is −0.002 ± 0.003 (200 shuffles).
- Changing the definition: rank correlation with the main score is 0.99 using all four bill types, 0.96 using
  only bills with at most 50 cosponsors, and 0.79 when cosponsors a member *received* are counted too. So the
  choice of bills hardly matters; the choice of direction does somewhat.
- Second method: among Republicans, walk against the roll-call ideology score gives ρ = −0.79 (n = 223).

**The language (talk)**

- 24,860 turns kept; 414 members have enough text (208 Republicans, 206 Democrats); median 12,702 words each.
- With a member's own speeches held out, the sign of the talk score matches their party for 92.5% of members.
- Most Republican words include *aliens, unborn, ccp, bureaucrats, cartels, biden, obamacare, border*.
  Most Democratic words include *musk, billionaire, tariffs, cruelty, maternal, disparities, lgbtq, racial*.
- Within the Republican party, talk tracks ideology only weakly: ρ = +0.24 with the roll-call score.
- **It is noisy.** Scoring each member's odd-day and even-day speeches separately, the two halves correlate at
  ρ = 0.41 among Republicans (n = 185), which implies a reliability of about 0.58 for the full score.
- It does carry some signal. By fifth of the roll-call score, mean talk runs 0.78 (least conservative), 1.00,
  1.08, 1.11, 1.09 (most conservative): the most moderate fifth sounds least like the party, and the other four
  cannot be told apart. Walk over the same fifths runs 0.26, 0.15, 0.12, 0.09, 0.05, a much cleaner gradient.

**Walk against talk** (no election needed)

- Among 206 Republicans with both scores, ρ = −0.20. Loosely related, in the expected direction.
- With a talk score this noisy, much of the disagreement between the two is measurement error. The members the
  notebook names as mismatches are the ends of a ranking, which always has ends:
  - high talk, high walk: Garbarino (NY), Bice (OK), Nunn (IA), Rutherford (FL), Baird (IN), Evans (CO);
  - low talk, low walk: Roy (TX), Norman (SC), Brecheen (OK), Greene (GA), Fine (FL), Harris (MD).
- The second list is all hardliners, which is suggestive, but the table by fifths above does **not** show the
  most conservative members sounding unlike the party as a group. Treat the lists as leads to read up on.

**The verdict**

- District lean alone explains 83% of the variation in margins. A district with even lean is predicted at −11.2
  points for the Republican, which is the size of the wave in this group.
- **Walk:** ρ = +0.14 (n = 162), inside the null band (−0.10 to +0.17), p = 0.10. No detectable relation.
- **Talk:** ρ = −0.20 (n = 154), outside the null band (−0.17 to +0.14), p = 0.018. Republicans who used more
  of the party's vocabulary ran slightly behind their district.
- How well the talk result holds up:
  - spoken floor turns only: ρ = −0.23 (n = 133), p = 0.006;
  - place and person words removed: ρ = −0.19 (n = 154), p = 0.027;
  - **without the nine redrawn states: ρ = −0.16 (n = 95), p = 0.17. It no longer clears the band.**
  - fitted together with lean and walk: about −1.2 points of margin per standard deviation of talk, against
    +13.9 for lean.
- Among districts leaning at most R+10, losers had a *higher* mean walk (0.24) than survivors (0.14). That is not
  an effect of cooperating: losers sat in closer districts (mean lean 3.0 against 8.1).

**In one sentence:** the network half is solid; the language half separates the parties well but is a noisy
measure of where a member stands within the party; and the election link is small and not robust.

**Zoom-in by the rule:** Tom Barrett (MI-7), district lean even, lost by 3.4 points where the fit predicts
−11.2 (7.8 points ahead). As a case he is thin: his most frequent cosponsorship partner accounts for 6 bills.
Next on the list is Brian Fitzpatrick (PA-1), 7.6 points ahead, with a walk score of 0.71, the highest of any
Republican. The rule should be reconsidered.

### Figures

| File | Shows | Likely role in the paper |
|---|---|---|
| `fig1_party_words.png` | Each word's rate among Republicans against Democrats, log axes | Methods or figure 1b |
| `fig2_walk_vs_talk.png` | Walk against talk, one dot per member, mismatches named | Candidate main figure |
| `fig3_network_two_colourings.png` | The same network layout coloured by party and by talk | Candidate main figure |
| `fig4_verdict.png` | Overperformance against walk and against talk, losers ringed | Result figure |

They are prototypes. Labels overlap in places and nothing is sized for the PNAS column width.

## 7. How the work was done, including what was seen when

For honesty about how much the definitions could have been tuned:

1. The definitions in section 5 were written into the notebook before any result was joined.
2. The notebook was first run on a **partial** download of the Record (64% of items). That run already printed a
   verdict (walk ρ = +0.14, talk ρ = −0.21, both inside their bands).
3. After that run, these things were changed. None changes a definition in section 5:
   - the p-value is now measured from the centre of the null (it disagreed with the band before);
   - a member who "was renominated but withdrew" (Chuck Edwards, NC-11) is now counted as not running;
   - figure labels use surnames; figure 1 labels were spread out;
   - two extra ways of building talk were added as robustness lines (floor turns only; 14 place and person words
     removed after reading the word lists);
   - the zoom-in prints the Democratic-leaning words the member uses.
4. The next run used the complete Record. Talk moved from just inside its band to just outside it.
5. After a review of that run, three checks that do not involve the election were added: a shuffle null for the
   modularity of the party split, the split-half check of the talk score, and the table of talk and walk by
   ideology fifth. They use their own random stream or none, and the verdict numbers did not change.
   The split-half check and the table led us to withdraw an earlier reading ("hardliners also sound unlike the
   party"), which had been based on six names.

So the talk result has been looked at twice with different amounts of data, and several variants were computed
after seeing it. Read p = 0.018 with that in mind.

## 8. Verified and not verified

**Checked on 11 November 2026**

- Election facts (Democrats projected to win House and Senate; Talarico beat Paxton in Texas) against NBC, CBS,
  CNBC, KUT and Wikipedia.
- All 435 districts appear in both NBC and Wikipedia. Lean is present for all 435.
- NBC and Wikipedia agree on the winner in all 161 study races where Wikipedia had recorded a result (it had
  not yet for one).
- The redrawn-state list was read off Wikipedia's summary table: the nine states marked "New districts enacted".
  `03_fetch_results.py` prints every state's status when it runs.
- TX-1 spot check: 181,987 to 81,598, as on NBC's page.
- Wikipedia's list of defeated incumbents: 34 House Republicans, all matched to our rows (30 in the study, 4 outside).
- Cosponsor records carry Bioguide IDs; none is missing.
- 99.6% of Record words are attached to a member (29,747 words are not; see
  `data/processed/record_unresolved.csv`). **Two known gaps in the name matcher, both Democrats:** turns printed
  as "GRIJALVA" (12,825 words; two members with that surname held AZ-7 in this Congress, so the matcher refuses
  to guess) and "PEREZ" (6,682 words; Marie Gluesenkamp Perez, whose surname is stored in two parts). Neither is
  in the study population, but both should be fixed in `scripts/roster.py` before the paper.
- Three references in section 10 were looked up and exist as cited.

**`[UNVERIFIED]`**

- **Speaker assignment.** No human has checked it. `data/processed/speaker_check_sample.csv` has 60 random turns
  with links; fill in the last column and report the agreement in Methods.
- **Lean for redrawn districts.** Nine states changed their maps (AL, CA, FL, LA, NC, OH, TN, TX, UT, from the
  Wikipedia summary table). Whether the PVI on the page describes the new lines was not checked. The two largest
  outliers (De La Cruz, TX-15, and Valadao, CA-22) are both in redrawn states, which suggests it may not. How to
  check: compare with the Cook Political Report's own 2025/2026 PVI release.
- **Vote counts.** Unofficial. Median 99% counted, minimum 77%. Re-download before hand-in and state the date.
- **The word lists** were read once by the assistant, not by the group. Places and tribute words leak in
  (*guam, omaha, jacksonville, ffa, ucla*).
- **Whether speeches are "political enough".** 27% of words are written Extensions of Remarks, which are
  largely tributes.
- **Kessler (2017), Scattertext**, and **Monroe, Colaresi and Quinn (2008), "Fightin' Words"**: cited from
  memory, not looked up. Check before they go in the paper.
- The claim that nobody else has analysed this is an assumption.

## 9. Limits and caveats

- **Walk** captures who a member signs on with. It misses bills that never needed cosponsors, informal
  cooperation, and why someone signed (many swing-seat members cosponsor across the aisle for show).
- **Talk** captures vocabulary on the House floor. It misses what members say to voters (ads, newsletters,
  social media), tone, and stance: a word's side is not the speaker's position on it.
- **Topic and geography.** Members speak about their districts and committees, and those differ by party.
- **Majority party.** Republicans ran the floor, so procedural language leans Republican. A stop list removes
  the obvious part only.
- **Finite-sample bias.** Measures of partisan speech are biased upward when vocabularies are large and texts
  are short (Gentzkow, Shapiro and Taddy 2019). Holding out each member's own text addresses the worst of it.
- **Overperformance** is relative to a straight line through lean. It ignores challenger quality, money,
  scandals and local issues, all of which could matter more than walk or talk.
- **Selection.** Members who retired or lost primaries are not in the study, and they may have left because
  they expected to lose.
- **One election.** No claim about elections in general.
- **Louisiana** uses a different election system. Its districts with several candidates per party are excluded
  by the population rule.

## 10. Literature to start from

Looked up on 11 November 2026:

- Canes-Wrone, B., Brady, D. W., and Cogan, J. F. (2002). Out of Step, Out of Office: Electoral Accountability
  and House Members' Voting. *American Political Science Review* 96(1), 127–140. doi:10.1017/S0003055402004276.
  Finds that incumbents' vote shares fall as their party-line voting rises. This is the prior result our
  question extends.
- Fowler, J. H. (2006). Connecting the Congress: A Study of Cosponsorship Networks. *Political Analysis* 14(4),
  456–487. doi:10.1093/pan/mpl002. Defines the cosponsor → sponsor network we use.
- Gentzkow, M., Shapiro, J. M., and Taddy, M. (2019). Measuring Group Differences in High-Dimensional Choices:
  Method and Application to Congressional Speech. *Econometrica* 87(4), 1307–1340. doi:10.3982/ECTA16566.
  Measures partisanship of congressional speech and warns about finite-sample bias.

Not looked up (see section 8): Kessler 2017; Monroe, Colaresi and Quinn 2008. Also to find: the Voteview
citation the site asks for, and the course texts for Louvain, modularity and NMI.

## 11. Decisions the group has to make

0. **Which question.** "Walk or talk" is one question tried on this data, not the chosen one. Two other angles
   raised in the group and not yet explored:
   - **Administration decisions.** Did specific decisions of the Trump administration (for example the Iran war
     and the financing of Israel) damage the Republicans' case? The speech table has a date on every turn, so
     how often and how each party talked about a topic before and after an event can be measured with the data
     we already have. Which events, and how to tie them to results, is undecided.
   - **Newsletter sentiment.** Did the tone of members' newsletters relate to how they did, and did the tone of
     Republicans and of Democrats change over the period? We have no newsletter data yet: the one archive we
     found (DCinbox) needs an account. Sentiment would also need a hand-labelled check (week 7).
1. **Go or no-go.** Does everyone want this topic, and do the teachers accept a dataset chosen after 4 November?
2. **What the paper's main claim is.** Neither candidate is strong yet. (a) Walk against talk: the network score
   is solid, but the talk score is too noisy to carry a claim about individual members. (b) The election
   verdict: small, and not robust to dropping the redrawn states. A third option, (c): "cooperation and
   vocabulary both mark party, but only cooperation marks position within the party, and neither bought votes
   in 2026" is what the evidence supports today. It is an honest, mostly negative result.
3. **Can the talk score be made more reliable?** More text per member (press releases, newsletters), fewer and
   better-chosen words, or phrases instead of single words. Without this, step 3 of the story is weak.
4. **Is floor speech the right text?** Alternatives: press releases, newsletters (DCinbox needs an account),
   social media. Each costs days.
5. **Strip more from the vocabulary?** Places, tribute language, bill names. Decide by reading the lists, and
   decide before looking at the verdict again.
6. **Thresholds:** 3,000 words, 50-word turns, 20 members per word, bill types. All are parameters in cell 1.
7. **Redrawn states:** keep, drop, or find the correct lean.
8. **Zoom-in rule and case.**
9. **Scope:** Republicans only, or Democrats too. Among Democrats walk and talk agree much more visibly (figure 2).
10. **Who does what:** data refresh, speaker hand-check, word-list reading, figures, writing.

## 12. Next steps if we go ahead

1. Hand-check the 60 sampled turns. Read the top 100 words per side and settle the stop lists.
   Fix the two name-matcher gaps (section 8).
   Add a null for the Louvain modularity itself (0.292 has none yet; only the party split does).
2. Verify or replace the lean figures for redrawn districts.
3. Re-download results close to the deadline; record the date.
4. Decide the main claim and cut to two or three figures.
5. Start the PNAS Overleaf template now and write into it.
6. Read the three references and find three or four more.
7. Prepare the three slides: question and data; main figure; meaning and checks.

## 13. Ideas we set aside

The course page says to keep the alternatives in case the chosen one fails.

- **US Supreme Court oral arguments.** Does the way a justice questions each side give away their vote?
  Transcripts with speaker names and each justice's vote from `api.oyez.org` (one 2022 case sampled: 420 turns,
  19,201 words, 9 votes). Cleanest ground truth; few justices, so lawyers must be the nodes.
- **Football playmakers.** Does a player Wikipedia calls a "playmaker" sit at the centre of the passing network?
  StatsBomb open data (2022 World Cup, 64 matches) plus 831 Wikipedia player pages. This was the first idea.
- **Rap disses.** Do rappers diss former collaborators? Wikipedia's list of diss tracks (about 400 rows) plus
  MusicBrainz collaborations. Lyric access not tested.
- **Wikipedia clicks.** Do readers of contested topics click toward similar pages or toward the debunking?
  Monthly clickstream files (October 2026: 468 MB).

## 14. How we got here

- Started from football statistics against how players are described. Problem: statistics are attributes, not a
  network.
- Considered the four alternatives above.
- The 2026 midterm result suggested a political project. "Why did the tide turn?" cannot be answered from one
  election, so the question became who lost less ground.
- Two wishes shaped the design: a general question followed by one zoomed-in case, and a party-word comparison
  like the 2012 convention figure in week 6. The word comparison became the instrument for the talk score.
- Data checks on 11 November settled it: cosponsors, speeches, margins and lean were all obtainable in a day.
