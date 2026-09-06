#!/usr/bin/env python3
"""
Render anl2094.pdf to straight, 300 dpi page images for the overlay pipeline.

    tools/deskew_pages.py ../../Busch-2090/manuals/anl2094.pdf

The 2094 scan is skewed, unlike the 2090 ones: sheets tilt by up to 2.7 deg,
with the sign alternating between consecutive pages - the signature of a book
flipped on the platen. That matters because the English overlay masks German
text with axis-aligned white boxes. Over a 1000 px text block a 2.7 deg tilt
drifts about 47 px vertically, several line heights, so a mask that covers the
German at one end leaves it showing at the other.

Skew is estimated by projection profile: rotate through candidate angles and
keep the one where the horizontal ink profile has the sharpest row-to-row
transitions, which is when text lines sit square on the pixel rows. Coarse pass
at 0.5 deg, refined at 0.1 deg.

Angles are written to pages/deskew.json so a re-run reproduces the same output,
and so a page can be corrected by hand if the estimate is ever wrong.
"""
import argparse, json, subprocess, sys
from pathlib import Path
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
DPI = 300
COARSE, FINE, LIMIT = 0.5, 0.1, 4.0

def ink(im, width=800):
    """Downscaled binary ink mask - estimation does not need full resolution."""
    g = im.convert('L')
    g = g.resize((width, max(1, int(g.height * width / g.width))), Image.BILINEAR)
    return (np.asarray(g, dtype=np.float32) < 160).astype(np.float32)

def sharpness(mask, angle):
    im = Image.fromarray((mask * 255).astype(np.uint8))
    if angle:
        im = im.rotate(angle, resample=Image.BILINEAR, fillcolor=0)
    prof = np.asarray(im, dtype=np.float32).sum(axis=1) / 255.0
    return float(((prof[1:] - prof[:-1]) ** 2).sum())

def estimate(im, min_ink=500):
    mask = ink(im)
    if mask.sum() < min_ink:
        return 0.0                      # blank or near-blank: leave alone
    best, angle = -1.0, 0.0
    for a in np.arange(-LIMIT, LIMIT + 1e-9, COARSE):
        s = sharpness(mask, a)
        if s > best:
            best, angle = s, a
    for a in np.arange(angle - COARSE, angle + COARSE + 1e-9, FINE):
        s = sharpness(mask, a)
        if s > best:
            best, angle = s, a
    return round(float(angle), 2)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf')
    ap.add_argument('--out', default='pages')
    ap.add_argument('--dpi', type=int, default=DPI)
    ap.add_argument('--force', action='store_true', help='re-render even if pages exist')
    a = ap.parse_args()

    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    raw = out / '_raw'; raw.mkdir(exist_ok=True)

    if a.force or not any(raw.glob('raw-*.png')):
        print(f"rendering {a.pdf} at {a.dpi} dpi ...", flush=True)
        subprocess.run(['pdftoppm', '-r', str(a.dpi), '-png', a.pdf, str(raw / 'raw')],
                       check=True)

    angles = {}
    for src in sorted(raw.glob('raw-*.png')):
        n = int(src.stem.split('-')[-1])
        im = Image.open(src)
        ang = estimate(im)
        if ang:
            im = im.rotate(ang, resample=Image.BICUBIC, fillcolor='white', expand=False)
        dst = out / f"page-{n:02d}.png"
        im.save(dst)
        angles[dst.name] = ang
        print(f"  {dst.name}  {ang:+.2f} deg", flush=True)

    (out / 'deskew.json').write_text(json.dumps(angles, indent=2) + '\n')
    nz = [v for v in angles.values() if v]
    print(f"\n{len(angles)} pages, {len(nz)} corrected, "
          f"largest {max((abs(v) for v in nz), default=0):.2f} deg")

if __name__ == '__main__':
    main()
