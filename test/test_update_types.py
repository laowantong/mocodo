import unittest

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.update import _types as update_types


class TestUpdateTypes(unittest.TestCase):

    def test_create(self):
        source = """
            MEAN: wash, rest [], king [int],
            HERE, 0N NICE, 0N MEAN: wood, much [], stop [int]
            NICE: _poke, news [], , lawn [int]
        """
        actual = update_types.run(source, {"create": True})
        expected = """
            MEAN: wash [], rest [], king [int],
            HERE, 0N NICE, 0N MEAN: wood [], much [], stop [int]
            NICE: _poke [], news [], , lawn [int]
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_guess_types(self):
        source = """
            ALREADY_TYPED: foo [int], bar [float], baz [date]
            EMPTY_BRACKETS: foo [], bar [], baz []
            NON_TYPABLE: foo, bar, baz
            TYPABLE: person id, name, birth date
        """
        actual = update_types.run(source, {"guess": True})
        expected = """
            ALREADY_TYPED: foo [int], bar [float], baz [date]
            EMPTY_BRACKETS: foo [], bar [], baz []
            NON_TYPABLE: foo [], bar [], baz []
            TYPABLE: person id [VARCHAR(8)?], name [VARCHAR(255)?], birth date [DATE?]
        """
        self.assertEqual(actual.strip(), expected.strip())

if __name__ == "__main__":
    unittest.main()
