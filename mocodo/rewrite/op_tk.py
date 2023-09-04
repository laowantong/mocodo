import random

__import__("sys").path[0:0] = ["."]

from ..parse_mcd import Transformer
from ..tools.parser_tools import transform_source
from ..tools.string_tools import ascii, camel, snake
from .cards import fix_card, randomize_cards
from .types import FIELD_TYPES, create_type_placeholders, guess_types
from .obfuscate import obfuscator_factory
from .arrows import create_df_arrows
from ..mocodo_error import MocodoError

ELEMENT_TO_TOKENS = {
    "arrows": ["leg_arrow"],
    "attrs": ["attr"],
    "boxes": ["box_name"],
    "cards": ["card"],
    "constraint_notes": ["constraint_note"],
    "labels": ["box_name", "attr"],
    "texts": ["box_name", "attr", "leg_note", "constraint_note"],
    "leg_notes": ["leg_note"],
    "notes": ["leg_note", "constraint_note"],
    "types": ["data_type"],
}

GENERAL_OPERATIONS = { # operations that can be applied to any token
    "ascii": ascii,
    "camel": camel,
    "capitalize": lambda x: x.capitalize(),
    "casefold": lambda x: x.casefold(),
    "echo": lambda x: x,
    "lower": lambda x: x.lower(),
    "snake": snake,
    "swapcase": lambda x: x.swapcase(),
    "title": lambda x: x.title(),
    "upper": lambda x: x.upper(),
}


class Mapper(Transformer):

    def __init__(self, op_name, pre_token, subsubarg, params):
        tokens = ELEMENT_TO_TOKENS[pre_token]
        op = GENERAL_OPERATIONS.get(op_name)
        if op is None: # op_tk operations with limited applicability
            if op_name == "randomize" and pre_token == "types":
                pool = list(FIELD_TYPES["en"].values())
                op = lambda x: x or random.choice(pool)
            elif op_name == "delete" and pre_token in ("attrs", "notes", "leg_notes", "constraint_notes", "arrows", "types"):
                op = lambda _: ""
            elif op_name == "delete" and pre_token == "cards":
                op = lambda _: "XX"
            elif op_name == "fix" and pre_token == "cards":
                op = fix_card
            elif op_name == "randomize" and pre_token in ("labels", "texts", "boxes", "attrs", "notes", "leg_notes", "constraint_notes"):
                op = obfuscator_factory(subsubarg, params)
            else:
                raise MocodoError(24, _('Operation {op_name} cannot be applied to {pre_token}.').format(op_name=op_name, pre_token=pre_token))
        update_tree = lambda tree: tree[0].update(value=op(tree[0].value))
        for token in tokens:
            setattr(self, token, update_tree)


def run(source, op_name, subargs, params, **kargs):
    for (pre_token, subsubarg) in subargs.items():
        # filter special non-op_tk operations
        if op_name == "create" and pre_token == "types":
            source = create_type_placeholders(source)
        elif op_name == "guess" and pre_token == "types":
            source = guess_types(source, subsubarg, params)
        elif op_name == "randomize" and pre_token == "cards":
            source = randomize_cards(source, params)
        elif op_name == "create" and pre_token == "df_arrows":
            source = create_df_arrows(source, subsubarg)
        else: # apply a normal op_tk operation
            source = transform_source(source, Mapper(op_name, pre_token, subsubarg, params))
    return source
