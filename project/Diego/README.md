# Diego: validation, labelling and literature

Diego Mijares's part of the project "Two maps of Congress", done with Claude (Anthropic's AI assistant). This
folder holds **only Diego's own work**: each check and analysis, its data, its code and what it found. The shared
paper is in [`../report/`](../report/README.md); this folder explains the pieces of it that come from Diego, so that
anyone, or any teammate's Claude, can use them in the paper and answer questions about them at the presentation.

Each member writes only in their own folder (`Diego/`, `Martin/`, `Anas/`). Every decision and its reason is in
[`../DECISIONS.md`](../DECISIONS.md); who did what and when is in [`../WORK_AND_DEADLINES.md`](../WORK_AND_DEADLINES.md).

## The project in two sentences

We draw the 119th US House twice on the same 450 members: a **working map** (A is tied to B when A cosponsors B's
bill) and a **floor map** (A is tied to B when A names B in a floor speech), and ask whether the floor map is less
divided by party. It is (38.7% of floor ties cross parties, against 28.6% of working ties of the same size; Martin's
part), and Diego's checks say what that number can and cannot carry.

## The parts, in the order they were done

| Part | Question it answers | Main result | Where |
|---|---|---|---|
| **D1** Matcher precision, first version | When the code finds "Mr. Cole" in a speech, is it the right member? | 93 of 100 right on the prototype matcher; errors mostly cross-party, which led to Martin's matcher fixes | [`d1_matcher_precision/`](d1_matcher_precision/REPORT.md) |
| **D2** What a mention does | Are cross-party mentions praise, attack or procedure? | 69% agreeing, 7% disagreeing, 23% neutral; human coders agree at κ 0.64 | [`d2_labelling/`](d2_labelling/RESULTS.md) |
| **D3** Prior work | What is known, and is our comparison new? | 12 references, all verified; Westwood (2022) is the closest study | [`d3_prior_work.md`](d3_prior_work.md), [`references.bib`](references.bib) |
| **D4** Introduction and Discussion | How the paper opens and what the result means | Drafted by Diego with Claude, revised with Martin (G3) | [`d4_introduction_discussion/`](d4_introduction_discussion/) |
| **D5** Text classifier | Can a model carry the 100 hand labels to all 9,909 mentions? | No: 73% right against 72% for always guessing "agreeing" | [`d5_classifier/`](d5_classifier/README.md) |
| **S2** Speaker check | Is each speech credited to the member who gave it? | 60 of 60 right | [`s2_speaker_check/`](s2_speaker_check/) |
| **AI methods** | Where did a model touch a result, and how was it checked? | 14 places, each with its check | [`AI_METHODS.md`](AI_METHODS.md) |
| **Reflection** | Did the course's "AI-drafted report" boxes change how we read our draft? | Draft for Diego to rewrite in his own words | [`reflection_draft.md`](reflection_draft.md) |

## Each part in plain words, with what to say if asked

**D1, matcher precision.** The name matcher is code that finds members' names in speeches. We drew 100 of its
matches at random and read each one in context. 93 were right (95% interval 86% to 97%). The 7 errors were a
constituent called "Mrs. Peters", a post office named after "Mrs. Cole", a member who had died and his namesake,
and Record text such as vote-change lines that nobody said. 5 of the 7 joined members of different parties, which
would make the floor map look *less* divided than it is. The checks also found that the member list stored 18
surnames in capitals and accented names (Velázquez, García) were never matched. Martin fixed these; precision on
the fixed matcher, measured in D2, is 98 of 100. *If asked "how do you know the names are right?":* we read 100 of
them by hand, twice over two versions of the matcher. Claude made the first-pass labels; Diego checked them.

