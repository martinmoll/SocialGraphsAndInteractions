# Methods drafts (A6)

> **25 Nov:** the final Methods text is [`methods_press.tex`](methods_press.tex). This file is kept because it holds
> the **A4 analysis plan written on 20 Nov before any release was analysed** (`a4/analysis.py` implements it) and
> the checks fixed in advance; the draft sentences below are superseded.

Anas. Sentences for the paper's Methods and limitations, written before the results so the choices are fixed
first. Text in [brackets] is filled in after A4. Each draft says where it would go and why.

## District lean and redrawn states (drafted 19 Nov)

**Methods, data paragraph:**

> District lean is the 2025 Cook Partisan Voting Index of the district each member represented in 2025–26.
> Nine states redrew their districts for the 2026 election, so for their 173 seats the 2026 lean describes a
> different area. We use the map members served, because the press releases were written for its voters.
> The lean agrees with the 2024 presidential margin on the same districts (The Downballot; r = 0.999).

**Limitations:**

> In redrawn states a member may have addressed the voters of their future district once the new map was
> known. Labelling exposure by the 2026 district each member ran in changes the label of 12 members, and 9 more
> could not be placed; [the result holds / changes] without these 21.

Source and checks: [`district_lean/README.md`](district_lean/README.md).

## A4 analysis plan (written 20 Nov, before any release text was analysed)

**Unit.** One member. Members with fewer than 10 releases in the window are reported but left out of the test
(their shares are too noisy). Party leaders stay in as authors; being named by others does not count (below).

**Outcome per member.** The share of their releases, within the common date window, that name at least one House
member of the other party who is (a) not a sponsor or original cosponsor of a bill the release mentions
(co-lead, from A3) and (b) not a party leader. Party leaders: Speaker, majority and minority leaders, whips and
conference/caucus chairs of the 119th Congress (list fixed in A3 before matching, from the House Clerk's
leadership page).

**Groups.** Party (R, D) × exposure (`exposed_2025`: lean ±5 on the district served, `district_lean/member_lean.csv`).

**Quantity tested.** The interaction: (mean share of exposed R − mean share of safe R) − (mean share of exposed
D − mean share of safe D). Each party's own gap is reported as well.

**Test.** Permutation test: shuffle `exposed_2025` among the members of each party separately (each party keeps
its number of exposed members; party is never shuffled), recompute the three quantities, 10,000 shuffles, seed
2805. Two-sided p-value = share of shuffles with an absolute value at least as large as observed. Figure: the null
distribution with the observed value marked.

**Wording.** "Consistent with a seat effect / a party effect", never "because".

**Reading the result** (fixed in advance):

| Exposed − safe gap | Reading |
|---|---|
| Positive in both parties, interaction near 0 | Seat effect: members in close seats show the other side, whatever their party |
| Positive for Republicans only, interaction positive | Consistent with a president's-party effect in a midterm year |
| No gap in either | Exposure does not go with naming the other side; part 3 reports whom members show, not why |

**Robustness checks** (each reruns the same test): checks 1 to 4 below, without caucus releases, leave one state
out, and the outcome counted with co-leads included.

## Checks planned for redrawn states (drafted 19 Nov, not yet run)

Decided before any release text is read:

1. **Without the 21.** Rerun the exposed-against-safe comparison leaving out the 12 members whose label differs
   between the district they served and the 2026 district they ran in, and the 9 with no 2026 contest in our data. Reported in the limitations sentence above.
2. **Releases about redistricting.** Flag releases that mention redistricting or the new map (`redistrict`,
   `new map`, `gerrymander`). In redrawn states these releases often name the other party in a fight over the
   map, not to show a partner. Report how many there are, and the result with them left out.
3. **Optional, only if A4 is done before Sun 22 Nov:** for members in redrawn states,
   the share naming the other party before and after their state's new map passed, against members in states
   that did not redraw over the same months. Otherwise one sentence in the Discussion as future work.
   Dates: `district_lean/redraw_dates.csv`, checked against official pages and news on 20 Nov. Only the five states
   that settled their maps in Aug to Nov 2025 (TX, NC, OH, CA, UT) leave a usable "after" period; the four from
   May 2026 are left out or reported apart.
4. **Cut-off.** The exposed/safe split at lean ±5 is a working rule. Rerun A4 with ±4 and ±6, or with lean as a
   number. Ten members change label between the Cook lean and the 2024 margin, all at the cut-off, so the cut-off
   matters more than the source.

5. **Recall of the name matcher on press releases** (added 20 Nov). Precision is measured (code X in Diego's
   sample), but a missed name never reaches that sample, so recall is unmeasured. Draw 30 releases at random
   from `press_releases.parquet` (fixed seed), spread over both parties and the four layouts. Read each one and
   list every House member named, in any form (title, full name, nickname, list, possessive). Count how many the
   matcher finds. Report recall with its interval, and list the forms it missed. One hour of reading.
   Draft sentence: *"On 30 hand-read releases the matcher found [x] of [y] named House members (recall [z]%,
   95% CI [a–b]); missed names were mostly [forms]. A name in a form neither the matcher nor the readers
   recognised cannot be counted, so the true recall may be somewhat lower."*

## Data sources for part 3 (drafted 20 Nov)

For the Methods data paragraph and the reference list. Every table is joined on the member's Bioguide ID.

| What | Source | Kind |
|---|---|---|
| Press releases | Each member's own `house.gov` site (and its WordPress API where it has one) | Primary: the members |
| Members, official sites | `unitedstates/congress-legislators` | Open data compiled from official sources |
| District lean (served map) | 2025 Cook PVI, via Wikipedia *Cook Partisan Voting Index*, revision of 25 May 2025 | Secondary, pinned |
| Second lean measure | The Downballot, 2024 presidential results on the 2024 district lines | Independent compilation (cite and link) |
| District run in 2026, fate | 2026 House elections page on Wikipedia (snapshot 11 Nov 2026), via `incumbents.csv` | Secondary |
| Redrawn states and map dates | Wikipedia, checked against state sources (California Secretary of State, Texas Senate Journal, NC session law, Ohio Secretary of State) and court filings | Official where opened |
| Bills, cosponsors (for A3) | govinfo BILLSTATUS | Primary: US government |
