# Methods: data, name matching and networks (Martin's part)

Martin with Claude, 22 November 2026. **Text for the Overleaf draft due Tue 24 Nov.** About 620 words. The paper's
Methods budget is 1.25 pages for everything, shared with Diego (labelling, classifier) and Anas (press releases), so
expect to cut this to about 400 words when the three parts are put together: the bracketed sentences are the first
to go or to move to the SI. Square brackets name the source of each number or choice; delete them in Overleaf.

---

**Data.** Members are the 450 Republicans and Democrats who served in the 119th House, identified by Bioguide ID
(Voteview, with unitedstates/congress-legislators for names). Floor speech comes from the Congressional Record on
govinfo.gov, 6 January 2025 to 9 November 2026, split into speaker turns; we keep the 17,824 House-floor turns of at
least 50 words spoken by a member. Bills and cosponsorships come from govinfo's BILLSTATUS bulk data for the same
Congress. [scripts/01, 02, 04] (Whether each turn is attributed to the right speaker was checked on a sample of 60
turns: S2, result to fill in.)

**Finding names.** A rule-based matcher finds each member named in a turn: a House title followed by a surname ("Mr.
Cole", "Chairman Cole", "Speaker Johnson"), names in lists after a plural title ("Representatives Lawler, Golden, and
Fitzpatrick"), and full names without a title ("my friend, Chip Roy"). Shared surnames are settled by first name
(official or nickname) and then by a state name within 80 characters; otherwise the name is dropped. Possessives and
middle initials are read through; names after "State", "Senator", "Governor" and similar titles are skipped. A member
naming themselves is not counted. On 100 hand-labelled mentions, 98 named the right member (precision; Diego's
sample, drawn before lists and untitled names were added; those two forms were checked separately, 20 of 20 and 30
of 30 right); in 30 randomly drawn turns, the matcher found 12 of the 13 members a reader found (recall, 92%). The one
miss was an unresolved shared surname. [Martin/matcher.py; DECISIONS G10, G14, G18, G19]

**Yields.** When a floor manager hands debate time to a member ("I yield 2 minutes to the gentleman from Texas"),
the name is procedure, not a choice to name someone. We flag a mention as a yield when "yield" (not "yield back")
precedes the name in the same sentence, or "for yielding" follows it, and leave yields out of the headline floor map.
On 30 held-out mentions where this rule and a simpler 60-character window disagreed, all 15 mentions only our rule
flagged were yields, and 14 of the 15 only the window flagged were not. [DECISIONS G1b, G1c]

**The two maps.** Both maps are undirected and unweighted, on the same members. Floor: two members are tied if either
named the other at least once (3,970 ties from 8,469 mentions without yields). Working: two members are tied if one
cosponsored a bill or joint resolution that the other sponsored, withdrawn cosponsorships removed (46,513 ties).
Because the working map is about twelve times denser, we compare the floor map with 200 random draws of working ties
of the same size, and separately with the 3,970 strongest working ties (pairs sharing the most bills). [G1a]

**Division and nulls.** We measure division by party as the share of ties that cross the aisle and as modularity Q of
the party split. Each map is compared with three nulls: (i) degree-preserving rewiring (double-edge swaps, five per
tie, 200 rewirings; 20 for the full working map), which keeps how many ties each member has; (ii) for the floor map,
a shuffle of who is named within each debate (one Congressional Record item; five swaps per mention, 200 shuffles),
which keeps who speaks and who is named in each debate; and (iii) a rewiring that also keeps each member's number of
ties within their own state (200 draws). Seed 2805 throughout. [M3, M4; G16]

**Communities.** We find communities with the Louvain method (resolution 1, 50 random starts, keeping the partition
with the highest modularity) and compare them with party, and between maps, by normalised mutual information. To ask
what the floor communities are, we use current House committee assignments (unitedstates/congress-legislators,
downloaded 22 November 2026) and count the floor ties that join two members of the same full committee, against the
same degree-preserving rewiring. [M5; G15]

---

## Notes for us (not for the paper)

- **Not checked yet:** speaker attribution (S2, 60 turns in `data/processed/speaker_check_sample.csv`). Nobody has
  started it. If it isn't done, the sentence in brackets must say so instead of giving a number.
- **Limits to state here or in the Discussion:**
  - committee lists are today's, not the start of the term;
  - the floor map is unweighted, so a pair named once counts like a pair named fifty times (the reason for G1a);
  - matcher recall rests on 13 names (interval 67% to 99%);
  - shared surnames with no first name or state nearby are dropped (828 titled names in all).
- **M6 belongs in Anas's part of Methods:** own bills = sponsored hr/hjres; cross-party = an original cosponsor of
  the other party; announced = cited in the member's releases (A3.5); within-member shuffle of the cross-party
  label, 10,000 shuffles. [G20]
- **References** (Martin's methods): modularity (Newman 2006) and double-edge swaps (Maslov and Sneppen 2002) are
  already in `Diego/references.bib`. **Missing, to add:** Louvain (Blondel et al. 2008) and NMI (Danon et al. 2005).
