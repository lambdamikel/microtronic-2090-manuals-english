"""Page 64 (printed 61) - the exponentiation flow chart.

Every label sits inside a drawn shape (diamond, box, parallelogram) or beside an
arrow, so each white-out has to stay clear of the outline. The marked boxes are
tight around the German, which is what we want here: the shapes are fixed and
the English must fit the same room, not more.

Two notes:
  * "START" is the same word in English, so the terminator is left as drawn.
  * The lower "Nein" (below the second diamond) was not marked. It is the twin
    of the marked one at y=946 and would otherwise have been the only German
    word left in the chart, so it is placed here at its measured position
    [442,1230,538,1272].
"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 64, align=False)   # scattered chart labels: no column snap

b.heading([320,378,554,450], "Flow chart", fs=11.5, bold=False)

# first decision: "Hochzahl / =0?"  - only the word is marked, "=0?" stays
b.heading([344,788,520,844], "Exponent", fs=9.9, bold=False)
b.heading([572,780,658,822], "Yes", fs=8.8, bold=False)
b.heading([828,774,1030,878], "Result<br>=1", fs=9.9, bold=False,
          nowrap=False, lh=1.15)
b.heading([444,946,540,988], "No", fs=9.9, bold=False)

# second decision: "Hochzahl / =1?"
b.heading([338,1080,522,1126], "Exponent", fs=9.9, bold=False)
b.heading([586,1068,644,1110], "Yes", fs=8.8, bold=False)
b.heading([824,1064,1024,1172], "Result<br>found", fs=9.9, bold=False,
          nowrap=False, lh=1.15)
b.heading([442,1230,538,1272], "No", fs=10.5, bold=False)   # not marked; measured

b.heading([242,1316,628,1532],
    "Multiply the base by itself, or by the result of the last calculation",
    fs=9.6, bold=False, nowrap=False, lh=1.28)

b.heading([296,1658,564,1728], "Exponent &ndash; 1", fs=9.9, bold=False)
b.write()
