# Charge-up supporting VFX provenance

Date: 2026-10-25. Artist: GPT Astra. Art director: Claude. Bead: ORKA-6jh1.

## Direction and scope

The art-director update makes the hero's own frozen sprite echo the primary charge effect. This set supplies converging light needles, ground light and a non-figurative radial release glint. No body silhouette, character aura, wing, hair, feather, text or hero sprite is baked into the strips. Deliverables occupy only art/vfx-astra/charge-up/. Source masters, packing/validation scripts and interactive review occupy art/_work/charge-up/. No runtime code, other artwork, tracker state or commits were changed by this art task.

## References

Studied art/vfx-astra/split-faze/spec.json for schema, and crimson-sweep/spec.json, PROVENANCE.md and preview.jpg plus bubble-pop/spec.json, PROVENANCE.md and preview.jpg for production conventions. Owner-provided art/_work/xeno/sheet.jpg and burst.jpg supplied the inward-speed-line and sprite-echo timing reference. No pixels from the Xenogears clip occur in the deliverables.

Preview heroes are read-only crops from web/gen/assets.json and its referenced atlas-001.png. The four idle crops are scaled to 32px visible height. The scratch review's optional arena comes from web/gen/arena.png. Existing client render/charge.rs supplied Fara, Hondo, Runa and Kaja primary tint RGB values. Runa's softer pink secondary tint is an art recommendation for the owner's aqua-pink treatment. Source sprites, arena and client files remain unchanged.

## Generation and packing

Four source masters were generated through the built-in image_gen.imagegen tool with transparent_background=true. The tool exposes no backend model/version identifier. References were inspected visually; prompts used text without reference-image inputs. No third-party art was downloaded. The first gather master was rejected because its thick teardrops suggested the forbidden organic forms. Only the replacement needle master contributes to charge-gather.png.

The scratch package.py cuts the generated grids, removes alpha <=6 and maps remaining alpha to 0..255, crops transparent margins where needed, resizes through premultiplied-alpha Lanczos and writes straight/unassociated RGBA8. All fully transparent RGB is zero. Every cel has at least three clear texels inside each edge; adjacent frames therefore have six clear texels in total, without changing frame stride. No palette quantization. No drawn vector line, curve, circle, star or particle primitive supplies any VFX pixels.

Gather animation places and rotates seven differently painted raster needles on fixed staggered inward paths. Two smaller motes reuse cropped painted tips. Each track repeats every 600ms; each of the eight cels holds 75ms. Needle heads move inward with dim endpoints for wrap. The first source master is retained only in ignored scratch as rejected evidence.

Ground cells use painted source light cropped to its envelope and scaled to authored 2:1 sizes: 48x24, 62x31, 78x39, 94x47, 106x53, 116x58 inside 128x64 frames. This encodes the requested 0.5 squash. Some upper diffuse light gives the ring texture; its brightest lower rim sits a few source texels below its geometric centre. Six cels hold 100ms each.

Flare cells share one source transform: a 512x512 cel becomes 144x144 at (8,44) inside 160x192. Painted centre is nominally (80,116). The feet pivot is (80,192), placing the burst 19 screen pixels above feet in a 40x48 screen quad. Six cels hold 33.333333ms; tail opacity multipliers are 1,1,1,0.8,0.45,0.12. Individual generated cels vary slightly in ray geometry.

## Integration contract

Charge anticipation lasts 600ms. The radial glint starts at the handoff into the special and runs for 200ms, without extending the pause. Ground fades over those 200ms; gather may retain a 75ms fading last-cel tail. spec.json owns exact values. Simulation timing remains client/lead-owned.

Recommended blending is SrcAlpha/One additive with straight-alpha textures. Suggested opacity: gather 1, ground 0.5, flare 0.9. Alpha blending is a softer alternative. Tint uses source luminance and a smooth white-core gate, documented exactly in spec.json and implemented in both previews. Simple RGB multiplication cannot keep white cores white. No shader or game implementation is included.

Gather centre anchors at the chest. Flare bottom-centre anchors at feet and must retain its 160:192 aspect ratio. Ground bottom-centre pivot requires a downward offset of half the displayed quad height, 16px at the recommended 64x32 screen size, so the ring's geometric centre falls beneath the feet. Apply no extra ground squash. These placements must be reconciled with the consuming renderer; existing caller behavior was not changed.

## Review and validation

