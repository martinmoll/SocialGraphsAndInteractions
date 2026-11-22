# Results, part 1: the two maps (DRAFT)

Martin with Claude, 20 November 2026; numbers updated 22 Nov (G18, G19). **Draft for the Overleaf text due Tue 24 Nov, 20:00.** Every number is from
the files named in brackets. **Numbers are not frozen**: they can still move with the hand checks before Sun 22 Nov
(yield rule, G1c; matcher, G14). Rerun the scripts and update the numbers here after the freeze. About 420 words;
the budget is about one page with Figure 1. Brackets [ ] are notes for us, to delete.

---

**Two maps of the same House.** We built two networks over the same 450 Republicans and Democrats of the 119th
House. In the *working map*, two members are tied if one cosponsored a bill or joint resolution the other
sponsored (46,513 ties). In the *floor map*, two members are tied if one named the other in a floor speech, with
yields of debate time left out (3,970 ties from 8,469 mentions; Methods). [m3_table.csv]

**The floor map is less divided by party than the working map.** 38.7% of floor ties cross the aisle. Because the
floor map is thirteen times sparser, we compare it with working ties drawn at random at the same size: across 200
draws, 28.6% of working ties cross the aisle (range 26.8% to 30.6%), and no draw comes within eight points of the
floor map (Fig. 1C). Party modularity tells the same story: 0.112 for the floor map against 0.211 (0.193 to 0.230)
for the draws. The difference is not a by-product of leaving out yields: with yields kept, the floor map is still
at 35.2% against 28.7%. Members' strongest working partnerships are far more partisan still: of the 3,970 pairs who
share the most bills, 12.8% cross the aisle. [m3_table.csv, m3_random_draws.csv]

**Both maps are more divided than chance.** If ties were rewired at random with every member keeping their number
of ties, about half would cross the aisle and modularity would be near zero, in both maps. [m3_table.csv] Floor
debate has its own structure, though: each debate has a cast, often with a manager from each party. When we shuffle
who is named only within each debate, modularity under the shuffle is 0.074 (0.065 to 0.082 over 200 shuffles),
against 0.112 observed. The debates explain about two thirds of the floor map's party division; the rest, members naming
their own side beyond what the debate forces, is larger than in every shuffle. [m4_debate_null.ipynb] Keeping each
member's number of ties to their own state's delegation explains almost none of it (Q 0.001 under that null, at
most 0.023 over 200 draws). [m3b_state_null.csv]

**Communities follow party on one map and committees on the other.** Louvain's communities on the working map are
the two parties (normalised mutual information with party 0.83). On the floor map they cut across party (NMI 0.03,
against 0.29 for working draws of the same size): eight communities of 28 to 80 members, each mixing both parties.
In seven of them one House committee is 3.0 to 7.9 times as common as in the House, among them Appropriations (82%
of the community's members), Ways and Means (79%) and Energy and Commerce (67%); the eighth holds the party leaders.
44% of floor ties join two members of the same committee, against 17.1% when ties are rewired at random, and 50% of
cross-party floor ties do. On the working map the share barely exceeds chance (22% against 18.7%). [m5_table.csv,
m5_committees/]

**What this says.** Members name colleagues of the other party on the floor more often than they cosponsor with them,
and much of that naming runs between colleagues of one committee. Part 2 reads what these mentions say.

---

## Notes for us (not for the paper)

- **Figure 1** is `figures/figure1_draft.png`. The skeleton also asks for a curve of cross-party share against
  ties kept (random against strongest thinning); not made yet.
- **Claims to keep honest:**
  - "less divided" is about who is *named*, not about cooperation (Discussion, and part 2).
  - Committee membership is today's list, not the start of the term (Methods limitation).
  - Committee managers name each other partly because House procedure puts them in the same debates; the debate
    null holds the debate fixed but not the committee.
  - The list fix (G14) raised the floor share by 0.6 points (38.1% without list hits): say so in Methods.
  - Since G19 the floor map counts untitled full names too ("my friend Chip Roy"): 930 mentions, 30 of 30 checked.
- **Methods paragraph still to write** (networks, Martin): tie definitions, the phrase yield rule, random thinning
  with 200 draws, degree-preserving rewiring (5 swaps per tie, 200 rewirings), the debate null, the state null,
  Louvain (50 seeds, best partition kept), NMI, committee data source, matcher precision and recall.
