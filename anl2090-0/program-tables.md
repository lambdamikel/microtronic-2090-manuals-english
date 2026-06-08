# Microtronic Computer System — English Translation

Translation of the German bookmark/quick-reference insert (Busch GmbH, Nr. 20904)
that ships with the *Busch 2090 Microtronic Computer System* manual.

---

## Page 1

### Quick-Start Information

After plugging the power supply into a 220 V outlet, the computer is ready
to operate. The display (LED display) shows: **00 000**. The power supply
is VDE-approved. It is a safety transformer that converts the 220 V mains
voltage into the 10 V operating voltage required by the computer.

### Built-in Programs

A number of easily accessible built-in programs are stored in the computer.
They are called up by pressing the function keys (on the right-hand side of
the dashboard panel): **HALT – PGM – 0** (or by entering the corresponding
number). To understand the built-in-program functions you should consult the
matching pages of the instruction manual:

* PGM 0 = Test program (see page 4–6)
** PGM 1 = Load program from cassette into computer (see note)
** PGM 2 = Load program from computer onto cassette (see note)
* PGM 3 = Enter time of day (page 8–9)
* PGM 4 = Display time of day (page 8–9)
  PGM 5 = Delete self-programmed programs (page 31)
  PGM 6 = Write the NOP instruction into every address of program memory
          (page 63)
* PGM 7 = "Nim" game (page 7–8)

\* These programs are suitable as demonstration programs.

\*\* If PGM 1 or PGM 2 are started without an attached interface, the computer
must be re-activated for operation with the RESET key (see page 4).

To select a different built-in program, first press **HALT**, then **PGM**,
and finally the program number.

### Interesting and Easily Programmable Demonstration Programs

The corresponding instructions from the manual must be programmed (entered).
Programming always starts with the keys **HALT – NEXT** followed by pressing
the number key **00** twice. Then the input instructions are entered with
the number and letter keys. An instruction always consists of a 3-digit
code, e.g. F05. After each instruction entry the **NEXT** key must be
pressed. The next instruction is then accepted. The "address" (shown by the
two left-most digits of the display) automatically increments after every
instruction entry (from 00 to 01, etc.).

| Program                                 | Page                   |
|-----------------------------------------|------------------------|
| Electronic die                          | 10–11                  |
| Automatic counter                       | 12                     |
| "The Moon Landing"                      | 23–24                  |
| Timer — the computer as a time switch   | 38–39                  |
| Lotto-number generator                  | 42                     |
| Computer as alarm clock                 | 45–46                  |
| Reaction test for two persons           | 55                     |
| Reaction test "de luxe"                 | 55–57                  |
| Arithmetic program "Multiplication"     | 61                     |
| Arithmetic program "Division"           | 62                     |
| Tic-Tac-Toe (computer board game)       | Manual, Part 2         |
| Sea battle                              | Manual, Part 2         |
| Code breaker                            | Manual, Part 2         |
| "Nim 2"                                 | Manual, Part 2         |
| Morse-code decoder                      | Manual, Part 2         |

### Function-Key Short Description

(detailed description see page 72–73)

| Key   | Function |
|-------|----------|
| HALT  | Cancel program execution |
| NEXT  | Displays the next following instruction in program memory. The instruction can be modified and, after pressing the NEXT key again, stored in program memory. |
| BKP   | Break-point (consult page 72) |
| REG   | Inspection and modification key for the working registers |
| C/CE  | Clear key for incorrectly entered instructions |
| RUN   | Program-start key (in combination with HALT – NEXT and entry of the start address, e.g. B 00) |
| STEP  | Single-step key for stepwise checking of program execution |
| PGM   | Call-up key for the built-in programs |

**Number and digit keys:** 1 to 9 and A to F — entry keys for programming
and for value input.

**Red function keys G and H:** Special-purpose keys for connecting input
signals.

**Green RESET key:** Located on the computer circuit board; serves to
re-activate the computer's operating system after faulty programming.

#### Comparison Decimal ↔ Hexadecimal Number System

(Dec. = Decimal, Hex. = Hexadecimal — table covering values 0 – 255 / 00 – FF)

---

## Page 2 — Bookmark

### Quick-Reference Information for Programming

