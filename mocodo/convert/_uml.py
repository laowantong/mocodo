import itertools
import gettext

__import__("sys").path[0:0] = ["."]

from ..parse_mcd import Visitor
from ..tools.parser_tools import first_child, parse_source, is_identifier
from ..rewrite import (
    _split as split,
    _drain as drain,
)
from ..version_number import version

MIN_MAX_IN_UML = {
    "01": "1..*",
    "0N": "*",
    "11": "1",
    "1N": "1..*",
}

gettext.NullTranslations().install()

INHERITANCE_IN_UML = {
    "XT": _("{complete, disjoint}"), # Partition
    "X": _("{incomplete, disjoint}"), # Exclusivité
    "T": _("{complete, overlapping}"), # Totalité
    "": _("{incomplete, overlapping}"),
}

class UmlClassDiagram(Visitor):
    def __init__(self, preamble, common):
        self.common = common
        self.preamble = preamble or "" # preamble may be None
        self.id_counter = itertools.count()
        self.df_label = common.params["df"]
        self.has_no_datatype = True
        self.acc = []
        self.invisible_boxes = set()

    def entity_or_table_attr(self, tree):
        id_groups = str(first_child(tree, "id_groups"))
        id_mark = str(first_child(tree, "id_mark"))
        attr = str(first_child(tree, "attr"))
        datatype = str(first_child(tree, "datatype"))
        if datatype:
            self.has_no_datatype = False
        tree.children = [(id_groups, id_mark, attr, datatype)]
    
    def entity_clause(self, tree):
        ent_name = str(first_child(tree, "box_name"))
        if first_child(tree, "box_def_prefix") == "-":
            self.invisible_boxes.add(ent_name)
            return
        attributes = []
        for (i, node) in enumerate(tree.find_data("entity_or_table_attr")):
            (id_groups, id_mark, attr_label, datatype) = node.children[0]
            attr_label = str(attr_label)
            if attr_label == "":
                continue # ignore spacer attributes
            attributes.append((is_identifier(i, id_groups, id_mark), attr_label, datatype))
        self.acc.append({
            "kind": "table",
            "name": ent_name,
            "attributes": attributes,
        })
        self.acc.append({"kind": "spacer"})
    
    def assoc_clause(self, tree):
        legs = [node for node in tree.find_data("assoc_leg")]
        assoc_name = str(first_child(tree, "assoc_name_def").children[0])
        if first_child(tree, "box_def_prefix") == "-":
            self.invisible_boxes.add(assoc_name)
            return

        min_maxs = [node.children[0].value for node in tree.find_data("card")]
        ent_names = [str(first_child(leg, "entity_name_ref").children[0]) for leg in legs]

        typed_attrs = []
        for node in list(tree.find_data("typed_attr")):
            attr_label = str(first_child(node, "attr"))
            if attr_label == "":
                continue # don't create a node for a spacer attribute
            datatype = str(first_child(node, "datatype"))
            typed_attrs.append((attr_label, datatype))

        if len(legs) == 2:
            weaks = [first_child(leg, "card_prefix") == "_" for leg in legs]
            self.acc.append({
                "kind": "binary_link",
                "tables": ent_names,
                "table_1": ent_names[0],
                "card_1": MIN_MAX_IN_UML.get(min_maxs[1], "*"),
                "composition_1": weaks[1],
                "table_2": ent_names[1],
                "card_2": MIN_MAX_IN_UML.get(min_maxs[0], "*"),
                "composition_2": weaks[0],
                "assoc_name": assoc_name,
            })
            if typed_attrs:
                self.acc.append({
                    "kind": "binary_link_attrs",
                    "tables": ent_names,
                    "table_1": ent_names[0],
                    "table_2": ent_names[1],
                    "assoc_name": assoc_name,
                })
        else:
            # The card is 1 (11) if the min-max card has a "/" prefix, 1..* or * otherwise
            diamond = f"N_ARY_{next(self.id_counter)}"
            self.acc.append({
                "kind": "n_ary_link",
                "diamond": diamond,
                "tables": ent_names,
                "cards": ["1" if first_child(leg, "card_prefix") == "/" else MIN_MAX_IN_UML.get(first_child(leg, "card"), "*") for leg in legs],
                "assoc_name": assoc_name,
            })
            if typed_attrs:
                self.acc.append({
                    "kind": "n_ary_link_attrs",
                    "diamond": diamond,
                    "tables": ent_names,
                    "assoc_name": assoc_name,
                })
        
        if typed_attrs:
            self.acc.append({
                "kind": "table",
                "name": assoc_name,
                "attributes": [(False, attr_label, datatype) for (attr_label, datatype) in typed_attrs],
                "tables": ent_names,
            })
        
        self.acc.append({"kind": "spacer"})
    
    def inheritance_clause(self, tree):
        inheritance_name = str(first_child(tree, "inheritance_name"))
        box_names = [str(first_child(leg, "box_name")) for leg in tree.find_data("box_name")]
        box_names.reverse() # not sure why, but the boxes seem to come in reverse order
        self.acc.append({
            "kind": "generalization",
            "set": INHERITANCE_IN_UML[inheritance_name],
            "parent": box_names[0],
            "children": [box_name for box_name in box_names[1:]],
            "id": f"GENERALIZATION_{next(self.id_counter)}",
        })
        self.acc.append({"kind": "spacer"})
    
    def start(self, tree):
        self.acc = list(filter(lambda d: not self.invisible_boxes.intersection(d.get("tables", [])), self.acc))
    
    def get_plantuml(self):
        style = self.common.load_style()
        result = []
        if not self.preamble.startswith("-"):
            result.append(f"' Generated by Mocodo {version}\n")
        result.append(f'@startuml "{self.common.params["title"]}"\n')
        result.append(f'!define Table(x) class "x" << (T,{style["entity_color"]}) >>')
        result.append("!define pk(x) <b>x</b>")
        if self.preamble.startswith("-"):
            self.preamble = self.preamble[1:]
        else:
            result.append("\n".join([
                "hide methods",
                "left to right direction",
                f'skinparam groupInheritance 2',
                f'skinparam lineThickness {style["box_stroke_depth"]}',
                f'skinparam lineColor {style["association_stroke_color"]}',
                f'skinparam backgroundColor {style["background_color"]}',
                f'skinparam classAttributeFontColor {style["entity_attribute_text_color"]}',
                f'skinparam classAttributeFontName Monospaced',
                f'skinparam classAttributeFontSize 14',
                f'skinparam classBackgroundColor {style["entity_color"]}',
                f'skinparam classBorderColor {style["entity_stroke_color"]}',
                f'skinparam classBorderThickness {style["box_stroke_depth"]}',
                f'skinparam classFontColor {style["entity_cartouche_text_color"]}',
                f'skinparam classFontName Arial',
                f'skinparam classFontSize 18',
                f'skinparam classHeaderBackgroundColor {style["entity_cartouche_color"]}',
            ]))
        result.append(self.preamble.replace(r"\n", "\n")) # the user-defined preamble comes raw
        for element in self.acc:
            if element["kind"] == "table":
                max_attr_length = max([len(attr) for (_, attr, _) in element["attributes"]], default=0)
                result.append(f'Table("{element["name"]}") {{')
                for (is_id, attr, datatype) in element["attributes"]:
                    suffix = ""
                    if datatype:
                        tabs = " " * (max_attr_length - len(attr) + 1)
                        suffix = f"{tabs}{datatype}"
                    if is_id:
                        attr = f"pk({attr})"
                    result.append(f"    {{field}} + {attr}{suffix}")
                result.append(f"}}")
            elif element["kind"] == "binary_link":
                head = "*" if element["composition_1"] else "-"
                tail = "*" if element["composition_2"] else "-"
                element["link"] = f"{head}-{tail}"
                if element["assoc_name"].upper() == self.df_label.upper():
                    result.append('"{table_1}" "{card_1}" {link} "{card_2}" "{table_2}"'.format(**element))
                else:
                    result.append('"{table_1}" "{card_1}" {link} "{card_2}" "{table_2}": "{assoc_name}"'.format(**element))
            elif element["kind"] == "n_ary_link":
                result.append(f"diamond {element['diamond']}")
                for (table_name, card) in zip(element["tables"], element["cards"]):
                    result.append(f'{element["diamond"]} -- "{card}" "{table_name}"')
            elif element["kind"] == "binary_link_attrs":
                result.append('("{table_1}", "{table_2}") .. "{assoc_name}"'.format(**element))
            elif element["kind"] == "n_ary_link_attrs":
                result.append('{diamond} "{assoc_name}" .. "{assoc_name}"'.format(**element))
            elif element["kind"] == "generalization":
                if element["set"]:
                    result.append(f'note "{element["set"]}" as {element["id"]}')
                    result.extend(f'{element["id"]} -[dotted]- {child}' for child in element["children"])
                result.extend(f'{element["parent"]} <|-- {child}' for child in element["children"])
            else: # spacer
                result.append("")
        result.append(f"@enduml\n")
        return "\n".join(result)


def run(source, subargs=None, common=None):
    (language, preamble) = next(iter(subargs.items()), ("plantuml", ""))
    source = split.run(source)
    source = drain.run(source)
    tree = parse_source(source)
    extractor = UmlClassDiagram(preamble, common)
    extractor.visit(tree)
    if True: # language == "plantuml":
        text = extractor.get_plantuml()
        extension = "puml"
        highlight = "puml"
    else:
        text = extractor.get_mermaid()
        extension = "mmd"
        highlight = "mermaid"
    return {
        "stem_suffix": "_uml",
        "text": text,
        "extension": extension,
        "to_defer": True,
        "highlight": highlight,
    }
