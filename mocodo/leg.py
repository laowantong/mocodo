import operator
from math import hypot, sqrt

from .mocodo_error import MocodoError
from .tools.string_tools import surrounds, raw_to_bid


class Leg:
    def __init__(self, association, leg, **params):
        params["card_format"] = params.get("card_format", "{min_card},{max_card}")

        self.card = leg.get("card", "XX")
        if self.card == "XX" or leg.get("card_hidden") == "-":
            self.card_view = "     "
        elif "X" in self.card:
            self.card_view = self.card.replace("X", "")
        else:
            self.card_view = params["card_format"].format(min_card=self.card[0], max_card=self.card[1])
        
        self.has_underlined_card = False
        if leg.get("card_prefix") == "_":
            if self.card != "11": # silently ignore the prefix
                self.kind = "leg"
                del leg["card_prefix"]
            else:
                self.kind = "strengthening"
                self.card_view = params.get("strengthen_card", "_1,1_")
                if surrounds(self.card_view, "_"):
                    self.has_underlined_card = True
                    self.card_view = self.card_view[1:-1]
        elif association.kind == "cluster":
            self.kind = "cluster_peg" if leg.get("card_prefix") == "/" else "cluster_leg"
        else:
            self.kind = "leg"
        
        self.arrow = leg.get("leg_arrow", "")
        self.peg = ("o" if self.kind == "cluster_peg" and not self.arrow else "")
        self.note = leg.get("leg_note")
        self.association = association
        self.entity_raw_name = leg["entity"]
        self.entity_bid = raw_to_bid(self.entity_raw_name)
        self.twist = False
        self.lid = None
        self.unicities = ""
        self.is_in_elected_group = False

    def register_entity(self, entity):
        self.entity = entity
    
    def register_mcd_has_cif(self, mcd_has_cif):
        self.mcd_has_cif = mcd_has_cif
        if self.mcd_has_cif:
            self.peg = ""

    def append_candidate_group(self, candidate_number: str):
        if candidate_number == "0":
            self.is_in_elected_group = True
        else:
            # concatenate the candidate number to the beginning of the string to ensure sorting
            self.unicities = candidate_number + self.unicities

    def calculate_size(self, style, get_font_metrics):
        font = get_font_metrics(style["card_font"])
        self.h = font.get_pixel_height()
        self.w = font.get_pixel_width(self.card_view)

    def set_spin_strategy(self, spin):
        self.spin = spin
        self.description = self._curved_description if spin else self._straight_description
        if self.lid is None:
            spin_str = str(round(spin, 2)).replace(".", "_")  # avoid dot for the web version
            self.lid = f"{self.association.bid},{self.entity_bid},{spin_str}"

    def _straight_description(self, style, geo):
        result = []
        ex = self.entity.cx
        ey = self.entity.cy
        ew = self.entity.w // 2
        eh = self.entity.h // 2
        ax = self.association.cx
        ay = self.association.cy
        aw = self.association.w // 2
        ah = self.association.h // 2
        card_margin = style["card_margin"]
        cw = self.w + 2 * card_margin
        ch = self.h + 2 * card_margin
        leg = straight_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, cw, ch, card_margin)
        if self.peg:
            (x, y, a, b) = leg.arrow_pos(self.arrow, 1)
            c = hypot(a, b)
            (cos, sin) = (a / c, b / c)
            result.append(
                (
                    "circle",
                    {
                        "cx": x + cos * style["arrow_width"] / 2,
                        "cy": y - sin * style["arrow_width"] / 2,
                        "r": style["arrow_width"] / 2,
                        "stroke_color": style["entity_stroke_color"],
                        "stroke_depth": style["leg_stroke_depth"],
                        "color": style["entity_color"]+ "55", # alpha channel
                    },
                ),
            )
        result.append(
            (
                "line",
                {
                    "x0": ex,
                    "y0": ey,
                    "x1": ax,
                    "y1": ay,
                    "stroke_color": style["leg_stroke_color"],
                    "stroke_depth": style["leg_stroke_depth"],
                },
            )
        )
        (x, y) = leg.card_pos(self.twist, geo["shift"][self.lid])
        tx = x + card_margin
        ty = y - card_margin - style["card_baseline"]
        self.saved_card_description = []
        if self.note:
            self.saved_card_description.append(
                (
                    "text_with_note",
                    {
                        "x": tx,
                        "y": ty,
                        "text_color": style["card_text_color"],
                        "family": style["card_font"]["family"],
                        "size": style["card_font"]["size"],
                        "text": self.card_view,
                        "note": self.note.lstrip("+").lstrip("-")
                    },
                )
            )
        else:
            self.saved_card_description.append(
                (
                    "text",
                    {
                        "x": tx,
                        "y": ty,
                        "text_color": style["card_text_color"],
                        "family": style["card_font"]["family"],
                        "size": style["card_font"]["size"],
                        "text": self.card_view,
                    },
                )
            )
        if self.has_underlined_card:
            self.saved_card_description.append(
                (
                    "line",
                    {
                        "x0": tx,
                        "y0": ty - style["card_underline_skip_height"],
                        "x1": tx + self.w,
                        "y1": ty - style["card_underline_skip_height"],
                        "stroke_color": style["card_text_color"],
                        "stroke_depth": style["card_underline_depth"],
                    },
                )
            )
        if self.arrow:
            (x, y, a, b) = leg.arrow_pos(self.arrow, geo["ratio"][self.lid])
            c = hypot(a, b)
            (cos, sin) = (a / c, b / c)
            result.append(
                (
                    "arrow",
                    {
                        "x0": x,
                        "y0": y,
                        "x1": x + style["arrow_width"] * cos - style["arrow_half_height"] * sin,
                        "y1": y - style["arrow_half_height"] * cos - style["arrow_width"] * sin,
                        "x2": x + style["arrow_axis"] * cos,
                        "y2": y - style["arrow_axis"] * sin,
                        "x3": x + style["arrow_width"] * cos + style["arrow_half_height"] * sin,
                        "y3": y + style["arrow_half_height"] * cos - style["arrow_width"] * sin,
                        "stroke_color": style["leg_stroke_color"],
                    },
                ),
            )
        return result

    def _curved_description(self, style, geo):
        result = []
        ex = self.entity.cx
        ey = self.entity.cy
        ew = self.entity.w // 2
        eh = self.entity.h // 2
        ax = self.association.cx
        ay = self.association.cy
        aw = self.association.w // 2
        ah = self.association.h // 2
        card_margin = style["card_margin"]
        cw = self.w + 2 * card_margin
        ch = self.h + 2 * card_margin
        spin = self.spin
        leg = curved_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, cw, ch, card_margin, spin)
        (x0, y0, x1, y1, x2, y2, x3, y3) = leg.points
        if self.peg:
            (x, y, a, b) = leg.arrow_pos(self.arrow, 1)
            c = hypot(a, b)
            (cos, sin) = (a / c, b / c)
            result.append(
                (
                    "circle",
                    {
                        "cx": x + cos * style["arrow_width"] / 2,
                        "cy": y - sin * style["arrow_width"] / 2,
                        "r": style["arrow_width"] / 2,
                        "stroke_color": style["entity_stroke_color"],
                        "stroke_depth": style["leg_stroke_depth"],
                        "color": style["entity_color"]+ "55", # alpha channel
                    },
                ),
            )
        result.append(
            (
                "curve",
                {
                    "x0": x0,
                    "y0": y0,
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "x3": x3,
                    "y3": y3,
                    "stroke_color": style["leg_stroke_color"],
                    "stroke_depth": style["leg_stroke_depth"],
                },
            )
        )
        (x, y) = leg.card_pos(geo["shift"][self.lid])
        tx = x + card_margin
        ty = y - card_margin - style["card_baseline"]
        self.saved_card_description = []
        if self.note:
            self.saved_card_description.append(
                (
                    "text_with_note",
                    {
                        "x": tx,
                        "y": ty,
                        "text_color": style["card_text_color"],
                        "family": style["card_font"]["family"],
                        "size": style["card_font"]["size"],
                        "text": self.card_view,
                        "note": self.note.lstrip("+").lstrip("-"),
                    },
                )
            )
        else:
            self.saved_card_description.append(
                (
                    "text",
                    {
                        "x": tx,
                        "y": ty,
                        "text_color": style["card_text_color"],
                        "family": style["card_font"]["family"],
                        "size": style["card_font"]["size"],
                        "text": self.card_view,
                    },
                )
            )
        if self.has_underlined_card:
            self.saved_card_description.append(
                (
                    "line",
                    {
                        "x0": tx,
                        "y0": ty - style["card_underline_skip_height"],
                        "x1": tx + self.w,
                        "y1": ty - style["card_underline_skip_height"],
                        "stroke_color": style["card_text_color"],
                        "stroke_depth": style["card_underline_depth"],
                    },
                )
            )
        if self.arrow:
            (x, y, a, b) = leg.arrow_pos(self.arrow, geo["ratio"][self.lid])
            c = hypot(a, b)
            (cos, sin) = (a / c, b / c)
            result.append(
                (
                    "arrow",
                    {
                        "x0": x,
                        "y0": y,
                        "x1": x + style["arrow_width"] * cos - style["arrow_half_height"] * sin,
                        "y1": y - style["arrow_half_height"] * cos - style["arrow_width"] * sin,
                        "x2": x + style["arrow_axis"] * cos,
                        "y2": y - style["arrow_axis"] * sin,
                        "x3": x + style["arrow_width"] * cos + style["arrow_half_height"] * sin,
                        "y3": y + style["arrow_half_height"] * cos - style["arrow_width"] * sin,
                        "stroke_color": style["leg_stroke_color"],
                    },
                ),
            )
        return result

