from collections import Counter

__import__("sys").path[0:0] = ["."]

from ..parse_mcd import Visitor
from ..tools.parser_tools import first_child, parse_source
from ..modify import drain, explode, split
from ..tools.graphviz_tools import create_name_to_index, minify
from ..tools.string_tools import wrap_label, rstrip_digit

SUFFIX = "_chen_erd.gv"

# Legends
# False: normal cardinality prefix
# True: weak cardinality prefix (i.e., _11)
# "SE": normal entity (i.e., simple box)
# "WE": weak entity (i.e., double box)
# "SA": normal association (i.e., simple losange)
# "WA": weak association (i.e., double losange)
# "-" : partial participation (i.e., simple line)
# "=" : total participation (i.e., double line)
MIN_MAX_TO_CHEN = {
    (False, "01", False, "01"): ("SE", "1", "-", "SA", "-", "1", "SE"),
    (False, "01", False, "11"): ("SE", "1", "-", "SA", "=", "1", "SE"),
    (False, "01", True, "11"): ("SE", "1", "-", "WA", "=", "1", "WE"),
    (False, "01", False, "0N"): ("SE", "N", "-", "SA", "-", "1", "SE"),
    (False, "01", False, "1N"): ("SE", "N", "-", "SA", "=", "1", "SE"),
    (False, "11", False, "01"): ("SE", "1", "=", "SA", "-", "1", "SE"),
    (False, "11", False, "11"): ("SE", "1", "=", "SA", "=", "1", "SE"),
    (False, "11", True, "11"): ("SE", "1", "=", "WA", "=", "1", "WE"),
    (False, "11", False, "0N"): ("SE", "N", "=", "SA", "-", "1", "SE"),
    (False, "11", False, "1N"): ("SE", "N", "=", "SA", "=", "1", "SE"),
    (True, "11", False, "01"): ("WE", "1", "=", "WA", "-", "1", "SE"),
    (True, "11", False, "11"): ("WE", "1", "=", "WA", "=", "1", "SE"),
    (True, "11", True, "11"): ("WE", "1", "=", "WA", "=", "1", "WE"),
    (True, "11", False, "0N"): ("WE", "N", "=", "WA", "-", "1", "SE"),
    (True, "11", False, "1N"): ("WE", "N", "=", "WA", "=", "1", "SE"),
    (False, "0N", False, "01"): ("SE", "1", "-", "SA", "-", "N", "SE"),
    (False, "0N", False, "11"): ("SE", "1", "-", "SA", "=", "N", "SE"),
    (False, "0N", True, "11"): ("SE", "1", "-", "WA", "=", "N", "WE"),
    (False, "0N", False, "0N"): ("SE", "M", "-", "SA", "-", "N", "SE"),
    (False, "0N", False, "1N"): ("SE", "M", "-", "SA", "=", "N", "SE"),
    (False, "1N", False, "01"): ("SE", "1", "=", "SA", "-", "N", "SE"),
    (False, "1N", False, "11"): ("SE", "1", "=", "SA", "=", "N", "SE"),
    (False, "1N", True, "11"): ("SE", "1", "=", "WA", "=", "N", "WE"),
    (False, "1N", False, "0N"): ("SE", "M", "=", "SA", "-", "N", "SE"),
    (False, "1N", False, "1N"): ("SE", "M", "=", "SA", "=", "N", "SE"),
}


