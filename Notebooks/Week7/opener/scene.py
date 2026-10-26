"""Builds the opener's sticker-sheet scene in Blender from layout.json and the textures in tex/.
Run inside Blender: exec(open(<this file>).read(), {"OPENER": "<folder of this file>"}).
The camera ends top-down; the page draws its peel on top of renders of that last frame."""
import json
import math
from pathlib import Path

import bmesh
import bpy
from mathutils import Vector

HERE = Path(OPENER)  # noqa: F821  (passed in by the caller)
L = json.loads((HERE / "layout.json").read_text())
SW, SH = L["sheet"]
FPS, FRAMES = 30, 132                     # 4.4 s camera move, last frames held
SHEET_ROT = math.radians(-2.0)
T_SHEET, T_STK = 0.0006, 0.0008

# ── a scene of its own, so the user's existing scene is left untouched; rebuilding replaces only this scene ──
if "Opener" in bpy.data.scenes:
    old = bpy.data.scenes["Opener"]
    for ob in list(old.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    bpy.data.scenes.remove(old)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras, bpy.data.images):
    for blk in list(coll):
        if blk.users == 0:
            coll.remove(blk)
scene = bpy.data.scenes.new("Opener")
if bpy.context.window:
    bpy.context.window.scene = scene
scene.unit_settings.system = "METRIC"
scene.render.fps = FPS
scene.frame_start, scene.frame_end = 1, FRAMES


def srgb(hexstr):
    h = hexstr.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return (*lin, 1.0)


def rounded_rect(name, w, h, r, seg=12):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    pts = []
    for cx, cy, a0 in [(w / 2 - r, h / 2 - r, 0), (-w / 2 + r, h / 2 - r, 90), (-w / 2 + r, -h / 2 + r, 180), (w / 2 - r, -h / 2 + r, 270)]:
        for k in range(seg + 1):
            a = math.radians(a0 + 90 * k / seg)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    verts = [bm.verts.new((x, y, 0)) for x, y in pts]
    face = bm.faces.new(verts)
    uv = bm.loops.layers.uv.new("UVMap")
    for loop in face.loops:
        x, y, _ = loop.vert.co
        loop[uv].uv = ((x + w / 2) / w, (y + h / 2) / h)
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    scene.collection.objects.link(ob)
    return ob


