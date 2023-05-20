from pathlib import Path
import unittest

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.transformers import obfuscate, fix_cardinalities, markdown_data_dict, asciify_source
from mocodo.argument_parser import parsed_arguments

class TestTransformers(unittest.TestCase):

    def test_obfuscate(self):
        source = """
            AYANT-DROIT: nom ayant-droit, lien
            DIRIGER, 0N EMPLOYÉ, 01 PROJET
            REQUÉRIR, 1N PROJET, 0N PIÈCE: qté requise
            PIÈCE: réf. pièce, libellé pièce
            COMPOSER, 0N [composée] PIÈCE, 0N [composante] PIÈCE: quantité

            DF1, _11 AYANT-DROIT, 0N EMPLOYÉ
            EMPLOYÉ: matricule, nom employé
            PROJET: num. projet, nom projet
            FOURNIR, 1N PROJET, 1N PIÈCE, 1N SOCIÉTÉ: qté fournie

            DÉPARTEMENT: num. département, nom département
            EMPLOYER, 11 EMPLOYÉ, 1N DÉPARTEMENT
            TRAVAILLER, 0N EMPLOYÉ, 1N PROJET
            SOCIÉTÉ: num. société, raison sociale
            CONTRÔLER, 0N< [filiale] SOCIÉTÉ, 01 [mère] SOCIÉTÉ

            (I) [Les pièces fournies par une société pour un projet font partie de celles qu'il requiert.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET
        """
        params = parsed_arguments()
        params["obfuscate"] = "four_letter_words.txt"
        params["seed"] = 42
        actual = obfuscate(source, params)
        expected = """
            FEEL: turn, grin
            LAND, 0N NEAR, 01 SILK
            DEBT, 1N SILK, 0N SHOE: loss
            SHOE: poet, stir
            AUTO, 0N [composée] SHOE, 0N [composante] SHOE: slew

            TAPE1, _11 FEEL, 0N NEAR
            NEAR: knee, code
            SILK: they, bath
            UNIT, 1N SILK, 1N SHOE, 1N HAUL: draw

            FOUR: duck, icon
            GOLF, 11 NEAR, 1N FOUR
            SNAP, 0N NEAR, 1N SILK
            HAUL: clip, area
            CALM, 0N< [filiale] HAUL, 01 [mère] HAUL

            (I) [Les pièces fournies par une société pour un projet font partie de celles qu'il requiert.] ..SHOE, ->DEBT, --UNIT, SILK
        """
        self.assertEqual(actual.strip(), expected.strip())
    
    def test_fix_cardinalities(self):
        source = "A, ON B, No No"
        actual = fix_cardinalities(source).strip()
        expected = "A, 0N B, 0N No"
        self.assertEqual(actual, expected)

    def test_markdown_data_dict_as_table(self):
        source = """
            CLIENT: Réf. client [varchar(8)], Nom [varchar(20)], Adresse [varchar(40)]
            DF, 0N CLIENT, 11 COMMANDE
            COMMANDE: Num commande [tinyint(4)], Date [date], Montant [decimal(5,2) DEFAULT '0.00']
            INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité [tinyint(4)]
            PRODUIT: Réf. produit [varchar(8)], Libellé [varchar(20)], Prix unitaire [decimal(5,2)]
        """
        actual = markdown_data_dict(source)
        expected = """
            | Attribut | Informations |
            |:---|:---|
            | Adresse | varchar(40) |
            | Date | date |
            | Libellé | varchar(20) |
            | Montant | decimal(5,2) DEFAULT '0.00' |
            | Nom | varchar(20) |
            | Num commande | tinyint(4) |
            | Prix unitaire | decimal(5,2) |
            | Quantité | tinyint(4) |
            | Réf. client | varchar(8) |
            | Réf. produit | varchar(8) |
        """
        self.assertEqual(actual.strip(), expected.replace("    ", "").strip())

    def test_markdown_data_dict_as_items(self):
        source = """
            CLIENT: Réf. client, Nom, Prénom, Adresse
            PASSER, 0N CLIENT, 11 COMMANDE
            COMMANDE: Num commande, Date, Montant
            INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité [nombre d'unités d'un produit donné dans une commande donnée]
            PRODUIT: Réf. produit, Libellé, Prix unitaire
        """
        actual = markdown_data_dict(source)
        expected = """
            - Adresse
            - Date
            - Libellé
            - Montant
            - Nom
            - Num commande
            - Prix unitaire
            - Prénom
            - Quantité : _nombre d'unités d'un produit donné dans une commande donnée_
            - Réf. client
            - Réf. produit
        """
        self.assertEqual(actual.strip(), expected.replace("    ", "").strip())

    def test_asciify_source(self):
        source = """
            AYANT-DROIT: nom ayant-droit, lien
            DIRIGER, 0N EMPLOYÉ, 01 PROJET
            REQUÉRIR, 1N PROJET, 0N PIÈCE: qté requise
            PIÈCE: réf. pièce, libellé pièce
            COMPOSER, 0N [composée] PIÈCE, 0N [composante] PIÈCE: quantité

            DF1, _11 AYANT-DROIT, 0N EMPLOYÉ
            EMPLOYÉ: matricule, nom employé
            PROJET: num. projet, nom projet
            FOURNIR, 1N PROJET, 1N PIÈCE, 1N SOCIÉTÉ: qté fournie

            DÉPARTEMENT: num. département, nom département
            EMPLOYER, 11 EMPLOYÉ, 1N DÉPARTEMENT
            TRAVAILLER, 0N EMPLOYÉ, 1N PROJET
            SOCIÉTÉ: num. société, raison sociale
            CONTRÔLER, 0N< [filiale] SOCIÉTÉ, 01 [mère] SOCIÉTÉ

            (I) [Les pièces fournies par une société pour un projet font partie de celles qu'il requiert.] ..PIÈCE, ->REQUÉRIR, --FOURNIR, PROJET
        """
        actual = asciify_source(source)
        expected = """
            AYANT_DROIT: nom_ayant_droit, lien
            DIRIGER, 0N EMPLOYE, 01 PROJET
            REQUERIR, 1N PROJET, 0N PIECE: qte_requise
            PIECE: ref_piece, libelle_piece
            COMPOSER, 0N [composee] PIECE, 0N [composante] PIECE: quantite

            DF1, _11 AYANT_DROIT, 0N EMPLOYE
            EMPLOYE: matricule, nom_employe
            PROJET: num_projet, nom_projet
            FOURNIR, 1N PROJET, 1N PIECE, 1N SOCIETE: qte_fournie

            DEPARTEMENT: num_departement, nom_departement
            EMPLOYER, 11 EMPLOYE, 1N DEPARTEMENT
            TRAVAILLER, 0N EMPLOYE, 1N PROJET
            SOCIETE: num_societe, raison_sociale
            CONTROLER, 0N< [filiale] SOCIETE, 01 [mere] SOCIETE

            (I) [Les pièces fournies par une société pour un projet font partie de celles qu'il requiert.] ..PIECE, ->REQUERIR, --FOURNIR, PROJET
        """
        self.assertEqual(actual.strip(), expected.strip())

if __name__ == '__main__':
    unittest.main()
