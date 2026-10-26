# Astra VFX integration contract

2026-10-25. Art handoff only. `vfx.json` owns filenames, source rectangles, frame holds, pivots, blend and trigger mappings. This document owns scheduling, compositing and acceptance. All sizes are **logical screen pixels at zoom0.5**, including transparent margins. DPR2 changes render density, never the specified apparent size. A zero size component in JSON means use its placement formula.

## 1. Load without changing combat

Extend `assets.rs::Assets::load` to load `art/vfx-astra/vfx.json` and its unique PNG files. This manifest is a new schema, not the existing `ArtManifest`. Deserialize the required data with the client's existing nanoserde dependency; retain semantic IDs in a BTreeMap. Several entries reuse a file, so load each path once. Entries with `file:null` describe existing rendering and require no texture load. Reject traversal/absolute paths as the current loader does. An absent replacement file is a visible integration error; count it and fail QA. No procedural effect fallback is approved for release.

Pack PNGs are straight-alpha RGBA. Use Linear filtering, ClampToEdge, no mipmaps. Horizontal source rectangle: `(index*frame_w,0,frame_w,frame_h)`. Keep at least4 source pixels of transparent gutter. Sample within the cell using half-texel inset when filtering would otherwise reach a neighbor. Do not trim frames at runtime. Frame-local pivot coordinates are pixels before scaling. Position = projected anchor minus `(pivot/frame_size)*destination_size`, then rotate about that anchor. The current `Assets::decal` helper centers textures and cannot honor every foot pivot or sheet frame; add a focused `Assets::vfx_frame` draw helper rather than feeding complete strips to `decal`.

Renderer material multiplication is `texture RGBA * tint RGBA`. Default-material alpha blending preserves painted dark edges. The existing additive material uses SourceAlpha + One. Use WHITE on colored assets. Neutral derivatives preserve original alpha and use maximum-channel luminance so team tint remains clean. Never tint an orange raster blue. Blend changes must be restored before the next pass. No new shader or dependency is required for the approved pass structure.

Ground projection remains `camera.project(world)`; only ground-local y distances receive0.75 squash. Upright burst/actor/head sprites do not receive a second squash. Projected projectile direction is `normalize(dir.x,dir.y*.75)`; angle is its atan2. All listed screen sizes scale by `camera.zoom/.5` if a future supported camera zoom changes. Boss hits stay capped40px so the large boss never turns every basic attack into an explosion.

## 2. Single event owner and clock

Use snapshot time for ages. Pause freezes all FX; S advances one sim step. One-shots advance by cumulative `frame_ms`; remove once age reaches their sum. Avoid `clips::sample` holding the last frame forever. For a one-shot with lifetime L, multiply the last frame by `clamp((L-age)/last_frame_duration,0,1)` to reach transparent exactly at L. First-frame alpha is1; no sine fade-in. Native frame shapes supply the expansion.

In `Presentation::ingest`, retain scene-epoch cleanup at the last `SceneReset` in the event batch. Clear all impacts, cached hazard shapes, projectile observations, cast latches, corpses, pickup records and shake state. Preserve the current suppression of death animation during wipe cleanup. Run each event owner once per drained batch.

Build a batch ownership set before generic hits: Split pairs `(hero,target)` from `SplitStrike`; Chain targets from `ChainHop`; Poison from the element. Preserve amount/crit on the associated `Hit`. Route one impact to its owner and still create its damage popup. Chain may not duplicate a second Arcane effect; Faze may not duplicate generic Poison. If a Chain target also receives an unrelated hit, suppress only the corresponding Runa source hit, matching actor archetype and target, rather than every hit to that target. If multiple sources of the same archetype exist, existing Event data cannot disambiguate every collision; retain one generic contact instead of suppressing unrelated damage feedback.

Trigger position is a copy of the current/previous actor position at the event, with chest offset `70*visual_scale(actor)*zoom`. Freeze this contact for hits. Set contact6px toward the attacker to expose the spark beside the body. This replaces the current behavior of dragging old impact sprites along with a moving target. Projectiles, sustained auras and buff ribbons follow their own live anchors.

