import re

__import__("sys").path[0:0] = ["."]

from ._crow import Crow
from ..tools.parser_tools import parse_source
from ..rewrite import (
    op_tk,
    _drain as drain,
    _explode as explode,
    _split as split,
)
from ..tools.string_tools import rstrip_digit

SUFFIX = "_crows_foot_erd.mmd"

LEFT_CARD = {
    "01": "|o",
    "0N": "}o",
    "11": "||",
    "1N": "}|",
}
RIGHT_CARD = {
    "01": "o|",
    "0N": "o{",
    "11": "||",
    "1N": "|{",
}


def sanitize_type(s):
    # In Mermaid syntax, the type values must begin with an alphabetic character
    # and may contain digits, hyphens, underscores, parentheses and square brackets.
    # This seems a too specific operation to be offered by op_tk.
    s = s.replace(
        ",", "-"
    )  # as long as https://github.com/mermaid-js/mermaid/issues/1546 is not fixed
    s = re.sub(r"[^-_0-9A-Za-z()[\]]", "_", s)
    s = re.sub(r"__+", "_", s)
    s = s.strip("_")
    return s


class CrowMmd(Crow):
    def get_text(self):
        result = []
        result.append("erDiagram")
        for (name, has_id, attrs) in self.tables.values():
            result.append(f"  {name} {{")
            for (data_type, attr, is_id) in attrs:
                data_type = sanitize_type(data_type) if data_type else "TYPE"
                pk = " PK" if is_id else ""
                result.append(f"    {data_type} {attr}{pk}")
            result.append(f"  }}")
        for (ent_1, card_1, kind, card_2, ent_2, assoc_name) in self.links:
            ent_1 = rstrip_digit(ent_1)
            ent_2 = rstrip_digit(ent_2)
            card_1 = LEFT_CARD.get(card_1, "}|")
            card_2 = RIGHT_CARD.get(card_2, "|{")
            result.append(f"  {ent_1} {card_1}{kind}{card_2} {ent_2}: {assoc_name}")
        return "\n".join(result)


def run(source, subargs, common=None):
    source = op_tk.run(source, "labels", {"ascii": 1, "snake": 1}, common.params)
    source = drain.run(source)
    source = split.run(source)
    source = explode.run(source, {"arity": "2.5", "weak": True})
    tree = parse_source(source)
    extractor = CrowMmd()
    extractor.visit(tree)
    result = extractor.get_text()
    return result
