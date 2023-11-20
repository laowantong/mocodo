__import__("sys").path[0:0] =  ["."]

from ..mocodo_error import MocodoError
from ..parse_mcd import Token, Visitor, Transformer, Lark_StandAlone, Discard

def parse_source(source):
    parser = Lark_StandAlone()
    try:
        return parser.parse(f"{source}\n")
    except Exception as error:
        pin = _("Parsing error:\n{e}\n").format(e=error.get_context(source))
        expected = set(error.expected)
        t = error.token.type
        v = repr(error.token.value)
        if error.token.value == "\n":
            t = "BREAK"
        try:
            previous = error.token_history[0].type
        except:
            previous = None
        if expected == {'PERCENT', 'CONSTRAINT_LPAREN', 'BREAK', 'INDENT', 'PHANTOMS', 'BOX_NAME', 'SLASH', 'PLUS', 'MINUS', 'NL'}:
            raise MocodoError(501, _('{pin}"{v}" is not a valid line beginning.').format(pin=pin, v=v)) # fmt: skip
        if expected == {'PHANTOMS', 'PERCENT', 'CONSTRAINT_LPAREN', 'PLUS', 'MINUS', 'NL', 'SLASH', 'BOX_NAME'}:
            raise MocodoError(501, _('{pin}"{v}" is not a valid line beginning.').format(pin=pin, v=v)) # fmt: skip
        if expected == {'INHERITANCE_ARROW', 'COLON', 'NL', 'MORETHAN', 'SP', 'COMMA'}:
            raise MocodoError(502, _('{pin}Malformed box name.').format(pin=pin, v=v)) # fmt: skip
        if expected == {'COLON', 'COMMA'}:
            raise MocodoError(503, _('{pin}A valid box name starting a line must be followed by a colon or a comma.').format(pin=pin)) # fmt: skip
        if t == "COMMA" and expected == {'SP', 'BOX_NAME'}:
            raise MocodoError(505, _('{pin}Illegal comma after inheritance.').format(pin=pin)) # fmt: skip
        if t == "NUMBER" and expected == {'BOX_NAME', 'CARD', 'LBRACKET', 'LEG_ARROW', 'MINUS', 'SLASH', 'SP', 'ID_MARK'}:
            raise MocodoError(506, _('{pin}Malformed cardinalities.').format(pin=pin)) # fmt: skip
        if expected == {'CARD'}:
            raise MocodoError(506, _('{pin}Malformed cardinalities.').format(pin=pin)) # fmt: skip
        if expected == {'SLASH', 'CARD', 'ID_MARK'}:
            raise MocodoError(506, _('{pin}Malformed cardinalities.').format(pin=pin)) # fmt: skip
        if expected == {'INHERITANCE_NAME', 'BACKSLASH'} or expected == {'BACKSLASH'}:
            raise MocodoError(507, _('{pin}An inheritance name must be "", "X", "T" or "XT".').format(pin=pin)) # fmt: skip
        if t == "COMMA" and expected == {'NL'}:
            raise MocodoError(508, _('{pin}Only two coords are allowed.').format(pin=pin)) # fmt: skip
        if t == "BREAK" and expected == {'BOX_NAME', 'CARD', 'LBRACKET', 'LEG_ARROW', 'MINUS', 'SLASH', 'SP', 'ID_MARK'}:
            raise MocodoError(509, _('{pin}An association leg cannot be empty.').format(pin=pin)) # fmt: skip
        if expected == {'BOX_NAME', 'NUMBER'}:
            raise MocodoError(510, _('{pin}Expected a number or a box name.').format(pin=pin)) # fmt: skip
        if expected == {'BOX_NAME'}:
            raise MocodoError(511, _('{pin}Only a box name is possible here.').format(pin=pin)) # fmt: skip
        if expected == {'RBRACKET'}:
            raise MocodoError(512, _('{pin}Unclosed square bracket.').format(pin=pin)) # fmt: skip
        if expected == {'CONSTRAINT_RPAREN'}:
            raise MocodoError(514, _('{pin}A constraint name cannot contain more than three characters.').format(pin=pin)) # fmt: skip
        if expected == {'SP', 'BOX_NAME', 'CONSTRAINT_LEG'}:
            raise MocodoError(515, _('{pin}Expected a box name or a constraint leg.').format(pin=pin)) # fmt: skip
        if expected == {'LBRACKET', 'SP', 'BOX_NAME', 'NL', 'COLON', 'CONSTRAINT_LEG'}:
            raise MocodoError(516, _('{pin}Illegal character after a constraint name.').format(pin=pin)) # fmt: skip
        if expected == {'INHERITANCE_ARROW', 'SP'} or expected == {'INHERITANCE_ARROW'}:
            raise MocodoError(517, _('{pin}A parent name must be followed by an inheritance arrow among "<=", "<-", "->", "=>".').format(pin=pin)) # fmt: skip
        if t == "INHERITANCE_ARROW" and expected == {'MORETHAN'}:
            raise MocodoError(518, _('{pin}Please change the old foreign key syntax ("->") by the new one (">").').format(pin=pin)) # fmt: skip
        if t == "SP" and expected == {'COMMA', 'COLON', 'NL'}:
            raise MocodoError(519, _('{pin}The constraint targets must be comma-separated.').format(pin=pin)) # fmt: skip
        if expected == {'HASHTAG', 'NL', 'ID_GROUPS', 'ID_MARK', 'ATTR', 'COMMA'}:
            raise MocodoError(500, _('{pin}An attribute label cannot start with "{v[1]!r}".').format(pin=pin, v=v)) # fmt: skip
        if expected == {'ID_MARK', 'NL', 'ATTR', 'COMMA'}:
            raise MocodoError(500, _('{pin}An attribute label cannot start with "{v[1]!r}".').format(pin=pin, v=v)) # fmt: skip
        if expected == {'LBRACKET', 'NL', 'COMMA'}:
            raise MocodoError(521, _('{pin}An attribute label cannot contain "{v}".').format(pin=pin, v=v)) # fmt: skip
        if t in ("COMMA", "NL", "BREAK") and expected == {'MORETHAN'}:
            raise MocodoError(522, _('{pin}An attribute starting with "#" must contain two ">".').format(pin=pin)) # fmt: skip
        if t in ("COMMA", "NL", "BREAK") and expected == {'ATTR'}:
            raise MocodoError(523, _('{pin}Expected an entity name.').format(pin=pin)) # fmt: skip
        if expected == {'COLON', 'COMMA', 'NL'}:
            raise MocodoError(524, _('{pin}A box name cannot contain "{v}".').format(pin=pin, v=v)) # fmt: skip
        if expected == {"COMMA"}:
            raise MocodoError(525, _('{pin}Expected a comma.').format(pin=pin, v=v)) # fmt: skip)
        if t == "BOX_NAME" and expected == {'COMMA', 'NL'}:
            raise MocodoError(526, _('{pin}Malformed number.').format(pin=pin, v=v)) # fmt: skip
        if previous in ("NUMBER", "BOX_NAME") and expected == {'COMMA', 'NL'}:
            raise MocodoError(527, _('{pin}More than two coordinates.').format(pin=pin, v=v)) # fmt: skip
        if expected == {'LBRACKET', 'NL', 'COMMA', 'MORETHAN'}:
            raise MocodoError(528, _('{pin}An attribute label cannot have more than one optionality marker.').format(pin=pin, v=v))
        raise MocodoError(504, _('{pin}Token "{t}" encountered. Expected tokens: {expected}.').format(pin=pin, expected=expected, t=t))
        
    
