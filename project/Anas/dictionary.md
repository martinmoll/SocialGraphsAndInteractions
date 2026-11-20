# Dictionary: the words we use in "Two maps of Congress"

Anas, 19 November 2026. Terms come from `README.md`, `WORK_AND_DEADLINES.md`, `DECISIONS.md`, `Martin/README.md`,
`Martin/M3_PROPOSAL.md`, `Diego/d2_labelling/PROTOCOL.md`, `Diego/report_skeleton.md` and `Anas/press_scope/`.
Numbers are the ones in those files on 18 November. If a definition here disagrees with a decision in
`DECISIONS.md`, the decision wins; tell Anas so this file can be fixed.

Each entry gives the plain meaning first, then how we use it in the project.

Sections:

1. Congress and elections
2. Bills and cosponsorship (the working map)
3. Floor speeches (the floor map)
4. Press releases (the home map and the close-up)
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
| Senate, senator | The smaller chamber: 100 senators, two per state. Senators are not in our network. They can still slip into our data because they are named in House texts, sometimes with the same surname as a House member (Collins). |
| Member, representative, congressman/congresswoman | One person elected to the House. In our files every member is a node. |
| Seat | One place in the House, won by one person in one district. It is not a mayor or a governor. The House has 435 voting seats, one per district, plus 6 non-voting delegates (see below). "Exposed seat" and "safe seat" describe the district, not the person. |
| District (congressional district) | The area of a state that elects one House member. States are cut into districts by population, so California has 52 and Alaska has 1. Our `districts.csv` has 435 rows, one per voting seat. |
| At-large district | A state with only one district. It is stored as district `0` (Alaska, for example). |
| Delegate | A non-voting House member for DC, Puerto Rico, Guam, the US Virgin Islands, American Samoa or the Northern Mariana Islands. All six are in `members.csv`, with `current = False`. They speak, sponsor and cosponsor, but have no district lean. |
| Why 450 or 451 members, not 435 | `members.csv` has 451 people: 433 current members, one in each voting seat (2 seats, FL-20 and TX-23, were vacant when the file was made), plus 18 marked not current: the 6 delegates and 12 members who left during the term (resigned, died, or took another office). We usually say "450 members". |
| State delegation | All the House members from one state. Delegations range from 1 seat (6 states) to 52 (California). The four largest (CA, TX, FL, NY) hold a third of all seats. See `state_seats/`. |
| Party | R (Republican), D (Democrat), I (independent). `members.csv`: 226 R, 224 D, 1 I. The one independent stays in the files; filter on party when you need two sides. |
| Majority, minority | The party with more seats controls the House: it elects the Speaker, chairs every committee and decides which bills reach the floor. In the 119th Congress the Republicans are the majority. |
| Speaker | The leader of the House, elected by the majority. Currently Mike Johnson (R). Named very often, mostly for procedural reasons. |
| Party leaders | Speaker, majority and minority leaders, whips. Their names are everywhere for reasons that have nothing to do with partnership, so the name pilot left them out. |
| Committee, chairman, ranking member | Bills are worked on in committees. The chairman is from the majority; the ranking member is the most senior minority member. "Thank Chairman Cole and Ranking Member DeLauro" is a routine courtesy. |
| Midterm election | The House election halfway through a president's four-year term. The 2026 midterm was on 3 November 2026. Historically the president's party tends to lose seats in midterms. |
| President's party | The party of the sitting president: the Republicans (Trump) in 2025-26. Part of our question is whether naming the other party is about being in the president's party or about having an exposed seat. |
| Incumbent | The person who currently holds the seat. `incumbents.csv` records who held each seat and what happened to them in 2026. |
| Redistricting, redraw, redrawn state | Redrawing the borders of a state's districts. It normally happens once a decade, after the census. Nine states (AL, CA, FL, LA, NC, OH, TN, TX, UT) drew new maps in the middle of the decade, for the 2026 election, so a member's 2026 district can be a different area from the one they served in 2025-26, even with the same number. Wikipedia's list of which states redrew is what `districts.csv` stores as `redrawn_state`. |
| Served district, new district | The served district is the one a member represented in 2025-26 (the number in `members.csv`). The new district is the 2026 district with that number. They are the same area except in redrawn states. |
| Voteview, DW-NOMINATE | Voteview is a public database of how every member voted. DW-NOMINATE turns those votes into a left-right score (`nominate_dim1` in `members.csv`: negative is liberal, positive is conservative). |
| Roll call | A recorded vote where each member's yes or no is written down. |
| Bioguide ID | The official ID of every member of Congress, such as `B001323` (Begich). Every table we have is joined on it. |

