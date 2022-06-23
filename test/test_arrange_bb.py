import unittest
from random import seed

__import__("sys").path[0:0] = ["mocodo"]
from mocodo.argument_parser import parsed_arguments
from mocodo.arrange_bb import *
from mocodo.mcd import Mcd


# WARNING: by default, this should fail for Python 3.
# Set PYTHONHASHSEED to 0 before launching the tests.
# cf. http://stackoverflow.com/questions/38943038/difference-between-python-2-and-3-for-shuffle-with-a-given-seed/

class ArrangeBB(unittest.TestCase):
    def test_constrained_rearrangement(self):
        clauses = """
            SUSPENDISSE: diam
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            CONSECTETUER: elit, sed
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM

            DF1, 11 LOREM, 1N SUSPENDISSE
            LOREM: ipsum, dolor, sit
            TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
            DIGNISSIM: ligula, massa, varius

            DF, 11 RISUS, 0N RISUS
            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
            RISUS: ultricies, _cras, elementum
            SEMPER, 0N RISUS, 1N DIGNISSIM
        """
        params = parsed_arguments()
        mcd = Mcd(clauses.split("\n"), params)
        params.update(mcd.get_layout_data())
        params["organic"] = False
        params["call_limit"] = 10000
        params["max_objective"] = 15
        params["min_objective"] = 0
        params["timeout"] = None
        params["verbose"] = False
        seed(42)
        rearrangement = arrange(**params)
        mcd.set_layout(**rearrangement)
        expected = {
            "coords": {
                0: (2, 0),
                1: (2, 1),
                2: (2, 2),
                3: (1, 0),
                4: (3, 0),
                5: (3, 1),
                6: (1, 2),
                7: (1, 1),
                8: (0, 2),
                9: (3, 2),
                10: (0, 1),
                11: (0, 0),
            },
            "crossings": 0,
            "distances": 0.8284271247461903,
            "layout": [11, 3, 0, 4, 10, 7, 1, 5, 8, 6, 2, 9],
        }
        self.assertEqual(rearrangement, expected)
        result = mcd.get_clauses()
        expected = """
            SEMPER, 0N RISUS, 1N DIGNISSIM
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM
            SUSPENDISSE: diam
            DF1, 11 LOREM, 1N SUSPENDISSE

            RISUS: ultricies, _cras, elementum
            DIGNISSIM: ligula, massa, varius
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            LOREM: ipsum, dolor, sit

            DF, 11 RISUS, 0N RISUS
            TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
            CONSECTETUER: elit, sed
            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
        """
        self.assertEqual(result, expected.strip().replace("  ", ""))

    def test_non_connected_graph(self):
        clauses = """
            SUSPENDISSE: diam
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            CONSECTETUER: elit, sed
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM

            DF1, 11 LOREM, 1N SUSPENDISSE
            LOREM: ipsum, dolor, sit
            DIGNISSIM: ligula, massa, varius

            DF, 11 RISUS, 0N RISUS
            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
            RISUS: ultricies, _cras, elementum
            SEMPER, 0N RISUS, 1N DIGNISSIM
        """
        params = parsed_arguments()
        mcd = Mcd(clauses.split("\n"), params)
        params.update(mcd.get_layout_data())
        params["organic"] = False
        params["call_limit"] = 10000
        params["max_objective"] = 15
        params["min_objective"] = 0
        params["timeout"] = None
        params["verbose"] = False
        seed(42)
        rearrangement = arrange(**params)
        expected = {
            "coords": {
                0: (0, 2),
                1: (0, 1),
                2: (0, 0),
                3: (2, 1),
                4: (1, 2),
                5: (1, 1),
                6: (2, 2),
                7: (2, 0),
                8: (3, 0),
                9: (1, 0),
                10: (3, 1),
                11: (3, 2),
            },
            "crossings": 0,
            "distances": 0.0,
            "layout": [2, 9, 7, 8, 1, 5, 3, 10, 0, 4, 6, 11],
        }
        self.assertEqual(rearrangement, expected)
        mcd.set_layout(**rearrangement)
        expected = """
            CONSECTETUER: elit, sed
            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
            :
            DF, 11 RISUS, 0N RISUS

            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            LOREM: ipsum, dolor, sit
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM
            RISUS: ultricies, _cras, elementum

            SUSPENDISSE: diam
            DF1, 11 LOREM, 1N SUSPENDISSE
            DIGNISSIM: ligula, massa, varius
            SEMPER, 0N RISUS, 1N DIGNISSIM
        """
        self.assertEqual(mcd.get_clauses(), expected.strip().replace("  ", ""))

    def test_no_links(self):
        clauses = """
            SUSPENDISSE: diam
            CONSECTETUER: elit, sed

            LOREM: ipsum, dolor, sit
            DIGNISSIM: ligula, massa, varius

            RISUS: ultricies, _cras, elementum
        """
        params = parsed_arguments()
        mcd = Mcd(clauses.split("\n"), params)
        params.update(mcd.get_layout_data())
        params["organic"] = False
        params["call_limit"] = 10000
        params["max_objective"] = 15
        params["min_objective"] = 0
        params["timeout"] = None
        params["verbose"] = False
        seed(458)
        expected = """
            :
            CONSECTETUER: elit, sed
            :
            LOREM: ipsum, dolor, sit
            :

            :
            :
            :
            DIGNISSIM: ligula, massa, varius
            :

            :
            RISUS: ultricies, _cras, elementum
            :
            SUSPENDISSE: diam
            :
        """.strip().replace(
            "  ", ""
        )
        rearrangement = arrange(**params)
        self.assertEqual(
            rearrangement,
            {
                "distances": 0.0,
                "layout": [1, 2, 5, 3, 4, 0],
                "crossings": 0,
            },
        )
        mcd.set_layout(**rearrangement)
        result = mcd.get_clauses()
        self.assertEqual(expected, result)

    def test_organic_rearrangement(self):
        clauses = """
            SUSPENDISSE: diam
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            CONSECTETUER: elit, sed
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM

            DF1, 11 LOREM, 1N SUSPENDISSE
            LOREM: ipsum, dolor, sit
            TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
            DIGNISSIM: ligula, massa, varius

            DF, 11 RISUS, 0N RISUS
            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
            RISUS: ultricies, _cras, elementum
            SEMPER, 0N RISUS, 1N DIGNISSIM
        """.replace(
            "  ", ""
        )
        params = parsed_arguments()
        mcd = Mcd(clauses.split("\n"), params)
        params.update(mcd.get_layout_data())
        params["organic"] = True
        params["call_limit"] = 10000
        params["max_objective"] = 15
        params["min_objective"] = 0
        params["timeout"] = None
        params["verbose"] = False
        seed(42)
        expected = {
            "coords": {
                7: (3, 2),
                11: (3, 3),
                3: (4, 2),
                6: (2, 2),
                10: (2, 3),
                2: (1, 2),
                8: (2, 4),
                1: (1, 1),
                9: (0, 2),
                5: (0, 1),
                0: (1, 0),
                4: (0, 0),
            },
            "crossings": 0,
            "distances": 0.0,
            "row_count": 5,
            "col_count": 5,
            "layout": [4, 0, None, None, None, 5, 1, None, None, None, 9, 2, 6, 7, 3, None, None, 10, 11, None, None, None, 8, None, None],  # fmt: skip
        }
        rearrangement = arrange(**params)
        self.assertEqual(rearrangement, expected)
        expected = """
            DF1, 11 LOREM, 1N SUSPENDISSE
            SUSPENDISSE: diam
            :
            :
            :

            LOREM: ipsum, dolor, sit
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            :
            :
            :

            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
            CONSECTETUER: elit, sed
            TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
            DIGNISSIM: ligula, massa, varius
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM

            :
            :
            RISUS: ultricies, _cras, elementum
            SEMPER, 0N RISUS, 1N DIGNISSIM
            :

            :
            :
            DF, 11 RISUS, 0N RISUS
            :
            :
        """
        mcd.set_layout(**rearrangement)
        self.assertEqual(mcd.get_clauses(), expected.strip().replace("  ", ""))


if __name__ == "__main__":
    unittest.main()
