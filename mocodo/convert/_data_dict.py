__import__("sys").path[0:0] = ["."]

import re

from ..tools.string_tools import markdown_table
from ..parse_mcd import Transformer
from ..tools.parser_tools import parse_source, first_child
from ..mocodo_error import subsubopt_error

DEFAULT_COLUMN_NAMES = {
    "en": {
        "label": "Label of the attribute",
        "type": "Type",
        "box": "Entity or relationship",
    },
    "fr": {
        "label": "Libellé de l'attribut",
        "type": "Type",
        "box": "Entité ou association",
    },
}

class AttributeListExtractor(Transformer): # depth-first, post-order
    def __init__(self):
        self.boxes = {}
        self.typed_attribute_accumulator = []
        self.assoc_clause = self._box_clause
        self.entity_clause = self._box_clause
    
    def _box_clause(self, children):
        # Associate the box name with the accumulated list of attributes
        box_def_prefix = first_child(children[0], "box_def_prefix")
        if box_def_prefix != "-":
            if not box_def_prefix:
                box_name = first_child(children[0], "box_name")
            else:
                box_name = first_child(children[1], "box_name")
            self.boxes[box_name] = self.typed_attribute_accumulator[:]
        self.typed_attribute_accumulator = []
    
    def attr(self, children):
        # Accumulate a couple (attribute name, data type placeholder)
        self.typed_attribute_accumulator.append((children[0].value, ""))
    
    def datatype(self, children):
        # Replace the last data type placeholder with the actual data type
        (name, _) = self.typed_attribute_accumulator.pop()
        self.typed_attribute_accumulator.append((name, children[0].value))
    
    def finalize(self, common, subargs):
        language = common.params["language"]
        actual_colons = {}
        for kind in list(subargs):
            m = re.match(r"^([*_`]*)(.+)\1$", kind) 
            if m[2] in ("label", "type", "box"):
                actual_colons[m[2]] = m[1]
            subargs[m[2]] = subargs.pop(kind)
        if not actual_colons:
            actual_colons["box"] = subargs["box"] = ""
            actual_colons["label"] = subargs["label"] = ""
            actual_colons["type"] = subargs["type"] = ""
        self.header = []
        self.projectors = []
        for (kind, col_name) in subargs.items():
            if kind in ("tsv", "md", "markdown"):
                continue
            if kind not in actual_colons:
                raise subsubopt_error(kind)
            self.header.append(col_name or DEFAULT_COLUMN_NAMES[language][kind])
            self.projectors.append(kind)
        self.rows = []
        for (box, attributes) in self.boxes.items():
            for (attr, datatype) in attributes:
                d = {"box": box, "label": attr, "type": datatype}
                row = [d[p] for p in self.projectors]
                self.rows.append(row)
        self.md_tags = [actual_colons[p] for p in self.projectors]
        self.rows.sort()
        return len(actual_colons)
    
    def get_tsv(self):
        result = []
        if len(self.header) > 1:
            result.append("\t".join(self.header))
        result.extend(map("\t".join, self.rows))
        return "\n".join(result)
    
    def get_markdown(self):
        if len(self.header) > 1: # output a table only if there are at least two columns
            result = []
            previous_leftmost = None
            for row in [self.header] + self.rows:
                if row[0] == previous_leftmost:
                    row[0] = '"'
                else:
                    previous_leftmost = row[0]
                result.append(f"{tag}{cell}{tag}" for (tag, cell) in zip(self.md_tags, row))
            return markdown_table(result)
        else: # otherwise, output a list
            return "\n".join([f"- {self.md_tags[0]}{row[0]}{self.md_tags[0]}" for row in self.rows])

def run(source, subargs=None, common=None):
    tree = parse_source(source)
    extractor = AttributeListExtractor()
    extractor.transform(tree)
    column_count = extractor.finalize(common, subargs)
    if "tsv" in subargs:
        return {
            "stem_suffix": f"_data_dict_{column_count}",
            "text": extractor.get_tsv(),
            "extension": "tsv",
            "to_defer": False,
            "highlight": "tsv",
        }
    else: # Markdown is the default
        return {
            "stem_suffix": f"_data_dict_{column_count}",
            "text": extractor.get_markdown(),
            "extension": "md",
            "to_defer": False,
            "highlight": "markdown",
        }
