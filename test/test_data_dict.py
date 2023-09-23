import re
import unittest

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.common import Common
from mocodo.convert import _data_dict as data_dict

class TestDataDict(unittest.TestCase):

    def test_data_dict(self):
        source = """
            CLIENT: Réf. client [varchar(8)], Nom, Adresse [varchar(40)]
            DF, 0N CLIENT, 11 COMMANDE
            COMMANDE: Num commande [tinyint(4)], Date [date], Montant [decimal(5,2) DEFAULT '0.00']
            INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité [tinyint(4)]
            PRODUIT: Réf. produit [varchar(8)], Libellé [varchar(20)], Prix unitaire [decimal(5,2)]
        """
        params = {"language": "fr"}
        common = Common(params)

        # Markdown table with two columns

        subargs ={
            "label": "Libellé des attributs",
            "type": "Type de données",
            "md": True,
        }
        actual = data_dict.run(source, common=common, subargs=subargs)["text"]
        expected = """
            | Libellé des attributs | Type de données             |
            |:----------------------|:----------------------------|
            | Adresse               | varchar(40)                 |
            | Date                  | date                        |
            | Libellé               | varchar(20)                 |
            | Montant               | decimal(5,2) DEFAULT '0.00' |
            | Nom                   |                             |
            | Num commande          | tinyint(4)                  |
            | Prix unitaire         | decimal(5,2)                |
            | Quantité              | tinyint(4)                  |
            | Réf. client           | varchar(8)                  |
            | Réf. produit          | varchar(8)                  |
        """
        self.assertEqual(actual.strip(), re.sub("(?m)^ +", "", expected).strip())

        # Markdown table with 3 columns in another order and a Markdown emphasis

        subargs ={
            "**box**": "Entité ou association",
            "type": "Type",
            "label": "", # omitted translation => default to a language-dependent one
            "md": True,
        }
        actual = data_dict.run(source, common=common, subargs=subargs)["text"]
        expected = """
            | **Entité ou association** | Type                        | Libellé de l'attribut |
            |:--------------------------|:----------------------------|:----------------------|
            | **CLIENT**                |                             | Nom                   |
            | **"**                     | varchar(40)                 | Adresse               |
            | **"**                     | varchar(8)                  | Réf. client           |
            | **COMMANDE**              | date                        | Date                  |
            | **"**                     | decimal(5,2) DEFAULT '0.00' | Montant               |
            | **"**                     | tinyint(4)                  | Num commande          |
            | **INCLURE**               | tinyint(4)                  | Quantité              |
            | **PRODUIT**               | decimal(5,2)                | Prix unitaire         |
            | **"**                     | varchar(20)                 | Libellé               |
            | **"**                     | varchar(8)                  | Réf. produit          |
        """
        self.assertEqual(actual.strip(), re.sub("(?m)^ +", "", expected).strip())

        # With just one column, the table is converted to a list and the header is omitted

        subargs = {"md": True, "label": ""}
        actual = data_dict.run(source, common=common, subargs=subargs)["text"]
        expected = """
            - Adresse
            - Date
            - Libellé
            - Montant
            - Nom
            - Num commande
            - Prix unitaire
            - Quantité
            - Réf. client
            - Réf. produit
        """
        self.assertEqual(actual.strip(), re.sub("(?m)^ +", "", expected).strip())

        # By default: md,box,label,type

        subargs = {"tsv": True}
        actual = data_dict.run(source, common=common, subargs=subargs)["text"]
        expected = """
            Entité ou association\tLibellé de l'attribut\tType
            CLIENT\tAdresse\tvarchar(40)
            CLIENT\tNom\t
            CLIENT\tRéf. client\tvarchar(8)
            COMMANDE\tDate\tdate
            COMMANDE\tMontant\tdecimal(5,2) DEFAULT '0.00'
            COMMANDE\tNum commande\ttinyint(4)
            INCLURE\tQuantité\ttinyint(4)
            PRODUIT\tLibellé\tvarchar(20)
            PRODUIT\tPrix unitaire\tdecimal(5,2)
            PRODUIT\tRéf. produit\tvarchar(8)
        """
        self.assertEqual(actual.strip(), re.sub("(?m)^ +", "", expected).strip())

    def test_data_dict_with_invisible_boxes(self):
        source = """
            CLIENT: Réf. client, Nom, Prénom, Adresse
            -Reflexive 6_, 11 COMMANDE, 01 COMMANDE
            -Entity 7_: id 7 1, _id 7 2, attr 7 3, attr 7 4
            -Reflexive 13_, 11 PRODUIT, 1N PRODUIT

            DF, 0N CLIENT, 11 COMMANDE
            COMMANDE: Num. commande, Date, Montant
            -Ternary 8_, 0N Entity 7_, 0N COMMANDE, 1N PRODUIT
            PRODUIT: Réf. produit, Libellé, Prix unitaire

            -Entity 14_: id 14 1, attr 14 2, attr 14 3, attr 14 4
            -Binary 15_, 0N Entity 14_, 01 Entity 11_
            INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité
            -Binary 10_, 1N Entity 9_, 1N PRODUIT: attr 10 1

            -Binary 16_, 0N Entity 14_, 1N Entity 11_
            -Entity 11_: id 11 1, attr 11 2
            -Binary 12_, 0N Entity 11_, 11 Entity 9_: attr 12 1
            -Entity 9_: id 9 1, attr 9 2, attr 9 3
        """
        params = {"language": "fr"}
        common = Common(params)
        actual = data_dict.run(source, common=common, subargs={})["text"]
        expected = """
            | Entité ou association | Libellé de l'attribut | Type |
            |:----------------------|:----------------------|:-----|
            | CLIENT                | Adresse               |      |
            | "                     | Nom                   |      |
            | "                     | Prénom                |      |
            | "                     | Réf. client           |      |
            | COMMANDE              | Date                  |      |
            | "                     | Montant               |      |
            | "                     | Num. commande         |      |
            | INCLURE               | Quantité              |      |
            | PRODUIT               | Libellé               |      |
            | "                     | Prix unitaire         |      |
            | "                     | Réf. produit          |      |
        """
        self.assertEqual(actual.strip(), re.sub("(?m)^ +", "", expected).strip())


if __name__ == '__main__':
    unittest.main()