#### The Microtronic Instruction Set
(see also instruction manual page 74 to 76)

Columns: Mnemonic · Instruction code · Explanation · Page (detailed example)

| Mnemonic | Code | Description | Meaning | Page |
|----------|------|-------------|---------|------|
| MOV  | 0 s d | s into d                | Move contents of register s into register d            | 22    |
| MOVI | 1 n d | n into d                | Move constant n into register d                        | 33    |
| AND  | 2 s d | s AND d = d             | Logical AND operation                                  | 59–60 |
| ANDI | 3 n d | n AND d = d             | Logical AND with a constant                            | 59–60 |
| ADD  | 4 s d | s ⊕ d = d               | Addition of register contents s ⊕ d = result in d      | 18–21 |
| ADDI | 5 n d | n ⊕ d = d               | Addition of constant n ⊕ Reg. d = result in d          | 19–21 |
| SUB  | 6 s d | d ⊖ s = d               | Subtraction of register contents d ⊖ s = result in d   | 35    |
| SUBI | 7 n d | d ⊖ n = d               | Subtraction d ⊖ constant n = result in d               | 35    |
| CMP  | 8 s d | Compare s, d            | Compare contents of register s with register d         | 74    |
| CMPI | 9 n d | Compare n, d            | Compare constant n with register d                     | 26    |
| OR   | A s d | s OR d = d              | Logical OR operation                                   | 59–60 |
| CALL | B a a | Jump to subroutine starting at address a a             |       | 63–64 |
| GOTO | C a a | Jump a a                | Jump to an arbitrary address a a                       | 14–15 |
| BRC  | D a a | Carry jump a a          | Jump to address a a if carry-flag set                  | 26    |
| BRZ  | E a a | Zero jump a a           | Jump to address a a if zero-flag set                   | 33    |
| MAS  | F 7 d | A-Reg. → S-Reg.         | Move working register d into memory register d         | 61    |
| INV  | F 8 d | Invert d                | Invert contents of register d                          | 50    |
| SHR  | F 9 d | Shift d right           | Shift register d binarily to the right                 | 49    |
| SHL  | F A d | Shift d left            | Shift register d binarily to the left                  | 48    |
| ADC  | F B d | d ⊕ C = d               | Set carry-flag adds "1" to register d                  | 19–21 |
| SUBC | F C d | d ⊖ C = d               | Set carry-flag subtracts "1" from register d           | 35    |
| DIN  | F D d | Data in                 | Store data from input into register d                  | 37    |
| DOT  | F E s | Data out                | Output data from register s to outputs                 | 36    |
| KIN  | F F d | Key value               | Wait for key entry. Store entered value in register d  | 14–15 |
| DISP | F n s | Display on              | Show: n = how many (reg.) digits, s = from register no.| 14–15 |
| HALT | F 0 0 | Program stop            | Halted program can be resumed with STEP key            | 63    |
| NOP  | F 0 1 | No operation            | An instruction code may be added later                 | 63    |
| DISOUT| F 0 2 | Display off            | Switch display off (for faster running)                | 14–15 |
| HXDZ | F 0 3 | Display in              | Convert hex → decimal in register D-E-F                | 43    |
| DZHX | F 0 4 | Dec to hex              | Convert decimal → hex in register D-E-F                | 43    |
| RND  | F 0 5 | Random generator        | Generate random numbers in registers D-E-F             | 41    |
| TIME | F 0 6 | Clock time              | Move time of day into registers A-B-C-D-E-F            | 44–45 |
| RET  | F 0 7 | Return                  | Return from a subroutine to the main program           | 63–64 |
| CLEAR| F 0 8 | Clear registers         | Set all register values to "0"                         | 21    |
| STC  | F 0 9 | Set carry               | Carry-flag is set (value: 1)                           | 52    |
| RSC  | F 0 A | Reset carry             | A set carry-flag is reset (0)                          | 52    |
| MULT | F 0 B | Multiplication          | Multiplication is performed in registers 0 to 5        | 61–62 |
| DIV  | F 0 C | Division                | Division is performed in registers 0 to 3              | 62–63 |
|      |       |                         | (Reg. 4 and 5 value "0")                               |       |
| EXRL | F 0 D | Exchange A/S 0–7        | Swap contents of working registers 0–7 with memory registers 0–7 | 61 |
| EXRM | F 0 E | Exchange A/S 8–F        | Swap contents of working registers 8–F with memory registers 8–F | 61 |
| EXRA | F 0 F | Exchange 0–7 / 8–F      | Swap contents of working registers 0–7 with working registers 8–F| 33 |

