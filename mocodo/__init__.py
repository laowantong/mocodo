import argparse
import importlib
import shlex
from pathlib import Path
from .__main__ import Printer, Runner

from .argument_parser import SCRIPT_DIRECTORY

def load_ipython_extension(ipython):
    # This function is called when the extension is loaded in a notebook
    # with %load_ext mocodo or %reload_ext mocodo.

    mocodo = importlib.import_module("mocodo.magic").mocodo
    ipython.register_magic_function(mocodo, 'line_cell', 'mocodo')
    
    pkg_resources = importlib.import_module("pkg_resources")

    try:
        MOCODO_VERSION = pkg_resources.get_distribution("mocodo").version
    except pkg_resources.DistributionNotFound:
        MOCODO_VERSION = "(unknown version)"  # For tests during CI
    print(f"Mocodo {MOCODO_VERSION} loaded.")


def mocodo(arg_string=None, quiet=True):
    """
    Simulate the command line `mocodo` as a function, with the same arguments provided as a string.
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--input", "-i")
    (args, remaining_args) = parser.parse_known_args(shlex.split(arg_string))

    input_path = args.input
    if not args.input:
        # No path is provided for the source of the MCD. Fall back to the pristine sandbox.
        input_path = str(Path(SCRIPT_DIRECTORY, "resources", "pristine_sandbox.mcd"))

    remaining_args.extend(["--input", input_path])
    printer = Printer(quiet=quiet)
    run = Runner(remaining_args, printer)
    run()