preview.jpg uses #1c1822 and shows the three supporting layers composited with actual hero crops in neutral, crimson, red-violet, aqua-pink and violet. Upper rows use game scale; the labelled lower comparison is 2x. At 633.34ms all three layers overlap, with gather in its release tail. Final packed artwork was visually inspected, including alpha edges and frame contacts. The preview deliberately omits the client-generated sprite echoes so the supporting art is assessable by itself.

The self-contained scratch review.html provides animation, pause/play, restart, timeline scrub, additive/alpha selection, gather-loop mode and a frozen arena under an 80% black scrim. T3 html_preview rendered the load state and the 666.67ms release against the scrim without console errors. Native preview evaluation confirmed eight loaded images, animation progression, pause stability and scrubbing. The native tab remained visible=false despite open/show; snapshot returned `Preview automation snapshot timed out after 15000ms`. The T3 inline HTML review is the user-visible surface. No external browser was opened.

validate.py verifies exact RGBA dimensions/counts, three-texel transparent borders on every frame, transparent RGB zeros, nonempty soft-alpha cels, asset hashes, inward track direction and the under-1MB budget. The gather last-to-first alpha-difference ratio is 1.046 relative to the other transitions, so the wrap is within ordinary cel change. Evidence: art/_work/charge-up/validation.json and gather-tracks.json. This is asset and staged-preview verification. Combat playback, renderer sizing/sorting, tint implementation and art-director acceptance remain pending.

## Exact generation prompts and sources

### gather (rejected)

Source: `/Users/Mace/.codex/generated_images/01a17425-854b-7821-9c8d-105842393aee/exec-cb7c837d-31e2-48f0-9740-aed9e8de301f.png`

SHA-256: `f9f52e653797b904fd568e2f848b22aa572d28089f02d629bc052bde12022f56`

Use case: stylized-concept. Production raster sprite animation master: charge-gather for a hand-crafted 2D JRPG, refined Xenogears/Capcom/Final Fantasy energy anticipation. True transparent RGBA background. EIGHT painted animation cels arranged in strict 4 column by 2 row uniform grid, canvas 2048x1024, each cell 512x512. NO text, panel, border, checkerboard, hero, body shape, aura silhouette, flame, wing, feather, hair, ring, rune, line-art symbols. Sparse thin WHITE LIGHT SPEED STREAKS and little pearly motes moving INWARD toward the EXACT cell centre (256,256). Neutral ivory-white and faint pale gold softer light, luminous white-hot pointed leading tips. Long delicate tapering tails extend AWAY from centre. Painterly raster edges, subtle hand-shaped irregularities, crisp glancing tips, soft luminous falloff narrowly around each streak. Mostly clear transparent space, centre remains clear to show an existing hero, no central flash. Only 5-7 unevenly spaced narrow streaks per cel, varied lengths, distinctly unequal angles, avoiding mechanical radial symmetry. Animation: frame1 streaks far out; frame2 slightly closer; frame3 closer still; frame4 leading tips reach near centre and dim; frame5 old tips vanish while a fresh staggered set begins at perimeter; frame6 fresh tips approach; frame7 closer; frame8 centre-near streaks dissolve and peripheral motes anticipate frame1. Continuous flowing inward loop, no outward explosion. ALL cels pivot exactly 256,256, maintain identical camera and scale, each drawing bounded within x=38..474,y=38..474. No cut-off pixels or overlap between cells. This is a subtle supporting layer around a tiny 32px hero while a client-generated sprite echo supplies the main body aura. Bold enough white tips to survive reduction to 128x128 texel frames and 64px screen width.

### ground

Source: `/Users/Mace/.codex/generated_images/01a17425-854b-7821-9c8d-105842393aee/exec-84a3de51-2f0b-4ca9-a619-100caa804dc9.png`

SHA-256: `b3220c18e38aa6f152437b54c532d0bac96a4e8eb9bcea06b772a960796bc390`

