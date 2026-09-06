import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 45)

b.heading([162,366,1000,430], "Function description:", fs=12.6)

b.prose([150,460,1254,888],
 "Before programming, the program memory must without fail be cleared by "
 "entering HALT &ndash; PGM &ndash; 5 (erase program). Then, after HALT &ndash; "
 "NEXT &ndash; 00, enter the program as per the table. Note that in the program "
 "table the middle digit of the instruction code is shown as X from address 03 "
 "to 08. In place of X one digit of the 6-digit code number is entered each "
 "time. If the code is to be 195513, for example, the following instructions "
 "have to be entered from address 03 to 08:", fs=10.4)

b.heading([138,916,692,984], "Address &nbsp; Instruction code", fs=10.6, bold=False)

b.prose([144,1292,1244,2246],
 "When the program has been entered completely, the piezo buzzer is connected to "
 "the GND and output 2 sockets. The BUSCH special relay 5964 or the BUSCH mains "
 "switching unit 2087 can be connected to output 1 as shown in the "
 "illustrations. Electronic or electrical devices can be connected to these "
 "relays, and they can only be put into operation by entering the correct "
 "code.<br><br>"
 "Program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN.<br><br>"
 "The display shows 000000. If the previously programmed code (195513 in our "
 "example) is now entered, output 1 is switched on together with the relay "
 "connected to it. If this output is to be switched off again, any number key "
 "has to be pressed. If a wrong code is entered, the piezo buzzer connected to "
 "output 2 sounds; it switches itself off again automatically after a short "
 "time. A new attempt at entry can then be made.", fs=10.4)

b.heading([138,2250,1240,2334],
    "Programmer: Frank Simon, 6342 Haiger-Allendorf", fs=11, bold=False)
b.write()
