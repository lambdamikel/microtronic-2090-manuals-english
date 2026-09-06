"""Page 4 - the inner title page.

Only the three-line subtitle needs translating; it is worded exactly as the
front cover's strapline, so the two match.

Left as printed: the "microtronic computer system" masthead and the "computer
spiele" logotype (display artwork, as on the cover), and the BUSCH postal
address, which is a company name and a German address.
"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 4, align=False)

b.prose([1253, 903, 1910, 1060],
        "25 games and experiments<br>to program yourself<br>"
        "for Microtronic 2090",
        fs=11.0, lh=1.10, justify=False)
b.write()