### District lean and exposed seats

| Term | Meaning |
|---|---|
| District lean | How Republican or Democratic a district votes, compared with the country as a whole. In our files it is the 2025 Cook PVI, as a signed number: positive leans Republican, negative leans Democratic. Alaska's `6` means R+6. There are two columns: `lean_2026` (the 2026 map, from the 2026 House election page on Wikipedia, in `districts.csv` as `lean`) and `lean_2025` (the map members served, from `Anas/district_lean/`). They differ only in redrawn states. |
| Cook PVI (Partisan Voting Index) | A widely used measure of lean published by the Cook Political Report. It compares how a district voted for president in the last two elections with the national result. R+6 means the district voted about 6 points more Republican than the country. EVEN means it voted like the country. |
| Safe seat | A seat the member's party is very likely to keep, because the district leans strongly their way. |
| Exposed seat, swing seat | A seat the member could lose, because the district is close or leans to the other party. **The group has not fixed a definition yet (G13, open point 2).** The scope scan used a working rule only to size the samples: a Republican in a district with lean ≤ 5 (R+5 or bluer), or a Democrat with lean ≥ −5 (D+5 or redder). |
| Crossover district, "Trump district" | A district that leans to the other party: a Democrat holding an R-leaning seat, or a Republican holding a D-leaning seat. The most exposed seats. |
| Lean in redrawn states | In a redrawn state `lean_2026` describes a district the member did not serve in. Cohen's TN-9 is D+23 as he served it and R+9 on the 2026 map. 12 members get a different exposed/safe label in the district they served and the 2026 district they ran in, and 9 more have no 2026 contest in our data. Proposed: label by `lean_2025`, the district served, and check the result without those 21. Use `Anas/district_lean/member_lean.csv`, never `districts.csv` joined by district number. |

## 2. Bills and cosponsorship (the working map)

| Term | Meaning |
|---|---|
| Bill | A proposed law. Ours come from `bills.parquet`: 12,987 House bills and resolutions of the 119th Congress, with type, number, sponsor, date, policy area and title. |
| Bill types | `hr` = H.R., a bill. `hres` = H.Res., a resolution of the House only. `hjres` = H.J.Res. and `hconres` = H.Con.Res., joint and concurrent resolutions. A bill number is type plus number, such as H.R. 152. Press releases cite these numbers, which is how we match a release to its bill (A3). |
| Sponsor | The one member who introduces a bill. |
| Cosponsor | A member who signs on to support someone else's bill. `cosponsors.parquet` has 149,015 cosponsorships. |
| Original cosponsor | A cosponsor who signed on the day the bill was introduced (column `original`). They usually helped write it. |
| Withdrawn | A cosponsor who took their name back off the bill (column `withdrawn`). |
| Co-lead | Our word for the members who lead a bill together, often one from each party ("a bipartisan bill I am leading with my good friend..."). In A3 a named colleague is marked co-lead if they are the sponsor or an original cosponsor of the bill the release announces. **Exact rule still to be written in A3.** |
| Policy area | The subject Congress staff give each bill (Emergency Management, Health, and so on). |
| govinfo, BILLSTATUS | The US government's publishing site and its bulk data of every bill's status. Our bill and cosponsor tables come from it. |
| Working tie | A link between two members who appear on the same bill (one sponsors, the other cosponsors). "Signed at least one bill together." |
| Working map | The network of all working ties: who works with whom on legislation. 46,513 ties before thinning. |

## 3. Floor speeches (the floor map)

