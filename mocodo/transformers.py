__import__("sys").path[0:0] = ["."]
from pprint import pprint
import random
import re
from pathlib import Path
import json

from .damerau_levenshtein import distance
from .mocodo_error import MocodoError
from .parse_mcd import Transformer, Visitor
from .parser_tools import transform_source, parse_source


def random_words_of(lorem_text, obfuscation_min_distance, seed=None):
    """Generate random words from a given text.

    Args:
        lorem_text (str): The text to generate random words from.
        obfuscation_min_distance (int): The minimum distance between two words.

    Yields:
        str: A random word from the text, guaranteed to be at least
            `obfuscation_min_distance` apart from the previous ones.

    Raises:
        StopIteration: If there are not enough words in the text to satisfy the
            `obfuscation_min_distance` constraint.
    """
    words = list(dict.fromkeys(word.lower() for word in re.findall(r"(?u)[^\W\d_]{3,}", lorem_text)))  # use dict.fromkeys instead of set for preserving order
    if seed is not None:
        random.seed(seed)
    random.shuffle(words)
    previous_words = set()
    for word in words:
        for previous_word in previous_words:
            if distance(word, previous_word) < obfuscation_min_distance:
                # Keeping this word would be too confusing, let's try the next one.
                break
        else:
            yield word
            previous_words.add(word)


class Obfuscator(Transformer):
    def __init__(self, params):
        lorem_filename = params["obfuscate"] or ""
        try:
            self.lorem_path = Path(lorem_filename)
            lorem_text = self.lorem_path.read_text()
        except IOError:
            lorem_dir = Path(params["script_directory"]) / "resources" / "lorem"
            if lorem_filename.endswith(".txt"):
                lorem_filename = lorem_filename[:-4]
            self.lorem_path = lorem_dir / f"{lorem_filename}.txt"
            try:
                lorem_text = self.lorem_path.read_text()
            except IOError:
                self.lorem_path = lorem_dir / "lorem_ipsum.txt"
                lorem_text = self.lorem_path.read_text()
        self.random_word = random_words_of(lorem_text, params["obfuscation_min_distance"], params["seed"])
        box_cache = {}
        self.box_name = lambda tree: self.obfuscate_name(box_cache, tree)
        attr_cache = {}
        self.attr = lambda tree: self.obfuscate_name(attr_cache, tree)

    def obfuscate_name(self, cache, tree):
        name = tree[0].value
        suffix = ""
        if name[-1].isdigit():
            suffix = name[-1]
            name = name[:-1]
        if name not in cache:
            try:
                new_name = next(self.random_word)
            except StopIteration:
                raise MocodoError(12, _('Obfuscation failed. Not enough substitution words in "{filename}". You may decrease the `obfuscation_min_distance` option values.').format(filename=self.lorem_path), filename=self.lorem_path, obfuscation_min_distance=params["obfuscation_min_distance"])  # fmt: skip
            if name.isupper():
                new_name = new_name.upper()
            elif name.islower():
                new_name = new_name.lower()
            elif name.istitle():
                new_name = new_name.capitalize()
            cache[name] = new_name + suffix
        return tree[0].update(value=cache[name])


def obfuscate(source, params, seed=None):
    return transform_source(source, Obfuscator(params))


class CardinalityFixer(Transformer):

    def __init__(self):
        self.fixes = {
            "01": ["O1", "o1", "10", "1O", "1o", "Ol", "ol", "l0", "lO", "lo"],
            "0N": ["ON", "oN", "NO", "No", "N0"],
            "0n": ["On", "on", "no", "nO", "n0"],
            "1N": ["N1", "Nl"],
            "1n": ["n1", "nl"],
        }
        self.fixes = {v: k for k in self.fixes for v in self.fixes[k]}
    
    def card(self, tree):
        card = tree[0].value
        new_card = self.fixes.get(card, card)
        return tree[0].update(value=new_card)

def fix_cardinalities(source):
    return transform_source(source, CardinalityFixer())

class AttributeListExtractor(Visitor):
    def __init__(self):
        self.attributes = []
        self.data_type_count = 0
    
    def attr(self, tree):
        self.attributes.append((tree.children[0].value, None))
    
    def data_type(self, tree):
        self.data_type_count += 1
        self.attributes[-1] = (self.attributes[-1][0], tree.children[1].value)

def markdown_data_dict(source):
    tree = parse_source(source)
    extractor = AttributeListExtractor()
    extractor.visit(tree)
    attributes = sorted(extractor.attributes)
    result = []
    if extractor.data_type_count < len(attributes):
        for (attr, data_type) in attributes:
            if data_type is None:
                result.append(f"- {attr}")
            else:
                result.append(f"- {attr} : _{data_type}_")
    else:
        result.append("| Attribut | Informations |")
        result.append("|:---|:---|")
        for (attr, data_type) in attributes:
            result.append(f"| {attr} | {data_type} |")
    return "\n".join(result)

from unicodedata import combining, normalize

LATIN = "ä  æ  ǽ  đ ð ƒ ħ ı ł ø ǿ ö  œ  ß  ŧ ü "
ASCII = "ae ae ae d d f h i l o o oe oe ss t ue"

def remove_diacritics(s, outliers=str.maketrans(dict(zip(LATIN.split(), ASCII.split())))):
    return "".join(c for c in normalize("NFD", s.lower().translate(outliers)) if not combining(c))

def asciify(text):
    text = remove_diacritics(text)
    text = re.sub(r"\W+", "_", text)
    return text

class Asciifier(Transformer):

    def box_name(self, tree):
        return tree[0].update(value=asciify(tree[0].value).upper())
    
    def attr(self, tree):
        return tree[0].update(value=asciify(tree[0].value))
    
    leg_role = attr

def asciify_source(source):
    return transform_source(source, Asciifier())

