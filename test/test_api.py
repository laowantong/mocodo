import unittest
import gettext
import re
from pathlib import Path

gettext.NullTranslations().install()

__import__("sys").path[0:0] = ["mocodo"]

from mocodo import __version__
from mocodo.api import mocodo

class TestMocodoApi(unittest.TestCase):

    def test_unrecognized_arguments(self):
        result = mocodo("foo bar")
        self.assertEqual(result, None)
    
    def test_no_arguments(self):
        paths = list(map(Path, [
            "pristine_sandbox.svg",
            "pristine_sandbox_static.svg",
            "pristine_sandbox_geo.json"
        ]))
        for path in paths:
            path.unlink(missing_ok=True)
        result = mocodo()
        self.assertEqual(mocodo(""), result)
        for path in paths:
            self.assertTrue(path.is_file())
        for path in paths:
            path.unlink()
    
    def test_help(self):
        result = mocodo("--help")
        self.assertEqual(result, None)
    
    def test_version(self):
        result = mocodo("--version")
        self.assertEqual(result, __version__)
    
    def test_language(self):
        result = mocodo("--language=en")
        self.assertRegex(result, re.compile(r"Output file.+generated"))
        result = mocodo("--language=fr")
        self.assertRegex(result, re.compile(r"Fichier de sortie.+succès"))
    
    def test_input_and_output_dir(self):
        path_json = Path("test/ccp_geo.json")
        path_svg = Path("test/ccp.svg")
        path_json.unlink(missing_ok=True)
        path_svg.unlink(missing_ok=True)
        mocodo("-i doc/mocodo_notebook/ccp.mcd --output_dir test")
        self.assertTrue(path_json.is_file())
        self.assertTrue(path_svg.is_file())
        path_json.unlink()
        path_svg.unlink()


if __name__ == "__main__":
    unittest.main()
