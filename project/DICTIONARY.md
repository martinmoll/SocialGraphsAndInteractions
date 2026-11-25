# Dictionary: the words we use in "Two maps of Congress"

Started by Anas on 19 November 2026; **updated 25 November 2026 to the final versions of all three parts** (the
paper in `report/sections/`, `Martin/README.md`, `Diego/README.md`, `Anas/README.md`) and moved from `Anas/` to the
project folder so all three of us use it. If a definition here disagrees with `DECISIONS.md` or the paper, those
win; fix this file.

Each entry gives the plain meaning first, then how we use it. Numbers are the final ones (frozen 22 Nov). Words
used only while planning are kept at the end of their section, marked *(planning only, not in the paper)*, so old
files still make sense.

Sections:

1. Congress and elections
2. Bills and cosponsorship (the working map)
3. Floor speeches (the floor map)
4. Press releases (part 3: the close-up and the home map)
5. Networks and null models
6. Text, matching and labelling
7. Statistics and research design
8. How the group works

---

## 1. Congress and elections

| Term | Meaning |
|---|---|
| Congress | The US parliament. It has two chambers, the House of Representatives and the Senate. We study only the House. |
| 119th Congress | The two-year term of Congress that started on 3 January 2025 and runs to January 2027. All our data are from this term. |
| House of Representatives (the House) | The larger chamber. Its members are elected every two years, each by one district. |
| Senate, senator | The smaller chamber: 100 senators, two per state. Senators are not in our networks. They can still slip into our data because they are named in House texts, sometimes with the same surname as a House member (Collins); the matcher skips names after "Senator". |
| Member, representative, congressman/congresswoman | One person elected to the House. In our files every member is a node. |
| Seat | One place in the House, won by one person in one district. The House has 435 voting seats, one per district, plus 6 non-voting delegates. "Exposed seat" and "safe seat" describe the district, not the person. |
| District (congressional district) | The area of a state that elects one House member. States are cut into districts by population, so California has 52 and Alaska has 1. `districts.csv` has 435 rows, one per voting seat. |
| At-large district | A state with only one district. It is stored as district `0` (Alaska, for example). |
| Delegate | A non-voting House member for DC, Puerto Rico, Guam, the US Virgin Islands, American Samoa or the Northern Mariana Islands. All six are in `members.csv` with `current = False`. They have no district lean. |
| Why "450 members" | `members.csv` has 451 people: 433 current members (FL-20 and TX-23 were vacant), plus 18 not current: the 6 delegates and 12 members who left during the term. Of the 451, 226 are R, 224 D and 1 independent (Kiley). The two maps use the **450 Republicans and Democrats**; Kiley stays in the files. |
| State delegation | All the House members from one state. Delegations range from 1 seat (6 states) to 52 (California). The four largest (CA, TX, FL, NY) hold a third of all seats. |
| Party | R (Republican), D (Democrat), I (independent). |
| Majority, minority | The party with more seats controls the House: it elects the Speaker, chairs every committee and decides which bills reach the floor. In the 119th Congress the Republicans are the majority. Part 3 names it as one possible reason why exposed Republicans and Democrats bridge differently (not tested). |
| Speaker | The leader of the House, elected by the majority. Mike Johnson (R). Named very often, mostly for procedural reasons. |
| Party leaders | The seven members in the House leadership list (Speaker, majority and minority leaders, whips, conference and caucus chairs; `Anas/a3/leaders.csv`). Their names are everywhere for reasons that have nothing to do with partnership, so part 3 leaves them out as the named member. On the floor map the eighth community gathers them. |
| Committee, chairman, ranking member | Bills are worked on in committees. The chairman is from the majority; the ranking member is the most senior minority member. "Thank Chairman Cole and Ranking Member DeLauro" is a routine courtesy. The floor map's communities follow committees (part 1). |
| Midterm election | The House election halfway through a president's term. The 2026 midterm was on 3 November 2026. It is the setting, not the outcome: we do not explain who won. |
| President's party | The party of the sitting president: the Republicans (Trump) in 2025-26. Part 3 asks whether naming the other party is about being in the president's party or about having an exposed seat. |
| Incumbent | The person who currently holds the seat. `incumbents.csv` records who held each seat and what happened to them in 2026. |
| Redistricting, redraw, redrawn state | Redrawing the borders of a state's districts, normally once a decade. Nine states (AL, CA, FL, LA, NC, OH, TN, TX, UT; 173 seats) drew new maps for the 2026 election, so a member's 2026 district can be a different area from the one they served, even with the same number. |
| Served district, 2026 district | The served district is the one a member represented in 2025-26. The 2026 district is the one they ran in. They are the same area except in redrawn states. Part 3 uses the **served** district: the releases were written for its voters. |
| Voteview, DW-NOMINATE | Voteview is a public database of how every member voted, and our source for the member list. DW-NOMINATE: see "Ideology" below. |
| Roll call | A recorded vote where each member's yes or no is written down. |
| Bioguide ID | The official ID of every member of Congress, such as `B001323` (Begich). Every table we have is joined on it. |

