class Attribute:

    def __init__(self, attribute):
        self.label = attribute.get("attribute_label", "")
        self.rank = attribute["rank"]
        self.data_type = attribute.get("data_type")
        self.primary_entity_name = attribute.get("that_table")
        self.primary_key_label = attribute.get("that_table_attribute_label")

    def calculate_size(self, style, get_font_metrics):
        self.attribute_font = style[self.font_type]
        self.font = get_font_metrics(self.attribute_font)
        self.w = self.font.get_pixel_width(self.label)
        self.h = self.font.get_pixel_height()

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

    def __init__(self, attribute):
        Attribute.__init__(self, attribute)
        self.box_type = "entity"
        self.font_type = "entity_attribute_font"
        self.kind = "simple"


class SimpleAssociationAttribute(Attribute):

    def __init__(self, attribute):
        Attribute.__init__(self, attribute)
        self.box_type = "association"
        self.font_type = "association_attribute_font"
        self.kind = "simple_association"


class StrongAttribute(Attribute):

    def __init__(self, attribute):
        Attribute.__init__(self, attribute)
        self.box_type = "entity"
        self.font_type = "entity_attribute_font"
        self.kind = "strong"

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

class AlternateIdentifierAttribute(Attribute):

    def __init__(self, attribute):
        Attribute.__init__(self, attribute)
        self.group = attribute["id_group"]
        self.box_type = "entity"
        self.font_type = "entity_attribute_font"
        self.kind = "alternate_identifier"

    def calculate_size(self, *args):
        Attribute.calculate_size(self, *args)
        self.group_width = self.font.get_pixel_width(self.group)

    def description(self, style, x, y, dx, dy):
        return [
            (
                "text",
                {
                    "x": x + dx,
                    "y": y + round(dy + style["attribute_text_height_ratio"] * self.h, 1),
                    "text": f"{self.group} {self.label}",
                    "text_color": style[f"{self.box_type}_attribute_text_color"],
                    "family": self.attribute_font["family"],
                    "size": self.attribute_font["size"],
                }
            ),
            (
                "line",
                {
                    "x0": x + dx,
                    "y0": y + dy + self.h + style["underline_skip_height"],
                    "x1": x + dx + self.group_width,
                    "y1": y + dy + self.h + style["underline_skip_height"],
                    "stroke_depth": style["underline_depth"],
                    "stroke_color": style['entity_attribute_text_color'],
                }
            )
        ]


class WeakAttribute(Attribute):

    def __init__(self, attribute):
        Attribute.__init__(self, attribute)
        self.box_type = "entity"
        self.font_type = "entity_attribute_font"
        self.kind = "weak"

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
    
    def __init__(self, attribute):
        Attribute.__init__(self, attribute)
        self.kind = "phantom"
    
    def description(self, style, x, y, dx, dy):
        return []


class InheritanceAttribute(Attribute):

    def __init__(self, attribute):
        Attribute.__init__(self, attribute)
        self.kind = "inheritance"
