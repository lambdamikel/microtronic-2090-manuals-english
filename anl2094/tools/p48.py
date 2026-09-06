import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 48)

b.prose([118,366,1220,1378],
 "With a slight change to the program the opposite case can also be monitored. "
 "By entering HALT &ndash; NEXT &ndash; 01 &nbsp; 109 &ndash; NEXT, the program "
 "is changed so that the time stops as soon as the photoresistor is darkened. In "
 "this way you can monitor whether and when the light was switched off in a lit "
 "room.<br><br>"
 "With these programs the exact time of sunrise or sunset could also be "
 "determined automatically, for example.<br><br>"
 "If a program does not work properly, check whether the potentiometer has been "
 "adjusted correctly. To do this enter HALT &ndash; NEXT &ndash; 0 &ndash; A "
 "&ndash; RUN, set the potentiometer (as described) and start the program.",
 fs=10.6)

b.heading([116,1772,1062,1854],
    "Programmer: Holger Witt, 4006 Erkrath", fs=11, bold=False)
b.write()
