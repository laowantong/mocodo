from IPython.core.magic import Magics, line_cell_magic, magics_class
from IPython.display import HTML, SVG, display
from IPython import get_ipython
import argparse
import warnings
from subprocess import PIPE, Popen
from pathlib import Path

import pkg_resources

try:
    MOCODO_VERSION = pkg_resources.get_distribution("mocodo").version
except pkg_resources.DistributionNotFound:
    MOCODO_VERSION = "(unknown version)"  # For tests during CI


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
            if svg_path.is_file() and input_path.stat().st_mtime <= svg_path.stat().st_mtime:
                if not notebook_options.no_mcd:
                    display(SVG(filename=svg_path))
                if notebook_options.mld:
                    mld = Path(output_name).with_suffix(".html").read_text("utf8")
                    display(HTML(mld))
                return True

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("--no_mcd", action="store_true")
        parser.add_argument("--mld", action="store_true")
        parser.add_argument("--input")
        parser.add_argument("--output_dir")
        (notebook_options, options) = parser.parse_known_args(line.split())

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

        def execute_command(options):
            global stdoutdata
            process = Popen(["mocodo"] + options, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            stdoutdata, stderrdata = process.communicate()
            try:
                stdoutdata = stdoutdata.strip().decode("utf8")
                stderrdata = stderrdata.strip().decode("utf8")
            except:
                pass
            status = process.wait()
            if status == 0 and not stderrdata:
                return True
            warnings.formatwarning = lambda x, *args, **kargs : str(x)
            warnings.warn(stderrdata)

        if execute_command(options):
            if not display_diagrams():
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
                    get_ipython().set_next_input("\n".join(form), replace = True)
                    return
                if "--help" in options:
                    print(stdoutdata)
                    return
                if "--replace" in options:
                    get_ipython().set_next_input("%%mocodo\n" + stdoutdata.rstrip(), replace = True)
                    return
                print(f"%%mocodo\n{stdoutdata.rstrip()}")
                if not notebook_options.no_mcd or notebook_options.mld:
                    parser.add_argument("--arrange", nargs="?")
                    parser.add_argument("--obfuscate", nargs="?")
                    parser.add_argument("--flip", nargs="?")
                    (_, options) = parser.parse_known_args(options)
                    input_path.write_text(stdoutdata, encoding="utf8")
                    options.extend(["--input", str(input_path), "--output_dir", str(output_dir)])
                    if execute_command(options):
                        display_diagrams()



def load_ipython_extension(ipython):
    ipython.register_magics(MocodoMagics)
    print(f"Mocodo {MOCODO_VERSION} loaded.")

load_ipython_extension(get_ipython())

