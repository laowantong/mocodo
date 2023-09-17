import unittest
import random
import gettext

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.rewrite._grow import run as grow

gettext.NullTranslations().install()

class TestGrow(unittest.TestCase):

    def test_default(self):
        random.seed(1)
        actual = grow("FOO: bar, biz", {})
        expected = """
            FOO: bar, biz
            Entity 2_: attr 2 1_, attr 2 2_, attr 2 3_, attr 2 4_
            Binary 3_, XX Entity 2_, XX FOO
            Entity 4_: attr 4 1_, attr 4 2_
            Binary 5_, XX Entity 4_, XX Entity 2_
            Entity 6_: attr 6 1_, attr 6 2_, attr 6 3_, attr 6 4_
            Binary 7_, XX Entity 6_, XX Entity 2_
            Entity 8_: attr 8 1_
            Binary 9_, XX Entity 8_, XX FOO
            Entity 10_: attr 10 1_, attr 10 2_
            Binary 11_, XX Entity 10_, XX Entity 6_
            Entity 12_: attr 12 1_, _attr 12 2_, attr 12 3_, attr 12 4_
            Ternary 13_, XX Entity 12_, XX Entity 8_, XX Entity 10_
            Reflexive 14_, XX FOO, XX FOO: attr 14 1_
            Entity 15_: attr 15 1_, _attr 15 2_, attr 15 3_
            Binary 16_, XX Entity 15_, XX Entity 2_
            Reflexive 17_, XX Entity 8_, XX Entity 8_: attr 17 1_
            Binary 18_, XX Entity 4_, XX Entity 2_
        """.replace("    ", "")
        self.assertEqual(actual.strip(), expected.strip())

if __name__ == "__main__":
    unittest.main()
