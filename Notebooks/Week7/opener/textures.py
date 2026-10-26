"""Textures for the opener's sticker sheet, drawn from stats.json: the printed liner (title, die-cut slots, the machine's
labels) and one face per sticker. Also writes layout.json, which the Blender scene and the page both read."""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).parent
STATS = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "../stats.json"
OUT = HERE / "tex"; OUT.mkdir(exist_ok=True)
GAME = json.loads(STATS.read_text(encoding="utf-8"))["viz"]["game"]

AVENIR, SFMONO = "/System/Library/Fonts/Avenir Next.ttc", "/System/Library/Fonts/SFNSMono.ttf"
heavy = lambda px: ImageFont.truetype(AVENIR, px, index=8)
bold = lambda px: ImageFont.truetype(AVENIR, px, index=0)


def mono(px, weight="Medium"):
    f = ImageFont.truetype(SFMONO, px)
    f.set_variation_by_name(weight)
    return f


# the page's palette, as sRGB
INK, INK2, MUTED, RULE = (36, 33, 29), (78, 72, 66), (119, 113, 106), (201, 195, 186)
PAPER, CREAM, WHITE = (245, 241, 232), (251, 249, 244), (253, 252, 250)
MARIGOLD, AMBER = (236, 191, 76), (150, 98, 26)

# sheet: 0.40 m × 0.225 m, printed at 10,000 px per metre
PX = 10000
SHEET = (0.40, 0.225)
W, H = int(SHEET[0] * PX), int(SHEET[1] * PX)
STK = (0.080, 0.064)                      # sticker footprint
COLS, ROWS, PITCH = 4, 2, (0.092, 0.080)
X0, Y0 = (SHEET[0] - (COLS - 1) * PITCH[0] - STK[0]) / 2, 0.056   # top-left of the first slot, from the sheet's top-left
RADIUS = 0.0065


def fit(draw, text, font_fn, max_w, start, min_px=20):
    px = start
    while px > min_px:
        f = font_fn(px)
        if draw.textlength(text, font=f) <= max_w:
            return f
        px -= 2
    return font_fn(min_px)


def dashed_round_rect(draw, box, r, dash, gap, width, fill):
    """A rounded rectangle outline drawn as dashes, walking the perimeter."""
    import math
    x0, y0, x1, y1 = box
    pts = []
    def arc(cx, cy, a0, a1):
        for k in range(13):
            a = math.radians(a0 + (a1 - a0) * k / 12)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    arc(x1 - r, y0 + r, -90, 0); arc(x1 - r, y1 - r, 0, 90); arc(x0 + r, y1 - r, 90, 180); arc(x0 + r, y0 + r, 180, 270)
    pts.append(pts[0])
    seg, on, left = [], True, dash
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        d = math.hypot(bx - ax, by - ay); t = 0.0
        while t < d:
            step = min(left, d - t)
            sx, sy = ax + (bx - ax) * t / d, ay + (by - ay) * t / d
            ex, ey = ax + (bx - ax) * (t + step) / d, ay + (by - ay) * (t + step) / d
            if on:
                draw.line([(sx, sy), (ex, ey)], fill=fill, width=width)
            t += step; left -= step
            if left <= 1e-6:
                on = not on; left = dash if on else gap


slots = []
for i, g in enumerate(GAME):
    c, r = i % COLS, i // COLS
    x, y = X0 + c * PITCH[0], Y0 + r * PITCH[1]
    slots.append(dict(i=i, x=x, y=y, w=STK[0], h=STK[1]))

# ── liner ──
lin = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(lin)
d.text((int(0.016 * PX), int(0.014 * PX)), "WHO DOES THE MACHINE THINK IT IS?", font=heavy(int(0.0125 * PX)), fill=INK)
d.text((int(0.0165 * PX), int(0.032 * PX)), "8 names · 8 tools from week 7 · pick a sticker, guess what the machine wrote, then peel",
       font=mono(int(0.0042 * PX)), fill=MUTED)
