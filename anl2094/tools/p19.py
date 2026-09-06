import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild, fit_fs
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 19)

b.heading([178,52,938,150], "MICROTRONIC Roulette", fs=15.5)
b.heading([172,1022,760,1096], "Function description:", fs=12.4)

b.prose([172,362,1256,1008],
 "As in the well-known game of roulette, you can bet on colours (red or black), on even or odd "
 "numbers, or on a particular number. Unlike ordinary roulette, MICROTRONIC roulette works with "
 "the numbers 0 &ndash; 256. This gives considerably more possibilities: you can also bet on the "
 "units, tens or hundreds digit of a number, for example. MICROTRONIC additionally acts as the "
 "bank, keeping the player's account automatically, debiting losses and crediting winnings to "
 "the starting capital. A starting capital of 10,000 play marks is available, to be increased by "
 "skilful betting.", fs=10.6)

b.prose([174,1116,1262,2122],
 "After HALT &ndash; NEXT &ndash; 00 the program is entered according to the table. The piezo "
 "buzzer is then connected to the output 1 and GND sockets.<br><br>"
 "Program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN.<br><br>"
 "The display goes dark briefly. The computer uses its random generator to pick a winning number "
 "between 0 and 256. At the same time it decides whether the number is red or black, and even or "
 "odd. The winning number is of course not revealed until the stake has been entered. For this "
 "the display shows: 0000. You now enter how many play marks are being staked, for example 200 "
 "(entry 200; maximum stake 9999). Then press key A. The display shows: A. One of six different "
 "betting options must be chosen and the corresponding key pressed according to the following "
 "table:", fs=10.6)

# ---- betting table: each cell is white-outed at its exact marked box, so the
#      printed grid lines around it are never touched. Text wraps inside.
CELL = dict(bold=False, center=False, nowrap=False, lh=1.05)
cells = [
 ([1326,394,1560,488],  "Betting option", True),
 ([1594,392,1704,468],  "Key",            True),
 ([1732,396,2076,482],  "further key press", True),
 ([2104,396,2348,486],  "Winnings",       True),
 ([1326,512,1570,620],  "Red/Black",      False),
 ([1322,682,1552,820],  "Even/Odd",       False),
 ([1320,886,1560,1040], "Directly on a number", False),
 ([1322,1096,1576,1206],"Hundreds digit", False),
 ([1324,1310,1578,1454],"Tens digit",     False),
 ([1316,1512,1580,1674],"Units digit",    False),
 ([1726,510,2070,656],  "Key 0 for red<br>Key 1 for black", False),
 ([1730,682,2060,860],  "Key 1 for even number<br>Key 2 for odd number", False),
 ([1728,890,2050,1068], "Enter the winning number; then key A", False),
 ([1728,1092,2052,1280],"Enter the 1st digit of the winning number (0, 1 or 2)", False),
 ([1728,1298,2056,1482],"Enter the 2nd digit of the winning number (0 to 9)", False),
 ([1724,1504,2074,1690],"Enter the 3rd digit of the winning number (0 to 9)", False),
 ([2106,518,2364,640],  "Stake is doubled", False),
 ([2102,684,2366,850],  "Stake is doubled", False),
 ([2100,890,2352,1052], "Stake &times; 300", False),
 ([2096,1098,2362,1264],"Stake is tripled", False),
 ([2100,1306,2362,1478],"Stake &times; 10", False),
 ([2100,1510,2362,1682],"Stake &times; 5", False),
]
for box, txt, hdr in cells:
    b.heading(box, txt, fs=9.0, **{**CELL, 'bold': hdr})
b.write()
