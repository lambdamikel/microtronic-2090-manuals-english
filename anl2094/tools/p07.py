import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
b = PageBuild(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 7)
b.heading([174,70,622,172], "Number Avalanche", fs=12.0)
b.heading([1306,376,1888,442], "Function description:", fs=13)
# the German in this block starts 2 px left of the marked box, so its stems
# survived the mask. Mask the sliver separately rather than widening the
# prose box, which would shift the English off the column's left margin.
b.whiteout([170,384,180,1836])
b.prose([180,384,1262,1836],
 "The game Number Avalanche is an electronic memory exercise. It demands and develops "
 "concentrated thinking.<br><br>"
 "Individual numbers or letters light up briefly on the computer display in random order. "
 "The player's task is to memorise the numbers or letters and repeat them, in the order the "
 "computer gave them, by entering them on the keypad. After each correct entry the computer "
 "briefly shows a further number. The sequence to be repeated grows ever longer; the process "
 "continues like an avalanche, up to a maximum of 14 numbers or letters entered in the "
 "correct order.<br><br>"
 "The computer records how many repetitions were made before the first mistake. Six to eight "
 "correct entries is already a good result. Anyone who can remember all 14 has an outstanding "
 "memory.<br><br>"
 "With several players, the winner is the one who achieves the highest entry score over the "
 "agreed number of rounds.", fs=11)
b.prose([1304,466,2392,1966],
 "After pressing HALT &ndash; NEXT &ndash; 00 the program is entered according to the program "
 "table. The piezo buzzer is then connected to the output 1 and GND sockets.<br><br>"
 "Program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN<br><br>"
 "A number (0 &ndash; 9) or a letter (A &ndash; F) is shown briefly on the computer display. "
 "The number or letter must be repeated by pressing the corresponding key. A second number is "
 "shown immediately. Both numbers must now be repeated on the keypad in the correct order. "
 "The computer shows a third number. All three numbers must again be entered one after "
 "another in the correct order.<br><br>"
 "The game continues until a mistake is made during entry.<br><br>"
 "As soon as a number or letter is entered incorrectly, or in the wrong order, the computer "
 "responds with a continuous tone and the display shows how many numbers were entered in the "
 "correct order. Pressing any number key restarts the game.<br><br>"
 "If all 14 numbers are entered in the correct order, the computer produces a rapidly "
 "warbling &ldquo;tone of joy&rdquo;. The game is restarted by pressing any number key.", fs=11)
b.heading([1298,2240,2206,2302], "Programmer: Frank Gothe, 2210 Itzehoe", fs=11, bold=False)
b.write()
