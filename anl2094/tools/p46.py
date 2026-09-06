import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 46)

b.heading([114,54,1106,236], "Light-barrier controlled time measurement",
          fs=13.3, nowrap=False, lh=1.15)

b.prose([132,368,1214,1034],
 "Also required are a few components from the BUSCH Electronic Studio 2065 (or "
 "2070).<br><br>"
 "The MICROTRONIC computer can solve problems with very small programs too. A "
 "typical case is room monitoring, for example. In combination with a simple "
 "light barrier and the following program, MICROTRONIC can determine whether and "
 "when the lighting in a room was switched on or off.", fs=10.6)

b.heading([1256,356,1820,430], "Function description:", fs=12.6)

b.prose([1258,446,2342,1850],
 "After HALT &ndash; NEXT &ndash; 00 the short program is entered as per the "
 "table. Then the small electronic circuit is built (as shown in the "
 "illustration). Then, after HALT &ndash; PGM &ndash; 3, enter the time of day "
 "as 4 digits (9.30 = 0930).<br><br>"
 "Before the program is started the photoresistor has to be adjusted correctly "
 "with the potentiometer. A helper program is available for this, which is "
 "started with HALT &ndash; NEXT &ndash; 0 &ndash; A &ndash; RUN. The "
 "potentiometer is set so that the LED at output 1 lights up under normal room "
 "lighting. With the room darkened (the photoresistor darkened) the LED at "
 "output 1 must go out.<br><br>"
 "Now the room to be monitored is darkened and the program is started with HALT "
 "&ndash; NEXT &ndash; 00 &ndash; RUN. The display shows the running time of "
 "day. As soon as a light is switched on (the photoresistor is illuminated), the "
 "time stops on the display and you can read off when the light was switched on. "
 "Pressing key 0 continues the program (with the room darkened again).<br><br>"
 "With this program you can monitor whether and when a light was switched on in "
 "a room. The time stays shown on the display even if the light is switched off "
 "again.", fs=10.6)
b.write()
