#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys
sys.path[0:0] = ["."]

from mocodo.arrange_bb import *

import unittest
from mocodo.mcd import Mcd
from mocodo.argument_parser import parsed_arguments
from time import time
from random import seed

# WARNING: by default, this should fail for Python 3.
# Set PYTHONHASHSEED to 0 before launching the tests.
# cf. http://stackoverflow.com/questions/38943038/difference-between-python-2-and-3-for-shuffle-with-a-given-seed/

class ArrangeBB(unittest.TestCase):
    
    def test_constrained_rearrangement(self):
        clauses = u"""
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
        """.replace("  ", "")
        params = parsed_arguments()
        mcd = Mcd(clauses.split("\n"), params)
        params.update(mcd.get_layout_data())
        params["organic"] = False
        params["call_limit"] = 10000
        params["max_objective"] = 15
        params["min_objective"] = 0
        params["timeout"] = None
        params["verbose"] = False
        seed(42 if sys.version_info.major == 2 else 1)
        rearrangement = arrange(**params)
        mcd.set_layout(**rearrangement)
        result = mcd.get_clauses()
        self.assertEqual(rearrangement, {
            'distances': 0.8284271247461903,
            'crossings': 0,
            'coords': {
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
                11: (0, 0)
            },
            'layout': [11, 3, 0, 4, 10, 7, 1, 5, 8, 6, 2, 9]
        })
        self.assertEqual(result, u"""
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
        """.strip().replace("  ", ""))
    
    def test_non_connected_graph(self):
        clauses = u"""
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
        """.replace("  ", "")
        params = parsed_arguments()
        mcd = Mcd(clauses.split("\n"), params)
        params.update(mcd.get_layout_data())
        params["organic"] = False
        params["call_limit"] = 10000
        params["max_objective"] = 15
        params["min_objective"] = 0
        params["timeout"] = None
        params["verbose"] = False
        seed(42 if sys.version_info.major == 2 else 129)
        rearrangement = arrange(**params)
        mcd.set_layout(**rearrangement)
        self.assertEqual(rearrangement, {
            'distances': 0.0,
            'crossings': 0,
            'coords': {
                0: (2, 2),
                1: (2, 1),
                2: (2, 0),
                3: (0, 0),
                4: (3, 2),
                5: (3, 1),
                6: (0, 1),
                7: (1, 0),
                8: (0, 2),
                9: (3, 0),
                10: (1, 2),
                11: (1, 1)
            },
            'layout': [3, 7, 2, 9, 6, 11, 1, 5, 8, 10, 0, 4]
        })
        expected = u"""
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM
            :
            CONSECTETUER: elit, sed
            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing

            DIGNISSIM: ligula, massa, varius
            SEMPER, 0N RISUS, 1N DIGNISSIM
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            LOREM: ipsum, dolor, sit

            DF, 11 RISUS, 0N RISUS
            RISUS: ultricies, _cras, elementum
            SUSPENDISSE: diam
            DF1, 11 LOREM, 1N SUSPENDISSE
        """.strip().replace("  ", "")
        result = mcd.get_clauses()
        self.assertEqual(expected, result)

    def test_no_links(self):
        clauses = u"""
            SUSPENDISSE: diam
            CONSECTETUER: elit, sed

            LOREM: ipsum, dolor, sit
            DIGNISSIM: ligula, massa, varius

            RISUS: ultricies, _cras, elementum
        """.replace("  ", "")
        params = parsed_arguments()
        mcd = Mcd(clauses.split("\n"), params)
        params.update(mcd.get_layout_data())
        params["organic"] = False
        params["call_limit"] = 10000
        params["max_objective"] = 15
        params["min_objective"] = 0
        params["timeout"] = None
        params["verbose"] = False
        seed(1 if sys.version_info.major == 2 else 458)
        expected = u"""
            :
            CONSECTETUER: elit, sed
            :
            LOREM: ipsum, dolor, sit
            :

            :::
            DIGNISSIM: ligula, massa, varius
            :

            :
            RISUS: ultricies, _cras, elementum
            :
            SUSPENDISSE: diam
            :
        """.strip().replace("  ", "")
        rearrangement = arrange(**params)
        self.assertEqual(rearrangement, {
            'distances': 0.0,
            'layout': [1, 2, 5, 3, 4, 0],
            'crossings': 0,
        })
        mcd.set_layout(**rearrangement)
        result = mcd.get_clauses()
        self.assertEqual(expected, result)
    
    def test_organic_rearrangement(self):
        clauses = u"""
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
        """.replace("  ", "")
        params = parsed_arguments()
        mcd = Mcd(clauses.split("\n"), params)
        params.update(mcd.get_layout_data())
        params["organic"] = True
        params["call_limit"] = 10000
        params["max_objective"] = 15
        params["min_objective"] = 0
        params["timeout"] = None
        params["verbose"] = False
        seed(1 if sys.version_info.major == 2 else 299)
        expected = u"""
            DF1, 11 LOREM, 1N SUSPENDISSE
            LOREM: ipsum, dolor, sit
            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
            :

            SUSPENDISSE: diam
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            CONSECTETUER: elit, sed
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM

            ::
            TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
            DIGNISSIM: ligula, massa, varius

            ::
            RISUS: ultricies, _cras, elementum
            SEMPER, 0N RISUS, 1N DIGNISSIM

            ::
            DF, 11 RISUS, 0N RISUS
            :
        """.strip().replace("  ", "")
        rearrangement = arrange(**params)
        self.assertEqual(rearrangement, {
            'distances': 0.0,
            'layout': [4, 5, 9, None, 0, 1, 2, 3, None, None, 6, 7, None, None, 10, 11, None, None, 8, None],
            'crossings': 0,
            'col_count': 4,
            'row_count': 5,
            'coords': {
                0: (0, 1),
                1: (1, 1),
                2: (2, 1),
                3: (3, 1),
                4: (0, 0),
                5: (1, 0),
                6: (2, 2),
                7: (3, 2),
                8: (2, 4),
                9: (2, 0),
                10: (2, 3),
                11: (3, 3)
            }
        })
        mcd.set_layout(**rearrangement)
        result = mcd.get_clauses()
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
