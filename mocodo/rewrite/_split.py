from collections import Counter

__import__("sys").path[0:0] = ["."]

from ..parse_mcd import Token, Visitor
from ..tools.parser_tools import parse_source, reconstruct_source, first_child

class Splitter(Visitor):

    def line(self, tree):
        # It is not possible to use a method `assoc_clause` since the amount of indentation needs
        # to be known for the added clauses.

        # Guard: store the indentation and abort if the clause is not an association.
        indent = next(tree.find_data("indent"), None)
        indent = indent.children[0].value if indent else ""
        tree = next(tree.find_data("assoc_clause"), None)
        if tree is None:
            return

        # Guard: abort if the association has less than 3 legs.
        legs = [node for node in tree.find_data("assoc_leg")]
        if len(legs) < 3:
            return

        # Reorder the legs with "11" cards first, then "01", then the other ones.
        d = {"11": 0, "01": 1}
        legs.sort(key=lambda leg: d.get(first_child(leg, "card").value, 2))

        # Guard: ensure that the first max cardinality is 1.
        if first_child(legs[0], "card")[1] != "1":
            return
        
        # Guard: don't split a clustered association
        card_prefixes = [first_child(leg, "card_prefix") == "/" for leg in legs]
        if any(card_prefixes):
            return
        
        # Accumulate the constituting elements (cf. grammar.lark) of the original legs.
        new_items = []
        for leg in legs:
            acc = []
            acc.append(first_child(leg, "card_hidden"))
            acc.append(first_child(leg, "card_prefix"))
            acc.append(first_child(leg, "card"))
            acc.append(first_child(leg, "leg_arrow"))
            acc.append(first_child(leg, "leg_note"))
            acc[-1] = f" [{acc[-1]}] " if acc[-1] else " "
            acc.append(first_child(leg, "entity_name_ref").children[0])
            new_items.append("".join(acc))
        
        # Concatenate any attributes of the association.
        attrs = []
        for child in tree.find_data("typed_attr"):
            acc = []
            acc.append(first_child(child, "attr"))
            datatype  = first_child(child, "datatype")
            if datatype:
                acc.append(f" [{datatype}]")
            attrs.append("".join(acc))
        
        # Construct the lines of the exploded association. The *1 leg is the first one.
        result = []
        box_def_prefix = first_child(tree, "box_def_prefix")
        assoc_name_def = first_child(tree, "assoc_name_def").children[0]
        for (i, new_item) in enumerate(new_items[1:]):
            result.append(f"{indent}{box_def_prefix}{assoc_name_def}{i}, {new_items[0]}, {new_item}")

        # Add the attributes to the first clause only. Duplicating them would be an error.
        result[0] += f": {', '.join(attrs)}" if attrs else ""

        # The first clause starts at the same position as the association name: unindent.
        result[0] = result[0].lstrip()

        # Add a blank line after the exploded association.
        result.append("")

        # Replace the original tree by a pseudo-tree containing only the desired string.
        token = first_child(tree, "box_name")
        tree.children = [Token("MOCK", "\n".join(result), line=token.line, column=token.column)]

def run(source, **kargs):
    tree = parse_source(source)
    visitor = Splitter()
    visitor.visit(tree)
    return reconstruct_source(tree)
