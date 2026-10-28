# Gloamink self-review · 2026-10-27

Disposition: CONCERNS for lead art-director review. All requested deliverables exist. Automated export checks pass. Art-director approval remains pending.

## Concept match
- Silhouette: four legs, forward crouch, swept ears, long tapered bushy tail and small harness retained. `vs-concept.png` compares identical 128 px canvases at 3x on both backgrounds. The rebuilt torso is rounder and the near foreleg is more tucked than the approved drawing; the tail root has a stronger upward hump. These are fidelity weak points.
- Palette: ash-grey paint, cream face/chest and claws, brown outline, deep red cloth, navy panel and gold edging retained. Generated paint has local shading differences; this is a repaint rather than pixel-identical source extraction.
- Face: narrow gold eye, dark socket, pointed muzzle and pale cheek retained. Ear/cheek contours vary slightly from the source. The mouth stays closed during the claw lunge; there is no new jaw drawing.

## Motion and role
- Idle: quiet head and two-joint tail motion in the low stance.
- Walk: two gallop cycles in 12 frames, rear drive and offset foreleg catch. Upper leg, shin and paw articulate separately on all four legs. Head stays low. This supports a fast fragile backline hunter; absolute 112 movement speed belongs to the client.
- Basic / attack: 9-frame crouch anticipation, forward claw lunge, recoil and recovery. Paw orientation compensates for the leg swing. Horizontal travel is deliberately contained by the 128 px canvas; client travel must provide the longer dive past the front line.
- Cast: 12-frame alternate stalking pounce using the same anatomy. It adds no spell or VFX design.
- Hurt / hit: 6-frame sharp head/body flinch with quick recovery.
- KO / defeated: legs fold, head rolls toward the ground and body settles into a flattened side silhouette. Last frames hold. The cut-out fall uses vertical compression and keeps the eye open; this is the weakest state for natural anatomy.
- Spawn: begins airborne, springs forward/down, compresses and settles into the crouch. It begins visibly present; no artificial fade is used.

## Joints and edges
- Reviewed every left frame in all seven final contact sheets on sand and #101116. The right exports are pixel-exact semantic mirrors, verified automatically.
- No open limb separation or transparent tearing was seen at runtime size. Shin/paw paint overlaps by 24 percent of the original lower-leg height. Tail base/tip and shoulder paint overlap throughout the sampled poses.
- At 3x the tail join and shoulder layering remain perceptible as cut-out paint boundaries. Those visible seams warrant lead review; seamless repaint fidelity is not claimed. The upright tail root also makes the joint more noticeable than in the concept.

## Canvas and ground
- 144 RGBA frames, each 128x128. Significant alpha (>=24) stays strictly inside every canvas; `checks.json` records all 72 left bounds. Right bounds follow by exact reflection.
- Idle, walk, hit and defeated significant-alpha bottom is consistently 125 (exclusive bbox edge, visible ground row approximately 124). Manifest foot origin is (64,125).
- Attack/cast bottoms range 121–126 during the pounce; spawn 115–126 while airborne and settling. Grounding measures the lowest painted contact, rather than locking a named paw in world X. Some treadmill foot slide is possible when client movement and this two-stride cadence differ.

## 58 px readability
- `readability-58.png` shows a representative middle frame of every state at 58x58 on both backgrounds. Swept ears, pale face/chest, grey quadruped silhouette and pale tail remain visible. Harness reads as a small red/navy/gold accent; gold detail and individual claws merge at this scale.
- Small foreleg movement and the closed-mouth attack are less distinct at 58 px than the head lunge. The KO silhouette is clearly low and still.

## Export proof and limits
- Synfig 1.5.5 rendered native parented bone clips at 1024x1024. Pillow Lanczos reduced to straight-alpha RGBA128; transparent RGB is zero. Native SIF sources exist for both facings plus neutral.
- Manifest follows the existing per-actor schema with `basic`, `hurt`, `ko` semantic keys, the requested frame filenames/counts, 1000/12 ms holds, only idle/walk looping, relative paths and foot origin (64,125).
- Source checks verified dimensions, all referenced files, frame holds, loop flags, canvas bounds and exact mirrors. Review covered rendered contact frames and fixed-scale stills; continuous playback, native Synfig GUI editing and battle integration were not verified.
- The first render was too squat and clipped during lunge/KO. Revised proportions and source-level hull constraints removed clipping. Next decision belongs to the lead art director: accept or request a bounded fidelity/motion revision against these sheets.
