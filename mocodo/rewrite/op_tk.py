import contextlib
from pathlib import Path
import random
import re

__import__("sys").path[0:0] = ["."]

from ..parse_mcd import Transformer
from ..tools.parser_tools import transform_source
from ..tools.string_tools import ascii, camel, snake, pascal, TRUNCATE_DEFAULT_SIZE
from ..mocodo_error import MocodoError
from .cards import fix_card, infer_dfs, infer_roles
from .types import read_default_datatypes, create_type_placeholders, guess_types
from .obfuscate import obfuscator_factory
from .arrows import create_df_arrows
from .constraints import create_cifs

ELEMENT_TO_TOKENS = {
    "arrows": ["leg_arrow"],
    "attrs": ["attr"],
    "boxes": ["box_name"],
    "card_prefixes": ["card_prefix"],
    "cards": ["card"],
    "roles": ["leg_note"],
    "leg_notes": ["leg_note"],
    "constraint_notes": ["constraint_note"],
    "labels": ["box_name", "attr"],
    "texts": ["box_name", "attr", "leg_note", "constraint_note"],
    "notes": ["leg_note", "constraint_note"],
    "types": ["datatype"],
}

GENERAL_OPERATIONS = { # operations that can be applied to any token
    "ascii": ascii,
    "camel": camel,
    "capitalize": lambda x: x.capitalize(),
    "casefold": lambda x: x.casefold(),
    "echo": lambda x: x,
    "lower": lambda x: x.lower(),
    "pascal": pascal,
    "snake": snake,
    "swapcase": lambda x: x.swapcase(),
    "title": lambda x: x.title(),
    "upper": lambda x: x.upper(),
}


class Mapper(Transformer):

    def __init__(self, op_name, pre_token, subsubarg, params):
        tokens = ELEMENT_TO_TOKENS[pre_token]
        op = GENERAL_OPERATIONS.get(op_name)
        if op is None: # op_tk operations with limited applicability and/or using a subsubarg
            if op_name == "randomize" and pre_token == "types":
                resource_dir = Path(params["script_directory"], "resources")
                pool = list(dict(read_default_datatypes(resource_dir)).values())
                op = lambda _: random.choice(pool)
            elif op_name == "delete" and pre_token in ("attrs", "notes", "roles", "constraint_notes", "arrows", "types", "card_prefixes"):
                op = lambda _: ""
            elif op_name == "delete" and pre_token == "cards":
                op = lambda _: "XX"
            elif op_name == "fix" and pre_token == "cards":
                op = fix_card
            elif op_name == "randomize" and pre_token in ("labels", "texts", "boxes", "attrs", "notes", "roles", "constraint_notes"):
                op = obfuscator_factory(subsubarg, params)
            elif op_name == "truncate":
                truncate_size = TRUNCATE_DEFAULT_SIZE
                if subsubarg and subsubarg.isdigit():
                    truncate_size = int(subsubarg) or truncate_size
                op = lambda x: x[:truncate_size]
            elif op_name == "slice":
                slice_start = slice_stop = None
                if subsubarg:
                    with contextlib.suppress(ValueError):
                        slice_start = int(subsubarg.partition(":")[0])
                    with contextlib.suppress(ValueError):
                        slice_stop = int(subsubarg.partition(":")[2])
                op = lambda x: x[slice_start:slice_stop]
            elif op_name == "replace":
                (substring, __, repl) = subsubarg.partition("/")
                op = lambda x: x.replace(substring, repl)
            elif op_name == "suffix":
                op = lambda x: f"{x}{subsubarg}"
            elif op_name == "prefix":
                op = lambda x: f"{subsubarg}{x}"
            else:
                raise MocodoError(24, _('Operation "{op_name}" cannot be applied to "{pre_token}".').format(op_name=op_name, pre_token=pre_token))
        update_first_child = lambda tree: tree[0].update(value=op(tree[0].value))
        for token in tokens:
            setattr(self, token, update_first_child)


def run(source, op_name, subargs, params, **kargs):
    if op_name == "randomize" and not subargs:
        subargs = {"labels": ""} # used for obfuscation
    elif op_name == "delete" and not subargs:
        subargs = dict.fromkeys("types notes attrs cards".split(), "")
    for (pre_token, subsubarg) in subargs.items():
        # filter special non-op_tk operations
        if op_name == "create" and pre_token == "types":
            source = create_type_placeholders(source, subsubarg) if subsubarg is not None else guess_types(source, params)
        elif op_name == "create" and pre_token == "df_arrows":
            source = create_df_arrows(source, subsubarg)
        elif op_name == "create" and re.match("(?i)dfs?$", pre_token):
            source = infer_dfs(source, params["df"])
        elif op_name == "create" and pre_token == "roles":
            source = infer_roles(source)
        elif op_name == "create" and re.match("(?i)cifs?$", pre_token):
            source = create_cifs(source, subsubarg)
        else: # apply a normal op_tk operation
            source = transform_source(source, Mapper(op_name, pre_token, subsubarg, params))
        if op_name == "delete":
            # After a delete operation, remove any [] that may have been left behind
            # (it's too tedious to remove them from the AST, and it's not worth it).
            source = re.sub(r" *\[\]", " ", source)
    return source
