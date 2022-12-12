from bisect import bisect_left
import json

from .mocodo_error import MocodoError

def read_template(name, template_folder=None):

    def traverse_templates(name, template_stack, already_seen):
        if name in already_seen:
            raise MocodoError(30, _('Circular inheritance in template "{name}.json" of "{folder}.').format(name=name, folder=template_folder))  # fmt: skip
        already_seen.add(name)
        path = template_folder / f"{name}.json"
        if not path.is_file():
            raise MocodoError(31, _('Template "{name}.json" not found in "{folder}".').format(name=name, folder=template_folder))  # fmt: skip
        try:
            template = json.loads(path.read_text())
        except json.JSONDecodeError:
            raise MocodoError(32, _('Unable to decode template "{name}.json" of "{folder}".').format(name=name, folder=template_folder))  # fmt: skip
        if not isinstance(template, dict):
            raise MocodoError(33, _('Template "{name}.json" of "{folder}" is not a JSON object.').format(name=name, folder=template_folder))  # fmt: skip
        for (key, array) in template.items():
            if isinstance(array, dict):
                raise MocodoError(34, _('Template "{name}.json" of "{folder}" contains a JSON object as value of key "{key}".').format(name=name, folder=template_folder, key=key))  # fmt: skip
            if not isinstance(array, list):
                continue
            for d in array:
                if not isinstance(d, dict):
                    raise MocodoError(35, _('Template "{name}.json" of "{folder}" contains a JSON array as value of key "{key}" which does not contain only JSON objects.').format(name=name, folder=template_folder, key=key))  # fmt: skip
                if "order" not in d:
                    raise MocodoError(36, _('Template "{name}.json" of "{folder}" contains a JSON array as value of key "{key}" which does not contain only objects having an "order" key.').format(name=name, folder=template_folder, key=key))  # fmt: skip
        template_stack.append(template)
        if "parent" in template:
            return traverse_templates(template["parent"], template_stack, already_seen)
        else:
            return reversed(template_stack)
    
    result = {}
    for template in traverse_templates(name, [], set()):
        for key in template:
            if not isinstance(result.get(key), list):
                # create or update a scalar value
                result[key] = template[key]
            else:
                # update a list of dictionaries having an "order" key
                for new_dictionary in template[key]:
                    order = new_dictionary["order"]
                    orders = [d["order"] for d in result[key]] # Prior to Python 3.10, bisect_left has no `key` argument
                    i = bisect_left(orders, order)
                    if i < len(result[key]) and result[key][i]["order"] == order:
                        # a dictionary with the same order already exists
                        if len(new_dictionary) == 1:
                            # the new dictionary is reduced to an "order" key: remove the existing dictionary
                            del result[key][i]
                        else:
                            # update the existing dictionary in place
                            result[key][i].update(new_dictionary)
                    else:
                        # insert the new dictionary at the right place
                        result[key].insert(i, new_dictionary)
    return result
