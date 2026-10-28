# Gloamink revision 2 review

Disposition: CONCERNS for lead art-director review. Revision deliverables are complete. Export checks pass. This document does not grant art approval or runtime acceptance.

## 1. Concept drift at neutral

Separated the four hip/shoulder and shin/paw placements. The near foreleg lifts ahead of the chest; the far foreleg plants farther forward, with the two hind feet separated. Added an overlapping painted neck under the head and torso so the longer stance retains a continuous chest. Neutral ear height, head/torso spacing and ground line were compared with the approved 128 px concept on the same canvas. `vs-concept.png` provides the direct comparison; `neutral-overlay.png` keeps their coordinates unchanged.

The tail now has a deeper shared joint, a broader distal section and a root that overlaps the rump. Root and tip remain parented; anticipation folds the tail to leave room for backward body travel. The connected-paint test covers every exported pose and finds no detached island larger than 12 pixels at alpha 48. Visual inspection includes every state on sand and #101116. The original transparent break has been removed.

Remaining weakness: neutral remains a reconstructed cutout. The torso is rounder, the planted foreleg bends more, and the lifted paw sits more horizontally than the concept. The tail has a stronger curl and its overlapping paint changes direction at the joint. At enlargement, that boundary can still read as a cutout seam. Exact silhouette overlay fidelity and seamless repainting are not claimed.

## 2. Walk almost static

Replaced the two tiny strides with one complete 12-frame gallop. Foreleg contact and hind drive lead into flight, gathering, forward reach and the next contact. Far limbs trail near limbs by two frames. Torso scale changes from 0.88 to 1.14 horizontally with opposing vertical compression; the head stays aimed forward while the tail follows the stride.

Native world-joint measurements: near/far forepaw horizontal spans 24.9/28.3 px; hind spans 27.4/23.5 px. Body vertical travel is 12.6 px, about 5.7 px at 58 px presentation. Flight moves the lowest paint about 9 px above the planted baseline. `readability-58-walk.png` shows every frame at actual 58 px dimensions. `r1-vs-r2-walk.png` places R1 above R2, in matching frame columns on both backgrounds. The reach/gather contrast is visibly larger than R1.

Remaining weakness: ears sweep back with the head pose and have no independent hinge. The ear pin is therefore coupled to head pitch. Some feet cross under the belly during the gathered phase. The cadence remains the required one-second clip; matching that cadence to movement speed 112 belongs to integration. No battle movement or foot-slide acceptance was tested.

## 3. Timid attack lunge

Frames 1–2 crouch and withdraw, folding the tail upward. Frame 3 drives out; frames 4–5 extend the body, head and forelegs. Frames 6–8 recover. Body horizontal span is 15.9 px and head-joint span 26.9 px across anticipation and impact. Near/far forepaw spans are 31.6/34.2 px. These are exported pose measurements after canvas containment, rather than requested source offsets. `r1-vs-r2-attack.png` and `readability-58-attack.png` show the difference.

Remaining weakness: head and muzzle lead the dive, but the painted mouth stays closed. There is no separate jaw-opening drawing. The pose reads as a fast reaching pounce; the bite itself still depends on impact timing and contact during integration. The anticipation tail curl is pronounced.

## Other states after the rig change

Hurt retains its quick recoil and return. Cast uses a longer anticipation before the same pounce vocabulary. Spawn starts airborne, lands and settles. Defeated splays the limbs and settles the rigid torso/head onto their side; the previous global vertical squash was removed. A detached far shin during intermediate defeat poses was found by the new connected-paint check and corrected with an overlapping joint arc. Last defeat frames hold. The open eye and retained upright ear shape weaken the dead-body read; the corpse also remains recognizable as a posed cutout.

## Export and review evidence

All 144 frames are RGBA 128x128, with the original counts: idle 12, walk 12, attack 9, cast 12, hit 6, defeated 12, spawn 9 per facing. Manifest keys, frame holds at 1000/12 ms, foot origin (64,125), relative paths and loop flags are preserved. Right exports match a horizontal reflection byte-for-byte. Significant alpha at threshold 24 stays strictly within every canvas. The walk/spawn have explicit flight; planted clips settle near the foot baseline. The foot origin is metadata, not a promise that every airborne frame touches it.

`python3 source/check.py` passes schema/path checks, mirror checks, all canvas bounds, connected-paint checks and the hashes of 198 R1 archive files. `_r1/` preserves original frames, QA, source, manifest and docs. Seven contact sheets include every frame on sand and #101116. Every frame was inspected in the final overview; larger contact sheets were inspected during pose review. Both motion states were checked in the actual-size 58 px sheets. Playback GIFs provide both facings for further review; continuous playback and native Synfig GUI editing were not verified here.

The predicted gain was greater pose separation without changing the export contract. The final walk and attack have substantially wider limb/head travel, and the automated export checks pass. Remaining concept/paint and jaw/ear limits above require the lead's visual verdict. No runtime files were changed; no commits were made.
