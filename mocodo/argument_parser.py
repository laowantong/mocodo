import argparse
import contextlib
import gettext
import json
import locale
import os
import random
import re
import importlib
import sys
from pathlib import Path

from mocodo.tools.string_tools import strip_surrounds
from mocodo.tools.various import invert_dict

from .version_number import version
from .mocodo_error import MocodoError

SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(os.path.join(__file__)))

class ArgumentDefaultsRawDescriptionHelpFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawDescriptionHelpFormatter,
):
    pass

def init_localization(language):
    if not language:
        if (
            sys.platform.lower().startswith("darwin")
            and os.system("defaults read -g AppleLanguages > /tmp/languages.txt") == 0
        ):
            language = re.search(r"\W*(\w+)", Path("/tmp/languages.txt").read_text(encoding="utf8")).group(1)
        else:
            try:
                language = locale.getdefaultlocale()[0][:2]
            except:
                language = "en"
    try:
        path = Path(f"{SCRIPT_DIRECTORY}/resources/i18n/messages_{language}.mo")
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

    def __init__(self, language):
        metadata_path = Path(f"{SCRIPT_DIRECTORY}/resources/transformations.json")
        self.metadata = json.loads(metadata_path.read_text(encoding="utf8"))
        index_path = Path(f"{SCRIPT_DIRECTORY}/resources/relation_templates/_index.json")
        template_data = json.loads(index_path.read_text(encoding="utf8"))
        for (stem, d) in template_data.items():
            if f"help_{language}" in d:
                d["help"] = d.pop(f"help_{language}")
                continue
            try:
                d["help"] = d[f"help_en"]
            except KeyError:
                raise MocodoError(22, _("The template '{stem}' doesn't have a help message in language of code '{language}' or 'en'.").format(stem=stem, language=language)) # fmt: skip
        self.metadata.update(template_data)
        self.normalize = invert_dict({k: v["aliases"] for (k, v) in self.metadata.items()})
        self.normalize.update((k, k) for k in self.metadata)
        # recreate the dictionary to have it in alphabetical order
        self.metadata = {k: self.metadata[k] for k in sorted(self.metadata.keys(), key=lambda x: x.lower())}
        self.operations = {"rw": [], "cv": []}
        self.op_tk_rewritings = set(k for (k, v) in self.metadata.items() if v.get("op_tk"))
        self.args_to_delete = ["-t", "-T", "--transform"]
        self.opt_to_restore = " "
    
    def extract_transformation_subargs(self, arg):
        (subopt, __, tail) = arg.partition(":")
        try:
            subopt = self.normalize[subopt.lower()]
        except:
            valid = ", ".join(sorted(self.normalize.keys()))
            raise MocodoError(45, _("The transformation '{subopt}' is not among the possible ones:\n{valid}.").format(subopt=subopt, valid=valid)) # fmt: skip
        result = extract_subargs(f"{subopt}:{tail}")
        category = self.metadata[subopt]["category"]
        self.operations[category].append(result)
        if category == "rw":
            self.args_to_delete.append(arg)
        else:
            self.opt_to_restore = " -t "
        return result


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

