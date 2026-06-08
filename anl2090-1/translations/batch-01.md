# Batch 1 — Pages 1–8 (English translation)

## Page 1 — Cover
*Color cover photo of the device. Original cover text:*
- **microtronic 2090 computer system**
- *Instruction book, Part 1*
- *Programming – experimenting – learn how a computer works while having fun.*

---

## Page 2 — Title page

**microtronic computer system**

# Instruction Book
# Part 1

Introduction to microprocessor technology.
Programming and experimenting with the microcomputer.

By Jörg Vallen

Production and distribution:
**BUSCH-Modellspielwaren**
Postfach 1360
D 6806 Viernheim

> Some experiments require additional power:
> a 9 V battery (IEC 6 F 22) or power supply 2059.

In collaboration with:
**ELO-Magazine** Franzis-Verlag
Postfach 370120
8000 München 37

---

## Page 3 — Copyright

Copyright 1981 by
BUSCH GmbH. + Co. KG, Viernheim

All rights reserved.

Illustrations
Atelier Wuthe, Weinheim

Printed in W.-Germany
10/81

---

## Page 4 — The Computer: That Unknown Creature

### The Computer — That Unknown Creature

**A handful of electronics? Unlimited possibilities!**

You can't tell by looking at it — and yet what stands before us
is a technological marvel of our time. A properly functioning
microcomputer, into whose keyboard we enter commands so
that, at the press of a button, it executes those
"programmed" commands.

If we operate it correctly, it will perform the most amazing
feats. Its ability to astonish us is fascinating.

We will witness enormous accomplishments that our
microcomputer will carry out before our very eyes.

Perhaps we are surprised by the "little bit of electronics"
sitting in front of us?

A few years ago you would have filled an entire cabinet with
this "little bit of electronics". Today, electronics has shrunk to
microscopic dimensions, while its performance has reached
astronomical possibilities.

Can we imagine that the roughly 5-cm-long black IC chip with
40 silver pins (on the board under the smoke-tinted plastic
cover) contains around 35,000 transistor functions?

A gigantic electronic switching system.

Now we want to get to know this unknown creature more
closely.

If we had bought, say, a young dog instead of the computer,
the situation would be: dog and human must learn to
understand each other. Each has his own language, which
the other cannot understand. So the owner will probably try to
find out what his new friend understands, which "commands"
he reacts to — or doesn't react to, or perhaps reacts to
incorrectly.

We too must find out which commands our new friend, the
microcomputer, will obey, so that he carries out everything
we expect of him.

If we want to penetrate his deepest secrets, we must work
with him, occupy ourselves intensively with him.

In return, we will experience a technically sophisticated
adventure of a kind that would have been unthinkable for
"home use" only a few years ago.

> By the way, this is "BUSCHI", the BUSCH mascot. He
> demonstrates in his own way how he imagines the function
> of a computer.

---

## Page 5 — Ready for the First Test Run!

### Ready for the First Test Run!

First, we plug the power supply into the wall socket.
Immediately, the dashboard display shows two zeros, a dark
position, and then three zeros. An LED on the computer
board (next to the label "Takt/Clock") starts blinking. We will
not notice any further reaction at first. Our computer is ready
to accept "commands" from us. It is waiting for us to tell it
what to do.

Our microcomputer is prepared to check itself and verify that
all its functions work correctly. This computer self-test gives
us the assurance that nothing was damaged in transit.

We should by no means now start pressing keys randomly,
because our computer doesn't expect nonsense from us, but
rather logical commands. Should we have already produced
"nonsense" before reading these lines, the computer will lock
out this nonsense attempt — i.e. it will not react to any further
key presses.

There is nothing left to do but to inform the computer that we
have just stopped our nonsense activity. For this purpose, we
briefly press the green RESET key on the computer board.
The computer will immediately confirm via its display that it
wants to work with us again (display: **00 000**).

### The Computer Tests Itself — The Test Program

For the self-test, a few cable connections must be made.
Following the diagram, the bare (stripped) wire ends are
inserted into the sockets on the rear of the board and held by
a pressed-on yellow plastic plug. We make sure that the
wires are not pushed too far into the socket, because only
the bare wire end produces the desired contact in the
socket. The four required cables each run from the
numbered output sockets to the numbered input sockets,
with output No. 1 connected to input No. 1, No. 2 to No. 2,
and so on.

