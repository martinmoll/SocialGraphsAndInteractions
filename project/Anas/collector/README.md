# A1: the press-release collector

Anas, 20 November 2026. Collects the full text and date of every press release House members posted on their own
`house.gov` sites since 3 January 2025. No name matching: that is Martin's matcher, in A3.

## Files

| File | What |
|---|---|
| `collect.py` | The collector. One row per release, written per member to a `parts/` folder with a status file and a failure log |
| `combine.py` | Joins the parts into `press_releases.parquet` and `collect_log.csv` |
| `check.py` | The checks below, run on any set of parts |
| `pick_first20.py`, `first20.csv` | The first 20 members (G5 test), chosen by a rule written before collecting |
| `extra_listings.csv` | Six listings the scope scan missed, found through each site's WordPress category list |

```
python Anas/collector/collect.py --scope Anas/press_scope/scope_by_member.csv --raw ../press_raw \
    --out ../press_raw/parts --members all --threads 4          # add --skip-done to resume
python Anas/collector/combine.py ../press_raw/parts Anas/collector
python Anas/collector/check.py ../press_raw/parts Anas/press_scope/scope_by_member.csv
```

Raw pages are kept, gzipped, in `press_raw/` next to the repository (about 30 KB per release), not in the repo.

## Columns of `press_releases.parquet`

The five agreed in `WORK_AND_DEADLINES.md` section 3, then where each value came from.

| Column | Meaning |
|---|---|
| `bioguide`, `url`, `date`, `title`, `text` | As agreed. `text` is the article body only |
| `listing_url`, `layout` | The listing the release was found on and its pager type |
| `date_source` | `meta:article:published_time`, `meta:date`, `url` (a /2026/11/18/ path), `date element` (a visible date label), `time`, `listing` (the date shown next to the link on the listing page, used when the release page has no metadata or URL date), `page time` (a `<time>` outside the article, weak), `body text` |
| `body_selector` | Which article container the text came from |
| `n_words`, `text_sha1` | Length; a fingerprint of the normalised text, to find the same release posted by several members |
| `item_type` | `press release`, `statement`, `op-ed`, `media` (interviews, TV), `newsletter`, from the URL and title. A flag, nothing is dropped |
| `fetched_at` | When the row was produced (the release page itself may come from the raw cache, fetched earlier the same day) |
| `listed` | False for a release the listing no longer shows, kept from an earlier run (its page was online when collected) |
| `member_complete`, `member_stop` | Whether the member's run was complete, and why it stopped (from `parts/<bioguide>.status.json`) |

## How it works

1. **Listing pages** are walked from the newest, with the pager the scope scan found for each site (Drupal
   `?page=N` from 0 or 1, ASP `&Page=N`, WordPress `/page/N/`, `PageNum_rs=N`). Each listing page is fetched
   fresh, so a later run sees new releases.
2. **Each release** on a page is fetched and parsed: title (page metadata, or the `<title>` tag when the
   metadata only gives the member's name), date, and the article body.
3. **The walk stops** when a page's releases are all older than 3 Jan 2025, when a page brings no new links or
   repeats an earlier page, or at a page cap. The stop reason is saved per member.
4. **Only complete members** (stopped at the cut-off, at the last page, with no failed release fetch) count as
   done. A rerun with `--skip-done` retries the rest, and never replaces a complete result with a worse one.

**Politeness and rules.** Each site's `robots.txt` is read and followed. One request at a time per site, 0.5 s
apart, four sites in parallel (eight for the second half of the full run, 20 Nov; the pace per site is the same). A site that answers with 403, 429, 503 or a block page four times in a row is left
alone and the member marked incomplete.

**Article body only.** The text comes from the release's own container (`.evo-press-release__body`,
`.bodycopy`, `.post-body`, `.et_pb_post_content`, `.entry-content`, `#press`, ...). Navigation, sidebars,
"recent releases" boxes, sliders, share buttons and footers are removed, because they name other members and
would turn into false mentions in A3.

## Problems found and fixed during testing (20 Nov)

