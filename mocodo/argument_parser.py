import argparse
from collections import defaultdict
import gettext
import json
import locale
import os
import random
import re
import shutil
import sys
from pathlib import Path
import textwrap

from mocodo.tools.string_tools import strip_surrounds
from mocodo.tools.various import invert_dict
from mocodo.tools import load_mini_yaml

from .common import version
from .mocodo_error import MocodoError

SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(os.path.join(__file__)))

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
  Documentation         https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html
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



def init_localization(language):
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
        path = Path(f"{SCRIPT_DIRECTORY}/resources/res/messages_{language}.mo")
        with path.open("rb") as mo_contents:
            trans = gettext.GNUTranslations(mo_contents)
    except IOError:
        trans = gettext.NullTranslations()

    # Beware that the following line sets the global variable `_`. Using a single underscore
    # would clash with the gettext alias, EVEN IF THE CODE IS NOT REACHED: the compiler would
    # consider that _ is a local variable, and shadow the global one, resulting in:
    # UnboundLocalError: local variable '_' referenced before assignment
    # Solution : use `__` instead of `_` in any function that uses the gettext alias.
    trans.install()
    return language


class Transformations:

    metadata = {
        "arrange": {
            "category": "rw",
            "help": "rearrange the layout with either a Branch & Bound or a Genetic Algorithm",
            "aliases": [],
        },
        "ascii": {
            "category": "rw",
            "help": "rewrite the given elements in ASCII",
            "aliases": [],
            "op_tk": True,
        },
        "camel": {
            "category": "rw",
            "help": "rewrite the given elements in camelCase",
            "aliases": ["camel_case", "camelCase"],
            "op_tk": True,
        },
        "capitalize": {
            "category": "rw",
            "help": "rewrite the given elements by capitalizing the first letter of each word",
            "aliases": [],
            "op_tk": True,
        },
        "casefold": {
            "category": "rw",
            "help": "rewrite the given elements in lowercase, but more aggressively than 'lower'",
            "aliases": [],
            "op_tk": True,
        },
        "chen": {
            "category": "cv",
            "help": "convert the conceptual model into a Chen's ERD",
            "aliases": ["Chen"],
        },
        "create": {
            "category": "rw",
            "help": "try to infer types, entities, CIFs or DF arrows from the existing elements",
            "aliases": ["add", "insert", "make", "guess", "infer", "complete", "new"],
            "op_tk": True,
        },
        "crow": {
            "category": "cv",
            "help": "convert the conceptual model into a crow's foot ERD",
            "aliases": ["crowfoot", "crowsfoot"],
        },
        "data_dict": {
            "category": "cv",
            "help": "collect all the attributes of the MCD in a table",
            "aliases": ["data-dict", "data-dictionary"],
        },
        "defer": {
            "category": "cv",
            "help": "use an external web-service to further convert the result into a given graphical format (default: svg)",
            "aliases": ["deferred"],
        },
        "delete": {
            "category": "rw",
            "help": "suppress the given elements whenever possible",
            "aliases": ["del", "suppress", "erase", "remove", "hide"],
            "op_tk": True,
        },
        "drain": {
            "category": "rw",
            "help": "move any (1,1) association attribute to the appropriate entity",
            "aliases": [],
        },
        "echo": {
            "category": "rw",
            "help": "rewrite the source text as is",
            "aliases": [], 
        },
        "explode": {
            "category": "rw",
            "help": "decompose any n-ary (*,N) associations into n binary ones",
            "aliases": [],
        },
        "fix": {
            "category": "rw",
            "help": "try to fix common errors in the given elements",
            "aliases": [],
            "op_tk": True,
        },
        "flip": {
            "category": "rw",
            "help": "Apply a vertical (v), horizontal (h) or diagonal (d) symmetry to the diagram",
            "aliases": ["mirror", "reflect"],
            "op_tk": True,
        },
        "lower": {
            "category": "rw",
            "help": "rewrite the given elements in lowercase",
            "aliases": ["lowercase", "lower_case"],
            "op_tk": True,
        },
        "mute": {
            "category": "both",
            "help": "under Jupyter Notebook, do not display the result in the cell output",
            "aliases": ["quiet"],
        },
        "randomize": {
            "category": "rw",
            "help": "keep the stucture, but replace the given elements with random ones whenever possible",
            "aliases": ["rand", "random", "randomise", "obfuscate", "obscure"],
            "op_tk": True,
        },
        "relation": {
            "category": "cv",
            "help": "convert the conceptual model into a relational schema with the given template path",
            "aliases": ["relation_template"]
        },
        "snake": {
            "category": "rw",
            "help": "rewrite the given elements in snake_case",
            "aliases": ["snake_case"],
            "op_tk": True,
        },
        "split": {
            "category": "rw",
            "help": "decompose any n-ary (*,1) associations into n-1 binary ones",
            "aliases": [],
        },
        "swapcase": {
            "category": "rw",
            "help": "rewrite the given elements by swapping the case of each letter",
            "aliases": [],
            "op_tk": True,
        },
        "title": {
            "category": "rw",
            "help": "rewrite the given elements in Title Case",
            "aliases": [],
            "op_tk": True,
        },
        "uml": {
            "category": "cv",
            "help": "convert the conceptual model into a UML class diagram",
            "aliases": ["UML", "class_diagram"],
        },
        "upper": {
            "category": "rw",
            "help": "rewrite the given elements in UPPERCASE",
            "aliases": ["uppercase", "upper_case"],
            "op_tk": True,
        },
    }

    def __init__(self):
        template_folder_path = Path(f"{SCRIPT_DIRECTORY}/resources/relation_templates")
        aliases = defaultdict(list)
        for path in template_folder_path.glob("*.yaml"):
            if path.stem in self.metadata:
                raise MocodoError(26, _("The file '{path}' has the same name as the builtin transformation '{path.stem}'. Please rename it.").format(path=path)) # fmt: skip
            if "-" in path.name:
                continue
            data = load_mini_yaml.run(path)
            if "help" in data:
                self.metadata[path.stem] = {
                    "category": "cv",
                    "help": data["help"],
                    "aliases": [],
                }
            elif "parent" in data:
                aliases[data["parent"]].append(path.stem)
        for (parent, children) in aliases.items():
            self.metadata[parent]["aliases"] = children
        self.normalize = invert_dict({k: v["aliases"] for (k, v) in self.metadata.items()})
        self.normalize.update((k, k) for k in self.metadata)
        # recreate the dictionary to have it in alphabetical order
        self.metadata = {k: self.metadata[k] for k in sorted(self.metadata.keys(), key=lambda x: x.lower())}
        self.operations = {"rw": [], "cv": []}
        self.op_tk_rewritings = set(k for (k, v) in self.metadata.items() if v.get("op_tk"))
    
    def extract_subargs(self, arg):
        (subopt, __, tail) = arg.partition(":")
        try:
            subopt = self.normalize[subopt]
        except:
            valid = ", ".join(sorted(self.normalize.keys(), key=lambda x: x.lower()))
            raise MocodoError(45, _("The transformation '{subopt}' is not among the possible ones:\n{valid}.").format(subopt=subopt, valid=valid)) # fmt: skip
        result = extract_subargs(f"{subopt}:{tail}") # NB: calls the global function, not the method
        category = self.metadata[subopt]["category"]
        if category != "cv":
            self.operations["rw"].append(result)
        if category != "rw":
            self.operations["cv"].append(result)
        return result

    def get_help(self):
        result = []
        for (category, header) in ("rw", "REWRITING OPERATIONS"), ("cv", "CONVERSION OPERATIONS"), ("both", "BOTH CATEGORIES"):
            result.append(f"{header}:")
            for (name, transformation) in self.metadata.items():
                if transformation["category"] != category:
                    continue
                aliases = self.metadata[name]["aliases"]
                aliases = f". Aliases: {', '.join(aliases)}" if aliases else ""
                result.append(f"- {name}: {transformation['help']}{aliases};")
            result[-1] = result[-1][:-1] + "."  # replace the last semicolon by a dot
        return "\n".join(result)

