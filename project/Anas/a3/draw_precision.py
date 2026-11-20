"""A3.3 check: draw the precision samples for the press layer, one reading tab per rule (decision 3).

Run from Anas/ after press_layer.py:
    python a3/draw_precision.py --press press_releases --repo <project/ of the group repo>

For each rule, 30 hits drawn at random (seed 2805) from the hits it changed or added, with the status they count
under. Written to precision_check/precision_sheets.xlsx: a "How to read" tab, then one tab per rule, the text
with its own line breaks and the matched name in bold red, and a y / n / ? dropdown in `correct`. Anas reads each
one: y (the right House member, and a real naming), n (wrong person, not a House member, or not a naming), ?
(cannot tell). Claude does not fill these in. score_precision.py reads the workbook and gives precision with a
Wilson 95% interval per rule; a rule under 95% is narrowed or dropped (decision 3). The workbook is never
overwritten once it exists (the reading would be lost); delete it on purpose to draw again.

Rules sampled: untitled full name, list, alias first name, party-state tag (counted hits); own surname (hits
moved to "self"); state legislator (hits removed by the guard). The last two check that a rule removes the right
things.
"""
import argparse
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import OUT, load_inputs, HITS

SEED, N, WINDOW = 2805, 30, 300
HOW_TO = [
    "How to read these sheets (A3.3 precision check)",
    "",
    "Each tab is one rule of the press layer. Each row is one name the rule found, drawn at random (seed 2805).",
    "The name is in [[ bold red ]] in the text. 'release_by' is the member whose release it is; 'matched_to' is the",
    "House member the rule says was named.",
    "",
    "Fill 'correct' from the dropdown:",
    "  y  the name is that House member, and the release really names them",
    "  n  wrong member, not a House member (a senator, a state legislator, someone else), or not a naming",
    "  ?  cannot tell from the text (open the link)",
    "",
    "Tabs 'own surname' and 'state legislator' check rules that remove names: y means the rule was right",
    "('own surname': the name is the releasing member themselves; 'state legislator': not a House member).",
    "",
    "Each row is ONE name the rule found. A release often names many members (a list of co-sponsors); judge only",
    "the name in bold red. 'colleagues named in this release' shows how many it names in all (decision 8).",
    "Districts are the ones members served (district_lean/member_lean.csv), as releases write them: (TN-07).",
    "",
    "Do not read the matcher's other output first. Write anything worth keeping in 'note'.",
    "Then run:  python a3/score_precision.py",
]
SAMPLES = {"untitled full name": "counted", "list": "counted", "alias first name": "counted",
           "party-state tag": "counted", "own surname": "self", "state legislator": "state legislator"}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--press", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--folder", default=None, help="where to write the workbook (default: precision_check/)")
    a = ap.parse_args()
    d, members, *_ = load_inputs(a.press, a.repo)
    texts = dict(zip(d.url, d.text))
    m = members.set_index("bioguide")
    # the district the member SERVED (district_lean/member_lean.csv): what releases write, "(TN-07)"
    served = pd.read_csv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "district_lean",
                                      "member_lean.csv")).set_index("bioguide").district

    def who(b):
        if not isinstance(b, str):
            return ""
        dist = served.get(b)
        dist = "" if pd.isna(dist) else "-AL" if int(dist) == 0 else f"-{int(dist):02d}"
        return f"{m.at[b, 'name']} ({m.at[b, 'party']}-{m.at[b, 'state']}{dist})"
    from openpyxl import Workbook
    from openpyxl.cell.rich_text import CellRichText, TextBlock
    from openpyxl.cell.text import InlineFont
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation

    L = pd.read_parquet(os.path.join(HITS, "press_hits_layer.parquet"))
    folder = a.folder or os.path.join(os.path.dirname(OUT), "precision_check")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "precision_sheets.xlsx")
    if os.path.exists(path):
        sys.exit(f"{path} exists and may hold your reading; delete it on purpose to draw again")

    wb = Workbook()
    ws = wb.active
    ws.title = "How to read"
    for i, line in enumerate(HOW_TO, 1):
        ws.cell(i, 1, line).font = Font(bold=(i == 1), size=13 if i == 1 else 11)
    ws.column_dimensions["A"].width = 110
    COLS = [("sample_id", 22), ("release_by", 24), ("matched_to", 24), ("text", 95), ("correct", 9),
            ("note", 30), ("url", 18), ("rule", 14), ("status", 12), ("start", 8),
            ("colleagues named in this release", 14)]
    counted = L[L.status == "counted"].drop_duplicates(["doc_id", "named"]).groupby("doc_id").size()
    wrap = Alignment(wrap_text=True, vertical="top")
    red = InlineFont(b=True, color="C00000")
    for rule, status in SAMPLES.items():
        pool = L[(L.layer_rule == rule) & (L.status == status)]
        s = pool.sample(min(N, len(pool)), random_state=SEED)
        sh = wb.create_sheet(rule[:31])
        for j, (name, width) in enumerate(COLS, 1):
            c = sh.cell(1, j, name)
            c.font, c.fill = Font(bold=True), PatternFill("solid", fgColor="DDDDDD")
            sh.column_dimensions[c.column_letter].width = width
        sh.freeze_panes = "A2"
        dv = DataValidation(type="list", formula1='"y,n,?"', allow_blank=True)
        sh.add_data_validation(dv)
        for i, r in enumerate(s.itertuples(), 1):
            t = texts[r.doc_id]
            before, name, after = t[max(0, r.start - WINDOW):r.start], t[r.start:r.end], t[r.end:r.end + WINDOW]
            row = i + 1
            values = [f"{rule.replace(' ', '_')}_{i:02d}", who(r.speaker), who(r.named), None, None, None,
                      r.doc_id, rule, status, r.start, int(counted.get(r.doc_id, 0))]
            for j, v in enumerate(values, 1):
                if v is not None:
                    sh.cell(row, j, v).alignment = wrap
            tc = sh.cell(row, 4)
            tc.value = CellRichText(("… " if r.start > WINDOW else "") + before, TextBlock(red, "[[ " + name + " ]]"),
                                    after + (" …" if r.end + WINDOW < len(t) else ""))
            tc.alignment = wrap
            sh.cell(row, 7).hyperlink = r.doc_id
            sh.cell(row, 7).font = Font(color="0563C1", underline="single")
            for j in (5, 6):
                sh.cell(row, j).alignment = wrap
            dv.add(sh.cell(row, 5))
            lines = sum(max(1, len(p) // 90 + 1) for p in (before + name + after).split("\n"))
            sh.row_dimensions[row].height = min(409, 15 * lines + 6)
        print(f"{rule}: {len(s)} of {len(pool):,}")
    wb.save(path)
    print("->", path)
