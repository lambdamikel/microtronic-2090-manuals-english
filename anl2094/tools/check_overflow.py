#!/usr/bin/env python3
"""Report overlay text that does not fit inside its marked box.

    tools/check_overflow.py --pages 6,7,9 [--html /tmp/batch.html]

The English is often longer than the German it replaces. An overlay that
overruns its box does not get clipped - it spills over whatever sits below,
which is how a callout diagram ended up underneath the tail of a paragraph.
Nothing in the pipeline caught that, because check_graphics looks for masks
eating figures, not for text eating its neighbour.

Measurement is done by the browser that will render the page, not estimated:
each .ovr element is asked for its scrollHeight/scrollWidth against its
client box, so it reflects the real font metrics and justification.
"""
import argparse, json, re, subprocess, sys, tempfile
from pathlib import Path

PROBE = """
<script>
document.addEventListener('DOMContentLoaded', function () {
  var out = [];
  document.querySelectorAll('.ovr').forEach(function (el, i) {
    var sec = el.closest('section.page');
    var pg  = sec ? sec.getAttribute('data-page') : null;
    var dy = el.scrollHeight - el.clientHeight;
    var dx = el.scrollWidth  - el.clientWidth;
    if (dy > 2 || dx > 2) {
      out.push({i: i, page: pg, cls: el.className, dy: dy, dx: dx,
                h: el.clientHeight, w: el.clientWidth,
                text: (el.innerText || '').slice(0, 60)});
    }
  });
  var pre = document.createElement('pre');
  pre.id = 'overflow-report';
  pre.textContent = JSON.stringify(out);
  document.body.appendChild(pre);
});
</script>
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--pages', required=True)
    ap.add_argument('--html')
    a = ap.parse_args()

    html = a.html
    if not html:
        html = tempfile.mktemp(suffix='.html')
        subprocess.run([sys.executable, 'tools/build_page_html.py', '--root', a.root,
                        '--pages', a.pages, '--out', html], check=True,
                       stdout=subprocess.DEVNULL)

    src = Path(html).read_text()
    probed = tempfile.mktemp(suffix='.html')
    Path(probed).write_text(src.replace('</body>', PROBE + '</body>')
                            if '</body>' in src else src + PROBE)

    dom = subprocess.run(['google-chrome', '--headless', '--disable-gpu', '--no-sandbox',
                          '--virtual-time-budget=4000', '--dump-dom', 'file://' + probed],
                         capture_output=True, text=True).stdout
    m = re.search(r'<pre id="overflow-report">(.*?)</pre>', dom, re.S)
    if not m:
        sys.exit('could not read the probe result - did the page load?')
    bad = json.loads(m.group(1).replace('&quot;', '"').replace('&amp;', '&')
                     .replace('&lt;', '<').replace('&gt;', '>'))
    if not bad:
        print('no overflow'); return
    print(f"{len(bad)} overlay block(s) overflow their box:\n")
    for b in bad:
        why = []
        if b['dy'] > 2: why.append(f"{b['dy']}px too tall (box {b['h']}px)")
        if b['dx'] > 2: why.append(f"{b['dx']}px too wide (box {b['w']}px)")
        pg = f"page {b['page']} " if b.get('page') else ""
        print(f"  {pg}block {b['i']:2d} [{b['cls']}]  {', '.join(why)}")
        print(f"      {b['text'].strip()[:58]}...")
    sys.exit(1)

if __name__ == '__main__':
    main()
