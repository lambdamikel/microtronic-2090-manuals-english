# Busch Microtronic 2090 — Computer System Manual (English)

An English translation of the **Busch Microtronic 2090** *Computer System* instruction book,
the manual for Busch's 1981 4‑bit educational microcomputer kit. Both parts are included:
**Part 1** (*Introduction to microprocessor and computer technology*, 82 pp) and **Part 2**
(*An interesting selection of large computer programs*, 83 pp). The English text is overlaid
onto the original scanned pages, so the layout, figures, cartoons and program listings are
preserved exactly as in the German original.

Also included is the companion book **Computer Spiele** (*Computer Games*, Busch Nr. 2094) —
25 games and experiments to program yourself on the Microtronic 2090, from Black Jack and
Roulette to a chess clock, a code lock and a prime‑number benchmark.

## 📚 Read the manual

| | |
|---|---|
| 📖 **Part 1 — PDF** | **[Busch_Microtronic_2090_Manual_EN.pdf](Busch_Microtronic_2090_Manual_EN.pdf)** — full 82‑page manual (Part 1), A4 |
| 🌐 **Part 1 — online** | **<https://lambdamikel.github.io/microtronic-2090-manuals-english/>** — read in your browser, with a clickable table of contents |
| 📖 **Part 2 — PDF** | **[Busch_Microtronic_2090_Manual_Part2_EN.pdf](Busch_Microtronic_2090_Manual_Part2_EN.pdf)** — full 83‑page manual (Part 2), A4 |
| 🌐 **Part 2 — online** | **<https://lambdamikel.github.io/microtronic-2090-manuals-english/part2.html>** — the large‑program collection, with a clickable table of contents |
| 🎲 **Computer Games (2094) — PDF** | **[Busch_Microtronic_2094_Computer_Games_EN.pdf](Busch_Microtronic_2094_Computer_Games_EN.pdf)** — the full *Computer Spiele* book, 66 sheets (printed pages 1–64) including the covers and the two loose game boards |
| 🌐 **Computer Games (2094) — online** | **<https://lambdamikel.github.io/microtronic-2090-manuals-english/computer-games.html>** — 25 games and experiments, with a clickable table of contents |
| 📑 **Program Tables / quick reference** | the bookmark insert (Busch Nr. 20904): **[PDF](Busch_Microtronic_2090_Program_Tables_EN.pdf)** · **[HTML](https://lambdamikel.github.io/microtronic-2090-manuals-english/program-tables.html)** — instruction set, function keys, number‑system conversion tables |

## Copyright & permission

The original German manual is **© Busch GmbH & Co. KG**, Heidelberger Straße 26, 68519
Viernheim, Germany. The Microtronic 2090 and its manuals were designed and written by
**Jörg Vallen**.

This English translation is a non‑commercial fan / preservation work and is **hosted with
the kind permission of Jörg Vallen, Managing Director (CEO) of Busch GmbH & Co. KG**, who
generously granted permission for the Microtronic manuals to be published for preservation
by **Michael Wessel** ([lambdamikel](https://github.com/lambdamikel)) — see the
[permission on record](https://github.com/lambdamikel/Busch-2090/blob/master/manuals/permission-to-include-manuals-here-from-busch.txt).

All trademarks, the original text and the original artwork remain the property of their
respective owners. This project is **not affiliated with or endorsed by Busch GmbH & Co. KG**.
See [COPYRIGHT.md](COPYRIGHT.md) for details.

## How it was made

This English edition was produced by **Claude Opus 4.8** (Anthropic) running as an *agentic*
coding assistant in Claude Code, directed page‑by‑page by Michael Wessel. Rather than
re‑typesetting the book, the goal was to keep the original 1981 layout perfectly intact: for
each of the 165 scanned pages across both parts the AI looked at the page image, translated
the German, and wrote a precise overlay that masks the German with white and prints the
English in its place — while leaving every figure, photograph, cartoon (with its
hand‑lettered German speech bubbles) and circuit diagram untouched. Program listings and data
tables were re‑drawn in English, and the red cover banners and the two‑column table of
contents were rebuilt to match the originals. Part 2 added its own challenges — long two‑page
machine‑code program listings with a translated "Explanation" column, model‑railway wiring
schematics, flow charts (kept in German by design) and the BUSCH product‑catalogue back
matter, including a white‑on‑red back‑cover advert.

The work ran as a tight build‑and‑inspect loop. A small Python pipeline (extract layout →
write the English JSON → auto‑fit tables → render HTML → PDF via headless Chrome) does the
mechanics, but the AI drives it: it measures each text block's geometry straight from the
pixels, picks fonts and bounding boxes, then renders every page back to an image and checks
it for trouble — German bleeding past a mask, a flow‑chart line hidden under a caption, a
page number clipped, a table overrunning the margin — and iterates until the page is clean.
It was done in batches of eight sheets across several sessions, with Michael reviewing each
batch and requesting fixes (column breaks, alignment nudges, cover wording) that were folded
back in. The same `tools/` are included here so the whole manual can be re‑rendered from the
scans + translation JSON.

The *Computer Spiele* book (2094) was translated the same way, by **Claude Opus 5**, and
added a few problems of its own. Its scans were skewed, so every sheet is deskewed by a
projection‑profile search before anything else happens; Michael hand‑marked each text block
with an interactive tool, which lifts OCR accuracy on these mixed prose‑and‑hex‑table pages
from roughly 60 % to over 90 %. Game‑board artwork is translated in place — the word ZIEL is
replaced letter by letter with GOAL inside the grid squares, a flow chart is relabelled
without disturbing its boxes and arrows, and a vertical axis caption is re‑set bottom‑to‑top.
The red covers needed masks painted in the page colour sampled from the scan rather than the
usual white. Four checkers guard the result: overflow (English overrunning its box), graphics
(a mask eating a figure), residue (German surviving just outside a mask) and coverage (a
marked block that never got a translation).

The pipeline (in `anl2090-1/tools/`):

| tool | role |
|---|---|
| `extract_layout.py` | OCR/segment each scan into text blocks (bounding boxes) |
| `build_page_html.py` | render the English overlay (`translations/page-NN.en.json`) onto each scan → HTML (→ PDF via headless Chrome) |
| `autofit_tables.py` | binary‑search font sizes so re‑drawn tables fill their region |
| `check_graphics.py` | flag any figure/line accidentally covered by a text mask |
| `make_site.py` | wrap the rendered HTML into this GitHub Pages site (lazy images, anchors, TOC) |

Data lives alongside the tools in each part's folder (`anl2090-1/` for Part 1, `anl2090-2/`
for Part 2): `pages/` (scans), `layout/` (block geometry), `translations/` (the English text),
`contents.json` (TOC). Part 2 was built with the same pipeline plus a small
`mark_text.py` / `page_build.py` "mark‑then‑translate" step: Michael marks the translatable
text rectangles on each scan and the AI fills, translates and lays out the English overlay.

Rebuild the sites locally:

```bash
# Part 1
python3 anl2090-1/tools/build_page_html.py --root anl2090-1 --pages 1-82 --out index.html
python3 anl2090-1/tools/make_site.py index.html

# Part 2
python3 anl2090-2/tools/build_page_html.py --root anl2090-2 --pages 1-83 --out part2.html
python3 anl2090-2/tools/make_site.py part2.html
```

## Roadmap

- [x] **Part 1** — *Introduction to microprocessor and computer technology*
- [x] **Part 2** — *An interesting selection of large computer programs*
- [ ] The **"Computerspiele"** (computer games) book

## Credits

English translation, tooling and hosting by **Michael Wessel**
([lambdamikel](https://github.com/lambdamikel) · <https://www.michael-wessel.info>), who also
maintains the [Busch‑2090 emulator & preservation project](https://github.com/lambdamikel/Busch-2090).
The English translation and rendering pipeline were produced by **Claude Opus 4.8** (Anthropic)
working as an agentic AI under his direction.
Original manual by Jörg Vallen / Busch GmbH & Co. KG — published here with his permission.
