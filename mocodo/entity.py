from .attribute import *


class Entity:
    def __init__(self, clause):
        (name, attribute_labels) = clause.split(":", 1)
        self.name = name.strip().replace("\\", "")
        self.attribute_labels = outer_split(attribute_labels)
        self.name_view = self.name[:-1] if self.name[-1].isdigit() else self.name  # get rid of single digit suffix, if any
        self.legs = []  # iterating over box's legs does nothing if it is not an association
        self.kind = "entity"
        self.clause = clause

    def add_attributes(self, legs_to_strenghten, is_child=False):
        if is_child:
            IdentifierAttribute = SimpleEntityAttribute
        elif legs_to_strenghten:
            IdentifierAttribute = WeakAttribute
        else:
            IdentifierAttribute = StrongAttribute
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
        self.strengthening_legs = legs_to_strenghten

    def register_boxes(self, boxes):
        self.boxes = boxes
    
    def calculate_size(self, style, get_font_metrics):
        cartouche_font = get_font_metrics(style["entity_cartouche_font"])
        self.get_cartouche_string_width = cartouche_font.get_pixel_width
        self.cartouche_height = cartouche_font.get_pixel_height()
        attribute_font = get_font_metrics(style["entity_attribute_font"])
        self.attribute_height = attribute_font.get_pixel_height()
        for attribute in self.attributes:
            attribute.calculate_size(style, get_font_metrics)
        cartouche_and_attribute_widths = [self.get_cartouche_string_width(self.name_view)] + [
            a.w for a in self.attributes
        ]
        self.w = 2 * style["rect_margin_width"] + max(cartouche_and_attribute_widths)
        self.h = (
            len(self.attributes) * (self.attribute_height + style["line_skip_height"])
            - style["line_skip_height"]
            + 4 * style["rect_margin_height"]
            + self.cartouche_height
        )
        self.w += self.w % 2
        self.h += self.h % 2

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
                {
                    "x": self.l,
                    "y": self.t,
                    "w": self.w,
                    "h": self.cartouche_height + 2 * style["rect_margin_height"],
                    "color": style["entity_cartouche_color"],
                    "stroke_color": style["entity_cartouche_color"],
                    "stroke_depth": 0,
                    "opacity": 1,
                },
            )
        )
        result.append(
            (
                "rect",
                {
                    "x": self.l,
                    "y": self.t + self.cartouche_height + 2 * style["rect_margin_height"],
                    "w": self.w,
                    "h": self.h - self.cartouche_height - 2 * style["rect_margin_height"],
                    "stroke_color": style["entity_color"],
                    "color": style["entity_color"],
                    "stroke_depth": 0,
                    "opacity": 1,
                },
            )
        )
        result.append(
            (
                "rect",
                {
                    "x": self.l,
                    "y": self.t,
                    "w": self.w,
                    "h": self.h,
                    "stroke_color": style["entity_stroke_color"],
                    "color": style["transparent_color"],
                    "stroke_depth": style["box_stroke_depth"],
                    "opacity": 1,
                },
            )
        )
        result.append(
            (
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
            (
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
        dx = style["rect_margin_width"] - self.w // 2
        dy = self.cartouche_height + 3 * style["rect_margin_height"] - self.h // 2
        for attribute in self.attributes:
            attribute.name = self.name
            result.extend(attribute.description(style, self.cx, self.cy, dx, dy))
            dy += self.attribute_height + style["line_skip_height"]
        result.append(("end", {}))
        return result
