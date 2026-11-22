# A5: does a release that says "bipartisan" name a real cross-party partner? (22 Nov, late)

Anas with Claude. Design fixed first: [`PLAN.md`](PLAN.md). Optional item under G17; Martin and Diego decide whether it
stays in.

> **Status, 22 Nov, late: not finished.** Done: the numbers and the check of releases with *no* partner. **Still to
> do (Mon 23 Nov):** the mirror check. The "named" measure counts any House member of the other party named in a
> "bipartisan" release as a partner, but a release can name one as an opponent. Three blind readers will code 30
> random "bipartisan" releases with a named partner (is the named member a partner?), and Anas reads the
> disagreements. Until then the safe figure is **36.9% (on record)**; the 63.9% (either) leans on the unchecked
> "named" part.

```bash
python a5/analysis.py --press press_releases --repo <repo>   # about 5 s; a5/out/, a5/check/draw.csv
python a5/make_packet.py                                     # the readers' packet, a5/check/packet/
python a5/score_check.py                                     # after the readers' CSVs are in a5/check/readers/
```

## Result (`out/results.csv`, one run, 22 Nov)

**Releases:** the 406 A4 members, 3 Jan 2025 to 20 Nov 2026, templates out: 53,664 releases. 13,744 (25.6%) say
"bipartisan" outside the member's own repeated sentences. 370 members have at least 5 such releases.

| Partner of the other party in the House | "Bipartisan" releases | Other releases | Difference (p) |
|---|---|---|---|
| **Either: named or on record** | **63.9%** | 8.6% | +55.3 points (< 0.001) |
| Named in the release | 53.4% | 4.3% | +49.1 points (< 0.001) |
| On record (a cited bill has one as sponsor or original cosponsor) | 36.9% | 5.3% | +31.6 points (< 0.001) |

Means over the 370 members; p from flipping the sign of each member's difference (10,000 times). Pooled over
releases instead: 63.5% against 8.3% (either).

- **Reading:** in about two of three releases that say "bipartisan", a House member of the other party is there to
  back it, by name or on the bill. Releases that do not use the word have one in fewer than one in ten. The word mostly
  comes with a partner.
- **About a third (36.5%, 5,011 releases) have no such partner on either measure.** The reading check below says what
  they are.
- **By seat (the A4 split; one test per party, no correction):** among Republicans, exposed 72.1% against safe 69.1%
  (p 0.40); among Democrats, exposed 63.0% against safe 56.7% (p 0.012). Exposed members use the word with a
  partner at least as often as safe members; the difference is clear only for Democrats.

## The reading check (`check/`)

30 partner-less "bipartisan" releases, drawn at random (seed 2805), coded by three blind AI readers (two Claude Opus,
one Claude Sonnet) from the packet alone (`check/packet/`): H a House partner the matcher missed, S a senator, O a
partner outside Congress, V no partner named, X the word not about the member's work.

**Result (`score_check.py`, `check/scored.csv`):** the readers agree on 28 of 30 items, and on every item two of
three agree (pairwise agreement 100%, 93%, 93%). Final codes: Anas's for the 2 disagreements, the readers'
unanimous code for the other 28.

| Code | Items | Share (95% interval) |
|---|---|---|
| V: no partner of the other party named | 25 | 83% (66% to 93%) |
| X: the word not about the member's work | 4 | 13% (5% to 30%) |
| S: a senator of the other party (Michael Bennet) | 1 | 3% (1% to 17%) |
| H: a House partner the matcher missed | 0 | 0% (0% to 11%) |
| O: a partner outside Congress | 0 | 0% (0% to 11%) |

- **Reading:** 29 of the 30 partner-less releases really name no partner from the other party. The instrument's
  blind spot (senators, missed House members) explains 1 of 30. So the "no partner" third is mostly the release, not
  the method: "bipartisan" there describes a bill, a vote, past funding or general support, with nobody from the
  other side named.
- **X examples:** the word describes a past appropriations act, a state's approach under two governors, or a
  group of lawmakers from an earlier year.
- **Disagreements** (`check/DIFFERENCES.md`, with excerpts and tick boxes; the bare list is
  `check/disagreements_auto.md`): a5_01 (V, V, X) and a5_02 (X, X, O). Neither changes the reading:
  both stay "no partner of the member's own". **Anas read both on 22 Nov: X and X** (`check/anas_codes.csv`), so
  a5_01 moves from the majority's V to X; a5_02 stays X.

**For the paper (one short paragraph, in `../results_part3.tex`, marked optional):** a quarter of releases call
something bipartisan; in 64% of them a House member of the other party is named or co-leads a cited bill, against
9% of other releases; of 30 without one, 29 name no partner from the other party.

## Limits

- **Senators and Senate bills are invisible** to both measures; the check measures how often that hides a partner.
- **On record uses original cosponsors;** later cosponsors are not counted.
- **Named counts co-leads,** on purpose: a co-lead is the partner.
- **AI readers:** same model family, so not independent of each other; Anas reads every disagreement.
