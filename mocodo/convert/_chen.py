from collections import Counter
import itertools
import re

__import__("sys").path[0:0] = ["."]

from ..parse_mcd import Visitor
from ..tools.parser_tools import first_child, parse_source, is_identifier
from ..rewrite import _split as split
from ..tools.graphviz_tools import create_name_to_index
from ..tools.string_tools import wrap_label, rstrip_digit_or_underline
from ..version_number import version

class Chen(Visitor):
    def __init__(self, subargs, common):
        self.no_attrs = "attrs" not in subargs
        subargs.pop("attrs", None)
        self.subargs = subargs
        self.df_counter = itertools.count()
        self.df_label = common.params["df"]

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
        # Invisible boxes
        self.invisible_boxes = set()

    def entity_or_table_attr(self, tree):
        id_groups = str(first_child(tree, "id_groups"))
        id_mark = str(first_child(tree, "id_mark"))
        attr = str(first_child(tree, "attr"))
        tree.children = [(id_groups, id_mark, attr)]
    
    def entity_clause(self, tree):
        ent_name = str(first_child(tree, "box_name"))
        ent_index = self.name_to_index(f"ent_{ent_name}")
        if first_child(tree, "box_def_prefix") == "-":
            self.invisible_boxes.add(ent_index)
            return
        ent_name = rstrip_digit_or_underline(ent_name)
        self.entity_nodes.append((ent_index, ent_name))

        # Entity attributes
        if self.no_attrs:
            return
        for (i, node) in enumerate(tree.find_data("entity_or_table_attr")):
            (id_groups, id_mark, attr_label) = node.children[0]
            attr_label = str(attr_label)
            if attr_label == "":
                continue # don't create a node for a spacer attribute
            attr_index = self.name_to_index(f"ent_attr_{ent_index}_{attr_label}")
            if is_identifier(i, id_groups, id_mark):
                self.ent_key_attr_nodes.append((attr_index, attr_label, ent_index))
            else:
                self.ent_attr_nodes.append((attr_index, attr_label))
            self.ent_attr_edges.append((ent_index, attr_index))
    
    def assoc_clause(self, tree):
        legs = [node for node in tree.find_data("assoc_leg")]

        # Accumulate the association as a new relationship
        assoc_name = str(first_child(tree, "assoc_name_def").children[0])
        if assoc_name == self.df_label:
            assoc_name = f"{assoc_name}{next(self.df_counter)}"
        assoc_index = self.name_to_index(f"assoc_{assoc_name}")
        if first_child(tree, "box_def_prefix") == "-":
            self.invisible_boxes.add(assoc_index)
            return
        assoc_name = rstrip_digit_or_underline(assoc_name)
        self.rel_nodes.append((assoc_index, assoc_name))

        min_maxs = [node.children[0].value for node in tree.find_data("card")]
        ent_names = [str(first_child(leg, "entity_name_ref").children[0]) for leg in legs]

        edge_accs = [self.partial_edges if c[0] == "0" else self.total_edges for c in min_maxs]
        ent_indexes = [self.name_to_index(f"ent_{ent_name}") for ent_name in ent_names]

        if len(legs) == 2:
            weaks = [first_child(leg, "card_prefix") == "_" for leg in legs]
            if any(weaks): # the binary association is "weak", in the Chen sense
                self.weak_box_indexes.add(assoc_index)
            # If both legs are *N, change one with *M
            if min_maxs[0][1] == min_maxs[1][1] == "N":
                min_maxs[0] = f"{min_maxs[0][0]}M"
            for i in range(2):
                # The 1-i is to get the other leg, i.e., to look across instead of to look here
                edge_accs[i].append((ent_indexes[i], assoc_index, min_maxs[1-i][1]))
                if weaks[i]: # the entity is distinguished by a _11
                    self.weak_box_indexes.add(ent_indexes[i])
                    self.strengthening_leg_count[ent_indexes[i]] += 1
                else: # we are sure that it is not an associative entity
                    self.not_gerund_nodes.add(ent_indexes[i])
        else:
            # The Chen's card is 1 if the min-max card has a "/" prefix, N otherwise
            chen_cards = ["1" if first_child(leg, "card_prefix") == "/" else "N" for leg in legs]
            for (chen_card, edge_acc, ent_index) in zip(chen_cards, edge_accs, ent_indexes):
                edge_acc.append((ent_index, assoc_index, chen_card))
                self.not_gerund_nodes.add(ent_index)
        
        # Association attributes
        if self.no_attrs:
            return
        for node in tree.find_data("attr"):
            attr_label = str(node.children[0])
            if attr_label == "":
                continue # don't create a node for a spacer attribute
            attr_index = self.name_to_index(f"assoc_attr_{assoc_index}_{attr_label}")
            self.rel_attr_nodes.append((attr_index, attr_label))
            self.rel_attr_edges.append((assoc_index, attr_index))
    
    def start(self, tree):
        # Since the traversal is depth-first, this is in fact a post-treatment
        for (ent_index, strengthening_leg_count) in self.strengthening_leg_count.items():
            if strengthening_leg_count < 2:
                self.not_gerund_nodes.add(ent_index)
        self.partial_edges = [(x, y, c) for (x, y, c) in self.partial_edges if x not in self.invisible_boxes and y not in self.invisible_boxes]
        self.total_edges = [(x, y, c) for (x, y, c) in self.total_edges if x not in self.invisible_boxes and y not in self.invisible_boxes]
    
    def get_graphviz(self, common):
        style = common.load_style()
        result = []
        result.append(f'// Generated by Mocodo {version}\n')
        result.append(f'graph{{')
        result.append(f'  bgcolor="{style["background_color"]}"')
        if common.params["seed"] is not None:
            result.append(f'  start={common.params["seed"]}')

        for (subsubopt, subsubarg) in self.subargs.items():
            result.append(f'  {subsubopt}={subsubarg}')

        result.append(f'\n  // Entities')
        result.append(f'  node [')
        result.append(f'    shape=box')
        result.append(f'    style=filled')
        result.append(f'    penwidth={style["box_stroke_depth"]}')
        result.append(f'    color="{style["entity_stroke_color"]}"')
        result.append(f'    fillcolor="{style["entity_cartouche_color"]}"')
        result.append(f'    fontcolor="{style["entity_cartouche_text_color"]}"')
        result.append(f'  ]')
        for (index, name) in self.entity_nodes:
            name = "\\n".join(wrap_label(name))
            if index in self.not_gerund_nodes:
                if index in self.weak_box_indexes:
                    result.append(f'  {index} [label="{name}",peripheries=2]')
                else:
                    result.append(f'  {index} [label="{name}"]')
        
        if len(self.entity_nodes) > len(self.not_gerund_nodes):
            result.append(f'\n  // Associative entities')
            for (index, name) in self.entity_nodes:
                name = "\\n".join(wrap_label(name))
                if index not in self.not_gerund_nodes:
                    result.append(f'  {index} [label="{name}",shape=Mdiamond]')

        if self.ent_attr_nodes or self.ent_key_attr_nodes:
            result.append(f'\n  // Normal entity attributes')
            result.append(f'  node [')
            result.append(f'    shape=oval')
            result.append(f'    penwidth={style["box_stroke_depth"]}')
            result.append(f'    color="{style["entity_stroke_color"]}"')
            result.append(f'    fillcolor="{style["entity_color"]}"')
            result.append(f'    fontcolor="{style["entity_attribute_text_color"]}"')
            result.append(f'  ]')
            for (index, name) in self.ent_attr_nodes:
                name = "\\n".join(wrap_label(name))
                result.append(f'  {index} [label="{name}"]')
            result.append(f'\n  // Weak and strong entity attributes')
            for (index, name, ent_index) in self.ent_key_attr_nodes:
                name = "<br/>".join(wrap_label(name))
                if ent_index in self.weak_box_indexes:
                    result.append(f'  {index} [label=<<u>{name}</u>> style="dashed,filled"]')
                else:
                    result.append(f'  {index} [label=<<u>{name}</u>>]')
        
        if self.rel_attr_nodes:
            result.append(f'\n  // Relationship attributes')
            result.append(f'  node [')
            result.append(f'    color="{style["association_stroke_color"]}"')
            result.append(f'    fillcolor="{style["association_color"]}"')
            result.append(f'    fontcolor="{style["association_attribute_text_color"]}"')
            result.append(f'  ]')
            for (index, name) in self.rel_attr_nodes:
                name = "\\n".join(wrap_label(name))
                result.append(f'  {index} [label="{name}"]')

        if self.rel_nodes:
            result.append(f'\n  // Relationships')
            result.append(f'  node [')
            result.append(f'    shape=diamond')
            result.append(f'    height=0.7')
            result.append(f'    penwidth={style["box_stroke_depth"]}')
            result.append(f'    color="{style["association_stroke_color"]}"')
            result.append(f'    fillcolor="{style["association_cartouche_color"]}"')
            result.append(f'    fontcolor="{style["association_cartouche_text_color"]}"')
            result.append(f'  ]')
            for (index, name) in self.rel_nodes:
                name = "\\n".join(wrap_label(name))
                if index in self.weak_box_indexes:
                    result.append(f'  {index} [label="{name}",peripheries=2]')
                else:
                    result.append(f'  {index} [label="{name}"]')

        if self.ent_attr_edges or self.rel_attr_edges:
            result.append(f'\n  // Edges between entities and attributes')
            result.append(f'  edge [')
            result.append(f'    penwidth={style["box_stroke_depth"]}')
            result.append(f'    color="{style["entity_stroke_color"]}"')
            result.append(f'  ]')
            for (ent_index, attr_index) in sorted(self.ent_attr_edges):
                result.append(f'  {ent_index} -- {attr_index}')
            result.append(f'\n  // Edges between relationships and attributes')
            result.append(f'  edge [color="{style["association_stroke_color"]}"]')
            useless = True
            for (assoc_index, attr_index) in sorted(self.rel_attr_edges):
                result.append(f'  {assoc_index} -- {attr_index}')
                useless = False
            if useless:
                result.pop()
                result.pop()

        if self.partial_edges or self.total_edges:
            seen_edges = set()
            result.append(f'\n  // Edges between entities and relationships')
            result.append(f'  edge [')
            result.append(f'    penwidth={style["leg_stroke_depth"]}')
            result.append(f'    color="{style["leg_stroke_color"]}:{style["leg_stroke_color"]}"') # default to total participation
            result.append(f'    fontcolor="{style["card_text_color"]}"')
            result.append(f'    labeldistance=2')
            result.append(f'    headlabel=1')
            result.append(f'  ]')
            for label in "1MN":
                useless = label != "1"
                if label != "1":
                    result.append(f'  edge [headlabel={label}]')
                suffix = ""
                for edges in (self.total_edges, self.partial_edges):
                    for (ent_index, assoc_index, edge_label) in sorted(edges):
                        if label == edge_label:
                            if (ent_index, assoc_index) in seen_edges:
                                (assoc_index, ent_index) = (ent_index, assoc_index)
                            result.append(f'  {ent_index} -- {assoc_index}{suffix}')
                            seen_edges.add((ent_index, assoc_index))
                            useless = False
                    suffix = f' [color="{style["leg_stroke_color"]}"]' # from now on, partial participation
                if useless:
                    result.pop()
        result.append("}")

        result = "\n".join(result)
        useless_colors = [
            'bgcolor="#FFFFFF"',
            'color="#000000"',
            'fontcolor="#000000"',
        ]
        for useless_color in useless_colors:
            result = re.sub(fr'(?m)^ *{useless_color}\n', "", result)
        return result

    def get_text_for_testing(self):
        nodes = {}
        for (i, x) in self.entity_nodes:
            if i in self.not_gerund_nodes:
                if i in self.weak_box_indexes:
                    nodes[i] = f"[[{x}]]"
                else:
                    nodes[i] = f"[{x}]"
            else:
                nodes[i] = f"[<{x}>]"
        for (i, x) in self.rel_nodes:
            if i in self.weak_box_indexes:
                nodes[i] = f"<<{x}>>"
            else:
                nodes[i] = f"<{x}>"
        for (i, x, j) in self.ent_key_attr_nodes:
            if j in self.weak_box_indexes:
                nodes[i] = f"(.{x}.)"
            else:
                nodes[i] = f"(_{x}_)"
        nodes.update((i, f"({x})") for (i, x) in self.ent_attr_nodes + self.rel_attr_nodes)
        result = []
        for (x, y, c) in self.partial_edges:
            result.append(f"            {nodes[x]} --{c}-- {nodes[y]}")
        for (x, y, c) in self.total_edges:
            result.append(f"            {nodes[x]} =={c}== {nodes[y]}")
        for (x, y) in self.ent_attr_edges + self.rel_attr_edges:
            result.append(f"            {nodes[x]} -- {nodes[y]}")
        return "\n".join(sorted(result))


def run(source, subargs=None, common=None, testing=False):
    subargs = subargs or {}
    source = split.run(source)
    tree = parse_source(source)
    extractor = Chen(subargs, common)
    extractor.visit(tree)
    if testing:
        return extractor.get_text_for_testing()
    text = extractor.get_graphviz(common)
    return {
        "stem_suffix": "_erd_chen",
        "text": text,
        "extension": "gv",
        "to_defer": True,
        "highlight": "graphviz",
    }
