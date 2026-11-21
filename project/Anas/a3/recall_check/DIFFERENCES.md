# A3.4: the 7 cases where the readers and the matcher disagree

Anas, for review. Prepared by Claude, Sat 21 Nov 2026.

**What this is.** Five blind AI readers listed every House member named in 40 press releases. In 7 places their
lists and the matcher's output differ. These 7 are the only places where the recall and precision numbers depend
on who is right. Everywhere else the readers and the matcher agree.

**What you'd do.** For each case, read the excerpt and tick who is right. Each takes under a minute. The link opens
the release on the member's own site if you want more context.

**Why it matters.** The readers are all AI, from one model family. The course asks for model output to be checked
against human labels, so your ticks are that check. Methods can then say *"the 7 cases where readers and matcher
disagreed were checked by hand."*

## Overview

| # | Release | Name in the text | Readers say | Matcher did | Now, with the press layer |
|---|---|---|---|---|---|
| 1 | Mike Johnson, 9 Feb 2026 | "Subcommittee Chair **Flood**" | Mike Flood, named | Missed it | Still missed |
| 2 | Maxine Dexter, 5 Aug 2025 | "Ranking Members Huffman and **Lofgren**" | Zoe Lofgren, named | Missed it | Still missed |
| 3 | Yvette Clarke, 13 Jan 2026 | "former Congresswomen … **Barbara Jordan**" | Not a sitting member | Counted Jim Jordan | Still counted |
| 4 | Ayanna Pressley, 19 Jun 2026 | "Reps. Pressley, Clarke, Demings and **Levin**" (2021) | Andy Levin, a former member | Counted Mike Levin | Still counted |
| 5 | Ayanna Pressley, 19 Jun 2026 | "Reps. **Cherfilus McCormick** and Yvette Clarke" | Sheila Cherfilus-McCormick | Counted Rich McCormick | Still counted |
| 6 | Riley Moore, 8 Jul 2025 | "Congressman **Riley M. Moore**" | Moore himself, so nobody | Counted Josh Riley | **Fixed** (the middle-initial rule) |
| 7 | Bonnie Watson Coleman, 23 Jul 2026 | "Representatives **Alma S. Adams**, Ph.D." | Alma Adams, named | Missed it | **Fixed** (the middle-initial rule) |

Cases 6 and 7 are already fixed. In those, the readers' reading is what the press layer now does, so a tick there
only confirms the fix. **Cases 1 to 5 are the ones that still count**:
- in 1 and 2 the matcher **missed** a name, which lowers recall;
- in 3, 4 and 5 it **counted the wrong member**, which lowers precision.

If you only have two minutes, do 3, 4 and 5. They are the ones where the matcher puts a wrong tie in the data.

---

## 1. Missed: "Subcommittee Chair Flood"

