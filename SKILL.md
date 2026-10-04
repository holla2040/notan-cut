---
name: notan
description: Turn a photo into Notan-style (two-tone black/white) art that can be cut from one sheet of metal with a fiber laser, then prepped in xTool Studio. Use when the user hands over a photo and says /notan, "make this cuttable", "turn this into metal wall art", "Notan this", or "convert this photo for the MetalFab".
---

# Notan: photo to cuttable metal art

Method from NeedItMakeIt, "Converting any photo into Artwork and making it with the xTool MetalFab" (https://youtu.be/OXh7r_nBAEA).
Notan is the Japanese style built only from flat black and white shapes. The word "Notan" in the prompt is what makes the image model produce something cuttable. Without it, "stencil", "black and white" and "laser cut" prompts all fail.

Black = metal that stays. White = cut away. Every black area must connect to one main piece, or it falls out.

## Inputs

- **Photo** (required).
- **Finished width in mm.** If not given, use 400 mm and say so. The thin-line check depends on it.
- **Minimum metal width in mm.** Default 1.0, which suits 20 ga (~0.9 mm) mild steel. Use the sheet thickness for thicker stock.
- **Use.** Default is fiber-laser metal art. For 3D-print inlays, ask for much less detail and use `--min-mm 0.8`.

## Tools

`<skill-dir>/notan.py`. On Windows use `python`; on Linux use `python3`.

| Command | Does |
| --- | --- |
| `notan.py gen PHOTO OUT.png --prompt-file P.txt [--ref PREV.png] [--size 2K]` | One Nano Banana Pro call (`gemini-3-pro-image`). Each call is stateless, so it acts like a new chat. |
| `notan.py check IMG.png --width-mm W [--min-mm M] [--fix]` | JSON report on islands (pieces that fall out) and metal that is too thin. Writes `IMG_check.png`: red = island, blue = too thin. `--fix` writes `IMG_clean.png` with specks under 4 mm² turned white. |
| `notan.py trace IMG.png OUT.svg --width-mm W` | potrace fallback, only when xTool Studio can't be driven |
| `notan.py selftest` | Checks that the island and thin-line detection works |

Each `gen` call is a paid image generation. Limit it to **5 rounds** per photo unless the user says otherwise.

## Procedure

Work in a job folder next to the photo, `<photo-stem>_notan/`. For each round, save `promptN.txt` and `roundN.png` there, so the user can see every prompt that was sent.

### 0. Look at the photo first

Open it and look at it yourself.
- **Blurry, or short side under ~1000 px:** run one `gen` with `Upscale this image, keep it photographic and identical in content.` Use that output as the photo from then on.
- **Flat lighting on a hard-surface subject** (car, machine): optionally run one `gen` that adds more dramatic lighting, reflections and shadows, or a better view angle. Ask the user first, because it changes the picture. Reflections give cars structure; on animals, fur highlights do the same job.
- **Busy background:** that's fine. The prompt tells the model to ignore it.
- **Portraits:** expect the eyes, nose, mouth and cheek lines to float free inside an open white face. Name those bridges by round 2.

### 1. Round 1: the base prompt

Copy this template into `prompt1.txt`. Replace `<subject>`, list the subject's real parts, and name its detail cue (fur highlights, reflections, folds).

```
Convert this image into Notan style to be suitable to cut using a fiber laser from a sheet of metal, avoid lines which are too thin for the laser to cut.  Add as much detail as possible while considering the structure of the finished metal wall art.  Use the highlights in the image as a reference for where to have the added detail; the <subject>'s <part>, <part> and <part> all need to have as much detail as possible to resemble the original image well.  The <most important part> can have the most detail.  Ignore the background in the image.  The resulting image needs to be 2 dimensional without shadows, solid black on a plain white background.  Make sure all areas have enough connection between dark areas so there are no tiny sections wanting to fall away from the rest.  Remove extremely small sections of black and either combine them with other sections, or replace them with white.
```

Then run `notan.py gen photo.jpg <job>/round1.png --prompt-file <job>/prompt1.txt`.

### 2. Judge every round two ways

1. **Look at the image yourself.** Does it read as *this* subject (face, markings, proportions)? Is the background gone? Is it pure black and white, with no grey and no outlines-only drawing? Is the subject black on white? If it is inverted, say "black subject on white background" next round.
2. **Run `notan.py check roundN.png --width-mm W --min-mm M`**, then open `roundN_check.png`.
   - `islands`: whatever isn't a speck must be fixed. Find the red areas in the overlay and name them in the next prompt (e.g. "the left eye is a separate piece; connect it to the head").
   - `thin_pct_of_metal` over 0.5 %: blue areas will burn away or warp. Ask for thicker shapes there.
   - Specks alone are fine. `--fix` removes them.

### 3. Refine (rounds 2–5)

Send the original photo again every round, and pass the best result so far as `--ref`. The model doesn't hold onto images reliably, and the video says re-attaching the original is essential. Each new prompt is the **whole previous prompt plus correction sentences**, so you never send only a delta. Change one or two things per round.

Correction sentences, by problem:

| Problem | Add |
| --- | --- |
| Too blocky, looks like a stencil | `Add more detail than the previous generation, using the highlights as the guide.` |
| Too busy, too many fragments | `Slightly, and I mean slightly, reduce the detail from the previous image; it should be a level right in the middle of the previous two images.` (pass both earlier rounds as `--ref`) |
| Named piece is an island | `The <part> is a separate piece; connect it to the <neighbour> with a solid black bridge.` |
| Thin lines in an area | `Lines in the <area> are too thin to cut; make them at least twice as thick.` |
| Background or floor showing | `Ignore the <floor/background> completely; nothing but the <subject> should be black.` |
| Missing a feature | `The <feet> should also include <small claws>.` |
| Grey, gradients or shadows | `Use only pure black and pure white, no grey, no shading, no shadows.` |

**When only a few islands are left, edit the result directly.** Pass the best round itself as the photo (`gen roundN.png roundN+1.png`, no `--ref`). Write a short prompt that starts with "This is Notan style black and white art that will be cut from metal… Make only these changes and keep everything else exactly as it is:", then number each bridge and say where it goes, using "left/right side of the image" and never the subject's own left or right. Don't re-send the photo with `--ref` and "keep it the same": the model copies the reference and ignores the fixes (boys example, round 3). Each direct edit can break a joint somewhere else, so check every round.

**Stop** once the check shows no islands except specks, thin metal is under 0.5 %, and it clearly looks like the subject. Then run `check --fix` and continue with `roundN_clean.png`.
**After 5 rounds without passing:** stop, show the user the best round and its overlay, and say which islands remain. They can be bridged by hand in xTool Studio with very thin lines, as in the video.

### 4. xTool Studio

xTool Studio has no command line. If you can control the desktop (computer use), do these steps yourself. If not, stop here and give the user this list with the real file name and width filled in:

1. New project, then import `roundN_clean.png`.
2. Select the image, then **Trace image**. Check that the preview is a single *closed* outline set (closed paths are what make it cuttable), then apply.
3. Delete the bitmap, keeping only the vector. Set the vector's width to **W mm** with the aspect ratio locked.
4. Optional (ask the user): add a border frame touching the art so everything connects, mounting holes, or stencil-font text in empty space.
5. Look for loose pieces one last time. Bridge any you find with very thin lines in places where they barely change the look (text and wheel rims needed this in the video).
6. Export SVG to the job folder as `<photo-stem>.svg`.
7. MetalFab settings used in the video for 20 ga cold-rolled steel: material preset "1 mm carbon steel", 2 mm nozzle, compressed-air assist, calibrate the height sensor, then process. Degrease oiled steel first.

Fallback when xTool Studio can't be used: `notan.py trace roundN_clean.png <job>/<stem>.svg --width-mm W`. This needs potrace on PATH.

### 5. Write the job README, then report

Write `<job>/README.md` with the next steps for this piece. Model it on `<skill-dir>/examples/boys/020703-070728_notan/README.md`, which is a real run (the boys portrait): same sections, same order, same level of detail, but every fact comes from **this** run. That means:
- the photo name, image to cut, width, date, rounds used
- a status table built from the last `check` (loose pieces named by where they are, specks removed, thin %)
- the island fixes that fit *these* islands (drop that section if there are none)
- the thin-metal note (drop it if under 0.5 %)
- the subject-specific places to look in the final pass
- mounting suggestions in this design's solid areas, and the export name `<stem>.svg`

Keep the xTool Studio, cut and finish steps. If the user gave a material other than 20 ga steel, adjust them.

Then reply in a few lines: the rounds used, the final image path, loose pieces left, thin %, and the README path.

## Setup (once per machine)

- `pip install opencv-python numpy pillow`
- Gemini API key in `GEMINI_API_KEY`. On Windows: `setx GEMINI_API_KEY "..."`, then restart the terminal.
- xTool Studio installed.
- Optional: potrace (Windows build from potrace.sourceforge.net, on PATH), for the fallback trace only.
- Check: `python notan.py selftest` prints `selftest ok`.
