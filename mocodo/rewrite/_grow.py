import random

from ..tools.parser_tools import parse_source


def random_booleans(n, p):
    p = min(n, p)
    result = [True] * p + [False] * (n - p)
    random.shuffle(result)
    return result


def run(source, subargs=None, params=None, **kargs):
    default = {
            "n": 10,
            "arity_1": 2,
            "arity_3": 2,
            "arity_4": 0,
            "ent_attrs": 4,
            "doubles": 1,
            "composite_ids": 2,
            "assoc_attrs": 2,
        }
    subargs = {**default, **(subargs or {})}

    association_bases = [None, _("Reflexive"), _("Binary"), _("Ternary"), _("Quaternary")]
    entity_base = _("Entity")

    n = subargs["n"]

    arities = [1] * subargs["arity_1"] + [3] * subargs["arity_3"] + [4] * subargs["arity_4"] + [2] * n
    arities = arities[:n]
    random.shuffle(arities)

    for key in ("assoc_attrs", "composite_ids"):
        subargs[key] = random_booleans(n, subargs[key])
    
    ent_attr_prefixes = []
    for is_composite in subargs["composite_ids"]:
        if is_composite:
            ent_attr_prefixes.append(["", "_"] + [""] * random.randint(1, subargs["ent_attrs"] - 2))
        else:
            ent_attr_prefixes.append([""] * random.randint(1, subargs["ent_attrs"]))
    
    tree = parse_source(source)
    entities = [node.children[0].children[0].value for node in tree.find_data("entity_name_def")]
    associations = [node.children[0].children[0].value for node in tree.find_data("assoc_name_def")]
    counter = len(entities) + len(associations) + 1

    clauses = [source]
    ref_pool = []
    for i in range(subargs["n"] - subargs["doubles"]):


        if arities[i] == 1:
            # to keep the MCD connected, don't create a new entity if the association is reflexive
            old_entity = random.choice(entities)
            refs = [old_entity, old_entity]
        else:
            # Normal case: create a new entity
            new_entity = f"{entity_base} {counter}_"
            new_ent_attrs = [f"{prefix}attr {counter} {j}_" for (j, prefix) in enumerate(ent_attr_prefixes[i], 1)]
            clauses.append(f"{new_entity}: {', '.join(new_ent_attrs)}")
            old_refs = [random.choice(entities) for _ in range(arities[i] - 1)]
            refs = [new_entity] + old_refs
            entities.append(new_entity)
            counter += 1
        
        new_association = f"{association_bases[arities[i]]} {counter}_"
        ref_pool.append(refs)
        clauses.append(", XX ".join([new_association] + refs))
        new_assoc_attrs = [f"attr {counter} {j}_" for j in range(1, subargs["assoc_attrs"][i] + 1)]
        if new_assoc_attrs:
            clauses[-1] += f": {', '.join(new_assoc_attrs)}"
        associations.append(new_association)
        counter += 1
    
    for i in range(subargs["n"] - subargs["doubles"], subargs["n"]):
        old_refs = random.choice(ref_pool)
        arity = len(set(old_refs))
        new_association = f"{association_bases[arity]} {counter}_"
        clauses.append(", XX ".join([new_association] + old_refs))
        new_assoc_attrs = [f"attr {counter} {j}_" for j in range(1, subargs["assoc_attrs"][i] + 1)]
        if new_assoc_attrs:
            clauses[-1] += f": {', '.join(new_assoc_attrs)}"
        associations.append(new_association)
        counter += 1
    
    return "\n".join(clauses)
