import gettext
import unittest

__import__("sys").path[0:0] = ["mocodo"]
from mocodo.inheritance import *
from mocodo.parser_tools import extract_clauses


gettext.NullTranslations().install()

def inheritance_wrapper(s, **kargs):
    return Inheritance(extract_clauses(s)[0], **kargs)

class parse_test(unittest.TestCase):
    
    def test_backslash_conservation(self):
        a = inheritance_wrapper(r"/XT\ FOO => BAR")
        self.assertEqual(a.name, "XT => FOO,BAR")
        self.assertEqual(a.name_view, "XT")
        self.assertEqual(a.legs[0].entity_name, "FOO")
        self.assertEqual(a.legs[1].entity_name, "BAR")
        self.assertEqual(a.kind, "=>")

    def test_numbered_inheritance(self):
        a = inheritance_wrapper(r"/XT1\ FOO => BAR")
        self.assertEqual(a.name, "XT1 => FOO,BAR")
        self.assertEqual(a.name_view, "XT")
        self.assertEqual(a.legs[0].entity_name, "FOO")
        self.assertEqual(a.legs[1].entity_name, "BAR")
        self.assertEqual(a.kind, "=>")
        a = inheritance_wrapper(r"/1\ FOO => BAR")
        self.assertEqual(a.name, "1 => FOO,BAR")
        self.assertEqual(a.name_view, "")
        self.assertEqual(a.legs[0].entity_name, "FOO")
        self.assertEqual(a.legs[1].entity_name, "BAR")
        self.assertEqual(a.kind, "=>")

if __name__ == '__main__':
    unittest.main()
