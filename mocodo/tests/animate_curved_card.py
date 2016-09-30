# Run this under NodeBox 1.9 (Mac OS X)

from __future__ import division
from math import hypot, cos, sin, radians

(width, height) = (256, 256)
(ew, eh) = (40, 50)
(cw, ch) = (32, 20)
ANIMATE = True

def line_intersection(ex, ey, w, h, ax, ay):
    if ax == ex:
        return (ax, ey + cmp(ay, ey) * h)
    if ay == ey:
        return (ex + cmp(ax, ex) * w, ay)
    x = ex + cmp(ax, ex) * w
    y = ey + (ay-ey) * (x-ex) / (ax-ex)
    if abs(y-ey) > h:
        y = ey + cmp(ay, ey) * h
        x = ex + (ax-ex) * (y-ey) / (ay-ey)
    return (x, y)

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
    stroke(color(1, 0, 0))
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
            if predicate(bezier(m)):
                a = m
            else:
                b = m
        return m
    
    def intersection(left, top, right, bottom):
       (x, y) = bezier(bisection(lambda p: left <= p[0] <= right and top <= p[1] <= bottom))
       return (int(round(x)), int(round(y)))
    
    def card_pos(shift):
        diagonal = hypot(ax-ex, ay-ey)
        correction = card_margin * 1.4142 * (1 - abs(abs(ax-ex) - abs(ay-ey)) / diagonal)
        (top, bot) = (ey - eh, ey + eh)
        (TOP, BOT) = (top - ch, bot + ch)
        (lef, rig) = (ex - ew, ex + ew)
        (LEF, RIG) = (lef - cw, rig + cw)
        (xr, yr) = intersection(LEF, TOP, RIG, BOT)
        (xg, yg) = intersection(lef, TOP, rig, BOT)
        (xb, yb) = intersection(LEF, top, RIG, bot)
        if spin > 0:
            if (yr == BOT and xr <= rig) or (xr == LEF and yr >= bot):
                return (max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) - correction + shift, bot + ch)
            if (xr == RIG and yr >= top) or yr == BOT:
                return (rig, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) + correction + shift)
            if (yr == TOP and xr >= lef) or xr == RIG:
                return (min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) + correction + shift - cw, TOP + ch)
            return (LEF, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) - correction + shift + ch)
        if (yr == BOT and xr >= lef) or (xr == RIG and yr >= bot):
            return (min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) + correction + shift - cw, bot + ch)
        if xr == RIG or (yr == TOP and xr >= rig):
            return (rig, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) - correction + shift + ch)
        if yr == TOP or (xr == LEF and yr <= top):
            return (max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) - correction + shift, TOP + ch)
        return (LEF, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) + correction + shift)
    
    
    for spin in (-1, 1):
        diagonal = hypot(ax - ex, ay - ey)
        (x, y) = line_intersection(ex, ey, ew + cw / 2, eh + ch / 2, ax, ay)
        k = ((cw + card_margin) *  abs((ay - ey) / diagonal) + (ch + card_margin) * abs((ax - ex) / diagonal))
        (x, y) = (x - spin * k * (ay - ey) / diagonal, y + spin * k * (ax - ex) / diagonal)
        (hx, hy) = (2 * x - (ex + ax) / 2, 2 * y - (ey + ay) / 2)
        (x1, y1) = (ex + (hx - ex) * 2 / 3, ey + (hy - ey) * 2 / 3)
        (x2, y2) = (ax + (hx - ax) * 2 / 3, ay + (hy - ay) * 2 / 3)
        (kax, kay) = (ex - 2 * hx + ax, ey - 2 * hy + ay)
        (kbx, kby) = (2 * hx - 2 * ex, 2 * hy - 2 * ey)
        bezier = lambda t: (kax*t*t + kbx*t + ex, kay*t*t + kby*t + ey)
        derivate = lambda t: (2*kax*t + kbx, 2*kay*t + kby)

        (top, bot) = (ey - eh, ey + eh)
        (TOP, BOT) = (top - ch, bot + ch)
        (lef, rig) = (ex - ew, ex + ew)
        (LEF, RIG) = (lef - cw, rig + cw)
        (xr, yr) = intersection(LEF, TOP, RIG, BOT)
        (xg, yg) = intersection(lef, TOP, rig, BOT)
        (xb, yb) = intersection(LEF, top, RIG, bot)
        (x, y) = card_pos(0)
    
        # Leg
        strokewidth(2)
        stroke(0)
        curve(ex, ey, x1, y1, x2, y2, ax, ay)

        # Cardinality bounding box
        stroke(0)
        strokewidth(1)
        fill(color(1, 1, 0, 0.5))
        rect(x, y-ch, cw, ch)

        # Intersection points
        strokewidth(2)
        stroke(color(1, 0, 0)) # red
        oval(xr-3, yr-3, 6, 6)
        stroke(color(0, 1, 0)) # green
        oval(xg-1, yg-1, 2, 2)
        stroke(color(0, 0, 1)) # blue
        oval(xb-1, yb-1, 2, 2)


def curve(x0, y0, x1, y1, x2, y2, x3, y3):
    autoclosepath(False)
    nofill()
    beginpath(x0, y0)
    curveto(x1, y1, x2, y2, x3, y3)
    endpath()

size(width, height)
(ex, ey) = (width/2, height/2)
card_margin = 0


if ANIMATE:
    speed(50)
    frame = -180
else:
    var("frame", NUMBER, -180, -180, 180)

draw()
