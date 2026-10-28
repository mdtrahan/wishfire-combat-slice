# Bastorto

Cut-out guardian tortoise for ORKA-6jh1.8. Round-2 approved `art/_work/enemy-identities/new/bastorto-source.png` and `bastorto-128.png` are the sole concept inputs. Immutable copies and SHA-256 hashes live in `source/`. Rejected r1 designs were excluded.

Built-in image generation received the approved source and produced `source/parts-left-v1.png`, a transparent atlas of nine painted parts. Pillow isolates paint islands and recovers approved face/neck and visible shell pixels directly from the concept. Generated paint supplies the navy harness, red clasp, plastron, hidden limb anatomy and tail. Four separate toe cutouts preserve flat planted feet. `parts.json` records sizes, pivots and parent links; `provenance.json` records inputs and pipeline references. Harness detail and limb contours were reconstructed and differ in small details from the flattened concept.

The source follows Gloamink/Fizzmite's native Synfig skeleton and bone_link pipeline. Each state has editable left/right `.sif` files. Native canvas 256, author render 1024, Lanczos export 128 RGBA, transparent RGB cleared, semantic foot (64,125). Right runtime frames are exact horizontal mirrors. No aura, bubble, glow or painted shadow is included.

Run from this folder:

```sh
python3 source/prepare.py
python3 source/check.py
```

Requires existing Pillow, NumPy and `/opt/homebrew/bin/synfig`. No dependencies were added. `--prepare-only` rebuilds sources without frames; `--only=attack` renders one changed state and refreshes QA using the remaining existing exports. The default rebuild renders all seven states.

Frames per facing: idle 12, walk 12, attack 9, cast 12, hit 6, defeated 12, spawn 9. Each hold is 1000/12 ms. Idle/walk loop. Manifest semantic keys basic/hurt/ko resolve attack/hit/defeated filenames; frame paths retain the actor prefix expected by the slice asset builder.

`qa/contact-*.png` contains every left frame at 3x on sand and dark backgrounds. `qa/readability-58.png` contains all frames of all states on both backgrounds, each full canvas reduced to 58 px. `qa/preview-*.gif` adds cadence previews. `qa/motion.json` records consecutive bounds and pixel changes at both sizes, sampled world landmarks and amplitude measurements. `qa/validation.json` records export hashes, silhouette components, bounds, mirror checks and planted-toe error. See `qa/review.md` for visual findings and limits.

Only this actor folder was written. No commits. Runtime integration and lead art approval are pending.
