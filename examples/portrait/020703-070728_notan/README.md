# 020703-070728: Notan metal art, next steps

Source photo: `../020703-070728.jpg`
Image to cut: **`round5_clean.png`**, planned at **400 mm wide** (the default; no width was given).
Cut file: **`020703-070728.svg`**, traced from it with potrace. The page is 400 × 300 mm; the art inside is about 359 × 291 mm, because the image has a white margin on the left.
Made with the `notan` skill on 2026-10-04 in 5 Gemini rounds. Every prompt is saved as `prompt1–5.txt`.

## Where it stands

| Check | Result | What to do |
| --- | --- | --- |
| Face (eyes, nose, mouth, cheeks) | Fully connected | Nothing |
| Specks | 94 removed | Nothing |
| Loose pieces | **2**: the two black shirt spikes in the bottom-right corner (659 and 109 mm²) | Connect them (step 3) |
| Metal thinner than 1 mm | 1.23 % of the metal, mostly tapered hair tips | Accept it, or thicken the worst tips (step 4) |

`round5_check.png` shows the problems: red = loose piece, blue = too thin.
If you prefer the lighter face of round 1, it would need all the face bridges added by hand, so round 5 is the better starting point.

## 1. Pick the size

400 mm wide makes it about 300 mm tall. To change the size, re-run the check at the new width, because what counts as "too thin" depends on the final size:

```
python3 ~/.claude/skills/notan/notan.py check round5_clean.png --width-mm <W>
python3 ~/.claude/skills/notan/notan.py trace round5_clean.png 020703-070728.svg --width-mm <W>
```

At smaller sizes, more hair tips fall under 1 mm. At 500 mm or more, most of them pass.

## 2. Import the SVG into xTool Studio

1. New project, then import `020703-070728.svg`.
2. Keep it at the size it imports at (art about 359 mm wide). Don't stretch it to 400 mm; the thin-metal check assumed this size.

The SVG is already traced, so xTool Studio's **Trace image** isn't needed. To trace there instead: import `round5_clean.png`, **Trace image**, check that the preview is *closed* outlines, apply, delete the bitmap, and set the width to 400 mm with the aspect ratio locked.

## 3. Connect the two shirt spikes

Choose one:
- **Bottom bar (easiest).** Draw a rectangle along the bottom edge, about 8–10 mm tall, spanning the art, and union it with the vector. The spikes and the shirt already run to that edge, so everything joins, and the bar doubles as a base or hanging rail.
- **Border frame.** A rectangle around the whole piece, 8–10 mm wide, that the hair, shirt and spikes all touch. Union it with the vector. This is what the video did for the grizzly. It's sturdier, and mounting holes can go in the frame.
- **Bridges.** Thin lines (at least 1.5 mm wide) from the top of each spike to the black shirt band above it. This changes the look the least.

## 4. Thin metal (optional)

The blue spots in `round5_check.png` are hair tips that taper to a point. On 20 ga steel they'll burn back slightly and come out a bit shorter. That's cosmetic, not structural. To fix the worst ones, widen them in xTool Studio, or trim them off square.

## 5. Final look for loose pieces

Before cutting, ask: if this were cut out right now, would any black shape fall away? Check zoomed in around the eyes, teeth, ear and every curl. Bridge anything that would.
Optional: import the SVG into Fusion, extrude it 1 mm, and drag the body around. Anything that doesn't move with it is loose.

## 6. Mounting

- Frame option: 2–4 holes, about 5 mm, in the frame corners.
- No frame: holes in solid black areas of the hair, at least 5 mm from any edge. Or skip holes and glue it to a backer board.
- Optional, as in the video: stencil-font text in empty space (a name or date). It must touch the frame or the art.

## 7. Export

If you added a frame or bridges, export the result to this folder as `020703-070728_final.svg`. Keep the `.xs` project file next to it.

## 8. Cut (xTool MetalFab, as in the video)

- 20 ga cold-rolled mild steel. **Degrease it first**, because it ships oiled.
- Material preset: "1 mm carbon steel". 2 mm nozzle, compressed-air assist.
- Clamp the sheet flat and calibrate the height sensor.
- Use the space efficiently; rotate the design if that saves a strip of sheet.
- Process with the lights off to watch it. Small dropped pieces can tip up; check that the nozzle path clears them.

## 9. Finish

1. Knock off dross along the bottom edges with a file or deburring tool.
2. Wipe down with alcohol.
3. Spray paint black in light coats. Black works best on most walls.
4. Optional: mount it on a planed 1×12 pine board, with a recessed adjustable hanger on the back so it's easy to level.

## Files here

| File | What it is |
| --- | --- |
| `020703-070728.svg` | Cut file, traced from `round5_clean.png` |
| `round5_clean.png` | Image the SVG was traced from |
| `round5_check.png` | Problem overlay for round 5 |
| `round1–5.png`, `prompt1–5.txt` | Every round and the prompt that produced it |
| `round*_check.png` | Overlay for each round |
