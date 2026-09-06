import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
b = PageBuild(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 15)
b.heading([170,40,1058,156], "Number Guessing (High-Low Game)", fs=12.3)
b.heading([170,788,756,858], "Function description:", fs=13)
b.heading([172,1242,878,1310], "Example of a game in progress:", fs=10.1)
b.prose([168,344,1266,768],
 "Number guessing is one of the classic computer games. MICROTRONIC uses its random number "
 "generator to pick a number between 0 and 999. The aim is to find this hidden random number "
 "in as few guesses as possible. After each attempt the computer indicates whether the "
 "guessed number is larger or smaller than the computer's number. With logical thinking it is "
 "possible to find it in 5 to 6 guesses.", fs=10.9)
b.prose([166,870,1256,1222],
 "After HALT &ndash; NEXT &ndash; 00 the program is entered according to the table.<br><br>"
 "Program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN. The display stays dark for a short "
 "time while the computer picks a random number between 0 and 999. It then shows: 000.", fs=10.9)
b.prose([1300,344,2390,960],
 "If key C is pressed while a 6-digit display is showing, the display shows the number of "
 "guesses made so far. Pressing key C again brings back the 6-digit display and guessing can "
 "continue.<br><br>"
 "If the number cannot be found, the game can be broken off at any time by pressing key B. The "
 "display then shows BXXXB (XXX = the random number picked by the computer). Pressing key A "
 "shows the number of guesses made so far. Pressing key A again starts a new game.", fs=10.9)
b.prose([174,1328,1266,2286],
 "Suppose 368 is the random number picked by the computer. For a first guess the number 560 is "
 "entered, then key A is pressed. The display shows: 560 000. The three left-hand positions "
 "show the number that is larger than the number sought; the three right-hand positions show "
 "the number that is smaller.<br><br>"
 "For a second guess the number 275 is entered, say, pressing key A after every entry. The "
 "display now shows: 560 275. The number sought must therefore lie between 560 and 275. If 355 "
 "is entered on the next attempt, the display shows 560 355.<br><br>"
 "With further guesses you feel your way closer and closer to the number the computer is "
 "keeping hidden. When the number is found, the display in our example shows E368E. Pressing "
 "key A again shows the number of guesses. Pressing key A once more starts the next game.", fs=10.9)
b.heading([1296,974,2246,1028], "Programmer: Markus Jouaux, 6970 Lauda", fs=11, bold=False)
b.write()
