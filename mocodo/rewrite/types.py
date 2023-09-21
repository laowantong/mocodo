from pathlib import Path
import re

from ..parse_mcd import Visitor, Token
from ..tools.parser_tools import first_child, parse_source, reconstruct_source
from ..tools.string_tools import ascii, snake

class CreateTypePlaceholder(Visitor):

    def typed_attr(self, tree):
        if first_child(tree, "datatype"):
            return
        name_token = first_child(tree, "attr")
        if not name_token:
            return
        name_token.value += " []"

def create_type_placeholders(source):
    visitor = CreateTypePlaceholder()
    tree = parse_source(source)
    visitor.visit(tree)
    return reconstruct_source(tree)

def read_default_datatypes(resource_dir, language="en"):
    path = Path(resource_dir, f"default_datatypes_{language}.tsv")
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        yield tuple(fields[:2])

class GuessType(Visitor):

    def __init__(self, guessing_suffix, params):
        # Example: -r guess:types=? will complete all guessed types with a question mark.
        resource_dir = Path(params["script_directory"], "resources")
        self.field_types = dict(read_default_datatypes(resource_dir)) # English always used as fallback
        language = params.get("language", "en")
        if language != "en":
            self.field_types.update(read_default_datatypes(resource_dir, language))
        # Convert the dict to a list of tuples, and sort them by decreasing length
        # so that the longest match is found first.
        self.field_types = sorted(self.field_types.items(), key=lambda x: -len(x[0]))
        # Precompile the regexes
        self.field_types = [(re.compile(k).search, v) for (k, v) in self.field_types]
        self.guessing_suffix = guessing_suffix or ""

    def typed_attr(self, tree):
        a = list(tree.find_data("datatype"))
        if a and "".join(a[0].children)[2:-1]:
            return # already typed
        attr = first_child(tree, "attr")
        if attr == "":
            return
        needle = snake(ascii(attr)).replace("_", " ").lower()
        for (found, datatype) in self.field_types:
            if found(needle):
                datatype = f"{datatype}{self.guessing_suffix}"
                break
        else:
            datatype = ""
        tree.children = [Token("MOCK", f"{attr.value} [{datatype}]", line=attr.line, column=attr.column)]


def guess_types(source, subsubarg, params):
    visitor = GuessType(subsubarg, params)
    tree = parse_source(source)
    visitor.visit(tree)
    return reconstruct_source(tree)
