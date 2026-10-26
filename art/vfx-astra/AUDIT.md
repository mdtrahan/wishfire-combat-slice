# Combat VFX audit

Astra • 2026-10-25 • ORKA-6jh1 isolated experiment

## Evidence and scope

Read ARCHITECTURE.md including R3/R3.2a, LOG.md decisions 12–29, all requested art manifests and render modules, plus `wishfire.rs`, `clips.rs`, `assets.rs`, `main.rs`, and frozen `api.rs`. Source hashes are in `../_work/astra/source-hashes.json`; final reading hashes accompany this delivery. The last read found Faze placement reduced from110px to80px; that concurrent improvement is preserved in this audit baseline. The engineer was changing the client during this audit. Preserve their newer Poison/Faze routing and special-impact deduplication.

Inspected supplied bomb, enrage and skill-art images. Recorded an independent headless Playwright run at the supplied port: 360×640 CSS, DPR 2, 720×1280 canvas, zero page errors, simulation time 0.93–84.73 s in the sampled section. `../_work/astra/capture.json`, JPEGs and WebM retain evidence. Most playback was 4× to reach encounter transitions; final three seconds were 1×. This supports scale and clustering findings. Sub-frame timing findings below come from source, rather than a claim of frame-accurate live measurement. Supplied historical captures support the boss audit; this run reached boss entry, not every boss variant or resurrection outcome.

`mock-*.png` are authored composites using the real arena, atlas actors, current HUD crops and delivered VFX. They are visual targets, not screenshots of an integrated replacement. Scene positions and simultaneous effects are composed for review.

Severity: **P0** breaks a cue or its timing; **P1** harms combat readability; **P2** limits polish. Fix type identifies new art, repaint, retime, or retained behavior.

## Inventory