| Problem | Where | Fix |
|---|---|---|
| The same release linked as `/News/` and `/news/` was collected twice | Cuellar (counted 130 for 65) | Links compared without letter case |
| WordPress category listings link to `/press-releases/<slug>/`, not under `/category/` | Steube, Goodlander | Link rule for WordPress categories |
| Releases on the listing path with `?ID=` | Hal Rogers | Link rule for `?ID=` |
| The whole page inside a `<header>` element | Kiggans | Header removed only when it holds no article |
| Text kept in plain `<div>`s, not paragraphs | Correa | Whole container used when paragraphs miss most of it |
| Date only in a visible label | Steube | Date read from `class="date"` elements |
| Metadata title is just the member's name | Jeffries | `<title>` tag used instead |
| Listing moved since the scan (site moved to WordPress after 18 Nov) | Lynch | Listing found again from the homepage, logged |
| reCAPTCHA scripts in contact forms read as a block page | Clark, Loudermilk | Block pages recognised by their page title only |
| Listing pages without dates walked to the page cap | Ross, Stefanik, Crenshaw | Release dates also end the walk |
| A failed rerun overwrote a good result with an empty file | Clark, Loudermilk | Complete results are never replaced by worse ones |

## Found in the full-run audit and fixed (20 Nov, morning)

Each fix was tested against the cached pages of every member collected by then: old and new rules run side by
side, and the only differences allowed were the intended ones (links: 228 members identical, the rest only gain
links; text: 9 of 31,767 pages change, all gains, no date or title changes).

