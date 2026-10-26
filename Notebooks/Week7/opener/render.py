"""Renders the opener inside Blender (run after scene.py; same OPENER and OUT variables passed in):
the two plates of the last frame (stickers on / stickers off), the stickers' projected corners for the page's peel,
and the intro camera move as MP4 + WebM. OUT is site/Figures/Week7/opener."""
import json
from pathlib import Path

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector

HERE, OUT = Path(OPENER), Path(OUT_DIR)  # noqa: F821
OUT.mkdir(parents=True, exist_ok=True)
L = json.loads((HERE / "layout.json").read_text())
sc = bpy.data.scenes["Opener"]
LAST = sc.frame_end
PW, PH = 3200, 1800
stickers = [sc.objects[f"Sticker{i + 1}"] for i in range(len(L["slots"]))]
done = {}

# ── plates of the last frame ──
sc.frame_set(LAST)
r = sc.render
r.resolution_x, r.resolution_y, r.resolution_percentage = PW, PH, 100
sc.eevee.taa_render_samples = 64
r.image_settings.file_format = "PNG"
for name, hide in (("plate-stickers", False), ("plate-liner", True)):
    for ob in stickers:
        ob.hide_render = hide
    r.filepath = str(OUT / f"{name}.png")
    bpy.ops.render.render(write_still=True, scene=sc.name)
    done[name] = r.filepath
for ob in stickers:
    ob.hide_render = False

# ── where each sticker's top face lands in plate pixels (tl, tr, br, bl) ──
deps = bpy.context.evaluated_depsgraph_get()
cam = sc.camera
geo = []
for ob, slot in zip(stickers, L["slots"]):
    w, h = L["sticker"][0] * 1.012, L["sticker"][1] * 1.012
    top = ob.modifiers["solid"].thickness
    px = []
    for lx, ly in ((-w / 2, h / 2), (w / 2, h / 2), (w / 2, -h / 2), (-w / 2, -h / 2)):
        co = world_to_camera_view(sc, cam, ob.matrix_world @ Vector((lx, ly, top)))
        px.append([round(co.x * PW, 2), round((1 - co.y) * PH, 2)])
    edge = ((px[1][0] - px[0][0]) ** 2 + (px[1][1] - px[0][1]) ** 2) ** 0.5
    geo.append(dict(i=slot["i"], c=px, r=round(L["radius"] * 1.012 * edge / w, 2)))
(OUT / "geometry.json").write_text(json.dumps(dict(plate=[PW, PH], stickers=geo), indent=1))

# ── the intro: 1600×900, H.264 MP4 and VP9 WebM ──
r.resolution_x, r.resolution_y = 1600, 900
sc.eevee.taa_render_samples = 32
for ext, container, codec in (("mp4", "MPEG4", "H264"), ("webm", "WEBM", "WEBM")):
    try:
        r.image_settings.media_type = "VIDEO"            # Blender 5.x
    except (AttributeError, TypeError):
        pass
    r.image_settings.file_format = "FFMPEG"
    f = r.ffmpeg
    f.format, f.codec = container, codec
    f.constant_rate_factor = "MEDIUM"
    f.ffmpeg_preset = "GOOD"
    f.gopsize = 15
    f.audio_codec = "NONE"
    r.filepath = str(OUT / f"intro.{ext}")
    r.use_file_extension = False
    bpy.ops.render.render(animation=True, scene=sc.name)
    done[ext] = r.filepath
r.use_file_extension = True
result = dict(done=done, stickers=len(geo))
