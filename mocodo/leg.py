#!/usr/bin/env python
# encoding: utf-8

import font_metrics
import sys
import re

match_card = re.compile(r"(_11|..)([<>]?)\s*(?:\[(.+?)\])?").match

html_escape_table = {
    "&": "&amp;",
    '"': r'\\"',
    "'": r"\\'",
    ">": "&gt;",
    "<": "&lt;",
}

auto_correction = {
    "01": ["O1", "o1", "10", "1O", "1o"],
    "0N": ["ON", "oN", "NO", "No", "N0"],
    "0n": ["On", "on", "no", "nO", "n0"],
    "1N": ["N1"],
    "1n": ["n1"]
}
auto_correction = dict((v,k) for k in auto_correction for v in auto_correction[k])

def html_escape(text):
    return "".join(html_escape_table.get(c,c) for c in text)

class Leg:

    def __init__(self, association, card, entity_name):
        self.association = association
        self.may_identify = not entity_name.startswith("/")
        if not self.may_identify:
            entity_name = entity_name[1:]
        self.entity_name = entity_name
        (self.cards, self.arrow, self.annotation) = match_card(card).groups()
        self.strengthen = self.cards == "_11"
        if self.strengthen:
            self.cards = "11"
        else:
            self.cards = auto_correction.get(self.cards, self.cards)
        if self.annotation:
            self.annotation = html_escape(self.annotation.replace("<<<protected-comma>>>", ",").replace("<<<protected-colon>>>", ":"))

    def calculate_size(self, style):
        font = font_metrics.FontMetrics(style["card_font"])
        self.h = font.get_pixel_height()
        self.w = font.get_pixel_width(self.cardinalities)
        self.style = style

    def set_card_sep(self, card_sep):
        self.cardinalities = (u"" if self.cards.startswith("XX") else self.cards[0] + card_sep + self.cards[1])


class StraightLeg(Leg):

    def __init__(self, association, card, entity_name):
        Leg.__init__(self, association, card, entity_name)
        self.num = 0

    def description(self):
        result = []
        result.append({
                "key": u"stroke_color",
                "stroke_color": "leg_stroke_color",
            })
        result.append({
                "key": u"stroke_depth",
                "stroke_depth": self.style["leg_stroke_depth"],
            })
        result.append({
                "key": u"env",
                "env": [("ex", """cx[u"%s"]""" % self.entity.name), ("ey", """cy[u"%s"]""" % self.entity.name)],
            })
        result.append({
                "key": u"line",
                "x0": "ex",
                "y0": "ey",
                "x1": "x",
                "y1": "y",
            })
        result.append({
            "key": u"card",
            "text": self.cardinalities,
            "text_color": "card_text_color",
            "ex": "ex",
            "ey": "%s+ey" % (self.style["card_text_height_ratio"] * self.h),
            "ew": self.entity.w,
            "eh": self.entity.h,
            "ax": "x",
            "ay": "%s+y" % (self.style["card_text_height_ratio"] * self.h),
            "leg_identifier": "%s,%s" % (self.association.name, self.entity_name),
            "family": self.style["card_font"]["family"],
            "size": self.style["card_font"]["size"],
        })
        if self.annotation:
            result[-1].update({
                "key": u"annotated_card",
                "annotation": self.annotation,
            })
        if self.strengthen:
            result.append({
                    "key": u"stroke_depth",
                    "stroke_depth": self.style["card_underline_depth"],
                })
            result.append({
                    "key": u"stroke_color",
                    "stroke_color": "card_text_color",
                })
            result.append({
                    "key": u"card_underline",
                    "x1": "tx",
                    "x2": "tx+%s" % font_metrics.FontMetrics(self.style["card_font"]).get_pixel_width(self.cardinalities),
                    "y1": "ty-%s" % self.style["card_underline_skip_height"],
                })
        if self.arrow == ">":
            result.extend([
                {
                    "key": u"color",
                    "color": "leg_stroke_color",
                },
                {
                    "key": u"stroke_depth",
                    "stroke_depth": 0,
                },
                {
                    "key": u"line_arrow",
                    "x0": "ex",
                    "y0": "ey",
                    "w0": self.entity.w / 2,
                    "h0": self.entity.h / 2,
                    "x1": "x",
                    "y1": "y",
                    "w1": self.association.w / 2,
                    "h1": self.association.h / 2,
                    "leg_identifier": "%s,%s" % (self.association.name, self.entity_name),
                }
            ])
        elif self.arrow == "<":
            result.extend([
                {
                    "key": u"color",
                    "color": "leg_stroke_color",
                },
                {
                    "key": u"stroke_depth",
                    "stroke_depth": 0,
                },
                {
                    "key": u"line_arrow",
                    "x1": "ex",
                    "y1": "ey",
                    "w1": self.entity.w / 2,
                    "h1": self.entity.h / 2,
                    "x0": "x",
                    "y0": "y",
                    "w0": self.association.w / 2,
                    "h0": self.association.h / 2,
                    "leg_identifier": "%s,%s" % (self.association.name, self.entity_name),
                }
            ])
        return result

    def identifier(self):
        return "%s,%s" % (self.association.name, self.entity_name)

    def value(self):
        return 1.0


