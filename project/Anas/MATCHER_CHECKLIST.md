# Matcher checklist for Martin

**From Anas, 18 November 2026. For `Martin/matcher.py` (M1). You decide every item. Nothing here has been
changed in your files.**

**Status 20 Nov:** no decision yet. Items 9 (nicknames), 10 (state legislators) and 11 (recall check) were added on 20 Nov. **Suggested order: 9, 11, 1, 2, 10; then the rest.** Whatever is decided for the floor, the press side (A3) will apply items 1
and 2 to press releases: in 60 releases the current rules missed 3 names in lists and 26 colleagues named
without a title (on top of 198 found).

The press releases (A3, A4) will use your matcher, so the press side needs to know which version it is.
Each item below gives the proposed change, the course idea behind it, the evidence from **one run of your
matcher as it is today**, a recommendation, and when it would have to happen. Tick one box per item.

**Two deadlines decide most of this.**

- **Sun 22 Nov:** part 1 definitions freeze (G7). A change that adds or removes floor mentions changes the
  floor map, so it has to land before then or wait until after the paper.
- **G10:** matcher precision is measured from the D2 labelling sample, which the current matcher drew. A
  change that adds rows needs its own small hand check (20 to 30 rows) or a sentence in Methods saying
  the new rows were not checked.

How the evidence was made: `matcher_check/measure_floor.py` runs your `Matcher` over the floor turns that
`build_mentions.py` keeps (section H, at least 50 words, member speaker). `matcher_check/measure_press.py`
runs it over 60 recent press releases, 10 each from Golden, Kaptur, Vasquez, Lawler, Bacon and Fitzpatrick.
Every number is one run.

---

## Summary

| # | Proposed change | Floor | Press | Recommendation | When |
|---|---|---|---|---|---|
| 1 | Plural titles and name lists ("Reps. A, B and C") | 325 turns hold such a list | 3 names missed in 60 releases | **Do it** | Before Sun 22 Nov |
| 2 | Full names without a title ("Chip Roy") | 939 untitled vs 1,116 titled full names | +26 colleagues on top of 198 found | **Press: yes. Floor: hand-check 30 first** | Floor: before Sun; press: A3 |
| 3 | Carry a resolved name forward in the same turn | 58 of 783 dropped mentions | 3 dropped in 60 releases | Optional | Before Sun, or Methods note |
| 4 | Use `(R-ST)` tags in press releases | — | 16 tags, all already found; 1 was a senator | **No change to the matcher** | Anas's side |
| 5 | Guard against senators | 42 suspect contexts, all 8 read were correct | none found | Not needed; add a test | Any time |
| 6 | Hyphenated and multi-word surnames | — | — | Already works | Nothing to do |
| 7 | spaCy NER as the matcher | — | — | No | — |
| 8 | Unit of a mention (turn, release) | — | — | Write it in Methods | Draft, 24 Nov |
| 9 | **Nicknames as first names** (added 20 Nov) | 6 members dropped when named by nickname; about 72 such names on the floor | not yet measured | **Do it** | Before Sun 22 Nov |
| 10 | **Skip state legislators** ("State Rep. Smith") (added 20 Nov) | not measured | likely in home-state releases | Add a test; skip on "State" before the title | Before A3 |
| 11 | **Recall check on the floor** (added 20 Nov) | not measured: D1 and D2 measure precision only | Anas does it for press (A3) | **Do it**: 30 turns, one hour | Before Sun 22 Nov |

---

## 1. Plural titles and lists of names

- [ ] Need it  - [ ] Not needed  - [ ] Later

**The gap.** `TITLE` has `Rep\.` but not `Reps\.`, and a title captures one name. Tested on your matcher:

| Text | Found |
|---|---|
| "Reps. Lawler, Golden, and Fitzpatrick introduced the bill." | nobody |
| "Representatives Lawler and Golden introduced it." | Lawler only |
| "Congressmen Bacon and Golden wrote." | Bacon only |

**Evidence.** 325 of 17,824 floor turns contain a list after a plural title. On the press side, 12 lists in
60 releases, with 3 colleagues missed (most list members were found elsewhere in the same release).
How many floor mentions this adds is not measured. The rerun diff below gives it.

**Course idea.** Week 5, tokenization: the unit you match on decides what you can find. A rule written for
"Mr. Cole" does not see a list.

**How.** Add `Reps\.` to `TITLE`. After a plural title (`Reps.`, `Representatives`, `Congressmen`,
`Congresswomen`), split the following span on commas and "and", and resolve each name with the same rules
(longest surname first, then first name, then state). Give these hits `how="list after plural title"`.

**Check.** Rerun `build_mentions.py`, count the new rows by `how`, and read 20 of them.

