# 02 · Pilot findings (11 November 2026)

One evening, on `data/processed/` as committed (119th Congress, Jan 2025 to early Nov 2026) plus a
sample of the 115th Congress (2017-18). Reproduce with `python Diego_Claude/pilot/pilot_distancing.py` from
`project/`. Numbers in brackets refer to the script's printed sections.

**Status: exploratory.** Definitions were chosen while looking at the numbers. Before the paper, fix the
definitions in `03_plan_if_chosen.md`, then rerun. Nothing has been hand-checked.

Definitions used here: speaker turns of at least 50 words; "early" = before 1 Dec 2025, "late" = from
1 Dec 2025; Trump rate = occurrences of the whole word "trump" per 10,000 words.

## 1. Republicans stopped saying Trump's name on the floor [1, 2]

House floor only (section H), Republican members, per 10,000 words:

| Half-year | "trump" | "the president" | "administration" | "biden" | Words |
|---|---|---|---|---|---|
| 2025 H1 | 13.94 | 3.42 | 10.48 | 8.86 | 918,240 |
| 2025 H2 | 10.85 | 3.94 | 8.60 | 5.14 | 614,993 |
| 2026 H1 | 9.47 | 3.84 | 6.09 | 3.68 | 910,386 |
| 2026 H2 | 4.92 | 3.82 | 3.63 | 1.55 | 317,025 |

Share of Republicans (at least 1,000 words in the half-year) who name Trump at least once per 1,000 words:
33%, 24%, 24%, 6%.

- "The president" is flat, so members did not just swap the name for the title.
- **Caution:** "biden" fell faster than "trump" in relative terms. Part of the drop may be a general fade
  of national names over a term. The 2017-18 baseline is what separates the two readings.
- 2026 H2 is short (317,025 words, September to early November) and pre-election.

Monthly rates by party show clear events in the Record, which the "silence" panel could use (per 100,000
words, Republicans vs Democrats at their peak month): "iran" 113.1 vs 110.4 (Mar 2026); "ice" 52.1 vs 69.8
(Jan 2026) and 24.7 vs 140.3 (Mar 2026); "tariff" 23.6 vs 93.6 (Feb 2026); "medicaid" 55.1 vs 189.1 (May 2025);
"epstein" 99.2 vs 50.6 (Nov 2025); "affordab" 86.9 vs 89.7 (Dec 2025).

## 2. Republicans signed more Democratic bills [3]

Cross-party share of cosponsorships by quarter signed:

| Quarter | Republican n | Republican → Democratic sponsor | Democratic n | Democratic → Republican sponsor |
|---|---|---|---|---|
| 2025Q1 | 14,026 | 9.0% | 17,434 | 22.9% |
| 2025Q2 | 7,834 | 15.6% | 15,853 | 22.4% |
| 2025Q3 | 6,352 | 18.5% | 14,119 | 22.9% |
| 2025Q4 | 5,599 | 21.4% | 13,333 | 24.7% |
| 2026Q1 | 5,312 | 18.1% | 11,952 | 16.9% |
| 2026Q2 | 6,092 | 20.1% | 12,202 | 21.0% |
| 2026Q3 | 4,807 | 20.5% | 9,268 | 21.0% |
| 2026Q4 | 1,114 | 31.0% | 3,523 | 21.4% |

Democrats stay flat around 21-25%; Republicans more than double.

**Baseline, 115th Congress (2017-18), sample of every 6th House bill** (`pilot/billstatus115_sample.js`;
1,233 bills, 19,356 cosponsorships; `hr` only, the 119th table includes `hjres`):

