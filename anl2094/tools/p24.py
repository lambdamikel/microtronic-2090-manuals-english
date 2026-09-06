import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 24)

b.heading([112,1512,1200,1578], "(Fig. El. Studio 2070)", fs=10.0, bold=False)

b.prose([122,1584,1216,2314],
 "The connecting leads (1&ndash;4 and GND) run to the corresponding computer "
 "output sockets (1&ndash;4 and GND). The connections must not be swapped.<br><br>"
 "Since both the Studio Center 2070 and the computer have transfer sockets, the "
 "leads intended for the computer outputs can first be taken to the "
 "transfer-cable module. In that case the transfer-cable module is used on the "
 "computer as well, and the connections to the computer outputs are made from "
 "there. Care must then be taken to use the same numbering for the connections "
 "on both transfer-cable modules. The two units can now be linked to each other "
 "with a standard transfer cable.", fs=10.6)
b.write()
