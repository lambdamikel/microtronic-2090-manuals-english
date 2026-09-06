import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from page_build import PageBuild
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
b = PageBuild(ROOT, 33)

b.heading([158,52,1250,194], "Forming Words and Sentences", fs=15)

b.prose([158,370,1250,1146],
 "With this program MICROTRONIC can display simple words and form sentences.<br><br>"
 "The letters A &ndash; F are available for showing such words on the display. "
 "In addition the digit zero can be used as the letter &ldquo;o&rdquo;, the "
 "digit 1 as &ldquo;i&rdquo; and the digit 5 as &ldquo;s&rdquo;. This gives 9 "
 "different letters, which can be put together by suitable programming into "
 "short German words such as AFFE, EI, BOESE, BADE, SIE, SOFT, BABIE, IDA and so "
 "on.<br><br>"
 "The following program forms more or less sensible sentences from such words, "
 "whereby well-meant computer advice such as &ldquo;BADE BEI EBBE&rdquo; (bathe "
 "at low tide) need not necessarily be followed, and small cheeky remarks "
 "(&ldquo;SIE AFFE&rdquo; &ndash; you ape) should on no account be taken "
 "personally.", fs=10.4)

b.heading([156,1170,754,1252], "Function description:", fs=12.6)

b.prose([158,1274,1252,2318],
 "After HALT &ndash; NEXT &ndash; 00 the program is entered.<br>"
 "Program start: HALT &ndash; NEXT &ndash; 00 &ndash; RUN.<br><br>"
 "The display shows the words for two sentences one after the other and then "
 "switches off. After pressing key 0 the computer brings the next sentences, "
 "until the display goes dark again. Key 0 calls up the sentences that follow. "
 "This goes on until the computer takes its leave with &ldquo;ADE&rdquo; "
 "(farewell). Pressing key 0 once more restarts the program.<br><br>"
 "This program is only meant to give a few ideas for programming similar "
 "comments for games and the like yourself. Once the MICROTRONIC instruction "
 "books have been worked through, the structure of the program is simple: MOVI "
 "instructions move the appropriate letters and numbers into the registers, and "
 "DISP instructions then show them. The subroutines from address AD and B3 "
 "generate pauses so that the words are shown on the display for a short "
 "time.", fs=10.4)

# ---- right column ------------------------------------------------------
b.prose([1288,370,2396,1014],
 "The use of this is demonstrated in the following game &ldquo;17 + 4&rdquo;, "
 "where the computer pays the winner a compliment (in English): &ldquo;GOOD&rdquo;, "
 "or tells the loser with &ldquo;BAD&rdquo; that their result was poor.<br><br>"
 "With a little thought many more words can be formed from the 9 available "
 "letters, whereby the spelling &ldquo;&szlig;&rdquo; (at the end of a word) has "
 "to be turned into &ldquo;ss&rdquo;, e.g. &ldquo;FASS&rdquo; (instead of "
 "Fa&szlig;). Further examples of words: ABI (Abitur), ABBA (pop group), AS "
 "(playing card), BASS (musical instrument), FASSE, ESSE, OB, SAFE, SIEB, SIE, "
 "ES, SASS and so on.", fs=10.4)

b.heading([1286,1026,2378,1136],
    "Programmer: Frank Simon, 6342 Haiger 6", fs=11, bold=False)
b.write()
