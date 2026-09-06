"""Page 66 - the table of contents.

The marked prose boxes span the FULL width of each list, page numbers included,
so the white-out takes the numbers with it and they have to be redrawn. Each
list is therefore rebuilt as a two-column table: entry left, page number right.

Row pitch is set from the scan (62 px = 5.25 mm between baselines) so the
English lines land on the German ones. The page numbers are the manual's own
printed numbers and are reproduced unchanged.

Entry names are kept identical to the title actually used on each translated
page, so the contents and the pages agree.
"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 66)

PITCH = "5.25mm"          # measured line pitch of the German lists
NUMPAD = "0 1.9mm 0 0"    # brings the right-aligned numbers onto the German column


def toc(box, rows, fs=10.0):
    tr = "".join(
        f'<tr><td style="line-height:{PITCH};padding:0;white-space:nowrap">{t}</td>'
        f'<td style="line-height:{PITCH};padding:{NUMPAD};text-align:right;'
        f'white-space:nowrap">{p}</td></tr>'
        for t, p in rows)
    b.raw(box,
          f'<table style="width:100%;border-collapse:collapse;'
          f'font-family:Helvetica,Arial,sans-serif;color:#111;'
          f'font-size:{fs}pt">{tr}</table>')


b.heading([396,62,1226,240], "Table of Contents", fs=15)

b.heading([396,370,1870,448], "1. Computer games:", fs=11.5)
b.heading([1894,382,2036,450], "Page", fs=11.5)

toc([390,462,2040,1404], [
    ("Number Avalanche &ndash; electronic memory training", 4),
    ("Blockade &ndash; a strategy game", 6),
    ("One-Armed Bandit &ndash; a game of chance", 8),
    ("Arithmetic Trainer &ndash; the computer checks arithmetic problems", 11),
    ("Number Guessing (High-Low Game) &ndash; classic computer game", 12),
    ("A Hundred Wins &ndash; a devilish puzzle game", 14),
    ("MICROTRONIC Roulette &ndash; a game of chance on a well-known model", 16),
    ("Sound Memory &ndash; a concentration game", 19),
    ("Pull &ndash; a strategy game", 23),
    ("Car Race &ndash; an interesting reaction game", 26),
    ("Sorting Digits &ndash; a tricky brain-teaser", 28),
    ("Forming Words and Sentences &ndash; the funny computer", 30),
    ("17 + 4 (Black Jack) &ndash; a game of chance against the computer", 32),
    ("Fallgrube (Pitfall) &ndash; a tactical game of chance", 34),
    ("Chess Clock &ndash; the computer checks thinking times", 37),
])

b.heading([392,1426,2040,1506], "2. Interesting computer experiments:", fs=11.5)

toc([386,1520,2034,1868], [
    ("Code Lock &ndash; a microelectronic alarm centre", 40),
    ("Light-barrier controlled time measurement &ndash; when was the light "
     "switched on?", 43),
    ("Clock with chimes, date display and alarm function", 46),
    ("World Time Calculation &ndash; what time is it in Tokyo?", 50),
    ("Acoustic Computer Remote Switching &ndash; switching electrical devices "
     "by telephone", 52),
])

b.heading([392,1882,2040,1960], "3. For mathematicians and statisticians:", fs=11.5)

toc([388,1962,2036,2320], [
    ("Program for drawing pie charts", 54),
    ("Diagonal calculation program for polygons", 55),
    ("Division program for any number of decimal places", 56),
    ("Prime number calculation", 58),
    ("Exponentiation", 60),
])
b.write()
