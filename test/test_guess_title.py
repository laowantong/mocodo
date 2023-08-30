import unittest

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.guess_title import guess_title

class TestDumps(unittest.TestCase):

    def test_guess_title(self):
        # The central entity is the most referenced one
        source = """
            CLIENT: Réf. client, Nom, Prénom, Adresse
            PASSER, 0N CLIENT, 11 COMMANDE
            COMMANDE: Num commande, Date, Montant
            INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité
            PRODUIT: Réf. produit, Libellé, Prix unitaire
        """
        actual = guess_title(source, "fr")
        self.assertEqual(actual, "Commandes")
        # A more intricate case
        source = """
            AYANT-DROIT: nom ayant-droit, lien
            DIRIGER, 0N EMPLOYÉ, 01 PROJET
            REQUÉRIR, 1N PROJET, 0N PIÈCE: qté requise
            PIÈCE: réf. pièce, libellé pièce
            COMPOSER, 0N [composée] PIÈCE, 0N [composante] PIÈCE: quantité

            DF, _11 AYANT-DROIT, 0N EMPLOYÉ
            EMPLOYÉ: matricule, nom employé
            PROJET: num. projet, nom projet
            FOURNIR, 1N PROJET, 1N PIÈCE, 1N SOCIÉTÉ: qté fournie

            DÉPARTEMENT: num. département, nom département
            EMPLOYER, 11 EMPLOYÉ, 1N DÉPARTEMENT
            TRAVAILLER, 0N EMPLOYÉ, 1N PROJET
            SOCIÉTÉ: num. société, raison sociale
            CONTRÔLER, 0N< [filiale] SOCIÉTÉ, 01 [mère] SOCIÉTÉ
        """
        actual = guess_title(source, "fr")
        self.assertEqual(actual, "Employés")
        # A case showing that the numeric suffix is ignored
        source = """
            Egestas: vivamus, semper, aliquam
            Lorem1: ipsum
            Pharetra, 0N Curabitur, 0N Lorem1, 0N Vitae justo: massa
            Vitae justo: lobortis, purus

            Ultricies, 11 Rhoncus, 0N Egestas
            Imperdiet, 0N Egestas, 0N Curabitur, 0N Lorem1
            Curabitur: blandit, suscipit
            adipiscing, 0N Curabitur, 0N Vitae justo, 0N Lorem2

            Rhoncus: dolor a, bibendum, euismod, consectetuer, leo
            Porttitor, 1N Rhoncus, 0N Lorem2
            Lorem2: dolor
        """
        actual = guess_title(source, "fr")
        self.assertEqual(actual, "Lorems")
        # When the most referenced entity is a date,
        # the second most referenced entity is chosen.
        source = source.replace("Lorem", "Date")
        actual = guess_title(source, "fr")
        self.assertEqual(actual, "Curabiturs")

if __name__ == '__main__':
    unittest.main()
