#!/usr/bin/env python3
"""
Render a debug visualization of layout extraction.

Reads layout/page-NN.json and overlays color-coded bboxes on a thumbnail
of the page so we can sanity-check classification before generating overlay
HTML.

Colors:
  body  → blue
  title → green
  label → orange
  noise → red (dashed)
"""
import argparse, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

COLORS = {
    "body":  (40, 90, 220, 200),
    "title": (40, 160, 60, 220),
    "label": (230, 140, 30, 200),
    "noise": (220, 40, 40, 160),
}


def render(page_png: Path, layout_json: Path, out_png: Path, scale: float = 0.4):
    layout = json.loads(layout_json.read_text())
    img = Image.open(page_png).convert("RGB")
    # Scale down for legibility
    w, h = img.size
    nw, nh = int(w * scale), int(h * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    overlay = Image.new("RGBA", (nw, nh), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except OSError:
        font = ImageFont.load_default()

    for b in layout["text_blocks"]:
        bb = b["bbox"]
        kind = b.get("kind", "label")
        color = COLORS.get(kind, (128, 128, 128, 200))
        x0, y0, x1, y1 = (int(c * scale) for c in bb)
        if kind == "noise":
            # dashed
            for y in range(y0, y1, 6):
                draw.line([x0, y, x0, min(y + 3, y1)], fill=color, width=2)
                draw.line([x1, y, x1, min(y + 3, y1)], fill=color, width=2)
            for x in range(x0, x1, 6):
                draw.line([x, y0, min(x + 3, x1), y0], fill=color, width=2)
                draw.line([x, y1, min(x + 3, x1), y1], fill=color, width=2)
        else:
            draw.rectangle([x0, y0, x1, y1], outline=color, width=3)
        label = f"{kind}"
        draw.rectangle([x0, y0, x0 + 60, y0 + 18], fill=color)
        draw.text((x0 + 3, y0 + 1), label, fill=(255, 255, 255), font=font)

    out = Image.alpha_composite(img.convert("RGBA"), overlay)
    out.convert("RGB").save(out_png, "PNG")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--page", type=int, required=True)
    ap.add_argument("--scale", type=float, default=0.4)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    n = args.page
    page_png = root / "pages" / f"page-{n:02d}.png"
    layout_json = root / "layout" / f"page-{n:02d}.json"
    out_png = Path(args.out) if args.out else root / "layout" / f"page-{n:02d}-debug.png"
    render(page_png, layout_json, out_png, args.scale)
    print(f"wrote {out_png}")


if __name__ == "__main__":
    main()
