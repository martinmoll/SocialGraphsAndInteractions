# Anas: status, findings and proposals

Anas, Friday 20 November 2026. **Start here.** This replaces `REVISIONS_19NOV.md` and is kept up to date.
**Proposals, not decisions:** parts 1 and 2 belong to Martin and Diego, who decide on anything in them. Agreed
changes go into `DECISIONS.md` before the freeze on Sun 22 Nov (G7).

## 1. Priority list for the group

Ordered by how much depends on it. Items 1 and 2 matter to all three parts.

| # | Who | What | Why it comes first | By |
|---|---|---|---|---|
| 1 | **Martin** | **Matcher fixes:** items 9 (nicknames), 1 (name lists), 2 (untitled full names), 10 (state legislators) in [`MATCHER_CHECKLIST.md`](MATCHER_CHECKLIST.md) | The floor map (part 1), Diego's sample (part 2) and the press mentions (part 3) all come from the matcher. Six members are dropped whenever named by nickname (Hank Johnson, Bobby Scott, Chris Smith, Buddy Carter, Hal Rogers, Chuy García) | Sun 22 Nov |
| 2 | **Martin** (floor), **Anas** (press) | **Recall check** (checklist item 11; `methods_drafts.md` check 5): hand-read 30 turns and 30 releases, count how many named members the matcher finds | Precision is measured (98/100), recall is not. A missed name can never appear in a sample drawn from `mentions.parquet` | Sun 22 Nov (floor); with A3 (press) |
| 3 | **Group** | **Swing-seat definition** (G13, open point 2): lean ±5 on the district members **served** (`lean_2025`), with the checks in section 4 | The core comparison of part 3 rests on it, and 12 members change label on the 2026 map they ran in (9 more are unknown) | Before the first 20 are collected |
| 4 | **Group** | **Date window** and **leader list** (party leaders excluded from "naming the other side") | Needed before A4; fixed in writing before results | Sun 22 Nov |
| 5 | **Martin** | Yes or no to the **state null** ([`state_null/`](state_null/README.md)), one optional robustness row | Answers "members only know their own delegation"; the pilot says state explains almost none of the division | Sun 22 Nov |
| 6 | **Diego** | One sentence in part 2's limitations on matcher recall, once item 2 has a number | His codes measure precision; missed names never reach his sample | Draft, Tue 24 Nov |
| 7 | **Anas** | Tidy G13 in `DECISIONS.md` (draft headings "Edit 1/2" were pasted with it) | Cosmetic, but Martin reads that file daily | Any time |

## 2. Where I stand

| Done (in this folder) | In progress / next |
|---|---|
| Press-release scope, both parties (`press_scope/`), rechecked 19 Nov | **A1: built and tested; first 20 complete (G5 met); full collection running** (`collector/`) |
| Matcher checklist for Martin, 11 items (`MATCHER_CHECKLIST.md`) | A2 to A6 |
| Seats per state, exposure, redrawn states (`state_seats/`) | `docs/AI_METHODS.md` |
| Lean of the districts members served, 2026 districts run in, second lean measure, redraw dates (`district_lean/`) | Analysis plan for A4 (written while A1 runs) |
| Proposal and pilot for a state null (`state_null/`) | |
| Methods and limitation drafts, planned checks, data sources (`methods_drafts.md`) | |
| Glossary (`dictionary.md`) | |
| S1: second coding of D2 rows 76 to 100 (κ 0.69 with Diego) | |
| G13 pasted into `DECISIONS.md`, work plan log updated (19 Nov) | |

## 3. What we found since 18 Nov

### More and better sources for part 3

Wikipedia is used only for district context, and now each of its numbers has a second source:

| What | Main source | Second source / check |
|---|---|---|
| Lean of the district served | 2025 Cook PVI, Wikipedia revision of 25 May 2025 (pinned, before any redraw) | **The Downballot**, 2024 presidential margin on the 2024 district lines: r = 0.999 |
| District run in 2026 | `incumbents.csv` (2026 House elections page, snapshot 11 Nov) | Roster check: nobody joined or left since 11 Nov |
| Redraw dates | Wikipedia, one article per state with revision id | **Official pages or news, all nine agree:** California Secretary of State, Texas Senate Journal, NC Session Law 2025-95, Ohio Secretary of State, Utah court order, news for FL, TN, LA, AL |
| Press releases | Members' own `house.gov` sites; `robots.txt` allows release pages (checked on six sites) | Counts from the scope scan, a different method |

