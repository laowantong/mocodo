import argparse
import contextlib
import importlib
import json
import os
import re
import shlex
import warnings
from base64 import b64encode
from itertools import takewhile
from pathlib import Path
from subprocess import PIPE, Popen

import pkg_resources
from IPython import get_ipython
from IPython.core.magic import Magics, line_cell_magic, magics_class
from IPython.display import HTML, SVG, Code, Image, Markdown, display

try:
    MOCODO_VERSION = pkg_resources.get_distribution("mocodo").version
except pkg_resources.DistributionNotFound:
    MOCODO_VERSION = "(unknown version)"  # For tests during CI

# ANSI color codes
OK = "\033[92m"
WARNING = "\033[1m\033[38;5;166m"
FAIL = "\033[1m\033[91m"
RESET = "\033[0m"

IPYTHON = get_ipython()

def update_cell(content):
    IPYTHON.set_next_input(content, replace=True)

PARAM_TEMPLATE = '''\
# You may edit and run the following lines
import json, pathlib
params = """
{stdoutdata}
"""
try:
    json.loads(params)
except:
    raise RuntimeError("Invalid JSON. Check your syntax on https://jsonlint.com.")
pathlib.Path("{output_dir}/params.json").write_text(params.strip(), encoding="utf8")
'''

OUTPUT_PART_HEADER = re.sub("  +", "", """
<div style="position: relative; height: 3ex; background-color: transparent">
  <hr style="margin: 1ex 0 0 0; border-top: 1px solid #BBB">
  <span style="position: absolute; right: 0; color: #BBB">
    <tt>
        {label}
    </tt>
  </span>
</div>
""")

def display_converted_file(path, hide_header):
    if not (hide_header and path.name.endswith("_mld.md")):
        display(Markdown(OUTPUT_PART_HEADER.format(label=path.relative_to(Path.cwd()))))
    extension=path.suffix[1:]
    if extension == "svg":
        # Fix a maximum width for SVG images:
        # https://stackoverflow.com/questions/51452569/how-to-resize-rescale-a-svg-graphic-in-an-ipython-jupyter-notebook
        svg = b64encode(path.read_bytes()).decode("utf8")
        # Use Markdown instead of HTML to avoid a grey background.
        display(Markdown(f'<img max-width="100%" src="data:image/svg+xml;base64,{svg}">'))
    elif extension == "md":
        display(Markdown(filename=path))
    elif extension == "png":
        display(Image(filename=path, unconfined=False))
    elif extension == "html":
        text = path.read_text()
        text = re.sub('<!-- TO_BE_DELETED_BY_MOCODO_MAGIC -->.+\n', "", text)
        display(HTML(text))
    elif extension == "tex":
        display(Code(filename=path, language="latex"))
    elif extension == "tsv":
        try:
            df = importlib.import_module("pandas").read_csv(path, sep="\t", header=0, index_col=False)
            df = df.style.set_properties(**{'text-align': 'left'}).set_table_styles([ dict(selector='th', props=[('text-align', 'left')] ) ])
            display(df)
        except ImportError:
            display(Markdown(f"```\n{path.read_text()}\n```"))
    else:
        display(Markdown(f"```{extension}\n{path.read_text()}\n```"))

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
        parser.add_argument("--no_mcd", "--quiet", "--mute", action="store_true")
        parser.add_argument("--input", "-i")
        parser.add_argument("--output_dir")
        (args, remaining_args) = parser.parse_known_args(shlex.split(line))
        remaining_args = list(takewhile(lambda x: not x.startswith("#"), remaining_args))

        if Path.cwd().name != "mocodo_notebook":
            Path("mocodo_notebook").mkdir(parents=True, exist_ok=True)
            os.chdir("mocodo_notebook")

        if not args.input:
            input_path = Path.cwd() / "sandbox.mcd"
            input_path.write_text(cell, encoding="utf8")
        else:
            input_path = Path(args.input)
            if not input_path.suffix:
                input_path = input_path.with_suffix(".mcd")

        if not args.output_dir:
            output_dir = Path.cwd()
        else:
            output_dir = Path(args.output_dir)
            try:
                output_dir.mkdir(parents=True, exist_ok=True)
            except OSError:
                if not output_dir.is_dir():
                    raise
        output_path_radical = output_dir / input_path.stem

        remaining_args.extend([
            "--input", str(input_path),
            "--output_dir", str(output_dir),
            "--is_magic",
        ]) # may override user's provided options

        process = Popen(["mocodo"] + remaining_args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdoutdata, stderrdata = process.communicate()
        try:
            stdoutdata = stdoutdata.decode("utf8")
            stderrdata = stderrdata.decode("utf8")
        except:
            pass
        status = process.wait()

        if "--help" in remaining_args:
            print(stdoutdata)
            return
        
        if "--print_params" in remaining_args:
            update_cell(PARAM_TEMPLATE.format(stdoutdata=stdoutdata, output_dir=output_dir))
            return
        
        response_path = Path(f"{output_path_radical}_response_for_magic_command.json")
        try: 
            response = json.loads(response_path.read_text())
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            response = {}
        finally:
            with contextlib.suppress(FileNotFoundError): # From Python 3.8, use the missing_ok argument
                response_path.unlink()
        
        rewritten_source = response.get("rewritten_source", "")
        redirect_output = response.get("redirect_output", False)
        converted_file_paths = response.get("converted_file_paths", [])

        if status != 0 or stderrdata:
            message = stderrdata
            if rewritten_source:
                message = f"{rewritten_source}\n\n{message}"
            warnings.formatwarning = lambda x, *args, **kargs : str(x)
            warnings.warn(message)
            return
        
        if rewritten_source and not rewritten_source.startswith("%%mocodo"):
            rewritten_source = f"%%mocodo\n{rewritten_source}"
        
        for show in response.get("show", []):
            if show == "mcd":
                svg_path = output_path_radical.with_suffix(".svg")
                if svg_path.is_file() and input_path.stat().st_mtime <= svg_path.stat().st_mtime:
                    display(SVG(filename=svg_path))
            elif show == "rw":
                path = output_path_radical.with_suffix(".mcd")
                display(Markdown(OUTPUT_PART_HEADER.format(label=path.relative_to(output_dir))))
                if rewritten_source:
                    print(rewritten_source)
                else:
                    print(cell)
            elif show == "cv":
                for converted_file_path in converted_file_paths:
                    display_converted_file(Path(converted_file_path), hide_header=response.get("mld"))

        if redirect_output:
            if rewritten_source:
                update_cell(rewritten_source)
            if converted_file_paths:
                # Copy the last converted file source to the clipboard
                with contextlib.suppress(ImportError):
                    pyperclip = importlib.import_module("pyperclip")
                    converted_file_path = Path(converted_file_paths[-1])
                    pyperclip.copy(converted_file_path.read_text())
                    print(f'⧉ {OK}The contents of "{converted_file_path.relative_to(output_dir)}" has been copied to the clipboard.{RESET}')




try:
    IPYTHON.register_magics(MocodoMagics)
except AttributeError:
    pass # necessary for launching the tests
else:
    print(f"Mocodo {MOCODO_VERSION} loaded.")