class CurvedLeg(Leg):

    def __init__(self, association, card, entity_name, count, num):
        Leg.__init__(self, association, card, entity_name)
        self.count = count
        self.num = num
        self.spin = float(2 * self.num) / (self.count - 1) - 1

    def description(self):
        (x0, y0) = (self.entity.x + self.entity.w / 2, self.entity.y + self.entity.h / 2)
        (x3, y3) = (self.association.x + self.association.w / 2, self.association.y + self.association.h / 2)
        result = []
        result.append({
                "key": u"stroke_depth",
                "stroke_depth": self.style["leg_stroke_depth"],
            })
        result.append({
                "key": u"stroke_color",
                "stroke_color": "leg_stroke_color",
            })
        result.append({
                "key": u"env",
                "env": [("ex", """cx[u"%s"]""" % self.entity.name), ("ey", """cy[u"%s"]""" % self.entity.name)],
            })
        result.append({
                "key": u"env",
                "env": [("d", "hypot(x-ex,y-ey)")],
            })
        result.append({
                "key": u"curve",
                "x0": "ex",
                "y0": "ey",
                "x1": "ex+(x-ex)*%s-%s*(%s*(y-ey)/d)" % (self.style["curvature_ratio"], self.spin, self.style["curvature_length"]),
                "y1": "ey+(y-ey)*%s+%s*(%s*(x-ex)/d)" % (self.style["curvature_ratio"], self.spin, self.style["curvature_length"]),
                "x2": "x+(ex-x)*%s-%s*(%s*(y-ey)/d)" % (self.style["curvature_ratio"], self.spin, self.style["curvature_length"]),
                "y2": "y+(ey-y)*%s+%s*(%s*(x-ex)/d)" % (self.style["curvature_ratio"], self.spin, self.style["curvature_length"]),
                "x3": "x",
                "y3": "y",
            })
        result.append({
            "key": u"card",
            "text": self.cardinalities,
            "text_color": "card_text_color",
            "ex": "ex",
            "ey": "%s+ey" % (self.style["card_text_height_ratio"] * self.h),
            "ew": self.entity.w / 2,
            "eh": self.entity.h / 2,
            "ax": "x",
            "ay": "%s+y" % (self.style["card_text_height_ratio"] * self.h),
            "leg_identifier": self.identifier(),
            "family": self.style["card_font"]["family"],
            "size": self.style["card_font"]["size"],
        })
        if self.annotation:
            result[-1].update({
                "key": u"annotated_card",
                "annotation": self.annotation,
            })
        if self.strengthen:
            result.append({
                    "key": u"stroke_depth",
                    "stroke_depth": self.style["card_underline_depth"],
                })
            result.append({
                    "key": u"stroke_color",
                    "stroke_color": "card_text_color",
                })
            result.append({
                    "key": u"card_underline",
                    "x1": "tx",
                    "x2": "tx+%s" % font_metrics.FontMetrics(self.style["card_font"]).get_pixel_width(self.cardinalities),
                    "y1": "ty-%s" % self.style["card_underline_skip_height"],
                })
        if self.arrow == ">":
            result.extend([
                {
                    "key": u"color",
                    "color": "leg_stroke_color",
                },
                {
                    "key": u"stroke_depth",
                    "stroke_depth": 0,
                },
                {
                    "key": u"curve_arrow",
                    "x0": "ex",
                    "y0": "ey",
                    "w0": self.entity.w / 2,
                    "h0": self.entity.h / 2,
                    "x1": "ex+(x-ex)*%s-%s*(%s*(y-ey)/d)" % (self.style["curvature_ratio"], self.spin, self.style["curvature_length"]),
                    "y1": "ey+(y-ey)*%s+%s*(%s*(x-ex)/d)" % (self.style["curvature_ratio"], self.spin, self.style["curvature_length"]),
                    "x2": "x+(ex-x)*%s-%s*(%s*(y-ey)/d)" % (self.style["curvature_ratio"], self.spin, self.style["curvature_length"]),
                    "y2": "y+(ey-y)*%s+%s*(%s*(x-ex)/d)" % (self.style["curvature_ratio"], self.spin, self.style["curvature_length"]),
                    "x3": "x",
                    "y3": "y",
                    "w3": self.association.w / 2,
                    "h3": self.association.h / 2,
                    "leg_identifier": self.identifier(),
                }
            ])
        elif self.arrow == "<":
            result.extend([
                {
                    "key": u"color",
                    "color": "leg_stroke_color",
                },
                {
                    "key": u"stroke_depth",
                    "stroke_depth": 0,
                },
                {
                    "key": u"curve_arrow",
                    "x3": "ex",
                    "y3": "ey",
                    "w3": self.entity.w / 2,
                    "h3": self.entity.h / 2,
                    "x2": "ex+(x-ex)*%s-%s*(%s*(y-ey)/d)" % (self.style["curvature_ratio"], self.spin, self.style["curvature_length"]),
                    "y2": "ey+(y-ey)*%s+%s*(%s*(x-ex)/d)" % (self.style["curvature_ratio"], self.spin, self.style["curvature_length"]),
                    "x1": "x+(ex-x)*%s-%s*(%s*(y-ey)/d)" % (self.style["curvature_ratio"], self.spin, self.style["curvature_length"]),
                    "y1": "y+(ey-y)*%s+%s*(%s*(x-ex)/d)" % (self.style["curvature_ratio"], self.spin, self.style["curvature_length"]),
                    "x0": "x",
                    "y0": "y",
                    "w0": self.association.w / 2,
                    "h0": self.association.h / 2,
                    "leg_identifier": self.identifier(),
                }
            ])
        return result

    def identifier(self):
        return "%s,%s,%s" % (self.association.name, self.entity_name, self.spin)

    def value(self):
        return 2 * self.spin * self.count
