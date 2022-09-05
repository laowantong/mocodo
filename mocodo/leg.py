import operator
import re
from math import hypot, sqrt

from .mocodo_error import MocodoError

auto_correction = {
    "01": ["O1", "o1", "10", "1O", "1o"],
    "0N": ["ON", "oN", "NO", "No", "N0"],
    "0n": ["On", "on", "no", "nO", "n0"],
    "1N": ["N1"],
    "1n": ["n1"],
}
auto_correction = {v: k for k in auto_correction for v in auto_correction[k]}


class Leg:
    def __init__(
        self,
        association,
        card,
        entity_name,
        match_card=re.compile(r"(_11|/0N|/1N|..)([<>]?)\s*(?:\[(.+?)\])?").match,
        **params,
    ):
        params["strengthen_card"] = params.get("strengthen_card", "_1,1_")
        params["card_format"] = params.get("card_format", "{min_card},{max_card}")
        (card, arrow, note) = match_card(card).groups()
        kind = "leg"
        if card == "_11":
            kind = "strengthening"
            card = "11"
            card_view = params["strengthen_card"]
        elif association.kind == "cluster":
            if card.startswith("/"):
                kind = "cluster_peg"
                card = card[1:]
            else:
                kind = "cluster_leg"
            card_view = params["card_format"].format(min_card=card[0], max_card=card[1])
        elif association.kind.startswith("inheritance"):
            if association.prettify_inheritance:
                if association.kind[-2:] == "=>" == card[:2]:
                    kind = "inheritance_emphasis"
                elif association.kind[-2:] == "<=" != card[:2]:
                    kind = "inheritance_emphasis"
                card_view = "     "
            else:
                card_view = "     "
        elif card.startswith("XX"):
            card_view = "     "
        else:
            card = auto_correction.get(card, card)
            card_view = params["card_format"].format(min_card=card[0], max_card=card[1])
        self.card = card
        self.arrow = arrow
        self.kind = kind
        self.card_view = card_view
        self.note = note and note.replace("<<<safe-comma>>>", ",").replace("<<<safe-colon>>>", ":")
        self.association = association
        self.entity_name = entity_name
        self.twist = False
        self.identifier = None

    def register_entity(self, entity):
        self.entity = entity

    def calculate_size(self, style, get_font_metrics):
        font = get_font_metrics(style["card_font"])
        self.h = font.get_pixel_height()
        self.w = font.get_pixel_width(self.card_view.strip("_"))

    def set_spin_strategy(self, spin):
        self.spin = spin
        self.description = self._curved_description if spin else self._straight_description
        if self.identifier is None:
            spin_str = str(round(spin, 2)).replace(".", "_")  # avoid dot for the web version
            self.identifier = f"{self.association.name},{self.entity_name},{spin_str}"

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
        if self.kind == "cluster_peg":
            result.append(
                (
                    "dash_line",
                    {
                        "x0": ex,
                        "y0": ey,
                        "x1": ax,
                        "y1": ay,
                        "stroke_color": style["leg_stroke_color"],
                        "stroke_depth": style["leg_stroke_depth"],
                        "dash_width": style["dash_width"],
                    },
                )
            )
        elif self.kind == "inheritance_emphasis":
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

        (x, y) = leg.card_pos(self.twist, geo["shift"][self.identifier])
        tx = x + card_margin
        ty = y - card_margin - style["card_baseline"]
        if self.note:
            result.append(
                (
                    "text_with_note",
                    {
                        "x": tx,
                        "y": ty,
                        "text_color": style["card_text_color"],
                        "family": style["card_font"]["family"],
                        "size": style["card_font"]["size"],
                        "note": self.note,
                        "text": self.card_view,
                    },
                )
            )
        else:
            result.append(
                (
                    "text",
                    {
                        "x": tx,
                        "y": ty,
                        "text_color": style["card_text_color"],
                        "family": style["card_font"]["family"],
                        "size": style["card_font"]["size"],
                        "note": self.note,
                        "text": self.card_view.strip("_"),
                    },
                )
            )
        if self.kind == "strengthening" and self.card_view[:1] + self.card_view[-1:] == "__":
            result.append(
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
            (x, y, a, b) = leg.arrow_pos(self.arrow, geo["ratio"][self.identifier])
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
        (x, y) = leg.card_pos(geo["shift"][self.identifier])
        tx = x + card_margin
        ty = y - card_margin - style["card_baseline"]
        if self.note:
            result.append(
                (
                    "text_with_note",
                    {
                        "x": tx,
                        "y": ty,
                        "text_color": style["card_text_color"],
                        "family": style["card_font"]["family"],
                        "size": style["card_font"]["size"],
                        "note": self.note,
                        "text": self.card_view,
                    },
                )
            )
        else:
            result.append(
                (
                    "text",
                    {
                        "x": tx,
                        "y": ty,
                        "text_color": style["card_text_color"],
                        "family": style["card_font"]["family"],
                        "size": style["card_font"]["size"],
                        "note": self.note,
                        "text": self.card_view.strip("_"),
                    },
                )
            )
        if self.kind == "strengthening" and self.card_view[:1] + self.card_view[-1:] == "__":
            result.append(
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
            (x, y, a, b) = leg.arrow_pos(self.arrow, geo["ratio"][self.identifier])
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


class DiagramLink:
    def __init__(self, entities, foreign_entity, foreign_key):
        self.foreign_entity = foreign_entity
        self.foreign_key = foreign_key
        try:
            self.primary_entity = entities[foreign_key.primary_entity_name]
        except KeyError:
            raise MocodoError(14, _('Attribute "{attribute}" in entity "{entity_1}" references an unknown entity "{entity_2}".').format(attribute=foreign_key.label, entity_1=foreign_entity.name, entity_2=foreign_key.primary_entity_name)) # fmt: skip
        for candidate in self.primary_entity.attributes:
            if candidate.label.lstrip("#") == foreign_key.primary_key_label.lstrip("#"):
                self.primary_key = candidate
                break
        else:
            raise MocodoError(15, _('Attribute "{attribute_1}" in entity "{entity_1}" references an unknown attribute "{attribute_2}" in entity "{entity_2}".').format(attribute_1=foreign_key.label, entity_1=foreign_entity.name, attribute_2=foreign_key.primary_key_label, entity_2=foreign_key.primary_entity_name)) # fmt: skip

    def calculate_size(self, style, *ignored):
        self.fdx = self.foreign_entity.w // 2
        self.pdx = self.primary_entity.w // 2
        self.fdy = (
            -self.foreign_entity.h // 2
            + 3 * style["rect_margin_height"]
            + self.foreign_entity.cartouche_height
            + (self.foreign_key.rank + 0.5)
            * (self.foreign_entity.attribute_height + style["line_skip_height"])
        )
        self.pdy = (
            -self.primary_entity.h // 2
            + 3 * style["rect_margin_height"]
            + self.primary_entity.cartouche_height
            + (self.primary_key.rank + 0.5)
            * (self.primary_entity.attribute_height + style["line_skip_height"])
        )
        self.offset = 2 * (style["card_margin"] + style["card_max_width"])

    def description(self, style, geo):
        result = [
            (
                "comment",
                {
                    "text": f'Link from "{self.foreign_key.primary_key_label}" ({self.foreign_entity.name}) to "{self.primary_key.label}" ({self.primary_entity.name})'
                },
            )
        ]
        spins = (
            [(-1, -1), (1, -1), (-1, 1), (1, 1)]
            if self.foreign_key.rank % 2
            else [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        )
        (fs, ps) = min(
            spins,
            key=lambda fs_ps: abs(
                geo["cx"][self.foreign_entity.name]
                + self.fdx * fs_ps[0]
                - geo["cx"][self.primary_entity.name]
                - self.pdx * fs_ps[1]
            ),
        )
        xf = geo["cx"][self.foreign_entity.name] + self.fdx * fs
        yf = geo["cy"][self.foreign_entity.name] + self.fdy
        xp = geo["cx"][self.primary_entity.name] + self.pdx * ps
        yp = geo["cy"][self.primary_entity.name] + self.pdy
        result.append(
            (
                "curve",
                {
                    "x0": xf,
                    "y0": yf,
                    "x1": xf + (xp - xf) / 2 if fs != ps else xf + self.offset * fs,
                    "y1": yf + (yp - yf) / 2,
                    "x2": xf + (xp - xf) / 3 if fs != ps else xp + self.offset * ps,
                    "y2": yp,
                    "x3": xp,
                    "y3": yp,
                    "stroke_color": style["leg_stroke_color"],
                    "stroke_depth": style["leg_stroke_depth"],
                },
            )
        )
        result.append(
            (
                "arrow",
                {
                    "color": style["leg_stroke_color"],
                    "x": xp,
                    "y": yp,
                    "a": ps,
                    "b": 0,
                },
            )
        )
        result.append(
            (
                "circle",
                {
                    "stroke_depth": style["box_stroke_depth"],
                    "cx": xf,
                    "cy": yf,
                    "r": style["box_stroke_depth"],
                },
            )
        )
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


def straight_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, cw, ch, card_margin):
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
