"""Page 3 - the colour game-board sheet (Blockade + FALLGRUBE).

The same labels as the black-and-white boards on pages 10 and 37, printed in
colour on the loose insert. They are translated the same way, so the appendix
agrees with the pages that describe the games.

The sheet scanned 2464 px wide rather than 2480, which is why PageBuild now
derives px_per_mm from the image instead of assuming it.

Colours: the labels around the Blockade board are dark on white, so they take
the default white mask. The ZIEL letters are white on the red squares of the
FALLGRUBE grid, so each one takes the red of its own square. "START" and the
grid numbers read the same in English and are left as printed.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
from page_build import PageBuild

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN = np.asarray(Image.open(f"{ROOT}/pages/page-03.png").convert("RGB")).astype(int)


def field(box):
    """Median of the printed red inside `box`, ignoring the white letters and
    the black grid lines that bound it."""
    x0, y0, x1, y1 = box
    px = SCAN[y0:y1, x0:x1].reshape(-1, 3)
    keep = (px.max(1) > 100) & (px.min(1) < 195)
    px = px[keep]
    r, g, b = np.median(px, 0).astype(int)
    return f"#{r:02x}{g:02x}{b:02x}"


b = PageBuild(ROOT, 3, align=False)

# ---- Blockade board: lane and start labels -----------------------------
LBL = dict(fs=10.5, bold=False, lh=1.0)
b.heading([495, 596, 700, 652], "Track 1", **LBL)
b.heading([813, 944, 1030, 1002], "Track 2", **LBL)
b.heading([370, 872, 710, 922], "Computer start", **LBL)
b.heading([1881, 866, 2150, 916], "Player start", **LBL)

# ---- FALLGRUBE board: ZIEL -> GOAL, one letter per square --------------
# grid lines measured at x=512/652/792/932/1072, y=1340/1482; the boxes are the
# square interiors, inset 6 px so no rule is masked.
CELL = dict(fs=22.5, bold=True, center=True, lh=1.28, color="#ffffff")
for x0, x1, ch in ((518, 646, "G"), (658, 786, "O"),
                   (798, 926, "A"), (938, 1066, "L")):
    box = [x0, 1348, x1, 1476]
    b.heading(box, ch, mask=field(box), **CELL)

# ---- FALLGRUBE board: axis labels --------------------------------------
b.heading([1036, 2816, 1440, 2870], "1st entry = column", fs=9.1,
          bold=False, lh=1.0)

# reads bottom-to-top, as on page 37
b.raw([1998, 1786, 2068, 2314],
      '<div style="writing-mode:vertical-rl;transform:rotate(180deg);'
      'white-space:nowrap;text-align:center;width:100%;height:100%;'
      'font-family:Helvetica,Arial,sans-serif;color:#111;line-height:1;'
      'font-size:12.4pt">2nd entry = row</div>')
b.write()
