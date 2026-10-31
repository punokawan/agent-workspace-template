# Reel tooling compared

Checked 2026-10-31 against each tool's own README, LICENSE or pricing page. Marks: ✅ read on the
primary source · ◐ partial or inferred · ❓ not verified. Licences and prices change: re-read the
source page before you depend on one, and record the date you did.

## Renderers: code to video

| Tool | What it is | Licence / cost | Mac Apple Silicon | Use it for |
|---|---|---|---|---|
| **claude.ai Motion artifact** | Animations written as code, scrub, comment on moments, export MP4 | Part of claude.ai ◐ | Browser ✅ | The default for code-drawn reels: films live in the artifact's store; stills render offline with the type's own `render.mjs` |
| **HyperFrames** ([heygen-com/hyperframes](https://github.com/heygen-com/hyperframes)) | HTML/CSS + seekable animation (GSAP, CSS, Lottie, Three.js, Anime.js, WAAPI) rendered frame by frame in headless Chrome + FFmpeg to deterministic MP4; CLI, block catalogue, agent skills (`npx skills add heygen-com/hyperframes`) | Apache-2.0, "no per-render fees or commercial-use thresholds" ✅ | Node 22+, FFmpeg, macOS app ✅ | A local renderer for HTML films when you need an MP4 outside claude.ai, or Three.js scenes. The hosted HeyGen MCP disables compose/render from CLI clients ◐ |
| **Remotion** | Video from React, deterministic per frame; `@remotion/three`, `@remotion/rive`, `@remotion/lottie` | Free for individuals, companies ≤ 3 employees and non-profits, commercial included; otherwise a Company License ✅ | Node ✅ | React-based teams; check headcount before use |
| **Motion Canvas** | Explainer animation in TypeScript | MIT ✅ | Node ✅ | Diagram and code explainers; no character rig |
| **three.js** | 3D in the browser, loads rigged GLB | MIT ✅ | ✅ | A rigged 3D hand or object posed as a function of time inside the film; illustration lines need a custom shader |
| **Claude Animation Base** ([JohnHeibel/ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase)) | p5.js + p5.brush starter kit: storyboard, build per shot, contact-sheet self-check, MP4; vertical 1080×1920 forks exist | MIT ✅ | Node, Chrome, ffmpeg; slow without a GPU when watercolour fill is on ✅ | Borrow the **contact-sheet loop** and "boiling" linework. Its Clawd character is not ours: never use it |
| **Lemo-Opuscar** ([lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar)) | 66 film styles made in code (canvas/WebGL frames, sample music, TTS; no video generation, no stock footage), e.g. Whiteboard Explainer, Isometric Infographic, Sports Telestrator | Code MIT; demo films CC BY 4.0 (credit LemoLab); your own films need no credit ✅ | Node 20+, ffmpeg 7+, Python 3.11+ ✅ (not run here) | Style prompts as a technique library; Sports Telestrator for annotated real footage. Do not copy demo visuals |

## 3D

| Tool | Licence / cost | Mac | Notes |
|---|---|---|---|
| **Blender** | GPL, free; rendered output is yours ◐ | ✅ | Model, rig, animate; EEVEE + Line Art/Freestyle for illustrated lines; transparent PNG sequences become film clips. Runs headless outside Codex's sandbox (`codex.sh blender`) |
| **Human Base Meshes v1.4.1** (Blender Studio, [demo files](https://www.blender.org/download/demo-files/)) | **CC0** ✅, Blender 4.2+ | ✅ | Includes a hand mesh ◐; assume it has no rig ❓ and add finger bones |
| **Rigify** | Part of Blender ◐ | ✅ | Human meta-rig with finger chains |
| **Unreal + MetaHuman** | MetaHuman free under $1M revenue, usable in any software ✅ | ❓ | Heavy for a single hand |
| Cinema 4D | Paid; price not read ❓ | ❓ | Not needed when Blender is installed |

## Pose and motion data

| Tool | Licence | Mac | Notes |
|---|---|---|---|
| **MediaPipe Hand/Pose Landmarker** | Apache-2.0 ✅ (model card ◐) | CPU ✅ | 21 hand landmarks in image and world coordinates; quality drops when fingers are hidden ◐. Needs the model file (`hand_landmarker.task`) |
| **BlendArMocap** ([cgtinker](https://github.com/cgtinker/BlendArMocap)) | GPL-3.0 ✅ | ❓ | **Discontinued**, last release 1.6.1 (July 2023) ✅. Read it for the rotation maths; write a small retarget script instead |
| FreeMoCap | AGPL-3.0 ✅ | ❓ | Multi-camera body mocap; overkill for one hand |
| **HaMeR, WiLoR, Dyn-HaMR, FrankMocap** | All need **MANO** ✅; MANO and SMPL-X licences are **non-commercial research only**, including "production of other artefacts for commercial purposes" ([MANO licence](https://mano.is.tue.mpg.de/license.html)) ✅; WiLoR CC BY-NC-ND, FrankMocap CC BY-NC ✅ | READMEs assume CUDA ✅ | **Not for commercial reels** unless a commercial MANO licence is bought (ps-license@tue.mpg.de) |

## 2D rigs

| Tool | Licence / cost | Mac | Notes |
|---|---|---|---|
| **Rive** | Editor Free (exports carry a splash screen), Cadet $9/seat/month ✅; web runtime MIT ✅ | ◐ | Bones + mesh deformation; runtime can be set to a time ◐ (untested); still needs good source drawings |
| **Spine** | Essential $69 (no mesh), Professional $379; every runtime user needs an editor licence ✅ | ✅ | Mesh only in Professional; licence binds the runtime |
| **Moho Pro 14** | Perpetual; new price not read ❓ | ✅ | Strong 2D rigging for an animator; render to clips |
| Lottie (lottie-web) | MIT ✅ | Web | A player; the animation still comes from After Effects or similar |
| DragonBones | Runtime MIT ✅; editor status ❓ | ❓ | Not recommended |

## Generative and editing services

| Tool | What it is | Licence / cost | Use it for |
|---|---|---|---|
| **ComfyUI** ([Comfy-Org/ComfyUI](https://github.com/Comfy-Org/ComfyUI)) | Node-graph diffusion workflows; DWPose/OpenPose ControlNet for pose; AnimateDiff, Wan 2.2, LTX video models | ComfyUI GPL-3.0 ✅; DWPose, comfyui_controlnet_aux, AnimateDiff, Wan 2.2 Apache-2.0 ✅; ControlNet 1.1 OpenRAIL ◐; LTX-2 community licence, paid at ≥ $10M revenue ✅. Apple Silicon supported ✅, video-model speed on MPS ❓ | Stylising footage or mood clips behind an approval gate. **Not** for frames that teach a technique |
| **Collage B-roll skills** (most likely [gbro-collage-broll](https://github.com/pyang5166/gbro-collage-broll) and its variants VOX-COLLAGE-BROLL, eian-collage-broll, darin-broll-skill; the name is ambiguous ◐) | A ~5 s voiceover line becomes a halftone paper-collage clip; three approval gates (metaphor → still → video) | MIT ✅; generation via Gemini video (`GEMINI_API_KEY`, paid per use) or MaxFusion ✅ | Openers and transitions with no technical claim. Borrow the **three-gate process** |
| **OneTake AI** ([onetake.ai](https://onetake.ai/)) | An "autonomous video editing agent" for raw recordings (courses, podcasts, Shorts), subtitles and dubbing | SaaS, from $10/month billed yearly ✅ | Cutting and subtitling real camera footage. It does not animate |
| **HeyGen HyperFrames MCP** (hosted) | Hosted HyperFrames projects and cloud renders | HeyGen account ◐ | Shareable HeyGen projects; from a CLI agent use the local skills instead |
| Codex `image_gen` | Image generation through Codex CLI | ChatGPT login ✅ | Concept art, textures, sprites, drafts (`codex-delegate` skill); never the technical claim |
