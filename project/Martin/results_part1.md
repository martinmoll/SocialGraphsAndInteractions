# Results, part 1: the two maps

Martin with Claude, 22 November 2026, on the frozen numbers (after G18 and G19; all hand checks done). **Text for the
Overleaf draft due Tue 24 Nov, 20:00.** About 560 words plus a 150-word caption: probably a little over the budget of about one page with
Figure 1, so expect to cut 100 words at the Wednesday read-through (the committee paragraph can lose its list of
committees, the yields sentence can move to Methods). Square brackets name the file each number comes from: delete them in Overleaf.

---

**Two maps of the same House.** We built two networks on the same 450 Republicans and Democrats of the 119th House.
In the *working map*, two members are tied if one cosponsored a bill or joint resolution that the other sponsored
(46,513 ties). In the *floor map*, two members are tied if one named the other in a floor speech, leaving out
yields of debate time (3,970 ties from 8,469 mentions; Methods). [m3_table.csv]

**The floor map is less divided by party than the working map.** 38.7% of floor ties cross the aisle (Fig. 1A, C).
The floor map is about twelve times sparser, so we compare it with working ties drawn at random at the same size:
across 200 draws, 28.6% of working ties cross the aisle (range 26.8% to 30.6%), and no draw comes within eight points
of the floor map (Fig. 1B, C). Party modularity agrees: 0.112 for the floor map against 0.211 (0.193 to 0.230) for
the draws (Fig. 1D). Leaving out yields does not create the gap: with yields kept, the floor map is at 35.2% against
28.7%. Members' strongest working partnerships are far more partisan still: of the 3,970 pairs who share the most
bills, 12.8% cross the aisle. [m3_table.csv, m3_random_draws.csv]

**Both maps are more divided than chance, and the floor map's division is partly procedure.** If ties were rewired
at random with every member keeping their number of ties, about half would cross the aisle and modularity would be
near zero in both maps (Fig. 1C, D). Floor debate has a structure of its own: each debate has a cast, often with a
manager from each party. Shuffling who is named only within each debate leaves a modularity of 0.074 (0.065 to 0.082
over 200 shuffles) against 0.112 observed. The debates thus account for about two thirds of the floor map's party
division; the rest, members naming their own side beyond what the debate forces, exceeds every shuffle.
[m4_results.csv] State delegations account for almost none of it: keeping each member's number of ties within their
own state gives a modularity of 0.001 (at most 0.023 over 200 draws). [m3b_state_null.csv]

**Communities follow party on one map and committees on the other.** On the working map, Louvain's communities are
the two parties (normalised mutual information with party, NMI, 0.83). On the floor map they cut across party (NMI
0.03, against 0.29 for working draws of the same size): eight communities of 28 to 80 members, each holding both
parties. In seven of them one House committee is 3.0 to 7.9 times as common as in the House as a whole, among them
Appropriations (82% of the community's members), Ways and Means (79%) and Energy and Commerce (67%); the eighth
gathers the party leaders. 44% of floor ties join two members of the same committee, against 17.1% when ties are
rewired at random, and so do 50% of cross-party floor ties. In the working map the share barely exceeds chance (22%
against 18.7%). [m5_table.csv, m5_committees/committee_table.csv]

**In short,** members name colleagues of the other party on the floor more often than they cosponsor with them, and
much of that naming runs between members of the same committee. Part 2 reads what these mentions say.

---

**Figure 1.** The House as two networks, January 2025 to November 2026. (*A*) Floor map: members tied when one names the
other in a floor speech, yields of debate time left out. (*B*) Working map: one random draw of sponsor–cosponsor
ties, thinned to the floor map's 3,970 ties. Nodes are members (red Republican, blue Democrat); purple ties cross
the aisle. Positions come from a spring layout and carry no meaning. (*C*) Share of ties that cross the aisle; the
bar for the random draws shows the range over 200 draws, and the dashed line the level expected if ties were
rewired at random. (*D*) Party modularity of each map (filled) against its nulls (open; lines show the range over
the draws): shuffling who is named within each debate, keeping each member's same-state ties, and keeping each
member's number of ties.

---

## For part 3 (Anas): the M6 paragraph, ready to paste or shorten

**Do members show their cross-party bills at home?** Of the bills a member sponsored, those with an original
cosponsor from the other party were cited in that member's press releases more often than their other bills (52.7%
against 45.1%; 388 members, 10,125 bills). Shuffling, within each member, which bills count as cross-party gives a
null in which the observed count is 1.08 times the expected (p < 0.001), in both parties. Most of the gap, however,
separates co-led bills from solo bills: against bills co-led only by the member's own party, cross-party bills are
cited 3.5 points more often (52.6% against 49.1%, p = 0.02). As original cosponsors, members cite the cross-party
bills they join about three times as often as same-party ones (8.6% against 2.9%). We cannot rule out that
bipartisan bills are cited more because they more often pass. [Martin/m6_results.csv; DECISIONS G20]

---

## Notes for us (not for the paper)

- **Figure 1:** `figures/figure1.pdf` (vector, for Overleaf) and `figures/figure1.png`. Full PNAS width (17.8 cm).
  Rebuilt by `m7_figure1.py` from the result files. The thinning curve from the report skeleton was optional and is
  dropped under the scope freeze (G17): panel C already shows random against strongest thinning.
- **Claims to keep honest:**
  - "Less divided" is about who is *named*, not about cooperation (Discussion, and part 2).
  - Committee membership is today's list, not the start of the term (Methods limitation).
  - Committee managers name each other partly because House procedure puts them in the same debates; the debate
    null holds the debate fixed, but not the committee.
  - Matcher changes and their effect on the headline go in Methods: lists +0.6 points (G14); untitled names, 930
    mentions, 30 of 30 checked (G19); precision 98 of 100, recall 12 of 13.
- **Methods paragraph still to write** (networks): tie definitions, the phrase yield rule (G1c test: 15 of 15),
  random thinning with 200 draws, degree-preserving rewiring (5 swaps per tie, 200 rewirings), the debate null, the
  state null, Louvain (50 seeds, best partition kept), NMI, the committee data source, matcher precision and recall.