The rest of the project already rests on primary sources (govinfo bills and Congressional Record, Voteview,
`unitedstates/congress-legislators`). Full list for the Methods: `methods_drafts.md`, "Data sources".

### Redrawn states: served districts versus 2026 districts

- **Nine states redrew their maps for 2026** (AL, CA, FL, LA, NC, OH, TN, TX, UT): 173 seats, 40% of the
  House. In those states the 2026 lean describes a different area from the one the member represented.
  Steve Cohen's TN-9 is D+23 as he served it and R+9 on the 2026 map.
- **The 2026 lean in `districts.csv` cannot be joined to members by district number.** 7 members also ran in
  2026 under a different number (Bera served CA-6, ran in CA-3).
- **Fix:** [`district_lean/member_lean.csv`](district_lean/member_lean.csv), one row per member, joined on
  `bioguide`: the district served (`lean_2025`, `exposed_2025`), the 2026 district actually run in
  (`lean_2026_ran`, `exposed_2026`), the second lean measure (`pres_margin_2024`, `exposed_pres`), and `fate`.
- **Use the served district** for the main comparison: the releases were written for its voters.
- **What it changes:** 12 members get a different label in the district they ran in, 9 have no 2026 contest in
  our data. Under the old same-number join, safe Democrats like Cohen would have counted as exposed.
- **Map dates** ([`district_lean/redraw_dates.csv`](district_lean/redraw_dates.csv)): TX 29 Aug, NC 22 Oct,
  OH 31 Oct, CA 4 Nov, UT 10 Nov 2025; FL 4 May, TN 7 May, AL 11 May, LA 29 May 2026. Only the 2025 group
  leaves a usable "after" period for a before/after comparison.

### Collect everyone, not a sample

The "first 20" is the go/no-go test of the collector (G5), not the size of the analysis. Collecting all
**about 410 countable members** (56,747 releases, a few hours at a polite pace) means no sampling choices to
defend, every exposed member included (all 21 exposed members in the 2025-redraw states, for the before/after
check), and whole states for the leave-one-state-out check. Fallback if it is too slow or the file too big
for GitHub: all ~97 exposed members plus an equal number of safe members spread over states.

### The name matcher (affects all three parts)

- **"Who" and "what":** the exposed/safe groups are built from IDs and district numbers, so they are immune to
  naming errors. What we compare between the groups (how often a member names the other party) comes from the
  matcher, and so does the whole floor map and Diego's sample.