Footnotes:
- For **d** the register number is entered. Register d contains the result after instruction execution. (page 15)
- For **s** the register number is entered. Register s is not modified by instruction execution. (page 16)
- For **n** a constant (the same in all operations) value is entered. (page 74)
- For **a a** the jump address (the address number to jump to) is entered. (page 15/74)

#### The Number Systems

| Decimal | Hex | Binary | Inverted Binary / Hex |
|---------|-----|--------|------------------------|
| 0       | 0   | 0000   | 1111   F |
| 1       | 1   | 0001   | 1110   E |
| 2       | 2   | 0010   | 1101   D |
| 3       | 3   | 0011   | 1100   C |
| 4       | 4   | 0100   | 1011   B |
| 5       | 5   | 0101   | 1010   A |
| 6       | 6   | 0110   | 1001   9 |
| 7       | 7   | 0111   | 1000   8 |
| 8       | 8   | 1000   | 0111   7 |
| 9       | 9   | 1001   | 0110   6 |
| 10      | A   | 1010   | 0101   5 |
| 11      | B   | 1011   | 0100   4 |
| 12      | C   | 1100   | 0011   3 |
| 13      | D   | 1101   | 0010   2 |
| 14      | E   | 1110   | 0001   1 |
| 15      | F   | 1111   | 0000   0 |

The binary system can be represented by the LEDs at the 4 outputs: 4 3 2 1
The 4 outputs have the values: 8 4 2 1

#### Symbols for Flowcharts

- Rectangle: General operation
- Diamond: Branching
- Rectangle with double sides: Subroutine
- Parallelogram: Input/Output
- Rounded rectangle: Beginning or end of a program
- Circle: Connector / transition to other program parts
- `>` means: greater
- `<` means: smaller
- `=` means: equal value

**BUSCH GmbH**
Postfach 1360
D-6806 Viernheim

---

## Page 3 — Cover page of the program-sheet pad

### Notes for Microtronic Programmers — on Using the Program Tables

The enclosed program lists are for the development of self-designed programs.

**Register allocation:** It is important to keep track of the registers
required by a program and their contents.

**Jump target:** Entry for short labels indicating at which addresses special
program parts begin that are jumped to from another program part.

**Address-Nr.:** It is practical to start a program at address 00. When
programming, the computer automatically assigns the further address
numberings. The address number is given to 2 hex digits, and it is
recommended that the address number be supplemented, e.g. 10, 1F, etc.

**Input instruction code:** The instruction codes to be programmed are
entered in this column.

**Mnemonic (Befehls-Kürzel):** Noting the mnemonic, such as MOV, GOTO etc.,
is advisable so that, in case of troubleshooting, the program is clearer.

**Jump-to:** Here it can be indicated by a short label from where individual
program jumps are made.

**Explanations:** Important lines of thought can be recorded in this column.

The bookmark (in the manual) is an important helper containing all
necessary quick-reference information.

Have fun programming and experimenting.

**BUSCH**

Nr. 20904

---

## Page 4 — Blank Program List Form

**Program list for Microtronic Computer System 2090**

Fields:
- Program name: ____   Sheet no.: ____
- Programmer: ____     Date: ____

**Register allocation**
- Register-Nr.: 0 1 2 3 4 5 6 7 8 9 A B C D E F
- Register contents: (blank cells)

Then a table with the columns:
- **Jump target** (Sprungziel)
- **Address Nr.** (Adresse Nr.) — addresses 0 through F repeated three times (0–F, 0–F, 0–F)
- **Input / Instruction code** (Eingabe Befehls-Code)
- **Mnemonic** (Befehlskürzel)
- **Jump to** (Sprung nach)
- **Explanations** (Erklärungen)

(blank rows for hand-written entries)

BUSCH GmbH + Co. KG, Viernheim/W.-Germany — Order no. 20904
