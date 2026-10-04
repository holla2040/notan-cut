# Manual guide: photo to Notan metal art with a free chat AI

No Python, no Claude Code, no API keys. Just a chat AI that can make images, a free paint program, and your laser software.

This is [NeedItMakeIt](https://www.youtube.com/@NeedItMakeIt)'s method from his video
["Converting any photo into Artwork and making it with the xTool MetalFab"](https://www.youtube.com/watch?v=OXh7r_nBAEA).
**Watch it first.** Seeing him judge and steer each round teaches more than any written guide. If it helps you, support him on [Patreon](https://www.patreon.com/Needitmakeit).

The rules that never change:
- **Black = metal that stays. White = cut away.**
- **Every black shape must connect to one main piece,** or it falls out of the sheet when it's cut.

## 1. Pick a chat AI

You need one that can **edit an image you upload**. Free tiers and their daily limits change often, so check what yours allows today.

| Chat AI | Notes |
| --- | --- |
| **Google Gemini** | What the video used, and what worked best. His results only came together after Gemini's "Nano Banana" image model came out. |
| **ChatGPT** | Can make images. He tried ChatGPT first and had much less luck with it, but it's worth a try if it's what you have. |
| **Grok** | Can make images. Untested here, so judge the results the same way. |
| **Claude** | Can't produce images, so it can't make the art. It can still help: paste in your prompt and a description of what's wrong, and ask it to write the correction sentences. |

Most of these need you to sign in before they make images. If you already have a Google account, Gemini needs nothing new.

## 2. Get the photo ready

- **Sharper is better.** If the photo is blurry or small (under about 1000 pixels on the short side), first ask the AI: `Upscale this image, keep it photographic and identical in content.` Download the result and use it from then on.
- **Strong light and contrast help.** Highlights are what the AI turns into detail. On cars and machines, reflections are your friend. On animals, the highlights in the fur do the same job.
- **A busy background is fine.** The prompt tells the AI to ignore it.

## 3. Round 1: the base prompt

**Start a new chat.** Attach your photo and paste the prompt below. Fill in the `<...>` parts with your subject's real parts and the part that matters most.

```
Convert this image into Notan style to be suitable to cut using a fiber laser from a sheet of metal, avoid lines which are too thin for the laser to cut.  Add as much detail as possible while considering the structure of the finished metal wall art.  Use the highlights in the image as a reference for where to have the added detail; the <subject>'s <part>, <part> and <part> all need to have as much detail as possible to resemble the original image well.  The <most important part> can have the most detail.  Ignore the background in the image.  The resulting image needs to be 2 dimensional without shadows, solid black on a plain white background.  Make sure all areas have enough connection between dark areas so there are no tiny sections wanting to fall away from the rest.  Remove extremely small sections of black and either combine them with other sections, or replace them with white.
```

Example of a filled-in middle, for a portrait:
`...especially the highlights in the curls of the hair; the boy's curly hair, eyes, eyebrows, nose, smile, ear and shirt collar all need to have as much detail as possible to resemble the original image well.  The face, especially the eyes and the smile, can have the most detail...`

**Why the word "Notan" matters:** he tried "stencil," "make this laser cuttable" and "convert to black and white," and none of them worked. *Notan* is a Japanese art style built from flat light and dark shapes, and naming it is what gets you something cuttable that still looks like the photo.

Download the result at full size. Keep every round; you may want to go back to one.

## 4. Judge the result

Look at it and ask:
- Does it clearly look like *this* subject (face, markings, proportions)?
- Is the background gone?
- Is it pure black and white, with no grey, no shading and no outline-only drawing?
- Is the subject black on white? If it came out inverted, add `black subject on a white background` next round.
- **Would anything fall out?** Look for black shapes that don't touch the rest: eyes, nostrils, teeth and cheek lines inside an open white face are the usual ones. Step 7 has a reliable way to check this.
- Are any lines hair-thin? They'll burn away in metal.

## 5. Rounds 2–5: refine

The two tips from the video that matter most:

1. **Start a new chat every round.** If you keep going in the same chat, the AI leans on its previous image and stops listening.
2. **Attach the original photo every time,** plus the best result so far. The AI doesn't remember images well.

In the new chat, attach the original photo and your best result. Paste the **whole** previous prompt, then add one or two correction sentences at the end. Change one or two things per round, not everything at once.

| Problem | Add this |
| --- | --- |
| Too blocky, looks like a stencil | `Add more detail than the previous generation, using the highlights as the guide.` |
| Too busy, too many fragments | `Slightly, and I mean slightly, reduce the detail from the previous image; it should be a level right in the middle of the previous two images.` (attach both earlier rounds) |
| A piece would fall out | `The <part> is a separate piece; connect it to the <neighbour> with a solid black bridge.` |
| Lines too thin in one area | `Lines in the <area> are too thin to cut; make them at least twice as thick.` |
| Background or floor showing | `Ignore the <floor/background> completely; nothing but the <subject> should be black.` |
| A feature is missing | `The <feet> should also include <small claws>.` |
| Grey, gradients or shadows | `Use only pure black and pure white, no grey, no shading, no shadows.` |

**Say "left side of the image" and "right side of the image,"** never the subject's own left or right. The AI mixes those up.

Stop when it looks like the subject and nothing would fall out. Five rounds is usually enough. Past that, fix the rest by hand (step 8).

## 6. The last few loose pieces: edit the result directly

When it's close and only a few pieces float free, change approach. Start a new chat, attach **only your best result** (not the photo), and number each fix:

```
This is Notan style black and white art that will be cut from a sheet of metal with a fiber laser, so every black shape must be physically connected to the rest.  Make only these changes and keep everything else exactly as it is:  1. <The eyebrow and eye on the left side of the image float free inside the white face.  Join the left end of that eyebrow to the black hair next to it with a solid black bridge as thick as the eyebrow.>  2. <...>  Keep pure black and pure white only.
```

Don't attach the original photo and say "keep it the same, but fix X." The AI copies the reference and ignores the fixes.
Each edit can break a joint somewhere else, so check every round again.

## 7. Check it yourself: the paint-bucket test

This is the manual version of the `check` command in this repo. It takes two minutes and finds every loose piece.

1. Open the image in a paint program. **[Photopea](https://www.photopea.com)** runs in the browser with no account; Windows Paint, GIMP and Krita work too.
2. Pick a bright color like red. Take the **paint bucket** (fill) tool and click once on the biggest black area.
3. Everything connected turns red. **Any black left over is a loose piece.** Zoom in around the eyes, teeth, ears, lettering and wheel rims.

Tiny black specks you can just paint white. Bigger pieces need a bridge: ask the AI (step 6) or draw one yourself (step 8).

**Thin lines.** Decide how wide the finished piece will be. Then 1 mm of metal = (image width in pixels ÷ finished width in mm) pixels.
Example: a 2000-pixel-wide image cut 400 mm wide gives 5 pixels per mm, so a 1 mm line is 5 pixels wide. Zoom in and check that no important line is narrower than your sheet thickness.

## 8. Trace, fix and cut

1. **Trace it to a vector.** In xTool Studio: import the image, select it, then **Trace image**, and check the preview is closed outlines. Then delete the bitmap. Inkscape (free: Path → Trace Bitmap) and LightBurn trace images too.
2. **Set the real size,** with the aspect ratio locked.
3. **Bridge any last loose pieces by hand** with thin lines where they barely change the look. The video did this for text and wheel rims.
   Or add a **border frame** that touches the art, so everything connects to it. It's sturdier and gives you room for mounting holes.
4. **Cut.** The video used 20 ga cold-rolled steel on an xTool MetalFab: material preset "1 mm carbon steel," 2 mm nozzle, compressed-air assist, calibrated height sensor. Degrease the steel first; it ships oiled.
5. **Finish.** Knock the dross off the bottom edges, wipe with alcohol, and spray paint (black works on most walls). He mounted his on a planed pine board.

## Other materials

The same method works for acrylic on a diode laser or for 3D-printed inlays; only the detail level changes.
For 3D prints, ask for much less detail: small parts don't print well.

## Tips

- **Keep a notes file** with every prompt you sent. When a round goes wrong, you can go back one step.
- **Download at the largest size offered.** Small images trace badly.
- **Be blunt in corrections.** "Slightly, and I mean slightly" is in the video for a reason.
- **One subject, plain words.** "The truck's grille, headlights and wheels" works better than a long description of the scene.
- **Not getting there after 5 rounds?** Try a different photo of the same subject, with better light or a clearer angle. It's often faster than fighting the AI.
