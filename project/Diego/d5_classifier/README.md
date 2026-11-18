# D5: what do floor mentions do, across all of them?

Diego Mijares with Claude, 18 November 2026. Part 2 of the paper reads 100 mentions by hand (D2). This step
carries those labels to all floor mentions with a TF-IDF and logistic-regression classifier, the course's
own week 6 tools, and checks it against the hand labels before anything is reported.

**State on 18 Nov: the pipeline runs end to end on Claude's 50 codes as a stand-in. Every number it prints
now is stamped PLACEHOLDER and goes nowhere.** It switches to the human labels by itself once
`agreement.py` has written `../d2_labelling/labels_final.csv` from the returned sheets.

```
python Diego/d2_labelling/agreement.py <folder with the returned .xlsx files>
python Diego/d5_classifier/classify.py
```

## What it does

1. **Text.** The mention's context (the sentence with the name and one either side, from
   `Martin/mentions.parquet`), with the named member's surname replaced by `NAMED`.[^mask]
2. **Features and model.** TF-IDF on words and word pairs that occur in at least two mentions; logistic
   regression with classes weighted by their inverse frequency, so the rare codes are not ignored.[^model]
3. **Check.** Leave-one-out cross-validation: each labelled mention is predicted by a model trained on the
   other 99. Reported: accuracy against always guessing the most common code, macro F1, F1 per code, the
   confusion matrix, and accuracy separately for cross-party and same-party mentions.[^loo]
4. **Apply.** Refit on all labelled mentions and predict every floor mention between two members of the two
   parties: 8,041 mentions, 2,898 cross-party and 5,143 same-party.
5. **Output.** `results.txt`, `shares.csv` (share of each code, classifier on all mentions next to the hand
   labels on the sample), `predictions.parquet`, `figures/d5_codes.png`.

## What the placeholder run already shows

With 50 labels, 38 of them "agreeing", the classifier predicts "agreeing" for almost everything. It scores
80% against 76% for always guessing "agreeing", and finds 1 of 5 disagreements. Expect the same problem with
100 labels. The rare codes have too few examples to learn from. Two consequences for the paper:

- **The hand labels carry the result; the classifier is the extension.** If the classifier does not beat
  the baseline clearly on disagreement, the paper reports the hand-labelled shares with their intervals and
  says, as a finding, that 100 labels are too few for a word-count model to separate praise from attack.
  That counts as a check reported honestly, which the grading rewards.
- **Procedure does not need a model.** Martin's phrase rule for yields (M3) found 30 of 30 labelled yields.
  If the classifier misses P, use the rule for P and the classifier for the rest. Not built yet; one line
  once the group adopts the rule.

[^mask]: Masking the surname stops the model learning that "Johnson" means the Speaker and so tends to be
    criticised. Diego took this decision under Claude's guidance.
[^model]: Default settings (C = 1, no tuning). Tuning on 100 labels would need a cross-validation inside
    the cross-validation and would mostly fit noise. Diego took this decision under Claude's guidance.
[^loo]: Leave-one-out and not 5-fold, because with one or two examples of a code a fold can hold none of
    them. Diego took this decision under Claude's guidance.
