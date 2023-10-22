import re

from .attribute import *
from .leg import ConstraintLeg
from .tools.string_tools import is_a_description, raw_to_bid

class Constraint:

    counter = 0

    @classmethod
    def reset_counter(cls):
        cls.counter = 0

    def __init__(self, clause):
        self.source = clause["source"]
        self.raw_name = clause.get("name", "Anonymous")
        self.name_view = clause.get("name", "")
        Constraint.counter += 1
        self.bid = f'{raw_to_bid(self.raw_name)}_CONSTRAINT_#{Constraint.counter}'
        self.note = clause.get("constraint_note")
        self.legs = []
        for target in clause.get("constraint_targets", []):
            self.legs.append(ConstraintLeg(self, target.get("constraint_leg", ""), target["name"]))
        if self.legs:
            self.coords = clause.get("constraint_coords", [])
        else:
            # When there is neither coord nor target, the constraint is placed at the top right corner
            # which is obviously undesirable, forcing the user to specify at least one coord.
            self.coords = clause.get("constraint_coords", [0, 0])
        self.kind= "constraint"

    def register_boxes(self, boxes):
        self.boxes = boxes

    def calculate_size(self, style, get_font_metrics):
        constraint_font = get_font_metrics(style["constraint_font"])
        self.get_constraint_string_width = constraint_font.get_pixel_width
        self.constraint_height = constraint_font.get_pixel_height()
        if self.name_view.strip():
            size = max(self.get_constraint_string_width(self.name_view), self.constraint_height)
        else:
            size = self.get_constraint_string_width("W") * len(self.name_view)
        self.w = self.h = style["constraint_margin"] * 2 + size

    def register_center(self, geo):
        self.page_width = geo["width"]
        self.page_height = geo["height"]
        if self.coords:
            # The center of a constraint is either at a certain ratio of the width and height of the
            # page, or aligned with the center of a box.
            if isinstance(self.coords[0], (float, int)):
                self.cx = self.coords[0] * self.page_width // 100
            else:
                self.cx = geo["cx"][raw_to_bid(self.coords[0])]
            if isinstance(self.coords[1], (float, int)):
                self.cy = self.coords[1] * self.page_height // 100
            else:
                self.cy = geo["cy"][raw_to_bid(self.coords[1])]
        else:
            # The center of a constraint is the barycenter of the centers of its boxes
            self.cx = sum(geo["cx"][leg.bid] for leg in self.legs) / len(self.legs)
            self.cy = sum(geo["cy"][leg.bid] for leg in self.legs) / len(self.legs)
        self.l = self.cx - self.w // 2
        self.r = self.cx + self.w // 2
        self.t = self.cy - self.h // 2
        self.b = self.cy + self.h // 2

    def _description(self, style):
        return [
            (
                "circle_with_note" if is_a_description(self.note) else "circle",
                {
                    "stroke_depth": style["constraint_stroke_depth"],
                    "stroke_color": style["constraint_stroke_color"],
                    "color": style["constraint_background_color"],
                    "cx": self.cx,
                    "cy": self.cy,
                    "r": self.w // 2,
                    "note": self.note,
                },
            ),
            (
                "text_above_note",
                {
                    "text": self.name_view,
                    "text_color": style['constraint_text_color'],
                    "x": self.cx - self.get_constraint_string_width(self.name_view) / 2,
                    "y": self.cy + self.constraint_height * style["constraint_text_height_tweak"],
                    "family": style["card_font"]["family"],
                    "size": style["card_font"]["size"],
                },
            ),
        ]

    def description(self, style, geo):
        result = []
        result.append(("comment", {"text": f"Constraint {self.bid}"}))
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

    def invert_coords_horizontal_mirror(self):
        if self.coords and isinstance(self.coords[1], (float, int)):
            self.coords[1] = 100 - self.coords[1]
            self.source = re.sub(r"(.+):.+", fr"\1: {self.coords[0]}, {self.coords[1]}", self.source)
    
    def invert_coords_vertical_mirror(self):
        if self.coords and isinstance(self.coords[0], (float, int)):
            self.coords[0] = 100 - self.coords[0]
            self.source = re.sub(r"(.+):.+", fr"\1: {self.coords[0]}, {self.coords[1]}", self.source)
    
    def invert_coords_diagonal_mirror(self):
        if self.coords:
            (self.coords[0], self.coords[1]) = (self.coords[1], self.coords[0])
            self.source = re.sub(r"(.+):.+", fr"\1: {self.coords[0]}, {self.coords[1]}", self.source)
