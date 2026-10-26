# Healing Spring: Moonlit Current production set

Owner selected concept A. Lead/art director: Claude. VFX artist: GPT Astra. The selected A was titled Twin Confluence in the final concept-v2 gallery; it is the same a-moonlit-current artwork selected by the owner. Owner passed the mobile affected-ally and zone motes. Date: 2026-10-25.

## Authorship and references

Built-in image_gen generated the raster light artwork. The selected zone reference is exec-90c6050b-cbdd-4c21-b8dc-82de9bdcbd8e.png; recipient reference is exec-c1a70ebc-4e30-4ce0-9864-ecc7c70827be.png. Both live under /Users/Mace/.codex/generated_images/01a174a3-67cf-7602-845d-db36418cd0d8/. Their concept lineage uses the owner-supplied FFX Valefor summon frame, /Users/Mace/.t3/userdata/attachments/5489509e-3800-46e0-9c98-aca707e0a6be-254509cc-a026-475e-9cf5-66635c0c7e97.png, as a visual reference. No pixels from the FFX frame are copied into the deliverables. Approved project finishes studied include bubble-swell, Ground Pound eruption and crimson crescent.

Final source paintings use the same tool-managed source directory. Exact prompts, source-path manifest, packing recipe and verification results are retained in art/_work/healing-spring/final/. No external stock assets, vector drawings or procedural light primitives were used.

| Production file | Generated source | Source SHA-256 | Baked RGB gain |
| --- | --- | --- | --- |
| spring-ring-outer.png | exec-81c25f3d-b9d3-43eb-be04-433ca0f70f79.png | 831ce8df051271b2aee8a02009b478af3d10840ef60afb69618dccd359c4a0df | 0.27 |
| spring-swirl-inner.png | exec-68111825-710e-4d98-b7df-e35adc49cc96.png | ffed8e5254d8a699d719c201d619debe0ce0648ab044844b457c4de52a155233 | 0.19 |
| spring-core.png | exec-d32798a2-8abf-4b2e-8b85-1297edc0b69b.png | 06474da1c9108cf1dfab1ad2050d444e9bf37221f502b600769b695a905012be | 0.045 |
| spring-motes.png | exec-28948f38-2698-411f-88a2-5ba27ba51933.png | 68a6c26302642d2c32aae20f42d99ecbe2d3a77f8ba51cdea968cb85dc0af954 | 0.65 |
| spring-land.png | exec-64fe6df3-bf7e-465f-8a08-cddd6f424c1a.png | 16da18715229b4a5201ee70ebf8c726fa2125e5304148f7d1dbeeb82919085a8 | 0.23 |
| spring-ally.png | exec-6abab64b-16cc-4437-8d1a-84d757144c2b.png | f561840e9b4713ff1d968f44cabb902843a4559d9d49b34918e82b89583b3ecf | 0.29 |
| spring-ally-motes.png | exec-f2b4b03f-6d79-48a5-9ad0-9d42c2c25368.png | 5060e4ef256ba499722b579369604abd5905979d9e4764b1b2393700dcca1200 | 0.65 |
| spring-heal.png | exec-d70da487-040d-49b4-9dce-d842420d8b57.png | 02d18a239b9438c07c4bb22cda2c6e6c7abaca6704b9c33fe09e9227efec56b3 | 0.48 |

## Production preparation

Source sheets were split by their regular grids, resized into fixed frame sizes and packed horizontally. Source alpha is preserved except effectively invisible alpha <=4, which is set to zero. Every frame has at least 3px of empty gutter on each side inside its stated frame dimensions; there are no extra pixels between frame rectangles. Transparent RGB is zero. RGB is exposure-scaled for additive drawing, preserving straight alpha. Final files are losslessly compressed RGBA8 PNGs.

The three persistent layers share 512x384 frames and centre pivot [256,192]. Their source art is overhead; storage is normalized to 4:3 for the same 276x276 world quad and 138x103.5px projection as faze-pool. The inner swirl and core are inset inside the boundary. Rotate in world ground space before projection. The texture aspect must not be squashed a second time. Screen-space rotation of an already projected ellipse is incorrect.

All current strips use their source cells in reading order. No frame was synthesized from procedural VFX shapes. Optional adjacent-frame interpolation uses the authored frames with complementary weights.

## Blend and timings

All assets use additive SrcAlpha/One. PNG light values already carry baseline exposure; draw with white tint and opacity 1. A One/One implementation must premultiply by texture alpha once in the shader. This set is not designed for normal alpha or screen blending.

The zone lives for 5s. Suggested rotations: outer +5 degrees/s, inner -9 degrees/s, core +2 degrees/s. Ground layers fade in over 0.18s and out over the final 0.2s. Landing: 6 frames at 20fps, 0.30s. Zone mote: 8 at 8fps, 1.0s one-shot. Ally ankle echo: 6 at 6fps, 1.0s loop. Ally motes: 8 at 8fps, 1.0s loop. Heal tick: 5 at 20fps, 0.25s, triggered only by simulation heal events.

Each affected hero receives one ankle echo and one mote strip with staggered phases. Ally motes use 0.65 behind all actors and 0.35 in front. Each ally has roughly 12-16 varied light points and glints. The zone uses nine three-mote clusters in the review frame, with a suggested runtime cap of twelve clusters. Detailed placement and draw order are in spec.json.

## Evidence and scope

Final sand and spotlight frames, detail crops, Faze comparison and standalone playback live only in art/_work/healing-spring/final/. Actual project sprites are shown at 32px height, with Runa/Fara/Hondo inside and Gobloc outside. Sand uses the existing oasis corridor with central colour matched to RGB 163,146,120. Spotlight applies the existing 80% background scrim. These are art mock frames and standalone playback, not engine captures.

Frame dimensions, 3px gutters, transparent RGB, PNG hashes and loop transition differences were checked. Additive composition never darkens the ground. At the checked settled time, less than 1% of ground-test pixels clip any colour channel; visual inspection confirms ground texture remains visible. Runtime integration, GPU colour-space behaviour and gameplay remain unverified and lead-owned.

Replaced rejected spring-pool/spring-splash/spring-bubbles with the separated set and repainted spring-heal. No preview images are stored in the production folder. No code outside the authorized scratch folder changed. No commits.

## Mobile visibility revision: motes PASS

The owner passed spring-ally-motes and spring-motes. Ally motes occupy 48x88px and rise above the head with varied pearl sizes and sparkle glints. Surface clusters use 18x18px and lift 20-36px across the zone. Updated RGB exposure is baked into these PNGs. File IDs, frame counts, frame sizes and timing remain stable; all retained PNGs are unchanged by the rejection cleanup.

Exact prompts, source hashes, packing recipe, structural checks, phone frames and playback from the mobile review remain in art/_work/healing-spring/final-v2/. Those historical review frames include subsequently rejected elements and do not represent the current production composition. Runtime integration remains unverified.

## Owner rejection

The owner rejected the ally light shafts and tall rim pillars. spring-ally-rays.png and spring-pillar.png were moved unchanged to art/_work/healing-spring/rejected/ and removed from the production asset list, timing and draw instructions. Everything else remains. No commits.
