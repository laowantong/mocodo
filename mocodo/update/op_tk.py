__import__("sys").path[0:0] = ["."]

from ..parse_mcd import Transformer
from ..tools.parser_tools import transform_source
from ..tools.string_tools import ascii, camel, snake


class Mapper(Transformer):

    FIXED_OPERATIONS = {
        None: lambda x: x,
        "ascii": ascii,
        "camel": camel,
        "capitalize": lambda x: x.capitalize(),
        "casefold": lambda x: x.casefold(),
        "lower": lambda x: x.lower(),
        "snake": snake,
        "swapcase": lambda x: x.swapcase(),
        "title": lambda x: x.title(),
        "upper": lambda x: x.upper(),
    }

    def __init__(self, token, op_name_or_function):
        if token.endswith("s"): # tolerance for the plural forms
            token = token[:-1]
        if token == "label":
            tokens = ["box_name", "attr"]
        elif token == "note":
            tokens = ["leg_note", "constraint_note"]
        else:
            tokens = [token]
        op = self.FIXED_OPERATIONS.get(op_name_or_function, op_name_or_function)
        for token in tokens:
            setattr(
                self,
                token,
                lambda tree: tree[0].update(value=op(tree[0].value)),
            )


def op_tk(source, subopt, subsubopt):
    return transform_source(source, Mapper(subopt, subsubopt))
