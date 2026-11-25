# A3: press releases to named colleagues (scripts)

Plan, decisions and traps: [`../A3_PLAN.md`](../A3_PLAN.md). Run from `Anas/`, with `<repo>` = the `project/` folder of a
checkout of the group repo (for `members.csv` and Martin's matcher):

```bash
python a3/freeze.py       --press press_releases --repo <repo>   # A3.0, about 2 s
python a3/prepare.py      --press press_releases --repo <repo>   # A3.1, about 5 s
python a3/match_shared.py --press press_releases --repo <repo>   # A3.2, about 20 s
python a3/press_layer.py  --press press_releases --repo <repo>   # A3.3, about 30 s
python a3/draw_precision.py --press press_releases --repo <repo>   # A3.3 samples (only once: they are read by hand)
python a3/score_precision.py                                       # after precision_sheets.xlsx is filled in
# after the 21 Nov switch (on Anas's machine: needs the 20 Nov hits, press_hits_layer_75c67ae.parquet)
python a3/rescore_switch.py                                        # what happened to the 180 rows read on 20 Nov
python a3/draw_precision.py --press press_releases --repo <repo> --switch   # 30 rows new after the switch
python a3/score_precision.py switch_sheet.xlsx                     # after switch_sheet.xlsx is filled in
python a3/draw_recall.py  --press press_releases --repo <repo>     # A3.4 sample (only once)
python a3/score_recall.py                                          # A3.4, after the readers' lists are in recall_check/raters/
python a3/bills.py        --press press_releases --repo <repo>     # A3.5, about 20 s
python a3/draw_bill_check.py --press press_releases --repo <repo> --packet <folder>   # A3.5 check sample (only once)
python a3/score_bill_check.py                                      # A3.5 check, after bill_check/raters/
python a3/flags.py        --press press_releases --repo <repo>     # A3.6 + A3.7: out/mentions_press.parquet, about 10 s
python a3/examples.py     --press press_releases --repo <repo>     # A3.7 named examples
```

**If Martin's matcher changes** (items 12 and 15): `freeze.py`, `match_shared.py`, `press_layer.py`, then
`score_recall.py`, `bills.py`, `flags.py` and `examples.py`, about two minutes in all. The hand and reader samples are
stored by release and member, so they are scored again without new reading.

`<repo>` must be at commit `bc1c2344` (main, 22 Nov 20:28: Martin's matcher with the 22 Nov fixes G18 and G19).
Until the 22 Nov rerun it was `7bdbc18c`.

> **Rerun 22 Nov on Martin's 22 Nov matcher** (possessives and middle initials, Anas's checklist items 12 and 15).
> The headline numbers below are updated; old against new for every number, and the one change to the press layer
> (the middle-initial rule now acts only where Martin's reading differs): [`../RERUN_22NOV.md`](../RERUN_22NOV.md).
> Sections describing the 20 and 21 Nov steps (the switch, the guard fix) keep their numbers of that day.

## The 21 Nov matcher switch (DECISIONS G14; plan and reasons in [`../A3_MATCHER_SWITCH.md`](../A3_MATCHER_SWITCH.md))

A3 now uses Martin's matcher of 20 Nov (nicknames, lists after plural titles, "State Rep." skipped, untitled full
names as an option), with his code unchanged. What differs from the floor is input and a thin layer:

| Rule set | What | Use |
|---|---|---|
| `shared` (`match_shared.py`) | Martin's matcher exactly as the floor runs it: his `nicknames.csv`, no untitled names | Like-for-like row in the confusion table |
| `shared + press layer` (`press_layer.py`) | The same matcher with `untitled=True` and `nicknames=out/matcher_aliases.csv` (his 19 nicknames plus the 406 first names members use in their own releases, from the frozen 20 Nov `out/aliases.csv`), plus seven layer rules: party-state tag, own surname, "Assembly" guard, title guard on untitled names, list across party-state tags, quoted nickname, middle initial | A4 (decision 3) |

`out/aliases.csv` is now a frozen input (built 20 Nov, never rebuilt). `out/matcher_aliases.csv` is written from it.

### Results, 21 Nov 2026 (frozen inputs: commit `7bdbc18c`, 55,023 releases; one run)

- **`shared`:** 205,557 hits; self 123,014, counted 71,690, unresolved 10,853. Once per release: **51,569 mentions in
  19,661 releases (35.7%)**, 24.1% cross-party (R–D). Before the switch: 38,557, 29.4%. The rise is Martin's
  list and nickname rules.
- **22 Nov rerun:** `shared` once per release **53,625 mentions in 19,914 releases (36.2%)**, 23.0% cross-party;
  `shared + press layer` **129,473 mentions in 21,867 releases**, 14.4% cross-party (33.0% weighted by 1/n).
  424 release–member pairs new (mostly possessives), 3 gone ("James P. McGovern" in lists read as John James).
- **`shared + press layer`, 21 Nov:** once per release **129,052 mentions in 21,672 releases**, 14.4% cross-party (20 Nov
  layer: 123,147, 15.1%). These are the numbers after the middle-initial rule was added the same evening (see A3.4);
  before it, 128,996 and 14.6%, which appear in some places below.
  - **Counted hits added, by rule:**
    - untitled full name 86,476;
    - quoted nickname 1,112;
    - middle initial 824, which replaces Martin's hit at the same place (3,838 more become self);
    - list across tags 643;
    - alias first name 220;
    - party-state tag 59;
    - list 37.
  - **Moved to self:** own surname 6,421.
  - **Flagged and not counted:** title guard 28, "Assembly" 1.
  - **Martin's hits dropped by the middle-initial rule** because the full name is no member: 16.
  - Still unresolved: 3,531.
- **Against the 20 Nov layer, (release, member) pairs once per release:** 123,013 in both; **134 only in the 20 Nov
  layer** (0.1%; the three looked at are possessives, "Rep. Robin Kelly’s H. Res. 996": Martin's matcher reads
  "Kelly’s" as one word and never matches a possessive, titled or not; reported to Martin in
  `../A3_MATCHER_SWITCH.md`); **5,983 only now** (mostly full names with a middle name or initial, "Mary Gay Scanlon", which the 20
  Nov untitled rule could not see).
- **17 hits give a different member at the same place than on 20 Nov.** All 17 were read on 21 Nov: the new
  version is right in each. 5 are "Chris Smith" and "Buddy Carter", now pinned by nickname: the old matcher gave
  them to Adam Smith (a "WASHINGTON, DC" dateline matched the state rule) and John Carter. 12 are errors of the 20
  Nov list rule: a period joined two names ("Reps. Meng and Malliotakis. Meng" gave Meng), or a middle initial
  split one ("James R. Walkinshaw" gave John James). The 20 Nov 30-row sample (30/30) was too small to see them.
- **The 180 rows read on 20 Nov** (`rescore_switch.py`, `precision_check/rescore_switch.csv`):
  - 152 are found again at the same place, for the same member, with the same status, so the reading carries over.
    The other 28 are gone (below).
  - All 120 counted rows of the four adding rules (untitled full name, list, alias first name, party-state tag)
    carry over: 119 read y, 1 ? (`list_30`, which the three blind readers read y), none n. The 30 own-surname rows
    carry over as self, all y.
  - The two rows read n were the guard's two errors. Omar is now counted under `shared`, which is right.
    Mackenzie is gone; he is a self-mention either way.
  - 28 state-legislator rows are gone, because Martin's matcher skips "State Rep." before matching. That is the
    removal the reading confirmed.
- **New reading, 30 rows** (`precision_check/switch_sheet.xlsx`, seed 2805): counted hits whose (release, member)
  the 20 Nov layer did not have: 26 untitled full names, 4 quoted nicknames. **To be read by Anas**; then
  `python a3/score_precision.py switch_sheet.xlsx`.

Every step after `freeze.py` checks its inputs against `out/inputs.json` and stops if a file differs, so results never
mix two versions of the data or of the matcher.

The two hit files, `press_hits_shared.parquet` (41 MB) and `press_hits_layer.parquet` (55 MB), are over GitHub's
25 MB limit and are not in the repo: `match_shared.py` and `press_layer.py` rebuild them in about 80 seconds. They are
written to `out/` (left out by `.gitignore`), or, on Anas's machine, to `press_raw/a3_out/` next to the raw page cache
(`common.HITS`). Everything else in `out/` is small and is uploaded.

## If the press data or the matcher changes later

1. Rerun the collector (`collector/`, about 15 minutes from the raw-page cache), `combine.py`, `split.py`.
2. Rerun every step above, starting with `freeze.py`: **under a minute** for A3.0 to A3.2.
3. Hand-read samples (precision, recall) are stored by release URL and named member, so they are scored again
   automatically; only releases whose text changed need reading again.
4. Log the date and the reason in `../collector/README.md` and `../../WORK_AND_DEADLINES.md`.

## A3.4 recall check (drawn 21 Nov; reading open)

`python a3/draw_recall.py --press press_releases --repo <repo>` writes `recall_check/recall_sheet.xlsx` and
`recall_check/recall_draw.csv`.

**Design, decided by Anas on 21 Nov.** The sample is drawn without the matcher. A sample drawn from its hits could
never contain a release where it missed everyone, and that would inflate recall.
- **Pool:** releases containing the surname of a House member other than the author. Found by plain string
  search, with accents folded, whole words only, capitalised. That is 31,094 of 55,023 releases (56.5%). **30 are
  drawn from the pool; they give the recall number.**
- **Outside the pool:** the other 23,929. **10 are drawn from them, to check that the pool loses nobody.** They
  should name no one. Before the draw, the matcher found a colleague in only 29 of the 23,929 (0.1%).
- **Blind reading:** the 40 are shuffled together with seed 2805, and the sheet doesn't show which group a release
  is from. Anas lists every House member named, in any form, without seeing the matcher's hits.
- **Size:** 24,769 words in all, median 419 per release, about two hours of reading. One tab per release, one
  paragraph per row.

**Readers changed 21 Nov (Anas): five blind AI readers instead of Anas's own reading.**
- **Who:** 3 Opus and 2 Sonnet sub-agents, each given only a packet. The packet held `INSTRUCTIONS.md` (the same
  counting rules as `recall_sheet.xlsx`), the member list (name, party, state, district) and the 40 release texts.
  No matcher output, no project files, no web.
- **Their lists:** `recall_check/raters/reader1..5.csv`. What they were given is kept in
  `recall_check/reader_instructions.md` and `recall_check/house_members_readers_saw.csv`; the release texts are the
  40 in `recall_draw.csv`. The 7 differences, for a human look: `recall_check/DIFFERENCES.md`. **Anas read all 7 on
  21 Nov and agreed with the readers in each**, so the key and the numbers below stand.
- **The 30-row switch sheet** (`precision_check/switch_sheet.xlsx`) was left unread, by Anas's decision.
  Precision of the switched version comes from this check instead (0.96 on 78 hits) and from the automatic tag check.
- **One rule broken:** reader 1 wrote a scratch copy of releases 11 to 19 outside the packet. It says the copy was
  not used, and it was deleted.
- **Limits:**
  - All five are one model family, so their agreement is not the independent check five people would give.
  - The course asks for model output to be checked against human labels. **The 7 cases where readers and matcher
    differ (below) are for Anas to look at.**

**Results, 21 Nov** (`python a3/score_recall.py`, `recall_check/recall_scored.csv`; one run, matcher at `7bdbc18c`)
- **The key:** all five readers agree on every pair. There are 77 (release, member) pairs in 20 of the 30 pool
  releases, and each was listed by 5 of 5 readers.
  - No pair was listed by only 1 or 2 readers.
  - One unresolved name: "Lee" in a list of Delta sisters (`recall_17`). All five marked it `?`, and it is not
    scored.
- **The 10 releases outside the pool name nobody**, by all five readers. The pool lost no one.

| Press, 40 releases | TP | FP | FN | Precision | Recall | F1 |
|---|---|---|---|---|---|---|
| `shared` (Martin's matcher as on the floor) | 56 | 4 | 21 | 0.93 (0.84–0.98) | **0.73** (0.62–0.81) | 0.82 |
| `shared + press layer`, first run | 74 | 4 | 3 | 0.95 (0.88–0.98) | 0.96 (0.89–0.99) | 0.95 |
| **`shared + press layer` with the middle-initial rule (A4)** | **75** | **3** | **2** | **0.96** (0.89–0.99) | **0.97** (0.91–0.99) | **0.97** |
| `shared`, 22 Nov matcher (rerun) | 58 | 3 | 19 | 0.95 (0.87–0.98) | 0.75 (0.65–0.84) | 0.84 |
| `shared + press layer`, 22 Nov rerun (A4) | 75 | 3 | 2 | 0.96 | 0.97 | 0.97 (unchanged) |

Wilson 95% intervals. Recall's bootstrap interval over releases is wider (0.56–0.88 for shared, 0.59–0.91 after the 22 Nov rerun; 0.94–1.00 with the
layer), because names come in lists. Precision here is a second estimate, from 78 hits; the 30-row rule samples
gave 0.97 or more per rule. The middle-initial rule was added after this check found the bug, so its own row is
scored on the same sample that revealed it (a fit, not a fresh test). Its precision across all releases is
checked below by the counts it moves.

- **What the layer recovers (19 of the 21 shared misses; after the 22 Nov rerun the shared matcher misses 19 and the
  layer recovers 17 of them):**
  - names with a district tag in lists, "Jim McGovern (MA-02), Lori Trahan (MA-03), …";
  - untitled names, "Adriano Espaillat (D-NY)";
  - with the new rule, "Representatives **Alma S. Adams**, Ph.D."
- **The 2 still missed:**
  - "Subcommittee **Chair** Flood": "Chair" is not a title word, only "Chairman".
  - "Ranking **Members** Huffman and Lofgren": the plural of "Ranking Member" starts no list.
- **The wrong ones (counted, in no reader's list):** 4 before the new rule, 3 after.
  - **"Congressman Riley M. Moore" counted as Josh Riley. Fixed by the middle-initial rule.** The middle initial
    made the matcher read the first name as the surname. It is the same bug as the Adams miss; see below.
  - **"Reps. Pressley, Clarke, Demings and Levin" (2021) counted as Mike Levin.** It means Andy Levin, a former
    member: a former member with the surname of a sitting one.
  - **"Congresswomen Shirley Chisholm, **Barbara Jordan**, …" counted as Jim Jordan.** Same kind of error.
  - **"Reps. **Cherfilus McCormick** and Yvette Clarke" counted as Rich McCormick.** The surname is written
    without its hyphen.
- **The middle-initial bug across all releases:**
  - **364 counted press mentions** (once per release) are wrong this way, 96% of them cross-party.
  - John James receives 248, from "James P. McGovern", "James E. Clyburn", "James R. Walkinshaw" and others.
  - Josh Riley receives 114, from Riley Moore's own releases.
  - Small against 128,996, but concentrated: it adds false cross-party ties to two members and inflates Riley
    Moore's cross-party share.
  - **Floor: 4 hits**, all non-members ("Mr. James R. Willis") → `MATCHER_CHECKLIST.md` item 15.
  - **The 20 Nov layer had the same bug**: John James 347 and Josh Riley 318 mentions, against 97 and 204 now.
- **Corrected in the press layer, 21 Nov (approved by Anas): the "middle initial" rule.**
  - **How it reads a name:** a title, first name(s), one capital initial, then the surname. It uses Martin's own
    `TITLE` and `WORD` and his `Matcher.resolve`, so first name and surname are resolved together. It replaces his
    hit at that title, or drops it when the full name is no member (16 hits).
  - **After the rule:** Riley Moore names Josh Riley in none of his releases. John James's 97 and Josh Riley's 204
    remaining mentions are mostly untitled full names, from colleagues such as Lawler and Gillen for Riley.
  - **Left:** 3 counted titled hits still followed by an initial, against 449 before.
  - Floor and press now differ on this rule until Martin fixes item 15. If he does, the rule changes nothing more
    and can stay.

**Scoring rules** (`score_recall.py`):
- Recall = members listed by Anas that the matcher also finds in that release / members listed. Wilson 95%
  interval.
- Computed for `shared` and for `shared + press layer`, with each form missed.
- Names that appear only in template releases or repeated paragraphs are reported separately, since the matcher
  finds them but leaves them out of the count by design.
- The 10 releases from outside the pool are reported on their own.
- The results fill the press rows of the confusion table (`../A3_PLAN.md` section 8).

## A3.5 bills and co-leads (21 Nov)

Run `python a3/bills.py --press press_releases --repo <repo>` (about 20 s). It writes `out/release_bills.csv`, one
row per bill cited in a release. The data is Martin's `bills.parquet` and `cosponsors.parquet` (govinfo BILLSTATUS,
119th Congress).

**How a bill is found:**
- **By number:** H.R., H.Res., H.J.Res. and H.Con.Res., with or without spaces and periods. Senate numbers are kept
  as `senate`; House members cannot cosponsor them.
- **By title (decision 7):** the exact official title, "Act" included, of a House bill whose title belongs to that
  bill alone. Only in releases that cite no bill number.

**When a found bill is set aside as `other Congress`:**
- "118th Congress", "last Congress" and similar within 150 characters;
- a year before 2025 in the same sentence ("In October 2019, … introduced H.R. 5021");
- the bill was introduced after the release date.

Also set aside: `not in data`, a number with no 119th bill.

**For each resolved link:** the sponsor, the number of original cosponsors, and the releasing member's role on the
bill (sponsor, original cosponsor, later cosponsor, none; withdrawn cosponsors left out). Number links also carry
`title_overlap`: the share of the title's content words found within 400 characters.

**Results (one run):**
- **Numbers:** 9,712 cited in 6,473 releases. 8,600 resolved; 645 other Congress, 453 Senate, 14 not in data.
- **Decision 7, titles:**
  - releases naming a House bill by its exact title and no number: 8,410, **+15.3 points of releases**, over the
    5-point bar;
  - the loose version (title words without "Act") would add 24.3 points, but it catches common phrases, so it is not
    used.
- **Together: 18,177 resolved links in 13,944 releases (25.3%)**, 8,600 by number and 9,577 by title.
- **The releasing member's role:** sponsor 8,067, original cosponsor 3,623, later cosponsor 1,636, none 4,851 (a
  bill they comment on or voted for).

