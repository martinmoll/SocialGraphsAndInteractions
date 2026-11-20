# Press releases: one table in 3 parts

`press_releases.parquet` (55,023 releases, 412 members) is split into **3 parts**
because GitHub's web upload takes files under 25 MB. **Load all parts together**; one part alone is not the data.
Every member is in exactly one part (split by member, in bioguide order), so per-member counts never span files.

```python
import glob, pandas as pd
d = pd.concat(map(pd.read_parquet, sorted(glob.glob("press_releases_part*of3.parquet"))), ignore_index=True)
assert len(d) == 55023  # rows in the unsplit file
```

| File | Releases | Members | First bioguide | Last bioguide | MB | SHA-256 (first 16) |
|---|---|---|---|---|---|---|
| `press_releases_part1of3.parquet` | 21,039 | 158 | A000055 | H001052 | 22.2 | `fef22a6e99d6f8c9` |
| `press_releases_part2of3.parquet` | 19,819 | 146 | H001058 | P000613 | 21.9 | `346755da9b878b0c` |
| `press_releases_part3of3.parquet` | 14,165 | 108 | P000614 | Z000018 | 15.6 | `d57a3148f7dff222` |

Checked when written: the parts read back together are identical to the unsplit table (rows, columns, values),
and no member appears in more than one part. Column meanings: `collector/README.md`.

Releases dated 03 Jan 2025 to 20 Nov 2026; rows produced 2026-11-20 to 2026-11-20. `member_status.csv` gives every member's stop reason and completeness, `collect_log.csv` every failed or excused fetch. Members not collected (listing loads by JavaScript only, or gone): `collector/README.md`, "Not collected".
