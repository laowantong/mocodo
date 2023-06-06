import unittest

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.magic_command import split_by_unquoted_spaces_or_equals as split


class SplitTest(unittest.TestCase):
    def test_default(self):
        self.assertEqual(split("a b c"), ["a", "b", "c"])

    def test_double_quote(self):
        self.assertEqual(split('a "b c" d'), ["a", "b c", "d"])

    def test_single_quote(self):
        self.assertEqual(split("a 'b c' d"), ["a", "b c", "d"])

    def test_double_quote_with_single_quote(self):
        self.assertEqual(split('a "b\'c" d'), ["a", "b'c", "d"])

    def test_single_quote_with_double_quote(self):
        self.assertEqual(split("a 'b\"c' d"), ["a", 'b"c', "d"])

    def test_double_quote_with_double_quote(self):
        self.assertEqual(split('a "b""c" d'), ["a", "b", "c", "d"])

    def test_single_quote_with_single_quote(self):
        self.assertEqual(split("a 'b''c' d"), ["a", "b", "c", "d"])

    def test_equal_symbol(self):
        self.assertEqual(split("a=b=c"), ["a", "b", "c"])

    def test_equal_symbol_with_spaces(self):
        self.assertEqual(split("a = b = c"), ["a", "b", "c"])

    def test_equal_symbol_with_double_quote(self):
        self.assertEqual(split('a="b=c"'), ["a", "b=c"])

    def test_equal_symbol_with_single_quote(self):
        self.assertEqual(split("a='b=c'"), ["a", "b=c"])

    def real_example(self):
        source = """mocodo --mld --colors = brewer+1 --shapes=copperplate --relations mysql markdown text --title="foobar" --left_gutter_alt_ids "(1)" 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣\""""
        expected = [
            "mocodo",
            "--mld",
            "--colors",
            "brewer+1",
            "--shapes",
            "copperplate",
            "--relations",
            "mysql",
            "markdown",
            "text",
            "--title",
            "foobar",
            "--left_gutter_alt_ids",
            "(1)",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            "8️⃣",
            "9️⃣",
        ]
        self.assertEqual(split(source), expected)


if __name__ == "__main__":
    unittest.main()
