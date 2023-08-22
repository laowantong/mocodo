import argparse
import gettext
import json
import locale
import os
import random
import re
import sys
from io import open
from pathlib import Path

from mocodo.tools.string_tools import strip_surrounds

from .common import version
from .mocodo_error import MocodoError

DESCRIPTION = """
NAME:
  Mocodo - An Entity-Relation Diagram Generator.

DESCRIPTION:
  Mocodo is an open-source tool for designing and teaching relational databases.
  It takes as an input a textual description of both entities and associations
  of an entity-relationship diagram (ERD). It outputs a vectorial drawing in SVG
  and a relational schema in various formats (SQL, LaTeX, Markdown, etc.).

NOTE:
  Each one of the following values is:
  - explicitely specified by the user as a command line option;
  - otherwise, retrieved from a file located at --params_path;
  - otherwise, retrieved from a file named 'params.json' in the input directory;
  - otherwise, calculated from a default value, possibly dependant of your system.
"""

EPILOG = """
SEE ALSO:
  Online version        https://mocodo.net
  Source code           https://github.com/laowantong/mocodo
  Localization          https://www.transifex.com/aristide/mocodo/

LICENSE:
  MIT LICENSE.

CONTACT:
  Mail                  <author.full.name>@univ-lorraine.fr
  Author                Aristide Grange
  Address               Université de Lorraine
                        Laboratoire LCOMS - UFR MIM
                        3 rue Augustin Fresnel
                        57070 METZ Technopôle
                        France
"""

class ArgumentDefaultsRawDescriptionHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawDescriptionHelpFormatter,
):
    pass


def init_localization(script_directory, language):
    if not language:
        if (
            sys.platform.lower().startswith("darwin")
            and os.system("defaults read -g AppleLanguages > /tmp/languages.txt") == 0
        ):
            language = re.search(r"\W*(\w+)", Path("/tmp/languages.txt").read_text()).group(1)
        else:
            try:
                language = locale.getdefaultlocale()[0][:2]
            except:
                language = "en"
    try:
        path = Path(f"{script_directory}/resources/res/messages_{language}.mo")
        with path.open("rb") as mo_contents:
            trans = gettext.GNUTranslations(mo_contents)
    except IOError:
        trans = gettext.NullTranslations()

    # Beware that the following line set the global variable `_`. Using a single underscore
    # would clash with the gettext alias, EVEN IF THE CODE IS NOT REACHED: the compiler would
    # consider that _ is a local variable, and shadow the global one, resulting in:
    # UnboundLocalError: local variable '_' referenced before assignment
    # Solution : use `__` instead of `_` in any function that uses the gettext alias.
    trans.install()
    return language


def extract_subargs(arg):
    (subopt, _, tail) = arg.partition(":")
    subargs = {}
    for string in filter(None, tail.split(",")):
        subsubopt, _, subsubarg = string.partition("=")
        subsubarg = strip_surrounds(subsubarg, "''")
        subsubarg = strip_surrounds(subsubarg, '""')
        subargs[subsubopt] = subsubarg
    return subopt, subargs


def rate(string):
    try:
        value = float(string)
    except ValueError:
        msg = f"The rate {repr(string)} cannot be coerced to float"
        raise argparse.ArgumentTypeError(msg)
    if not (0 <= value <= 1):
        msg = f"The rate {repr(string)} is not between 0 and 1"
        raise argparse.ArgumentTypeError(msg)
    return value


def scale(string):
    try:
        value = float(string)
    except ValueError:
        msg = f"The scale {repr(string)} cannot be coerced to float"
        raise argparse.ArgumentTypeError(msg)
    if value <= 0:
        msg = f"The scale {repr(string)} is not strictly positive"
        raise argparse.ArgumentTypeError(msg)
    return value


def non_negative_integer(string):
    try:
        value = int(string)
    except ValueError:
        msg = f"The value {repr(string)} cannot be coerced to an integer"
        raise argparse.ArgumentTypeError(msg)
    if value < 0:
        msg = f"The integer {repr(string)} is negative"
        raise argparse.ArgumentTypeError(msg)
    return value


def positive_integer(string):
    try:
        value = int(string)
    except ValueError:
        msg = f"The value {repr(string)} cannot be coerced to an integer"
        raise argparse.ArgumentTypeError(msg)
    if value <= 0:
        msg = f"The integer {repr(string)} is negative or zero"
        raise argparse.ArgumentTypeError(msg)
    return value

