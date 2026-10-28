# Gloamink puppet · ORKA-6jh1.8 · revision 2

Authored 2026-10-27 with the built-in `image_gen` tool (backend model identifier was not exposed), Pillow and Synfig 1.5.5. The approved concept was attached to image generation. Painted parts retain ash-grey fur, pale cheeks/chest, gold eye, swept ears, bushy tapered tail and the red/navy/gold harness.

Approved source: `../../_work/enemy-identities/new/gloamink-source.png`; comparison sprite: `../../_work/enemy-identities/new/gloamink-128.png` (paths relative to this folder).

`source/parts-left-v1.png` preserves the generated sheet. `source/prepare.py` isolates paint with Pillow, builds 17 parented painted parts with separate shin/paw joints, writes neutral and seven state SIFs in both facings, renders left at 1024, reduces with Lanczos to straight-alpha 128 and creates exact semantic mirrors. Ground origin: (64,125). Run `python3 source/prepare.py --render`, then `python3 source/check.py`. Requires existing Pillow and `/opt/homebrew/bin/synfig`.

Manifest matches each existing actor object: semantic clip keys `basic`, `hurt`, `ko` map to `attack`, `hit`, `defeated` filenames. Only idle/walk loop. 72 frames per facing; each hold is 1000/12 ms. Relative manifest paths resolve from `art/puppets/`.

Round 1 is preserved byte-for-byte in `_r1/`, including `frames/`, `qa/`, original native sources, manifest and documentation. `_r1/archive-sha256.json` verifies 198 preserved files. Leave this archive unchanged.

Revision 2 separates the standing and lifted forelegs, lengthens the stance, adds a painted neck overlap and broadens the tail joint overlap. Walk is one 12-frame gallop with offset fore/hind legs, flight and torso stretch/compression. Attack uses a backward crouch with a tucked tail before forward head/foreleg extension. Defeat folds and splays the legs as the rigid torso settles onto its side; global vertical compression has been removed.

Review `qa/review-r2.md`, seven contact sheets, `qa/vs-concept.png`, `qa/neutral-overlay.png`, `qa/readability-58.png`, the seven all-frame `qa/readability-58-<state>.png` sheets, and `qa/r1-vs-r2-{walk,attack}.png`. Comparison sheets place round 1 above round 2 for each background. `qa/checks.json` covers exports; `qa/motion-checks-r2.json` covers motion and connected paint. `source/poses-r2.json` records native bone poses and world joints. Animated `qa/playback-<state>.gif` files provide both facings on sand and #101116. GIFs are review aids; PNG frames and manifest timings are authoritative.

Run `python3 source/prepare.py --render`, then `python3 source/check.py`. For a focused render, append `--only=defeated` (or another state). Regenerate all states after any shared rig change. This is an art-director review candidate. No runtime integration or commits.