| Problem | Where | Fix |
|---|---|---|
| Listing at `/media/press-releases`, releases linked at `/media-center/press-releases/<slug>`, `/media/...` or `/press-releases/<slug>`: no link matched | Radewagen, DeGette, Keating, Crow, Scalise, Hudson, Cole (none collected); Foster (1 missed) | Links `.../press-releases/<slug>` accepted under any prefix on the same site |
| Some releases linked only as `/2025/1/<slug>/<uuid>` | Crenshaw 4, LaHood 5, McClain 4, Stefanik 4, Raskin 2, Sewell 1, Fischbach 8, Fitzpatrick 3, Dean 1 (silently missed; members showed as complete) | Trailing uuid accepted; `/<slug>` and `/<slug>/<uuid>` counted as one release |
| WordPress posts at the site root (`/<slug>/`), pager `?paged=N` | Brownley, Clarke (none collected; Clarke's listing shows two-digit years, `11/18/26`, so her walk stops on release dates) | Links inside the listed `<article>`s or `div.post`s of a category page; Brownley's pager set in `extra_listings.csv` (an extra row now replaces the scan's row). WordPress API total since 3 Jan 2025: 169, equal to the scan |
| A link the site itself cut short ("...tribute-to-") gives 404 and kept the member incomplete forever | Harder, Courtney, Zinke, Adrian Smith | A 404 is excused, and logged, when the full link was also listed and collected |
| Release text inside wrappers whose class looks like page furniture (emails or Word pasted into the site: `header-bar`, `x_newsletterContent`, `subscriber-only`, `MsoCommentText`) was removed, sometimes the whole release | Boebert, Hoyer, Miller-Meeks, Westerman (no text at all); Finstad (lead paragraph naming Fischbach and Stauber), DeLauro, Crank, Buddy Carter, Rouzer | Such wrappers kept; a block holding half the body or more is kept, unless it is a slider, "related", "recent" or share block |
| `combine.py` mixed partial members in with complete ones | all | `member_complete` and `member_stop` columns, `member_status.csv`, incomplete members printed |
| Pages showing only two fixed sidebar dates looked like "repeated pages" and ended the walk | **Jeffries: 10 of 709** (marked complete) | A page counts as a repeat by its dates only when it shows at least 5. Checked on all 74 members that stopped on "no new links": only Jeffries was cut this way. Now 709 = WordPress API 709 |
| Pager `?query-79-page=N` (WordPress block pager); `/page/N/` repeats page 1 | **Goodlander: 15 of 360** (marked complete) | Pager set in `extra_listings.csv`. Now 357 + 2 dead links on her site = 359; the 360th is filed at `/media/in-the-news/` (known miss: a rule accepting any path inside a listed post was tested and rejected, it picked up issue and newsletter pages) |
| A run that found more could not replace an earlier, falsely complete one | Goodlander | A new result with more releases always replaces the old one |
| Releases linked at `/press-release/<slug>` (singular) | Amo (none collected), Scalise (2 missed) | Singular accepted |
| A 404 past a WordPress listing's last page read as a failure | Baumgartner (99 = API 99) | Stop reason "listing ended (404 past last page)", complete |
| Dead release links on the site (404, redirect loop) kept members incomplete forever | Wittman, Wied, Goodlander | Counted as `missing_at_source` in the status file and logged; connection errors and timeouts still block completeness |
| Release pages without date metadata fell back to the first date in the text, often a quoted old date: releases dropped as "before 2025", and the walk stopped early | **Latta: 14 of about 110** | (1) A release with no date, or only a text date, takes the date shown next to its link on the listing (date source `listing`; 717 of 718 agree with the release's own date on 80 members tested). (2) A page with at least 5 listing dates decides the cut-off on its own |

| A `<time>` element in the page template (outside the article) read as the release date | Latta: 13 Nov 2017 on every page, so new releases were dropped as "2017" | Such a date is `page time`, a weak source; the listing date also replaces `time` and `date element` dates. When a link's block shows several dates (a title quoting "September 11, 2001"), the one the page uses as an item date. Listing dates against page metadata on 80 members: 694 of 694 agree within a day. Latta: 107 (scan 110) |
| A release that leaves the listing while its page stays online was lost on the next run | Obernolte: 2 releases of March and April 2026 unlisted on 20 Nov (pages still answer 200) | Kept from the earlier run and flagged `listed = False`; undated earlier rows are not carried over |
| Releases with no date at all were kept by default | Espaillat: 14, which the listing dates show are from 2024 | Listing dates now date them, and they are dropped as before 3 Jan 2025 |

After these fixes all 413 members were collected again with the final code (20 Nov, afternoon), so the whole table
comes from one version of the collector.

**Independent check, WordPress API** (`/wp-json/wp/v2/posts?categories=<id>&after=2025-01-03`, 37 WordPress members):
26 equal. Below the API by 1 to 3: McBath, Neal, Whitesides, Lynch, Mullin, Garamendi, the posts logged as "no
article body" (image or video posts). Above: Finstad and McClellan +1 (their 3 Jan 2025 swearing-in post falls outside
the API's date filter, which works in the site's time zone), Carey +8 (releases on his press listing filed under
another WordPress category; the listing is our definition). Riley's site has no matching category.

Checked and left as they are: the drop rule removes 0.12% of all words (15,941 of 13.8 million), mostly share
buttons (690 releases), tag lists (269), "related posts" (160) and category boxes (146). Posts with no text of their
own (McBath, Neal, Whitesides: an image or embed, the page only shows a slider of other posts) stay "no article
body". Divi sites, PDFs-only letters (King-Hinds) and an X-post embed (Díaz-Balart) likewise.

**Not a fault of the collector:** the scope scan's counts are estimates from dates on listing pages, and many sites
show extra dates (Womack and Loudermilk 2 per release; Schmidt 20 dates for 10 items on one page). For the members
furthest below the scan, the collector's link count equals what the listing pages hold.

## First 20 members: results (the G5 test)

`first20.csv`: 2 Republicans and 2 Democrats for each of the five layouts, seed 2805. **All 20 complete**,
2,118 releases (before the title fix; the full run re-parses them).

- **Count against the scope scan:** 15 of 20 within 10%, 14 within 3%. The scan counted dates on listing pages, and
  some sites show two dates per release: Begich's page shows 14 dates for 10 releases, Loudermilk's 20 for 10
  (checked by hand). So the scan overcounted Begich (252, collected 137), Loudermilk (86, 41) and Burchett
  (84, 52); the collector counts releases. Menefee, Crenshaw and Castro are 10 to 14% below; not yet explained.
- **Dates:** every release has one. For the four sites whose date comes from `meta:date`, the collected date
  equals the date shown next to the link on the listing page for **399 of 399** releases.
- **Text:** median 368 words; 14 releases (0.7%) under 60 words, all short statements or notices on reading.
  No broken characters. One sentence recurs in 35% of one member's releases (Burchett's press contact line,
  no member names).
- **Duplicates:** no duplicate URLs; 4 texts posted by more than one member (joint releases, kept).
- **Failures:** 3, all explained (Lynch's moved listing).
- **File size:** 2.4 MB for 2,118 releases, so about 60 MB for everyone. Above GitHub's 25 MB limit for web
  uploads; the full file will be split by party or state for the repo.

## Not collected

Members whose listing loads releases with JavaScript only ("See More" button, no page links, no data feed
found): Budzinski, Gottheimer, Gluesenkamp Perez (all exposed Democrats), Morrison (her `/media/press-releases`
listing answers 410 Gone on 20 Nov; `/news/` shows only the 20 newest releases of about 160, with no pager). Also the 12 who left office
and Jim Jordan (listing ends in 2024). To be named in Methods.
