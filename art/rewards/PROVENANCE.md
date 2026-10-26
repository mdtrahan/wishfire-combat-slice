# Reward art provenance

Date: 2026-10-25

Tool: built-in `image_gen` in Codex. The tool response did not expose a model identifier, so the model is unreported.

Prompts used:

- Chest sheet: “Transparent PNG item sprite sheet, three columns by two rows, equal square cells with clear transparent space around sprites. Cohesive premium painted console JRPG inventory art. Top left ornate small closed desert treasure chest, three-quarter top-down angle, warm aged brass, gold sandstone wood and deep teal enamel bands, bold readable silhouette. Top center exact same chest open, lid hinged back, warm gold light from inside. Top right soft white radial burst fading to transparent. Bottom left ruby red heart and healing sparkle. Bottom center steel sword angled up-right with red-orange up-arrow. Bottom right cobalt shield with gold rim and up-arrow. No text, scene, visible grid, labels, or background. Objects centered within cells.”
- Range and speed sheet: “One 2 by 1 icon sheet, two large separate square game icons on a perfectly uniform chroma-key magenta background. Premium painted fantasy JRPG item icons. Left: golden recurved bow with teal grip and arrow pointed diagonally up-right, paired with a bright green upward-pointing arrow. Right: brown leather boot with turquoise feather wings, paired with a cyan upward-pointing arrow. Centered, bold silhouette, no text.”

Post-processing: cropped chest and first three reward icons from generated sheet. OpenCV GrabCut isolated those silhouettes from the generated dark backdrop; small detached flecks were removed and edges softened slightly. The bow and winged boot used a magenta color matte with edge unmixing. Chest sprites were fit to a 96×96 canvas with a shared baseline at y=88 and center x=48. Icons were fit to 64×64 canvases. The 128×128 white glow was drawn procedurally with a smooth radial alpha falloff and restrained soft rays. Pillow Lanczos resizing/compositing created the 360×200 arena-floor preview with the Fara idle frame at 32 px, both chests at 26 px, and icons at 20/40 px. The preview uses a small arena floor crop rather than the full portrait arena.

Source sheets and the build script remain in `art/_work/rewards/`; delivery files are in `art/rewards/`.

Round 2 corrections (2026-10-24): Re-keyed `buff-range.png` and `buff-speed.png` from the original magenta-backed sheet with a matte threshold and edge unmixing; pixels outside each cutout are transparent and edge pixels are despilled. Applied one shared 22×22 bright-green up arrow with dark outline at the lower-right of attack, defense, range, and speed icons. Heal remains arrow-free. Regenerated `preview.jpg` with the existing 360×200 layout and placements. Verified both keyed icons at 4× on pure black and white backgrounds; no rectangular matte or pink fringe was visible. All reward icons remain 64×64 RGBA. Chest files were left untouched.

Round 3 replacement (2026-10-25): Replaced the movement-coded winged boot with `buff-attack-speed.png`, a crossed-blade icon with motion arcs and the shared bright-green outlined up-arrow. Removed `buff-speed.png`, changed the catalog path and intended use to attack speed, and regenerated `preview.jpg` at the existing 360×200 layout with 20 px and 40 px icon placements. Verified the new 64×64 RGBA icon at 4× on black and white and compared it beside `buff-attack.png` at 20 px; crossed blades remain distinct from the single sword and no halo or fringe is visible.
