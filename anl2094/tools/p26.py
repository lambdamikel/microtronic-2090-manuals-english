import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 26)

# title "Pull" is identical in English - left as printed, not overlaid.

b.prose([112,374,1212,1038],
 "Pull is a strategy game. It is played on a square board of 25 individual "
 "squares. The computer gets one playing piece, which is placed on square C. We "
 "have three pieces, which are placed on squares 1, 2 and 3 at the start of the "
 "game. We may move our pieces forwards only on the dark squares, while the "
 "computer may move both forwards and backwards. We win if we manage to block "
 "the computer's piece so that it can make no further move. The computer wins "
 "as soon as it reaches one of the squares 1, 2 or 3. A Pull game board is "
 "enclosed with this book.", fs=10.8)

b.heading([1236,368,1806,440], "Function description:", fs=12.6)

b.prose([1236,462,2328,2160],
 "After HALT &ndash; NEXT &ndash; 00 the program is entered carefully according "
 "to the table. Then press the reset button briefly. The piezo buzzer is "
 "connected to output 3 and socket GND. Owners of the Electronic Studio 2065 or "
 "2070 can also build the &ldquo;mini organ&rdquo; circuit (see page 20) and "
 "connect it to the computer outputs.<br>"
 "Program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN.<br><br>"
 "The display shows the starting position of our pieces: 123 (our pieces are on "
 "squares 1, 2 and 3, the computer's piece on square C). We begin and make a "
 "first move. Say we want to move a piece from square 3 to square 5 (only one "
 "piece may ever be moved at a time). Our pieces are then on squares 1, 2 and 5. "
 "We enter: 125 (the new piece positions). The display now shows: A (we must "
 "place the computer's piece on square A). Then press key 0. The display shows "
 "our position 125 again. We can make the next move, for example from square 1 "
 "to square 4. We enter: 425 (the new positions of the pieces). The display now "
 "shows: 7 (the computer's piece goes to square 7). We press key 0 again and "
 "then enter our new position.<br><br>"
 "If the computer reaches square 1, 2 or 3, an interrupted tone sounds (or, with "
 "the &ldquo;mini organ&rdquo; connected, a falling sequence of notes). If we "
 "manage to beat the computer, a short and a long tone are produced alternately "
 "(or, with the &ldquo;mini organ&rdquo; connected, a short melody is played). "
 "The display then shows the positions of the four pieces in four digits. "
 "Pressing key 0 starts a new game.", fs=10.8)
b.write()
