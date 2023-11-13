from pathlib import Path
import re

from ..parse_mcd import Visitor
from ..tools.parser_tools import first_child, parse_source, reconstruct_source
from ..tools.string_tools import ascii, snake, strip_surrounds

class CreateTypePlaceholder(Visitor):

    def __init__(self, subsubarg):
        self.default = strip_surrounds(subsubarg, "[]")

    def typed_attr(self, tree):
        if len(tree.children) == 1:
            tree.children[0].children[0].value += f" [{self.default}]"

def create_type_placeholders(source, subsubarg):
    visitor = CreateTypePlaceholder(subsubarg)
    tree = parse_source(source)
    visitor.visit(tree)
    return reconstruct_source(tree)

def read_default_datatypes(resource_dir, language="en"):
    path = Path(resource_dir, f"default_datatypes_{language}.tsv")
    if not path.exists():
        return
    for line in path.read_text(encoding="utf8").splitlines():
        fields = line.split("\t")
        if len(fields) < 2:
            continue
        yield tuple(fields[:2])

class GuessType(Visitor):

    def __init__(self,params):
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

    def typed_attr(self, tree):
        n = len(tree.children)
        # Possible lengths of the children list:
        # 0: empty attribute
        # 1: attribute without datatype
        # 3: attribute with empty datatype
        # 4: attribute with non-empty datatype
        if n not in (1, 3):
            return
        attr = first_child(tree, "attr")
        needle = snake(ascii(attr)).replace("_", " ").lower()
        for (found, datatype) in self.field_types:
            if found(needle):
                break
        else:
            datatype = ""
        if n == 1: # concatenate to the attribute label the datatype between brackets
            tree.children[0].children[0].value += f" [{datatype}]"
        else: # insert the datatype between brackets
            tree.children[1].value += datatype


def guess_types(source, params):
    visitor = GuessType(params)
    tree = parse_source(source)
    visitor.visit(tree)
    return reconstruct_source(tree)
