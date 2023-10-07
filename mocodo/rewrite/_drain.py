from collections import defaultdict

__import__("sys").path[0:0] = ["."]

from ..parse_mcd import Token, Visitor
from ..tools.parser_tools import parse_source, reconstruct_source, first_child


class DrainerFirstPass(Visitor):
    """
    In the first pass, the attributes to drain are suppressed from the tree and
    stored in a dictionary.
    """
    def __init__(self):
        self.drained_attrs = defaultdict(list)

    def assoc_clause(self, tree):

        # Guard: ensure that exactly one cardinality is 11
        cards = [node.children[0].value for node in tree.find_data("card")]
        if cards.count("11") != 1:
            return

        # Guard: ensure that the association has at least one attributes
        attrs = [*tree.find_data("typed_attr")]
        if len(attrs) == 0:
            return

        # Find out the name of the entity that is the target of the 11 leg
        entity_name_refs = [node.children[0] for node in tree.find_data("entity_name_ref")]
        i = cards.index("11")
        entity_name_ref = entity_name_refs[i].children[0].value

        # Store the attributes to drain
        self.drained_attrs[entity_name_ref].extend(map(reconstruct_source, attrs))

        # Remove the attributes from the association
        drop = False
        children = []
        for child in tree.children:
            if isinstance(child, Token):
                if child.type == "COLON":
                    drop = True
                elif child.type == "NL":
                    drop = False
            if not drop:
                children.append(child)
        tree.children = children


class DrainerSecondPass(Visitor):
    """
    In the second pass, the drained attributes are reinjected into the appropriate entities.
    """
    def __init__(self, drained_attrs):
        self.drained_attrs = drained_attrs

    def entity_clause(self, tree):

        # Guard: ensure that the entity must get drained attributes
        entity_name_def = first_child(tree, "entity_name_def").children[0]
        if not entity_name_def in self.drained_attrs:
            return

        # Add the drained attributes to the entity
        attrs = self.drained_attrs[entity_name_def]
        last_token = tree.children[-1]
        last_token.value = f", {', '.join(attrs)}{last_token.value}"


def run(source, **kargs):
    tree = parse_source(source)
    visitor = DrainerFirstPass()
    visitor.visit(tree)
    visitor = DrainerSecondPass(visitor.drained_attrs)
    visitor.visit(tree)
    return reconstruct_source(tree)
