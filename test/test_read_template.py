import json
import unittest
from pathlib import Path

__import__("sys").path[0:0] = ["mocodo"]
from mocodo.read_template import read_template
from mocodo.mocodo_error import MocodoError

TEMPLATE_FOLDER = Path("test") / "test_data" / "templates"

class TestReadTemplate(unittest.TestCase):

    def test_root_template(self):
        template = read_template("root", TEMPLATE_FOLDER)
        expected = json.loads((TEMPLATE_FOLDER / "root.json").read_text())
        self.assertEqual(template, expected)
    
    def test_child_template(self):
        template = read_template("child", TEMPLATE_FOLDER)
        # print(json.dumps(template, indent=4))
        expected = json.loads((TEMPLATE_FOLDER / "expected_child.json").read_text())
        self.assertEqual(template, expected)
    
    def test_grandchild_template(self):
        template = read_template("grandchild", TEMPLATE_FOLDER)
        # print(json.dumps(template, indent=4))
        expected = json.loads((TEMPLATE_FOLDER / "expected_grandchild.json").read_text())
        self.assertEqual(template, expected)
    
    def test_errors(self):
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.30", read_template, "bad_circular_1", TEMPLATE_FOLDER)
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.31", read_template, "not_a_file", TEMPLATE_FOLDER)
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.32", read_template, "bad_not_json", TEMPLATE_FOLDER)
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.33", read_template, "bad_not_an_object", TEMPLATE_FOLDER)
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.34", read_template, "bad_object_value", TEMPLATE_FOLDER)
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.35", read_template, "bad_array_element", TEMPLATE_FOLDER)
        self.assertRaisesRegex(MocodoError, "Mocodo Err\.36", read_template, "bad_no_order", TEMPLATE_FOLDER)

if __name__ == '__main__':
    unittest.main()
