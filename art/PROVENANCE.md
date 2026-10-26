# Art provenance

Raw generated source sheets are retained in `art/_work/`. Projectiles were edited against the named permitted Wishfire Fara frame. Image generation used transparent backgrounds. Prompt text is a concise content description of each generated source when the exact original wording is unavailable. Pillow geometry and texture processing are distinguished per asset.

### `telegraph/rim.png`
- Prompt: Transparent 1024x1024 fantasy JRPG VFX atlas, 4 columns x 3 rows: ornate rim; arcane disc; ring wave; impact flash; 14-segment dashed rim; diagonal hatch; vertical beam; rounded cap; tracking chevrons; upward fan; safe donut; outward chevrons. White/gray painterly pearl energy.
- Source/reference: telegraph_atlas_v1.png.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Pillow radial alpha geometry sets the hit radius, crisp alpha-255 outer edge, 14 px band and 40 px inward glow; generated ring grain modulates the energy.
- Date: 2026-10-25.

### `telegraph/fill_disc.png`
- Prompt: Transparent 1024x1024 fantasy JRPG VFX atlas, 4 columns x 3 rows: ornate rim; arcane disc; ring wave; impact flash; 14-segment dashed rim; diagonal hatch; vertical beam; rounded cap; tracking chevrons; upward fan; safe donut; outward chevrons. White/gray painterly pearl energy.
- Source/reference: telegraph_atlas_v1.png.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Pillow radial alpha profile sets the disc and edge lift; generated source grain is median/gaussian softened and carried through the full radius; peak alpha 45/255.
- Date: 2026-10-25.

### `telegraph/wave_band.png`
- Prompt: Transparent 1024x1024 fantasy JRPG VFX atlas, 4 columns x 3 rows: ornate rim; arcane disc; ring wave; impact flash; 14-segment dashed rim; diagonal hatch; vertical beam; rounded cap; tracking chevrons; upward fan; safe donut; outward chevrons. White/gray painterly pearl energy.
- Source/reference: telegraph_atlas_v1.png.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Generated ring energy polar-mapped in Pillow to a 30 px annulus; antipodal texture average balances angular energy while retaining authored source grain.
- Date: 2026-10-25.

### `telegraph/flash.png`
- Prompt: Transparent 1024x1024 fantasy JRPG VFX atlas, 4 columns x 3 rows: ornate rim; arcane disc; ring wave; impact flash; 14-segment dashed rim; diagonal hatch; vertical beam; rounded cap; tracking chevrons; upward fan; safe donut; outward chevrons. White/gray painterly pearl energy.
- Source/reference: telegraph_atlas_v1.png.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Generated flash crop and 180-degree texture average centers the luminous mass while keeping the authored starburst.
- Date: 2026-10-25.

### `telegraph/dash_rim.png`
- Prompt: Transparent 1024x1024 fantasy JRPG VFX atlas, 4 columns x 3 rows: ornate rim; arcane disc; ring wave; impact flash; 14-segment dashed rim; diagonal hatch; vertical beam; rounded cap; tracking chevrons; upward fan; safe donut; outward chevrons. White/gray painterly pearl energy.
- Source/reference: telegraph_atlas_v1.png.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Generated 14-segment ring texture is circle-fit in Pillow, then polar-remapped to a centered 27 px annulus at the disc boundary; luminance remap preserves the authored dashed pattern with antialiased edges.
- Date: 2026-10-25.

### `telegraph/hatch_tile.png`
- Prompt: Transparent 1024x1024 fantasy JRPG VFX atlas, 4 columns x 3 rows: ornate rim; arcane disc; ring wave; impact flash; 14-segment dashed rim; diagonal hatch; vertical beam; rounded cap; tracking chevrons; upward fan; safe donut; outward chevrons. White/gray painterly pearl energy.
- Source/reference: telegraph_atlas_v1.png.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Generated diagonal swatch crop threshold-fitted to fill 128 square; opposing edges eased toward common samples in Pillow for two-axis seamless tiling.
- Date: 2026-10-25.

### `telegraph/beam_body.png`
- Prompt: Transparent 1024x1024 2x2 VFX atlas: continuous vertical beam body with uninterrupted bright core; rounded hemispherical cap with flat base; vertical tracking line with four chevrons; exact 90-degree up-facing fan with bottom apex and textured sides/arc.
- Source/reference: specialist beam/fan atlas.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Generated shaft crop/resize; 12-row wrap crossfade; bright core boosted with a soft cross-section ramp so edges taper into the source texture.
- Date: 2026-10-25.

