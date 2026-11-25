# Methods from outside the course: inventory, references and why each one is needed

Anas with Claude, Mon 23 Nov 2026. **Status, 25 Nov: done.** `holm1979`, `wilson1927`, `cohen1960`, `cook2025pvi`,
`wikipedia2025pvi` and `downballot2024` are in `report/references.bib` and cited in the text (Holm in
`methods_press.tex`; Wilson at its first use in Martin's Methods; Cohen at Diego's κ). The home map and A5 are in the
paper (25 Nov), so Holm stays. The "Cited?" column and the to-do list at the end describe 23 Nov and are kept as the
record. Use this file as the answer to "why did you use X?".
Purpose: every method we use that the course pages do not teach should be (1) cited, (2) documented, and (3) argued
for, as a complement to a course method, not as something added for its own sake.

## How this was checked

- **The curriculum:** the eight week pages (`sunelehmann.com/socialgraphs2026-web/weeks/week1–8.html`), fetched
  23 Nov 2026 and searched for each method's name; every hit was read in context (e.g. "Holm" on week 2 is Petter
  Holme, "Wilson" is Ken Wilson's renormalization group: neither is the method).
- **Our project:** every `.py`, `.md`, `.tex` and `.bib` in the repo's `project/` (GitHub `main`, `ead58176`) and
  in the local `Anas/` folder, `archive/` left out.
- **References:** each looked up in Crossref or OpenAlex and its DOI resolved at doi.org, 23 Nov. None is from memory.

## A. Outside the course and in the paper: need a citation and a sentence of reasoning

| # | Method | Where (owner) | In the paper now | Cited? |
|---|---|---|---|---|
| A1 | **Wilson score interval** for a proportion | Every hand or reader check: Diego's labels (`methods.tex`, Figure 2 caption), Martin's speaker check (S2, 60 of 60), Anas's A3 and A5 checks | Yes, three places | **No** |
| A2 | **Holm's correction** for many tests | Home map, exposed vs safe on 10 measures (`a4/NETWORK_METHODS.md` §3) (Anas) | Results part 3 ("Holm-corrected"), `methods_press.tex` | **No** |
| A3 | **Cohen's κ** (and the Landis–Koch labels) | Labelling agreement (Diego, S1) | Yes (`results.tex`, `methods.tex`) | κ **no**; Landis–Koch yes (`landis1977`) |
| A4 | **Leave-one-out cross-validation, macro F1, majority baseline** | Classifier check (Diego, `methods.tex`) | Yes | No (not strictly needed, see below) |
| A5 | **Cook PVI** as district lean | Exposure (Anas; `scripts/`) | Yes (`methods_press.tex`, Results part 3) | **No** (a data source, not a method) |

### Why each one is needed, and how it complements the course

**A1. Wilson interval.** *Course method it serves:* week 8 asks that every number a model produced be checked "on
examples you read" (precision, κ). *Gap:* the course reports such checks as bare percentages. Ours are small samples
(30, 60, 100) and often at the edge: 30 of 30, 60 of 60. A bare 100% says nothing about how sure we are. The textbook
normal (Wald) interval fails exactly here: at 30 of 30 it has zero width, and near 0% or 100% it leaves [0, 1].
*Why Wilson:* it stays inside [0, 1], is not zero width at the edges, and holds close to its stated 95% coverage at
small n. That is why 60 of 60 can honestly be reported as "94% to 100%". *Complement, not replacement:* the check is
still the course's (read a sample, count); Wilson only says how far the count can be trusted.
Reference: Wilson, E. B. (1927). Probable inference, the law of succession, and statistical inference. *JASA* 22(158),
209–212. doi:10.1080/01621459.1927.10502953 (Crossref; resolves).
*Proposed sentence (Methods, once):* "Shares from hand or reader checks are given with 95% Wilson intervals, which
stay informative for small samples and for shares near 0 or 100% \cite{wilson1927}."

**A2. Holm's correction.** *Course method it serves:* the course's nulls (configuration model and degree-preserving
swaps, weeks 2–4; permutation tests, week 2 Goodies and week 3) each tell whether *one* statistic is surprising.
*Gap:* the home map compares exposed and safe members on ten measures at once (five measures × two parties). With
ten tests at the 5% level and no real differences, the chance that at least one comes out "significant" is about
1 − 0.95¹⁰ ≈ 40%. The course pages do not discuss testing many statistics together (searched: "multiple test",
"many tests", "multiple comparison": no hits). *Why Holm:* it controls the chance of *any* false positive among the
ten at 5%. It needs no assumption about how the ten tests depend on each other, which matters here because degree,
betweenness and closeness are correlated. It always rejects at least as much as plain Bonferroni (Holm's own result),
so it costs less power. *Complement, not replacement:* each p-value still comes from the course's within-party shuffle.
Holm only decides which of the ten to believe together. *It made a difference:* five of the ten raw p-values are below 0.05, but only three
survive Holm. Republican betweenness (0.010 → 0.059) and closeness (0.008 → 0.055) and the Democrats' betweenness given
degree (0.016 → 0.08) drop out (`NETWORK_METHODS.md` §3d). Without Holm we would have reported all five.
Reference: Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of
Statistics* 6, 65–70. JSTOR stable URL https://www.jstor.org/stable/4615733 (OpenAlex W2121044470; the JSTOR DOI
10.2307/4615733 listed there does not resolve, so the URL is used).
*Proposed sentence (Methods, home map):* "...with Holm's correction over the ten comparisons \cite{holm1979}, which
keeps the chance of any false positive among them at 5% without assuming the tests are independent."
**If the home-map paragraph is cut (G17), Holm leaves the paper with it.**

