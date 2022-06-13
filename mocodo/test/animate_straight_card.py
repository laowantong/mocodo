# Run this under NodeBox 1.9 (Mac OS X)

from __future__ import division

from math import hypot, cos, sin, radians

(width, height) = (256, 256)
(ew, eh) = (40, 50)
(cw, ch) = (32, 20)
ANIMATE = False

def setup():
    global frame
    frame = -180

def draw():
    global frame
    frame += 1
    if frame == 180:
        frame = -180
    slope = radians(frame)

    # Copy-paste below the functions from drawing_helpers.py (NodeBox import is buggy)

    def intersection(ex, ey, w, h, ax, ay):
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
    
    def card_pos(cw, ch, shift):
        diagonal = hypot(ax-ex, ay-ey)
        correction = card_margin * (1 - abs(abs(ax-ex) - abs(ay-ey)) / diagonal) - shift
        (xg, yg) = intersection(ex, ey, ew, eh + ch, ax, ay)
        (xb, yb) = intersection(ex, ey, ew + cw, eh, ax, ay)
        if xg <= xb:
            if xg <= ex:
                if yb <= ey:
                    return (xb - correction, yb)
                return (xb - correction, yb + ch)
            if yb <= ey:
                return (xg, yg + ch - correction)
            return (xg, yg + correction)
        if xb <= ex:
            if yb <= ey:
                return (xg - cw, yg + ch - correction)
            return (xg - cw, yg + correction)
        if yb <= ey:
            return (xb - cw + correction, yb)
        return (xb - cw + correction, yb + ch)

    (ax, ay) = ex + cos(slope) * width, ey + sin(slope) * height
    (xr, yr) = (ex, ey)
    (xg, yg) = intersection(ex, ey, ew, eh+ch, ax, ay)
    (xb, yb) = intersection(ex, ey, ew+cw, eh, ax, ay)
    (x, y) = card_pos(cw, ch, 0)
    
    # Outer frame
    fill(None)
    strokewidth(1)
    stroke(color(1, 0, 0))
    rect(ex-ew-cw, ey-eh-ch, 2*ew+2*cw, 2*eh+2*ch)

    # Inner frame
    strokewidth(2)
    stroke(0)
    rect(ex-ew, ey-eh, 2*ew, 2*eh)
    
    # Leg
    strokewidth(2)
    stroke(0)
    line(ex, ey, ax, ay)

    # Cardinality bounding box
    stroke(0)
    strokewidth(1)
    fill(color(1, 1, 0, 0.5))
    rect(x, y-ch, cw, ch)

    # Intersection points
    strokewidth(2)
    stroke(color(1, 0, 0)) # red
    oval(ex-1, ey-1, 2, 2)
    stroke(color(0, 1, 0)) # green
    oval(xg-1, yg-1, 2, 2)
    stroke(color(0, 0, 1)) # blue
    oval(xb-1, yb-1, 2, 2)


size(width, height)
(ex, ey) = (width/2, height/2)
card_margin = 0

if ANIMATE:
    speed(50)
    frame = -180
else:
    var("frame", NUMBER, -180, -180, 180)

draw()