### `telegraph/beam_cap.png`
- Prompt: Transparent 1024x1024 2x2 VFX atlas: continuous vertical beam body with uninterrupted bright core; rounded hemispherical cap with flat base; vertical tracking line with four chevrons; exact 90-degree up-facing fan with bottom apex and textured sides/arc.
- Source/reference: specialist beam/fan atlas.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Generated dome crop thresholded to remove stray lower plume, fitted to 36 px bright-core width, then contact row matched to beam_body seam profile.
- Date: 2026-10-25.

### `telegraph/aim_line.png`
- Prompt: Transparent 1024x1024 2x2 VFX atlas: continuous vertical beam body with uninterrupted bright core; rounded hemispherical cap with flat base; vertical tracking line with four chevrons; exact 90-degree up-facing fan with bottom apex and textured sides/arc.
- Source/reference: specialist beam/fan atlas.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Generated line-and-chevron crop/resize; centered on pivot, wrap crossfade, continuous bright core and authored pulses retained.
- Date: 2026-10-25.

### `telegraph/cone_fan.png`
- Prompt: Transparent 1024x1024 2x2 VFX atlas: continuous vertical beam body with uninterrupted bright core; rounded hemispherical cap with flat base; vertical tracking line with four chevrons; exact 90-degree up-facing fan with bottom apex and textured sides/arc.
- Source/reference: specialist beam/fan atlas.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Pillow maps generated fan grain into the exact 90-degree radius255 sector; Gaussian softening removes internal nested contours; textured 6 px boundary reinforced to alpha 210-245; interior capped below .22.
- Date: 2026-10-25.

### `telegraph/ring_safe.png`
- Prompt: Transparent 1024x1024 fantasy JRPG VFX atlas, 4 columns x 3 rows: ornate rim; arcane disc; ring wave; impact flash; 14-segment dashed rim; diagonal hatch; vertical beam; rounded cap; tracking chevrons; upward fan; safe donut; outward chevrons. White/gray painterly pearl energy.
- Source/reference: telegraph_atlas_v1.png.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Pillow radial geometry creates a centered 0.45-radius clear hole and fades a textured band evenly to radius1; generated ring grain quarter-turn averaged.
- Date: 2026-10-25.

### `telegraph/arrows_out.png`
- Prompt: Transparent 1024x1024 fantasy JRPG VFX atlas, 4 columns x 3 rows: ornate rim; arcane disc; ring wave; impact flash; 14-segment dashed rim; diagonal hatch; vertical beam; rounded cap; tracking chevrons; upward fan; safe donut; outward chevrons. White/gray painterly pearl energy.
- Source/reference: telegraph_atlas_v1.png.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Generated four-chevron direction cue crop; grayscale mask fitted to 256 square and center cleared in Pillow.
- Date: 2026-10-25.

### `icons/shield.png`
- Prompt: Transparent 1024x1024 combat status icon atlas, 4 columns x 2 rows: shield crest; heal plus with leaf; upward buff arrow; warning exclamation; lethal skull; downed crossed/fallen marker; revive spark with wings; bold chibi JRPG interface silhouettes, white and gray painterly energy, readable at 16 px.
- Source/reference: icons_atlas_v1.png.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Generated combat status glyph crop; grayscale RGB carries shading while a strengthened solid silhouette alpha preserves the shape at 16 px.
- Date: 2026-10-25.

### `icons/heal.png`
- Prompt: Transparent 1024x1024 combat status icon atlas, 4 columns x 2 rows: shield crest; heal plus with leaf; upward buff arrow; warning exclamation; lethal skull; downed crossed/fallen marker; revive spark with wings; bold chibi JRPG interface silhouettes, white and gray painterly energy, readable at 16 px.
- Source/reference: icons_atlas_v1.png.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Generated combat status glyph crop; grayscale RGB carries shading while a strengthened solid silhouette alpha preserves the shape at 16 px.
- Date: 2026-10-25.

### `icons/buff.png`
- Prompt: Transparent 1024x1024 combat status icon atlas, 4 columns x 2 rows: shield crest; heal plus with leaf; upward buff arrow; warning exclamation; lethal skull; downed crossed/fallen marker; revive spark with wings; bold chibi JRPG interface silhouettes, white and gray painterly energy, readable at 16 px.
- Source/reference: icons_atlas_v1.png.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Generated combat status glyph crop; grayscale RGB carries shading while a strengthened solid silhouette alpha preserves the shape at 16 px.
- Date: 2026-10-25.

