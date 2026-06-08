#!/usr/bin/env python3
"""Turn the raw build_page_html.py output (index.html) into a GitHub-Pages-ready site:

  * lazy-load every page scan (<img class="bg" loading="lazy">) so the 82 images stream in,
  * give every page a stable anchor (id="page-N") for deep links,
  * prepend a header with the title, the copyright / permission notice, and a clickable
    table of contents (chapter -> page anchor) read from anl2090-1/contents.json.

Usage:  python3 anl2090-1/tools/make_site.py index.html
        (edits the file in place)

The chapter list uses the manual's PRINTED page numbers; printed page P is the (P+1)-th
physical sheet, i.e. anchor #page-{P+1}.
"""
import sys, json, html, pathlib

HEADER_CSS = """
<style>
  .site-header{max-width:210mm;margin:12mm auto 0;padding:0 6mm;
    font-family:"Helvetica Neue",Helvetica,Arial,sans-serif;color:#eee}
  .site-header h1{font-size:1.6rem;margin:.2rem 0}
  .site-header .lead{color:#cfcfcf;margin:.2rem 0 1rem}
  .notice{background:#1f1f1f;border:1px solid #444;border-radius:8px;padding:.9rem 1.1rem;
    font-size:.86rem;line-height:1.5;color:#ddd}
  .notice b{color:#fff}
  .toc{background:#fff;color:#111;border-radius:8px;padding:1rem 1.2rem;margin:1rem 0 0}
  .toc h2{font-size:1.05rem;margin:.1rem 0 .6rem}
  .toc ol{margin:0;padding:0;list-style:none;columns:2;column-gap:2.2rem;font-size:.82rem}
  .toc li{break-inside:avoid;display:flex;justify-content:space-between;gap:.6rem;
    padding:.08rem 0;border-bottom:1px dotted #ccc}
  .toc a{color:#0a4;text-decoration:none}
  .toc a:hover{text-decoration:underline}
  .toc .pg{color:#888;white-space:nowrap}
  @media(max-width:760px){.toc ol{columns:1}}
</style>
"""

NOTICE = """
<div class="notice">
  <b>Busch Microtronic 2090 — Instruction Book, Part 1 (English translation).</b><br>
  Original German manual <b>&copy; Busch GmbH &amp; Co. KG</b>, Heidelberger Stra&szlig;e 26,
  68519 Viernheim, Germany. The Microtronic 2090 and its manuals were designed and written by
  <b>J&ouml;rg Vallen</b>. This English translation is a fan/preservation work and is
  <b>hosted with the kind permission of J&ouml;rg Vallen, Managing Director (CEO) of Busch
  GmbH &amp; Co. KG</b>, who granted permission for the Microtronic manuals to be published
  for preservation (<a href="https://github.com/lambdamikel/Busch-2090/blob/master/manuals/permission-to-include-manuals-here-from-busch.txt" style="color:#6cf">permission on record</a>).
  English translation, tooling and hosting by <b>Michael Wessel</b>
  (<a href="https://github.com/lambdamikel" style="color:#6cf">lambdamikel</a>), the recipient
  of that permission &mdash; see the
  <a href="https://github.com/lambdamikel/Busch-2090" style="color:#6cf">Busch&#8209;2090 project</a>
  and <a href="https://www.michael-wessel.info" style="color:#6cf">michael-wessel.info</a>.
  The English translation and rendering pipeline were produced by <b>Claude Opus 4.8</b>
  (Anthropic) working as an agentic AI, under Michael Wessel's direction.
  All trademarks and the original artwork remain the property of their
  respective owners. Not affiliated with or endorsed by Busch GmbH &amp; Co. KG.
</div>
"""

def build_header(contents):
    items = []
    for title, page in contents:
        anchor = f"page-{page + 1}"  # printed page P -> physical sheet P+1
        items.append(f'<li><a href="#{anchor}">{html.escape(title)}</a>'
                     f'<span class="pg">{page}</span></li>')
    toc = ('<div class="toc"><h2>Contents &mdash; Part 1</h2><ol>'
           + "".join(items) + "</ol></div>")
    return (HEADER_CSS
            + '<div class="site-header">'
            + '<h1>Busch Microtronic 2090 &mdash; Computer System Manual (English)</h1>'
            + '<p class="lead">Programming &ndash; Experimenting &ndash; learning playfully '
              'how a computer works.</p>'
            + NOTICE + toc + '</div>\n')

def main():
    path = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "index.html")
    contents = json.load(open(path.parent / "anl2090-1" / "contents.json", encoding="utf-8"))
    doc = path.read_text(encoding="utf-8")

    doc = doc.replace('<img class="bg"', '<img loading="lazy" class="bg"')
    # anchor each page section
    for line in [l for l in doc.splitlines() if '<section class="page" data-page=' in l]:
        n = line.split('data-page="')[1].split('"')[0]
        doc = doc.replace(line, line.replace('<section class="page"',
                                             f'<section class="page" id="page-{n}"'), 1)
    doc = doc.replace("<body>", "<body>\n" + build_header(contents), 1)

    path.write_text(doc, encoding="utf-8")
    print(f"site-ified {path} ({len(contents)} TOC chapters)")

if __name__ == "__main__":
    main()
