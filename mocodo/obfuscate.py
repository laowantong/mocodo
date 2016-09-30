#!/usr/bin/env python
# encoding: utf-8

from __future__ import division

import re
import textwrap
import random
from .file_helpers import read_contents
import itertools
import os
from .damerau_levenshtein import damerau_levenshtein
from .mocodo_error import MocodoError

def random_chunks_of(lorem_text, obfuscation_max_length, params):
    words = list(set(word.lower() for word in re.findall(r"(?u)[^\W\d]+", lorem_text)))
    random.shuffle(words)
    if obfuscation_max_length is None:
        obfuscation_max_length = max(map(len, words))
        raw_chunks = iter(textwrap.wrap(" ".join(words), width=obfuscation_max_length))
    else:
        raw_chunks = iter(label for label in textwrap.wrap(" ".join(words), width=obfuscation_max_length, break_long_words=False) if len(label) <= obfuscation_max_length)
    previous_chunks = set()
    for chunk in raw_chunks:
        for previous_chunk in previous_chunks:
            if damerau_levenshtein(chunk, previous_chunk) < params["obfuscation_min_distance"]:
                # print "_%s_ (possible confusion with _%s_)," % (chunk, previous_chunk)
                break
        else:
            yield chunk
            previous_chunks.add(chunk)

def obfuscate(clauses, params):
    
    cache = {"": ""}
    def obfuscate_label(label):
        if label not in cache:
            try:
                new_label = next(random_chunk)
            except StopIteration:
                raise MocodoError(12, _('Obfuscation failed. Not enough substitution words in "{filename}". You may either increase the `obfuscation_max_length` or decrease the `obfuscation_min_distance` option values.').format(filename=lorem_filename))
            if label.isupper():
                new_label = new_label.upper()
            elif label == label.capitalize():
                new_label = new_label.capitalize()
            cache[label] = new_label
        return cache[label]

    lorem_filename = params["obfuscate"] or ""
    try:
        lorem_text = read_contents(lorem_filename)
    except IOError:
        try:
            if lorem_filename.endswith(".txt"):
                lorem_filename = lorem_filename[:-4]
            lorem_text = read_contents("%s/lorem/%s.txt" % (params["script_directory"], os.path.basename(lorem_filename)))
        except IOError:
            lorem_text = read_contents("%s/lorem/lorem_ipsum.txt" % params["script_directory"])
    random_chunk = random_chunks_of(lorem_text, params["obfuscation_max_length"], params)
    header = [comment + "\n" for comment in itertools.takewhile(lambda line: line.startswith("%"), clauses)]
    clauses = "\n".join(clauses[len(header):])
    clauses = re.sub(r"\[.+?\]", "", clauses)
    clauses = re.sub(r"(?m)^%.*\n?", "", clauses)
    elements = re.split(r"([ \t]*[:,\n]+[ \t]*)", clauses) + ['']
    after_first_comma = False
    before_colon = True
    for (i, element) in enumerate(elements):
        if i % 2:
            if "\n" in element:
                after_first_comma = False
                before_colon = True
            elif "," in element:
                after_first_comma = True
            elif ":" in element:
                before_colon = False
        else:
            if after_first_comma and before_colon:
                (card, entity_name) = element.split(" ", 1)
                elements[i-1] += card + " "
                elements[i] = entity_name.strip()
            elements[i] = obfuscate_label(elements[i])
    return "".join(header + elements).strip()


if __name__=="__main__":
    from .argument_parser import parsed_arguments
    clauses = u"""
        CLIENT: Réf. client, Nom, Prénom, Adresse
        PASSER, 0N CLIENT, 11 COMMANDE
        COMMANDE: Num commande, Date, Montant
        INCLURE, 1N [foobar] COMMANDE, 0N PRODUIT: Quantité
        PRODUIT: Réf. produit, Libellé, Prix unitaire
    """.replace("  ", "").split("\n")
    params = parsed_arguments()
    params["seed"] = 42
    params["obfuscate"] = "four_letter_words.txt"
    print(obfuscate(clauses, params))