| Term | Meaning |
|---|---|
| The floor | The chamber where the whole House debates and votes. "Floor speech" means something said there, in public. |
| Congressional Record | The official daily transcript of everything said on the House and Senate floors. Our speeches come from it (via govinfo). |
| Speaker turn | One uninterrupted stretch of speech by one member. `speeches.parquet` has 35,629 turns. We keep House turns of 50 words or more. |
| Debate, Record item, `doc_id` | One item in the Record, usually the debate on one bill. The debate null (M4) shuffles names only inside one `doc_id`. |
| Floor manager | The member from each party who runs the debate on a bill and hands out speaking time. Every debate has one from each side, which is why the floor map has a built-in cross-party element. |
| Yield | Handing speaking time to another member: "I yield 2 minutes to the gentleman from Texas." A yield is procedure, not talking about someone. Yields are dropped from the headline floor map (G1b). |
| "Will the gentleman yield?" | Asking the named member to give up time. Not a yield (G12): it is addressing that member, usually mid-argument, so it stays in the map. |
| Yield rule (phrase rule, window rule) | How code spots yields. Phrase rule (used now): "yield" before the name, not "yield back"/"yield myself", or "for yielding" after the name, in one sentence. Window rule (old, kept as `is_yield_window`): "yield" within 60 characters of the name. |
| Unanimous consent | A request to do something without a vote, passed if nobody objects. Often names members. Coded P (procedural). |
| "The gentleman/gentlewoman from [state]" | How members refer to each other on the floor, often followed by the name in brackets: "(Mr. Peters)". The matcher reads these. |
| Floor mention | One member naming another on the floor. `Martin/mentions.parquet` has 8,092. |
| Floor tie, floor map | A link from a speaker to a member they named at least once; the network of all of them. "Whom members talk about in Washington." |

## 4. Press releases (the home map and the close-up)

| Term | Meaning |
|---|---|
| Press release | A short news text a member's office posts on their own website (`name.house.gov`) and sends to journalists: "Lawler introduces bipartisan bill to...". |
| Newsletter | An email a member sends to constituents. **Not collected and not part of our design.** The README says press releases miss newsletters, ads and social media. |
| Listing, listing page | The page on a member's site that lists their press releases, newest first, spread over many pages. |
| Pager, layout | How a site numbers its listing pages. We found four: Drupal `?page=N`, ASP `documentquery.aspx?...&Page=N`, WordPress `/page/N/`, and `PageNum_rs=N`. |
| WordPress API | 36 member sites answer `/wp-json/wp/v2/posts`, which hands over full text and exact counts without scraping the page. |
| Scope scan | Anas's 18 Nov count of how many releases each member has posted since 3 Jan 2025: 407 of 450 members, 56,747 releases. Counts only, no text. |
| Collector (A1) | The script that will download the full text and date of each release into `press_releases.parquet` (`bioguide, url, date, title, text`). |
| Name pilot | 20 recent releases each from 16 members, used to see whether anyone names the other party at all. Too small to report. |
| Press mention | One member naming another in a press release. Found with Martin's shared matcher, like floor mentions (`source = press`). |
| Home map | The network of press mentions: whom members choose to show voters back home. Our third map, on the same nodes as the other two. |
| Showing, being shown | Naming someone in your own release. We can say who is **shown**. With about 40 releases per member we cannot say who is **hidden**. |
| Showcase tie | A cross-party colleague a member shows at home. Figure 3 is about these. |
| Mutual showing (option E) | Two members of different parties who each show the other: Golden and Lawler, Golden and Fitzpatrick, Kaptur and Fitzpatrick in the pilot. Checkable only because both parties are now collected (G13). |
| Release-to-bill table (A3) | Matching each release to the bill it announces by bill number, so we know whether a named colleague is just the co-lead on that bill. |
| Close-up | Part 3 of the paper: named pairs and examples from press releases. About half a page with Figure 3. |
| Stopped posting | 27 Republican and 5 Democratic sites have no releases after some date before September 2026. Why is not checked. It is why both parties need one common date window. |
| Common date window | One start and end date used for every member, so a member who stopped posting is not compared with one who kept going. Proposed: 3 Jan 2025 to a cutoff before the summer drop-off. Not yet decided. |
| "Bipartisan" (A5, optional) | Whether a release that calls itself bipartisan actually names a partner from the other party. Extends Westwood's study of the word. |

## 5. Networks and null models