Keep a small presentation-only hazard cache keyed by id containing latest full HazardView. Refresh from current and previous snapshots, clear on scene reset. `HazardResolved` can then resolve geometry after a hazard disappears; expire cached non-live ids after0.3s. Do not invent missing positions at world origin. A hazard that spawned and disappeared between both snapshots may have no geometry in the frozen events. In that case omit decorative blast, retain damage floats, and report the missing-cache counter; the integration QA at4× must establish whether this occurs. A future per-step presentation hook can eliminate that information gap if observed. No API or simulation mutation is included here.

There is **no hit-stop** in this package:0ms. Cosmetic shake applies only to enrage or a major boss explosion, never to ordinary hits. At most2px peak for120ms: `x=2*(1-t)^2*sin(2π*3t)`, `y=.6*(1-t)^2*sin(2π*2t)`. Replace, never accumulate, active shake. Offset the entire world presentation together; HUD stays fixed. Respect reduced-motion settings by using zero shake. Combat timing and camera framing remain authoritative.

## 3. Draw order with explicit visibility guarantees

Split current `Presentation::ground`/`impacts` responsibilities into these passes, wired at the existing draw seam in `main.rs`:

1. Arena, static shadows, scorch.
2. Faze pool, neutral portals, support ornament, resurrect ground ring.
3. Under-actor sprites: smoke, fireball, boss flanks/aura/roar, column/motes, chest body and sparkle, pickup ribbons, skill ribbons/slashes, ordinary impacts, projectile tails/heads/bombs. Preserve y-sorting for chest bodies with actors if already implemented by the engineer.
4. Hostile footprint base fill, countdown fill, resolved fill, then all hostile boundary rims. Draw all rims last within this pass, sorted by hazard id, so adjacent fill cannot erase an earlier rim.
5. Actor sprites, shadows if their local implementation requires it, body bars. Ward shell is behind its actor. Bodies remain opaque over all large effects. Enemy corpse fade retains its own opacity.
6. Damage/heal/Miss floats, HUD, existing reward banner and controls; scene fade remains last.

This deliberately places the delivered world effects below actors and hostile edges. A spark still reads in the6px exposed contact area around a body. There is no full-body overdraw bloom. Do not keep the old `presentation.impacts` call drawing these same records over actors. If an actor hides an exact piece of a telegraph at its feet, retain the actor silhouette; surrounding boundary stays crisp. FX may not cover the remaining boundary. Sniper projectile art remains visible in open lanes; the affected body's silhouette wins at contact.

Decorative ground pool colors never become red. Support uses blue/green/gold; Faze uses native purple. Split's retained warm ivory/orange airborne crescent does not mark a ground danger footprint.

## 4. Function-by-function replacement

### `vfx.rs::family`, `Presentation::ingest`, `impacts`, `labels`

Replace the wind/fire/ice/dark lookup with six explicit hit IDs. Store element, crit, source direction and frozen contact on Impact. Ordinary impact frame24×24, timings25/40/55/60ms. Crit frame38×38, timings25/45/65/85ms. One contact per `(source,target,element)` per80ms; a crit promotes a lower-priority pending hit instead of disappearing behind its debounce. Keep continuous Nature bucket aggregation at750ms. Each emitted poison tick uses its purple strip and matching purple number.

Use `hit-physical` for physical, `hit-fire` fire, `hit-ice` ice, `hit-arcane` arcane, `hit-nature` nature, and poison owner `faze-impact` for ordinary Poison. Crit variants use the corresponding `crit-*`, including `crit-poison` inside the Faze owner. Hits with amount≤0 and Event::Evaded generate no spark. Elemental crit variants are final rasters with an authored secondary shard; no extra runtime particle is needed.

Normal floating text16px, crit20px, Miss14px; keep current shadow. Hold full alpha500ms then fade250ms; Miss400+250. Rise `18*(1-(1-t)^2)`px over lifetime. At most3 per target,12px vertical offset. Anchor top = actual idle-frame visible body top minus6px; constrain baseline to [60,552] after stacking. HUD needs no new text. Keep integer formatting and existing reward wording. `Noticed` diagnostic icons become debug-only.

