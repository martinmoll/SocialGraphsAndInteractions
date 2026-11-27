# commitments.md

## 0) Snapshot
- Title: Two maps of Congress: the House is less divided in whom its members name than in whom they work with
- Authors: Anas Mir, Martin Møllenhus, Diego A. Mijares
- Venue/year: DTU 02805 Social Graphs and Interactions, course paper, 2026 (PNAS template)
- One-line gist: The same 450 House members look less divided by party in whom they name on the floor than in whom they cosponsor with, and cross-party names are mostly credit.
- Paper type (conf/journal/arXiv/other): other (course paper)
- Links present in paper (repo/project/arXiv if present): github.com/martinmoll/SocialGraphsAndInteractions
- Stated page limit (if present): 6 pages

## 1) Talk contract
- Target audience: course teachers and fellow students (network science and NLP literate)
- Assumed prerequisites (1–3 bullets):
  - Modularity, null models, community detection (Louvain, NMI)
  - Basic US Congress vocabulary (cosponsor, floor speech)
- Talk goal (inform/persuade/teach/pitch): persuade (the record you read changes how divided Congress looks)
- Presentation length (minutes): 3
- Target slide count: 3 (course rule: three pages, no animations)
- Style (figure-first / balanced / text-first): figure-first
- Math level (light/medium/heavy): light
- Must-include (2–5 bullets):
  - 38.7% vs 28.6% cross-party ties at equal size
  - What mentions mean: 69% credit, 7% disagreement (100 hand-coded)
  - Debate procedure explains about two thirds of floor division; communities follow committees
  - Exposed seats name the other party more at home (13.3% vs 9.2% R; 11.6% vs 9.0% D)
- Must-avoid (2–5 bullets):
  - Causal claims ("because"); seat and moderation cannot be separated
  - Classifier results as measurements
  - Method detail beyond one line per check

## 2) Core content
- Thesis (1 sentence): How divided the House looks depends on the record read; in whom members name, it is less divided than in whom they work with.
- Key takeaways (3 bullets):
  - Floor map crosses the aisle more than working map at equal size
  - Cross-party mentions are mostly credit, organised by committee
  - At home, members in close seats name the other party most, mostly as partners
- Core contributions (3–5 bullets, ranked):
  1. A new network: who names whom in floor speech, on the same nodes as cosponsorship
  2. Null models separating debate procedure from member choice
  3. Hand-coded meaning of mentions
  4. Press-release close-up on 55,023 releases
- Out-of-scope / de-emphasize (2–4 bullets):
  - Matcher rules, yield detection details
  - Backbone centrality differences between parties
  - Cited-bills analysis

## 3) Narrative spine
1. Congress is described as two camps from votes and words
2. We draw the same 450 members twice: working vs floor
3. Floor is less divided (38.7% vs 28.6%)
4. Is it attack? No: 69% credit; debates and committees structure it
5. At home: exposed members name the other party most, as partners
6. Takeaway: division depends on the record; a name can be checked

## 4) Section plan (light)
| Section (paper heading) | Purpose in talk (short) | Priority (H/M/L) | Suggested slides |
|---|---|---:|---:|
| Introduction | Puzzle and question | H | 0.5 |
| Two maps of the same House | Headline result | H | 0.5 |
| What a cross-party mention means | Meaning + procedure + committees | H | 1 |
| Close-up: whom members name at home | Exposed seats, home map | H | 1 |
| Discussion | Takeaway + caveat | M | 0 (folded into slide 3) |
| Methods | Checks only, one line each | L | 0 |