class InheritanceLeg:
    def __init__(self, inheritance, leg, **params):
        self.kind = leg["kind"] # "-" or "="
        self.arrow = leg["arrow"]
        self.inheritance = inheritance
        self.entity_bid = raw_to_bid(leg["entity"])
        self.entity_raw_name = leg["entity"]
        self.lid = f"{self.inheritance.bid} / {self.entity_bid}"

    def register_entity(self, entity):
        self.entity = entity
    
    def calculate_size(self, style, get_font_metrics):
        font = get_font_metrics(style["card_font"])
        self.h = font.get_pixel_height()
        self.w = font.get_pixel_width("--")

    def description(self, style, geo):
        result = []
        ex = self.entity.cx
        ey = self.entity.cy
        ew = self.entity.w // 2
        eh = self.entity.h // 2
        ax = self.inheritance.cx
        ay = self.inheritance.cy
        aw = self.inheritance.w // 2
        ah = self.inheritance.h // 2
        card_margin = style["card_margin"]
        cw = self.w + 2 * card_margin
        ch = self.h + 2 * card_margin
        leg = straight_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, cw, ch, card_margin)
        if self.kind == "=":
            for d in (style["leg_stroke_depth"], -style["leg_stroke_depth"]):
                (x0, y0, x1, y1) = orthogonal_translation(ex, ey, ax, ay, d)
                result.append(
                    (
                        "line",
                        {
                            "x0": x0,
                            "y0": y0,
                            "x1": x1,
                            "y1": y1,
                            "stroke_color": style["leg_stroke_color"],
                            "stroke_depth": style["leg_stroke_depth"],
                        },
                    )
                )
        else:
            result.append(
                (
                    "line",
                    {
                        "x0": ex,
                        "y0": ey,
                        "x1": ax,
                        "y1": ay,
                        "stroke_color": style["leg_stroke_color"],
                        "stroke_depth": style["leg_stroke_depth"],
                    },
                )
            )
        if self.arrow:
            (x, y, a, b) = leg.arrow_pos(self.arrow, geo["ratio"][self.lid])
            c = hypot(a, b)
            (cos, sin) = (a / c, b / c)
            result.append(
                (
                    "arrow",
                    {
                        "x0": x,
                        "y0": y,
                        "x1": x + style["arrow_width"] * cos - style["arrow_half_height"] * sin,
                        "y1": y - style["arrow_half_height"] * cos - style["arrow_width"] * sin,
                        "x2": x + style["arrow_axis"] * cos,
                        "y2": y - style["arrow_axis"] * sin,
                        "x3": x + style["arrow_width"] * cos + style["arrow_half_height"] * sin,
                        "y3": y + style["arrow_half_height"] * cos - style["arrow_width"] * sin,
                        "stroke_color": style["leg_stroke_color"],
                    },
                ),
            )
        return result


