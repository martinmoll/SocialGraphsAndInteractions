# District lean on the map members served in

Anas, 19 November 2026. Fixes the gap noted in the 19 Nov status notes (`STATUS.md`, removed 25 Nov; in the git history): we had the lean of each district on the
2026 map only, but nine states redrew their districts for 2026, so in those states the 2026 lean describes a
different area from the one the member represented in 2025 and 2026.

[`district_lean.csv`](district_lean.csv): one row per district (435), with `lean_2025` (the district as it was
in 2025, the one the member served), `lean_2026` (from `data/processed/districts.csv`), `redrawn_state` and
`changed`. Positive lean = Republican (R+6 is 6), as in `districts.csv`.

[`member_lean.csv`](member_lean.csv): one row per current member (432 R and D), **the file to use in part 3**.
Join on `bioguide`. Columns:

| Column | Meaning |
|---|---|
| `state`, `district`, `lean_2025`, `exposed_2025` | The district the member served in 2025-26, its lean and the exposed label (working rule below) |
| `district_2026`, `lean_2026_ran`, `exposed_2026` | The 2026 district the member actually ran in (from `incumbents.csv`), its lean and label. Empty where our data has no 2026 contest for the member |
| `moved` | Ran under a different district number than the one served (7 members, e.g. Bera CA-6 → CA-3) |
| `redrawn_state`, `fate` | Served in a redrawn state; what happened in 2026 (re-elected, did not run, lost, ...) |

Never join `districts.csv`'s `lean` to a member by district number: in redrawn states that gives the lean of a
different area, and for the 7 who moved it gives the wrong 2026 district too.

```
python Anas/district_lean/old_lean.py data/processed Anas/district_lean
```

## Source

The 2025 Cook PVI (based on the 2020 and 2024 presidential elections), from the table "By congressional
district" in the Wikipedia article *Cook Partisan Voting Index*, **as it stood on 25 May 2025** (revision
1292130997). That is after Cook's 2025 release and before any state redrew for 2026. The script asks Wikipedia
for that exact revision, so it returns the same table every time.

The current version of the article cannot be used: it has been updated to the 2026 maps and gives exactly
the numbers already in `districts.csv` (435 of 435 the same, checked 19 Nov).

It is a secondary source (Wikipedia quoting Cook). Cook's own list was not checked, but a second,
independent source agrees with it almost exactly (next section).

## Second source: 2024 presidential margin (The Downballot)

`pres_margin_2024` in both CSVs: Trump's 2024 margin over Harris in percentage points (positive = Republican,
like the lean), **on the district lines used in 2024**, which are the districts members served. Source: The
Downballot, "2020 and 2024 results according to the district lines used in 2024", linked from
<https://www.the-downballot.com/data> (spreadsheet `1ng1i_Dm_RMDnEvauH44pgE6JCUsapcuu8F2pCfeLWFo`). Their
terms: cite and link, and do not reproduce whole spreadsheets. So only this one column is kept; the script
downloads the sheet each run and the sheet itself is not in the repo.

It is not a third period. The 2024 election was fought on the map members served, and Cook's 2025 PVI is
built from the same 2024 result (plus 2020). It is the same districts, measured a second way, by a source that
does not depend on Wikipedia.

Checks (one run, 20 Nov):

- **Same districts:** the incumbent the sheet names for each district is our member in 411 of 432 cases by
  surname. The other 21 were read by eye: spelling (Jr., accents, nicknames such as Hank Johnson, Chuy
  García) or a vacancy since filled by our member (Wahab for Swalwell, Blair for Scott). So 432 of 432 line up.
- **Agreement:** Pearson r = 0.999, Spearman 0.999 between `lean_2025` and `pres_margin_2024`. Fit:
  lean = −0.73 + 0.515 × margin, so lean +5 is about Trump +11 and lean −5 about Harris +8.
- **What the high agreement means:** it confirms that the lean we took from Wikipedia is right. It is not two
  independent views of the electorate, because PVI is built from these same election results.
- **Labels:** with the margin cut-offs above, 33 Republicans and 58 Democrats are exposed (against 38 and 59).
  **10 members differ, all on the edge:** Republicans at exactly R+5 whose 2024 margin is Trump +12 or +13
  (Bean, Mills, Luna, Zinke, Van Drew), Democrats at D+4 to D+6 (Budzinski, Mejia, Meng, Bynum, Subramanyam).
  So the source hardly matters; the **cut-off** does. A useful check is the A4 result with a cut-off of 4 and
  6 as well as 5, or with lean as a number instead of two groups.

## Checks

- **States that were not redrawn:** 262 of 262 districts have the same lean in the 2025 table and in
  `districts.csv`. So both tables are the same Cook release on the same map there, and the only differences
  are where the maps changed.
- **Redrawn states:** 118 of 173 districts changed lean (AL 4, CA 39, FL 16, LA 6, NC 2, OH 12, TN 6, TX 29,
  UT 4).
- **Spot checks:** Cohen's TN-9 (Memphis) is D+23 in 2025 and R+9 in 2026; Valadao's CA-22 is R+1 in 2025,
  the median district named in that revision's text.

## What it changes

Exposed members by the scope scan's working rule (a Republican with lean ≤ 5, a Democrat with lean ≥ −5),
current members:

