import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 35)

# title "17 + 4 (Black Jack)" is identical in English - left as printed.

b.prose([156,386,1250,1030],
 "17 + 4 is a well-known card game (a game of chance). The aim of the game is to "
 "come as close as possible to the number 21 (17 + 4) by drawing 2 or more "
 "cards. Under no circumstances may 21 be exceeded. The players receive a card "
 "in turn until one of them believes they have enough points. The winner is the "
 "one who comes closest to 21. The game (further dealing of cards) is ended when "
 "a player has either received 2 aces or has reached 21, which means that this "
 "player has won.", fs=10.6)

b.heading([154,1066,714,1130], "Function description:", fs=12.6)

b.prose([162,1156,1266,1654],
 "After HALT &ndash; NEXT &ndash; 00 the program is entered according to the "
 "table. Then the piezo buzzer is connected to output 1 and socket GND.<br>"
 "Program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN.<br><br>"
 "The display shows: &ldquo;17 ADD 4&rdquo; (17 + 4). After key 1 is pressed the "
 "computer deals a &ldquo;card&rdquo; to us and one to itself (that is, it deals "
 "out the &ldquo;card values&rdquo;). The display shows the value dealt to "
 "us.", fs=10.6)

# display-digit callouts (the leader lines and the X = / XX = prefixes stay)
b.heading([302,1738,1202,1820],
    "card value we have just received.", fs=10.2, bold=False)
b.heading([260,1824,1202,1926],
    "sum of the card values we have received altogether.",
    fs=10.2, bold=False, nowrap=False, lh=1.25)

b.prose([152,1954,1262,2354],
 "We can now decide whether we want to draw another card, or whether the game "
 "should be ended because we think we have enough card values:<br><br>"
 "Key 1 = the computer gives us another card.<br>"
 "Key 0 = the game is to be ended.", fs=10.6)

# ---- right column ------------------------------------------------------
b.prose([1284,382,2394,630],
 "At the end of the game the piezo buzzer sounds and the display shows "
 "&ldquo;GOOD&rdquo; (6 is used as G) if we have won, or &ldquo;BAD&rdquo; if "
 "the game was lost. On pressing key 1 the display shows the final score of the "
 "game:", fs=10.6)

b.heading([1476,714,2400,792], "sum of our card values.", fs=10.2, bold=False)
b.heading([1392,802,2400,878],
    "sum of the computer's card values.", fs=10.2, bold=False)

b.prose([1292,886,2422,2330],
 "If the points are level the computer wins (that is how the program works). "
 "After pressing key 1 the display shows &ldquo;17 ADD 4&rdquo; and we can risk "
 "a new game.<br><br>"
 "Note that the numbers 1 to 9 and A as the ace (value 10) are allowed as card "
 "values. (The number 0 counts as a blank.) These values do not correspond "
 "exactly to the original cards, but the computer version of &ldquo;17 + 4&rdquo; "
 "is nevertheless just as interesting as the real model.<br><br>"
 "The computer ends the game automatically when the following score is "
 "reached:<br><br>"
 "1. The computer or we have reached more than 21 points.<br>"
 "2. The computer or we have reached exactly 21 points.<br>"
 "3. The first two cards drawn were 2 aces. In this case the display shows "
 "&ldquo;AA&rdquo; at the corresponding points position instead of the sum of "
 "the card values.<br><br>"
 "The program is written so that the computer plays as an independent player. It "
 "cannot &ldquo;see&rdquo; our cards. The cards drawn in turn are determined by a "
 "random generator.", fs=10.6)
b.write()
