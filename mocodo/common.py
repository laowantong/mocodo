import json
import numbers
import sys
from pathlib import Path
import contextlib

from .mocodo_error import MocodoError


def safe_print_for_PHP(s):
    """ It seems that when called from PHP, Python is unable to guess correctly
        the encoding of the standard output. """
    try:
        print(s, file=sys.stdout)
    except UnicodeEncodeError:
        print(s.encode("utf8"), file=sys.stdout)


class Common:

    def __init__(self, params):
        self.params = params

    def output_success_message(self, path):
        return _('Output file "{filename}" successfully generated.').format(filename=path)

    def update_source(self, source):
        path = Path(f"{self.params['output_name']}.mcd")
        path.write_text(source, encoding="utf8")
        return _('Source file "{filename}" successfully updated.').format(filename=path)

    def load_input_file(self):
        path = Path(self.params["input"])
        for encoding in self.params["encodings"]:
            with contextlib.suppress(UnicodeError):
                self.encoding = encoding
                return path.read_text(encoding=encoding).replace('"', '')
        raise MocodoError(5, _('Unable to read "{filename}" with any of the following encodings: "{encodings}".').format(filename=self.params["input"], encodings= ", ".join(self.params["encodings"]))) # fmt: skip

    def update_input_file(self, source):
        if not source.startswith("%%mocodo"):
            source = f"%%mocodo\n{source}"
        Path(self.params["input"])(source, encoding=self.encoding)
        safe_print_for_PHP(self.output_success_message(self.params["input"]))

    def load_style(self):
        
        def load_by_name(name):
            path = Path(self.params[name]).with_suffix(".json")
            if path.is_file():
                try:
                    return json.loads(path.read_text(encoding="utf8"))
                except:
                    raise MocodoError(3, _('Problem with "{name}" file "{path}".').format(name=name, path=path)) # fmt: skip
            path = Path(self.params["script_directory"], "resources", name, path)
            try:
                return json.loads(path.read_text(encoding="utf8"))
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

    def dump_file(self, path, content):
        Path(path).write_text(content, encoding="utf8")
        safe_print_for_PHP(self.output_success_message(path))
