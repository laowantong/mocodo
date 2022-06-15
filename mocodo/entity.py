from .attribute import *


class Entity:
    def __init__(self, clause):
        def clean_up(name, attributes):
            name = name.strip().replace("\\", "")
            cartouche = name[:-1] if name[-1].isdigit() else name  # get rid of digit suffix, if any
            return (name, cartouche, outer_split(attributes))

        (self.name, self.attribute_labels) = clause.split(":", 1)
        (self.name, self.cartouche, self.attribute_labels) = clean_up(
            self.name, self.attribute_labels
        )
        self.legs = []  # iterating over box's legs does nothing if it is not an association
        self.kind = "entity"
        self.clause = clause

    def set_strengthen_legs(self, legs):
        self.strengthen_legs = legs
        IdentifierAttribute = WeakAttribute if legs else StrongAttribute
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

    def calculate_size(self, style, get_font_metrics):
        cartouche_font = get_font_metrics(style["entity_cartouche_font"])
        self.get_cartouche_string_width = cartouche_font.get_pixel_width
        self.cartouche_height = cartouche_font.get_pixel_height()
        attribute_font = get_font_metrics(style["entity_attribute_font"])
        self.attribute_height = attribute_font.get_pixel_height()
        for attribute in self.attributes:
            attribute.calculate_size(style, get_font_metrics)
        cartouche_and_attribute_widths = [self.get_cartouche_string_width(self.cartouche)] + [
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

    def description(self, style, geo):
        result = []
        self.cx = geo["cx"][self.name]
        self.cy = geo["cy"][self.name]
        result.append(("comment", {"comment": f"Entity {self.name}"}))
        result.append(("begin", {"id": f"entity-{self.name}"}))
        result.append(("begin", {"id": f"frame-{self.name}"}))
        result.append(
            (
                "rect",
                {
                    "x": self.cx - self.w // 2,
                    "y": self.cy - self.h // 2,
                    "w": self.w,
                    "h": self.cartouche_height + 2 * style["rect_margin_height"],
                    "color": style["entity_cartouche_color"],
                    "stroke_color": style["entity_cartouche_color"],
                    "stroke_depth": 0,
                },
            )
        )
        result.append(
            (
                "rect",
                {
                    "x": self.cx - self.w // 2,
                    "y": self.cy + round(-self.h / 2 + self.cartouche_height + 2 * style["rect_margin_height"], 1),
                    "w": self.w,
                    "h": self.h - self.cartouche_height - 2 * style["rect_margin_height"],
                    "stroke_color": style["entity_color"],
                    "color": style["entity_color"],
                    "stroke_depth": 0,
                },
            )
        )
        result.append(
            (
                "rect",
                {
                    "x": self.cx - self.w // 2,
                    "y": self.cy - self.h // 2,
                    "w": self.w,
                    "h": self.h,
                    "stroke_color": style["entity_stroke_color"],
                    "color": style["transparent_color"],
                    "stroke_depth": style["box_stroke_depth"],
                },
            )
        )
        result.append(
            (
                "line",
                {
                    "x0": self.cx - self.w // 2,
                    "y0": self.cy - self.h // 2 + self.cartouche_height + 2 * style["rect_margin_height"],
                    "x1": self.cx + self.w // 2,
                    "y1": self.cy - self.h // 2 + self.cartouche_height + 2 * style["rect_margin_height"],
                    "stroke_color": style["entity_stroke_color"],
                    "stroke_depth": style["inner_stroke_depth"],
                },
            )
        )
        result.append(("end", {"id": f"frame-{self.name}"}))
        result.append(
            (
                "text",
                {
                    "x": self.cx - self.get_cartouche_string_width(self.cartouche) // 2,
                    "y": self.cy + round(-self.h / 2 + style["rect_margin_height"] + style["cartouche_text_height_ratio"] * self.cartouche_height, 1),
                    "text_color": style["entity_cartouche_text_color"],
                    "family": style["entity_cartouche_font"]["family"],
                    "size": style["entity_cartouche_font"]["size"],
                    "text": self.cartouche,
                },
            )
        )
        dx = style["rect_margin_width"] - self.w // 2
        dy = self.cartouche_height + 3 * style["rect_margin_height"] - self.h // 2
        for attribute in self.attributes:
            attribute.name = self.name
            result.extend(attribute.description(style, self.cx, self.cy, dx, dy))
            dy += self.attribute_height + style["line_skip_height"]
        result.append(("end", {"id": f"entity-{self.name}"}))
        return result
