import argparse
import gettext
import json
import locale
import os
import random
import re
import shutil
import sys
from pathlib import Path

from mocodo.tools.string_tools import strip_surrounds, TRUNCATE_DEFAULT_SIZE
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
            language = re.search(r"\W*(\w+)", Path("/tmp/languages.txt").read_text()).group(1)
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
        self.metadata = {
            "arrange": {
                "category": "rw",
                "help": _("rearrange the layout with either a Branch & Bound or a Genetic Algorithm"),
                "fr_examples": {
                    "arrange": "B&B sans contraintes",
                    "arrange:timeout=60": "B&B limité à une minute",
                    "arrange:wide": "B&B privilégiant la largeur",
                    "arrange:current": "B&B sur la grille courante",
                    "arrange:balanced=0": "B&B sur la plus petite grille équilibrée",
                    "arrange:balanced=1": "B&B sur la seconde plus petite grille équilibrée",
                    "arrange:algo=ga": "algorithme génétique",
                },
                "aliases": [],
            },
            "ascii": {
                "category": "rw",
                "help": _("rewrite the given elements in ASCII"),
                "fr_examples": {
                    "ascii:roles,labels": "rôles, libellés des boîtes et des attributs en ASCII",
                },
                "aliases": [],
                "op_tk": True,
            },
            "ast": {
                "category": "cv",
                "help": _("dump the abstract syntax tree of the source text (for debugging purposes)"),
                "aliases": []
            },
            "camel": {
                "category": "rw",
                "help": _("rewrite the given elements in camelCase"),
                "aliases": ["camelcase", "camel_case"],
                "op_tk": True,
            },
            "capitalize": {
                "category": "rw",
                "help": _("rewrite the given elements by capitalizing the first letter of each word"),
                "aliases": [],
                "op_tk": True,
            },
            "casefold": {
                "category": "rw",
                "help": _("rewrite the given elements in lowercase, but more aggressively than 'lower'"),
                "aliases": ["case_fold"],
                "op_tk": True,
            },
            "chen": {
                "category": "cv",
                "help": _("convert the conceptual model into a Chen's ERD"),
                "fr_examples": {
                    "chen": "sans attributs",
                    "chen:attrs": "avec attributs",
                    "chen:attrs --defer": "calcule le rendu graphique via un service web",
                    "chen:layout=circo,mindist=2,scale=0.6": "ajoute des options arbitraires pour Graphviz",
                },
                "aliases": [],
            },
            "create": {
                "category": "rw",
                "help": _("try to infer types, entities, CIFs or DF arrows from the existing elements"),
                "fr_examples": {
                    "guess:types": "deviner les types manquants",
                    "create:types=": "remplacer les types manquants par `[]`",
                    "create:types=TODO": "remplacer les types manquants par `[TODO]`",
                    "make:entities": "réparer l'oubli d'entités référencées dans des associations",
                    "create:dfs": "mettre des DF partout où c'est possible",
                    "add:df_arrows": "ajouter des flèches aux DF",
                    "add:cifs": "ajouter les CIF correspondant aux agrégats",
                    "add:cifs=light": "même chose en visualisation allégée",
                    "add:roles": "mettre comme rôles le nom des associations partout où c'est utile",
                },
                "aliases": ["add", "insert", "make", "guess", "infer", "complete", "new"],
                "op_tk": True,
            },
            "crow": {
                "category": "cv",
                "help": _("convert the conceptual model into a crow's foot ERD"),
                "fr_examples": {
                    "crow": "format Graphviz",
                    "crow --defer": "calcule le rendu graphique via un service web",
                    "crow:mmd": "format Mermaid",
                    "crow:mermaid": "idem",
                },
                "aliases": ["crowfoot", "crowsfoot"],
            },
            "data_dict": {
                "category": "cv",
                "help": _("collect all the attributes of the MCD in a table"),
                "aliases": ["data_dictionary"],
                "fr_examples": {
                    "data_dict": "tableau Markdown, trois colonnes",
                    "data_dict:label": "liste Markdown, une colonne",
                    'data_dict:label,type="Description"': "deux colonnes, un libellé personnalisé",
                    'data_dict:label="Attribut",type="Description"': "deux colonnes, deux libellés personnalisés",
                    'data_dict:**box**="Entité ou<br>association",label,`type`=`"Type de données"`': "mise en forme de certains libellés",
                    "data_dict:tsv": "tableau TSV, trois colonnes",
                    "data_dict:tsv,label": "liste des attributs séparés par des retours à la ligne",
                },
            },
            "delete": {
                "category": "rw",
                "help": _("suppress the given elements whenever possible"),
                "fr_examples": {
                    "empty": "ne garde que la structure et le nom des boîtes",
                    "delete:types,notes,attrs,cards": "idem",
                    "delete:cards": "remplace les cardinalités par `XX`",
                    "delete:card_prefixes": "supprime les marqueurs d'entités faibles et d'agrégats",
                    "delete:dfs": "supprime les entités indépendantes dont tous les attributs sont identifiants (et les DF qui les relient)",
                },
                "aliases": ["del", "suppress", "erase", "remove", "hide", "empty"],
                "op_tk": True,
            },
            "drain": {
                "category": "rw",
                "help": _("move any (1,1) association attribute to the appropriate entity"),
                "aliases": [],
            },
            "drown": {
                "category": "rw",
                "help": _("replace all element names by a numbered generic label"),
                "aliases": ["drown_by_numbers", "anonymize", "anonymise"],
            },
            "echo": {
                "category": "rw",
                "help": _("rewrite the source text as is"),
                "aliases": [], 
            },
            "explode": {
                "category": "rw",
                "help": _("decompose any n-ary (*,N) associations into n binary ones"),
                "fr_examples": {
                    "explode arrange": "décomposer les non-DF ternaires et plus, puis réarranger",
                    "explode:arity=3 arrange": "idem",
                    "explode:weak arrange": "idem, avec création d'entités faibles",
                    "explode:arity=2.5 arrange": "étendre aux non-DF binaires porteuses d'attributs",
                    "explode:arity=2 arrange": "étendre à toutes les non-DF binaires",
                },
                "aliases": [],
            },
            "fix": {
                "category": "rw",
                "help": _("try to fix common errors in the given elements"),
                "fr_examples": {
                    "fix:cards": "normaliser les cardinalités en 01, 11, 0N et 1N",
                },
                "aliases": [],
                "op_tk": True,
            },
            "flip": {
                "category": "rw",
                "help": _("apply a vertical, horizontal or diagonal symmetry to the diagram"),
                "fr_examples": {
                    "flip:v": "symétrie verticale",
                    "flip:h": "symétrie horizontale",
                    "flip:d": "symétrie selon la seconde diagonale",
                    "flip:vhd": "symétrie selon la première diagonale",
                    "flip:dhv": "idem (ordre indifférent)",
                },
                "aliases": ["mirror", "reflect"],
            },
            "grow": {
                "category": "rw",
                "help": _("add random entities and associations (default: 10 new associations)"),
                "fr_examples": {
                    'grow arrange': "ajouter des éléments avec les paramètres par défaut, puis réarranger",
                    'grow:n=10': "nombre total d'associations à ajouter (défaut)",
                    'grow:arity_1=2': "nombre d'associations réflexives (défaut)",
                    'grow:arity_3=2': "nombre d'associations ternaires (défaut)",
                    'grow:arity_4=0': "nombre d'associations quaternaires (défaut)",
                    'grow:doubles=1': "nombre d'associations liant deux mêmes entités (défaut)",
                    'grow:composite_ids=1': "nombre d'identifiants composites (défaut)",
                    'grow:ent_attrs=4': "nombre maximal d'attributs par entité (défaut)",
                    'grow:assoc_attrs=2': "nombre maximal d'attributs par association (défaut)",
                    'grow:"*1-*N"=3': "nombre d'associations `*1-*N` (défaut)",
                    'grow:"01-11"=1': "nombre d'associations `01-11` (défaut)",
                    'grow:"_11-*N"=1': "une entité faible (zéro par défaut)",
                    'grow:"/1N-*N"=1': "un agrégat (zéro par défaut)",
                    'grow:from_scratch arrange': "à partir d'un MCD vide",
                    'grow:from_scratch,arity_3=1 obfuscate create:roles lower:roles arrange': "créer un MCD d'entraînement à la conversion en relationnel",
                },
                "aliases": []
            },
            "lower": {
                "category": "rw",
                "help": _("rewrite the given elements in lowercase"),
                "fr_examples": {
                    "lower:attrs,roles": "attributs et rôles en minuscules",
                },
                "aliases": ["lowercase", "lower_case"],
                "op_tk": True,
            },
            "prefix": {
                "category": "rw",
                "help": _("prefix the given elements with the given string"),
                "fr_examples": {
                    'prefix:roles="-"': "force les rôles à remplacer le nom des clés étrangères lors du passage au relationnel",
                },
                "aliases": ["prepend"],
                "op_tk": True,
            },
            "randomize": {
                "category": "rw",
                "help": _("keep the stucture, but replace the given elements with random ones whenever possible"),
                "fr_examples": {
                    "obfuscate": "libellés remplacés par du Lorem Ipsum",
                    "obfuscate:labels=lorem": "idem",
                    "obfuscate:labels=disparition": "idem, lexique du roman de Perec",
                    "obfuscate:labels=en4": "idem, mots anglais de 4 lettres (SFW)",
                    "obfuscate:attrs=fr,boxes=fr5": "idem, mots français de longueur quelconque pour les attributs, de 5 lettres pour les boîtes",
                    "randomize:types": "types randomisés avec les fréquences de `default_datatypes_fr.tsv`.",
                },
                "aliases": ["rand", "random", "randomise", "obfuscate", "obscure"],
                "op_tk": True,
            },
            "relation": {
                "category": "cv",
                "help": _("convert the conceptual model into a relational schema with the given template path"),
                "fr_examples": {
                    'relation:path/to/my_template.yaml': "chemin relatif, extension obligatoire",
                },
                "aliases": ["template", "relation_template"]
            },
            "replace": {
                "category": "rw",
                "help": _("rewrite the given elements by applying the given 'search/repl' pattern"),
                "fr_examples": {
                    'replace:boxes="DIRIGER/RÉPONDRE DE"': "renomme une boîte",
                    'replace:texts="personel/personnel"': "corrige une faute d'orthographe",
                    'replace:replace:texts="_/ "': "remplace les tirets bas par des espaces",
                    'replace:types="VARCHAR/VARCHAR2"': "modifie un nom de type",
                    'replace:cards=0N/1N': "remplace toutes les cardinalités 0N par 1N",
                    'replace:cards=1N//1N': "ajout des marqueurs d'agrégats",
                    'replace:cards="0/X" replace:cards="11/X1" replace:cards="1N/XN"': "masque les cardinalités minimales",
                    'replace:cards=1N//1N': "crée des agrégats un peu partout",
                    'delete:card_prefixes replace:cards=11/_11': "ajoute des marqueurs d'entités faibles",
                },
                "aliases": ["substitute", "sub", "repl"],
                "op_tk": True,
            },
            "slice": {
                "category": "rw",
                "help": _("rewrite the given elements by keeping only a given slice"),
                "fr_examples": {
                    "slice:boxes=5:10": "de l'indice 5 (inclus) à l'indice 10 (exclu)",
                    "slice:boxes=5:": "supprime les 5 premiers caractères",
                    "slice:boxes=:5": "ne garde que les 5 premiers caractères",
                    "slice:boxes=:-5": "supprime les 5 derniers caractères",
                    "slice:boxes=:": "équivalent de `echo`",
                    "slice:boxes=": "idem",
                    "slice:boxes": "idem",
                },
                "aliases": ["cut", "interval"],
                "op_tk": True,
            },
            "snake": {
                "category": "rw",
                "help": _("rewrite the given elements in snake_case"),
                "aliases": ["snakecase", "snake_case"],
                "op_tk": True,
            },
            "split": {
                "category": "rw",
                "help": _("decompose any n-ary (*,1) associations into n-1 binary ones"),
                "fr_examples": {
                    "split arrange": "décomposer, puis réarranger",
                },
                "aliases": [],
            },
            "suffix": {
                "category": "rw",
                "help": _("suffix the given elements with the given string"),
                "fr_examples": {
                    "suffix:boxes=1": "Ajoute un suffixe numérique au nom des boîtes en vue de mettre un MCD et sa copie sur le même diagramme.",
                },
                "aliases": ["append"],
                "op_tk": True,
            },
            "swapcase": {
                "category": "rw",
                "help": _("rewrite the given elements by swapping the case of each letter"),
                "aliases": ["swap_case"],
                "op_tk": True,
            },
            "title": {
                "category": "rw",
                "help": _("rewrite the given elements in Title Case"),
                "aliases": ["titlecase", "title_case"],
                "op_tk": True,
            },
            "truncate": {
                "category": "rw",
                "help": _("truncate the given elements to the given length (default: {n})").format(n=TRUNCATE_DEFAULT_SIZE),
                "fr_examples": {
                    "truncate:boxes=10": "tronque les noms des boîtes à 10 caractères",
                },
                "aliases": ["trunc", "shorten"],
                "op_tk": True,
            },
            "uml": {
                "category": "cv",
                "help": _("convert the conceptual model into a UML class diagram"),
                "fr_examples": {
                    "uml": "format PlantUML",
                    "uml:plantuml": "idem",
                    "uml --defer": "calcule le rendu graphique via un service web",
                    "uml:plantuml=-": "supprime les styles par défaut",
                    'uml:plantuml="skinparam backgroundColor yellow\nskinparam classAttributeFontName Arial\n"': "ajoute des styles personnalisés",
                },
                "aliases": ["uml", "class_diagram"],
            },
            "share": {
                "category": "cv",
                "help": _("encode the MCD into a URL for Mocodo online"),
                "fr_examples": {
                    "qr --defer": "génère un QR code via un service web",
                },
                "aliases": ["url", "link", "qr", "qr_code"],
            },
            "upper": {
                "category": "rw",
                "help": _("rewrite the given elements in UPPERCASE"),
                "fr_examples": {
                    "upper:boxes": "noms des boîtes en majuscules",
                },
                "aliases": ["uppercase", "upper_case"],
                "op_tk": True,
            },
        }

        index_path = Path(f"{SCRIPT_DIRECTORY}/resources/relation_templates/_index.json")
        template_data = json.loads(index_path.read_text())
        for (stem, d) in template_data.items():
            try:
                d["help"] = d.pop(f"help_{language}")
            except KeyError:
                raise MocodoError(22, _("The template '{stem}' doesn't have a help message in language of code '{language}'.").format(stem=stem, language=language)) # fmt: skip
        self.metadata.update(template_data)
        self.normalize = invert_dict({k: v["aliases"] for (k, v) in self.metadata.items()})
        self.normalize.update((k, k) for k in self.metadata)
        # recreate the dictionary to have it in alphabetical order
        self.metadata = {k: self.metadata[k] for k in sorted(self.metadata.keys(), key=lambda x: x.lower())}
        self.operations = {"rw": [], "cv": []}
        self.op_tk_rewritings = set(k for (k, v) in self.metadata.items() if v.get("op_tk"))
        self.args_to_delete = ["-t", "-T", "--transform"]
        self.opt_to_restore = " "
    
    def extract_subargs(self, arg):
        (subopt, __, tail) = arg.partition(":")
        try:
            subopt = self.normalize[subopt.lower()]
        except:
            valid = ", ".join(sorted(self.normalize.keys()))
            raise MocodoError(45, _("The transformation '{subopt}' is not among the possible ones:\n{valid}.").format(subopt=subopt, valid=valid)) # fmt: skip
        result = extract_subargs(f"{subopt}:{tail}") # NB: calls the global function, not the method
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

