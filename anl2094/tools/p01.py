"""Page 1 - the front cover.

Unlike every other page in this book the cover prints white text on a red
field, so the pipeline's default white mask would punch holes in the artwork.
Each mask therefore takes the colour of the red around it, sampled from the
scan (the red is a scan of print, so it is not perfectly flat and drifts a
little across the sheet).

Two further differences:
  * the left-hand list is right-aligned, so it is laid out as one masked block
    with the lines set over it - thirteen separate masks would show as banding.
  * the big "computer spiele" logotype is left exactly as printed. It is drawn
    in a 1970s rounded display face that nothing on this machine can match, and
    setting "games" in Helvetica beside that "computer" would look worse than
    leaving it. Same reasoning as FALLGRUBE and the START terminator.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
from page_build import PageBuild

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN = np.asarray(Image.open(f"{ROOT}/pages/page-01.png").convert("RGB")).astype(int)


def bg(box, pad=18):
    """Median colour of the ring just outside `box`, as #rrggbb."""
    x0, y0, x1, y1 = box
    h, w, _ = SCAN.shape
    outer = SCAN[max(0, y0 - pad):min(h, y1 + pad), max(0, x0 - pad):min(w, x1 + pad)]
    inner = SCAN[y0:y1, x0:x1]
    ring = np.concatenate([outer.reshape(-1, 3),
                           np.repeat(inner.reshape(-1, 3), 0, axis=0)])
    # drop the text itself: keep only pixels that are not near-white
    ring = ring[~((ring[:, 0] > 195) & (ring[:, 1] > 195) & (ring[:, 2] > 195))]
    if len(ring) == 0:
        return "#ffffff"
    r, g, b = np.median(ring, 0).astype(int)
    return f"#{r:02x}{g:02x}{b:02x}"


b = PageBuild(ROOT, 1, align=False, ink="#ffffff", crop=(21, 18, 7, 35))

# ---- left-hand teaser list (white, right-aligned on red) ----------------
LIST = [1005, 2005]                      # the block the German list occupies
LX, RX = 128, 891                        # left margin / common right edge
b.raw([LX, LIST[0], RX, LIST[1]], "<div></div>", mask=bg([LX, LIST[0], RX, LIST[1]]))

ROWS = [1018, 1097, 1172, 1251, 1331, 1411, 1490,
        1570, 1650, 1731, 1811, 1873, 1953]
ITEMS = [
    "Strategy and puzzle games",
    "Games of chance and patience",
    "17+4",
    "Reaction games",
    "Number Avalanche",
    "One-Armed Bandit",
    "Chess Clock",
    "Code Lock",
    "Clock with chimes",
    "World Time Calculation",
    "Prime number and",
    "exponentiation calculations",
    ". . . and much more.",
]
for y, txt in zip(ROWS, ITEMS):
    b.heading([LX, y, RX, y + 56], txt, fs=12.0, bold=True, right=True,
              whiteout=False, lh=1.0)

# ---- picture captions --------------------------------------------------
# "Black Jack", "Roulette" and "Blockade" read the same in English and are left
# as printed; "Fallgrube" keeps its German name, as it does on its own page.
# The masks stop at y=1412: the white picture panels end at y~1406.
CAP = dict(fs=12.0, bold=True, center=True, lh=1.0)
for box, txt in (([1418, 1412, 1800, 1495], "Sound Memory"),
                 ([1872, 1412, 2228, 1495], "Car Race")):
    b.heading(box, txt, mask=bg(box), **CAP)

# ---- strapline ---------------------------------------------------------
# One mask for both lines. Measured tight, the German's ascenders (y=2207) and
# descenders (y=2349) fall outside the two ink boxes and ghost through.
STRAP = [110, 2192, 1900, 2362]
b.raw(STRAP, "<div></div>", mask=bg(STRAP))
for box, txt in (([120, 2205, 1106, 2280], "25 games and experiments"),
                 ([120, 2283, 1860, 2358],
                  "to program yourself for Microtronic 2090")):
    b.heading(box, txt, fs=17.4, bold=True, whiteout=False, lh=1.0)

# ---- order number (black text, also on the red) ------------------------
ORD = [1930, 2350, 2330, 2410]
b.heading(ORD, "Order no. 2094", fs=11.5, bold=False, color="#111",
          mask=bg(ORD), lh=1.0)
b.write()
