import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 10, align=False)   # free-floating diagram labels: no column snap

L = dict(fs=7.2, bold=False)   # small diagram labels (~7 pt in the original)
b.heading([223,402, 400,442], "Track 1",        **L)   # room to the right, verified blank
b.heading([149,554, 362,614], "Computer start", **L)
b.heading([401,605, 620,642], "Track 2",        **L)
b.heading([1019,551,1181,595], "Player start",  **L)   # frame at x~1190: keep inside
b.write()
