# A3: press releases to named colleagues (scripts)

Plan, decisions and traps: [`../A3_PLAN.md`](../A3_PLAN.md). Run from `Anas/`, with `<repo>` = the `project/` folder of a
checkout of the group repo (for `members.csv` and Martin's matcher):

```bash
python a3/freeze.py       --press press_releases --repo <repo>   # A3.0, about 2 s
python a3/prepare.py      --press press_releases --repo <repo>   # A3.1, about 5 s
python a3/match_shared.py --press press_releases --repo <repo>   # A3.2, about 20 s
python a3/press_layer.py  --press press_releases --repo <repo> --leg press_scope/leg.json   # A3.3, about 2.5 min
python a3/draw_precision.py --press press_releases --repo <repo>   # A3.3 samples (only once: they are read by hand)
python a3/score_precision.py                                       # after precision_sheets.xlsx is filled in
```

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
4. Log the date and the reason in `../collector/README.md` and `../STATUS.md`.

## Results, 20 Nov 2026 (frozen inputs: commit `75c67ae`, 55,023 releases)

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
