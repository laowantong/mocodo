import unittest
from pathlib import Path

__import__("sys").path[0:0] = ["mocodo"]
from mocodo.tools.string_tools import *


class StringToolsTest(unittest.TestCase):
    
    def test_wrap_label(self):
        sample = [
            "Adresse 1",
            "Adresse 1 du détenteur",
            "Apporteur",
            "Ayant-droit",
            "Code pays",
            "Code pays de résidence du détenteur",
            "Code pays détenteur",
            "Code postal",
            "Commune du détenteur",
            "Date de création",
            "Date de création en BDNI",
            "Date de réception",
            "Date de réception en BDNI",
            "Nom",
            "Nom du détenteur",
            "Numéro de SIREN du détenteur",
            "Numéro détenteur",
            "Raison sociale",
            "Raison sociale ou situation civile",
        ]
        wrapped = [
            ["Adresse", "1"],
            ["Adresse 1", "du", "détenteur"],
            ["Apporteur"],
            ["Ayant-", "droit"],
            ["Code pays"],
            ["Code pays de", "résidence du", "détenteur"],
            ["Code pays", "détenteur"],
            ["Code", "postal"],
            ["Commune", "du", "détenteur"],
            ["Date de", "création"],
            ["Date de", "création", "en BDNI"],
            ["Date de", "réception"],
            ["Date de", "réception", "en BDNI"],
            ["Nom"],
            ["Nom du", "détenteur"],
            ["Numéro de", "SIREN du", "détenteur"],
            ["Numéro", "détenteur"],
            ["Raison", "sociale"],
            ["Raison", "sociale ou", "situation", "civile"],
        ]
        for (label, expected) in zip(sample, wrapped):
            self.assertEqual(wrap_label(label), expected)

    def test_rstrip_digit_or_underline(self):
        self.assertEqual(rstrip_digit_or_underline("foo"), "foo")
        self.assertEqual(rstrip_digit_or_underline("foo1"), "foo")
        self.assertEqual(rstrip_digit_or_underline("foo12"), "foo1")
        self.assertEqual(rstrip_digit_or_underline(""), "")
        self.assertEqual(rstrip_digit_or_underline("1"), "")
        self.assertEqual(rstrip_digit_or_underline("foo_"), "foo")
        self.assertEqual(rstrip_digit_or_underline("foo1_"), "foo1")
        self.assertEqual(rstrip_digit_or_underline("_"), "")

    def test_surrounds(self):
        self.assertTrue(surrounds("(foobar)", "()"))
        self.assertTrue(surrounds("_foobar_", "_"))
        self.assertTrue(surrounds("_foobar_", "__"))
        self.assertFalse(surrounds("(foobar)", ")("))
        self.assertTrue(surrounds("()", "()"))
        self.assertFalse(surrounds("", "()"))
        self.assertFalse(surrounds("foobar", "fo"))

    def test_snake(self):
        self.assertEqual(snake("foo"), "foo")
        self.assertEqual(snake("Foo"), "Foo")
        self.assertEqual(snake("FOO"), "FOO")
        self.assertEqual(snake("fooBar"), "foo_Bar")
        self.assertEqual(snake("fooBar"), "foo_Bar")
        self.assertEqual(snake("FOOBar"), "FOOBar")
        self.assertEqual(snake("fooBAR"), "foo_BAR")
        self.assertEqual(snake("foo bar"), "foo_bar")
        self.assertEqual(snake("foo  bar"), "foo_bar")
        self.assertEqual(snake("foo-bar"), "foo_bar")
        self.assertEqual(snake("foo--bar"), "foo_bar")
        self.assertEqual(snake("foo_bar"), "foo_bar")
        self.assertEqual(snake("foo__bar"), "foo_bar")
        self.assertEqual(snake("foo1bar"), "foo_1_bar")
        self.assertEqual(snake("foo1Bar"), "foo_1_Bar")
        self.assertEqual(snake("foO1Bar"), "fo_O_1_Bar")
        self.assertEqual(snake("FOO BAR"), "FOO_BAR")
        self.assertEqual(snake("-FOO-BAR-"), "FOO_BAR")
        self.assertEqual(snake("_FOO_BAR_"), "FOO_BAR_")
        self.assertEqual(snake("_FOO_BAR1"), "FOO_BAR1")
    
    def test_camel(self):
        self.assertEqual(camel("foo"), "foo")
        self.assertEqual(camel("Foo"), "foo")
        self.assertEqual(camel("FOO"), "foo")
        self.assertEqual(camel("fooBar"), "fooBar")
        self.assertEqual(camel("FooBar"), "fooBar")
        self.assertEqual(camel("FOOBar"), "foobar")
        self.assertEqual(camel("fooBAR"), "fooBar")
        self.assertEqual(camel("foo bar"), "fooBar")
        self.assertEqual(camel("foo  bar"), "fooBar")
        self.assertEqual(camel("foo-bar"), "fooBar")
        self.assertEqual(camel("foo--bar"), "fooBar")
        self.assertEqual(camel("foo_bar"), "fooBar")
        self.assertEqual(camel("foo__bar"), "fooBar")
        self.assertEqual(camel("foo1bar"), "foo1Bar")
        self.assertEqual(camel("foo1Bar"), "foo1Bar")
        self.assertEqual(camel("foO1Bar"), "foO1Bar")
        self.assertEqual(camel("FOO BAR"), "fooBar")
        self.assertEqual(camel("-FOO-BAR-"), "fooBar")
        self.assertEqual(camel("-FOO-BAR_"), "fooBar_")
        self.assertEqual(camel("-FOO-BAR1"), "fooBar1")
    
    def test_pascal(self):
        self.assertEqual(pascal("foo"), "Foo")
        self.assertEqual(pascal("Foo"), "Foo")
        self.assertEqual(pascal("FOO"), "Foo")
        self.assertEqual(pascal("fooBar"), "FooBar")
        self.assertEqual(pascal("FooBar"), "FooBar")
        self.assertEqual(pascal("FOOBar"), "Foobar")
        self.assertEqual(pascal("fooBAR"), "FooBar")
        self.assertEqual(pascal("foo bar"), "FooBar")
        self.assertEqual(pascal("foo  bar"), "FooBar")
        self.assertEqual(pascal("foo-bar"), "FooBar")
        self.assertEqual(pascal("foo--bar"), "FooBar")
        self.assertEqual(pascal("foo_bar"), "FooBar")
        self.assertEqual(pascal("foo__bar"), "FooBar")
        self.assertEqual(pascal("foo1bar"), "Foo1Bar")
        self.assertEqual(pascal("foo1Bar"), "Foo1Bar")
        self.assertEqual(pascal("foO1Bar"), "FoO1Bar")
        self.assertEqual(pascal("FOO BAR"), "FooBar")
        self.assertEqual(pascal("-FOO-BAR-"), "FooBar")
        self.assertEqual(pascal("-FOO-BAR_"), "FooBar_")
        self.assertEqual(pascal("-FOO-BAR1"), "FooBar1")

    def test_aggressive_split(self):
        f = aggressive_split
        self.assertEqual(f(''), [])
        self.assertEqual(f('p'), ['p'])
        self.assertEqual(f('3-'), ['3'])
        self.assertEqual(f('NOM'), ['NOM'])
        self.assertEqual(f('CONTRÔLER'), ['CONTRÔLER'])
        self.assertEqual(f('Nom'), ['Nom'])
        self.assertEqual(f('nom'), ['nom'])
        self.assertEqual(f('Nom lieu'), ['Nom', 'lieu'])
        self.assertEqual(f('nom de compte'), ['nom', 'de', 'compte'])
        self.assertEqual(f('Nom_lieu'), ['Nom', 'lieu'])
        self.assertEqual(f('Nom_Lieu'), ['Nom', 'Lieu'])
        self.assertEqual(f('NomLieu'), ['Nom', 'Lieu'])
        self.assertEqual(f('nomlieu'), ['nomlieu'])
        self.assertEqual(f('Gratte-ciel'), ['Gratte', 'ciel'])
        self.assertEqual(f('Identité_pays'), ['Identité', 'pays'])
        self.assertEqual(f('ID_Produit'), ['ID', 'Produit'])
        self.assertEqual(f('FolderID'), ['Folder', 'ID'])
        self.assertEqual(f('IdVoyage-'), ['Id', 'Voyage'])
        self.assertEqual(f('N°Lieu'), ['N', 'Lieu'])
        self.assertEqual(f('N°lieu'), ['N', 'lieu'])
        self.assertEqual(f('NumLieuTournage-'), ['Num', 'Lieu', 'Tournage'])
        self.assertEqual(f('nomPays_EN'), ['nom', 'Pays', 'EN'])
        self.assertEqual(f('Conditions(Affichage)'), ['Conditions', 'Affichage'])
        self.assertEqual(f('Conditions (Affichage)'), ['Conditions', 'Affichage'])
        self.assertEqual(f('COMPOSE3'), ['COMPOSE', '3'])
        self.assertEqual(f('téléphone2'), ['téléphone', '2'])
        self.assertEqual(f('téléphone23'), ['téléphone', '23'])
        self.assertEqual(f('téléphone 2'), ['téléphone', '2'])
        self.assertEqual(f('beginning-date'), ['beginning', 'date'])
        self.assertEqual(f('latitude_L'), ['latitude', 'L'])
        self.assertEqual(f('id_insert → equipement_id'), ['id', 'insert', 'equipement', 'id'])
        self.assertEqual(f('CNIPays'), ['CNIPays'])
        self.assertEqual(f('réf. client'), ['réf', 'client'])
        self.assertEqual(f('kWday_summer'), ['k', 'Wday', 'summer'])
        self.assertEqual(f('DescriptionŒuvre'), ['Description', 'Œuvre'])


if __name__ == "__main__":
    unittest.main()
