import argparse
import os
from pathlib import Path
import shlex
from . import __version__, SCRIPT_DIRECTORY
from .__main__ import Printer, Runner


def mocodo(arg_string="", quiet=True):
    """
    Simulate the command line `mocodo` as a function, with the same arguments provided as a string.
    With `quiet=True`, no success messages are printed.
    In either case, return the printed messages accumulated in a "\n" separated string.
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--input", "-i")
    parser.add_argument("--output_dir")
    (args, remaining_args) = parser.parse_known_args(shlex.split(arg_string))

    input_path = args.input
    if not args.input:
        # No path is provided for the source of the MCD. Fall back to the pristine sandbox.
        input_path = str(Path(SCRIPT_DIRECTORY, "resources", "pristine_sandbox.mcd"))
    
    output_dir = args.output_dir
    if not args.output_dir:
        output_dir = os.getcwd()

    remaining_args.extend([
        "--input", input_path,
        "--output_dir", output_dir,
    ]) # may override user's provided options
    printer = Printer(quiet=quiet)
    try:
        run = Runner(remaining_args, printer)
    except SystemExit: # raised by argparse with certain arguments: --help, --version
        if "--version" in remaining_args:
            return __version__
        return
    run()
    return "".join(printer.accumulator)
