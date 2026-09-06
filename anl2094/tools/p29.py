import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 29)

b.heading([170,68,1000,184], "Car Race", fs=15)

b.prose([172,378,1256,1104],
 "The car race is an interesting reaction game. You have to try to dodge "
 "oncoming cars within a reaction time of two seconds (or, at the increased "
 "difficulty level, within one second). The road is represented by the four LEDs "
 "at the computer outputs and by four places of the display. Each LED, or each "
 "display place, corresponds to one lane. The lane occupied by your own car is "
 "marked on the display by a 1, the free lanes are marked by 000. Lit LEDs at "
 "the outputs mean that those lanes are occupied by oncoming vehicles, which "
 "change lane after every move (controlled by the computer's random generator). "
 "The player has to try to steer their car into a free lane.", fs=10.6)

b.heading([162,1112,730,1182], "Function description:", fs=12.6)

b.prose([164,1190,1258,2338],
 "After HALT &ndash; NEXT &ndash; 00 the program is entered according to the "
 "table. Then &ldquo;input 4&rdquo; is connected to the socket "
 "&ldquo;Takt/Clock&rdquo;.<br>"
 "Program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN.<br><br>"
 "The display shows, for example: 0100 = our vehicle (1) is in the second lane "
 "from the left. Individual LEDs light up at the outputs (oncoming vehicles). "
 "There are several ways of changing lane by pressing the appropriate key:<br><br>"
 "Key 1: the vehicle moves one lane to the left (the 1 on the display is shifted "
 "one place to the left).<br>"
 "Key 2: the vehicle stays in its lane (the display remains unchanged).<br>"
 "Key 3: the vehicle moves one lane to the right.<br>"
 "Key 5: the vehicle moves two lanes to the left.<br>"
 "Key 7: the vehicle moves two lanes to the right.<br>"
 "Key 9: the vehicle moves three lanes to the left.<br>"
 "Key B: the vehicle moves three lanes to the right.", fs=10.6)

# ---- right column ------------------------------------------------------
b.prose([1294,382,2392,476],
 "The way the game works is made clear by the following example:", fs=10.6)

# two-line label; the LED artwork and the 0100 digits to its right stay put
b.prose([1298,518,2056,678],
 "2 LEDs are lit at the 4 outputs:<br>The display shows:",
 fs=10.2, lh=1.55, justify=False)

b.prose([1294,692,2378,1942],
 "Lanes 2 and 3 are occupied by oncoming cars. Our car is in the second lane, "
 "that is, in a moment it will collide with an oncoming car. An immediate "
 "evasive manoeuvre is needed: either one lane to the left (press key 1) or two "
 "lanes to the right (press key 7). The pattern of lit LEDs at the outputs "
 "changes, and we have to dodge the oncoming vehicles with quick-reaction "
 "entries.<br><br>"
 "The game ends automatically if more than two seconds are needed to enter the "
 "evasive manoeuvre. The game also ends if we dodge into a lane in which a car "
 "is coming towards us, or if we move into a lane that does not exist (too far "
 "to the left or to the right). The end of the game is signalled by the flashing "
 "display, on which the kilometres driven (the number of successful evasive "
 "manoeuvres) then light up. A new game can be started by pressing key 0.<br><br>"
 "BUSCH MICROTRONIC wishes you a good trip.", fs=10.6)
b.write()
