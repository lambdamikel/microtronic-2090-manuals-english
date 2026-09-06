import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
b = PageBuild(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 11)
b.heading([174,70,698,164], "One-Armed Bandit", fs=14.0)
b.heading([1300,374,1836,444], "Function description:", fs=12.4)
b.prose([172,376,1250,794],
 "The program &ldquo;One-Armed Bandit&rdquo; is a game of chance for 2 players, similar to the "
 "well-known machine found in pubs and amusement arcades. The computer display shows three "
 "rows of digits which change rapidly. The individual rows can be stopped by pressing the "
 "appropriate keys. The aim is to stop the display on several identical digits, or on a rising "
 "or falling sequence.", fs=11)
b.prose([1300,464,2388,808],
 "The program is entered after HALT &ndash; NEXT &ndash; 00 according to the program table. "
 "Push-button G must then be connected to input 1 and push-button H to input 2 (see "
 "illustration).<br><br>"
 "Program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN. The display shows: 000000.", fs=11)
b.write()
