import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 55)

b.heading([156,76,1076,206], "Acoustic Computer Remote Switching",
          fs=14.5, nowrap=False, lh=1.15)

b.prose([152,386,1256,810],
 "With this program electrical devices can be switched on and off "
 "&ldquo;acoustically by remote control&rdquo;. An electronic circuit (a "
 "colour-organ type circuit) converts sounds into low (0) and high (1) signals. "
 "The computer evaluates these 0 and 1 signals accordingly, so that its outputs "
 "are switched on and off by sounds that can be determined in advance.", fs=10.6)

b.heading([154,826,798,914], "Function description:", fs=12.6)

b.prose([154,924,1245,2212],
 "After HALT &ndash; NEXT &ndash; 00 the program is entered as per the table. "
 "Then the electronic circuit (as per the assembly plan) is connected to the "
 "computer's input 1 and GND sockets.<br><br>"
 "The circuit has to be adjusted with the potentiometer so that the light bulb "
 "is switched on by hand-clapping or a telephone ringing, for example, and goes "
 "out again after a short time.<br><br>"
 "Program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN.<br><br>"
 "The display shows 0. The computer is waiting for the entry of how many sounds "
 "(hand claps, telephone rings or similar) are to switch its outputs on or off. "
 "Any entry number between 1 and 9 is possible, or the letters (A = 10, B = 11, "
 "C = 12, D = 13, E = 14, F = 15).<br><br>"
 "Example: the number 4 (for four sound intervals) is entered. The display goes "
 "dark. The computer outputs can now be switched on by clapping four times. Take "
 "care, however, to leave a short pause between each clap until the light bulb "
 "(of the circuit) has switched itself off again. In the same way (four claps) "
 "the computer outputs can also be switched off.", fs=10.6)

b.heading([1282,382,1900,456], "Important!", fs=12.6)

b.prose([1282,464,2372,2070],
 "The program has some special features so that the switching cannot be carried "
 "out by unauthorised people. In our example we entered that the switching is "
 "triggered by four sounds. The computer counts the sounds internally (which are "
 "registered through the colour-organ type circuit). It is a condition, however, "
 "that the sound intervals are made without long pauses. If there is a pause of "
 "more than 3 seconds between the second and third clap, for example, the "
 "computer assumes that the sound entry has been broken off. After a break-off "
 "the following sounds are registered as a new start, that is, a third and "
 "fourth clap do not trigger any switching.<br><br>"
 "Once the computer has registered the number of sounds entered (4 in our "
 "example), its outputs are not switched on or off immediately. It now waits "
 "about five seconds and checks whether further sounds are received during that "
 "time. If a fifth clap comes within this five-second period, for example, the "
 "program is broken off by the computer. To trigger the switching, 4 sound "
 "intervals are required in this example. Fewer (3) or more (5) are not "
 "accepted.<br><br>"
 "Thanks to this checking, the program works absolutely reliably as a telephone "
 "switch, for example. The electronic sound-receiving circuit is set up so that "
 "a telephone ringing is registered. When dialling this telephone you have to "
 "let it ring as many times as was entered into the computer. If a stranger "
 "calls, they can only trigger the switching if they happen by chance to reach "
 "the number of sounds entered into the computer.", fs=10.6)

b.heading([1278,2230,2260,2330],
    "Programmer: Peter Polzer, 7000 Stuttgart", fs=11, bold=False)
b.write()
