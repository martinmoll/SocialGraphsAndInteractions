# NOTES — Bridge topics in a research field (prototype, 11 Nov 2026)

Question: which topics connect citation communities that rarely cite each other, and do they
differ from the topics inside the communities?

Two candidate fields have been run through the same pipeline: **energy systems** and **ocean science**.
The field is not decided yet.

## Run it

```
python src/collect.py FIELD 3000      # FIELD = energy_systems or ocean_science
python src/pipeline.py FIELD 100      # 100 = number of null runs
```

Then open `explorer_FIELD.html` by double-click.

| Output | Path |
|---|---|
| Raw OpenAlex pages (read-only) | `data/raw/openalex_FIELD_DATE_n3000.json` |
| Node table, edge lists, metrics, topic samples | `data/processed/FIELD/` |
| Explorer | `explorer_energy_systems.html`, `explorer_ocean_science.html` |

To add a field, add one line to `FILTERS` in `src/collect.py` and, if needed, its stop words to `FIELD_STOP`
in `src/pipeline.py`. Nothing else is field-specific.

## First numbers

| | Energy systems | Ocean science |
|---|---|---|
| Works matching the query in OpenAlex | 47,658 | 118,748 |
| Works collected (the most cited) | 3,000 | 3,000 |
| Citation range of the sample | 111 – 4,387 | 90 – 2,607 |
| With an abstract in OpenAlex | 1,292 (43%) | 2,312 (77%) |
| Citation edges inside the sample | 11,569 | 13,462 |
| Largest connected component | 2,463 papers, 11,469 edges | 2,819 papers, 13,418 edges |
| … of which with abstract | 981 | 2,189 |
| Coupling edges (≥ 5 shared references) | 12,335 | 36,296 |
| Coupling density | 0.0027 | 0.0081 |
| Louvain communities | 13 | 19 |
| Modularity, real | 0.619 | 0.698 |
| Modularity, 100 rewired nulls | 0.290 ± 0.003 | 0.288 ± 0.003 |
| Stability over 10 seeds (mean pairwise NMI) | 0.70 | 0.77 |
| Papers with ≥ 5 links (eligible) | 1,557 | 2,024 |
| Bridges (top 10% participation among eligible) | 155 (P ≥ 0.66) | 202 (P ≥ 0.63) |
| Review-like titles: bridges vs eligible | 39% vs 23% | 3% vs 3% |
| Papers with participation ≥ 0.6: real vs null | 253 vs 1,333 ± 22 | 250 vs 1,721 ± 44 |
| NMI citation communities vs LDA topics | 0.29 | 0.34 |
| NMI citation communities vs LSA k-means | 0.31 | 0.40 |
| NMI citation communities vs OpenAlex topic | 0.39 | 0.44 |
| NMI LDA vs LSA k-means | 0.35 | 0.46 |
| NMI shuffled baseline | 0.01 | 0.01 |
| Edges pointing to a newer paper | 19 | 29 |

Topics on bridges (z against the 100 nulls; second z drops review-like papers):

Energy systems
- Over-represented: smart grid / future power (+7.0 / +7.0), storage and solar thermal (+3.6 / +3.6),
  learning / forecasting / thermal storage (+3.5 / +5.0), building modelling tools (+4.2 / +1.9).
- Under-represented: hybrid renewable system optimisation (−6.3 / −4.8).
- This fits the hypothesis (bridges carry shared methods and shared problems such as storage), but see the risks.

Ocean science
- Mildly over-represented: phytoplankton / nutrients (+2.3 / +2.0), climate change / warming (+2.2 / +2.1).
- Mildly under-represented: dissolved organic matter / rivers (−2.1 / −2.1).
- No topic passes |z| ≈ 2.3. With 12 topics tested, this is weak evidence: bridge papers here write about
  roughly the same things as the rest of the field.