- **Six members are dropped whenever named by nickname** (tested on Martin's matcher, 20 Nov). Fix: nicknames
  from `legislators-current.json` as second first names (item 9).
- **State legislators** ("State Rep. Smith") would be counted as House members with the same surname (item 10).
- **Recall is unmeasured** (item 11 and check 5). No alias list is complete, so the paper reports the measured
  recall as a limitation.

### A1: the collector works (20 Nov)

Details in [`collector/README.md`](collector/README.md).

- **First 20 members (G5 test): all complete**, 2,118 releases. Every release has a date; where the date comes
  from page metadata it matches the listing page 399 of 399 times. Median 368 words; 0.7% under 60 words.
- **The scope scan overcounted some sites** (it counted dates on listing pages, and some sites show every date
  twice; checked by hand on Begich and Loudermilk). The collector's counts replace the scan's 56,747.
- **Eleven problems found and fixed in testing**, from duplicate URLs differing only in letter case to a site
  that moved to WordPress after 18 Nov (table in the README).
- **Full collection of every countable member started 20 Nov, about 01:15**, four sites in parallel, 0.5 s per
  site between requests, `robots.txt` followed. About 3 hours. Interrupted or failed members are retried with
  `--skip-done`.
- **Not collected:** Budzinski, Gottheimer, Gluesenkamp Perez, Morrison (listings load only with JavaScript);
  the 12 who left office; Jordan (listing ends in 2024).
- **The A4 analysis plan is written** (`methods_drafts.md`) before any release has been analysed: outcome,
  groups, permutation test, and how each result will be read.

## 4. Proposed revisions, part by part

### Part 1: the two maps (Martin)

- **Proposed:** matcher items 9, 1, 2, 10 and the floor recall check (priority 1 and 2). Optional: the state
  null as one robustness row.
- **Why:** the floor map is built entirely from matcher output. Same-state ties are over-represented (floor
  9.0% against 3.7% by chance), but the pilot finds they explain almost none of the party division (Q about
  0.005 under the state null, against 0.111 and 0.210).
- **Not proposed:** exposure in part 1. It could matter there too, but it would be a new question after seeing
  results, on six pages.
- **Unchanged:** M1 to M8; G1a to G1c, G12; the plain and debate nulls; Figure 1; the slides.

### Part 2: what a mention means (Diego)

- **Proposed:** one limitation sentence on recall once the floor recall check has a number.
- **Why:** hand codes catch wrong matches (code X), not missed ones. Splitting 75 cross-party rows by exposure or
  state would leave groups too small to say anything, so nothing else changes.
- **Unchanged:** D1 to D5, the protocol, κ, the D5 decision, the drafts.

### Part 3: the close-up (Anas)

Half a page and Figure 3. The two maps stay the headline. G5 still applies.

| Task | Before | Now | Why |
|---|---|---|---|
| **A1** Collector | Keep full text and date | Same five columns plus provenance (`listing_date`, `date_source`, `layout`, `n_words`, `fetched_at`). Builds on the scope scan's pagers and the WordPress API. Follows each site's `robots.txt`. Logs failed fetches instead of storing empty rows. Keeps raw pages. Flags item type (release, statement, op-ed), a text fingerprint for releases posted by several members, and each member's first and last release | Scope scan; sites may change when members leave in January; duplicates across co-leads; members who served part of the term |
| **A2** Collection | First 20 Republicans, then about 60 | **First 20 as the test** (both parties, all four layouts, both redraw groups), **then everyone countable**, about 410 | Collect everyone (section 3) |
| **A3** Release to bill, names | Bill number; co-lead or not | Plus **same state**, **party of the named member**, flags for **caucus releases** (e.g. Problem Solvers) and **releases about redistricting**; **recall check** on 30 releases | Matcher items 1, 2, 9, 10; caucus lists name members by membership, not choice |
| **A4** Figure 3, text | Which Democrats Republicans name | Share of each member's releases naming the other party (not a co-lead, not a party leader), **exposed against safe within each party**, then compared between parties. **Permutation test** (shuffle exposed/safe labels within each party). Panel B: named showcase ties and mutual pairs | Parties differ in posting rates and majority status, so only within-party gaps are compared |
| **A5** "Bipartisan" | Optional | Still optional: a short list of partnership phrases per release (week 7 word-list method) | |
| **A6** Methods, AI file, download | Data paragraph, `docs/AI_METHODS.md`, download Mon 23 Nov | Drafts in [`methods_drafts.md`](methods_drafts.md): served map and why, second lean source, data sources table, planned checks | |

**Checks fixed before any results** (`methods_drafts.md`): (1) without the 21 members whose 2026 label differs
or is unknown; (2) without releases about redistricting; (3) optional before/after the new map, 2025 group
only; (4) cut-off ±4 and ±6, or lean as a number; (5) matcher recall on 30 releases. Plus: without caucus
releases, and leave one state out.

**Unchanged in part 3:** the question (whom members show at home); the shared columns of
`press_releases.parquet` and `mentions.parquet` (`source = press`); Martin's matcher as the one name finder;
M6, the null on members' own bills (Martin); the four named examples to check (Roy–Cohen, Biggs–Jayapal,
Lawler, Bacon); the page budget.

## 5. Next steps (Anas)

1. Finish the full collection (rerun with `--skip-done` if it stopped), run `check.py` on everyone, and explain
   the three members 10 to 14% below the scan (Menefee, Crenshaw, Castro).
2. Audit the text where a generic container was used (`body_selector` = `main`, `article`, `#main_column`) and
   whether WordPress listings pick up sidebar posts from other categories.
3. Split `press_releases.parquet` under 25 MB per file (by party or state) and add it to this folder.
4. A3: party-leader list, matcher on the press text (with nicknames if item 9 is not done), release-to-bill
   matching, caucus and redistricting flags, recall check on 30 releases.
5. A4 by the draft on Tue 24 Nov.

## 6. Files in this folder

See [`README.md`](README.md).