def parsed_arguments():
    def add_key(key, value):
        params[key] = value
        params["added_keys"].append(key)

    script_directory = os.path.dirname(os.path.realpath(os.path.join(__file__)))
    parser = argparse.ArgumentParser(
        prog="mocodo",
        add_help=False,
        formatter_class=ArgumentDefaultsRawDescriptionHelpFormatter,
        description=DESCRIPTION,
        epilog=EPILOG,
        allow_abbrev=False,
    )

    mocodo_group = parser.add_argument_group("OPTIONS ON MOCODO ITSELF")
    io_group = parser.add_argument_group("INPUT/OUTPUT")
    source_group = parser.add_argument_group("OPERATIONS ON THE SOURCE TEXT")
    aspect_group = parser.add_argument_group("ASPECT OF THE GRAPHICAL OUTPUT")
    nb_group = parser.add_argument_group(
        "NOTEBOOK SPECIFIC OPTIONS",
        "ignored when called from the command line",
    )

    if sys.platform.lower().startswith("darwin"):
        default_params = {
            "encodings": ["utf8", "macroman"],
            "shapes": "copperplate",
        }
    elif sys.platform.lower().startswith("win"):
        default_params = {
            "encodings": ["utf8", "ISO_8859-15"],
            "shapes": "trebuchet",
        }
    else:  # linux
        default_params = {
            "encodings": ["utf8", "ISO_8859-15"],
            "shapes": "serif",
        }

    # First, add the arguments that need some preprocessing

    mocodo_group.add_argument("--language",
        metavar="CODE",
        type=str,
        help="override the automatic localization of the messages with the given language code (e.g., 'fr', 'en', ...)",
    )
    io_group.add_argument("--params_path",
        metavar="PATH",
        default="params.json",
        help="the path of the parameter file. If omitted, use 'params.json' in the input directory. If non existent, use default parameters.",
    )
    io_group.add_argument("--input",
        metavar="PATH",
        help="the path of the input file. By default, the output files will be generated in the same directory",
    )
    
    (args, remaining_args) = parser.parse_known_args()

    if args.input and not os.path.exists(args.input):
        if os.path.exists(args.input + ".mcd"):
            args.input += ".mcd"
        else:  # the user has explicitely specified a non existent input file
            init_localization(script_directory, default_params.get("language", args.language))
            raise MocodoError(18, _('The file "{input}" doesn\'t exist.').format(input=args.input))  # fmt: skip
    default_params["input"] = args.input

    if os.path.exists(args.params_path):
        default_params.update(json.loads(Path(args.params_path).read_text()))
    if not default_params["input"]:
        default_params["input"] = "sandbox.mcd"
    default_params["language"] = init_localization(
        script_directory,
        default_params.get("language", args.language),
    )
    default_params.setdefault("output_dir", os.path.dirname(default_params["input"]))

    mocodo_group.add_argument("--help",
        action="help",
        help="show this help message and exit",
    )
    mocodo_group.add_argument("--version",
        action="version",
        version="%(prog)s " + version,
        help="display the version number, then exit",
    )
    mocodo_group.add_argument("--restore",
        action="store_true",
        help="recreate a pristine version of the files 'sandbox.mcd' and 'params.json' in the input directory, then exit",
    )

    io_group.add_argument("--output_dir",
        metavar="PATH",
        help="the directory of the output files",
    )
    io_group.add_argument("--encodings",
        metavar="STR",
        nargs="*",
        help="one or several encodings to be tried successively when reading the input file",
    )
    io_group.add_argument("--png",
        action="store_true",
        help="generate a PNG version of the SVG output (requires CairoSVG)",
    )
    io_group.add_argument("--pdf",
        action="store_true",
        help="generate a PDF version of the SVG output (requires CairoSVG)",
    )
    io_group.add_argument("--print_params",
        action="store_true",
        help="display the contents of the parameter file, then exit",
    )
    io_group.add_argument("--reuse_geo",
        action="store_true",
        help="reuse the geometry file of the previous execution",
    )
    io_group.add_argument("--uid_suffix",
        metavar="INT",
        type=non_negative_integer,
        default=0,
        help="discriminate between multiple SVG of the same interactive diagram",
    )
    io_group.add_argument("--defer",
        nargs="*",
        choices=["svg", "png", "pdf"],
        default=["svg"],
        help="defer the post-processing of some outputs to an external web-service",
    )

    source_group.add_argument("-r", "--rewrite",
        metavar="STR",
        nargs="*",
        type=extract_subargs,
        # default=["echo"],
        help="make a new version of the MCD by applying one or several modifications",
    )
    source_group.add_argument("-e", "-x", "--export",
        metavar="STR",
        nargs="+",
        type=extract_subargs,
        help="translate all or parts of the MCD into a different format",
    )
    source_group.add_argument("--relations",
        metavar="STEM_OR_PATH",
        nargs="*",
        default=["html", "text"],
        help="use one or several templates to transform the MCD into a relational model. Name (without extension) of files located in the directory 'relation_templates', or path to personal files",
    )
    source_group.add_argument("--seed",
        metavar="FLOAT",
        type=float,
        help="initial value for the random number generator",
    )
    source_group.add_argument("--disambiguation",
        choices=["numbers_only", "notes"],
        default="notes",
        help="specify the way to disambiguate outer attributes during the conversion to a relational model",
    )
    source_group.add_argument("--title",
        metavar="STR",
        default=_("Untitled").encode("utf8"),
        type=str,
        help="name of the model, used at various places (file system, database, etc.)",
    )
    aspect_group.add_argument("--df",
        metavar="STR",
        type=str,
        default="DF",
        help="the acronym to be circled in a functional dependency",
    )
    aspect_group.add_argument("--card_format",
        metavar="STR",
        type=str,
        nargs="?",
        default="{min_card},{max_card}",
        help="format string for minimal and maximal cardinalities",
    )
    aspect_group.add_argument("--strengthen_card",
        metavar="STR",
        type=str,
        nargs="?",
        default="_1,1_",
        help="string for relative cardinalities",
    )
    aspect_group.add_argument("--flex",
        metavar="FLOAT",
        type=float,
        default=0.75,
        help="flex straight legs whose cardinalities may collide",
    )
    aspect_group.add_argument("--colors",
        metavar="STEM_OR_PATH",
        default="bw",
        help="the color palette to use when generating the drawing. Name (without extension) of a file located in the directory 'colors', or path to a personal file",
    )
    aspect_group.add_argument("--shapes",
        metavar="STEM_OR_PATH",
        help="specification of the fonts, dimensions, etc. Name (without extension) of a file located in the directory 'shapes', or path to a personal file",
    )
    aspect_group.add_argument("--scale",
        metavar="RATE",
        type=scale,
        default=1,
        help="scale the diagram by the given factor",
    )
    aspect_group.add_argument("--adjust_width",
        metavar="RATE",
        type=scale,
        default=1,
        help="scale all calculated text widths by the given factor",
    )
    aspect_group.add_argument("--hide_notes",
        action="store_true",
        help="ignore the hovering of annotated elements",
    )
    aspect_group.add_argument("--detect_overlaps",
        action="store_true",
        help="raise an error when horizontal or vertical legs overlap",
    )
    aspect_group.add_argument("--left_gutter",
        choices=["on", "off", "auto"],
        default="auto",
        help="show the status of candidate identifiers in each entity",
    )
    aspect_group.add_argument("--left_gutter_strong_id",
        metavar="STR",
        default="ID",
        type=str,
        help="string to be used in the left gutter for strong identifiers",
    )
    aspect_group.add_argument("--left_gutter_weak_id",
        metavar="STR",
        default="id",
        type=str,
        help="string to be used in the left gutter for weak identifiers",
    )
    aspect_group.add_argument("--left_gutter_alt_ids",
        metavar="STR",
        nargs="+",
        default=list("123456789"),
        help="strings to be used in the left gutter for alt identifiers",
    )

    nb_group.add_argument("--mld",
        action="store_true",
        help="display the HTML relational model in the cell output",
    )
    nb_group.add_argument("--no_mcd",
        action="store_true",
        help="do not display the conceptual diagram in the cell output",
    )
    nb_group.add_argument("--no_text",
        action="store_true",
        help="do not print the rewritten MCD source in the cell output",
    )
    nb_group.add_argument("--replace",
        action="store_true",
        help="replaces the cell contents by its output",
    )

    parser.set_defaults(**default_params)
    params = vars(parser.parse_args(remaining_args))
    alt_ids = params["left_gutter_alt_ids"]
    alt_ids += list("123456789")[len(alt_ids):]
    params["left_gutter_alt_ids"] = dict(zip("123456789", alt_ids))
    params["added_keys"] = ["added_keys", "params_path"]
    add_key("script_directory", script_directory)
    add_key("output_name", os.path.join(params["output_dir"], os.path.splitext(os.path.basename(params["input"]))[0]))

    if not os.path.exists(params["input"]):
        import shutil  # fmt: skip
        shutil.copyfile(
            Path(params["script_directory"]) / "resources" / "pristine_sandbox.mcd",
            params["input"],
        )
    random.seed(params["seed"])
    try:
        params["title"] = params["title"].decode("utf8")
    except:
        pass
    return params
