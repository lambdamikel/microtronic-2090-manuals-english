import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 30)

b.prose([104,374,1206,1052],
 "For experts who would like to shorten the reaction time from two seconds to "
 "one, the instruction code 527 at address 15 can be changed to 517 in the "
 "program. Entry: HALT &ndash; NEXT &ndash; 15 &nbsp; 517 &ndash; NEXT. New "
 "program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN.<br><br>"
 "Besides fast reactions, a little luck will now also be needed for an "
 "accident-free car race.<br><br>"
 "For fast reactions it is a good idea to cover the computer's keypad with the "
 "white keypad mask (see the accessories enclosed) and to label it as shown "
 "below:", fs=10.6)

# ---- keypad-mask legend ------------------------------------------------
LBL = dict(fs=10.0, bold=False)
b.heading([110,1176, 274,1252], "3 left",  **LBL)   # left of the keypad
b.heading([112,1280, 274,1348], "2 left",  **LBL)
b.heading([110,1376, 272,1452], "1 left",  **LBL)
b.heading([1018,1180,1240,1248], "3 right", **LBL)  # right of the keypad
b.heading([1012,1276,1240,1330], "2 right", **LBL)
b.heading([1010,1370,1240,1434], "1 right", **LBL)
b.heading([650,1496, 1000,1564], "straight", **LBL) # under the "2" key

b.heading([102,2218,1122,2348],
    "Programmer: K.-T. Eggert, 2117 Tostedt", fs=11, bold=False)
b.write()
