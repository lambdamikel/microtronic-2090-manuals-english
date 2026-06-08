#!/usr/bin/env python3
"""
OCR-independent detection of tables and figures via long straight lines.

Prose text has only short strokes; tables and flow charts/diagrams are built
from long straight lines (borders, box edges, connectors). We find those lines,
cluster them into regions, and classify each region:

  table  — a regular grid: several near-full-width horizontal rules PLUS
           full-height vertical column separators.
  figure — line-art that is not a grid (flow chart, schematic, diagram).

Output regions are in full-resolution page pixels: {bbox:[x0,y0,x1,y1], kind}.

This module is used by extract_layout.py to (a) clip text-block masks so they
can never cover a figure, and (b) emit table regions as translation stubs.

Run standalone to dump a debug overlay:
    python3 detect_regions.py pages/page-40.png --debug /tmp/p40_regions.png
"""
import argparse, json, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


# --- tuning (all in FULL-resolution pixels; scaled internally) -----------------
DOWNSCALE = 2                 # work at half resolution for speed
MIN_LINE_FULL = 46            # a "long line" is >= this many px (full res)
DARK_THRESH = 135             # grayscale < this = ink
CELL_FULL = 24                # coarse-grid cell size (full res) for clustering
GAP_CELLS = 1                 # bridge gaps up to this many empty cells
MIN_REGION_FULL = 70          # drop regions smaller than this in either dim


def _runs(mask_row, min_len):
    """Yield (start, end) half-open index ranges of True runs >= min_len."""
    d = np.diff(np.concatenate(([0], mask_row.astype(np.int8), [0])))
    starts = np.where(d == 1)[0]
    ends = np.where(d == -1)[0]
    out = []
    for s, e in zip(starts, ends):
        if e - s >= min_len:
            out.append((s, e))
    return out


def _line_segments(dark, min_len):
    """Return (h_segments, v_segments) as lists of (x0, y0, x1, y1) in the
    downscaled coordinate frame. Horizontal segments scan rows; vertical scan
    columns."""
    h, w = dark.shape
    hsegs, vsegs = [], []
    for y in range(h):
        for s, e in _runs(dark[y], min_len):
            hsegs.append((s, y, e, y))
    for x in range(w):
        for s, e in _runs(dark[:, x], min_len):
            vsegs.append((x, s, x, e))
    return hsegs, vsegs


def _cluster_cells(cells, gap):
    """Flood-fill a boolean coarse grid into connected components, bridging up
    to `gap` empty cells. Returns list of (r0, c0, r1, c1) inclusive bounds."""
    H, W = cells.shape
    seen = np.zeros_like(cells, dtype=bool)
    comps = []
    for r0 in range(H):
        for c0 in range(W):
            if not cells[r0, c0] or seen[r0, c0]:
                continue
            stack = [(r0, c0)]
            seen[r0, c0] = True
            minr = maxr = r0
            minc = maxc = c0
            while stack:
                r, c = stack.pop()
                minr, maxr = min(minr, r), max(maxr, r)
                minc, maxc = min(minc, c), max(maxc, c)
                for dr in range(-1 - gap, 2 + gap):
                    for dc in range(-1 - gap, 2 + gap):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < H and 0 <= nc < W and cells[nr, nc] and not seen[nr, nc]:
                            seen[nr, nc] = True
                            stack.append((nr, nc))
            comps.append((minr, minc, maxr, maxc))
    return comps


def _classify(region, hsegs, vsegs, ds):
    """table vs figure for a region (full-res bbox). A table has >=3 horizontal
    rules spanning >=55% of its width and >=2 vertical rules spanning >=45% of
    its height."""
    x0, y0, x1, y1 = [v / ds for v in region]      # to downscaled frame
    rw, rh = max(1, x1 - x0), max(1, y1 - y0)
    full_h = 0
    for sx0, sy0, sx1, sy1 in hsegs:
        if y0 - 2 <= sy0 <= y1 + 2 and (min(sx1, x1) - max(sx0, x0)) >= 0.55 * rw:
            full_h += 1
    full_v = 0
    for sx0, sy0, sx1, sy1 in vsegs:
        if x0 - 2 <= sx0 <= x1 + 2 and (min(sy1, y1) - max(sy0, y0)) >= 0.45 * rh:
            full_v += 1
    return "table" if (full_h >= 3 and full_v >= 2) else "figure"


