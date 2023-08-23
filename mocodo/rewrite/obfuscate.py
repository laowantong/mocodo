import random
import re
from pathlib import Path

from .damerau_levenshtein import distance
from ..mocodo_error import MocodoError

MIN_DISTANCE = 3  # Minimal Damereau-Levenshtein distance between two words.

def random_words_generator(
    lorem_text,
    find_all_words=re.compile(r"(?u)[^\W\d_]{3,}").findall,
):
    # use dict.fromkeys instead of set for preserving order
    words = list(dict.fromkeys(word.lower() for word in find_all_words(lorem_text)))
    random.shuffle(words)
    previous_words = set()
    for word in words:
        for previous_word in previous_words:
            if distance(word, previous_word) < MIN_DISTANCE:
                # Keeping this word would be too confusing, let's try the next one.
                break
        else:
            yield word
            previous_words.add(word)


def obfuscator_factory(pool, params):

    if params["seed"] is not None:
        random.seed(params["seed"])

    # Initialize the random word generator
    try:
        lorem_path = Path(pool)
        lorem_text = lorem_path.read_text()
    except IOError:
        lorem_dir = Path(params["script_directory"], "resources", "lorem")
        lorem_path = lorem_dir / f"{lorem_path.stem}.txt"
        try:
            lorem_text = lorem_path.read_text()
        except IOError:
            lorem_path = lorem_dir / "lorem_ipsum.txt"
            lorem_text = lorem_path.read_text()
    random_word = random_words_generator(lorem_text)

    # Define and return the inner obfuscator function
    cache = {}
    def obfuscate(name):
        suffix = ""
        if name[-1].isdigit():
            suffix = name[-1]
            name = name[:-1]
        if name not in cache:
            try:
                new_name = next(random_word)
            except StopIteration:
                raise MocodoError(12, _('Obfuscation failed. Not enough substitution words in "{filename}". You may decrease the `obfuscation_MIN_DISTANCE` option values.').format(filename=self.lorem_path), filename=self.lorem_path, obfuscation_MIN_DISTANCE=params["obfuscation_MIN_DISTANCE"])  # fmt: skip
            if name.isupper():
                new_name = new_name.upper()
            elif name.islower():
                new_name = new_name.lower()
            elif name.istitle():
                new_name = new_name.title()
            cache[name] = new_name
        return cache[name] + suffix
    return obfuscate
