import sys

if sys.version_info < (3, 6):
    print(f"Mocodo requires Python 3.6 or later to run.\nThis version is {sys.version}.")
    sys.exit()

import contextlib
import importlib
import json
from pathlib import Path

from .argument_parser import parsed_arguments
from .common import Common, Printer
from .convert.read_template import read_template
from .convert.relations import Relations
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
    "rw": ["rw", "source", "text", "code", "mocodo"],
    "cv": ["cv", "mld", "ddl", "sql"],
})

class ResponseLogger:

    def __init__(self, params):
        if not params["is_magic"]:
            self.may_log = self.log_nothing
            return
        self.response = {
            "mld": params["mld"],
            "args_to_delete": params["args_to_delete"],
            "opt_to_restore": params["opt_to_restore"],
            "redirect_output": params["redirect_output"],
            "select": params["select"],
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
        self.path.write_text(json.dumps(self.response, ensure_ascii=False), encoding="utf8")


def flip(source, subargs):
    for subsubopt in "".join(subargs.keys()):
        mcd = Mcd(source)
        if subsubopt == "v":
            source = mcd.get_vertically_flipped_clauses()
        elif subsubopt == "h":
            source = mcd.get_horizontally_flipped_clauses()
        elif subsubopt == "d":
            source = mcd.get_diagonally_flipped_clauses()
        else:
            subopt_error("flip", subsubopt)
    return source


class Runner:

    def __init__(self, args, printer):
        self.printer = printer
        try:
            self.params = parsed_arguments(args)
            self.parsing_error = None
            self.common = Common(self.params)
            self.get_font_metrics = font_metrics_factory(self.params)
        except MocodoError as e:
            # Raising a parsing error must be delayed, otherwise it will not be displayed as a MocodoError
            self.parsing_error = e
    
    def __call__(self):
        if self.parsing_error:
            raise self.parsing_error
        
        source = self.common.load_input_file()

        if self.params["restore"]:
            shutil = importlib.import_module("shutil")
            path = Path(self.params["script_directory"], "resources", "pristine_sandbox.mcd")
            shutil.copyfile(path, "sandbox.mcd")
            Path("params.json").write_text("{}\n", encoding="utf8")
            return
        
        if self.params["print_params"]:
            for added_key in self.params["keys_to_hide"][:]:
                self.params.pop(added_key, None)
            with contextlib.suppress(ValueError): # raised when called as a function (from mocodo import mocodo)
                self.params["output_dir"] = str(Path(self.params["output_dir"]).resolve().relative_to(Path.cwd()))
            text = json.dumps(self.params, ensure_ascii=False, indent=2, sort_keys=True)
            text = text.replace("\n    ", " ")
            text = text.replace("\n  ]", " ]")
            self.printer.write(text.strip())
            return "\n".join(self.printer.accumulator)

        self.add_gutter_params(self.params)

        if self.params["mld"] or ("transform" in self.params and self.params["transform"] == []):
            # In case there is an option `--mld` or an option `--transform` without arguments,
            # inject manually the equivalent --convert sub-option
            self.params["mld"] = True
            self.params["convert"].insert(0, ("markdown", {}))

        if "select" in self.params: # the user wants to override the default display policy under Jupyter
            if "all" in self.params["select"]:
                self.params["select"] = ["mcd", "rw", "cv"] if self.params["rewrite"] else ["mcd", "cv"]
            normalized_user_choices = []
            for k in self.params["select"]:
                if k.lower() not in SHOW_ARGS:
                    raise MocodoError(28, _('Unknown argument "{k}" for option --select.').format(k=k)) # fmt: skip
                normalized_user_choices.append(SHOW_ARGS[k.lower()])
            self.params["select"] = normalized_user_choices
        else:
            if self.params["rewrite"] and self.params["convert"]:
                self.params["select"] = ["mcd", "cv"]
            elif self.params["rewrite"]:
                self.params["select"] = ["mcd", "rw"]
            elif self.params["convert"] and self.params["mld"]:
                self.params["select"] = ["mcd", "cv"]
            elif self.params["convert"]:
                self.params["select"] = ["cv"]
            else:
                self.params["select"] = ["mcd"]

        response = ResponseLogger(self.params)

        if self.params["rewrite"]:
            for (subopt, subargs) in self.params["rewrite"]:
                if subopt == "echo":
                    pass
                elif subopt == "flip":
                    source = flip(source, subargs)
                elif subopt == "create" and "entities" in subargs:
                    source = guess_entities.run(source, subargs["entities"])
                elif subopt == "delete" and "dfs" in subargs:
                    module = importlib.import_module(f".rewrite._delete_dfs", package="mocodo")
                    source = module.run(source, self.params)
                elif subopt in self.params["op_tk_rewritings"]: # ex.: create, delete, ascii, etc.
                    source = op_tk.run(source, op_name=subopt, subargs=subargs, params=self.params).rstrip()
                else: # An unspecified rewrite operation, dynamically loaded
                    try:
                        module = importlib.import_module(f".rewrite._{subopt}", package="mocodo")
                    except ModuleNotFoundError:
                        raise subopt_error("rewrite", subopt)
                    source = module.run(source, subopt=subopt, subargs=subargs, params=self.params).rstrip()
                response.may_log("rewritten_source", source)
            if not self.params["is_magic"]:
                self.printer.write(self.common.update_source(source))
        
        may_update_params_with_guessed_title(source, self.params)

        converted_file_paths = [] # list of files to be displayed in the notebook
        raw_relations = None
        sql_relations = None
        if self.params["convert"]:
            response.may_log("has_explicit_conversion", True)
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
                    if template_suffix and set("bce").issuperset(template_suffix):
                        stem = f"{subopt}-{''.join(sorted(template_suffix))}"
                    else:
                        stem = subopt
                    template = read_template(stem, official_template_dir)
                
                # If the subopt was a relation template, use it to convert the source
                if template:
                    if template["extension"] == "sql":
                        if not sql_relations:
                            sql_source = source
                            sql_source = op_tk.run(sql_source, "ascii", {"labels": 1, "roles": 1}, self.params)
                            sql_mcd = Mcd(sql_source, self.get_font_metrics, **self.params)
                            sql_relations = Relations(sql_mcd, self.params)
                        text = sql_relations.get_text(template)
                    else:
                        if not raw_relations:
                            mcd = Mcd(source, self.get_font_metrics, **self.params)
                            raw_relations = Relations(mcd, self.params)
                        text = raw_relations.get_text(template)
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
                result["text_path"].write_text(f"{result['text'].rstrip()}\n", encoding="utf8")
                self.printer.write(self.common.output_success_message(result["text_path"]))
                results.append(result)
            for result in results:
                converted_file_paths.extend(self.get_converted_file_paths(result))
            response.may_log("converted_file_paths", converted_file_paths)

        if not raw_relations: # if the MCD has not be calculated during the conversions
            mcd = Mcd(source, self.get_font_metrics, **self.params)
        self.control_for_overlaps(mcd)
        resulting_paths = dump_mcd_to_svg(mcd, self.common)  # potential side-effect: update *_geo.json
        for path in resulting_paths:
            self.printer.write(self.common.output_success_message(path))

    def get_rendering_service(self, extension):
        path = Path(self.params["script_directory"], "resources", "rendering_services.json")
        try:
            rendering_services = json.loads(path.read_text(encoding="utf8"))
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

    def get_converted_file_paths(self, result):
        if result.get("to_defer") and "defer" in self.params:
            # This text must be rendered by a third-party service
            urllib = importlib.import_module("urllib")
            requests = importlib.import_module("requests")
            mimetypes = importlib.import_module("mimetypes")
            service = self.get_rendering_service(result["extension"])
            data = result["text"]
            for preprocessing in service.get("preprocessing", []):
                if preprocessing == "minify_graphviz":
                    # Spare some bandwidth
                    data = minify_graphviz(data)
                elif preprocessing == "urlsafe_encoding":
                    data = urlsafe_encoding(data)
                elif preprocessing == "encode_prefix":
                    # Sole use case (so far): "https://mocodo.net/?mcd="" becomes "https%3A//mocodo.net/%3Fmcd%3D"
                    index = data.find("=") + 1
                    data = urllib.parse.quote(data[:index]) + data[index:]
            url = service["url"].format(data=data)
            response = requests.get(url)
            if not response.ok:
                raise MocodoError(23, _("The HTTP status code {code} was returned by:\n{url}").format(code=response.status_code, url=url)) # fmt: skip
            content_type = response.headers['content-type']
            extension = mimetypes.guess_extension(content_type)
            resp_path = result["text_path"].with_suffix(extension)
            if content_type.startswith("text/"):
                resp_path.write_text(response.text, encoding="utf8")
            else:
                resp_path.write_bytes(response.content)
            yield str(resp_path)
        elif result.get("stem_suffix") == "_mld" and result.get("extension") == "mcd" and self.params["is_magic"]: # relational diagram
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
                        acc.append(_('  - Leg "{b1} — {b2}" overlaps "{b3}".').format(b1=b1, b2=b2, b3=b3))  # fmt: skip
                    else:
                        acc.append(_('  - Legs "{b1} — {b2}" and "{b3} — {b4}" overlap.').format(b1=b1, b2=b2, b3=b3, b4=b4))  # fmt: skip
                details = "\n".join(sorted(acc))
                raise MocodoError(29, _('Bad layout of boxes:\n{details}\nTo fix the problem, reorder and/or skip lines in the source text, either manually, or with the option -t arrange (chocolate bar under Mocodo online).').format(details=details))  # fmt: skip

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
        s = gutters["ids"].get("alts", "123456789")
        params["id_gutter_alts"] = dict(zip("123456789", s + "123456789"[len(s):]))

        # Create the sub-option "types" if needed, and initialize type_gutter params
        # NB: the gutter for types is not implemented yet, but all needed params are already there
        if "types" not in gutters:
            gutters["types"] = {}
        params["type_gutter_visibility"] = gutters["types"].get("visibility", "auto")

        # We are sure that gutters is a dict with keys "ids" and "types" only. Order matters.
        (params["left_gutter"], params["right_gutter"]) = tuple(gutters.keys())


def main():
    printer = Printer(quiet=True)
    run = Runner(sys.argv[1:], printer)
    try:
        run()
    except MocodoError as err:
        print(str(err), file=sys.stderr)
        sys.exit(err.errno)


if __name__ == "__main__": # to be run with `python -m mocodo`
    main()
