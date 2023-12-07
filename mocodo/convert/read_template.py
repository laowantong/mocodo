from bisect import bisect_left
from pathlib import Path

from ..tools import load_mini_yaml
from ..mocodo_error import MocodoError

def read_template(stem_or_path, official_template_dir):

    def traverse_templates(stem_or_path, template_stack, already_seen):
        if stem_or_path.endswith(".yaml"):
            path = Path(stem_or_path).absolute()
        else:
            path = official_template_dir / f"{stem_or_path}.yaml"
        (folder, name) = (path.parent, path.stem)
        if stem_or_path in already_seen:
            raise MocodoError(30, _('Circular inheritance in template "{name}.yaml" of "{folder}.').format(name=name, folder=folder))  # fmt: skip
        already_seen.add(stem_or_path)
        if not path.is_file():
            raise MocodoError(31, _('Template "{name}.yaml" not found in "{folder}".').format(name=name, folder=folder))  # fmt: skip
        try:
            template = load_mini_yaml.run(path)
        except:
            raise MocodoError(32, _('Unable to decode template "{name}.yaml" of "{folder}".').format(name=name, folder=folder))  # fmt: skip
        for (key, array) in template.items():
            if isinstance(array, dict):
                raise MocodoError(34, _('Template "{name}.yaml" of "{folder}" contains a YAML object as value of key "{key}".').format(name=name, folder=folder, key=key))  # fmt: skip
            if not isinstance(array, list):
                continue
            previous_order = None
            for d in array:
                if not isinstance(d, dict):
                    raise MocodoError(35, _('Template "{name}.yaml" of "{folder}" contains a YAML array as value of key "{key}" which does not contain only YAML objects.').format(name=name, folder=official_template_dir, key=key))  # fmt: skip
                if "order" not in d:
                    raise MocodoError(36, _('Template "{name}.yaml" of "{folder}" contains a YAML array as value of key "{key}" which does not contain only objects having an "order" key.').format(name=name, folder=official_template_dir, key=key))  # fmt: skip
                order = d["order"]
                if not isinstance(order, (int, float)):
                    raise MocodoError(38, _('Template "{name}.yaml" of "{folder}" contains a YAML array as value of key "{key}" where the "order" key is not associated to a number.').format(name=name, folder=official_template_dir, key=key))
                if previous_order is not None and order <= previous_order:
                    raise MocodoError(39, _('Template "{name}.yaml" of "{folder}" contains a YAML array as value of key "{key}" where the "order" keys are not sorted in ascending order.').format(name=name, folder=official_template_dir, key=key))
                previous_order = order
        template_stack.append(template)
        if "parent" in template:
            return traverse_templates(template["parent"], template_stack, already_seen)
        else:
            return reversed(template_stack)
    
    result = {}
    for template in traverse_templates(stem_or_path, [], set()):
        for key in template:
            if not isinstance(result.get(key), list):
                # create or update a scalar value
                result[key] = template[key]
            else:
                if template[key] == []:
                    result[key] = []                    
                # update a non-empty list of dictionaries having an "order" key
                for new_dictionary in template[key]:
                    order = new_dictionary["order"]
                    orders = [d["order"] for d in result[key]] # Prior to Python 3.10, bisect_left has no `key` argument
                    i = bisect_left(orders, order)
                    if i < len(result[key]) and result[key][i]["order"] == order:
                        # a dictionary with the same order already exists
                        if set(new_dictionary.keys()).issubset({"order", "comment"}):
                            # the new dictionary defines nothing: remove the existing dictionary
                            del result[key][i]
                        else:
                            # update the existing dictionary in place
                            result[key][i].update(new_dictionary)
                    else:
                        # insert the new dictionary at the right place
                        result[key].insert(i, new_dictionary)
    result.pop("parent", None)
    return result
