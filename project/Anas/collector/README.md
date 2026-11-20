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
| `date_source` | `meta:article:published_time`, `meta:date`, `url` (a /2026/11/18/ path), `date element` (a visible date label), `time`, `body text` |
| `body_selector` | Which article container the text came from |
| `n_words`, `text_sha1` | Length; a fingerprint of the normalised text, to find the same release posted by several members |
| `item_type` | `press release`, `statement`, `op-ed`, `media` (interviews, TV), `newsletter`, from the URL and title. A flag, nothing is dropped |
| `fetched_at` | When the page was fetched |

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
apart, four sites in parallel. A site that answers with 403, 429, 503 or a block page four times in a row is left
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
found): Budzinski, Gottheimer, Gluesenkamp Perez (all exposed Democrats), Morrison. Also the 12 who left office
and Jim Jordan (listing ends in 2024). To be named in Methods.
