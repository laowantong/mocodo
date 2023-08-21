import argparse
import shlex
import warnings
from pathlib import Path
from subprocess import PIPE, Popen

import pkg_resources
from IPython import get_ipython
from IPython.core.magic import Magics, line_cell_magic, magics_class
from IPython.display import HTML, Image, SVG, display, Markdown
from base64 import b64encode

try:
    MOCODO_VERSION = pkg_resources.get_distribution("mocodo").version
except pkg_resources.DistributionNotFound:
    MOCODO_VERSION = "(unknown version)"  # For tests during CI


IPYTHON = get_ipython()

def update_cell(content):
    IPYTHON.set_next_input(content, replace=True)

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
        parser.add_argument("--no_text", action="store_true")
        parser.add_argument("--replace", action="store_true")
        parser.add_argument("--input")
        parser.add_argument("--output_dir")
        (args, remaining_args) = parser.parse_known_args(shlex.split(line))

        Path("mocodo_notebook").mkdir(parents=True, exist_ok=True)

        if not args.input:
            input_path = Path("mocodo_notebook/sandbox.mcd")
            input_path.write_text(cell, encoding="utf8")
        else:
            input_path = Path(args.input)
            if not input_path.suffix:
                input_path = input_path.with_suffix(".mcd")

        if not args.output_dir:
            output_dir = Path("mocodo_notebook")
        else:
            output_dir = Path(args.output_dir)
            try:
                output_dir.mkdir(parents=True, exist_ok=True)
            except OSError:
                if not output_dir.is_dir():
                    raise
        output_name = output_dir / input_path.stem

        remaining_args.extend(["--input", str(input_path), "--output_dir", str(output_dir)]) # may override user's provided options
        try: # prevent explicit option --relations to override HTML generation
            remaining_args.insert(remaining_args.index("--relations") + 1, "html")
        except ValueError:
            remaining_args.extend(["--relations", "html"])

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
        if any(x in remaining_args for x in ("--update", "-u")):
            updated_source = input_path.read_text().rstrip()
            if args.replace:
                update_cell(updated_source)
                return # abort, since this erases the [Out] section after returning asynchronously
        
        defer_path = output_dir / "things_to_be_displayed.tmp"
        if defer_path.is_file():
            for filename in defer_path.read_text().splitlines():
                extension=Path(filename).suffix[1:]
                if extension == "svg":
                    # Fix a maximum width for SVG images:
                    # https://stackoverflow.com/questions/51452569/how-to-resize-rescale-a-svg-graphic-in-an-ipython-jupyter-notebook
                    svg = b64encode(Path(filename).read_bytes()).decode("utf8")
                    display(HTML(f'<img max-width="100%" src="data:image/svg+xml;base64,{svg}">'))
                elif extension == "md":
                    display(Markdown(filename=filename))
                else:
                    display(Image(filename=filename, unconfined=False))
            defer_path.unlink()
        
        if any(x in remaining_args for x in ("-e", "-x", "--export")):
            print(stdoutdata, end="")
            return
        
        svg_path = Path(output_name).with_suffix(".svg")
        if svg_path.is_file() and input_path.stat().st_mtime <= svg_path.stat().st_mtime:
            if not args.no_mcd:
                display(SVG(filename=svg_path))
            if args.mld:
                mld = Path(output_name).with_suffix(".html").read_text("utf8")
                display(HTML(mld))

        if updated_source and not args.no_text:
            print(updated_source)


try:
    IPYTHON.register_magics(MocodoMagics)
except AttributeError:
    pass # necessary for launching the tests
else:
    print(f"Mocodo {MOCODO_VERSION} loaded.")

