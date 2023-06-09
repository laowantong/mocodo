import itertools

from .attribute import *
from .leg import ConstraintLeg

constraint_counter = itertools.count(1)

class Constraint:

    def __init__(self, clause):
        self.source = clause["source"]
        self.name_view = clause.get("name", "")
        self.name = f'{clause.get("name", "Anonymous")} constraint #{next(constraint_counter)}'
        self.note = clause.get("constraint_note")
        self.legs = []
        for target in clause.get("constraint_targets", []):
            self.legs.append(ConstraintLeg(self, target.get("constraint_leg", ""), target["box"]))
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
        if self.coords:
            # The center of a constraint is either at a certain ratio of the width and height of the
            # page, or aligned with the center of a box.
            if isinstance(self.coords[0], float):
                self.cx = self.coords[0] * geo["width"] // 100
            else:
                self.cx = geo["cx"][self.coords[0]]
            if isinstance(self.coords[1], float):
                self.cy = self.coords[1] * geo["height"] // 100
            else:
                self.cy = geo["cy"][self.coords[1]]
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
                "circle_with_note" if self.note else "circle",
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
