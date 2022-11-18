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
            kind = "association"
            ends = name[:1] + name[-1:]
            if ends == "/\\":
                name = name[1:-1].replace(" ", "").upper().replace("TX", "XT")
                unnumbered_name = (name[:-1] if name[-1:].isdigit() else name)
                if unnumbered_name not in ("X", "T", "XT", ""):
                    raise MocodoError(24, _('Unknown specialization "{name}".').format(name=name)) # fmt: skip
                kind = "inheritance"
            elif ends == "[]":
                name = name[1:-1]
                kind = "forced_table"
            name = name.replace("\\", "")
            name_view = (name[:-1] if name[-1:].isdigit() else name)
            return (name, name_view, kind)
        
        def clean_up_legs_and_attributes(
            legs_and_attributes,
            match_leg = re.compile(r"((?:_11|/..|..)[<>]?\s+(?:\[.+?\]\s+)?)(.+)").match,
        ):
            (legs, attributes) = (legs_and_attributes.split(":", 1) + [""])[:2]
            (cards, entity_names) = ([], [])
            for leg in legs.split(","):
                leg = leg.strip().replace("\\", "")
                m = match_leg(leg)
                if m:
                    cards.append(m[1].strip())
                    entity_names.append(m[2].lstrip())
                elif leg:
                    raise MocodoError(2, _('Missing cardinalities on leg "{leg}" of association "{name}".').format(leg=leg, name=self.name)) # fmt: skip
                else:
                    raise MocodoError(11, _('Missing leg in association "{name}".').format(name=self.name)) # fmt: skip
            return (cards, entity_names, outer_split(attributes))

        
        self.clause = clause
        match = re.match(r"\s*(/\w*\\)", clause)
        if match: # If the clause starts with an inheritance symbol, start "normalizing" its syntax:
            # e.g. change "/XT\ parent => child1, child2" into "/XT\, => parent, child1, child2".
            (clause, n) = re.subn(
                r"(\s*/\w*\\)\s*([^:,]+)\s+(<=|<-|->|=>)([<=->]?)",
                r"\1, \3\4 \2, ",
                clause,
            )
            if n == 0:
                raise MocodoError(23, _('Syntax error in inheritance "{inheritance}".').format(inheritance=match[1])) # fmt: skip
        (name, legs_and_attributes) = clause.split(",", 1)
        (self.name, self.name_view, kind) = clean_up_name(name)
        if kind == "inheritance": # Finish syntax normalization by prefixing children names with fake cardinalities
            # e.g. change "/XT\, => parent, child1, child2" into "/XT\, => parent, XX child1, XX child2"
            legs_and_attributes = re.sub(r",\s*", ", XX ", legs_and_attributes)
        (cards, entity_names, attributes) = clean_up_legs_and_attributes(legs_and_attributes)
        self.attributes = [SimpleAssociationAttribute(attribute, i) for (i, attribute) in enumerate(attributes)]
        self.df_label = params.get("df", "DF")
        if self.name_view == self.df_label:
            self.kind = "df"
        elif kind == "inheritance":
            if cards[0][2:3] == cards[0][1]: # the last symbol of the arrow is repeated
                cards[0] = cards[0][:2] + ">" # replace it by the "standard" arrow
                self.prettify_inheritance = False
            else:
                self.prettify_inheritance = True
                if cards[0][1] == ">":
                    for i in range(1, len(cards)):
                        cards[i] = cards[i][:2] + ">" + cards[i][2:]
                elif cards[0][0] == "<":
                    cards[0] = cards[0][:2] + ">" + cards[0][2:]
            self.kind = f"inheritance: {cards[0][:2]}"
        elif kind == "forced_table":
            self.kind = kind
        else:
            candidate_peg_count = sum(card.startswith("/") for card in cards)
            valid_peg_count = sum(card in ("/0N", "/1N") for card in cards)
            if candidate_peg_count > valid_peg_count:
                raise MocodoError(26, _('Only cardinalities "/0N" or "/1N" are permitted to start with a "/" character.').format(name=self.name)) # fmt: skip
            if valid_peg_count > 0:
                valid_leg_count = sum(card in ("0N", "1N") for card in cards)
                if valid_leg_count < 1:
                    raise MocodoError(27, _('To become a cluster, association "{name}" must have at least one cardinality "0N" or "1N" (without "/").').format(name=self.name)) # fmt: skip
                if valid_leg_count + valid_peg_count < len(cards):
                    raise MocodoError(28, _('''To become a cluster, association "{name}"'s cardinalities must all be "0N", "1N", "/0N" or "/1N".''').format(name=self.name)) # fmt: skip
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
        self.calculate_size_depending_on_kind(style, get_font_metrics)
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
            cartouche_and_attribute_widths = [a.w for a in self.attributes] + [self.get_cartouche_string_width(self.name_view)]
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
                        "x": self.l + style["round_rect_margin_width"],
                        "y": self.t + style["round_rect_margin_height"] + style["df_text_height_ratio"] * self.cartouche_height,
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
        
        def optional_description_for_cluster(style):
            clustered_entities = [leg.entity for leg in self.legs if leg.kind == "cluster_leg"]
            if len(clustered_entities) == 2:
                (e1, e2) = clustered_entities
            elif len(clustered_entities) == 1:
                e1 = e2 = clustered_entities[0]
            else:
                return []

            x_min = min(box.l for box in (self, e1, e2))
            y_min = min(box.t for box in (self, e1, e2))
            x_max = max(box.r for box in (self, e1, e2))
            y_max = max(box.b for box in (self, e1, e2))
            x = x_min - style["card_margin"] // 2
            y = y_min - style["card_margin"] // 2
            w = x_max - x_min + style["card_margin"]
            h = y_max - y_min + style["card_margin"]

            x1_min = min(box.l for box in (self, e1))
            y1_min = min(box.t for box in (self, e1))
            x1_max = max(box.r for box in (self, e1))
            y1_max = max(box.b for box in (self, e1))
            x1 = x1_min - style["card_margin"] // 2
            y1 = y1_min - style["card_margin"] // 2
            w1 = x1_max - x1_min + style["card_margin"]
            h1 = y1_max - y1_min + style["card_margin"]
            
            x2_min = min(box.l for box in (self, e2))
            y2_min = min(box.t for box in (self, e2))
            x2_max = max(box.r for box in (self, e2))
            y2_max = max(box.b for box in (self, e2))
            x2 = x2_min - style["card_margin"] // 2
            y2 = y2_min - style["card_margin"] // 2
            w2 = x2_max - x2_min + style["card_margin"]
            h2 = y2_max - y2_min + style["card_margin"]

            e1_same_row = e1.t <= self.t < self.b <= e1.b or self.t <= e1.t < e1.b <= self.b
            e2_same_row = e2.t <= self.t < self.b <= e2.b or self.t <= e2.t < e2.b <= self.b
            e1_same_col = e1.l <= self.l < self.r <= e1.r or self.l <= e1.l < e1.r <= self.r
            e2_same_col = e2.l <= self.l < self.r <= e2.r or self.l <= e2.l < e2.r <= self.r
            if e1_same_row and e2_same_row or e1_same_col and e2_same_col:
                points = (x, y, x+w, y, x+w, y+h, x, y+h)
            elif e1_same_row and e2_same_col:
                if e1.cx < self.cx:
                    if e2.cy < self.cy:
                        #   2
                        # 1 a
                        points = (x, y1, x2, y1, x2, y, x+w, y, x+w, y+h, x, y+h)
                    else:
                        # 1 a
                        #   2
                        points = (x, y, x+w, y, x+w, y+h, x2, y+h, x2, y1+h1, x, y1+h1)
                else:
                    if e2.cy < self.cy:
                        # 2
                        # a 1
                        points = (x, y, x2+w2, y, x2+w2, y1, x+w, y1, x+w, y+h, x, y+h)
                    else:
                        # a 1
                        # 2
                        points = (x, y, x+w, y, x+w, y1+h1, x2+w2, y1+h1, x2+w2, y+h, x, y+h)
            elif e2_same_row and e1_same_col:
                if e2.cx < self.cx:
                    if e1.cy < self.cy:
                        #   1
                        # 2 a
                        points = (x, y2, x1, y2, x1, y, x+w, y, x+w, y+h, x, y+h)
                    else:
                        # 2 a
                        #   1
                        points = (x, y, x+w, y, x+w, y+h, x1, y+h, x1, y2+h2, x, y2+h2)
                else:
                    if e1.cy < self.cy:
                        # 1
                        # a 2
                        points = (x, y, x1+w1, y, x1+w1, y2, x+w, y2, x+w, y+h, x, y+h)
                    else:
                        # a 2
                        # 1
                        points = (x, y, x+w, y, x+w, y2+h2, x1+w1, y2+h2, x1+w1, y+h, x, y+h)
            else:
                return []
            points = ",".join(map(str, points))
            return [
                (
                    "polygon",
                    {
                        "points": points,
                        "stroke_color": None,
                        "stroke_depth": 0,
                        "color": style["entity_color"],
                        "opacity": 0.2,
                    },
                ),
                (
                    "dot_polygon",
                    {
                        "points": points,
                        "stroke_color": style['entity_stroke_color'],
                        "stroke_depth": style["box_stroke_depth"],
                        "color": None,
                        "dash_gap": style["dash_width"],
                    },
                )
            ]

        def description_when_default(style):
            result = []
            result.extend(optional_description_for_cluster(style))
            x = self.l
            y = self.t
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
            y = self.t + self.attribute_height + style["round_rect_margin_height"] + style["rect_margin_height"]
            h = self.h - self.attribute_height - style["round_rect_margin_height"] - style["rect_margin_height"]
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
                        "x": self.l,
                        "y": self.t,
                        "w": self.w,
                        "h": self.h,
                        "radius": r,
                        "color": style['transparent_color'],
                        "stroke_color": style['association_stroke_color'],
                        "stroke_depth": style["box_stroke_depth"],
                    },
                )
            )
            if self.kind == "forced_table":
                result.append(
                    (
                        "dash_rect",
                        {
                            "x": self.l - 2 * style["box_stroke_depth"],
                            "y": self.t - 2 * style["box_stroke_depth"],
                            "w": self.w + 4 * style["box_stroke_depth"],
                            "h": self.h + 4 * style["box_stroke_depth"],
                            "color": style['transparent_color'],
                            "stroke_color": style['entity_stroke_color'],
                            "stroke_depth": style["box_stroke_depth"],
                            "dash_width": style["dash_width"],
                        },
                    )
                )
            result.append(
                (
                    "line",
                    {
                        "x0": self.l,
                        "y0": self.t + self.attribute_height + style["round_rect_margin_height"] + style["rect_margin_height"],
                        "x1": self.r,
                        "y1": self.t + self.attribute_height + style["round_rect_margin_height"] + style["rect_margin_height"],
                        "stroke_color": style['association_stroke_color'],
                        "stroke_depth": style["inner_stroke_depth"],
                    },
                )
            )
            result.append(
                (
                    "text",
                    {
                        "text": self.name_view,
                        "text_color": style['association_cartouche_text_color'],
                        "x": self.cx - self.get_cartouche_string_width(self.name_view) // 2,
                        "y": self.t + style["rect_margin_height"] + style["cartouche_text_height_ratio"] * self.cartouche_height,
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
            self.calculate_size_depending_on_kind = calculate_size_when_df
            self.description_depending_on_kind = description_when_df
        elif self.kind.startswith("inheritance"):
            self.calculate_size_depending_on_kind = calculate_size_when_inheritance
            self.description_depending_on_kind = description_when_inheritance
        else:
            self.calculate_size_depending_on_kind = calculate_size_when_default
            self.description_depending_on_kind = description_when_default

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
        result.extend(self.description_depending_on_kind(style))
        result.append(("end", {}))
        result.append(("end", {}))
        return result

    def leg_descriptions(self, style, geo):
        result = []
        for leg in self.legs:
            result.extend(leg.description(style, geo))
        return result
