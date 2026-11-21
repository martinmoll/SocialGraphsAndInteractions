# The home map: values, formulas and how each number was computed

Anas with Claude, 21 to 22 Nov 2026. The reference for part 3's network layer: every value in one place, with the
formula behind it and the script that produced it, so any of us can answer "how did you get that?" at the
presentation. Design: [`HOME_NETWORK_PLAN.md`](HOME_NETWORK_PLAN.md), fixed before computing (with its
corrections). Discussion: [`README.md`](README.md). Every number comes from one run.

**Status:** all of this is new analysis after the G17 scope freeze, for Martin and Diego to accept or cut.

---

## 1. The network

| Step | What was done | Script |
|---|---|---|
| Nodes | The 406 members of the A4 test: R or D, with a 2025 district lean and at least 10 releases (37 exposed and 171 safe Republicans; 54 exposed and 144 safe Democrats) | `analysis.py` |
| Directed tie *i → j* | *i* named *j* in at least one release, 3 Jan 2025 to 20 Nov 2026 (counted mentions, once per release). Party leaders as the named member are left out; co-leads are kept | `home_network.py` |
| Cross-party network | The R–D ties: 8,787 directed, 6,732 undirected (a tie if either names the other), 2,055 mutual pairs | `home_network.py` |
| Full weighted home map | All ties, same-party and cross-party, undirected: 29,163 ties. Weight w_ij = Σ over releases r naming the pair (either direction) of 1/n_r, with n_r the colleagues counted in release r (decision 8), so a 40-name list adds 1/40 per name | `figure_home_map.py`, `home_measures.py` |
| Backbone | The disparity filter (week 4, Serrano et al. 2009) at α = 0.01: 1,659 ties (630 cross-party), all 406 members in one component | same |

**Disparity filter.** For member *i*, with strength s_i = Σ_j w_ij and degree k_i:

  α_ij = (1 − w_ij / s_i)^(k_i − 1)   (α_ij = 1 when k_i = 1)

A tie is kept if it is significant at *either* end: min(α_ij, α_ji) < α. In words, a tie is kept when it takes a much
larger share of *i*'s (or *j*'s) naming than if *i* spread their weight evenly at random over k_i ties. α = 0.01 was
chosen for readability (0.02, 0.05, 0.1 and 0.2 keep 2,136, 3,081, 4,277 and 6,021 ties), as in the course's 4.11.

**Layout.** ForceAtlas2 (networkx `forceatlas2_layout`), 2,000 iterations, scaling ratio 5, strong gravity, weighted,
seed 11: the 4.11 recipe. FA2's LinLog mode was tried and mixed the parties more, so it was not used.

## 2. Hubs: who carries the cross-party ties

| Value | Exposed members | Safe members | How |
|---|---|---|---|
| Share of members | 22.4% | 77.6% | 91 of 406 |
| Share of cross-party ties sent (out-ties) | 34.9% | 65.1% | Σ out-degree over the group / Σ over all, directed cross-party network |
| Share of cross-party ties received (in-ties) | 34.2% | 65.8% | the same for in-degree |
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
| S2, ties joining two exposed members | **10.8%** | 4.9%, p < 0.001 | **10.3% (95%: 9.9 to 10.7%), ratio 1.05, p 0.025** |
| S1, exposure assortativity | −0.010 | −0.014, p 0.73 | −0.031, p 0.025 |

- **Which null is right:** the configuration model, the right-hand column. The label shuffle moves "exposed" onto
  less active members, so its S2 null mostly measures the hub effect, not a preference.
- **Configuration model, step by step:** start from the observed cross-party ties. Repeat 10 × 6,732 times: pick two
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
- **Reading:** exposed members tie to each other about 5% more than their activity predicts (p 0.025). That is a
  small but real preference.
- **Correction:** an earlier shortcut, the product of each party's exposed share of tie ends (0.298 × 0.365 =
  10.9%), suggested none. It ignores that two members can be tied only once, and it overstates the null for the
  busiest members.

### 3b. Is it mutual? (S3)

Reciprocity = the share of directed cross-party ties *i → j* where *j → i* also exists.

| | Exposed–exposed ties | Other cross-party ties | Difference | p (label shuffle) | p (degree-matched, post hoc) |
|---|---|---|---|---|---|
| Reciprocity | 62.1% | 44.7% | +17.4 points | < 0.001 | 0.02 |

**Suggestive only.** Reciprocity rises with activity. The effect fades for ties in 2+ releases (p 0.44) and with
co-leads left out (p 0.09), and co-led bills make ties mutual by construction.

### 3c. Do safe members cross locally? (S4)

| | Safe speakers | Exposed speakers | Difference | p |
|---|---|---|---|---|
| Share of cross-party ties to a member of the same state | 11.2% | 10.7% | +0.5 points | 0.76 |

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