transformations = Transformations()


def extract_subargs(arg):
    (subopt, _, tail) = arg.partition(":")
    subargs = {}
    for string in filter(None, tail.split(",")):
        subsubopt, equal, subsubarg = string.partition("=")
        if equal: # subopt:subsubopt= / subopt:subsubopt=subsubarg
            subsubarg = strip_surrounds(subsubarg, "''")
            subsubarg = strip_surrounds(subsubarg, '""')
        else: # subopt:subsubopt
            subsubarg = None
        subargs[subsubopt] = subsubarg
    return (subopt, subargs)

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

    parser = argparse.ArgumentParser(
        prog="mocodo",
        add_help=False,
        formatter_class=argparse.RawTextHelpFormatter,
        description=DESCRIPTION,
        epilog=EPILOG,
        allow_abbrev=False,
    )

    mocodo_group = parser.add_argument_group("OPTIONS ON MOCODO ITSELF")
    io_group = parser.add_argument_group("INPUT/OUTPUT")
    source_group = parser.add_argument_group("OPERATIONS ON THE SOURCE TEXT")
    aspect_group = parser.add_argument_group("ASPECT OF THE GRAPHICAL OUTPUT")

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
    io_group.add_argument("--input", "-i",
        metavar="PATH",
        help="the path of the input file. By default, the output files will be generated in the same directory",
    )
    
    (args, remaining_args) = parser.parse_known_args()

    if args.input and not os.path.exists(args.input):
        if os.path.exists(args.input + ".mcd"):
            args.input += ".mcd"
        else:  # the user has explicitely specified a non existent input file
            init_localization(default_params.get("language", args.language))
            raise MocodoError(2, _('The file "{input}" doesn\'t exist.').format(input=args.input))  # fmt: skip
    default_params["input"] = args.input

    if os.path.exists(args.params_path):
        default_params.update(json.loads(Path(args.params_path).read_text()))
    if not default_params["input"]:
        default_params["input"] = "sandbox.mcd"
    default_params["language"] = init_localization(default_params.get("language", args.language))
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
    io_group.add_argument("--svg_to",
        choices=["png", "pdf"],
        nargs="+",
        default=[],
        help="generate a PNG or a PDF version of the SVG output (requires CairoSVG)",
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
    io_group.add_argument("--no_mcd", "--quiet", "--mute",
        action="store_true",
        help="under Jupyter Notebook, do not render the conceptual diagram in the cell output",
    )
    io_group.add_argument("--mld",
        action="store_true",
        help="backward compatibility alias for '-t' (with no arguments). Same as '-t markdown' but, under Jupyter Notebook, does not prevent the rendering of the conceptual diagram in the cell output",
    )
    io_group.add_argument("--is_magic",
        action="store_true",
        help=argparse.SUPPRESS, # don't show this argument in the help message
    )

    source_group.add_argument("--transform", "-t",
        metavar="STR",
        nargs="*",
        type=transformations.extract_subargs,
        default=argparse.SUPPRESS, # causes no attribute to be added if the argument was not present
        help=textwrap.dedent("either make a new version of the MCD by applying sequentially the given rewriting operations, or convert it into the given formats or languages.\nUnder Jupyter Notebook, '-T' respectively replaces the current cell by the textual result, or copies it into the clipboard (pip3 install pyperclip).\n" + transformations.get_help()),
    )
    source_group.add_argument("--Transform", "--TRANSFORM", "-T",
        metavar="STR",
        nargs="*",
        type=transformations.extract_subargs,
        help=argparse.SUPPRESS, # don't show this argument in the help message
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
    aspect_group.add_argument("--gutters",
        metavar="STR",
        nargs="+",
        type=extract_subargs,
        default=argparse.SUPPRESS, 
        help="set the visibility and the contents of the lateral gutters",
    )

    parser.set_defaults(**default_params)
    params = vars(parser.parse_args(remaining_args))
    params["script_directory"] = SCRIPT_DIRECTORY
    params["output_name"] = Path(params["output_dir"]) / Path(params["input"]).stem
    params["rewrite"] = transformations.operations["rw"]
    params["convert"] = transformations.operations["cv"]
    params["redirect_output"] = ("-T" in remaining_args or "--Transform" in remaining_args)
    params["keys_to_hide"] = ["keys_to_hide", "params_path", "SCRIPT_DIRECTORY", "output_name", "rewrite", "convert", "redirect_output"]

    if not os.path.exists(params["input"]):
        path = Path(params["SCRIPT_DIRECTORY"], "resources", "pristine_sandbox.mcd")
        shutil.copyfile(path, params["input"])
    random.seed(params["seed"])
    try:
        params["title"] = params["title"].decode("utf8")
    except:
        pass
    return params
