import collections
from pathlib import Path
import re

from ..mocodo_error import MocodoError


def set_defaults(template):
    result = {
        "transform_attribute": [],
        "transform_title": [],
        "transform_data_type": [],
        "compose_label_disambiguated_by_note": "{label_before_disambiguation} {leg_note}",
        "compose_label_disambiguated_by_number": "{label_before_disambiguation}.{disambiguation_number}",
        "compose_primary_key": "_{label}_",
        "compose_normal_attribute": "{label}",
        "compose_foreign_key": "#{label}",
        "compose_primary_foreign_key": "_#{label}_",
        "add_alt_constraints": [],
        "transform_relation_name": [],
        "column_separator": ", ",
        "compose_relation": "{this_relation_name} ({columns})",
        "deleted_relation_separator": "",
        "compose_deleted_relation": "",
        "compose_deleted_relations": "",
        "transform_forced_relation": [],
        "transform_relation": [],
        "relation_separator": "\n",
        "compose_relational_schema": "{relations}",
        "transform_relational_schema": [],
    }
    result.update(template)
    result.setdefault("compose_naturalized_foreign_key", result["compose_normal_attribute"])
    result.setdefault("compose_primary_naturalized_foreign_key", result["compose_primary_key"])
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
    result.setdefault("compose_stopped_foreign_key", result["compose_foreign_key"])
    result.setdefault("compose_outer_attribute", result["compose_normal_attribute"])
    result.setdefault("compose_parent_primary_key", result["compose_primary_foreign_key"])
    result.setdefault("compose_strengthening_primary_foreign_key", result["compose_primary_foreign_key"])
    result.setdefault("compose_strengthening_primary_naturalized_foreign_key", result["compose_primary_key"])
    result.setdefault("compose_unsourced_foreign_key", result["compose_normal_attribute"])
    result.setdefault("compose_unsourced_primary_foreign_key", result["compose_primary_key"])
    result.setdefault("compose_naturalized_foreign_key", result["compose_normal_attribute"])
    result.setdefault("compose_primary_naturalized_foreign_key", result["compose_primary_key"])
    result.setdefault("compose_deleted_child_naturalized_foreign_key", result["compose_normal_attribute"])
    result.setdefault("compose_deleted_parent_naturalized_foreign_key", result["compose_normal_attribute"])
    result.setdefault("compose_stopped_naturalized_foreign_key", result["compose_normal_attribute"])
    result.setdefault("compose_unsourced_naturalized_foreign_key", result["compose_normal_attribute"])
    result.setdefault("compose_unsourced_primary_naturalized_foreign_key", result["compose_primary_key"])
    return result


