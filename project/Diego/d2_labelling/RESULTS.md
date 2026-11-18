# D2 results: what floor mentions do

Diego Mijares with Claude, 18 November 2026. Coding complete: Diego coded all 100 mentions, Martin rows
1–25, Anas rows 76–100, Claude rows 26–75, and three further Claude runs (AI1–AI3) all 100. Full output in
`agreement_results.txt`, from `agreement.py`.

## Agreement

| Pair | Rows | Raw agreement | Cohen's κ |
|---|---|---|---|
| Diego and Martin | 25 | 80% | 0.59 |
| Diego and Anas | 25 | 88% | 0.76 |
| Diego and a second human, pooled | 50 | 84% | 0.67 |
| Diego and Claude | 50 | 86% | 0.66 |
| Diego and each of AI1–AI3 | 100 | 79–80% | 0.51–0.53 |
| Diego and the AI1–AI3 majority | 100 | 80% | 0.53 |
| AI runs with each other | 50–100 | 94–100% | 0.85–1.00 |

Human agreement is above the 0.6 set in advance (pooled), so the codes carry the headline. The AI runs
agree with Diego about as well as the second humans on their 50 rows, less on all 100. They agree with each
other almost perfectly because they are the same model: that is stability, not independence.

Two cells held two codes and were read by the protocol's priority: row 85 (Diego, "A or N") as A, row 94
(Anas, "D, N") as D.

## Shares, from Diego's codes (95% Wilson intervals)

| | Procedure | Agreeing | Disagreeing | Neutral | Wrong person |
|---|---|---|---|---|---|
| Cross-party, n = 75 | 0% (0–5) | 71% (60–80) | 7% (3–15) | 23% (15–33) | 0% (0–5) |
| Same-party, n = 25 | 12% (4–30) | 80% (61–91) | 0% (0–13) | 8% (2–25) | 0% (0–13) |

**Reading:** cross-party mentions on the floor are mostly credit and thanks, and rarely argument. The
headline "members talk across the aisle to argue" is not supported; the floor map's lower division reflects
whom members credit. Procedure (yields) stays almost entirely within a party.

## Two rows for Diego to look at again

All three AI runs and Claude coded these as **wrong person**, and Diego did not. Reading the context, the
AI codes look right. They are Diego's to change; nothing has been overruled.

- **Row 38:** "Griff Lynch", the head of the Georgia Ports Authority, matched to Rep. Stephen Lynch. Diego: A.
- **Row 86:** "Representatives Bob Matsui and Glenn Anderson", the late husband of Rep. Doris Matsui, matched
  to her. Diego: N.

If both become X, the matcher's precision in this sample (DECISIONS G10) is 98 of 100, not 100 of 100, and
the shares above move by about one point.