**A3. Cohen's κ.** *Course:* week 8 names κ as a check ("a hand-labeled sample (precision, κ)"), so the measure is
on the curriculum, but its origin is not cited in our paper. *Why κ and not raw agreement:* with one code at 72%, two
coders who guess from the base rates already agree often; κ removes the agreement expected by chance. Landis and Koch
give the words (moderate, substantial) and are already cited.
Reference: Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*
20(1), 37–46. doi:10.1177/001316446002000104 (Crossref; resolves).
*Proposed:* add `\cite{cohen1960}` at the first "Cohen's $\kappa$" (Diego's text).

**A4. Leave-one-out, macro F1, majority baseline.** *Course:* week 7 trains TF-IDF + logistic regression and asks
for a held-out test set and a baseline. *Gap:* with 100 labels a held-out set (say 20) gives a number too noisy to
read. Leave-one-out uses every label once as test, which is the held-out idea made fit for a tiny sample. Macro F1
because the codes are unbalanced: always guessing the 72% code gets 72% accuracy, and macro F1 exposes that. These
are standard and the text already explains them; a citation is optional. If one is wanted, the software reference:
Pedregosa, F. et al. (2011). Scikit-learn: Machine learning in Python. *JMLR* 12(85), 2825–2830 (checked on jmlr.org;
no DOI). **Diego's call.**

**A5. Cook PVI.** A data source, not a method, but the course's Methods rule asks "what, from where, collected when".
*Why it fits:* "exposed seat" needs a measure of how safe a district is that does not use the member's own vote
share (which would be partly caused by what they do at home, including their press releases). The PVI is built from
presidential votes in the district, so it is fixed before the member acts. The 2024 presidential margin (The
Downballot) is the independent check (r = 0.999). *Proposed:* cite the Cook Political Report's 2025 PVI and the
Wikipedia revision we used (25 May 2025) as a web reference, and The Downballot's 2024 results by district.
(Done 23 Nov: `cook2025pvi`, `wikipedia2025pvi`, `downballot2024` in `report/references.bib`. Cook's date, 3 Apr
2025, comes from Wikipedia's citation only: Cook's own page is behind a subscription.)

## B. Course methods we adapted: say what changed, and why (no new citation needed)

| # | Course method (week) | Our version | Where | Why the change |
|---|---|---|---|---|
| B1 | Configuration model / degree-preserving swaps (2, 3; Maslov–Sneppen, cited) | **Bipartite** version: only R–D ties, swapped so every tie stays R–D | Home map, ties between exposed members (Anas) | The question is about cross-party ties only; an ordinary swap would turn R–D ties into R–R ties and change what is counted |
| B2 | Same | Swaps that also keep each member's ties within their own state | Martin's state null | Members name colleagues from their own state; without this the null would credit that to the map |
| B3 | Label permutation (2 Goodies, 3) | Shuffle **within party** (and within member for M6) | A4 test, home map, M6 | Parties differ in size and in how often they name the other side; shuffling across parties would mix that into the null |
| B4 | Same | **Paired sign-flip** (flip each member's bipartisan − other difference) | A5 (docs only, not in the paper) | Each member gives two shares; flipping the sign is the permutation test for paired data |
| B5 | Week 7 held-out test set | Leave-one-out | Diego (see A4) | 100 labels |
| B6 | Course reads shuffles as z-scores | We report a two-sided permutation p (share of shuffles at least as extreme) | All tests | A p does not assume the null is normal; the course's own permutation logic, read as a share |
| B7 | Betweenness and closeness (3) | Residual after regressing log betweenness on log degree, within party | Home map, 2 of the 10 Holm tests (docs; not reported in the paper) | Betweenness grows with degree; the residual asks whether exposed members broker more than their number of ties predicts. The course's "say compared to what" (week 3), done by regression instead of a null |

## C. Outside the course, documentation only (not in the paper): no citation needed in the paper

| Method | Where | Note |
|---|---|---|
| Bootstrap interval over releases | A3 recall (`a3/README.md`) | Names come in lists, so pairs in one release are not independent; resampling whole releases gives the honest (wider) interval. If it ever goes into the paper: Efron, B. (1979). Bootstrap methods: another look at the jackknife. *Ann. Statist.* 7(1), 1–26. doi:10.1214/aos/1176344552 (Crossref; resolves) |
| Bonferroni | `NETWORK_METHODS.md`, only to explain Holm | — |

## What to do (proposed 23 Nov; all done by 25 Nov, see the status at the top)

1. **Add four checked entries to `references.bib`:** `wilson1927`, `holm1979`, `cohen1960`, and the Cook PVI and
   Downballot web references (once their details are taken from the pages themselves). Draft entries for the first
   three: `references_additions.bib` in this folder.
2. **Anas's text:** add `\cite{holm1979}` and its one-clause reason in `methods_press.tex`. Add the Wilson sentence
   once in Methods (whoever's paragraph comes first).
3. **Diego's text:** `\cite{cohen1960}` at κ; optionally scikit-learn. **Martin's text:** nothing beyond the shared
   Wilson sentence; B2 is already explained there. A message to both, since each writes only in their own folder.
4. **`AI_METHODS.md` (Diego):** unchanged by this; this file is about methods, not AI use.
5. **Presentation:** keep this file as the answer to "why did you use X?"; the A and B tables are the short version.
