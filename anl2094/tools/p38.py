import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 38)

b.heading([110,364,700,440], "End of game:", fs=12.6)

b.prose([102,456,1212,1412],
 "The display shows: 66 F00 = all 3 pieces have fallen into a pitfall, none has "
 "reached the GOAL. New game start: HALT &ndash; NEXT &ndash; 00 &ndash; "
 "RUN.<br><br>"
 "The display shows: 1000 (or 2000 or 3000) = one piece (or 2 or 3 pieces) has "
 "arrived safely at the GOAL. The game is over, no further playing pieces are "
 "available. New game start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN.", fs=10.6)

b.heading([94,2228,1092,2326],
    "Programmer: Frank Simon, 6342 Haiger 6", fs=11, bold=False)
b.write()