right = "DTU 02805 · MARVEL SUPERSTARS · SHEET 7/8"
f = mono(int(0.0036 * PX), "Semibold")
d.text((W - int(0.016 * PX) - d.textlength(right, font=f), int(0.017 * PX)), right, font=f, fill=INK2)
for s, g in zip(slots, GAME):
    box = [int(s["x"] * PX), int(s["y"] * PX), int((s["x"] + s["w"]) * PX), int((s["y"] + s["h"]) * PX)]
    fillc = CREAM if g["state"] == "right" else MARIGOLD
    d.rounded_rectangle(box, radius=int(RADIUS * PX), fill=fillc, outline=RULE, width=6)
    cx, bw = (box[0] + box[2]) / 2, box[2] - box[0]
    tag = "the machine wrote"
    ft = mono(int(0.0030 * PX), "Semibold")
    d.text((cx - d.textlength(tag, font=ft) / 2, box[1] + int(0.0075 * PX)), tag, font=ft, fill=INK2)
    words = g["label"].split(" ")
    lines = [g["label"]] if len(g["label"]) <= 11 else [" ".join(words[:-1]), words[-1]]
    fl = fit(d, max(lines, key=len), heavy, bw * 0.84, int(0.0118 * PX))
    lh = fl.size * 1.02
    y_text = box[1] + (box[3] - box[1]) / 2 - lh * len(lines) / 2 - int(0.001 * PX)
    for k, line in enumerate(lines):
        d.text((cx - d.textlength(line, font=fl) / 2, y_text + k * lh), line, font=fl, fill=INK)
    fs = mono(int(0.0034 * PX))
    d.text((cx - d.textlength(g["sub"], font=fs) / 2, box[3] - int(0.0115 * PX)), g["sub"], font=fs, fill=INK2)
lin.save(OUT / "liner.png")

# ── sticker faces (each at 2× the liner's density for crisp zooms) ──
SW, SH = int(STK[0] * PX * 2), int(STK[1] * PX * 2)
for s, g in zip(slots, GAME):
    face = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    fd = ImageDraw.Draw(face)
    rad, inset, bw = int(RADIUS * PX * 2), 34, 22
    fd.rounded_rectangle([0, 0, SW - 1, SH - 1], radius=rad, fill=WHITE if g["ghost"] else CREAM)
    if g["ghost"]:
        dashed_round_rect(fd, [inset, inset, SW - inset, SH - inset], rad - inset, 70, 46, bw, INK)
    else:
        fd.rounded_rectangle([inset, inset, SW - inset, SH - inset], radius=rad - inset, outline=INK, width=bw)
    # number badge
    br = 74; bx, by = inset + 70 + br, inset + 64 + br
    fd.ellipse([bx - br, by - br, bx + br, by + br], fill=INK)
    fn = heavy(104); n = str(s["i"] + 1)
    fd.text((bx - fd.textlength(n, font=fn) / 2, by - 72), n, font=fn, fill=CREAM)
    # tool, top right
    ft = mono(54, "Semibold"); tool = g["tool"].split(" · ")[0]
    fd.text((SW - inset - 70 - fd.textlength(tool, font=ft), inset + 92), tool, font=ft, fill=INK2)
    # the name
    fname = fit(fd, g["name"], heavy, SW * 0.80, 236)
    fd.text(((SW - fd.textlength(g["name"], font=fname)) / 2, SH * 0.47 - fname.size * 0.62), g["name"], font=fname,
            fill=MUTED if g["ghost"] else INK)
    foot = "no page · answered anyway" if g["ghost"] else "peel me"
    ff = mono(52)
    fd.text(((SW - fd.textlength(foot, font=ff)) / 2, SH - inset - 150), foot, font=ff, fill=AMBER if g["ghost"] else MUTED)
    face.save(OUT / f"sticker{s['i'] + 1}.png")

layout = dict(sheet=SHEET, sticker=STK, radius=RADIUS, slots=slots, names=[g["name"] for g in GAME], ghost=[g["ghost"] for g in GAME])
(HERE / "layout.json").write_text(json.dumps(layout, indent=1), encoding="utf-8")
print("textures written:", sorted(p.name for p in OUT.iterdir()))
