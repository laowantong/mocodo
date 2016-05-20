def straight_leg(ex, ey, ew, eh, ax, ay, aw, ah):
    
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
    
    def card_pos(cw, ch, k):
        diagonal = hypot(ax-ex, ay-ey)
        correction = card_margin * (1 - abs(abs(ax-ex) - abs(ay-ey)) / diagonal) - k
        (xg, yg) = intersection(ex, ey, ew, eh + ch, ax, ay)
        (xb, yb) = intersection(ex, ey, ew + cw, eh, ax, ay)
        if xg <= xb:
            if xg <= ex:
                if yb <= ey:
                    (x, y) = (xb - correction, yb)
                else:
                    (x, y) = (xb - correction, yb + ch)
            else:
                if yb <= ey:
                    (x, y) = (xg, yg + ch - correction)
                else:
                    (x, y) = (xg, yg + correction)
        else:
            if xb <= ex:
                if yb <= ey:
                    (x, y) = (xg - cw, yg + ch - correction)
                else:
                    (x, y) = (xg - cw, yg + correction)
            else:
                if yb <= ey:
                    (x, y) = (xb - cw + correction, yb)
                else:
                    (x, y) = (xb - cw + correction, yb + ch)
        return (x, y + card_underline_skip_height)
    
    def arrow_pos(direction, t):
        (x0, y0) = intersection(ex, ey, ew, eh, ax, ay)
        (x1, y1) = intersection(ax, ay, aw, ah, ex, ey)
        (x, y) = (t * x0 + (1 - t) * x1, t * y0 + (1 - t) * y1)
        if direction == ">":
            return (x, y, x1 - x0, y0 - y1)
        else:
            return (x + x1 - x0, y + y0 - y1, x0 - x1, y1 - y0)
    
    line(ex, ey, ax, ay)
    return (card_pos, arrow_pos)


def curved_leg(ex, ey, ew, eh, ax, ay, aw, ah, spin):
    
    def function_factory():
        (cx, cy) = (3 * (x1 - x0), 3 * (y1 - y0))
        (bx, by) = (3 * (x2 - x1) - cx, 3 * (y2 - y1) - cy)
        (ax, ay) = (x3 - x0 - cx - bx, y3 - y0 - cy - by)
        bezier = lambda t: (ax*t*t*t + bx*t*t + cx*t + x0, ay*t*t*t + by*t*t + cy*t + y0)
        derivate = lambda t: (3*ax*t*t + 2*bx*t + cx, 3*ay*t*t + 2*by*t + cy)
        return (bezier, derivate)
    
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
    
    def card_pos(cw, ch, k):
        diagonal = hypot(ax-ex, ay-ey)
        correction = card_margin * (1 - abs(abs(ax-ex) - abs(ay-ey)) / diagonal) - k
        (top, bot) = (ey - eh, ey + eh)
        (TOP, BOT) = (top - ch, bot + ch)
        (lef, rig) = (ex - ew, ex + ew)
        (LEF, RIG) = (lef - cw, rig + cw)
        (xr, yr) = intersection(LEF, TOP, RIG, BOT)
        (xg, yg) = intersection(lef, TOP, rig, BOT)
        (xb, yb) = intersection(LEF, top, RIG, bot)
        if spin == 1:
            if (yr == BOT and xr <= rig) or (xr == LEF and yr >= bot):
                (y, x) = (bot, max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) - correction)
            elif (xr == RIG and yr >= top) or yr == BOT:
                (x, y) = (rig, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) - correction - ch)
            elif (yr == TOP and xr >= lef) or xr == RIG:
                (y, x) = (TOP, min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) - correction - cw)
            else:
                (x, y) = (LEF, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) - correction)
        else:
            if (yr == BOT and xr >= lef) or (xr == RIG and yr >= bot):
                (y, x) = (bot, min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) - correction - cw)
            elif xr == RIG or (yr == TOP and xr >= rig):
                (x, y) = (rig, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) - correction)
            elif yr == TOP or (xr == RIG and yr <= top):
                (y, x) = (TOP, max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) - correction)
            else:
                (x, y) = (LEF, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) - correction - ch)
        return (x, y + ch + card_underline_skip_height)
    
    def arrow_pos(direction, t):
        t0 = bisection(lambda x, y: abs(x - ax) > aw or abs(y - ay) > ah)
        t3 = bisection(lambda x, y: abs(x - ex) < ew and abs(y - ey) < eh)
        if direction == "<":
            (t0, t3) = (t3, t0)
        tc = t0 + (t3 - t0) * t
        (xc, yc) = bezier(tc)
        (x, y) = derivate(tc)
        if direction == "<":
            (x, y) = (-x, -y)
        return (xc, yc, x, -y)
    
    diagonal = hypot(ax-ex, ay-ey)
    x0 = ex
    y0 = ey
    x1 = ex + (ax-ex) * curvature_ratio - spin * curvature_gap * (ay-ey) / diagonal
    y1 = ey + (ay-ey) * curvature_ratio + spin * curvature_gap * (ax-ex) / diagonal
    x2 = ax + (ex-ax) * curvature_ratio - spin * curvature_gap * (ay-ey) / diagonal
    y2 = ay + (ey-ay) * curvature_ratio + spin * curvature_gap * (ax-ex) / diagonal
    x3 = ax
    y3 = ay
    (bezier, derivate) = function_factory()
    curve(x0, y0, x1, y1, x2, y2, x3, y3)
    return card_pos, arrow_pos
