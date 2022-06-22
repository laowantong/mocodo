import re
from math import sqrt

from .attribute import *
from .leg import *
from .mocodo_error import MocodoError

TRIANGLE_ALTITUDE = sqrt(3) / 2
INCIRCLE_RADIUS = 1 / sqrt(12)

class Association:

    def __init__(self, clause, **params):
        def clean_up_name(name):
            name = name.strip()
            is_inheritance = False
            if name[:1] + name[-1:] == "/\\":
                name = name[1:-1]
                is_inheritance = True
            name = name.replace("\\", "")
            cartouche = (name[:-1] if name[-1:].isdigit() else name)
            return (name, cartouche, is_inheritance)
        
        def clean_up_legs_and_attributes(
            legs_and_attributes,
            match_leg = re.compile(r"((?:_11|..)[<>]?\s+(?:\[.+?\]\s+)?)(.+)").match,
        ):
            (legs, attributes) = (legs_and_attributes.split(":", 1) + [""])[:2]
            (cards, entity_names) = ([], [])
            for leg in legs.split(","):
                leg = leg.strip().replace("\\", "")
                m = match_leg(leg)
                if m:
                    cards.append(m[1])
                    entity_names.append(m[2].lstrip())
                elif leg:
                    raise MocodoError(2, _(f'Missing cardinalities on leg "{leg}" of association "{self.name}".'))
                else:
                    raise MocodoError(11, _(f'Missing leg in association "{self.name}".'))
            return (cards, entity_names, outer_split(attributes))

        
        self.clause = clause
        match = re.match(r"\s*(/\w*\\)", clause)
        if match: # If the clause startswith an inheritance symbol, start to "normalize" its syntax:
            # e.g. change "/XT\ parent => child1, child2" into "/XT\, => parent, child1, child2"
            (clause, n) = re.subn(r"(\s*/\w*\\)\s*([^:,]+)\s*((?:<=|<-|->|=>)[<>]?)", r"\1, \3 \2, ", clause)
            if n == 0:
                raise MocodoError(14, _(f'Syntax error in inheritance "{match[1]}".'))
        (name, legs_and_attributes) = clause.split(",", 1)
        (self.name, self.cartouche, is_inheritance) = clean_up_name(name)
        if is_inheritance: # Finish syntax normalization by prefixing children names with fake cardinalities
            # e.g. change "/XT\, => parent, child1, child2" into "/XT\, => parent, XX child1, XX child2"
            legs_and_attributes = re.sub(r",\s*", ", XX ", legs_and_attributes)
        (cards, entity_names, attributes) = clean_up_legs_and_attributes(legs_and_attributes)
        self.attributes = [SimpleAssociationAttribute(attribute, i) for (i, attribute) in enumerate(attributes)]
        self.df_label = params.get("df", "DF")
        if self.cartouche == self.df_label:
            self.kind = "df"
        elif is_inheritance:
            if cards[0][2:3] in "<>":
                self.prettify_inheritance = False
            else:
                self.prettify_inheritance = True
                if cards[0][1] == ">":
                    for i in range(1, len(cards)):
                        cards[i] = cards[i][:2] + ">" + cards[i][2:]
                elif cards[0][0] == "<":
                    cards[0] = cards[0][:2] + ">" + cards[0][2:]
            self.kind = f"inheritance: {cards[0][:2]}"
        elif any(name.startswith("/") for name in entity_names):
            self.kind = "cluster"
        else:
            self.kind = "association"
        self.set_view_strategies()
        self.legs = []
        for (i, (card, name)) in enumerate(zip(cards, entity_names)):
            leg = Leg(self, card, name, **params)
            mutiplicity = entity_names.count(name)
            rank = entity_names[:i].count(name)
            leg.set_spin_strategy(0 if mutiplicity == 1 else 2 * rank / (mutiplicity - 1) - 1)
            self.legs.append(leg)


    def register_boxes(self, boxes):
        self.boxes = boxes

    def calculate_size(self, style, get_font_metrics):
        cartouche_font = get_font_metrics(style["association_cartouche_font"])
        self.get_cartouche_string_width = cartouche_font.get_pixel_width
        self.cartouche_height = cartouche_font.get_pixel_height()
        attribute_font = get_font_metrics(style["association_attribute_font"])
        self.attribute_height = attribute_font.get_pixel_height()
        self.calculate_size_depending_on_df(style, get_font_metrics)
        self.w += self.w % 2
        self.h += self.h % 2
        for leg in self.legs:
            leg.calculate_size(style, get_font_metrics)

    def register_center(self, geo):
        self.cx = geo["cx"][self.name]
        self.cy = geo["cy"][self.name]

    def set_view_strategies(self):

        def calculate_size_when_df(style, get_font_metrics):
            self.w = self.h = max(
                style["round_rect_margin_width"] * 2 + self.get_cartouche_string_width(self.df_label),
                style["round_rect_margin_width"] * 2 + self.cartouche_height
            )

        def calculate_size_when_inheritance(style, get_font_metrics):
            self.w = self.h = max(
                style["round_rect_margin_width"] * 2 + self.cartouche_height * 2,
                style["round_rect_margin_width"] * 2 + self.cartouche_height * 2
            )

        def calculate_size_when_default(style, get_font_metrics):
            for attribute in self.attributes:
                attribute.calculate_size(style, get_font_metrics)
            cartouche_and_attribute_widths = [a.w for a in self.attributes] + [self.get_cartouche_string_width(self.cartouche)]
            self.w = 2 * style["round_rect_margin_width"] + max(cartouche_and_attribute_widths)
            self.h = max(1, len(self.attributes)) * (self.attribute_height + style["line_skip_height"]) \
                - style["line_skip_height"] \
                + 2 * style["rect_margin_height"] \
                + 2 * style["round_rect_margin_height"] \
                + self.cartouche_height
            self.w += self.w % 2
            self.h += self.h % 2

        def description_when_df(style):
            return [
                (
                    "circle",
                    {
                        "stroke_depth": style["box_stroke_depth"],
                        "stroke_color": style["association_stroke_color"],
                        "color": style["association_cartouche_color"],
                        "cx": self.cx,
                        "cy": self.cy,
                        "r": self.w // 2,
                    },
                ),
                (
                    "text",
                    {
                        "text": self.df_label,
                        "text_color": style['association_cartouche_text_color'],
                        "x": self.cx + style["round_rect_margin_width"] - self.w // 2,
                        "y": self.cy + round(style["round_rect_margin_height"] - self.h / 2 + style["df_text_height_ratio"] * self.cartouche_height, 1),
                        "family": style["association_cartouche_font"]["family"],
                        "size": style["association_cartouche_font"]["size"],
                    },
                )
            ]

        def description_when_inheritance(style):
            return [
                (
                    "triangle",
                    {
                        "stroke_depth": style["box_stroke_depth"],
                        "stroke_color": style['association_stroke_color'],
                        "color": style['association_cartouche_color'],
                        "x1": self.cx,
                        "x2": self.cx - self.w // 2,
                        "x3": self.cx + self.w // 2,
                        "y1": self.cy - (TRIANGLE_ALTITUDE - INCIRCLE_RADIUS) * self.w,
                        "y2": self.cy + INCIRCLE_RADIUS * self.w,
                        "y3": self.cy + INCIRCLE_RADIUS * self.w,
                    },
                ),
                (
                    "text",
                    {
                        "text": self.cartouche,
                        "text_color": style['association_cartouche_text_color'],
                        "x": self.cx - self.get_cartouche_string_width(self.cartouche) // 2,
                        "y": self.cy + self.cartouche_height // 3,
                        "family": style["association_cartouche_font"]["family"],
                        "size": style["association_cartouche_font"]["size"],
                    },
                ),
            ]

        def description_when_default(style):
            result = []
            if self.kind == "cluster":
                clustered_boxes = [self] + [leg.entity for leg in self.legs if leg.kind == "cluster_leg"]
                x_min = min(b.cx - b.w // 2 for b in clustered_boxes)
                y_min = min(b.cy - b.h // 2 for b in clustered_boxes)
                x_max = max(b.cx + b.w // 2 for b in clustered_boxes)
                y_max = max(b.cy + b.h // 2 for b in clustered_boxes)
                x = x_min - style["card_margin"] // 2
                y = y_min - style["card_margin"] // 2
                w = x_max - x_min + style["card_margin"]
                h = y_max - y_min + style["card_margin"]
                for box in self.boxes:
                    if box.kind == "phantom":
                        continue
                    if box in clustered_boxes:
                        continue
                    if x_min <= box.cx <= x_max and y_min <= box.cy <= y_max:
                        break  # do not draw anything if this box is in the cluster
                else:
                    result.append(
                        (
                            "rect",
                            {
                                "x": x,
                                "y": y,
                                "w": w,
                                "h": h,
                                "stroke_color": None,
                                "stroke_depth": 0,
                                "color": style["entity_color"],
                                "opacity": 0.2,
                            },
                        )
                    )
                    result.append(
                        (
                            "dash_rect",
                            {
                                "x": x,
                                "y": y,
                                "w": w,
                                "h": h,
                                "stroke_color": style['entity_stroke_color'],
                                "stroke_depth": style["box_stroke_depth"] / 2,
                                "color": None,
                                "dash_width": style["dash_width"],
                            },
                        )
                    )
            x = self.cx - self.w // 2
            y = self.cy - self.h // 2
            w = self.w
            h = self.attribute_height + style["round_rect_margin_height"] + style["rect_margin_height"]
            r = style["round_corner_radius"]
            result.append(
                (
                    "upper_round_rect",
                    {
                        "x0": x + w - r,
                        "y0": y,
                        "y1": y + h,
                        "y2": y + r,
                        "w": w,
                        "r": r,
                        "color": style['association_cartouche_color'],
                        "stroke_color": style['association_cartouche_color'],
                        "stroke_depth": 0,
                    },
                )
            )
            y = self.cy + round(self.attribute_height + style["round_rect_margin_height"] + style["rect_margin_height"] - self.h / 2, 1)
            h = self.h - (self.attribute_height + style["round_rect_margin_height"] + style["rect_margin_height"])
            result.append(
                (
                    "lower_round_rect",
                    {
                        "x0": x + w,
                        "y0": y,
                        "y1": h - r,
                        "x1": x + r,
                        "w": w,
                        "r": r,
                        "color": style['association_color'],
                        "stroke_color": style['association_color'],
                        "stroke_depth": 0,
                    },
                )
            )
            result.append(
                (
                    "round_rect",
                    {
                        "x": self.cx - self.w // 2,
                        "y": self.cy - self.h // 2,
                        "w": self.w,
                        "h": self.h,
                        "radius": r,
                        "color": style['transparent_color'],
                        "stroke_color": style['association_stroke_color'],
                        "stroke_depth": style["box_stroke_depth"],
                    },
                )
            )
            result.append(
                (
                    "line",
                    {
                        "x0": self.cx - self.w // 2,
                        "y0": self.cy + self.attribute_height + style["round_rect_margin_height"] + style["rect_margin_height"] - self.h // 2,
                        "x1": self.cx + self.w // 2,
                        "y1": self.cy + self.attribute_height + style["round_rect_margin_height"] + style["rect_margin_height"] - self.h // 2,
                        "stroke_color": style['association_stroke_color'],
                        "stroke_depth": style["inner_stroke_depth"],
                    },
                )
            )
            result.append(
                (
                    "text",
                    {
                        "text": self.cartouche,
                        "text_color": style['association_cartouche_text_color'],
                        "x": self.cx - self.get_cartouche_string_width(self.cartouche) // 2,
                        "y": self.cy + round(-self.h / 2 + style["rect_margin_height"] + style["cartouche_text_height_ratio"] * self.cartouche_height, 1),
                        "family": style["association_cartouche_font"]["family"],
                        "size": style["association_cartouche_font"]["size"],
                    },
                ),
            )
            dx = style["round_rect_margin_width"] - self.w // 2
            dy = style["round_rect_margin_height"] + self.cartouche_height + 2 * style["rect_margin_height"] - self.h // 2
            for attribute in self.attributes:
                attribute.name = self.name
                result.extend(attribute.description(style, self.cx, self.cy, dx, dy))
                dy += self.attribute_height + style["line_skip_height"]
            return result

        if self.kind == "df":
            self.calculate_size_depending_on_df = calculate_size_when_df
            self.description_depending_on_df = description_when_df
        elif self.kind.startswith("inheritance"):
            self.calculate_size_depending_on_df = calculate_size_when_inheritance
            self.description_depending_on_df = description_when_inheritance
        else:
            self.calculate_size_depending_on_df = calculate_size_when_default
            self.description_depending_on_df = description_when_default

    def description(self, style, geo):
        result = []
        result.append(("comment", {"text": f"Association {self.name}"}))
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
        result.extend(self.description_depending_on_df(style))
        result.append(("end", {}))
        result.append(("end", {}))
        return result

    def leg_descriptions(self, style, geo):
        result = []
        for leg in self.legs:
            result.extend(leg.description(style, geo))
        return result
