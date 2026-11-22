# G13: the swing-seat definition and the date window (for DECISIONS.md)

Anas, Sat 21 Nov 2026. **For Martin and Diego to agree to or change by the freeze on Sun 22 Nov.**

This is written here rather than in `DECISIONS.md` itself because Martin's newest `DECISIONS.md` is on his branch
(`claude/nice-bardeen-snc57e`) and not on `main` yet. An upload from this folder would risk overwriting it. Paste the
block below into G13's "Open" list, replacing open points 2 and 3. While doing so, please remove the draft headings
("Draft for G13", "Edit 1", "Edit 2") left above G13.

---

- **Status of open points 2 and 3:** decided by Anas 21 Nov, for Martin and Diego to agree to or change by Sun 22 Nov.
- **2. Swing seat ("exposed"):** `exposed_2025` in `Anas/district_lean/member_lean.csv`.
  - **Rule:** a member is exposed when the district they **served** leans toward their own party by 5 points or
    less (Cook PVI 2025, pinned 25 May 2025). Republican: lean ≤ R+5. Democrat: lean ≤ D+5. This includes members in
    seats that lean to the other party.
  - **Count:** 38 exposed Republicans and 59 exposed Democrats.
  - **Why the district served:** the releases were written for its voters. In the nine redrawn states the 2026 lean
    describes a different area.
- **3. Date window:** the full snapshot, 3 Jan 2025 to 20 Nov 2026 (press data collected 20 Nov). Both parties are
  compared over the same days. The floor data should end on or before 20 Nov too.
- **What the choice does** (A4, rerun 22 Nov on Martin's 22 Nov matcher, `Anas/a4/README.md`):
  - **Main result:** exposed members name the other party more than safe members in **both** parties (Republicans
    +4.1 points, Democrats +2.6, each p < 0.01). The interaction is small (+1.5 points, p 0.36). The reading fixed in
    advance is: a seat effect, not a president's-party effect.
  - **Cut-off:** 4 and 6 points, and the 2024 presidential margin as a second source, change the size of the gaps
    (R +3.6 to +6.4) but not their direction or the reading. The interaction comes closest to significant at 4
    points (+3.6, p 0.051).
  - **Lean as a number, all members** (`Anas/a4/out/figure_lean.png`): the share peaks in the closest seats, above
    all in the 18 crossover seats (members in districts leaning to the other party: Republicans 19.1%, Democrats
    14.0%). Beyond 5 to 10 points it is nearly flat at 8 to 10%. So the cut-off decides how much of that peak the
    exposed group holds, which is why its size moves with the cut-off and its direction does not.
- **Alternative and what it would change:** a tighter line (4 points) makes the Republican gap larger and hints at
  a president's-party effect (p 0.06). A looser one (6) shrinks both gaps a little. The 2026 district instead of the
  one served would relabel 12 members; without them and the 9 unknown, the result holds (check 1).
