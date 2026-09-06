import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 20)

b.prose([112,62,1196,222],
 "We choose one of the betting options and press the corresponding keys. The display then shows "
 "the winning number according to the following scheme:", fs=10.6)

b.heading([104,240,358,314], "Example:", fs=12, bold=False)

# display-format callout: vertical leaders of differing depth, as in the original
b.raw([558,232,1182,558],
 '<div style="font-family:\'DejaVu Sans Mono\',Courier,monospace;font-size:7.4pt;'
 'line-height:1.16;color:#111;white-space:pre">'
 '217 0 1   means:\n'
 ' &#9474;  &#9474; &#9474;\n'
 ' &#9474;  &#9474; &#9660;  0 = odd number\n'
 ' &#9474;  &#9474;     1 = even number\n'
 ' &#9474;  &#9660;\n'
 ' &#9474;      0 = black\n'
 ' &#9474;      1 = red\n'
 ' &#9660;\n'
 'Lucky number (3 digits)'
 '</div>')

b.prose([112,566,1202,2224],
 "The example above (217 0 1) would produce the following winnings:<br><br>"
 "217 wins 300 times the stake.<br>"
 "The hundreds digit (bet on the number 2) = 3 times the stake.<br>"
 "The tens digit (bet on the number 1) = 10 times the stake.<br>"
 "The units digit (bet on the number 7) = 5 times the stake.<br>"
 "Black (4th winning position: 0) = double the stake.<br>"
 "Odd (5th winning position: 1) = double the stake.<br><br>"
 "If key A is then pressed, the sum of money won appears, including the stake. A display of "
 "00000 means that nothing was won and the stake was lost.<br><br>"
 "If key A is pressed again, the new account balance appears, that is, the total available for "
 "further games. On pressing key A once more the display shows 0000 again. The computer is "
 "waiting for your new stake: &ldquo;place your bets!&rdquo;<br><br>"
 "The game is ended automatically if more than 99,999 play marks have been won. In this case the "
 "display shows: EEEEE. The game is also ended if no money remains (display: E0000 and a "
 "continuous tone). In both cases a new game can be started by pressing any number key.", fs=10.6)

b.heading([100,2232,1204,2306], "Programmer: Frank Simon, 6342 Haiger 6", fs=11, bold=False)
b.write()
