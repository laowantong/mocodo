import re


def outer_split(s, findall_outer_commas = re.compile(r'[^,]+\[.*?\][^,]*|[^,]+').findall):
    return [s.replace(", ", ",").strip(" \t").replace("\\", "") for s in findall_outer_commas(s.replace(",", ", "))]



class Attribute:

    def __init__(self, attribute, rank, search_label_and_type = re.compile(r"^(.*?)(?: *\[(.*)\])?$").search):
        (label, dt) = search_label_and_type(attribute).groups()
        self.data_type = dt and dt.replace("<<<safe-comma>>>", ",").replace("<<<safe-colon>>>", ":")
        components = label.split("->")
        if len(components) == 3:
            (self.label, self.primary_entity_name, self.primary_key_label) = components
        else:
            (self.label, self.primary_entity_name, self.primary_key_label) = (label, None, None)
        self.box_type = "entity"
        self.font_type = "entity_attribute_font"
        self.rank = rank

    def calculate_size(self, style, get_font_metrics):
        self.attribute_font = style[self.font_type]
        font = get_font_metrics(self.attribute_font)
        self.w = font.get_pixel_width(self.label)
        self.h = font.get_pixel_height()

    def description(self, style, x, y, dx, dy):
        return [
            (
                "text",
                {
                    "x": x + dx,
                    "y": y + round(dy + style["attribute_text_height_ratio"] * self.h, 1),
                    "text": self.label,
                    "text_color": style[f"{self.box_type}_attribute_text_color"],
                    "family": self.attribute_font["family"],
                    "size": self.attribute_font["size"],
                }
            )
        ]


class SimpleEntityAttribute(Attribute):

    def __init__(self, attribute, rank):
        Attribute.__init__(self, attribute, rank)

    def get_category(self):
        return "simple"


class SimpleAssociationAttribute(Attribute):

    def __init__(self, attribute, rank):
        Attribute.__init__(self, attribute, rank)
        self.box_type = "association"
        self.font_type = "association_attribute_font"


class StrongAttribute(Attribute):

    def __init__(self, attribute, rank):
        Attribute.__init__(self, attribute, rank)

    def get_category(self):
        return "strong"

    def description(self, style, x, y, dx, dy):
        return Attribute.description(self, style, x, y, dx, dy) + [
            (
                "line",
                {
                    "x0": x + dx,
                    "y0": y + dy + self.h + style["underline_skip_height"],
                    "x1": x + dx + self.w,
                    "y1": y + dy + self.h + style["underline_skip_height"],
                    "stroke_depth": style["underline_depth"],
                    "stroke_color": style['entity_attribute_text_color'],
                }
            )
        ]


class WeakAttribute(Attribute):

    def __init__(self, attribute, rank):
        Attribute.__init__(self, attribute, rank)

    def get_category(self):
        return "weak"

    def description(self, style, x, y, dx, dy):
        return Attribute.description(self, style, x, y, dx, dy) + [
            (
                "dash_line",
                {
                    "x0": x + dx,
                    "x1": x + dx + self.w,
                    "y0": y + dy + self.h + style["underline_skip_height"],
                    "y1": y + dy + self.h + style["underline_skip_height"],
                    "dash_width": style["dash_width"],
                    "stroke_depth": style["underline_depth"],
                    "stroke_color": style['entity_attribute_text_color'],
                }
            )
        ]


class PhantomAttribute(Attribute):

    def __init__(self, rank):
        Attribute.__init__(self, "", rank)

    def get_category(self):
        return "phantom"

    def description(self, style, x, y, dx, dy):
        return []
