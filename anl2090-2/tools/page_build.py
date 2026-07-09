#!/usr/bin/env python3
"""Reusable page builder for the mark-then-translate workflow.

The user marks translatable-text rectangles with tools/mark_text.py ->
  figures/page-NN.json {"prose":[...], "heading":[...], "table":[...], "targets":[...]}

A per-page script then supplies the English text and lets this module emit
layout/page-NN.json + translations/page-NN.en.json, which build_page_html reads.

Every overlay white-outs its box with a pad-0 (tight) mask at the EXACT marked
coordinates, so it never bleeds onto a frame. Anything not marked is preserved.

Typical per-page script:

    from page_build import PageBuild
    P = PageBuild(ROOT, 30); M = P.marks
    P.prose(M["prose"][0], "English paragraph 1 ...")
    P.prose(M["prose"][1], "English paragraph 2 ...")
    P.whiteout(M["heading"][0]); P.heading(M["targets"][0], "Heading text", fs=15)
    P.write()
"""
import json

PPM = 2480 / 210.0
Z = lambda s: f'&bdquo;{s}&ldquo;'          # German low-high quotes for labels
NDASH, TIMES, DIV = '&ndash;', '&times;', '&divide;'
FONT = 'font-family:Helvetica,Arial,sans-serif;color:#111;'


class PageBuild:
    def __init__(self, root, nn, align=True):
        self.root, self.nn = root, nn
        self.blocks, self.en = [], {}
        try:
            self.marks = json.load(open(f"{root}/figures/page-{nn:02d}.json"))
        except FileNotFoundError:
            self.marks = {"prose": [], "heading": [], "table": [], "targets": []}
        if align:
            self._align()

    def _align(self, tol=14, min_w=300):
        """RULE: prose + heading boxes in the same column share their LEFT edge.
        Hand-marked (mouse-drag) xmins flutter a few px, so a heading rarely starts
        at exactly the body-text margin. Snap the LEFT edge (xmin) of every wide
        prose/heading box to its cluster's OUTER (leftmost) edge, so headings sit
        flush with their prose column and each column keeps one clean left margin.
        Snapping to the leftmost is mask-safe -- a pad-0 mask only ever extends
        left, never exposing German. Only xmin moves; xmax / y and every TABLE
        (Erklaerungen) box stay exactly as marked (those are tight, per-cell).
        Columns fall in their own clusters (the left/right gap >> tol) and are
        aligned independently."""
        boxes = [b for cat in ("prose", "heading")
                 for b in self.marks.get(cat, []) if b[2] - b[0] >= min_w]
        if len(boxes) < 2:
            return
        xs = sorted({b[0] for b in boxes})
        clusters, cur = [], [xs[0]]
        for v in xs[1:]:
            if v - cur[-1] <= tol:
                cur.append(v)
            else:
                clusters.append(cur); cur = [v]
        clusters.append(cur)
        left = {v: c[0] for c in clusters for v in c}   # c[0] = cluster leftmost
        for b in boxes:
            b[0] = left[b[0]]

    # ---- core ----
    def _add(self, bbox, html, tight=None):
        i = len(self.blocks)
        blk = {"kind": "body", "bbox": list(bbox), "fragments": [list(bbox)],
               "lines": [list(bbox)], "text": ""}
        if tight is not None:
            # mask ONLY the tight rects (pad 0); suppress the default bbox mask
            # with a 1px throwaway rect up in the page margin.
            blk["mask_lines"] = True
            blk["lines"] = [[2, 2, 3, 3]]; blk["fragments"] = [[2, 2, 3, 3]]
            blk["tight_masks"] = [list(r) for r in tight]
        self.blocks.append(blk)
        self.en[str(i)] = {"de": "", "en": html}
        return i

    # ---- white-out a marked box (no text) ----
    def whiteout(self, box):
        self._add(box, "<div></div>", tight=[box])

    # ---- a body paragraph fit into (and white-ing out) its box ----
    def prose(self, box, html, fs=11, lh=1.06, justify=True):
        al = 'justify' if justify else 'left'
        # set font-size on the <p> too — the build CSS (.ovr.body p) otherwise
        # forces it to 9pt and overrides the wrapper div.
        self._add(box, f'<div style="{FONT}font-size:{fs}pt;line-height:{lh};'
                  f'text-align:{al}"><p style="margin:0;font-size:{fs}pt;'
                  f'line-height:{lh}">{html}</p></div>', tight=[box])

    # ---- a heading / caption / label placed at an exact box ----
    def heading(self, box, html, fs=13, bold=True, center=False,
                nowrap=True, whiteout=True, lh=1.1):
        w = 700 if bold else 400
        al = 'center' if center else 'left'
        ws = 'white-space:nowrap;' if nowrap else ''
        self._add(box, f'<div style="{FONT}font-size:{fs}pt;font-weight:{w};'
                  f'{ws}text-align:{al};line-height:{lh}">{html}</div>',
                  tight=[box] if whiteout else None)

    # ---- raw html overlay (e.g. a rebuilt HTML table) at a box ----
    def raw(self, box, html, whiteout=True, extra_white=None):
        rects = []
        if whiteout:
            rects.append(box)
        if extra_white:
            rects += [list(r) for r in extra_white]
        self._add(box, html, tight=rects or None)

    # ---- re-draw a thin black line (frame/rule segment the white-out covered) ----
    def line(self, box):
        self._add(box, f'<div style="width:100%;height:100%;background:#111">'
                  f'</div>', tight=[box])

    def write(self):
        layout = {"page_size_px": [2480, 3507], "dpi": 300, "px_per_mm": PPM,
                  "text_blocks": self.blocks, "raw_blocks": []}
        json.dump(layout, open(f"{self.root}/layout/page-{self.nn:02d}.json", "w"),
                  indent=2)
        json.dump(self.en,
                  open(f"{self.root}/translations/page-{self.nn:02d}.en.json", "w"),
                  indent=2, ensure_ascii=False)
        print(f"page-{self.nn:02d}: {len(self.blocks)} overlay blocks "
              f"(prose {len(self.marks.get('prose', []))}, "
              f"heading {len(self.marks.get('heading', []))}, "
              f"table {len(self.marks.get('table', []))}, "
              f"targets {len(self.marks.get('targets', []))})")
