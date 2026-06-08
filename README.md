# Busch Microtronic 2090 — Computer System Manual (English)

An English translation of the **Busch Microtronic 2090** *Computer System* instruction
book (Part 1), the manual for Busch's 1981 4‑bit educational microcomputer kit. The English
text is overlaid onto the original scanned pages, so the layout, figures, cartoons and
program listings are preserved exactly as in the German original.

## 📚 Read the manual

| | |
|---|---|
| 📖 **PDF** | **[Busch_Microtronic_2090_Manual_EN.pdf](Busch_Microtronic_2090_Manual_EN.pdf)** — full 82‑page manual, A4 |
| 🌐 **Online (HTML)** | **<https://lambdamikel.github.io/microtronic-2090-manuals-english/>** — read in your browser, with a clickable table of contents |

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
each of the 82 scanned pages the AI looked at the page image, translated the German, and wrote
a precise overlay that masks the German with white and prints the English in its place — while
leaving every figure, photograph, cartoon (with its hand‑lettered German speech bubbles) and
circuit diagram untouched. Program listings and data tables were re‑drawn in English, and the
red cover banners and the two‑column table of contents were rebuilt to match the originals.

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

The pipeline (in `anl2090-1/tools/`):

| tool | role |
|---|---|
| `extract_layout.py` | OCR/segment each scan into text blocks (bounding boxes) |
| `build_page_html.py` | render the English overlay (`translations/page-NN.en.json`) onto each scan → HTML (→ PDF via headless Chrome) |
| `autofit_tables.py` | binary‑search font sizes so re‑drawn tables fill their region |
| `check_graphics.py` | flag any figure/line accidentally covered by a text mask |
| `make_site.py` | wrap the rendered HTML into this GitHub Pages site (lazy images, anchors, TOC) |

Data lives alongside the tools: `anl2090-1/pages/` (scans), `anl2090-1/layout/` (block
geometry), `anl2090-1/translations/` (the English text), `anl2090-1/contents.json` (TOC).

Rebuild the site locally:

```bash
python3 anl2090-1/tools/build_page_html.py --root anl2090-1 --pages 1-82 --out index.html
python3 anl2090-1/tools/make_site.py index.html
```

## Roadmap

- [x] **Part 1** — *Introduction to microprocessor and computer technology* (this manual)
- [ ] **Part 2** — *An interesting selection of large computer programs*
- [ ] The **"Computerspiele"** (computer games) book

## Credits

English translation, tooling and hosting by **Michael Wessel**
([lambdamikel](https://github.com/lambdamikel) · <https://www.michael-wessel.info>), who also
maintains the [Busch‑2090 emulator & preservation project](https://github.com/lambdamikel/Busch-2090).
The English translation and rendering pipeline were produced by **Claude Opus 4.8** (Anthropic)
working as an agentic AI under his direction.
Original manual by Jörg Vallen / Busch GmbH & Co. KG — published here with his permission.
