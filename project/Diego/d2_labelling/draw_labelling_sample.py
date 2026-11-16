"""D2: draw the labelling sample from mentions.parquet and write one sheet per coder.

Run from project/ once Martin's file exists:
    python Diego/d2_labelling/draw_labelling_sample.py [path/to/mentions.parquet]

Design (see PROTOCOL.md): 150 cross-party and 50 same-party floor mentions, drawn at random with seed 2805
and shuffled together. Diego codes all 200. Martin and Anas each code 100, so every mention has two coders.
Party is left off the coder sheets. The key that links ids to parties and flags is written separately.
"""
import sys
from pathlib import Path
import pandas as pd

SEED, N_CROSS, N_SAME = 2805, 150, 50
HERE = Path(__file__).parent
src = sys.argv[1] if len(sys.argv) > 1 else "data/processed/mentions.parquet"

members = pd.read_csv("data/processed/members.csv").set_index("bioguide")
m = pd.read_parquet(src)
m = m[(m.source == "floor") & m.speaker.isin(members.index) & m.named.isin(members.index)].copy()
m["speaker_party"], m["named_party"] = members.party[m.speaker].values, members.party[m.named].values
m = m[m.speaker_party.isin(["R", "D"]) & m.named_party.isin(["R", "D"])]
m["cross"] = m.speaker_party != m.named_party

picked = pd.concat([m[m.cross].sample(N_CROSS, random_state=SEED), m[~m.cross].sample(N_SAME, random_state=SEED)])
picked = picked.sample(frac=1, random_state=SEED).reset_index(names="mention_row")
picked.insert(0, "id", [f"L{i:03d}" for i in range(1, len(picked) + 1)])
picked["speaker_name"], picked["named_name"] = members.name[picked.speaker].values, members.name[picked.named].values
picked["second_coder"] = ["martin" if i % 2 == 0 else "anas" for i in range(len(picked))]
picked.to_csv(HERE / "sample_key.csv", index=False)

sheet = picked[["id", "date", "doc_id", "speaker_name", "named_name", "context"]].assign(code="", unsure="", comment="")
for coder, rows in (("diego", sheet), ("martin", sheet[picked.second_coder == "martin"]), ("anas", sheet[picked.second_coder == "anas"])):
    out = HERE / f"sheet_{coder}.csv"
    if out.exists():
        sys.exit(f"{out} already exists. Coding may have started, so nothing was overwritten.")
    rows.to_csv(out, index=False)
print(f"{len(picked)} mentions: {int(picked.cross.sum())} cross-party, {int((~picked.cross).sum())} same-party; "
      f"flagged as yields: {int(picked.is_yield.sum())}")