### `projectiles.rs::draw`

Retain physical shot positions, directions, height, orphan behavior and17px bomb body. Replace four repeated head tails with one authored `orb-trail` or `bolt-trail`, then one head. Head frame1 stays static. Orb12×12, tail24×6; bolt23×8, tail34×4. Use native hero palette; enemy versions use the matching neutral files tinted pale pink. This does not recolor hero Faze projectiles red.

Tail's bright right tip sits4px/7px behind the head. Clamp length to actual travelled distance since first observation and cap24/34. First-observation time and position are keyed by projectile id. If projection direction is zero, omit trail and rotation. Do not home art on target. Remove records when id leaves snapshot, including orphan shots that exit arena.

A new Bolt id creates `muzzle-flash` at its first observed projected position,16×10 aligned to dir,160ms. This requires no missing ProjectileView owner field. For hero cast flash use Event::ActionStarted to latch actor id, state and intended target, then emit20px once at the first snapshot crossing `state_age >= impact_at`; copy the same release/impact marker selection used by `clips::actor`. Cancel latch if actor changes state or action restarts before crossing. Restrict to ranged casters, not all Basic attacks. Preserve the current clip and sim damage schedule.

Bomb fuse spark is8px, additive WHITE, offset(+3,-7) from bomb center. Flying frame holds60ms. On landing match LobberDrop by existing coordinate rule; last30% switch35ms holds and alpha pulses. Remove whole-body scaling/24px blink flash. Do not respawn fuse after hazard resolves.

### `vfx.rs` explosions / scorch

On LobberDrop or ExploderBlast HazardResolved, let `D=2*radius*zoom`. Emit `bomb-fireball` width/height1.12D, foot pivot(64,122), ground anchor at origin,340ms (35/65/100/140). Airborne painted flame may exceed radius vertically; decorative ground smoke/scorch must fit withinD. Max fireball frame112px for regular blasts; larger boss barrages retain their actual D and use crowd opacity below.

At+70ms emit `blast-smoke`, width.90D, height.64D, foot pivot(64,122), opacity≤.38,480ms (65/100/140/175). At+70ms place scorch .85D×.6375D, dark tint(75,52,38), initial alpha.30; hold until400ms then linear fade to0 at2200ms from original resolve. Maximum8 scorch decals; evict oldest. Delete the expanding `rim` shockwave and generic `flash` overlay entirely. Sim resolution is the only trigger, never bomb visual landing.

For four simultaneous barrage blasts, one fireball and one smoke per blast, with alpha=.80 and .28 respectively; stagger nothing that could imply later damage. The shape's own frame progress supplies staggered-looking fragments. Screen-wide flash is forbidden.

### `hazards.rs::draw`, `draw_one`, shape helpers

Retain canonical Circle/Cone/Line/Ring geometry, arena scissor, real hazard dimensions and tracking direction. Project vertices with squash once. Apply the generated white fill/rim/edge textures to those meshes. Normalize UVs to each mask’s occupied alpha bounds before mapping; transparent packing gutters must not shrink the indicated danger footprint. Full fill reaches the inside edge of the rim at p=1. Mesh geometry is necessary to fit the sim contract; final visible strokes sample authored raster art rather than primitive line calls.

Use `telegraph-edge` as a narrow texture along boundaries. Extract its occupied stroke band once at load; normalize that band to the full strip UV height so final stroke thickness is exactly1.5px at zoom.5. Tessellate ellipses and cone arcs with maximum1px chord error;128 segments is the upper bound for a full large circle. Compute stroke normals in projected screen space for uniform thickness. `telegraph-rim` is suitable for fixed-size ornamental rings; do not stretch its source stroke into a4px boss boundary.

Full footprint base alpha.12, progressing interior alpha.34. Hostile RGB(255,55,75). For Circle, moving radius=`radius*p`; Cone length=`length*p`; Line filled length=`length*p`. Preserve existing line width/width_scale, because that is part of the supported attack geometry. Ring fills from inner to outer radius using existing safe-center shape. Clamp p from the snapshot, no easing. This brief's source-out rule explicitly replaces BossNova TwoWay's old inward-rim visualization; display radius*p while retaining its authoritative progress and resolution.