def parsed_arguments(args):
    # When mocodo is called from the command line, `args` is just `sys.argv[1:]`.
    # When it is imported, `args` is a list of strings constructed with shlex.split().

    parser = argparse.ArgumentParser(
        prog="mocodo",
        add_help=False,
        formatter_class=ArgumentDefaultsRawDescriptionHelpFormatter,
        allow_abbrev=False,
    )

    mocodo_group = parser.add_argument_group()
    io_group = parser.add_argument_group()
    aspect_group = parser.add_argument_group()

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

    # First, add the arguments that need some preprocessing.
    # The help messages will be added later, after the localization.

    mocodo_group.add_argument("--language",
        metavar="CODE",
        type=str,
    )
    language_action = mocodo_group._group_actions[-1]
    io_group.add_argument("--params_path",
        metavar="PATH",
        default="params.json",
    )
    params_path_action = io_group._group_actions[-1]
    io_group.add_argument("--input", "-i",
        metavar="PATH",
        default=""
    )
    input_action = io_group._group_actions[-1]
    
    (args, remaining_args) = parser.parse_known_args(args)

    if not args.input:
        # no input file is specified, use the pristine sandbox
        source = Path(SCRIPT_DIRECTORY, "resources", "pristine_sandbox.mcd").read_text(encoding="utf8")
        args.input = "sandbox.mcd"
        Path(args.input).write_text(source, encoding="utf8")
    elif not args.input.endswith(".mcd"):
        # the input file has no extension, assume it is a stem
        args.input += ".mcd"
    default_params["input"] = args.input

    if os.path.exists(args.params_path):
        default_params.update(json.loads(Path(args.params_path).read_text(encoding="utf8")))
    if not default_params["input"]:
        default_params["input"] = "sandbox.mcd"
    default_params["language"] = init_localization(default_params.get("language", args.language))
    default_params.setdefault("output_dir", os.path.dirname(default_params["input"]))

    # Add localized messages.

    mocodo_group.title = _("OPTIONS ON MOCODO ITSELF")
    io_group.title = _("INPUT/OUTPUT")
    aspect_group.title = _("ASPECT OF THE GRAPHICAL OUTPUT")

    language_action.help = _("override the automatic localization of the messages with the given language code (e.g., 'fr', 'en', ...)")
    params_path_action.help = _("the path of the parameter file. If omitted, use 'params.json' in the input directory. If non existent, use default parameters.")
    input_action.help = _("the path of the input file. By default, the output files will be generated in the same directory")

    parser.description = re.sub(r"(?m)^(        )", "", _("""
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
    """)) # fmt: skip

    parser.epilog = re.sub(r"(?m)^(        )", "", _("""
        SEE ALSO:
          Online version        https://mocodo.net
          Source code           https://github.com/laowantong/mocodo
          Documentation         https://rawgit.com/laowantong/mocodo/master/doc/fr_refman.html
          Cheat sheet for -t    https://github.com/laowantong/mocodo/blob/master/doc/fr_cheat_sheet.md

        LICENSE:                MIT

        CONTACT:
          Author                Aristide Grange
          Address               Université de Lorraine
                                Laboratoire LCOMS - UFR MIM
                                3 rue Augustin Fresnel
                                57070 METZ Technopôle
                                France
          Mail                  <author.full.name>@univ-lorraine.fr
    """)) # fmt: skip

    transformations = Transformations(default_params["language"])

    mocodo_group.add_argument("--help",
        action="help",
        help=_("show this help message, then exit"),
    )
    mocodo_group.add_argument("--version",
        action="version",
        version="%(prog)s " + version,
        help=_("display the version number, then exit"),
    )
    mocodo_group.add_argument("--restore",
        action="store_true",
        help=_("recreate a pristine version of the files 'sandbox.mcd' and 'params.json' in the input directory, then exit"),
    )

    io_group.add_argument("--lib",
        metavar="URL",
        nargs="?",
        help=_("remote directory to use as fallback when the input file is not found locally"),
    )
    io_group.add_argument("--output_dir",
        metavar="PATH",
        help=_("the directory of the output files"),
    )
    io_group.add_argument("--encodings",
        metavar="STR",
        nargs="*",
        help=_("one or several encodings to be tried successively when reading the input file"),
    )
    io_group.add_argument("--svg_to",
        choices=["png", "pdf"],
        nargs="+",
        default=[],
        help=_("generate a PNG or a PDF version of the SVG output (requires CairoSVG)"),
    )
    io_group.add_argument("--print_params",
        action="store_true",
        help=_("display the contents of the parameter file, then exit"),
    )
    io_group.add_argument("--reuse_geo",
        action="store_true",
        help=_("reuse the geometry file of the previous execution"),
    )
    io_group.add_argument("--uid_suffix",
        metavar="INT",
        type=non_negative_integer,
        default=0,
        help=_("discriminate between multiple SVG of the same interactive diagram"),
    )
    io_group.add_argument("--select",
        choices=["all", "mcd", "rw", "source", "text", "code", "mocodo", "cv", "mld", "ddl", "sql"],
        nargs="*",
        default=argparse.SUPPRESS, # causes no attribute to be added if the argument was not present
        help=_("under Jupyter Notebook, explicitely state the categories of results to display"),
    )
    io_group.add_argument("--defer",
        metavar="STR",
        nargs="*",
        default=argparse.SUPPRESS,
        help=_("use an external web-service to further convert the conversion results into the given graphical formats"),
    )
    io_group.add_argument("--mld",
        action="store_true",
        help=_("backward compatibility alias for '-t' (with no arguments). Same as '-t markdown' but, under Jupyter Notebook, does not prevent the rendering of the conceptual diagram in the cell output"),
    )
    io_group.add_argument("--is_magic",
        action="store_true",
        help=argparse.SUPPRESS, # don't show this argument in the help message
    )
    io_group.add_argument("--transform", "-t",
        metavar="STR",
        nargs="*",
        type=transformations.extract_transformation_subargs,
        default=argparse.SUPPRESS,
        help=_("make a new version of the MCD by applying sequentially the given rewriting operations, and/or convert it into the given formats or languages. Under Jupyter Notebook, '-T' respectively replaces the current cell by the textual result, or copies it into the clipboard (pip3 install pyperclip)"),
    )
    io_group.add_argument("--Transform", "--TRANSFORM", "-T",
        metavar="STR",
        nargs="*",
        type=transformations.extract_transformation_subargs,
        help=argparse.SUPPRESS, # don't show this argument in the help message
    )
    io_group.add_argument("--seed",
        metavar="FLOAT",
        nargs="?",
        type=float,
        help=_("initial value for the random number generator"),
    )
    io_group.add_argument("--title",
        metavar="STR",
        default=_("Untitled"),
        type=str,
        help=_("name of the model, used at various places (file system, database, etc.)"),
    )

    aspect_group.add_argument("--df",
        metavar="STR",
        type=str,
        default="DF",
        help=_("the acronym to be circled in a functional dependency"),
    )
    aspect_group.add_argument("--card_format",
        metavar="STR",
        type=str,
        nargs="?",
        default="{min_card},{max_card}",
        help=_("format string for minimal and maximal cardinalities"),
    )
    aspect_group.add_argument("--fk_format",
        metavar="STR",
        type=str,
        nargs="?",
        default="#{label}",
        help=_("format string for foreign keys in relational diagram"),
    )
    aspect_group.add_argument("--strengthen_card",
        metavar="STR",
        type=str,
        nargs="?",
        default="_1,1_",
        help=_("string for relative cardinalities"),
    )
    aspect_group.add_argument("--flex",
        metavar="FLOAT",
        type=float,
        default=0.75,
        help=_("flex straight legs whose cardinalities may collide"),
    )
    aspect_group.add_argument("--colors",
        metavar="STEM_OR_PATH",
        default="bw",
        help=_("the color palette to use when generating the drawing. Name (without extension) of a file located in the directory 'colors', or path to a personal file"),
    )
    aspect_group.add_argument("--shapes",
        metavar="STEM_OR_PATH",
        help=_("specification of the fonts, dimensions, etc. Name (without extension) of a file located in the directory 'shapes', or path to a personal file"),
    )
    aspect_group.add_argument("--scale",
        metavar="RATE",
        type=scale,
        default=1,
        help=_("scale the diagram by the given factor"),
    )
    aspect_group.add_argument("--adjust_width",
        metavar="RATE",
        type=scale,
        default=1,
        help=_("scale all calculated text widths by the given factor"),
    )
    aspect_group.add_argument("--detect_overlaps",
        action="store_true",
        help=_("raise an error when horizontal or vertical legs overlap"),
    )
    aspect_group.add_argument("--no_assoc_ids",
        action="store_true",
        help=_("forbid the use of identifiers in associations (according to the Merise standard)"),
    )
    aspect_group.add_argument("--gutters",
        metavar="STR",
        nargs="+",
        type=extract_subargs,
        default=argparse.SUPPRESS, 
        help=_("set the visibility and the contents of the lateral gutters"),
    )

    parser.set_defaults(**default_params)
    params = vars(parser.parse_args(remaining_args))
    params["script_directory"] = SCRIPT_DIRECTORY
    params["output_name"] = Path(params["output_dir"]) / Path(params["input"]).stem
    params["rewrite"] = transformations.operations["rw"]
    params["convert"] = transformations.operations["cv"]
    params["args_to_delete"] = transformations.args_to_delete
    params["opt_to_restore"] = transformations.opt_to_restore
    params["op_tk_rewritings"] = transformations.op_tk_rewritings
    params["redirect_output"] = ("-T" in remaining_args or "--Transform" in remaining_args)
    params["keys_to_hide"] = [
        "keys_to_hide",
        "script_directory",
        "output_name",
        "rewrite",
        "convert",
        "args_to_delete",
        "opt_to_restore",
        "op_tk_rewritings",
        "redirect_output",
        "params_path",
        "Transform",
        "is_magic",
        "print_params",
        "reuse_geo",
        "input",
    ]

    lib = "https://mocodo.net/web/lib"
    if params["lib"]:
        parse_url = importlib.import_module("urllib.parse").urlparse
        if parse_url(params["lib"]).scheme:
            lib = params["lib"]
    params["lib"] = lib

    if params["seed"] is not None:
        random.seed(params["seed"])
    
    with contextlib.suppress(UnicodeDecodeError, AttributeError):
        params["title"] = params["title"].decode("utf8")
    
    return params
