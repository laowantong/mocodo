from ..parse_mcd import Visitor
from ..tools.parser_tools import first_child, parse_source, reconstruct_source
from ..tools.string_tools import surrounds
    
class CreateCifs(Visitor):

    def __init__(self):
        self.candidates = set()
        self.existing = set()

    def assoc_clause(self, tree):
        legs = [node for node in tree.find_data("assoc_leg")]
        if len(legs) <= 2:
            return
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
        result = [] if self.existing else [""]
        sep = ", " if hidden_links_from_sources else ", --"
        for (assoc_name, *entity_names) in self.new_cifs:
            result.append(f"(CIF) ..{assoc_name}, ->{sep.join(entity_names)}")
        return "\n".join(result)


def create_cifs(source, subsubarg):
    visitor = CreateCifs()
    tree = parse_source(source)
    visitor.visit(tree)
    return source + visitor.get_new_cifs(subsubarg == "min")
