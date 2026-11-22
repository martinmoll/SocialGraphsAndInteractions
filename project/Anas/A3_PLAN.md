# A3: from press releases to named colleagues and bills (plan)

Anas, 20 Nov 2026. **Plan approved 20 Nov**; nothing has been run on the full data yet. Section 6 holds the seven
decisions fixed before any result is seen (A4 analysis plan: `methods_drafts.md`). Two numberings: **steps** are
A3.0 to A3.7 (section 5); **sections** are 1 to 7 of this document.

## 1. What A3 delivers

| Output | One row per | Columns | Used by |
|---|---|---|---|
| `mentions_press.parquet` | one colleague named in one release | the shared `mentions.parquet` columns (`speaker`, `named`, `source = press`, `date`, `doc_id` = release URL, `context`, `is_yield` = False) plus `how` (matcher rule), `rule_set` (`shared` or `press extension`), and the flags in step 6 | A4 (Figure 3), M6 (Martin's null) |
| `release_bills.csv` | one bill cited in one release | `url`, `bill_id` (e.g. `hr1234-119`), how it was found, sponsor, whether the releasing member is sponsor or original cosponsor | A3 co-lead flag, M6 |
| `recall_check/` | 30 releases | Anas's hand list of every member named, the matcher's hits, recall with a 95% interval, the forms missed | Methods (STATUS section 0, row 3) |
| `confusion_table.md` | one source and rule set | TP, FP, FN, precision, recall, F1 with 95% intervals (section 8); filled in as each check is done | Methods: one table for all three parts |

## 2. What the data looks like (measured 20 Nov on the 55,023 releases)

- **One release in three names another member** (2,000 releases sampled; Martin's matcher as it is). Two thirds of
  all matcher hits are members naming **themselves**: these are not mentions and are removed, as on the floor.
- **Party-state tags are common:** 23.5% of releases write names as "Reps. Smith (R-TX) and Jones (D-CA)". This is
  where the matcher misses names in lists (checklist item 1), and the tag gives the state, which settles shared
  surnames.
- **Bill numbers are rare:** 11.5% of releases cite one (`H.R. 1234`, `H.Res. 56`). Many name the bill instead
  ("the Laken Riley Act"); how many can be matched by title is measured in step 5 before it is used.
- **Shared texts are few:** 80 texts appear under two or more members, 3 under five or more (largest: "119th
  United States Congress Convenes", 34 members, a House-wide template that names dozens of members).
- **Names in capitals in the body are rare** (0.5% of releases); the matcher drops them on purpose (its change B).
- **Senators appear in 10% of releases.** A senator who shares a surname with a House member ("Sen. Collins")
  must not become a House mention (checklist; matcher's planned guard).

## 3. Principles

1. **One matcher.** Martin's `matcher.py` is used unchanged as the baseline (`rule_set = shared`). Press-specific
   rules are added in a separate layer in `Anas/` and every hit says which rule found it, so the baseline result
   can always be shown on its own. If Martin adopts checklist items 1, 2, 9, 10, the layer shrinks to what is
   left. **Done 21 Nov** (G14; [`A3_MATCHER_SWITCH.md`](A3_MATCHER_SWITCH.md)): his 20 Nov matcher, code unchanged,
   with press input (untitled names, members' own first names) and a thin layer.
2. **Measure before trusting.** Every rule is checked on a sample before it is used on all releases, as in the
   collector audit (README): precision on hits, recall on hand-read releases.
3. **Fixed before results.** Leader list, flags, cut-offs and exclusions are written down (section 6) before
   A4 compares any groups.
4. **Nothing is deleted.** Excluded hits (self-mentions, template posts, boilerplate, senators) stay in the file
   with a reason, so every count can be rebuilt with a different choice.

## 4. Traps known now, and the guard for each

| Trap | Example | Guard |
|---|---|---|
| Members naming themselves | 66% of hits | `named == speaker` dropped (reason kept) |
| House-wide template posts | "Newest Members of Congress", 34 members | Same text (`text_sha1`) under 5 or more members (decision 4): flagged `template`, not counted |
| Repeated paragraphs | Cleaver's bio in 99% of his releases; press contacts | Sentences of 6 or more words in 30% or more of the releases of a member with at least 10 releases (decision 5, exactly as `check.py` section 5): a hit inside one is flagged `in_boilerplate`, not counted |
| Joint releases | 80 texts under 2 or more members | Kept for each member (each chose to post it); flagged `shared_text` for a robustness check |
| Senators with a House surname | "Sen. Collins (R-ME)" | A name after "Sen." or "Senator", or tagged with a state whose House member of that surname does not exist, is not a House mention |
| State legislators | "State Rep. Smith" | "State Rep.", "Assemblyman", "State Senator" before the name: not a House mention (checklist item 10) |
| Party leaders | Speaker Johnson, Leader Jeffries | Named by role, not as a partner: the leader list (section 6) is excluded from "naming the other side" in A4 |
| Caucus releases | Problem Solvers lists | Flag `caucus` (list of caucus names, fixed in advance); a robustness check without them |
| Releases about redistricting | the 2025 maps | Flag `redistricting` (word list fixed in advance); check 2 in `methods_drafts.md` |
| Dates outside the term window | none expected | Window applied as frozen on Sun 22 Nov; snapshot ends 20 Nov |
| Undated releases | 2 of 55,023 | Left out of anything dated |

## 5. Steps

| Step | What | Check before going on | When |
|---|---|---|---|
| **A3.0** | Freeze inputs: the 20 Nov snapshot, `members.csv`, the commit of `Martin/matcher.py` used | Hashes written into the output folder | Sat 21 Nov |
| **A3.1** | Prepare text for matching: mark template posts and repeated paragraphs (section 4) | Read 10 flagged and 10 unflagged by hand | Sat 21 Nov |
| **A3.2** | Run the shared matcher on all releases: `rule_set = shared` | Its self-check passes; hit counts per rule against the 2,000-release sample above | Sat 21 Nov |
| **A3.3** | Press layer: (a) "Surname (R-ST)" tags, (b) name lists after "Reps.", (c) untitled full names, (d) nicknames (checklist 9), (e) senator and state-legislator guards | **Precision:** 30 hits per new rule read by hand; a rule under 95% is dropped or narrowed | Sat 21 to Sun 22 Nov |
| **A3.4** | **Recall check:** ~~30 releases drawn at random (seed 2805) from releases that name anyone other than the member~~ **Changed 21 Nov (Anas):** 30 from releases containing another member's surname by plain string search (31,094), plus 10 from all other releases as a check that this pool loses nobody, shuffled together, seed 2805 (`a3/README.md`, A3.4). Choosing releases with the matcher would have biased recall upward. Anas reads each **without seeing the matcher's hits** and lists every House member named, in any form; then the script compares | Recall with a 95% interval, for `shared` alone and `shared + press layer`, and the forms still missed. This is the number for Methods | Sun 22 Nov |
| **A3.5** | Bills: find bill numbers; resolve them in `bills.parquet` (119th Congress); mark whether the releasing member and each named colleague is sponsor or original cosponsor (`cosponsors.parquet`). Measure how many releases name a bill only by title before deciding to match titles | 30 resolved bills checked by hand | Mon 23 Nov |
| **A3.6** | Flags on every mention: `same_state`, `named_party`, `cross_party`, `named_is_leader`, `co_lead`, `first_named`, `in_list`, `caucus`, `redistricting`, `template`, `shared_text`, `item_type`, `listed`; tie weight `weight` = 1/n and `n_named` (decision 8) | Counts per flag; any flag above 30% of rows is read again | Mon 23 Nov |
| **A3.7** | Write `mentions_press.parquet` and `release_bills.csv`, README with every choice and count | The four named examples (Roy–Cohen, Biggs–Jayapal, Lawler, Bacon) and the pilot's mutual pairs (Golden–Lawler, Golden–Fitzpatrick, Kaptur–Fitzpatrick) read against the new file | Mon 23 Nov, ready for A4 on Tue 24 Nov |

Who reads by hand: the recall check (A3.4) and the precision samples (A3.3) are read by Anas. Claude prepares the
samples and the sheets and scores them, but does not label them, so the numbers are a human check of the machine
(stated in `docs/AI_METHODS.md`).

## 6. Decisions fixed before results (approved by Anas, 20 Nov)

Not to be confused with step A3.6: these eight decisions steer different steps of section 5, and are grouped here
because all must be fixed before Sun 22 Nov (G7), before any group is compared.

| # | Decision | Steers step | What was decided | Why |
|---|---|---|---|---|
| 1 | **Unit of a press mention** | A3.2, A3.7, A4 | A colleague named **at least once** in a release counts once (not per occurrence) | A release that names a partner five times is still one showing; occurrences depend on writing style |
| 2 | **Leader list** | A3.6 | Speaker, Majority and Minority Leader, the two Whips, the two conference/caucus chairs, as of the snapshot | They are named for their role; "naming the other side" in A4 is about partners |
| 3 | **Press layer used in A4** | A3.3 | `shared + press layer` if every new rule passes 95% precision in A3.3; `shared` alone reported as a robustness row. **Since 21 Nov:** `shared` = Martin's matcher exactly as the floor runs it; `shared + press layer` = the same matcher with press input and the thin layer (`A3_MATCHER_SWITCH.md`); the bar now also covers the 30 rows new after the switch | Recall rises without giving up precision; both versions stay visible |
| 4 | **Template threshold** | A3.1 | Same text under 5 or more members | Joint releases of 2 to 4 co-leads are real partnerships; 34 copies of "119th Congress Convenes" are not |
| 5 | **Repeated-paragraph threshold** | A3.1 | Sentences in 30% or more of a member's releases | The level `check.py` already reports; bios and contact lines sit at 35 to 99% |
| 6 | **Caucus and redistricting word lists** | A3.6 | Written down before matching (Problem Solvers, Blue Dog, Freedom Caucus, ...; "redistricting", "new map", "special session", ...) | Fixed before results |
| 7 | **Bill titles** | A3.5 | Matched only if A3.5 shows titles add more than 5 percentage points of releases with a bill, at 95% precision. **Met 21 Nov:** exact titles add 15.3 points; 30 of 30 read right by 3 blind readers. Titles are used | Numbers are unambiguous; titles are not |
| 8 | **Tie weight** (added 20 Nov, after A3.3 found signatory lists: releases naming 10 or more colleagues are 12% of releases naming anyone but hold 63% of mentions, 6.9% cross-party) | A3.6, A4 panel B, any press network | **Fractional:** each counted colleague in a release gets weight 1/n, n = colleagues counted in that release (after self, template and repeated-paragraph exclusions), so every release has total weight 1. **Robustness row:** plain counts from releases naming fewer than 10 colleagues | No free threshold; the same principle as PageRank's 1/k_out and Newman's collaboration weights. Affects ties only: A4's main outcome is per release already. Known assumption: every name in a release gets equal attention (see section 9) |

## 7. What happens if a step fails

- **Recall below about 80%** on the shared matcher: report it, use the press layer if it lifts recall, and say
  in Methods which forms are still missed. The A4 comparison (exposed against safe within a party) is robust to
  a recall that is the same in both groups; check 5 tests whether it is.
- **Martin changes the matcher after Sun 22 Nov:** rerun A3.2 to A3.7 (they are scripts, about 15 minutes) and
  state the matcher commit in Methods.
- **No time for A3.5:** A4 runs without the co-lead flag and says so; M6 is then dropped (WORK_AND_DEADLINES).

## 8. The matcher's confusion table (all three parts)

Precision, recall and F1 all come from a confusion matrix; the project already reports one for Diego's D5
classifier. For the matcher it has **no true-negative cell**: a "true negative" would be every member not named
and not found in a text, about 430 per release, so accuracy, (TP + TN) / all, would be near 100% even for a poor
matcher. As in named-entity recognition (week 7), we report precision, recall and F1, and say why accuracy is left
out.

| Source | Rule set | TP | FP | FN | Precision | Recall | F1 | Where the numbers come from |
|---|---|---|---|---|---|---|---|---|
| Floor | shared | | | | 98/100 (D2) | | | Precision: Diego's D2 (code X = wrong match). Recall: Martin's 30 hand-read turns (checklist 11) |
| Press | shared | | | | | | | A3.3 precision sample, A3.4 recall check |
| Press | shared + press layer | | | | | | | Same samples, scored with the layer |

Each cell is measured where it can be: **precision** from samples of the matcher's hits (TP against FP), **recall**
only from hand-read texts (TP against FN), because a missed name never appears among the hits. The table is
filled in as each check is done; empty cells are reported as not measured, never guessed. Intervals: Wilson 95%.

Optional (appendix or repo): a member-by-member table for shared surnames (Al Green and Mark Green, the Scotts,
the Johnsons): which member a hit was given to against the member really named. It shows who is confused with
whom, where a single precision number cannot.

## 9. Are all names in a release equally important? (decision 8's assumption)

Fractional weights give every colleague in a release the same share, 1/n. Some names matter more: the co-lead of
the bill, the first name, "special thanks to Rep. X", a leader named for their role. **Decision: record these roles
as flags, not as weights.**

- **Why not weights.** Any importance weight (say 2 for a co-lead, 1.5 for a thanks) is a number we would have to
  invent, which brings back the free parameter decision 8 removed, and an examiner can ask "why 2?". Reading
  "special thanks" reliably is a coding task (Diego's D2 needed a protocol, two coders and κ); a word list would
  miss most of it and add errors of its own.
- **What the flags give instead** (A3.6): `co_lead` (sponsor or original cosponsor of a bill in the release, from
  `cosponsors.parquet`, measured, not guessed), `named_is_leader` (decision 2), `first_named` (first colleague
  named in the release), `in_list` (found inside a list of names). A4 can then say, for example, what share of
  cross-party names are co-leads, without changing any weight.
- **The same assumption as PageRank:** a node splits its vote equally over its out-links, although links differ in
  importance. Weighted versions exist, but only where the weights are measured, not assumed.
- **Limitation in Methods (one sentence):** "Tie weights treat every colleague named in a release equally; roles
  such as co-lead are reported separately rather than weighted."
