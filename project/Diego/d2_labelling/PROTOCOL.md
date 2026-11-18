# D2: labelling protocol for floor mentions

Diego Mijares with Claude, 14 November 2026. Version 1, for the group to amend on 18 November and then
freeze. After the first sheet is opened for coding, the codes do not change.

**Changed on 18 November: 20 mentions, all three code all of them.** The sample is 15 cross-party and 5
same-party mentions (seed 2805), in one sheet, `D2_coding_sheet.xlsx`, with a short key at the top and a code
column per person. The five codes and the rules below are unchanged. Where this file still says 200 mentions
and two coders per mention, the 18 November version replaces it. With 20 mentions the shares come with wide
intervals (15 cross-party mentions give about ±25 points), so the paper can say whether cross-party
mentions are mostly agreement, mostly disagreement or mostly procedure, and not much finer than that.
`agreement.py` reports Cohen's κ for each pair and Fleiss' κ for all three.[^twenty]

## What the labels are for

Part 1 of the paper finds that the floor map is less divided by party than the working map. That can mean
two different things. Either members refer to colleagues across the aisle as partners, or they name them
in order to argue. The labels decide which sentence the paper may write. They also tell us how much of the
floor map is House procedure.

## Unit and sample

- **Unit:** one row of `mentions.parquet` with `source == "floor"`: one speaker naming one member once.
- **Sample:** 150 cross-party and 50 same-party mentions, drawn at random with seed 2805 by
  `draw_labelling_sample.py` and shuffled together.[^size] Yields are not excluded, because "procedural" is
  one of the codes and the automatic yield flag is imperfect (D1: recall 87%, precision 90%).
- **Coders:** Diego codes all 200. Martin and Anas each code 100. Every mention has two coders (S1).
- **What a coder sees:** speaker, named member, date, the context. Party is not shown on the sheet. Coders
  will often know it anyway, so the coding is not blind and the paper should not say it is.
- **Context:** code from the `context` column. If it does not settle the code, open the turn through
  `doc_id` and read the paragraph. In D1 about one match in ten needed more than a sentence. Request to
  Martin: let `context` hold the sentence with the mention plus one sentence either side.

## The codes

Code what the speaker is doing **towards the named member in this mention**. Not the speaker's view of the
bill, the other party or the President.

| Code | Name | Use when the speaker |
|---|---|---|
| **P** | Procedural | manages the floor: yields time to the member, thanks the member for yielding, names the member in a unanimous-consent request, a motion or the order of debate |
| **A** | Agreeing | thanks, praises or credits the member, calls the member a partner or co-lead, supports the member's bill or amendment, or cites the member's statement with approval |
| **D** | Disagreeing | rebuts, criticises, blames or mocks the member, opposes the member's bill or amendment, or cites the member's words or record in order to attack them |
| **N** | Neutral | refers to the member without taking a side: reports who introduced or said something, names the member whose district someone lives in, lists members |
| **X** | Not a mention | the name is not that member, or the speaker did not say it (a constituent, a namesake, a vote-change line, a speaker heading) |

The work plan names three categories. N and X are added because both occur and forcing them into the three
would lower agreement and hide matcher errors.[^five]

## Rules for the hard cases

1. **One code per mention.** If two apply, the order is X, then P, then D, then A, then N. A yield is P even
   when it comes with a compliment ("I yield to my good friend"). The compliment belongs to the ritual.
2. **Thanks for yielding is P. Any other thanks is A**, including the routine thanks to a chairman or
   ranking member for bringing a bill to the floor. We do not ask coders to judge sincerity. The share of A
   that is addressed with a leadership title can be reported from the matcher's own flag.
3. **"My friend" does not decide the code.** "My friend, the gentleman from Massachusetts, may also recall
   that..." introduces a rebuttal and is D.
4. **Supporting a bill is A towards its sponsor. Opposing a bill is D towards its sponsor** only when the
   member is named as its author or defender in that sentence. "I rise in opposition to the bill" two
   sentences after thanking the ranking member for time leaves the thanks as it is.
5. **Demands and appeals.** Urging a member to act against their current position ("Speaker Johnson should
   bring the bill to the floor") is D. Asking a member a factual question in a colloquy is N.
6. **Quotations.** Code the speaker's use of the quote. Quoting a member to endorse the point is A, to
   refute it is D.
7. **Tributes and condolences** to or about the member are A.
8. **Do not guess.** If the context and the turn do not settle it, give the best code and put `1` in the
   `unsure` column. Unsure rows are reported separately and are the first to be discussed.

## Worked examples

From the D1 sample of the prototype's matches (item numbers refer to
`../d1_matcher_precision/labels.csv`).

