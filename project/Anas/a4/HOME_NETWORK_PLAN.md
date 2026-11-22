# A4 extension: the home network of cross-party showing (design, fixed before computing)

Anas with Claude, Sat 21 Nov 2026, evening. **Written before any of these numbers was computed.**

**Scope.** This builds out "mutual showing": one of the two reasons G13 gives for including Democrats ("when a
Republican shows a Democrat at home, does that Democrat show the Republican back?"). It is also the planned panel
for named showcase ties and mutual pairs (STATUS section 4, A4). It adds a network view of the same data, not a new
data source. **Under G17, Martin and Diego can still say it goes too far.** If so, only the mutual-pair sentence
from A3.7 stays.

**Questions (Anas, 21 Nov):**
1. Do exposed members form a cross-party network of their own: do they name exposed members of the other party
   more than chance?
2. Is that showing mutual?
3. Do safe members, by contrast, cross the aisle mainly to members of their own state's delegation?

## The network

- **Nodes:** the 406 members in the A4 test (R or D, with a 2025 lean and at least 10 releases). Each node carries
  its party, `exposed_2025` and its state.
- **A directed tie A → B:** A named B in at least one release in the window (`a3/out/mentions_press.parquet`;
  counted mentions, once per release). Party leaders as the named member are left out, as in the A4 outcome.
  **Co-leads are kept**: showing a partner on a shared bill is showing them.
- **The cross-party network:** the ties between a Republican and a Democrat. For questions 1 and 3 it is taken
  undirected (a tie if either names the other).

## Statistics and the null (all fixed now)

| # | Statistic | Reading |
|---|---|---|
| S1 | **Exposure assortativity** of the undirected cross-party network, attribute `exposed` (networkx `attribute_assortativity_coefficient`; course week 3, mixing) | > 0: exposed members' cross-party ties go to exposed members more than chance |
| S2 | **Share of cross-party ties joining two exposed members**, and its ratio to the null mean | The same in plain terms: "x% of cross-party ties join two exposed members, y times what chance gives" |
| S3 | **Reciprocity of exposed–exposed cross-party ties minus reciprocity of all other cross-party ties** (directed: the share of A → B with B → A too) | > 0: mutual showing concentrates among exposed members |
| S4 | **Same-state share of cross-party ties, safe speakers minus exposed speakers** (directed ties, by the speaker's exposure) | > 0: safe members cross the aisle more to their own state's delegation (question 3) |

**The null, one for all four:** `exposed_2025` shuffled among the members of each party, as in the A4 test. The
network, every tie, party and state stay fixed. 10,000 shuffles, seed 2805, two-sided p.

This asks whether the exposed label sits where the ties are more than chance would put it. It holds each member's
number of ties fixed, so "exposed members simply name more people" cannot by itself produce S1 or S2. One caveat:
exposed members do have more cross-party ties (A4), so S2's expected value is computed under the same shuffle, not
from group sizes.

> **Correction, added after the results (21 Nov):** the sentence above is wrong for S2 and S3.
> - **Why:** shuffling the label within party moves "exposed" from members with many cross-party ties to members
>   with fewer. So S2 can exceed this null just because exposed members are hubs.
> - **S1 is not affected:** assortativity compares against each group's share of tie ends, so it corrects for this.
> - **The fix:** a degree-matched null, shuffling within party and within quintiles of cross-party degree. It was
>   added and is **reported as post hoc**, next to the planned test (`home_network_posthoc.py`).
> - **Second correction:** the quintile bins are too coarse, and their ×1.11 is leftover hub effect. The
>   activity-only expectation, the product of each party's exposed share of tie ends (10.9%), matches the observed
>   10.8%.
> - **The reading that applies, as fixed above:** "S1/S2 not significant: exposed members name the other side more,
>   but not each other in particular". S1, which corrects for activity, was null from the start.

**Robustness (fixed now):**
- ties that need at least 2 releases;
- co-leads left out of the ties;
- the cut-offs 4 and 6.

**Figure (planned):** the cross-party network with Democrats in a left column and Republicans in a right column.
Each member is placed by their lean toward their own party, crossover and close seats at the top and the safest at
the bottom. Exposed members are filled and safe members hollow. Mutual ties are drawn darker. If exposed members
form a network of their own, the top of the figure carries a dense band of ties.

**How the result will be read** (fixed now):
- **S1/S2 positive and significant:** exposed members show each other across the aisle. They form a cross-party
  club of the vulnerable.
- **S1/S2 not significant:** exposed members show the other side more (A4), but not each other in particular.
- **S3:** whether that showing is mutual.
- **S4:** whether safe members' crossing is local, to their own state, rather than to people in their position.
- Wording, as in A4: "consistent with", never "because".

---

# Addendum: null model, centrality, communities (design, fixed before computing)

Anas with Claude, Sat 21 Nov 2026, late evening. **Written before any of these numbers was computed**, after the
S1–S4 results above were known. Course weeks 2 (random network models), 3 (centrality) and 4 (communities).
**New analysis after the G17 scope freeze, for Martin and Diego to accept or cut.**

The network is the one used above: 406 members, a tie when one named the other in a release (leaders as the named
member left out, co-leads kept). The full home map has every tie, weighted by decision 8's 1/n weights; the
backbone is the disparity filter at α = 0.01 (`figure_home_map.py`).

**N1. Null model (week 2).** The question is whether exposed members prefer each other across the aisle, beyond
their activity.
- **Model:** degree-preserving rewiring of the cross-party ties. Each swap exchanges the Democratic ends of two R–D
  ties, so every member keeps their number of cross-party ties and every tie stays cross-party. 10 swaps per tie,
  1,000 rewirings, seed 2805.
- **Measured:** S2 (the share of cross-party ties joining two exposed members) and S1 (assortativity), observed
  against the rewired distribution.
- **Why not Erdős–Rényi:** it erases the differences in activity, which are the finding. The configuration model
  holds them fixed. It is also the null Martin uses in part 1.

**N2. Centrality (week 3).** Computed on the backbone, which is sparse enough for paths to mean something. On the
full map most members are two steps apart.
- **Measures:** degree (all ties), cross-party degree (full map), betweenness (unweighted, normalised) and closeness.
- **Test:** for each measure and each party, exposed mean minus safe mean, with the A4 permutation (exposure
  shuffled within party, 10,000, seed 2805).
- **Betweenness given degree:** betweenness rises with degree, so it is also compared through the residual of
  log(betweenness + 1e-6) on log(degree) within each party. This asks whether exposed members broker more than
  their number of ties alone would give.

**N3. Communities (week 4).**
- **Method:** Louvain on the full weighted home map, resolution 1, 50 seeds, best partition kept (as in Martin's
  G15).
- **Reported:**
  - the number of communities and their modularity;
  - NMI between the communities and party;
  - the modularity Q of the party split itself, for comparison with part 1's floor (0.106) and working (0.211)
    maps. These are not on equal footing: different tie definitions and densities.
- **Where exposed members sit:** for each member, the share of their community that belongs to the other party.
  Exposed against safe within party, same permutation.

**Reading, fixed now:**
- **N1:** S2 within the rewired range means no preference beyond activity (expected from the tie-end check).
- **N2:** higher betweenness for exposed members, also given degree, supports "bridges". Higher only before the
  degree adjustment means they are bridges because they have more ties.
- **N3:** communities near the party split (high NMI) with exposed members in mixed communities would place them at
  the seam, as the layout suggests.

**Result of the addendum (21 Nov, late; numbers in `a4/README.md`).** The 22 Nov rerun on Martin's new matcher
moves these slightly (S2 10.7% against 10.2%, p 0.015; NMI 0.20; the close-seat community 35 members, 19 exposed);
every reading holds. Old against new: `../RERUN_22NOV.md`.
- **N1:** S2 is above the rewired range: 10.8% against 10.3% (9.9 to 10.7%), p 0.025. By the reading fixed above,
  this is a small preference beyond activity, about 5%. It also corrects the earlier tie-end shortcut, which gave
  "no preference".
- **N2:** exposed Republicans are more central because they have more ties. Exposed Democrats have more betweenness
  given their ties (p 0.02). Tentative, with 10 comparisons.
- **N3:** 11 communities, NMI with party 0.22. Exposed members sit in more mixed communities. One 37-member
  bipartisan community is half exposed members.
