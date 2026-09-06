import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 56)

b.heading([112,1462,1242,1624],
    "Additionally required: BUSCH Electronic Studio 2060 (or 2065 or 2070).",
    fs=11.5, nowrap=False, lh=1.2)

b.heading([106,1924,518,1990], "Important note!", fs=12.6)

b.prose([106,2002,1224,2504],
 "For telephone experiments, note that the Deutsche Bundespost forbids data "
 "transmission over its own telephone lines as a matter of principle, unless a "
 "corresponding application has been approved. Trials should therefore only be "
 "carried out with a house telephone system.", fs=10.6)

# circuit-diagram labels; "GND" is the same in English and is left as printed
b.heading([1304,852,1444,966], "Input 1", fs=9.5, bold=False, nowrap=False, lh=1.2)
b.write()
