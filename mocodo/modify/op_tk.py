import re
from unicodedata import combining, normalize

__import__("sys").path[0:0] = ["."]

from ..parse_mcd import Transformer
from ..parser_tools import transform_source

# One-liners to be used in the transformer

OPERATIONS = {
    None: lambda x: x,
    "upper": lambda x: x.upper(),
    "lower": lambda x: x.lower(),
    "title": lambda x: x.title(),
    "casefold": lambda x: x.casefold(),
    "capitalize": lambda x: x.capitalize(),
    "swapcase": lambda x: x.swapcase(),
    "sub": lambda x: "",
    "subXX": lambda x: "XX",
    "sub??": lambda x: "??",
}


# ASCII

LATIN = "ä  æ  ǽ  đ ð ƒ ħ ı ł ø ǿ ö  œ  ß  ŧ ü  Ä  Æ  Ǽ  Đ Ð Ƒ Ħ I Ł Ø Ǿ Ö  Œ  ẞ  Ŧ Ü "
ASCII = "ae ae ae d d f h i l o o oe oe ss t ue AE AE AE D D F H I L O O OE OE SS T UE"


def ascii(s, outliers=str.maketrans(dict(zip(LATIN.split(), ASCII.split())))):
    return "".join(c for c in normalize("NFD", s.translate(outliers)) if not combining(c))


OPERATIONS["ascii"] = ascii


# Camel case

def camel_repl(m):
    return f"{m[1].lower()}{m[2].upper()}{m[3].lower()}"


def camel(label):
    return re.sub(r"([^\W_]*)[\W_]+(.?)([^\W_]*)", camel_repl, label)


OPERATIONS["camel"] = camel


# Snake case

def split_camel_case(
        s,
        upper = lambda x: x.upper(),
        lower = lambda x: x.lower(),
    ):
    change_case = upper if s.isupper() else lower
    result = []
    previous_is_lower = False
    for c in s:
        if previous_is_lower and c.isupper():
            result.extend(["_", change_case(c)])
        elif not c.isalnum():
            result.append("_")
        else:
            result.append(change_case(c))
        previous_is_lower = c.islower()
    return "".join(result)

def compress_underscores(s):
    return re.sub(r"_+", "_", s.strip("_"))

def snake(label):
    return compress_underscores(split_camel_case(label))

OPERATIONS["snake"] = snake


# Actual transformer

class TokenRewriter(Transformer):
    def __init__(self, token, operation):
        self.operation = OPERATIONS[operation]
        if token.endswith("s"): # tolerance for the plural forms
            token = token[:-1]
        if token == "label":
            tokens = ["box_name", "attr", "leg_note"]
        elif token == "note":
            tokens = ["leg_note", "constraint_note"]
        else:
            tokens = [token]
        for token in tokens:
            setattr(self, token, self._modify)

    def _modify(self, tree):
        return tree[0].update(value=self.operation(tree[0].value))


def run(source, operation, token):
    return transform_source(source, TokenRewriter(token, operation))
