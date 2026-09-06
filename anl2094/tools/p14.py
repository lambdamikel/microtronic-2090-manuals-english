import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
b = PageBuild(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 14)
b.heading([108,40,572,178], "Arithmetic Trainer", fs=11.9)
b.heading([102,680,828,756], "Function description:", fs=13)
b.prose([100,350,1196,668],
 "This arithmetic trainer program lets you practise multiplication tables. The computer sets "
 "a sum. The result, worked out in your head, is entered. The computer checks whether the "
 "result is correct and then sets the next sum. If the entry is wrong, the computer shows the "
 "correct result.", fs=11)
b.prose([96,768,1184,2178],
 "After HALT &ndash; NEXT &ndash; 00 the program is entered according to the table. The green "
 "reset key must then be pressed briefly and the piezo buzzer connected to the GND and output "
 "1 sockets.<br><br>"
 "Program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN. The display shows 00000. Two "
 "arbitrary numbers, which must be smaller than 20, are entered, for example 15 and 12. The "
 "display shows 15012. This is the first sum. The two left-hand positions of the display (15) "
 "must be multiplied by the two right-hand positions (12). 15 &times; 12 = 180.<br><br>"
 "The result (180) is entered, then key A is pressed. A short beep confirms that the entry was "
 "correct. The display automatically shows the next sum: 15013. 15 &times; 13 is worked out "
 "and the result (195) entered, then key A pressed again.<br><br>"
 "If a wrong result is entered, the computer produces 2 short beeps. The message FE (error) "
 "appears on the display, then the correct result is shown. After a short time the next sum is "
 "set automatically.<br><br>"
 "To practise the whole multiplication table up to 20 &times; 20, enter 0101 after the program "
 "start (HALT &ndash; NEXT &ndash; 00 &ndash; RUN). Do not forget to press key A after every "
 "entry.", fs=11)
b.heading([90,2198,1154,2296], "Programmer: Alexander Stadler, A-1160 Vienna", fs=11, bold=False)
b.write()
