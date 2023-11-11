from ..parse_mcd import Visitor
from ..tools.parser_tools import first_child, parse_source, reconstruct_source

class ArrowsHere(Visitor):

    def assoc_leg(self, tree):
        card = first_child(tree, "card")
        if card != "11":
            return
        if first_child(tree, "leg_arrow") != "":
            return
        card.value += "<"
    
class ArrowsAcross(Visitor):

    def assoc_clause(self, tree):
        legs = [node for node in tree.find_data("assoc_leg")]
        cards = [first_child(leg, "card") for leg in legs]
        for (i, card) in enumerate(cards):
            if card == "11":
                for (j, other_leg) in enumerate(legs):
                    if i != j and first_child(other_leg, "leg_arrow") == "":
                        other_card = first_child(other_leg, "card")
                        other_card.value += ">"


def create_df_arrows(source, where):
    visitor = ArrowsHere() if where == "here" else ArrowsAcross()
    tree = parse_source(source)
    visitor.visit(tree)
    return reconstruct_source(tree)
