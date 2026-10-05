#!/usr/bin/env python3
"""Notan photo -> cuttable metal art helpers.

Method by NeedItMakeIt: "Converting any photo into Artwork and making it with
the xTool MetalFab", https://www.youtube.com/watch?v=OXh7r_nBAEA

  gen   PHOTO OUT.png --prompt-file P.txt [--ref PREV.png] [--size 2K]
        One Gemini (Nano Banana Pro) call. Stateless, so every call is a "new chat"
        that re-sends the original photo (what the video recommends anyway).
  check IMG.png --width-mm 600 [--min-mm 1.0] [--fix]
        Finds islands (black pieces not attached to the main body: they fall out
        when cut) and metal thinner than --min-mm. Writes IMG_check.png overlay
        (red = island, blue = too thin) and prints JSON. --fix whitens specks.
  trace IMG.png OUT.svg --width-mm 600
        potrace -> closed-path SVG at real size.
  selftest
"""
import argparse, base64, json, os, subprocess, sys, urllib.request
import cv2
import numpy as np

MODEL = "gemini-3-pro-image"  # "Nano Banana Pro"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"


def gen(photo, out, prompt, refs=(), size="2K"):
    def part(path):
        mime = "image/png" if path.lower().endswith(".png") else "image/jpeg"
        return {"inline_data": {"mime_type": mime, "data": base64.b64encode(open(path, "rb").read()).decode()}}
    body = {
        "contents": [{"parts": [part(photo), *[part(r) for r in refs], {"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"], "imageConfig": {"imageSize": size}},
    }
    req = urllib.request.Request(URL, json.dumps(body).encode(), {
        "Content-Type": "application/json", "x-goog-api-key": os.environ["GEMINI_API_KEY"]})
    resp = json.load(urllib.request.urlopen(req, timeout=300))
    cand = (resp.get("candidates") or [{}])[0]
    parts = cand.get("content", {}).get("parts")
    if not parts:  # refused: promptFeedback.blockReason, or a candidate with only a finishReason
        sys.exit("blocked by Gemini: " + json.dumps(resp.get("promptFeedback") or {"finishReason": cand.get("finishReason")}))
    imgs = [p["inlineData"]["data"] for p in parts if "inlineData" in p]
    if not imgs:
        sys.exit("no image returned: " + " ".join(p.get("text", "") for p in parts)[:500])
    open(out, "wb").write(base64.b64decode(imgs[-1]))
    print(out)


def binarize(img):
    """True = black = metal that stays."""
    g = img if img.ndim == 2 else cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, b = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return b == 0


def check(metal, width_mm, min_mm=1.0, speck_mm2=4.0):
    px_mm = metal.shape[1] / width_mm
    # 4-connectivity: corner-touching pixels are not a real metal joint
    n, lab, stats, _ = cv2.connectedComponentsWithStats(metal.astype(np.uint8), connectivity=4)
    areas = stats[1:, cv2.CC_STAT_AREA]
    main = 1 + int(np.argmax(areas)) if n > 1 else 0
    islands = [i for i in range(1, n) if i != main]
    speck_px = speck_mm2 * px_mm ** 2
    specks = [i for i in islands if stats[i, cv2.CC_STAT_AREA] < speck_px]
    # metal an opening with a min-width disk can't keep = too thin to survive the cut
    k = max(3, int(round(min_mm * px_mm)) | 1)
    disk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    thin = metal & ~cv2.morphologyEx(metal.astype(np.uint8), cv2.MORPH_OPEN, disk).astype(bool)
    thin_px = int(thin.sum())
    return {
        "px_per_mm": round(px_mm, 2),
        "pieces": n - 1,
        "islands": len(islands),
        "specks": len(specks),
        "island_areas_mm2": sorted((round(stats[i, cv2.CC_STAT_AREA] / px_mm ** 2, 1) for i in islands), reverse=True)[:20],
        "thin_pct_of_metal": round(100 * thin_px / max(1, int(metal.sum())), 2),
        "ok": not islands and thin_px / max(1, int(metal.sum())) < 0.005,
    }, lab, islands, specks, thin


def cmd_check(a):
    metal = binarize(cv2.imread(a.img))
    rep, lab, islands, specks, thin = check(metal, a.width_mm, a.min_mm)
    vis = np.full(metal.shape + (3,), 255, np.uint8)
    vis[metal] = (90, 90, 90)
    vis[thin] = (255, 120, 0)                       # blue (BGR)
    vis[np.isin(lab, islands)] = (0, 0, 255)        # red
    base = os.path.splitext(a.img)[0]
    cv2.imwrite(base + "_check.png", vis)
    if a.fix and specks:
        metal[np.isin(lab, specks)] = False
        cv2.imwrite(base + "_clean.png", np.where(metal, 0, 255).astype(np.uint8))
        rep["clean"] = base + "_clean.png"
    rep["overlay"] = base + "_check.png"
    print(json.dumps(rep, indent=1))


def cmd_trace(a):
    metal = binarize(cv2.imread(a.img))
    pbm = os.path.splitext(a.out)[0] + ".pbm"  # not a NamedTemporaryFile: Windows can't reopen those
    cv2.imwrite(pbm, np.where(metal, 0, 255).astype(np.uint8))  # PBM: black pixel = shape
    try:
        # ponytail: turdsize 10px drops specks; raise it if traces come out noisy
        subprocess.run(["potrace", pbm, "-s", "-o", a.out, "-W", f"{a.width_mm}mm",
                        "--turdsize", "10", "--alphamax", "1.0", "--opttolerance", "0.2"], check=True)
    finally:
        os.remove(pbm)
    print(a.out)


def selftest():
    m = np.zeros((400, 400), bool)
    m[50:350, 50:150] = True              # main body
    m[50:350, 250:350] = True             # second big piece -> island
    m[195:197, 150:250] = True            # 2px bridge joins them: thin, not an island
    m[10:12, 10] = True                   # speck: 2 mm^2 at 1 px/mm, under the 4 mm^2 limit
    rep, *_ = check(m, width_mm=400)      # 1 px/mm
    assert rep["islands"] == 1 and rep["specks"] == 1, rep
    assert rep["thin_pct_of_metal"] > 0, rep
    m[195:197, 150:250] = False           # cut the bridge -> 2 islands
    assert check(m, 400)[0]["islands"] == 2
    print("selftest ok")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    g = s.add_parser("gen"); g.add_argument("photo"); g.add_argument("out")
    g.add_argument("--prompt-file", required=True); g.add_argument("--ref", action="append", default=[])
    g.add_argument("--size", default="2K", choices=["1K", "2K", "4K"])
    c = s.add_parser("check"); c.add_argument("img"); c.add_argument("--width-mm", type=float, required=True)
    c.add_argument("--min-mm", type=float, default=1.0); c.add_argument("--fix", action="store_true")
    t = s.add_parser("trace"); t.add_argument("img"); t.add_argument("out"); t.add_argument("--width-mm", type=float, required=True)
    s.add_parser("selftest")
    a = p.parse_args()
    if a.cmd == "gen":
        gen(a.photo, a.out, open(a.prompt_file).read(), a.ref, a.size)
    elif a.cmd == "check":
        cmd_check(a)
    elif a.cmd == "trace":
        cmd_trace(a)
    else:
        selftest()
