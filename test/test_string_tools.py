import unittest

__import__("sys").path[0:0] = ["mocodo"]
from mocodo.tools import string_tools


class WrapLabelTest(unittest.TestCase):

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
            ['Adresse', '1'],
            ['Adresse 1', 'du', 'détenteur'],
            ['Apporteur'],
            ['Ayant-', 'droit'],
            ['Code pays'],
            ['Code pays de', 'résidence du', 'détenteur'],
            ['Code pays', 'détenteur'],
            ['Code', 'postal'],
            ['Commune', 'du', 'détenteur'],
            ['Date de', 'création'],
            ['Date de', 'création', 'en BDNI'],
            ['Date de', 'réception'],
            ['Date de', 'réception', 'en BDNI'],
            ['Nom'],
            ['Nom du', 'détenteur'],
            ['Numéro de', 'SIREN du', 'détenteur'],
            ['Numéro', 'détenteur'],
            ['Raison', 'sociale'],
            ['Raison', 'sociale ou', 'situation', 'civile'],
        ]
        for (label, expected) in zip(sample, wrapped):
            self.assertEqual(string_tools.wrap_label(label), expected)

class TestRstripDigit(unittest.TestCase):

    def test_rstrip_digit(self):
        assert string_tools.rstrip_digit("foo") == "foo"
        assert string_tools.rstrip_digit("foo1") == "foo"
        assert string_tools.rstrip_digit("foo12") == "foo1"
        assert string_tools.rstrip_digit("") == ""
        assert string_tools.rstrip_digit("1") == ""

class TestSurrounds(unittest.TestCase):

    def test_surrounds(self):
        assert string_tools.surrounds("(foobar)", "()")
        string_tools.surrounds("_foobar_", "_")
        string_tools.surrounds("_foobar_", "__")
        assert not string_tools.surrounds("(foobar)", ")(")
        assert string_tools.surrounds("()", "()")
        assert not string_tools.surrounds("", "()")
        assert not string_tools.surrounds("foobar", "fo")

if __name__ == "__main__":
    unittest.main()