class ConstraintLeg:

    def __init__(self, constraint, kind, box_raw_name):
        self.constraint = constraint
        self.kind = kind
        self.bid = raw_to_bid(box_raw_name)
        self.entity_raw_name = box_raw_name
        self.lid = None
    
    def register_box(self, box):
        self.box = box
    
    def description(self, style, geo):
        if self.kind == "": # a phantom leg, useful to tweak the barycenter
            return []
        result = []
        bx = self.box.cx
        by = self.box.cy
        bw = self.box.w // 2
        bh = self.box.h // 2
        cx = self.constraint.cx
        cy = self.constraint.cy
        cw = self.constraint.w // 2
        ch = self.constraint.h // 2
        leg = straight_leg_factory(bx, by, bw, bh, cx, cy, cw, ch)
        kind = self.kind
        for direction in "<>":
            if direction in self.kind:
                (x, y, a, b) = leg.arrow_pos(direction, 1)
                c = hypot(a, b) or 1
                (cos, sin) = (a / c, b / c)
                result.append(
                    (
                        "arrow",
                        {
                            "x0": x,
                            "y0": y,
                            "x1": x + style["arrow_width"] * cos - style["arrow_half_height"] * sin,
                            "y1": y - style["arrow_half_height"] * cos - style["arrow_width"] * sin,
                            "x2": x + style["arrow_axis"] * cos,
                            "y2": y - style["arrow_axis"] * sin,
                            "x3": x + style["arrow_width"] * cos + style["arrow_half_height"] * sin,
                            "y3": y + style["arrow_half_height"] * cos - style["arrow_width"] * sin,
                            "stroke_color": style["constraint_stroke_color"],
                        },
                    ),
                )
                kind = kind.replace(direction, "")
        if kind[:1] == "-":
            result.append(
                (
                    "line",
                    {
                        "x0": bx,
                        "y0": by,
                        "x1": cx,
                        "y1": cy,
                        "stroke_color": style["constraint_stroke_color"],
                        "stroke_depth": style["constraint_stroke_depth"],
                    }
                )
            )
        elif kind[:1] == ".":
            result.append(
                (
                    "dot_line",
                    {
                        "x0": bx,
                        "y0": by,
                        "x1": cx,
                        "y1": cy,
                        "stroke_color": style["constraint_stroke_color"],
                        "stroke_depth": style["constraint_dot_stroke_depth"],
                        "dash_gap": style["constraint_dot_gap_width"],
                    }
                )
            )
        else:
            raise NotImplementedError
        return result


