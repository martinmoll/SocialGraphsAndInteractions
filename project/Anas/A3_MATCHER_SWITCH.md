# A3: switching to Martin's 21 Nov matcher (plan, for Anas's approval)

Anas with Claude, Sat 21 Nov 2026. **Approved by Anas 21 Nov; done the same evening** (section 4; numbers in
[`a3/README.md`](a3/README.md)). Only the 30-row reading (point 5) is open. Why: DECISIONS G14 (agreed by Martin
21 Nov) says A3 moves to the current matcher, so floor and press use one name matcher, and "what his press layer
still adds on top is his to record". This file is that record. A3.0 to A3.3 are frozen to the matcher at commit
`75c67ae`; the a3 scripts refuse to run on the new one until it is frozen on purpose (`common.load_inputs`).

## 1. What was measured first (one read-only run, 21 Nov; nothing in `Anas/` written)

Martin's matcher at `5b65a830` (`matcher.py` is identical on `main`, `7bdbc18c`) run on all 55,023 releases with
`untitled=True`, statuses as in `match_shared.py`, compared with the frozen layer hits (`press_hits_layer.parquet`).
Counted mentions, once per release:

| Version | Mentions | Releases naming a colleague | Cross-party (R–D) |
|---|---|---|---|
| Old shared matcher (`75c67ae`), A3.2 | 38,557 | 18,308 | 29.4% |
| Old shared + press layer, A3.3 | 123,147 | 21,652 | 15.1% |
| New matcher, titles and lists only | 51,569 | 19,661 | 24.1% |
| New matcher, plus untitled full names | 123,726 | 21,580 | 14.6% |

- **96% of (release, member) pairs are the same** (118,048). Only in the old layer: 5,099. Only in the new matcher:
  5,678.
- **Only in the old layer:** mostly first names members use themselves ("Val Hoyle", "Pat Ryan", "Don Davis",
  "Dan Meuser"). The new matcher knows only `members.csv` first names plus 19 official nicknames. Our
  `aliases.csv` adds 406 more. The rest: 39 party-state tags, and quoted nicknames (Robert C. "Bobby" Scott).
