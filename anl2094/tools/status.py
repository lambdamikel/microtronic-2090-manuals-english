#!/usr/bin/env python3
"""Show how far each page has got through the pipeline.

    tools/status.py           all pages that have been started
    tools/status.py --todo    just what is waiting on me

marked   -> figures/page-NN.json      (you drew boxes)
ocr      -> figures/page-NN.de.json   (German captured)
built    -> translations/page-NN.en.json
"""
import argparse, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--todo', action='store_true')
    a = ap.parse_args()
    rows = []
    for f in sorted((ROOT/'figures').glob('page-*.json')):
        if f.name.endswith('.de.json'):
            continue
        nn = f.stem.split('-')[1]
        boxes = json.load(open(f))
        n = sum(len(v) for v in boxes.values() if isinstance(v, list))
        ocr = (ROOT/'figures'/f'page-{nn}.de.json').exists()
        built = (ROOT/'translations'/f'page-{nn}.en.json').exists()
        rows.append((nn, n, ocr, built))
    if not rows:
        print('nothing marked yet'); return
    todo = [r for r in rows if not r[3]]
    show = todo if a.todo else rows
    print(f"{'page':6}{'boxes':>6}  {'ocr':^5} {'built':^6}")
    for nn, n, ocr, built in show:
        print(f"  {nn:4}{n:6}  {'yes' if ocr else ' - ':^5} {'yes' if built else ' - ':^6}")
    print(f"\n{len(rows)} marked, {sum(1 for r in rows if r[3])} built, {len(todo)} waiting")

if __name__ == '__main__':
    main()
