import unittest

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.rewrite.types import guess_types, create_type_placeholders


class TestUpdateTypes(unittest.TestCase):

    def test_create(self):
        source = """
            MEAN: wash, rest [], king [int],
            HERE, 0N NICE, 0N MEAN: wood, much [], stop [int]
            NICE: _poke, news [], , lawn [int]
        """
        actual = create_type_placeholders(source, "TODO")
        expected = """
            MEAN: wash [TODO], rest [], king [int],
            HERE, 0N NICE, 0N MEAN: wood [TODO], much [], stop [int]
            NICE: _poke [TODO], news [], , lawn [int]
        """
        self.assertEqual(actual.strip(), expected.strip())

    def test_guess_types(self):
        source = """
            ALREADY_TYPED: foo [int], bar [float], baz [date]
            EMPTY_BRACKETS: foo [], bar [], baz []
            NON_TYPABLE: foo, bar, baz
            TYPABLE: person id, name, birth date
        """
        actual = guess_types(source, {"script_directory": "mocodo"})
        expected = """
            ALREADY_TYPED: foo [int], bar [float], baz [date]
            EMPTY_BRACKETS: foo [], bar [], baz []
            NON_TYPABLE: foo [], bar [], baz []
            TYPABLE: person id [VARCHAR(8)], name [VARCHAR(255)], birth date [DATE]
        """
        self.assertEqual(actual.strip(), expected.strip())

if __name__ == "__main__":
    unittest.main()
