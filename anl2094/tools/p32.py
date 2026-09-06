import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 32)

b.prose([158,54,1218,618],
 "The correct order has been found. The piezo buzzer sounds for a short time. "
 "For the example above the display then shows: 0004, that is, 4 swap attempts "
 "were needed to find the correct number sequence. Pressing any number key "
 "restarts the program.<br><br>"
 "If key F is pressed during play (instead of 0, 1 or 2), the number of swap "
 "attempts needed so far is displayed. Pressing key F again brings back the "
 "number sequence and the game can be continued.", fs=10.6)

b.heading([152,630,1218,732],
    "Programmer: Markus Jouaux, 6970 Lauda", fs=11, bold=False)
b.write()
