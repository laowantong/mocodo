import random
import re
from pathlib import Path

__import__("sys").path[0:0] = ["."]

from ..damerau_levenshtein import distance
from ..mocodo_error import MocodoError
from ..parse_mcd import Transformer
from ..parser_tools import transform_source


def random_words_of(
    lorem_text,
    obfuscation_min_distance,
    seed,
    find_all_words=re.compile(r"(?u)[^\W\d_]{3,}").findall,
):
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
    # use dict.fromkeys instead of set for preserving order
    words = list(dict.fromkeys(word.lower() for word in find_all_words(lorem_text)))
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
        try:
            self.lorem_path = Path(params["obfuscation_source"] or "")
            lorem_text = self.lorem_path.read_text()
        except IOError:
            lorem_dir = Path(params["script_directory"]) / "resources" / "lorem"
            self.lorem_path = lorem_dir / f"{self.lorem_path.stem}.txt"
            try:
                lorem_text = self.lorem_path.read_text()
            except IOError:
                self.lorem_path = lorem_dir / "lorem_ipsum.txt"
                lorem_text = self.lorem_path.read_text()
        self.random_word = random_words_of(
            lorem_text,
            params["obfuscation_min_distance"],
            params["seed"],
        )
        self.box_cache = {}
        self.attr_cache = {}

    def _obfuscate_name(self, cache, tree):
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
                new_name = new_name.title()
            cache[name] = new_name + suffix
        return tree[0].update(value=cache[name])

    def box_name(self, tree):
        return self._obfuscate_name(self.box_cache, tree)

    def attr(self, tree):
        return self._obfuscate_name(self.attr_cache, tree)
    
    def leg_note(self, tree):
        return self._obfuscate_name({}, tree)


def run(source, params):
    return transform_source(source, Obfuscator(params))
