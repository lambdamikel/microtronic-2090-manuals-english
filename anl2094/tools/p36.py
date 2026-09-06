import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 36)

b.prose([104,380,1216,902],
 "With games of chance of this kind no special winning strategy can be "
 "programmed that would give the computer a better chance than us. MICROTRONIC "
 "has been programmed so that after every deal it checks whether it has already "
 "reached more than 16 points. In that case it draws no further card for itself. "
 "A &ldquo;feel&rdquo; for the game cannot be programmed into a computer. A "
 "person may well draw another card (although they already have 18 points) "
 "because they hope to reach exactly 21 that way, or may stop even though only "
 "14 points have been reached.", fs=10.6)

b.heading([92,922,1214,1136],
    "Programmer: Johannes Freundorfer, 8354 Metten", fs=11, bold=False)
b.write()
