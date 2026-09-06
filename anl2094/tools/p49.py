import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 49)

b.heading([146,74,1218,284],
    "Clock with chimes, date display and alarm function",
    fs=14.0, nowrap=False, lh=1.15)

b.prose([150,378,1234,818],
 "With this program MICROTRONIC becomes a &ldquo;multi-function clock&rdquo;. On "
 "every full hour the computer strikes the hour (like a church tower clock). The "
 "display alternately shows the time for 7 seconds and the date for 3 seconds. "
 "An alarm time can also be entered (for triggering an alarm, etc.). To produce "
 "the chime true to life, the BUSCH Electronic Studio 2070 and", fs=10.6)

b.prose([1276,370,2364,804],
 "special relay 5964 are needed. To try the program out (without the chime), the "
 "piezo buzzer can be used.<br><br>"
 "Additionally required: Electronic Studio 2070 and BUSCH special relay 5964.",
 fs=10.6)
b.write()
