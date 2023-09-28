from ..parse_mcd import Visitor
from ..tools.parser_tools import first_child, parse_source, reconstruct_source


class Numbering(Visitor):

    def __init__(self, tree, params):

        self.size = len(str(len(set(node.children[0].value for node in tree.find_data("box_name")))))

        def new_name(base_name, name, i):
            if name == params["df"]:
                return name
            return f"{base_name} {i:0{self.size}d}_"

        def update_translations(token_name, base_name, n):
            nodes = tree.find_data(token_name)
            names = [node.children[0].children[0].value for node in nodes]
            self.names.update({name: new_name(base_name, name, i) for (i, name) in enumerate(names, n)})
            self.numbers.update({new_name(base_name, name, i): f"{i:0{self.size}d}"  for (i, name) in enumerate(names, n)})
        
        self.names = {}
        self.numbers = {}
        update_translations("entity_name_def", _("ENTITY"), 1)
        update_translations("assoc_name_def", _("ASSOC"), len(self.names) + 1)

        self.attr_base = _("attr")
        self.leg_note_base = _("role")

    def update_box_attrs(self, tree, token_name):
        number = self.numbers[first_child(tree, token_name).children[0].value]
        for (i, attr) in enumerate(tree.find_data("attr"), 1):
            if attr.children[0] == "":
                continue # do nothing for a spacer attribute
            attr.children[0].value = f"{self.attr_base} {number} {i}"
    
    def box_name(self, tree):
        token = tree.children[0]
        token.value = self.names[token.value]

    def entity_clause(self, tree):
        self.update_box_attrs(tree, "entity_name_def")
    
    def assoc_clause(self, tree):
        self.update_box_attrs(tree, "assoc_name_def")
        for (i, attr) in enumerate(tree.find_data("leg_note"), 1):
            attr.children[0].value = f"{self.leg_note_base} {i}"


def run(source, params, **kargs):
    tree = parse_source(source)
    visitor = Numbering(tree, params)
    visitor.visit(tree)
    return reconstruct_source(tree)