**Check: precision of the links.** Done 21 Nov with `draw_bill_check.py` and `score_bill_check.py`, in
`bill_check/`.
- **Sample:** 30 random number links and 30 random title links, shuffled, read by **3 blind AI readers** (2 Opus,
  1 Sonnet).
- **What the readers saw:** the excerpt and the candidate bill (number, official title, sponsor, date introduced),
  nothing else.
- **Result:** **number 30 of 30, title 30 of 30, unanimous** (precision 1.00, Wilson 0.89–1.00). Titles therefore
  pass decision 7's 95% bar and are used.
- **Nothing needed a human look:** there were no disagreements.
- **Limits:**
  - Same-family AI readers, as in A3.4.
  - **A few wrong number links do exist.** Claude's own look at 10 links with no title words nearby found
    "H.R. 5334, the SEED Act" pointing to a different H.R. 5334. Such links sit mostly in the 9.8% with
    `title_overlap` = 0, so `title_overlap` is kept for a robustness row.

## A3.6 and A3.7: flags, weights and the press-mention file (21 Nov)

Run `python a3/flags.py --press press_releases --repo <repo>` (about 10 s), then
`python a3/examples.py --press press_releases --repo <repo>`.

**`out/mentions_press.parquet`** (8.1 MB, zstd) is **the file A4 reads**.
- **One row per colleague counted in a release:** 129,473 rows in 21,867 releases, 412 speakers, 451 named (22 Nov
  rerun; 21 Nov: 129,052 in 21,672).
