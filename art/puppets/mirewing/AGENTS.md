# Mirewing source contract

- ORKA-6jh1.8 art-only ownership. Preserve approved source paint and source-facing left.
- Write only inside this actor folder. Shared Wishfire assets and exporter are read-only references.
- `source/build.py` owns separation, native parented Synfig rigs and frame export. `source/qa.py` owns contract checks and review sheets.
- Shadow is root-parented at native (128,250); hover transforms belong to the body parent. Defeat settles onto the shadow.
- Manifest uses existing semantic `basic/hurt/ko` keys with `attack/hit/defeated` filenames, 12 fps, 128px frames, foot (64,125), paths relative to `art/puppets/`.
- No commits or runtime integration. Lead art-director review remains required.
