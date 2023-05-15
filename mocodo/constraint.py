import re

from .attribute import *
from .leg import ConstraintLeg
from .mocodo_error import MocodoError


class Constraint:

    def __init__(self, clause):
        (self.name, legs) = re.match(r"\s*\((.{0,3})\)(.+)", clause).groups() # already checked by the caller
        (legs, self.ratios) = re.match(r"^\s*(.*?)\s*(?::\s*(.+))?$", legs).groups()
        if self.ratios:
            try:
                self.ratios = [int(ratio) for ratio in self.ratios.split(",")]
            except ValueError:
                raise MocodoError(104, _('Malformed constraint ratios "{ratios}".').format(ratios=self.ratios))
            if len(self.ratios) == 1:
                self.ratios += self.ratios # if only one ratio is given, it is used for both width and height
            self.ratios = self.ratios[:2] # the subsequent ratios are ignored
        self.legs = []
        for leg in legs.split(","):
            leg = leg.strip()
            if not leg:
                continue
            try:
                kind_and_box_name = re.match(r"(<?[-.=]{1,2}>?|)\s*(.+)", leg).groups()
            except AttributeError:
                raise MocodoError(102, _('Malformed constraint leg "{leg}".').format(leg=leg))
            self.legs.append(ConstraintLeg(self, *kind_and_box_name))
        self.kind= "constraint"

    def register_boxes(self, boxes):
        self.boxes = boxes

    def calculate_size(self, style, get_font_metrics):
        constraint_font = get_font_metrics(style["constraint_font"])
        self.get_constraint_string_width = constraint_font.get_pixel_width
        self.constraint_height = constraint_font.get_pixel_height()
        if self.name.strip():
            size = max(self.get_constraint_string_width(self.name), self.constraint_height)
        else:
            size = self.get_constraint_string_width(self.name * 2)
        self.w = self.h = style["constraint_margin"] * 2 + size

    def register_center(self, geo):
        if self.ratios:
            # The center of a constraint is at a certain ratio of the width and height of the page
            self.cx = self.ratios[0] * geo["width"] // 100
            self.cy = self.ratios[1] * geo["height"] // 100
        else:
            # The center of a constraint is the barycenter of the centers of its boxes
            self.cx = sum(geo["cx"][leg.box_name] for leg in self.legs) / len(self.legs)
            self.cy = sum(geo["cy"][leg.box_name] for leg in self.legs) / len(self.legs)
        self.l = self.cx - self.w // 2
        self.r = self.cx + self.w // 2
        self.t = self.cy - self.h // 2
        self.b = self.cy + self.h // 2

    def _description(self, style):
        return [
            (
                "circle",
                {
                    "stroke_depth": style["constraint_stroke_depth"],
                    "stroke_color": style["association_stroke_color"],
                    "color": style["background_color"],
                    "cx": self.cx,
                    "cy": self.cy,
                    "r": self.w // 2,
                },
            ),
            (
                "text",
                {
                    "text": self.name,
                    "text_color": style['card_text_color'],
                    "x": self.cx - self.get_constraint_string_width(self.name) / 2,
                    "y": self.cy + self.constraint_height * 0.3, # TODO: suppress magic number
                    "family": style["constraint_font"]["family"],
                    "size": style["constraint_font"]["size"],
                },
            )
        ]

    def description(self, style, geo):
        result = []
        result.append(("comment", {"text": f"Constraint {self.name}"}))
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
        result.extend(self._description(style))
        result.append(("end", {}))
        result.append(("end", {}))
        return result

    def leg_descriptions(self, style, geo):
        result = []
        for leg in self.legs:
            result.extend(leg.description(style, geo))
        return result
