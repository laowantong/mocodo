import argparse
import os
from pathlib import Path
import shlex

from .__main__ import Runner
from .common import Printer

SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(os.path.join(__file__)))

def mocodo(arg_string="", source=""):
    """
    Call `mocodo` as a function.
    When no source path is provided, the given source is used, and written to the output directory
    as "sandbox.mcd".
    When no source is provided, either as a file path or a string, the pristine sandbox is used as
    a fallback.

    Args:
        arg_string (str, optional): The same arguments as the command line. Defaults to "".
        source (str, optional): The source code of the MCD file. Defaults to "".
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--input", "-i")
    parser.add_argument("--output_dir")
    (args, remaining_args) = parser.parse_known_args(shlex.split(arg_string))
    input_dir = Path.cwd()

    # Create or retrieve the path to the source file.
    if not args.input:
        # No path is provided for the source of the MCD.
        if source:
            # The source is provided as a string. Write it to a file named "sandbox.mcd".
            input_path = input_dir / "sandbox.mcd"
            input_path.write_text(source, encoding="utf8")
        else:
            # No source is provided. Fall back to the pristine sandbox.
            input_path = Path(SCRIPT_DIRECTORY, "resources", "pristine_sandbox.mcd")
    else:
        # Retrieve the path to the source file.
        input_path = Path(args.input)
        if not input_path.suffix:
            input_path = input_path.with_suffix(".mcd")

    if not args.output_dir:
        # No output directory is provided. Fall back to the input directory.
        output_dir = input_dir
    else:
        # Retrieve the path to the output directory, and create it if it doesn't exist.
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    remaining_args.extend([
        "--input", str(input_path),
        "--output_dir", str(output_dir)
    ])

    printer = Printer(accumulate=True) # silence the success messages
    run = Runner(remaining_args, printer)
    run()