**Why before Sunday.** It adds floor mentions, so it changes the floor map (G7).

## 2. Full names without a title

- [ ] Need it, both  - [ ] Press only  - [ ] Not needed

**The gap.** The matcher only looks after a title. "my colleague and friend, Chip Roy" is not found.

**Evidence.**

- **Floor:** a full name of a member ("First Last") appears 1,116 times after a title and 939 times without
  one. The untitled ones are mixed:
  - real mentions ("my colleague and friend, Chip Roy");
  - procedure ("tellers on the part of the Senate, Bryan Steil and Joseph Morelle");
  - non-members whose names contain a member's ("Jimmy 'James' Earl Carter" matches Earl Carter).
  
  How many are real is unknown until someone reads a sample.
- **Press:** 26 colleagues named only in full without a title, on top of the 198 the matcher finds (+13%):
  Golden names Bacon, Fitzpatrick, Young Kim and Gluesenkamp Perez this way. Press releases name colleagues
  this way far more than the floor does, and A4 is about exactly these names.

**Course idea.** Week 7, entities: extraction and resolution are separate steps. The title rule is a
high-precision extractor with limited recall, like spaCy's tagger in 7.8. Week 5, n-grams: "First Last" as
a bigram is what tells Al Green from Mark Green.

**How.** A second pattern: the roster's "First Last" pairs (also nickname pairs from members.csv's
`first`, e.g. "Chip"), anywhere in the text. Give these hits `how="full name, no title"` so they can be
filtered or reported separately. Skip lists that are procedure (a "tellers" or "appointed" window).

**Check.** Read 30 untitled floor hits. If most are real mentions, include them. If most are procedure or
non-members, use the rule for press only and say so in Methods.

**When.** Floor: before Sun 22 Nov, or not at all. Press: Anas uses it from A3, whatever the floor decision.
If the two sources use different rules, the Methods text has to say so, because part 1 compares floor
and press.

## 3. Carry a resolved name forward within a turn or release

- [ ] Need it  - [ ] Not needed

**The gap.** A shared surname with no first name and no state nearby is dropped, even when the same turn
already named that member in full ("Mr. Austin Scott … Mr. Scott").

**Evidence.** 783 floor mentions are dropped as "shared surname". 58 of them could be resolved by an
earlier unique resolution of the same surname **in the same turn**, which is 0.7% of the 8,092 mentions.
Another 173 could be resolved only by looking across the whole debate (`doc_id`). That is riskier, because a
debate can hold both Scotts. Press: 3 shared surnames dropped in 60 releases.

**Course idea.** Week 7, entity resolution: Peter, Peter Parker and Spider-Man; the first full mention
fixes who a later short form is.

**How.** Inside `find`, keep a dict surname → Bioguide of members already resolved in this text. When a
shared surname would be dropped and the dict has exactly one entry for it, use it,
`how="earlier in the turn"`. Do not carry across turns.

**Recommendation.** Small gain. Take it only if it is quick, otherwise write one sentence in Methods:
"783 of 9,008 titled names (8.7%) have a surname shared by several members and no first name or state
nearby, and are dropped."

## 4. `(R-ST)` tags in press releases

- [ ] Agree: no matcher change

**Evidence.** In the 60 releases, 16 names carry a party-state tag ("Rep. Mike Lawler (R-NY)"). The matcher
already resolves all of them through the title before the name. One tag named a senator: "US Senators
Mark Kelly (D-AZ)". Its surname matches a House member, but its state matches none.

**Recommendation.** Leave the matcher alone. On the press side, Anas uses the tag only as a check: a
tag whose state disagrees with every House member of that surname marks a senator or an outsider and
is dropped. An earlier name pilot (not your matcher) counted "Collins (R-ME)" as a House Collins because
it checked the party but not the state. That is the mistake to avoid.

## 5. Guard against senators

- [ ] Add a test only  - [ ] Not needed

**Evidence.** "Senator" and "Sen." are not titles in your matcher, so the 551 "Senator X" occurrences on the
floor are never matched. 546 floor mentions name a House member whose surname a senator shares (13
senators: Collins, Johnson, Kelly, Kennedy, Kim, Lee, McCormick, Moran, Murphy, Peters, Scott ×2, Smith).
42 of them have "Senate" in the context. The 8 I read were all the House member: Speaker Johnson, and Mike
Kennedy introduced by state. None in the press sample.

**Recommendation.** No rule. If you want it pinned, add one line to the self-check:
`assert mt.find("I thank Senator Collins.") == []`.

## 6. Hyphenated and multi-word surnames

- [x] Already handled