### District lean and exposed seats

| Term | Meaning |
|---|---|
| District lean | How Republican or Democratic a district votes, compared with the country as a whole. We use the 2025 Cook PVI as a signed number: positive leans Republican, negative Democratic (Alaska's `6` is R+6). `lean_2025` is the lean of the district served (`Anas/district_lean/member_lean.csv`, read from the Wikipedia revision of 25 May 2025, before any redraw); `lean_2026` (`districts.csv`, column `lean`) is the 2026 map. Never join `districts.csv` to members by district number. |
| Cook PVI (Partisan Voting Index) | A measure of lean from the Cook Political Report: how a district voted for president in the last two elections against the national result. R+6 means about 6 points more Republican than the country; EVEN means like the country. Cited as `cook2025pvi`. |
| Second lean measure | `pres_margin_2024`: Trump's 2024 margin on the districts members served (The Downballot, `downballot2024`). It agrees with the Cook lean at r = 0.999; one of part 3's robustness checks. |
| Exposed seat (the rule in the paper, G13) | The district the member served leans toward their own party by **5 points or less**, which includes seats leaning to the other party. A Republican with lean ≤ R+5, a Democrat with lean ≤ D+5. 91 of the 406 members in part 3 are exposed (37 R, 54 D). Agreed by Martin 23 Nov; text for `DECISIONS.md` in `Anas/G13_UPDATE.md`. |
| Safe seat | Every seat that is not exposed: the district leans toward the member's own party by more than 5 points. |
| Crossover seat | A district that leans to the other party: a Democrat holding an R-leaning seat, or a Republican holding a D-leaning seat (18 members in part 3: 8 R, 10 D). The most exposed seats, and where the naming gap is largest. |
| Relabelled members | 12 members whose exposed/safe label differs between the district served and the 2026 district, plus 9 with no 2026 contest in our data. Part 3 checks the result without these 21. |

### Ideology: a second, separate property of a member

Seat and ideology describe different things. **The seat is about the district's voters** (how the district voted
for president). **Ideology is about the member's own votes.** A member can be in an exposed seat and vote like a
hardliner. In practice the two go together, which is why check I was needed.

| Term | Meaning |
|---|---|
| DW-NOMINATE (first dimension) | A score for each member computed from all their roll-call votes, from about −1 (most liberal) to +1 (most conservative). From Voteview (`members.csv`, column `nominate_dim1`). It measures how a member votes, not what they believe or say. |
| Extremity | How far a member's score is from the centre in their own party's direction: the score for Republicans, minus the score for Democrats. Used to rank members within their party. |
| Moderate, extreme (within a party) | Members at the low or high end of extremity **within their own party**. Relative: a moderate Republican is still to the right of nearly every Democrat. 22 of 37 exposed Republicans and 27 of 54 exposed Democrats are in their party's most moderate fifth. |
| Ideology band | One fifth (quintile) of a party's members, ranked by extremity (thirds as a check). Check I shuffles the exposed label only within party and band. |

## 2. Bills and cosponsorship (the working map)

