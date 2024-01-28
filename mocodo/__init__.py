import argparse
import importlib
import os
import shlex
from pathlib import Path

from .__main__ import Printer, Runner
from .argument_parser import SCRIPT_DIRECTORY
from .version_number import version

def load_ipython_extension(ipython):
    # This function is called when the extension is loaded in a notebook
    # with %load_ext mocodo or %reload_ext mocodo.
    mocodo = importlib.import_module("mocodo.magic").mocodo
    ipython.register_magic_function(mocodo, 'line_cell', 'mocodo')
    print(f"Mocodo {version} loaded.")


def mocodo(arg_string=None, quiet=True):
    """
    Simulate the command line `mocodo` as a function, with the same arguments provided as a string.
    With `quiet=True`, no success messages are printed.
    In either case, return the printed messages accumulated in a "\n" separated string.
    Exceptions:
    - For "--version", returns the version number as a string.
    - For "--help", returns None.
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--input", "-i")
    parser.add_argument("--output_dir")
    (args, remaining_args) = parser.parse_known_args(shlex.split(arg_string))

    input_path = args.input
    if not args.input:
        # No path is provided for the source of the MCD. Fall back to the pristine sandbox.
        input_path = str(Path(SCRIPT_DIRECTORY, "resources", "pristine_sandbox.mcd"))
    if not args.output_dir:
        output_dir = Path(os.getcwd())

    remaining_args.extend([
        "--input", str(input_path),
        "--output_dir", str(output_dir),
    ]) # may override user's provided options
    printer = Printer(quiet=quiet)
    try:
        run = Runner(remaining_args, printer)
    except SystemExit: # raised by argparse with certain arguments: --help, --version
        if "--version" in remaining_args:
            return version
        return
    run()
    return "".join(printer.accumulator)
