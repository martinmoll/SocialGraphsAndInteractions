"""Blender command-line entry for the opener: builds the scene, then renders it.
    blender -b -P run_render.py          (from this folder, after `python textures.py`)
Writes ../../../Figures/Week7/opener/{plate-stickers,plate-liner}.png, geometry.json, intro.mp4, intro.webm;
then run `python finish.py` to turn the plates into WebP."""
from pathlib import Path

OPENER = str(Path(__file__).resolve().parent)
OUT_DIR = str(Path(OPENER) / "../../../Figures/Week7/opener")
for script in ("scene.py", "render.py"):
    exec(open(Path(OPENER) / script).read(), {"OPENER": OPENER, "OUT_DIR": OUT_DIR, "__name__": "opener_" + script[:-3]})
