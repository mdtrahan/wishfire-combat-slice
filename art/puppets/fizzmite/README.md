# Fizzmite puppet · ORKA-6jh1.8

Built from the owner-approved `art/_work/enemy-identities/new/fizzmite-source.png` and checked beside `fizzmite-128.png`. Built-in image generation supplied isolated painted shell, underside, leg, fuse and flame pieces with the approved source attached. The face and sparks retain approved-source pixels. `source/provenance.json` pins source hashes. No runtime files changed; no commits.

Editable Synfig 1.5.5 sources use 14 painted parts, six independent leg controls and parented shell → fuse → flame → spark controls. Every clip has both facing sources. `neutral-*.sif` opens the idle rig at frame zero. Native canvas 256×256, foot (128,250); native 1024×1024 renders reduce through Lanczos to straight-alpha 128×128, foot (64,125). Alpha values ≤4 are cleared to remove resampling ringing. Delivered right frames are exact semantic mirrors; costume and shell asymmetry reverse.

From this folder: `python3 source/build.py` rebuilds everything; `python3 source/check-source.py` verifies it. Requires installed Synfig, Pillow and NumPy. `--state cast` renders one state; `--prepare-only` rebuilds source files without rendering. Sources read the approved concepts in their existing location. Generation prompt is in `source/imagegen-prompt.txt`.

The per-actor manifest follows the existing semantic schema: `basic` uses attack filenames, `hurt` uses hit filenames and `ko` uses defeated filenames. Idle/walk loop; all other states hold their final frame. Holds are 1000/12 ms. Sim inspection: `enemies.rs` triggers Exploder Cast within 55 units, with current `EXPLODER_FUSE=1.0` in `tuning.rs`; its ordinary Basic does not perform the detonation. The supplied basic clip is the required wind-up variant. No explosion is painted.

Lead review: seven `qa/contact-*.png` sheets contain every left frame at 3× on sand and dark. `qa/vs-concept.png`, `qa/readability-58.png`, `qa/review.md` and `qa/validation.json` document comparison, limits and checks.

Revision 2 supersedes the motion assessment in `qa/review.md`; see `qa/review-r2.md`. Round 1 frames and QA are preserved in `_r1/`, with its builder/checker. `qa/readability-58-sequence.png` shows every frame at actual phone size on both backgrounds. `qa/r1-vs-r2-{walk,attack}.png` places round 1 above round 2, frame by frame. Three `qa/playback-58-*.gif` files provide 12 fps phone-size playback with a final-pose review pause for wind-ups. `qa/motion-r2.json` records amplitudes and unchanged-state checks. Runtime manifest, counts and timing remain unchanged.
