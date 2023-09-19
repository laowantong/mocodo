import unittest
from random import seed
import gettext

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.rewrite._arrange import run as arrange

gettext.NullTranslations().install()

class ArrangeGA(unittest.TestCase):

    def test_arrange(self):
        source = """
            SUSPENDISSE: diam
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            CONSECTETUER: elit, sed
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM

            DF, 11 LOREM, 1N SUSPENDISSE
            LOREM: ipsum, dolor, sit
            TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
            DIGNISSIM: ligula, massa, varius

            DF, 11 RISUS, 0N RISUS
            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
            RISUS: ultricies, _cras, elementum
            SEMPER, 0N RISUS, 1N DIGNISSIM
        """.replace("   ", "").strip()
        subargs = {"algo": "ga", "max_generations": 50, "population_size": 100}
        seed(1)
        actual = arrange(source, subargs)
        expected = """
            DF, 11 RISUS, 0N RISUS
            SUSPENDISSE: diam
            DF, 11 LOREM, 1N SUSPENDISSE
            LOREM: ipsum, dolor, sit

            RISUS: ultricies, _cras, elementum
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            CONSECTETUER: elit, sed
            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing

            SEMPER, 0N RISUS, 1N DIGNISSIM
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM
            DIGNISSIM: ligula, massa, varius
            TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
        """.replace("   ", "").strip()
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
