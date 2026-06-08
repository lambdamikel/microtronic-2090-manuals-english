#!/usr/bin/env python3
"""
Generate overlay HTML for one or more pages.

Input per page:
  layout/page-NN.json              ← bboxes + kind (body/title/label/noise)
  translations/page-NN.en.json     ← English text keyed by block index

Output:
  pages-html/page-NN.html
  (or, with --combine, one consolidated HTML for the whole batch)

The translation JSON looks like:
{
  "0":  { "en": "Ready for the First Test Run!" },          # title
  "1":  { "en": "First, we plug the power supply..." },     # body
  ...
}

Untranslated body blocks fall back to a placeholder so we can see what's
still pending.
"""
import argparse, json
from pathlib import Path

PAGE_CSS = """
:root { --ink: #111; }
html, body { margin:0; padding:0; background:#555;
  font-family:"Helvetica Neue", Helvetica, Arial, sans-serif; color:var(--ink); }
.page {
  width:210mm; height:297mm;
  position:relative; background:#fff;
  margin:12mm auto; box-shadow:0 2px 8px rgba(0,0,0,.4);
  overflow:hidden;
}
.page > img.bg { position:absolute; inset:0; width:100%; height:100%; display:block; z-index:0; }
.mask { position:absolute; background:#fff; z-index:1; }
.ovr  { position:absolute; z-index:2; color:var(--ink); }
.ovr.title h2 { margin:0; font-size:13pt; font-weight:700; line-height:1.1; }
.ovr.body p   { margin:0 0 1.2mm; font-size:9pt; line-height:1.18; text-align:justify; }
.ovr.body p:last-child { margin-bottom:0; }
.ovr.body ul, .ovr.body ol { margin:0 0 1.2mm 4mm; padding:0; font-size:9pt; line-height:1.2; }
.ovr.body li { margin-bottom:.3mm; }
.ovr.body table { border-collapse:collapse; margin:.5mm 0 1.5mm; font-size:9pt; line-height:1.2; }
.ovr.body th, .ovr.body td { padding:.2mm 1.2mm .2mm 0; vertical-align:top; text-align:left; }
.ovr.body th { font-weight:700; border-bottom:.2mm solid #888; padding-right:2mm; }
.ovr.body table.codes { font-family:"Courier New", monospace; font-size:8.5pt; line-height:1.25; }
.ovr.body table.codes td:first-child { font-weight:700; white-space:nowrap; padding-right:3mm; }
.ovr.body table.codes td:nth-child(2) { white-space:nowrap; padding-right:3mm; }
.ovr.body table.hexgrid { font-family:"Courier New", monospace; font-size:6.5pt; line-height:1.0;
  border-collapse:collapse; width:100%; }
.ovr.body table.hexgrid th, .ovr.body table.hexgrid td {
  padding:.1mm .8mm .1mm 0; text-align:right; white-space:nowrap;
  border:none;
}
.ovr.body table.hexgrid th { font-weight:700; border-bottom:.15mm solid #888; }
.ovr.body table.hexgrid td { font-weight:normal; }
.ovr.body table.boxed { width:100%; border:.35mm solid #111; border-collapse:collapse; }
.ovr.body table.boxed th, .ovr.body table.boxed td {
  border:.25mm solid #111; padding:.6mm 1.4mm;
}
.ovr.body table.boxed th { background:#f0f0f0; }
/* Hex/decimal -> binary (LED outputs) reference table. */
.ovr.body table.hexbin { border-collapse:collapse; font-family:"Courier New", monospace;
  font-size:8pt; line-height:1.05; margin:.4mm 0; }
.ovr.body table.hexbin th, .ovr.body table.hexbin td {
  border:.2mm solid #111; padding:.22mm 2.2mm; text-align:center; }
.ovr.body table.hexbin th { background:#f0f0f0; font-weight:700; white-space:nowrap; }
.ovr.body table.hexbin td:first-child, .ovr.body table.hexbin th:first-child { font-weight:700; }
.ovr.body table.hexbin tr.decend td { border-bottom:.5mm solid #111; }
.ovr.body .hexnote { font-size:8pt; font-style:italic; margin:1mm 0 0; }
/* Six-column program listing (label / addr / code / mnem / jump / explanation). */
.ovr.body table.timer { width:100%; border-collapse:collapse;
  font-family:"Helvetica Neue", Arial, sans-serif; font-size:8.6pt; line-height:1.14; }
.ovr.body table.timer th, .ovr.body table.timer td {
  border:.18mm solid #111; padding:.45mm 1.2mm; vertical-align:top; text-align:left; }
.ovr.body table.timer th { background:#f0f0f0; font-weight:700; }
.ovr.body table.timer td.a { font-family:"Courier New", monospace; font-weight:700;
  text-align:center; white-space:nowrap; }
.ovr.body table.timer td.c { font-family:"Courier New", monospace; font-weight:700; white-space:nowrap; }
.ovr.body table.timer td.m { font-family:"Courier New", monospace; white-space:nowrap; }
.ovr.body table.timer td.lbl, .ovr.body table.timer td.jmp {
  font-weight:700; white-space:nowrap; text-align:center; }
/* Dense full-program listing: many rows must fit a tall column. */
.ovr.body table.codes.lst { width:100%; table-layout:auto; font-size:8.5pt; line-height:1.18; }
.ovr.body table.codes.lst th, .ovr.body table.codes.lst td { padding:.34mm 1.1mm; white-space:nowrap; }
.ovr.body table.codes.lst td:first-child,
.ovr.body table.codes.lst th:first-child { padding-right:1.4mm; }
.ovr.body table.codes.lst td:nth-child(2),
.ovr.body table.codes.lst td:nth-child(3) { padding-right:1.4mm; }
.ovr.body table.codes.lst td:last-child,
.ovr.body table.codes.lst th:last-child { width:46%; white-space:normal; }
/* Step-by-step calculation table (decimal/hex/binary worked example). */
.ovr.body table.calc { width:100%; border-collapse:collapse; font-size:8pt; line-height:1.15; }
.ovr.body table.calc th, .ovr.body table.calc td {
  border:.18mm solid #111; padding:.4mm 1.4mm; vertical-align:top; text-align:left; }
.ovr.body table.calc th { background:#f0f0f0; font-weight:700; }
.ovr.body table.calc td.hx { font-family:"Courier New", monospace; white-space:nowrap; }
.led { display:inline-block; font-family:"Courier New", monospace; font-weight:700;
  background:#111; color:#f33; padding:0 .7mm; border-radius:.5mm; letter-spacing:.15mm; }
.todo { color:#a00; font-style:italic; opacity:.5; }
@page { size:A4; margin:0; }
@media print {
  html, body { background:#fff; }
  .page { margin:0; box-shadow:none; width:210mm; height:296mm;
    page-break-after:always; break-after:page;
    -webkit-print-color-adjust:exact; print-color-adjust:exact; }
  .page:last-child { page-break-after:auto; break-after:auto; }
}
"""

