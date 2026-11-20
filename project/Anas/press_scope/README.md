# Press-release scope: what can be collected, both parties

**One run, 18 November 2026; rechecked 19 November (section "Recheck").** This folder answers how many press
releases each House member has published since the 119th Congress began, and whether a Democratic version of the
close-up is possible. It does not collect release text. That is A1/A2.

Decision G4 (18 Nov) said Republicans only, because both parties would mean "roughly twice the collection".
After the meeting on 18 Nov the group agreed to include the Democrats in a small role, using these numbers.
That decision is drafted as G13 (replacing G4) and will be pasted into `DECISIONS.md`. What it changes for
A1 to A6 is in [`../STATUS.md`](../STATUS.md).

## Results

Releases dated on or after 3 January 2025, on each member's own `house.gov` site:

| | Democrats | Republicans |
|---|---|---|
| Members counted | 198 | 209 |
| Releases | 33,485 | 23,262 |
| Median per member (IQR) | 152 (103–210) | 90 (54–134) |
| Exposed members counted (2026 lean within 5 points, or toward the other party) | 56, ≈10,400 releases | 36, ≈4,700 releases |
| Stopped posting before Sep 2026 | 5 | 27 |

Of the other 43 members: 12 are not in the current-members file (`reps.json`), Jim Jordan's listing ends in
2024, and 30 need hand work. 8 of the 407 counts come from a guessed listing path (`guessed` in the table);
Morrison's is `/news/`, which may hold more than press releases.
The 30 have menus that open only on click, pagers the script does not follow, or (Meeks) a site that serves
the same page for every page number. Six of them answer the WordPress API (see "Recheck").

**Name pilot** (`names_both.py`, 20 recent releases each, 16 members). Share of releases naming at least one
House member of the other party, party leaders left out:

| | Exposed | Safe |
|---|---|---|
| Democrats | 21% (4 members) | 5% (4) |
| Republicans | 36% (4) | 8% (4) |

Too small to report. It shows the Democratic close-up and mutual showing (option E) have material. Pairs that name each other within
these 20 releases: Golden and Lawler, Golden and Fitzpatrick, Kaptur and Fitzpatrick.

## Recheck, 19 November

- **Members:** the official current list (`unitedstates/congress-legislators`, downloaded 19 Nov) has 439
  representatives: the 433 current members in `members.csv` plus the 6 delegates. Nobody joined or left
  since 11 Nov.
- **The 31 sites not counted** (30 hand work plus Jordan): one request each to `/wp-json/wp/v2/posts`.
  Six answer it: Crane, Himes, Nunn, Goodlander, Jeffries, Jayapal. Their full text can be collected through
  the API. The API total counts all posts, not only press releases, so it is not a release count.
  Nunn (exposed R) was missed because his listing redirects to `/category/news/press-releases/` and uses short
  dates ("Oct 27, 2026").
- **A newer site layout:** Budzinski, Gottheimer and Gluesenkamp Perez (all exposed D) list releases at
  `/press` behind a "See More" button, with no page links and no data request that a browser session
  (playwright-cli) could find. Left out of the first rounds; to be named in Methods.
- **api-anything** (a shared catalog of site APIs) still has nothing for `house.gov`.
- **Exposed members in redrawn states,** among those counted: 21 Democrats and 10 Republicans. An earlier
  version of this file said 12 Republicans; that included LaMalfa (left office) and Max Miller (no listing).

Counts were not rerun: a day of new releases does not change the scope, and the final download (A6, Mon 23 Nov)
fixes the dates.

## How it was measured

1. `probe1.py`: fetch each current member's homepage (URLs from `unitedstates/congress-legislators`,
   `reps.json`) and pick the link to the press-release listing. → `stage1.json`
2. `probe2.py`: read the dates on each listing page and binary-search the page where 3 Jan 2025 is crossed.
   Count = full pages before it × releases per page + releases on that page dated after the cutoff.
   → `stage2b.json`
