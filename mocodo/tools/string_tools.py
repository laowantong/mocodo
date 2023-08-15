import textwrap
import re

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

def surrounds(ends, s):
    """
    Check if s is surrounded by the first and last characters of ends.
    Works on empty strings too.
    """
    return s[:1] == ends[:1] and s[-1:] == ends[-1:]