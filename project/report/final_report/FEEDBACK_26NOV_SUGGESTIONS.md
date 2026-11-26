# Martin's comments on the final report (26 Nov): suggested changes

Source: Martin's annotated PDF of `two_maps_full_draft_overleaf/main.pdf` (13 notes and two hand-drawn marks).
Line numbers refer to `two_maps_full_draft_overleaf/main.tex` as of 26 Nov. **Nothing is applied yet.** No number
changes; every new sentence uses numbers or facts already in the paper or the repository.

The rewrites follow the humanizer rules by hand: plain words, no em dashes, no inflated vocabulary, no padding lists,
no "not only … but also". The `/humanizer` skill is not installed in this cloud session, so I couldn't run it here.

---

## 1. Abstract, last sentence: "What does this mean?" (page 1, line 67)

**Now:** How divided Congress looks depends on which record is read.

**Why it is unclear:** "record" is doing too much work. The reader has to guess that it means bills, speeches or
press releases.

**Suggested:** The same members look more or less divided depending on the record we read: their bills, their floor
speeches or their press releases.

(+9 words. The abstract is at about 150 words, so cut 9 words elsewhere. One option is "Reading 100 mentions by hand
shows" → "Hand-coding 100 mentions shows", which saves 2 words.)

## 2. Significance statement: "Improve this section. It is not a 'WOW!' reading, yet." (page 1, lines 36–40)

**Problem:** it opens with background ("Congress is described as two camps") instead of the finding, and the finding
is buried in one long sentence.

**Suggested (about 100 words, within PNAS's 50–120):**

> The US House looks less divided when you ask whom its members name than when you ask whom they work with.
> Polarization is usually measured from votes or vocabulary, and both show two camps. We drew the same 450 members
> twice. On the floor, members name colleagues of the other party more often than they cosponsor bills with them,
> and mostly to give them credit. In press releases, members in close districts name the other party most, and
> mostly name partners. How polarized Congress looks depends on the record you choose, and a named partner, unlike
> the word "bipartisan", can be checked against the bills.

It opens on the finding, uses one short sentence per idea, and ends with the point about method.

## 3. Empty space on page 1 under the Significance box: "Is this space needed?"

The space comes from the PNAS template. On page 1 the narrow right column holds only the Significance box, with the
affiliations and contributions pinned to the bottom, so nothing else flows into it.

**Suggested:** the longer Significance statement in item 2 fills about a third of the gap. To fill more of it, the
author-contributions footnote can be longer, since the course wants contributions "specific, per person". Beyond that
the gap belongs to the template, and there is no clean way to put body text there.

## 4. Empty space on page 2 above the Figure 1 caption: "Can this be used more efficiently?"

The side caption (`SCfigure*`, line 124) is shorter than the figure, and LaTeX aligns it to the bottom, so a block of
blank space sits above it. Two options, cheapest first:

- **a.** Give more width to the figure and less to the caption: `\begin{SCfigure*}[0.4][t]` and
  `width=12.4cm`. A narrower caption column runs longer and fills the height, and the maps get bigger.
- **b.** Go back to the full-width Figure 1 (`figures/figure1.pdf`, 17.8 cm) with the caption underneath. This
  removes the gap entirely but costs about 4 lines of text, because a caption under the figure is shorter and wider.

Not compiled: there is no LaTeX here, so check the page break in Overleaf.

## 5. "Yields": "state what yielding means the first time we encounter it" (page 2, Results, lines 140–141, and the Figure 1 caption, line 128)

The first time a reader meets the word is the Figure 1 caption, then the Results text. Neither explains it until
Methods.

**Results, now:** … leaving out yields of debate time (3,970 ties from 8,469 mentions; Methods).

**Suggested:** … leaving out yields, the moments when the member managing a debate hands speaking time to a
colleague by name ("I yield 2 minutes to the gentleman from Texas", as in Methods), which are procedure rather than a choice
to name someone (3,970 ties from 8,469 mentions; Methods).

**Figure 1 caption, now:** yields of debate time left out.
**Suggested:** yields (handing over debate time) left out.

## 6. Two headings stacked: "Why is one small size, the other large. Can we merge the two?" (page 3, lines 206 and 222)

The subsection heading "Close-up: whom members name at home" is directly followed by a run-in bold heading. Parts 1
and 2 start their subsections with plain text, so part 3 is the odd one out.

**Suggested:** keep the subsection heading and drop the bold run-in in the first paragraph. Its claim moves into
the paragraph:

> We asked whom members name in their own press releases, and whether members whose seat is at risk name the other
> party more. They do, in both parties. For each of the 406 members …

## 7. "Two coders agreed": "should be clear that this is us, the authors" (page 3, line 183)

**Now:** Two coders agreed on 82% of the mentions (Cohen's κ = 0.64).

**Suggested:** Where two of us coded the same mention independently (50 mentions), we agreed on 82% (Cohen's
κ = 0.64).

Fact check: Diego coded all 100, and Martin and Anas coded 25 each, so human pairs exist on 50 mentions. Methods
(line 395) says the same.

## 8. "Three blind AI readers": "Too ambiguous. Name provider and model (opus 5.5)" (page 3, line 242; page 4, line 285; Methods lines 409, 412, 423)

**Correction before writing "Opus 5.5":** Anas's records say the readers were not all Opus. They were two Claude
Opus and one Claude Sonnet (checks T, A5 and the bill links), and three Opus and two Sonnet for the press recall
check (`docs/AI_METHODS.md` rows 9 and 11b–11e; `Anas/a3/README.md`, `Anas/a4/README.md`). The repository does not
record model versions, so **Anas should confirm the versions** before they go in the paper.

**Suggested:** define the readers once in Methods and use a short name in Results.

- Results (line 242): "Three AI readers (Claude models from Anthropic; Methods), who did not see the seat, coded 60
  counted names …"
- Results (line 285): "Three AI readers (Methods) checked 30 releases of each kind …"
- Methods, new first sentence of "Exposure and tests" or "AI use": "Where AI readers were used, each was a separate
  Claude session (Anthropic; two Claude Opus and one Claude Sonnet unless stated) given only a packet with the text
  to read and the written rules. It could not open other files and did not see party, seat or another reader's
  answers."
- Methods line 409: "five blind AI readers (Claude)" → "five AI readers (three Claude Opus, two Claude Sonnet)".

## 9. "Moderates" is not defined (page 4, lines 247–254)

**Suggested (the paragraph's opening):**

> **Exposed members are also their party's moderates, and the two cannot be separated.** We measure ideology with
> DW-NOMINATE, a standard score that places each member from liberal to conservative by their roll-call votes. A
> moderate is a member whose votes place them close to the other party. Split each party into five equal bands by
> this score: 22 of the 37 exposed Republicans are in the most moderate band, as are 27 of the 54 exposed Democrats,
> while the most extreme bands hold 3 and 2. …

The rest of the paragraph stays as it is. Since "roll-call votes" is defined in the Introduction (line 90), this
needs no new definition.

## 10. "blind": "In a controlled environment" (page 6, AI use, lines 440–441)

**Now:** AI coders and readers were used blind and next to human checks, and a person read every disagreement.

**Suggested:** AI coders and readers worked blind, in a controlled setting: each ran as a separate session with only
the text to code and the written rules, without party, seat or any other coder's answers, and a person read every
case where they disagreed.

(This is consistent with item 8. If item 8's Methods sentence goes in, this one can shorten to "AI coders and
readers worked blind (see above), and a person read every case where they disagreed.")

---

## Length

Items 2, 5, 8 and 9 add about 8 lines and items 6 and 7 save about 1, so about 7 lines net. The 25 Nov build had
about 34 free lines on page 6 (DECISIONS G22), so the paper should stay at six pages. Check this in Overleaf.
