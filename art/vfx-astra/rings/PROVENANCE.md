# Rings: art-director review handoff

ORKA-6jh1. Author: GPT Astra. Art director: Claude. Owner approved warcry-shockwave, warcry-roar, arcane-gather-ring and arcane-burst-ring. Client integration remains lead-owned. No runtime code or other artwork changed; no commits. Deliverable folder contains four approved PNG strips plus spec.json and this provenance file. Previews and comparison artifacts live only in art/_work/rings/.

## Final owner direction

Painted, translucent magic energy with layered internal colour and soft edges, using the owner-praised bubble-swell rim as finish reference. No solid ornamental props. Warcry remains an outward roar wave. Owner rejected the initial regeneration aura as generic green swirls; its PNG was moved to art/_work/rings/regen/rejected-regen-aura.png. Latest Arcane correction takes precedence: ONLY replace the generic wave_band base ring. Existing gathering glow, contraction, expansion, opacity curves and four-flare crackling sphere stay client-owned and unchanged. The intervening summon-sigil direction was withdrawn; its generated drafts are excluded from this package.

## Sources and method

Artwork generated with built-in image_gen using the owner-provided art direction and local bubble-swell reference. These are AI-generated painted-style raster assets, not a claim of human hand-painting. The supplied FFX/Valefor reference informed a discarded intermediate direction and is not incorporated into final texture content. No downloaded artwork or third-party game pixels were copied into deliverable textures.

Reference image: art/vfx-astra/bubble-pop/bubble-swell.png. Existing crimson-sweep, bubble-pop, ground-pound and charge-up PNGs/specs informed finish, packing and handoff conventions. Renderer usage read: crates/wf_client/src/render/vfx.rs (Taunt), render/arcane.rs and render/regen.rs. Camera ground squash verified0.75; current Taunt radius440u, lifetime0.45s; Arcane radius95u, countdown0.45s, burst package0.55s with ring lasting0.385s. Chimerilass reference uses current2.2 scale, zoom0.5 and idle foot/body metrics.

Pillow/NumPy performed technical extraction, alpha cleanup, centring, sizing and horizontal packing. Every frame uses independent generated paint. Alpha floors16/24/32 remove low-alpha source residue; ceiling253 maps to255. Exact crop rectangles, thresholds, opacity envelopes, source hashes and painted widths are in art/_work/rings/packing.json. Lanczos resampling preserves straight alpha. RGB under zero alpha is explicitly zero. No procedural strokes, circles, noise textures or generated geometry were drawn into the four approved textures. Three clear texels are reserved inside every cell edge. PNG RGBA8, lossless, no palette reduction.

Fara shockwave has expansion/fade baked into its eight frames. Roar has a brief authored dissolve. Taunt mark was dropped; the existing eye icon stays. Rejected regen aura is retained only in scratch. Three new regeneration concepts await review. Arcane frames all have the same176x132px painted envelope within192x144px cells; only internal painted light shimmers. Client retains its current scale/opacity curves. Gutter compensation192/176 preserves intended95px screen footprint at full scale. Ground0.75 ratio is already baked; do not squash it again. Alpha blending with white tint is the review baseline, retaining internal colour on sand. Existing additive glow/flare layers stay unchanged; the lead must approve ring blend choice before integration.

## Files and timing

- warcry-shockwave.png: 3072x288px strip; 8 cels of 384x288px; 17.7778fps; 0.45s once; centred pivot [192.0, 144.0]; alpha; quad [480, 360]px at zoom0.5; 257,993bytes.
- warcry-roar.png: 768x128px strip; 6 cels of 128x128px; 20fps; 0.3s once; centred pivot [64.0, 64.0]; alpha; quad [54, 54]px at zoom0.5; 68,318bytes.
- arcane-gather-ring.png: 1536x144px strip; 8 cels of 192x144px; 17.7778fps; 0.45s once; centred pivot [96.0, 72.0]; alpha; quad [103.636, 77.727]px at zoom0.5; 232,224bytes.
- arcane-burst-ring.png: 1152x144px strip; 6 cels of 192x144px; 15.5844fps; 0.385s once; centred pivot [96.0, 72.0]; alpha; quad [103.636, 77.727]px at zoom0.5; 142,583bytes.