- **Only in the new matcher:** mostly full names with a middle name or initial ("Bennie G. Thompson", "Mary Gay
  Scanlon", "Eugene Simon Vindman"). The old untitled rule could not see them. In the 12 sampled, every one was right.
- **17 hits where the two give a different member at the same place.** The new matcher is right in all 17 I read:
  - **5 from the old shared matcher (fixed by the nicknames):** "Congressman Chris Smith (NJ-04)" went to Adam
    Smith because of "WASHINGTON, DC" in the dateline, and "Buddy Carter" went to John Carter.
  - **12 from the old layer's list rule:**
    - **A period ran two names together:** "Reps. Meng and Malliotakis. Meng recently…" gave Meng.
    - **A middle initial split a name:** "James R. Walkinshaw" gave John James.
  - Its 30-row precision sample (30/30) was too small to catch these.
- **Three things for Martin, not changed here (error fixes, allowed under G17):**
  - **"Washington" counts as the state.** The "state nearby" rule reads Washington the city as Washington the
    state.
    - The old matcher's two Chris Smith errors came from a "Washington, DC –" dateline.
    - With the new matcher, **up to 6 press hits** go to Adam Smith this way ("when I return to Washington,
      Chairman Smith…"), and at least one of them is right ("veterans in Washington State," said Rep. Smith).
    - **Floor: 2 mentions**, from one passage. On my reading of the excerpt it is about the film *Mr. Smith Goes to
      Washington*, not a member.
  - **The untitled rule has no guard against a preceding title.** 11 of 81,950 untitled press hits follow a word
    such as "Sen." or "Governor". Some are real errors ("New Jersey Governor Mikie Sherrill"). Others are correct
    and only tripped our guard (Mike Rogers after "The President and"; signatories after "Secretary Noem:").
    It is off for the floor.
  - **Added after the run: possessives are never matched** (both versions, all sources). "Mr. Cole’s amendment"
    and "Rep. Chip Roy’s bill" give no hit, because the matcher reads "Cole’s" as one word (tested on his
    `matcher.py` at `7bdbc18c`). One run with the possessive blanked out:
    - **Floor:** 417 more colleague mentions (4.8% on top of 8,622), 33.6% of them cross-party.
    - **Press, titled names only:** 1,275 more, 37.5% cross-party.
    - Not hand-checked.

## 2. Proposed switch (each point for Anas to approve)

1. **Base:** Martin's matcher at `main` commit `7bdbc18c`, frozen by SHA-256 as before. The untitled rule is on
   for press. G14 allows that ("the press side can turn it on"), and it replaces our own untitled rule.
2. **Aliases go in as input, not as code:** `Matcher(members, nicknames=<aliases>)` with the 20 Nov `aliases.csv`
   (official nicknames plus the first names members use in their own releases), unchanged and frozen.
   - Martin's code stays untouched, and the aliases reach titles, lists and untitled names alike.
   - The alias rule already read 30/30 for precision.
3. **The press layer shrinks to what the matcher lacks:**
   - **Kept:** party-state tags "(R-NJ)" to settle shared surnames; a member's own shared surname counted as a
     self-mention ("Congressman Biggs" in Andy Biggs's release); "Assembly" before a title; the guard on untitled
     names after "Sen.", "Gov.", "Mayor" and similar (flagged, not deleted).
   - **Dropped:** the layer's own list, untitled and alias rules, now done by the matcher.
4. **Two rule sets stay visible, as decision 3 of `A3_PLAN.md` requires:**
   - `shared`: Martin's matcher exactly as the floor uses it (no untitled names, no extra aliases). This is the
     like-for-like row in the confusion table.
   - `shared + press layer`: points 1 to 3 above. This is the version A4 uses.
5. **Precision is checked again without starting over.**
   - The 180 rows read on 20 Nov are stored by release and member, so the script re-scores the ones the new
     matcher still produces.
   - **New reading (Anas, about 15 minutes):** 30 rows drawn (seed 2805) from the hits that only the new version
     produces. The bar is still 95%.
6. **Order:** this switch comes before A3.4. The recall sheet is read without the matcher's hits, so it can be
   drawn now, but it is scored against the switched matcher.

## 3. Steps (Claude: about an hour; Anas: about 15 minutes of reading)

1. Clone the repo at `7bdbc18c`. In `common.input_files`, add `aliases.csv` to the frozen inputs. Run `freeze.py`.
2. In `match_shared.py`, pass the aliases and `untitled=True` for the layer run, and keep a run with neither as
   `shared`. Then trim `press_layer.py` as in point 3. Rerun A3.2 and A3.3 (about 2 minutes).
3. Check that the self-check passes, that the totals are within a few hundred of section 1's preview, and that
   the 17 conflicts now come out as read.
4. Re-score the 180 rows, draw the 30 new rows, then score them once Anas has read them. (Done, except the 30 rows:
   left unread by Anas's decision of 21 Nov. The A3.4 recall check measured the switched version's precision
   instead, at 0.96.)
5. Update `a3/README.md`, keeping the 20 Nov numbers as the record, plus STATUS section 3, decision 3 in
   `A3_PLAN.md`, and a log line. Message Martin the two points at the end of section 1.

**Not changed:** decisions 1 to 8 of `A3_PLAN.md` (including weight 1/n), the press data, A3.1's flags.

## 4. What was done, 21 Nov, and two deviations from the plan

Steps 1 to 4 are done. Inputs are frozen at `7bdbc18c`, and `inputs.json` now also holds `Martin/nicknames.csv` and
`aliases.csv`. The 20 Nov hit files are kept on Anas's machine as `press_hits_*_75c67ae.parquet`, outside the
upload folder. Step 5's message to Martin is not sent yet.

**Two layer rules added that point 3 did not list.** The re-score showed that dropping the old layer's own rules
lost mentions in two forms Martin's matcher cannot read. Both rules restore what the 20 Nov layer already
counted; neither adds a new kind of mention:

1. **List across tags.** "Reps. Sessions (R-TX), Meuser (R-PA) and Bacon (R-NE)": Martin's list rule stops at the
   first tag. This rule steps over the tag and resolves each name with his own `Matcher.resolve`. It does not join
   names across a period, which was the 20 Nov rule's error. Pairs lost against 20 Nov fell from 439 to 11.
2. **Quoted nickname.** Jesús G. “Chuy” García, Henry C. “Hank” Johnson, Robert C. “Bobby” Scott, Glenn “GT”
   Thompson, Earl L. “Buddy” Carter: the quote mark stops Martin's untitled rule. About 750 mentions came back,
   most of them of four of the six nickname members of checklist item 9 (García, Johnson, Scott, Carter).

With both, **134 pairs (0.1%) are only in the 20 Nov layer**; the three I looked at are possessives (see "for
Martin" in section 1).

**No precision sample yet for the two added rules.** The 30-row switch sheet holds 4 quoted-nickname rows and no
list-across-tags rows. The automatic tag check of 20 Nov was rerun instead, on hits followed by a party-state tag,
leaving out hits where the tag itself chose the member:
- quoted nickname: 214 of 214 agree;
- list across tags: 552 of 574 (96.2%);
- untitled full name: 19,529 of 19,623 (99.5%);
- alias first name: 52 of 52.

That check is not a hand reading. Whether to read 30 rows each for the two rules is Anas's call. 5,983 are only in the new version, mostly middle
names, and the 30-row sample is drawn from them.

**Result in one line:** 128,996 press mentions once per release, 14.6% cross-party, against 123,147 and 15.1% on
20 Nov.

**A third rule, added later on 21 Nov** after the A3.4 recall check found the bug: "middle initial" (`a3/README.md`,
A3.4; `MATCHER_CHECKLIST.md` item 15). With it, the totals are 129,052 and 14.4%. All 120 carried-over counted readings are still y or ? (none n).
