class Attribute:

    def __init__(self, attribute, id_text=None):
        self.label = attribute.get("attribute_label", "")
        self.rank = attribute["rank"]
        self.data_type = attribute.get("data_type")
        self.primary_entity_name = attribute.get("that_table")
        self.primary_key_label = attribute.get("that_table_attribute_label")
        self.id_text = id_text

    def calculate_size(self, style, get_font_metrics):
        self.attribute_font = style[self.font_type]
        self.font = get_font_metrics(self.attribute_font)
        self.w = self.font.get_pixel_width(self.label)
        self.h = self.font.get_pixel_height()
        self.id_width = 0

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

    def __init__(self, attribute, id_text=None):
        Attribute.__init__(self, attribute, id_text)
        self.box_type = "entity"
        self.font_type = "entity_attribute_font"
        self.kind = "simple"


class SimpleAssociationAttribute(Attribute):

    def __init__(self, attribute):
        Attribute.__init__(self, attribute)
        self.box_type = "association"
        self.font_type = "association_attribute_font"
        self.kind = "simple_association"


class IdentifierAttribute(Attribute):

    def __init__(self, attribute, id_text):
        Attribute.__init__(self, attribute)
        self.box_type = "entity"
        self.font_type = "entity_attribute_font"
        self.id_text = id_text

    def calculate_size(self, *args):
        Attribute.calculate_size(self, *args)
        self.id_width = self.font.get_pixel_width(self.id_text)

    def description(self, style, x, y, left_gutter_width, dy):
        result = Attribute.description(self, style, x, y, left_gutter_width, dy)
        if left_gutter_width:
            result.append(
                (
                    "text",
                    {
                        "x": x + (left_gutter_width - self.id_width) // 2 - style["rect_margin_width"],
                        "y": y + round(dy + style["attribute_text_height_ratio"] * self.h, 1),
                        "text": self.id_text,
                        "text_color": style[f"{self.box_type}_attribute_text_color"],
                        "family": self.attribute_font["family"],
                        "size": self.attribute_font["size"],
                    }
                )
            )
        return result

class StrongAttribute(IdentifierAttribute):

    def __init__(self, attribute, id_text):
        IdentifierAttribute.__init__(self, attribute, id_text)
        self.kind = "strong"

    def description(self, style, x, y, left_gutter_width, dy):
        return IdentifierAttribute.description(self, style, x, y, left_gutter_width, dy) + [
            (
                "line",
                {
                    "x0": x + left_gutter_width,
                    "y0": y + dy + self.h + style["underline_skip_height"],
                    "x1": x + left_gutter_width + self.w,
                    "y1": y + dy + self.h + style["underline_skip_height"],
                    "stroke_depth": style["underline_depth"],
                    "stroke_color": style['entity_attribute_text_color'],
                }
            )
        ]

class WeakAttribute(IdentifierAttribute):

    def __init__(self, attribute, id_text):
        IdentifierAttribute.__init__(self, attribute, id_text)
        self.kind = "weak"

    def description(self, style, x, y, left_gutter_width, dy):
        return IdentifierAttribute.description(self, style, x, y, left_gutter_width, dy) + [
            (
                "dash_line",
                {
                    "x0": x + left_gutter_width,
                    "y0": y + dy + self.h + style["underline_skip_height"],
                    "x1": x + left_gutter_width + self.w,
                    "y1": y + dy + self.h + style["underline_skip_height"],
                    "dash_width": style["dash_width"],
                    "stroke_depth": style["underline_depth"],
                    "stroke_color": style['entity_attribute_text_color'],
                }
            )
        ]


class AltIdentifierAttribute(IdentifierAttribute):

    def __init__(self, attribute, id_text):
        IdentifierAttribute.__init__(self, attribute, id_text)
        self.id_groups = "".join(sorted(set(attribute["id_groups"])))
        self.kind = "alt_identifier"


class PhantomAttribute(Attribute):
    
    def __init__(self, attribute):
        Attribute.__init__(self, attribute)
        self.kind = "phantom"
        self.font_type = "entity_attribute_font" # dummy
    
    def description(self, style, x, y, left_gutter_width, dy):
        return []


class InheritanceAttribute(Attribute):

    def __init__(self, attribute):
        Attribute.__init__(self, attribute)
        self.kind = "inheritance"