def detect_regions(image_path, return_segments=False):
    img = Image.open(image_path).convert("L")
    W0, H0 = img.size
    ds = DOWNSCALE
    small = img.resize((W0 // ds, H0 // ds))
    arr = np.asarray(small)
    dark = arr < DARK_THRESH
    min_len = max(8, MIN_LINE_FULL // ds)
    hsegs, vsegs = _line_segments(dark, min_len)

    # mark coarse cells that contain any long-line pixel
    cell = max(4, CELL_FULL // ds)
    Hs, Ws = dark.shape
    gh, gw = (Hs + cell - 1) // cell, (Ws + cell - 1) // cell
    cells = np.zeros((gh, gw), dtype=bool)
    for x0, y0, x1, y1 in hsegs:
        cy = y0 // cell
        for cx in range(x0 // cell, x1 // cell + 1):
            cells[cy, cx] = True
    for x0, y0, x1, y1 in vsegs:
        cx = x0 // cell
        for cy in range(y0 // cell, y1 // cell + 1):
            cells[cy, cx] = True

    comps = _cluster_cells(cells, GAP_CELLS)
    regions = []
    for (r0, c0, r1, c1) in comps:
        bx0 = c0 * cell * ds
        by0 = r0 * cell * ds
        bx1 = min(W0, (c1 + 1) * cell * ds)
        by1 = min(H0, (r1 + 1) * cell * ds)
        if (bx1 - bx0) < MIN_REGION_FULL or (by1 - by0) < MIN_REGION_FULL:
            continue
        kind = _classify((bx0, by0, bx1, by1), hsegs, vsegs, ds)
        regions.append({"bbox": [bx0, by0, bx1, by1], "kind": kind})
    regions.sort(key=lambda r: (r["bbox"][1], r["bbox"][0]))
    if return_segments:
        return regions, (hsegs, vsegs, ds)
    return regions


def _longest_run(row):
    d = np.diff(np.concatenate(([0], row.astype(np.int8), [0])))
    s = np.where(d == 1)[0]
    e = np.where(d == -1)[0]
    return int((e - s).max()) if len(s) else 0


def _is_preservable_figure(band, W, ppm):
    """True if `band` (rows x W bool) looks like an irregular figure we must
    preserve (flow chart, cartoon, schematic). Distinguishers:
      * NOT a regular table grid (>=3 near-full-width rules => redraw target),
      * sparse: a low fraction of rows are text rows (prose is dense),
      * has at least one long vertical stroke (prose has none).
    """
    H = band.shape[0]
    ink_thr = max(3, int(0.012 * W))
    if H < int(8 * ppm) or band.sum() < 6 * ink_thr:
        return False
    line_thr = 0.5 * W
    # regular grid? -> redraw target, do not clip prose off it
    full_h = sum(1 for r in range(H) if _longest_run(band[r]) >= 0.55 * W)
    if full_h >= 3:
        return False
    # text-row fraction: prose is dense with text rows; a figure (flow chart /
    # cartoon / schematic) is sparse — lots of whitespace between strokes.
    text_rows = 0
    for r in range(H):
        if band[r].sum() >= ink_thr and _longest_run(band[r]) < line_thr:
            text_rows += 1
    # sparse, non-grid, inked region right below the gap -> a figure to preserve
    return text_rows / H < 0.42


def text_extent_ymax(arr, bbox, ppm, dark=DARK_THRESH):
    """Return the y_max to which a text block's mask should be clipped so it
    does not cover a *figure* (flow chart / cartoon / schematic) sitting below
    its text. Conservative by design — only clips when, immediately below a
    rule or a >=12 mm blank gap, there is irregular line-art (NOT a table grid,
    which is a redraw target, and NOT prose, which has no long vertical lines).
    Returns the original y_max if nothing qualifies."""
    x0, y0, x1, y1 = bbox
    sub = arr[y0:y1, x0:x1] < dark
    if sub.size == 0:
        return y1
    H, W = sub.shape
    ink = sub.sum(axis=1)
    line_thr = 0.5 * W
    ink_thr = max(3, int(0.012 * W))
    gap_rows = int(12 * ppm)          # bigger than any prose paragraph break
    look = int(55 * ppm)              # inspect the figure band just below
    margin = int(1.5 * ppm)
    is_text = np.zeros(H, bool)
    is_line = np.zeros(H, bool)
    for r in range(H):
        is_line[r] = _longest_run(sub[r]) >= line_thr
        is_text[r] = (ink[r] >= ink_thr) and not is_line[r]

    last_text = -1
    r = 0
    while r < H:
        if is_text[r]:
            last_text = r
            r += 1
            continue
        if last_text < 0:             # leading blank before any text
            r += 1
            continue
        # candidate boundary: a rule row, or the start of a long blank gap
        if is_line[r]:
            boundary = r
        else:
            j = r
            while j < H and not is_text[j] and not is_line[j]:
                j += 1
            if j - r < gap_rows:      # small paragraph gap — keep scanning
                r = j
                continue
            boundary = r
        band = sub[boundary: min(H, boundary + look)]
        if band.sum() >= 5 * ink_thr and _is_preservable_figure(band, W, ppm):
            return y0 + last_text + margin
        # not a figure (prose or a redraw table) — skip past and keep scanning
        r = boundary + 1
        while r < H and not is_text[r]:
            r += 1
    return y1


def clip_blocks_to_text(blocks, image_path, ppm):
    """Shrink each body/title block's mask off any figure/table below its text.
    Mutates block bboxes/fragments/lines in place. Returns the blocks."""
    arr = np.asarray(Image.open(image_path).convert("L"))
    Hh, Ww = arr.shape
    for b in blocks:
        if b.get("kind") not in ("body", "title"):
            continue
        x0, y0, x1, y1 = b["bbox"]
        x0 = max(0, x0); y0 = max(0, y0); x1 = min(Ww, x1); y1 = min(Hh, y1)
        new_y_max = text_extent_ymax(arr, [x0, y0, x1, y1], ppm)
        if new_y_max < b["bbox"][3] - 2:
            b["bbox"][3] = int(new_y_max)
            b["fragments"] = [list(b["bbox"])]
            b["lines"] = [list(b["bbox"])]
    return blocks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("--debug", help="write an overlay PNG")
    ap.add_argument("--json", action="store_true", help="print regions as JSON")
    args = ap.parse_args()
    regions = detect_regions(args.image)
    if args.json:
        print(json.dumps(regions, indent=2))
    else:
        for r in regions:
            print(r["kind"], r["bbox"])
    if args.debug:
        im = Image.open(args.image).convert("RGB")
        d = ImageDraw.Draw(im)
        for r in regions:
            color = (30, 90, 220) if r["kind"] == "table" else (220, 40, 40)
            d.rectangle(r["bbox"], outline=color, width=6)
        im.save(args.debug)
        print(f"wrote {args.debug}", file=sys.stderr)


if __name__ == "__main__":
    main()
