# Paper V1: the brief it was written to

Martin with Claude, 24 November 2026. V1 is Martin's own full draft of the paper, written to fit the six pages, so
that the group can compare it with the shared draft in `../../report/` at the read-through on Wed 25 Nov. It does not
replace that draft; the group decides which text goes in.

## What the lecturer asks (course pages, read 24 Nov 2026)

From week 8, sections 2, 6 and 7, and the front page's project box.

- **Why the format:** it grades two things, "can you pick an interesting problem" and "can you communicate it
  clearly". "A reader who sees six pages of everything can easily tell that you didn't focus." Two or three figures
  carry the story.
- **Sections:**
  - **Abstract:** 150 words. The question, the data, the main result with a number, and what it means. Write it last.
  - **Significance statement:** two or three sentences for a reader outside the field.
  - **Introduction:** the question, why it is interesting, what is known, and a one-sentence preview of the answer.
    Cite the work we build on.
  - **Results:** carried by the figures. Each figure answers one part of the question, has a caption that reads
    on its own, and shows the check next to the claim.
  - **Discussion:** what the result means, what it does not mean, and a limitation we found ourselves.
  - **Methods:** enough to redo the work. The data (what, from where, when, how many), every choice that could
    change a number, and each measurement and each validation with its result.
  - **Author contributions:** specific to each person.
- **Rules that apply to every analysis:**
  - one sentence on what it captures and one on what it misses;
  - a check next to every number a model produced, with the agreement reported.
- **What makes an analysis convincing:** a clear question, a measurement that fits it, a check that it works, a
  comparison that rules out the boring explanation, and a limitation found by ourselves.
- **Grading:** one 0–3 score for paper and presentation together, on eight categories. They are the research
  question, data and scope, showcasing the course, analysis and checks, figures, references, overall impression
  ("one story, told well"), and presentation and questions.
- **Not yet seen:** the lecturer's video on the anatomy of a paper (youtube.com/watch?v=vtppZ3wDVGs), which he says to
  watch before writing. Martin to watch.

## Martin's choices for V1 (asked and answered 24 Nov)

| Question | Choice |
|---|---|
| The one sentence a reader repeats | **The record decides:** how divided the same House looks depends on which record is read |
| Part 3 (press releases) | **A short third section**, about half a page with Figure 3: exposed members name the other party more at home, with the ideology caveat; M6 in two sentences. The home network and "bipartisan" stay in the repository and the Q&A |
| Length | **Fits six pages:** about 4,000 words with three figures |
| Where decisions are defended | **Inline:** each choice gets one "because" clause in Methods, each measurement a "captures / misses" sentence; the full record stays in `DECISIONS.md` for the oral |
| The press record's different measure | **Say it openly:** it asks a different question of a third record, and is not on Figure 1's scale |
| Debate procedure (two thirds of the floor map's division) | **Part of the finding:** each record has rules that shape how divided it looks |
| Literature gap | **Measurement:** division depends on the record (Harbridge 2015, Green et al. 2024); we add a record of named colleagues, on identical members, with the same nulls |
| Figures | **The existing three:** two maps against nulls; what cross-party mentions do; exposed against safe at home |
| Reader | The professor and the TAs: networks and NLP known, Congress mechanics explained in a clause |
| The NLP side | **The matcher as entity extraction** (text to network), validated by precision, recall and hand checks; hand labels as the reading check; the failed classifier in one sentence |
| Numbers in Results | **A claim with its one check**; other robustness numbers go to Methods or captions |

## Still open for the group

- Author order and lead author (the shared draft has Mir, Møllenhus, Mijares).
- Whether the home network and the "bipartisan" check (Anas, G17) get a sentence.
- No LaTeX check against the real `pnas-new.cls`: V1 compiles with a stand-in class here, so check page length in
  Overleaf.

## Files and how to use them

- `main.tex`: the whole paper in one file (about 3,850 words: abstract 150, Introduction 380, Results 1,450 with
  captions, Discussion 490, Methods 1,160). Each number has its source file in a `%` comment.
- `figures/` and `references.bib`: copies from `../../report/`, so the folder uploads to Overleaf as it is.
- In Overleaf: open the PNAS template, replace its main file with `main.tex`, upload `figures/` and `references.bib`.
- Checked 24 Nov with a stand-in for `pnas-new.cls` (same page size, columns and type size; not the real class): no
  errors or undefined references, 6 pages with about four fifths of the last page free. The shared draft in
  `../../report/` gives 7 pages on the same stand-in. Methods uses a plain `\section*`, not `\matmethods`, so it
  works with either version of the template.
