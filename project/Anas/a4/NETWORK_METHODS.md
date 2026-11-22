# The home map: values, formulas and how each number was computed

Anas with Claude, 21 to 22 Nov 2026. The reference for part 3's network layer: every value in one place, with the
formula behind it and the script that produced it, so any of us can answer "how did you get that?" at the
presentation. Design: [`HOME_NETWORK_PLAN.md`](HOME_NETWORK_PLAN.md), fixed before computing (with its
corrections). Discussion: [`README.md`](README.md). Every number comes from one run.

> **Rerun 22 Nov on Martin's 22 Nov matcher:** the values in sections 1 to 3 are the rerun's. Old against new:
> [`../RERUN_22NOV.md`](../RERUN_22NOV.md). Three one-off side checks were not repeated and are the 21 Nov values:
> the tie counts at other α (section 1), the swaps-per-tie check (3a) and the shortcut product (3a correction).
> **Correction:** Republican closeness no longer survives Holm (0.055).

**Status:** all of this is new analysis after the G17 scope freeze, for Martin and Diego to accept or cut.

---

## 1. The network

| Step | What was done | Script |
|---|---|---|
| Nodes | The 406 members of the A4 test: R or D, with a 2025 district lean and at least 10 releases (37 exposed and 171 safe Republicans; 54 exposed and 144 safe Democrats) | `analysis.py` |
| Directed tie *i → j* | *i* named *j* in at least one release, 3 Jan 2025 to 20 Nov 2026 (counted mentions, once per release). Party leaders as the named member are left out; co-leads are kept | `home_network.py` |
| Cross-party network | The R–D ties: 8,825 directed, 6,765 undirected (a tie if either names the other), 2,060 mutual pairs | `home_network.py` |
| Full weighted home map | All ties, same-party and cross-party, undirected: 29,210 ties. Weight w_ij = Σ over releases r naming the pair (either direction) of 1/n_r, with n_r the colleagues counted in release r (decision 8), so a 40-name list adds 1/40 per name | `figure_home_map.py`, `home_measures.py` |
| Backbone | The disparity filter (week 4, Serrano et al. 2009) at α = 0.01: 1,656 ties (630 cross-party), all 406 members in one component | same |

**Disparity filter.** For member *i*, with strength s_i = Σ_j w_ij and degree k_i:

  α_ij = (1 − w_ij / s_i)^(k_i − 1)   (α_ij = 1 when k_i = 1)

A tie is kept if it is significant at *either* end: min(α_ij, α_ji) < α. In words, a tie is kept when it takes a much
larger share of *i*'s (or *j*'s) naming than if *i* spread their weight evenly at random over k_i ties. α = 0.01 was
chosen for readability (0.02, 0.05, 0.1 and 0.2 keep 2,136, 3,081, 4,277 and 6,021 ties), as in the course's 4.11.

**The α sweep (added 22 Nov, after the rerun; `alpha_sweep.py`, `out/alpha_sweep.csv`).** Same graph and filter:

