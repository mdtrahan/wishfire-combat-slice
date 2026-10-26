# Oasis Corridor provenance

**Date:** 2026-10-25 (date requested in the brief; generation session ran 2026-10-24, America/Los_Angeles)

## Generation

**Tool:** OpenAI built-in `image_gen` tool. The available interface does not expose a model identifier.

Three independently generated portrait environment sections were used. Style and palette were guided by the read-only Wishfire oasis court and puppet references. Composition followed the brief's high 3/4 top-down corridor reference.

1. **Boss court, top:** “Portrait 4:5 upper boss arena panel for a tall oasis corridor video game background, elevated 3/4 top-down painted console JRPG environment. Grand open sandstone court fills center with a broad circular paving inlay, a simple single subtly darker ring roughly 600 pixels across after final 960 pixel width. Circle centered in panel's upper-middle with enough full visible outline to read. Entire walkable floor remains empty, flat, mid-value sand and sandstone with low-contrast subdued paving, no obstacles. Non-walkable edges frame both long sides clearly as sandstone ledges and narrow turquoise water channels, a few palms, foliage and brass urns only at the far margins. The court narrows into a corridor at the bottom edge so it continues from the lower promenade. Warm muted oasis palette, soft top-left illumination, polished hand-painted 3/4 game art. No text, characters, signs, symbols, UI, strong tile patterns, or high contrast.”
2. **Promenade, middle:** “Portrait 4:5 painted game background section for a vertical 960x2200 oasis court. Create only the MIDDLE PROMENADE zone viewed from an elevated 3/4 top-down angle. Broad long vertical open warm sandstone walking lane in center, unbroken and calm; low-contrast mid-value sand and worn sandstone, faint diffuse texture only. Clearly raised boundary ledges follow both long sides, about 8-10 percent of panel width, with slender teal water channels outside the ledges and sparse palms, small shrubs, brass urns confined strictly to outer side margins. Central floor has no objects or obstacles. Consistent soft light from upper left, muted oasis palette, polished hand-painted console JRPG quality. The corridor continues out through top and bottom edges. No characters, text, signs, UI, high-contrast tiles, or patterns.”
3. **Starting plaza, bottom:** “Wide horizontal 16:9 game background panel, painted environment for lower starting plaza of a portrait oasis corridor. Overhead 3/4 top-down console JRPG scene. Keep broad central floor open and calm in mid-value pale sandstone and warm sand, almost no paving marks; peaceful rectangular plaza with no objects on floor. Strong narrow vertical left and right margins form raised sandstone boundary ledges with tiny teal water rills, a few palms and brass urns only at these outer edges. Edge structures extend continuously across top and bottom image edges for stitching to neighboring sections. Center floor extends to all panel edges. Soft top-left light. Muted warm stone, restrained gold, teal water accents. Low contrast for red white blue battle telegraphs and 30-60px characters. No high contrast, no busy patterns, no obstacles in center, no text, no characters, no UI.”

## Assembly and post-processing

- Cropped source images to retain the central walkable floor and narrow side boundaries, then resized sections to 960x800.
- Arranged sections boss court → promenade → plaza from top to bottom. Stitched at y=700 and y=1400 with 100-pixel row-wise crossfades to soften joins.
- Adjusted section brightness, reduced color saturation to 82% and contrast to 86%, then applied a 7% warm sandstone wash. Converted to opaque RGB PNG at exactly 960x2200.
- Built the preview at 360x825 (0.375 scale). Added Runa, Fara, Hondo and Kaja idle-right frames at 42x42 source-frame size; their visible bodies are approximately 36 pixels tall. Added a 65-pixel red translucent circle behind the heroes.

## Review notes

The central floor remains unobstructed and readable under the red circle and sprites. The boundary ledges, water and palms frame the path. The independently generated sections still show a faint softened change in wall and foliage placement at the two joins on close inspection; the crossfades reduce the hard cut but do not make those details continuous. The ring and arena read clearly, though its paving has more texture than the quietest parts of the corridor.

## Round 2: gameplay readability

**Date:** 2026-10-24

- Re-edited the assembled corridor with the built-in OpenAI image tool to remove the boss-court ring, clear the court-to-corridor ledge, and keep water, walls, and planting at the side margins. No exposed model identifier.
- Resized to 960×2200 RGB, reduced saturation and contrast, and added a low-strength warm tint. Added only a soft upper-court tint over y=40..660 to retain court identity without circular or concentric floor marks.
- Clipped side-wall spill at the walkable bounds with narrow feathered floor fills. Added 40 px masonry end thresholds from the previous top-edge architecture, rotated for the lower edge.
- Walkable bounds in `arena.json` use half-open pixels `[96,864) × [40,2160)`. Court center measured at `[480,320]` from the upper paving field.
- Rebuilt the 360×825 preview with a thin cyan walkable rectangle, Runa/Fara/Hondo/Kaja idle sprites, and one red circle as a telegraph readability check. Preview overlays are not in the shipped arena image.
- Preserved the prior 960×2200 image as `art/_work/arena/oasis-corridor-v1.png`.

**Review:** The circular telegraph confusion is removed and the route reads as one open floor. The side ledges remain close to the x bounds; narrow floor fills keep their foliage and masonry outside the rectangle, though the edge texture has slight softness on close inspection. Upper-court distinction is intentionally faint. The floor texture retains visible mottling that could compete with very small telegraphs at close zoom; verify in the target gameplay camera before further texture reduction.
