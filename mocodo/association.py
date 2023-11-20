import re
from .attribute import *
from .leg import *
from .mocodo_error import MocodoError
from .tools.string_tools import rstrip_digit_or_underline, raw_to_bid

class Association:

    df_counter = 0

    @classmethod
    def reset_df_counter(cls):
        cls.df_counter = 0

    def __init__(self, clause, **params):
        self.source = clause["source"]
        self.raw_name = clause["name"]
        self.bid = raw_to_bid(self.raw_name)
        # A protected association results in a table, even if this association is a DF.
        self.is_protected = (clause.get("box_def_prefix") == "+")
        if clause.get("box_def_prefix") == "-":
            self.calculate_size = self.calculate_size_when_invisible
            self.description = lambda *ignored: []
            self.is_invisible = True
        else:
            self.calculate_size = self.calculate_size_when_visible
            self.description = self.description_when_visible
            self.is_invisible = False
        self.peg_count = 0
        self.attributes = []
        for attr in clause.get("attrs", []):
            if attr.get("attribute_label", "") == "":
                self.attributes.append(PhantomAttribute(attr))
            elif attr.get("id_mark", "") == "_":
                if params.get("no_assoc_ids"):
                    raise MocodoError(52, _('The association "{name}" cannot have an identifier.').format(name=self.raw_name))
                self.attributes.append(StrongAttribute(attr))
            else:
                self.attributes.append(SimpleAssociationAttribute(attr))
        df_label = params.get("df", "DF")
        if re.match(fr"^{df_label.upper()}\d*$", self.raw_name.upper()):
            self.name_view = df_label # strip all digits suffixing a DF name
            self.bid = f"{df_label}{Association.df_counter}"
            Association.df_counter += 1
            self.kind = "df"
        else:
            self.name_view = rstrip_digit_or_underline(self.raw_name)
            legs = clause["legs"]
            # A "peg" is a leg that is prefixed by a "/" character.
            for leg in legs:
                if leg.get("card_prefix") == "/":
                    self.peg_count += 1
            if self.peg_count > 0:
                if len(legs) < 3:
                    raise MocodoError(51, _('The association "{name}" should have at least 3 legs to become a cluster.').format(name=self.raw_name))
                self.kind = "cluster"
            else:
                self.kind = "association"
        self.set_view_strategies()
        entity_raw_names = [leg["entity"] for leg in clause["legs"]]
        self.legs = []
        for leg_clause in clause["legs"]:
            entity_raw_name = leg_clause["entity"]
            rank = leg_clause["rank"]
            leg = Leg(self, leg_clause, **params)
            mutiplicity = entity_raw_names.count(entity_raw_name)
            rank = entity_raw_names[:rank].count(entity_raw_name)
            leg.set_spin_strategy(0 if mutiplicity == 1 else 2 * rank / (mutiplicity - 1) - 1)
            self.legs.append(leg)
        if self.kind == "cluster":
            candidate_groups = iter([0] + list(range(self.peg_count - 1, 0, -1)))
            for leg in self.legs:
                if leg.kind == "cluster_peg":
                    group_number = str(next(candidate_groups))
                    for other_leg in self.legs:
                        if other_leg is leg:
                            continue
                        other_leg.append_candidate_group(group_number)
        elif self.kind == "df":
            for leg in self.legs:
                if leg.card.endswith(("1", "X")):
                    break
            else:
                raise MocodoError(37, _('An association named "{df_label}" must have at least one leg with a maximal cardinality of 1.').format(df_label=df_label)) # fmt: skip


    def register_boxes(self, boxes):
        self.boxes = boxes

    def register_mcd_has_cif(self, mcd_has_cif):
        self.mcd_has_cif = mcd_has_cif
        for leg in self.legs:
            leg.register_mcd_has_cif(mcd_has_cif)

    def calculate_size_when_invisible(self, *ignored):
        self.w = 0
        self.h = 0
    
    def calculate_size_when_visible(self, style, get_font_metrics):
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
        self.cx = geo["cx"][self.bid]
        self.cy = geo["cy"][self.bid]
        self.l = self.cx - self.w // 2
        self.r = self.cx + self.w // 2
        self.t = self.cy - self.h // 2
        self.b = self.cy + self.h // 2

    def set_view_strategies(self):

        def calculate_size_when_df(style, get_font_metrics):
            self.w = self.h = max(
                style["round_rect_margin_width"] * 2 + self.get_cartouche_string_width(self.name_view),
                style["round_rect_margin_width"] * 2 + self.cartouche_height
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
                        "text": self.name_view,
                        "text_color": style['association_cartouche_text_color'],
                        "x": self.l + style["round_rect_margin_width"],
                        "y": self.t + style["round_rect_margin_height"] + style["df_text_height_ratio"] * self.cartouche_height,
                        "family": style["association_cartouche_font"]["family"],
                        "size": style["association_cartouche_font"]["size"],
                    },
                )
            ]
        
        def optional_description_for_cluster(style):
            if self.kind != "cluster" or self.mcd_has_cif:
                return []
            if len(self.legs) > 3:
                # The calculation of a hull with more than 3 legs is not implemented yet.
                return []
            result = []
            tweak = 1
            for (i, leg) in enumerate(self.legs):
                if leg.kind == "cluster_peg":
                    other_legs = self.legs[:i] + self.legs[i+1:]
                    e1 = other_legs[0].entity # the first entity of the other legs
                    e2 = other_legs[-1].entity # the last one, either the same as e1 or not
                    points = self.cluster_hull(e1, e2, style["card_margin"] * tweak)
                    if not points: # complex hulls are not implemented yet
                        continue
                    path = points_to_rounded_path(points, style["round_corner_radius"] // 2)
                    result.extend([
                        (
                            "polygon",
                            {
                                "path": path,
                                "stroke_color": None,
                                "stroke_depth": 0,
                                "color": style["entity_color"],
                                "opacity": 0.3 / self.peg_count,
                            },
                        ),
                        (
                            "dot_polygon",
                            {
                                "path": path,
                                "stroke_color": style['entity_stroke_color'],
                                "stroke_depth": style["box_stroke_depth"],
                                "color": None,
                                "dash_gap": style["dash_width"],
                            },
                        )
                    ])
                    tweak += 1
            return result

        def description_when_default(style):
            result = []
            result.extend(optional_description_for_cluster(style))
            if self.is_protected:
                result.append(
                    (
                        "round_rect",
                        {
                            "x": self.l - style["card_margin"] * 2,
                            "y": self.t - style["card_margin"] * 2,
                            "w": self.w + style["card_margin"] * 4,
                            "h": self.h + style["card_margin"] * 4,
                            "radius": style["round_corner_radius"] // 2,
                            "stroke_color": style['entity_stroke_color'] + "55", # alpha channel
                            "stroke_depth": style["box_stroke_depth"],
                            "color": style["entity_color"] + "55", # alpha channel
                        },
                    )
                )
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
            x = self.cx - self.w // 2 + style["round_rect_margin_width"]
            dx = 0
            dy = style["round_rect_margin_height"] + self.cartouche_height + 2 * style["rect_margin_height"] - self.h // 2
            for attribute in self.attributes:
                result.extend(attribute.description(style, x, self.cy, dx, dy))
                dy += self.attribute_height + style["line_skip_height"]
            return result

        if self.kind == "df":
            self.calculate_size_depending_on_kind = calculate_size_when_df
            self.description_depending_on_kind = description_when_df
        else:
            self.calculate_size_depending_on_kind = calculate_size_when_default
            self.description_depending_on_kind = description_when_default

    def description_when_visible(self, style, geo):
        self.saved_card_description = []
        result = []
        result.append(("comment", {"text": f"Association {self.bid}"}))
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
        result.extend(self.saved_card_description) # need to be displayed after the clusters for more readability
        result.append(("end", {}))
        return result

    def leg_descriptions(self, style, geo):
        result = []
        for leg in self.legs:
            result.extend(leg.description(style, geo))
            self.saved_card_description.extend(leg.saved_card_description)
        return result

    def cluster_hull(self, e1, e2, card_margin):
        x_min = min(box.l for box in (self, e1, e2))
        y_min = min(box.t for box in (self, e1, e2))
        x_max = max(box.r for box in (self, e1, e2))
        y_max = max(box.b for box in (self, e1, e2))
        x = x_min - card_margin // 2
        y = y_min - card_margin // 2
        w = x_max - x_min + card_margin
        h = y_max - y_min + card_margin

        x1_min = min(box.l for box in (self, e1))
        y1_min = min(box.t for box in (self, e1))
        x1_max = max(box.r for box in (self, e1))
        y1_max = max(box.b for box in (self, e1))
        x1 = x1_min - card_margin // 2
        y1 = y1_min - card_margin // 2
        w1 = x1_max - x1_min + card_margin
        h1 = y1_max - y1_min + card_margin
        
        x2_min = min(box.l for box in (self, e2))
        y2_min = min(box.t for box in (self, e2))
        x2_max = max(box.r for box in (self, e2))
        y2_max = max(box.b for box in (self, e2))
        x2 = x2_min - card_margin // 2
        y2 = y2_min - card_margin // 2
        w2 = x2_max - x2_min + card_margin
        h2 = y2_max - y2_min + card_margin

        e1_same_row = e1.t <= self.t < self.b <= e1.b or self.t <= e1.t < e1.b <= self.b
        e2_same_row = e2.t <= self.t < self.b <= e2.b or self.t <= e2.t < e2.b <= self.b
        e1_same_col = e1.l <= self.l < self.r <= e1.r or self.l <= e1.l < e1.r <= self.r
        e2_same_col = e2.l <= self.l < self.r <= e2.r or self.l <= e2.l < e2.r <= self.r
        if e1_same_row and e2_same_row or e1_same_col and e2_same_col:
            return [x, y, x+w, y, x+w, y+h, x, y+h]
        elif e1_same_row and e2_same_col:
            if e1.cx < self.cx:
                if e2.cy < self.cy:
                    #   2
                    # 1 a
                    return [x, y1, x2, y1, x2, y, x+w, y, x+w, y+h, x, y+h]
                else:
                    # 1 a
                    #   2
                    return [x, y, x+w, y, x+w, y+h, x2, y+h, x2, y1+h1, x, y1+h1]
            else:
                if e2.cy < self.cy:
                    # 2
                    # a 1
                    return [x, y, x2+w2, y, x2+w2, y1, x+w, y1, x+w, y+h, x, y+h]
                else:
                    # a 1
                    # 2
                    return [x, y, x+w, y, x+w, y1+h1, x2+w2, y1+h1, x2+w2, y+h, x, y+h]
        elif e2_same_row and e1_same_col:
            if e2.cx < self.cx:
                if e1.cy < self.cy:
                    #   1
                    # 2 a
                    return [x, y2, x1, y2, x1, y, x+w, y, x+w, y+h, x, y+h]
                else:
                    # 2 a
                    #   1
                    return [x, y, x+w, y, x+w, y+h, x1, y+h, x1, y2+h2, x, y2+h2]
            else:
                if e1.cy < self.cy:
                    # 1
                    # a 2
                    return [x, y, x1+w1, y, x1+w1, y2, x+w, y2, x+w, y+h, x, y+h]
                else:
                    # a 2
                    # 1
                    return [x, y, x+w, y, x+w, y2+h2, x1+w1, y2+h2, x1+w1, y+h, x, y+h]
        else:
            return []

def points_to_rounded_path(points, r):
    result = []
    points.extend(points[:6])
    for i in range(0, len(points) - 6, 2):
        (x1, y1, x2, y2, x3, y3) = points[i:i+6]
        if x1 < x2 and y2 > y3:
            #   3
            # 1 2
            (x2, c, dx, dy) = (x2 - r, 0, r, -r)
        elif x1 < x2 and y2 < y3:
            # 1 2
            #   3
            (x2, c, dx, dy) = (x2 - r, 1, r, r)
        elif x1 > x2 and y2 < y3:
            # 2 1
            # 3
            (x2, c, dx, dy) = (x2 + r, 0, -r, r)
        elif x1 > x2 and y2 > y3:
            # 3
            # 2 1
            (x2, c, dx, dy) = (x2 + r, 1, -r, -r)
        elif y1 < y2 and x2 > x3:
            #   1
            # 3 2
            (y2, c, dx, dy) = (y2 - r, 1, -r, r)
        elif y1 < y2 and x2 < x3:
            # 1
            # 2 3
            (y2, c, dx, dy) = (y2 - r, 0, r, r)
        elif y1 > y2 and x2 < x3:
            # 2 3
            # 1
            (y2, c, dx, dy) = (y2 + r, 1, r, -r)
        elif y1 > y2 and x2 > x3:
            # 3 2
            #   1
            (y2, c, dx, dy) = (y2 + r, 0, -r, -r)
        result.append(f"L{x2} {y2} a{r} {r} 0 0 {c} {dx} {dy}")
    result[0:0] = [f"M{x2+dx} {y2+dy}"]
    return " ".join(result)
