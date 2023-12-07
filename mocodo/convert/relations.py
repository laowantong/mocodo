import collections
from pathlib import Path
import re

from mocodo.tools.various import first_missing_positive

from ..mocodo_error import MocodoError
from ..version_number import version


def set_defaults(template):
    result = {
        "transform_attribute": [],
        "transform_label": [],
        "transform_title": [],
        "transform_datatype": [],
        "transform_optionality": [],
        "label_role_separator": " ",
        "compose_primary_key": "_{label}_",
        "compose_normal_attribute": "{label}",
        "compose_foreign_key": "#{label}",
        "compose_primary_foreign_key": "_#{label}_",
        "add_unicity_constraints": [],
        "add_optionality_constraints": [],
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
    result.setdefault("compose_ex_foreign_key", result["compose_normal_attribute"])
    result.setdefault("compose_primary_ex_foreign_key", result["compose_primary_key"])
    result.setdefault("compose_association_attribute", result["compose_normal_attribute"])
    result.setdefault("compose_association_primary_key", result["compose_primary_key"])
    result.setdefault("compose_deleted_child_attribute", result["compose_normal_attribute"])
    result.setdefault("compose_deleted_child_discriminator_", result["compose_normal_attribute"])
    result.setdefault("compose_deleted_child_discriminator_T", result["compose_normal_attribute"])
    result.setdefault("compose_deleted_child_discriminator_X", result["compose_normal_attribute"])
    result.setdefault("compose_deleted_child_discriminator_XT", result["compose_normal_attribute"])
    result.setdefault("compose_deleted_child_entity_name", result["compose_normal_attribute"])
    result.setdefault("compose_deleted_child_foreign_key", result["compose_foreign_key"])
    result.setdefault("compose_deleted_parent_discriminator_", result["compose_normal_attribute"])
    result.setdefault("compose_deleted_parent_discriminator_T", result["compose_normal_attribute"])
    result.setdefault("compose_deleted_parent_discriminator_X", result["compose_normal_attribute"])
    result.setdefault("compose_deleted_parent_discriminator_XT", result["compose_normal_attribute"])
    result.setdefault("compose_deleted_parent_attribute", result["compose_normal_attribute"])
    result.setdefault("compose_deleted_parent_foreign_key", result["compose_foreign_key"])
    result.setdefault("compose_deleted_parent_primary_key", result["compose_primary_key"])
    result.setdefault("compose_stopped_foreign_key", result["compose_foreign_key"])
    result.setdefault("compose_outer_attribute", result["compose_normal_attribute"])
    result.setdefault("compose_outer_primary_key", result["compose_primary_key"])
    result.setdefault("compose_parent_primary_key", result["compose_primary_foreign_key"])
    result.setdefault("compose_strengthening_primary_foreign_key", result["compose_primary_foreign_key"])
    result.setdefault("compose_strengthening_primary_ex_foreign_key", result["compose_primary_key"])
    result.setdefault("compose_unsourced_foreign_key", result["compose_normal_attribute"])
    result.setdefault("compose_unsourced_primary_foreign_key", result["compose_primary_key"])
    result.setdefault("compose_ex_foreign_key", result["compose_normal_attribute"])
    result.setdefault("compose_primary_ex_foreign_key", result["compose_primary_key"])
    result.setdefault("compose_deleted_child_ex_foreign_key", result["compose_normal_attribute"])
    result.setdefault("compose_deleted_parent_ex_foreign_key", result["compose_normal_attribute"])
    result.setdefault("compose_stopped_ex_foreign_key", result["compose_normal_attribute"])
    result.setdefault("compose_unsourced_ex_foreign_key", result["compose_normal_attribute"])
    result.setdefault("compose_unsourced_primary_ex_foreign_key", result["compose_primary_key"])
    return result


class Relations:

    def __init__(self, mcd, params):
        
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
        
        def make_non_disambiguated_labels_from_attributes():
            for relation in self.relations.values():
                for column in relation["columns"]:
                    column["non_disambiguated_label"] = transform(column["attribute"], "transform_attribute")
        make_non_disambiguated_labels_from_attributes()

        def make_labels_from_non_disambiguated_labels():
            for relation in self.relations.values():
                for column in relation["columns"]:
                    if not column["leg_note"]:
                        column["label"] = column["non_disambiguated_label"]
                    elif column["leg_note"].startswith("-"):
                        column["label"] = column["leg_note"][1:]
                    elif column["leg_note"].startswith("+"):
                        column["label"] = column["non_disambiguated_label"] + column["leg_note"][1:]
                    elif " " in column["leg_note"]:
                        column["label"] = column["non_disambiguated_label"]
                    else:
                        column["label"] = column["non_disambiguated_label"] + template["label_role_separator"] + column["leg_note"]
            # After labels have been disambiguated by roles, ensure all of them are distinct.
            for relation in self.relations.values():
                occurrences = collections.Counter(column["label"] for column in relation["columns"])
                occurrences = dict(c for c in occurrences.items() if c[1] > 1)
                for column in reversed(relation["columns"]):
                    if column["label"] in occurrences and column["nature"] != "primary_key":
                        occurrences[column["label"]] -= 1
                        column["label"] = column["label"] + template["label_role_separator"] + str(occurrences[column["label"]] + 1)
        make_labels_from_non_disambiguated_labels()

        def transform_labels(): # after labels have been disambiguated by roles
            for relation in self.relations.values():
                for column in relation["columns"]:
                    column["label"] = transform(column["label"], "transform_label")
        transform_labels()
    
        def add_fillers():
            for relation in self.relations.values():
                label_max_length = max(len(column["label"]) for column in relation["columns"])
                for column in relation["columns"]:
                    column["filler"] = " " * (label_max_length - len(column["label"]) + 1)
        add_fillers()

        data = {}
        data["stem"] = self.output_stem
        data["title"] = transform(self.mcd.title, "transform_title")
        data["version"] = version
        lines = []
        for (__, relation) in sorted(self.relations.items()): # For the double underscore, see __main__.py
            data["this_relation_name"] = transform(relation["this_relation_name"], "transform_relation_name")
            data["is_forced"] = relation["is_forced"]
            fields = []
            for column in relation["columns"]:
                column["datatype"] = transform(column["datatype"], "transform_datatype")
                column["optionality"] = transform(column["optionality"], "transform_optionality")
                data.update(column)
                field = template["compose_%s" % column["nature"]].format(**data)
                if column["unicities"]:
                    field = transform(field, "add_unicity_constraints").format(**data)
                if column["optionality"]:
                    field = transform(field, "add_optionality_constraints").format(**data)
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
                    if line.startswith(box.name_view + ":"):
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
        if leg.entity_bid in self.inheritance_parent_or_children_to_delete:
            for d in self.relations[leg.entity.bid]["columns"]:
                if d["attribute"] == attribute["attribute"] and d["adjacent_source"] == attribute["adjacent_source"]:
                    return d["leg_note"]
        return leg.note

    def may_retrieve_distant_outer_source(self, leg, attribute):
        if leg.entity_bid in self.inheritance_parent_or_children_to_delete:
            for d in self.relations[leg.entity_bid]["columns"]:
                if d["attribute"] == attribute["attribute"] and d["adjacent_source"] == attribute["adjacent_source"]:
                    return d["outer_source"]
        return leg.entity.name_view

    def ensure_no_reciprocical_relative_entities(self):
        for association in self.mcd.associations.values():
            if association.is_invisible:
                continue
            weak_count = 0
            for leg in association.legs:
                if leg.kind == "strengthening":
                    weak_count += 1
                    if weak_count == 2:
                        raise MocodoError(11, _('Reciprocal relative identification around {association}.').format(association=association.bid)) # fmt: skip

    @staticmethod
    def pop_optionality_from_datatype(attribute, is_primary = False):
        (datatype, n) = re.subn(r"(?i) *\bnot +null\b *", " ", attribute.datatype)
        attribute.datatype = datatype.strip() # suppress the NOT NULL, if any
        if n: # A NOT NULL has been suppressed
            return "!" # the attribute is mandatory (as explicitely stated)
        (datatype, n) = re.subn(r"(?i) *\bnull\b *", " ", attribute.datatype)
        attribute.datatype = datatype.strip() # suppress the NULL, if any
        if is_primary:
            return "!" # the attribute is mandatory (even if not explicitely stated)
        if n: # A NULL has been suppressed
            return "?" # the attribute is optional (as explicitely stated)
        return "" # the attribute is neither optional nor mandatory

    def relations_from_entities(self):
        for (name, entity) in self.mcd.entities.items():
            if entity.is_invisible:
                continue
            self.relations[name] = {
                "this_relation_name": entity.name_view,
                "is_forced": False, # an entity naturally results in a relation. No need to force it.
                "is_protected": entity.is_protected,
                "columns": [],
                "existing_unicity_numbers": set(),
            }
            for attribute in entity.attributes:
                if attribute.label.strip() == "":
                    continue # ignore empty attributes
                nature = "primary_key" if attribute.kind in ("strong", "weak") else "normal_attribute"
                unicities = "".join(c for c in sorted(attribute.id_groups) if c != "0")
                is_primary = (nature == "primary_key")
                optionality = self.pop_optionality_from_datatype(attribute, is_primary)
                self.relations[name]["columns"].append({
                    "attribute": attribute.label,
                    "optionality": optionality,
                    "datatype": attribute.datatype,
                    "adjacent_source": None,
                    "outer_source": None,
                    "association_name": None,
                    "leg_note": None,
                    "is_primary": is_primary,
                    "nature": nature,
                    "unicities": unicities,
                })
                self.relations[name]["existing_unicity_numbers"].update(map(int, unicities))

    def strengthen_weak_identifiers(self):
        for entity in self.mcd.entities.values():
            entity.is_strong_or_strengthened = not entity.strengthening_legs
        remaining_entities = [entity for entity in self.mcd.entities.values() if not entity.is_strong_or_strengthened and not entity.is_invisible]
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
                            if leg.entity_bid == strengthening_entity.bid:
                                leg_note = leg.note
                                break
                        else:
                            leg_note = None
                        # migrate the whole primary key of the strengthening entity into the weak one
                        self.relations[entity.bid]["columns"][0:0] = [{
                                "attribute": attribute["attribute"],
                                "optionality": "!",
                                "datatype": attribute["datatype"],
                                "adjacent_source": strengthening_entity.name_view,
                                "outer_source": strengthening_entity.name_view,
                                "association_name": association.name_view,
                                "leg_note": leg_note,
                                "is_primary": True,
                                "nature": "strengthening_primary_foreign_key",
                                "unicities": "",
                            } for attribute in self.relations[strengthening_entity.bid]["columns"] if attribute["is_primary"]]
                        self.freeze_strengthening_foreign_key_migration.add((entity.bid, association.bid, strengthening_entity.bid))
                    remaining_entities.remove(entity)
                    entity.is_strong_or_strengthened = True
                    break
            else:
                if len(remaining_entities) == 1:
                    raise MocodoError(16, _('A weak entity (here, {entity}) cannot be strengthened by itself.').format(entity=remaining_entities[0].bid)) # fmt: skip
                else:
                    remaining_entity_names = ", ".join('"%s"' % entity.raw_name for entity in remaining_entities)
                    raise MocodoError(17, _('Cycle of weak entities in {entities}.').format(entities=remaining_entity_names)) # fmt: skip

    def find_inheritance_parent_or_children_to_delete(self):
        result = set()
        for inheritance in self.mcd.inheritances:
            parent_leg = inheritance.legs[0]
            if inheritance.kind in ("<-", "<="):
                for child_leg in inheritance.legs[1:]:
                    result.add(child_leg.entity_bid)
            elif inheritance.kind == "=>":
                if "T" not in inheritance.name_view:
                    raise MocodoError(25, _('Totality (/T\\ or /XT\\) is mandatory for "=>" inheritance of parent "{name}".').format(name=parent_leg.entity_raw_name)) # fmt: skip
                result.add(parent_leg.entity_bid)
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
            to_be_deleted = parent_leg.entity_bid in self.inheritance_parent_or_children_to_delete
            for child_leg in inheritance.legs[1:]: 
                self.relations[child_leg.entity_bid]["columns"][0:0] = [{
                    "attribute": attribute["attribute"],
                    "optionality": "!",
                    "datatype": attribute["datatype"],
                    "adjacent_source": parent_leg.entity.name_view,
                    "outer_source": parent_leg.entity.name_view,
                    "association_name": inheritance.name_view,
                    "leg_note": None,
                    "is_primary": True,
                    "nature": "deleted_parent_primary_key" if to_be_deleted else "parent_primary_key",
                    "unicities": "",
                } for attribute in self.relations[parent_leg.entity_bid]["columns"] if attribute["is_primary"]]

    def strengthen_parents(self):
        """
        Migrate the optional children's discriminators in their parent when it disappears (totality + =>).
        In this case, this discriminator should further migrate with the identifier of the parent.
        """
        for inheritance in self.mcd.inheritances:
            if inheritance.kind == "=>":
                parent_leg = inheritance.legs[0]
                self.relations[parent_leg.entity_bid]["columns"].extend({ 
                    "attribute": attribute.label,
                    "optionality": "!" if 'T' in inheritance.name_view else "?",
                    "datatype": attribute.datatype or "UNSIGNED_INT_PLACEHOLDER",
                    "adjacent_source": None,
                    "outer_source": None,
                    "association_name": inheritance.name_view,
                    "leg_note": None,
                    "is_primary": False,
                    "nature": f"deleted_parent_discriminator_{inheritance.name_view}",
                    "unicities": "",
                } for attribute in inheritance.attributes)

    def process_associations(self):
        for association in self.mcd.associations.values():
            if association.is_invisible:
                continue
            is_cluster = (association.kind == "cluster")
            df_leg = None
            for leg in association.legs:
                if leg.entity.is_invisible:
                    continue
                if leg.card[1] == "1":
                    df_leg = leg
                    if leg.card[0] == "1":
                        break # elect the first leg with cardinality 11
            
            if df_leg is None or association.is_protected:
                # make a relation of this association
                self.relations[association.bid] = {
                    "this_relation_name": association.name_view,
                    "is_forced": bool(df_leg), # if this association has a 11 leg, being here means it is protected: it must be forced into a relation
                    "columns": [],
                    "existing_unicity_numbers": set(),
                }
                for leg in association.legs:
                    if leg.entity.is_invisible:
                        continue
                    for attribute in self.relations[leg.entity_bid]["columns"]:
                        if attribute["is_primary"]:
                            outer_source = self.may_retrieve_distant_outer_source(leg, attribute)
                            if is_cluster:
                                self.relations[association.bid]["columns"].append({ # gather all migrant attributes
                                    "attribute": attribute["attribute"],
                                    "optionality": "!",
                                    "datatype": attribute["datatype"],
                                    "adjacent_source": leg.entity.name_view,
                                    "outer_source": outer_source,
                                    "association_name": association.name_view,
                                    "leg_note": leg.note,
                                    "is_primary": leg.is_in_elected_group,
                                    "nature": "primary_foreign_key" if leg.is_in_elected_group else "stopped_foreign_key",
                                    "unicities": leg.unicities,
                                })
                                self.relations[association.bid]["existing_unicity_numbers"].update(map(int, leg.unicities))
                            elif association.is_protected and df_leg is not None and leg is not df_leg:
                                self.relations[association.bid]["columns"].append({ # gather all migrant attributes
                                    "attribute": attribute["attribute"],
                                    "optionality": "!",
                                    "datatype": attribute["datatype"],
                                    "adjacent_source": leg.entity.name_view,
                                    "outer_source": outer_source,
                                    "association_name": association.name_view,
                                    "leg_note": leg.note,
                                    "is_primary": False,
                                    "nature": "stopped_foreign_key",
                                    "unicities": "",
                                })
                            else:
                                self.relations[association.bid]["columns"].append({ # gather all migrant attributes
                                    "attribute": attribute["attribute"],
                                    "optionality": "!",
                                    "datatype": attribute["datatype"],
                                    "adjacent_source": leg.entity.name_view,
                                    "outer_source": outer_source,
                                    "association_name": association.name_view,
                                    "leg_note": leg.note,
                                    "is_primary": True,
                                    "nature": "unsourced_primary_foreign_key" if outer_source is None else "primary_foreign_key",
                                    "unicities": "",
                                })
                        elif attribute["nature"].startswith("deleted_parent_discriminator"):
                            self.relations[association.bid]["columns"].append({
                                "attribute": attribute["attribute"],
                                "optionality": "!",
                                "datatype": attribute["datatype"],
                                "adjacent_source": leg.entity.name_view,
                                "outer_source": None,
                                "association_name": association.name_view,
                                "leg_note": leg.note,
                                "is_primary": False,
                                "nature": attribute["nature"],
                                "unicities": "",
                            })
                self.relations[association.bid]["columns"].extend({ # and the attributes already existing in the association
                        "attribute": attribute.label,
                        "optionality": "!" if attribute.kind == "strong" else self.pop_optionality_from_datatype(attribute),
                        "datatype": attribute.datatype,
                        "adjacent_source": None,
                        "outer_source": None,
                        "association_name": association.name_view,
                        "leg_note": None,
                        "is_primary": attribute.kind == "strong",
                        "nature": "association_primary_key" if attribute.kind == "strong" else "association_attribute",
                        "unicities": "",
                    } for attribute in association.attributes if attribute.label.strip() != ""
                )
                continue

            # No relation will be created from this association.

            # Check the number of /?1 legs (pegs)
            df_pegs = []
            for leg in association.legs:
                if leg.entity.is_invisible:
                    continue
                if leg.card[1] == "1" and leg.kind == "cluster_peg":
                    df_pegs.append(leg)
            
            if df_pegs: # A cluster with at least one /?1 leg (peg)
                for df_peg in df_pegs:
                    # All migrating attribute must belong to the same new unicity group
                    unicities = str(first_missing_positive(self.relations[df_peg.entity_bid]["existing_unicity_numbers"]))
                    self.relations[df_leg.entity_bid]["existing_unicity_numbers"].update(map(int, unicities))
                    for leg in association.legs:
                        if leg is df_peg:
                            continue
                        for attribute in list(self.relations[leg.entity_bid]["columns"]): # traverse a copy...
                            # ... to prevent an infinite migration of the child discriminator
                            if attribute["is_primary"]:
                                # Their primary keys must migrate in `entity_name`.
                                outer_source = self.may_retrieve_distant_outer_source(leg, attribute)
                                self.relations[df_peg.entity_bid]["columns"].append({
                                    "attribute": attribute["attribute"],
                                    "optionality": "!",
                                    "datatype": attribute["datatype"],
                                    "adjacent_source": leg.entity.name_view,
                                    "outer_source": outer_source,
                                    "association_name": association.name_view,
                                    "leg_note": leg.note,
                                    "is_primary": False,
                                    "nature": "unsourced_foreign_key" if outer_source is None else "foreign_key",
                                    "unicities": unicities,
                                    # NB: technically, an unsourced foreign key is not foreign anymore
                                })
                # The association attributes must migrate only once, df_leg is elected.
                # Delay the addition of the association attributes after the else part.

            else:
                # A normal DF association. Traverse the other legs to find the attributes to migrate.
                for leg in association.legs:
                    if leg.entity.is_invisible:
                        continue
                    if leg is not df_leg:
                        if (df_leg.entity_bid, association.bid, leg.entity_bid) not in self.freeze_strengthening_foreign_key_migration:
                            unicities = ""
                            if leg.card[1] == "1": # *1 --(DF)-- 11 => the migrating attribute must be made unique, find a new unicity group
                                unicities = str(first_missing_positive(self.relations[df_leg.entity_bid]["existing_unicity_numbers"]))
                            for attribute in list(self.relations[leg.entity_bid]["columns"]): # traverse a copy...
                                # ... to prevent an infinite migration of the child discriminator
                                optionality = "!" if df_leg.card[0] == "1" else "?"
                                if attribute["is_primary"]:
                                    # Their primary keys must migrate in df_leg.entity_bid.
                                    outer_source = self.may_retrieve_distant_outer_source(leg, attribute)
                                    self.relations[df_leg.entity_bid]["columns"].append({
                                        "attribute": attribute["attribute"],
                                        "optionality": optionality,
                                        "datatype": attribute["datatype"],
                                        "adjacent_source": leg.entity.name_view,
                                        "outer_source": outer_source,
                                        "association_name": association.name_view,
                                        "leg_note": leg.note,
                                        "is_primary": False,
                                        "nature": "unsourced_foreign_key" if outer_source is None else "foreign_key",
                                        "unicities": unicities,
                                        # NB: technically, an unsourced foreign key is not foreign anymore
                                    })
                                    self.relations[df_leg.entity_bid]["existing_unicity_numbers"].update(map(int, unicities))
                                elif attribute["nature"].startswith("deleted_parent_discriminator"):
                                    self.relations[df_leg.entity_bid]["columns"].append({
                                        "attribute": attribute["attribute"],
                                        "optionality": optionality,
                                        "datatype": attribute["datatype"],
                                        "adjacent_source": leg.entity.name_view,
                                        "outer_source": None,
                                        "association_name": association.name_view,
                                        "leg_note": leg.note,
                                        "is_primary": False,
                                        "nature": attribute["nature"],
                                        "unicities": "",
                                    })
                
            # Add the attributes already existing in the association
            self.relations[df_leg.entity_bid]["columns"].extend([{
                    "attribute": attribute.label,
                    "optionality": "!" if attribute.kind == "strong" else self.pop_optionality_from_datatype(attribute),
                    "datatype": attribute.datatype,
                    "association_name": association.name_view,
                    "adjacent_source": None,
                    "outer_source": None,
                    "leg_note": None,
                    "is_primary": attribute.kind == "strong",
                    "nature": "outer_primary_key" if attribute.kind == "strong" else "outer_attribute",
                    "unicities": "",
                } for attribute in association.attributes if attribute.label.strip() != ""])


    def process_inheritances(self):
        for inheritance in self.mcd.inheritances:
            parent_leg = inheritance.legs[0]
            if inheritance.kind == "=>": # total migration: parent > children
                for child_leg in inheritance.legs[1:]: 
                    # migrate the parent's attributes, except those of nature "deleted_parent_discriminator"
                    self.relations[child_leg.entity_bid]["columns"][0:0] = [{
                        "attribute": attribute["attribute"],
                        "optionality": attribute["optionality"],
                        "datatype": attribute["datatype"],
                        "adjacent_source": parent_leg.entity.name_view,
                        "outer_source": self.may_retrieve_distant_outer_source(parent_leg, attribute),
                        "association_name": inheritance.name_view,
                        "leg_note": self.may_retrieve_distant_leg_note(parent_leg, attribute),
                        "is_primary": False,
                        "nature": "deleted_parent_foreign_key" if attribute["nature"] == "foreign_key" else "deleted_parent_attribute",
                        "unicities": "",
                    } for attribute in self.relations[parent_leg.entity_bid]["columns"] if not attribute["is_primary"] and not attribute["nature"].startswith("deleted_parent_discriminator")]
            else: # migration: triangle attributes > parent
                self.relations[parent_leg.entity_bid]["columns"].extend({ 
                    "attribute": attribute.label,
                    "optionality": "!" if 'T' in inheritance.name_view else "?",
                    "datatype": attribute.datatype or "UNSIGNED_INT_PLACEHOLDER",
                    "adjacent_source": None,
                    "outer_source": None,
                    "association_name": inheritance.name_view,
                    "leg_note": None,
                    "is_primary": False,
                    "nature": f"deleted_child_discriminator_{inheritance.name_view}", # "", "X", "T" or "XT"
                    "unicities": "",
                } for attribute in inheritance.attributes)
                if inheritance.kind in ("<-", "<="): # migration: children > parent, and suppress children
                    for child_leg in inheritance.legs[1:]:
                        if inheritance.kind == "<=":
                            # make the child's name a boolean attribute of the parent
                            self.relations[parent_leg.entity_bid]["columns"].append({
                                "attribute": _('is {name}').format(name=child_leg.entity_bid.lower()),
                                "optionality": "!",
                                "datatype": "BOOLEAN_PLACEHOLDER",
                                "adjacent_source": child_leg.entity.name_view,
                                "outer_source": child_leg.entity.name_view,
                                "association_name": inheritance.name_view,
                                "leg_note": None,
                                "is_primary": False,
                                "nature": "deleted_child_entity_name",
                                "unicities": "",
                            })
                        # migrate all child's attributes
                        for attribute in self.relations[child_leg.entity_bid]["columns"]:
                            if attribute["nature"].endswith("parent_primary_key"):
                                continue # except the "strengthening" parent identifier
                            self.relations[parent_leg.entity_bid]["columns"].append({
                                "attribute": attribute["attribute"],
                                "optionality": "?",
                                "datatype": attribute["datatype"],
                                "adjacent_source": child_leg.entity.name_view,
                                "outer_source": self.may_retrieve_distant_outer_source(child_leg, attribute),
                                "association_name": inheritance.name_view,
                                "leg_note": self.may_retrieve_distant_leg_note(child_leg, attribute),
                                "is_primary": False,
                                "nature": "deleted_child_foreign_key" if attribute["nature"] == "foreign_key" else "deleted_child_attribute",
                                "unicities": "",
                            })
    
    def delete_inheritance_parent_or_children_to_delete(self):
        for entity_to_delete in self.inheritance_parent_or_children_to_delete:
            del self.relations[entity_to_delete]

    def delete_deletable_relations(self):
        deleted_outer_sources = set()
        for (bid, relation) in list(self.relations.items()):
            if not relation.get("is_protected") and all(column["nature"] == "primary_key" for column in relation["columns"]):
                del self.relations[bid]
                deleted_outer_sources.add(relation["this_relation_name"])
        for relation in self.relations.values():
            for column in relation["columns"]:
                if column["outer_source"] in deleted_outer_sources:
                    column["nature"] = column["nature"].replace("foreign", "ex_foreign")
        self.deleted_relations = sorted(deleted_outer_sources)

    def make_primary_keys_first(self):
        for relation in self.relations.values():
            relation["columns"].sort(key=lambda column: not column["is_primary"])
