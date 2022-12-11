from bisect import bisect_left
import json
import numbers
import os
import sys
import time
from pathlib import Path

from .file_helpers import read_contents, write_contents
from .mocodo_error import MocodoError
from .version_number import version


def safe_print_for_PHP(s):
    """ It seems that when called from PHP, Python is unable to guess correctly
        the encoding of the standard output. """
    try:
        print(s, file=sys.stdout)
    except UnicodeEncodeError:
        print(s.encode("utf8"), file=sys.stdout)

def read_template(template_name, template_folder=None):

    def traverse_templates(template_name, template_stack):
        path = template_folder / f"{template_name}.json"
        template = json.loads(read_contents(path))
        template_stack.append(template)
        if "parent" in template:
            return traverse_templates(template["parent"], template_stack)
        else:
            return reversed(template_stack)
    
    result = {}
    for template in traverse_templates(template_name, []):
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
        

class Common:

    def __init__(self, params):
        self.params = params

    def output_success_message(self, path):
        return _('Output file "{filename}" successfully generated.').format(filename=path)

    def timestamp(self):
        return _("Generated by Mocodo {version} on {date}").format(version=version, date=time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime()))

    def load_input_file(self):
        for encoding in self.params["encodings"]:
            try:
                self.encoding = encoding
                return read_contents(self.params["input"], encoding=encoding).replace('"', '').splitlines()
            except UnicodeError:
                pass
        raise MocodoError(5, _('Unable to read "{filename}" with any of the following encodings: "{encodings}".').format(filename=self.params["input"], encodings= ", ".join(self.params["encodings"]))) # fmt: skip

    def load_style(self):
        
        def load_by_name(name):
            path = self.params[name] + ("" if self.params[name].endswith(".json") else ".json") 
            if os.path.exists(path):
                try:
                    return json.loads(read_contents(path))
                except:
                    raise MocodoError(3, _('Problem with "{name}" file "{path}".').format(name=name, path=path)) # fmt: skip
            path = os.path.join(self.params["script_directory"], "resources", name, path)
            try:
                return json.loads(read_contents(path))
            except:
                raise MocodoError(3, _('Problem with "{name}" file "{path}".').format(name=name, path=path)) # fmt: skip
        
        def may_apply_scaling(shapes):
            if self.params["scale"] == 1:
                return
            scale = self.params["scale"]
            for key in shapes:
                if key.endswith("font"):
                    shapes[key]["size"] = shapes[key]["size"] * scale
                elif not key.endswith("ratio") and isinstance(shapes[key], numbers.Number):
                    shapes[key] *= scale
        
        def ensure_margins_are_integer(shapes):
            # Some nasty failures are known to occur otherwise.
            for key in shapes:
                if "margin" in key:
                    shapes[key] = int(shapes[key] + 0.5)
            
        style = {}
        style.update(load_by_name("colors"))
        shapes = load_by_name("shapes")
        may_apply_scaling(shapes)
        ensure_margins_are_integer(shapes)
        style.update(shapes)
        style["transparent_color"] = None
        return style

    def dump_mld_files(self, relations):
        relation_templates = []
        for template_name in self.params["relations"]:
            try:
                template_folder = Path(self.params["script_directory"]) / "resources" / "templates"
                contents = read_template(template_name, template_folder)
                relation_templates.append(contents)
            except:
                safe_print_for_PHP(_('Problem with template {template}.').format(template=template_name + ".json"))
        for template_name in relation_templates:
            path = os.path.join(self.params["output_name"] + template_name["extension"])
            try:
                text = relations.get_text(template_name)
                safe_print_for_PHP(self.output_success_message(path))
            except:
                text = _("Problem during the generation of the relational schema.")
                safe_print_for_PHP(text)
                raise
            write_contents(path, text)

    def calculate_or_retrieve_geo(self, mcd, reuse_geo=False):
        geo_path = Path(f"{self.params['output_name']}_geo.json")
        mcd_path = Path(f"{self.params['input']}")
        if geo_path.is_file() and (reuse_geo or mcd_path.stat().st_mtime < geo_path.stat().st_mtime):
            try:
                web_geo = json.loads(geo_path.read_text("utf8"))
                geo = {k: dict(v) if isinstance(v, list) else v for (k, v) in web_geo.items()}
                return geo
            except: # in case a problem occurs with the geo file, fallback to silently regenerate it
                pass
        geo = {
            "width": mcd.w,
            "height": mcd.h,
            "cx": {
                box.name: box.x + box.w // 2
                for row in mcd.rows
                for box in row
                if box.kind != "phantom"
            },
            "cy": {
                box.name: box.y + box.h // 2
                for row in mcd.rows
                for box in row
                if box.kind != "phantom"
            },
            "shift": {leg.identifier: 0 for row in mcd.rows for box in row for leg in box.legs},
            "ratio": {
                leg.identifier: 1.0
                for row in mcd.rows
                for box in row
                for leg in box.legs
                if leg.arrow
            },
        }
        path = f"{self.params['output_name']}_geo.json"
        web_geo = {k: list(v.items()) if isinstance(v, dict) else v for (k, v) in geo.items()}
        text = json.dumps(web_geo, indent=2, ensure_ascii=False)
        text = text.replace("\n      ", " ")
        text = text.replace("\n    ]", " ]")
        try:
            write_contents(path, text)
            safe_print_for_PHP(self.output_success_message(path))
        except IOError:
            safe_print_for_PHP(_('Unable to generate file "{filename}"!').format(filename=os.path.basename(path)))
        return geo
