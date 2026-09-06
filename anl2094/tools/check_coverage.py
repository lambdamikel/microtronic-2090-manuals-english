#!/usr/bin/env python3
"""Report marked blocks that never got an English overlay.

    tools/check_coverage.py --pages 23-36

check_overflow catches text that does not FIT its box; nothing caught text that
was never written at all. A per-page build script is hand-written from the
German, and a block can simply be skipped - that is how the last paragraph of
page 35 went missing, silently, past both existing checks.

A shortfall is not always a bug: a heading that reads the same in English (page
26 "Pull", page 35 "17 + 4 (Black Jack)") is deliberately left as printed. So
this reports counts and names the German text of the surplus blocks, and you
decide.
"""
import argparse, json
from pathlib import Path


def parse_pages(spec):
    out = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-"); out += list(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--pages", required=True, help="e.g. 23-36 or 26,35")
    args = ap.parse_args()
    root = Path(args.root).resolve()

    bad = 0
    for n in parse_pages(args.pages):
        de_p = root / "figures" / f"page-{n:02d}.de.json"
        en_p = root / "translations" / f"page-{n:02d}.en.json"
        if not de_p.exists() or not en_p.exists():
            continue
        de = json.loads(de_p.read_text())
        en = json.loads(en_p.read_text())
        if len(en) >= len(de):
            print(f"✓ page {n}: {len(de)} marked, {len(en)} overlays")
            continue
        bad += 1
        print(f"✗ page {n}: {len(de)} marked but only {len(en)} overlays "
              f"- {len(de) - len(en)} block(s) unaccounted for:")
        for k, v in de.items():
            print(f"      {k:9} {v['box']}  {v['de'][:70]}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