*Figure labels (clockwise from top-left):*
- Why does it work?
- Input/output sockets
- LEDs indicating output state
- Clock LED (blinks as soon as the computer is connected to power)
- Power supply for current supply, 220 V/9 V, 250 mA (socket must not have a wobbly contact!)
- Breadboard for building additional circuits with BUSCH-Electronic-Studios
- Reset key
- Microprocessor / computer board
- 6-digit LED display
- Keyboard with 16 entry keys and 8 function keys
- 2 LEDs for computer state display
- Standard sockets for connecting transfer cables
- Special keys

---

## Page 6 — Cable Connections for the Test Program

...continuing from the previous page: from the numbered
output sockets to the numbered input sockets, where output
No. 1 must be connected to input No. 1, No. 2 with No. 2, etc.
Swapped wires lead to an error message from the computer.
(See illustration below.)

We must also know that our computer requires a steady
power supply — that is, the grounded wall socket used to plug
in the power supply must not have a wobbly contact,
otherwise no program execution is possible.

Now we give the computer the command to start its test
program. To do this we press (with a short, light tap) the
"HALT" key, then the "PGM" key. If we now press the "0" key,
the first part of the automatic test program begins. The
display shows in succession:

```
0 0 0 0 0 0
1 1 1 1 1 1
2 2 2 2 2 2
3 3 3 3 3 3
4 4 4 4 4 4
5 5 5 5 5 5
6 6 6 6 6 6
7 7 7 7 7 7
8 8 8 8 8 8
9 9 9 9 9 9
A A A A A A
b b b b b b
C C C C C C
d d d d d d
E E E E E E
F F F F F F
```

The computer demonstrates that it can count: alongside the
digits 0 through 9 it also shows the letters A through F. We
notice that it writes the letters **b** and **d** in lowercase,
while A, C, E and F are written in uppercase.

While the computer counts, we can check that all the
"light-segments" forming the individual digits and letters are
lit correctly.

Once the computer has counted up to "FFFFFF", the two LEDs
on the dashboard left of the display light up and the display
shows:

**00 100**

This message tells us that the computer has correctly
completed the first part of the test program. If we want to run
the same test again, we press HALT – PGM – 0 again and
wait until the run is finished.

Now the computer wants to test its keyboard, to check that
all keys function properly when lightly pressed. The display
shows a "0" at the far right, indicating that we should press
the "0" key. If "0" was pressed correctly, the display shows:

**00 101**

For us this means: press the "1" key. The computer shows 00
102, so press the "2" key. In this way all keys up to "F" are
tested.

If we accidentally press a different key than the one the
computer wants, it immediately recognizes the wrong key
press and the display shows:

```
F E 1 X X
       └─ key actually pressed
     └─── key that should have been pressed
F E means: ERROR!
```

*Figure caption:* **Cable connections for the test program**

---

## Page 7 — A Good Comparison: Computer vs. Human

If we have made a mistake, we press the key requested by
the computer once more (rightmost display digit). If, despite
correct key entry (check carefully), another error message
appears, we should restart the program from the very
beginning to be safe (key "HALT", "PGM", "0"). Perhaps also
check that all cable connections from the outputs to the
inputs have been made correctly. If yet another error
message appears, please send the device — stating the
fault — in the original Styrofoam packaging directly to our
address. Please fill out the registration card accompanying
the device completely; you will receive a replacement
shortly.

Once all keys through "F" have been tested, the computer
continues its test program automatically. The two LEDs to
the left of the display go out and the display shows in
succession:

**00 200**, **00 211**, **00 222**, **00 233**, **00 244**, etc., up to **00 2FF**

The computer counts in the two rightmost positions from 0 to
F. It checks the four inputs and the four outputs. If the
computer does not count up to "00 2FF", the error message
"FE 2XX" appears (the computer shows a digit or letter in the
"X" position). The error message indicates that there is
certainly something wrong with the cable connections
between inputs and outputs. We should check again and also
make sure that all small plastic plugs are pushed firmly home
so that no unwanted wobbly contact arises. Then the test
program is to be restarted from the beginning ("HALT", "PGM",
"0").

If this test was also successfully completed, the lower LED
beside the display lights up and the display turns off for
about 20–30 seconds. During this time another internal test
program runs, in which the computer checks that all
memories etc. are in order. We can tell the computer is still
working by the alternating blinking of the LEDs at the outputs
on the computer board. As soon as this test has completed
successfully, the display shows:

**00 000**

All four LEDs on the computer board (next to the outputs) light
up.

Our computer is ready for new feats.

Should the computer fail to display this final "00 000"
message, a component on the computer board is faulty. The
device would then have to be sent in to us.

