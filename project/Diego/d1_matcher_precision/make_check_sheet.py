"""D1: write CHECK.md, the 100 main-sample matches in a form that is quick to read by hand.

Run from project/:  python Diego/d1_matcher_precision/make_check_sheet.py
"""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).parent
L = pd.read_csv(HERE / "labels.csv", dtype=str, keep_default_na=False)
L = L[L["sample"] == "main"]
out = ["# D1: the 100 matches to check by hand", "",
       "For each item: does the **bold** text refer to the member named in the heading, and did the speaker say it?",
       "Claude's verdict is shown under each item. Read all 100, then reply in the project thread with the item numbers",
       "you disagree with and your verdict (`correct`, `wrong_person` or `not_spoken`). Claude writes your answers into",
       "the `diego_check` column of `labels.csv` and reruns the scoring. Silence on an item means you agree with it.",
       "About 15 minutes.", ""]
todo = list(L[L.diego_check == ""].item)
if todo:
    out += [f"**Still to check: items {', '.join(todo)}.** An earlier version of this sheet put the bold on a Record page",
            "number such as [Page H744] instead of the matched name in these rows. The bold is now on the name.", ""]
for r in L.itertuples():
    w = r.wide_context
    i = w.index("[[" + r.matched_text)          # not w.index("[["): the Record's own [[Page H123]] markers come first in some rows
    j = i + 2 + len(r.matched_text)
    snippet = (w[max(0, i - 220):i] + "**" + w[i + 2:j] + "**" + w[j + 2:j + 2 + 160]).replace("[[Page", "[Page").replace("]]", "]")
    flag = " ⚠" if r.verdict != "correct" else ""
    out += [f"**{r.item}.** {r.speaker_name} ({r.speaker_party}) → {r.named_name} ({r.named_party}, {r.named_state})", "",
            f"> …{snippet}…", "", f"Claude: `{r.verdict}`{flag}" + (f". {r.note}" if r.note else ""), ""]
(HERE / "CHECK.md").write_text("\n".join(out), encoding="utf-8")
print("wrote CHECK.md with", len(L), "items")
