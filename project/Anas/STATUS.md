# Anas: status, findings and proposals

> **22 Nov, added by Diego (with Claude) with the group's agreement:** `AI_METHODS.md` (part of A6) has moved to
> `Diego/AI_METHODS.md`, so Anas does not need to spend time on it. Additions welcome there.

Anas, Friday 20 November 2026 (last updated **Sun 22 Nov, early morning: A3 complete, A4 first run and the home-map
network extension**; section 3, [`a3/README.md`](a3/README.md), [`a4/README.md`](a4/README.md)). **Start here.** This
replaces `REVISIONS_19NOV.md` and is kept up to date.
**Proposals, not decisions:** parts 1 and 2 belong to Martin and Diego, who decide on anything in them. Agreed
changes go into `DECISIONS.md` before the freeze on Sun 22 Nov (G7).

## 0. Martin and Diego: what is proposed for your parts, on one page

Everything below is a proposal; you decide for your own part. Agreed items go into `DECISIONS.md` before the
freeze on **Sun 22 Nov**. Details: section 1 (order), section 4 (per part), `MATCHER_CHECKLIST.md` (matcher).

**Why bother with these at all.** On DTU's scale a 12 is the excellent performance with *no or only a few minor
weaknesses*. Our headline (two maps, one more divided than the other) is already in place; what separates a 10 from a
12 is whether an examiner can find a weakness we did not see first. Each row closes one such weakness, and most cost
an hour. A limitation we measured and report is a strength; one an examiner finds is a deduction.

