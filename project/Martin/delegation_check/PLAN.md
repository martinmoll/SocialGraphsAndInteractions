# Delegation check: is "exposed" just "has many colleagues of the other party back home"?

Written 25 Nov 2026 by Martin with Claude, **before running anything**. A post-hoc check: it was not in the A4 plan
(`Anas/methods_drafts.md`), and G21 closed the analysis, so its result goes to the group before anything enters the
paper.

## The worry

Part 3 finds that members in exposed seats name the other party more often in their press releases. Members often
name colleagues from their own state's House delegation (joint letters, a local project, disaster aid). Close
districts tend to sit in states whose delegation is mixed (Pennsylvania, Michigan, New York), so an exposed member
may simply have more other-party colleagues from home to name. Then part of the gap would come from the delegation,
not the district.

## Inputs (frozen, unchanged)

- `Anas/a4/out/member_shares.csv`: the 406 members of the A4 test, with party, state, exposed and share.
- `Anas/a3/out/mentions_press.parquet`: every name found in a release, with `cross_party`, `co_lead`,
  `named_is_leader` and `same_state`.
- `Anas/press_releases/press_releases_part*of3.parquet` and `Anas/a3/out/release_flags.parquet`: the releases, to
  recompute the share with a different set of names.
- `data/processed/members.csv`: party and state of the 450 Republicans and Democrats who served in the 119th House.

## Delegation measures

For each member: `opp_n`, the number of House members of the other party from the same state (all 450 who served,
since any of them could be named), and `opp_share`, `opp_n` divided by the rest of the delegation (members of the
same state minus the member). Robustness: the same counted on members still serving (`current`).

## Tests (statistic: A4's gap, exposed minus safe mean share, within each party)

0. **Reproduce** A4's main gaps from the inputs (R 4.08, D 2.58 points). If they don't reproduce, stop.
1. **Overlap.** Mean `opp_n` and `opp_share` for exposed and safe members, by party. If exposed members do not have
   more other-party colleagues at home, the worry has no material and the rest is a formality.
2. **Where the names go.** Of the releases that count as naming the other party, the share whose only counted names
   are same-state members, exposed against safe.
3. **Without same-state names.** Recompute each member's share counting only other-party names from *other* states
   (same rules otherwise: no leaders, no co-leads). Gap and within-party permutation p (10,000 shuffles, seed 2805).
4. **Within delegation bands.** As check I (`Anas/a4/ideology_check.py`): exposed shuffled only within party and band
   of `opp_share` (quintiles; terciles as robustness; tied values kept in one band, so fewer bands if needed).
   The shuffles' mean is the gap the delegation mix alone gives; p = share of shuffles at least as far from that
   mean as the observed gap. Also with `opp_n` bands.
5. **Both at once.** Test 4's bands on test 3's outcome.

## How the result will be read (fixed now)

- The gap **survives** if, in both parties, test 3 keeps a gap with p < 0.05 and test 4 leaves most of it (more than
  half) beyond what the delegation mix gives, with p < 0.05.
- The delegation **explains** the gap if test 4 leaves a remainder that cannot be told from chance; then the paper
  must say, as for ideology, that seat and delegation cannot be separated.
- Anything in between is reported as it is, by party.

## Results (run 25 Nov 2026, after the plan above; `delegation_check.py`, full readout in `readout.txt`)

0. A4 reproduces from the inputs: 406 members, gaps R 4.08 and D 2.58 points.
1. **Overlap.** Exposed Republicans do have more Democrats in their home delegation than safe Republicans (8.9
   against 6.6; share 0.45 against 0.34). Exposed Democrats do not have more Republicans at home than safe Democrats
   (6.8 against 7.1; 0.37 against 0.34).
2. **Same-state names.** About one counted release in seven counts only because it names an other-party member from
   the same state: R exposed 14.8%, safe 15.2%; D exposed 17.6%, safe 13.7%.
3. **Without same-state names.** R gap 3.74 points (was 4.08), p = 0.003. D gap 1.44 (was 2.58), p = 0.067.
4. **Within delegation bands.** The delegation mix alone gives a gap of about zero (-0.3 to +0.3 points) in every
   variant (opp_share or opp_n, quintiles or terciles, all or current members). What is beyond it is the whole gap:
   R 3.8 to 4.4 points, D 2.6 to 2.8, p between 0.001 and 0.006.
5. **Both.** R 3.7 to 4.3 points beyond, p <= 0.002; D 1.5 to 1.6 beyond, p 0.037 to 0.047.

**Reading (by the rule fixed above).** The delegation mix does not explain the gap in either party: test 4 leaves
all of it. Republicans pass both tests. Democrats are in between: their gap does not come from having more
Republicans at home (they don't), but about 1.1 of its 2.6 points are names of home-state Republicans, and on
names from other states alone the gap is 1.4 points (p = 0.07 within party, 0.04 within delegation bands).

**Limits.** Post-hoc, after G21 closed the analysis; ten variants of test 4 and 5 are reported without a
correction for multiple tests, but they all point the same way. The delegation counts every member who served,
including those who left (the `current` variant gives the same result).