spec.json is the integration contract and contains exact motion/placement instructions, hashes, sampling, blend and padding. Timings are presentation metadata; authoritative simulation events own effect start, resolution and expiry.

## Comparison and limits

art/_work/rings/compare.jpg: native logical pixel composites on sand RGB(163,146,120) and spotlight RGB(33,29,24), the sand under current80% black scrim. Existing actor atlas art supplies scale/context; the bubble-swell rim laid flat supplies the finish reference. Four columns show old/new on both backgrounds. Old ring/glow samples use the actual wave_band.png/flash.png and current tint/additive algebra. New samples use exact delivered cels and recommended alpha blend. Arcane new panels retain current glow layers and change only the base ring. The existing four-flare sphere is omitted from both columns to expose the ground layer. Regen isolates the old body glow; separate tick glints/motes are omitted from both columns. These are staged art comparisons, not screenshots from a running client.

The full440px Taunt diameter exceeds the360px portrait viewport; the comparison includes an unclipped native-size final frame. Arcane source cels remain equal size; the review player applies current client curves to them. Eight and six discrete cels imply visible stepped shimmer; runtime interpolation, layering and playback have not been tested. Taunt chest light is intentionally small beside the retained head icon. Regen has slight perimeter movement across its loop, which the lead should assess in playback.

Asset validation: every strip has expected dimensions/count, unique cels, zero-alpha three-texel gutters, transparent background, zero RGB under zero alpha, and matching SHA-256. All-frame contact sheet inspected. Scratch review player checked through T3 html_preview (12 images loaded, no console errors) and native preview automation (selection, scrub, play/pause,360x380px canvas display). Native preview remained reported hidden even after explicit show; inline HTML review is the presentation surface. Owner approval covers only the four retained textures. Runtime integration and client screenshots remain pending. The original comparison is historical review evidence; taunt-mark and regeneration shown there are excluded from the approved package.

## Exact final generation prompts and source provenance

### warcry-shockwave

Source: /Users/Mace/.codex/generated_images/01a174db-88b7-75d0-ba06-786b9a4fac7b/exec-2b852300-dc9b-41e0-b798-feb1fe7675a8.png

Source SHA-256: `a9fcbac15a4499eb468d836f2a79985965e3b20717d77c637d5051f4e28a7015`

```text
New production game VFX animation using reference ONLY for painted luminous bubble-rim finish. Gold-amber MAGIC ENERGY shockwave. One simple translucent flowing body of light + a soft short falloff + at most 2 sparks. Quiet layered honey/peach/cream internal colour flow, soft edge and uneven painted thickness. Absolutely no fire, teeth, crowns, spikes, objects, glyphs, ornaments, metal, smoke, texture noise or hard outlines. Empty centre, no filled disc. Lies FLAT ON GROUND as an ellipse height 0.75 width. Exactly EIGHT chronological cels arranged TWO columns FOUR rows. Each effect SMALL with at least 20% cell margins, NO cropping or touching other cells. Transparent canvas everywhere except painted light. All cel centres fixed. 1 small tight ring,2 small expanding ring,3 medium ring,4 larger luminous ring,5 broad thin ring,6 maximum wide ring starting to dissolve,7 maximum radius soft broken arcs,8 faint few outer wisps. Expanding ring from 10% to 60% cell width, no standing flames. Hand-painted sophisticated JRPG spell light, subtle and luminous like the iridescent soap-film reference, in warm gold colour family. NO scene, text, grid, people, ground painting or black opaque background. Tall source sheet.
```

### warcry-roar

Source: /Users/Mace/.codex/generated_images/01a174db-88b7-75d0-ba06-786b9a4fac7b/exec-141169f2-5e02-4f7c-8c31-d01d59a84c36.png

Source SHA-256: `42837c2c5ee2ab98f3b409122255b0b8f5f3bab99485dfad48349e12d9e3124f`

