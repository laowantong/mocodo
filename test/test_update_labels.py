import unittest

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.update import op_tk


class TestUpdateLabels(unittest.TestCase):

    def test_upper(self):
        source = "composer, 0n [composée] pièce, 0n [composante] pièce: quantité"
        actual = op_tk.run(source, "labels", {"upper": None}, {})
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
        subargs = {"obfuscate": "four_letter_words.txt"}
        params = {"seed": 42, "script_directory": "mocodo"}
        actual = op_tk.run(source, "labels", subargs, params)
        print(actual)
        expected = """
            feel: turn, grin
            land, 0N Near, 0N feel, 0N SILK2
            SILK2: debt
            Shoe, 0N Near, 0N SILK, 0N feel: loss
            Near: poet, stir
            Auto, 1N Slew, 0N SILK2
            SILK: debt
            Tape, 0N Knee, 0N Near, 0N SILK
            Slew: code, they, bath, unit, haul
            Knee: draw, four, duck
            Icon, 11 Slew, 0N Knee
        """
        self.assertEqual(actual.strip(), expected.strip())
    
if __name__ == "__main__":
    unittest.main()
