import collections
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
                    # FIXME: the previous version said:
                    # if column["foreign"] and column["outer_source"] and column["nature"] != "strengthening_primary_key":
                    if column["outer_source"] and column["nature"] != "strengthening_primary_key":
                        counter[(column["outer_source"], column["attribute"])] += 1
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
        self.inheritance_parent_or_children_to_delete = self.find_inheritance_parent_or_children_to_delete()
        self.strengthen_children()
        self.strengthen_parents()
        self.process_associations()
        self.process_inheritances()
        self.delete_inheritance_parent_or_children_to_delete()
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
              "compose_primary_foreign_key": "_#{label}_",
              "transform_relation_name": [],
              "column_sorting_key": {
                "search": "(.+)",
                "replace": "\\1"
              },
              "column_separator": ", ",
              "compose_relation": "{this_relation_name} ({columns})",
              "transform_single_column_relation": [],
              "transform_forced_relation": [],
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
            result.setdefault("compose_association_attribute", result["compose_normal_attribute"])
            result.setdefault("compose_deleted_child_attribute", result["compose_normal_attribute"])
            result.setdefault("compose_deleted_child_discriminant_", result["compose_normal_attribute"])
            result.setdefault("compose_deleted_child_discriminant_T", result["compose_normal_attribute"])
            result.setdefault("compose_deleted_child_discriminant_X", result["compose_normal_attribute"])
            result.setdefault("compose_deleted_child_discriminant_XT", result["compose_normal_attribute"])
            result.setdefault("compose_deleted_child_entity_name", result["compose_normal_attribute"])
            result.setdefault("compose_deleted_child_foreign_key", result["compose_foreign_key"])
            result.setdefault("compose_deleted_parent_discriminant_", result["compose_normal_attribute"])
            result.setdefault("compose_deleted_parent_discriminant_T", result["compose_normal_attribute"])
            result.setdefault("compose_deleted_parent_discriminant_X", result["compose_normal_attribute"])
            result.setdefault("compose_deleted_parent_discriminant_XT", result["compose_normal_attribute"])
            result.setdefault("compose_deleted_parent_attribute", result["compose_normal_attribute"])
            result.setdefault("compose_deleted_parent_foreign_key", result["compose_foreign_key"])
            result.setdefault("compose_deleted_parent_primary_key", result["compose_primary_key"])
            result.setdefault("compose_demoted_foreign_key", result["compose_foreign_key"])
            result.setdefault("compose_stopped_foreign_key", result["compose_foreign_key"])
            result.setdefault("compose_outer_attribute", result["compose_normal_attribute"])
            result.setdefault("compose_parent_primary_key", result["compose_primary_foreign_key"])
            result.setdefault("compose_strengthening_primary_key", result["compose_primary_foreign_key"])
            result.setdefault("compose_unsourced_foreign_key", result["compose_normal_attribute"])
            result.setdefault("compose_unsourced_primary_foreign_key", result["compose_primary_key"])
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
            data["is_forced"] = relation["is_forced"]
            fields = []
            for column in relation["columns"]:
                data.update(column)
                data["outer_source_lowercase"] = data["outer_source"] and data["outer_source"].lower()
                data["outer_source_uppercase"] = data["outer_source"] and data["outer_source"].upper()
                data["outer_source_titlecase"] = data["outer_source"] and data["outer_source"].capitalize()
                data["association_name_lowercase"] = data["association_name"] and data["association_name"].lower()
                data["association_name_uppercase"] = data["association_name"] and data["association_name"].upper()
                data["association_name_titlecase"] = data["association_name"] and data["association_name"].capitalize()
                fields.append(template["compose_%s" % column["nature"]].format(**data))
            data["sorted_columns"] = template["column_separator"].join(sorted(fields, key=lambda field: extract_sorting_key(field, "column_sorting_key")))
            data["columns"] = template["column_separator"].join(fields)
            line = template["compose_relation"].format(**data)
            if len(relation["columns"]) == 1:
                line = transform(line, "transform_single_column_relation")
            if relation["is_forced"]:
                line = transform(line, "transform_forced_relation")
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

    def may_retrieve_distant_leg_note(self, leg, attribute):
        if leg.entity_name in self.inheritance_parent_or_children_to_delete:
            for d in self.relations[leg.entity.name]["columns"]:
                if d["attribute"] == attribute["attribute"] and d["adjacent_source"] == attribute["adjacent_source"]:
                    return d["leg_note"]
        return leg.note

    def may_retrieve_distant_outer_source(self, leg, attribute):
        if leg.entity_name in self.inheritance_parent_or_children_to_delete:
            for d in self.relations[leg.entity_name]["columns"]:
                if d["attribute"] == attribute["attribute"] and d["adjacent_source"] == attribute["adjacent_source"]:
                    return d["outer_source"]
        return leg.entity_name

    def ensure_no_reciprocical_relative_entities(self):
        for association in self.mcd.associations.values():
            weak_count = 0
            for leg in association.legs:
                if leg.kind == "strengthening":
                    weak_count += 1
                    if weak_count == 2:
                        raise MocodoError(22, _('Reciprocal relative identification around {association}.').format(association=association.name)) # fmt: skip

    def relations_from_entities(self):
        for (name, entity) in self.mcd.entities.items():
            self.relations[name] = {
                "this_relation_name": entity.name,
                "is_forced": False,
                "columns": []
            }
            for attribute in entity.attributes:
                self.relations[name]["columns"].append({
                    "attribute": attribute.label,
                    "data_type": attribute.data_type,
                    "adjacent_source": None,
                    "outer_source": None,
                    "association_name": None,
                    "leg_note": None,
                    "primary": attribute.get_category() in ("strong", "weak"),
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
                                "adjacent_source": strengthening_entity.name,
                                "outer_source": strengthening_entity.name,
                                "association_name": association.name,
                                "leg_note": leg_note,
                                "primary": True,
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
                    remaining_entity_names = ", ".join('"%s"' % entity.name for entity in remaining_entities)
                    raise MocodoError(17, _('Cycle of weak entities in {entities}.').format(entities=remaining_entity_names)) # fmt: skip

    def find_inheritance_parent_or_children_to_delete(self):
        result = set()
        for association in self.mcd.associations.values():
            if not association.kind.startswith("inheritance"):
                continue
            parent_leg = association.legs[0]
            if association.kind[-2:] in ("<-", "<="):
                for child_leg in association.legs[1:]:
                    result.add(child_leg.entity_name)
            elif association.kind[-2:] == "=>":
                if "T" not in association.name:
                    raise MocodoError(25, _('Totality (/T\\ or /XT\\) is mandatory for "=>" inheritance of parent {name}.').format(name=parent_leg.entity_name)) # fmt: skip
                result.add(parent_leg.entity_name)
        return result

    def strengthen_children(self):
        """
        Migrate the parent's identifier in the children. This is obviously necessary if the parent
        must disappear (`=>` + totality) or its attributes copied in its children. Otherwise, the
        children must disappear. But in the case they are connected to other entities, they need
        an identifier to make possible to apply the remaining rules.
        """
        for association in self.mcd.associations.values():
            if not association.kind.startswith("inheritance"):
                continue
            parent_leg = association.legs[0]
            to_be_deleted = parent_leg.entity_name in self.inheritance_parent_or_children_to_delete
            for child_leg in association.legs[1:]: 
                self.relations[child_leg.entity_name]["columns"][0:0] = [{
                    "attribute": attribute["attribute"],
                    "data_type": attribute["data_type"],
                    "adjacent_source": parent_leg.entity_name,
                    "outer_source": parent_leg.entity_name,
                    "leg_note": parent_leg.note,
                    "association_name": association.name,
                    "primary": True,
                    "nature": "deleted_parent_primary_key" if to_be_deleted else "parent_primary_key"
                } for attribute in self.relations[parent_leg.entity_name]["columns"] if attribute["primary"]]

    def strengthen_parents(self):
        """
        Migrate the optional children's discriminants in their parent when it disappears (totality + =>).
        In this case, this discriminant should further migrate with the identifier of the parent.
        """
        for association in self.mcd.associations.values():
            if association.kind == "inheritance: =>":
                parent_leg = association.legs[0]
                self.relations[parent_leg.entity_name]["columns"].extend({ 
                    "attribute": attribute.label,
                    "data_type": attribute.data_type or (f"INTEGER UNSIGNED{'' if 'T' in association.name else ' NOT NULL'}"),
                    "adjacent_source": None,
                    "outer_source": None,
                    "association_name": association.name, # "", "X", "T" or "XT"
                    "leg_note": None,
                    "primary": False,
                    "nature": f"deleted_parent_discriminant_{association.name_view}"
                } for attribute in association.attributes)

    def process_associations(self):
        for association in self.mcd.associations.values():
            if association.kind.startswith("inheritance"):
                continue
            df_leg = None
            for leg in association.legs:
                if leg.card[1] == "1":
                    df_leg = leg
                    if leg.card[0] == "1":
                        break # elect the first leg with cardinality 11
            if df_leg is None or association.kind == "forced_table":
                # make a relation of this association
                self.relations[association.name] = {
                    "this_relation_name": association.name,
                    "is_forced": bool(df_leg),
                    "columns": []
                }
                for leg in association.legs:
                    for attribute in self.relations[leg.entity_name]["columns"]:
                        if attribute["primary"]:
                            outer_source = self.may_retrieve_distant_outer_source(leg, attribute)
                            if leg.kind == "cluster_peg":
                                self.relations[association.name]["columns"].append({ # gather all migrant attributes
                                    "attribute": attribute["attribute"],
                                    "data_type": attribute["data_type"],
                                    "adjacent_source": leg.entity_name,
                                    "outer_source": outer_source,
                                    "leg_note": leg.note,
                                    "association_name": association.name,
                                    "primary": False,
                                    "nature": "demoted_foreign_key"
                                })
                            elif association.kind == "forced_table" and df_leg is not None and leg is not df_leg:
                                self.relations[association.name]["columns"].append({ # gather all migrant attributes
                                    "attribute": attribute["attribute"],
                                    "data_type": attribute["data_type"],
                                    "adjacent_source": leg.entity_name,
                                    "outer_source": outer_source,
                                    "leg_note": leg.note,
                                    "association_name": association.name,
                                    "primary": False,
                                    "nature": "stopped_foreign_key"
                                })
                            else:
                                self.relations[association.name]["columns"].append({ # gather all migrant attributes
                                    "attribute": attribute["attribute"],
                                    "data_type": attribute["data_type"],
                                    "adjacent_source": leg.entity_name,
                                    "outer_source": outer_source,
                                    "leg_note": leg.note,
                                    "association_name": association.name,
                                    "primary": True,
                                    "nature": "unsourced_primary_foreign_key" if outer_source is None else "primary_foreign_key"
                                })
                        elif attribute["nature"].startswith("deleted_parent_discriminant"):
                            self.relations[association.name]["columns"].append({
                                "attribute": attribute["attribute"],
                                "data_type": attribute["data_type"],
                                "adjacent_source": leg.entity_name,
                                "outer_source": None,
                                "leg_note": leg.note,
                                "association_name": association.name,
                                "primary": False,
                                "nature": attribute["nature"]
                            })
                self.relations[association.name]["columns"].extend({ # and the attributes already existing in the association
                        "attribute": attribute.label,
                        "data_type": attribute.data_type,
                        "adjacent_source": None,
                        "outer_source": None,
                        "association_name": association.name,
                        "leg_note": None,
                        "primary": False,
                        "nature": "association_attribute"
                    } for attribute in association.attributes
                )
            else: # this association is a DF
                # The entity named `entity_name` is distinguished by the *1 cardinality
                already_rejected = False
                for leg in association.legs:
                    if leg.entity_name != df_leg.entity_name or already_rejected:
                        # This leg distinguishes one of the other entities.
                        if (df_leg.entity_name, association.name, leg.entity_name) not in self.freeze_strengthening_foreign_key_migration:
                            for attribute in list(self.relations[leg.entity_name]["columns"]): # traverse a copy...
                                # ... to prevent an infinite migration of the child discriminant
                                if attribute["primary"]:
                                    # Their primary keys must migrate in `entity_name`.
                                    outer_source = self.may_retrieve_distant_outer_source(leg, attribute)
                                    self.relations[df_leg.entity_name]["columns"].append({
                                        "attribute": attribute["attribute"],
                                        "data_type": attribute["data_type"],
                                        "adjacent_source": leg.entity_name,
                                        "outer_source": outer_source,
                                        "leg_note": leg.note,
                                        "association_name": association.name,
                                        "primary": False,
                                        "nature": "unsourced_foreign_key" if outer_source is None else "foreign_key"
                                        # NB: technically, an unsourced foreign key is not foreign anymore
                                    })
                                elif attribute["nature"].startswith("deleted_parent_discriminant"):
                                    self.relations[df_leg.entity_name]["columns"].append({
                                        "attribute": attribute["attribute"],
                                        "data_type": attribute["data_type"],
                                        "adjacent_source": leg.entity_name,
                                        "outer_source": None,
                                        "leg_note": leg.note,
                                        "association_name": association.name,
                                        "primary": False,
                                        "nature": attribute["nature"]
                                    })
                    else:
                        already_rejected = True
                self.relations[df_leg.entity_name]["columns"].extend([{
                        "attribute": attribute.label,
                        "data_type": attribute.data_type,
                        "association_name": association.name,
                        "adjacent_source": None,
                        "outer_source": None,
                        "leg_note": None,
                        "primary": False,
                        "nature": "outer_attribute",
                    } for attribute in association.attributes])


    def process_inheritances(self):
        for association in self.mcd.associations.values():
            if not association.kind.startswith("inheritance"):
                continue
            parent_leg = association.legs[0]
            if association.kind[-2:] == "=>": # total migration: parent > children
                for child_leg in association.legs[1:]: 
                    # migrate the parent's attributes, except those of nature "deleted_parent_discriminant"
                    self.relations[child_leg.entity_name]["columns"][0:0] = [{
                        "attribute": attribute["attribute"],
                        "data_type": attribute["data_type"],
                        "adjacent_source": parent_leg.entity_name,
                        "outer_source": self.may_retrieve_distant_outer_source(parent_leg, attribute),
                        "leg_note": self.may_retrieve_distant_leg_note(parent_leg, attribute),
                        "association_name": association.name,
                        "primary": False,
                        "nature": "deleted_parent_foreign_key" if attribute["nature"] == "foreign_key" else "deleted_parent_attribute"
                    } for attribute in self.relations[parent_leg.entity_name]["columns"] if not attribute["primary"] and not attribute["nature"].startswith("deleted_parent_discriminant")]
            else: # migration: triangle attributes > parent
                self.relations[parent_leg.entity_name]["columns"].extend({ 
                    "attribute": attribute.label,
                    "data_type": attribute.data_type or (f"INTEGER UNSIGNED{'' if 'T' in association.name else ' NOT NULL'}"),
                    "adjacent_source": None,
                    "outer_source": None,
                    "association_name": association.name,
                    "leg_note": None,
                    "primary": False,
                    "nature": f"deleted_child_discriminant_{association.name_view}" # "", "X", "T" or "XT"
                } for attribute in association.attributes)
                if association.kind[-2:] in ("<-", "<="): # migration: children > parent, and suppress children
                    for child_leg in association.legs[1:]:
                        if association.kind[-2:] == "<=":
                            # make the child's name a boolean attribute of the parent
                            self.relations[parent_leg.entity_name]["columns"].append({
                                "attribute": child_leg.entity_name,
                                "data_type": "BOOLEAN",
                                "adjacent_source": child_leg.entity_name,
                                "outer_source": child_leg.entity_name,
                                "leg_note": parent_leg.note,
                                "association_name": association.name,
                                "primary": False,
                                "nature": "deleted_child_entity_name"
                            })
                        # migrate all child's attributes
                        for attribute in self.relations[child_leg.entity_name]["columns"]:
                            if attribute["nature"].endswith("parent_primary_key"):
                                continue # except the "strenghtening" parent identifier
                            self.relations[parent_leg.entity_name]["columns"].append({
                                "attribute": attribute["attribute"],
                                "data_type": attribute["data_type"],
                                "adjacent_source": child_leg.entity_name,
                                "outer_source": self.may_retrieve_distant_outer_source(child_leg, attribute),
                                "leg_note": self.may_retrieve_distant_leg_note(child_leg, attribute),
                                "association_name": association.name,
                                "primary": False,
                                "nature": "deleted_child_foreign_key" if attribute["nature"] == "foreign_key" else "deleted_child_attribute"
                            })
    
    def delete_inheritance_parent_or_children_to_delete(self):
        for entity_to_delete in self.inheritance_parent_or_children_to_delete:
            del self.relations[entity_to_delete]




    def make_primary_keys_first(self):
        for relation in self.relations.values():
            relation["columns"].sort(key=lambda column: not column["primary"])
        
    

if __name__=="__main__":
    import sys
    sys.path.append("/Users/aristide/Dropbox/Sites/mocodo_online/mocodo")
    from .mocodo import main
    main()
