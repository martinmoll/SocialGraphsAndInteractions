# Archive: how the direction was chosen

Everything here is from **before 13 November 2026**, when the group settled on "Two maps of Congress"
(see [`../README.md`](../README.md)). Nothing in this folder is the current plan. It is kept because the
course advises keeping the roads not taken, and because `docs/AI_METHODS.md` has to describe how AI was
used along the way.

**The files are unchanged.** Paths inside them refer to where they used to live, directly in `project/`.
To rerun an archived notebook, copy it back to `project/` first: it reads `data/processed/` relative to
that folder. The pilot scripts take the data folder as an argument and run from `project/` as
`python archive/Anas_Claude/pilot/<script>.py data/processed`.

| File | What it is | Date | Still worth knowing |
|---|---|---|---|
| `walk_or_talk_outline.md` (was `readme.md`), `walk_or_talk.ipynb`, `figures/fig1`–`fig4` | First question: did Republicans who cooperated or sounded less partisan run ahead of their district? | 11 Nov | Data sources, addresses and known gaps (sections 4 and 8). District lean explains 83% of margins, so the election is a poor outcome |
| `martin_work_plan.md`, `martin_blocs.ipynb`, `martin_blocs.html`, `martin_blocs_template.html` | Second question: blocs inside the Republican party | 11 Nov | The disparity-filter backbone and the rewired null, reused in the prototype. State alone explains 66% of running ahead |
| `research_questions_rating_and_proposals.md`, `Anas_Claude/` | Ratings of every question, four pilots, and proposal P1 (which working relationships do members show their voters?) | 12 Nov | Pilot 4.1: use counts, not the cross-party *share* over time. P1 is now the close-up. `press_pull.py` is the starting point for the collector |
| `martin_council_review.md` | Review of P1 by five AI reviewers: the vote, the recommendation, three fixes, the prototype result | 13 Nov | Section 5 has the full reasoning for the three fixes. Section 8 lists what is unverified |

Not in this folder: Diego's direction ("Running from Trump?") is in `Diego_Claude/` on the branch
`diego-claude-research-question`. A citation-network prototype is on the branch `final-project-prototype`.
