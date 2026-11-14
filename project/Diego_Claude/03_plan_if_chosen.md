# 03 · Plan if the group picks "Running from Trump?"

The division of labour is **not** in this file yet. It will be written once the group has picked a question,
on the same principles as Martin's `work_plan.md` (one stream per person, one shared file joins the
streams, nobody edits another person's notebook, definitions fixed before results are looked at again).

## Definitions to fix before rerunning (proposal)

| Item | Proposal | Why |
|---|---|---|
| Periods | Half-years, plus a two-period early/late split at 1 Dec 2025 for per-member change | Half-years are long enough for per-member rates; the split is pre-shutdown vs election year |
| Baseline periods | The same calendar positions in the 115th Congress (Jan 2017 to Nov 2018) | Like for like within a term |
| Words | Turns of at least 50 words; House floor (H) as main, Extensions of Remarks as a robustness line | Extensions are mostly tributes |
| Trump measure | Whole word "trump" per 10,000 words; robustness: "president trump" only, and excluding bill titles | Bill titles that name him are not a member's own choice |
| Stance | 100 Republican mentions, stratified by period, coded praise / neutral / critical by two people independently; report Cohen's kappa | Week 7 hand-label check |
| Deeds | Cross-party share of cosponsorships by sign date; `hr` and `hjres`; withdrawn dropped; first and last quarter of each Congress reported but not interpreted | Q1 and Q4 are structurally odd in both Congresses |
| Who | Change scores against NOMINATE, lean and Martin's blocs; permutation null (shuffle members' change scores) and bootstrap intervals | Week 2 null |
| Role check | Rerun "who" without committee chairs and party leaders | Floor managers' words follow the schedule |
| Election | Secondary: overperformance vs change scores, with Martin's within-state shuffle | Already known to be weak |

## The three figures (draft)

1. **Words.** Trump rate and share of members naming him, by half-year, 2025-26 against 2017-18, approval as
   a thin line underneath. The claim: Republicans went quiet on Trump, more (or not) than in his first term.
2. **Deeds.** Republican cross-party cosponsorship share by quarter, both Congresses, with the label-shuffle
   null band, and the party-split modularity per period. The claim: Republicans moved toward Democrats in
   deeds, by this much more than in 2017-18.
3. **Who.** One dot per Republican: change in words (x) against change in deeds (y), coloured by bloc,
   swing-seat members ringed, a small inset of overperformance. The claim: the quiet and the crossers are
   different people, and the quiet are the hardline wing.

## Kill tests and gates (reusing the earlier idea-agnostic schedule)

| Date | Gate | Pass condition | If it fails |
|---|---|---|---|
| Thu 12 Nov | Question locked | Group agrees on this file's question in the chat | Fall back to blocs refocused (alternative 2 in `01`) |
| Sun 15 Nov | **Data gate and kill test** | 115th Record and bills downloaded with the same scripts; Trump-rate and cross-party tables computed for 2017-18 | If 2017-18 shows the same pattern in both halves, decide on 18 Nov between "normal cycle" paper and blocs |
| Mon 16 Nov | Stance check | 100 mentions coded by two people, kappa ≥ 0.6 | Switch the words measure to "president trump" in praise contexts only, or report stance as a limitation |
| Wed 18 Nov | TA check | Show figure 1 and 2 drafts to Lasse or a TA in the morning session | Adjust the claim |
| Sun 22 Nov | Results frozen | All numbers final, rerun on final results download | Nothing new after this |
| Wed 25 Nov | Full draft to TA | Six pages in Overleaf, three slides drafted | |
| Thu 26 Nov | Submit | Martin's plan submits Thursday; keep it | Friday 27 Nov is buffer only, hand-in deadline 23:59 |

## Risks

| Risk | What we do |
|---|---|
| 2017-18 shows the same drop | Report it: "normal pre-midterm cycle, not a Trump-specific reaction" is still a checked result. Decide on 18 Nov |
| Mentions are mostly critical, not praise | Then "naming him less" is not distancing; reframe as attention, or use stance-coded rate |
| NOMINATE effect disappears under the permutation null | Drop "hardliners led" and keep "words and deeds came apart" |
| govinfo blocked on someone's machine | Run downloads on a laptop, not a sandbox; Anas's machine ran them before |
| Too many panels for six pages | Silence-on-issues panel is optional; cut it first |
