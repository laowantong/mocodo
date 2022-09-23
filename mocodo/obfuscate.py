__import__("sys").path[0:0] =  ["."]
import itertools
import os
import random
import re

from .damerau_levenshtein import damerau_levenshtein
from .file_helpers import read_contents
from .mocodo_error import MocodoError


def random_words_of(lorem_text, params):
    words = list(dict.fromkeys(word.lower() for word in re.findall(r"(?u)[^\W\d_]{3,}", lorem_text))) # use dict.fromkeys instead of set for preserving order
    random.shuffle(words)
    previous_words = set()
    for word in words:
        for previous_word in previous_words:
            if damerau_levenshtein(word, previous_word) < params["obfuscation_min_distance"]:
                # print "_%s_ (possible confusion with _%s_)," % (word, previous_word)
                break
        else:
            yield word
            previous_words.add(word)

def obfuscate(clauses, params):
    
    cache = {"": ""}
    def obfuscate_label(label):
        if label not in cache:
            try:
                new_label = next(random_word)
            except StopIteration:
                raise MocodoError(12, _('Obfuscation failed. Not enough substitution words in "{filename}". You may decrease the `obfuscation_min_distance` option values.').format(filename=lorem_filename)) # fmt: skip
            if label.isupper():
                new_label = new_label.upper()
            elif label == label.capitalize():
                new_label = new_label.capitalize()
            cache[label] = new_label
        return cache[label]

    random.seed(params["seed"])
    lorem_filename = params["obfuscate"] or ""
    try:
        lorem_text = read_contents(lorem_filename)
    except IOError:
        try:
            if lorem_filename.endswith(".txt"):
                lorem_filename = lorem_filename[:-4]
            lorem_text = read_contents("%s/resources/lorem/%s.txt" % (params["script_directory"], os.path.basename(lorem_filename)))
        except IOError:
            lorem_text = read_contents("%s/resources/lorem/lorem_ipsum.txt" % params["script_directory"])
    random_word = random_words_of(lorem_text, params)
    header = [comment + "\n" for comment in itertools.takewhile(lambda line: line.startswith("%"), clauses)]
    clauses = "\n".join(clauses[len(header):])
    clauses = re.sub(r"(?m)^([ \t]*)\[(.+?)\]", r"\1<<<safe-left-bracket>>>\2<<<safe-right-bracket>>>", clauses)
    clauses = re.sub(r"\[.+?\]", "", clauses)
    clauses = clauses.replace("<<<safe-left-bracket>>>", "[")
    clauses = clauses.replace("<<<safe-right-bracket>>>", "]")
    clauses = re.sub(r"(?m)^%.*\n?", "", clauses)
    elements = re.split(r"([ \t\]]*(?:[:,\n]+|/[XT]*\\|=>|<=|->|<-)[ \t_\[]*)", clauses) + ['']
    after_first_comma = False
    before_colon = True
    for (i, element) in enumerate(elements):
        if i % 2:
            if "\n" in element:
                after_first_comma = False
                before_colon = True
                inheritance = False
            elif element.startswith("/"):
                inheritance = True
            elif "," in element:
                after_first_comma = True
            elif ":" in element:
                before_colon = False
        else:
            if after_first_comma and before_colon and not inheritance:
                (card, entity_name) = element.split(" ", 1)
                entity_name = entity_name.strip()
                elements[i-1] += card + " "
                elements[i] = entity_name
            elements[i] = obfuscate_label(elements[i])
    return "".join(header + elements).strip()


if __name__=="__main__":
    # launch with:
    # python -m mocodo.obfuscate
    from .argument_parser import parsed_arguments
    clauses = """
        CLIENT: Réf. client, Nom, Prénom, Adresse
        PASSER, 0N CLIENT, /11 COMMANDE
        COMMANDE: Num commande, Date, Montant
        INCLURE, 1N [foobar] COMMANDE, 0N PRODUIT: Quantité
        PRODUIT: Réf. produit, Libellé, Prix unitaire
        [AVOIR COLORIS], 01 PRODUIT, 0N COLORIS
        COLORIS: coloris
    """.replace("  ", "").split("\n")
    params = parsed_arguments()
    params["obfuscate"] = "four_letter_words.txt"
    print(obfuscate(clauses, params))