| Effect / current owner | Finding | Severity | Prescribed fix |
|---|---|---|---|
| Physical basic hit / `vfx::Presentation::impacts` | 28px generic flash can approach a hero's entire body size; symmetric glow conveys little strike direction. | P1 | New asymmetric ivory shard strip, 24px frame, 180ms. Freeze contact position and orient to incoming hit. |
| Physical special / same | Uses the wind family, conflating movement and weapon impact. | P1 | Physical family with explicit crit or special ownership; no second generic hit underneath Split. |
| Fire hit / same | Full imported effect sampled for a small hit; broad additive values wash out on sand. | P1 | Painted orange flame wedges with white core, alpha blend; peak at 25–65ms, disappear180ms. |
| Ice hit / same | Silhouette differs too little once the general additive pass flattens color. | P1 | Cyan angular crystal fracture, 24px; preserve dark blue edges with alpha. |
| Arcane hit / same | Dark atlas family loses saturated detail under additive blending. | P1 | Indigo diamond fracture with lavender core, 24px alpha. |
| Nature hit / `family` | Shares `wind` with physical; source has no leaf identity. | P1 | Separate jade leaf blades, 24px. Keep continuous-damage batching. |
| Poison hit / `wishfire::Wishfire` | Approved purple image is recognizable; static 280ms sine envelope postpones maximum brightness. New generic suppression is correct. | P1 | Four-frame purple repaint, 26px, immediate frame0, 220ms. One owner per hit, including poison crit. |
| Critical hits / `vfx` | Crit chooses a full flipbook but does not carry a separate critical silhouette; number enlargement bears most of the distinction. | P1 | Six authored-family crit variants with a secondary shard fan, 38px frame, 220ms. Retain crit number. |
| Damage / crit / heal floats / `labels` | 950ms life and 26px stack separation produce tall clutter; anchor clamp can detach messages from actors high in the arena. | P1 | 750ms damage/heal, 650ms Miss, 12px stack separation. Anchor above actual visible body; clamp only to HUD safe bounds. Preserve integer display and batching. |
| Miss / `Evaded` | Semantic trigger is correct. A Miss must never gain an impact flash during upgrade. | P2 | Retain text only; quieter14px and 650ms. |
| Notice / `Noticed` | Warn diamonds introduce another urgent cue beside hostile boundaries; fallback prints `!`. | P1 | Keep this diagnostic under debug; no new combat text or banner. |
| Muzzle/cast flash | No dedicated release flash in the inspected projectile renderer. | P1 | New20px cast and16×10 muzzle strips at release, with bounded event/state latch. |
| Orb head / `projectiles::draw` | Small pale orb has weak direction; hero vs enemy uses multiply tint on existing art. | P1 | 12px cyan-white teardrop; neutral duplicate for team tint. |
| Bolt head / same | Static23×6 body lacks a clear energetic leading edge; edge can disappear against sand. | P1 | 23×8 spearhead, frame1 held, native gold or neutral hostile pink. |
| Projectile trails / same | Four scaled copies create bead trains and spend four extra draws per projectile. | P1 | One continuous painted trail per head, 24×6 orb or34×4 bolt; never attach trail to target position. |
| Bomb body and fuse / same | Existing17px bomb reads well. Whole-bomb1.15 scale blink plus24px flash can resemble an early impact. | P1 | Retain bomb raster and landing timing. Add8px fuse spark; last30% fuse acceleration affects spark only. |
| Projectile shadows | Soft shadow is adequate; all shots currently receive it regardless of visible height. | P2 | Retain for airborne bombs; omit tiny flat-bolt shadows. Shared neutral shadow is supplied. |
| Bomb/exploder explosion / `impacts` | Imported fire impact used as blast; 800ms effect, quarter-second broad flash and shockwave beyond1× radius compete with hazard geometry. | P0 | New ignition→fire lobes→open curls→embers,340ms, width1.12D. Ground extent never exceeds actual blast boundary. |
| Explosion debris and smoke | No independent low-contrast aftermath; fire asset carries too much of the sequence. | P1 | New smoke/debris strip starts70ms later, alpha≤.38,480ms; keep behind bodies and danger edges. |
| Scorch / `ground` | Reuses a tinted projectile shadow, so blast aftermath reads as a generic oval. | P2 | Irregular authored charred decal, .85D, desaturated dark tint,2.2s fade; decorative only. |
| Sniper firing streak / `hazards::draw` | Full-length procedural line flashes before the physical bolt has travelled the lane, implying simultaneous beam damage. | P0 | Painted4px streak may extend only from muzzle to actual bolt front;110ms decay. Physical projectile remains authoritative. |
| Hostile circular fill / `draw_one` | Correct center-out countdown for ordinary circles; procedural fill and one-pixel rim lack the same authored finish as characters. | P1 | Supplied raster masks mapped onto exact sim shape. Base alpha.12, countdown.34,1.5px rim. |
| Hostile line/cone fill / same | Progress already radiates from source. Width scaling and squash must survive art swap; a decorative slash cannot replace geometry. | P0 | Preserve length/width/angle from HazardView; textured exact mesh; resolve at progress1, no eased timing. |
| BossNova TwoWay fill | Current center-out plus rim-in closes at half-radius, conflicting with this brief's single source-out language. | P0 | Presentation uses radius×progress for nova too. Keep sim timing and damage unchanged. Record this explicit visual override of older TwoWay art direction. |
| Final150ms pulse | Absolute-time sine has arbitrary phase when each hazard enters its final warning. | P1 | One deterministic pulse keyed to remaining time, brightening rim modestly; fill endpoint stays authoritative. |
| Resolve footprint flash / `flashes` | Full red footprint lingers150ms while bright explosion overlays it. | P1 | 80ms alpha.18 maximum; no re-expansion, no replaying warning pulse. |
| Spawn markers / `draw_one` | Layered ellipses and growing band resemble a secondary hazard. | P1 | Warm open-ribbon portal,36×27px, phase-driven; no red. Neutral marker remains non-damaging. |
| Boss energy glow / `actors::draw` | 3 radii×8 copies of colored actor sprite creates 24 ghost draws; sprite RGB multiplication yields muddy orange fragments. | P1 | Two painted flank lobes in one quad behind boss. Alpha follows energy², keeping silhouette uncovered. |
| Full-energy flare / `boss_flashes` | Same soft flash texture as hits,550ms growth, weak distinction from rage. | P1 | Gold energy-lobe flare,220ms; recognizable inward fuel-up gesture, no screen wash. |
| Enrage roar | Generic growing halo has no tear/open/decay shape. | P1 | New crimson broken flame mane,480ms; center transparent, cap112px. Optional2px120ms shake. |
| Sustained enrage aura | Large additive flash sits over actors for the remainder of fight. | P1 | Sparse roar frame2 behind boss, alpha.12–.16, cap96px. No periodic opaque bloom. |
| Enemy KO/fade / `Corpses` | Existing KO persistence and wipe guard are correct; uniform650ms fade has little finish. | P2 | Preserve clip, add one30px dissolve puff after clip; fade body420ms. Boss puff cap42px. |
| Hero Downed | Requires persistent recoverable body; disappearance would mislead resurrect. | P0 | Retain downed pose. Never use enemy dissolve on heroes. |
| Chest drop / `Rewards::draw` |20px sine bounce plus22% scale makes chest jump despite already dropping into scene. | P2 | Retain chest32px; 12px settling arc, one8% squash at landing,350ms. |
| Chest opening/glow | Static glow grows to117px around32px chest; overwhelms local reward source. | P1 |44px authored upward sparkle,600ms. Brief30px floor glow only. |
| Reward banner/buff strip | Existing reward banner is the authorized text surface; attack-speed label is corrected. | P2 | Preserve label, multiplier,1.4s hold+.6s fade and strip. No speed/movement ambiguity. |
| Buff pickup | Receipt is mostly communicated through banner/icon; party-wide application lacks localized feedback. | P2 |22×38px blue/green ribbons on living heroes,600ms,35ms stagger. No moving loot or invented buff mechanics. |
| Resurrect column |160px light pillar is five normal body heights, dominates battlefield. | P1 |28×104px authored column behind bodies, alpha.18–.30; retain authoritative progress. |
| Resurrect progress ring |Up to80 line draws per revive, repeating a procedural outline around the authored ring. | P1 |Gold raster edge in a single textured progress mesh plus base ring;40×30px. |
| Resurrect motes/channel glow |Nine15px sprites plus43×58 halo cover both participants. | P1 |Three18px sparkle fragments behind actors; channel caster gets one18px glint. |
| Resurrect completion/interruption |85×112 burst grows further for750ms; interruption shares similar glow language. | P1 |52×64 upward burst600ms on matched Revived. Interrupted column collapses by opacity over120ms; retained progress persists. |
| Chain Strike II / `wishfire` |Distinct ribbon retained;280ms impact scheduled250ms after hop; sine opacity hides initial attack read. | P0 |Cyan/lavender ribbon repaint180ms; impact begins in same event batch as Hit/ChainHop. No damage delay. |
| Split / `wishfire` |128px slash is four hero heights wide, grows for440ms, plus58px impact on every victim. | P1 |58×39px main crescent, cap80×54 for spread,220ms;24px victim strikes. Keep ivory/orange silhouette. |
| Faze placement/pool |New source separates purple damage and generic impacts correctly. Broad pool and placement image can still cover other cues. | P1 |Repaint purple open-center pool at alpha.22 behind all hostile fills;44px placement burst,26px ticks. Pool footprint follows actual radius. |
| Ward/Elevate |Current one-shot cast pulse honors owner removal of persistent range rings. | P2 |Retain behavior; replace wave-band with neutral portal painted blue/green for300ms. |
| Ward on actor |Procedural protective ellipse resembles a permanent bubble. | P2 |24×35 blue flank shell for200ms on gain; preserve ward bar as lasting indicator. |
| KajaAura / BubblePop legacy kinds |KajaAura hidden footprint is intentional. API retains older kinds although accepted skills changed. | P2 |Do not revive retired range circles. Only render BubblePop if a current event emits it. |
| Scene fade / `main` |Full-screen black rect reads authoritative `stage.fade`; SceneReset cleanup exists. | P2 |Retain exact fade and silent wipe. Delete all new transient records at SceneReset. |

## Art judgment

The largest improvement comes from a clear peak followed by open fragments. Current glow-heavy effects keep similar brightness for too long and let decorative area suggest damage area. The supplied art separates attack families through silhouette, protects silhouettes with draw order, and keeps exact ground geometry as the source of danger information.

All 48 shipped textures have transparent margins. Contact sheet exposes every frame; smaller samples show phone-scale peaks. Runtime timing, draw budgets and final actor visibility remain integration acceptance work. No code, git, Beads, build output or external repository documentation was changed for this delivery.
