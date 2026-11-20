"""A3.0: record exactly which inputs A3 is built from.

Run from Anas/:  python a3/freeze.py --press press_releases --repo <path to project/ of the group repo>

Writes out/inputs.json: a SHA-256 of every press-release part, of members.csv and of Martin's matcher.py and
build_mentions.py, the repo commit, the row count and the date. Every later A3 step checks its inputs against this
file and stops if anything differs (common.py), so all A3 results come from one frozen set of inputs.
"""
import argparse
import datetime as dt
import json
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # run with python -I: add this folder only
from common import OUT, git_commit, input_files, sha256

ap = argparse.ArgumentParser()
ap.add_argument("--press", required=True)
ap.add_argument("--repo", required=True)
a = ap.parse_args()

files = input_files(a.press, a.repo)
rows = sum(len(pd.read_parquet(p, columns=["url"])) for k, p in files.items() if k.startswith("press_releases_part"))
rec = dict(frozen_at=dt.datetime.now().isoformat(timespec="seconds"), snapshot="press releases collected 20 Nov 2026",
           rows=rows, repo_commit=git_commit(a.repo), files={k: sha256(p) for k, p in files.items()})
os.makedirs(OUT, exist_ok=True)
json.dump(rec, open(os.path.join(OUT, "inputs.json"), "w"), indent=1)
print(json.dumps(rec, indent=1))
