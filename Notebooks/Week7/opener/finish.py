"""After Blender: the PNG plates become WebP (the page loads these), and the PNGs are removed from the site folder."""
from pathlib import Path

from PIL import Image

OUT = Path(__file__).parent / "../../../Figures/Week7/opener"
for name in ("plate-stickers", "plate-liner"):
    png = OUT / f"{name}.png"
    im = Image.open(png).convert("RGB")
    im.save(OUT / f"{name}.webp", "WEBP", quality=84, method=6)
    png.unlink()
for p in sorted(OUT.iterdir()):
    print(f"{p.name:22s} {p.stat().st_size / 1e3:8.0f} kB")
