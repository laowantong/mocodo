
def card_pos(ex, ey, ew, eh, ax, ay, k):
    if ax != ex and abs(float(ay - ey) / (ax - ex)) < float(eh) / ew:
        (x0, x1) = (ex + cmp(ax, ex) * (ew + card_margin), ex + cmp(ax, ex) * (ew + card_margin + card_max_width))
        (y0, y1) = sorted([ey + (x0 - ex) * (ay - ey) / (ax - ex), ey + (x1 - ex) * (ay - ey) / (ax - ex)])
        return (min(x0, x1), (y0 + y1 - card_max_height + k * abs(y1 - y0 + card_max_height)) / 2 + cmp(k, 0) * card_margin)
    else:
        (y0, y1) = (ey + cmp(ay, ey) * (eh + card_margin), ey + cmp(ay, ey) * (eh + card_margin + card_max_height))
        (x0, x1) = sorted([ex + (y0 - ey) * (ax - ex) / (ay - ey), ex + (y1 - ey) * (ax - ex) / (ay - ey)])
        return ((x0 + x1 - card_max_width + k * abs(x1 - x0 + card_max_width)) / 2 + cmp(k, 0) * card_margin, min(y0, y1))


def line_arrow(x0, y0, x1, y1, t):
    (x, y) = (t * x0 + (1 - t) * x1, t * y0 + (1 - t) * y1)
    return arrow(x, y, x1 - x0, y0 - y1)


def curve_arrow(x0, y0, x1, y1, x2, y2, x3, y3, t):
    (cx, cy) = (3 * (x1 - x0), 3 * (y1 - y0))
    (bx, by) = (3 * (x2 - x1) - cx, 3 * (y2 - y1) - cy)
    (ax, ay) = (x3 - x0 - cx - bx, y3 - y0 - cy - by)
    t = 1 - t
    bezier = lambda t: (ax*t*t*t + bx*t*t + cx*t + x0, ay*t*t*t + by*t*t + cy*t + y0)
    (x, y) = bezier(t)
    u = 1.0
    while t < u:
        m = (u + t) / 2.0
        (xc, yc) = bezier(m)
        d = ((x - xc)**2 + (y - yc)**2)**0.5
        if abs(d - arrow_axis) < 0.01:
            break
        if d > arrow_axis:
            u = m
        else:
            t = m
    return arrow(x, y, xc - x, y - yc)
