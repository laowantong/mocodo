#!/usr/bin/python
# encoding: utf-8

import unittest
from mocodo.relations import *
from mocodo.mcd import Mcd
import json
from file_helpers import read_contents
from copy import deepcopy
from mocodo.argument_parser import parsed_arguments

minimal_template = json.loads(read_contents("mocodo/relation_templates/text.json"))
json_template = json.loads(read_contents("mocodo/relation_templates/json.json"))
params = parsed_arguments()
params["title"] = "Untitled"
params["guess_title"] = False

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
        self.assertEquals(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEquals(d["title"], u"Untitled")
        self.assertEquals(d["title_titlecase"], u"Untitled")
        self.assertEquals(d["title_lowercase"], u"untitled")
        self.assertEquals(d["title_uppercase"], u"UNTITLED")
        self.assertEquals(d["relations"][0]["this_relation_name"], u"Riot")
        self.assertEquals(d["relations"][0]["this_relation_name_titlecase"], u"Riot")
        self.assertEquals(d["relations"][0]["this_relation_name_uppercase"], u"RIOT")
        self.assertEquals(d["relations"][0]["this_relation_name_lowercase"], u"riot")
        self.assertEquals(d["relations"][0]["columns"][0]["attribute"], u"clue")
        self.assertEquals(d["relations"][0]["columns"][0]["label"], u"clue")
        self.assertEquals(d["relations"][0]["columns"][0]["label_titlecase"], u"Clue")
        self.assertEquals(d["relations"][0]["columns"][0]["label_uppercase"], u"CLUE")
        self.assertEquals(d["relations"][0]["columns"][0]["label_lowercase"], u"clue")
        self.assertEquals(d["relations"][0]["columns"][0]["raw_label"], u"clue")
        self.assertEquals(d["relations"][0]["columns"][0]["raw_label_titlecase"], u"Clue")
        self.assertEquals(d["relations"][0]["columns"][0]["raw_label_uppercase"], u"CLUE")
        self.assertEquals(d["relations"][0]["columns"][0]["raw_label_lowercase"], u"clue")
        self.assertEquals(d["relations"][0]["columns"][0]["primary_relation_name"], None)
        self.assertEquals(d["relations"][0]["columns"][0]["primary_relation_name_titlecase"], None)
        self.assertEquals(d["relations"][0]["columns"][0]["primary_relation_name_uppercase"], None)
        self.assertEquals(d["relations"][0]["columns"][0]["primary_relation_name_lowercase"], None)
        self.assertEquals(d["relations"][0]["columns"][0]["association_name"], None)
        self.assertEquals(d["relations"][0]["columns"][0]["association_name_uppercase"], None)
        self.assertEquals(d["relations"][0]["columns"][0]["association_name_titlecase"], None)
        self.assertEquals(d["relations"][0]["columns"][0]["association_name_lower_case"], None)
        self.assertEquals(d["relations"][1]["columns"][2]["primary_relation_name"], u"Riot")
        self.assertEquals(d["relations"][1]["columns"][2]["primary_relation_name_titlecase"], u"Riot")
        self.assertEquals(d["relations"][1]["columns"][2]["primary_relation_name_uppercase"], u"RIOT")
        self.assertEquals(d["relations"][1]["columns"][2]["primary_relation_name_lowercase"], u"riot")
        self.assertEquals(d["relations"][1]["columns"][2]["association_name"], u"Into")
        self.assertEquals(d["relations"][1]["columns"][2]["association_name_titlecase"], u"Into")
        self.assertEquals(d["relations"][1]["columns"][3]["association_name_lower_case"], u"into")
        self.assertEquals(d["relations"][1]["columns"][2]["association_name_uppercase"], u"INTO")

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
        self.assertEquals(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEquals(d["relations"][0]["this_relation_name"], u"Riot")
        self.assertEquals(d["relations"][0]["columns"][0]["nature"], u"primary_key")
        self.assertEquals(d["relations"][0]["columns"][0]["label"], u"clue")
        self.assertEquals(d["relations"][1]["this_relation_name"], u"Form")
        self.assertEquals(d["relations"][1]["columns"][0]["nature"], u"primary_key")
        self.assertEquals(d["relations"][1]["columns"][0]["label"], u"land")
        self.assertEquals(d["relations"][1]["columns"][1]["nature"], u"normal_attribute")
        self.assertEquals(d["relations"][1]["columns"][1]["label"], u"hide")
        self.assertEquals(d["relations"][1]["columns"][2]["nature"], u"foreign_key")
        self.assertEquals(d["relations"][1]["columns"][2]["label"], u"clue")
        self.assertEquals(d["relations"][1]["columns"][3]["nature"], u"foreign_attribute")
        self.assertEquals(d["relations"][1]["columns"][3]["label"], u"goat")
        self.assertEquals(d["relations"][2]["this_relation_name"], u"Tuck")
        self.assertEquals(d["relations"][2]["columns"][0]["nature"], u"foreign_primary_key")
        self.assertEquals(d["relations"][2]["columns"][0]["label"], u"wage")
        self.assertEquals(d["relations"][2]["columns"][1]["nature"], u"foreign_primary_key")
        self.assertEquals(d["relations"][2]["columns"][1]["label"], u"land")
        self.assertEquals(d["relations"][2]["columns"][2]["nature"], u"association_attribute")
        self.assertEquals(d["relations"][2]["columns"][2]["label"], u"thin")
        self.assertEquals(d["relations"][3]["this_relation_name"], u"Read")
        self.assertEquals(d["relations"][3]["columns"][0]["nature"], u"primary_key")
        self.assertEquals(d["relations"][3]["columns"][0]["label"], u"wage")

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
        self.assertEquals(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEquals(d["relations"][0]["this_relation_name"], u"Riot")
        self.assertEquals(d["relations"][0]["columns"][0]["nature"], u"primary_key")
        self.assertEquals(d["relations"][0]["columns"][0]["label"], u"clue")
        self.assertEquals(d["relations"][1]["this_relation_name"], u"Hour")
        self.assertEquals(d["relations"][1]["columns"][0]["nature"], u"strengthening_primary_key")
        self.assertEquals(d["relations"][1]["columns"][0]["label"], u"clue")
        self.assertEquals(d["relations"][1]["columns"][1]["nature"], u"primary_key")
        self.assertEquals(d["relations"][1]["columns"][1]["label"], u"book")
        self.assertEquals(d["relations"][2]["this_relation_name"], u"Poll")
        self.assertEquals(d["relations"][2]["columns"][0]["nature"], u"foreign_primary_key")
        self.assertEquals(d["relations"][2]["columns"][0]["label"], u"mere")
        self.assertEquals(d["relations"][2]["columns"][1]["nature"], u"demoted_foreign_key")
        self.assertEquals(d["relations"][2]["columns"][1]["label"], u"clue")
        self.assertEquals(d["relations"][2]["columns"][2]["nature"], u"demoted_foreign_key")
        self.assertEquals(d["relations"][2]["columns"][2]["label"], u"book")
        self.assertEquals(d["relations"][3]["this_relation_name"], u"Cast")
        self.assertEquals(d["relations"][3]["columns"][0]["nature"], u"primary_key")
        self.assertEquals(d["relations"][3]["columns"][0]["label"], u"mere")
        self.assertEquals(d["relations"][4]["this_relation_name"], u"Army")
        self.assertEquals(d["relations"][4]["columns"][0]["nature"], u"promoting_foreign_key")
        self.assertEquals(d["relations"][4]["columns"][0]["label"], u"fail")
        self.assertEquals(d["relations"][4]["columns"][1]["nature"], u"foreign_primary_key")
        self.assertEquals(d["relations"][4]["columns"][1]["label"], u"mere")
        self.assertEquals(d["relations"][5]["this_relation_name"], u"Busy")
        self.assertEquals(d["relations"][5]["columns"][0]["nature"], u"primary_key")
        self.assertEquals(d["relations"][5]["columns"][0]["label"], u"fail")

    def test_composite_identifier(self):
        clauses = u"""
            GRATTE-CIEL: latitude, _longitude, nom, hauteur, année de construction
        """
        text = u"""
            GRATTE-CIEL (_latitude_, _longitude_, nom, hauteur, année de construction)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEquals(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEquals(d["relations"][0]["columns"][0]["nature"], u"primary_key")
        self.assertEquals(d["relations"][0]["columns"][0]["label"], u"latitude")
        self.assertEquals(d["relations"][0]["columns"][1]["nature"], u"primary_key")
        self.assertEquals(d["relations"][0]["columns"][1]["label"], u"longitude")
    
    def test_reflexive_df(self):
        clauses = u"""
            HOMME: Num. SS, Nom, Prénom
            ENGENDRER, 0N HOMME, 11 HOMME
        """
        text = u"""
            HOMME (_Num. SS_, Nom, Prénom, #Num. SS.1)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEquals(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEquals(d["relations"][0]["columns"][3]["foreign"], True)
        self.assertEquals(d["relations"][0]["columns"][3]["data_type"], None)
        self.assertEquals(d["relations"][0]["columns"][3]["nature"], u"foreign_key")
        self.assertEquals(d["relations"][0]["columns"][3]["attribute"], u"Num. SS")
        self.assertEquals(d["relations"][0]["columns"][3]["primary"], False)
        self.assertEquals(d["relations"][0]["columns"][3]["label"], u"Num. SS.1")
        self.assertEquals(d["relations"][0]["columns"][3]["raw_label"], u"Num. SS")
        self.assertEquals(d["relations"][0]["columns"][3]["association_name"], u"ENGENDRER")
        self.assertEquals(d["relations"][0]["columns"][3]["disambiguation_number"], 1)
        self.assertEquals(d["relations"][0]["columns"][3]["primary_relation_name"], u"HOMME")
        self.assertEquals(d["title"], u"Untitled")

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
        self.assertEquals(d1, d2)
    
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
        self.assertEquals(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEquals(d["relations"][0]["this_relation_name"], u"Personne")
        self.assertEquals(d["relations"][0]["columns"][0]["leg_annotation"], None)
        self.assertEquals(d["relations"][0]["columns"][0]["label"], u"Num. SS")
        self.assertEquals(d["relations"][0]["columns"][1]["leg_annotation"], None)
        self.assertEquals(d["relations"][0]["columns"][1]["label"], u"Nom")
        self.assertEquals(d["relations"][0]["columns"][2]["leg_annotation"], None)
        self.assertEquals(d["relations"][0]["columns"][2]["label"], u"Prénom")
        self.assertEquals(d["relations"][0]["columns"][3]["leg_annotation"], None)
        self.assertEquals(d["relations"][0]["columns"][3]["label"], u"Sexe")
        self.assertEquals(d["relations"][1]["this_relation_name"], u"Engendrer")
        self.assertEquals(d["relations"][1]["columns"][0]["leg_annotation"], u"parent")
        self.assertEquals(d["relations"][1]["columns"][0]["label"], u"Num. SS parent")
        self.assertEquals(d["relations"][1]["columns"][1]["leg_annotation"], u"enfant")
        self.assertEquals(d["relations"][1]["columns"][1]["label"], u"Num. SS enfant")
    
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
        self.assertEquals(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEquals(d["relations"][0]["this_relation_name"], u"Personne")
        self.assertEquals(d["relations"][0]["columns"][0]["leg_annotation"], None)
        self.assertEquals(d["relations"][0]["columns"][0]["label"], u"Num. SS")
        self.assertEquals(d["relations"][0]["columns"][1]["leg_annotation"], None)
        self.assertEquals(d["relations"][0]["columns"][1]["label"], u"Nom")
        self.assertEquals(d["relations"][0]["columns"][2]["leg_annotation"], None)
        self.assertEquals(d["relations"][0]["columns"][2]["label"], u"Prénom")
        self.assertEquals(d["relations"][0]["columns"][3]["leg_annotation"], None)
        self.assertEquals(d["relations"][0]["columns"][3]["label"], u"Sexe")
        self.assertEquals(d["relations"][1]["this_relation_name"], u"Engendrer")
        self.assertEquals(d["relations"][1]["columns"][0]["leg_annotation"], u"Une personne peut avoir un nombre quelconque d\\'enfants.")
        self.assertEquals(d["relations"][1]["columns"][0]["label"], u"Num. SS")
        self.assertEquals(d["relations"][1]["columns"][1]["leg_annotation"], u"Une personne peut avoir un nombre quelconque de parents dans la base.\nRemarque : vous avez peut-être envie de remplacer la cardinalité maximale N par sa valeur réelle, à savoir 2. Cette précision disparaissant lors du passage au relationnel, elle est en général jugée inutile.")
        self.assertEquals(d["relations"][1]["columns"][1]["label"], u"Num. SS.1")

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
        self.assertEquals(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEquals(d["relations"][0]["this_relation_name"], u"CLIENT")
        self.assertEquals(d["relations"][0]["columns"][0]["data_type"], u"varchar(8)")
        self.assertEquals(d["relations"][0]["columns"][0]["label"], u"Réf. client")
        self.assertEquals(d["relations"][0]["columns"][1]["data_type"], u"varchar(20)")
        self.assertEquals(d["relations"][0]["columns"][1]["label"], u"Nom")
        self.assertEquals(d["relations"][0]["columns"][2]["data_type"], u"varchar(40)")
        self.assertEquals(d["relations"][0]["columns"][2]["label"], u"Adresse")
        self.assertEquals(d["relations"][1]["this_relation_name"], u"COMMANDE")
        self.assertEquals(d["relations"][1]["columns"][0]["data_type"], u"tinyint(4)")
        self.assertEquals(d["relations"][1]["columns"][0]["label"], u"Num commande")
        self.assertEquals(d["relations"][1]["columns"][1]["data_type"], u"date")
        self.assertEquals(d["relations"][1]["columns"][1]["label"], u"Date")
        self.assertEquals(d["relations"][1]["columns"][2]["data_type"], u"decimal(5,2) DEFAULT '0.00'")
        self.assertEquals(d["relations"][1]["columns"][2]["label"], u"Montant")
        self.assertEquals(d["relations"][1]["columns"][3]["data_type"], u"varchar(8)")
        self.assertEquals(d["relations"][1]["columns"][3]["label"], u"Réf. client")
        self.assertEquals(d["relations"][2]["this_relation_name"], u"INCLURE")
        self.assertEquals(d["relations"][2]["columns"][0]["data_type"], u"tinyint(4)")
        self.assertEquals(d["relations"][2]["columns"][0]["label"], u"Num commande")
        self.assertEquals(d["relations"][2]["columns"][1]["data_type"], None)
        self.assertEquals(d["relations"][2]["columns"][1]["label"], u"Réf. produit")
        self.assertEquals(d["relations"][2]["columns"][2]["data_type"], u"tinyint(4)")
        self.assertEquals(d["relations"][2]["columns"][2]["label"], u"Quantité")
        self.assertEquals(d["relations"][3]["this_relation_name"], u"PRODUIT")
        self.assertEquals(d["relations"][3]["columns"][0]["data_type"], None)
        self.assertEquals(d["relations"][3]["columns"][0]["label"], u"Réf. produit")
        self.assertEquals(d["relations"][3]["columns"][1]["data_type"], None)
        self.assertEquals(d["relations"][3]["columns"][1]["label"], u"Libellé")
        self.assertEquals(d["relations"][3]["columns"][2]["data_type"], None)
        self.assertEquals(d["relations"][3]["columns"][2]["label"], u"Prix unitaire")

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
        self.assertEquals(d1, d2)

    def test_empty_attributes(self):
        clauses = u"""
            CLIENT: Réf. client, , , 
        """
        text = u"""
            CLIENT (_Réf. client_, , .1, .2)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEquals(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEquals(d["relations"][0]["columns"][1]["attribute"], u"")
        self.assertEquals(d["relations"][0]["columns"][1]["raw_label"], u"")
        self.assertEquals(d["relations"][0]["columns"][1]["label"], u"")
        self.assertEquals(d["relations"][0]["columns"][1]["disambiguation_number"], None)
        self.assertEquals(d["relations"][0]["columns"][2]["attribute"], u"")
        self.assertEquals(d["relations"][0]["columns"][2]["raw_label"], u"")
        self.assertEquals(d["relations"][0]["columns"][2]["label"], u".1")
        self.assertEquals(d["relations"][0]["columns"][2]["disambiguation_number"], 1)

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
        self.assertEquals(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEquals(d["relations"][1]["this_relation_name"], u"LIGULA")
        self.assertEquals(d["relations"][1]["columns"][0]["nature"], u"foreign_primary_key")
        self.assertEquals(d["relations"][1]["columns"][0]["primary_relation_name"], u"LACUS")
        self.assertEquals(d["relations"][1]["columns"][1]["nature"], u"demoted_foreign_key")
        self.assertEquals(d["relations"][1]["columns"][1]["primary_relation_name"], u"EROS")
        self.assertEquals(d["relations"][1]["columns"][2]["nature"], u"foreign_primary_key")
        self.assertEquals(d["relations"][1]["columns"][2]["primary_relation_name"], u"TELLUS")
        self.assertEquals(d["relations"][1]["columns"][3]["nature"], u"association_attribute")
        self.assertEquals(d["relations"][1]["columns"][3]["primary_relation_name"], None)

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
        self.assertEquals(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEquals(d["relations"][1]["this_relation_name"], u"LIGULA")
        self.assertEquals(d["relations"][1]["columns"][0]["nature"], u"foreign_primary_key")
        self.assertEquals(d["relations"][1]["columns"][0]["primary_relation_name"], u"LACUS")
        self.assertEquals(d["relations"][1]["columns"][1]["nature"], u"promoting_foreign_key")
        self.assertEquals(d["relations"][1]["columns"][1]["primary_relation_name"], u"EROS")
        self.assertEquals(d["relations"][1]["columns"][2]["nature"], u"association_attribute")
        self.assertEquals(d["relations"][1]["columns"][2]["primary_relation_name"], None)
    
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
        self.assertEquals(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEquals(d["relations"][3]["this_relation_name"], u"Appartement")
        self.assertEquals(d["relations"][3]["columns"][0]["attribute"], u"code rue")
        self.assertEquals(d["relations"][3]["columns"][0]["label"], u"code rue")
        self.assertEquals(d["relations"][3]["columns"][0]["raw_label"], u"code rue")
        self.assertEquals(d["relations"][3]["columns"][0]["foreign"], True)
        self.assertEquals(d["relations"][3]["columns"][0]["primary"], True)
        self.assertEquals(d["relations"][3]["columns"][0]["nature"], u"strengthening_primary_key")
        self.assertEquals(d["relations"][3]["columns"][0]["association_name"], u"Composer")
        self.assertEquals(d["relations"][3]["columns"][0]["primary_relation_name"], u"Étage")
        
        self.assertEquals(d["relations"][3]["columns"][1]["attribute"], u"num immeuble")
        self.assertEquals(d["relations"][3]["columns"][1]["label"], u"num immeuble")
        self.assertEquals(d["relations"][3]["columns"][1]["raw_label"], u"num immeuble")
        self.assertEquals(d["relations"][3]["columns"][1]["foreign"], True)
        self.assertEquals(d["relations"][3]["columns"][1]["primary"], True)
        self.assertEquals(d["relations"][3]["columns"][1]["nature"], u"strengthening_primary_key")
        self.assertEquals(d["relations"][3]["columns"][1]["association_name"], u"Composer")
        self.assertEquals(d["relations"][3]["columns"][1]["primary_relation_name"], u"Étage")
        
        self.assertEquals(d["relations"][3]["columns"][2]["attribute"], u"num étage")
        self.assertEquals(d["relations"][3]["columns"][2]["label"], u"num étage")
        self.assertEquals(d["relations"][3]["columns"][2]["raw_label"], u"num étage")
        self.assertEquals(d["relations"][3]["columns"][2]["foreign"], True)
        self.assertEquals(d["relations"][3]["columns"][2]["primary"], True)
        self.assertEquals(d["relations"][3]["columns"][2]["nature"], u"strengthening_primary_key")
        self.assertEquals(d["relations"][3]["columns"][2]["association_name"], u"Composer")
        self.assertEquals(d["relations"][3]["columns"][2]["primary_relation_name"], u"Étage")
        
        self.assertEquals(d["relations"][3]["columns"][3]["attribute"], u"num appart.")
        self.assertEquals(d["relations"][3]["columns"][3]["label"], u"num appart.")
        self.assertEquals(d["relations"][3]["columns"][3]["raw_label"], u"num appart.")
        self.assertEquals(d["relations"][3]["columns"][3]["foreign"], False)
        self.assertEquals(d["relations"][3]["columns"][3]["primary"], True)
        self.assertEquals(d["relations"][3]["columns"][3]["nature"], u"primary_key")
        self.assertEquals(d["relations"][3]["columns"][3]["association_name"], None)
        self.assertEquals(d["relations"][3]["columns"][3]["primary_relation_name"], None)
        
        self.assertEquals(d["relations"][3]["columns"][4]["attribute"], u"nb pièces appart.")
        self.assertEquals(d["relations"][3]["columns"][4]["label"], u"nb pièces appart.")
        self.assertEquals(d["relations"][3]["columns"][4]["raw_label"], u"nb pièces appart.")
        self.assertEquals(d["relations"][3]["columns"][4]["foreign"], False)
        self.assertEquals(d["relations"][3]["columns"][4]["primary"], False)
        self.assertEquals(d["relations"][3]["columns"][4]["nature"], u"normal_attribute")
        self.assertEquals(d["relations"][3]["columns"][4]["association_name"], None)
        self.assertEquals(d["relations"][3]["columns"][4]["primary_relation_name"], None)
        self.assertEquals(d["title"], u"Untitled")
    
    def test_weak_entities_strengthened_by_itself(self):
        clauses = u"""
            SCELERISQUE: blandit, elit
            DF, _11 SCELERISQUE, 1N SCELERISQUE
        """
        mcd = Mcd(clauses.split("\n"), params)
        self.assertRaisesRegexp(RuntimeError, "Err\.16", Relations, mcd, params)
    
    def test_weak_entities_with_cycle(self):
        clauses = u"""
            ITEM: norm, wash, haul
            MILK, _11 ITEM, 1N DRAW: lady, face

            SOON, 1N ITEM, _11 DRAW
            DRAW: ever, unit, tour, fold
        """
        mcd = Mcd(clauses.split("\n"), params)
        self.assertRaisesRegexp(RuntimeError, "Err\.17", Relations, mcd, params)
    
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
        self.assertEquals(t.get_text(template), text)
        my_json_template = deepcopy(json_template)
        my_json_template.update(template)
        d = json.loads(t.get_text(my_json_template))
        self.assertEquals(d["relations"][0]["this_relation_name"], u"Chien")
        self.assertEquals(d["relations"][0]["columns"][0]["attribute"], u"num. chien")
        self.assertEquals(d["relations"][0]["columns"][0]["raw_label"], u"num_chien")
        self.assertEquals(d["relations"][0]["columns"][0]["label"],     u"num_chien")
        self.assertEquals(d["relations"][0]["columns"][4]["attribute"], u"num. chien")
        self.assertEquals(d["relations"][0]["columns"][4]["raw_label"], u"num_chien")
        self.assertEquals(d["relations"][0]["columns"][4]["label"],     u"num_mère")
        self.assertEquals(d["relations"][1]["this_relation_name"], u"A pour père présumé")
        self.assertEquals(d["relations"][1]["columns"][1]["attribute"], u"num. chien")
        self.assertEquals(d["relations"][1]["columns"][1]["raw_label"], u"num_chien")
        self.assertEquals(d["relations"][1]["columns"][1]["label"],     u"num_père")
    
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
        self.assertEquals(t.get_text(template), text)
        my_json_template = deepcopy(json_template)
        my_json_template.update(template)
        d = json.loads(t.get_text(my_json_template))
        self.assertEquals(d["relations"][0]["this_relation_name"], u"Chien")
        self.assertEquals(d["relations"][0]["columns"][0]["attribute"], u"num. chien")
        self.assertEquals(d["relations"][0]["columns"][0]["raw_label"], u"num_chien")
        self.assertEquals(d["relations"][0]["columns"][0]["label"],     u"num_chien")
        self.assertEquals(d["relations"][0]["columns"][4]["attribute"], u"num. chien")
        self.assertEquals(d["relations"][0]["columns"][4]["raw_label"], u"num_chien")
        self.assertEquals(d["relations"][0]["columns"][4]["label"],     u"num_chien_1")
        self.assertEquals(d["relations"][1]["this_relation_name"], u"A pour père présumé")
        self.assertEquals(d["relations"][1]["columns"][1]["attribute"], u"num. chien")
        self.assertEquals(d["relations"][1]["columns"][1]["raw_label"], u"num_chien")
        self.assertEquals(d["relations"][1]["columns"][1]["label"],     u"num_chien_1")


if __name__ == '__main__':
    unittest.main()
