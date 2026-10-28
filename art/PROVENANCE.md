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

### `elevate/sword.png`
- Prompt: Create a production painted bitmap VFX sprite: ONE single vertical spectral SWORD, blade pointing DOWN, hilt at TOP. Fully transparent background, no ground or shadow. Narrow portrait 1:3 composition, entire sword centered with generous clean transparent padding for its very tight glow. Sword silhouette: simple small pommel, short straight grip, unmistakable bold straight horizontal crossguard, broad double-edged straight blade tapering to a sharp downward point. Blade is 70 percent of total sword length, grip 15 percent. Guard width about 70 percent of canvas width, blade width about 36 percent. Entire solid sword made from luminous conjured energy, saturated Kaja violet #A11FFF body, magenta violet #CC61FF, #E08CFF and #F0ADFF highlights. White-hot sharp central ridge running down blade, saturated violet edges, tight bright rim glow just a few pixels at 128x384 final size. Keep violet opaque mass around the white core for contrast on pale sand. Crisp rich hand-painted fantasy mobile RPG summon-blade finish, dramatic luminous faceted brush shading, Final Fantasy / Kingdom Hearts quality. Instantly recognizable bold sword at 35 pixels tall. No pixel art, no vector or flat clip art; no ornamental crests, gems, wings, chains, ribbons, runes, letters, smoke, swirls, particles, broad haze or aura blob. Absolutely one sword and nothing else. Output transparent portrait canvas.
- Source/reference: Original built-in generation; retained at art/_work/elevate/generated-sword.png. Review uses arena/oasis-corridor.png and Hondo idle frame 0 from gen/assets.json (atlas-002.png).
- Tool/model: built-in OpenAI image_gen, model identifier not exposed.
- Post-process: Pillow crop of transparent margins, Lanczos resize without recoloring, centered in 128x384 RGBA with clear glow padding; zero RGB under zero alpha. Review composites use existing arena and packed actor art; mock sampled directly into a 720x480 backing buffer for a 240x160 logical view (3x device scale).
- Date: 2026-10-27.

### `fonts/Bungee-Regular.ttf`
- Source: byte-identical copy of Wishfire `web-runner/assets/fonts/Bungee-Regular.ttf` (damage-number face); Wishfire main left unchanged.
- License: Bungee by David Jonathan Ross, SIL Open Font License 1.1.
- Date: 2026-10-27.

### `puppets/mirewing/`
- Source: owner-approved `source/approved-source.png` and `source/approved-128.png`; built-in image_gen supplied separated paint with the approved source attached (model identifier unavailable).
- Process: Pillow extraction and fringe cleanup; parented Synfig 1.5.5 body/wings/glands/mouth rig with root-parented shadow. Native 1024px renders reduce with Lanczos to straight-alpha 128px, foot (64,125); right frames are semantic mirrors. Seven states at 12 fps. See `puppets/mirewing/README.md`.
- Date: 2026-10-27.

### `puppets/gloamink/`
- Source: owner-approved `art/_work/enemy-identities/new/gloamink-source.png` and `gloamink-128.png`; built-in image_gen supplied painted parts with the approved concept attached (model identifier unavailable).
- Process: Pillow isolates 17 parented parts with shin/paw joints (revision 2); Synfig 1.5.5 renders native 1024px, Lanczos reduces to straight-alpha 128px, foot (64,125). Seven states at 12 fps; opposite-facing frames are semantic mirrors. See `puppets/gloamink/README.md`.
- Date: 2026-10-27.

### `puppets/fizzmite/`
- Source: owner-approved `art/_work/enemy-identities/new/fizzmite-source.png` and `fizzmite-128.png`; built-in image_gen supplied isolated painted parts with the approved source attached (model identifier unavailable). Source face/sparks retain approved pixels; hashes in `puppets/fizzmite/source/provenance.json`.
- Process: Synfig 1.5.5 rigs 14 painted parts, six independent legs and parented fuse/flame/sparks. Native 1024px renders reduce through Lanczos to straight-alpha 128px, foot (64,125); alpha <=4 cleared. Seven states at 12 fps; right frames are semantic mirrors. See `puppets/fizzmite/README.md`.
- Date: 2026-10-27.
