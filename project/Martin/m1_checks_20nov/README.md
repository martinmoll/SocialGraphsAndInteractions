# M1: the 20 November matcher changes and their hand checks

Martin working with Claude, Friday 20 November 2026. Claude wrote the code. The changes come from Anas's
[`MATCHER_CHECKLIST.md`](../../Anas/MATCHER_CHECKLIST.md) (item numbers are his). Recorded as DECISIONS G14.

## What changed in `matcher.py`

| Item | Change | Floor effect (rebuild of `mentions.parquet`) |
|---|---|---|
| 9 | Nicknames count as first names (`nicknames.csv`, 19 House members, from `legislators-current.json` in unitedstates/congress-legislators) | +21 mentions, all of four of the six: Chuy García 9, Bobby Scott 8, Chris Smith 3, Hal Rogers 1. Hank Johnson and Buddy Carter are now matched in the tests but gain no floor rows (their nickname forms appear 2 and 8 times on the floor, mostly without a title). 5 mentions resolved by "state nearby" are now resolved by first name (same member) |
| 1 | Lists after a plural title: "Reps. A, B, and C", "Representatives A and B" | +508 mentions with `how` starting `list: ` (34 more dropped as shared surnames) |
| 10 | Skip a title right after "State" ("State Rep. Smith") | No floor row removed |
| 5 | Senators: no change ("Senator" is not a title); pinned by a test | — |
| 2 | Full names without a title: **optional, off for the floor** (`find(text, untitled=True)`) | Not in `mentions.parquet`. 904 such hits on the floor; the hand check below decides |
| 3 | Carry a resolved name forward within a turn | **Not done.** Methods sentence instead |

**Total: 8,092 → 8,622 mentions; 4,610 → 4,931 directed pairs. No 18 Nov row was lost.** (22 Nov, G18: possessives and
middle initials fixed, 9,058 mentions and 5,039 pairs; 4 wrong rows removed, all D2 and yield-check rows kept.
G19: untitled full names on, 9,988 mentions and 5,400 pairs.) The rows are in turn
order, so row numbers moved: [`row_map.csv`](row_map.csv) maps every 18 Nov row to its new row.
[`compare_18nov.py`](compare_18nov.py) checks that all 100 rows of Diego's `full_key.csv`, the 20 of
`sample_key.csv` and the 30 of `m3_yield_check/yield_check_key.csv` are still there with the same speaker,
named member and context. **Diego:** your codes still apply; use `row_map.csv` if you look up a row by
`mention_row`. D5 reads `mentions.parquet` and will now apply to 9,988 mentions (22 Nov, G19).

