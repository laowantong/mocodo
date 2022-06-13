#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import sys
sys.path[0:0] = ["."]

from arrange_lp import *

import unittest
from mocodo.mcd import Mcd
from mocodo.argument_parser import parsed_arguments
from time import time
from random import seed

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


class ArrangeLP(unittest.TestCase):
    
    def test_with_cplex(self):
        params["engine"] = "cplex"
        rearrangement = arrange(**params)
        mcd.set_layout(**rearrangement)
        result = mcd.get_clauses()
        self.assertEqual(rearrangement["crossings"], 0)
        self.assertEqual(round(rearrangement["distances"], 4), 0.8284)
        self.assertEqual(rearrangement["layout"], [11, 3, 0, 4, 10, 7, 1, 5, 8, 6, 2, 9])
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
    
    def test_with_gurobi(self):
        params["engine"] = "gurobi"
        rearrangement = arrange(**params)
        mcd.set_layout(**rearrangement)
        result = mcd.get_clauses()
        self.assertEqual(rearrangement["crossings"], 0)
        self.assertEqual(round(rearrangement["distances"], 4), 0.8284)
        self.assertEqual(rearrangement["layout"], [4, 0, 3, 11, 5, 1, 7, 10, 9, 2, 6, 8])
        self.assertEqual(result, u"""
            DF1, 11 LOREM, 1N SUSPENDISSE
            SUSPENDISSE: diam
            MAECENAS, 1N DIGNISSIM, 1N DIGNISSIM
            SEMPER, 0N RISUS, 1N DIGNISSIM

            LOREM: ipsum, dolor, sit
            SOLLICITUDIN, 0N SUSPENDISSE, 0N CONSECTETUER, 0N LOREM: lectus
            DIGNISSIM: ligula, massa, varius
            RISUS: ultricies, _cras, elementum

            AMET, 11> LOREM, 01 CONSECTETUER: adipiscing
            CONSECTETUER: elit, sed
            TORTOR, 0N RISUS, 11 DIGNISSIM, 1N CONSECTETUER: nec
            DF, 11 RISUS, 0N RISUS
        """.strip().replace("  ", ""))
    


if __name__ == '__main__':
    unittest.main()
