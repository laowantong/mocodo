#!/usr/bin/env python
# encoding: utf-8

import font_metrics

from attribute import *


class Entity:

    def __init__(self, clause):
        
        def clean_up(name, attributes):
            name = name.strip(" \n\t")
            cartouche = (name[:-1] if name[-1].isdigit() else name)
            return (name, cartouche, outer_split(attributes))
        
        (self.name, self.attribute_labels) = clause.split(":", 1)
        (self.name, self.cartouche, self.attribute_labels) = clean_up(self.name, self.attribute_labels)
        self.legs = [] # iterating over box's legs does nothing if it is not an association
        self.kind = "entity"
        self.clause = clause
    
    def set_strengthen_legs(self, legs):
        self.strengthen_legs = legs
        IdentifierAttribute = WeakAttribute if legs else StrongAttribute
        self.attributes = []
        for (i, attribute_label) in enumerate(self.attribute_labels):
            if attribute_label == "":
                self.attributes.append(PhantomAttribute(i))
            elif attribute_label.startswith("_"):
                if i == 0:
                    self.attributes.append(SimpleEntityAttribute(attribute_label[1:], i))
                else:
                    self.attributes.append(IdentifierAttribute(attribute_label[1:], i))
            elif i == 0:
                self.attributes.append(IdentifierAttribute(attribute_label, i))
            else:
                self.attributes.append(SimpleEntityAttribute(attribute_label, i))
    
    def calculate_size(self, style):
        cartouche_font = font_metrics.FontMetrics(style["entity_cartouche_font"])
        self.get_cartouche_string_width = cartouche_font.get_pixel_width
        self.cartouche_height = cartouche_font.get_pixel_height()
        attribute_font = font_metrics.FontMetrics(style["entity_attribute_font"])
        self.attribute_height = attribute_font.get_pixel_height()
        for attribute in self.attributes:
            attribute.calculate_size(style)
        self.w = 2 * style["rect_margin_width"] + max([a.w for a in self.attributes] + [self.get_cartouche_string_width(self.cartouche)])
        self.h = len(self.attributes) * (self.attribute_height + style["line_skip_height"]) - style["line_skip_height"] + 4 * style["rect_margin_height"] + self.cartouche_height
        self.w += self.w % 2
        self.h += self.h % 2
        self.style = style

    def description(self):
        result = ["Entity %s" % self.name]
        result.extend([
            {
                "key": u"env",
                "env": [("x", """cx[u"%s"]""" % self.name), ("y", """cy[u"%s"]""" % self.name)],
            },
            {
                "key": u"begin",
                "id": u"entity-%s" % self.name,
            },
            {
                "key": u"begin",
                "id": u"frame-%s" % self.name,
            },
            {
                "key": u"stroke_depth",
                "stroke_depth": 0,
            },
            {
                "key": u"stroke_color",
                "stroke_color": "entity_cartouche_color",
            },
            {
                "key": u"color",
                "color": "entity_cartouche_color",
            },
            {
                "key": u"rect",
                "x": "%s+x" % (-self.w / 2),
                "y": "%s+y" % (-self.h / 2),
                "w": self.w,
                "h": self.cartouche_height + 2 * self.style["rect_margin_height"],
            },
            {
                "key": u"stroke_color",
                "stroke_color": "entity_color",
            },
            {
                "key": u"color",
                "color": "entity_color",
            },
            {
                "key": u"rect",
                "x": "%s+x" % (-self.w / 2),
                "y": "%s+y" % (-self.h / 2 + self.cartouche_height + 2 * self.style["rect_margin_height"]),
                "w": self.w,
                "h": self.h - self.cartouche_height - 2 * self.style["rect_margin_height"],
            },
            {
                "key": u"stroke_color",
                "stroke_color": "entity_stroke_color",
            },
            {
                "key": u"stroke_depth",
                "stroke_depth": self.style["box_stroke_depth"],
            },
            {
                "key": u"color",
                "color": "transparent_color",
            },
            {
                "key": u"rect",
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
                "y0": "%s+y" % (-self.h / 2 + self.cartouche_height + 2 * self.style["rect_margin_height"]),
                "x1": "%s+x" % (self.w / 2),
                "y1": "%s+y" % (-self.h / 2 + self.cartouche_height + 2 * self.style["rect_margin_height"]),
            },
            {
                "key": u"end",
            },
            {
                "key": u"text",
                "family": self.style["entity_cartouche_font"]["family"],
                "size": self.style["entity_cartouche_font"]["size"],
                "text": self.cartouche,
                "text_color": "entity_cartouche_text_color",
                "x": "%s+x" % (-self.get_cartouche_string_width(self.cartouche) / 2),
                "y": "%s+y" % (-self.h / 2 + self.style["rect_margin_height"] + self.style["cartouche_text_height_ratio"] * self.cartouche_height),
            },
        ])
        dx = self.style["rect_margin_width"] - self.w / 2
        dy = self.cartouche_height + 3 * self.style["rect_margin_height"] - self.h / 2
        for attribute in self.attributes:
            attribute.name = self.name
            result.extend(attribute.description(dx, dy))
            dy += self.attribute_height + self.style["line_skip_height"]
        result.extend([
            {
                "key": u"end",
            },
        ])
        return result
