# Proposal for Martin: a null that keeps members' own states

Anas, 19 November 2026. **A suggestion, not a decision.** Part 1 is Martin's, and so is whether to use this.
If he takes it up, it needs a `DECISIONS.md` entry before the freeze on Sun 22 Nov (G7).

## The suggestion in short

Add one more null to the part 1 table: rewire each map while every member keeps both their number of ties
and their number of ties to members of their own state. It answers a question a reader can fairly ask:
**is part of the party division in the two maps just members working with, and talking about, their own state's
delegation?** States are often lopsided by party (Massachusetts has 9 Democrats and no Republicans, Oklahoma 5
Republicans and no Democrats), so ties inside a state are often same-party ties for reasons that have nothing to
do with party.

The pilot below says the answer is almost certainly no, so this would be one robustness row and one sentence,
not a new result.

## Why it is worth a row

1. **It closes an obvious attack.** The plain rewired null shuffles ties freely across the whole country. A
   reviewer can say real members don't choose partners from the whole country: they know their own delegation
   best, share home-state issues (disasters, military bases, highways) and are often of one party. The debate null
   (M4) answers the same kind of attack for the floor map. This one answers it for both maps.
2. **Same-state ties are over-represented.** In the pilot, 6.7% of working ties and 9.0% of floor ties connect
   two members of one state, against 4.3% and 3.7% when ties are shuffled freely. On the floor, members name their
   own state's members about 2.4 times more often than chance. So state is a real structure in the data, not an
   imagined one.
3. **It costs little.** The function is in `state_null_pilot.py` (about 30 lines) and reads the same inputs as
   `m3_definitions.py`. It runs in under two minutes for both maps.
4. **It ties part 1 to part 3.** Same-state naming is a possible reason why a member names someone in a press
   release (home-state projects). A floor result on state gives part 3 a reference point.

## Pilot (one run, my code, Martin's definitions)

Maps built as in `Martin/m3_definitions.py`: undirected, unweighted, Republicans and Democrats only. Working
map = sponsor-cosponsor pairs on `hr` and `hjres`, withdrawn removed (46,513 ties, Q 0.210, as in M3). Floor map =
the headline map, phrase-rule yields dropped (3,284 ties, 38.6% cross-party, Q 0.111, as in G1b).

| | Working (all ties) | Floor (yields dropped) |
|---|---|---|
| Ties | 46,513 | 3,284 |
| Same-state share of ties | 6.7% | 9.0% |
| Same-state share, plain rewired null | 4.3% | 3.7% |
| Cross-party share of same-state ties | 27.2% | 31.3% |
| Cross-party share of ties between states | 28.8% | 39.4% |
| **Party modularity Q, observed** | **0.210** | **0.111** |
| Q, plain rewired null (mean) | 0.000 | −0.002 |
| Q, state null (mean / largest) | 0.006 / 0.008 | 0.004 / 0.021 |
| Cross-party share: observed / plain null / state null | 28.7% / 49.7% / 49.1% | 38.6% / 49.9% / 49.3% |
| Draws | 10 | 50 |

What it says:

- **State structure explains almost none of the party division.** Keeping everyone's same-state ties moves Q
  from about 0 to about 0.005. The observed maps sit at 0.210 and 0.111. Both maps are more divided than every
  state-null draw.
- **The floor map's same-state ties are more partisan than its other ties** (31% cross-party against 39%).
  Members who name a colleague from their own state usually name one of their own party. In the working map the
  difference is small (27% against 29%).
- Checked: the state null keeps every member's degree and the same-state share exactly (9.04% before and after
  on the floor map), and changes 87% of the ties in a draw.

Pilot numbers, not results: 10 and 50 draws, one seed (2805), my reimplementation. Martin's code is the
reference if he reruns it.

## How to add it

1. Copy `state_rewire()` from `state_null_pilot.py` into `m3_definitions.py` (it needs a `state` Series indexed
   by Bioguide ID, from `members.csv`).
2. In the loop over `LAYERS`, next to `nx.double_edge_swap`, call `state_rewire(G, random.Random(SEED + s))` and
   record `stats(R)` as a second null. Same 200 draws as the plain null.
3. Add two columns to `m3_table.csv`: `Q state null mean` and `cross state null`.
4. Optional: the same idea inside the debate null (M4), shuffling the named ends within a debate only among
   members of one state. Probably not worth it: the floor map's state null is already near zero.

How the swap works: ties are split into one group per state (both ends in that state) and one group of ties
between states. A swap trades ends between two ties of the same group. A swap that would make a tie between
states into a same-state tie is rejected, as are self-ties and duplicates. Every member keeps their degree and
their number of same-state ties.

## How it changes the reading

| If Martin's run shows | Then the paper can say |
|---|---|
| Q under the state null stays near 0 (what the pilot shows) | Party division in both maps is not a state effect. One sentence in Results, one row in the table, and the "members only know their own delegation" attack is answered. |
| Q under the state null is a large part of observed Q | Part of what looks like party division is geography. The headline would be reported net of state, and the Discussion would say so. |
| The two maps differ: state matters on the floor, not in the working map | A finding of its own: members talk about their delegation more than they work with it, and the floor map's division is partly home-state talk. |

Beyond the null, one descriptive line is worth having whatever he decides: on the floor, members name their own
state's members 2.4 times more often than chance, and those mentions are more often same-party.

## What it does not do

- It says nothing about exposure. District lean stays in part 3 (close-up), as agreed.
- It doesn't test the gap between the two maps, only each map's division.
- States are a coarse grouping. Large states (California 52 seats) contribute most same-state pairs; see
  `../state_seats/` for seats per state.

## Files

| File | What |
|---|---|
| `state_null_pilot.py` | Builds both maps as in M3, runs the plain and the state null, prints the table above |

```
python Anas/state_null/state_null_pilot.py data/processed Martin/mentions.parquet
```
