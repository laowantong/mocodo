import re
from ..parse_mcd import Visitor
from ..tools.parser_tools import first_child, parse_source
from ..tools.string_tools import surrounds
from ..tools.various import first_missing_positive
    
class CreateCifs(Visitor):

    def __init__(self):
        self.candidates = set()
        self.existing = set()
        self.invisible_numbers = []

    def entity_clause(self, tree):
        ent_name = str(first_child(tree, "box_name"))
        m = re.match(r"(?i)invisible(\d+)$", ent_name)
        if m:
            self.invisible_numbers.append(int(m.group(1)))

    def assoc_clause(self, tree):
        legs = [node for node in tree.find_data("assoc_leg")]
        assoc_name = str(first_child(tree, "assoc_name_def").children[0])
        target_names = []
        entity_names = set()
        for leg in legs:
            entity_name = first_child(leg, "entity_name_ref").children[0].value
            entity_names.add(entity_name)
            if first_child(leg, "card_prefix") == "/":
                target_names.append(entity_name)
        for target_name in target_names:
            self.candidates.add((assoc_name, target_name, *sorted(entity_names - {target_name})))
    
    def constraint_clause(self, tree):
        if first_child(tree, "constraint_name").upper() != "CIF":
            return
        assoc_name = None
        target_name = None
        source_names = []
        for node in tree.find_data("constraint_target"):
            leg = first_child(node, "constraint_leg")
            box_name = first_child(node, "box_name_ref").children[0].value
            if surrounds(leg, ".."):
                if assoc_name is not None:
                    return
                assoc_name = box_name
            elif surrounds(leg, "->"):
                if target_name is not None:
                    return
                target_name = box_name
            elif leg == "" or surrounds(leg, "--"):
                source_names.append(box_name)
            else:
                return
        self.existing.add((assoc_name, target_name, *sorted(source_names)))
    
    def get_new_cifs(self, hidden_links_from_sources=False):
        self.new_cifs = self.candidates - self.existing
        if not self.new_cifs:
            return ""
        sep = ", " if hidden_links_from_sources else ", --"
        new_invisible_clauses = ["\n"]
        new_cif_clauses = [""]
        for (assoc_name, *entity_names) in sorted(self.new_cifs):
            n = first_missing_positive(self.invisible_numbers)
            self.invisible_numbers.append(n)
            new_invisible_clauses.append(f"-INVISIBLE_{n}, XX {entity_names[0]}, XX {entity_names[0]}")
            new_cif_clauses.append(f"(CIF) ..{assoc_name}, ->{sep.join(entity_names)}: INVISIBLE_{n}, INVISIBLE_{n}")
        if new_cif_clauses == [""]:
            return ""
        return "\n".join(new_invisible_clauses + new_cif_clauses)


def create_cifs(source, subsubarg):
    visitor = CreateCifs()
    tree = parse_source(source)
    visitor.visit(tree)
    return source + visitor.get_new_cifs(subsubarg == "light")