- **Columns:** the shared columns of `mentions.parquet` first (`speaker`, `named`, `source` = press, `date`,
  `doc_id`, `context`, `is_yield`), then the flags. Every flag is described at the top of `flags.py`.
- **Fixed inputs written down before A4:**
  - **Leaders (decision 2):** [`leaders.csv`](leaders.csv). The seven officers in decision 2, as listed on
    house.gov/leadership, read 21 Nov.
  - **Caucus and redistricting word lists (decision 6):** in `flags.py`, written 21 Nov before any group is
    compared.

| Flag | Share of rows | Cross-party among them |
|---|---|---|
| all rows (R–D pairs) | 100% | 14.4%; **33.0% weighted by 1/n** (decision 8) |
| `in_shared` (Martin's matcher alone also counts it) | 41.4% | 23.0% |
| `co_lead` (named member leads a bill the release cites) | 20.5% | 23.8% |
| `same_state` | 19.3% | 11.3% |
| `first_named` | 16.9% | 34.8% |
| `in_list` | 12.5% | 16.0% |
| `caucus` | 8.4% | 7.4% |
| `named_is_leader` | 2.2% | 36.6% |
| `shared_text` (joint release, 2–4 members) | 0.7% | 6.4% |
| `redistricting` | 0.3% | 10.3% |

Releases name a median of 2 colleagues; 12.4% name 10 or more (22 Nov rerun). Weighting matters because long lists are mostly one
party.

**Named examples and mutual pairs** (`out/named_examples.csv`), over the whole snapshot, not yet the common date
window:

| Pair | A names B | B names A | Co-led bills among them |
|---|---|---|---|
| Roy ↔ Cohen | 4 | 4 | 4 / 1 (the ARTICLE ONE Act) |
| Biggs ↔ Jayapal | 1 | 1 | 0 / 0 (one joint letter on financial surveillance) |
| Golden ↔ Lawler | 8 | 5 | 2 / 2 |
| Golden ↔ Fitzpatrick | 14 | 10 | 7 / 5 |
| Kaptur ↔ Fitzpatrick | 18 | 8 | 3 / 4 (Ukraine Caucus co-chairs) |

**The A4 outcome for the named members:** the share of a member's releases naming the other party, with co-leads
and leaders left out, and with co-leads kept:

| Member | Releases | Outcome | With co-leads |
|---|---|---|---|
| Lawler (R) | 383 | 19.8% | 37.6% |
| Bacon (R) | 163 | 32.5% | 58.3% |
| Golden (D) | 161 | 19.3% | 33.5% |
| Fitzpatrick (R) | 206 | 38.3% | 65.0% |
| Kaptur (D) | 236 | 18.6% | 25.8% |
| Roy (R) | 180 | 5.0% | 8.9% |
| Biggs (R) | 102 | 9.8% | 11.8% |

**The pilot's member figures don't hold.** It counted Lawler at 1 of 10 releases and Bacon at 8 of 10, from 10
recent releases each with its own name rules. On all their releases, Lawler is at 19.8% and Bacon at 32.5%. Every
mutual pair from the pilot is confirmed, in both directions.

## Results, 20 Nov 2026, before the switch (frozen inputs: commit `75c67ae`, 55,023 releases; kept as the record)

These numbers are from the 20 Nov matcher and the 20 Nov layer, which the 21 Nov switch above replaces. The scripts
in this folder now produce the 21 Nov numbers; the 20 Nov scripts are in the repo history (commit `7492057c`).

**A3.0** `out/inputs.json`: SHA-256 of the three parts (equal to `press_releases/MANIFEST.md`), `members.csv`
(identical to the course-folder copy), `Martin/matcher.py`, `Martin/build_mentions.py`.

**A3.1** `out/release_flags.parquet`, `out/repeated_sentences.csv`
- Template texts (decision 4, 5 or more members): **3 texts, 64 releases** ("119th United States Congress
  Convenes" 34 and 5 members, "Newest Members of Congress" 25). Joint releases (2 to 4 members): 164.
- Repeated sentences (decision 5): **84 in 41 members**, median share 57%. **None names another House member**
  (checked with the matcher), so decision 5 removes no partner mentions.

**A3.2** `press_hits_shared.parquet` (not in the repo, see above) (Martin's matcher unchanged, every hit kept with its status)
- 181,963 hits in 50,976 releases: **self 119,546** (members naming themselves), **counted 52,212**,
  unresolved 10,205 (shared surname 10,202, capitals 3).
- Counted, once per release (decision 1): **38,557 mentions in 18,308 releases (33.3%)**, 412 speakers, 450
  members named. Between R and D: 29.4% cross-party. Named with a leadership title: 16.2%.
- Template releases: 0 hits (their name lists carry no titles, which this matcher needs; the flag matters for the
  press layer). Hits in repeated sentences: 2,428, of which 2,421 are members naming themselves (bios).
- **Unresolved, read further:** 7,002 of the 10,205 (69%) are the member's own surname shared with another member
  ("Congressman Biggs": Andy and Sheri Biggs), so not lost mentions. About **3,200 are colleagues lost**, mostly
  nickname first names that do not match `members.csv` ("Rep. Hal Rogers", "Rep. Don Davis", "Congressman Chris
  Smith"): checklist item 9, to be recovered by the press layer (A3.3).

**A3.3** `out/aliases.csv`, `press_hits_layer.parquet` (not in the repo), `precision_check/precision_sheets.xlsx` (Martin's matcher unchanged;
rules follow `MATCHER_CHECKLIST.md` items 1, 2, 4, 9, 10)
- **Aliases:** members.csv first names, plus 19 official nicknames, plus **406 first names members use for themselves**
  in their own releases (most frequent first name before their own surname, at least 5 uses and half of them):
  "Don" Davis, "Chris" Smith, which the official nickname list lacks.
- Rule results (all statuses): untitled full name 72,680 (70,055 counted), list 34,601 (30,968 counted), own surname
  6,180 (moved to self), alias first name 1,362 (563 counted), party-state tag 71 (51 counted), state legislator 42
  (removed; 43 before the 20 Nov guard fix below). Still unresolved: 2,576 (from 10,205).
- **Automatic precision check** (no hand-reading): where a new hit is followed by a party-state tag, does the tag
  match the member chosen? Untitled full name 57,520 of 57,670 (99.7%), list 14,072 of 14,179 (99.2%), alias and tag
  rules 100%. Most disagreements are the release's own typo ("Emanuel Cleaver (MI-05)") or a tag format the check
  does not read ("R-CA-03").
- **Hand precision samples, read 20 Nov:** 30 per rule (seed 2805), one tab per rule in
  `precision_check/precision_sheets.xlsx`. Even 30 of 30 has a Wilson lower bound of about 0.89, so the 95% bar is
  judged on the point estimate with the interval shown. `score_precision.py` prints two tables:

  | Rule | As read by Anas | With `resolutions.csv` | Rows resolved by Claude |
  |---|---|---|---|
  | untitled full name | 30/30, 1.00 | 1.00 (0.89-1.00) | 0 |
  | list | 29/29 (1 ?), 1.00 | 1.00 (0.88-1.00) | 0 |
  | alias first name | 23/25 (5 ?), 0.92 | 1.00 (0.89-1.00) | 7 |
  | party-state tag | 15/21 (9 ?), 0.71 | 1.00 (0.89-1.00) | 15 |
  | own surname | 1/2 (28 ?), 0.50 | 1.00 (0.89-1.00) | 29 |
  | state legislator | 26/30, 0.87 | 0.93 (0.79-0.98); 0.97 (0.83-0.99) after the guard fix | 2 |

  Anas read n or ? where the person could not be confirmed the person from outside the text. `resolutions.csv` resolves those
  rows, one reason per row: alias and tag rows by uniqueness in `members.csv` (only one member has that first name
  and surname, or surname, party and state), own-surname rows by context (bio lines, "said Congressman X" in X's own
  release), and two state-legislator rows where y and n were flipped (former state representatives, not House
  members). The workbook's `correct` column is unchanged. **Own surname rests on Claude's reading (29 of 30)**, so
  it is a second reader's check, not an independent one; say so wherever it is reported.
- **Three blind second readers, 20 Nov** (`score_raters.py`, labels in `precision_check/raters/`): three LLM
  sub-agents (2 Opus, 1 Sonnet), each given only a blank copy of the workbook (`correct` and `note` emptied), its
  "How to read" tab and the list of House members; no other file, no web, no matcher output, no one else's labels.
  One instruction was added to the tab's: a name identifies a member when, with the excerpt's context, it fits
  exactly one member in the list (no outside confirmation needed). Result: **the three agree on all 180 rows**
  (Fleiss' kappa 1.00) and with Anas + `resolutions.csv` on 179 (the exception: `list_30`, Anas ?, raters y).
  Precision is 30/30 on the five adding and own-surname rules, and 28/29 (0.97, 0.83-0.99) on the state-legislator
  guard after the fix; the only n rows are the two guard errors above (Omar, now fixed; Mackenzie). **Limits:** the
  raters are the same model family as the one that wrote `resolutions.csv`, so their agreement is not independent
  evidence the way three human readers would be; and the "fits exactly one member" instruction sets the same
  standard the resolutions used. What they do show: blind to the matcher, all three read the excerpts the same
  way, and none found a wrong member.
- **Guard fix, 20 Nov (from the reading):** the state-legislator guard also accepted lowercase "state", so the verb
  in "Reports further state Rep. Omar" removed a real mention. Now capital "State" only. Rerun: exactly one hit
  changed (back to counted), aliases identical, once-per-release totals unchanged (Omar is named 4 more times in
  that release). That row leaves the guard's pool, so its sample is 29 rows: 28 right (0.97). The other guard
  error is a sitting member named by a former title ("then-State Representative Mackenzie", his own release, so a
  self-mention either way).
- **New finding: signatory lists.** With the layer, mentions rise from 38,557 to 123,147 (once per release), but
  the extra mass sits in a few releases: releases naming 10 or more colleagues are 12% of releases naming anyone
  and hold **63% of all mentions**, at 6.9% cross-party (letters signed by dozens of same-party members). In
  releases naming 1 to 4 colleagues the layer and the shared matcher agree: 35.4% against 34.8% cross-party.
  A4's outcome is per release ("share of a member's releases naming the other party"), so long lists count once
  there; but tie counts (Figure 3 panel B, mutual pairs) would be dominated by them. **Open decision 8**
  (A3_PLAN.md section 6): how ties from long lists are counted.
