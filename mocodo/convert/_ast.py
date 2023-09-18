from ..tools.parser_tools import parse_source, Token

def ast_to_yaml(node, indent=""):
    indent += "  "
    if isinstance(node, Token):
        yield f"{indent}- type: {node.type}"
        yield f"{indent}  value: {repr(node.value)}"
    else:
        yield f"{indent}- type: {node.data}"
        yield f"{indent}  children:"
        for child in node.children:
            yield from ast_to_yaml(child, indent)


def run(source, subargs=None, common=None):
    tree = parse_source(source)
    return {
        "stem_suffix": "_ast",
        "text": "\n".join(ast_to_yaml(tree)),
        "extension": "yaml",
        "to_defer": False,
        "highlight": "yaml",
    }