Estimate remaining time only when current and previous phases match Locked and progress increased: `(1-p)/((p-prev_p)/(time-prev_time))`. If there is no valid slope yet, show ordinary warning rather than guessing duration. When remaining≤.15s, q=clamp(1-remaining/.15,0,1), pulse=`sin(π*q)`. Tint rim toward(255,145,150) by pulse and increase fill alpha by at most.05*pulse. Never animate radius beyond p. On HazardResolved render p=1 in the resolution frame even if prior sampled progress was below1, then fade resolve footprint alpha.18→0 in80ms. Last-frame pulse never delays damage.

SpawnMarker uses36×27 portal, frames0/1/2 at progress0/.30/.70; on Spawned show frame3 for200ms and fade. Match marker and actor by nearest same-position spawn, with a small tolerance matching current spawn placement. It never inherits hostile tint or resolution flash.

Faze Active: one `faze-pool` alpha.22, width2r*zoom, height*.75; keep full footprint until expiration, opacity fade only during last10% of Drain. Delete prior concentric shrinking fill and hatch. Resolved Faze draws nothing and never enters the shared hostile-flash path. Ward/Elevate cast once: neutral portal blue/green42×31.5 over300ms, then gone; no enduring radius circle. KajaAura remains visually hidden.

SniperLine/BossSnipe Active: remove full-length `draw_line` flash. Retain beam source/dir and first Active time per hazard. End at the physical bolt's current position projected along dir, clamped to shape length. Match a same-team Bolt travelling within.01 directional dot tolerance and within the lane, launched at this source. A shot without an unambiguous match gets its head and trail only. This prevents implying a damaging instantaneous beam. Use `sniper-beam-neutral`, tint(255,150,170), thickness4px, alpha.60*(1-age/.11); no stroke beyond travelled front.

### `actors.rs::draw` and `Corpses`

Remove the 24-copy boss glow loop. One `boss-energy` behind the body at chest, size(1.22H,1.42H), where H is visible idle body height at current scale; alpha=.06+.20*energy² while energy>0. At energy crossing1, a separate220ms flare at alpha.40*(1-t)², scale1+.08t. Warm gold remains distinct from red rage.

On Enraged: `enrage-roar` at chest, frame size min(1.55H,112),480ms. Then hold frame2 for sustained aura at size min(1.35H,96), alpha .12+.04*sin(2π*.75*time). Full charge flare is suppressed during initial roar to prevent stacking bloom. Boss bar and art stay visible above these sprites.

Enemy Died keeps the existing KO clip and frozen corpse. At clip end emit `ko-puff`, size min(.70H,42), ordinary target30px maximum; fade corpse over420ms. Downed heroes retain their final KO pose and never dissolve. No death effects on WaveReset or scene cleanup. WardGained emits blue shell24×35 for200ms behind its actor, debounced250ms; lasting ward remains visible in the bar.

### `wishfire.rs::Wishfire::ingest/draw`

ChainHop anchors both actors at their event chest positions. Play `chain-strike` for180ms, width equal projected separation, height clamp(distance*.15,8,18). Use its four frame holds25/40/55/60. Map painted ribbon's occupied horizontal span between endpoints; exclude transparent gutters. Endpoints are equal-height in local coordinates before rotation. Emit target `hit-ice`24px in the same event batch; associated crit uses `crit-ice`38px. Remove existing born+0.25 delay. The immediate impact describes the current sim event, while the ribbon is a brief connection trace.

SplitStrike plays `split`58×39,220ms; orient its convex right edge along caster→center. If projected victim span exceeds44px, grow width to clamp(span+14,58,80), height=width*39/58. Emit per-victim physical24px or crit38px once, suppress generic duplicates. Keep original C-shaped ivory/orange blade identity. Do not stretch the square strip itself to an arbitrary rectangle without honoring the destination size.

