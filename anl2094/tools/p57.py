import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 57)

b.heading([154,58,1154,272], "For statisticians: drawing pie charts",
          fs=14.5, nowrap=False, lh=1.15)

b.prose([148,376,1236,868],
 "So-called &ldquo;pie charts&rdquo; are often used for the graphical "
 "presentation of tables or statistics. For this it is necessary to divide the "
 "percentage shares into &ldquo;slices&rdquo; of the right size (see "
 "illustration). The following program is a valuable aid in preparing pie charts "
 "for drawing. From the percentage values entered, the computer works out the "
 "angles in degrees for the corresponding sectors of the circle.", fs=10.6)

b.heading([146,900,736,986], "Function description:", fs=12.6)

b.prose([154,996,1246,1386],
 "After HALT &ndash; NEXT &ndash; 00 the program is entered according to the "
 "table.<br><br>"
 "Program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN.<br><br>"
 "The display shows: 00.", fs=10.6)

# ---- right column ------------------------------------------------------
b.heading([1282,372,1776,452], "Example of use:", fs=12.6)

b.prose([1286,456,2384,1160],
 "The proportions making up air are to be shown in a pie chart. Air consists of "
 "78% nitrogen, 21% oxygen and 1% noble gases. These percentages have to be "
 "converted into angles in degrees.<br><br>"
 "We enter the first percentage, for nitrogen (78). Then press key A. The "
 "display shows: 2808 = 280.8 degrees. Press key A. Enter the second value (21) "
 "for oxygen, press key A, the display shows 756 = 75.6 degrees. Key A, then the "
 "last entry for noble gases (1). Key A once more &ndash; display result: 36 "
 "(3.6 degrees).<br><br>"
 "With the values in degrees calculated by the computer, a pie chart with the "
 "corresponding sectors can easily be laid out and drawn:", fs=10.6)

# pie-chart callouts
PIE = dict(fs=10.0, bold=False)
b.heading([1290,1222,1590,1276], "78% nitrogen",   **PIE)
b.heading([2136,1374,2430,1428], "1% noble gas",   **PIE)
b.heading([2142,1442,2356,1502], "3.6&deg;",       **PIE)
b.heading([2052,1550,2364,1604], "21% oxygen",     **PIE)
b.heading([1850,1462,2050,1508], "75.6&deg;",      **PIE)
b.heading([1592,1400,1808,1450], "280.8&deg;",     **PIE)

b.prose([1274,1710,2386,2208],
 "In this way any number of divisions of the circle can be made. All you have to "
 "make sure of is that all the values of the circle's contents add up to 100% "
 "(as in our example 78% + 21% + 1%).<br><br>"
 "The way the program works is simple: the percentage entered is multiplied by "
 "3.6 and you get the result in degrees. The program demonstrates how an "
 "individually programmed computer can be used as an important aid for a wide "
 "variety of tasks.", fs=10.6)

b.heading([1274,2232,2386,2338],
    "Programmer: Thorsten Lindner, 5600 Wuppertal 2", fs=11, bold=False)
b.write()