def line_intersection(ex, ey, w, h, ax, ay, cmp=lambda x, y: (x > y) - (x < y)):
    if ax == ex:
        return (ax, ey + cmp(ay, ey) * h)
    if ay == ey:
        return (ex + cmp(ax, ex) * w, ay)
    x = ex + cmp(ax, ex) * w
    y = ey + (ay - ey) * (x - ex) / (ax - ex)
    if abs(y - ey) > h:
        y = ey + cmp(ay, ey) * h
        x = ex + (ax - ex) * (y - ey) / (ay - ey)
    return (x, y)


def straight_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, cw=0, ch=0, card_margin=0):
    def card_pos(twist, shift):
        compare = operator.lt if twist else operator.le
        correction = 1 - abs(abs(ax - ex) - abs(ay - ey)) / hypot(ax - ex, ay - ey)
        correction = card_margin * 1.4142 * correction - shift
        (xg, yg) = line_intersection(ex, ey, ew, eh + ch, ax, ay)
        (xb, yb) = line_intersection(ex, ey, ew + cw, eh, ax, ay)
        if compare(xg, xb):
            if compare(xg, ex):
                if compare(yb, ey):
                    return (xb - correction, yb)
                else:
                    return (xb - correction, yb + ch)
            else:
                if compare(yb, ey):
                    return (xg, yg + ch - correction)
                else:
                    return (xg, yg + correction)
        else:
            if compare(xb, ex):
                if compare(yb, ey):
                    return (xg - cw, yg + ch - correction)
                else:
                    return (xg - cw, yg + correction)
            else:
                if compare(yb, ey):
                    return (xb - cw + correction, yb)
                else:
                    return (xb - cw + correction, yb + ch)

    def arrow_pos(direction, ratio):
        (x0, y0) = line_intersection(ex, ey, ew, eh, ax, ay)
        (x1, y1) = line_intersection(ax, ay, aw, ah, ex, ey)
        if direction == "<":
            (x0, y0, x1, y1) = (x1, y1, x0, y0)
        (x, y) = (ratio * x0 + (1 - ratio) * x1, ratio * y0 + (1 - ratio) * y1)
        return (x, y, x1 - x0, y0 - y1)

    straight_leg_factory.card_pos = card_pos
    straight_leg_factory.arrow_pos = arrow_pos
    return straight_leg_factory


