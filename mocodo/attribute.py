#!/usr/bin/env python
# encoding: utf-8

from __future__ import division


import re
from .dynamic import Dynamic

findall_outer_commas = re.compile(r'[^,]+\[.*?\][^,]*|[^,]+').findall


def outer_split(s):
    return [s.replace(", ", ",").strip(" \n\t") for s in findall_outer_commas(s.replace(",", ", "))]

search_label_and_type = re.compile(r"^(.*?)(?: *\[(.*)\])?$").search


class Attribute:

    def __init__(self, attribute, rank):
        (label, self.data_type) = search_label_and_type(attribute).groups()
        self.data_type = None if self.data_type is None else self.data_type.replace("<<<protected-comma>>>", ",").replace("<<<protected-colon>>>", ":")
        components = label.split("->")
        if len(components) == 3:
            (self.label, self.primary_entity_name, self.primary_key_label) = components
        else:
            (self.label, self.primary_entity_name, self.primary_key_label) = (label, None, None)
        self.box_type = "entity"
        self.font_type = "entity_attribute_font"
        self.rank = rank

    def calculate_size(self, style, get_font_metrics):
        self.attribute_font = style[self.font_type]
        font = get_font_metrics(self.attribute_font)
        self.w = font.get_pixel_width(self.label)
        self.h = font.get_pixel_height()
        self.style = style

    def description(self, dx, dy):
        return [
            {
                "key": "text",
                "text": self.label,
                "text_color": Dynamic("colors['%s']" % (self.box_type + "_attribute_text_color")),
                "x": Dynamic("%s+x" % (dx)),
                "y": Dynamic("%s+y" % round(dy + self.style["attribute_text_height_ratio"] * self.h, 1)),
                "family": self.attribute_font["family"],
                "size": self.attribute_font["size"],
            }
        ]


class SimpleEntityAttribute(Attribute):

    def __init__(self, attribute, rank):
        Attribute.__init__(self, attribute, rank)

    def get_category(self):
        return "simple"


class SimpleAssociationAttribute(Attribute):

    def __init__(self, attribute, rank):
        Attribute.__init__(self, attribute, rank)
        self.box_type = "association"
        self.font_type = "association_attribute_font"


class StrongAttribute(Attribute):

    def __init__(self, attribute, rank):
        Attribute.__init__(self, attribute, rank)

    def get_category(self):
        return "strong"

    def description(self, dx, dy):
        return Attribute.description(self, dx, dy) + [
            {
                "key": "stroke_depth",
                "stroke_depth": self.style["underline_depth"],
            },
            {
                "key": "stroke_color",
                "stroke_color": Dynamic("colors['entity_attribute_text_color']"),
            },
            {
                "key": "line",
                "x0": Dynamic("%s+x" % (dx)),
                "y0": Dynamic("%s+y" % (dy + self.h + self.style["underline_skip_height"])),
                "x1": Dynamic("%s+x" % (dx + self.w)),
                "y1": Dynamic("%s+y" % (dy + self.h + self.style["underline_skip_height"])),
            }
        ]


class WeakAttribute(Attribute):

    def __init__(self, attribute, rank):
        Attribute.__init__(self, attribute, rank)

    def get_category(self):
        return "weak"

    def description(self, dx, dy):
        return Attribute.description(self, dx, dy) + [
            {
                "key": "stroke_depth",
                "stroke_depth": self.style["underline_depth"],
            },
            {
                "key": "stroke_color",
                "stroke_color": Dynamic("colors['entity_attribute_text_color']"),
            },
            {
                "key": "dash_line",
                "x0": Dynamic("%s+x" % (dx)),
                "x1": Dynamic("%s+x" % (dx + self.w)),
                "y": Dynamic("%s+y" % (dy + self.h + self.style["underline_skip_height"])),
                "dash_width": self.style["dash_width"],
            }
        ]


class PhantomAttribute(Attribute):

    def __init__(self, rank):
        Attribute.__init__(self, "", rank)

    def get_category(self):
        return "phantom"

    def description(self, dx, dy):
        return []
