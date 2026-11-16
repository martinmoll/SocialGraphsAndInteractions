# D4: Introduction, Discussion and reflection (drafts)

Diego Mijares with Claude, 14 November 2026. Drafts to be moved into Overleaf after the 18 November
meeting.

**Placeholders.** Anything in `[[double brackets]]` is not known yet and must be replaced after the freeze
on 22 November. The prototype's numbers (34% and 12% cross-party at equal size) appear nowhere below,
because the definitions behind them are not agreed. Citation keys are those of `references.bib`.

**Length.** Introduction about 380 words, Discussion about 430, for a six-page PNAS paper with three
figures. Both can lose a paragraph if space is short: the third of the Introduction, the fourth of the
Discussion.

---

## Introduction

The United States Congress is usually described as two camps, and most ways of measuring it agree. Members
of the two parties vote apart, and they have used increasingly different words since the early 1990s
\cite{gentzkow2019}. Networks built from who signs whose bills show the same split, with ties between the
parties growing rarer and more hostile over four decades \cite{neal2020}.

How deep the split looks depends, however, on which record is read. Harbridge showed that between 1973 and
2004 bipartisan agreement fell in roll-call votes while staying far more stable in cosponsorship, because
party leaders chose which bills reached a vote \cite{harbridge2015}. Across communication channels the
parties are always distinguishable, but more so in front of national audiences than local ones
\cite{green2024}. Division is a property of the measurement as well as of the institution.

Members also have reasons to manage how divided they appear. Voters with weak party attachments reward a
bipartisan image \cite{harbridge2011}, and what members say to constituents is a strategic presentation of
their work \cite{grimmer2013}. The presentation need not match the work: floor speeches that use the word
"bipartisan" are no more likely to concern bills with support from both parties \cite{westwood2022}.

We compare two records of the same 450 members of the House in the 119th Congress (2025–26). The first is
the cosponsorship network \cite{fowler2006}: two members are tied when one signs a bill the other
sponsors. The second is new to our knowledge:[^novel] two members are tied when one names the other in a
speech on the House floor. Both are networks on identical nodes, so the same measure, the modularity of
the partition into two parties tested against degree-preserving rewiring, applies to each. A word such as
"bipartisan" costs nothing to say. A name identifies a specific colleague, and it can be checked against
whether the two have worked together.

Whether naming is more or less partisan than working cannot be guessed in advance. Members might attack
the other side in public and cooperate quietly, or they might display the few cross-party partners they
have. We find that the floor map is `[[less / more / no differently]]` divided by party than the working
map at equal density (cross-party share `[[x]]`% against `[[y]]`%). Reading a sample of cross-party
mentions by hand shows that `[[most express agreement / most express disagreement]]`, so the difference
reflects `[[whom members credit / whom members argue with]]`. In press releases from `[[n]]` Republicans,
`[[one-sentence result of the close-up, or delete if the collection stops after A2]]`.

---

## Discussion

Drawn from the same speeches and bills, the House looks `[[less]]` divided in whom its members name than
in whom they work with. The comparison holds when the two networks have the same number of ties, when
yields of floor time are removed, and under a null model that keeps `[[who spoke in the same debate]]`
fixed `[[M4: confirm it survives, or rewrite this sentence]]`.

`[[Version A, if most cross-party mentions are coded agreeing.]]` The hand-coded sample says what these
ties are. Of `[[150]]` cross-party mentions, `[[a]]`% credit or thank the named member, `[[d]]`% argue with
them and `[[p]]`% are procedure (two coders, κ = `[[k]]`). The floor is therefore where cross-party work is
acknowledged: a bill's manager thanks its co-lead and the committee's leaders of both parties. Much of
this is courtesy, and courtesy is itself informative, since it is extended across the aisle as a matter of
routine in a chamber that votes along party lines.

`[[Version B, if most are coded disagreeing.]]` The hand-coded sample changes the reading. Of `[[150]]`
cross-party mentions, `[[d]]`% argue with the named member and only `[[a]]`% credit them (two coders,
κ = `[[k]]`). Members name the other side mainly to oppose it. In Neal's terms \cite{neal2020}, the floor
map contains many negative ties, and a network that ignores sign mistakes conflict for contact. The floor
is less segregated than the working map and no less polarized.

The result does not show that members cooperate more than cosponsorship suggests. A mention is a
reference, made in a setting where debate time is divided between a majority and a minority manager, and
part of the cross-party contact follows from that format. Nor is the comparison independent of how the
dense cosponsorship network is thinned: with every tie kept its cross-party share is `[[z]]`%, closer to
the floor map than the equal-size version is.

One limitation we found ourselves. Checking 100 name matches gave a precision of `[[93]]`%
(`[[86 to 97]]`), and the errors were not neutral: `[[5 of 7]]` joined members of different parties,
because a constituent or a namesake who is mistaken for a member belongs to the other party about half the
time. Matching errors therefore make the floor map look less divided than it is. The errors we could
identify mechanically moved the cross-party share by `[[0.1]]` percentage points, far less than the gap
between the maps, but the bias runs in the direction of our finding and we could not measure recall.[^d1]

The floor is the Washington audience. `[[Close-up paragraph: what the press releases add about which
partners members show at home, with the test against the member's own bills. Delete if A3 to A5 are
dropped.]]` Where Westwood found that the word "bipartisan" is detached from behaviour
\cite{westwood2022}, named partners are `[[tied / not tied]]` to the cosponsorship record. One Congress
and one chamber cannot say whether this is stable. The same two maps can be drawn for any Congress since
the Record went online.

---

## Reflection (half a page, ungraded)

The question set by the course: did the "From an AI-drafted report" boxes on the week pages change how you
read your own draft, and where in your own report work did you use them, or not?

*This draft reports only what has happened up to 14 November. The group has not yet read a full draft
against the boxes, so the second half is a frame to fill in on 25 November. The reflection is in the
group's voice and all three members should recognise it before it is handed in.*

We built this project with AI assistants throughout: Claude wrote most of the code, proposed and reviewed
the research questions, and drafted text, and `docs/AI_METHODS.md` lists where. The boxes mattered less as
writing advice than as a list of things a fluent draft leaves out.

The week 8 box ("five methods, three numbers, zero questions") is the one closest to our project. Its
example reports a modularity with no null and methods that are never compared with each other. Our
prototype produced a clean headline within a day, and the box is a fair description of what that headline
would have been without the rewired networks, the equal-size comparison and the hand-coded sample.
`[[Martin and Anas: did the box prompt those checks, or were they planned anyway? Say which. "They did
not help" is an accepted answer.]]`

The box on names that are not yet resolved entities `[[week 7; Diego to confirm the wording on the page]]`
described our name matcher. The notebook printed thirty matches and all but one looked right. Counting
them properly showed something the printout could not: `[[7 of 100]]` wrong, and wrong mostly in the
direction of our finding. An AI assistant found those errors, which says something about the boxes too.
The risk they describe is not that the model cannot check its work but that nobody asks it to.

Where we did not use them: `[[to be written after the read-through on 25 November. Candidates: the
literature section, where the check was looking up each reference and not rereading the draft; the
figures.]]`

`[[One closing sentence from the group, in its own words.]]`

[^novel]: "New to our knowledge" rests on two short searches (see `d3_prior_work.md`). Diego took the
    decision to phrase it this way under Claude's guidance.
[^d1]: The numbers in this paragraph are the provisional D1 values and stay in brackets until Diego has
    checked the labels and Martin has rebuilt the matcher. Putting the direction of the matcher's bias in
    the Discussion, where a reader will see it, is a choice. Diego took it under Claude's guidance.