| α | Ties kept | Weight kept | Cross-party ties | Mean degree | Components | Members with no tie |
|---|---|---|---|---|---|---|
| 0.001 | 813 | 30% | 301 | 4.0 | 20 | 18 |
| 0.005 | 1,321 | 38% | 508 | 6.5 | 7 | 6 |
| **0.01** | **1,656** | **43%** | **630** | **8.2** | **1** | **0** |
| 0.02 | 2,137 | 48% | 792 | 10.5 | 1 | 0 |
| 0.05 | 3,092 | 57% | 1,118 | 15.2 | 1 | 0 |
| 0.1 | 4,279 | 66% | 1,497 | 21.1 | 1 | 0 |
| 0.3 (4.11's choice) | 7,522 | 81% | 2,451 | 37.1 | 1 | 0 |
| none (full map) | 29,210 | 100% | 6,765 | 143.9 | 1 | 0 |

- **What the sweep shows:** α = 0.01 is the strictest of these values that still keeps all 406 members in one
  component. At 0.005, six members lose every tie; above 0.01 the drawing only gets denser.
- **Why not 4.11's 0.3:** the philosophers' network was sparse (most ties weight 1), so 0.3 was needed to keep the
  groups connected. The home map is much denser: mean degree 144 against 13 for the philosophers' giant component
  (density 0.36 against 0.010), so at 0.3 the backbone still has a mean degree of 37: a hairball.
- **How it was chosen, honestly:** on 21 Nov by looking at the drawing; the sweep was run on 22 Nov and supports that
  choice with a rule that can be stated in advance.

**Layout.** ForceAtlas2 (networkx `forceatlas2_layout`), 2,000 iterations, scaling ratio 5, strong gravity, weighted,
seed 11: the 4.11 recipe. FA2's LinLog mode was tried and mixed the parties more, so it was not used.

## 2. Hubs: who carries the cross-party ties

| Value | Exposed members | Safe members | How |
|---|---|---|---|
| Share of members | 22.4% | 77.6% | 91 of 406 |
| Share of cross-party ties sent (out-ties) | 34.9% | 65.1% | Σ out-degree over the group / Σ over all, directed cross-party network |
| Share of cross-party ties received (in-ties) | 34.1% | 65.9% | the same for in-degree |
| Cross-party ties per member, Democrats | 45 | 30 | mean cross-party degree, full map |
| Cross-party ties per member, Republicans | 54 | 28 | same |

## 3. The tests

All p-values are two-sided. **Permutation within party:** `exposed_2025` is shuffled among the members of each party
10,000 times (seed 2805); everything else stays fixed. p = the share of shuffles with |null − mean(null)| ≥
|observed − mean(null)|. A p of 0 means none of the 10,000 shuffles, reported as p < 0.001.

### 3a. Do exposed members tie to each other? (S1, S2; week 2 null model)

**S2** = (cross-party ties with both ends exposed) / (all cross-party ties).

**S1**, binary attribute assortativity (week 3, mixing). From the mixing matrix e of tie ends (each tie counted from
both ends), with a_i = Σ_j e_ij:

  r = (Σ_i e_ii − Σ_i a_i²) / (1 − Σ_i a_i²)

It is checked equal to networkx's `attribute_assortativity_coefficient` to four decimals.

| Statistic | Observed | Within-party label shuffle | Degree-preserving rewiring (configuration model) |
|---|---|---|---|
| S2, ties joining two exposed members | **10.7%** | 4.9%, p < 0.001 | **10.2% (95%: 9.8 to 10.6%), ratio 1.05, p 0.015** |
| S1, exposure assortativity | −0.011 | −0.014, p 0.78 | −0.032, p 0.015 |

- **Which null is right:** the configuration model, the right-hand column. The label shuffle moves "exposed" onto
  less active members, so its S2 null mostly measures the hub effect, not a preference.
- **Configuration model, step by step:** start from the observed cross-party ties. Repeat 10 × 6,765 times: pick two
  ties (R₁–D₁) and (R₂–D₂) at random and swap them to (R₁–D₂) and (R₂–D₁), unless that would create a tie that
  already exists or join a member to the same member twice. Every member keeps their number of cross-party ties, and
  every tie stays R–D (a bipartite configuration model).
  - **Repeats:** 1,000 independent rewirings, each starting from the observed network, with S2 and S1 measured on
    each.
  - **Swaps per tie:** checked on 100 rewirings each. The null mean is 10.43% at 1 swap per tie, then 10.27%,
    10.27% and 10.30% at 5, 10 and 20, so 10 is enough.
- **Why not Watts–Strogatz or Erdős–Rényi (week 2):** both are models that *generate* networks. ER gives every node
  roughly the same expected degree, and WS rewires a ring lattice with probability β. Neither keeps the observed
  differences in activity, which are exactly what the hub finding is about. The configuration model holds every
  member's degree fixed and randomises everything else, so it asks only "beyond their activity, do exposed members
  tie to each other?". It is also the null of Martin's part 1.
- **Reading:** exposed members tie to each other about 5% more than their activity predicts (p 0.015). That is a
  small but real preference.
- **Correction:** an earlier shortcut, the product of each party's exposed share of tie ends (0.298 × 0.365 =
  10.9%), suggested none. It ignores that two members can be tied only once, and it overstates the null for the
  busiest members.