```text
Production transparent sprite atlas, SIX chronological frames, THREE columns TWO rows. New GOLD ROAR ENERGY pulse around an invisible warrior body. Reference is finish only: luminous hand-painted bubble rim with layered translucent internal colour and soft unstroked edge. Replace hard radial shards with ONE soft short radiating body of golden light, flowing airy brush-painted streaks blended together, hollow centre allowing body visibility. Warm amber/pale peach/ivory light, restrained pearlescent highlights. Six stages: compressed tiny energy knot; opens into compact soft radial bloom; full gentle roar pulse with short outward flowing light; dispersing soft rays; two faint wisps; tiny fading light. Simple restrained magical energy, no ornaments, no physical objects, no hard spikes, no glyphs, no leaves, no fire, no cartoon outlines, no people. Native 48px display. Each sprite central HALF of its square cell, broad 25% clear margins on every side. TRANSPARENT exterior and centre; only a short soft edge attached to body of light, NO large fog halo across background. Each cel fully isolated, no text or grid. Craftsmanship of hand-painted JRPG spell animation.
```

### arcane-gather-ring

Source: /Users/Mace/.codex/generated_images/01a174db-88b7-75d0-ba06-786b9a4fac7b/exec-a26081de-c5cd-4870-85df-c9e1cf5d15a3.png

Source SHA-256: `be15f38296c56eb853d399671139ad3481428d6ad2dcb8002535461ff900db7f`

```text
Production game sprite sheet ONLY. Eight SAME-SIZED violet light rings, animation frames in FOUR columns TWO rows, evenly separated with wide transparent gutters. Use reference bubble rim for FINISH ONLY: rich painted pearlescent internal flowing colour and SOFT luminous edge, like soap-film light. Each frame depicts ONE simple smooth circular violet ring with EMPTY TRANSPARENT CENTRE. No concentric rings, no spiral, no sigil, no stars, no glyphs, no ornaments, no tendrils, no rays, no extra effects. Camera near top-down: every ring is same ellipse height0.75width. Subtle violet/periwinkle/lavender/light pink variation flows around the painted band in eight different shimmer poses, but outer diameter and centred pivot stay IDENTICAL in EVERY frame. All eight rings 55%cellwidth, equal thickness, same perspective. Client will contract this ring, so DO NOT draw a growing or shrinking sequence. Each ring is soft light with gently varying painted thickness and translucent falloff, not a physical torus, not a metallic band or generic tinted outline. Surface finish matches owner-praised luminous painted bubble rim. Gentle modest light, no full-cell background fog/glow and no filled centre. All eight completely contained and separated. True transparent RGBA background. No text/labels/scenery/person/checkerboard.
```

### arcane-burst-ring

Source: /Users/Mace/.codex/generated_images/01a174db-88b7-75d0-ba06-786b9a4fac7b/exec-4808813b-5371-4ef1-99ce-a21dd47e3240.png

Source SHA-256: `b3b43df988535482c2c88c8a5595556ba58a2c12678608e616d56943ee6924bb`

```text
Production transparent 2D game VFX source sheet. SIX SAME-SIZED painted violet energy rings in THREE columns TWO rows, fixed centred pivot and identical diameter all six. Reference only for luminous hand-painted bubble-rim finish: soft alpha edge, layered violet/periwinkle/pink/ivory internal flowing light. ONE simple thin ring per cel, EMPTY transparent centre. This is only a bitmap replacement for a generic base ring under an existing Arcane Pulse burst; do not design any other burst. Client already handles all expansion and fading, so keep same full diameter and similar opacity in every cel while a gentle highlight flows around perimeter. Subtle painted variations of thickness, airy translucent light, not physical metal/glass, not a hard stroked circle. Near top-down ground ellipse 0.75 high relative to wide. NO spirals, no concentric layers, no sigil or glyphs, no stars, no sparks, no flames, no pillar, no explosion, no character, no ornaments. No diffuse glow across centre or background. All effects inside central65% of cell with generous transparent gutters. No text/scenery/grid/checkerboard. Six clean simple hand-painted ring light cels with restrained shimmering colour.
```