| Term | Meaning |
|---|---|
| Node | One member. All three maps have the same nodes. |
| Tie, edge, link | A connection between two nodes. Which kind depends on the map: signed a bill together, named on the floor, named at home. |
| Directed | The tie has a direction: A names B is not B names A. Floor and home ties are directed; `named_ties.csv` has one row per (speaker, named). |
| Weighted | The tie has a strength, such as the number of shared bills. Working ties are weighted; floor ties are not. |
| The two maps | The working map (cosponsorship) and the floor map (mentions) on the same 450 members. The home map is the press-release close-up. |
| Cross-party share | The share of ties that connect a Republican and a Democrat. Higher means less divided. The main number of part 1. |
| Party modularity (Q) | One number for how much more ties stay inside a party than chance would predict. 0 means no more than chance; higher means more divided. It depends on how dense the network is, so maps are compared at the same number of ties. |
| Thinning | Cutting the working map down to the floor map's size so the two can be compared fairly. |
| Random working ties (headline, G1a) | Keep a random sample of working ties of the floor map's size, 200 times, and report the range. Changes the size and nothing else. |
| Strongest ties | Keep only pairs with 6 or more shared bills. A second comparison: close allies are more partisan (12.6% cross-party). |
| Backbone (disparity filter, α = 0.05) | Keep only ties that are unusually strong for at least one of the two members. One robustness row in the table. |
| Null model | A fake version of the network made by shuffling, used to ask "would we see this by chance?" If the real number lies outside all the fake ones, chance is an unlikely explanation. |
| Degree-preserving rewiring | A null that shuffles the ends of ties while every member keeps the same number of ties. |
| Debate null (M4) | A harder null: names are shuffled only within one debate. It keeps the fact that each debate has a manager from each party. It explains about half of the floor map's party division. |
| Rewirings, draws | One shuffled version is one rewiring or draw. We use 200, with a fixed seed (2805) so anyone can repeat them. |
| Louvain communities (M5) | An algorithm that splits a network into groups with many ties inside and few between. We check whether the groups match the parties. |
| NMI (normalized mutual information) | A score from 0 to 1 for how well two groupings agree: communities against party, or the two maps' communities against each other. |
| Ego network | One member plus everyone they are tied to. |

## 6. Text, matching and labelling

| Term | Meaning |
|---|---|
| Mention | One place in a text where one member names another. The shared file is `mentions.parquet`: `speaker`, `named`, `source`, `date`, `doc_id`, `context`, `is_yield`. |
| Matcher (M1, `Martin/matcher.py`) | The shared code that finds member names in a text and turns them into Bioguide IDs. The same one is used for floor and press, so the maps are comparable. |
| Title | "Rep.", "Mr.", "Congresswoman", "Chairman" and so on. The matcher looks for a title before a surname. |
| Shared surname | 56 of 450 members share a surname with another member. The matcher tries the first name, then the state within 80 characters, and otherwise drops the mention (783 drops). |
| Untitled full name | A name without a title: "Mike Lawler said". Not matched yet. Common in press releases. |
| List rule | "Reps. Golden, Lawler and Fitzpatrick": today only the first name after a plural title is matched. In `MATCHER_CHECKLIST.md`, waiting on Martin. |
| Leader title (`is_leader_title`) | Flags a mention made through a leadership title such as "Speaker Johnson". |
| Context | The sentence with the name plus one either side, at most 1,000 characters. What coders read. |
| Labelling, coding | Reading a mention and giving it a code by hand. Part 2 of the paper. |
| Codes P, A, D, N, X | P procedural (yields, unanimous consent), A agreeing (thanks, praise, partner), D disagreeing (rebuts, blames, opposes), N neutral (just reports), X not a mention (wrong person, a constituent, a heading). |
| Coder, second coder | The person who labels. Every mention in the 100-row sample has two coders: Diego plus Martin (rows 1-25), Claude (26-75) or Anas (76-100). |
| Cohen's κ (kappa) | Agreement between two coders after removing the agreement you would get by guessing. 0 is chance, 1 is perfect. Ours: pooled 0.64; Diego-Anas 0.69. We set 0.6 as the bar in advance. |
| Precision | Of the names the matcher found, the share that were the right member. 98 of 100 in Diego's sample (G10). |
| Recall | Of the names that were really there, the share the matcher (or a rule) found. |
| TF-IDF | A way to turn text into numbers: words that are frequent in this text but rare across all texts get high weight. Course week 6. |
| Classifier (D5) | A model trained on the 100 hand labels to label all floor mentions automatically. Scored 73% against 72% for always guessing "agreeing", so not used as a measurement. |
| Baseline (for a classifier) | The score you get without a model, here by always guessing the most common code. |
| Regex | A text pattern for finding things like `H.R. 152` or `(R-NY)`. |
| Party-state tag | `(R-NY)` after a name in a press release. Must match the roster on both party and state, or senators slip in. |
| Recall check | Hand-reading a random sample of raw texts (releases or floor turns), listing every House member named in any form, and counting how many the matcher found. The only way to measure missed names, because a sample drawn from the matcher's output contains only names it found. Planned for 30 releases and 30 floor turns. |
| Alias, nickname | Another name for the same person ("Hank" Johnson for Henry Johnson, "Chuy" García for Jesús García). Week 7. Official nicknames are in `unitedstates/congress-legislators`; no alias list is complete, which is why recall is measured. |
| Caucus release | A release from a group of members such as the Problem Solvers Caucus, which is bipartisan by design and lists many members of both parties. Naming because of membership, not a choice to show someone, so these are flagged. |
| Lexicon, dictionary method | Counting words from a fixed list (course week 7, sentiment). Not in our design; possible for A5 with a short list of partnership words. |

