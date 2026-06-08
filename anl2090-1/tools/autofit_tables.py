#!/usr/bin/env python3
"""
Auto-fit redrawn tables to their layout region.

For every body block whose English contains a <table>, binary-search a font
size so the rendered table fills its bbox region without overflowing past it.
The table is rendered IN ISOLATION (only that table, at its real position and
width, on a blank A4) so its rendered bottom is unambiguous — no confounding
prose/figures below it. The chosen size is written back into the layout block
as "font_pt", which build_page_html injects as an inline style on the table.

Replaces the manual render-measure-tweak loop:

    python3 autofit_tables.py --root anl2090-1 --pages 33-40
"""
import argparse, json, subprocess, sys, tempfile
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
from build_page_html import PAGE_CSS, px_to_mm   # noqa: E402

SAFE_Y_PX = 3380
TARGET_LO, TARGET_HI = 0.90, 0.99      # desired fill fraction of the region
DARK = 135
DPI = 150


def _isolated_html(table_html, x_mm, y_mm, w_mm, font_pt):
    table_html = table_html.replace("<table", f'<table style="font-size:{font_pt}pt"', 1)
    return (
        f"<!doctype html><html><head><meta charset='utf-8'><style>{PAGE_CSS}</style>"
        f"</head><body><section class='page'>"
        f"<div class='ovr body' style='left:{x_mm:.2f}mm;top:{y_mm:.2f}mm;width:{w_mm:.2f}mm'>"
        f"{table_html}</div></section></body></html>"
    )


def _render_bottom_px(html, ppm, page_w=2480, page_h=3508):
    """Render the isolated HTML and return the lowest inked row in page-px."""
    with tempfile.TemporaryDirectory() as td:
        hp = Path(td) / "t.html"; hp.write_text(html, encoding="utf-8")
        pdf = Path(td) / "t.pdf"; stem = Path(td) / "t"
        subprocess.run(["google-chrome", "--headless", "--disable-gpu",
                        "--no-pdf-header-footer", "--no-margins",
                        f"--print-to-pdf={pdf}", hp.as_uri()],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["pdftocairo", "-png", "-r", str(DPI), "-f", "1", "-l", "1",
                        str(pdf), str(stem)], check=True, stdout=subprocess.DEVNULL)
        arr = np.asarray(Image.open(f"{stem}-1.png").convert("L"))
    rh, rw = arr.shape
    band = arr < DARK
    rows = np.where(band.sum(axis=1) > 2)[0]
    if len(rows) == 0:
        return None
    return int(rows[-1]) * (page_h / rh)


def fit_page(root, page_num):
    layout_path = root / "layout" / f"page-{page_num:02d}.json"
    layout = json.loads(layout_path.read_text())
    ppm = layout["px_per_mm"]
    en_path = root / "translations" / f"page-{page_num:02d}.en.json"
    en = json.loads(en_path.read_text()) if en_path.exists() else {}
    any_fit = False
    for i, b in enumerate(layout["text_blocks"]):
        if b.get("kind") != "body":
            continue
        html_en = (en.get(str(i)) or {}).get("en") or ""
        # Only fit blocks that ARE a table (optionally + a trailing caption),
        # not prose that happens to embed a small table mid-paragraph.
        if not html_en.strip().lower().startswith("<table"):
            continue
        bb = b["bbox"]
        x_mm, y_mm = px_to_mm(bb[0], ppm), px_to_mm(bb[1], ppm)
        w_mm = px_to_mm(bb[2] - bb[0], ppm)
        target = min(bb[3], SAFE_Y_PX)
        avail = target - bb[1]
        # take just the first table fragment of the en (ignore captions)
        table_html = html_en.split("\n\n")[0]
        lo, hi, best = 6.0, 11.5, None
        for _ in range(7):
            mid = round((lo + hi) / 2, 1)
            bottom = _render_bottom_px(_isolated_html(table_html, x_mm, y_mm, w_mm, mid), ppm)
            if bottom is None:
                break
            fill = (bottom - bb[1]) / max(1, avail)
            if bottom > target:
                hi = mid
            elif fill < TARGET_LO:
                lo = mid; best = mid
            else:
                best = mid; break
        chosen = best if best is not None else round((lo + hi) / 2, 1)
        b["font_pt"] = chosen
        any_fit = True
        print(f"  page {page_num} block {i}: font_pt={chosen}  region {bb[1]}..{target}")
    if any_fit:
        layout_path.write_text(json.dumps(layout, indent=2, ensure_ascii=False))
    return any_fit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="anl2090-1")
    ap.add_argument("--pages", required=True)
    args = ap.parse_args()
    root = Path(args.root).resolve()
    if "-" in args.pages:
        a, z = (int(x) for x in args.pages.split("-")); nums = range(a, z + 1)
    else:
        nums = [int(x) for x in args.pages.split(",")]
    for n in nums:
        fit_page(root, n)


if __name__ == "__main__":
    main()
