import json
import unittest
from copy import deepcopy

__import__("sys").path[0:0] = ["mocodo"]
from mocodo.argument_parser import parsed_arguments
from mocodo.file_helpers import read_contents
from mocodo.mcd import Mcd
from mocodo.relations import *


minimal_template = json.loads(read_contents("mocodo/resources/relation_templates/text.json"))
json_template = json.loads(read_contents("mocodo/resources/relation_templates/json.json"))
params = parsed_arguments()
params["title"] = "Untitled"
params["guess_title"] = False

class relationsTest(unittest.TestCase):
    
    def test_character_cases(self):
        clauses = """
            Riot: clue
            Into, 11 Form, 1N Riot: goat
            Form: land, hide
            Tuck, 1N Read, 1N Form: thin
            Read: wage
        """
        text = """
            Form (_land_, hide, #clue, goat)
            Read (_wage_)
            Riot (_clue_)
            Tuck (_#wage_, _#land_, thin)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["title"], "Untitled")
        self.assertEqual(d["title_titlecase"], "Untitled")
        self.assertEqual(d["title_lowercase"], "untitled")
        self.assertEqual(d["title_uppercase"], "UNTITLED")
        self.assertEqual(d["relations"][0]["columns"][2]["association_name_titlecase"], "Into")
        self.assertEqual(d["relations"][0]["columns"][2]["association_name_uppercase"], "INTO")
        self.assertEqual(d["relations"][0]["columns"][2]["association_name"], "Into")
        self.assertEqual(d["relations"][0]["columns"][2]["outer_source_lowercase"], "riot")
        self.assertEqual(d["relations"][0]["columns"][2]["outer_source_titlecase"], "Riot")
        self.assertEqual(d["relations"][0]["columns"][2]["outer_source_uppercase"], "RIOT")
        self.assertEqual(d["relations"][0]["columns"][2]["outer_source"], "Riot")
        self.assertEqual(d["relations"][0]["columns"][3]["association_name_lower_case"], "into")
        self.assertEqual(d["relations"][2]["this_relation_name_lowercase"], "riot")
        self.assertEqual(d["relations"][2]["this_relation_name_titlecase"], "Riot")
        self.assertEqual(d["relations"][2]["this_relation_name_uppercase"], "RIOT")
        self.assertEqual(d["relations"][2]["this_relation_name"], "Riot")
        self.assertEqual(d["relations"][2]["columns"][0]["association_name_lower_case"], None)
        self.assertEqual(d["relations"][2]["columns"][0]["association_name_titlecase"], None)
        self.assertEqual(d["relations"][2]["columns"][0]["association_name_uppercase"], None)
        self.assertEqual(d["relations"][2]["columns"][0]["association_name"], None)
        self.assertEqual(d["relations"][2]["columns"][0]["attribute"], "clue")
        self.assertEqual(d["relations"][2]["columns"][0]["label_lowercase"], "clue")
        self.assertEqual(d["relations"][2]["columns"][0]["label_titlecase"], "Clue")
        self.assertEqual(d["relations"][2]["columns"][0]["label_uppercase"], "CLUE")
        self.assertEqual(d["relations"][2]["columns"][0]["label"], "clue")
        self.assertEqual(d["relations"][2]["columns"][0]["outer_source_lowercase"], None)
        self.assertEqual(d["relations"][2]["columns"][0]["outer_source_titlecase"], None)
        self.assertEqual(d["relations"][2]["columns"][0]["outer_source_uppercase"], None)
        self.assertEqual(d["relations"][2]["columns"][0]["outer_source"], None)
        self.assertEqual(d["relations"][2]["columns"][0]["raw_label_lowercase"], "clue")
        self.assertEqual(d["relations"][2]["columns"][0]["raw_label_titlecase"], "Clue")
        self.assertEqual(d["relations"][2]["columns"][0]["raw_label_uppercase"], "CLUE")
        self.assertEqual(d["relations"][2]["columns"][0]["raw_label"], "clue")

    def test_attribute_nature_simple(self):
        clauses = """
            Riot: clue
            Into, 11 Form, 1N Riot: goat
            Form: land, hide
            Tuck, 1N Read, 1N Form: thin
            Read: wage
        """
        t = Relations(Mcd(clauses.split("\n"), params), params)
        text = """
            Form (_land_, hide, #clue, goat)
            Read (_wage_)
            Riot (_clue_)
            Tuck (_#wage_, _#land_, thin)
        """.strip().replace("    ", "")
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["this_relation_name"], "Form")
        self.assertEqual(d["relations"][0]["columns"][0]["label"], "land")
        self.assertEqual(d["relations"][0]["columns"][0]["nature"], "primary_key")
        self.assertEqual(d["relations"][0]["columns"][1]["label"], "hide")
        self.assertEqual(d["relations"][0]["columns"][1]["nature"], "normal_attribute")
        self.assertEqual(d["relations"][0]["columns"][2]["label"], "clue")
        self.assertEqual(d["relations"][0]["columns"][2]["nature"], "foreign_key")
        self.assertEqual(d["relations"][0]["columns"][3]["label"], "goat")
        self.assertEqual(d["relations"][0]["columns"][3]["nature"], "outer_attribute")
        self.assertEqual(d["relations"][1]["this_relation_name"], "Read")
        self.assertEqual(d["relations"][1]["columns"][0]["label"], "wage")
        self.assertEqual(d["relations"][1]["columns"][0]["nature"], "primary_key")
        self.assertEqual(d["relations"][2]["this_relation_name"], "Riot")
        self.assertEqual(d["relations"][2]["columns"][0]["label"], "clue")
        self.assertEqual(d["relations"][2]["columns"][0]["nature"], "primary_key")
        self.assertEqual(d["relations"][3]["this_relation_name"], "Tuck")
        self.assertEqual(d["relations"][3]["columns"][0]["label"], "wage")
        self.assertEqual(d["relations"][3]["columns"][0]["nature"], "primary_foreign_key")
        self.assertEqual(d["relations"][3]["columns"][1]["label"], "land")
        self.assertEqual(d["relations"][3]["columns"][1]["nature"], "primary_foreign_key")
        self.assertEqual(d["relations"][3]["columns"][2]["label"], "thin")
        self.assertEqual(d["relations"][3]["columns"][2]["nature"], "association_attribute")

    def test_attribute_nature_complex(self):
        clauses = """
            Riot: clue
            Walk, 1N Riot, _11 Hour
            Hour: book
            Poll, 1N Cast, /1N Hour
            Cast: mere
            [Army], 1N Busy, 01 Cast
            Busy: fail
        """
        text = """
            Army (_#mere_, #fail)
            Busy (_fail_)
            Cast (_mere_)
            Hour (_#clue_, _book_)
            Poll (_#mere_, #clue, #book)
            Riot (_clue_)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["this_relation_name"], "Army")
        self.assertEqual(d["relations"][0]["columns"][0]["label"], "mere")
        self.assertEqual(d["relations"][0]["columns"][0]["nature"], "primary_foreign_key")
        self.assertEqual(d["relations"][0]["columns"][1]["label"], "fail")
        self.assertEqual(d["relations"][0]["columns"][1]["nature"], "stopped_foreign_key")
        self.assertEqual(d["relations"][1]["this_relation_name"], "Busy")
        self.assertEqual(d["relations"][1]["columns"][0]["label"], "fail")
        self.assertEqual(d["relations"][1]["columns"][0]["nature"], "primary_key")
        self.assertEqual(d["relations"][2]["this_relation_name"], "Cast")
        self.assertEqual(d["relations"][2]["columns"][0]["label"], "mere")
        self.assertEqual(d["relations"][2]["columns"][0]["nature"], "primary_key")
        self.assertEqual(d["relations"][3]["this_relation_name"], "Hour")
        self.assertEqual(d["relations"][3]["columns"][0]["label"], "clue")
        self.assertEqual(d["relations"][3]["columns"][0]["nature"], "strengthening_primary_key")
        self.assertEqual(d["relations"][3]["columns"][1]["label"], "book")
        self.assertEqual(d["relations"][3]["columns"][1]["nature"], "primary_key")
        self.assertEqual(d["relations"][4]["this_relation_name"], "Poll")
        self.assertEqual(d["relations"][4]["columns"][0]["label"], "mere")
        self.assertEqual(d["relations"][4]["columns"][0]["nature"], "primary_foreign_key")
        self.assertEqual(d["relations"][4]["columns"][1]["label"], "clue")
        self.assertEqual(d["relations"][4]["columns"][1]["nature"], "demoted_foreign_key")
        self.assertEqual(d["relations"][4]["columns"][2]["label"], "book")
        self.assertEqual(d["relations"][4]["columns"][2]["nature"], "demoted_foreign_key")
        self.assertEqual(d["relations"][5]["this_relation_name"], "Riot")
        self.assertEqual(d["relations"][5]["columns"][0]["label"], "clue")
        self.assertEqual(d["relations"][5]["columns"][0]["nature"], "primary_key")

    def test_composite_identifier(self):
        clauses = """
            GRATTE-CIEL: latitude, _longitude, nom, hauteur, année de construction
        """
        text = """
            GRATTE-CIEL (_latitude_, _longitude_, nom, hauteur, année de construction)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["columns"][0]["nature"], "primary_key")
        self.assertEqual(d["relations"][0]["columns"][0]["label"], "latitude")
        self.assertEqual(d["relations"][0]["columns"][1]["nature"], "primary_key")
        self.assertEqual(d["relations"][0]["columns"][1]["label"], "longitude")
    
    def test_reflexive_df(self):
        clauses = """
            HOMME: Num. SS, Nom, Prénom
            ENGENDRER, 0N HOMME, 11 HOMME
        """
        text = """
            HOMME (_Num. SS_, Nom, Prénom, #Num. SS.1)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["columns"][3]["data_type"], None)
        self.assertEqual(d["relations"][0]["columns"][3]["nature"], "foreign_key")
        self.assertEqual(d["relations"][0]["columns"][3]["attribute"], "Num. SS")
        self.assertEqual(d["relations"][0]["columns"][3]["primary"], False)
        self.assertEqual(d["relations"][0]["columns"][3]["label"], "Num. SS.1")
        self.assertEqual(d["relations"][0]["columns"][3]["raw_label"], "Num. SS")
        self.assertEqual(d["relations"][0]["columns"][3]["association_name"], "ENGENDRER")
        self.assertEqual(d["relations"][0]["columns"][3]["disambiguation_number"], 1)
        self.assertEqual(d["relations"][0]["columns"][3]["outer_source"], "HOMME")
        self.assertEqual(d["title"], "Untitled")

    def test_arrows_are_ignored(self):
        clauses = """
            Personne: Num. SS, Nom, Prénom, Sexe
            Engendrer, 0N< Personne, 22> Personne
        """
        t = Relations(Mcd(clauses.split("\n"), params), params)
        d1 = json.loads(t.get_text(json_template))
        clauses = """
            Personne: Num. SS, Nom, Prénom, Sexe
            Engendrer, 0N Personne, 22 Personne
        """
        t = Relations(Mcd(clauses.split("\n"), params), params)
        d2 = json.loads(t.get_text(json_template))
        self.assertEqual(d1, d2)
    
    def test_notes(self):
        clauses = """
            Personne: Num. SS, Nom, Prénom, Sexe
            Engendrer, 0N [parent] Personne, 0N [enfant] Personne
        """
        text = """
            Engendrer (_#Num. SS parent_, _#Num. SS enfant_)
            Personne (_Num. SS_, Nom, Prénom, Sexe)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["this_relation_name"], "Engendrer")
        self.assertEqual(d["relations"][0]["columns"][0]["label"], "Num. SS parent")
        self.assertEqual(d["relations"][0]["columns"][0]["leg_note"], "parent")
        self.assertEqual(d["relations"][0]["columns"][1]["label"], "Num. SS enfant")
        self.assertEqual(d["relations"][0]["columns"][1]["leg_note"], "enfant")
        self.assertEqual(d["relations"][1]["this_relation_name"], "Personne")
        self.assertEqual(d["relations"][1]["columns"][0]["label"], "Num. SS")
        self.assertEqual(d["relations"][1]["columns"][0]["leg_note"], None)
        self.assertEqual(d["relations"][1]["columns"][1]["label"], "Nom")
        self.assertEqual(d["relations"][1]["columns"][1]["leg_note"], None)
        self.assertEqual(d["relations"][1]["columns"][2]["label"], "Prénom")
        self.assertEqual(d["relations"][1]["columns"][2]["leg_note"], None)
        self.assertEqual(d["relations"][1]["columns"][3]["label"], "Sexe")
        self.assertEqual(d["relations"][1]["columns"][3]["leg_note"], None)
    
    def test_notes_with_numbers_only_disambiguation_strategy(self):
        clauses = """
            Personne: Num. SS, Nom, Prénom, Sexe
            Engendrer, 0N [Une personne peut avoir un nombre quelconque d'enfants.] Personne, 0N [Une personne peut avoir un nombre quelconque de parents dans la base. Remarque : vous avez peut-être envie de remplacer la cardinalité maximale N par sa valeur réelle, à savoir 2. Cette précision disparaissant lors du passage au relationnel, elle est en général jugée inutile.] Personne
        """
        text = """
            Engendrer (_#Num. SS_, _#Num. SS.1_)
            Personne (_Num. SS_, Nom, Prénom, Sexe)
        """.strip().replace("    ", "")
        local_params = deepcopy(params)
        local_params["disambiguation"] = "numbers_only"
        t = Relations(Mcd(clauses.split("\n"), local_params), local_params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["this_relation_name"], "Engendrer")
        self.assertEqual(d["relations"][0]["columns"][0]["label"], "Num. SS")
        self.assertEqual(d["relations"][0]["columns"][0]["leg_note"], "Une personne peut avoir un nombre quelconque d'enfants.")
        self.assertEqual(d["relations"][0]["columns"][1]["label"], "Num. SS.1")
        self.assertEqual(d["relations"][0]["columns"][1]["leg_note"], "Une personne peut avoir un nombre quelconque de parents dans la base. Remarque : vous avez peut-être envie de remplacer la cardinalité maximale N par sa valeur réelle, à savoir 2. Cette précision disparaissant lors du passage au relationnel, elle est en général jugée inutile.")
        self.assertEqual(d["relations"][1]["this_relation_name"], "Personne")
        self.assertEqual(d["relations"][1]["columns"][0]["label"], "Num. SS")
        self.assertEqual(d["relations"][1]["columns"][0]["leg_note"], None)
        self.assertEqual(d["relations"][1]["columns"][1]["label"], "Nom")
        self.assertEqual(d["relations"][1]["columns"][1]["leg_note"], None)
        self.assertEqual(d["relations"][1]["columns"][2]["label"], "Prénom")
        self.assertEqual(d["relations"][1]["columns"][2]["leg_note"], None)
        self.assertEqual(d["relations"][1]["columns"][3]["label"], "Sexe")
        self.assertEqual(d["relations"][1]["columns"][3]["leg_note"], None)

    def test_data_types(self):
        clauses = """
            CLIENT: Réf. client [varchar(8)], Nom [varchar(20)], Adresse [varchar(40)]
            DF, 0N CLIENT, 11 COMMANDE
            COMMANDE: Num commande [tinyint(4)], Date [date], Montant [decimal(5,2) DEFAULT '0.00']
            INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité [tinyint(4)]
            PRODUIT: Réf. produit, Libellé, Prix unitaire
        """
        text = """
            CLIENT (_Réf. client_, Nom, Adresse)
            COMMANDE (_Num commande_, Date, Montant, #Réf. client)
            INCLURE (_#Num commande_, _#Réf. produit_, Quantité)
            PRODUIT (_Réf. produit_, Libellé, Prix unitaire)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["this_relation_name"], "CLIENT")
        self.assertEqual(d["relations"][0]["columns"][0]["data_type"], "varchar(8)")
        self.assertEqual(d["relations"][0]["columns"][0]["label"], "Réf. client")
        self.assertEqual(d["relations"][0]["columns"][1]["data_type"], "varchar(20)")
        self.assertEqual(d["relations"][0]["columns"][1]["label"], "Nom")
        self.assertEqual(d["relations"][0]["columns"][2]["data_type"], "varchar(40)")
        self.assertEqual(d["relations"][0]["columns"][2]["label"], "Adresse")
        self.assertEqual(d["relations"][1]["this_relation_name"], "COMMANDE")
        self.assertEqual(d["relations"][1]["columns"][0]["data_type"], "tinyint(4)")
        self.assertEqual(d["relations"][1]["columns"][0]["label"], "Num commande")
        self.assertEqual(d["relations"][1]["columns"][1]["data_type"], "date")
        self.assertEqual(d["relations"][1]["columns"][1]["label"], "Date")
        self.assertEqual(d["relations"][1]["columns"][2]["data_type"], "decimal(5,2) DEFAULT '0.00'")
        self.assertEqual(d["relations"][1]["columns"][2]["label"], "Montant")
        self.assertEqual(d["relations"][1]["columns"][3]["data_type"], "varchar(8)")
        self.assertEqual(d["relations"][1]["columns"][3]["label"], "Réf. client")
        self.assertEqual(d["relations"][2]["this_relation_name"], "INCLURE")
        self.assertEqual(d["relations"][2]["columns"][0]["data_type"], "tinyint(4)")
        self.assertEqual(d["relations"][2]["columns"][0]["label"], "Num commande")
        self.assertEqual(d["relations"][2]["columns"][1]["data_type"], None)
        self.assertEqual(d["relations"][2]["columns"][1]["label"], "Réf. produit")
        self.assertEqual(d["relations"][2]["columns"][2]["data_type"], "tinyint(4)")
        self.assertEqual(d["relations"][2]["columns"][2]["label"], "Quantité")
        self.assertEqual(d["relations"][3]["this_relation_name"], "PRODUIT")
        self.assertEqual(d["relations"][3]["columns"][0]["data_type"], None)
        self.assertEqual(d["relations"][3]["columns"][0]["label"], "Réf. produit")
        self.assertEqual(d["relations"][3]["columns"][1]["data_type"], None)
        self.assertEqual(d["relations"][3]["columns"][1]["label"], "Libellé")
        self.assertEqual(d["relations"][3]["columns"][2]["data_type"], None)
        self.assertEqual(d["relations"][3]["columns"][2]["label"], "Prix unitaire")

    def test_all_cardinalities_other_than_01_and_11_are_treated_as_1N(self):
        clauses = """
            CLIENT: Réf. client, Nom, Prénom, Adresse
            PASSER, XX CLIENT, N1 COMMANDE
            COMMANDE: Num commande, Date, Montant
            INCLURE, 03 COMMANDE, ?? PRODUIT: Quantité
            PRODUIT: Réf. produit, Libellé, Prix unitaire
        """
        t = Relations(Mcd(clauses.split("\n"), params), params)
        d1 = json.loads(t.get_text(json_template))
        clauses = """
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
        clauses = """
            CLIENT: Réf. client, , , 
        """
        text = """
            CLIENT (_Réf. client_, , .1, .2)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["columns"][1]["attribute"], "")
        self.assertEqual(d["relations"][0]["columns"][1]["raw_label"], "")
        self.assertEqual(d["relations"][0]["columns"][1]["label"], "")
        self.assertEqual(d["relations"][0]["columns"][1]["disambiguation_number"], None)
        self.assertEqual(d["relations"][0]["columns"][2]["attribute"], "")
        self.assertEqual(d["relations"][0]["columns"][2]["raw_label"], "")
        self.assertEqual(d["relations"][0]["columns"][2]["label"], ".1")
        self.assertEqual(d["relations"][0]["columns"][2]["disambiguation_number"], 1)

    def test_demoted_foreign_key(self):
        clauses = """
            LACUS: blandit, elit
            LIGULA, 0N LACUS, /1N EROS, 0N TELLUS: metus
            EROS: congue, nibh, tincidunt
            
            TELLUS: integer, odio
        """
        text = """
            EROS (_congue_, nibh, tincidunt)
            LACUS (_blandit_, elit)
            LIGULA (_#blandit_, _#integer_, #congue, metus)
            TELLUS (_integer_, odio)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][2]["this_relation_name"], "LIGULA")
        self.assertEqual(d["relations"][2]["columns"][0]["nature"], "primary_foreign_key")
        self.assertEqual(d["relations"][2]["columns"][0]["outer_source"], "LACUS")
        self.assertEqual(d["relations"][2]["columns"][1]["nature"], "primary_foreign_key")
        self.assertEqual(d["relations"][2]["columns"][1]["outer_source"], "TELLUS")
        self.assertEqual(d["relations"][2]["columns"][2]["nature"], "demoted_foreign_key")
        self.assertEqual(d["relations"][2]["columns"][2]["outer_source"], "EROS")
        self.assertEqual(d["relations"][2]["columns"][3]["nature"], "association_attribute")
        self.assertEqual(d["relations"][2]["columns"][3]["outer_source"], None)

    def test_forced_table(self):
        clauses = """
            LACUS: blandit, elit
            [LIGULA], 01 LACUS, 1N EROS: metus
            EROS: congue, nibh, tincidunt
        """
        text = """
            EROS (_congue_, nibh, tincidunt)
            LACUS (_blandit_, elit)
            LIGULA (_#blandit_, #congue, metus)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][2]["this_relation_name"], "LIGULA")
        self.assertEqual(d["relations"][2]["columns"][0]["nature"], "primary_foreign_key")
        self.assertEqual(d["relations"][2]["columns"][0]["outer_source"], "LACUS")
        self.assertEqual(d["relations"][2]["columns"][1]["nature"], "stopped_foreign_key")
        self.assertEqual(d["relations"][2]["columns"][1]["outer_source"], "EROS")
        self.assertEqual(d["relations"][2]["columns"][2]["nature"], "association_attribute")
        self.assertEqual(d["relations"][2]["columns"][2]["outer_source"], None)

    def test_forced_table_ignored(self):
        clauses = """
            LACUS: blandit, elit
            [LIGULA], 1N LACUS, 1N EROS: metus
            EROS: congue, nibh, tincidunt
        """
        text = """
            EROS (_congue_, nibh, tincidunt)
            LACUS (_blandit_, elit)
            LIGULA (_#blandit_, _#congue_, metus)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][2]["this_relation_name"], "LIGULA")
        self.assertEqual(d["relations"][2]["columns"][0]["nature"], "primary_foreign_key")
        self.assertEqual(d["relations"][2]["columns"][0]["outer_source"], "LACUS")
        self.assertEqual(d["relations"][2]["columns"][1]["nature"], "primary_foreign_key")
        self.assertEqual(d["relations"][2]["columns"][1]["outer_source"], "EROS")
        self.assertEqual(d["relations"][2]["columns"][2]["nature"], "association_attribute")
        self.assertEqual(d["relations"][2]["columns"][2]["outer_source"], None)
    
    def test_weak_entities(self):
        clauses = """
            Rue: code rue, nom rue
            Se situer, 0N Rue, _11 Immeuble
            Immeuble: num immeuble, nb étages immeuble
            Appartenir, 1N Immeuble, _11 Étage
            Étage: num étage, nb appart. étage
            Composer, 0N Étage, _11 Appartement
            Appartement: num appart., nb pièces appart.
        """
        text = """
            Appartement (_#code rue_, _#num immeuble_, _#num étage_, _num appart._, nb pièces appart.)
            Immeuble (_#code rue_, _num immeuble_, nb étages immeuble)
            Rue (_code rue_, nom rue)
            Étage (_#code rue_, _#num immeuble_, _num étage_, nb appart. étage)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["this_relation_name"], "Appartement")
        self.assertEqual(d["relations"][0]["columns"][0]["attribute"], "code rue")
        self.assertEqual(d["relations"][0]["columns"][0]["label"], "code rue")
        self.assertEqual(d["relations"][0]["columns"][0]["raw_label"], "code rue")
        self.assertEqual(d["relations"][0]["columns"][0]["primary"], True)
        self.assertEqual(d["relations"][0]["columns"][0]["nature"], "strengthening_primary_key")
        self.assertEqual(d["relations"][0]["columns"][0]["association_name"], "Composer")
        self.assertEqual(d["relations"][0]["columns"][0]["outer_source"], "Étage")
        
        self.assertEqual(d["relations"][0]["columns"][1]["attribute"], "num immeuble")
        self.assertEqual(d["relations"][0]["columns"][1]["label"], "num immeuble")
        self.assertEqual(d["relations"][0]["columns"][1]["raw_label"], "num immeuble")
        self.assertEqual(d["relations"][0]["columns"][1]["primary"], True)
        self.assertEqual(d["relations"][0]["columns"][1]["nature"], "strengthening_primary_key")
        self.assertEqual(d["relations"][0]["columns"][1]["association_name"], "Composer")
        self.assertEqual(d["relations"][0]["columns"][1]["outer_source"], "Étage")
        
        self.assertEqual(d["relations"][0]["columns"][2]["attribute"], "num étage")
        self.assertEqual(d["relations"][0]["columns"][2]["label"], "num étage")
        self.assertEqual(d["relations"][0]["columns"][2]["raw_label"], "num étage")
        self.assertEqual(d["relations"][0]["columns"][2]["primary"], True)
        self.assertEqual(d["relations"][0]["columns"][2]["nature"], "strengthening_primary_key")
        self.assertEqual(d["relations"][0]["columns"][2]["association_name"], "Composer")
        self.assertEqual(d["relations"][0]["columns"][2]["outer_source"], "Étage")
        
        self.assertEqual(d["relations"][0]["columns"][3]["attribute"], "num appart.")
        self.assertEqual(d["relations"][0]["columns"][3]["label"], "num appart.")
        self.assertEqual(d["relations"][0]["columns"][3]["raw_label"], "num appart.")
        self.assertEqual(d["relations"][0]["columns"][3]["primary"], True)
        self.assertEqual(d["relations"][0]["columns"][3]["nature"], "primary_key")
        self.assertEqual(d["relations"][0]["columns"][3]["association_name"], None)
        self.assertEqual(d["relations"][0]["columns"][3]["outer_source"], None)
        
        self.assertEqual(d["relations"][0]["columns"][4]["attribute"], "nb pièces appart.")
        self.assertEqual(d["relations"][0]["columns"][4]["label"], "nb pièces appart.")
        self.assertEqual(d["relations"][0]["columns"][4]["raw_label"], "nb pièces appart.")
        self.assertEqual(d["relations"][0]["columns"][4]["primary"], False)
        self.assertEqual(d["relations"][0]["columns"][4]["nature"], "normal_attribute")
        self.assertEqual(d["relations"][0]["columns"][4]["association_name"], None)
        self.assertEqual(d["relations"][0]["columns"][4]["outer_source"], None)
        self.assertEqual(d["title"], "Untitled")
    
    def test_reciprocical_relative_entities(self):
        clauses = """
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
        clauses = """
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
        clauses = """
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
        clauses = """
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
        clauses = """
            SCELERISQUE: blandit, elit
            DF, _11 SCELERISQUE, 1N SCELERISQUE
        """
        mcd = Mcd(clauses.split("\n"), params)
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.16", Relations, mcd, params)
    
    def test_weak_entities_strengthened_by_several_entities(self):
        clauses = """
            Baby: Soon
            Yard, _11 Unit, ON Baby: Hall
            
            :
            Unit: Folk, Peer
            
            
            Item: Norm, Wash
            Ever, _11 Unit, 1N Item: Tour
        """
        expected = """
            Baby (_Soon_)
            Item (_Norm_, Wash)
            Unit (_#Norm_, _#Soon_, _Folk_, Peer, Hall, Tour)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertTrue(t.get_text(minimal_template) == expected)
    
    def test_weak_entities_with_cycle(self):
        clauses = """
            ITEM: norm, wash, haul
            MILK, _11 ITEM, 1N DRAW: lady, face

            SOON, 1N ITEM, _11 DRAW
            DRAW: ever, unit, tour, fold
        """
        mcd = Mcd(clauses.split("\n"), params)
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.17", Relations, mcd, params)
    
    def test_difference_between_attribute_raw_label_and_label_with_notes(self):
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
          "compose_label_disambiguated_by_note": "{leg_note}",
        }
        clauses = """
            A pour mère, 01 Chien, 0N [num_mère] Chien
            Chien: num. chien, nom chien, sexe, date naissance
            A pour père présumé, 0N Chien, 0N [num_père] Chien
        """
        text = """
            A pour père présumé (_#num_chien_, _#num_père_)
            Chien (_num_chien_, nom_chien, sexe, date_naissance, #num_mère)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(template), text)
        my_json_template = deepcopy(json_template)
        my_json_template.update(template)
        d = json.loads(t.get_text(my_json_template))
        self.assertEqual(d["relations"][0]["this_relation_name"], "A pour père présumé")
        self.assertEqual(d["relations"][0]["columns"][1]["attribute"], "num. chien")
        self.assertEqual(d["relations"][0]["columns"][1]["label"],     "num_père")
        self.assertEqual(d["relations"][0]["columns"][1]["raw_label"], "num_chien")
        self.assertEqual(d["relations"][1]["this_relation_name"], "Chien")
        self.assertEqual(d["relations"][1]["columns"][0]["attribute"], "num. chien")
        self.assertEqual(d["relations"][1]["columns"][0]["label"],     "num_chien")
        self.assertEqual(d["relations"][1]["columns"][0]["raw_label"], "num_chien")
        self.assertEqual(d["relations"][1]["columns"][4]["attribute"], "num. chien")
        self.assertEqual(d["relations"][1]["columns"][4]["label"],     "num_mère")
        self.assertEqual(d["relations"][1]["columns"][4]["raw_label"], "num_chien")
    
    def test_difference_between_attribute_raw_label_and_label_without_notes(self):
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
          "compose_label_disambiguated_by_number": "{label}_{disambiguation_number}",
        }
        clauses = """
            A pour mère, 01 Chien, 0N Chien
            Chien: num. chien, nom chien, sexe, date naissance
            A pour père présumé, 0N Chien, 0N Chien
        """
        text = """
            A pour père présumé (_#num_chien_, _#num_chien_1_)
            Chien (_num_chien_, nom_chien, sexe, date_naissance, #num_chien_1)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(template), text)
        my_json_template = deepcopy(json_template)
        my_json_template.update(template)
        d = json.loads(t.get_text(my_json_template))
        self.assertEqual(d["relations"][0]["this_relation_name"], "A pour père présumé")
        self.assertEqual(d["relations"][0]["columns"][1]["attribute"], "num. chien")
        self.assertEqual(d["relations"][0]["columns"][1]["label"],     "num_chien_1")
        self.assertEqual(d["relations"][0]["columns"][1]["raw_label"], "num_chien")
        self.assertEqual(d["relations"][1]["this_relation_name"], "Chien")
        self.assertEqual(d["relations"][1]["columns"][0]["attribute"], "num. chien")
        self.assertEqual(d["relations"][1]["columns"][0]["label"],     "num_chien")
        self.assertEqual(d["relations"][1]["columns"][0]["raw_label"], "num_chien")
        self.assertEqual(d["relations"][1]["columns"][4]["attribute"], "num. chien")
        self.assertEqual(d["relations"][1]["columns"][4]["label"],     "num_chien_1")
        self.assertEqual(d["relations"][1]["columns"][4]["raw_label"], "num_chien")
    
    def test_inheritance_leftwards_double_arrow(self):
        clauses = """
            /\ ANIMAL <= CARNIVORE, HERBIVORE
            ANIMAL: animal, poids
            CARNIVORE: quantité viande
            HERBIVORE: plante préférée
        """
        text = """
            ANIMAL (_animal_, poids, CARNIVORE, quantité viande, HERBIVORE, plante préférée)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["columns"][2]["attribute"], "CARNIVORE")
        self.assertEqual(d["relations"][0]["columns"][2]["data_type"], "BOOLEAN")
        self.assertEqual(d["relations"][0]["columns"][2]["nature"], "deleted_child_entity_name")
        self.assertEqual(d["relations"][0]["columns"][3]["attribute"], "quantité viande")
        self.assertEqual(d["relations"][0]["columns"][3]["nature"], "deleted_child_attribute")

    def test_inheritance_leftwards_simple_arrow(self):
        clauses = """
            /\ ANIMAL <- CARNIVORE, HERBIVORE: type
            ANIMAL: animal, poids
            CARNIVORE: quantité viande
            HERBIVORE: plante préférée
        """
        text = """
            ANIMAL (_animal_, poids, type, quantité viande, plante préférée)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["columns"][2]["attribute"], "type")
        self.assertEqual(d["relations"][0]["columns"][2]["nature"], "deleted_child_discriminant_")
        self.assertEqual(d["relations"][0]["columns"][3]["attribute"], "quantité viande")
        self.assertEqual(d["relations"][0]["columns"][3]["nature"], "deleted_child_attribute")

    def test_inheritance_rightwards_simple_arrow(self):
        clauses = """
            /\ ANIMAL -> CARNIVORE, HERBIVORE: type
            ANIMAL: animal, poids
            CARNIVORE: quantité viande
            HERBIVORE: plante préférée
        """
        text = """
            ANIMAL (_animal_, poids, type)
            CARNIVORE (_#animal_, quantité viande)
            HERBIVORE (_#animal_, plante préférée)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["columns"][1]["attribute"], "poids")
        self.assertEqual(d["relations"][0]["columns"][1]["nature"], "normal_attribute")
        self.assertEqual(d["relations"][0]["columns"][2]["attribute"], "type")
        self.assertEqual(d["relations"][0]["columns"][2]["nature"], "deleted_child_discriminant_")
        self.assertEqual(d["relations"][1]["columns"][0]["attribute"], "animal")
        self.assertEqual(d["relations"][1]["columns"][0]["nature"], "parent_primary_key")

    def test_inheritance_rightwards_double_arrow_with_totality(self):
        clauses = """
            /T\ ANIMAL => CARNIVORE, HERBIVORE: type
            ANIMAL: animal, poids
            CARNIVORE: quantité viande
            HERBIVORE: plante préférée
        """
        text = """
            CARNIVORE (_animal_, poids, quantité viande)
            HERBIVORE (_animal_, poids, plante préférée)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["columns"][0]["attribute"], "animal")
        self.assertEqual(d["relations"][0]["columns"][0]["nature"], "deleted_parent_primary_key")
        self.assertEqual(d["relations"][0]["columns"][1]["attribute"], "poids")
        self.assertEqual(d["relations"][0]["columns"][1]["nature"], "deleted_parent_attribute")
        self.assertEqual(d["relations"][0]["columns"][2]["attribute"], "quantité viande")
        self.assertEqual(d["relations"][0]["columns"][2]["nature"], "normal_attribute")

    def test_inheritance_rightwards_double_arrow_without_totality(self):
        clauses = """
            /X\ ANIMAL => CARNIVORE, HERBIVORE: type
            ANIMAL: animal, poids
            CARNIVORE: quantité viande
            HERBIVORE: plante préférée
        """
        mcd = Mcd(clauses.split("\n"), params)
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.25", Relations, mcd, params)

    def test_inheritance_leftwards_simple_arrow_with_right_arrow(self):
        clauses = """
            /\ ANIMAL <-> CARNIVORE, HERBIVORE: type
            ANIMAL: animal, poids
            CARNIVORE: quantité viande
            HERBIVORE: plante préférée
        """
        text = """
            ANIMAL (_animal_, poids, type, quantité viande, plante préférée)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["columns"][2]["attribute"], "type")
        self.assertEqual(d["relations"][0]["columns"][2]["nature"], "deleted_child_discriminant_")
        self.assertEqual(d["relations"][0]["columns"][3]["attribute"], "quantité viande")
        self.assertEqual(d["relations"][0]["columns"][3]["nature"], "deleted_child_attribute")


    def test_inheritance_leftwards_simple_arrow_with_left_arrow(self):
        clauses = """
            /\ ANIMAL <-< CARNIVORE, HERBIVORE: type
            ANIMAL: animal, poids
            CARNIVORE: quantité viande
            HERBIVORE: plante préférée
        """
        text = """
            ANIMAL (_animal_, poids, type, quantité viande, plante préférée)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][0]["columns"][2]["attribute"], "type")
        self.assertEqual(d["relations"][0]["columns"][2]["nature"], "deleted_child_discriminant_")
        self.assertEqual(d["relations"][0]["columns"][3]["attribute"], "quantité viande")
        self.assertEqual(d["relations"][0]["columns"][3]["nature"], "deleted_child_attribute")

    def test_inheritance_with_unique_child(self):
        clauses = """
            CARNIVORE: quantité viande
            /\ ANIMAL -> CARNIVORE: type
            ANIMAL: animal, poids
        """
        text = """
            ANIMAL (_animal_, poids, type)
            CARNIVORE (_#animal_, quantité viande)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
        d = json.loads(t.get_text(json_template))
        self.assertEqual(d["relations"][1]["columns"][0]["attribute"], "animal")
        self.assertEqual(d["relations"][1]["columns"][0]["nature"], "parent_primary_key")

    def test_inheritance_with_distant_leg_note(self):
        clauses = """
            HERBIVORE: plante préférée
            :
            :

            /XT\ ANIMAL => CARNIVORE, HERBIVORE: type alimentation
            ANIMAL: nom, sexe, date naissance, date décès
            A MÈRE, 01 ANIMAL, 0N> [mère] ANIMAL

            CARNIVORE: quantité viande
            :
            :        
        """
        text = """
            CARNIVORE (_nom_, sexe, date naissance, date décès, nom mère, quantité viande)
            HERBIVORE (_nom_, sexe, date naissance, date décès, nom mère, plante préférée)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)
    
    def test_two_same_type_inheritances(self):
        # example from user fduchatea on https://github.com/laowantong/mocodo/issues/64
        clauses = """
            :
            :
            Inscrites :
            :

            :
            UtilisatricesPlus : nom, prénom
            /XT1\ UtilisatricesPlus ->> Inscrites, Abonnées : catégorie
            Abonnées :

            Utilisatrices : idU, email
            /XT2\ Utilisatrices ->> Invitées, UtilisatricesPlus : catégorie
            Invitées : adresseIP
            :
        """
        text = """
            Abonnées ()
            Inscrites ()
            Invitées (_#idU_, adresseIP)
            Utilisatrices (_idU_, email, catégorie)
            UtilisatricesPlus (_#idU_, nom, prénom, catégorie)
        """.strip().replace("    ", "")
        t = Relations(Mcd(clauses.split("\n"), params), params)
        self.assertEqual(t.get_text(minimal_template), text)

if __name__ == '__main__':
    unittest.main()
