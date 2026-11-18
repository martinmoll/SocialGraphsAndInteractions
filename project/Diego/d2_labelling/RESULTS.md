# D2 results: what floor mentions do

Diego Mijares with Claude, 18 November 2026. Coding complete: Diego coded all 100 mentions, Martin rows
1–25, Anas rows 76–100, Claude rows 26–75, and three further Claude runs (AI1–AI3) all 100. Full output in
`agreement_results.txt`, from `agreement.py`.

## Agreement

| Pair | Rows | Raw agreement | Cohen's κ |
|---|---|---|---|
| Diego and Martin | 25 | 80% | 0.59 |
| Diego and Anas | 25 | 84% | 0.69 |
| Diego and a second human, pooled | 50 | 82% | 0.64 |
| Diego and Claude | 50 | 88% | 0.72 |
| Diego and each of AI1–AI3 | 100 | 81–82% | 0.56–0.58 |
| Diego and the AI1–AI3 majority | 100 | 82% | 0.58 |
| AI runs with each other | 50–100 | 94–100% | 0.85–1.00 |

Human agreement is above the 0.6 set in advance (pooled), so the codes carry the headline. The AI runs
agree with Diego about as well as the second humans on their 50 rows, less on all 100. They agree with each
other almost perfectly because they are the same model: that is stability, not independence.

Two cells held two codes and were read by the protocol's priority: row 85 (Diego, "A or N") as A, row 94
(Anas, "D, N") as D.

## Shares, from Diego's codes (95% Wilson intervals)

| | Procedure | Agreeing | Disagreeing | Neutral | Wrong person |
|---|---|---|---|---|---|
| Cross-party, n = 75 | 0% (0–5) | 69% (58–79) | 7% (3–15) | 23% (15–33) | 1% (0–7) |
| Same-party, n = 25 | 12% (4–30) | 80% (61–91) | 0% (0–13) | 4% (1–20) | 4% (1–20) |

**Reading:** cross-party mentions on the floor are mostly credit and thanks, and rarely argument. The
headline "members talk across the aisle to argue" is not supported; the floor map's lower division reflects
whom members credit. Procedure (yields) stays almost entirely within a party.

## Two codes Diego changed after seeing the AI flags

All three AI runs and Claude coded rows 38 and 86 as **wrong person**, and Diego had not. On 18 November
Diego reread both, agreed, and changed his codes to X. The numbers above include the change. Because he
changed them after seeing the AI codes, those two rows are not independent of the AI coding; the paper says
so in one clause.

- **Row 38:** "Griff Lynch", the head of the Georgia Ports Authority, matched to Rep. Stephen Lynch. A to X.
- **Row 86:** "Bob Matsui", the late husband of Rep. Doris Matsui, matched to her. N to X.

Effect: the matcher's precision in this sample (DECISIONS G10) is **98 of 100** (95% interval 93 to 99),
not 100 of 100. Diego–Anas κ fell from 0.76 to 0.69, because Anas had coded row 86 as neutral. The shares
moved by a point or less.

## What this does to the headline

Cross-party mentions on the floor are mostly agreeing: thanks, credit and partnership (69%). Disagreement
is rare (7%). The alternative headline, "members talk across the aisle to argue", is not supported. The
floor map's lower division reflects whom members credit, and the Introduction, Discussion and slides should
be written that way.