**Release:** Mike Johnson (R-LA), 9 Feb 2026, *House Passes the Housing for the 21st Century Act*
[link](https://mikejohnson.house.gov/news/documentsingle.aspx?DocumentID=2841)

> … The passage of the Housing for the 21st Century Act includes real, bipartisan solutions to expanding supply,
> lowering costs, and providing families with more options. I commend Ranking Member Waters, **Subcommittee Chair
> Flood**, and Subcommittee Ranking Member Cleaver on collaborating on this legislation …

- **Readers (5 of 5):** Mike Flood (R-NE), Financial Services subcommittee chair.
- **Matcher:** finds Waters and Cleaver ("Ranking Member" is a title word), but not Flood: "Chair" is not a title
  word, only "Chairman" is.
- **Claude's reading:** the readers are right. Flood is the only House Flood.

- [ ] Readers right (Flood is named, the matcher missed him)
- [ ] Matcher right
- [ ] Can't tell

## 2. Missed: "Ranking Members Huffman and Lofgren"

**Release:** Maxine Dexter (D-OR), 5 Aug 2025, *Top Democrats Condemn Trump's Federal Workforce Purge, …*
[link](https://dexter.house.gov/media/press-releases/top-democrats-condemn-trumps-federal-workforce-purge-back-bills-block-mass)

> "… Our country is better off with these federal employees on the job. I'm proud to join **Ranking Members Huffman
> and Lofgren** in stepping up to protect our civil servants …," said Vice Ranking Member Sarah Elfreth (D-Md.).

- **Readers (5 of 5):** Zoe Lofgren (D-CA).
- **Matcher:** finds Huffman but not Lofgren. The plural "Ranking Members" does not start a list, as "Reps." does.
- **Claude's reading:** the readers are right. Lofgren is the only House Lofgren, and ranking member of Science,
  Space, and Technology.

- [ ] Readers right (Lofgren is named, the matcher missed her)
- [ ] Matcher right
- [ ] Can't tell

## 3. Wrong member: "Barbara Jordan" counted as Jim Jordan

**Release:** Yvette D. Clarke (D-NY), 13 Jan 2026, *Clarke Celebrates the 113th Anniversary of Delta Sigma Theta*
[link](https://clarke.house.gov/clarke-celebrates-the-one-hundred-thirteenth-anniversary-of-delta-sigma-theta-sorority-inc/)

> … I also carry forward the wisdom and fortitude of trailblazing members such as **former Congresswomen Shirley
> Chisholm, Barbara Jordan, Marcia Fudge, Brenda Lawrence, and Val Demings**, sharing in their enduring legacy …

- **Readers (5 of 5):** nobody. Barbara Jordan (TX, 1973–79) is a former member, not in the member list.
- **Matcher:** "Congresswomen" is a plural title, so it reads the list and resolves "Jordan" to the only sitting
  Jordan, **Jim Jordan (R-OH)**. That is a false cross-party tie, Clarke (D) → Jordan (R).
- **Claude's reading:** the readers are right. "former Congresswomen" is the clue the matcher can't use.

- [ ] Readers right (no sitting member, the matcher's Jim Jordan is wrong)
- [ ] Matcher right
- [ ] Can't tell

## 4. Wrong member: "Demings and Levin" (2021) counted as Mike Levin

**Release:** Ayanna Pressley (D-MA), 19 Jun 2026, *Pressley Commends Senate Partners for … Haiti …* (a long
release with a timeline of her Haiti work)
[link](https://pressley.house.gov/2026/06/19/pressley-commends-senate-partners-for-introducing-bill-to-designate-haiti-for-temporary-protected-status-following-house-passage/)

> … In July 2021, the **Reps. Pressley, Clarke, Demings and Levin** issued a statement condemning the
> assassination of President Moïse and calling for swift and decisive action to bring political stability …

- **Readers (5 of 5):** not a sitting member. In 2021 this was **Andy Levin** (D-MI), co-chair of the Haiti Caucus,
  who left the House in January 2023.
- **Matcher:** resolves "Levin" to the only sitting Levin, **Mike Levin (D-CA)**. Same party, so no false
  cross-party tie, but a wrong tie Pressley → Mike Levin.
- **Claude's reading:** the readers are right, from outside knowledge. The text alone gives "July 2021" and the
  Haiti context, and Val Demings, listed with him, also left in 2023.

- [ ] Readers right (Andy Levin, the matcher's Mike Levin is wrong)
- [ ] Matcher right
- [ ] Can't tell

## 5. Wrong member: "Cherfilus McCormick" counted as Rich McCormick

**Release:** the same Pressley release as case 4.

> … On March 12, 2024, Rep. Pressley and **Haiti Caucus Co-Chairs Reps. Cherfilus McCormick and Yvette Clarke**
> issued a statement on the resignation of Haitian Prime Minister Ariel Henry …

- **Readers (5 of 5):** Sheila Cherfilus-McCormick (D-FL). The release drops her hyphen here.
- **Matcher:** without the hyphen it reads "McCormick" as the surname and resolves it to the only plain McCormick,
  **Rich McCormick (R-GA)**. That is a false cross-party tie, Pressley (D) → McCormick (R). Cherfilus-McCormick is
  also named in the same release with the hyphen, so she is counted there anyway.
- **Claude's reading:** the readers are right. "Haiti Caucus Co-Chairs" fits Cherfilus-McCormick, not Rich
  McCormick.

- [ ] Readers right (Cherfilus-McCormick, the matcher's Rich McCormick is wrong)
- [ ] Matcher right
- [ ] Can't tell

## 6. Fixed: "Congressman Riley M. Moore" counted as Josh Riley

**Release:** Riley M. Moore (R-WV), 8 Jul 2025, *Congressman Moore Announces Over $2 Million Recovered for West
Virginians* [link](https://rileymoore.house.gov/media/press-releases/congressman-moore-announces-over-2-million-recovered-west-virginians)

> Washington, D.C. – **Congressman Riley M. Moore** is proud to announce that he and his team have recovered over
> $2 million for West Virginians …

- **Readers (5 of 5):** nobody. This is Moore writing about himself.
- **Matcher:** stops at the initial "M." and reads "Riley" as the surname, giving **Josh Riley (D-NY)**. That is a
  false cross-party tie. Across all releases this bug produced 364 wrong mentions, 96% of them cross-party.
- **Now:** fixed by the press layer's middle-initial rule. Martin has it as `MATCHER_CHECKLIST.md` item 15.

- [ ] Readers right (confirms the fix)
- [ ] Matcher right
- [ ] Can't tell

## 7. Fixed: "Representatives Alma S. Adams, Ph.D." missed

**Release:** Bonnie Watson Coleman (D-NJ), 23 Jul 2026, *Adams, Frankel, Leger Fernández, Watson Coleman, Blunt
Rochester Introduce Black Women's Equal Pay Day Resolution*
[link](https://watsoncoleman.house.gov/newsroom/press-releases/adams-frankel-leger-fernandez-watson-coleman-blunt-rochester-introduce-black-womens-equal-pay-day-resolution)

> WASHINGTON, D.C. — Today, **Representatives Alma S. Adams, Ph.D. (NC-12)**, Lois Frankel (FL-22), Bonnie Watson
> Coleman (NJ-12), Teresa Leger Fernández (NM-03), and Senator Lisa Blunt Rochester (DE), introduced …

- **Readers (5 of 5):** Alma Adams (D-NC).
- **Matcher:** the same initial bug as case 6. It reads "Alma" as the surname and finds no member, so Adams is
  missed.
- **Now:** fixed by the middle-initial rule.

- [ ] Readers right (confirms the fix)
- [ ] Matcher right
- [ ] Can't tell

---

**After you've ticked:** tell Claude. If all are "readers right", nothing changes: the numbers in `a3/README.md`
(recall 0.97, precision 0.96 with the press layer) already assume the readers are right. If you tick "matcher
right" anywhere, the numbers are rescored with your answer.

My answers:

## 1. Missed: "Subcommittee Chair Flood"

**Release:** Mike Johnson (R-LA), 9 Feb 2026, *House Passes the Housing for the 21st Century Act*
[link](https://mikejohnson.house.gov/news/documentsingle.aspx?DocumentID=2841)

> … The passage of the Housing for the 21st Century Act includes real, bipartisan solutions to expanding supply,
> lowering costs, and providing families with more options. I commend Ranking Member Waters, **Subcommittee Chair
> Flood**, and Subcommittee Ranking Member Cleaver on collaborating on this legislation …

- **Readers (5 of 5):** Mike Flood (R-NE), Financial Services subcommittee chair.
- **Matcher:** finds Waters and Cleaver ("Ranking Member" is a title word), but not Flood: "Chair" is not a title
  word, only "Chairman" is.
- **Claude's reading:** the readers are right. Flood is the only House Flood.

- [x] Readers right (Flood is named, the matcher missed him)
- [ ] Matcher right
- [ ] Can't tell

## 2. Missed: "Ranking Members Huffman and Lofgren"

**Release:** Maxine Dexter (D-OR), 5 Aug 2025, *Top Democrats Condemn Trump's Federal Workforce Purge, …*
[link](https://dexter.house.gov/media/press-releases/top-democrats-condemn-trumps-federal-workforce-purge-back-bills-block-mass)

> "… Our country is better off with these federal employees on the job. I'm proud to join **Ranking Members Huffman
> and Lofgren** in stepping up to protect our civil servants …," said Vice Ranking Member Sarah Elfreth (D-Md.).

- **Readers (5 of 5):** Zoe Lofgren (D-CA).
- **Matcher:** finds Huffman but not Lofgren. The plural "Ranking Members" does not start a list, as "Reps." does.
- **Claude's reading:** the readers are right. Lofgren is the only House Lofgren, and ranking member of Science,
  Space, and Technology.

- [x] Readers right (Lofgren is named, the matcher missed her)
- [ ] Matcher right
- [ ] Can't tell

## 3. Wrong member: "Barbara Jordan" counted as Jim Jordan

**Release:** Yvette D. Clarke (D-NY), 13 Jan 2026, *Clarke Celebrates the 113th Anniversary of Delta Sigma Theta*
[link](https://clarke.house.gov/clarke-celebrates-the-one-hundred-thirteenth-anniversary-of-delta-sigma-theta-sorority-inc/)

> … I also carry forward the wisdom and fortitude of trailblazing members such as **former Congresswomen Shirley
> Chisholm, Barbara Jordan, Marcia Fudge, Brenda Lawrence, and Val Demings**, sharing in their enduring legacy …

- **Readers (5 of 5):** nobody. Barbara Jordan (TX, 1973–79) is a former member, not in the member list.
- **Matcher:** "Congresswomen" is a plural title, so it reads the list and resolves "Jordan" to the only sitting
  Jordan, **Jim Jordan (R-OH)**. That is a false cross-party tie, Clarke (D) → Jordan (R).
- **Claude's reading:** the readers are right. "former Congresswomen" is the clue the matcher can't use.

- [x] Readers right (no sitting member, the matcher's Jim Jordan is wrong)
- [ ] Matcher right
- [ ] Can't tell

## 4. Wrong member: "Demings and Levin" (2021) counted as Mike Levin

**Release:** Ayanna Pressley (D-MA), 19 Jun 2026, *Pressley Commends Senate Partners for … Haiti …* (a long
release with a timeline of her Haiti work)
[link](https://pressley.house.gov/2026/06/19/pressley-commends-senate-partners-for-introducing-bill-to-designate-haiti-for-temporary-protected-status-following-house-passage/)

> … In July 2021, the **Reps. Pressley, Clarke, Demings and Levin** issued a statement condemning the
> assassination of President Moïse and calling for swift and decisive action to bring political stability …

- **Readers (5 of 5):** not a sitting member. In 2021 this was **Andy Levin** (D-MI), co-chair of the Haiti Caucus,
  who left the House in January 2023.
- **Matcher:** resolves "Levin" to the only sitting Levin, **Mike Levin (D-CA)**. Same party, so no false
  cross-party tie, but a wrong tie Pressley → Mike Levin.
- **Claude's reading:** the readers are right, from outside knowledge. The text alone gives "July 2021" and the
  Haiti context, and Val Demings, listed with him, also left in 2023.

- [x] Readers right (Andy Levin, the matcher's Mike Levin is wrong)
- [ ] Matcher right
- [ ] Can't tell

## 5. Wrong member: "Cherfilus McCormick" counted as Rich McCormick

**Release:** the same Pressley release as case 4.

> … On March 12, 2024, Rep. Pressley and **Haiti Caucus Co-Chairs Reps. Cherfilus McCormick and Yvette Clarke**
> issued a statement on the resignation of Haitian Prime Minister Ariel Henry …

- **Readers (5 of 5):** Sheila Cherfilus-McCormick (D-FL). The release drops her hyphen here.
- **Matcher:** without the hyphen it reads "McCormick" as the surname and resolves it to the only plain McCormick,
  **Rich McCormick (R-GA)**. That is a false cross-party tie, Pressley (D) → McCormick (R). Cherfilus-McCormick is
  also named in the same release with the hyphen, so she is counted there anyway.
- **Claude's reading:** the readers are right. "Haiti Caucus Co-Chairs" fits Cherfilus-McCormick, not Rich
  McCormick.

- [x] Readers right (Cherfilus-McCormick, the matcher's Rich McCormick is wrong)
- [ ] Matcher right
- [ ] Can't tell

## 6. Fixed: "Congressman Riley M. Moore" counted as Josh Riley

**Release:** Riley M. Moore (R-WV), 8 Jul 2025, *Congressman Moore Announces Over $2 Million Recovered for West
Virginians* [link](https://rileymoore.house.gov/media/press-releases/congressman-moore-announces-over-2-million-recovered-west-virginians)

> Washington, D.C. – **Congressman Riley M. Moore** is proud to announce that he and his team have recovered over
> $2 million for West Virginians …

- **Readers (5 of 5):** nobody. This is Moore writing about himself.
- **Matcher:** stops at the initial "M." and reads "Riley" as the surname, giving **Josh Riley (D-NY)**. That is a
  false cross-party tie. Across all releases this bug produced 364 wrong mentions, 96% of them cross-party.
- **Now:** fixed by the press layer's middle-initial rule. Martin has it as `MATCHER_CHECKLIST.md` item 15.

- [x] Readers right (confirms the fix)
- [ ] Matcher right
- [ ] Can't tell

## 7. Fixed: "Representatives Alma S. Adams, Ph.D." missed

**Release:** Bonnie Watson Coleman (D-NJ), 23 Jul 2026, *Adams, Frankel, Leger Fernández, Watson Coleman, Blunt
Rochester Introduce Black Women's Equal Pay Day Resolution*
[link](https://watsoncoleman.house.gov/newsroom/press-releases/adams-frankel-leger-fernandez-watson-coleman-blunt-rochester-introduce-black-womens-equal-pay-day-resolution)

> WASHINGTON, D.C. — Today, **Representatives Alma S. Adams, Ph.D. (NC-12)**, Lois Frankel (FL-22), Bonnie Watson
> Coleman (NJ-12), Teresa Leger Fernández (NM-03), and Senator Lisa Blunt Rochester (DE), introduced …

- **Readers (5 of 5):** Alma Adams (D-NC).
- **Matcher:** the same initial bug as case 6. It reads "Alma" as the surname and finds no member, so Adams is
  missed.
- **Now:** fixed by the middle-initial rule.

- [x] Readers right (confirms the fix)
- [ ] Matcher right
- [ ] Can't tell

---
