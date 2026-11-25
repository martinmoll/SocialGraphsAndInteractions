# Methods from outside the course: what they are, where we use them, and why

Started by Anas (with Claude) on 23 Nov 2026; **updated 25 Nov 2026 to the final versions of all three parts** and
moved from `Anas/` to the project folder, so any of us can answer "why did you use X?" at the presentation. Every
method in the paper that the course pages do not teach should be (1) cited, (2) described in Methods, and (3)
argued for as a complement to a course method, not added for its own sake.

**State on 25 Nov:** every method from outside the course that the paper uses is cited and described (table A),
and so is every data source. `serrano2009` (the disparity filter) is cited in part 3 and `voteview2026` in the
press-release Methods since 25 Nov. Only `landis1977` sits in `report/references.bib` without a `\cite`: the text
does not use the Landis and Koch words, and BibTeX leaves an uncited entry out.

## How this was checked

- **The curriculum (23 Nov):** the eight week pages (`sunelehmann.com/socialgraphs2026-web/weeks/week1–8.html`),
  searched for each method's name; every hit was read in context (e.g. "Holm" on week 2 is Petter Holme, "Wilson" is
  Ken Wilson's renormalization group: neither is the method).
- **Our project (25 Nov):** every section of the paper in `report/sections/` and the final README of each member's
  folder, at GitHub `main` `876d88cd`. The added rows (B8 to B10) are our own versions of course methods.
- **References:** each looked up in Crossref or OpenAlex and its DOI resolved at doi.org (23 Nov). None is from memory.

## A. Outside the course and in the paper: cited, with a sentence of reasoning

