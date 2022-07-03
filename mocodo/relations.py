import collections
import itertools
import os
import re

from .file_helpers import write_contents
from .mocodo_error import MocodoError


class Relations:

    def __init__(self, mcd, params):
        
        def set_disambiguation_strategy(strategy):
            if strategy == "numbers_only":
                def inner_function(template):
                    for relation in self.relations.values():
                        for column in relation["columns"]:
                            column["label"] = column["raw_label"]
            elif strategy == "notes":
                def inner_function(template):
                    for relation in self.relations.values():
                        for column in relation["columns"]:
                            column["label"] = column["raw_label"] if column["leg_note"] is None else template["compose_label_disambiguated_by_note"].format(**column)
            else:
                raise NotImplemented
            return inner_function
        
        def may_update_params_with_guessed_title():
            if not params["guess_title"]:
                return
            counter = collections.Counter()
            for d in self.relations.values():
                for column in d["columns"]:
                    if column["foreign"] and column["primary_relation_name"] and column["nature"] != "strengthening_primary_key":
                        counter[(column["primary_relation_name"], column["attribute"])] += 1
                    elif column["nature"] == "primary_key":
                        counter[(d["this_relation_name"], column["attribute"])] += 1
            if not counter:
                return
            title = counter.most_common(1)[0][0][0]
            title = re.sub("[^A-Za-zÀ-ÖØ-öø-ÿ0-9 '\._-]", "-", title)
            if params["language"].startswith("fr"):
                from .pluralize_fr import pluralize
                title = " ".join(map(pluralize, title.split()))
            title = title.capitalize()
            if not title:
                return
            write_contents(f"{params['output_name']}_new_title.txt", title)
            params["title"] = title
            params["output_name"] = os.path.join(params["output_dir"], title)
        
        self.mcd = mcd
        self.ensure_no_reciprocical_relative_entities()
        self.freeze_strengthening_foreign_key_migration = set()
        self.relations = {}
        self.relations_from_entities()
        self.strengthen_weak_identifiers()
        self.process_parent_identifier_migration()
        self.process_associations()
        self.process_inheritances()
        self.make_primary_keys_first()
        self.may_disambiguate_with_leg_notes = set_disambiguation_strategy(params["disambiguation"])
        may_update_params_with_guessed_title()
        self.relations = dict(sorted(self.relations.items()))

    
    def get_text(self, template):
        
        def transform(string, transformation):
            for d in template[transformation]:
                while True:
                    (string, n) = re.subn(d["search"], d["replace"], string)
                    if n == 0 or not d.get("iterated"):
                        break
            return string
        
        def extract_sorting_key(string, transformation):
            d = template[transformation]
            return re.sub(d["search"], d["replace"], string)
        
        def set_defaults(template):
            result = {
              "transform_attribute": [],
              "transform_title": [],
              "transform_data_type": [],
              "compose_label_disambiguated_by_note": "{raw_label} {leg_note}",
              "compose_label_disambiguated_by_number": "{label}.{disambiguation_number}",
              "compose_primary_key": "_{label}_",
              "compose_normal_attribute": "{label}",
              "compose_foreign_key": "#{label}",
              "compose_foreign_primary_key": "_#{label}_",
              "transform_relation_name": [],
              "column_sorting_key": {
                "search": "(.+)",
                "replace": "\\1"
              },
              "column_separator": ", ",
              "compose_relation": "{this_relation_name} ({columns})",
              "transform_single_column_relation": [],
              "transform_relation": [],
              "relation_separator": "\n",
              "relation_sorting_key": {
                "search": "(.+)",
                "replace": "\\1"
              },
              "compose_relational_schema": "{relations}",
              "transform_relational_schema": [],
            }
            result.update(template)
            result.setdefault("compose_strengthening_primary_key", result["compose_foreign_primary_key"])
            result.setdefault("compose_demoted_foreign_key", result["compose_foreign_key"])
            result.setdefault("compose_promoting_foreign_key", result["compose_foreign_key"])
            result.setdefault("compose_foreign_attribute", result["compose_normal_attribute"])
            result.setdefault("compose_association_attribute", result["compose_normal_attribute"])
            result.setdefault("compose_child_discriminant_", result["compose_foreign_attribute"])
            result.setdefault("compose_child_discriminant_X", result["compose_foreign_attribute"])
            result.setdefault("compose_child_discriminant_T", result["compose_foreign_attribute"])
            result.setdefault("compose_child_discriminant_XT", result["compose_foreign_attribute"])
            result.setdefault("compose_parent_primary_key", result["compose_foreign_primary_key"])
            result.setdefault("compose_parent_foreign_key", result["compose_foreign_key"])
            result.setdefault("compose_parent_attribute", result["compose_foreign_attribute"])
            result.setdefault("compose_child_entity_name", result["compose_foreign_attribute"])
            result.setdefault("compose_child_key", result["compose_foreign_key"])
            result.setdefault("compose_child_attribute", result["compose_foreign_attribute"])
            result.setdefault("compose_child_foreign_key", result["compose_foreign_key"])
            return result
        template = set_defaults(template)
        
        def make_raw_labels_from_attributes():
            for relation in self.relations.values():
                for column in relation["columns"]:
                    column["raw_label"] = transform(column["attribute"], "transform_attribute")
                    column["raw_label_lowercase"] = column["raw_label"].lower()
                    column["raw_label_uppercase"] = column["raw_label"].upper()
                    column["raw_label_titlecase"] = column["raw_label"].capitalize()
        make_raw_labels_from_attributes()
        
        def make_labels_from_raw_labels():
            self.may_disambiguate_with_leg_notes(template)
            for relation in self.relations.values():
                occurrences = collections.Counter(column["label"] for column in relation["columns"])
                occurrences = dict(c for c in occurrences.items() if c[1] > 1)
                for column in reversed(relation["columns"]):
                    if column["label"] in occurrences:
                        occurrences[column["label"]] -= 1
                        if occurrences[column["label"]]:
                            column["disambiguation_number"] = occurrences[column["label"]]
                            column["label"] = template["compose_label_disambiguated_by_number"].format(**column)
                        else:
                            column["disambiguation_number"] = None
                    else:
                        column["disambiguation_number"] = None
                    column["label_lowercase"] = column["label"].lower()
                    column["label_uppercase"] = column["label"].upper()
                    column["label_titlecase"] = column["label"].capitalize()
        make_labels_from_raw_labels()
        
        # pprint.pprint(self.relations)
        data = {}
        data["title"] = transform(self.mcd.title, "transform_title")
        data["title_lowercase"] = data["title"].lower()
        data["title_uppercase"] = data["title"].upper()
        data["title_titlecase"] = data["title"].capitalize()
        lines = []
        for (_, relation) in sorted(self.relations.items()):
            data["this_relation_name"] = transform(relation["this_relation_name"], "transform_relation_name")
            data["this_relation_name_lowercase"] = data["this_relation_name"].lower()
            data["this_relation_name_uppercase"] = data["this_relation_name"].upper()
            data["this_relation_name_titlecase"] = data["this_relation_name"].capitalize()
            fields = []
            for column in relation["columns"]:
                data.update(column)
                data["primary_relation_name_lowercase"] = data["primary_relation_name"] and data["primary_relation_name"].lower()
                data["primary_relation_name_uppercase"] = data["primary_relation_name"] and data["primary_relation_name"].upper()
                data["primary_relation_name_titlecase"] = data["primary_relation_name"] and data["primary_relation_name"].capitalize()
                data["association_name_lowercase"] = data["association_name"] and data["association_name"].lower()
                data["association_name_uppercase"] = data["association_name"] and data["association_name"].upper()
                data["association_name_titlecase"] = data["association_name"] and data["association_name"].capitalize()
                fields.append(template["compose_%s" % column["nature"]].format(**data))
            data["sorted_columns"] = template["column_separator"].join(sorted(fields, key=lambda field: extract_sorting_key(field, "column_sorting_key")))
            data["columns"] = template["column_separator"].join(fields)
            line = template["compose_relation"].format(**data)
            if len(relation["columns"]) == 1:
                line = transform(line, "transform_single_column_relation")
            line = transform(line, "transform_relation")
            lines.append(line)
        if template["extension"] == ".mld":
            rows = [[]]
            all_commas = [True] * self.mcd.col_count
            for row in self.mcd.rows:
                for (i, box) in enumerate(row):
                    for line in lines:
                        if line.startswith(box.cartouche + ":"):
                            rows[-1].append(line)
                            all_commas[i] = False
                            break
                    else:
                        rows[-1].append(":")
                rows.append([])
            rows.pop()
            for row in rows:
                row[:] = [x for (x, all_comma) in zip(row, all_commas) if not all_comma]
            lines = []
            for row in rows:
                lines.append(":")
                for x in row:
                    lines.append(x)
                    lines.append(":")
                lines.append("\n")
            lines.pop()
        data["relations"] = template["relation_separator"].join(lines)
        data["sorted_relations"] = template["relation_separator"].join(sorted(lines, key=lambda line: extract_sorting_key(line, "relation_sorting_key")))
        data["relations"] = template["compose_relational_schema"].format(**data)
        result = transform(data["relations"], "transform_relational_schema")
        return result


    # private

    def ensure_no_reciprocical_relative_entities(self):
        for association in self.mcd.associations.values():
            weak_count = 0
            for leg in association.legs:
                if leg.kind == "strengthening":
                    weak_count += 1
                    if weak_count == 2:
                        raise MocodoError(22, _('Reciprocal relative identification around {association}.').format(association=association.name)) # fmt: skip
                    other_leg = leg

    def relations_from_entities(self):
        for (name, entity) in self.mcd.entities.items():
            self.relations[name] = {
                "this_relation_name": entity.cartouche,
                "columns": []
            }
            for attribute in entity.attributes:
                self.relations[name]["columns"].append({
                    "attribute": attribute.label,
                    "data_type": attribute.data_type,
                    "primary_relation_name": None,
                    "association_name": None,
                    "leg_note": None,
                    "primary": attribute.get_category() in ("strong", "weak"),
                    "foreign": False,
                    "nature": "primary_key" if attribute.get_category() in ("strong", "weak") else "normal_attribute"
                })

    def strengthen_weak_identifiers(self):
        for entity in self.mcd.entities.values():
            entity.is_strong_or_strengthened = not entity.strengthening_legs
        remaining_entities = [entity for entity in self.mcd.entities.values() if not entity.is_strong_or_strengthened]
        while remaining_entities:
            for entity in remaining_entities:
                strengthening_entities_via_associations = []
                for strengthening_leg in entity.strengthening_legs:
                    association = strengthening_leg.association
                    for other_leg in association.legs:
                        other_entity = other_leg.entity
                        if other_entity == entity:
                            continue
                        if not other_entity.is_strong_or_strengthened:
                            break # weak entity linked to a weak entity
                        strengthening_entities_via_associations.append((other_entity, association))
                    else:
                        continue
                    break
                if strengthening_entities_via_associations:
                    for (strengthening_entity, association) in strengthening_entities_via_associations:
                        # find the potential note on the strenghening leg
                        for leg in association.legs:
                            if leg.entity_name == strengthening_entity.name:
                                leg_note = leg.note
                                break
                        else:
                            leg_note = None
                        # migrate the whole primary key of the strengthening entity into the weak one
                        self.relations[entity.name]["columns"][0:0] = [{
                                "attribute": attribute["attribute"],
                                "data_type": attribute["data_type"],
                                "primary_relation_name": strengthening_entity.cartouche,
                                "association_name": association.cartouche,
                                "leg_note": leg_note,
                                "primary": True,
                                "foreign": True,
                                "nature": "strengthening_primary_key"
                            } for attribute in self.relations[strengthening_entity.name]["columns"] if attribute["primary"]]
                        self.freeze_strengthening_foreign_key_migration.add((entity.name, association.name, strengthening_entity.name))
                    remaining_entities.remove(entity)
                    entity.is_strong_or_strengthened = True
                    break
            else:
                if len(remaining_entities) == 1:
                    raise MocodoError(16, _('A weak entity (here, {entity}) cannot be strengthened by itself.').format(entity=remaining_entities[0].name)) # fmt: skip
                else:
                    remaining_entity_names = u", ".join('"%s"' % entity.name for entity in remaining_entities)
                    raise MocodoError(17, _('Cycle of weak entities in {entities}.').format(entities=remaining_entity_names)) # fmt: skip
    
    def process_parent_identifier_migration(self):
        for association in self.mcd.associations.values():
            if not association.kind.startswith("inheritance"):
                continue
            parent_leg = association.legs[0]
            if parent_leg.card in ("->", "=>"): # migration: parent > children
                for child_leg in association.legs[1:]: 
                    # migrate the parent's identifier
                    self.relations[child_leg.entity_name]["columns"][0:0] = [{
                        "attribute": attribute["attribute"],
                        "data_type": attribute["data_type"],
                        "primary_relation_name": self.mcd.entities[parent_leg.entity_name].cartouche,
                        "leg_note": parent_leg.note,
                        "association_name": association.cartouche,
                        "primary": True,
                        "foreign": True,
                        "nature": "parent_primary_key"
                    } for attribute in self.relations[parent_leg.entity_name]["columns"] if attribute["primary"]]

    def process_associations(self):
        for association in self.mcd.associations.values():
            if association.kind.startswith("inheritance"):
                continue
            (entity_name, entity_priority) = (None, 0)
            for leg in association.legs:
                if leg.card[:2] == "11":
                    entity_priority = 2
                    entity_name = leg.entity_name
                    break
                if leg.card[1] == "1":
                    entity_priority = 1
                    entity_name = leg.entity_name
            may_identify = all(leg.may_identify for leg in association.legs)
            if entity_name is None or (entity_priority == 1 and not may_identify):
                self.relations[association.name] = { # make a relation of this association
                    "this_relation_name": association.cartouche,
                    "columns": [{ # gather all migrant attributes
                        "attribute": attribute["attribute"],
                        "data_type": attribute["data_type"],
                        "primary_relation_name": self.mcd.entities[leg.entity_name].cartouche,
                        "leg_note": leg.note,
                        "association_name": association.cartouche,
                        "primary": leg.may_identify,
                        "foreign": True,
                        "nature": "foreign_primary_key" if leg.may_identify else ("promoting_foreign_key" if entity_priority else "demoted_foreign_key")
                    } for leg in association.legs for attribute in self.relations[leg.entity_name]["columns"] if attribute["primary"]
                    ] + [{ # and the attributes already existing in the association
                        "attribute": attribute.label,
                        "data_type": attribute.data_type,
                        "primary_relation_name": None,
                        "association_name": association.cartouche,
                        "leg_note": None,
                        "primary": False,
                        "foreign": False,
                        "nature": "association_attribute"
                    } for attribute in association.attributes]
                }
            else: # this association is a DF
                already_rejected = False
                for leg in association.legs:
                    if leg.entity_name != entity_name or already_rejected:
                        if (entity_name, association.name, leg.entity_name) not in self.freeze_strengthening_foreign_key_migration:
                            self.relations[entity_name]["columns"].extend({
                                "attribute": attribute["attribute"],
                                "data_type": attribute["data_type"],
                                "primary_relation_name": self.mcd.entities[leg.entity_name].cartouche,
                                "leg_note": leg.note,
                                "association_name": association.cartouche,
                                "primary": False,
                                "foreign": True,
                                "nature": "foreign_key"
                            } for attribute in self.relations[leg.entity_name]["columns"] if attribute["primary"])
                    else:
                        already_rejected = True
                self.relations[entity_name]["columns"].extend([{
                        "attribute": attribute.label,
                        "data_type": attribute.data_type,
                        "association_name": association.cartouche,
                        "primary_relation_name": None,
                        "leg_note": None,
                        "primary": False,
                        "foreign": True,
                        "nature": "foreign_attribute",
                    } for attribute in association.attributes])
    
    def process_inheritances(self):
        entities_to_delete = []
        for association in self.mcd.associations.values():
            if not association.kind.startswith("inheritance"):
                continue
            parent_leg = association.legs[0]
            if parent_leg.card != "=>": # migration: triangle attributes > parent
                self.relations[parent_leg.entity_name]["columns"].extend({ 
                    "attribute": attribute.label,
                    "data_type": attribute.data_type or (f"INTEGER UNSIGNED{'' if 'T' in association.name else ' NOT NULL'}"),
                    "primary_relation_name": None,
                    "association_name": association.cartouche,
                    "leg_note": None,
                    "primary": False,
                    "foreign": True,
                    "nature": f"child_discriminant_{association.name}"
                } for attribute in association.attributes)
            if parent_leg.card == "=>": # total migration: parent > children
                for child_leg in association.legs[1:]: 
                    # migrate the parent's attributes
                    self.relations[child_leg.entity_name]["columns"][0:0] = [{
                        "attribute": attribute["attribute"],
                        "data_type": attribute["data_type"],
                        "primary_relation_name": self.mcd.entities[parent_leg.entity_name].cartouche,
                        "leg_note": parent_leg.note,
                        "association_name": association.cartouche,
                        "primary": False,
                        "foreign": True,
                        "nature": "parent_foreign_key" if attribute["nature"] == "foreign_key" else "parent_attribute"
                    } for attribute in self.relations[parent_leg.entity_name]["columns"] if not attribute["primary"]]
            elif parent_leg.card in ("<-", "<="): # migration: children > parent
                for child_leg in association.legs[1:]:
                    if parent_leg.card == "<=":
                        # make the child's name a boolean attribute of the parent
                        self.relations[parent_leg.entity_name]["columns"].append({
                            "attribute": child_leg.entity_name,
                            "data_type": "BOOLEAN",
                            "primary_relation_name": child_leg.entity_name,
                            "leg_note": parent_leg.note,
                            "association_name": association.cartouche,
                            "primary": False,
                            "foreign": True,
                            "nature": "child_entity_name"
                        })
                    # migrate all child's attributes
                    self.relations[parent_leg.entity_name]["columns"].extend({
                        "attribute": attribute["attribute"],
                        "data_type": attribute["data_type"],
                        "primary_relation_name": child_leg.entity_name,
                        "leg_note": parent_leg.note,
                        "association_name": association.cartouche,
                        "primary": False,
                        "foreign": True,
                        "nature": "child_foreign_key" if attribute["nature"] == "foreign_key" else "child_attribute"
                    } for attribute in self.relations[child_leg.entity_name]["columns"])
                    entities_to_delete.append(child_leg.entity_name)
            if parent_leg.card == "=>" and "T" in association.name: # ensure the inheritance is total before suppressing the parent table
                entities_to_delete.append(parent_leg.entity_name)
        for entity_to_delete in entities_to_delete:
            del self.relations[entity_to_delete]

    def make_primary_keys_first(self):
        for relation in self.relations.values():
            relation["columns"].sort(key=lambda column: not column["primary"])
        
    

if __name__=="__main__":
    import sys
    sys.path.append("/Users/aristide/Dropbox/Sites/mocodo_online/mocodo")
    from .mocodo import main
    main()
