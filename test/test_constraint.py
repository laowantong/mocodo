import gettext
import unittest

__import__("sys").path[0:0] = ["mocodo"]
from mocodo.constraint import *


gettext.NullTranslations().install()

class parse_test(unittest.TestCase):
    
    def test_constraint_size(self):
        for content in ("", "X", "XX", "XXX"):
            c = Constraint(f"({content})")
            self.assertEqual(c.kind, "constraint")
            self.assertEqual(c.legs, [])
            self.assertEqual(c.note, None)
        self.assertRaises(AttributeError, Constraint, "(XXXX)")
    
    def test_legs(self):
        c = Constraint("(XX) foo, foo, foo")
        self.assertEqual(len(c.legs), 3)
        for leg in c.legs:
            self.assertEqual(leg.box_name, "foo")
            self.assertEqual(leg.kind, "")
        c = Constraint("(XX) ->foo, -->foo, -> foo, --> foo")
        for leg in c.legs:
            self.assertTrue(leg.kind.endswith("->"))
        c = Constraint("(XX) .>foo, ..>foo, .> foo, ..> foo")
        for leg in c.legs:
            self.assertTrue(leg.kind.endswith(".>"))

    def test_note(self):
        c = Constraint("(XX) [note]")
        self.assertEqual(c.note, "note")
        c = Constraint("(XX) [note] foo, foo, foo")
        self.assertEqual(c.note, "note")
        c = Constraint("(XX) [note]: 42")
        self.assertEqual(c.note, "note")
        c = Constraint("(XX) [note] foo, foo, foo: 42")
        self.assertEqual(c.note, "note")
    
    def test_ratios(self):
        c = Constraint("(XX) foo, foo, foo: 42")
        self.assertEqual(c.ratios, (42, 42))
        c = Constraint("(XX): 1, 2")
        self.assertEqual(c.ratios, (1, 2))
        c = Constraint("(XX): 1, 2, 3")
        self.assertEqual(c.ratios, (1, 2))
        c = Constraint("(XX) [note]: 1, 2, 3, 4")
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.42", Constraint, "(XX) foo, bar: baz, qux")


if __name__ == '__main__':
    unittest.main()
