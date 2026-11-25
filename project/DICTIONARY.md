# Dictionary: the words we use in "Two maps of Congress"

Look a word up in the A to Z index at the bottom, or read a topic section from the top. Each entry says what the
word means in plain English and then how we use it in the project. These are the definitions we agreed on (25 Nov
2026). The paper, the slides and our answers at the presentation use the words this way. If something here
disagrees with `DECISIONS.md` or the paper, they win, and this file should be fixed.

Numbers are the final ones, frozen on 22 Nov. A few words we only used while planning are kept at the end of their
section and marked "(planning only)", so older files still make sense. Anas started the list on 19 Nov; it covers
all three parts.

## What the "Kind" column tells you

| Kind | Meaning | Can you trust the everyday meaning? |
|---|---|---|
| General | Ordinary English or a common web word | Yes |
| Politics | A term from US politics or political science, used the way people in that field use it | Yes, in a political sense |
| Course | Something taught in 02805, used the way the course pages use it | Yes, as the course defines it |
| Statistics | A standard statistics term. The ones the course does not teach are explained in [`OFF_CURRICULUM.md`](OFF_CURRICULUM.md) | Yes, as a textbook defines it |
| Data | The name of a data source, a file or a column | Only as the file defines it |
| Ours | A word we made up, or an ordinary word we use in a narrower way | No. Use the definition here |

## Topics

0. Words that mean something narrower here than usual
1. Congress and elections
2. Bills and cosponsorship (the working map)
3. Floor speeches (the floor map)
4. Press releases (part 3: the close-up and the home map)
5. Networks and null models
6. Finding names in text, and labelling them
7. Statistics and research design
8. How the group works

Then: A to Z index.

## 0. Words that mean something narrower here than usual

These are the words most likely to be misread, by an examiner or by us. Each one has an everyday or political
meaning that is wider than ours. If unsure, say the narrow version out loud, for example "moderate within their
own party, judged by their votes".

### About seats and members

| Word | Usual meaning | What it means in our paper | Avoid saying |
|---|---|---|---|
| Moderate | A centrist; someone who likes to compromise, often judged from speeches or stated positions | A member whose votes in the House (DW-NOMINATE) put them in the least extreme fifth of their own party. It is relative: a moderate Republican still votes to the right of almost every Democrat. It says nothing about personality, tone or willingness to compromise | "Moderates are more willing to work with the other side" (we never measured willingness) |
| Extreme | Radical, outside the mainstream | In the most extreme fifth of their own party, judged by votes. A ranking, not a judgement of the person | "Extremists" |
| Ideology | What a person believes | Where a member's votes place them on the left to right scale of DW-NOMINATE | "What members believe" |
| Exposed (seat) | Vulnerable. In politics it can also mean being on a party's list of members at risk, or in a race that forecasters call close | Our own fixed rule about the district the member served: it leans toward the member's own party by 5 points or less (Cook PVI 2025). Seats that lean to the other party count too. It is not the member's own winning margin, a forecaster's rating or a party's list | "Vulnerable members" or "frontline members", as if it were an official list |
| Safe (seat) | A seat forecasters rate "Solid", one nobody expects to change party | Any seat that is not exposed under our rule: the district leans toward the member's own party by more than 5 points | "Uncompetitive" as a claim about the 2026 race |
| Swing seat (also competitive, battleground) | A seat that forecasters think could change party at the next election | Our planning files use it to mean "exposed". The paper only says "exposed" | Using "swing" and "exposed" side by side in one text |
| Lean | In election forecasting, "Lean R" is a race rating (the scale runs Solid, Likely, Lean, Toss-up) | The Cook PVI number of a district: how it voted for president compared with the whole country. Never a race rating | "The district is rated Lean R" |
| Crossover | A voter or member who crosses party lines | A district that leans to the other party from the member's (for example a Democrat holding a seat that leans Republican) | "Crossover members vote with the other party" |
| Leader | Anyone in a leading role, committee chairs included | Only the seven members on the House leadership list: the Speaker, the majority leader and whip, the Republican conference chair, and the Democratic leader, whip and caucus chair. Committee chairs are not leaders here | "Leaders" when you mean chairs |
| President's party, majority | Two different things in general | In this House (the 119th), the Republicans are both. So our data cannot tell a president's-party effect apart from a majority effect | Claiming one of the two specifically |

### About what members do

| Word | Usual meaning | What it means in our paper | Avoid saying |
|---|---|---|---|
| Name, naming | To mention someone | A House member that our matching code found in a text (a floor speech or a press release), counted once per text | "Praise", "show", "promote", "endorse". Tone was only measured in part 2 and check T |
| Mention | Any reference to someone | One hit of the matching code: one member found in one floor turn or one release | "Talk about", as if we read every mention |
| Partner | A friend or ally | Someone credited for working together: a co-lead of a bill, or a member thanked or praised for joint work. In check T this is the code P; in A5 a partner is either named in the release or on record through a cited bill | "Friend" or "ally" |
| Co-lead | Anyone who leads something together with others | The sponsor of a bill, or an original cosponsor who did not withdraw, for a bill the text cites | |
| Agreeing, disagreeing | Holding the same or the opposite opinion | Part 2's codes for what the speaker does towards the named member in that sentence: thanks, praise and support, or rebuttal and blame. It is about the person named, not the bill, the party or the President | "Members agree with the other party" |
| Credit, acknowledgement | Recognition | Our short way of describing mentions coded "agreeing": thanks and credit for specific bills and committee work | "Cooperation" |
| Bipartisan | Involving both parties; also a label members put on their own work | Only the word itself, written in a release (A5: "says bipartisan"). When we measure that a tie or a bill joins both parties, we call it cross-party | "Bipartisan tie" for a tie we measured |
| Cross-party, across the aisle | Involving both parties | A tie, mention or bill that joins a Republican and a Democrat. The one independent member (Kiley) is left out | |
| Procedure | Rules and formalities | Part 2's code P: handing over debate time, thanking someone for it, or asking for unanimous consent. Yields are left out of the headline floor map | |

### About the maps and the network