class Relations:

    def __init__(self, mcd, params):
        
        def set_disambiguation_strategy(strategy):
            if strategy == "numbers_only":
                def inner_function(template):
                    for relation in self.relations.values():
                        for column in relation["columns"]:
                            column["label"] = column["label_before_disambiguation"]
            elif strategy == "notes":
                def inner_function(template):
                    for relation in self.relations.values():
                        for column in relation["columns"]:
                            if column["leg_note"] is None:
                                column["label"] = column["label_before_disambiguation"]
                            else:
                                column["label"] = template["compose_label_disambiguated_by_note"].format(**column)
                                
            else:
                raise NotImplemented
            return inner_function
        
        self.mcd = mcd
        self.output_stem = Path(params["output_name"]).stem
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
        self.delete_deletable_relations()
        self.make_primary_keys_first()
        self.may_disambiguate_with_leg_notes = set_disambiguation_strategy(params["disambiguation"])
        self.relations = dict(sorted(self.relations.items()))

    
    def get_text(self, template):
        
        def transform(string, transformation):
            for d in template[transformation]:
                while True:
                    try:
                        (string, n) = re.subn(d["search"], d["replace"], str(string))
                    except:
                        raise MocodoError(27, _('Cannot compile the regular expression "{regex}" or the remplacement string "{replace}" in a relation template producing "*{stem_suffix}.{extension}" files.').format(regex=d["search"], replace=d["replace"], stem_suffix=template["stem_suffix"], extension=template["extension"])) # fmt: skip
                    if n == 0 or not d.get("iterated"):
                        break
            return string
        
        template = set_defaults(template)
        
        def make_label_before_disambiguations_from_attributes():
            for relation in self.relations.values():
                for column in relation["columns"]:
                    column["label_before_disambiguation"] = transform(column["attribute"], "transform_attribute")
        make_label_before_disambiguations_from_attributes()
        
        def make_labels_from_label_before_disambiguations():
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
        make_labels_from_label_before_disambiguations()
        
        data = {}
        data["stem"] = self.output_stem
        data["title"] = transform(self.mcd.title, "transform_title")
        lines = []
        for (__, relation) in sorted(self.relations.items()): # For the double underscore, see __main__.py
            data["this_relation_name"] = transform(relation["this_relation_name"], "transform_relation_name")
            data["is_forced"] = relation["is_forced"]
            fields = []
            for column in relation["columns"]:
                column["data_type"] = transform(column["data_type"], "transform_data_type")
                data.update(column)
                field = template["compose_%s" % column["nature"]].format(**data)
                if column["alt_groups"]:
                    field = transform(field, "add_alt_constraints").format(**data)
                fields.append(field)
            data["columns"] = template["column_separator"].join(fields)
            line = template["compose_relation"].format(**data)
            if relation["is_forced"]:
                line = transform(line, "transform_forced_relation")
            line = transform(line, "transform_relation")
            lines.append(line)
        if template.get("stem_suffix") == "_mld" and template.get("extension") == "mcd": # relational diagram
            lines = self.map_mcd_layout_onto_mld(lines)
        data["relations"] = template["relation_separator"].join(lines)

        if self.deleted_relations:
            lines = []
            for deleted_relation in self.deleted_relations:
                lines.append(template["compose_deleted_relation"].format(this_relation_name=deleted_relation))
            deleted_relation_lines = template["deleted_relation_separator"].join(lines)
            data["deleted_relations"] = template["compose_deleted_relations"].format(deleted_relation_lines=deleted_relation_lines)
        else:
            data["deleted_relations"] = ""

        data["relations"] = template["compose_relational_schema"].format(**data)
        result = transform(data["relations"], "transform_relational_schema")
        return result


    # private

    def map_mcd_layout_onto_mld(self, lines):
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
        return lines

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
                        raise MocodoError(11, _('Reciprocal relative identification around {association}.').format(association=association.name)) # fmt: skip

    def relations_from_entities(self):
        for (name, entity) in self.mcd.entities.items():
            self.relations[name] = {
                "this_relation_name": entity.name,
                "is_forced": False, # an entity naturally results in a relation. No need to force it.
                "is_protected": entity.is_protected,
                "columns": []
            }
            for attribute in entity.attributes:
                if attribute.label.strip() == "":
                    continue # ignore empty attributes
                nature = "primary_key" if attribute.kind in ("strong", "weak") else "normal_attribute"
                alt_groups = "".join(c for c in sorted(attribute.id_groups) if c != "0")
                self.relations[name]["columns"].append({
                    "attribute": attribute.label,
                    "data_type": attribute.data_type,
                    "adjacent_source": None,
                    "outer_source": None,
                    "association_name": None,
                    "leg_note": None,
                    "primary": nature == "primary_key",
                    "nature": nature,
                    "alt_groups": alt_groups,
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
                        # find the potential note on the strengthening leg
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
                                "nature": "strengthening_primary_foreign_key",
                                "alt_groups": "",
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
        for inheritance in self.mcd.inheritances:
            parent_leg = inheritance.legs[0]
            if inheritance.kind in ("<-", "<="):
                for child_leg in inheritance.legs[1:]:
                    result.add(child_leg.entity_name)
            elif inheritance.kind == "=>":
                if "T" not in inheritance.name_view:
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
        for inheritance in self.mcd.inheritances:
            parent_leg = inheritance.legs[0]
            to_be_deleted = parent_leg.entity_name in self.inheritance_parent_or_children_to_delete
            for child_leg in inheritance.legs[1:]: 
                self.relations[child_leg.entity_name]["columns"][0:0] = [{
                    "attribute": attribute["attribute"],
                    "data_type": attribute["data_type"],
                    "adjacent_source": parent_leg.entity_name,
                    "outer_source": parent_leg.entity_name,
                    "leg_note": None,
                    "association_name": inheritance.name,
                    "primary": True,
                    "nature": "deleted_parent_primary_key" if to_be_deleted else "parent_primary_key",
                    "alt_groups": "",
                } for attribute in self.relations[parent_leg.entity_name]["columns"] if attribute["primary"]]

    def strengthen_parents(self):
        """
        Migrate the optional children's discriminants in their parent when it disappears (totality + =>).
        In this case, this discriminant should further migrate with the identifier of the parent.
        """
        for inheritance in self.mcd.inheritances:
            if inheritance.kind == "=>":
                parent_leg = inheritance.legs[0]
                self.relations[parent_leg.entity_name]["columns"].extend({ 
                    "attribute": attribute.label,
                    "data_type": attribute.data_type or (f"INTEGER UNSIGNED{'' if 'T' in inheritance.name_view else ' NOT NULL'}"),
                    "adjacent_source": None,
                    "outer_source": None,
                    "association_name": inheritance.name,
                    "leg_note": None,
                    "primary": False,
                    "nature": f"deleted_parent_discriminant_{inheritance.name_view}",
                    "alt_groups": "",
                } for attribute in inheritance.attributes)

    def process_associations(self):
        for association in self.mcd.associations.values():
            df_leg = None
            for leg in association.legs:
                if leg.card[1] == "1":
                    df_leg = leg
                    if leg.card[0] == "1":
                        break # elect the first leg with cardinality 11
            if df_leg is None or association.is_protected:
                # make a relation of this association
                self.relations[association.name] = {
                    "this_relation_name": association.name,
                    "is_forced": bool(df_leg), # if this association has a 11 leg, being here means it is protected: it must be forced into a relation
                    "columns": []
                }
                for leg in association.legs:
                    for attribute in self.relations[leg.entity_name]["columns"]:
                        if attribute["primary"]:
                            outer_source = self.may_retrieve_distant_outer_source(leg, attribute)
                            if leg.kind in ("cluster_peg", "cluster_leg"):
                                self.relations[association.name]["columns"].append({ # gather all migrant attributes
                                    "attribute": attribute["attribute"],
                                    "data_type": attribute["data_type"],
                                    "adjacent_source": leg.entity_name,
                                    "outer_source": outer_source,
                                    "leg_note": leg.note,
                                    "association_name": association.name,
                                    "primary": leg.is_in_elected_group,
                                    "nature": "primary_foreign_key" if leg.is_in_elected_group else "foreign_key",
                                    "alt_groups": leg.alt_groups,
                                })
                            elif association.is_protected and df_leg is not None and leg is not df_leg:
                                self.relations[association.name]["columns"].append({ # gather all migrant attributes
                                    "attribute": attribute["attribute"],
                                    "data_type": attribute["data_type"],
                                    "adjacent_source": leg.entity_name,
                                    "outer_source": outer_source,
                                    "leg_note": leg.note,
                                    "association_name": association.name,
                                    "primary": False,
                                    "nature": "stopped_foreign_key",
                                    "alt_groups": "",
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
                                    "nature": "unsourced_primary_foreign_key" if outer_source is None else "primary_foreign_key",
                                    "alt_groups": "",
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
                                "nature": attribute["nature"],
                                "alt_groups": "",
                            })
                self.relations[association.name]["columns"].extend({ # and the attributes already existing in the association
                        "attribute": attribute.label,
                        "data_type": attribute.data_type,
                        "adjacent_source": None,
                        "outer_source": None,
                        "association_name": association.name,
                        "leg_note": None,
                        "primary": False,
                        "nature": "association_attribute",
                        "alt_groups": "",
                    } for attribute in association.attributes if attribute.label.strip() != ""
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
                                        "nature": "unsourced_foreign_key" if outer_source is None else "foreign_key",
                                        "alt_groups": "",
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
                                        "nature": attribute["nature"],
                                        "alt_groups": "",
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
                        "alt_groups": "",
                    } for attribute in association.attributes if attribute.label.strip() != ""])


    def process_inheritances(self):
        for inheritance in self.mcd.inheritances:
            parent_leg = inheritance.legs[0]
            if inheritance.kind == "=>": # total migration: parent > children
                for child_leg in inheritance.legs[1:]: 
                    # migrate the parent's attributes, except those of nature "deleted_parent_discriminant"
                    self.relations[child_leg.entity_name]["columns"][0:0] = [{
                        "attribute": attribute["attribute"],
                        "data_type": attribute["data_type"],
                        "adjacent_source": parent_leg.entity_name,
                        "outer_source": self.may_retrieve_distant_outer_source(parent_leg, attribute),
                        "leg_note": self.may_retrieve_distant_leg_note(parent_leg, attribute),
                        "association_name": inheritance.name,
                        "primary": False,
                        "nature": "deleted_parent_foreign_key" if attribute["nature"] == "foreign_key" else "deleted_parent_attribute",
                        "alt_groups": "",
                    } for attribute in self.relations[parent_leg.entity_name]["columns"] if not attribute["primary"] and not attribute["nature"].startswith("deleted_parent_discriminant")]
            else: # migration: triangle attributes > parent
                self.relations[parent_leg.entity_name]["columns"].extend({ 
                    "attribute": attribute.label,
                    "data_type": attribute.data_type or (f"INTEGER UNSIGNED{'' if 'T' in inheritance.name_view else ' NOT NULL'}"),
                    "adjacent_source": None,
                    "outer_source": None,
                    "association_name": inheritance.name,
                    "leg_note": None,
                    "primary": False,
                    "nature": f"deleted_child_discriminant_{inheritance.name_view}", # "", "X", "T" or "XT"
                    "alt_groups": "",
                } for attribute in inheritance.attributes)
                if inheritance.kind in ("<-", "<="): # migration: children > parent, and suppress children
                    for child_leg in inheritance.legs[1:]:
                        if inheritance.kind == "<=":
                            # make the child's name a boolean attribute of the parent
                            self.relations[parent_leg.entity_name]["columns"].append({
                                "attribute": child_leg.entity_name,
                                "data_type": "BOOLEAN",
                                "adjacent_source": child_leg.entity_name,
                                "outer_source": child_leg.entity_name,
                                "leg_note": None,
                                "association_name": inheritance.name,
                                "primary": False,
                                "nature": "deleted_child_entity_name",
                                "alt_groups": "",
                            })
                        # migrate all child's attributes
                        for attribute in self.relations[child_leg.entity_name]["columns"]:
                            if attribute["nature"].endswith("parent_primary_key"):
                                continue # except the "strengthening" parent identifier
                            self.relations[parent_leg.entity_name]["columns"].append({
                                "attribute": attribute["attribute"],
                                "data_type": attribute["data_type"],
                                "adjacent_source": child_leg.entity_name,
                                "outer_source": self.may_retrieve_distant_outer_source(child_leg, attribute),
                                "leg_note": self.may_retrieve_distant_leg_note(child_leg, attribute),
                                "association_name": inheritance.name,
                                "primary": False,
                                "nature": "deleted_child_foreign_key" if attribute["nature"] == "foreign_key" else "deleted_child_attribute",
                                "alt_groups": "",
                            })
    
    def delete_inheritance_parent_or_children_to_delete(self):
        for entity_to_delete in self.inheritance_parent_or_children_to_delete:
            del self.relations[entity_to_delete]

    def delete_deletable_relations(self):
        deleted_outer_sources = set()
        for (name, relation) in list(self.relations.items()):
            if not relation.get("is_protected") and all(column["nature"] == "primary_key" for column in relation["columns"]):
                del self.relations[name]
                deleted_outer_sources.add(name)
        for relation in self.relations.values():
            for column in relation["columns"]:
                if column["outer_source"] in deleted_outer_sources:
                    column["nature"] = column["nature"].replace("foreign", "naturalized_foreign")
        self.deleted_relations = sorted(deleted_outer_sources)

    def make_primary_keys_first(self):
        for relation in self.relations.values():
            relation["columns"].sort(key=lambda column: not column["primary"])
        
