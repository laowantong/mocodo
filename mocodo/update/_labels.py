from ..mocodo_error import subsubopt_error
from . import stand_for
from .op_tk import op_tk
from .obfuscate import obfuscator_factory


def run(source, subargs=None, params=None):
    subargs = subargs or {}
    params = params or {}
    for (subsubopt, subsubarg) in subargs.items():
        if stand_for(subsubopt, "obfuscate", "randomize"):
            obfuscate = obfuscator_factory(subsubarg, params)
            source = op_tk(source, "label", obfuscate)
        elif stand_for(subsubopt, "ascii", "camel", "capitalize", "casefold", "lower", "snake", "swapcase", "title", "upper"):
            source = op_tk(source, "label", subsubopt)
        else:
            raise subsubopt_error(subsubopt)
    return source
