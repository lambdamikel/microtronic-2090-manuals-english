import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
b = PageBuild(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 12)
b.heading([100,1742,722,1818], "Ending the game:", fs=13)
b.prose([100,56,1202,1716],
 "Now 6 arbitrary digits are entered, which the computer uses as a random starting value. "
 "After the 6th digit has been entered, the number 1 (or 2) appears briefly on the display. "
 "According to this, the first or the second player may begin.<br><br>"
 "Numbers and letters are now shown in very rapid succession at three positions of the "
 "display. Each of the three positions works independently and &ldquo;counts&rdquo; from "
 "0 &ndash; 9, then from A &ndash; F, and begins again at 0. The player whose turn it is can "
 "stop this counting with the red push-buttons as follows:<br><br>"
 "Button G: the left display position is stopped.<br>"
 "Button H: the middle display position is stopped.<br>"
 "Buttons G + H together: the right position is stopped.<br><br>"
 "As soon as all 3 positions have been stopped, the computer works out the score achieved and "
 "displays it. The score is determined by the computer on the following basis:<br><br>"
 "For each F on the display there are 5 points.<br>"
 "For 2 identical digits there are 10 points.<br>"
 "For 3 identical digits there are 20 points.<br>"
 "For a rising or falling sequence (for example 4 5 6 or 4 3 2) there are 40 points.<br><br>"
 "After the score has been shown briefly, the display shows the number of the player whose "
 "turn is next (1 or 2). The new game begins automatically and the next player can try their "
 "luck as described.", fs=11)
b.prose([102,1832,1192,2198],
 "If buttons G and H are pressed together while a player's score is being displayed, the game "
 "is ended. The computer shows the total score of player 1 and, after key 0 is pressed, the "
 "total score of player 2. Pressing key 0 once more restarts the game.", fs=11)
b.heading([100,2218,1190,2308], "Programmer: Valentin Illich, 7750 Konstanz", fs=11, bold=False)
b.write()
