import unittest

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.rewrite import op_tk


class TestUpdateCards(unittest.TestCase):
    def test_randomize(self):
        source = """
            BAKE, 0N TEND, 01 TALL
            FISH, -1N TALL, -0N TOUR: slot
            DOWN, 0N [cold] TOUR, 0N [echo] TOUR: hang
            DF, _11 PORK, 0N TEND
            DF, 11 DRAW, 0N BULK
            HERE, 1N TALL, 1N TOUR, 1N HOST: mask
            GOAL, 11 TEND, 1N AIDS
            ZONE, 0N TEND, /1N TALL
            LUCK, 0N< [find] HOST, 01 [hill] HOST
            AIDS, XX VARY, ?? WRAP
        """
        actual = op_tk.run(source, "cards", {"random": True}, {})
        expected = """
            BAKE, 01 TEND, 01 TALL
            FISH, -0N TALL, -_11 TOUR: slot
            DOWN, 01 [cold] TOUR, /1N [echo] TOUR: hang
            DF, 01 PORK, _11 TEND
            DF, 01 DRAW, 11 BULK
            HERE, 1N TALL, 11 TOUR, /1N HOST: mask
            GOAL, 11 TEND, 1N AIDS
            ZONE, 0N TEND, 01 TALL
            LUCK, 01< [find] HOST, 0N [hill] HOST
            AIDS, 0N VARY, 01 WRAP
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_fix_cards(self):
        source = "A, ON B, No No"
        actual = op_tk.run(source, "cards", {"fix": True}, {}).strip()
        expected = "A, 0N B, 0N No"
        self.assertEqual(actual, expected)

    def test_delete_cards(self):
        source = "A, 01 B, 0N C"
        actual = op_tk.run(source, "cards", {"delete": True}, {}).strip()
        expected = "A, XX B, XX C"
        self.assertEqual(actual, expected)

    def test_change_capitalization_cards(self):
        source = "A, 0N B, _1N No"
        actual = op_tk.run(source, "cards", {"lower": True}, {}).strip()
        expected = "A, 0n B, _1n No"
        self.assertEqual(actual, expected)
        source = expected
        actual = op_tk.run(source, "cards", {"upper": True}, {}).strip()
        expected = "A, 0N B, _1N No"
        self.assertEqual(actual, expected)
    
if __name__ == "__main__":
    unittest.main()