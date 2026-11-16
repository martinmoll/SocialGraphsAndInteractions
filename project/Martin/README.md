# Martin: the two maps (network and nulls)

Martin's own folder. Each member writes only in their own folder (`Diego/`, `Martin/`, `Anas/`) and never edits or deletes another's.

Martin Møllenhus working with Claude (Anthropic's AI assistant), 16 November 2026. Claude wrote the code;
the choices below are for Martin to defend and for the group to change on 18 November.

| Task | File | State on 16 Nov |
|---|---|---|
| M1 Shared name matcher | [`matcher.py`](matcher.py) | First version. The prototype's matcher plus three fixes from Diego's D1 report. No guard against senators and non-members yet |
| M2 Floor mentions | [`build_mentions.py`](build_mentions.py) → [`mentions.parquet`](mentions.parquet), [`named_ties.csv`](named_ties.csv) | First version: 8,092 mentions, 4,610 directed pairs |

**The shared files are here, not in `data/processed/`**, because of the folder rule. Columns are the ones
agreed in [`../WORK_AND_DEADLINES.md`](../WORK_AND_DEADLINES.md), section 3.

## What the others need to know

1. **Diego (D2):** draw the sample with
   `python Diego/d2_labelling/draw_labelling_sample.py Martin/mentions.parquet`. `context` is the sentence
   with the name plus one sentence either side, as you asked. A few contexts are very long (the longest is
   7,192 characters, the median 349) where the Record has no sentence break.
2. **Anas (A3):** from `project/`, `from Martin.matcher import Matcher`; the docstring in `matcher.py`
   shows the three lines needed. It takes any text, so it runs on press releases as it is.
3. **Everyone:** `mentions.parquet` has two columns beyond the agreed seven: `how` (the rule that resolved
   the name) and `is_leader_title`. `named_ties.csv` is directed: one row per (speaker, named).

## Choices made here

| # | Choice | Alternative and what it would change |
|---|---|---|
| 1 | Surnames are compared without case or accents | The prototype compared exactly: 18 members stored in capitals were invisible, their namesakes took their mentions, and unaccented spellings were lost |
| 2 | A name printed in capitals is dropped (93 hits) | Keeping them counts speaker headings and vote-change lines as speech (3 of the 7 errors in D1) |
| 3 | The independent (Kiley) stays in the file | The prototype dropped him. Filter on party where two sides are needed |
| 4 | Context is three sentences, from a simple splitter | 60 characters either side, as in the prototype: too short to label tone |
| 5 | `is_yield` is unchanged: "yield" within 60 characters | Matching the yielding phrase itself, as D1 suggests. D1 measured the current flag at 87% recall, 90% precision. For M3 |
| 6 | Everything else as in the prototype (its choices 2 to 5): House floor turns of 50 words or more, a title before the surname, shared surnames resolved by first name, then state within 80 characters, else dropped | See section 0 of `../prototype_two_maps.ipynb` |

## What changed against the prototype

| | Prototype (13 Nov) | This version |
|---|---|---|
| Mentions | 7,931 | 8,092 |
| Shared-surname mentions dropped | 717 | 783 |
| Printed in capitals, dropped | counted as mentions | 93 |
| Ties between Republicans and Democrats | 3,718 | 3,777 |
| Cross-party share of those ties | 34.5% | 34.2% |

More shared-surname drops is expected: Green, Turner, Scott, Grijalva and García now have a visible
namesake and go through the shared-surname rules. The 17 formerly invisible members now receive 203
mentions. **Not re-validated:** the 93% precision in D1 was measured on the prototype's matcher, not this one.

## To rerun

From `project/`, with pandas and pyarrow:

```
python Martin/matcher.py           # self-check: nine known cases
python Martin/build_mentions.py    # writes mentions.parquet and named_ties.csv, prints the counts above
```

Run on 16 November with Python 3.14 and pandas 3.0.3.
