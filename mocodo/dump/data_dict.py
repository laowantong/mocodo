__import__("sys").path[0:0] = ["."]

from ..parse_mcd import Visitor
from ..tools.parser_tools import parse_source

FILENAME_SUFFIX = "_data_dict.md"

class AttributeListExtractor(Visitor):
    def __init__(self):
        self.attributes = []
        self.data_type_count = 0
    
    def attr(self, tree):
        self.attributes.append((tree.children[0].value, None))
    
    def data_type(self, tree):
        self.data_type_count += 1
        self.attributes[-1] = (self.attributes[-1][0], tree.children[1].value)

def run(source, common):
    tree = parse_source(source)
    extractor = AttributeListExtractor()
    extractor.visit(tree)
    attributes = sorted(extractor.attributes)
    result = []
    if extractor.data_type_count < len(attributes):
        for (attr, data_type) in attributes:
            if data_type is None:
                result.append(f"- {attr}")
            else:
                result.append(f"- {attr} : _{data_type}_")
    else:
        result.append("| Attribut | Informations |")
        result.append("|:---|:---|")
        for (attr, data_type) in attributes:
            result.append(f"| {attr} | {data_type} |")
    return "\n".join(result)