| Term | Meaning |
|---|---|
| Bill | A proposed law. `bills.parquet`: 12,987 House bills and resolutions of the 119th Congress, from govinfo's BILLSTATUS data. |
| Bill types | `hr` = H.R., a bill. `hres` = H.Res., a resolution of the House only. `hjres` = H.J.Res. and `hconres` = H.Con.Res., joint and concurrent resolutions. The working map and M6 use H.R. and H.J.Res. |
| Sponsor | The one member who introduces a bill. |
| Cosponsor | A member who signs on to support someone else's bill. `cosponsors.parquet` has 149,015 cosponsorships. |
| Original cosponsor | A cosponsor who signed on the day the bill was introduced (column `original`). They usually helped write it. |
| Withdrawn | A cosponsor who took their name back off the bill. Withdrawn cosponsorships are removed from the working map. |
| Co-lead | A bill's sponsor or a non-withdrawn original cosponsor. In part 3 a named colleague who co-leads a bill the release cites is named because of the bill, so the main outcome leaves co-leads out (a robustness row puts them back). In the home map co-leads count: a named partner is a tie. |
| Cross-party bill (M6) | A bill with an original cosponsor from the other party. |
| Policy area | The subject Congress staff give each bill (Health, Emergency Management, ...). |
| govinfo, BILLSTATUS | The US government's publishing site and its bulk data of every bill's status. Our bills, cosponsors and Congressional Record come from it. |
| Working tie | Two members are tied when one cosponsored a bill or joint resolution the other sponsored. |
| Working map | The network of all working ties: 46,513 ties on the 450 members. Whom members work with. |

## 3. Floor speeches (the floor map)

| Term | Meaning |
|---|---|
| The floor | The chamber where the whole House debates and votes. A floor speech is something said there, in public. |
| Congressional Record | The official daily transcript of everything said on the House and Senate floors, 6 January 2025 to 9 November 2026 in our data. |
| Speaker turn | One uninterrupted stretch of speech by one member. `speeches.parquet` has 35,629 turns; we keep the 17,824 House-floor turns of at least 50 words spoken by a member. |
| Speaker check (S2) | Is each turn credited to the right member? 60 of 60 random turns were (95% Wilson interval 94% to 100%). |
| Debate, Record item, `doc_id` | One item in the Record, usually the debate on one bill. The debate null shuffles names only inside one `doc_id`. |
| Floor manager | The member from each party who runs the debate on a bill and hands out speaking time. Every debate has one from each side, a built-in cross-party element. |
| Yield | Handing speaking time to another member: "I yield 2 minutes to the gentleman from Texas." Procedure, not a choice to name someone, so yields are left out of the headline floor map (G1b). With yields kept: 35.2% against 28.7%. |
| Yield rule | How code spots a yield: "yield" (not "yield back") before the name in the same sentence, or "for yielding" after it (G1c). On the 30 rows where it disagreed with an older 60-character window, 15 of 15 it alone flagged were yields. |
| "Will the gentleman yield?" | Asking the named member to give up time. Not a yield (G12): it addresses that member, usually mid-argument. |
| Unanimous consent | A request to do something without a vote. Often names members; coded procedure in part 2. |
| "The gentleman/gentlewoman from [state]" | How members refer to each other on the floor, often followed by "(Mr. Peters)". The matcher reads these. |
| Floor mention | One member naming another on the floor. `Martin/mentions.parquet` has 9,988; 8,469 between Republicans and Democrats with yields left out make the headline map. |
| Floor tie, floor map | Two members are tied when either named the other at least once: 3,970 ties. Undirected and unweighted. Whom members talk about in Washington. |

## 4. Press releases (part 3: the close-up and the home map)

