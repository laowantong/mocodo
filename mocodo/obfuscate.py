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
            if label.isdigit():
                cache[label] = label
            else:
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
    elements = re.split(r"([ \t\]]*(?:[:,\n]+|/[XT]*\\|\(.*?\)|=>|<=|->|<-|(?<= )<?[-.]+>?)[ \t_\[]*)", clauses) + ['']
    after_first_comma = False
    before_colon = True
    constraint = False
    for (i, element) in enumerate(elements):
        if i % 2:
            if "\n" in element:
                after_first_comma = False
                before_colon = True
                inheritance = False
                constraint = False
            elif element.startswith("/"):
                inheritance = True
            elif element.startswith("("):
                constraint = True
            elif "," in element:
                after_first_comma = True
            elif ":" in element:
                before_colon = False
        else:
            if element and after_first_comma and before_colon and not inheritance and not constraint:
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
        Projet: num. projet, nom projet
        :
        Fournir, 1N Projet, 1N Pièce, 1N Fournisseur
        Fournisseur: num. fournisseur, raison sociale
            
        Requérir, 1N Projet, 0N Pièce: quantité
        :
        Pièce: réf. pièce, libellé pièce

        Date: Date
        Réserver, /1N Client, 1N Chambre, 0N Date: Durée
        Chambre: Numéro, Prix

        :
            
        Client: Id. client

        (CIF) [Même date, même chambre => un seul client] --Chambre, --Date, ->Client, ..Réserver: 20, 80
        (X) [Toute pièce fournie doit avoir été requise.] ..Pièce, ->Requérir, --Fournir, Projet
    """.replace("  ", "").split("\n")
    params = parsed_arguments()
    params["obfuscate"] = "four_letter_words.txt"
    print(obfuscate(clauses, params))