| # | Method | Where (owner) | Cited in the paper |
|---|---|---|---|
| A1 | **Wilson score interval** for a proportion | Speaker check S2 (Martin's Methods, first use), labelling shares (Diego's Methods, Figure 2 caption); Anas's reader checks in the repository | Yes, `wilson1927`, at first use |
| A2 | **Holm's correction** for many tests | Home map: exposed against safe on ten measures (Anas; `Anas/a4/NETWORK_METHODS.md` §3) | Yes, `holm1979`, in `methods_press.tex` |
| A3 | **Cohen's κ** | Labelling agreement (Diego). κ itself is on the curriculum (week 8); its origin is cited | Yes, `cohen1960` |
| A4 | **Leave-one-out cross-validation, macro F1, majority baseline** | Classifier check D5 (Diego, `methods.tex`) | Described, not cited (Diego's call; standard) |
| A5 | **Cook PVI, The Downballot, a pinned Wikipedia revision** (data sources for district lean) | Exposure (Anas) | Yes, `cook2025pvi`, `downballot2024`, `wikipedia2025pvi` |
| A6 | **DW-NOMINATE from Voteview** (data source for ideology and the member list) | Check I (Anas); Martin's Methods names Voteview for members | Yes, `voteview2026` (the citation printed on voteview.com/data, read 25 Nov), in `methods_press.tex` |

### Why each one is needed, and how it complements the course

**A1. Wilson interval.** *Course method it serves:* week 8 asks that every number a model produced be checked "on
examples you read" (precision, κ). *Gap:* the course reports such checks as bare percentages. Ours are small samples
(30, 60, 100) and often at the edge: 30 of 30, 60 of 60. A bare 100% says nothing about how sure we are. The textbook
normal (Wald) interval fails exactly here: at 30 of 30 it has zero width, and near 0% or 100% it leaves [0, 1].
*Why Wilson:* it stays inside [0, 1], is not zero width at the edges, and holds close to its stated 95% coverage at
small n. That is why 60 of 60 can honestly be reported as "94% to 100%". *Complement, not replacement:* the check is
still the course's (read a sample, count); Wilson only says how far the count can be trusted.
Reference: Wilson, E. B. (1927). Probable inference, the law of succession, and statistical inference. *JASA* 22(158),
209–212. doi:10.1080/01621459.1927.10502953.

**A2. Holm's correction.** *Course method it serves:* the course's nulls (configuration model and degree-preserving
swaps, weeks 2–4; permutation tests, week 2 Goodies and week 3) each tell whether *one* statistic is surprising.
*Gap:* the home map compares exposed and safe members on ten measures at once (five measures × two parties). With
ten tests at the 5% level and no real differences, the chance that at least one comes out "significant" is about
1 − 0.95¹⁰ ≈ 40%. The course pages do not discuss testing many statistics together (searched: "multiple test",
"many tests", "multiple comparison": no hits). *Why Holm:* it controls the chance of *any* false positive among the
ten at 5%, needs no assumption about how the tests depend on each other (degree, betweenness and closeness are
correlated), and always rejects at least as much as plain Bonferroni. *Complement, not replacement:* each p-value
still comes from the course's within-party shuffle; Holm only decides which of the ten to believe together. *It made
a difference:* five of the ten raw p-values are below 0.05, but only three survive Holm. Republican betweenness
(0.010 → 0.059) and closeness (0.008 → 0.055) and the Democrats' betweenness given degree (0.016 → 0.08) drop out,
which is why part 3 calls the parties' different bridging roles borderline.
Reference: Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of
Statistics* 6, 65–70. https://www.jstor.org/stable/4615733 (the JSTOR DOI 10.2307/4615733 does not resolve).

**A3. Cohen's κ.** *Course:* week 8 names κ as a check ("a hand-labeled sample (precision, κ)"). *Why κ and not raw
agreement:* with one code at 72%, two coders who guess from the base rates already agree often; κ removes the
agreement expected by chance. The bar (0.6) was set before coding. The text reports κ as a number and does not use
the Landis–Koch words ("moderate", "substantial"), so `landis1977` is not needed.
Reference: Cohen, J. (1960). A coefficient of agreement for nominal scales. *Educational and Psychological Measurement*
20(1), 37–46. doi:10.1177/001316446002000104.

**A4. Leave-one-out, macro F1, majority baseline.** *Course:* week 7 trains TF-IDF + logistic regression and asks
for a held-out test set and a baseline. *Gap:* with 100 labels a held-out set (say 20) gives a number too noisy to
read. Leave-one-out uses every label once as test, the held-out idea made fit for a tiny sample. Macro F1 because the
codes are unbalanced: always guessing the 72% code gets 72% accuracy, and macro F1 (0.26 for our model) exposes that.
If a citation is wanted, the software reference: Pedregosa, F. et al. (2011). Scikit-learn: Machine learning in
Python. *JMLR* 12(85), 2825–2830 (checked on jmlr.org; no DOI).

**A5. Cook PVI and its checks.** A data source, not a method, but the course's Methods rule asks "what, from where,
collected when". *Why it fits:* "exposed seat" needs a measure of how safe a district is that does not use the
member's own vote share (which would be partly caused by what they do at home, press releases included). The PVI is
built from presidential votes in the district, so it is fixed before the member acts. The Wikipedia revision of 25
May 2025 gives the lean of the districts members served, before any 2026 redraw; the 2024 presidential margin (The
Downballot) is the independent check (r = 0.999). Cook's own page is behind a subscription, so its date (3 April
2025) comes from Wikipedia's citation only.

**A6. DW-NOMINATE.** A data source: each member's score from all their roll-call votes, from Voteview (also our
source for the member list). *Why it is needed:* check I asks whether "exposed" is just "moderate", which needs a
measure of how members vote that is separate from their district. *Limit, stated in the paper:* votes may themselves
follow the seat, so holding ideology fixed can remove part of a real seat effect. *Reference:* the
citation Voteview asks for on its data page (read 25 Nov): Lewis, Poole, Rosenthal, Boche, Rudkin and Sonnet (2026),
*Voteview: Congressional Roll-Call Votes Database*, https://voteview.com/.

## B. Course methods we adapted: what changed, and why (no new citation needed)