Use case: stylized-concept. Paint a production 2D JRPG charge-ground sprite animation. SIX distinct animation cels in a strict three-column by two-row grid of equal cells on a 1536x1024 transparent canvas. Each cell 512x512, no labels or visible grid. A delicately hand-painted SOFT IVORY WHITE and PALE CHAMPAGNE GOLD pool of light on the ground, an irregular finely feathered luminous elliptical rim with translucent inner glow. Already squashed exactly half height: final largest ellipse spans about 420x210 texels, floating centred at x256,y320 of its cell. Gentle uneven brush textures and wispy soft scalloped light, a brighter thin wet-looking glancing front edge, quietly broken rear edge. NO procedural vector outline, no solid disk, no magic sigil, no perspective cylinder. The ground light swells through six cels: 40%,55%,70%,84%,95%,100% of final size with increasing luminosity. Centre fixed x256,y320 in all cells. Neutral near-white, only subtle pale warm gold in low lights; white-hot highlight filaments within soft luminance. Background and margins TRUE RGBA TRANSPARENT, plenty of clear space, no black fill, checkerboard, characters, upright aura, body silhouette, flames, feathers, wings, hair, text, runes, symbols. Polished Xenogears/Final Fantasy/Capcom painterly sprite craft, soft light support for a separate hero sprite echo. Keep all strokes and glow within cell x38..474 and y190..450. This will be reduced to 128x64 strips, keep shapes luminous and readable.

### flare

Source: `/Users/Mace/.codex/generated_images/01a17425-854b-7821-9c8d-105842393aee/exec-38fa662f-9bdf-41b5-b141-86abd949de4b.png`

SHA-256: `1d75eeeed7116e6ba1eb8697e230cc88c67ca93f5011f26fbf23fe1ace0c4c5e`

Use case: stylized-concept. Paint a production JRPG 2D release-glint animation master, hand-crafted Xenogears/Final Fantasy/Capcom luminous raster sprite art. SIX animation cels in strict three-column two-row uniform grid, canvas1536x1024, cells512x512. True transparent RGBA background and clear gutters. Every cel is a NON-FIGURATIVE RADIAL WHITE LIGHT BURST centered at (256,256), roughly ROUND footprint with unequal rays. It must never suggest any body, person, upright aura, body outline, fire wing, hair or feather. A small white-hot central bead with sharp slender ivory-white rays expanding radially, soft pale-champagne light narrowly wrapped around them. Beautiful irregular hand-painted glancing edges, fine taper, some tiny pearl glints, restrained softness; no perfect geometric star primitive, no thick petals or brushy flame. Leave most of each cel transparent. SIX PHASES: 1 compact pinched bright glint diameter100px; 2 snappy bright irregular radial flash diameter280px; 3 largest expanded radiating flash diameter400px, its small opaque centre only35px; 4 thinning broken rays diameter360px with centre fading; 5 two faint slivers and three small residual motes; 6 barely-visible small trailing glints, almost gone. Keep all light within x40..472,y40..472, no overlap or cropped rays. Neutral white with faint warm pale gold in middle values, white-hot cores. No saturated colour. No ring, sigil, circle outline, icons, lightning bolt, weapon, background, ground, smoke, characters, silhouette, text, frame labels, borders or checkerboard. This is a supporting brief star-glint at the chest of a 32px-tall hero whose expanding body echo is rendered separately by the game; keep the burst refined and see-through.

### gather-streak

Source: `/Users/Mace/.codex/generated_images/01a17425-854b-7821-9c8d-105842393aee/exec-41e5ef19-76eb-40f3-acb9-88d0ae2cc784.png`

SHA-256: `499e5dd365bc3b11c4195d38d3bf0bfcc497a5d342dd995dc51541fc6bc01c5e`

Use case: stylized-concept. Paint a transparent game VFX SOURCE MASTER with EIGHT tiny THIN WHITE SPEED STREAKS, each individually isolated in its own cell, strict 4 columns x 2 rows on a 2048x1024 canvas. ONE streak per 512x512 cell, horizontal from LEFT to RIGHT, white-hot head on the RIGHT, softly fading thin tail on the LEFT. Each streak is extremely narrow, like a white needle of light or white sword glint, length 340 pixels, painted core only 3 to 7 pixels thick, narrow soft halo only 10-16 pixels thick. KEEP AN ASPECT RATIO of at least 20:1 for each streak. Flat pointed thread of light. No chunky round head, no teardrop, no flame, no feathers, no wings, no hair, no thick brushstroke. Asymmetric minute hand-painted breaks and subtle differences in taper, very fine ivory-white sheen, near-white pale gold halo. All streaks share centre (256,256); tail starts x80, tip ends x430. Eight variants of this ONE simple slender luminous needle, tiny variations in length and texture, no arc or curve. Most of each cell COMPLETELY EMPTY AND TRANSPARENT. No radial explosion, no centre star, no circle or ring. These thin white lines will be translated and rotated as painted sprites converging toward a hero, inspired by Xenogears power-up speed lines. 2D hand-painted pixel raster sprite craft, not vectors. True transparent RGBA background, no black/gray matte, no checkerboard, no labels, no text, no grid lines, no background, no characters or body shapes.
