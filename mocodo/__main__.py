from pathlib import Path
import sys

if sys.version_info < (3, 6):
    print(f"Mocodo requires Python 3.6 or later to run.\nThis version is {sys.version}.")
    sys.exit()

import importlib
import json
import contextlib
import requests
import shutil

from .argument_parser import parsed_arguments, transformations
from .common import Common, safe_print_for_PHP
from .convert.read_template import read_template
from .convert.relations import Relations
from .file_helpers import write_contents
from .font_metrics import font_metrics_factory
from .guess_title import may_update_params_with_guessed_title
from .mcd import Mcd
from .mcd_to_svg import main as dump_mcd_to_svg
from .mocodo_error import MocodoError, subopt_error
from .rewrite import op_tk, guess_entities
from .tools.graphviz_tools import minify_graphviz
from .tools.string_tools import urlsafe_encoding
from .tools.various import invert_dict


SHOW_ARGS = invert_dict({
    "mcd": ["mcd"],
    "rw": ["rw", "source", "text", "code"],
    "cv": ["cv", "mld", "ddl"],
})

class ResponseLogger:

    def __init__(self, params):
        if not params["is_magic"]:
            self.may_log = self.log_nothing
            return
        self.response = {
            "mld": params["mld"],
            "redirect_output": params["redirect_output"],
            "show": params["show"],
        }
        self.may_log = self.log_for_magic
        self.path = Path(f"{params['output_name']}_response_for_magic_command.json")
        self.dump()
    
    def log_nothing(self, *args, **kwargs):
        pass

    def log_for_magic(self, key, value):
        self.response[key] = value
        self.dump()
    
    def dump(self):
        self.path.write_text(json.dumps(self.response, ensure_ascii=False))