class Chen(Visitor):
    def __init__(self):
        self.name_to_index = create_name_to_index()
        # Entities and their attributes
        self.entity_nodes = []
        self.weak_box_indexes = set()
        self.strengthening_leg_count = Counter()
        self.ent_attr_nodes = []
        self.ent_key_attr_nodes = []
        self.ent_attr_edges = []
        self.not_gerund_nodes = set()
        # Associations and their attributes
        self.rel_nodes = []
        self.rel_attr_nodes = []
        self.rel_attr_edges = []
        # Legs with their participation
        self.partial_edges = []
        self.total_edges = []

    def entity_or_table_attr(self, tree):
        attr = first_child(tree, "attr")
        id_mark = int(bool(first_child(tree, "id_mark")))
        tree.children = [(id_mark, attr)]
    
    def entity_clause(self, tree):
        ent_name = first_child(tree, "box_name")
        ent_index = self.name_to_index(f"ent_{ent_name}")
        ent_name = rstrip_digit(ent_name)
        self.entity_nodes.append((ent_index, ent_name))
        for (i, node) in enumerate(tree.find_data("entity_or_table_attr")):
            (id_mark, attr) = node.children[0]
            attr_index = self.name_to_index(f"{ent_index}_{attr}")
            if (not id_mark and i == 0) or (id_mark and i != 0):
                self.ent_key_attr_nodes.append((attr_index, attr, ent_index))
            else:
                self.ent_attr_nodes.append((attr_index, attr))
            self.ent_attr_edges.append((ent_index, attr_index))
    
    def assoc_clause(self, tree):
        legs = [node for node in tree.find_data("assoc_leg")]
        assert len(legs) == 2 # The semantics of n-ary relationships is not supported
        # Accumulate the association as a new relationship
        assoc_name = first_child(tree, "assoc_name_def").children[0]
        assoc_index = self.name_to_index(f"assoc_{assoc_name}")
        assoc_name = rstrip_digit(assoc_name)
        self.rel_nodes.append((assoc_index, assoc_name))
        # Convert "look here" notation to "look across"
        (card_1, card_2) = [node.children[0].value for node in tree.find_data("card")]
        (w1, w2) = [first_child(leg, "card_prefix") == "_" for leg in legs]
        (e1, c1, p1, a, p2, c2, e2) = MIN_MAX_TO_CHEN[(w1, card_1, w2, card_2)]
        if a == "WA": # the association has a strengthening leg
            self.weak_box_indexes.add(assoc_index)
        (ent_name_1, ent_name_2) = [first_child(leg, "entity_name_ref").children[0] for leg in legs]
        for (e, ent_name, p, edge_label, w) in ((e1, ent_name_1, p1, c1, w1), (e2, ent_name_2, p2, c2, w2)):
            ent_index = self.name_to_index(f"ent_{ent_name}")
            participants = self.partial_edges if p == "-" else self.total_edges
            participants.append((ent_index, assoc_index, edge_label))
            if e == "WE": # the entity is distinguished by a _11
                self.weak_box_indexes.add(ent_index)
                self.strengthening_leg_count[ent_index] += 1
            else: # we are sure that it is not an associative entity
                self.not_gerund_nodes.add(ent_index)
        # Attributes
        for node in tree.find_data("attr"):
            attr = node.children[0]
            attr_index = self.name_to_index(f"{ent_index}_{attr}")
            self.rel_attr_nodes.append((attr_index, attr))
            self.rel_attr_edges.append((assoc_index, attr_index))
    
    def start(self, tree):
        # Since the traversal is depth-first, this is in fact a post-treatment
        for (ent_index, strengthening_leg_count) in self.strengthening_leg_count.items():
            if strengthening_leg_count < 2:
                self.not_gerund_nodes.add(ent_index)

    def get_graphviz(self, common):
        style = common.load_style()
        acc = []
        acc.append(f'graph{{')
        acc.append(f'  layout=fdp')
        acc.append(f'  bgcolor="{style["background_color"]}"')
        acc.append(f'  start={common.params["seed"]}')
        acc.append(f'  nodesep=0.5') # increase spacing between multiedges
        acc.append(f'  sep=0.1') # margin to leave around nodes when removing node overlap

        acc.append(f'\n  // Entities')
        acc.append(f'  node [')
        acc.append(f'    shape=box')
        acc.append(f'    margin=0.2')
        acc.append(f'    style=filled')
        acc.append(f'    penwidth={style["box_stroke_depth"]}')
        acc.append(f'    color="{style["entity_stroke_color"]}"')
        acc.append(f'    fillcolor="{style["entity_cartouche_color"]}"')
        acc.append(f'    fontcolor="{style["entity_cartouche_text_color"]}"')
        acc.append(f'    fontname="{style["entity_cartouche_font"]["family"]}"')
        acc.append(f'    fontsize={style["entity_cartouche_font"]["size"]}')
        acc.append(f'  ]')
        for (index, name) in self.entity_nodes:
            name = "\\n".join(wrap_label(name))
            if index in self.not_gerund_nodes:
                if index in self.weak_box_indexes:
                    acc.append(f'  {index} [label="{name}",peripheries=2]')
                else:
                    acc.append(f'  {index} [label="{name}"]')
        
        acc.append(f'\n  // Associative entities')
        for (index, name) in self.entity_nodes:
            name = "\\n".join(wrap_label(name))
            if index not in self.not_gerund_nodes:
                acc.append(f'  {index} [label="{name}",shape=Mdiamond]')

        acc.append(f'\n  // Normal entity attributes')
        acc.append(f'  node [')
        acc.append(f'    shape=oval')
        acc.append(f'    margin=0.1')
        acc.append(f'    penwidth={style["box_stroke_depth"]}')
        acc.append(f'    color="{style["entity_stroke_color"]}"')
        acc.append(f'    fillcolor="{style["entity_color"]}"')
        acc.append(f'    fontcolor="{style["entity_attribute_text_color"]}"')
        acc.append(f'    fontname="{style["entity_attribute_font"]["family"]}"')
        acc.append(f'    fontsize={style["entity_attribute_font"]["size"]}')
        acc.append(f'  ]')
        for (index, name) in self.ent_attr_nodes:
            name = "\\n".join(wrap_label(name))
            acc.append(f'  {index} [label="{name}"]')
        
        acc.append(f'\n  // Weak and strong entity attributes')
        for (index, name, ent_index) in self.ent_key_attr_nodes:
            name = "<br/>".join(wrap_label(name))
            if ent_index in self.weak_box_indexes:
                acc.append(f'  {index} [label=<<u>{name}</u>> style="dashed,filled"]')
            else:
                acc.append(f'  {index} [label=<<u>{name}</u>>]')
        
        acc.append(f'\n  // Relationship attributes')
        acc.append(f'  node [')
        acc.append(f'    color="{style["association_stroke_color"]}"')
        acc.append(f'    fillcolor="{style["association_color"]}"')
        acc.append(f'    fontcolor="{style["association_attribute_text_color"]}"')
        acc.append(f'    fontname="{style["association_attribute_font"]["family"]}"')
        acc.append(f'    fontsize={style["association_attribute_font"]["size"]}')
        acc.append(f'  ]')
        for (index, name) in self.rel_attr_nodes:
            name = "\\n".join(wrap_label(name))
            acc.append(f'  {index} [label="{name}"]')

        acc.append(f'\n  // Relationships')
        acc.append(f'  node [')
        acc.append(f'    shape=diamond')
        acc.append(f'    margin=0.05')
        acc.append(f'    penwidth={style["box_stroke_depth"]}')
        acc.append(f'    color="{style["association_stroke_color"]}"')
        acc.append(f'    fillcolor="{style["association_cartouche_color"]}"')
        acc.append(f'    fontcolor="{style["association_cartouche_text_color"]}"')
        acc.append(f'    fontname="{style["association_cartouche_font"]["family"]}"')
        acc.append(f'    fontsize={style["association_cartouche_font"]["size"]}')
        acc.append(f'  ]')
        for (index, name) in self.rel_nodes:
            name = "\\n".join(wrap_label(name))
            if index in self.weak_box_indexes:
                acc.append(f'  {index} [label="{name}",peripheries=2]')
            else:
                acc.append(f'  {index} [label="{name}"]')

        acc.append(f'\n  // Edges between entities and attributes')
        acc.append(f'  edge [')
        acc.append(f'    penwidth={style["box_stroke_depth"]}')
        acc.append(f'    color="{style["entity_stroke_color"]}"')
        acc.append(f'  ]')
        for (ent_index, attr_index) in sorted(self.ent_attr_edges):
            acc.append(f'  {ent_index} -- {attr_index}')

        acc.append(f'\n  // Edges between relationships and attributes')
        acc.append(f'  edge [color="{style["association_stroke_color"]}"]')
        for (ent_index, attr_index) in sorted(self.rel_attr_edges):
            acc.append(f'  {ent_index} -- {attr_index}')

        acc.append(f'\n  // Edges between entities and relationships: partial participation')
        acc.append(f'  edge [')
        acc.append(f'    penwidth={style["leg_stroke_depth"]}')
        acc.append(f'    color="{style["leg_stroke_color"]}"')
        acc.append(f'    fontcolor="{style["card_text_color"]}"')
        acc.append(f'    fontname="{style["card_font"]["family"]}"')
        acc.append(f'    fontsize={style["card_font"]["size"]}')
        acc.append(f'  ]')
        for label in "1MN":
            acc.append(f'  edge [label={label}]')
            for (ent_index, assoc_index, edge_label) in sorted(self.partial_edges):
                if label == edge_label:
                    acc.append(f'  {ent_index} -- {assoc_index}')

        acc.append(f'\n  // Edges between entities and relationships: total participation')
        acc.append(f'  edge [color="{style["leg_stroke_color"]}:invis:{style["leg_stroke_color"]}"]')
        for label in "1MN":
            acc.append(f'  edge [label={label}]')
            for (ent_index, assoc_index, edge_label) in sorted(self.total_edges):
                if label == edge_label:
                    acc.append(f'  {ent_index} -- {assoc_index}')
        acc.append("}")

        return "\n".join(acc)

def run(source, common):
    source = drain.run(source)
    source = split.run(source)
    source = explode.run(source, {"explosion_arity": "3", "weak_explosion": True})
    tree = parse_source(source)
    extractor = Chen()
    extractor.visit(tree)
    result = extractor.get_graphviz(common)
    if common.params["suck"]:
        result = minify(result)
    return result
