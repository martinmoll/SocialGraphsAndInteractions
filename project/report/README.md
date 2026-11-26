# The paper, the slides and what goes with them

Set up by Diego with Claude on 22 November 2026 so that the paper is written in one place in the repository and
then moved to Overleaf. **Anyone, and any of our Claude sessions, may add to it.** Read the rules at the bottom
first.

## The near-final paper: `final_report/`

**Start here.** [`final_report/two_maps_full_draft_overleaf/`](final_report/two_maps_full_draft_overleaf/) is the
near-final six-page paper (25 Nov, DECISIONS G22 and G23): `main.tex` with `main.pdf` beside it, the PNAS class
files, `figures/` and `references.bib`, so the folder compiles in Overleaf as it is
(`final_report/two_maps_full_draft_overleaf.zip` is the same folder zipped for upload). Next to it:
`v2_comments_SGAI_PAPER.pdf` (the group's printed comments on v2, which the cut applied) and `TEXT_TAKEAWAYS.md`
(how much space each section gets, from Sekara et al., PNAS 2016). Martin is giving feedback on `main.pdf`; that
feedback is the next revision. Moved here from `Martin/final_report/` on 26 Nov: it is the group's paper, not one
member's part. The tables below describe the earlier section files in `sections/`, which v2 was built from.

## What is handed in, and where it is here

Checked against the course pages (front page `#project`, week 8, "The new way of working") on 18 November 2026.

| Hand-in, Fri 27 Nov 23:59, DTU Learn | Rule from the course | Here |
|---|---|---|
| 1. **Paper**, PDF | PNAS template, LaTeX only (Overleaf). At most **6 pages including figures and references**. Sections: Abstract, Significance Statement, Introduction, Results, Discussion, Methods, References, Author contributions. Abstract 150 words. Captions readable on their own. Author contributions specific ("contributed equally" is not accepted). Methods states for the data what, from where, collected when, how many. Every number a model produced is checked on examples we read ourselves, with agreement reported | `main.tex`, `sections/`, `figures/`, `references.bib` |
| 2. **Slides**, PDF | Three pages, one per slide, no animations. Handed in with the paper; the teachers merge all groups' slides, so they cannot change after 27 Nov | `slides/slides.tex` (draft) |
| 3. **Reflection**, PDF | Ungraded. Half a page (week 8: one page at most). Question: did the "From an AI-drafted report" boxes change how you read your own draft, and where did you use them, or not? | `../Diego/reflection_draft.md` (draft, Diego rewrites) |
| In the repository, not uploaded | `AI_METHODS.md`: every place a model touched the results and how it was checked | `../../docs/AI_METHODS.md` |

Presentation Wed 2 Dec: three slides, three minutes, then questions to any of us. Everyone must be able to explain
everything in the paper.

## State of each part, 25 Nov

All parts are written on the frozen numbers. The analysis is closed (DECISIONS G21); what is left is the split of
the six pages, the cuts, and the hand-in. Words are counted without LaTeX commands and comments.

| Part | File | Owner (DECISIONS G3) | State | Words |
|---|---|---|---|---|
| Abstract | `sections/abstract.tex` | Diego, all | Draft; does not mention the home map or A5 | 148 of 150 |
| Significance statement | `sections/significance.tex` | Diego, all | Draft | 117 of 120 |
| Introduction | `sections/introduction.tex` | Diego and Martin | Drafted by Diego, revised with Martin | 411 |
| Results part 1, two maps | `sections/from_martin_results.tex` | Martin | Final; generated from `Martin/results_part1.md` | 536 |
| Figure 1 and caption | `figures/figure1.pdf`, `sections/from_martin_caption1.tex` | Martin | Final | caption 139 |
| Results part 2, what a mention means | in `sections/results.tex` | Diego | Final | 265 |
| Figure 2 and caption | `figures/figure2.pdf`, in `results.tex` | Diego | Final; made by `Diego/d2_labelling/figure2.py` | caption 50 |
| Results part 3, close-up | `sections/results_part3.tex` (copy of `Anas/results_part3.tex`) | Anas | Full length on purpose: six paragraphs (main result, closest seats and checks, check T, check I, home map, A5); to be cut at the split | 916 |
| Close-up null (M6) | `sections/from_martin_m6.tex` | Martin | Final | 139 |
| Figure 3 and caption | `figures/figure3.pdf`, in `results.tex` (copy of `Anas/figure3_caption.tex`) | Anas | Final (one column) | caption 197 |
| Discussion | `sections/discussion.tex` | Diego and Martin | Drafted, revised with Martin; mentions check I, not the home map or A5 | 547 |
| Methods: data, matching, maps, nulls | `sections/from_martin_methods.tex` | Martin | Final; generated from `Martin/methods_networks.md` | 639 |
| Methods: labelling, classifier | in `sections/methods.tex` | Diego | Final | 400 |
| Methods: press releases | `sections/methods_press.tex` (copy of `Anas/methods_press.tex`) | Anas | Final at full length, with Martin's M6 sentence (41 words) | 660 |
| Methods: AI use, data and code | in `sections/methods.tex` | all | Final | 57 |
| Author contributions | `sections/contributions.tex` | all | Each checks their own line | 146 |
| References | `references.bib` | all | 21 entries, 20 cited; `landis1977` unused (BibTeX leaves it out) | |

**Length.** About 5,400 words of text and captions plus three figures. The estimate below is that six PNAS pages
hold roughly 4,000 words with three figures and the references, so about 1,400 words have to go
[UNVERIFIED: the 4,000-word estimate has not been checked by compiling]. Nobody has compiled the paper yet, so the
first Overleaf compile is the real test.

## Moving it to Overleaf

1. In Overleaf, open the PNAS template ("PNAS Template for Research Reports"), which brings `pnas-new.cls`.
2. Upload `main.tex` (replace the template's main file), the folders `sections/` and `figures/`, and
   `references.bib`. Compile.
3. From then on, either edit in Overleaf and copy changes back here, or keep editing here and re-upload. Pick one
   and say which in the group chat; editing both at once loses work.

No LaTeX is installed on Diego's laptop, so this has not been compiled yet. Expect small fixes on the first compile.

## Rules for adding to it (people and Claude sessions)

- **Numbers come from result files, never from memory.** Each number in the text must be traceable to a file in
  someone's folder (`m3_table.csv`, `RESULTS.md`, ...). Numbers are frozen since Sun 22 Nov (G7): change one only
  to fix an error, and log it in `../WORK_AND_DEADLINES.md`.
- **Write in your own section.** Martin's text is generated: edit `Martin/results_part1.md` or
  `Martin/methods_networks.md` and run `python report/md2tex.py` from `project/`, or move the text into
  `sections/results.tex` and stop regenerating it. Say which in the log.
- **Course style:** plain, understated, no claim stronger than its check. "Consistent with", not "because". Every
  model-made number reported with its check.
- **Budget** (planned 22 Nov, from Diego's report skeleton, since removed): front matter 0.5 page, Introduction
  0.75, Results 2.25 with figures, Discussion 0.75, Methods 1.25, references and contributions 0.5.
- **Log every change** that affects the paper in `../WORK_AND_DEADLINES.md`, and every new choice in
  `../DECISIONS.md` with its reason.
