#!/usr/bin/env python3
"""Mark the graphic/figure boxes to PRESERVE on a manual page.

The boxes are saved (in page-pixel coordinates, 2480x3507) to
    anl2090-2/figures/page-NN.json   ->  {"preserve": [[x0,y0,x1,y1], ...]}
which the page build reads to mask the text column MINUS these rectangles.

Usage:
    python3 anl2090-2/tools/mark_figures.py NN          # mark figures on sheet NN
    python3 anl2090-2/tools/mark_figures.py NN scan     # (default) draw on the German scan
    python3 anl2090-2/tools/mark_figures.py NN /path.png

Controls (tkinter — no matplotlib/numpy needed, no toolbar to fight):
    * LEFT-drag            draw a box around a figure  -> saved + printed immediately
    * u                    undo last box
    * c                    clear all boxes
    * i / o                zoom in / out      1 2 3 4   jump to a zoom level
    * mouse wheel          scroll vertically  (Shift+wheel = horizontal)
    * boxes already in the json are shown on load; close the window when done.
"""
import sys, os, json, tkinter as tk
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # .../anl2090-2
if len(sys.argv) < 2:
    sys.exit("usage: mark_figures.py NN [scan|/path.png]")
NN  = int(sys.argv[1])
arg = sys.argv[2] if len(sys.argv) > 2 else "scan"
PNG = (f"{ROOT}/pages/page-{NN:02d}.png" if arg in ("scan", "") else arg)
OUT = f"{ROOT}/figures/page-{NN:02d}.json"
os.makedirs(f"{ROOT}/figures", exist_ok=True)

im = Image.open(PNG).convert("RGB")
OW, OH = im.size
PPM = "/tmp/_markfig.ppm"; im.save(PPM)

boxes = []
if os.path.exists(OUT):
    try: boxes = json.load(open(OUT)).get("preserve", [])
    except Exception: boxes = []

def save():
    json.dump({"page": NN, "preserve": boxes}, open(OUT, "w"), indent=2)

root = tk.Tk()
root.title(f"page-{NN:02d}  —  LEFT-drag = figure box (saved to figures/page-{NN:02d}.json)  |  i/o zoom, u undo, c clear")
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
    for i, (x0, y0, x1, y1) in enumerate(boxes):
        cv.create_rectangle(x0*s, y0*s, x1*s, y1*s, outline="red", width=2, tags="box")
        cv.create_text(x0*s+3, y0*s+2, anchor="nw", text=str(i+1), fill="red", tags="box")
def refresh():
    photo[0] = photo_at(sc())
    cv.itemconfigure(img_id, image=photo[0])
    cv.configure(scrollregion=(0, 0, int(OW*sc()), int(OH*sc())))
    info.config(text=f"zoom {LEVELS[cur[0]][0]}   |   {len(boxes)} box(es)   |   i/o zoom, u undo, c clear, LEFT-drag = new box")
    redraw_boxes()
refresh()
cv.configure(width=min(1300, int(OW*sc())), height=min(930, int(OH*sc())))

def zoom(d): cur[0] = max(0, min(len(LEVELS)-1, cur[0]+d)); refresh()
root.bind("i", lambda e: zoom(1)); root.bind("o", lambda e: zoom(-1))
for k, idx in (("1",3),("2",2),("3",1),("4",0)):
    root.bind(k, lambda e, i=idx: (cur.__setitem__(0, i), refresh()))
def undo(e):
    if boxes: boxes.pop(); save(); refresh(); print(f"# undo -> {len(boxes)} boxes", flush=True)
def clear(e):
    boxes.clear(); save(); refresh(); print("# cleared", flush=True)
root.bind("u", undo); root.bind("c", clear)

st = {"x": 0, "y": 0, "r": None}
def press(e):
    st["x"], st["y"] = cv.canvasx(e.x), cv.canvasy(e.y)
    st["r"] = cv.create_rectangle(st["x"], st["y"], st["x"], st["y"], outline="lime", width=2)
def drag(e):
    if st["r"]: cv.coords(st["r"], st["x"], st["y"], cv.canvasx(e.x), cv.canvasy(e.y))
def release(e):
    s = sc()
    x0, x1 = sorted([st["x"]/s, cv.canvasx(e.x)/s]); y0, y1 = sorted([st["y"]/s, cv.canvasy(e.y)/s])
    if cv.coords(st["r"]): cv.delete(st["r"]); st["r"] = None
    if (x1-x0) < 3 or (y1-y0) < 3: return
    box = [int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))]
    boxes.append(box); save(); refresh()
    print(f"figure {len(boxes)}: {box}   (-> {OUT})", flush=True)
cv.bind("<ButtonPress-1>", press); cv.bind("<B1-Motion>", drag); cv.bind("<ButtonRelease-1>", release)
cv.bind("<MouseWheel>", lambda e: cv.yview_scroll(-1 if e.delta>0 else 1, "units"))
cv.bind("<Button-4>", lambda e: cv.yview_scroll(-1, "units")); cv.bind("<Button-5>", lambda e: cv.yview_scroll(1, "units"))
cv.bind("<Shift-Button-4>", lambda e: cv.xview_scroll(-1, "units")); cv.bind("<Shift-Button-5>", lambda e: cv.xview_scroll(1, "units"))

print(f"# marking page-{NN:02d} ({OW}x{OH}); {len(boxes)} existing box(es). LEFT-drag to add; close when done.", flush=True)
root.mainloop()
print(f"# done: {len(boxes)} box(es) saved to {OUT}", flush=True)
