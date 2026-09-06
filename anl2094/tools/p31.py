import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 31)

b.heading([164,66,1000,182], "Sorting Digits", fs=15)

b.prose([164,372,1254,876],
 "A tricky brain-teaser. The numbers 1 &ndash; 6 appear on the computer display "
 "in random order (e.g. 264315). These digits have to be sorted into ascending "
 "order (123456) by means of prescribed swap operations. The swap operations are "
 "laid down in such a way that it is not possible simply to exchange two digits "
 "with each other; instead four numbers are swapped in every swap operation. The "
 "aim of the game is to reach ascending order with as few swap operations as "
 "possible.", fs=10.6)

b.heading([168,900,720,978], "Function description:", fs=12.6)

b.prose([168,984,1246,2212],
 "First the program is entered after HALT &ndash; NEXT &ndash; 00 according to "
 "the program table. Then the piezo buzzer is connected to output 1 and socket "
 "GND.<br>"
 "Program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN. The display shows: "
 "000.<br><br>"
 "The computer has now stored the number sequence 123456 and wants to know how "
 "often these numbers are to be swapped among themselves. Entering a small "
 "number (e.g. 2) gives an easier puzzle. Entering a larger number (e.g. 8) "
 "increases the difficulty. Maximum entry = 999. To begin with it is advisable "
 "to start with a small number, e.g. 2. This entry has to be completed by "
 "pressing key A.<br><br>"
 "After a short time the six numbers appear on the display in a jumbled order "
 "(e.g. 251346). Three different swap operations are available (which may also "
 "be used in alternation) to turn the jumbled sequence into an ascending one "
 "(123456). With badly jumbled sequences, &ldquo;sorting digits&rdquo; becomes a "
 "real brain-teaser.", fs=10.6)

# ---- right column ------------------------------------------------------
b.prose([1290,376,2360,464],
 "The following swap operations are available:", fs=10.6, justify=False)

SW = dict(fs=11.0, bold=False)
b.heading([1296,478,2420,552], "1st swap operation = press key 0", **SW)
b.prose([1302,552,2400,748],
 "The 1st (left-hand) number of the display is exchanged with the 4th number "
 "(half right), and at the same time the 2nd number is exchanged with the 3rd. "
 "(Example: 251346 becomes 315246.)", fs=10.6)

b.heading([1290,754,2420,836], "2nd swap operation = press key 1", **SW)
b.prose([1286,840,2396,988],
 "The 2nd number is exchanged with the 5th and at the same time the 3rd number "
 "with the 4th. (Example: 251346 becomes 243156.)", fs=10.6)

b.heading([1292,1002,2420,1082], "3rd swap operation = press key 2", **SW)
b.prose([1290,1086,2390,1718],
 "The 3rd number is exchanged with the 6th and the 4th number with the 5th. "
 "(Example: 251346 becomes 256431.)<br><br>"
 "A game in progress and the use of the swap operations are demonstrated by the "
 "following example:<br><br>"
 "After the program start the display shows: 000. Enter e.g. 4, then press key "
 "A. The computer now swaps the number sequence 123456 four times, in a random "
 "order of the swap operations described. The display now shows, for example: "
 "264315", fs=10.6)

# ---- worked example: attempt / result pairs ----------------------------
ATT = dict(fs=10.4, lh=1.25, justify=False)
b.prose([1298,1756,1800,1872], "1st swap attempt<br>entry e.g. key 0", **ATT)
b.prose([1290,1886,1812,1994], "2nd swap attempt<br>entry e.g. key 2", **ATT)
b.prose([1288,2004,1798,2124], "3rd swap attempt<br>entry e.g. key 0", **ATT)
b.prose([1288,2134,1810,2260], "4th swap attempt<br>entry e.g. key 1", **ATT)

RES = dict(fs=10.4, bold=False)
b.heading([2050,1806,2420,1884], "gives 346215", **RES)
b.heading([2056,1932,2420,2002], "gives 345126", **RES)
b.heading([2050,2054,2420,2132], "gives 154326", **RES)
b.heading([2062,2172,2420,2240], "gives 123456", **RES)
b.write()
