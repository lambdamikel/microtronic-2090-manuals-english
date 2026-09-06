#!/usr/bin/env python3
"""Mark TRANSLATABLE-TEXT rectangles on a manual page (two-pass workflow).

Pick a category (key), then LEFT-drag a box. Boxes are colour-coded and saved
live to  anl2090-2/figures/page-NN.json :
    {"prose":[...], "heading":[...], "table":[...], "targets":[...]}
(coords are page pixels, 2480x3507.)

Categories
    p  prose    (green)   a paragraph / column of body text
                          -> assistant white-outs it and fits the translation in.
    h  heading  (blue)    a heading / caption / label
                          -> white-out now; the translated text is placed in PASS 2.
    t  table    (orange)  a table region to REBUILD in English.
    g  target   (red)     PASS 2: the EXACT box where the i-th heading/table text
                          goes (mark targets in the SAME order as the headings).

Everything you do NOT mark is preserved untouched (figures, grids, numbers,
opcodes, glyphs, key buttons, page numbers).

Controls
    LEFT-drag   add a box in the current category (saved + printed immediately)
    p h t g     switch current category
    u           undo last box in the current category
    C           clear the current category (Shift+c)
    i / o       zoom in / out          1 2 3 4  jump to a zoom level
    wheel       scroll (Shift+wheel = horizontal)

Usage:  python3 anl2090-2/tools/mark_text.py NN [scan|/path.png]
"""
import sys, os, json, tkinter as tk
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if len(sys.argv) < 2:
    sys.exit("usage: mark_text.py NN [scan|/path.png]")
NN  = int(sys.argv[1])
arg = sys.argv[2] if len(sys.argv) > 2 else "scan"
PNG = (f"{ROOT}/pages/page-{NN:02d}.png" if arg in ("scan", "") else arg)
OUT = f"{ROOT}/figures/page-{NN:02d}.json"
os.makedirs(f"{ROOT}/figures", exist_ok=True)

CATS = [("prose", "p", "#22aa22"), ("heading", "h", "#2266dd"),
        ("table", "t", "#dd8800"), ("targets", "g", "#ee2222")]
KEY2CAT = {k: c for c, k, _ in CATS}
COLOR = {c: col for c, _, col in CATS}

im = Image.open(PNG).convert("RGB")
OW, OH = im.size
PPM = "/tmp/_marktext.ppm"; im.save(PPM)

data = {c: [] for c, _, _ in CATS}
if os.path.exists(OUT):
    try:
        j = json.load(open(OUT))
        for c, _, _ in CATS:
            data[c] = list(j.get(c, []))
    except Exception:
        pass
cat = ["prose"]

def save():
    out = {"page": NN}; out.update(data)
    json.dump(out, open(OUT, "w"), indent=2)

root = tk.Tk()
base = tk.PhotoImage(file=PPM)
LEVELS = [("1/4", 0.25), ("1/3", 1/3.0), ("1/2", 0.5), ("1:1", 1.0)]
cur = [2]
def photo_at(scale):
    if scale >= 1.0: return base
    n = int(round(1.0/scale)); return base.subsample(n, n)
photo = [photo_at(LEVELS[cur[0]][1])]

info = tk.Label(root, anchor="w", font=("TkDefaultFont", 11)); info.pack(fill="x")
fr = tk.Frame(root); fr.pack(fill="both", expand=True)
cv = tk.Canvas(fr, bg="#888", cursor="crosshair")
hb = tk.Scrollbar(fr, orient="horizontal", command=cv.xview)
vb = tk.Scrollbar(fr, orient="vertical",   command=cv.yview)
cv.configure(xscrollcommand=hb.set, yscrollcommand=vb.set)
vb.pack(side="right", fill="y"); hb.pack(side="bottom", fill="x")
cv.pack(side="left", fill="both", expand=True)
img_id = cv.create_image(0, 0, anchor="nw", image=photo[0])

