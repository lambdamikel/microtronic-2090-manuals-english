#!/usr/bin/env python3
"""
Catch mutilated graphics: figures/diagrams that a text-block mask is covering.

Idea (per review feedback): "subtract the transcribed from the original — if you
find graphics outside your text boxes, there's an issue." We rebuild the exact
white masks that build_page_html lays down, subtract the regions where we
legitimately redraw a table, and then look at what ORIGINAL ink is left under a
mask. Prose is made of short strokes; figures (flow charts, cartoons,
schematics, the computer-board drawing) are made of LONG straight lines and big
solid fills. So: any long line of original ink sitting under a mask is a figure
being eaten — we report it.

This is the backstop for the known gap in detect_regions.clip_blocks_to_text
(merge sometimes over-extends a prose bbox past its text onto a figure below).

    python3 tools/check_graphics.py --root anl2090-1 --pages 49-56
    python3 tools/check_graphics.py --root anl2090-1 --pages 56 --debug /tmp/p56.png
"""
import argparse, json, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from detect_regions import _cluster_cells, detect_regions   # noqa: E402

DARK = 135
PAD_MM = {"body": 1.2, "title": 1.5}   # must match build_page_html.PAD_MM
MIN_LINE_PX = 40        # a "graphic" line is at least this long (full res)
MIN_CLUSTER_INK = 40    # ignore clusters with fewer removed line-pixels
CELL = 24               # coarse-grid cell (full res) for clustering hits


def _runs_ge(row, min_len):
    d = np.diff(np.concatenate(([0], row.astype(np.int8), [0])))
    s = np.where(d == 1)[0]
    e = np.where(d == -1)[0]
    return [(a, b) for a, b in zip(s, e) if b - a >= min_len]


def _mask_and_table(layout, en, ppm, shape):
    """Return (mask_union, redrawn_table_union) boolean bitmaps, mirroring how
    build_page_html decides what to white out."""
    H, W = shape
    mask = np.zeros((H, W), bool)
    tbl = np.zeros((H, W), bool)
    for i, b in enumerate(layout["text_blocks"]):
        if b.get("kind") not in ("body", "title"):
            continue
        e = (en.get(str(i)) or {}).get("en")
        if not e:                       # empty en => build lays no mask
            continue
        pad = int(round(PAD_MM[b["kind"]] * ppm))
        if b.get("mask_lines"):
            units = b.get("lines") or b.get("fragments") or [b["bbox"]]
        else:
            units = [b["bbox"]] + list(b.get("extra_masks", []))
        for (x0, y0, x1, y1) in units:
            mask[max(0, y0 - pad):min(H, y1 + pad),
                 max(0, x0 - pad):min(W, x1 + pad)] = True
        if "<table" in e.lower():       # redrawn table (standalone or embedded)
            x0, y0, x1, y1 = b["bbox"]
            tbl[max(0, y0 - pad):min(H, y1 + pad),
                max(0, x0 - pad):min(W, x1 + pad)] = True
    return mask, tbl


def _removed_lines(removed):
    """Bitmap of removed-ink pixels that belong to a long horizontal or vertical
    run (i.e. figure edges, not prose strokes)."""
    H, W = removed.shape
    out = np.zeros((H, W), bool)
    for y in range(H):
        for a, b in _runs_ge(removed[y], MIN_LINE_PX):
            out[y, a:b] = True
    for x in range(W):
        for a, b in _runs_ge(removed[:, x], MIN_LINE_PX):
            out[a:b, x] = True
    return out


def check_page(root, n, debug=None):
    layout = json.loads((root / "layout" / f"page-{n:02d}.json").read_text())
    enpath = root / "translations" / f"page-{n:02d}.en.json"
    en = json.loads(enpath.read_text()) if enpath.exists() else {}
    ppm = layout["px_per_mm"]
    img = np.asarray(Image.open(root / "pages" / f"page-{n:02d}.png").convert("L"))
    H, W = img.shape
    dark = img < DARK

    mask, tbl = _mask_and_table(layout, en, ppm, (H, W))
    # also exclude any grid detect_regions sees as a table: a table grid covered
    # by a prose mask is intended (e.g. the German header a redrawn table starts
    # below), not a mutilated figure.
    for r in detect_regions(str(root / "pages" / f"page-{n:02d}.png")):
        if r["kind"] == "table":
            x0, y0, x1, y1 = r["bbox"]
            tbl[max(0, y0 - 6):min(H, y1 + 6), max(0, x0 - 6):min(W, x1 + 6)] = True
    removed = dark & mask & (~tbl)
    lines = _removed_lines(removed)

    # cluster the offending pixels into report boxes via a coarse grid
    gh, gw = (H + CELL - 1) // CELL, (W + CELL - 1) // CELL
    cells = np.zeros((gh, gw), bool)
    ys, xs = np.where(lines)
    cells[ys // CELL, xs // CELL] = True
    findings = []
    for (r0, c0, r1, c1) in _cluster_cells(cells, 1):
        bx0, by0 = c0 * CELL, r0 * CELL
        bx1, by1 = min(W, (c1 + 1) * CELL), min(H, (r1 + 1) * CELL)
        ink = int(lines[by0:by1, bx0:bx1].sum())
        if ink >= MIN_CLUSTER_INK:
            findings.append({"bbox": [bx0, by0, bx1, by1], "line_px": ink})
    findings.sort(key=lambda f: -f["line_px"])

    if debug:
        im = Image.open(root / "pages" / f"page-{n:02d}.png").convert("RGB")
        ov = np.asarray(im).copy()
        ov[lines] = (255, 30, 30)
        im = Image.fromarray(ov)
        d = ImageDraw.Draw(im)
        for f in findings:
            d.rectangle(f["bbox"], outline=(255, 0, 0), width=6)
        im.save(debug)
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="anl2090-1")
    ap.add_argument("--pages", required=True, help="e.g. 49-56 or 5,7,8")
    ap.add_argument("--debug", help="write an overlay PNG (single page only)")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    if "-" in args.pages:
        a, z = (int(x) for x in args.pages.split("-")); nums = range(a, z + 1)
    else:
        nums = [int(x) for x in args.pages.split(",")]
    total = 0
    for n in nums:
        if not (root / "layout" / f"page-{n:02d}.json").exists():
            continue
        findings = check_page(root, n, args.debug if len(list(nums)) == 1 else None)
        if findings:
            total += len(findings)
            print(f"⚠ page {n}: {len(findings)} graphic(s) under a mask")
            for f in findings:
                print(f"    bbox {f['bbox']}  ({f['line_px']} line-px masked)")
        else:
            print(f"✓ page {n}: clean")
    if total:
        print(f"\n{total} suspect region(s). A figure is being covered by a text "
              f"mask — clip that block's bbox y_max to just below its last text row.")
        sys.exit(1)


if __name__ == "__main__":
    main()