| | Same-numbered 2026 district (used until now) | District served (`lean_2025`) | 2026 district run in (`lean_2026_ran`) |
|---|---|---|---|
| Exposed Republicans | 38 | 38 | 36 |
| Exposed Democrats | 60 | 59 | 55 |

The last column is smaller partly because 9 members have no 2026 contest in our data (below).

**12 members get a different label from the district they served and the district they ran in,** all in
redrawn states:

- **Safe as served, exposed in the 2026 district:** Fields, Cohen (D); Gallagher, Issa (R).
- **Exposed as served, safe in the 2026 district:** Harder, Whitesides, Min, Levin, Frankel (D); Young Kim,
  Luna, Laurel Lee (R).

**9 more have no 2026 contest in `incumbents.csv`:** Begich, Barry Moore, Calvert, Wasserman Schultz,
Al Green, Julie Johnson, Veasey, Casar, Kennedy. Why was not checked (another office, a race against another
incumbent, or a name the matching missed). Their 2026 label is left empty rather than guessed.

An earlier version of this file compared with the 2026 district **of the same number** and found 17 changes.
That was wrong for members who ran under a new number (Bera, Moskowitz, Blake Moore) and for the 9 above.

Without this table, the same-numbered 2026 lean would have put members like Cohen (D+23 as served) into the
"exposed Democrat" group, which is the group the comparison depends on.

## When each new map was settled

[`redraw_dates.csv`](redraw_dates.csv): one row per redrawn state, for the optional before/after check
(`../methods_drafts.md`, check 3). Collected 19 Nov from Wikipedia (the snapshot of the 2026 House elections page that
`scripts/03_fetch_results.py` saved on 11 Nov 2026, and one article per state with its revision id), then
checked against official pages and news on 20 Nov.

| Column | Meaning |
|---|---|
| `enacted` | The day the map used in 2026 became law or was adopted: signed, approved by voters, passed by the commission, or ordered by the court |
| `final_for_2026` | Where courts kept it in doubt afterwards, the day it was cleared for 2026 (Texas, Alabama). Empty = not checked |
| `anticipation_note` | When the plan was already public, so members could react earlier than `enacted` |
| `group` | `2025` or `2026`, by the year of `enacted` |
| `check` | How the date was confirmed outside Wikipedia (official page opened, official page seen through a search excerpt, or news with several outlets agreeing) |
| `non_wikipedia_source`, `wikipedia_source` | Where each date comes from |

| State | Enacted | How | Members (exposed as served) |
|---|---|---|---|
| Texas | 29 Aug 2025 | Signed by the governor; in court until 27 Apr 2026 | 37 (2) |
| North Carolina | 22 Oct 2025 | Passed by the legislature | 14 (2) |
| Ohio | 31 Oct 2025 | Redistricting Commission | 15 (6) |
| California | 4 Nov 2025 | Voters approved Proposition 50 | 51 (11) |
| Utah | 10 Nov 2025 | Court-ordered map | 4 (0) |
| Florida | 4 May 2026 | Signed by the governor | 27 (9) |
| Tennessee | 7 May 2026 | Signed by the governor | 9 (0) |
| Alabama | 11 May 2026 | Supreme Court lifted the restriction; cleared 2 Jun 2026 | 7 (1) |
| Louisiana | 29 May 2026 | Signed by the governor | 6 (0) |

**Checked outside Wikipedia on 20 Nov: all nine dates agree.**

- **Official page opened:** California (Secretary of State release of 12 Dec 2025 certifying the 4 Nov 2025
  election); Texas (Senate Journal, passage of HB 4 on the session day of 22 Aug 2025; the signing on 29 Aug
  is from news).
- **Official page read through a search excerpt** (the site blocked a script): North Carolina (Session Law
  2025-95, "ratified this the 22nd day of October, 2025"); Ohio (Secretary of State, "Congressional District
  Plan As Adopted on October 31, 2025").
- **Court documents or several news outlets agreeing:** Utah (the remedial order), Florida, Tennessee,
  Louisiana (the state's notice to the court), Alabama.
- Not checked: the Supreme Court orders for Texas and Alabama themselves, and the Tennessee and Louisiana
  legislature pages.

What this means for check 3:

- **Only the 2025 group has a real "after" period.** Texas, North Carolina, Ohio, California and Utah settled
  their maps between August and November 2025, which leaves 7 to 12 months of releases afterwards.
- **The 2026 group (Florida, Alabama, Tennessee, Louisiana) settled in May 2026,** so "after" is a few months of
  primary season and the summer drop-off in posting. Leave them out of check 3, or report them apart.
- **Anticipation blurs the date.** The Texas plan was public from July 2025, and California answered it in
  August. A member could have changed tone before `enacted`. Try the date of the first public step as a second
  cut-off before trusting a result.
- **Few exposed members.** In the 2025 group, 21 members were exposed as served (California 11, Ohio 6, Texas 2,
  North Carolina 2). The sample would need several of them.

## Which lean to use (for the group: G13, open point 2)

- **Proposed: `lean_2025`, the district served,** for the main comparison. The press releases in 2025 and
  most of 2026 were written for that district's voters.
- **Limit:** once a new map was passed, a member in a redrawn state knew which district they would run in
  next, and may have started speaking to it. The dates the maps passed were not checked here.
- **Check:** rerun the A4 comparison leaving out the 21 members whose label differs or is unknown (the 12 and
  the 9 above). If the result holds, the choice of map does not drive it.