| Term | Meaning |
|---|---|
| Press release | A short news text a member's office posts on their own `house.gov` site: "Lawler introduces bipartisan bill to...". |
| Listing, listing page | The page on a member's site that lists their press releases, newest first, over many pages. |
| Collector (A1) | Anas's script that follows each listing back to 3 January 2025 and stores each release's full text and date (`Anas/collector/`). It follows each site's `robots.txt`. |
| Press-release data | 55,023 releases from 412 members, 3 January 2025 to 20 November 2026 (the snapshot date), in three files split by member (`Anas/press_releases/`). Not collected: four members whose listing needs JavaScript or is gone, Jim Jordan (listing ends 2024), and the 12 who left office. |
| Template release | A text posted by five or more members (such as "Newest Members of Congress"): 64 releases, set aside. |
| Repeated sentence | A sentence a member repeats across releases (a bio or press-contact line): 84 in 41 members, not counted as that release's content. |
| Press mention | One member naming another in a release, found with the shared matcher plus the press layer. 129,473 (release, member) pairs; 14.4% cross-party. |
| Press layer | The few extra rules used on releases on top of Martin's matcher: untitled full names, members' own first names, party-state tags, lists across tags, quoted nicknames, middle initials, and a guard against state legislators. Every hit says which rule found it. |
| Party-state tag | `(R-NY)` after a name in a release. Must match the roster on both party and state, or senators slip in. |
| Release-to-bill link (A3.5) | A release is linked to a House bill by its number or by an official title that belongs to that bill alone: 18,177 links in 13,944 releases (25%); 30 of 30 right for each kind. |
| Caucus release, redistricting release | Releases from a group such as the Problem Solvers Caucus (members named by membership, not choice) and releases about the new maps. Flagged, and left out in two robustness rows. |
| The outcome of part 3 | The share of a member's releases that name at least one House member of the other party who is neither a party leader nor a co-lead of a bill the release cites. For the 406 members with at least 10 releases (53,664 releases). |
| Name, naming | What the paper says members do: "name the other party". We do not write "show" or "praise": tone is measured only in check T, where most names are partners. |
| Close-up | Part 3 of the paper: whom members name at home, by seat. Exposed Republicans 13.3% against 9.2% safe; exposed Democrats 11.6% against 9.0%. |
| Check T (what the names do) | 60 counted names, 15 per party and seat, coded by three blind AI readers: 46 partner or praise (77%), 9 neutral, 4 wrong match, 1 criticism. |
| Check I (ideology) | The exposed label shuffled only within party and ideology band: ideology alone gives 2.9 of the 4.1 Republican points and 2.4 of the 2.6 Democratic ones. Seat and ideology cannot be separated with our data. |
| Home map | The network of press mentions on the same 406 members: two members are tied when one names the other in a release (co-leads kept, leaders left out as the named member). 6,765 cross-party ties, 2,060 of them mutual. Accepted into the paper 25 Nov. |
| Hub (of the home map) | A member with many ties. Exposed members are 22% of members but send 35% and receive 34% of cross-party ties. |
| Bridging by volume, by position | Part 3's network twist. Exposed Republicans have more backbone ties than safe Republicans (by volume). Exposed Democrats have no more ties but sit on more shortest paths than their ties predict (by position). Borderline after Holm; we did not test why. |
| Mutual pair | Two members of different parties who each name the other (Golden and Fitzpatrick, Kaptur and Fitzpatrick, Golden and Lawler). Documented, not in the paper. |
| "Says bipartisan" (A5) | A release in which the word "bipartisan" appears outside the member's repeated sentences: 13,744 of 53,664 (25.6%). |
| "Has a partner" (A5) | The release names a House member of the other party (not a leader) or cites a bill with one as co-lead (**named** or **on record**; **either** is the main measure): 63.9% of "bipartisan" releases against 8.6% of others. |
| Mirror check (A5) | Do the named members in "bipartisan" releases work with the member, or are they opponents? 30 releases: 28 partners, 0 opponents. Its pair, the partner-less check: 29 of 30 really name no partner. |
| Common date window | One start and end date for every member: 3 January 2025 to 20 November 2026. Needed because 27 Republican and 5 Democratic sites stopped posting before September 2026. |
| Newsletter | An email a member sends to constituents. Not collected; press releases miss newsletters, ads and social media. *(planning only)* |
| Scope scan | Anas's 18 Nov count of releases per member (56,747; an overestimate, because some sites show two dates per release). Its counts sized the collection; the collector's counts replace them. *(planning only)* |
| Name pilot | 20 releases each from 16 members, used on 18 Nov to see whether anyone names the other party at all. Too small to report. *(planning only)* |
| Showing, showcase tie, mutual showing | Earlier words for naming a colleague at home. Replaced by "name" and "mutual pair". *(planning only)* |

