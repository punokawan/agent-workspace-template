---
name: threejs-web
description: When and how to put a three.js (WebGL) scene in a web app, including three.js as an alternative to pre-rendered motion assets (frame sequences, video, GIF, Lottie, Rive) — live glTF animation in the browser or offline rendering to video/frames — plus the decision gate before 3D, vanilla three vs React Three Fiber, client-only loading in Next.js App Router, asset formats and size budgets (glTF/GLB, Draco/Meshopt, KTX2), frame-loop and GPU performance, disposal, reduced motion and accessibility, WebGL fallback and context loss, Core Web Vitals, CSP for decoders, offline tests, and a review checklist. Load before you add, change or review any three.js, R3F or WebGL code in a web repo. For UI motion use animate; for video reels use reel-production or motion-reel.
license: Proprietary
---

# three.js on the web

A 3D scene costs JavaScript, GPU time and battery on every device that opens the page. Add one
only when it earns that cost. These rules are project-agnostic. A project keeps its own facts
(pages that may use 3D, asset host, budgets) in a `<project>-threejs` overlay if it has one.

Read the installed versions before you write code: `three`, `@react-three/fiber` and
`@react-three/drei` change APIs between majors. In Next.js, read the docs bundled in
`node_modules/next/dist/docs/` for `next/dynamic` and client components.

## 1. Decision gate

For a motion asset (an animated mascot, illustration or loop that would otherwise ship as frames,
video, GIF, Lottie or Rive), use the motion-asset gate in section 11 instead.

For any other scene, use three.js only when every answer below is "yes":

1. The effect needs real 3D: a camera, depth, lighting or a model the user turns or moves through.
2. CSS 3D transforms, Motion, Lottie, Rive, an SVG, a short video or a still image cannot give the
   same result. Try the cheapest of those first (`animate`, section 3).
3. The page is not a core task screen. Forms, tables, dashboards and checkout get no 3D.
4. The scene has a static fallback that carries the same meaning.

If one answer is "no", do not add three.js. Write down which alternative you used.

## 2. Stack

| Situation | Use |
|---|---|
| React or Next.js app | React Three Fiber (`@react-three/fiber`) with only the `@react-three/drei` helpers you use |
| Plain page, a single effect, no React | `three` directly, as ES modules |
| A background shader with no scene graph | A plain `<canvas>` with a fragment shader, or a lighter WebGL library; measure before you add three |

- Import named modules: `import { Mesh, BoxGeometry } from 'three'`. Never `import * as THREE`
  in app code; it defeats tree shaking.
- Import loaders and controls from their own paths (`three/examples/jsm/...` or
  `three/addons/...`, whichever the installed version exports). Add each one only when used.
