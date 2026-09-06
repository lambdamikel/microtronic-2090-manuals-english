#!/usr/bin/env python3
"""
Extract per-page layout from a scanned PDF page.

For each page PNG it:
  1. Runs tesseract with hOCR output (German, -psm 1).
  2. Parses the hOCR to extract text-block bounding boxes (ocr_carea + ocr_par).
  3. Writes layout/page-NN.json with { page_size, text_blocks: [{bbox, text}] }.

Figures = "everything on the page that is not inside a text bbox". So once we have
precise text-block bboxes, masking and figure cropping are both driven from the same
data and there is no per-page eyeball work.
"""
import argparse, json, os, re, subprocess, sys
from pathlib import Path
from html.parser import HTMLParser

BBOX_RE = re.compile(r"bbox (\d+) (\d+) (\d+) (\d+)")


def run_tesseract_hocr(image_path: Path, out_stem: Path):
    """Run tesseract producing <out_stem>.hocr if not already present."""
    hocr_path = out_stem.with_suffix(".hocr")
    if hocr_path.exists() and hocr_path.stat().st_mtime > image_path.stat().st_mtime:
        return hocr_path
    subprocess.run(
        ["tesseract", str(image_path), str(out_stem), "-l", "deu", "--psm", "1", "hocr"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return hocr_path


class HocrParser(HTMLParser):
    """Pull out ocr_carea bboxes and the words they contain."""

    def __init__(self):
        super().__init__()
        self.page_size = None  # (w, h)
        self.blocks = []  # list of {bbox: [x0,y0,x1,y1], text: str}
        self._stack = []  # stack of (class, bbox, text_buf)

    @staticmethod
    def _bbox_from_title(title):
        m = BBOX_RE.search(title or "")
        if not m:
            return None
        return [int(m.group(i)) for i in range(1, 5)]

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "")
        title = a.get("title", "")
        bbox = self._bbox_from_title(title)
        if cls == "ocr_page" and bbox:
            self.page_size = (bbox[2], bbox[3])
        if cls in ("ocr_carea", "ocr_line", "ocrx_word"):
            self._stack.append({"class": cls, "bbox": bbox, "text": [], "lines": []})

    def handle_data(self, data):
        if not self._stack:
            return
        if self._stack[-1]["class"] == "ocrx_word":
            self._stack[-1]["text"].append(data)

    def handle_endtag(self, tag):
        if not self._stack:
            return
        top = self._stack[-1]
        # Lines and words use <span>; areas use <div>. Pop only on a class match.
        if tag == "span" and top["class"] in ("ocrx_word", "ocr_line"):
            popped = self._stack.pop()
            if popped["class"] == "ocrx_word":
                for parent in reversed(self._stack):
                    if parent["class"] == "ocr_carea":
                        parent["text"].append("".join(popped["text"]).strip())
                        break
            elif popped["class"] == "ocr_line":
                # attach line bbox to enclosing carea
                for parent in reversed(self._stack):
                    if parent["class"] == "ocr_carea" and popped["bbox"]:
                        parent["lines"].append(popped["bbox"])
                        break
        elif tag == "div" and top["class"] == "ocr_carea":
            popped = self._stack.pop()
            text = " ".join(t for t in popped["text"] if t).strip()
            if popped["bbox"]:
                self.blocks.append(
                    {
                        "bbox": popped["bbox"],
                        "text": text,
                        "lines": popped["lines"],
                    }
                )


def parse_hocr(hocr_path: Path):
    p = HocrParser()
    p.feed(hocr_path.read_text(encoding="utf-8", errors="replace"))
    return p.page_size, p.blocks


def classify(block, px_per_mm):
    """Tag each block as 'body', 'title', 'label', or 'noise'.

    body  — real body-text paragraph (will be masked + overlaid in English)
    title — page/section heading at top of a column (masked + overlaid)
    label — annotation near a figure (kept in original German)
    noise — garbage OCR (dot grids, decorative borders) — ignored entirely
    """
    bb = block["bbox"]
    x0, y0, x1, y1 = bb
    w_mm = (x1 - x0) / px_per_mm
    h_mm = (y1 - y0) / px_per_mm
    area = w_mm * h_mm
    text = block["text"]
    n = len(text)
    if n == 0:
        return "noise"
    alpha = sum(1 for c in text if c.isalpha())
    alpha_ratio = alpha / n

    # Reject obvious noise: symbol-heavy, or oddly wide (page-spanning) blocks
    # that are almost always dot-grid OCR.
    if alpha_ratio < 0.55:
        return "noise"
    if w_mm > 140 and h_mm > 40:
        return "noise"
    # Diagrammatic text inside figures often contains '|' or '_' separators.
    if (text.count("|") + text.count("_")) / n > 0.03:
        return "noise"

    # Title / section sub-heading: short bold-looking text.
    # Allowed either at the very top of a column (y_top < 25 mm) OR as a
    # narrower stand-alone line that we can later promote next to a body block.
    y_top_mm = y0 / px_per_mm
    if y_top_mm < 25 and h_mm < 14 and 20 < w_mm < 130 and n < 100:
        return "title"

    # Body: column-shaped block. Either tall (≥ 12 mm, ~4 lines) OR shorter but
    # with many real words (multi-sentence body fragment that wrapped tightly).
    word_count = len(text.split())
    if (
        40 <= w_mm <= 110
        and alpha_ratio >= 0.6
        and n >= 60
        and (h_mm >= 12 or word_count >= 10)
    ):
        return "body"

    # Anything else: small annotation / figure label.
    return "label"


def promote_wrap_fragments(blocks, px_per_mm):
    """Tesseract splits a paragraph that wraps around a figure into multiple
    ocr_careas. Promote 'label' blocks to 'body' iff they are
      * wide enough to be a real body-text fragment (≥ 30 mm),
      * vertically adjacent (≤ 6 mm) to an existing body block,
      * horizontally overlapping the body's x-range.
    A 30 mm width floor keeps narrow callouts/speech bubbles out.
    """
    near_mm = 6.0
    near_px = near_mm * px_per_mm
    min_w_px = 30.0 * px_per_mm
    bodies = [b for b in blocks if b["kind"] == "body"]
    changed = True
    while changed:
        changed = False
        for b in blocks:
            if b["kind"] != "label":
                continue
            bb = b["bbox"]
            if (bb[2] - bb[0]) < min_w_px:
                continue
            for body in bodies:
                cb = body["bbox"]
                if bb[2] < cb[0] or bb[0] > cb[2]:
                    continue
                if abs(bb[1] - cb[3]) < near_px or abs(cb[1] - bb[3]) < near_px:
                    b["kind"] = "body"
                    bodies.append(b)
                    changed = True
                    break
    return blocks


def _x_overlap_ratio(a, b):
    """Fraction of the narrower bbox's x-extent that overlaps the wider one."""
    ax0, ax1 = a[0], a[2]
    bx0, bx1 = b[0], b[2]
    inter = max(0, min(ax1, bx1) - max(ax0, bx0))
    return inter / max(1, min(ax1 - ax0, bx1 - bx0))


def merge_into_regions(blocks, px_per_mm, kind):
    """Cluster same-kind blocks into one merged region per column.

    Two blocks belong to the same region if their x-ranges overlap by ≥ 60%
    AND they are vertically reachable (≤ 100 mm gap), regardless of any
    figures sitting between them.
    """
    items = sorted(
        [b for b in blocks if b["kind"] == kind], key=lambda b: b["bbox"][1]
    )
    if not items:
        return []
    # 18 mm: small enough to split sub-sections separated by visible whitespace
    # (which is typically ~22 mm in this 1981 layout), large enough to keep
    # paragraph-level breaks (~3-5 mm) merged.
    max_gap_px = 18 * px_per_mm
    clusters = []
    for b in items:
        bb = b["bbox"]
        placed = False
        for c in clusters:
            for cb in c["bboxes"]:
                if _x_overlap_ratio(bb, cb) < 0.6:
                    continue
                vgap = max(0, max(bb[1] - cb[3], cb[1] - bb[3]))
                if vgap <= max_gap_px:
                    c["bboxes"].append(bb)
                    c["texts"].append(b["text"])
                    c["lines"].extend(b.get("lines") or [bb])
                    placed = True
                    break
            if placed:
                break
        if not placed:
            clusters.append(
                {
                    "bboxes": [bb],
                    "texts": [b["text"]],
                    "lines": list(b.get("lines") or [bb]),
                }
            )

    merged = []
    for c in clusters:
        bbs = c["bboxes"]
        union = [
            min(x[0] for x in bbs),
            min(x[1] for x in bbs),
            max(x[2] for x in bbs),
            max(x[3] for x in bbs),
        ]
        merged.append(
            {
                "kind": kind,
                "bbox": union,
                "fragments": bbs,
                "lines": c["lines"],
                "text": "  ".join(t for t in c["texts"] if t),
            }
        )
    return merged


def _has_tabular_neighbors(label, all_labels, px_per_mm):
    """Heuristic: a label is part of a table if there are several other small
    labels stacked near it (in the same column, similar widths/heights).
    Used to reject false title promotions from table-cell text.
    """
    bb = label["bbox"]
    h_label = bb[3] - bb[1]
    nearby = 0
    band_y = 30 * px_per_mm  # consider labels within ±30 mm vertically
    for other in all_labels:
        if other is label:
            continue
        ob = other["bbox"]
        if abs(ob[1] - bb[1]) > band_y and abs(ob[3] - bb[3]) > band_y:
            continue
        if _x_overlap_ratio(bb, ob) < 0.2:
            continue
        h_other = ob[3] - ob[1]
        if 0.5 * h_label <= h_other <= 2.0 * h_label:
            nearby += 1
    return nearby >= 3


def promote_section_headings(blocks, body_regions, px_per_mm):
    """Promote `label` blocks that look like section headings to `title`.
    A heading is short text either
      * at the top of a column (y_top < 25 mm), or
      * directly above a body block, with 5–25 mm of whitespace below it.
    Rejected if surrounded by ≥ 3 other similarly-sized labels (looks like a
    table cell), if digit-heavy, or if ending mid-sentence.
    """
    promoted = []
    near_max = 25 * px_per_mm
    near_min = 5 * px_per_mm
    min_w_px = 30 * px_per_mm
    all_labels = [b for b in blocks if b.get("kind") == "label"]
    for b in blocks:
        if b.get("kind") != "label":
            continue
        bb = b["bbox"]
        w_px = bb[2] - bb[0]
        h_mm = (bb[3] - bb[1]) / px_per_mm
        n = len(b["text"])
        if w_px < min_w_px or h_mm > 14 or n > 80 or n < 8:
            continue
        text = b["text"]
        digit_ratio = sum(1 for c in text if c.isdigit()) / max(1, n)
        if digit_ratio > 0.3:
            continue
        if text.rstrip().endswith(("-", ",", ".")) and not text.rstrip().endswith("!"):
            continue
        # New: reject if surrounded by similar-sized labels (table cells)
        if _has_tabular_neighbors(b, all_labels, px_per_mm):
            continue
        y_top_mm = bb[1] / px_per_mm
        if y_top_mm < 25:
            promoted.append(b)
            continue
        for body in body_regions:
            cb = body["bbox"]
            if _x_overlap_ratio(bb, cb) < 0.4:
                continue
            gap_above = cb[1] - bb[3]
            if near_min <= gap_above <= near_max:
                promoted.append(b)
                break
    new_titles = []
    for b in promoted:
        bb = b["bbox"]
        new_titles.append(
            {
                "kind": "title",
                "bbox": list(bb),
                "fragments": [list(bb)],
                "lines": [list(bb)],
                "text": b["text"],
            }
        )
    return new_titles


PAGE_NUM_SAFE_Y_PX = 3380  # do not extend any block below this y; reserve for page number


def detect_figure_bands(page_image_path: Path, blocks, px_per_mm, page_height_px):
    """Identify horizontal y-bands of the page that contain figure content —
    dark-pixel density much higher than would be expected from text alone,
    and crucially NOT covered by any OCR text bbox. Returns a list of (y0, y1)
    tuples in original-page pixels.

    Used by auto_extend to avoid pushing body bboxes into figure areas.
    """
    try:
        from PIL import Image
    except ImportError:
        return []
    if not page_image_path.exists():
        return []
    img = Image.open(page_image_path).convert("L")
    w, h = img.size
    # quick density per y-row, sampling every 8 px horizontally
    row_density = []
    step_x = 8
    sample_xs = list(range(0, w, step_x))
    for y in range(0, h, 4):
        dark = sum(1 for x in sample_xs if img.getpixel((x, y)) < 100)
        row_density.append((y, dark))
    # collect y-rows that are dense (≥ 15% of samples dark) and NOT inside
    # any text bbox
    text_bboxes = [b["bbox"] for b in blocks if b.get("kind") in ("body", "title", "label")]
    figure_rows = []
    threshold = max(8, int(0.10 * len(sample_xs)))
    for y, dark in row_density:
        if dark < threshold:
            continue
        # is this y inside any text bbox?
        inside_text = any(bb[1] <= y <= bb[3] for bb in text_bboxes)
        if not inside_text:
            figure_rows.append(y)
    # cluster contiguous rows into bands
    bands = []
    if not figure_rows:
        return bands
    band_start = figure_rows[0]
    last = band_start
    for y in figure_rows[1:]:
        if y - last > 30:  # gap > 30 px ends a band
            if last - band_start > 60:  # only keep bands ≥ 60 px tall
                bands.append((band_start, last))
            band_start = y
        last = y
    if last - band_start > 60:
        bands.append((band_start, last))
    return bands


def auto_extend_bodies_to_column_edges(blocks, px_per_mm, page_height_px, figure_bands=None):
    """Auto-extend each body block's y_max down to either:
      - the next-in-column block's y_min minus a small gap, or
      - the page-number safe-zone y (PAGE_NUM_SAFE_Y_PX),
    whichever comes first. This eliminates the recurring need to manually
    extend a body bbox when tables or extra rows live below the OCR-detected
    text region.

    Two blocks are 'in the same column' if their x-ranges overlap ≥ 50%.
    The extension only happens if no other block (any kind) intervenes in the
    vertical interval, AND the extension distance is ≤ 80 mm (above 80 mm we
    assume there's a figure / structural break we shouldn't cover blindly).
    """
    bottom_limit = min(page_height_px - 5, PAGE_NUM_SAFE_Y_PX)
    blocks_sorted = sorted(blocks, key=lambda b: (b["bbox"][1], b["bbox"][0]))
    intro_cap_px = 30 * px_per_mm
    body_cap_px = 80 * px_per_mm
    figure_bands = figure_bands or []
    for b in blocks_sorted:
        if b["kind"] != "body":
            continue
        bb = b["bbox"]
        original_h = bb[3] - bb[1]
        original_h_mm = original_h / px_per_mm
        # Find the next block in the same column below
        next_top = bottom_limit
        for other in blocks_sorted:
            if other is b:
                continue
            ob = other["bbox"]
            if _x_overlap_ratio(bb, ob) < 0.5:
                continue
            if ob[1] <= bb[3]:
                continue
            if ob[1] < next_top:
                next_top = ob[1]
        # Also stop at any figure band that begins below this block
        for fb_y0, fb_y1 in figure_bands:
            if fb_y0 > bb[3] and fb_y0 < next_top:
                next_top = fb_y0
        new_y_max = min(next_top - int(2 * px_per_mm), bottom_limit)
        if new_y_max <= bb[3]:
            continue
        extension = new_y_max - bb[3]
        # Stronger caps:
        #   - "intro" blocks (≤ 15 mm tall, ~3 lines) extend ≤ 30 mm absolute
        #   - everything else: 1.5× original height OR 80 mm, whichever smaller
        if original_h_mm <= 15:
            max_local = intro_cap_px
        else:
            max_local = min(body_cap_px, int(1.5 * original_h))
        if extension > max_local:
            new_y_max = bb[3] + int(max_local)
        bb[3] = new_y_max
        b["lines"] = [list(bb)]
        b["fragments"] = [list(bb)]
    return blocks


def clamp_to_page_safe_zone(blocks):
    """Ensure no block's bbox extends below the page-number safe zone."""
    for b in blocks:
        if b["bbox"][3] > PAGE_NUM_SAFE_Y_PX:
            b["bbox"][3] = PAGE_NUM_SAFE_Y_PX
            b["lines"] = [list(b["bbox"])]
            b["fragments"] = [list(b["bbox"])]
    return blocks


def write_layout(layout_path: Path, page_size, blocks, page_image_path: Path = None):
    px_per_mm = page_size[0] / 210.0
    page_height_px = page_size[1]
    for b in blocks:
        b["kind"] = classify(b, px_per_mm)
    blocks = promote_wrap_fragments(blocks, px_per_mm)

    body_regions = merge_into_regions(blocks, px_per_mm, "body")
    title_regions = merge_into_regions(blocks, px_per_mm, "title")

    # Auto-promote section headings from leftover labels
    section_titles = promote_section_headings(
        blocks, body_regions, px_per_mm
    )

    merged_blocks = body_regions + title_regions + section_titles

    # Detect figure bands from the image so auto-extend respects them
    figure_bands = []
    if page_image_path is not None:
        figure_bands = detect_figure_bands(page_image_path, blocks, px_per_mm, page_height_px)

    # Auto-extend body bboxes to fill their column down to the next block or figure
    merged_blocks = auto_extend_bodies_to_column_edges(
        merged_blocks, px_per_mm, page_height_px, figure_bands
    )

    # Clamp to page-number safe zone
    merged_blocks = clamp_to_page_safe_zone(merged_blocks)

    # Figure-safe masking: clip any block whose mask would cover a figure/table
    # that sits below its actual text (OCR careas often swallow a flow chart or
    # table beneath a paragraph). This is what prevents the "mask ate the
    # diagram" class of bug without any per-page work.
    if page_image_path is not None:
        try:
            from detect_regions import clip_blocks_to_text
            merged_blocks = clip_blocks_to_text(merged_blocks, page_image_path, px_per_mm)
        except Exception as e:
            print(f"  (clip_blocks_to_text skipped: {e})", file=sys.stderr)

    merged_blocks = sorted(
        merged_blocks, key=lambda b: (b["bbox"][1], b["bbox"][0])
    )
    payload = {
        "page_size_px": list(page_size),
        "dpi": 300,
        "px_per_mm": px_per_mm,
        "text_blocks": merged_blocks,
        "raw_blocks": [b for b in blocks if b["kind"] in ("body", "title", "label")],
    }
    layout_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".", help="Project root (anl2090-1/)")
    ap.add_argument("--page", type=int, help="Single page number (e.g. 5)")
    ap.add_argument("--range", help="Page range, e.g. 1-8")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    pages_dir = root / "pages"
    hocr_dir = root / "hocr"
    layout_dir = root / "layout"
    hocr_dir.mkdir(exist_ok=True)
    layout_dir.mkdir(exist_ok=True)

    if args.page is not None:
        nums = [args.page]
    elif args.range:
        lo, hi = (int(x) for x in args.range.split("-"))
        nums = list(range(lo, hi + 1))
    else:
        nums = sorted(
            int(p.stem.split("-")[1]) for p in pages_dir.glob("page-*.png")
        )

    for n in nums:
        page_png = pages_dir / f"page-{n:02d}.png"
        if not page_png.exists():
            print(f"skip page {n}: {page_png} missing", file=sys.stderr)
            continue
        hocr_stem = hocr_dir / f"page-{n:02d}"
        hocr_path = run_tesseract_hocr(page_png, hocr_stem)
        page_size, blocks = parse_hocr(hocr_path)
        layout_path = layout_dir / f"page-{n:02d}.json"
        write_layout(layout_path, page_size or (2480, 3507), blocks, page_png)
        print(f"page {n:02d}: {len(blocks)} text blocks → {layout_path.name}")


if __name__ == "__main__":
    main()
