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

        # Guard: ensure that only one max cardinality is 1 and there are more than 2 legs.
        cards = [node.children[0].value for node in tree.find_data("card")]
        max_cards = Counter(card[1] for card in cards)
        if max_cards["1"] != 1 or max_cards["N"] < 2:
            return
        
        # Guard: don't split a clustered association
        card_prefixes = [node.children[0].value == "/" for node in tree.find_data("card_prefix")]
        if any(card_prefixes):
            return
        
        # Concatenate the constituting elements (cf. grammar.lark) of the original legs
        # and associate them to their max cardinality.
        legs = {"1": [], "N": []}
        for (card, child) in zip(cards, tree.find_data("assoc_leg")):
            acc = []
            acc.append(first_child(child, "card_hidden"))
            acc.append(first_child(child, "card_prefix"))
            acc.append(first_child(child, "card"))
            acc.append(first_child(child, "leg_arrow"))
            acc.append(first_child(child, "leg_note"))
            acc[-1] = f" [{acc[-1]}] " if acc[-1] else " "
            acc.append(first_child(child, "entity_name_ref").children[0])
            legs[card[1]].append("".join(acc))
        
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
        for (i, leg) in enumerate(legs["N"]):
            result.append(f"{indent}{box_def_prefix}{assoc_name_def}{i}, {legs['1'][0]}, {leg}")

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
