"""
Associate common field names (expressed as regular expressions) to data types.

Suppose that the field names have been preprocessed to consist of space separated
words. Use only SQL:2016 standard data types, namely: CHAR, VARCHAR, CLOB, BINARY,
VARBINARY, BLOB, NUMERIC, DECIMAL, SMALLINT, INTEGER, BIGINT, FLOAT, REAL, DOUBLE
PRECISION, DATE, TIME, TIMESTAMP, INTERVAL, BOOLEAN, XML, JSON.

If mandatory, the data types must be followed by a size specification, e.g.
VARCHAR(255) or DECIMAL(11,2). Do not add column properties such as UNSIGNED since
they are not supported by all DBMS.
"""

# TODO: check https://www.google.com/search?rls=en&q=site%3Alegifrance.gouv.fr+varchar&ie=UTF-8&oe=UTF-8

import re

from ..parse_mcd import Visitor, Token
from ..tools.parser_tools import first_child, parse_source, reconstruct_source
from ..tools.string_tools import ascii, snake

class CreateTypePlaceholder(Visitor):

    def typed_attr(self, tree):
        if first_child(tree, "data_type"):
            return
        name_token = first_child(tree, "attr")
        if not name_token:
            return
        name_token.value += " []"

def create_type_placeholders(source):
    visitor = CreateTypePlaceholder()
    tree = parse_source(source)
    visitor.visit(tree)
    return reconstruct_source(tree)


