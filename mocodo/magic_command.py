import argparse
import contextlib
import json
import os
import re
import shlex
import warnings
from pathlib import Path
from subprocess import PIPE, Popen
import importlib
from itertools import takewhile

import pkg_resources
from IPython import get_ipython
from IPython.core.magic import Magics, line_cell_magic, magics_class
from IPython.display import HTML, Image, SVG, display, Markdown, Code
from base64 import b64encode

try:
    MOCODO_VERSION = pkg_resources.get_distribution("mocodo").version
except pkg_resources.DistributionNotFound:
    MOCODO_VERSION = "(unknown version)"  # For tests during CI


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

def display_converted_file(path):
    extension=path.suffix[1:]
    display(Markdown(OUTPUT_PART_HEADER.format(label=path.relative_to(Path.cwd()))))
    if extension == "svg":
        # Fix a maximum width for SVG images:
        # https://stackoverflow.com/questions/51452569/how-to-resize-rescale-a-svg-graphic-in-an-ipython-jupyter-notebook
        svg = b64encode(path.read_bytes()).decode("utf8")
        display(HTML(f'<img max-width="100%" src="data:image/svg+xml;base64,{svg}">'))
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
        parser.add_argument("--input")
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
        if status != 0 or stderrdata:
            warnings.formatwarning = lambda x, *args, **kargs : str(x)
            warnings.warn(stderrdata)
            return
        
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
        is_muted = response.get("is_muted", False)
        converted_file_paths = response.get("converted_file_paths", [])
        must_display_default_mld = response.get("must_display_default_mld", False)

        if not args.no_mcd and ((rewritten_source and not redirect_output) or (not rewritten_source and not converted_file_paths)):
            # Display the MCD when not explicitely disabled and (there is a not redirected rewriting or no transformation at all)
            svg_path = output_path_radical.with_suffix(".svg")
            if svg_path.is_file() and input_path.stat().st_mtime <= svg_path.stat().st_mtime:
                display(SVG(filename=svg_path))

        if must_display_default_mld:
            # Display the Markdown MLD without header and exit
            display(Markdown(filename=f"{output_path_radical}_mld.md"))
            return

        if rewritten_source:
            if redirect_output:
                if not rewritten_source.startswith("%%mocodo"):
                    rewritten_source = f"%%mocodo\n{rewritten_source}"
                update_cell(rewritten_source)
            elif not is_muted:
                display(Markdown(OUTPUT_PART_HEADER.format(label=Path(f"{output_path_radical}.mcd").relative_to(output_dir))))
                print(rewritten_source)
        
        if converted_file_paths:
            if redirect_output:
                # Copy the last converted file source to the clipboard
                with contextlib.suppress(ImportError):
                    pyperclip = importlib.import_module("pyperclip")
                    converted_file_path = Path(converted_file_paths[-1])
                    pyperclip.copy(converted_file_path.read_text())
                    print(f"Source code of {converted_file_path.relative_to(output_dir)} copied to the clipboard.")
            if not is_muted:
                # Display all converted files
                for converted_file_path in converted_file_paths:
                    display_converted_file(Path(converted_file_path))


try:
    IPYTHON.register_magics(MocodoMagics)
except AttributeError:
    pass # necessary for launching the tests
else:
    print(f"Mocodo {MOCODO_VERSION} loaded.")

