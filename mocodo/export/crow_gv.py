__import__("sys").path[0:0] = ["."]

from ._crow import Crow
from ..tools.parser_tools import parse_source
from ..update import (
    _drain as drain,
    _explode as explode,
    _split as split,
)
from ..tools.string_tools import rstrip_digit
from ..tools.graphviz_tools import NODE_OPTIONS_TEMPLATE, table_as_label

SUFFIX = "_crows_foot_erd.gv"

GV_CARD = {
    "01": "teeodot",
    "0N": "crowodot",
    "11": "teetee",
    "1N": "crowtee",
}

class CrowGv(Crow):
  
    def get_text(self, common):
        style = common.load_style()
        ent_table_style = {
            "stroke_color": style["box_stroke_depth"],
            "cell_bg_color": style["entity_color"],
            "header_bg_color": style["entity_cartouche_color"],
            "header_font_color": style["entity_cartouche_text_color"],
            "header_font_size": style["entity_cartouche_font"]["size"],
            "cell_font_color": style["entity_attribute_text_color"],
            "cell_font_size": style["entity_attribute_font"]["size"],
        }
        assoc_table_style = {
            "stroke_color": style["box_stroke_depth"],
            "cell_bg_color": style["association_color"],
            "header_bg_color": style["association_cartouche_color"],
            "header_font_color": style["association_cartouche_text_color"],
            "header_font_size": style["association_cartouche_font"]["size"],
            "cell_font_color": style["association_attribute_text_color"],
            "cell_font_size": style["association_attribute_font"]["size"],
        }
        acc = []
        acc.append(f'digraph{{')
        acc.append(f'  layout=dot')
        acc.append(f'  bgcolor="{style["background_color"]}"')
        acc.append(f'  nodesep=0.5') # increase spacing between multiedges

        acc.append(f'\n  // Nodes')
        for (i, table_style) in enumerate([assoc_table_style, ent_table_style]):
            node_options = NODE_OPTIONS_TEMPLATE.format(**ent_table_style)
            acc.append(f'  node [{node_options}]')
            for (ent_index, (ent_name, has_id, attrs)) in self.tables.items():
                if i != has_id:
                    continue
                attrs = [(("PK" if is_id else " "), a, (t or " ")) for (t, a, is_id) in attrs]
                row_format = "|c|lR|"
                if self.has_no_data_type:
                    attrs = [attr[:-1] for attr in attrs]
                    row_format = row_format.replace("R|", "|")
                label = table_as_label(ent_name, attrs, row_format, table_style)
                acc.append(f'  {ent_index} [label=<{label}>]')
        
        acc.append(f'\n  // Edges')
        acc.append(f'  edge [')
        acc.append(f'    penwidth={style["leg_stroke_depth"]}')
        acc.append(f'    color="{style["leg_stroke_color"]}"')
        acc.append(f'    fontcolor="{style["card_text_color"]}"')
        acc.append(f'    fontname="{style["card_font"]["family"]}"')
        acc.append(f'    fontsize={style["card_font"]["size"]}')
        acc.append(f'    dir=both') # bidirectional arrows, otherwise the tail doesn't appear
        acc.append(f'  ]')
        for (ent_1, card_1, kind, card_2, ent_2, assoc_name) in self.links:
            ent_index_1 = self.name_to_index(ent_1)
            ent_index_2 = self.name_to_index(ent_2)
            tail = GV_CARD.get(card_1, "crowodot")
            head = GV_CARD.get(card_2, "crowodot")
            kind = " style=dotted" if kind == ".." else ""
            label = ""
            if self.tables[ent_index_1][1] and self.tables[ent_index_2][1]:
                label = f' label="{rstrip_digit(assoc_name)}"'
            acc.append(f'  {ent_index_1} -> {ent_index_2} [arrowhead="{head}" arrowtail="{tail}"{label}{kind}]')
        acc.append('}')

        return "\n".join(acc)

def run(source, subargs, common=None):
    source = drain.run(source)
    source = split.run(source)
    source = explode.run(source, {"arity": "2.5", "weak": True})
    tree = parse_source(source)
    extractor = CrowGv()
    extractor.visit(tree)
    result = extractor.get_text(common)
    return result