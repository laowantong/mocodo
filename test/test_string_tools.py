import unittest

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
        self.assertEqual(snake("Foo"), "foo")
        self.assertEqual(snake("FOO"), "FOO")
        self.assertEqual(snake("fooBar"), "foo_bar")
        self.assertEqual(snake("FooBar"), "foo_bar")
        self.assertEqual(snake("FOOBar"), "foobar")
        self.assertEqual(snake("fooBAR"), "foo_bar")
        self.assertEqual(snake("foo bar"), "foo_bar")
        self.assertEqual(snake("foo  bar"), "foo_bar")
        self.assertEqual(snake("foo-bar"), "foo_bar")
        self.assertEqual(snake("foo--bar"), "foo_bar")
        self.assertEqual(snake("foo_bar"), "foo_bar")
        self.assertEqual(snake("foo__bar"), "foo_bar")
        self.assertEqual(snake("foo1bar"), "foo1bar")
        self.assertEqual(snake("foo1Bar"), "foo1bar")
        self.assertEqual(snake("foO1Bar"), "fo_o1bar")
        self.assertEqual(snake("FOO BAR"), "FOO_BAR")
        self.assertEqual(snake("-FOO-BAR-"), "FOO_BAR")
        self.assertEqual(snake("_FOO_BAR_"), "_FOO_BAR_")
    
    def test_camel(self):
        self.assertEqual(camel("foo"), "foo")
        self.assertEqual(camel("Foo"), "Foo")
        self.assertEqual(camel("FOO"), "FOO")
        self.assertEqual(camel("fooBar"), "fooBar")
        self.assertEqual(camel("FooBar"), "FooBar")
        self.assertEqual(camel("FOOBar"), "FOOBar")
        self.assertEqual(camel("fooBAR"), "fooBAR")
        self.assertEqual(camel("foo bar"), "fooBar")
        self.assertEqual(camel("foo  bar"), "fooBar")
        self.assertEqual(camel("foo-bar"), "fooBar")
        self.assertEqual(camel("foo--bar"), "fooBar")
        self.assertEqual(camel("foo_bar"), "fooBar")
        self.assertEqual(camel("foo__bar"), "fooBar")
        self.assertEqual(camel("foo1bar"), "foo1bar")
        self.assertEqual(camel("foo1Bar"), "foo1Bar")
        self.assertEqual(camel("foO1Bar"), "foO1Bar")
        self.assertEqual(camel("FOO BAR"), "FOOBar")
        self.assertEqual(camel("-FOO-BAR-"), "FooBar")




if __name__ == "__main__":
    unittest.main()
