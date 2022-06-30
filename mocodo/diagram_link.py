from .mocodo_error import MocodoError


class DiagramLink:
    def __init__(self, entities, foreign_entity, foreign_key):
        self.foreign_entity = foreign_entity
        self.foreign_key = foreign_key
        try:
            self.primary_entity = entities[foreign_key.primary_entity_name]
        except KeyError:
            raise MocodoError(14, _('Attribute "{attribute}" in entity "{entity_1}" references an unknown entity "{entity_2}".').format(attribute=foreign_key.label, entity_1=foreign_entity.name, entity_2=foreign_key.primary_entity_name)) # fmt: skip
        for candidate in self.primary_entity.attributes:
            if candidate.label.lstrip("#") == foreign_key.primary_key_label.lstrip("#"):
                self.primary_key = candidate
                break
        else:
            raise MocodoError(15, _('Attribute "{attribute_1}" in entity "{entity_1}" references an unknown attribute "{attribute_2}" in entity "{entity_2}".').format(attribute_1=foreign_key.label, entity_1=foreign_entity.name, attribute_2=foreign_key.primary_key_label, entity_2=foreign_key.primary_entity_name)) # fmt: skip

    def calculate_size(self, style, *ignored):
        self.fdx = self.foreign_entity.w // 2
        self.pdx = self.primary_entity.w // 2
        self.fdy = (
            -self.foreign_entity.h // 2
            + 3 * style["rect_margin_height"]
            + self.foreign_entity.cartouche_height
            + (self.foreign_key.rank + 0.5)
            * (self.foreign_entity.attribute_height + style["line_skip_height"])
        )
        self.pdy = (
            -self.primary_entity.h // 2
            + 3 * style["rect_margin_height"]
            + self.primary_entity.cartouche_height
            + (self.primary_key.rank + 0.5)
            * (self.primary_entity.attribute_height + style["line_skip_height"])
        )
        self.offset = 2 * (style["card_margin"] + style["card_max_width"])

    def description(self, style, geo):
        result = [("comment", {"text": f'Link from "{self.foreign_key.primary_key_label}" ({self.foreign_entity.name}) to "{self.primary_key.label}" ({self.primary_entity.name})'})]
        spins = (
            [(-1, -1), (1, -1), (-1, 1), (1, 1)]
            if self.foreign_key.rank % 2
            else [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        )
        (fs, ps) = min(
            spins,
            key=lambda fs_ps: abs(
                geo["cx"][self.foreign_entity.name]
                + self.fdx * fs_ps[0]
                - geo["cx"][self.primary_entity.name]
                - self.pdx * fs_ps[1]
            ),
        )
        xf = geo["cx"][self.foreign_entity.name] + self.fdx * fs
        yf = geo["cy"][self.foreign_entity.name] + self.fdy
        xp = geo["cx"][self.primary_entity.name] + self.pdx * ps
        yp = geo["cy"][self.primary_entity.name] + self.pdy
        result.append(
            (
                "curve",
                {
                    "x0": xf,
                    "y0": yf,
                    "x1": xf + (xp - xf) / 2 if fs != ps else xf + self.offset * fs,
                    "y1": yf + (yp - yf) / 2,
                    "x2": xf + (xp - xf) / 3 if fs != ps else xp + self.offset * ps,
                    "y2": yp,
                    "x3": xp,
                    "y3": yp,
                    "stroke_color": style["leg_stroke_color"],
                    "stroke_depth": style["leg_stroke_depth"],
                }
            )
        )
        result.append(
            (
                "arrow",
                {
                    "x0": xp,
                    "y0": yp,
                    "x1": xp + ps * style["arrow_width"],
                    "y1": yp - ps * style["arrow_half_height"],
                    "x2": xp + ps * style["arrow_axis"],
                    "y2": yp,
                    "x3": xp + ps * style["arrow_width"],
                    "y3": yp + ps * style["arrow_half_height"],
                    "stroke_color": style["leg_stroke_color"],
                },
            ),
        )
        result.append(
            (
                "circle",
                {
                    "cx": xf,
                    "cy": yf,
                    "r": style["box_stroke_depth"],
                    "stroke_depth": style["box_stroke_depth"],
                    "stroke_color": style["leg_stroke_color"],
                    "color": style["leg_stroke_color"],
                }
            )
        )
        return result
