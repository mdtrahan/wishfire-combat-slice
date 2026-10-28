# Bastorto self-check

Build complete; automated export checks PASS. Lead art approval remains pending.

## Concept match

Round-2 source and 128 concept only. The grey face, pale jaw, golden eye, heavy brow and visible dusty-rose/gold shell use approved pixels. Navy harness, deep-red clasp, grey limbs and pale claws retain the approved palette and painted outline. `vs-concept.png` shows the actual idle export beside the approved concept on both backgrounds at 3x.

The decomposed assembly differs slightly in shoulder proportions and harness hardware placement. Generated harness and limb details are reconstructed paint rather than an exact pixel extraction of those regions. The neutral front leg sits a little farther back than the flattened reference. These differences are visible in the comparison and require the lead's judgment.

## Role and state motion

- Idle: all four toe pivots planted; the shell rises with breathing, with a small alert head scan. The stance remains broad and low.
- Walk: opposite diagonal pairs lift alternately, with a visible 9-canvas-pixel toe lift, pronounced shell rock and heavy body rise/sink. Ground contact returns between each lift; independent toe cutouts remain flat. Far legs become partly hidden behind the shell and near limbs.
- Attack: two-frame rearward anticipation, then a forceful forward shell/body ram and recovery. Body advances 14 canvas px from neutral; the neck absorbs the impact, with slight head compression. Shell travel remains visible even while the head braces.
- Cast: four planted toes support an extended front stance. The shell rises and flexes as the head throws back, then settles. Frame 5 deliberately holds the peak of frame 4 for one extra exposure.
- Hit: abrupt head/neck retraction into the shell with a body jolt; feet remain on the ground. The empty collar opening becomes visible during deep retraction.
- Defeated: head and legs withdraw while the shell sinks to the foot plane. Final shell bottom is y=125. Frames 8–11 hold the settled pose.
- Spawn: begins withdrawn, resting at y=125, then head and feet pop out and settle into idle. Separate head and limb emergence reads at 58 px.

No aura, bubble, glow or painted ground shadow is included.

## Measured amplitudes

Measurements use the saved native transforms and exported pixels. A 58 px review canvas applies scale 58/128. `motion.json` distinguishes rig landmarks from actual RGBA bounds and pixel differences.

| Measurement | 128 canvas px | On 58 px canvas |
|---|---:|---:|
| Walk body bob, peak to trough | 10.00 | 4.53 |
| Walk toe lift | 9.00 | 4.08 |
| Attack body advance from neutral | 14.00 | 6.34 |
| Attack anticipation to full thrust | 22.00 | 9.97 |
| Cast front-shell lift | 16.06 | 7.28 |

Walk shell rock is 10 degrees peak to peak locally, with body roll added. Every state changes visibly at 58 px. Static peak/settle holds are retained explicitly in the per-frame measurements.

## Seams and bounds

All final contact sheets and the complete 58 px sequence were inspected on sand and #101116. Neck backing, hidden hip paint and overlapping upper-leg/toe cutouts prevent detached joints. Automated silhouette checks find one connected paint component of six or more pixels in every left frame; tiny antialias islands are below that cutoff. This check supplements the visual inspection and cannot certify every internal paint edge.

All 144 exports decode as 128x128 RGBA; transparent pixels have zero RGB. No canvas edge exceeds alpha 16. The source foot origin remains (64,125). Defeated and spawn were lowered after the first proof to remove the hovering withdrawn shell. Right frames are pixel-identical horizontal mirrors of left frames.

## Planted feet

Independent toes counter body translation and rotation. Idle, attack and cast toe-pivot y stays at 123.5 with numerical error below 1.5e-14 canvas px. The visible antialiased toe edge sits near y=124. Walk lifts alternate diagonals; selected stance toes stay planted while the others move. Defeated/spawn intentionally retract the limbs. Toe pivots establish rig contact; there has been no in-game terrain or animation-timing integration test.

## Weak points and limits

The cast uses the approved closed-mouth face, so the roar is conveyed by the neck throw and raised chest. A separate open-mouth painting would make that cue stronger. At peak cast the upper-leg texture stretches as the guardian braces; overlapping toes preserve clean ground contact. Deep withdrawal retains small clasp/plastron details beneath the shell. Far-leg visibility is limited by the approved three-quarter view. Harness reconstruction and subtle silhouette differences remain the main concept-match risks.

`source/check.py` passed dimensions, counts, semantic mappings, exact mirrors, alpha bounds, connected paint, amplitude gates and planted toes. A fresh native idle-frame render reproduced every exported pixel (`repeat-render.json`). Runtime integration, playback against combat timing, native Synfig GUI editing and independent lead critique remain unverified.

The amplitude targets were met. The smallest next step is lead review of the complete sheets and cadence GIFs before integration.