What the comparison says: ocean science is the better dataset (more abstracts, larger component, stronger and
more stable communities, almost no review papers on the bridges). Energy systems has the stronger finding.
The two samples are defined differently (see "Sample" below), which may explain part of the gap.

## Things that did not go as the handoff assumed

1. **The stop signal is worded the wrong way round.** The real network has far *fewer* high-participation papers
   than the shuffle (energy: 253 against 1,333 ± 22 with P ≥ 0.6; ocean: 250 against 1,721 ± 44). That is what
   strong communities mean: a shuffle destroys the communities, so every paper looks like a bridge. Counting
   bridges against the shuffle cannot show that bridges are "real". The useful test is the one in the chart: do
   the *topics* on bridges differ from the topics on the "bridges" of a rewired network? In energy systems they
   do, clearly. In ocean science they barely do.
2. **Many papers have no abstract in OpenAlex** (publisher restrictions): 57% in energy systems, 23% in ocean
   science. For those papers the text is the title only. This is the largest weakness of the text half in
   energy systems.
3. **No API key was set.** OpenAlex still answers without one, but cursor paging needs a key, so the collector
   uses page-number paging (works to 10,000 results). Search requests cost 10× more of the shared daily budget;
   3,000 works used about a third of it.
4. **Louvain, not Leiden**, and **LSA + k-means, not sentence embeddings**: `leidenalg` and
   `sentence-transformers` are not installed.
5. **Source 2 (conference sessions) is not started.** It needs a cURL from the browser.

## Choices, each with what it captures and what it misses

The numbers quoted in this section are for energy systems unless a line says otherwise. The choices are the
same for both fields, except the sample definition and the field stop words.

**Sample, energy systems.** Articles 2015–2024 with the phrase "energy system" in title or abstract, the 3,000
most cited.
- Captures: the visible core of the field, and it is dense enough to form a citation network without seed expansion.
- Misses: recent papers (127 from 2024 against 416 from 2020), papers that never use the phrase, and anything
  outside the top 6% by citations. Sorting by citations also favours review papers (23% of the papers with
  ≥ 5 links have a review-like title).

**Sample, ocean science.** Articles 2015–2024 whose primary topic sits in OpenAlex subfield 1910
(Oceanography), the 3,000 most cited. Filter: `primary_topic.subfield.id:1910`.
- Why not a phrase search: the phrase "ocean science" matches only 1,145 works, and few papers name their own
  field in the abstract.
- Captures: the most cited 2.5% of what OpenAlex's classifier calls oceanography.
- Misses: the subfield label comes from OpenAlex's topic model, not from a human. Ocean papers that the
  classifier files elsewhere (ocean engineering, marine biology, climate) are left out.
- **The two samples are not defined the same way.** The energy sample is a phrase search and spans several
  subfields; the ocean sample sits inside one subfield. A fair comparison needs one rule for both.

**Field stop words.** "energy", "system", "systems" are dropped for energy systems; "ocean", "oceans", "oceanic"
for ocean science. These words appear in nearly every paper of their field and carry no topic.

**Citation graph.** Edge A → B when A's reference list in OpenAlex contains B; largest weakly connected component only.
- Captures: who builds on whom inside the sample.
- Misses: 537 papers outside the component, and every citation to a paper outside the sample. 19 edges point to
  a newer paper (publication-year noise).

**Coupling graph.** Edge when two papers share ≥ 5 references.
- Captures: papers that draw on the same literature, also when they do not cite each other.
- Misses: the threshold is arbitrary. At ≥ 1 there are 195,336 edges, at ≥ 3 there are 32,246. It is only shown
  in the explorer; no measurement uses it yet.

**Communities.** Louvain on the undirected citation graph, resolution 1, seed 0 as the reference partition.
- Captures: groups of papers that cite each other more than a degree-matched random graph would.
- Misses: modularity says how grouped a partition is, not how correct. Pairwise NMI of 0.70 over seeds means the
  partition moves between runs, so some papers are bridges in one run and not in another.

