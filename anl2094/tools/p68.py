"""Page 68 - the back cover (the Cassette Interface 2095 advertisement).

White text on red, like the front cover, so every mask takes its colour from
the scan rather than the pipeline's default white. See p01.py.

The "cassetten interface 2095" logotype is left as printed: it is set in the
same italic display face as the "microtronic" masthead above it and names the
product, so it is artwork rather than running text.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
from page_build import PageBuild

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN = np.asarray(Image.open(f"{ROOT}/pages/page-68.png").convert("RGB")).astype(int)


def bg(box, pad=18):
    """Median colour of the ring just outside `box`, as #rrggbb."""
    x0, y0, x1, y1 = box
    h, w, _ = SCAN.shape
    ring = SCAN[max(0, y0 - pad):min(h, y1 + pad),
                max(0, x0 - pad):min(w, x1 + pad)].reshape(-1, 3)
    ring = ring[~((ring[:, 0] > 195) & (ring[:, 1] > 195) & (ring[:, 2] > 195))]
    if len(ring) == 0:
        return "#ffffff"
    r, g, b = np.median(ring, 0).astype(int)
    return f"#{r:02x}{g:02x}{b:02x}"


b = PageBuild(ROOT, 68, align=False, ink="#ffffff", crop=(15, 14, 6, 32))

# caption beside the photograph
ERG = [150, 1235, 700, 1310]
b.heading(ERG, "Add-on for 2090", fs=12.5, bold=True, mask=bg(ERG), lh=1.0)

# ---- right-hand copy ---------------------------------------------------
# The photograph ends at x~1497 and the text starts at 1520, so the masks
# begin at 1505.
BODY = dict(fs=12.0, lh=1.06, justify=False)
for box, txt in (
    ([1505, 1310, 2400, 1435],
     "Ready-to-use plug-in module for easy installation."),
    ([1505, 1440, 2400, 1625],
     "For transferring (saving) computer programs onto cassettes or tape."),
    ([1505, 1630, 2400, 2182],
     "The digital computer signals are recorded by ordinary cassette recorders "
     "or tape machines. Transfer time for a full Microtronic program memory "
     "(256 addresses) approx. 4 minutes. 12&ndash;14 large computer programs "
     "can be stored on one C60 cassette."),
    ([1505, 2187, 2400, 2360],
     "On playback the interface turns the audio signals back into digital "
     "computer signals."),
):
    b.prose(box, f"<b>{txt}</b>", mask=bg(box), **BODY)
b.write()