3. `guess.py`: for members with no listing link, try common listing paths. → `guess2.json` (flag `guessed`)
4. `wpcheck.py`: which sites answer the WordPress posts API (`/wp-json/wp/v2/posts`). → `wp.json`
5. `scope_table.py`: join with `data/processed/members.csv` and `districts.csv`. → `scope_by_member.csv`

From `project/`:

```
python Anas/press_scope/probe1.py Anas/press_scope/reps.json Anas/press_scope/stage1.json
python Anas/press_scope/probe2.py Anas/press_scope/stage1.json Anas/press_scope/stage2b.json
python Anas/press_scope/guess.py Anas/press_scope/probe2.py Anas/press_scope/stage1.json Anas/press_scope/guess1.json <IDs>
python Anas/press_scope/probe2.py Anas/press_scope/guess1.json Anas/press_scope/guess2.json
python Anas/press_scope/scope_table.py data/processed Anas/press_scope
```

`<IDs>` is a comma-separated list of the Bioguide IDs whose status in `stage2b.json` is not `ok`.
```

Steps 1 and 2 take about 15 minutes, about ten requests per site, 0.4 s apart on each site.

## Checks

- **Against the release pages themselves** (`spot.py`): Huffman, Lawler and Fitzpatrick, one per pager type.
  The release at position `count` is dated on or after 3 Jan 2025 and the next one before it. Exact in all
  three (Fitzpatrick: release 207 is his swearing-in on 3 Jan 2025, release 208 is from 16 Dec 2024).
- **Against the site's own total:** four WordPress sites, where the API gives the category total since
  3 Jan 2025. Clarke 138, Garamendi 211, Neal 318, Schweikert 39. All four equal the scraped count.
- **Full page walk** (`fullscan.py`): Golden 160 against 162, Lawler 382 against 390. The walk overcounts
  by a few dates that appear twice on a page.

## Known problems

- **Two bugs were fixed before the run above.** Release titles that quote "September 11, 2001" broke
  the date paging, so dates far from the page's median are now dropped. A site that ignores out-of-range
  page numbers (Meeks) gave 10,250, so a repeated page now counts as past the end.
- **"Exposed" is a working rule, not the group's definition.** G4 says a swing seat is not yet defined;
  "within 5 points" was chosen here only to size the samples.
- **"Exposed" uses the 2026 lean.** Of the counted members, 21 exposed Democrats and 10 exposed Republicans are in redrawn states
  (12 Republicans if LaMalfa, who left office, and Max Miller, no listing found, are included),
  where the 2026 district is not the one they served in (Cohen shows +9). Pick exposed members there by
  the old district.
- **Sites that stopped posting skew Republican** (Feenstra and Stefanik both stop on 22 July 2026). Why they
  stopped was not checked. A party comparison needs one common date window.
- **One listing per member.** Some ASP sites split releases over several `DocumentTypeID`s (Cuellar), so
  their counts may be low.
- **The name pilot uses the old regex**, not `Martin/matcher.py`. A senator whose surname is also a House
  member's (Collins) can still match, because the `(R-ST)` tag is checked against party, not state.

## Layouts found

| Layout | Paging | Sites |
|---|---|---|
| Drupal (`/media/press-releases`, `/press-releases`, ...) | `?page=N`, from 0 | 259 |
| Drupal, numbered from 1 (Fitzpatrick) | `?page=N`, from 1 | 19 |
| ASP.NET (`/news/documentquery.aspx?DocumentTypeID=27`) | `&Page=N`, from 1; the ID varies by member | 77 |
| WordPress (`/category/press-releases/`) | `/page/N/` | 25 |
| `PageNum_rs` (Huffman) | `PageNum_rs=N`, from 1 | 21 |

Counts are listings counted in `stage2b.json` (401), before the path guesses. 36 sites answer the WordPress
posts API, some of them with Drupal-style listing URLs.

Drupal sites have no JSON route. Their RSS feed holds 10 items. The api-anything catalog has nothing for
`house.gov`.
