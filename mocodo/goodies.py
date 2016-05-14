
from math import hypot

def card_pos(ex, ey, ew, eh, ax, ay, k):
    (qx, qy) = quadrants(1.0, 1.0, ax-ex, ay-ey)
    (qxr, qyr) = quadrants(ew/2, eh/2, ax-ex, ay-ey)
    if qxr == 0:
        aex = (k if ax == ex else cmp(ax, ex))
        return line_box_intersection(
            ex - aex * qyr * qy * card_margin - (aex + 1) * card_max_width / 2,
            ey + aex * qyr * qx * card_margin + (qyr - 1) * card_max_height / 2,
            ew,
            eh/2 + qyr * qy * card_margin,
            ax-ex,
            ay-ey
        )
    else:
        aey = (k if ay == ey else cmp(ay, ey))
        return line_box_intersection(
            ex + aey * qxr * qy * card_margin + (qxr - 1) * card_max_width / 2,
            ey - aey * qxr * qx * card_margin - (aey + 1) * card_max_height / 2,
            ew/2 + qxr * qx * card_margin,
            eh,
            ax-ex,
            ay-ey
        )

def line_box_intersection(x, y, w, h, dx, dy):
    (qx, qy) = quadrants(w, h, dx, dy)
    return (x + qx * w + (qy * dx * h / dy if qy else 0), y + qy * h + (qx * dy * w / dx if qx else 0))

def quadrants(w, h, dx, dy):
    (a, b) = (h * dx, w * dy)
    if a > b:
        if a > -b:
            return (1, 0)
        else:
            return (0, -1)
    else:
        if a > -b:
            return (0, 1)
        else:
            return (-1, 0)

def line_arrow(x0, y0, w0, h0, x1, y1, w1, h1, t):
    ((x0, y0), (x1,y1)) = (line_box_intersection(x0, y0, w0, h0, x1-x0, y1-y0), line_box_intersection(x1, y1, w1, h1, x0-x1, y0-y1))
    (x, y) = (t * x0 + (1 - t) * x1, t * y0 + (1 - t) * y1)
    return arrow(x, y, x1 - x0, y0 - y1)

def curve_arrow(x0, y0, w0, h0, x1, y1, x2, y2, x3, y3, w3, h3, t):
    (cx, cy) = (3 * (x1 - x0), 3 * (y1 - y0))
    (bx, by) = (3 * (x2 - x1) - cx, 3 * (y2 - y1) - cy)
    (ax, ay) = (x3 - x0 - cx - bx, y3 - y0 - cy - by)
    def bezier(t):
        return ax*t*t*t + bx*t*t + cx*t + x0, ay*t*t*t + by*t*t + cy*t + y0
    def visible_end_ratio(a, b, left, right, bottom, top):
        while abs(b - a) > 0.001:
            m = (a + b) / 2
            (x, y) = bezier(m)
            if left < x < right and bottom < y < top:
                a = m
            else:
                b = m
        return m
    t0 = visible_end_ratio(0.0, 1.0, x0 - w0, x0 + w0, y0 - h0, y0 + h0)
    t3 = visible_end_ratio(1.0, 0.0, x3 - w3, x3 + w3, y3 - h3, y3 + h3)
    t = t0 + (t3 - t0) * t
    (x, y) = bezier(t)
    u = 1.0
    while t < u:
        m = (u + t) / 2.0
        (xc, yc) = bezier(m)
        d = hypot(x - xc, y - yc)
        if abs(d - arrow_axis) < 0.001:
            break
        if d > arrow_axis:
            u = m
        else:
            t = m
    return arrow(x, y, xc - x, y - yc)
