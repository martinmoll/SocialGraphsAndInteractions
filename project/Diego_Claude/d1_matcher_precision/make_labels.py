"""D1: the labels for the sampled matches.

Every label below was assigned by Claude (the AI assistant working with Diego) on 14 Nov 2026 after reading
the match with 400 characters of context either side, and the full turn where that was not enough. They are
a first pass. The column `diego_check` in labels.csv is empty until Diego has read the row himself:
write `ok` to confirm or the corrected verdict to overrule.

verdict
  correct       the matched text refers to the House member the matcher chose, and the speaker said it
  wrong_person  the matched text refers to somebody else (a constituent, another member, a film character)
  not_spoken    the member is the right one, but the text is Congressional Record boilerplate that the parser
                left inside the speaker's turn (a vote-change line or another member's speaker heading)
kind (correct rows only)
  yield         the mention yields time to the member or thanks the member for yielding
  other         any other reference
"""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).parent
WRONG = {
    5:   "Mrs. Peters is Carol Peters, a constituent of the speaker, not Scott Peters",
    37:  "Chairman Green is Mark Green (R-TN), then chair of Homeland Security, not Al Green (D-TX)",
    75:  "Mr. Turner is the late Sylvester Turner (D-TX), named in the previous sentence, not Michael Turner (R-OH)",
    99:  "Mrs. Cole is Bettie Cole, the person a post office is being named after, not Tom Cole",
    "S2": "Mr. Smith is the film character (Mr. Smith Goes to Washington); 'Washington' nearby selected Adam Smith (D-WA)",
    "S4": "Same sentence pair as S2: the film character, not Adam Smith",
}
NOT_SPOKEN = {
    56:  "Vote-change line printed after the vote (Mr. VEASEY changed his vote), not said by the speaker",
    68:  "Speaker heading of Mr. Hoyer's own turn (Mr. HOYER.--but what he did) left inside Mr. Mast's turn",
    96:  "Vote-change line printed after the vote (Ms. SCHOLTEN changed her vote)",
    "S11": "Vote-change line printed after the vote (Mr. DAVIS of Illinois)",
}
YIELD = {3, 13, 15, 18, 19, 20, 24, 27, 32, 45, 47, 55, 73, 74, 80, 84, 89, 93,
         "S1", "S3", "S6", "S8", "S10", "S13", "S15", "S16", "S18", "S19", "S28", "S35"}
NOTES = {
    12: "Flagged as a yield because 'yielding' is nearby, but the mention is a disagreement with Chairman Cole",
    21: "Thanks 'the chairman' for yielding, then praises Mr. Comer by name in the next sentence; counted as other",
    33: "Unanimous-consent request naming the debate managers; procedural but not a yield",
    52: "Flagged as a yield because of 'I yield myself the balance of my time'; the mention thanks the bill's sponsor",
    66: "Direct address to Ms. Clark in debate",
    "S59": "Inside a quotation from another member; the name still refers to Speaker Johnson",
}

frames = []
for f, sample in (("sample_main.csv", "main"), ("sample_supplement.csv", "supplement")):
    s = pd.read_csv(HERE / f, dtype={"item": str})
    s.insert(0, "sample", sample)
    frames.append(s)
L = pd.concat(frames, ignore_index=True)
key = [int(i) if i.isdigit() else i for i in L["item"]]
L["verdict"] = ["wrong_person" if k in WRONG else "not_spoken" if k in NOT_SPOKEN else "correct" for k in key]
L["kind"] = ["" if v != "correct" else "yield" if k in YIELD else "other" for k, v in zip(key, L.verdict)]
L["note"] = [WRONG.get(k) or NOT_SPOKEN.get(k) or NOTES.get(k, "") for k in key]
L["labelled_by"] = "Claude, first pass, 14 Nov 2026"
L["diego_check"] = ""
cols = ["sample", "item", "verdict", "kind", "note", "labelled_by", "diego_check", "speaker_name", "speaker_party",
        "named_name", "named_party", "named_state", "cross", "how", "is_yield", "is_leader_title", "day",
        "matched_text", "wide_context", "mention_row", "turn_row", "speaker", "named"]
old = HERE / "labels.csv"
if old.exists():                                    # never overwrite checks Diego has already entered
    prev = pd.read_csv(old, dtype=str).fillna("").set_index("item").diego_check
    L["diego_check"] = L["item"].map(prev).fillna("")
L[cols].to_csv(old, index=False)
print(L.groupby(["sample", "verdict"]).size().to_string())
