# jesse: Notan metal art, next steps

Source photo: `jesse.jpg` (moved into this folder when the run finished)
Image to cut: **`round2_clean.png`**, planned at **400 mm wide** (the default; no width was given).
Cut file: **`jesse.svg`**, traced from it with potrace. The page is 400 × 300 mm; the art inside is about 317 × 275 mm, because the image has a white margin on the right and at the top.
Made with the `notan` skill on 2026-10-04 in 2 Gemini rounds. Every prompt is saved as `prompt1–2.txt`.

## Where it stands

| Check | Result | What to do |
| --- | --- | --- |
| Face (eyes, blaze, nose, muzzle) | Fully connected | Nothing |
| Specks | 35 removed | Nothing |
| Loose pieces | **0** | Nothing |
| Metal thinner than 1 mm | 1.07 % of the metal, mostly pointed fur tips | Accept it, or thicken the worst tips (step 3) |

`round2_clean_check.png` shows what's left: blue = too thin. There's no red, so nothing falls out.
Round 1 had two loose pieces (a fur stroke at the bottom edge and a whisker stroke in the muzzle). Round 2 bridged both and thickened the fur tips, without changing anything else.

## 1. Pick the size

400 mm wide makes it about 300 mm tall. To change the size, re-run the check and the trace at the new width, because what counts as "too thin" depends on the final size:

```
python3 ~/.claude/skills/notan/notan.py check round2_clean.png --width-mm <W>
python3 ~/.claude/skills/notan/notan.py trace round2_clean.png jesse.svg --width-mm <W>
```

At smaller sizes, more fur tips fall under 1 mm. At 500 mm or more, most of them pass.

## 2. Import the SVG into xTool Studio

1. New project, then import `jesse.svg`.
2. Keep it at the size it imports at (art about 317 mm wide). Don't stretch it to 400 mm; the thin-metal check assumed this size.

The SVG is already traced, so xTool Studio's **Trace image** isn't needed. To trace there instead: import `round2_clean.png`, **Trace image**, check that the preview is *closed* outlines, apply, delete the bitmap, and set the width to 400 mm with the aspect ratio locked.

## 3. Thin metal (optional)

The blue spots in `round2_clean_check.png` are fur tips that taper to a point, around the ears, the head outline and the chest ruff. On 20 ga steel they'll burn back slightly and come out a bit shorter. That's cosmetic, not structural. To fix the worst ones, widen them in xTool Studio, or trim them off square.

## 4. Final look for loose pieces

Before cutting, ask: if this were cut out right now, would any black shape fall away? Check zoomed in around the eyes (the pupils and the rims around them), the nose, the whisker strokes beside the muzzle, and the fur strokes in the white chest ruff. Bridge anything that would.
Optional: import the SVG into Fusion, extrude it 1 mm, and drag the body around. Anything that doesn't move with it is loose.

## 5. Mounting

- The dog runs off the left and bottom edges, so those edges are cut straight. A **bottom bar** (a rectangle 8–10 mm tall along the bottom edge, unioned with the vector) makes a sturdy base and hanging rail.
- No bar: holes in the solid black areas, at least 5 mm from any edge. Good spots: the big black cheek on the left side of the image, the black ear on the right, and the black body in the bottom-left corner. Or skip holes and glue it to a backer board.
- Optional, as in the video: stencil-font text in the empty space on the right ("Jesse"). It must touch the art or the bar.

## 6. Export

If you added a bar, holes or bridges, export the result to this folder as `jesse_final.svg`. Keep the `.xs` project file next to it.

## 7. Cut (xTool MetalFab, as in the video)

- 20 ga cold-rolled mild steel. **Degrease it first**, because it ships oiled.
- Material preset: "1 mm carbon steel". 2 mm nozzle, compressed-air assist.
- Clamp the sheet flat and calibrate the height sensor.
- Use the space efficiently; rotate the design if that saves a strip of sheet.
- Process with the lights off to watch it. Small dropped pieces can tip up; check that the nozzle path clears them.

## 8. Finish

1. Knock off dross along the bottom edges with a file or deburring tool.
2. Wipe down with alcohol.
3. Spray paint black in light coats. Black works best on most walls.
4. Optional: mount it on a planed 1×12 pine board, with a recessed adjustable hanger on the back so it's easy to level.

## Files here

| File | What it is |
| --- | --- |
| `jesse.jpg` | Original photo |
| `jesse.svg` | Cut file, traced from `round2_clean.png` |
| `round2_clean.png` | Image the SVG was traced from |
| `round2_clean_check.png` | Overlay for the final image (blue = too thin) |
| `round1–2.png`, `prompt1–2.txt` | Every round and the prompt that produced it |
| `round*_check.png` | Overlay for each round |
