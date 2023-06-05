__import__("sys").path[0:0] = ["."]
import random
import re
from pathlib import Path

from .damerau_levenshtein import distance
from .mocodo_error import MocodoError
from .parse_mcd import Transformer
from .parser_tools import transform_source


def random_words_of(lorem_text, obfuscation_min_distance):
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
    words = list(
        dict.fromkeys(word.lower() for word in re.findall(r"(?u)[^\W\d_]{3,}", lorem_text))
    )  # use dict.fromkeys instead of set for preserving order
    random.shuffle(words)
    previous_words = set()
    for word in words:
        for previous_word in previous_words:
            if distance(word, previous_word) < obfuscation_min_distance:
                # print "_%s_ (possible confusion with _%s_)," % (word, previous_word)
                break
        else:
            yield word
            previous_words.add(word)


class Obfuscator(Transformer):
    def __init__(self, params):
        box_cache = {}
        attr_cache = {}
        lorem_filename = params["obfuscate"] or ""
        try:
            self.lorem_path = Path(lorem_filename)
            lorem_text = self.lorem_path.read_text()
        except IOError:
            try:
                if lorem_filename.endswith(".txt"):
                    lorem_filename = lorem_filename[:-4]
                self.lorem_path = (
                    Path(params["script_directory"])
                    / "resources"
                    / "lorem"
                    / f"{lorem_filename}.txt"
                )
                lorem_text = self.lorem_path.read_text()
            except IOError:
                self.lorem_path = (
                    Path(params["script_directory"]) / "resources" / "lorem" / "lorem_ipsum.txt"
                )
                lorem_text = self.lorem_path.read_text()
        self.random_word = random_words_of(lorem_text, params["obfuscation_min_distance"])
        self.box_name = lambda tree: self.obfuscate_name(box_cache, tree)
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
                raise MocodoError(12, _('Obfuscation failed. Not enough substitution words in "{filename}". You may decrease the `obfuscation_min_distance` option values.').format(filename=self.lorem_path)) # fmt: skip
            if name.isupper():
                new_name = new_name.upper()
            elif name == name.lower():
                new_name = new_name.lower()
            elif name == name.capitalize():
                new_name = new_name.capitalize()
            cache[name] = new_name + suffix
        return tree[0].update(value=cache[name])


def obfuscate(source, params):
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


if __name__ == "__main__":
    # launch with:
    # python -m mocodo.obfuscate
    from .argument_parser import parsed_arguments

    clauses = Path("mocodo/resources/pristine_sandbox.mcd").read_text()
    params = parsed_arguments()
    params["obfuscate"] = "four_letter_words.txt"
    obfuscated_source = obfuscate(f"\n{clauses}\n", params)
    print(obfuscated_source[1:-1])
