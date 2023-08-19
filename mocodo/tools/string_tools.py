import textwrap
import re
from unicodedata import combining, normalize
import base64
import zlib


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

def rstrip_digit(s):
    """
    Get rid of single digit suffix, if any. Works on empty strings too.
    Used for entity and association names.
    """
    return s[:-1] if s[-1:].isdigit() else s

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

# ASCII

LATIN = "ä  æ  ǽ  đ ð ƒ ħ ı ł ø ǿ ö  œ  ß  ŧ ü  Ä  Æ  Ǽ  Đ Ð Ƒ Ħ I Ł Ø Ǿ Ö  Œ  ẞ  Ŧ Ü "
ASCII = "ae ae ae d d f h i l o o oe oe ss t ue AE AE AE D D F H I L O O OE OE SS T UE"


def ascii(s, outliers=str.maketrans(dict(zip(LATIN.split(), ASCII.split())))):
    return "".join(c for c in normalize("NFD", s.translate(outliers)) if not combining(c))


# Camel case

def camel(input_string):
    (head, *words) = re.split(r'[_\W]+', input_string)
    return ''.join([head] + [word.capitalize() for word in words])

# Snake case

def split_camel_case(
        s,
        upper = lambda x: x.upper(),
        lower = lambda x: x.lower(),
    ):
    change_case = upper if s.isupper() else lower
    result = []
    previous_is_lower = False
    for c in s:
        if previous_is_lower and c.isupper():
            result.extend(["_", change_case(c)])
        elif not c.isalnum():
            result.append("_")
        else:
            result.append(change_case(c))
        previous_is_lower = c.islower()
    return "".join(result)

def compress_underscores(s):
    return re.sub(r"_+", "_", s.strip("_"))

def snake(label):
    return compress_underscores(split_camel_case(label))

def urlsafe_encoding(text):
    return base64.urlsafe_b64encode(zlib.compress(text.encode('utf-8'), 9)).decode('ascii')