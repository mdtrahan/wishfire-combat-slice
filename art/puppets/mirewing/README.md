# Mirewing puppet • ORKA-6jh1.8

Owner-approved Mirewing source and 128px concept are preserved in `source/approved-source.png` and `source/approved-128.png`. Visible paint is extracted from that source, preserving its face, palette, plum markings and costume. Built-in image generation, with the approved full-resolution source attached, produced `source/generated-parts-atlas.png`; a small cleaned teal crop supplies hidden attachment tissue. Pillow separates the approved paint and removes low-alpha fringe. No projectile is painted.

`source/parts.json` records painted bounds, pivots and parents. Native Synfig 1.5.5 SIFs contain editable skeleton bones and bone-linked imported PNG layers. Shadow is root-parented at native (128,250); the flying body parents both wings, glands, mouth and body paint. Wings remain independent from the body. The paired near wings share one attachment; the far wing has its own.

Rebuild: `python3 source/build.py`, then `python3 source/qa.py`. Requires installed Synfig at `/opt/homebrew/bin/synfig` and Pillow. Rendering uses native 1024×1024 RGBA, then Lanczos to straight-alpha 128×128. Left is the approved source facing; right frames are exact semantic horizontal mirrors. Right-facing editable SIFs carry the same semantic mirror.

Manifest is an actor entry with paths relative to `art/puppets/`. Existing Wishfire semantic keys are `basic`, `hurt`, `ko`; these point to `attack`, `hit`, `defeated` filenames. Idle/walk loop. All holds are 1000/12 ms. The foot origin is (64,125). Motion expresses role only; simulation owns movement, shot cadence, impact and poison.

Art-director candidate. No runtime integration, commits, independent critique or owner animation acceptance is claimed. `qa/review.md` records limitations.
