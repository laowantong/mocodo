from pathlib import Path
import unittest

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.dump import (
    data_dict,
)

class TestDumps(unittest.TestCase):

    def test_data_dict_md_as_table(self):
        source = """
            CLIENT: Réf. client [varchar(8)], Nom [varchar(20)], Adresse [varchar(40)]
            DF, 0N CLIENT, 11 COMMANDE
            COMMANDE: Num commande [tinyint(4)], Date [date], Montant [decimal(5,2) DEFAULT '0.00']
            INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité [tinyint(4)]
            PRODUIT: Réf. produit [varchar(8)], Libellé [varchar(20)], Prix unitaire [decimal(5,2)]
        """
        actual = data_dict.run(source)
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

    def test_data_dict_md_as_items(self):
        source = """
            CLIENT: Réf. client, Nom, Prénom, Adresse
            PASSER, 0N CLIENT, 11 COMMANDE
            COMMANDE: Num commande, Date, Montant
            INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité [nombre d'unités d'un produit donné dans une commande donnée]
            PRODUIT: Réf. produit, Libellé, Prix unitaire
        """
        actual = data_dict.run(source)
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

if __name__ == '__main__':
    unittest.main()
