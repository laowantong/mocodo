from collections import defaultdict
from .attribute import *
from .tools.string_tools import rstrip_digit_or_underline, raw_to_bid

class Entity:
    def __init__(self, clause):
        self.source = clause["source"]
        self.raw_name = clause["name"]
        # A protected entity results in a table, even if all its columns are part of its primary key.
        self.is_protected = (clause.get("box_def_prefix") == "+")
        self.bid = raw_to_bid(self.raw_name)
        self.name_view = rstrip_digit_or_underline(self.raw_name)
        self.attributes = clause.get("attrs", [])
        self.legs = []  # iterating over box's legs does nothing if it is not an association
        self.kind = "entity"
        if clause.get("box_def_prefix") == "-":
            self.calculate_size = self.calculate_size_when_invisible
            self.description = lambda *ignored: []
            self.is_invisible = True
        else:
            self.calculate_size = self.calculate_size_when_visible
            self.description = self.description_when_visible
            self.is_invisible = False
        self.has_alt_identifier = False

    def add_attributes(self, legs_to_strengthen, is_child, fk_format):
        weak_entity = bool(legs_to_strengthen)
        self.strengthening_legs = legs_to_strengthen
        for (i, a) in enumerate(self.attributes):
            id_mark = a.get("id_mark","")
            explicit_underscore = "0" in a.get("id_groups", "") or a.get("id_groups", "") == ""
            if a.get("attribute_label", "") == "":
                attribute = PhantomAttribute(a)
            elif is_child:
                attribute = SimpleEntityAttribute(a)
            elif i == 0 and id_mark != "_":
                attribute = WeakAttribute(a) if  weak_entity else StrongAttribute(a)
            elif i == 0 and id_mark == "_" and not explicit_underscore:
                attribute = WeakAttribute(a) if  weak_entity else StrongAttribute(a)
            elif i != 0 and id_mark == "_" and explicit_underscore:
                attribute = WeakAttribute(a) if  weak_entity else StrongAttribute(a)
            else:
                attribute = SimpleEntityAttribute(a)
            attribute.register_foreign_key_status(a, fk_format)
            self.attributes[i] = attribute
        self.candidates = defaultdict(set)
        for a in self.attributes:
            for id_group in a.id_groups:
                self.candidates[id_group].add(a.label)
        self.candidates = dict(self.candidates)
        if len(self.candidates) > 1:
            self.has_alt_identifier = True
        
    def register_boxes(self, boxes):
        self.boxes = boxes
    
    def set_id_gutter_visibility(self, is_visible):
        self.show_id_gutter = is_visible
    
    def calculate_size_when_invisible(self, *ignored):
        self.w = 0
        self.h = 0
    
    def calculate_size_when_visible(self, style, get_font_metrics):
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
        self.id_gutter_width = 0
        if self.show_id_gutter:
            self.id_gutter_width = 2 * style["rect_margin_width"]
            if self.attributes:
                self.id_gutter_width += max(attribute.id_width for attribute in self.attributes)
        self.w = 2 * style["rect_margin_width"] + self.id_gutter_width + max(cartouche_and_attribute_widths)
        self.h = (
            len(self.attributes) * (self.attribute_height + style["line_skip_height"])
            - style["line_skip_height"]
            + 4 * style["rect_margin_height"]
            + self.cartouche_height
        )
        self.w += self.w % 2
        self.h += self.h % 2
        for attribute in self.attributes:
            attribute.set_id_gutter_width(self.id_gutter_width)

    def register_center(self, geo):
        self.cx = geo["cx"][self.bid]
        self.cy = geo["cy"][self.bid]
        self.l = self.cx - self.w // 2
        self.r = self.cx + self.w // 2
        self.t = self.cy - self.h // 2
        self.b = self.cy + self.h // 2

    def description_when_visible(self, style, geo):
        result = []
        result.append(("comment", {"text": f"Entity {self.bid}"}))
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
                    "x": self.l + self.id_gutter_width,
                    "y": self.t + self.cartouche_height + 2 * style["rect_margin_height"],
                    "w": self.w - self.id_gutter_width,
                    "h": self.h - self.cartouche_height - 2 * style["rect_margin_height"],
                    "color": style["entity_color"],
                    "stroke_color": "none",
                    "stroke_depth": 0,
                    "opacity": 1,
                },
            )
        )
        if self.show_id_gutter:
            result.append(
                ( # id_gutter background
                    "rect",
                    {
                        "x": self.l,
                        "y": self.t + self.cartouche_height + 2 * style["rect_margin_height"],
                        "w": self.id_gutter_width,
                        "h": self.h - self.cartouche_height - 2 * style["rect_margin_height"],
                        "color": style["id_gutter_color"],
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
                        "x0": self.l + self.id_gutter_width,
                        "y0": self.t + self.cartouche_height + 2 * style["rect_margin_height"],
                        "x1": self.l + self.id_gutter_width,
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
        dx = self.id_gutter_width
        dy = self.cartouche_height + 3 * style["rect_margin_height"] - self.h // 2
        for attribute in self.attributes:
            result.extend(attribute.description(style, x, self.cy, dx, dy))
            dy += self.attribute_height + style["line_skip_height"]
        result.append(("end", {}))
        return result
