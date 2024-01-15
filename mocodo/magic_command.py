import argparse
import contextlib
import importlib
import json
import re
import shlex
import warnings
from base64 import b64encode
from itertools import takewhile
from pathlib import Path

from IPython import get_ipython
from IPython.display import HTML, SVG, Image, Markdown, display

try:
    from IPython.display import Code
    latex = lambda x: Code(x, language='latex')
except ImportError:
    # Fallback for Basthon
    from IPython.display import Latex
    latex = lambda x: Latex(x)


from .__main__ import Printer, Runner
from .mocodo_error import MocodoError

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
params = """\\
{stdoutdata}"""
try:
    json.loads(params)
except:
    raise RuntimeError("Invalid JSON. Check your syntax on https://jsonlint.com.")
pathlib.Path("{output_dir}/params.json").write_text(params, encoding="utf8");'''

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

def read_and_cleanup_text(path):
    text = path.read_text(encoding="utf8")
    text = re.sub(r"(?m).+Generated by Mocodo.+\n+", "", text)
    return text

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
        display(Markdown(read_and_cleanup_text(path)))
    elif extension == "png":
        display(Image(filename=path, unconfined=False))
    elif extension == "html":
        text = path.read_text(encoding="utf8")
        text = re.sub('<!-- TO_BE_DELETED_BY_MOCODO_MAGIC -->.+\n', "", text)
        display(HTML(text))
    elif extension == "tex":
        display(latex(read_and_cleanup_text(path)))
    elif extension == "url":
        print(path.read_text(encoding="utf8")) # make the link clickable
    elif extension == "tsv":
        try:
            df = importlib.import_module("pandas").read_csv(path, sep="\t", header=0, index_col=False)
            df = df.style.set_properties(**{'text-align': 'left'}).set_table_styles([ dict(selector='th', props=[('text-align', 'left')] ) ])
            display(df)
        except ImportError:
            display(Markdown(f'```\n{path.read_text(encoding="utf8")}\n```'))
    else:
        display(Markdown(f"```{extension}\n{read_and_cleanup_text(path)}\n```"))

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
    parser.add_argument("--input", "-i")
    parser.add_argument("--output_dir")
    (args, remaining_args) = parser.parse_known_args(shlex.split(line))
    remaining_args = list(takewhile(lambda x: not x.startswith("#"), remaining_args))
    new_args = remaining_args[:]

    mocodo_notebook_dir = Path.cwd()
    if mocodo_notebook_dir.name != "mocodo_notebook":
        mocodo_notebook_dir = mocodo_notebook_dir / "mocodo_notebook"
        mocodo_notebook_dir.mkdir(parents=True, exist_ok=True)
    if not args.input:
        input_path = mocodo_notebook_dir / "sandbox.mcd"
        input_path.write_text(cell, encoding="utf8")
    else:
        input_path = Path(args.input)
        if not input_path.suffix:
            input_path = input_path.with_suffix(".mcd")

    if not args.output_dir:
        output_dir = mocodo_notebook_dir
    else:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    output_path_radical = output_dir / input_path.stem

    remaining_args.extend([
        "--input", str(input_path),
        "--output_dir", str(output_dir),
        "--is_magic",
    ]) # may override user's provided options

    stdoutdata = ""
    stderrdata = ""
    printer = Printer(accumulate=True)
    run = Runner(remaining_args, printer)
    try:
        stdoutdata = run()
    except MocodoError as err:
        stderrdata = str(err)
    except SystemExit: # raised by argparse when --help is used
        return
    
    if "--print_params" in remaining_args:
        update_cell(PARAM_TEMPLATE.format(stdoutdata=stdoutdata, output_dir=output_dir.relative_to(Path.cwd())))
        return
    
    response_path = Path(f"{output_path_radical}_response_for_magic_command.json")
    try: 
        response = json.loads(response_path.read_text(encoding="utf8"))
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        response = {}
    finally:
        with contextlib.suppress(FileNotFoundError): # From Python 3.8, use the missing_ok argument
            response_path.unlink()
    
    rewritten_source = response.get("rewritten_source", "")
    redirect_output = response.get("redirect_output", False)
    converted_file_paths = response.get("converted_file_paths", [])

    if stderrdata:
        message = stderrdata
        if rewritten_source:
            message = f"{rewritten_source}\n\n{message}"
        warnings.formatwarning = lambda x, *args, **kargs : str(x)
        warnings.warn(message)
        return
    
    if rewritten_source and not rewritten_source.startswith("%%mocodo"):
        new_args = " ".join(filter(lambda x: x not in response["args_to_delete"], new_args))
        new_args = response["opt_to_restore"] + new_args
        rewritten_source = f"%%mocodo{new_args}\n{rewritten_source}"
    
    for select in response.get("select", []):
        if select == "mcd":
            svg_path = output_path_radical.with_suffix(".svg")
            if svg_path.is_file() and input_path.stat().st_mtime <= svg_path.stat().st_mtime:
                # SVG(filename=...) argument not working under Basthon
                text = svg_path.read_text(encoding="utf8")
                display(SVG(text))
        elif select == "rw":
            path = output_path_radical.with_suffix(".mcd")
            display(Markdown(OUTPUT_PART_HEADER.format(label=path.relative_to(output_dir))))
            print(rewritten_source or cell)
        elif select == "cv":
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
                pyperclip.copy(converted_file_path.read_text(encoding="utf8"))
                print(f'⧉ {OK}The contents of "{converted_file_path.relative_to(output_dir)}" has been copied to the clipboard.{RESET}')