### 3b. Is it mutual? (S3)

Reciprocity = the share of directed cross-party ties *i → j* where *j → i* also exists.

| | Exposed–exposed ties | Other cross-party ties | Difference | p (label shuffle) | p (degree-matched, post hoc) |
|---|---|---|---|---|---|
| Reciprocity | 62.2% | 44.6% | +17.6 points | < 0.001 | 0.014 |

**Suggestive only.** Reciprocity rises with activity. The effect fades for ties in 2+ releases (p 0.45) and with
co-leads left out (p 0.09), and co-led bills make ties mutual by construction.

### 3c. Do safe members cross locally? (S4)

| | Safe speakers | Exposed speakers | Difference | p |
|---|---|---|---|---|
| Share of cross-party ties to a member of the same state | 11.1% | 10.7% | +0.4 points | 0.79 |

**No.** This is null in every robustness row.

### 3d. Centrality (week 3), on the backbone

| Measure | Formula (networkx) |
|---|---|
| Degree k_i | the number of ties of *i* in the backbone |
| Cross-party degree | the number of other-party members *i* is tied to in the full map |
| Betweenness b_i | Σ over pairs s ≠ i ≠ t of σ_st(i) / σ_st, normalised by 2 / ((n − 1)(n − 2)). σ_st is the number of shortest paths from s to t; σ_st(i) is those through *i*. Unweighted |
| Closeness c_i | (n − 1) / Σ_j d(i, j), with d the shortest-path length. Unweighted |
| Betweenness given degree | within each party, the residual of log(b_i + 10⁻⁶) regressed on log(k_i) |

Exposed against safe within each party. **Holm** corrects for the 10 tests: sort the p-values p₍₁₎ ≤ … ≤ p₍₁₀₎, set
p̃₍ₖ₎ = max over j ≤ k of min(1, (10 − j + 1) p₍ⱼ₎), and call a result significant when p̃ < 0.05.

> **Not from the course.** Holm (1979, the Holm–Bonferroni method) is a general statistics tool, not a network model:
> it does not generate or rewire anything. With 10 tests at p < 0.05 and no real effect anywhere, the chance of at least
> one false positive is 1 − 0.95¹⁰ ≈ 40%; Holm raises the bar so that the chance of *any* false positive among the 10 stays below 5%. It is
> less strict than plain Bonferroni (10 × p) for all but the smallest p. The degree-preserving rewiring *is* from the course
> (week 2, SGI-2.8; week 4, SGI-4.6). The within-party label shuffle is a permutation test: the same logic as comparing
> a network to random ones, but it shuffles who is exposed instead of who is tied. Watts–Strogatz (week 2, SGI-2.4) is not used: it generates small-world
> networks from a ring lattice, so it has no members, parties or seats to compare.

| Measure | Party | Exposed | Safe | p | Holm p |
|---|---|---|---|---|---|
| Cross-party degree (full map) | R | 54.2 | 27.8 | < 0.001 | **0.001** |
| | D | 45.7 | 29.9 | < 0.001 | **0.001** |
| Degree (backbone) | R | 8.6 | 5.7 | 0.002 | **0.013** |
| | D | 9.8 | 10.3 | 0.57 | 1.00 |
| Betweenness (backbone) | R | 0.0067 | 0.0037 | 0.010 | 0.059 |
| | D | 0.0065 | 0.0066 | 0.91 | 1.00 |
| Closeness (backbone) | R | 0.316 | 0.300 | 0.008 | 0.055 |
| | D | 0.337 | 0.335 | 0.52 | 1.00 |
| Betweenness given degree | R | −0.25 | +0.05 | 0.12 | 0.47 |
| | D | +0.18 | −0.07 | 0.016 | 0.08 |

