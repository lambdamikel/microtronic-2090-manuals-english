import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
b = PageBuild(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 6)
b.heading([106,70,1384,194], "Before you try the first programs!", fs=17)
b.prose([114,370,1194,1944],
 "All programs are intended specifically for the BUSCH MICROTRONIC computer system 2090. "
 "A basic knowledge of the functions of the MICROTRONIC computer is assumed. You should "
 "therefore have worked through the instruction book Part 1 supplied with the computer at "
 "least as far as page 22.<br><br>"
 "Every program has been tested several times for correct operation. If a program does not "
 "behave as described, you have certainly made a mistake while programming (transposed "
 "digits or similar).<br><br>"
 "In such a case you should go back to the start of the program once more. Required key "
 "presses: HALT &ndash; NEXT &ndash; 00. The first instruction code (address 00) is now "
 "displayed. Each time you press the NEXT key the next instruction entry is displayed, and "
 "you can use the program table to check whether all instruction codes have been entered "
 "correctly. Please bear in mind that a single incorrect instruction entry may be enough to "
 "stop the program working properly. After checking, please try a new program start: "
 "HALT &ndash; NEXT &ndash; 00 &ndash; RUN.<br><br>"
 "By purchasing the MICROTRONIC cassette interface 2095 you can transfer the programs "
 "entered into the computer onto a cassette recorder or tape machine. Even the longest "
 "programs are then ready to play within a few minutes, without having to be entered again. "
 "You can put together your own MICROTRONIC program library.", fs=11)
b.prose([1236,370,2328,1340],
 "The programs published in this book were developed by entrants to the BUSCH MICROTRONIC "
 "programming competition of 1983. If you too have a good idea, you should send us your "
 "program for informal appraisal. Perhaps your suggestion will also be published in a "
 "following MICROTRONIC book. Please note the guidance given in the MICROTRONIC instruction "
 "book Part 2 (page 77).<br><br>"
 "We wish you continued enjoyment in programming, experimenting and learning through play "
 "how a computer works.", fs=11)
b.write()
