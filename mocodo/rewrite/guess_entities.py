from ..tools.parser_tools import parse_source

def run(source, id_prefix):
    if id_prefix is None:
        id_prefix = "id. "
    tree = parse_source(source)
    entity_name_refs =set(node.children[0].children[0].value for node in tree.find_data("entity_name_ref"))
    entity_name_defs = set(node.children[0].children[0].value for node in tree.find_data("entity_name_def"))
    new_entity_names = entity_name_refs - entity_name_defs
    new_entity_clauses = '\n'.join(f"{ent}: {id_prefix}{ent.lower()}, " for ent in new_entity_names)
    return f"{source}\n{new_entity_clauses}"