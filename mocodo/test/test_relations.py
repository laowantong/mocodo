#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys
sys.path[0:0] = ["."]

import unittest
from mocodo.relations import *
from mocodo.mcd import Mcd
import json
from mocodo.file_helpers import read_contents
from copy import deepcopy
from mocodo.argument_parser import parsed_arguments

minimal_template = json.loads(read_contents("mocodo/relation_templates/text.json"))
json_template = json.loads(read_contents("mocodo/relation_templates/json.json"))
params = parsed_arguments()
params["title"] = "Untitled"
params["guess_title"] = False

# Python 2.7 compatibility
if not hasattr(unittest.TestCase, "assertRaisesRegex"):
    unittest.TestCase.assertRaisesRegex = unittest.TestCase.assertRaisesRegexp

class relationsTest(unittest.TestCase):
    
    def test_character_cases(self):
        clauses = u"""
            Riot: clue
            Into, 11 Form, 1N Riot: goat
            Form: land, hide
            Tuck, 1N Read, 1N Form: thin
            Read: wage
        """
        text = u"""
            Riot (_clue_)
            Form (_land_, hide, #clue, goat)
            Tuck (_#wage_, _#land_, thin)
            Read (_wage_)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["title"], u"Untitled")
        self.assertEqual(d["title_titlecase"], u"Untitled")
        self.assertEqual(d["title_lowercase"], u"untitled")
        self.assertEqual(d["title_uppercase"], u"UNTITLED")
        self.assertEqual(d["relations"][0]["this_relation_name"], u"Riot")
        self.assertEqual(d["relations"][0]["this_relation_name_titlecase"], u"Riot")
        self.assertEqual(d["relations"][0]["this_relation_name_uppercase"], u"RIOT")
        self.assertEqual(d["relations"][0]["this_relation_name_lowercase"], u"riot")
        self.assertEqual(d["relations"][0]["columns"][0]["attribute"], u"clue")
        self.assertEqual(d["relations"][0]["columns"][0]["label"], u"clue")
        self.assertEqual(d["relations"][0]["columns"][0]["label_titlecase"], u"Clue")
        self.assertEqual(d["relations"][0]["columns"][0]["label_uppercase"], u"CLUE")
        self.assertEqual(d["relations"][0]["columns"][0]["label_lowercase"], u"clue")
        self.assertEqual(d["relations"][0]["columns"][0]["raw_label"], u"clue")
        self.assertEqual(d["relations"][0]["columns"][0]["raw_label_titlecase"], u"Clue")
        self.assertEqual(d["relations"][0]["columns"][0]["raw_label_uppercase"], u"CLUE")
        self.assertEqual(d["relations"][0]["columns"][0]["raw_label_lowercase"], u"clue")
        self.assertEqual(d["relations"][0]["columns"][0]["primary_relation_name"], None)
        self.assertEqual(d["relations"][0]["columns"][0]["primary_relation_name_titlecase"], None)
        self.assertEqual(d["relations"][0]["columns"][0]["primary_relation_name_uppercase"], None)
        self.assertEqual(d["relations"][0]["columns"][0]["primary_relation_name_lowercase"], None)
        self.assertEqual(d["relations"][0]["columns"][0]["association_name"], None)
        self.assertEqual(d["relations"][0]["columns"][0]["association_name_uppercase"], None)
        self.assertEqual(d["relations"][0]["columns"][0]["association_name_titlecase"], None)
        self.assertEqual(d["relations"][0]["columns"][0]["association_name_lower_case"], None)
        self.assertEqual(d["relations"][1]["columns"][2]["primary_relation_name"], u"Riot")
        self.assertEqual(d["relations"][1]["columns"][2]["primary_relation_name_titlecase"], u"Riot")
        self.assertEqual(d["relations"][1]["columns"][2]["primary_relation_name_uppercase"], u"RIOT")
        self.assertEqual(d["relations"][1]["columns"][2]["primary_relation_name_lowercase"], u"riot")
        self.assertEqual(d["relations"][1]["columns"][2]["association_name"], u"Into")
        self.assertEqual(d["relations"][1]["columns"][2]["association_name_titlecase"], u"Into")
        self.assertEqual(d["relations"][1]["columns"][3]["association_name_lower_case"], u"into")
        self.assertEqual(d["relations"][1]["columns"][2]["association_name_uppercase"], u"INTO")

    def test_attribute_nature_simple(self):
        clauses = u"""
            Riot: clue
            Into, 11 Form, 1N Riot: goat
            Form: land, hide
            Tuck, 1N Read, 1N Form: thin
            Read: wage
        """
        t = Relations(Mcd(clauses.split("\n"), params), params)
        text = u"""
            Riot (_clue_)
            Form (_land_, hide, #clue, goat)
            Tuck (_#wage_, _#land_, thin)
            Read (_wage_)
        """.strip().replace("    ", "")
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["this_relation_name"], u"Riot")
        self.assertEqual(d["relations"][0]["columns"][0]["nature"], u"primary_key")
        self.assertEqual(d["relations"][0]["columns"][0]["label"], u"clue")
        self.assertEqual(d["relations"][1]["this_relation_name"], u"Form")
        self.assertEqual(d["relations"][1]["columns"][0]["nature"], u"primary_key")
        self.assertEqual(d["relations"][1]["columns"][0]["label"], u"land")
        self.assertEqual(d["relations"][1]["columns"][1]["nature"], u"normal_attribute")
        self.assertEqual(d["relations"][1]["columns"][1]["label"], u"hide")
        self.assertEqual(d["relations"][1]["columns"][2]["nature"], u"foreign_key")
        self.assertEqual(d["relations"][1]["columns"][2]["label"], u"clue")
        self.assertEqual(d["relations"][1]["columns"][3]["nature"], u"foreign_attribute")
        self.assertEqual(d["relations"][1]["columns"][3]["label"], u"goat")
        self.assertEqual(d["relations"][2]["this_relation_name"], u"Tuck")
        self.assertEqual(d["relations"][2]["columns"][0]["nature"], u"foreign_primary_key")
        self.assertEqual(d["relations"][2]["columns"][0]["label"], u"wage")
        self.assertEqual(d["relations"][2]["columns"][1]["nature"], u"foreign_primary_key")
        self.assertEqual(d["relations"][2]["columns"][1]["label"], u"land")
        self.assertEqual(d["relations"][2]["columns"][2]["nature"], u"association_attribute")
        self.assertEqual(d["relations"][2]["columns"][2]["label"], u"thin")
        self.assertEqual(d["relations"][3]["this_relation_name"], u"Read")
        self.assertEqual(d["relations"][3]["columns"][0]["nature"], u"primary_key")
        self.assertEqual(d["relations"][3]["columns"][0]["label"], u"wage")

    def test_attribute_nature_complex(self):
        clauses = u"""
            Riot: clue
            Walk, 1N Riot, _11 Hour
            Hour: book
            Poll, 1N Cast, 1N /Hour
            Cast: mere
            Army, 1N /Busy, 01 Cast
            Busy: fail
        """
        text = u"""
            Riot (_clue_)
            Hour (_#clue_, _book_)
            Poll (_#mere_, #clue, #book)
            Cast (_mere_)
            Army (#fail, _#mere_)
            Busy (_fail_)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["this_relation_name"], u"Riot")
        self.assertEqual(d["relations"][0]["columns"][0]["nature"], u"primary_key")
        self.assertEqual(d["relations"][0]["columns"][0]["label"], u"clue")
        self.assertEqual(d["relations"][1]["this_relation_name"], u"Hour")
        self.assertEqual(d["relations"][1]["columns"][0]["nature"], u"strengthening_primary_key")
        self.assertEqual(d["relations"][1]["columns"][0]["label"], u"clue")
        self.assertEqual(d["relations"][1]["columns"][1]["nature"], u"primary_key")
        self.assertEqual(d["relations"][1]["columns"][1]["label"], u"book")
        self.assertEqual(d["relations"][2]["this_relation_name"], u"Poll")
        self.assertEqual(d["relations"][2]["columns"][0]["nature"], u"foreign_primary_key")
        self.assertEqual(d["relations"][2]["columns"][0]["label"], u"mere")
        self.assertEqual(d["relations"][2]["columns"][1]["nature"], u"demoted_foreign_key")
        self.assertEqual(d["relations"][2]["columns"][1]["label"], u"clue")
        self.assertEqual(d["relations"][2]["columns"][2]["nature"], u"demoted_foreign_key")
        self.assertEqual(d["relations"][2]["columns"][2]["label"], u"book")
        self.assertEqual(d["relations"][3]["this_relation_name"], u"Cast")
        self.assertEqual(d["relations"][3]["columns"][0]["nature"], u"primary_key")
        self.assertEqual(d["relations"][3]["columns"][0]["label"], u"mere")
        self.assertEqual(d["relations"][4]["this_relation_name"], u"Army")
        self.assertEqual(d["relations"][4]["columns"][0]["nature"], u"promoting_foreign_key")
        self.assertEqual(d["relations"][4]["columns"][0]["label"], u"fail")
        self.assertEqual(d["relations"][4]["columns"][1]["nature"], u"foreign_primary_key")
        self.assertEqual(d["relations"][4]["columns"][1]["label"], u"mere")
        self.assertEqual(d["relations"][5]["this_relation_name"], u"Busy")
        self.assertEqual(d["relations"][5]["columns"][0]["nature"], u"primary_key")
        self.assertEqual(d["relations"][5]["columns"][0]["label"], u"fail")

    def test_composite_identifier(self):
        clauses = u"""
            GRATTE-CIEL: latitude, _longitude, nom, hauteur, année de construction
        """
        text = u"""
            GRATTE-CIEL (_latitude_, _longitude_, nom, hauteur, année de construction)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["columns"][0]["nature"], u"primary_key")
        self.assertEqual(d["relations"][0]["columns"][0]["label"], u"latitude")
        self.assertEqual(d["relations"][0]["columns"][1]["nature"], u"primary_key")
        self.assertEqual(d["relations"][0]["columns"][1]["label"], u"longitude")
    
    def test_reflexive_df(self):
        clauses = u"""
            HOMME: Num. SS, Nom, Prénom
            ENGENDRER, 0N HOMME, 11 HOMME
        """
        text = u"""
            HOMME (_Num. SS_, Nom, Prénom, #Num. SS.1)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["columns"][3]["foreign"], True)
        self.assertEqual(d["relations"][0]["columns"][3]["data_type"], None)
        self.assertEqual(d["relations"][0]["columns"][3]["nature"], u"foreign_key")
        self.assertEqual(d["relations"][0]["columns"][3]["attribute"], u"Num. SS")
        self.assertEqual(d["relations"][0]["columns"][3]["primary"], False)
        self.assertEqual(d["relations"][0]["columns"][3]["label"], u"Num. SS.1")
        self.assertEqual(d["relations"][0]["columns"][3]["raw_label"], u"Num. SS")
        self.assertEqual(d["relations"][0]["columns"][3]["association_name"], u"ENGENDRER")
        self.assertEqual(d["relations"][0]["columns"][3]["disambiguation_number"], 1)
        self.assertEqual(d["relations"][0]["columns"][3]["primary_relation_name"], u"HOMME")
        self.assertEqual(d["title"], u"Untitled")

    def test_arrows_are_ignored(self):
        clauses = u"""
            Personne: Num. SS, Nom, Prénom, Sexe
            Engendrer, 0N< Personne, 22> Personne
        """
        t = Relations(Mcd(clauses.split("\n"), params), params)
        d1 = json.loads(t.get_text(json_template))
        clauses = u"""
            Personne: Num. SS, Nom, Prénom, Sexe
            Engendrer, 0N Personne, 22 Personne
        """
        t = Relations(Mcd(clauses.split("\n"), params), params)
        d2 = json.loads(t.get_text(json_template))
        self.assertEqual(d1, d2)
    
    def test_annotations(self):
        clauses = u"""
            Personne: Num. SS, Nom, Prénom, Sexe
            Engendrer, 0N [parent] Personne, 0N [enfant] Personne
        """
        text = u"""
            Personne (_Num. SS_, Nom, Prénom, Sexe)
            Engendrer (_#Num. SS parent_, _#Num. SS enfant_)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["this_relation_name"], u"Personne")
        self.assertEqual(d["relations"][0]["columns"][0]["leg_annotation"], None)
        self.assertEqual(d["relations"][0]["columns"][0]["label"], u"Num. SS")
        self.assertEqual(d["relations"][0]["columns"][1]["leg_annotation"], None)
        self.assertEqual(d["relations"][0]["columns"][1]["label"], u"Nom")
        self.assertEqual(d["relations"][0]["columns"][2]["leg_annotation"], None)
        self.assertEqual(d["relations"][0]["columns"][2]["label"], u"Prénom")
        self.assertEqual(d["relations"][0]["columns"][3]["leg_annotation"], None)
        self.assertEqual(d["relations"][0]["columns"][3]["label"], u"Sexe")
        self.assertEqual(d["relations"][1]["this_relation_name"], u"Engendrer")
        self.assertEqual(d["relations"][1]["columns"][0]["leg_annotation"], u"parent")
        self.assertEqual(d["relations"][1]["columns"][0]["label"], u"Num. SS parent")
        self.assertEqual(d["relations"][1]["columns"][1]["leg_annotation"], u"enfant")
        self.assertEqual(d["relations"][1]["columns"][1]["label"], u"Num. SS enfant")
    
    def test_annotations_with_numbers_only_disambiguation_strategy(self):
        clauses = u"""
            Personne: Num. SS, Nom, Prénom, Sexe
            Engendrer, 0N [Une personne peut avoir un nombre quelconque d'enfants.] Personne, 0N [Une personne peut avoir un nombre quelconque de parents dans la base.\\nRemarque : vous avez peut-être envie de remplacer la cardinalité maximale N par sa valeur réelle, à savoir 2. Cette précision disparaissant lors du passage au relationnel, elle est en général jugée inutile.] Personne
        """
        text = u"""
            Personne (_Num. SS_, Nom, Prénom, Sexe)
            Engendrer (_#Num. SS_, _#Num. SS.1_)
        """.strip().replace("    ", "")
        local_params = deepcopy(params)
        local_params["disambiguation"] = "numbers_only"
        t = Relations(Mcd(clauses.split("\n"), local_params), local_params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["this_relation_name"], u"Personne")
        self.assertEqual(d["relations"][0]["columns"][0]["leg_annotation"], None)
        self.assertEqual(d["relations"][0]["columns"][0]["label"], u"Num. SS")
        self.assertEqual(d["relations"][0]["columns"][1]["leg_annotation"], None)
        self.assertEqual(d["relations"][0]["columns"][1]["label"], u"Nom")
        self.assertEqual(d["relations"][0]["columns"][2]["leg_annotation"], None)
        self.assertEqual(d["relations"][0]["columns"][2]["label"], u"Prénom")
        self.assertEqual(d["relations"][0]["columns"][3]["leg_annotation"], None)
        self.assertEqual(d["relations"][0]["columns"][3]["label"], u"Sexe")
        self.assertEqual(d["relations"][1]["this_relation_name"], u"Engendrer")
        self.assertEqual(d["relations"][1]["columns"][0]["leg_annotation"], u"Une personne peut avoir un nombre quelconque d\\'enfants.")
        self.assertEqual(d["relations"][1]["columns"][0]["label"], u"Num. SS")
        self.assertEqual(d["relations"][1]["columns"][1]["leg_annotation"], u"Une personne peut avoir un nombre quelconque de parents dans la base.\nRemarque : vous avez peut-être envie de remplacer la cardinalité maximale N par sa valeur réelle, à savoir 2. Cette précision disparaissant lors du passage au relationnel, elle est en général jugée inutile.")
        self.assertEqual(d["relations"][1]["columns"][1]["label"], u"Num. SS.1")

    def test_data_types(self):
        clauses = u"""
            CLIENT: Réf. client [varchar(8)], Nom [varchar(20)], Adresse [varchar(40)]
            DF, 0N CLIENT, 11 COMMANDE
            COMMANDE: Num commande [tinyint(4)], Date [date], Montant [decimal(5,2) DEFAULT '0.00']
            INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité [tinyint(4)]
            PRODUIT: Réf. produit, Libellé, Prix unitaire
        """
        text = u"""
            CLIENT (_Réf. client_, Nom, Adresse)
            COMMANDE (_Num commande_, Date, Montant, #Réf. client)
            INCLURE (_#Num commande_, _#Réf. produit_, Quantité)
            PRODUIT (_Réf. produit_, Libellé, Prix unitaire)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["this_relation_name"], u"CLIENT")
        self.assertEqual(d["relations"][0]["columns"][0]["data_type"], u"varchar(8)")
        self.assertEqual(d["relations"][0]["columns"][0]["label"], u"Réf. client")
        self.assertEqual(d["relations"][0]["columns"][1]["data_type"], u"varchar(20)")
        self.assertEqual(d["relations"][0]["columns"][1]["label"], u"Nom")
        self.assertEqual(d["relations"][0]["columns"][2]["data_type"], u"varchar(40)")
        self.assertEqual(d["relations"][0]["columns"][2]["label"], u"Adresse")
        self.assertEqual(d["relations"][1]["this_relation_name"], u"COMMANDE")
        self.assertEqual(d["relations"][1]["columns"][0]["data_type"], u"tinyint(4)")
        self.assertEqual(d["relations"][1]["columns"][0]["label"], u"Num commande")
        self.assertEqual(d["relations"][1]["columns"][1]["data_type"], u"date")
        self.assertEqual(d["relations"][1]["columns"][1]["label"], u"Date")
        self.assertEqual(d["relations"][1]["columns"][2]["data_type"], u"decimal(5,2) DEFAULT '0.00'")
        self.assertEqual(d["relations"][1]["columns"][2]["label"], u"Montant")
        self.assertEqual(d["relations"][1]["columns"][3]["data_type"], u"varchar(8)")
        self.assertEqual(d["relations"][1]["columns"][3]["label"], u"Réf. client")
        self.assertEqual(d["relations"][2]["this_relation_name"], u"INCLURE")
        self.assertEqual(d["relations"][2]["columns"][0]["data_type"], u"tinyint(4)")
        self.assertEqual(d["relations"][2]["columns"][0]["label"], u"Num commande")
        self.assertEqual(d["relations"][2]["columns"][1]["data_type"], None)
        self.assertEqual(d["relations"][2]["columns"][1]["label"], u"Réf. produit")
        self.assertEqual(d["relations"][2]["columns"][2]["data_type"], u"tinyint(4)")
        self.assertEqual(d["relations"][2]["columns"][2]["label"], u"Quantité")
        self.assertEqual(d["relations"][3]["this_relation_name"], u"PRODUIT")
        self.assertEqual(d["relations"][3]["columns"][0]["data_type"], None)
        self.assertEqual(d["relations"][3]["columns"][0]["label"], u"Réf. produit")
        self.assertEqual(d["relations"][3]["columns"][1]["data_type"], None)
        self.assertEqual(d["relations"][3]["columns"][1]["label"], u"Libellé")
        self.assertEqual(d["relations"][3]["columns"][2]["data_type"], None)
        self.assertEqual(d["relations"][3]["columns"][2]["label"], u"Prix unitaire")

    def test_all_cardinalities_other_than_01_and_11_are_treated_as_1N(self):
        clauses = u"""
            CLIENT: Réf. client, Nom, Prénom, Adresse
            PASSER, XX CLIENT, N1 COMMANDE
            COMMANDE: Num commande, Date, Montant
            INCLURE, 03 COMMANDE, ?? PRODUIT: Quantité
            PRODUIT: Réf. produit, Libellé, Prix unitaire
        """
        t = Relations(Mcd(clauses.split("\n"), params), params)
        d1 = json.loads(t.get_text(json_template))
        clauses = u"""
            CLIENT: Réf. client, Nom, Prénom, Adresse
            PASSER, 1N CLIENT, 1N COMMANDE
            COMMANDE: Num commande, Date, Montant
            INCLURE, 1N COMMANDE, 1N PRODUIT: Quantité
            PRODUIT: Réf. produit, Libellé, Prix unitaire
        """
        t = Relations(Mcd(clauses.split("\n"), params), params)
        d2 = json.loads(t.get_text(json_template))
        self.assertEqual(d1, d2)

    def test_empty_attributes(self):
        clauses = u"""
            CLIENT: Réf. client, , , 
        """
        text = u"""
            CLIENT (_Réf. client_, , .1, .2)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["columns"][1]["attribute"], u"")
        self.assertEqual(d["relations"][0]["columns"][1]["raw_label"], u"")
        self.assertEqual(d["relations"][0]["columns"][1]["label"], u"")
        self.assertEqual(d["relations"][0]["columns"][1]["disambiguation_number"], None)
        self.assertEqual(d["relations"][0]["columns"][2]["attribute"], u"")
        self.assertEqual(d["relations"][0]["columns"][2]["raw_label"], u"")
        self.assertEqual(d["relations"][0]["columns"][2]["label"], u".1")
        self.assertEqual(d["relations"][0]["columns"][2]["disambiguation_number"], 1)

    def test_demoted_foreign_key(self):
        clauses = u"""
            LACUS: blandit, elit
            LIGULA, 0N LACUS, 1N /EROS, 0N TELLUS: metus
            EROS: congue, nibh, tincidunt
            
            TELLUS: integer, odio
        """
        text = u"""
            LACUS (_blandit_, elit)
            LIGULA (_#blandit_, #congue, _#integer_, metus)
            EROS (_congue_, nibh, tincidunt)
            TELLUS (_integer_, odio)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][1]["this_relation_name"], u"LIGULA")
        self.assertEqual(d["relations"][1]["columns"][0]["nature"], u"foreign_primary_key")
        self.assertEqual(d["relations"][1]["columns"][0]["primary_relation_name"], u"LACUS")
        self.assertEqual(d["relations"][1]["columns"][1]["nature"], u"demoted_foreign_key")
        self.assertEqual(d["relations"][1]["columns"][1]["primary_relation_name"], u"EROS")
        self.assertEqual(d["relations"][1]["columns"][2]["nature"], u"foreign_primary_key")
        self.assertEqual(d["relations"][1]["columns"][2]["primary_relation_name"], u"TELLUS")
        self.assertEqual(d["relations"][1]["columns"][3]["nature"], u"association_attribute")
        self.assertEqual(d["relations"][1]["columns"][3]["primary_relation_name"], None)

    def test_promoting_foreign_key(self):
        clauses = u"""
            LACUS: blandit, elit
            LIGULA, 01 LACUS, 1N /EROS: metus
            EROS: congue, nibh, tincidunt
        """
        text = u"""
            LACUS (_blandit_, elit)
            LIGULA (_#blandit_, #congue, metus)
            EROS (_congue_, nibh, tincidunt)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][1]["this_relation_name"], u"LIGULA")
        self.assertEqual(d["relations"][1]["columns"][0]["nature"], u"foreign_primary_key")
        self.assertEqual(d["relations"][1]["columns"][0]["primary_relation_name"], u"LACUS")
        self.assertEqual(d["relations"][1]["columns"][1]["nature"], u"promoting_foreign_key")
        self.assertEqual(d["relations"][1]["columns"][1]["primary_relation_name"], u"EROS")
        self.assertEqual(d["relations"][1]["columns"][2]["nature"], u"association_attribute")
        self.assertEqual(d["relations"][1]["columns"][2]["primary_relation_name"], None)
    
    def test_weak_entities(self):
        clauses = u"""
            Rue: code rue, nom rue
            Se situer, 0N Rue, _11 Immeuble
            Immeuble: num immeuble, nb étages immeuble
            Appartenir, 1N Immeuble, _11 Étage
            Étage: num étage, nb appart. étage
            Composer, 0N Étage, _11 Appartement
            Appartement: num appart., nb pièces appart.
        """
        text = u"""
            Rue (_code rue_, nom rue)
            Immeuble (_#code rue_, _num immeuble_, nb étages immeuble)
            Étage (_#code rue_, _#num immeuble_, _num étage_, nb appart. étage)
            Appartement (_#code rue_, _#num immeuble_, _#num étage_, _num appart._, nb pièces appart.)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][3]["this_relation_name"], u"Appartement")
        self.assertEqual(d["relations"][3]["columns"][0]["attribute"], u"code rue")
        self.assertEqual(d["relations"][3]["columns"][0]["label"], u"code rue")
        self.assertEqual(d["relations"][3]["columns"][0]["raw_label"], u"code rue")
        self.assertEqual(d["relations"][3]["columns"][0]["foreign"], True)
        self.assertEqual(d["relations"][3]["columns"][0]["primary"], True)
        self.assertEqual(d["relations"][3]["columns"][0]["nature"], u"strengthening_primary_key")
        self.assertEqual(d["relations"][3]["columns"][0]["association_name"], u"Composer")
        self.assertEqual(d["relations"][3]["columns"][0]["primary_relation_name"], u"Étage")
        
        self.assertEqual(d["relations"][3]["columns"][1]["attribute"], u"num immeuble")
        self.assertEqual(d["relations"][3]["columns"][1]["label"], u"num immeuble")
        self.assertEqual(d["relations"][3]["columns"][1]["raw_label"], u"num immeuble")
        self.assertEqual(d["relations"][3]["columns"][1]["foreign"], True)
        self.assertEqual(d["relations"][3]["columns"][1]["primary"], True)
        self.assertEqual(d["relations"][3]["columns"][1]["nature"], u"strengthening_primary_key")
        self.assertEqual(d["relations"][3]["columns"][1]["association_name"], u"Composer")
        self.assertEqual(d["relations"][3]["columns"][1]["primary_relation_name"], u"Étage")
        
        self.assertEqual(d["relations"][3]["columns"][2]["attribute"], u"num étage")
        self.assertEqual(d["relations"][3]["columns"][2]["label"], u"num étage")
        self.assertEqual(d["relations"][3]["columns"][2]["raw_label"], u"num étage")
        self.assertEqual(d["relations"][3]["columns"][2]["foreign"], True)
        self.assertEqual(d["relations"][3]["columns"][2]["primary"], True)
        self.assertEqual(d["relations"][3]["columns"][2]["nature"], u"strengthening_primary_key")
        self.assertEqual(d["relations"][3]["columns"][2]["association_name"], u"Composer")
        self.assertEqual(d["relations"][3]["columns"][2]["primary_relation_name"], u"Étage")
        
        self.assertEqual(d["relations"][3]["columns"][3]["attribute"], u"num appart.")
        self.assertEqual(d["relations"][3]["columns"][3]["label"], u"num appart.")
        self.assertEqual(d["relations"][3]["columns"][3]["raw_label"], u"num appart.")
        self.assertEqual(d["relations"][3]["columns"][3]["foreign"], False)
        self.assertEqual(d["relations"][3]["columns"][3]["primary"], True)
        self.assertEqual(d["relations"][3]["columns"][3]["nature"], u"primary_key")
        self.assertEqual(d["relations"][3]["columns"][3]["association_name"], None)
        self.assertEqual(d["relations"][3]["columns"][3]["primary_relation_name"], None)
        
        self.assertEqual(d["relations"][3]["columns"][4]["attribute"], u"nb pièces appart.")
        self.assertEqual(d["relations"][3]["columns"][4]["label"], u"nb pièces appart.")
        self.assertEqual(d["relations"][3]["columns"][4]["raw_label"], u"nb pièces appart.")
        self.assertEqual(d["relations"][3]["columns"][4]["foreign"], False)
        self.assertEqual(d["relations"][3]["columns"][4]["primary"], False)
        self.assertEqual(d["relations"][3]["columns"][4]["nature"], u"normal_attribute")
        self.assertEqual(d["relations"][3]["columns"][4]["association_name"], None)
        self.assertEqual(d["relations"][3]["columns"][4]["primary_relation_name"], None)
        self.assertEqual(d["title"], u"Untitled")
    
    def test_reciprocical_relative_entities(self):
        clauses = u"""
            Aids: Norm, Free, Soon, Pack, Face, Seem, Teen
            Yard, 0N Unit, ON Aids
            Ever, 1N Unit, 1N Item
            Item: Norm, Wash, Haul, Milk, Draw, Lady, Face, Soon, Dish
            :

            Amid, 1n Aids, 1n Disk, _11 Flip: Gold
            Same, _11 Unit, 0N Flip
            Unit: Folk, Peer, Tour, Hall
            Fold, _11 Unit, 1N Baby, _11 Item
            Baby: Soon

            Disk: Soon, Ride, Folk, Call, Gear, Tent, Lean
            Flip: Lend
            Pump, _11 Flip, 1N Unit: Both, Raid
            Gene: Soon
            Bind, _11 Baby, 1n Gene
        """
        mcd = Mcd(clauses.split("\n"), params)
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.22", Relations, mcd, params)
        clauses = u"""
            Disk: Soon, Ride, Folk, Call, Gear, Tent, Lean
            Flip: Lend
            Pump, _11 Flip, 1N Unit: Both, Raid
            Gene: Soon
            Bind, _11 Baby, 1n Gene

            Amid, 1n Aids, 1n Disk, _11 Flip: Gold
            Same, _11 Unit, 0N Flip
            Unit: Folk, Peer, Tour, Hall
            Fold, _11 Unit, 1N Baby, _11 Item
            Baby: Soon

            Aids: Norm, Free, Soon, Pack, Face, Seem, Teen
            Yard, 0N Unit, ON Aids
            Ever, 1N Unit, 1N Item
            Item: Norm, Wash, Haul, Milk, Draw, Lady, Face, Soon, Dish
            :
        """
        mcd = Mcd(clauses.split("\n"), params)
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.22", Relations, mcd, params)
        mcd = Mcd(clauses.split("\n"), params)
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.22", Relations, mcd, params)
        clauses = u"""
            ITEM, 1N NORM, 1N WASH
            NORM: haul
            
            WASH: soon
            BABY, 1N WASH, 1N FACE
            FACE: gene
            
            AAA, _11 FLIP, 1N WASH
            FLIP: soona
            GEAR, _11 FLIP, _11 FACE
        """
        mcd = Mcd(clauses.split("\n"), params)
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.22", Relations, mcd, params)
        clauses = u"""
            ITEM, 1N NORM, 1N WASH
            NORM: haul
            
            WASH: soon
            BABY, 1N WASH, 1N FACE
            FACE: gene
            
            CCC, _11 FLIP, 1N WASH
            FLIP: soona
            GEAR, _11 FLIP, _11 FACE
        """
        mcd = Mcd(clauses.split("\n"), params)
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.22", Relations, mcd, params)

    
    def test_weak_entities_strengthened_by_itself(self):
        clauses = u"""
            SCELERISQUE: blandit, elit
            DF, _11 SCELERISQUE, 1N SCELERISQUE
        """
        mcd = Mcd(clauses.split("\n"), params)
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.16", Relations, mcd, params)
    
    def test_weak_entities_strengthened_by_several_entities(self):
        clauses = u"""
            Baby: Soon
            Yard, _11 Unit, ON Baby: Hall
            
            :
            Unit: Folk, Peer
            
            
            Item: Norm, Wash
            Ever, _11 Unit, 1N Item: Tour
        """
        # the actual order of the result depends on Python's version
        possible_text_1 = u"""
            Baby (_Soon_)
            Unit (_#Norm_, _#Soon_, _Folk_, Peer, Hall, Tour)
            Item (_Norm_, Wash)
        """.strip().replace("    ", "")
        possible_text_2 = u"""
            Baby (_Soon_)
            Unit (_#Soon_, _#Norm_, _Folk_, Peer, Tour, Hall)
            Item (_Norm_, Wash)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertTrue(t.get_text(minimal_template) in (possible_text_1, possible_text_2))
    
    def test_weak_entities_with_cycle(self):
        clauses = u"""
            ITEM: norm, wash, haul
            MILK, _11 ITEM, 1N DRAW: lady, face

            SOON, 1N ITEM, _11 DRAW
            DRAW: ever, unit, tour, fold
        """
        mcd = Mcd(clauses.split("\n"), params)
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.17", Relations, mcd, params)
    
    def test_difference_between_attribute_raw_label_and_label_with_annotations(self):
        template = {
          "extension": ".json",
          "transform_attribute": [
            {
              "search": " ",
              "replace": "_"
            },
            {
              "search": "\\.",
              "replace": ""
            }
          ],
          "compose_label_disambiguated_by_annotation": u"{leg_annotation}",
        }
        clauses = u"""
            A pour mère, 01 Chien, 0N [num_mère] Chien
            Chien: num. chien, nom chien, sexe, date naissance
            A pour père présumé, 0N Chien, 0N [num_père] Chien
        """
        text = u"""
            Chien (_num_chien_, nom_chien, sexe, date_naissance, #num_mère)
            A pour père présumé (_#num_chien_, _#num_père_)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(template), text)
        my_json_template = deepcopy(json_template)
        my_json_template.update(template)
        d = json.loads(t.get_text(my_json_template))
        self.assertEqual(d["relations"][0]["this_relation_name"], u"Chien")
        self.assertEqual(d["relations"][0]["columns"][0]["attribute"], u"num. chien")
        self.assertEqual(d["relations"][0]["columns"][0]["raw_label"], u"num_chien")
        self.assertEqual(d["relations"][0]["columns"][0]["label"],     u"num_chien")
        self.assertEqual(d["relations"][0]["columns"][4]["attribute"], u"num. chien")
        self.assertEqual(d["relations"][0]["columns"][4]["raw_label"], u"num_chien")
        self.assertEqual(d["relations"][0]["columns"][4]["label"],     u"num_mère")
        self.assertEqual(d["relations"][1]["this_relation_name"], u"A pour père présumé")
        self.assertEqual(d["relations"][1]["columns"][1]["attribute"], u"num. chien")
        self.assertEqual(d["relations"][1]["columns"][1]["raw_label"], u"num_chien")
        self.assertEqual(d["relations"][1]["columns"][1]["label"],     u"num_père")
    
    def test_difference_between_attribute_raw_label_and_label_without_annotations(self):
        template = {
          "extension": None,
          "transform_attribute": [
            {
              "search": " ",
              "replace": "_"
            },
            {
              "search": "\\.",
              "replace": ""
            }
          ],
          "compose_label_disambiguated_by_number": u"{label}_{disambiguation_number}",
        }
        clauses = u"""
            A pour mère, 01 Chien, 0N Chien
            Chien: num. chien, nom chien, sexe, date naissance
            A pour père présumé, 0N Chien, 0N Chien
        """
        text = u"""
            Chien (_num_chien_, nom_chien, sexe, date_naissance, #num_chien_1)
            A pour père présumé (_#num_chien_, _#num_chien_1_)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(template), text)
        my_json_template = deepcopy(json_template)
        my_json_template.update(template)
        d = json.loads(t.get_text(my_json_template))
        self.assertEqual(d["relations"][0]["this_relation_name"], u"Chien")
        self.assertEqual(d["relations"][0]["columns"][0]["attribute"], u"num. chien")
        self.assertEqual(d["relations"][0]["columns"][0]["raw_label"], u"num_chien")
        self.assertEqual(d["relations"][0]["columns"][0]["label"],     u"num_chien")
        self.assertEqual(d["relations"][0]["columns"][4]["attribute"], u"num. chien")
        self.assertEqual(d["relations"][0]["columns"][4]["raw_label"], u"num_chien")
        self.assertEqual(d["relations"][0]["columns"][4]["label"],     u"num_chien_1")
        self.assertEqual(d["relations"][1]["this_relation_name"], u"A pour père présumé")
        self.assertEqual(d["relations"][1]["columns"][1]["attribute"], u"num. chien")
        self.assertEqual(d["relations"][1]["columns"][1]["raw_label"], u"num_chien")
        self.assertEqual(d["relations"][1]["columns"][1]["label"],     u"num_chien_1")


if __name__ == '__main__':
    unittest.main()
