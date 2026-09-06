#!/usr/bin/env python3
"""Find German that survives just outside a white-out - "pixel dust".

    tools/check_residue.py --pages 6-68 [--band 6]

Every overlay masks its box at the EXACT marked coordinates. If a box was drawn
a few pixels inside the German it covers, the stems of the outermost glyphs
survive as a thin line of dust along the edge, right where the English now
sits. It is easy to miss on screen and impossible to miss in print.

check_overflow measures the English against its box; check_graphics looks for
figures being eaten by a mask. Neither looks at what the mask FAILED to cover.

Method: for each masked rect, read a `band`-pixel strip just outside each edge
of the ORIGINAL scan. Ink there is only interesting if it lines up with the
text inside the box - so for the left/right strips we keep only ink on rows
that carry text inside the box, and for the top/bottom strips only ink on such
columns. Rules, frames and the neighbouring column sit on their own rows or far
enough away not to register.
"""
import argparse, json, sys
from pathlib import Path

import numpy as np
from PIL import Image

DARK = 128
MIN_INK = 12          # pixels of aligned dust before it is worth reporting


def check_page(root, n, band):
    lay = root / "layout" / f"page-{n:02d}.json"
    img = root / "pages" / f"page-{n:02d}.png"
    if not lay.exists() or not img.exists():
        return []
    blocks = json.loads(lay.read_text()).get("text_blocks", [])

    # This test assumes dark text on a light page: it thresholds grayscale, and
    # on the colour covers the red field itself falls below DARK, so every mask
    # would be reported as sitting in a sea of "ink". Skip those and say so.
    rgb = np.asarray(Image.open(img).convert("RGB")).astype(int)
    sat = (rgb.max(2) - rgb.min(2)) > 60
    if sat.mean() > 0.05:
        return "colour"

    a = np.asarray(Image.open(img).convert("L")) < DARK
    H, W = a.shape
    hits = []

    # Ink under ANY mask on the page is covered, whichever block put it there:
    # a sliver masked by its own whiteout block is not residue. Blank it first,
    # then every remaining dark pixel is genuinely still on the page.
    for b in blocks:
        for r in b.get("tight_masks", []):
            mx0, my0, mx1, my1 = (int(v) for v in r)
            a[max(0, my0):min(H, my1), max(0, mx0):min(W, mx1)] = False

    orig = np.asarray(Image.open(img).convert("L")) < DARK

    for bi, b in enumerate(blocks):
        for r in b.get("tight_masks", []):
            x0, y0, x1, y1 = (int(v) for v in r)
            x0, y0 = max(0, x0), max(0, y0)
            x1, y1 = min(W, x1), min(H, y1)
            if x1 - x0 < 20 or y1 - y0 < 20:
                continue
            inside = orig[y0:y1, x0:x1]
            rows = inside.sum(1) > 0          # rows that carry text
            cols = inside.sum(0) > 0
            for edge, strip, mask in (
                    ("left",   a[y0:y1, max(0, x0 - band):x0],      rows),
                    ("right",  a[y0:y1, x1:min(W, x1 + band)],      rows),
                    ("top",    a[max(0, y0 - band):y0, x0:x1],      cols),
                    ("bottom", a[y1:min(H, y1 + band), x0:x1],      cols)):
                if strip.size == 0:
                    continue
                sel = strip[mask] if edge in ("left", "right") else strip[:, mask]
                ink = int(sel.sum())
                if ink >= MIN_INK:
                    hits.append((bi, edge, ink, [x0, y0, x1, y1]))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--pages", required=True)
    ap.add_argument("--band", type=int, default=6)
    args = ap.parse_args()
    root = Path(args.root).resolve()

    nums = []
    for part in args.pages.split(","):
        if "-" in part:
            a, b = part.split("-"); nums += list(range(int(a), int(b) + 1))
        else:
            nums.append(int(part))

    bad = 0
    for n in nums:
        hits = check_page(root, n, args.band)
        if hits == "colour":
            print(f"page {n}: colour page - edge test does not apply, skipped")
            continue
        if not hits:
            continue
        bad += 1
        print(f"page {n}:")
        for bi, edge, ink, box in hits:
            print(f"    block {bi:2d} {edge:6} edge  {ink:4d} px of aligned ink  box={box}")
    if not bad:
        print("no residue")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
