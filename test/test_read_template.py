import gettext
import unittest
from pathlib import Path

__import__("sys").path[0:0] = ["mocodo"]
from mocodo.convert.read_template import read_template
from mocodo.tools import load_mini_yaml
from mocodo.mocodo_error import MocodoError
from mocodo.dev import update_transfo_metadata # just update the graph and index

gettext.NullTranslations().install()

TEMPLATE_FOLDER = Path("test", "test_data", "templates")

class TestReadTemplate(unittest.TestCase):

    def test_root_template(self):
        template = read_template("root", TEMPLATE_FOLDER)
        expected = load_mini_yaml.run(Path(TEMPLATE_FOLDER, "root.yaml"))
        self.assertEqual(template, expected)
    
    def test_child_template(self):
        template = read_template("child", TEMPLATE_FOLDER)
        expected = load_mini_yaml.run(Path(TEMPLATE_FOLDER, "expected_child.yaml"))
        self.assertEqual(template, expected)
    
    def test_grandchild_template(self):
        template = read_template("grandchild", TEMPLATE_FOLDER)
        expected = load_mini_yaml.run(Path(TEMPLATE_FOLDER, "expected_grandchild.yaml"))
        self.assertEqual(template, expected)
    
    def test_errors(self):
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.30", read_template, "bad_circular_1", TEMPLATE_FOLDER)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.31", read_template, "not_a_file", TEMPLATE_FOLDER)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.32", read_template, "bad_array_element", TEMPLATE_FOLDER)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.32", read_template, "bad_not_an_object", TEMPLATE_FOLDER)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.32", read_template, "bad_object_value", TEMPLATE_FOLDER)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.36", read_template, "bad_no_order", TEMPLATE_FOLDER)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.38", read_template, "bad_non_numeric_order", TEMPLATE_FOLDER)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.39", read_template, "bad_non_increasing_order", TEMPLATE_FOLDER)


if __name__ == '__main__':
    unittest.main()
