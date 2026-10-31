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