# Mask padding around each text bbox in mm so we cover descenders / kerning bleed.
PAD_MM = {"body": 1.2, "title": 1.5}


def px_to_mm(px, ppm):
    return px / ppm


def _mask_div(bbox, ppm, pad_mm):
    x = px_to_mm(bbox[0], ppm) - pad_mm
    y = px_to_mm(bbox[1], ppm) - pad_mm
    w = px_to_mm(bbox[2] - bbox[0], ppm) + 2 * pad_mm
    h = px_to_mm(bbox[3] - bbox[1], ppm) + 2 * pad_mm
    return (
        f'  <div class="mask" '
        f'style="left:{x:.2f}mm;top:{y:.2f}mm;width:{w:.2f}mm;height:{h:.2f}mm"></div>'
    )


def _column_width_for_title(title_bbox, blocks):
    """Find the body/table block immediately below the title that overlaps the
    title's x-range. Returns (x0, x1, gap_px) where gap_px is the vertical gap
    to that block (used to decide whether a 2-line title would collide), or
    None if there's nothing below."""
    tx0, ty0, tx1, ty1 = title_bbox
    candidates = []
    for b in blocks:
        if b["kind"] not in ("body", "title"):
            continue
        bx0, by0, bx1, by1 = b["bbox"]
        if by0 < ty1:           # must be below the title
            continue
        if bx1 < tx0 or bx0 > tx1:
            continue
        candidates.append((by0 - ty1, bx0, bx1))
    if not candidates:
        return None
    candidates.sort()
    gap, bx0, bx1 = candidates[0]
    return (bx0, bx1, gap)


