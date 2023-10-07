__import__("sys").path[0:0] = ["."]

import contextlib
from ..parse_mcd import Token, Visitor
from ..tools.parser_tools import parse_source, reconstruct_source, first_child

class Exploder(Visitor):

    def __init__(self, subargs, params):
        arity = 3
        with contextlib.suppress(ValueError, KeyError):
            arity = float(subargs["arity"])
        self.empty_only = (arity == 2.5)
        self.threshold = int(arity)
        self.allow_weak = "weak" in subargs
        if self.allow_weak:
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
        self.df_label = params["df"]

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
        
        # Guard: on demand, avoid processing binary associations with no attributes.
        if self.empty_only and not first_child(tree, "typed_attr"):
            return

        # Guard: don't explode a clustered association if weak is not allowed
        card_prefixes = [node.children[0].value == "/" for node in tree.find_data("card_prefix")]
        if any(card_prefixes) and not self.allow_weak:
            return
        
        # Guard: don't explode an association of several clusters
        if sum(card_prefixes) > 1:
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
        for leg in legs:
            card = self.explosion_card
            # TODO: check this logic
            if leg.startswith("/"): # when there is a cluster
                leg = leg[1:] # suppress it
                card = "11" # and switch to a non-strenghtening leg
            clauses.append(f"{indent}{prefix}{self.df_label}, {card} {assoc_name}, {leg}")

        # Suffix the resulting string to the last node (a "NL" token")
        tree.children[-1].value += "\n".join(clauses) + "\n"


def run(source, subargs=None, params=None, **kargs):
    subargs = subargs or {}
    params = params or {"df": "DF"}
    tree = parse_source(source)
    visitor = Exploder(subargs, params)
    visitor.visit(tree)
    return reconstruct_source(tree)