## 7. Statistics and research design

| Term | Meaning |
|---|---|
| Observation vs result | An observation is one run, not yet checked. A result has been checked (a null, a second method or a hand sample). Our files say which. |
| Within-party comparison | Compare exposed with safe seats inside one party, then compare that gap between the parties. Each party is its own baseline, so differences in how much each party publishes or names people cancel out. |
| Difference-in-differences | The name for the comparison above when it is done before and after an event. Ours has no time dimension, so it is better called an interaction between party and exposure. |
| Seat effect vs party effect | Seat effect: anyone in a close district names the other side more. Party effect: only the president's party does. The Democrats are collected to tell these apart (G13). |
| Confound | Something else that could produce the same pattern. Majority status is one: Republicans lead most bipartisan bills that pass, so they have more cross-party news to announce. |
| Permutation test | A test that shuffles labels many times to see how often chance alone gives a result as large as the real one. In part 3: shuffle the exposed/safe labels within each party and recompute the party × exposure gap. The same logic as the course's shuffle nulls. |
| Second lean measure | `pres_margin_2024`: Trump's 2024 margin on the districts members served (The Downballot). It agrees with the Cook lean (r = 0.999), which confirms the Wikipedia numbers; labels differ only for 10 members at the ±5 cut-off. |
| Seed | A fixed starting number for random draws, so the same draws come out every time. |
| Held-out rows | Rows a rule was not built on, used to test it fairly. |
| 95% interval | The range a number would likely fall in if the sample were drawn again. Matcher precision 93% (86 to 97%) in D1. |

## 8. How the group works

| Term | Meaning |
|---|---|
| G1a, G4, G13, ... | Entries in `DECISIONS.md`. Each records a decision, its reason and the alternative. |
| M1-M8, A1-A6, D1-D5, S1-S3 | Tasks in `WORK_AND_DEADLINES.md`: M Martin, A Anas, D Diego, S everyone. |
| Stop rule (G5) | No press data for the first 20 members by Fri 20 Nov, and the close-up is dropped. |
| Freeze (G7) | No definition changes after Sun 22 Nov. |
| Shared files | `mentions.parquet`, `named_ties.csv`, `press_releases.parquet`. Their columns are fixed; nobody changes one without saying so in the chat. |
| Own folder | `Anas/`, `Martin/`, `Diego/`. Each person writes only in their own. |
| robots.txt | A file on each website saying what automated tools may fetch. On the member sites checked it allows press-release pages and blocks only print views, forms, previews and search. The collector follows it. |
| `docs/AI_METHODS.md` | The required file on how AI was used in the project. Anas writes it (A6). Not created yet. |