def render_page(page_idx, layout, en_map, bg_rel_path):
    ppm = layout["px_per_mm"]
    blocks = layout["text_blocks"]
    parts = []
    parts.append(f'<section class="page" data-page="{page_idx}">')
    parts.append(f'  <img class="bg" src="{bg_rel_path}" alt="">')

    # Build mask + overlay only for blocks that have a non-empty English entry.
    # If en is empty, the block is left in German (useful for figure annotations
    # the user chose not to translate).
    #
    # Masking strategy: by default we lay ONE opaque rectangle over the full
    # block bbox. This reliably wipes everything underneath — German text, table
    # grid lines, box borders — so the English overlay sits on a clean white
    # surface. A block can opt into finer line-level masking by setting
    # "mask_lines": true in its layout entry (useful when there's a figure
    # sitting inside the text region that we want to keep visible).
    for i, b in enumerate(blocks):
        if b["kind"] not in ("body", "title"):
            continue
        en = (en_map.get(str(i)) or {}).get("en")
        if not en:
            continue

        pad = PAD_MM[b["kind"]]
        if b.get("mask_lines"):
            units = b.get("lines") or b.get("fragments") or [b["bbox"]]
        else:
            # default: one big rectangle covering the whole block area, plus
            # any extra fragments the layout JSON adds explicitly.
            units = [b["bbox"]] + list(b.get("extra_masks", []))
        for f in units:
            parts.append(_mask_div(f, ppm, pad))

        bb = b["bbox"]
        x = px_to_mm(bb[0], ppm)
        y = px_to_mm(bb[1], ppm)
        w = px_to_mm(bb[2] - bb[0], ppm)
        h = px_to_mm(bb[3] - bb[1], ppm)
        cls = b["kind"]
        if cls == "title":
            # English may be slightly wider than the German ink bbox — stretch
            # the overlay to the underlying column width when we can find it.
            col = _column_width_for_title(bb, blocks)
            gap_mm = 999.0
            if col:
                x = px_to_mm(col[0], ppm)
                w = px_to_mm(col[1] - col[0], ppm)
                gap_mm = px_to_mm(col[2], ppm)
            # A title that's too wide for one line at 13pt was typeset on two
            # lines (breaking after ":" or an em-dash). But if there isn't room
            # below for a 2nd line (the block beneath sits within ~12 mm), break
            # would collide — so instead shrink the font to keep it on one line.
            # ~2.5mm/char at 13pt for the bold title face (calibrated).
            capacity = max(1, int(w / 2.0))
            overflows = len(en) > capacity and "<br>" not in en and "\n" not in en
            one_line = b.get("one_line") or (overflows and gap_mm < 12.0)
            h2_style = ""
            if one_line:
                est_mm = len(en) * 2.5
                if est_mm > w:
                    fs = max(8.0, 13.0 * w / est_mm)
                    h2_style = f' style="font-size:{fs:.1f}pt;white-space:nowrap"'
                else:
                    h2_style = ' style="white-space:nowrap"'
            elif overflows:
                if ": " in en:
                    en = en.replace(": ", ":<br>", 1)
                elif " — " in en:
                    en = en.replace(" — ", " —<br>", 1)
                elif " -- " in en:
                    en = en.replace(" -- ", " —<br>", 1)
            inner = f"<h2{h2_style}>{en}</h2>"
            style = f"left:{x:.2f}mm;top:{y:.2f}mm;width:{w:.2f}mm"
        else:
            block_starts = ("<ol", "<ul", "<table", "<div", "<h", "<pre", "<blockquote")
            # Per-block table font override (set by the auto-fit tool): inject an
            # inline font-size onto the table element so it overrides the class.
            font_pt = b.get("font_pt")
            paragraphs = []
            for p in en.split("\n\n"):
                p = p.strip()
                if not p:
                    continue
                if font_pt and p.lower().startswith("<table"):
                    p = p.replace("<table", f'<table style="font-size:{font_pt}pt"', 1)
                if p.lower().startswith(block_starts):
                    paragraphs.append(p)  # block-level — render as-is
                else:
                    paragraphs.append(f"<p>{p}</p>")
            inner = "\n    ".join(paragraphs) or f"<p>{en}</p>"
            style = (
                f"left:{x:.2f}mm;top:{y:.2f}mm;"
                f"width:{w:.2f}mm;height:{h:.2f}mm"
            )
        parts.append(
            f'  <div class="ovr {cls}" '
            f'style="{style}">\n'
            f"    {inner}\n"
            f"  </div>"
        )

    parts.append("</section>")
    return "\n".join(parts)


def make_template(layout):
    out = {}
    for i, b in enumerate(layout["text_blocks"]):
        if b["kind"] in ("body", "title"):
            out[str(i)] = {"de": b["text"], "en": ""}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--pages", required=True, help="e.g. 1-8 or 5,7,8")
    ap.add_argument("--out", required=True, help="output HTML path")
    ap.add_argument(
        "--make-templates",
        action="store_true",
        help="Write translations/page-NN.en.json templates for missing pages",
    )
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if "-" in args.pages:
        lo, hi = (int(x) for x in args.pages.split("-"))
        page_nums = list(range(lo, hi + 1))
    else:
        page_nums = [int(x) for x in args.pages.split(",")]

    translations_dir = root / "translations"
    translations_dir.mkdir(exist_ok=True)

    sections = []
    for n in page_nums:
        layout_path = root / "layout" / f"page-{n:02d}.json"
        if not layout_path.exists():
            print(f"⚠ skip page {n}: no layout/{layout_path.name}")
            continue
        layout = json.loads(layout_path.read_text())
        en_path = translations_dir / f"page-{n:02d}.en.json"
        if args.make_templates and not en_path.exists():
            tmpl = make_template(layout)
            en_path.write_text(json.dumps(tmpl, indent=2, ensure_ascii=False))
            print(f"+ wrote template {en_path.name}")
        en_map = json.loads(en_path.read_text()) if en_path.exists() else {}
        bg_rel = f"anl2090-1/pages/page-{n:02d}.png"
        sections.append(render_page(n, layout, en_map, bg_rel))

    out_path = Path(args.out)
    out_path.write_text(
        "<!doctype html>\n<html><head><meta charset='utf-8'>"
        f"<title>Microtronic 2090 — pages {args.pages}</title>"
        f"<style>{PAGE_CSS}</style></head><body>\n"
        + "\n".join(sections)
        + "\n</body></html>\n"
    )
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
