# Run this under NodeBox 1.9 (Mac OS X)

from __future__ import division
from math import hypot, cos, sin, radians

(width,height) = (256, 256)
(ew,eh) = (40, 50)
(cw,ch) = (32, 20)
ANIMATE = True
curvature_ratio = 0.3
curvature_gap = 60

def setup():
    global frame
    frame = -180

def draw():
    global frame
    frame += 1
    if frame == 180:
        frame = -180
    slope = radians(frame)

    # Outer frame
    fill(None)
    strokewidth(1)
    stroke(color(1,0,0))
    rect(ex-ew-cw, ey-eh-ch, 2*ew+2*cw, 2*eh+2*ch)

    # Inner frame
    strokewidth(2)
    stroke(0)
    rect(ex-ew, ey-eh, 2*ew, 2*eh)

    (ax, ay) = ex + cos(slope) * width / 2, ey + sin(slope) * height / 2

    # Copy-paste below the functions from drawing_helpers.py (NodeBox import is buggy)

    def bisection(predicate):
        (a, b) = (0, 1)
        while abs(b - a) > 0.001:
            m = (a + b) / 2
            (x, y) = bezier(m)
            if predicate(x, y):
                a = m
            else:
                b = m
        return m
    
    def intersection(left, top, right, bottom):
        (x, y) = bezier(bisection(lambda x, y: left <= x <= right and top <= y <= bottom))
        return (int(round(x)), int(round(y)))
    
    def card_pos(cw, ch, shift):
        diagonal = hypot(ax-ex, ay-ey)
        correction = card_margin * (1 - abs(abs(ax-ex) - abs(ay-ey)) / diagonal) - shift
        (top, bot) = (ey - eh, ey + eh)
        (TOP, BOT) = (top - ch, bot + ch)
        (lef, rig) = (ex - ew, ex + ew)
        (LEF, RIG) = (lef - cw, rig + cw)
        (xr, yr) = intersection(LEF, TOP, RIG, BOT)
        (xg, yg) = intersection(lef, TOP, rig, BOT)
        (xb, yb) = intersection(LEF, top, RIG, bot)
        if spin == 1:
            if (yr == BOT and xr <= rig) or (xr == LEF and yr >= bot):
                return (max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) - correction, bot + ch)
            if (xr == RIG and yr >= top) or yr == BOT:
                return (rig, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) - correction)
            if (yr == TOP and xr >= lef) or xr == RIG:
                return (min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) - correction - cw, TOP + ch)
            return (LEF, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) - correction + ch)
        if (yr == BOT and xr >= lef) or (xr == RIG and yr >= bot):
            return (min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) - correction - cw, bot + ch)
        if xr == RIG or (yr == TOP and xr >= rig):
            return (rig, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) - correction + ch)
        if yr == TOP or (xr == LEF and yr <= top):
            return (max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) - correction, TOP + ch)
        return (LEF, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) - correction)
    
    for spin in (-1, 1):
        diagonal = hypot(ax-ex, ay-ey)
        x1 = ex + (ax-ex) * curvature_ratio - spin * curvature_gap * (ay-ey) / diagonal
        y1 = ey + (ay-ey) * curvature_ratio + spin * curvature_gap * (ax-ex) / diagonal
        x2 = ax + (ex-ax) * curvature_ratio - spin * curvature_gap * (ay-ey) / diagonal
        y2 = ay + (ey-ay) * curvature_ratio + spin * curvature_gap * (ax-ex) / diagonal
        (kcx, kcy) = (3 * (x1 - ex), 3 * (y1 - ey))
        (kbx, kby) = (3 * (x2 - x1) - kcx, 3 * (y2 - y1) - kcy)
        (kax, kay) = (ax - ex - kcx - kbx, ay - ey - kcy - kby)
        bezier = lambda t: (kax*t*t*t + kbx*t*t + kcx*t + ex, kay*t*t*t + kby*t*t + kcy*t + ey)
        derivate = lambda t: (3*kax*t*t + 2*kbx*t + kcx, 3*kay*t*t + 2*kby*t + kcy)

        (top, bot) = (ey - eh, ey + eh)
        (TOP, BOT) = (top - ch, bot + ch)
        (lef, rig) = (ex - ew, ex + ew)
        (LEF, RIG) = (lef - cw, rig + cw)
        (xr, yr) = intersection(LEF, TOP, RIG, BOT)
        (xg, yg) = intersection(lef, TOP, rig, BOT)
        (xb, yb) = intersection(LEF, top, RIG, bot)
        (x, y) = card_pos(cw, ch, 0)
    
        # Leg
        strokewidth(2)
        stroke(0)
        curve(ex, ey, x1, y1, x2, y2, ax, ay)

        # Cardinality bounding box
        stroke(0)
        strokewidth(1)
        fill(color(1,1,0,0.5))
        rect(x, y-ch, cw, ch)

        # Intersection points
        strokewidth(2)
        stroke(color(1,0,0)) # red
        oval(xr-3,yr-3, 6, 6)
        stroke(color(0,1,0)) # green
        oval(xg-1, yg-1, 2, 2)
        stroke(color(0,0,1)) # blue
        oval(xb-1, yb-1, 2, 2)


def curve(x0, y0, x1, y1, x2, y2, x3, y3):
    autoclosepath(False)
    nofill()
    beginpath(x0, y0)
    curveto(x1, y1, x2, y2, x3, y3)
    endpath()

size(width,height)
(ex,ey) = (width/2, height/2)
card_margin = 0


if ANIMATE:
    speed(50)
    frame = -180
else:
    var("frame", NUMBER, -180, -180, 180)

draw()
