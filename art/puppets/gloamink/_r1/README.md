# Gloamink puppet · ORKA-6jh1.8

Authored 2026-10-27 with the built-in `image_gen` tool (backend model identifier was not exposed), Pillow and Synfig 1.5.5. The approved concept was attached to image generation. Painted parts retain ash-grey fur, pale cheeks/chest, gold eye, swept ears, bushy tapered tail and the red/navy/gold harness.

Approved source: `../../_work/enemy-identities/new/gloamink-source.png`; comparison sprite: `../../_work/enemy-identities/new/gloamink-128.png` (paths relative to this folder).

`source/parts-left-v1.png` preserves the generated sheet. `source/prepare.py` isolates paint with Pillow, builds 16 parented painted parts with separate shin/paw joints, writes neutral and seven state SIFs in both facings, renders left at 1024, reduces with Lanczos to straight-alpha 128 and creates exact semantic mirrors. Ground origin: (64,125). Run `python3 source/prepare.py --render`, then `python3 source/check.py`. Requires existing Pillow and `/opt/homebrew/bin/synfig`.

Manifest matches each existing actor object: semantic clip keys `basic`, `hurt`, `ko` map to `attack`, `hit`, `defeated` filenames. Only idle/walk loop. 72 frames per facing; each hold is 1000/12 ms. Relative manifest paths resolve from `art/puppets/`.

Review `qa/review.md`, seven contact sheets, `qa/vs-concept.png`, `qa/readability-58.png` and `qa/checks.json`. This is an art-director review candidate. No runtime integration or commits.
