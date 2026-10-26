# Week 7 opener: the sticker sheet

The post opens on a sheet of eight name stickers rendered in Blender (5.2, EEVEE). The page peels each sticker in real time
by folding its region of `plate-stickers.webp` back over `plate-liner.webp`, using the corner positions in `geometry.json`.

Rebuild, from this folder, after the notebook has written `../stats.json`:

1. `python textures.py`: draws the printed liner (the machine's labels, from `stats.json`) and the eight sticker faces into `tex/`,
   and writes `layout.json`. Fonts: Avenir Next and SF Mono (macOS system fonts).
2. `blender -b -P run_render.py`: builds the scene (`scene.py`) in a scene of its own and renders (`render.py`) the two plates of
   the last frame, the stickers' projected corners and the 4.4 s intro (MP4 and WebM) into `../../../Figures/Week7/opener/`.
3. `python finish.py`: converts the plates to WebP.

Then rebuild the post so it embeds the new `geometry.json`.