**D2, what a mention does.** A name can be thanks or an attack, so we read 100 floor mentions (75 between parties,
25 within one) and gave each one of five codes: procedure (handing over speaking time), agreeing, disagreeing,
neutral, or not that member. The rules are in [`d2_labelling/PROTOCOL.md`](d2_labelling/PROTOCOL.md) and were fixed
before coding; the party was hidden on the sheet. Diego coded all 100; Martin coded rows 1 to 25, Anas rows 76 to
100 and Claude rows 26 to 75 as second coders. Humans agreed on 82% (Cohen's κ 0.64, above the 0.6 set in advance).
Result: cross-party mentions are mostly credit (69% agreeing, 95% interval 58% to 79%) and rarely argument (7%).
So the "members talk across the aisle to argue" reading is out. Three extra Claude runs agreed with each other
almost perfectly and with Diego at κ about 0.57: being the same model, they show stability, not correctness.
Diego changed two codes after the AI flagged them (a port director and a member's late husband, both matcher
errors); the paper says so. Figure 2 of the paper is made here by [`d2_labelling/figure2.py`](d2_labelling/figure2.py).

**D3, prior work.** Every reference was looked up in Crossref; summaries come from abstracts, and Westwood's from
the publisher's page. The key ones: Fowler (2006) defines the cosponsorship network; Harbridge (2015) shows that
votes and cosponsorship give different levels of bipartisanship; Westwood (2022) shows that saying "bipartisan" on
the floor is unrelated to bipartisan votes; Green et al. (2024) show polarization differs by communication venue.
Our contribution is to use *named colleagues* instead of words. Novelty is claimed only as "to our knowledge".

**D4, Introduction and Discussion.** Drafted by Diego with Claude on the frozen numbers, revised with Martin.
The folder holds a snapshot of both sections as of 25 November; the live version is in `../report/sections/`.
The Discussion's main points: the floor map is less divided, but a mention is not cooperation; debate procedure
explains about two thirds of the floor map's party division and its communities follow committees; precision 98
of 100 and recall 12 of 13; the classifier failed; one Congress only.

**D5, classifier.** A TF-IDF and logistic-regression model (week 6 tools) trained on the 100 hand labels, tested
by leave-one-out against them. It scored 73% against 72% for always answering "agreeing" and found none of the
5 disagreements, so it is not used as a measurement and the paper reports the hand-labelled shares. *If asked why
report a failure:* the course asks for every model number to be checked against labels we read; this is that check,
and 100 labels with 5 disagreements are too few for a word-count model.

**S2, speaker check.** The data credits each floor speech to a member. We drew 60 speeches at random and compared
the assigned member with the name the Congressional Record prints before the speech. All 60 were right (95%
interval 94% to 100%). Claude extracted the printed names to save time; Diego compared them and wrote every y/n.

**AI methods.** [`AI_METHODS.md`](AI_METHODS.md) is required by the course to be in the repository. It lists every
place a model touched a result in the project (all three members), and how it was checked. It moved here from
Anas's task list on 22 November. Before hand-in it is copied to `docs/AI_METHODS.md`.

## Files that are not obvious

- `d1_matcher_precision/CHECK.md` and `labels.csv`: the 100 matches with Claude's labels and Diego's check.
- `d2_labelling/sheets/`: the filled-in coding sheets, one per coder; `sheets/ai/` holds the three extra AI runs.
  `D2_coding_sheet.xlsx` (20 rows) and `D2_full_sheet.xlsx` are earlier versions of the same sample.
- `d2_labelling/labels_final.csv`: one row per mention with every coder's code; the input to Figure 2 and D5.
- `s2_speaker_check/speaker_check_with_headings.xlsx`: the 60 speeches with Diego's y/n.

## To rerun

From `project/`, with pandas, pyarrow, openpyxl, scikit-learn and matplotlib:

```
python Diego/d1_matcher_precision/score.py          # D1 numbers
python Diego/d2_labelling/agreement.py              # D2 agreement and shares, writes labels_final.csv
python Diego/d2_labelling/figure2.py                # Figure 2 into report/figures/
python Diego/d5_classifier/classify.py              # D5
```
