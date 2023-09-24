import unittest
from random import seed
import gettext

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.rewrite._arrange import run as arrange
from mocodo.mocodo_error import MocodoError

gettext.NullTranslations().install()

class ArrangeBB(unittest.TestCase):

    def test_constraints(self):
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

        # balanced = 0
        subargs = {"algo": "bb", "balanced": ""}
        seed(42)
        actual = arrange(source, subargs)
        expected = """
            SEMPER, 0N RISUS, 1N DIGNISSIM
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM
            SUSPENDISSE: diam
            DF, 11 LOREM, 1N SUSPENDISSE

            RISUS: ultricies, _cras, elementum
            DIGNISSIM: ligula, massa, varius
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            LOREM: ipsum, dolor, sit

            DF, 11 RISUS, 0N RISUS
            TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
            CONSECTETUER: elit, sed
            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
        """.replace("   ", "").strip()
        self.assertEqual(actual, expected)

        # balanced = 1

        subargs = {"algo": "bb", "balanced": "1"}
        seed(42)
        actual = arrange(source, subargs)
        expected = """
            DF, 11 RISUS, 0N RISUS
            :
            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
            LOREM: ipsum, dolor, sit
            DF, 11 LOREM, 1N SUSPENDISSE

            RISUS: ultricies, _cras, elementum
            TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
            CONSECTETUER: elit, sed
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            SUSPENDISSE: diam

            SEMPER, 0N RISUS, 1N DIGNISSIM
            DIGNISSIM: ligula, massa, varius
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM
            :
            :
        """.replace("   ", "").strip()
        self.assertEqual(actual, expected)

        # organic

        subargs = {"algo": "bb"}
        seed(2)
        actual = arrange(source, subargs)
        expected = """
            DF, 11 LOREM, 1N SUSPENDISSE
            SUSPENDISSE: diam
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM
            :

            LOREM: ipsum, dolor, sit
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            DIGNISSIM: ligula, massa, varius
            SEMPER, 0N RISUS, 1N DIGNISSIM

            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
            CONSECTETUER: elit, sed
            TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
            RISUS: ultricies, _cras, elementum

            :
            :
            :
            DF, 11 RISUS, 0N RISUS
        """.replace("   ", "").strip()
        self.assertEqual(actual, expected)

        # wide = 8 (default)

        subargs = {"algo": "bb", "wide": None} # the mere presence of the key is enough
        seed(2)
        actual = arrange(source, subargs)
        expected = """
            DF, 11 RISUS, 0N RISUS
            RISUS: ultricies, _cras, elementum
            TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
            :
            CONSECTETUER: elit, sed
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            SUSPENDISSE: diam

            :
            SEMPER, 0N RISUS, 1N DIGNISSIM
            DIGNISSIM: ligula, massa, varius
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM
            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
            LOREM: ipsum, dolor, sit
            DF, 11 LOREM, 1N SUSPENDISSE
        """.replace("   ", "").strip()
        self.assertEqual(actual, expected)

        # wide = 3

        subargs = {"algo": "bb", "wide": "3"} # the mere presence of the key is enough
        seed(2)
        actual = arrange(source, subargs)
        expected = """
            DF, 11 LOREM, 1N SUSPENDISSE
            SUSPENDISSE: diam
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM
            SEMPER, 0N RISUS, 1N DIGNISSIM

            LOREM: ipsum, dolor, sit
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            DIGNISSIM: ligula, massa, varius
            RISUS: ultricies, _cras, elementum

            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
            CONSECTETUER: elit, sed
            TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
            DF, 11 RISUS, 0N RISUS
        """.replace("   ", "").strip()
        self.assertEqual(actual, expected)

        # timeout too low

        subargs = {"algo": "bb", "timeout": 0.000001}
        seed(2)
        self.assertRaisesRegex(MocodoError, r"Mocodo Err\.10", arrange, source, subargs)

    def test_non_connected_graph(self):
        source = """
            SUSPENDISSE: diam
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            CONSECTETUER: elit, sed
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM

            DF, 11 LOREM, 1N SUSPENDISSE
            LOREM: ipsum, dolor, sit
            DIGNISSIM: ligula, massa, varius

            DF, 11 RISUS, 0N RISUS
            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
            RISUS: ultricies, _cras, elementum
            SEMPER, 0N RISUS, 1N DIGNISSIM
        """.replace("   ", "").strip()
        subargs = {"algo": "bb", "balanced": ""}
        seed(42)
        actual = arrange(source, subargs)
        expected = """
            DF, 11 RISUS, 0N RISUS
            SUSPENDISSE: diam
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            CONSECTETUER: elit, sed

            RISUS: ultricies, _cras, elementum
            DF, 11 LOREM, 1N SUSPENDISSE
            LOREM: ipsum, dolor, sit
            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing

            SEMPER, 0N RISUS, 1N DIGNISSIM
            DIGNISSIM: ligula, massa, varius
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM
            :
        """.replace("   ", "").strip()
        self.assertEqual(actual, expected)

    def test_no_link(self):
        source = """
            SUSPENDISSE: diam
            CONSECTETUER: elit, sed

            LOREM: ipsum, dolor, sit
            DIGNISSIM: ligula, massa, varius

            RISUS: ultricies, _cras, elementum
        """.replace("   ", "").strip()
        subargs = {"algo": "bb", "balanced": "0"}
        seed(42)
        actual = arrange(source, subargs)
        expected = """
            :
            DIGNISSIM: ligula, massa, varius
            :
            CONSECTETUER: elit, sed
            :
            LOREM: ipsum, dolor, sit
            :

            :
            RISUS: ultricies, _cras, elementum
            :
            SUSPENDISSE: diam
            :
            :
            :
        """.replace("   ", "").strip()
        self.assertEqual(actual, expected)

    def test_inheritance(self):
        source = """
            SUSPENDISSE: diam
            /XT\\ SUSPENDISSE -> CONSECTETUER, LOREM
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
        subargs = {"algo": "bb"}
        seed(4)
        actual = arrange(source, subargs)
        expected = """
            DF, 11 LOREM, 1N SUSPENDISSE
            SUSPENDISSE: diam
            :
            :
            :

            LOREM: ipsum, dolor, sit
            /XT\\ SUSPENDISSE -> CONSECTETUER, LOREM
            :
            :
            :

            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
            CONSECTETUER: elit, sed
            TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
            RISUS: ultricies, _cras, elementum
            DF, 11 RISUS, 0N RISUS

            :
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM
            DIGNISSIM: ligula, massa, varius
            SEMPER, 0N RISUS, 1N DIGNISSIM
            :
        """.replace("   ", "").strip()
        self.assertEqual(actual, expected)
        

if __name__ == "__main__":
    unittest.main()
