---
name: reel-production
description: How to plan and produce short vertical explainer reels (9:16, 15–40 s) for any project — choosing the pipeline (code-drawn film in a Motion artifact or HTML renderer, Blender clips, rotoscoped SVG, three.js), the ground rules (real reference for anything that must be true, commercial licences, generative tools kept away from technically exact content, drafts labelled inside the film), the work loop (storyboard → approval gates → contact sheet → independent review → owner), and the lessons from hand and body animation. references/tooling.md compares the tools (HyperFrames, ComfyUI, OneTake, collage B-roll skills, Claude Animation Base, Lemo-Opuscar, Rive, Spine, Remotion, Motion Canvas, three.js, Blender, MediaPipe, MANO-based mocap) with licence and Mac support; references/hands.md covers animating hands and bodies and the capture shot list. Load before making or revising a reel, choosing a video tool, or animating a hand, pose or technique.
license: MIT
compatibility: macOS Apple Silicon or Linux; Blender 4.2+ for 3D clips; Node 22+ for HTML renderers; MediaPipe for pose data
---

# Reel production

A reel is judged in its first second on a phone with the sound off. Everything here serves
that: one idea per screen, a subject that reads at phone size, words inside the safe zone, and
nothing on screen that presents as true what nobody has checked.

Project specifics (brand, palette, voice, review checklist, reviewers, publishing) live in the
project's own reel skill and guide. This skill is the shared method; the project's rules win.

## Ground rules

- **What must be true comes from real reference.** Poses, hand positions, anatomy, sport
  technique, a product's parts and proportions: measured from a photo or video of the real
  thing (landmarks, traced frames, measured dimensions) and named as the source in the review
  report. A shape drawn or generated without reference is a guess, however good it looks.
- **Generative tools are for mood, never for the claim.** Image or video models (ComfyUI,
  Gemini/Wan/LTX video, `image_gen`) may make a B-roll opener, a texture, a concept. They may
  not make the frame that teaches the technique: finger count, joint angles, contact points and
  positions are not guaranteed. A generated reference used as a stand-in is a **draft**, and the
  film says so on screen until real reference replaces it.
- **Label inside the piece.** A caveat in chat does not travel with an exported video. Drafts,
  unreleased features ("segera hadir"/"coming soon") and unreviewed technique carry a visible
  label in the film itself.
- **Commercial licences only.** A reel that promotes a product is commercial use. Check the
  licence of every model, asset, font and sound on its own page before use; "free for research"
  (MANO, SMPL-X, most hand-mocap weights) is not free for us. Record the licence next to the asset.
- **Technique, not someone else's look.** Study how a creator works; never copy their
  characters, visuals, script or assets.
- **Prompts and uploads leave the machine.** No customer data, secrets or unreleased material
  in a prompt to a hosted tool.

## Choosing the pipeline

| Need | Pipeline | Why |
|---|---|---|
| Type, diagrams, UI, icons, data, simple objects | **Code-drawn film**: a claude.ai Motion artifact, or HyperFrames / Remotion / Motion Canvas rendering HTML/canvas to MP4 | Deterministic (every frame a function of time), scrubbable, reviewable from stills, cheap to revise |
| A body part or object that must grip, wrap, occlude or turn in depth | **Blender clip**: rigged CC0 mesh posed from reference data, rendered to transparent PNG frames, placed as a clip in the film | Real occlusion and contact; the film keeps the text, labels and timing |
| Natural 2D hands or bodies without 3D | **Rotoscoped SVG**: 8–12 key poses traced from real video, same path structure in every pose, occlusion drawn in | Shape comes from a real body, so it reads human; stays inside the HTML film |
| Real footage with annotations | Footage + overlay (telestrator style): lines, labels and highlights drawn as code over the clip | The footage is the reference |
| Mood opener, transition, texture | Generative clip (collage B-roll skills, ComfyUI) behind an approval gate | Fine where nothing technical is claimed |

A 2D skeleton or capsule silhouette built straight from landmarks is a **diagnostic**, not a
final look: it has no volume, no occlusion and no contact, and viewers read it as floating.
Details and fixes: `references/hands.md`.

## The loop

1. **Script and storyboard first.** One idea per beat, the hook readable by 2 s, a final card
   held ≥ 3 s, 15–30 s unless the project says otherwise. Name the reference every beat needs.
2. **Capture or collect reference** before drawing (`references/hands.md` has the shot list).
   No reference yet: build what does not depend on it and give the owner the exact shot list.
3. **Approval gates for anything expensive or generative**: idea → one still → full render.
4. **Build, then look.** Render stills offline at each scene's middle and end, the hook at
   ~0.8 s and the last frame; put them on one contact sheet; zoom into contact points and
   joints at full resolution. Fix collisions with the safe zone before style.
5. **Independent review** by agents that did not build it (visual, copy), then the project's
   own gates (for example a coach or a domain expert). A reviewer checks readability; only a
   real-reference check catches a wrong pose.
6. **Owner watches it moving.** Stills cannot show motion problems; say plainly that motion and
   sound were not seen when you only checked stills.

## Motion that does not read as stiff

- The whole subject breathes or drifts slowly; never let joints wobble independently.
- Arrivals ease out with a small overshoot and settle; things enter with intent, not a fade.
- Overlap: parts that move together start a few frames apart (fingers close one after another).
- Change of view is a clean cut on a beat with a short settle; a 2D "flip" that squashes a
  figure to a line reads as broken.
- Interpolate only between two real poses; never invent a pose in between and present it as
  the technique.

## References

- `references/tooling.md`: every tool compared (what it is, licence, cost, Mac support, fit).
- `references/hands.md`: hands and bodies (layering, silhouettes, data cleanup, the capture
  shot list).
- The `codex-delegate` skill for generating images or Blender scripts with Codex; the
  `motion-reel` plugin skill when it is available for a full launch or product reel.
