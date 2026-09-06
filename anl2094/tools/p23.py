import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 23)

# figure caption (box widened to the right - verified blank - so the longer
# English caption keeps the German's ~10 pt size instead of shrinking to 8)
b.heading([172,1536,1500,1630],
    "(Fig. El. Studio 2060/65 built into the MICROTRONIC housing)",
    fs=10.0, bold=False)

b.prose([170,1788,1288,2316],
 "To do this the instruction at address 10 has to be changed (F02 to F1D).<br><br>"
 "Entry: HALT &ndash; NEXT &ndash; 10 &nbsp; F1D &ndash; NEXT.<br><br>"
 "New program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN.<br><br>"
 "In addition to playing the tone, the display now also shows the "
 "corresponding key to be pressed.", fs=10.6)
b.write()
