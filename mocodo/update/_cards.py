import random
import re
from collections import Counter


from . import stand_for
from ..mocodo_error import subsubopt_error
from ..parse_mcd import Visitor, Tree
from ..tools.parser_tools import parse_source, reconstruct_source
from ..tools.various import invert_dict
from .op_tk import op_tk


def fix_card(
    card,
    fixes=invert_dict(
        {
            "01": ["O1", "o1", "10", "1O", "1o", "Ol", "ol", "l0", "lO", "lo"],
            "0N": ["ON", "oN", "NO", "No", "N0"],
            "0n": ["On", "on", "no", "nO", "n0"],
            "1N": ["N1", "Nl"],
            "1n": ["n1", "nl"],
        }
    ),
):
    return fixes.get(card, card)


class CardRandomizer(Visitor):
    def __init__(self, card_prefixes, card_counter, params):
        self.card_prefixes = card_prefixes
        self.card_counter = card_counter
        seed = params.get("seed", 42)
        if seed is not None:
            random.seed(seed)
        self.df_label = params.get("df", "DF")

    def assoc_clause(self, tree):

        # Suppress all card prefixes
        for leg_tree in tree.find_data("assoc_leg"):
            new_children = []
            for child in leg_tree.children:
                if type(child) == Tree and child.data == "card_prefix":
                    continue
                new_children.append(child)
            leg_tree.children = new_children

        # Find the association name
        def_tree = next(tree.find_data("assoc_name_def"))
        box_tree = next(def_tree.find_data("box_name"))
        assoc_name = box_tree.children[0].value

        # Find the card tokens to be randomized
        card_tokens = [t.children[0] for t in tree.find_data("card")]

        # Construct a new list of cards, containing at most one "11"
        new_cards = []
        while True:
            candidate = random.choice(("01", "11", "0N", "1N"))
            if candidate != "11" or "11" not in new_cards:
                new_cards.append(candidate)
                if len(new_cards) == len(card_tokens):
                    break

        # If the association is explicitely a DF, make sure that at least one card is "11"
        if re.match(rf"{self.df_label}\d*$", assoc_name):
            if "11" not in new_cards:
                new_cards[random.randrange(len(new_cards))] = "11"

        # If there is at least one "_" prefix in the original MCD, prefix it to approximately
        # the same proportion of random "11" cards. Note that the new prefix should be stored
        # in its own node in the tree, but we don't bother to do that since the tree will immediately
        # be converted back to a string.
        if self.card_counter["11"] > 0:
            proba = self.card_prefixes["_"] / self.card_counter["11"]
            new_cards = [
                f"_{card}" if card == "11" and random.random() < proba else card
                for card in new_cards
            ]

        # Same treatment for "/" prefix with "0N" and "1N" cards.
        if self.card_counter["0N"] + self.card_counter["1N"] > 0:
            proba = self.card_prefixes["/"] / (self.card_counter["0N"] + self.card_counter["1N"])
            new_cards = [
                f"/{card}" if card in ("0N", "1N") and random.random() < proba else card
                for card in new_cards
            ]

        # Map the new cards to the card tokens
        for (card_token, new_card) in zip(card_tokens, new_cards):
            card_token.value = new_card


def run(source, subargs=None, params=None):
    subargs = subargs or {}
    params = params or {}
    for (subsubopt, subsubarg) in subargs.items():
        if stand_for(subsubopt, "lower", "upper"):
            source = op_tk(source, "card", subsubopt)
        elif stand_for(subsubopt, "delete"):
            source = op_tk(source, "card", lambda _: "XX")
        elif stand_for(subsubopt, "fix"):
            source = op_tk(source, "card", fix_card)
        elif stand_for(subsubopt, "randomize"):
            tree = parse_source(source)
            card_prefixes = Counter(node.children[0].value for node in tree.find_data("card_prefix"))
            card_counter = Counter(node.children[0].value for node in tree.find_data("card"))
            visitor = CardRandomizer(card_prefixes, card_counter, params)
            visitor.visit(tree)
            source = reconstruct_source(tree)
        else:
            raise subsubopt_error(subsubopt)
    return source
