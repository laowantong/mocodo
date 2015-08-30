#!/usr/bin/env python
# encoding: utf-8

irregular_plurals = {
 'aieul': 'aieux',
 'aval': 'avals',
 'bail': 'baux',
 'bal': 'bals',
 'betail': 'bestiaux',
 'bijou': 'bijoux',
 'bleu': 'bleus',
 'caillou': 'cailloux',
 'cal': 'cals',
 'carnaval': 'carnavals',
 'chacal': 'chacals',
 'choral': 'chorals',
 'chou': 'choux',
 'ciel': 'cieux',
 'corail': 'coraux',
 'credit-bail': 'credits-baux',
 'email': 'emaux',
 'emeu': 'emeus',
 'emmenthal': 'emmenthals',
 'enfeu': 'enfeus',
 'etal': 'etals',
 'fatal': 'fatals',
 'festival': 'festivals',
 'gemmail': 'gemmaux',
 'genou': 'genoux',
 'gentilhomme': 'gentilshommes',
 'glacial': 'glacials',
 'hibou': 'hiboux',
 'joujou': 'joujoux',
 'landau': 'landaus',
 'madame': 'mesdames',
 'mademoiselle': 'mesdemoiselles',
 'mistral': 'mistrals',
 'monsieur': 'messieurs',
 'natal': 'natals',
 'naval': 'navals',
 'oeil': 'yeux',
 'oeil-de-boeuf': 'oeils-de-boeuf',
 'oeil-de-chat': 'oeils-de-chat',
 'pal': 'pals',
 'pascal': 'pascals',
 'perinatal': 'perinatals',
 'pneu': 'pneus',
 'postnatal': 'postnatals',
 'pou': 'poux',
 'prenatal': 'prenatals',
 'recital': 'recitals',
 'regal': 'regals',
 'sarrau': 'sarraus',
 'soupirail': 'soupiraux',
 'travail': 'travaux',
 'unau': 'unaus',
 'vantail': 'vantaux',
 'veto': 'veto',
 'vitrail': 'vitraux'
}

def pluralize(word):
    if word in irregular_plurals:
        return irregular_plurals[word]
    if word.endswith(("eau", "oeu")):
        return word + "x"
    if word.endswith(("s", "x", "z")):
        return word
    if word.endswith("al"):
        return word[:-2] + "aux"
    if word.endswith(("au", "eu")):
        return word + "x"
    return word + "s"
