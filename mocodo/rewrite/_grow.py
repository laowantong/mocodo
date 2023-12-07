import contextlib
import random
import re

from ..tools.parser_tools import parse_source
from ..mocodo_error import MocodoError


def random_booleans(n, p):
    p = min(n, p)
    result = [True] * p + [False] * (n - p)
    random.shuffle(result)
    return result

def calculate_cards(scheme, refs):
    if len(refs) > len(set(refs)): # If the association is reflexive
        # Process the cases of n-ary associations with n > 2
        # (the other ones have already been filtered out by the caller)
        scheme = scheme.replace("_", "") # silently forbid weak associations
        scheme = scheme.replace("/", "") # silently forbid cluster associations
    (head, tail) = scheme.split("-")
    cards = [head] + [tail] * (len(refs) - 1)
    cards = [card.replace("*", random.choice("01")) for card in cards]
    random.shuffle(cards)
    return cards

def extract_weak_entities(cards, refs):
    for (card, ref) in zip(cards, refs):
        if "_" in card:
            yield ref

def biased_choice(elements):
    # Return a random element from a list, with a bias towards the last elements.
    i = max(random.randrange(0, len(elements)) for _ in range(3))
    return elements[i]

def biased_sample(elements, k):
    # Return a random sample of k elements from a list, with a bias towards the last elements.
    max_sample = [-1] # incorrect sample, but it will be replaced on the first iteration
    for _ in range(3):
        sample = random.sample(range(len(elements)), k)
        if min(sample) > min(max_sample):
            max_sample = sample
    return [elements[i] for i in max_sample]

