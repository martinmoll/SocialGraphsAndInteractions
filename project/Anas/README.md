# Anas

Anas's own folder. Each member writes only in their own folder (`Diego/`, `Martin/`, `Anas/`) and never edits or deletes another's.

**Start here: [`STATUS.md`](STATUS.md)** (20 Nov). A priority list for the group, where I stand, what we found
since 18 Nov, and the proposed revisions to each part, with why and what stays unchanged. In short:

- **Top priority, for all three parts:** Martin's name matcher drops six members named by nickname, and its
  recall has never been measured (`MATCHER_CHECKLIST.md`, items 9 to 11).
- **Part 1 (Martin):** the matcher items; optionally one robustness row, a null that keeps members' own states.
- **Part 2 (Diego):** one limitation sentence on recall.
- **Part 3 (me):** both parties (G13); exposure on the district members **served**, not the 2026 map; a second
  lean source; collect every countable member; checks fixed before results. **Collection done (55,023 releases,
  412 members); A3.0 to A3.3 done** (press mentions found and their precision checked).

**New since the last upload (commit `75c67ae`, 20 Nov morning), for Martin and Diego:**

- **The press data is in:** [`press_releases/`](press_releases/MANIFEST.md), 55,023 releases from 412 members,
  snapshot 20 Nov 2026 (kept unless something changes; then rerun in full and logged). Three files, each member
  whole in one file; `MANIFEST.md` has the loader and checksums.
- **The collector was audited before the data was accepted** ([`collector/README.md`](collector/README.md)): it had
  reported members complete that were cut short (Jeffries 10 of 709 releases, Latta 14 of 107, Goodlander 15 of
  360); all fixed, checked against the WordPress API and by a second identical run. Lesson for every dataset we
  use: "the code finished" is not evidence the data is complete; an outside count is.
- **[`STATUS.md`](STATUS.md) section 0:** one page of what is proposed for your parts and why it matters for the
  grade. **Please read row 3:** "measured recall" means checking *the same matcher* for the names it misses (not a
  second matcher). Row 8 proposes one confusion table for the matcher in Methods.
- **[`A3_PLAN.md`](A3_PLAN.md):** the plan for turning releases into named colleagues, with eight decisions
  (section 6). Decision 8 is new: a release naming n colleagues gives each weight 1/n, because releases naming 10
  or more colleagues (signatory lists) are 12% of releases but hold 63% of all mentions.
- **[`a3/`](a3/README.md): Martin's matcher run unchanged on all releases**, plus a separate press layer
  (untitled full names, name lists, nicknames, party-state tags, a state-legislator guard). Precision of every
  rule is 0.97 or above (read by Anas and by three blind readers). Martin: the nickname list and the guard are
  in `a3/press_layer.py` if you want them for the floor matcher (checklist items 9 and 10).
- **Next (Anas):** recall check on 30 releases (Sun 22 Nov), bills and co-leads, flags, the press-mention file
  (Mon 23 Nov), then A4.

| File or folder | What | Date |
|---|---|---|
| [`STATUS.md`](STATUS.md) | Status, findings, proposed revisions to parts 1 to 3, priority list | 20 Nov 2026 |
| [`press_releases/`](press_releases/MANIFEST.md) | **The press data:** 55,023 releases from 412 members, 3 Jan 2025 to 20 Nov 2026, in three parquet files split by member. Read `MANIFEST.md` for how to load them | 20 Nov 2026 |
| [`A3_PLAN.md`](A3_PLAN.md) | A3 plan: steps A3.0 to A3.7, the eight decisions, traps, fallbacks, the confusion-table template | 20 Nov 2026 |
| [`a3/`](a3/README.md) | **A3 scripts and results:** frozen inputs, shared matcher and press layer on the releases, precision check (`precision_check/`: Anas's reading, resolutions, three blind readers). The two large hit files (41 and 55 MB, over GitHub's limit) are not uploaded; the scripts rebuild them in about two minutes (`a3/README.md`) | 20 Nov 2026 |
| [`collector/`](collector/README.md) | **A1:** the press-release collector, its checks and every fix, the WordPress API cross-check, `split.py` | 20 Nov 2026 |
| [`MATCHER_CHECKLIST.md`](MATCHER_CHECKLIST.md) | For Martin: 11 proposed matcher choices with evidence from his matcher, a recommendation and a deadline for each. Scripts in `matcher_check/` | 18 Nov, items 9 to 11 added 20 Nov |
| [`methods_drafts.md`](methods_drafts.md) | Draft Methods and limitation sentences (A6), five checks fixed before the results, data sources table | 19 to 20 Nov |
| [`district_lean/`](district_lean/README.md) | `member_lean.csv` (the file to use): district served and its lean, the 2026 district run in, a second lean measure (2024 presidential margin), fate in 2026. `redraw_dates.csv`: when each of the nine new maps was settled, checked against official sources | 19 to 20 Nov |
| [`press_scope/`](press_scope/README.md) | How many press releases every House member has published since Jan 2025, both parties; layouts of the sites; a small name pilot; recheck of the uncounted sites. No release text collected | 18 Nov, rechecked 19 Nov |
| [`state_seats/`](state_seats/README.md) | Seats per state by party and exposure, redrawn states, releases per state; what the state layer is useful for | 19 Nov |
| [`state_null/`](state_null/README.md) | **For Martin:** proposal and pilot for a null that keeps members' own states. Pilot: state explains almost none of the party division in either map | 19 Nov |
| [`dictionary.md`](dictionary.md) | Every term the project uses, in plain words, so the three of us read them the same way | 19 to 20 Nov |
| [`REVISIONS_19NOV.md`](REVISIONS_19NOV.md) | Replaced by `STATUS.md` | 19 Nov |
