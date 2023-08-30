import unittest

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.common import Common
from mocodo.convert._chen import *

params = {"df": "DF"}
common = Common(params)

class TestChen(unittest.TestCase):

    def test111N(self):
        source = """
            Employé: employé
            Travailler, 11 Département, 1N Employé
            Département: département
        """
        actual = run(source, common=common, testing=True)
        expected = """
            [Département] ==N== <Travailler>
            [Employé] ==1== <Travailler>
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test011N(self):
        source = """
            Mer: mer
            Recevoir, 01 Rivière, 1N Mer
            Rivière: rivière
        """
        actual = run(source, common=common, testing=True)
        expected = """
            [Mer] ==1== <Recevoir>
            [Rivière] --N-- <Recevoir>
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test0N1N(self):
        source = """
            PROJET: projet
            REQUÉRIR, 1N PROJET, 0N PIÈCE
            PIÈCE: pièce
            COMPOSER, 0N PIÈCE, 0N PIÈCE
        """
        actual = run(source, common=common, testing=True)
        expected = """
            [PIÈCE] --M-- <COMPOSER>
            [PIÈCE] --M-- <REQUÉRIR>
            [PIÈCE] --N-- <COMPOSER>
            [PROJET] ==N== <REQUÉRIR>
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_110N(self):
        source = """
            Œuvre: œuvre
            DF, 0N Œuvre, _11 Exemplaire
            Exemplaire: exemplaire
        """
        actual = run(source, common=common, testing=True)
        expected = """
            [[Exemplaire]] ==N== <<DF>>
            [Œuvre] --1-- <<DF>>
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_gerund(self):
        source = """
            Produit: produit
            DF, _11 Ligne de commande, 0N Produit
            Ligne de commande: _quantité
            DF, _11 Ligne de commande, 1N Commande
            Commande: commande
        """
        actual = run(source, common=common, testing=True)
        expected = """
            [<Ligne de commande>] ==N== <<DF>>
            [<Ligne de commande>] ==N== <<DF>>
            [Commande] ==1== <<DF>>
            [Produit] --1-- <<DF>>
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_NNN(self):
        source = """
            Employé: employé
            Appliquer, 0N Employé, 1N Projet, 1N Compétence
            Projet: projet
            Compétence: compétence
        """
        actual = run(source, common=common, testing=True)
        expected = """
            [Compétence] ==N== <Appliquer>
            [Employé] --N-- <Appliquer>
            [Projet] ==N== <Appliquer>
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_1NN(self):
        source = """
            Ingénieur: ingénieur
            Gérer, /1N Responsable, 1N Ingénieur, 1N Projet
            Projet: projet
            Responsable: responsable
        """
        actual = run(source, common=common, testing=True)
        expected = """
            [Ingénieur] ==N== <Gérer>
            [Projet] ==N== <Gérer>
            [Responsable] ==1== <Gérer>
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_11N(self):
        source = """
            Projet: projet
            Affecter, /1N Site, /1N Projet, 0N Employé
            Site: site
            Employé: employé
        """
        actual = run(source, common=common, testing=True)
        expected = """
            [Employé] --N-- <Affecter>
            [Projet] ==1== <Affecter>
            [Site] ==1== <Affecter>
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_111(self):
        source = """
            Technicien: technicien
            Utiliser, /1N Technicien, /1N Carnet, /1N Projet
            Projet: projet
            Carnet: carnet
        """
        actual = run(source, common=common, testing=True)
        expected = """
            [Carnet] ==1== <Utiliser>
            [Projet] ==1== <Utiliser>
            [Technicien] ==1== <Utiliser>
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_attrs(self):
        source = """
            COMMANDE: Num. commande, Date, Montant
            INCLURE, 1N COMMANDE, 0N PRODUIT: Quantité
            PRODUIT: Réf. produit, Libellé, Prix unitaire
        """
        actual = run(source, common=common, subargs={"attrs": 1}, testing=True)
        expected = """
            <INCLURE> -- (Quantité)
            [COMMANDE] -- (Date)
            [COMMANDE] -- (Montant)
            [COMMANDE] -- (_Num. commande_)
            [COMMANDE] ==N== <INCLURE>
            [PRODUIT] -- (Libellé)
            [PRODUIT] -- (Prix unitaire)
            [PRODUIT] -- (_Réf. produit_)
            [PRODUIT] --M-- <INCLURE>
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_id_weakness(self):
        source = """
            Œuvre: œuvre
            DF, 0N Œuvre, _11 Exemplaire
            Exemplaire: exemplaire
        """
        actual = run(source, common=common, subargs={"attrs": 1}, testing=True)
        expected = """
            [[Exemplaire]] -- (.exemplaire.)
            [[Exemplaire]] ==N== <<DF>>
            [Œuvre] -- (_œuvre_)
            [Œuvre] --1-- <<DF>>
        """
        self.assertEqual(actual.strip(), expected.strip())


if __name__ == "__main__":
    unittest.main()
