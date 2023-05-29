__import__("sys").path[0:0] =  ["."]

import re
from .parse_mcd import Token, Visitor, Transformer, Lark_StandAlone, Discard

# @v_args(inline=True)
# class Stripper(Transformer):

#     def __default__(self, data, children, meta):
#         if data in ("attr",):
#             children[0] = children[0].update(value=children[0].value.strip())
#         tree = super().__default__(data, children, meta)
#         return tree

def parse_source(source):
    parser = Lark_StandAlone()
    tree = parser.parse(f"{source}\n")
    return tree

class Reconstructor(Visitor):

    def __init__(self):
        self.result = []
    
    def __default__(self, tree):
        for child in tree.children:
            if isinstance(child, Token):
                self.result.append((child.line, child.column, child.value))

def reconstruct_source(tree):
    visitor = Reconstructor()
    visitor.visit(tree)
    return "".join(s for (_, _, s) in sorted(visitor.result))

def transform_source(source, transformer):
    tree = parse_source(source)
    new_tree = transformer.transform(tree)
    return reconstruct_source(new_tree)

class ClauseExtractor(Transformer):

    discard = lambda self, tree: Discard
    COLON = discard
    COMMA = discard
    NL = discard
    SP = discard
    LBRACKET = discard
    RBRACKET = discard
    LPAREN = discard
    RPAREN = discard
    HASHTAG = discard
    MORETHAN = discard
    PERCENT = discard
    BACKSLASH = discard

    def _item(self, key, tree):
        return (key, tree[0].value)
    
    card = lambda self, tree: self._item("card", tree)
    entity_name_ref = lambda self, tree: self._item("entity", tree)
    box_name_ref = lambda self, tree: self._item("box", tree)
    leg_role = lambda self, tree: self._item("role", tree)
    constraint_message = lambda self, tree: self._item("constraint_message", tree)
    constraint_link = lambda self, tree: self._item("constraint_link", tree)
    constraint_name = lambda self, tree: self._item("name", tree)
    card_prefix = lambda self, tree: self._item("card_prefix", tree)
    card_hidden = lambda self, tree: self._item("card_hidden", tree)
    leg_arrow = lambda self, tree: self._item("leg_arrow", tree)
    herit_arrow = lambda self, tree: self._item("herit_arrow", tree)
    entity_name_def = lambda self, tree: self._item("name", tree)
    herit_name = lambda self, tree: self._item("name", tree)
    assoc_name_def = lambda self, tree: self._item("name", tree)
    attr = lambda self, tree: self._item("attribute_label", tree)
    box_def_prefix = lambda self, tree: self._item("box_def_prefix", tree)
    
    def start(self, tree):
        return tree

    def line(self, tree):
        d = {}
        for t in tree:
            d.update(t)
        return d
    
    def break_(self, tree):
        return {"type": "break"}

    def phantoms(self, tree):
        return {"type": "phantoms", "count": tree[0].value.count(":")}
    
    def comment(self, tree):
        return {"type": "comment", "text": tree[0].value.strip()}
    
    def entity_clause(self, tree):
        return tree + [("type", "entity")]

    def assoc_clause(self, tree):
        return tree + [("type", "association")]
    
    def constraint_clause(self, tree):
        return tree + [("type", "constraint")]
    
    def herit_clause(self, tree):
        # Tweak the tree to make it look like an association
        d = dict(item for item in tree if isinstance(item, tuple))
        d["name"] = d.get("name", "")
        d["type"] = "inheritance"
        d["legs"] = [{"entity": d["entity"], "rank": -1}] + d["legs"]
        del d["entity"]
        return list(d.items())
    
    def box_attr(self, tree):
        return ("attribute", dict(tree))
    
    def assoc_leg(self, tree):
        return ("leg", dict(tree))
    
    def herit_parent(self, tree):
        return ("entity", tree[0][1])
    
    def herit_child(self, tree):
        return ("leg", dict(tree))
    
    def assoc_attr(self, tree):
        return ("attr", dict(tree))
    
    def foreign_reference(self, tree):
        return ("foreign_reference", dict(tree))
    
    def forced_to_table_lbracket(self, tree):
        return ("forced_to_table", True)

    def foreign_reference(self, tree):
        return ("foreign_reference", dict(tree))
    
    def forced_to_table_lbracket(self, tree):
        return ("forced_to_table", True)

    def assoc_protect(self, tree):
        return ("protect", True)

    def box_name(self, tree):
        return tree[0]
    
    def seq(self, tree):
        items = []
        for (rank, (_, d)) in enumerate(tree):
            d["rank"] = rank
            items.append(d)
        return (f"{tree[0][0]}s", items)

    def entity_attr_underscore(self, tree):
        return ("underscore", True)
    
    def assoc_leg(self, tree):
        return ("leg", dict(tree))
    
    def constraint_target(self, tree):
        return ("constraint_target", dict(tree))
    
    def foreign_reference(self, tree):
        return ("foreign_reference", dict(tree))

    def entity_or_table_attr(self, tree):
        d = dict(tree)
        if "foreign_reference" in d:
            d.update(d.pop("foreign_reference"))
        return ("attr", d)
    
    def this_table_attr(self, tree):
        return ("attribute_label", tree[0][1])
    
    def that_table(self, tree):
        return ("that_table", tree[0][1])
    
    def that_table_attr(self, tree):
        return ("that_table_attribute_label", tree[0][1])
    
    def constraint_ratios(self, tree):
        return ("constraint_ratios", tree)
    
    def constraint_ratio(self, tree):
        return float(tree[0].value)

    def indent(self, tree):
        return {"type": "break", "indent": tree[0].value} # Add a default type for dangling indents
    
    def data_type(self, tree):
        return ("data_type", tree[0].value if tree else "")
    
def extract_clauses(source):
    tree = parse_source(source)
    extractor = ClauseExtractor()
    result = extractor.transform(tree)    
    # Uniformize indentations. First, find the set of all distinct indentations.
    # Include the empty string if absent. Then, sort them by length. Finally,
    # replace each indentation by a number of spaces proportional to its index
    # in the sorted list.
    indents = set(line.get("indent", "") for line in result)
    indents.add("")
    indents = sorted(indents, key=len)
    indents = {indent: "  " * i for (i, indent) in enumerate(indents)}
    for (line, raw_line) in zip(result, source.splitlines()):
        line["indent"] = indents[line.get("indent", "")]
        line["source"] = line["indent"] + raw_line.lstrip()
    return result



if __name__ == "__main__":
    source = "Foo: bar [baz]"
    print(parse_source(source))