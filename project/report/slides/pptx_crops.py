# Render the slide figures to PNG at 300 dpi and crop them exactly as slides.tex trims them (trim = left bottom right top, pt).
import subprocess, sys
from PIL import Image
FIG, OUT = sys.argv[1], sys.argv[2]
DPI = 300
crops = {  # name: (source pdf, trim l b r t) ; None = no trim
    "fig1_C": ("figure1.pdf", (2, 2, 252, 196)),
    "fig1_D": ("figure1.pdf", (258, 2, 2, 198)),
    "fig2": ("figure2.pdf", None),
    "lean": ("figure_lean.pdf", (0, 0, 0, 20)),
    "home": ("figure4.pdf", (0, 38.16, 220, 35.6)),   # map only, as slides.tex
}
for name, (src, trim) in crops.items():
    base = f"{OUT}/{name}_full"
    subprocess.run(["pdftoppm", "-png", "-r", str(DPI), "-singlefile", f"{FIG}/{src}", base], check=True)
    im = Image.open(base + ".png")
    if trim:
        s = DPI / 72; l, b, r, t = trim; W, H = im.size
        im = im.crop((round(l * s), round(t * s), W - round(r * s), H - round(b * s)))
    im.save(f"{OUT}/{name}.png"); print(name, im.size)
