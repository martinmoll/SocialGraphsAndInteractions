# Two checks on part 3's main result: designs fixed before anything is drawn or computed

Anas with Claude, Mon 23 Nov 2026, evening. **Status: approved by Anas in the chat ("Yes, run both") before anything was drawn or computed.**
Only design facts were looked at: the A4 outcome's definition (`a4/analysis.py`), the group sizes (R 37 exposed /
171 safe, D 54 / 144) and that all 406 members have a DW-NOMINATE score in `members.csv` (none missing).

**Why now:** the course grades "a check that the measurement works" and "a comparison that rules out the boring
explanation" (week 8). Part 3's main result has neither yet: we never read what the counted names do (T), and
exposed seats go with moderate members (I).

---

## Check T: what do the counted names do?

**Question.** When a member names a House member of the other party (not a co-lead, not a party leader, so exactly
what A4 counts), is it partnership, criticism or a plain mention? And is the mix different in exposed and safe seats?

**Why it matters.** The paper reads the result as display ("name", and in the Discussion "show"). If exposed members
name the other side more *to attack it* (2026 is an election year), the reading changes. Part 2's hand labels cover
floor mentions only; today's A5 mirror check covers "bipartisan" releases only.

**Sample** (`a4/check_tone/`, seed 2805):
- **Population:** the mentions A4 counts: `a3/out/mentions_press.parquet` rows with `cross_party`, not
  `named_is_leader`, not `co_lead`, in a release of an A4 member inside the window with template posts left out.
- **Four cells** (party × seat), **15 items each, 60 in all.** Equal cells so that the small exposed groups are
  not swamped.
- **Drawn member first, then release:** in each cell, draw 15 members at random without replacement from those with
  at least one counted mention; for each, one random qualifying release; in that release, one random named
  other-party member. Members first, because A4's outcome is a mean over members, not over releases.

**What the readers see:** releasing member's name and party; the named member's name and party; the release title,
its first 1,200 characters, and every sentence naming that member with two sentences either side (at most 3,500
characters). **Not shown:** the district lean or whether the seat is exposed, and the cell. Items are shuffled.

**Codes** (one per item, about the named member):

| Code | Meaning |
|---|---|
| P | **Partner or praise:** works with the releasing member (joint letter, bill, event, caucus), or is thanked or praised |
| C | **Criticised or opposed:** blamed, attacked, named as someone who blocked, voted against or is wrong |
| M | **Mentioned, neither:** neutral reference (chairs a committee, attended, one of a list, a letter's addressee) |
| N | **Not that member:** the text means someone else (wrong match) |

Mixed cases, fixed now: if the release both works with and criticises the member, code **C** (criticism is the
reading that would change our story, so it wins ties). If unsure between P and M, **M**.

**Readers:** three blind AI readers (two Opus, one Sonnet), packet only, forbidden to read or write any other file;
the example row uses a made-up id. **Anas reads** every item where the readers differ, plus any close call all
three flag if it could move a cell's C share across the 25% line below. `DIFFERENCES.md` with excerpts, links and
tick boxes, as for A5.

**Reported:** P, C, M, N shares per cell and for exposed vs safe within each party, with Wilson 95% intervals. N
shares are a second precision estimate for the A4 outcome. Difference in C share, exposed − safe, with a permutation
p (seat labels shuffled among the 30 items of each party, 10,000 shuffles). With 15 per cell this can find only large
differences; it is a check, not a new test, and is reported as such.

**Reading, fixed now:**

| Result | What it means for part 3 |
|---|---|
| C is 25% or less in every cell | Counted names are mostly partnership or neutral. "Name" stands; the Discussion can say the names are mostly partners (with the share) |
| C over 25% in some cell, no clear exposed–safe difference | Naming includes much criticism in both seat types. Text says "name, often to criticise"; Discussion drops "show" |
| C clearly higher in exposed seats (difference of 20 points or more) | Part of the exposed gap is attack. Part 3 must say so; the "display" reading goes |

**Time:** draw and packet 10 min, readers 5 min, scoring 5 min, Anas's reading 10–15 min.

---

## Check I: is "exposed" just "moderate"?

**Question.** Do exposed members name the other party more than safe members *of similar ideology*?

**Why it matters.** Moderates tend to sit in swing seats. If moderates name the other side more wherever they sit,
A4's gap could be ideology, not the seat. This is the "boring explanation" a reader will raise first.

**Data:** `nominate_dim1` (DW-NOMINATE first dimension, 119th Congress) from `data/processed/members.csv`; all 406
A4 members have it. **Extremity** = dim1 for Republicans, −dim1 for Democrats (higher = further from the centre).

**Method:** the course's own logic for "part of your effect that degree already explained" (week 3), with ideology
in the place of degree:
- **Statistic:** A4's gap, unchanged (mean share exposed − safe, within each party).
- **Null A (A4 as reported):** shuffle `exposed` among a party's members.
- **Null B (new):** shuffle `exposed` only among members of the same party **and the same ideology band**: five
  bands, the party's quintiles of extremity. Null B keeps how many exposed members each band has, so it keeps the
  link between ideology and exposure, and breaks only what exposure adds within a band.
- **Reported, per party:** the observed gap; null B's mean (the gap expected from ideology alone); the observed gap
  minus that mean (the part beyond ideology); and p from null B. 10,000 shuffles, seed 2805.
- **Robustness:** three bands (terciles) instead of five. Reported beside the main row, whatever it shows.

**Reading, fixed now:**

| Result | What it means for part 3 |
|---|---|
| Gap beyond ideology positive with p < 0.05 in both parties | The seat effect holds among members of similar ideology: one clause in part 3 and the check in Methods |
| Positive in one party only | Report per party; the other party's gap cannot be told apart from ideology |
| Not distinguishable in either | Exposure and moderation cannot be separated with these data; part 3 says "consistent with a seat effect, which we cannot separate from ideology", and the Discussion names it as a limitation |

**Limits known in advance:**
- DW-NOMINATE comes from roll-call votes, and members in swing seats may vote more moderately *because* of the
  seat. Holding ideology fixed can then remove part of a real seat effect, so null B is a conservative test.
- With 37 exposed Republicans spread over five bands, some bands have few exposed members; the tercile row shows
  whether that matters.
- Check I is not from the course pages' examples, but its method is (week 3 stratified shuffle); only the
  stratifying variable is new. NOMINATE needs a citation (Voteview) if it enters the paper
  [UNVERIFIED: reference not yet looked up].

**Time:** 15 min (one script, no reading).

---

## After both

Rewrite part 3 to about 200 words with what T and I show, then copy to `report/` (checklist in
`../MESSAGES_23NOV.md`). Results go in `a4/README.md`; T's AI-reader rows go to Diego for `AI_METHODS.md`.
