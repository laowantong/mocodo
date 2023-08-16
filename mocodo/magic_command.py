import argparse
import base64
import re
import warnings
from pathlib import Path
from subprocess import PIPE, Popen
import zlib

import pkg_resources
from IPython import get_ipython
from IPython.core.magic import Magics, line_cell_magic, magics_class
from IPython.display import HTML, Image, SVG, display

try:
    MOCODO_VERSION = pkg_resources.get_distribution("mocodo").version
except pkg_resources.DistributionNotFound:
    MOCODO_VERSION = "(unknown version)"  # For tests during CI

# TODO: parse arguments with argparse:
# Sometimes a script may only parse a few of the command-line arguments,
# passing the remaining arguments on to another script or program.
# In these cases, the parse_known_args() method can be useful.
# It works much like parse_args() except that it does not produce an error
# when extra arguments are present. Instead, it returns a two item tuple
# containing the populated namespace and the list of remaining argument strings.
# source: https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_known_args


IPYTHON = get_ipython()

def update_cell(content):
    IPYTHON.set_next_input(content, replace=True)

RENDERING_SERVICE = "https://kroki.io/{input_format}/{output_format}/{payload}"

INPUT_FORMATS = {
    "gv": "graphviz",
    "mmd": "mermaid"
}

def encode_text(text):
    return base64.urlsafe_b64encode(zlib.compress(text.encode('utf-8'), 9)).decode('ascii')

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
        
        if "--help" in options:
            print(stdoutdata)
            return
        
        if "--print_params" in options:
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
            return
        
        updated_source = None
        if any(x in options for x in ("--modify", "-m")):
            updated_source = input_path.read_text().rstrip()
            if "--replace" in options:
                update_cell(updated_source)
                return # abort, since this erases the [Out] section after returning asynchronously
        
        if "--suck" in options:
            keys = "|".join(INPUT_FORMATS)
            # Parse the output message to find the names of the generated files of interest
            for diagram_path in re.findall(fr"{output_name}.+?\.(?:{keys})\b", stdoutdata):
                diagram_path = Path(diagram_path)
                # Read the diagram file, encode and render it
                diagram = Path(diagram_path).read_text()
                suffix = diagram_path.suffix[1:]
                url = RENDERING_SERVICE.format(
                    input_format=INPUT_FORMATS.get(suffix, suffix),
                    output_format="svg", # TODO: support other formats as --suck argument
                    payload=encode_text(diagram),
                )
                display(Image(url=url, unconfined=False))
        
        if any(x in options for x in ("--dump", "-d")):
            print(stdoutdata, end="")
            return
        
        svg_path = Path(output_name).with_suffix(".svg")
        if svg_path.is_file() and input_path.stat().st_mtime <= svg_path.stat().st_mtime:
            if not notebook_options.no_mcd:
                display(SVG(filename=svg_path))
            if notebook_options.mld:
                mld = Path(output_name).with_suffix(".html").read_text("utf8")
                display(HTML(mld))

        if not(updated_source is None or "--no_text" in options):
            print(updated_source)


try:
    IPYTHON.register_magics(MocodoMagics)
except AttributeError:
    pass # necessary for launching the tests
else:
    print(f"Mocodo {MOCODO_VERSION} loaded.")

