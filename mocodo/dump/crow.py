import re

__import__("sys").path[0:0] = ["."]

from ..parse_mcd import Visitor, Token, Tree
from ..parser_tools import transform_source, first_child, parse_source
from ..modify import (
    op_tk,
    drain,
    explode,
    split,
)

FILENAME_SUFFIX = "_crows_foot_erd.mmd"

LEFT_CARD = {
    "01": "|o",
    "0N": "}o",
    "11": "||",
    "1N": "}|",
}
RIGHT_CARD = {
    "01": "o|",
    "0N": "o{",
    "11": "||",
    "1N": "|{",
}

class Crow(Visitor):
    def __init__(self):
        self.result = ["erDiagram"]
    
    def data_type(self, tree):
        s = "".join(tree.children)[2:-1] # remove the surrounding brackets
        # In Mermaid syntax, the type values must begin with an alphabetic character
        # and may contain digits, hyphens, underscores, parentheses and square brackets.
        s = s.replace(",", "-") # as long as https://github.com/mermaid-js/mermaid/issues/1546 is not fixed
        s = re.sub(r"[^-_0-9A-Za-z()[\]]", "_", s)
        s = re.sub(r"__+", "_", s)
        s = s.strip("_")
        tree.children = [s]

    def entity_or_table_attr(self, tree):
        attr = first_child(tree, "attr")
        id_mark = int(bool(first_child(tree, "id_mark")))
        data_type = first_child(tree, "data_type")
        data_type = data_type or "TYPE"
        tree.children = [f'        {data_type} {attr}{id_mark}']
    
    def entity_clause(self, tree):
        name = first_child(tree, "box_name")
        attrs = []
        for (i, node) in enumerate(tree.find_data("entity_or_table_attr")):
            s = node.children[0]
            if (s[-1] == "0" and i == 0) or (s[-1] == "1" and i != 0):
                s = s[:-1] + " PK"
            else:
                s = s[:-1]
            attrs.append(s)
        self.result.append(f"    {name} {{")
        self.result.extend(attrs)
        self.result.append(f"    }}")
    
    def assoc_clause(self, tree):
        cards = [node.children[0].value for node in tree.find_data("card")]
        if len(cards) != 2:
            return
        assoc = first_child(tree, "assoc_name_def").children[0].lower()
        if assoc[-1].isdigit():
            assoc = assoc[:-1]
        card_1 = LEFT_CARD.get(cards[1], "}|")
        card_2 = RIGHT_CARD.get(cards[0], "|{")
        kind = "--" if any(tree.find_data("card_prefix")) else ".."
        entities = tree.find_data("entity_name_ref")
        ent_1 = first_child(next(entities), "entity_name_ref").children[0]
        ent_2 = first_child(next(entities), "entity_name_ref").children[0]
        self.result.append(f"    {ent_1} {card_1}{kind}{card_2} {ent_2}: {assoc}")

def run(source, params=None):
    source = op_tk.run(source, "ascii", "label")
    source = op_tk.run(source, "snake", "label")
    source = drain.run(source)
    source = split.run(source)
    source = explode.run(source, {"explosion_arity": "2.5", "weak_explosion": True})
    tree = parse_source(source)
    extractor = Crow()
    extractor.visit(tree)
    result = "\n".join(extractor.result)
    return result
