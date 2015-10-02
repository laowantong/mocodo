#!/usr/bin/env python
# encoding: utf-8

import re
import textwrap
import random
import codecs
import itertools
import os
from damerau_levenshtein import damerau_levenshtein

def random_chunks_of(lorem_text, obfuscation_max_length):
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
            if damerau_levenshtein(chunk, previous_chunk) <= 2:
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
                new_label = random_chunk.next()
            except StopIteration:
                if params["obfuscation_max_length"] is None:
                    raise RuntimeError(("Mocodo Err.11 - " + _('Obfuscation failed. You may increase the `obfuscation_max_length` option value.')).encode("utf8"))
                else:
                    raise RuntimeError(("Mocodo Err.12 - " + _('Obfuscation failed. Not enough substitution words in "{filename}".').format(filename=lorem_filename)).encode("utf8"))
            if label.isupper():
                new_label = new_label.upper()
            elif label == label.capitalize():
                new_label = new_label.capitalize()
            cache[label] = new_label
        return cache[label]

    lorem_filename = params["obfuscate"] or ""
    try:
        lorem_text = codecs.open(lorem_filename, encoding="utf8").read()
    except IOError:
        try:
            if lorem_filename.endswith(".txt"):
                lorem_filename = lorem_filename[:-4]
            lorem_text = codecs.open("%s/lorem/%s.txt" % (params["script_directory"], os.path.basename(lorem_filename)), encoding="utf8").read()
        except IOError:
            lorem_text = codecs.open("%s/lorem/lorem_ipsum.txt" % params["script_directory"]).read()
    random_chunk = random_chunks_of(lorem_text, params["obfuscation_max_length"])
    header = map(lambda comment: comment + "\n", itertools.takewhile(lambda line: line.startswith("%"), clauses))
    clauses = "\n".join(clauses[len(header):])
    elements = re.split(r"(?u)([:,\n]+ *(?:_?(?:01|0N|11|1N|XX|\?\?)\S*(?: +\[.+?\])? +/?)?)", clauses) + ['']
    for i in range(0,len(elements),2):
        elements[i] = obfuscate_label(elements[i])
    return "".join(header + elements).strip()


if __name__=="__main__":
    from argument_parser import parsed_arguments
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
    print obfuscate(clauses, params)