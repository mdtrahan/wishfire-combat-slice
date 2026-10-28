# Fizzmite revision 2 · ORKA-6jh1.8

Authored revision complete for lead review. Every final contact sheet was inspected on sand (#d6c09a) and dark (#101116), together with the concept comparison and every-frame 58 px sheet. Automated source validation passes. Owner acceptance and in-game motion review remain with the lead.

## Round-1 findings

- **Concept and colours retained.** Source paint, original face extraction and palette are unchanged. Idle, hit, spawn and defeated frames are byte-identical to the archived round 1. Face tension in attack/cast comes from compressing the intact head cutout; no replacement face was painted.
- **Fuse flicker retained.** The original irregular flicker samples still drive the flame. Idle remains calm with a visibly lit fuse. Walk adds an 11-degree whipping motion; wind-up adds stronger irregular rope/flame rotation and growing sparks.
- **Defeat retained.** All 24 facing frames match round 1 exactly: flame snuffs in the opening frames, sparks disappear, then the body flips onto its shell and holds.
- **Walk: alternating tripods.** Near front/rear and far middle share a phase; the opposite tripod is half a cycle apart. Each foot reaches ±6 pixels at 128 output and lifts up to 7.36 sampled output pixels. Two gait cycles occur in the 12-frame second. Hip-preserving length/angle changes replace the first revised render's detached rear-foot appearance.
- **Walk: body bounce.** Sampled body excursion rises from round 1's 1.04 output pixels to 5.20 pixels, about 2.35 pixels on the actual 58 px sheet. The body rises over planted feet and settles between steps. Actor travel stays in the game.
- **Walk: shell lag.** Shell offset and four-degree rotation trail the head phase by 0.8 radians. The shell's changing angle and lifted body remain visible at 58 px; head and shell retain overlapping roots.
- **Walk: fuse whip.** The rope swings with a delayed phase. Sparks are pulled inward to retain transparent edge padding during the larger bounce.
- **Attack and cast: inflation.** Both finish at shell scale 1.16 × 1.18, exceeding round 1's 1.095 × 1.11. This produces a visibly fuller shell through the last frames. Growth accelerates quadratically toward detonation.
- **Attack and cast: accelerating tremor.** Early rocks hold the same sign for two frames, then alternate every frame. Horizontal body range reaches 5.69 output pixels in attack and 5.77 in cast, about 2.58 and 2.62 pixels at 58 px. Feet retain their planted baseline while the body shakes above them.
- **Attack and cast: flare and sparks.** The flame base grows to 1.56 × 1.94 before applying retained flicker, and the three sparks grow by 65%. The lengthened flame stays inside the canvas. The final frame holds pressure; explosion imagery remains game-owned.
- **Attack and cast: brace.** Front feet spread 3.5 output pixels forward and rear feet 2.5 backward, giving six more pixels of stance width by the first third of the clip. Foot y channels stay planted.
- **Attack and cast: tense face.** Head height compresses 14%, width grows 3.5%, and the head pitches into an eight-degree tense pose. The eye reads narrower at 128 px. At 58 px this expression supports the body warning, with shell growth and shake carrying more of the signal.
- **Idle, hit and spawn rechecked.** Their regenerated contact sheets retain the original living fuse, recoil and uncurl. Pixel identity against `_r1/frames/` confirms the revision introduced no change to these clips.

## Phone-size assessment and weak points

The every-frame 58 px sheet shows clear differences between down and lifted walk poses. Wind-up combines a widening silhouette with frame-to-frame lateral displacement and a taller flame. R1-above-R2 sheets expose the increased amplitude directly. Timed GIFs are supplied for lead playback review; this self-review used decoded frame sequences and stills, without an in-game playback session.

The navy underside loses contrast against dark. Sparks shrink to isolated bright pixels. The whole-head squash also compresses the horn and jaw; it provides a cutout expression rather than an independently articulated eyelid. Shell inflation stretches the painted straps and hardware. Single-piece legs stretch to keep their hips connected, which is visible at 3×. The walk repeats six poses twice with independent flame variation; it has a brisk, stylized cadence at 12 fps. Actual approach at speed 90, combat clutter and damage timing require lead runtime review.

## Delivery checks

`python3 source/check-source.py`: PASS for all 144 RGBA frames, 128×128 bounds with empty outer edges, foot metadata (64,125), existing counts, 12 fps holds, semantic clip schema, idle/walk loops, parent hierarchy, stationary foot channels, exact mirrored right delivery and repeatable native renders. `qa/validation.json` contains hashes. `qa/motion-r2.json` records sampled amplitude and unchanged-state checks. All writes remain inside this Fizzmite folder; no commits or runtime integration.