FIELD_TYPES = {
    "en": {
        # Date and Time
        r"\bdate$": "DATE",
        r"\btime$": "TIME",
        r"\bdatetime$": "DATETIME",
        r"\btimestamp$": "TIMESTAMP",
        r"\bat$": "TIMESTAMP",
        # Identifying and Validating Information
        r"\bid$": "VARCHAR(8)",
        r"\bcode$": "VARCHAR(8)",
        r"\bref$": "VARCHAR(8)",
        r"\bnum$": "VARCHAR(8)",
        r"\buuid$": "VARCHAR(36)",
        r"\bsalt$": "BINARY(16)",
        r"\bhash$": "BINARY(64)",
        r"\btoken$": "VARCHAR(255)",
        r"\bpassword$": "VARCHAR(255)",
        r"\bpwd$": "VARCHAR(255)",
        r"\bdigest$": "BINARY(64)",
        r"\bsignature$": "BINARY(64)",
        # Internet and Computers
        r"\burl$": "VARCHAR(2000)",
        r"\bip$": "VARCHAR(15)",
        r"\bipv4$": "VARCHAR(15)",
        r"\bipv6$": "VARCHAR(45)",
        r"\bcookie$": "VARCHAR(255)",
        r"\bsession$": "VARCHAR(255)",
        r"\bmd5$": "BINARY(16)",
        r"\bpath$": "VARCHAR(255)",
        r"\bstatus$": "VARCHAR(20)",
        r"\bpriority$": "SMALLINT",
        r"\bversion$": "VARCHAR(10)",
        # Personal information
        r"\bname$": "VARCHAR(255)",
        r"\bsex$": "CHAR(1)",
        r"\bgender$": "VARCHAR(10)",
        r"\bage$": "SMALLINT",
        # Addressing
        r"\bpost code$": "VARCHAR(20)",
        r"\bzip code$": "VARCHAR(20)",
        r"\bphone number$": "VARCHAR(20)",
        r"\bphone$": "VARCHAR(20)",
        r"\bfax number$": "VARCHAR(20)",
        r"\bfax$": "VARCHAR(20)",
        r"\bemail$": "VARCHAR(255)",
        r"\bcountry name$": "VARCHAR(100)",
        r"\bcity name$": "VARCHAR(100)",
        r"\bcountry code$": "CHAR(2)",
        # Financial
        r"\bprice$": "DECIMAL(10,2)",
        r"\bamount$": "DECIMAL(10,2)",
        # Predicate
        r"^is\b": "BOOLEAN",
        r"^has\b": "BOOLEAN",
        r"^does\b": "BOOLEAN",
        r"^can\b": "BOOLEAN",
        r"\bflag$": "BOOLEAN",
        # Text
        r"\btag$": "VARCHAR(50)",
        r"\blabel$": "VARCHAR(50)",
        r"\bbody$": "TEXT",
        r"\bcomment$": "TEXT",
        r"\bdescription$": "TEXT",
        r"\bnote$": "TEXT",
        r"\bmessage$": "TEXT",
        r"\bcontent$": "TEXT",
        r"\binfo(rmation)?s?$": "JSON",
        # Geographical
        r"\blat(itude)?$": "DECIMAL(9,6)",
        r"\blon(gitude)?$": "DECIMAL(9,6)",
        r"\bpos(ition)?$": "POINT",
        # Grading
        r"\bstars$": "DECIMAL(3,2)",
        r"\brating$": "DECIMAL(3,2)",
        r"\brating$": "DECIMAL(3,2)",
        r"\bgrade$": "DECIMAL(3,2)",
        # Quantity
        r"\bquantity$": "INTEGER",
        r"\bpercent(age)?$": "DECIMAL(5,2)",
        r"\bratio$": "DECIMAL(5,2)",
        r"\bweight$": "DECIMAL(10,2)",
        r"\bsize$": "VARCHAR(20)",
        r"\blength$": "DECIMAL(10,2)",
        r"\bwidth$": "DECIMAL(10,2)",
        r"\bheight$": "DECIMAL(10,2)",
        r"\bvolume$": "DECIMAL(10,2)",
        r"\btemperature$": "DECIMAL(5,1)",
        r"\bhumidity$": "DECIMAL(5,2)",
        r"\bcolor$": "VARCHAR(50)",
        # Blobs
        r"\bimage$": "BLOB",
        r"\bpicture$": "BLOB",
        r"\bphoto$": "BLOB",
        r"\blogo$": "BLOB",
        r"\bicon$": "BLOB",
        r"\bfile$": "BLOB",
        r"\bvideo$": "BLOB",
        r"\baudio$": "BLOB",
        r"\bbinary$": "BLOB",
        r"\bblob$": "BLOB",
    },
    "fr": {
        # Date and Time
        r"^date\b": "DATE",
        r"^heure\b": "TIME",
        r"^date et heure\b": "DATETIME",
        r"^horodatage\b": "TIMESTAMP",
        r"\ba$": "TIMESTAMP",
        # Identifying and Validating Information
        r"^id\b": "VARCHAR(8)",
        r"^code\b": "VARCHAR(8)",
        r"^ref\b": "VARCHAR(8)",
        r"^num\b": "VARCHAR(8)",
        r"^uuid\b": "VARCHAR(36)",
        r"^sel\b": "BINARY(16)",
        r"^empreinte\b": "BINARY(64)",
        r"^token\b": "VARCHAR(255)",
        r"^passe\b": "VARCHAR(255)",
        r"^pwd\b": "VARCHAR(255)",
        r"^digest\b": "BINARY(64)",
        r"^signature\b": "BINARY(64)",
        r"\bsire(t|n)\b": "CHAR(14)",
        # Internet and Computers
        r"^url\b": "VARCHAR(2000)",
        r"^ip\b": "VARCHAR(15)",
        r"^ipv4\b": "VARCHAR(15)",
        r"^ipv6\b": "VARCHAR(45)",
        r"^cookie\b": "VARCHAR(255)",
        r"^session\b": "VARCHAR(255)",
        r"^md5\b": "BINARY(16)",
        r"^chemin\b": "VARCHAR(255)",
        r"^statut\b": "VARCHAR(20)",
        r"^priorite\b": "SMALLINT",
        r"^version\b": "VARCHAR(10)",
        # Personal information
        r"^(pre)?nom\b": "VARCHAR(255)",
        r"^sexe\b": "CHAR(1)",
        r"^genre\b": "VARCHAR(10)",
        r"^age\b": "SMALLINT",
        r"^nir\b": "VARCHAR(15)",
        r"^ss\b": "VARCHAR(15)",
        r"\bsecu(rite sociale)?\b": "VARCHAR(15)",
        # Addressing
        r"^code postal\b": "VARCHAR(20)",
        r"^tel(ephone)?\b": "VARCHAR(20)",
        r"^fax\b": "VARCHAR(20)",
        r"^e?mail\b": "VARCHAR(255)",
        r"^(nom )?pays\b": "VARCHAR(100)",
        r"^(nom )?ville\b": "VARCHAR(100)",
        r"^code pays\b": "CHAR(2)",
        # Financial
        r"^prix\b": "DECIMAL(10,2)",
        r"^montant\b": "DECIMAL(10,2)",
        # Predicate
        r"^est\b": "BOOLEAN",
        r"^a\b": "BOOLEAN",
        r"^peut\b": "BOOLEAN",
        r"^drapeau\b": "BOOLEAN",
        # Text
        r"^mot clef?\b": "VARCHAR(50)",
        r"\blibelle$": "VARCHAR(50)",
        r"^corps\b": "TEXT",
        r"^commentaire\b": "TEXT",
        r"^desc(r?(iption)?)\b": "TEXT",
        r"^descriptif\b": "TEXT",
        r"^notes?\b": "TEXT",
        r"^message\b": "TEXT",
        r"^avis\b": "TEXT",
        r"^contenu\b": "TEXT",
        r"\binfo(rmation)?s?\b": "JSON",
        # Geographical
        r"^lat(itude)?\b": "DECIMAL(9,6)",
        r"^lon(gitude)?\b": "DECIMAL(9,6)",
        r"^pos(ition)?\b": "POINT",
        # Grading
        r"\bétoiles$": "DECIMAL(3,2)",
        # Quantity
        r"^(quantite|qte)\b": "INTEGER",
        r"^(nombre|nb)\b": "INTEGER",
        r"^pourcent(age)?\b": "DECIMAL(5,2)",
        r"^ratio\b": "DECIMAL(5,2)",
        r"^poids\b": "DECIMAL(10,2)",
        r"^taille\b": "VARCHAR(20)",
        r"^longueur\b": "DECIMAL(10,2)",
        r"^largeur\b": "DECIMAL(10,2)",
        r"^hauteur\b": "DECIMAL(10,2)",
        r"^vol(ume)?\b": "DECIMAL(10,2)",
        r"^temp(erature)?\b": "DECIMAL(5,1)",
        r"^humidite\b": "DECIMAL(5,2)",
        r"^couleur\b": "VARCHAR(50)",
        # Blobs
        r"^image\b": "BLOB",
        r"^photo\b": "BLOB",
        r"^logo\b": "BLOB",
        r"^icone\b": "BLOB",
        r"^fichier\b": "BLOB",
        r"^video\b": "BLOB",
        r"^audio\b": "BLOB",
        r"^binaire\b": "BLOB",
        r"^blob\b": "BLOB",
    },
}


