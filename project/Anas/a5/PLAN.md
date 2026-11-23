# A5: does a release that says "bipartisan" name a real cross-party partner?

Anas with Claude, Sun 22 Nov 2026, 23:00. **Written before anything was computed.** Only the word count was looked
at first (14,111 of 55,021 releases in the window, 26%, from 409 members), to size the work. Anas approved the four
choices below in the chat ("Yes, start A5").

**Scope (G17):** A5 is an optional item that had to be finished by Sun 22 Nov. The numbers are meant to exist
tonight; the reading check may run into Monday. Martin and Diego decide whether it stays in.

## The question

When a member's release calls something bipartisan, is there a partner from the other party in the House to back
it, by name in the release or on the record of a bill the release cites? Prior work (Westwood) found the word
"bipartisan" detached from votes; this asks the same of the partners.

## Fixed choices

1. **"Says bipartisan":** `\bbi-?partisan` (any case) in the title or body, after removing the member's own repeated
   sentences (`a3/out/repeated_sentences.csv`; a boilerplate "I work across the aisle" line is not this release's
   claim). Template releases are left out (`release_flags.template`). Window 3 Jan 2025 to 20 Nov 2026, as A4.
2. **"A real partner,"** two measures and their union:
   - **Named:** the release names a House member of the other party (`a3/out/mentions_press.parquet`,
     `cross_party`), party leaders left out (`named_is_leader`). Co-leads count here, since a co-lead is a partner.
   - **On record:** the release cites a House bill (`a3/out/release_bills.csv`, status resolved) whose sponsor or a
     non-withdrawn original cosponsor is from the other party than the releasing member.
   - **Either:** named or on record (the main measure).
3. **The comparison:**
   - **Main:** among each member's "bipartisan" releases, the share with a partner (either measure); the mean over
     members, so prolific members do not dominate. Members need at least 5 "bipartisan" releases.
   - **Baseline:** the same share among the same members' other releases. The word should carry a partner far more
     often than releases that do not use it.
   - **Pooled release shares** are reported beside it.
   - **By seat (ties to A4):** exposed against safe within party (`exposed_2025`), same permutation test as A4
     (10,000 shuffles within party, seed 2805).
4. **The reading check:** 30 "bipartisan" releases with no partner on either measure, drawn at random (seed 2805).
   Three blind AI readers each code every release with one of:
   - **S**: a senator of the other party is the partner (our matcher never matches senators);
   - **H**: a House member of the other party is named but the matcher missed them;
   - **O**: a partner outside Congress (governor, state legislature, administration, local officials);
   - **V**: vague, with no partner named ("bipartisan support", "a bipartisan bill", "bipartisan vote");
   - **X**: other (the word in a quote, a name, a group such as "Bipartisan Policy Center").

   Anas reads every release where the readers disagree. The S and H shares say how much "no partner" is our
   instrument's blind spot rather than the release.

## Limits known in advance

- **Senate partners are invisible to both measures** (the matcher skips senators; bill links cover House bills only).
  The check measures this.
- **"On record" uses original cosponsors only;** a partner who joined later is not counted.
- **One release can say "bipartisan" about something other than the member's own work** (a vote, another bill). The
  check measures this too (V and X).

## Outputs

`a5/analysis.py` → `a5/out/results.csv`, `a5/out/member_shares.csv`; `a5/check/` (packet, readers' answers, scores);
`a5/README.md`.

## Addendum, Mon 23 Nov 2026: the mirror check (written before anything was drawn or read)

Anas approved the design in the chat ("Yes, start it"), as proposed in `HANDOFF_2026-11-23.md`.

**Why:** "named" counts any House member of the other party named in a "bipartisan" release as a partner. A release
can name one as an opponent ("my bipartisan bill, which Rep. X blocked"). The 63.9% (either) leans on this; the
on-record 36.9% does not.

- **Sample:** 30 random "bipartisan" releases of the A4 members with a named partner (`a5/out/release_flags.parquet`,
  `says & named`; pool 7,192 releases), seed 2805. For each, the named other-party House members that make it count
  (`a3/out/mentions_press.parquet`, `cross_party`, not `named_is_leader`), with the sentence they are named in.
- **Question, per release:** is a named other-party member a partner in what the release calls bipartisan? One code
  per release, the first that applies in this order (the measure needs only one partner):
  - **P** partner: co-lead, co-sponsor, co-signer, joint letter, event or caucus, thanked for joint work;
  - **C** criticised or opposed;
  - **M** mentioned without partnership (a neutral reference);
  - **N** not that member (the text means someone else: a wrong match).
- **Readers:** three blind sub-agents (two Opus, one Sonnet), packet only (`a5/mirror/packet/`), forbidden to write
  any other file; the example row uses a made-up id.
- **Anas** reads only the releases where the readers differ, in `a5/mirror/DIFFERENCES.md` (excerpt, link, tick
  boxes); the codes Anas gives go in `a5/mirror/anas_codes.csv`.
- **Decision rule, fixed now:** if P is 27 or more of 30, the named and either figures stand, reported with the P
  share as their check. If not, the paper leads with the on-record figure and gives the named one with its P share.