def run(source, subargs=None, params=None, **kargs):
    match_card_scheme = re.compile(r"^[/_]?[01*][1N]-[/_]?[01*][1N]$").match
    subargs = subargs or {}
    default = {
            "n": 10,
            "arity_1": 2,
            "arity_3": 2,
            "arity_4": 0,
            "ent_attrs": 4,
            "doubles": 1,
            "composite_ids": 1,
            "assoc_attrs": 2,
            "*1-*N": 3,
            "01-11": 1,
            "from_scratch": False,
        }
    # Complete the given subargs with default values
    settings = {}
    for (k, v) in default.items():
        if k in subargs:
            cast = type(v) # cast to the same type as the default value
            with contextlib.suppress(TypeError):
                settings[k] = cast(subargs[k])
                continue
            # If the cast fails, silently fall back to the default value
        settings[k] = v
    
    # Complete the settings with the remaining card schemes
    for (k, v) in subargs.items():
        if match_card_scheme(k):
            with contextlib.suppress(TypeError):
                settings[k] = int(v)
    
    # Silently correct incompatible numbers
    n = settings["n"]
    for (k, v) in list(settings.items()):
        if k in ("n", "assoc_attrs"):
            continue
        elif k == "ent_attrs":
            settings[k] = max(v, 1)
        elif k in ("doubles", "arity_1", "arity_3", "arity_4"):
            settings[k] = min(v, n - 1)

    association_bases = [None, _("Reflexive"), _("Binary"), _("Ternary"), _("Quaternary")]
    entity_base = _("Entity")
    weak_entity_base = _("Weak Entity")
    attr_base = _("attr")
    id_base = _("id")

    card_schemes = []
    for (k, v) in settings.items():
        if match_card_scheme(k):
            card_schemes.extend([k] * v)
    card_schemes.extend(["*N-*N"] * (n - len(card_schemes)))

    # Try to find a combination of card schemes and arities that is compatible
    arities = [1] * settings["arity_1"] + [3] * settings["arity_3"] + [4] * settings["arity_4"] + [2] * n
    arities = arities[:n]
    max_tries = 100
    while max_tries > 0:
        random.shuffle(arities)
        # Slightly push the non binary arities towards the end (one iteration of bubble sort).
        # Reason: the non binary arities are tougher to place when there are not many entities yet
        for i in range(len(arities) - 1):
            if arities[i] != 2 and arities[i + 1] == 2:
                (arities[i], arities[i + 1]) = (arities[i + 1], arities[i])
        random.shuffle(card_schemes) # avoid being stuck with a card scheme incompatible with a small arity
        max_tries -= 1
        for (scheme, arity) in zip(card_schemes, arities):
            if "_" in scheme and arity == 1:
                break # A reflexive association cannot be weak
            if "/" in scheme and arity < 3:
                break # A cluster association is better with at least 3 entities
            if "11" in scheme and (arity > 2 or "/" in scheme):
                break # A DF is better with at most 2 entities or a cluster
        else:
            # All associations are compatible with their card schemes
            break
    else:
        raise MocodoError(28, _("Cannot find a suitable combination of card schemes and arities."))  # fmt: skip

    for key in ("assoc_attrs", "composite_ids"):
        settings[key] = random_booleans(n, settings[key])
    
    ent_attr_names = []
    for is_composite in settings["composite_ids"]:
        if is_composite:
            ent_attr_names.append([f"{id_base}", f"_{id_base}"] + [f"{attr_base}"] * random.randint(0, settings["ent_attrs"] - 2))
        else:
            ent_attr_names.append([f"{id_base}"] + [f"{attr_base}"] * random.randint(0, settings["ent_attrs"] - 1))
    
    if "from_scratch" in subargs:
        source = f"ENTITY_NAME_PLACEHOLDER 1_: {id_base} 1 1, {attr_base} 1 2, {attr_base} 1 3\n"

    tree = parse_source(source)
    entities = [node.children[0].children[0].value for node in tree.find_data("entity_name_def")]
    associations = [node.children[0].children[0].value for node in tree.find_data("assoc_name_def")]
    counter = len(entities) + len(associations) + 1

    clauses = [source]
    ref_pool = []
    weak_entities = set()
    for i in range(settings["n"] - settings["doubles"]):

        if arities[i] == 1:
            # to keep the MCD connected, don't create a new entity if the association is reflexive
            old_entity = biased_choice(entities)
            refs = [old_entity, old_entity]
        else:
            # Normal case: create a new entity
            new_entity = f"ENTITY_NAME_PLACEHOLDER {counter}_"
            new_ent_attrs = [f"{ent_attr_name} {counter} {j}" for (j, ent_attr_name) in enumerate(ent_attr_names[i], 1)]
            clauses.append(f"{new_entity}: {', '.join(new_ent_attrs)}")
            try: # Prefer all distinct entities
                old_refs = biased_sample(entities, arities[i] - 1)
            except ValueError: # If there are not enough entities, allow reflexive associations
                old_refs = [biased_choice(entities) for _ in range(arities[i] - 1)]
            refs = [new_entity] + old_refs
            entities.append(new_entity)
            counter += 1
        
        new_association = f"{association_bases[arities[i]]} {counter}_"
        ref_pool.append(refs)
        cards = calculate_cards(card_schemes[i], refs)
        clauses.append(", ".join([new_association] + [f"{card} {ref}" for (card, ref) in zip(cards, refs)]))
        weak_entities.update(extract_weak_entities(cards, refs))
        new_assoc_attrs = [f"{attr_base} {counter} {j}" for j in range(1, settings["assoc_attrs"][i] + 1)]
        if new_assoc_attrs:
            clauses[-1] += f": {', '.join(new_assoc_attrs)}"
        associations.append(new_association)
        counter += 1
    for i in range(settings["n"] - settings["doubles"], settings["n"]):
        refs = biased_choice(ref_pool)
        arity = len(set(refs))
        new_association = f"{association_bases[arity]} {counter}_"
        cards = calculate_cards(card_schemes[i], refs)
        clauses.append(", ".join([new_association] + [f"{card} {ref}" for (card, ref) in zip(cards, refs)]))
        weak_entities.update(extract_weak_entities(cards, refs))
        new_assoc_attrs = [f"{attr_base} {counter} {j}" for j in range(1, settings["assoc_attrs"][i] + 1)]
        if new_assoc_attrs:
            clauses[-1] += f": {', '.join(new_assoc_attrs)}"
        associations.append(new_association)
        counter += 1
    
    text = "\n".join(clauses)

    j = len("ENTITY_NAME_PLACEHOLDER")
    for e in weak_entities:
        text = re.sub(fr"\b{e}\b", lambda m: f"{weak_entity_base}{m.group(0)[j:]}", text)
    text = text.replace("ENTITY_NAME_PLACEHOLDER", entity_base)
    
    return text
