# The paper, the slides and what goes with them

Set up by Diego with Claude on 22 November 2026 so that the paper is written in one place in the repository and
then moved to Overleaf. **Anyone, and any of our Claude sessions, may add to it.** Read the rules at the bottom
first.

## What is handed in, and where it is here

Checked against the course pages (front page `#project`, week 8, "The new way of working") on 18 November 2026.

| Hand-in, Fri 27 Nov 23:59, DTU Learn | Rule from the course | Here |
|---|---|---|
| 1. **Paper**, PDF | PNAS template, LaTeX only (Overleaf). At most **6 pages including figures and references**. Sections: Abstract, Significance Statement, Introduction, Results, Discussion, Methods, References, Author contributions. Abstract 150 words. Captions readable on their own. Author contributions specific ("contributed equally" is not accepted). Methods states for the data what, from where, collected when, how many. Every number a model produced is checked on examples we read ourselves, with agreement reported | `main.tex`, `sections/`, `figures/`, `references.bib` |
| 2. **Slides**, PDF | Three pages, one per slide, no animations. Handed in with the paper; the teachers merge all groups' slides, so they cannot change after 27 Nov | `slides/slides.tex` (draft) |
| 3. **Reflection**, PDF | Ungraded. Half a page (week 8: one page at most). Question: did the "From an AI-drafted report" boxes change how you read your own draft, and where did you use them, or not? | `../Diego/reflection_draft.md` (draft, Diego rewrites) |
| In the repository, not uploaded | `AI_METHODS.md`: every place a model touched the results and how it was checked | `../Diego/AI_METHODS.md`; copy to `docs/AI_METHODS.md` before hand-in |

Presentation Wed 2 Dec: three slides, three minutes, then questions to any of us. Everyone must be able to explain
everything in the paper.

## State of each part, 22 Nov

| Part | File | Owner (DECISIONS G3) | State | Words |
|---|---|---|---|---|
| Abstract | `sections/abstract.tex` | Diego, all | First draft on frozen numbers | 148 of 150 |
| Significance statement | `sections/significance.tex` | Diego, all | First draft | 117 of 120 |
| Introduction | `sections/introduction.tex` | Diego and Martin | First draft (Diego with Claude); Martin to revise | 418 |
| Results part 1, two maps | `sections/from_martin_results.tex` | Martin | Generated from `Martin/results_part1.md` | 528 |
| Figure 1 and caption | `figures/figure1.pdf`, `sections/from_martin_caption1.tex` | Martin | Final, copied from `Martin/figures/` | |
| Results part 2, what a mention means | in `sections/results.tex` | Diego | Written | about 250 |
| Figure 2 | `figures/figure2.pdf` | Diego | Made by `Diego/d2_labelling/figure2.py` | |
| Results part 3, close-up | in `sections/results.tex`, `sections/from_martin_m6.tex` | Anas | Placeholder: Anas's A4 wording and Martin's M6 paragraph; Anas to revise | about 200 |
| Figure 3 and caption | `figures/figure3.pdf` | Anas | Draft figure copied from `Anas/a4/out/`; caption missing | |
| Discussion | `sections/discussion.tex` | Diego and Martin | First draft; Martin to revise; S2 sentence missing | 466 |
| Methods: data, matching, maps, nulls | `sections/from_martin_methods.tex` | Martin | Generated from `Martin/methods_networks.md`; S2 result missing | 618 |
| Methods: labelling, classifier | in `sections/methods.tex` | Diego | Written | about 330 |
| Methods: press releases | in `sections/methods.tex` | Anas | Placeholder with the facts to cover | |
| Author contributions | `sections/contributions.tex` | all | Draft; each checks their own line | 145 |
| References | `references.bib` | all | 14 entries, all checked in Crossref | |

**Length.** About 3,100 words of text plus three figures. Six PNAS pages hold roughly 4,000 words with three figures
and the references, so there is little room left: cut, do not add. The Wednesday read-through (25 Nov) cuts to six
pages.

**Still missing:** the S2 speaker check (Diego; one sentence in Methods and one in the Discussion), Anas's part 3
text, caption and Methods paragraph, `\cite` commands in Martin's Methods (Louvain `blondel2008`, NMI `danon2005`,
modularity `newman2006`, rewiring `maslov2002`), and the repository link.

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
- **Budget:** front matter 0.5 page, Introduction 0.75, Results 2.25 with figures, Discussion 0.75, Methods 1.25,
  references and contributions 0.5 (from `../Diego/report_skeleton.md`).
- **Log every change** that affects the paper in `../WORK_AND_DEADLINES.md`, and every new choice in
  `../DECISIONS.md` with its reason.