def principled(name, color=None, image=None, rough=0.5, spec=0.5, bump=None, alpha=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree; bsdf = nt.nodes["Principled BSDF"]
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Specular IOR Level"].default_value = spec
    if image:
        tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = bpy.data.images.load(str(image)); tex.interpolation = "Cubic"
        nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
        if alpha:
            nt.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
    elif color:
        bsdf.inputs["Base Color"].default_value = srgb(color)
    if bump:
        noise = nt.nodes.new("ShaderNodeTexNoise"); noise.inputs["Scale"].default_value = bump[0]; noise.inputs["Detail"].default_value = 8
        b = nt.nodes.new("ShaderNodeBump"); b.inputs["Strength"].default_value = bump[1]; b.inputs["Distance"].default_value = 0.0004
        nt.links.new(noise.outputs["Fac"], b.inputs["Height"]); nt.links.new(b.outputs["Normal"], bsdf.inputs["Normal"])
    return m


def solidify(ob, t, rim_material_offset=1, bevel=0.00012):
    s = ob.modifiers.new("solid", "SOLIDIFY"); s.thickness = t; s.offset = 1; s.material_offset_rim = rim_material_offset; s.use_rim = True
    b = ob.modifiers.new("bevel", "BEVEL"); b.width = bevel; b.segments = 3; b.limit_method = "ANGLE"


# ── desk ──
desk = rounded_rect("Desk", 3.0, 3.0, 0.01, seg=2)
desk.location.z = -0.0002
desk.data.materials.append(principled("desk", color="#EDE7DF", rough=0.85, spec=0.2, bump=(900, 0.08)))

# ── sheet (liner printed with the machine's labels) ──
sheet = rounded_rect("Sheet", SW, SH, 0.004)
sheet.rotation_euler.z = SHEET_ROT
sheet.data.materials.append(principled("liner", image=HERE / "tex/liner.png", rough=0.38, spec=0.45))
sheet.data.materials.append(principled("liner_edge", color="#EFEAE0", rough=0.6))
solidify(sheet, T_SHEET, bevel=0.0002)

# ── stickers, parented to the sheet ──
edge = principled("sticker_edge", color="#F4F0E6", rough=0.5)
stickers = []
for s in L["slots"]:
    w, h = L["sticker"][0] * 1.012, L["sticker"][1] * 1.012          # a hair larger than the slot, so no liner peeks out
    ob = rounded_rect(f"Sticker{s['i'] + 1}", w, h, L["radius"] * 1.012)
    ob.parent = sheet
    ob.location = (s["x"] + s["w"] / 2 - SW / 2, SH / 2 - (s["y"] + s["h"] / 2), T_SHEET)
    ob.data.materials.append(principled(f"face{s['i'] + 1}", image=HERE / f"tex/sticker{s['i'] + 1}.png", rough=0.48, spec=0.5))
    ob.data.materials.append(edge)
    solidify(ob, T_STK)
    stickers.append(ob)

# ── light: a soft warm key, a fill, and a cool flash for Storm ──
world = bpy.data.worlds.new("World"); scene.world = world; world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = srgb("#D9D4CB")
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.45


def area(name, loc, size, power, color, target=(0, 0, 0)):
    data = bpy.data.lights.new(name, "AREA"); data.size = size; data.energy = power; data.color = srgb(color)[:3]
    ob = bpy.data.objects.new(name, data); scene.collection.objects.link(ob); ob.location = loc
    direction = Vector(target) - Vector(loc); ob.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    return ob


key = area("Key", (-0.50, 0.42, 0.50), 0.35, 5.0, "#FFE9CC")
fill = area("Fill", (0.6, -0.35, 0.6), 0.9, 1.4, "#E8EEFF")
flash = area("Flash", (0.25, 0.35, 0.35), 0.25, 0, "#BFD3FF", target=(-0.1, 0.04, 0))
for f, p in [(1, 0), (13, 0), (15, 1.1), (17, 0.25), (19, 0), (23, 0), (24, 0.7), (27, 0)]:
    flash.data.energy = p; flash.data.keyframe_insert("energy", frame=f)

# ── camera: low close-up on the Storm sticker → top-down over the whole sheet ──
scene.frame_set(1)
scene.view_layers[0].update()
storm = stickers[0].matrix_world.translation.copy()
target = bpy.data.objects.new("CamTarget", None); scene.collection.objects.link(target)
cam_data = bpy.data.cameras.new("Cam"); cam = bpy.data.objects.new("Cam", cam_data); scene.collection.objects.link(cam)
scene.camera = cam
tt = cam.constraints.new("TRACK_TO"); tt.target = target; tt.track_axis = "TRACK_NEGATIVE_Z"; tt.up_axis = "UP_Y"
cam_data.sensor_width = 36
cam_data.dof.use_dof = True; cam_data.dof.focus_object = target
FINAL_H = 1.30
keys = [  # frame, camera location, target location, focal length, f-stop
    (1, (storm.x + 0.10, storm.y - 0.16, 0.05), (storm.x, storm.y, 0.0), 42, 5.6),
    (40, (storm.x + 0.03, storm.y - 0.12, 0.13), (storm.x + 0.02, storm.y - 0.01, 0.0), 50, 4.0),
    (112, (0.0, -0.0001, FINAL_H), (0.0, 0.0, 0.0), 100, 22),
    (FRAMES, (0.0, -0.0001, FINAL_H), (0.0, 0.0, 0.0), 100, 22),
]
for f, cl, tl, fl, fs in keys:
    cam.location = cl; cam.keyframe_insert("location", frame=f)
    target.location = tl; target.keyframe_insert("location", frame=f)
    cam_data.lens = fl; cam_data.keyframe_insert("lens", frame=f)
    cam_data.dof.aperture_fstop = fs; cam_data.dof.keyframe_insert("aperture_fstop", frame=f)
for ob in (cam, target, cam_data):
    ad = ob.animation_data
    if ad and ad.action:
        for fc in getattr(ad.action, "fcurves", []):
            for kp in fc.keyframe_points:
                kp.interpolation = "BEZIER"; kp.easing = "AUTO"

# ── render settings ──
r = scene.render
r.engine = "BLENDER_EEVEE"
scene.eevee.taa_render_samples = 64
scene.eevee.use_raytracing = True
scene.eevee.use_shadows = True
scene.view_settings.view_transform = "Standard"
scene.view_settings.look = "None"
scene.view_settings.exposure = 0.35
r.resolution_x, r.resolution_y, r.resolution_percentage = 2400, 1350, 100
r.film_transparent = False
result = dict(objects=len(scene.objects), stickers=[o.name for o in stickers], storm=list(storm))