| Quarter | Republican n | Republican cross | Democratic n | Democratic cross |
|---|---|---|---|---|
| 2017Q1 | 1,468 | 8.0% | 1,991 | 26.1% |
| 2017Q2 | 1,397 | 16.7% | 2,456 | 31.7% |
| 2017Q3 | 725 | 12.4% | 1,415 | 30.4% |
| 2017Q4 | 1,158 | 10.9% | 1,794 | 32.8% |
| 2018Q1 | 997 | 12.6% | 1,620 | 32.8% |
| 2018Q2 | 691 | 17.5% | 1,300 | 26.3% |
| 2018Q3 | 563 | 17.1% | 1,249 | 19.9% |
| 2018Q4 | 115 | 37.4% | 412 | 22.3% |

**Reading:** the first quarter of a Congress is always low (partisan reintroductions), and the last quarter
is tiny and noisy. Between those, Republicans ran at 11-18% in 2017-18 and at 16-21% in 2025-26, and the
Democratic side was less cross-party in 2025-26 than in 2017-18. So there is a gap, of roughly 3-6 points,
but it is smaller than the raw 9% → 20% suggests. **This must be redone on the full download before any claim.**

## 3. Who went quiet and who crossed over [4, 5, 6]

Per Republican member, early vs late:

- **Words** (n = 181 with at least 1,500 words in each period): median Trump rate 5.95 → 2.90 per 10,000
  words; 57% fell. Regressing the late rate on the early rate, NOMINATE and district lean (standardised):
  NOMINATE −0.991 per SD, lean −0.234 per SD. **More conservative members dropped Trump's name more**, at
  the same starting level. Swing-seat exposure (lean) barely matters.
- **Deeds** (n = 218 with at least 10 cosponsorships in each period): median cross-party share 8.7% → 14.5%;
  87% rose. NOMINATE −0.023 per SD, lean −0.004 per SD: moderates crossed more, exposure again barely matters.
- **Words vs deeds:** the change in Trump rate and the change in cross-party share are unrelated
  (Spearman 0.06, p = 0.46, n = 178). Different members distanced in different ways.

Largest drops in Trump rate (at least 3,000 words in each period; per 10,000 words): Joyce (PA) 55.8 → 12.5,
Mann (KS) 53.5 → 13.1, Stutzman (IN) 53.2 → 14.4, Jordan (OH) 37.8 → 0.0, Clyde (GA) 45.5 → 12.3, Miller (IL)
34.8 → 7.3. Largest rises: Malliotakis (NY) 9.3 → 31.6, LaHood (IL) 3.8 → 19.0, Mast (FL) 2.7 → 17.7.

**Caution:** several of the biggest droppers manage floor debate (Jordan chairs Judiciary, Steil chairs
House Administration). No standard errors yet; the NOMINATE coefficient needs a permutation or bootstrap
before it is a finding.

## 4. Distancing and the election [7]

Approximate study population (Republican incumbent, one Democrat, called race, enough words): n = 140.
Spearman of running ahead of the district with the change in Trump rate: 0.08, p = 0.33. **No detectable
relation**, in line with walk-or-talk and with Martin's state check.

## 5. Facts checked on 11 November 2026

- Wikipedia, "2026 United States House of Representatives elections": Democrats 255 seats, Republicans 168,
  97.2% declared at 2:25 PM EST 11 Nov; popular vote 56.1% vs 42.5%.
- Wikipedia, "Opinion polling on the second Trump presidency", aggregates updated 1 Nov 2026: approval
  between 34.0% (CNN) and 39.0% (RealClearPolitics); Silver Bulletin 37.3% approve, 59.9% disapprove.
- govinfo bulk BILLSTATUS 115 (hr zip 28,697,203 bytes) and the 2017 Congressional Record (CREC-2017-05-03
  mods.xml) both return HTTP 200 from a normal browser. From some sandboxed machines govinfo is blocked; run
  the scripts on a laptop.

## 6. What the pilot does not show

- Whether any Trump mention is praise or criticism (not read).
- Whether 2017-18 had the same drop in Trump mentions (Record not downloaded yet).
- Standard errors or nulls for anything in section 3.
- Anything causal.
