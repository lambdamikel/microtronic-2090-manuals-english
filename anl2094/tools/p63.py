import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 63)

b.heading([154,72,1250,240], "For mathematicians: exponentiation",
          fs=13.5, nowrap=False, lh=1.15)

b.prose([160,380,1256,732],
 "The following program shows that besides the four basic arithmetic operations "
 "(see the instruction books) MICROTRONIC can also carry out exponentiation. An "
 "example of exponentiation is 57<sup>3</sup> (57 &times; 57 &times; 57 = "
 "185,193).", fs=10.6)

b.heading([156,750,754,822], "Function description:", fs=12.6)

b.prose([146,842,1234,1838],
 "After HALT &ndash; NEXT &ndash; 00 the program is entered according to the "
 "table.<br><br>"
 "Program start with HALT &ndash; NEXT &ndash; 00 &ndash; RUN. The display shows "
 "000.<br><br>"
 "Example: the problem 57<sup>3</sup> is to be calculated. First the number 57 "
 "is entered &ndash; then key A. The display shows: 00. Now the exponent 3 is "
 "entered &ndash; key A. After a short calculating time the display shows 185193 "
 "as the result. After pressing any number key a new calculation can be carried "
 "out.<br><br>"
 "If the result is too large (more than 6 digits), the display shows: EEEEEE.<br><br>"
 "Note that the power 0 to the power of 0 is not calculated correctly, because "
 "it is not mathematically defined.", fs=10.6)

b.heading([1284,374,2044,446], "Of interest to the programmer:", fs=12.6)

b.prose([1282,458,2382,1834],
 "On many pocket calculators exponentiation can be called up by pressing a key. "
 "In these calculators the microprocessor is programmed to carry out the "
 "exponentiation by repeated multiplication. The algorithm needed for this is "
 "quite simple. First it is checked whether the exponent is a 1. If yes, the "
 "base (57 in our example) is the result. If the exponent is greater than 1, the "
 "base is multiplied by itself (57 &times; 57 in our example) and 1 is "
 "subtracted from the exponent entered. If the exponent is now 1, the result has "
 "been found. If no, the result of the last calculation (57 &times; 57 = 3,249) "
 "is multiplied by the base entered (57 in our example) again. 1 is again "
 "subtracted from the exponent and it is then checked whether the exponent is "
 "now equal to 1 and the result has thus been found.<br><br>"
 "The flow chart makes this principle clear. Note that the flow chart shows only "
 "the actual calculating part. Special input and output routines are of course "
 "also needed for the program. The flow chart shows one more special feature: in "
 "exponentiation it has been defined that the result is 1 if the exponent is 0. "
 "For this reason it is checked before the actual calculation whether the "
 "exponent is equal to 0 &ndash; if yes, the result is automatically 1.",
 fs=10.6)

b.heading([1274,2238,2180,2304],
    "Programmer: Matthias Gorek, 3210 Elze", fs=11, bold=False)
b.write()