**Reading:**
- **Holds after correction:** exposed members of both parties have far more cross-party ties. Exposed Republicans
  also have more backbone ties (Holm 0.013); their higher closeness and betweenness are borderline (0.055, 0.059).
  **Corrected 22 Nov:** on the 21 Nov run closeness held (0.034).
- **Does not hold at α = 0.01:** "exposed Democrats broker given their ties" (p 0.016 before correction, 0.08 after).
  **But it is α-dependent** (sensitivity table below): it holds after Holm at every looser α (0.002 to 0.009).
- **Sensitivity to α (added 22 Nov; `alpha_centrality.py`, `out/alpha_centrality.csv`).** The same test at six α
  values; ratio exposed ÷ safe, Holm p in brackets (for the residual: the gap):

  | Measure | Party | 0.005 | **0.01** | 0.02 | 0.05 | 0.1 | 0.2 |
  |---|---|---|---|---|---|---|---|
  | Degree (backbone) | R | 1.56 (0.009) | **1.51 (0.013)** | 1.46 (0.009) | 1.42 (0.009) | 1.39 (0.005) | 1.39 (0.004) |
  | | D | 0.97 (1.00) | **0.96 (1.00)** | 0.95 (1.00) | 0.94 (1.00) | 0.91 (0.39) | 0.90 (0.19) |
  | Betweenness (backbone) | R | 2.08 (0.045) | **1.84 (0.059)** | 1.79 (0.041) | 1.72 (0.032) | 1.60 (0.042) | 1.58 (0.042) |
  | | D | 1.00 (1.00) | **0.98 (1.00)** | 0.99 (1.00) | 1.00 (1.00) | 0.97 (1.00) | 0.95 (1.00) |
  | Closeness (backbone) | R | 1.06 (0.58) | **1.05 (0.055)** | 1.05 (0.020) | 1.05 (0.009) | 1.05 (0.005) | 1.05 (0.004) |
  | | D | 1.01 (1.00) | **1.01 (1.00)** | 1.00 (1.00) | 0.99 (1.00) | 0.99 (1.00) | 1.00 (1.00) |
  | Betweenness given degree | R | −0.22 (1.00) | **−0.31 (0.47)** | −0.29 (0.13) | −0.25 (0.009) | −0.22 (0.003) | −0.21 (0.001) |
  | | D | +0.31 (0.22) | **+0.25 (0.08)** | +0.18 (0.009) | +0.18 (0.002) | +0.22 (0.001) | +0.22 (0.001) |

  - **Stable at every α:** the *direction* of every comparison, and roughly its size (Republican betweenness
    moves most, 2.1× to 1.6×). Exposed Republicans have about 1.4 to 1.6
    times the backbone ties of safe Republicans (significant everywhere); exposed and safe Democrats do not differ in
    degree, betweenness or closeness at any α.
  - **What moves is significance at the margin.** α = 0.01 is the sparsest connected backbone, so it has the fewest
    ties and the least power. From 0.02 up, Republican betweenness and closeness and the Democrats' "brokering given
    ties" pass Holm; from 0.05 up, so does "exposed Republicans sit on *fewer* paths than their ties predict".
  - **What we report:** α = 0.01 stays the main setting (chosen 21 Nov, before this check), with one sentence: "the
    party difference in how exposed members bridge (Republicans by volume, Democrats by position) is significant at
    every looser backbone level but not at the strictest". Switching α after seeing this would be choosing the result.
  - At 0.005 six members have no tie; their betweenness and closeness are 0 (networkx), which is why that column is
    noisier.
- **Closeness hardly varies** (standard deviation 0.02 to 0.03), because in this network most members are two or
  three steps apart.

### 3e. Communities (week 4)

