__import__("sys").path[0:0] = ["mocodo"]

import json
import unittest
from pathlib import Path
from mocodo.common import read_template

TEMPLATE_FOLDER = Path("test") / "test_data" / "inherited_templates"

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


if __name__ == '__main__':
    unittest.main()
