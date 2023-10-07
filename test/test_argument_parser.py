import unittest
import argparse

__import__("sys").path[0:0] = ["mocodo"]

from mocodo.argument_parser import extract_subargs


class TestSubArguments(unittest.TestCase):
    def test_extract_subargs(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--actual",
            metavar="STR",
            nargs="*",
            type=extract_subargs,
        )
        args = parser.parse_args(
            [  # NB: names not necessarily the same as in the current version
                "--actual",
                "arrange:algo=bb,grid=organic",
                "randomize:cards=_/,types=mysql,labels=four_letter_words",
                "map:ascii=labels,n=3,x=3.14,delete='',guess=types,create=types",
                "drain",
                "flip:vertical,horizontal,diagonal",
                """data_dict:type,box="",label="libellé de l'attribut",tsv""",
            ]
        )
        expected = [
            (
                "arrange",
                {"algo": "bb", "grid": "organic"},
            ),
            (
                "randomize",
                {"cards": "_/", "types": "mysql", "labels": "four_letter_words"},
            ),
            (
                "map",
                {"ascii": "labels", "n": "3", "x": "3.14", "delete": "", "guess": "types", "create": "types"},
            ),
            ("drain", {}),
            (
                "flip",
                {"vertical": None, "horizontal": None, "diagonal": None},
            ),
            (
                "data_dict",
                {"type": None, "box": "", "label": "libellé de l'attribut", "tsv": None}
            ),
        ]
        self.assertEqual(args.actual, expected)


if __name__ == "__main__":
    unittest.main()
