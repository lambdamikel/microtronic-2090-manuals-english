#!/usr/bin/env python3
"""Give every body paragraph on a page the same font size.

    tools/unify_prose_fs.py --pages 15,17,26 [--apply]

Per-block sizing was chosen box by box, which is why a page can end up with
paragraphs at 10.2, 10.4 and 10.6 pt sitting side by side. On the page that
reads as an inconsistency, not as fitting. This tool picks, per page, the
LARGEST single size at which every body paragraph still fits its box.

It starts from the largest size the page currently uses and steps down until
the browser probe reports the page clean, so the answer is measured, not
estimated. Shrinking is always safe: a block that fits at size S also fits at
any size below it, so the search can only be stopped by a block that wants to
be smaller than the current candidate.

Left alone deliberately:
  * headings, captions and chart labels - they are sized to their own shapes
  * prose calls passing justify=False - the diagram callouts, worked-example
    labels and programmer credits, whose leading is tuned to line up with
    artwork next to them
  * prose calls with no explicit fs= (they take the module default)
"""
import argparse, json, re, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FLOOR = 8.5
STEP = 0.1


def prose_calls(src):
    """(start, end, text) of every b.prose(...) call, paren-balanced."""
    out = []
    for m in re.finditer(r'\bb\.prose\(', src):
        i, depth = m.end(), 1
        while depth:
            if src[i] == '(':
                depth += 1
            elif src[i] == ')':
                depth -= 1
            i += 1
        out.append((m.start(), i, src[m.start():i]))
    return out


def targets(src):
    """Calls this tool is allowed to resize, plus their current fs."""
    hits = []
    for s, e, txt in prose_calls(src):
        if 'justify=False' in txt:
            continue
        m = re.search(r'\bfs=([0-9.]+)', txt)
        if m:
            hits.append((s, e, float(m.group(1))))
    return hits


def set_fs(path, value):
    src = path.read_text()
    for s, e, _ in reversed(targets(src)):
        call = src[s:e]
        src = src[:s] + re.sub(r'\bfs=[0-9.]+', f'fs={value:g}', call, count=1) + src[e:]
    path.write_text(src)


def script_for(page):
    for name in (f'p{page:02d}.py', f'p{page}.py', f'page{page}.py'):
        p = ROOT / 'tools' / name
        if p.exists():
            return p
    return None


def overflowing_pages(pages):
    """Page numbers whose body overlays overflow, measured in the browser."""
    out = tempfile.mktemp(suffix='.html')
    subprocess.run([sys.executable, str(ROOT / 'tools' / 'build_page_html.py'),
                    '--root', str(ROOT), '--pages', ','.join(map(str, pages)),
                    '--out', out], check=True, stdout=subprocess.DEVNULL, cwd=ROOT)
    r = subprocess.run([sys.executable, str(ROOT / 'tools' / 'check_overflow.py'),
                        '--root', str(ROOT), '--pages', ','.join(map(str, pages)),
                        '--html', out], capture_output=True, text=True, cwd=ROOT)
    bad = set()
    for line in r.stdout.splitlines():
        m = re.search(r'page (\d+) block .*\[ovr body\]', line)
        if m:
            bad.add(int(m.group(1)))
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pages', required=True)
    ap.add_argument('--apply', action='store_true',
                    help='keep the result; without it the scripts are restored')
    args = ap.parse_args()

    pages = []
    for part in args.pages.split(','):
        if '-' in part:
            a, b = part.split('-'); pages += list(range(int(a), int(b) + 1))
        else:
            pages.append(int(part))

    scripts, backup, cand = {}, {}, {}
    for n in pages:
        p = script_for(n)
        if not p:
            continue
        t = targets(p.read_text())
        if len(t) < 2 or len({round(x[2], 2) for x in t}) < 2:
            continue                      # already uniform, or nothing to do
        scripts[n] = p
        backup[n] = p.read_text()
        cand[n] = max(x[2] for x in t)

    if not scripts:
        print('nothing to unify'); return 0

    print(f'unifying {len(scripts)} page(s): '
          + ', '.join(f'{n}@{cand[n]:g}' for n in sorted(scripts)))

    live = sorted(scripts)
    for _ in range(40):
        for n in live:
            set_fs(scripts[n], cand[n])
            subprocess.run([sys.executable, str(scripts[n])], check=True,
                           stdout=subprocess.DEVNULL, cwd=ROOT)
        bad = overflowing_pages(live) & set(live)
        if not bad:
            break
        for n in bad:
            cand[n] = round(cand[n] - STEP, 2)
        stuck = [n for n in bad if cand[n] < FLOOR]
        if stuck:
            print(f'! hit the {FLOOR} pt floor on {stuck}', file=sys.stderr)
            return 1
        print('  retry: ' + ', '.join(f'{n}@{cand[n]:g}' for n in sorted(bad)))
    else:
        print('! did not converge', file=sys.stderr); return 1

    for n in sorted(scripts):
        was = sorted({x[2] for x in targets(backup[n])})
        print(f'  page {n}: {[f"{v:g}" for v in was]} -> {cand[n]:g} pt')

    if not args.apply:
        for n, p in scripts.items():
            p.write_text(backup[n])
            subprocess.run([sys.executable, str(p)], check=True,
                           stdout=subprocess.DEVNULL, cwd=ROOT)
        print('(dry run - scripts restored; pass --apply to keep)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