"Rep. Miller-Meeks", "Rep. Ocasio-Cortez", "Rep. Gluesenkamp Perez", "Rep. Van Duyne" and "Rep. Scott Franklin" all
resolve, because you match on raw text with longest surname first. A spaCy tokenizer would split the
hyphen (week 5: it splits "Spider-Man"). Keep matching on raw text.

## 7. spaCy NER instead of the title rule

- [ ] Agree: no

Week 7 shows `en_core_web_sm` missing names and mislabelling them. In our 7.8 exercise it found 47% of
the labelled people. Item 2 closes the main recall gap more cheaply and with known behaviour. NER could
serve as a recall check on a hand-labelled sample, but there is no time before Sunday.

## 8. What one mention is

- [ ] Written in Methods

Week 7: the unit of co-occurrence is a modelling decision. On the floor a tie is "named in a speaker
turn"; in press it is "named in a release". Both are directed (who names whom). One sentence in Methods,
next to the yield rule.

---

## 9. Nicknames as first names (added 20 Nov)

**Problem.** When two members share a surname, the matcher picks the right one by the first name in
`members.csv`. That is the official first name, so a member known by a nickname is dropped when named that way.

**Evidence** (one run of your matcher, 20 Nov):

| Text | Result |
|---|---|
| "Rep. Hank Johnson (D-GA) joined." | dropped (shared surname), even with the state tag next to it |
| "Rep. Henry Johnson joined." | J000288, by first name |
| "Rep. Bobby Scott", "Rep. Chris Smith", "Rep. Buddy Carter", "Rep. Hal Rogers", "Rep. Chuy Garcia" | all dropped |

Six members have this problem: the 19 members with a nickname in `unitedstates/congress-legislators`
(`name.nickname`), crossed with the shared surnames. Floor text (section H, turns of 50+ words) has about 72
uses of these six nickname forms (Chuy García 31, Chris Smith 15, Bobby Scott 14, Buddy Carter 8, Hank Johnson 2,
Hal Rogers 2). `mentions.parquet` has 54 mentions of the six in total and none of Hal Rogers. Not all 72 are
mentions (some are untitled or quoted), so this is the size of the problem, not the number of lost rows.

**Proposed change.** Accept the nickname as a second first name. The nicknames are in the same
`legislators-current.json` that `scripts/roster.py` already reads, so no new source is needed: about five lines
in `Matcher.__init__`, plus a test per member above.

**Course idea.** Week 7: one person, several names. The aliases list for named entities.

**Also worth a test:** the state tag `(D-GA)` did not break the tie here. Item 4 says tags are handled on the
press side, so this does not change your matcher, but a test would document it.

## 10. State legislators (added 20 Nov)

**Problem.** Press releases about home-state issues name state legislators: "State Representative Smith",
"State Sen. Johnson". With a title followed by a House surname, the matcher would count them as the House member.

**Proposed change.** Skip a match when the title is preceded by "State" (or "Assemblyman", "Delegate" in states
that use those words). Add a test. Not measured yet; A3 will count how often it happens in press releases.

## 11. Recall check on the floor (added 20 Nov)

**Problem.** The matcher's precision is measured: 98 of 100 in Diego's D2 sample (G10), where code X marks a
wrong match. Its recall is not. A sample drawn from `mentions.parquet` contains only names the matcher found,
so a missed name (item 9's nicknames, an unknown alias) can never show up in it. Part 1's floor map, part 2's
sample and part 3's press mentions all depend on recall.

**Proposed check.** Draw 30 floor turns at random from the turns `build_mentions.py` keeps (fixed seed). Read
each and list every House member named, in any form. Count how many the matcher finds. Report recall with a 95%
interval and the forms it missed. About an hour; the same check on 30 press releases is in Anas's plan (A3,
`methods_drafts.md` check 5), so the paper can give recall for both sources.

**Why before Sun 22 Nov.** If recall turns out low for a fixable reason (nicknames, lists), the fix has to land
before the freeze. If it is fine, the number goes in Methods as it is.

**What the paper can say.** *"The matcher found [x]% of named members in 30 hand-read floor turns and [y]% in
30 press releases."* No alias list is complete, so this is reported as a measured limitation, not removed.

## Files

- `matcher_check/measure_floor.py`: items 2, 3, 5, 6 on the floor. Run from `project/`:
  `python Anas/matcher_check/measure_floor.py Anas/press_scope/leg.json`. About 5 minutes.
- `matcher_check/measure_press.py`: items 1, 2, 4 on 60 press releases. Run from `project/`:
  `python Anas/matcher_check/measure_press.py Anas/press_scope/probe2.py Anas/press_scope/stage1.json out.json`.
  It fetches the releases again, so numbers can move as members post.
- `matcher_check/measure_press.json`: the hits, tags and missed names for each of the 60 releases.
