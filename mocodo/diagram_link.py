#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import sys
import re
from .dynamic import Dynamic
from .mocodo_error import MocodoError

class DiagramLink:

    def __init__(self, entities, foreign_entity, foreign_key):
        self.foreign_entity = foreign_entity
        self.foreign_key = foreign_key
        try:
            self.primary_entity = entities[foreign_key.primary_entity_name]
        except KeyError:
            raise MocodoError(14, _('Attribute "{foreign_key}" in entity "{foreign_entity}" references an unknown entity "{primary_entity}".').format(foreign_key=foreign_key.label, foreign_entity=foreign_entity.name, primary_entity=foreign_key.primary_entity_name))
        for candidate in self.primary_entity.attributes:
            if candidate.label.lstrip("#") == foreign_key.primary_key_label.lstrip("#"):
                self.primary_key = candidate
                break
        else:
            raise MocodoError(15, _('Attribute "{foreign_key}" in entity "{foreign_entity}" references an unknown attribute "{primary_key}" in entity "{primary_entity}".').format(foreign_key.label, foreign_entity.name, foreign_key.primary_key_label, foreign_key.primary_entity_name))
    
    def calculate_size(self, style, *ignored):
        self.fdx = self.foreign_entity.w // 2
        self.pdx = self.primary_entity.w // 2
        self.fdy = - self.foreign_entity.h / 2 + 3 * style["rect_margin_height"] + self.foreign_entity.cartouche_height + (self.foreign_key.rank + 0.5) * (self.foreign_entity.attribute_height + style["line_skip_height"])
        self.pdy = - self.primary_entity.h / 2 + 3 * style["rect_margin_height"] + self.primary_entity.cartouche_height + (self.primary_key.rank + 0.5) * (self.primary_entity.attribute_height + style["line_skip_height"])
        self.style = style
        self.offset = 2 * (style["card_margin"] + style["card_max_width"])
    
    def description(self):
        result = []
        result.append({
                "key": "stroke_color",
                "stroke_color": Dynamic("colors['leg_stroke_color']"),
            })
        result.append({
                "key": "stroke_depth",
                "stroke_depth": self.style["leg_stroke_depth"],
            })
        spins = [(-1, -1), (1, -1), (-1, 1), (1, 1)] if self.foreign_key.rank % 2 else [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        result.append({
                "key": "env",
                "env": [
                    ("fs,ps", """min(%s, key=lambda fs_ps: abs(cx[u"%s"]+%s*fs_ps[0] - cx[u"%s"]-%s*fs_ps[1]))""" % (spins, self.foreign_entity.name, self.fdx, self.primary_entity.name, self.pdx)),
                ],
            })
        result.append({
                "key": "env",
                "env": [
                    ("xf", """cx[u"%s"]+%s*fs""" % (self.foreign_entity.name, self.fdx)),
                    ("yf", """cy[u"%s"]+%s""" % (self.foreign_entity.name, self.fdy)),
                    ("xp", """cx[u"%s"]+%s*ps""" % (self.primary_entity.name, self.pdx)),
                    ("yp", """cy[u"%s"]+%s""" % (self.primary_entity.name, self.pdy)),
                ],
            })
        result.append({
                "key": "curve",
                "x0": Dynamic("xf"),
                "y0": Dynamic("yf"),
                "x1": Dynamic("xf+(xp-xf)/2 if fs != ps else xf+%s*fs" % self.offset),
                "y1": Dynamic("yf+(yp-yf)/2"),
                "x2": Dynamic("xf+(xp-xf)/3 if fs != ps else xp+%s*ps" % self.offset),
                "y2": Dynamic("yp"),
                "x3": Dynamic("xp"),
                "y3": Dynamic("yp"),
            })
        result.append({
                "key": "color",
                "color": Dynamic("colors['leg_stroke_color']"),
            })
        result.append({
                "key": "arrow",
                "x": Dynamic("xp"),
                "y": Dynamic("yp"),
                "a": Dynamic("ps"),
                "b": 0,
            })
        result.append({
                "key": "stroke_depth",
                "stroke_depth": self.style["box_stroke_depth"],
            })
        result.append({
                "key": "circle",
                "cx": Dynamic("xf"),
                "cy": Dynamic("yf"),
                "r": self.style["box_stroke_depth"],
            })
        return result
