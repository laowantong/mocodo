import random
import re
from collections import Counter

__import__("sys").path[0:0] = ["."]

from ..parse_mcd import Tree, Visitor
from ..tools.parser_tools import parse_source, reconstruct_source


class CardRandomizer(Visitor):

    def __init__(self, card_prefixes, cards, params):
        self.card_prefixes = card_prefixes
        self.cards = cards
        seed = params["seed"]
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
        if re.match(fr"{self.df_label}\d*$", assoc_name):
            if "11" not in new_cards:
                new_cards[random.randrange(len(new_cards))] = "11"
        
        # If there is at least one "_" prefix in the original MCD, prefix it to approximately
        # the same proportion of random "11" cards. Note that the new prefix should be stored
        # in its own node in the tree, but we don't bother to do that since the tree will immediately
        # be converted back to a string.
        if self.cards["11"] > 0:
            proba = self.card_prefixes["_"] / self.cards["11"]
            new_cards = [f"_{card}" if card == "11" and random.random() < proba else card for card in new_cards]
        
        # Same treatment for "/" prefix with "0N" and "1N" cards.
        if self.cards["0N"] + self.cards["1N"] > 0:
            proba = self.card_prefixes["/"] / (self.cards["0N"] + self.cards["1N"])
            new_cards = [f"/{card}" if card in ("0N", "1N") and random.random() < proba else card for card in new_cards]

        # Map the new cards to the card tokens
        for (card_token, new_card) in zip(card_tokens, new_cards):
            card_token.value = new_card


def run(source, params):
    tree = parse_source(source)
    card_prefixes = Counter(node.children[0].value for node in tree.find_data("card_prefix"))
    cards = Counter(node.children[0].value for node in tree.find_data("card"))
    visitor = CardRandomizer(card_prefixes, cards, params)
    visitor.visit(tree)
    return reconstruct_source(tree)
