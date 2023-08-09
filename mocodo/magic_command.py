import argparse
import re
import warnings
from pathlib import Path
from subprocess import PIPE, Popen

import pkg_resources
from IPython import get_ipython
from IPython.core.magic import Magics, line_cell_magic, magics_class
from IPython.display import HTML, SVG, display

try:
    MOCODO_VERSION = pkg_resources.get_distribution("mocodo").version
except pkg_resources.DistributionNotFound:
    MOCODO_VERSION = "(unknown version)"  # For tests during CI

IPYTHON = get_ipython()

def update_cell(content):
    IPYTHON.set_next_input(content, replace=True)

def split_by_unquoted_spaces_or_equals(
        string,
        findall=re.compile(r'(?:[^=\s\'"]+|"[^"]*"|\'[^\']*\')').findall,
    ):
    result = []
    for s in findall(string):
        if s.startswith('"') and s.endswith('"'):
            s = s[1:-1]
        elif s.startswith("'") and s.endswith("'"):
            s = s[1:-1]
        result.append(s)
    return result

@magics_class
class MocodoMagics(Magics):
    @staticmethod
    @line_cell_magic
    def mocodo(line, cell=""):
        """
        Mocodo IPython magic extension

        Magic methods:
            %mocodo [command line options]
            %%mocodo [command line options]
            < MCD ... >

        Usage:
            %load_ext mocodo
        """

        def display_diagrams():
            svg_path = Path(output_name).with_suffix(".svg")
            svg_was_updated = svg_path.is_file() and input_path.stat().st_mtime <= svg_path.stat().st_mtime
            if svg_was_updated:
                if not notebook_options.no_mcd:
                    display(SVG(filename=svg_path))
                if notebook_options.mld:
                    mld = Path(output_name).with_suffix(".html").read_text("utf8")
                    display(HTML(mld))
            return svg_was_updated

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--no_mcd", action="store_true")
        parser.add_argument("--mld", action="store_true")
        parser.add_argument("--input")
        parser.add_argument("--output_dir")
        chunks = split_by_unquoted_spaces_or_equals(line)
        (notebook_options, options) = parser.parse_known_args(chunks)

        Path("mocodo_notebook").mkdir(parents=True, exist_ok=True)

        if not notebook_options.input:
            input_path = Path("mocodo_notebook/sandbox.mcd")
            input_path.write_text(cell, encoding="utf8")
        else:
            input_path = Path(notebook_options.input)
            if not input_path.suffix:
                input_path = input_path.with_suffix(".mcd")

        if not notebook_options.output_dir:
            output_dir = Path("mocodo_notebook")
        else:
            output_dir = Path(notebook_options.output_dir)
            try:
                output_dir.mkdir(parents=True, exist_ok=True)
            except OSError:
                if not output_dir.is_dir():
                    raise
        output_name = output_dir / input_path.stem

        options.extend(["--input", str(input_path), "--output_dir", str(output_dir)]) # may override user's provided options
        try: # prevent explicit option --relations to override HTML generation
            options.insert(options.index("--relations") + 1, "html")
        except ValueError:
            options.extend(["--relations", "html"])

        process = Popen(["mocodo"] + options, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdoutdata, stderrdata = process.communicate()
        try:
            stdoutdata = stdoutdata.decode("utf8")
            stderrdata = stderrdata.decode("utf8")
        except:
            pass
        status = process.wait()
        if status != 0 or stderrdata:
            warnings.formatwarning = lambda x, *args, **kargs : str(x)
            warnings.warn(stderrdata)
            return
        
        if "--rewrite" in options:
            updated_source = input_path.read_text().rstrip()
            if "--replace" in options:
                update_cell(updated_source)
                return # abort, since this erases the [Out] section after returning asynchronously
            svg_was_updated = display_diagrams()
            if "--no_source" not in options:
                print(updated_source)
        else:
            svg_was_updated = display_diagrams()
        
        if svg_was_updated:
            return
        
        if "--help" in options:
            print(stdoutdata)
        elif "--print_params" in options:
            form = [
                f'# You may edit and run the following lines',
                f'import json, pathlib',
                f'params = """',
                f'{stdoutdata}',
                f'"""',
                f'try:',
                f'    json.loads(params)',
                f'except:',
                f'    raise RuntimeError("Invalid JSON. Check your syntax on https://jsonlint.com.")',
                f'pathlib.Path("{output_dir}/params.json").write_text(params.strip(), encoding="utf8")',
            ]
            update_cell("\n".join(form))

try:
    IPYTHON.register_magics(MocodoMagics)
except AttributeError:
    pass # necessary for launching the tests
else:
    print(f"Mocodo {MOCODO_VERSION} loaded.")