### `icons/warn.png`
- Prompt: Transparent 1024x1024 combat status icon atlas, 4 columns x 2 rows: shield crest; heal plus with leaf; upward buff arrow; warning exclamation; lethal skull; downed crossed/fallen marker; revive spark with wings; bold chibi JRPG interface silhouettes, white and gray painterly energy, readable at 16 px.
- Source/reference: icons_atlas_v1.png.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Generated combat status glyph crop; grayscale RGB carries shading while a strengthened solid silhouette alpha preserves the shape at 16 px.
- Date: 2026-10-25.

### `icons/lethal.png`
- Prompt: Transparent 1024x1024 combat status icon atlas, 4 columns x 2 rows: shield crest; heal plus with leaf; upward buff arrow; warning exclamation; lethal skull; downed crossed/fallen marker; revive spark with wings; bold chibi JRPG interface silhouettes, white and gray painterly energy, readable at 16 px.
- Source/reference: icons_atlas_v1.png.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Generated combat status glyph crop; grayscale RGB carries shading while a strengthened solid silhouette alpha preserves the shape at 16 px.
- Date: 2026-10-25.

### `icons/downed.png`
- Prompt: Simplified solid downed marker: horizontal fallen chibi hero, one diagonal marker slash and short crossbar, bold high-contrast cel-shaded silhouette.
- Source/reference: isolated downed icon.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Generated downed marker crop; grayscale source shading retained in RGB; solid silhouette alpha; fitted to 64 square.
- Date: 2026-10-25.

### `icons/revive.png`
- Prompt: Transparent 1024x1024 combat status icon atlas, 4 columns x 2 rows: shield crest; heal plus with leaf; upward buff arrow; warning exclamation; lethal skull; downed crossed/fallen marker; revive spark with wings; bold chibi JRPG interface silhouettes, white and gray painterly energy, readable at 16 px.
- Source/reference: icons_atlas_v1.png.
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Generated combat status glyph crop; grayscale RGB carries shading while a strengthened solid silhouette alpha preserves the shape at 16 px.
- Date: 2026-10-25.

### `projectiles/bomb.png`
- Prompt: Edit projectile atlas using Fara attack-left-000.png as the named style reference. Redraw bolt as broad saturated azure/cyan right-facing bolt and orb as compact violet/cyan shell with white core; preserve bomb and shadow.
- Source/reference: projectiles_restyled_v2.png; reference web-runner/assets/puppets/fara/frames/attack-left-000.png.
- Tool/model: built-in OpenAI image_gen edit with Fara frame reference, model identifier not exposed.
- Post-process: Generated full-color bomb crop/refit; original cel-shaded RGB preserved and centered to 48 square.
- Date: 2026-10-25.

### `projectiles/bolt.png`
- Prompt: Edit projectile atlas using Fara attack-left-000.png as the named style reference. Redraw bolt as broad saturated azure/cyan right-facing bolt and orb as compact violet/cyan shell with white core; preserve bomb and shadow.
- Source/reference: projectiles_restyled_v2.png; reference web-runner/assets/puppets/fara/frames/attack-left-000.png.
- Tool/model: built-in OpenAI image_gen edit with Fara frame reference, model identifier not exposed.
- Post-process: Generated cel-shaded bolt crop/refit and scaled to 56x10 content in 64x16 canvas.
- Date: 2026-10-25.

### `projectiles/orb.png`
- Prompt: Edit projectile atlas using Fara attack-left-000.png as the named style reference. Redraw bolt as broad saturated azure/cyan right-facing bolt and orb as compact violet/cyan shell with white core; preserve bomb and shadow.
- Source/reference: projectiles_restyled_v2.png; reference web-runner/assets/puppets/fara/frames/attack-left-000.png.
- Tool/model: built-in OpenAI image_gen edit with Fara frame reference, model identifier not exposed.
- Post-process: Generated cel-shaded violet/cyan orb crop/refit; Pillow converts shading to grayscale while retaining bright core, so runtime tint multiplication can recolor it.
- Date: 2026-10-25.

### `projectiles/shadow.png`
- Prompt: Edit projectile atlas using Fara attack-left-000.png as the named style reference. Redraw bolt as broad saturated azure/cyan right-facing bolt and orb as compact violet/cyan shell with white core; preserve bomb and shadow.
- Source/reference: projectiles_restyled_v2.png; reference web-runner/assets/puppets/fara/frames/attack-left-000.png.
- Tool/model: built-in OpenAI image_gen edit with Fara frame reference, model identifier not exposed.
- Post-process: Generated shadow crop/refit; content scaled to 40x16, RGB set black, source luminance drives softly blurred alpha.
- Date: 2026-10-25.