| Measure | Party | Exposed | Safe | p | Holm p |
|---|---|---|---|---|---|
| Cross-party degree (full map) | R | 54.2 | 27.6 | < 0.001 | **0.001** |
| | D | 45.5 | 29.7 | < 0.001 | **0.001** |
| Degree (backbone) | R | 8.7 | 5.8 | 0.001 | **0.010** |
| | D | 9.9 | 10.3 | 0.63 | 1.00 |
| Betweenness (backbone) | R | 0.0067 | 0.0036 | 0.010 | 0.058 |
| | D | 0.0066 | 0.0067 | 0.94 | 1.00 |
| Closeness (backbone) | R | 0.317 | 0.300 | 0.005 | **0.034** |
| | D | 0.338 | 0.335 | 0.44 | 1.00 |
| Betweenness given degree | R | −0.29 | +0.06 | 0.07 | 0.27 |
| | D | +0.17 | −0.06 | 0.02 | 0.12 |

**Reading:**
- **Holds after correction:** exposed members of both parties have far more cross-party ties. Exposed Republicans
  are also more central in the backbone (more ties, higher closeness, borderline higher betweenness).
- **Does not hold:** "exposed Democrats broker given their ties" (p 0.02 before correction, 0.12 after). It is a hint
  at most.
- **Closeness hardly varies** (standard deviation 0.02 to 0.03), because in this network most members are two or
  three steps apart.

### 3e. Communities (week 4)

| Value | Result | How |
|---|---|---|
| Method | Louvain, resolution 1, full weighted map | networkx `louvain_communities`, 50 seeds (0 to 49), the partition with the highest modularity kept (as in Martin's G15) |
| Modularity Q | 0.273 | Q = (1 / 2m) Σ_ij [w_ij − s_i s_j / 2m] δ(c_i, c_j), with m the total weight and s the strengths |
| Communities | 11 (9 with at least 10 members) | |
| NMI with party | 0.22 | normalised mutual information between community and party (sklearn). For comparison, the working map (Martin's M5) is 0.83 |
| Q of the party split | 0.151 weighted, 0.237 unweighted | the same Q formula with the two parties as the communities. **Not comparable** to the floor (0.106) or working (0.211) maps: different tie definitions and densities |
| Where exposed members sit | 36% (R) and 39% (D) of an exposed member's community is from the other party, against 24% and 23% for safe members (p 0.010 and < 0.001) | per member, the share of the rest of their community from the other party; exposed against safe, within-party shuffle |

| Community (label from its makeup) | Members | R | D | Exposed |
|---|---|---|---|---|
| Republican core | 124 | 117 | 7 | 16 |
| Democratic core | 101 | 6 | 95 | 14 |
| Texas, Connecticut (and Ohio) | 41 | 25 | 16 | 6 |
| **Close seats** (New York, Michigan): Bacon, LaLota, Gillen, Scholten, Golden, J. Riley, Kaptur, Cuellar, Mannion, … | **37** | 19 | 18 | **19** |
| North Carolina, Minnesota (and Iowa) | 24 | 11 | 13 | 9 |
| Florida, Nevada | 21 | 14 | 7 | 9 |
| Maryland, Virginia | 21 | 6 | 15 | 5 |
| Washington, Oregon (and Arizona) | 19 | 4 | 15 | 5 |
| California, Hawaii | 14 | 6 | 8 | 5 |
| Two pairs (Rhode Island, New Hampshire) | 2 + 2 | 0 | 4 | 3 |

- **Labels:** a community is a "core" when over 90% is one party, "close seats" when at least half its members are
  exposed, and otherwise named by its two most common states.
- **Members by community:** `out/home_communities_members.csv`.
- **Caveat:** Louvain is random, so the best of 50 seeds is one partition among similar ones. The close-seat
  community's exact membership can change at the edges between runs.

### 3f. The picture itself (not a test)

Of each member's 10 nearest neighbours in the drawn layout, the share from the other party is 47 to 50% for exposed
members and 31 to 38% for safe members, over layout seeds 11, 12 and 13. It shows that the drawing places exposed
members where the parties meet. The tests are above.

## 4. Answers to the obvious questions

- **"Is this Watts–Strogatz?"** No. WS is a generative small-world model with a rewiring probability β. We test an
  observed network, so the null is the configuration model (§3a): no β, and every member's degree held fixed by
  double-edge swaps.
- **"How does the null connect to the backbone?"** It doesn't. The null runs on all 6,732 cross-party ties. The
  backbone is used only for the drawing and for path-based centrality, where the full map is too dense for paths to
  mean anything.
- **"Why α = 0.01?"** Readability: every member stays connected with about 4 ties each. Results that use the backbone
  (§3d) depend on it; the tests in §3a to §3c and the communities (§3e) do not.
- **"Only 10 comparisons?"** All 406 members are in every calculation. The 10 are tests (5 measures × 2 parties),
  corrected with Holm (§3d).
- **"Naming means praise?"** No. It means naming; tone is not measured here.
