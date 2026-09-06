import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 61)

b.heading([156,82,1144,258], "For mathematicians: prime number calculation",
          fs=14.0, nowrap=False, lh=1.15)

b.prose([156,392,1246,1768],
 "The definition of prime numbers is given in the &ldquo;Guinness Book of "
 "Records&rdquo; as follows:<br><br>"
 "Prime numbers are all whole numbers (with the exception of 1) that are "
 "divisible only by themselves and by 1, e.g. 2, 3, 5, 7 or 11.<br><br>"
 "The smallest prime number is therefore 2; the largest known prime number (a "
 "number with 13395 digits) is 2<sup>44497</sup> &ndash; 1. It was reported as "
 "the highest prime number on 8 April 1979, after Harry Nelson (47) and David "
 "Slowinski (25) had worked on this calculation for two months with the help of "
 "a Cray One computer at the University of California (Lawrence Livermore "
 "Laboratory).<br><br>"
 "Prime numbers play a large part in mathematics. Prime number calculation is "
 "also often used in computer technology for so-called &ldquo;benchmark&rdquo; "
 "programs. With benchmark programs the calculating speed of different types of "
 "computer, or of different programming languages, can be compared. A computer "
 "is made to calculate the first thousand prime numbers one after the other, for "
 "example, and the time needed for this is measured. If these calculations are "
 "carried out with different computers, you get a very good comparison of their "
 "working speed.<br><br>"
 "With the following program all prime numbers between 0 and 99,999 can be "
 "calculated, or particular numbers can be checked to see whether they are a "
 "prime number.", fs=10.3)

b.heading([156,1770,774,1834], "Function description:", fs=12.6)

# NOTE: the sentence runs across the column break, exactly as in the German
# ("Nach jedem Tastendruck" / "C wird die naechste Primzahl berechnet").
b.prose([158,1846,1242,2342],
 "After HALT &ndash; NEXT &ndash; 00 the program is entered carefully as per the "
 "table. Then connect the piezo buzzer to output 1 and socket GND. Program start "
 "with HALT &ndash; NEXT &ndash; 00 &ndash; RUN.<br><br>"
 "The display shows: 00000. If key C is pressed, the computer calculates the "
 "first prime number. It starts automatically with 1 (although this is not "
 "really a prime number at all). The result shown is announced at the same time "
 "by a buzzer tone. After each press of key", fs=10.3)

b.prose([1280,392,2388,1378],
 "C the next prime number is calculated (2, 3, 5, etc.). The piezo buzzer can be "
 "switched off with key D. With key A the display is set back to 0. If key B is "
 "then pressed, any numerical value can be entered for a prime number "
 "check.<br><br>"
 "Example: press keys A and B one after the other. Then enter the number 500. "
 "Press key C. The computer checks whether the number entered (500) is a prime "
 "number. If it were, the number entered would be displayed again. As in our "
 "example the number 500 is not a prime number, the next higher prime number "
 "(503) is displayed. Key C can then be pressed again for the calculation of the "
 "next prime number.<br><br>"
 "When calculating larger prime numbers the calculating time may in some "
 "circumstances amount to several minutes. The piezo buzzer draws attention to "
 "the result found (switch the buzzer off with key D).", fs=10.3)

b.prose([1282,1386,2386,1496],
 "Programmer: Klaus Hallatschek,<br>9850 Neugablonz-Kaufbeuren",
 fs=11, lh=1.25, justify=False)
b.write()
