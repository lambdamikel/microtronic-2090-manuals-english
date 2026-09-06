import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 51)

b.heading([140,360,918,432], "Function description:", fs=12.6)

b.prose([148,464,1232,2230],
 "After HALT &ndash; NEXT &ndash; 00 the program is entered according to the "
 "table. Then the additional electronic circuit (see illustration) is built with "
 "the Electronic Studio 2070 and connected to the computer. (If the Electronic "
 "Studio IC amplifier set 2072 is available as well, the circuit can be built as "
 "shown in illustration 20 of the 2072 instruction book. In that case the "
 "push-button is replaced by the special relay 5964.) Without an Electronic "
 "Studio 2070 the piezo buzzer can be connected to the GND and output 1 sockets "
 "as a makeshift. A true-to-life chime is then not possible, however. In every "
 "case make sure that, as shown in the illustration, push-button G is connected "
 "to input 1 and that a connection is made from the Takt/Clock socket to input "
 "4.<br><br>"
 "The &ldquo;multi-function clock&rdquo; is now ready for use. First the time "
 "has to be entered. To do this press the keys HALT &ndash; PGM &ndash; 3 and "
 "enter the time as 4 digits (e.g. 7.30 = entry: 0730). Then start the program "
 "with HALT &ndash; NEXT &ndash; 00 &ndash; RUN and switch on the additional "
 "circuit on the Electronic Studio 2070 with the slide switch.<br><br>"
 "The display shows: D0000. Now follows the 4-digit entry of the date (e.g. 20 "
 "March = 2003). The two left-hand display places show the day of the month, the "
 "right-hand display places the month. Then key A still has to be pressed. The "
 "display now shows the time for 7 seconds and the date for 3 seconds "
 "alternately. On every full hour the corresponding chime is produced (e.g. at "
 "10 o'clock in the morning 10 chimes are produced, 3 p.m. gives 3 chimes).",
 fs=10.6)

b.prose([1276,366,2362,1538],
 "The multi-function clock can be used in continuous operation. The day of the "
 "month is changed automatically at midnight. The computer also takes into "
 "account that January has 31 days or February only 28 days, for example. Only "
 "in leap years does the date have to be changed manually.<br><br>"
 "An alarm time can also be entered. To do this, push-button G is held down "
 "until AAAA appears on the display. Enter the alarm time (4 digits) and press "
 "key B. If the alarm time is to be cleared, enter AAAA (in place of the alarm "
 "time already there).<br><br>"
 "At the alarm time a continuous tone is produced. It can be switched off by "
 "pressing any number key.", fs=10.6)

b.prose([1276,2086,2382,2232],
 "Programmers: Frank Simon, 6342 Haiger<br>"
 "Michael Bahn, 5000 Cologne", fs=11, lh=1.25, justify=False)
b.write()
