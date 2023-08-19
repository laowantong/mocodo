import unittest

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.common import Common
from mocodo.export import _data_dict as data_dict

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
            | Libellé des attributs | Type de données |
            |:---|:---|
            | Adresse | varchar(40) |
            | Date | date |
            | Libellé | varchar(20) |
            | Montant | decimal(5,2) DEFAULT '0.00' |
            | Nom |  |
            | Num commande | tinyint(4) |
            | Prix unitaire | decimal(5,2) |
            | Quantité | tinyint(4) |
            | Réf. client | varchar(8) |
            | Réf. produit | varchar(8) |
        """
        self.assertEqual(actual.strip(), expected.replace("    ", "").strip())

        # Markdown table with 3 columns in another order and a Markdown emphasis

        subargs ={
            "**box**": "Entité ou association",
            "type": "Type",
            "label": "", # omitted translation => default to a language-dependent one
            "md": True,
        }
        actual = data_dict.run(source, common=common, subargs=subargs)["text"]
        expected = """
            | Entité ou association | Type | Libellé |
            |:---|:---|:---|
            | **CLIENT** |  | Nom |
            | **"** | varchar(40) | Adresse |
            | **"** | varchar(8) | Réf. client |
            | **COMMANDE** | date | Date |
            | **"** | decimal(5,2) DEFAULT '0.00' | Montant |
            | **"** | tinyint(4) | Num commande |
            | **INCLURE** | tinyint(4) | Quantité |
            | **PRODUIT** | decimal(5,2) | Prix unitaire |
            | **"** | varchar(20) | Libellé |
            | **"** | varchar(8) | Réf. produit |
        """
        self.assertEqual(actual.strip(), expected.replace("    ", "").strip())

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
        self.assertEqual(actual.strip(), expected.replace("    ", "").strip())

        # By default: label,type,svg

        subargs = {}
        actual = data_dict.run(source, common=common, subargs=subargs)["text"]
        expected = """
            Libellé\tType
            Adresse\tvarchar(40)
            Date\tdate
            Libellé\tvarchar(20)
            Montant\tdecimal(5,2) DEFAULT '0.00'
            Nom\t
            Num commande\ttinyint(4)
            Prix unitaire\tdecimal(5,2)
            Quantité\ttinyint(4)
            Réf. client\tvarchar(8)
            Réf. produit\tvarchar(8)
        """
        self.assertEqual(actual.strip(), expected.replace("    ", "").strip())

if __name__ == '__main__':
    unittest.main()
