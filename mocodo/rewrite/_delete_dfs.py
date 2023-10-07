from collections import defaultdict
import re
import sys

__import__("sys").path[0:0] = ["."]

from ..parse_mcd import Token, Visitor
from ..tools.parser_tools import parse_source, reconstruct_source, first_child, is_identifier


class SqueezerFirstPass(Visitor):
    """
    In the first pass, find out which entities E:
     1. are not suffixed by "+";
     2. have no attribute outside their identifier;
     3. appear only in associations of the form: [E]-*N-(A)-11-[E'] where E ≠ E'
    """
    def __init__(self, params):
        self.possible_entities = {} # { E1: [E1_id_1, E2_id_2], ... }
        self.rejected_entities = set()
        self.possible_associations = [] # [ (E1, A1, E'1, E'1_is_weak), ...]
        self.df_label = params["df"]

    def assoc_clause(self, tree):
        # Guard: ensure that the association is named DF
        assoc_name = first_child(tree, "assoc_name_def").children[0].value
        if assoc_name != self.df_label:
            return

        entity_names = [node.children[0].children[0] for node in tree.find_data("entity_name_ref")]

        # Guard: ensure that exactly one cardinality is 11
        cards = [node.children[0].value for node in tree.find_data("card")]
        if cards.count("11") != 1:
            self.rejected_entities.update(entity_names)
            return

        # Guard: ensure that the association is binary
        if len(cards) != 2:
            self.rejected_entities.update(entity_names)
            return

        # Store the names of E, A and E'
        legs = [node for node in tree.find_data("assoc_leg")]
        weaks = [first_child(leg, "card_prefix") == "_" for leg in legs]
        i = cards.index("11")
        self.rejected_entities.add(entity_names[i])
        self.possible_associations.append(
            (
                entity_names[1-i].value,
                assoc_name,
                entity_names[i].value,
                weaks[i]
            )
        )
    
    def entity_clause(self, tree):
        if first_child(tree, "box_def_prefix") == "+": # protected entity
            return
        ent_name = str(first_child(tree, "box_name"))
        attrs = []
        for (i, node) in enumerate(tree.find_data("entity_or_table_attr")):
            id_groups = str(first_child(node, "id_groups"))
            id_mark = str(first_child(node, "id_mark"))
            attr_label = str(first_child(node, "attr"))
            datatype = str(first_child(node, "datatype"))
            if attr_label == "":
                continue # ignore spacer attributes
            if not is_identifier(i, id_groups, id_mark):
                return
            attrs.append((attr_label, datatype))
        self.possible_entities[ent_name] = attrs
    
    def start(self, tree): # post-processing
        possible_entities = { e: attrs for (e, attrs) in self.possible_entities.items() if e not in self.rejected_entities}
        distinguished_entities = { t[0] for t in self.possible_associations }
        possible_entities = { e: attrs for (e, attrs) in possible_entities.items() if e in distinguished_entities }
        self.entities_to_delete = set(possible_entities)
        self.entities_to_complete = { e2: (is_weak, possible_entities[e1]) for (e1, _, e2, is_weak) in self.possible_associations if e1 in possible_entities}

class SqueezerSecondPass(Visitor):
    """
    In the second pass, delete the boxes to delete and complete the entities to complete.
    """
    def __init__(self, previous_visitor):
        self.entities_to_delete = previous_visitor.entities_to_delete
        self.entities_to_complete = previous_visitor.entities_to_complete

    def entity_clause(self, tree):
        token = first_child(tree, "box_name")
        ent_name = token.value
        if ent_name in self.entities_to_delete:
            token = tree.children[-1]
            tree.children = [Token("MOCK", ":\n", line=token.line, column=token.column)]
        elif ent_name in self.entities_to_complete:
            has_existing_attributes = bool(first_child(tree, "attr"))
            (is_weak, labels_and_types) = self.entities_to_complete[ent_name]
            attrs = []
            for (i, (attr_label, datatype)) in enumerate(labels_and_types):
                id_mark = ""
                if is_weak and (i > 0 or has_existing_attributes):
                    id_mark = "_"
                datatype = f" [{datatype}]" if datatype else ""
                attrs.append(id_mark + attr_label + datatype)
            token = tree.children[-1]
            separator = ", " if has_existing_attributes else " "
            token.value = f"{separator}{', '.join(attrs)}{token.value}"

    def assoc_clause(self, tree):
        entity_names = [node.children[0].children[0] for node in tree.find_data("entity_name_ref")]
        if self.entities_to_delete.intersection(entity_names):
            token = tree.children[-1]
            tree.children = [Token("MOCK", ":\n", line=token.line, column=token.column)]


def run(source, params, **kargs):
    tree = parse_source(source)
    visitor = SqueezerFirstPass(params)
    visitor.visit(tree)
    visitor = SqueezerSecondPass(visitor)
    visitor.visit(tree)
    source = f"\n\n{reconstruct_source(tree)}\n\n"
    source = re.sub(r"\n\n[:\s]*\n\n", "\n\n", source)
    return source.strip("\n")