**Not yet validated by a human:** the 530 new rows. Claude read 25 of them at random on 20 Nov and found no
wrong member. A later audit the same day found a double count (a list running into a titled name, "Representatives
Scholten and Representative Gillen", counted Gillen twice: 4 rows, no tie changed) and fixed it, with a test, but G10's 98/100 precision was measured on the 18 Nov rows only. The list check below is the
human check.

**A modelling point for the defence:** most new rows come from thank-you lists, some long ("I thank
Representatives Joyce, Larsen, Figures, Rouzer, …", 15 names). Each name becomes a tie. That is what the floor
map means by "named", but the M3 table now has a row with the list hits dropped, so the effect on the headline is
visible.

## Three hand checks for Martin (before Sun 22 Nov)

Fill in the `_sheet.csv` files. **Don't open the `_key.csv` files until you are done.** Then tell Claude, and it
scores them.

### 1. Recall: `recall_sheet.csv` (30 floor turns, about an hour) — item 11

For each turn, write in `named_members` **every House member named in it**, surnames separated by `;`.
Count a member once per turn.

- **Counts:** a name in any form: "Mr. Cole", "Chairman Cole", "Tom Cole", "Bobby Scott", a name in a list.
- **Doesn't count:** the speaker themselves; "Mr. Speaker" or "Madam Chair" as an address; a member described
  without a name ("the gentleman from Texas"); senators, presidents, state legislators, staff, constituents.
- Not sure if someone is a House member? Write the name with `?` and a note.

Recall = members the matcher found / members you listed. The turns are drawn at random from turns of 50 to 1,000
words (97% of the turns), so many name nobody: the matcher finds 12 members in the 30. If your list gives fewer
than about 20 names, the interval will be wide; say so, or draw 30 more.

### 2. Untitled full names: `untitled_sheet.csv` (30 rows, 20 minutes) — item 2

Each row is a full name without a title, marked `[[like this]]`. Code:

| Code | When |
|---|---|
| **M** | A mention of that House member ("my colleague and friend, [[Chip Roy]]") |
| **P** | The member, but procedure: tellers, appointments, a list of conferees read by the Clerk |
| **X** | Not that member (someone else with the same name, a bill named after someone, a quote) |

Proposed rule, **set by Claude, for Martin to confirm before coding**: if **at least 24 of 30 are M**, the untitled rule goes into the floor mentions as well; if
not, it is used for press releases only and Methods says so.

### 3. List hits: `list_sheet.csv` (20 rows, 10 minutes) — item 1

Each row is a member found in a list after a plural title. Code **OK** if `named_name` is the member the speaker
names, **X** if not. With 20 rows this catches a gross failure, not a precise rate.

## To rerun

From `project/`:

```
python Martin/matcher.py                          # self-check, now 20 cases
PYTHONPATH=Martin python Martin/build_mentions.py
python Martin/m1_checks_20nov/compare_18nov.py
python Martin/m1_checks_20nov/draw_checks.py       # redraws the same sheets (fixed seed): don't run after you start coding
```

## Result 1: recall (coded by Martin, scored 22 Nov)

Coded sheet: `recall_sheet.csv` (original `recall_sheet_coded.xlsx`). The matcher of 22 Nov (G18) finds the same
members in these 30 turns as the 20 Nov one, so the key did not change.

- Martin listed 12 House members in the 30 turns (most turns name none). The matcher found 11: **recall 11 of 12 = 92%
  (95% interval 65% to 99%)**.
- **One name the matcher found and the sheet left out:** turn 16, "Speaker Johnson is calling this a show vote".
  That is Mike Johnson, named with his title, so by the coding rules he counts; the matcher was right (Speaker rule).
  Counted with him: **12 of 13 = 92% (67% to 99%)**. The paper should use this reading, and say so.
- **The one miss:** turn 24, "I am proud to lead this bipartisan bill with Congressman Evans". Two members are named
  Evans (Gabe Evans R-CO, Dwight Evans D-PA) and nothing nearby gives a first name or a state, so the matcher drops
  the name by design ("shared surname, dropped": 828 floor names in all). Not a fixable bug: guessing would add
  wrong ties. Methods can say so in one sentence.
- **Limit:** 13 names is few, so the interval is wide. It rules out a recall below about two thirds, not more. Drawing
  30 more turns would narrow it; under the scope freeze (G17) that is optional.

**For Methods / Anas's matcher table:** floor precision 98 of 100 (D2, G10); floor recall 12 of 13 on 30 hand-read
turns; the only miss is a shared surname with no first name or state nearby.

## Result 2: untitled full names (coded by Martin, scored 22 Nov)

- **29 of 30 coded M (97%, 95% interval 83% to 99%)**, 0 P, 1 X. The one X is row 24, "the great [[Jim Clyburn]]
  flipped the script", said by Jeffries about Rep. James E. Clyburn; "Jim" is his official nickname, so on a second
  reading it is M as well. **Recoded M by Martin 22 Nov: 30 of 30 (95% interval 89% to 100%).**
- **By the rule agreed before coding (G14: 24 or more of 30 M), untitled full names go into the floor data too.**
  Applied 22 Nov with a title guard: see DECISIONS G19.

## Result 3: list hits (coded by Martin, scored 22 Nov)

- **19 of 20 coded OK (95%, 95% interval 76% to 99%)**. The one X is row 10, "[[Dave Taylor]]" in Sam Graves's thanks
  to Transportation and Infrastructure members, with the note "Dave instead of David, unsure if Dave is a nickname".
  It is Rep. David J. Taylor (R-OH), on that committee; on a second reading it is OK. **Recoded OK by Martin 22 Nov: 20 of 20 (95% interval 84% to 100%).**
- No sign of a wrong rule: the list hits stay as they are (G14).
