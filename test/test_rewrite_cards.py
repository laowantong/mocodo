import unittest
import random

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.rewrite import op_tk


class TestUpdateCards(unittest.TestCase):

    def test_infer_df(self):
        # Actually not a card update, but I don't want to create a new test file just for this.
        source = """
            BAKE, 0N TEND, 01 TALL
            FISH, -1N TALL, -11 TOUR: slot
            DOWN, 0N [cold] TOUR, 0N [echo] TOUR: hang
            WRAP, _11 PORK, 0N TEND
            FINE, 11 DRAW, 0N BULK
            HERE, 1N TALL, 1N TOUR, /11 HOST: mask
            GOAL, 11 TEND, 1N AIDS
            ZONE, 0N TEND, /1N TALL
            LUCK, 0N< [find] HOST, /11 [hill] HOST
            AIDS, XX VARY, ?? WRAP
        """
        actual = op_tk.run(source, "create", {"df": 1}, {"df": "DF"})
        expected = """
            BAKE, 0N TEND, 01 TALL
            DF, -1N TALL, -11 TOUR: slot
            DOWN, 0N [cold] TOUR, 0N [echo] TOUR: hang
            DF, _11 PORK, 0N TEND
            DF, 11 DRAW, 0N BULK
            HERE, 1N TALL, 1N TOUR, /11 HOST: mask
            DF, 11 TEND, 1N AIDS
            ZONE, 0N TEND, /1N TALL
            LUCK, 0N< [find] HOST, /11 [hill] HOST
            AIDS, XX VARY, ?? WRAP
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_fix_cards(self):
        source = "A, ON B, No No"
        actual = op_tk.run(source, "fix", {"cards": 1}, {}).strip()
        expected = "A, 0N B, 0N No"
        self.assertEqual(actual, expected)

    def test_delete_cards(self):
        source = "A, 01 B, 0N C"
        actual = op_tk.run(source, "delete", {"cards": 1}, {}).strip()
        expected = "A, XX B, XX C"
        self.assertEqual(actual, expected)

    def test_change_capitalization_cards(self):
        source = "A, 0N B, _1N No"
        actual = op_tk.run(source, "lower", {"cards": 1}, {}).strip()
        expected = "A, 0n B, _1n No"
        self.assertEqual(actual, expected)
        source = expected
        actual = op_tk.run(source, "upper", {"cards": 1}, {}).strip()
        expected = "A, 0N B, _1N No"
        self.assertEqual(actual, expected)
    
    def test_infer_roles(self):

        # Cases *N vs *1

        source = "Rule, 0N Else, 11 Peel"
        actual = op_tk.run(source, "create", {"roles": 1}, {}).strip()
        expected = "Rule, 0N [Rule] Else, 11 Peel"
        self.assertEqual(actual, expected)
        
        source = "Rule, 1N Else, 11 Peel"
        actual = op_tk.run(source, "create", {"roles": 1}, {}).strip()
        expected = "Rule, 1N [Rule] Else, 11 Peel"
        self.assertEqual(actual, expected)

        source = "Rule, 0N Else, 01 Peel"
        actual = op_tk.run(source, "create", {"roles": 1}, {}).strip()
        expected = "Rule, 0N [Rule] Else, 01 Peel"
        self.assertEqual(actual, expected)
        
        source = "Rule, 1N Else, 01 Peel"
        actual = op_tk.run(source, "create", {"roles": 1}, {}).strip()
        expected = "Rule, 1N [Rule] Else, 01 Peel"
        self.assertEqual(actual, expected)

        source = "Rule, XX Else, 11 Peel"
        actual = op_tk.run(source, "create", {"roles": 1}, {}).strip()
        expected = "Rule, XX [Rule] Else, 11 Peel"
        self.assertEqual(actual, expected)

        source = "Rule, XX Else, 01 Peel"
        actual = op_tk.run(source, "create", {"roles": 1}, {}).strip()
        expected = "Rule, XX [Rule] Else, 01 Peel"
        self.assertEqual(actual, expected)

        # Cases *1 vs *1
        
        source = "Rule, 01 Else, 11 Peel"
        actual = op_tk.run(source, "create", {"roles": 1}, {}).strip()
        expected = "Rule, 01 [Rule] Else, 11 Peel"
        self.assertEqual(actual, expected)
        
        source = "Rule, 11 Else, 11 Peel"
        actual = op_tk.run(source, "create", {"roles": 1}, {}).strip()
        expected = "Rule, 11 [Rule] Else, 11 [Rule] Peel"  # slightly overkill
        self.assertEqual(actual, expected)

        # Other cases

        source = "Rule, 0N Else, 1N Peel"
        actual = op_tk.run(source, "create", {"roles": 1}, {}).strip()
        expected = "Rule, 0N Else, 1N Peel"
        self.assertEqual(actual, expected)

    
if __name__ == "__main__":
    unittest.main()
