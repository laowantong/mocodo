import textwrap
import re
from unicodedata import combining, normalize
import base64
import zlib

TRUNCATE_DEFAULT_SIZE = 64

def wrap_label(s, wrapping_ratio=2):
    """
    Break a given short string into a list of lines, trying to keep the
    width/height ratio just above wrapping_ratio.
    """
    min_width = max(map(len, re.split(r"[-\s]+", s)))
    for width in range(min_width, len(s)):
        lines = textwrap.wrap(s, width=width)
        if max(map(len, lines)) / len(lines) > wrapping_ratio:
            return lines
    return [s]

def rstrip_digit_or_underline(s):
    """
    Get rid of single digit suffix, if any. Works on empty strings too.
    Used for entity and association raw names.
    """
    return s[:-1] if s[-1:].isdigit() or s[-1:] == "_" else s

def surrounds(s, ends):
    """
    Check if s is surrounded by the first and last characters of ends.
    Works on empty strings too.
    """
    return s[:1] == ends[:1] and s[-1:] == ends[-1:]

def strip_surrounds(s, ends):
    """
    Remove the first and last characters of s if they match the first and last
    characters of ends. Works on empty strings too.
    """
    return s[1:-1] if surrounds(s, ends) else s

def is_a_description(note):
    if not note:
        return False
    if note.startswith(("+", "-")):
        return False
    return " " in note

# ASCII

LATIN = "ä  æ  ǽ  đ ð ƒ ħ ı ł ø ǿ ö  œ  ß  ŧ ü  Ä  Æ  Ǽ  Đ Ð Ƒ Ħ I Ł Ø Ǿ Ö  Œ  ẞ  Ŧ Ü "
ASCII = "ae ae ae d d f h i l o o oe oe ss t ue AE AE AE D D F H I L O O OE OE SS T UE"


def ascii(s, outliers=str.maketrans(dict(zip(LATIN.split(), ASCII.split())))):
    return "".join(c for c in normalize("NFD", s.translate(outliers)) if not combining(c))

def raw_to_bid(box_raw_name):
    return re.sub(r"\W", "_", ascii(box_raw_name).upper())

def aggressive_split(
    input_string,
    find_all_words = re.compile(r"(?u)[^\W_]+").findall
):
    # Split the string, and further split the words
    result = []
    for word in find_all_words(input_string):
        previous_is_digit = word[0].isdigit()
        previous_is_lower = word[0].islower()
        i = 0
        for (j, c) in enumerate(word[1:], 1):
            current_is_lower = c.islower()
            current_is_digit = c.isdigit()
            if (
                previous_is_digit and not current_is_digit
                or
                not previous_is_digit and current_is_digit
                or
                previous_is_lower and not current_is_lower
            ):
                result.append(word[i:j])
                i = j
            previous_is_lower = current_is_lower
            previous_is_digit = current_is_digit
        result.append(word[i:])
    return result

# A decorator which calls

def spare_protected_suffix(
    function,
    is_protected_suffix = re.compile(r"[_0-9]").match,
):
    def wrapper(input_string):
        suffix = input_string[-1:]
        if is_protected_suffix(suffix):
            input_string = input_string[:-1]
        else:
            suffix = ""
        result = function(input_string)
        return result + suffix
    return wrapper

@spare_protected_suffix
def camel(input_string):
    result = "".join([word.capitalize() for word in aggressive_split(input_string)])
    return result[:1].lower() + result[1:]

@spare_protected_suffix
def pascal(input_string):
    return "".join([word.capitalize() for word in aggressive_split(input_string)])

@spare_protected_suffix
def snake(input_string):
    return "_".join([word for word in aggressive_split(input_string)])

def urlsafe_encoding(text):
    return base64.urlsafe_b64encode(zlib.compress(text.encode('utf-8'), 9)).decode('ascii')

# Markdown

def markdown_table(rows, formats=None):
    """
    Return a Markdown table from a list of rows, each row being a tuple.
    The first row is the header. For maximum readability, in text mode, each column
    is filled with spaces so that the longest cell fits in the column.
    'formats' is a sequence of formatting symbols "l", "c", "r".
    """
    rows = [list(map(str, row)) for row in rows]
    widths = [max(map(len, column)) for column in zip(*rows)]
    result = ["| " + " | ".join(f"{c:<{w}}" for (w, c) in zip(widths, row)) + " |" for row in rows]
    formats = formats or "l" * len(rows[0])
    formats = [("-" if x == "r" else ":") + "-" * w + ("-" if x == "l" else ":") for (w, x) in zip(widths, formats)]
    result[1:1] = ["|" + "|".join(formats) + "|"]
    return "\n".join(result)
