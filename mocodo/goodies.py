class StraightLeg:
    
    def __init__(self, ex, ey, ew, eh, ax, ay, aw, ah):
        (self.ex, self.ey) = (ex, ey)
        (self.ew, self.eh) = (ew, eh)
        (self.ax, self.ay) = (ax, ay)
        (self.aw, self.ah) = (aw, ah)
        line(ex, ey, ax, ay)
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
        self.intersection = intersection
    
    def card_pos(self, cw, ch, k):
        (xg, yg) = self.intersection(self.ex, self.ey, self.ew,      self.eh + ch, self.ax, self.ay)
        (xb, yb) = self.intersection(self.ex, self.ey, self.ew + cw, self.eh,      self.ax, self.ay)
        if xg <= xb:
            if xg <= self.ex:
                if yb <= self.ey:
                    return (xb, yb)
                else:
                    return (xb, yb + ch)
            else:
                if yb <= self.ey:
                    return (xg, yg + ch)
                else:
                    return (xg, yg)
        else:
            if xb <= self.ex:
                if yb <= self.ey:
                    return (xg - cw, yg + ch)
                else:
                    return (xg - cw, yg)
            else:
                if yb <= self.ey:
                    return (xb - cw, yb)
                else:
                    return (xb - cw, yb + ch)
    
    def arrow(self, direction, t):
        (x0, y0) = self.intersection(self.ex, self.ey, self.ew, self.eh, self.ax, self.ay)
        (x1, y1) = self.intersection(self.ax, self.ay, self.aw, self.ah, self.ex, self.ey)
        (x, y) = (t * x0 + (1 - t) * x1, t * y0 + (1 - t) * y1)
        if direction == ">":
            return arrow(x, y, x1 - x0, y0 - y1)
        else:
            return arrow(x + x1 - x0, y + y0 - y1, x0 - x1, y1 - y0)


class CurvedLeg:
    
    def __init__(self, ex, ey, ew, eh, ax, ay, aw, ah, spin):
        (self.ex, self.ey) = (ex, ey)
        (self.ew, self.eh) = (ew, eh)
        (self.ax, self.ay) = (ax, ay)
        (self.aw, self.ah) = (aw, ah)
        self.spin = spin
        diagonal = hypot(ax-ex, ay-ey)
        x0 = ex
        y0 = ey
        x1 = ex + (ax-ex) * curvature_ratio - spin * curvature_length * (ay-ey) / diagonal
        y1 = ey + (ay-ey) * curvature_ratio + spin * curvature_length * (ax-ex) / diagonal
        x2 = ax + (ex-ax) * curvature_ratio - spin * curvature_length * (ay-ey) / diagonal
        y2 = ay + (ey-ay) * curvature_ratio + spin * curvature_length * (ax-ex) / diagonal
        x3 = ax
        y3 = ay
        curve(x0, y0, x1, y1, x2, y2, x3, y3)
        (cx, cy) = (3 * (x1 - x0), 3 * (y1 - y0))
        (bx, by) = (3 * (x2 - x1) - cx, 3 * (y2 - y1) - cy)
        (ax, ay) = (x3 - x0 - cx - bx, y3 - y0 - cy - by)
        def bezier(t):
            return ax*t*t*t + bx*t*t + cx*t + x0, ay*t*t*t + by*t*t + cy*t + y0
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
        self.bisection = bisection
        self.intersection = intersection
        self.bezier = bezier
        curve(x0, y0, x1, y1, x2, y2, x3, y3)
    
    def card_pos(self, cw, ch, k):
        (top, bot) = (ey - self.eh, ey + self.eh)
        (TOP, BOT) = (top - ch, bot + ch)
        (lef, rig) = (ex - self.ew, ex + self.ew)
        (LEF, RIG) = (lef - cw, rig + cw)
        (xr, yr) = self.intersection(LEF, TOP, RIG, BOT)
        (xg, yg) = self.intersection(lef, TOP, rig, BOT)
        (xb, yb) = self.intersection(LEF, top, RIG, bot)
        if self.spin == 1:
            if (yr == BOT and xr <= rig) or (xr == LEF and yr >= bot):
                (y, x) = (bot, max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot))
            elif (xr == RIG and yr >= top) or yr == BOT:
                (x, y) = (rig, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) - ch)
            elif (yr == TOP and xr >= lef) or xr == RIG:
                (y, x) = (TOP, min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) - cw)
            else:
                (x, y) = (LEF, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef))
        else:
            if (yr == BOT and xr >= lef) or (xr == RIG and yr >= bot):
                (y, x) = (bot, min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) - cw)
            elif xr == RIG or (yr == TOP and xr >= rig):
                (x, y) = (rig, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig))
            elif yr == TOP or (xr == RIG and yr <= top):
                (y, x) = (TOP, max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top))
            else:
                (x, y) = (LEF, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) - ch)
        return (x, y + ch)
    
    def arrow(self, direction, t):
        t0 = self.bisection(lambda x, y: abs(x - self.ax) > self.aw or abs(y - self.ay) > self.ah)
        t3 = self.bisection(lambda x, y: abs(x - self.ex) < self.ew and abs(y - self.ey) < self.eh)
        if direction == "<":
            (t0, t3) = (t3, t0)
        tc = t0 + (t3 - t0) * t
        (xc, yc) = self.bezier(tc)
        (x, y) = self.derivate(tc)
        if direction == "<":
            (x, y) = (-x, -y)
        arrow(xc, yc, x, -y)
