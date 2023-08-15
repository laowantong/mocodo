from collections import defaultdict
from .attribute import *
from .tools.string_tools import rstrip_digit

class Entity:
    def __init__(self, clause):
        self.source = clause["source"]
        # A protected entity results in a table, even if all its columns are part of its primary key.
        self.is_protected = (clause.get("box_def_prefix") == "+") 
        self.name = clause["name"]
        self.name_view = rstrip_digit(self.name)
        self.attributes = clause.get("attrs", [])
        self.legs = []  # iterating over box's legs does nothing if it is not an association
        self.kind = "entity"
        self.has_alt_identifier = False

    def add_attributes(self, legs_to_strengthen, is_child=False):
        weak_entity = bool(legs_to_strengthen)
        self.strengthening_legs = legs_to_strengthen
        for (i, a) in enumerate(self.attributes):
            id_mark = a.get("id_mark","")
            explicit_underscore = "0" in a.get("id_groups", "") or a.get("id_groups", "") == ""
            if a.get("attribute_label", "") == "":
                self.attributes[i] = PhantomAttribute(a)
            elif is_child:
                self.attributes[i] = SimpleEntityAttribute(a)
            elif i == 0 and id_mark != "_":
                self.attributes[i] = WeakAttribute(a) if  weak_entity else StrongAttribute(a)
            elif i == 0 and id_mark == "_" and not explicit_underscore:
                self.attributes[i] = WeakAttribute(a) if  weak_entity else StrongAttribute(a)
            elif i != 0 and id_mark == "_" and explicit_underscore:
                self.attributes[i] = WeakAttribute(a) if  weak_entity else StrongAttribute(a)
            else:
                self.attributes[i] = SimpleEntityAttribute(a)
        
        self.candidates = defaultdict(set)
        for a in self.attributes:
            for id_group in a.id_groups:
                self.candidates[id_group].add(a.label)
        self.candidates = dict(self.candidates)
        if len(self.candidates) > 1:
            self.has_alt_identifier = True
        

    def register_boxes(self, boxes):
        self.boxes = boxes
    
    def set_left_gutter_visibility(self, is_visible):
        self.show_left_gutter = is_visible
    
    def calculate_size(self, style, get_font_metrics):
        cartouche_font = get_font_metrics(style["entity_cartouche_font"])
        self.get_cartouche_string_width = cartouche_font.get_pixel_width
        self.cartouche_height = cartouche_font.get_pixel_height()
        attribute_font = get_font_metrics(style["entity_attribute_font"])
        self.attribute_height = attribute_font.get_pixel_height()
        for attribute in self.attributes:
            attribute.calculate_size(style, get_font_metrics)
        cartouche_and_attribute_widths = []
        cartouche_and_attribute_widths.append(self.get_cartouche_string_width(self.name_view))
        cartouche_and_attribute_widths.extend(a.w for a in self.attributes)
        self.left_gutter_width = 0
        if self.show_left_gutter:
            self.left_gutter_width = 2 * style["rect_margin_width"]
            self.left_gutter_width += max(attribute.id_width for attribute in self.attributes)
        self.w = 2 * style["rect_margin_width"] + self.left_gutter_width + max(cartouche_and_attribute_widths)
        self.h = (
            len(self.attributes) * (self.attribute_height + style["line_skip_height"])
            - style["line_skip_height"]
            + 4 * style["rect_margin_height"]
            + self.cartouche_height
        )
        self.w += self.w % 2
        self.h += self.h % 2
        for attribute in self.attributes:
            attribute.set_left_gutter_width(self.left_gutter_width)

    def register_center(self, geo):
        self.cx = geo["cx"][self.name]
        self.cy = geo["cy"][self.name]
        self.l = self.cx - self.w // 2
        self.r = self.cx + self.w // 2
        self.t = self.cy - self.h // 2
        self.b = self.cy + self.h // 2

    def description(self, style, geo):
        result = []
        result.append(("comment", {"text": f"Entity {self.name}"}))
        result.append(
            (
                "begin_component",
                {
                    "page": self.page,
                    "visibility": "hidden" if self.page else "visible",
                }
            )
        )
        result.append(("begin_group", {}))
        result.append(
            (
                "rect",
                { # upper part background
                    "x": self.l,
                    "y": self.t,
                    "w": self.w,
                    "h": self.cartouche_height + 2 * style["rect_margin_height"],
                    "color": style["entity_cartouche_color"],
                    "stroke_color": "none",
                    "stroke_depth": 0,
                    "opacity": 1,
                },
            )
        )
        result.append(
            ( # lower part background (with or without a margin for the left gutter)
                "rect",
                { 
                    "x": self.l + self.left_gutter_width,
                    "y": self.t + self.cartouche_height + 2 * style["rect_margin_height"],
                    "w": self.w - self.left_gutter_width,
                    "h": self.h - self.cartouche_height - 2 * style["rect_margin_height"],
                    "color": style["entity_color"],
                    "stroke_color": "none",
                    "stroke_depth": 0,
                    "opacity": 1,
                },
            )
        )
        if self.show_left_gutter:
            result.append(
                ( # left_gutter background
                    "rect",
                    {
                        "x": self.l,
                        "y": self.t + self.cartouche_height + 2 * style["rect_margin_height"],
                        "w": self.left_gutter_width,
                        "h": self.h - self.cartouche_height - 2 * style["rect_margin_height"],
                        "color": style["left_gutter_color"],
                        "stroke_color": "none",
                        "stroke_depth": 0,
                        "opacity": 1,
                    },
                )
            )
            result.append(
                ( # line at the right of the left gutter
                    "line",
                    {
                        "x0": self.l + self.left_gutter_width,
                        "y0": self.t + self.cartouche_height + 2 * style["rect_margin_height"],
                        "x1": self.l + self.left_gutter_width,
                        "y1": self.b,
                        "stroke_color": style["entity_stroke_color"],
                        "stroke_depth": style["inner_stroke_depth"] / 4,
                    },
                )
            )
        result.append(
            ( # outer frame
                "rect",
                {
                    "x": self.l,
                    "y": self.t,
                    "w": self.w,
                    "h": self.h,
                    "color": style["transparent_color"],
                    "stroke_color": style["entity_stroke_color"],
                    "stroke_depth": style["box_stroke_depth"],
                    "opacity": 1,
                },
            )
        )
        result.append(
            ( # line between upper and lower part
                "line",
                {
                    "x0": self.l,
                    "y0": self.t + self.cartouche_height + 2 * style["rect_margin_height"],
                    "x1": self.r,
                    "y1": self.t + self.cartouche_height + 2 * style["rect_margin_height"],
                    "stroke_color": style["entity_stroke_color"],
                    "stroke_depth": style["inner_stroke_depth"],
                },
            )
        )
        result.append(("end", {}))
        result.append(
            ( # cartouche text
                "text",
                {
                    "x": self.cx - self.get_cartouche_string_width(self.name_view) // 2,
                    "y": self.t + style["rect_margin_height"] + style["cartouche_text_height_ratio"] * self.cartouche_height,
                    "text_color": style["entity_cartouche_text_color"],
                    "family": style["entity_cartouche_font"]["family"],
                    "size": style["entity_cartouche_font"]["size"],
                    "text": self.name_view,
                },
            )
        )
        x = self.cx - self.w // 2 + style["rect_margin_width"]
        dx = self.left_gutter_width
        dy = self.cartouche_height + 3 * style["rect_margin_height"] - self.h // 2
        for attribute in self.attributes:
            attribute.name = self.name
            result.extend(attribute.description(style, x, self.cy, dx, dy))
            dy += self.attribute_height + style["line_skip_height"]
        result.append(("end", {}))
        return result
