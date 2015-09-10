#!/usr/bin/python
# encoding: utf-8

from mocodo.arrange_bb import *

import unittest
from mocodo.mcd import Mcd
from mocodo.argument_parser import parsed_arguments
from time import time
from random import seed

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
        seed(42)
        expected = u"""
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
        """.strip().replace("  ", "")
        rearrangement = arrange(**params)
        self.assertEquals(rearrangement, {
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
        result = mcd.get_clauses_from_layout(**rearrangement)
        self.assertEquals(expected, result)

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
        seed(1)
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
        self.assertEquals(rearrangement, {
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
        result = mcd.get_clauses_from_layout(**rearrangement)
        self.assertEquals(expected, result)


if __name__ == '__main__':
    unittest.main()