**Bridges.** Participation coefficient P = 1 − Σ_c (k_c / k)², top 10% among papers with ≥ 5 links.
- Captures: papers whose citation links are spread over many communities.
- Misses: it does not separate "cites widely" (a review) from "is cited from many communities". 39% of bridges
  have a review-like title against 23% of eligible papers. Hubs are not over-represented (7% against 9%).
  The review flag is a regular expression on the title, not a checked label.
- Betweenness is computed from 500 sampled sources, shown in the explorer, and not used in the bridge definition.

**Text topics.** LDA with 12 topics on word counts of title + abstract; each paper gets its largest topic.
- Captures: recurring word groups across the sample.
- Misses: the topics are not named by hand yet (read `data/processed/topic_samples.md`). The topics are
  unstable: adding four stop words ("review", "survey", "overview", "comprehensive") changed which topics came
  out. Storage and smart grid stayed over-represented on bridges and hybrid system optimisation stayed
  under-represented, but the z-values moved. K = 12 is a guess.

**Second text method.** TF-IDF → 100-dimension LSA → k-means with 12 clusters.
- Captures: a grouping that does not depend on LDA.
- Misses: it uses the same words as LDA, so it is not an independent check in the way sentence embeddings would be.

**NMI between groupings.**
- Captures: how much knowing one grouping tells you about the other. 0.29 to 0.39 against a shuffled baseline of
  0.01 means citations and text agree partly, and far from fully.
- Misses: NMI depends on the number of groups, and the title-only papers pull it down (0.33 on abstracts only).

**Null model.** Swap the targets of two citation edges, only when both new edges still point from a newer (or
same-year) paper to an older one and no duplicate appears; 10 attempts per edge; 100 runs; Louvain on each.
- Captures: what degree and publication year alone would produce. Each paper keeps its number of references
  and citations.
- Misses: it removes all topical structure at once, so it is a weak opponent. A stricter null would keep the
  communities and shuffle only the text labels.

**Missing links.** Pairs with high TF-IDF cosine similarity, in different communities, ≥ 3 citation steps apart;
only papers with abstracts.
- Captures: papers that write about the same thing and do not see each other in citations.
- Misses: TF-IDF similarity is shared vocabulary, not shared meaning. Not checked by hand yet.

**Explorer.** One self-contained HTML file with a hand-written canvas renderer.
- Why: it opens by double-click, works offline at the meeting, and needs no server or library. Streamlit would
  need Python running on the presenting machine.
- The layout is for the eye only: links inside a community pull harder, and the dense core is stretched.
  Distances on screen are not measurements.

## Next steps

1. Get an OpenAlex key and set `OPENALEX_API_KEY`.
2. Fill the missing abstracts from a second source (Semantic Scholar or Crossref), and report the match rate.
3. Name the 12 topics by hand from `topic_samples.md`; hand-label about 50 bridges as review / not review.
4. Check that the bridge-topic result survives 10 Louvain seeds and several values of K.
5. Paste the cURL for a conference programme to start source 2.
6. Decide the field. The pipeline re-runs on a new field in about five minutes.
7. If both fields stay in play, define both samples by the same rule (both by subfield, or both by phrase).

## Sources for the Methods section

- OpenAlex: Priem, Piwowar, Orr (2022), arXiv:2205.01833.
- Louvain: Blondel et al. (2008), J. Stat. Mech. P10008. Implementation: networkx 3.5.
- Participation coefficient: Guimerà and Amaral (2005), Nature 433, 895.
- LDA: Blei, Ng, Jordan (2003), JMLR 3, 993. Implementation: scikit-learn 1.9.
- NMI: Danon et al. (2005), J. Stat. Mech. P09008.
- Bibliographic coupling: Kessler (1963), American Documentation 14, 10.

AI use: Claude wrote the collection and pipeline code and this file. No model labelled any data. All numbers above
come from `data/processed/FIELD/metrics.json`.
