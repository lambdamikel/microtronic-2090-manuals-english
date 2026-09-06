import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
b = PageBuild(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 17)
b.heading([186,54,688,200], "A Hundred Wins", fs=15.4)
b.heading([1324,358,1960,436], "Function description:", fs=13)
b.prose([192,360,1274,920],
 "A Hundred Wins is a positively fiendish puzzle game. A number between 1 and 10 is added in "
 "turn by the player and by the computer to a random number picked by the computer at the "
 "start of play. Whoever reaches 100 first has won.", fs=10.1)
b.prose([1322,448,2408,1290],
 "After HALT &ndash; NEXT &ndash; 00 the program is entered carefully according to the table. "
 "The piezo buzzer is then connected to the output 1 and GND sockets. Then program start: "
 "HALT &ndash; NEXT &ndash; 00 &ndash; RUN.<br><br>"
 "The display shows: 0XXA00 (XX = the random starting number picked by the computer).<br><br>"
 "If the computer is to begin the game, the number 0 is entered. Entering zero is not allowed "
 "later in the game. If the player wants to add a number to the starting number, a number "
 "between 1 and 10 is entered. The entry is shown on the two right-hand positions of the "
 "display. Then press key A. The computer adds the entered number to the starting number and "
 "shows the result on the left-hand 3 display positions. The computer then carries on "
 "automatically and adds its own number to that result. After a short calculation a brief tone "
 "sounds and the display shows:", fs=10.1)
# the ASCII-art callout: keep the leader lines, translate only the two labels
b.raw([1314,1310,2412,1570],
 '<div style="font-family:\'DejaVu Sans Mono\',Courier,monospace;font-size:10.5pt;'
 'line-height:1.15;color:#111;white-space:pre">'
 '0XXCXX\n'
 ' &#9474;  &#9492;&#9472;&#9472;&#9658; Number the computer has added to\n'
 ' &#9474;       its last result.\n'
 ' &#9492;&#9472;&#9472;&#9472;&#9472;&#9472;&#9658; New total result.'
 '</div>')
b.prose([1318,1604,2408,2198],
 "Now the player enters a number again, confirming with key A after each entry. It is "
 "essential to note that the entered number must lie between 1 and 10; entering 0, or a number "
 "greater than 10, is not permitted.<br><br>"
 "The game ends as soon as the number 100 is reached. If the computer wins, the display shows: "
 "C100C. If the player wins, the display shows: E100E. A new game is started by pressing "
 "key 0.", fs=10.1)
b.write()
