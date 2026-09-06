import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
b = PageBuild(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 9)
b.heading([178,50,656,180], "Blockade", fs=19)
b.heading([166,1238,746,1298], "Function description:", fs=13)
b.heading([1296,1238,2104,1304], "If you cheat during entry:", fs=13)
b.prose([170,362,1256,1230],
 "Blockade is a strategy game played on two tracks of 5 and 10 squares. The computer and the "
 "player each have one piece on each track; the computer's two pieces are placed at the far "
 "left of the tracks and the player's at the far right. The pieces may then be pushed freely "
 "forwards and backwards along either track, the computer and the player taking turns. Jumping "
 "over the opponent's pieces is not permitted. The aim is to force both of the computer's "
 "pieces back into their starting position, on the leftmost squares, so that it has no moves "
 "left. This takes a good deal of tactics and strategy, since the computer also tries to block "
 "the player's pieces and force them back into the right-hand half of the board.<br><br>"
 "A Blockade playing field with counters, to serve as pieces, is supplied with this book.", fs=11)
b.prose([170,1322,1244,2294],
 "First the program is entered after HALT &ndash; NEXT &ndash; 00 according to the table. The "
 "piezo buzzer is then connected to the GND and output 1 sockets on the computer board.<br><br>"
 "Program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN. The display shows 00.<br><br>"
 "The computer's pieces are placed on square 1 of each track. The player's pieces go on square "
 "A of track 1 and square 5 of track 2. The player's first move can then be entered into the "
 "computer. To do this, first enter 1 or 2 for the track, then the number of the square the "
 "player wishes to move to.<br><br>"
 "To place a piece on track 1, square 7, for example, the entry 17 is required. The computer "
 "shows its move (13), that is, the computer piece", fs=11)
b.prose([1304,360,2386,1194],
 "is to be placed on track 1, square 3. The player now enters 22, say, and places a piece on "
 "square 2 of the second track. The computer announces that it wants to place its piece on "
 "track 1, square 6 (display: 16).<br><br>"
 "The computer already has the upper hand. The player can no longer advance further to the "
 "left, because the computer's pieces block the way. The player must retreat and enters, for "
 "example, 18. The computer immediately moves its piece to square 7 of the first track "
 "(display: 17). The player is pushed back further.<br><br>"
 "If the computer wins in this example, the display shows FFF and a short continuous signal "
 "sounds. A new game can be started by pressing key 0.", fs=11)
b.prose([1300,1320,2392,2034],
 "If, for example, 26 is entered (square 6 does not exist on track 2), or a move is entered "
 "onto a square already occupied by a piece, the game is broken off at once and the display "
 "shows 00 &ndash; the game must be started again.<br><br>"
 "If you manage to beat the computer, which is possible once you have worked out the right "
 "strategy, the display shows CCC and the computer produces an interrupted signal tone.<br><br>"
 "If you cannot win the game after several attempts, you will find the strategy explained on "
 "page 13.", fs=11)
b.heading([1300,2192,2276,2282], "Programmer: Christoph Fuchs, 6920 Sinsheim", fs=11, bold=False)
b.write()
