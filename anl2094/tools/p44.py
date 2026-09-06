import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 44)

b.prose([124,378,1224,812],
 "The 6-digit code gives more than 16 million (16,777,216) different "
 "possibilities. At least 5 seconds are needed to try one possibility, that is, "
 "if you wanted to find the code number by trial and error, more than 2 1/2 "
 "years would be needed for it.", fs=10.6)
b.write()
