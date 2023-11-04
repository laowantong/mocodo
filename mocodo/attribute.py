from .tools.string_tools import raw_to_bid

class Attribute:

    # The following three static attributes will be updated by Mcd.add_attributes() method.
    # They are here to simplify the writing of some tests.
    id_gutter_strong_string = "ID"
    id_gutter_weak_string = "id"
    id_gutter_alts = dict(zip("123456789", "123456789"))

    def __init__(self, attribute):
        self.label = attribute.get("attribute_label", "")
        self.label_view = self.label # may be updated in self.register_foreign_key_status()
        self.rank = attribute["rank"]
        self.datatype = attribute.get("datatype", "")
        self.primary_entity_bid = raw_to_bid(attribute.get("that_table", ""))
        self.id_groups = set(attribute.get("id_groups", "").replace("0", ""))
        self.id_text =  " ".join(map(self.id_gutter_alts.get, sorted(self.id_groups)))
        self.id_gutter_width = 0  # For anything but entities

    def register_foreign_key_status(self, attribute, fk_format):
        that_table = attribute.get("that_table")
        if not that_table:
            return
        self.primary_key_label = attribute.get("that_table_attribute_label")
        self.label_view = fk_format.format(label=self.label)

    def calculate_size(self, style, get_font_metrics):
        self.attribute_font = style[self.font_type]
        self.font = get_font_metrics(self.attribute_font)
        self.w = self.font.get_pixel_width(self.label_view)
        self.h = self.font.get_pixel_height()
        self.id_width = self.font.get_pixel_width(self.id_text)

    def set_id_gutter_width(self, id_gutter_width):
        self.id_gutter_width = id_gutter_width

    def description(self, style, x, y, dx, dy):
        result = [
            (
                "text",
                {
                    "x": x + dx,
                    "y": y + round(dy + style["attribute_text_height_ratio"] * self.h, 1),
                    "text": self.label_view,
                    "text_color": style[f"{self.box_type}_attribute_text_color"],
                    "family": self.attribute_font["family"],
                    "size": self.attribute_font["size"],
                }
            )
        ]
        if self.id_gutter_width:
            result.append(
                (
                    "text",
                    {
                        "x": x + (self.id_gutter_width - self.id_width) // 2 - style["rect_margin_width"],
                        "y": y + round(dy + style["attribute_text_height_ratio"] * self.h, 1),
                        "text": self.id_text,
                        "text_color": style[f"{self.box_type}_attribute_text_color"],
                        "family": self.attribute_font["family"],
                        "size": self.attribute_font["size"],
                    }
                )
            )
        return result

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


class IdentifierAttribute(Attribute):

    def __init__(self, attribute):
        Attribute.__init__(self, attribute)
        self.box_type = "entity"
        self.font_type = "entity_attribute_font"
        self.id_groups.add("0")

    def calculate_size(self, *args):
        Attribute.calculate_size(self, *args)

class StrongAttribute(IdentifierAttribute):

    def __init__(self, attribute):
        IdentifierAttribute.__init__(self, attribute)
        self.id_text = f"{self.id_text} {self.id_gutter_strong_string}".lstrip()
        self.kind = "strong"

    def description(self, style, x, y, dx, dy):
        return IdentifierAttribute.description(self, style, x, y, dx, dy) + [
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

class WeakAttribute(IdentifierAttribute):

    def __init__(self, attribute):
        IdentifierAttribute.__init__(self, attribute)
        self.id_text = f"{self.id_text} {self.id_gutter_weak_string}".lstrip()
        self.kind = "weak"

    def description(self, style, x, y, dx, dy):
        return IdentifierAttribute.description(self, style, x, y, dx, dy) + [
            (
                "dash_line",
                {
                    "x0": x + dx,
                    "y0": y + dy + self.h + style["underline_skip_height"],
                    "x1": x + dx + self.w,
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
        self.font_type = "entity_attribute_font" # dummy
    
    def description(self, *_):
        return []


class InheritanceAttribute(Attribute):

    def __init__(self, attribute):
        Attribute.__init__(self, attribute)
        self.kind = "inheritance"
