# Diego_Claude: validation and literature

Diego Mijares working with Claude (Anthropic's AI assistant), 14 November 2026. This folder holds Diego's
share of the project as proposed in [`../WORK_AND_DEADLINES.md`](../WORK_AND_DEADLINES.md): D1 to D4. Owners
are not confirmed until 18 November. Nothing here edits another person's notebook or the shared data.

The work was done by Claude in one session at Diego's request and is to be reviewed by Diego. Where a
choice was a matter of judgement, the file carries a footnote saying so, and the choices are listed below.

| Task | File | State on 14 Nov |
|---|---|---|
| D1 Matcher precision | [`d1_matcher_precision/REPORT.md`](d1_matcher_precision/REPORT.md) | 160 matches labelled by Claude. **93 of 100 correct in the random sample, provisional until Diego has checked the labels** |
| D2 Labelling protocol | [`d2_labelling/PROTOCOL.md`](d2_labelling/PROTOCOL.md) | Version 1 written, scripts tested on a stand-in file. Sample waits for `mentions.parquet` (M2) |
| D3 Prior work | [`d3_prior_work.md`](d3_prior_work.md), [`references.bib`](references.bib) | Eight references verified in Crossref and summarised from abstracts. Westwood's year settled: 2022 |
| D4 Introduction, Discussion, reflection | [`d4_drafts.md`](d4_drafts.md) | Drafted with placeholders for every number that is not frozen |

## What the others need to know before 18 November

1. **Martin (M1):** `members.csv` stores the surname of 18 members in capitals and the matcher never finds
   them. Their namesakes (Al Green, Adelita Grijalva, Michael Turner, the Scotts) receive their mentions.
   Details and counts in the D1 report, with two further fixes: drop matches whose surname is printed in
   capitals, and match the yielding phrase instead of a 60-character window.
2. **Martin (M2):** for the hand-labelling, `context` is more useful as the sentence plus one sentence
   either side.
3. **Everyone:** the protocol proposes five codes, 200 mentions, Diego coding all and Martin and Anas 100
   each. About an hour each for Martin and Anas.
4. **Anas (`docs/AI_METHODS.md`):** D1 labels are a model's first pass until checked by a person, and this
   file should be listed with the rest.

## Decisions that are Diego's to confirm

Taken by Claude as the best option and footnoted in the files. Each can be changed.

| # | Decision | Where | Alternative |
|---|---|---|---|
| 1 | A match in a vote-change line or speaker heading counts as an error (strict precision, 93%) | D1 | Count it as correct because the member is right (96%) |
| 2 | Sixty extra matches from the rare resolution routes, reported separately | D1 | Only the random 100 |
| 3 | Five codes: agreeing, disagreeing, procedural, neutral, not a mention | D2 | The three in the work plan plus "other" |
| 4 | Routine thanks to a chairman or ranking member are coded agreeing | D2 | Code them procedural, which would lower the agreeing share |
| 5 | Sample of 150 cross-party and 50 same-party; Diego codes all, the others half each | D2 | Everyone codes everything; or cross-party only |
| 6 | If κ is below 0.6 the paper reports only procedural against not procedural | D2 | No threshold fixed in advance |
| 7 | References chosen: Green et al. (2024), Grimmer (2013), Harbridge and Malhotra (2011) added to the README's list; Andris, Kirkland, Grimmer et al. (2012) left out | D3 | A longer list |
| 8 | Novelty is claimed only as "to our knowledge" | D3, D4 | A stronger claim, which two searches do not support |
| 9 | The direction of the matcher's bias is stated in the Discussion | D4 | Methods only |
| 10 | The Discussion is drafted in two versions, to be chosen by the labelling result | D4 | Wait for the result |

## To rerun

From `project/`, with pandas and pyarrow installed:

```
python Diego_Claude/d1_matcher_precision/draw_sample.py     # rebuilds the notebook's mentions, draws the samples
python Diego_Claude/d1_matcher_precision/make_labels.py     # writes labels.csv, keeps any diego_check entries
python Diego_Claude/d1_matcher_precision/score.py           # every number in the D1 report
```

Run on 14 November with Python 3.12 and pandas 3.1.1. The mention table reproduces the notebook's exactly
(7,931 mentions, 717 dropped) and the first 30 sampled rows are the 30 the notebook prints.