Even after a successful test run you should send us the
registration card directly. You will then receive further
information on how your Microtronic computer system can be
expanded with new add-on stages.

If during later experiments we find that the computer does
not work as described in the instruction book, we can use the
test program at any time to check that the computer is
functioning correctly.

### A Good Comparison: Computer vs. Human?

Computers are electronic machines that cannot think
independently. A computer has no intelligence — it
presupposes it!

We must first teach the computer how and when to do what.
Humans too must learn, in their first years of life, to
understand and to act on what they have understood. At first
a person learns only the most important things, e.g. "Mama"
and "Papa". More words are added — sentences are formed
— the person learns to think, see, sense, feel, perceive,
calculate and write. With our sense organs we take in the
information of our environment. It is processed in the brain
and stored in memory.

Instead of the word "information" we can also use the word
"data". Now the principle of "data processing" becomes
clear: take in data (see, hear, feel) — process data (in the
brain) — store data (keep in memory) — output data (show,
speak, write).

"Human data processing" and "electronic data processing"
follow almost the same principle:
**Input data. Process data. Output data.**

A child learns not only from his parents — the parents must
take into account what the child can understand. Something
similar applies to our computer: through a long development
process, the computer has been taught ("pre-programmed")
to understand a special language consisting of many words
("commands"). The computer has its own language ("instruction
set"). Since the computer has no intelligence, we must learn
its "language" so that it is able to carry out our "commands".
The technical entity "computer" has something resembling a
brain: a microprocessor and a memory chip. Its sense organs
(hearing, seeing, feeling) are received via a keyboard and the
data inputs. The output of its stored information (data)
happens via the display, various LEDs, and the outputs.
Whereas in humans the individual…

*Figure labels:*
- Keyboard / Data input
- Memory chip · Microprocessor — "Brain of the computer"
- LED display / Data output
- Take in data — Process data — Output data

---

## Page 8 — The Computer as Play-Partner: The Nim Game

…organs are connected by nerve strands, the computer uses
the "conductor traces" on the computer board and the
microscopic conductor strands inside the microprocessor and
the various IC chips for this purpose.

The illustration shows us that even in "human data
processing" there is no direct connection between the
data-input points (eyes, ears) and the data-output points
(e.g. mouth). All information is forwarded through processing
in the brain. In the computer, too, data cannot travel directly
from the keyboard to the display; rather, it must be
appropriately processed by the microprocessor. The
microprocessor is the "thinking part" of the computer's brain,
while its "knowledge" is stored in the memory chips.

The more intelligent one gives way — so we must learn the
language of our computer. As soon as we master its
language enough to command (program) it, however, it will
do everything we ask of it. We now realize: the computer is a
slave, with no will of its own. It only does what the intelligent
human tells it to do.

Our Microtronic computer learned a lot in years of training at
its developer. For example, a small game has been firmly
anchored in its technical brain (firmly programmed), which it
has not forgotten even during storage and transport. In the
following experiment we want to play against the computer.
Who will win?

**Connecting the piezo buzzer:**
The piezo buzzer must be connected with the correct
polarity. Do not swap the cables! Please follow the
illustration below.

If the buzzer disturbs you (e.g. during pauses in the
following Nim game), disconnect one of the wires.

### The Computer as Play-Partner: The Nim Game

The so-called Nim game (also known under other names) is
a small thinking game for 2 people. It is normally played with
matches.

**Rules of play:**
The players agree that, for example, 15 matches lie on the
table. Each player in turn may take 1, 2, or at most 3 matches
away. Whoever has to take the last match from the table has
lost the game. The thinking therefore goes: toward the end
of the game, arrange the number of remaining matches so
that you yourself are able to take 1–3 matches, so that the
last match remains for your opponent — and he loses the
game.

Our computer is now looking forward to acting as our play
partner and showing what it has already learned. We don't
play with matches; rather, the computer shows us the
progress of the game on the display.

The game is firmly programmed into the computer. We must
help it find this game program in its memory. To do this we
press, in turn, the keys: "HALT", "PGM", "7". As soon as the
computer has found the game in its memory, it reports on the
display: **44 F07**. We confirm that we want to play the game
with it by pressing the keys: "HALT", "NEXT", "0", "0". The
display shows **00 F08** as confirmation that the computer is
ready for the start of the game. We press the "RUN" key — the
game begins: the four LEDs at the outputs are dark, the
signal tone generator (if we have connected the piezo
buzzer per the illustration) has gone silent. The display
shows: **0000**.

*Figure caption:* **Piezo buzzer connection**
