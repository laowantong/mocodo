#!/usr/bin/env python
# encoding: utf-8

import font_metrics

import re

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

    def calculate_size(self, style):
        self.attribute_font = style[self.font_type]
        font = font_metrics.FontMetrics(self.attribute_font)
        self.w = font.get_pixel_width(self.label)
        self.h = font.get_pixel_height()
        self.style = style

    def description(self, dx, dy):
        return [
            {
                "key": u"text",
                "text": self.label,
                "text_color": self.box_type + "_attribute_text_color",
                "x": "%s+x" % (dx),
                "y": "%s+y" % (dy + self.style["attribute_text_height_ratio"] * self.h),
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
                "key": u"stroke_depth",
                "stroke_depth": self.style["underline_depth"],
            },
            {
                "key": u"stroke_color",
                "stroke_color": "entity_attribute_text_color",
            },
            {
                "key": u"line",
                "x0": "%s+x" % (dx),
                "y0": "%s+y" % (dy + self.h + self.style["underline_skip_height"]),
                "x1": "%s+x" % (dx + self.w),
                "y1": "%s+y" % (dy + self.h + self.style["underline_skip_height"]),
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
                "key": u"stroke_depth",
                "stroke_depth": self.style["underline_depth"],
            },
            {
                "key": u"stroke_color",
                "stroke_color": "entity_attribute_text_color",
            },
            {
                "key": u"dash_line",
                "x0": "%s+x" % (dx),
                "x1": "%s+x" % (dx + self.w),
                "y": "%s+y" % (dy + self.h + self.style["underline_skip_height"]),
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