| Word | Usual meaning | What it means in our paper | Avoid saying |
|---|---|---|---|
| Divided, division (by party) | Political conflict or disagreement | How strongly a network splits into a Republican side and a Democratic side. We measure it with the share of ties that cross the aisle and with party modularity Q | "Members disagree more" |
| Polarization | In political science, usually how far apart the two parties vote (or, as "affective polarization", how much party supporters dislike each other) | We use the word only loosely, in the framing ("measured polarization depends on the record"). What we actually measure is how divided a network is | Treating our numbers as roll-call polarization |
| Working (map) | A working relationship | Cosponsorship only | "Members who work together" as a fact beyond signing bills |
| Floor (map) | The floor of a room | Speeches on the House floor, as printed in the Congressional Record | |
| Home, at home | In political science, how members present themselves to the people they represent | In press releases on the members' own websites. National media read these too | "In their districts", as if we saw local events |
| Debate | An argument | One item of the Congressional Record, usually the discussion of one bill (`doc_id`) | |
| Community | A neighbourhood or a group of people | A group the Louvain method finds: members with many ties inside the group and few to the outside | "Caucus" or "coalition" |
| Hub | A busy centre | A member with many ties. As a group, exposed members hold a large share of the home map's cross-party ties | "Influential", "powerful" |
| Bridge, broker | A go-between, or a deal-maker | A member who sits between groups in the network. "By volume" means having many cross-party ties on the backbone. "By position" means lying on more shortest paths than one would expect from the number of ties | "Deal-makers" |
| Backbone | The most important part | The ties that the disparity filter keeps (α = 0.01) | "The important members" |

### About results and checks