def curved_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, cw, ch, card_margin, spin):
    def bisection(predicate):
        (a, b) = (0, 1)
        while abs(b - a) > 0.0001:
            m = (a + b) / 2
            if predicate(bezier(m)):
                a = m
            else:
                b = m
        return m

    def intersection(left, top, right, bottom):
        (x, y) = bezier(bisection(lambda p: left <= p[0] <= right and top <= p[1] <= bottom))
        return (int(round(x)), int(round(y)))  # avoid comparing floats

    def card_pos(shift):
        diagonal = hypot(ax - ex, ay - ey)
        correction = card_margin * 1.4142 * (1 - abs(abs(ax - ex) - abs(ay - ey)) / diagonal)
        (top, bot) = (ey - eh, ey + eh)
        (TOP, BOT) = (top - ch, bot + ch)
        (lef, rig) = (ex - ew, ex + ew)
        (LEF, RIG) = (lef - cw, rig + cw)
        (xr, yr) = intersection(LEF, TOP, RIG, BOT)
        (xg, yg) = intersection(lef, TOP, rig, BOT)
        (xb, yb) = intersection(LEF, top, RIG, bot)
        if spin > 0:
            if (yr == BOT and xr <= rig) or (xr == LEF and yr >= bot):
                return (
                    max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot)
                    - correction
                    + shift,
                    bot + ch,
                )
            if (xr == RIG and yr >= top) or yr == BOT:
                return (
                    rig,
                    min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig)
                    + correction
                    + shift,
                )
            if (yr == TOP and xr >= lef) or xr == RIG:
                return (
                    min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top)
                    + correction
                    + shift
                    - cw,
                    TOP + ch,
                )
            return (
                LEF,
                max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef)
                - correction
                + shift
                + ch,
            )
        if (yr == BOT and xr >= lef) or (xr == RIG and yr >= bot):
            return (
                min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot)
                + correction
                + shift
                - cw,
                bot + ch,
            )
        if xr == RIG or (yr == TOP and xr >= rig):
            return (
                rig,
                max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig)
                - correction
                + shift
                + ch,
            )
        if yr == TOP or (xr == LEF and yr <= top):
            return (
                max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top)
                - correction
                + shift,
                TOP + ch,
            )
        return (
            LEF,
            min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) + correction + shift,
        )

    def arrow_pos(direction, ratio):
        t0 = bisection(lambda p: abs(p[0] - ax) > aw or abs(p[1] - ay) > ah)
        t3 = bisection(lambda p: abs(p[0] - ex) < ew and abs(p[1] - ey) < eh)
        if direction == "<":
            (t0, t3) = (t3, t0)
        tc = t0 + (t3 - t0) * ratio
        (xc, yc) = bezier(tc)
        (x, y) = derivate(tc)
        if direction == "<":
            (x, y) = (-x, -y)
        return (xc, yc, x, -y)

    diagonal = hypot(ax - ex, ay - ey)
    (x, y) = line_intersection(ex, ey, ew + cw / 2, eh + ch / 2, ax, ay)
    k = cw * abs((ay - ey) / diagonal) + ch * abs((ax - ex) / diagonal)
    (x, y) = (x - spin * k * (ay - ey) / diagonal, y + spin * k * (ax - ex) / diagonal)
    (hx, hy) = (2 * x - (ex + ax) / 2, 2 * y - (ey + ay) / 2)
    (x1, y1) = (ex + (hx - ex) * 2 / 3, ey + (hy - ey) * 2 / 3)
    (x2, y2) = (ax + (hx - ax) * 2 / 3, ay + (hy - ay) * 2 / 3)
    (kax, kay) = (ex - 2 * hx + ax, ey - 2 * hy + ay)
    (kbx, kby) = (2 * hx - 2 * ex, 2 * hy - 2 * ey)
    bezier = lambda t: (kax * t * t + kbx * t + ex, kay * t * t + kby * t + ey)
    derivate = lambda t: (2 * kax * t + kbx, 2 * kay * t + kby)

    curved_leg_factory.points = (ex, ey, x1, y1, x2, y2, ax, ay)
    curved_leg_factory.card_pos = card_pos
    curved_leg_factory.arrow_pos = arrow_pos
    return curved_leg_factory

def orthogonal_translation(x1, y1, x2, y2, d):
    if x1 == x2:
        return (x1+d, y1, x1+d, y2)
    slope = (y2 - y1) / (x2 - x1)
    dy = sqrt(d * d / (slope * slope + 1))
    dx = -slope * dy
    if d > 0:
        return (x1+dx, y1+dy, x2+dx, y2+dy)
    else:
        return (x1-dx, y1-dy, x2-dx, y2-dy)
