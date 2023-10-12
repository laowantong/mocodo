import unittest
import random
import gettext

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.rewrite import op_tk

gettext.NullTranslations().install()

class TestUpdateLabels(unittest.TestCase):

    def test_upper(self):
        source = "composer, 0n [composée] pièce, 0n [composante] pièce: quantité"
        actual = op_tk.run(source, "upper", {"labels": ""}, {})
        expected = "COMPOSER, 0n [composée] PIÈCE, 0n [composante] PIÈCE: QUANTITÉ"
        self.assertEqual(actual.strip(), expected.strip())

    def test_obfuscate(self):
        source = """
            Vitae justo: lobortis, purus
            adipiscing, 0N Curabitur, 0N Vitae justo, 0N DATE2
            DATE2: date
            Pharetra, 0N Curabitur, 0N DATE, 0N Vitae justo: massa
            Curabitur: blandit, suscipit
            Porttitor, 1N Rhoncus, 0N DATE2
            DATE: date
            Imperdiet, 0N Egestas, 0N Curabitur, 0N DATE
            Rhoncus: dolor a, bibendum, euismod, consectetuer, leo
            Egestas: vivamus, semper, aliquam
            Ultricies, 11 Rhoncus, 0N Egestas
        """
        subargs = {"labels": "en4.txt"}
        params = {"script_directory": "mocodo", "df": "DF"}
        random.seed(42)
        actual = op_tk.run(source, "randomize", subargs, params)
        expected = """
            Feel: turn, grin
            land, 0N Near, 0N Feel, 0N SILK
            SILK: debt
            Shoe, 0N Near, 0N LOSS, 0N Feel: poet
            Near: stir, auto
            Slew, 1N Tape, 0N SILK
            LOSS: debt
            Knee, 0N Code, 0N Near, 0N LOSS
            Tape: they, bath, unit, haul, draw
            Code: four, duck, icon
            Golf, 11 Tape, 0N Code
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_obfuscate_df(self):
        source = """
            DF, 11 Curabitur, 0N Vitae justo, 0N DATE2
            DF, 1N Rhoncus, 11 DATE2
            DF, 11 Rhoncus, 0N Egestas
        """
        subargs = {"labels": "en4.txt"}
        params = {"script_directory": "mocodo", "df": "DF"}
        random.seed(42)
        actual = op_tk.run(source, "randomize", subargs, params)
        expected = """
            FEEL, 11 Turn, 0N Grin, 0N LAND
            NEAR, 1N Silk, 11 LAND
            DEBT, 11 Silk, 0N Shoe
        """
        self.assertEqual(actual.strip(), expected.strip())
    
    def test_obfuscate_pool_too_small(self):
        source = """
            DF, 11 Curabitur, 0N Vitae justo, 0N DATE2
            DF, 1N Rhoncus, 11 DATE2
            DF, 11 Rhoncus, 0N Egestas
        """
        subargs = {"labels": "test/test_data/small_pool.txt"}
        params = {"script_directory": "mocodo", "df": "DF"}
        random.seed(42)
        self.assertRaises(op_tk.MocodoError, op_tk.run, source, "randomize", subargs, params)

if __name__ == "__main__":
    unittest.main()