FazePool spawn plays `faze-impact`44px at the origin for220ms. Poison Hit plays same family26px at victim chest; crit uses supplied purple crit. Pool drawing remains in hazards ground pass. Do not tint these assets red and do not add text for the skill names.

### `rewards.rs` and `resurrect.rs`

Chest body art and foot pivot remain from rewards.json,32px canvas height. Drop350ms: height=`12*sin(π*t)`; at landing apply one8% y squash for60ms with reciprocal x stretch, then restore. Opening state shakes at existing frequency but cap angle.025rad. At ChestOpened play chest-sparkle44px,600ms, pivot(64,122) at lip. Retain authorized banner timing/contents. Emit buff-ribbons22×38 on each living hero;600ms and35ms index stagger, no travel simulation or pickup logic.

Resurrect column28×104, pivot(32,252) at downed foot, opacity .18+.12*progress; no pulsing large halo. Ring40×30, alpha.30 base plus gold progress edge in one mesh. Three sparkle motes using chest-sparkle frame3 at18px, each rises60px over850ms, phase offsets0/⅓/⅔, alpha≤.32*(1-phase); no9-mote pass. Resurrect progress uses HazardView.progress, including retention/decay after interruption. Do not compute a new5-second timer. Interrupted fades column/motes120ms, keeps subdued retained ring at alpha.12 if hazard persists. A matched Revived emits resurrect-burst52×64,600ms; skip on wave/scene reset. One18px neutral gold glint marks active reviver, under their body.

Scene fade remains the existing black rectangle using `stage.fade` and the existing SceneReset moment. No new banner, vignette or letterboxing.

## 5. Fixed budgets and acceptance

Preload48 unique textures; the current set's exact compressed and decoded byte totals are in VALIDATION.json. No runtime image decode per event. No per-frame file loading. Reuse bounded vectors.

Decoration budget: maximum112 textured FX quads/frame and48 transient FX records (persistent hazard/actor views excluded). Pools:16 hit/crit,4 explosions (each up to fire+smoke+scorch),8 skill ribbons/slashes,8 spawn portals,4 pickup ribbons,4 resurrection channels,8 scorch. Per-pool caps are additional limits, not permission to exceed48 records/112 draws. One head+one trail per projectile; head is mandatory, trail is decorative. Three motes/channel is the particle ceiling; no independent spark emitters.

Priorities when decoration budget fills: omit smoke and scorch, then pickup/motes, then redundant ordinary impacts, then trails; retain crit, release cue, main blast, and rage onset. Never drop actors, shot heads, authoritative hostile footprints or damage/heal/Miss numbers to meet a decorative cap. Cache and batch hazard meshes by texture/material where possible; plan≤4 geometry submissions per hazard, with96 submissions reserved for24 simultaneous hazard shapes. This is a target budget, not a measured runtime pass. Report actual peak `DrawStats.calls`, frame time and GPU submissions separately; current counters approximate submissions.

Engineer acceptance at360×640/DPR2,1× and4×: test farming swarm, four-bomb barrage, each boss normal/enraged, every skill, downed→interrupted→resumed→revived, chest reward, wipe/reset and orphan projectile. Record motion. Compare actual damage step with peak start; ≤one30Hz step alignment error, zero fixed250ms Chain delay. Pause/S must freeze/advance sprites predictably. Every hostile countdown reaches its rim at resolution; active beam stays behind shot front. All hero bodies and exposed hostile rims remain visible through the busiest frame. No red hero pool, missing file, edge bleed, double squash, repeated final frame, duplicate special impact or wipe death puff. Compare unchanged seeded sim hashes at matching steps. This handoff does not certify those runtime checks.

## First implementation order

1. Correct Chain event alignment and remove duplicate/oversized special impacts.
2. Replace blast stack and enforce the under-actor/under-rim pass order.
3. Apply exact textured hostile geometry, single source-out fill and final150ms pulse.
4. Replace boss24-copy glow with energy lobes and explicit rage burst/aura.
5. Replace six hit families, critical shapes and repeated-head trails; then rewards/resurrect polish.