| Value | Result | How |
|---|---|---|
| Method | Louvain, resolution 1, full weighted map | networkx `louvain_communities`, 50 seeds (0 to 49), the partition with the highest modularity kept (as in Martin's G15) |
| Modularity Q | 0.272 | Q = (1 / 2m) Σ_ij [w_ij − s_i s_j / 2m] δ(c_i, c_j), with m the total weight and s the strengths |
| Communities | 11 (9 with at least 10 members) | |
| NMI with party | 0.20 | normalised mutual information between community and party (sklearn). For comparison, the working map (Martin's M5) is 0.83 |
| Q of the party split | 0.152 weighted, 0.237 unweighted | the same Q formula with the two parties as the communities. **Not comparable** to the floor (0.106) or working (0.211) maps: different tie definitions and densities |
| Where exposed members sit | 37% (R) and 39% (D) of an exposed member's community is from the other party, against 26% and 26% for safe members (p 0.012 and 0.002) | per member, the share of the rest of their community from the other party; exposed against safe, within-party shuffle |

| Community (label from its makeup) | Members | R | D | Exposed |
|---|---|---|---|---|
| Republican core | 120 | 112 | 8 | 16 |
| Democratic core | 95 | 6 | 89 | 13 |
| Texas, Florida (and Connecticut) | 52 | 33 | 19 | 7 |
| **Close seats** (New York, Michigan): Bacon, LaLota, Gillen, Golden, J. Riley, Kaptur, Cuellar, Fitzpatrick, Lawler, … | **35** | 17 | 18 | **19** |
| Minnesota, North Carolina (and Ohio) | 31 | 14 | 17 | 11 |
| Maryland, Virginia | 23 | 7 | 16 | 5 |
| Washington, Oregon (and Arizona) | 18 | 4 | 14 | 4 |
| Florida, Nevada | 18 | 11 | 7 | 8 |
| **Close seats** (California, Hawaii): Costa, Gray, Harder, Kim, Valadao | 10 | 4 | 6 | 5 |
| Two pairs (New Hampshire, Rhode Island) | 2 + 2 | 0 | 4 | 3 |

- **Labels:** a community is a "core" when over 90% is one party, "close seats" when at least half its members are
  exposed, and otherwise named by its two most common states.
- **Members by community:** `out/home_communities_members.csv`.
- **Caveat:** Louvain is random, so the best of 50 seeds is one partition among similar ones. The close-seat
  community's exact membership can change at the edges between runs: after the 22 Nov rerun it lost
  Malliotakis, Latta and Matsui and gained McBride (37 → 35; adjusted Rand index 0.88 between the two partitions).

### 3f. The picture itself (not a test)

Of each member's 10 nearest neighbours in the drawn layout, the share from the other party is 46 to 50% for exposed
members and 30 to 41% for safe members, over layout seeds 11, 12 and 13. It shows that the drawing places exposed
members where the parties meet. The tests are above.

## 4. Answers to the obvious questions

- **"Is this Watts–Strogatz?"** No. WS is a generative small-world model with a rewiring probability β. We test an
  observed network, so the null is the configuration model (§3a): no β, and every member's degree held fixed by
  double-edge swaps.
- **"How does the null connect to the backbone?"** It doesn't. The null runs on all 6,765 cross-party ties. The
  backbone is used only for the drawing and for path-based centrality, where the full map is too dense for paths to
  mean anything.
- **"Why α = 0.01?"** It is the strictest α that keeps every member in one component (the sweep in §1). Members
  keep 8.2 backbone ties on average (1,656 ties, so about 4 per member when each tie is counted once; **corrected
  22 Nov:** this line said "about 4 ties each"). Results that use the backbone
  (§3d) depend on it; the tests in §3a to §3c and the communities (§3e) do not.
- **"Only 10 comparisons?"** All 406 members are in every calculation. The 10 are tests (5 measures × 2 parties),
  corrected with Holm (§3d).
- **"Naming means praise?"** No. It means naming; tone is not measured here.
