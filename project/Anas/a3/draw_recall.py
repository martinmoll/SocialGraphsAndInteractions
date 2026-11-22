"""A3.4: draw the recall sample (A3_PLAN.md step A3.4; design decided by Anas 21 Nov).

Run from Anas/:  python a3/draw_recall.py --press press_releases --repo <project/ of the group repo>

Recall = names the matcher finds / names really in the text. A sample drawn from the matcher's own hits can never
contain a release where it missed everyone, so the sample is drawn without the matcher:

  pool     releases containing the surname of a House member other than the author (plain string search,
           accents folded, whole words, capitalised): 31,094 of 55,023      -> 30 releases (the recall number)
  outside  every other release: 23,929                                      -> 10 releases (checks that the pool
                                                                               loses nobody: they should name no one)

The 40 are shuffled together, and the sheet does not say which group a release is from, so both are read the same
way. Seed 2805. Anas lists every House member named in each release, in any form, without seeing the matcher's
hits; score_recall.py (written when the reading is done) compares with the matcher.

Writes recall_check/recall_sheet.xlsx (never overwritten once it exists) and recall_check/recall_draw.csv
(sample_id, url, group: the key, not to be opened before the reading is done).
"""
import argparse
import os
import re
import sys
import unicodedata

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_inputs

SEED, N_POOL, N_OUT = 2805, 30, 10
HOW_TO = [
    "How to read this sheet (A3.4 recall check)",
    "",
    "Each row is one whole press release, drawn at random. You do NOT see what the matcher found: that is the point.",
    "",
    "Open each release from the 'answers' tab (click its sample_id); the text is on its own tab, one paragraph",
    "per row. Back on 'answers', write in 'named_members' EVERY House member named in it, surnames separated by ';'.",
    "Count each member once per release, however often they are named.",
    "",
    "Counts: a name in any form: 'Rep. Lawler', 'Congressman Mike Lawler', 'Mike Lawler', 'Chuy García',",
    "  a name in a list or a co-sponsor list, a name inside a quote, 'Speaker Johnson', 'Leader Jeffries'.",
    "Does not count: the member whose release it is ('release_by'); a member described without a name",
    "  ('my colleague from Texas'); senators, governors, state legislators, the President, staff, constituents.",
    "Not sure whether someone is a sitting House member? Write the name with '?' and say why in 'note'.",
    "If the release names no House member, write: none",
    "",
    "Shared surnames (two Scotts, two Greens): write first name and surname, e.g. 'Austin Scott'.",
    "Leaders, template posts and repeated bio paragraphs: list them anyway; the scoring handles them.",
    "",
    "When done: tell Claude, which then writes and runs score_recall.py. Do not open recall_draw.csv before.",
]


def fold(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--press", required=True)
    ap.add_argument("--repo", required=True)
    a = ap.parse_args()
    d, members, *_ = load_inputs(a.press, a.repo)
    d = d.reset_index(drop=True)
    folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recall_check")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "recall_sheet.xlsx")
    if os.path.exists(path):
        sys.exit(f"{path} exists and may hold your reading; delete it on purpose to draw again")

    last = members.set_index("bioguide")["last"].map(lambda x: fold(x).title() if x.isupper() else fold(x))
    rx = re.compile(r"\b(" + "|".join(re.escape(s) for s in sorted(set(last), key=len, reverse=True)) + r")\b")
    own = last.to_dict()
    d["pool"] = [bool(set(rx.findall(fold(t))) - {own.get(b)}) for t, b in zip(d.text, d.bioguide)]
    s = pd.concat([d[d.pool].sample(N_POOL, random_state=SEED).assign(group="pool"),
                   d[~d.pool].sample(N_OUT, random_state=SEED).assign(group="outside")])
    s = s.sample(frac=1, random_state=SEED).reset_index(drop=True)
    s["sample_id"] = [f"recall_{i:02d}" for i in range(1, len(s) + 1)]
    s[["sample_id", "url", "group"]].to_csv(os.path.join(folder, "recall_draw.csv"), index=False)

    m = members.set_index("bioguide")
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = Workbook()
    ws = wb.active
    ws.title = "How to read"
    for i, line in enumerate(HOW_TO, 1):
        ws.cell(i, 1, line).font = Font(bold=(i == 1), size=13 if i == 1 else 11)
    ws.column_dimensions["A"].width = 115
    # one answer tab, then one tab per release with one paragraph per row (a whole release does not fit one cell)
    sh = wb.create_sheet("answers", 0)
    COLS = [("sample_id", 11), ("release_by", 26), ("date", 11), ("title", 45), ("named_members", 40),
            ("note", 35), ("words", 7), ("url", 18)]
    for j, (name, width) in enumerate(COLS, 1):
        c = sh.cell(1, j, name)
        c.font, c.fill = Font(bold=True), PatternFill("solid", fgColor="DDDDDD")
        sh.column_dimensions[c.column_letter].width = width
    sh.freeze_panes = "A2"
    wrap = Alignment(wrap_text=True, vertical="top")
    for i, r in enumerate(s.itertuples(), 2):
        who = f"{m.at[r.bioguide, 'name']} ({m.at[r.bioguide, 'party']}-{m.at[r.bioguide, 'state']})"
        vals = [r.sample_id, who, str(r.date)[:10], r.title, None, None, len(r.text.split()), r.url]
        for j, v in enumerate(vals, 1):
            sh.cell(i, j, v).alignment = wrap
        sh.cell(i, 1).hyperlink = f"#'{r.sample_id}'!A1"
        sh.cell(i, 1).font = Font(color="0563C1", underline="single")
        sh.cell(i, 8).hyperlink = r.url
        sh.cell(i, 8).font = Font(color="0563C1", underline="single")
        rt = wb.create_sheet(r.sample_id)
        rt.column_dimensions["A"].width = 120
        rt.cell(1, 1, f"{r.sample_id} · {who} · {str(r.date)[:10]}").font = Font(bold=True, size=12)
        rt.cell(2, 1, r.title).font = Font(bold=True)
        back = rt.cell(3, 1, "← back to answers")
        back.hyperlink, back.font = "#'answers'!A1", Font(color="0563C1", underline="single")
        paras = [p.strip() for p in r.text.split("\n") if p.strip()]
        for k, p in enumerate(paras, 5):
            c = rt.cell(k, 1, p)
            c.alignment = wrap
            rt.row_dimensions[k].height = min(409, 15 * (len(p) // 110 + 1) + 4)
    wb.move_sheet("How to read", offset=-wb.index(wb["How to read"]))
    wb.save(path)
    print(f"pool {int(d.pool.sum()):,}, outside {int((~d.pool).sum()):,}; drew {N_POOL} + {N_OUT}; "
          f"median {int(s.text.str.split().str.len().median())} words, longest {int(s.text.str.split().str.len().max())}")
    print("->", path)