| Word | Usual meaning | What it means in our paper | Avoid saying |
|---|---|---|---|
| Seat effect | The seat causes something | A pattern by type of seat that holds in both parties. We do not claim it is a cause, and we cannot separate it from ideology | "Exposure makes members name the other party" |
| Significant | Important | p < 0.05 under the shuffle we name (and after Holm's correction where we say so) | "A significant effect" meaning a large one |
| Borderline | Almost | Below 0.05 before Holm's correction but above it after, or the other way round at another α | "Shows" |
| Check | A quick look | A planned test of a measurement or a result. Where we say "fixed in advance", the rule for reading it was written down first | |
| Blind (reader) | Unable to see | The reader did not see the seat, the party label (where it was hidden) or the other readers' answers | "Double-blind" |
| Fixed in advance | Rigged | Written down before the analysis was run: the A4 plan, the home-map plan, checks T and I, and A5 | Using it for choices made after seeing results |
| Holds | Stays true | Keeps the same direction and stays below p 0.05 in the check | "Proves" |

## 1. Congress and elections

| Term | Kind | What it means |
|---|---|---|
| Congress | Politics | The US parliament. It has two chambers, the House of Representatives and the Senate. We only study the House. |
| 119th Congress | Politics | The two-year term of Congress that began on 3 January 2025 and runs to January 2027. All our data come from it. |
| House of Representatives (the House) | Politics | The larger chamber. Every member is elected for two years by one district. |
| Senate, senator | Politics | The smaller chamber, with 100 senators, two per state. Senators are not in our networks, but House texts name them, sometimes with the same surname as a House member (Collins). The matching code skips names that come after "Senator". |
| Member, representative, congressman, congresswoman | Politics | A person elected to the House. In our files every member is a node. |
| Seat | Politics | One place in the House, held by one person for one district. The House has 435 voting seats, one per district, plus 6 delegates who cannot vote. "Exposed" and "safe" describe the district, not the person. |
| District (congressional district) | Politics | The part of a state that elects one House member. States are divided by population, so California has 52 districts and Alaska has 1. `districts.csv` has 435 rows, one per voting seat. |
| At-large district | Politics | A state that has only one district. We store it as district `0` (Alaska, for example). |
| Delegate | Politics | A House member who cannot vote, representing DC, Puerto Rico, Guam, the US Virgin Islands, American Samoa or the Northern Mariana Islands. All six are in `members.csv` with `current = False`. They have no district lean. |
| Why "450 members" | Data | `members.csv` lists 451 people. 433 are current members (two seats, FL-20 and TX-23, were empty) and 18 are not current: the 6 delegates and 12 members who left during the term. 226 are Republicans, 224 Democrats and 1 independent (Kiley). The two maps use the 450 Republicans and Democrats; Kiley stays in the files. |
| State delegation | Politics | All the House members from one state. A delegation can be 1 seat (6 states) or as many as 52 (California). The four biggest states (California, Texas, Florida, New York) hold a third of all seats. |
| Party | Politics | R for Republican, D for Democrat, I for independent. |
| Majority, minority | Politics | The party with more seats runs the House: it picks the Speaker, chairs every committee and decides which bills reach the floor. In the 119th Congress the Republicans are the majority. Part 3 mentions this as one possible reason why exposed Republicans and Democrats connect across the aisle in different ways, but we did not test it. |
| Speaker | Politics | The leader of the House, chosen by the majority: Mike Johnson (R). He is named very often, mostly for procedural reasons. |
| Party leaders | Ours | The seven members on the House leadership list (`Anas/a3/leaders.csv`): the Speaker, the majority leader and whip, the Republican conference chair, and the Democratic leader, whip and caucus chair. Their names turn up everywhere for reasons unrelated to partnership, so part 3 does not count them when they are the one named. On the floor map, they make up the eighth community. |
| Committee, chairman, ranking member | Politics | Committees do the detailed work on bills. The chairman comes from the majority; the ranking member is the most senior member from the minority. "Thank Chairman Cole and Ranking Member DeLauro" is ordinary politeness. The floor map's communities follow committees (part 1). |
| Midterm election | Politics | The House election held halfway through a president's term. The 2026 midterm was on 3 November 2026. It is the background of the project; we do not try to explain who won. |
| President's party | Politics | The party of the sitting president: the Republicans (Trump) in 2025 and 2026. Part 3 asks whether naming the other party goes with being in the president's party or with having an exposed seat. |
| Incumbent | Politics | The person who holds a seat right now. `incumbents.csv` records who held each seat and what happened to them in 2026. |
| Redistricting, redraw, redrawn state | Politics | Drawing new borders for a state's districts, which normally happens once every ten years. Nine states (Alabama, California, Florida, Louisiana, North Carolina, Ohio, Tennessee, Texas, Utah; 173 seats) drew new maps for the 2026 election. In those states a member's 2026 district can cover a different area from the one they served, even with the same number. |
| Served district, 2026 district | Ours | The served district is the one a member represented in 2025 and 2026. The 2026 district is the one they ran in. They cover the same area except in the redrawn states. Part 3 uses the served district, because the press releases were written for its voters. |
| Voteview | Data | A public database of every vote in Congress, and our source for the list of members. See DW-NOMINATE below. |
| Roll call | Politics | A recorded vote, where each member's yes or no is written down. |
| Bioguide ID | Data | The official ID of every member of Congress, such as `B001323` (Begich). All our tables are joined on it. |

### District lean and exposed seats

| Term | Kind | What it means |
|---|---|---|
| District lean | Politics | How much more Republican or Democratic a district votes than the country as a whole. We use the 2025 Cook PVI as a number with a sign: positive leans Republican, negative leans Democratic (Alaska's `6` means R+6). `lean_2025` is the lean of the district the member served (`Anas/district_lean/member_lean.csv`, taken from the Wikipedia page as it was on 25 May 2025, before any new maps). `lean_2026` (`districts.csv`, column `lean`) is the new 2026 map. Never join `districts.csv` to members by district number. |
| Cook PVI (Partisan Voting Index) | Politics | The lean measure published by the Cook Political Report. It compares how a district voted for president in the last two elections with how the whole country voted. R+6 means about 6 points more Republican than the country; EVEN means the same as the country. Cited as `cook2025pvi`. |
| Second lean measure | Ours | `pres_margin_2024`: Trump's 2024 winning or losing margin in each district members served (from The Downballot, `downballot2024`). It agrees with the Cook lean almost perfectly (r = 0.999). Part 3 uses it as a robustness check. |
| Exposed seat (the rule in the paper, G13) | Ours | The district the member served leans toward the member's own party by 5 points or less. Seats that lean to the other party count too. For a Republican that means a lean of R+5 or less; for a Democrat, D+5 or less. 91 of the 406 members in part 3 are exposed (37 Republicans, 54 Democrats). All three of us agreed on this rule (`DECISIONS.md` G13). |
| Safe seat | Ours | Any seat that is not exposed: the district leans toward the member's own party by more than 5 points. |
| Crossover seat | Politics | A district that leans to the other party: a Democrat holding a seat that leans Republican, or the reverse. In part 3 there are 18 (8 Republicans, 10 Democrats). These are the most exposed seats, and they show the biggest naming gap. |
| Relabelled members | Ours | 12 members who get a different exposed or safe label depending on whether we use the district they served or the one they ran in for 2026, plus 9 with no 2026 race in our data. Part 3 checks that the result holds without these 21. |

### Ideology, a separate property of a member

The seat describes the district's voters (how the district voted for president). Ideology describes the member's
own votes in the House. A member in an exposed seat can still vote like a hardliner. In practice the two tend to
go together, which is why we ran check I.

| Term | Kind | What it means |
|---|---|---|
| DW-NOMINATE (first dimension) | Politics | A score for each member, calculated from all their roll-call votes. It runs from about −1 (most liberal) to +1 (most conservative). It comes from Voteview (`members.csv`, column `nominate_dim1`) and describes how a member votes, which may differ from what they believe or say. |
| Extremity | Ours | How far a member's score is from the centre, in their own party's direction. For Republicans it is the score itself; for Democrats it is minus the score. Higher means further from the centre. We use it to rank members inside their own party. |
| Moderate, extreme (within a party) | Ours | Members at the low or the high end of extremity inside their own party. It is relative: a moderate Republican still votes to the right of almost every Democrat. 22 of the 37 exposed Republicans and 27 of the 54 exposed Democrats are in their party's most moderate fifth. See also section 0. |
| Ideology band | Ours | One fifth of a party's members, ranked by extremity (we also tried thirds as a check). Check I shuffles the exposed label only among members of the same party and band. |

## 2. Bills and cosponsorship (the working map)

| Term | Kind | What it means |
|---|---|---|
| Bill | Politics | A proposed law. `bills.parquet` holds 12,987 House bills and resolutions from the 119th Congress, taken from govinfo's BILLSTATUS data. |
| Bill types | Politics | `hr` is H.R., a bill. `hres` is H.Res., a resolution of the House alone. `hjres` (H.J.Res.) and `hconres` (H.Con.Res.) are joint and concurrent resolutions. The working map and M6 use H.R. and H.J.Res. |
| Sponsor | Politics | The one member who introduces a bill. |
| Cosponsor | Politics | A member who adds their name to support someone else's bill. `cosponsors.parquet` has 149,015 of these. |
| Original cosponsor | Politics | A cosponsor who signed on the day the bill was introduced (column `original`). They usually helped write it. |
| Withdrawn | Politics | A cosponsor who took their name off the bill again. We remove these from the working map. |
| Co-lead | Ours | The sponsor of a bill, or an original cosponsor who did not withdraw. In part 3, a colleague who co-leads a bill that the release cites is named because of that bill, so the main measure leaves co-leads out (one robustness check puts them back). In the home map co-leads do count, because a named partner is a real tie. |
| Cross-party bill (M6) | Ours | A bill with an original cosponsor from the other party. |
| Policy area | Politics | The subject that Congress staff give each bill, such as Health or Emergency Management. |
| govinfo, BILLSTATUS | Data | The US government's publishing website, and its bulk download of every bill's status. Our bills, cosponsors and Congressional Record all come from govinfo. |
| Working tie | Ours | Two members are tied when one cosponsored a bill or joint resolution that the other sponsored. |
| Working map | Ours | The network of all working ties: 46,513 ties between the 450 members. It shows whom members work with on bills. |

## 3. Floor speeches (the floor map)

| Term | Kind | What it means |
|---|---|---|
| The floor | Politics | The chamber where the whole House debates and votes. A floor speech is something said there, in public. |
| Congressional Record | Politics | The official daily transcript of everything said on the floors of the House and the Senate. Our copy runs from 6 January 2025 to 9 November 2026. |
| Speaker turn | Data | One stretch of speech by one member without interruption. `speeches.parquet` has 35,629 turns. We keep the 17,824 turns on the House floor that a member spoke and that have at least 50 words. |
| Speaker check (S2) | Ours | Our test of whether each turn is credited to the right member. All 60 randomly drawn turns were (95% Wilson interval 94% to 100%). |
| Debate, Record item, `doc_id` | Ours | One item in the Record, usually the debate on one bill. The debate null shuffles names only inside one `doc_id`. |
| Floor manager | Politics | The member from each party who runs the debate on a bill and hands out speaking time. Every debate has one manager per party, so the floor has some cross-party contact built in. |
| Yield | Politics | Giving speaking time to another member: "I yield 2 minutes to the gentleman from Texas." It is procedure, not a free choice to name someone, so we leave yields out of the headline floor map (G1b). With yields kept, the result is 35.2% against 28.7%. |
| Yield rule | Ours | How the code spots a yield: "yield" (but not "yield back") comes before the name in the same sentence, or "for yielding" comes after it (G1c). On the 30 rows where it disagreed with an older rule (a 60-character window), all 15 rows that only our rule flagged really were yields. |
| "Will the gentleman yield?" | Politics | Asking the named member to give up some of their time. This is not a yield (G12): the speaker is addressing that member, usually in the middle of an argument. |
| Unanimous consent | Politics | A request to do something without a vote. It often names members. Part 2 codes it as procedure. |
| "The gentleman (or gentlewoman) from [state]" | Politics | How members refer to each other on the floor, often followed by the name in brackets: "(Mr. Peters)". The matching code reads these. |
| Floor mention | Ours | One member naming another on the floor. `Martin/mentions.parquet` holds 9,988. The 8,469 between Republicans and Democrats, without yields, make up the headline map. |
| Floor tie, floor map | Ours | Two members are tied when either one named the other at least once. That gives 3,970 ties, with no direction and no weights. The floor map shows whom members talk about in Washington. |

## 4. Press releases (part 3: the close-up and the home map)

| Term | Kind | What it means |
|---|---|---|
| Press release | General | A short news text that a member's office posts on its own `house.gov` website, such as "Lawler introduces bipartisan bill to...". |
| Listing, listing page | General | The page on a member's website that lists their press releases, newest first, spread over many pages. |
| Collector (A1) | Ours | Anas's program that follows each listing back to 3 January 2025 and saves the full text and date of every release (`Anas/collector/`). It respects each site's `robots.txt`. |
| Press-release data | Ours | 55,023 releases from 412 members, from 3 January 2025 to 20 November 2026 (the day of the download), stored in three files split by member (`Anas/press_releases/`). Not collected: four members whose listing needs JavaScript or no longer exists, Jim Jordan (his listing stops in 2024), and the 12 members who left office. |
| Template release | Ours | A text posted by five or more members, such as "Newest Members of Congress". There are 64 such releases, and we set them aside. |
| Repeated sentence | Ours | A sentence a member puts in many of their releases, such as a short bio or press contact line. We found 84, in 41 members, and do not count them as part of a release's content. |
| Press mention | Ours | One member naming another in a release, found by the shared matching code plus the press layer. There are 129,473 (release, member) pairs; 14.4% of them cross party lines. |
| Press layer | Ours | The few extra rules we use for releases on top of Martin's matching code: full names without a title, the first names members use for themselves, party-state tags, lists across tags, nicknames in quotes, middle initials, and a guard against state legislators. Every hit records which rule found it. |
| Party-state tag | Politics | A tag like `(R-NY)` after a name in a release. It has to match the member list on both party and state, otherwise senators slip in. |
| Release-to-bill link (A3.5) | Ours | A release is linked to a House bill through the bill's number, or through an official title that belongs to that bill alone. There are 18,177 links in 13,944 releases (25%). A check found 30 of 30 correct for each kind. |
| Caucus release, redistricting release | Ours | A caucus release comes from a group such as the Problem Solvers Caucus, which names members because they belong to it, not by choice. A redistricting release is about the new maps. We flag both kinds and leave them out in two robustness checks. |
| The outcome of part 3 | Ours | For each member: the share of their releases that name at least one House member of the other party who is neither a party leader nor a co-lead of a bill the release cites. Measured for the 406 members with at least 10 releases (53,664 releases). |
| Name, naming | Ours | What the paper says members do: they "name the other party". We avoid "show" or "praise", because tone was only measured in check T, where most named members turned out to be partners. |
| Close-up | Ours | Part 3 of the paper: whom members name at home, by type of seat. Exposed Republicans 13.3% against 9.2% for safe ones; exposed Democrats 11.6% against 9.0%. |
| Check T (what the names do) | Ours | 60 counted names, 15 for each party and type of seat, read by three blind AI readers: 46 partners or praise (77%), 9 neutral, 4 wrong matches and 1 criticism. |
| Check I (ideology) | Ours | We shuffled the exposed label only within the same party and ideology band. Ideology alone accounts for 2.9 of the 4.1 Republican points and 2.4 of the 2.6 Democratic points. With our data we cannot separate the seat from ideology. |
| Home map | Ours | The network of press mentions among the same 406 members: two members are tied when one names the other in a release (co-leads count, leaders do not count as the one named). It has 6,765 cross-party ties, and in 2,060 of them both members name each other. The group accepted it into the paper on 25 Nov. |
| Hub (of the home map) | Ours | A member with many ties. Exposed members are 22% of the members, but they send 35% and receive 34% of the cross-party ties. |
| Bridging by volume, bridging by position | Ours | The twist in part 3's network results. Exposed Republicans have more backbone ties than safe Republicans: they bridge by volume. Exposed Democrats do not have more ties, but they lie on more shortest paths than their number of ties would suggest: they bridge by position. Both results are borderline after Holm's correction, and we did not test why. |
| Mutual pair | Ours | Two members of different parties who name each other, such as Golden and Fitzpatrick, Kaptur and Fitzpatrick, or Golden and Lawler. Documented in Anas's folder, not in the paper. |
| "Says bipartisan" (A5) | Ours | A release that uses the word "bipartisan" outside the member's repeated sentences: 13,744 of the 53,664 releases (25.6%). |
| "Has a partner" (A5) | Ours | The release names a House member of the other party (not a leader), or cites a bill that has one as co-lead. These are called "named" and "on record"; the main measure, "either", counts both. 63.9% of releases that say "bipartisan" have a partner, against 8.6% of other releases. |
| Mirror check (A5) | Ours | A check of whether the members named in "bipartisan" releases are working with the member or are being opposed. Of 30 releases, 28 name partners and none names an opponent. Its counterpart, the check of releases without a partner, found that 29 of 30 really name none. |
| Common date window | Ours | The same start and end date for every member: 3 January 2025 to 20 November 2026. We need it because 27 Republican and 5 Democratic websites stopped posting before September 2026. |
| Newsletter | General | An email a member sends to people in their district. We did not collect newsletters, and press releases do not include them, ads or social media. (planning only) |
| Scope scan | Ours | Anas's count on 18 Nov of how many releases each member had posted: 56,747. It was too high, because some sites show two dates for each release. It was used to plan the collection, and the collector's own counts replaced it. (planning only) |
| Name pilot | Ours | 20 releases each from 16 members, read on 18 Nov to see whether anyone names the other party at all. Too small to report. (planning only) |
| Showing, showcase tie, mutual showing | Ours | Our early words for naming a colleague at home. Replaced by "name" and "mutual pair". (planning only) |

## 5. Networks and null models

| Term | Kind | What it means |
|---|---|---|
| Node | Course | One point in a network; for us, one member. The working and floor maps share the same 450 nodes; the home map has the 406 members of part 3. |
| Tie, edge, link | Course | A connection between two nodes. Depending on the map, it means signing a bill together, naming someone on the floor, or naming someone at home. |
| Directed | Course | A tie that has a direction: "A names B" is different from "B names A". Mentions are directed, and `named_ties.csv` has one row for each (speaker, named) pair: 5,400. The two maps of part 1 ignore direction. |
| Weighted | Course | A tie that has a strength. The two maps of part 1 have no weights. The home map does: each name in a release counts 1/n, where n is the number of colleagues the release names, so a list of 40 names adds only 1/40 for each name. |
| The two maps | Ours | The working map and the floor map, on the same 450 members. They are the paper's headline. The home map is a third network, used in part 3. |
| Cross-party share | Ours | The share of ties that join a Republican and a Democrat. Higher means less divided. Floor map 38.7%, working map draws 28.6%. |
| Party modularity (Q) | Course | One number for how many more ties stay inside a party than chance would give. 0 means no more than chance. Floor 0.112, working map draws 0.211. It changes with the number of ties, so maps are only compared at the same size. |
| Thinning, random working draws (G1a) | Ours | The floor map has 3,970 ties and the working map 46,513. To compare them fairly, we draw 3,970 working ties at random, 200 times. This is the headline comparison. |
| Strongest ties | Ours | The 3,970 pairs of members who share the most bills. A second comparison: close allies are far more split by party (12.8% cross-party). |
| Null model | Course | A shuffled version of a network, used to ask "would we see this by chance?" When the real number lies outside all the shuffled ones, chance is an unlikely explanation. |
| Degree-preserving rewiring | Course | A null model that swaps the ends of ties while every member keeps the same number of ties (double-edge swaps, Maslov and Sneppen). Under it, both maps come out about 50% cross-party with Q near 0. |
| Debate null (M4) | Ours | Names are shuffled only inside each debate, so every debate keeps the same people. Q drops from 0.112 to 0.074. So the way debates are organised explains about two thirds of the floor map's split by party, and the rest is beyond every shuffle. |
| State null (M3b, G16) | Ours | A rewiring that also keeps each member's number of ties inside their own state. Q is 0.001, so state delegations explain almost none of the split. |
| Bipartite rewiring (home map) | Ours | Swaps that keep every tie cross-party and keep each member's number of cross-party ties. 10.7% of cross-party ties join two exposed members, against 10.2% after rewiring: a small preference. |
| Draws, shuffles, seed | Course | One shuffled version is one draw. We use 200 draws (10,000 when shuffling labels) and the seed 2805, so anyone can repeat them. |
| Louvain communities | Course | A method that splits a network into groups with many ties inside and few between (resolution 1, 50 random starts, best result kept). The working map splits into the two parties. The floor map splits into 8 groups that mix both parties and follow committees. The home map gives 11 groups, one of them a group of 35 members in close seats (documented, not in the paper). |
| NMI (normalised mutual information) | Course | A score from 0 to 1 for how well two ways of grouping the same members agree. Communities compared with party: working map 0.83, floor map 0.03, home map 0.20. |
| Committee communities | Ours | In 7 of the floor map's 8 communities, one committee is 3.0 to 7.9 times more common than in the House overall. 44% of floor ties join two members of the same committee, against 17.1% after rewiring. |
| Backbone, disparity filter | Course | The disparity filter keeps only the ties that are unusually strong for at least one of the two members (week 4; Serrano and others, 2009). The ties it keeps are the backbone. We use it on the home map at α = 0.01, the strictest setting that still keeps all 406 members connected: 1,656 of 29,210 ties. |
| α (alpha), α sweep | Course | How strict the disparity filter is: a smaller α keeps fewer ties. The sweep repeats every home map result for α from 0.005 to 0.2, and all of them point the same way. |
| Degree, cross-party degree | Course | How many ties a member has, and how many of those cross the aisle. Exposed members' cross-party degree: Republicans 54 against 28, Democrats 46 against 30. |
| Betweenness | Course | How often a member lies on the shortest paths between other members. A measure of being "in between". |
| Closeness | Course | How few steps a member needs to reach everyone else. It hardly varies in a network as dense as ours. |
| Betweenness given degree | Ours | The betweenness that is left once we allow for the number of ties (the residual from regressing log betweenness on log degree). It asks: does this member sit "in between" more than their ties alone would predict? |
| ForceAtlas2 | Course | The method that placed the members when we drew the home map (week 4). The positions in the picture are not a measurement. |
| Ego network | Course | One member plus everyone they are tied to. (planning only) |

## 6. Finding names in text, and labelling them

| Term | Kind | What it means |
|---|---|---|
| Mention | Ours | One place in a text where one member names another. `mentions.parquet` has the columns `speaker`, `named`, `source`, `date`, `doc_id`, `context`, `is_yield` and `how` (the rule that found it). |
| Matcher (M1, `Martin/matcher.py`) | Ours | The shared code that finds members' names in a text and turns them into Bioguide IDs. Floor and press use the same code, so the maps can be compared. |
| Title | Politics | Words such as "Rep.", "Mr.", "Congresswoman" or "Chairman". The matcher looks for a title followed by a surname. |
| Untitled full name | Ours | A full name without a title, as in "my friend, Chip Roy". Matched on the floor too since G19, with a guard against names after "Senator", "Governor" and similar words. |
| List rule | Ours | In "Representatives Lawler, Golden, and Fitzpatrick", every name in the list is matched (G14). |
| Possessive, middle initial | Ours | "Mr. Cole's amendment" gives Cole, and "Rep. James P. McGovern" gives McGovern, not John James (G18). |
| Shared surname | Ours | When members share a surname, the matcher tells them apart by first name (official or nickname), then by a state name within 80 characters. If neither works, the name is dropped (828 names with a title). |
| Alias, nickname | Course | Another name for the same person, such as "Hank" Johnson. Official nicknames come from `unitedstates/congress-legislators`. No list of nicknames is ever complete, which is why we measure recall. |
| Leader title (`is_leader_title`) | Data | A column marking a mention made through a leadership title, such as "Speaker Johnson". |
| Context | Ours | The sentence with the name plus one sentence on each side, at most 1,000 characters. This is what coders read. |
| Precision | Course | Of the names the matcher found, the share that were the right member. Floor: 98 of 100 (Diego's D2 sample). Press: 0.96. |
| Recall | Course | Of the names that were really in the text, the share the matcher found. Floor: 12 of 13 (30 turns read in full). Press: 0.97 (40 releases, five blind AI readers). |
| Recall check | Ours | Reading texts chosen without using the matcher, listing every member named in them, and counting how many the matcher found. It is the only way to measure missed names, since a sample drawn from the matcher's own output contains only the names it found. |
| Labelling, coding | Course | Reading a mention and giving it a code by hand. Part 2 of the paper (Diego). |
| The five codes (D2) | Ours | P, procedure (yields, unanimous consent). A, agreeing (thanks, praise, partnership, support for the member's bill). D, disagreeing (rebuttal, criticism, blame). N, neutral (a reference that takes no side). X, not that member (a wrong match, or Record text nobody said). When two codes fit, the order X, P, D, A, N decides. Cross-party mentions: 69% agreeing, 23% neutral, 7% disagreeing. |
| Coder, second coder | Course | Diego coded all 100 mentions. Martin (rows 1 to 25), Claude (rows 26 to 75) and Anas (rows 76 to 100) were second coders. |
| Cohen's κ (kappa) | Course | How much two coders agree beyond what guessing would give. 0 means chance, 1 means perfect. Human coders: 0.64 (0.59 and 0.69 for the two pairs), above the 0.6 we set in advance. Diego and Claude: 0.72. |
| Blind AI reader | Ours | A run of Claude that codes or lists names using only a written packet, without seeing the seat, the party or the other readers' answers. Used in part 3's checks. The readers are all the same kind of model, so their agreement shows they are consistent, not that they are right; a person reads every case where they disagree. |
| TF-IDF | Course | A way to turn text into numbers: words that are common in one text but rare across all texts get a high weight (course week 6). |
| Classifier (D5) | Ours | A logistic regression model on TF-IDF numbers, trained on the 100 hand labels to label all 9,909 floor mentions. It got 73% right, against 72% for always guessing "agreeing" (macro F1 0.26), so we do not use it as a measurement. |
| Baseline (for a classifier) | Course | The score you get without a model, here by always guessing the most common code. |
| Leave-one-out | Statistics | Testing a model on each labelled row in turn, after training it on the other 99. Used for D5 because 100 labels are too few to set some aside for testing. |
| Macro F1 | Statistics | The F1 score worked out for each code and then averaged with equal weight, so a model that only guesses the most common code gets a low score. |
| Regex | General | A text pattern for finding things like `H.R. 152` or `(R-NY)`. |
| Lexicon, dictionary method | Course | Counting the words from a fixed list (course week 7). A5 looks for one word: "bipartisan". |

## 7. Statistics and research design

| Term | Kind | What it means |
|---|---|---|
| Observation vs result | Ours | An observation comes from one run and has not been checked yet. A result has been checked, with a null model, a second method or a hand-read sample. |
| Fixed in advance | Ours | A design, a measure or a rule for reading the result that was written down before the analysis was run: the A4 plan (20 Nov), the home map plan, checks T and I, and A5. The paper uses "fixed before the analysis" only for these. |
| Within-party comparison | Ours | Comparing exposed with safe seats inside one party, and only then comparing that gap between the two parties. Each party is its own baseline. |
| Interaction | Statistics | The difference between the Republican gap and the Democratic gap: +1.5 points (p 0.36), too small to tell apart from zero. |
| Seat effect vs president's-party effect | Ours | A seat effect means that anyone in a close district names the other side more. A president's-party effect means that only the president's party does. Part 3 reads its result as a seat effect, which we cannot separate from ideology. |
| Confound | Statistics | Something else that could produce the same pattern. Part 3 measured one (ideology) and could not measure another (being in the majority). |
| Permutation test | Course | Shuffling labels many times to see how often chance alone gives a result as large as the real one. p is the share of shuffles that are at least as extreme, counting both directions. Part 3 shuffles the exposed label inside each party; M6 shuffles, inside each member, which bills count as cross-party. |
| Stratified shuffle | Ours | A permutation test whose shuffles stay inside groups. In check I, the groups are party and ideology band. |
| Holm's correction | Statistics | A rule for testing ten comparisons together that keeps the chance of even one false alarm at 5% (`holm1979`). Used on the home map. The course does not teach it. |
| Wilson interval | Statistics | A 95% interval for a share from a small sample that stays sensible close to 0% or 100%: 60 out of 60 gives 94% to 100% (`wilson1927`). The course does not teach it. |
| 95% interval | Statistics | The range in which a number would most likely land if we drew the sample again. |
| Robustness row, robustness check | Statistics | The same test, rerun under another reasonable choice: a cut-off of 4 or 6, the second lean measure, without the relabelled members, and so on. Part 3 holds in every one. |
| Leave one state out | Ours | Rerunning the test with each state left out in turn. No single state carries part 3's gap. |
| Seed | Course | A fixed starting number for random draws, so the same draws come out every time. Ours is 2805. |
| Held-out rows | Course | Rows a rule was not built on, used to test it fairly, such as the 30 rows for the yield rule. |
| Difference-in-differences | Statistics | The name for a comparison like ours when it is made before and after an event. Ours has no before and after, so it is called an interaction. (planning only) |

## 8. How the group works

| Term | Kind | What it means |
|---|---|---|
| G1a, G13, ... | Ours | The entries in `DECISIONS.md`. Each one records a decision, the reason for it and the alternative. |
| M1 to M8, A1 to A6, D1 to D5, S1 to S3 | Ours | The tasks in `WORK_AND_DEADLINES.md`: M is Martin's, A is Anas's, D is Diego's, S is shared. |
| Parts 1, 2, 3 | Ours | The three parts of the Results: the two maps (Martin), what a mention means (Diego), and the close-up at home (Anas). |
| Freeze (G7, G17) | Ours | The scope was frozen on Sat 21 Nov and the numbers on Sun 22 Nov. On 25 Nov all three agreed to close the analysis: nothing new is added, and we only cut or refine. |
| Stop rule (G5) | Ours | The rule that the close-up would be dropped if there were no press data for the first 20 members by Fri 20 Nov. Passed on 20 Nov. (planning only) |
| Shared files | Ours | `mentions.parquet`, `named_ties.csv` and the press release files. Their columns are fixed. |
| Own folder | Ours | `Anas/`, `Martin/` and `Diego/`. Each person writes only in their own folder. The files at the project level (this one, `DECISIONS.md`, `WORK_AND_DEADLINES.md`, `OFF_CURRICULUM.md`) and `report/` are shared. |
| robots.txt | General | A file on each website that says what automated programs may download. On the members' sites it allows press release pages, and the collector follows it. |
| `AI_METHODS.md` | Course | The file the course requires, listing every place a model touched a result and how we checked it. Diego keeps it (`Diego/AI_METHODS.md`), and it is copied to `docs/AI_METHODS.md` before hand-in. |
| `OFF_CURRICULUM.md` | Ours | Every method we use that the course does not teach, with its reference and why it fits. |

## A to Z index

Each term links to the table it is in. A word can appear twice: once in section 0 (how its meaning is narrower
here) and once in its topic section.

A: [Agreeing, disagreeing](#about-what-members-do), [`AI_METHODS.md`](#8-how-the-group-works), [Alias, nickname](#6-finding-names-in-text-and-labelling-them), [At-large district](#1-congress-and-elections)  
B: [Backbone](#about-the-maps-and-the-network), [Backbone, disparity filter](#5-networks-and-null-models), [Baseline (for a classifier)](#6-finding-names-in-text-and-labelling-them), [Betweenness](#5-networks-and-null-models), [Betweenness given degree](#5-networks-and-null-models), [Bill](#2-bills-and-cosponsorship-the-working-map), [Bill types](#2-bills-and-cosponsorship-the-working-map), [Bioguide ID](#1-congress-and-elections), [Bipartisan](#about-what-members-do), [Bipartite rewiring (home map)](#5-networks-and-null-models), [Blind (reader)](#about-results-and-checks), [Blind AI reader](#6-finding-names-in-text-and-labelling-them), [Borderline](#about-results-and-checks), [Bridge, broker](#about-the-maps-and-the-network), [Bridging by volume, bridging by position](#4-press-releases-part-3-the-close-up-and-the-home-map)  
C: [Caucus release, redistricting release](#4-press-releases-part-3-the-close-up-and-the-home-map), [Check](#about-results-and-checks), [Check I (ideology)](#4-press-releases-part-3-the-close-up-and-the-home-map), [Check T (what the names do)](#4-press-releases-part-3-the-close-up-and-the-home-map), [Classifier (D5)](#6-finding-names-in-text-and-labelling-them), [Close-up](#4-press-releases-part-3-the-close-up-and-the-home-map), [Closeness](#5-networks-and-null-models), [Co-lead](#about-what-members-do), [Co-lead](#2-bills-and-cosponsorship-the-working-map), [Coder, second coder](#6-finding-names-in-text-and-labelling-them), [Cohen's κ (kappa)](#6-finding-names-in-text-and-labelling-them), [Collector (A1)](#4-press-releases-part-3-the-close-up-and-the-home-map), [Committee communities](#5-networks-and-null-models), [Committee, chairman, ranking member](#1-congress-and-elections), [Common date window](#4-press-releases-part-3-the-close-up-and-the-home-map), [Community](#about-the-maps-and-the-network), [Confound](#7-statistics-and-research-design), [Congress](#1-congress-and-elections), [Congressional Record](#3-floor-speeches-the-floor-map), [Context](#6-finding-names-in-text-and-labelling-them), [Cook PVI (Partisan Voting Index)](#district-lean-and-exposed-seats), [Cosponsor](#2-bills-and-cosponsorship-the-working-map), [Credit, acknowledgement](#about-what-members-do), [Cross-party bill (M6)](#2-bills-and-cosponsorship-the-working-map), [Cross-party share](#5-networks-and-null-models), [Cross-party, across the aisle](#about-what-members-do), [Crossover](#about-seats-and-members), [Crossover seat](#district-lean-and-exposed-seats)  
D: [Debate](#about-the-maps-and-the-network), [Debate null (M4)](#5-networks-and-null-models), [Debate, Record item, `doc_id`](#3-floor-speeches-the-floor-map), [Degree, cross-party degree](#5-networks-and-null-models), [Degree-preserving rewiring](#5-networks-and-null-models), [Delegate](#1-congress-and-elections), [Difference-in-differences](#7-statistics-and-research-design), [Directed](#5-networks-and-null-models), [District (congressional district)](#1-congress-and-elections), [District lean](#district-lean-and-exposed-seats), [Divided, division (by party)](#about-the-maps-and-the-network), [Draws, shuffles, seed](#5-networks-and-null-models), [DW-NOMINATE (first dimension)](#ideology-a-separate-property-of-a-member)  
E: [Ego network](#5-networks-and-null-models), [Exposed (seat)](#about-seats-and-members), [Exposed seat (the rule in the paper, G13)](#district-lean-and-exposed-seats), [Extreme](#about-seats-and-members), [Extremity](#ideology-a-separate-property-of-a-member)  
F: [Fixed in advance](#about-results-and-checks), [Fixed in advance](#7-statistics-and-research-design), [Floor (map)](#about-the-maps-and-the-network), [Floor manager](#3-floor-speeches-the-floor-map), [Floor mention](#3-floor-speeches-the-floor-map), [Floor tie, floor map](#3-floor-speeches-the-floor-map), [ForceAtlas2](#5-networks-and-null-models), [Freeze (G7, G17)](#8-how-the-group-works)  
G: [G1a, G13, ...](#8-how-the-group-works), [govinfo, BILLSTATUS](#2-bills-and-cosponsorship-the-working-map)  
H: ["Has a partner" (A5)](#4-press-releases-part-3-the-close-up-and-the-home-map), [Held-out rows](#7-statistics-and-research-design), [Holds](#about-results-and-checks), [Holm's correction](#7-statistics-and-research-design), [Home map](#4-press-releases-part-3-the-close-up-and-the-home-map), [Home, at home](#about-the-maps-and-the-network), [House of Representatives (the House)](#1-congress-and-elections), [Hub](#about-the-maps-and-the-network), [Hub (of the home map)](#4-press-releases-part-3-the-close-up-and-the-home-map)  
I: [Ideology](#about-seats-and-members), [Ideology band](#ideology-a-separate-property-of-a-member), [Incumbent](#1-congress-and-elections), [Interaction](#7-statistics-and-research-design)  
L: [Labelling, coding](#6-finding-names-in-text-and-labelling-them), [Leader](#about-seats-and-members), [Leader title (`is_leader_title`)](#6-finding-names-in-text-and-labelling-them), [Lean](#about-seats-and-members), [Leave one state out](#7-statistics-and-research-design), [Leave-one-out](#6-finding-names-in-text-and-labelling-them), [Lexicon, dictionary method](#6-finding-names-in-text-and-labelling-them), [List rule](#6-finding-names-in-text-and-labelling-them), [Listing, listing page](#4-press-releases-part-3-the-close-up-and-the-home-map), [Louvain communities](#5-networks-and-null-models)  
M: [M1 to M8, A1 to A6, D1 to D5, S1 to S3](#8-how-the-group-works), [Macro F1](#6-finding-names-in-text-and-labelling-them), [Majority, minority](#1-congress-and-elections), [Matcher (M1, `Martin/matcher.py`)](#6-finding-names-in-text-and-labelling-them), [Member, representative, congressman, congresswoman](#1-congress-and-elections), [Mention](#about-what-members-do), [Mention](#6-finding-names-in-text-and-labelling-them), [Midterm election](#1-congress-and-elections), [Mirror check (A5)](#4-press-releases-part-3-the-close-up-and-the-home-map), [Moderate](#about-seats-and-members), [Moderate, extreme (within a party)](#ideology-a-separate-property-of-a-member), [Mutual pair](#4-press-releases-part-3-the-close-up-and-the-home-map)  
N: [Name pilot](#4-press-releases-part-3-the-close-up-and-the-home-map), [Name, naming](#about-what-members-do), [Name, naming](#4-press-releases-part-3-the-close-up-and-the-home-map), [Newsletter](#4-press-releases-part-3-the-close-up-and-the-home-map), [NMI (normalised mutual information)](#5-networks-and-null-models), [Node](#5-networks-and-null-models), [Null model](#5-networks-and-null-models)  
O: [Observation vs result](#7-statistics-and-research-design), [`OFF_CURRICULUM.md`](#8-how-the-group-works), [Original cosponsor](#2-bills-and-cosponsorship-the-working-map), [Own folder](#8-how-the-group-works)  
P: [Partner](#about-what-members-do), [Parts 1, 2, 3](#8-how-the-group-works), [Party](#1-congress-and-elections), [Party leaders](#1-congress-and-elections), [Party modularity (Q)](#5-networks-and-null-models), [Party-state tag](#4-press-releases-part-3-the-close-up-and-the-home-map), [Permutation test](#7-statistics-and-research-design), [Polarization](#about-the-maps-and-the-network), [Policy area](#2-bills-and-cosponsorship-the-working-map), [Possessive, middle initial](#6-finding-names-in-text-and-labelling-them), [Precision](#6-finding-names-in-text-and-labelling-them), [President's party](#1-congress-and-elections), [President's party, majority](#about-seats-and-members), [Press layer](#4-press-releases-part-3-the-close-up-and-the-home-map), [Press mention](#4-press-releases-part-3-the-close-up-and-the-home-map), [Press release](#4-press-releases-part-3-the-close-up-and-the-home-map), [Press-release data](#4-press-releases-part-3-the-close-up-and-the-home-map), [Procedure](#about-what-members-do)  
R: [Recall](#6-finding-names-in-text-and-labelling-them), [Recall check](#6-finding-names-in-text-and-labelling-them), [Redistricting, redraw, redrawn state](#1-congress-and-elections), [Regex](#6-finding-names-in-text-and-labelling-them), [Relabelled members](#district-lean-and-exposed-seats), [Release-to-bill link (A3.5)](#4-press-releases-part-3-the-close-up-and-the-home-map), [Repeated sentence](#4-press-releases-part-3-the-close-up-and-the-home-map), [robots.txt](#8-how-the-group-works), [Robustness row, robustness check](#7-statistics-and-research-design), [Roll call](#1-congress-and-elections)  
S: [Safe (seat)](#about-seats-and-members), [Safe seat](#district-lean-and-exposed-seats), ["Says bipartisan" (A5)](#4-press-releases-part-3-the-close-up-and-the-home-map), [Scope scan](#4-press-releases-part-3-the-close-up-and-the-home-map), [Seat](#1-congress-and-elections), [Seat effect](#about-results-and-checks), [Seat effect vs president's-party effect](#7-statistics-and-research-design), [Second lean measure](#district-lean-and-exposed-seats), [Seed](#7-statistics-and-research-design), [Senate, senator](#1-congress-and-elections), [Served district, 2026 district](#1-congress-and-elections), [Shared files](#8-how-the-group-works), [Shared surname](#6-finding-names-in-text-and-labelling-them), [Showing, showcase tie, mutual showing](#4-press-releases-part-3-the-close-up-and-the-home-map), [Significant](#about-results-and-checks), [Speaker](#1-congress-and-elections), [Speaker check (S2)](#3-floor-speeches-the-floor-map), [Speaker turn](#3-floor-speeches-the-floor-map), [Sponsor](#2-bills-and-cosponsorship-the-working-map), [State delegation](#1-congress-and-elections), [State null (M3b, G16)](#5-networks-and-null-models), [Stop rule (G5)](#8-how-the-group-works), [Stratified shuffle](#7-statistics-and-research-design), [Strongest ties](#5-networks-and-null-models), [Swing seat (also competitive, battleground)](#about-seats-and-members)  
T: [Template release](#4-press-releases-part-3-the-close-up-and-the-home-map), [TF-IDF](#6-finding-names-in-text-and-labelling-them), [The five codes (D2)](#6-finding-names-in-text-and-labelling-them), [The floor](#3-floor-speeches-the-floor-map), ["The gentleman (or gentlewoman) from [state]"](#3-floor-speeches-the-floor-map), [The outcome of part 3](#4-press-releases-part-3-the-close-up-and-the-home-map), [The two maps](#5-networks-and-null-models), [Thinning, random working draws (G1a)](#5-networks-and-null-models), [Tie, edge, link](#5-networks-and-null-models), [Title](#6-finding-names-in-text-and-labelling-them)  
U: [Unanimous consent](#3-floor-speeches-the-floor-map), [Untitled full name](#6-finding-names-in-text-and-labelling-them)  
V: [Voteview](#1-congress-and-elections)  
W: [Weighted](#5-networks-and-null-models), [Why "450 members"](#1-congress-and-elections), ["Will the gentleman yield?"](#3-floor-speeches-the-floor-map), [Wilson interval](#7-statistics-and-research-design), [Withdrawn](#2-bills-and-cosponsorship-the-working-map), [Within-party comparison](#7-statistics-and-research-design), [Working (map)](#about-the-maps-and-the-network), [Working map](#2-bills-and-cosponsorship-the-working-map), [Working tie](#2-bills-and-cosponsorship-the-working-map)  
Y: [Yield](#3-floor-speeches-the-floor-map), [Yield rule](#3-floor-speeches-the-floor-map)  
α (Greek letters): [α (alpha), α sweep](#5-networks-and-null-models)  
Other: [119th Congress](#1-congress-and-elections), [95% interval](#7-statistics-and-research-design)  
