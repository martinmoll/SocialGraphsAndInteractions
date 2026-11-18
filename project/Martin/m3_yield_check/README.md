# G1c: hand check of the yield rule

Martin, 18 November 2026. The main test of the phrase yield rule (DECISIONS G1c). It decides whether the
headline floor map, which drops yields (G1b), drops the right mentions.

**Open `yield_check_sheet.csv` and code it. Do not open `yield_check_key.csv` until you are done**: it says
which rule flagged each row.

## What is on the sheet

There are 30 mentions where the old rule ("yield" within 60 characters) and the new phrase rule disagree. Half
were flagged only by the new rule and half only by the old one, shuffled together. The named member's surname
is marked `[[like this]]`. `speaker` is the member talking; `named` is the member in `[[ ]]`.

## How to code

For each row, ask one question: **is the speaker handing floor time to `named`, or thanking `named` for handing
it over?** Write the code in the `code` column.

| Code | When |
|---|---|
| **Y** | The speaker yields time to `named` ("I yield 2 minutes to the gentleman from Texas (Mr. [[Roy]])"), or thanks `named` for yielding ("I thank Chairman [[Cole]] for yielding") |
| **N** | Anything else, **including a yield that goes to someone else in the same passage**, and asking `named` to yield ("Will the gentleman from Texas yield?"): that is not a yield (DECISIONS G12) |
| **?** | You can't tell from the context. Add a note, and open the debate through `doc_id` if you want |

**Watch for the trap:** row 1 starts "I thank the gentlewoman for yielding", and then talks about
[[Fitzpatrick]]. The thanks go to the gentlewoman, not to Fitzpatrick, so it is **N**. A "yield" near the name
isn't enough; it has to be aimed at `named`.

Write a note on any row you hesitated over. About 20–30 minutes.

## When you are done

Save the sheet as CSV under the same name and tell Claude. It scores the rows against the key and reports
them for each side separately:

- **"Phrase only" rows coded N:** false flags of the new rule. The headline map wrongly drops these mentions.
- **"Window only" rows coded Y:** real yields the new rule misses. They stay in the headline map.

Fifteen rows per side gives a rough figure, not a precise rate. Report it as "n of 15".

To redraw: `python Martin/m3_yield_check/draw_yield_check.py` from `project/` (seed 2805, the same rows).