## 5. Networks and null models

| Term | Meaning |
|---|---|
| Node | One member. The working and floor maps have the same 450 nodes; the home map has the 406 members of part 3. |
| Tie, edge, link | A connection between two nodes: signed a bill together, named on the floor, named at home. |
| Directed | The tie has a direction: A names B is not B names A. Mentions are directed; `named_ties.csv` has one row per (speaker, named) pair (5,400). The two maps of part 1 are made undirected. |
| Weighted | The tie has a strength. The two maps of part 1 are unweighted. The home map is weighted: each name in a release counts 1/n, with n the colleagues the release names, so a 40-name list adds 1/40 per name. |
| The two maps | The working map and the floor map on the same 450 members: the paper's headline. The home map is part 3's third network. |
| Cross-party share | The share of ties that join a Republican and a Democrat. Higher means less divided. Floor map 38.7%, working draws 28.6%. |
| Party modularity (Q) | One number for how much more ties stay inside a party than chance predicts: 0 means no more than chance. Floor 0.112, working draws 0.211. It depends on density, so maps are compared at the same number of ties. |
| Thinning, random working draws (G1a) | The floor map has 3,970 ties and the working map 46,513, so the floor map is compared with 200 random draws of 3,970 working ties: the headline comparison. |
| Strongest ties | The 3,970 working pairs that share the most bills. A second comparison: close allies are far more partisan (12.8% cross-party). |
| Null model | A shuffled version of a network, to ask "would we see this by chance?" If the real number lies outside all the shuffles, chance is an unlikely explanation. |
| Degree-preserving rewiring | A null that swaps the ends of ties while every member keeps their number of ties (double-edge swaps, Maslov–Sneppen). Both maps give about 50% cross-party and Q near 0 under it. |
| Debate null (M4) | Names shuffled only within one debate, so each debate keeps its cast. Q falls from 0.112 to 0.074: debate procedure explains about **two thirds** of the floor map's party division; the rest is beyond every shuffle. |
| State null (M3b, G16) | A rewiring that also keeps each member's number of ties within their own state. Q 0.001: state delegations explain almost none of the division. |
| Bipartite rewiring (home map) | Swaps that keep every tie cross-party and every member's number of cross-party ties. 10.7% of cross-party ties join two exposed members against 10.2% under it: a small preference. |
| Draws, shuffles, seed | One shuffled version is one draw. We use 200 (10,000 for label shuffles), with seed 2805 so anyone can repeat them. |
| Louvain communities | An algorithm that splits a network into groups with many ties inside and few between (resolution 1, 50 random starts, best kept). Working map: the two parties. Floor map: 8 groups across party that follow committees. Home map: 11 groups, among them a 35-member group of close-seat members (documented, not in the paper). |
| NMI (normalised mutual information) | A score from 0 to 1 for how well two groupings agree. Communities against party: working 0.83, floor 0.03, home 0.20. |
| Committee communities | In 7 of the floor map's 8 communities one committee is 3.0 to 7.9 times as common as in the House; 44% of floor ties join two members of one committee, against 17.1% under rewiring. |
| Backbone, disparity filter | Keeps only ties that are unusually strong for at least one of the two members (week 4; Serrano et al. 2009). Used on the home map at α = 0.01, the strictest level that keeps all 406 members connected: 1,656 of 29,210 ties. |
| α (alpha), α sweep | The disparity filter's strictness: smaller keeps fewer ties. The sweep checks every home-map result at α 0.005 to 0.2: all point the same way. |
| Degree, cross-party degree | How many ties a member has; how many of them cross the aisle. Exposed members' cross-party degree: R 54 against 28, D 46 against 30. |
| Betweenness | How often a member lies on the shortest paths between other members: a measure of brokering. |
| Closeness | How few steps a member is from everyone else. Varies little in a dense network. |
| Betweenness given degree | The betweenness left after allowing for the number of ties (residual of log betweenness on log degree): does a member broker more than their ties predict? |
| ForceAtlas2 | The layout used to draw the home map (week 4). Positions carry no measured meaning. |
| Ego network | One member plus everyone they are tied to. *(planning only)* |