- Measure the bundle after the change (the framework's bundle analyzer or build output). State
  the added size for the route in the PR.

## 3. Loading in Next.js App Router

1. Put the scene in a client component (`'use client'`).
2. Load that component with `next/dynamic` and `{ ssr: false }` from another client component.
   The server never imports `three`.
3. Start loading only when the canvas area is near the viewport (IntersectionObserver), or on a
   user action. Do not load 3D for content below the fold on first paint.
4. Reserve the exact box of the canvas with a poster image of the first frame. The page layout
   must not shift when the scene arrives (CLS).
5. Show the poster while the scene loads and when it fails. The poster is the fallback in
   section 7.
6. Never make the canvas the largest element in the first viewport. LCP must be text or the
   poster image.

## 4. Assets

- **Models:** glTF binary (`.glb`). Compress geometry with Draco or Meshopt. Remove unused
  nodes, animations and materials before export.
- **Textures:** KTX2 (Basis) where the loader is available; otherwise WebP or JPEG at the
  smallest size that holds at the canvas size × device pixel ratio 2. Power-of-two sizes.
- **Budget per scene, first load:** state it in the PR. Default: at most 1 MB compressed for
  models and textures together, unless the project overlay sets another value.
- **Hosting:** serve from the CDN or object storage with long cache headers and a content hash in
  the file name. Do not put large assets in the repo; follow the project's asset rules.
- **Decoders:** Draco, Meshopt and KTX2 decoders are separate files (JS or WASM). Host them
  yourself, same origin, and load them only when a model needs them.

## 5. Performance

- **Pixel ratio:** clamp to at most 2 (`dpr={[1, 2]}` in R3F, `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))` in three).
- **Frame loop:** if the scene is still until the user acts, render on demand
  (`frameloop="demand"` in R3F, or render only on change). Never run a 60 fps loop for a static
  image.
- **Pause** the loop when the canvas leaves the viewport and when the tab is hidden
  (`visibilitychange`).
- **Draw calls:** share geometries and materials. Use instancing for repeated objects. Merge
  static meshes.
- **No allocations per frame:** create vectors, matrices and colors once, outside the render
  loop. Do not set React state per frame; mutate refs in `useFrame`.
- **Expensive features are opt-in:** shadows, post-processing, antialias on high-DPR screens,
  transparency sorting, real-time reflections. Add each one only with a measured reason.
- **Dispose** geometries, materials, textures and render targets when the scene unmounts. R3F
  disposes what it created; dispose what you created by hand.
- **Measure** on a low-end phone profile (CPU 4× slowdown in DevTools) and give the frame time.

## 6. Motion and accessibility

- If `prefers-reduced-motion: reduce` is set, show a still frame or the poster. No auto-rotation,
  no camera moves, no parallax.
- A decorative canvas gets `aria-hidden="true"` and no focus.
- Information in the scene must also exist in the DOM as text: product names, numbers, labels.
- An interactive scene needs a keyboard path and visible focus for every action, or a DOM
  control that does the same thing.
- Text drawn over the canvas meets contrast against every frame, not only the first one.

## 7. Fallback and failure

- Check for WebGL before you create the renderer. If it is missing, keep the poster.
- Listen for `webglcontextlost`. On loss, stop the loop and show the poster. Restore only on
  `webglcontextrestored`.
- A loader error shows the poster and logs once. It never throws into the page.
- Data saver (`navigator.connection.saveData`) and low memory: keep the poster and offer a
  "show 3D" button.

## 8. Security

- Load models and textures only from your own origin or storage. Never load a model from a URL a
  user supplies.
- A model a user uploads is untrusted: validate size and format on the server, and render it in
  a scene that has no access to secrets.
- Decoders that use WASM or workers can need Content Security Policy changes, for example
  `worker-src blob:` or `script-src 'wasm-unsafe-eval'`. Check the decoder's docs and the
  project's CSP, and add only what the decoder needs, on the routes that use it.

## 9. Tests

- Unit tests run in jsdom, which has no WebGL. Mock the scene component and test the parts
  around it: the poster, the reduced-motion branch, the WebGL-missing branch and the loader-error
  branch.
- Keep scene math (camera paths, layout of objects) in plain functions and unit test them.
- Check the real scene in a browser: a screenshot at the default viewport, a reduced-motion
  screenshot, and the frame time from a performance trace. Follow the project's visual QA rules.

## 10. Review checklist

- [ ] The decision gate (section 1) is answered in the PR, with the alternative that was rejected.
- [ ] `three` is loaded client-only, lazily, on the routes that need it.
- [ ] A poster reserves the box; no layout shift; LCP is not the canvas.
- [ ] The added bundle size and the asset size are stated and within budget.
- [ ] DPR is clamped; the loop pauses offscreen and on hidden tabs; static scenes render on demand.
- [ ] Nothing allocates or sets React state per frame.
- [ ] Hand-made GPU resources are disposed on unmount.
- [ ] Reduced motion, WebGL missing, context loss and loader errors all show the poster.
- [ ] Scene information also exists as DOM text; interactive parts work by keyboard.
- [ ] Assets and decoders come from your own origin; CSP changes are minimal and route-scoped.
- [ ] Tests cover the fallback branches; a browser check covers the real scene.

## 11. three.js as a motion-asset alternative

A motion asset is an animation the product ships as a file: a mascot loop, an illustrated
reaction, an onboarding animation, a hero loop. The usual formats are a frame sequence or sprite
sheet, a video (WebM/MP4), a GIF, Lottie or Rive. three.js gives two alternatives.

### Two modes

| Mode | What ships | Use when |
|---|---|---|
| **Live** | One `.glb` with its animation clips, played in the browser by `AnimationMixer` | The asset has several states or loops that share one character, must react to the user (look at the pointer, change state on an event), or must render sharp at any size |
| **Offline** | Video or frames rendered from the same three.js scene at build time | The asset is fixed, plays on a core task screen, or must also run where WebGL is off; three.js is only the production tool |

### Motion-asset gate

Choose three.js (either mode) only when at least one is true:

1. **Size:** the frame sequences or videos for all states together are larger than the model plus
   the three.js chunk. Measure both before you decide. Example to measure: 6 states × 48 frames ×
   WebP, against one Draco-compressed `.glb` plus about 150 KB of gzipped `three` (read the real
   number from the build).
2. **States:** the asset needs more than about 3 states or transitions between them. Pre-rendered
   formats need one file per state and per transition; a model blends clips (`crossFadeTo`).
3. **Interaction:** the asset reacts to input (pointer, scroll, an app event) in a way a fixed
   file cannot.
4. **Consistency:** a character must look the same across many assets, and one rigged model keeps
   them consistent better than separate drawings.

If none is true, keep the existing format: video for a fixed loop, Lottie or Rive for flat vector
motion, a sprite sheet for a short UI animation.

### Live mode rules

- The model comes from the existing pipeline: Blender (or another DCC tool) → glTF with named
  animation clips (`idle`, `wave`, `celebrate`). Name clips in lowercase kebab-case and keep the
  names stable; code selects clips by name.
- One `AnimationMixer` per character. Switch states with `crossFadeTo` (200–400 ms). Do not
  restart a clip from frame 0 for every event.
- Keep the poster (the still asset that exists today) as the fallback and as the
  reduced-motion frame. The rules in sections 3, 6 and 7 apply unchanged.
- Render on demand when the character is idle and still. If the idle loop moves, cap the frame
  rate with the scene's needs (a mascot idle loop needs no more than 30 fps) and pause offscreen.
- Lighting and materials must match the 2D art direction of the product. Use flat or toon
  materials and a fixed camera for a mascot. A realistic PBR look next to flat UI is an art
  direction change: get the owner's approval first.
- Budget: state the model size, the clip count and the frame time on the low-end profile in the PR.

### Offline mode rules

- Render from the same scene and the same clips the live mode would use, so both modes stay one
  source.
- Render deterministically: a fixed frame rate, a seeded random, time taken from the frame
  number (not the wall clock). Capture frames with a headless browser, or render the scene in
  Remotion with `@remotion/three`. See `reel-production` (`references/tooling.md`) for the video
  tools and their licences.
- Export what the product already plays: WebM (VP9 or AV1) with an MP4 fallback for video, WebP
  frames or a sprite sheet for short UI loops. Keep transparency only if the format and the
  target browsers support it; test Safari.
- Large outputs (frame sequences, masters) follow the project's asset-export rules. Commit only
  the final web assets and the small metadata the build needs.

### Where the model comes from

- Ask for a rigged model from the designer, or build it with the `codex-delegate` skill (model
  mode: Blender `bpy`, exported as `.glb`). Review it in a viewer before you write code.
- Never invent a pose or a hand shape. Take poses from a real reference (photo or video), the
  same rule as `reel-production`.
