def offset(x, y):
    return (x + card_margin, y - card_baseline - card_margin)

def straight_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah):
    
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
    
    def card_pos(cw, ch, twist, shift):
        compare = (lambda x1, y1: x1 < y1) if twist else (lambda x1, y1: x1 <= y1)
        diagonal = hypot(ax-ex, ay-ey)
        correction = card_margin * (1 - abs(abs(ax-ex) - abs(ay-ey)) / diagonal) - shift
        (xg, yg) = intersection(ex, ey, ew, eh + ch, ax, ay)
        (xb, yb) = intersection(ex, ey, ew + cw, eh, ax, ay)
        if compare(xg, xb):
            if compare(xg, ex):
                if compare(yb, ey):
                    return (xb - correction, yb)
                return (xb - correction, yb + ch)
            if compare(yb, ey):
                return (xg, yg + ch - correction)
            return (xg, yg + correction)
        if compare(xb, ex):
            if compare(yb, ey):
                return (xg - cw, yg + ch - correction)
            return (xg - cw, yg + correction)
        if compare(yb, ey):
            return (xb - cw + correction, yb)
        return (xb - cw + correction, yb + ch)
    
    def arrow_pos(direction, ratio):
        (x0, y0) = intersection(ex, ey, ew, eh, ax, ay)
        (x1, y1) = intersection(ax, ay, aw, ah, ex, ey)
        if direction == "<":
            (x0, y0, x1, y1) = (x1, y1, x0, y0)
        (x, y) = (ratio * x0 + (1 - ratio) * x1, ratio * y0 + (1 - ratio) * y1)
        return (x, y, x1 - x0, y0 - y1)
    
    straight_leg_factory.card_pos = card_pos
    straight_leg_factory.arrow_pos = arrow_pos
    return straight_leg_factory


def curved_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, spin):
    
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
    
    def arrow_pos(direction, ratio):
        t0 = bisection(lambda x, y: abs(x - ax) > aw or abs(y - ay) > ah)
        t3 = bisection(lambda x, y: abs(x - ex) < ew and abs(y - ey) < eh)
        if direction == "<":
            (t0, t3) = (t3, t0)
        tc = t0 + (t3 - t0) * ratio
        (xc, yc) = bezier(tc)
        (x, y) = derivate(tc)
        if direction == "<":
            (x, y) = (-x, -y)
        return (xc, yc, x, -y)
    
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
    
    curved_leg_factory.points = (ex, ey, x1, y1, x2, y2, ax, ay)
    curved_leg_factory.card_pos = card_pos
    curved_leg_factory.arrow_pos = arrow_pos
    return curved_leg_factory
