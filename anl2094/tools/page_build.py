#!/usr/bin/env python3
"""Reusable page builder for the mark-then-translate workflow.

NOTE: after building, run tools/check_overflow.py for the page. English is
often longer than the German it replaces, and an overlay that overruns its
box is not clipped - it spills onto whatever is below. A 5 px overrun is
invisible in review and wrong in print.

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
    def __init__(self, root, nn, align=True, mask_color=None, ink="#111",
                 crop=None):
        """mask_color / ink: the covers print white text on red, where the
        default white mask would punch a hole in the artwork. Set them per page
        (or per call) to paint the mask in the page colour and the text in the
        colour it replaces."""
        self.root, self.nn = root, nn
        self.mask_color, self.ink = mask_color, ink
        # crop=(left, top, right, bottom) px trimmed off the scan, for the
        # covers: the sheet was scanned with a white sliver of the platen down
        # two edges, which shows as a pale border around the red. Boxes are
        # still written in SCAN coordinates - write() does the shift.
        self.crop = tuple(crop) if crop else None
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
    def _font(self, color=None):
        return f"font-family:Helvetica,Arial,sans-serif;color:{color or self.ink};"

    def _add(self, bbox, html, tight=None, mask=None):
        i = len(self.blocks)
        blk = {"kind": "body", "bbox": list(bbox), "fragments": [list(bbox)],
               "lines": [list(bbox)], "text": ""}
        mc = mask or self.mask_color
        if mc:
            blk["mask_color"] = mc
        # Always opt out of build_page_html's default "one fat rectangle over the
        # whole bbox" mask - park it on a 1px throwaway rect up in the margin.
        # Every call site here states its own masking, and a block that asks for
        # NO mask (whiteout=False) must actually get none: on the red covers that
        # stray white rectangle is a hole in the artwork, not a no-op.
        blk["mask_lines"] = True
        blk["lines"] = [[2, 2, 3, 3]]; blk["fragments"] = [[2, 2, 3, 3]]
        if tight is not None:
            blk["tight_masks"] = [list(r) for r in tight]
        self.blocks.append(blk)
        self.en[str(i)] = {"de": "", "en": html}
        return i

    # ---- white-out a marked box (no text) ----
    def whiteout(self, box):
        self._add(box, "<div></div>", tight=[box])

    # ---- a body paragraph fit into (and white-ing out) its box ----
    def prose(self, box, html, fs=11, lh=1.06, justify=True,
              color=None, mask=None, align=None):
        al = align or ('justify' if justify else 'left')
        # set font-size on the <p> too — the build CSS (.ovr.body p) otherwise
        # forces it to 9pt and overrides the wrapper div.
        # font-size, line-height AND text-align all have to be set on the <p>:
        # the build CSS targets `.ovr.body p` directly, so a value set only on
        # the wrapper div loses to it (justify=False was silently ignored).
        self._add(box, f'<div style="{self._font(color)}font-size:{fs}pt;'
                  f'line-height:{lh};text-align:{al}">'
                  f'<p style="margin:0;font-size:{fs}pt;'
                  f'line-height:{lh};text-align:{al}">{html}</p></div>',
                  tight=[box], mask=mask)

    # ---- a heading / caption / label placed at an exact box ----
    def heading(self, box, html, fs=13, bold=True, center=False,
                nowrap=True, whiteout=True, lh=1.1, color=None, mask=None,
                right=False, italic=False):
        w = 700 if bold else 400
        al = 'right' if right else ('center' if center else 'left')
        ws = 'white-space:nowrap;' if nowrap else ''
        it = 'font-style:italic;' if italic else ''
        self._add(box, f'<div style="{self._font(color)}font-size:{fs}pt;'
                  f'font-weight:{w};{ws}{it}text-align:{al};line-height:{lh}">'
                  f'{html}</div>',
                  tight=[box] if whiteout else None, mask=mask)

    # ---- raw html overlay (e.g. a rebuilt HTML table) at a box ----
    def raw(self, box, html, whiteout=True, extra_white=None, mask=None):
        rects = []
        if whiteout:
            rects.append(box)
        if extra_white:
            rects += [list(r) for r in extra_white]
        self._add(box, html, tight=rects or None, mask=mask)

    # ---- re-draw a thin black line (frame/rule segment the white-out covered) ----
    def line(self, box):
        self._add(box, f'<div style="width:100%;height:100%;background:#111">'
                  f'</div>', tight=[box])

    def write(self):
        # the covers are square; take the real size so the sheet is not stretched
        try:
            from PIL import Image
            size = list(Image.open(f"{self.root}/pages/page-{self.nn:02d}.png").size)
        except Exception:
            size = [2480, 3507]
        extra = {}
        if self.crop:
            l, t, r, bm = self.crop
            size = [size[0] - l - r, size[1] - t - bm]
            extra["bg_crop_px"] = [l, t, r, bm]
            for blk in self.blocks:
                blk["bbox"] = [blk["bbox"][0] - l, blk["bbox"][1] - t,
                               blk["bbox"][2] - l, blk["bbox"][3] - t]
                if "tight_masks" in blk:
                    blk["tight_masks"] = [[m[0] - l, m[1] - t, m[2] - l, m[3] - t]
                                          for m in blk["tight_masks"]]
        # px_per_mm from the sheet's own width: the loose game-board sheets
        # scanned 2464 px wide, and PPM's fixed 2480 would drift ~13 px by the
        # right-hand edge.
        ppm = size[0] / 210.0
        layout = {"page_size_px": size, "dpi": 300, "px_per_mm": ppm, **extra,
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

def fit_fs(box, text, cap=19.0, floor=9.0, dpi=300, adv=0.56):
    """Largest font size (pt) at which `text` fits `box` on one line.

    The English title of a section is usually longer than the German it
    replaces, while the box is marked around the German. heading() defaults to
    nowrap, so an over-long title runs off the page instead of wrapping - which
    is exactly how a title ended up past the right edge. Sizing from the box
    removes the guesswork; `cap` keeps short titles from becoming huge.
    """
    w_pt = (box[2] - box[0]) / dpi * 72.0
    return round(max(floor, min(cap, w_pt / (max(1, len(text)) * adv))), 1)