class Reconstructor(Visitor):

    def __init__(self):
        self.result = []
    
    def __default__(self, tree):
        for child in tree.children:
            if isinstance(child, Token):
                self.result.append((child.line, child.column, child.value))

def reconstruct_source(tree):
    visitor = Reconstructor()
    try:
        visitor.visit(tree)
    except Exception as visitor_error:
        raise visitor_error.__context__ if visitor_error.__context__ else visitor_error
    return "".join(s for (_, _, s) in sorted(visitor.result))

def transform_source(source, transformer):
    tree = parse_source(source)
    try:
        new_tree = transformer.transform(tree)
    except Exception as transformer_error:
        raise transformer_error.__context__ if transformer_error.__context__ else transformer_error
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
    CONSTRAINT_LPAREN = discard
    CONSTRAINT_RPAREN = discard
    HASHTAG = discard
    MORETHAN = discard
    PERCENT = discard
    BACKSLASH = discard

    def _item(self, key, tree):
        return (key, tree[0].value)
    
    card = lambda self, tree: self._item("card", tree)
    entity_name_ref = lambda self, tree: self._item("entity", tree)
    box_name_ref = lambda self, tree: self._item("name", tree)
    leg_note = lambda self, tree: self._item("leg_note", tree)
    constraint_note = lambda self, tree: self._item("constraint_note", tree)
    constraint_leg = lambda self, tree: self._item("constraint_leg", tree)
    constraint_name = lambda self, tree: self._item("name", tree)
    card_prefix = lambda self, tree: self._item("card_prefix", tree)
    card_hidden = lambda self, tree: self._item("card_hidden", tree)
    leg_arrow = lambda self, tree: self._item("leg_arrow", tree)
    inheritance_arrow = lambda self, tree: self._item("inheritance_arrow", tree)
    entity_name_def = lambda self, tree: self._item("name", tree)
    inheritance_name = lambda self, tree: self._item("name", tree)
    assoc_name_def = lambda self, tree: self._item("name", tree)
    attr = lambda self, tree: self._item("attribute_label", tree)
    box_def_prefix = lambda self, tree: self._item("box_def_prefix", tree)
    id_mark = lambda self, tree: self._item("id_mark", tree)

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
        return {"type": "comment", "text": f"%{tree[0].value.rstrip()}"}
    
    def entity_clause(self, tree):
        return tree + [("type", "entity")]

    def assoc_clause(self, tree):
        return tree + [("type", "association")]
    
    def constraint_clause(self, tree):
        return tree + [("type", "constraint")]
    
    def inheritance_clause(self, tree):
        # Tweak the tree to make it look like an association
        d = dict(item for item in tree if isinstance(item, tuple))
        d["name"] = d.get("name", "")
        d["type"] = "inheritance"
        d["legs"] = [{"entity": d["entity"], "rank": -1}] + d["legs"]
        del d["entity"]
        return list(d.items())

    def typed_attr(self, tree):
        return ("attr", dict(tree))
    
    def assoc_leg(self, tree):
        return ("leg", dict(tree))
    
    def inheritance_parent(self, tree):
        return ("entity", tree[0][1])
    
    def inheritance_child(self, tree):
        return ("leg", dict(tree))
    
    def foreign_reference(self, tree):
        return ("foreign_reference", dict(tree))

    def box_name(self, tree):
        return tree[0]
    
    def seq(self, tree):
        items = []
        for (rank, (_, d)) in enumerate(tree):
            d["rank"] = rank
            items.append(d)
        return (f"{tree[0][0]}s", items)

    def assoc_attr(self, tree):
        if tree[0] == "_":
            tree[-1][1]["id_mark"] = "_"
        return ("attr", tree[-1][1])

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
        if "attr" in d:
            d.update(d.pop("attr"))
        return ("attr", d)
    
    def this_table_attr(self, tree):
        return ("attribute_label", tree[0][1])
    
    def that_table(self, tree):
        return ("that_table", tree[0][1])
    
    def that_table_attr(self, tree):
        return ("that_table_attribute_label", tree[0][1])
    
    def constraint_coords(self, tree):
        return ("constraint_coords", [self._constraint_coord(x) for x in tree])
    
    def _constraint_coord(self, x):
        try:
            x = float(x)
            return int(x) if x == int(x) else x
        except (TypeError, ValueError):
            return x[1]

    def indent(self, tree):
        return {"type": "break", "indent": tree[0].value} # Add a default type for dangling indents
    
    def datatype(self, tree):
        return ("datatype", tree[0].value if tree else "")
    
    def id_groups(self, tree):
        return ("id_groups", "".join(sorted(set(tree[0].value))))
    
def extract_clauses(source):
    tree = parse_source(source)
    extractor = ClauseExtractor()
    result = extractor.transform(tree)
    for line in result:
        if "type" not in line:
            line["type"] = "break"
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


def first_child(tree, name, i=0):
    result = next(tree.find_data(name), None)
    if result is None:
        return ""
    return result.children[i]

def is_identifier(i, id_groups, id_mark):
    # Entity (foo, bar)
    if i == 0:
        if "0" not in id_groups:
            return True # foo / 1_foo
    elif "0" in id_groups:
        return True # 0_bar / 01_bar
    elif id_mark == "_" and id_groups == "":
        return True # _bar
    return False # 0_foo / 01_foo / _foo / bar / 1_bar

if __name__ == "__main__":
    # python -m mocodo.tools.parser_tools
    source = "EMPLOYER, 01 PARTICIPANT, 0N ENTREPRISE:\nCLIENT: num client, nom"
    tree = parse_source(source)
    print(tree.pretty())
    print(reconstruct_source(tree))
    print(extract_clauses(source))