| # | Course method (week) | Our version | Where (owner) | Why the change | In the paper |
|---|---|---|---|---|---|
| B1 | Configuration model / degree-preserving swaps (2, 3; Maslov–Sneppen, cited) | **Bipartite** version: only R–D ties, swapped so every tie stays R–D and every member keeps their number of cross-party ties | Home map, ties between exposed members (Anas) | The question is about cross-party ties only; an ordinary swap would turn R–D ties into R–R ties | Yes (`methods_press.tex`) |
| B2 | Same | Swaps that also keep each member's ties within their own state (state null) | Part 1 (Martin, on Anas's proposal, G16) | Members name colleagues from their own state; without this the null would credit that to the map | Yes |
| B3 | Same | **Debate null:** who is named is shuffled only within one debate (one Record item) | Part 1 (Martin, M4) | Every debate has a manager from each party; a null that ignores that would credit procedure to the members | Yes |
| B4 | Label permutation (2 Goodies, 3) | Shuffle **within party**; within member for M6 | Part 3 test and home map (Anas); M6 (Martin) | Parties differ in size and in how often they name the other side; mixing them would put that difference into the null | Yes |
| B5 | Same | **Stratified shuffle:** within party *and* ideology band | Check I (Anas) | The course's "compared to what" (week 3): the gap ideology alone would give is the mean of these shuffles | Yes |
| B6 | Same | **Paired sign-flip** (flip each member's bipartisan − other difference) | A5 main comparison (Anas) | Each member gives two shares; flipping the sign is the permutation test for paired data | No (the paper gives the shares; the p is in `Anas/a5/README.md`) |
| B7 | Course reads shuffles as z-scores | A two-sided permutation p (share of shuffles at least as extreme) | All tests | A p does not assume the null is normal; the course's own permutation logic, read as a share | Yes |
| B8 | Betweenness and closeness (3) | Residual after regressing log betweenness on log degree, within party ("betweenness given degree") | Home map (Anas) | Betweenness grows with degree; the residual asks whether exposed members broker more than their ties predict | Yes ("more shortest paths than their ties predict") |
| B9 | Weighted networks and the disparity filter (4) | Tie weight = sum of 1/n over releases naming the pair, n the colleagues each release names | Home map backbone (Anas) | One 40-name signatory list would otherwise outweigh 39 ordinary releases | Described in `Anas/a4/NETWORK_METHODS.md`; backbone named in the text |
| B10 | Logistic regression on TF-IDF (6–7) | Classes weighted by inverse frequency; surname replaced by a placeholder | Classifier D5 (Diego) | Unbalanced codes; the model must not learn members' names | Yes |
| B11 | Week 7 held-out test set | Leave-one-out | D5 (Diego; see A4) | 100 labels | Yes |

## C. Outside the course, documentation only (not in the paper): no citation needed

| Method | Where | Note |
|---|---|---|
| Bootstrap interval over releases | Press recall (`Anas/a3/README.md`) | Names come in lists, so pairs in one release are not independent; resampling whole releases gives the honest (wider) interval. If it ever goes into the paper: Efron, B. (1979). Bootstrap methods: another look at the jackknife. *Ann. Statist.* 7(1), 1–26. doi:10.1214/aos/1176344552 |
| Bonferroni | `Anas/a4/NETWORK_METHODS.md`, only to explain Holm | — |
| Blind AI readers and AI coders | Diego's D2, Anas's A3, T and A5 checks | An AI method, not a statistical one: every use and its check is in `docs/AI_METHODS.md` |

## Course methods used as taught (for reference)

Degree-preserving rewiring, party modularity, Louvain communities and NMI, betweenness and closeness, the disparity
filter and ForceAtlas2 (weeks 2 to 4); TF-IDF and logistic regression (weeks 6 and 7); hand-labelled checks with
precision, recall and κ (week 8). Original papers are cited where the paper uses the method (Maslov–Sneppen,
Newman, Blondel, Danon, Fowler, Serrano).
