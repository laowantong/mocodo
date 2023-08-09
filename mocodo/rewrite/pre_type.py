__import__("sys").path[0:0] = ["."]

from ..parse_mcd import Visitor
from ..parser_tools import parse_source, reconstruct_source, first_child

class CreateTypePlaceholder(Visitor):

    def typed_attr(self, tree):
        if first_child(tree, "data_type"):
            return
        name_token = first_child(tree, "attr")
        if not name_token:
            return
        name_token.value += " []"

def run(source, params=None):
    tree = parse_source(source)
    visitor = CreateTypePlaceholder()
    visitor.visit(tree)
    return reconstruct_source(tree)