def parsed_arguments():

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
    )
    input_action = io_group._group_actions[-1]
    
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
          Cheat sheet for -t    https://github.com/laowantong/mocodo/master/doc/fr_cheat_sheet.md

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
        choices=["*", "mcd", "rw", "source", "text", "code", "mocodo", "cv", "mld", "ddl", "sql"],
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
        type=transformations.extract_subargs,
        default=argparse.SUPPRESS,
        help=_("make a new version of the MCD by applying sequentially the given rewriting operations, and/or convert it into the given formats or languages. Under Jupyter Notebook, '-T' respectively replaces the current cell by the textual result, or copies it into the clipboard (pip3 install pyperclip)"),
    )
    io_group.add_argument("--Transform", "--TRANSFORM", "-T",
        metavar="STR",
        nargs="*",
        type=transformations.extract_subargs,
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
    params["keys_to_hide"] = ["keys_to_hide", "params_path", "script_directory", "output_name", "rewrite", "convert", "redirect_output"]

    if not os.path.exists(params["input"]):
        path = Path(SCRIPT_DIRECTORY, "resources", "pristine_sandbox.mcd")
        shutil.copyfile(path, params["input"])
    if params["seed"] is not None:
        random.seed(params["seed"])
    try:
        params["title"] = params["title"].decode("utf8")
    except:
        pass
    return params