class GuessType(Visitor):

    def __init__(self, guessing_suffix, params):
        # Example: -r types:guess=? will complete all guessed types with a question mark.
        self.field_types = FIELD_TYPES["en"] # English is always used as fallback
        language = params.get("language", "en")
        if language != "en":
            self.field_types.update(FIELD_TYPES[language])
        # Convert the dict to a list of tuples, and sort them by decreasing length
        # so that the longest match is found first.
        self.field_types = sorted(self.field_types.items(), key=lambda x: -len(x[0]))
        # Precompile the regexes
        self.field_types = [(re.compile(k).search, v) for (k, v) in self.field_types]
        self.guessing_suffix = guessing_suffix

    def typed_attr(self, tree):
        a = list(tree.find_data("data_type"))
        if a and "".join(a[0].children)[2:-1]:
            return # already typed
        attr = first_child(tree, "attr")
        if attr == "":
            return
        needle = snake(ascii(attr)).replace("_", " ").lower()
        for (found, data_type) in self.field_types:
            if found(needle):
                data_type = f"{data_type}{self.guessing_suffix}"
                break
        else:
            data_type = ""
        tree.children = [Token("MOCK", f"{attr.value} [{data_type}]", line=attr.line, column=attr.column)]


def guess_types(source, subsubarg, params):
    visitor = GuessType(subsubarg, params)
    tree = parse_source(source)
    visitor.visit(tree)
    return reconstruct_source(tree)
