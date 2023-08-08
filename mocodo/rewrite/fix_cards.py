__import__("sys").path[0:0] = ["."]

from ..parse_mcd import Transformer
from ..parser_tools import transform_source


class CardinalityFixer(Transformer):

    def __init__(self):
        self.fixes = {
            "01": ["O1", "o1", "10", "1O", "1o", "Ol", "ol", "l0", "lO", "lo"],
            "0N": ["ON", "oN", "NO", "No", "N0"],
            "0n": ["On", "on", "no", "nO", "n0"],
            "1N": ["N1", "Nl"],
            "1n": ["n1", "nl"],
        }
        self.fixes = {v: k for k in self.fixes for v in self.fixes[k]}
    
    def card(self, tree):
        card = tree[0].value
        new_card = self.fixes.get(card, card)
        return tree[0].update(value=new_card)

def run(source, params=None):
    return transform_source(source, CardinalityFixer())
