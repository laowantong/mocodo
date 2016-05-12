#!/usr/bin/env python
# encoding: utf-8

import font_metrics
import re

from attribute import *
from leg import *

match_leg = re.compile(r"((?:_11|..)[<>]?\s+(?:\[.+?\]\s+)?)(.+)").match

class Association:

    def __init__(self, clause, params={"df": u"DF"}):
        def clean_up(name, legs, attributes):
            name = name.strip(" \n\t")
            cartouche = (name[:-1] if name[-1].isdigit() else name)
            (cards, entities) = ([], [])
            l = []
            for leg in legs.split(","):
                leg = leg.strip(" \n\t")
                m = match_leg(leg)
                if m:
                    l.append(m.groups())
                else:
                    raise RuntimeError(("Mocodo Err.2 - " + _('Missing cardinalities in leg "{leg}" of association "{association}".').format(leg=leg, association=name).encode("utf8")))
            (cards, entities) = zip(*l)
            return (name, cartouche, cards, list(entities), outer_split(attributes))

        (name, legs_and_attributes) = clause.split(",", 1)
        (legs, attributes) = (legs_and_attributes.split(":", 1) + [""])[:2]
        (self.name, self.cartouche, cards, entities, attributes) = clean_up(name, legs, attributes)
        self.attributes = [SimpleAssociationAttribute(attribute, i) for (i, attribute) in enumerate(attributes)]
        entities = [(e.strip(" \n\t"), entities.count(e), entities[:i].count(e)) for (i, e) in enumerate(entities)]
        self.legs = [(StraightLeg(self, card, entity) if count == 1 else CurvedLeg(self, card, entity, count, num)) for (card, (entity, count, num)) in zip(cards, entities)]
        self.df_label = params["df"]
        self.check_df_strategy(self.cartouche == self.df_label)
        self.kind = "association"
        self.clause = clause

    def calculate_size(self, style):
        self.style = style
        cartouche_font = font_metrics.FontMetrics(style["association_cartouche_font"])
        self.get_cartouche_string_width = cartouche_font.get_pixel_width
        self.cartouche_height = cartouche_font.get_pixel_height()
        attribute_font = font_metrics.FontMetrics(style["association_attribute_font"])
        self.attribute_height = attribute_font.get_pixel_height()
        self.calculate_size_depending_on_df()
        self.w += self.w % 2
        self.h += self.h % 2
        for leg in self.legs:
            leg.calculate_size(style)

    def check_df_strategy(self, is_df):

        def calculate_size_when_df():
            self.w = self.h = max(self.style["round_rect_margin_width"] * 2 + self.get_cartouche_string_width(
                self.df_label), self.style["round_rect_margin_width"] * 2 + self.cartouche_height)

        def calculate_size_when_not_df():
            for attribute in self.attributes:
                attribute.calculate_size(self.style)
            self.w = 2 * self.style["round_rect_margin_width"] + \
                max([a.w for a in self.attributes] + [self.get_cartouche_string_width(self.cartouche)])
            self.h = max(1, len(self.attributes)) * (self.attribute_height + self.style["line_skip_height"]) - \
                self.style["line_skip_height"] + \
                2 * self.style["rect_margin_height"] + \
                2 * self.style["round_rect_margin_height"] + \
                self.cartouche_height

        def description_when_df():
            return [
                {
                    "key": u"stroke_depth",
                    "stroke_depth": self.style["box_stroke_depth"],
                },
                {
                    "key": u"stroke_color",
                    "stroke_color": "association_stroke_color",
                },
                {
                    "key": u"color",
                    "color": "association_cartouche_color",
                },
                {
                    "key": u"circle",
                    "cx": "x",
                    "cy": "y",
                    "r": self.w / 2.0,
                },
                {
                    "key": u"text",
                    "text": self.df_label,
                    "text_color": "association_cartouche_text_color",
                    "x": "%s+x" % (self.style["round_rect_margin_width"] - self.w / 2),
                    "y": "%s+y" % (self.style["round_rect_margin_height"] - self.h / 2 + 
                                   self.style["df_text_height_ratio"] * self.cartouche_height),
                    "family": self.style["association_cartouche_font"]["family"],
                    "size": self.style["association_cartouche_font"]["size"],
                },
            ]

        def description_when_not_df():
            result = [
                {
                    "key": u"stroke_depth",
                    "stroke_depth": 0,
                },
                {
                    "key": u"stroke_color",
                    "stroke_color": "association_cartouche_color",
                },
                {
                    "key": u"color",
                    "color": "association_cartouche_color",
                },
                {
                    "key": u"upper_round_rect",
                    "radius": self.style["round_corner_radius"],
                    "x": "%s+x" % (-self.w / 2),
                    "y": "%s+y" % (-self.h / 2),
                    "w": self.w,
                    "h": self.attribute_height +
                         self.style["round_rect_margin_height"] +
                         self.style["rect_margin_height"],
                },
                {
                    "key": u"stroke_color",
                    "stroke_color": "association_color",
                },
                {
                    "key": u"color",
                    "color": "association_color",
                },
                {
                    "key": u"lower_round_rect",
                    "radius": self.style["round_corner_radius"],
                    "x": "%s+x" % (-self.w / 2),
                    "y": "%s+y" % (self.attribute_height + self.style["round_rect_margin_height"] + self.style["rect_margin_height"] - self.h / 2),
                    "w": self.w,
                    "h": self.h - (self.attribute_height + self.style["round_rect_margin_height"] + self.style["rect_margin_height"]),
                },
                {
                    "key": u"color",
                    "color": "transparent_color",
                },
                {
                    "key": u"stroke_color",
                    "stroke_color": "association_stroke_color",
                },
                {
                    "key": u"stroke_depth",
                    "stroke_depth": self.style["box_stroke_depth"],
                },
                {
                    "key": u"round_rect",
                    "radius": self.style["round_corner_radius"],
                    "x": "%s+x" % (-self.w / 2),
                    "y": "%s+y" % (-self.h / 2),
                    "w": self.w,
                    "h": self.h,
                },
                {
                    "key": u"stroke_depth",
                    "stroke_depth": self.style["inner_stroke_depth"],
                },
                {
                    "key": u"line",
                    "x0": "%s+x" % (-self.w / 2),
                    "y0": "%s+y" % (self.attribute_height + self.style["round_rect_margin_height"] + self.style["rect_margin_height"] - self.h / 2),
                    "x1": "%s+x" % (self.w / 2),
                    "y1": "%s+y" % (self.attribute_height + self.style["round_rect_margin_height"] + self.style["rect_margin_height"] - self.h / 2),
                },
                {
                    "key": u"text",
                    "text": self.cartouche,
                    "text_color": "association_cartouche_text_color",
                    "x": "%s+x" % (-self.get_cartouche_string_width(self.cartouche) / 2),
                    "y": "%s+y" % (-self.h / 2 + self.style["rect_margin_height"] + self.style["cartouche_text_height_ratio"] * self.cartouche_height),
                    "family": self.style["association_cartouche_font"]["family"],
                    "size": self.style["association_cartouche_font"]["size"],
                }
            ]
            dx = self.style["round_rect_margin_width"] - self.w / 2
            dy = self.style["round_rect_margin_height"] + self.cartouche_height + 2 * self.style["rect_margin_height"] - self.h / 2
            for attribute in self.attributes:
                attribute.name = self.name
                result.extend(attribute.description(dx, dy))
                dy += self.attribute_height + self.style["line_skip_height"]
            return result

        if is_df:
            self.calculate_size_depending_on_df = calculate_size_when_df
            self.description_depending_on_df = description_when_df
        else:
            self.calculate_size_depending_on_df = calculate_size_when_not_df
            self.description_depending_on_df = description_when_not_df

    def set_df_label(self, df_label):
        self.set_df_label_depending_on_df(df_label)

    def description(self):
        return self.leg_descriptions() + [
            {
                "key": u"begin",
                "id": u"association-%s" % self.name,
            },
        ] + self.description_depending_on_df() + [
            {
                "key": u"end",
            },
        ]

    def leg_descriptions(self):
        result = [
            "Association %s" % self.name,
            {
                "key": u"env",
                "env": [("x", """cx[u"%s"]""" % self.name), ("y", """cy[u"%s"]""" % self.name)],
            },
        ]
        for leg in self.legs:
            result.extend(leg.description())
        return result

    def leg_identifiers(self):
        for leg in self.legs:
            yield leg.identifier()