def sc(): return LEVELS[cur[0]][1]
def redraw_boxes():
    cv.delete("box")
    s = sc()
    for c, _, _ in CATS:
        for i, (x0, y0, x1, y1) in enumerate(data[c]):
            cv.create_rectangle(x0*s, y0*s, x1*s, y1*s, outline=COLOR[c],
                                width=2, tags="box")
            cv.create_text(x0*s+3, y0*s+2, anchor="nw", text=f"{c[0]}{i+1}",
                           fill=COLOR[c], tags="box")
def refresh():
    photo[0] = photo_at(sc())
    cv.itemconfigure(img_id, image=photo[0])
    cv.configure(scrollregion=(0, 0, int(OW*sc()), int(OH*sc())))
    counts = "  ".join(f"{c}:{len(data[c])}" for c, _, _ in CATS)
    info.config(text=f"CATEGORY=[{cat[0].upper()}]   {counts}   |   "
                     f"zoom {LEVELS[cur[0]][0]}   p/h/t/g=cat  u=undo  C=clear  i/o=zoom",
                fg=COLOR[cat[0]])
    redraw_boxes()
refresh()
cv.configure(width=min(1300, int(OW*sc())), height=min(930, int(OH*sc())))

def zoom(d): cur[0] = max(0, min(len(LEVELS)-1, cur[0]+d)); refresh()
root.bind("i", lambda e: zoom(1)); root.bind("o", lambda e: zoom(-1))
for k, idx in (("1",3),("2",2),("3",1),("4",0)):
    root.bind(k, lambda e, i=idx: (cur.__setitem__(0, i), refresh()))
def setcat(c): cat[0] = c; refresh(); print(f"# category -> {c}", flush=True)
for k, c in KEY2CAT.items():
    root.bind(k, lambda e, c=c: setcat(c))
def undo(e):
    if data[cat[0]]:
        data[cat[0]].pop(); save(); refresh()
        print(f"# undo {cat[0]} -> {len(data[cat[0]])}", flush=True)
def clear(e):
    data[cat[0]].clear(); save(); refresh(); print(f"# cleared {cat[0]}", flush=True)
root.bind("u", undo); root.bind("C", clear)

st = {"x": 0, "y": 0, "r": None}
def press(e):
    st["x"], st["y"] = cv.canvasx(e.x), cv.canvasy(e.y)
    st["r"] = cv.create_rectangle(st["x"], st["y"], st["x"], st["y"],
                                  outline=COLOR[cat[0]], width=2)
def drag(e):
    if st["r"]: cv.coords(st["r"], st["x"], st["y"], cv.canvasx(e.x), cv.canvasy(e.y))
def release(e):
    s = sc()
    x0, x1 = sorted([st["x"]/s, cv.canvasx(e.x)/s])
    y0, y1 = sorted([st["y"]/s, cv.canvasy(e.y)/s])
    if st["r"]: cv.delete(st["r"]); st["r"] = None
    if (x1-x0) < 3 or (y1-y0) < 3: return
    box = [int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))]
    data[cat[0]].append(box); save(); refresh()
    print(f"{cat[0]} {len(data[cat[0]])}: {box}", flush=True)
cv.bind("<ButtonPress-1>", press); cv.bind("<B1-Motion>", drag)
cv.bind("<ButtonRelease-1>", release)
cv.bind("<MouseWheel>", lambda e: cv.yview_scroll(-1 if e.delta>0 else 1, "units"))
cv.bind("<Button-4>", lambda e: cv.yview_scroll(-1, "units"))
cv.bind("<Button-5>", lambda e: cv.yview_scroll(1, "units"))
cv.bind("<Shift-Button-4>", lambda e: cv.xview_scroll(-1, "units"))
cv.bind("<Shift-Button-5>", lambda e: cv.xview_scroll(1, "units"))
root.title(f"page-{NN:02d}  —  mark translatable text  ->  {OUT}")
print(f"# marking page-{NN:02d} ({OW}x{OH}); current category=prose. "
      f"p/h/t/g to switch. LEFT-drag to add.", flush=True)
root.mainloop()
print(f"# done -> {OUT}", flush=True)
