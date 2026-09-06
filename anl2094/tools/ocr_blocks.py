#!/usr/bin/env python3
"""OCR the boxes marked by mark_text.py and write the German source.

    tools/ocr_blocks.py 9          -> figures/page-09.de.json

Small crops are the weak point: a 60 px-tall heading read straight from the
300 dpi scan can come back in the 50s, while the same crop upscaled 3x reads in
the 90s. 4x is measurably worse than 3x, so 3x is the default rather than
"as large as possible". Anything still below 80 after that is reported so it can
be checked by eye instead of trusted.
"""
import argparse, csv, io, json, subprocess, sys
from pathlib import Path
from PIL import Image

SCALE, LOW = 3, 80.0
ROOT = Path(__file__).resolve().parent.parent

def ocr(img, psm=6):
    img.save('/tmp/_ocr.png')
    tsv = subprocess.run(['tesseract', '/tmp/_ocr.png', '-', '-l', 'deu',
                          '--psm', str(psm), 'tsv'],
                         capture_output=True, text=True).stdout
    rows = [r for r in csv.DictReader(io.StringIO(tsv), delimiter='\t',
                                      quoting=csv.QUOTE_NONE)
            if r.get('text', '').strip() and r.get('conf', '-1') not in ('-1', '')]
    conf = [float(r['conf']) for r in rows]
    return ' '.join(r['text'] for r in rows), (sum(conf)/len(conf) if conf else 0.0), len(rows)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('page', type=int)
    a = ap.parse_args()
    nn = f"{a.page:02d}"
    boxes = json.load(open(ROOT/'figures'/f'page-{nn}.json'))
    im = Image.open(ROOT/'pages'/f'page-{nn}.png')

    out, weak = {}, []
    for cat in ('heading', 'prose', 'table'):
        for i, b in enumerate(boxes.get(cat, [])):
            c = im.crop(tuple(b))
            c = c.resize((c.width*SCALE, c.height*SCALE), Image.LANCZOS)
            text, conf, n = ocr(c)
            key = f"{cat}{i}"
            out[key] = {"box": b, "conf": round(conf, 1), "words": n, "de": text}
            print(f"  {key:10}{b[2]-b[0]:5d}x{b[3]-b[1]:<5d}{n:5d}w  {conf:5.1f}")
            if conf < LOW:
                weak.append(key)

    dst = ROOT/'figures'/f'page-{nn}.de.json'
    dst.write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n')
    print(f"-> {dst.relative_to(ROOT)}")
    if weak:
        print(f"** check by eye (conf < {LOW:.0f}): {', '.join(weak)}")

if __name__ == '__main__':
    main()
