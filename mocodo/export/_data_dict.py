__import__("sys").path[0:0] = ["."]

import re
from ..parse_mcd import Transformer
from ..tools.parser_tools import parse_source, first_child
from ..mocodo_error import subsubopt_error

DEFAULT_COLUMN_NAMES = {
    "en": {
        "label": "Label",
        "type": "Type",
        "box": "Box",
    },
    "fr": {
        "label": "Libellé",
        "type": "Type",
        "box": "Boîte",
    },
}

class AttributeListExtractor(Transformer): # depth-first, post-order
    def __init__(self):
        self.boxes = {}
        self.typed_attribute_accumulator = []
        self.assoc_clause = self._box_clause
        self.entity_clause = self._box_clause
    
    def _box_clause(self, tree):
        # Associate the box name with the accumulated list of attributes
        box_name = first_child(tree[0], "box_name").value
        self.boxes[box_name] = self.typed_attribute_accumulator[:]
        self.typed_attribute_accumulator = []
    
    def attr(self, tree):
        # Accumulate a couple (attribute name, data type placeholder)
        self.typed_attribute_accumulator.append((tree[0].value, ""))
    
    def data_type(self, tree):
        # Replace the last data type placeholder with the actual data type
        (name, _) = self.typed_attribute_accumulator.pop()
        self.typed_attribute_accumulator.append((name, tree[1].value))
    
    def finalize(self, common, subargs):
        language = common.params["language"]
        actual_colons = {}
        for kind in list(subargs):
            m = re.match(r"^([*_`]*)(.+)\1$", kind) 
            if m[2] in ("label", "type", "box"):
                actual_colons[m[2]] = m[1]
            subargs[m[2]] = subargs.pop(kind)
        if not actual_colons:
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
            for (attr, data_type) in attributes:
                d = {"box": box, "label": attr, "type": data_type}
                row = [d[p] for p in self.projectors]
                self.rows.append(row)
        self.md_tags = [actual_colons[p] for p in self.projectors]
        self.rows.sort()
    
    def get_tsv(self):
        result = []
        if len(self.header) > 1:
            result.append("\t".join(self.header))
        result.extend(map("\t".join, self.rows))
        return "\n".join(result)
    
    def add_md_tags(self, row):
        return " | ".join(f"{tag}{cell}{tag}" for (tag, cell) in zip(self.md_tags, row))

    def get_markdown(self):
        result = []
        if len(self.header) > 1: # output a table only if there are at least two columns
            result.append("| " + " | ".join(self.header) + " |")
            result.append("|:---" * len(self.header) + "|")
            previous_leftmost = None
            for row in self.rows:
                if row[0] == previous_leftmost:
                    row[0] = '"'
                else:
                    previous_leftmost = row[0]
                result.append(f"| {self.add_md_tags(row)} |")
        else: # otherwise, output a list
            result.extend(f"- {self.add_md_tags(row)}" for row in self.rows)
        return "\n".join(result)

def run(source, subargs=None, common=None):
    tree = parse_source(source)
    extractor = AttributeListExtractor()
    extractor.transform(tree)
    extractor.finalize(common, subargs)
    result = {"stem_suffix": "data_dict"}
    if "md" in subargs or "markdown" in subargs:
        result["text"] = extractor.get_markdown()
        result["extension"] = "md"
        result["displayable"] = True
    else: # "tsv" is the default
        result["text"] = extractor.get_tsv()
        result["extension"] = "tsv"
        result["displayable"] = False
    return result

# --export data_dict:type,box,label="libellé de l'attribut",tsv