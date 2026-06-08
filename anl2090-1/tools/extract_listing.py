#!/usr/bin/env python3
"""
Semi-automatic transcription of a Microtronic program-listing table.

Given a page and a table-region bbox, this:
  1. finds the row grid lines (horizontal rules) and column grid lines
     (vertical rules) inside the region,
  2. OCRs the region once (Tesseract hOCR) and buckets each word into its
     (row, column) cell,
  3. validates the rigid columns — address (hex), entry code (3 hex digits),
     mnemonic (known opcode) — and flags rows that don't parse,
  4. writes a stub JSON of rows with the codes filled in and the German
     "Erklärungen" column captured verbatim for translation.

The codes are language-neutral, so only the Explanation column needs
translating afterwards. Dot-matrix OCR is imperfect — every row carries an
`ok` flag and the raw OCR so flagged rows can be eyeballed quickly.

    python3 extract_listing.py pages/page-37.png 120 170 1198 1010 \
        --cols 3 --out /tmp/p37_listing.json
"""
import argparse, json, re, subprocess, tempfile
from pathlib import Path
from html.parser import HTMLParser

import numpy as np
from PIL import Image

OPCODES = {
    "CLEAR", "MOV", "MOVI", "ADD", "ADDI", "SUB", "SUBI", "SUBC", "ADDC",
    "CMP", "CMPI", "OR", "ORI", "AND", "ANDI", "XOR", "XORI",
    "BRC", "BRZ", "GOTO", "CALL", "RET", "DISP", "KIN", "DIN", "DOT",
    "EXRA", "EXRB", "HALT", "NOP", "SCALL", "SBR", "RSB",
}
BBOX_RE = re.compile(r"bbox (\d+) (\d+) (\d+) (\d+)")
HEX = set("0123456789ABCDEF")


def grid_lines(gray, x0, y0, x1, y1):
    """Return (row_cuts, col_cuts) — y of horizontal rules and x of vertical
    rules bounding the cells, in full-page px."""
    sub = (np.asarray(gray)[y0:y1, x0:x1] < 135)
    h, w = sub.shape
    row_cuts, col_cuts = [], []
    for r in range(h):
        if sub[r].sum() > 0.6 * w:
            row_cuts.append(y0 + r)
    for c in range(w):
        if sub[:, c].sum() > 0.6 * h:
            col_cuts.append(x0 + c)

    def dedup(vals, gap):
        out = []
        for v in sorted(vals):
            if not out or v - out[-1] > gap:
                out.append(v)
        return out

    return dedup(row_cuts, 8), dedup(col_cuts, 8)


class Words(HTMLParser):
    def __init__(self):
        super().__init__()
        self.words = []
        self._cur = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("class") == "ocrx_word":
            m = BBOX_RE.search(a.get("title", ""))
            self._cur = [int(m.group(i)) for i in range(1, 5)] if m else None
            self._buf = []

    def handle_data(self, data):
        if self._cur is not None:
            self._buf.append(data)

    def handle_endtag(self, tag):
        if tag == "span" and self._cur is not None:
            txt = "".join(self._buf).strip()
            if txt:
                cx = (self._cur[0] + self._cur[2]) // 2
                cy = (self._cur[1] + self._cur[3]) // 2
                self.words.append((cx, cy, txt))
            self._cur = None


def ocr_words(image, x0, y0, x1, y1):
    """hOCR the cropped region; return words as (cx, cy, text) in full-page px."""
    with tempfile.TemporaryDirectory() as td:
        crop = image.crop((x0, y0, x1, y1))
        cp = Path(td) / "c.png"; crop.save(cp)
        stem = Path(td) / "c"
        subprocess.run(["tesseract", str(cp), str(stem), "-l", "deu",
                        "--psm", "6", "hocr"], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        p = Words(); p.feed((stem.with_suffix(".hocr")).read_text(encoding="utf-8", errors="replace"))
    return [(cx + x0, cy + y0, t) for (cx, cy, t) in p.words]


def bucket(words, row_cuts, col_cuts):
    """Group words into rows (between consecutive row_cuts) and columns."""
    rows = []
    for a, b in zip(row_cuts, row_cuts[1:]):
        if b - a < 18:                       # skip header double-lines
            continue
        cells = [[] for _ in range(max(1, len(col_cuts) - 1))]
        for cx, cy, t in words:
            if not (a < cy < b):
                continue
            col = 0
            for k in range(len(col_cuts) - 1):
                if col_cuts[k] <= cx < col_cuts[k + 1]:
                    col = k; break
            else:
                col = len(cells) - 1
            cells[col].append((cx, t))
        joined = [" ".join(t for _, t in sorted(c)) for c in cells]
        if any(joined):
            rows.append((a, b, joined))
    return rows


def validate(cells):
    """Heuristic: identify addr / code / mnemonic columns and check format."""
    addr = code = mnem = None
    for v in cells:
        s = v.strip().upper()
        if addr is None and 1 <= len(s) <= 2 and all(ch in HEX for ch in s):
            addr = s; continue
        if code is None and len(s) == 3 and all(ch in HEX for ch in s):
            code = s; continue
        if mnem is None and s.split() and s.split()[0] in OPCODES:
            mnem = v.strip()
    ok = addr is not None and code is not None and mnem is not None
    return ok, addr, code, mnem


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("x0", type=int); ap.add_argument("y0", type=int)
    ap.add_argument("x1", type=int); ap.add_argument("y1", type=int)
    ap.add_argument("--out")
    args = ap.parse_args()

    img = Image.open(args.image)
    gray = img.convert("L")
    row_cuts, col_cuts = grid_lines(gray, args.x0, args.y0, args.x1, args.y1)
    words = ocr_words(img.convert("RGB"), args.x0, args.y0, args.x1, args.y1)
    rows = bucket(words, row_cuts, col_cuts)

    out_rows, n_ok = [], 0
    for a, b, cells in rows:
        ok, addr, code, mnem = validate(cells)
        n_ok += ok
        expl = ""
        # last column that isn't addr/code/mnem is usually the Explanation
        used = {addr, code, mnem}
        for v in cells:
            if v.strip() and v.strip() not in used and v.strip().upper() not in used:
                if v.strip() not in (addr, code, mnem):
                    expl = v.strip()
        out_rows.append({"ok": ok, "addr": addr, "code": code, "mnem": mnem,
                         "erkl_de": expl, "raw": cells})
    result = {
        "region": [args.x0, args.y0, args.x1, args.y1],
        "rows_total": len(out_rows), "rows_ok": n_ok,
        "col_cuts": col_cuts, "row_cuts": len(row_cuts),
        "rows": out_rows,
    }
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(text)
        print(f"{n_ok}/{len(out_rows)} rows parsed OK -> {args.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
