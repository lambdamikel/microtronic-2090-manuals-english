import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 53)

b.heading([162,72,1200,186], "World Time Calculation", fs=14.5)

b.prose([154,382,1236,1372],
 "With the World Time Calculation program the time can be worked out for any "
 "place on earth. All you need to know for this is the meridian of longitude the "
 "place lies on.<br><br>"
 "The earth is divided into so-called time zones. These time zones mean that "
 "within an individual country the same time applies everywhere. Otherwise the "
 "time in the west of Germany would differ from the time in the east of Germany "
 "by several minutes, for example. The World Time Calculation program does not "
 "take these time zones into account, but calculates the actual time (position "
 "of the sun) for the corresponding meridian of longitude.", fs=10.6)

b.heading([1278,382,1808,446], "Function description:", fs=12.6)

b.prose([1280,452,2376,1802],
 "After HALT &ndash; NEXT &ndash; 00 the program is entered according to the "
 "table. Then input 4 is connected to the Takt/Clock socket. After HALT &ndash; "
 "PGM &ndash; 3 the Central European Time (CET) is entered. During summer time 1 "
 "hour has to be added to CET.<br><br>"
 "Program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN.<br><br>"
 "The display shows: 0000. Say the computer is to work out the time for Tokyo. "
 "Tokyo lies on the 138th meridian (entry: 138). Then either key 0 has to be "
 "pressed (for the time of a city that lies to the east) or key 1 (if the city "
 "lies to the west). As Tokyo lies to the east of us, key 0 is pressed.<br><br>"
 "After a short calculating time the time for this meridian appears. If it is "
 "17.36 CET here, for example, the result for Tokyo is 2.48. For a new time "
 "calculation press key 0. The display shows 0000 again.<br><br>"
 "If CET is to be displayed, either 0 degrees west (that is, 0001) or 360 "
 "degrees east (that is, 3600) has to be entered.", fs=10.6)

b.heading([1268,2226,2336,2326],
    "Programmer: Michael Stapfer, 8850 Donauw&ouml;rth", fs=11, bold=False)
b.write()
