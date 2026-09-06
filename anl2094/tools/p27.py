import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 27)

b.heading([166,84,600,166], "Important:", fs=13)
b.heading([164,218,1210,280], "The computer has a built-in cheat check!", fs=11.5)

b.prose([160,306,1252,1282],
 "If, for instance, we move one of our pieces backwards, the game is broken off "
 "at once and the display shows: F01. A new program start must be made here with "
 "HALT &ndash; NEXT &ndash; 00 &ndash; RUN.<br><br>"
 "When entering new playing positions we should also make quite sure that only "
 "one of the three piece positions is changed per move. If the display shows, "
 "say, 496 and we want to move the piece from square 9 to square B, we have to "
 "enter 4B6. If we were to enter B46, two piece positions would have changed and "
 "the computer would likewise break off the game. (Display F01 = new program "
 "start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN.)", fs=10.6)

b.heading([152,2246,1290,2334],
    "Programmer: Markus Baumann, 6660 Zweibr&uuml;cken 16", fs=11, bold=False)
b.write()