| Item | Text | Code | Why |
|---|---|---|---|
| 15 | "I yield 1 1/2 minutes to the gentlewoman from New Mexico (Ms. Stansbury)" | P | Yield |
| 32 | "I thank the gentlewoman from Indiana (Mrs. Houchin) for yielding me the customary 30 minutes" | P | Thanks for yielding, across parties |
| 33 | "...controlled by Representative Mast of Florida and Representative Meeks of New York..." | P | Unanimous-consent request |
| 9 | "a bipartisan bill I am leading with my good friend from California (Mr. Peters)" | A | Partner on a bill |
| 1 | "I thank Chairman Cole and Ranking Member DeLauro for their hard work" | A | Routine thanks, rule 2 |
| 12 | "sadly, I cannot agree with Chairman Cole" | D | Direct disagreement, though flagged as a yield |
| 34 | "My friend, the gentleman from Massachusetts (Mr. McGovern), may also recall..." | D | Rebuttal, rule 3 |
| 62 | "they won't ask Speaker Johnson or the President why they voted this way" | D | Blame |
| 29 | "the text of my December 10, 2025, letter to Speaker Mike Johnson" | N | Reports a letter |
| 98 | "Minnesota's Eighth Congressional District, represented by our colleague ... Congressman Peter Stauber" | N | Names whose district it is |
| 5 | "Mrs. Peters now holds classes showing students how to raise ... livestock" | X | A constituent |

## Pilot

Claude applied version 1 to the 39 correct cross-party mentions in the D1 main sample: 24 A, 9 D, 4 P, 2 N.
This is one AI coder on a small sample from the unvalidated prototype matcher. It is an indication of what
to expect, not a result, and it does not enter the paper. If the pattern holds, most cross-party mentions
are bill managers thanking co-leads and committee leaders, about a quarter are argument, and the headline
"less divided" survives with the qualification that routine thanks carry much of it.

## Agreement and reporting

- `agreement.py` reports raw agreement and Cohen's κ over the five codes, for all 200, for the 150
  cross-party mentions, and for each pair of coders.
- Rows where the two coders differ go to `disagreements.csv`. The member who coded neither decides where
  there is one. For the rest, the two coders settle it together. The paper reports κ **before** this step.
- The paper reports the distribution of codes among cross-party mentions with an interval, the same for
  same-party mentions as the comparison, the share coded X, and κ.
- Decided in advance: if κ on the cross-party mentions is below 0.6, the paper says the codes are not
  reliable enough to carry the headline and reports only P against not-P, where agreement is easier.[^kappa]
- If an LLM is used to code more mentions later, this hand-coded sample is its ground truth and its error
  rate is reported (course rule for model labels). Not planned.

## Order of work

1. 18 Nov: group reads this file, amends, freezes.
2. Martin's `mentions.parquet` exists: Diego runs `draw_labelling_sample.py`, which writes
   `sample_key.csv` and the three sheets. It refuses to overwrite sheets.
3. Each coder fills in their own sheet alone, without looking at another sheet. About 100 mentions an hour.
4. Diego runs `agreement.py`. Numbers are in by the freeze on Sun 22 Nov.

Both scripts have been run on a stand-in file built from the prototype's mention table and random codes,
in a scratch folder. No sample has been drawn in the repository.

[^size]: 150 gives an interval of about ±8 percentage points on a share near 50%, enough to tell "mostly
    agreeing" from "mostly disagreeing" and feasible in the week available: 200 rows for Diego, 100 each for
    Martin and Anas. The 50 same-party rows are the comparison and stop coders from assuming every row
    crosses the aisle. Diego took this decision under Claude's guidance.
[^five]: Diego took this decision under Claude's guidance. The alternative is the three codes of the work
    plan with an "other" box.
[^kappa]: 0.6 is the lower edge of what Landis and Koch (1977) call substantial agreement. Any threshold is
    a convention. Setting it before coding is what matters. Diego took this decision under Claude's guidance.
[^twenty]: Smaller than the 200 first proposed, to fit the time the group has. Diego took this decision
    under Claude's guidance, on 18 November.
