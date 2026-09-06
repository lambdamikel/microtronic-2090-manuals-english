import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 43)

b.heading([138,68,592,220], "Code Lock", fs=15)

b.prose([148,378,1240,804],
 "Code locks have been used for decades to secure safes, bank deposit boxes or "
 "suitcases, for example. The action of these code locks used to be achieved by "
 "complicated mechanics. For some years now there have also been electronic code "
 "locks, which have several important advantages: they work completely "
 "silently, for instance, and electronic code locks can be connected directly to "
 "an alarm system, so as to set off an alarm if a wrong code is entered, for "
 "example.", fs=10.6)

b.prose([1270,378,2356,798],
 "With the following program MICROTRONIC can be turned into a code lock with "
 "alarm triggering. By entering a 6-digit numerical code, electrical or "
 "electronic devices connected to the computer can be put into operation only by "
 "someone who knows the code. If a wrong code is entered, an alarm is set "
 "off.", fs=10.6)
b.write()
