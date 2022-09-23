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
from time import time

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
                        Ile du Saulcy
                        57000 Metz
                        France
"""  # NB: accents raise an error in Jupyter Notebook


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
            language = re.search("\W*(\w+)", Path("/tmp/languages.txt").read_text()).group(1)
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

    trans.install()
    return language


def has_expired_factory(timeout):
    if timeout:
        timeout += time()
        return lambda: time() > timeout
    else:
        return lambda: False


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
    )
    mocodo_group = parser.add_argument_group("OPTIONS ON MOCODO ITSELF")
    io_group = parser.add_argument_group("INPUT/OUTPUT")
    aspect_group = parser.add_argument_group("ASPECT OF THE GRAPHICAL OUTPUT")
    relational_group = parser.add_argument_group("RELATIONAL OUTPUT")
    source_group = parser.add_argument_group("MODIFICATIONS OF THE SOURCE TEXT")
    bb_group = parser.add_argument_group(
        "BRANCH & BOUND LAYOUT REARRANGEMENT",
        "sub-options triggered by the option --arrange=bb",
    )
    ga_group = parser.add_argument_group(
        "GENETIC ALGORITHM LAYOUT REARRANGEMENT",
        "sub-options triggered by the option --arrange=ga",
    )
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

    mocodo_group.add_argument(
        "--language",
        metavar="CODE",
        type=str,
        help="override the automatic localization of the messages with the given language code (e.g., 'fr', 'en', ...)",
    )
    io_group.add_argument(
        "--params_path",
        metavar="PATH",
        default="params.json",
        help="the path of the parameter file. If omitted, use 'params.json' in the input directory. If non existent, use default parameters.",
    )
    io_group.add_argument(
        "--input",
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

    mocodo_group.add_argument(
        "--help",
        action="help",
        help="show this help message and exit",
    )
    mocodo_group.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + version,
        help="display the version number, then exit",
    )
    mocodo_group.add_argument(
        "--restore",
        action="store_true",
        help="recreate a pristine version of the files 'sandbox.mcd' and 'params.json' in the input directory, then exit",
    )

    aspect_group.add_argument(
        "--df",
        metavar="STR",
        type=str,
        default="DF",
        help="the acronym to be circled in a functional dependency",
    )
    aspect_group.add_argument(
        "--card_format",
        metavar="STR",
        type=str,
        nargs="?",
        default="{min_card},{max_card}",
        help="format string for minimal and maximal cardinalities",
    )
    aspect_group.add_argument(
        "--strengthen_card",
        metavar="STR",
        type=str,
        nargs="?",
        default="_1,1_",
        help="string for relative cardinalities",
    )
    source_group.add_argument(
        "--flex",
        metavar="FLOAT",
        type=float,
        default=0.75,
        help="flex straight legs whose cardinalities may collide",
    )
    aspect_group.add_argument(
        "--colors",
        metavar="PATH",
        default="bw",
        help="the color palette to use when generating the drawing. Name (without extension) of a file located in the directory 'colors', or path to a personal file",
    )
    aspect_group.add_argument(
        "--shapes",
        metavar="PATH",
        help="specification of the fonts, dimensions, etc. Name (without extension) of a file located in the directory 'shapes', or path to a personal file",
    )
    aspect_group.add_argument(
        "--scale",
        metavar="RATE",
        type=scale,
        default=1,
        help="scale the diagram by the given factor",
    )
    aspect_group.add_argument(
        "--adjust_width",
        metavar="RATE",
        type=scale,
        default=1,
        help="scale all calculated text widths by the given factor",
    )
    aspect_group.add_argument(
        "--hide_notes", action="store_true", help="ignore the hovering of annotated elements"
    )
    aspect_group.add_argument(
        "--detect_overlaps",
        action="store_true",
        help="raise an error when horizontal or vertical legs overlap",
    )

    relational_group.add_argument(
        "--relations",
        metavar="NAME",
        nargs="*",
        default=["html", "text"],
        help="one or several templates for the generated relational schemas. Cf. directory 'relation_templates'",
    )
    relational_group.add_argument(
        "--disambiguation",
        choices=["numbers_only", "notes"],
        default="notes",
        help="specify the way to disambiguate outer attributes",
    )
    relational_group.add_argument(
        "--title",
        metavar="STR",
        default=_("Untitled").encode("utf8"),
        type=str,
        help="database name (used for SQL output)",
    )
    relational_group.add_argument(
        "--guess_title",
        action="store_true",
        help="use the name of the most referred entity as title",
    )

    io_group.add_argument(
        "--output_dir",
        metavar="PATH",
        help="the directory of the output files",
    )
    io_group.add_argument(
        "--encodings",
        metavar="STR",
        nargs="*",
        help="one or several encodings to be tried successively when reading the input file",
    )
    io_group.add_argument(
        "--png",
        action="store_true",
        help="generate a PNG version of the SVG output (requires CairoSVG)",
    )
    io_group.add_argument(
        "--pdf",
        action="store_true",
        help="generate a PDF version of the SVG output (requires CairoSVG)",
    )
    io_group.add_argument(
        "--print_params",
        action="store_true",
        help="display the contents of the parameter file, then exit",
    )
    io_group.add_argument(
        "--reuse_geo",
        action="store_true",
        help="reuse the geometry file of the previous execution",
    )

    source_group.add_argument(
        "--arrange",
        nargs="?",
        const="bb",
        choices=["bb", "ga", "lp"],
        help="rearrange the layout with either a Branch & Bound, a Genetic Algorithm, or a Linear Program solver, then exit",
    )
    source_group.add_argument(
        "--timeout",
        metavar="SECONDS",
        type=int,
        help="limit the duration of the layout rearrangement",
    )
    source_group.add_argument(
        "--verbose",
        action="store_true",
        help="display some gory details during the layout rearrangement",
    )
    source_group.add_argument(
        "--fit",
        metavar="INT",
        type=int,
        const=0,
        nargs="?",
        help="fit the layout in the nth smallest grid",
    )
    source_group.add_argument(
        "--flip",
        choices=["h", "v", "d"],
        help="display an horizontal / vertical / diagonal flip of the input file, then exit",
    )
    source_group.add_argument(
        "--obfuscate",
        metavar="PATH",
        type=os.path.abspath,
        nargs="?",
        const="lorem_ipsum.txt",
        help="display an obfuscated version of the input file, then exit. Cf. directory 'lorem'",
    )
    source_group.add_argument(
        "--obfuscation_min_distance",
        metavar="NAT*",
        type=positive_integer,
        default=3,
        help="minimal Damerau-Levenshtein's distance between any two obfuscated labels",
    )
    source_group.add_argument(
        "--seed",
        metavar="FLOAT",
        type=float,
        help="initial value for the random number generator",
    )

    bb_group.add_argument(
        "--call_limit",
        metavar="NAT*",
        type=positive_integer,
        default=10000,
        help="maximal number of calls for a given starting box",
    )
    bb_group.add_argument(
        "--min_objective",
        metavar="NAT*",
        type=positive_integer,
        default=0,
        help="best acceptable fitness for a layout",
    )
    bb_group.add_argument(
        "--max_objective",
        metavar="NAT*",
        type=positive_integer,
        default=15,
        help="worst acceptable fitness for a layout",
    )
    bb_group.add_argument(
        "--organic",
        action="store_true",
        help="unconstrained Branch & Bound",
    )

    ga_group.add_argument(
        "--population_size",
        metavar="NAT*",
        type=positive_integer,
        default=1000,
        help="number of individuals to evolve",
    )
    ga_group.add_argument(
        "--crossover_rate",
        metavar="RATE",
        type=rate,
        default=0.9,
        help="crossover rate, between 0 and 1",
    )
    ga_group.add_argument(
        "--mutation_rate",
        metavar="RATE",
        type=rate,
        default=0.06,
        help="mutation rate, between 0 and 1",
    )
    ga_group.add_argument(
        "--sample_size",
        metavar="NAT*",
        type=positive_integer,
        default=7,
        help="the sample size in tournaments",
    )
    ga_group.add_argument(
        "--max_generations",
        metavar="NAT*",
        type=positive_integer,
        default=300,
        help="maximal number of generations",
    )
    ga_group.add_argument(
        "--plateau",
        metavar="NAT*",
        type=positive_integer,
        default=30,
        help="maximal number of consecutive generations without improvement",
    )

    nb_group.add_argument(
        "--mld",
        action="store_true",
        help="display the HTML relational model in the cell output",
    )
    nb_group.add_argument(
        "--no_mcd",
        action="store_true",
        help="do not display the conceptual diagram in the cell output",
    )
    nb_group.add_argument(
        "--replace",
        action="store_true",
        help="replaces the cell contents by its output",
    )

    parser.set_defaults(**default_params)
    params = vars(parser.parse_args(remaining_args))
    params["added_keys"] = ["added_keys", "params_path"]
    add_key("script_directory", script_directory)
    add_key("has_expired", has_expired_factory(params["timeout"]))
    add_key(
        "output_name",
        os.path.join(params["output_dir"], os.path.splitext(os.path.basename(params["input"]))[0]),
    )

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
