from math import sqrt

from .attribute import *
from .leg import *

TRIANGLE_ALTITUDE = sqrt(3) / 2
INCIRCLE_RADIUS = 1 / sqrt(12)

class Inheritance:

    def __init__(self, clause, **params):
        self.source = clause["source"]
        leg_entities = [leg["entity"] for leg in clause["legs"]]
        self.name = f'{clause["name"]} {clause["herit_arrow"]} {",".join(leg_entities)}'
        self.name_view = clause['name'][:-1] if clause['name'][-1:].isdigit() else clause['name']  # get rid of single digit suffix, if any
        self.attributes = [InheritanceAttribute(attr) for attr in clause.get("attrs", [])]
        for leg_clause in clause["legs"]:
            leg_clause["kind"] = "-"
            leg_clause["arrow"] = False
        herit_arrow = clause["herit_arrow"]
        if herit_arrow == "<-":
            clause["legs"][0]["arrow"] = True
        elif herit_arrow == "->":
            for leg_clause in clause["legs"][1:]:
                leg_clause["arrow"] = True
        elif herit_arrow == "<=":
            clause["legs"][0]["arrow"] = True
            for leg_clause in clause["legs"][1:]:
                leg_clause["kind"] = "="
        elif herit_arrow == "=>":
            clause["legs"][0]["kind"] = "="
            for leg_clause in clause["legs"][1:]:
                leg_clause["arrow"] = True
        else:
            clause["legs"][0]["arrow"] = True
        self.legs = [InheritanceLeg(self, leg, **params) for leg in clause["legs"]]
        self.kind = herit_arrow.replace("--", "-").replace("==", "=")

    def register_boxes(self, boxes):
        self.boxes = boxes

    def calculate_size(self, style, get_font_metrics):
        cartouche_font = get_font_metrics(style["association_cartouche_font"])
        self.get_cartouche_string_width = cartouche_font.get_pixel_width
        self.cartouche_height = cartouche_font.get_pixel_height()
        attribute_font = get_font_metrics(style["association_attribute_font"])
        self.attribute_height = attribute_font.get_pixel_height()
        self.w = self.h = max(
            style["round_rect_margin_width"] * 2 + self.cartouche_height * 2,
            style["round_rect_margin_width"] * 2 + self.cartouche_height * 2
        )
        self.w += self.w % 2
        self.h += self.h % 2
        for leg in self.legs:
            leg.calculate_size(style, get_font_metrics)

    def register_center(self, geo):
        self.cx = geo["cx"][self.name]
        self.cy = geo["cy"][self.name]
        self.l = self.cx - self.w // 2
        self.r = self.cx + self.w // 2
        self.t = self.cy - self.h // 2
        self.b = self.cy + self.h // 2

    def description(self, style, geo):
        result = []
        result.append(("comment", {"text": f"Inheritance {self.name}"}))
        result.append(
            (
                "begin_component",
                {
                    "page": self.page,
                    "visibility": "hidden" if self.page else "visible",
                }
            )
        )
        result.extend(self.leg_descriptions(style, geo))
        result.append(("begin_group", {}))
        result.extend(
            [
                (
                    "triangle",
                    {
                        "stroke_depth": style["box_stroke_depth"],
                        "stroke_color": style['association_stroke_color'],
                        "color": style['association_cartouche_color'],
                        "x1": self.cx,
                        "x2": self.l,
                        "x3": self.r,
                        "y1": self.cy - (TRIANGLE_ALTITUDE - INCIRCLE_RADIUS) * self.w,
                        "y2": self.cy + INCIRCLE_RADIUS * self.w,
                        "y3": self.cy + INCIRCLE_RADIUS * self.w,
                    },
                ),
                (
                    "text",
                    {
                        "text": self.name_view,
                        "text_color": style['association_cartouche_text_color'],
                        "x": self.cx - self.get_cartouche_string_width(self.name_view) // 2,
                        "y": self.cy + self.cartouche_height // 3,
                        "family": style["association_cartouche_font"]["family"],
                        "size": style["association_cartouche_font"]["size"],
                    },
                ),
            ]
        )
        result.append(("end", {}))
        result.append(("end", {}))
        return result

    def leg_descriptions(self, style, geo):
        result = []
        for leg in self.legs:
            result.extend(leg.description(style, geo))
        return result
