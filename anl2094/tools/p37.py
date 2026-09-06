"""Page 37 (printed 34) - FALLGRUBE.

Three things here are unlike any other page in this manual:
  * the game-board graphic spells ZIEL one big letter per grid cell, so the
    four letters are replaced one-for-one by GOAL. The marked boxes are tight
    around the German glyphs; the boxes used below are the CELL INTERIORS
    (grid lines measured at x=1313/1391/1469/1548/1626, y=1419/1497, inset 4px)
    because a "G" or an "O" is wider than the "I" it replaces and would spill.
  * the row axis is labelled with text rotated 90 deg counter-clockwise. CSS
    `rotate(-90deg)` reproduces it; the wrapper clips at the untransformed box
    so check_overflow still measures something meaningful.
  * the game's name FALLGRUBE stays German (it is drawn into the board art and
    is left untouched there); the section title carries the gloss.
"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 37)

b.heading([158,76,800,162], "Fallgrube (Pitfall)", fs=13.5)

b.prose([160,378,1242,780],
 "A game board of one hundred squares holds 12 invisible pitfalls. One after "
 "another, three playing pieces have to be brought from the starting position "
 "to the GOAL without falling into a pit. Tactics and a generous helping of luck "
 "are needed for this. Every time a new game begins the computer lays out the "
 "pitfalls afresh. A special game board is enclosed with this book as an "
 "accessory.", fs=10.6)

b.heading([154,796,850,872], "Function description:", fs=12.6)

b.prose([154,888,1260,1440],
 "After HALT &ndash; NEXT &ndash; 00 the program is entered according to the "
 "table. Then the piezo buzzer is connected to output 4 and socket GND.<br><br>"
 "Program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN.<br><br>"
 "At the start of the game the computer distributes 12 pitfalls (controlled by "
 "its random generator). The display then shows: 00. The first playing piece can "
 "start. Note that the start is always made in ROW 9. You may, however, choose "
 "which COLUMN the piece starts in.", fs=10.6)

b.heading([150,1448,500,1506], "Example:", fs=12.6)

b.prose([148,1516,1236,1770],
 "The first piece is to start in the 3rd column of row 9. When entering on the "
 "computer, the COLUMN is always entered first and then the ROW. In this example "
 "the entry is: 39. The display goes dark for a moment &ndash; then the value "
 "entered is shown.", fs=10.6)

b.heading([154,1780,600,1840], "Important:", fs=12.6)

b.prose([152,1848,1252,2336],
 "The playing piece may only ever advance one square in the direction of the "
 "GOAL. Sideways or backwards it may skip any number of squares. The piece can "
 "now go, for example, to the 4th column of row 8. Entry: 48.<br><br>"
 "If the piezo buzzer sounds briefly after the position numbers (COLUMN and ROW) "
 "have been entered, a wrong position was entered (e.g. advanced by more than "
 "one square). In that case the position has to be repeated correctly.", fs=10.6)

# ---- right column ------------------------------------------------------
b.prose([1284,384,2374,1290],
 "If a continuous tone sounds, the playing piece has fallen into a pit. The "
 "display shows: 02. The first digit tells us how many pieces have reached the "
 "GOAL (in this case none so far). The second digit shows how many pieces are "
 "still available (in this case 2). After key 0 is pressed the display shows 00 "
 "&ndash; the next piece can be started. (Start in ROW 9.)<br><br>"
 "Once a piece has reached the goal line (row 0) there are two possibilities:<br>"
 "1. The piezo buzzer sounds: the piece has fallen into a pit on the goal "
 "line.<br>"
 "2. The piezo buzzer does not sound: the piece has arrived safely at the "
 "GOAL.<br><br>"
 "In both cases the score is displayed, e.g. 11 (1 piece at the GOAL, 1 piece "
 "still available). Pressing key 0 redistributes the pitfalls. The next piece "
 "can start.", fs=10.6)

# ---- game board: Z I E L -> G O A L, one letter per grid cell ----------
# cell interiors, inset 4px from the measured grid lines so no rule is masked
CELL = dict(fs=12.5, bold=True, center=True, nowrap=True, lh=1.35)
b.heading([1317,1423,1387,1494], "G", **CELL)
b.heading([1395,1423,1465,1494], "O", **CELL)
b.heading([1473,1423,1544,1494], "A", **CELL)
b.heading([1552,1423,1622,1494], "L", **CELL)

# ---- game board axis labels -------------------------------------------
SANS = "font-family:Helvetica,Arial,sans-serif;color:#111;line-height:1;"

# row axis: reads bottom-to-top in the original.
# writing-mode gives the text a genuinely narrow-and-tall layout box (so it
# centres and measures correctly); rotate(180deg) turns vertical-rl's
# top-to-bottom reading into the bottom-to-top of the original.
b.raw([2124,1650,2160,1970],
 '<div style="writing-mode:vertical-rl;transform:rotate(180deg);'
 'white-space:nowrap;text-align:center;width:100%;height:100%;'
 f'{SANS}font-size:6.8pt">2nd entry = row</div>')

# column axis, under the board
b.heading([1586,2236,1864,2266], "1st entry = column",
          fs=6.5, bold=False, center=True, lh=1.0)
b.write()
