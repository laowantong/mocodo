import unittest
import random
import gettext

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.rewrite._grow import run as grow

class TestGrow(unittest.TestCase):

    def test_default(self):
        gettext.NullTranslations().install()
        random.seed(1)
        actual = grow("FOO: bar, biz", {})
        expected = """
            FOO: bar, biz
            Reflexive 2_, 1N FOO, 0N FOO
            Entity 3_: id 3 1, attr 3 2, attr 3 3, attr 3 4
            Binary 4_, 11 Entity 3_, 0N FOO: attr 4 1
            Reflexive 5_, 1N Entity 3_, 11 Entity 3_
            Entity 6_: id 6 1, _id 6 2, attr 6 3, attr 6 4
            Ternary 7_, 0N Entity 6_, 0N Entity 3_, 0N FOO
            Entity 8_: id 8 1, attr 8 2, attr 8 3, attr 8 4
            Binary 9_, 1N Entity 8_, 1N Entity 6_
            Entity 10_: id 10 1, attr 10 2, attr 10 3, attr 10 4
            Binary 11_, 1N Entity 10_, 0N Entity 8_
            Entity 12_: id 12 1, attr 12 2
            Binary 13_, 0N Entity 12_, 1N Entity 10_: attr 13 1
            Entity 14_: id 14 1, _id 14 2, attr 14 3, attr 14 4
            Binary 15_, 01 Entity 14_, 11 Entity 8_
            Entity 16_: id 16 1, attr 16 2, attr 16 3
            Binary 17_, 0N Entity 16_, 0N Entity 14_
            Binary 18_, 0N Entity 16_, 01 Entity 14_
        """.replace("    ", "")
        self.assertEqual(actual.strip(), expected.strip())

if __name__ == "__main__":
    unittest.main()
