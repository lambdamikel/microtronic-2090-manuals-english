import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 59)

b.heading([154,70,992,214], "For mathematicians: a super division program",
          fs=14.0, nowrap=False, lh=1.15)

b.prose([150,378,1250,862],
 "This big division program shows how MICROTRONIC can carry out complicated "
 "calculations too with a simple algorithm, for example division problems with "
 "any number of decimal places.<br><br>"
 "Example: 787 : 63 = 12.4920634920634920... With this problem MICROTRONIC will "
 "go on calculating and displaying decimal places until the program is broken "
 "off.", fs=10.6)

b.heading([156,904,1150,972], "Function description:", fs=12.6)

b.prose([154,992,1240,1372],
 "After HALT &ndash; NEXT &ndash; 00 enter the program as per the table.<br><br>"
 "Program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN.<br><br>"
 "The display shows: A0. The computer now offers three different "
 "possibilities.", fs=10.6)

b.heading([158,1386,654,1452], "First possibility:", fs=12.6)

b.prose([154,1474,1244,2154],
 "Calculation of three decimal places, the last place being rounded up or down "
 "automatically. This possibility is selected with key 1. The display shows: "
 "000.<br><br>"
 "Now the divisor (three places at most) is entered (e.g. 787). The entry is "
 "completed by pressing key A. Then the dividend (e.g. 63) is entered. This "
 "entry too must be completed with key A. The computer now calculates the "
 "division 787 : 63. The result before the decimal point appears on the display: "
 "12. Pressing key 0 shows the three decimal places: 492. The complete result is "
 "therefore 12.49. A new program start is made with key 0.", fs=10.6)

# ---- right column ------------------------------------------------------
b.heading([1290,378,2250,460], "Second possibility:", fs=12.6)

b.prose([1290,468,2380,1128],
 "Calculation of any number of decimal places. Four places are shown at a time. "
 "Pressing key 0 brings the next four places, and so on. The display shows: A0. "
 "Select this program run with key 2. Then enter the divisor and dividend. "
 "(Example 14 : 973 = entry: 14 then key A, then entry: 973 and key A "
 "again.)<br><br>"
 "The display first shows the result before the decimal point (0). If key 0 is "
 "pressed, the first four decimal places are shown (0143). After each press of "
 "key 0 the next four places appear. Complete result for this example: "
 "0.01438848... The calculation of further decimal places can be broken off with "
 "key F.", fs=10.6)

b.heading([1278,1148,1702,1220], "Third possibility:", fs=12.6)

b.prose([1278,1238,2366,2048],
 "Calculation of any number of decimal places, four places always being shown "
 "one after the other automatically. The display shows: A0. Select this program "
 "run with key 3.<br><br>"
 "After entering the numbers (do not forget key A) the result before the decimal "
 "point is shown first. With key 0 four decimal places are shown for a short "
 "time. The next four places follow automatically, and so on. The program is "
 "broken off and at the same time restarted with HALT &ndash; NEXT &ndash; 00 "
 "&ndash; RUN.", fs=10.6)
b.write()