| # | Extension | Part | What it takes | If we do it | If we don't | Status |
|---|---|---|---|---|---|---|
| 1 | **Redrawn states** (9 states, 173 seats): exposure measured on the district members **served** (`lean_2025`), plus a check without the 21 members whose label changes | 3, Methods | Done (Anas) | Exposure means what members faced while they wrote | "Exposed" partly reflects a map drawn after the releases | You know this one |
| 2 | **State null** (shuffle ties within states) as one robustness row | 1 | Yes or no from Martin; pilot ready (`state_null/`) | Answers "members only know their own delegation": state explains almost none of the division | An examiner can say the division is just geography | You know this one |
| 3 | **Measured recall of the matcher.** Not a second matcher: the same one, checked for what it *misses*. Hand-read 30 floor turns (Martin) and 30 press releases (Anas), list every member named in any form, count how many the matcher finds | 1, 2, 3 | About an hour each; floor by Sun 22 Nov | Methods states: *"The matcher found x% of named members in 30 floor turns and y% in 30 releases"*, with the forms it missed | Our precision (98/100, Diego's D2) says nothing about missed names: a sample drawn from `mentions.parquet` can never contain a name the matcher missed. Every count in all three parts would rest on an unmeasured number | **New: please read.** Press precision measured 20 Nov (section 3); press recall next (A3.4) |
| 4 | **Matcher fixes** that raise recall: nicknames (item 9: Hank Johnson, Bobby Scott, Chris Smith, Buddy Carter, Hal Rogers, Chuy García are dropped whenever named so), name lists (1), untitled full names (2), state legislators (10) | 1 (and so 2, 3) | Martin, `MATCHER_CHECKLIST.md`, by Sun 22 Nov | Recall (row 3) goes up before it is measured; six members stop disappearing | Six members are systematically under-counted on the floor map | **Done 20 Nov (G14)**: 9, 1, 10 applied; 2 waits for a 30-row check. A3 switched to this matcher 21 Nov |
| 5 | **One recall sentence in part 2's limitations** | 2 | Diego, one sentence once row 3 has a number | Part 2 says plainly what hand codes can and cannot catch (wrong matches yes, missed names no) | The obvious examiner question about part 2 goes unanswered | Waiting for row 3 |
| 6 | **Date window and leader list** fixed in writing before results | All | Group, Sun 22 Nov | Results cannot be accused of a window chosen after seeing them | Same | Open |
| 7 | **Press data snapshot: 20 Nov 2026** (55,023 releases, 412 members; `press_releases/MANIFEST.md`) | 3, and the window in row 6 | Window must end on or before 20 Nov | All three parts cover the same days | Press and floor would cover different periods | Decided by Anas 20 Nov |
| 8 | **One confusion table for the matcher** in Methods: TP, FP, FN, precision, recall, F1 per source (floor, press) | 1, 2, 3, Methods | Nothing extra: filled from D2 (precision), Martin's 30 turns and Anas's checks (recall); template in [`A3_PLAN.md`](A3_PLAN.md) section 8 | The matcher's quality in one place, measured cell by cell; one sentence explains why accuracy is left out (no meaningful true negatives) | Precision and recall stay scattered, and an examiner may ask why there is no accuracy | **New**, Anas |
| 9 | **Four more matcher items, 21 Nov** ([`MATCHER_CHECKLIST.md`](MATCHER_CHECKLIST.md) items 12 to 15): **12, possessives are never matched** ("Mr. Cole’s amendment"); **15, a middle initial makes the first name the surname** ("Congressman Riley M. Moore" → Josh Riley; 4 floor hits, 364 press mentions); 13, "Washington" the city counts as the state; 14, no guard on untitled names after "Sen." or "Governor" | 1 (and so 2, 3) | Item 12: a few lines in `matcher.py` and a rerun, by Sun 22 Nov. Items 13 and 14: nothing, only know them | Item 12 adds about 417 floor mentions (4.8%, 33.6% cross-party), so the headline should barely move. Items 13 and 14 have answers ready if asked | Item 12 becomes one Methods sentence. Items 13 and 14 affect 2 floor mentions and none, so they are harmless | **New: please read item 12**, Martin |

**Rows 3, 4, 5, 8 and 9 belong together:** the fixes (4) raise recall, the check (3) measures what remains, the
sentence (5) reports it for part 2, and the confusion table (8) puts precision and recall for floor and press in one
place. No alias list is ever complete, so the goal is not 100%; it is a number we stand behind.

**A lesson from the press collection that applies to the floor data too** (collector README): our first collector
reported members as *complete* that held 10 of 709 releases (Jeffries) or 14 of 107 (Latta). Only an outside count
caught it (the WordPress API, the dates the walk reached). "The code finished without errors" is not evidence that
the data is complete; a count from an independent source is.

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
| Press-release scope, both parties (`press_scope/`), rechecked 19 Nov | **A1 and A2 done (20 Nov): 55,023 releases from 412 members**, in `press_releases/` (3 parts, read `MANIFEST.md`) |
| Matcher checklist for Martin, 11 items (`MATCHER_CHECKLIST.md`) | **A3.0 to A3.3 done (20 Nov)**, scripts in `a3/`, plan in `A3_PLAN.md`. Next: A3.4 recall (by Sun 22 Nov), A3.5 to A3.7 (Mon 23 Nov), then A4 to A6 |
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
- **Full collection done (20 Nov): 55,023 releases from 412 of 413 countable members**, dated 3 Jan 2025 to 20 Nov
  2026, in [`press_releases/`](press_releases/MANIFEST.md): three files under GitHub's 25 MB limit, split by member
  (every member in one file), checked to add up exactly to the whole. 100% dated; median 351 words.
- **Audited before it was accepted.** Every fix was tested against the cached pages of all members (old and new
  rules side by side), and the final table comes from one run of the final code; a second full run 15 minutes
  later gave the same rows. The audit found members the first version had cut short while reporting them
  complete: **Jeffries 10 of 709, Goodlander 15 of 360, Latta 14 of 107**, and none at all for Radewagen, DeGette,
  Keating, Crow, Scalise, Hudson, Cole, Brownley, Clarke and Amo; plus 37 releases silently missed on 13 more
  members (Fischbach 8, LaHood 5, Crenshaw, McClain and Stefanik 4 each, ...), 14 Espaillat releases from 2024
  wrongly kept, and release text deleted or cut in 19 releases (12 members). All fixed (table in the collector
  README).
- **Independent check against the WordPress API** (37 members whose sites expose it): 26 equal; every other
  difference explained (posts with no text, a 3 Jan time-zone edge, Carey's releases filed under another
  category).
- **The scope scan's counts are estimates, not the truth.** It counted dates on listing pages, and many sites
  show two per release (Womack, Loudermilk, Foushee, Mace). For each of the 38 members more than 15% below the scan,
  the collector holds what the listing holds and reaches back to January 2025 (or the member started later).
- **Not collected:** Budzinski, Gottheimer, Gluesenkamp Perez (listings load only with JavaScript), Morrison
  (listing answers "410 Gone", only her 20 newest releases are shown); the 12 who left office; Jordan (listing
  ends in 2024). Known gaps inside the data: 28 posts with no text of their own (image or video), 3 dead links on
  the sites (Wittman 1, Goodlander 2), 1 Goodlander release filed under "in the news".
- **For A3:** some freshman sites carry House-wide template posts ("Newest Members of Congress") that name dozens
  of members, and many members repeat a bio or press-contact paragraph in most releases (`check.py`, section 5).
  The matcher should not count these as mentions.
- **The A4 analysis plan is written** (`methods_drafts.md`) before any release has been analysed: outcome,
  groups, permutation test, and how each result will be read.

### A3: switched to Martin's 20 Nov matcher (21 Nov)

Plan, reasons and two deviations: [`A3_MATCHER_SWITCH.md`](A3_MATCHER_SWITCH.md). Numbers: [`a3/README.md`](a3/README.md).

- **One matcher for floor and press (G14).** Martin's code is unchanged. Press differs from the floor only in
  input and in a thin layer:
  - **Input:** untitled names on, plus the first names members use for themselves.
  - **Layer:** party-state tags, own surname, title guards, lists that carry tags, quoted nicknames, middle initials.
- **`shared` (exactly as on the floor):** 51,569 mentions once per release, 24.1% cross-party.
  **`shared + press layer` (for A4):** 129,052 mentions, 14.4%, with the middle-initial rule (20 Nov: 123,147, 15.1%).
- **Against 20 Nov:** 123,013 (release, member) pairs are in both, 134 are only in the old version, and 5,983
  are only in the new one.
  - 17 hits name a different member at the same place, and the new version is right in all 17.
  - 12 of the 17 were errors in the 20 Nov list rule that its 30-row sample did not catch.
- **Precision:** the 180 rows read on 20 Nov carry over (120 counted rows: 119 y, 1 ?, 0 n).
  - **The 30-row switch sheet** (`a3/precision_check/switch_sheet.xlsx`) **was left unread, by decision of Anas on
    21 Nov.**
  - **Reason:** the A3.4 recall check measures the switched version's precision end to end, at 0.96 on 78 hits
    that include the new forms. The automatic tag check agrees 99.5% for untitled names.
  - The sheet is kept, so it can still be read.
- **A3.4 recall, done 21 Nov, with five blind AI readers instead of Anas's own reading** (`a3/README.md`, A3.4):
  - **Sample:** 30 releases from the surname pool and 10 from outside it.
  - **Agreement:** all five readers agree on all 77 pairs, and the 10 outside releases name nobody.
  - **Press recall:** 0.73 (0.62–0.81) for Martin's matcher as used on the floor, and **0.97 (0.91–0.99) with the
    press layer**. Precision in the same sample is 0.93 and 0.96.
  - **Found by it:** a middle-initial bug. "Congressman Riley M. Moore" was counted as Josh Riley, giving 364 false
    press mentions, 96% of them cross-party. It is `MATCHER_CHECKLIST.md` item 15 for Martin.
  - **Corrected in the press layer the same evening** (the "middle initial" rule). Only 3 such hits are left,
    against 449 before.
  - **Human check, done 21 Nov:** Anas read the 7 reader–matcher differences (`a3/recall_check/DIFFERENCES.md`) and
    agreed with the readers on all 7, so the numbers stand.
- **A3.5 bills and co-leads, done 21 Nov** (`a3/README.md`, A3.5; output `a3/out/release_bills.csv`):
  - **Links:** 18,177 bill links in 13,944 releases (25%), 8,600 found by bill number and 9,577 by exact title.
    Decision 7 is met: titles add 15.3 points.
  - **Each link carries** the bill's sponsor and the releasing member's role on it.
  - **Precision check by 3 blind AI readers:** 30 of 30 numbers and 30 of 30 titles, unanimous, so nothing needed
    a human look.
  - **For Martin:** this is the table M6 needs.
- **A3.6 and A3.7, done 21 Nov** (`a3/README.md`; output **`a3/out/mentions_press.parquet`**, 129,052 rows, the file
  A4 reads):
  - **Flags and weights** from the plan, with the leader list and word lists fixed before A4 (`a3/leaders.csv`,
    `a3/flags.py`).
  - **Weights matter:** 14.4% of press mentions cross party, and 33.0% weighted by 1/n.
  - **Named examples:** all three mutual pairs hold, in both directions. The pilot's Lawler figure (1 of 10) and
    Bacon figure (8 of 10) do not: on all their releases, 19.8% and 32.5%.
  - **A3 is complete.**
- **A4 first run, done 21 Nov** (`a4/README.md`, Figure 3 draft `a4/out/figure3_draft.png`):
  - **Result:** exposed members name the other party more at home in **both** parties. Republicans 13.2% against
    9.2% (+4.0 points, p 0.004); Democrats 11.5% against 8.9% (+2.6, p 0.003). The interaction is +1.4 (p 0.40).
  - **Reading fixed in advance:** a seat effect, not a president's-party effect.
  - **Robustness:** it holds in every row, including the cut-offs at 4 and 6, the second lean source, leaving one
    state out, and Martin's matcher alone.
  - **All members by district lean** (Figure 3A now): the share peaks in the closest and crossover seats and is
    nearly flat beyond them.
  - **Extension, the home network** (`a4/HOME_NETWORK_PLAN.md`, fixed before computing; **for Martin and Diego to
    accept under G17**):
    - **Hubs:** exposed members are the hubs of cross-party naming. They are 22% of members but send 35% and
      receive 34% of cross-party ties.
    - **Only a small preference for each other beyond that activity:** 10.8% of ties join two exposed members,
      against 10.3% under a degree-preserving rewiring (+5%, p 0.025).
    - **One bipartisan community of close-seat members:** Louvain finds 37 members, half of them exposed (Bacon,
      Golden, Kaptur, LaLota, Gillen and others). The other mixed communities are state delegations.
    - **Centrality, Holm-corrected:** exposed members have far more cross-party ties in both parties. The party
      difference in how they bridge does not survive the correction.
    - **Everything is documented in `a4/NETWORK_METHODS.md`:** values, formulas and steps, with the configuration
      model as the null (not Watts–Strogatz).
    - **Mutual ties:** ties between exposed members are more often mutual (62% against 45%). This is suggestive only;
      it fades in the robustness rows.
    - **Not local:** safe members' cross-party ties are no more same-state than exposed members' (about 11% each).
    - **Three corrections, all written into the plan and README:** the planned null does not rule out the hub effect;
      the post hoc quintile check was too coarse to remove it; and the tie-end shortcut overstated the null, so its
      "no preference" is replaced by the degree-preserving rewiring's +5%.
  - **Settings (Anas's choice, `G13_UPDATE.md`, for Martin and Diego to agree to by Sun 22 Nov):** swing seat =
    `exposed_2025` (lean within 5 of the member's own party, on the district served); window = 3 Jan 2025 to
    20 Nov 2026.
- **For Martin (error notes, not scope):**
  - His "state nearby" rule reads "Washington" the city as the state: up to 6 press hits to Adam Smith, and 2 on
    the floor (one passage, apparently about the film).
  - His untitled option has no guard after "Sen." or "Gov.": 11 press hits in 81,950, some of them correct anyway;
    it is off for the floor.
  - **Possessives are never matched:** "Mr. Cole’s amendment" gives no hit. One run with the possessive blanked out
    gives **+417 floor mentions** (4.8%, 33.6% cross-party) and +1,275 titled press hits. Not hand-checked. The
    largest of the three; the fix belongs in his matcher, so floor and press stay one matcher.
  - All three are written up for Martin as `MATCHER_CHECKLIST.md` items 12 to 14 (section 0, row 9).

### A3: from press releases to named colleagues (20 Nov; replaced by the switch above, kept as the record)

Plan, decisions and traps: [`A3_PLAN.md`](A3_PLAN.md). Scripts and full numbers: [`a3/README.md`](a3/README.md).
Martin's matcher is used unchanged; everything A3 adds is a separate layer, so both versions stay visible.

- **Inputs frozen** (A3.0): the three press files, `members.csv` and Martin's matcher at repo commit `75c67ae`,
  by SHA-256. Every later step stops if any of them changes, so no result mixes two versions. Rerunning A3.0 to
  A3.3 takes about two minutes.
- **Shared matcher on the press text** (A3.2): 38,557 colleague mentions (once per release) in 18,308 releases;
  29.4% cross-party. Two thirds of all hits are members naming themselves.
- **Press layer** (A3.3) recovers what the matcher's title rule cannot see in releases: untitled full names,
  name lists after "Reps.", nicknames (Hal Rogers, Chris Smith, Don Davis), party-state tags ("Rep. Smith
  (R-NE)"), plus a guard for state legislators. Mentions rise to 123,147.
- **Precision, every rule at or above 95%.** 30 random hits per rule, read by Anas and by three blind LLM readers
  that saw only the excerpt and the member list. The three agreed on all 180 rows and with Anas's resolved reading
  on 179. Every adding rule 30/30; the state-legislator guard 28/29 after a fix the reading found (a lowercase
  verb, "reports further state Rep. Omar"). Limits and the two versions of the table: `a3/README.md`.
- **New finding, signatory lists:** releases naming 10 or more colleagues are 12% of releases naming anyone but
  hold 63% of mentions (6.9% cross-party). **Decision 8:** each colleague in a release gets weight 1/n, so every
  release counts once in tie counts; plain counts from releases naming fewer than 10 as the robustness row.
- **Next:** A3.4 recall on 30 hand-read releases (design question open: draw from releases containing any House
  surname, so the sample does not depend on what the matcher found); A3.5 bills and co-leads; A3.6 flags;
  A3.7 the press-mention file and the named examples.

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

1. ~~Finish the full collection, check, split~~ Done 20 Nov (`press_releases/`). **Snapshot: 20 Nov 2026** (decided
   20 Nov; needs the date window frozen on Sun 22 Nov to end on or before 20 Nov). A later update only if
   something changes or a missed problem turns up: then the whole collector is rerun (about 15 minutes, release
   pages come from the cache), never patched by hand, and the date and reason are logged in `collector/README.md`
   and here.
2. Audit the text where a generic container was used (`body_selector` = `main`, `article`, `#main_column`).
3. ~~A3.0 to A3.7~~ **Done 20 to 21 Nov**, on Martin's 20 Nov matcher (switch 21 Nov). Rerun everything in about
   two minutes if Martin fixes items 12 and 15 (`a3/README.md`, "If Martin's matcher changes").
4. **A4: first run done 21 Nov** (`a4/README.md`). Left:
   - the group's agreement on the swing seat and the window (`G13_UPDATE.md`, Sun 22 Nov);
   - the group's answer on the network extension under G17;
   - a better network figure (the current one is a draft; see the handoff);
   - deciding how the extension's measures (centrality, communities, null model) enter the paper: figure, table or
     text;
   - the part 3 Results text for the Overleaf draft, Tue 24 Nov 20:00.
5. **A6:** Methods and `docs/AI_METHODS.md`. The AI file has to record:
   - the blind AI readers used in A3.3, A3.4 and A3.5, and Anas's checks of their disagreements;
   - Claude's resolutions;
   - that Claude wrote the code.
6. **Confirm G17 in the group chat,** saying that the pre-registered checks count as listed tasks.

## 6. Files in this folder

See [`README.md`](README.md).
