import importlib

__import__("sys").path[0:0] = ["."]

from ..mocodo_error import subsubopt_error
from ..parse_mcd import Visitor
from ..tools.parser_tools import first_child, is_identifier
from ..tools.string_tools import rstrip_digit_or_underline
from ..tools.graphviz_tools import create_name_to_index


class Crow(Visitor):
    def __init__(self):
        self.name_to_index = create_name_to_index()
        self.tables = {}
        self.links = []
        self.has_no_data_type = True
    
    def data_type(self, tree):
        s = "".join(tree.children)[2:-1] # remove the surrounding brackets
        tree.children = [s]

    def entity_or_table_attr(self, tree):
        id_groups = str(first_child(tree, "id_groups"))
        id_mark = str(first_child(tree, "id_mark"))
        attr = str(first_child(tree, "attr"))
        data_type = str(first_child(tree, "data_type"))
        if data_type:
            self.has_no_data_type = False
        tree.children = [(id_groups, id_mark, attr, data_type)]
    
    def entity_clause(self, tree):
        ent_name = first_child(tree, "box_name").value
        ent_index = self.name_to_index(ent_name)
        ent_name = rstrip_digit_or_underline(ent_name)
        attrs = []
        has_id = False
        for (i, node) in enumerate(tree.find_data("entity_or_table_attr")):
            (id_groups, id_mark, attr, data_type) = node.children[0]
            is_id = is_identifier(i, id_groups, id_mark)
            has_id = has_id or is_id
            attrs.append((data_type, attr, is_id))
        self.tables[ent_index] = (ent_name, has_id, attrs)
    
    def assoc_clause(self, tree):
        cards = [node.children[0].value for node in tree.find_data("card")]
        assert len(cards) == 2
        assoc_name = first_child(tree, "assoc_name_def").children[0].value
        assoc_name = rstrip_digit_or_underline(assoc_name)
        kind = ".." if any(s.children[0].value == "_" for s in tree.find_data("card_prefix")) else "--"
        entities = tree.find_data("entity_name_ref")
        ent_1 = first_child(next(entities), "entity_name_ref").children[0]
        ent_2 = first_child(next(entities), "entity_name_ref").children[0]
        self.links.append((ent_1, cards[1], kind, cards[0], ent_2, assoc_name))


def run(source, subargs, common=None):
    extension = "mmd" if "mmd" in subargs or "mermaid" in subargs else "gv"
    try:
        module = importlib.import_module(f".convert.crow_{extension}", package="mocodo")
    except ModuleNotFoundError:
        raise subsubopt_error(extension)
    text = module.run(source, subargs, common)
    return {
        "stem_suffix": "_erd_crow",
        "text": text,
        "extension": extension,
        "to_defer": True,
        "highlight": "mermaid" if extension == "mmd" else "graphviz",
    }
