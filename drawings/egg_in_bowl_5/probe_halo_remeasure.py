"""The round's gauge on the paper halo round the bowl after the table pass: the share
of paper never touched in rings 0-10, 10-20, ... 70-80 px out from the bowl's
silhouette, read off the canvas replayed to the end of `p01_table.py` (record 76).
Run as a plain script from this folder with PYTHONPATH on the checkout's src."""
import numpy as np
import easel
from easel import Session, polygon, union

s = Session.load("drawing.easel")
scope = {name: getattr(easel, name) for name in dir(easel) if not name.startswith("_")}
scope["s"] = s
exec(open("prelude.py", encoding="utf-8").read(), scope)
ell_pts, RIM, BELLY = scope["ell_pts"], scope["RIM"], scope["BELLY"]

t = s.replay(upto=76, frames=False)
g = np.asarray(t.canvas.graphite)
paper = g <= 0.0
print(f"replayed to record 76: {len(t.history.records)} records, {(g > 0).mean():.1%} of the sheet touched")

def grown(px):
    return union(polygon(ell_pts(RIM[0], RIM[1], RIM[2] + px, RIM[3] + px, 0, 360)),
                 polygon(ell_pts(BELLY[0], BELLY[1], BELLY[2] + px, BELLY[3] + px, 0, 360)))

masks = {px: s._place_mask(grown(px)) for px in range(0, 90, 10)}
for px in range(0, 80, 10):
    ring = masks[px + 10] & ~masks[px]
    print(f"ring {px:2d}-{px + 10:2d} px out: {paper[ring].mean():6.1%} paper never touched")
