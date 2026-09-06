import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
b = PageBuild(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 16)
b.heading([1224,56,2124,190], "Winning strategy for BLOCKADE", fs=13.3)
b.prose([1228,372,2330,1734],
 "This section should only be read once the Blockade game has proved impossible to win "
 "despite repeated attempts.<br><br>"
 "Winning this game is actually quite simple: you must try to achieve the same number of empty "
 "squares between the computer's pieces and your own on both tracks.<br><br>"
 "After the program start, at the beginning of play, there are three empty squares between the "
 "pieces on track 2. With our first entry, 15, we achieve the necessary three empty squares "
 "between the pieces on track 1 as well. The computer now moves to square 2 on track 1, which "
 "means only two empty squares remain on track 1 while there are three on track 2. We can now "
 "either move our piece one square to the right on track 1, or one square to the left on track "
 "2. In both cases the same number of empty squares between our pieces and the computer's is "
 "restored on both tracks.<br><br>"
 "The game can be continued in this way until victory. The important thing is that we "
 "consistently aim for the same number of empty squares between the pieces on both tracks.", fs=11)
b.write()
