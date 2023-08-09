__import__("sys").path[0:0] = ["."]

from ..parse_mcd import Token, Visitor
from ..parser_tools import parse_source, reconstruct_source, first_child

class Exploder(Visitor):

    def __init__(self, params):
        self.threshold = int(params["explosion_arity"])
        if params["weak_explosion"]:
            # Don't create an identifier for the new weak entity
            self.explosion_template = ":"
            # Prefix the potential first attribute with an underscore
            self.explosion_prefix = " _"
            # Strenghten the new legs
            self.explosion_card = "_11"
        else:
            # Create a strong identifier for the new entity
            self.explosion_template = ": id. {}"
            # Separate the potential first attribute with a comma
            self.explosion_prefix = ", "
            # Don't strengthen the new legs
            self.explosion_card = "11"

    def line(self, tree):
        # It is not possible to use a method `assoc_clause` since the amount of indentation needs
        # to be known for the added clauses.

        # Guard: store the indentation and abort if the clause is not an association.
        indent = next(tree.find_data("indent"), None)
        indent = indent.children[0].value if indent else ""
        tree = next(tree.find_data("assoc_clause"), None)
        if tree is None:
            return

        # Guard: ensure that there are enough legs and all their max cards are N.
        cards = [node.children[0].value for node in tree.find_data("card")]
        if len(cards) < self.threshold or any(card[1] != "N" for card in cards):
            return
        
        # Back the legs up as a list of strings.
        legs = list(map(reconstruct_source, tree.find_data("assoc_leg")))

        # Convert the original association into an entity.
        assoc_name = first_child(tree, "assoc_name_def").children[0]
        state = "Waiting for first comma"
        children = []
        for child in tree.children:
            if isinstance(child, Token):
                if child.type == "COMMA" and state == "Waiting for first comma":
                    child.value = self.explosion_template.format(assoc_name.lower())
                    children.append(child)
                    state = "Scanning legs"
                    continue
                if child.type == "COLON": # There were at least one attribute
                    state = "Scanning attributes"
                    child.value = self.explosion_prefix
                if child.type == "NL": # useful where there are no attributes
                    state = "EOL"
            if state != "Scanning legs":
                children.append(child)
        tree.children = children

        # Construct the clauses of the new associations
        clauses = []
        prefix = first_child(tree, "box_def_prefix")
        base = assoc_name[:2]
        for (i, leg) in enumerate(legs, 1):
            clauses.append(f"{indent}{prefix}{base}{i}, {self.explosion_card} {assoc_name}, {leg}")

        # Suffix the resulting string to the last node (a "NL" token")
        tree.children[-1].value += "\n".join(clauses) + "\n"


def run(source, params):
    tree = parse_source(source)
    visitor = Exploder(params)
    visitor.visit(tree)
    return reconstruct_source(tree)