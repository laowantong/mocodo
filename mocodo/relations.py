#!/usr/bin/python
# encoding: utf-8

import re
import collections
import itertools
import unicodedata
import os
from file_helpers import write_contents
# import pprint

class Relations:

    def __init__(self, mcd, params):
        
        def set_disambiguation_strategy(strategy):
            if strategy == "numbers_only":
                def inner_function(template):
                    for relation in self.relations.values():
                        for column in relation["columns"]:
                            column["label"] = column["raw_label"]
            elif strategy == "annotations":
                def inner_function(template):
                    for relation in self.relations.values():
                        for column in relation["columns"]:
                            column["label"] = column["raw_label"] if column["leg_annotation"] is None else template["compose_label_disambiguated_by_annotation"].format(**column)
            else:
                raise NotImplemented
            return inner_function
        
        def may_update_params_with_guessed_title():
            if not params["guess_title"]:
                return
            counter = collections.Counter()
            for d in self.relations.itervalues():
                for column in d["columns"]:
                    if column["foreign"] and column["primary_relation_name"] and column["nature"] != "strengthening_primary_key":
                        counter[(column["primary_relation_name"], column["attribute"])] += 1
                    elif column["nature"] == "primary_key":
                        counter[(d["this_relation_name"], column["attribute"])] += 1
            if not counter:
                return
            title = counter.most_common(1)[0][0][0]
            title = title.lower().replace(u"œ", "oe").replace(u"æ", "ae")
            title = unicodedata.normalize('NFKD', title).encode('ascii','ignore')
            title = re.sub("[^-A-Za-z0-9 _]", "", title)
            if params["language"].startswith("fr"):
                from pluralize_fr import pluralize
                title = " ".join(map(pluralize, title.split()))
            title = title.capitalize()
            if not title:
                return
            write_contents("%(output_name)s_new_title.txt" % params, title)
            params["title"] = title
            params["output_name"] = os.path.join(params["output_dir"], title)
        
        self.mcd = mcd
        self.freeze_strengthening_foreign_key_migration = set()
        self.relations_from_entities()
        self.strengthen_weak_identifiers()
        self.process_associations()
        self.add_sorting_this_relation_number()
        self.may_disambiguate_with_leg_annotations = set_disambiguation_strategy(params["disambiguation"])
        may_update_params_with_guessed_title()
        
    
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
              "compose_label_disambiguated_by_annotation": u"{raw_label} {leg_annotation}",
              "compose_label_disambiguated_by_number": u"{label}.{disambiguation_number}",
              "compose_primary_key": u"_{label}_",
              "compose_normal_attribute": u"{label}",
              "compose_foreign_key": u"#{label}",
              "compose_foreign_primary_key": u"_#{label}_",
              "transform_relation_name": [],
              "column_sorting_key": {
                "search": "(.+)",
                "replace": "\\1"
              },
              "column_separator": ", ",
              "compose_relation": u"{this_relation_name} ({columns})",
              "transform_single_column_relation": [],
              "transform_relation": [],
              "relation_separator": "\n",
              "relation_sorting_key": {
                "search": "(.+)",
                "replace": "\\1"
              },
              "compose_relational_schema": u"{relations}",
              "transform_relational_schema": [],
            }
            result.update(template)
            result.setdefault("compose_strengthening_primary_key", result["compose_foreign_primary_key"])
            result.setdefault("compose_demoted_foreign_key", result["compose_foreign_key"])
            result.setdefault("compose_promoting_foreign_key", result["compose_foreign_key"])
            result.setdefault("compose_foreign_attribute", result["compose_normal_attribute"])
            result.setdefault("compose_association_attribute", result["compose_normal_attribute"])
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
            self.may_disambiguate_with_leg_annotations(template)
            for relation in self.relations.values():
                occurrences = collections.Counter(column["label"] for column in relation["columns"])
                occurrences = dict(c for c in occurrences.iteritems() if c[1] > 1)
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
        for relation in sorted(self.relations.values(), key=lambda v: v["this_relation_number"]):
            data["this_relation_name"] = transform(relation["this_relation_name"], "transform_relation_name")
            data["this_relation_name_lowercase"] = data["this_relation_name"].lower()
            data["this_relation_name_uppercase"] = data["this_relation_name"].upper()
            data["this_relation_name_titlecase"] = data["this_relation_name"].capitalize()
            data["this_relation_number"] = relation["this_relation_number"]
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
                        if line.startswith(box.name + ":"):
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

    def relations_from_entities(self):
        self.relations = {}
        for (name, entity) in self.mcd.entities.iteritems():
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
                    "leg_annotation": None,
                    "primary": attribute.get_category() in ("strong", "weak"),
                    "foreign": False,
                    "nature": "primary_key" if attribute.get_category() in ("strong", "weak") else "normal_attribute"
                })

    def strengthen_weak_identifiers(self):
        for entity in self.mcd.entities.values():
            entity.is_strong_or_strengthened = not entity.strengthen_legs
        remaining_entities = [entity for entity in self.mcd.entities.values() if not entity.is_strong_or_strengthened]
        while remaining_entities:
            for entity in remaining_entities:
                strengthening_entities = []
                for strengthen_leg in entity.strengthen_legs:
                    association = strengthen_leg.association
                    for other_leg in association.legs:
                        other_entity = other_leg.entity
                        if other_entity == entity:
                            continue
                        if not other_entity.is_strong_or_strengthened:
                            break # weak entity linked to a weak entity
                        strengthening_entities.append(other_entity)
                    else:
                        continue
                    break
                if strengthening_entities:
                    for strengthening_entity in strengthening_entities:
                        self.relations[entity.name]["columns"][0:0] = [{
                                "attribute": attribute["attribute"],
                                "data_type": attribute["data_type"],
                                "primary_relation_name": strengthening_entity.name,
                                "association_name": association.cartouche,
                                "leg_annotation": None,
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
                    raise RuntimeError(("Mocodo Err.16 - " + _('A weak entity (here, {entity}) cannot be strengthened by itself.').format(entity=remaining_entities[0].name)).encode("utf8"))
                else:
                    remaining_entity_names = u", ".join('"%s"' % entity.name for entity in remaining_entities)
                    raise RuntimeError(("Mocodo Err.17 - " + _('Cycle of weak entities in {entities}.').format(entities=remaining_entity_names)).encode("utf8"))

    def process_associations(self):
        for association in self.mcd.associations.itervalues():
            (entity_name, entity_priority) = (None, 0)
            may_identify = True
            for leg in association.legs:
                current_entity_priority = (2 if leg.cards[:2] == "11" else (1 if leg.cards[1] == "1" else 0))
                if current_entity_priority > entity_priority:
                    entity_name = leg.entity_name
                    entity_priority = current_entity_priority
                may_identify = may_identify and leg.may_identify
            if entity_name is None or (entity_priority == 1 and not may_identify):
                self.relations[association.name] = {
                    "this_relation_name": association.cartouche,
                    "columns": [{
                        "attribute": attribute["attribute"],
                        "data_type": attribute["data_type"],
                        "primary_relation_name": self.mcd.entities[leg.entity_name].cartouche,
                        "leg_annotation": leg.annotation,
                        "association_name": association.cartouche,
                        "primary": leg.may_identify,
                        "foreign": True,
                        "nature": "foreign_primary_key" if leg.may_identify else ("promoting_foreign_key" if entity_priority else "demoted_foreign_key")
                    } for leg in association.legs for attribute in self.relations[leg.entity_name]["columns"] if attribute["primary"]
                    ] + [{
                        "attribute": attribute.label,
                        "data_type": attribute.data_type,
                        "primary_relation_name": None,
                        "association_name": association.cartouche,
                        "leg_annotation": None,
                        "primary": False,
                        "foreign": False,
                        "nature": "association_attribute"
                    } for attribute in association.attributes]
                }
            else:
                already_rejected = False
                for leg in association.legs:
                    if leg.entity_name != entity_name or already_rejected:
                        if (entity_name, association.name, leg.entity_name) not in self.freeze_strengthening_foreign_key_migration:
                            self.relations[entity_name]["columns"].extend({
                                "attribute": attribute["attribute"],
                                "data_type": attribute["data_type"],
                                "primary_relation_name": self.mcd.entities[leg.entity_name].cartouche,
                                "leg_annotation": leg.annotation,
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
                        "leg_annotation": None,
                        "primary": False,
                        "foreign": True,
                        "nature": "foreign_attribute",
                    } for attribute in association.attributes])

    def add_sorting_this_relation_number(self):
        this_relation_number = itertools.count(1)
        for row in self.mcd.rows:
            for box in row:
                if box.name in self.relations:
                    self.relations[box.name]["this_relation_number"] = this_relation_number.next()
    
        
    

if __name__=="__main__":
    import sys
    sys.path.append("/Users/aristide/Dropbox/Sites/mocodo_online/mocodo")
    from mocodo import main
    main()