class Runner:

    def __init__(self):
        self.params = parsed_arguments()
        self.common = Common(self.params)
        self.get_font_metrics = font_metrics_factory(self.params)
    
    def __call__(self):
        source = self.common.load_input_file()

        if self.params["restore"]:
            path = Path(self.params["script_directory"], "resources", "pristine_sandbox.mcd")
            shutil.copyfile(path, "sandbox.mcd")
            return write_contents("self.params.json", "{}")
        
        if self.params["print_params"]:
            for added_key in self.params["keys_to_hide"][:]:
                del self.params[added_key]
            self.params["print_params"] = False
            self.params_contents = json.dumps(self.params, ensure_ascii=False, indent=2, sort_keys=True)
            return safe_print_for_PHP(self.params_contents)

        self.add_gutter_params(self.params)

        if self.params["mld"] or ("transform" in self.params and self.params["transform"] == []):
            # In case there is an option `--mld` or an option `--transform` without arguments,
            # inject manually the equivalent --convert sub-option
            self.params["mld"] = True
            self.params["convert"].insert(0, ("markdown", {}))

        if self.params.get("show"): # the user wants to override the default display policy under Jupyter
            normalized_user_choices = []
            for k in self.params["show"]:
                if k.lower() not in SHOW_ARGS:
                    raise MocodoError(28, _('Unknown argument "{k}" for option --show.').format(k=k)) # fmt: skip
                normalized_user_choices.append(SHOW_ARGS[k.lower()])
            self.params["show"] = normalized_user_choices
        
        if "show" in self.params:
            if self.params["show"] == []: # display all outputs: MCD, rewritten source, converted files
                self.params["show"] = ["mcd", "rw", "cv"]
            # else: don't touch to the user's choices
        elif self.params["rewrite"] and self.params["convert"]:
            self.params["show"] = ["mcd", "cv"]
        elif self.params["rewrite"]:
            self.params["show"] = ["mcd", "rw"]
        elif self.params["convert"] and self.params["mld"]:
            self.params["show"] = ["mcd", "cv"]
        elif self.params["convert"]:
            self.params["show"] = ["cv"]
        else:
            self.params["show"] = ["mcd"]

        response = ResponseLogger(self.params)

        if self.params["rewrite"]:
            for (subopt, subargs) in self.params["rewrite"]:
                if subopt == "echo":
                    pass
                elif subopt == "flip":
                    source = self.flip(source, subargs)
                elif subopt == "create" and "entities" in subargs:
                    source = guess_entities.run(source, subargs["entities"])
                elif subopt in transformations.op_tk_rewritings: # ex.: create, delete, ascii, etc.
                    source = op_tk.run(source, op_name=subopt, subargs=subargs, params=self.params).rstrip()
                else: # An unspecified rewrite operation, dynamically loaded
                    try:
                        module = importlib.import_module(f".rewrite._{subopt}", package="mocodo")
                    except ModuleNotFoundError:
                        raise subopt_error("rewrite", subopt)
                    source = module.run(source, subopt=subopt, subargs=subargs, params=self.params).rstrip()
                response.may_log("rewritten_source", source)
            # The geometry needs to be recomputed after the rewrite operations
            with contextlib.suppress(FileNotFoundError): # Argument missing_ok=True is not available prior to Python 3.8
                Path(f"{self.params['output_name']}_geo.json").unlink()
        
        may_update_params_with_guessed_title(source, self.params)

        deferred_output_formats = []
        if "defer" in self.params:
            deferred_output_formats = self.params["defer"] or ["svg"]

        converted_file_paths = [] # list of files to be displayed in the notebook
        if self.params["convert"]:
            response.may_log("has_explicit_conversion", True)
            relations = None
            results = []
            for (subopt, subargs) in self.params["convert"]:

                # Try to interpret subopt as the stem or path of a relation template
                template = None
                official_template_dir = Path(self.params["script_directory"], "resources", "relation_templates")
                if subopt == "relation":
                    stem_or_path = next(iter(subargs.keys()), "") # ignore all sub-arguments after the first one
                    template = read_template(stem_or_path, official_template_dir)
                elif Path(official_template_dir, f"{subopt}.yaml").is_file():
                    template_suffix = next(iter(subargs.keys()), "") # ignore all sub-arguments after the first one
                    if template_suffix and set("ces").issuperset(template_suffix):
                        stem = f"{subopt}-{''.join(sorted(template_suffix))}"
                    else:
                        stem = subopt
                    template = read_template(stem, official_template_dir)
                
                # If the subopt was a relation template, use it to convert the source
                if template:
                    if template["extension"] == "sql":
                        source = op_tk.run(source, "ascii", {"labels": 1}, self.params)
                        source = op_tk.run(source, "snake", {"labels": 1}, self.params)
                        source = op_tk.run(source, "lower", {"attrs": 1, "roles": 1}, self.params)
                        source = op_tk.run(source, "upper", {"boxes": 1}, self.params)
                        relations = None # force the re-computation of the relations after the rewrite operations
                    if not relations: # don't recompute the relations if they have already been computed
                        mcd = Mcd(source, self.get_font_metrics, **self.params)
                        relations = Relations(mcd, self.params)
                    text = relations.get_text(template)
                    result = {
                        "stem_suffix": template["stem_suffix"],
                        "text": text,
                        "extension": template["extension"],
                        "to_defer": template.get("to_defer", False),
                        "highlight": template.get("highlight", "plain"),
                    }

                # Fall back to a dynamically loaded conversion operation
                else:
                    try:
                        module = importlib.import_module(f".convert._{subopt}", package="mocodo")
                    except ModuleNotFoundError:
                        raise subopt_error("convert", subopt)
                    result = module.run(source, subargs, self.common)
                
                result["text_path"] = Path(f"{self.params['output_name']}{result['stem_suffix']}.{result['extension']}")
                self.common.dump_file(result["text_path"], f"{result['text'].rstrip()}\n")
                results.append(result)
            for result in results:
                converted_file_paths.extend(self.generate_converted_files(result, deferred_output_formats))
            response.may_log("converted_file_paths", converted_file_paths)

        mcd = Mcd(source, self.get_font_metrics, **self.params)
        self.control_for_overlaps(mcd)
        resulting_paths = dump_mcd_to_svg(mcd, self.common)  # potential side-effect: update *_geo.json
        for path in resulting_paths:
            safe_print_for_PHP(self.common.output_success_message(path))

    def flip(self, source, subargs):
        mcd = Mcd(source, self.get_font_metrics, **self.params)
        for subsubopt in subargs:
            if subsubopt in ("v", "vertical"):
                source = mcd.get_vertically_flipped_clauses()
            elif subsubopt in ("h", "horizontal"):
                source = mcd.get_horizontally_flipped_clauses()
            elif subsubopt in ("d", "diagonal"):
                source = mcd.get_diagonally_flipped_clauses()
            else:
                raise MocodoError(22, _("Unknown argument {subsubopt} for operation {subopt}".format(subsubopt=subsubopt, subopt=subopt)))  # fmt: skip
        return source


    def get_rendering_service(self, extension):
        path = Path(self.params["script_directory"], "resources", "rendering_services.json")
        try:
            rendering_services = json.loads(path.read_text())
        except FileNotFoundError:
            raise MocodoError(46, _('The file "{path}" is missing.').format(path=path))  # fmt: skip
        except json.decoder.JSONDecodeError:
            raise MocodoError(47, _('The file "{path}" is not a valid JSON file.').format(path=path))  # fmt: skip
        except Exception as err:
            raise MocodoError(48, _('The file "{path}" could not be read:\n{err}').format(path=path, err=err))  # fmt: skip
        try:
            return rendering_services[extension]
        except KeyError:
            raise MocodoError(49, _('No third-party rendering service for extension "{extension}". You may want to add one in "{path}".').format(extension=extension, path=path))

    def generate_converted_files(self, result, deferred_output_formats):
        if result.get("to_defer") and deferred_output_formats:
            # This text must be rendered by a third-party service in at least one format
            rendering_service = self.get_rendering_service(result["extension"])
            if result["extension"] == "gv":
                payload = minify_graphviz(result["text"]) # spare some bandwidth
            payload = urlsafe_encoding(result["text"])
            for output_format in deferred_output_formats: # ex.: svg, png, etc.
                if output_format == "raw":
                    resp_path = str(result["text_path"])
                else:
                    url = rendering_service.format(output_format=output_format, payload=payload)
                    response = requests.get(url)
                    if not response.ok:
                        raise MocodoError(23, _("The HTTP status code {code} was returned by:\n{url}").format(code=response.status_code, url=url)) # fmt: skip
                    resp_path = result["text_path"].with_suffix(f".{output_format}")
                    if response.headers["content-type"].startswith("text/"):
                        resp_path.write_text(response.text)
                    else:
                        resp_path.write_bytes(response.content)
                yield str(resp_path)
        elif result.get("stem_suffix") == "_mld" and result.get("extension") == "mcd": # relational diagram
            mld = Mcd(result["text"], self.get_font_metrics, **self.params)
            backup_input = self.params["input"]
            backup_output_name = self.params["output_name"]
            self.params["input"] = result["text_path"]
            self.params["output_name"] = f"{self.params['output_name']}_mld"
            dump_mcd_to_svg(mld, self.common)
            self.params["input"] = backup_input
            self.params["output_name"] = backup_output_name
            yield str(result['text_path'].with_suffix(".svg"))
        else:
            # This text doesn't need further processing
            yield str(result["text_path"])

    def control_for_overlaps(self, mcd):
        if self.params["detect_overlaps"]:
            overlaps = mcd.get_overlaps()
            if overlaps:
                acc = []
                for (b1, b2, b3, b4) in overlaps:
                    if b3 == b4:
                        acc.append(_("- Leg “{b1} — {b2}” overlaps “{b3}”.").format(b1=b1, b2=b2, b3=b3))  # fmt: skip
                    else:
                        acc.append(_("- Legs “{b1} — {b2}” and “{b3} — {b4}” overlap.").format(b1=b1, b2=b2, b3=b3, b4=b4))  # fmt: skip
                details = "\n".join(acc)
                raise MocodoError(29, _('On Mocodo online, click the 🔀 button to fix the following problem(s):\n{details}').format(details=details))  # fmt: skip

    def add_gutter_params(self, params):
        gutters = dict(params.get("gutters", []))

        # Ensure that the --gutter sub-options are a subset of {"ids", "types"}
        for subopt in gutters:
            if subopt not in ("ids", "types"):
                raise subopt_error("gutters", subopt)
        
        # Create the sub-option "ids" if needed, and initialize id_gutter params
        if "ids" not in gutters:
            gutters["ids"] = {} # created at the end of the (ordered) dict
        params["id_gutter_visibility"] = gutters["ids"].get("visibility", "auto")
        params["id_gutter_weak_string"] = gutters["ids"].get("weak", "id")
        params["id_gutter_strong_string"] = gutters["ids"].get("strong", "ID")
        s = gutters["ids"].get("unicities", "123456789")
        params["id_gutter_unicities"] = dict(zip("123456789", s + "123456789"[len(s):]))

        # Create the sub-option "types" if needed, and initialize type_gutter params
        # NB: the gutter for types is not implemented yet, but all needed params are already there
        if "types" not in gutters:
            gutters["types"] = {}
        params["type_gutter_visibility"] = gutters["types"].get("visibility", "auto")

        # We are sure that gutters is a dict with keys "ids" and "types" only. Order matters.
        (params["left_gutter"], params["right_gutter"]) = tuple(gutters.keys())

def main():
    run = Runner()
    try:
        run()
    except MocodoError as err:
        print(str(err), file=sys.stderr)
        sys.exit(err.errno)


if __name__ == "__main__": # to be run with `python -m mocodo`
    main()
