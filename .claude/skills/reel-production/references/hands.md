# Hands and bodies that read as human

Learned the hard way: a hand drawn from invented coordinates was rejected by the owner at a
glance ("not how a normal human hand sits"), and two agent reviews missed it because they
checked readability, not anatomy. A hand built from AI-generated reference photos then read as
stiff and "not gripping". The fixes below are what changed that.

## Why a landmark skeleton looks wrong

| Symptom | Cause | Fix |
|---|---|---|
| The hand floats instead of gripping | No occlusion and no contact: every part drawn in front of the object | Per pose, decide what sits in front of the object and what behind it, from the reference photo (palm side of a grip: palm behind the handle, fingers wrapped in front; back of the hand: knuckles on top, fingers underneath; thumb side: thumb and index in front, the rest behind). Draw the object between the two layers |
| Joints show as seams | Each segment's outline painted over its neighbour's fill | Draw the whole silhouette as one shape: every outline first, then every fill, palm and arm included |
| Shape looks like sausages | Uniform capsule widths, oversized forearm | Taper fingers toward the tips, thicker thumb, slimmer forearm narrowing at the wrist; keep the skeleton as a thin layer over the silhouette, not the main read |
| Jittery or robotic motion | Raw landmarks, every joint drifting on its own noise | Smooth the data (One-Euro or Savitzky–Golay), clamp to anatomical joint ranges; idle motion moves the whole hand together |
| Fingers "melt" between poses | Linear interpolation between distant poses | Keep key poses close together; close fingers one by one with overlap and a small settle; interpolate only between real poses |
| Fingers wrong where the object hides them | MediaPipe guesses occluded joints | Use data for the open-hand phase; match the closed phase to close-up photos by eye, and say so in the report |

A 2D landmark skeleton is a diagnostic. For a final look, use a rotoscoped SVG (shape from the
real hand) or a rigged 3D mesh with real occlusion (see `tooling.md`).

## Flat illustrated hands that read as human

Studied from a motion-design reference an owner shared (a hand built in shape layers, shown in
both its construction view and its final frame). Copy the method, never the drawing:

- **Build from simple overlapping shapes**: a large circle at the base of the thumb and at the
  wrist, an ellipse for the palm, tapered capsules per finger segment with a circle at each joint.
  The masses give the palm its volume, which a polygon between knuckles never does.
- **Merge them into one flat silhouette**: every shape the same fill, no stroke, so the overlaps
  disappear. No outline around the hand.
- **Depth by tone, not lines**: parts behind the object are a dimmer tone of the same colour; a
  single darker shape under the thumb gives contact. Status (wrong/right) can tint the whole hand,
  always alongside the tick or cross and its word.
- **Lines only where they mean something**: a thin crease where one finger overlaps another or the
  palm, coloured close to the background so it disappears against it; nail or knuckle marks only
  when the view shows them.
- **A landmark skeleton, if the style keeps one, is a faint thin overlay**, never the main read.

### A hand holding an object

From flat-illustration references of a hand holding a phone and a hand pointing at a screen:

- **Let the object do the occluding.** The palm sits behind the object; the thumb lies in front
  on one side; of the wrapping fingers only the tips show, as stacked rounded lozenges coming
  round the object's far edge. The grip reads because the occlusion is right, not because of
  detail.
- **Simplify hard**: one flat skin tone, each finger a single soft tapered shape, no knuckle
  segments, generous rounding, few vertices.
- **Separate fingers with almost nothing**: a thin slightly lighter rim, or one darker tone on the
  side of a bent finger; nail marks as a short thin arc only when the nail faces the camera.
- **Getting there from real footage**: trace the silhouette from the video (rotoscope), then
  simplify the traced contour (fewer points, rounder corners) until it reads like an illustration.
  The shape stays true to the real hand; only the detail goes.
- **Separate touching fingers with the photo's own creases**: a black-hat filter (closing minus
  image, kernel a little wider than the gap) finds the thin dark valleys between fingers; keep the
  long thin ones, turn each into a smooth centre-line (mean offset along its main axis) and draw it
  as a thin rounded stroke one tone darker than the skin. A single flat fill otherwise merges a
  stacked grip into one blob.
- **Nails show which way a finger faces**: a lighter, slightly elongated shape on the end segment,
  with a thin arc at the free edge, only where the back of that finger faces the camera.
  **Trace them from the photo or video, not from landmark maths.** An audit against the reference
  photos found both shortcuts wrong: a facing test from MediaPipe world landmarks (depth is too noisy:
  it hid a clearly visible thumbnail and put another on the wrong side of the thumb) and an automatic
  "lighter patch near the fingertip" detector (it took fingertip pads for nails and missed real ones).
  For each pose, zoom into every fingertip on a coordinate grid, read the nail's centre, size and the
  direction of its free edge, and record them as matched by eye. Draw nothing where you cannot tell.
  Audit by mapping the drawn nails back onto the source frame.

## Data cleanup

- Store landmarks with their `source` (who was filmed, when) and licence; refuse data without it.
- World landmarks are metres but their absolute scale is unstable: scale the model uniformly
  from one stable length (wrist to middle knuckle) and compare ratios, not millimetres.
- Several hands in frame: pick the one you want explicitly (largest, leftmost, rightmost); the
  left/right label assumes a mirrored image and is not reliable for choosing.
- A hand the detector misses in the full frame may be found on a crop around it.
- Map image landmarks into the object's own frame (for a racket: the handle axis from the grip
  top to the butt) by rotation and uniform scale only. Never mirror, or a right hand becomes a left.

## Capture shot list (ask the owner for this)

| Item | Request |
|---|---|
| Camera | Phone on a tripod or propped, not hand-held. 1080p minimum, 4K if possible, **60 fps**. Lock focus and exposure |
| Light | Soft and even: a window without direct sun, or two lights left and right. No hard shadows, no backlight |
| Background and clothing | Plain background contrasting with skin. Sleeves rolled to the elbow, no rings or watch |
| Angles | Recorded separately: the main side (for a grip: the palm side), the second side (the thumb side), and end-on (along the object's axis). Bonus: one slow orbit around the final pose |
| Movement | The script's steps, **slowly**, holding each pose 2 s. Add the wrong version as its own clip |
| Takes | 10–20 s per angle, 3 takes each |
| Stills | 6–8 close-up photos of each final pose, for the hidden-finger phase |
| Measurements | Real dimensions of the object (for a handle: circumference and size code) |
| Who | Ideally the expert (coach, doctor, mechanic): the footage then doubles as the technique check |
