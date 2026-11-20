"""Shared helpers for the A3 scripts: where the inputs are, and the check that they are the frozen ones.

Every A3 script starts with `inputs = load_inputs(args)`. It refuses to run when an input file differs from what
`freeze.py` recorded in `out/inputs.json`, so a result can never silently mix two versions of the data or of
Martin's matcher. After a deliberate change (a new collection, a new matcher), rerun `freeze.py`, then the rest.
"""
import glob
import hashlib
import json
import os
import subprocess
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
# The two hit files (press_hits_shared/layer.parquet, 41 and 55 MB) are over GitHub's 25 MB upload limit and are
# rebuilt in about two minutes, so on Anas's machine they live next to the raw page cache (press_raw/, outside the
# folder that is uploaded). Anywhere else (a clone of the repo) they go to out/, which .gitignore leaves out.
_LOCAL = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "press_raw"))
HITS = os.path.join(_LOCAL, "a3_out") if os.path.isdir(_LOCAL) else OUT
os.makedirs(HITS, exist_ok=True)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def input_files(press, repo):
    """The files A3 depends on: the press-release parts, members.csv, Martin's matcher and context code."""
    parts = sorted(glob.glob(os.path.join(press, "press_releases_part*of*.parquet")))
    if not parts:
        sys.exit(f"no press_releases_part*of*.parquet in {press}")
    return {**{os.path.basename(p): p for p in parts},
            "members.csv": os.path.join(repo, "data", "processed", "members.csv"),
            "Martin/matcher.py": os.path.join(repo, "Martin", "matcher.py"),
            "Martin/build_mentions.py": os.path.join(repo, "Martin", "build_mentions.py")}


def git_commit(repo):
    try:
        return subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], capture_output=True, text=True,
                              check=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def load_inputs(press, repo):
    """Check the inputs against out/inputs.json; return (releases, members, Matcher class, context helpers)."""
    frozen_path = os.path.join(OUT, "inputs.json")
    if not os.path.exists(frozen_path):
        sys.exit("run freeze.py first")
    frozen = json.load(open(frozen_path))
    files = input_files(press, repo)
    changed = [k for k, p in files.items() if frozen["files"].get(k) != sha256(p)]
    missing = [k for k in frozen["files"] if k not in files]
    if changed or missing:
        sys.exit(f"inputs differ from out/inputs.json (changed: {changed}, missing: {missing}). "
                 "If the change is deliberate, rerun freeze.py and then every A3 step.")
    d = pd.concat([pd.read_parquet(files[k]) for k in sorted(files) if k.startswith("press_releases_part")],
                  ignore_index=True)
    assert len(d) == frozen["rows"], "row count differs from the frozen one"
    members = pd.read_csv(files["members.csv"])
    sys.path.insert(0, os.path.join(repo, "Martin"))
    import build_mentions                                     # Martin's context() and sentence splitter
    from matcher import Matcher, LEADER_TITLES
    return d, members, Matcher, LEADER_TITLES, build_mentions