## 6. Text, matching and labelling

| Term | Meaning |
|---|---|
| Mention | One place in a text where one member names another. `mentions.parquet`: `speaker`, `named`, `source`, `date`, `doc_id`, `context`, `is_yield`, plus `how` (the rule that found it). |
| Matcher (M1, `Martin/matcher.py`) | The shared code that finds member names in a text and turns them into Bioguide IDs. One matcher for floor and press, so the maps are comparable. |
| Title | "Rep.", "Mr.", "Congresswoman", "Chairman" and so on. The matcher reads a title before a surname. |
| Untitled full name | A name without a title: "my friend, Chip Roy". Matched on the floor too since G19, with a guard against "Senator", "Governor" and similar. |
| List rule | "Representatives Lawler, Golden, and Fitzpatrick": every name in the list is matched (G14). |
| Possessive, middle initial | "Mr. Cole's amendment" gives Cole; "Rep. James P. McGovern" gives McGovern, not John James (G18). |
| Shared surname | Members who share a surname are told apart by first name (official or nickname), then by a state name within 80 characters; otherwise the name is dropped (828 titled names). |
| Alias, nickname | Another name for the same person ("Hank" Johnson). Official nicknames come from `unitedstates/congress-legislators`; no alias list is complete, which is why recall is measured. |
| Leader title (`is_leader_title`) | Flags a mention made through a leadership title such as "Speaker Johnson". |
| Context | The sentence with the name plus one either side, at most 1,000 characters. What coders read. |
| Precision | Of the names the matcher found, the share that were the right member. Floor 98 of 100 (Diego's D2 sample); press 0.96. |
| Recall | Of the names really there, the share the matcher found. Floor 12 of 13 (30 turns read in full); press 0.97 (40 releases, five blind AI readers). |
| Recall check | Reading raw texts drawn without the matcher, listing every member named, and counting how many the matcher found. The only way to measure missed names, because a sample drawn from the matcher's output holds only names it found. |
| Labelling, coding | Reading a mention and giving it a code by hand. Part 2 of the paper (Diego). |
| The five codes (D2) | **P** procedure (yields, unanimous consent), **A** agreeing (thanks, praise, partnership, support for the member's bill), **D** disagreeing (rebuttal, criticism, blame), **N** neutral (a reference that takes no side), **X** not that member (wrong match, or Record text nobody said). Where two fit, the order X, P, D, A, N decides. Cross-party: 69% agreeing, 23% neutral, 7% disagreeing. |
| Coder, second coder | Diego coded all 100 mentions; Martin (rows 1-25), Claude (26-75) and Anas (76-100) were second coders. |
| Cohen's κ (kappa) | Agreement between two coders after removing what guessing would give. 0 is chance, 1 perfect. Human coders 0.64 (pairs 0.59 and 0.69), above the 0.6 set in advance; Diego and Claude 0.72. |
| Blind AI reader | A Claude run that codes or lists from a written packet only, without seeing the seat, the party or the other readers. Used in part 3's checks; same model family, so they show stability, not truth, and a human reads every disagreement. |
| TF-IDF | Turning text into numbers: words frequent in this text but rare across all texts get high weight (course week 6). |
| Classifier (D5) | A logistic-regression model on TF-IDF features, trained on the 100 hand labels to label all 9,909 floor mentions. 73% against 72% for always guessing "agreeing" (macro F1 0.26), so not used as a measurement. |
| Baseline (for a classifier) | The score without a model, here always guessing the most common code. |
| Leave-one-out | Testing a model on each labelled row in turn after training on the other 99. Used for D5 because 100 labels are too few for a held-out set. |
| Macro F1 | The F1 score averaged over the codes with equal weight, so a model that only guesses the common code scores low. |
| Regex | A text pattern for finding things like `H.R. 152` or `(R-NY)`. |
| Lexicon, dictionary method | Counting words from a fixed list (course week 7). A5 searches for one word, "bipartisan". |

## 7. Statistics and research design

| Term | Meaning |
|---|---|
| Observation vs result | An observation is one run, not yet checked. A result has been checked (a null, a second method or a hand sample). |
| Fixed in advance | A design, outcome or reading rule written down before the analysis was run (A4 plan 20 Nov, home-map plan, checks T and I, A5). The paper says "checks fixed before the analysis" only for these. |
| Within-party comparison | Compare exposed with safe seats inside one party, then compare that gap between the parties. Each party is its own baseline. |
| Interaction | The difference between the Republican gap and the Democratic gap: +1.5 points (p 0.36), too small to tell. |
| Seat effect vs president's-party effect | Seat effect: anyone in a close district names the other side more. President's-party effect: only the president's party does. Part 3's reading: a seat effect, which we cannot separate from ideology. |
| Confound | Something else that could produce the same pattern. Ideology is the one part 3 measured; majority status is one it did not. |
| Permutation test | Shuffle labels many times to see how often chance alone gives a result as large as the real one; p is the share of shuffles at least as extreme (two-sided). Part 3 shuffles the exposed label within party; M6 shuffles which bills are cross-party within each member. |
| Stratified shuffle | A permutation test whose shuffles stay inside groups (party and ideology band in check I). |
| Holm's correction | When ten comparisons are tested together, it keeps the chance of any false positive at 5% (`holm1979`). Used on the home map; outside the course. |
| Wilson interval | A 95% interval for a share from a small sample that stays sensible near 0% or 100% (60 of 60 gives 94% to 100%; `wilson1927`). Outside the course. |
| 95% interval | The range a number would likely fall in if the sample were drawn again. |
| Robustness row, check | The same test under another reasonable choice (cut-off 4 or 6, second lean source, without relabelled members, ...). Part 3 holds in every one. |
| Leave one state out | Rerunning the test with each state left out in turn; no single state carries part 3's gap. |
| Seed | A fixed starting number for random draws, so the same draws come out every time (2805). |
| Held-out rows | Rows a rule was not built on, used to test it fairly (the yield rule's 30 rows). |
| Difference-in-differences | The name for a within-party comparison done before and after an event. Ours has no time dimension, so it is an interaction. *(planning only)* |

## 8. How the group works

| Term | Meaning |
|---|---|
| G1a, G13, ... | Entries in `DECISIONS.md`. Each records a decision, its reason and the alternative. |
| M1-M8, A1-A6, D1-D5, S1-S3 | Tasks in `WORK_AND_DEADLINES.md`: M Martin, A Anas, D Diego, S shared. |
| Parts 1, 2, 3 | Results: the two maps (Martin), what a mention means (Diego), the close-up at home (Anas). |
| Freeze (G7, G17) | Numbers frozen since Sun 22 Nov; scope frozen since Sat 21 Nov. On 25 Nov the analysis was closed: no new analyses, only writing. |
| Stop rule (G5) | If no press data for the first 20 members by Fri 20 Nov, the close-up would be dropped. Passed on 20 Nov. *(planning only)* |
| Shared files | `mentions.parquet`, `named_ties.csv`, the press-release files. Their columns are fixed. |
| Own folder | `Anas/`, `Martin/`, `Diego/`. Each person writes only in their own; project-level files (this one, `DECISIONS.md`, `WORK_AND_DEADLINES.md`, `OFF_CURRICULUM.md`, `report/`) are shared. |
| robots.txt | A file on each website saying what automated tools may fetch. On the member sites it allows press-release pages; the collector follows it. |
| `AI_METHODS.md` | The required file on where a model touched a result and how it was checked. Diego keeps it (`Diego/AI_METHODS.md`); copied to `docs/AI_METHODS.md` before hand-in. |
| `OFF_CURRICULUM.md` | Every method we use that the course does not teach, with its reference and why it fits. |
