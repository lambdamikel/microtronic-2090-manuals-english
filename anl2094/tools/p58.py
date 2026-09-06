import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 58)

b.heading([132,70,1240,164], "Diagonal calculation for polygons", fs=14.5)

b.prose([126,376,1228,918],
 "With this program the computer works out how many ways there are of drawing "
 "diagonals into a polygon. It is well known, for example, that in a "
 "quadrilateral only two diagonals are possible, while in a pentagon there are "
 "already five different possibilities (see drawing). The program can calculate "
 "the number of diagonals of all polygons with up to a maximum of 99 corners.",
 fs=10.6)

b.heading([1270,376,2250,464], "Function description:", fs=12.6)

b.prose([1264,474,2354,1466],
 "After HALT &ndash; NEXT &ndash; 00 the program is entered as per the "
 "table.<br><br>"
 "Program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN.<br><br>"
 "The display shows: 00. Entry e.g.: 10 (for a decagon). Then press key A. The "
 "result is shown immediately as four digits (0035 in this example), that is, 35 "
 "diagonals are possible in a decagon.<br><br>"
 "If key A is then pressed, the display shows 00 again. A new number for a "
 "polygon can be entered.<br><br>"
 "The number of diagonals is calculated by the following formula:<br><br>"
 "d = (n &times; (n &ndash; 3)) : 2<br><br>"
 "d = number of diagonals<br>"
 "n = number of corners", fs=10.6)

b.heading([1256,2228,2256,2314],
    "Programmer: Peter Feltens, 5450 Neuwied 12", fs=11, bold=False)
b.write()
