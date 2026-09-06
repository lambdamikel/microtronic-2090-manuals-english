import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 60)

b.heading([122,374,930,444], "Of interest to the programmer:", fs=12.6)

b.prose([122,458,1216,1198],
 "The algorithm for the big division program is relatively simple: with a "
 "problem such as 787 : 63 the two numbers are divided in the working and "
 "storage registers by the division instruction. The working registers then hold "
 "the result before the decimal point, 12. The remainder, 31, stays in the "
 "storage registers.<br><br>"
 "The decimal places are calculated further by multiplying the remainder (31) by "
 "10 and dividing the result, 310, by 63 again. The first decimal place, 4, "
 "moves into the working register; the remaining remainder (58) is again "
 "multiplied by 10 in the storage registers and divided by 63. That gives the "
 "second decimal place. This process is repeated automatically until the program "
 "is broken off, so that any number of decimal places can be calculated.",
 fs=10.4)

b.heading([118,1210,1216,1314],
    "Programmer: Michael Stapfer, 8850 Donauw&ouml;rth", fs=11, bold=False)
b.write()
